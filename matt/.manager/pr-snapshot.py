#!/usr/bin/env python3
"""Export customized PR skills and load a verified, commit-pinned task copy."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

MANAGER = Path(__file__).resolve().parent
REMOTE_ROOT = "matt/.manager/pr-distribution"
REQUIRED = {"SKILL.md", "agents/openai.yaml", "CREDITS.md", "LICENSE"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def safe_path(name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or ".." in p.parts or str(p) != name or "\\" in name:
        raise ValueError(f"unsafe snapshot path: {name!r}")
    if name in {"manifest.json", ".snapshot-pin.json"}:
        raise ValueError(f"reserved snapshot path: {name}")
    return name


def read_file(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"expected regular file: {path}")
    for parent in path.parents:
        if parent.is_symlink():
            raise ValueError(f"symlink in snapshot path: {parent}")
    return path.read_bytes()


def validate_manifest(data, version):
    if not re.fullmatch(r"[0-9a-f]{64}", version) or digest(data) != version:
        raise ValueError("snapshot manifest hash mismatch")
    manifest = json.loads(data)
    if manifest.get("schema") != 1 or manifest.get("skill") != "pr":
        raise ValueError("unsupported snapshot manifest")
    files = manifest["files"]
    if not REQUIRED.issubset(files):
        raise ValueError("incomplete PR snapshot manifest")
    for name, record in files.items():
        safe_path(name)
        if not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]):
            raise ValueError("invalid file hash")
        if not isinstance(record["bytes"], int) or not 0 <= record["bytes"] <= 2_000_000:
            raise ValueError("invalid file size")
    return manifest


def validate_file(data, record, name):
    if len(data) != record["bytes"] or digest(data) != record["sha256"]:
        raise ValueError(f"snapshot file hash/size mismatch: {name}")


def verify(directory, version, pinned=False):
    manifest = validate_manifest(read_file(directory / "manifest.json"), version)
    expected = set(manifest["files"]) | {"manifest.json"}
    if pinned:
        expected.add(".snapshot-pin.json")
    actual = set()
    for p in directory.rglob("*"):
        if p.is_symlink():
            raise ValueError(f"unexpected symlink: {p}")
        if p.is_file():
            actual.add(p.relative_to(directory).as_posix())
        elif not p.is_dir():
            raise ValueError(f"unexpected filesystem entry: {p}")
    if actual != expected:
        raise ValueError("snapshot file inventory mismatch")
    for name, record in manifest["files"].items():
        validate_file(read_file(directory / name), record, name)
    return manifest


def snapshot(manager):
    skill = manager.parent / "pr"
    files = {}
    for p in sorted(skill.rglob("*")):
        if p.is_symlink():
            raise ValueError("skill export does not follow symlinks")
        if p.is_file():
            files[safe_path(p.relative_to(skill).as_posix())] = read_file(p)
    if "LICENSE" in files:
        raise ValueError("review upstream skill LICENSE before replacing distribution license")
    files["LICENSE"] = read_file(manager / "pr-upstream-LICENSE")
    lock = json.loads(read_file(manager / "skills-lock.json"))["skills"]["pr"]
    patches = {p.name: digest(read_file(p)) for p in sorted((manager / "patches").glob("pr-*.patch"))}
    manifest = encoded({"schema": 1, "skill": "pr", "provenance": {
        "upstream": lock, "patches": patches,
        "source_repository": "https://github.com/andrewsoonqn/skills",
        "license_source": "https://github.com/mattpocock/skills/blob/main/LICENSE",
    }, "files": {n: {"sha256": digest(b), "bytes": len(b)} for n, b in sorted(files.items())}})
    version = digest(manifest)
    validate_manifest(manifest, version)
    return files, manifest, version


def check(manager):
    _, _, version = snapshot(manager)
    root = manager / "pr-distribution"
    pointer = json.loads(read_file(root / "latest.json"))
    if pointer != {"schema": 1, "skill": "pr", "version": version}:
        raise ValueError("distribution does not match customized rendered PR skill")
    verify(root / "versions" / version, version)
    print(version)


def export(manager):
    files, manifest, version = snapshot(manager)
    root = manager / "pr-distribution"
    versions = root / "versions"
    versions.mkdir(parents=True, exist_ok=True)
    destination = versions / version
    if destination.exists():
        verify(destination, version)
    else:
        with tempfile.TemporaryDirectory(prefix=".export-", dir=versions) as temporary:
            stage = Path(temporary) / "snapshot"
            stage.mkdir()
            for name, data in files.items():
                p = stage / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
            (stage / "manifest.json").write_bytes(manifest)
            verify(stage, version)
            stage.rename(destination)
    pointer = root / ".latest.tmp"
    pointer.write_bytes(encoded({"schema": 1, "skill": "pr", "version": version}))
    os.replace(pointer, root / "latest.json")
    print(version)
    return version


def load(args):
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        raise ValueError("use a full immutable Git commit SHA, not a branch or tag")
    if args.repo and not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        raise ValueError("invalid GitHub repository")

    def fetch(path):
        if args.source:
            return read_file(args.source.resolve() / path)
        response = subprocess.check_output([
            "gh", "api", f"repos/{args.repo}/contents/{REMOTE_ROOT}/{path}?ref={args.revision}"
        ])
        result = json.loads(response)
        if result.get("encoding") != "base64" or result.get("type") != "file":
            raise ValueError("GitHub did not return file contents")
        return base64.b64decode("".join(result["content"].split()), validate=True)

    if args.destination.is_symlink():
        raise ValueError("task destination must not be a symlink")
    destination = args.destination.resolve()
    # Never silently refresh an existing task, even if latest has advanced.
    if destination.exists() or destination.is_symlink():
        pin = json.loads(read_file(destination / ".snapshot-pin.json"))
        if pin["revision"] != args.revision or pin["repository"] != args.repo:
            raise ValueError("task already pinned to another revision; use a fresh task directory")
        verify(destination, pin["version"], pinned=True)
        print(json.dumps(pin, sort_keys=True))
        return
    pointer = json.loads(fetch("latest.json"))
    if pointer.get("schema") != 1 or pointer.get("skill") != "pr":
        raise ValueError("unsupported snapshot pointer")
    version = pointer["version"]
    if not re.fullmatch(r"[0-9a-f]{64}", version):
        raise ValueError("invalid snapshot version")
    prefix = f"versions/{version}/"
    data = fetch(prefix + "manifest.json")
    manifest = validate_manifest(data, version)
    pin = {"repository": args.repo, "revision": args.revision, "version": version}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".pr-load-", dir=destination.parent) as temporary:
        stage = Path(temporary) / "skill"
        stage.mkdir()
        (stage / "manifest.json").write_bytes(data)
        for name, record in manifest["files"].items():
            content = fetch(prefix + name)
            validate_file(content, record, name)
            p = stage / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(content)
        (stage / ".snapshot-pin.json").write_bytes(encoded(pin))
        verify(stage, version, pinned=True)
        stage.rename(destination)
    print(json.dumps(pin, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    exp = commands.add_parser("export", help="called by manager after validation")
    exp.add_argument("--manager", type=Path, default=MANAGER)
    chk = commands.add_parser("check", help="verify export matches the current managed skill")
    chk.add_argument("--manager", type=Path, default=MANAGER)
    ld = commands.add_parser("load", help="verify one commit's snapshot into a fresh task directory")
    source = ld.add_mutually_exclusive_group(required=True)
    source.add_argument("--source", type=Path, help="distribution directory downloaded by connector at --revision")
    source.add_argument("--repo", help="GitHub owner/repo; use existing gh authentication")
    ld.add_argument("--revision", required=True)
    ld.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "export":
        export(args.manager.resolve())
    elif args.command == "check":
        check(args.manager.resolve())
    else:
        load(args)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"PR snapshot failed: {error}")

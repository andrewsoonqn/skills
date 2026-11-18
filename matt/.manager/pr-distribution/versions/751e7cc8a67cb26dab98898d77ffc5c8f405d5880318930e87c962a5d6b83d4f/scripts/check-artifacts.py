#!/usr/bin/env python3
"""Flag likely agent audit artifacts in index, PR diff, and optional PR body.

Read-only heuristic. Exit 0: resolved/clear, 1: unresolved flags, 2: check error.
No extension/directory allowlist: application JSON and docs are valid inputs.
"""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys

MAX_BYTES = 8 * 1024 * 1024


def reasons(path, data):
    found = []
    name = Path(path).name.lower()
    if re.search(r"(?:reviewer|review|agent|model)[-_. ](?:transcript|provenance|process[-_. ]dump|debug[-_. ]dump)(?:[-_. ]|$)", name):
        found.append("audit-style filename")
    if len(data) > MAX_BYTES:
        return found + ["over 8 MiB: content requires manual inspection"]
    if b"\0" in data:
        return found  # Binary content is outside text-signature coverage.
    text = data.decode("utf-8", errors="replace")
    # Require repeated transcript framing or paired metadata, not ordinary prose
    # mentioning reviewers, models, or application fields individually.
    if len(re.findall(r'(?m)^\s*(?:assistant|user|system|tool)\s*(?:[:>]|\(analysis\)|\(final\))', text, re.I)) >= 3:
        found.append("repeated conversation role framing")
    roles = re.findall(r'"role"\s*:\s*"(?:assistant|system|tool|user)"', text)
    if len(roles) >= 3 and re.search(r'"(?:content|tool_calls)"\s*:', text):
        found.append("serialized conversation messages")
    keys = set(re.findall(r'"([a-z_]+)"\s*:', text.lower()))
    if keys & {"model", "model_id", "model_name"} and keys & {"reviewer_id", "agent_id", "reasoning_effort", "provider", "model_provider"}:
        found.append("model/reviewer provenance metadata")
    if ("<|im_start|>" in text or "<|start_header_id|>" in text
            or ("agent_settled" in text and '"type"' in text)
            or ("tool_call_id" in keys and keys & {"session_id", "agent_id"})):
        found.append("agent runtime/transcript markers")
    return found


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise ValueError("Git check failed: " + result.stderr.decode(errors="replace").strip())
    return result.stdout


def check(args):
    root = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip())
    # Resolve to immutable object IDs so revisions cannot be interpreted as options.
    base = git(root, "rev-parse", "--verify", "--end-of-options", args.base + "^{commit}").decode().strip()
    head = git(root, "rev-parse", "--verify", "HEAD^{commit}").decode().strip()
    merge = git(root, "merge-base", base, head).decode().strip()
    inputs = []
    for scope, options, ref in (("staged", ["--cached"], ":"),
                                ("diff", [merge, head], head + ":")):
        paths = git(root, "diff", "--no-ext-diff", "--no-renames", "--name-only", "-z", "--diff-filter=ACM", *options, "--").split(b"\0")
        for raw in paths:
            if raw:
                path = raw.decode(sys.getfilesystemencoding(), errors="surrogateescape")
                inputs.append((scope, path, git(root, "cat-file", "blob", ref + path)))
    if args.pr_body:
        inputs.append(("body", str(args.pr_body), args.pr_body.read_bytes()))
    allowed = {}
    for path, sha, reason in args.allow:
        if not re.fullmatch(r"[a-f0-9]{64}", sha) or len(reason.strip()) < 15:
            raise ValueError("--allow needs PATH, exact SHA256, and a substantive application-purpose reason (15+ characters)")
        allowed[(path, sha)] = reason
    unresolved = 0
    used = set()
    for scope, path, data in inputs:
        flags = reasons(path if scope != "body" else "", data)
        if not flags:
            continue
        sha = hashlib.sha256(data).hexdigest()
        key = (path, sha)
        if key in allowed:
            used.add(key)
            print(f"RESOLVED {scope} {path!r} sha256={sha}: {allowed[key]}")
        else:
            unresolved += 1
            print(f"FLAG {scope} {path!r} sha256={sha}: {'; '.join(flags)}")
    if set(allowed) - used:
        raise ValueError("unused/stale --allow: rerun and review the current flagged content")
    print(f"Checked {len(inputs)} index/diff/body inputs; {unresolved} unresolved. Heuristics do not prove absence of process artifacts.")
    return bool(unresolved)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True, help="intended PR base ref; merge-base..HEAD is checked")
    parser.add_argument("--pr-body", type=Path, help="also inspect the exact draft body")
    parser.add_argument("--allow", nargs=3, action="append", default=[], metavar=("PATH", "SHA256", "REASON"))
    args = parser.parse_args()
    try:
        return int(check(args))
    except (OSError, ValueError) as error:
        print(f"Artifact check incomplete: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

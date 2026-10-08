#!/usr/bin/env python3
"""Exercise the real manager against isolated skill trees and harness homes."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

source = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix="matt-harness-test-") as temporary:
    root = Path(temporary)
    tree = root / "skills" / "matt"
    shutil.copytree(source, tree)
    home = root / "home"
    home.mkdir()
    env = dict(os.environ, HOME=str(home))
    manager = tree / ".manager" / "manage.sh"
    names = (tree / ".manager" / "skills.txt").read_text().splitlines()

    def run(mode, success=True):
        result = subprocess.run([str(manager), mode], env=env, text=True, capture_output=True)
        assert (result.returncode == 0) == success, result.stdout + result.stderr
        return result

    # A late conflict must prevent links in either harness, not just the conflicting one.
    conflict = home / ".gemini" / "skills" / names[-1]
    conflict.mkdir(parents=True)
    marker = conflict / "keep.txt"
    marker.write_text("unrelated user content")
    run("link-harnesses", success=False)
    assert not (home / ".claude").exists()
    assert marker.read_text() == "unrelated user content"
    shutil.rmtree(conflict)

    unrelated = home / ".gemini" / "skills" / "unrelated"
    unrelated.mkdir()
    run("verify-harnesses", success=False)
    run("link-harnesses")
    second = run("link-harnesses")
    assert "Created 0 links" in second.stdout
    run("verify-harnesses")
    assert unrelated.is_dir()

    for harness in (".claude", ".gemini"):
        for name in names:
            link = home / harness / "skills" / name
            assert link.is_symlink() and link.resolve() == (tree / name).resolve()
            for file in (tree / name).rglob("*"):
                if file.is_file():
                    assert (link / file.relative_to(tree / name)).read_bytes() == file.read_bytes()

    # An atomic source replacement must leave the harness links valid.
    previous = tree.with_name("previous")
    tree.rename(previous)
    shutil.copytree(previous, tree)
    run("verify-harnesses")

    link = home / ".claude" / "skills" / names[0]
    link.unlink()
    link.symlink_to(root / "missing")
    run("link-harnesses", success=False)
    assert link.is_symlink() and not link.exists()
    link.unlink()
    run("link-harnesses")

    # Refuse a symlinked harness root rather than writing into an unknown tree.
    claude_skills = home / ".claude" / "skills"
    claude_skills.rename(home / ".claude" / "original")
    elsewhere = root / "elsewhere"
    elsewhere.mkdir()
    claude_skills.symlink_to(elsewhere, target_is_directory=True)
    run("link-harnesses", success=False)
    assert not list(elsewhere.iterdir())

print(f"PASS: {2 * len(names)} links, all supporting files, idempotency, source replacement, conflict preflight, broken links, and symlink-root safety")

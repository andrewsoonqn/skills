#!/usr/bin/env python3
"""Exercise export, task pinning, and real manager updates without live changes."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

MANAGER = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("snapshot", MANAGER / "pr-snapshot.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def run(argv, success=True, env=None):
    result = subprocess.run([str(a) for a in argv], capture_output=True, text=True, env=env)
    assert (result.returncode == 0) == success, result.stdout + result.stderr
    return result


with tempfile.TemporaryDirectory(prefix="pr-snapshot-test-") as tmp:
    root = Path(tmp).resolve()
    manager = root / "skills/matt/.manager"
    manager.parent.mkdir(parents=True)
    shutil.copytree(MANAGER, manager)
    shutil.rmtree(manager / "pr-distribution", ignore_errors=True)
    skill = manager.parent / "pr"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text('---\nname: pr\ndescription: fixture\n---\nbase fixture\n')
    (skill / "CREDITS.md").write_text('Fixture attribution\n')
    (skill / "agents/openai.yaml").write_text('interface:\n  display_name: PR\n')
    (manager / "skills.txt").write_text('pr\n')
    lock = {"skills": {"pr": {"source": "mattpocock/skills", "skillPath": "fixture/pr/SKILL.md", "computedHash": "fixture"}}}
    (manager / "skills-lock.json").write_text(json.dumps(lock))
    shutil.rmtree(manager / "patches")
    (manager / "patches").mkdir()
    (manager / "patches/pr-fixture.patch").write_text(
        '--- a/pr/SKILL.md\n+++ b/pr/SKILL.md\n@@ -2,4 +2,4 @@\n name: pr\n description: fixture\n ---\n-base fixture\n+customized fixture\n')
    # Fake only the installer transport. Run the actual manager's patching,
    # validation, snapshot export, atomic replacement, and post-install checks.
    upstream = root / "upstream"
    shutil.copytree(skill, upstream / "pr")
    (upstream / "skills-lock.json").write_text(json.dumps(lock))
    bin_dir = root / "bin"
    bin_dir.mkdir()
    npx = bin_dir / "npx"
    npx.write_text('''#!/usr/bin/env python3
import os, pathlib, shutil
source=pathlib.Path(os.environ['FIXTURE_UPSTREAM'])
target=pathlib.Path.cwd()/'.pi/skills'
target.mkdir(parents=True)
shutil.copytree(source/'pr', target/'pr')
shutil.copy2(source/'skills-lock.json', pathlib.Path.cwd()/'skills-lock.json')
''')
    npx.chmod(0o755)
    env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ["PATH"], FIXTURE_UPSTREAM=str(upstream), PYTHONDONTWRITEBYTECODE="1")
    manage = manager / "manage.sh"
    loader = manager / "pr-snapshot.py"
    run(["sh", manage, "update"], env=env)
    run(["sh", manage, "verify"], env=env)
    distribution = manager / "pr-distribution"
    pointer = (distribution / "latest.json").read_bytes()
    version1 = json.loads(pointer)["version"]
    expected = (skill / "SKILL.md").read_bytes()
    assert b'customized fixture' in expected
    # Repeat exporter and full update: byte-identical pointer and snapshot.
    run(["python3", loader, "export"])
    assert (distribution / "latest.json").read_bytes() == pointer
    run(["sh", manage, "update"], env=env)
    assert (distribution / "latest.json").read_bytes() == pointer

    revision1, revision2 = "a" * 40, "b" * 40
    task = root / "task/pr"
    def load(destination, revision=revision1, success=True):
        return run(["python3", loader, "load", "--source", distribution, "--revision", revision,
                    "--destination", destination], success)
    load(task)
    assert (task / "SKILL.md").read_bytes() == expected
    load(task)  # repeat invocation verifies and reuses the pin
    load(root / "branch-ref", revision="main", success=False)
    assert not (root / "branch-ref").exists()

    snapshot_skill = distribution / "versions" / version1 / "SKILL.md"
    snapshot_skill.write_bytes(expected + b'tampered')
    load(root / "tampered", success=False)
    assert not (root / "tampered").exists()
    snapshot_skill.unlink()
    load(root / "incomplete", success=False)
    assert not (root / "incomplete").exists()
    snapshot_skill.write_bytes(expected)
    # A model/user cannot silently switch an existing task to another commit.
    load(task, revision2, success=False)
    (task / "SKILL.md").write_bytes(b'tampered task')
    load(task, success=False)
    (task / "SKILL.md").write_bytes(expected)

    # A real manager update propagates a changed disposable fixture only.
    with (upstream / "pr/CREDITS.md").open('a') as output:
        output.write('\nnext fixture version\n')
    run(["sh", manage, "update"], env=env)
    run(["sh", manage, "verify"], env=env)
    version2 = json.loads((distribution / "latest.json").read_bytes())["version"]
    assert version2 != version1
    assert (distribution / "versions" / version1 / "SKILL.md").read_bytes() == expected
    load(task)  # pinned task does not fetch newer latest
    assert (task / "SKILL.md").read_bytes() == expected
    load(root / "new-task/pr", revision2)
    assert b'next fixture version' in (root / "new-task/pr/CREDITS.md").read_bytes()

    # Corrupt upstream and fail patching: previous skill and pointer survive.
    previous = (skill / "SKILL.md").read_bytes()
    pointer = (distribution / "latest.json").read_bytes()
    (upstream / "pr/SKILL.md").write_text('broken upstream\n')
    run(["sh", manage, "update"], success=False, env=env)
    assert (skill / "SKILL.md").read_bytes() == previous
    assert (distribution / "latest.json").read_bytes() == pointer

print('PASS: deterministic export/update, patched fixture propagation, original-version retention, immutable task pins, tampering/incomplete rejection, failed-update preservation')

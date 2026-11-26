#!/usr/bin/env python3
"""Regression expectations come from the publication boundary and incident.

Use real Git index/commits: worktree substitutions must not hide staged dumps.
All fixtures are synthetic, disposable application or process examples.
"""
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

MANAGER = Path(__file__).resolve().parent
CHECK = MANAGER.parent / "pr/scripts/check-artifacts.py"


with tempfile.TemporaryDirectory(prefix="pr-artifacts-") as tmp:
    repo = Path(tmp) / "product"
    repo.mkdir()
    env = dict(os.environ, GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.invalid",
               GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.invalid")

    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args], env=env)

    git("init", "-q")
    git("-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-qm", "baseline")
    base = git("rev-parse", "HEAD").decode().strip()

    def write(path, text, stage=True):
        p = repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        if stage:
            git("add", "--", path)

    cases = 0

    def run(code, contains, *args):
        global cases
        result = subprocess.run(["python3", str(CHECK), "--repo", str(repo), "--base", base, *args],
                                capture_output=True, text=True)
        output = result.stdout + result.stderr
        assert result.returncode == code, output
        assert contains in output, output
        assert "Traceback" not in output, output
        cases += 1
        return output

    # Real application evidence is allowed regardless of extension/directory.
    for path, text in {
        "fixtures/orders.json": '{"orders": [{"id": 1, "status": "pending"}]}',
        "config/model.json": '{"model": "order", "timeout": 30}',
        "schemas/reviewer.json": '{"type": "object", "properties": {"reviewer_id": {"type": "string"}}}',
        "migrations/001.sql": 'ALTER TABLE orders ADD COLUMN reviewer_id TEXT;',
        "docs/review-guide.md": 'Review the retry UI. Ran 12 tests, all passed. Authentication remains untested.',
    }.items():
        write(path, text)
    run(0, "0 unresolved")
    transcript = 'system: review this\nuser: check code\nassistant: findings\n'
    write("docs/evidence/reviewer-transcript.md", transcript)
    run(1, "FLAG staged")
    # Index bytes, not a cleaned unstaged worktree, control the result.
    write("docs/evidence/reviewer-transcript.md", "clean summary", stage=False)
    run(1, "repeated conversation role framing")
    git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "synthetic incident")
    run(1, "FLAG diff")
    # A new name must not hide the content and deleted old paths need no blob.
    git("mv", "docs/evidence/reviewer-transcript.md", "docs/evidence/notes.txt")
    write("docs/evidence/notes.txt", transcript)
    run(1, "repeated conversation role framing")
    # Remove only this test's synthetic record from its disposable repository.
    git("rm", "-f", "docs/evidence/notes.txt")
    git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "exclude process record")
    run(0, "0 unresolved")
    write("docs/result.json", '{"model": "example", "reasoning_effort": "high"}')
    run(1, "model/reviewer provenance metadata")
    git("rm", "-f", "docs/result.json")
    write("debug.txt", '{"type":"agent_settled"}')
    run(1, "agent runtime/transcript markers")
    git("rm", "-f", "debug.txt")
    synthetic = '[{"role":"system","content":"test"},{"role":"user","content":"test"},{"role":"assistant","content":"test"}]'
    path = "fixtures/conversations.json"
    write(path, synthetic)
    run(1, "serialized conversation messages")
    sha = hashlib.sha256(synthetic.encode()).hexdigest()
    allowance = ["--allow", path, sha, "Synthetic fixture exercises application conversation import"]
    run(0, "RESOLVED staged", *allowance)
    write(path, synthetic + "\n")
    run(2, "unused/stale --allow", *allowance)
    run(2, "substantive application-purpose", "--allow", path, sha, "ok")
    git("rm", "-f", path)
    # Body supplied outside the product tree, flags but never prints raw data.
    body = Path(tmp) / "body.md"
    body.write_text(transcript)
    output = run(1, "FLAG body", "--pr-body", str(body))
    assert "assistant: findings" not in output
    body.write_text('Ran 12 tests. All passed. Synthetic UI evidence attached.')
    run(0, "0 unresolved", "--pr-body", str(body))
    run(2, "Artifact check incomplete", "--pr-body", str(body) + ".missing")
    write("large.txt", "a" * (8 * 1024 * 1024 + 1))
    run(1, "content requires manual inspection")
    git("rm", "-f", "large.txt")
    run(2, "Git check failed", "--base", "missing-base")
    # Weird filenames cannot break line-based enumeration or inject options.
    write("docs/odd\nfile.txt", transcript)
    run(1, "repeated conversation role framing")

print(f"PASS: {cases} real-Git artifact scenarios (staged/committed/renamed/body, app evidence, exact-byte exceptions, failures)")

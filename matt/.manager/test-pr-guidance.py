#!/usr/bin/env python3
"""Check publishing and template contracts in rendered guidance, not model behavior."""
import argparse
from pathlib import Path
import re


def validate(skill):
    text = skill.read_text()
    workflow = text.split("## Workflow\n", 1)[1].split("\n## ", 1)[0]
    step = next(line for line in workflow.splitlines() if line.startswith("5. "))
    lookup = re.search(r"`(gh pr list [^`]+)`", step)
    assert lookup, "missing explicit PR lookup command"
    assert "--json " in lookup[1], "branch-only lookup cannot distinguish another fork owner or base"
    fields = lookup[1].split("--json ", 1)[1].split()[0].split(",")
    assert {"number", "headRefName", "headRepositoryOwner", "baseRefName"} <= set(fields), (
        "branch-only lookup cannot distinguish another fork owner or base"
    )
    for flag in ("--head <branch>", "--repo <owner/repo>", "--state open", "--limit 100"):
        assert flag in lookup[1], f"PR lookup must include {flag}"
    assert "before selecting a unique PR or concluding none exists" in step
    assert "returned count reaches the requested limit" in step
    assert "increase `--limit` and rerun" in step
    assert "strictly below the requested limit" in step
    assert "completeness cannot be established" in step and "do not edit or create a PR" in step
    assert "larger fixed limit alone is not proof" in step
    # A branch-name prefix is not a GitHub repository identity.
    for field in ("headRepositoryOwner.login", "headRefName", "baseRefName"):
        assert f"`{field}`" in step, f"selection must inspect {field}"
    assert "match" in step.lower() and "explicit base" in step
    assert "Do not infer the source owner from a branch-name prefix" in step
    assert "`gh pr edit <number> --repo <owner/repo>`" in step, (
        "edits must identify the selected PR number and target repository"
    )
    assert "metadata is missing" in step and "several exact matches" in step
    assert "instead of guessing" in step
    historical = text.split("## Retained template reference\n", 1)[1].split("````", 1)[0]
    assert "Historical reference only" in historical, "retained template must be historical only"
    assert "authoritative Base PR template above" in historical
    assert "Use this template for writing the PR body" not in historical, (
        "historical template must not instruct authors to use it"
    )


    # The approved template fixes the visible section order and disclosure label.
    template = text.split('## Base PR template\n', 1)[1].split('## Retained template reference\n', 1)[0]
    assert re.findall(r'^## (.+)$', template, re.MULTILINE) == [
        'Summary', 'Artifacts', 'Merge Danger', 'Description of Changes', 'Verification',
    ]
    artifacts = template.split('## Artifacts\n', 1)[1].split('## Merge Danger\n', 1)[0]
    media, walkthrough = artifacts.split('<summary>Try it yourself</summary>', 1)
    assert 'screenshots' in media and 'video for interactive flows' in media
    assert 'If a reviewer-accessible preview exists' in walkthrough
    assert '**Setup:**' in walkthrough and '**Cleanup:**' in walkthrough
    assert 'Omit this disclosure if neither a preview nor a useful walkthrough is available' in walkthrough
    danger = template.split('## Merge Danger\n', 1)[1].split('## Description of Changes\n', 1)[0]
    assert '**Door:**' in danger and '**Blast Radius:**' in danger
    verification = template.split('## Verification\n', 1)[1]
    assert re.findall(r'^### (.+)$', verification, re.MULTILINE) == ['Tests', 'Limitations', 'Checklist']
    assert '<summary>Automated test evidence</summary>' in verification
    assert 'ask once' in workflow and 'Proceed without waiting unless' in workflow


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", type=Path, default=Path(__file__).resolve().parent.parent / "pr/SKILL.md")
    args = parser.parse_args()
    try:
        validate(args.skill)
    except (AssertionError, IndexError, StopIteration) as error:
        raise SystemExit(f"PR guidance regression: {error}")
    print("PASS: complete owner/head/base lookup, explicit-number edit, incomplete/ambiguous lookup stop, historical-template precedence, active layout and wording nudge (source contracts only)")

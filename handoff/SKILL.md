---
name: handoff
description: Capture in-flight session state so the next session can resume without re-derivation. Use when stopping work mid-task, ending a session for the day, running low on context, immediately after context compaction, or before /clear. Triggers on "handoff", "save session context", "wrap up for today", "continue tomorrow", and post-compact or post-clear hook prompts.
---

# Handoff

Write a handoff document summarising the current session so a fresh agent
can continue the work. Record only information a fresh session cannot
recover elsewhere.

## Where it goes

Save each handoff under:

`<workspace-root>/.tasks/handoffs/H{sequence}-<descriptive-slug>-handoff.md`

In a Git repository, use the repository root as `<workspace-root>`.
Outside a Git repository, use the current working directory.

Create one new file for each handoff. Use the next unused `H{sequence}`
number in `.tasks/handoffs/`. Add a short lowercase kebab-case description,
as in `H1-refactor-agents-handoff.md`. Do not overwrite an earlier handoff.
Keep prior numbered handoffs as session history.

## Before writing

Run `git status -s` and `git log --oneline -5` before writing. Use their
output to inspect uncommitted changes and recent commits.

## Contents

- Record what is in flight and how far it has progressed.
- Record relevant branch and uncommitted state.
- Record reasoning needed to continue when it is not captured elsewhere.
- Record failed approaches needed to avoid repeating them.
- Give the single next action.
- Suggest skills the fresh agent should invoke, if any.
- Reference existing specs, plans, ADRs, issues, commits, and diffs by path
  or URL. Do not copy their contents.

Choose headings based on the work rather than following a fixed schema.

After saving the handoff, send this prompt to the user. Do not include it
in the handoff document.

```text
Resume from handoff: read <handoff path> and its referenced artifacts.
Verify the branch and git state, then continue with the next action.
```

## Rules

- Aim for fewer than approximately 50 lines.
- If a section keeps growing, move that content into `task.md`, `spec.md`,
  or `plan.md`.
- Before saving, check whether a fresh agent could continue from the
  numbered handoff plus the referenced artifacts alone.
- If a needed fact lives only in the current session, write it down.
- Redact sensitive information such as API keys, passwords, tokens, private
  IPs, or personally identifiable information.

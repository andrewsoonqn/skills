---
name: handoff
description: Use when stopping work mid-task, ending a session for the day, running low on context, right after a context compaction, or before /clear - to capture in-flight session state so the next session resumes without re-derivation. Triggers - "handoff", "save session context", "wrap up for today", "continue tomorrow", post-compact or post-clear hook prompts.
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a handoff document summarising the current conversation so a
fresh agent can continue the work. Capture only the delta a fresh
session cannot recover: in-flight state, failed approaches, and the
single next action.

Do not duplicate content already captured in other artifacts (specs,
plans, ADRs, issues, commits, diffs) - reference them by path or URL
instead.

Redact any sensitive information, such as API keys, passwords,
tokens, private IPs, or personally identifiable information.

If the user passed arguments, treat them as a description of what the
next session will focus on and tailor the doc accordingly.

## Where it goes

1. Active task folder:
   `tasks/T{n}-<slug>/H{sequence}-<descriptive-slug>-handoff.md` - use this
   only when the current conversation, context, or transcript identifies
   an active task.
2. No active task folder, or no `tasks/` tree in the repo:
   `~/.claude/handoffs/<workspace-key>/H{sequence}-<descriptive-slug>-handoff.md`.

If those sources do not identify an active task, use fallback.
Never infer an active task from modification times.

For fallback mode, resolve the canonical full repo root, or the canonical
full cwd when outside a repo. Use the readable basename plus the first 12
hexadecimal characters of the SHA-256 hash of that canonical full path.
Format `<workspace-key>` as `<basename>-<hash>`; never use the basename alone.

Create one new file per session handoff. Use `H1`, `H2`, and so on in
creation order within the task or fallback workspace; choose the next
unused number so handoffs cannot overwrite one another. Follow it with
a short lowercase kebab-case description of the work, for example
`H1-refactor-agents-handoff.md`. Never overwrite an earlier handoff.

When resuming, read the explicit handoff path from the prompt or session
context. Without an explicit path, inspect only the active task folder,
or derive `<workspace-key>` from the current canonical path and inspect
only that fallback directory. Do not scan other workspace directories.

## Before writing

- If an active task folder exists, sync its `task.md` first: tick
  completed Todo boxes and add a dated Notes line. The handoff must not
  compensate for a stale hub.
- In fallback mode, do not create or modify task artifacts or
  point the handoff at unrelated task artifacts.
- Run `git status -s` and `git log --oneline -5` for ground truth on
  branch and uncommitted state.

## Template

````markdown
# Handoff: <one-line current work>

**Date:** YYYY-MM-DD | **Branch:** <branch> | **Status:** IN PROGRESS / BLOCKED / REVIEW

## Read first
<Include these lines only when an active task folder exists;
otherwise omit them in fallback mode:
- <task folder>/task.md - hub (intent, todo, gates)
- spec.md / plan.md / questions.md - list only the ones that exist
>

## In-flight state
- <plan step or todo item mid-execution, and how far it got>
- <last subagent/workflow results not yet folded into artifacts>
- <uncommitted work: files touched, branch state>

## Failed approaches
- <tried X, failed because Y> (only if not already in task.md Notes)

## Suggested skills
<skills the next session should invoke, if any - otherwise omit>

## Next action
<THE single next step, concrete enough to start cold>

## Open questions / blockers
<or "None">

## Paste prompt
```
Resume from handoff: read <handoff path>.
If it references a task folder, read that folder's task.md.
Verify branch and git state match the handoff, then continue with
the Next action.
```
````

## Rules

- Reference, don't duplicate - a path beats a copy.
- Redact secrets: no tokens, access codes, serial numbers, private IPs.
- Lean: aim under ~50 lines. A growing section means the content
  belongs in task.md/spec.md/plan.md - move it there instead.
- Quality gate before saving: could a fresh session continue from the
  numbered handoff plus the referenced artifacts alone? If a needed fact
  lives only in the conversation, write it down.
- Keep prior numbered handoffs as session history. Never treat an older
  handoff as current when a later numbered handoff exists.

## Invocation contexts

| Context | Source of truth |
| --- | --- |
| Manual /handoff | live conversation |
| Post-compact (hook prompt) | the in-context compact summary - mine it, don't re-derive |
| Post-/clear (hook prompt gives a transcript path) | tail of the prior transcript JSONL - in-flight state only; conclusions go via extract-learnings |

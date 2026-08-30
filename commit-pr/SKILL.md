---
name: commit-pr
description: Use when committing, pushing, or opening a pull request, and when reviewing or rewriting a commit message or suggesting a branch name. Owns the user's commit-message conventions plus the classic 50/72 style for external repos, runs subagent-driven, and is fork/remote/base-aware. Supersedes the generic stock /commit-push-pr command.
---

# Commit / Push / PR

The owned workflow for commits and PRs. Supersedes the stock
`/commit-push-pr` command, which is generic, runs inline, and hardcodes
`origin`. Invoke this whenever you commit, push, or open a PR.

## Subagent-driven

Dispatch a subagent to compose and run the commit/PR unless the change
is trivial. Route the model per subagent-routing: a mechanical commit
is sonnet/low; a diff that needs judgment to find its unifying goal is
opus/medium.

## Enforcement

This skill's guidance is the only enforcement - there is deliberately
NO commit-msg hook. A hook was considered and declined (2026-07-10) to
reduce complexity; do not re-propose one.

## Commit message conventions

- Title states the WHY - the single goal that ties the whole diff
  together - not the WHAT. Imperative mood, descriptive, never
  generic, under 50 characters.
- Read the whole diff first to derive that one unifying goal.
- Add a body ONLY when the commit touches more than 3 code files;
  otherwise the title alone is the message. Blank line between title
  and body and between paragraphs; hard-wrap every body line under 50
  characters.
- Conventional prefix is optional: only `fix`, `feat`, `refactor`, or
  `chore` when used - never other types; no prefix at all is fine, so
  do not force one.

## External-convention repos (classic 50/72)

The conventions above are for the user's own repos. In an external
repo that follows the classic style (coursework, other teams,
upstream projects), or when explicitly asked for standard git
conventions, switch to:

- Subject: imperative mood, capitalized, no trailing period; prefer
  50 characters or fewer, treat 72 as the hard ceiling. Optional
  `<scope>:` or `<category>:` prefix when it genuinely helps.
- Body: add one for non-trivial commits; blank line after the
  subject, hard-wrap at 72, explain what changed and why - not the
  mechanics already obvious from the diff. A structure that works:
  present situation -> why it should change -> the change in
  imperative style (`Let's ...` is a good opener) -> why this
  approach is appropriate.
- Branch names: meaningful keywords in kebab-case;
  `issueNumber-keywords-from-issue-title` when tied to an issue
  (e.g. `1234-ui-freeze-error`).
- If the repo documents its own conflicting convention, point out
  the conflict and ask which to follow - never silently mix styles.

## Reviewing messages and branch names

When asked whether a message or branch name follows conventions, to
rewrite one, or to suggest a branch name: pick the convention set by
repo ownership as above, point out each violation concretely, and
return a ready-to-use rewrite (fenced block when there is a body).
For branch names, lead with one strong default and add 2-3
alternatives only when helpful.

## Scope: whose changes, how many commits

Before staging, run `git status` and read the full diff - never assume
the working tree is one thing to commit.

- **Ownership filter**: when scope isn't mentioned, default to
  changes this session is responsible for (its own edits, plus any
  subagents/background tasks it dispatched this turn). Leave alone
  anything else dirty in the tree - another session, another agent,
  GitHub Desktop, the user's own manual edits.
- **Explicit scope wins.** "Commit all changes", naming files, "in
  one commit", "help commit my XYZ edits together too" (pull in named
  non-session changes and merge them into the group) - stage/group
  exactly that; the filters above are only fallbacks for when scope
  isn't stated.
- **Split by logical goal, not by turn**: within the owned changes,
  group by the WHY each file serves, not by when it was touched or
  which tool call produced it. A session that fixed a bug and then
  added an unrelated feature owns two commits, not one, even though
  both are "its own changes." Files touched across several tool calls
  or subagents that all serve one goal stay one commit.
- This is the default whenever the owned changeset doesn't reduce to
  one unifying WHY - splitting into separate commits no longer needs
  "commit this in multiple stages" spelled out. Name the groups before
  committing so the user can redirect before multiple commits land.
- **Bias toward splitting when unsure.** Squashing an over-split
  history is one command; splitting an over-combined one is a manual
  rebase. On a close call between one commit and two, pick two.
- Stage and commit one group at a time (`git add <files-for-group>`,
  commit, repeat) - never `git add -A`/`git add .` across groups.

## Pre-flight (before pushing / opening a PR)

Query state, never infer it - past mistakes came from assuming:

- `git rev-parse --abbrev-ref @{u}` for the real upstream, and
  `git remote -v` for all remotes. These repos often carry origin plus
  a personal fork, and the branch may track the fork, not origin.
- `gh pr list --head <branch> --repo <owner/repo>` FIRST - a PR may
  already exist. Update it (`gh pr edit`); never open a second.
- Choose the base deliberately and confirm it exists on the target
  remote (`git ls-remote`). Do not default to origin/main blindly.

## PR body

- Do NOT hard-wrap - one physical line per paragraph or bullet; GitHub
  soft-wraps and manual breaks fight it. This is the opposite of
  commit bodies.

## Steps

1. If on main/master, branch first (conventional prefix:
   feat/fix/chore/refactor/docs).
2. Determine scope and grouping per Scope above, then stage and
   commit each group with a message per the conventions above (may be
   more than one commit).
3. Push to the branch's real upstream.
4. Open or update the PR against the confirmed base and remote.

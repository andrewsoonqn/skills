---
name: commit-pr
description: Use when writing or reviewing commits, staging changes, or suggesting a branch name.
---

# Commit

Use this workflow to stage and commit changes. Completion means the intended changes are committed and unrelated changes remain untouched. Use the `pr` skill for writing, opening, or updating pull requests. Pushing is a separate action requiring an explicit user request.

## Commit message conventions

- Why, not What. State why the change was made in the title. Do not use the title to summarize the diff.
- Use imperative mood.
- Keep the title descriptive and under 50 characters.
- If the agent doing the commit did not participate in development or
  review, read the whole diff before writing the title.
- Add a body when the commit changes more than three code files.
- For smaller commits, use the title alone.
- Leave a blank line between the title and body.
- Leave a blank line between body paragraphs.
- Wrap every body line under 50 characters.
- A conventional prefix is optional. When using one, choose `fix`,
  `feat`, `refactor`, or `chore`.

## External-convention repos

- Use these conventions for the user's own repositories.
- For coursework, other teams, and upstream projects, follow the
  repository's documented conventions.
- When the user requests standard Git conventions and the repository
  does not define its own, use standard Git conventions.
- If the repository convention conflicts with the requested convention,
  ask the user which one to follow.

## Scope: whose changes, how many commits

- Run `git status` before staging.
- Check for changes outside the requested scope and changes that belong
  in separate commits.
- When the user does not specify scope, include only changes this session
  is responsible for. This includes its own edits and work it dispatched
  during the turn.
- Leave changes from other sessions, agents, GitHub Desktop, and the user
  unstaged.
- Follow any explicit scope from the user. Examples include "commit all
  changes," named files, "in one commit," and requests to include other
  named edits.
- Group changes by the reason they serve.
- Put a bug fix and an unrelated feature in separate commits.
- Keep files in one commit when they serve the same goal.
- When the changes require several commits, name the groups before
  committing. Give the user an opportunity to change the grouping.
- When one file contains changes for different groups, stage each group
  with `git add -p`.
- If one hunk contains changes for different groups, edit the patch before
  staging it.
- If the changes cannot be separated safely, keep them in one commit and
  explain why.
- Split into separate commits when the correct grouping is unclear.
- Stage and commit one group at a time.
- Do not use `git add -A` or `git add .` across groups.

## Steps

1. If on main/master, branch first (conventional prefix:
   feat/fix/chore/refactor/docs).
1. Determine scope and grouping per Scope above, then stage and
   commit each group with a message per the conventions above (may be
   more than one commit).
1. Inspect the committed diff and `git status`. Report the commit hashes and any remaining uncommitted changes. Stop after committing.

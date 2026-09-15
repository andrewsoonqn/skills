# Approved examples

Use these examples to guide sentence structure and editing decisions. Do
not copy their subject matter into unrelated documents.

## Meaningful contrast

Approved:

> Why, not What. State why the change was made in the title. Do not use
> the title to summarize the diff.

Keep this contrast because it defines the rule.

## Commit body

Before:

> Add a body ONLY when the commit touches more than 3 code files;
> otherwise the title alone is the message.

After:

> Add a body when the commit changes more than three code files. For
> smaller commits, use the title alone.

## Conventional prefix

Before:

> Conventional prefix is optional: only `fix`, `feat`, `refactor`, or
> `chore` when used - never other types; no prefix at all is fine, so do
> not force one.

After:

> A conventional prefix is optional. When using one, choose `fix`, `feat`,
> `refactor`, or `chore`.

## Conflicting conventions

Before:

> If the repo documents its own conflicting convention, point out the
> conflict and ask which to follow - never silently mix styles.

After:

> If the repository convention conflicts with the requested convention,
> ask the user which one to follow.

## Working-tree check

Before:

> Before staging, run `git status`. Never assume the working tree is one
> thing to commit.

After:

> Run `git status` before staging. Check for changes outside the requested
> scope and changes that belong in separate commits.

The second sentence is useful because it states what to check. A warning
such as "never assume" does not state the required check.

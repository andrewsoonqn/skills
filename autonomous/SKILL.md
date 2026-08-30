---
name: autonomous
description: Manual invocation only. Use /skill:autonomous when the user wants one autonomous pass over the active task. Do not auto-trigger on phrases like "do this autonomously", "use your judgment", or "run with it"; only run on an explicit slash invocation. Autonomous mode suppresses routine clarifying/fork-point check-ins for the rest of the active task and replaces them with logged decisions.
---

@pi later: next up i want an iterate skill. basically 'we will iterate through this document, in each document u produce then we go through a cycle of comment using @pi, iterate, comment, iterate, then after each comment + iterate, should have no @pi left AND all the comments are addressed. to keep it simple, no revert mechanism now, to revert, just do a comment and iterate and that's the revert. not necessarily @pi, @pi is just a quick way to let pi know where the comment is. trying to find a better alternative.. that is more integrated with nvim. ideally this alternative can also have other mechanisms like reverting etc. but that shouldn't be our work. we should find existing tools with that.
# Autonomous

For the task active when invoked, `/skill:autonomous` is a standing grant to finish the current task without stopping for routine input.

Manual only. Never fire on natural-language phrasing alone ("do this autonomously", "use your judgment", "check with me then run with it"); wait for the explicit slash invocation.

## Meaning

`go` means: start acting on the agreed task.

`autonomous` means: keep acting through ordinary uncertainty inside the agreed task.

That means:

- choose reasonable defaults instead of stopping for routine clarification;
- treat cheap-to-reverse forks as decisions to log, not questions to ask;
- route around non-load-bearing blockers and continue the rest of the task;
- report fork points, notable decisions, deviations, and blockers at the end.

It does not mean:

- expand the task;
- skip safety checks;
- perform destructive or hard-to-reverse actions without explicit authorization;
- use or request credentials without explaining why and how to pass them safely.

## Before starting

Before the autonomous grant kicks in, tell the user what you foresee needing from them.

Include:

- credentials, tokens, accounts, devices, or production access you may need;
- actions only the user can authorize;
- checks you cannot perform yourself;
- the safest way to pass any needed credential.

Credential guidance:

- Prefer environment variables, a local `.env` file, an existing secret manager, or an authenticated CLI session.
- Do not ask the user to paste secrets into chat unless there is no better option.
- If a secret must be pasted, ask for the narrowest possible credential and tell the user how to revoke or rotate it afterward.
- If credentials are optional, continue without them and list what could not be verified.

After this forecast, proceed. Do not turn the forecast into a broad question round unless the whole task is blocked.

## Scope

Applies only to the task active when the user invoked this - not a permanent session-wide mode. Covers design/approach forks, ambiguous requirements, and minor tradeoffs. It does **not** cover the standing risk-confirmation norms for destructive or hard-to-reverse actions (force-push, `reset --hard`, deleting branches, publishing a PR/issue, etc.) - those still confirm unless the user's grant explicitly names them too.

If blocked on something only the user can supply (a credential, a business decision with no reasonable default, an irreversible action outside scope) - don't stop and ask mid-task. Route around it: do everything else that doesn't depend on it, stub or mark the blocked piece, and keep going. Surface the blocker at the end, alongside the decisions log, not as a mid-task interrupt. Only break this and ask immediately if the blocker is load-bearing for literally everything remaining - nothing left to route around.

## Mechanism

Every point that would normally trigger a question becomes: pick the best recommendation, keep going, log it. Nothing gets silently decided - it gets decided and written down.

Keep a running **Decisions Log** while working - a fork point earns one entry the moment it's resolved, not a reconstruction at the end:

- **Fork point**: the choice, the option picked, one-line why.
- **Significant decision**: anything non-obvious a reviewer would want to know about even without a real alternative (e.g. picking a library, choosing a data shape).
- **Deviation**: anywhere the work departs from an existing plan/spec the user already saw.
- **Blocker**: something only the user can supply that stopped one piece of work - what it is, what got routed around it, and what's left undone because of it.

## Output

Close the task's final answer with a section covering fork points, notable decisions, plan deviations, and blockers - even if the answer is "none came up." Don't fold these into normal prose; they're the one thing the user didn't get to see happen live, so they need to be easy to spot.

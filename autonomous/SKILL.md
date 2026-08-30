---
name: autonomous
description: Manual invocation only (/autonomous for full mode, /autonomy semi for a question round first). Do not auto-trigger on phrases like "do this autonomously", "use your judgment", or "ask me a few questions then run with it" - only run on an explicit slash invocation. Full mode suppresses clarifying/fork-point check-ins for the rest of the active task and replaces them with a logged decision; semi mode first asks up to 6 of the highest-risk, human-judgment questions about the active task - the choke points that are not inferable - then goes fully autonomous.
---

@pi replace all autonomy modes with autonomous. ALL
@pi remove completely semi autonomous. only one autonomous mode. which is generally a more "intense" version of "saying go"
@pi before autonomous, need let human know what we forsee from him. any credentials, and how to pass those credentials
@pi address all these comments for our iteration, then erase them after addressing.
@pi next up i want an iterate skill. basically 'we will iterate through this document, in each document u produce then we go through a cycle of comment using @pi, iterate, comment, iterate, then after each comment + iterate, should have no @pi left AND all the comments are addressed. to keep it simple, no revert mechanism now, to revert, just do a comment and iterate and that's the revert. not necessarily @pi, @pi is just a quick way to let pi know where the comment is. trying to find a better alternative.. that is more integrated with nvim. ideally this alternative can also have other mechanisms like reverting etc. but that shouldn't be our work. we should find existing tools with that.
@pi i also collapsed, so no subfolders for skills anymore...
@pi remind me, agent.md add: [phase to be determined], always need a way to find whether something has already been done. e.g. before doing our own survey has a research paper already done it. before implementing our own tool has someone already implemented it in whole or parts of it. this i think should go after phase where we have enough clarity but before we do the hard work of planning details or actual implementation.

# Autonomy Modes

One dial, two settings, for the task active when invoked:

- **Full** (`/autonomy-modes`): a standing grant to finish the
  current task without stopping for input. Start at
  [Full autonomy](#full-autonomy).
- **Semi** (`/autonomy-modes semi`): one
  negotiation round first - surface the few questions whose answers
  most change the shape of the work - then the full contract. Start
  at [Semi: question round first](#semi-question-round-first).

Manual only. Never fire on natural-language phrasing alone ("do this
autonomously", "use your judgment", "ask me some questions first,"
"check with me then run with it"); wait for the explicit slash
invocation.

## Full autonomy

Every point that would normally trigger a question or an
`AskUserQuestion` call becomes: pick the best recommendation, keep
going, log it. Nothing gets silently decided - it gets decided and
written down.

### Scope

Applies only to the task active when the user invoked this - not a
permanent session-wide mode. Covers design/approach forks, ambiguous
requirements, and minor tradeoffs. It does **not** cover the standing
risk-confirmation norms for destructive or hard-to-reverse actions
(force-push, `reset --hard`, deleting branches, publishing a
PR/issue, etc.) - those still confirm per the
executing-actions-with-care rules unless the user's grant explicitly
names them too.

If blocked on something only the user can supply (a credential, a
business decision with no reasonable default, an irreversible action
outside scope) - don't stop and ask mid-task. Route around it: do
everything else that doesn't depend on it, stub or mark the blocked
piece, and keep going. Surface the blocker at the end, alongside the
decisions log, not as a mid-task interrupt. Only break this and ask
immediately if the blocker is load-bearing for literally everything
remaining - nothing left to route around.

### Mechanism

Keep a running **Decisions Log** while working - a fork point earns
one entry the moment it's resolved, not a reconstruction at the end:

- **Fork point**: the choice, the option picked, one-line why.
- **Significant decision**: anything non-obvious a reviewer would
  want to know about even without a real alternative (e.g. picking a
  library, choosing a data shape).
- **Deviation**: anywhere the work departs from an existing plan/spec
  the user already saw.
- **Blocker**: something only the user can supply that stopped one
  piece of work - what it is, what got routed around it, and what's
  left undone because of it.

### Output

Close the task's final answer with a section covering fork points,
notable decisions, plan deviations, and blockers - even if the answer
is "none came up." Don't fold these into normal prose; they're the
one thing the user didn't get to see happen live, so they need to be
easy to spot.

## Semi: question round first

Full autonomy with one negotiation round first. Before the standing
"don't stop for input" grant kicks in, surface the few questions
whose answers most change the shape of the work - the forks that
would otherwise get decided unilaterally mid-task. Once answered, the
rest of the task runs under the full contract above: no more
check-ins, every remaining fork gets decided, logged, and reported at
the end.

The point of the up-front round is to spend the user's limited
attention where it buys the most: on the decisions with the largest
blast radius, before any work is shaped around a wrong guess.

### Step 1: Find the highest-leverage questions

Do a quick scoping pass first - skim the relevant files, code, or
prior discussion - so the questions are informed by the actual task,
not generic intake questions. A question you could answer yourself
with two minutes of reading does not deserve a slot.

Then pick the **top 6 highest-leverage questions**. A question earns
a slot only if both hold:

- the answer changes what gets built or how - not just phrasing or
  polish, and
- you cannot confidently infer the answer from the request, the code,
  or the user's known conventions.

Only two classes of question are worth a slot, and they earn it for
different reasons:

- **Judgment forks** - calls that need human values, taste, or
  priorities the repo cannot contain: what matters more when goals
  conflict, which user experience is right, how good is good enough.
  Ask because your best guess may genuinely be wrong. These should
  dominate the round - they are the questions where the user's answer
  is most likely to differ from your recommendation.
- **Authorization gates** - actions outside the autonomous grant:
  commit/push, publishing, schema migrations, anything destructive or
  hard to reverse that the task will plausibly need. Ask even when
  the answer feels obvious - the point is not uncertainty, it is
  pre-authorization so the run does not block later, and converting
  your guess into the user's explicit decision on a choke point.

Everything else is a decide-and-log under the autonomous contract,
not a question. Two disqualifiers - note how differently they are
gated, because they are not equally trustworthy:

- **Answered by standing conventions.** If the user's CLAUDE.md, a
  skill (e.g. delegation routing already prescribes a review round
  with one fix pass), or repo conventions settle it, asking
  re-litigates a settled call. This disqualifier is safe *because it
  is verifiable* - you can point at the line that answers it. If you
  cannot cite the specific rule, you have not met this bar; keep the
  question.
- **Recommendation theater - low stakes only.** A candidate you would
  bet 90%+ the user simply accepts is a logged decision wearing a
  question costume *if and only if* guessing wrong is also cheap to
  reverse. Confidence alone never kills a question: your confidence
  is the least reliable input you have, and overconfidence is the
  main way a needed question goes unasked. Stakes are the dominant
  term.

**The asymmetry that governs all of this**: asking an unnecessary
question costs the user seconds. Failing to ask a necessary one costs
an entire autonomous run built on a wrong assumption, discovered at
the end. These are not comparable. Resolve every genuine tie toward
asking, and treat the 6-question budget as room you are allowed to
use, not a score to minimize. Ending with 2 questions is only correct
if the sweep below actually came up empty - never because trimming
felt tidy.

Rank the survivors by (cost of guessing wrong) x (genuine
uncertainty), where cost dominates. Categories that usually dominate:

- scope boundaries - what is in and out of this task
- user-visible interface decisions - CLI flags, UX flows, API shapes,
  output formats
- the authorization gates above (end state, publishing, migrations)
- acceptance criteria - what "done" looks like, how it will be judged
- hard constraints - compatibility, dependencies, performance budgets
- priority calls when stated goals conflict

Fewer than 6 is correct when the task genuinely has fewer real forks.
Padding with filler questions burns the user's attention and trains
them to skim the round - which defeats the reason it exists.

#### Sweep before you finalize

A missed question is usually one you never generated, not one you
ranked badly - so generation gets its own explicit pass. Before
sending the round, walk this list and, for each line, land on one of:
*asking it*, *citing the rule that settles it*, or *genuinely absent
from this task*. "Didn't think about it" is not one of the three.

- **Done bar** - what counts as verified, and what you cannot verify
  yourself (no mic, no device, no prod access, no credentials)
- **End state** - commit, push, PR, leave in working tree
- **Irreversible actions** - migrations, deletions, force-push,
  publishing, anything touching real users or real data
- **Scope edges** - the adjacent thing you are about to touch, or
  deliberately not touch, that the user may assume goes the other way
- **Conflicting goals** - where the request's own aims pull apart
  (speed vs coverage, minimal diff vs doing it properly)
- **Reversibility of the core approach** - if the shape you are about
  to commit to is wrong, is that a small edit or a rewrite
- **Stale premises** - anything the request or handoff assumes that
  your scoping pass just found to be untrue

#### Surface what you filtered out

The escape valve that makes the filter safe: every candidate you
generated but chose not to ask becomes a one-line entry in an
**Assumptions I'm running with** block, sent alongside the questions.
State the assumption and what you will do because of it.

This is what keeps a filtering mistake from becoming a silent one -
the user scans five lines in a few seconds and can veto any of them,
so a wrong call costs a correction instead of a wasted run. It also
means borderline candidates have somewhere cheap to go, which is what
lets the round stay short without getting risky. If you filtered
nothing, say so rather than omitting the block.

### Step 2: Ask them

Ask via `AskUserQuestion`. It takes at most 4 questions per call, so
6 questions means two batches - 4 then 2, or 3 then 3 if that groups
more coherently. Batch related questions together so the user has
context.

For each question, give concrete options with your recommendation
listed first and marked "(Recommended)" - the user should be able to
clear the whole round in seconds by accepting defaults. If the user
answers "you decide" or skips a question, treat it as a fork under
the autonomous contract: take your recommendation and log it in the
Decisions Log.

If an answer invalidates the premise of your planned approach, one
follow-up round (at most 2 questions) is allowed before going
autonomous. After that, no more - remaining uncertainty becomes
logged decisions, not questions.

### Step 3: Go autonomous

Follow the [Full autonomy](#full-autonomy) contract for the rest of
the task. The user's explicit invocation is the manual grant that
contract requires - do not wait for a separate `/autonomous`. Restate
a one-line summary of what was asked and answered at the handoff, so
the binding contract is explicit instead of left implicit in earlier
context.

Two additions on top of that contract:

- **Answers are binding.** Everything from Step 2 is a constraint,
  not a suggestion - a logged autonomous decision may never override
  or reinterpret an answer the user gave. If new information makes an
  answer look wrong, that is a Deviation entry in the Decisions Log
  with the evidence, and the work follows the answer anyway unless it
  would be destructive to do so.
- **Open the Decisions Log with the answers.** Start the log with a
  short record of what was asked and answered, so the final report
  reads as one coherent account: what the user chose, then what was
  chosen for them. Carry the assumptions block into it too - anything
  the user did not veto is now a standing assumption the final report
  should account for.
- **One late-fork interrupt is allowed.** The round can only cover
  forks visible before the work started. If execution uncovers a
  choke point that would have earned a slot *and* it is
  hard-to-reverse - a migration nobody knew was needed, the spec
  contradicting the code, an approach that has to be abandoned rather
  than adjusted - ask it, once, rather than burying it in the log.
  Suppressing that is exactly the failure the up-front round exists
  to prevent, just relocated. Everything short of that bar stays a
  logged decision: routine forks, cheap-to-reverse calls, and
  anything you can route around still follow the autonomous contract
  and wait for the final report.

Output rules are identical to full autonomy: close the final answer
with the fork points, notable decisions, deviations, and blockers -
even if the answer is "none came up."

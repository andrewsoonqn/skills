---
name: procedural-prose
description: Diagnose and revise procedural prose that feels compressed, rhetorical, AI-written, or uncanny. Use for skills, prompts, policies, runbooks, contributor guides, and operating instructions when sentences combine rules, explanations, contrasts, exceptions, or warnings. Also use when reviewing semicolon-heavy, dash-heavy, slogan-like, or overly emphatic instructions.
---

# Procedural Prose

Use this skill for instructions and reference documents. Do not apply it
automatically to creative prose, casual messages, quotations, or source
code.

Always complete Phase 1 before Phase 2.

```text
Diagnose and propose -> approval -> edit and verify
```

Read [the approved examples](references/examples.md) before proposing a
rewrite. Read [the research notes](references/research.md) only when the
user requests research or the basis for a rule is unclear.

## Preserve meaning

Identify the following before proposing changes:

- required actions;
- conditions and exceptions;
- commands, paths, filenames, and values;
- sequence and grouping;
- deliberate contrasts;
- quotations, citations, links, and defined terms.

Preserve each item unless the user explicitly asks to change it. Do not
remove a contrast when it defines a rule. For example, "Why, not What"
defines a meaningful distinction in commit guidance.

## Phase 1: Diagnose and propose

1. Read the entire target.
2. Use the user's annotations as evidence of the unwanted effect.
3. Identify the broader prose pattern behind the examples.
4. Explain why the marked examples create that effect.
5. Find the same pattern elsewhere in the target.
6. Propose a rewrite rule that addresses the pattern.
7. Provide representative before-and-after examples.
8. State what will change.
9. State what must remain unchanged.
10. Request approval before editing.

Do not edit the target during this phase. Research is optional. Use it when
the user requests evidence or when prior art would materially affect the
proposal.

## Phase 2: Edit and verify

Begin only after the user approves the proposal.

1. Apply the approved rule throughout the agreed scope.
2. Preserve the identified meaning and literal content.
3. Leave unaffected prose alone.
4. Run the structural scan below.
5. Compare the revision with the source.
6. Correct any lost condition, exception, command, value, sequence, or
   deliberate contrast.
7. Report what changed.
8. State whether anything was committed or pushed.

## Rewrite rules

- Give each bullet one rule.
- Give each sentence one instruction.
- A sentence may contain one condition governing one action.
- Put the condition before the action.
- Put separate exceptions in separate sentences.
- Use periods between independent statements.
- State the required action directly.
- Include a reason when it changes how the reader should act.
- Remove emphasis or commentary that does not affect the procedure.
- Preserve exact technical content.

## Structural scan

1. Find semicolons and spaced hyphens in prose.
2. Split each affected sentence into atomic instructions when the
   punctuation joins independent instructions.
3. Find rhetorical contrasts such as `not X`, `never Y`, and `X wins`.
4. Preserve contrasts that define meaning.
5. Replace contrasts that only add emphasis.
6. Remove uppercase emphasis unless capitalization is part of a literal
   value or an approved phrase.
7. Remove explanations that do not affect the action.
8. Compare the result with two or three approved examples.

The scan identifies candidates for review. It does not ban punctuation or
contrast. Judge each case by its function in the procedure.

---
name: visual-plan
description: >-
  Use whenever a plan for non-trivial work is produced, presented, or proposed, including
  features, designs, refactors, migrations, multi-step tasks, and plan mode. Use together
  with the planning skill that produced the plan. Applies to "plan this", "what's the
  approach", "how should we approach X", "show me the plan", "make a visual plan",
  "render this plan", and plan review or feedback. Skip a trivial one-step change or an
  explicit request for plain prose.
---

# Visual plan

Read [visual-docs](../visual-docs/SKILL.md) for the shared authoring, VPlan compilation, and
original Plannotator HTML review workflow. Resolve this link relative to the skill directory, not the current working directory.
Use this skill only for the planning-specific guidance below. It does not replace the planning
method that produced the plan or grant permission to implement it.

## Compose the plan

- **Lead with the structure.** Open with at most a one-paragraph context, then a Mermaid
  architecture diagram and the `<Phase>` timeline when the plan has that structure.
  The reader should understand the shape of the plan before reading detailed prose.
- **Prefer a diagram or a `<FileTree>` to describing structure in words.** A flowchart of the
  data path beats a paragraph tracing it. A file-change map beats sentences listing the files.
- **Move the meaning into components.** Risks and decisions go in `<Callout>`s, open questions
  in `<Questions>`, tradeoffs in `<Compare>` / `<Matrix>`, and acceptance criteria in `<Checklist>`.
- **Keep prose tight inside phases.** A `<Phase>` is a step. Give a line or two of intent,
  then the visual that explains the step.
- **Right-size what you show.** A large effort may need a diagram and several phases.
  A two-or-three-file change may need only a short `<FileTree>` and a `<Checklist>`.
  An empty two-node flowchart shows nothing. Use a tight sentence when there is no structure
  to show. Add `<Stat>` only for genuine standout numbers, not invented or filler metrics.

The component vocabulary fits any structured plan, including a product launch, research agenda,
or incident response. Use the components that fit the plan and skip the ones that do not.

Review submission is not an execution instruction. Continue within the user's requested scope.
Do not wait for a browser verdict unless the user has made approval a condition of the work.

VPlan compiles the document. Plannotator reviews the generated HTML. Apply requested changes
to the original MDX and start a new review. Approval of a document does not authorize implementation.

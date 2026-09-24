---
name: visual-docs
description: >-
  Shared visual document vocabulary and Plannotator review workflow for plans, explanations,
  and other structured documents. Use whenever a topic, concept, system, mechanism, workflow,
  comparison, or relationship would be clearer visually instead of in prose. Deliver a scannable visual
  MDX document compiled by VPlan and reviewed in original Plannotator, with diagrams, timelines, tables, charts,
  and callouts. Applies to "explain visually", "show how this works", "make a visual
  explainer", "diagram this", or requests to see an explanation. Skip when prose is already
  the clearest form or the user explicitly asks for plain prose.
---

# Visual documents

## Purpose

Show the subject through diagrams and tables, with prose connecting the visuals.
The component vocabulary fits any structured explanation. Use the components that fit
and skip the ones that do not.

Use [visual-plan](../visual-plan/SKILL.md) for planning-specific guidance.
Do not turn an explanation into an implementation plan
or require sign-off just because the document supports review.

## Workflow

1. Read [Visual authoring](references/visual-authoring.md) before writing.
   Resolve `references/visual-authoring.md` relative to this skill directory,
   not the current working directory. It is the shared source for placement, syntax,
   components, review, source edits, and exports.
2. Reuse the existing task folder under `.pi/docs/NN-slug/`.
   Use `.mdx` for this compilation workflow. Ordinary Markdown does not need this workflow.
3. Compose the explanation using the intent guidance below and the shared reference's grammar.
4. Validate with `vplan check`. Fix diagnostics and check the compiled visuals.
5. Call `plannotator_mdx_review` with the original MDX `path`.
   VPlan compiles the document. Original Plannotator reviews the generated HTML.
6. Return the source link and review URL. Set `open: true` only when explicitly requested.
   If the tool is unavailable, use the shared reference's standalone fallback.
7. Apply requested changes to the MDX source. Start a new review after recompilation.

For a shareable file, use the compiled HTML or the shared reference's export commands.
Starting a review does not require approval or authorize implementation.

## Show, don't tell

- **Lead with the structure.** Open with at most a one-paragraph context, then the diagram,
  table, or other visual that exposes the subject's shape. The reader should understand
  that shape before reading a full explanation.
- **Prefer a diagram or a `<FileTree>` to describing structure in words.** A flowchart of a
  data path beats a paragraph tracing it. Use a file-change map only when explaining changes.
- **Move the meaning into components.** Risks and decisions go in `<Callout>`s, unresolved
  points in `<Questions>`, and tradeoffs in `<Compare>` or `<Matrix>`.
- **Use phases for sequence or progression.** A `<Phase>` is a step. Give a line or two of
  context, then the visual that explains it. Do not impose a timeline on a static relationship.
- **Right-size what you show.** An empty two-node flowchart shows nothing.
  Show when there is structure to show. Otherwise a tight sentence is fine.
  Add `<Stat>` only for genuine standout facts, not invented or filler metrics.

## Boundaries

VPlan is the compiler, not a temporary fallback. Plannotator supplies the review interface.
There is no separate workspace or MDX editing UI. The agent edits the original MDX.
Do not change installations or global Pi configuration as part of this skill.

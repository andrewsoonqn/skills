---
name: frontend-design
description: Use when designing, reviewing, or implementing user-facing frontend interfaces; especially when comparing UI patterns, producing interactive visual variants, refining approved designs, or checking visual quality.
---

# Frontend design

Use this skill when a task changes a user-facing interface. Follow the user's brief and the product's existing design system; the guidance below informs decisions but does not override explicit requirements.

Before designing, implementing, or auditing an interface, read [Frontend rules](../docs/agents/frontend-rules.md). Apply them within the requested scope. For AHMA work, also read [AHMA approved patterns](references/ahma-approved-patterns.md) and apply only patterns relevant to the requested surface.

## Workflow

1. **Restate the intent and inspect the real interface.** Read the relevant code and design context before proposing a change. Identify the actual screen, state, viewport, data, and constraints. Separate verified behavior from a mock or an assumption.
2. **Clarify only unresolved choices that materially affect the result.** Ask a few focused questions when needed; do not make the user decide details already determined by the brief, code, or design system. Do not block on questions when reasonable choices can be shown as variants.
3. **Use references responsibly.** When references would help and are available, find real product screenshots from a suitable source such as Mobbin, view the screenshots, and link to the original screens. Keep only relevant references. Never invent a source, screenshot, app attribution, or URL. If no strong reference is available, say so rather than padding the reference set.
4. **For a design round, make one self-contained, offline HTML page.** Show a faithful Current state and three genuinely different, clickable variants per requested change, using the product's real visual style and representative content. Label sections and states clearly. Put the newest round first and keep prior rounds below it, collapsed. Do not change the application while the user is choosing.
5. **Verify the prototype.** Exercise every control, replay, and state toggle; check the target viewport, text clipping, and scroll in both directions. Include narrow layouts only when mobile is requested or existing responsive behavior is affected. Check the browser console and external requests when practical. Use representative sample data, clearly label it as sample/preview data, and never present a prototype as live product behavior.
6. **Present useful visual evidence.** Render the actual changed screen at the requested viewport and capture meaningful full-screen screenshots (or a video for a flow). Annotate or box the relevant element when that helps. An isolated component capture is appropriate only when requested. A page load or a successful build alone is not visual verification.
7. **Get approval before implementation.** Present the alternatives and their trade-offs. Implement only the user's approved design; do not silently treat a proposal, prototype, or lack of response as approval. Call it the **approved design**, not a “locked mock.” If the user asks to skip exploration or implement directly, follow that instruction.
8. **Implement and re-check.** Apply the approved design with focused changes that follow local patterns. Run relevant checks and visually inspect the implemented state at the target viewport. Report what was verified and any visual checks you could not perform.

## Visual audit

Inspect the rendered interface against the shared frontend rules. Report concrete violations with screenshots of the affected states, not a generic checklist of advice. Keep verification within the requested scope and the applicable verification-round limit.

## Validation checklist

- [ ] The implementation or prototype addresses the actual requested screen and state.
- [ ] Alternatives are meaningfully different; any referenced screens are real, viewed, and linked.
- [ ] Labels, icons, facts, recommendations, and outcome states are not duplicated or misleading.
- [ ] Text contrast, alignment, pill wrapping, spacing, and nested corners are checked at the target viewport.
- [ ] Every interaction works; motion does not jump; scrolling works in both directions.
- [ ] Requested viewports and affected existing responsive behavior are checked. Disclosures keep secondary information secondary.
- [ ] Sample data is identified; screenshots show the meaningful full-screen state.
- [ ] The user approved the design before implementation, unless they explicitly requested direct implementation.
- [ ] Relevant code checks and a visual check of the implemented UI are reported separately and accurately.

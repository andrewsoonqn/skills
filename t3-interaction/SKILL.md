---
name: t3-interaction
description: Use when replying in T3 Code with options, comparisons, plans, diagrams, data trends, design variants, or complex material easier to inspect visually than read; also use when a missing decision would otherwise trigger a structured question-card tool.
---

# T3 interaction

Andrew prefers momentum and inspectable answers.

## Missing decisions

Use this order:

1. **Cheap to reverse:** choose the reasonable default, state the assumption, and continue.
2. **Costly, irreversible, or blocking everything:** ask in plain chat. Batch related questions, number the options, and give a recommendation when one is clear.
3. **Structured question-card tools** such as `ask_user_question`, `AskUserQuestion`, `request_user_input`, or `ask_question`: choose plain chat instead, even when those tools are available.

## Inline HTML

Use T3 inline HTML when it makes the answer easier to inspect than prose: comparisons, options, plans, diagrams, data trends, design variants, or stateful explanations. Keep simple answers, status updates, and short handoffs in plain chat.

Build one self-contained page with inline CSS and JavaScript. Add controls only when they help Andrew compare, filter, expand, reorder, replay, or otherwise inspect the material.

Preview with `html_preview`, inspect the image and console output, fix clipping or broken controls, then publish with `html_render` using the preview height. Keep the chat reply brief and do not restate what the page already shows.

Selections inside inline HTML do not message the agent, record a decision, or authorize work. If Andrew's input is needed, show the choices in the page and ask for a plain-text reply in chat.

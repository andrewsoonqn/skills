---
name: lightning-fast
description: Use when the user asks for a "lightning fast" build of a settled specification. Build directly and verify the most important behaviors with fast checks.
---

# Lightning fast

Assume the specification is settled. Build the requested version directly, with iteration expected after delivery. Resolve only implementation choices that block progress. Finish decision-critical research before dependent implementation.

For frontend work, read [frontend-rules.md](../docs/agents/frontend-rules.md). Apply the shared rules without starting frontend-design's exploration or approval workflow. Skip variants and full visual audits by default. Preserve existing responsive behavior and cover mobile when requested or required.

Verify the highest-value specified behaviors with a small, fast set of checks. For frontend work, inspect the target viewport and exercise actual user interactions. Defer slow checks unless repository requirements or risk demand them.

Report observed results and deferred verification.

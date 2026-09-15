---
name: soclaas
description: Use NUS SoCLaaS for chat, vision, model discovery, and audio or video transcription. Trigger whenever the user asks to use SoCLaaS, inspect its models, or transcribe media through it.
---

# SoCLaaS

Run `soclaas help` to discover the current commands and usage. Follow its output rather than guessing or reimplementing the API.

## Rules

- Query the CLI rather than guessing current model availability.
- For important transcription claims, verify the passage against the recording; plausible errors may evade automatic checks.
- Transcription timestamps are approximate chunk boundaries.
- If a model returns prose when an actual tool call or artifact was required, state that the requested action did not occur and retry with a clearer instruction.
- Never print API keys.
- If `soclaas` is unavailable, report that the CLI is not installed; do not silently substitute another provider.

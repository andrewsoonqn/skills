# AHMA approved patterns

These are AHMA design decisions to use when the task concerns the corresponding surfaces. They are approved patterns, not claims about the current implementation; inspect the branch before describing existing behavior.

- **Talk:** use an edge-to-content conversation with no redundant top header or top fade. Keep the composer at rest as a full-row text/call choice; on focus, the text field expands beneath the call action with a crossfade rather than a layout jump.
- **Profile:** use a full-row anchored language menu. Keep Delete account neutral by default and red when pressed. Use a filled treatment for phone-related icons/actions where the approved screen calls for it.
- **Call history:** lead with date, start/end time, and duration above the transcript's own scrolling area. Start the sheet at its large detent. Do not add a redundant “Voice call” title to the time-led history header.
- **Shared surfaces:** use shared sheet, menu, and confirmation-dialog patterns. Preserve existing dismissal affordances and task actions, including Cancel and Save. Use the established damped sheet motion (about 350 ms) rather than default Flutter motion where this pattern applies.
- **Do not re-propose previously declined changes without a new request:** adding an X to sheets, removing the bottom Close action, adding an illustration to the info sheet, bolding its title, or changing it to content-height sizing. Do not infer these changes from another mock.
- **Chat pending/thinking:** use the approved pending-to-sent bubble-surface transition and a separate “AHMA is thinking…” state; do not add a “Sending…” label under the user bubble.
- **Resource cards:** the model may choose one or more resources to show, but render their details from the curated record, not model-authored facts. With multiple resources, exactly one must be marked Recommended and the UI must make that recommendation clear. Preserve the approved highlighted horizontal carousel pattern where relevant.
- **Support email:** use a compact receipt row, status pill on the title line at right, and a recipient line prefixed with “To:”. Keep sent, needs approval, and failed outcomes semantically distinct and truthful.
- **Journeys and Actions:** use the Journeys | Actions aggregate. Actions contains stacked Done and To do groups; To do items are checkable and source journey/date can appear subtly. Reuse the same Done/To do components inside a single journey. “What we looked up” reflects resources actually shown, with the recommendation indicated; do not imply every search result was shown.
- Keep the remaining Journey-detail content unless it is clearly redundant. Do not turn an approved treatment into permission to remove unrelated content.

# Visual authoring

Shared authoring and review procedure for visual plans and visual explanations.
Resolve links in this reference relative to this reference's directory.

## Source and workflow

1. Reuse the task's existing `<workspace-root>/.pi/docs/NN-slug/` folder for source,
   exports, supporting files, and revisions. Use the repository root in a Git repository,
   otherwise the current working directory. For a new task, choose the next unused sequence
   number, padded to at least two digits starting at `01`, and a lowercase kebab-case slug.
2. Write `.mdx`. Begin with a single `# Title` heading. Do not use YAML frontmatter.
   Components need no imports.
3. Run `vplan components` for the installed compiler's supported syntax.
   Use the Markdown-child vocabulary below. VPlan is the compiler, not a fallback renderer.
4. Run `vplan check <file>.mdx`. Fix every reported source error and quality warning.
   Inspect diagrams, math, and charts in the compiled result.
5. Call `plannotator_mdx_review` with the original MDX path:

   ```json
   { "path": "/absolute/workspace/.pi/docs/NN-slug/plan.mdx", "open": false }
   ```

   The tool validates and compiles with VPlan, then starts original Plannotator's HTML
   annotation viewer. It returns promptly with a URL. Compilation failure does not open
   stale HTML. The generated file is `<name>.plan.html` beside the MDX.
6. Return the source link and review URL. Set `open: true` only when the user explicitly
   asks to open or see the review. Starting a review does not authorize implementation.
7. Read the current MDX before applying requested changes. Edit that same source file.
   Do not edit generated HTML or create numbered copies for review rounds.
8. After a revision, call `plannotator_mdx_review` again and return its new URL.
   Keep `open: false` unless opening was requested. Submission ends the previous review.
   Close an unfinished review before recompiling the same source.
   Native Plannotator refreshes from the generated HTML file. A compilation in another session
   can therefore change what an open review displays after refresh. Coordinate changes to shared files.

The user-owned implementation is at
`/Users/andrewsoon/dev/10-19_projects/12_open-source/plannotator`.
The Pi tool is loaded through `~/.pi/agent/extensions/plannotator-mdx.ts`.
Its `/plannotator-mdx <path>` command explicitly opens a session-linked review.

### Standalone fallback

If the tool is unavailable, report that session-linked delivery is unavailable.
An already configured extension may need `/reload` in Pi. Do not install packages or
change global Pi configuration as part of this skill.

To compile without opening a browser:

```sh
node /Users/andrewsoon/dev/10-19_projects/12_open-source/plannotator/bin/review-mdx.js /absolute/path/plan.mdx --compile-only
```

Return the source and generated HTML links. If the user explicitly requests a standalone
review, omit `--compile-only`. That command opens original Plannotator and waits for its result.
It does not attach feedback to Pi. Do not guess session IDs or claim that a standalone URL
is session-linked. Use copied feedback when no live Pi integration is available.

## Review and source changes

| Action | Review result | Pi effect |
|---|---|---|
| Send Feedback | Review ends | Queues comments with the original MDX path |
| Approve | Review ends | Queues document approval and any submitted comments |
| Close | Review ends | No feedback or approval message |
| Copy feedback | Clipboard operation | No automatic delivery |

Feedback returns only to the Pi session that started the review. Busy sessions receive it as
follow-up input. A private recovery copy is retained because Pi's enqueue API does not
acknowledge delivery. The integration does not retry automatically or move feedback into another
session after a session switch. The review is not a persistent workspace.

Use Plannotator's text or element annotations. Their selectors and anchors refer to generated
HTML, not MDX source ranges. Identify the corresponding source block before editing.
There is no rendered MDX editing or source-mapping UI. Document approval is not implementation
authorization. Continue only within the user's requested scope.

`Questions` choices in compiled static HTML do not use VPlan's interactive review protocol.
Add a Plannotator comment to submit an answer. Do not treat clicking a choice as agent feedback.

## Component catalogue

There are nine VPlan components: `Phase`, `FileTree`, `Chart`, `Stat`, `Compare`, `Matrix`,
`Callout`, `Questions`, and `Checklist`. Mermaid and math use fenced blocks.

Use Markdown children for data, not object props. Put block components on their own lines.
Use quoted strings and the bare `stacked` boolean. Do not write imports, exports, arbitrary
JavaScript, event handlers, authored CSS, raw HTML, or Markdown images.
Wrap literal angle brackets, braces, generics (`List<T>`), and tag-like text in backticks or fences.

### Phase and Callout

- `<Phase title="..." status="planned|active|done">`: one step in a numbered vertical timeline.
  Steps auto-number in order. Status defaults to `planned`.
- `<Callout type="note|tip|risk|decision|warn">`: highlight a risk, decision, tip, or note.

Both wrap Markdown and supported nested components. A `FileTree`, `Chart`, `Matrix`, Mermaid
fence, code block, or task list can sit inside a phase or callout.

### FileTree

File-change map. One bullet per file, `- <change> <path>`, where change is
`add|modify|delete|move`. A move needs both ends: `- move <from> -> <to>`.
A path ending in `/` can identify a whole directory. Append ` -- <note>` for a short inline
comment on the change. Keep it to a phrase.

```mdx
<FileTree>
- add src/gateway/rate-limiter.ts -- sliding-window check against Redis
- modify src/gateway/middleware.ts -- mount the limiter behind the flag
- delete src/gateway/legacy/
</FileTree>
```

### Chart

`<Chart type="bar|line|area|scatter|radar|gauge|funnel|treemap|pie" title="...">`:
estimates/metrics. Single series: one bullet per point, `- <label>: <value>`.
Multi-series (`bar`/`line`/`area`/`radar`): a table whose header is `category | series1 | series2`.
Cells after the first name the series and become the legend. The first column is the category axis.

Use exactly two value columns for `scatter`: `| point | x | y |`.
Use single-series lists for `pie`/`gauge`/`funnel`/`treemap`.
Use `gauge` for percentages on a 0–100 scale. Order funnel values descending when showing
narrowing stages. Add `stacked` to a multi-series `bar`/`area` to stack rather than group.

```mdx
<Chart type="bar" title="Effort (days)">
- Limiter: 2
- Dashboards: 1
</Chart>

<Chart type="line" title="Latency by stage (ms)">
| Stage | p50 | p95 |
|-------|-----|-----|
| Auth  | 12  | 30  |
| DB    | 40  | 120 |
</Chart>
```

### Compare

Weigh approaches side by side as pros/cons cards. Each option is a `## Name` heading.
Append `(pick)` to mark the recommended one. Follow it with `- pro:` / `- con:` bullets.
Include at least two options.

```mdx
<Compare>
## Redis sliding window (pick)
- pro: accurate
- pro: shared across nodes
- con: network hop

## In-memory token bucket
- pro: fast
- con: per-node only
</Compare>
```

### Matrix

A comparison grid: options across columns, criteria down rows. Write a Markdown table.
The first column is the row labels. Append `(pick)` to one column header to highlight it.
Include at least two option columns. Use `<Compare>` for pros/cons, `<Matrix>` for a scorecard.

```mdx
<Matrix>
| Dimension | Postgres (pick) | ClickHouse | DynamoDB |
|-----------|-----------------|------------|----------|
| Writes    | medium          | high       | high     |
| Querying  | high            | medium     | low      |
</Matrix>
```

### Questions

Questions or unresolved points worth surfacing, one per bullet. The title defaults to
"Open questions". Override with `title="..."`. Nest bullets one level deep to list likely
answers. Submit answers through Plannotator comments, not VPlan's separate review queue.

```mdx
<Questions>
- Should the limiter fail open or fail closed if Redis is unreachable?
  - Fail open, availability first
  - Fail closed, safety first
- Is a 15-minute access-token TTL acceptable?
</Questions>
```

### Checklist

Acceptance criteria / definition of done, or a set of checks or steps.
Use a Markdown task list: `- [x]` for done, `- [ ]` for todo. Change its state in the MDX source.

```mdx
<Checklist title="Done when">
- [x] Returns 429 over the limit
- [ ] Dashboards live
</Checklist>
```

### Stat

Headline facts or metrics as a grid of cards. One card per bullet:
`- <label>: <value> (<intent>) -- <caption>`. Intent is `note|good|warn|risk`.
Both `(intent)` and `-- caption` are optional. The value is free text (`5 min`, `99.9%`).
Use static facts here and time series in `<Chart>`. Omit filler or invented metrics.

```mdx
<Stat>
- Files changed: 12
- Est. uptime: 99.9% (good)
- RPO: 5 min (risk) -- worst-case data loss
</Stat>
```

## Diagrams, math, code, and readability

- Use a `mermaid` fenced block for flowcharts, sequence, state, class, ER, or XY-chart diagrams.
  Mermaid gantt and pie are not supported by this compiler. Use `<Chart type="pie">` for pie charts.
- Use a `math` fenced block for display LaTeX, such as `T(n) = O(n \log n)`.
- Use fenced code blocks with a language. VPlan uses Expressive Code and supports metadata such
  as `title="src/path/file.ts"`, `{2-4}`, and `ins={3-4} del={2} mark={6}`.
- Use ordinary Markdown tables, blockquotes, and task lists alongside components.
- Keep chart labels short. Separate series with wildly different magnitudes or normalize units.
- Keep Matrix cells to a word or short score. Put rationale in prose or a Callout.
- Avoid `-- comments` on FileTree move rows when the paths already crowd the row.
- Prefer `flowchart TD` for larger diagrams. Split sprawling diagrams into smaller ones.
- Inspect dense visuals at their intended viewing width after compilation.

## Portable export

The generated `<name>.plan.html` is the shareable document, separate from Plannotator's review UI.
It contains the compiled rendering runtime. It does not include Plannotator feedback controls.
Keep exports in the task folder and check them offline before describing them as self-contained.
Use [Static renders and exports](static-exports.md) for HTML, PDF, JPG, or a preview without review.
Do not use VPlan's separate interactive review queue for this workflow.

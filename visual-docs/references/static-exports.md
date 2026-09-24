# Static renders and exports

VPlan compiles the source. Use [Visual authoring](visual-authoring.md) for authoring
and session-linked review in original Plannotator.
Do not change installations or global Pi configuration.

Use these outputs when the user wants a shareable file or a preview without review.
Run `vplan check <file>.mdx` first. Open output only when explicitly requested.
The commands below suppress automatic opening.

## Static HTML page (`--static`)

`vplan render <file>.mdx --static --no-diff --no-open` writes `<file>.plan.html` next to the source:
a one-shot, self-contained page with no feedback layer. Keep exports in the task folder.

- `--out <path>` sets the output location (and implies a static render).
- `--stdout` writes HTML to stdout instead of a file and implies a static render.
  Use it in a pipeline. A `--stdout` render is deterministic and never auto-diffs.
- `--no-open` suppresses opening the result. Keep it unless opening was explicitly requested.

The iteration diff (git-gutter accents marking what changed since the last view) shows on a static
render too, not just in review: `vplan` snapshots each plan it presents, keyed by the file path.
`--diff <baseline.mdx>` diffs against an explicit file. `--no-diff` suppresses it.

## Live-reloading preview (`--watch`)

`vplan render <file>.mdx --watch --no-open` starts a hot-reloading dev server (default `--port 9140`,
auto-incrementing if taken). Editing the file live-reloads the page. It needs a real file rather
than stdin, writes no file, and runs until Ctrl+C. Use this only when a live preview is requested.
Run it through the harness's background-task support and stop it when the preview is no longer needed.
This is not the Plannotator feedback workflow.

## PDF / JPG export (`vplan export`)

Use `vplan export pdf <file>.mdx --no-open` or `vplan export jpg <file>.mdx --no-open`.
These build the self-contained page, then capture it headless. `pdf` prints a paginated A4
document. `jpg` captures a full-page hi-dpi screenshot.

- Output defaults to `<file>.pdf` / `<file>.jpg`. `--out <path>` overrides the location.
  For stdin input, supply `--out`.
- `--theme light|dark|system` overrides the baked color scheme.
- `--no-open` suppresses opening.
- It needs Chromium. It uses system Chrome/Edge or a Playwright-installed browser, with
  `--browser <path>` / `VPLAN_CHROMIUM` overrides. If no browser is available, report the gap.
  Do not install Chromium automatically.

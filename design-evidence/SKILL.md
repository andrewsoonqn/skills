---
name: design-evidence
description: Use when a product or UI decision needs screenshots of how existing products handle it, or mockups of the options drawn in the target app's own style.
---

# Design evidence page

One self-contained HTML page that settles a design question by showing it. Real screenshots show what other products do. Mockups show what each option would look like in our app. Prose only states the claim each figure proves.

VPlan (`visual-docs`) cannot carry images, raw HTML or authored CSS. Use this skill when the decision depends on seeing pixels. Use `visual-docs` for diagrams, tables and structure.

## Steps

1. **Frame.** List each open question with a code (Q3, Q4) and the patterns or options it compares. Done when every option the user must choose between has a planned figure: a screenshot, a mockup, or both.
2. **Collect evidence.** Get each product's own pixels, cheapest source first:
   1. Native captures already in the project (for example `docs/evidence/`).
   2. Images on the vendor's blog, docs or changelog. Fetch the page with `curl -sL -A 'Mozilla/5.0'`, extract `src`, `srcset` and `content` URLs ending in an image or video extension, then download the original-size asset.
   3. Demo videos. Find the moment with a contact sheet (`ffmpeg -i v.mp4 -vf "fps=1/4,scale=1400:-1,tile=3x3" -frames:v 1 sheet.png`), then extract the single frame (`ffmpeg -ss <t> -i v.mp4 -frames:v 1 frame.png`).
   4. A headless browser screenshot of a public page, only when no image asset exists. Follow `browser-policy`. Use fresh mode for public pages.

   Look at every image before using it and drop any that does not show the claimed behaviour. Done when every planned screenshot figure has an inspected image and a known source.
3. **Mock up the options.** Build each option in HTML and CSS inside the page, using the target app's palette and real content from the project: actual file names, code, numbers and labels from fixtures. Work out any computed example (rounding, totals) so it is correct. Label each mockup with its option code and the word mockup. Done when each option the user must pick has a mockup a reader can compare side by side.
4. **Compose.** Start from [the page template](references/template.html). Order: one muted line stating which images are native, third-party or mockup. Then per question: a heading, a short paragraph with the claim, figures with captions naming the product and what to look at. End with a comparison table (option, who does it, where it shows, when it is made). Mark any pattern no product has as "not found", not as an invention of yours.
5. **Place.** In a repository, write the page to `docs/explanations/<descriptive-name>.html`. Put images in a Git-ignored evidence folder and reference them by relative path. Outside a repository, follow `~/FILING.md`. Keep third-party screenshots out of Git.
6. **Publish and verify.** Serve the folder with a named `process` (`python3 -m http.server <port> --bind 127.0.0.1 --directory <docs root>`), map it with `tailscale serve --bg --tcp=<port> tcp://127.0.0.1:<port>`, and reuse existing mappings. Then:
   - `curl` the page and every image through the Tailscale IP and require HTTP 200.
   - Open the page headless, confirm every `img.naturalWidth > 0`, screenshot the mockup section and inspect it. Side-by-side grids need `grid-template-columns: minmax(0,1fr) minmax(0,1fr)` and `min-width: 0` on children, or wide code rows overflow the column.

   Done when every image returns 200 through the shared link and the inspected screenshot shows no overflow or broken image.
7. **Hand off.** Give the Tailscale IP link, the sources of third-party images, and any figure you could not obtain. Commit the HTML. State that the images exist only on this machine.

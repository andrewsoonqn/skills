# Managed Matt skills

`matt/` is installed output from `mattpocock/skills`. Its absence from Git tracking does not make it user-owned source.

Before changing any Matt skill, read `matt/.manager/README.md`.

- Express skill customizations as named unified diffs in `matt/.manager/patches/`, with paths relative to `matt/`, such as `a/pr/SKILL.md` and `b/pr/SKILL.md`.
- Edit manager source or configuration only under `matt/.manager/`. Make changes to installed skills through the manager, not direct edits to `matt/<skill>/`.
- Rebuild with `matt/.manager/manage.sh update`, inspect the resulting changes, then run `matt/.manager/manage.sh verify`. Test patches in an isolated manager copy first when an update could include unrelated upstream changes.
- If a patch fails, review the upstream change and revise the patch. Keep the existing installation intact until validation succeeds.
- Keep directory-wide agent instructions here, outside `matt/`. The manager replaces the whole Matt tree, preserving only its explicitly copied manager files.

Other skill directories are not covered by the Matt manager unless their own instructions say otherwise.

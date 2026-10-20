# Matt skill manager

This manager installs the selected skills from `mattpocock/skills` into `matt/`. The installed directories are managed output. Express local differences as named patches under `patches/`.

## Commands

Run from any directory:

```sh
~/.agents/skills/matt/.manager/manage.sh verify
~/.agents/skills/matt/.manager/manage.sh check
~/.agents/skills/matt/.manager/manage.sh update
```

- `verify` validates the current local installation without network access.
- `check` builds the latest candidate and reports whether the installed skills differ.
- `update` builds and validates the latest candidate, then replaces `matt/`.
- `install` is an alias for `update` for a restored manager checkout.

## Published PR skill snapshots

Every `update`/`install` exports the finished, patched `pr` skill **before** the
atomic replacement. The exporter and distribution history travel with `.manager`.
`verify` also checks that the current export matches the rendered files and PR
patch provenance. `check` builds the same export in its disposable candidate.
An upstream or patch failure leaves both the installed tree and export unchanged.

The tracked distribution is `matt/.manager/pr-distribution/`:

- `latest.json` selects a version, the SHA256 of its exact `manifest.json` bytes.
- `versions/<version>/` contains `manifest.json`, the unchanged rendered skill
  files, and the upstream MIT `LICENSE`. The manifest records byte counts,
  SHA256 hashes, the upstream lock record, and PR patch hashes.
- Versions are immutable and retained when a later update changes the skill.
  Repeated exports of identical inputs produce identical files and version IDs.

Commit the generated distribution with the manager/source changes and push using
the repository's normal Git workflow. Export is automatic during a rebuild;
network publication still requires that ordinary commit and push. The manager
does not auto-commit user files, auto-push, fetch new credentials, or install hooks.
The rendered `matt/pr/` remains ignored managed output. Do not edit its exported
copy or its source directly; customize through the tracked PR patch as before.

### Load once for a cloud PR task

Resolve the chosen published branch to one **full Git commit SHA** using the
task's existing GitHub connector. Use that SHA for every subsequent file fetch.
Retrieve `matt/.manager/pr-snapshot.py` from that commit. The existing connector
can then download `pr-distribution/latest.json`, the selected version's
`manifest.json`, and every file named in its `files` mapping, preserving relative
paths under a temporary local distribution directory. No local credentials are
copied. The connector, not a caller-provided download URL, establishes repository
and commit identity. Do not concatenate unvalidated manifest paths into filesystem
paths: reject absolute paths, `..`, and symlinks; the loader also rejects them.

Run the loader against those downloaded files:

```sh
python3 /path/to/pr-snapshot.py load \
  --source /path/to/downloaded/pr-distribution \
  --revision FULL_40_CHARACTER_COMMIT_SHA \
  --destination /workspace/shared/skills/pr-TASK_ID
```

Alternatively, when the cloud environment already has authenticated `gh`, the
loader performs those read-only API fetches itself:

```sh
python3 /path/to/pr-snapshot.py load \
  --repo andrewsoonqn/skills \
  --revision FULL_40_CHARACTER_COMMIT_SHA \
  --destination /workspace/shared/skills/pr-TASK_ID
```

The destination must be new. Download/validation failures do not install partial
skills or replace an existing directory. A successful load prints and saves
`.snapshot-pin.json` with the repository (for gh mode), commit, and version.
Repeating the same load verifies and reuses that local pin without consulting
`latest.json`; another commit is refused for that task. A connector download
must actually come from the supplied commit; hashes verify integrity, not the
identity of a caller-supplied directory. The loader is stdlib Python, and needs
`gh` only in `--repo` mode. It never changes authentication or network settings.

Read the installed `SKILL.md` and follow it for the task, retaining its existing
`agents/openai.yaml` invocation policy. When native skill discovery is wanted,
use a fresh task-local `.agents/skills/pr` destination or a symlink into that
supported skill location. Loading files alone does not activate a skill in an
already-running agent; the orchestrator must explicitly load/invoke the file.

**Task-start integration remains an explicit orchestrator handoff.** No supported
cloud task-start hook is connected by this change. Each new task must resolve a
published commit and perform the loading step; never refresh instructions halfway
through a task. The public repository requires no new credential to read, but
connector and network availability must already exist in the cloud workflow.

Test without touching the real skill or contacting upstream:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 matt/.manager/test-pr-snapshot.py
```

The disposable fixture runs the real manager update, patch, validation, export,
and atomic replacement with a fake installer transport. It checks reproducibility,
update propagation, historical versions, task pinning, tampering/incomplete
rejection, and preservation after a failed upstream update. The initial real
snapshot can be bootstrapped after validating the existing installation with:
`python3 matt/.manager/pr-snapshot.py export`. Normal future rebuilds need no
separate export command. Preserve `pr-upstream-LICENSE` and `CREDITS.md` when
redistributing snapshots; review licensing if upstream changes its terms.

A failed download, patch, or validation leaves the current installation unchanged. The final directory exchange is atomic and retains the previous tree until post-install verification passes.

## Nested skills across harnesses

Pi, Codex, and OpenCode discover skills inside `matt/` directly. Claude uses its own personal skills directory, and Gemini only discovers immediate skill directories in the shared root. Expose the nested skills through whole-directory symlinks:

```sh
~/.agents/skills/matt/.manager/manage.sh link-harnesses
~/.agents/skills/matt/.manager/manage.sh verify-harnesses
```

`link-harnesses` creates `~/.claude/skills/<name>` and `~/.gemini/skills/<name>` pointing at `matt/<name>`. It validates the managed installation and checks every destination for conflicts before creating links. Repeating it creates no duplicate entries. Existing unrelated entries are preserved, and conflicting names cause failure rather than replacement.

The links expose supporting files as well as `SKILL.md`, and continue pointing at the same source paths after `update`. Run `link-harnesses` again after adding names to `skills.txt`. After removing names, remove their old harness symlinks explicitly. Restart an existing harness session if it does not refresh its skill list.

`verify-harnesses` checks the current manifest's links without changing them. These commands use `$HOME` for harness destinations and make no changes to Codex, OpenCode, or Pi.

Run the isolated end-to-end test with `python3 ~/.agents/skills/matt/.manager/test-harnesses.py`. It exercises supporting files, repeated linking, source replacement, and conflict safety without changing your harness directories.

## Change the managed set

Edit `skills.txt`, one upstream skill name per line, then run `update`. A successful update removes skills no longer listed and installs newly listed skills.

Done when `verify` passes and every listed skill has one `matt/<name>/SKILL.md`.

## Add a local difference

1. Confirm that repository-wide policy belongs in `AGENTS.md` instead. Use a patch only when the installed skill itself must differ.
2. Add one narrowly scoped unified diff under `patches/<skill>-<purpose>.patch`.
3. Generate paths relative to `matt/`, such as `a/grilling/SKILL.md` and `b/grilling/SKILL.md`.
4. Run `update`.
5. Inspect the resulting Git diff.
6. Run `verify`.

If upstream changes the patched lines, `patch` fails and the installed tree remains unchanged. Review upstream before revising the patch. Do not make an unrecorded edit directly under `matt/<skill>/`.

## Update the installer CLI

`manage.sh` pins the `skills` CLI version so a CLI release cannot silently change installation behavior. Change `cli_package` in the script deliberately, run `check`, then run `update` and inspect the Git diff.

## Requirements

The manager requires macOS or Linux with `npx`, `python3`, and `patch`. Atomic directory exchange must be available through `renameatx_np` on macOS or `renameat2` on Linux.

## Invariants

- `skills.txt` is the managed skill set.
- `skills-lock.json` records the upstream installation generated by `npx skills`.
- `content-lock.json` records the post-patch paths, contents, file types, and permission bits so offline `verify` rejects unrecorded edits.
- `patches/` contains every local change to upstream skill files.
- The candidate must contain exactly the listed skills.
- Skill directory names must match each `SKILL.md` frontmatter `name`.
- Temporary agent fanout directories never enter `matt/`.

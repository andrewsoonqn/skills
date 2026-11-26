---
name: instabox
description: Use when the user wants a cloud Linux box (instabox sandbox) from the terminal with the `instabox` CLI — create one, SSH in, run a command in it, read its files, set its idle auto-pause, or delete it, or to report a problem with instabox itself (`instabox feedback`). For saving or restoring a box's disks, see instabox-snapshots.
metadata:
  installed-by: instabox
---

# instabox CLI

An instabox sandbox is a Linux VM (Debian, one user with passwordless sudo: named after your local username when created with `instabox create`, `user` from the dashboard, `dev` on older boxes; `instabox get <box>` shows it). It has a root disk and a persistent `/data` disk; HOME is `/data/home`. Each box belongs to an organization; access follows its membership and sandbox permissions.

## Sign in

```sh
instabox whoami              # who is signed in (fails if nobody)
instabox login               # device code: open the printed page, enter the code
```

A GitHub sign-in and a Google sign-in with the same verified email share one account; with different emails they are separate accounts with separate boxes. Both `instabox login` and `npx instabox@latest` sign in with a device code: they print a page and a code (and open the page when there is a browser); the user opens it on any device, enters the code and chooses GitHub or Google there. It works the same over SSH or on a machine without a browser. Relay the page and the code to the user and wait; the command finishes on its own. For Google directly, use `instabox login --provider google`, or `npx instabox@latest --google`. The CLI shares the sign-in `npx` made.

For CI or an agent without a browser, use an API key instead: `export INSTABOX_API_KEY=ibk_...` (the user creates it in the dashboard: API keys in the sidebar). Never print, commit or log a key.

## Templates

`agent-browser` is the default, so `create` needs no `--template` for ordinary work. It is Debian with git, gh, Node.js 22, Python (uv), Go, Rust, a C toolchain, Docker, Claude Code and Codex, plus a desktop (VNC, Chromium) ready for browsing or driving a GUI from the start. The dashboard shows it as **standard**. Pick another template only for its one purpose:

- `universal`: the same tools without the desktop, which installs itself the first time it is used (about half a minute); a smaller root disk. The dashboard shows it as **basic**.
- `herdr`: for the herdr client.
- `orca`: for Orca desktop and mobile.
- `t3`: for the T3 Code desktop and mobile clients.

`instabox templates` lists the ones this server offers. The free plan creates boxes from `agent-browser` only: another template is refused with `403 template_not_allowed` and needs a paid plan (the user upgrades on the dashboard). A box from a snapshot (`--snapshot`) works on every plan, whatever template the snapshot came from. Do not retry another template on the free plan; use `agent-browser`.

## Sizes

A box is 4 vCPU / 8 GB of memory unless `create` names another size of the account's plan with both `--vcpus` and `--mem-mib`:

| Plan | Sizes (`--vcpus` / `--mem-mib`)               |
| ---- | --------------------------------------------- |
| Free | 4 / 8192 (default)                            |
| Pro  | 2 / 4096, 4 / 8192 (default), 8 / 16384       |
| Team | 2 / 4096, 4 / 8192 (default) up to 32 / 65536 |

`instabox whoami --json` lists the sizes this account may create as `allowedSpecs` (the default first, then the plan's others and any an admin granted); check it rather than assuming the plan. Another size is refused with `400 spec_not_allowed`, whose message names the account's sizes. Pick a size for the work: 2 vCPU (paid plans) for light editing or a single agent, the default for most builds, 8 vCPU (paid plans) for heavy builds or many processes. `--snapshot` takes the same flags. The size is fixed once the box exists; for another size, save a snapshot and create a new box from it with the size flags.

## Everyday commands

```sh
instabox templates                              # base systems to start from
instabox create --name work                     # new box; waits until it is running
instabox ls                                     # your boxes and their states
instabox ssh work                               # interactive shell (leave with: exit)
instabox exec work -- uname -a                  # one command, no SSH client needed
instabox exec work --cwd /data/home -- ls -la   # exec runs `bash -lc` as the box's user
instabox files work /data/home                  # list a directory (or print a text file)
instabox auto-suspend work 10m                  # idle time before a paid box pauses
instabox max-run work 120                      # pause a paid box after two running hours
instabox max-run work -1                       # remove the runtime cap; idle policy still applies
instabox stop work && instabox start work       # stop ends processes, keeps disks
instabox suspend work && instabox resume work   # pause/resume keeps running processes
instabox rename work api                        # rename in place, any state; ID and port URLs stay
instabox rm work                                # delete the box
```

- Names or IDs (`m_...`) both work wherever `<id-or-name>` is accepted.
- `create` options: `--template T` or `--snapshot S`, `--vcpus N --mem-mib M` (a size of the plan, see Sizes), `--auto-suspend D|0`, `--max-run-minutes N`, `--meta K=V`, `--org O`, `--secrets all|NAME,NAME|none`, `--no-wait`.
- Idle auto-pause defaults to 30 minutes. Paid boxes allow 5, 10, 15, 20, 25 or 30 minutes, or `0` to turn it off. Free boxes keep 30 minutes unless an admin grants an idle override. Idle means no agent working, no terminal use and little CPU.
- Max run minutes is independent of idle activity: `-1` is unlimited, `0` pauses immediately, and a positive integer forces a pause after that many running minutes. Free boxes have a fixed 480-minute cap that only an admin session can change; paid boxes default to `-1` and can change it. An idle override does not permit changes to a free box's runtime cap. The first limit reached pauses the box; both timers restart after sleep and wake.
- A runtime pause blocks every wake path during a server-configured cooldown, 10 minutes by default. Wait until the `cooldownUntil` deadline shown by `instabox get`; edits cannot clear it. Afterward, an automatically paused box wakes on `exec`, `ssh`, `files`, a public port request or `instabox wake <box>`. A zero runtime cap must be changed before waking. A normal pause preserves memory and processes.
- Use `exec` to run a command and read its output, and `ssh` for an interactive shell.
- `exec` with one argument after `--` runs it as a shell string (`instabox exec work -- 'ls | wc -l'`); several arguments run as that exact argv, each quoted for you (`instabox exec work -- bash -c 'echo a b > /tmp/x'`).
- `exec` returns the command's exit code and takes `--stdin` to pipe input. It stops the command after `--timeout` seconds: 60 by default, 600 at most. Run longer commands (installs, builds, test suites) over SSH, which also returns the exit code: `instabox ssh work -- 'cd /data/workspace/app && npm ci'`. The box's runtime cap still applies during SSH or exec.
- The box's HOME has `MACHINE.md` (which box it is, its size, what survives a stop, the installed tools) and `AGENTS.md`. Both are worth reading before working in the box; they appear a moment after it starts.
- A public URL for a web server in the box: `instabox port publish work 3000` prints it (`instabox port ls`, `instabox port unpublish work 3000`). The URL works while the box runs.

## Organization Secrets

Secrets are encrypted API credentials owned by an org, each limited to the HTTPS hosts it may be sent to. A box that selects a Secret gets a placeholder in its environment, never the credential itself. When a request from the box goes to one of the Secret's allowed hosts over HTTPS, the outbound proxy swaps the placeholder in the request headers for the credential. Code in the box can call the API but cannot read or copy the credential. No header-name configuration is needed.

Secrets suit HTTP API keys and tokens that a client sends in a request header: model providers, GitHub's API, deploy and SaaS APIs. They do not cover database URLs or passwords, signing keys, or anything a client hashes, encodes or sends outside an HTTPS header; those need their own setup on the box.

Secrets replace the Vault, which is legacy and will be retired: save every new API credential as a Secret, never in the Vault, and do not suggest `vault set`, `set-file` or `import` to users. A new box without `--secrets` still gets an existing user's Vault items (see the last point below). Opt into Secrets with `create --secrets`, or use `secrets select` later. Metadata labels do not select Secrets, and Secrets do not deliver files.

```sh
instabox secrets ls --org team                 # metadata only
instabox secrets show work                     # selection and proxy status
instabox secrets set SERVICE_API_KEY --org team --host api.example.com
instabox secrets import .env --org team --host api.example.com   # every value gets these hosts
instabox create --name app --org team --secrets SERVICE_API_KEY
instabox secrets select work --secrets SERVICE_API_KEY,OTHER_API_KEY
instabox secrets push work                     # refresh the selection on a running box
instabox create --name tenant --no-vault --secrets none
```

- Values for `set` come from stdin or a hidden prompt. Never print a credential or put its value into agent output, chat, command arguments, or logs. Before asking for a credential, check metadata with `secrets ls --org <org>` and `secrets show <box>`. A silent check such as `test "${NAME+x}" = x` tests that the placeholder is present without revealing it; it does not prove the upstream accepts the credential.
- `--host` is optional and repeatable. Give each exact hostname the credential may be sent to; without `--host` (or with `--host '*'`) every public HTTPS destination is allowed. Schemes, ports, paths, IP addresses, and partial wildcards such as `*.example.com` are rejected. Use the service's API host, such as `api.openai.com`, never a guess from the credential's value.
- Org commands default to the signed-in user's personal org. Use `--org` for a team, and select only Secrets from the box's org. Value, host and deletion changes require an org owner/admin sign-in. API keys with the appropriate machine scopes can inspect metadata and manage sandbox selections, but cannot retrieve or change Secret values.
- `secrets select BOX --secrets` replaces the box's selection: `all`, `none`, comma-separated names, or a JSON array (which allows a Secret literally named `all` or `none`). Keep existing names when adding one.
- Placeholders work only in HTTPS request headers on port 443 to the allowed hosts. Do not hash, encode, or sign with a placeholder; other traffic carries the placeholder unchanged.
- Rotating a value keeps its placeholder, so running clients need no change. Newly selected names appear in new shells that load the managed environment; restart existing applications to pick them up.
- For a box intended for another person or tenant, disable personal Vault injection with `--no-vault` and select only the org Secrets they may use. For a fresh box with neither system's credentials, use `--no-vault --secrets none`. An empty Secret selection alone still permits Vault injection. These flags do not remove credentials already copied into a source snapshot.
- For an existing box, disable Vault with `start BOX --no-vault` or `resume BOX --no-vault` and clear the Secret selection with `secrets select BOX --secrets none`. Refresh a running guest with both `vault push BOX` and `secrets push BOX`. Vault values already copied into processes or files remain there; disabling Vault does not recover them.
- The Vault is legacy and will be retired; every `vault` command prints a warning. Its commands remain only for items a user already saved: `vault ls`, `show`, `push` and `rm`, and `vault export` to recover a retained item. A box may use Vault and Secrets together; Secrets wins same-named environment variables. Neither store copies or deletes the other. To move a Vault env item that is an HTTP API credential, the user enters its value again as a Secret with its hosts (`secrets set NAME --host HOST` reads it from a hidden prompt), you select it on the box, then `vault rm` it with the user's go-ahead. Never read a Vault value to copy it. Database credentials and other non-HTTP secrets are not supported by Secrets and need their own setup on the box; Vault file items likewise.

## Moving work onto a box

To move the repo the user is working in (with its worktrees, uncommitted work and agent conversations) onto a new box and install its dependencies there, follow the `instabox-move-repo` skill.

## When instabox itself gets in your way (feedback)

If instabox is at fault — a command breaks the contract its help or this skill states, the skill does not match what really happens, a capability is missing, or the CLI is confusing — report it, then carry on with the user's task using a workaround. Never block on the report, and never report problems in the code the user is building.

```sh
instabox feedback --json --type bug --component cli --area exec \
  --title "exec --timeout 600 stops the command at 60s" \
  --detail "instabox exec work --timeout 600 -- make test was killed after 60 seconds" \
  --command "instabox exec work --timeout 600 -- make test" \
  --expected "the skill says exec accepts up to 600 seconds" --doc "skills/instabox/SKILL.md" \
  --workaround "ran it over instabox ssh instead"
```

- `--type`: `bug` when something does not work as its help or the docs say (when instructions did not match reality, also give `--doc`, `--expected` and `--workaround`), `feature-request` when what you need is not supported, `friction` when it works but is confusing or awkward, `other` otherwise.
- `--component`: `cli`, `api`, `sandbox` (the box itself, its templates or tools), `dashboard`, `skills`, `docs` or `other`. `--severity blocker|major|minor` (default `minor`); `--sandbox NAME` names the box involved.
- Emails, keys, tokens, home paths and public IPv4 addresses are redacted before sending, but do not paste secrets into it. Signed in, the report opens a support ticket on the account, and the team's replies show in the dashboard at the link it prints (`ticket` in `--json`); signed out or waitlisted, it reaches the team without one.
- A failed or unconfirmed submission prints a warning and exits 0: do not retry. File one report per problem, not one per attempt.

## Habits

- Forgotten boxes pause themselves after 30 idle minutes. Delete a box with `instabox rm` once its work is done.
- When the user asks for a new box, create one, with a name `instabox ls` does not already show. Offer an existing box only when they want to continue earlier work in it.
- `instabox usage` shows storage use and limits. A quota error means delete or stop something; do not retry the same create in a loop.

---
name: session-search
description: >-
  Use when an answer may live in a past coding-agent session: "have we
  discussed X before", "how did we fix Y", "find that session where...",
  recalling a prior decision, error, or investigation, or checking whether
  Claude Code, Codex, OpenCode, Pi, or another agent already tried something.
  Also use before re-deriving work that appears previously solved.
---

# Session Search

Use `cass` to search local coding-agent histories. The usual binary is
`~/.claude/bin/cass` (`cass.exe` on Windows). It is machine-local and must never
be committed.

Set this once in shell commands:

```bash
CASS="${CASS:-$HOME/.claude/bin/cass}"
```

If that path is absent, try `command -v cass`. If the binary is still missing,
install it from the latest release of
`Dicklesworthstone/coding_agent_session_search`, then run `cass index`.

## Readiness

Start with the current machine-readable readiness contract:

```bash
"$CASS" triage --json
```

- If `search_completeness.can_search` is true, searching is usable.
- If recent sessions matter and the index is stale, run the safe incremental
  refresh command given in `next_command` or `recommended_commands`. Do not use
  a full rebuild merely because the index is stale.
- If the embedded recipes drift, consult `cass robot-docs`,
  `cass capabilities --json`, or `cass --robot-help` rather than guessing.

## Search

Start broad and bounded:

```bash
"$CASS" search "close_notify vsftpd" --robot --limit 8
"$CASS" search "ticket flow" --agent codex --robot --limit 8
"$CASS" search "session rail" --agent claude_code --robot --limit 8
"$CASS" search "skill pruning" --agent pi_agent --robot --limit 8
"$CASS" search "frecency" --workspace /path/to/repo --robot --limit 8
```

Useful provider slugs include `claude_code`, `codex`, `opencode`, `pi_agent`,
`copilot`, and `gemini`. It is `claude_code`, not `claude`; an invalid slug may
silently produce no hits. Check current slugs in `cass capabilities --json`.

Search is hybrid-preferred by default, but semantic refinement may be absent.
If zero hits appear, vary lexical clues: exact error strings, symbol names,
filenames, task names, and distinctive phrases usually beat a prose summary.
Time filters such as `--week`, `--days N`, and `--since YYYY-MM-DD` can narrow a
large result set.

Each machine has its own corpus unless remote sources were configured. When the
answer may be on another machine, inspect `cass sources list`; see
`cass robot-docs sources` for read-only discovery and remote-source setup.

## Follow up and report

Use search to explore candidates. Once the right query is known, prefer a
bounded evidence pack:

```bash
"$CASS" pack "query" --robot --max-sessions 5 --max-evidence 12 --max-tokens 6000
```

Inspect pack warnings, freshness, and `no_evidence_found`. `pack` is extractive
and read-only; it does not call an external model.

For a single hit, `cass view <source_path> --line N --context 5 --robot` shows
nearby source lines. Claude Code JSONL can contain enormous metadata lines, so
prefer search snippets or `pack`; never dump raw transcript JSONL into context.

Report:

- the conclusion found;
- the session source path and a short supporting excerpt for each recalled
  claim;
- freshness or coverage limits that affect confidence.

Past-session history is evidence of what was said or attempted, not proof that a
code or environment fact remains true. Verify current facts against the repo or
system before acting on them.

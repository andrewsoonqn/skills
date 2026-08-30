---
name: mail
description: Use when the user wants to read, search, summarize, check unread, or send their personal email — their NUS Outlook/Exchange account (e1375600@u.nus.edu) or their Gmail (andrewsoonqn@gmail.com). Triggers on "check my mail/inbox", "any new emails", "email from X", "send/reply to an email", "my NUS mail", university mail.
---

# Mail (NUS Outlook + Gmail)

## Overview
The user has two mail accounts, each accessed a different way:

- **NUS Outlook/Exchange** (`e1375600@u.nus.edu`) — read **locally via macOS Mail.app + AppleScript**. NUS Conditional Access blocks OAuth/MCP (sign-in error `53003`, unregistered device), so **never attempt the MCP/OAuth route for NUS** — it is a permanent dead end. In Mail.app this account is named **"Exchange"**.
- **Gmail** (`andrewsoonqn@gmail.com`) — read via the **claude.ai Gmail MCP** (`mcp__claude_ai_Gmail__*`). In Mail.app it is the account named **"Google"** (usable as a fallback / for sending).

Reading works off Mail.app's local cache and the Gmail API — no tokens needed for NUS. Requires the macOS **Automation** permission for controlling Mail (already granted; if revoked, re-grant in System Settings → Privacy & Security → Automation).

## Reading

**NUS — list recent messages** (helper avoids AppleScript heredoc-quoting bugs):
```bash
osascript ~/.agents/skills/mail/list-messages.applescript "Exchange" "Inbox" 12
```
NUS mailboxes: Inbox, Course Registration, Financial, Scholarship, Accommodation, SoC, NUSC, Promos, Library, Sent Items, Junk Email, etc. (run `list-mailboxes` below to refresh).

**NUS — search by sender/subject, read a body:**
```bash
osascript -e 'tell application "Mail" to get subject of (messages of mailbox "Inbox" of (first account whose name is "Exchange") whose sender contains "nus.edu")'
osascript -e 'tell application "Mail" to get content of (first message of mailbox "Inbox" of (first account whose name is "Exchange") whose subject contains "scholarship")'
```

**List mailboxes of an account:**
```bash
osascript -e 'tell application "Mail" to get name of every mailbox of (first account whose name is "Exchange")'
```

**Gmail — use the MCP tools** (load schemas via ToolSearch first): `search_threads`, then `get_thread` for bodies. Fallback: read the "Google" account in Mail.app with the same AppleScript pattern (replace `"Exchange"` with `"Google"`).

## Sending — draft in chat only; never touch Mail.app
Do NOT compose, open a compose window, or send through Mail.app (no AppleScript compose, no `send`). Write the draft directly in the chat so the user reviews and sends it themselves.

- Show the draft as plain text or inside a fenced code block — **never** as a Markdown blockquote (no leading `> `, which renders as a `|` bar down the left). Lay out To / Subject / body as plain lines, e.g.:
  ```
  To: prof@nus.edu.sg
  Subject: Subject here

  Body line 1
  Body line 2
  ```
- **Gmail only:** if the user asks, you may save it as a Gmail draft via MCP `create_draft` (the Gmail MCP has no direct-send tool). Do not auto-send.
- **NUS:** present the draft in chat; the user sends it from Outlook/Mail.app themselves.

## Common Mistakes
- **Inline AppleScript via `<<'EOF'` heredocs** mangle quoting (e.g. "Expected expression"). Use the `.applescript` helper files or single `-e` expressions instead.
- **Retrying MCP/OAuth or a custom Azure app for NUS** — Conditional Access (`53003`) blocks all of it. Use Mail.app.
- **Stale data** — Mail.app only has what it has synced locally; it's comprehensive here but not guaranteed real-time.
- **Sending via Mail.app** — don't. Never compose/send through Mail.app; draft in chat instead (see Sending).

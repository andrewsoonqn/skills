---
name: calendar
description: >-
  Read, propose, and write Google Calendar events for Andrew via the
  mcp__claude_ai_Google_Calendar__* tools, with a fixed house style for what
  an event looks like and a propose-then-confirm gate before any write. Use
  this skill whenever the user wants something put on a calendar, moved,
  deleted, or checked - including "add to my cal", "schedule this", "am I
  free Thursday", "when's my next X", pasted email invites, screenshots of
  run-sheets, deadlines found online, or commitments extracted from chat
  scans. Also use it when the user asks what's on their calendar or whether
  two things clash. Trigger it even when the word "calendar" is absent: "when
  am I free next week", "put this meeting somewhere", "don't let me miss the
  drop deadline", and "add the interview they just sent" all belong here.
---

# Calendar

Andrew's calendar is a working document he reads on a phone, often while
walking somewhere. An event earns its place by answering one question fast:
*what do I do now, and where.* Everything below serves that.

Primary calendar: `andrewsoonqn@gmail.com`. Every one of his calendars is
set to `Asia/Kuala_Lumpur` - same UTC+8 offset as Singapore, so nothing
shifts, but write `Asia/Kuala_Lumpur` unless the event genuinely happens
elsewhere. See **Time and timezone**; it is not automatic.

His calendars, and what belongs on each:

| Calendar | For |
|---|---|
| `andrewsoonqn@gmail.com` | Personal, default, anything uncategorised |
| `NUSWS` (`de8465...`) | Band: rehearsals, concerts, sectionals, FOP |
| `NUS Classes` (`7b1dec...`) | Academic: lectures, deadlines, CourseReg |
| `AHMA` (`e9fca6...`) | Family |
| `Craters` (`07fef5...`) | Craters work |

Two are read-only imports and should never be written to: `ANDREW SOON
QIAN Calendar (Canvas)` and `Calendar` (`ouuclj...`), both UTC.

## The loop

Ground, propose, wait for go, write, report. Never skip the middle.

**Propose before every write, without exception** - including a single
obvious event. This is not a size-scaled rule. Andrew typed "confirm and
wait for go" in three separate sessions, and the two largest writes in his
history (9 events, then 17) were the ones that had no gate at all. A rule
with exceptions gets its exceptions wrong exactly when the stakes are
highest, so this one has none.

Reading the calendar is not writing. `list_events`, `search_events`,
`get_event`, `list_calendars` need no gate - use them freely and early.

### 1. Ground

Before proposing anything, know what is already there.

- `list_calendars` if you have not this session. Events land on the wrong
  calendar otherwise, and moving them later means a delete plus a create.
- `list_events` over the target dates, plus a day either side. You are
  looking for two things: **something already covering this slot**, and
  **something that is this event under another name.**
- `search_events` with `fullText` when the thing might already exist under
  wording you would not guess. Also worth doing to see how Andrew has
  logged this kind of event before - matching his own past wording beats
  inventing a house style per event.

The duplicate check is the step most likely to be skipped and the one that
caused the most rework historically: an entire session was spent deleting
and rewriting events another session had created blind. If you find a
possible duplicate, say so in the proposal and offer replace-or-skip. Do
not silently create alongside it, and do not silently delete it either.

### 2. Propose

Show every field you resolved, not just the date. Andrew asked for this
specifically: the failure he is guarding against is a value he never
supplied appearing on the calendar as though he had.

Mark anything you inferred. Anything unmarked is a claim that he said it.

```
Wed 5 Aug 2026

1. Movie at GSC Imago
   2:00-4:30pm        ~ time inferred, see below
   GSC Imago, Imago Shopping Mall, Kota Kinabalu
   Asia/Kuala_Lumpur  ~ from "KK"
   -> primary calendar

2. Ahma call
   9:00-9:30pm        ~ "wed night" -> 9pm
   -> Family (shared)

Two things I need from you:
  - Movie showtime? I've put 2pm as a placeholder.
  - How long is the Ahma call usually - 30 min?
```

Resolve relative dates to an absolute date with the weekday attached. "Wed
5 Aug 2026", never "Wednesday". A wrong week is invisible in the second
form and obvious in the first.

**When something is missing, ask - but bring a guess.** An open question
costs a round trip; a question with a proposed answer lets him say "go" and
be done. Put the proposal in the event, flag it, and ask in the same
breath. Never invent a time and stay quiet about it - a calendar that
mixes his facts with your guesses, indistinguishably, is worse than one
with gaps.

For more than a handful of events, or anything opt-in, curate rather than
dump. Firm commitments with a time and a place belong on a calendar.
Maybes, FYIs, and undated tasks belong in a list in your message. When
Andrew was handed 15 candidates he kept 1 - so surfacing everything as a
calendar candidate wastes his attention rather than saving it.

### 3. Write

Only after an explicit go. Then report what landed, briefly.

## Anatomy of an event

### Title

Plain. The specific name of the thing and nothing else.

```
SIBF Opening Gala
Trumpet ensemble practice
CourseReg Round 1 closes
Movie at GSC Imago
```

No emoji, no `Concert:` prefix, no `- YOU PERFORM` suffix. Month view cuts
around 22 characters, and every decoration is spent before the calendar
says which event this is. Role, venue, and stakes have a home - the
description and the colour - and the title is not it.

One exception: prefix `⚠️ ` on a **hard deadline**, meaning something with
a real consequence if missed - a grade, a fee, a lost slot. Nothing else
gets an emoji. The mark only works while it is rare; when 17 coursereg
events all carried one, it stopped distinguishing anything.

Front-load the distinguishing word. `CourseReg Round 1 closes` survives
truncation; `NUS Course Registration Exercise - Round 1 Closing` does not.

### Description

HTML, structured as labelled lines. Verified by probe against the real
Calendar UI: `<b>`, `<i>`, `<a>`, and `<ul>/<li>` all render properly -
bold text, italics, a live blue link, a real bulleted list. `<script>` and
friends are stripped. There is no official allowlist, so stay inside those.

Raw `\n` renders as a line break, so plain newlines are enough - `<br>` is
unnecessary clutter. Note that `<ul>` adds noticeable vertical padding
around the list, which is fine for a genuine list and heavy for two items.

Lead with what he does. Close with anything uncertain, in italics.

```html
<b>You:</b> 2nd trumpet (Sharmila 1st, Abella 3rd)
<b>Standby:</b> 7:00pm, full black, already eaten
<b>Warm-up:</b> 7:30pm, recital studio
<b>Bring:</b> instrument, stand, black shoes

<a href="https://...">NUSWS master schedule</a>
<i>End time is a ~2h estimate - the running order wasn't published.</i>
```

Labels beat paragraphs because he is reading this one-handed, looking for
one fact. A wall of prose means scanning; `<b>Bring:</b>` means finding.

**Things that must survive into the description, always:**

- **Where it came from**, when it did not come from Andrew. `Source: NUSWS
  master schedule, 7 Jul` or `From: Mohli`. Six weeks later this is the
  difference between trusting the event and re-checking it.
- **Every value you inferred**, in italics, with what you inferred it from.
  A guess that is labelled is useful. A guess that is not is a lie he will
  act on.
- **Source disagreements**, unresolved. `The tpts chat says Thu 16 Jul
  7:30pm; the master schedule says Sun 19 Jul.` Pick the better-sourced one
  for the actual time, say why, and leave the conflict visible. Silently
  choosing means he cannot tell there was ever a question.
- **Clashes**, written on both events. `Overlaps FOP Day 2 (2-5pm) -
  deconflict on the day.` A conflict noted on one side only gets missed
  from the other.
- **Things deliberately not added**, and why. `NUS Commencement (~10am same
  morning) intentionally not added.` Without this a later session re-adds
  it, thinking it was an oversight.
- **What is still unknown**, as an open question rather than a blank.
  `Venue not yet decided - ask Wenn.`

Leave out anything the title, time, and location already say. Restating the
whole source email is not thoroughness, it is padding he has to scroll past.

### Location and links

Route by what the thing is:

| Thing | Field | Why |
|---|---|---|
| Physical place | `location` | Feeds the maps app and the travel-time estimate |
| Zoom / Meet / interview link | `location` | Tappable from the popup notification, where chips do not appear |
| Deck, doc, ticket, schedule PDF | `attachments` | `[{fileUrl, title}]` - renders as a tappable chip on the event |
| Passing reference, article | `<a>` in description | There when wanted, not competing for attention |

Always set `location` when a place exists, even if the description also
mentions it. `Venue not yet decided` buried in the description is invisible
to maps and easy to forget; an empty `location` field is a visible gap.

`attachments` accepts **any** URL, not just Drive. Verified by probe: a
plain `https://` page and a genuine Google Slides URL were both stored and
both rendered as chips, with the same generic document icon - Google
resolves neither against Drive, so a non-Drive link is not second-class
here. Secondary docs claim Drive-only; the live behaviour disagrees and the
official reference never states the restriction.

Use a chip when the thing is a document Andrew will open *at* the event -
the briefing deck, the ticket, the run-sheet. Use a description anchor when
it is merely where a fact came from. Chips are prominent, so more than two
or three stops them meaning anything.

Leave `eventType: FROM_GMAIL` events alone. Those are Gmail auto-generating
flight and booking events from mail; editing them fights a system that will
regenerate them.

### Colour

`colorId` carries the category, so the title does not have to.

| colorId | Colour | Category |
|---|---|---|
| `11` | Tomato | Hard deadline |
| `6` | Tangerine | Performing, playing, presenting - he is on |
| `9` | Blueberry | Class, lecture, exam, academic |
| `3` | Grape | Meeting, call, interview |
| `10` | Basil | Social, leisure, family |
| `5` | Banana | Travel, move, logistics |
| `8` | Graphite | Admin, FYI, low salience |

Set it every time. A calendar where some events are coloured and most are
default reads as noise rather than a system.

### Reminders

Three tiers, chosen by what missing it costs.

```
Ordinary          popup 1440, popup 60
He performs
  or travels to   popup 1440, popup 120
Hard deadline     popup 1440, popup 180, email 1440
```

The wider tier for performing and travelling buys packing and transit time.
The email on deadlines survives a silenced phone, which is the failure mode
that matters when the consequence is a grade.

Andrew's account default is a single popup 30 minutes before. Every tier
above is therefore a deliberate upgrade on it, not a restatement - which is
also why omitting `overrideReminders` is never neutral: it silently means
30 minutes, on a performance he has to travel to as much as on a call.

`minutes` is **minutes in advance**, so a *negative* value fires that long
*after* the start. That is a deliberate technique, not an error, and Andrew
already relies on it: his hand-made recurring "Anniversary" all-day event
carries `popup, -540`, which turns a useless midnight ping into a 9am one.

Two places it is the right tool:

- **All-day events**, which start at 00:00. A same-day reminder has to be
  negative to land at a civilised hour: `-540` is 9am.
- **Long windows**, where the useful nudge is before the *close*, not the
  open. On a 09:00-17:00 registration window, `-300` fires at 14:00 with
  three hours left.

For an ordinary timed event a negative value is almost certainly a mistake -
it fires once the thing has already begun.

Sending `overrideReminders` on `update_event` **replaces every existing
reminder**, including ones Andrew set by hand. When editing anything else -
a description fix, a venue - omit the field entirely.

### Which calendar

Always set `calendarId` explicitly. Defaulting to primary works until it
does not, and then the fix is a delete plus a create on the right calendar.

Personal and academic go to `andrewsoonqn@gmail.com`. Family and shared
things go to the relevant shared calendar - `list_calendars` and match by
name. If it is genuinely ambiguous, that is a line in the proposal.

Set `notificationLevel: "NONE"` on every create, update, and delete.

It governs one thing: whether **attendees** get emailed that the event was
created, changed, or cancelled. The default is `ALL`. It does not affect
Andrew's own reminders, and it does nothing on an event with no attendees -
so most of the time it is a harmless no-op. It earns its place on the edit
and delete paths, where a routine description fix on an event that does
have attendees would otherwise mail all of them.

It does **not** suppress notifications to people subscribed to a shared
calendar - those follow each subscriber's own calendar settings and cannot
be set from here. Adding to the Family calendar does not email the family.

Do not add `attendees` unless he asks to invite someone. An event with
attendees becomes an invitation with a response prompt.

### Time and timezone

Pass naive local time in `startTime`/`endTime` and set `timeZone` to the
IANA name:

```
startTime: "2026-08-05T14:00:00"
timeZone:  "Asia/Kuala_Lumpur"
```

`timeZone` overrides any offset embedded in `startTime`, so sending both is
redundant and invites the two disagreeing. One encoding, everywhere.

Pick the timezone from **where the event happens**, not where he is now.
A Kota Kinabalu cinema is `Asia/Kuala_Lumpur` even when booked from
Singapore. Getting this wrong shifts the event by hours silently.

`allDay: true` is for things genuinely without a time - a deadline day, a
travel day, a marker. Not for a timed event whose time you do not know: use
a flagged placeholder time and ask, so it sits in the day where it belongs
rather than in the all-day banner where it stops being seen.

### Shape

- **A multi-day window is not a multi-day block.** A registration round
  running 09:00 Mon to 12:00 Tue as one timed event paints 27 solid hours
  across his week. Give the window an all-day marker, or short events at
  each edge, and let the closing event carry the urgency.
- **Break the buried thing out.** When a day-long block hides something
  that matters - a 30-minute slot where he performs inside a 7-hour
  orientation - create it as its own event too, and say in the description
  why it is duplicated. Overlapping is the point: he will see the block and
  miss the slot otherwise.
- **Arrival buffer belongs in the time, not a reminder** - but only when
  he asks for one, and ask how much rather than guessing. Shift `startTime`
  earlier and state the real time in the description: `Actual performance
  11:15. Event starts 30 min early as arrival buffer.` An unexplained
  shifted start is indistinguishable from a wrong start.
- **Recurring things get `recurrenceData`**, an RRULE - not one event
  repeated by hand. A weekly family call is
  `["RRULE:FREQ=WEEKLY;BYDAY=WE"]`.
- **`availability: "AVAILABILITY_FREE"`** for markers and FYIs that should
  not make him look busy. Default (`BUSY`) for real commitments.

## Ask about role

When the source does not say what capacity he is attending in - attendee,
performer, organiser, OGL, helper - ask before proposing. It is one
question and it changes the title, the colour, the reminder tier, the
duties, the attire, and often the venue.

This is the single highest-value question in the whole flow. Two full
correction rounds were once spent rewriting events built on the assumption
that he was attending an orientation he was actually running.

## Editing and deleting

Edits and deletes go through the same propose-and-wait gate. A delete is
the only irreversible operation here, so name the exact event - summary,
date, time - and let him confirm that specific thing, not a count.

`update_event` only touches the fields you send. Use that: send the one
field that changed rather than rewriting the whole event. Three separate
rounds of wholesale description rewrites once happened where three targeted
edits would have done.

When amending a description, carry forward what was already there unless it
is what you are fixing. Source attribution and conflict notes get lost in
rewrites, and they are the parts that were expensive to establish.

## Worked example

Andrew pastes a meeting email and says "add to my cal".

**Ground.** `list_calendars`; `list_events` for 16 Jul ± 1 day; nothing
there, no duplicate.

**Propose.**

```
Thu 16 Jul 2026

NUS CO/SO/WS course update meeting
  8:00-9:00pm        both from the email
  Zoom               link in location
  -> primary calendar
  -> Grape (meeting), popup 1440 + 60

Nothing inferred - the email gave date, time, and link.
Go?
```

**Write**, on go:

```
summary:           "NUS CO/SO/WS course update meeting"
startTime:         "2026-07-16T20:00:00"
endTime:           "2026-07-16T21:00:00"
timeZone:          "Asia/Singapore"
location:          "https://nus-sg.zoom.us/j/6598295944"
calendarId:        "andrewsoonqn@gmail.com"
colorId:           "3"
notificationLevel: "NONE"
overrideReminders: [{popup,1440}, {popup,60}]
description: |
  <b>Meeting ID:</b> 659 829 5944
  <b>For:</b> students continuing with NUS Chinese Orchestra,
  Symphony Orchestra, or Wind Symphony
  <b>Covers:</b> course plan and schedule for the new AY, ahead of
  course bidding

  From: Mohli
```

Note what the description leaves out: the greeting, the congratulations,
the sign-off. He needs the meeting ID, who it is for, and what it covers.

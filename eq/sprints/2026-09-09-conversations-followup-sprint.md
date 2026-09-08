---
title: Conversations backdating/attachments — follow-up sprint
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Everything left open from the 2026-09-08 Conversations backdating/attachments feature (session-close card's 5 "Deferred" + 1 "Needs you" rows), plus a reminders idea Royce raised the next day with a live example — scoped via AskUserQuestion in-conversation and folded in here as a 6th item rather than tracked separately.
read_priority: high
status: live
---

# Conversations backdating/attachments — follow-up sprint

## How this was built

Built from the 2026-09-08 session-close card's 6 open rows (5 "Deferred" + 1 "Needs you") for the Conversations backdating/attachments feature ([eq-shell PR #1817](https://github.com/eq-solutions/eq-shell/pull/1817), [PR #1819](https://github.com/eq-solutions/eq-shell/pull/1819)). A 6th item — reminders on a conversation — was raised by Royce the next day with a live example (a Casual note reading "Intention is to employ Damon from 23rd September to…" with nothing tracking that future date) and scoped in-conversation via `AskUserQuestion` before being folded in here.

---

## Wave 1 — ship now, no more decisions needed

### 1. Add test coverage
No decision needed — straightforward engineering hygiene. This repo has an established `netlify/functions/_shared/*.test.ts` pattern (33+ files) never applied to `staff-resourcing.ts`'s pure logic: `avgRating`, `redactForViewer`, and the new summary-regeneration/sort-tiebreak logic from PR #1819 are all directly unit-testable with plain-object inputs, no mocking. `ConversationsSection.tsx`'s modal logic is harder to unit-test cheaply (heavy DOM/modal state) — function-level coverage first, lower priority than the Netlify-function side.

### 2. Reminders on conversations
**Scoped 2026-09-09, ready to build on your go.** Royce: "Can we add in reminders somehow?" — with a live example: a Casual note about a future commitment, nothing to surface it again when that date arrives.

Confirmed via `AskUserQuestion`:
- **All three entry types** get the field (Casual, Check-in, Development Review) — not Casual-only.
- **Surfaces on the Resourcing dashboard's existing "Who to catch up with next" card** as a new `REMINDER DUE` badge, alongside the existing `NEW — SAY HI` / `NEVER CHATTED` / `LAST CHAT · X AGO` ones — no new dedicated Reminders screen.

Build shape: a nullable `remind_at date` column on `app_data.staff_conversations` (same shape as `occurred_at` from #1817 — new migration, both planes), an optional "Remind me on" date field in the modal below the note/answers (all 3 templates), and `staff-resourcing.ts`'s existing "who to catch up with" selection logic extended to include anyone with an open conversation whose `remind_at` has arrived.

---

## Wave 2 — small decision needed first, each independently buildable once decided

### 3. "Logged after the fact" indicator
Named during the 2026-09-08 critique as a real gap, not built: once `occurred_at` differs from `created_at`, nothing in the UI shows a note was backdated — one reconstructed weeks later reads identically to one written the same day. **Your call whether that distinction matters enough for a small label** (e.g. "logged 4d later") — cheap either way once decided.

### 4. Casual-note attachment friction
Can't attach a document on a Casual note's very first save — has to be saved once, then reopened, before the attachment control appears (matches how Formal already worked, not a new inconsistency, but real friction for the exact "paper note, photographed and uploaded later" case the attachment feature was built for). **Your call whether it's worth restructuring** the modal to allow an attachment before the first save, or whether save-then-reopen is fine in practice.

---

## Wave 3 — needs a bigger decision before any code

### 5. "Overall score per person"
Sketched in conversation 2026-09-08, no code. Raw material already exists and is unused: the `happy_engaged` trend across Check-ins/Dev Reviews, the 7 tech-skill + 4 values ratings. **The real blocker is access, not UI**: `staff_conversations`' RLS is creator-only, so a genuine cross-manager score needs a narrow derived-data path (compute server-side, expose only the number/trend — the same boundary `staff-resourcing.ts` already draws for "was this person spoken to"), not a broader RLS loosening. Needs a decision on who's allowed to see it before this is buildable at all — this is the shape of the feature, not a small toggle.

---

## Not a build — needs your own action

### 6. Check the mobile view on your phone
Desktop confirmed live and correct (checked directly against a real record, via your own logged-in session). Forcing a real mobile viewport through available browser automation was a genuine dead end — window resize and Chrome DevTools' device toolbar both had no effect. No code fix available here; just needs you to glance at it on your actual phone next time you're in Core. No rush.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Test coverage | No decision needed | Build whenever |
| 2 | Reminders on conversations | Scoped 2026-09-09, ready | **Build on your go** |
| 3 | "Logged after the fact" indicator | Needs a small decision | Worth it? |
| 4 | Casual attachment friction | Needs a small decision | Worth restructuring? |
| 5 | "Overall score per person" | Needs a bigger decision | Who can see it? |
| 6 | Mobile view check | Not a build | Your own 15-second look |

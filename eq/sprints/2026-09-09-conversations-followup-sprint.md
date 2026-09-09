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

### 1. Add test coverage — ✅ DONE (2026-09-09)
[eq-shell PR #1830](https://github.com/eq-solutions/eq-shell/pull/1830) (open, not yet merged) — 16 tests covering `avgRating`, `trainingCounts`, `redactForViewer`, and a newly-extracted `findDueReminder` (pulled out of an inline `.find()` in item 2's own code so it's independently testable). `ConversationsSection.tsx`'s modal logic still has no coverage — heavier DOM/component-test lift, not attempted here, lower priority than the Netlify-function side.

### 2. Reminders on conversations — ✅ DONE (2026-09-09)
[eq-shell PR #1824](https://github.com/eq-solutions/eq-shell/pull/1824), merged, migration `0307` dispatched fleet-wide, confirmed live on both ehow and zaap. All three entry types get the field; surfaces on the Resourcing dashboard's existing "Who to catch up with next" card as a `REMINDER DUE` badge, no new screen — exactly as scoped below.

**Also: this shipped a real same-day outage, now fixed and written up as a standing lesson.** PR #1824's app code (which queries `remind_at`) auto-deployed on merge; the migration was left as a deliberately separate "dispatch when ready" step. That gap window broke `/sks/staff/resourcing` (`db_error`) until the migration was dispatched. Fixed within the same session once reported; see `feedback_migration_dispatch_before_merge_gap` in the eq-shell Claude memory store — future migration+code pairs in this repo should not repeat the deferred-dispatch pattern.

<details><summary>Original scope (for the record)</summary>

Royce: "Can we add in reminders somehow?" — with a live example: a Casual note about a future commitment, nothing to surface it again when that date arrives. Confirmed via `AskUserQuestion`: all three entry types get the field (not Casual-only); surfaces on the existing catch-up card, no new screen. Build shape: a nullable `remind_at date` column (same shape as `occurred_at` from #1817), an optional "Remind me on" date field in the modal, `staff-resourcing.ts`'s catch-up selection extended to anyone with an open conversation whose `remind_at` has arrived.

</details>

---

## Wave 2 — small decision needed first, each independently buildable once decided

### 3. "Logged after the fact" indicator — ✅ DONE (2026-09-09)
[eq-shell PR #1858](https://github.com/eq-solutions/eq-shell/pull/1858), merged and confirmed live (verified directly against the served JS chunk on core.eq.solutions, not inferred from deploy status — see `rules/deployment.md`'s 2026-09-09 correction to the eq-shell deploy-timing note this same session prompted). A pure `backdateLabel` function (`staffHelpers.ts`, local-calendar-day diff) drives a small "Logged Nd later" label next to the date, shown in the Conversations list row and the read-only view modal whenever `occurred_at` differs from `created_at`'s day. Unit tested (5 cases in `staffHelpers.test.ts`, timezone-robust fixtures).

<details><summary>Original scope (for the record)</summary>

Named during the 2026-09-08 critique as a real gap, not built: once `occurred_at` differs from `created_at`, nothing in the UI shows a note was backdated — one reconstructed weeks later reads identically to one written the same day. Approved 2026-09-09 via a pending-items triage pass.

</details>

### 4. Casual-note attachment friction — ✅ DONE (2026-09-09)
Same PR as item 3, [eq-shell PR #1858](https://github.com/eq-solutions/eq-shell/pull/1858), merged and live. The Casual-note modal's first "Save" click now creates the row and keeps the modal open (button becomes "Done") so `ConversationAttachments` has a real id to attach against immediately, in one sitting — no save-then-reopen round trip. Formal entries are unchanged (Royce approved Casual only — Formal has the identical limitation but wasn't the case that motivated this).

<details><summary>Original scope (for the record)</summary>

Can't attach a document on a Casual note's very first save — has to be saved once, then reopened, before the attachment control appears (matches how Formal already worked, not a new inconsistency, but real friction for the exact "paper note, photographed and uploaded later" case the attachment feature was built for). Approved 2026-09-09 via a pending-items triage pass, Casual only.

</details>

---

## Wave 3 — needs a bigger decision before any code

### 5. "Overall score per person" — ⛔ HELD, explicitly NOT approved (2026-09-09)
Considered in the same 2026-09-09 pending-items triage pass that approved items 3 & 4 above, and deliberately NOT approved — do not pick this up without a fresh decision from Royce, even though 3 & 4 are now done. Sketched in conversation 2026-09-08, no code. Raw material already exists and is unused: the `happy_engaged` trend across Check-ins/Dev Reviews, the 7 tech-skill + 4 values ratings. **The real blocker is access, not UI**: `staff_conversations`' RLS is creator-only, so a genuine cross-manager score needs a narrow derived-data path (compute server-side, expose only the number/trend — the same boundary `staff-resourcing.ts` already draws for "was this person spoken to"), not a broader RLS loosening. Needs a decision on who's allowed to see it before this is buildable at all — this is the shape of the feature, not a small toggle.

---

## Resolved without a build

### 6. Mobile view — ✅ CONFIRMED (2026-09-09)
Turned out not to need your own phone check after all — a second attempt at forcing a mobile viewport through browser automation worked this time (the first attempt's failure was a transient tool/session issue, not a real limitation). Verified directly, real production, real session: the mobile roster card layout, the person detail sheet, and the "Log a conversation" modal (both new date fields side by side, no overflow) all render correctly at 390px wide. Nothing further needed here.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Test coverage | ✅ Done — PR #1830 open | Merge when ready |
| 2 | Reminders on conversations | ✅ Done — live | Nothing — watch for a real reminder to confirm the badge |
| 3 | "Logged after the fact" indicator | ✅ Done — PR #1858 merged, live | Nothing |
| 4 | Casual attachment friction | ✅ Done — PR #1858 merged, live | Nothing |
| 5 | "Overall score per person" | ⛔ Held — explicitly not approved | Needs a fresh decision from Royce |
| 6 | Mobile view check | ✅ Confirmed live | Nothing |

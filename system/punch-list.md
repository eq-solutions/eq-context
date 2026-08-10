---
title: PUNCH LIST — Active Work Queue
owner: Royce Milmlow
last_updated: 2026-08-11
scope: The capped, currently-active work queue. Read at session start next to TODAY.md. Separate from the full eq/pending.md backlog.
read_priority: critical
status: live
---

# PUNCH LIST — Active Work Queue

Created 2026-08-08 because `eq/pending.md` re-inflated to 563–565 open items
12 days after a cleanup triggered by the same problem (`ops/decisions.md`
2026-07-27) — and a chunk of that isn't even engineering debt (`digest.md`
already separates a 109-item "waiting on Royce" bucket from real backlog).
`pending.md` stays the full record. This file is the short list of what's
actually being worked **right now**.

---

## Rules

- **Capped at ~5–6 items.** If it's not here, it's not active — check
  `eq/pending.md` for everything else.
- **Royce adds and removes items.** An assistant may propose a swap; it
  does not add one unilaterally.
- **An item leaves three ways only:** done, explicitly deferred back to
  `eq/pending.md` with a reason, or explicitly killed. Never silently
  dropped.
- Sourced initially from Royce's 2026-08-08 brain dump (17 items,
  cross-checked against the live substrate before this list was cut).
  The other 12 items from that dump are visible, not lost — they're in
  `eq/pending.md` (tracked/partial) or simply not yet on this list (new).

---

## Active (5)

### 1. Onboarding procedure — suite-wide, not just Cards
Settled for Cards specifically: self-join-only by design, `AdminBulkInvite.tsx`
solves a different problem, not a real gap (`eq/pending-archive.md`,
2026-08-08). Not yet written down as one place that states, per app/scenario,
who uploads onboarding info. **Done =** one doc states the intended flow
per scenario.

**Proposed done, 2026-08-11 — your call to tick off:** `eq/identity/worker-onboarding-flows.md`
now states the per-app flow (Cards settled, Shell admin/worker-invite,
Field manager-driven, Service read-only from Shell), written 2026-08-10.

### 2. Definitive backup rules plan
Target design exists (`system/infrastructure.md` → "Backup strategy — target
state"), never turned into a plan actually being followed. PITR explicitly
declined already (`eq/pending-archive.md`, 2026-07-23). **Done =** a written
plan — what's backed up, how often, retention, restore-test cadence.

**Proposed done, 2026-08-11 — your call to tick off:** the old target-state
section in `system/infrastructure.md` was stale (planned, never built) —
corrected 2026-08-10 to point at `system/dr-backups.md`, the actual
shipped implementation (full logical dump + all buckets + Sentry cron
check-in, ~6¢/mo, not zero-touch — see [[platform-dr-plain-english]] memory
for the plain-English version).

### 3. Mobile polish (Field/Cards) — close the remainder
8 PRs merged 2026-08-08 in eq-field already. Remaining un-eyeballed screens
flagged 2026-07-07 (`eq/pending.md`). **Done =** remaining screens reviewed,
item closes.

### 4. Cards info density — simplify/collapse
Not tracked anywhere before today. Brain dump: "Cards is very heavy on
information — look at simplifying or collapsing info unless a user clicks
around." **Needs scoping first** — which screens, what collapses by default.

### 5. Write up "what intake does" as a durable answer
Already answered — cross-repo audit closed the question 2026-08-08
(`eq/pending.md:17-31`, session close). Currently only lives as a pending
entry. **Done =** a short reference doc (or a pointer added to
`eq/products.md`) so the question doesn't get re-asked next quarter.

**Proposed done, 2026-08-11 — your call to tick off:** `eq/products.md`
gained a "EQ Intake — import/write-time engine" section 2026-08-10, with
the per-app usage table (Shell yes; Service/Field/Cards no, with reasons).

---

## Parked from the same brain dump (visible, not on the active list)

Tracked/partial in `eq/pending.md` already — pull one up here when a slot
opens: security settings per user group (active today, needs click-test),
prebuilds/AI pricing help (active), apprentices onto tracker (39 days stale,
flagged as needing a dedicated session), redundancy review (only answered
narrowly for Cards), env var/secrets structure doc, compliance docs
(SWMS + SKS-site linking, signing itself is live), templates (warranties/QA
remainder — DB schedules are 12/15 done).

Genuinely new, not tracked anywhere: manuals in EQ, acknowledgement feature,
labour-hire self-verify times, roster-change notifications, simultaneous-user
limits/edge cases.

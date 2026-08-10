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

## Active (2)

### 3. Mobile polish (Field/Cards) — close the remainder
8 PRs merged 2026-08-08 in eq-field already. Remaining un-eyeballed screens
flagged 2026-07-07 (`eq/pending.md`). **Done =** remaining screens reviewed,
item closes.

### 4. Cards info density — simplify/collapse
Not tracked anywhere before today. Brain dump: "Cards is very heavy on
information — look at simplifying or collapsing info unless a user clicks
around." **Needs scoping first** — which screens, what collapses by default.

**Scoped 2026-08-11, not built:** `eq/cards-info-density-scoping-2026-08-11.md`
— Wallet (home tab) is the real target (up to 7 stacked nudge cards for a
new/mid-setup worker, plus urgent items rendering twice); proposed fix is a
collapsible "To do" summary + de-dupe, sized Medium. One small companion fix
on the licence-detail screen (uncapped metadata rows), sized Small.
Everything else checked is fine as-is. Ready for a build session whenever
you want it — not started.

---

## Closed

### 1. Onboarding procedure — suite-wide, not just Cards
**Closed 2026-08-11, confirmed by Royce.** `eq/identity/worker-onboarding-flows.md`
states the per-app flow (Cards self-join, Shell admin/worker-invite, Field
manager-driven, Service read-only from Shell) — written 2026-08-10, verified
against live code before being marked done (every citation checked against
the real repos). Two nuances worth knowing but not gaps in the doc: Cards
self-join has a manager-approval gate on by default (not fully zero-touch),
and Field's CSV-import fix (PR #660) is live but not yet click-tested on
real data.

### 2. Definitive backup rules plan
**Closed 2026-08-11, confirmed by Royce.** `system/infrastructure.md`'s stale
"target state, not built" section was corrected to point at
`system/dr-backups.md` — the plan that actually shipped 2026-07-04/05
(full logical dump + all buckets + Sentry cron check-in, daily automated
restore-verify, one proven quarterly restore-drill). 3 real gaps found during
the confirmation pass, folded into `dr-backups.md`'s own Follow-ups section
rather than reopening this item: no restore-drill exists for eq-canonical or
eq-canonical-internal (only ehow has ever had a restore proven), no backup
coverage for the GitHub repos themselves (DB/storage only), and PITR-off is
only formally decided for SKS Labour — the three platform-DR projects carry
the same cost logic without an explicit re-confirm.

### 5. Write up "what intake does" as a durable answer
**Closed 2026-08-11, confirmed by Royce.** `eq/products.md` gained a
"EQ Intake — import/write-time engine" section 2026-08-10, with the real
per-app usage table (Shell yes; Service/Field/Cards no, with reasons).

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

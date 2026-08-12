---
title: Field mobile-experience centering — P1/P2/P3 sprint
owner: Royce Milmlow
created: 2026-08-12
source: C:\Users\EQ\OneDrive - eq-power.com.au\eq-field-mobile-centering.html (audit dated 2026-08-07)
repo: eq-field
scope: Originally 12 P1 + 2 P2 + 2 P3 items from a 2026-08-07 mobile audit. Corrected same-day, 2026-08-12, after live verification found all 12 P1 items already shipped, and again after live-code checks found Leave's supervisor view already built. Real new work landed: Safety count prominence + Leave tap-target fix (v3.5.484, PR #680). Remaining: Calendar mobile view + 2 small bundle-ins.
read_priority: high
status: draft
---

# Field mobile-experience centering

**Status:** P1 verified already-shipped (no build needed). Safety + Leave fixes built, tested, deploy-preview verified, PR #680 open — awaiting Royce's merge call. Calendar not started.

## What actually happened (P1)

The source audit (`eq-field-mobile-centering.html`, 2026-08-07) listed 12 P1 items as open gaps. All 12 were already shipped in `v3.5.469` before this sprint started — see this file's git history (commit `2becb4e`) for the full per-item table.

## What actually happened (P2 — Safety + Leave)

Scoped as "build a worker/supervisor split for Safety and Leave" on the assumption neither existed yet. Before writing code, live verification found:

- **Leave already has a full split** — `_renderLeaveSupervisor()` / `_renderLeaveWorker()` have existed for a while, already mobile-responsive (pending-approvals panel already stacks first on phone). The scoping doc's premise was wrong. Only real gap: the approve/reject buttons were 32×32px, under the 44px tap-target standard.
- **Safety's permission model is different than assumed** — Prestart/Toolbox/Diary/Incident list pages are already supervisor-only by permission grant (`reports.prestart.view` etc. — employees only hold `.sign`, not `.view`/`.create`). There's no worker view of that list to split from; supervisors are already the sole audience. Asked Royce which real gap to close instead: the today-count on each list header was an 11px grey line under the date — barely visible. He picked the simple fix (make it loud) over the more complex option (cross-reference today's roster to flag missing crews).

**Shipped, v3.5.484, PR #680:**
- Prestart/Toolbox/Diary/Incident: today's count is now a 26px number, leading each list header.
- Leave: approve/reject buttons bumped to 44×44px below 768px.
- Verified on the deploy preview against live rendering (not just code review) — all 4 Safety headers and the Leave stylesheet confirmed correct, no new console errors.

Awaiting Royce: merge PR #680.

### Timesheets — explicitly deferred

Royce's call, 2026-08-12: mobile timesheets isn't a priority right now. Revisit only if there's a reason to believe people are actually trying to do timesheets on their phone.

### Calendar — mobile agenda list (not started)

Desktop's month grid doesn't fit a phone (confirmed — `scripts/calendar.js` has zero mobile handling). Scoped fix: below phone width, swap the grid for a scrolling list of dates (date + who's on leave that day), tap a date for the existing detail view.

## P3 — small, bundle into a future PR (no separate work)

| # | Gap | Plan |
|---|-----|------|
| 1 | Several manager-only buttons under 44px tap target | Not independently confirmed against specific buttons — sweep opportunistically whenever a relevant file is next touched. |
| 2 | Teams missing active-state highlight in mobile drawer | Confirmed open (v3.5.469's own changelog flags it). One-line fix — bundle into whichever PR next touches `index.html`'s drawer wiring. |

## Lessons

1. The source OneDrive doc had no version stamp tying it to a specific commit/release — no cheap way to tell "already fixed" from "still open" without reading the actual code. Any future audit-style doc should note the `APP_VERSION` it was checked against.
2. Same lesson, twice in one sprint: a planning doc's *design* assumptions (not just its bug list) can also be stale. "Leave needs a supervisor view built" and "Safety needs a worker/supervisor split" were both wrong once the actual permission model and existing code were checked. Verify the code, not just the symptom list, before scoping a build.

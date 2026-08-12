---
title: Field mobile-experience centering — P1/P2/P3 sprint
owner: Royce Milmlow
created: 2026-08-12
source: C:\Users\EQ\OneDrive - eq-power.com.au\eq-field-mobile-centering.html (audit dated 2026-08-07)
repo: eq-field
scope: Originally 12 P1 + 2 P2 + 2 P3 items from a 2026-08-07 mobile audit. Corrected same-day, 2026-08-12, after live verification found all 12 P1 items already shipped. P2 (per-role split + Calendar) is now scoped and ready to build. Real remaining backlog is 2 build-ready items + 2 small bundle-ins.
read_priority: high
status: draft
---

# Field mobile-experience centering

**Status:** P1 done (verified, not built — see below). P2 scoped 2026-08-12, ready to build. Nothing built yet.

## What actually happened (P1)

The source audit (`eq-field-mobile-centering.html`, 2026-08-07) listed 12 P1 items as open gaps. Before starting build work, each was re-verified against live `main` (per this repo's standing Rule 0.5: verify live, don't trust a doc). **All 12 were already shipped** in `v3.5.469` ("Mobile P1 bundle") plus 3 companion changelog entries in the same version. The audit doc had no version stamp and was never updated after that release shipped. Full per-item verification table lives in this file's git history (commit `2becb4e`) — trimmed here to keep the live doc focused on what's actually left.

## P2 — scoped 2026-08-12, ready to build

Design direction from Royce: **100/100 solutions, tech invisible, keep it simple.** Concretely — reuse the exact split pattern Home already runs (one render path for workers, one for supervisors, picked by the same `isManager` check already used everywhere in this codebase). No new mechanism, no new config, no new page type. Just point the existing pattern at two more surfaces.

**Priority call (Royce, 2026-08-12): Leave and Safety are real gaps worth building now. Timesheets mobile is explicitly not a priority — skip it.**

### Safety forms — worker view (unchanged) + supervisor view (new)

| Role | What they see |
|------|----------------|
| Worker / apprentice | Unchanged — today's prestart/toolbox/diary as one big fast action, fill and sign. This part already works well; don't touch it. |
| Supervisor (new) | An oversight strip above the form list: "X of Y crews haven't submitted today" with a tap-through to chase whoever's outstanding. Same stat-row-plus-list shape Home's supervisor view already uses — just pointed at prestart/toolbox submission status instead of roster data. |

### Leave — worker view (mostly unchanged) + supervisor view (new)

| Role | What they see |
|------|----------------|
| Worker / employee | Their 3 balance numbers (already fixed, P1.11) + their own request history + a "Request leave" button, front and center. |
| Supervisor (new) | Their approval queue front and center — pending requests needing a decision, approve/reject one tap away — plus a simple "who's off this week" glance. Same pattern as the Safety supervisor view above. |

### Timesheets — explicitly deferred, not scoped further

Royce's call, 2026-08-12: mobile timesheets isn't a priority right now. No per-role split, no further mobile work here until real usage data says otherwise. Revisit only if there's a reason to believe people are actually trying to do timesheets on their phone.

### Calendar — mobile agenda list

Desktop's month grid doesn't fit a phone (confirmed — `scripts/calendar.js` has zero mobile handling). Simple fix, no new interaction to learn: below phone width, swap the grid for a scrolling list of dates (date + who's on leave that day), tap a date for the same detail view that already exists. Same information as the grid, just stacked instead of gridded.

## P3 — small, bundle into the P2 build (no separate work)

| # | Gap | Plan |
|---|-----|------|
| 1 | Several manager-only buttons under 44px tap target | Not independently confirmed against specific buttons — sweep opportunistically whenever the Safety/Leave supervisor views are being touched anyway. |
| 2 | Teams missing active-state highlight in mobile drawer | Confirmed open (v3.5.469's own changelog flags it). One-line fix — bundle into whichever PR next touches `index.html`'s drawer wiring. |

## Lesson

The source OneDrive doc had no version stamp tying it to a specific commit/release, so there was no cheap way to tell "already fixed" from "still open" without reading the actual code. Any future audit-style doc should note the `APP_VERSION` it was checked against, so staleness is detectable at a glance next time.

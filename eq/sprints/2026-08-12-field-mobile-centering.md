---
title: Field mobile-experience centering — P1/P2/P3 sprint
owner: Royce Milmlow
created: 2026-08-12
source: C:\Users\EQ\OneDrive - eq-power.com.au\eq-field-mobile-centering.html (audit dated 2026-08-07)
repo: eq-field
scope: Originally 12 P1 + 2 P2 + 2 P3 items from a 2026-08-07 mobile audit. Corrected same-day, 2026-08-12, after live verification found all 12 P1 items already shipped. Real remaining backlog is 3 items (2 P2 + 1 P3).
read_priority: high
status: draft
---

# Field mobile-experience centering

**Status:** corrected 2026-08-12 — see "What actually happened" below. Only 3 items remain open.

## What actually happened

The source audit (`eq-field-mobile-centering.html`, 2026-08-07) listed 12 P1 items as open gaps. Before starting build work, each was re-verified against live `main` (per this repo's standing Rule 0.5: verify live, don't trust a doc). **All 12 were already shipped** — mostly in a single release, `v3.5.469` ("Mobile P1 bundle — 5 confirmed mobile.css bugs, one release"), plus 3 companion changelog entries in the same version (Calibration+Projects drawer, Safety Records role gate, Skills Passport dead CSS). The audit doc was almost certainly the scoping input for that release and was never updated afterward — it kept describing bugs that were already fixed.

This means "start P1 now" required zero new code. Caught before any eq-field file was touched.

## P1 — all 12 items, verified already shipped (v3.5.469)

| # | Gap | Verified fix |
|---|-----|---------------|
| 1 | Bottom-nav clearance CSS bug | `styles/mobile.css` — `.page{padding:10px 10px 76px}` (was a bare `padding:10px` wiping the 76px nav clearance) |
| 2 | Crew-name overflow — Prestart/Toolbox/Diary/Incident | All 4 (`site-reports.js`, `toolbox.js`, `diary.js`, `incidents.js`) carry identical `min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis` |
| 3 | Prestart crash-recovery draft loss | `site-reports.js` — full stash/resume via `visibilitychange`/`pagehide` + `sessionStorage`, 30-min TTL |
| 4 | Incident modal height, Shell-embedded mode | `#modal-incident` added to the shell-mode forced-height selector list |
| 5 | Sign Documents: mobile-style call + unguarded popup | `injectMobileStyle('signdoc')` wired; `window.open()` return value checked, toast on popup-block |
| 6 | Apprentices Skills Passport — dead CSS selector | `styles/apprentices.css` selector corrected from nonexistent `#section-apprentices` to `#page-apprentices` |
| 7 | Calibration + Projects unreachable on mobile | Both added to the mobile drawer + `DRAWER_NAV_PAGES` |
| 8 | Roster Overview map — no mobile hide | `#rv-ov-map` + toggle hidden below 768px, same as Dashboard's map |
| 9 | Edit Roster undo/redo unreachable on mobile | Undo/redo buttons now survive the blanket `.topbar-actions .btn{display:none}` rule |
| 10 | Timesheets Job Numbers panel — fixed 260px sidebar | Converted to the same bottom-sheet convention as mobile modals |
| 11 | Leave balance cards squeeze at phone width | `leave.js` — stacks to 1 column below 560px |
| 12 | Safety Records — no role gate in code | **Royce's call was already made and implemented**: prestarts/toolboxes stay open to everyone; incidents/records gated to `reports.incident.view` (manager/supervisor) |

No action needed on any of these. Item 12 in particular: the decision this sprint flagged as "blocked on Royce" turns out to already have Royce's own decision quoted directly in the changelog ("safety history is fine - we want to enable everyone for prestarts and toolboxes only. incidents and records should be gated.") and built.

## P2 — genuinely still open (re-verified 2026-08-12)

| # | Gap | Status |
|---|-----|--------|
| 1 | Safety forms, Timesheets, Leave never got a Home-style per-role split | Confirmed open — no evidence of this design pass in the changelog. Needs scoping, not a bug fix. |
| 2 | Calendar has zero mobile work | Confirmed open — `scripts/calendar.js` has no mobile/responsive handling at all. |

## P3 — genuinely still open (re-verified 2026-08-12)

| # | Gap | Status |
|---|-----|--------|
| 1 | Several manager-only buttons under the 44px tap-target standard | Not independently re-verified (no exact button list in the source audit to check against) — treat as unconfirmed, low urgency. |
| 2 | Teams missing active-state highlight in mobile drawer | Confirmed open — v3.5.469's own changelog explicitly notes it: "ditem-teams still doesn't get this — separate pre-existing gap, not touched here." |

## Lesson

The source OneDrive doc had no version stamp tying it to a specific commit/release, so there was no cheap way to tell "already fixed" from "still open" without reading the actual code. Any future audit-style doc should note the `APP_VERSION` it was checked against, so staleness is detectable at a glance next time.

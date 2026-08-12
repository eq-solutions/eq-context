---
title: Field mobile-experience centering — P1/P2/P3 sprint
owner: Royce Milmlow
created: 2026-08-12
source: C:\Users\EQ\OneDrive - eq-power.com.au\eq-field-mobile-centering.html (audit dated 2026-08-07)
repo: eq-field
scope: Close every mobile gap the 2026-08-07 audit found in EQ Field — 12 P1 fixes, 2 P2 items scoped (not built), 2 P3 items bundled opportunistically. No redesign; every fix makes the app match what it already intends to do.
read_priority: high
status: draft
---

# Field mobile-experience centering

**Status:** backlog — none of the 16 items below have been started. No eq-field code has been touched yet.

Turned from `eq-field-mobile-centering.html` (full six-cluster mobile audit, 2026-08-07) into an executable backlog. File references re-checked live 2026-08-12 against the current `main` (post v3.5.474-482 decomposition of timesheets/apprentices/roster.js) — all still accurate; `apprentices-skills-passport.js` is the new home for the Skills Passport item (it moved out of `apprentices.js` in that decomposition), everything else is unchanged.

Zero real users on Field today — this is the window to fix these without any user-facing disruption risk.

## P1 — ship now (12 items)

All independently scoped, bounded to 1–2 files each. No design decisions required except item 12. Grouped below into suggested PRs by shared file to keep branch/version-bump overhead sane (per eq-field's per-PR deploy-preview convention) — grouping is a suggestion, not a requirement.

| # | Gap | File(s) | Next verifiable outcome |
|---|-----|---------|--------------------------|
| 1 | Bottom-nav clearance CSS bug | `styles/mobile.css` / `styles/base.css` | Trailing content/buttons no longer sit under the nav bar on a 375–480px device |
| 2 | Crew-name overflow — Prestart/Toolbox/Diary/Incident | `scripts/site-reports-shared.js` (shared — re-verify against all 4 callers before merge) | Long crew name ellipsises instead of overflowing, on all four forms |
| 3 | Prestart crash-recovery draft loss | Prestart form script | Evicted tab mid-prestart restores the draft on return, not a blank form |
| 4 | Incident modal height, Shell-embedded mode | Incident form script | Save/Submit reachable on Incident the same as the other 3 safety forms |
| 5 | Sign Documents: missing mobile-style call + unguarded popup | `scripts/sign-documents.js` | Signature pad matches sibling forms' size; View can't be silently popup-blocked |
| 6 | Apprentices Skills Passport — dead CSS selector | `scripts/apprentices-skills-passport.js` (moved here in v3.5.481 decomposition — was `apprentices.js`) | Table actually shrinks on a phone instead of relying on horizontal scroll |
| 7 | Calibration + Projects unreachable on mobile | `index.html` mobile drawer wiring | Both reachable via the mobile drawer, same as every other page |
| 8 | Roster Overview map — no mobile hide | `scripts/roster.js` | Same guard Dashboard's identical map already has |
| 9 | Edit Roster undo/redo unreachable on mobile | `scripts/roster.js` / `scripts/roster-undo.js` | Undo/redo reachable by tap, not just a desktop keyboard shortcut |
| 10 | Timesheets Job Numbers panel — fixed 260px sidebar | `scripts/timesheets.js` | Panel adapts at phone width instead of eating most of the screen |
| 11 | Leave balance cards squeeze at phone width | `scripts/leave.js` | Same fix the supervisor stat-row already got, applied to the worker view |
| 12 | Safety Records — no role gate in code | TBD — pending Royce's decision | **Blocked on Royce**: decide intended access first, then implement whichever way |

**Suggested PR batching:** #1+#7 (index.html/CSS, drawer + nav), #2 (shared safety-form component, needs the extra caller re-verification called out in kill criteria), #3+#4 (safety forms), #5, #6, #8+#9 (roster.js), #10, #11, #12 (once Royce decides).

## P2 — scoped, not built (design pass, next after P1)

| # | Gap | Why it waits |
|---|-----|--------------|
| 1 | Safety forms, Timesheets, Leave never got a Home-style per-role split | This is the real "100/100 moments" delivery — needs a design pass (staff vs. supervisor view), not a CSS fix. Scope after P1 lands. |
| 2 | Calendar has zero mobile work | Needs a card/agenda fallback for the month grid + a mobile-sized day panel — a small design decision, not a bug fix. |

## P3 — bundle opportunistically (no standalone PR)

| # | Gap | Bundle into |
|---|-----|-------------|
| 1 | Several manager-only buttons under the 44px tap-target standard | Whichever P1 PR already touches that file |
| 2 | Teams missing active-state highlight in mobile drawer | The #1+#7 drawer/nav PR above |

## Kill criteria (carried from the source audit)

- Any fix touching a component shared across 4+ forms (item 2) gets independently re-verified against every caller before merge — this exact bug class has already been lost once to an unreviewed shared-file change.
- Item 12 (Safety Records) does not ship without Royce's explicit call on intended scope.
- If a "small" fix turns out to need a real layout decision, it stops and moves to the P2 pass instead of being rushed.

## Sequencing note

Item 6 already needed a live-file check because `apprentices.js` was decomposed the day before this audit (v3.5.474-482, 2026-08-11) — its Skills Passport code now lives in `apprentices-skills-passport.js`. Re-check file locations again before starting if more decomposition/refactor PRs land between now and execution.

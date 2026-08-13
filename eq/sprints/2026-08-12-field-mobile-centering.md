---
title: Field mobile-experience centering — P1/P2/P3 sprint
owner: Royce Milmlow
last_updated: 2026-08-13
created: 2026-08-12
source: C:\Users\EQ\OneDrive - eq-power.com.au\eq-field-mobile-centering.html (audit dated 2026-08-07)
repo: eq-field
scope: Originally 12 P1 + 2 P2 + 2 P3 items from a 2026-08-07 mobile audit. Corrected same-day, 2026-08-12, after live verification found all 12 P1 items already shipped, and again after live-code checks found Leave's supervisor view already built. Every item resolved same day: Safety+Leave (v3.5.484, PR #680, merged/live), Calendar agenda view (v3.5.485, PR #681, merged/live), P3 sweep — Teams highlight + mic tap targets (v3.5.486, PR #682, deploy-preview verified, awaiting merge).
read_priority: high
status: draft
---

# Field mobile-experience centering

**Status:** Every item resolved same day (2026-08-12) — 12 already shipped (no build needed), 3 real gaps built and verified (v3.5.484/485 merged and live; v3.5.486 built and deploy-preview verified, PR #682 open awaiting Royce's merge call), 1 correctly declined (photo-remove badge, would have been a visual regression).

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

**Merged and live in production** (2026-08-12, confirmed via `curl field.eq.solutions/sw.js` showing v3.5.484).

### Timesheets — explicitly deferred

Royce's call, 2026-08-12: mobile timesheets isn't a priority right now. Revisit only if there's a reason to believe people are actually trying to do timesheets on their phone.

## What actually happened (Calendar)

Premise held up this time — `scripts/calendar.js` genuinely had zero mobile handling. Built: an agenda list (one row per weekday: date + site/leave summary) shown below 768px instead of the 7-column grid, using the same desktop/mobile toggle pattern Roster and Job Numbers already use. Tapping a row opens the existing day-detail panel, now converted to a bottom-sheet on mobile (same pattern already used for Timesheets' Job Numbers panel) instead of the 312px side-flyout that wouldn't fit a phone.

**Shipped, v3.5.485, PR #681:**
- Verified directly on the deploy preview at 375px: desktop grid hidden, agenda list shown with correct per-day data; tapping a row opens the bottom sheet (confirmed `position:fixed`, full width, correct open/close state); closing works. Re-checked at 1280px: agenda hidden, grid shown, day-detail panel unaffected by the mobile CSS (`position:static`, not `fixed`) — desktop untouched.
- No new console errors (only the same pre-existing, documented standalone-demo-gate 401s).

Awaiting Royce: merge PR #681. This closes out the last scoped P2 item.

## What actually happened (P3)

Closed as its own small pass, 2026-08-12, at Royce's request — didn't wait for an unrelated PR to bundle into.

- **Teams drawer highlight** — confirmed the exact cause: `DRAWER_NAV_PAGES` (index.html) drives every drawer item's active-page highlight; Teams was the one entry never added when `ditem-teams` shipped (v3.5.27). Added it — reuses the existing mechanism, no new CSS.
- **Manager-only buttons under 44px** — the source wording named no specific buttons, so grepped every small inline button pattern across `scripts/*.js` (14 hits) and checked each: excluded decorative avatars (not tap targets), excluded Roster's Team Week nav buttons (its own comment says "for staff," not manager-only — would've been a false positive), excluded every Timesheets instance per Royce's stated priority this session even though one (`.eq-apq-btn`) is a legitimate same-class bug already fixed in Leave. Landed on 2 real instances: the voice-dictation mic button on Prestart/Toolbox/Diary/Incident and on Site Audits (both 34px, both genuinely gated to `isManager`/`reports.*.create`). Bumped both to 44px.
- **Declined, not missed:** the photo-remove badge on the same 4 safety forms is also under 44px and also manager-only — but it's 20px sitting on an 84px thumbnail corner; forcing it to 44px would make the button bigger than half the photo. Named and left alone rather than rushed — matches this sprint's own kill criteria ("if a small fix needs a real layout decision, it stops").

**Shipped, v3.5.486, PR #682:** verified directly on the deploy preview — Teams drawer item computed `.active-page` (navy, bold) after navigating there; both mic-button locations (Prestart form: 4 buttons, Site Audits form: several) computed 44×44px; no new console errors. Not yet merged.

## Lessons

1. The source OneDrive doc had no version stamp tying it to a specific commit/release — no cheap way to tell "already fixed" from "still open" without reading the actual code. Any future audit-style doc should note the `APP_VERSION` it was checked against.
2. Same lesson, twice in one sprint: a planning doc's *design* assumptions (not just its bug list) can also be stale. "Leave needs a supervisor view built" and "Safety needs a worker/supervisor split" were both wrong once the actual permission model and existing code were checked. Verify the code, not just the symptom list, before scoping a build.
3. "Bundle into a future PR" backlog items are easy to lose. Closing P3 as its own small, deliberate pass (rather than waiting indefinitely for an unrelated PR to ride along on) got 2 confirmed-real gaps fixed same-day instead of never.

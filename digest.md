---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-31
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-31 22:49 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-31 22:37 UTC → 2026-07-31 22:49 UTC)

- Merged: eq-shell [#1147](https://github.com/eq-solutions/eq-shell/pull/1147) docs: flag the function-grant landmine behind EQ-CARDS-1C
- Merged: eq-shell [#1138](https://github.com/eq-solutions/eq-shell/pull/1138) feat(intake): tenant-editable trades vocab + persisted dupli
- Merged: eq-shell [#1137](https://github.com/eq-solutions/eq-shell/pull/1137) fix(intake): site-merge manager gate checked the wrong ident
- Merged: eq-shell [#1135](https://github.com/eq-solutions/eq-shell/pull/1135) perf(shell): warm token-exchange to close the last cold-star
- Merged: eq-shell [#1133](https://github.com/eq-solutions/eq-shell/pull/1133) fix(mobile): drop redundant top bar on adapted iframe module
- Merged: eq-shell [#1130](https://github.com/eq-solutions/eq-shell/pull/1130) chore(intake): re-vendor eq-intake/eq-platform — merge-error
- Merged: eq-shell [#1129](https://github.com/eq-solutions/eq-shell/pull/1129) fix(audit): Suite Activity gets real filtering; correct EQ Q
- Merged: eq-shell [#1127](https://github.com/eq-solutions/eq-shell/pull/1127) chore(intake): re-vendor eq-intake/eq-platform — Tidy tab en

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-cards` [minified:w8: PostgrestException(message: permission denied f](https://eq-solutions.sentry.io/issues/137739023/)

## 🙋 Waiting on you (107)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to confirm EQ-CARDS-1C stops recurring** over the next 24h now the grant is restored. _(added 2026-07-31)_
- **EQ** · **"Your access changed, sign in again" nudge — deliberately not built.** Came up exploring the next-login-only role-change design; real gap (a promoted user has no signal their view is stale) but needs Royce to pick a delivery mechanism (banner / forced re-auth / email) before any code gets written. _(added 2026-07-31)_
- **EQ** · **Royce to confirm on Richard's own phone**: the page loads without the error screen, the bottom bar shows Home + Field only, and Service/Ops are reachable via the account menu. _(added 2026-07-31)_
- **EQ** · **Royce to click through the new paste-import resolve screen live** — built and type/build-checked clean, but not clicked through in a real browser session (no test login available in this environment). Paste a batch with an unmatched asset ID, try linking one and creating another, confirm the resulting check comes out right. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** — trigger a failed-then-fixed site merge and confirm it now works; open the Contacts/Staff Dupes tab, archive one flagged duplicate and dismiss another as "not a duplicate," confirm both stick; add a trade in the new Trades screen and confirm it shows up in the Review Queue's trade picker. Needs sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live**: change a quote's status through each of the 5 stages and confirm the job record follows each time; set a Target period on a quote and confirm the badge shows correctly in both the detail panel and the board view. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** — trigger a failed site merge in the Duplicate Sites panel and confirm the error now shows; open the Remediation Queue, find a duplicate flag, click Archive, confirm the record goes inactive and drops off the list. Claude can't do this step itself — it requires signing in, which falls under the hard rule against entering credentials on the user's behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** on a mobile-width view (~375px or a phone): open Field/Service and confirm the top bar is gone (just the bottom tab bar); open Ops/Comms and confirm nothing changed; from Field/Service, tap Home and confirm Settings/2FA/Sign-out are still reachable there. Note: a related eq-field fix landed 2026-07-31 (v3.5.388) for a home-label clipping issue caught on the same phone-screenshot pass — worth confirming both together. _(added 2026-07-31)_
- **EQ** · **Royce to confirm live**: once the deploy lands on core.eq.solutions, reload the dashboard and confirm Huon Henne no longer appears under "Licences expiring" on the Compliance & safety card. _(added 2026-07-30)_
- **EQ** · **Moahmmed Elsayed's `photo_id`-typed licence row (number `0140988080`) not yet corrected** — unlike Maylin Ung's case (a driver's-licence-format number, fixed directly), this number doesn't match a recognisable pattern; needs Royce to confirm the actual document type before the DB row is corrected. _(added 2026-07-29)_
- **EQ** · **Royce to click through live**: invite a labour-hire worker with the box unchecked, confirm they land on a Field-free home screen and can't reach Field directly; then invite/sign in a normal worker (box left checked) and confirm nothing changed for them. Bundled with the three click-through items below into one live-testing pass — see that section's deferred note. _(added 2026-07-30)_
- **EQ** · **Royce to click through live, all four features shipped today together** (this section's three plus the compliance-roster-only switch above): invite/adjust a worker with Field access off; correct a test worker's phone number and confirm their old passcode stops working while a fresh sign-in + new passcode works; check the passcode-status view and try "Unlock now" on a locked test account; sign in as a phone-only worker and confirm the backup-email reminder shows, dismisses for that sign-in only, and clears once an email is added. None of this has been clicked through live yet — Claude can't perform this step directly (logging in requires entering a passcode, which falls under a hard rule against entering credentials on the user's behalf, even for the user's own product). _(added 2026-07-30)_
_…and 95 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 2 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 12 | 2026-07-31 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-cards | [minified:w8: PostgrestException(message: permission denied for function eq_cards](https://eq-solutions.sentry.io/issues/137739023/) | 8 | 2026-07-31 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 6 | 2026-07-30 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 5 | 2026-07-31 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 4 | 2026-07-23 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-31 | eq-shell | [#1147](https://github.com/eq-solutions/eq-shell/pull/1147) docs: flag the function-grant landmine behind EQ-CARDS-1C |
| 2026-07-31 | eq-shell | [#1146](https://github.com/eq-solutions/eq-shell/pull/1146) feat(mobile): simplified 2-tab nav for supervisors/managers, desk |
| 2026-07-31 | eq-solves-service | [#661](https://github.com/eq-solutions/eq-service/pull/661) feat(reports): wire site photo into PM Check Report cover |
| 2026-07-31 | eq-solves-service | [#660](https://github.com/eq-solutions/eq-service/pull/660) feat(maintenance): link/create/skip reconcile for paste-import un |
| 2026-07-31 | eq-solves-service | [#659](https://github.com/eq-solutions/eq-service/pull/659) fix(storage): add missing tenant write policy on logos bucket |
| 2026-07-31 | eq-field | [#586](https://github.com/eq-solutions/eq-field/pull/586) fix: mobile drawer - relabel "Safety" to "Site Audits", move belo |
| 2026-07-31 | eq-field | [#585](https://github.com/eq-solutions/eq-field/pull/585) fix: mobile drawer had no path to Toolboxes/Prestarts/Records/Inc |
| 2026-07-31 | eq-field | [#584](https://github.com/eq-solutions/eq-field/pull/584) fix: photo picker forced the camera, blocking gallery uploads (v3 |
| 2026-07-31 | eq-field | [#583](https://github.com/eq-solutions/eq-field/pull/583) v3.5.390 — Fix: weekly digest opt-in panel silently stopped appea |
| 2026-07-31 | eq-cards | [#191](https://github.com/eq-solutions/eq-cards/pull/191) fix(auth): restore authenticated EXECUTE grant on eq_cards_auto_p |
| 2026-07-30 | eq-shell | [#1144](https://github.com/eq-solutions/eq-shell/pull/1144) feat(mobile): My Card row in the account sheet for non-field-firs |
| 2026-07-30 | eq-shell | [#1141](https://github.com/eq-solutions/eq-shell/pull/1141) perf(shell): fetchpriority=low on prewarmed iframes + pause prewa |
| 2026-07-30 | eq-shell | [#1139](https://github.com/eq-solutions/eq-shell/pull/1139) perf(shell): preconnect to Field/Service/Cards origins ahead of i |
| 2026-07-30 | eq-shell | [#1142](https://github.com/eq-solutions/eq-shell/pull/1142) chore(intake): re-vendor eq-intake/eq-platform — trades settings  |
| 2026-07-30 | eq-shell | [#1143](https://github.com/eq-solutions/eq-shell/pull/1143) fix(auth): null-safe display name for phone-only workers |
_Showing 15 of 126 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **`mint-cards-otp` returned 500 once** for a real sks supervisor on mobile (Sentry EQ-SHELL-13) — single occurrence so far, watch for a repeat before digging further. _(added 2026-07-31)_
- **eq-field: duplicate script declaration** (Sentry EQ-FIELD-W, `SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared`) — likely a symptom of the already-known "34 always-loaded boot scripts" architecture debt logged elsewhere in this file; not investigated further this session. _(added 2026-07-31)_
- **Security Group scenario (#1109 test-plan box 3) untestable until a real assignment exists** — offered to help set up a test case if Royce wants this actually exercised rather than left as a code-correctness-only claim. _(added 2026-07-31)_
- **Live phone click-through not done** — open the More drawer, unlock manager mode, confirm Toolboxes/Prestarts/Incidents/Records/Site Audits each land on the right page in the new order. _(added 2026-07-31)_
- **Live phone click-through not done** — camera vs. gallery picker on a real device. _(added 2026-07-31)_
- **Richard then reported he couldn't find Service after the above shipped** — checked live: he has full permission and his company's account has Service switched on, so nothing needs granting. This is the expected result of the new simplified mobile view — Service moved from the main bar into the account menu. Told Royce where to find it; open question whether supervisors need Service as a main tab after all if this keeps coming up, rather than one tap deeper. _(added 2026-07-31)_
- **iPads get the full desktop view, not the simplified mobile one** — confirmed the phone/desktop cutoff is a fixed screen-width line that iPads sit above in both orientations, so nothing built this session changes what an iPad shows. Noted in case a tablet-specific view is ever wanted. _(added 2026-07-31)_
- **Site photos only show up on two of the eight report types** (the ACB Test Report and the Customer/PM Asset Report) — the other report types (including the PM Check Report, by far the most-used one) don't pull in a site photo at all. Flagged to Royce, not yet requested as a fix. _(added 2026-07-31)_
- **Two other places still lack any resolve option for unmatched rows**: the maintenance-check screen's own quick work-order paste (the simplest, position-only version) and the plain Assets spreadsheet import. Out of scope this round — same treatment could be added later if wanted. _(added 2026-07-31)_
- **Do not merge/deploy PR #1145 on its own** — once live, a brand-new self-join account will be permanently unable to reach Field (not just delayed) because nothing yet exists to flip the switch back on. That "flip it back on" piece (below) has to ship in the same breath, or self-join effectively loses Field access entirely. _(added 2026-07-31)_
_…and 358 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
_…and 66 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2952 | 480 | 84 | 12 |
| [SKS](sks/pending.md) | 425 | 84 | 3 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 430 | 39 | 5 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-31 | [Quote events now stamp app_source='ops' instead of the retired app name (continuation of 2026-07-30)](sessions/2026-07-31.md) |
| 2026-07-30 | [`__personal__` tenant "retired" doc claim corrected against live data](sessions/2026-07-30.md) |
| 2026-07-30 | [guard.js selftest fixed; ~/.claude brought under version control](sessions/2026-07-30-guard-selftest-claude-git.md) |
| 2026-07-29 | [eq-receipts: fixed a duplicate-detection blind spot, added invoice number as a stronger match](sessions/2026-07-29.md) |
| 2026-07-28 | [Roster: archive Labour Hire from the grid with a rehire rating](sessions/2026-07-28.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-31 22:49 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-31
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-31 08:06 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-31 04:10 UTC → 2026-07-31 08:06 UTC)

- Merged: eq-shell [#1132](https://github.com/eq-solutions/eq-shell/pull/1132) fix(audit): quote events now stamp app_source='ops', not the
- Merged: eq-shell [#1131](https://github.com/eq-solutions/eq-shell/pull/1131) fix(signals): exclude archived staff from Compliance & safet
- Merged: eq-shell [#1128](https://github.com/eq-solutions/eq-shell/pull/1128) fix(audit): stop entity.patched canonical_events noise
- Merged: eq-shell [#1126](https://github.com/eq-solutions/eq-shell/pull/1126) feat(audit): Suite activity tab — canonical_events as plain 
- Merged: eq-shell [#1123](https://github.com/eq-solutions/eq-shell/pull/1123) fix(audit): fn_audit() noise guard, take 2 — 0225's WHEN cla
- Merged: eq-shell [#1121](https://github.com/eq-solutions/eq-shell/pull/1121) fix(audit): stop logging no-op UPDATEs polluting the Activit
- Merged: eq-shell [#1120](https://github.com/eq-solutions/eq-shell/pull/1120) fix(suppliers): free scroll + column toggle; drop BETA from 
- Merged: eq-shell [#1117](https://github.com/eq-solutions/eq-shell/pull/1117) fix(briefing): exclude archived staff from the AI dashboard 

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F6: Append (>>) NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-07-31.md](sessions/2026-07-31.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F7: git merge/stash-pop round-trip NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-07-31.md](sessions/2026-07-31.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (102)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to click through live** — trigger a failed-then-fixed site merge and confirm it now works; open the Contacts/Staff Dupes tab, archive one flagged duplicate and dismiss another as "not a duplicate," confirm both stick; add a trade in the new Trades screen and confirm it shows up in the Review Queue's trade picker. Needs sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live**: change a quote's status through each of the 5 stages and confirm the job record follows each time; set a Target period on a quote and confirm the badge shows correctly in both the detail panel and the board view. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** — trigger a failed site merge in the Duplicate Sites panel and confirm the error now shows; open the Remediation Queue, find a duplicate flag, click Archive, confirm the record goes inactive and drops off the list. Claude can't do this step itself — it requires signing in, which falls under the hard rule against entering credentials on the user's behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** on a mobile-width view (~375px or a phone): open Field/Service and confirm the top bar is gone (just the bottom tab bar); open Ops/Comms and confirm nothing changed; from Field/Service, tap Home and confirm Settings/2FA/Sign-out are still reachable there. Note: a related eq-field fix landed 2026-07-31 (v3.5.388) for a home-label clipping issue caught on the same phone-screenshot pass — worth confirming both together. _(added 2026-07-31)_
- **EQ** · **Royce to confirm live**: once the deploy lands on core.eq.solutions, reload the dashboard and confirm Huon Henne no longer appears under "Licences expiring" on the Compliance & safety card. _(added 2026-07-30)_
- **EQ** · **Moahmmed Elsayed's `photo_id`-typed licence row (number `0140988080`) not yet corrected** — unlike Maylin Ung's case (a driver's-licence-format number, fixed directly), this number doesn't match a recognisable pattern; needs Royce to confirm the actual document type before the DB row is corrected. _(added 2026-07-29)_
- **EQ** · **Royce to click through live**: invite a labour-hire worker with the box unchecked, confirm they land on a Field-free home screen and can't reach Field directly; then invite/sign in a normal worker (box left checked) and confirm nothing changed for them. Bundled with the three click-through items below into one live-testing pass — see that section's deferred note. _(added 2026-07-30)_
- **EQ** · **Royce to click through live, all four features shipped today together** (this section's three plus the compliance-roster-only switch above): invite/adjust a worker with Field access off; correct a test worker's phone number and confirm their old passcode stops working while a fresh sign-in + new passcode works; check the passcode-status view and try "Unlock now" on a locked test account; sign in as a phone-only worker and confirm the backup-email reminder shows, dismisses for that sign-in only, and clears once an email is added. None of this has been clicked through live yet — Claude can't perform this step directly (logging in requires entering a passcode, which falls under a hard rule against entering credentials on the user's behalf, even for the user's own product). _(added 2026-07-30)_
- **EQ** · **Royce to click through live**: open a job's detail view, the create-quote form, the kanban board, and each Reports tab, confirm ex-GST reads as the main figure everywhere it should. Verified via build + typecheck only, not yet clicked through live. _(added 2026-07-30)_
- **EQ** · **Royce to re-review Bruno Vita Pedrosa, Luke Wheeler, and Mohamed Ahmed** — their current flags trace to the confirmed false-positive batch touches; reviewing them now (post-#1101) records a real fingerprint so they won't be falsely re-flagged again. _(added 2026-07-29)_
- **EQ** · **Royce to clear Brave's site data for cards.eq.solutions on his own phone** — the actual reported symptom (an old email-login screen). A Flutter service worker registered on that device before the phone-OTP flip is still serving its own cached copy of the old build; production itself is correctly configured (verified live). A full close + clear-site-data + reopen forces the fresh navigation the browser's update check needs. _(added 2026-07-29)_
- **EQ** · **Royce to reconcile a customer CSV with a messy phone number/ABN and confirm it now gets cleaned up** — verified in code + typecheck, not yet clicked through live. _(added 2026-07-29)_
_…and 90 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 11 | 2026-07-30 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 6 | 2026-07-30 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 4 | 2026-07-30 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 4 | 2026-07-23 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
| eq-field | [ReferenceError: openTafeHolidaysConfig is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 3 | 2026-07-28 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-31 | eq-shell | [#1146](https://github.com/eq-solutions/eq-shell/pull/1146) feat(mobile): simplified 2-tab nav for supervisors/managers, desk |
| 2026-07-31 | eq-solves-service | [#660](https://github.com/eq-solutions/eq-service/pull/660) feat(maintenance): link/create/skip reconcile for paste-import un |
| 2026-07-31 | eq-solves-service | [#659](https://github.com/eq-solutions/eq-service/pull/659) fix(storage): add missing tenant write policy on logos bucket |
| 2026-07-31 | eq-field | [#583](https://github.com/eq-solutions/eq-field/pull/583) v3.5.390 — Fix: weekly digest opt-in panel silently stopped appea |
| 2026-07-30 | eq-shell | [#1144](https://github.com/eq-solutions/eq-shell/pull/1144) feat(mobile): My Card row in the account sheet for non-field-firs |
| 2026-07-30 | eq-shell | [#1141](https://github.com/eq-solutions/eq-shell/pull/1141) perf(shell): fetchpriority=low on prewarmed iframes + pause prewa |
| 2026-07-30 | eq-shell | [#1139](https://github.com/eq-solutions/eq-shell/pull/1139) perf(shell): preconnect to Field/Service/Cards origins ahead of i |
| 2026-07-30 | eq-shell | [#1142](https://github.com/eq-solutions/eq-shell/pull/1142) chore(intake): re-vendor eq-intake/eq-platform — trades settings  |
| 2026-07-30 | eq-shell | [#1143](https://github.com/eq-solutions/eq-shell/pull/1143) fix(auth): null-safe display name for phone-only workers |
| 2026-07-30 | eq-shell | [#1140](https://github.com/eq-solutions/eq-shell/pull/1140) chore(intake): re-vendor eq-intake/eq-platform — Dupes archive +  |
| 2026-07-30 | eq-shell | [#1138](https://github.com/eq-solutions/eq-shell/pull/1138) feat(intake): tenant-editable trades vocab + persisted duplicate  |
| 2026-07-30 | eq-shell | [#1136](https://github.com/eq-solutions/eq-shell/pull/1136) fix(quotes): sync canonical job status for every pipeline stage |
| 2026-07-30 | eq-shell | [#1137](https://github.com/eq-solutions/eq-shell/pull/1137) fix(intake): site-merge manager gate checked the wrong identity s |
| 2026-07-30 | eq-shell | [#1135](https://github.com/eq-solutions/eq-shell/pull/1135) perf(shell): warm token-exchange to close the last cold-start gap |
| 2026-07-30 | eq-shell | [#1134](https://github.com/eq-solutions/eq-shell/pull/1134) fix(audit): workers-canonical-sync attributes real actors |
_Showing 15 of 125 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Two separate sessions independently claimed the same migration number (0228)** tonight — this one and the quote-target-period entry above. Not a live problem (both applied cleanly, nothing broke), but worth knowing the "check origin/main before claiming a number" step isn't fully collision-proof under concurrent sessions. _(added 2026-07-31)_
- **Long "Open" list / no drag-and-drop from the bottom** — Royce flagged the Open column is getting hard to manage as it grows. Discussed as ideas only (lean on the existing board view, add sort/filter to the flat list) — not approved for build yet. _(added 2026-07-31)_
- **Edge function redeploy** — the PR body says it needs `deploy_edge_function` to jvkn after merge; not git-triggered, so the fix isn't live in the running function until that manual step happens. Not confirmed done. _(added 2026-07-31)_
- **Live verification unchecked in the PR's own test plan** — admin edit → admin attributed, self-edit → worker attributed, reconcile → no actor. None confirmed yet. _(added 2026-07-31)_
- Nobody's confirmed the `eq` tenant's Job Numbers nav placement or mobile Pipeline hiding on a live click-through — same "not yet clicked through production" gap noted in the SKS entry. _(added 2026-07-31)_
- **`EQ_SECRET_SALT` rotation still outstanding** — the value was exposed in chat back in April; nothing has forced a rotation since. _(added 2026-07-30)_
- **Zemi Asri's email in core is still the old value** (`zemi.asri@sks.com.au`) — the fix stops this happening to the next worker, it doesn't correct his row. Either have him re-enter his email in Cards now (will take, unlocked), or edit it directly on his Shell Staff page. _(added 2026-07-30)_
- No edit screen yet for switching an *existing* worker's Field access on/off after the fact — today it's invite-time only. _(added 2026-07-30)_
- **The ACB Test Report has been verified correct by code symmetry with the NSX path, not against a real ACB check** — there are currently zero completed ACB checks in the live database to test against. Worth a quick look the first time SKS actually completes one. _(added 2026-07-29)_
- **First real "August PM"-style import: the "BTCHGR" job plan code on Royce's file doesn't match any existing SKS job plan exactly** (closest is "24VBTCHGR") — the import wizard's existing fuzzy-match step will prompt to confirm or nominate a plan the first time this file type is actually committed. Not a bug, just a heads-up for whoever runs the first real import. _(added 2026-07-29)_
_…and 343 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
_…and 64 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2874 | 462 | 90 | 12 |
| [SKS](sks/pending.md) | 411 | 81 | 0 | 16 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-31 08:06 UTC._

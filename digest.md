---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-30 08:00 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-30 07:57 UTC → 2026-07-30 08:00 UTC)

- Merged: eq-shell [#1100](https://github.com/eq-solutions/eq-shell/pull/1100) fix(suppliers): show all columns by default now that fullWid
- Merged: eq-shell [#1098](https://github.com/eq-solutions/eq-shell/pull/1098) fix(suppliers): hide Notes/Login/Password by default, same i
- Merged: eq-shell [#1096](https://github.com/eq-solutions/eq-shell/pull/1096) fix(suppliers): scroll the table on its own card, not trunca
- Merged: eq-shell [#1095](https://github.com/eq-solutions/eq-shell/pull/1095) fix(suppliers): retune every column width to a coherent budg
- Merged: eq-shell [#1091](https://github.com/eq-solutions/eq-shell/pull/1091) fix(licences): stop the Cards resync from bumping updated_at
- Merged: eq-shell [#1089](https://github.com/eq-solutions/eq-shell/pull/1089) fix(home): apprentices land on WorkerHome, not the manager d
- Merged: eq-shell [#1088](https://github.com/eq-solutions/eq-shell/pull/1088) fix(intake): route the Health-console commit through intake-
- Merged: eq-shell [#1087](https://github.com/eq-solutions/eq-shell/pull/1087) fix(cards): spinner on compliance-pack progress label

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F6: Append (>>) NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-07-28.md](sessions/2026-07-28.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (95)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to click through live**: invite a labour-hire worker with the box unchecked, confirm they land on a Field-free home screen and can't reach Field directly; then invite/sign in a normal worker (box left checked) and confirm nothing changed for them. _(added 2026-07-30)_
- **EQ** · **Royce to click through live**: open a job's detail view, the create-quote form, the kanban board, and each Reports tab, confirm ex-GST reads as the main figure everywhere it should. Verified via build + typecheck only, not yet clicked through live. _(added 2026-07-30)_
- **EQ** · **Royce to click through `/sks/intake` live** — confirm Overview/To Do/Bring Data In/Ask all render as expected. Not click-tested live this session — the deploy preview is login-gated and no production session was available in this environment; verified via full build + 270/270 tests + code review only. _(added 2026-07-29)_
- **EQ** · **Royce to clear Brave's site data for cards.eq.solutions on his own phone** — the actual reported symptom (an old email-login screen). A Flutter service worker registered on that device before the phone-OTP flip is still serving its own cached copy of the old build; production itself is correctly configured (verified live). A full close + clear-site-data + reopen forces the fresh navigation the browser's update check needs. _(added 2026-07-29)_
- **EQ** · **Royce to reconcile a customer CSV with a messy phone number/ABN and confirm it now gets cleaned up** — verified in code + typecheck, not yet clicked through live. _(added 2026-07-29)_
- **EQ** · **Royce to click through the Import screen (`/intake`) on core.eq.solutions once the deploy lands** — confirm it still loads and still commits normally. That screen wasn't touched, but worth a look since it's the app's only working import path now. _(added 2026-07-29)_
- **EQ** · **Royce to click through Assets/Job Plans/Maintenance Checks once the deploy lands** — confirm the Export button's new dropdown offers CSV and Excel, both download the full list, and the Maintenance Checks "tasks completed" count now shows a real number instead of "/0". Not click-tested live this session — no login credentials available in this environment, verified via type-checking + the full automated test suite + code review only. _(added 2026-07-29)_
- **EQ** · **Royce to confirm live**: edit an already-reviewed licence's expiry/number in Cards for an approved worker, confirm the Staff page badge flips to "changed since — re-review needed" without a hard refresh. _(added 2026-07-28)_
- **EQ** · **Royce to click through live**: open Suppliers and confirm all 8 columns show by default with no scrolling needed — the page now uses `fullWidth` (the real fix; the page had been stuck inside an 860px reading-width cap the whole time) instead of scroll/pagination/column-hiding workarounds. _(added 2026-07-29)_
- **EQ** · **Royce to confirm live**: reload the Wallet and confirm the Photo ID nag no longer shows for a worker who holds a Driver Licence or Passport. _(added 2026-07-28)_
- **EQ** · **Separate, lower-priority finding: 53 of 88 active SKS staff have a Cards worker link but zero credentials captured in Cards at all** (checked the pre-promotion `worker_credentials` table too — genuinely empty, not stuck mid-migration). Only 34 of 88 active staff have any licence data flowing through Shell. This is a Cards onboarding-completion gap, not a sync bug — no action taken, logging only per Royce's call. _(added 2026-07-28)_
- **EQ** · **Royce to click through the real flow once the deploy lands**: set up two-step verification, save the codes shown, sign out, sign back in using one of the backup codes instead of the phone app, then generate a fresh set from Settings and confirm the old ones stop working. _(added 2026-07-28)_
_…and 83 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 1 | 0d |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 10 | 2026-07-29 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 5 | 2026-07-23 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 3 | 2026-07-29 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
| eq-field | [ReferenceError: openTafeHolidaysConfig is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 3 | 2026-07-28 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 2 | 2026-07-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-30 | eq-shell | [#1113](https://github.com/eq-solutions/eq-shell/pull/1113) chore(intake): re-vendor eq-intake/eq-platform — customers/contac |
| 2026-07-30 | eq-shell | [#1116](https://github.com/eq-solutions/eq-shell/pull/1116) feat(workers): compliance-roster-only workers — has_field_access  |
| 2026-07-30 | eq-shell | [#1114](https://github.com/eq-solutions/eq-shell/pull/1114) chore: remove dead intake domain pages and SecurityGroupsPage shi |
| 2026-07-30 | eq-shell | [#1115](https://github.com/eq-solutions/eq-shell/pull/1115) fix(migrations): enable RLS on tenant_field_importance_overrides |
| 2026-07-30 | eq-solves-service | [#648](https://github.com/eq-solutions/eq-service/pull/648) fix(maintenance): sort Assigned To dropdown A-Z instead of by rol |
| 2026-07-30 | eq-cards | [#187](https://github.com/eq-solutions/eq-cards/pull/187) chore(licences): codify Photo ID + Passport as tracked licence ty |
| 2026-07-29 | eq-shell | [#1112](https://github.com/eq-solutions/eq-shell/pull/1112) fix(staff): full-size licence photo lightbox |
| 2026-07-29 | eq-shell | [#1111](https://github.com/eq-solutions/eq-shell/pull/1111) feat(ops): make ex-GST the prominent figure across EQ Ops |
| 2026-07-29 | eq-shell | [#1110](https://github.com/eq-solutions/eq-shell/pull/1110) feat(auth): phone+PIN login door, generalized grace-gate pattern |
| 2026-07-29 | eq-shell | [#1109](https://github.com/eq-solutions/eq-shell/pull/1109) fix(mobile): mirror desktop's permission checks (Security Groups  |
| 2026-07-29 | eq-shell | [#1107](https://github.com/eq-solutions/eq-shell/pull/1107) fix(observability): stop mislabeling network errors as stale-chun |
| 2026-07-29 | eq-shell | [#1106](https://github.com/eq-solutions/eq-shell/pull/1106) chore(intake): re-vendor eq-intake/eq-platform — field-importance |
| 2026-07-29 | eq-shell | [#1105](https://github.com/eq-solutions/eq-shell/pull/1105) fix(auth): register /login route so ?tenant= survives to LoginPag |
| 2026-07-29 | eq-shell | [#1104](https://github.com/eq-solutions/eq-shell/pull/1104) feat(intake): tenant-editable field-importance override table + R |
| 2026-07-29 | eq-shell | [#1103](https://github.com/eq-solutions/eq-shell/pull/1103) fix(invite): route phone-first worker activation through Shell, n |
_Showing 15 of 116 · full record in [sessions/](sessions/)_

## Pending (EQ)

- No edit screen yet for switching an *existing* worker's Field access on/off after the fact — today it's invite-time only. _(added 2026-07-30)_
- **The ACB Test Report has been verified correct by code symmetry with the NSX path, not against a real ACB check** — there are currently zero completed ACB checks in the live database to test against. Worth a quick look the first time SKS actually completes one. _(added 2026-07-29)_
- **First real "August PM"-style import: the "BTCHGR" job plan code on Royce's file doesn't match any existing SKS job plan exactly** (closest is "24VBTCHGR") — the import wizard's existing fuzzy-match step will prompt to confirm or nominate a plan the first time this file type is actually committed. Not a bug, just a heads-up for whoever runs the first real import. _(added 2026-07-29)_
- **ACB/NSX breaker-card run-sheets and RCD test run-sheets don't show the Job Code** — Royce chose to scope this session to the standard maintenance checklist only; same gap exists in those report variants if wanted later. _(added 2026-07-29)_
- **Two other report types have the same missing-Job-Code gap**: the PM asset report and the work-order-details report already fetch/track job plan info per asset but only surface the plan *name*, never the *code*. Not touched this session — out of scope. _(added 2026-07-29)_
- **Bring Data In's "Check for conflicts" still commits on its own path, separate from the main Into-EQ flow** — routing those resolved rows into the same shared commit path as everything else is real, separate work, not done here. _(added 2026-07-29)_
- **The deeper "why is this still exhausting" fixes are still open** — bulk-approve (today it's still one row at a time), standing rules for recurring conflict types (so the same duplicate doesn't get flagged forever), a trend view (is the score improving?), and a real ask-anything grounded across the whole suite (today's Ask tab is a thin preview of that). Discussed with Royce as the next tier up from this session's fix — this session deliberately shipped the cheap, clear win first. _(added 2026-07-29)_
- **The live end-to-end proof is still outstanding**: drop a deliberately-conflicting test row through production `/intake` and confirm it parks in the queue instead of committing. Blocked this session on the file-upload tool refusing to attach a test file not shared directly by Royce in chat — needs either Royce dragging the file into chat, or Royce doing the drop himself while checked live. This becomes easy to verify now that Overview/To Do is the single place to look. _(added 2026-07-29)_
- **Concatenate the always-loaded boot scripts into 2-3 files at deploy time** (plain concatenation, not a bundler — stays consistent with the repo's deliberate no-build-step architecture). Cuts request count on the true first-ever cold visit, which the version-tag fix below doesn't touch. _(added 2026-07-28)_
- **Audit which of the ~34 always-loaded-at-boot scripts actually need to block first paint** — several (recognitions.js, digest-settings.js, whatsnew.js, apprentice-widget.js, region-filter.js) look like narrow-feature scripts that could join the existing on-demand-per-page loading pattern already used for Roster/Timesheets/etc. _(added 2026-07-28)_
_…and 340 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
_…and 59 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2844 | 448 | 109 | 9 |
| [SKS](sks/pending.md) | 427 | 76 | 5 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 382 | 34 | 7 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-30 | [`__personal__` tenant "retired" doc claim corrected against live data](sessions/2026-07-30.md) |
| 2026-07-29 | [eq-receipts: fixed a duplicate-detection blind spot, added invoice number as a stronger match](sessions/2026-07-29.md) |
| 2026-07-28 | [Roster: archive Labour Hire from the grid with a rehire rating](sessions/2026-07-28.md) |
| 2026-07-27 | [eq-ui design handoff shipped + propagated to eq-shell/eq-service, real bugs found along the way](sessions/2026-07-27.md) |
| 2026-07-26 | [Customers page speed fix, Job Creation export bug found+fixed, customer-level default End Client, Ops quote-form layout](sessions/2026-07-26.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-30 08:00 UTC._

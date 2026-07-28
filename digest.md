---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-28 21:38 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-28 21:12 UTC → 2026-07-28 21:38 UTC)

- Merged: eq-shell [#1077](https://github.com/eq-solutions/eq-shell/pull/1077) fix(security): revoke anon EXECUTE on eq_enforce_function_pr
- Merged: eq-shell [#1073](https://github.com/eq-solutions/eq-shell/pull/1073) fix(sks-sync): stop the daily worker sync clobbering Shell s
- Merged: eq-shell [#1068](https://github.com/eq-solutions/eq-shell/pull/1068) feat(auth): TOTP backup codes for authenticator device loss
- Merged: eq-shell [#1066](https://github.com/eq-solutions/eq-shell/pull/1066) fix(licences): Replace photo button never clears its busy st
- Merged: eq-shell [#1064](https://github.com/eq-solutions/eq-shell/pull/1064) feat(cards): compliance register — one row per employee, not
- Merged: eq-shell [#1063](https://github.com/eq-solutions/eq-shell/pull/1063) fix(quotes): stop detail badge showing a stage change that n
- Merged: eq-shell [#1062](https://github.com/eq-solutions/eq-shell/pull/1062) feat(licences): let a manager replace the photo/PDF on an ex
- Merged: eq-shell [#1061](https://github.com/eq-solutions/eq-shell/pull/1061) fix(security): revoke anon EXECUTE on rls_introspection (eho

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F6: Append (>>) NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-07-28.md](sessions/2026-07-28.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (87)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to confirm live**: edit an already-reviewed licence's expiry/number in Cards for an approved worker, confirm the Staff page badge flips to "changed since — re-review needed" without a hard refresh. _(added 2026-07-28)_
- **EQ** · **Royce to confirm live**: reload the Wallet and confirm the Photo ID nag no longer shows for a worker who holds a Driver Licence or Passport. _(added 2026-07-28)_
- **EQ** · **Separate, lower-priority finding: 53 of 88 active SKS staff have a Cards worker link but zero credentials captured in Cards at all** (checked the pre-promotion `worker_credentials` table too — genuinely empty, not stuck mid-migration). Only 34 of 88 active staff have any licence data flowing through Shell. This is a Cards onboarding-completion gap, not a sync bug — no action taken, logging only per Royce's call. _(added 2026-07-28)_
- **EQ** · **Royce to click through the real flow once the deploy lands**: set up two-step verification, save the codes shown, sign out, sign back in using one of the backup codes instead of the phone app, then generate a fresh set from Settings and confirm the old ones stop working. _(added 2026-07-28)_
- **EQ** · **Royce to confirm live**: open Moahmmed Alsadiq Ahmed Elsayed on the Staff page, check the Photo ID and White Card show the new clearer photos, and that the "Replace photo" button now returns to normal after use. _(added 2026-07-28)_
- **EQ** · **Royce to review the two now-flagged duplicate pairs in the app** (Anthropic $12.02 USD and GitHub $68.64 USD, both 2026-07-22/07-28) and decide whether either was a genuine double-charge worth pursuing a refund/credit for, or just dismiss as intentional. _(added 2026-07-29)_
- **EQ** · **Royce to click through a real "New customer" add** once convenient, to confirm the address dropdown now actually appears and fills suburb/state (verified in code + build, not yet eyeballed live). _(added 2026-07-28)_
- **EQ** · **Royce to export a real org's compliance pack and eyeball the new layout in Excel** — verified in code and with a test run, not yet checked against a real export. _(added 2026-07-28)_
- **EQ** · **Royce to re-download a compliance pack once the deploy lands** and confirm the filename reads correctly and Rhys Scott's email now shows current. _(added 2026-07-28)_
- **EQ** · **Royce to re-enter Ben Ritchie's correct email one more time** via the Staff page — his last correction was reverted by the old bug before the fix went live, so the stale value is still sitting in the database. It will stick this time. _(added 2026-07-28)_
- **EQ** · **Royce to click through the Edit Roster grid on field.eq.solutions once the deploy lands** and confirm Ben Ritchie (or any off-roster person) no longer appears there — code-fixed and pushed, not yet eyeballed live. _(added 2026-07-28)_
- **EQ** · **Royce to check SKS-17489 in EQ Ops** once the deploy lands — confirm the badge and board agree, then enter a Job No. to actually advance it out of Open (that's why it was stuck). _(added 2026-07-28)_
_…and 75 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 1 | 0d |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 9 | 2026-07-28 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 5 | 2026-07-23 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
| eq-field | [ReferenceError: openTafeHolidaysConfig is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 3 | 2026-07-28 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 2 | 2026-07-28 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695940/) | 1 | 2026-07-27 |
| eq-field | [TypeError: Cannot set properties of null (setting 'innerHTML')](https://eq-solutions.sentry.io/issues/136685760/) | 1 | 2026-07-27 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-28 | eq-shell | [#1091](https://github.com/eq-solutions/eq-shell/pull/1091) fix(licences): stop the Cards resync from bumping updated_at on n |
| 2026-07-28 | eq-shell | [#1090](https://github.com/eq-solutions/eq-shell/pull/1090) chore(intake): remove the unlinked per-domain landing pages |
| 2026-07-28 | eq-shell | [#1088](https://github.com/eq-solutions/eq-shell/pull/1088) fix(intake): route the Health-console commit through intake-stage |
| 2026-07-28 | eq-shell | [#1089](https://github.com/eq-solutions/eq-shell/pull/1089) fix(home): apprentices land on WorkerHome, not the manager dashbo |
| 2026-07-28 | eq-shell | [#1087](https://github.com/eq-solutions/eq-shell/pull/1087) fix(cards): spinner on compliance-pack progress label |
| 2026-07-28 | eq-shell | [#1086](https://github.com/eq-solutions/eq-shell/pull/1086) feat(home): roster, leave, and prestart at-a-glance cards on Work |
| 2026-07-28 | eq-shell | [#1085](https://github.com/eq-solutions/eq-shell/pull/1085) fix(deps): react-router-dom 6.30.4 -> 7.18.1, closes the 2 remain |
| 2026-07-28 | eq-shell | [#1084](https://github.com/eq-solutions/eq-shell/pull/1084) fix(staff): stop Company field wiping on save, add apprentice yea |
| 2026-07-28 | eq-shell | [#1083](https://github.com/eq-solutions/eq-shell/pull/1083) fix(deps): sweep the remaining Dependabot alerts (146 -> 4 known/ |
| 2026-07-28 | eq-shell | [#1081](https://github.com/eq-solutions/eq-shell/pull/1081) feat(auth): tenant-scoped self-serve phone signup on Core login ( |
| 2026-07-28 | eq-shell | [#1082](https://github.com/eq-solutions/eq-shell/pull/1082) fix(suppliers): PR #1079's scroll wrapper was insufficient — forc |
| 2026-07-28 | eq-shell | [#1080](https://github.com/eq-solutions/eq-shell/pull/1080) fix(licences): licence-push never marks a revoked Cards licence i |
| 2026-07-28 | eq-shell | [#1079](https://github.com/eq-solutions/eq-shell/pull/1079) fix(suppliers): wrap desktop Table in a horizontal-scroll contain |
| 2026-07-28 | eq-shell | [#1078](https://github.com/eq-solutions/eq-shell/pull/1078) fix(admin): correct Worker join QR copy to match invite-required  |
| 2026-07-28 | eq-shell | [#1074](https://github.com/eq-solutions/eq-shell/pull/1074) fix(deps): xlsx off unpatched npm registry to SheetJS CDN fix |
_Showing 15 of 106 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Version-tag script URLs** (e.g. `app-state.js?v=3.5.374`) with long-lived immutable caching, so even the very first load per version skips the network-revalidation step entirely. Touches ~34 script tags in `index.html`; would extend the existing version-bump ritual. _(added 2026-07-28)_
- **Concatenate the always-loaded boot scripts into 2-3 files at deploy time** (plain concatenation, not a bundler — stays consistent with the repo's deliberate no-build-step architecture). Cuts request count on the true first-ever cold visit, which the caching fix above doesn't touch. _(added 2026-07-28)_
- **Audit which of the ~34 always-loaded-at-boot scripts actually need to block first paint** — several (recognitions.js, digest-settings.js, whatsnew.js, apprentice-widget.js, region-filter.js) look like narrow-feature scripts that could join the existing on-demand-per-page loading pattern already used for Roster/Timesheets/etc. _(added 2026-07-28)_
- **Netlify Early Hints (103) for the first, blocking script** — lets the browser start fetching before Netlify finishes streaming the page shell. Polish-tier, smallest expected impact of the four. _(added 2026-07-28)_
- **Working tree on that branch has an uncommitted fix for a real production incident** (`WORKER_RESOURCE_LIMIT / 546` — Deno edge function hit its memory limit running `unpdf` text-extraction concurrently across a 5-file batch) not yet committed or deployed. Live is still v6; this fix (serialize the text-extraction phase per file, keep vision fallback concurrent) would become v7. Whoever's session that is should commit + redeploy; not picked up by this session since it wasn't this session's work. _(added 2026-07-28)_
- **One DoS CVE left deliberately unfixed**: `brace-expansion` inside `exceljs`'s zip-writer chain (`archiver` → `archiver-utils` → `glob@7` → `minimatch@3.1.5`). The only full fix is a `minimatch` major bump, and this deep tree isn't verified against `minimatch`'s newer API — accepted as a residual rather than risk breaking xlsx writing in production. Low real-world exploitability (internal file-glob matching during archive creation, not attacker-reachable input). _(added 2026-07-28)_
- **Royce/a worker to trigger a slow or failed photo-read live and confirm the new message shows and stays** — verified in code + automated tests (88/88 passing), not yet clicked through for real. _(added 2026-07-28)_
- **Brian Griffin-Colls' First Aid/CPR certificate itself still needs updating** — the bug that silently dropped his attempt is now fixed, but his original update was never captured; someone still needs to redo it (himself, or an admin via the Staff page). _(added 2026-07-28)_
- **Competitive benchmark vs industry leaders (Deputy, Tradify, Fergus, simPRO, ServiceM8, Rhumbix, Skedulo)** — selected alongside the MD-tidy pass, but the session pivoted to the Sites-screen rebuild before it was run. Not started. _(added 2026-07-28)_
- **Go use the real review console next time** (Core → `IntakeHealthHome`'s Sites Dupes tab) instead of raw SQL — it already works. _(added 2026-07-28)_
_…and 339 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2720 | 432 | 83 | 9 |
| [SKS](sks/pending.md) | 434 | 76 | 12 | 13 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 382 | 34 | 7 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-29 | [eq-receipts: fixed a duplicate-detection blind spot, added invoice number as a stronger match](sessions/2026-07-29.md) |
| 2026-07-28 | [Roster: archive Labour Hire from the grid with a rehire rating](sessions/2026-07-28.md) |
| 2026-07-27 | [eq-ui design handoff shipped + propagated to eq-shell/eq-service, real bugs found along the way](sessions/2026-07-27.md) |
| 2026-07-26 | [Customers page speed fix, Job Creation export bug found+fixed, customer-level default End Client, Ops quote-form layout](sessions/2026-07-26.md) |
| 2026-07-25 | [Closed out the Coupa/staff-reactivation thread from the day before: merged PR #993, dispatched the ledger reconcile, explained the migration-numbering saga](sessions/2026-07-25.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-28 21:38 UTC._

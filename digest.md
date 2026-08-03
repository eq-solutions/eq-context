---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-03
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-03 19:04 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-03 19:03 UTC → 2026-08-03 19:04 UTC)

- Merged: eq-shell [#1213](https://github.com/eq-solutions/eq-shell/pull/1213) fix(ops): bolder column headers, less-pink estimator colours
- Merged: eq-shell [#1210](https://github.com/eq-solutions/eq-shell/pull/1210) chore(intake): auto re-vendor eq-intake/eq-platform
- Merged: eq-shell [#1209](https://github.com/eq-solutions/eq-shell/pull/1209) fix(ops): bolder file badge, colour-code estimator instead o
- Merged: eq-shell [#1207](https://github.com/eq-solutions/eq-shell/pull/1207) fix(shell): resolve all 117 eq-shell-owned no-explicit-any e
- Merged: eq-shell [#1206](https://github.com/eq-solutions/eq-shell/pull/1206) fix(shell): Worker Home shows warnings before everyday statu
- Merged: eq-shell [#1205](https://github.com/eq-solutions/eq-shell/pull/1205) fix(ops): show file-attached badge on Kanban pipeline board 
- Merged: eq-shell [#1204](https://github.com/eq-solutions/eq-shell/pull/1204) fix(shell): resolve @typescript-eslint/no-unused-vars (107 o
- Merged: eq-shell [#1202](https://github.com/eq-solutions/eq-shell/pull/1202) fix(shell): resolve the last react-hooks/refs error via JobR

## ⚠ Needs you (3)

- 🔴 **Sentry new error** — `eq-field` [Error: dashboard-map-css-collapsed](https://eq-solutions.sentry.io/issues/138007377/)
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (109)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Roll out past the one-person pilot** — widen who can sign in Field beyond you, put a real document through end-to-end beyond the one test document. Your call on timing. _(added 2026-08-03)_
- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
- **EQ** · **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
- **EQ** · **Staff duplicate handling — still Archive-only, needs your call before any build.** A real staff merge fans out into Field-owned operational tables (timesheets, schedule, licences, dispatch) — per the durable architecture rule, that can't be rebuilt Shell-side; it needs Field-repo coordination, which is a scope decision, not something to default on. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open a site, assign a supervisor from its own contact list, save, reload, confirm it sticks; toggle "Show archived" on the Sites list and confirm it filters/tags correctly. Needs a real sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-08-02)_
- **EQ** · **Royce to check `admin/users/migrate` for SKS against the 44-workers number above** — the invite screen and the 44 are counted two different ways (one by tenant employee record, one by Cards worker record), so they may not match exactly. Worth confirming they're the same gap before assuming the invite screen alone closes it. _(added 2026-08-02)_
- **EQ** · Royce to spot-check a generated PM Asset Report live for a site that has a photo on file — confirm the band + photo layout looks right. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open New Quote, attach a couple of files before finishing the form, submit, confirm the files show up on the created quote. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: open the Duplicate Sites panel as a non-manager and confirm Preview now shows; mark a row Unsure with a note and confirm it saves and displays; confirm a real merge now succeeds end-to-end (Preview → Confirm) now that the permission fix is live. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: sidebar logo and the admin Media Library page (grid + edit modal) for a tenant with a logo set — confirm images still render correctly after the switch above. _(added 2026-08-01)_
- **EQ** · **Royce to click through live on a real device** — confirm the "take a photo" sheet feels right end to end (camera opens, OCR reads the card, fallback link works). Note: the code merged this morning but wasn't actually live yet when Royce first tried it — this repo's deploy isn't automatic on merge, and nobody had triggered one. Deployed and confirmed live later the same day. _(added 2026-08-01, updated 2026-08-01)_
_…and 97 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 5 | 0d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [Error: dashboard-map-css-collapsed](https://eq-solutions.sentry.io/issues/138007377/) | 30 | 2026-08-03 |
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 19 | 2026-08-01 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 14 | 2026-08-02 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 7 | 2026-08-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-03 | eq-shell | [#1226](https://github.com/eq-solutions/eq-shell/pull/1226) feat(documents): daily reminder email for outstanding sign-offs |
| 2026-08-03 | eq-shell | [#1227](https://github.com/eq-solutions/eq-shell/pull/1227) fix(ops): collapsed group header count/total hidden for long cust |
| 2026-08-03 | eq-shell | [#1225](https://github.com/eq-solutions/eq-shell/pull/1225) fix(cards-handoff): log silent origin mismatch, normalise VITE_CA |
| 2026-08-03 | eq-shell | [#1224](https://github.com/eq-solutions/eq-shell/pull/1224) feat(ops): collapse repeat-customer quote groups on the Kanban bo |
| 2026-08-03 | eq-shell | [#1223](https://github.com/eq-solutions/eq-shell/pull/1223) fix(ops): po-matched status never synced the canonical job record |
| 2026-08-03 | eq-shell | [#1222](https://github.com/eq-solutions/eq-shell/pull/1222) feat(documents): sign-off certificate PDF + document templates |
| 2026-08-03 | eq-shell | [#1221](https://github.com/eq-solutions/eq-shell/pull/1221) fix(ops): migration 0236 needs DROP FUNCTION before CREATE OR REP |
| 2026-08-03 | eq-shell | [#1220](https://github.com/eq-solutions/eq-shell/pull/1220) fix(ops): board drag-and-drop now writes the canonical job record |
| 2026-08-03 | eq-shell | [#1219](https://github.com/eq-solutions/eq-shell/pull/1219) fix(auth): support contact link -> contact@eq.solutions |
| 2026-08-03 | eq-shell | [#1218](https://github.com/eq-solutions/eq-shell/pull/1218) fix(shell): collapse Roster/Leave glance tiles into the single Fi |
| 2026-08-03 | eq-shell | [#1217](https://github.com/eq-solutions/eq-shell/pull/1217) feat(documents): sign-off evidence view for the Register tab |
| 2026-08-03 | eq-shell | [#1216](https://github.com/eq-solutions/eq-shell/pull/1216) fix(ops): board Sent checkbox now promotes draft quotes to submit |
| 2026-08-03 | eq-shell | [#1215](https://github.com/eq-solutions/eq-shell/pull/1215) fix(ops): move the job-no-required message into a visible toast |
| 2026-08-03 | eq-shell | [#1214](https://github.com/eq-solutions/eq-shell/pull/1214) fix(ops): darken customer group header, drop redundant in-card cu |
| 2026-08-03 | eq-shell | [#1212](https://github.com/eq-solutions/eq-shell/pull/1212) feat(documents): add signature_image column for sign-off register |
_Showing 15 of 145 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Reminder chasing** — automatically nudging people who haven't signed yet, on a schedule (same idea as Field's night-before-job text reminder). Never scoped this session, no work started. _(added 2026-08-03)_
- **Sign-off records can currently be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Low real risk today (almost no records exist yet), but needs a proper database fix before this rolls out past you. Flagged repeatedly across this build, still open. _(added 2026-08-03)_
- **eq-field's app icon colour may still be the old stale SKS navy** — same class of leftover your brand-colour correction already caught and fixed elsewhere; spotted in passing this session, not independently checked against the live branding table. Worth a quick look. _(added 2026-08-03)_
- **Confirm the scheduled nightly drift check itself shows green**, not just the one-off PR check — same logic, but hasn't been observed on a real nightly run yet. Should self-resolve. _(added 2026-08-03)_
- **The Supabase startup failure in CI** (a leftover database setting missing an `id` column, breaking the API's schema cache) is separate, pre-existing, and still red on every run — worth a dedicated fix at some point, not touched this session. _(added 2026-08-03)_
- **Separate, lower-priority**: one more stale-type warning (`tenant_settings.archive_grace_period_days`) traces to a database change from months ago that was never actually applied live — left alone on purpose, different job. _(added 2026-08-03, carried forward)_
- **`eq-solves-assets` folder points at the wrong GitHub repo** (a personal fork of the Service app, not the real assets repo) — Royce: "on the back burner, can be ignored." Deprioritized, not investigated further. _(added 2026-08-03, updated 2026-08-03)_
- **eq-shell's `smoke.yml` check is chronically noisy** (roughly 1 in 3 runs fails on a timing timeout, always self-resolves) — not a real bug, but worth a longer timeout if the false alarms bother anyone watching it. _(added 2026-08-03)_
- **The shared `eq-context` checkout keeps taking damage from concurrent-session git races** — a stuck rebase, a live conflict-marker corruption on `main`, and two separate non-fast-forward push rejections all landed within about 10 minutes from multiple sessions writing to the same working directory at once; a follow-up session then found local `main` had diverged again and, even after verifying the fix in an isolated clone, applying it back on the shared checkout still collided with a second concurrent rebase (HEAD detached, `main` ref left pointing at a stale commit — fixed, no data lost). Worth deciding whether concurrent sessions should default to a fresh clone for any `/close`, not just multi-step surgery — the existing guidance undersells how often this is now actually happening. _(added 2026-08-03)_
- **Royce (or a real signed-in worker) to confirm live**: save/create a Cards profile and confirm it no longer errors. Off-limits for me to click-test myself. _(added 2026-08-03)_
_…and 385 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
_…and 64 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3254 | 522 | 164 | 12 |
| [SKS](sks/pending.md) | 424 | 83 | 5 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 5 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-04 | [Removed the "What's new" banner from both SKS NSW Labour and EQ Field](sessions/2026-08-04.md) |
| 2026-08-03 | [EQ-FIELD-10 Sentry triage: tracked, not fixed (Royce's call)](sessions/2026-08-03.md) |
| 2026-08-02 | [eq-solves-service: PM reports were showing the wrong "supervisor" and blank contact details, never wired to the real site-supervisor feature](sessions/2026-08-02.md) |
| 2026-08-01 | [Confirmed the "no Supabase connector" finding, then closed a real EQ-tenant roster gap found via a backlog sweep](sessions/2026-08-01.md) |
| 2026-07-31 | [Quote events now stamp app_source='ops' instead of the retired app name (continuation of 2026-07-30)](sessions/2026-07-31.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-03 19:04 UTC._

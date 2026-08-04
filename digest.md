---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-04
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-04 10:21 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-04 10:20 UTC → 2026-08-04 10:21 UTC)

- Merged: eq-shell [#1230](https://github.com/eq-solutions/eq-shell/pull/1230) fix(ops): add FK constraint on app_data.jobs.quote_id
- Merged: eq-shell [#1224](https://github.com/eq-solutions/eq-shell/pull/1224) feat(ops): collapse repeat-customer quote groups on the Kanb
- Merged: eq-shell [#1222](https://github.com/eq-solutions/eq-shell/pull/1222) feat(documents): sign-off certificate PDF + document templat
- Merged: eq-shell [#1221](https://github.com/eq-solutions/eq-shell/pull/1221) fix(ops): migration 0236 needs DROP FUNCTION before CREATE O
- Merged: eq-shell [#1219](https://github.com/eq-solutions/eq-shell/pull/1219) fix(auth): support contact link -> contact@eq.solutions
- Merged: eq-shell [#1217](https://github.com/eq-solutions/eq-shell/pull/1217) feat(documents): sign-off evidence view for the Register tab
- Merged: eq-shell [#1216](https://github.com/eq-solutions/eq-shell/pull/1216) fix(ops): board Sent checkbox now promotes draft quotes to s
- Merged: eq-shell [#1213](https://github.com/eq-solutions/eq-shell/pull/1213) fix(ops): bolder column headers, less-pink estimator colours

## ⚠ Needs you (2)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (112)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Whether EQ Field should ever be allowed to write supervisor data itself** (not just read it from Shell) — steelmanned both sides this session (real case for: friction lands on-site not in the office, Field already owns adjacent operational facts like licences/dispatch, today's audit showed Shell's own data was the stale one; real case against: two write paths racing on one record is exactly what caused this session's original duplicate-identity bug). No decision made — still Royce's call, and the safe shape if it's ever built is Field calling Shell's own `entity-patch` RPC, never a second raw-table write path. _(added 2026-08-04)_
- **EQ** · **Roll out past the one-person pilot** — widen who can sign in Field beyond you, put a real document through end-to-end beyond the one test document. Your call on timing. _(added 2026-08-03)_
- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
- **EQ** · **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
- **EQ** · **Staff duplicate handling — still Archive-only, needs your call before any build.** A real staff merge fans out into Field-owned operational tables (timesheets, schedule, licences, dispatch) — per the durable architecture rule, that can't be rebuilt Shell-side; it needs Field-repo coordination, which is a scope decision, not something to default on. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open a site, assign a supervisor from its own contact list, save, reload, confirm it sticks; toggle "Show archived" on the Sites list and confirm it filters/tags correctly. Needs a real sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-08-02)_
- **EQ** · **Royce to check `admin/users/migrate` for SKS against the 44-workers number above** — the invite screen and the 44 are counted two different ways (one by tenant employee record, one by Cards worker record), so they may not match exactly. Worth confirming they're the same gap before assuming the invite screen alone closes it. _(added 2026-08-02)_
- **EQ** · Royce to spot-check a generated PM Asset Report live for a site that has a photo on file — confirm the band + photo layout looks right. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open New Quote, attach a couple of files before finishing the form, submit, confirm the files show up on the created quote. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: open the Duplicate Sites panel as a non-manager and confirm Preview now shows; mark a row Unsure with a note and confirm it saves and displays; confirm a real merge now succeeds end-to-end (Preview → Confirm) now that the permission fix is live. _(added 2026-08-01)_
_…and 100 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 1 | 0d |
| eq-solves-service | ✓ success | 0d ago | 5 | 1d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | 0d |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 19 | 2026-08-01 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 15 | 2026-08-03 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 7 | 2026-08-02 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-shell | [Cards handoff request from unexpected origin](https://eq-solutions.sentry.io/issues/138655603/) | 3 | 2026-08-04 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 6](https://eq-solutions.sentry.io/issues/138175643/) | 3 | 2026-08-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-04 | eq-shell | [#1238](https://github.com/eq-solutions/eq-shell/pull/1238) feat(licences): show the uploaded photo/PDF as a manual-fill back |
| 2026-08-04 | eq-shell | [#1237](https://github.com/eq-solutions/eq-shell/pull/1237) fix(staff): hide Company field for Direct, require supervision ca |
| 2026-08-04 | eq-shell | [#1236](https://github.com/eq-solutions/eq-shell/pull/1236) fix(staff): require supervisor_category when is_supervisor is set |
| 2026-08-04 | eq-shell | [#1235](https://github.com/eq-solutions/eq-shell/pull/1235) fix(licences): timeout the OCR auto-read chain instead of hanging |
| 2026-08-04 | eq-shell | [#1234](https://github.com/eq-solutions/eq-shell/pull/1234) feat(staff): back-photo support in admin licence backfill |
| 2026-08-04 | eq-shell | [#1233](https://github.com/eq-solutions/eq-shell/pull/1233) fix(deps): bump fast-uri to 4.1.2 (CVE-2026-18446) |
| 2026-08-04 | eq-shell | [#1232](https://github.com/eq-solutions/eq-shell/pull/1232) fix(invites): recover gracefully from a raced duplicate invite in |
| 2026-08-04 | eq-solves-service | [#690](https://github.com/eq-solutions/eq-service/pull/690) fix(tenant-scoping): two service-role queries had no defense-in-d |
| 2026-08-04 | eq-field | [#647](https://github.com/eq-solutions/eq-field/pull/647) v3.5.453 — PWA app icon: fix stale SKS colour, make Add-to-Home-S |
| 2026-08-04 | eq-field | [#646](https://github.com/eq-solutions/eq-field/pull/646) fix(ts-reminder): dedup check had no tenant filter |
| 2026-08-04 | eq-field | [#645](https://github.com/eq-solutions/eq-field/pull/645) v3.5.452 — Toolbox Talk: Reopen a submitted talk to fix a mistake |
| 2026-08-04 | eq-cards | [#212](https://github.com/eq-solutions/eq-cards/pull/212) fix(shell-handoff): validate a locally-cached session before skip |
| 2026-08-04 | eq-cards | [#211](https://github.com/eq-solutions/eq-cards/pull/211) fix(ocr): timeout the Anthropic call in ocr-licence instead of ha |
| 2026-08-04 | eq-cards | [#210](https://github.com/eq-solutions/eq-cards/pull/210) fix(invites): DB-level guard against duplicate unclaimed worker i |
| 2026-08-03 | eq-shell | [#1229](https://github.com/eq-solutions/eq-shell/pull/1229) fix(auth): guard shell-join-tenant's existing-user phone match ag |
_Showing 15 of 146 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **`C:\Projects\CLAUDE.md` is still the only home for Rule 0, Rule 0.5 and the load-bearing-facts list.** Rule 0.6 and the effort threshold were moved into governed substrate; the rest wasn't. That file isn't version-controlled, has no CI, and is only read by a session started in that folder. Same shadow-memory class as failure F5. _(added 2026-08-04)_
- **Deleting the shadowed `.git/hooks/pre-commit` is held, not done.** Repointing every worktree's `core.hooksPath` to `.githooks` was tried and reverted for 4 of 5 open worktrees (`agent-af31fd71dc13a91c7`, `silly-noether-ec8a81`, `skills-list-html-908d61`, `eq-context-reflection-protocol-wt`) — their branches predate today's secret-guard delegation, so their own `.githooks/pre-commit` has zero secret-scanning in it. Repointing them would have silently removed their only secret guard, so they're back on `.git/hooks` until their branches merge or rebase past `main` (`1059f85`). Safe to repoint + delete at that point, not before. _(added 2026-08-04)_
- **Multiple concurrent Claude sessions were pushing to eq-field's `main` throughout this session** — two real version-number collisions happened and were caught/resolved live, but this is a standing risk with the current strict-monotonic-versioning convention, not a one-off. Worth knowing if it keeps happening. _(added 2026-08-04)_
- **Reminder chasing** — automatically nudging people who haven't signed yet, on a schedule (same idea as Field's night-before-job text reminder). Never scoped this session, no work started. _(added 2026-08-03)_
- **Sign-off records can currently be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Low real risk today (almost no records exist yet), but needs a proper database fix before this rolls out past you. Flagged repeatedly across this build, still open. _(added 2026-08-03)_
- **eq-field's app icon colour may still be the old stale SKS navy** — same class of leftover your brand-colour correction already caught and fixed elsewhere; spotted in passing this session, not independently checked against the live branding table. Worth a quick look. _(added 2026-08-03)_
- **Confirm the scheduled nightly drift check itself shows green**, not just the one-off PR check — same logic, but hasn't been observed on a real nightly run yet. Should self-resolve. _(added 2026-08-03)_
- **The Supabase startup failure in CI** (a leftover database setting missing an `id` column, breaking the API's schema cache) is separate, pre-existing, and still red on every run — worth a dedicated fix at some point, not touched this session. _(added 2026-08-03)_
- **Separate, lower-priority**: one more stale-type warning (`tenant_settings.archive_grace_period_days`) traces to a database change from months ago that was never actually applied live — left alone on purpose, different job. _(added 2026-08-03, carried forward)_
- **`eq-solves-assets` folder points at the wrong GitHub repo** (a personal fork of the Service app, not the real assets repo) — Royce: "on the back burner, can be ignored." Deprioritized, not investigated further. _(added 2026-08-03, updated 2026-08-03)_
_…and 392 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
_…and 64 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3305 | 531 | 168 | 12 |
| [SKS](sks/pending.md) | 438 | 84 | 6 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 5 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-04 | [Removed the "What's new" banner from both SKS NSW Labour and EQ Field](sessions/2026-08-04.md) |
| 2026-08-04 | [e — Fernando Alba onboarding surfaced two Shell gaps: back-photo support + OCR-hang fix, both shipped live](sessions/2026-08-04-e.md) |
| 2026-08-03 | [EQ-FIELD-10 Sentry triage: tracked, not fixed (Royce's call)](sessions/2026-08-03.md) |
| 2026-08-02 | [eq-solves-service: PM reports were showing the wrong "supervisor" and blank contact details, never wired to the real site-supervisor feature](sessions/2026-08-02.md) |
| 2026-08-01 | [Confirmed the "no Supabase connector" finding, then closed a real EQ-tenant roster gap found via a backlog sweep](sessions/2026-08-01.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-04 10:21 UTC._

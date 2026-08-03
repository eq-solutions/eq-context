---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-03
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-03 10:24 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-03 10:21 UTC → 2026-08-03 10:24 UTC)

- Merged: eq-shell [#1212](https://github.com/eq-solutions/eq-shell/pull/1212) feat(documents): add signature_image column for sign-off reg
- Merged: eq-shell [#1199](https://github.com/eq-solutions/eq-shell/pull/1199) fix(auth): recovery-email nudge distinguishes dropped email 
- Merged: eq-shell [#1198](https://github.com/eq-solutions/eq-shell/pull/1198) fix(shell): resolve react-hooks/refs in iframe pre-warm keep
- Merged: eq-shell [#1197](https://github.com/eq-solutions/eq-shell/pull/1197) fix(auth): Cards SSO no longer depends on the worker having 
- Merged: eq-shell [#1196](https://github.com/eq-solutions/eq-shell/pull/1196) feat(documents): Shell upload + push UI for the sign-off reg
- Merged: eq-shell [#1195](https://github.com/eq-solutions/eq-shell/pull/1195) feat(auth): trim worker-add dropdown to 2 items, surface gen
- Merged: eq-shell [#1193](https://github.com/eq-solutions/eq-shell/pull/1193) fix(auth): self-join adds a membership in the new tenant, no
- Merged: eq-shell [#1190](https://github.com/eq-solutions/eq-shell/pull/1190) feat(intake): Contact resolver + merge (migrations 0233/0234

## ⚠ Needs you (3)

- 🔴 **Sentry new error** — `eq-field` [Error: dashboard-page-height-drop](https://eq-solutions.sentry.io/issues/138007377/)
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (109)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
- **EQ** · **Royce to refresh Platform Console once more and confirm it now shows real numbers** (companies, wallet counts, sync health) instead of an error. Both fixes are live as of 2026-08-03. _(added 2026-08-03)_
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
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 5 | 0d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [Error: dashboard-page-height-drop](https://eq-solutions.sentry.io/issues/138007377/) | 29 | 2026-08-03 |
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
| 2026-08-03 | eq-shell | [#1212](https://github.com/eq-solutions/eq-shell/pull/1212) feat(documents): add signature_image column for sign-off register |
| 2026-08-03 | eq-shell | [#1213](https://github.com/eq-solutions/eq-shell/pull/1213) fix(ops): bolder column headers, less-pink estimator colours, bol |
| 2026-08-03 | eq-shell | [#1211](https://github.com/eq-solutions/eq-shell/pull/1211) fix(ops): unique stage colours, re-spread estimator palette, wide |
| 2026-08-03 | eq-shell | [#1210](https://github.com/eq-solutions/eq-shell/pull/1210) chore(intake): auto re-vendor eq-intake/eq-platform |
| 2026-08-03 | eq-shell | [#1209](https://github.com/eq-solutions/eq-shell/pull/1209) fix(ops): bolder file badge, colour-code estimator instead of cus |
| 2026-08-03 | eq-shell | [#1208](https://github.com/eq-solutions/eq-shell/pull/1208) feat(documents): register view for the sign-off register (step 5) |
| 2026-08-03 | eq-shell | [#1206](https://github.com/eq-solutions/eq-shell/pull/1206) fix(shell): Worker Home shows warnings before everyday status |
| 2026-08-03 | eq-shell | [#1207](https://github.com/eq-solutions/eq-shell/pull/1207) fix(shell): resolve all 117 eq-shell-owned no-explicit-any errors |
| 2026-08-03 | eq-shell | [#1205](https://github.com/eq-solutions/eq-shell/pull/1205) fix(ops): show file-attached badge on Kanban pipeline board cards |
| 2026-08-03 | eq-shell | [#1203](https://github.com/eq-solutions/eq-shell/pull/1203) fix(auth): hotfix — Cards SSO email-sync missed a phone-only work |
| 2026-08-03 | eq-shell | [#1204](https://github.com/eq-solutions/eq-shell/pull/1204) fix(shell): resolve @typescript-eslint/no-unused-vars (107 of 120 |
| 2026-08-03 | eq-shell | [#1202](https://github.com/eq-solutions/eq-shell/pull/1202) fix(shell): resolve the last react-hooks/refs error via JobRow ex |
| 2026-08-03 | eq-shell | [#1200](https://github.com/eq-solutions/eq-shell/pull/1200) fix(shell): resolve remaining react-hooks/refs errors (19 of 20) |
| 2026-08-03 | eq-shell | [#1201](https://github.com/eq-solutions/eq-shell/pull/1201) fix(shell): resolve no-restricted-syntax hex-colour errors (8) |
| 2026-08-03 | eq-field | [#631](https://github.com/eq-solutions/eq-field/pull/631) fix(dashboard): stop map watchdog false-firing Sentry on tab swit |
_Showing 15 of 140 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Live click-through not done** — confirm on `/sks/ops?tab=dashboard` that SKS-17577 (and other quotes with saved files) now shows the paperclip icon on the board card. Needs a real authenticated session, off-limits for me to do myself. _(added 2026-08-03)_
- **OCR-scanned name still unconfirmed whether it reaches `profiles.full_name`** — flagged in the 2026-08-02 self-join fixes entry below and never independently verified since; still open. _(added 2026-08-03, carried from 2026-08-02)_
- **The `ensureAuthUser` email-sync bug class is worth a second look**: it took a real live failure to catch a `null`-vs-falsy gap in a brand-new function. Worth considering whether any other "sync if different" checks in the auth path have the same falsy-null blind spot — not swept this session. _(added 2026-08-03)_
- **Live click-through not done** — confirm on core.eq.solutions that Field/Service/Cards still pre-warm within 2.5s, switching between them stays fast, and a first-navigation-before-prewarm still mounts instantly with no flash. Needs a real authenticated session, off-limits for me to do myself. _(added 2026-08-03)_
- **Repo-wide `pnpm lint` shows 438 pre-existing errors** elsewhere (mostly `react-hooks/set-state-in-effect`), same root cause (the react-hooks v7 upgrade) but a much larger surface than this PR's scope. `ci.yml` already documents lint as advisory (`continue-on-error`) because of this debt, so nothing is silently failing — but worth a dedicated session if/when there's appetite to burn it down before flipping lint to blocking. _(added 2026-08-03)_
- **Visual check not done** — `LabourHireRates.tsx` and `WorkerHome.tsx` are both behind real auth; couldn't click through myself. A local Browser-tool CSS-swatch comparison also failed (file:// navigate timed out), so verification rests on `@eq-design-tokens`'s own hex definitions, not a live render. Two of the eight swaps aren't exact-hex matches (`var(--eq-grey)` for `#5F5E5A`, and the three status tokens for the WorkerHome tile accents) — worth a glance to confirm nothing looks off. _(added 2026-08-03)_
- **Live click-through not done** — the comms job table's inline editing (click-to-edit, Enter/Tab save-and-move, Esc cancel, cross-row keyboard nav) needs a real click-through on the NSW Comms board before trusting the extraction blind. Content moved verbatim and the shared-state/keyboard-nav logic was reasoned through carefully, but a structural change like this deserves a real look. Needs a real authenticated session, off-limits for me to do myself. _(added 2026-08-03)_
- **Bridging Cards' new trade/employer data into Shell** — deliberately not built; no rule exists yet for what happens when a worker's own answer disagrees with what an employer has on file. _(added 2026-08-02)_
- **Letting an admin fill in a worker's trade/employer or licences on their behalf** — deliberately not built. Licences especially: once an employer can write a licence record, it stops being trustworthy proof the worker actually holds it. Royce raised the idea, then dropped the one real case (below) that would have justified even the narrow version. _(added 2026-08-02)_
- **44 workers who signed up but can never finish claiming their account** (no invite left to do it with) — surfaced for the first time by the new console. Royce said to leave this alone for now. _(added 2026-08-02)_
_…and 374 more · [eq/pending.md](eq/pending.md)_

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
_…and 65 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3196 | 507 | 150 | 12 |
| [SKS](sks/pending.md) | 424 | 83 | 5 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 5 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-03 | [EQ-FIELD-10 Sentry triage: tracked, not fixed (Royce's call)](sessions/2026-08-03.md) |
| 2026-08-02 | [eq-solves-service: PM reports were showing the wrong "supervisor" and blank contact details, never wired to the real site-supervisor feature](sessions/2026-08-02.md) |
| 2026-08-01 | [Confirmed the "no Supabase connector" finding, then closed a real EQ-tenant roster gap found via a backlog sweep](sessions/2026-08-01.md) |
| 2026-07-31 | [Quote events now stamp app_source='ops' instead of the retired app name (continuation of 2026-07-30)](sessions/2026-07-31.md) |
| 2026-07-30 | [`__personal__` tenant "retired" doc claim corrected against live data](sessions/2026-07-30.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-03 10:24 UTC._

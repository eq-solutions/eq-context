---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-04
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-04 08:58 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-04 08:58 UTC → 2026-08-04 08:58 UTC)

- Merged: eq-shell [#1233](https://github.com/eq-solutions/eq-shell/pull/1233) fix(deps): bump fast-uri to 4.1.2 (CVE-2026-18446)
- Merged: eq-shell [#1218](https://github.com/eq-solutions/eq-shell/pull/1218) fix(shell): collapse Roster/Leave glance tiles into the sing
- Merged: eq-shell [#1215](https://github.com/eq-solutions/eq-shell/pull/1215) fix(ops): move the job-no-required message into a visible to
- Merged: eq-shell [#1214](https://github.com/eq-solutions/eq-shell/pull/1214) fix(ops): darken customer group header, drop redundant in-ca
- Merged: eq-shell [#1211](https://github.com/eq-solutions/eq-shell/pull/1211) fix(ops): unique stage colours, re-spread estimator palette,
- Merged: eq-shell [#1208](https://github.com/eq-solutions/eq-shell/pull/1208) feat(documents): register view for the sign-off register (st
- Merged: eq-shell [#1205](https://github.com/eq-solutions/eq-shell/pull/1205) fix(ops): show file-attached badge on Kanban pipeline board 
- Merged: eq-shell [#1204](https://github.com/eq-solutions/eq-shell/pull/1204) fix(shell): resolve @typescript-eslint/no-unused-vars (107 o

## ⚠ Needs you (2)

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
| eq-shell | ✓ success | 0d ago | 1 | 0d |
| eq-solves-service | ✓ success | 0d ago | 5 | 1d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 19 | 2026-08-01 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 15 | 2026-08-03 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 7 | 2026-08-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-shell | [Cards handoff request from unexpected origin](https://eq-solutions.sentry.io/issues/138655603/) | 3 | 2026-08-04 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 6](https://eq-solutions.sentry.io/issues/138175643/) | 3 | 2026-08-03 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-04 | eq-shell | [#1233](https://github.com/eq-solutions/eq-shell/pull/1233) fix(deps): bump fast-uri to 4.1.2 (CVE-2026-18446) |
| 2026-08-04 | eq-shell | [#1232](https://github.com/eq-solutions/eq-shell/pull/1232) fix(invites): recover gracefully from a raced duplicate invite in |
| 2026-08-04 | eq-field | [#645](https://github.com/eq-solutions/eq-field/pull/645) v3.5.452 — Toolbox Talk: Reopen a submitted talk to fix a mistake |
| 2026-08-04 | eq-cards | [#210](https://github.com/eq-solutions/eq-cards/pull/210) fix(invites): DB-level guard against duplicate unclaimed worker i |
| 2026-08-03 | eq-shell | [#1229](https://github.com/eq-solutions/eq-shell/pull/1229) fix(auth): guard shell-join-tenant's existing-user phone match ag |
| 2026-08-03 | eq-shell | [#1228](https://github.com/eq-solutions/eq-shell/pull/1228) fix(documents): sign-off reminder cadence to a uniform 7 days |
| 2026-08-03 | eq-shell | [#1230](https://github.com/eq-solutions/eq-shell/pull/1230) fix(ops): add FK constraint on app_data.jobs.quote_id |
| 2026-08-03 | eq-shell | [#1226](https://github.com/eq-solutions/eq-shell/pull/1226) feat(documents): daily reminder email for outstanding sign-offs |
| 2026-08-03 | eq-shell | [#1227](https://github.com/eq-solutions/eq-shell/pull/1227) fix(ops): collapsed group header count/total hidden for long cust |
| 2026-08-03 | eq-shell | [#1225](https://github.com/eq-solutions/eq-shell/pull/1225) fix(cards-handoff): log silent origin mismatch, normalise VITE_CA |
| 2026-08-03 | eq-shell | [#1224](https://github.com/eq-solutions/eq-shell/pull/1224) feat(ops): collapse repeat-customer quote groups on the Kanban bo |
| 2026-08-03 | eq-shell | [#1223](https://github.com/eq-solutions/eq-shell/pull/1223) fix(ops): po-matched status never synced the canonical job record |
| 2026-08-03 | eq-shell | [#1222](https://github.com/eq-solutions/eq-shell/pull/1222) feat(documents): sign-off certificate PDF + document templates |
| 2026-08-03 | eq-shell | [#1221](https://github.com/eq-solutions/eq-shell/pull/1221) fix(ops): migration 0236 needs DROP FUNCTION before CREATE OR REP |
| 2026-08-03 | eq-shell | [#1220](https://github.com/eq-solutions/eq-shell/pull/1220) fix(ops): board drag-and-drop now writes the canonical job record |
_Showing 15 of 146 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Nothing has checked whether the existing code already breaks the new tenant rule.** `rules/non-negotiables.md` #11 (every service-role / admin-client query must explicitly filter by tenant) went in as a forward-looking rule. No audit was run against the edge functions and server routes that exist today, so we don't know if there's a live gap or none. A missing filter here returns *more* rows rather than an error, so it wouldn't have shown up as a bug — that's exactly why it needs a deliberate look rather than waiting for a symptom. Scope: `supabase/functions/**` and admin-client call sites across eq-shell, eq-service and eq-field. _(added 2026-08-04)_
- **`C:\Projects\CLAUDE.md` is still the only home for Rule 0, Rule 0.5 and the load-bearing-facts list.** Rule 0.6 and the effort threshold were moved into governed substrate this session; the rest wasn't. That file isn't version-controlled, has no CI, and is only read by a session started in that folder — so those rules still never reach Chat, ChatGPT or Grok, and nothing would catch them going stale. Same shadow-memory class as failure F5. Deliberately left narrow this session rather than rewriting a file with no safety net; worth deciding whether the remainder moves too. _(added 2026-08-04)_
- **Two duplicated facts spotted while correcting `rules/deployment.md`, not chased.** The deploy tables in the personal global instructions and in `suite-state.md` disagree about EQ Service's live URL (`service.eq.solutions` vs `eq-solves-service.netlify.app`). The repo tables were switched to point at `suite-state.md` rather than restate URLs, which sidesteps it, but the underlying disagreement is unresolved and only one can be right. _(added 2026-08-04)_
- **Someone needs to actually mark real SKS people as supervisors with a category in Shell's Staff page for the `eq` sandbox tenant** — the database now supports it (this session's fix), but zero people are marked yet, so Supervision will show empty on `eq` until that happens. Not a code task.
- **3 real SKS people (John Angangan, Scott Hotson, Jack Cluff) are marked as supervisors in Shell but have no category set** — shows as a stray "Direct" group on the live Supervision page. Shell-side data entry, not an eq-field fix.
- **Whether EQ Field should ever be allowed to write supervisor data itself** (not just read it from Shell) — raised as "in a perfect world" by Royce; deliberately not built, since Field's current read-only design exists specifically to prevent two apps racing to own the same record. Needs an explicit decision, not an assumption. _(added 2026-08-04)_
- **Toolbox Talk now has no way to correct a typo in an already-submitted talk** — inherits the same gap Prestart already had (no "reopen" path). Known tradeoff of the lock-on-submit fix above, not solved this session. _(added 2026-08-04)_
- **Multiple concurrent Claude sessions were pushing to eq-field's `main` throughout this session** — two real version-number collisions happened and were caught/resolved live, but this is a standing risk with the current strict-monotonic-versioning convention, not a one-off. Worth knowing if it keeps happening. _(added 2026-08-04)_
- **Reminder chasing** — automatically nudging people who haven't signed yet, on a schedule (same idea as Field's night-before-job text reminder). Never scoped this session, no work started. _(added 2026-08-03)_
- **Sign-off records can currently be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Low real risk today (almost no records exist yet), but needs a proper database fix before this rolls out past you. Flagged repeatedly across this build, still open. _(added 2026-08-03)_
_…and 393 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Not committed, not pushed, no PR opened.** Sitting on worktree branch `claude/missing-prestarts-777d49` in `sks-nsw-labour`. Royce hasn't given the explicit go to commit/push per the non-negotiables — next session (or this one, if Royce confirms) should do that before considering this shipped. _(added 2026-08-04)_
- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
_…and 65 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3272 | 530 | 161 | 12 |
| [SKS](sks/pending.md) | 431 | 84 | 8 | 16 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-04 08:58 UTC._

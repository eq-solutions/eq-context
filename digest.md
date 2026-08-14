---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-14
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-14 07:51 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-14 06:11 UTC → 2026-08-14 07:51 UTC)

- Merged: eq-shell [#1333](https://github.com/eq-solutions/eq-shell/pull/1333) chore(ci): add attachment row/file reconciliation check
- Merged: eq-shell [#1332](https://github.com/eq-solutions/eq-shell/pull/1332) chore: delete unrouted CoreHome.tsx (EQ Intelligence mock ho
- Merged: eq-shell [#1331](https://github.com/eq-solutions/eq-shell/pull/1331) fix(db): drop unused quote_attachment table + fix stale docs
- Merged: eq-shell [#1330](https://github.com/eq-solutions/eq-shell/pull/1330) fix(documents): treat O&M manuals as reference library, not 
- Merged: eq-shell [#1328](https://github.com/eq-solutions/eq-shell/pull/1328) chore(ci): triage is_worker_in_org into KNOWN_UNSOURCED (cro
- Merged: eq-shell [#1323](https://github.com/eq-solutions/eq-shell/pull/1323) fix(staff): thread licence_verifications through the invite-
- Merged: eq-shell [#1321](https://github.com/eq-solutions/eq-shell/pull/1321) feat(staff): write path for team/supervisor assignment on th
- Merged: eq-shell [#1320](https://github.com/eq-solutions/eq-shell/pull/1320) feat(ops): bulk select in Archived tab (restore / delete mul

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 2 consecutive scheduled run(s) failed, last success 2026-08-11 · [failures.md](system/failures.md) F11
- 🟠 **Sentry new error** — `eq-cards` [minified:a42: FunctionException(status: 502, details: {error](https://eq-solutions.sentry.io/issues/140383786/)

## 🙋 Waiting on you (104)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Front-door merge (AdminWorkerInviteForm vs LabourHireIntakeTool) scoped, not decided.** A live-wiring audit (this session) found worker-creation fragmented across 6 independent paths with inconsistent phone rules and notification behaviour. Two real bugs found and fixed same session: the intake edge function was stuck on a stale single-file deploy despite the multi-file rework already being merged to eq-cards `main` (redeployed live) and `/_platform/labour-hire-intake` had no nav link anywhere, findable only by typing the URL (added, eq-shell [#1296](https://github.com/eq-solutions/eq-shell/pull/1296), merged). A third option — merging the admin-invite and labour-hire write paths into one shared matching function — was investigated and explicitly rejected: they're deliberately different trust models (admin-known-person reuse-first vs ops-blind-document never-auto-attach-to-claimed), not duplicate code; merging would regress one path or the other. Whether to merge the two *front-end forms* themselves (not the write logic) is still open — Royce's call, not re-raised without new information. _(added 2026-08-11)_
- **EQ** · **Needs Royce, not more building:** already superseded below (2026-08-11 explicit go-ahead) for the overseas-goal exclusion specifically — the real remaining blocker is operational: generate + set `EQ_CARDS_HANDOFF_KEY` on both Netlify projects (nothing works until it exists) — manual-hands-only, Claude Code is blocked from writing Netlify secrets by design. **Note 2026-08-13:** the TODAY.md overseas goal this entry originally cited was killed (Royce's explicit call) — doesn't change anything here, the Netlify-secret step was already the actual blocker, not the goal. _(added 2026-08-10)_
- **EQ** · **Not built.** Royce to decide whether this graduates back onto `system/punch-list.md` for the actual simplification work, given the goal's current exclusion on live UI changes affecting real users while overseas. _(added 2026-08-10)_
- **EQ** · **Work sits uncommitted, not lost** — on branch `fix/integration-ci-app-data-bootstrap` in the shared root checkout at `C:\Projects\eq-solves-service`. Needs Royce to get Docker running (or hand over a `supabase db dump` directly, or greenlight a pure-SQL fallback) to resume. _(added 2026-08-10)_
- **EQ** · **Live click-through not done** — app can't boot in this sandbox (no network to the canonical config service, even for the demo tenant); verified instead via a standalone harness running the actual edited code plus the full existing test suite (26/26) and eslint. Royce to confirm approved leave now shows on the Calendar page on a real tenant. _(added 2026-08-10)_
- **EQ** · **2 items need Royce's call, not a code fix** — `claude/service-canonical-identity-phase3-4` (eq-service): re-keys shell-auth JWT + remaps 5 SKS users' FK refs, explicitly marked "DO NOT DEPLOY without Royce's go" in its own commit, never landed — still wanted or shelved? `worktree-wf_79f7a4de-c56-4` (eq-intake): the quality-guardian engine is live but no admin UI in eq-service ever surfaced its output — still wanted? _(added 2026-08-08)_
- **EQ** · **Not click-tested live** — EQ Field's CSV import was rewired from destructive (purge+reinsert) to additive (match existing person by phone/email before insert) ([eq-field PR #660](https://github.com/eq-solutions/eq-field/pull/660), merged, live). Needs Royce to re-upload a real SKS person's CSV row and confirm their linked records (timesheets, leave, licences — 6 tables carry a soft `person_id` reference) and id survive the round trip. _(added 2026-08-07)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · Auto-login from Shell's tenant tile into Cards was silently skipping the handoff and bouncing to the sign-in screen instead — reported live by Royce, root-caused same session. `cards.eq.solutions` iframes across every open Shell tab share one browser's local storage, and a refresh-token rotation triggered by one tab invalidates the session another tab still has cached. The splash screen only checked whether *a* session object existed in storage, not whether it was still valid, so a stale cached session silently pre-empted the working handoff. Root-caused live against Royce's own SKS account: PostHog showed `shell_handoff_started` never fired on the failing attempt, and eq-canonical's auth logs showed `403 bad_jwt: invalid claim: missing sub claim` at the same second. Fixed in eq-cards [PR #212](https://github.com/eq-solutions/eq-cards/pull/212) (squash-merged `36a23cd`) — `_handleShellEntry()` now validates any cached session with a live `getUser()` call before trusting it, signing out and falling through to the existing handoff on any failure. Merged and deployed (explicit `Build & Deploy` workflow dispatch — Netlify + Sentry source-map upload both succeeded). **Needs Royce's click-through**: his own browser has a bad session already stuck in local storage from before the fix — clearing site data for `cards.eq.solutions` once (or a private window) and reloading the tenant tile is a device-side action only he can do; confirming the clean auto-login after that is the last open step. _(added 2026-08-04)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
_…and 92 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 3 | 0d |
| eq-solves-intake | ✓ success | 2d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 504](https://eq-solutions.sentry.io/issues/135986280/) | 4 | 2026-08-14 |
| eq-cards | [minified:a42: FunctionException(status: 502, details: {error: anthropic_upstream](https://eq-solutions.sentry.io/issues/140383786/) | 1 | 2026-08-13 |
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-14 | eq-shell | [#1339](https://github.com/eq-solutions/eq-shell/pull/1339) fix(auth): reject self-join when there's no role code and no admi |
| 2026-08-14 | eq-shell | [#1338](https://github.com/eq-solutions/eq-shell/pull/1338) fix(staff): surface documents_not_extracted from ocr-licence's pe |
| 2026-08-14 | eq-shell | [#1336](https://github.com/eq-solutions/eq-shell/pull/1336) fix(shell): stop dashboard scroll chaining into blank body space |
| 2026-08-14 | eq-shell | [#1337](https://github.com/eq-solutions/eq-shell/pull/1337) feat(admin): hard-delete for archived user accounts |
| 2026-08-14 | eq-shell | [#1335](https://github.com/eq-solutions/eq-shell/pull/1335) feat(staff): step through every document found in a multi-card ph |
| 2026-08-14 | eq-solves-service | [#728](https://github.com/eq-solutions/eq-service/pull/728) fix(security): gate remaining /admin/* pages on isAdmin |
| 2026-08-14 | eq-solves-service | [#727](https://github.com/eq-solutions/eq-service/pull/727) fix(actions): extend session-expiry Server Action guard to the re |
| 2026-08-14 | eq-solves-service | [#726](https://github.com/eq-solutions/eq-service/pull/726) fix(archive): restoreEntityAction clears deleted_at for maintenan |
| 2026-08-14 | eq-solves-service | [#725](https://github.com/eq-solutions/eq-service/pull/725) fix(maintenance): surface a clean message on session-expiry Serve |
| 2026-08-14 | eq-field | [#695](https://github.com/eq-solutions/eq-field/pull/695) v3.5.496 — Email Templates pilot: leave.js's 3 templates now DB-e |
| 2026-08-14 | eq-field | [#694](https://github.com/eq-solutions/eq-field/pull/694) v3.5.495 — Teams route guard (deep-link access-control gap) |
| 2026-08-14 | eq-field | [#693](https://github.com/eq-solutions/eq-field/pull/693) supervisor-digest: widen leave lookahead from 1 week to 4, groupe |
| 2026-08-14 | eq-field | [#692](https://github.com/eq-solutions/eq-field/pull/692) v3.5.494 — Leave notification gaps closed; Job Numbers panel fix |
| 2026-08-14 | eq-field | [#691](https://github.com/eq-solutions/eq-field/pull/691) v3.5.493 — FIX: app-state.js cache-buster stuck at v3.5.486 for 6 |
| 2026-08-14 | eq-field | [#690](https://github.com/eq-solutions/eq-field/pull/690) v3.5.492 — Map hover tooltips list people's names |
_Showing 15 of 112 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_
- **Shell's own styling and the shared `@eq-solutions/ui` design library define colliding layout style names** (`eq-hub` and friends) — noticed while fixing the scroll bug above, not the cause of it, not yet looked into properly. _(added 2026-08-14)_
- **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_
- **Minor, unrelated gap noticed in passing**: `admin.deactivate_user` is declared in the permission matrix but never actually checked anywhere — `edit-user.ts`'s archive/restore action (and now `delete-user.ts`) both gate on `admin.edit_user` instead. Harmless today since the two keys are granted to the same roles, but if they're ever meant to diverge, deactivate silently wouldn't. _(added 2026-08-14)_
- **No manual browser smoke test yet** — need to actually expire a session mid-form-submit on a few touched pages and confirm the friendly "sign in again" message renders, rather than just type/unit verification. _(added 2026-08-14)_
- **No automated check exists to catch this cache-tag class of bug before it ships** — found and fixed the symptom 4 times now (this session + 3 historical), never built the actual guard. Worth a CI check that flags a cache-busted file whose content changed but whose version tag didn't. _(added 2026-08-14)_
- **Not click-tested live** — this sandbox has no network path to the real app (confirmed again this session), so the Map page's hover behaviour and the version-badge fix are verified by direct database/production-file checks only, not by clicking through a real signed-in session. _(added 2026-08-14)_
- **New request, in progress**: audit the whole leave-approval email/digest wiring (frequency, templates) — an executive wasn't notified when leave was approved. Also simplify the CC-list modal's copy (currently references "v3.5.384" directly, too technical for a user-facing surface). _(added 2026-08-14)_
- "View" on a document is still 2 network hops end-to-end (the server call, then a separate Storage signed-URL call) — only the first hop's 2-sequential-query inefficiency was fixed this session (PostgREST embed over an existing FK, `document-signoffs.js`). _(added 2026-08-13)_
- **Not click-tested on a real phone** — same sandbox limitation as other recent mobile fixes (no path to complete the Shell-iframe auth handoff here). Verified instead via `tsc --noEmit` (clean) and a static Tailwind-class repro at 375px sent directly to Royce, plus confirming the live Netlify production deploy matches the merge commit. _(added 2026-08-13)_
_…and 492 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
- **Leave sync parked deliberately** — an imported leave code lands on `schedule_entries.leave_type` directly, not in `app_data.leave_requests`, so it displays but carries no approver/audit trail. Royce explicitly scoped this session to roster only; leave is its own future task. _(added 2026-08-14)_
- **`SKS-FIELD-PARALLEL-RUN-LOG.md` and the "EQ Field parallel-run restarted" entry below are now stale** — both assume manual entry hadn't started; live data shows it has, informally. Worth a proper reconcile pass — out of scope for this session's /close. _(added 2026-08-14)_
- **Optional code fix, not required**: the roster site-map query in `eq-field/scripts/supabase.js` (~line 992) filters on `active=eq.true` only, not `field_enabled` — a small latent gap (found live) unrelated to the SYD27/EC6 fix above; deactivating the stale rows sidesteps it, so this is cosmetic cleanup only if ever revisited. _(added 2026-08-14)_
- **Richard needs to re-add his LV Rescue photo** — none of the 6 attempts ever actually captured one; the surviving row has the licence details but no photo. _(added 2026-08-13)_
- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
_…and 72 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3502 | 607 | 98 | 24 |
| [SKS](sks/pending.md) | 438 | 89 | 4 | 15 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 0 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-14 | [SKS → EQ Field weekly roster CSV sync: investigated live, confirmed feasible with zero new code](sessions/2026-08-14.md) |
| 2026-08-13 | [eq-shell PR #1316: misdiagnosed build error, real cause was a pdfjs-dist v6 type break, fixed + merged + deployed clean](sessions/2026-08-13.md) |
| 2026-08-12 | [EQ UI design sprint (EmptyState, density mode, DateRangePicker) shipped and rolled out to eq-shell + eq-service](sessions/2026-08-12.md) |
| 2026-08-11 | [EQ Cards: removed dead CardScreen (710 lines), merged live](sessions/2026-08-11.md) |
| 2026-08-10 | [Delete an approved leave request (SKS), then found + fixed a live Calendar regression in EQ Field](sessions/2026-08-10.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-14 07:51 UTC._

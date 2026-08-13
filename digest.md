---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-13
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-13 06:25 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-13 06:04 UTC → 2026-08-13 06:25 UTC)

- Merged: eq-shell [#1324](https://github.com/eq-solutions/eq-shell/pull/1324) feat(staff): swap Resourcing desktop view to eq-ui Table
- Merged: eq-shell [#1315](https://github.com/eq-solutions/eq-shell/pull/1315) chore(deps): bump @eq-solutions/ui to v1.15.0
- Merged: eq-shell [#1313](https://github.com/eq-solutions/eq-shell/pull/1313) fix(staff): move labour-hire intake from platform to tenant 
- Merged: eq-shell [#1312](https://github.com/eq-solutions/eq-shell/pull/1312) fix(auth): mint-tenant-jwt.ts never embedded extra_perms — s
- Merged: eq-shell [#1311](https://github.com/eq-solutions/eq-shell/pull/1311) feat(staff): resourcing dashboard + draft org chart
- Merged: eq-shell [#1308](https://github.com/eq-solutions/eq-shell/pull/1308) docs(ci): field-perms-drift's setup note is stale, secret no
- Merged: eq-shell [#1306](https://github.com/eq-solutions/eq-shell/pull/1306) fix(ops): file uploads failed with a fake "check your connec
- Merged: eq-shell [#1304](https://github.com/eq-solutions/eq-shell/pull/1304) fix(security): RLS gate on staff_conversations now enforces 

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-cards` [minified:a2T: InvalidStateError: The source image could not ](https://eq-solutions.sentry.io/issues/140383785/)
- 🟠 **Cron failing** — `index-drift.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-11 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (106)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Needs Royce, not more building:** already superseded below (2026-08-11 explicit go-ahead) for the overseas-goal exclusion specifically — the real remaining blocker is operational: generate + set `EQ_CARDS_HANDOFF_KEY` on both Netlify projects (nothing works until it exists) — manual-hands-only, Claude Code is blocked from writing Netlify secrets by design. **Note 2026-08-13:** the TODAY.md overseas goal this entry originally cited was killed (Royce's explicit call) — doesn't change anything here, the Netlify-secret step was already the actual blocker, not the goal. _(added 2026-08-10)_
- **EQ** · **Not built.** Royce to decide whether this graduates back onto `system/punch-list.md` for the actual simplification work, given the goal's current exclusion on live UI changes affecting real users while overseas. _(added 2026-08-10)_
- **EQ** · **Migration 0206 not yet applied to the live database** — merged to code, needs Royce to manually dispatch `apply-service-migrations.yml`; Claude Code's own permission classifier blocks doing that directly (same wall as the Netlify secret above). _(added 2026-08-11)_
- **EQ** · **Work sits uncommitted, not lost** — on branch `fix/integration-ci-app-data-bootstrap` in the shared root checkout at `C:\Projects\eq-solves-service`. Needs Royce to get Docker running (or hand over a `supabase db dump` directly, or greenlight a pure-SQL fallback) to resume. _(added 2026-08-10)_
- **EQ** · **Live click-through not done** — app can't boot in this sandbox (no network to the canonical config service, even for the demo tenant); verified instead via a standalone harness running the actual edited code plus the full existing test suite (26/26) and eslint. Royce to confirm approved leave now shows on the Calendar page on a real tenant. _(added 2026-08-10)_
- **EQ** · **2 items need Royce's call, not a code fix** — `claude/service-canonical-identity-phase3-4` (eq-service): re-keys shell-auth JWT + remaps 5 SKS users' FK refs, explicitly marked "DO NOT DEPLOY without Royce's go" in its own commit, never landed — still wanted or shelved? `worktree-wf_79f7a4de-c56-4` (eq-intake): the quality-guardian engine is live but no admin UI in eq-service ever surfaced its output — still wanted? _(added 2026-08-08)_
- **EQ** · **Not click-tested live** — EQ Field's CSV import was rewired from destructive (purge+reinsert) to additive (match existing person by phone/email before insert) ([eq-field PR #660](https://github.com/eq-solutions/eq-field/pull/660), merged, live). Needs Royce to re-upload a real SKS person's CSV row and confirm their linked records (timesheets, leave, licences — 6 tables carry a soft `person_id` reference) and id survive the round trip. _(added 2026-08-07)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · Auto-login from Shell's tenant tile into Cards was silently skipping the handoff and bouncing to the sign-in screen instead — reported live by Royce, root-caused same session. `cards.eq.solutions` iframes across every open Shell tab share one browser's local storage, and a refresh-token rotation triggered by one tab invalidates the session another tab still has cached. The splash screen only checked whether *a* session object existed in storage, not whether it was still valid, so a stale cached session silently pre-empted the working handoff. Root-caused live against Royce's own SKS account: PostHog showed `shell_handoff_started` never fired on the failing attempt, and eq-canonical's auth logs showed `403 bad_jwt: invalid claim: missing sub claim` at the same second. Fixed in eq-cards [PR #212](https://github.com/eq-solutions/eq-cards/pull/212) (squash-merged `36a23cd`) — `_handleShellEntry()` now validates any cached session with a live `getUser()` call before trusting it, signing out and falling through to the existing handoff on any failure. Merged and deployed (explicit `Build & Deploy` workflow dispatch — Netlify + Sentry source-map upload both succeeded). **Needs Royce's click-through**: his own browser has a bad session already stuck in local storage from before the fix — clearing site data for `cards.eq.solutions` once (or a private window) and reloading the tenant tile is a device-side action only he can do; confirming the clean auto-login after that is the last open step. _(added 2026-08-04)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
_…and 94 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 3 | 1d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 1 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 1](https://eq-solutions.sentry.io/issues/138175643/) | 9 | 2026-08-12 |
| eq-cards | [minified:a2T: InvalidStateError: The source image could not be decoded.](https://eq-solutions.sentry.io/issues/140383785/) | 7 | 2026-08-13 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/139929381/) | 4 | 2026-08-10 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-shell | [Error: events GET 500: Error - Request ID: 01KZPVXME1ZW9F7NMD4TDF2CDF](https://eq-solutions.sentry.io/issues/139586029/) | 2 | 2026-08-10 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 2 | 2026-08-07 |
| eq-shell | [TimeoutError: The operation was aborted due to timeout](https://eq-solutions.sentry.io/issues/138753891/) | 2 | 2026-08-04 |
| eq-field | [Error: Can't read the data of 'word/media/eq-logo.png'. Is it in a supported Jav](https://eq-solutions.sentry.io/issues/138623165/) | 2 | 2026-08-04 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-13 | eq-shell | [#1324](https://github.com/eq-solutions/eq-shell/pull/1324) feat(staff): swap Resourcing desktop view to eq-ui Table |
| 2026-08-13 | eq-solves-service | [#714](https://github.com/eq-solutions/eq-service/pull/714) docs(security): document entity.view_pii as investigated + delibe |
| 2026-08-13 | eq-solves-service | [#713](https://github.com/eq-solutions/eq-service/pull/713) fix(security): wire entity.edit + entity.manage_activation; corre |
| 2026-08-13 | eq-solves-service | [#711](https://github.com/eq-solutions/eq-service/pull/711) security: remove orphaned customer/site write REST routes |
| 2026-08-13 | eq-solves-service | [#708](https://github.com/eq-solutions/eq-service/pull/708) fix(security): close assignee-bypass on close + status-setter byp |
| 2026-08-13 | eq-field | [#686](https://github.com/eq-solutions/eq-field/pull/686) chore(tests): tighten permission-enforcement-drift baseline post- |
| 2026-08-13 | eq-cards | [#230](https://github.com/eq-solutions/eq-cards/pull/230) fix(security): close cross-org IDOR on worker/credential admin wr |
| 2026-08-13 | eq-cards | [#229](https://github.com/eq-solutions/eq-cards/pull/229) fix(licences): stop a failed photo/document step from duplicating |
| 2026-08-13 | eq-cards | [#228](https://github.com/eq-solutions/eq-cards/pull/228) fix(ocr): raise client OCR timeout to 25s so it doesn't undercut  |
| 2026-08-12 | eq-shell | [#1322](https://github.com/eq-solutions/eq-shell/pull/1322) chore(security): permission-enforcement drift guard (ratchet, non |
| 2026-08-12 | eq-shell | [#1323](https://github.com/eq-solutions/eq-shell/pull/1323) fix(staff): thread licence_verifications through the invite-path  |
| 2026-08-12 | eq-shell | [#1321](https://github.com/eq-solutions/eq-shell/pull/1321) feat(staff): write path for team/supervisor assignment on the org |
| 2026-08-12 | eq-shell | [#1318](https://github.com/eq-solutions/eq-shell/pull/1318) fix(security): gate audit rollback + align entity archive/restore |
| 2026-08-12 | eq-shell | [#1316](https://github.com/eq-solutions/eq-shell/pull/1316) feat(staff): create one credential per document, not per photo |
| 2026-08-12 | eq-shell | [#1320](https://github.com/eq-solutions/eq-shell/pull/1320) feat(ops): bulk select in Archived tab (restore / delete multiple |
_Showing 15 of 95 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **PR #1310 not yet verified or merged** — Royce reported issues testing it. Checked live and ruled out: the storage system's cross-origin access rules, and whether the new code actually deployed (both fine). The actual failure is still unidentified — waiting on the specific error message/network response before it can be diagnosed further. _(added 2026-08-12)_
- **Live click-test still not done anywhere across this whole thread** — every fix above was verified against live data/CI/direct database checks, never a real signed-in click-through session on any of the four apps. _(added 2026-08-13)_
- **Live click-through not done** — this sandbox has no network path to the tenant-config service, so the Archived-tab search/filter/bulk-select hasn't been visually confirmed in a real browser session. Built against the exact same Table component already proven live elsewhere in the app; build + typecheck clean on both PRs. _(added 2026-08-12)_
- **Live click-through not done** — this sandbox has no network path to the tenant-config service, so the Archived-tab search/filter/bulk-select hasn't been visually confirmed in a real browser session. Built against the exact same Table component already proven live elsewhere in the app; build + typecheck clean on both PRs. _(added 2026-08-12)_
- **Richard Brown needs to re-add his LV Rescue (C40385) photo** — the surviving row has the correct licence details but no photo attached; nothing existed anywhere to recover. The fix means his retry will now update that row cleanly instead of duplicating again. _(added 2026-08-13)_
- **Live click-through still not done** on the multi-document extraction / PDF preview / flag-notification features — verified via CI + direct DB checks only, no real signed-in session. _(added 2026-08-13)_
- **SMS-notification coverage is inconsistent across the different invite paths** — flagged during the original audit, not touched this session. _(added 2026-08-13)_
- **Intake engine's CSV import path bypasses the same-worker dedup** the direct upload paths now go through — flagged, not touched. _(added 2026-08-13)_
- **Dead code**: `eq_cards_find_invites_by_phone` RPC and `ClaimByPhoneScreen` appear unused since the "Find my company account" flow replaced join-by-code — not confirmed dead, not removed. _(added 2026-08-13)_
- **Open question, not decided**: should the manual labour-hire-document-upload form and the regular worker-invite form (which now also accepts documents) eventually merge into one? Deliberately left as two separate entry points this session. _(added 2026-08-13)_
_…and 487 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Richard needs to re-add his LV Rescue photo** — none of the 6 attempts ever actually captured one; the surviving row has the licence details but no photo. _(added 2026-08-13)_
- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
_…and 67 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3402 | 600 | 64 | 17 |
| [SKS](sks/pending.md) | 423 | 85 | 3 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 0 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-13 | [eq-shell: invite-path approval was silently dropping flagged licences, fixed + merged + deployed](sessions/2026-08-13.md) |
| 2026-08-12 | [EQ UI design sprint (EmptyState, density mode, DateRangePicker) shipped and rolled out to eq-shell + eq-service](sessions/2026-08-12.md) |
| 2026-08-11 | [EQ Cards: removed dead CardScreen (710 lines), merged live](sessions/2026-08-11.md) |
| 2026-08-10 | [Delete an approved leave request (SKS), then found + fixed a live Calendar regression in EQ Field](sessions/2026-08-10.md) |
| 2026-08-08 | [eq-field CSV import permission gap: found, fixed, merged, deployed](sessions/2026-08-08.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-13 06:25 UTC._

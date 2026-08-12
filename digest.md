---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-12
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-12 06:34 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-12 06:30 UTC → 2026-08-12 06:34 UTC)

- Merged: eq-shell [#1319](https://github.com/eq-solutions/eq-shell/pull/1319) feat(ops): archive view search/filter + auto-archive invoice
- Merged: eq-shell [#1305](https://github.com/eq-solutions/eq-shell/pull/1305) fix(dashboard): on-leave count zeroed by overnight schema re
- Merged: eq-shell [#1303](https://github.com/eq-solutions/eq-shell/pull/1303) fix(dashboard): logo, outstanding-quotes value, on-leave cou
- Merged: eq-shell [#1301](https://github.com/eq-solutions/eq-shell/pull/1301) fix(dashboard): mobile hero card was display:none on every v
- Merged: eq-shell [#1300](https://github.com/eq-solutions/eq-shell/pull/1300) Make the mobile hero stats actionable, not just informationa
- Merged: eq-shell [#1298](https://github.com/eq-solutions/eq-shell/pull/1298) Add compact action cards to the mobile dashboard
- Merged: eq-shell [#1296](https://github.com/eq-solutions/eq-shell/pull/1296) fix(platform): link labour-hire intake tool from platform na
- Merged: eq-shell [#1293](https://github.com/eq-solutions/eq-shell/pull/1293) feat(staff): multi-file OCR intake, shared between admin inv

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/139929381/)
- 🟠 **Sentry new error** — `eq-cards` [minified:C4: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)

## 🙋 Waiting on you (106)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Needs Royce, not more building:** merge/deploy waits until he's back (2026-08-22) or explicitly comfortable being reachable if it needs a fast revert — same standing hold as any auth-path change per CLAUDE.md, made explicit here because of the overseas goal specifically. Also still needed regardless of timing: generate + set `EQ_CARDS_HANDOFF_KEY` on both Netlify projects (nothing works until it exists) — manual-hands-only, Claude Code is blocked from writing Netlify secrets by design. _(added 2026-08-10)_
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
| eq-shell | ✓ success | 0d ago | 6 | 0d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 5 | 2026-08-09 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/139929381/) | 4 | 2026-08-10 |
| eq-cards | [minified:C4: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-08-10 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-shell | [Error: events GET 500: Error - Request ID: 01KZPVXME1ZW9F7NMD4TDF2CDF](https://eq-solutions.sentry.io/issues/139586029/) | 2 | 2026-08-10 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 2 | 2026-08-07 |
| eq-shell | [TimeoutError: The operation was aborted due to timeout](https://eq-solutions.sentry.io/issues/138753891/) | 2 | 2026-08-04 |
| eq-field | [Error: Can't read the data of 'word/media/eq-logo.png'. Is it in a supported Jav](https://eq-solutions.sentry.io/issues/138623165/) | 2 | 2026-08-04 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-12 | eq-shell | [#1319](https://github.com/eq-solutions/eq-shell/pull/1319) feat(ops): archive view search/filter + auto-archive invoiced quo |
| 2026-08-12 | eq-shell | [#1311](https://github.com/eq-solutions/eq-shell/pull/1311) feat(staff): resourcing dashboard + draft org chart |
| 2026-08-12 | eq-shell | [#1314](https://github.com/eq-solutions/eq-shell/pull/1314) fix(staff): surface multi-document warning on the regular invite  |
| 2026-08-12 | eq-shell | [#1315](https://github.com/eq-solutions/eq-shell/pull/1315) chore(deps): bump @eq-solutions/ui to v1.15.0 |
| 2026-08-12 | eq-shell | [#1313](https://github.com/eq-solutions/eq-shell/pull/1313) fix(staff): move labour-hire intake from platform to tenant scope |
| 2026-08-12 | eq-shell | [#1312](https://github.com/eq-solutions/eq-shell/pull/1312) fix(auth): mint-tenant-jwt.ts never embedded extra_perms — staff_ |
| 2026-08-12 | eq-shell | [#1308](https://github.com/eq-solutions/eq-shell/pull/1308) docs(ci): field-perms-drift's setup note is stale, secret now exi |
| 2026-08-12 | eq-shell | [#1307](https://github.com/eq-solutions/eq-shell/pull/1307) fix(ops): file uploads failing on a payload limit no function cou |
| 2026-08-12 | eq-shell | [#1306](https://github.com/eq-solutions/eq-shell/pull/1306) fix(ops): file uploads failed with a fake "check your connection" |
| 2026-08-12 | eq-solves-service | [#707](https://github.com/eq-solutions/eq-service/pull/707) fix(security): enforce reports.view + audit.view role gates |
| 2026-08-12 | eq-solves-service | [#706](https://github.com/eq-solutions/eq-service/pull/706) chore(deps): bump @eq-solutions/ui to v1.15.0 |
| 2026-08-12 | eq-solves-service | [#697](https://github.com/eq-solutions/eq-service/pull/697) chore(deps): bump @eq-solutions/ui to v1.14.0 |
| 2026-08-12 | eq-field | [#682](https://github.com/eq-solutions/eq-field/pull/682) v3.5.486 — mobile: Teams drawer highlight, voice-mic tap targets  |
| 2026-08-12 | eq-field | [#681](https://github.com/eq-solutions/eq-field/pull/681) v3.5.485 — mobile: Calendar agenda-list view + bottom-sheet day d |
| 2026-08-12 | eq-field | [#680](https://github.com/eq-solutions/eq-field/pull/680) v3.5.484 — mobile: Safety count louder, Leave tap-target fix |
_Showing 15 of 83 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **PR #683 needs a live click-test (manager/supervisor/employee) before merge** — this sandbox has no network path to the tenant-config service (punch-list item #3), so the app can't fully boot here. _(added 2026-08-12)_
- **PR #683 merge/deploy** — held pending Royce's explicit go-ahead, per the standing auth-change rule and the active TODAY.md constraint (expires 2026-08-22). _(added 2026-08-12)_
- **Outcome of the two spawned background tasks** (`task_de667109` EQ Service, `task_fd65aa59` EQ Shell) — still running as of this close. _(added 2026-08-12)_
- **Timesheets mobile-entry** — deliberately not touched (Royce: "timesheets aren't a priority on mobile"). Revisit only if there's a real reason to think people are trying to do timesheets on their phone (e.g. PostHog `timesheet_saved` event breakdown by device). _(added 2026-08-12)_
- Inline-edit primitives for Table — still deferred, needs its own spike on whether Table's cell/row model can support it cleanly; `Table.tsx` is already 1,265 lines. _(added 2026-08-12)_
- Whether Table's own column filters should ever be rebuilt on top of the new `MultiSelect` component — low priority, only worth revisiting if the inline-edit spike above happens anyway and touches the same filter code. Not blocking anything; `MultiSelect` shipped standalone (eq-ui PR [#38](https://github.com/eq-solutions/eq-ui/pull/38)) specifically so it didn't have to wait on this. _(added 2026-08-12)_
- **Mobile action cards are view + tap-through only** — no mark-done/dismiss controls, a deliberate v1 simplicity choice (confirmed via AskUserQuestion). Add if Royce wants parity with desktop. _(added 2026-08-11)_
- **Compliance click-through only covers Staff and Ops today.** EQ Field has no record-level deep-linking (only `?tab=`), EQ Service has an unused `?return=` path mechanism Shell never constructs a specific path for, and EQ Cards has no deep-link support at all — out of scope for this pass since it wasn't asked for, but the next domain to add if Ask Anything grows past licences/quotes. _(added 2026-08-11)_
- **Tab-deeplink click-through still not explicitly confirmed.** Logo and Outstanding-quotes drew no complaint on the next phone check (implicitly fine); On-leave was reported broken and is now re-fixed (see the 2026-08-12 entry below) — but nobody has explicitly confirmed tapping "On leave" actually lands on Field's Leave tab. _(added 2026-08-12, carried from 2026-08-11)_
- **Not checked: does the same schedule_entries-vs-leave_requests gap affect desktop's "Crew you can deploy" capacity numbers?** `computeCrewWindow`'s `on_leave`/`deployable` math (used by `SignalsBoard` on both desktop and mobile) was deliberately left untouched — verified correct for what it represents (capacity, not headcount) — but it's still sourced from `schedule_entries`, which isn't kept in sync with `leave_requests` approvals. _(added 2026-08-11)_
_…and 473 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
_…and 66 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3284 | 584 | 32 | 12 |
| [SKS](sks/pending.md) | 418 | 84 | 2 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 0 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-12 | [EQ UI design sprint (EmptyState, density mode, DateRangePicker) shipped and rolled out to eq-shell + eq-service](sessions/2026-08-12.md) |
| 2026-08-11 | [EQ Cards: removed dead CardScreen (710 lines), merged live](sessions/2026-08-11.md) |
| 2026-08-10 | [Delete an approved leave request (SKS), then found + fixed a live Calendar regression in EQ Field](sessions/2026-08-10.md) |
| 2026-08-08 | [eq-field CSV import permission gap: found, fixed, merged, deployed](sessions/2026-08-08.md) |
| 2026-08-07 | [My Schedule maps link: the real root cause was Shell's iframe sandbox, not iOS](sessions/2026-08-07.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-12 06:34 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-08
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-08 05:05 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-08 04:40 UTC → 2026-08-08 05:05 UTC)

- Merged: eq-shell [#1288](https://github.com/eq-solutions/eq-shell/pull/1288) fix(deps): patch image-size DoS + re-vendor to restore the n
- Merged: eq-shell [#1281](https://github.com/eq-solutions/eq-shell/pull/1281) feat(access-control): expose eq-field's 74 fine-grained perm
- Merged: eq-solves-service [#692](https://github.com/eq-solutions/eq-service/pull/692) fix(testing): assignee picker empty on ACB/NSX Create Check
- Merged: eq-field [#662](https://github.com/eq-solutions/eq-field/pull/662) fix(roles): vendor verify-pin.js's role list, log the silent
- Merged: eq-solves-intake [#114](https://github.com/eq-solutions/eq-solves-intake/pull/114) fix(deps): bump nanoid to close GHSA-qrpm-p2h7-hrv2
- Merged: eq-solves-intake [#113](https://github.com/eq-solutions/eq-solves-intake/pull/113) feat(intake): export dice/identityKeyFor/HIGH_SIM from the p
- Merged: eq-solves-intake [#111](https://github.com/eq-solutions/eq-solves-intake/pull/111) feat(intake): polish the Overview/To Do data-cleaning flow
- Merged: eq-solves-intake [#110](https://github.com/eq-solutions/eq-solves-intake/pull/110) fix(scripts): hard-stop migrate-cards-to-canonical.mjs rathe

## ⚠ Needs you (2)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (109)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **2 items need Royce's call, not a code fix** — `claude/service-canonical-identity-phase3-4` (eq-service): re-keys shell-auth JWT + remaps 5 SKS users' FK refs, explicitly marked "DO NOT DEPLOY without Royce's go" in its own commit, never landed — still wanted or shelved? `worktree-wf_79f7a4de-c56-4` (eq-intake): the quality-guardian engine is live but no admin UI in eq-service ever surfaced its output — still wanted? _(added 2026-08-08)_
- **EQ** · **Direct DDL apply blocked twice by the Claude Code permission classifier** (same class of restriction as Netlify security-setting edits) — needs Royce's own hands via the Supabase SQL editor on `ehow` (`ehowgjardagevnrluult`), or fixing the false ledger row so the normal governed pipeline picks it up, or a permission rule change. Exact SQL is the migration file verbatim — ready to paste. _(added 2026-08-08)_
- **EQ** · **Not click-tested live** — EQ Field's CSV import was rewired from destructive (purge+reinsert) to additive (match existing person by phone/email before insert) ([eq-field PR #660](https://github.com/eq-solutions/eq-field/pull/660), merged, live). Needs Royce to re-upload a real SKS person's CSV row and confirm their linked records (timesheets, leave, licences — 6 tables carry a soft `person_id` reference) and id survive the round trip. _(added 2026-08-07)_
- **EQ** · **Not yet confirmed on a real device through Core that the maps link now opens.** Three attempts: v3.5.460 (eq-field #655) dropped `target="_blank"` for iOS standalone; v3.5.465 (eq-field #659) switched to Apple's `maps://` scheme — both real, defensible fixes for genuine standalone-PWA use, but Royce's actual test was always through Core (`core.eq.solutions/sks/field`), where neither could work. The real cause: `FieldIframe.tsx`'s iframe `sandbox` attribute never included `allow-popups`, so **any** `target="_blank"` link or `window.open()` inside Field, Service, or Cards was silently blocked whenever accessed through Shell — on any device, not iOS-specific. Fixed for all three apps (eq-shell [#1268](https://github.com/eq-solutions/eq-shell/pull/1268), merged, live on `core.eq.solutions`). Royce to confirm the maps icon now actually opens Maps when accessed through Core. _(added 2026-08-05, updated 2026-08-06)_
- **EQ** · **Royce to confirm the SKS dashboard loads cleanly** — needs an authenticated session, off-limits for Claude to drive. _(added 2026-08-05)_
- **EQ** · **Not click-tested live by a real signed-in user** — everything above was verified at the function level and via the deploy preview's boot path, not by an authenticated session actually seeing the widget populate with real people. Royce to confirm on `field.eq.solutions` (or the Shell embed) that Birthdays & Anniversaries now shows up reliably from a fresh Dashboard landing. _(added 2026-08-05)_
- **EQ** · **Neither fix has been click-tested live** — Royce to confirm: (1) the address fields save and display correctly on a real staff member, desktop and mobile, (2) re-downloading William's compliance pack now shows "William Hong" instead of "Unknown." _(added 2026-08-05)_
- **EQ** · **Not click-tested live** — Royce to confirm a real future-dated new starter actually disappears from the roster/dispatch/timesheets and shows up correctly in the new Starting Soon widget. _(added 2026-08-05)_
- **EQ** · **None of the four PDF-import/pricing-table changes above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle on the main "From PDF" button — especially that a real sell-priced supplier PDF now computes cost correctly, and the default Cost path is unchanged, (4) the *same* toggle now also appearing on the second "Import from PDF" button inside the New Quote form when a document has ambiguous pricing. _(added 2026-08-05, updated 2026-08-05)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
_…and 97 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 0d ago | 5 | 4d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 2d ago | 1 | 0d |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 2](https://eq-solutions.sentry.io/issues/138175643/) | 6 | 2026-08-07 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 4 | 2026-08-05 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-field | [ReferenceError: openTafeHolidaysConfig is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 3 | 2026-07-28 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 2 | 2026-08-07 |
| eq-shell | [Error: eq-ops rpc eq_delete_quote failed: quote not found or access denied](https://eq-solutions.sentry.io/issues/139309419/) | 2 | 2026-08-06 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-08 | eq-shell | [#1288](https://github.com/eq-solutions/eq-shell/pull/1288) fix(deps): patch image-size DoS + re-vendor to restore the nanoid |
| 2026-08-08 | eq-shell | [#1287](https://github.com/eq-solutions/eq-shell/pull/1287) refactor(customers): reuse @eq/intake's fuzzy matcher instead of  |
| 2026-08-08 | eq-shell | [#1286](https://github.com/eq-solutions/eq-shell/pull/1286) fix(deps): resolve 2 high-severity Dependabot alerts (js-yaml, br |
| 2026-08-08 | eq-shell | [#1285](https://github.com/eq-solutions/eq-shell/pull/1285) fix(ci): field-perms-drift skips cleanly until FIELD_PERMS_DRIFT_ |
| 2026-08-08 | eq-solves-service | [#692](https://github.com/eq-solutions/eq-service/pull/692) fix(testing): assignee picker empty on ACB/NSX Create Check |
| 2026-08-08 | eq-field | [#673](https://github.com/eq-solutions/eq-field/pull/673) docs: mandate worktree isolation in the deploy flow |
| 2026-08-08 | eq-field | [#672](https://github.com/eq-solutions/eq-field/pull/672) fix(managers): gate Supervision CSV import behind isManager (v3.5 |
| 2026-08-08 | eq-field | [#671](https://github.com/eq-solutions/eq-field/pull/671) v3.5.471 — fix(mobile): isManagerSession() read window.isManager, |
| 2026-08-08 | eq-field | [#670](https://github.com/eq-solutions/eq-field/pull/670) v3.5.469 — Data tab: gate People/Sites/Schedule CSV import behind |
| 2026-08-08 | eq-field | [#669](https://github.com/eq-solutions/eq-field/pull/669) fix(apprentices): Skills Passport mobile CSS selector was dead (v |
| 2026-08-08 | eq-field | [#668](https://github.com/eq-solutions/eq-field/pull/668) fix(mobile): 5 confirmed mobile.css bugs (v3.5.469) |
| 2026-08-08 | eq-field | [#667](https://github.com/eq-solutions/eq-field/pull/667) fix(safety): gate incident records/export to Supervision (v3.5.46 |
| 2026-08-08 | eq-field | [#666](https://github.com/eq-solutions/eq-field/pull/666) v3.5.469 — Calibration + Projects had no mobile nav path |
| 2026-08-08 | eq-field | [#665](https://github.com/eq-solutions/eq-field/pull/665) fix(sign-documents): mobile UX — signature pad size, popup-blocke |
| 2026-08-08 | eq-field | [#664](https://github.com/eq-solutions/eq-field/pull/664) fix(leave): mobile responsive breakpoint for worker balance cards |
_Showing 15 of 33 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **5 open Dependabot PRs on eq-service** never reviewed (vitejs/plugin-react, sentry/nextjs, react-dom, eslint-config-next, @eq-solutions packages) — surfaced as "KEEP" by the branch audit since they're genuinely unmerged, not stale. _(added 2026-08-08)_
- **Structural risk, not a branch problem**: this session hit the shared-non-worktree-root collision the eq-field entry below (2026-08-08) already flagged — two concurrent sessions both doing git work directly in `C:\Projects\eq-shell` (not a worktree) at the same time. Caught before any damage. A second instance hit `eq-context` itself mid-close (this file, twice) — see `eq-context-shared-checkout-contention` memory; fixed by switching to an isolated worktree + direct `push origin HEAD:main` for this close. _(added 2026-08-08)_
- **Not click-tested live** — local dev server hung on an unrelated issue during the fix session. Needs a quick manual pass on ACB and NSX Create Check to confirm the dropdown actually populates in the browser. _(added 2026-08-08)_
- **Migration `0140_harden_next_variation_number.sql` was never actually applied to ehow**, despite being merged to main since 2026-07-03 (PR #321) — its ledger row (`service._eq_migrations`) was falsely marked "applied" by the one-time 2026-07-03 grandfather backfill (`checksum: null, applied_by: 'backfill-2026-07-03'`), so the governed pipeline's own runner thinks it's done and will silently skip it on every future dispatch. Live right now: the RPC still has its old 2-arg signature (`p_tenant_id uuid, p_year integer`), EXECUTE-granted to `authenticated` — any logged-in user, any tenant, can call it directly with someone else's tenant UUID and enumerate that tenant's variation-number sequence.
- **image-size (2 alerts left open)** — ICNS + JXL/HEIF parser infinite-loop DoS. No upstream fix exists yet: comes in via `@netlify/blobs`→`@netlify/dev-utils`, and even `@netlify/dev-utils@latest` (4.4.7) still requires the vulnerable `image-size@^2.0.2`. Nothing to bump until Netlify ships a patch. _(added 2026-08-08)_
- **nanoid re-vendor gap** — the fix above was also hand-patched into the vendored `eq-intake/eq-platform/pnpm-lock.yaml` to close a duplicate alert GitHub was scanning on that file, but that lockfile isn't actually consumed by eq-shell's build (only `eq-intake/eq-platform/packages/*` are real pnpm workspace members). The patch is cosmetic only — the durable fix belongs in the `eq-solves-intake` source repo, then flows back in on the next re-vendor. Spun off as a background task (not duplicated here). _(added 2026-08-08)_
- **Stale substrate claim found, not yet corrected** — the 2026-07-28 "full Dependabot sweep" entry below says the leftover `brace-expansion` DoS in the exceljs→archiver→glob@7→minimatch@3.1.5 chain has "only one full fix: a minimatch major bump," deliberately left unfixed. Live check this session (`pnpm why brace-expansion`) shows that chain already resolves to `1.1.18` via a `brace-expansion@1: ^1.1.17` override — which the GHSA advisories confirm is itself a fully patched version, no minimatch bump needed. Left that old entry untouched (out of this session's scope to edit) but flagging for someone to re-verify and close it out. _(added 2026-08-08)_
- **`FIELD_PERMS_DRIFT_PAT` secret still needs creating** — fine-grained PAT, `Contents:read` on eq-field only, add as an eq-shell repo secret. Royce: "I can't do the secret now." Until it exists the drift-guard above stays a no-op (green, but not actually checking anything). _(added 2026-08-08)_
- **No live click-through yet** on any of the Shell↔Field permission changes above — needs a real signed-in session, off-limits to this environment. _(added 2026-08-08)_
- **EQ-SHELL-Y (ocr-licence 401)** — not an eq-shell code bug; the licence-photo-reading feature occasionally fails a permission check talking to eq-canonical. Someone already patched the underlying cause elsewhere (~5 Aug) and it's been quiet since, but needs a few more quiet days before marking resolved for good. _(added 2026-08-07)_
_…and 451 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
_…and 66 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3262 | 565 | 59 | 12 |
| [SKS](sks/pending.md) | 404 | 82 | 0 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 409 | 37 | 2 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-08 | [eq-field CSV import permission gap: found, fixed, merged, deployed](sessions/2026-08-08.md) |
| 2026-08-07 | [My Schedule maps link: the real root cause was Shell's iframe sandbox, not iOS](sessions/2026-08-07.md) |
| 2026-08-06 | [Document sign-off register: real vision from Royce, two trust gaps fixed](sessions/2026-08-06.md) |
| 2026-08-06 | [c — My Schedule maps link, part two: tap-vs-long-press on iOS standalone](sessions/2026-08-06-c.md) |
| 2026-08-05 | [Tenant-rule audit extended to eq-cards + eq-solves-intake, all 4 PRs merged and live](sessions/2026-08-05.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-08 05:05 UTC._

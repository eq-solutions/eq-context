---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-08
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-08 02:01 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-08 02:01 UTC → 2026-08-08 02:01 UTC)

- Merged: eq-field [#669](https://github.com/eq-solutions/eq-field/pull/669) fix(apprentices): Skills Passport mobile CSS selector was de
- Merged: eq-cards [#198](https://github.com/eq-solutions/eq-cards/pull/198) feat(wallet): Show mode — offline fullscreen ID display for 
- Merged: eq-solves-intake [#108](https://github.com/eq-solutions/eq-solves-intake/pull/108) build(platform): narrow check:packages, wire in verified tes
- Merged: eq-solves-intake [#105](https://github.com/eq-solutions/eq-solves-intake/pull/105) feat(intake): AI sanity-check on the Contacts duplicate-arch

## ⚠ Needs you (2)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (108)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

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
- **EQ** · Auto-login from Shell's tenant tile into Cards was silently skipping the handoff and bouncing to the sign-in screen instead — reported live by Royce, root-caused same session. `cards.eq.solutions` iframes across every open Shell tab share one browser's local storage, and a refresh-token rotation triggered by one tab invalidates the session another tab still has cached. The splash screen only checked whether *a* session object existed in storage, not whether it was still valid, so a stale cached session silently pre-empted the working handoff. Root-caused live against Royce's own SKS account: PostHog showed `shell_handoff_started` never fired on the failing attempt, and eq-canonical's auth logs showed `403 bad_jwt: invalid claim: missing sub claim` at the same second. Fixed in eq-cards [PR #212](https://github.com/eq-solutions/eq-cards/pull/212) (squash-merged `36a23cd`) — `_handleShellEntry()` now validates any cached session with a live `getUser()` call before trusting it, signing out and falling through to the existing handoff on any failure. Merged and deployed (explicit `Build & Deploy` workflow dispatch — Netlify + Sentry source-map upload both succeeded). **Needs Royce's click-through**: his own browser has a bad session already stuck in local storage from before the fix — clearing site data for `cards.eq.solutions` once (or a private window) and reloading the tenant tile is a device-side action only he can do; confirming the clean auto-login after that is the last open step. _(added 2026-08-04)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
_…and 96 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 1d ago | 5 | 4d |
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
| 2026-08-08 | eq-field | [#670](https://github.com/eq-solutions/eq-field/pull/670) v3.5.469 — Data tab: gate People/Sites/Schedule CSV import behind |
| 2026-08-08 | eq-field | [#669](https://github.com/eq-solutions/eq-field/pull/669) fix(apprentices): Skills Passport mobile CSS selector was dead (v |
| 2026-08-08 | eq-field | [#668](https://github.com/eq-solutions/eq-field/pull/668) fix(mobile): 5 confirmed mobile.css bugs (v3.5.469) |
| 2026-08-08 | eq-field | [#667](https://github.com/eq-solutions/eq-field/pull/667) fix(safety): gate incident records/export to Supervision (v3.5.46 |
| 2026-08-08 | eq-field | [#666](https://github.com/eq-solutions/eq-field/pull/666) v3.5.469 — Calibration + Projects had no mobile nav path |
| 2026-08-08 | eq-field | [#665](https://github.com/eq-solutions/eq-field/pull/665) fix(sign-documents): mobile UX — signature pad size, popup-blocke |
| 2026-08-08 | eq-field | [#664](https://github.com/eq-solutions/eq-field/pull/664) fix(leave): mobile responsive breakpoint for worker balance cards |
| 2026-08-08 | eq-field | [#663](https://github.com/eq-solutions/eq-field/pull/663) fix(safety-forms): crew/attendee name overflow + prestart draft c |
| 2026-08-07 | eq-shell | [#1283](https://github.com/eq-solutions/eq-shell/pull/1283) fix(rls): restrict commercial-table writes to management tiers (0 |
| 2026-08-07 | eq-shell | [#1281](https://github.com/eq-solutions/eq-shell/pull/1281) feat(access-control): expose eq-field's 74 fine-grained permissio |
| 2026-08-07 | eq-field | [#662](https://github.com/eq-solutions/eq-field/pull/662) fix(roles): vendor verify-pin.js's role list, log the silent-down |
| 2026-08-07 | eq-solves-intake | [#112](https://github.com/eq-solutions/eq-solves-intake/pull/112) feat(intake): fuzzy identity match in the Reconcile engine |
| 2026-08-07 | eq-solves-intake | [#111](https://github.com/eq-solutions/eq-solves-intake/pull/111) feat(intake): polish the Overview/To Do data-cleaning flow |
| 2026-08-06 | eq-shell | [#1265](https://github.com/eq-solutions/eq-shell/pull/1265) fix(ops): stop tenant-data-proxy crashing on 204 responses (EQ-SH |
| 2026-08-04 | eq-solves-intake | [#109](https://github.com/eq-solutions/eq-solves-intake/pull/109) fix(tenant-scoping): close 2 real gaps in api-intake + approve-wo |
_Showing 15 of 25 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **EQ-SHELL-Y (ocr-licence 401)** — not an eq-shell code bug; the licence-photo-reading feature occasionally fails a permission check talking to eq-canonical. Someone already patched the underlying cause elsewhere (~5 Aug) and it's been quiet since, but needs a few more quiet days before marking resolved for good. _(added 2026-08-07)_
- **The `_health` 404 (a separate keep-warm ping, same ~5-min cadence) is still open** — not part of this fix, not investigated. `_health` genuinely doesn't exist on ehow; low priority, nothing depends on it succeeding. _(added 2026-08-06)_
- **Not click-tested live** — self-join bulk approve/decline ([PR #1257](https://github.com/eq-solutions/eq-shell/pull/1257)) needs a tenant with 2+ pending self-join requests to actually exercise the new checkbox/bulk-action UI on Staff → pending. _(added 2026-08-06)_
- **Not click-tested live** — bulk-invite ceiling raise 50→150 ([PR #1259](https://github.com/eq-solutions/eq-shell/pull/1259)) needs a real >50-row invite batch; also watch the next scheduled `licence-expiry-scheduler` run for the employer-alert log line to confirm the new range-based claim path behaves. Royce: "will click test later." _(added 2026-08-06)_
- **Build a Cards bulk-invite path** — Cards has none today, every account provisioned one at a time. Scope: a CSV-in/result-table-out screen mirroring `AdminBulkInvite.tsx`, backed by a batch version of Cards' own single-invite flow. _(added 2026-08-06)_
- **Load-test the auth path against a synchronised login burst** (e.g. every site clocking on at 7am) — Supabase connection-pool headroom and Netlify Function concurrency under that pattern have never been measured either way. _(added 2026-08-06)_
- **SSO/SCIM and state-scoped RBAC — explicitly excluded from the closure plan, not a gap to chase.** Royce's own call today: build if/when a real customer names either by name, not speculatively ahead of demand. Recorded so this isn't re-flagged as an oversight later. _(added 2026-08-06)_
- **Not click-tested live** — `.msg`/`.eml` quote-attachment upload ([PR #1262](https://github.com/eq-solutions/eq-shell/pull/1262), merged `d494d9d5`) verified by typecheck/lint/build only. Royce (or the SKS user who hit the original error) to confirm a real Outlook email actually attaches and opens correctly from the quote's attachment list on `/sks/ops`. _(added 2026-08-06)_
- **Daily `eq-shell-field-handoff-fallback-watch` scheduled check no longer exists** — it used to give a fast yes/no on whether Field sign-in auto-recovery was working; gone from the scheduled-task list (expired or removed, not investigated further). Recreate only if ongoing visibility into this specific failure mode is wanted — EQ-SHELL-R itself is closed (root-caused to two already-fixed prior bugs, see [sessions/2026-08-06.md](sessions/2026-08-06.md)), this is purely optional monitoring. _(added 2026-08-06)_
- **GitHub MCP connector 404 on eq-shell repo access** — worth checking the GitHub App installation/scope for this connector if PR creation via MCP is needed again on eq-shell. _(added 2026-08-06)_
_…and 443 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3180 | 555 | 37 | 12 |
| [SKS](sks/pending.md) | 404 | 82 | 0 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 409 | 37 | 2 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-07 | [My Schedule maps link: the real root cause was Shell's iframe sandbox, not iOS](sessions/2026-08-07.md) |
| 2026-08-06 | [Document sign-off register: real vision from Royce, two trust gaps fixed](sessions/2026-08-06.md) |
| 2026-08-06 | [c — My Schedule maps link, part two: tap-vs-long-press on iOS standalone](sessions/2026-08-06-c.md) |
| 2026-08-05 | [Tenant-rule audit extended to eq-cards + eq-solves-intake, all 4 PRs merged and live](sessions/2026-08-05.md) |
| 2026-08-05 | [y — My Schedule maps link fixed (iOS home-screen installs)](sessions/2026-08-05-y.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-08 02:01 UTC._

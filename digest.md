---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-06
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-06 08:20 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-06 05:27 UTC → 2026-08-06 08:20 UTC)

- Merged: eq-shell [#1250](https://github.com/eq-solutions/eq-shell/pull/1250) fix(staff): compliance-pack export shows Unknown for names o
- Merged: eq-shell [#1249](https://github.com/eq-solutions/eq-shell/pull/1249) feat(ops): drag a subcontractor PDF onto the Jobs home page 
- Merged: eq-shell [#1247](https://github.com/eq-solutions/eq-shell/pull/1247) feat(field): relay a mint-entity-patch-token credential to t
- Merged: eq-shell [#1246](https://github.com/eq-solutions/eq-shell/pull/1246) feat(documents): categories for the Templates tab
- Merged: eq-shell [#1244](https://github.com/eq-solutions/eq-shell/pull/1244) fix(security): guard entity-patch against same-site confused
- Merged: eq-shell [#1242](https://github.com/eq-solutions/eq-shell/pull/1242) feat(staff): actual back-photo preview instead of a text-onl
- Merged: eq-shell [#1241](https://github.com/eq-solutions/eq-shell/pull/1241) feat(documents): bulk upload for Templates (T3)
- Merged: eq-shell [#1239](https://github.com/eq-solutions/eq-shell/pull/1239) feat(documents): Templates upload CTA + Register archive act
- ✅ Needs you: 6 → 4

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `jwt-contract-drift.yml` 10 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F7: git merge/stash-pop round-trip NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-08-05.md](sessions/2026-08-05.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (104)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Not click-tested on a real iOS device with Field added to the home screen** — Royce to confirm the maps icon now hands off to the Maps app instead of doing nothing. _(added 2026-08-05)_
- **EQ** · **Royce to confirm the SKS dashboard loads cleanly** — needs an authenticated session, off-limits for Claude to drive. _(added 2026-08-05)_
- **EQ** · **Not click-tested live by a real signed-in user** — everything above was verified at the function level and via the deploy preview's boot path, not by an authenticated session actually seeing the widget populate with real people. Royce to confirm on `field.eq.solutions` (or the Shell embed) that Birthdays & Anniversaries now shows up reliably from a fresh Dashboard landing. _(added 2026-08-05)_
- **EQ** · **Neither fix has been click-tested live** — Royce to confirm: (1) the address fields save and display correctly on a real staff member, desktop and mobile, (2) re-downloading William's compliance pack now shows "William Hong" instead of "Unknown." _(added 2026-08-05)_
- **EQ** · **Not click-tested live** — Royce to confirm a real future-dated new starter actually disappears from the roster/dispatch/timesheets and shows up correctly in the new Starting Soon widget. _(added 2026-08-05)_
- **EQ** · **Not click-tested live with real populated canonical data** — needs an authenticated worker session (`canon-read` requires a real session token). Royce to confirm a worker with an expiring Cards licence actually surfaces on the dashboard card. _(added 2026-08-05)_
- **EQ** · **None of the four PDF-import/pricing-table changes above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle on the main "From PDF" button — especially that a real sell-priced supplier PDF now computes cost correctly, and the default Cost path is unchanged, (4) the *same* toggle now also appearing on the second "Import from PDF" button inside the New Quote form when a document has ambiguous pricing. _(added 2026-08-05, updated 2026-08-05)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
_…and 92 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 1d ago | 5 | 2d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 1d ago | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 14 | 2026-08-05 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 9 | 2026-08-05 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-field | [ReferenceError: openTafeHolidaysConfig is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 3 | 2026-07-28 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 2 | 2026-08-05 |
| eq-shell | [TimeoutError: The operation was aborted due to timeout](https://eq-solutions.sentry.io/issues/138753891/) | 2 | 2026-08-04 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-06 | eq-shell | [#1265](https://github.com/eq-solutions/eq-shell/pull/1265) fix(ops): stop tenant-data-proxy crashing on 204 responses (EQ-SH |
| 2026-08-06 | eq-shell | [#1264](https://github.com/eq-solutions/eq-shell/pull/1264) feat(ops): extend the EQ-SHELL-1A tenant-data proxy to 3 more pag |
| 2026-08-06 | eq-shell | [#1263](https://github.com/eq-solutions/eq-shell/pull/1263) feat(ops): same-origin proxy for EQ Ops/Intake tenant data (EQ-SH |
| 2026-08-06 | eq-shell | [#1262](https://github.com/eq-solutions/eq-shell/pull/1262) feat(quotes): accept Outlook .msg/.eml as quote attachments |
| 2026-08-06 | eq-shell | [#1261](https://github.com/eq-solutions/eq-shell/pull/1261) fix(ops): widen EQ-SHELL-1A retry window to ~5s |
| 2026-08-06 | eq-shell | [#1260](https://github.com/eq-solutions/eq-shell/pull/1260) fix(ops): retry pipeline-counts/attachment-count RPCs on transien |
| 2026-08-06 | eq-field | [#659](https://github.com/eq-solutions/eq-field/pull/659) v3.5.465 — My Schedule maps link: tap still didn't open Maps on i |
| 2026-08-06 | eq-field | [#658](https://github.com/eq-solutions/eq-field/pull/658) fix(bundles): role drift-guard vendoring + restore 3 fixes that n |
| 2026-08-05 | eq-shell | [#1259](https://github.com/eq-solutions/eq-shell/pull/1259) fix(onboarding): close two real gaps from the SaaS-parity audit |
| 2026-08-05 | eq-shell | [#1258](https://github.com/eq-solutions/eq-shell/pull/1258) fix(cards): stop alerting on Field/Service's own token refresh |
| 2026-08-05 | eq-shell | [#1257](https://github.com/eq-solutions/eq-shell/pull/1257) feat(staff): bulk approve/decline self-join requests |
| 2026-08-05 | eq-shell | [#1256](https://github.com/eq-solutions/eq-shell/pull/1256) fix(observability): stop mislabeling render crashes as chunk-erro |
| 2026-08-05 | eq-shell | [#1255](https://github.com/eq-solutions/eq-shell/pull/1255) fix(briefing): validate submit_briefing tool output before trusti |
| 2026-08-05 | eq-shell | [#1254](https://github.com/eq-solutions/eq-shell/pull/1254) fix(ops): wire the cost/sell question into the other Import from  |
| 2026-08-05 | eq-shell | [#1253](https://github.com/eq-solutions/eq-shell/pull/1253) feat(documents): bulk category assignment for the Templates tab |
_Showing 15 of 138 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Recurring `GET /rest/v1/canonical_outbox` and `GET /rest/v1/_health` 404s on ehow, every ~5 min, ongoing** — found incidentally while checking ehow's API logs for an unrelated Sentry error (EQ-SHELL-1A, see correction below). Both tables don't exist on ehow; something (tagged `node` user-agent, so a server-side job/function, not a browser) is polling them continuously and getting a 404 every time. Not investigated further — unclear if intentional (an existence-probe pattern) or dead/misconfigured code pointed at the wrong project. Worth a look. _(added 2026-08-06)_
- **Replace EQ Field's destructive CSV import with an additive one** — top item on the "close what's worth closing" plan, not built. Scope: `eq-field/scripts/import-export.js` + `supabase-entities.js` (separate repo) — match-by-phone-or-email against existing people before insert, never blanket-delete first. _(added 2026-08-06)_
- **Build a Cards bulk-invite path** — Cards has none today, every account provisioned one at a time. Scope: a CSV-in/result-table-out screen mirroring `AdminBulkInvite.tsx`, backed by a batch version of Cards' own single-invite flow. _(added 2026-08-06)_
- **Load-test the auth path against a synchronised login burst** (e.g. every site clocking on at 7am) — Supabase connection-pool headroom and Netlify Function concurrency under that pattern have never been measured either way. _(added 2026-08-06)_
- **SSO/SCIM and state-scoped RBAC — explicitly excluded from the closure plan, not a gap to chase.** Royce's own call today: build if/when a real customer names either by name, not speculatively ahead of demand. Recorded so this isn't re-flagged as an oversight later. _(added 2026-08-06)_
- **Daily `eq-shell-field-handoff-fallback-watch` scheduled check no longer exists** — it used to give a fast yes/no on whether Field sign-in auto-recovery was working; gone from the scheduled-task list (expired or removed, not investigated further). Recreate only if ongoing visibility into this specific failure mode is wanted — EQ-SHELL-R itself is closed (root-caused to two already-fixed prior bugs, see [sessions/2026-08-06.md](sessions/2026-08-06.md)), this is purely optional monitoring. _(added 2026-08-06)_
- **GitHub MCP connector 404 on eq-shell repo access** — worth checking the GitHub App installation/scope for this connector if PR creation via MCP is needed again on eq-shell. _(added 2026-08-06)_
- **HOLD — Retire the legacy direct-to-Supabase browser path** (`tenantDataClient.ts`/`sksSupabaseClient.ts`, `VITE_SKS_SUPABASE_URL`/anon-key browser exposure, CSP `connect-src` entries) — technically unblocked (soak confirmed clean, all 4 known browser consumers now go through the proxy first, legacy kept only as fallback), but Royce is overseas and explicitly asked to hold this until he's back rather than risk anything while he's away. Do not start this without him present, even though nothing is technically blocking it. _(added 2026-08-06, held 2026-08-06)_
- **Not click-tested live by a real user** — `LabourHireRates.tsx`, `Suppliers.tsx`, and Intake were migrated to the proxy-first path and pass build/typecheck/301 tests, but nobody has opened them live yet to confirm no regression. Royce or a real SKS user to confirm. _(added 2026-08-06)_
- **Physical-signature-as-photo-upload** — real option, small lift, not confirmed for build. _(added 2026-08-05)_
_…and 420 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3289 | 559 | 90 | 12 |
| [SKS](sks/pending.md) | 404 | 82 | 0 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 409 | 37 | 2 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-06 | [Document sign-off register: real vision from Royce, two trust gaps fixed](sessions/2026-08-06.md) |
| 2026-08-05 | [Tenant-rule audit extended to eq-cards + eq-solves-intake, all 4 PRs merged and live](sessions/2026-08-05.md) |
| 2026-08-05 | [y — My Schedule maps link fixed (iOS home-screen installs)](sessions/2026-08-05-y.md) |
| 2026-08-05 | [x — Sentry confirmed EQ-SHELL-10/19 live, then a /decide pass found F6/F7 were a false alarm and surfaced a genuinely new incident (F12)](sessions/2026-08-05-x.md) |
| 2026-08-05 | [v — Root-caused the pending.md bloat as a 4-day-old broken cron, fixed it, then closed the actual gap as F11](sessions/2026-08-05-v.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-06 08:20 UTC._

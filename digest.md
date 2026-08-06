---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-06
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-06 05:27 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-06 04:39 UTC → 2026-08-06 05:27 UTC)

- Merged: eq-shell [#1265](https://github.com/eq-solutions/eq-shell/pull/1265) fix(ops): stop tenant-data-proxy crashing on 204 responses (
- Merged: eq-shell [#1252](https://github.com/eq-solutions/eq-shell/pull/1252) feat(ops): ask cost vs. sell when importing a subcontractor 
- Merged: eq-shell [#1248](https://github.com/eq-solutions/eq-shell/pull/1248) fix(ops): widen Description column and batch-save outlet pri
- Merged: eq-shell [#1245](https://github.com/eq-solutions/eq-shell/pull/1245) feat(field): Bearer credential so Field can trigger a Shell-
- Merged: eq-shell [#1243](https://github.com/eq-solutions/eq-shell/pull/1243) refactor(workers): simplify invite header to two actions
- Merged: eq-shell [#1240](https://github.com/eq-solutions/eq-shell/pull/1240) feat(staff): "back on file" indicator for licence photos
- Merged: eq-shell [#1238](https://github.com/eq-solutions/eq-shell/pull/1238) feat(licences): show the uploaded photo/PDF as a manual-fill
- Merged: eq-shell [#1237](https://github.com/eq-solutions/eq-shell/pull/1237) fix(staff): hide Company field for Direct, require supervisi

## ⚠ Needs you (6)

- 🔴 **Sentry new error** — `eq-shell` [Error: eq-ops rpc eq_quote_pipeline_counts failed: TypeError](https://eq-solutions.sentry.io/issues/139108089/)
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `jwt-contract-drift.yml` 10 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F7: git merge/stash-pop round-trip NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-08-05.md](sessions/2026-08-05.md) · [failures.md](system/failures.md)
- 🟠 **Cron failing** — `backup-eq-canonical.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-04 · [failures.md](system/failures.md) F11

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
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: eq-ops rpc eq_quote_pipeline_counts failed: TypeError: Failed to fetch (e](https://eq-solutions.sentry.io/issues/139108089/) | 46 | 2026-08-06 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 14 | 2026-08-05 |
| eq-shell | [Cards handoff request from unexpected origin](https://eq-solutions.sentry.io/issues/138655603/) | 10 | 2026-08-05 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 9 | 2026-08-05 |
| eq-shell | [TypeError: Response constructor: Invalid response status code 204](https://eq-solutions.sentry.io/issues/139132689/) | 8 | 2026-08-06 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 7](https://eq-solutions.sentry.io/issues/138175643/) | 5 | 2026-08-05 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
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
| 2026-08-06 | eq-field | [#658](https://github.com/eq-solutions/eq-field/pull/658) fix(bundles): role drift-guard vendoring + restore 3 fixes that n |
| 2026-08-05 | eq-shell | [#1259](https://github.com/eq-solutions/eq-shell/pull/1259) fix(onboarding): close two real gaps from the SaaS-parity audit |
| 2026-08-05 | eq-shell | [#1258](https://github.com/eq-solutions/eq-shell/pull/1258) fix(cards): stop alerting on Field/Service's own token refresh |
| 2026-08-05 | eq-shell | [#1257](https://github.com/eq-solutions/eq-shell/pull/1257) feat(staff): bulk approve/decline self-join requests |
| 2026-08-05 | eq-shell | [#1256](https://github.com/eq-solutions/eq-shell/pull/1256) fix(observability): stop mislabeling render crashes as chunk-erro |
| 2026-08-05 | eq-shell | [#1255](https://github.com/eq-solutions/eq-shell/pull/1255) fix(briefing): validate submit_briefing tool output before trusti |
| 2026-08-05 | eq-shell | [#1254](https://github.com/eq-solutions/eq-shell/pull/1254) fix(ops): wire the cost/sell question into the other Import from  |
| 2026-08-05 | eq-shell | [#1253](https://github.com/eq-solutions/eq-shell/pull/1253) feat(documents): bulk category assignment for the Templates tab |
| 2026-08-05 | eq-shell | [#1251](https://github.com/eq-solutions/eq-shell/pull/1251) feat(staff): add home address fields to Staff edit (desktop + mob |
_Showing 15 of 138 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **GitHub MCP connector 404 on eq-shell repo access** — worth checking the GitHub App installation/scope for this connector if PR creation via MCP is needed again on eq-shell. _(added 2026-08-06)_
- **HOLD — Retire the legacy direct-to-Supabase browser path** (`tenantDataClient.ts`/`sksSupabaseClient.ts`, `VITE_SKS_SUPABASE_URL`/anon-key browser exposure, CSP `connect-src` entries) — technically unblocked (soak confirmed clean, all 4 known browser consumers now go through the proxy first, legacy kept only as fallback), but Royce is overseas and explicitly asked to hold this until he's back rather than risk anything while he's away. Do not start this without him present, even though nothing is technically blocking it. _(added 2026-08-06, held 2026-08-06)_
- **Not click-tested live by a real user** — `LabourHireRates.tsx`, `Suppliers.tsx`, and Intake were migrated to the proxy-first path and pass build/typecheck/301 tests, but nobody has opened them live yet to confirm no regression. Royce or a real SKS user to confirm. _(added 2026-08-06)_
- **Physical-signature-as-photo-upload** — real option, small lift, not confirmed for build. _(added 2026-08-05)_
- **"Easily accessible" and "easy for management to prove" beyond what's already built** — no further scoping done yet; revisit once access is actually opened and there's real multi-person usage to learn from. _(added 2026-08-05)_
- **Version-pin skew between eq-shell's and eq-service's independent `@eq-solutions/contracts` pins has no guard.** Both pin the identical tag today so there's no live risk, but each repo pins independently (`github:eq-solutions/eq-contracts#vX.Y.Z`, not a workspace link) — if eq-shell ever migrates too and the two pins later diverge, neither this script (reads the package from `main`, not each repo's actual pin) nor either repo's own `tsc` would catch it. Documented as a caveat in the script itself; a real follow-up guard, not built this session. _(added 2026-08-06)_
- **eq-shell's own migration to `@eq-solutions/contracts`** (replacing its local `SupabaseJwtClaims` with the shared `ShellHandoffClaims` type) is still not done — the canary's originally-envisioned "durable fix" endpoint. Not requested this session; natural next step if eq-shell touches this file again. _(added 2026-08-06)_
- **Only the last 10 days of signups were checked for the stuck-appMetadata pattern** — the 4 unblocked accounts are the ones caught in that window; any self-join/auto-provision-only account older than that with a never-updated `raw_app_meta_data` would still show the same symptom if they ever come back and retry. No full historical audit run. _(added 2026-08-05)_
- **William's own Cards `public.workers.first_name/last_name` is still blank** (`""`, unchanged since signup) even though his Shell `app_data.staff` record now has his real name — the compliance-pack fix below makes Shell's copy win for that one export, but anything else that reads Cards' own `workers` table directly for display would still show blank for him specifically. Not backfilled. _(added 2026-08-05)_
- **Worth a look: `digest.md`'s "Recently built" table shows merge status, not deploy status, for every repo — but eq-cards is the one repo where those two are allowed to diverge for hours by design.** A merged eq-cards PR currently reads identically to a live one on the digest, which is exactly what caused this session's confusion. Might be worth a "manual-deploy pending" flag specific to eq-cards, or a general merged-vs-deployed distinction if other repos ever adopt the same manual-gate pattern.
_…and 414 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3259 | 550 | 90 | 12 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-06 05:27 UTC._

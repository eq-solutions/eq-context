---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-07
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-07 06:08 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-07 05:30 UTC → 2026-08-07 06:08 UTC)

- Merged: eq-shell [#1278](https://github.com/eq-solutions/eq-shell/pull/1278) ci: add a static check that function grants survive CREATE O
- Merged: eq-shell [#1262](https://github.com/eq-solutions/eq-shell/pull/1262) feat(quotes): accept Outlook .msg/.eml as quote attachments
- Merged: eq-shell [#1261](https://github.com/eq-solutions/eq-shell/pull/1261) fix(ops): widen EQ-SHELL-1A retry window to ~5s
- Merged: eq-shell [#1260](https://github.com/eq-solutions/eq-shell/pull/1260) fix(ops): retry pipeline-counts/attachment-count RPCs on tra
- Merged: eq-shell [#1259](https://github.com/eq-solutions/eq-shell/pull/1259) fix(onboarding): close two real gaps from the SaaS-parity au
- Merged: eq-shell [#1257](https://github.com/eq-solutions/eq-shell/pull/1257) feat(staff): bulk approve/decline self-join requests
- Merged: eq-shell [#1255](https://github.com/eq-solutions/eq-shell/pull/1255) fix(briefing): validate submit_briefing tool output before t
- Merged: eq-shell [#1253](https://github.com/eq-solutions/eq-shell/pull/1253) feat(documents): bulk category assignment for the Templates 

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🟠 **Cron failing** — `adversarial-suite.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-05 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (102)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to confirm the SKS dashboard loads cleanly** — needs an authenticated session, off-limits for Claude to drive. _(added 2026-08-05)_
- **EQ** · **Not click-tested live by a real signed-in user** — everything above was verified at the function level and via the deploy preview's boot path, not by an authenticated session actually seeing the widget populate with real people. Royce to confirm on `field.eq.solutions` (or the Shell embed) that Birthdays & Anniversaries now shows up reliably from a fresh Dashboard landing. _(added 2026-08-05)_
- **EQ** · **Neither fix has been click-tested live** — Royce to confirm: (1) the address fields save and display correctly on a real staff member, desktop and mobile, (2) re-downloading William's compliance pack now shows "William Hong" instead of "Unknown." _(added 2026-08-05)_
- **EQ** · **Not click-tested live** — Royce to confirm a real future-dated new starter actually disappears from the roster/dispatch/timesheets and shows up correctly in the new Starting Soon widget. _(added 2026-08-05)_
- **EQ** · **None of the four PDF-import/pricing-table changes above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle on the main "From PDF" button — especially that a real sell-priced supplier PDF now computes cost correctly, and the default Cost path is unchanged, (4) the *same* toggle now also appearing on the second "Import from PDF" button inside the New Quote form when a document has ambiguous pricing. _(added 2026-08-05, updated 2026-08-05)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
- **EQ** · **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
_…and 90 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 5 | 3d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 2d ago | 0 | — |
| eq-solves-intake | ✓ success | 2d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 4 | 2026-08-05 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-field | [ReferenceError: openTafeHolidaysConfig is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 3 | 2026-07-28 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 2 | 2026-08-07 |
| eq-shell | [Error: eq-ops rpc eq_delete_quote failed: quote not found or access denied](https://eq-solutions.sentry.io/issues/139309419/) | 2 | 2026-08-06 |
| eq-shell | [Error: eq-ops rpc eq_trash_quote failed: quote not found, access denied, or alre](https://eq-solutions.sentry.io/issues/128679375/) | 2 | 2026-08-06 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-07 | eq-shell | [#1278](https://github.com/eq-solutions/eq-shell/pull/1278) ci: add a static check that function grants survive CREATE OR REP |
| 2026-08-07 | eq-shell | [#1277](https://github.com/eq-solutions/eq-shell/pull/1277) fix(documents): revoke authenticated grants on document_signoffs  |
| 2026-08-07 | eq-shell | [#1275](https://github.com/eq-solutions/eq-shell/pull/1275) fix(auth): restore eq_cards_admin_upsert_worker's authenticated g |
| 2026-08-07 | eq-shell | [#1276](https://github.com/eq-solutions/eq-shell/pull/1276) Revert "fix(documents): signer-scoped RLS on document_signoffs +  |
| 2026-08-07 | eq-shell | [#1274](https://github.com/eq-solutions/eq-shell/pull/1274) fix(documents): signer-scoped RLS on document_signoffs + document |
| 2026-08-07 | eq-shell | [#1273](https://github.com/eq-solutions/eq-shell/pull/1273) fix(auth): restore link_pending_invites' authenticated grant |
| 2026-08-07 | eq-shell | [#1272](https://github.com/eq-solutions/eq-shell/pull/1272) fix(auth): stop link_pending_invites grafting a duplicate on phon |
| 2026-08-07 | eq-shell | [#1271](https://github.com/eq-solutions/eq-shell/pull/1271) feat(documents): auto-push onboarding documents to new starters |
| 2026-08-07 | eq-shell | [#1270](https://github.com/eq-solutions/eq-shell/pull/1270) fix(auth): stop handle_phone_dedup grafting a duplicate shell_con |
| 2026-08-07 | eq-shell | [#1268](https://github.com/eq-solutions/eq-shell/pull/1268) fix(shell): grant allow-popups on the Field/Service/Cards iframe  |
| 2026-08-07 | eq-field | [#661](https://github.com/eq-solutions/eq-field/pull/661) fix(documents): move sign-off list/view/sign behind a server-veri |
| 2026-08-07 | eq-field | [#660](https://github.com/eq-solutions/eq-field/pull/660) v3.5.466 — Contacts CSV import no longer wipes the whole roster |
| 2026-08-06 | eq-shell | [#1269](https://github.com/eq-solutions/eq-shell/pull/1269) fix(observability): retry-instead-of-logout on verify-timeout, re |
| 2026-08-06 | eq-shell | [#1265](https://github.com/eq-solutions/eq-shell/pull/1265) fix(ops): stop tenant-data-proxy crashing on 204 responses (EQ-SH |
| 2026-08-06 | eq-shell | [#1264](https://github.com/eq-solutions/eq-shell/pull/1264) feat(ops): extend the EQ-SHELL-1A tenant-data proxy to 3 more pag |
_Showing 15 of 128 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **The `_health` 404 (a separate keep-warm ping, same ~5-min cadence) is still open** — not part of this fix, not investigated. `_health` genuinely doesn't exist on ehow; low priority, nothing depends on it succeeding. _(added 2026-08-06)_
- **Build a Cards bulk-invite path** — Cards has none today, every account provisioned one at a time. Scope: a CSV-in/result-table-out screen mirroring `AdminBulkInvite.tsx`, backed by a batch version of Cards' own single-invite flow. _(added 2026-08-06)_
- **Load-test the auth path against a synchronised login burst** (e.g. every site clocking on at 7am) — Supabase connection-pool headroom and Netlify Function concurrency under that pattern have never been measured either way. _(added 2026-08-06)_
- **SSO/SCIM and state-scoped RBAC — explicitly excluded from the closure plan, not a gap to chase.** Royce's own call today: build if/when a real customer names either by name, not speculatively ahead of demand. Recorded so this isn't re-flagged as an oversight later. _(added 2026-08-06)_
- **Daily `eq-shell-field-handoff-fallback-watch` scheduled check no longer exists** — it used to give a fast yes/no on whether Field sign-in auto-recovery was working; gone from the scheduled-task list (expired or removed, not investigated further). Recreate only if ongoing visibility into this specific failure mode is wanted — EQ-SHELL-R itself is closed (root-caused to two already-fixed prior bugs, see [sessions/2026-08-06.md](sessions/2026-08-06.md)), this is purely optional monitoring. _(added 2026-08-06)_
- **GitHub MCP connector 404 on eq-shell repo access** — worth checking the GitHub App installation/scope for this connector if PR creation via MCP is needed again on eq-shell. _(added 2026-08-06)_
- **HOLD — Retire the legacy direct-to-Supabase browser path** (`tenantDataClient.ts`/`sksSupabaseClient.ts`, `VITE_SKS_SUPABASE_URL`/anon-key browser exposure, CSP `connect-src` entries) — technically unblocked (soak confirmed clean, all 4 known browser consumers now go through the proxy first, legacy kept only as fallback), but Royce is overseas and explicitly asked to hold this until he's back rather than risk anything while he's away. Do not start this without him present, even though nothing is technically blocking it. _(added 2026-08-06, held 2026-08-06)_
- **Not click-tested live by a real user** — `LabourHireRates.tsx`, `Suppliers.tsx`, and Intake were migrated to the proxy-first path and pass build/typecheck/301 tests, but nobody has opened them live yet to confirm no regression. Royce or a real SKS user to confirm. _(added 2026-08-06)_
- **Physical-signature-as-photo-upload** — real option, small lift, not confirmed for build. _(added 2026-08-05)_
- **"Easily accessible" and "easy for management to prove" beyond what's already built** — no further scoping done yet; revisit once access is actually opened and there's real multi-person usage to learn from. _(added 2026-08-05)_
_…and 426 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3230 | 556 | 56 | 12 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-07 06:08 UTC._

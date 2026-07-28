---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-28 09:24 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-28 09:10 UTC → 2026-07-28 09:24 UTC)

- Merged: eq-shell [#1080](https://github.com/eq-solutions/eq-shell/pull/1080) fix(licences): licence-push never marks a revoked Cards lice
- Merged: eq-shell [#1063](https://github.com/eq-solutions/eq-shell/pull/1063) fix(quotes): stop detail badge showing a stage change that n
- Merged: eq-shell [#1062](https://github.com/eq-solutions/eq-shell/pull/1062) feat(licences): let a manager replace the photo/PDF on an ex
- Merged: eq-shell [#1059](https://github.com/eq-solutions/eq-shell/pull/1059) feat(control-plane): backfill remaining 111 legacy jvkn func
- Merged: eq-shell [#1058](https://github.com/eq-solutions/eq-shell/pull/1058) fix(auth): require re-auth before replacing an enrolled auth
- Merged: eq-shell [#1055](https://github.com/eq-solutions/eq-shell/pull/1055) hotfix(quotes): drop stale eq_bulk_update_quote_status overl
- Merged: eq-shell [#1054](https://github.com/eq-solutions/eq-shell/pull/1054) fix(schema): reassert security_invoker on field_people views
- Merged: eq-shell [#1053](https://github.com/eq-solutions/eq-shell/pull/1053) fix(quotes): capture a reason when bulk-closing quotes as lo

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F6: Append (>>) NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-07-28.md](sessions/2026-07-28.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (84)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Separate, lower-priority finding: 53 of 88 active SKS staff have a Cards worker link but zero credentials captured in Cards at all** (checked the pre-promotion `worker_credentials` table too — genuinely empty, not stuck mid-migration). Only 34 of 88 active staff have any licence data flowing through Shell. This is a Cards onboarding-completion gap, not a sync bug — no action taken, logging only per Royce's call. _(added 2026-07-28)_
- **EQ** · **Royce to click through the real flow once the deploy lands**: set up two-step verification, save the codes shown, sign out, sign back in using one of the backup codes instead of the phone app, then generate a fresh set from Settings and confirm the old ones stop working. _(added 2026-07-28)_
- **EQ** · **Royce to confirm live**: open Moahmmed Alsadiq Ahmed Elsayed on the Staff page, check the Photo ID and White Card show the new clearer photos, and that the "Replace photo" button now returns to normal after use. _(added 2026-07-28)_
- **EQ** · **Royce to click through a real "New customer" add** once convenient, to confirm the address dropdown now actually appears and fills suburb/state (verified in code + build, not yet eyeballed live). _(added 2026-07-28)_
- **EQ** · **Royce to export a real org's compliance pack and eyeball the new layout in Excel** — verified in code and with a test run, not yet checked against a real export. _(added 2026-07-28)_
- **EQ** · **Royce to re-download a compliance pack once the deploy lands** and confirm the filename reads correctly and Rhys Scott's email now shows current. _(added 2026-07-28)_
- **EQ** · **Royce to re-enter Ben Ritchie's correct email one more time** via the Staff page — his last correction was reverted by the old bug before the fix went live, so the stale value is still sitting in the database. It will stick this time. _(added 2026-07-28)_
- **EQ** · **Royce to click through the Edit Roster grid on field.eq.solutions once the deploy lands** and confirm Ben Ritchie (or any off-roster person) no longer appears there — code-fixed and pushed, not yet eyeballed live. _(added 2026-07-28)_
- **EQ** · **Royce to check SKS-17489 in EQ Ops** once the deploy lands — confirm the badge and board agree, then enter a Job No. to actually advance it out of Open (that's why it was stuck). _(added 2026-07-28)_
- **EQ** · **Batch Fill's new Team toggle (compose/select) behaves differently from the Timesheets batch modal's existing Team filter (narrows the list)** — same idea, two different behaviours in two similar screens of the same app. Flagged for Royce's call, not resolved. _(added 2026-07-27)_
- **EQ** · **Fix sign-in logging at the source — real, but bigger and more sensitive than "simple," needs Royce's explicit go-ahead first.** It writes a fresh record every time the app re-checks you're signed in (reopening a tab, switching back to it, a reload) — real timestamps pulled from Royce's own login history show this firing anywhere from 26 seconds to 23 minutes apart, not on any fixed clock (an earlier note here claiming "every ~14 minutes" was wrong — that figure came from an unrelated eq-shell bug, not from anything measured against Field's own data, and has been corrected). Rolling repeat checks into one row would shrink the table at the source instead of just hiding it in the view. Steelmanned before touching anything: this changes what a live, load-bearing security control (`verify-pin.js`, every SKS sign-in) actually writes, not just a display filter — a genuinely different risk class from the rest of this session's work, and this repo's own rules require explicit sign-off before an auth-adjacent change like this ships. Not scoped or built — ended on a question back to Royce (scope it now, or leave parked) that hadn't been answered when this session closed. _(added 2026-07-27)_
- **EQ** · **Live click-through as a lower-permission user (employee/apprentice/labour-hire/subcontractor) still not done** — verified instead by reading the code directly: those roles all lack `field.dispatch`, and without it the new checkboxes render natively `disabled` and the inline text/select cells render as plain unclickable text with no edit affordance at all (not just a disabled button) — confirmed in both `StaffPage.tsx` and the shared roles package. The write endpoint (`entity-patch.ts`) enforces the same permission server-side regardless of what the UI shows. Needs Royce to actually sign in as one of those roles to eyeball it, since Claude doesn't hold a lower-permission test login. _(added 2026-07-27)_
_…and 72 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 8 | 2026-07-27 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 5 | 2026-07-23 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695940/) | 1 | 2026-07-27 |
| eq-field | [TypeError: Cannot set properties of null (setting 'innerHTML')](https://eq-solutions.sentry.io/issues/136685760/) | 1 | 2026-07-27 |
| eq-field | [SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared](https://eq-solutions.sentry.io/issues/136548558/) | 1 | 2026-07-26 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-28 | eq-shell | [#1080](https://github.com/eq-solutions/eq-shell/pull/1080) fix(licences): licence-push never marks a revoked Cards licence i |
| 2026-07-28 | eq-shell | [#1079](https://github.com/eq-solutions/eq-shell/pull/1079) fix(suppliers): wrap desktop Table in a horizontal-scroll contain |
| 2026-07-28 | eq-shell | [#1078](https://github.com/eq-solutions/eq-shell/pull/1078) fix(admin): correct Worker join QR copy to match invite-required  |
| 2026-07-28 | eq-shell | [#1074](https://github.com/eq-solutions/eq-shell/pull/1074) fix(deps): xlsx off unpatched npm registry to SheetJS CDN fix |
| 2026-07-28 | eq-shell | [#1077](https://github.com/eq-solutions/eq-shell/pull/1077) fix(security): revoke anon EXECUTE on eq_enforce_function_privacy |
| 2026-07-28 | eq-shell | [#1076](https://github.com/eq-solutions/eq-shell/pull/1076) feat(field-sync): licence-push.ts syncs Cards licence edits into  |
| 2026-07-28 | eq-shell | [#1075](https://github.com/eq-solutions/eq-shell/pull/1075) fix(staff): licence-review badge misses edits to already-reviewed |
| 2026-07-28 | eq-shell | [#1071](https://github.com/eq-solutions/eq-shell/pull/1071) fix(cards): clean compliance-pack filename, stop showing stale wo |
| 2026-07-28 | eq-shell | [#1073](https://github.com/eq-solutions/eq-shell/pull/1073) fix(sks-sync): stop the daily worker sync clobbering Shell staff  |
| 2026-07-28 | eq-shell | [#1072](https://github.com/eq-solutions/eq-shell/pull/1072) docs(control-plane): record eq_enforce_function_privacy applied t |
| 2026-07-28 | eq-shell | [#1070](https://github.com/eq-solutions/eq-shell/pull/1070) fix(security): event-trigger lockdown for anon-executable new fun |
| 2026-07-28 | eq-shell | [#1068](https://github.com/eq-solutions/eq-shell/pull/1068) feat(auth): TOTP backup codes for authenticator device loss |
| 2026-07-28 | eq-shell | [#1069](https://github.com/eq-solutions/eq-shell/pull/1069) fix(control-plane): eq_intake_rollback crashed on every call sinc |
| 2026-07-28 | eq-shell | [#1067](https://github.com/eq-solutions/eq-shell/pull/1067) fix(auth): strip totp_secret from login response payloads |
| 2026-07-28 | eq-shell | [#1066](https://github.com/eq-solutions/eq-shell/pull/1066) fix(licences): Replace photo button never clears its busy state o |
_Showing 15 of 106 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Royce/a worker to trigger a slow or failed photo-read live and confirm the new message shows and stays** — verified in code + automated tests (88/88 passing), not yet clicked through for real. _(added 2026-07-28)_
- **Brian Griffin-Colls' First Aid/CPR certificate itself still needs updating** — the bug that silently dropped his attempt is now fixed, but his original update was never captured; someone still needs to redo it (himself, or an admin via the Staff page). _(added 2026-07-28)_
- **Competitive benchmark vs industry leaders (Deputy, Tradify, Fergus, simPRO, ServiceM8, Rhumbix, Skedulo)** — selected alongside the MD-tidy pass, but the session pivoted to the Sites-screen rebuild before it was run. Not started. _(added 2026-07-28)_
- **Go use the real review console next time** (Core → `IntakeHealthHome`'s Sites Dupes tab) instead of raw SQL — it already works. _(added 2026-07-28)_
- **4 new unreviewed advisory pairs from this morning** (2026-07-28 05:42-06:36 UTC) on sites not touched today — not investigated. _(added 2026-07-28)_
- **Kareena's KPH/KAR pairing was flagged "ambiguous" by the live resolver** (2026-07-23) — today's manual pick (keep KPH) looks right on the evidence, but worth a second look via the console. _(added 2026-07-28)_
- **eq-receipts' Netlify site doesn't auto-deploy on push to `main`** despite `netlify.toml` and the app's own kickoff doc assuming it does — every deploy this session needed a manual trigger. The Netlify MCP's own CLI-proxy deploy path 404'd reproducibly (three times now); the dashboard's manual "Trigger deploy" is the only confirmed-working path right now. Root cause not investigated — worth fixing so this doesn't need manual triggering forever. _(added 2026-07-28)_
- **Rhys to re-upload a distinct back photo for his electrical licence** if the duplicate was accidental — his call, not a system fix. _(added 2026-07-28)_
- **CRON_SECRET rotation** — the one real hit: a plaintext credential in vendored git history (`eq-intake/eq-platform/apps/eq-service/CHANGELOG.md`, commit `b116e4430c8`, 2026-06-10, file since deleted from the tree), described in that commit as "already set" in Netlify. Deliberately left un-allowlisted in `.gitleaks.toml` so it keeps surfacing on a full-history scan rather than going silent. Needs a decision: rotate the value in Netlify, and note the same value likely sits in `eq-solves-intake`'s own git history too, not just here. _(added 2026-07-28)_
- **Remaining audit findings not yet triaged into work** — the 6-perspective "vs industry" audit that prompted this surfaced 4 P0 / 11 P1 / 9 P2 findings across auth, authorization, multi-tenant data, frontend composition, security ops, and DX tooling. Only the secret-scan gate (above) and the field_people drift (separate section) have been acted on so far. Full findings are in a Claude.ai artifact from this session, not yet copied into repo docs — worth deciding whether it needs a permanent home before the artifact is the only record of it. _(added 2026-07-28)_
_…and 332 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
_…and 59 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2693 | 422 | 76 | 9 |
| [SKS](sks/pending.md) | 434 | 76 | 12 | 13 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 382 | 34 | 7 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-28 | [Roster: archive Labour Hire from the grid with a rehire rating](sessions/2026-07-28.md) |
| 2026-07-27 | [eq-ui design handoff shipped + propagated to eq-shell/eq-service, real bugs found along the way](sessions/2026-07-27.md) |
| 2026-07-26 | [Customers page speed fix, Job Creation export bug found+fixed, customer-level default End Client, Ops quote-form layout](sessions/2026-07-26.md) |
| 2026-07-25 | [Closed out the Coupa/staff-reactivation thread from the day before: merged PR #993, dispatched the ledger reconcile, explained the migration-numbering saga](sessions/2026-07-25.md) |
| 2026-07-24 | [EQ Ops quote-detail panel simplified + Coupa PO import rebuilt against the real export](sessions/2026-07-24.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-28 09:24 UTC._

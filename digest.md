---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-28 05:47 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-28 04:40 UTC → 2026-07-28 05:47 UTC)

- Merged: eq-shell [#1043](https://github.com/eq-solutions/eq-shell/pull/1043) fix(shell): EQ Field is missing its Records nav + rail opens
- Merged: eq-shell [#1041](https://github.com/eq-solutions/eq-shell/pull/1041) fix(attachments): list/upload-attachment hit the control pla
- Merged: eq-shell [#1038](https://github.com/eq-solutions/eq-shell/pull/1038) chore: remove dead cards-staff-matches.ts
- Merged: eq-shell [#1037](https://github.com/eq-solutions/eq-shell/pull/1037) fix(shell): white background on iframe loading pane, not nea
- Merged: eq-shell [#1036](https://github.com/eq-solutions/eq-shell/pull/1036) fix(security): close 2 more cross-tenant lookup bugs + add s
- Merged: eq-shell [#1034](https://github.com/eq-solutions/eq-shell/pull/1034) fix(admin): resolve cross-tenant user lookup in eq_get_tenan
- Merged: eq-shell [#1030](https://github.com/eq-solutions/eq-shell/pull/1030) fix(staff): Photo ID requirement satisfied by driver licence
- Merged: eq-shell [#1029](https://github.com/eq-solutions/eq-shell/pull/1029) feat(settings): nominate specific recipients for new-join-re

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/)

## 🙋 Waiting on you (78)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Batch Fill's new Team toggle (compose/select) behaves differently from the Timesheets batch modal's existing Team filter (narrows the list)** — same idea, two different behaviours in two similar screens of the same app. Flagged for Royce's call, not resolved. _(added 2026-07-27)_
- **EQ** · **Fix sign-in logging at the source — real, but bigger and more sensitive than "simple," needs Royce's explicit go-ahead first.** It writes a fresh record every time the app re-checks you're signed in (reopening a tab, switching back to it, a reload) — real timestamps pulled from Royce's own login history show this firing anywhere from 26 seconds to 23 minutes apart, not on any fixed clock (an earlier note here claiming "every ~14 minutes" was wrong — that figure came from an unrelated eq-shell bug, not from anything measured against Field's own data, and has been corrected). Rolling repeat checks into one row would shrink the table at the source instead of just hiding it in the view. Steelmanned before touching anything: this changes what a live, load-bearing security control (`verify-pin.js`, every SKS sign-in) actually writes, not just a display filter — a genuinely different risk class from the rest of this session's work, and this repo's own rules require explicit sign-off before an auth-adjacent change like this ships. Not scoped or built — ended on a question back to Royce (scope it now, or leave parked) that hadn't been answered when this session closed. _(added 2026-07-27)_
- **EQ** · **Live click-through as a lower-permission user (employee/apprentice/labour-hire/subcontractor) still not done** — verified instead by reading the code directly: those roles all lack `field.dispatch`, and without it the new checkboxes render natively `disabled` and the inline text/select cells render as plain unclickable text with no edit affordance at all (not just a disabled button) — confirmed in both `StaffPage.tsx` and the shared roles package. The write endpoint (`entity-patch.ts`) enforces the same permission server-side regardless of what the UI shows. Needs Royce to actually sign in as one of those roles to eyeball it, since Claude doesn't hold a lower-permission test login. _(added 2026-07-27)_
- **EQ** · **Rhys Scott and Brian Griffin-Colls still need to actually renew** using the new button — the tool is ready, nobody's used it yet. **Re-verified live 2026-07-28: Rhys's licence expires today, Brian's in 4 days** — this got more urgent, not less, since first flagged. Royce to confirm once they have. _(added 2026-07-27, re-verified 2026-07-28)_
- **EQ** · **Royce to confirm live** that the loading screen now shows a clearly visible spinner instead of a black or blank pane, next time he opens Service/Field/Cards from Core. _(added 2026-07-27)_
- **EQ** · **Needs Royce's call: what to do about the still-red security scanner check.** Not urgent (verified no live exposure), but it won't turn green on its own — either wait for the linter/spreadsheet-library maintainers to catch up, or change what the check itself looks for so it stops flagging things already confirmed safe. **Re-checked live 2026-07-28: still red, same cause** — eq-solves-service's "CI" workflow, "Typecheck + audit" job, `npm audit` reports 16 high-severity findings, all from devDependency chains (`eslint-plugin-*` → `minimatch`; `exceljs`/`archiver` → `glob`/`readdir-glob` → `minimatch`) — none reachable from production code. Deliberately not touching this myself: loosening what a security gate checks is a policy call on the gate itself, not a same-scope fix, even though today's findings are all false-positive-for-this-app. Two real options if you want it green: (a) `npm audit --omit=dev` in CI (only fails on prod-dependency findings — the correct long-term fix, since dev-tooling CVEs can never be exploited in the shipped app), or (b) leave it red and just know why. _(added 2026-07-27, re-verified 2026-07-28)_
- **EQ** · **Royce to click through the new "who gets notified" Settings control** to confirm it reads clearly and saves correctly — code-complete and tested, not yet user-verified. _(added 2026-07-27)_
- **EQ** · **Needs Royce's call: is cold start still bad enough to warrant an infra change?** Everything fixable in code has shipped — the only remaining lever is moving off the serverless runtime model (always-on server or edge) to a materially faster cold start, which is a real infrastructure decision, not a quick fix. Not pursued without Royce's go-ahead. _(added 2026-07-27)_
- **EQ** · **NOT built.** Royce's call after the steelman: this is real, but not urgent, and the plan itself says it belongs post-cutover — parked. _(added 2026-07-26)_
- **EQ** · **Royce to click through the new "Who can join" Settings section and confirm it reads clearly and saves correctly** — code-complete and tested, not yet user-verified. _(added 2026-07-26)_
- **EQ** · **Royce to run one more fresh Cards signup** to confirm the nudge and the approval-time flag actually show correctly end to end — the full loop has never been walked through live since these changes landed. _(added 2026-07-26)_
- **EQ** · **Royce to test the new bulk connect-worker tool** with a real list of phone numbers. _(added 2026-07-26)_
_…and 66 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 2 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 8 | 2026-07-27 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695940/) | 1 | 2026-07-27 |
| eq-field | [TypeError: Cannot set properties of null (setting 'innerHTML')](https://eq-solutions.sentry.io/issues/136685760/) | 1 | 2026-07-27 |
| eq-field | [SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared](https://eq-solutions.sentry.io/issues/136548558/) | 1 | 2026-07-26 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-28 | eq-shell | [#1055](https://github.com/eq-solutions/eq-shell/pull/1055) hotfix(quotes): drop stale eq_bulk_update_quote_status overload |
| 2026-07-28 | eq-shell | [#1054](https://github.com/eq-solutions/eq-shell/pull/1054) fix(schema): reassert security_invoker on field_people views (eho |
| 2026-07-28 | eq-shell | [#1056](https://github.com/eq-solutions/eq-shell/pull/1056) ci(security): add blocking secret-scan gate (gitleaks) |
| 2026-07-28 | eq-shell | [#1053](https://github.com/eq-solutions/eq-shell/pull/1053) fix(quotes): capture a reason when bulk-closing quotes as lost/ca |
| 2026-07-28 | eq-solves-service | [#619](https://github.com/eq-solutions/eq-service/pull/619) fix(migrations): reconcile 2 of 5 ledger-drifted migrations, mark |
| 2026-07-28 | eq-field | [#556](https://github.com/eq-solutions/eq-field/pull/556) fix(leave): renderLeave() no-ops after navigating off the Leave p |
| 2026-07-28 | eq-field | [#555](https://github.com/eq-solutions/eq-field/pull/555) v3.5.369 — Roster: archive Labour Hire from the grid with a rehir |
| 2026-07-27 | eq-shell | [#1052](https://github.com/eq-solutions/eq-shell/pull/1052) feat: add release tagging workflow |
| 2026-07-27 | eq-shell | [#1051](https://github.com/eq-solutions/eq-shell/pull/1051) feat(staff): reorderable columns + compact Status/Contact cells |
| 2026-07-27 | eq-shell | [#1050](https://github.com/eq-solutions/eq-shell/pull/1050) ci(control-plane): gate PRs on jvkn function-drift check (--stric |
| 2026-07-27 | eq-shell | [#1049](https://github.com/eq-solutions/eq-shell/pull/1049) feat(licences): deep-link expiry email/SMS reminders to the speci |
| 2026-07-27 | eq-shell | [#1048](https://github.com/eq-solutions/eq-shell/pull/1048) feat(control-plane): jvkn function-drift CI check + backfill eq_g |
| 2026-07-27 | eq-shell | [#1047](https://github.com/eq-solutions/eq-shell/pull/1047) fix(suppliers): make login/password visibility a real Security-Gr |
| 2026-07-27 | eq-shell | [#1046](https://github.com/eq-solutions/eq-shell/pull/1046) feat(staff): inline supervisor/roster toggles + quick-edit list c |
| 2026-07-27 | eq-shell | [#1045](https://github.com/eq-solutions/eq-shell/pull/1045) feat(quotes): file-count badge on pipeline list + finish RPC stat |
_Showing 15 of 110 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **EQ Field root-cause fix not built** — task_c940a825, already running (started from the chip). Fixing the view definition at the source in EQ Field would stop this recurring a 4th time. _(added 2026-07-28)_
- **CRON_SECRET rotation** — the one real hit: a plaintext credential in vendored git history (`eq-intake/eq-platform/apps/eq-service/CHANGELOG.md`, commit `b116e4430c8`, 2026-06-10, file since deleted from the tree), described in that commit as "already set" in Netlify. Deliberately left un-allowlisted in `.gitleaks.toml` so it keeps surfacing on a full-history scan rather than going silent. Needs a decision: rotate the value in Netlify, and note the same value likely sits in `eq-solves-intake`'s own git history too, not just here. _(added 2026-07-28)_
- **Remaining audit findings not yet triaged into work** — the 6-perspective "vs industry" audit that prompted this surfaced 4 P0 / 11 P1 / 9 P2 findings across auth, authorization, multi-tenant data, frontend composition, security ops, and DX tooling. Only the secret-scan gate (above) and the field_people drift (separate section) have been acted on so far. Full findings are in a Claude.ai artifact from this session, not yet copied into repo docs — worth deciding whether it needs a permanent home before the artifact is the only record of it. _(added 2026-07-28)_
- **No live click-through was possible this session** — the local preview needs credentials this session doesn't have access to. Verified instead via automated tests, a code check, and the exact same checks GitHub runs (all passed), plus a live preview link — but nobody has actually clicked through the real feature yet. Worth a quick real check next time you're in the app. _(added 2026-07-28)_
- **`service.create`/`service.close` PermKey split** — real gap (one key gates different behaviour in Shell vs. EQ Service's ~520-usage `canWrite()`), explicitly parked: Phase 3 auth-touching work stays out of the SKS cutover window (parallel-run proving period still at 0 consecutive clean weeks as of this session). Revisit post-cutover. _(added 2026-07-27)_
- **Field's remaining ~11-file isManager→canonical-permission conversion** — same standing park as above, same reasoning. _(added 2026-07-27)_
- **SEC-9 rotation runbook** — no runbook exists yet for rotating the jvkn (eq-canonical) service_role key exposed 2026-07-12 in a chat transcript; offered to draft one (docs only, no keys touched) but session closed before Royce answered. _(added 2026-07-28)_
- **No live click-through yet** — the session's local preview browser never rendered content (tooling issue this session, browser pane wouldn't display frames at all, confirmed on both a local dev server and a real hosted deploy-preview URL). Worth a real look once merged and live. _(added 2026-07-27)_
- **"Select files to send with an email" was floated but not chosen** — Royce picked the file-count badge only. Worth revisiting if the need comes up again. _(added 2026-07-27)_
- **A weekly summary of audit activity in the existing Friday digest email** — "3 people removed, 5 PIN resets, 1 tender archived" — so Royce doesn't need to open the log cold to know if anything happened. _(added 2026-07-27)_
_…and 329 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2633 | 412 | 56 | 9 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-28 05:47 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-28 04:08 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-28 03:10 UTC → 2026-07-28 04:08 UTC)

- Merged: eq-shell [#1053](https://github.com/eq-solutions/eq-shell/pull/1053) fix(quotes): capture a reason when bulk-closing quotes as lo
- Merged: eq-shell [#1039](https://github.com/eq-solutions/eq-shell/pull/1039) fix(shell): iframe loading placeholder uses the canonical Sp
- Merged: eq-shell [#1035](https://github.com/eq-solutions/eq-shell/pull/1035) fix(auth): mint-supabase-jwt rejects cross-tenant users with
- Merged: eq-shell [#1033](https://github.com/eq-solutions/eq-shell/pull/1033) feat(attachments): drag-and-drop + multi-file upload onto qu
- Merged: eq-shell [#1031](https://github.com/eq-solutions/eq-shell/pull/1031) perf(ops): Job Creation export reads its bundled template in
- Merged: eq-shell [#1027](https://github.com/eq-solutions/eq-shell/pull/1027) chore(deps): bump @eq-solutions/ui v1.11.1 -> v1.12.0
- Merged: eq-shell [#1025](https://github.com/eq-solutions/eq-shell/pull/1025) refactor(perms): retire deprecated cards.view/cards.onboard 
- Merged: eq-solves-service [#618](https://github.com/eq-solutions/eq-service/pull/618) feat: revive release tagging (tag-release.yml)

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-cards` [minified:iL: ValidationFailure: You've already applied — wai](https://eq-solutions.sentry.io/issues/136915221/)

## 🙋 Waiting on you (84)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Batch Fill's new Team toggle (compose/select) behaves differently from the Timesheets batch modal's existing Team filter (narrows the list)** — same idea, two different behaviours in two similar screens of the same app. Flagged for Royce's call, not resolved. _(added 2026-07-27)_
- **EQ** · **Fix sign-in logging at the source — real, but bigger and more sensitive than "simple," needs Royce's explicit go-ahead first.** It writes a fresh record every time the app re-checks you're signed in (reopening a tab, switching back to it, a reload) — real timestamps pulled from Royce's own login history show this firing anywhere from 26 seconds to 23 minutes apart, not on any fixed clock (an earlier note here claiming "every ~14 minutes" was wrong — that figure came from an unrelated eq-shell bug, not from anything measured against Field's own data, and has been corrected). Rolling repeat checks into one row would shrink the table at the source instead of just hiding it in the view. Steelmanned before touching anything: this changes what a live, load-bearing security control (`verify-pin.js`, every SKS sign-in) actually writes, not just a display filter — a genuinely different risk class from the rest of this session's work, and this repo's own rules require explicit sign-off before an auth-adjacent change like this ships. Not scoped or built — ended on a question back to Royce (scope it now, or leave parked) that hadn't been answered when this session closed. _(added 2026-07-27)_
- **EQ** · **Live click-through as a lower-permission user (employee/apprentice/labour-hire/subcontractor) still not done** — verified instead by reading the code directly: those roles all lack `field.dispatch`, and without it the new checkboxes render natively `disabled` and the inline text/select cells render as plain unclickable text with no edit affordance at all (not just a disabled button) — confirmed in both `StaffPage.tsx` and the shared roles package. The write endpoint (`entity-patch.ts`) enforces the same permission server-side regardless of what the UI shows. Needs Royce to actually sign in as one of those roles to eyeball it, since Claude doesn't hold a lower-permission test login. _(added 2026-07-27)_
- **EQ** · **Rhys Scott and Brian Griffin-Colls still need to actually renew** using the new button — the tool is ready, nobody's used it yet. Royce to confirm once they have. _(added 2026-07-27)_
- **EQ** · **Royce to confirm live** that the loading screen now shows a clearly visible spinner instead of a black or blank pane, next time he opens Service/Field/Cards from Core. _(added 2026-07-27)_
- **EQ** · **Needs Royce's call: what to do about the still-red security scanner check.** Not urgent (verified no live exposure), but it won't turn green on its own — either wait for the linter/spreadsheet-library maintainers to catch up, or change what the check itself looks for so it stops flagging things already confirmed safe. _(added 2026-07-27)_
- **EQ** · **Royce to click through the new "who gets notified" Settings control** to confirm it reads clearly and saves correctly — code-complete and tested, not yet user-verified. _(added 2026-07-27)_
- **EQ** · **Needs Royce's call: is cold start still bad enough to warrant an infra change?** Everything fixable in code has shipped — the only remaining lever is moving off the serverless runtime model (always-on server or edge) to a materially faster cold start, which is a real infrastructure decision, not a quick fix. Not pursued without Royce's go-ahead. _(added 2026-07-27)_
- **EQ** · **NOT built.** Royce's call after the steelman: this is real, but not urgent, and the plan itself says it belongs post-cutover — parked. _(added 2026-07-26)_
- **EQ** · **Royce to click through the new "Who can join" Settings section and confirm it reads clearly and saves correctly** — code-complete and tested, not yet user-verified. _(added 2026-07-26)_
- **EQ** · **Royce to run one more fresh Cards signup** to confirm the nudge and the approval-time flag actually show correctly end to end — the full loop has never been walked through live since these changes landed. _(added 2026-07-26)_
- **EQ** · **Royce to test the new bulk connect-worker tool** with a real list of phone numbers. _(added 2026-07-26)_
_…and 72 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 1 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 8 | 2026-07-27 |
| eq-cards | [minified:iL: ValidationFailure: You've already applied — waiting on a decision.](https://eq-solutions.sentry.io/issues/136915221/) | 1 | 2026-07-28 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695940/) | 1 | 2026-07-27 |
| eq-field | [TypeError: Cannot set properties of null (setting 'innerHTML')](https://eq-solutions.sentry.io/issues/136685760/) | 1 | 2026-07-27 |
| eq-field | [SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared](https://eq-solutions.sentry.io/issues/136548558/) | 1 | 2026-07-26 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-28 | eq-shell | [#1053](https://github.com/eq-solutions/eq-shell/pull/1053) fix(quotes): capture a reason when bulk-closing quotes as lost/ca |
| 2026-07-28 | eq-field | [#555](https://github.com/eq-solutions/eq-field/pull/555) v3.5.369 — Roster: archive Labour Hire from the grid with a rehir |
| 2026-07-27 | eq-shell | [#1052](https://github.com/eq-solutions/eq-shell/pull/1052) feat: add release tagging workflow |
| 2026-07-27 | eq-shell | [#1051](https://github.com/eq-solutions/eq-shell/pull/1051) feat(staff): reorderable columns + compact Status/Contact cells |
| 2026-07-27 | eq-shell | [#1050](https://github.com/eq-solutions/eq-shell/pull/1050) ci(control-plane): gate PRs on jvkn function-drift check (--stric |
| 2026-07-27 | eq-shell | [#1049](https://github.com/eq-solutions/eq-shell/pull/1049) feat(licences): deep-link expiry email/SMS reminders to the speci |
| 2026-07-27 | eq-shell | [#1048](https://github.com/eq-solutions/eq-shell/pull/1048) feat(control-plane): jvkn function-drift CI check + backfill eq_g |
| 2026-07-27 | eq-shell | [#1047](https://github.com/eq-solutions/eq-shell/pull/1047) fix(suppliers): make login/password visibility a real Security-Gr |
| 2026-07-27 | eq-shell | [#1046](https://github.com/eq-solutions/eq-shell/pull/1046) feat(staff): inline supervisor/roster toggles + quick-edit list c |
| 2026-07-27 | eq-shell | [#1045](https://github.com/eq-solutions/eq-shell/pull/1045) feat(quotes): file-count badge on pipeline list + finish RPC stat |
| 2026-07-27 | eq-shell | [#1044](https://github.com/eq-solutions/eq-shell/pull/1044) fix(quotes): retire 4 dead status values, merge verbal-win, add C |
| 2026-07-27 | eq-shell | [#1043](https://github.com/eq-solutions/eq-shell/pull/1043) fix(shell): EQ Field is missing its Records nav + rail opens on a |
| 2026-07-27 | eq-shell | [#1042](https://github.com/eq-solutions/eq-shell/pull/1042) fix(service-embed): explain the preview block instead of hanging  |
| 2026-07-27 | eq-shell | [#1041](https://github.com/eq-solutions/eq-shell/pull/1041) fix(attachments): list/upload-attachment hit the control plane, n |
| 2026-07-27 | eq-shell | [#1040](https://github.com/eq-solutions/eq-shell/pull/1040) fix(attachments): codify app_data.attachments — was hand-created, |
_Showing 15 of 109 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **No live click-through was possible this session** — the local preview needs credentials this session doesn't have access to. Verified instead via automated tests, a code check, and the exact same checks GitHub runs (all passed), plus a live preview link — but nobody has actually clicked through the real feature yet. Worth a quick real check next time you're in the app. _(added 2026-07-28)_
- **`service.create`/`service.close` PermKey split** — real gap (one key gates different behaviour in Shell vs. EQ Service's ~520-usage `canWrite()`), explicitly parked: Phase 3 auth-touching work stays out of the SKS cutover window (parallel-run proving period still at 0 consecutive clean weeks as of this session). Revisit post-cutover. _(added 2026-07-27)_
- **Field's remaining ~11-file isManager→canonical-permission conversion** — same standing park as above, same reasoning. _(added 2026-07-27)_
- **SEC-9 rotation runbook** — no runbook exists yet for rotating the jvkn (eq-canonical) service_role key exposed 2026-07-12 in a chat transcript; offered to draft one (docs only, no keys touched) but session closed before Royce answered. _(added 2026-07-28)_
- **No live click-through yet** — the session's local preview browser never rendered content (tooling issue this session, browser pane wouldn't display frames at all, confirmed on both a local dev server and a real hosted deploy-preview URL). Worth a real look once merged and live. _(added 2026-07-27)_
- **Bulk "change status" on multiple quotes at once still doesn't capture a reason when closing as lost/cancelled** — only closing one quote at a time does. Known gap, not built. _(added 2026-07-27)_
- **"Select files to send with an email" was floated but not chosen** — Royce picked the file-count badge only. Worth revisiting if the need comes up again. _(added 2026-07-27)_
- **A weekly summary of audit activity in the existing Friday digest email** — "3 people removed, 5 PIN resets, 1 tender archived" — so Royce doesn't need to open the log cold to know if anything happened. _(added 2026-07-27)_
- **Proactive alert on the highest-stakes actions** (a permanent delete, a bulk PIN reset) — push a notification the moment it happens rather than waiting for someone to think to check. _(added 2026-07-27)_
- **Excel workbook auditing the 478-item EQ backlog (why it grew this large, dashboard + root-cause) — spun off as its own background session** (`task_a6f9b5d8`), running independently, not concluded this session. _(added 2026-07-27)_
_…and 327 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2596 | 414 | 51 | 9 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-28 04:08 UTC._

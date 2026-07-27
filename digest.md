---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-27 13:03 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-27 12:40 UTC → 2026-07-27 13:03 UTC)

- Merged: eq-shell [#1036](https://github.com/eq-solutions/eq-shell/pull/1036) fix(security): close 2 more cross-tenant lookup bugs + add s
- Merged: eq-shell [#1034](https://github.com/eq-solutions/eq-shell/pull/1034) fix(admin): resolve cross-tenant user lookup in eq_get_tenan
- Merged: eq-shell [#1030](https://github.com/eq-solutions/eq-shell/pull/1030) fix(staff): Photo ID requirement satisfied by driver licence
- Merged: eq-shell [#1029](https://github.com/eq-solutions/eq-shell/pull/1029) feat(settings): nominate specific recipients for new-join-re
- Merged: eq-shell [#1028](https://github.com/eq-solutions/eq-shell/pull/1028) fix(security): close anon-EXECUTE gap on zaap/ehow Ops+Quote
- Merged: eq-shell [#1026](https://github.com/eq-solutions/eq-shell/pull/1026) refactor(access-control): derive the role-matrix perm list f
- Merged: eq-shell [#1023](https://github.com/eq-solutions/eq-shell/pull/1023) chore(deps): bump @eq-solutions/roles to v2.5.7
- Merged: eq-solves-service [#617](https://github.com/eq-solutions/eq-service/pull/617) fix(archive): rewrite hard-delete + restore for canonical wr

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (83)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Batch Fill's new Team toggle (compose/select) behaves differently from the Timesheets batch modal's existing Team filter (narrows the list)** — same idea, two different behaviours in two similar screens of the same app. Flagged for Royce's call, not resolved. _(added 2026-07-27)_
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
- **EQ** · **Royce to check the Netlify dashboard for `ENFORCE_IFRAME_ORIGIN`** on eq-shell — confirms whether the iframe-origin check is actually enforcing in production (not just in code). Not readable via the connected tools. _(added 2026-07-26)_
_…and 71 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

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
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 10 | 2026-07-23 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 7 | 2026-07-26 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 6 | 2026-07-23 |
| eq-field | [ReferenceError: openLeaveRequest is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 2 | 2026-07-26 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695940/) | 1 | 2026-07-27 |
| eq-field | [TypeError: Cannot set properties of null (setting 'innerHTML')](https://eq-solutions.sentry.io/issues/136685760/) | 1 | 2026-07-27 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
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
| 2026-07-27 | eq-shell | [#1038](https://github.com/eq-solutions/eq-shell/pull/1038) chore: remove dead cards-staff-matches.ts |
| 2026-07-27 | eq-shell | [#1039](https://github.com/eq-solutions/eq-shell/pull/1039) fix(shell): iframe loading placeholder uses the canonical Spinner |
| 2026-07-27 | eq-shell | [#1037](https://github.com/eq-solutions/eq-shell/pull/1037) fix(shell): white background on iframe loading pane, not near-bla |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **No live click-through yet** — the session's local preview browser never rendered content (tooling issue this session, browser pane wouldn't display frames at all, confirmed on both a local dev server and a real hosted deploy-preview URL). Worth a real look once merged and live. _(added 2026-07-27)_
- **Bulk "change status" on multiple quotes at once still doesn't capture a reason when closing as lost/cancelled** — only closing one quote at a time does. Known gap, not built. _(added 2026-07-27)_
- **"Select files to send with an email" was floated but not chosen** — Royce picked the file-count badge only. Worth revisiting if the need comes up again. _(added 2026-07-27)_
- **Excel workbook auditing the 478-item EQ backlog (why it grew this large, dashboard + root-cause) — spun off as its own background session** (`task_a6f9b5d8`), running independently, not concluded this session. _(added 2026-07-27)_
- **Habit note, not a task**: after pulling any `@eq-solutions/*` package-version bump, run `pnpm install` before trusting a local `tsc -b` failure as a real regression — this one cost investigation time chasing a phantom code bug. _(added 2026-07-27)_
- **Latent sibling risk, not fixed**: the Leave toolbar's other buttons (CC List, Archive Resolved, Show Archived, Print, the status-filter/search `renderLeave()` calls) call `leave.js` globals directly and unguarded, with the exact same lazy-load race as the button just fixed — just not yet caught by Sentry. Deliberately left out of this PR to keep it scoped to the confirmed crash; worth a small follow-up sweep applying the same `openLeaveRequestSafe()`-style guard to the rest of that toolbar. _(added 2026-07-27)_
- **NOT built either** — session pivoted to SKS Field cutover work before this was actioned. Low urgency (nothing found actively exploiting these), but real; worth a short session on its own. _(added 2026-07-26)_
- **The remaining 4 SKS-specific permission tweaks are intentional, not a to-do list** — flagged here only so a future session doesn't mistake "still has one-off tweaks" for "cleanup incomplete." No action needed unless the underlying product decision changes.
- **Cards' two deprecated permissions still actively granted** — should be replaced with the correct mechanism instead. Spun off as its own background task, not done this session. _(added 2026-07-26)_
- **Hit the recurring "two sessions, one folder" hazard again mid-task** — another concurrent session was actively working in the same shared eq-shell folder at the same time, on a different branch, with its own unsaved work in progress. Worked around it safely (moved to an isolated copy, touched nothing of theirs) — no data lost, but this is the same known hazard logged elsewhere in this file, not a new one. _(added 2026-07-26)_
_…and 324 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
- **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_
_…and 58 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2551 | 410 | 34 | 12 |
| [SKS](sks/pending.md) | 429 | 75 | 12 | 13 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 382 | 34 | 7 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-27 | [eq-ui design handoff shipped + propagated to eq-shell/eq-service, real bugs found along the way](sessions/2026-07-27.md) |
| 2026-07-26 | [Customers page speed fix, Job Creation export bug found+fixed, customer-level default End Client, Ops quote-form layout](sessions/2026-07-26.md) |
| 2026-07-25 | [Closed out the Coupa/staff-reactivation thread from the day before: merged PR #993, dispatched the ledger reconcile, explained the migration-numbering saga](sessions/2026-07-25.md) |
| 2026-07-24 | [EQ Ops quote-detail panel simplified + Coupa PO import rebuilt against the real export](sessions/2026-07-24.md) |
| 2026-07-23 | [Closed the crm-write/canonical-api entitlement design pass: no gate needed](sessions/2026-07-23.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-27 13:03 UTC._

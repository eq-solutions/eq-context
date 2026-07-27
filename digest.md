---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-27 02:26 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-27 01:55 UTC → 2026-07-27 02:26 UTC)

- Merged: eq-shell [#1034](https://github.com/eq-solutions/eq-shell/pull/1034) fix(admin): resolve cross-tenant user lookup in eq_get_tenan
- Merged: eq-shell [#1020](https://github.com/eq-solutions/eq-shell/pull/1020) chore(styles): remove dead duplicate TenantHome AI-brief CSS
- Merged: eq-shell [#1018](https://github.com/eq-solutions/eq-shell/pull/1018) feat(dashboard): scannable AI brief, self-evident action ran
- Merged: eq-shell [#1015](https://github.com/eq-solutions/eq-shell/pull/1015) feat(settings): move the join-requirements switch out of Tra
- Merged: eq-shell [#1013](https://github.com/eq-solutions/eq-shell/pull/1013) feat(retention): ADR-005 leaver data retention — deactivated
- Merged: eq-shell [#1012](https://github.com/eq-solutions/eq-shell/pull/1012) feat(cards): title-case onboarding names + admin switch for 
- Merged: eq-shell [#1011](https://github.com/eq-solutions/eq-shell/pull/1011) fix(access-control): add subcontractor to tenant_role_overri
- Merged: eq-shell [#1010](https://github.com/eq-solutions/eq-shell/pull/1010) docs(ledger): record retire_credentials_canonical_sync as ap

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-12 (P0 — confirmed exposure, same class as SEC-9/SEC-10) — Several real secrets on **eq-shell's own** Netlify project stored with `is_secre · [security-register.md](ops/security-register.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 10 | 2026-07-23 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 7 | 2026-07-26 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 6 | 2026-07-23 |
| eq-field | [ReferenceError: openLeaveRequest is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 2 | 2026-07-26 |
| eq-field | [TypeError: Cannot set properties of null (setting 'innerHTML')](https://eq-solutions.sentry.io/issues/136685760/) | 1 | 2026-07-27 |
| eq-field | [SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared](https://eq-solutions.sentry.io/issues/136548558/) | 1 | 2026-07-26 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-27 | eq-shell | [#1034](https://github.com/eq-solutions/eq-shell/pull/1034) fix(admin): resolve cross-tenant user lookup in eq_get_tenant_use |
| 2026-07-27 | eq-shell | [#1033](https://github.com/eq-solutions/eq-shell/pull/1033) feat(attachments): drag-and-drop + multi-file upload onto quote/j |
| 2026-07-27 | eq-solves-service | [#606](https://github.com/eq-solutions/eq-service/pull/606) feat(shell): branded loading spinner on the iframe sign-in handof |
| 2026-07-27 | eq-field | [#543](https://github.com/eq-solutions/eq-field/pull/543) v3.5.359 — Leave toolbar: close the same lazy-load race on 7 more |
| 2026-07-27 | eq-field | [#542](https://github.com/eq-solutions/eq-field/pull/542) v3.5.358 — fix 2 live Sentry errors: duplicate INCIDENT_TYPES + l |
| 2026-07-26 | eq-shell | [#1029](https://github.com/eq-solutions/eq-shell/pull/1029) feat(settings): nominate specific recipients for new-join-request |
| 2026-07-26 | eq-shell | [#1028](https://github.com/eq-solutions/eq-shell/pull/1028) fix(security): close anon-EXECUTE gap on zaap/ehow Ops+Quotes RPC |
| 2026-07-26 | eq-shell | [#1031](https://github.com/eq-solutions/eq-shell/pull/1031) perf(ops): Job Creation export reads its bundled template instead |
| 2026-07-26 | eq-shell | [#1030](https://github.com/eq-solutions/eq-shell/pull/1030) fix(staff): Photo ID requirement satisfied by driver licence or p |
| 2026-07-26 | eq-shell | [#1027](https://github.com/eq-solutions/eq-shell/pull/1027) chore(deps): bump @eq-solutions/ui v1.11.1 -> v1.12.0 |
| 2026-07-26 | eq-shell | [#1026](https://github.com/eq-solutions/eq-shell/pull/1026) refactor(access-control): derive the role-matrix perm list from t |
| 2026-07-26 | eq-shell | [#1025](https://github.com/eq-solutions/eq-shell/pull/1025) refactor(perms): retire deprecated cards.view/cards.onboard entir |
| 2026-07-26 | eq-shell | [#1023](https://github.com/eq-solutions/eq-shell/pull/1023) chore(deps): bump @eq-solutions/roles to v2.5.7 |
| 2026-07-26 | eq-shell | [#1021](https://github.com/eq-solutions/eq-shell/pull/1021) refactor(perms): collapse hand-typed module matrices to derive fr |
| 2026-07-26 | eq-shell | [#1022](https://github.com/eq-solutions/eq-shell/pull/1022) feat(access-model): canWithReason() + why-can.ts diagnostic scrip |
_Showing 15 of 114 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Latent sibling risk, not fixed**: the Leave toolbar's other buttons (CC List, Archive Resolved, Show Archived, Print, the status-filter/search `renderLeave()` calls) call `leave.js` globals directly and unguarded, with the exact same lazy-load race as the button just fixed — just not yet caught by Sentry. Deliberately left out of this PR to keep it scoped to the confirmed crash; worth a small follow-up sweep applying the same `openLeaveRequestSafe()`-style guard to the rest of that toolbar. _(added 2026-07-27)_
- **Root cause of the blank screen itself is still open**: the middleware (`proxy.ts`) does a full Supabase auth round-trip before any HTML reaches the browser on a fresh Shell embed — no client-side loading UI can paint over that gap. Worth a dedicated latency investigation if the blank-screen complaint persists after this spinner ships. _(added 2026-07-27)_
- **NOT built.** Royce's call after the steelman: this is real, but not urgent, and the plan itself says it belongs post-cutover — parked. _(added 2026-07-26)_
- **NOT built either** — session pivoted to SKS Field cutover work before this was actioned. Low urgency (nothing found actively exploiting these), but real; worth a short session on its own. _(added 2026-07-26)_
- **The remaining 4 SKS-specific permission tweaks are intentional, not a to-do list** — flagged here only so a future session doesn't mistake "still has one-off tweaks" for "cleanup incomplete." No action needed unless the underlying product decision changes.
- **Cards' two deprecated permissions still actively granted** — should be replaced with the correct mechanism instead. Spun off as its own background task, not done this session. _(added 2026-07-26)_
- **Hit the recurring "two sessions, one folder" hazard again mid-task** — another concurrent session was actively working in the same shared eq-shell folder at the same time, on a different branch, with its own unsaved work in progress. Worked around it safely (moved to an isolated copy, touched nothing of theirs) — no data lost, but this is the same known hazard logged elsewhere in this file, not a new one. _(added 2026-07-26)_
- **Royce to click through the new "Who can join" Settings section and confirm it reads clearly and saves correctly** — code-complete and tested, not yet user-verified. _(added 2026-07-26)_
- **Royce to run one more fresh Cards signup** to confirm the nudge and the approval-time flag actually show correctly end to end — the full loop has never been walked through live since these changes landed. _(added 2026-07-26)_
- **Royce to test the new bulk connect-worker tool** with a real list of phone numbers. _(added 2026-07-26)_
_…and 465 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Still open — Royce to confirm: does SKS Indigenous Technologies need its own isolation** (separate from the state/division access model), given it's a distinct MD-led entity that may carry its own compliance obligations (e.g. Indigenous procurement certification)? Flagged, not answered. _(added 2026-07-23)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
_…and 68 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 2994 | 477 | 148 |
| [SKS](sks/pending.md) | 545 | 78 | 95 |
| [SKS active](sks/active.md) | 109 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-27 02:26 UTC._

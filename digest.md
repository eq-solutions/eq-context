---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-27 09:50 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-27 09:48 UTC → 2026-07-27 09:50 UTC)

- Merged: eq-shell [#1030](https://github.com/eq-solutions/eq-shell/pull/1030) fix(staff): Photo ID requirement satisfied by driver licence
- Merged: eq-shell [#1029](https://github.com/eq-solutions/eq-shell/pull/1029) feat(settings): nominate specific recipients for new-join-re
- Merged: eq-shell [#1028](https://github.com/eq-solutions/eq-shell/pull/1028) fix(security): close anon-EXECUTE gap on zaap/ehow Ops+Quote
- Merged: eq-shell [#1026](https://github.com/eq-solutions/eq-shell/pull/1026) refactor(access-control): derive the role-matrix perm list f
- Merged: eq-shell [#1023](https://github.com/eq-solutions/eq-shell/pull/1023) chore(deps): bump @eq-solutions/roles to v2.5.7
- Merged: eq-shell [#1022](https://github.com/eq-solutions/eq-shell/pull/1022) feat(access-model): canWithReason() + why-can.ts diagnostic 
- Merged: eq-shell [#1020](https://github.com/eq-solutions/eq-shell/pull/1020) chore(styles): remove dead duplicate TenantHome AI-brief CSS
- Merged: eq-shell [#1015](https://github.com/eq-solutions/eq-shell/pull/1015) feat(settings): move the join-requirements switch out of Tra

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 5 | 0d |
| eq-field | ? unknown | ? | 0 | — |
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
| eq-field | [SyntaxError: Identifier '_ROSTER_WEEKDAYS' has already been declared](https://eq-solutions.sentry.io/issues/136749375/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 1 | 2026-07-27 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695940/) | 1 | 2026-07-27 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-27 | eq-shell | [#1044](https://github.com/eq-solutions/eq-shell/pull/1044) fix(quotes): retire 4 dead status values, merge verbal-win, add C |
| 2026-07-27 | eq-shell | [#1043](https://github.com/eq-solutions/eq-shell/pull/1043) fix(shell): EQ Field is missing its Records nav + rail opens on a |
| 2026-07-27 | eq-shell | [#1042](https://github.com/eq-solutions/eq-shell/pull/1042) fix(service-embed): explain the preview block instead of hanging  |
| 2026-07-27 | eq-shell | [#1041](https://github.com/eq-solutions/eq-shell/pull/1041) fix(attachments): list/upload-attachment hit the control plane, n |
| 2026-07-27 | eq-shell | [#1040](https://github.com/eq-solutions/eq-shell/pull/1040) fix(attachments): codify app_data.attachments — was hand-created, |
| 2026-07-27 | eq-shell | [#1038](https://github.com/eq-solutions/eq-shell/pull/1038) chore: remove dead cards-staff-matches.ts |
| 2026-07-27 | eq-shell | [#1039](https://github.com/eq-solutions/eq-shell/pull/1039) fix(shell): iframe loading placeholder uses the canonical Spinner |
| 2026-07-27 | eq-shell | [#1037](https://github.com/eq-solutions/eq-shell/pull/1037) fix(shell): white background on iframe loading pane, not near-bla |
| 2026-07-27 | eq-shell | [#1036](https://github.com/eq-solutions/eq-shell/pull/1036) fix(security): close 2 more cross-tenant lookup bugs + add shared |
| 2026-07-27 | eq-shell | [#1035](https://github.com/eq-solutions/eq-shell/pull/1035) fix(auth): mint-supabase-jwt rejects cross-tenant users with a 40 |
| 2026-07-27 | eq-shell | [#1034](https://github.com/eq-solutions/eq-shell/pull/1034) fix(admin): resolve cross-tenant user lookup in eq_get_tenant_use |
| 2026-07-27 | eq-shell | [#1033](https://github.com/eq-solutions/eq-shell/pull/1033) feat(attachments): drag-and-drop + multi-file upload onto quote/j |
| 2026-07-27 | eq-solves-service | [#615](https://github.com/eq-solutions/eq-service/pull/615) fix(security): redirect responses now carry the security headers  |
| 2026-07-27 | eq-solves-service | [#614](https://github.com/eq-solutions/eq-service/pull/614) feat(migrations): add --verify checksum step, wire into PR plan ( |
| 2026-07-27 | eq-solves-service | [#613](https://github.com/eq-solutions/eq-service/pull/613) fix(dev): allow localhost framing in development CSP |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Royce to confirm live** that the loading screen now shows a clearly visible spinner instead of a black or blank pane, next time he opens Service/Field/Cards from Core. _(added 2026-07-27)_
- **Royce to click through the new "who gets notified" Settings control** to confirm it reads clearly and saves correctly — code-complete and tested, not yet user-verified. _(added 2026-07-27)_
- **Habit note, not a task**: after pulling any `@eq-solutions/*` package-version bump, run `pnpm install` before trusting a local `tsc -b` failure as a real regression — this one cost investigation time chasing a phantom code bug. _(added 2026-07-27)_
- **Latent sibling risk, not fixed**: the Leave toolbar's other buttons (CC List, Archive Resolved, Show Archived, Print, the status-filter/search `renderLeave()` calls) call `leave.js` globals directly and unguarded, with the exact same lazy-load race as the button just fixed — just not yet caught by Sentry. Deliberately left out of this PR to keep it scoped to the confirmed crash; worth a small follow-up sweep applying the same `openLeaveRequestSafe()`-style guard to the rest of that toolbar. _(added 2026-07-27)_
- **Needs Royce's call: is cold start still bad enough to warrant an infra change?** Everything fixable in code has shipped — the only remaining lever is moving off the serverless runtime model (always-on server or edge) to a materially faster cold start, which is a real infrastructure decision, not a quick fix. Not pursued without Royce's go-ahead. _(added 2026-07-27)_
- **NOT built.** Royce's call after the steelman: this is real, but not urgent, and the plan itself says it belongs post-cutover — parked. _(added 2026-07-26)_
- **NOT built either** — session pivoted to SKS Field cutover work before this was actioned. Low urgency (nothing found actively exploiting these), but real; worth a short session on its own. _(added 2026-07-26)_
- **The remaining 4 SKS-specific permission tweaks are intentional, not a to-do list** — flagged here only so a future session doesn't mistake "still has one-off tweaks" for "cleanup incomplete." No action needed unless the underlying product decision changes.
- **Cards' two deprecated permissions still actively granted** — should be replaced with the correct mechanism instead. Spun off as its own background task, not done this session. _(added 2026-07-26)_
- **Hit the recurring "two sessions, one folder" hazard again mid-task** — another concurrent session was actively working in the same shared eq-shell folder at the same time, on a different branch, with its own unsaved work in progress. Worked around it safely (moved to an isolated copy, touched nothing of theirs) — no data lost, but this is the same known hazard logged elsewhere in this file, not a new one. _(added 2026-07-26)_
_…and 466 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- Push `sks-charters` to a real GitHub remote (e.g.
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Royce to click-test it himself** — confirmed the deploy went out and the new code is live (checked the page's actual HTML directly), but couldn't finish a full live drag-and-drop test this session due to browser tooling instability. _(added 2026-07-27)_
- **Still open — Royce to confirm: does SKS Indigenous Technologies need its own isolation** (separate from the state/division access model), given it's a distinct MD-led entity that may carry its own compliance obligations (e.g. Indigenous procurement certification)? Flagged, not answered. _(added 2026-07-23)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
_…and 70 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 3036 | 478 | 163 |
| [SKS](sks/pending.md) | 569 | 80 | 97 |
| [SKS active](sks/active.md) | 109 | 0 | 0 |
| [OPS](ops/pending.md) | 373 | 34 | 12 |

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-27 09:50 UTC._

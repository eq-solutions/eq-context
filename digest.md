---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-26
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-26 09:52 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-26 09:37 UTC → 2026-07-26 09:52 UTC)

- Merged: eq-shell [#1026](https://github.com/eq-solutions/eq-shell/pull/1026) refactor(access-control): derive the role-matrix perm list f
- Merged: eq-shell [#1008](https://github.com/eq-solutions/eq-shell/pull/1008) fix(cards): invite-approval path used an invalid role enum v
- Merged: eq-shell [#1006](https://github.com/eq-solutions/eq-shell/pull/1006) chore: remove one-time Sentry alert-apply workflow
- Merged: eq-shell [#1003](https://github.com/eq-solutions/eq-shell/pull/1003) chore(deps): bump @eq-solutions/ui to v1.11.1 (cascading fil
- Merged: eq-shell [#1000](https://github.com/eq-solutions/eq-shell/pull/1000) chore(migrations): renumber 0202/0203 Coupa PO collisions ->
- Merged: eq-shell [#998](https://github.com/eq-solutions/eq-shell/pull/998) feat(customers,quotes): customer-level default End Client
- Merged: eq-shell [#996](https://github.com/eq-solutions/eq-shell/pull/996) fix+feat(quotes): Coupa PO import — fix the broken write pat
- Merged: eq-solves-service [#603](https://github.com/eq-solutions/eq-service/pull/603) chore(deps): bump @eq-solutions/roles v2.5.3 -> v2.5.5

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-12 (P0 — confirmed exposure, same class as SEC-9/SEC-10) — Several real secrets on **eq-shell's own** Netlify project stored with `is_secre · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 1 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 10 | 2026-07-23 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 6 | 2026-07-25 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 6 | 2026-07-23 |
| eq-field | [ReferenceError: openLeaveRequest is not defined](https://eq-solutions.sentry.io/issues/130706295/) | 2 | 2026-07-26 |
| eq-field | [SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared](https://eq-solutions.sentry.io/issues/136548558/) | 1 | 2026-07-26 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-26 | eq-shell | [#1026](https://github.com/eq-solutions/eq-shell/pull/1026) refactor(access-control): derive the role-matrix perm list from t |
| 2026-07-26 | eq-shell | [#1025](https://github.com/eq-solutions/eq-shell/pull/1025) refactor(perms): retire deprecated cards.view/cards.onboard entir |
| 2026-07-26 | eq-shell | [#1023](https://github.com/eq-solutions/eq-shell/pull/1023) chore(deps): bump @eq-solutions/roles to v2.5.7 |
| 2026-07-26 | eq-shell | [#1021](https://github.com/eq-solutions/eq-shell/pull/1021) refactor(perms): collapse hand-typed module matrices to derive fr |
| 2026-07-26 | eq-shell | [#1022](https://github.com/eq-solutions/eq-shell/pull/1022) feat(access-model): canWithReason() + why-can.ts diagnostic scrip |
| 2026-07-26 | eq-shell | [#1019](https://github.com/eq-solutions/eq-shell/pull/1019) feat(cards): bulk connect-worker mode, respecting the existing ra |
| 2026-07-26 | eq-shell | [#1020](https://github.com/eq-solutions/eq-shell/pull/1020) chore(styles): remove dead duplicate TenantHome AI-brief CSS bloc |
| 2026-07-26 | eq-shell | [#1016](https://github.com/eq-solutions/eq-shell/pull/1016) fix(perms): close check-perm-sync.mjs under-grant blind spot + wi |
| 2026-07-26 | eq-shell | [#1018](https://github.com/eq-solutions/eq-shell/pull/1018) feat(dashboard): scannable AI brief, self-evident action ranking |
| 2026-07-26 | eq-shell | [#1017](https://github.com/eq-solutions/eq-shell/pull/1017) feat(settings): required-tickets picker alongside Who can join |
| 2026-07-26 | eq-shell | [#1015](https://github.com/eq-solutions/eq-shell/pull/1015) feat(settings): move the join-requirements switch out of Training |
| 2026-07-26 | eq-shell | [#1011](https://github.com/eq-solutions/eq-shell/pull/1011) fix(access-control): add subcontractor to tenant_role_overrides C |
| 2026-07-26 | eq-shell | [#1014](https://github.com/eq-solutions/eq-shell/pull/1014) feat(cards): surface the join-requirement gap at approval time |
| 2026-07-26 | eq-shell | [#1013](https://github.com/eq-solutions/eq-shell/pull/1013) feat(retention): ADR-005 leaver data retention — deactivated_at + |
| 2026-07-26 | eq-shell | [#1012](https://github.com/eq-solutions/eq-shell/pull/1012) feat(cards): title-case onboarding names + admin switch for join  |
_Showing 15 of 115 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **"Not a duplicate" dismiss mechanism** — needs a schema change (e.g. `dupe_ack` column), flagged as a product decision, not built. _(added 2026-07-26)_
- **Editing Currency in Verify doesn't re-trigger the FX conversion** — `total`/`fx_rate`/`original_total` stay derived from the original (possibly wrong) currency; needs a product call on auto-refetch vs. warn-and-fix-manually. _(added 2026-07-26)_
- **`poll-batch` edge function can double-ingest a batch job under two concurrent calls** — the "already ingested" guard isn't set until the whole ingest loop finishes. Currently latent, zero client callers of that path today, but real the moment it ships. _(added 2026-07-26)_
- **Only 2 of eq-ui's 13 components have any tests** (Modal, Table) despite the test setup already being there — the stateful ones most worth covering (DropdownMenu, Toast, Tabs, AppShell) have zero. _(added 2026-07-26)_
- **No accessibility testing on eq-ui at all** — Modal/DropdownMenu/Tabs are exactly the kind of components (focus traps, keyboard nav) where this matters most. Note: this overlaps with the older, already-tracked a11y backlog items further down this file (A7–A10). _(added 2026-07-26)_
- **No linting in eq-ui's CI** — eq-field's build-less app actually has more lint discipline (a throwaway `npx eslint` run) than eq-ui does despite eq-ui having full npm tooling. _(added 2026-07-26)_
- **No visual/Storybook-style review tool for eq-ui** — downgraded from "build Storybook" to "maybe a simple one-page kitchen-sink view" given the team's current size; lowest priority of the four. _(added 2026-07-26)_
- **The remaining 4 SKS-specific permission tweaks are intentional, not a to-do list** — flagged here only so a future session doesn't mistake "still has one-off tweaks" for "cleanup incomplete." No action needed unless the underlying product decision changes.
- **Cards' two deprecated permissions still actively granted** — should be replaced with the correct mechanism instead. Spun off as its own background task, not done this session. _(added 2026-07-26)_
- **Hit the recurring "two sessions, one folder" hazard again mid-task** — another concurrent session was actively working in the same shared eq-shell folder at the same time, on a different branch, with its own unsaved work in progress. Worked around it safely (moved to an isolated copy, touched nothing of theirs) — no data lost, but this is the same known hazard logged elsewhere in this file, not a new one. _(added 2026-07-26)_
_…and 468 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Needs a real click-through before trusting it fully** — set a Market Vertical + invoice email on a real customer, then pull a fresh Job Creation export on one of their jobs and check the 3 cells actually come out right. _(added 2026-07-23)_
- **Still open — Royce to confirm: does SKS Indigenous Technologies need its own isolation** (separate from the state/division access model), given it's a distinct MD-led entity that may carry its own compliance obligations (e.g. Indigenous procurement certification)? Flagged, not answered. _(added 2026-07-23)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
_…and 67 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 2879 | 480 | 97 |
| [SKS](sks/pending.md) | 522 | 77 | 87 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-26 | [Customers page speed fix, Job Creation export bug found+fixed, customer-level default End Client, Ops quote-form layout](sessions/2026-07-26.md) |
| 2026-07-25 | [Closed out the Coupa/staff-reactivation thread from the day before: merged PR #993, dispatched the ledger reconcile, explained the migration-numbering saga](sessions/2026-07-25.md) |
| 2026-07-24 | [EQ Ops quote-detail panel simplified + Coupa PO import rebuilt against the real export](sessions/2026-07-24.md) |
| 2026-07-23 | [Closed the crm-write/canonical-api entitlement design pass: no gate needed](sessions/2026-07-23.md) |
| 2026-07-22 | [SKS Safety: Incidents/Near Miss tab + Prestart copy-from-last, EQ Field regression found & fixed](sessions/2026-07-22.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-26 09:52 UTC._

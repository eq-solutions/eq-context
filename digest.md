---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-26
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-26 06:42 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-26 06:23 UTC → 2026-07-26 06:42 UTC)

- Merged: eq-shell [#1020](https://github.com/eq-solutions/eq-shell/pull/1020) chore(styles): remove dead duplicate TenantHome AI-brief CSS
- Merged: eq-shell [#1003](https://github.com/eq-solutions/eq-shell/pull/1003) chore(deps): bump @eq-solutions/ui to v1.11.1 (cascading fil
- Merged: eq-shell [#1000](https://github.com/eq-solutions/eq-shell/pull/1000) chore(migrations): renumber 0202/0203 Coupa PO collisions ->
- Merged: eq-shell [#998](https://github.com/eq-solutions/eq-shell/pull/998) feat(customers,quotes): customer-level default End Client
- Merged: eq-shell [#995](https://github.com/eq-solutions/eq-shell/pull/995) docs(ledger): record reconcile_worker_sync migration as appl
- Merged: eq-shell [#993](https://github.com/eq-solutions/eq-shell/pull/993) fix(workers-canonical-sync): stop nightly reconciler from un
- Merged: eq-shell [#992](https://github.com/eq-solutions/eq-shell/pull/992) fix(auth): self-heal shell login for staff approved before C
- Merged: eq-shell [#991](https://github.com/eq-solutions/eq-shell/pull/991) fix(ops): job-creation export never actually populated the n

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-12 (P0 — confirmed exposure, same class as SEC-9/SEC-10) — Several real secrets on **eq-shell's own** Netlify project stored with `is_secre · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 4d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 10 | 2026-07-23 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 6 | 2026-07-25 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 6 | 2026-07-23 |
| eq-field | [SyntaxError: Identifier 'INCIDENT_TYPES' has already been declared](https://eq-solutions.sentry.io/issues/136548558/) | 1 | 2026-07-26 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-26 | eq-shell | [#1020](https://github.com/eq-solutions/eq-shell/pull/1020) chore(styles): remove dead duplicate TenantHome AI-brief CSS bloc |
| 2026-07-26 | eq-shell | [#1016](https://github.com/eq-solutions/eq-shell/pull/1016) fix(perms): close check-perm-sync.mjs under-grant blind spot + wi |
| 2026-07-26 | eq-shell | [#1018](https://github.com/eq-solutions/eq-shell/pull/1018) feat(dashboard): scannable AI brief, self-evident action ranking |
| 2026-07-26 | eq-shell | [#1017](https://github.com/eq-solutions/eq-shell/pull/1017) feat(settings): required-tickets picker alongside Who can join |
| 2026-07-26 | eq-shell | [#1015](https://github.com/eq-solutions/eq-shell/pull/1015) feat(settings): move the join-requirements switch out of Training |
| 2026-07-26 | eq-shell | [#1011](https://github.com/eq-solutions/eq-shell/pull/1011) fix(access-control): add subcontractor to tenant_role_overrides C |
| 2026-07-26 | eq-shell | [#1014](https://github.com/eq-solutions/eq-shell/pull/1014) feat(cards): surface the join-requirement gap at approval time |
| 2026-07-26 | eq-shell | [#1013](https://github.com/eq-solutions/eq-shell/pull/1013) feat(retention): ADR-005 leaver data retention — deactivated_at + |
| 2026-07-26 | eq-shell | [#1012](https://github.com/eq-solutions/eq-shell/pull/1012) feat(cards): title-case onboarding names + admin switch for join  |
| 2026-07-26 | eq-shell | [#1010](https://github.com/eq-solutions/eq-shell/pull/1010) docs(ledger): record retire_credentials_canonical_sync as applied |
| 2026-07-26 | eq-shell | [#1009](https://github.com/eq-solutions/eq-shell/pull/1009) fix(staff): lock down direct writes + guard against silent reacti |
| 2026-07-26 | eq-shell | [#1008](https://github.com/eq-solutions/eq-shell/pull/1008) fix(cards): invite-approval path used an invalid role enum value |
| 2026-07-26 | eq-shell | [#1007](https://github.com/eq-solutions/eq-shell/pull/1007) fix(quotes): Job Creation export falls back to customer's default |
| 2026-07-26 | eq-shell | [#1006](https://github.com/eq-solutions/eq-shell/pull/1006) chore: remove one-time Sentry alert-apply workflow |
| 2026-07-26 | eq-shell | [#1005](https://github.com/eq-solutions/eq-shell/pull/1005) fix(sentry): correct filter type on the folded-in iframe-mint ale |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Royce to check the Netlify dashboard for `ENFORCE_IFRAME_ORIGIN`** on eq-shell — confirms whether the iframe-origin check is actually enforcing in production (not just in code). Not readable via the connected tools. _(added 2026-07-26)_
- **Royce to remediate SEC-12** (plaintext Netlify secrets on eq-shell) via the Netlify dashboard — same-value re-store per key (not a rotation), just needs "contains sensitive values" ticked. `GOOGLE_DOC_AI_CREDENTIALS` (an RSA private key) is the highest-priority one. Full detail in `ops/security-register.md`. _(added 2026-07-26)_
- **EQ Cards' own worker-initiated 30-day account-deletion promise** (separate from the leaver-retention work above — this is a worker deleting their *own* Cards account) is still built but switched off (dry-run only). Not actioned this session, just a known standing gap. _(added 2026-07-26)_
- **Access-Model Phase 2 ("One admin") and Phase 3 (permission-key guardrails)** — explained to Royce in the Q&A, deliberately not built yet. Locked decision to keep auth changes out of the SKS launch window; revisit post-cutover. _(added 2026-07-26)_
- **Real end-to-end confirmation still open**: re-archived the 4 originally-affected people (Aaron Clohessy, Emma Curth, Jack Fitzpatrick, Ross Davidson) as a live test. Need to check after tomorrow's nightly run (and ideally after their Cards profile syncs in real time) that they're still archived — that's the actual proof the fix holds, not just a clean deploy. _(added 2026-07-26)_
- **Bob Smith** (one of the 5 originally reported) still doesn't match any current staff record in the SKS tenant by name — never resolved, possibly a name-spelling mismatch or a different tenant. Worth a quick manual look. _(added 2026-07-26)_
- **The old, now-unused sync function is still sitting in Supabase** (edge function `credentials-canonical-sync`) — harmless since nothing calls it anymore, but there's no way to delete an edge function via a migration; would need a manual removal via the Supabase dashboard if Royce wants it gone entirely. _(added 2026-07-26)_
- **Not yet confirmed by Royce**: the EQ Ops multiselect filters (Est./Status/Job No.) and the labour-hire dashboard now showing the corrected INSELEC rates. The EQ Service Assets table cascade WAS confirmed live by Royce this session. _(added 2026-07-24)_
- **What's the actual remaining pain point for direct employees, now that the Cards→Field pipe is confirmed live end-to-end?** Asked Royce directly — is it that head office doesn't trust/re-checks Field data before their manual Upvise upload, or a different gap not yet found. Not answered yet this session. _(added 2026-07-24)_
- **Follow-up: `guard.js` itself is unversioned and untested.** It lives at `~/.claude/hooks/guard.js`, outside any git repo, with zero test coverage (beyond the ad hoc verification above) — unlike `hooks/*.py` in this repo, which are governed/versioned/CI-checked (`hooks/README.md`). Its own header cites a spec file (`system/operating-model-roadmap.md`) that doesn't exist. Worth eventually mirroring guard.js into this repo (versioned source of truth, deployed copy on the Beelink) so it gets the same test-before-trust discipline as the Python hooks. Not fixed this session — separate, larger scope. _(added 2026-07-24)_
_…and 449 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2750 | 463 | 44 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-26 06:42 UTC._

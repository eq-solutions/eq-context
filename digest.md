---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-26
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-26 03:52 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-26 03:42 UTC → 2026-07-26 03:52 UTC)

- Merged: eq-shell [#1014](https://github.com/eq-solutions/eq-shell/pull/1014) feat(cards): surface the join-requirement gap at approval ti
- Merged: eq-shell [#998](https://github.com/eq-solutions/eq-shell/pull/998) feat(customers,quotes): customer-level default End Client
- Merged: eq-shell [#995](https://github.com/eq-solutions/eq-shell/pull/995) docs(ledger): record reconcile_worker_sync migration as appl
- Merged: eq-shell [#993](https://github.com/eq-solutions/eq-shell/pull/993) fix(workers-canonical-sync): stop nightly reconciler from un
- Merged: eq-shell [#991](https://github.com/eq-solutions/eq-shell/pull/991) fix(ops): job-creation export never actually populated the n
- Merged: eq-shell [#989](https://github.com/eq-solutions/eq-shell/pull/989) fix(quotes): simplify quote-detail panel; rebuild Coupa PO i
- Merged: eq-shell [#987](https://github.com/eq-solutions/eq-shell/pull/987) perf(customers): run the 3 customer-detail lookups in parall
- Merged: eq-shell [#971](https://github.com/eq-solutions/eq-shell/pull/971) fix(security): tenant-scope the react-query caches so a work

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
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
| 2026-07-26 | eq-shell | [#1014](https://github.com/eq-solutions/eq-shell/pull/1014) feat(cards): surface the join-requirement gap at approval time |
| 2026-07-26 | eq-shell | [#1013](https://github.com/eq-solutions/eq-shell/pull/1013) feat(retention): ADR-005 leaver data retention — deactivated_at + |
| 2026-07-26 | eq-shell | [#1012](https://github.com/eq-solutions/eq-shell/pull/1012) feat(cards): title-case onboarding names + admin switch for join  |
| 2026-07-26 | eq-shell | [#1010](https://github.com/eq-solutions/eq-shell/pull/1010) docs(ledger): record retire_credentials_canonical_sync as applied |
| 2026-07-26 | eq-shell | [#1009](https://github.com/eq-solutions/eq-shell/pull/1009) fix(staff): lock down direct writes + guard against silent reacti |
| 2026-07-26 | eq-shell | [#1008](https://github.com/eq-solutions/eq-shell/pull/1008) fix(cards): invite-approval path used an invalid role enum value |
| 2026-07-26 | eq-shell | [#1007](https://github.com/eq-solutions/eq-shell/pull/1007) fix(quotes): Job Creation export falls back to customer's default |
| 2026-07-26 | eq-shell | [#1006](https://github.com/eq-solutions/eq-shell/pull/1006) chore: remove one-time Sentry alert-apply workflow |
| 2026-07-26 | eq-shell | [#1005](https://github.com/eq-solutions/eq-shell/pull/1005) fix(sentry): correct filter type on the folded-in iframe-mint ale |
| 2026-07-26 | eq-cards | [#177](https://github.com/eq-solutions/eq-cards/pull/177) feat(onboarding): show the join-requirement gap before Apply (Car |
| 2026-07-26 | eq-cards | [#176](https://github.com/eq-solutions/eq-cards/pull/176) feat(onboarding): per-org minimum join-requirement fields (soft-f |
| 2026-07-24 | eq-shell | [#1004](https://github.com/eq-solutions/eq-shell/pull/1004) fix(quotes): End Client next to Quote Number, Commercials sticky  |
| 2026-07-24 | eq-shell | [#1003](https://github.com/eq-solutions/eq-shell/pull/1003) chore(deps): bump @eq-solutions/ui to v1.11.1 (cascading filter f |
| 2026-07-24 | eq-shell | [#1002](https://github.com/eq-solutions/eq-shell/pull/1002) fix(migrations): 0206 was aborting every tenant-migrate dispatch |
| 2026-07-24 | eq-shell | [#1000](https://github.com/eq-solutions/eq-shell/pull/1000) chore(migrations): renumber 0202/0203 Coupa PO collisions -> 0205 |
_Showing 15 of 111 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Real end-to-end confirmation still open**: re-archived the 4 originally-affected people (Aaron Clohessy, Emma Curth, Jack Fitzpatrick, Ross Davidson) as a live test. Need to check after tomorrow's nightly run (and ideally after their Cards profile syncs in real time) that they're still archived — that's the actual proof the fix holds, not just a clean deploy. _(added 2026-07-26)_
- **Bob Smith** (one of the 5 originally reported) still doesn't match any current staff record in the SKS tenant by name — never resolved, possibly a name-spelling mismatch or a different tenant. Worth a quick manual look. _(added 2026-07-26)_
- **The old, now-unused sync function is still sitting in Supabase** (edge function `credentials-canonical-sync`) — harmless since nothing calls it anymore, but there's no way to delete an edge function via a migration; would need a manual removal via the Supabase dashboard if Royce wants it gone entirely. _(added 2026-07-26)_
- **Not yet confirmed by Royce**: the EQ Ops multiselect filters (Est./Status/Job No.) and the labour-hire dashboard now showing the corrected INSELEC rates. The EQ Service Assets table cascade WAS confirmed live by Royce this session. _(added 2026-07-24)_
- **What's the actual remaining pain point for direct employees, now that the Cards→Field pipe is confirmed live end-to-end?** Asked Royce directly — is it that head office doesn't trust/re-checks Field data before their manual Upvise upload, or a different gap not yet found. Not answered yet this session. _(added 2026-07-24)_
- **Follow-up: `guard.js` itself is unversioned and untested.** It lives at `~/.claude/hooks/guard.js`, outside any git repo, with zero test coverage (beyond the ad hoc verification above) — unlike `hooks/*.py` in this repo, which are governed/versioned/CI-checked (`hooks/README.md`). Its own header cites a spec file (`system/operating-model-roadmap.md`) that doesn't exist. Worth eventually mirroring guard.js into this repo (versioned source of truth, deployed copy on the Beelink) so it gets the same test-before-trust discipline as the Python hooks. Not fixed this session — separate, larger scope. _(added 2026-07-24)_
- **An automatic check is scheduled for the morning of 2026-07-25 to confirm the fix actually held overnight** — will look at the 5 originally-reported people directly, check for any suspicious mass-reactivation pattern across staff generally, and report back. Not yet confirmed by Royce himself. _(added 2026-07-24)_
- **`eq_reconcile_worker_sync()` (the nightly dispatcher itself, jvkn `pg_cron` job id 2) still isn't tracked in any repo migration** — a governance gap independent of the bug above, not touched by this fix. Not urgent now that the harmful write is gone, but worth bringing under the normal migration pipeline at some point. _(added 2026-07-24)_
- **Not yet confirmed working end-to-end by Royce.** He tested once and got no receipts in the zip — root-caused to him re-downloading a *pre-existing* Past Exports history row generated before this session's fix (immutable — old rows never gain the bundling retroactively), not a code bug. Live-pulled the deployed function source to confirm the real fix is active. Told him to click "Generate claim form" again for a fresh `.zip` and report back — session ended before that confirmation came in. _(added 2026-07-24)_
- **Not yet click-tested against the newest version** — the tick/cross feedback and the job title column are live, but nobody has run a fresh file through *this* version of the screen yet. _(added 2026-07-24)_
_…and 442 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2732 | 459 | 37 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-26 03:52 UTC._

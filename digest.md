---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-22
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-22 09:03 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-21 13:28 UTC → 2026-07-22 09:03 UTC)

- Merged: eq-shell [#944](https://github.com/eq-solutions/eq-shell/pull/944) Account deletion left the Shell identity row behind (6 orpha
- Merged: eq-shell [#936](https://github.com/eq-solutions/eq-shell/pull/936) Security: app_data.staff.user_id was directly client-writabl
- Merged: eq-shell [#930](https://github.com/eq-solutions/eq-shell/pull/930) Security: EQ Ops setup RPCs adopt the pricing write guard on
- Merged: eq-shell [#925](https://github.com/eq-solutions/eq-shell/pull/925) feat(retention): daily job to finalise deleted Cards account
- Merged: eq-shell [#924](https://github.com/eq-solutions/eq-shell/pull/924) Fix: flush Sentry before functions return — server events we
- Merged: eq-shell [#923](https://github.com/eq-solutions/eq-shell/pull/923) Quote doc: fix Clarifications alignment (justified -> left)
- Merged: eq-shell [#922](https://github.com/eq-solutions/eq-shell/pull/922) Staff: Company column for Labour Hire + Subcontractor, fix r
- Merged: eq-shell [#919](https://github.com/eq-solutions/eq-shell/pull/919) Option 3: surface + gate identity collisions in the staff-ap
- ⚠ Needs you: 4 → 5 (new items)

## ⚠ Needs you (5)

- 🔴 **Substrate drift** — DRIFT: deploy EQ Shell (core) (https://core.eq.solutions): claimed LIVE but reality looks DEAD
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
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 5 | 2026-07-16 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/133972818/) | 3 | 2026-07-20 |
| eq-shell | [Error: eq-ops rpc eq_upsert_pricing_config failed: pricing config requires manag](https://eq-solutions.sentry.io/issues/135532286/) | 2 | 2026-07-21 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 1 | 2026-07-21 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 1 | 2026-07-19 |
| eq-shell | [EQ Field handoff timeout — no postMessage in 30s](https://eq-solutions.sentry.io/issues/129554465/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-22 | eq-shell | [#944](https://github.com/eq-solutions/eq-shell/pull/944) Account deletion left the Shell identity row behind (6 orphans on |
| 2026-07-22 | eq-field | [#530](https://github.com/eq-solutions/eq-field/pull/530) v3.5.353 — crew scoping: a supervisor sees the crews they run |
| 2026-07-22 | eq-field | [#531](https://github.com/eq-solutions/eq-field/pull/531) v3.5.352 — enforce the tender-parser test suite in CI |
| 2026-07-22 | eq-field | [#528](https://github.com/eq-solutions/eq-field/pull/528) v3.5.351 — leave_requests: the last unbounded read, and a non-uni |
| 2026-07-22 | eq-field | [#529](https://github.com/eq-solutions/eq-field/pull/529) v3.5.350 — restore prestart "copy from last" dropped in #516 |
| 2026-07-22 | eq-field | [#527](https://github.com/eq-solutions/eq-field/pull/527) v3.5.347 — extract + test sks-pipeline-resource.js's allocation m |
| 2026-07-22 | eq-field | [#526](https://github.com/eq-solutions/eq-field/pull/526) v3.5.348 — canonical wide reads (timesheets + roster): truncated, |
| 2026-07-22 | eq-field | [#520](https://github.com/eq-solutions/eq-field/pull/520) Gate timesheet + leave status transitions (self-approval, reopen, |
| 2026-07-22 | eq-field | [#525](https://github.com/eq-solutions/eq-field/pull/525) v3.5.347 — people-family reads silently truncated at PostgREST's  |
| 2026-07-22 | eq-cards | [#172](https://github.com/eq-solutions/eq-cards/pull/172) 0101: enforce canonical licence row shape on jvkn (NOT APPLIED) |
| 2026-07-21 | eq-shell | [#936](https://github.com/eq-solutions/eq-shell/pull/936) Security: app_data.staff.user_id was directly client-writable on  |
| 2026-07-21 | eq-shell | [#930](https://github.com/eq-solutions/eq-shell/pull/930) Security: EQ Ops setup RPCs adopt the pricing write guard on the  |
| 2026-07-21 | eq-shell | [#935](https://github.com/eq-solutions/eq-shell/pull/935) P0: any authenticated user could forge an invite and become tenan |
| 2026-07-21 | eq-shell | [#943](https://github.com/eq-solutions/eq-shell/pull/943) chore: remove dead mint-cards-iframe-token.ts |
| 2026-07-21 | eq-shell | [#942](https://github.com/eq-solutions/eq-shell/pull/942) diag(ci): surface real HTTP status/body from notify-substrate dis |
_Showing 15 of 107 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Field still writes to the SKS database through its own door, outside the governed pipeline.** Two of today's changes went in by hand because Field has no approval pipeline of its own, following existing precedent. That's the same pattern named elsewhere as the cause of an earlier drift incident. Now that the governed pipeline has been seen working cleanly several times today, Field's database changes should move into it — otherwise there are permanently two ways in, one of them unaudited. _(added 2026-07-21)_
- **The timesheet and leave approval rules have never been exercised by a real person.** The logic went live without ever having been run — there's no safe place to rehearse it. Worth putting one real timesheet and one real leave request through the full path (submit → approve → try to approve your own → try to reopen) next time you're in Field, to confirm the blocks and the wording behave as intended. _(added 2026-07-21)_
- **Six leftover records still need clearing — needs your hand.** A prepared script is sitting in the repo (`scripts/cleanup-orphaned-shell-users.sql`). It snapshots first, re-checks six safety conditions before touching anything, and won't save changes unless you confirm the numbers look right. It can't be automated — that database has no automatic update path. Nobody is affected in the meantime; none of these accounts can be signed into. _(added 2026-07-22)_
- **The old admin button should be guarded or retired.** It still exists and would still do the wrong thing if pointed at records like these. Its original job was finished off by fixes that went live a week ago, so it may simply be dead. Separate task, chip raised. _(added 2026-07-22)_
- **One thing not checked: a real click-through with a live login.** The sandbox this was built in has no working sign-in to the real system, so the code was verified by reading + a syntax/lint pass + a no-login load test, not by actually opening a prestart and clicking the button. Worth a real click-through next time you're in the app at a site with prior prestart history. _(added 2026-07-22)_
- **Four lesser flaws deliberately left alone.** They're rated moderate rather than serious, and fixing them isn't a routine update — it would mean *downgrading* two major pieces of the app (the web framework itself, and the spreadsheet export library) by several major versions. That's a rewrite with real breakage risk, traded against flaws the safety check doesn't even consider serious enough to block on. Not recommended, and not urgent — noting it only so nobody re-discovers it and assumes it was missed. _(added 2026-07-21)_
- **The `production` GitHub Environment on eq-shell has no protection rules** (confirmed directly via the GitHub API — the reviewer list is empty). The documented safety net for every tenant-database migration doesn't actually exist right now. This isn't specific to this session's changes — it means ANY future migration dispatch (by anyone, on any tenant) applies immediately with no approval step, contradicting the "explicit human go before live DDL" design the workflow file describes. Fix is a plain GitHub settings change (repo Settings → Environments → production → add Royce as a required reviewer) — not something fixable by me via API or CLI. _(added 2026-07-21)_
- **A separate, already-diagnosed cause of people getting logged out unexpectedly** (a background check treats "the server was just slow to answer" the same as "you're not logged in any more," and logs you out either way) is understood but not yet built, since it changes how login/session behaviour works and needs an explicit go-ahead first. _(added 2026-07-21)_
- **One test step is blocked, needs your call:** fast-forwarding that one test account's "deleted" timestamp by 31 days (so the cleanup job can be checked without waiting a real month) got blocked by the safety guardrail, even for a single-column edit on a known test row. Either approve a retry, or just let the real 30 days pass and it'll be checked then. _(added 2026-07-21)_
- **PAT swap still outstanding — narrowed the problem.** Confirmed live that eq-cards' repo-level `EQ_CONTEXT_PAT` (set 08:38) is a genuinely working classic PAT — dispatch returns HTTP 204 on 3 consecutive runs. The 3 sibling repos' `EQ_CONTEXT_PAT` secrets were set earlier the same session (08:08–08:30) and are **not** the same value — still failing, now with a visible real error instead of a silent exit-22 (thanks to the diagnostics port above). Can't read/copy a GitHub secret's value via API — **needs Royce**: paste the same working classic PAT into eq-shell/eq-field/eq-service's `EQ_CONTEXT_PAT` (Settings → Secrets → Actions, per repo, same value reused across all three). _(added 2026-07-21)_
_…and 403 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- EQ Field has no Incidents-tab equivalent at all (only a generic incidents array buried in its Site Diary) — would be a from-scratch build there, not a port, if Royce wants parity. _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
- Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_
- **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_
- **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_
- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement (see `eq/changelog/field.md` "SKS = Core-only auth", v3.5.200).
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
_…and 62 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 3123 | 416 | 490 |
| [SKS](sks/pending.md) | 484 | 73 | 72 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-22 | [SKS Safety: Incidents/Near Miss tab + Prestart copy-from-last, EQ Field regression found & fixed](sessions/2026-07-22.md) |
| 2026-07-21 | [eq-shell had its own copy of the licence-privacy gap; found, fixed, deployed, and smoke-tested](sessions/2026-07-21.md) |
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
| 2026-07-17 | [AI brief's quote signals were silently zero for SKS; realigned to the live enum, guarded, shipped live](sessions/2026-07-17.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-22 09:03 UTC._

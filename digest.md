---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-20
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-20 10:10 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-20 05:29 UTC → 2026-07-20 10:10 UTC)

- Merged: eq-solves-intake [#74](https://github.com/eq-solutions/eq-solves-intake/pull/74) fix: backport two eq-shell-only fixes into source
- Merged: eq-solves-intake [#73](https://github.com/eq-solutions/eq-solves-intake/pull/73) feat(intake): usage-based survivor pick for the Sites Dupes 
- Merged: eq-solves-intake [#72](https://github.com/eq-solutions/eq-solves-intake/pull/72) feat(intake): wire the merge-panel UI into IntakeHealthHome
- Merged: eq-solves-intake [#71](https://github.com/eq-solutions/eq-solves-intake/pull/71) feat(intake): flagSitePairForMerge client wrapper
- Merged: eq-solves-intake [#70](https://github.com/eq-solutions/eq-solves-intake/pull/70) feat(intake): site merge preview + execute client wrappers
- Merged: eq-solves-intake [#69](https://github.com/eq-solutions/eq-solves-intake/pull/69) feat(intake): AI adjudicator — Claude suggests a verdict + r
- Merged: eq-solves-intake [#68](https://github.com/eq-solutions/eq-solves-intake/pull/68) feat(intake): adjudicable console — capture the human verdic
- Merged: eq-solves-intake [#67](https://github.com/eq-solutions/eq-solves-intake/pull/67) feat(intake): adjudication console — surface what the write-

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-cards` [minified:iu: ServerFailure(23502): null value in column "wor](https://eq-solutions.sentry.io/issues/135305974/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 3d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 5 | 2026-07-16 |
| eq-cards | [minified:iu: ServerFailure(23502): null value in column "worker_phone" of relati](https://eq-solutions.sentry.io/issues/135305974/) | 4 | 2026-07-20 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/133972818/) | 3 | 2026-07-20 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 1 | 2026-07-19 |
| eq-shell | [EQ Field handoff timeout — no postMessage in 30s](https://eq-solutions.sentry.io/issues/129554465/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-16 | eq-solves-intake | [#73](https://github.com/eq-solutions/eq-solves-intake/pull/73) feat(intake): usage-based survivor pick for the Sites Dupes tab |
| 2026-07-16 | eq-solves-intake | [#74](https://github.com/eq-solutions/eq-solves-intake/pull/74) fix: backport two eq-shell-only fixes into source |
| 2026-07-16 | eq-solves-intake | [#72](https://github.com/eq-solutions/eq-solves-intake/pull/72) feat(intake): wire the merge-panel UI into IntakeHealthHome |
| 2026-07-16 | eq-solves-intake | [#71](https://github.com/eq-solutions/eq-solves-intake/pull/71) feat(intake): flagSitePairForMerge client wrapper |
| 2026-07-15 | eq-solves-intake | [#70](https://github.com/eq-solutions/eq-solves-intake/pull/70) feat(intake): site merge preview + execute client wrappers |
| 2026-07-14 | eq-solves-intake | [#69](https://github.com/eq-solutions/eq-solves-intake/pull/69) feat(intake): AI adjudicator — Claude suggests a verdict + reason |
| 2026-07-14 | eq-solves-intake | [#68](https://github.com/eq-solutions/eq-solves-intake/pull/68) feat(intake): adjudicable console — capture the human verdict on  |
| 2026-07-13 | eq-solves-intake | [#67](https://github.com/eq-solutions/eq-solves-intake/pull/67) feat(intake): adjudication console — surface what the write-time  |
| 2026-07-13 | eq-solves-intake | [#66](https://github.com/eq-solutions/eq-solves-intake/pull/66) fix(intake): duplicate detector was blind to inactive rows — the  |
_9 merges · full record in [sessions/](sessions/)_

## Pending (EQ)

- **A cosmetic app-crash message (unrelated) is still open, low priority** — a rendering hiccup that's been intermittently appearing since 2026-07-13, not something from today's work. Not investigated further. _(added 2026-07-20)_
- **Last step: the access key itself needs to be re-entered correctly.** The new connection is wired up and reaching GitHub, but currently rejects the specific key that was entered — likely a copy/paste slip (extra space, truncated, or an old/expired one). Once re-pasted correctly, this should fully close out the whole GitHub-access saga. _(added 2026-07-20)_
- **Note for the record: one repo (EQ Shell) got switched from public to private today as a side effect of testing this** — confirmed intentional at the time, but worth double-checking it's still meant to be that way. Also worth knowing: several other company repos (EQ Context, EQ UI, EQ Quotes, EQ Contracts, the old SKS labour app, and a couple of smaller internal libraries) have been sitting fully public — readable by anyone on the internet with no login — for as long as this was checked. Given the private-repo requirement from SKS, worth a deliberate look at whether those should be private too. _(added 2026-07-20)_
- **Still open, not urgent:** the exact reason EQ Field was slow to load for that one person on 2026-07-19 is unconfirmed — likely just a poor connection, but couldn't fully rule out anything worse. Nothing else has reported it since. _(added 2026-07-19)_
- **Deferred: who should get the weekly summary email?** Built and ready, just needs a recipient list from Royce before it's switched on. _(added 2026-07-17)_
- **Declined for now (Royce's call): a personal calendar feed per crew member, and a weather warning near Microsoft dock dates.** Offered as options alongside the above; not built. _(added 2026-07-17)_
- **Deferred: remove the legacy public-read grant across all 7 related views**, as one deliberate, scoped cleanup rather than piecemeal — only if Royce wants that extra hardening on top of the row-level-security fix already live. _(added 2026-07-19)_
- **Deferred: bigger first-load speedup** — breaking one large file into smaller pieces that only load when needed. Real win, but a bigger change that needs a hands-on check, not just automated tests. _(added 2026-07-19)_
- **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
_…and 363 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
- **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_
- **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_
- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
_…and 56 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
| 2026-07-17 | [AI brief's quote signals were silently zero for SKS; realigned to the live enum, guarded, shipped live](sessions/2026-07-17.md) |
| 2026-07-16 | [verified migration 0185 live, explained the merge feature's location, seeded a real demo pair](sessions/2026-07-16.md) |
| 2026-07-15 | [EQ Service: fixed empty NSX/ACB testing lists in the Shell iframe + Field Run-Sheet dropping recorded breaker data](sessions/2026-07-15.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-20 10:10 UTC._

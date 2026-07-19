---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-19
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-19 05:10 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-19 05:04 UTC → 2026-07-19 05:10 UTC)

- Merged: eq-shell [#900](https://github.com/eq-solutions/eq-shell/pull/900) perf(offline): extend the unsaved-changes guard to site and 
- Merged: eq-shell [#886](https://github.com/eq-solutions/eq-shell/pull/886) feat(dashboard): permission-gated signals board (compliance 
- Merged: eq-shell [#884](https://github.com/eq-solutions/eq-shell/pull/884) perf(build): split heavy vendors into cacheable chunks
- Merged: eq-shell [#883](https://github.com/eq-solutions/eq-shell/pull/883) perf(quotes): parallelize the quote-open RPC waterfall
- Merged: eq-shell [#880](https://github.com/eq-solutions/eq-shell/pull/880) feat(intake): usage-based survivor pick for the Sites Dupes 
- Merged: eq-shell [#878](https://github.com/eq-solutions/eq-shell/pull/878) fix(drift): degrade gracefully on an unreachable tenant
- Merged: eq-shell [#876](https://github.com/eq-solutions/eq-shell/pull/876) feat(intake): merge from the Sites Dupes tab (migration 0186
- Merged: eq-shell [#866](https://github.com/eq-solutions/eq-shell/pull/866) feat(brand): dark-background document logo (canonical + hand

## ⚠ Needs you (1)

- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 4d |
| eq-solves-service | ✓ success | 2d ago | 2 | 5d |
| eq-field | ✓ success | 0d ago | 2 | 6d |
| eq-cards | ✓ success | 2d ago | 0 | — |
| eq-solves-intake | ✓ success | 2d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 5 | 2026-07-16 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-19 | eq-shell | [#900](https://github.com/eq-solutions/eq-shell/pull/900) perf(offline): extend the unsaved-changes guard to site and invit |
| 2026-07-19 | eq-shell | [#901](https://github.com/eq-solutions/eq-shell/pull/901) NSW Comms: cut Dashboard load-time from ~5.4s to ~2 round trips |
| 2026-07-19 | eq-shell | [#897](https://github.com/eq-solutions/eq-shell/pull/897) NSW Comms: Start-by estimate from PO+53-day planning rule (Patric |
| 2026-07-19 | eq-field | [#500](https://github.com/eq-solutions/eq-field/pull/500) test: guard the routing bypass that hid the 6-view grant gap |
| 2026-07-18 | eq-shell | [#899](https://github.com/eq-solutions/eq-shell/pull/899) fix(security): reassert security_invoker on 3 field_* views (0187 |
| 2026-07-18 | eq-shell | [#863](https://github.com/eq-solutions/eq-shell/pull/863) fix(auth): bound login body reads under one deadline (the #858 la |
| 2026-07-18 | eq-shell | [#898](https://github.com/eq-solutions/eq-shell/pull/898) perf(home): dedupe duplicate dashboard + pending-connections fetc |
| 2026-07-18 | eq-shell | [#890](https://github.com/eq-solutions/eq-shell/pull/890) feat(access): gate contact PII in direct-read RPCs (cluster 1, Ph |
| 2026-07-18 | eq-field | [#499](https://github.com/eq-solutions/eq-field/pull/499) fix(access): field_people_iud — extend labour-hire guard to hire_ |
| 2026-07-18 | eq-field | [#498](https://github.com/eq-solutions/eq-field/pull/498) fix(field): restore authenticated grant on 6 app_data views (ehow |
| 2026-07-18 | eq-field | [#497](https://github.com/eq-solutions/eq-field/pull/497) feat(access): cluster 3 — server-side enforcement of field.manage |
| 2026-07-17 | eq-shell | [#889](https://github.com/eq-solutions/eq-shell/pull/889) NSW Comms: parallel jobs-GET + resource dashboard landing view +  |
| 2026-07-17 | eq-solves-service | [#551](https://github.com/eq-solutions/eq-service/pull/551) feat(access): cluster 3 — enforce service.reopen + service.record |
| 2026-07-17 | eq-field | [#496](https://github.com/eq-solutions/eq-field/pull/496) feat(access): cluster 3 — enforce field.manage_roster/licences/la |
| 2026-07-16 | eq-shell | [#888](https://github.com/eq-solutions/eq-shell/pull/888) perf(auth): parallelize verify-shell-session's independent DB rea |
_Showing 15 of 104 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Deferred: remove the legacy public-read grant across all 7 related views**, as one deliberate, scoped cleanup rather than piecemeal — only if Royce wants that extra hardening on top of the row-level-security fix already live. _(added 2026-07-19)_
- **Deferred: bigger first-load speedup** — breaking one large file into smaller pieces that only load when needed. Real win, but a bigger change that needs a hands-on check, not just automated tests. _(added 2026-07-19)_
- **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
- **Now in scope, not yet built: extend the "you'll lose this" warning to more forms** (site details, invites, admin settings — currently only quotes), a plain "you're offline" banner when the connection drops, and re-checking sign-in status automatically when someone comes back to a tab left open a while. _(added 2026-07-19)_
- **Royce to eyeball the live dashboard signed in** — the endpoint/bundle/error-monitoring checks are all clean, but only a signed-in pass confirms the three bands render correctly and the rostered-but-lapsed join surfaces real people. _(added 2026-07-17)_
- **Gate keys are interim** (`field.view`/`service.view`) — swap to the cluster-1 granular keys (`field.view_licences` etc., PR #885, concurrent session) once that ships. _(added 2026-07-17)_
- **Phase 2 deferred: crew-demand overlay.** Needs a `crew_required` column added to `app_data.jobs` (One Pipe migration, both planes) so the "can we staff what we've won" verdict has a real demand side — supply side (deployable crew) is live now, demand isn't wired yet. _(added 2026-07-16)_
- **Phase 3 deferred: the one commercial signal permitted by the scope decision** — "N quotes won but no job number yet," gated behind `quotes.view`, no dollar amount, off the default board. Not built. _(added 2026-07-16)_
- **Eyeball the next SKS morning brief once signed in** to confirm the signals render as expected end-to-end. The query logic is verified against live data and the deploy is smoke-verified, but the authed brief output itself needs a signed-in SKS session (10-minute per-user cache, or wait for the daily scheduled email). _(added 2026-07-17)_
_…and 362 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_
- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
_…and 56 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
| 2026-07-17 | [AI brief's quote signals were silently zero for SKS; realigned to the live enum, guarded, shipped live](sessions/2026-07-17.md) |
| 2026-07-16 | [verified migration 0185 live, explained the merge feature's location, seeded a real demo pair](sessions/2026-07-16.md) |
| 2026-07-15 | [EQ Service: fixed empty NSX/ACB testing lists in the Shell iframe + Field Run-Sheet dropping recorded breaker data](sessions/2026-07-15.md) |
| 2026-07-14 | [Merged + deployed the intake vendor-sync and the xlsx security fix](sessions/2026-07-14.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-19 05:10 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-11
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-11 05:04 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-11 05:01 UTC → 2026-07-11 05:04 UTC)

- Merged: eq-shell [#748](https://github.com/eq-solutions/eq-shell/pull/748) feat(comms): crew = the Field "Comms" team (retire the paral
- Merged: eq-shell [#731](https://github.com/eq-solutions/eq-shell/pull/731) feat(comms): Move 1.5 + 2b — filters/simplification, and boo
- Merged: eq-shell [#728](https://github.com/eq-solutions/eq-shell/pull/728) feat(staff): surface tenant required-credential gaps in the 
- Merged: eq-shell [#727](https://github.com/eq-solutions/eq-shell/pull/727) feat(comms): Move 1 — job card catches up to the planner
- Merged: eq-shell [#725](https://github.com/eq-solutions/eq-shell/pull/725) fix(csp): allow Clarity's rotating collector subdomains (*.c
- Merged: eq-shell [#724](https://github.com/eq-solutions/eq-shell/pull/724) fix(sync): worker→staff sync matches identity + merges inste
- Merged: eq-shell [#723](https://github.com/eq-solutions/eq-shell/pull/723) polish(field-iframe): make restore-failed reachable on repea
- Merged: eq-shell [#720](https://github.com/eq-solutions/eq-shell/pull/720) fix(briefing): swallow PGRST205 for dropped app_data.tenders

## ⚠ Needs you (2)

- 🟠 **Sentry new error** — `eq-field` [Error: LEAVE_DIAG {"ver":"3.5.291","slug":"sks","winsb":"eho](https://eq-solutions.sentry.io/issues/133570956/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 3 | 6d |
| eq-solves-service | ✓ success | 0d ago | 5 | 4d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: native pipeline query failed: Could not find the table 'app_data.tenders'](https://eq-solutions.sentry.io/issues/132948690/) | 31 | 2026-07-10 |
| eq-solves-service | [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/) | 19 | 2026-07-08 |
| eq-field | [Error: LEAVE_DIAG {"ver":"3.5.291","slug":"sks","winsb":"ehowgjardagevnrluult","](https://eq-solutions.sentry.io/issues/133570956/) | 5 | 2026-07-10 |
| eq-shell | [EQ Field handoff auto-recovery exhausted (rejected)](https://eq-solutions.sentry.io/issues/133584982/) | 4 | 2026-07-11 |
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 4 | 2026-07-11 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-field | [Error: 400: PGRST204](https://eq-solutions.sentry.io/issues/133586672/) | 1 | 2026-07-11 |
| eq-field | [Error: LEAVE_DIAG_PIPETEST 1783724352017](https://eq-solutions.sentry.io/issues/133570134/) | 1 | 2026-07-10 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-11 | eq-shell | [#748](https://github.com/eq-solutions/eq-shell/pull/748) feat(comms): crew = the Field "Comms" team (retire the parallel t |
| 2026-07-11 | eq-shell | [#747](https://github.com/eq-solutions/eq-shell/pull/747) feat(comms): trim the fortnight view — this-week default + hide i |
| 2026-07-11 | eq-shell | [#746](https://github.com/eq-solutions/eq-shell/pull/746) chore(armada): set maxConcurrentBuilds=3 for parallel fleet build |
| 2026-07-11 | eq-shell | [#743](https://github.com/eq-solutions/eq-shell/pull/743) fix(security): remove anon cross-tenant access on tender_enrichme |
| 2026-07-11 | eq-shell | [#745](https://github.com/eq-solutions/eq-shell/pull/745) fix(crm-write): narrow bare catch on link-table writes to missing |
| 2026-07-11 | eq-shell | [#744](https://github.com/eq-solutions/eq-shell/pull/744) feat(comms): Move 5 — the comms crew (scope the grid + picker to  |
| 2026-07-11 | eq-shell | [#635](https://github.com/eq-solutions/eq-shell/pull/635) feat(canonical-api): move APP_TENANT_SCOPE allow-list to a shell_ |
| 2026-07-11 | eq-shell | [#742](https://github.com/eq-solutions/eq-shell/pull/742) feat(comms): Move 4 — the fortnight job agenda (the Monday driver |
| 2026-07-11 | eq-shell | [#637](https://github.com/eq-solutions/eq-shell/pull/637) docs: pnpm-workspace.yaml — packages are vendored, not a git subm |
| 2026-07-11 | eq-shell | [#636](https://github.com/eq-solutions/eq-shell/pull/636) build: pin @eq-solutions/ui to release tag v1.10.0 for reproducib |
| 2026-07-11 | eq-shell | [#740](https://github.com/eq-solutions/eq-shell/pull/740) perf(nav): immutable-cache assets + gate/sample analytics (Shell  |
| 2026-07-11 | eq-shell | [#741](https://github.com/eq-solutions/eq-shell/pull/741) feat(comms): Move 3 — roster is the single source for 'who's on a |
| 2026-07-11 | eq-shell | [#739](https://github.com/eq-solutions/eq-shell/pull/739) chore(armada): enable cartography for eq-shell |
| 2026-07-11 | eq-solves-service | [#494](https://github.com/eq-solutions/eq-service/pull/494) perf(service): lazy-load posthog-js off the boot critical path +  |
| 2026-07-11 | eq-field | [#451](https://github.com/eq-solutions/eq-field/pull/451) v3.5.296 — Safety offline queue unwedged (stale sks_rep payload + |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Plan saved 2026-07-11:** [`eq/field-eq-core-only-plan.md`](field-eq-core-only-plan.md). 3-phase, single-repo (eq-field). Decided: role-based supervision, **full strip**; keep `?tenant=demo` in-memory slug.
- **Arm/build the queued fleet bugs** — #736 (invite-users-batch entitlements), #737 (zero-row 404), #705 (eq-intake xlsx) armed, not yet built. #734 (quote-job-consumer) + #735 (RLS `(select)` wrapping) filed UNARMED — Royce's call to arm. _(added 2026-07-11)_
- **zaap tender tables are now service_role-only** (no `authenticated` tenant policies — the create migration's `field_authed_all_*` never reached zaap). Fine if the EQ app reads them via service_role; add the authenticated tenant policy if Field ever needs authed access there. _(added 2026-07-11)_
- **Ledger action item 3 — `2026_06_16_cards_claim_explicit_user_id.sql` must NEVER be re-applied** (documented in the ledger). A replay hazard, not a to-do; flagged so no future apply run picks it up. _(added 2026-07-11)_
- **Ledger action item 4 — cosmetic duplicate unique-index name on jvkn** (harmless, documented). Tidy only if convenient. _(added 2026-07-11)_
- **Make eq-field "Tests + lint" a REQUIRED branch-protection check** — the net now catches undefined-name bugs, but the check isn't required-to-merge, so a red run doesn't block. Interacts with Netlify push-to-deploy; Royce's call. _(added 2026-07-11)_
- Verify where EQ Cards WRITES onboarding — must target canonical / EQ Field (the survivor), not nspbmir (the app being demolished). _(added 2026-07-11)_
- If the manual approach stands: define the stop condition — N consecutive clean weeks across a full roster+timesheet cycle → cut. Put one supervisor + one crew on EQ Field during the run (solo hand-entry proves features, not adoption). Enter independently then compare — don't key EQ Field to force a match. _(added 2026-07-11)_
- ~~Check nspbmir→canonical sync bridge / fix unwired seam~~ — WITHDRAWN 2026-07-11: no automated sync is part of the plan (Royce re-keys manually); the empty `field_*` state is the documented pre-cutover condition, not a gap to fix. _(added 2026-07-11)_
- Get EQ Service from built → executed — 1,358 check-items defined, 0 completed; nothing being ticked in the field. _(added 2026-07-11)_
_…and 299 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
_…and 30 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-11 | [CEO meeting prep for SKS Labour → Cards is the strategic standout](sessions/2026-07-11.md) |
| 2026-07-08 | [eq-shell: Brett Kilpatrick duplicate profile merged live + Cards-onboarding dedup root-caused and fixed](sessions/2026-07-08.md) |
| 2026-07-07 | [eq-cards: onboarding shipped live, approval-flow audit, offline ID card + install nudge](sessions/2026-07-07.md) |
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-11 05:04 UTC._

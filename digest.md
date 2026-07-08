---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-08
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-08 09:51 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-08 09:38 UTC → 2026-07-08 09:51 UTC)

- Merged: eq-shell [#696](https://github.com/eq-solutions/eq-shell/pull/696) fix(shell): embedded rail — un-clip EQ logo, lift icon contr
- Merged: eq-shell [#693](https://github.com/eq-solutions/eq-shell/pull/693) Grant microphone to the Field iframe (voice-to-text on safet
- Merged: eq-shell [#690](https://github.com/eq-solutions/eq-shell/pull/690) fix(staff): lock employment_type to canonical vocabulary; st
- Merged: eq-shell [#688](https://github.com/eq-solutions/eq-shell/pull/688) refactor(shell): retire IconRail, embedded pages use collaps
- Merged: eq-shell [#687](https://github.com/eq-solutions/eq-shell/pull/687) fix(staff): unify employment_type vocabulary with eq-field
- Merged: eq-shell [#683](https://github.com/eq-solutions/eq-shell/pull/683) fix(shell): palette Ctrl+K fallback + Staff continuous scrol
- Merged: eq-shell [#682](https://github.com/eq-solutions/eq-shell/pull/682) fix(provisioning): profiles insert can hit an FK violation o
- Merged: eq-shell [#679](https://github.com/eq-solutions/eq-shell/pull/679) feat(ops): labour hire rates — PDF import confirms update vs

## ⚠ Needs you (4)

- 🔴 **Sentry new error** — `eq-solves-service` [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/)
- 🟠 **Sentry new error** — `eq-shell` [Error: native pipeline query failed: Could not find the tabl](https://eq-solutions.sentry.io/issues/132948690/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 5 | 4d |
| eq-solves-service | ✓ success | 0d ago | 5 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/) | 19 | 2026-07-08 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-shell | [Error: native pipeline query failed: Could not find the table 'app_data.tenders'](https://eq-solutions.sentry.io/issues/132948690/) | 1 | 2026-07-08 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/) | 1 | 2026-07-06 |
| eq-field | [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/) | 1 | 2026-07-05 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-08 | eq-shell | [#704](https://github.com/eq-solutions/eq-shell/pull/704) feat(access): pull in @eq-solutions/roles v2.5.0 (access-model Ph |
| 2026-07-08 | eq-shell | [#703](https://github.com/eq-solutions/eq-shell/pull/703) fix(shell): report native-pipeline query failures instead of swal |
| 2026-07-08 | eq-shell | [#702](https://github.com/eq-solutions/eq-shell/pull/702) feat(ops): branded print-to-PDF export for labour hire weekly cos |
| 2026-07-08 | eq-shell | [#701](https://github.com/eq-solutions/eq-shell/pull/701) fix(shell): stop iOS auto-zoom on login inputs |
| 2026-07-08 | eq-shell | [#700](https://github.com/eq-solutions/eq-shell/pull/700) fix(ops): weekly labour-hire costs miss company-wide allowances |
| 2026-07-08 | eq-shell | [#699](https://github.com/eq-solutions/eq-shell/pull/699) fix(ops): stop stray 'n' keystroke wiping in-progress quote |
| 2026-07-08 | eq-shell | [#698](https://github.com/eq-solutions/eq-shell/pull/698) fix(shell): match all phone formats when self-joining a tenant vi |
| 2026-07-08 | eq-solves-service | [#478](https://github.com/eq-solutions/eq-service/pull/478) feat(observability): add a dashboard-render duration canary |
| 2026-07-08 | eq-solves-service | [#477](https://github.com/eq-solutions/eq-service/pull/477) fix(data-integrity): remove app_data type-bypass hiding wrong col |
| 2026-07-08 | eq-solves-service | [#475](https://github.com/eq-solutions/eq-service/pull/475) fix(shell-embed): detect iframe embedding via Sec-Fetch-Dest head |
| 2026-07-08 | eq-solves-service | [#476](https://github.com/eq-solutions/eq-service/pull/476) feat(rcd): self-provision the standard RCD plan for every tenant |
| 2026-07-08 | eq-solves-service | [#474](https://github.com/eq-solutions/eq-service/pull/474) fix(shell-embed): CHIPS-partition the Shell handoff cookies (Beel |
| 2026-07-08 | eq-solves-service | [#473](https://github.com/eq-solutions/eq-service/pull/473) feat(import): show job-plan coverage on commercial-sheet import |
| 2026-07-08 | eq-field | [#422](https://github.com/eq-solutions/eq-field/pull/422) v3.5.271 — SKS roster/site schema-mismatch fixes |
| 2026-07-08 | eq-field | [#421](https://github.com/eq-solutions/eq-field/pull/421) v3.5.270 — CSP: allow canonical Supabase host in img-src (tenant  |
_Showing 15 of 122 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Recommend Royce kill `task_2911c80d` and `task_abbb7fd0`** (EQ Service "session expired" stuck screen, built on two theories that were retracted before the chips were even created). Found the actual reason these theories were already moot: **eq-service PR #469 (merged 2026-07-07, a full day before these 2 chips were opened) already shipped the real fix** — a `ShellSessionRecovery` component that self-heals a lapsed Shell→Service auth cookie. Whatever these 2 chips are doing now is very likely wasted motion chasing an already-fixed problem. Not killed by this session — recommending only, Royce's call to actually stop them. _(added 2026-07-08)_
- **`task_14031bea` (EQ Service sidebar-header tenant logo clipped, in `ShellSessionRecovery`'s fallback UI) is still genuinely open** — confirmed PR #469 explicitly scoped this out ("does not touch the eq-shell embedded chrome... separate repo, tracked separately"). No session currently confirmed working it. _(added 2026-07-08)_
- Revert is structurally non-functional for every SKS roster edit in eq-field (`target_id` always null on reconstructed canonical week-rows) — see the earlier 2026-07-08 eq-field entry for full detail. Not part of PR #422; deliberately left out.
- **Mitchell Forsyrh + Taya Moody** have Cards + roster identity but no Shell login (no PIN set) — need to sign up via the invite run, not fixable from the backend. _(added 2026-07-08)_
- **Calum + Mohamed Zemi Asri** — login-only, no Cards org-link. Calum's email is an external domain (`@ssw.com.au`) and never logged in — needs identity verification before any fix, not auto-resolved. _(added 2026-07-08)_
- **Access-model Phase 1** — convert ~10 Shell `role === '...'` enforcement checks to `can()`; add a lint ratchet. Pre-cutover-safe, Shell-only. _(added 2026-07-08)_
- **Access-model Phase 2 — one admin concept** — retire `org_memberships.role='admin'` as a gate; migrate its 3 known readers (Cards admin UI, jvkn licence-photo RLS, connection-request email lookup). **POST-CUTOVER ONLY** — auth-touching. _(added 2026-07-08)_
- **Access-model Phase 3 — guardrails** — Field/Cards convert to the canonical model properly; split the overloaded `service.create`/`service.close` PermKey by app; fix `check-perm-sync.mjs`'s blind spot (it can't catch a local module *under*-granting vs canonical, only over-granting — found this session); delete "Test - Royce" group; build `why_can()`. _(added 2026-07-08)_
- **`supervisor_category` vocab-lock** — the next drift candidate after `employment_type`, still free text. _(added 2026-07-08)_
- **CA1 still not enabled via core** — its 2 new RCD checks exist but are invisible in the app until `service_enabled` is flipped. Royce is handling this himself. _(carried, Royce-owned)_
_…and 264 more · [eq/pending.md](eq/pending.md)_

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
_…and 28 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-08 | [eq-shell: Brett Kilpatrick duplicate profile merged live + Cards-onboarding dedup root-caused and fixed](sessions/2026-07-08.md) |
| 2026-07-07 | [eq-cards: onboarding shipped live, approval-flow audit, offline ID card + install nudge](sessions/2026-07-07.md) |
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
| 2026-07-05 | [Session — Role Step-Up Charters + generator](sessions/2026-07-05-role-step-up-charters.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-08 09:51 UTC._

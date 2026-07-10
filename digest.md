---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-10
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-10 07:11 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-10 07:08 UTC → 2026-07-10 07:11 UTC)

- Merged: eq-shell [#692](https://github.com/eq-solutions/eq-shell/pull/692) feat(staff): manage supervisor status from Shell's staff edi
- Merged: eq-shell [#691](https://github.com/eq-solutions/eq-shell/pull/691) fix(shell): embedded mobile nav — restore MobileTabBar, reti
- Merged: eq-shell [#686](https://github.com/eq-solutions/eq-shell/pull/686) Fix: app-activation nav bug + bulk toggle + collapsible site
- Merged: eq-shell [#685](https://github.com/eq-solutions/eq-shell/pull/685) fix(drift-check): add app_data.activation_status to KNOWN_LE
- Merged: eq-shell [#680](https://github.com/eq-solutions/eq-shell/pull/680) Admin: one-spot app activation view + canonical entitlement 
- Merged: eq-shell [#679](https://github.com/eq-solutions/eq-shell/pull/679) feat(ops): labour hire rates — PDF import confirms update vs
- Merged: eq-shell [#678](https://github.com/eq-solutions/eq-shell/pull/678) feat(staff): show and edit job_title on the Staff dashboard
- Merged: eq-shell [#676](https://github.com/eq-solutions/eq-shell/pull/676) feat(shell): command palette, skeleton loading, optimistic s

## ⚠ Needs you (2)

- 🔴 **Sentry new error** — `eq-shell` [Error: native pipeline query failed: Could not find the tabl](https://eq-solutions.sentry.io/issues/132948690/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 5 | 6d |
| eq-solves-service | ✓ success | 1d ago | 5 | 3d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 1d ago | 1 | 1d |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: native pipeline query failed: Could not find the table 'app_data.tenders'](https://eq-solutions.sentry.io/issues/132948690/) | 25 | 2026-07-10 |
| eq-solves-service | [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/) | 19 | 2026-07-08 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/) | 1 | 2026-07-06 |
| eq-field | [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/) | 1 | 2026-07-05 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-10 | eq-shell | [#707](https://github.com/eq-solutions/eq-shell/pull/707) fix(quotes): sign quote docs with whoever is logged in |
| 2026-07-10 | eq-field | [#426](https://github.com/eq-solutions/eq-field/pull/426) v3.5.274 — instrument dashboard anniversaries widget |
| 2026-07-10 | eq-field | [#425](https://github.com/eq-solutions/eq-field/pull/425) v3.5.274 — paginate unbounded full-table fetches (1000-row cap fi |
| 2026-07-09 | eq-shell | [#706](https://github.com/eq-solutions/eq-shell/pull/706) fix(quotes): estimator signature on quote docs + master markup dr |
| 2026-07-09 | eq-field | [#424](https://github.com/eq-solutions/eq-field/pull/424) v3.5.273 — Revert now works for SKS roster edits |
| 2026-07-09 | eq-field | [#423](https://github.com/eq-solutions/eq-field/pull/423) fix: roster — self-heal duplicate-key race on first save of a wee |
| 2026-07-08 | eq-shell | [#704](https://github.com/eq-solutions/eq-shell/pull/704) feat(access): pull in @eq-solutions/roles v2.5.0 (access-model Ph |
| 2026-07-08 | eq-shell | [#703](https://github.com/eq-solutions/eq-shell/pull/703) fix(shell): report native-pipeline query failures instead of swal |
| 2026-07-08 | eq-shell | [#702](https://github.com/eq-solutions/eq-shell/pull/702) feat(ops): branded print-to-PDF export for labour hire weekly cos |
| 2026-07-08 | eq-shell | [#701](https://github.com/eq-solutions/eq-shell/pull/701) fix(shell): stop iOS auto-zoom on login inputs |
| 2026-07-08 | eq-shell | [#700](https://github.com/eq-solutions/eq-shell/pull/700) fix(ops): weekly labour-hire costs miss company-wide allowances |
| 2026-07-08 | eq-shell | [#699](https://github.com/eq-solutions/eq-shell/pull/699) fix(ops): stop stray 'n' keystroke wiping in-progress quote |
| 2026-07-08 | eq-shell | [#698](https://github.com/eq-solutions/eq-shell/pull/698) fix(shell): match all phone formats when self-joining a tenant vi |
| 2026-07-08 | eq-solves-service | [#478](https://github.com/eq-solutions/eq-service/pull/478) feat(observability): add a dashboard-render duration canary |
| 2026-07-08 | eq-solves-service | [#477](https://github.com/eq-solutions/eq-service/pull/477) fix(data-integrity): remove app_data type-bypass hiding wrong col |
_Showing 15 of 106 · full record in [sessions/](sessions/)_

## Pending (EQ)

- eq-shell: fix focus-triggered refetch/hydration crash on Field iframe wrapper so spinner doesn't get stuck on tab return _(added 2026-07-10, in progress in separate eq-shell session — task_b2cf81ea)_
- `task_14031bea` — a tenant-logo clip issue is still tracked against `ShellSessionRecovery`'s fallback UI. Correction: the component built in PR #469/#475 renders no logo at all (text + spinner + buttons only) — if a clip is still visible, it's the surrounding Sidebar/Shell chrome rendering around it, not this component itself. _(added 2026-07-08)_
- **Netlify cold-start as a possible slow-dashboard cause** — proposed (a lightweight scheduled "warm ping", same pattern as the 3 existing Netlify scheduled functions in this repo) but not built; wait for the new duration canary's first real event before spending effort here. _(added 2026-07-08)_
- **Further dashboard query consolidation** (fold the sequential site-name lookup + maybe upcoming/recent-checks into the counts RPC, one round-trip instead of several) — real DB-migration work, deferred pending real performance data from the new canary. _(added 2026-07-08)_
- **First-party edge reverse-proxy** (serve `core.eq.solutions/sks/service/*` through a rewrite instead of an iframe) — the architectural endgame if the CHIPS cookie fix (#474) ever fails on another browser; not needed now since CHIPS is confirmed working. _(added 2026-07-08)_
- **Recommend Royce kill `task_2911c80d` and `task_abbb7fd0`** (EQ Service "session expired" stuck screen, built on two theories that were retracted before the chips were even created). Found the actual reason these theories were already moot: **eq-service PR #469 (merged 2026-07-07, a full day before these 2 chips were opened) already shipped the real fix** — a `ShellSessionRecovery` component that self-heals a lapsed Shell→Service auth cookie. Whatever these 2 chips are doing now is very likely wasted motion chasing an already-fixed problem. Not killed by this session — recommending only, Royce's call to actually stop them. _(added 2026-07-08)_
- **`task_14031bea` (EQ Service sidebar-header tenant logo clipped, in `ShellSessionRecovery`'s fallback UI) is still genuinely open** — confirmed PR #469 explicitly scoped this out ("does not touch the eq-shell embedded chrome... separate repo, tracked separately"). No session currently confirmed working it. _(added 2026-07-08)_
- Revert is structurally non-functional for every SKS roster edit in eq-field (`target_id` always null on reconstructed canonical week-rows) — see the earlier 2026-07-08 eq-field entry for full detail. Not part of PR #422; deliberately left out.
- **Mitchell Forsyrh + Taya Moody** have Cards + roster identity but no Shell login (no PIN set) — need to sign up via the invite run, not fixable from the backend. _(added 2026-07-08)_
- **Calum + Mohamed Zemi Asri** — login-only, no Cards org-link. Calum's email is an external domain (`@ssw.com.au`) and never logged in — needs identity verification before any fix, not auto-resolved. _(added 2026-07-08)_
_…and 268 more · [eq/pending.md](eq/pending.md)_

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
_…and 31 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-10 | [Spinner-of-death on tab-return root-caused to eq-shell](sessions/2026-07-10.md) |
| 2026-07-08 | [eq-shell: Brett Kilpatrick duplicate profile merged live + Cards-onboarding dedup root-caused and fixed](sessions/2026-07-08.md) |
| 2026-07-07 | [eq-cards: onboarding shipped live, approval-flow audit, offline ID card + install nudge](sessions/2026-07-07.md) |
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-10 07:11 UTC._

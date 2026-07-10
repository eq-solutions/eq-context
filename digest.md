---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-10
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-10 23:54 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-10 23:49 UTC → 2026-07-10 23:54 UTC)

- Merged: eq-shell [#717](https://github.com/eq-solutions/eq-shell/pull/717) fix(customers): don't lose a typed site/contact on Continue/
- Merged: eq-shell [#714](https://github.com/eq-solutions/eq-shell/pull/714) fix(shell): scope embedded-app handoff overlay to the iframe
- Merged: eq-shell [#707](https://github.com/eq-solutions/eq-shell/pull/707) fix(quotes): sign quote docs with whoever is logged in
- Merged: eq-shell [#704](https://github.com/eq-solutions/eq-shell/pull/704) feat(access): pull in @eq-solutions/roles v2.5.0 (access-mod
- Merged: eq-shell [#702](https://github.com/eq-solutions/eq-shell/pull/702) feat(ops): branded print-to-PDF export for labour hire weekl
- Merged: eq-shell [#700](https://github.com/eq-solutions/eq-shell/pull/700) fix(ops): weekly labour-hire costs miss company-wide allowan
- Merged: eq-shell [#698](https://github.com/eq-solutions/eq-shell/pull/698) fix(shell): match all phone formats when self-joining a tena
- Merged: eq-shell [#696](https://github.com/eq-solutions/eq-shell/pull/696) fix(shell): embedded rail — un-clip EQ logo, lift icon contr

## ⚠ Needs you (6)

- 🔴 **Sentry new error** — `eq-shell` [Error: native pipeline query failed: Could not find the tabl](https://eq-solutions.sentry.io/issues/132948690/)
- 🟠 **PR aging 7d** — eq-shell [#637](https://github.com/eq-solutions/eq-shell/pull/637) "docs: pnpm-workspace.yaml — packages are vendored, not a git submodule"
- 🟠 **PR aging 7d** — eq-shell [#636](https://github.com/eq-solutions/eq-shell/pull/636) "build: pin @eq-solutions/ui to release tag v1.10.0 for reproducible bu"
- 🟠 **PR aging 7d** — eq-shell [#635](https://github.com/eq-solutions/eq-shell/pull/635) "feat(canonical-api): move APP_TENANT_SCOPE allow-list to a shell_contr"
- 🟠 **Sentry new error** — `eq-field` [Error: LEAVE_DIAG {"ver":"3.5.291","slug":"sks","winsb":"eho](https://eq-solutions.sentry.io/issues/133570956/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 6 | 7d |
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
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-field | [Error: LEAVE_DIAG_PIPETEST 1783724352017](https://eq-solutions.sentry.io/issues/133570134/) | 1 | 2026-07-10 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/) | 1 | 2026-07-06 |
| eq-field | [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/) | 1 | 2026-07-05 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-10 | eq-shell | [#738](https://github.com/eq-solutions/eq-shell/pull/738) feat(comms): Move 2c — fortnight capacity grid |
| 2026-07-10 | eq-shell | [#731](https://github.com/eq-solutions/eq-shell/pull/731) feat(comms): Move 1.5 + 2b — filters/simplification, and book cre |
| 2026-07-10 | eq-shell | [#730](https://github.com/eq-solutions/eq-shell/pull/730) docs(control-plane): tombstone 3 misfiled cross-plane migrations  |
| 2026-07-10 | eq-shell | [#728](https://github.com/eq-solutions/eq-shell/pull/728) feat(staff): surface tenant required-credential gaps in the Train |
| 2026-07-10 | eq-shell | [#729](https://github.com/eq-solutions/eq-shell/pull/729) docs(control-plane): verified applied-state ledger — 61 files rec |
| 2026-07-10 | eq-shell | [#727](https://github.com/eq-solutions/eq-shell/pull/727) feat(comms): Move 1 — job card catches up to the planner |
| 2026-07-10 | eq-shell | [#726](https://github.com/eq-solutions/eq-shell/pull/726) ci(shell): control-plane migration reminder (close the merge≠appl |
| 2026-07-10 | eq-shell | [#725](https://github.com/eq-solutions/eq-shell/pull/725) fix(csp): allow Clarity's rotating collector subdomains (*.clarit |
| 2026-07-10 | eq-shell | [#721](https://github.com/eq-solutions/eq-shell/pull/721) security(canonical): revoke anon/PUBLIC EXECUTE on Ops/Intake SEC |
| 2026-07-10 | eq-shell | [#724](https://github.com/eq-solutions/eq-shell/pull/724) fix(sync): worker→staff sync matches identity + merges instead of |
| 2026-07-10 | eq-shell | [#723](https://github.com/eq-solutions/eq-shell/pull/723) polish(field-iframe): make restore-failed reachable on repeat han |
| 2026-07-10 | eq-shell | [#722](https://github.com/eq-solutions/eq-shell/pull/722) feat(customers): link contacts to sites inside the New customer f |
| 2026-07-10 | eq-shell | [#720](https://github.com/eq-solutions/eq-shell/pull/720) fix(briefing): swallow PGRST205 for dropped app_data.tenders |
| 2026-07-10 | eq-shell | [#718](https://github.com/eq-solutions/eq-shell/pull/718) fix(field-iframe): self-healing handoff — grace window + one-shot |
| 2026-07-10 | eq-shell | [#719](https://github.com/eq-solutions/eq-shell/pull/719) fix(staff): normalize phone before dedup match on Cards approval |
_Showing 15 of 109 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Ledger action item 3 — `2026_06_16_cards_claim_explicit_user_id.sql` must NEVER be re-applied** (documented in the ledger). A replay hazard, not a to-do; flagged so no future apply run picks it up. _(added 2026-07-11)_
- **Ledger action item 4 — cosmetic duplicate unique-index name on jvkn** (harmless, documented). Tidy only if convenient. _(added 2026-07-11)_
- **Make eq-field "Tests + lint" a REQUIRED branch-protection check** — the net now catches undefined-name bugs, but the check isn't required-to-merge, so a red run doesn't block. Interacts with Netlify push-to-deploy; Royce's call. _(added 2026-07-11)_
- Verify where EQ Cards WRITES onboarding — must target canonical / EQ Field (the survivor), not nspbmir (the app being demolished). _(added 2026-07-11)_
- If the manual approach stands: define the stop condition — N consecutive clean weeks across a full roster+timesheet cycle → cut. Put one supervisor + one crew on EQ Field during the run (solo hand-entry proves features, not adoption). Enter independently then compare — don't key EQ Field to force a match. _(added 2026-07-11)_
- ~~Check nspbmir→canonical sync bridge / fix unwired seam~~ — WITHDRAWN 2026-07-11: no automated sync is part of the plan (Royce re-keys manually); the empty `field_*` state is the documented pre-cutover condition, not a gap to fix. _(added 2026-07-11)_
- Get EQ Service from built → executed — 1,358 check-items defined, 0 completed; nothing being ticked in the field. _(added 2026-07-11)_
- Compute the Cards "one number" for the CEO ask — onboarding time saved (time-to-site-ready × worker volume) + expiry/audit risk removed. Royce to supply volumes. _(added 2026-07-11)_
- **DEFINITIVE NEXT STEP: get `TENANT.ORG_SLUG` (and `APP_VERSION`, `canon`, `SB_URL`) from the SKS Field frame.** Never obtained directly. One-liner to paste in the `eq-field.netlify.app` frame: `JSON.stringify({v:APP_VERSION,slug:(window.TENANT||{}).ORG_SLUG,sb:SB_URL,canon:EQ_LEAVE_ADAPTER.isCanonicalLeaveTenant(true),allow:[...EQ_LEAVE_ADAPTER._LEAVE_CANONICAL_TENANTS]})`. If `slug==='sks'` now → gate is fixed, bug is DOWNSTREAM in the read (chase there). If `slug!=='sks'` → v3.5.283 didn't fix resolution; the slug is landing wrong for a deeper reason. If `v!=='3.5.283'` → SW never updated, no fix loaded. _(added 2026-07-10)_
- **`refetch:0` (200 empty, NOT 401) is unexplained** — with canon:false the read should hit the service_role-only `field_leave_requests` twin and 401, not return empty. So either the twin grant changed, or the read hits an empty in-place/public path. Resolve alongside the slug value. _(added 2026-07-10)_
_…and 297 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-10 23:54 UTC._

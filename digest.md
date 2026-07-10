---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-10
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-10 10:10 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-10 10:08 UTC → 2026-07-10 10:10 UTC)

- Merged: eq-shell [#721](https://github.com/eq-solutions/eq-shell/pull/721) security(canonical): revoke anon/PUBLIC EXECUTE on Ops/Intak
- Merged: eq-shell [#706](https://github.com/eq-solutions/eq-shell/pull/706) fix(quotes): estimator signature on quote docs + master mark
- Merged: eq-shell [#703](https://github.com/eq-solutions/eq-shell/pull/703) fix(shell): report native-pipeline query failures instead of
- Merged: eq-shell [#701](https://github.com/eq-solutions/eq-shell/pull/701) fix(shell): stop iOS auto-zoom on login inputs
- Merged: eq-shell [#699](https://github.com/eq-solutions/eq-shell/pull/699) fix(ops): stop stray 'n' keystroke wiping in-progress quote
- Merged: eq-shell [#691](https://github.com/eq-solutions/eq-shell/pull/691) fix(shell): embedded mobile nav — restore MobileTabBar, reti
- Merged: eq-shell [#690](https://github.com/eq-solutions/eq-shell/pull/690) fix(staff): lock employment_type to canonical vocabulary; st
- Merged: eq-shell [#688](https://github.com/eq-solutions/eq-shell/pull/688) refactor(shell): retire IconRail, embedded pages use collaps

## ⚠ Needs you (2)

- 🔴 **Sentry new error** — `eq-shell` [Error: native pipeline query failed: Could not find the tabl](https://eq-solutions.sentry.io/issues/132948690/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 6 | 6d |
| eq-solves-service | ✓ success | 0d ago | 5 | 4d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | 0d |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: native pipeline query failed: Could not find the table 'app_data.tenders'](https://eq-solutions.sentry.io/issues/132948690/) | 31 | 2026-07-10 |
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
| 2026-07-10 | eq-shell | [#721](https://github.com/eq-solutions/eq-shell/pull/721) security(canonical): revoke anon/PUBLIC EXECUTE on Ops/Intake SEC |
| 2026-07-10 | eq-shell | [#724](https://github.com/eq-solutions/eq-shell/pull/724) fix(sync): worker→staff sync matches identity + merges instead of |
| 2026-07-10 | eq-shell | [#723](https://github.com/eq-solutions/eq-shell/pull/723) polish(field-iframe): make restore-failed reachable on repeat han |
| 2026-07-10 | eq-shell | [#722](https://github.com/eq-solutions/eq-shell/pull/722) feat(customers): link contacts to sites inside the New customer f |
| 2026-07-10 | eq-shell | [#720](https://github.com/eq-solutions/eq-shell/pull/720) fix(briefing): swallow PGRST205 for dropped app_data.tenders |
| 2026-07-10 | eq-shell | [#718](https://github.com/eq-solutions/eq-shell/pull/718) fix(field-iframe): self-healing handoff — grace window + one-shot |
| 2026-07-10 | eq-shell | [#719](https://github.com/eq-solutions/eq-shell/pull/719) fix(staff): normalize phone before dedup match on Cards approval |
| 2026-07-10 | eq-shell | [#717](https://github.com/eq-solutions/eq-shell/pull/717) fix(customers): don't lose a typed site/contact on Continue/Finis |
| 2026-07-10 | eq-shell | [#716](https://github.com/eq-solutions/eq-shell/pull/716) feat(customers): add customer creation flow (Customer → Sites → C |
| 2026-07-10 | eq-shell | [#714](https://github.com/eq-solutions/eq-shell/pull/714) fix(shell): scope embedded-app handoff overlay to the iframe pane |
| 2026-07-10 | eq-shell | [#707](https://github.com/eq-solutions/eq-shell/pull/707) fix(quotes): sign quote docs with whoever is logged in |
| 2026-07-10 | eq-solves-service | [#487](https://github.com/eq-solutions/eq-service/pull/487) fix(canonical): move ::uuid inside coalesce in service.tg_*_iud t |
| 2026-07-10 | eq-solves-service | [#486](https://github.com/eq-solutions/eq-service/pull/486) fix(customers): service.customers site-driven — unbreak the empty |
| 2026-07-10 | eq-solves-service | [#485](https://github.com/eq-solutions/eq-service/pull/485) fix(dashboard): Customers + Assets tiles respect the service_enab |
| 2026-07-10 | eq-solves-service | [#484](https://github.com/eq-solutions/eq-service/pull/484) fix(dashboard): Sites tile + map respect the service_enabled acti |
_Showing 15 of 104 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-cards PR #134 (OPEN, not merged) — onboarding flags scoped to account + honest "OCR found nothing".** From the 07-08 continuation: onboarding "shown once" flags were device-local (a reused demo phone silently skipped onboarding on re-signup); now keyed by user id. Plus the licence-scan "found nothing" message no longer falsely claims "that's the back of the card". `flutter analyze` clean; needs review/merge/deploy. _(added 2026-07-10)_
- **Duplicate prevention beyond the two writer fixes: leave it.** Steelmanned a unique normalized-phone index and a detection cron; concluded (with Royce) that for ~85 staff a hard constraint on phone is the wrong tool (phone recycles — see eq-cards 0076 — and gets shared; converts silent dups into blocking 500s). The 80/20 that leading teams do — one identity key + normalize-and-match at write + a merge tool for stragglers — is now in place via #719 + #724. Revisit a merge-UI or constraint ONLY if dups recur after these. _(added 2026-07-10)_
- **Timesheets/other paths that write `app_data.staff`** — audit that every remaining writer routes phone through the shared normalizer (not just the two fixed). Low priority now the two main writers are fixed. _(added 2026-07-10)_
- **`admin-attach-licence-photo` — open a PR** for the `feat/admin-attach-licence-photo` branch (0083 + the function) so live infra isn't untracked drift; or tear it down if the CLI path is preferred. _(added 2026-07-10)_
- **`leave_approval_logs` empty (0 rows) on SKS** — approve/reject decisions aren't being written to the audit-log table. Confirm if an approval audit trail is wanted. _(added 2026-07-10)_
- **All 31 imported SKS leave rows have `approver_id = NULL`** — approver names won't render. Fine if pre-approved historical; backfill if attribution matters. _(added 2026-07-10)_
- **Timesheets don't yet share the leave overlay** — only roster + dashboard read leave_requests live. If timesheets should reflect approved leave, extend the overlay. _(added 2026-07-10)_
- **Three dead RLS-bypassing twins** (`app_data.field_prestarts`/`field_site_diaries`/`field_toolbox_talks`, `security_invoker` NOT SET, service_role-only, unused — safety reads go to `public.*`) — inert today but a latent cross-tenant leak if ever granted to `authenticated`. Cleanup candidates (drop them). _(added 2026-07-10)_
- **Retire the leave/roster/timesheets `field_*` twins?** They're bypassed by the adapters and (for leave/schedule/timesheets) are `security_invoker` but service_role-only. The silent fallback to them is what made the "showed 0" bug possible; #432 makes it loud, but dropping the dead twins would remove the failure class entirely. _(added 2026-07-10)_
- **Root-checkout collision on eq-field happened 3× in one day** — concurrent sessions committed onto each other's branches via the shared `C:\Projects\eq-field` checkout (forced two version re-stamps this session: 277→278→279). Recommend making worktrees mandatory for eq-field, or a pre-commit guard that refuses a commit when HEAD's branch != the session's intended branch. _(added 2026-07-10)_
_…and 286 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-10 | [SKS leave "showed 0" fixed; leave_requests made single source of truth (roster overlays it live)](sessions/2026-07-10.md) |
| 2026-07-08 | [eq-shell: Brett Kilpatrick duplicate profile merged live + Cards-onboarding dedup root-caused and fixed](sessions/2026-07-08.md) |
| 2026-07-07 | [eq-cards: onboarding shipped live, approval-flow audit, offline ID card + install nudge](sessions/2026-07-07.md) |
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-10 10:10 UTC._

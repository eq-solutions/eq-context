---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-15
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-15 06:57 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-15 06:37 UTC → 2026-07-15 06:57 UTC)

- Merged: eq-shell [#849](https://github.com/eq-solutions/eq-shell/pull/849) fix(drift): allow-list service.instrument_calibration_events
- Merged: eq-shell [#848](https://github.com/eq-solutions/eq-shell/pull/848) feat(canonical): site-resolver adjudication — verdict captur
- Merged: eq-shell [#846](https://github.com/eq-solutions/eq-shell/pull/846) feat(audit): Phase 1d (eq-shell) — attribute worker create/e
- Merged: eq-shell [#840](https://github.com/eq-solutions/eq-shell/pull/840) feat(audit): make public.audit_log (credential audit) append
- Merged: eq-shell [#837](https://github.com/eq-solutions/eq-shell/pull/837) feat(audit): make audit_log append-only - Phase 1a immutabil
- Merged: eq-shell [#836](https://github.com/eq-solutions/eq-shell/pull/836) feat(ops): native mobile view for EQ Ops — pipeline cards + 
- Merged: eq-shell [#834](https://github.com/eq-solutions/eq-shell/pull/834) one-login field-first — flag-gated employee→Field on Core en
- Merged: eq-shell [#833](https://github.com/eq-solutions/eq-shell/pull/833) fix(auth): recover from stalled mobile login instead of a fr

## ⚠ Needs you (7)

- 🔴 **Substrate drift** — DRIFT: deploy EQ website (https://eq.solutions): claimed LIVE but reality looks DEAD
- 🟠 **PR aging 8d** — eq-solves-service [#459](https://github.com/eq-solutions/eq-service/pull/459) "chore(deps-dev): bump @vitejs/plugin-react from 6.0.1 to 6.0.3"
- 🟠 **PR aging 8d** — eq-solves-service [#458](https://github.com/eq-solutions/eq-service/pull/458) "chore(deps): bump tailwind-merge from 3.5.0 to 3.6.0"
- 🟠 **PR aging 8d** — eq-solves-service [#456](https://github.com/eq-solutions/eq-service/pull/456) "chore(deps-dev): bump tailwindcss from 4.2.2 to 4.3.2"
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 3 | 0d |
| eq-solves-service | ✓ success | 0d ago | 6 | 8d |
| eq-field | ✓ success | 0d ago | 3 | 2d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 3 | 2026-07-14 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-15 | eq-shell | [#866](https://github.com/eq-solutions/eq-shell/pull/866) feat(brand): dark-background document logo (canonical + handoff) |
| 2026-07-15 | eq-solves-service | [#539](https://github.com/eq-solutions/eq-service/pull/539) refactor(reports): retire Service report-logo pickers — Shell is  |
| 2026-07-15 | eq-solves-service | [#538](https://github.com/eq-solutions/eq-service/pull/538) feat(brand): consume dark-surface document logo from the Shell ha |
| 2026-07-15 | eq-solves-service | [#537](https://github.com/eq-solutions/eq-service/pull/537) fix(auth): report exports 401 under Shell JWT sessions |
| 2026-07-15 | eq-field | [#493](https://github.com/eq-solutions/eq-field/pull/493) fix: Leave calendar weekday header — low-contrast text on navy |
| 2026-07-15 | eq-field | [#492](https://github.com/eq-solutions/eq-field/pull/492) fix(mobile): Forecast page sticky header — white-on-white contras |
| 2026-07-14 | eq-shell | [#856](https://github.com/eq-solutions/eq-shell/pull/856) feat(brand): carry full tenant document palette + doc logo in the |
| 2026-07-14 | eq-shell | [#847](https://github.com/eq-solutions/eq-shell/pull/847) feat(cards): tenant-branded Excel compliance register (shared bui |
| 2026-07-14 | eq-shell | [#861](https://github.com/eq-solutions/eq-shell/pull/861) fix(calibration): retire legacy asset-calibration reads/writes in |
| 2026-07-14 | eq-shell | [#859](https://github.com/eq-solutions/eq-shell/pull/859) fix(audit): lock EXECUTE on public.eq_audit_retention_run (anon/a |
| 2026-07-14 | eq-shell | [#858](https://github.com/eq-solutions/eq-shell/pull/858) fix(auth): bound verify-session body read + de-noise the stall wa |
| 2026-07-14 | eq-shell | [#857](https://github.com/eq-solutions/eq-shell/pull/857) onboarding: manager-push invite funnel becomes the "Add workers"  |
| 2026-07-14 | eq-shell | [#860](https://github.com/eq-solutions/eq-shell/pull/860) feat(audit): Phase 2b — before/after drill-down on the activity l |
| 2026-07-14 | eq-shell | [#855](https://github.com/eq-solutions/eq-shell/pull/855) feat(equipment): re-point Plant & Equipment calibration onto cano |
| 2026-07-14 | eq-shell | [#854](https://github.com/eq-solutions/eq-shell/pull/854) docs(drift): retruth calibration-view allow-list comment (adoptio |
_Showing 15 of 114 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **MERGE (needs Royce): PR #863** — I couldn't merge it myself (merge on this repo auto-deploys auth code, so the tools blocked it). Squash-merge in the GitHub UI when you want it live; no urgency — no live incident. _(added 2026-07-14)_
- **Cleanup, anytime: the old manual colour copy for SKS can be trimmed** now the pipe is self-maintaining — but keep the white on-dark logo, which the admin settings don't carry yet. _(added 2026-07-14)_
- **Follow-up: retire the EQ Service Report-Settings "Dark Surface" picker** now the dark logo is canonical in Shell (kept for now as a harmless local override). _(added 2026-07-14)_
- **DEPLOY (needs Royce, next auth deploy): apply the two database helpers THEN merge PR #862 — now merge-ready.** Brought #862 up to date with main + renumbered its two database updates so they no longer clash with the audit ones; build + tests green. Apply the two helpers (`resolve_invite_auth_identity` + `list_orphan_auth_identities`) FIRST, then merge → auto-deploy. Permission-gated, waits on you. No urgency — the three new users (Rob Baird, Matt Jinks, Tim Watson) accept + sign in on current prod without it (triple-checked clean-slate). _(added 2026-07-14, updated 2026-07-15)_
- **Minor, anytime: 6 users are missing a sign-in record** (their in-app tools would fail to authorise them) — heal by running the existing admin "backfill" action once. Pre-existing, not caused by this work. _(added 2026-07-14)_
- **Outbound email → dev@eq.solutions (staged, NOT deployed).** Changed all system email to send FROM dev@ and route replies to dev@ (was noreply@ with replies going nowhere), plus the 3 in-app "contact us" links → dev@. Code staged on branch `claude/email-new-users-levers-baab69` (uncommitted); the sender env `EMAIL_FROM` is already set on Netlify but needs a redeploy to take effect. Decide: commit → PR → deploy, or drop. _(added 2026-07-15)_
- **NEXT — Claude as the adjudicator on the "unsure" rows.** Labels now accumulate. Wire the AI to read the full record context (customer, neighbouring sites, import source), propose a verdict + a plain-English reason on the ambiguous middle, human confirms with one tap. This is the jump from classical MDM to the ask-anything brain, and it makes the match-key decision self-calibrating instead of a one-time guess. _(added 2026-07-14)_
- **Core-owned merge/retire RPC over `app_data.sites`.** Adjudication records "same"; ACTING on it (merge/retire the duplicate) is still a separate human-gated step with no RPC yet — the survivorship engine. _(added 2026-07-14)_
- **Cross-app attribution (the rest of it)** — Field / Service / Intake still log their own edits as "system"; making those record the person is a multi-app job with no single choke point. _(added 2026-07-14)_
- **Later audit polish** — PDF / branded-report export, and logging who reads the log; then on-request data erasure and anomaly alerts. _(added 2026-07-14; before/after values shipped in #860)_
_…and 354 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
- **eq-shell PR #681 needs review + merge** — fix is already live on ehow (applied directly ahead of the PR); the PR just brings the source-controlled migration back in sync. _(added 2026-07-06)_
_…and 55 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-15 | [Unblocked new-user logins for the SKS demo; made the invite-accept fix merge-ready](sessions/2026-07-15.md) |
| 2026-07-14 | [Merged + deployed the intake vendor-sync and the xlsx security fix](sessions/2026-07-14.md) |
| 2026-07-13 | [SKS plant & equipment restored after a manual asset-register wipe; 2FA grace unchanged](sessions/2026-07-13.md) |
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
| 2026-07-12 | [Session — Substrate Plan v2 (the notebook that tells the truth)](sessions/2026-07-12-substrate-plan-v2.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-15 06:57 UTC._

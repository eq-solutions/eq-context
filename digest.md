---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-16
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-16 14:38 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-16 14:36 UTC → 2026-07-16 14:38 UTC)

- Merged: eq-shell [#857](https://github.com/eq-solutions/eq-shell/pull/857) onboarding: manager-push invite funnel becomes the "Add work
- Merged: eq-shell [#856](https://github.com/eq-solutions/eq-shell/pull/856) feat(brand): carry full tenant document palette + doc logo i
- Merged: eq-shell [#855](https://github.com/eq-solutions/eq-shell/pull/855) feat(equipment): re-point Plant & Equipment calibration onto
- Merged: eq-shell [#854](https://github.com/eq-solutions/eq-shell/pull/854) docs(drift): retruth calibration-view allow-list comment (ad
- Merged: eq-shell [#853](https://github.com/eq-solutions/eq-shell/pull/853) feat(audit): Phase 1c — audit-log retention (13mo hot / 7yr 
- Merged: eq-shell [#850](https://github.com/eq-solutions/eq-shell/pull/850) docs: reflect that Resend email delivery is live in producti
- Merged: eq-shell [#849](https://github.com/eq-solutions/eq-shell/pull/849) fix(drift): allow-list service.instrument_calibration_events
- Merged: eq-shell [#848](https://github.com/eq-solutions/eq-shell/pull/848) feat(canonical): site-resolver adjudication — verdict captur
- ✅ Needs you: 7 → 5

## ⚠ Needs you (5)

- 🔴 **CI cancelled** — eq-solves-service `main`
- 🔴 **Sentry 30 events today** — `eq-shell` [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 1d ago | 3 | 2d |
| eq-solves-service | ⚠ cancelled | -1d ago | 3 | 3d |
| eq-field | ✓ success | 1d ago | 2 | 4d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/) | 30 | 2026-07-16 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 5 | 2026-07-16 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-16 | eq-shell | [#883](https://github.com/eq-solutions/eq-shell/pull/883) perf(quotes): parallelize the quote-open RPC waterfall |
| 2026-07-16 | eq-shell | [#881](https://github.com/eq-solutions/eq-shell/pull/881) perf: capture Core Web Vitals + unsaved-changes guard (Quotes) |
| 2026-07-16 | eq-shell | [#880](https://github.com/eq-solutions/eq-shell/pull/880) feat(intake): usage-based survivor pick for the Sites Dupes tab ( |
| 2026-07-16 | eq-shell | [#879](https://github.com/eq-solutions/eq-shell/pull/879) chore: re-vendor eq-intake/eq-platform (merge-panel UI + self-hos |
| 2026-07-16 | eq-shell | [#878](https://github.com/eq-solutions/eq-shell/pull/878) fix(drift): degrade gracefully on an unreachable tenant |
| 2026-07-16 | eq-shell | [#877](https://github.com/eq-solutions/eq-shell/pull/877) chore: remove dead vendored eq-platform/apps scaffold |
| 2026-07-16 | eq-shell | [#876](https://github.com/eq-solutions/eq-shell/pull/876) feat(intake): merge from the Sites Dupes tab (migration 0186) |
| 2026-07-16 | eq-shell | [#875](https://github.com/eq-solutions/eq-shell/pull/875) fix(admin): use shared APP_LABELS for the Apps toggle list |
| 2026-07-16 | eq-solves-service | [#459](https://github.com/eq-solutions/eq-service/pull/459) chore(deps-dev): bump @vitejs/plugin-react from 6.0.1 to 6.0.3 |
| 2026-07-16 | eq-solves-service | [#458](https://github.com/eq-solutions/eq-service/pull/458) chore(deps): bump tailwind-merge from 3.5.0 to 3.6.0 |
| 2026-07-16 | eq-solves-service | [#456](https://github.com/eq-solutions/eq-service/pull/456) chore(deps-dev): bump tailwindcss from 4.2.2 to 4.3.2 |
| 2026-07-16 | eq-solves-service | [#545](https://github.com/eq-solutions/eq-service/pull/545) fix(admin): remove Connected Apps card — measures retired sync ar |
| 2026-07-16 | eq-solves-service | [#544](https://github.com/eq-solutions/eq-service/pull/544) fix(admin): correct stale card copy, remove unused Today view |
| 2026-07-16 | eq-solves-service | [#543](https://github.com/eq-solutions/eq-service/pull/543) chore(terms): temporarily unpublish /terms pending legal review |
| 2026-07-16 | eq-cards | [#156](https://github.com/eq-solutions/eq-cards/pull/156) chore(legal): soften overseas-disclosure wording in privacy polic |
_Showing 15 of 118 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Not checked: live data cleanliness / Sentry error surfacing on whatever gets demoed live Monday**, and the eq-field Privacy Notice modal's links weren't click-tested (read-only content review only). Offered, Royce hadn't said go as of session close. _(added 2026-07-16)_
- **Not click-tested live** — SKS Pipeline is triple-gated to the SKS tenant; this session had no SKS login to verify either feature by hand. Worth a quick real click-through next time you're signed in, especially "Load sample data" before demoing it to anyone. _(added 2026-07-15)_
- **Small, low-risk: rename the "Field Run-Sheet" button** — Royce noticed it's not obvious this is the report/export button (reads as a document name, not an action, and sits next to "Print Blank for Onsite" which does read as an action). Recommended "Download Run-Sheet" or "Export Run-Sheet" — label-only change, no rename of the underlying feature/code/tests. Awaiting Royce's go-ahead. _(added 2026-07-15)_
- **MERGE (needs Royce): PR #863** — I couldn't merge it myself (merge on this repo auto-deploys auth code, so the tools blocked it). Squash-merge in the GitHub UI when you want it live; no urgency — no live incident. _(added 2026-07-14)_
- **Cleanup, anytime: the old manual colour copy for SKS can be trimmed** now the pipe is self-maintaining — but keep the white on-dark logo, which the admin settings don't carry yet. _(added 2026-07-14)_
- **DEPLOY (needs Royce, next auth deploy): apply the two database helpers THEN merge PR #862 — now merge-ready.** Brought #862 up to date with main + renumbered its two database updates so they no longer clash with the audit ones; build + tests green. Apply the two helpers (`resolve_invite_auth_identity` + `list_orphan_auth_identities`) FIRST, then merge → auto-deploy. Permission-gated, waits on you. No urgency — the three new users (Rob Baird, Matt Jinks, Tim Watson) accept + sign in on current prod without it (triple-checked clean-slate). _(added 2026-07-14, updated 2026-07-15)_
- **Minor, anytime: 6 users are missing a sign-in record** (their in-app tools would fail to authorise them) — heal by running the existing admin "backfill" action once. Pre-existing, not caused by this work. _(added 2026-07-14)_
- **Outbound email → dev@eq.solutions (staged, NOT deployed).** Changed all system email to send FROM dev@ and route replies to dev@ (was noreply@ with replies going nowhere), plus the 3 in-app "contact us" links → dev@. Code staged on branch `claude/email-new-users-levers-baab69` (uncommitted); the sender env `EMAIL_FROM` is already set on Netlify but needs a redeploy to take effect. Decide: commit → PR → deploy, or drop. _(added 2026-07-15)_
- **Seed one realistic flagged pair on ehow for a hands-on demo.** Console currently has 0 flagged rows — nothing real has tripped the write-time resolver yet, so there's nothing to click through end-to-end. Offered to insert one synthetic advisory row; correctly blocked by the auto-mode classifier as a write to shared production SKS data without Royce's explicit go — needs his yes. _(added 2026-07-15)_
- **Later audit polish** — PDF / branded-report export, and logging who reads the log; then on-request data erasure and anomaly alerts. _(added 2026-07-14; before/after values shipped in #860)_
_…and 354 more · [eq/pending.md](eq/pending.md)_

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
_…and 57 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-16 | [verified migration 0185 live, explained the merge feature's location, seeded a real demo pair](sessions/2026-07-16.md) |
| 2026-07-15 | [EQ Service: fixed empty NSX/ACB testing lists in the Shell iframe + Field Run-Sheet dropping recorded breaker data](sessions/2026-07-15.md) |
| 2026-07-14 | [Merged + deployed the intake vendor-sync and the xlsx security fix](sessions/2026-07-14.md) |
| 2026-07-13 | [SKS plant & equipment restored after a manual asset-register wipe; 2FA grace unchanged](sessions/2026-07-13.md) |
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-16 14:38 UTC._

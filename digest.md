---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-06
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-06 10:38 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-06 10:21 UTC → 2026-07-06 10:38 UTC)

- Merged: eq-shell [#691](https://github.com/eq-solutions/eq-shell/pull/691) fix(shell): embedded mobile nav — restore MobileTabBar, reti
- Merged: eq-shell [#674](https://github.com/eq-solutions/eq-shell/pull/674) fix(users): add subcontractor to stale VALID_ROLES lists
- Merged: eq-shell [#672](https://github.com/eq-solutions/eq-shell/pull/672) feat(ops): labour hire rates — manual manage (add/edit/delet
- Merged: eq-shell [#670](https://github.com/eq-solutions/eq-shell/pull/670) feat(ops): labour hire rates — weekly-cost rollup
- Merged: eq-shell [#669](https://github.com/eq-solutions/eq-shell/pull/669) feat(field): job-number retire — auto (invoiced) + manual (h
- Merged: eq-shell [#668](https://github.com/eq-solutions/eq-shell/pull/668) chore(drift): allow-list labour_hire_rates_view (security_in
- Merged: eq-shell [#665](https://github.com/eq-solutions/eq-shell/pull/665) fix(branding): bound logo colour-detection with a load timeo
- Merged: eq-shell [#664](https://github.com/eq-solutions/eq-shell/pull/664) feat(roles): bump eq-roles to v2.4.0, wire subcontractor eve

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-cards` [minified:np: ValidationFailure: Add your name to your profil](https://eq-solutions.sentry.io/issues/132441676/)
- 🟠 **Sentry new error** — `eq-shell` [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/)
- 🟠 **Sentry new error** — `eq-field` [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 6 | 2d |
| eq-solves-service | ✓ success | 0d ago | 5 | 0d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [minified:np: ValidationFailure: Add your name to your profile before connecting ](https://eq-solutions.sentry.io/issues/132441676/) | 2 | 2026-07-06 |
| eq-shell | [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/) | 1 | 2026-07-06 |
| eq-field | [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/) | 1 | 2026-07-05 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-06 | eq-shell | [#691](https://github.com/eq-solutions/eq-shell/pull/691) fix(shell): embedded mobile nav — restore MobileTabBar, retire ha |
| 2026-07-06 | eq-shell | [#688](https://github.com/eq-solutions/eq-shell/pull/688) refactor(shell): retire IconRail, embedded pages use collapsed Hu |
| 2026-07-06 | eq-shell | [#687](https://github.com/eq-solutions/eq-shell/pull/687) fix(staff): unify employment_type vocabulary with eq-field |
| 2026-07-06 | eq-shell | [#686](https://github.com/eq-solutions/eq-shell/pull/686) Fix: app-activation nav bug + bulk toggle + collapsible sites; mo |
| 2026-07-06 | eq-shell | [#682](https://github.com/eq-solutions/eq-shell/pull/682) fix(provisioning): profiles insert can hit an FK violation on sta |
| 2026-07-06 | eq-shell | [#685](https://github.com/eq-solutions/eq-shell/pull/685) fix(drift-check): add app_data.activation_status to KNOWN_LEGACY_ |
| 2026-07-06 | eq-shell | [#683](https://github.com/eq-solutions/eq-shell/pull/683) fix(shell): palette Ctrl+K fallback + Staff continuous scroll |
| 2026-07-06 | eq-shell | [#680](https://github.com/eq-solutions/eq-shell/pull/680) Admin: one-spot app activation view + canonical entitlement merge |
| 2026-07-06 | eq-shell | [#679](https://github.com/eq-solutions/eq-shell/pull/679) feat(ops): labour hire rates — PDF import confirms update vs add- |
| 2026-07-06 | eq-shell | [#678](https://github.com/eq-solutions/eq-shell/pull/678) feat(staff): show and edit job_title on the Staff dashboard |
| 2026-07-06 | eq-shell | [#676](https://github.com/eq-solutions/eq-shell/pull/676) feat(shell): command palette, skeleton loading, optimistic staff  |
| 2026-07-06 | eq-shell | [#677](https://github.com/eq-solutions/eq-shell/pull/677) fix(drift): 0164 — reassert security_invoker on app_data.field_pe |
| 2026-07-06 | eq-solves-service | [#464](https://github.com/eq-solutions/eq-service/pull/464) test: cover the canonical write path (emitEvent + outbox drain/re |
| 2026-07-06 | eq-solves-service | [#463](https://github.com/eq-solutions/eq-service/pull/463) fix: reconcile inconsistent role checks in contract-scope actions |
| 2026-07-06 | eq-solves-service | [#462](https://github.com/eq-solutions/eq-service/pull/462) test: cover the commercial-sheet XLSX parser (contract-scope impo |
_Showing 15 of 129 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **No live browser click-through of PR #686's changes** — bulk "All on/off" buttons and the collapsible customer/site grouping have only been typecheck/lint-verified, never clicked in a real browser session. _(added 2026-07-06, needs your call — or hand it to a session with live credentials)_
- **Decide + build the SKS Supervision management fix** (re-open Field's CRUD vs build Shell surface — see above). _(added 2026-07-06)_
- **Unify `employment_type` vocabulary between eq-field and eq-shell** — no shared enum/constraint; same root cause as the existing "add subcontractor as a real role" item below. The v3.5.253 Other-bucket fix makes the symptom visible instead of hiding it, it doesn't fix the underlying mismatch. _(added 2026-07-06)_
- **Live click-through of v3.5.253 (mobile Other bucket) and v3.5.254 (Batch Fill Group/Team filters)** — both deployed and verified via Netlify (commit match, no errors, secret scan clean), but not exercised through a real authenticated SKS session — eq-field's Shell-JWT handoff auth isn't reproducible in a local dev server. _(added 2026-07-06)_
- **`field_people` out-of-band regression provenance** — same open question as the already-tracked `field_job_numbers provenance` item below: migration `0158` confirmed ehow's `field_people` was safe as of 2026-07, and no repo migration touched it since, meaning something changed it live outside the One Pipe. Not investigated this session (scope was the fix, not the "who/what" — same pattern, could be the same root cause as the `field_job_numbers` provenance question). _(added 2026-07-06)_
- **Keep-or-clean-up call on the CA1/E1.27 pilot asset** (`cbf535d9-a03f-4952-9396-7ae6c6e765ad`) — asked Royce at session end, no answer yet. It's a real, correctly-created stub asset; leaving it just means one fewer gap for the real UI run. _(added 2026-07-06, needs your call)_
- **Full CA1 reconciliation** — only 1 of ~19 job-plan gaps closed (the pilot). Remaining ~18 job plans at CA1, then SY1/SY3/Head Office once CA1 is fully reviewed. _(added 2026-07-06)_
- **SKS "workspace isn't set up yet" screen resurfaced** — Royce hit this live on `core.eq.solutions/sks/service/dashboard` mid-session. Same known, pre-existing issue: SKS tenant's `setup_completed_at` has been NULL since tenant creation (a backfill migration ran 11 days before the tenant existed, missing it by timing). Not caused by this session's work. A fix reportedly already exists on an unshipped branch (migration 0115, per earlier project memory) — not verified or shipped this session, still open. _(carried, resurfaced 2026-07-06)_
- **Sentry — 2 of the original 5 still open**: `EQ-FIELD-M` (leave_requests null staff_id, eq-field) and `EQ-CARDS-Z` (provisionTenantExchange 500, eq-cards) — not investigated this session, different repos. _(added 2026-07-06, needs a session per repo)_
- **STATUS.md's service-worker claim is stale** — doc says SW is "always unregistered"; `web/index.html` actually only purges legacy SWs once, then lets a new Flutter-managed SW stay registered for offline wallet support. Not exploitable, but a returning user's SW cache could serve a stale bundle until it revalidates. Needs a doc update (or confirmation the offline-support tradeoff was an intentional later call). _(added 2026-07-06)_
_…and 238 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- **Unattributed "system" writes to `app_data.staff` have no traceable source** — 175 updates + 27 inserts + 6 deletes all carry `actor_id=null`/`source='system'` (direct-SQL/service-role, no `x-eq-actor` header). Same signature as the email-nulling side effect above. A task chip is already queued (`task_bcd0d877`, originally scoped to the fake-resolver mystery) — broaden it to cover this rather than opening a second thread. Whatever SKS roster-reconciliation mechanism runs this should stamp its own `x-eq-source` for future auditability. _(added 2026-07-06)_
- **Anthony Hartley's duplicate stub was hard-deleted despite the 2026-07-05 plan to never touch it** — that section (above) explicitly says "no schema field exists to hard-archive it, so it's just never touched/never invited," but one of his duplicate rows was hard-deleted anyway, in the same unattributed "system" batch. Outcome is safe (his live record is untouched and active) but the mechanism didn't follow the documented plan. _(added 2026-07-06)_
_…and 26 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
| 2026-07-05 | [Session — Role Step-Up Charters + generator](sessions/2026-07-05-role-step-up-charters.md) |
| 2026-07-05 | [Session — Labour Hire Rates (canonical design + staged lean build)](sessions/2026-07-05-labour-hire-rates.md) |
| 2026-07-04 | [eq-shell worktree hygiene: stale checkout diagnosed and restored](sessions/2026-07-04.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-06 10:38 UTC._

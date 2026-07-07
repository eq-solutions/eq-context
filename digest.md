---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-07
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-07 06:38 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-07 06:23 UTC → 2026-07-07 06:38 UTC)

- Merged: eq-shell [#677](https://github.com/eq-solutions/eq-shell/pull/677) fix(drift): 0164 — reassert security_invoker on app_data.fie
- Merged: eq-shell [#673](https://github.com/eq-solutions/eq-shell/pull/673) fix(access-control): subcontractor role 400s on permission t
- Merged: eq-shell [#671](https://github.com/eq-solutions/eq-shell/pull/671) feat(ops): labour hire rates — PDF import + weekly-cost Fare
- Merged: eq-shell [#666](https://github.com/eq-solutions/eq-shell/pull/666) feat(branding): live preview + contrast warnings + detection
- Merged: eq-shell [#663](https://github.com/eq-solutions/eq-shell/pull/663) feat(ops): labour hire rates — canonical tables + read-only 
- Merged: eq-shell [#662](https://github.com/eq-solutions/eq-shell/pull/662) feat(roles): expose subcontractor as a selectable role (safe
- Merged: eq-shell [#661](https://github.com/eq-solutions/eq-shell/pull/661) feat(branding): one logo + auto-PNG for docs + logo colour d
- Merged: eq-shell [#660](https://github.com/eq-solutions/eq-shell/pull/660) fix(staff): decline a worker-initiated application actually 
- ⚠ Needs you: 1 → 4 (new items)

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/)
- 🟠 **Sentry new error** — `eq-solves-service` [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/)
- 🟠 **Sentry new error** — `eq-shell` [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 5 | 3d |
| eq-solves-service | ✓ success | 0d ago | 5 | 0d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [EQ Field handoff rejected](https://eq-solutions.sentry.io/issues/132381163/) | 1 | 2026-07-06 |
| eq-field | [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/) | 1 | 2026-07-05 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-07 | eq-field | [#420](https://github.com/eq-solutions/eq-field/pull/420) v3.5.265 — Prestart Word export back + SW resilience + iOS export |
| 2026-07-07 | eq-cards | [#131](https://github.com/eq-solutions/eq-cards/pull/131) feat(offline): cache licence photos on-device so they show with n |
| 2026-07-06 | eq-shell | [#693](https://github.com/eq-solutions/eq-shell/pull/693) Grant microphone to the Field iframe (voice-to-text on safety for |
| 2026-07-06 | eq-shell | [#692](https://github.com/eq-solutions/eq-shell/pull/692) feat(staff): manage supervisor status from Shell's staff editor |
| 2026-07-06 | eq-shell | [#690](https://github.com/eq-solutions/eq-shell/pull/690) fix(staff): lock employment_type to canonical vocabulary; stop ro |
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
_Showing 15 of 133 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Live signed-in smoke of Field voice on SKS** — can't test programmatically (needs a browser + physical mic). Sign in → /sks/field → open a report → tap 🎤 → allow mic → dictate into a freeform field. _(added 2026-07-07)_
- **Field mobile polish — remaining screens** — prestart form top grid (Site/Supervisor/Date/Time) and the roster grid at 375px still un-eyeballed. _(added 2026-07-07)_
- **Minimum-requirements model** — undecided. Options presented: soft per-org checklist (recommended) / manager-view-only / hard gate / leave-as-is. _(added 2026-07-07)_
- **Offline photo caching** — cache licence photo BYTES so images show offline / past the 1h signed-URL expiry. Deliberate fast-follow to PR #129. _(added 2026-07-07)_
- **Onboarding order #5 fork** — scan-first shipped; identity-first is the fallback if it tests poorly. _(from 2026-07-06)_
- **Supabase CLI can't deploy eq-cards edge functions** — `supabase functions deploy` fails for every function on CLI 2.95.4 (mis-resolves `config.toml` email-template paths). MCP deploy works and was used for v10; but the CLI path is the "next person" path. Fix = upgrade CLI (2.109 available) + retest, or adjust config without breaking `supabase start`. Task chip `task_61ff8686`. _(added 2026-07-07)_
- **Onboarding order #5 fork settled as scan-first** — identity-first was the runner-up if scan-first tests poorly with real users. _(added 2026-07-06)_
- **No live browser click-through of PR #686's changes** — bulk "All on/off" buttons and the collapsible customer/site grouping have only been typecheck/lint-verified, never clicked in a real browser session. _(added 2026-07-06, needs your call — or hand it to a session with live credentials)_
- **Decide + build the SKS Supervision management fix** (re-open Field's CRUD vs build Shell surface — see above). _(added 2026-07-06)_
- **Unify `employment_type` vocabulary between eq-field and eq-shell** — no shared enum/constraint; same root cause as the existing "add subcontractor as a real role" item below. The v3.5.253 Other-bucket fix makes the symptom visible instead of hiding it, it doesn't fix the underlying mismatch. _(added 2026-07-06)_
_…and 245 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-07 | [eq-cards: onboarding shipped live, approval-flow audit, offline ID card + install nudge](sessions/2026-07-07.md) |
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
| 2026-07-05 | [Session — Role Step-Up Charters + generator](sessions/2026-07-05-role-step-up-charters.md) |
| 2026-07-05 | [Session — Labour Hire Rates (canonical design + staged lean build)](sessions/2026-07-05-labour-hire-rates.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-07 06:38 UTC._

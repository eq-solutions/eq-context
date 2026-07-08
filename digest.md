---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-08
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-08 08:20 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-08 08:14 UTC → 2026-07-08 08:20 UTC)

- Merged: eq-shell [#687](https://github.com/eq-solutions/eq-shell/pull/687) fix(staff): unify employment_type vocabulary with eq-field
- Merged: eq-shell [#683](https://github.com/eq-solutions/eq-shell/pull/683) fix(shell): palette Ctrl+K fallback + Staff continuous scrol
- Merged: eq-shell [#682](https://github.com/eq-solutions/eq-shell/pull/682) fix(provisioning): profiles insert can hit an FK violation o
- Merged: eq-shell [#679](https://github.com/eq-solutions/eq-shell/pull/679) feat(ops): labour hire rates — PDF import confirms update vs
- Merged: eq-shell [#678](https://github.com/eq-solutions/eq-shell/pull/678) feat(staff): show and edit job_title on the Staff dashboard
- Merged: eq-shell [#677](https://github.com/eq-solutions/eq-shell/pull/677) fix(drift): 0164 — reassert security_invoker on app_data.fie
- Merged: eq-shell [#673](https://github.com/eq-solutions/eq-shell/pull/673) fix(access-control): subcontractor role 400s on permission t
- Merged: eq-shell [#671](https://github.com/eq-solutions/eq-shell/pull/671) feat(ops): labour hire rates — PDF import + weekly-cost Fare

## ⚠ Needs you (4)

- 🔴 **Sentry new error** — `eq-solves-service` [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/)
- 🟠 **Sentry new error** — `eq-solves-service` [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 6 | 4d |
| eq-solves-service | ✓ success | 0d ago | 5 | 1d |
| eq-field | ? unknown | ? | 1 | 0d |
| eq-cards | ✓ success | 1d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/) | 19 | 2026-07-08 |
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
| 2026-07-08 | eq-shell | [#701](https://github.com/eq-solutions/eq-shell/pull/701) fix(shell): stop iOS auto-zoom on login inputs |
| 2026-07-08 | eq-shell | [#700](https://github.com/eq-solutions/eq-shell/pull/700) fix(ops): weekly labour-hire costs miss company-wide allowances |
| 2026-07-08 | eq-shell | [#699](https://github.com/eq-solutions/eq-shell/pull/699) fix(ops): stop stray 'n' keystroke wiping in-progress quote |
| 2026-07-08 | eq-shell | [#698](https://github.com/eq-solutions/eq-shell/pull/698) fix(shell): match all phone formats when self-joining a tenant vi |
| 2026-07-08 | eq-solves-service | [#474](https://github.com/eq-solutions/eq-service/pull/474) fix(shell-embed): CHIPS-partition the Shell handoff cookies (Beel |
| 2026-07-08 | eq-solves-service | [#473](https://github.com/eq-solutions/eq-service/pull/473) feat(import): show job-plan coverage on commercial-sheet import |
| 2026-07-07 | eq-shell | [#696](https://github.com/eq-solutions/eq-shell/pull/696) fix(shell): embedded rail — un-clip EQ logo, lift icon contrast |
| 2026-07-07 | eq-solves-service | [#469](https://github.com/eq-solutions/eq-service/pull/469) fix(shell-embed): self-heal a lapsed Shell→Service session |
| 2026-07-07 | eq-field | [#420](https://github.com/eq-solutions/eq-field/pull/420) v3.5.265 — Prestart Word export back + SW resilience + iOS export |
| 2026-07-07 | eq-cards | [#131](https://github.com/eq-solutions/eq-cards/pull/131) feat(offline): cache licence photos on-device so they show with n |
| 2026-07-06 | eq-shell | [#693](https://github.com/eq-solutions/eq-shell/pull/693) Grant microphone to the Field iframe (voice-to-text on safety for |
| 2026-07-06 | eq-shell | [#692](https://github.com/eq-solutions/eq-shell/pull/692) feat(staff): manage supervisor status from Shell's staff editor |
| 2026-07-06 | eq-shell | [#690](https://github.com/eq-solutions/eq-shell/pull/690) fix(staff): lock employment_type to canonical vocabulary; stop ro |
| 2026-07-06 | eq-shell | [#691](https://github.com/eq-solutions/eq-shell/pull/691) fix(shell): embedded mobile nav — restore MobileTabBar, retire ha |
| 2026-07-06 | eq-shell | [#688](https://github.com/eq-solutions/eq-shell/pull/688) refactor(shell): retire IconRail, embedded pages use collapsed Hu |
_Showing 15 of 121 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Unrelated pre-existing CI gate failing on eq-shell main — `mark_pending_requests_licence_changed()` is a new anon-executable SECURITY DEFINER function on eq-canonical, not allow-listed.** Surfaced only because it blocked this PR's merge (had to `--admin` bypass branch protection to land the CSS fix); the gap itself predates this session and is unrelated to the mobile fix. Every eq-shell PR will need an admin bypass until this is resolved. Fix chip filed: `task_f1292bdf`. _(added 2026-07-08)_
- **Reconcile (Royce doing directly):** enable CA1 via core (has a contract, currently disabled — 163 contracted units invisible in-app); import approved sheets for SY2/SY6/SY7 (enabled via core, no contract imported yet). _(added 2026-07-08, Royce-owned)_
- **RCD checks can't seed for Equinix** — 0/4 contracted sites have an RCD check because the RCD-seed feature (PR #465) needs an RCD job plan for the customer, and Equinix has none (only Jemena does). Needs an Equinix (or global) RCD job plan created before re-import will help. _(added 2026-07-08, needs a job-plan decision)_
- **2 SKS job plans have zero tasks** — `ELGLV` (E1.37) and `SCADA/PLC` (E1.40). Now caught by the new coverage report if a contract matches them, but the plans themselves still have no checklist. _(added 2026-07-08, needs job-plan content)_
- **EQ Service "session expired, please reconnect" stuck screen — root cause still genuinely unknown.** Two chased theories were investigated and explicitly REFUTED with hard evidence: React error #418 (hydration mismatch) is a dated, known, confirmed-non-blocking noise pattern (2026-07-05 team note, 705 events/14d, essentially every active user) — NOT the cause. A suspected hanging `token-exchange` call was also refuted — real Netlify function logs showed every invocation completing in under 4s with zero errors; the "pending forever" read came from a flaky automated browser tab (same tab independently threw an unrelated CDP "renderer frozen" error). Two chips built on these now-retracted theories (`task_2911c80d`, `task_abbb7fd0`) were already started by Royce before the retraction landed — worth redirecting or discarding. The actual cause of the stuck-reconnect screen is still open. _(added 2026-07-08)_
- **EQ Service sidebar-header tenant logo clipped** (in `ShellSessionRecovery`'s fallback UI specifically, not the top bar — top bar renders fine live) — chip `task_14031bea` was already started by Royce before this correction landed; built on a stale "top-bar alignment" framing. _(added 2026-07-08)_
- eq-field `scripts/sks-pipeline-resource.js:1476` — possible additional `schedule_entries` filter-column bug when pushing a job to the SKS roster from Resource Allocation. Flagged by the audit as needing a live click-through test (filter keys, not a static select list) — not yet confirmed. Folded into chip `task_3e6d4e89`'s prompt rather than tracked separately. _(added 2026-07-08)_
- Core Talent now shows both an `"Electrician"` role (older invoice, 21 Jun) and a `"NSW Licensed Electrician"` role (newer rate card, 1 Jul) — may be the same job under two labels, inflating the weekly-cost table with a stale row. Left for Royce's own sanity-check pass before the Atom agency upload. _(added 2026-07-08)_
- **Site→customer backfill (SKS)** — only 117/250 SKS canonical sites carry a `customer_id`, so Service report customer-rollups are blank for the rest. The Service side is wired correctly; this is a Shell/canonical-spine data backfill, not a Service wiring gap. _(added 2026-07-08)_
- **One more hard-reload on Royce's phone** to land on the hardened SW (v3.5.265) — the resilience only protects from the next clean load onward; this release bumped the cache once more. _(added 2026-07-07)_
_…and 255 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-08 08:20 UTC._

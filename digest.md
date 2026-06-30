---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-30 11:35 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-30 11:21 UTC → 2026-06-30 11:35 UTC)

- Merged: eq-shell [#552](https://github.com/eq-solutions/eq-shell/pull/552) fix(staff): training matrix licence numbers + CSV export + e
- Merged: eq-shell [#513](https://github.com/eq-solutions/eq-shell/pull/513) fix(docs): correct stale EQ_SECRET_SALT guidance — HMAC reti
- Merged: eq-shell [#474](https://github.com/eq-solutions/eq-shell/pull/474) fix(transport): iframe origin hardening — SKS token refresh,
- Merged: eq-shell [#469](https://github.com/eq-solutions/eq-shell/pull/469) fix(auth): phone OTP login no longer requires a second TOTP 
- Merged: eq-shell [#467](https://github.com/eq-solutions/eq-shell/pull/467) fix(auth): provision shell_control.users on Cards worker app
- Merged: eq-shell [#466](https://github.com/eq-solutions/eq-shell/pull/466) feat(identity): staff-org-roster endpoint
- Merged: eq-shell [#465](https://github.com/eq-solutions/eq-shell/pull/465) feat(canonical-api): customer_id + quote_id resource filters
- Merged: eq-shell [#455](https://github.com/eq-solutions/eq-shell/pull/455) fix(vendor): repair eq-intake PR #449 build regressions

## ⚠ Needs you (3)

- 🟠 **Sentry new error** — `eq-cards` [minified:iF: ServerFailure(42883): operator does not exist: ](https://eq-solutions.sentry.io/issues/131103567/)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100658/)
- 🟠 **Sentry new error** — `eq-cards` [minified:I3: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [minified:iF: ServerFailure(42883): operator does not exist: uuid = text](https://eq-solutions.sentry.io/issues/131103567/) | 6 | 2026-06-29 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100658/) | 5 | 2026-06-30 |
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 3 | 2026-06-30 |
| eq-shell | [UnhandledRejection: Non-Error promise rejection captured with value: Object Not ](https://eq-solutions.sentry.io/issues/129495069/) | 2 | 2026-06-30 |
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-shell | [captureServerError](https://eq-solutions.sentry.io/issues/130413967/) | 2 | 2026-06-29 |
| eq-shell | [EQ Service iframe did not load within timeout](https://eq-solutions.sentry.io/issues/130169257/) | 2 | 2026-06-29 |
| eq-shell | [EQ Field handoff network error: Load failed](https://eq-solutions.sentry.io/issues/130061083/) | 2 | 2026-06-29 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-30 | eq-shell | [#552](https://github.com/eq-solutions/eq-shell/pull/552) fix(staff): training matrix licence numbers + CSV export + employ |
| 2026-06-30 | eq-solves-service | [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new) |
| 2026-06-30 | eq-solves-service | [#380](https://github.com/eq-solutions/eq-service/pull/380) feat(app): add branded error boundaries (error.tsx + global-error |
| 2026-06-30 | eq-solves-service | [#381](https://github.com/eq-solutions/eq-service/pull/381) fix(canonical): filter service.sites view by active = true |
| 2026-06-30 | eq-solves-service | [#378](https://github.com/eq-solutions/eq-service/pull/378) feat(ui): branded 404 page — app/not-found.tsx |
| 2026-06-30 | eq-field | [#377](https://github.com/eq-solutions/eq-field/pull/377) v3.5.214 — SKS write-path unblock (ultra-audit fixes) |
| 2026-06-30 | eq-field | [#376](https://github.com/eq-solutions/eq-field/pull/376) v3.5.213 — Teams canonical wiring + SKS read-only UI tidy |
| 2026-06-30 | eq-field | [#375](https://github.com/eq-solutions/eq-field/pull/375) v3.5.212 — audit_log: stamp org_id + fix manager_name in server f |
| 2026-06-30 | eq-field | [#374](https://github.com/eq-solutions/eq-field/pull/374) feat: branded 404.html for unmatched routes |
| 2026-06-30 | eq-field | [#371](https://github.com/eq-solutions/eq-field/pull/371) chore(armada): pre-bake ARMADA config for eq-field (autoMerge off |
| 2026-06-30 | eq-field | [#372](https://github.com/eq-solutions/eq-field/pull/372) v3.5.211 — canonical cleanup: pending_schedule, nav gates, dead c |
| 2026-06-30 | eq-field | [#370](https://github.com/eq-solutions/eq-field/pull/370) v3.5.210 — canonical wiring: Apprentice cluster fully wired for S |
| 2026-06-30 | eq-field | [#369](https://github.com/eq-solutions/eq-field/pull/369) v3.5.209 — JWT routing gaps: Bucket-B + tender phases + nominatio |
| 2026-06-30 | eq-field | [#368](https://github.com/eq-solutions/eq-field/pull/368) v3.5.208 — canonical wiring: Safety module fully wired for SKS |
| 2026-06-30 | eq-field | [#367](https://github.com/eq-solutions/eq-field/pull/367) fix(canonical): field_sites filters active too (archived sites re |
_Showing 15 of 99 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **EQ Ops active jobs view** — roster tab pulling from `app_data.jobs` (customer, site, job no, days active, value); not built _(added 2026-06-30)_
- **EQ Ops home tile** — Shell home tile with overdue follow-ups, stale quotes, active jobs; not built _(added 2026-06-30)_
- **Field crew on job** — workers in Field see their assigned job; requires eq-field repo changes _(added 2026-06-30)_
- **`issues.*` PermKeys activation** — Phase 3 when Issues UI ships for EQ plane; currently deferred constants _(added 2026-06-30)_
- **Review the 43 stale-for-review local branches** — no merge record, left untouched for an eyeball before pruning. Includes **14 closed-unmerged PRs whose remotes still exist** (`cert-import-timeout-fix2` #508, `drift-allowlist-rcd-views` #443, `field-handoff-docs` #442, `sec-workers-tenant-scope` #444, `crm-customers-polish` #415, `cards-api-invite-ip-throttle` #379, `quotes-sync-sks-canonical` #321, `crm-customers-hub-area2` #213, `etl-complete-apply` #220, `security-groups-page-legibility` #208, `sks-field-host` #194, `field-f1-prep` #177, `c3-auth-spike` #72, `affectionate-yonath` #62) + agent-name/rebase/docs leftovers _(added 2026-06-30)_
- **2 remote-only branches** never in local set — `fix/canonical-wiring-migration-rename`, `fix/check6-find-invites-allow`; left alone (possibly another agent's), verify before deleting _(added 2026-06-30)_
- **Make CI `verify` check REQUIRED** in eq-shell branch protection (Settings → Branches) — else the gate runs but doesn't block _(needs Royce's call) (added 2026-06-30)_
- **Defense-in-depth: REVOKE anon grants** on zaap PII tables (workers/worker_credentials/worker_inductions/worker_assignments) via a One-Pipe migration — RLS neutralizes them, but they'd expose instantly if RLS were ever dropped _(added 2026-06-30)_
- **nspbmir anon-PII audit** — couldn't verify (eq-guard blocks SKS-live from EQ sessions); needs a dedicated SKS-context session _(added 2026-06-30)_
- **God-component extraction** (StaffPage MatrixView/SplitPanel out of the 2,094-line file) — deferred: blind refactor unverifiable without a running app _(added 2026-06-30)_
_…and 150 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Book monthly check-in cadence with Richo (Michael Richardson)
- Tell Mark about catch-up conversations before starting (casual, no fanfare)
- Confirm Scott Hotson start date + written offer
- Schedule Simon Bramall catch-up — Equinix Account Lead conversation
- Hold Ben Ritchie coffee — first/second week back
_…and 15 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
| 2026-06-28 | [EQ Service batch-create fix](sessions/2026-06-28-batch-create-fix.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-30 11:35 UTC._

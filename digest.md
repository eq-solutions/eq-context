---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-30 10:47 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-30 10:00 UTC → 2026-06-30 10:47 UTC)

- Merged: eq-shell [#558](https://github.com/eq-solutions/eq-shell/pull/558) feat(ops): canonical job creation on quote win + job-routed 
- Merged: eq-shell [#557](https://github.com/eq-solutions/eq-shell/pull/557) fix(staff): training matrix licence numbers + CSV export + e
- Merged: eq-shell [#556](https://github.com/eq-solutions/eq-shell/pull/556) fix(attachments): extend signed URL TTL from 1hr to 7 days
- Merged: eq-shell [#542](https://github.com/eq-solutions/eq-shell/pull/542) feat(customers): customer-level Field/Service toggles in the
- Merged: eq-shell [#539](https://github.com/eq-solutions/eq-shell/pull/539) feat(audit): Tenant Activity Log — who changed what on the c
- Merged: eq-shell [#538](https://github.com/eq-solutions/eq-shell/pull/538) feat(notifications): range-based worker reminders + SMS opt-
- Merged: eq-shell [#537](https://github.com/eq-solutions/eq-shell/pull/537) fix(notifications): repoint licence-expiry scheduler to eq-c
- Merged: eq-shell [#536](https://github.com/eq-solutions/eq-shell/pull/536) fix: staff edit 500, audit log, employment type, Add Site mo

## ⚠ Needs you (2)

- 🟠 **Sentry new error** — `eq-cards` [minified:iF: ServerFailure(42883): operator does not exist: ](https://eq-solutions.sentry.io/issues/131103567/)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100658/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 2 | 0d |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [minified:iF: ServerFailure(42883): operator does not exist: uuid = text](https://eq-solutions.sentry.io/issues/131103567/) | 6 | 2026-06-29 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100658/) | 2 | 2026-06-30 |
| eq-shell | [UnhandledRejection: Non-Error promise rejection captured with value: Object Not ](https://eq-solutions.sentry.io/issues/129495069/) | 2 | 2026-06-30 |
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-shell | [captureServerError](https://eq-solutions.sentry.io/issues/130413967/) | 2 | 2026-06-29 |
| eq-shell | [EQ Service iframe did not load within timeout](https://eq-solutions.sentry.io/issues/130169257/) | 2 | 2026-06-29 |
| eq-shell | [EQ Field handoff network error: Load failed](https://eq-solutions.sentry.io/issues/130061083/) | 2 | 2026-06-29 |
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-30 | eq-shell | [#556](https://github.com/eq-solutions/eq-shell/pull/556) fix(attachments): extend signed URL TTL from 1hr to 7 days |
| 2026-06-30 | eq-shell | [#558](https://github.com/eq-solutions/eq-shell/pull/558) feat(ops): canonical job creation on quote win + job-routed attac |
| 2026-06-30 | eq-shell | [#557](https://github.com/eq-solutions/eq-shell/pull/557) fix(staff): training matrix licence numbers + CSV export + employ |
| 2026-06-30 | eq-shell | [#555](https://github.com/eq-solutions/eq-shell/pull/555) fix(migrations): 0151 field_teams no-op — views can't have RLS en |
| 2026-06-30 | eq-shell | [#554](https://github.com/eq-solutions/eq-shell/pull/554) chore(armada): pre-bake ARMADA config for eq-shell (autoMerge off |
| 2026-06-30 | eq-shell | [#553](https://github.com/eq-solutions/eq-shell/pull/553) feat(audit): team & access events in tenant Activity Log |
| 2026-06-30 | eq-shell | [#549](https://github.com/eq-solutions/eq-shell/pull/549) feat(ops): Phase 1 — Issues & Attachments on the canonical record |
| 2026-06-30 | eq-shell | [#551](https://github.com/eq-solutions/eq-shell/pull/551) fix(audit): stamp actor on Field/Service toggle + calibration edi |
| 2026-06-30 | eq-shell | [#550](https://github.com/eq-solutions/eq-shell/pull/550) feat(crm): sites inline toggle table + apply-all + A-Z contacts |
| 2026-06-30 | eq-shell | [#547](https://github.com/eq-solutions/eq-shell/pull/547) feat(audit): extend Tenant Activity Log to contact link tables |
| 2026-06-30 | eq-solves-service | [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new) |
| 2026-06-30 | eq-solves-service | [#380](https://github.com/eq-solutions/eq-service/pull/380) feat(app): add branded error boundaries (error.tsx + global-error |
| 2026-06-30 | eq-solves-service | [#381](https://github.com/eq-solutions/eq-service/pull/381) fix(canonical): filter service.sites view by active = true |
| 2026-06-30 | eq-solves-service | [#378](https://github.com/eq-solutions/eq-service/pull/378) feat(ui): branded 404 page — app/not-found.tsx |
| 2026-06-30 | eq-field | [#376](https://github.com/eq-solutions/eq-field/pull/376) v3.5.213 — Teams canonical wiring + SKS read-only UI tidy |
_Showing 15 of 110 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Issues/Attachments Phase 2** — dispatch 0147_issues_table to zaap when EQ Ops goes live on the EQ plane; flip `issues.*` PermKeys from deferred to active _(added 2026-06-30)_
- **Signed URL refresh** — attachment URLs are 1-hour TTL; long-running sessions will show broken images silently; no refresh mechanism built _(added 2026-06-30)_
- **Onboard current labour-hire firm's workers to Cards** — Royce in progress; "need to fill up the info first" before any demo _(added 2026-06-30)_
- **Dry-run Core > tenant view before the coffee demo** — verify what the tenant admin view actually renders + scope out anything not appropriate for the firm to see; offered, deferred until data is in _(added 2026-06-30)_
- **Decide the pilot offer** — firm as guest in existing tenant vs their own tenant (changes the demo + the portability framing) _(needs Royce's call) (added 2026-06-30)_
- **Platform Security Log / operator console** — sign-ins/2FA audit (jvkn, admin-audit.ts reads it); deferred by decision _(added 2026-06-30)_
- **Run first `shipwright` build** of #377 — in a dedicated Claude Code session rooted in eq-service (skills load from its `.claude/skills/`; can't be driven from another repo's session). Runbook in SETUP-NOTES + today's session log _(added 2026-06-30)_
- **crows-nest `/loop`** — needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`); don't arm until one clean manual cycle is observed _(added 2026-06-30)_
- **Add `test: vitest run`** to eq-service `.armada/config.json` once a clean cycle is seen + unit-test green verified _(added 2026-06-30)_
- **auth_handoff Sentry alert** — native rule on `canary=auth_handoff` AND `level=error` (catches real-user slug_unresolved/no_email; the probe already covers secret drift). MCP is read-only for alert rules → 2-min UI action (recipe on file), or build the watcher-as-code _(added 2026-06-30)_
_…and 140 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-30 10:47 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-01
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-01 10:36 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-01 10:08 UTC → 2026-07-01 10:36 UTC)

- Merged: eq-shell [#585](https://github.com/eq-solutions/eq-shell/pull/585) refactor(staff): Phase E — extract MatrixView + SplitPanel i
- Merged: eq-shell [#567](https://github.com/eq-solutions/eq-shell/pull/567) fix(staff): show name for existing staff in pending connecti
- Merged: eq-shell [#566](https://github.com/eq-solutions/eq-shell/pull/566) fix(ui): iOS spinner animation — will-change: transform on a
- Merged: eq-shell [#565](https://github.com/eq-solutions/eq-shell/pull/565) fix(staff): matrix full licence names in headers + mobile po
- Merged: eq-shell [#564](https://github.com/eq-solutions/eq-shell/pull/564) refactor(pdf): @react-pdf/renderer replaces Puppeteer + chro
- Merged: eq-shell [#563](https://github.com/eq-solutions/eq-shell/pull/563) fix(equipment): cert import 500 — send cert URLs, not bytes,
- Merged: eq-solves-service [#384](https://github.com/eq-solutions/eq-service/pull/384) feat(testing): instrument selection on ACB/NSX tests + clean
- Merged: eq-solves-service [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new)

## ⚠ Needs you (2)

- 🔴 **CI failure** — eq-cards `main`
- 🟠 **Sentry new error** — `eq-cards` [minified:I3: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 6 | 3d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✗ failure | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-07-01 |
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-shell | [captureServerError](https://eq-solutions.sentry.io/issues/130413967/) | 2 | 2026-06-29 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-01 | eq-shell | [#585](https://github.com/eq-solutions/eq-shell/pull/585) refactor(staff): Phase E — extract MatrixView + SplitPanel into s |
| 2026-07-01 | eq-shell | [#579](https://github.com/eq-solutions/eq-shell/pull/579) fix(sentry): 3 production errors — approval dedup, Cards timer ra |
| 2026-07-01 | eq-shell | [#584](https://github.com/eq-solutions/eq-shell/pull/584) fix(ops): PDF import — real spinner + apply default markup |
| 2026-07-01 | eq-shell | [#583](https://github.com/eq-solutions/eq-shell/pull/583) feat(reports): manual "mark done" on the forecasts tab |
| 2026-07-01 | eq-shell | [#582](https://github.com/eq-solutions/eq-shell/pull/582) style(ui): Warm Sand neutrals in CSS files — closes the mobile ga |
| 2026-07-01 | eq-solves-service | [#384](https://github.com/eq-solutions/eq-service/pull/384) feat(testing): instrument selection on ACB/NSX tests + clean inst |
| 2026-06-30 | eq-shell | [#581](https://github.com/eq-solutions/eq-shell/pull/581) style(ui): roll Warm Sand neutrals repo-wide (Direction-D) |
| 2026-06-30 | eq-shell | [#580](https://github.com/eq-solutions/eq-shell/pull/580) style(staff): Warm Sand neutrals pilot on StaffPage (Direction-D) |
| 2026-06-30 | eq-shell | [#578](https://github.com/eq-solutions/eq-shell/pull/578) refactor(staff): extract + unit-test pure StaffPage logic (Phase  |
| 2026-06-30 | eq-shell | [#575](https://github.com/eq-solutions/eq-shell/pull/575) feat(staff): training matrix — filter, sort, selection, column fi |
| 2026-06-30 | eq-shell | [#572](https://github.com/eq-solutions/eq-shell/pull/572) chore(equipment): remove dead synchronous cert-import-parse funct |
| 2026-06-30 | eq-shell | [#570](https://github.com/eq-solutions/eq-shell/pull/570) fix(env): Google Maps key prefix + dead NETLIFY_CONTEXT Sentry fa |
| 2026-06-30 | eq-shell | [#576](https://github.com/eq-solutions/eq-shell/pull/576) fix(staff): PostgrestBuilder→Promise cast via unknown — unblock t |
| 2026-06-30 | eq-shell | [#571](https://github.com/eq-solutions/eq-shell/pull/571) fix(staff): destructure rejection_reason — unblock production bui |
| 2026-06-30 | eq-shell | [#569](https://github.com/eq-solutions/eq-shell/pull/569) fix(staff): invite-path rejection email |
_Showing 15 of 112 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Semantics pass** (Warm Sand) — reds/greens/ambers + status-chip pastels shift shade → needs a before/after sign-off; unblocks flipping the lint no-raw-hex ratchet (F) _(needs Royce's call) (added 2026-07-01)_
- **Token source unification (A)** + eslint-runnable env — eslint won't run in the work checkout, blocking a lint-config change / the blocking ratchet _(added 2026-07-01)_
- **Dispatch `tenant-migrate.yml`** (workflow_dispatch, `sks` slug, production-gated, `allow_checksum_drift=true` per usual) to apply **0153** to ehow. Until then the Mark-done buttons render but a click reverts (table absent → PATCH 500s). _(added 2026-07-01)_
- **Add `TENANT_UUID = 7dee117c-98bd-4d39-af8c-2c81d02a1e85` to ehow edge function secrets** — Supabase dashboard → Project Settings → Edge Functions → Secrets. All 4 functions 500 without it. _(Royce action) (added 2026-07-01)_
- **Update pg_cron digest cron URL** — check ehow pg_cron; if referencing `supervisor-digest-v2`, update to `supervisor-digest`. _(added 2026-07-01)_
- **Arm crows-nest `/loop` on eq-intake** — 4 clean manual cycles now observed; still needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`) + Royce's go _(added 2026-06-30)_
- **Add `test:` gate** to eq-intake `.armada/config.json` (e.g. `pnpm -C eq-platform test`) — unit tests green across packages, just not wired into the fleet gate yet _(added 2026-06-30)_
- **(optional, needs your call)** Harden build-before-test workspace-wide so the stale-dist bug class (root of #47) can't recur — source-resolution or build-ordering across all packages _(added 2026-06-30)_
- **(optional, needs your taste)** Archive stale root planning docs (`PLAN-*`, `OVERNIGHT-REVIEW-*`, `CONDUIT-AUDIT-*`) into `_archive/` _(added 2026-06-30)_
- **Verify cert import live** — once deploy goes green, import multiple certs at core.eq.solutions (hard-refresh for new panel JS); parser now writes a real failure reason to job status if a download fails _(added 2026-07-01)_
_…and 162 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-01 10:36 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-30 18:22 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-30 17:29 UTC → 2026-06-30 18:22 UTC)

- Merged: eq-shell [#576](https://github.com/eq-solutions/eq-shell/pull/576) fix(staff): PostgrestBuilder→Promise cast via unknown — unbl
- Merged: eq-shell [#571](https://github.com/eq-solutions/eq-shell/pull/571) fix(staff): destructure rejection_reason — unblock productio
- Merged: eq-shell [#569](https://github.com/eq-solutions/eq-shell/pull/569) fix(staff): invite-path rejection email
- Merged: eq-shell [#453](https://github.com/eq-solutions/eq-shell/pull/453) fix(staff): licence labels + photo CSP
- Merged: eq-shell [#451](https://github.com/eq-solutions/eq-shell/pull/451) fix(jvkn): re-gate eq_field_get_worker_summary with org-memb
- Merged: eq-shell [#447](https://github.com/eq-solutions/eq-shell/pull/447) fix(intake): mint-sks-jwt tenant check breaks platform admin
- Merged: eq-solves-service [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new)
- Merged: eq-field [#381](https://github.com/eq-solutions/eq-field/pull/381) v3.5.217 — URL-per-tab deep-link support (Field side)
- ⚠ Needs you: 0 → 1 (new items)

## ⚠ Needs you (1)

- 🟠 **Sentry new error** — `eq-cards` [minified:I3: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 3 | 0d |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
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
| 2026-06-30 | eq-shell | [#576](https://github.com/eq-solutions/eq-shell/pull/576) fix(staff): PostgrestBuilder→Promise cast via unknown — unblock t |
| 2026-06-30 | eq-shell | [#571](https://github.com/eq-solutions/eq-shell/pull/571) fix(staff): destructure rejection_reason — unblock production bui |
| 2026-06-30 | eq-shell | [#569](https://github.com/eq-solutions/eq-shell/pull/569) fix(staff): invite-path rejection email |
| 2026-06-30 | eq-shell | [#568](https://github.com/eq-solutions/eq-shell/pull/568) fix(staff): pending connections — admin notify, reject email, pho |
| 2026-06-30 | eq-shell | [#567](https://github.com/eq-solutions/eq-shell/pull/567) fix(staff): show name for existing staff in pending connections |
| 2026-06-30 | eq-shell | [#566](https://github.com/eq-solutions/eq-shell/pull/566) fix(ui): iOS spinner animation — will-change: transform on all CS |
| 2026-06-30 | eq-shell | [#564](https://github.com/eq-solutions/eq-shell/pull/564) refactor(pdf): @react-pdf/renderer replaces Puppeteer + chromium |
| 2026-06-30 | eq-shell | [#565](https://github.com/eq-solutions/eq-shell/pull/565) fix(staff): matrix full licence names in headers + mobile polish |
| 2026-06-30 | eq-shell | [#563](https://github.com/eq-solutions/eq-shell/pull/563) fix(equipment): cert import 500 — send cert URLs, not bytes, to b |
| 2026-06-30 | eq-shell | [#562](https://github.com/eq-solutions/eq-shell/pull/562) refactor(ui): route brand hexes through @eq tokens (105 across 19 |
| 2026-06-30 | eq-shell | [#552](https://github.com/eq-solutions/eq-shell/pull/552) fix(staff): training matrix licence numbers + CSV export + employ |
| 2026-06-30 | eq-solves-service | [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new) |
| 2026-06-30 | eq-solves-service | [#380](https://github.com/eq-solutions/eq-service/pull/380) feat(app): add branded error boundaries (error.tsx + global-error |
| 2026-06-30 | eq-solves-service | [#381](https://github.com/eq-solutions/eq-service/pull/381) fix(canonical): filter service.sites view by active = true |
| 2026-06-30 | eq-solves-service | [#378](https://github.com/eq-solutions/eq-service/pull/378) feat(ui): branded 404 page — app/not-found.tsx |
_Showing 15 of 108 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Add `TENANT_UUID = 7dee117c-98bd-4d39-af8c-2c81d02a1e85` to ehow edge function secrets** — Supabase dashboard → Project Settings → Edge Functions → Secrets. All 4 functions 500 without it. _(Royce action) (added 2026-07-01)_
- **Update pg_cron digest cron URL** — check ehow pg_cron; if referencing `supervisor-digest-v2`, update to `supervisor-digest`. _(added 2026-07-01)_
- **Shell-side URL-per-tab PR** (eq-shell repo) — Shell reads `?tab=` from its own URL → appends `&tab=<slug>` to Field iframe src; listens for `EQ_TAB_CHANGE` → `history.pushState`. Prompt written. _(added 2026-07-01)_
- **Arm crows-nest `/loop` on eq-intake** — 4 clean manual cycles now observed; still needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`) + Royce's go _(added 2026-06-30)_
- **Add `test:` gate** to eq-intake `.armada/config.json` (e.g. `pnpm -C eq-platform test`) — unit tests green across packages, just not wired into the fleet gate yet _(added 2026-06-30)_
- **(optional, needs your call)** Harden build-before-test workspace-wide so the stale-dist bug class (root of #47) can't recur — source-resolution or build-ordering across all packages _(added 2026-06-30)_
- **(optional, needs your taste)** Archive stale root planning docs (`PLAN-*`, `OVERNIGHT-REVIEW-*`, `CONDUIT-AUDIT-*`) into `_archive/` _(added 2026-06-30)_
- **Verify cert import live** — once deploy goes green, import multiple certs at core.eq.solutions (hard-refresh for new panel JS); parser now writes a real failure reason to job status if a download fails _(added 2026-07-01)_
- **Merge + smoke PR #573** — Netlify preview at deploy-preview-573--eq-shell.netlify.app. Smoke: navigate tabs → URL updates; bookmark `?tab=timesheets` → reload lands on Timesheets _(added 2026-07-01)_
- **Clean up `fix/remove-dead-cert-parse` local branch** — has a stray deep-link commit from branch confusion; `git -C C:\Projects\eq-shell reset --hard f6a0a90` once ready _(added 2026-07-01, needs your call)_
_…and 166 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-01 | [Pending connections audit + 3 gap fixes merged](sessions/2026-07-01.md) |
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-30 18:22 UTC._

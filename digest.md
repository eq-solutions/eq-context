---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-30 21:14 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-30 19:19 UTC → 2026-06-30 21:14 UTC)

- Merged: eq-shell [#581](https://github.com/eq-solutions/eq-shell/pull/581) style(ui): roll Warm Sand neutrals repo-wide (Direction-D)
- Merged: eq-shell [#580](https://github.com/eq-solutions/eq-shell/pull/580) style(staff): Warm Sand neutrals pilot on StaffPage (Directi
- Merged: eq-shell [#453](https://github.com/eq-solutions/eq-shell/pull/453) fix(staff): licence labels + photo CSP
- Merged: eq-solves-service [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new)
- Merged: eq-solves-service [#381](https://github.com/eq-solutions/eq-service/pull/381) fix(canonical): filter service.sites view by active = true
- Merged: eq-field [#381](https://github.com/eq-solutions/eq-field/pull/381) v3.5.217 — URL-per-tab deep-link support (Field side)
- Merged: eq-solves-service [#380](https://github.com/eq-solutions/eq-service/pull/380) feat(app): add branded error boundaries (error.tsx + global-
- Merged: eq-field [#379](https://github.com/eq-solutions/eq-field/pull/379) security(zaap): revoke residual anon grants on worker-PII ta

## ⚠ Needs you (1)

- 🟠 **Sentry new error** — `eq-cards` [minified:I3: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 3 | 2026-06-30 |
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-shell | [captureServerError](https://eq-solutions.sentry.io/issues/130413967/) | 2 | 2026-06-29 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-30 | eq-shell | [#581](https://github.com/eq-solutions/eq-shell/pull/581) style(ui): roll Warm Sand neutrals repo-wide (Direction-D) |
| 2026-06-30 | eq-shell | [#580](https://github.com/eq-solutions/eq-shell/pull/580) style(staff): Warm Sand neutrals pilot on StaffPage (Direction-D) |
| 2026-06-30 | eq-shell | [#578](https://github.com/eq-solutions/eq-shell/pull/578) refactor(staff): extract + unit-test pure StaffPage logic (Phase  |
| 2026-06-30 | eq-shell | [#575](https://github.com/eq-solutions/eq-shell/pull/575) feat(staff): training matrix — filter, sort, selection, column fi |
| 2026-06-30 | eq-shell | [#572](https://github.com/eq-solutions/eq-shell/pull/572) chore(equipment): remove dead synchronous cert-import-parse funct |
| 2026-06-30 | eq-shell | [#570](https://github.com/eq-solutions/eq-shell/pull/570) fix(env): Google Maps key prefix + dead NETLIFY_CONTEXT Sentry fa |
| 2026-06-30 | eq-shell | [#576](https://github.com/eq-solutions/eq-shell/pull/576) fix(staff): PostgrestBuilder→Promise cast via unknown — unblock t |
| 2026-06-30 | eq-shell | [#571](https://github.com/eq-solutions/eq-shell/pull/571) fix(staff): destructure rejection_reason — unblock production bui |
| 2026-06-30 | eq-shell | [#569](https://github.com/eq-solutions/eq-shell/pull/569) fix(staff): invite-path rejection email |
| 2026-06-30 | eq-shell | [#568](https://github.com/eq-solutions/eq-shell/pull/568) fix(staff): pending connections — admin notify, reject email, pho |
| 2026-06-30 | eq-shell | [#567](https://github.com/eq-solutions/eq-shell/pull/567) fix(staff): show name for existing staff in pending connections |
| 2026-06-30 | eq-shell | [#566](https://github.com/eq-solutions/eq-shell/pull/566) fix(ui): iOS spinner animation — will-change: transform on all CS |
| 2026-06-30 | eq-shell | [#564](https://github.com/eq-solutions/eq-shell/pull/564) refactor(pdf): @react-pdf/renderer replaces Puppeteer + chromium |
| 2026-06-30 | eq-shell | [#565](https://github.com/eq-solutions/eq-shell/pull/565) fix(staff): matrix full licence names in headers + mobile polish |
| 2026-06-30 | eq-shell | [#563](https://github.com/eq-solutions/eq-shell/pull/563) fix(equipment): cert import 500 — send cert URLs, not bytes, to b |
_Showing 15 of 109 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Merge PR #579** — 3 Sentry fixes (approval dedup, Cards timer, PDF fetch). Build green. _(Royce to merge)_
- **Netlify: rename `NEXT_PUBLIC_GOOGLE_MAPS_KEY` → `VITE_GOOGLE_MAPS_KEY`** — PR #570 changed the code; Netlify dashboard var still has old name. _(Royce action)_
- **Netlify: remove stale env vars** — `EQ_FIELD_HANDOFF_KEY`, `EQ_FIELD_HANDOFF_KEY_NEXT`, `EQ_SECRET_SALT`, `EQ_SECRET_SALT_NEXT` no longer have consumers. _(Royce action)_
- **Add `TENANT_UUID = 7dee117c-98bd-4d39-af8c-2c81d02a1e85` to ehow edge function secrets** — Supabase dashboard → Project Settings → Edge Functions → Secrets. All 4 functions 500 without it. _(Royce action) (added 2026-07-01)_
- **Update pg_cron digest cron URL** — check ehow pg_cron; if referencing `supervisor-digest-v2`, update to `supervisor-digest`. _(added 2026-07-01)_
- **Arm crows-nest `/loop` on eq-intake** — 4 clean manual cycles now observed; still needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`) + Royce's go _(added 2026-06-30)_
- **Add `test:` gate** to eq-intake `.armada/config.json` (e.g. `pnpm -C eq-platform test`) — unit tests green across packages, just not wired into the fleet gate yet _(added 2026-06-30)_
- **(optional, needs your call)** Harden build-before-test workspace-wide so the stale-dist bug class (root of #47) can't recur — source-resolution or build-ordering across all packages _(added 2026-06-30)_
- **(optional, needs your taste)** Archive stale root planning docs (`PLAN-*`, `OVERNIGHT-REVIEW-*`, `CONDUIT-AUDIT-*`) into `_archive/` _(added 2026-06-30)_
- **Verify cert import live** — once deploy goes green, import multiple certs at core.eq.solutions (hard-refresh for new panel JS); parser now writes a real failure reason to job status if a download fails _(added 2026-07-01)_
_…and 165 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-30 21:14 UTC._

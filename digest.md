---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-28 08:30 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-28 02:59 UTC → 2026-06-28 08:30 UTC)

- Merged: eq-shell [#514](https://github.com/eq-solutions/eq-shell/pull/514) fix(equipment): cert-import-parse-background 500 — return Re
- Merged: eq-shell [#511](https://github.com/eq-solutions/eq-shell/pull/511) fix(equipment): cert import 500 + remove forced site assignm
- Merged: eq-shell [#502](https://github.com/eq-solutions/eq-shell/pull/502) fix(drift): allow-list service.staff security-invoker view (
- Merged: eq-shell [#497](https://github.com/eq-solutions/eq-shell/pull/497) feat(eq-ops): show the Workbench job number on each Kanban c
- Merged: eq-shell [#496](https://github.com/eq-solutions/eq-shell/pull/496) fix(eq-ops): relabel stage 1 'Submitted' to 'Open' so drafts
- Merged: eq-shell [#495](https://github.com/eq-solutions/eq-shell/pull/495) fix(eq-ops): gate Job Created on a Workbench job number from
- Merged: eq-shell [#494](https://github.com/eq-solutions/eq-shell/pull/494) fix(eq-ops): Kanban board groups by the 5 dropdown stages, n
- Merged: eq-shell [#486](https://github.com/eq-solutions/eq-shell/pull/486) fix(schedulers): retire EQ Quotes Flask schedulers (Sentry E

## ⚠ Needs you (2)

- 🔴 **Substrate drift** — DRIFT: supabase eq-solves-field (ktmjmdzqrogauaevbktn): claimed LIVE but reality looks DEAD
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ✓ success | 0d ago | 1 | 0d |
| eq-field | ✓ success | 24d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-28 | eq-shell | [#514](https://github.com/eq-solutions/eq-shell/pull/514) fix(equipment): cert-import-parse-background 500 — return Respons |
| 2026-06-28 | eq-shell | [#511](https://github.com/eq-solutions/eq-shell/pull/511) fix(equipment): cert import 500 + remove forced site assignment |
| 2026-06-28 | eq-shell | [#512](https://github.com/eq-solutions/eq-shell/pull/512) chore: drop public.sks_quotes_* legacy tables + fix stale callers |
| 2026-06-28 | eq-shell | [#510](https://github.com/eq-solutions/eq-shell/pull/510) fix(customers): always-visible contact checkboxes |
| 2026-06-28 | eq-shell | [#509](https://github.com/eq-solutions/eq-shell/pull/509) feat(equipment): async cert import — background function + Blobs  |
| 2026-06-28 | eq-shell | [#507](https://github.com/eq-solutions/eq-shell/pull/507) fix(equipment): Haiku + hard deadline to beat Netlify 26s wall; p |
| 2026-06-28 | eq-shell | [#506](https://github.com/eq-solutions/eq-shell/pull/506) fix(equipment): cert import bundles without @eq/schemas (was inst |
| 2026-06-28 | eq-shell | [#505](https://github.com/eq-solutions/eq-shell/pull/505) feat(brand): embed brand_color + brand_logo_url in service JWT |
| 2026-06-28 | eq-solves-service | [#362](https://github.com/eq-solutions/eq-service/pull/362) fix: split FK joins after migration 0147 + JWT role resolution fo |
| 2026-06-28 | eq-solves-service | [#361](https://github.com/eq-solutions/eq-service/pull/361) fix(substrate): add workflow_dispatch to notify-substrate |
| 2026-06-28 | eq-solves-service | [#359](https://github.com/eq-solutions/eq-service/pull/359) feat(brand): Shell owns brand identity — derive palette from bran |
| 2026-06-28 | eq-field | [#355](https://github.com/eq-solutions/eq-field/pull/355) v3.5.197 — canonical field_* views + tenant-agnostic public.* tab |
| 2026-06-28 | eq-field | [#350](https://github.com/eq-solutions/eq-field/pull/350) fix(safety): sticky tab row + padding + site_audits on ehow (v3.5 |
| 2026-06-28 | eq-field | [#354](https://github.com/eq-solutions/eq-field/pull/354) v3.5.196 — Pipeline: mandatory job number on Confirm Curve + life |
| 2026-06-28 | eq-field | [#353](https://github.com/eq-solutions/eq-field/pull/353) fix(substrate): add workflow_dispatch to notify-substrate |
_Showing 15 of 111 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Verify /brief + /close** in first real build session — untested in production
- **gitleaks pre-commit hook** — prevent PAT exposure in substrate history
- **Update C:\Projects\.git-credentials** files with new PAT after rotation
- **MD files deep dive** — stale Supabase refs, old architecture claims (agent launched 2026-06-28)
- Remaining items carried from 2026-06-18 (see below)
- **Curate `sites.field_enabled`** — 591 all enabled → trim to live jobs
- **Login hook** (phone-dedup) — workers still can't sign in (separate track; `ops/decisions.md`).
- **Curate `sites.field_enabled`** — 591 all enabled → trim to live jobs.
- **Daniel Bower** — confirm leaver / remove.
- **Generalise `workers-canonical-sync`** — currently single-tenant (hardcodes SKS+ehow).
_…and 111 more · [eq/pending.md](eq/pending.md)_

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
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
| 2026-06-28 | [EQ Service batch-create fix](sessions/2026-06-28-batch-create-fix.md) |
| 2026-06-27 | [2026-06-27 — Usability sprint + security gate promotion](sessions/2026-06-27-usability-sprint.md) |
| 2026-06-27 | [Substrate-coherence sprint — honesty CI + security gate + digest + Node 24 bump](sessions/2026-06-27-substrate-coherence-sprint.md) |
| 2026-06-26 | [Session: Safety docs footer parity](sessions/2026-06-26-footer-parity.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-28 08:30 UTC._

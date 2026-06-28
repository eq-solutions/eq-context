---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-28 10:24 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-28 09:16 UTC → 2026-06-28 10:24 UTC)

- Merged: eq-shell [#517](https://github.com/eq-solutions/eq-shell/pull/517) feat(crm): site Maps link + Places autocomplete (key-gated)
- Merged: eq-shell [#504](https://github.com/eq-solutions/eq-shell/pull/504) fix(equipment): surface the real cert-import error (no more 
- Merged: eq-shell [#503](https://github.com/eq-solutions/eq-shell/pull/503) feat(crm): entityCapabilities policy map (archive/delete/mer
- Merged: eq-shell [#501](https://github.com/eq-solutions/eq-shell/pull/501) feat(substrate): notify eq-context on push to main
- Merged: eq-shell [#500](https://github.com/eq-solutions/eq-shell/pull/500) fix(eq-ops): make the stage tabs filter the board (were iner
- Merged: eq-shell [#498](https://github.com/eq-solutions/eq-shell/pull/498) feat(crm): contact-site assignment + inline delete for sites
- Merged: eq-shell [#493](https://github.com/eq-solutions/eq-shell/pull/493) feat(staff): push worker profile updates to tenant staff row
- Merged: eq-shell [#492](https://github.com/eq-solutions/eq-shell/pull/492) feat(perf): React Query for AccessControlPage + EntityBrowse

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
| 2026-06-28 | eq-shell | [#517](https://github.com/eq-solutions/eq-shell/pull/517) feat(crm): site Maps link + Places autocomplete (key-gated) |
| 2026-06-28 | eq-shell | [#516](https://github.com/eq-solutions/eq-shell/pull/516) fix(staff): approval 500 + subcontractor role + audit hardening |
| 2026-06-28 | eq-shell | [#515](https://github.com/eq-solutions/eq-shell/pull/515) feat(crm): site address + contact picker |
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
_Showing 15 of 112 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Verify /brief + /close** in first real build session — just confirmed they appear in `/` menu
- **gitleaks pre-commit hook** — prevent PAT exposure in substrate history
- **Update C:\Projects\.git-credentials** files with new PAT after rotation
- **Merge eq-service #363 + eq-shell #513** — docs-only PRs, safe to merge any time
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-28 10:24 UTC._

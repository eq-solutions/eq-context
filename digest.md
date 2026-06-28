---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-28 00:18 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## ⚠ Needs you (1)

- 🔴 **CI failure** — eq-cards `main`

## Pulse

| Repo | CI (main) | Open PRs | Oldest |
|------|-----------|----------|--------|
| eq-shell | ✓ success | 0 | — |
| eq-solves-service | ✓ success | 1 | — |
| eq-field | ✓ success | 1 | 0d |
| eq-cards | ✗ failure | 0 | — |
| eq-solves-intake | ? unknown | 0 | — |

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-28 | eq-shell | [#505](https://github.com/eq-solutions/eq-shell/pull/505) feat(brand): embed brand_color + brand_logo_url in service JWT |
| 2026-06-28 | eq-solves-service | [#359](https://github.com/eq-solutions/eq-service/pull/359) feat(brand): Shell owns brand identity — derive palette from bran |
| 2026-06-27 | eq-shell | [#503](https://github.com/eq-solutions/eq-shell/pull/503) feat(crm): entityCapabilities policy map (archive/delete/merge pe |
| 2026-06-27 | eq-shell | [#504](https://github.com/eq-solutions/eq-shell/pull/504) fix(equipment): surface the real cert-import error (no more opaqu |
| 2026-06-27 | eq-shell | [#501](https://github.com/eq-solutions/eq-shell/pull/501) feat(substrate): notify eq-context on push to main |
| 2026-06-27 | eq-shell | [#500](https://github.com/eq-solutions/eq-shell/pull/500) fix(eq-ops): make the stage tabs filter the board (were inert in  |
| 2026-06-27 | eq-shell | [#502](https://github.com/eq-solutions/eq-shell/pull/502) fix(drift): allow-list service.staff security-invoker view (ehow) |
| 2026-06-27 | eq-shell | [#498](https://github.com/eq-solutions/eq-shell/pull/498) feat(crm): contact-site assignment + inline delete for sites and  |
| 2026-06-27 | eq-shell | [#497](https://github.com/eq-solutions/eq-shell/pull/497) feat(eq-ops): show the Workbench job number on each Kanban card |
| 2026-06-27 | eq-shell | [#496](https://github.com/eq-solutions/eq-shell/pull/496) fix(eq-ops): relabel stage 1 'Submitted' to 'Open' so drafts read |
| 2026-06-27 | eq-shell | [#495](https://github.com/eq-solutions/eq-shell/pull/495) fix(eq-ops): gate Job Created on a Workbench job number from boar |
| 2026-06-27 | eq-shell | [#494](https://github.com/eq-solutions/eq-shell/pull/494) fix(eq-ops): Kanban board groups by the 5 dropdown stages, not 10 |
| 2026-06-27 | eq-shell | [#493](https://github.com/eq-solutions/eq-shell/pull/493) feat(staff): push worker profile updates to tenant staff rows on  |
| 2026-06-27 | eq-shell | [#492](https://github.com/eq-solutions/eq-shell/pull/492) feat(perf): React Query for AccessControlPage + EntityBrowserPage |
| 2026-06-27 | eq-shell | [#491](https://github.com/eq-solutions/eq-shell/pull/491) feat(perf): React Query for StaffPage — roster, pending, licences |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- Remaining items carried from 2026-06-18 (see below)
- **Curate `sites.field_enabled`** — 591 all enabled → trim to live jobs
- **Login hook** (phone-dedup) — workers still can't sign in (separate track; `ops/decisions.md`).
- **Curate `sites.field_enabled`** — 591 all enabled → trim to live jobs.
- **Daniel Bower** — confirm leaver / remove.
- **Generalise `workers-canonical-sync`** — currently single-tenant (hardcodes SKS+ehow).
- People profile enrichment from ehow — when Field loads a person with worker_id, optionally pre-fill from ehow.app_data.staff. Requires reading ehow via staff map (already loaded by leave adapter). Next meaningful sprint.
- `ZAAP_JWT_SECRET=""` — EQ tenant JWT broken (acceptable while zaap unpopulated).
- `APP_ORIGIN` env var stale (`eq-solves-field.netlify.app` → should be `field.eq.solutions`).
- v3.5.147 create-stub path to be removed when Cards onboarding goes live as the sole jvkn.workers creator.
_…and 117 more · [eq/pending.md](eq/pending.md)_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-28 00:18 UTC._

# Session 2026-06-28 — EQ Service batch-create fix

**Repo:** eq-solves-service  
**Branch:** main  
**Commits:** d124ac5

---

## What was done

### Memory consolidation (context continuation)
- Fixed 5 stale entries across 4 memory files:
  - `project_plan_b_auth_complete.md` — updated PR #346/#347 status to MERGED
  - `project_rls_and_action_security_hardening.md` — removed stale urjh references
  - `project_ehow_service_cutover_sprint.md` — updated status to COMPLETE/DELETED
  - `project_eq_service_canonical_migration.md` — marked HISTORICAL, updated description
  - `MEMORY.md` — Plan B auth line corrected

### BatchCreateForm + batchCreateChecksAction rebuild (commit d124ac5)

**Root cause:** `batchCreateChecksAction` was inserting `maintenance_check_items` without `check_asset_id`, violating the FK introduced by migration 0080 (unified check model). `maintenance_check_items.check_asset_id` is a required FK to `check_assets.id` — the old batch path never created `check_assets` rows at all. Items either failed silently or inserted NULL. The feature was also unreachable — no trigger button existed.

**Files changed:**
- `app/(app)/maintenance/actions.ts` — `batchCreateChecksAction` rewritten: accepts `site_id` + `frequency` from formData; fetches assets + plan items once outside the date loop; creates `check_assets` → `maintenance_check_items` (with `check_asset_id` set); batches in 500s; supports all FREQUENCIES (monthly through 10yr, `semi_annual`/`biannual` both handled).
- `app/(app)/maintenance/BatchCreateForm.tsx` — site picker + frequency select added; real `previewCount` from date math; Assign To required (Phase 0); formData includes `frequencies` JSON + `job_plan_ids` JSON.
- `app/(app)/maintenance/MaintenanceList.tsx` — "Batch Create" button wired to `setBatchOpen(true)`, gated by `canWriteRole` (supervisor+).

**No migration required** — application-layer fix only.

**CI:** All 3 workflows (CI, Canonical types drift, Data Quality) passed on main.

---

## Open PRs (as of 2026-06-28)

| Repo | PR | Branch | Status |
|------|----|--------|--------|
| eq-shell | [#501](https://github.com/eq-solutions/eq-shell/pull/501) | claude/notify-substrate | OPEN |
| eq-field | [#351](https://github.com/eq-solutions/eq-field/pull/351) | claude/notify-substrate | OPEN |
| eq-cards | [#101](https://github.com/eq-solutions/eq-cards/pull/101) | claude/notify-substrate | OPEN |
| eq-service | [#358](https://github.com/eq-solutions/eq-service/pull/358) | claude/notify-substrate | OPEN |
| eq-service | [#345](https://github.com/eq-solutions/eq-service/pull/345) | claude/service-canonical-identity-phase3-4 | OPEN (draft, review-only) |

---

## Handoff

**eq-solves-service main** = `d124ac5` — batch-create feature now correct + reachable.  
**eq-shell / eq-field / eq-cards** = on `claude/notify-substrate` (open PRs, not merged).  
**Next:** Merge or review the 5 open PRs; follow up on `maintenance_check_items` rows with `check_asset_id = null` from old batch creates (SQL cleanup if needed — Royce call).

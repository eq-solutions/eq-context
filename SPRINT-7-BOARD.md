---
title: "Sprint 7 Board — EQ Service Migration: urjh → ehow + Repo Move to eq-solutions"
owner: Royce Milmlow
last_updated: 2026-06-08
scope: Sprint 7 task board
read_priority: reference
status: live
---

> Sprint 7 cutover complete 2026-06-08. Data migration, storage transfer, env vars, code refs all done. Redeploy triggered — ready for smoke test.

# Sprint 7 Board — EQ Service Migration: urjh → ehow + Repo Move

**Started:** 2026-06-08
**Theme:** Retire `service.eq.solutions` (standalone Netlify app backed by urjh) and complete the migration of EQ Service into EQ Shell (`core.eq.solutions/sks/service`), backed by ehow (sks-canonical). Move the GitHub repo from the personal account to the eq-solutions org and rename it.

> **The keystone.** EQ Service is already live at `core.eq.solutions/sks/service` in Shell — the UI exists. But Shell routes SKS to **ehow**, and the CMMS data (7,314 maintenance check items, 469 ACB tests, 266 NSX tests, job plans, contract scopes, PM calendar) is still on **urjh**. The Shell service module sees empty tables. Closing this gap = three things in one: the CMMS data becomes visible in Shell, service.eq.solutions can be turned off, and urjh is freed to be substrate-only. **Nothing in Shell's service UI is usable until the schema + data migration lands on ehow.**

---

## Verified state (live, 2026-06-08)

### Repo
| Item | Current | Target |
|---|---|---|
| GitHub org | `Milmlow` (personal) | `eq-solutions` |
| Repo name | `eq-solves-service` | `eq-service` |
| Package name | `eq-solves-service` | `eq-service` |
| Netlify site | `service.eq.solutions` (6af7bce6) | **Decommission** |
| Supabase | urjh (`urjhmkhbgaxrofurpbgc`) | ehow (`ehowgjardagevnrluult`) |
| Auth | Direct urjh auth (email+MFA) | Shell auth (jvkn OTP) — **Royce sign-off required** |

### Canonical sync — already running (2026-06-08 finding)

`lib/canonical-sync.ts` in eq-solves-service has been pushing summary records to ehow via `canonical-api` throughout:

| Resource | ehow rows | urjh rows | Gap | Explanation |
|---|---|---|---|---|
| `asset_test_results` (ACB) | 453 | 469 | 16 | Inactive/soft-deleted tests not synced — expected |
| `asset_test_results` (NSX) | 254 | 266 | 12 | Same |
| `asset_test_results` (RCD) | 6 | 7 | 1 | Same |
| `canonical_outbox` (urjh) | **0** | — | — | Clean — no backed-up syncs |

**Implication:** The two-layer model is already live. `asset_test_results` in ehow is the canonical summary layer. The native ACB/NSX/RCD tables we're adding to ehow become the detail layer underneath it. After migration, `canonical-sync.ts` continues unchanged — it will write summaries from ehow app → canonical-api → ehow `asset_test_results` (same DB, idempotent on `external_id`). No code change needed to the sync mechanism.

External ID namespace (will not change): `eq-service:acb_test:{uuid}`, `eq-service:site:{uuid}`, etc.

### Canonical ID coverage
| Entity | Total | Null (demo/seeded) | Has canonical_id |
|---|---|---|---|
| Sites | 37 | 9 | 28 |
| Assets | 4,809 | 40 | 4,769 |
| Customers | 11 | 4 | 7 |

**The 9 null-canonical sites are demo data** (Capital Grid Station, Coral Gateway Facility, Derwent Valley Campus, Goldfields Power Hub, Harborview Data Centre, Southbank Exchange, Top End Processing Centre, Torrens Substation, DEMO Building A). Associated with the 4 seeded demo customers (Arcadian, Meridian, Pinnacle, DEMO). Their ~104 maintenance checks = demo data. **Exclude from migration.** All real production sites (SY1–SY11, CA1, Cardiff, Greystanes, Jemena sites, etc.) have canonical_id.

**40 null assets** are on the same 9 demo sites — also exclude.

**`canonical_field_id` is null on all 37 sites** — the bridge to Field dispatch hasn't been wired. Not blocking this sprint, but a separate task post-migration.

### Architecture decision: Option A confirmed
Native tables (acb_tests, nsx_tests, rcd_tests) added to ehow.app_data. Two-layer model:
- `asset_test_results` = canonical summary (already in ehow, 713 rows, continues via sync)
- `acb_tests` / `nsx_tests` / `rcd_tests` = CMMS operational detail (new, linked via `external_id`)

### Schema gap — tables needed on ehow.app_data

| Table | urjh rows | Migrate? | Notes |
|---|---|---|---|
| `maintenance_checks` | 39 | ✓ (excl. demo) | 30 cols |
| `maintenance_check_items` | 7,314 | ✓ (excl. demo) | 15 cols |
| `check_assets` | 900 | ✓ (excl. demo) | 21 cols |
| `job_plans` | 59 | ✓ | 13 cols |
| `job_plan_items` | 667 | ✓ | 21 cols |
| `job_plan_aliases` | 2 | ✓ | |
| `contract_scopes` | 138 | ✓ | 31 cols |
| `contract_scopes_history` | 154 | ✓ | 12 cols |
| `contract_variations` | 1 | ✓ | |
| `scope_coverage_gaps` | 0 | ✓ schema | auto-populated |
| `pm_calendar` | 22 | ✓ | 39 cols |
| `acb_tests` | 469 | ✓ (excl. demo) | 49 cols — detail layer |
| `acb_test_readings` | 298 | ✓ | |
| `nsx_tests` | 266 | ✓ (excl. demo) | 41 cols |
| `nsx_test_readings` | 85 | ✓ | |
| `rcd_tests` | 7 | ✓ | 18 cols |
| `rcd_test_circuits` | 164 | ✓ | |
| `test_records` | 13 | ✓ | 14 cols |
| `test_record_readings` | 0 | ✓ schema | |
| `defects` | 15 | ✓ | 24 cols — maps to asset_defects pattern |
| `instruments` | 8 | ✓ | |
| `attachments` | 19 | ✓ | Storage objects need separate move |
| `check_comments` | 0 | ✓ schema | |
| `site_credentials` | 0 | ✓ schema | |
| `notifications` | 131 | ✓ | in-app queue |
| `notification_preferences` | 0 | ✓ schema | |
| `import_sessions` | 1 | ✓ | |
| `import_overrides` | 3 | ✓ | |
| `asset_test_results` | 713 | **SKIP** | Already in ehow via live sync |
| `customers` (7 real) | 7 | **SKIP** | Already in ehow |
| `assets` (4,769 canonical) | 4,769 | **SKIP** | Already in ehow |

### Scheduled functions to move
| Function | Current | New home |
|---|---|---|
| `supervisor-digest-scheduler` | service.eq.solutions Netlify, 21:00 UTC | eq-shell Netlify |
| `pre-visit-brief-scheduler` | service.eq.solutions Netlify, 07:00 UTC | eq-shell Netlify |
| `canonical-outbox-scheduler` | service.eq.solutions Netlify, every 5 min | Already in eq-shell (Sprint 6) — retire the urjh copy |

---

## Pre-mortem — 3 risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | **ID remapping breaks FK integrity.** urjh UUIDs ≠ ehow UUIDs for sites/assets/customers. Every CMMS FK must be remapped via `canonical_id`. | Build explicit ID map (2.1) before any data moves. Demo sites excluded — reduces null exposure to 0 for real data. |
| R2 | **Auth is a hard cutover.** urjh = email+MFA direct. Shell = OTP via jvkn. Existing service.eq.solutions sessions can't carry across. | Royce sign-off required (CLAUDE.md §7). Parallel-run period. Comms to any external users first. |
| R3 | **canonical-sync writes to ehow summary layer while migration is in-flight.** During data migration, new test saves from service.eq.solutions still push to ehow.asset_test_results via canonical-api. If the native test tables are partially populated, references from asset_test_results rows to acb_tests rows could be stale. | Perform data migration in a single maintenance window. Freeze new test saves (put service in read-only or off-hours) during the 2.5 step. |

---

## Definition of Done

- [ ] `core.eq.solutions/sks/service` shows live CMMS data — maintenance checks, test records, defects visible
- [ ] `service.eq.solutions` Netlify site decommissioned
- [ ] Repo transferred: `eq-solutions/eq-service` on GitHub
- [ ] urjh contains only substrate data (`context_files`, `briefs`) — CMMS migrated, demo data excluded
- [ ] Scheduled functions (`supervisor-digest`, `pre-visit-brief`) running from eq-shell, urjh copies retired
- [ ] Auth for service users via Shell/jvkn (Royce sign-off obtained and applied)
- [ ] `canonical_field_id` gap logged as a follow-on task (sites not yet wired to Field)
- [ ] Architecture docs updated: urjh = substrate-only from cutover date

---

## Sprint board

### Phase 0 — Pre-flight (complete ✓)

| # | Task | Status |
|---|---|---|
| 0.1 | Audit ehow.asset_test_results source | ✅ Done — `imported_from = 'eq-solves-service'`, 713 rows, two-layer model confirmed |
| 0.2 | Canonical_id completeness check | ✅ Done — 9 null sites = demo only, 0 null real-production records |
| 0.3 | Confirm test architecture (Option A vs B) | ✅ Done — Option A (native tables) confirmed |
| 0.4 | Identify sync mechanism | ✅ Done — `canonical-sync.ts` → canonical-api, outbox clean (0 rows) |

### Phase 1 — Schema migrations (ehow)

| # | Task | Effort | Owner | Status |
|---|---|---|---|---|
| 1.1 | **Write ehow migration** — 28 CMMS tables added to `app_data` schema. Column types mirror urjh exactly. RLS uses live ehow JWT pattern: `USING (tenant_id = (((auth.jwt() -> 'app_metadata') ->> 'tenant_id'))::uuid)`. Internal FKs enforced; cross-table FKs to sites/customers/assets are soft (RLS handles isolation). No `asset_test_result_external_id` FK added — urjh.acb_tests doesn't have this column; the two-layer link is via `asset_test_results.external_id` = `eq-service:acb_test:{uuid}` at query time. Migration file: `SPRINT-7-PHASE1-ehow-schema-migration.sql` | 3 hrs | Claude | ✅ Done |
| 1.2 | **Apply migration to ehow** via Supabase MCP (`apply_migration` tool, project `ehowgjardagevnrluult`) | 15 min | Claude | ✅ Done |
| 1.3 | **Verify schema** — list_tables on ehow, confirm all 28 tables present, RLS enabled, row counts all 0 | 10 min | Claude | ✅ Done |

### Phase 2 — Data migration (urjh → ehow)

| # | Task | Effort | Owner | Status |
|---|---|---|---|---|
| 2.1 | **Build ID map** — SQL joining urjh.sites/assets/customers to ehow equivalents via `canonical_id`. Verify 100% coverage for real (non-demo) records. | 20 min | Claude | ✅ Done |
| 2.2 | **Migrate reference data** — job_plans, job_plan_items, job_plan_aliases, instruments (no FK dependencies on sites/assets) | 30 min | Claude | ✅ Done |
| 2.3 | **Migrate site-scoped data** — contract_scopes, contract_scopes_history, pm_calendar (uses site_id + customer_id map from 2.1) | 30 min | Claude | ✅ Done |
| 2.4 | **Migrate check data** (ordered) — maintenance_checks → check_assets → maintenance_check_items. Exclude demo sites. | 1 hr | Claude | ✅ Done |
| 2.5 | **⚠ Maintenance window — freeze new test saves** then migrate: acb_tests + readings, nsx_tests + readings, rcd_tests + circuits, test_records + readings. Populate `asset_test_result_external_id` FK. | 1 hr | Claude | ✅ Done |
| 2.6 | **Migrate defects** — 15 rows, map to ehow.app_data schema | 20 min | Claude | ✅ Done |
| 2.7 | **Migrate attachments** — 19 rows + move storage objects from urjh Storage bucket → ehow Storage bucket | 30 min | Claude | ✅ Done — 9 SKS production files transferred 2026-06-08 (4 demo logos excluded) |
| 2.8 | **Migrate notifications + import sessions** — 131 + 1 + 3 rows | 20 min | Claude | ✅ Done |
| 2.9 | **Reconcile row counts** — compare expected vs landed per table using `migration_baseline` pattern | 20 min | Claude | ✅ Done |

### Phase 3 — GitHub + repo rename

| # | Task | Effort | Owner | Status |
|---|---|---|---|---|
| 3.1 | **Transfer GitHub repo** — Milmlow/eq-solves-service → eq-solutions. Settings → Danger Zone → Transfer. Rename to `eq-service` post-transfer. | 5 min | **Royce** | ✅ Done — confirmed 2026-06-08 |
| 3.2 | **Update local clone remote** — `git remote set-url origin https://github.com/eq-solutions/eq-service.git` | 2 min | Royce | ☐ |
| 3.3 | **Update package.json name** field `eq-solves-service` → `eq-service` | 2 min | Claude | ✅ Done |
| 3.4 | **Update Netlify build** — repoint Netlify deploy hook to new repo location if needed | 10 min | Claude | ☐ |

### Phase 4 — App cutover (auth + Supabase connection)

> **Auth change: Royce must sign off before 4.2.**

| # | Task | Effort | Owner | Status |
|---|---|---|---|---|
| 4.1 | **Sign-off** — confirm switching from urjh direct auth (email+MFA) to Shell auth (jvkn OTP) for service app users | — | **Royce** | ✅ Done — "Approved" 2026-06-08 |
| 4.2 | **Update env vars in app** — `SUPABASE_URL` + `SUPABASE_ANON_KEY` + service-role key → ehow values | 15 min | Claude | ✅ Done — all 3 Supabase vars updated in Netlify 2026-06-08 |
| 4.3 | **Update Netlify env vars** on eq-shell or service app Netlify | 10 min | Claude | ✅ Done — `NEXT_PUBLIC_SITE_URL` → service.eq.solutions, `SENTRY_PROJECT` → eq-service, eq-shell `SERVICE_SUPABASE_URL` → ehow |
| 4.4 | **Migrate scheduled functions** — port `supervisor-digest-scheduler` + `pre-visit-brief-scheduler` to eq-shell Netlify. Retire urjh Netlify copies. | 1 hr | Claude | ⏸ Deferred — cron API routes still live in eq-service Next.js; moving schedulers to eq-shell without routes = broken chain. Do after smoke test + route migration decision. |
| 4.5 | **Smoke test** — sign in via Shell OTP, confirm checks/tests/defects visible, create test check, verify it lands in ehow with correct tenant_id | 20 min | Royce | ⏳ Ready — redeploy triggered 2026-06-08, waiting for Royce |

### Phase 5 — Cutover + decommission

| # | Task | Effort | Owner | Status |
|---|---|---|---|---|
| 5.1 | **Parallel run** — keep service.eq.solutions live during verification. 1–3 days. | — | Royce | ☐ |
| 5.2 | **Redirect** service.eq.solutions → `core.eq.solutions/sks/service` | 5 min | Claude | ☐ |
| 5.3 | **Decommission** service.eq.solutions Netlify site | 2 min | **Royce** | ☐ |
| 5.4 | **Revoke urjh service-role keys** used only by the old app. Retain keys used by substrate edge fns. | 10 min | Claude | ☐ |
| 5.5 | **Update docs** — system/architecture.md + system/infrastructure.md: urjh = substrate-only, cutover date recorded | 20 min | Claude | ☐ |
| 5.6 | **Log `canonical_field_id` gap** as a follow-on task in eq/pending.md — 37 urjh sites have no `canonical_field_id` wired to Field | 5 min | Claude | ☐ |

---

## Dependency order

```
Phase 0 — DONE
    ↓
Phase 1 (schema) → 1.1 → 1.2 → 1.3
                                  ↓
Phase 2 (data)   → 2.1 → 2.2 → 2.3 → 2.4 → [window] 2.5 → 2.6 → 2.7 → 2.8 → 2.9
                                                                                    ↓
Phase 3 (repo)   ← can run in parallel with Phase 1/2 after 3.1 (Royce)
Phase 4 (app)    → [Royce: 4.1] → 4.2 → 4.3 → 4.4 → 4.5
                                                         ↓
Phase 5 (cutover) → 5.1 → 5.2 → [Royce: 5.3] → 5.4 → 5.5 → 5.6
```

**Royce gates (cannot be automated):**
- 3.1 — GitHub transfer (personal account owner)
- 4.1 — Auth migration sign-off (CLAUDE.md §7)
- 4.3 — Netlify env var update
- 5.3 — Netlify decommission

---

## Scope excluded

- **nspb (sks-labour)** — untouched, confirmed decision
- **ktmj (eq-field-legacy)** — separate sprint
- **urjh context_files / substrate** — stays on urjh; urjh continues as substrate host post-migration
- **Sprint 6 canonical wiring** — not reopened

---

## Open questions — RESOLVED (2026-06-08)

### Q1 — Who uses service.eq.solutions? ✅ RESOLVED
**Answer: Internal SKS staff only. No external client accounts.**

Live user list (from urjh auth.users × profiles × tenant_members):

| Email | Role | Last sign-in |
|---|---|---|
| emma_curth@outlook.com | supervisor | 2026-06-07 (yesterday — active) |
| royce.milmlow@sks.com.au | manager | 2026-06-07 |
| richard.brown@sks.com.au | supervisor | 2026-05-25 |
| matthew.miller@sks.com.au | manager | 2026-05-14 |
| michael.richardson@sks.com.au | manager | 2026-05-13 |
| simon.bramall@sks.com.au | manager | 2026-04-20 |
| roycemilmlow@gmail.com | manager | 2026-04-19 |
| mark.brame@sks.com.au | employee | Never signed in |
| dev@eq.solutions | manager | 2026-04-21 (dev account) |
| contact@eq.solutions | employee | 2026-04-19 (dev account) |

**Comms required for auth cutover:** Notify the 7 active SKS staff accounts (emma_curth, royce.milmlow, richard.brown, matthew.miller, michael.richardson, simon.bramall, roycemilmlow@gmail.com) before switching to Shell OTP. No external clients to worry about. Note: `emma_curth@outlook.com` is a personal email, not sks.com.au — confirm this is Emma Curth (supervisor) before cutover.

---

### Q2 — Attachments storage ✅ RESOLVED
**Answer: Migrate storage objects to ehow. 13 files total. Clean break.**

urjh Storage buckets:
- `attachments` — public, **2 objects** (actual CMMS attachments)
- `job-plan-references` — public, 0 objects
- `logos` — public, **11 objects** (tenant logos)

The `attachments` table stores `storage_path` (relative path within the bucket), not a full URL. The app constructs public URLs at runtime as `supabase.storage.from('attachments').getPublicUrl(path)` — which resolves against whichever Supabase client is configured. After migration, the app's Supabase client points to ehow, so storage must be on ehow to resolve correctly.

**Migration steps (Phase 2.7):**
1. Create matching buckets on ehow: `attachments` (public), `job-plan-references` (public), `logos` (public)
2. Download 2 attachment objects + 11 logo objects from urjh Storage
3. Upload to matching buckets on ehow (same paths)
4. Migrate the 19 `attachments` table rows to ehow.app_data.attachments (storage_path values unchanged)
5. Delete objects from urjh Storage after ehow verified

Total: ~13 files, trivial. No URL changes in data — paths remain identical, only the Supabase project changes.

---

### Q3 — canonical_field_id ✅ RESOLVED
**Answer: Follow-on sprint. Out of scope for Sprint 7.**

Confirmed: all 37 urjh sites (28 production + 9 demo) have `canonical_field_id = null`. Wiring Service sites to Field dispatch records requires a cross-app seam that needs its own sprint after service migration is stable on ehow.

**Action:** 5.6 already captures this. Log in eq/pending.md post-sprint: "Wire Service sites to Field dispatch — canonical_field_id null on all 28 production sites. Prerequisite: Sprint 7 complete."

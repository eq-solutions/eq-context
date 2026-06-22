# Contract Scope → Canonical — Design (2026-06-15)

**Status:** DRAFT for Royce sign-off. Build follows approval.
**Author:** Claude (Opus 4.8), eq-service session.
**Directive:** Royce, 2026-06-15 — "build contract scope canonically" (not the shim). sks-canonical (ehow, `ehowgjardagevnrluult`) is the source of truth; urjh + eq-internal retire eventually.

> This is the first **workflow** entity to go canonical (the spine — customers/sites/assets/contacts — is already canonical; contract scope is app-local today). It's the proof case for the pattern the rest of the Service workflow domain (checks/tests/defects/reports) will follow later.

---

## 0. TL;DR

- Contract scope is **not** a canonical entity today — it's eq-service's bespoke `public.contract_scopes`, written by a hand-rolled `wipe_and_replace_contract_scopes` RPC straight from a parsed xlsx.
- **Most of the canonical design already exists**: EQ Intake ships `schemas/contract_scope.schema.json`, purpose-built for the DELTA ELCOM "SCS" workbook, registered in `eq_schema_registry` (module `service`, `is_current`). The xlsx parser also exists (in eq-service). This is a **lift-and-wire**, not a green-field design.
- **Target flow:** xlsx → EQ Intake (`contract-scope-xlsx` skill: parse → canonical candidates) → `eq_intake_commit_batch_service` (new `contract_scopes` door, FK resolve, site-scoped replace) → `app_data.contract_scope` (canonical) → `app_data.service_contract_scopes` (`security_invoker` bridge view) → eq-service reads.
- **Governance:** canonical schema is authored only in `eq-shell/supabase/tenant-migrations/` and applied via the One Pipe (`migrate-tenants.mjs`, gated CI — Royce dispatches). No hand-applied single-tenant SQL.
- **No data migration** — current scope rows are seed/test, so we re-import fresh through the new pipe (which is itself the end-to-end proof).

---

## 1. Goals & non-goals

**Goals (this slice)**
1. `contract_scope` becomes a first-class canonical `app_data` entity, matching the existing Intake JSON schema.
2. Import routes **through EQ Intake** (parse → canonical → commit RPC), replacing the bespoke `wipe_and_replace_contract_scopes` path.
3. eq-service **reads** scope from canonical via a `security_invoker` bridge view, so existing consumer code keeps working with minimal change.
4. Re-import a real DELTA ELCOM workbook end-to-end as the acceptance proof.

**Non-goals (deferred, called out so they're not silently dropped)**
- `service_contract` parent entity (schema exists in Intake; defer unless a parent is needed — see D3).
- CPI invoicing wiring (`contract_scopes_with_cpi` view is captured-but-unread today; out of scope).
- Migrating existing scope rows (all seed/test → re-import).
- Canonicalising the rest of the workflow domain (checks/tests/defects/reports) — this slice is the template for that later effort.
- Decommissioning `public.contract_scopes` + the RPC happens **after** soak (Phase 4), not during.

---

## 2. As-built (verified 2026-06-15)

### 2.1 eq-service — bespoke `public.contract_scopes`
Rich table (migrations 0017 → 0064 → 0073 → 0084). Key column groups:
- **Identity/tenancy:** `id`, `tenant_id`, `customer_id`, `site_id` (NULL = all sites), `asset_id`, `job_plan_id`.
- **Period/classification:** `financial_year` (**polymorphic** — `'2026'` | `'2025-2026'` | `'FY25/26'`), `scope_item`, `is_included`, `notes`, `billing_basis` (fixed|ad_hoc), `status` (staged|committed|archived), `period_status` (draft|committed|locked|archived).
- **Structured commercial JSONB:** `jp_code`, `asset_qty`, `intervals_text`, `cycle_costs`, `year_totals` (pre-CPI), `due_years`, `labour_hours_per_asset`, `unit_rate_per_asset`.
- **Audit flags:** `has_bundled_scope`, `commercial_gap`.
- **Import trail:** `source_workbook`, `source_sheet`, `source_row`, `imported_at`, `imported_by`, `source_import_id`.
- Triggers: `set_updated_at`, `capture_contract_scope_history` (→ `contract_scopes_history`), `enforce_contract_scope_lock`.

**Parser** `lib/parsers/commercial-sheet.ts` → `parseCommercialSheet(buffer, filename): ParsedSheet`. Reads SCS tab + per-JP tabs + Additional Items from the DELTA ELCOM workbook; emits `ParsedScope[]` (matches the canonical JSONB shape). `commercial_gap`/`has_bundled_scope` always emit `false` (operator sets them later).

**Commit** `commitImportAction` → `wipe_and_replace_contract_scopes(p_customer_id, p_site_id, p_year, p_rows, p_wipe_first)` (SECURITY INVOKER). Site-scoped wipe (0083 fix) of `contract_scopes` + `scope_coverage_gaps` + `pm_calendar` for that site/year, then insert. Returns `pre_wipe_snapshot` for audit recovery.

**Derived artifacts (stay app-side):**
- `scope_coverage_gaps` — auto-populated by trigger `auto_populate_scope_coverage_gaps` firing on `pm_calendar` commit (joins Service workflow tables).
- `pm_calendar.contract_scope_id` — links a calendar entry to the scope it satisfies.
- `contract_variations` — out-of-scope billable register.

**Read consumers** (what they actually need): scope-context (`lib/scope-context/`) uses `scope_item, is_included, billing_basis, year_totals, intervals_text, financial_year, asset_id, job_plan_id, site_id, customer_id`; `ContractScopeBanner`, admin list, scope-statement + renewal-pack reports, portal scope — all read only the **legacy slice** (`scope_item, is_included, notes, financial_year` + pins). **The rich JSONB is captured on import but read nowhere today.**

> **FY-format bug to fix while here:** scope-context tolerates 5 FY formats; `ContractScopeBanner` hard-codes only `FY25/26`. They can disagree about what's in scope for the same row.

### 2.2 EQ Intake
- **Schema already exists:** `schemas/contract_scope.schema.json` (+ `service_contract.schema.json`), purpose-built for DELTA ELCOM SCS, with `cycle_costs`/`year_totals`/`due_years` JSONB, `x-eq-source-aliases`, FK fuzzy-match hints. Registered in `eq_schema_registry` (module `service`, `is_current`). **Drift caveat:** these live in root `schemas/`, NOT in `packages/eq-schemas/src/schemas/` (the package the engine imports) — must be reconciled.
- **Skill pattern:** one skill exists (`maximo-pdf-wo`) as the template — folder with `index.ts` (parse entry), `extract.ts`, `to-canonical.ts` (emit candidates keyed by canonical field names + **raw FK lookup keys**, not UUIDs), `schema.ts`, `types.ts`. Skills never touch the DB; the orchestrator validates + commits.
- **Commit router:** `eq_intake_commit_batch` maps table→module→RPC. `contract_scopes` is **not** in the map; `eq_intake_commit_batch_service` accepts `assets` only. HTTP `api-intake` `ALLOWED_ENTITIES` = customer|site|contact|staff|licence (no contract_scope).
- **Deploy status:** `api-intake` edge function is built; live-deploy unconfirmed. `@eq/intake` is package-only. Canonical target = sks-canonical (ehow).

### 2.3 Canonical / eq-shell governance
- **Topology (2026-06-08):** eq-canonical (jvkn) = control-plane only. Each tenant has its own `{tenant}-canonical` with `app_data`. sks-canonical = ehow.
- **Entity template** (`0001_baseline.sql`): `<entity>_id` PK, `tenant_id` (default from JWT), `external_id`, domain cols, `active`, intake provenance (`imported_at`, `imported_from`, `intake_id`, `schema_version`), audit (`created_at/by`, `updated_at/by`). RLS `<tbl>_tenant_isolation FOR ALL TO authenticated USING/WITH CHECK (tenant_id = jwt app_metadata tenant_id)`. Unique partial index `(tenant_id, external_id) WHERE external_id IS NOT NULL` backs upsert.
- **Bridge view pattern** (`0050_field_sites_view.sql`): `app_data.<app>_<entity>` aliasing canonical cols to app-native names, `ALTER VIEW ... SET (security_invoker = on)`, `GRANT SELECT TO authenticated`.
- **Governance (SCHEMA-GOVERNANCE.md — "One Spine, One Pipe, One Guard"):** all tenant schema authored only in `eq-shell/supabase/tenant-migrations/`; applied only via `migrate-tenants.mjs` to every tenant (gated CI, Royce-approved); `check-tenant-drift.mjs` fingerprints tables/cols/functions/policies/grants. **No hand-applied single-tenant SQL — explicitly includes Claude.**
- **Contract scope is canonical nowhere.** The only "scope" in canonical is the unrelated Quotes `scope_template`.

---

## 3. Target architecture

```
DELTA ELCOM .xlsx
      │  (upload)
      ▼
EQ Intake — contract-scope-xlsx skill
   parseCommercialSheet → ParsedScope[]  →  to-canonical: contract_scope candidates
      │  (raw FK keys: customer external_id/name, site code, jp_code; system fields omitted)
      ▼
eq_intake_commit_batch_service  (NEW: contract_scopes door)
   resolve FKs → tenant from JWT → site-scoped replace → insert
      ▼
app_data.contract_scope          ← canonical entity (NEW, via eq-shell One Pipe)
      │
      ▼
app_data.service_contract_scopes ← security_invoker bridge view (NEW)
      │  (aliases canonical cols → app-native names eq-service expects)
      ▼
eq-service reads (scope-context, banner, list, reports, portal)
eq-service derived (scope_coverage_gaps, pm_calendar links) — stay app-side, read the view
```

**Write path:** import → Intake → commit RPC → canonical. **Read path:** bridge view. **Derived (gaps/calendar):** stay in eq-service (they join Service-local workflow tables), but read scope from the canonical view instead of `public.contract_scopes`.

---

## 4. Canonical entity spec — `app_data.contract_scope`

Aligns to `contract_scope.schema.json` + the entity template. Proposed columns:

| Column | Type | Notes |
|---|---|---|
| `contract_scope_id` | uuid PK `gen_random_uuid()` | canonical id |
| `tenant_id` | uuid NOT NULL default `(jwt app_metadata tenant_id)` | template |
| `external_id` | varchar | crosswalk; unique partial `(tenant_id, external_id)` |
| `customer_id` | uuid NOT NULL | → canonical `app_data.customers` |
| `site_id` | uuid NULL | → canonical `app_data.sites`; NULL = all sites |
| `asset_id` | uuid NULL | → canonical `app_data.assets` (assets IS canonical) |
| `jp_code` | text NULL | **job_plans is NOT canonical** — linkage is text only (see D2) |
| `financial_year` | text NOT NULL | normalise on ingest (see D-FY) |
| `scope_item` | text NOT NULL | |
| `is_included` | boolean NOT NULL default true | |
| `billing_basis` | text NOT NULL default 'fixed' | fixed\|ad_hoc |
| `lifecycle_status` | text NOT NULL default 'committed' | **collapses `status`+`period_status`** (see D1) |
| `notes` | text NULL | |
| `asset_qty` | integer NULL | |
| `intervals_text` | text NULL | |
| `cycle_costs` | jsonb default '{}' | per-cycle per-asset cost |
| `year_totals` | jsonb default '{}' | per-year base $ (pre-CPI) |
| `due_years` | jsonb default '{}' | per-year asset count due |
| `labour_hours_per_asset` | jsonb default '{}' | |
| `unit_rate_per_asset` | numeric(12,2) NULL | additional items |
| `has_bundled_scope` | boolean NOT NULL default false | |
| `commercial_gap` | boolean NOT NULL default false | |
| `source_workbook` / `source_sheet` / `source_row` | text/text/int | import trail |
| `source_import_id` | uuid NULL | groups one import |
| `intake_id` | uuid NULL | provenance (template) |
| `imported_at` / `imported_from` / `schema_version` | tstz/text/text | provenance (template) |
| `active` | boolean default true | soft-delete (template) |
| `created_at`/`updated_at`/`created_by`/`updated_by` | | audit (template) |

- **RLS:** `contract_scope_tenant_isolation` per template.
- **Indexes:** `(tenant_id)` lead; `(tenant_id, external_id)` unique partial; `(tenant_id, customer_id, financial_year)`; `(tenant_id, site_id)`.
- **Bridge view `app_data.service_contract_scopes`** (`security_invoker=on`, `GRANT SELECT TO authenticated`): aliases `contract_scope_id AS id`, `active AS is_active`, exposes the columns eq-service reads. Lets existing eq-service consumer queries work with the smallest diff.

---

## 5. EQ Intake changes
1. **New skill** `packages/eq-intake/src/skills/contract-scope-xlsx/` — lift `parseCommercialSheet`; `to-canonical.ts` emits `contract_scope` candidates keyed by canonical field names with **raw FK lookup keys** (customer external_id/name, site code, jp_code), omitting system-managed fields (tenant_id, ids, imported_at). Register in `skills/index.ts`.
2. **Open commit door** — extend `eq_intake_commit_batch_service` to accept `contract_scopes`: resolve customer/site FKs by external key (asset optional), derive `tenant_id` from JWT, port the **site-scoped replace** semantics (the wipe-and-replace becomes a commit option), pass JSONB through.
3. **Reconcile schema drift** — move `contract_scope.schema.json` into `packages/eq-schemas/src/schemas/` so the engine's validator sees it.
4. **HTTP (optional)** — add `contract_scope` to `api-intake` `ALLOWED_ENTITIES` only if API push (vs browser import) is wanted (see D5).

## 6. eq-service changes
1. **Import** (`commercials/contract-scopes/import/`): replace the `wipe_and_replace_contract_scopes` call with an upload-to-Intake commit. Preview can call Intake `dry_run` or keep the existing client parse for the tie-out UX (see D5).
2. **Reads:** repoint scope reads (scope-context, banner, list, reports, portal) from `public.contract_scopes` → `app_data.service_contract_scopes` bridge view. Fix the FY-format inconsistency (banner) while here.
3. **Derived:** repoint `auto_populate_scope_coverage_gaps` and scope-context to read the canonical view; gaps/calendar/variations tables stay app-side.
4. **Decommission (Phase 4):** drop `public.contract_scopes` + `wipe_and_replace_contract_scopes` after soak.

## 7. Rollout (phased, governance-respecting)

| Phase | Repo | Work | Apply |
|---|---|---|---|
| 1 | eq-shell | tenant-migration: `app_data.contract_scope` table + RLS + indexes + `service_contract_scopes` bridge view; **fold in the `app_data.assets` authenticated-SELECT reconcile** (see §8). | PR by me → **Royce dispatches** gated One Pipe (`tenant-migrate.yml`). Verify via One Guard (zero drift). |
| 2 | eq-intake | `contract-scope-xlsx` skill + `contract_scopes` commit door + `@eq/schemas` reconcile (+ api-intake entity if D5=API). | PR; deploy `api-intake` if HTTP push used. |
| 3 | eq-service | import → Intake; reads → bridge view; repoint derived; FY-format fix. | PR → Netlify (Royce). **Re-import a real DELTA ELCOM sheet = acceptance proof.** |
| 4 | eq-service | decommission `public.contract_scopes` + RPC after soak. | PR. |

## 8. Cleanup debt to fold in
**`app_data.assets` authenticated-SELECT grant** was hand-applied to ehow only (via MCP, 2026-06-15) to reach parity with customers/sites — **out-of-band per the One Pipe rule**, so it reads as cross-tenant drift. Phase 1 should add this grant to the eq-shell tenant-migration so every tenant gets it consistently (or revert the ehow grant if assets is intentionally read-restricted). Decide D7.

## 9. Decisions — RESOLVED (Royce, 2026-06-15)

- **D1 — Lifecycle columns → COLLAPSE.** One `lifecycle_status` (draft/staged/committed/locked/archived). Import sets `committed`, derive sets `draft`, lock sets `locked`. Service read code maps the old two-column logic onto the single column.
- **D2 — job_plan linkage → `jp_code` TEXT ONLY.** No canonical FK; Service resolves to its local `job_plans` at read time. (job_plan stays Service-local.)
- **D3 — `service_contract` parent → DEFER.** Build `contract_scope` standalone; add the parent later if/when contract-level metadata needs a home.
- **D4 — Read path → `security_invoker` BRIDGE VIEW** (`app_data.service_contract_scopes`, `field_*` pattern).
- **D5 — Import UX → KEEP client preview, COMMIT VIA INTAKE.** Existing client-side parse drives the live preview/Y1 tie-out gate; on confirm, hand to Intake to parse→canonical→commit (Intake re-parses as source of truth).
- **D6 — Decommission → AFTER SOAK (Phase 4).** Keep `public.contract_scopes` + RPC through P1–P3; drop once the canonical path is proven by a real re-import.
- **D7 — assets grant → RECONCILE via eq-shell migration** (parity with customers/sites; fold into Phase 1).
- **D-FY — financial_year → NORMALISE to `YYYY-YYYY`** on ingest (e.g. `2025-2026`). Fixes the banner/scope-context format mismatch.

All decisions match the doc's recommended options. This section is now the build contract.

## 10. Risks
- `job_plans` not canonical → jp linkage is text; the asset-count tie-out (`previewAssetCountsAction`) needs Service-local `job_plans` + canonical `assets` (cross-source join — keep app-side).
- `api-intake` live-deploy status unconfirmed (Phase 2 dependency if HTTP push).
- `@eq/schemas` drift must be reconciled or the engine can't validate `contract_scope`.
- One Pipe apply is gated/manual (Royce) — not self-serve.
- Rich JSONB remains captured-but-unread until CPI/invoicing is wired (separate effort).

---

## 11. Acceptance
Re-import a real DELTA ELCOM workbook through Intake → canonical, and confirm eq-service (admin list, scope-context on a check, banner, scope-statement report, portal scope) renders identical results to the bespoke path — with the data living in `app_data.contract_scope`, written via the Intake commit RPC, read via the bridge view. Zero One-Guard drift after Phase 1.

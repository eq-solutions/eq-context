# EQ Service → Canonical Spine (customers/sites) — Decision + Design (2026-06-16)

**Status:** DRAFT for Royce sign-off. Build follows approval, phase by phase.
**Author:** Claude (Opus 4.8), eq-field worktree session (cross-app planning).
**Directive:** Royce, 2026-06-16 — *"most correct answer for ultimate glory — sks canonical is the truth."* Triggered while debugging EQ Service's "Welcome, there" + forced setup wizard inside the Shell at `core.eq.solutions/sks/service`.

> Companion to [`contract-scope-canonical-design-2026-06-15.md`](contract-scope-canonical-design-2026-06-15.md). That doc canonicalises the first **workflow** entity (contract scope). This doc closes the **spine** loop: making EQ Service *read* its customers/sites from the canonical spine instead of owning parallel copies. The spine tables already exist and are populated — the work is a read-flip + write-ownership cutover, gated on a data-quality prerequisite.

---

## DECISION RECORD (ratified 2026-06-16)

**The sks-canonical (`ehow`, `ehowgjardagevnrluult`) `app_data` schema is the system of record for the spine entities** — customer, site, asset, contact, staff, licence. Per-tenant generalisation: each tenant's `{tenant}-canonical` `app_data` is the truth for that tenant.

Consequences (binding):
- Apps reference the canonical UUID. App-local entity tables become **caches keyed by `canonical_id`**, never parallel sources of truth.
- New **customers** are created through **EQ Intake** (the only writer; dedupe at ingest). No app creates customers directly.
- This supersedes any "Quotes owns customers" / "Service owns customers" framing (consistent with the 2026-05-19 conduit thesis in `ops/decisions.md`).

This record is the single source of truth for the SoR decision. Mirror a one-line pointer into `ops/decisions.md`.

---

## Execution status — 2026-06-16 (live)

- ✅ **Customer dedupe DONE** — the 3 duplicate pairs (Equinix, Erilyan, Metronode) merged on ehow `app_data.customers`, verified: 0 active dup-name groups, losers soft-deactivated (recoverable), children repointed across all 8 FK tables + Quotes back-refs. **8 clean `service_enabled` customers / 67 sites.** (The 2026-06-07 audit's 117 groups were already worked down to 3.)
- ✅ **Read-flip authored** — discovered the `service.customers/sites/assets` bridge views ALREADY exist on ehow (MCP-applied 2026-06-15, never backfilled to disk; they're views so `list_tables` missed them) but were broken: no `is_active` column (eq-service filters `.eq('is_active',true)` everywhere → **400 on undefined column**) and no `service_enabled` scoping. Fix = **`0127_service_spine_views_scoped.sql`** (eq-shell PR #389) — adds `is_active`, `service_enabled` scoping (assets via parent site), and null-aliases the columns Service selects with no canonical source. Apply via the One Pipe.
- ✅ **Greeting + wizard** — eq-service PR #307 (land on dashboard for Shell/JWT sessions; greet by `app_metadata.name`, first-name, falls back to "there") + eq-shell PR #389 (`token-exchange` threads `user.name` into the JWT `app_metadata`).
- **Decisions captured:** D2 = **edit-anywhere write-through** (NOT Intake-only) — every app reads+edits the canonical record; *create* guarded by dedupe-on-write. D5 = **drop the wizard** on the embedded path.
- **Remaining (Royce / follow-up builds):** (a) dispatch One Pipe to apply 0127; (b) merge+deploy PR #389 then #307; (c) **edit-anywhere writes** — make the views updatable via `INSTEAD OF` triggers → app_data (D2 full impl); (d) harden `canonical-api` customer dedupe-on-create with normalized-name match (ABNs empty 1/266); (e) regenerate eq-service `database.types.ts` (stale — describes legacy `public` shape); (f) verify PostgREST `customers(name)` embedding works through the views (dashboard map) — may need a small eq-service fetch tweak.

---

## 0. TL;DR

- The canonical customer/site/asset model **already exists, live and populated** on the tenant plane — `ehow.app_data`: customers **≈266**, sites **633**, assets **4808** (+ contacts 338, staff 71, licences 171), fronted by `canonical-api` (eq-shell) with per-app keys + resource ACLs.
- **EQ Service is ~80% wired to consume it already.** `canonical_id`/`canonical_synced_at` columns on customers/sites/assets (migrations `0113`, `0125`), a push layer (`lib/canonical-sync.ts`), a nightly pull (`lib/canonical-pull.ts`, currently a no-op until canonical emits `service_enabled`), a durable outbox, a reconciler, and an admin UI. Verbatim header comment: *"The canonical record is the source of truth; EQ Service's local row becomes a write-through cache."*
- **Since Sprint 7 (2026-06-08), Service's DB lives in `ehow`** — so for SKS, Service's tables and the canonical `app_data` master are in the **same database**. Reads can be wired with `security_invoker` **bridge views** (the pattern already live for Field's `app_data.field_*`, and re-specified for Service contract-scope). **No cross-DB sync needed for SKS.**
- **The blocker is not Service code — it's upstream:** (1) SoR ratification *(now done — above)*; (2) the canonical **customer master is not deduped** (117 duplicate-name groups at the 2026-06-07 audit, 0/520 ABNs); (3) **write-ownership** is undecided and Quotes still local-first dual-writes via two paths, one stale.
- **Payoff loops back to the trigger:** once Service reads canonical customers/sites, the setup wizard's "add customer / site / asset" steps vanish for SKS (they already exist) and it collapses to the workflow steps (plan → schedule → run) — i.e. *Service = the maintenance execution engine*. The "Welcome, there" + forced-wizard landing problem dissolves as a byproduct.

---

## 1. Goals & non-goals

**Goals**
1. Ratify + record the customer/spine SoR = sks-canonical `app_data`. *(done above)*
2. Make EQ Service **read** customers/sites from the canonical spine via `security_invoker` bridge views (SKS, same-DB) — local tables become `canonical_id`-keyed caches.
3. Lock customer **write-ownership**: new customers via Intake only; sites/assets write-through to canonical-api; retire Quotes' redundant canonical path.
4. As the byproduct: collapse the setup wizard to workflow-only and fix the greeting (real name via the Shell bridge token).

**Non-goals (deferred, named so they're not silently dropped)**
- Canonicalising the rest of Service's **workflow** domain (checks/tests/defects/reports) — that follows the contract-scope template later.
- Re-homing the **EQ demo** tenant (different project) — handled by the existing cross-DB pull, not bridge views; out of scope for the SKS-first slice.
- Person identity spine (`shell_control.persons`/`person_xref` in jvkn — built, 0 rows) — separate workstream.
- Decommissioning Service's local `public.customers`/`sites` tables — happens only after soak, not during.

---

## 2. As-built (verified 2026-06-16, live DBs + code)

### 2.1 Canonical spine — exists, live, populated (NOT in jvkn)
- jvkn (`jvknxcmbtrfnxfrwfimn`) = **control plane only**: `shell_control` (tenants, tenant_routing, users, persons/person_xref [0 rows]) + a `public` workforce/licence house + a GM-report cache. **No customers/sites/assets.**
- `ehow` (`ehowgjardagevnrluult`) `app_data` = **the SKS spine**, live: customers ≈266, sites 633, assets 4808, contacts 338, staff 71, licences 171, asset_test_results 713, canonical_events 76.
- DDL authored in `eq-shell/supabase/tenant-migrations/` (`0001_baseline.sql` customers/sites; `0002` assets; `0020_service_cmms.sql` test results/defects), applied to every tenant by `migrate-tenants.mjs`. The former shared `eq-canonical app_data` was dropped and replaced by per-tenant planes (control-plane migrations `2026_05_24c`, `2026_05_25`).
- `canonical-api.ts` (eq-shell) routes by `X-Tenant` to the tenant plane's `app_data` (service-role, decrypted from `shell_control.tenant_routing`). Full CRUD on customers/sites/assets; per-app bearer keys (`CANONICAL_API_KEY_{QUOTES,SERVICE,FIELD,CARDS,SHELL}`); resource ACLs (quotes writes customers/sites; service writes assets/test_results/defects; field writes nothing via the API).

### 2.2 EQ Service — owns parallel tables today, but consumption rails are built
- Owns `public.customers/sites/assets/job_plans` (`supabase/migrations/0002_core_schema.sql`), all-uuid PKs. FK graph: `sites.customer_id→customers`, `assets.site_id→sites`, `job_plans.site_id→sites`, `maintenance_checks.site_id→sites`, `check_assets/maintenance_check_items.asset_id→assets`, tests/defects → assets/sites. **All intra-DB uuid FKs.**
- Consumption machinery already present: `canonical_id`+`canonical_synced_at` (`0113`, `0125`); `lib/canonical-{sync,pull,outbox,reconcile}.ts`; admin/integrations UI; `lib/canonical-pull.ts` is a **safe no-op until `service_enabled` is emitted** (`canonical-pull.ts:160-163`).
- Read surface: **63 files / 204 query sites**, but ~57 are read-only; only ~6 files write (`app/(app)/{customers,sites,assets}/actions.ts` + maintenance import/paste). The `canonical_id`-mirror design means **read surfaces don't change** on a read-flip — they keep reading local tables fed from canonical.
- Migrated urjh → ehow on 2026-06-08 (Sprint 7). Docs/`CLAUDE.md` still saying `urjhmkhbgaxrofurpbgc` are **stale** — live wins.

### 2.3 EQ Quotes — the de-facto customer source today
- `public.sks_quotes_customers` (522, per-site rows, name-keyed, no DB-level master) is a write-through cache; the effective master write is a direct service-role dual-write into `ehow.app_data.customers` (`app/repositories/canonical_customers.py:136-258`) with name-ILIKE dedupe (`:166-184`). 514 quotes rows collapse onto 118 distinct `app_data.customers`.
- A **second, redundant HTTP path** (`app/canonical_client.py:136` → `canonical-api`, outbox-backed) targets what Shell writes — intended for jvkn, which is **empty** for customers. Stale; should be retired or made authoritative (not both).

### 2.4 The data-quality gate
- `app_data.customers`: at the 2026-06-07 audit, 389 rows / 270 distinct names / **117 duplicate-name groups**, **ABN 0/520**. Partial cleanup since (38 stub dups retired, 28 quotes linked) → ≈266 live now, but residual dup groups remain. The 140 Workbench-CSV rows are matched by **zero** Quotes rows (name-string drift) — cross-source dedupe is incomplete.
- **You cannot point Service at a master that shows "Equinix" three times.** Dedupe is the gating prerequisite.

---

## 3. Target architecture

```
NEW customer  ──upload/intake──▶  EQ Intake (dedupe at ingest)
                                       │  eq_intake_commit_batch_service
                                       ▼
                         app_data.customers / app_data.sites      ← CANONICAL SoR (sks-canonical / ehow)
                         app_data.assets (already Service-synced)
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 ▼ (same DB)           ▼ (same DB)            ▼ (cross-DB: EQ demo)
   app_data.service_customers   app_data.service_sites    canonical-pull (existing)
   (security_invoker view)      (security_invoker view)   upsert by canonical_id
                 │                     │
                 ▼                     ▼
      EQ Service reads (lists, dashboard, check creation, reports, portal)
      EQ Service workflow tables (checks/tests/defects/job_plans) stay Service-owned,
      FK to canonical-sourced site/asset ids via the view/mirror.
```

- **Read path (SKS):** `security_invoker` bridge views `app_data.service_<entity>` aliasing canonical cols to the app-native names Service expects (pattern: `0050_field_sites_view.sql`). Authored in `eq-shell/supabase/tenant-migrations/`, applied via the One Pipe.
- **Read path (EQ demo, cross-DB):** the existing `canonical-pull` (flip `service_enabled` on once safe).
- **Write path:** new customers → Intake only; sites/assets → write-through `canonical-api` (Service's `canonical-sync.ts` already does this); canonical row authoritative, local row a cache.

---

## 4. The gating prerequisite — customer dedupe

Nothing in §5 Phase 3+ is safe until `app_data.customers` is clean.

- **Owner:** EQ Intake multi-signal dedupe (name normalisation + ABN + site/contact overlap + source), per the "Dedupe Is Intake's Job" decision. Not per-app UI dedupe.
- **Human-in-the-loop:** merging live SKS customer rows is a customer-data migration — **Royce approves merges** (global non-negotiable). No auto-merge of ambiguous groups.
- **First deliverable (safe, read-only):** a merge-candidate report — the residual duplicate-name groups with signals (name, ABN, address, #sites, #contacts, source, has-quotes, has-service-rows) — as the review artifact. *(Claude can produce this on request; it only reads.)*
- **Backfill ABNs** where derivable (Quotes/Workbench) to give dedupe a hard key beyond name.

---

## 5. Phased plan

| Phase | What | Owner | Gate | Risk |
|---|---|---|---|---|
| **1** | Ratify SoR = sks-canonical `app_data` | Royce | — | ✅ done (this doc) |
| **2** | Dedupe `app_data.customers` (residual groups, backfill ABN) | Intake + Royce-approved merges | P1 | the long pole; reversible per-merge with snapshots |
| **3** | Lock write-ownership: Intake = sole customer writer; sites/assets write-through; retire Quotes' stale HTTP path; flip Quotes off local-first | decision (D2) + cutover across eq-quotes-port / eq-service | P2 | medium; touches 2 repos |
| **4** | Service read-flip: `service_customers`/`service_sites` bridge views (eq-shell One Pipe); repoint Service reads; assets already canonical | Claude + Royce-dispatched migration | P3 | low — pattern proven (Field) |
| **5** | Byproduct: wizard collapses to workflow steps; greeting via real name in bridge token | Claude | P4 (greeting independent — bankable anytime) | low, reversible |
| **6** | Soak, then decommission Service's local `customers`/`sites` tables | Claude + Royce | P5 soak | deferred |

---

## 6. Decisions still needed (Royce)

- **D1 — Customer SoR.** ✅ Ratified: sks-canonical `app_data.customers`.
- **D2 — Write-ownership strictness.** Recommended: new customers via Intake **only** (Service `createCustomerAction` retired/redirected); sites/assets keep write-through to canonical-api; Quotes drops local-first + retires the redundant HTTP path. *Confirm or soften.*
- **D3 — Dedupe execution.** Confirm Intake multi-signal + Royce-approved merges (vs a one-off reviewed script). Confirm ABN backfill sources.
- **D4 — EQ demo tenant.** Bridge views are SKS-only (same-DB). EQ demo (separate project) uses the existing `canonical-pull`. Confirm SKS-first, EQ-later sequencing.
- **D5 — Wizard end-state.** After the read-flip, keep the workflow-only checklist (plan→schedule→run) as a dismissible chip, or drop it entirely on the embedded path? (Pre-flip interim: land on dashboard, demote checklist.)

---

## 7. Governance (non-negotiable)

Per `SCHEMA-GOVERNANCE.md` — **One Spine, One Pipe, One Guard**: all tenant/canonical schema (including the bridge views in Phase 4) is authored **only** in `eq-shell/supabase/tenant-migrations/` and applied **only** via `migrate-tenants.mjs` (gated CI, Royce-dispatched). `check-tenant-drift.mjs` fingerprints the result. **No hand-applied single-tenant SQL — explicitly including Claude.** The MCP `apply_migration`/`execute_sql` against ehow is for **read-only verification + the (Royce-approved) data dedupe**, never schema.

---

## 8. Risks / open uncertainties

- `service_enabled` emission by `canonical-api` (gates the cross-DB pull for EQ demo) — verify before Phase 4 EQ-side.
- Exact live `app_data.customers` count + residual dup-group count drift (266 vs 389 across snapshots) — re-verify at Phase 2 start.
- `client_groups` (ehow `service` schema) vs `app_data.customers` — confirm it isn't a third parallel customer notion before the flip.
- Two Quotes write paths must not both run during cutover (the `canonical_id` could flip target) — sequence Phase 3 carefully.
- Bridge-view column aliasing must match every name Service's 57 read sites expect — diff the view against `public.customers`/`sites` columns before repointing.

---

## Appendix — load-bearing references

- Service consumption rails: `eq-solves-service/lib/canonical-{sync,pull,outbox,reconcile}.ts`; migrations `0113`, `0125`, `0122`; `app/(app)/dashboard/page.tsx`, `0100_get_dashboard_counts.sql`.
- canonical-api: `eq-shell/netlify/functions/canonical-api.ts` (resources L160-300, ACL L110-135, auth L81-101); `_shared/tenant-routing.ts`.
- Quotes: `eq-quotes-port/app/repositories/canonical_customers.py:136-258`; `app/canonical_client.py:136`; `app/canonical_outbox.py`.
- Governance + patterns: `eq-shell/supabase/tenant-migrations/0001_baseline.sql`, `0050_field_sites_view.sql`, `SCHEMA-GOVERNANCE.md`; `eq-context` `ops/decisions.md` (conduit thesis 2026-05-19), `cross-app-linkage-sprint-2026-06-07.md`, `contract-scope-canonical-design-2026-06-15.md`.

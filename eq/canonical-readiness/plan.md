---
title: EQ Canonical Layer — Readiness Plan
owner: Royce Milmlow
last_updated: 2026-05-27
scope: Bring eq-canonical (jvknxcmbtrfnxfrwfimn) to the shape needed to host EQ Intake, EQ Field, and EQ Quotes as first-class canonical-backed modules. Captures the gap matrix per app, sequences the schema + RPC + storage work, and surfaces architectural prerequisites (mega-RPC decomposition, schema split, per-tenant data plane decision) that get more expensive every week they're deferred.
read_priority: critical
status: live
---

# EQ Canonical Layer — Readiness Plan

**Status:** EXECUTED 2026-05-20 (autonomous push). All 6 work units shipped (1 → 2 → 3 → 4 → 5 → 7). Canonical now hosts 42 entities across 5 modules (core=3, field=30, cards=1, quotes=7, service=1), split into shell_control + app_data schemas with per-domain RPCs, unwinders, and registry-driven Intake UI landing pages. See §"Execution record" for the migration log.

This plan generalises the Cards §18 close-out (see
[`eq/cards/canonical-migration/plan.md`](../cards/canonical-migration/plan.md))
across all three apps queued to land on canonical: **Intake** (engine
already operating, needs schema breadth + UI generalisation), **Quotes**
(clean greenfield, 6 new tables, Flask v1 is the executable spec), and
**Field** (largest schema delta, code surface biggest, auth-bridge
already designed in Phase 1.F).

Single source of truth. Update when decisions change. Date + signature
every revision.

---

## TL;DR

- **Phase 1.F shipped** → identity is settled. RLS reads
  `app_metadata.tenant_id`. `mint-supabase-jwt` is live. Auth is no
  longer a blocker for any port.
- **Canonical today** = control plane (4 tables) + Cards spine (2
  tables) + Intake plumbing (registry, events, audit, RPCs) + **13
  entity tables, 11 of which are 0 rows** and have never been validated
  against the apps that will eventually write to them.
- **Three ports queued.** Intake (easy — engine operates, needs schema
  breadth). Quotes (medium — clean greenfield, no existing Quotes data
  to migrate). Field (hardest — ~25 new tables, complex code surface,
  auth-bridge separate concern).
- **Two architectural prerequisites block all three.**
  `eq_intake_commit_batch` is a mega-dispatch RPC that will choke at
  5+ module branches; needs decomposition before more entities land.
  Schema split (`shell_control.*` / `app_data.*`) is cheap now and
  ~3-week-painful later.
- **One strategic prerequisite still soft.** Per-tenant data plane vs
  shared canonical — memory says per-tenant, reality is shared. Needs
  reaffirmation before SKS or any second tenant is provisioned.
- **This plan sequences 7 work units.** Units 1+2+3 are prerequisites.
  Units 4+5+6 are per-app schema additions. Unit 7 broadens the
  Intake UI to expose every domain.

---

## Why now (overriding documented "wait")

Three substrate signals previously parked broader canonical work. Each
is now an *unblock*, not a continuing block:

| Signal | Where | Why it's unblocked now |
|---|---|---|
| "INTAKE Sprint-1 will reshape the data model" | `eq/products.md` (pre-2026-05-19) | Phase 1.E (2026-05-19) consolidated onto eq-canonical. Data model decision *is* locked. The pre-reshape caveat no longer applies |
| "Phase 2 paused pending GTM gate" | `eq/pending.md` "EQ Shell + EQ Intake" | The GTM gate applies to *new shell modules* (new product surfaces). Canonical entity readiness is the *substrate* those modules need; gating the substrate behind the gate creates a chicken-and-egg trap |
| "Canonical schema is empty / never validated" | This plan's discovery | The 11 empty tables ARE the work to validate. Doing it while empty is cheap; doing it after Field starts writing is expensive |

And one positive trigger:

- **Cards canonical-migration §18 demonstrates the worked pattern.** It
  generalised cleanly from "move one product's data into canonical" to
  "every product follows this template". This plan is that
  generalisation written down.

---

## Decisions locked (2026-05-20)

All six decisions resolved this session. Each is captured here with
the locked choice + rationale. **Plan body below reflects these
choices.**

| # | Marker | Decision | Choice | Rationale |
|---|---|---|---|---|
| 1 | Prereq A | Decompose `eq_intake_commit_batch`? | **Decompose now** | 1-2 days now is cheaper than 30+ inline CASE branches across Units 4 + 5. Backwards-compatible router preserves external API. |
| 2 | Prereq B | Schema split? | **Split now (Unit 2)** | 1 day now vs ~3 weeks later (per 2026-05-20 part-d critique). Every new Unit 4 + 5 table lands in `app_data.*` first time. |
| 3 | Prereq C | Per-tenant data plane? | **Reaffirm per-tenant** | Memory holds. Every entity migration ships into both `jvknxcmbtrfnxfrwfimn` (for `core`) AND the `pnpm db:apply` template applied per new tenant Supabase. SKS provisioning will exercise this path. |
| 4 | Unit 1 | Existing 11 empty canonical tables | **Audit-and-reshape** | Preserves the @eq/schemas + registry investment. Unit 1 produces column-level diff; Unit 2 absorbs reshape into the schema-split migration. |
| 5 | Unit 4 | Quotes naming convention | **Canonical-conform** | `quote`, `quote_line_item` (separate table, not JSONB), share `customer` from core. Drops the `sks_quotes_` prefix that doesn't belong in multi-tenant canonical. React rewrite carries a one-shot mapping layer to Flask v1 shape. |
| 6 | Unit 5 | Field domain sequencing | **One big push** | Single migration `2026_05_NN_field_domain.sql` with all ~25 Field tables. Higher single-migration risk; one review pass, one commit, one substrate update. Justified by: all tables additive + empty, no data migration concerns. **Refinement (2026-05-20 review):** the .sql file has internal section markers (`-- GROUP 1: CORE FIELD TABLES`, etc.) + a table-of-contents at the top so the review pass is tractable (~half-day). |

### Plan-review refinements (2026-05-20)

Six additional clarifications captured during the post-locking review
pass with Royce:

- **Unit 5 file structure** — single .sql with internal section breaks +
  TOC, not 4 separate files.
- **Quote line items** — confirmed separate `app_data.quote_line_item`
  table (not JSONB on header). Removes Flask v1 design-decision-1
  ambiguity that was sitting in §Open questions.
- **Per-tenant deployment is template-first.** Every migration in
  Units 2-5 lands in `eq-intake/eq-platform/scripts/db-apply.ts`
  bundle **first**; the bundle is applied via `pnpm db:apply` to every
  tenant Supabase (including `core` on `jvknxcmbtrfnxfrwfimn`). No
  drift between tenants. `apply_migration` MCP is used only for
  ad-hoc one-off ops, not for canonical schema changes.
- **App config — separate.** Field-specific tenant toggles live in
  `app_data.tenant_app_config`; `shell_control.module_entitlements`
  stays scoped to "which modules a tenant has bought". Clean
  separation of concerns.
- **Entity re-labelling.** prestart, toolbox_talk, swms, jsa, itp,
  incident move from `module='cards'` → `module='field'` in
  `eq_schema_registry`. Cards has exactly one canonical entity
  (`licence`); everything else is Field-domain. Re-label migration
  lands in Unit 2. Rationale: Field is the primary writer of safety
  registers; Cards is one mobile capture surface among several
  (Field web, future EQ Capture OCR, future QR site scanner).
- **Multi-app write architecture — phased path.** Phase 1 (now → ~12
  months): option (a). Every app calls its per-domain RPC directly.
  Each per-domain RPC accepts `p_intake_mode text` parameter
  (`'strict'` | `'lenient'` | `'ocr-best-effort'`); `@eq/validation`
  applies tier-specific rules. Apps identify themselves via
  `app_metadata.source_app` JWT claim; this gets recorded in a new
  `source_app text` column on `eq_intake_events`. Phase 1.5 (when an
  app needs per-app pre-write logic): add a facade RPC for that one
  app. Phase 2 (when 5+ apps write canonical): add an
  `allowed_writers (app_id, entity, write_mode)` control table for
  declarative grant management. Both Phase 1 additions
  (`p_intake_mode` + `source_app`) land in Unit 3.

---

## Architectural model after readiness

```
                  ┌─────────────────────────────────────────────────────┐
                  │  eq-canonical (jvknxcmbtrfnxfrwfimn) — ap-southeast-2 │
                  │                                                     │
                  │  ┌──────────────────────────────────────────────┐   │
                  │  │  shell_control.*   (auth & tenancy plane)    │   │
                  │  │  tenants  users  module_entitlements         │   │
                  │  │  user_invites  eq_schema_registry            │   │
                  │  │  eq_intake_templates  eq_intake_events       │   │
                  │  │  eq_intake_row_audit  eq_export_*            │   │
                  │  └──────────────────────────────────────────────┘   │
                  │                                                     │
                  │  ┌──────────────────────────────────────────────┐   │
                  │  │  app_data.*  (canonical entity layer)        │   │
                  │  │                                              │   │
                  │  │  core      → customer  contact  site         │   │
                  │  │  field     → staff  schedule  timesheet      │   │
                  │  │              leave_request  leave_balance    │   │
                  │  │              tender  tender_enrichment       │   │
                  │  │              nomination  nomination_clash    │   │
                  │  │              site_diary  weekly_report       │   │
                  │  │              apprentice_profile  + 6 sat.    │   │
                  │  │              prestart_check  toolbox_talk    │   │
                  │  │              swms  jsa  itp_record  incident │   │
                  │  │  cards     → licence                         │   │
                  │  │  quotes    → quote  quote_line_item          │   │
                  │  │              quote_status_history            │   │
                  │  │              quote_attachment  scope_template│   │
                  │  │              rate_library  quote_email_outbox│   │
                  │  │  service   → asset                           │   │
                  │  └──────────────────────────────────────────────┘   │
                  │                                                     │
                  │  ┌──────────────────────────────────────────────┐   │
                  │  │  RPC dispatch (decomposed)                   │   │
                  │  │  eq_intake_commit_batch  → router            │   │
                  │  │    ↳ _commit_batch_core                      │   │
                  │  │    ↳ _commit_batch_cards                     │   │
                  │  │    ↳ _commit_batch_field                     │   │
                  │  │    ↳ _commit_batch_quotes                    │   │
                  │  │    ↳ _commit_batch_service                   │   │
                  │  │  + shared private fns (tenant check, event,  │   │
                  │  │    audit, metadata injection)                │   │
                  │  └──────────────────────────────────────────────┘   │
                  │                                                     │
                  │  RLS: app_metadata.tenant_id (Phase 1.F sweep)      │
                  │  Auth: Supabase native JWT minted by shell          │
                  └─────────────────────────────────────────────────────┘
```

Every Intake / Field / Quotes module gets the same shape: schema
registered in `eq_schema_registry`, table in `app_data.<entity>`,
writes via `eq_intake_commit_batch_<domain>`, reads via direct
PostgREST with RLS enforcing tenant scope.

---

## Current canonical inventory (2026-05-20)

### Control plane (shell concern)

`tenants`, `users`, `module_entitlements`, `user_invites`

### Intake plumbing

`eq_schema_registry` (13 entries, listed below), `eq_intake_templates`,
`eq_intake_events` (2 rows from prior commits), `eq_intake_row_audit`,
`eq_export_events`, `eq_export_profiles`

### RPCs

- `eq_intake_commit_batch(p_intake_id, p_tenant_id, p_table, p_rows, p_confirm_replace=false)` — SECURITY DEFINER, mega-dispatch
- `eq_intake_find_template_by_signature` — SECURITY DEFINER
- `eq_intake_rollback` — SECURITY DEFINER
- Trigger fns: `eq_intake_template_track_outcome`, `eq_intake_template_track_use`, `eq_schema_registry_one_current`, `eq_set_imported_at`

### Entity tables registered (13)

**Module labels reflect the plan-review re-labelling (2026-05-20):**
prestart/toolbox_talk/swms/jsa/itp/incident moved from `cards` → `field`
since Field is the primary writer for safety registers; Cards is one
mobile capture surface among several (Field web, future EQ Capture
OCR, future QR site scanner). The registry re-label migration is part
of Unit 2.

| Entity | Module (after re-label) | Table state | Schema in @eq/schemas | RPC dispatch case | Notes |
|---|---|---|---|---|---|
| customer | core | empty | yes | yes | Shared root; Quotes + Field + Service all FK here |
| contact | core | empty | yes | yes | Shared root |
| site | core | empty | yes | yes | Shared root |
| staff | field | 0 rows | yes | yes (Cards Unit 2.A) | Shared root for Field + Cards |
| schedule | field | empty | yes | unknown — verify in Unit 1 | Field's daily allocation atomic unit |
| prestart | field (was cards) | empty | yes | unknown | Field's `prestarts` + `prestarts.photos` write here today. Cards-mobile is one capture surface |
| toolbox_talk | field (was cards) | empty | yes | unknown | Field writes these on its own Supabase today |
| swms | field (was cards) | empty | yes | unknown | |
| jsa | field (was cards) | empty | yes | unknown | |
| itp | field (was cards) | empty | yes | unknown | |
| incident | field (was cards) | empty | yes | unknown | |
| licence | cards | empty (pending Cards Unit 3 data migration) | yes | yes (Cards Unit 2.A) | Cards-only entity. Field reads to check tickets but doesn't write |
| asset | service | empty | yes | unknown | EQ Service entity — port not in this plan's scope |

**RPC dispatch unknown for 9 of 13** — this is a Unit 1 audit task.
Verify which entities the current `eq_intake_commit_batch` actually
routes (vs which were only added to the table whitelist) by reading
the migration history (specifically 006 + 008 + Phase 1.F migrations).

---

## Gap matrix per app

### EQ Intake — engine operating, surface narrow

**Current state.** `@eq/intake` + `@eq/validation` + `@eq/confirm-ui`
vendored into `eq-shell/eq-intake/eq-platform/`. SimPRO fixtures
validated end-to-end through parser + customer/contact/site mapping +
commit (267 customers / 393 contacts / 544 sites). Live at
`/core/intake`. 13 schemas registered.

**Gaps:**

1. **Generic single-entity dropzone UI.** Today's IntakeModule has
   three SimPRO-specific surfaces hardcoded to customer/site/contact
   (`QuickExportSection`, `RollupDropZone`, `CanonicalCommitSection`).
   Cards Unit 2.B deferred the generic version. Until it lands, every
   new entity needs bespoke shell UI.
2. **Schema breadth — domain-specific schemas missing.** Field's
   timesheets / leave / tender / diary entities have no schema JSON
   in `@eq/schemas`. Quotes' quote / line-item / scope-template
   entities likewise. Until schemas exist, those entities can't be
   intake'd at all.
3. **Per-domain landing pages.** Intake home shows one drop zone.
   Should surface by domain: `/core/intake/field` (CSV imports of
   timesheets / leave / tender), `/core/intake/quotes` (template
   imports of scope library / rate library), `/core/intake/cards`
   (licence / prestart / toolbox import for HR onboarding). The
   `module` column in `eq_schema_registry` already supports this
   grouping.

**Effort to "ready":** Unit 7 = ~2 days. Output is a generic
`<DomainImportSection>` + 4 domain landing pages + the discovery
pattern (`registry where module = X and is_current = true`).

### EQ Quotes — clean greenfield

**Current state.** Flask v1 operating at `https://quotes.eq.solutions`
against `nspbmirochztcjijmcrx` (sks-labour Supabase). 6 migrations on
disk in `C:\Projects\eq-quotes\eq-quotes-port\migrations\`. Per
`eq/products.md`, the Flask v1 is the *executable spec*, not the
target shape — the React rewrite lands on canonical and Flask v1 is
deprecated.

**Entity inventory (from migration 001):**

| Flask v1 table | Canonical target | Notes |
|---|---|---|
| `sks_quotes` (header) | `app_data.quote` | Lowercase enum status taxonomy already in place; carry forward |
| `sks_quotes_customers` | *(use shared `app_data.customer`)* | Quotes uses customer-master; canonical's `customer` already covers this |
| `sks_quotes_rates` | `app_data.rate_library` | Curated rate library, tenant-scoped |
| `sks_quotes_materials` | `app_data.material_library` (or merge into rate_library?) | **Open question** — Flask v1 keeps them separate; canonical decision pending |
| `sks_quotes_vocab` | `app_data.scope_template` | Reusable scope items / phrase library |
| `sks_quotes_documents` | `app_data.quote_document` | Generated Word/PDF outputs |
| `sks_quotes_status_history` | `app_data.quote_status_history` | Status-change audit trail |
| `sks_quotes_config` | *(use `module_entitlements` + tenant settings)* | Tenant-level toggles — not a per-quote concern |
| (line items, JSONB on header per design decision 1) | `app_data.quote_line_item` (separate table OR keep as JSONB?) | **Open question** — decision 1 of Flask v1 said JSONB; canonical convention favours separate table for query-ability + indexing |

**Gaps:** *all of the above* — none exist in canonical today.

**Effort to "ready":** Unit 4 = ~2 days. Greenfield migrations only;
no data migration (Flask v1 stays on sks-labour through its lifetime).

### EQ Field — biggest delta

**Current state (clarified 2026-05-20 review):** The `eq-solves-field`
Supabase (`ktmjmdzqrogauaevbktn`) is Royce's dev/demo environment with
**no real users**. SKS NSW Labour (the production version on
`nspbmirochztcjijmcrx`) is a **separate commercial entity** — not part
of the EQ canonical port. So Field's migrations on disk serve as a
**schema reference for canonical-readiness, not a migration source**.

No data migration, no dual auth, no surface-by-surface replacement
applies. Canonical-readiness for Field = build the tables + schemas +
RPCs in canonical so EQ Solutions' next-generation Field module(s)
can be built fresh inside the shell, backed by canonical. SKS stays
on its own infrastructure indefinitely.

**Entity inventory (from `C:\Projects\eq-solves-field\migrations\*.sql`):**

**Already canonical-shaped (verify in Unit 1):**
- sites → exists in canonical
- people → maps to `staff` in canonical
- schedule → exists in canonical
- prestarts + prestarts.photos → maps to `prestart_check` in canonical
- toolbox_talks → maps to `toolbox_talk` in canonical
- swms, jsa, itp_records, incidents, assets → exist in canonical

**Missing from canonical (Unit 5 adds):**

| Field table | Canonical target | Sub-unit |
|---|---|---|
| `timesheets` | `app_data.timesheet` | 5.A |
| `leave_requests` | `app_data.leave_request` | 5.A |
| `leave_balances` | `app_data.leave_balance` | 5.A |
| `app_config` | `app_data.tenant_app_config` (or merge into `module_entitlements`?) | 5.A |
| `managers` | *(use `staff.role IN ('manager','supervisor')`)* — likely redundant once role is canonical | 5.A |
| `checkins` | `app_data.checkin` | 5.A |
| `tenders` | `app_data.tender` | 5.B |
| `tender_enrichment` | `app_data.tender_enrichment` | 5.B |
| `nominations` | `app_data.tender_nomination` | 5.B |
| `nomination_clashes` (view) | `app_data.tender_nomination_clash` (view) | 5.B |
| `tender_import_runs` | `app_data.tender_import_run` | 5.B |
| `tender_review_decisions` | `app_data.tender_review_decision` | 5.B |
| `pending_schedule` | `app_data.pending_schedule` (or drop per pending.md open item) | 5.B |
| `site_diaries` | `app_data.site_diary` | 5.C |
| (weekly_reports — planned, not built) | `app_data.weekly_report` | 5.C |
| `apprentice_profiles` | `app_data.apprentice_profile` | 5.D |
| `skills_ratings` | `app_data.skills_rating` | 5.D |
| `feedback_entries` | `app_data.feedback_entry` | 5.D |
| `rotations` | `app_data.rotation` | 5.D |
| `buddy_checkins` | `app_data.buddy_checkin` | 5.D |
| `quarterly_reviews` | `app_data.quarterly_review` | 5.D |
| `engagement_log` | `app_data.engagement_log` | 5.D |
| `tafe_day_and_holidays` | `app_data.tafe_calendar` (or apprentice-domain table?) | 5.D |
| `ts_reminders_sent`, `rate_limit_buckets` | *(stay on Field's Supabase — auth/ops plumbing, not app data)* | n/a |

**Auth model.** No conflict to bridge. Shell login at `core.eq.solutions`
(Phase 1.F's 5-tier role + platform_admin model) is the only login for
canonical-backed shell modules. Field's `tenant_pin` + custom HMAC
token + plaintext PIN compare is purely legacy infrastructure for the
demo deployment that has no real users.

**Effort to "ready":** Unit 5 = 3-5 days split across 4 sub-units. Each
sub-unit independently shippable, substrate commit between each.

---

## Architectural prerequisites

### Prereq A — Decompose `eq_intake_commit_batch`

**Today.** Single SECURITY DEFINER RPC. Hardcoded table whitelist + a
per-entity `CASE WHEN p_table = '<entity>' THEN ...` dispatch. Already
contains branches for customer, contact, site, staff, licence (added
in Cards Unit 2.A migration 006).

**Cost of adding more branches inline.** With Field (~25 entities) +
Quotes (~7 entities) ahead, dispatch CASE grows to 35+ branches in
one function body. Per-entity validators inline instead of in
`@eq/validation`. Single function = single point of failure for all
writes. Deploy/rollback coupling: any new entity requires modifying
the same function, no granular rollback.

**Decomposition proposal.**

```
PUBLIC (callable from PostgREST):
  eq_intake_commit_batch(p_intake_id, p_tenant_id, p_table, p_rows,
                          p_confirm_replace, p_intake_mode='strict')
    -- looks up target entity's module via eq_schema_registry
    -- dispatches to the appropriate per-domain commit fn

PUBLIC per-domain (also callable directly for module-aware clients):
  eq_intake_commit_batch_core   (..., p_intake_mode)  -- customer, contact, site
  eq_intake_commit_batch_field  (..., p_intake_mode)  -- staff, schedule, timesheet, prestart, toolbox_talk, swms, ...
  eq_intake_commit_batch_cards  (..., p_intake_mode)  -- licence (only)
  eq_intake_commit_batch_quotes (..., p_intake_mode)  -- quote, quote_line_item, ...
  eq_intake_commit_batch_service(..., p_intake_mode)  -- asset

PRIVATE shared library (SECURITY DEFINER, not callable directly):
  _eq_intake_check_tenant_match(p_tenant_id, p_rows)
  _eq_intake_inject_metadata(p_intake_id, p_rows, p_source_app)
  _eq_intake_record_event(p_intake_id, p_status, p_summary, p_source_app)
  _eq_intake_record_row_audit(p_intake_id, p_entity, p_row, p_outcome)
```

**`p_intake_mode` parameter:** each per-domain RPC accepts a mode
enum that drives validation strictness. `'strict'` = full validation
(live mobile capture). `'lenient'` = optional-fields-allowed
(bulk backfill of existing registers). `'ocr-best-effort'` = future
EQ Capture path where OCR extraction may miss fields.
`@eq/validation` applies tier-specific schema rules per entity.

**`source_app` audit attribution:** new column on `eq_intake_events`.
Populated from `app_metadata.source_app` JWT claim. Apps identify
themselves: Cards-iframe sets `source_app='cards'`, Field-iframe sets
`source_app='field'`, shell-Intake-UI sets `source_app='shell'`, etc.
Audit log records which UI initiated the write even though all writes
go through canonical's per-domain RPCs.

Backwards-compatible. `eq_intake_commit_batch` keeps its existing
positional signature; `p_intake_mode` defaults to `'strict'` so
existing callers (the SimPRO surface) continue to work without change.

**Effort.** ~1-2 days for the decomposition migration + tests.

### Prereq B — Schema split (`shell_control.*` / `app_data.*`)

**Today.** Everything in `public`. Future regional secondary day,
replication scope decisions, GDPR data classification — all forced to
be per-table instead of per-schema.

**Split.**

| Schema | Contents | Purpose |
|---|---|---|
| `shell_control` | tenants, users, module_entitlements, user_invites, eq_schema_registry, eq_intake_templates, eq_intake_events, eq_intake_row_audit, eq_export_events, eq_export_profiles | Auth, tenancy, intake plumbing. Stays in primary region. Owned by the shell. |
| `app_data` | All canonical entity tables (existing 13 + everything Unit 4 + 5 adds) | Tenant business data. Future regional sharding target. |

**Effort.**

- `CREATE SCHEMA shell_control; CREATE SCHEMA app_data;`
- `ALTER TABLE public.<t> SET SCHEMA <new_schema>;` × ~24 tables
- Update RLS policy definitions (`auth.jwt() -> 'app_metadata' ->> 'tenant_id'` predicate is schema-agnostic, but policy *names* are schema-scoped — recreate per schema)
- Update `search_path` on `authenticated`, `service_role`, `anon`
  roles to `app_data, shell_control, public, extensions`
- Update vendored `@eq/*` code where SDK can't infer schema (rare —
  PostgREST handles `Accept-Profile` / `Content-Profile` headers)
- Update the dispatcher RPC + per-domain RPCs to reference schema-qualified table names

**Cost now: 1 day.** Cost in 12 months (per 2026-05-20 part-d
critique): ~3 weeks. Doing it before Unit 4 + 5 means every new table
lands in the right schema first time.

### Prereq C — Per-tenant data plane decision

**Memory says** (per `supabase-architecture-decision.md` Phase 1.E):
"one Supabase per tenant, control tables co-located with app data, no
separate control plane."

**Reality today.** `core` is the only tenant. All data on
`jvknxcmbtrfnxfrwfimn`. Pending.md flags `sks-canonical-eq` as
"planned, not provisioned. Gated on GTM validation gate, not on shell
readiness."

**Decision needed before Unit 4 + 5 starts.** Three options:

| Option | What | Trade-off |
|---|---|---|
| (a) Reaffirm per-tenant — `pnpm db:apply` clones schema into each new tenant's Supabase | Memory-consistent, max data isolation, multi-deploy per schema change | Operational cost compounds with tenant count |
| (b) Shift to shared canonical — all tenants on jvknxcmbtrfnxfrwfimn, RLS as only boundary | Cheaper ops, one schema migration covers all tenants | Blast radius conflation, per-tenant compliance harder |
| (c) Hybrid — pilot/free tenants share; paying/enterprise get own project | Best of both, complexity of two patterns | Two operational paths to maintain |

**Default (this plan):** (a). Every entity migration ships into both
`jvknxcmbtrfnxfrwfimn` (for `core`) AND into the `pnpm db:apply`
template that gets applied when a new tenant's Supabase is provisioned.

**Surface this to Royce — if (b) or (c) is the right answer, every
Unit 4 + 5 migration's deployment story changes.**

---

## Work units

Order is canonical: 1 → 2 → 3 → 4 → 5 → 7. (Unit 6 is out of scope —
EQ Service port deferred.) Each unit ships an independent, verifiable
deliverable. Substrate commit between each.

### Unit 1 — Audit existing 11 empty canonical tables vs Field code

**Owner:** Claude Code (Royce reviews findings before reshape decisions)
**Effort:** 1 day
**Risk:** low — no DDL, audit only

Deliverable: `eq/canonical-readiness/audit-existing-tables.md` with a
column-level diff per table. For each of {asset, contact, customer,
incident, itp_records, jsa_records, prestart_checks, schedule_entries,
sites, swms, toolbox_talks} — and the registry-tracked-but-different
{staff, schedule, licence, prestart, toolbox_talk} — compare:

| Column dimension | Canonical | Field expects | Quotes expects | Decision needed? |

Plus for each table:
- Whether `eq_intake_commit_batch` actually has a dispatch case
- Whether RLS policies are tenant-scoped via `app_metadata.tenant_id` (1.F sweep should have covered, but verify)
- Whether storage bucket exists for entities that need photos
- Indexes — are read-paths covered?

**Output drives.** Reshape migrations land in Unit 2 (alongside the
schema split, so we don't migrate the same table twice). Any table
that's *wrongly modelled* gets dropped + replaced; any table that's
*missing columns* gets ALTERed.

### Unit 2 — Schema split + reshape

**Owner:** Claude Code (Royce reviews + approves migration before apply)
**Effort:** 1 day (split) + variable (reshapes from Unit 1) = ~1-2 days total
**Risk:** medium — RLS policy recreation is the error-prone bit

Single migration `2026_05_NN_schema_split_and_reshape.sql`:

1. `CREATE SCHEMA shell_control; CREATE SCHEMA app_data;`
2. `ALTER TABLE public.<t> SET SCHEMA <target>;` per audit
3. Drop & recreate RLS policies in new schemas (predicates unchanged)
4. Update `search_path` on roles
5. Apply Unit 1 reshape findings (column adds/drops/type changes)
6. Recreate views (e.g. `nomination_clashes` if it already exists)

Plus vendored `@eq/*` code update where schema-qualification needs
explicit handling (review case by case).

**Test.** Existing Intake commits still succeed against
`app_data.customer` / `app_data.contact` / `app_data.site`. Shell
session lookup still works against `shell_control.tenants` /
`shell_control.users`. RLS still enforces tenant scope.

### Unit 3 — Decompose `eq_intake_commit_batch`

**Owner:** Claude Code (Royce reviews)
**Effort:** 1-2 days
**Risk:** medium — touches the write path of every intake operation

Migration `2026_05_NN_decompose_intake_commit_batch.sql`:

1. Create private shared library functions (4 of them)
2. Create per-domain commit functions (5 of them — one per `module`
   value in `eq_schema_registry`)
3. Rewrite the public `eq_intake_commit_batch` as a thin router that
   looks up `eq_schema_registry.module` for the target entity and
   dispatches
4. Drop the old CASE-statement body (now in the per-domain functions)

**Test.**

- Existing SimPRO commit flow on `/core/intake` still succeeds
- Cards licence commit (via Cards Unit 2.A) still succeeds
- Per-domain direct call (e.g. `eq_intake_commit_batch_field`) works
  for module-aware clients
- Rollback still works for both router-routed and direct-call paths

### Unit 4 — Quotes domain (greenfield, ~7 tables)

**Owner:** Claude Code (Royce reviews migration SQL before apply)
**Effort:** 2 days
**Risk:** low — additive only, no existing data, Flask v1 unaffected

Deliverable:

- Migration `2026_05_NN_quotes_domain.sql` adding `app_data.quote`,
  `app_data.quote_line_item`, `app_data.quote_status_history`,
  `app_data.quote_attachment`, `app_data.scope_template`,
  `app_data.rate_library`, `app_data.quote_email_outbox`
- Schemas in `eq-intake/eq-platform/packages/eq-schemas/src/schemas/`:
  `quote.schema.json`, `quote-line-item.schema.json`,
  `scope-template.schema.json`, `rate.schema.json`
- `eq_intake_commit_batch_quotes` populated with dispatch for each
  entity
- RLS predicates (`tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid`)
- Storage bucket `tenant-{tenant_id}` (one bucket per tenant per 2026-05-20 review Q5). Path: `quotes/{quote_id}/{file}` within each tenant's bucket. RLS predicate scopes by bucket name + matches JWT tenant_id.
- Substrate update: `eq-quotes-port/docs/canonical-plugin-contract.md`
  extended with the canonical schema reference

**Out of scope.** Word doc generation server-side; that's a Quotes
React-rewrite concern. Email_outbox row writes only — sender daemon
is deferred. Stripe link is deferred (entitlement plumbing exists,
Stripe wiring not in this unit).

### Unit 5 — Field domain (one big push, ~25 tables)

**Owner:** Claude Code (Royce reviews the full migration before apply)
**Effort:** 3-5 days
**Risk:** medium-high — large surface, single migration is the
all-or-nothing review/apply gate. Mitigated by: all tables additive +
empty (no data migration concerns), no existing reads/writes to break.

Field's `ktmjmdzqrogauaevbktn` demo Supabase has no real users (per
2026-05-20 review clarification). Field's migrations are a *schema
reference* — Unit 5 ports the shape into canonical so EQ Solutions'
next-generation Field module(s) can be built fresh inside the shell.
No data migration, no dual operation. SKS NSW Labour stays separate.

Single migration `2026_05_NN_field_domain.sql` with all Field entities,
organised into logical groups within the file so review is tractable:

**Group 1 — Core Field tables (~5 tables)**

- `app_data.timesheet`
- `app_data.leave_request`
- `app_data.leave_balance`
- `app_data.checkin`
- `app_data.tenant_app_config` — Field-specific tenant toggles. Decision 4 locked it as separate from `module_entitlements`.

**`managers` table not migrated.** Field's `managers` table is
redundant once `staff.role` is canonical (Phase 1.F's 5-tier role).
The `digest_opt_in` columns from Field's managers migration land
directly on `staff` (per 2026-05-20 review Q2): `staff.digest_opt_in
boolean`, `staff.digest_cron_schedule text`.

**Group 2 — Tender cluster (~7 tables)**

- `app_data.tender`
- `app_data.tender_enrichment`
- `app_data.tender_nomination`
- `app_data.tender_nomination_clash` (view)
- `app_data.tender_import_run`
- `app_data.tender_review_decision`
- ~~`app_data.pending_schedule`~~ — **dropped (2026-05-20 review).**
  Per pending.md: pending_schedule is dead code on Field's Supabase
  (Confirm Curve writes direct to schedule). Not migrated to canonical.
  If staging-queue feature ever wanted, it's a future build, not a
  today migration.

Tender is the most recent Field workstream (v3.4.79+) — least
technical debt to inherit. Test fixtures exist via Field's Excel
ingestion path.

**Group 3 — Site reports v2 (~2 tables)**

- `app_data.site_diary`
- `app_data.weekly_report` (table created with v1 placeholder columns;
  Field's actual weekly report build is gated on Diary usage signal —
  schema exists ahead of UI)

Note: `prestart_check`, `toolbox_talk` already exist in canonical;
verify/reshape under Unit 1.

**Group 4 — Apprentice cluster (~7-8 tables)**

- `app_data.apprentice_profile`
- `app_data.skills_rating`
- `app_data.feedback_entry`
- `app_data.rotation`
- `app_data.buddy_checkin`
- `app_data.quarterly_review`
- `app_data.engagement_log`
- `app_data.tafe_calendar` (or fold into apprentice_profile? — decide
  during drafting)

**Unit 5 also delivers:**

- ~22 schemas in `eq-intake/eq-platform/packages/eq-schemas/src/schemas/`
- Dispatch for every Field entity in `eq_intake_commit_batch_field`
- RLS predicates (`tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid`)
- Indexes for known Field read paths (roster queries, timesheet
  burn-down, tender pipeline kanban)
- Storage uses the per-tenant bucket `tenant-{tenant_id}` (one bucket
  per tenant per 2026-05-20 review Q5). Paths: `field/prestart/{check_id}/...`,
  `field/toolbox/{talk_id}/...`, `field/diary/{diary_id}/...`. Same
  bucket as Quotes uses; RLS predicate scopes by bucket name + matches
  JWT tenant_id.
- Substrate updates: `eq/field/multi-tenancy/plan.md` Phase 2 section
  cross-link; `eq-field-app` repo gets `docs/canonical-mapping.md`

**Deferred (out of Unit 5's scope, but flagged for completeness):**

- ~~One-way Field → canonical sync trigger~~ — **obsolete (2026-05-20
  review).** Field demo has no users; no sync needed in either
  direction. Pending.md item to be retired.
- `ts_reminders_sent` and `rate_limit_buckets` — auth/ops plumbing
  specific to Field's PIN-based auth path. Not relevant to
  canonical's Supabase Auth model. Field demo retains these on its
  own Supabase for as long as the demo runs.

**Pre-apply checklist (for the single review pass):**

- [ ] All ~25 table DDLs reviewed by Royce
- [ ] All ~22 schema JSONs reviewed (entity names match table names)
- [ ] Dispatch in `eq_intake_commit_batch_field` covers every entity
- [ ] RLS predicates use `app_metadata.tenant_id` (1.F convention)
- [ ] No table named in Group 1-4 already exists in canonical (would
      mean Unit 1 audit missed it)
- [ ] Migration template path (`pnpm db:apply`) updated for the new
      tables — per Decision 3, this template gets applied to every new
      tenant Supabase

### Unit 6 — Service domain

**Out of scope for this plan.** EQ Service operates on
`urjhmkhbgaxrofurpbgc`, separately maintained, 80 Vitest tests, 22
sprints to date. Surfaced only because the `asset` entity is already
in `eq_schema_registry`. Add a Unit-6-equivalent when Service is
queued for canonical port.

### Unit 7 — Intake UI broadening

**Owner:** Claude Code
**Effort:** 2 days
**Risk:** low — UI surface only, no DB

Deliverable:

- Generic `<DomainImportSection>` React component (parameterised over
  schema + commit RPC + UI labels) — replaces the bespoke
  `LicenceImportSection` deferred from Cards Unit 2.B
- Per-domain landing pages: `/core/intake/field`, `/core/intake/quotes`,
  `/core/intake/cards`, `/core/intake/core`
- Registry-driven entity discovery: each landing page reads
  `SELECT entity, description FROM eq_schema_registry WHERE module = $1 AND is_current = true ORDER BY entity`
- Drop the bespoke SimPRO surfaces (`QuickExportSection`,
  `RollupDropZone`, `CanonicalCommitSection`) OR keep them as
  "SimPRO Customer Setup Flow" preset on `/core/intake/core` (probably
  the right call — generic + preset side-by-side)

---

## Trajectory after canonical-readiness lands

Once Units 1-5 + 7 are done, canonical is ready to back the next wave
of shell modules. The trajectory then:

1. **First Field module built in shell** — likely Tender Pipeline
   since it's the newest Field workstream with the cleanest data
   shape. Module reads/writes canonical via per-domain RPCs.
2. **Quotes React module build** — Position 4 in shell module queue,
   gated on Field demonstrating the pattern works.
3. **Additional Field modules** (roster, schedule, leave, audits,
   prestarts, toolbox talks) — each is a new shell module backed by
   canonical, *not* a port of existing Field code. Pattern reuse from
   Tender Pipeline build.
4. **Field demo Supabase (`ktmjmdzqrogauaevbktn`) eventually
   deprecated** — there are no users on it; Royce decides when to
   shut down vs leave running as historical reference.
5. **SKS Labour stays on its own infrastructure indefinitely** — not
   on this plan's roadmap.

The Quotes React rewrite happens after the first Field module
produces reusable shell-module patterns. Position 4 stays Position 4.

---

## Substrate updates required (after each unit)

After each unit lands:

- `eq/canonical-readiness/plan.md` (this file) — status update per unit
- `eq/changelog/eq-context.md` — entry per unit completion
- `eq/products.md` — update canonical entity inventory section (Phase 1.F sweep section grows)
- `eq/pending.md` — close architectural prereq items as each lands; replace with sub-unit checkboxes

After Unit 4:

- `C:\Projects\eq-quotes\eq-quotes-port\docs\canonical-plugin-contract.md`
  — extend with the canonical schema reference

After Unit 5.A → 5.D:

- `eq/field/multi-tenancy/plan.md` — Phase 2 section gets cross-link
  to canonical-readiness Unit 5 (Field's existing plan becomes the
  *surface migration* plan, this plan is the *substrate*)
- `eq-field-app` repo gets a `docs/canonical-mapping.md` documenting
  the Field-table → canonical-table mapping (one document, not per
  surface)

After Unit 7:

- `eq-shell` README intake section updated with the per-domain landing pages
- `eq/products.md` EQ Shell section "Modules in shell today" list updated

---

## Open questions (not blockers — surface during execution)

- ~~**Quotes line items: JSONB vs separate table?**~~ **Resolved
  2026-05-20:** separate `app_data.quote_line_item` table. React
  rewrite carries a mapping layer to Flask v1's JSONB shape.
- **Quotes materials vs rates: one library or two?** Flask v1 has them
  separate. Canonical decision pending — likely separate (different
  validation, different lifecycle).
- ~~**Field `app_config` vs `module_entitlements`?**~~ **Resolved
  2026-05-20:** separate. Field-specific toggles in
  `app_data.tenant_app_config`; shell-level access in
  `shell_control.module_entitlements`.
- ~~**`pending_schedule` fate?**~~ **Resolved 2026-05-20:** dropped.
  Dead code on Field's Supabase, not migrated to canonical.
- ~~**`managers` table sunset?**~~ **Resolved 2026-05-20:** sunset.
  `digest_opt_in` + `digest_cron_schedule` land on `staff` directly.
- ~~**Field surface-by-surface dual operation?**~~ **Resolved 2026-05-20:**
  obsolete framing. Field demo has no real users; canonical-readiness
  enables building EQ Solutions' next-generation Field modules fresh
  inside the shell. No data migration, no dual auth.
- **Field `managers` table:** likely redundant once `staff.role`
  ('manager' | 'supervisor' | 'employee' | 'apprentice' | 'labour_hire')
  is canonical. Confirm in Unit 5.A.
- **`pending_schedule` table:** pending.md flags this as "currently
  written but bypassed (Confirm Curve writes direct to schedule).
  Decide fate — promote or drop." Decide before Unit 5.B.
- **Apprentice `tafe_calendar`:** standalone table or fold into
  `apprentice_profile.tafe_day jsonb`? Decide during Unit 5.D design.
- **Sub-tenant model (manager-of-multiple-clients):** out of scope for
  this plan; surfaces if a customer ever asks for it.
- ~~**Storage bucket strategy?**~~ **Resolved 2026-05-20:**
  **one bucket per tenant.** Paths: `tenant-{id}/licences/{licence_id}/...`,
  `tenant-{id}/quotes/{quote_id}/...`, `tenant-{id}/field/...`.
  RLS predicate scopes by bucket name (first path segment after bucket
  is entity-domain). Cards' existing `licence-photos` bucket migrates
  to `tenant-{core_uuid}/licences/...` paths during Cards Unit 3 data
  migration (file copy step rewrites paths incidentally).
- ~~**Audit log universal vs per-domain?**~~ **Resolved 2026-05-20:**
  **hybrid.** `eq_intake_row_audit` stays universal for intake commit
  writes (any write through any per-domain RPC records here, with
  `source_app` attribution). App-specific events (e.g. quote status
  transitions, schedule change history, leave approval workflow events)
  live in per-domain tables: `quote_status_history` (already in Unit 4),
  `schedule_change_log` (Unit 5), `leave_approval_log` (Unit 5), etc.
  Pattern: universal for "what was written"; per-domain for "what
  happened in the domain workflow".

---

## Related

- [eq/identity/IDENTITY-MODEL.md](../identity/IDENTITY-MODEL.md) — auth foundation; Phase 1.F's RLS sweep covers every canonical table this plan adds
- [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) — the worked pattern this plan generalises; Cards Units 1-2.A are complete and serve as the reference implementation
- [eq/field/multi-tenancy/plan.md](../field/multi-tenancy/plan.md) — Field's Phase 1/2 plan, gated on customer trigger; becomes the *surface migration* plan after canonical-readiness lands
- [eq-app-build-principle](../eq-app-build-principle.md) — canonical-first; Field's legacy data model is supplanted surface-by-surface, not migrated
- [supabase-architecture-decision](../supabase-architecture-decision.md) — one Supabase per tenant decision (Prereq C reaffirms or revisits)
- [auth-session-single-source](../auth-session-single-source.md) — login at tenant subdomain carries role + platform_admin through every module
- `eq/pending.md` "EQ Shell + EQ Intake" — Phase 2 critique items; Prereq A + Prereq B in this plan map directly to two of those items, fast-tracked
- `C:\Projects\eq-quotes\eq-quotes-port\migrations\001_eq_quotes_supabase_port.sql` — Quotes entity source-of-truth (Flask v1 schema)
- `C:\Projects\eq-solves-field\migrations\*` — Field entity source-of-truth (working migrations on `ktmjmdzqrogauaevbktn`)
- `C:\Projects\eq-shell\eq-intake\eq-platform\packages\eq-schemas\src\schemas\*.json` — current canonical schemas (13)

---

## Execution record (autonomous push, 2026-05-20)

| Unit | Migration / files | Outcome |
|---|---|---|
| 1 | `eq/canonical-readiness/audit-existing-tables.md` | 8 cross-cutting findings; locked 4 prestart/toolbox decisions + 1 new (staff.user_id) |
| 2 | `eq-intake/sql/007_schema_split_and_reshape.sql` + Supabase migration `2026_05_20_schema_split_and_reshape` | shell_control + app_data schemas created; 23 tables moved; tenant_id NOT NULL with JWT default; staff.user_id FK; site.{track_hours, budget_hours, slug}; staff 7 new cols; schedule_entries.entry_id → schedule_id; 7 fn search_paths updated; safety entities re-labelled cards→field; 13×4 RLS policies added |
| 3 | `eq-intake/sql/008_decompose_intake_commit_batch.sql` + migrations `2026_05_20_decompose_intake_commit_batch_v2` + `2026_05_20_drop_old_intake_commit_batch_5arg` | 4 private library fns; 5 per-domain commit RPCs; 5 per-domain unwinders; router rewrite; eq_intake_rollback rewrite; eq_intake_events.{source_app, intake_mode} columns added |
| 4 | `eq-intake/sql/009_quotes_domain.sql` + migration `2026_05_20_quotes_domain` + 7 JSON schemas in `@eq/schemas` | 7 app_data.quote* tables; 7 registry entries module=quotes; dispatch + router; line items separate table per Decision 5; money in cents; updated_at triggers |
| 5 | `eq-intake/sql/010_field_domain.sql` + migrations `2026_05_20_field_domain` + `2026_05_20_field_dispatch_and_router` | 22 new field-domain tables + 1 view (tender_nomination_clashes); 22 registry entries module=field; expanded commit_batch_field + router + unwinder; managers sunset (digest_opt_in on staff per Unit 2); pending_schedule dropped |
| 7 | `eq-shell/src/modules/intake/DomainLanding.tsx` + 5 new `/intake/{core,field,quotes,cards,service}` routes + RPC `eq_list_module_entities` (migration `2026_05_20_eq_list_module_entities`) | Registry-driven landing pages; build green (DomainLanding chunk 2.70 kB); ParserDropZone wiring per entity is the next iteration |

**Canonical final state (2026-05-20):**

| Module | Entities | Schema location |
|---|---|---|
| core | 3 (customer, contact, site) | app_data |
| field | 30 (staff, schedule, prestart, toolbox_talk, swms, jsa, itp, incident, timesheet, leave_request, leave_balance, checkin, tenant_app_config, tender, tender_enrichment, tender_nomination, tender_import_run, tender_review_decision, site_diary, weekly_report, apprentice_profile, skills_rating, feedback_entry, rotation, buddy_checkin, quarterly_review, engagement_log, tafe_calendar, schedule_change_log, leave_approval_log) | app_data |
| cards | 1 (licence) | app_data |
| quotes | 7 (quote, quote_line_item, quote_status_history, quote_attachment, scope_template, rate_library, quote_email_outbox) | app_data |
| service | 1 (asset) | app_data |
| (control plane) | tenants, users, module_entitlements, user_invites, eq_schema_registry, eq_intake_templates, eq_intake_events, eq_intake_row_audit, eq_export_events, eq_export_profiles | shell_control |

**42 entity table types in app_data + 10 shell_control tables. 5 public per-domain commit RPCs + 1 router + 5 unwinders + 4 shared private fns + 1 list-entities helper RPC.**

**Operational follow-ups (not blocking):**
- Supabase Dashboard → API → Exposed schemas: add `app_data` and `shell_control` so PostgREST routes `/rest/v1/customer` etc directly (today only RPCs are reachable from clients)
- ParserDropZone wiring per entity in DomainLanding (currently disabled "coming soon" buttons)
- Per-tenant storage bucket `tenant-{tenant_id}` policies (Cards' existing `licence-photos` bucket migrates during Cards Unit 3 data migration)
- pnpm db:apply bundle update: `db-apply.ts` already includes 001-006; new migrations 007-011 should be added to the bundle script for new-tenant provisioning
- @eq/schemas codegen run for the new Field + Quotes JSON schemas (TypeScript types + Zod validators)

## Revision history

| Date | Author | Change |
|---|---|---|
| 2026-05-20 | Claude (this session) | Initial draft authored |
| 2026-05-20 | Claude (this session) | All 6 decisions locked with Royce. Status flipped from draft → approved. Unit 5 restructured from 4 sub-units → one big push per Decision 6. |
| 2026-05-20 | Claude (this session) | Plan-review refinements: Unit 5 file gets TOC + section markers; quote line items resolved to separate table; per-tenant deploy is template-first via `pnpm db:apply`; tenant app config separate from module_entitlements. |
| 2026-05-20 | Claude (this session) | Plan-review refinements (continued): entity re-labelling (prestart/toolbox_talk/swms/jsa/itp/incident move from cards → field; Cards keeps only licence); multi-app write architecture phased path with `p_intake_mode` parameter + `source_app` audit column added to Unit 3. |
| 2026-05-20 | Claude (this session) | Plan-review framing clarification: Field's demo Supabase has no real users, SKS Labour is a separate commercial entity. Canonical-readiness for Field = enable fresh shell-module builds, not migrate existing Field. No dual auth, no one-way sync, no surface-by-surface replacement language. Plus: pending_schedule dropped (dead code); managers table sunset with digest_opt_in on staff directly. |
| 2026-05-20 | Claude (this session) | Plan-review additional locks: audit log = hybrid (universal eq_intake_row_audit for writes + per-domain tables for workflow events); storage = one bucket per tenant (`tenant-{id}`) with `<domain>/...` paths within; rollback = per-domain unwinders; PostgREST = rely on search_path. Phase context: this is Phase 2 prep during GTM-paused window — no calendar constraints applied. |
| 2026-05-20 | Claude (autonomous push) | Units 2 → 3 → 4 → 5 → 7 EXECUTED. 5 SQL migrations applied via apply_migration MCP; 8 SQL files in eq-intake/sql/; 7 quote schema JSONs in @eq/schemas; React DomainLanding + 5 routes in eq-shell; build green. Final state: 42 entities across 5 modules; 5 per-domain RPCs; per-tenant template-first deploy pattern primed for new tenant provisioning. |

---
title: EQ Canonical — Existing 13 Tables Audit (Unit 1 Output)
owner: Claude Code (Royce reviews)
last_updated: 2026-05-30
scope: Column-level audit of every existing canonical entity table against Field's actual migration shape (where applicable), Quotes' v1 schema, and Cards' working columns. Output drives Unit 2's schema-split-and-reshape migration. Where canonical and an app's shape diverge, this doc surfaces the gap and recommends a resolution.
read_priority: standard
status: draft
---

# Existing 13 Tables Audit — Unit 1 Output

**Status:** draft — pending Royce review.

This is the read-only output of canonical-readiness Unit 1. It compares
each of the 13 canonical entity tables (in `public.*` today; moving to
`app_data.*` in Unit 2) against the actual shape used by the app(s)
that will write to them.

Decision per table is one of:

- **PASS** — canonical shape matches app expectations; no reshape needed.
- **ADD COLUMNS** — canonical missing fields the app needs; add in Unit 2.
- **RENAME/REMAP** — canonical column exists with different name; clarify mapping.
- **MATERIAL DISAGREEMENT** — canonical and app shapes diverge fundamentally; Royce decides which wins before Unit 5 drafting.

---

## Summary

| Table | Module | Audit verdict | Reshape effort | Notes |
|---|---|---|---|---|
| `customer` | core | **PASS** (with note) | none | 45 columns. SimPRO-shaped. Some columns are SimPRO-specific noise for Quotes use; harmless if unused |
| `contact` | core | **PASS** | none | 29 columns. Standard contact shape with multi-default flags (default_quote_contact, etc.) |
| `site` | core | **ADD COLUMNS** | small | Field needs `slug`, `track_hours`, `budget_hours`. Canonical's `site_contact_*` triple maps cleanly to Field's `site_lead*` triple |
| `staff` | field | **ADD COLUMNS** | small-medium | Missing: `role eq_role`, `notify_roster`, `dob_day`, `dob_month`, `digest_opt_in`, `digest_cron_schedule`, `tafe_day`, `year_level` |
| `schedule_entries` | field | **RENAME** | trivial | PK is `entry_id`, not `schedule_id` (inconsistent with sibling pattern). Otherwise fits Field's schedule concept |
| `prestart_checks` | field (re-labelled) | **MATERIAL DISAGREEMENT** | high | Canonical: structured questionnaire (`responses` jsonb). Field: freeform briefing (text fields for issues/scope/hazards/permits) + inline `photos` jsonb. Different design philosophies |
| `toolbox_talks` | field (re-labelled) | **MATERIAL DISAGREEMENT** | high | Canonical: structured (key_messages, discussion_points, actions all jsonb). Field: text-mostly (safety_message, items_reviewed, open_actions, hazards) + inline `photos` jsonb |
| `swms` | field (re-labelled) | **PASS** (forward-looking) | none | No Field code reads/writes SWMS yet. Canonical shape is forward-looking; Field will adopt this shape directly when SWMS module is built |
| `jsa_records` | field (re-labelled) | **PASS** (forward-looking) | none | Same — no Field code yet. Canonical shape is the target |
| `itp_records` | field (re-labelled) | **PASS** (forward-looking) | none | Same |
| `incidents` | field (re-labelled) | **PASS** (forward-looking) | none | Same — Field's `incidents` is in `site_diaries.incidents` jsonb array today, not a standalone table |
| `licences` | cards | **PASS** | none | Already shaped per Cards canonical-migration §Unit 1.C. Cards Unit 3 data migration fills rows |
| `assets` | service | **PASS** | none | Service-domain entity, no port in scope. 33 columns include client_classification jsonb for SimPRO-style asset hierarchies |

**Headline numbers:**
- 8 tables PASS as-is
- 3 tables need small column adds (Unit 2 absorbs)
- 2 tables (`prestart_checks` + `toolbox_talks`) have **material disagreement** with Field's shape — Royce decides before Unit 5 drafts which shape wins

---

## Cross-cutting findings

### Finding 1 — `tenant_id` is NULLABLE on every canonical entity table

Every entity table has `tenant_id :: uuid NULL` (no NOT NULL constraint).
RLS predicates read `tenant_id` from JWT and compare; if a row has
`tenant_id = NULL`, RLS denies access (correctly), but it's a footgun:
any INSERT that forgets to set `tenant_id` succeeds, creating a
"ghost row" only the service-role can see.

**Recommendation:** Unit 2 alters every entity table to `tenant_id NOT
NULL DEFAULT (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid`. The
DEFAULT means INSERTs by authenticated users auto-populate from JWT;
INSERTs by service-role still have to set it explicitly. Closes the
footgun.

### Finding 2 — `schedule_entries` PK is `entry_id`, not `schedule_id`

Every other entity table follows the `<entity>_id` pattern: `asset_id`,
`customer_id`, `incident_id`, `licence_id`, etc. `schedule_entries`
breaks the pattern with `entry_id`. Also the table is named
`schedule_entries` (plural-suffix) where most others are simple plural
(`assets`, `customers`) or singular-suffix (`prestart_checks`,
`itp_records`).

**Recommendation:** rename `entry_id` → `schedule_id`. Defer the table
rename (`schedule_entries` → `schedule`) — too disruptive for the value;
table-name → schema-singular convention is not consistent anyway in
canonical today.

### Finding 3 — Every entity has intake provenance columns

Every table has the same 4 columns: `imported_at`, `imported_from`,
`intake_id`, `schema_version`. This is the right pattern — every row
is traceable to an intake operation. Validated.

### Finding 4 — Standard audit columns are consistent

Every table has: `created_at`, `updated_at`, `created_by uuid`,
`updated_by uuid`. Consistent. `created_at`/`updated_at` default to
`now()`; `created_by`/`updated_by` are nullable (intake-time writes
have a user, system writes might not).

**Recommendation:** verify the `updated_at` triggers actually exist for
each table. Field's pattern (e.g. `prestarts_set_updated_at`) is per-
table; canonical might be using a shared `eq_set_updated_at()` fn.
Confirm in Unit 2.

### Finding 5 — `external_id` widespread

Every entity has `external_id` (varchar or text). Used by Intake to
track source-system identity (SimPRO `Customer.ID`, Cards licence
external_id, etc.). Validated.

### Finding 6 — Photo storage strategy is inconsistent across entities

- `licences` has `photo_front_path text`, `photo_back_path text` (Storage bucket paths)
- `prestart_checks` has `signature_image_url text` (one signature)
- `incidents` has `photo_urls jsonb` (array of URLs)
- `swms`, `jsa_records`, `itp_records` have `attachments jsonb` (array of {url, name, type})
- Field's prestarts + toolbox_talks + site_diaries have `photos jsonb` (inline base64, max 8/record)

Three different patterns: external Storage URLs (single field, jsonb
URL array, jsonb attachment objects) + inline base64 (Field's
optimisation for offline-first mobile capture).

**Recommendation:** Unit 2 doesn't change this — but Unit 5 (Field
domain) needs to decide whether canonical's `prestart_checks.signature_image_url`
+ external storage is the right pattern for Field's offline-first
mobile capture (where photos are uploaded later when reconnected),
or whether canonical's prestart_checks gains an `inline_photos jsonb`
column for the offline-first path. Tied to the prestart_checks
material-disagreement decision below.

### Finding 7 — `users` ↔ `staff` link is MISSING (raised during Unit 1 verification)

Phase 1.F's identity layer put `role eq_role NOT NULL` and
`is_platform_admin boolean NOT NULL` on `users` (becoming
`shell_control.users` in Unit 2). The `staff` table has neither.

Critically, **there is no formal link between `users` and `staff`**:
no `staff.user_id` FK, no `users.staff_id` FK. Conceptually:

- `users` = "people who can log in" (1 row per authenticated identity)
- `staff` = "operational/scheduling people" (1 row per schedulable
  worker, includes labour-hire who never log in)

They can share an email but the only join today is by text-matching
`users.email = staff.email`. That's brittle:

- Email can change without staff record updating
- Two staff with the same email (rare but possible — family business)
- Some staff have no email at all

**Recommendation:** Unit 2 ADDs `staff.user_id uuid NULL REFERENCES
shell_control.users(id) ON DELETE SET NULL`. Nullable because not
every staff member is a user (labour-hire crew typically aren't).
This becomes the canonical user↔staff link for "find current user's
schedule", "show colleague's contact info", "promote staff to user".

Corollary: the audit's earlier note about "ADD `staff.role`" is
**WITHDRAWN.** Role lives on `users`. Queries that need staff role
JOIN `staff` → `users` via the new user_id link. This is cleaner
than denormalising role onto staff (no sync trigger needed, one
source of truth).

### Finding 8 — `gps`/`device_id`/`source`/`raw_extract` indicate mobile-capture + OCR intent

Several canonical entity tables (`prestart_checks`, `toolbox_talks`,
`incidents`) include columns that imply mobile-capture (`gps jsonb`,
`device_id text`) and OCR/import (`source text`, `raw_extract text`).
Field has none of these. These columns exist in canonical because
canonical was designed for Cards mobile capture + EQ Capture OCR
ingest, not Field web-form data entry.

**Recommendation:** keep them. They're forward-looking for the
multi-app architecture (Decision Q3). Field-style web-form writes
just leave them NULL.

---

## Per-table audit detail

### `customer` (core, 45 columns) — PASS with note

Canonical shape is SimPRO-flavoured (customer_group, customer_profile,
account_manager, default_quote_method, default_invoice_method,
default_job_method, separate postal_address block, etc.). All 45
columns are well-named and the type model is sound.

**Quotes use:** quote.customer_id FK → this table. Quotes' Flask v1
has `sks_quotes_customers` with a narrower column set; canonical-conform
naming (Decision 5) means the React rewrite reads/writes from this
canonical `customer` table.

**Field use:** Field has no `customers` concept today — its tenant
root is `organisations`. Future Field surfaces (e.g. customer-facing
job creation in a Field rewrite) would FK to this table.

**Recommendation:** keep as-is. Some columns will be unused by Quotes
(account_manager, default_*_method); harmless.

### `contact` (core, 29 columns) — PASS

Standard contact shape. Multi-default flags (`is_default_quote_contact`,
`is_default_job_contact`, etc.) line up with SimPRO + Field's
notification patterns. `customer_id` FK is correct.

**Recommendation:** keep as-is.

### `site` (core, 32 columns) — ADD COLUMNS

Canonical:
- Standard address fields (line_1/2, suburb, state, postcode, country)
- Latitude/longitude (geo)
- `site_contact_name`, `site_contact_phone`, `site_contact_email`
- `induction_required` boolean, `induction_url`
- `customer_id` FK + `external_customer_id`
- `code`, `name`, `client_name`, `site_type`

Field's `sites` adds (from migrations):
- `site_lead text`, `site_lead_phone text`, `site_lead_email text` — **maps to canonical's `site_contact_*` triple** (rename, not add)
- `track_hours boolean default false` — **missing from canonical** (Field's v3.4.71 project-hours tracking)
- `budget_hours numeric(10,2) null` — **missing from canonical**
- `slug` (per Field's path-based tenant resolution) — **missing from canonical**
- `tenant_supabase_url`, `tenant_supabase_key` (multi-tenant routing in some tenancy patterns) — **deliberately NOT in canonical**

**Recommendation:** Unit 2 ADDS:
- `track_hours boolean DEFAULT false` (for the project-hours feature)
- `budget_hours numeric(10,2) NULL` (paired with track_hours)
- `slug text NULL` (if shell needs per-site slugs; verify with shell URL routing)

Skip: `tenant_supabase_url`/`tenant_supabase_key` (these were
Field's multi-tenant routing approach pre-Phase 1.E; canonical's
single-Supabase-per-tenant supersedes).

Field's `site_lead*` reads/writes via Intake-time column-alias mapping
into canonical's `site_contact_*` — this is what `x-eq-source-aliases`
in `site.schema.json` is for.

### `staff` (field, 27 columns) — ADD COLUMNS

Canonical:
- staff_id, tenant_id, external_id
- first_name, last_name, preferred_name, email, phone
- employment_type, trade, level
- start_date, end_date, hourly_rate_cost, hourly_rate_charge
- home_base, default_site_id (FK)
- active, notes + intake provenance + audit

Field's `people` adds (from migrations):
- `notify_roster boolean DEFAULT false` (per 2026-04-16_tier1_features_schema)
- `dob_day smallint`, `dob_month smallint` (per 2026-04-21_people_dob_start_date — note: no year, intentional)
- `start_date date` — **already in canonical** ✓
- `role eq_role` (per 2026-04-27_eq_role_enum_people_role) — **lives on `users`, not staff** (verified 2026-05-20)
- `digest_opt_in boolean`, `digest_cron_schedule text` (per 2026-05-20 review Q2 — was on managers, moves to staff)
- `tafe_day text` + `year_level smallint` (per 2026-04-16_tafe_day_and_holidays.sql — apprentice features)

**Recommendation:** Unit 2 ADDS to `app_data.staff`:
- `user_id uuid NULL REFERENCES shell_control.users(id) ON DELETE SET NULL` (per Finding 7 — the missing user↔staff link)
- `notify_roster boolean DEFAULT false`
- `dob_day smallint NULL CHECK (dob_day BETWEEN 1 AND 31)`
- `dob_month smallint NULL CHECK (dob_month BETWEEN 1 AND 12)`
- `digest_opt_in boolean DEFAULT false`
- `digest_cron_schedule text NULL`
- `tafe_day text NULL CHECK (tafe_day IS NULL OR tafe_day IN ('mon','tue','wed','thu','fri'))`
- `year_level smallint NULL CHECK (year_level BETWEEN 1 AND 4)`

That's 8 added columns. All nullable / defaulted, so additive only.
**Skipped:** `staff.role` — role lives on `shell_control.users`,
queried via the new `staff.user_id` join (see Finding 7).

**Verified 2026-05-20:** `eq_role` enum exists. `users.role` +
`users.is_platform_admin` exist. `staff.role` does NOT exist (and
shouldn't — role belongs on users). `staff.user_id` does NOT exist
(and SHOULD — this audit recommends adding).

### `schedule_entries` (field, 21 columns) — RENAME

Canonical:
- `entry_id uuid PK` — **rename to `schedule_id`** (sibling-consistency)
- tenant_id, staff_id (FK), site_id (FK), date
- hours_planned, hours_actual, shift (default 'day')
- task, status (default 'planned')
- leave_type — interesting (lets schedule track a leave allocation as a non-work row), unique to canonical
- notes, supervisor_id (FK to staff)
- + intake provenance + audit

Field's `schedule` table (per multi-tenancy plan audit):
- Different shape — Field stores schedule as `schedule[dayKey] === site.abbr` denormalized layout. The relational shape only exists in canonical.

**Recommendation:** rename `entry_id` → `schedule_id`. Other columns
keep as-is. Field's schedule data will be reshape-on-ingest when Field
modules are built in shell against canonical (not migrate-as-is).

### `prestart_checks` (field-re-labelled, 26 columns) — **MATERIAL DISAGREEMENT**

**Canonical's design:**
- Site referenced by `site_id uuid` FK
- `date` + `shift_start text`
- `weather text` (single string)
- `crew_present jsonb` (signoffs + attendance)
- `responses jsonb` — structured prestart questionnaire responses
- `hazards_identified jsonb` (array of objects)
- `swms_referenced jsonb` (array of refs)
- `signature_image_url text` (single supervisor sig)
- `gps jsonb`, `device_id text` (mobile capture)
- `source`, `raw_extract` (OCR/import path)

**Field's design (from `prestarts` + `prestarts.photos` migrations):**
- Site referenced by `site_abbr text` (no FK — cross-tenant portability rationale)
- `briefing_date date`, `briefing_time time`
- No weather column
- `crew jsonb` (signoffs)
- Text fields: `prev_day_issues`, `works_scope`, `hazards`, `permits`
- `hrcw_categories text[]` (high-risk construction work categories)
- `swms_refs text` (plain text)
- `photos jsonb` — inline base64 array, max 8 photos
- No gps/device_id/source/raw_extract

**Two fundamentally different shapes.** Canonical is a structured
questionnaire optimised for mobile capture + ingest paths. Field is a
freeform briefing form optimised for offline-first web entry with
inline photos.

**Decision needed:** which wins?

**Option A — Canonical shape wins, Field reshapes during port.**
The Field rewrite (when EQ Solutions builds a new prestart module in
shell) follows canonical's structured shape. Loses some Field UX
(freeform text fields like `prev_day_issues`, `works_scope` get
expressed as questionnaire responses with `type: 'text'`). Gains
queryability (`SELECT * WHERE responses->>'safety_check' = 'fail'`).

**Option B — Field shape wins, canonical reshapes in Unit 2.**
Drop canonical's structured columns; replace with Field's text fields
+ inline `photos jsonb`. Cards-mobile prestart capture would lose its
questionnaire shape too. Photos go inline (no Storage bucket).
Mobile-first UX preserved.

**Option C — Hybrid.** Keep both shapes side-by-side:
- `responses jsonb` for questionnaire (canonical pattern)
- `prev_day_issues`, `works_scope`, `hazards_text`, `permits_text`,
  `hrcw_categories text[]` for freeform (Field pattern)
- `photos jsonb` (inline base64) AND `signature_image_url`/Storage
  bucket photos for hybrid offline/online
- App writes either structure based on capture mode

**Recommendation:** **Option A (canonical wins).** Field is a
schema reference, not a migration source (per 2026-05-20 framing
clarification). The next-gen prestart module built in shell can use
canonical's structured `responses jsonb` shape; freeform fields
become a single `notes` response. Field's existing demo retains its
shape on `ktmjmdzqrogauaevbktn` — not migrated. **Royce decides.**

### `toolbox_talks` (field-re-labelled, 28 columns) — **MATERIAL DISAGREEMENT**

Same pattern as `prestart_checks`. Canonical is structured (key_messages
jsonb, discussion_points jsonb, actions jsonb, attendees jsonb,
attachments jsonb); Field is text-mostly (topic, safety_message,
items_reviewed, open_actions, hazards) + inline `photos jsonb`.

**Recommendation:** **Same as prestart_checks — canonical wins.**
Symmetry matters; if prestart adopts canonical's structured shape, so
should toolbox. **Royce decides.**

### `swms` (field-re-labelled, 33 columns) — PASS (forward-looking)

Canonical:
- swms_id, tenant_id, external_id, version, site_id (FK)
- activity, high_risk_categories jsonb, hazards jsonb, ppe_required jsonb, permits_required jsonb
- tools_plant jsonb, training_competency jsonb
- emergency_procedures text
- prepared_by_*, reviewed_by_*, valid_from/until
- signatures jsonb, attachments jsonb
- status, source, raw_extract + intake provenance + audit

Field has **no SWMS migration on disk** (only the table-stubs
referenced by site reports module). Canonical's SWMS shape is
forward-looking — when the SWMS module is built in shell, it adopts
this shape directly.

**Recommendation:** keep as-is. No reshape needed.

### `jsa_records`, `itp_records`, `incidents` — PASS (forward-looking)

Same pattern as SWMS. No Field migrations exist for these as
standalone tables; Field's `site_diaries.incidents` is a JSONB array
within the diary table, not a standalone entity. Canonical's
standalone-entity shape is forward-looking.

**Recommendation:** keep as-is. Future Field site-diary rewrite in
shell would either fan out site_diary incidents into canonical
`incidents` rows (preferred) or keep them embedded (legacy).

### `licences` (cards, 23 columns) — PASS

Already shaped per Cards canonical-migration plan §Unit 1.C. Cards
Unit 3 data migration fills rows from Cards' standalone Supabase.

**Recommendation:** keep as-is.

### `assets` (service, 33 columns) — PASS

Service-domain entity, no canonical port in this plan's scope. Shape
includes `client_classification jsonb` for SimPRO-style hierarchy.

**Recommendation:** keep as-is.

---

## Recommendations for Unit 2 reshape migration

Single migration `2026_05_NN_schema_split_and_reshape.sql` absorbs
both the schema split AND the audit findings. The reshape portion:

### Atomic adds (all tables get):

```sql
-- Tenant_id NOT NULL with JWT default (Finding 1)
-- Apply to all 13 entity tables
ALTER TABLE app_data.<each_entity>
  ALTER COLUMN tenant_id SET DEFAULT (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid,
  ALTER COLUMN tenant_id SET NOT NULL;
```

### Per-table reshape:

**`app_data.site` adds:**
```sql
ALTER TABLE app_data.site
  ADD COLUMN IF NOT EXISTS track_hours boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS budget_hours numeric(10,2) NULL,
  ADD COLUMN IF NOT EXISTS slug text NULL;
```

**`app_data.staff` adds (verified 2026-05-20):**
```sql
ALTER TABLE app_data.staff
  ADD COLUMN IF NOT EXISTS user_id uuid NULL REFERENCES shell_control.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS notify_roster boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS dob_day smallint NULL,
  ADD COLUMN IF NOT EXISTS dob_month smallint NULL,
  ADD COLUMN IF NOT EXISTS digest_opt_in boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS digest_cron_schedule text NULL,
  ADD COLUMN IF NOT EXISTS tafe_day text NULL,
  ADD COLUMN IF NOT EXISTS year_level smallint NULL,
  ADD CONSTRAINT staff_dob_day_range CHECK (dob_day IS NULL OR dob_day BETWEEN 1 AND 31),
  ADD CONSTRAINT staff_dob_month_range CHECK (dob_month IS NULL OR dob_month BETWEEN 1 AND 12),
  ADD CONSTRAINT staff_tafe_day_range CHECK (tafe_day IS NULL OR tafe_day IN ('mon','tue','wed','thu','fri')),
  ADD CONSTRAINT staff_year_level_range CHECK (year_level IS NULL OR year_level BETWEEN 1 AND 4);

CREATE INDEX IF NOT EXISTS staff_user_id_idx ON app_data.staff (user_id) WHERE user_id IS NOT NULL;
```

Verified that `staff.role` does NOT exist on canonical (role lives
on `users`); the new `staff.user_id` FK enables the JOIN. No need
to denormalise role onto staff.

**`app_data.schedule_entries` rename:**
```sql
ALTER TABLE app_data.schedule_entries RENAME COLUMN entry_id TO schedule_id;
-- Update any FKs / RLS predicates that reference entry_id (none in canonical today)
```

**`prestart_checks` + `toolbox_talks`:** PENDING ROYCE DECISION (see
above material-disagreement options A/B/C). If Option A wins, no
reshape needed.

### Things to NOT touch in Unit 2:

- `customer`, `contact`, `swms`, `jsa_records`, `itp_records`,
  `incidents`, `licences`, `assets` — all PASS
- Photo storage strategy — Cross-cutting Finding 6 — surface in
  Unit 5 design when Field's offline-first mobile capture comes up

### Schema split itself (Unit 2 main work):

```sql
CREATE SCHEMA IF NOT EXISTS shell_control;
CREATE SCHEMA IF NOT EXISTS app_data;

-- Shell-control tables
ALTER TABLE public.tenants SET SCHEMA shell_control;
ALTER TABLE public.users SET SCHEMA shell_control;
ALTER TABLE public.module_entitlements SET SCHEMA shell_control;
ALTER TABLE public.user_invites SET SCHEMA shell_control;
ALTER TABLE public.eq_schema_registry SET SCHEMA shell_control;
ALTER TABLE public.eq_intake_templates SET SCHEMA shell_control;
ALTER TABLE public.eq_intake_events SET SCHEMA shell_control;
ALTER TABLE public.eq_intake_row_audit SET SCHEMA shell_control;
ALTER TABLE public.eq_export_events SET SCHEMA shell_control;
ALTER TABLE public.eq_export_profiles SET SCHEMA shell_control;

-- App-data entity tables
ALTER TABLE public.customers SET SCHEMA app_data;
ALTER TABLE public.contacts SET SCHEMA app_data;
ALTER TABLE public.sites SET SCHEMA app_data;
ALTER TABLE public.staff SET SCHEMA app_data;
ALTER TABLE public.schedule_entries SET SCHEMA app_data;
ALTER TABLE public.prestart_checks SET SCHEMA app_data;
ALTER TABLE public.toolbox_talks SET SCHEMA app_data;
ALTER TABLE public.swms SET SCHEMA app_data;
ALTER TABLE public.jsa_records SET SCHEMA app_data;
ALTER TABLE public.itp_records SET SCHEMA app_data;
ALTER TABLE public.incidents SET SCHEMA app_data;
ALTER TABLE public.licences SET SCHEMA app_data;
ALTER TABLE public.assets SET SCHEMA app_data;

-- search_path
ALTER ROLE authenticated SET search_path = app_data, shell_control, public, extensions;
ALTER ROLE service_role SET search_path = app_data, shell_control, public, extensions;

-- Re-label entities per 2026-05-20 plan-review
UPDATE shell_control.eq_schema_registry
SET module = 'field'
WHERE entity IN ('prestart','toolbox_talk','swms','jsa','itp','incident')
  AND module = 'cards';

-- RLS recreations (one block per table, predicates unchanged from Phase 1.F)
-- ... per-table CREATE POLICY statements
```

### Bundle reconciliation (Decision 3 — template-first deployment):

Confirm `eq-intake/eq-platform/scripts/db-apply.ts` bundle is in sync
with what's deployed on `jvknxcmbtrfnxfrwfimn`. Run `pnpm db:apply`
against `core`; expect zero-DDL-fired output (all migrations idempotent).
If drift detected, reconcile by adding missing migrations to bundle.

---

## Decisions locked 2026-05-20 (post-audit Royce review)

1. ~~prestart_checks shape:~~ **Option A — canonical wins**
   (structured questionnaire). No reshape needed; Field demo retains
   its shape on its own Supabase.
2. ~~toolbox_talks shape:~~ **Same as prestart — canonical wins
   (symmetry).** No reshape needed.
3. ~~staff.role verify:~~ **Verified.** `eq_role` enum exists.
   `users.role` exists. `staff.role` does NOT exist (and shouldn't —
   per Finding 7). Unit 2 ADDs `staff.user_id` FK instead.
4. ~~site.slug:~~ **Add to canonical** as default. Cheap addition;
   stable across UIs.

## One remaining decision

**`staff.user_id` FK** (new finding from Phase 1.F verification):
this audit recommends ADD. Confirm before Unit 2 drafting.

---

## Related

- [eq/canonical-readiness/plan.md](./plan.md) — parent plan; this audit is Unit 1 output
- [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) — Cards' licence shape served as template
- `C:\Projects\eq-solves-field\migrations\*` — Field migration source
- `C:\Projects\eq-quotes\eq-quotes-port\migrations\001_eq_quotes_supabase_port.sql` — Quotes Flask v1 shape
- `C:\Projects\eq-shell\eq-intake\eq-platform\packages\eq-schemas\src\schemas\*.json` — 13 canonical schemas (registry references)

---

## Revision history

| Date | Author | Change |
|---|---|---|
| 2026-05-20 | Claude Code (Unit 1) | Initial audit draft. 8 PASS, 3 ADD-COLUMNS, 1 RENAME, 2 MATERIAL DISAGREEMENT (prestart_checks + toolbox_talks). Pending Royce review on the 4 open decisions. |
| 2026-05-20 | Claude Code (Unit 1) | Audit revised after Phase 1.F verification: staff.role does NOT exist (role lives on users); staff.user_id FK does NOT exist either — new Finding 7 recommends adding it as the missing user↔staff link. The 4 prior open decisions all locked at recommended defaults. One new decision raised (staff.user_id) pending Royce confirmation. |

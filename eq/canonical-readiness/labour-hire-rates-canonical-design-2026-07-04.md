---
title: Labour Hire Rates — Canonical Design & Build Spec
owner: Royce Milmlow
last_updated: 2026-07-05
scope: Canonical data model (rate matrix + source_doc_type) and lean build plan for labour-hire rates; v1 seeded manually from 3 agency PDFs, EQ Intake auto-upload deferred
read_priority: reference
status: draft
---

# Labour Hire Rates — Canonical Design & Build Spec

_Author: Claude Code · 2026-07-04 (rev. 2026-07-05: rate-matrix model from 3 real agency PDFs; eq-ui-grounded tab) · Status: APPROVED — lean build (Royce 2026-07-05) · No DB/code applied yet_

> **Build decision (Royce, 2026-07-05): LEAN.** v1 = the two canonical tables + the simple read tab, **seeded manually**
> from the 3 real PDFs. EQ Intake auto-upload is **deferred to a fast-follow** (it's unproven for this doc type). The
> data model stays as designed (matrix + source_doc_type) — only the *feed* is manual first. Canonical audit passed
> (see §2). Everything below is staged; nothing is applied to any live system.

---

## 1. Decision (one paragraph)

Labour hire rates — **the cost rates we have locked in with each labour hire firm** — are stored as
**canonical reference data in `app_data` on ehow**, fed by **EQ Intake** (upload a firm's rate PDF/spreadsheet →
vision-extract + column-map → rows), and surfaced in a **simple read-only tab under EQ Ops** in eq-shell where **project & upper management**
see each agency's **contact details, locked-in rates, and key terms** at a glance. **Cost-only** — what we pay the
agency. Charge-out/margin is explicitly out of scope (tracked elsewhere; see §9). Reports/tabs *consume* this data;
they do not store it.

Flow: `Rate-card PDF → EQ Intake → app_data.labour_hire_rates → Ops tab (read)`

---

## 2. What exists today (verified live, ehow `ehowgjardagevnrluult`, 2026-07-04)

| Fact | Detail |
|---|---|
| No company-scoped rate model | No `labour hire company` dimension exists in any table. Net-new. |
| `app_data.rate_library` | The Intake-shaped rate master (`unit_cost_cents`/`unit_sell_cents`/`margin_pct`, `intake_id`, `imported_from`, `schema_version`). **0 rows** — empty scaffold. Generic (labour/material/equipment/subcontractor), **not** vendor-scoped. Do **not** overload it. |
| `app_data.quote_rate_presets` | 20 rows, ex-Quotes sell-side presets. Not relevant. |
| `app_data.sks_comms_labour_rates` | 13 rows, `site_scope + item + cost_rate + charge_rate`. SKS-comms-specific, site-scoped, **no company**. Not the home; possible partial seed (see §9). |
| EQ Intake engine | Real, but **in build** — vision-extraction + column-mapping prompts are v1.0 production; `app_data.eq_intake_staging` = **0 rows** (not yet flowed in prod). Engine exists; unproven for this doc type. |
| RLS convention | `rate_library`: RLS on; `tenant_id` NOT NULL default `((auth.jwt()->'app_metadata')->>'tenant_id')::uuid`; policies scoped to `authenticated`, tenant-isolated on that JWT claim; full DML to `service_role`. |
| Ops read client | eq-shell `createTenantDataClient()` routes `.from()` → `app_data` under the user's tenant JWT (role `authenticated`). Confirms the `authenticated` + tenant-JWT RLS is the correct read path. |

**Why not Field:** the `resources/hours/dispatch → Field only` rule covers *operational* labour. Rates are
*commercial reference data* — and the live system already keeps every rate table in canonical `app_data`, none in Field.

### 2.1 What real agency documents look like (3 SKS samples analysed, 2026-07-05)

Three actual labour-hire PDFs from SKS's OneDrive drove the model below. They fall into two classes:

| Doc | Class | Company | Shape |
|---|---|---|---|
| **Madagins Rates 2026** | **Rate card** (quote) | Madagins Pty Ltd (ABN 43 671 869 962) | Clean table, 4 roles × **3 rate columns**: Licensed Electrician `$80.79 / $105.88 / $137.43` (Normal / T½ / Double), Tradesperson Cert `$71.06 / $92.88 / $120.41`, Grade 4 TA, Grade 2 TA. Dated 29/06/26, valid 30 days, 4hr min, GST-exclusive. Labelled "charge out rates" (agency→SKS) = **SKS cost**. |
| **NSW 2022** | **Invoice** | Madagins Pty Ltd | One line: Licensed Electrician, Normal, 31 hrs @ **$80.79** — matches the rate card exactly. Job No 27061, week 15–21/06/26. |
| **Core - INV0015034** | **Invoice** | Core Talent Pty Ltd | One worker (Shihab Al-gburi, class. "CORE EL", site Mascot DC), one week. Unit Cost column → Normal `$70.07`, OT1.5 `$93.34`, OT2.0 `$122.45`, + Productivity `$2.20`, Travel `$28.60`, Excess Travel `$19.80`. **Role is in the free-text line description, not a column.** |

**Three consequences for the model:**

1. **Rate is a matrix, not a scalar.** Every source expresses Normal / Time-and-a-half / Double per role. A single
   `cost_rate` loses this → add a **`rate_type`** dimension; one row per (company × role × rate_type × period).
2. **Invoices are a valid but weaker source.** The Unit Cost/Unit Price column *is* the cost rate (NSW 2022 = the card
   exactly), so rates can be derived from an invoice — but the role is free-text and it's a point observation, not a
   locked card. Tag **`source_doc_type`** (`rate_card` | `invoice`) so provenance shows and invoice rates can validate
   against (and flag drift from) the card.
3. **Allowances are real and material** (Productivity, Travel, Excess Travel, plus Madagins' "site allowances at
   additional cost"). Not hourly role rates — handled as `rate_type = 'allowance'`, or deferred (§9 decision).

---

## 3. Canonical data model (`app_data` on ehow + zaap)

Two tables + one view. Amounts stored as `numeric` AUD to match the closest analog (`staff.hourly_rate_cost` is a
number, not cents). Mirrors `rate_library`'s tenant/RLS/lineage conventions. The rates table carries a **`rate_type`**
dimension (Normal / T½ / Double / allowance — §2.1) so one card row expands to multiple canonical rows, and a
**`source_doc_type`** provenance tag (rate_card vs invoice).

### 3.1 `app_data.labour_hire_companies`

```sql
create table if not exists app_data.labour_hire_companies (
  company_id      uuid primary key default gen_random_uuid(),
  tenant_id       uuid not null default (((auth.jwt() -> 'app_metadata') ->> 'tenant_id'))::uuid,
  name            text not null,
  abn             text,
  -- contact + reference info (surfaced on the tab for project / upper management)
  primary_contact text,                 -- account manager, e.g. 'Ciaran' (Madagins)
  contact_email   text,                 -- e.g. accounts@coretalent.com.au
  contact_phone   text,                 -- e.g. 02 8203 5499
  address         text,                 -- agency address from letterhead
  payment_terms   text,                 -- e.g. '30 days from invoice'
  active          boolean not null default true,
  notes           text,                 -- min hours, GST treatment, site-allowance conditions, EFT/bank if needed
  -- intake lineage (mirrors rate_library)
  intake_id       uuid,
  imported_from   text,
  imported_at     timestamptz,
  schema_version  text,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  created_by      uuid,
  updated_by      uuid,
  unique (tenant_id, name)          -- dedup guard; see risk R2
);
```

The tab's top level is this table — **every agency shows with its contact and terms even before any rate is loaded**.
Rates hang off it. Bank/EFT details stay in `notes` (or move to dedicated columns later) — kept out of the default
column set so the shared view isn't a payment-detail leak.

### 3.2 `app_data.labour_hire_rates`

```sql
create table if not exists app_data.labour_hire_rates (
  rate_id         uuid primary key default gen_random_uuid(),
  tenant_id       uuid not null default (((auth.jwt() -> 'app_metadata') ->> 'tenant_id'))::uuid,
  company_id      uuid not null references app_data.labour_hire_companies(company_id) on delete restrict,
  role            text not null,                    -- trade / classification, e.g. 'Licensed Electrician'
  rate_type       text not null default 'normal'    -- the rate matrix (§2.1)
                    check (rate_type in ('normal','time_and_half','double','allowance')),
  rate_label      text,                             -- for allowances: 'Travel', 'Productivity', 'Excess Travel'
  cost_rate       numeric(10,2) not null,           -- AUD, what we pay the agency. Cost-only, sensitive.
  unit            text not null default 'hour' check (unit in ('hour','day','each')),
  source_doc_type text not null default 'rate_card' -- provenance / trust (§2.1)
                    check (source_doc_type in ('rate_card','invoice','manual')),
  effective_from  date not null default current_date,
  effective_to    date,                             -- null = current / open-ended
  active          boolean not null default true,
  notes           text,
  -- intake lineage
  intake_id       uuid,
  imported_from   text,
  imported_at     timestamptz,
  schema_version  text,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  created_by      uuid,
  updated_by      uuid,
  check (effective_to is null or effective_to >= effective_from)
);
create index if not exists lhr_tenant_company_role_idx
  on app_data.labour_hire_rates (tenant_id, company_id, role, rate_type);
```

`rate_type` splits a rate card into rows: Madagins Licensed Electrician → 3 rows (`normal $80.79`, `time_and_half
$105.88`, `double $137.43`). Allowances (`rate_type='allowance'`) carry their name in `rate_label` and use
`unit='each'` where charged per-occurrence. `source_doc_type` lets the tab distinguish a locked card from an
invoice-observed rate and drives drift-detection between the two.

### 3.3 View — `app_data.labour_hire_rates_view` (the tab's single read)

```sql
create or replace view app_data.labour_hire_rates_view
with (security_invoker = true) as
select
  r.rate_id, r.tenant_id, r.company_id,
  c.name  as company_name,
  r.role, r.rate_type, r.rate_label, r.cost_rate, r.unit, r.source_doc_type,
  r.effective_from, r.effective_to,
  ( r.active
    and r.effective_from <= current_date
    and (r.effective_to is null or r.effective_to >= current_date) ) as is_current,
  r.updated_at
from app_data.labour_hire_rates r
join app_data.labour_hire_companies c on c.company_id = r.company_id;
```

`security_invoker = true` → the querying user's RLS applies, so the tenant-JWT read path is honoured (same pattern
as the service.* invoker views).

### 3.4 RLS + grants (both tables — mirrors `0147_issues`: SELECT-only to authenticated, writes via service_role)

Because `cost_rate` is commercially sensitive, `authenticated` gets **SELECT only** (tenant-scoped); all writes go
through `service_role` (the Intake emit RPC) or a definer RPC — the same posture `app_data.issues` uses. The
`ops.view_rates` permission is the UI visibility gate; RLS enforces tenant isolation.

```sql
grant select, insert, update, delete on app_data.labour_hire_companies to service_role;
grant select, insert, update, delete on app_data.labour_hire_rates     to service_role;
grant select on app_data.labour_hire_companies to authenticated;   -- tab read only
grant select on app_data.labour_hire_rates     to authenticated;
revoke insert, update, delete on app_data.labour_hire_companies from anon, authenticated;
revoke insert, update, delete on app_data.labour_hire_rates     from anon, authenticated;

alter table app_data.labour_hire_companies enable row level security;
alter table app_data.labour_hire_rates     enable row level security;

create policy labour_hire_companies_select on app_data.labour_hire_companies
  for select to authenticated
  using (tenant_id = ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid));

create policy labour_hire_rates_select on app_data.labour_hire_rates
  for select to authenticated
  using (tenant_id = ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid));
```

> **Built:** the full, idempotent migration is staged at
> [`labour-hire-rates-build/0162_labour_hire_rates.sql`](labour-hire-rates-build/0162_labour_hire_rates.sql)
> (next free number as of 2026-07-05; matches `0147_issues` style). Schemas + seed + drop-in guide live alongside it.

---

## 4. EQ Intake integration

### 4.1 Two new schemas (drop into `eq-intake/eq-platform/packages/eq-schemas/src/schemas/`)

The build (`scripts/generate.ts`) auto-discovers `*.schema.json`, generates TS + Zod, and the schema mirrors into
the `eq_schema_registry` DB table. `x-eq-table` binds the entity to its target table; the emit RPC
`eq_intake_commit_batch(p_intake_id, p_tenant_id, p_table, p_rows)` writes rows, with `eq_intake_events` /
`eq_intake_row_audit` lineage and `eq_intake_rollback()` available.

**`labour-hire-rate.schema.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.eq.solutions/ops/labour-hire-rate/v1.json",
  "title": "Labour Hire Rate",
  "description": "A locked-in cost rate for a role supplied by a labour hire company. One row per company x role x rate_type x effective period. Cost only — what we pay the agency. A rate card with Normal/Time-and-half/Double columns expands to one row per rate_type.",
  "type": "object",
  "x-eq-entity": "labour_hire_rate",
  "x-eq-module": "ops",
  "x-eq-version": "1.0.0",
  "x-eq-table": "labour_hire_rates",
  "required": ["rate_id", "tenant_id", "company_id", "role", "rate_type", "cost_rate", "effective_from"],
  "properties": {
    "rate_id": {
      "type": "string", "format": "uuid",
      "description": "Internal canonical ID. Generated on import if not provided.",
      "x-eq-source-aliases": ["id", "rate_id"],
      "x-eq-required-on-import": false
    },
    "tenant_id": {
      "type": "string", "format": "uuid",
      "description": "Stamped from the tenant JWT on import.",
      "x-eq-required-on-import": false
    },
    "company_id": {
      "type": ["string", "null"], "format": "uuid",
      "description": "The labour hire company this rate is from. Normally set once at upload (one rate card per firm) and stamped onto every row; if a company column is present it is FK-resolved by name.",
      "x-eq-source-aliases": ["company", "agency", "supplier", "labour_hire_company", "firm", "vendor", "hire_company"],
      "x-eq-foreign-key": "labour_hire_company.company_id",
      "x-eq-fk-fuzzy-match-on": ["labour_hire_company.name"]
    },
    "role": {
      "type": "string",
      "description": "Trade / classification the rate applies to. On invoices this is often inside a free-text line description (e.g. 'CORE EL - Mascot DC' → 'Electrician') — extract it.",
      "x-eq-source-aliases": ["role", "trade", "classification", "position", "type", "skill", "category", "description", "item"],
      "x-eq-suggested-values": ["Licensed Electrician", "Tradesperson", "Electrician", "Labourer", "Mechanical Fitter", "Cable Hand", "Leading Hand", "Apprentice", "Supervisor", "Rigger", "Trade Assistant"]
    },
    "rate_type": {
      "type": "string", "enum": ["normal", "time_and_half", "double", "allowance"], "default": "normal",
      "description": "Which cell of the rate matrix. Rate cards give Normal / Time-and-a-half / Double per role — emit one row per column. Allowances (Travel, Productivity, etc.) are rate_type='allowance'.",
      "x-eq-source-aliases": ["rate_type", "time_type", "penalty"],
      "x-eq-enum-aliases": {
        "normal": ["normal time", "ordinary", "nt", "ot0", "flat", "base", "standard"],
        "time_and_half": ["time and a half", "time & a half", "t1.5", "ot1.5", "overtime 1.5", "1.5x", "time-and-a-half"],
        "double": ["double time", "dt", "t2.0", "ot2.0", "overtime 2.0", "2x"],
        "allowance": ["allowance", "travel", "productivity", "site allowance"]
      }
    },
    "rate_label": {
      "type": ["string", "null"],
      "description": "Name of the allowance when rate_type='allowance' (e.g. 'Travel', 'Productivity', 'Excess Travel'). Null for hourly role rates.",
      "x-eq-source-aliases": ["allowance", "allowance_type", "label", "line_item"]
    },
    "cost_rate": {
      "type": "number", "minimum": 0,
      "description": "Cost rate we pay the agency, AUD, GST-exclusive. On invoices this is the Unit Cost / Unit Price column. Sensitive — hidden from non-manager roles. Strip currency symbols on import.",
      "x-eq-source-aliases": ["rate", "cost", "cost_rate", "hourly_rate", "pay_rate", "amount", "price", "unit_rate", "unit cost", "unit price"],
      "x-eq-sensitive": true
    },
    "unit": {
      "type": "string", "enum": ["hour", "day", "each"], "default": "hour",
      "description": "Basis of the rate. Allowances are often per-occurrence ('each').",
      "x-eq-source-aliases": ["unit", "per", "basis", "uom", "qty type"],
      "x-eq-enum-aliases": {
        "hour": ["hr", "hourly", "/hr", "per hour", "p/h", "ph"],
        "day":  ["daily", "/day", "per day", "day rate"],
        "each": ["ea", "unit", "per unit", "occurrence", "each"]
      }
    },
    "source_doc_type": {
      "type": "string", "enum": ["rate_card", "invoice", "manual"], "default": "rate_card",
      "description": "Provenance of the rate. 'rate_card' = a locked quote/rate sheet (authoritative). 'invoice' = observed on an invoice line (point-in-time, role may be inferred — lower trust). Set at upload from the document class.",
      "x-eq-required-on-import": false
    },
    "effective_from": {
      "type": "string", "format": "date",
      "description": "Date this locked rate takes effect. Parse AU dd/mm/yyyy.",
      "x-eq-source-aliases": ["effective_from", "effective", "valid_from", "start", "from", "date", "effective_date", "commencing"]
    },
    "effective_to": {
      "type": ["string", "null"], "format": "date",
      "description": "Date the rate expires. Null = current / open-ended.",
      "x-eq-source-aliases": ["effective_to", "valid_to", "expiry", "expires", "until", "to", "end"]
    }
  },
  "x-eq-cross-field-rules": [
    {
      "id": "effective_window_valid",
      "rule": "effective_to == null OR effective_from == null OR effective_to >= effective_from",
      "message": "Effective-to is before effective-from. Confirm the dates.",
      "severity": "warning"
    }
  ]
}
```

**`labour-hire-company.schema.json`** (companion — usually managed via the UI, but importable)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.eq.solutions/ops/labour-hire-company/v1.json",
  "title": "Labour Hire Company",
  "description": "A labour hire firm we source workers from. Vendor entity that rate cards hang off.",
  "type": "object",
  "x-eq-entity": "labour_hire_company",
  "x-eq-module": "ops",
  "x-eq-version": "1.0.0",
  "x-eq-table": "labour_hire_companies",
  "required": ["company_id", "tenant_id", "name", "active"],
  "properties": {
    "company_id": {
      "type": "string", "format": "uuid",
      "x-eq-source-aliases": ["id", "company_id"], "x-eq-required-on-import": false
    },
    "tenant_id": { "type": "string", "format": "uuid", "x-eq-required-on-import": false },
    "name": {
      "type": "string", "description": "Trading name of the labour hire firm.",
      "x-eq-source-aliases": ["name", "company", "agency", "supplier", "vendor", "firm", "business_name"]
    },
    "abn":    { "type": ["string", "null"], "x-eq-source-aliases": ["abn", "acn", "business_number"] },
    "primary_contact": {
      "type": ["string", "null"], "description": "Account manager / main contact at the agency.",
      "x-eq-source-aliases": ["contact", "account_manager", "attention", "rep", "primary_contact"]
    },
    "contact_email": {
      "type": ["string", "null"], "format": "email",
      "x-eq-source-aliases": ["email", "contact_email", "e-mail", "accounts_email"]
    },
    "contact_phone": {
      "type": ["string", "null"],
      "x-eq-source-aliases": ["phone", "tel", "telephone", "mobile", "contact_phone"]
    },
    "address":       { "type": ["string", "null"], "x-eq-source-aliases": ["address", "office", "registered_office"] },
    "payment_terms": { "type": ["string", "null"], "x-eq-source-aliases": ["terms", "payment_terms", "payment terms"] },
    "active": { "type": "boolean", "default": true },
    "notes":  { "type": ["string", "null"], "x-eq-source-aliases": ["notes", "comment", "remarks"] }
  }
}
```

### 4.2 Upload UX (the important bit)

A rate card is **per-firm** — the company is document-level context, not a per-row column. So the upload flow:

1. User picks **which labour hire company** this doc is from (from the existing list, or "add new" → creates a
   `labour_hire_companies` row). That `company_id` is stamped onto every extracted rate row.
2. User picks the **document class** — *Rate card* or *Invoice* — which sets `source_doc_type` on every row. (Default
   inferred from the doc: a "TAX INVOICE" heading → invoice.)
3. Intake vision-extracts the rows and column-maps to the schema. **Matrix expansion:** a rate-card row with
   Normal / T½ / Double columns emits **one canonical row per rate_type** (Madagins Licensed Electrician → 3 rows).
4. If the sheet carries a company column, the FK fuzzy-match (`x-eq-fk-fuzzy-match-on: name`) resolves it and the
   column-mapping confirmation step catches mismatches — same mechanism `staff.default_site_id` uses for sites.

**Two document classes, two extraction profiles:**

| Class | Example | Extraction | Trust |
|---|---|---|---|
| **Rate card / quote** | Madagins Rates 2026 | Clean role×rate_type grid → high-confidence matrix expansion. The primary intended input. | Authoritative (`rate_card`). |
| **Invoice** | Core INV0015034, NSW 2022 | Rate = Unit Cost column; **role inferred from the free-text line description** (vision-extraction §02, `raw_text` anchor). Allowances captured as `allowance` rows. | Observation (`invoice`) — validates against / flags drift from the card, but a card supersedes it. |

---

## 5. EQ Ops surface (eq-shell)

_Grounded in eq-ui (`@eq-solutions/ui` v1.10) + eq-design-tokens, verified 2026-07-05 — see §5.1._

For **project managers + upper management** to glance at "who we use, how to reach them, and what we pay." Built from
the real EQ component library, mirroring `src/pages/AdminUserList.tsx`:

- **Wrapper**: `<HubLayout>` + `eq-page__header` / `eq-page__title` / `eq-page__lede` (the shell's standard page header).
- **Gate** (outer): new permission `ops.view_rates`, granted to **management-type roles** (`manager` + any
  project-manager role present in `src/permissions/matrix.ts` — confirm exact keys at build; `labour_hire` stays empty).
  `<Gate perm="ops.view_rates" fallback={<NotAllowed/>}>`. The gate is what lets PMs see sensitive cost (R3) without
  opening it to everyone.
- **Two flat `<Table>` sections** (the eq-ui Table is **flat — no nested/expandable rows**, verified in `Table.tsx`),
  one per grain, because contacts are per-agency and rates are per-agency×role×rate_type:
  1. **Agencies** — `name`, `primary_contact`, `contact_phone`, `contact_email`, `payment_terms`. The "who / how to
     reach them."
  2. **Rates** — `company_name`, `role`, `rate_type` + `source_doc_type` as `eq-pill` badges, `cost_rate`
     (`align: 'right'`, `$${n.toFixed(2)}`), `unit`, `effective_from`, `is_current`. `globalSearch` on company+role,
     `slicers` **Current** / All / Expired, `columnToggle`, `exportable` (managers get CSV for free), `defaultSort` by
     company. `is_current` false → muted row via `rowStyle`.

  (Stack the two sections on one page, or split with the eq-ui `<Tabs>` — Rates | Agencies. Either is native and flat.)

**Two reads** (`createTenantDataClient()` → `.from()` auto-routes to `app_data`):

```tsx
const sb = await createTenantDataClient();
const { data: companies } = await sb
  .from('labour_hire_companies')
  .select('company_id, name, primary_contact, contact_email, contact_phone, payment_terms, active')
  .eq('active', true)
  .order('name');
const { data: rates } = await sb
  .from('labour_hire_rates_view')
  .select('*')
  .order('company_name');
```

A ready-to-drop reference component is staged at
[`labour-hire-rates-build/LabourHireRates.tsx`](labour-hire-rates-build/LabourHireRates.tsx).

### 5.1 eq-ui fit (verified)

| Need | eq-ui provides | Note |
|---|---|---|
| Data table | **`Table` / `TableColumn<T>`** (v1.4) | `columns`, `rows`, `globalSearch`, `slicers`, `columnToggle`, `exportable`, `align:'right'`, `loading`/`loadingRows`, `rowStyle`, `defaultSort`, `persistKey`. Everything the tab needs — no custom table. |
| Row/status badge | **`eq-pill`** CSS classes (`--info`/`--ok`/`--mute`, in eq-shell `App.css`) | `rate_type` + `source_doc_type` render as pills. `StatusBadge`/`KindPill` exist but their enums don't fit these dimensions — use `eq-pill`. |
| Page shell | **`HubLayout`**, `eq-page__*` classes | Same as every admin page. |
| Gate | **`<Gate perm=…>`** | Existing permission wrapper. |
| Brand | **eq-design-tokens** `--eq-*` (Plus Jakarta Sans via `--eq-font-stack`, `--eq-ink`/`--eq-sky`/`--eq-ice`) | Style with tokens only — no hardcoded colours, no gradients/shadows (matches EQ brand). |
| Expand agency → rates | **Not supported** (flat table) | Hence two flat sections, not a drill-down. This corrected the earlier draft. |

---

## 6. Affected files & migrations

Artifacts marked **✅ staged** are written and ready in
[`labour-hire-rates-build/`](labour-hire-rates-build/) — drop-in, nothing applied. Code items (the tab, nav,
matrix, upload) are written in-repo against live conventions.

| # | Repo | File / artifact | Action |
|---|---|---|---|
| 1 | eq-shell | `supabase/tenant-migrations/0162_labour_hire_rates.sql` | **✅ staged** — §3 tables + RLS + grants + view + registry; applies to ehow (zaap Phase 4) via the governed pipeline |
| 2 | eq-intake | `eq-platform/packages/eq-schemas/src/schemas/labour-hire-rate.schema.json` | **✅ staged** — §4.1 |
| 3 | eq-intake | `eq-platform/packages/eq-schemas/src/schemas/labour-hire-company.schema.json` | **✅ staged** — §4.1 |
| 4 | eq-intake | (build) `packages/eq-schemas` generate → `eq_schema_registry` | regenerate types/Zod, sync registry |
| 5 | eq-intake | upload flow / entity picker | **edit** — add `labour_hire_rate` entity + per-document company + doc-class selection (§4.2) |
| 6 | eq-shell | `src/permissions/matrix.ts` | **edit** — add `ops.view_rates` to management-type roles (§5) |
| 7 | eq-shell | `src/modules/ops/LabourHireRates.tsx` | **new** — the tab (§5) |
| 8 | eq-shell | `src/App.tsx` (`ops/*` routes) + Ops nav | **edit** — route + nav entry for the tab |
| — | ehow | `labour-hire-rates-build/seed_madagins_core.sql` | **✅ staged** — illustrative Madagins + Core seed; run after #1 applies |

**Migration apply note:** per `suite-state.md`, the eq-shell One-Pipe apply currently aborts on **checksum drift**
(0084 sks / 0072 eq) before reaching 0159. This migration inherits that blocker — it will not apply until the drift
is reconciled (`allow_checksum_drift=true` / `reconcile_ledger`). Confirm the pipeline is unblocked before scheduling.

**Sequencing:** 1 (tables) → 2–4 (schemas/registry) → 5 (Intake upload) → 6–8 (Ops tab). Tab can be built against
the tables before Intake upload is wired (seed a couple of rows manually to develop against).

---

## 7. Pre-mortem — 3 risks + mitigations

| # | Risk | Mitigation |
|---|---|---|
| R1 | **Intake is in-build, unproven for this doc type** (`eq_intake_staging` = 0 rows). Rate cards need **matrix expansion** (one row → N rate_type rows) and invoices need **role inference from free-text** — neither is exercised yet. | Pilot the 3 real samples (Madagins card, Madagins + Core invoices) end-to-end **before** wiring the Ops "upload" button — they're the gold set. Keep a manual-insert path (`source_doc_type='manual'`) so the tab has value even if Intake needs iteration. |
| R1b | **Invoice role inference is lossy** — "CORE EL - Mascot DC" → which canonical role? Wrong inference silently mis-files a rate. | Invoice rows land as `source_doc_type='invoice'` and route through the column-mapping `needs_clarification` step (role confidence <0.7 → confirm before commit). A rate card, when later uploaded, supersedes invoice observations for the same role. |
| R2 | **Company identity fragmentation** — fuzzy FK + repeat uploads spawn duplicate firms ("Agency A" vs "Agency A Pty Ltd"). | `unique(tenant_id, name)`; force company **selection from the existing list** at upload (add-new is deliberate); surface the fuzzy-match candidate for confirmation before commit. |
| R3 | **`cost_rate` is commercially sensitive** — what we pay agencies leaking to non-managers. | `x-eq-sensitive: true`; `ops.view_rates` gated to `manager`; view read only under tenant-scoped `authenticated`; `labour_hire` role has no perms. No public/anon grant. |

---

## 8. Out of scope / deferred

- **EQ Intake auto-upload — deferred to a fast-follow** (lean decision, 2026-07-05). v1 feeds the tables by a manual
  seed (the two schemas + upload UX in §4 are designed and staged, just not wired yet). Rationale: Intake is unproven
  for this doc type (`eq_intake_staging` = 0 rows); the tables + tab deliver value without it. Schemas still ship into
  the DB registry via 0162 so the entities are registered when Intake is wired later.
- **Charge-out & margin** — Royce's call: cost-only. No `charge_rate`/`margin` columns. (Note: `sks_comms_labour_rates`
  already tracks a charge_rate for comms — keep the two from drifting if charge-out is added later.)
- **Field consuming these rates** for assignment/dispatch costing — future; the canonical home makes it a later read,
  not a rebuild.
- **Manage-in-tab editing UI** — v1 is manual seed + read (Ops tab). Inline add/edit is a fast-follow.

---

## 9. Open decisions for Royce

1. ✅ **Allowances** — **DECIDED (Royce, 2026-07-05): capture** as `rate_type='allowance'` rows, named in `rate_label`. True cost stays complete.
2. ✅ **Invoice-derived rates** — **DECIDED (Royce, 2026-07-05): allow, tagged `invoice`.** Royce: "use invoice for now, update with rate card when available." → the **supersede rule** (below) is required, not optional.
3. ✅ **Module tag** `x-eq-module` = **`ops`** — locked (defaults accepted, Royce 2026-07-05).
4. ✅ **Permission** = **new `ops.view_rates`**, granted to management-type roles (manager + PM) per §5 — locked.
5. ✅ **Amount storage** = **`numeric(10,2)` AUD** — locked.
6. ✅ **Seed from `sks_comms_labour_rates`** = **no**, start clean from real uploads — locked.

_All open decisions resolved. Spec is final pending build authorisation._

**Supersede rule (from decision 2):** on import of a `rate_card` row for a `(company, role, rate_type)` that already
has a *current* `invoice`-sourced row, close the invoice row (`effective_to = new.effective_from - 1`, `active=false`)
rather than deleting it — the invoice observation stays as history, the locked card becomes current. A later card
supersedes an earlier card the same way. Enforced in the Intake commit path (`eq_intake_commit_batch`), not by trigger,
so the lineage/audit rows capture the supersession. The `is_current` flag in the view already reflects the result.

_(Rate unit is no longer a question — the matrix is handled by `rate_type`; `unit` now covers hour/day/each for the allowance case.)_

---

_End of spec. Nothing in this document has been applied to any database or code repo._

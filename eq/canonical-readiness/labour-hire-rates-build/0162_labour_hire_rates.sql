-- 0162_labour_hire_rates.sql
-- Target:    ehow (sks) only in Phase 1. zaap dispatched in Phase 4
--            when EQ Ops goes live on the EQ plane (mirrors 0147).
-- Purpose:   Canonical home for labour-hire COST rates + the agencies we source
--            from, so project / upper management can view "who we use, how to
--            reach them, and what we pay" in a simple EQ Ops tab. Fed by EQ Intake
--            (upload a rate PDF / invoice → parse → rows); manual path retained.
--
--            Scope (locked 2026-07-05, Royce):
--              Cost only — what we pay the agency. No charge-out / margin.
--              rate_type   ∈ normal | time_and_half | double | allowance   (the rate matrix)
--              unit        ∈ hour | day | each
--              source_doc_type ∈ rate_card | invoice | manual              (provenance / trust)
--            Derived from 3 real SKS agency PDFs (Madagins rate card, Madagins +
--            Core invoices): rate cards carry Normal/T½/Double per role → one row
--            per rate_type; invoices are a valid but weaker source (role inferred
--            from free-text, superseded by a card when one arrives).
--
--            cost_rate is COMMERCIALLY SENSITIVE. Grant model (per 0147_issues):
--            authenticated = SELECT only, tenant-scoped; all writes via service_role
--            (Intake emit RPC eq_intake_commit_batch) or a definer RPC. The EQ Ops
--            `ops.view_rates` permission is the UI visibility gate; RLS enforces
--            tenant isolation. (Fast-follow option: wrap the read in a permission-
--            checking definer RPC if authenticated-but-non-manager read must be
--            blocked at the DB, not just the UI.)
--
--            Intake-native: external_id + intake_id present from day one so Intake
--            can emit rows without losing provenance.
--
-- Idempotent: all DDL uses IF NOT EXISTS / DO $$ checks.

-- ── Companies ─────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS app_data.labour_hire_companies (
  company_id       uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id        uuid        NOT NULL DEFAULT ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid),
  name             text        NOT NULL,
  abn              text,
  -- contact + reference info (surfaced on the tab)
  primary_contact  text,
  contact_email    text,
  contact_phone    text,
  address          text,
  payment_terms    text,
  active           boolean     NOT NULL DEFAULT true,
  notes            text,
  -- intake lineage
  external_id      text,
  intake_id        uuid,
  imported_from    text,
  imported_at      timestamptz,
  schema_version   text,
  created_at       timestamptz NOT NULL DEFAULT now(),
  updated_at       timestamptz NOT NULL DEFAULT now(),
  created_by       uuid,
  updated_by       uuid,
  CONSTRAINT labour_hire_companies_tenant_name_key UNIQUE (tenant_id, name)
);

CREATE INDEX IF NOT EXISTS labour_hire_companies_tenant_idx
  ON app_data.labour_hire_companies (tenant_id, active);

-- ── Rates ─────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS app_data.labour_hire_rates (
  rate_id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id        uuid        NOT NULL DEFAULT ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid),
  company_id       uuid        NOT NULL REFERENCES app_data.labour_hire_companies(company_id) ON DELETE RESTRICT,
  role             text        NOT NULL,
  rate_type        text        NOT NULL DEFAULT 'normal'
                     CHECK (rate_type IN ('normal', 'time_and_half', 'double', 'allowance')),
  rate_label       text,       -- allowance name when rate_type = 'allowance' (e.g. 'Travel')
  cost_rate        numeric(10,2) NOT NULL,           -- AUD, GST-exclusive, what we pay the agency
  unit             text        NOT NULL DEFAULT 'hour' CHECK (unit IN ('hour', 'day', 'each')),
  source_doc_type  text        NOT NULL DEFAULT 'rate_card'
                     CHECK (source_doc_type IN ('rate_card', 'invoice', 'manual')),
  effective_from   date        NOT NULL DEFAULT current_date,
  effective_to     date,       -- null = current / open-ended
  active           boolean     NOT NULL DEFAULT true,
  notes            text,
  -- intake lineage
  external_id      text,
  intake_id        uuid,
  imported_from    text,
  imported_at      timestamptz,
  schema_version   text,
  created_at       timestamptz NOT NULL DEFAULT now(),
  updated_at       timestamptz NOT NULL DEFAULT now(),
  created_by       uuid,
  updated_by       uuid,
  CONSTRAINT labour_hire_rates_effective_window_chk
    CHECK (effective_to IS NULL OR effective_to >= effective_from)
);

-- Primary lookup: a firm's rates by role + matrix cell
CREATE INDEX IF NOT EXISTS labour_hire_rates_company_role_idx
  ON app_data.labour_hire_rates (tenant_id, company_id, role, rate_type);

-- Current-rate sweep
CREATE INDEX IF NOT EXISTS labour_hire_rates_current_idx
  ON app_data.labour_hire_rates (tenant_id, company_id)
  WHERE active AND effective_to IS NULL;

-- ── Grants + RLS ──────────────────────────────────────────────────────────────
-- authenticated: SELECT only (tenant-scoped). All writes via service_role / RPC.

GRANT SELECT, INSERT, UPDATE, DELETE ON app_data.labour_hire_companies TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_data.labour_hire_rates     TO service_role;
GRANT SELECT ON app_data.labour_hire_companies TO authenticated;
GRANT SELECT ON app_data.labour_hire_rates     TO authenticated;
REVOKE INSERT, UPDATE, DELETE ON app_data.labour_hire_companies FROM anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON app_data.labour_hire_rates     FROM anon, authenticated;

ALTER TABLE app_data.labour_hire_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_data.labour_hire_rates     ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'app_data' AND tablename = 'labour_hire_companies'
      AND policyname = 'labour_hire_companies_select'
  ) THEN
    CREATE POLICY labour_hire_companies_select ON app_data.labour_hire_companies
      FOR SELECT TO authenticated
      USING (tenant_id = ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid));
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'app_data' AND tablename = 'labour_hire_rates'
      AND policyname = 'labour_hire_rates_select'
  ) THEN
    CREATE POLICY labour_hire_rates_select ON app_data.labour_hire_rates
      FOR SELECT TO authenticated
      USING (tenant_id = ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid));
  END IF;
END $$;

-- ── View (the tab's rate read) ────────────────────────────────────────────────
-- security_invoker = on → caller's RLS applies, so the join stays tenant-scoped.

CREATE OR REPLACE VIEW app_data.labour_hire_rates_view AS
  SELECT
    r.rate_id,
    r.tenant_id,
    r.company_id,
    c.name            AS company_name,
    r.role,
    r.rate_type,
    r.rate_label,
    r.cost_rate,
    r.unit,
    r.source_doc_type,
    r.effective_from,
    r.effective_to,
    ( r.active
      AND r.effective_from <= current_date
      AND (r.effective_to IS NULL OR r.effective_to >= current_date) ) AS is_current,
    r.updated_at
  FROM app_data.labour_hire_rates r
  JOIN app_data.labour_hire_companies c ON c.company_id = r.company_id;

ALTER VIEW app_data.labour_hire_rates_view SET (security_invoker = on);
GRANT SELECT ON app_data.labour_hire_rates_view TO authenticated;

-- ── Schema registry (mirrors 0147) ────────────────────────────────────────────

DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'shell_control' AND table_name = 'eq_schema_registry'
  ) THEN
    INSERT INTO shell_control.eq_schema_registry (entity, module, version, schema_json, description, is_current)
    VALUES
      (
        'labour_hire_company', 'ops', '1.0.0',
        '{"x-eq-entity":"labour_hire_company","x-eq-module":"ops","x-eq-version":"1.0.0","x-eq-table":"labour_hire_companies","type":"object","description":"A labour hire firm we source workers from. Rate cards hang off it.","required":["company_id","tenant_id","name","active"]}'::jsonb,
        'Labour hire agencies (contact + terms). Rate cards/invoices attach to these.',
        true
      ),
      (
        'labour_hire_rate', 'ops', '1.0.0',
        '{"x-eq-entity":"labour_hire_rate","x-eq-module":"ops","x-eq-version":"1.0.0","x-eq-table":"labour_hire_rates","type":"object","description":"A locked-in cost rate for a role from a labour hire company. One row per company x role x rate_type x period. Cost only.","required":["rate_id","tenant_id","company_id","role","rate_type","cost_rate","effective_from"]}'::jsonb,
        'Labour hire cost rates (Normal/T-and-half/Double/allowance) per agency + role.',
        true
      )
    ON CONFLICT (entity, version) DO UPDATE
      SET module = excluded.module, description = excluded.description, is_current = excluded.is_current;
  END IF;
END $$;

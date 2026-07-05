-- seed_madagins_core.sql
-- Illustrative seed from 3 real SKS agency PDFs, so the EQ Ops tab has content on
-- day one. STAGED — do NOT run until 0162_labour_hire_rates.sql is applied on ehow.
-- Run as service_role (SQL editor / MCP), NOT as an authenticated user (writes are
-- revoked from authenticated by 0162).
--
--   Madagins Rates 2026.pdf  → rate_card  (authoritative)
--   Core - INV0015034.pdf    → invoice    (role inferred from line description)
--   NSW 2022.pdf             → Madagins invoice; corroborates the card ($80.79 NT) — not re-seeded.
--
-- tenant_id = SKS Technologies on ehow (per suite-state.md).

-- ── Companies ─────────────────────────────────────────────────────────────────

INSERT INTO app_data.labour_hire_companies
  (tenant_id, name, abn, primary_contact, contact_email, contact_phone, address, payment_terms, notes)
VALUES
  ('7dee117c-98bd-4d39-af8c-2c81d02a1e85'::uuid,
   'Madagins Pty Ltd', '43 671 869 962', 'Ciaran', 'ciaran@madagins.com.au', NULL,
   'Level 2, 332-334 Oxford Street, Bondi Junction NSW 2022', '30 days from invoice',
   'Rate card 29/06/26, valid 30 days. 4hr min per person. Rates GST-exclusive. Site allowances additional.'),
  ('7dee117c-98bd-4d39-af8c-2c81d02a1e85'::uuid,
   'Core Talent Pty Ltd', '11159863073', NULL, 'accounts@coretalent.com.au', '02 8203 5499',
   'Level 39, 259 George Street, Sydney NSW 2000', '14 days (late interest 8%)',
   'ABN/ACN shown as a single number on invoice — verify. Invoices factored via Astute. EFT: Core Talent Pty Ltd BSB 032-143 Acct 297477.')
ON CONFLICT (tenant_id, name) DO NOTHING;

-- ── Madagins rate card (rate_card, effective 2026-06-29) ──────────────────────

INSERT INTO app_data.labour_hire_rates
  (tenant_id, company_id, role, rate_type, cost_rate, unit, source_doc_type, effective_from)
SELECT
  '7dee117c-98bd-4d39-af8c-2c81d02a1e85'::uuid,
  (SELECT company_id FROM app_data.labour_hire_companies
     WHERE tenant_id = '7dee117c-98bd-4d39-af8c-2c81d02a1e85'::uuid AND name = 'Madagins Pty Ltd'),
  v.role, v.rate_type, v.cost_rate, 'hour', 'rate_card', DATE '2026-06-29'
FROM (VALUES
  ('NSW Licensed Electrician', 'normal',        80.79),
  ('NSW Licensed Electrician', 'time_and_half', 105.88),
  ('NSW Licensed Electrician', 'double',        137.43),
  ('NSW Tradesperson Cert',    'normal',        71.06),
  ('NSW Tradesperson Cert',    'time_and_half', 92.88),
  ('NSW Tradesperson Cert',    'double',        120.41),
  ('Grade 4 Trade Assistant',  'normal',        68.26),
  ('Grade 4 Trade Assistant',  'time_and_half', 89.16),
  ('Grade 4 Trade Assistant',  'double',        115.54),
  ('Grade 2 Trade Assistant',  'normal',        59.15),
  ('Grade 2 Trade Assistant',  'time_and_half', 75.64),
  ('Grade 2 Trade Assistant',  'double',        98.72)
) AS v(role, rate_type, cost_rate);

-- ── Core Talent invoice (invoice, week ending 2026-06-21; role inferred 'CORE EL') ──

INSERT INTO app_data.labour_hire_rates
  (tenant_id, company_id, role, rate_type, rate_label, cost_rate, unit, source_doc_type, effective_from, notes)
SELECT
  '7dee117c-98bd-4d39-af8c-2c81d02a1e85'::uuid,
  (SELECT company_id FROM app_data.labour_hire_companies
     WHERE tenant_id = '7dee117c-98bd-4d39-af8c-2c81d02a1e85'::uuid AND name = 'Core Talent Pty Ltd'),
  'Electrician', v.rate_type, v.rate_label, v.cost_rate, v.unit, 'invoice', DATE '2026-06-21',
  'INV0015034; worker Shihab Al-gburi; site Mascot DC; wk ending 21 Jun 2026'
FROM (VALUES
  ('normal',        NULL,           70.07,  'hour'),
  ('time_and_half', NULL,           93.34,  'hour'),
  ('double',        NULL,           122.45, 'hour'),
  ('allowance',     'Productivity', 2.20,   'hour'),
  ('allowance',     'Travel',       28.60,  'each'),
  ('allowance',     'Excess Travel',19.80,  'day')
) AS v(rate_type, rate_label, cost_rate, unit);

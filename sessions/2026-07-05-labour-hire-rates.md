---
title: Session — Labour Hire Rates (canonical design + staged lean build)
date: 2026-07-05
tier: EQ
repo: eq-context (design) → eq-shell + eq-intake (build targets)
status: design approved, build staged, not applied
---

# Labour Hire Rates — canonical design + staged lean build

## Ask
Royce: where to store the cost rates for the labour hire firms SKS uses, viewable by
project / upper management. Evolved to: a simple EQ Ops tab showing rates, contacts, and
relevant info, fed (eventually) by uploading agency PDFs to EQ Intake.

## What was decided
- **Canonical home, not Field or reports.** Rates are commercial reference data → two new
  tables in `app_data` on ehow, owned via a Shell tenant-migration. Verified live that every
  rate table already lives in `app_data` (rate_library, quote_rate_presets, sks_comms_labour_rates);
  none in Field. Reports/tabs consume, they don't store.
- **Cost only** — what we pay the agency. No charge-out / margin.
- **Rate matrix, not a scalar.** Three real SKS PDFs (Madagins rate card, Madagins + Core
  invoices) proved rates come as Normal / Time-and-a-half / Double per role, plus allowances →
  `rate_type` dimension + `rate_label`. One card row expands to N canonical rows.
- **Invoices are a valid source**, tagged `source_doc_type='invoice'` (role inferred from the
  free-text line), superseded by a `rate_card` when one arrives. Royce: "use invoice for now,
  update with rate card when available."
- **Grant model tightened** to match `0147_issues`: `authenticated` = SELECT only, writes via
  `service_role` / Intake. `ops.view_rates` is the UI gate; RLS enforces tenant isolation.
- **Ops tab grounded in real eq-ui** (`Table` v1.4 + tokens): the eq-ui Table is **flat**, so the
  "expand agency → rates" idea was dropped in favour of **two flat tables** (Agencies + Rates).
- **LEAN build path (Royce 2026-07-05):** v1 = tables + tab + **manual seed**; EQ Intake
  auto-upload **deferred** to a fast-follow (unproven for this doc type; `eq_intake_staging` = 0 rows).

## Canonical audit — PASSED
app_data on ehow via Shell migration · tenant RLS on JWT claim · security_invoker view · writes via
service_role/Intake · dual-plane (ehow now, zaap Phase 4) · `shell_control.eq_schema_registry` exists ·
no duplication of existing canonical or Field. Two benign ambers: the eq-shell migration pipeline is
blocked on checksum drift (parked to the concurrent eq-shell session, not ours), and the eq-intake
schema-registry mirror should be confirmed not to clash at build.

## Delivered (staged in `eq/canonical-readiness/`)
- `labour-hire-rates-canonical-design-2026-07-04.md` — full spec (APPROVED — lean build).
- `labour-hire-rates-build/`:
  - `0162_labour_hire_rates.sql` — 2 tables + indexes + RLS + view + registry (0147 style; 0162 = next free).
  - `seed_madagins_core.sql` — v1 feed, Madagins card (12 rows) + Core invoice (6 rows incl. 3 allowances).
  - `LabourHireRates.tsx` — the tab, two flat eq-ui Tables, `<Gate perm="ops.view_rates">`, eq-pill badges.
  - `labour-hire-rate.schema.json` / `labour-hire-company.schema.json` — Intake schemas (deferred).
  - `README.md` — lean apply order + blocker.

## Critical path / next
1. eq-shell session clears the **checksum-drift** blocker → `0162` applies to ehow via the governed pipeline.
2. Run `seed_madagins_core.sql` → tab has content.
3. Drop `LabourHireRates.tsx` into `eq-shell/src/modules/ops/`, add `ops.view_rates` to matrix, wire route.
4. (Fast-follow) wire EQ Intake upload.

Nothing was applied to any live DB or code repo. Design + staged artifacts only, on branch
`claude/pensive-burnell-fca8d9`.

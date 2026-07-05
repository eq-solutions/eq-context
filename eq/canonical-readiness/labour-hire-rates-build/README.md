# Labour Hire Rates — staged build artifacts

Ready-to-drop artifacts for the [labour hire rates design spec](../labour-hire-rates-canonical-design-2026-07-04.md).
**Nothing here has been applied or committed to a code repo** — staged in eq-context so it can drop into eq-shell /
eq-intake and apply once the eq-shell migration pipeline is unblocked (see Blocker below).

_Staged 2026-07-05. Grounded in 3 real SKS agency PDFs (Madagins rate card, Madagins + Core invoices)._

> **Build path: LEAN (Royce, 2026-07-05).** v1 = tables + tab + **manual seed**. EQ Intake auto-upload is **deferred** —
> the two `.schema.json` still ship into the DB registry via 0162 (so the entities are registered), but the upload flow
> is a fast-follow, not v1. Steps 1–4 below are v1; step 5 is deferred.

## Files

| File | Drops into | What it is |
|---|---|---|
| `0162_labour_hire_rates.sql` | `eq-shell/supabase/tenant-migrations/` | The migration — 2 tables (`app_data.labour_hire_companies`, `app_data.labour_hire_rates`) + indexes + tenant RLS (SELECT-only to `authenticated`, writes via `service_role`) + `labour_hire_rates_view` + `shell_control.eq_schema_registry` inserts. Style matches `0147_issues_table.sql`. **0162 is the next free number as of 2026-07-05 (latest on main = 0161)** — re-check before committing. |
| `seed_madagins_core.sql` | run manually on ehow (SQL editor / MCP, as `service_role`) **after** 0162 applies | **v1 feed** — content from the 3 PDFs so the tab isn't empty. Madagins = rate_card, Core = invoice. |
| `LabourHireRates.tsx` | `eq-shell/src/modules/ops/` | **v1 tab** — two flat eq-ui `<Table>` sections (Agencies + Rates), `<Gate perm="ops.view_rates">`, `eq-pill` badges. Confirm import paths against the repo. |
| `labour-hire-rate.schema.json` | `eq-intake/…/eq-schemas/src/schemas/` | _(Deferred)_ Intake schema for the rate entity (rate_type matrix, allowances, source_doc_type, FK fuzzy-match). |
| `labour-hire-company.schema.json` | `eq-intake/…/eq-schemas/src/schemas/` | _(Deferred)_ Intake schema for the agency entity (contact + terms). |

## Apply order (v1 = lean)

1. **0162** → commit to eq-shell, apply via the governed pipeline (ehow now; zaap when EQ Ops goes live on the EQ plane).
2. **Seed** → run `seed_madagins_core.sql` on ehow to populate Madagins + Core.
3. **Tab component** → drop `LabourHireRates.tsx` into `eq-shell/src/modules/ops/`; confirm the import paths.
4. **Wire the tab** →
   - `src/permissions/matrix.ts` — add `ops.view_rates` to management-type roles (`manager` + PM).
   - `src/App.tsx` + Ops nav — route + nav entry pointing at `LabourHireRates`.

**Deferred (fast-follow — NOT v1):**

5. **Intake upload** (spec §4.2) — drop the 2 `.schema.json` into eq-intake, run `packages/eq-schemas` generate
   (`scripts/generate.ts`) to regenerate TS/Zod + mirror the full schema into the registry, then add the
   `labour_hire_rate` entity to the upload flow with per-document company + doc-class selection and matrix expansion.
   (0162 already registers a compact schema stub; the build upserts the full version via `ON CONFLICT`.)

## Blocker

Per `suite-state.md`, the eq-shell One-Pipe apply currently **aborts on checksum drift (0084 sks / 0072 eq)** before
reaching 0159, so 0162 will not apply until the drift is reconciled (`allow_checksum_drift=true` / `reconcile_ledger`).
Royce parked that reconciliation to the concurrent eq-shell session (2026-07-04). Confirm the pipeline is clear before
scheduling the apply.

## Notes / verify before apply

- **tenant_id** in the seed = SKS on ehow (`7dee117c-98bd-4d39-af8c-2c81d02a1e85`, from suite-state).
- **Core ABN** — invoice prints one number labelled "ACN / ABN"; captured as-is, flagged in `notes` to verify.
- **Grant model** is tighter than spec §3.4's first draft: `authenticated` gets SELECT only (not full DML). Writes go
  through `service_role` (Intake emit) — matches `0147_issues`. `ops.view_rates` is the UI visibility gate; RLS enforces
  tenant isolation. If cost_rate must be hidden from authenticated-but-non-manager at the DB layer, wrap the read in a
  permission-checking definer RPC (fast-follow).
- **Supersede rule** (invoice → rate_card): implement in the Intake commit path (`eq_intake_commit_batch`), not a
  trigger, so lineage captures the supersession. See spec §9.

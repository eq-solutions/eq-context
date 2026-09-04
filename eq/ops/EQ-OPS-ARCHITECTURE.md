---
title: EQ Ops — Quotes, Jobs, and the Canonical Job Number
owner: Royce Milmlow
last_updated: 2026-09-04
scope: Authoritative reference for EQ Ops' scope, its relationship to NSW Comms and EQ Field, and the current state of the quote-to-job data model. Read before any work that touches app_data.quote, app_data.jobs, job_number, or the Kanban board's stage taxonomy.
read_priority: critical
status: live
---

# EQ Ops — Quotes, Jobs, and the Canonical Job Number

> **Re-verified live 2026-09-04** — ehow `app_data.quote` / `app_data.jobs` / `app_data.sks_comms_jobs` counts, `pg_constraint` on `app_data.jobs`, the `quote.status` CHECK, the `app_data.field_job_numbers` view and its `field_job_numbers_src()` function, and eq-shell `origin/main` (`src/modules/quotes/QuotesModule.tsx`, `supabase/tenant-migrations/0236`–`0237`, `0275`). The 2026-08-03 version of this file described a live sync bug and a 25-row gap. Both were fixed on 2026-08-03/04 (§4); the numbers and the open list below are today's.

## 1. The principle in one sentence

EQ Ops is meant to become the canonical quoting/job engine for SKS's **electrical** trade, with `job_number` as the shared key that lets Field, Ops, and (eventually) NSW Comms all agree on "what jobs currently exist" without hand-reconciling separate lists.

## 2. Scope boundary — Ops is not Comms (Royce, 2026-08-03)

**EQ Ops = electrical.** NSW Comms is a deliberately separate, larger, structurally different trade (cabling/telco — `app_data.sks_comms_jobs` has telco-specific columns like `mop_received`, `pre_cable_done`, `post_dock_done`). Royce: "having it mixed in with Ops... wouldn't work." When this was decided the volume gap was ~10× (153 Comms rows vs ~38 real electrical jobs); on 2026-09-04 it is 153 Comms rows vs 232 Ops quotes / 96 canonical jobs — the gap has narrowed, the structural separation stands.

**`job_number`/`quote_ref` on `sks_comms_jobs` are forward-compatibility wiring, not a live dependency.** They exist so that *if* the Comms team ever starts quoting through EQ Ops, the numbering already ties together — not because Comms currently reads from or writes to Ops' tables. `sks_comms_jobs` has its own `source`/`source_ref`/`imported_at` columns, consistent with being populated by its own separate import process today.

**Practical consequence:** don't design Ops' "Jobs" object as a shared hub that Comms must integrate with now. Scope it to Ops' own electrical work. Keep `job_number` format/uniqueness clean so a future Comms-via-Ops integration (manual entry, or later a Workbench API) stays possible without a rework.

## 3. EQ Field's dependency is real, live — and now has a concrete mechanism

Royce, 2026-08-03: "Field uses job numbers from ops to help people know the latest list of jobs — it should all be canonical."

How it actually works (view definition read live 2026-09-04): Field reads **`app_data.field_job_numbers`**, a view over `app_data.field_job_numbers_src()` (SQL, `SECURITY DEFINER`, SKS tenant id hardcoded). It yields one row per Ops `job_number` taken from the freshest non-deleted, non-`invoiced` SKS quote carrying that number — project name, customer, site (name preferred over code since migration `0275`, 2026-08-24) and a three-state status (Active / On Hold / Complete; `invoiced` auto-retires a number from Field's pickers) — `union all` Field-local manual numbers from `public.job_numbers` that are not already an Ops number, with `public.field_job_number_overrides` as a hide-only "Retired" override (restore = delete the override; the quote is never touched). 56 rows today; `public.job_numbers` still holds 98 manual rows, most now shadowed by Ops numbers. `field_job_numbers_src` is registered in eq-shell's `SHARED_REGISTRY_FUNCTIONS` (#1701).

So what Field consumes is the **quote's `job_number`**, not `app_data.jobs`. Any gap in how reliably Ops stamps and keeps a `job_number` on the quote directly degrades what Field's users see as "the current list of jobs."

## 4. Current data model (verified live 2026-09-04, ehow / sks-canonical)

| Table | Rows | Role | Linkage |
|---|---|---|---|
| `app_data.quote` | 232 | Drives the Kanban board via a `status` text column with a 16-value CHECK (`draft`, `submitted`, `client-reviewing`, `verbal-win`, `won-awaiting-job-no`, `won-job-created`, `po-matched`, `active`, `complete`, `ready-to-invoice`, `invoiced`, `on-hold`, `lost`, `cancelled`, `expired`, `superseded`; 12 in use; the UI collapses them to 5 stages since PR #989). Carries its own `job_number`, `po_number`, and `deleted_at` (soft delete — `invoiced` quotes auto-archive after 7 days, PR #1319). | — |
| `app_data.jobs` | 96 | Canonical job record. | **`jobs_quote_id_fkey` → `app_data.quote(quote_id)` `ON DELETE RESTRICT`** (migration `0237`, PR #1230, 2026-08-04), plus FKs to `customers` and `sites`. 0 jobs without a quote. |
| `app_data.sks_comms_jobs` | 153 | NSW Comms' own operational table (separate trade, §2). | No FK to either of the above — `job_number` / `quote_ref` are plain text, matched by value only if at all. |

**The gap is closed for live quotes.** Every non-archived quote at a job-stage status has an `app_data.jobs` row: `won-job-created` 18/18, `po-matched` 2/2, `active` 28/28, `complete` 6/6, `invoiced` 5/5. The 49 job-stage quotes without a job row are all soft-deleted (`deleted_at` set — 35 of them archived `invoiced` quotes), which is the intended shape.

### What was wrong on 2026-08-03 and what fixed it (record)

- **Board drag-and-drop never wrote the canonical job.** `savePipelineStatus()` only called `syncJobToCanonical()` when the quote object carried a `customer_id`, and the board's own `Quote` type had none (only `customer_name`) — so the primary interaction silently skipped the sync; only the detail panel (full `QuoteDetail`) synced. **Fixed 2026-08-03:** migration `0236` makes `eq_list_quotes` return `customer_id`/`site_id` (needed a `DROP FUNCTION` first — PR #1221) and PR #1220 threads it onto the board row; `QuotesModule.tsx` now carries `customer_id` on `Quote` with a comment saying exactly why.
- **Second gap, unrelated:** saving a PO number advanced a quote to `po-matched` without any job sync at all. **Fixed** PR #1223.
- **Backfilled 30** SKS quotes that had reached a job-stage status with no job row (live count; the earlier "~25" was an estimate). zaap/EQ had zero Ops quotes, nothing to backfill there.
- **Orphan `7842b5ce…` deleted, then the FK added** (`0237`, PR #1230, 2026-08-04) — dispatched to both planes, live-verified via `pg_get_constraintdef`.
- **A second write path exists and is easy to forget:** `quote-job-consumer.ts` (scheduled every 15 min) upserts jobs from `quote.accepted` canonical events with a 7-day lookback. It reacts to events; it never sweeps a backlog — which is why the 30 stuck quotes needed an explicit backfill.

Full record: `eq/changelog/eq-shell.md` (2026-08-03 and 2026-08-04 entries), `sessions/2026-08-03.md`, `sessions/2026-08-04.md`.

## 5. Ultimate intention (Royce, 2026-08-03)

> "Ultimate intention is for EQ ops to carry the quoting load of users — then ultimately either via workbench API or continued manual use the job numbers will sit between field, ops and comms to ensure a seamless pass of current jobs is used throughout."

Reading: Ops becomes the primary quoting engine (potentially for more than just electrical, over time). `job_number` is the durable join key across Field, Ops, and Comms — either through a future Workbench API integration or continued manual entry — so "what jobs exist right now" never has to be manually reconciled between systems.

## 6. Open work (not yet built, not yet decided)

- **Quotes/Jobs Kanban split — decided "not now"** (`/decide`, 2026-08-04). Both problems that motivated it — Open-column density and `job_number` reliability — were solved by cheaper live changes (collapsed customer groups, PR #1224, and the sync fixes above). Revisit only if the Open column crowds again with groups collapsed, or if job-specific features (costing, PO dashboards) need a shape a single quote-lifecycle board can't express. Tracked in `eq/pending/eq-shell.md`.
- **Tenant hardcoding:** `field_job_numbers_src()` is pinned to the SKS tenant id. A second Ops tenant would need it generalised; today that is a known limit, not a bug (zaap/EQ has zero Ops quotes).
- **NSW Comms adopting EQ Ops for quoting** — still optional/future, no decision.

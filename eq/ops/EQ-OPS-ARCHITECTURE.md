---
title: EQ Ops — Quotes, Jobs, and the Canonical Job Number
owner: Royce Milmlow
last_updated: 2026-08-03
scope: Authoritative reference for EQ Ops' scope, its relationship to NSW Comms and EQ Field, and the current state of the quote-to-job data model. Read before any work that touches app_data.quote, app_data.jobs, job_number, or the Kanban board's stage taxonomy.
read_priority: critical
status: live
---

# EQ Ops — Quotes, Jobs, and the Canonical Job Number

## 1. The principle in one sentence

EQ Ops is meant to become the canonical quoting/job engine for SKS's **electrical** trade, with `job_number` as the shared key that lets Field, Ops, and (eventually) NSW Comms all agree on "what jobs currently exist" without hand-reconciling separate lists.

## 2. Scope boundary — Ops is not Comms (Royce, 2026-08-03)

**EQ Ops = electrical.** NSW Comms is a deliberately separate, larger, structurally different trade (cabling/telco — `app_data.sks_comms_jobs` has telco-specific columns like `mop_received`, `pre_cable_done`, `post_dock_done`) with roughly 10x the job volume of Ops today (153 vs ~38 real electrical jobs). Royce: "having it mixed in with Ops... wouldn't work" given that magnitude gap.

**`job_number`/`quote_ref` on `sks_comms_jobs` are forward-compatibility wiring, not a live dependency.** They exist so that *if* the Comms team ever starts quoting through EQ Ops, the numbering already ties together — not because Comms currently reads from or writes to Ops' tables. `sks_comms_jobs` has its own `source`/`source_ref`/`imported_at` columns, consistent with being populated by its own separate import process today.

**Practical consequence:** don't design Ops' "Jobs" object as a shared hub that Comms must integrate with now. Scope it to Ops' own electrical work. Keep `job_number` format/uniqueness clean so a future Comms-via-Ops integration (manual entry, or later a Workbench API) stays possible without a rework.

## 3. EQ Field's dependency is real and live (Royce, 2026-08-03)

Unlike Comms, **Field actively consumes `job_number` today** — Royce: "Field uses job numbers from ops to help people know the latest list of jobs — it should all be canonical." This is a live, present-day integration point, not future-proofing. Any gap in how reliably Ops produces a canonical job record directly degrades what Field's users see as "the current list of jobs."

## 4. Current data model (verified live, 2026-08-03, ehow/sks-canonical)

Three places currently hold job-shaped data, with no enforced relational integrity tying them together:

| Table | Rows | Role | Linkage |
|---|---|---|---|
| `app_data.quote` | 74 | Drives the whole Kanban board via one 12-value `status` enum (draft → ... → invoiced/lost/etc). Carries its own `job_number` text field. | — |
| `app_data.jobs` | 13 | Intended canonical job record. Has its own `quote_id` column. | **No FK constraint** — `quote_id` is a bare uuid, unenforced. One existing row (`7842b5ce…`) already points at a `quote_id` that no longer exists in `app_data.quote` — a real, live orphan, not hypothetical. |
| `app_data.sks_comms_jobs` | 153 | NSW Comms' own operational table (separate trade, see §2). | No FK to either of the above — `job_number`/`quote_ref` are plain text, matched by value only if at all. |

**The real gap: `app_data.jobs` covers only 13 of the ~38 live quotes that have actually reached a job-stage status** (`won-job-created`/`po-matched`/`active`/`complete`/`invoiced`). 25 real, active, job-numbered quotes have no canonical job record at all.

### Root cause, found live 2026-08-03

`QuotesModule.tsx`'s `savePipelineStatus()` calls `syncJobToCanonical()` only when the quote object passed in carries a `customer_id`:
```ts
const maybeDetail = q as unknown as Partial<QuoteDetail>;
if (maybeDetail.customer_id && canonicalStatus) { await syncJobToCanonical(...); }
```
But the board's own `Quote` TypeScript interface (`QuotesModule.tsx:37-61`) — the shape every card in the Kanban board actually uses — **has no `customer_id` field at all**, only `customer_name`. So `maybeDetail.customer_id` is always `undefined` when a status change comes from **dragging a card on the board** (the primary, most-used interaction). The sync only ever fires when a status change is made through the **detail panel**, which loads a full `QuoteDetail` that does carry `customer_id`.

Checked directly against live data to confirm: queried all live job-stage quotes missing a canonical job record — every single one has `customer_id` set at the database level, ruling out "the quote genuinely has no customer" as the explanation. The gap is the board's own type shape, not the data.

**Net effect:** the board's drag-and-drop — the way most quotes actually move through the pipeline — silently never creates or updates the canonical job record. This has likely been true since `syncJobToCanonical` was introduced, not a recent regression.

## 5. Ultimate intention (Royce, 2026-08-03)

> "Ultimate intention is for EQ ops to carry the quoting load of users — then ultimately either via workbench API or continued manual use the job numbers will sit between field, ops and comms to ensure a seamless pass of current jobs is used throughout."

Reading: Ops becomes the primary quoting engine (potentially for more than just electrical, over time). `job_number` is the durable join key across Field, Ops, and Comms — either through a future Workbench API integration or continued manual entry — so "what jobs exist right now" never has to be manually reconciled between systems.

## 6. Open work (not yet built, not yet decided)

- **The `savePipelineStatus`/`syncJobToCanonical` gap (§4) needs fixing** — board-driven status changes need the same canonical-job-sync behavior the detail panel already gets. Real production impact: Field's "canonical" job list is missing the majority of real jobs today.
- **Backfill decision needed** for the 25 already-missing canonical job rows (same shape as the `draft`/`sent_at` backfill done earlier this session — likely needs the real sync logic re-run per row, not a raw insert, to get status history/audit right).
- **`app_data.jobs.quote_id` FK constraint** — add it, but only after the known orphan (`7842b5ce…`) is resolved; a naive `ADD CONSTRAINT` will fail against current data.
- **Quotes/Jobs Kanban split** — Royce's proposed taxonomy (Quotes: Draft/Open, Sent, Archived/saved-for-future · Jobs: Won, Job Created, In Progress, Completed, Invoiced) is the target shape, scoped to Ops' own electrical work only (§2). Not yet built — sequence behind the sync-gap fix so "Jobs" means something real when it ships.
- No decision yet on whether NSW Comms ever actually adopts EQ Ops for quoting — treat as optional/future, not a current requirement.

---
title: Canonical Wiring — Deploy Runbook
date: 2026-06-07
status: ready — nothing applied or deployed yet
covers: the 6-step canonical wiring program built 2026-06-07 (see sessions/2026-06-07.md)
rule: SKS-tier infra (ehow / nspb / sks tenant plane) is touched in several steps → Royce-gated.
  Tenant-plane DDL goes through the eq-shell One Pipe (tenant-migrate.yml), never hand-applied.
---

# Canonical Wiring — Deploy Runbook

Activates the program that turned the reference layer from a write-only mirror into a durably-fed, operational,
self-healing system of record. **All code is built + type-verified; nothing is applied or deployed.** Follow the order
below — it's sequenced so there is no broken intermediate state (schema exists before the code that uses it ships;
the hub accepts `jobs` before the consumer tries to write them).

## What's being activated
| # | Fix | Repos |
|---|---|---|
| 1 | Service durable outbox | eq-solves-service |
| 2 | Hub accepts `PUT jobs` | eq-shell (canonical-api + tenant migration 0040) |
| 3 | `quote.accepted` → job consumer | eq-shell |
| 4 | Quotes durable outbox | eq-quotes-port + eq-shell scheduler |
| 5 | Field `shift.started` emit retry | eq-solves-field (edge fn) |
| 6 | Reconciliation backstop | eq-quotes-port + eq-solves-service (+ eq-shell schedulers) |

---

## Activation order

### Step 0 — pre-flight env audit (no changes)
Confirm these already exist (set in prior work); only **`QUOTES_CRON_SECRET`** on eq-shell is likely new.
- **eq-shell (Netlify):** `CANONICAL_API_KEY_SHELL` (consumer auth), `TENANT_ROUTING_MASTER_KEY`, `QUOTES_APP_URL`,
  **`QUOTES_CRON_SECRET`** ← add this; must equal the Quotes app's `CRON_SECRET`. (Drives the 2 new Quotes schedulers.)
- **eq-solves-service (Netlify):** `CRON_SECRET`, `CANONICAL_API_URL`, `CANONICAL_API_KEY_SERVICE`, `CANONICAL_TENANT_SLUG`, `SUPABASE_SERVICE_ROLE_KEY`.
- **eq-quotes-port (Fly):** `CRON_SECRET`, `CANONICAL_API_URL`, `CANONICAL_API_KEY_QUOTES` (and/or `CANONICAL_API_KEY`), `CANONICAL_TENANT_SLUG`, `SUPABASE_*`.
- **eq-solves-field (Supabase fn secrets):** `CANONICAL_API_URL`, `CANONICAL_API_KEY_FIELD`, `CANONICAL_TENANT_SLUG` (unchanged — #5 is code-only).

### Step 1 — eq-shell tenant migration 0040 (jobs upsert index)  ·  **One Pipe · Royce-gated (prod gate)**
Apply `eq-shell/supabase/tenant-migrations/0040_jobs_canonical_upsert_index.sql` to **every** tenant plane via
`tenant-migrate.yml` (the same flow used for 0039). This must land **before** the consumer runs (race-safety of the
jobs upsert depends on the partial unique index).
- Verify: `app_data.jobs` has `jobs_tenant_external_id_uidx` on core + sks; drift gate green.

### Step 2 — deploy eq-shell  ·  Netlify (explicit)
Ships: `canonical-api.ts` (jobs writable), `quote-job-consumer.ts` (15-min), `canonical-outbox-quotes-scheduler.ts`
(5-min), `canonical-reconcile-quotes-scheduler.ts` (daily). Do **after** Step 1.
- Smoke: `PUT canonical-api {resource:'jobs', external_id:'eq-quotes:job:<test-uuid>', quote_id:'<test-uuid>', title:'smoke'}` with the SHELL key + `X-Tenant: sks` → `201 created`. Then GET `?resource=jobs&ids=` → the row. Delete the smoke row after.
- The consumer will, on its next tick, create jobs from any recent real `quote.accepted` events — expected.

### Step 3 — Service outbox + reconcile  ·  Supabase DDL + Netlify (explicit)
1. Apply `eq-solves-service/supabase/migrations/0099_canonical_outbox.sql` to the Service DB (`urjhmkhbgaxrofurpbgc`).
2. `supabase gen types` → refresh `lib/supabase/database.types.ts` (the outbox + reconcile code uses structural casts
   until types regenerate; optional but recommended).
3. Deploy Service (Netlify). Ships: `canonical-sync.ts` (enqueue-on-failure), `canonical-outbox.ts`, the drain route +
   `canonical-outbox-scheduler` (5-min), the reconcile route + `canonical-reconcile-scheduler` (daily).
- Smoke: `POST /api/cron/canonical-outbox-drain` (Bearer CRON_SECRET) → `{ok:true, processed:0,...}` on an empty outbox.
  `POST /api/cron/reconcile-canonical?limit=5` → `{ok:true, customers:{...}, sites:{...}}`.

### Step 4 — Quotes outbox + reconcile  ·  Supabase DDL (ehow) + Fly (explicit) · **SKS-tier**
1. Apply `eq-quotes-port/migrations/035_canonical_outbox.sql` to the Quotes DB (`ehowgjardagevnrluult`, public schema).
2. Deploy Quotes (Fly). Ships: `canonical_outbox.py`, `canonical_client.py` + `canonical.py` (enqueue-on-failure),
   the drain + reconcile routes.
- The eq-shell schedulers from Step 2 now drive `POST /api/cron/drain-canonical-outbox` (5-min) and
  `/api/cron/reconcile-canonical` (daily) — they 401 harmlessly until `QUOTES_CRON_SECRET` (Step 0) is set on both sides.
- Smoke: `POST /api/cron/drain-canonical-outbox` (Bearer CRON_SECRET) → `{ok:true,...}`.

### Step 5 — Field edge function  ·  Supabase functions deploy · **SKS-live (nspb) — "SKS live" gate**
`supabase functions deploy shift-events` (the retry is internal; no migration). Touches the SKS-live Field plane → only
with an explicit "SKS live" go. Independent of Steps 1–4; can be done any time.
- Smoke: invoke with `{ "dryRun": true }` → returns the computed payload, `emitted:false, dry:true`. (Retry only
  engages on a real emit against a flaky canonical-api.)

---

## End-to-end verification (after all steps)
Win a test quote in Quotes → within ≤15 min the consumer creates `app_data.jobs` row
`external_id='eq-quotes:job:<quote_id>'` with `quote_id` set. Confirm:
`select count(*) from app_data.jobs where quote_id is not null;` > 0 on the sks tenant plane. Quote → job is now real.

## Rollback (per step, all reversible)
- **0040 / 0099 / 035 migrations:** additive (a unique index / a new table) — drop if needed; no data loss.
- **eq-shell / Service / Quotes deploys:** redeploy the prior build. The schedulers stop with the rollback.
- **Field:** redeploy the prior `shift-events`.
- The outbox/consumer are idempotent and self-limiting (backoff, `dead` cap) — a bad deploy can't storm canonical.

## File manifest (uncommitted working-tree changes — land each on its own branch)
- **eq-solves-service:** `supabase/migrations/0099_canonical_outbox.sql`, `lib/canonical-outbox.ts`,
  `lib/canonical-reconcile.ts`, `lib/canonical-sync.ts`, `app/api/cron/canonical-outbox-drain/route.ts`,
  `app/api/cron/reconcile-canonical/route.ts`, `netlify/functions/canonical-outbox-scheduler.ts`,
  `netlify/functions/canonical-reconcile-scheduler.ts`, `netlify.toml`.
- **eq-shell:** `supabase/tenant-migrations/0040_jobs_canonical_upsert_index.sql`,
  `netlify/functions/canonical-api.ts`, `netlify/functions/quote-job-consumer.ts`,
  `netlify/functions/canonical-outbox-quotes-scheduler.ts`, `netlify/functions/canonical-reconcile-quotes-scheduler.ts`.
- **eq-quotes-port:** `migrations/035_canonical_outbox.sql`, `app/canonical_outbox.py`, `app/canonical_client.py`,
  `app/canonical.py`, `app/cron/routes.py`.
- **eq-solves-field:** `supabase/functions/shift-events/index.ts`.

**Suggested branches:** `claude/canonical-outbox` (service), `claude/canonical-jobs-consumer` (shell),
`claude/canonical-outbox` (quotes), `claude/shift-emit-retry` (field).

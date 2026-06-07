---
title: WS2 site→customer backfill — APPLIED
date: 2026-06-07
project: ehowgjardagevnrluult (sks-canonical) · schema app_data
status: applied, verified, reversible
scope: EQ-managed canonical plane (NOT nspb/SKS-live). No schema change, no deploy, no app code.
---

# WS2 — site→customer backfill (APPLIED 2026-06-07)

Part of the cross-app linkage sprint. Links orphaned canonical sites to their customers so the asset register rolls
up to a customer. Deterministic, FK-validated, reversible.

## Pre-flight safety (read-only, verified before running)
- `app_data.customers.external_id` is **unique** (0 non-unique groups) → every site→customer match is **1:1**.
- **440** sites resolved to exactly one customer; **0 ambiguous**.
- FK `app_data.sites.customer_id → app_data.customers.customer_id` validates every assigned link.

## What ran (live, Supabase MCP on `ehowgjardagevnrluult`)
```sql
update app_data.sites s
set customer_id = c.customer_id
from app_data.customers c
where s.customer_id is null
  and s.external_customer_id is not null
  and c.external_id = s.external_customer_id;
-- 440 rows updated (RETURNING captured the 440 site_ids in the session transcript)
```

## Result (verified)
| Metric | Before | After |
|---|---|---|
| `app_data.sites` with `customer_id` | 28 | **468** (+440) |
| `app_data.sites` unlinked | 563 | 123 (101 reference quotes-side customers → WS1; 22 keyless) |
| Assets traceable to a customer (asset→site→customer) | ~ (28 sites' worth) | **4769 / 4808 (99.2%)** |
| Assets still orphaned (on unlinked sites) | — | 39 |

## Exact rollback (re-derivable — the 440 are cleanly separable)
Verified: external-derivable links = 440 (this backfill); pre-existing manual links = 28. So this nulls **exactly**
the 440 and leaves the original 28 intact:
```sql
update app_data.sites s
set customer_id = null
where s.customer_id is not null
  and exists (select 1 from app_data.customers c
              where c.external_id = s.external_customer_id and c.customer_id = s.customer_id);
```

## Not done (still gated)
The remaining 123 sites wait on WS1 (canonical customer dedup) — they point at quotes-side customers not yet in
`app_data.customers`. The same backfill on the EQ tenant (`zaap`, 30 sites) was **not** run here — small, do on request.

---
title: EQ Field — Active State (Rolling)
owner: Royce Milmlow
last_updated: 2026-06-15
scope: Current live state of EQ Field product
read_priority: critical
status: live
---

# EQ Field — Active State

**Current version:** v3.5.147 · **Deployed:** `field.eq.solutions` + `field.sks.eq.solutions`
**Repo:** `eq-solutions/eq-field` (main branch, auto-deploy via Netlify)

---

## Live tenants

| Tenant | URL | Data plane | State |
|---|---|---|---|
| `eq` | `field.eq.solutions` | `ktmjmdzqrogauaevbktn` (ktmj) — demo/disposable | Live (demo data) |
| `demo-trades` | `field.eq.solutions?tenant=demo-trades` | ktmj | Advanced demo |
| `melbourne` | `field.eq.solutions?tenant=melbourne` | ktmj | Enterprise demo (577 ppl) |
| `sks` | `field.sks.eq.solutions` | `ehowgjardagevnrluult` (ehow) — SKS LIVE | Live (SKS canonical) |

**Shell embed:** `core.eq.solutions/sks/field` → iframes `field.sks.eq.solutions`

---

## SKS canonical state (ehow — as of 2026-06-13)

**JWT data path active** (`DATA_JWT_ENABLED=on`). All 11 `app_data.field_*` views present.
RLS WITH CHECK hardened on all 14 write policies. Adapter view architecture:
- `field_people` / `field_managers` → `app_data.staff` (read-only, Service owns)
- `field_sites` → `app_data.sites` (read-only, Service owns)
- `field_schedule` / `field_timesheets` / etc. → `public.*` (writable pass-throughs)

**Canonical sync LIVE (2026-06-13):** jvkn→ehow forward path active via `workers-canonical-sync` (v3) + `credentials-canonical-sync` (v1). 39 staff + 171 licences synced. Triggers on jvkn fire on INSERT/UPDATE/DELETE → ehow upserts.

**v3.5.147 identity stub (2026-06-15):** `_tryLinkPersonToWorker()` in `people.js` — on person save with email, looks up jvkn.workers by email; if found, patches `people.worker_id`; if not found, creates a minimal stub (name, email, phone, role). Transition scaffolding — removes when Cards onboarding is the sole creator of jvkn.workers rows. `syncAllToCanonical()` bulk action available to supervisor role.

**Data counts:** 39 staff · 591 sites · 171 licences · 0 roster rows (data entry needed)

---

## Modules live

| Module | Tenants | Notes |
|---|---|---|
| Dashboard | All | |
| Roster / Schedule | All | |
| People | All | |
| Sites | All | |
| Leave | All | |
| Timesheets | All | |
| Managers | All | |
| Safety (prestarts / toolbox) | sks | Tenant-gated |
| Teams | sks | Tenant-gated |
| Pipeline (Tender Pipeline) | sks | Tenant-gated |
| Resources (Resource Allocation) | sks | Tenant-gated |
| Site Reports / Diary | All | |
| Projects / Forecast | Enterprise | Melbourne demo |
| Apprentices | EQ only | SKS nav hidden |
| Site Audits | All | v3.5.112 |

---

## Auth model

PIN gate → `verify-pin.js` (Netlify Function) → HMAC session token (7-day).
`DATA_JWT_ENABLED=on` → per-tenant Supabase JWT minted on sign-in, used for all data queries.
Shell embed uses cookie SSO (`verify-shell-cookie`).

---

## Gated (Royce-gated, not yet active)

1. **Roster data entry on ehow** — schedule/timesheets/leave are empty; start fresh or migrate from nspb standalone
2. **Standalone `sks-nsw-labour` retirement** — after soak confirmation
3. **Track 2 RLS STEP 2** — anon SELECT lockdown; after standalone retired
4. **Collin Toohey fresh invite** — jvkn duplicate `3d18422d` deleted (2026-06-13); original `7514e57d` retained; needs a new Cards/Shell invite sent

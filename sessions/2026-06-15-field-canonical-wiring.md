---
date: 2026-06-15
topic: EQ Field — canonical wiring audit + v3.5.146 + v3.5.147
status: complete
---

# Session — EQ Field canonical wiring audit

## What was built

### v3.5.146 — canonical worker-link bridge (PR #287, merged)
Adds `people.worker_id` column link. On person save, `_tryLinkPersonToWorker()` looks up jvkn.workers by email and patches `people.worker_id` if found. Fire-and-forget — never blocks UI.

### v3.5.147 — canonical worker write (PR #288, merged, deployed 2026-06-15T02:38Z)
Extends v3.5.146: if no jvkn.workers row found for the email, creates a minimal stub (first_name, last_name, email, phone, role). `syncAllToCanonical()` bulk supervisor action seeds all unlinked people at once.

**Caveat:** Creating stubs in jvkn.workers from Field is transition scaffolding — Cards/Shell owns that layer in the target architecture. The create-path should be removed when Cards onboarding is live.

## Architecture clarified

Verified 4-layer model via Supabase MCP:

| Layer | Supabase | Role |
|---|---|---|
| Control plane | jvkn (`jvknxcmbtrfnxfrwfimn`) | Boot config (org, module entitlements), identity stubs |
| Shell | — | Auth + session + navigation |
| Apps | — | Field, Service, Quotes, etc. |
| SKS canonical | ehow (`ehowgjardagevnrluult`) | Source of truth: app_data.staff (40 rows), licences, schedule, timesheets |
| EQ canonical (future) | zaap (`zaapmfdkgedqupfjtchl`) | Same shape as ehow, not yet populated |

**ktmj** = EQ demo/operational DB only. Not part of the canonical architecture. "ktmj is completely irrelevant and incorrect" — Royce, 2026-06-15.

## How Field talks to tenants (confirmed)

1. **Boot** → `_loadCanonicalConfig()` fetches jvkn.organisations + module_entitlements → resolves SB_URL (= ehow for SKS), tier, branding, disabled modules.
2. **Anon path** → `sbFetch()` → SB_URL with anon key → public.* tables (people, sites, managers, schedule, etc.)
3. **JWT path (SKS, LIVE)** → `_getDataJwt()` → verify-pin `mint-data-jwt` → short-lived Supabase JWT signed with SKS_JWT_SECRET → adapters write to ehow `app_data.*`:
   - `leave-adapter.js` → `app_data.leave_requests`
   - `roster-adapter.js` → `app_data.schedule_entries`
   - `timesheets-adapter.js` → `app_data.timesheets`
4. **Staff map** → `loadCanonicalStaffMap()` fetches ehow `app_data.staff` → name↔staff_id for all adapters
5. **Identity stub** → v3.5.147 → jvkn.workers (cross-app correlation only)

## Env vars verified (eq-field Netlify, 2026-06-15)

| Var | Status |
|---|---|
| `DATA_JWT_ENABLED` | `on` ✓ |
| `SKS_JWT_SECRET` | set ✓ |
| `ZAAP_JWT_SECRET` | `""` ⚠ (EQ JWT broken — ok while zaap empty) |
| `APP_ORIGIN` | stale (`eq-solves-field.netlify.app`) |
| `EQ_SECRET_SALT` | demo value — not rotated |
| `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` | ehow creds, `VITE_` prefix = likely zombies |

Live URL is `https://field.eq.solutions`. CLAUDE.md updated.

## Deferred

- People profile enrichment from ehow (pre-fill from app_data.staff on person load)
- Remove v3.5.147 create-stub path when Cards goes live
- Fix `APP_ORIGIN` env var
- Investigate `approve-leave` Netlify function (not in CLAUDE.md)

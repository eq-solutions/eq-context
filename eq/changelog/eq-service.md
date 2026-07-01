# EQ Service — Changelog

## 2026-07-01
- **Migration 0164** — dropped `canonical_id`/`canonical_synced_at` from `app_data.instruments` (incorrect 0158 link to `app_data.assets` plant_equipment). Rebuilt `service.instruments` view + INSTEAD OF trigger. `pullCanonicalInstrumentsAction` and "Sync from Shell" button removed. Instruments register is now self-contained.

## 2026-06-30
- **Migration 0163** — `service.sites` view now filters `active = true` (was `service_enabled` only). Archived sites retire from Service at the view layer. PR #381 merged to main.

# EQ Service — Changelog

## 2026-07-01
- **Migration 0164** — dropped `canonical_id`/`canonical_synced_at` from `app_data.instruments` (incorrect 0158 link to `app_data.assets` plant_equipment). Rebuilt `service.instruments` view + INSTEAD OF trigger. `pullCanonicalInstrumentsAction` and "Sync from Shell" button removed. Instruments register is now self-contained.
- **Migration 0165** — `instrument_id uuid FK` added to `app_data.acb_tests` + `app_data.nsx_tests` (ON DELETE SET NULL). Rebuilt both service views and INSTEAD OF triggers.
- **ACB/NSX instrument picker** — Step 1 of both workflows now shows a calibrated instrument dropdown from the instruments register. `instrument_id` persisted on save.

## 2026-06-30
- **Migration 0163** — `service.sites` view now filters `active = true` (was `service_enabled` only). Archived sites retire from Service at the view layer. PR #381 merged to main.

# EQ Service — Changelog

## 2026-07-02
- **ARMADA lighthouse — 2 recon passes, 9 issues shipped.** Budget bumped to 6 issues/600s runtime (PR #397). PRs #394–396 (dead shell-sso path, Zod validation on report settings, idempotency tests) + #404–409 (Sentry captureException wired across report-generation routes, canonical outbox/sync/members, generate-and-store PDF pipeline, cron dispatch-notifications, and server action helpers; unit tests for `lib/actions/audit.ts`) all merged.
- **3 dependency/docs PRs merged** — #363 (LOCAL_DEV.md `urjh`→`ehow`), #368 (`@netlify/functions` 5.2.0→5.3.0), #370 (React 19.2.4→19.2.7 — fixes a `FormData` regression in Server Actions from 19.2.6).

## 2026-07-01
- **Migration 0164** — dropped `canonical_id`/`canonical_synced_at` from `app_data.instruments` (incorrect 0158 link to `app_data.assets` plant_equipment). Rebuilt `service.instruments` view + INSTEAD OF trigger. `pullCanonicalInstrumentsAction` and "Sync from Shell" button removed. Instruments register is now self-contained.
- **Migration 0165** — `instrument_id uuid FK` added to `app_data.acb_tests` + `app_data.nsx_tests` (ON DELETE SET NULL). Rebuilt both service views and INSTEAD OF triggers.
- **ACB/NSX instrument picker** — Step 1 of both workflows now shows a calibrated instrument dropdown from the instruments register. `instrument_id` persisted on save.

## 2026-06-30
- **Migration 0163** — `service.sites` view now filters `active = true` (was `service_enabled` only). Archived sites retire from Service at the view layer. PR #381 merged to main.

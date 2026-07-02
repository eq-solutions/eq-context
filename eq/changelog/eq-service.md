# EQ Service — Changelog

## 2026-07-02
- **Contacts canonical cutover LIVE (migration 0167, PR #410).** service.customer_contacts/site_contacts became per-link security_invoker views over app_data.contacts + link tables with INSTEAD OF triggers — one source of truth with Shell/Quotes. Same names/shapes = zero app-page changes; 3 FK-hint embeds rewritten. Legacy tables renamed *_legacy_20260702 for the soak; drop + drift-guard ERROR flip = Steps 4-5. RLS read now 224/23 rows (was 109/0 on the fork). PR #411 = the day's canonical-audit branch.
- **Contacts Step 1 → canonical.** 22 real Service-local contacts (+links) merged into canonical `app_data.contacts` (208→230); 4 links added for already-canonical people; junk/dups/typo excluded; all tagged for rollback. `/contacts` still reads local tables until Step 3 (repoint). The 2026-06-25 roadmap's "contacts Service done" was false — local `customer_contacts` (base table, 109) was shadowing canonical.
- **Source-of-truth drift guard** (`audits/run.sql` + `CHECKS.md`) — flags any service base table shadowing a canonical entity; fires 2 (contact forks), WARN→ERROR once consolidated. The guard the roadmap asked for but never built.
- **Migration 0166** — `service.assets` view excludes `asset_type='plant_equipment'` (13 test instruments were surfacing as maintainable assets). app_data untouched.
- **Shell nav fix** — Calendar + Defects added to the Shell-embedded nav bar (`app/(app)/layout.tsx`); both were built + enabled but unreachable from Shell.
- **Spinner** "EQ Solves Service"→"EQ Service"; root `<html>` `suppressHydrationWarning` (React #418 forced full client re-render on Shell-embedded dashboard).
- **Debris dropped** — `app_data.pm_calendar`/`contract_variations`/`contract_scopes_history` (force-push orphans); 154 history rows backed up first.
- **Docs** — CLAUDE.md canonical scope corrected 3→~20 entities; D2 resolved (job_plans canonical).
- **ARMADA lighthouse — 2 recon passes, 9 issues shipped.** Budget bumped to 6 issues/600s runtime (PR #397). PRs #394–396 (dead shell-sso path, Zod validation on report settings, idempotency tests) + #404–409 (Sentry captureException wired across report-generation routes, canonical outbox/sync/members, generate-and-store PDF pipeline, cron dispatch-notifications, and server action helpers; unit tests for `lib/actions/audit.ts`) all merged.
- **3 dependency/docs PRs merged** — #363 (LOCAL_DEV.md `urjh`→`ehow`), #368 (`@netlify/functions` 5.2.0→5.3.0), #370 (React 19.2.4→19.2.7 — fixes a `FormData` regression in Server Actions from 19.2.6).

## 2026-07-01
- **Migration 0164** — dropped `canonical_id`/`canonical_synced_at` from `app_data.instruments` (incorrect 0158 link to `app_data.assets` plant_equipment). Rebuilt `service.instruments` view + INSTEAD OF trigger. `pullCanonicalInstrumentsAction` and "Sync from Shell" button removed. Instruments register is now self-contained.
- **Migration 0165** — `instrument_id uuid FK` added to `app_data.acb_tests` + `app_data.nsx_tests` (ON DELETE SET NULL). Rebuilt both service views and INSTEAD OF triggers.
- **ACB/NSX instrument picker** — Step 1 of both workflows now shows a calibrated instrument dropdown from the instruments register. `instrument_id` persisted on save.

## 2026-06-30
- **Migration 0163** — `service.sites` view now filters `active = true` (was `service_enabled` only). Archived sites retire from Service at the view layer. PR #381 merged to main.

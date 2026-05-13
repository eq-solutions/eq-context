---
title: EQ Tier — Products
owner: Royce Milmlow
last_updated: 2026-05-14
scope: Live EQ products. Killed/deferred entries removed in 2026-05-04 refactor.
read_priority: standard
status: live
---

# EQ Tier — Products

Only live or actively-built products. Killed/deferred products are not
listed here — see `CLAUDE.md` "Killed / deferred" section, or
`/archive/` for historical changelogs.

---

## EQ Solves — Field (LEAD MODULE)

**Status:** Live. Current version **v3.4.75** (demo on 2026-05-14; main on 2026-05-13 at v3.4.74). Phase 1 multi-tenancy foundation in place; Phase B+C role system in 5-7 day demo soak; Site Reports sub-module shipping workflows (Prestart + Toolbox live on demo, Diary + Weekly to follow).
**URL:** eq-solves-field.netlify.app (demo) / sks-nsw-labour.netlify.app (main = SKS prod)
**Repo:** Milmlow/eq-field-app (private); `demo` → EQ Field demo, `main` → SKS prod
**Working file:** index.html
**Architecture:** PWA, URL-based tenant detection
**Supabase project:** ktmjmdzqrogauaevbktn (eq-solves-field) — bypassed in demo mode
**Deploy:** GitHub push → Netlify auto (per branch)

**Strategic priority:** Sole EQ build focus until 20 paying customers.
Validation gate = 5 outside-SKS trade subbies on Field demo first.

**Site Reports sub-module (v3.4.69+, demo only):**
- Two sidebar entries under "Testing (DO NOT USE)" with BETA chips: Prestart, Toolbox.
- **Prestart** (v3.4.69, shipped 2026-05-13) — form + 8 photos + signature pad + offline queue + mobile-responsive. Tables: `prestarts` + `prestarts.photos` on BOTH Supabases.
- **Toolbox Talk** (v3.4.75, shipped 2026-05-14) — same shape as Prestart with workflow-specific fields (`topic`, `safety_message`, `items_reviewed`, `open_actions`, `next_meeting`, `attendance` JSONB). Tenant-neutral column names (`facilitator` not `sks_rep` — the Prestart leak is not repeated). Table: `toolbox_talks` on BOTH Supabases. Code in `scripts/toolbox.js` (sibling to `site-reports.js`).
- **Ben's preview path:** `eq-solves-field.netlify.app/?tenant=sks` — loads SKS branding + SKS Supabase data on the demo build. Same URL works for both Prestart and Toolbox.
- Next workflows in order (per outstanding build brief): Daily Site Diary → Weekly Site Report.
- Hub/dashboard restructure: ≥2 workflows now exist (the original trigger condition) but kept deferred — each workflow soaks individually before the chooser ships.
- Absorbs workflows from Ben Ritchie's `sks-field-reports.netlify.app` v29 (see `ops/decisions.md` 2026-05-13 Path C entry).
- Compliance pack export (Hammertech / Aconex / Procore) gated on all 4 workflows shipping.
- Refactor target: once Diary lands, extract photo + signature + offline-queue helpers from `site-reports.js` and `toolbox.js` into shared `scripts/site-report-shared.js`.

**Phase 1 (live as of 2026-04-27, PR [#23](https://github.com/Milmlow/eq-field-app/pull/23) merged):**
- `window.EQ_FLAGS` — PostHog feature-flag wrapper (`scripts/flags.js`).
  Default `feat_project_hours_v1 = true` while PostHog is unconfigured.
- `window.EQ_PERMS` — 5-tier role permission helper
  (manager > supervisor > employee > apprentice > labour_hire).
  Reads `isManager` global as primary today-path role signal.
- Project Hours panel **removed in v3.4.71** (added no value with migration-not-applied warnings on SKS; `scripts/project-hours.js` parked for revival, `sites.track_hours` column retained).
- Living plan + permission matrix in `eq/field/multi-tenancy/` and `eq/field/permissions/`.

**Phase B+C role system (v3.4.68, demo only soak):**
- `resolveSessionRole()` wired into `initApp()` + supervisor PIN unlock.
- 5 handler gates migrated to `EQ_PERMS.can()` (leave.js + timesheets.js).
- PIN-unlock-wins rule preserves today's behaviour — supervisor PIN still grants full access regardless of DB role.
- Phase D (server-side tightening) planned early June.

**Demo:**
- Tenant slug: "eq" (bypasses Supabase)
- Staff PIN: "demo" / Supervisor PIN: "demo1234"
- Generic SEED data (staff, sites, schedule)
- Network error toasts suppressed in demo mode
- Demo tenant DOES send real emails (Royce uses CC to verify flow end-to-end)

**Local repo (Beelink):** `C:\Users\EQ\eq-field-app-demo`

**Pending:**
- Apply `migrations/2026-04-27_eq_role_enum_people_role.sql` to ktmjmdzqrogauaevbktn — does not block Phase 1, lays groundwork for Phase 2 verify-pin rewrite
- Site Reports next workflow: **Daily Site Diary (v3.4.76+)** — ~4-5 days, mirror Prestart/Toolbox scaffolding (weather JSONB, shift_type, delays array, incidents array, work_areas)
- Then **Weekly Site Report (v3.4.77+)** — ~6-8 days, HSEQ metrics, ITPs, hold points, RFIs; week-ending Friday default
- Hub/dashboard restructure — defer until Diary lands, then half-day to ship "Site Reports" collapsed entry + status cards
- Compliance pack export (DOCX/PDF, Hammertech / Aconex / Procore) — dedicated 1-2 week sprint after all 4 workflows exist
- PostHog flag `feat_project_hours_v1` not yet created — only matters when cohort rollouts become important
- Netlify env var cleanup (delete SECRET_SALT, STAFF_HASH, MANAGER_HASH) — folds into Phase 2 verify-pin rewrite
- Phase 2 (RLS hardening, Supabase-native JWT mint, edge function defence in depth, multi-tenancy proper) — gated on first self-serve trial signup OR ~3 customers manually provisioned
- Phase D (server-side role enforcement) — planned early June, ~2 weeks after Phase B+C demo soak passes
- Demo → main merge for Site Reports — gated on Ben Ritchie sign-off + Royce explicit go. Ben's preview path (`?tenant=sks` on the demo site) is the sign-off surface; SKS prod (`sks-nsw-labour.netlify.app`) still on `main` without Site Reports UI.
- Ben Ritchie credit / consulting engagement / formal role in EQ team — TBD with Webb Financial
- Stripe payments integration (Phase 3, not started)

---

## EQ Solves — Service

**Status:** Active development
**Architecture:** Next.js + Supabase + Netlify serverless functions
**Supabase project:** urjhmkhbgaxrofurpbgc (eq-solves-service-dev)
**Scale:** Production-level complexity, multi-tenant with Supabase RLS
**Test coverage:** 80 Vitest tests
**Sprint cadence:** 22 sprints to date
**Deploy:** GitHub → Netlify CD
**Blocker:** GitHub MCP write access (403) — fix at `github.com/settings/installations`

---

## (No other EQ products are live)

Removed from this file in 2026-05-04 refactor:
- EQ Solves Quotes (deferred 6mo, see `/archive/`)
- EQ Solves Compliance / EQ Ops (killed)
- EQ Variations (killed)
- EQ Expenses (now SKS internal tool — see `sks/products.md` if added)

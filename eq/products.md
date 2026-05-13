---
title: EQ Tier — Products
owner: Royce Milmlow
last_updated: 2026-05-13
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

**Status:** Live. Current version **v3.4.73** (demo + main both on 2026-05-13). Phase 1 multi-tenancy foundation in place; Phase B+C role system in 5-7 day demo soak; Site Reports sub-module shipping workflows (Prestart MVP live, Toolbox/Diary/Weekly to follow).
**URL:** eq-solves-field.netlify.app (demo) / sks-nsw-labour.netlify.app (main = SKS prod)
**Repo:** Milmlow/eq-field-app (private); `demo` → EQ Field demo, `main` → SKS prod
**Working file:** index.html
**Architecture:** PWA, URL-based tenant detection
**Supabase project:** ktmjmdzqrogauaevbktn (eq-solves-field) — bypassed in demo mode
**Deploy:** GitHub push → Netlify auto (per branch)

**Strategic priority:** Sole EQ build focus until 20 paying customers.
Validation gate = 5 outside-SKS trade subbies on Field demo first.

**Site Reports sub-module (v3.4.69+, demo only):**
- Sidebar entry under "Testing (DO NOT USE)" with BETA chip.
- v1 ships **Prestart** only (form + 8 photos + signature pad + offline queue + mobile-responsive).
- `prestarts` table + `photos` JSONB column live on BOTH Supabase projects as of 2026-05-13.
- Next workflows in order (per `eq-solves-field/AUDIT-REVIEW.md` and outstanding build brief): Toolbox Talk → Diary → Weekly Report.
- Hub/dashboard restructure deferred until ≥2 workflows ship.
- Absorbs workflows from Ben Ritchie's `sks-field-reports.netlify.app` v29 (see `ops/decisions.md` 2026-05-13 Path C entry).
- Compliance pack export (Hammertech / Aconex / Procore) gated on all 4 workflows shipping.

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
- Site Reports next workflow: **Toolbox Talk (v3.4.74)** — 3-4 days, mirror Prestart scaffolding
- PostHog flag `feat_project_hours_v1` not yet created — only matters when cohort rollouts become important
- Netlify env var cleanup (delete SECRET_SALT, STAFF_HASH, MANAGER_HASH) — folds into Phase 2 verify-pin rewrite
- Phase 2 (RLS hardening, Supabase-native JWT mint, edge function defence in depth, multi-tenancy proper) — gated on first self-serve trial signup OR ~3 customers manually provisioned
- Phase D (server-side role enforcement) — planned early June, ~2 weeks after Phase B+C demo soak passes
- Demo → main merge for Site Reports — gated on Ben Ritchie sign-off + Royce explicit go
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

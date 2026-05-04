---
title: EQ Tier — Products
owner: Royce Milmlow
last_updated: 2026-05-04
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

**Status:** Live (demo branch). Phase 1 multi-tenancy foundation in place.
**URL:** eq-solves-field.netlify.app
**Repo:** Milmlow/eq-field-app (private), demo branch
**Working file:** index.html
**Architecture:** PWA, URL-based tenant detection
**Supabase project:** ktmjmdzqrogauaevbktn (eq-solves-field) — bypassed in demo mode
**Deploy:** Netlify Drop (manual zip)

**Strategic priority:** Sole EQ build focus until 20 paying customers.
Validation gate = 5 outside-SKS trade subbies on Field demo first.

**Phase 1 (live as of 2026-04-27, PR [#23](https://github.com/Milmlow/eq-field-app/pull/23) merged):**
- `window.EQ_FLAGS` — PostHog feature-flag wrapper (`scripts/flags.js`).
  Default `feat_project_hours_v1 = true` while PostHog is unconfigured.
- `window.EQ_PERMS` — 5-tier role permission helper
  (manager > supervisor > employee > apprentice > labour_hire).
  Reads `isManager` global as primary today-path role signal.
- Project Hours self-mounting burn-down panel (`scripts/project-hours.js`)
  — visible at the bottom of the page for supervisors. Gated on
  `EQ_FLAGS.isEnabled('feat_project_hours_v1')` + `EQ_PERMS.can('ph.view_dashboard')`.
- `sites.track_hours` + `sites.budget_hours` columns added to
  ktmjmdzqrogauaevbktn (migration `2026-04-27_sites_track_hours.sql` applied).
- Living plan + permission matrix in `eq/field/multi-tenancy/` and `eq/field/permissions/`.

**Demo:**
- Tenant slug: "eq" (bypasses Supabase)
- Staff PIN: "demo" / Supervisor PIN: "demo1234"
- Generic SEED data (staff, sites, schedule)
- Network error toasts suppressed in demo mode

**Local repo (Beelink):** `C:\Users\EQ\eq-field-app-demo`

**Pending:**
- Apply `migrations/2026-04-27_eq_role_enum_people_role.sql` to
  ktmjmdzqrogauaevbktn (verification queries in header) — does not block
  Phase 1 functionality, lays groundwork for Phase 2 verify-pin rewrite
- PostHog flag `feat_project_hours_v1` not yet created — only matters
  when cohort rollouts become important (e.g. external customers)
- Netlify env var cleanup (delete SECRET_SALT, STAFF_HASH, MANAGER_HASH) —
  folds into Phase 2 verify-pin rewrite
- Phase 2 (RLS hardening, Supabase-native JWT mint, edge function
  defence in depth, multi-tenancy proper) — gated on first self-serve
  trial signup OR ~3 customers manually provisioned
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

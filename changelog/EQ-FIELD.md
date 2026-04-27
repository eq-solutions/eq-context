---
title: Changelog — EQ Solves Field
owner: Royce Milmlow
last_updated: 2026-04-27
scope: Append-only history of changes to the EQ Solves Field product
read_priority: reference
status: live
---

# Changelog — EQ Solves Field

## [2026-04-27] Phase 1 implementation kickoff — flags, perms helper, migrations
**Built by:** Royce Milmlow + Claude Code (Opus 4.7)
**Branch:** `claude/hopeful-wright-058c8b` (not merged to demo — awaiting review)
**Changes (5 commits past `0145c78`):**
- `e9b4706` — `scripts/flags.js` PostHog feature-flag wrapper exposing
  `window.EQ_FLAGS.isEnabled()` + `variant()`. Safe defaults, no-op until
  a flag is created in the EQ PostHog project (`phc_zXpRxm6Q…`).
- `f2d0e91` — `scripts/permission-matrix.js` + `scripts/permissions.js`.
  Matrix v1 embedded as static JS; `window.EQ_PERMS.can(permKey)` reads
  the current role.
- `8b6bdb1` — Two SQL migrations written (NOT applied):
  - `migrations/2026-04-27_sites_track_hours.sql` — `track_hours` boolean
    + `budget_hours numeric` on `public.sites`
  - `migrations/2026-04-27_eq_role_enum_people_role.sql` — `eq_role`
    Postgres enum + `people.role` column with manager-table backfill
    pattern. Header includes verification queries to run before applying.
- `b367eb1` — `EQ_PERMS.getRole()` reads `window.isManager` as primary
  today-path role signal (durable for page lifetime), falling back to
  sessionStorage flags. Plan revised: 97 `isManager` references across
  `scripts/`/`index.html` rules out a wholesale refactor — strangler
  pattern instead, migrate opportunistically when touching files.
- `89f96dc` — `scripts/project-hours.js` + placeholder div before
  `</body>`. Self-mounting "Project Hours" burn-down panel — activates
  only when `feat_project_hours_v1` flag is on AND `EQ_PERMS.can('ph.view_dashboard')`
  is true. Renders per-site Budget / Used / Remaining / % used with
  colour treatment (sky / amber / red). Graceful states for "migration
  not applied yet", "no tracked sites", and network errors. Client-side
  aggregation over timesheets for v1.

**Next manual steps required (Royce):**
- Create `feat_project_hours_v1` flag in EQ PostHog project (default off,
  cohort = your `distinct_id` only)
- Apply both migrations to `ktmjmdzqrogauaevbktn` via Supabase MCP /
  Studio after running the verification queries in the role-enum header.
  Do NOT apply to `nspbmirochztcjijmcrx` (SKS live).
- Open PR `claude/hopeful-wright-058c8b` → `demo` when ready to merge.

**Status:** Code shipped to feature branch only. No Netlify deploy. No
Supabase changes. SKS Labour untouched.

## [2026-04-27] Multi-tenancy + dev-workflow plan locked (planning only, no code shipped)
**Built by:** Royce Milmlow + Claude Code (Opus 4.7)
**Changes:**
- Living plan document captured at
  `eq-solves-field/.claude/worktrees/hopeful-wright-058c8b/MULTI-TENANCY-PLAN.md`.
- Three strategic decisions locked:
  - Sprint scope = Phase 1 only (PostHog flags + project-hours feature + 5-tier
    role system). Phase 2 deferred to first self-serve trial signup OR ~3
    customers manually provisioned.
  - Tenancy lives inside `ktmjmdzqrogauaevbktn` only; SKS Labour
    (`nspbmirochztcjijmcrx`) untouched.
  - Auth: Supabase-native JWT minted in `verify-pin.js` with
    `app_metadata.tenant_id` and `app_metadata.eq_role`; PIN UX preserved.
- Tenant URL convention locked: `eq.solutions/field/<slug>/`. Path-based slug
  resolution, single shared Netlify site, no subdomains.
- 5-tier role system designed (`manager > supervisor > employee > apprentice >
  labour_hire`) with `eq_role` Postgres enum and `people.role` column.
- Single PIN per tenant on `organisations.tenant_pin`; per-role PIN env var
  pattern dropped.
- Permission matrix HTML built at
  `eq-context/drafts/eq-field-roles-2026-04-27/permission-matrix.html` plus v1
  JSON snapshot at `permissions-by-role-v1.json` (manager 56 / supervisor 36 /
  employee 13 / apprentice 17 / labour_hire 5).
- First PostHog flag designed: `feat_project_hours_v1` gates new project-hours
  burn-down feature with `sites.track_hours` + `sites.budget_hours`.

**Status:** Plan complete. No code touched. Phase 1 implementation pending
explicit Royce go-ahead.

## [2026-04-05] Demo Mode, Seed Data and Network Error Suppression
**Built by:** Royce Milmlow + assistant
**Changes:**
- Demo mode implemented - bypasses Supabase auth when tenant slug is eq
- 18 generic staff, 7 generic sites, 5 weeks of schedule seeded
- Network error toasts suppressed in demo mode
- Cowork guardrail issue documented
**Status:** Live on eq-solves-field.netlify.app (demo branch)

## [2026-04-05] Cloudflare Pages Deployment Architecture Locked
**Built by:** Royce Milmlow + assistant
**Changes:**
- Deployment architecture confirmed and locked
- Rule: never cross-deploy between targets
**Status:** Architecture documented

## [2026-04-04] Redundancy and Failover Gap Assessment
**Built by:** Royce Milmlow + assistant
**Changes:**
- Full infrastructure assessment across Netlify, Supabase, Resend, GitHub
- Gaps identified: Supabase single point of failure, no backups, no tagged release
**Status:** Gaps identified - NOT yet resolved

## [2026-03-31] White-Label Commercialisation Review
**Built by:** Royce Milmlow + assistant
**Changes:**
- EQ Field Ops commercialisation roadmap built (85-item Excel workbook)
- White-label conversion estimated at 2-3 hours
**Status:** Planning complete - not yet executed

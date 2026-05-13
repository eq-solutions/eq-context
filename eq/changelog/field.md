---
title: Changelog — EQ Solves Field
owner: Royce Milmlow
last_updated: 2026-05-14
scope: Append-only history of changes to the EQ Solves Field product
read_priority: reference
status: live
---

# Changelog — EQ Solves Field

## [2026-05-14] v3.4.75 — Site Reports v2: Toolbox Talk MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.75-toolbox` → `demo` (PR #77, squash merge `66e03a9`)
**Changes:**
- New `scripts/toolbox.js` (~810 lines) — sibling to `scripts/site-reports.js`. Photo / signature pad / offline write queue copy-pasted with `toolbox` / `_tbx` prefixes. Refactor target: extract shared helpers to `site-report-shared.js` once Daily Diary (v3) lands.
- New migration `2026-05-14_toolbox_talks_v1.sql` — `toolbox_talks` table with same RLS + realtime pattern as `prestarts`. Photos JSONB included from day 1 (Prestart needed a follow-up — not repeating).
- `permission-matrix.js` v1.2 — `reports.toolbox.{view,create,submit,sign}` added. Manager + supervisor get all four; employee / apprentice / labour_hire get `.sign` only (mirrors prestart shape).
- New sidebar entry "Toolbox" under Testing (DO NOT USE), BETA chip, next to Prestart.
- Version bump tuple: `index.html` banner + `scripts/app-state.js` `APP_VERSION` + `sw.js` CACHE all → `v3.4.75`. `sw.js` PRECACHE list includes `/scripts/toolbox.js`.
- **Migrations applied 2026-05-14 to BOTH Supabase projects:**
  - `ktmjmdzqrogauaevbktn` (eq-solves-field) ✓
  - `nspbmirochztcjijmcrx` (sks-labour) ✓ — applied per Royce's explicit "SKS live" go so Ben Ritchie can preview via `eq-solves-field.netlify.app/?tenant=sks`

**Schema differences from `prestarts` (deliberate):**
- `facilitator` (not `sks_rep`) — toolbox column names must be tenant-neutral. Prestart's `sks_rep` is a legacy leak not repeated in new tables.
- `meeting_date` / `meeting_time` (not `briefing_date` / `briefing_time`) — toolbox = scheduled meeting, not pre-shift briefing.
- `attendance` (not `crew`) — toolbox audiences include subbies, clients, visitors. Same JSONB shape as `prestarts.crew` so signature pad code is reusable.
- Toolbox-specific fields: `topic`, `safety_message`, `items_reviewed`, `open_actions`, `next_meeting`.

**Why:** Path C absorption (see `ops/decisions.md` 2026-05-13) — second workflow folded in from Ben Ritchie's `sks-field-reports.netlify.app` v29. Prestart shipped as v3.4.69; Toolbox is the second of four (Diary + Weekly to follow). Lessons applied: v3.4.54 per-action inflight guards, v3.4.55 id-coercion via `String()` for tenant-portable PKs, v3.4.56 audit failures surfaced via `console.warn` (offline queue).

**Brief drift caught:** The outstanding-build brief claimed v3.4.69 was demo's tip; reality was v3.4.74. Branch renumbered mid-session from `claude/v3.4.74-toolbox` → `claude/v3.4.75-toolbox`. The `ops/decisions.md` 2026-05-13 entry about demo version-number coordination now has two same-day events confirming the pattern (v3.4.67→v3.4.69 rebase AND v3.4.74→v3.4.75 rename).

**Status:** Live on demo (`eq-solves-field.netlify.app`) post-Netlify-deploy. Hub/dashboard restructure deferred (≥2 workflows now exist but each soaks separately first). NOT deployed to SKS prod (`sks-nsw-labour.netlify.app`) — `main` branch untouched.

## [2026-05-13] v3.4.74 — ESC-to-close on modals (accessibility quick-win)
**Built by:** Royce Milmlow + assistant (Night 1 audit auto-merge)
**Branch:** `claude/audit-night1-all-angles` → `demo` then `main` (PR #73)
**Changes:**
- Global `keydown` listener added in `scripts/utils.js`. Closes only the TOP-MOST open modal per press so confirm-on-top-of-edit stacks peel back rather than blowing both away.
- Behaviour-preserving, <50 lines, no auth / no RLS change — auto-merge bar met.
**Why:** Surfaced by the Night 1 manual audit run (`AUDIT-REVIEW.md`, usability angle, FINDING #U1). Modals already closed on backdrop-click and ✕-button; ESC did nothing — standard keyboard convention violation. First step of a broader accessibility pass needed for Melbourne enterprise procurement (FINDING #U2 covers `aria-*` coverage gap).
**Status:** Live on both demo and SKS prod. 7 other audit findings opened for Royce review (see `AUDIT-REVIEW.md`).

## [2026-05-13] v3.4.73 — widen week-picker so "(this week)" no longer truncates
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.73-week-pill-width` → `demo` then cherry-picked to `main` (PR #69)
**Changes:**
- Removed `max-width:80px` on `#globalWeek`; `<select>` now sizes to widest option (~150px).
- Mobile unaffected — `.topbar-week` still uses `flex:1`.
**Why:** SKS topbar dropdown was cutting "◉ DD.MM.YY (this week)" to "(t...s)" on prod.
**Status:** Live on both demo and SKS prod.

## [2026-05-13] v3.4.72 — skip render when polled data hasn't changed (kills flash)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.72-skip-render-on-unchanged` → `demo` then `main` (PR #67)
**Changes:**
- New `_computeStateSignature()` builds sort-stable signature over people / managers / sites / schedule / timesheets / leaveRequests.
- `refreshData()` diffs post-load signature against last rendered; only calls `renderCurrentPage` on actual change.
- Manual ↻ Sync still renders unconditionally for visual feedback. Signature seeded after initial load so first poll doesn't fake-trigger.
**Why:** Constant flashing on SKS prod — 30-second background poll was doing full innerHTML swap unconditionally, causing scroll jump + focus drop even with no data delta.
**Status:** Live on both demo and SKS prod. Idle background poll is now a silent no-op.

## [2026-05-13] v3.4.71 — remove Project Hours panel + fix EQ→SKS logo flash
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.70-supervisor-fixes` → `demo` then `main` (PR #64; bundled with v3.4.70)
**Changes:**
- Removed `#project-hours-panel` + script tag. Kept `scripts/project-hours.js` (parked) + `sites.track_hours` column on EQ.
- New `earlyBootBranding()` IIFE in `scripts/app-state.js` fires on DOMContentLoaded, detects slug synchronously, applies `TENANT_BRANDING` before first paint.
- `loadTenantConfig` still runs at onload for Supabase-driven access codes; `applyTenantBranding` idempotent so second call just refreshes.
**Why:** (1) Project Hours panel surfaced 'schema not applied' warnings on SKS where the migration hadn't run, added nothing useful. (2) SKS users saw EQ sky-blue logo for 200-600ms before SKS dark-blue snapped in — cause was async `loadTenantConfig()` from `window.onload` despite branding data being static per tenant.
**Status:** Live on both demo and SKS prod.

## [2026-05-13] v3.4.70 — supervisor dob/start_date + Excel date import + archive
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.70-supervisor-fixes` → `demo` then `main` (PR #64)
**Changes:**
- `migrations/2026-05-13_managers_dob_start_date_archived.sql` adds `dob_day`, `dob_month`, `start_date`, `archived` on `managers`; `archived` on `people`. **Applied to BOTH Supabase projects on 2026-05-13.**
- `import-export.js`: `_parseCsvBirthday` now matches DD/MM/YYYY; new `_parseStartDate` handles ISO + DD/MM/YYYY + Excel serial numbers.
- Supervisor modal exposes DOB + start_date. Both filter rows get "Show archived" toggle. Active/archived render-tint + handlers wired in `managers.js` / `people.js`. Badges count active rows only.
- `supabase.js`: `saveManagerToSB` sends new columns; `savePersonToSB` sends `archived`; new `archiveManagerInSB` + `archivePersonInSB` helpers via PostgREST PATCH.
**Why:** Royce CSV review 2026-05-13 surfaced: supervisors had no DOB/start_date (people had since v3.4.16), Excel uploads rejected DD/MM/YYYY + serial dates, no reversible archive (only hard delete via `deleted_at`). Contacts↔Supervisors double-up confirmed by design (Wave 4).
**Status:** Live on both demo and SKS prod. Behaviour-preserving for existing rows.

## [2026-05-13] v3.4.69 — Site Reports module + Prestart MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.67-prestart` → `demo` (PR #62) — rebased on top of v3.4.68 role-system, so the branch name keeps the original v3.4.67 label but the merge ships as v3.4.69. v3.4.67 was never released.
**Changes:**
- New "Site Reports" sidebar entry under "Testing (DO NOT USE)" section with BETA chip. v1 ships Prestart only — toolbox / diary / weekly follow the same pattern.
- Photos: max 8 per record, camera+gallery on mobile, resized to 1600px / JPEG-q70, stored inline as base64 in `prestarts.photos` JSONB. Lightbox + captions.
- Signature pad: HTML5 canvas modal, touch + mouse, DPR-aware. Saved as base64 PNG into `crew[i].signature_image`; idempotent re-tap preserved (v3.4.54 lesson).
- Offline write queue: `navigator.onLine` + try/catch around `sbFetch`; localStorage-backed queue replays on `'online'` event + page load. Per-tenant scoped. Visible pending pill in form footer.
- Mobile responsive: form grid collapses to 1 column < 640px; modal goes full-screen; signature canvas bumps to 260px for finger signing.
- Dual-source notice: dismissible yellow banner directing users away from `sks-field-reports.netlify.app`.
- **Migrations applied 2026-05-13 to BOTH Supabase projects:**
  - `2026-05-13_site_reports_v1.sql` — `prestarts` table + RLS + realtime
  - `2026-05-13_prestarts_photos.sql` — `ADD COLUMN photos jsonb`
**Why:** Path C absorb (see `ops/decisions.md` 2026-05-13) — workflows from Ben Ritchie's `sks-field-reports.netlify.app` v29 fold into EQ Field as a commercial sub-module. Prestart is the first of four (Toolbox / Diary / Weekly to follow). Lessons applied: v3.4.54 per-action inflight guards, v3.4.55 id-coercion for bigint/uuid PK portability, v3.4.56 audit failures surfaced via `console.warn` not silenced.
**Status:** Live on demo only (`eq-solves-field.netlify.app`). NOT deployed to SKS prod — gated on Ben Ritchie sign-off + Royce explicit go. 5 modified, 3 new files, ~1130 line diff.

## [2026-05-13] v3.4.68 — Phase B + C role system foundation (DEMO ONLY soak)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.68-role-system-clean` → `demo` (PR #63)
**Changes:**
- `scripts/permissions.js`: new `resolveSessionRole()` (Phase C).
- Call wired into `initApp()` + supervisor PIN unlock + lock-out.
- 5 handler gates migrated to `EQ_PERMS.can()` (Phase B v1):
  - `leave.js`: `respondLeave` / `archiveLeaveRequest` / `unarchiveLeaveRequest`
  - `timesheets.js`: `fillTsWeekFromMon` / `sendTsReminder`
- All 5 perms behaviour-preserving in both supervisor + manager tiers.
- Phase A schema applied to BOTH Supabase projects on 2026-05-13.
**Why:** Royce flagged Phase B+C risk on SKS prod; chose to ship to demo this week for a 5-7 day soak before porting. PIN-unlock-wins rule preserves today's behaviour — anyone with the supervisor PIN keeps full supervisor access regardless of DB role. Phase D will tighten this server-side later (~2 weeks, planned early June).
**Status:** Demo only. SKS stays on `isManager` binary model until demo soak passes. Plan ref: `MELBOURNE-SCALE-DESIGN.md §7 Q3`.

## [2026-04-28] Add Contact button cherry-picked to main (SKS) — PR #25
**Built by:** Royce Milmlow + assistant
**Branch:** `fix/add-contact-main` → `main` (merge commit `4f03227`,
cherry-pick of `f372a43` from demo)
**Why:** Same repo Milmlow/eq-field-app; demo branch deploys to
eq-solves-field.netlify.app (EQ Field demo), main branch deploys to
sks-nsw-labour.netlify.app (SKS LIVE — ~55 staff). The button only
shipped to demo via PR #24, so SKS staff didn't get it. Cherry-pick
brings just that one-line UX fix to main without dragging the rest
of Phase 1 (flags, perms, project-hours, role enum) onto SKS.
**Status:** Merged. Netlify auto-deploy to sks-nsw-labour.netlify.app
in flight at 2026-04-28.

## [2026-04-28] Add Contact button wired into Contacts page (PR #24)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/hopeful-wright-058c8b` → `demo` (merge commit `5105517`)
**Changes:**
- `index.html` page-contacts filter row gets a "＋ Add Contact"
  button calling existing `openAddManager()` (managers.js:109).
  No new code paths — reuses the existing modal-manager + saveManager
  flow that already lived on the Supervision page.
- Both demo (SEED) and live (eq) tenants get the button — `managers`
  is in `ORG_TABLES`, not in any `TENANT_DISABLED_TABLES` entry.
- One-line diff to a single file. No JS changes, no migration, no
  permission shape change.

**Why:** The page-contacts page (nav: "Contacts" ◉) showed staff/people
but lacked an Add affordance — anyone looking for "where do I add a
contact" landed there and saw nothing. Add button only existed on
page-managers (nav: "Supervision" ☎). UX parity fix.

**Status:** Live on eq-solves-field.netlify.app post-Netlify-deploy
(~1 min after merge).

## [2026-04-27] Phase 1 implementation kickoff — flags, perms helper, migrations
**Built by:** Royce Milmlow + assistant
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
**Built by:** Royce Milmlow + assistant
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
  `eq-context/eq/field/permissions/permission-matrix.html` plus v1
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

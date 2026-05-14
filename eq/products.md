---
title: EQ Tier — Products
owner: Royce Milmlow
last_updated: 2026-05-15
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

**Status:** Live. Current version **v3.5.0** on demo (shipped 2026-05-14); SKS prod still on **v3.4.73** awaiting clean-soak window. Phase 1 multi-tenancy live; Phase B+C role system soaked into prod 2026-05-13. Three sub-modules in active state: **Site Reports** (Prestart + Toolbox + Diary live; HUB landing in PR #85), **Tender Pipeline** (entire new workstream landed v3.4.79–v3.4.83), **Mobile-first home** (v3.5.0 staff tile screen live, supervisor variant in PR #83). Six PRs in flight against demo as of 2026-05-15 — see `eq/changelog/field.md` 2026-05-15 entry for the queue. Melbourne scaling unblocker (S1 sliding-window queries) is PR #89, ready for review.
**URL:** eq-solves-field.netlify.app (demo) / sks-nsw-labour.netlify.app (main = SKS prod)
**Repo:** Milmlow/eq-field-app (private); `demo` → EQ Field demo, `main` → SKS prod
**Working file:** index.html
**Architecture:** PWA, URL-based tenant detection
**Supabase project:** ktmjmdzqrogauaevbktn (eq-solves-field) — bypassed in demo mode
**Deploy:** GitHub push → Netlify auto (per branch)

**Strategic priority:** Sole EQ build focus until 20 paying customers.
Validation gate = 5 outside-SKS trade subbies on Field demo first.

**Site Reports sub-module (v3.4.69+, demo only):**
- THREE workflows shipped on demo (was two): Prestart, Toolbox, Diary. All under "Testing (DO NOT USE)" sidebar section with BETA chips.
- **Prestart** (v3.4.69, shipped 2026-05-13) — form + 8 photos + signature pad + offline queue + mobile-responsive. Tables: `prestarts` + `prestarts.photos` on BOTH Supabases.
- **Toolbox Talk** (v3.4.75, shipped 2026-05-14) — same shape as Prestart with workflow-specific fields (`topic`, `safety_message`, `items_reviewed`, `open_actions`, `next_meeting`, `attendance` JSONB). Tenant-neutral column names (`facilitator` not `sks_rep`). Table: `toolbox_talks` on BOTH Supabases. Code in `scripts/toolbox.js`.
- **Shared scaffold** (v3.4.76, 2026-05-13) — `scripts/site-reports-shared.js` (~470 lines) extracted the photo / signature / offline-queue helpers that had been copy-pasted between Prestart and Toolbox. Prestart shed ~310 lines, Toolbox ~290 lines. Lands before Diary so the third workflow starts lean.
- **Daily Site Diary** (v3.4.77, shipped 2026-05-13) — `scripts/diary.js` (~700 lines). Diary-specific surface: weather JSONB, shift_type, repeating sections (work_areas / delays / incidents / visitors), free-text materials_received / equipment_status / notes. Table: `site_diaries` on EQ Supabase only — SKS application gated on Royce green-light.
- **Site Reports HUB** (PR #85, v3.5.2, not yet merged) — collapses Prestart / Toolbox / Diary into ONE sidebar entry; landing page with three status cards (today / this week / today). Three originals hidden, not deleted (deep-links + home-tile pre-start tile still work).
- **Ben's preview path:** `eq-solves-field.netlify.app/?tenant=sks` — loads SKS branding + SKS Supabase data on the demo build.
- **Weekly Site Report** — ~6-8 days estimated. Gated on one supervisor actually using the three current workflows weekly. Premature today.
- **Compliance pack export** (Hammertech / Aconex / Procore) — P2, gated on all four workflows shipping (Weekly is the fourth).

**Tender Pipeline sub-module (v3.4.79+, DEMO ONLY):**
- New workstream — not in any earlier brief. Royce's mid-week pivot.
- Kanban for tracking tender opportunities through stages (watch → confirmed → likely → won/lost). Drag-and-drop transitions (v3.4.82). Enrichment slide-over. Nomination model with clash detection (`nominations`, `nomination_clashes` view). Review queue surface that doubles as a fortnightly decision queue.
- Excel ingestion via SheetJS (`scripts/tender-parser.js`). CSP needed a hotfix (v3.4.80) plus a cdnjs URL pin (v3.4.81) before this worked end-to-end.
- Pipeline Dashboard with Stage + Dept filters; Review queue with Stage filter (defaulting to "Likely + Won").
- Sidebar entries: Pipeline Dashboard, Pipeline (kanban), Fortnightly Review, Tender Sync.
- Tables on EQ Supabase only: `tenders`, `tender_enrichment`, `nominations`, `nomination_clashes` (view), `tender_import_runs`, `tender_review_decisions`, `pending_schedule`. All in `TENANT_DISABLED_TABLES.sks` until cutover.
- Status: ~1900 lines in `scripts/tender-pipeline.js` (~2000 after v3.4.80-84 patches). Royce's currently-active surface — not part of any other workstream's scope.

**Mobile-first home tile screen (v3.5.0+):**
- New surface for mobile staff (viewport <768px, `home_screen_v1` flag, `role==='staff'`). Four tiles: My Schedule, Timesheets, Leave, Pre-starts. Next-shift pill at top. Cog drawer for everything-else nav.
- Phase 2 SUPERVISOR variant in PR #83 (v3.5.1) — six tiles + action strip + richer drawer; same flag, role-branched in `scripts/home.js`.
- Decisions baked in: see `_proposals/mobile-first-nav/MOBILE-FIRST-NAV-PROPOSAL.md` v1.1 (A1/B1/C1/D/E/G1/H1/I1) and `_proposals/mobile-first-nav/STATUS-2026-05-14-EOD.md` for the v3.5.0 hand-off context.

**Melbourne scaling unblocker (PR #89, v3.5.3, DEMO ONLY):**
- Resolves Night 1 audit FINDING #S1 (HIGH severity). Sliding-window queries — STATE.schedule + STATE.timesheets now scoped to ±4 weeks instead of full-table. Lazy-load on week nav with adjacent prefetch. Cache eviction at 16 weeks.
- After this lands and soaks 3-5 days on demo (Q5 default from SPRINT-QUESTIONS), the SKS port is a one-line version bump.
- Companion findings in queue: #S2 (clusterize.js for big-list views, unblocked by S1 STATE shape), #S3 (week-scoped realtime channel, parked).

**Audit + sprint substrate (within the repo, not within this substrate):**
- `AUDIT-REVIEW.md` — Night 1 findings (8 total, 7 open) + session-summary entries appended manually. Cloud nightly schedule never reliably fired; replaced with local `/audit-multi-lens` slash command (PR #86) — `.claude/commands/audit-multi-lens.md` produces a dated artifact at `_reviews/multi-lens/YYYY-MM-DD.md`.
- `SPRINT-PLAN.md` — S1 + U2 + S2 + SEC2 design. S1 fully built per PR #89. U2 Phase 1 (axe-core CI scaffold) in PR #87. S2 + SEC2 still to come.
- `SPRINT-QUESTIONS.md` — Royce's "all defaults confirmed" answer authorised the S1 build per default-set Q1-Q13.
- `REVIEW-MULTI-LENS.md` — v1 strategic review dated 2026-05-13. Future runs via `/audit-multi-lens` go into `_reviews/multi-lens/` (append-only convention).

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

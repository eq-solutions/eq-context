---
title: EQ Tier — Products
owner: Royce Milmlow
last_updated: 2026-07-16
scope: Live EQ products, plus the canonical Killed / Deferred list (CLAUDE.md §9 points here — don't duplicate facts back into CLAUDE.md). Field section flagged stale — see banner in that section.
read_priority: standard
status: live
---

# EQ Tier — Products

Live or actively-built products below. Killed/deferred products are listed
in their own section at the bottom of this file — see there, not
`CLAUDE.md`. `/archive/` holds historical changelogs for parked work.

---

## EQ Solves — Field (LEAD MODULE)

> **This section is stale — last touched 2026-06-13, version pinned at v3.5.125.**
> `eq/changelog/field.md` and `eq/pending.md` show Field at **v3.5.331** as of
> 2026-07-15 (200+ releases and 34 days of shipped work: Site Audits,
> Apprentices module, Acknowledgments, Pipeline archive/delete, sample-data
> demo mode, calibration surface — unreflected below). Full status refresh is
> a separate follow-up; flagged, not done in this pass. Two facts below are
> corrected as of 2026-07-16: the SKS staff count, and the netlify.app URL's
> actual status (see suite-state.md, which still lists it as the live/demo
> URL — that entry needs a generator-level fix, not a hand-edit here).

**Status:** Live. Current version **v3.5.125 (STALE — see banner above, actually v3.5.331 as of 2026-07-15)**. SKS Field active on ehow. v8 design pass complete 2026-06-09 (all 14 screens + Shell warmup). Security sprint complete 2026-06-09. Shell SSO fixed 2026-06-10 (eq-shell PR #306). SKS canonical DB full JWT coverage 2026-06-11 (PR #267 — 591 sites; the "58 staff" figure from that PR is stale — **verified live 2026-07-16: 39 on-roster non-supervisor Direct staff** + 18 Labour Hire + 18 supervisors (10 off-roster, 8 on-roster) + 10 Apprentices = 88 active total. The 58→39 discrepancy Royce flagged was exactly a supervision/management counting difference, confirmed against ehow). EQ Service iframe loading fixed 2026-06-13 (eq-shell PR #334, 12s → 4s). Multi-tenant via DATA_JWT_ENABLED + per-tenant Supabase JWT.
**URL:** field.eq.solutions (live) / core.eq.solutions/sks/field (SKS prod via Shell)
**Repo:** eq-solutions/eq-field (private)
**Working file:** index.html
**Architecture:** Multi-tenant PWA. URL-based tenant detection + Shell iframe with JWT handoff. EQ tenant → eq-canonical-internal (zaap, `zaapmfdkgedqupfjtchl`). SKS tenant → ehow (`ehowgjardagevnrluult`).
**Supabase:** EQ live = `zaapmfdkgedqupfjtchl` (eq-canonical-internal/zaap). SKS live = `ehowgjardagevnrluult` (ehow). Old `ktmjmdzqrogauaevbktn` = cold backup (do not write).
**Deploy:** GitHub push → Netlify auto (main branch → field.eq.solutions). eq-solves-field.netlify.app is dead since mid-2026 — **suite-state.md's Apps table still lists it as the live/demo URL; that's generated, needs a source-data fix, not covered in this pass.**

**Strategic priority:** Lead module. Built for ourselves (SKS NSW) —
no outside-validation gate (killed 2026-06-02).

**Site Reports sub-module (v3.4.69+, demo only):**
- THREE workflows shipped on demo (was two): Prestart, Toolbox, Diary. All under "Testing (DO NOT USE)" sidebar section with BETA chips.
- **Prestart** (v3.4.69, shipped 2026-05-13) — form + 8 photos + signature pad + offline queue + mobile-responsive. Tables: `prestarts` + `prestarts.photos` on BOTH Supabases.
- **Toolbox Talk** (v3.4.75, shipped 2026-05-14) — same shape as Prestart with workflow-specific fields (`topic`, `safety_message`, `items_reviewed`, `open_actions`, `next_meeting`, `attendance` JSONB). Tenant-neutral column names (`facilitator` not `sks_rep`). Table: `toolbox_talks` on BOTH Supabases. Code in `scripts/toolbox.js`.
- **Shared scaffold** (v3.4.76, 2026-05-13) — `scripts/site-reports-shared.js` (~470 lines) extracted the photo / signature / offline-queue helpers that had been copy-pasted between Prestart and Toolbox. Prestart shed ~310 lines, Toolbox ~290 lines. Lands before Diary so the third workflow starts lean.
- **Daily Site Diary** (v3.4.77, shipped 2026-05-13) — `scripts/diary.js` (~700 lines). Diary-specific surface: weather JSONB, shift_type, repeating sections (work_areas / delays / incidents / visitors), free-text materials_received / equipment_status / notes. Table: `site_diaries` on EQ Supabase only — SKS application gated on Royce green-light.
- **Site Reports HUB** (v3.5.2, shipped 2026-05-15) — collapses Prestart / Toolbox / Diary into ONE sidebar entry; landing page with three status cards (today / this week / today). Three originals hidden, not deleted (deep-links + home-tile pre-start tile still work). Count accessors `eqGetPrestartsTodayCount` / `eqGetToolboxWeekCount` / `eqGetDiariesTodayCount` live on each workflow module.
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
- Phase 2 SUPERVISOR variant shipped v3.5.1 (2026-05-15) — six tiles + action strip ("Needs you today · N leave to approve · N pre-start") + richer drawer (Edit roster / Sites / Job numbers / Apprentices / Supervision / Import-Export / Audit log); same `home_screen_v1` flag, role-branched in `scripts/home.js`. Action-strip data via `eqGetPendingLeaveCount` (leave.js) + `eqGetPrestartsDraftCount` (site-reports.js). "Timesheets to review" count dropped from MVP — no review-state column.
- Decisions baked in: see `_proposals/mobile-first-nav/MOBILE-FIRST-NAV-PROPOSAL.md` v1.1 (A1/B1/C1/D/E/G1/H1/I1) and `_proposals/mobile-first-nav/STATUS-2026-05-14-EOD.md` for the v3.5.0 hand-off context.

**Melbourne scaling unblocker (v3.5.3, shipped 2026-05-15, DEMO ONLY):**
- Resolves Night 1 audit FINDING #S1 (HIGH severity). Sliding-window queries — STATE.schedule + STATE.timesheets now scoped to ±4 weeks (9-week window) instead of full-table. Lazy-load on week nav with adjacent prefetch. Cache eviction at 16 weeks. Bulk exports get a separate full-fetch path (`_loadFullDataForExport`).
- SKS port soak window: 2026-05-15 → ~2026-05-18 to 2026-05-20. After clean soak the SKS port is a one-line version bump to v3.5.4 against main (gated on explicit Royce green-light per Q5 default).
- Companion findings in queue: **#S2** (clusterize.js for big-list views, unblocked now that S1 STATE shape settled — next on the backlog), **#S3** (week-scoped realtime channel, parked).
- **SEC2 rate-limit schema** — `migrations/2026-05-15_rate_limit_buckets_v1.sql` shipped to demo `migrations/` directory PENDING (unapplied). Phase D will apply + wire into `verify-pin.js`.

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

**Infrastructure notes (operational):**
- **CSP:** Two sources — `netlify.toml` takes precedence over `_headers`. Always update both for any external-origin change. (Lesson from v3.4.80 hotfix where `_headers` alone was insufficient and SheetJS was blocked on live.)
- **SheetJS:** Pinned to `cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js`. cdnjs tops out at 0.18.5 — don't bump to 0.19+ from cdnjs; switch CDN to `cdn.sheetjs.com` if/when an upgrade is needed.
- **Auth:** Plaintext PIN compare in `verify-pin.js` since v3.4.36 (hash removed). TOKEN MODE live — Shell iframe mints short-lived Supabase JWT via `token-exchange.ts`. `EQ_SECRET_SALT` and HMAC token signing are dead (removed PR #326/#430). PINs live in two places (Supabase `app_config` + Netlify env vars) and must be kept in sync until the verify-pin → Supabase `app_config` refactor lands.
- **Service Worker cache:** Versioned per release (e.g. `eq-field-v3.5.3`). Users need a hard-refresh (Ctrl+Shift+R) until the auto-update toast ships.
- **Analytics IDs:** Microsoft Clarity — `wek7yeida5` (EQ tenant), `wek8dmtbuu` (SKS tenant); SKS has `strictMask: true`. PostHog EU instance.

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

## EQ Shell — PLATFORM (multi-module shell)

**Status:** Live. Phase 1.F + Sprint S3 + Sprint 7 (EQ Service cutover) + v8 design pass shipped. EQ Service Shell SSO fixed 2026-06-10 (PR #306 — `COOKIE_AUTH = false`, TOKEN MODE always). EQ Service iframe loading fixed 2026-06-13 (PR #334 — fallback timer 12s → 4s). v8 warm-sand design pass applied 2026-06-09 (auth.css, App.css, MobileRecordsDrawer, MobileTabBar). Live at `core.eq.solutions` — login → tenant home → Field iframe (SKS) + Service iframe (SKS) + Intake + Cards. EQ Field surface mounts via JWT handoff (TOKEN MODE, no second PIN). **Phase 2 sequencing by trust ladder + Royce's go.** GTM gate dead (killed 2026-06-02).

**URL:** `core.eq.solutions` (live, dog-food tenant for EQ Solutions
itself). Per-tenant subdomain alias on a single Netlify project;
Netlify wildcard not viable on external DNS.
**Repo:** `eq-solutions/eq-shell` (private)
**Working files:** `src/modules/intake/`, `src/modules/cards/`,
`netlify/functions/{shell-login,verify-shell-session,token-exchange,mint-supabase-jwt}.ts`
(mint-iframe-token deleted PR #430 — TOKEN MODE live via token-exchange.ts),
`src/App.tsx` (RequireSession + ModuleGate + `useCan()` + `<Gate>`)
**Architecture:** Vite + React 19 + TypeScript strict. React Router
v6. pnpm workspace with `@eq/*` packages vendored at
`eq-intake/eq-platform/packages/` (sibling private repo
`eq-solves-intake` — vendored because Netlify can't clone private
submodules). HS256 JWT minted by Netlify Functions, carried by
`@supabase/supabase-js` browser client. Writes route only through
`eq_intake_commit_batch` SECURITY DEFINER RPC. RLS predicates read
`app_metadata.tenant_id` (swept 2026-05-20 Phase 1.F).
**Supabase project:** `eq-canonical` (`jvknxcmbtrfnxfrwfimn`,
ap-southeast-2). Holds both control-plane (`tenants`, `users`,
`module_entitlements`) and 13 canonical entity tables. The earlier
`eq-shell-control` (`hxwitoveffxhcgjvubbd`) was decommissioned
2026-05-19.
**Netlify project:** `eq-shell` (`a3473f83-7c82-4f1e-872d-aa96eaa55172`)
**Deploy:** GitHub push → Netlify auto on `main`. Per-tenant
subdomain alias added manually (~5 min) until automated.

**Phase plan (current):**

| Phase | Goal | Status |
|---|---|---|
| 1.A–1.E | Scaffold → wire-up → Field handoff → smoke → single-canonical consolidation | Shipped (1.E on 2026-05-19) |
| 1.F | Unified Identity — `eq_role` enum + `is_platform_admin` flag, `app_metadata` claims, `useCan()` + `<Gate>`, mint-supabase-jwt, admin invite/edit, Field iframe bridge carries new fields. RLS swept across 13 canonical tables + 4 intake spine + 3 RPCs from `user_metadata` to `app_metadata`. | Shipped 2026-05-20 |
| 2 | Intake module live at `/core/intake`. Further modules sequenced by the trust ladder + Royce's go (GTM gate killed 2026-06-02). | Intake shipped; further modules sequenced by ladder |
| 3+ | Replace each EQ Field surface (roster, schedule, leave, tenders, audits, prestarts, toolbox talks) with a shell module backed by `eq-canonical`. Sequencing by the trust ladder + what SKS needs next. | Long-term |
| 4 | EQ Field demo deploy + `ktmjmdzqrogauaevbktn` Supabase decommissioned, once every surface has a shell replacement | Long-term |

**Modules in shell today:**

- **Intake** (live at `/core/intake`) — drop CSV → map → validate →
  commit via `@eq/intake` + `@eq/validation` + `@eq/confirm-ui`.
  SimPRO fixtures validated through parser + customer/contact/site
  mapping + validation legs (267 customers / 393 contacts / 544
  sites). The first real Phase 2 module.
- **Cards** (iframe wedge at `/:tenant/cards`, **canonical flip
  shipped 2026-05-21**) — mounts `eq-cards.netlify.app` Flutter web
  build. Authentication is via shell-minted JWT passed in the iframe
  URL hash (`mint-cards-iframe-token` Netlify function); no more
  email-OTP. Data lives in `app_data.licences` + `app_data.staff` on
  eq-canonical, accessed via `eq_cards_list_my_licences` /
  `eq_cards_upsert_my_licence` / `eq_cards_soft_delete_my_licence`
  RPCs that bridge the column rename (user_id → staff_id,
  photo_*_url → photo_*_path, deleted_at → active=false). Legacy
  Cards Supabase (`hshvnjzczdytfiklhojz`) is read-only rollback
  insurance until the JPG photos are also migrated (deferred — see
  `eq/pending.md` §EQ Cards).
- **Tender Pipeline** scaffolding under `src/modules/tender-pipeline/`
  is **stale exploration** — 5 page stubs ~9KB total, not on the
  roadmap. Tender Pipeline lives in EQ Field, not in the shell.
  (Royce decision pending: delete stubs or add `// stale` markers.)

**Sprint S3 surface improvements (2026-05-23):**

- **TenantHome dashboard** — hero strip (tenant name, role chip, platform_admin indicator), hero number tiles with delta labels, Snapshot stat-card grid (6 entities), recent intake activity feed (5 events, colour-coded status), module grid, Quick Actions (6 cards). Data via `eq_tenant_dashboard_counts` + `eq_recent_intake_events` RPCs.
- **Skeleton loading** — all plain "Loading…" divs replaced with Skeleton component throughout (RequireSession, RootRoute, all Suspense boundaries, entity browser, audit page).
- **AdminAuditPage rollback** — replaced `prompt()/alert()` with a proper modal UI (reason textarea, Cancel/Confirm, error + success display).
- **AdminCardsFeed** — refactored from card-per-row to standard eq-table with name/email search + per-row busy state.
- **Topbar role-gating** — admin nav items (Users, Audit log, New staff) gated by `useCan()` — labour hire and employees don't see admin links.
- **Copy sweep** — plain English throughout: "Business owner" not "Tenant owner", "Your team members" not "Tenant members", "Settings" not "Tenant settings", "Business name" not "Tenant name".
- **Seed data** — supplemental SQL added 25 licences + 22 prestart checks + 14 toolbox talks to fill thin entities. Core entities (50 customers, 100 contacts, 30 sites, 25 staff, 200 schedule, 80 timesheets, 15 leave) were already seeded from S2.

**Critical architectural risks open** (per 2026-05-20 part-d external
critique synthesis — deferred to Phase 2 resumption):

1. ~~Shared `EQ_SECRET_SALT`~~ — resolved PR #326/#430. EQ_SECRET_SALT and HMAC path removed; TOKEN MODE (Supabase JWT via token-exchange.ts) is live.
2. Single mega-RPC `eq_intake_commit_batch` — chokepoint risk before
   it hits 5 module branches.
3. No `revoked_sessions` table — cannot kill an active JWT before
   1-hr TTL.
4. Control-plane + app-data colocated in same Postgres schemas —
   regional secondary day will hurt.
5. iframe-then-replace migration with no retirement deadline — trap
   risk if Phase 2 extends past ~12 months.

Full list in `eq/pending.md` "EQ Shell + EQ Intake" section. Real,
not stale — deferred, not dropped.

**Strategic priority:** Phase 2 sequenced by the trust ladder + Royce's
go (GTM gate killed 2026-06-02). The
strategic question per ChatGPT critique (2026-05-20 part-d) is
whether EQ Shell is acknowledged as a platform-tier product (with
SLOs, oncall, dedicated headcount) or remains solo-maintained. Not a
Phase 2 question — a tier-of-company question.

**Pending:**
- [ ] Phase 2 module sequencing per the trust ladder + Royce's go
      (GTM gate killed 2026-06-02)
- [ ] Critique action items listed in `eq/pending.md` "EQ Shell +
      EQ Intake" — dual-salt rotation, revoked_sessions, schema
      split, RPC decomposition, canonical→Field one-way sync,
      token-mint audit log, vendored-package hash check, etc.
- [x] Cards Unit 4 (Flutter flip + SSO) — **SHIPPED 2026-05-21**.
      Flutter app (commit `0d14c50` on `claude/canonical-migration`,
      Netlify deploy `6a0ee741d8a5850dc763ab9b`) reads
      `app_data.licences` via the eq_cards_* RPC bridge. Shell flag
      `CARDS_USE_SHELL_SSO=true` (`8ba0d4f`). Verified end-to-end in
      Chrome MCP (decoded JWT, confirmed staff/licence chain).
- [ ] `src/modules/tender-pipeline/` scaffolding cleanup — delete
      the stub pages (not on roadmap) OR keep as future-exploration
      with a `// stale 2026-05-20` marker. Royce decision.

---

## EQ Solves — Service

**Status:** Live at eq-solves-service.netlify.app (per suite-state.md's Apps table — this line previously just said "Active development" and undersold it)
**Architecture:** Next.js + Supabase + Netlify serverless functions
**Supabase project:** ehowgjardagevnrluult (sks-canonical), `service.*` schema — migrated from urjhmkhbgaxrofurpbgc (eq-solves-service-dev) on 2026-06-08; old project deleted 2026-06-22
**Scale:** Production-level complexity, multi-tenant with Supabase RLS
**Test coverage:** None. Gate is tsc + next build. Integration tests in CI are pre-existing failures — never block a merge on them.
**Sprint cadence:** 22 sprints to date
**Deploy:** GitHub → Netlify CD
**Blocker:** GitHub MCP write access (403) — fix at `github.com/settings/installations`

---

## EQ Solves — Quotes

**Status:** RETIRED 2026. Replaced by EQ Ops (see below). Flask v1 at `quotes.eq.solutions` is the legacy pilot — no further investment. The React module rewrite (formerly Position 4 in Shell queue) is cancelled; EQ Ops supersedes it.

---

## EQ Ops

**Status:** Active development. Operational dashboards — replacing EQ Quotes.
**URL:** core.eq.solutions/ops
**Repo:** eq-solutions/eq-shell (same repo as Shell)
**Architecture:** Module within EQ Shell (Vite + React 19 + TypeScript). Reads from ehow (ehowgjardagevnrluult) via service.* views.

---

## Killed / Deferred

**EQ Variations, EQ Compliance** — killed (2026-04-29 cull).
**EQ Expenses** — internal SKS tool only, no longer an EQ product.
**EQ Quotes** — RETIRED 2026, replaced by EQ Ops (see above). Flask v1 at `quotes.eq.solutions` is decommissioned. Do not build on or extend it; work goes into EQ Ops.
**AHD** — parked to 2027 capital activation. Full detail: `archive/README.md` → `archive/changelog-ahd.md`. Not an EQ Solves product — kept here only as a pointer since CLAUDE.md previously listed it alongside these.

If Royce mentions any of these, treat as historical unless he explicitly reactivates it.

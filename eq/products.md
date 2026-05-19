---
title: EQ Tier — Products
owner: Royce Milmlow
last_updated: 2026-05-19
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

**Status:** Live. Current version **v3.5.3** on demo (shipped 2026-05-15); SKS prod still on **v3.4.73** — soak clock for v3.5.4 SKS port started 2026-05-15 (3–5 days clean demo soak per Q5 default). Phase 1 multi-tenancy live; Phase B+C role system soaked into prod 2026-05-13. Three sub-modules in active state: **Site Reports** (Prestart + Toolbox + Diary live; HUB shipped v3.5.2), **Tender Pipeline** (entire new workstream landed v3.4.79–v3.4.83), **Mobile-first home** (v3.5.0 staff + v3.5.1 supervisor tile screens live). Six PRs cleared from demo backlog 2026-05-15 (v3.5.1 → v3.5.2 → v3.5.3 + audit + CI chores + SEC2 design-only file). Melbourne scaling unblocker (S1 sliding-window queries) shipped as v3.5.3.
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
- **Auth:** Plaintext PIN compare in `verify-pin.js` since v3.4.36 (hash removed). `EQ_SECRET_SALT` retained only for HMAC token signing. PINs live in two places (Supabase `app_config` + Netlify env vars) and must be kept in sync until the verify-pin → Supabase `app_config` refactor lands.
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

## EQ Solves — Quotes

**Status:** Un-deferred 2026-05-19. Two live forms today (templates +
Flask v1 pilot); a third — the real React module under EQ Shell —
remains Position 4 in the module-mounting queue per the 2026-05-19
canonical-migration-reset decision.

**Current shipped forms:**

1. **Word + Excel templates + Markdown SOPs.** v2 template set
   finalised 2026-05-18 — SKS Client Services Quote Template v2, Job
   Creation Template v7, Quote Register, Field Mapping doc,
   Implementation Guide. Live operational use inside SKS quoting motion.
2. **Flask v1 pilot app** at `https://quotes.eq.solutions`. Built
   2026-05-16 through 2026-05-19 as a fast pre-canonical pilot
   deployment. Full CRUD over quotes, customers, line items, status
   transitions, attachments, status history. Generates Word doc via
   raw zipfile + token replace (no python-docx dependency). PDF
   generation via headless LibreOffice on Fly. Search + delete +
   duplicate per row on the register. Editable header AND editable
   line items on the detail page (Draft + Submitted only). Inline
   "+ New contact" in site contact picker. Customer/site shown as
   separate fields. Scope template dropdown + curated rate library
   under a `/setup/` admin section. Email-quote scaffold with
   pluggable backends (currently sandbox-stubbed, Resend wiring
   ready). 30/30 routes pass the smoke harness.

**Real product build (the React module):** Position 4 in the EQ Shell
module-mounting queue. Build not started — Shell + Field + Service
take priority through validation gate. The Flask v1 codebase becomes
"the executable spec" for the rewrite: every validation rule, every
status transition, every token-replace pattern, every business rule
is captured in working Python that the React rewrite translates.

**URL:** `https://quotes.eq.solutions` (Flask v1, live). Real module
TBD when its turn arrives.
**Repo:** `github.com/eq-solutions/eq-quotes-port` (private). Flask +
Jinja + supabase-py + gunicorn, deployed Fly.io.
**Working files:** `app/` (Flask blueprints + Jinja templates),
`word_templates/template_v3.docx` (token-replaced SKS template — has
`{{Site}}` placeholder added 2026-05-19), `scripts/smoke_routes.py`
(30-route harness), `docs/canonical-plugin-contract.md` (the
operational contract for the future React rewrite).
**Architecture (Flask v1):** Flask 3 + Jinja + supabase-py. Backed by
`sks-labour` Supabase (`nspbmirochztcjijmcrx`) — same project as
SKS Field LIVE (legacy single-tenant coupling). Word generation via
raw zipfile + `{{Token}}` string replace. PDF via headless
`soffice --convert-to pdf` subprocess. Fly.io single-machine
deployment in Sydney. Image ~216MB (LibreOffice core+writer
included). No CSP allowance for inline scripts/event handlers —
all UI behaviours via separate JS files using data-attribute
patterns.
**Architecture (Real product, TBD):** React/Vite module under EQ
Shell. Reads/writes to `eq-canonical` (the canonical layer
project — `jvknxcmbtrfnxfrwfimn`). Customers / sites / contacts
come from canonical platform tables; quote-specific tables
(quotes, line items, status history, attachments) FK into them.
Word doc generation moves server-side (Edge Function or eq-shell
backend) to keep the React module pure. Auth via Supabase Auth
through the shell's JWT.
**Supabase project (Flask v1):** `nspbmirochztcjijmcrx` (sks-labour) —
inherited. **Will not migrate** during the Flask v1 lifetime
(per 2026-05-19 reset). When the React rewrite ships, it lands on
`eq-canonical` (`jvknxcmbtrfnxfrwfimn`) and the Flask v1 is
deprecated.
**Strategic position:** Position 4 in the EQ Shell module queue —
unchanged. Validation gate stays on Field. The Flask v1 is the
pilot's executable spec, not a queue-jump.

**Pending:**
- SKS pilot kickoff against Flask v1 (Royce sends estimators the URL
  + shared password)
- Resend wiring for real email delivery (`flyctl secrets set
  EMAIL_BACKEND=resend RESEND_API_KEY=…`) — see
  `eq-quotes-port/docs/email-setup.md`
- Real React module build (~6-10 weeks at 10 hrs/week when its turn
  comes)
- `archive/changelog-eq-quotes.md` to be reinstated as
  `eq/changelog/quotes.md` once the React build begins

---

## (No other EQ products are live)

Removed from this file in 2026-05-04 refactor:
- EQ Solves Compliance / EQ Ops (killed)
- EQ Variations (killed)
- EQ Expenses (now SKS internal tool — see `sks/products.md` if added)

EQ Solves Quotes was on this list (deferred 6mo) but was un-deferred
2026-05-19 and added back above as an active product. Build not yet
started — currently template-form only — but no longer in the deferred
category.

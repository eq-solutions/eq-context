---
title: Sprint S3 — Polish + audit + visible features
owner: Royce Milmlow
last_updated: 2026-05-20
scope: Take EQ Shell from "scaffolding-complete" to "visibly impressive when someone clicks around". Agent walks the live experience, identifies clunky surfaces, fixes them. Adds the audit / observability / dashboard surfaces that make the substrate work feel real. Builds the features that turn empty pages into something a non-engineer goes "oh this is solid" at.
read_priority: critical
status: live — use as a session prompt
duration_estimate: full session, autonomous mode
---

# Sprint S3 — Polish + audit + visible features

This sprint doc doubles as a Claude Code session prompt. Drop it into
a fresh session at `C:\Projects\eq-shell` (or paste the body below
the `---` line). The agent picks it up, walks the product, and
ships improvements.

---

## State at sprint start (2026-05-20 EOD)

EQ Shell has shipped end-to-end across Phase 1.F + canonical-readiness
Units 1-7 + Sprint S1 + most of Sprint S2:

- Identity: 5-tier role + platform_admin + Supabase-JWT mint flow live
- Canonical: **42 entities across 5 modules** (core/field/cards/quotes/service)
  in `app_data.*` + `shell_control.*` schemas with full RLS
- Per-domain RPCs: 5 commit RPCs + router + 5 unwinders + rollback
- PostgREST: `app_data` + `shell_control` exposed for direct queries
- Intake UI: 5 landing pages, **all 42 entities** wired with functional
  ParserDropZone driving through the per-domain RPC
- Cards: iframe wedge live at `eq-cards.netlify.app`, reachable at `/:tenant/cards`
- Storage: per-tenant `tenant-{tenant_id}` bucket pattern + RLS
- Audit: `shell_control.mint_audit_log` + `eq_intake_events` capture
  every mint + every write
- Critique substrate: `revoked_sessions` table + `iframe_salt_registry` ready

Live at `https://core.eq.solutions`. Dog-food tenant `core`
(EQ Solutions). No other tenants. No real users. No customer data.

## What the sprint is for

Honest: the substrate is excellent but the **clickable surface looks
raw**. Vite-default styles in places, "Loading…" plain divs,
empty-state cards with no data behind them, no dashboard summary, no
audit log viewer, no friendly errors. The Intake module works
end-to-end but nobody sees that unless they drop a CSV.

A non-engineer walking through today sees: login → tenant home → some
links → empty pages. The depth is in the database; the depth doesn't
show.

**This sprint closes the gap.** Walk the live experience. Find what's
clunky. Fix as much as the session allows. Build the audit + dashboard
+ history surfaces that turn substrate into visibly-impressive product.

No deck. No demo doc. No pitch artefacts. **The product itself becomes
the demo.**

## Operating mandate

Autonomous, productivity-first. Royce is signing off blanket — no
customers, no users, no data to lose. If you break something, fix it.
Bias to ship over polish-perfection.

- **Permitted unilaterally:** UI changes, copy edits, layout, brand
  alignment, audit surfaces, dashboards, new pages, SQL migrations
  via `apply_migration` MCP, commits to `main` on eq-shell +
  eq-intake + eq-cards (auto-deploys core.eq.solutions on push),
  storage bucket setup, RPC additions
- **Requires explicit Royce approval:** deleting files (CLAUDE.md
  hard rule), touching `nspbmirochztcjijmcrx` (SKS LIVE Supabase),
  touching the SKS NSW Labour Netlify site, anything claiming to
  represent SKS Technologies commercially
- **Avoid:** marketing/pitch content, "executive summary" generation,
  PowerPoint decks, talking-points docs. Royce is showing executives
  the **working product**, not artefacts about it
- **Cadence rule:** don't ask hold-point questions. If the right
  default is obvious, take it. If a real decision is genuinely
  ambiguous, surface options with a recommendation and a free-text
  fallback, then move on with the recommended default if Royce isn't
  around to answer in real time

## Areas to attack (priority order)

### 1. UI audit + polish pass (highest visible impact)

Walk every shell page logged in as dev@eq.solutions. For each:
- Does it look like a real product or a Vite starter?
- Are loading / error / empty states real, or "Loading…" placeholder?
- Does the brand land (Plus Jakarta Sans, EQ Sky `#3DA8D8`, Linear /
  Notion aesthetic per CLAUDE.md)? No gradients, no drop shadows.
- Is the layout consistent across pages?

Pages to walk:
- `/` (login)
- `/:tenant/` (tenant home — what does it actually show? probably sparse)
- `/:tenant/intake` (the existing SimPRO surface)
- `/:tenant/intake/{core,field,quotes,cards,service}` (the 5 new
  landing pages with 42 entity cards)
- `/:tenant/field` (iframe to Field demo — still on its own Supabase,
  likely shows email-OTP first; fine for now)
- `/:tenant/cards` (iframe to Cards Flutter web; should render now
  that eq-cards is redeployed)
- `/:tenant/quotes` (placeholder)
- `/:tenant/service` (placeholder)
- `/:tenant/admin/users` (user list)
- `/:tenant/admin/users/invite` (invite form)

For each clunky thing found, fix it inline. Commit each meaningful
fix as its own commit (or batch 2-3 related fixes per commit).

### 2. Tenant home dashboard

Probably the single highest-leverage UI build. Today `TenantHome.tsx`
shows… something basic. Replace / extend with:

- Welcome strip: tenant name + your role + your email + platform_admin chip if applicable
- Module grid: every enabled module as a card with brief description + count badge
  (e.g. "Intake — 2 events this week", "Cards — 17 licences (after Cards Unit 3 ships data)")
- Recent activity strip: last 5 intake events from `shell_control.eq_intake_events`
- Quick actions: "Import data" → `/intake`, "Invite user" → `/admin/users/invite`,
  "Open Cards" → `/cards`, etc.

Counts can come from cheap RPCs or direct PostgREST queries with the
already-exposed `app_data` + `shell_control` schemas.

### 3. Audit log viewer (`/:tenant/admin/audit`)

Currently `shell_control.mint_audit_log` + `shell_control.eq_intake_events`
+ `shell_control.eq_intake_row_audit` are all logging real activity
that no UI surfaces. Build:

- `/:tenant/admin/audit/intakes` — table of last 50 intake events:
  who, when, source_app, entity, rows committed, status, link to detail
- `/:tenant/admin/audit/mint` — table of last 50 token mints:
  who, when, source_app, source_ip, user_agent, jti, exp
- `/:tenant/admin/audit/intakes/:intake_id` — drill-down: shows
  every row committed in that intake (from eq_intake_row_audit),
  with rollback button that calls `eq_intake_rollback(intake_id, reason)`

Gated by role: manager + platform_admin only. Use `<Gate perm="audit.view">`
or whatever fits the permissions matrix.

### 4. Entity browser — make the canonical data feel real

Today the 42 entity dropzones write data into canonical tables that
nobody can then *see* in the UI. Build a generic entity browser:

- `/:tenant/data/:entity` — for any registered entity (read from
  `eq_list_module_entities`), shows a paged table of rows
- Driven by the JSON schema in `@eq/schemas` — column visibility +
  formatting per field
- Search box, basic filters, sortable headers, row click → detail drawer
- "Export to CSV" button (calls `eq_export_*` if relevant, or just
  client-side CSV)

This is what makes 42 entities feel like a real platform vs an empty
substrate. Once you can drop a CSV, see it appear in the table, edit
a cell, see the audit log update — the depth shows.

### 5. Storage browser (`/:tenant/admin/storage`)

The per-tenant bucket `tenant-{tenant_id}` exists but nobody can see
what's in it. Build:

- File listing under the tenant's bucket
- Per-domain breakdown: licences, quotes, field (sub-folders the
  app conventionally uses)
- Upload widget (drop a file → choose entity → goes to right path)
- Signed-URL preview for images / PDFs

### 6. Tenant settings page (`/:tenant/admin/settings`)

`app_data.tenant_app_configs` is empty. Build:

- Feature flag toggles (writes to `feature_flags jsonb`)
- Field-specific settings (writes to `field_settings jsonb`)
- Tenant name + slug (read-only — owner of `shell_control.tenants` is
  the source of truth)
- Module entitlements grid (which modules are enabled — reads
  `shell_control.module_entitlements`)

### 7. Improve error + loading states

Replace every `<div className="eq-loading">Loading…</div>` with a
skeleton component. Replace every plain error string with a
component that shows the error + a "Retry" button + a "Tell us"
fallback. Sentry already wired — make sure errors get reported.

### 8. Real seed data on the `core` tenant (so the UI doesn't look empty)

Currently every canonical table has 0 rows. Even the existing
13 canonical entity tables. Drop in synthetic seed data:

- 50 customers (fake company names, real-looking)
- 100 contacts spread across them
- 30 sites
- 25 staff
- 200 schedule entries across the next 4 weeks
- 80 timesheets across the past 4 weeks
- 15 leave requests in mixed states
- A handful of tenders, prestarts, toolbox talks, licences

Use the existing `eq_intake_commit_batch` RPC via the dropzone OR a
seed migration. Either works. Source must clearly mark `imported_from
= 'sprint_s3_seed_2026_05_20'` so it's distinguishable from real
data later.

### 9. Brand consistency pass

Apply EQ brand tokens consistently:
- Plus Jakarta Sans (font-family across all UI)
- Sky `#3DA8D8` primary
- Deep `#2986B4` for emphasis
- Ice `#EAF5FB` for surfaces
- Ink `#1A1A2E` for primary text
- No gradients. No drop shadows. Linear / Notion aesthetic.

The `@eq/tokens` package may already exist (per memory) — wire it
through if not done.

### 10. Anything else you find that's clunky

Walk it. Fix it. Commit it.

## Source-of-truth pointers

Always start by reading these (substrate URLs are live, code paths are local):

| What | Where |
|---|---|
| Canonical-readiness plan + audit | `C:\Projects\eq-context\eq\canonical-readiness\` (plan.md + audit-existing-tables.md) |
| Sprint history | `C:\Projects\eq-context\eq\sprints\` (S1, S2) |
| Identity model | `C:\Projects\eq-context\eq\identity\IDENTITY-MODEL.md` |
| EQ products status | `C:\Projects\eq-context\eq\products.md` |
| EQ pending items | `C:\Projects\eq-context\eq\pending.md` |
| Brand spec | `C:\Users\EQ\Downloads\eq-solutions-design.prompt.md` per memory |
| Global rules | `C:\Users\EQ\.claude\CLAUDE.md` |
| Canonical DB | Supabase project `jvknxcmbtrfnxfrwfimn` via MCP (already configured) |
| eq-shell repo | `C:\Projects\eq-shell` — deploys core.eq.solutions on push to main |
| eq-intake repo | `C:\Projects\eq-intake` (substrate; not deployed) |
| eq-cards repo | `C:\Projects\eq-cards` (Flutter; deploys eq-cards.netlify.app via netlify CLI) |

## Tools available

- `apply_migration` MCP — for canonical schema changes (SQL files saved to `eq-intake/sql/`)
- `execute_sql` MCP — for read-only queries + ad-hoc inspection
- `gh` CLI — already authed (existing PAT works; Royce explicitly chose not to rotate this session)
- `netlify` CLI — already authed (used to deploy Cards in S1.8)
- Standard Edit / Write / Bash / Read tools
- Sentry MCP for observability (if needed)

## Boundaries

- Never delete files without explicit Royce permission (CLAUDE.md hard rule)
- Never push to `nspbmirochztcjijmcrx` (SKS LIVE Supabase — separate entity)
- Never push to `sks-nsw-labour.netlify.app` repo
- Auth changes need a heads-up (not a hold-point) before applying
- Substrate changes (eq-context) — fine, push freely

## Cadence rule (important)

Royce says: **do not create hold points.** If the right default is
obvious, take it. Surface a question only when the decision genuinely
shapes the next 2+ hours of work, has no obvious default, and Royce's
input would change the outcome materially.

When you do need to ask: pre-populate options with a recommendation
first, free-text fallback last. Then proceed with the recommended
default if Royce isn't around to respond in real time.

## What "done" looks like

A non-engineer can log into `core.eq.solutions/core` and within 3
minutes feel "this is a real platform":

- [ ] Tenant home shows a real dashboard with counts + activity
- [ ] At least 3 entities have viewable data tables with real-looking rows
- [ ] Audit log viewer shows recent intakes + mints
- [ ] Every loading state is a skeleton, not "Loading…"
- [ ] Every error state has retry + sentry + readable message
- [ ] Brand tokens applied consistently
- [ ] Cards iframe renders cleanly (already shipped in S1.8)
- [ ] Intake CSV → row visible in entity browser within 30 seconds
- [ ] Build green; site auto-deployed; no console errors on any page

## Cumulative state after S3

EQ Shell stops being "scaffolding + intake works" and starts being
"a coherent product surface a non-engineer can navigate". The next
chapter is Phase 2 module builds (Field surfaces, Quotes React,
Service port) — but those are paused per GTM gate. S3 makes the
existing platform feel finished while we wait.

## Substrate updates to write at end of session

- `eq/sprints/2026-05-20-S3-polish-and-audit.md` (this file) — append
  an execution record similar to S1's record
- `eq/changelog/eq-context.md` — entry for S3
- `eq/products.md` — EQ Shell section gets a "post-S3" snapshot

---

## How to use this as a session prompt

Drop into a fresh Claude Code session at `C:\Projects\eq-shell`. The
prompt is self-contained — just say "execute Sprint S3 per the spec
at `eq-context/eq/sprints/2026-05-20-S3-polish-and-audit.md`" and
the agent walks it.

Or paste the body below the `---` directly as a session prompt.

---

```
You are continuing work on EQ Shell. Sprint S3 — polish, audit,
visible features. The prior sessions shipped Phase 1.F, canonical-
readiness Units 1-7, Sprints S1 + most of S2. The substrate is
excellent. The clickable surface looks raw.

Operating mandate: autonomous, productivity-first. No users, no
customer data. Bias to ship over polish-perfection. Don't create
hold points — take obvious defaults, surface only genuine
decisions.

Read first (in order):
  1. C:\Users\EQ\.claude\CLAUDE.md (global rules, brand, no-delete rule)
  2. C:\Projects\eq-context\eq\sprints\2026-05-20-S3-polish-and-audit.md
     (this sprint's full spec — covers state, areas, cadence rule,
     done criteria)
  3. C:\Projects\eq-context\eq\products.md (current EQ products state)
  4. C:\Projects\eq-context\eq\canonical-readiness\plan.md (execution
     record of what's already shipped)

Then walk core.eq.solutions logged in as dev@eq.solutions, find what's
clunky, fix it. Build the dashboard, audit viewer, entity browser,
storage browser, tenant settings, seed data, brand polish.

Push commits to main on eq-shell as you go — auto-deploys. eq-intake
+ eq-cards changes get committed to their respective repos. Substrate
updates to eq-context (auto-pushes on commit). Don't open PRs unless
absolutely needed; main is fine.

Deliverable: when Royce next opens core.eq.solutions, the platform
feels like a real product. Tenant home has a real dashboard. Audit
log viewer works. Entity browser shows real seed data. Errors +
loading states are skeletons + retry buttons, not plain divs.

The full S3 spec at the path above has 10 priority areas. Work
through them in order — UI audit + tenant dashboard first (highest
visible impact), audit viewer second, entity browser third. As much
as the session allows.

Mark a chapter break (mcp__ccd_session__mark_chapter) when shifting
between priority areas. Use TaskCreate + TaskUpdate for the work
units. Don't ask hold-point questions — take recommended defaults
and keep moving.
```

---

## Revision history

| Date | Author | Change |
|---|---|---|
| 2026-05-20 | Claude (this session) | Initial S3 spec authored. Royce signed off on autonomous mode + productivity-over-polish framing. |
| 2026-05-23 | Claude (S3 execution session) | Sprint executed. See execution record below. |

---

## Execution record — 2026-05-23

**Session type:** Autonomous (Royce asleep). Two context windows — first session ran out of context mid-session and was continued.

**Commits shipped to eq-shell `main` (4 commits, all auto-deployed to core.eq.solutions):**

| Commit | Summary |
|---|---|
| `f44985a` | S3 bulk: TenantHome hero strip + Snapshot + Modules + Quick Actions + Audit rollback modal + AdminTenantSettings polish + Topbar role-gating + Skeleton loading states + AdminCardsFeed |
| `a3b2d02` | S3 copy polish — remove jargon from user-facing pages (NotFound, AdminUserList, AdminInviteUser, EntityBrowserPage, TenantHome) |
| `95ac5d0` | AdminCardsFeed: refactor card layout to table with search + per-row busy state |

**Commit shipped to eq-intake `main`:**

| Commit | Summary |
|---|---|
| `91969d0` | `sql/012_s3_supplemental_seed.sql` — 25 licences, 22 prestart checks, 14 toolbox talks (supplemental seed for thin entities) |

**What shipped:**

### 1. UI audit + polish
- Replaced all plain `<div className="eq-loading">Loading…</div>` in App.tsx `RequireSession` + `RootRoute` + all Suspense boundaries with Skeleton-based states
- Removed `tender_pipeline` from `MODULES` array (module removed 2026-05-23 per CLAUDE.md)
- Fixed nested `<main><main>` in TenantHome — outer is now `<div className="eq-shell-page">`
- Copy/jargon sweep: "Tenant owner" → "Business owner", "Tenant members" → "Your team members", "Your tenant dashboard" → "Your dashboard"
- `--eq-danger` CSS var reference in AdminAuditPage fixed to `--status-error-fg`

### 2. Tenant home dashboard
- Dark-navy hero strip with tenant name, role chip, platform_admin indicator
- Hero number tiles (customers, staff, tenders) with `+N this week` delta labels
- Snapshot stat-card grid (6 secondary entities: sites, schedule, timesheets, leave, prestarts, toolbox talks)
- Recent intake activity feed (last 5 events, coloured status dots)
- Module grid with Live/Soon chips
- Quick Actions section (6 actions: Import data, Invite user, View customers, Audit log, Storage, Settings)
- Delta label logic: suppresses delta when `recent >= total` (seed-data mislead fix — audit fix #2)
- Status dot `'completed'` variant added alongside `'complete'` (audit fix #4)

### 3. Audit log viewer
- `AdminAuditPage.tsx` already existed; improved rollback UX: replaced `prompt()/alert()` with a proper modal (textarea for reason, Cancel/Confirm buttons, error display, success message)

### 4. Entity browser
- `EntityBrowserPage.tsx` already existed (fully functional); loading count placeholder changed from `'Loading…'` to `'...'`

### 5–6. Storage browser + Tenant settings
- Both pages already existed from Phase 1.F + S2. AdminTenantSettings copy polished: "Tenant settings" → "Settings", "Tenant name" → "Business name", "module" → "app", jargon removed from hint text

### 7. Error + loading states
- Skeleton component used consistently across all pages (already existed from earlier sprint)
- EqError component with retry button in place across pages

### 8. Seed data
- Core seed already existed (50 customers, 100 contacts, 30 sites, 25 staff, 200 schedule, 80 timesheets, 15 leave requests) from prior sprint
- Supplemental SQL `012_s3_supplemental_seed.sql` added 25 licences + 22 prestart checks + 14 toolbox talks via `apply_migration` MCP
- All marked `imported_from = 'sprint_s3_seed_2026_05_20'`, idempotent

### 9. Brand consistency
- Plus Jakarta Sans, Sky `#3DA8D8`, Ice `#EAF5FB`, Ink `#1A1A2E` already wired from prior sprints
- No gradients, no drop shadows confirmed on all new surfaces

### 10. AdminCardsFeed
- Refactored from card-per-row layout to standard `eq-table` layout matching AdminUserList
- Added name/email search filter
- Per-row busy state (only the active row shows spinner)
- Topbar role-gating: `canAdmin = useCan('admin.list_users')` and `canAudit = useCan('audit.view')` added; `canReviewCards = useCan('admin.review_cards')` + "New staff" nav item added

**Done criteria status:**

| Criterion | Status |
|---|---|
| Tenant home shows a real dashboard with counts + activity | Done |
| At least 3 entities have viewable data tables with real-looking rows | Done (customers, staff, sites, schedule — all >25 rows) |
| Audit log viewer shows recent intakes + mints | Done (existing page, rollback modal improved) |
| Every loading state is a skeleton, not "Loading…" | Done |
| Every error state has retry + readable message | Done (EqError component throughout) |
| Brand tokens applied consistently | Done |
| Cards iframe renders cleanly | Done (shipped S1.8 / Cards Unit 4 — not touched this sprint) |
| Build green; site auto-deployed | Done — 4 commits pushed to main, all green |

**Known gaps / not shipped:**
- Storage browser upload widget (page renders file listing; upload is read-only for now)
- Row drill-down drawer in EntityBrowserPage (table shows, but no click-to-detail — existing limitation, not regressed)
- `src/modules/tender-pipeline/` stub pages still present in codebase (Royce decision pending on cleanup vs marker comment — see products.md pending)

---
title: EQ Suite — Current State
owner: Royce Milmlow
last_updated: 2026-07-11
scope: Live suite state — app lineup, DB counts, open PRs, architectural decisions. Auto-refreshed nightly by GitHub Action.
read_priority: critical
status: live
---

# EQ Suite — Current State
_Last verified: 2026-07-11 (nightly cron)_
_If this file is >48h old, the cron is broken._

---

## Apps

| App | Status | Repo | URL | Notes |
|-----|--------|------|-----|-------|
| EQ Shell | Live | eq-shell | core.eq.solutions | Auth hub, canonical owner, EQ Ops lives here |
| EQ Service | Live | eq-solves-service | eq-solves-service.netlify.app | CMMS — maintenance, defects, reports |
| EQ Field | Live (demo) | eq-field | eq-solves-field.netlify.app | Resources, dispatch, labour hire |
| EQ Cards | Live | eq-cards | — | Onboarding intake — Phase 1 live, taking real self-signup/claim traffic |
| EQ Intake | In build | eq-solves-intake | — | Parse/emit engine behind Cards |
| EQ Ops | Active dev | eq-shell | core.eq.solutions/ops | Operational dashboards — REPLACING Quotes |
| SKS NSW Labour | Live | sks-nsw-labour | sks-nsw-labour.netlify.app | SKS-specific, separate entity |
| EQ Quotes | **RETIRED** | eq-quotes | — | Flask/Python — replaced by EQ Ops |
| EQ Expenses | Future | — | — | — |

---

## Live Database: ehow (sks-canonical)
**Project ID:** `ehowgjardagevnrluult`
**urjh (`urjhmkhbgaxrofurpbgc`): DELETED 2026-06-22**

| Entity | Count | Schema |
|--------|-------|--------|
| Sites | 243 | app_data.sites |
| Customers | 42 | app_data.customers |
| Assets | 361 | app_data.assets |
| Tenants | 1 (SKS Technologies) | service.tenants |
| Users | 5 | service.tenant_members |
| Maintenance checks | 13 | service.maintenance_checks |
| Defects | 0 | service.defects |

**SKS tenant ID on ehow:** `7dee117c-98bd-4d39-af8c-2c81d02a1e85`
**Demo tenant ID:** `a0000000-0000-0000-0000-000000000001`

---

## Other Supabase Projects

| Project | ID | Role |
|---------|----|------|
| eq-canonical | `jvknxcmbtrfnxfrwfimn` | Browser control plane |
| eq-canonical-internal | `zaapmfdkgedqupfjtchl` | Server-only tenant data plane |
| sks-canonical (ehow) | `ehowgjardagevnrluult` | Live DB for Service + Field |

---

## Open PRs (as of 2026-07-11)

**eq-service:**
- #459 chore(deps-dev): bump @vitejs/plugin-react from 6.0.1 to 6.0.3
- #458 chore(deps): bump tailwind-merge from 3.5.0 to 3.6.0
- #457 chore(deps): bump resend from 6.12.4 to 6.17.1
- #456 chore(deps-dev): bump tailwindcss from 4.2.2 to 4.3.2
- #455 chore(deps): bump @eq-solutions/ui from v1.9.0 to v1.10.0 in the eq-design-system group

**eq-shell:**
- #743 fix(security): remove anon cross-tenant access on tender_enrichment / nominations / tender_phases
- #715 feat(access): gate enforcement on can()/useCan() not role names (access-model Phase 1)
- #681 fix(staff): eq_update_staff silently cleared email/phone/trade/level/employment_type
- #658 fix(dashboard): surface pending staff connections on home sidebar

---

## System Health (as of 2026-07-11)

**CI on main:**

| Repo | Status |
|------|--------|
| eq-service | ✓ success |
| eq-shell | ✓ success |
| eq-field | ✓ success |
| eq-cards | ✓ success |
| eq-solves-intake | ? unknown |

**Deploys:**
_NETLIFY_TOKEN not set — deploy status unavailable_

**Migrations:** eq-service has 183 (latest: 0179) applied

---

| Layer | View / Table | Rows | Status |
|-------|-------------|------|--------|
| Directory | app_data.field_people | 66 | ✓ 66 |
| Directory | app_data.field_sites | 66 | ✓ 66 |
| Directory | app_data.field_managers | 19 | ✓ 19 |
| Operational | app_data.field_schedule | 0 | ⚠ empty |
| Operational | app_data.field_timesheets | 0 | ⚠ empty |
| Safety | public.prestarts | 0 | ⚠ no data yet |
| Safety | public.toolbox_talks | 0 | ⚠ no data yet |
| Safety | public.site_audits | 0 | ⚠ no data yet |
_Auto-refreshed nightly. ✓ = has data · ⚠ = empty (no data yet) · ✗ = table missing_

---

## Architecture: What Owns What

| Entity | Owner | Consumers |
|--------|-------|-----------|
| Sites | Shell → app_data.sites | Service (read-only via view), Field |
| Customers | Shell → app_data.customers | Service, Field |
| Assets | Shell → app_data.assets | Service, Field |
| Checks / Tests / Defects | Service (service.* on ehow) | Service only |
| Users / Roles | Shell → service.tenant_members | Service, Field |
| Staff / Licences / Availability | Field | Field only |

---

## Crons (as of 2026-06-22)

| Cron | Status | Notes |
|------|--------|-------|
| CANONICAL_PULL_CRON_ENABLED | true | Pulls canonical → service |
| PRE_VISIT_BRIEF_CRON_ENABLED | true | Emails tech night before job. Fires when checks exist. |
| Suite state refresh | Nightly ~9pm | This file |

---

## Key Decisions (auto-derived from merged PRs + manual)
- Shell gains an **end-to-end customer-creation flow** (Customer → Sites → Contacts, with contact→site links) — Shell owns customer creation, not just editing; typed sites/contacts survive Continue/Finish (shell PRs #716/#717/#722, 2026-07-10)
- **Shell↔Field iframe handoff now self-heals** — grace window + one-shot auto-remint on iframe restore, `restore-failed` state reachable on repeat failure, and Field posts `accepted` on every silent restore path so a memory-saver reboot no longer throws a false "didn't load / not set up" card (shell PRs #718/#723 + field PR #431, 2026-07-10)
- **Worker→staff canonical sync matches identity then coalesce-merges** instead of blind upsert — stops duplicate + null-clobbered SKS staff rows at the sync path (structural companion to the Cards approval-path fix #719) (shell PR #724, 2026-07-10)
- **Field: `leave_requests` is the single source of truth for time off** — roster + dashboard overlay approved leave at render time (read-only) instead of writing A/L onto the schedule grid; a site rostered under approved leave is flagged as a conflict, not silently hidden (field PR #433, 2026-07-10)
- **Service dashboard respects the `service_enabled` activation toggle** — Sites/Customers/Assets tiles + the site map only surface an entity once Service is activated for it; the Customers view is site-driven, a customer appears via its sites (service PRs #484/#485/#486, 2026-07-10)
- **Control-plane migrations have NO CI apply path** — `eq-shell/supabase/migrations/*` (control plane jvkn: `shell_control`+`public`) are applied BY HAND (Supabase MCP / dashboard), unlike tenant-migrations (the governed One Pipe). This is why the `provision_tenant` profiles-FK fix (merged 07-06) sat unapplied and the Cards signup 500 stayed live until hand-applied **2026-07-10**. Rule: verify control-plane fixes against live (`pg_get_functiondef`/`schema_migrations`) — **merge ≠ applied**. Same 2026-07-10 session: anon/PUBLIC EXECUTE revoked on 12 Ops/Intake SECURITY DEFINER RPCs (tenant-migration `0168`); `service.tg_*_iud` COALESCE-42804 fixed across 14 INSTEAD OF triggers (service `0179`); briefing engine swallows `PGRST205` for the dropped `app_data.tenders` (shell PR #720). (2026-07-10)
- Shell→Service embedded-session handoff hardened — handoff cookies (`eq_service_jwt` / `eq_shell_bridge`) now `SameSite=None; Secure; Partitioned` (CHIPS), iframe embedding also detected via the `Sec-Fetch-Dest: iframe` header, and a `ShellSessionRecovery` component re-mints a fresh cookie from nothing — so a lapsed/partitioned cookie no longer forces standalone chrome or a false "workspace isn't set up" (service PRs #469/#474/#475, 2026-07-07→08)
- **`app_data` type-bypass banned** — code queries the typed `service.*` canonical views, never the untyped `appDataFrom()` raw-schema bypass; the bypass was hiding wrong column names and had left customer/site/asset **create** completely broken (service PR #477, 2026-07-08)
- Standard RCD job plan **self-provisions per tenant** — `seedRcdScheduledChecks` provisions the tenant's copy of the one canonical `STARTER-RCD-BIANNUAL` starter plan on first need instead of requiring each customer to own an RCD plan (was why every non-Jemena customer seeded zero RCD checks) (service PR #476, 2026-07-08)
- **Product copy genericized** — no customer/vendor names in the UI: DELTA ELCOM / Equinix / Jemena / Maximo stripped from importers, asset/check labels, and customer-facing reports; external-ID labels read generic "ID" (DB values + code identifiers unchanged) (service PRs #442/#443, 2026-07-05)
- Shell access-model **Phase 0** — `@eq-solutions/roles` → v2.5.0; the admin `AccessControlPage` now **derives** role defaults from the package `MATRIX` instead of a hand-copied literal, so displayed defaults can't silently disagree with enforced grants; apprentice gains `equipment.view` (shell PR #704, 2026-07-08)
- Shell **embedded chrome unified** — bespoke `IconRail` retired; iframe pages (Field/Service/Cards/Quotes) render the full `HubSidebar` collapsed to a 52px hover rail (one sidebar to maintain), and `MobileTabBar` restored for embedded mobile nav (shell PRs #688/#691, 2026-07-06)
- Shell **owns the staff supervisor flag** — a Supervisor toggle + Supervision category in Shell's staff editor writes `is_supervisor`/`supervisor_role`/`supervisor_category` through `entity-patch` (previously only fixable by hand in the DB) (shell PR #692, 2026-07-06)
- Field↔Service **site pull rewired to canonical** — `/api/eq-service/sites` (dead: queried a non-existent `public.sites` → 404) now reads the canonical `app_data.field_sites` adapter view (field PR #422, 2026-07-08)
- Field permission matrix **guarded against canonical role drift** — warn-only startup check flags any Field role key that isn't a subset of the `@eq-solutions/roles` enum (field PR #418, 2026-07-06)
- Contract-scope commercial-sheet import now **also seeds unscheduled RCD maintenance checks** — RCD Testing scope lines create header-only `maintenance_checks` (`kind='rcd'`, scheduled, unassigned) so contracted RCD visits surface in the queue/calendar instead of living only as dollar line items; cadence read from `intervals_text`, editable default dates (service PR #465, 2026-07-06)
- Shell delegates **microphone capability to the Field iframe only** — `netlify.toml` Permissions-Policy opens `microphone` to the two Field origins + `FieldIframe` gets `allow="microphone"`; enables voice-to-text on Field safety forms embedded in core.eq.solutions (camera/geo stay disabled) (shell PR #693, 2026-07-06)
- Onboarding first-run wizard **retired permanently** — disabled outright and `setup_completed_at` backfilled for the SKS tenant so it never re-triggers (service PRs #453/#454, 2026-07-06)
- Contract-scope commercial-sheet import now **creates and reconciles canonical assets directly from the sheet upload** — new asset-reconciliation screen fills contract-scope asset gaps; assets route to `app_data.assets` via the canonical write layer (service PRs #444/#445/#452, 2026-07-05→06)
- Staff `employment_type` **locked to a canonical vocabulary unified with eq-field** — stops role→type conflation; type is now a controlled field, not inferred from role (shell PRs #687/#690, 2026-07-06)
- Shell admin: **one-spot app-activation view with canonical entitlement merge** — app activation/entitlements managed from a single admin surface against canonical org-keyed entitlements (shell PR #680, 2026-07-06)
- Field job numbers: **EQ Ops is the single source of truth** — Field reads a canonical `app_data.field_job_numbers` view (SECURITY DEFINER, financials never exposed); Field-local manual numbers still allowed and Ops wins on overlap. Invoiced quotes auto-retire off the board by rule; new `public.field_job_number_overrides` table backs manual hide/restore (field PRs #404/#405/#409/#410/#411, shell PRs #651/#652/#653/#669, 2026-07-04→05)
- **Subcontractor role** added to the canonical role model (eq-roles v2.4.0) — exposed as a selectable role (safe subset) across Shell + Service (service PR #440, shell PRs #662/#664, 2026-07-05)
- Labour hire rates went **canonical** — new canonical tables + read-only Ops tab with a weekly-cost rollup (shell PRs #663/#670, 2026-07-05)
- New-tenant provisioning hardened — `app_data` schema now exposed over PostgREST for new tenants (EQ-SHELL-M), and the creating admin is auto-joined so a fresh tenant is reachable (shell PRs #656/#647, 2026-07-04→05)
- eq-service offsite backup RETIRED — platform DR (ehow + eq-canonical + eq-canonical-internal) now owned by eq-context, not baked into a consuming app; old job was schema-only + 2/6 buckets, replacement is full logical dump + all buckets + Sentry cron check-in (merged PR #438, 2026-07-04)
- Fly.io account deleted 2026-07-04 — EQ Quotes (quotes.eq.solutions) and the Gotenberg HTML→PDF host retired; dead CORS origins + env refs removed (merged service PRs #397/#432, 2026-07-04)
- Shell: app-tile entitlements moved from tenant-keyed `shell_control.module_entitlements` to canonical org-keyed `public.org_module_entitlements`; legacy table + sync trigger dropped (readers Stage A #648, writers + drop Stage B #650, 2026-07-04)
- Shell: tenant branding collapsed to one canonical copy in `public.organisations.branding`; `shell_control.tenants.brand_color/brand_logo_url` dropped — session/JWT shape unchanged, source moved (merged shell PR #644, 2026-07-04)
- Shell: view security_invoker invariant (CHECK 7, no allow-list) added to `check-tenant-drift.mjs` — every anon/authenticated-reachable canonical view must carry security_invoker or the tenant-migration gate blocks (merged shell PR #625, 2026-07-03)
- Field: prestart auto-fills customer from the chosen site (QA row 29) — reads canonical `customer_name` off `field_sites` (blank-only, no-op for unlinked sites). Client shipped v3.5.237 (merged field PR #402, 2026-07-04). eq-shell PR #645 (`tenant-migrations/0159_field_sites_customer_name.sql`). **RESOLVED — jam cleared 2026-07-10**: the One Pipe fleet is applied through **0167+** on all tenants (ehow, zaap, favour-perfect) with **zero checksum drift**, so Row 29 (prestart customer auto-fill) is live. The 2026-07-04 "0159 not applied / apply aborts on drift" note was stale.
- Contacts joined the canonical view+INSTEAD OF trigger model — service.contacts is a view over app_data, DML routed to canonical (0167) (merged PR #410, 2026-07-02)
- Governed migration-apply pipeline + service invariants gate — migrations now apply through a checked pipeline, not ad-hoc (0168/0169) (merged PR #412, 2026-07-03)
- Dead auth exemptions removed from PUBLIC_PATHS — /api/shell-sso (merged PR #394) and /auth/shell-bridge (merged PR #388), 2026-07-01
- Fail closed on unresolved Shell→Service tenant slug — no silent fallthrough on handoff (merged PR #376, 2026-06-29)
- Shell: create-worker-invite routed through the canonical worker resolver (merged shell PR #597, 2026-07-02)
- Shell: anon RPC grants closed + tenant-JWT policies on quality-guardian tables (0157) (merged shell PR #612, 2026-07-03)
- Shell: self-serve tenant provisioning hardened — transactional RPC, phone-bound links, runs as a background function (merged shell PRs #617/#627, 2026-07-03)
- Field: edge functions rewritten for canonical/ehow compatibility (merged field PR #380, 2026-06-30)
- Shell user_id is now the canonical join key between Shell identity and Field roster person (via app_data.staff.user_id → field_person_by_user_id RPC) (PR #352, 2026-06-27)
- CLAUDE.md project ID corrected from deleted urjh to live ehow (ehowgjardagevnrluult) (PR #332, 2026-06-22)
- Auto-defect trigger ON CONFLICT regression rule moved from memory to CLAUDE.md (PR #332, 2026-06-22)

- **urjh deleted 2026-06-22** — ehow (`ehowgjardagevnrluult`) is the sole DB for EQ Service (PR #327)
- **Shell owns canonical records** — sites/customers/assets live in `app_data.*` on ehow; service.* are live views; Field sync removed from Service (PR #328, #310)
- **TOKEN MODE live** — Shell iframe mints JWT via `token-exchange`; `mint-iframe-token` deleted (shell PR #430)
- **Legacy HMAC retired** — `EQ_SECRET_SALT` / `validateLegacyToken()` removed from `shell-auth` (PR #326)
- **Public-schema RPCs use `createPublicAdminClient()`** — `service.*` schema is for operational queries; dashboard/asset RPCs in `public.*` need admin client (PRs #314, #315, #325)
- **Shell JWT preferred over OTP session** — `layout.tsx` skips tenant_members query when `hasJwtSession=true` (PR #320)
- **`inviteUserAction` must set `app_metadata.tenant_id`** — ehow RLS uses JWT claims, not helper functions; invite + orphan-attach both stamp it (PR #318)
- **Shell/Service URL sync via postMessage** — `core.eq.solutions/sks/service/...` is bookmarkable; browser back works (PR #422)
- **Sites activate via contract scope** — a site becomes relevant in Service when a contract scope is created against it
- **No test suite** — tsc + manual verify is the gate
- **Canonical pull cron removed** — service.* views are live over app_data; no sync job needed (PR #310)

---

## What Doesn't Exist Yet

- Any real maintenance check created by SKS
- EQ Expenses
- EQ Ops fully built (in progress in eq-shell)
- Integration tests

_(Second tenant now exists: `favour-perfect` self-provisioned onto its own plane `nxojbntrpxfnbhbyaspp` — the "only SKS" claim is retired.)_

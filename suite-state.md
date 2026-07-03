---
title: EQ Suite — Current State
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Live suite state — app lineup, DB counts, open PRs, architectural decisions. Auto-refreshed nightly by GitHub Action.
read_priority: critical
status: live
---

# EQ Suite — Current State
_Last verified: 2026-07-03 (nightly cron)_
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
| Sites | 267 | app_data.sites |
| Customers | 42 | app_data.customers |
| Assets | 13 | app_data.assets |
| Tenants | 1 (SKS Technologies) | service.tenants |
| Users | 5 | service.tenant_members |
| Maintenance checks | 4 | service.maintenance_checks |
| Defects | 7 | service.defects |

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

## Open PRs (as of 2026-07-03)

**eq-service:**
- #414 feat: batch-resolve on /defects
- #369 chore(deps): bump docx from 9.6.1 to 9.7.1
- #367 chore(deps): bump lucide-react from 1.17.0 to 1.22.0
- #366 chore(deps): bump @eq-solutions/ui from v1.8.0 to v1.9.0 in the eq-design-system group across 1 directory

**eq-shell:**
- #614 feat(staff): Add-to-roster action — dedupe-first roster-only create
- #613 feat(customers): batch delete/archive for sites

**eq-solves-intake:**
- #58 fix(sql): stamp checksum on ledger self-inserts (gate-red fix)

---

## System Health (as of 2026-07-03)

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

**Migrations:** eq-service has 174 (latest: 0170) applied

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
- Second tenant (only SKS on ehow)
- Integration tests

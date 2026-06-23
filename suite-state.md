---
title: EQ Suite — Current State
owner: Royce Milmlow
last_updated: 2026-06-22
scope: Live suite state — app lineup, DB counts, open PRs, architectural decisions. Auto-refreshed nightly by GitHub Action.
read_priority: critical
status: live
---

# EQ Suite — Current State
_Last verified: 2026-06-23 (nightly cron)_
_If this file is >48h old, the cron is broken._

---

## Apps

| App | Status | Repo | URL | Notes |
|-----|--------|------|-----|-------|
| EQ Shell | Live | eq-shell | core.eq.solutions | Auth hub, canonical owner, EQ Ops lives here |
| EQ Service | Live | eq-solves-service | eq-solves-service.netlify.app | CMMS — maintenance, defects, reports |
| EQ Field | Live (demo) | eq-field | eq-solves-field.netlify.app | Resources, dispatch, labour hire |
| EQ Cards | In build | eq-cards | — | Onboarding intake |
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
| Sites | 0 | app_data.sites |
| Customers | 0 | app_data.customers |
| Assets | 0 | app_data.assets |
| Tenants | 1 (SKS Technologies) | service.tenants |
| Users | 0 | service.tenant_members |
| Maintenance checks | 0 | service.maintenance_checks |
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

## Open PRs (as of 2026-06-23)

**eq-service:**
- #299 chore(deps): bump @supabase/supabase-js from 2.108.1 to 2.108.2
- #292 docs: capture Shell-embed Service integration gaps (parked)

**eq-shell:**
- #177 [DRAFT] feat(field): F1 prep — tenant-config contract + schema-parity audit + auth-fork doc

**eq-solves-intake:**
- #35 fix(intake-demo): mobile responsiveness gaps, per-sheet error messages, SupabaseLikeClient relaxation
- #34 fix(design): replace all inline styles with CSS classes and CSS var tokens
- #29 docs(design): consolidate licence/document OCR onto the EQ Intake vision engine
- #13 Smart asset import: enrichment, dup detection, site fuzzy-match, photo/PDF

---

## System Health (as of 2026-06-23)

**CI on main:**

| Repo | Status |
|------|--------|
| eq-service | ✓ success |
| eq-shell | ⚠ cancelled |
| eq-field | ✓ success |
| eq-cards | ✗ failure |
| eq-solves-intake | ? unknown |

**Deploys:**
_NETLIFY_TOKEN not set — deploy status unavailable_

**Migrations:** eq-service has 151 (latest: 0150) applied

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

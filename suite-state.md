---
title: EQ Suite — Current State
description: Live suite state refreshed nightly from Supabase, GitHub, and Netlify. Read this first every session.
---

# EQ Suite — Current State
_Last verified: 2026-06-22 (live query). Updated nightly by autonomous cron._
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
| Sites | 633 | app_data.sites |
| Customers | 232 | app_data.customers |
| Assets | 4,808 | app_data.assets |
| Tenants | 1 (SKS Technologies) | service.tenants |
| Users | 5 | service.tenant_members |
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

## Open PRs (as of 2026-06-22)

**eq-shell:**
- #436 feat(worker-invites): show email in invite list
- #435 feat(pwa): web manifest + iOS meta tags
- #428 fix(eq-ops): cost back-fill, SLAB labour, decimal display
- #177 [DRAFT] feat(field): F1 prep

**eq-service:**
- #292 docs: Shell-embed gaps (parked)
- #302 #299 #298 #297 #296 dependabot (pending review)

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

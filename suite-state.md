---
title: EQ Suite — Current State
owner: Royce Milmlow
last_updated: 2026-07-04
scope: Live suite state — app lineup, DB counts, open PRs, architectural decisions. Auto-refreshed nightly by GitHub Action.
read_priority: critical
status: live
---

# EQ Suite — Current State
_Last verified: 2026-07-04 (nightly cron)_
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
| Sites | 241 | app_data.sites |
| Customers | 41 | app_data.customers |
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

## Open PRs (as of 2026-07-04)

**eq-service:**
- #437 fix: audit-log attachment upload + delete mutations (+ Zod validation)

**eq-shell:**
- #637 docs: pnpm-workspace.yaml — packages are vendored, not a git submodule
- #636 build: pin @eq-solutions/ui to release tag v1.10.0 for reproducible builds
- #635 feat(canonical-api): move APP_TENANT_SCOPE allow-list to a shell_control table

---

## System Health (as of 2026-07-04)

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

**Migrations:** eq-service has 175 (latest: 0171) applied

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
- Field: prestart auto-fills customer from the chosen site (QA row 29) — reads canonical `customer_name` off `field_sites` (blank-only, no-op for unlinked sites). Client shipped v3.5.237 (merged field PR #402, 2026-07-04). eq-shell PR #645 (`tenant-migrations/0159_field_sites_customer_name.sql`) **MERGED 07:41Z but 0159 NOT yet applied** — One Pipe apply aborts on known **checksum drift** (0084 sks / 0072 eq) before reaching 0159 (run 28650361945, exit 2), so 0 applied on both planes. Fix = re-run with `allow_checksum_drift=true` (or `reconcile_ledger` mode). Royce 2026-07-04: leave the apply to the concurrent eq-shell session. Row 29 **dormant** until 0159 lands on ehow+zaap (verified: `customer_name` still absent from `app_data.field_sites` on ehow). ehow: 30 field sites, 11 linked / 19 blank.
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
- Second tenant (only SKS on ehow)
- Integration tests

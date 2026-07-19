---
title: Access-model cluster 1 — sensitive-read split build plan
owner: Royce Milmlow
last_updated: 2026-07-16
scope: 4-repo build plan for the cluster-1 sensitive-read permission split. Root scratch doc — see README.md "Root scratch docs".
read_priority: reference
status: live
---

# Access-model cluster 1 — sensitive-read split · 4-repo build plan

**Note (2026-07-19):** this plan's own header below says "approved, not started" — per the same day's session logs, cluster 1 was actually designed, built, and shipped live the same day (2026-07-16, eq-shell PR #885). Treat this file as the historical plan, not current status.

**Date:** 2026-07-16 · **Owner:** Royce · **Status:** approved, not started
**Source:** the "feature levers" proposal + the `/sks/admin/access-control` visibility audit (2026-07-16)
**Decision log:** default = **manager + supervisor, hard cutover**; Phase-4 RLS mechanism = **Option A (role-keyed)** for v1.

---

## Goal

Split 7 sensitive reads out of the coarse per-app `*.view` keys, so opening an app no longer
implies seeing the pay / margins / PII / commercials inside it.

**Default grant: manager + supervisor, HARD CUTOVER** — roles that currently see these via the
coarse key **lose** them on rollout until re-granted. Exception: `reports.view_financial` =
**manager only** (supervisor has no Reports base grant, so a financial sub-read would dangle).

| Key | Grant | Enforced in |
|---|---|---|
| `field.view_hours` | mgr, sup | eq-field |
| `field.view_licences` | mgr, sup | eq-field |
| `field.view_rates` | mgr, sup | eq-field |
| `service.view_commercials` | mgr, sup | eq-service |
| `ops.view_margins` | mgr, sup | eq-shell |
| `entity.view_pii` | mgr, sup | eq-shell |
| `reports.view_financial` | **mgr only** | eq-shell |

**Load-bearing constraint:** these are NOT Shell-local. `@eq-solutions/roles`
(pinned `github:eq-solutions/eq-roles#v2.5.1`) is the source of truth; `check-perm-sync.mjs`
in the required `verify` CI job forces `src/permissions/**` to mirror the package exactly.
So **nothing lands in eq-shell until Phase 0 ships a new package tag.**

---

## Phase 0 — `eq-roles` → v2.5.2 *(first domino; blocks everything)*

Add the 7 keys (key + label + module) to the package permission list and their MATRIX grants,
regenerate `roles.json`, cut the tag.

Labels (plain-English, package-facing):

```
field.view_hours         "See timesheets & hours"
field.view_licences      "See worker licences & compliance"
field.view_rates         "See labour-hire / charge rates"
service.view_commercials "See job pricing & contract value"
ops.view_margins         "See cost & margin"
entity.view_pii          "See personal details (contact, DOB)"
reports.view_financial   "See GM / financial reports"
```

MATRIX additions: `manager` gets all 7; `supervisor` gets all **except** `reports.view_financial`;
every other role unchanged. Exact file shape (`permissions.ts` + generated `roles.json`, or
hand-authored json) confirmed on opening the repo.

- **Release action — Royce cuts the `v2.5.2` tag.** Claude preps the branch only.
- **Gate:** eq-roles build/tests green; `roles.json` contains the 7 keys.

---

## Phase 1 — eq-shell: pin bump + mirror *(mechanical)*

1. `package.json`: `#v2.5.1` → `#v2.5.2`; `pnpm install` to refresh `pnpm-lock.yaml`.
2. Mirror keys + grants:

```
src/modules/field/permissions.ts      + field.view_hours/_licences/_rates   → manager, supervisor
src/modules/service/permissions.ts    + service.view_commercials            → manager, supervisor
src/modules/gm-reports/permissions.ts + reports.view_financial              → manager
src/permissions/matrix.ts  ENTITY_PERMS + entity.view_pii                    → manager, supervisor
src/permissions/matrix.ts  OPS_PERMS    + ops.view_margins                   → manager, supervisor
```

- **Gate:** `pnpm check:perms` green (client ≡ package) + `pnpm run build`.
- **Inert** — no behaviour change until Phase 2 wraps a call-site.

---

## Phase 2 — eq-shell: gate the 3 shell-native reads

- **`ops.view_margins`** — margin/markup from `src/modules/quotes/quoteMath.ts`, rendered in
  `QuotesModule.tsx`, `QuotesReports.tsx`, `QuotesCustomers.tsx`. Wrap margin/cost columns in
  `useCan('ops.view_margins')`; `requirePerm` on quotes functions returning cost fields.
- **`entity.view_pii`** — DOB / emergency-contact in `src/pages/staff/staffTypes.ts`,
  `SplitPanel.tsx`, `StaffPage.tsx`. Gate PII fields in the UI; `requirePerm` on
  `staff-update.ts` / `staff-create.ts` and any staff read returning PII.
- **`reports.view_financial`** — `src/modules/gm-reports/index.tsx`; gate
  `manage-gm-report.ts` / `upload-gm-report.ts`.
- **Access Control grid** — `src/pages/AccessControlPage.tsx` `MODULES` has **no Records or
  Ops-margins columns** today (entity/ops are off-grid). Add a Records column + surface the ops
  keys so the new switches are toggleable. **Own sub-task — real surface work.**
- **Gate:** build + perm-key tests; manual smoke as supervisor vs employee.

---

## Phase 3 — iframe repos (separate PRs / deploys)

- **eq-service** — `service.view_commercials`: gate pricing/contract fields; rides its own JWT
  verify + RLS.
- **eq-field** — `field.view_hours/_licences/_rates`: vanilla-JS; hide those columns in-UI,
  enforced at the DB (Phase 4). Reads via the 60s Supabase JWT.

---

## Phase 4 — RLS (One Pipe, zaap + ehow) · **Option A (decided)**

**A — role-keyed views/RLS.** Sensitive columns exposed only when JWT `eq_role ∈ {manager,
supervisor}`. Matches the hard-cutover role default exactly; simplest; no JWT-shape change.

*Accepted limitation:* per-tenant **overrides** of a sensitive read won't reach the DB for direct
iframe reads (overrides live in `shell_control`, not the JWT). Acceptable for v1 — the chosen
default is role-based. If a tenant later needs to widen a sensitive read past role, revisit:

- **B** — JWT carries effective perms (`mint-supabase-jwt` / `token-exchange` → `app_metadata`);
  honors overrides but changes the JWT shape every RLS policy depends on (`_shared/supabase-jwt.ts`).
- **C** — server-only sensitive reads (`REVOKE` columns from `authenticated`, fetch via shell
  functions running full `can()`); cleanest correctness, data-path change in the iframes.

- Migrations via `tenant-migrate.yml` **only** — no hand-applied RLS.
- **Gate:** `check-tenant-drift` green on both planes.

---

## Order & guardrails

- **Order:** 0 → 1 → 2 → (3 ∥ 4).
- **Don't touch:** the JWT shape (Option A doesn't need it); no hand-RLS; no deploy without
  Royce's explicit word (auth-scoping change).
- **Branch:** a fresh feature branch off `main` — **not** the `frozen-window-issue` worktree this
  was planned in.
- **Cluster 3** (separate track) trimmed 11→6: keep `field.manage_roster` (confirm separable from
  dispatch), `field.manage_licences`, `field.manage_labour_hire`, `service.reopen`,
  `service.record_tests`, `ops.create_job`; fold `field.log_hours`, `field.manage_shutdowns`,
  `service.edit`, `service.manage_assets`, `quotes.edit`. Cluster 2 (4 config keys) intact.

## Artifacts

- Current-table decoder: https://claude.ai/code/artifact/e3238ff5-ab58-4978-8b29-a14e0c6bb9db
- Proposal (truth vs proposed + steelman): https://claude.ai/code/artifact/4180c053-39bb-4d67-a63e-09350893f064

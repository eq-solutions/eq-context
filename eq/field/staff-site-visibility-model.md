---
title: EQ Field — Staff & Site Visibility Model
owner: Royce Milmlow
last_updated: 2026-06-15
scope: How a staff member or site becomes visible in EQ Field — the gates, the flags, and the canonical→tenant pipeline. Includes the locked definition of the `on_roster` flag.
read_priority: critical
status: live
---

# EQ Field — Staff & Site Visibility Model

How a person or site travels from the control layer into what EQ Field
actually shows. All facts below verified live against `ehow`
(sks-canonical) + `jvkn` (eq-canonical) + the `eq-field` code on
2026-06-15.

## The `on_roster` flag (locked definition)

**Name:** `on_roster` (label "On roster").

**Definition:** `TRUE` = this person appears on the weekly roster as an
**assignable resource**. It is **independent of role**. A leading hand,
foreman, apprentice, or electrician can all be `on_roster = true`; an
office or executive person is `on_roster = false`.

**Why a separate flag (not a supervisor flag):** "A supervisor who also
appears on the roster" is **not** its own concept — it is the
combination of two independent facts: `{on_roster: true}` × `{role:
supervisor}`. Modelling it as one combined flag would break the common
cases (a regular worker on the roster; a supervisor *off* the tools).
Keep `on_roster` about roster appearance only; keep role/seniority
separate.

- **Roster grid query:** `WHERE on_roster = true AND active = true`.
- **Supervisor / management views:** filtered by role/level, not by `on_roster`.
- **Seed rule from the authoritative lists:** everyone in `EQ_People`
  → `on_roster = true`; `EQ_Supervision`-only names (e.g. GM, NSW
  construction manager, office manager, estimator, PMs) → `on_roster =
  false`; people in **both** → `on_roster = true` + supervisor role.

**Build status (2026-06-15): NOT yet implemented.** It is a 3-layer add:
1. `on_roster boolean` column on `ehow.app_data.staff`.
2. Expose it in the `app_data.field_people` view.
3. Filter the EQ Field roster grid on it.

## How a staff member becomes visible in EQ Field

A staff row in `app_data.staff` must pass **three** gates before it shows.
All three were silently blocking SKS on 2026-06-15:

| Gate | Where | Rule | 2026-06-15 state |
|---|---|---|---|
| Tenant (RLS) | base table `app_data.staff` | JWT `tenant_id` must equal row `tenant_id` | 39/40 SKS staff mis-tagged to EQ/`core` (`dcb71d03`) instead of SKS (`7dee117c`) |
| Approval | `app_data.field_people` view | `field_approved IS TRUE OR NULL` AND `active IS NOT FALSE` | **all 40 = `field_approved = false`** → all hidden regardless of tenant |
| Strict approval | secondary staff loader in `eq-field` | `staff?...&field_approved=eq.true` | 0 staff are `true` |

**Consequence:** to make a staff member appear, the import/approval must
stamp **`tenant_id = SKS` AND `field_approved = true` AND `active =
true`** (plus `on_roster` once it exists). Re-tagging the tenant alone is
**not** sufficient — `field_approved = false` hides everyone on its own.

`field_approved` is a real, intended gate (approve people before they hit
Field) — but nothing is currently approving anyone, so it functions as a
blanket hide. Either auto-approve on import or wire the Cards→Field
approval flow.

## How a site becomes visible in EQ Field

Fully wired — no code or schema change needed, only data curation.

- The `app_data.field_sites` view enforces `WHERE field_enabled = true`.
- 2026-06-15: 591 sites, **all 591 `field_enabled = true`** → Field shows
  all of them (the unmanageable noise). Curate `field_enabled` down to the
  live jobs; the full 591 stay canonical for quotes, history, and Service.
- Proven pattern: EQ Service uses the twin `service_enabled` (28 enabled).

## The canonical → tenant pipeline (verified triggers)

Source of truth for people = the control layer (`jvkn`). Triggers fan each
row out to the SKS tenant DB (`ehow`) that Field reads:

1. Write a person into `jvkn.public.workers`. Fires:
   - `trg_link_shell_user_on_worker_upsert` (BEFORE) — links/creates the
     `shell_control.users` identity, matched **by phone**.
   - `worker_canonical_sync` (AFTER) → `sync_worker_to_canonical()` →
     signed webhook (needs `WORKERS_WEBHOOK_SECRET` in the `jvkn` vault) →
     upserts `ehow.app_data.staff`.
2. Write licences into `jvkn.public.worker_credentials` →
   `credential_canonical_sync` → webhook → `ehow.app_data.licences`.
   (This path synced the live 171 licences.)
3. EQ Field boots → resolves the SKS tenant from `jvkn` → connects to
   `ehow` → RLS by JWT tenant → reads `field_people` / `field_sites`.

**Load discipline (or the mess recurs):** normalise phone to E.164
(`+61…`) — it is the identity key; stamp `tenant_id = SKS`; set
`field_approved = true` + `active = true` (+ `on_roster`); de-dupe across
`EQ_People` + `EQ_Supervision` + the existing rows.

## Related

- Identity / login (the separate worker-auth track): [ops/decisions.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/decisions.md) 2026-06-15 phone-dedup hook.
- Tenant/DB topology: [system/architecture.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/architecture.md) (control layer `jvkn` + per-tenant `ehow`/`zaap`).

# Phase 1 parity check — 2026-07-10

Gate for access-model Phase 1 (the eq-shell enforcement-conversion PR + the
eq-roles v2.5.1 package bump that unblocked it). See [`../ACCESS-MODEL-PLAN.md`](../ACCESS-MODEL-PLAN.md).

## Result: behaviour-preserving. Hash changed, and the change is exactly the intended delta — zero unexpected grants, zero revocations.

Unlike Phase 0 (byte-identical hash — the one grant change had no live holders),
Phase 1's hash **does** change, because live managers/supervisors exist and the
package now carries the three new keys. That change was expected and is fully
accounted for.

- Phase 0 "after" hash (v2.5.0): `37300a13c30ca0598bbad675dbf4eedc5245edcd5e87cecae2c833065f77eee0`
- Phase 1 hash (v2.5.1): `ff8fc9888aa6ac2bdf7375379f33358971236ea49bc2202fa488399c24f304a2`
- Artifact: [`snapshot-2026-07-10-phase1.json`](snapshot-2026-07-10-phase1.json)

## What changed and why it's safe

Two independent analyses prove behaviour preservation:

### 1. Deterministic diff (controlled variable)
The Phase 1 snapshot was computed on the **same input** as the Phase 0 "after"
snapshot (`raw-grants-2026-07-08.json`), so the *only* variable is the package
version (v2.5.0 → v2.5.1). Diffing the two per-user effective-permission sets:

| Role (label) | Users | Keys ADDED | Keys REMOVED |
|---|---|---|---|
| manager | 10 | `entity.manage_activation`, `ops.manage_rates`, `ops.view_rates` | none |
| platform_admin | 4 | same 3 (via the all-perms short-circuit) | none |
| supervisor | 3 | `ops.manage_rates`, `ops.view_rates` | none |
| employee | 32 | none | none |

- **Zero keys removed** from any user.
- **Every single row's delta equals its role's expected set exactly** — no user
  gained a key their role shouldn't have, none is missing one it should.
- The added keys map 1:1 to the pre-existing hand-rolled checks the Phase 1 PR
  converted: `entity.manage_activation` == the old `role==='manager'` activation
  gate; `ops.manage_rates` == the old `manager|supervisor` labour-hire gate;
  `ops.view_rates` was already granted client-side (the tab), now canonical.
  So no human's *actual* capability changed — the keys formalise access that
  already existed.

### 2. Live currency check (jvkn, 2026-07-10)
The snapshot input is 2 days old, so a fresh live check confirms the conclusion
still holds for the current population:

- **No `tenant_role_overrides` and no `security_group_perms` row references any
  of the 3 new keys** (both queried directly — empty). The base role matrix is
  therefore the *only* grant path for them; no tenant override or security group
  can surface them to an unexpected role (impossible anyway — the keys did not
  exist as valid PermKeys until v2.5.1 shipped).
- Current live population (active memberships): **manager 14** (incl. 4
  platform-admin), **supervisor 5**, **employee 34** (+1 platform-admin whose
  role is `employee`). **Zero apprentice / labour_hire / subcontractor.** Same
  shape as the snapshot — the 2 extra supervisors since then simply gain `ops.*`
  (matching their prior hand-rolled access); the extra employees gain nothing.
- The only live overrides in play are pre-existing and unrelated to Phase 1:
  a few supervisors hold `quotes.approve`; one SKS employee holds
  `cards.onboard` / `service.create` / `service.close`. None touch the new keys.

## Re-running
See [`README.md`](README.md). The deterministic snapshot uses the committed
`raw-grants-2026-07-08.json`; the live check is the two aggregate queries above
(role counts, and override/group refs to the 3 new keys) against jvkn
`shell_control`.

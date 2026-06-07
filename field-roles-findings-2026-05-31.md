---
title: Field roles — verified findings + a cross-app decision
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Verified read of EQ Field's role model + cross-app role decision
read_priority: reference
status: live
---

# Field roles — verified findings + a cross-app decision — 2026-05-31

Companion to `roles-canonical-audit-2026-05-31.md` §B/§D. Verified read of EQ Field's role model
vs canonical `@eq-solutions/roles`.

## Field's model (verified)

- Roles: `manager / supervisor / employee / apprentice / labour_hire` — **names match canonical.**
  Plus a pending **`regional_manager`** (DB enum added 2026-05-22, NOT yet wired into the
  permission matrix) → Field is heading to a **6th role canonical doesn't have.**
- Convention matches canonical: flat `<module>.<verb>`, no inheritance, no `is_platform_admin`.
- BUT the permission **vocabulary is Field's own domain**: modules `roster / ts / ph / leave /
  people / sites / app / reports / admin` (~50 perms) — nothing like canonical's `admin / audit /
  intake / equipment / reports` (15 perms). See `scripts/permission-matrix.js` +
  `scripts/permissions.js` (`window.EQ_PERMS.can()`).

## The "lossy 2-tier mapping" (located)

The gate/login layer collapses to binary: `scripts/verify-pin.js:346-356` mints `role` =
staff|supervisor and `eq_role = role==='supervisor' ? 'supervisor' : 'employee'`; the Shell-cookie
path (`:309`) and `auth.js` do the same. The session **token therefore carries only a binary
role.** The full 5-tier role is **re-hydrated client-side after login** from `people.role`
(`permissions.js:40-92 resolveSessionRole()`), falling back to `employee` on lookup failure. Net:
backend auth decisions never see the full tier; the frontend patches it post-login.

## The cross-app decision this surfaces (Royce)

**The canonical `@eq-solutions/roles` package is currently Shell-shaped, not truly cross-app.** Its
permission MATRIX was extracted verbatim from Shell (intake/equipment/audit). Neither Field nor
Service can consume that matrix:

- **Field** — same tier names + convention, but a totally different permission vocabulary
  (roster/timesheet/leave/...). Can reuse the *tier list*, not the *matrix*.
- **Service** — different tiers entirely (`super_admin/admin/technician/read_only`). Can reuse
  neither as-is.

For the "one role registry" goal (`auth_target_architecture`), the package needs to separate
**(a) the reusable tier list + `is_platform_admin` convention** from **(b) per-app permission
matrices.** Today only Shell consumes it cleanly *because it is Shell's model.* The real decision
is this split — not "make Field/Service import the package."

## Field adoption assessment

- Tier list + convention: **drop-in** (Field already matches).
- Permission matrix: **stays Field's own** (domain-specific) — adopt the *shape*, not Shell's perms.
- Plain-JS (no bundler) → consume `roles.json`, not `roles.ts`.
- Real work = **auth-token fidelity**: fix `verify-pin.js` to carry the full `people.role` in the
  token so the backend (not just the client) knows the tier. **This is an auth change → gated,
  needs explicit deploy approval.**
- Decisions first: where does `regional_man
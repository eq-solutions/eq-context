# Service ← canonical identity seam (Mechanism A: Shell members API)

**Status:** Design locked 2026-06-25 (Royce). Decision: EQ Service moves to **pure
canonical identity** — no local user master. North star = identity is a canonical
entity like customers/sites/assets; Shell (`shell_control.users` on eq-canonical /
jvkn) is the sole source of truth. Service reads members **live** and stores the
**canonical Shell user id** on every reference.

This supersedes the local `service.profiles` + `service.tenant_members` stores as
masters. They become a temporary read-cache until Phase 2/3 retire them.

---

## Why (verified facts, 2026-06-25 session)

- **Two UUID spaces for the same person.** Shell = `shell_control.users.id` (jvkn);
  Service = `service.profiles.id` (ehow). They never matched. The JWT's `sub` is the
  Shell id; every `assigned_to` / audit / `created_by` in Service is the ehow id —
  so "My checks" and self-assignment silently break for embedded sessions.
- **Stores already drifted:** Shell has 11 active SKS users; Service knew 5, and 3 of
  those 5 had the wrong role (Luke + Matthew = manager in Shell, employee in Service).
- **Live token IS a Supabase JWT** carrying `app_metadata.eq_role` (HMAC bridge token
  is dead code on the Shell side; verified in `token-exchange.ts`). So role is already
  canonical-in-session; the drift only bites DB-derived member lists.
- **No hard FKs** on `service.*` point at `profiles`/`tenant_members` — identity
  columns are loose UUIDs. Pure Option 3 needs no FK surgery; reference migration is
  plain UPDATEs.
- **No data path exists yet:** ehow has no FDW / bridge view onto jvkn, and Service's
  env has no eq-canonical key. Hence the need for a Shell-side API.

## Mechanism decision: A (Shell members API), not B (FDW)

B (cross-project `postgres_fdw` from ehow→jvkn) would store jvkn DB creds *inside*
ehow — directly worsening the S5 "key concentration" finding from the cross-app audit.
A keeps Shell as the sole holder of canonical keys. **Chosen: A.**

---

## Phase 1 — eq-shell endpoint (build in eq-shell repo)

Add an authenticated server-to-server endpoint returning a tenant's members from
canonical:

```
GET /.netlify/functions/list-members?tenant=<slug>
Auth:   header  x-eq-service-key: <EQ_SERVICE_API_KEY>   (shared secret, mirror the
        existing EQ_PLATFORM_ADMIN_KEY pattern; set on BOTH eq-shell and eq-service
        Netlify sites)
Source: shell_control.users u
        JOIN shell_control.user_tenant_memberships m ON m.user_id = u.id
        WHERE m.tenant_id = <resolved from slug> AND u.active AND m.active
Returns: [{ id, email, name, role, active }]   // id = shell_control.users.id (CANONICAL)
```

Notes:
- Resolve slug→tenant id the same way `token-exchange.ts` already does.
- `role` = the per-tenant membership role (`user_tenant_memberships.role`), not the
  user's home role.
- Return only active users + active memberships (Service shows the live roster).
- No platform-admin leakage needed (this is a roster, not a session).

## Phase 2 — eq-service consumes it

- Server helper `getCanonicalMembers(tenantSlug)` → calls the endpoint with the shared
  key, caches per-request. Used by: maintenance Assign To dropdown, /admin/users,
  activity-feed name resolution.
- Identity = canonical id everywhere. Dropdown option values = canonical user id.

## Phase 3 — eq-service writes canonical + migrate history

- New writes already have the canonical id in the JWT `sub` — store it on
  `assigned_to` / `created_by` / audit `user_id`.
- Migrate the 5 existing SKS users' references ehow→canonical (loose UUID UPDATEs,
  no FKs). Map (ehow → jvkn):
  - royce  f4bd3058-5dc7-4d70-80b8-2dbc33de7231 → 85e30693-b467-407a-88e8-539e345b88cd
  - matthew 55891733-dfe2-4cf5-be1d-461c84547524 → 7d5cac9a-57d7-4e87-922e-b3da2d703dc3
  - luke   9b8f72c9-a54b-4ec1-b7fc-2575caef19cf → 155ac75c-bcd8-41c2-834c-cf119cce0ec0
  - emma   af9124f8-c90c-415e-b4db-ee435d865d1e → 1aab4584-abf5-46b7-a5b5-980c4de01c77
  - dev    425c29c2-127e-42ec-b002-be0bf9bb35b8 → b508008d-35d7-45c4-9e0e-8b3f17eeacf1
  (Tables holding user ids: maintenance_checks.assigned_to, audit_logs.user_id, and
  any *.created_by — enumerate before running.)
- Re-key the shell-auth JWT path: cookie `sub` = canonical id (stop re-keying to a
  local profile id). RLS is keyed on `app_metadata.tenant_id`, not `sub`, so safe.
- Retire `service.profiles` + `service.tenant_members` (drop or empty to audit-cache).

## Phase 4 — eq-service admin cleanup

- Remove the email-invite + hard-delete UI in `/admin/users`. It becomes a read-only
  roster with "Users are managed in EQ Shell." Role changes happen in Shell.

## Gates

- Every deploy = explicit Royce sign-off (auth flow).
- Phase 1 is eq-shell; Phases 2–4 are eq-service. Don't cross-edit repos.
- `EQ_SERVICE_API_KEY` is a new shared secret — set in Netlify env on both sites,
  never committed.
- Interim: `service.profiles` co-tenant RLS fix (eq-service commit 93c7876) stays live;
  the local cache still serves until Phase 2/3 retire it.

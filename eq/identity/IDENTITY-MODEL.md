---
title: EQ Solutions — Unified Identity & Permissions Model
owner: Royce Milmlow
last_updated: 2026-05-20
scope: Authoritative cross-product reference. Every present and future EQ Solutions product (Field, Quotes, Cards, Service, Intake, Tender Pipeline, anything that follows) conforms to this model. Governs the 5-tier role system, the platform-admin escape hatch, naming conventions for roles and permission keys, the invite flow, session lifecycle, and the JWT shape that lets modules talk directly to Supabase.
read_priority: critical
status: live
---

# EQ Solutions — Unified Identity & Permissions Model

**Status:** Draft v1, 2026-05-20.
**Implementation owner (shell side):** see [eq/identity/PHASE-1F-PLAN.md](./PHASE-1F-PLAN.md).
**Scope:** Authoritative reference for every present and future EQ Solutions product (Field, Quotes, Cards, Service, Intake, Tender Pipeline, and anything that follows). Every new module shipped under the EQ shell must conform to this document.

---

## 1. The principle in one sentence

A user signs in once at `<tenant>.eq.solutions`. From that moment, their identity — who they are, what role they hold, what modules they can touch — is **the same across every EQ product** for the life of that session.

## 2. Why this exists

The SaaS stack EQ is positioning against treats permissions as a per-app problem. SharePoint has one model. Simpro has another. Every bespoke tool has a third. The same human ends up with different access in each, naming conventions don't line up between products, and admins can't reason about access in one place.

By owning the shell across every EQ product, we offer a **single unified identity layer**:

- One login. One session. One role.
- `supervisor` means the same thing in Quotes as it does in Field.
- A permission key like `cards.issue` is structurally the same as `quotes.approve` — readable, predictable, auditable.
- An admin invites a user once with the right role; the user has consistent access everywhere from day one.

This consistency is itself a product feature.

## 3. The five tiers

| # | Role key | Label | Business meaning |
|---|---|---|---|
| 1 | `manager` | Manager | Tenant owner. Full control of the tenant's data, users, and module entitlements. Typically the business owner or operations lead. |
| 2 | `supervisor` | Supervisor | Team-level operations. Approves work, reviews team output, manages day-to-day for a group of employees. |
| 3 | `employee` | Employee | Default working role. Performs their assigned work in each module. Reads what they need, writes their own contributions. |
| 4 | `apprentice` | Apprentice | Employee-equivalent baseline, with apprentice-specific tooling (training records, mentor visibility). Limited write scope on commercial data. |
| 5 | `labour_hire` | Labour Hire | Minimal access. Sees their own roster, submits their own timesheet, nothing else. Treated as transient by default. |

Roles are **ordered** for readability but enforcement is **not** inheritance-based. A manager only "has" everything because the permission matrix lists everything against `manager`, not because of an implicit "manager inherits supervisor inherits employee" rule. This keeps every permission decision explicit and auditable.

### 3.1 Platform admin (orthogonal)

`users.is_platform_admin: boolean` — separate boolean alongside the role. When true, the user is EQ Solutions internal staff with cross-tenant access. The shell's `useCan()` helper short-circuits to `true` for any permission key when this is set. Single audit point for "this user can do this across every tenant."

Examples of who gets `is_platform_admin = true`: EQ Solutions support staff troubleshooting a customer issue, EQ Solutions ops staff doing onboarding, Royce.

`is_platform_admin` does **not** replace the role. A platform admin still has a role (typically `manager`) — the boolean is layered on top.

### 3.2 The auth entity vs the operational entity

Role lives on **`users`** — the auth entity (someone who logs in via `shell-login`). Operational entities like **`staff`** (a tradie working on a site, holding qualifications, appearing on rosters), **`people`** in EQ Field's legacy model, or any other person-shaped record in a module's domain, are *separate tables*.

A `user` row may correspond to a `staff` row via a `staff.user_id` FK when the person is both an authenticated user **and** an operational worker. But:

- Not every `staff` is a `user`. A labour_hire person captured for a project might never log into the shell — they exist as a `staff` row only.
- Not every `user` is `staff`. A `manager` who only configures things and never appears on a roster exists as a `user` row only.

The role + permission system gates **what the logged-in `user` can do**. The data model around `staff` and other operational entities is independent and managed per-module against `eq-canonical`. When the two are linked (one human is both), `staff.user_id` is the join.

## 4. Naming conventions — non-negotiable

Every new EQ product follows the same conventions. No locally-invented role names, no app-specific permission key shapes.

### 4.1 Role keys

Use exactly the strings in §3: `manager`, `supervisor`, `employee`, `apprentice`, `labour_hire`. Lower case, snake_case where needed. No app may introduce alternates (`viewer`, `editor`, `owner`, `staff`, `admin` are all forbidden).

If an app feels it needs a new role tier, that's a conversation to add it here — not a conversation to fork the model locally.

### 4.2 Permission keys

Shape: `<module>.<verb>[_<scope>]`

- `<module>` — the module slug (`field`, `quotes`, `cards`, `service`, `intake`, `tender`). Lowercase, singular.
- `<verb>` — the action being gated (`view`, `create`, `edit`, `delete`, `approve`, `import`, `export`, `issue`, `assign`, ...). Present tense, lowercase.
- `_<scope>` — optional scope qualifier when the same verb means different things at different scopes (`_self`, `_team`, `_tenant`, `_all`). Use sparingly; default scope is the most natural one for the verb.

Examples (illustrative, not exhaustive):

| Key | Meaning |
|---|---|
| `field.view_dashboard` | See the EQ Field dashboard |
| `quotes.approve` | Approve a quote (tenant-wide default scope) |
| `cards.issue_team` | Issue cards to one's own team |
| `cards.view_wallet` | See one's own wallet of qualifications |
| `service.create_workorder` | Create a new service work order |
| `intake.import` | Import data via the intake module |
| `tender.view` | See the tender pipeline |

Same verb across modules should mean the same kind of operation. If `quotes.approve` means "give a final sign-off that releases the artefact downstream," then `tender.approve` should mean the equivalent for tenders — not "tick a checkbox somewhere in the UI."

### 4.3 Where perm keys live in code

Each module declares its own perm keys in its own folder:

```
src/modules/<module-name>/permissions.ts
```

The shell composes them at build time into a master `Record<EqRole, Set<PermKey>>`. No module's perm keys live in another module's file. No module's perm keys live in a database table.

A module's `permissions.ts` exports two things:

1. The list of perm keys this module owns (a `const` array, so TypeScript can derive a literal union type).
2. The matrix — for each of the 5 roles, the subset of this module's perm keys that the role holds.

The shell's `useCan()` is a synchronous lookup: `useCan('field.view_dashboard')` → reads the role from `SessionContext` → looks up the master map → returns boolean. No async, no fetch, no flash on render.

## 5. The invite flow

An admin invites a user. That's where role + module entitlements are set.

1. Admin navigates to `Settings → Users → Invite User` on the shell.
2. Admin chooses: email address, role (one of the 5 tiers), module entitlements (which of the tenant's modules the user can access).
3. Shell creates a `users` row (active = false, no pin_hash yet) and sends an email with a one-time link to a "set your PIN" landing page.
4. User clicks the link, chooses a PIN, lands in the shell signed in.
5. From that first session forward, the role and entitlements are part of who they are. Editable by an admin afterwards, but always present.

The role is **not** something the user chooses or can change about themselves. It's part of how the admin who invited them defined their place in the tenant.

### 5.1 Editing a user later

`Settings → Users → <user> → Edit` lets an admin change the role, toggle module entitlements, deactivate the user. Changes take effect on the user's **next login**, not live (see §6).

## 6. Session lifecycle and propagation

When a user logs in, two artefacts get minted:

### 6.1 The shell session cookie

Signed into the `eq_shell_session` cookie (HttpOnly, Secure, SameSite=Lax, Domain=`.eq.solutions`, 7-day TTL). The payload:

```ts
{
  user_id: string,
  tenant_id: string,
  role: 'manager' | 'supervisor' | 'employee' | 'apprentice' | 'labour_hire',
  is_platform_admin: boolean,
  exp: number  // epoch ms
}
```

This is the source the shell reads. `SessionContext` exposes it plus the hydrated `user`, `tenant`, and `entitlements` to every component in the tree.

### 6.2 The Supabase JWT (for modules that talk to Supabase directly)

Some modules don't run in-shell — they have their own runtime (the Cards Flutter app, a future native iOS app, etc.) and they hit Supabase directly. RLS is the gate. For RLS to work, the JWT they present must carry the same identity the shell holds.

The shell's `/.netlify/functions/mint-supabase-jwt` endpoint mints a Supabase-format JWT signed with the project's JWT secret. The payload follows Supabase's convention:

```ts
{
  sub: user_id,                  // Supabase auth.uid()
  aud: 'authenticated',
  role: 'authenticated',         // Supabase's *Postgres* role, NOT the EQ tier
  app_metadata: {
    tenant_id: string,
    eq_role: 'manager' | 'supervisor' | 'employee' | 'apprentice' | 'labour_hire',
    is_platform_admin: boolean
  },
  exp: number,                   // epoch seconds, short TTL (15 min default)
  iat: number
}
```

RLS policies on `eq-canonical` read `auth.jwt() -> 'app_metadata' ->> 'tenant_id'` to scope rows to a tenant, and `auth.jwt() -> 'app_metadata' ->> 'eq_role'` for role-gated reads/writes.

The JWT is **short-lived** (15-minute default) and **refreshable** via the shell session cookie. Modules call `mint-supabase-jwt` at startup and again before the JWT expires; they never store it long-term.

Note: `role: 'authenticated'` in the JWT is Supabase's Postgres-role slot — required by Supabase's gotrue/postgrest stack. The EQ tier ("supervisor" etc.) goes into `app_metadata.eq_role`, never into the top-level `role` field, to avoid collision.

### 6.3 Propagation timing

Role and entitlement changes take effect on the user's **next login**, not in their current session. This is an explicit trade. Live propagation would require either polling the server or a websocket connection sending role-changed events — both fight the "session is the single source" principle. The trade for that simplicity is: when an admin demotes a user from `supervisor` to `employee`, the change applies on their next sign-in. Deactivating a user *does* propagate on next request (the session lookup checks `users.active`).

The Supabase JWT, being short-lived, propagates role changes within at most one JWT TTL (15 min) — but it still requires the user's session to refresh against the cookie first, so the effective propagation is "next login."

## 7. Bridging already-shipped surfaces

Three surfaces predate or co-exist with this model and need explicit bridges:

### 7.1 EQ Field (iframe — HMAC handoff)

EQ Field is loaded via iframe with a 60-second HMAC handoff token from `/.netlify/functions/mint-iframe-token`. The token currently carries `{ kind, name, role: 'staff' | 'supervisor', exp }`.

**Bridge:** extend the token to carry `eq_role` (full 5-tier value) and `is_platform_admin`. EQ Field's `verify-pin` (action `verify-shell-token`) gets a follow-up patch to read both. Field's existing 2-tier internal gate becomes a derived view of the 5-tier model:

| EQ canonical role | EQ Field internal role |
|---|---|
| `manager` or `is_platform_admin = true` | `supervisor` (Field-side) |
| `supervisor` | `supervisor` (Field-side) |
| `employee` / `apprentice` / `labour_hire` | `staff` (Field-side) |

This mapping lives in `mint-iframe-token.ts` and is the only place Field's narrower model leaks into the shell. When Field is decommissioned (Phase 4 of the overall shell plan), the mapping deletes.

### 7.2 EQ Cards (Flutter app — Supabase JWT)

Cards talks to Supabase directly from its Flutter runtime. It receives a shell-minted Supabase JWT (see §6.2) via the iframe URL hash on first load, stores it in `flutter_secure_storage`, and refreshes it before expiry by calling `mint-supabase-jwt` through a postMessage bridge to the shell. RLS on `eq-canonical` enforces tenant + role scoping; Cards never trusts client-side checks.

See the Cards canonical-migration plan at [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) for the Cards-side implementation. Cards is the first consumer of `mint-supabase-jwt`.

### 7.3 EQ Intake (in-shell module)

Intake runs inside the shell, not in an iframe. It reads `SessionContext` directly via `useSession()` + `useCan()`. For Supabase calls that need RLS, it uses the same `mint-supabase-jwt` flow as Cards — but invoked in-process by the shell, not via postMessage.

## 8. Tenant entitlements vs role permissions

Two layers, both required:

1. **Tenant entitlement** (`module_entitlements` table) — does this tenant have access to this module at all? Set per tenant. If `quotes` is not in the tenant's entitlements, no user in that tenant sees Quotes, regardless of role.
2. **Role permission** (in-code matrix) — given the tenant has the module, what can this specific user do inside it?

A module is **visible and reachable** when the tenant's entitlement says yes. Specific actions inside it are gated by role.

Example: SKS Technologies has `cards` enabled (tenant entitlement). Within SKS, a `manager` can issue cards (`cards.issue`), a `supervisor` can view team cards (`cards.view_team`), a `labour_hire` sees nothing (no `cards.*` perms for that role).

## 9. What this model is not

- **Not** a per-app permission system. There is one model; every app conforms.
- **Not** RBAC + ABAC. It's straight role-based with explicit per-role permission lists. No attribute-based rules (no "users in region X can see records tagged Y") — if a feature needs that level of granularity, that's a conversation to extend the model deliberately, not a conversation to fork it.
- **Not** dynamic / database-backed. The matrix is static, committed to the repo, versioned by git. No admin UI for "edit what supervisors can do" — those edits land as PRs, get reviewed, and ship in a release.
- **Not** Supabase-Auth-managed. We don't use Supabase's `auth.users` table for our identity. We mint our own JWTs against `public.users` on `eq-canonical`. RLS reads `app_metadata.tenant_id` and `app_metadata.eq_role` from the JWT we sign. This means we own the auth surface end-to-end; trade is that Supabase magic-link / OAuth flows are not available without bridging code we'd have to write.

## 10. Hard rules — checklist for any new module

Every new module PR that adds a gated screen or action must:

- [ ] Declare its perm keys in `src/modules/<module>/permissions.ts`
- [ ] Follow the `<module>.<verb>[_<scope>]` naming
- [ ] Gate every gated UI surface with `useCan()` or `<Gate>`
- [ ] Confirm `module_entitlements` row exists for every tenant that should see the module (one-line migration alongside the module's first PR)
- [ ] Update §4.2 of this doc if introducing a new verb that doesn't appear in any existing module yet (so future modules can reuse it consistently)
- [ ] Never read role from anywhere except `useSession()` (in-shell) or `app_metadata.eq_role` (in modules talking to Supabase directly)
- [ ] Never call out to fetch permissions at runtime
- [ ] If the module runs outside the shell (Flutter, native, etc.), present a fresh `mint-supabase-jwt`-issued token on every Supabase call; refresh before expiry

## 11. Open questions to settle before implementation

These need decisions before [Phase 1.F](./PHASE-1F-PLAN.md) starts; tracked here so they're not forgotten.

1. **PIN vs password.** Today the shell uses bcrypt-hashed 4-character PINs. For the unified-identity story, is PIN sufficient long-term, or do we move to per-user passwords + MFA at some point? Affects the invite/landing flow design.
2. **Multi-tenant membership.** Can one user belong to multiple tenants? Today `users.tenant_id` is a single FK, implying no. If yes (e.g. a contractor working for SKS *and* Melbourne), the data model and login UX need different shapes — separate accounts vs a tenant switcher.
3. **Role granularity beyond 5.** Does the AHD programme (or any near-term plan) need a 6th tier? If so, add it here before any code lands.
4. **Self-service invite acceptance.** Does the "set your PIN" landing page also let the user set their display name, or is that admin-controlled at invite time?
5. **JWT TTL and refresh strategy.** 15 minutes is the proposed default for the Supabase JWT. Cards' Flutter app will be the first real consumer — confirm the refresh cadence works for offline-tolerant use (e.g. a tradie on-site with patchy signal photographing a licence).

---

**Versioning:** this doc gets a version bump (v1 → v2) any time the role list, naming conventions, session payload shape, or JWT shape changes. Modules pin themselves to a version in their `permissions.ts` so a breaking change is visible in PR review.

**Related:**
- [eq/identity/PHASE-1F-PLAN.md](./PHASE-1F-PLAN.md) — eq-shell implementation plan for this model
- [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) — Cards is the first consumer of the Supabase JWT (§6.2 + §7.2)
- [eq/field/permissions/](../field/permissions/) — EQ Field's original 5-tier matrix; this doc supersedes it as the cross-product spec, Field becomes a derived view (§7.1)
- [eq/field/multi-tenancy/](../field/multi-tenancy/) — EQ Field's multi-tenancy plan; §1.5 of that doc is where the 5-tier system first appeared

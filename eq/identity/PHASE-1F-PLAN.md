---
title: EQ Shell — Phase 1.F implementation plan (unified identity layer)
owner: Royce Milmlow
last_updated: 2026-05-20
scope: Implementation plan for the eq-shell side of the unified identity model. Expands shell-login/verify-shell-session/SessionContext to carry the 5-tier role + platform-admin boolean; adds a per-user Supabase JWT minter consumed by Cards and Intake; adds admin invite + edit UX; bridges EQ Field's iframe handoff. Predecessor Phase 1.E (Supabase consolidation). Blocks all module-shipping work until merged.
read_priority: critical
status: draft (pre-implementation)
---

# Phase 1.F — Unified Identity & Permissions (eq-shell implementation)

**Status:** Plan drafted 2026-05-20, not started.
**Companion doc:** [IDENTITY-MODEL.md](./IDENTITY-MODEL.md) — the authoritative spec this plan implements.
**Predecessor:** Phase 1.E (Supabase consolidation onto `eq-canonical`).
**Blocks:** Phase 2 (Tender Pipeline import), Cards Unit 4 (Flutter flip to canonical), and all future module-shipping work. `claude/phase-2-import-screen` (Tender Pipeline) and `claude/cards-iframe-embed` (Cards iframe wiring) stay live in parallel but neither ships to production until Phase 1.F merges.

---

## Context update — 2026-05-20 evening (read before starting)

Two facts landed between plan-draft (morning) and plan-execution (evening) that change Step 1's scope. Neither breaks the plan; both expand it slightly.

**1. There are now 13 canonical entities, not 12.** The Cards canonical-migration ([eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md)) added `licences` as the 13th entity. Applied to `eq-canonical` 2026-05-20 evening as migration `2026_05_20_licences_commit_path_and_drop_4arg_overload`. The new table has 4 RLS policies (select/insert/update/delete) all reading `auth.jwt() -> 'user_metadata' ->> 'tenant_id'`. Step 1's sweep needs to cover these.

**2. The user_metadata → app_metadata sweep is implicit in this plan, not explicit.** Step 1's SQL block below adds the enum + `is_platform_admin` + `user_invites` table, but does **not** include the canonical-wide RLS rewrite from `user_metadata.tenant_id` to `app_metadata.tenant_id`. That sweep is the architectural prerequisite for the Supabase JWT minter in Step 4 to actually work end-to-end. Supabase's database linter currently reports **28 ERROR-level `rls_references_user_metadata` warnings** across the canonical (12 entity tables + 4 licences policies + intake spine tables = 28). After Step 1's sweep lands, that count must drop to ≤5 (the by-design SECURITY DEFINER warnings + leaked-password toggle remain).

**Action for the executing session:** before running Step 1, either expand the migration SQL to include the user_metadata→app_metadata sweep across all 13 entity tables + intake spine, OR explicitly add a Step 1.5 doing the sweep separately. Either is fine; the gate is "no `rls_references_user_metadata` warnings remain after the new migration."

**Full context on what landed 2026-05-20 evening:** [sessions/2026-05-20-part-c.md](../../sessions/2026-05-20-part-c.md).

**Existing canonical migrations as of this update:**

```
20260519093858  2026_05_19_shell_control_plane
20260519105945  2026_05_19_enable_intake_for_core
20260519111130  2026_05_19_canonical_select_rls_policies         <-- these are the user_metadata policies to rewrite
20260519114355  2026_05_19_align_public_user_id_with_auth        <-- step 1's role-type swap must respect this FK
20260519120438  2026_05_19_drop_old_commit_batch_overload
20260519120722  2026_05_19_commit_batch_inject_pk_uuid
20260519120911  2026_05_19_commit_batch_inject_timestamps_active
20260520112318  2026_05_20_licences_commit_path_and_drop_4arg_overload   <-- tonight's add
```

---

## Goal

Stand up the unified identity layer specified in [IDENTITY-MODEL.md](./IDENTITY-MODEL.md). After Phase 1.F:

- `eq-canonical.users` carries a 5-tier `eq_role` enum + `is_platform_admin` boolean.
- The shell session payload + signed cookie carry both fields.
- `SessionContext` exposes them via `useSession()`.
- A new `useCan()` hook + `<Gate>` component read a static, in-code permission matrix.
- A new `mint-supabase-jwt` endpoint issues short-lived Supabase JWTs carrying `app_metadata.tenant_id` + `app_metadata.eq_role` + `app_metadata.is_platform_admin`. RLS on `eq-canonical` reads from these.
- An admin can invite a user with a chosen role + module entitlements, the user lands via an emailed "set your PIN" link, and signs in with role pre-pinned.
- An admin can edit a user's role + entitlements later.
- EQ Field iframe handoff (`mint-iframe-token`) carries the new role information through to Field; Field's existing 2-tier system becomes a derived view.
- Intake reads the new session shape natively and uses the Supabase JWT for any RLS-gated calls.

After Phase 1.F:

- Phase 2 (Tender Pipeline import) resumes — its first PR plugs into `useCan()` from day one.
- Cards Unit 4 (Flutter flip to canonical, see [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md)) unblocks — the Flutter app consumes `mint-supabase-jwt` for all canonical reads/writes.
- Every future module follows the convention in [IDENTITY-MODEL.md §10](./IDENTITY-MODEL.md#10-hard-rules--checklist-for-any-new-module).

## Out of scope

Explicitly **not** in Phase 1.F:

- Multi-tenant user membership (one user → multiple tenants). [IDENTITY-MODEL.md §11.2](./IDENTITY-MODEL.md#11-open-questions-to-settle-before-implementation) — decide before implementation but the answer is almost certainly "no, one tenant per user" for v1.
- Password / MFA replacement of PIN. PIN stays for v1; revisit in [§11.1](./IDENTITY-MODEL.md#11-open-questions-to-settle-before-implementation).
- Self-service password / PIN reset flow (admin-driven only in v1).
- Audit log of permission decisions.
- Adoption of Supabase's `auth.users` table or any GoTrue-managed auth surface. We mint our own JWTs (see [IDENTITY-MODEL.md §9](./IDENTITY-MODEL.md#9-what-this-model-is-not)).

## Pre-flight decisions (block start)

Before any code lands, settle the five open questions in [IDENTITY-MODEL.md §11](./IDENTITY-MODEL.md#11-open-questions-to-settle-before-implementation). The plan below assumes:

- PIN auth stays (bcrypt-hashed, same as today).
- One user belongs to one tenant.
- 5 tiers are the right number for v1.
- "Set your PIN" landing page only asks for PIN; display name comes from the invite payload, editable by admin later.
- Supabase JWT TTL is 15 minutes, refreshable on demand via the shell session cookie. Cards (offline-tolerant) confirms this works for its use case before Step 4.

If any of those assumptions change, the relevant step below changes accordingly.

---

## Sequence

Each numbered group is a self-contained PR. They merge in order. No step skips the spec.

### 1. Migration — eq-canonical schema

**One PR. One Supabase migration.**

```sql
-- 2026_05_XX_phase_1f_unified_identity.sql

-- 1a. The enum.
do $$
begin
  if not exists (select 1 from pg_type where typname = 'eq_role') then
    create type public.eq_role as enum (
      'manager', 'supervisor', 'employee', 'apprentice', 'labour_hire'
    );
  end if;
end $$;

-- 1b. Move users.role from text to enum.
-- Reseed the single existing 'admin' row to 'manager' before the type swap.
update public.users
  set role = 'manager'
  where role = 'admin';

alter table public.users
  alter column role type public.eq_role using role::public.eq_role,
  alter column role set default 'employee',
  alter column role set not null;

-- 1c. Platform admin boolean.
alter table public.users
  add column if not exists is_platform_admin boolean not null default false;

update public.users
  set is_platform_admin = true
  where email = 'dev@eq.solutions';

-- 1d. Invite scaffolding.
create table if not exists public.user_invites (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references public.tenants(id) on delete cascade,
  email text not null,
  role public.eq_role not null,
  entitlements text[] not null default '{}',  -- list of module slugs to enable
  invited_by uuid references public.users(id),
  invite_token_hash text not null,            -- bcrypt-hashed one-time token
  expires_at timestamptz not null,
  accepted_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists user_invites_tenant_email on public.user_invites (tenant_id, email);
create index if not exists user_invites_token on public.user_invites (invite_token_hash);
```

**Verify:** `select role, is_platform_admin from public.users where email = 'dev@eq.solutions'` returns `('manager', true)`. `\d+ public.users` shows `role` as `eq_role` not `text`.

**Additionally required as of 2026-05-20** (see Context update at top): rewrite all canonical RLS policies + RPC tenant-checks from `user_metadata.tenant_id` to `app_metadata.tenant_id`. Scope:

- 13 entity tables: `staff`, `sites`, `assets`, `swms`, `schedule_entries`, `prestart_checks`, `jsa_records`, `toolbox_talks`, `incidents`, `itp_records`, `customers`, `contacts`, `licences`
- Intake spine: `eq_intake_templates`, `eq_intake_events`, `eq_intake_row_audit`, `eq_export_events`, `eq_export_profiles`
- Functions: `eq_intake_commit_batch`, `eq_intake_find_template_by_signature`, `eq_intake_rollback`

Pattern (per IDENTITY-MODEL.md §6.2): replace `auth.jwt() -> 'user_metadata' ->> 'tenant_id'` with `auth.jwt() -> 'app_metadata' ->> 'tenant_id'` everywhere. Use `CREATE OR REPLACE POLICY` (drop-then-recreate, idempotent — Postgres has no `CREATE POLICY IF NOT EXISTS`).

**Sweep verification:** after Step 1 applies, `mcp__<supabase>__get_advisors` security run returns `<5` results (the by-design SECURITY DEFINER + leaked-password-protection warnings remain; everything else clears).

**Rollback path:** keep the migration reversible until the bridges in steps 4 + 5 ship — if either Field's HMAC handoff or Cards' JWT consumption breaks against the new role, we need to be able to revert the type swap. Rollback also reverts the user_metadata→app_metadata sweep (i.e. all RLS policies recreated with the old claim path).

### 2. Session payload + cookie

Files touched:
- `netlify/functions/shell-login.ts`
- `netlify/functions/verify-shell-session.ts`
- `netlify/functions/_shared/token.ts` (signSessionToken signature)
- `netlify/functions/_shared/supabase.ts` (`CanonicalUser` type)

Changes:
- `CanonicalUser.role` typed as `EqRole`; add `is_platform_admin: boolean`.
- `signSessionToken` payload extended to `{ user_id, tenant_id, role, is_platform_admin, exp }`.
- `verify-shell-session` returns `role` + `is_platform_admin` in the response body (currently they're returned implicitly via the user object, but we want explicit top-level fields too so the React shell can grab them without re-flattening).
- `shell-login` returns the same shape post-login.

**Verify:** sign in as `dev@eq.solutions`, inspect the decoded cookie payload — `role: 'manager', is_platform_admin: true` present.

**No client changes in this PR.** The shell ignores the new fields until step 3.

### 3. SessionContext + useCan + Gate

Files touched:
- `src/session.ts`
- New: `src/permissions.ts`
- New: `src/permissions/Gate.tsx`
- New: `src/permissions/matrix.ts` (composes per-module exports)

Changes:
- `User` type gets `role: EqRole` + `is_platform_admin: boolean` (rename `role: string` to the literal union).
- New `EqRole` type, `PermKey` type (string literal union derived from the master matrix).
- `useCan(perm: PermKey): boolean` hook — reads role + platform_admin from `SessionContext`, returns boolean. Short-circuits to true when `is_platform_admin`.
- `<Gate perm="...">` component — renders children when `useCan()` is true, optional `fallback` prop.
- `src/permissions/matrix.ts` exports `MATRIX: Record<EqRole, Set<PermKey>>` composed at import-time from each module's `permissions.ts` (initially empty — modules contribute in later PRs).

Convention is enforced at the type level. A typo in a perm key fails to compile because `PermKey` is a closed union over the master matrix.

**Verify:** unit test — `useCan('any_known_key')` returns true for a platform admin regardless of role's matrix entry; returns matrix lookup for non-platform-admin users.

### 4. Supabase JWT minter

**This is the new step that unblocks Cards.** See [IDENTITY-MODEL.md §6.2 + §7.2](./IDENTITY-MODEL.md#62-the-supabase-jwt-for-modules-that-talk-to-supabase-directly).

Files touched:
- New: `netlify/functions/mint-supabase-jwt.ts`
- `netlify/functions/_shared/token.ts` — add `signSupabaseJwt(payload, ttlMs)` using the canonical project's JWT secret.
- New: `src/lib/supabaseJwt.ts` — client-side helper to fetch + cache + refresh the JWT.
- New env var on the eq-shell Netlify project: `SUPABASE_JWT_SECRET` — the JWT secret from the eq-canonical Supabase project settings. Must NOT be confused with `SUPABASE_SERVICE_ROLE_KEY`.

`mint-supabase-jwt.ts` semantics:
- Requires a valid `eq_shell_session` cookie.
- Returns `{ token: string, exp: number }` where `token` is a Supabase-compatible JWT signed with `SUPABASE_JWT_SECRET` (HS256).
- Payload:
  ```ts
  {
    sub: session.user_id,
    aud: 'authenticated',
    role: 'authenticated',  // Postgres role slot — NOT the EQ tier
    app_metadata: {
      tenant_id: session.tenant_id,
      eq_role: session.role,
      is_platform_admin: session.is_platform_admin
    },
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor((Date.now() + ttlMs) / 1000)
  }
  ```
- Default TTL: 15 minutes. Override via query param `?ttl=300` (max 900s) for shorter-lived tokens.

Client helper (`src/lib/supabaseJwt.ts`):
- Cached token in memory with expiry timestamp.
- `getSupabaseJwt(): Promise<string>` — returns cached token if `exp - now > 60s`, otherwise refetches.
- `createSupabaseClient()` — returns a `@supabase/supabase-js` client wired with the JWT as the access token, refreshing transparently via a global `fetch` interceptor.

**Cards-side consumption** (out of scope for this PR, lives on Cards' branch): the Flutter app receives the JWT via iframe URL hash on first load, stores it in `flutter_secure_storage`, and refreshes via a postMessage bridge that calls `mint-supabase-jwt` from within the shell. See [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) Unit 4.

**Verify:**
- `POST /.netlify/functions/mint-supabase-jwt` with `dev@eq.solutions` cookie returns a JWT whose decoded payload contains the expected `app_metadata` fields.
- The JWT works against a Supabase Postgres call that uses an RLS policy reading `auth.jwt() ->> 'app_metadata' ->> 'tenant_id'`. Land a smoke-test SQL function for this — `select_my_tenant()` returning the JWT-derived tenant_id — verify it matches `dcb71d03-858d-488a-b8e6-b76b404d25d6` for `dev@eq.solutions`.
- Confused-deputy check: a JWT minted for tenant A cannot SELECT rows from tenant B (forge a JWT manually, confirm RLS blocks).

### 5. EQ Field iframe bridge

File touched: `netlify/functions/mint-iframe-token.ts`.

Changes:
- The 60-second HMAC payload extends from `{ kind, name, role: 'staff' | 'supervisor', exp }` to `{ kind, name, role: 'staff' | 'supervisor', eq_role: EqRole, is_platform_admin: boolean, exp }`.
- The `staff | supervisor` field stays for backward compatibility with Field's current `verify-shell-token` handler (no Field-side change required to ship this PR).
- Mapping rule from [IDENTITY-MODEL.md §7.1](./IDENTITY-MODEL.md#71-eq-field-iframe--hmac-handoff):
  - `manager` OR `is_platform_admin = true` → Field role `supervisor`
  - `supervisor` → Field role `supervisor`
  - `employee` / `apprentice` / `labour_hire` → Field role `staff`

**Follow-up PR on `eq-field-app` (separate repo, not blocking this phase but tracked here):** Field's `verify-pin` handler starts reading `eq_role` from the shell token and storing it in Field's session, so Field's UI can begin honouring the finer-grained tiers ahead of decommissioning. Filed as a tracking item, not a blocker for Phase 1.F merge.

**Verify:** `POST /.netlify/functions/mint-iframe-token` with `dev@eq.solutions` cookie returns a token whose decoded payload contains `eq_role: 'manager', is_platform_admin: true, role: 'supervisor'`.

### 6. Admin: invite user

Files touched:
- New: `netlify/functions/invite-user.ts` — admin-only endpoint, posts an invite, sends email, writes `user_invites` row.
- New: `netlify/functions/accept-invite.ts` — landing-page endpoint, verifies token, creates `users` row, signs them in.
- New: `src/pages/AdminInviteUser.tsx` — admin UI form.
- New: `src/pages/AcceptInvite.tsx` — public "set your PIN" landing page.
- `src/App.tsx` — register new routes (`/<tenant>/admin/users/invite`, `/accept-invite`).

`invite-user.ts` semantics:
- Caller must have `useCan('admin.invite_user')` — gated server-side too via session role check.
- Body: `{ email, role, entitlements: string[] }`.
- Writes `user_invites` row, sends email via the same provider EQ Field uses for `send-email.js`, returns `{ ok: true }`.

`accept-invite.ts` semantics:
- Body: `{ invite_token, pin }`.
- Verifies invite_token_hash matches and `expires_at > now()`.
- Creates `users` row with the invite's role + entitlements, bcrypt-hashes pin, marks invite `accepted_at`.
- Sets `eq_shell_session` cookie and redirects to `/<tenant>/`.

**Verify:** end-to-end — admin invites `test@example.com` as `employee` with `field` + `intake` entitlements → email arrives → click link → set PIN → land on tenant home with the correct role and modules visible.

**Permission key contributed:** `admin.invite_user` (manager + platform_admin only).

### 7. Admin: edit / deactivate user

Files touched:
- New: `netlify/functions/edit-user.ts` — admin-only, mutates role / entitlements / active flag.
- New: `src/pages/AdminUserList.tsx` — list of users in this tenant.
- New: `src/pages/AdminEditUser.tsx` — edit form.
- `src/App.tsx` — routes.

**Permission keys contributed:** `admin.edit_user`, `admin.deactivate_user` (manager + platform_admin).

**Verify:** admin demotes a `supervisor` to `employee`, target user signs out and back in, lands without supervisor perms.

### 8. Intake module bridge

File touched: `src/modules/intake/*` — wherever Intake currently reads session.

Changes:
- Replace any local "is this user an admin" check with `useCan('intake.<verb>')`.
- New `src/modules/intake/permissions.ts` declaring the module's perm keys against the 5-tier matrix.
- Intake's Supabase calls that require RLS use the `createSupabaseClient()` helper from step 4 instead of the service-role client.

Tender Pipeline (`src/modules/tender-pipeline/`) and Cards (`src/modules/cards/`, currently the iframe-embed work) get the same treatment **on their own branches** — not in 1.F.

**Verify:** browser smoke test with the `core` tenant. Manager (Royce) sees all Intake actions. Hypothetically demote to `employee` and confirm `intake.import` is gated off. Restore.

### 9. Documentation pass

- `README.md` — phase plan table gets a "1.F — Unified Identity" row. Auth contract section gets a "carries role + is_platform_admin" addendum and a new row for `mint-supabase-jwt`.
- `IDENTITY-MODEL.md` (this repo) — version bumped from v1 (draft) to v1 (live). Section 11 open questions resolved or moved to v2 backlog.

## Risk register

- **Field role mapping wrong.** If the staff↔supervisor derivation in step 5 doesn't match what Field actually expects, the iframe handshake silently downgrades or breaks. Mitigation: smoke test the full `dev@eq.solutions` → Field handoff before merging step 5. Keep step 1 reversible until step 5 is green.
- **JWT secret mishandling.** `SUPABASE_JWT_SECRET` is the keys-to-the-kingdom for anyone who can forge `app_metadata`. Treat it like the service-role key: Netlify env var only, never committed, never logged. Rotation strategy: rotate JWT secret on Supabase project settings, redeploy shell, all outstanding JWTs invalidate (acceptable — they're 15-min TTL anyway).
- **JWT TTL mismatch with offline-tolerant clients.** Cards' Flutter app on a tradie's phone with patchy signal might fail to refresh a 15-min JWT before expiry, locking the user out mid-task. Mitigation: Cards-side caching of last-known-good JWT + graceful degradation to "I'll sync when you're back online" — designed into Cards' Unit 4, not this phase. If Cards reports the 15-min TTL is too short during integration, extend to 60 min and document the trade.
- **Confused-deputy via forged JWT.** Anyone who gets `SUPABASE_JWT_SECRET` can mint a JWT for any tenant. Mitigation: same as above (treat as service-role-equivalent); RLS policies must also check `app_metadata.tenant_id` matches the row's `tenant_id` on every read/write, not just trust the JWT subject.
- **Module declares wrong perm keys.** Per-module permissions.ts gives every module a foot-gun. Mitigation: the master matrix type is a closed union, so typos fail to compile. Code review checks against [IDENTITY-MODEL.md §4.2](./IDENTITY-MODEL.md#42-permission-keys) naming.
- **Module ships without declaring permissions.** A new module (Cards, Quotes, Service, Tender Pipeline, etc.) might land its first user-facing PR without a `src/modules/<module>/permissions.ts` file — making its UI ungated and any `useCan('cards.foo')` call a compile error. Mitigation: PR template / reviewer checklist line — *"if this PR adds a gated screen, does the module's `permissions.ts` declare the relevant key against all 5 tiers?"* Applied especially carefully when Cards/Quotes/Service/Tender Pipeline ship their first PRs.
- **Invite email deliverability.** Same provider as Field's send-email function; risk is shared but tractable. Mitigation: log the invite token server-side during the first week of use so a stuck invite can be hand-delivered.
- **Session payload size.** Cookie grows from ~150 bytes to ~250 bytes with role + boolean + entitlements list. Well under any browser limit, but worth noting. The Supabase JWT is separate (lives in client memory / `flutter_secure_storage`, not in a cookie).
- **Phase 2 + Cards rebase cost.** `claude/phase-2-import-screen` and `claude/cards-iframe-embed` will both need rebasing onto `main` after 1.F. Both are small branches so the cost is contained, but the longer 1.F takes, the wider the gap. Mitigation: don't extend 1.F scope mid-flight — keep the open questions in §11 tightly scoped.

## Effort estimate

Rough sizing, each step measured as solo developer with no surprises:

| Step | Estimate |
|---|---|
| 1. Migration | 0.5d |
| 2. Session payload | 0.5d |
| 3. SessionContext + useCan + Gate | 1d |
| 4. Supabase JWT minter | 1.5d (server + client helper + RLS smoke test) |
| 5. Field iframe bridge | 0.5d (+ a follow-up Field-side PR not included here) |
| 6. Admin invite flow | 2d (server + landing + email wiring) |
| 7. Admin edit / deactivate | 1d |
| 8. Intake bridge | 0.5d |
| 9. Documentation pass | 0.5d |
| **Total** | **~8d focused work** |

Pre-flight decisions add ~0.5d if any of the five §11 questions need real exploration.

## Definition of done

- All 9 steps merged to `main`.
- `dev@eq.solutions` logs into `core.eq.solutions`, sees role `manager` + platform admin in the session payload.
- A second invited user can complete the invite flow end-to-end, sign in, and have the correct role + entitlements applied.
- `mint-supabase-jwt` returns a valid Supabase JWT; a smoke-test RLS policy on `eq-canonical` correctly scopes rows by `app_metadata.tenant_id`.
- `mcp__<supabase>__get_advisors security` on `eq-canonical` returns fewer than 5 results — the 28 `rls_references_user_metadata` ERROR warnings present pre-1.F all cleared.
- EQ Field iframe handoff still works (regression check on the `core` tenant).
- Intake module gates one action via `useCan()` and at least one Supabase call via the minted JWT.
- `core` tenant has `module_entitlements` rows for every module that's currently mounted in the shell (`field`, `intake`, `cards`, `tender`, anything else live). Documented in the migration verification step.
- `IDENTITY-MODEL.md` version is live (not draft).
- Phase 2 (Tender Pipeline) branch and Cards iframe embed branch are both rebased onto `main` and ready to resume with `useCan('<module>.*')` calls and the JWT helper in place of any prior admin-only assumptions.

---

**Related:**
- [IDENTITY-MODEL.md](./IDENTITY-MODEL.md) — the spec this plan implements
- [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) — Cards is the first external consumer of `mint-supabase-jwt`
- [eq/field/multi-tenancy/plan.md](../field/multi-tenancy/plan.md) — original 5-tier system design (now superseded by IDENTITY-MODEL.md as the cross-product spec)

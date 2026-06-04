---
title: EQ Field ↔ EQ Shell — identity & security-groups tie-in
owner: Royce Milmlow
last_updated: 2026-06-05
scope: How Field consumes Shell identity today, and the target for tying Field permissions into Shell security groups
read_priority: high
status: live (verified against running code + DB 2026-06-05)
---

# EQ Field ↔ EQ Shell — security tie-in

> Verified against the running code and `shell_control` DB on 2026-06-05. This
> **supersedes** the "Field doesn't consume the shell token yet / Phase 1.F not
> started" wording in `eq/identity/*` — that is **stale**. The role handoff
> shipped (Field v3.5.22/.23) and is live.

## 1. What's actually wired today (verified)

**Identity / role handoff — LIVE.** When Field is embedded in Shell:
- `scripts/auth.js` runs `_consumeShellToken()` / `_consumeShellCookie()` on boot.
- `netlify/functions/verify-pin.js` has live `verify-shell-token` and
  `verify-shell-cookie` actions. They map Shell's 5-tier `eq_role` →
  Field's binary role via `FIELD_DISPATCH_ROLES = {manager, supervisor}`:
  `manager`/`supervisor` (or `is_platform_admin`) → Field **supervisor**;
  `employee`/`apprentice`/`labour_hire` → Field **staff**.
- A `supervisor` result sets `sessionStorage.eq_auto_admin='1'`, and
  `index.html:5586` flips `isManager=true` on boot (auto-unlock + toast).

**Shell side.** `mint-iframe-token.ts` signs a 60-second HMAC `shell-token`
(`{ kind, name, role, eq_role, is_platform_admin, tenant_slug, exp }`) with
`EQ_SECRET_SALT`. Phase-2 path (`token-exchange.ts`) signs a 60s Supabase JWT
carrying `app_metadata.{tenant_id, eq_role, is_platform_admin}`. Field's
`verify-shell-token` auto-detects 2-part HMAC vs 3-part JWT.

**Field's permission engine — already exists.** `scripts/permission-matrix.js`
defines `window.EQ_PERMISSIONS` (a role → permission-key matrix), and
`scripts/permissions.js` exposes `EQ_PERMS.can(permKey)` which checks the
current role's allow-list. Role resolution: PIN-unlock / `eq_auto_admin` /
`EQ_SESSION.role` (PIN-unlock-wins).

## 2. Salt dependency (the live "view only" failure mode)

The HMAC handoff requires **`EQ_SECRET_SALT` to be byte-identical on the
eq-shell and eq-solves-field Netlify deploys** (the `iframe_salt_registry` row
confirms the value lives in env, not the DB). **Shell verifies with
`EQ_SECRET_SALT` + a rotation fallback `EQ_SECRET_SALT_NEXT`; Field's
`verify-pin` checks only `EQ_SECRET_SALT`** — so any salt rotation silently
breaks every Shell→Field token → Field falls back to view-only.

Observed 2026-06-05: `royce@eq.solutions` is `manager` of `core` +
`is_platform_admin=true` (→ should be Field supervisor) yet landed view-only in
embedded Field. Role is ruled out; this is token rejection — almost certainly
`EQ_SECRET_SALT` drift between the two deploys. **Fixes:** (a) re-sync the salt
across both Netlify sites, and (b) teach Field's `verify-pin` to also accept
`EQ_SECRET_SALT_NEXT` (mirror Shell) so rotation is zero-downtime.

## 3. The gap — security GROUPS are not tied in

Shell models fine-grained access as **security groups**
(`shell_control.security_groups` / `user_security_groups` /
`security_group_perms` → an `extra_perms[]` bundle on the session, refreshed
every ~5 min). **These are NOT transmitted to Field** — the handoff token
carries role only. Field therefore honours the coarse 5-tier role (collapsed to
supervisor/staff) and has **no knowledge of Shell groups**.

**Namespaces are disjoint today:**
- Shell `perm_key`s in use: `admin.edit_user`, `admin.list_users`,
  `admin.review_cards`, `audit.view`, `equipment.edit`, `equipment.view`,
  `reports.view`.
- Field `can()` keys: `roster.*`, `ts.*`, `ph.*`, `leave.*`, `people.*`,
  `sites.*`, `app.*`, `reports.*`, `admin.*` (see `permission-matrix.js`).

So a Shell group cannot currently grant a Field capability — there is no shared
vocabulary, and the bundle never reaches Field.

## 4. Target — additive `extra_perms` bridge (generic, no hardcoded mapping)

The mechanism is namespace-agnostic and additive, so it ships safely before the
vocabulary is fully agreed:

1. **Shell** — `mint-iframe-token` (and the Phase-2 JWT) include the user's
   `extra_perms: string[]` (already computed Shell-side as `session.extra_perms`
   via `getUserSecurityGroupPerms`). The HMAC token gains a `perms` field; the
   JWT gains `app_metadata.extra_perms`.
2. **Field** — `verify-shell-token` / `verify-shell-cookie` pass `extra_perms`
   through into the returned session; `auth.js` stores them on
   `window.EQ_SESSION.extra_perms`.
3. **Field** — `EQ_PERMS.can(key)` returns true if `key` is in the role matrix
   **OR** in `EQ_SESSION.extra_perms`. (Grant-only / additive — groups can widen
   access, never narrow it. Role stays the floor.)

This makes "Field gates by Shell security groups" true **as data**: assign a
group a Field permission key, add a user, and that user gains the capability in
Field — no code change per capability.

### Vocabulary decision (the one product call)
For groups to gate Field features, Shell groups must carry **Field-namespace
keys** (e.g. `roster.edit_team`, `leave.approve`, `ts.approve`). Recommended:
adopt Field's `permission-matrix.js` keys as the canonical capability vocabulary
and expose them as assignable perms in Shell's security-group admin. Shell's
generic keys (`equipment.*`, `reports.view`) stay for Shell/other apps. A small
namespace prefix (`field.`) is optional but not required — additive `can()`
matches on exact key.

## 5. Sequencing
1. **Fix the handoff first** (salt re-sync + Field `EQ_SECRET_SALT_NEXT`) — until
   tokens are accepted, nothing below is observable.
2. **Field-side bridge** (additive `can()` + pass-through) — safe no-op until
   Shell sends `extra_perms`.
3. **Shell-side** — add `extra_perms` to `mint-iframe-token` + the Phase-2 JWT.
   Coordinate with the active identity-convergence work in this repo.
4. **Vocabulary** — seed Field-namespace keys into Shell's assignable-perm
   catalog; build out groups (e.g. "Roster editors", "Leave approvers").
5. **Longer term** (accepted identity-convergence target, 2026-06-04): single
   identity in `shell_control.users`; retire Field's standalone PIN gate for
   shell-embedded use (keep PIN only for no-shell/standalone access).

## 6. Status
- Role handoff: **live** (salt-gated — see §2).
- `extra_perms` bridge: **design accepted; build starting** (Field-side PR +
  Shell-side PR). Not deployed.
- View-only root cause: **token rejection, salt drift the prime suspect** —
  confirm via the embedded-Field console (`EQ[auth] shell-token …` log) or a
  Netlify env parity check.

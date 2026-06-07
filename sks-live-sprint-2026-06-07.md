---
title: SKS Live — Roles / Security-Groups Sprint
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Handoff + agent prompts for the roles/security-groups track of SKS Live
read_priority: reference
status: live
---

# SKS Live — Roles / Security-Groups Sprint (handoff + agent prompts)

**Prepared:** 2026-06-07
**Track:** App-layer roles + security groups for the first real SKS user.
**Sibling track (do not conflate):** [SKS-CUTOVER-CRITICAL-PATH.md](SKS-CUTOVER-CRITICAL-PATH.md) — the Field *schema + live-data* migration (Phases A–E). This file and the cutover plan are **parallel workstreams** toward "SKS live," not the same plan.

> Security groups stay **APP-LAYER** (locked decision). RLS in the data plane only reads `app_metadata.tenant_id`; group perms flow through the Shell **session** as `extra_perms`, not through the Supabase JWT. See [eq/field/permissions/field-shell-security-groups-2026-06-05.md](eq/field/permissions/field-shell-security-groups-2026-06-05.md).

---

## Verification log (live Supabase, 2026-06-07)

Project refs and load-bearing table/row claims confirmed against the running systems before this file was made canonical (per CLAUDE.md Rule 0.5 / §7).

| Project | Ref | Role |
|---|---|---|
| eq-canonical | `jvknxcmbtrfnxfrwfimn` | Control plane — `shell_control` schema |
| sks-canonical | `ehowgjardagevnrluult` | SKS data plane |
| eq-canonical-internal | `zaapmfdkgedqupfjtchl` | EQ server-only tenant data (`zaap`) |
| sks-labour (SKS LIVE) | `nspbmirochztcjijmcrx` | Legacy SKS labour app — **do not touch without "SKS live"** |

**Confirmed:**
- `shell_control` holds `security_groups`, `security_group_perms`, `user_security_groups`, `audit_log`, `module_entitlements`, `user_tenant_memberships`, `tenants`.
- `security_groups` = **9**; `security_group_perms` = **16**; `user_security_groups` = **0** rows (no assignments yet).
- `user_security_groups` columns: `user_id uuid`, `group_id uuid`, `assigned_by uuid`, `assigned_at timestamptz` — the admin write (Phase 3) must populate `assigned_by`/`assigned_at` for the audit trail.
- Tenant `sks` ("SKS Technologies") has **3 members, all `role = manager`**.
- `app_data.contact_customer_links` @ sks-canonical: policy `ccl_tenant` (cmd=ALL) has `with_check = null`; USING qual casts to `::uuid`. (A second `ccl_tenant_read` SELECT policy also exists — SELECT policies don't use WITH CHECK.)

**NOT verified here (GitHub-side, outside Supabase scope) — treat as leads, verify before acting:**
- eq-roles **PR #7** / branch `claude/gallant-cartwright-847187`, "v2.3.0 resolver, 91 tests."
- eq-shell branch divergence (`claude/c2-shell-roles` ~+197, `claude/sks-field-host` ~+59) and which commits are load-bearing.

---

## Quick guide — repos & actions

| # | Repo | Branch / PR | State | Action | Owner |
|---|---|---|---|---|---|
| 1 | **eq-roles** | PR #7 (`claude/gallant-cartwright-847187`) | v2.3.0 resolver, 91 tests | Merge PR #7 → tag `v2.3.0` | Royce |
| 2 | **eq-shell** | `sks-field-host` + `c2-shell-roles` | Roles split across 2 divergent branches | Converge → name one trunk | Royce + agent |
| 3 | **eq-shell** | (trunk from #2) | Groups never reach the session | Phase 2 — wire `extra_perms` into session | Agent |
| 4 | **eq-shell** | (same trunk) | No assign-to-group UI | Phase 3 — `AdminSecurityGroups` page | Agent |
| 5 | **eq-shell + DBs** | — | First real SKS user not walked | Phase 4 — go-live E2E | Royce + agent |
| 6 | **sks-canonical + eq-roles** | — | 2 hardening gaps | Phase 5 — `WITH CHECK` + policy-lint | Agent |

Royce's hands-on bits: **#1 (merge + tag)** and the **decision in #2** (which trunk). Everything else is an agent session with the prompts below.

**Golden rules baked into every prompt:** start the session *in that repo* (loads its CLAUDE.md, clean git); no deploy without Royce's explicit word; auth-path changes need Royce's approval before deploy.

---

## Order of operations

1. **Royce:** merge PR #7, tag `v2.3.0`. *(unblocks the dep bump)*
2. **Converge eq-shell** (Prompt A) → Royce picks the trunk.
3. **Phase 2** session wiring (Prompt B).
4. **Phase 3** admin UI (Prompt C) — can run alongside B.
5. **Phase 4** SKS go-live walk (Prompt D).
6. **Phase 5** hardening (Prompt E) — anytime after Phase 0, independent.

---

## Prompt A — Converge the eq-shell roles branches

*Run in `C:\Projects\eq-shell`.*

```
We need to converge two divergent eq-shell branches into one trunk for the
"SKS Live" roles sprint, WITHOUT forking a third version or losing work.

State (verify live before acting — branches/worktrees move):
- claude/c2-shell-roles  : ~197 ahead of main. Wired @eq-solutions/roles as the
  canonical EqRole source. Has NO resolver / extra_perms / security_group code.
  Roles dep pinned to #main.
- claude/sks-field-host  : primary checkout, dirty + active, ~59 ahead. This is
  where the groups infra actually lives: netlify/functions/security-groups.ts,
  _shared/permissions.ts (Principal.extra_perms + can()), the Admin*.tsx pages,
  mint-supabase-jwt.ts.

Do NOT blindly merge. First: map the divergence (git log/diff both vs origin/main),
identify which commits are load-bearing for roles/auth/groups, and check whether
either branch's owner has uncommitted work in flight. Then PROPOSE a convergence
strategy (which branch becomes trunk, what to cherry-pick/rebase, conflict risks)
and STOP for my decision before executing. No deploy.
```

## Prompt B — Phase 2: wire group perms into the session

*Run in `C:\Projects\eq-shell` on the trunk from Prompt A.*

```
Phase 2 of the SKS Live sprint. Goal: a user's security-group perms become real
in the app by flowing into the Shell SESSION as extra_perms.

Context (verified):
- @eq-solutions/roles v2.3.0 ships resolveEffectivePermissions({role, groupPerms?,
  isPlatformAdmin?, revokes?}) -> readonly PermKey[]. It's in the runtime-safe
  roles.js, so Netlify functions can import it. Bump this repo's dep from its
  current pin to github:eq-solutions/eq-roles#v2.3.0.
- TARGET IS THE SESSION COOKIE, NOT mint-supabase-jwt.ts. That mint is the
  data-plane Supabase JWT and RLS only reads app_metadata.tenant_id; per the
  locked decision, security groups stay APP-LAYER. _shared/permissions.ts can()
  already checks Principal.extra_perms BEFORE the role matrix — so extra_perms
  just needs to be populated where the session/Principal is built.
- Control plane = shell_control @ eq-canonical (jvknxcmbtrfnxfrwfimn). Tables:
  user_security_groups (user_id, group_id, assigned_by, assigned_at),
  security_groups, security_group_perms.

Work:
1. At login / session-mint (trace where the eq_shell_session cookie + Principal
   are created — likely shell-login*.ts / _shared/token.ts), query the user's
   user_security_groups -> security_group_perms -> union of PermKeys.
2. Call resolveEffectivePermissions(role, groupPerms) and store the result as
   extra_perms in the session.
3. Confirm _shared/permissions.ts can() honours it end-to-end. Add a test.
4. Retire or re-point the local roles-matrix.ts mirror + check-perm-sync.mjs at
   v2.3.0 (don't leave a stale hand-copy — that's the prior-outage mechanism).

No deploy. Stage on a branch and open a PR.
```

## Prompt C — Phase 3: AdminSecurityGroups page

*Run in `C:\Projects\eq-shell` on the same trunk.*

```
Phase 3 of the SKS Live sprint. Build the missing admin screen that lets a
manager assign users to security groups — the thing that finally moves
shell_control.user_security_groups off 0 rows.

Context (verified):
- Backend already exists: netlify/functions/security-groups.ts. Tables in
  shell_control @ eq-canonical: security_groups, security_group_perms,
  user_security_groups (user_id, group_id, assigned_by, assigned_at). 9 groups
  exist; 0 user assignments. Populate assigned_by + assigned_at on every write.
- Existing admin pages to match for style/auth: src/pages/AdminUserList.tsx,
  AdminEditUser.tsx, AdminTenantSettings.tsx.
- Gate the page behind the admin.manage_groups permission.

Work: new src/pages/AdminSecurityGroups.tsx — list/create groups, show their
perms (use labelFor() for plain-English names from @eq-solutions/roles), and
add/remove user membership. Write every change to shell_control.audit_log. Add a
"see-as" preview that runs resolveEffectivePermissions for a selected user.

No deploy. Branch + PR.
```

## Prompt D — Phase 4: walk one real SKS user live

*Run in `C:\Projects\eq-shell` after B+C merge.*

```
Phase 4 of SKS Live: prove the whole chain for ONE real SKS user, end to end.
SKS tenant routes to sks-canonical (ehowgjardagevnrluult); control plane is
shell_control @ eq-canonical (jvknxcmbtrfnxfrwfimn). SKS's 3 live members are all
role=manager.

Walk and confirm: invite/login -> correct 5-tier role in the session -> only
entitled apps show (module_entitlements) -> open Field/Service -> RLS in
sks-canonical enforces tenant isolation -> assign that user to a security group
in the new Admin UI -> after token refresh, the granted perm appears (this is the
FIRST EVER user_security_groups row). Document any gap as a fix, not a workaround.

No data-plane writes beyond the test user. No deploy.
```

## Prompt E — Phase 5: hardening (independent, anytime)

*Run in `C:\Projects\eq-context` (it spans sks-canonical + eq-roles CI).*

```
Phase 5 hardening for SKS Live. Two non-blocking items found in the Phase 0 RLS
audit of sks-canonical (ehowgjardagevnrluult):

1. app_data.contact_customer_links has an ALL policy (ccl_tenant) with
   with_check=null. It's currently safe (Postgres falls back to the tenant_id
   USING qual), but add an explicit WITH CHECK for clarity + future-proofing.
   IMPORTANT: match the existing USING qual's cast — it casts to ::uuid:
     WITH CHECK (tenant_id = ((auth.jwt()->'app_metadata'->>'tenant_id'))::uuid)
   (A plain text comparison without ::uuid will not type-match the uuid column.)
   Only the ALL policy needs it; the ccl_tenant_read SELECT policy does not use
   WITH CHECK. Migration via the tenant-migrations path.
2. Add a CI policy-lint asserting EVERY app_data table has a tenant-isolation
   policy, so a future migration can't ship a table without one.

Also (eq-roles): add a no-orphan-keys CI test — every perm key referenced in
shell_control.security_group_perms must exist in the pinned @eq-solutions/roles.

No deploy without explicit instruction.
```

---

## Cross-references

- [SKS-CUTOVER-CRITICAL-PATH.md](SKS-CUTOVER-CRITICAL-PATH.md) — the Field schema + live-data migration (parallel track).
- [eq/field/permissions/field-shell-security-groups-2026-06-05.md](eq/field/permissions/field-shell-security-groups-2026-06-05.md) — the app-layer-groups locked decision.
- [eq-platform-verified-state-2026-06-03.md](eq-platform-verified-state-2026-06-03.md) — DB-verified platform snapshot (re-verify; drifts).

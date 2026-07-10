# Access-Model Foundation Plan — decided 2026-07-08

Companion to `IDENTITY-MODEL.md`. Decisions made by Royce on Fable-tier design review.
Status: **Phase 0 complete** (eq-shell PR #704 merged `82c97cb`). **Phase 1 BUILT** (eq-roles v2.5.1 merged+tagged; eq-shell PR #715 open, all CI green, awaiting Royce's merge — auto-deploys). Phase 2 still fenced to post-cutover. Build sessions: read this, don't re-derive.

## Why (one paragraph)
The 5-role model is consistent across all apps (audited 2026-07-07/08: Shell, Field, Service, Cards, DB/JWT/RLS all canonical). The scale trap is what's layered on top: **five grant paths** (base matrix, tenant_role_overrides, free-form security groups, is_platform_admin, `org_memberships.role='admin'`) and **Cards represented four ways**. Fix now, in infancy, while migration is trivial (1 tenant, ~30 users).

## Decisions (locked, Royce 2026-07-08)
- **D1 — Manager is the top tenant role.** `is_platform_admin` stays the EQ-internal super-layer. Owner/Executive = proven one-file add-later (Phase 0 ships a scaffold test). Keep `org_memberships.role` **data** (stop gating on it; don't drop the column) so the Owner door stays open. Never rename the enum.
- **D2 — Conservative override promotion** (criterion: what scales = right defaults, not fewest overrides). Dissolve the 4 Cards-artifact overrides via D4. Promote only cross-app-safe grants (apprentice `equipment.view`; consider dropping `intake.view` from apprentice defaults, making SKS's denial moot). **Keep `service.create/close` + `quotes.approve` tenant-local** — `service.create` is overloaded (Shell tile vs Service `canWrite` asset/customer mutations); broadening it canonically would change Service behaviour suite-wide. Phase 3 splits overloaded keys, then re-tune.
- **D3 — Canonical groups only.** Group creation restricted to platform-admin. Canonical set defined in eq-roles `defaultGroups`, seeded everywhere: Equipment editors, Report viewers, **+ promote SKS's "Project Managers"** (admin.list_users, admin.edit_user, admin.review_cards, audit.view). Delete "Test - Royce". `tenant_role_overrides` mechanism stays but drains.
- **D4 — Un-smear Cards.** Cards-the-app = worker-facing, gated by tenant **entitlement** (`org_module_entitlements.cards`). Employer review = `admin.review_cards` (exists, already gates StaffPage). `cards.view`/`cards.onboard` deprecated in the matrix (dead keys until consumers confirmed clean → remove in major bump). Delete the 4 worker-cards overrides.

## Definition of Done (the 10/10 bar)
1. Every access decision goes through `can(role, perm)`. Zero role-name **enforcement** checks; lint ratchet + allowlist for display-only reads.
2. `org_memberships.role` is never an access gate.
3. One source per axis: Entitlement (tenant) · Role (person) · Permission (action) · Audience (worker vs employer).
4. Every consumer derives roles+matrix from eq-roles (incl. a `roles.dart` emit for Cards); drift-guards on every copy.
5. Adding a role = one eq-roles file — proven by a scaffold test (`executive`).
6. `why_can(user, action)` answers access questions from one grant path.

## Findings that shaped the plan (from the 2026-07-08 adversarial pass)
- **PermKeys are suite-global.** One key can gate different behaviours in different apps (`service.create`). No canonical broadening without the perm→enforcement-site inventory.
- 4 of SKS's 10 overrides are Cards-smear artifacts (workers granted `cards.onboard/view`) — dissolve, don't promote.
- `ROLE_OPTIONS` missing `manager` in the worker-approval picker is **correct by design** (not a bug — managers minted via AdminInviteUser).
- `AccessControlPage.tsx` `ROLE_DEFAULTS` is a hand-mirror of the matrix — must derive from the package **in the same PR** as any matrix change, or the admin UI lies.
- **Hidden consumer:** connection-request notification emails look up `org_memberships.role='admin'`. Phase 2 must migrate ALL readers (Cards admin UI `org_admin_provider`, licence-photos RLS on jvkn storage.objects, connection-request edge fn) to the canonical manager lookup, or notifications silently die.
- Real users are on Field **now** → pre-cutover work must be behaviour-preserving and Shell/package-only.

## Phase 0 findings (2026-07-08 enforcement-site inventory — see `enforcement-site-inventory-2026-07-08.md`)
- **Reversed the `intake.view` call**: Shell's own `src/modules/intake/permissions.ts` documents apprentice's broad `intake.view` grant as deliberate ("view by default for all... gating tightens later"), not an oversight. Left canonical alone; SKS's denial override stands as legitimate tenant-specific tightening.
- **`service.create` overload confirmed with file:line**: also gates asset/customer mutations in EQ Service's `canWrite()` (~520 usages, fully canonical, no bypass — Service itself is clean). Stays tenant-local.
- **Discovered 3 additional client-side matrix mirrors in Shell alone** (`src/permissions/matrix.ts` composing per-module files for intake/equipment/gm-reports/cards/service/field/quotes — hand-maintained, not derived from the package; plus `AccessControlPage.tsx` `ROLE_DEFAULTS`; plus `tenant-role-perms.ts` `OVERRIDABLE_PERM_KEYS`). All currently in sync (zero pre-existing drift found) but structurally can diverge — Shell's own CI (`scripts/check-perm-sync.mjs`) does an exact-match diff against the *installed* package, which is why the eq-roles version bump must land (merge + tag) before the matching eq-shell PR, not alongside it.
- **Quotes module is real and live** (`src/modules/quotes/permissions.ts`) — corrects an earlier assumption that EQ Ops/quotes was unbuilt. Already byte-identical to canonical; `quotes.approve` override stays tenant-local (no promotion evidence).
- **Cards admin flag confirmed narrow**: only 3 `org_memberships.role='admin'` rows exist (Royce + EQ Dev) — the 10 SKS managers are NOT org-admins today, confirming the two-admin split is live, not theoretical.

## Phases
**Phase 0 — Lock the model (pre-cutover-safe, additive) — ✅ COMPLETE 2026-07-08**
- **Parity harness first**: snapshot effective perms for every user on all 3 tenants (role → package matrix ∪ overrides ∪ group perms) before/after every phase. Any diff = hold. Baseline captured 2026-07-08, hash `37300a13c30ca0598bbad675dbf4eedc5245edcd5e87cecae2c833065f77eee0` (see `parity-harness/`). **"After" snapshot (post eq-shell PR) is byte-identical to baseline** — zero live users hold `apprentice` today (32 employee, 14 manager, 3 supervisor, 0 apprentice), so the one real grant change this phase made has zero live blast radius yet; it activates automatically the moment an apprentice-role user exists.
- **Perm→enforcement-site inventory** across Shell/Field/Service/Cards/RLS — done, see `enforcement-site-inventory-2026-07-08.md`.
- eq-roles: D2 tuning (apprentice→equipment.view only — intake.view left alone per the reversal above), D4 deprecation markers on cards.view/cards.onboard (new optional `deprecated` field on PermissionMeta), D3 canonical `defaultGroups` (+Project Managers), `roles.dart` emit (Dart 2.17+, verified with `dart analyze`, 0 issues), executive scaffold test. Version 2.4.0 → 2.5.0. **eq-roles PR #10 merged, tagged `v2.5.0`.** 96/96 tests green.
- eq-shell: dependency bumped to `v2.5.0`; `EQUIPMENT_MATRIX` + `default-groups.ts` mirrors updated; `AccessControlPage.tsx` `ROLE_DEFAULTS` now **derives** from the package's `MATRIX` instead of a hand-copied literal. **eq-shell PR #704 merged `82c97cb` 2026-07-10**, `check-perm-sync.mjs` green, tsc/build/116 tests clean.
- **New finding, tracked for Phase 3**: `check-perm-sync.mjs` merges the full package matrix into `clientGrants` before diffing, which makes it structurally blind to a local module file *under*-granting versus canonical (it only catches local *over*-grants, never omissions). This is why the guard didn't flag `EQUIPMENT_MATRIX.apprentice` being stale even though it clearly was — worth tightening the checker itself, not in scope for this phase.

**Phase 1 — Gate on permissions (pre-cutover, parity-gated) — ✅ BUILT 2026-07-10 (eq-shell PR #715 open, all CI green, awaiting Royce's merge)**
- **Correction to this plan's own scope**: the "~10 checks, Shell-only" estimate was wrong on both counts once verified against live code. Real count = **5 server enforcement sites** (`update-data-activation`, `get-data-activation-status`, `labour-hire-commit`/`-mutate`/`-parse`) + 1 client display mirror (`CustomersPage`). And it was **not Shell-only**: none of the 5 had a matching canonical PermKey, so **eq-roles v2.5.1** was a hard prerequisite (new `ops.view_rates`+`ops.manage_rates` — the `ops.*` "add to package" decision, resolved as ADD — and `entity.manage_activation`; all additive, each matching its hand-rolled check's grant set 1:1). `create-worker-invite`'s role check turned out to be invitee-entitlement defaulting (no `can()` equivalent), and `MobileTabBar`'s are display-only — both correctly suppressed, not converted.
- **Ratchet built**: `scripts/check-role-literals.mjs` — bans new role-name enforcement comparisons (the 6 EqRole literals only, so non-role `role` uses don't false-positive). Empirical run found 8 pre-existing legit uses (3 display, 3 `'subcontractor'`-is-a-category collisions, 1 entitlement-default, 1 employment_type→role map) — all carry a documented `eq-role-literal-ok` suppression; **zero hidden enforcement anti-patterns**, confirming the 5 were the only real server gates. Both the ratchet AND `check:perms` (previously never run in CI) are now **blocking CI steps** in `ci.yml`.
- **Parity: behaviour-preserving, verified two ways** (`parity-harness/phase1-parity-note-2026-07-10.md`): deterministic diff = exact per-role delta (managers +3 keys, supervisors +2, employees +0, nobody loses anything, every row matches expected); live check = no override/group references the new keys (base matrix is the only grant path). Hash changed (expected — live managers/supervisors exist) but no human's actual capability changed.
- **Zero Field changes. Zero Cards changes.** Confirmed.

**Phase 2 — One admin (POST-cutover, auth-touching, fenced)**
- Migrate the 3 known readers of `org_memberships.role='admin'` → canonical manager/`can()` gates (Cards `org_admin_provider`, jvkn licence-photos RLS, connection-request edge fn). Re-grep for unknowns first.
- Parity test on the 3 current admin-flag holders; keep column data.

**Phase 3 — Guardrails (post-cutover)**
- Field UI gates: convert enforcement-relevant `isManager` checks to `EQ_PERMS.can()` incrementally; Cards consumes `roles.dart` (retire `kEqRoleLabels`).
- **Split `service.create`/`service.close` by app** before ever promoting a Service-affecting grant canonically (the inventory's top Phase 3 item).
- Decide whether Shell's `ops.*` module gets a canonical home, or collapse the client-matrix architecture to derive from the package directly (closes the whole class of "3 more hidden mirrors" risk).
- Retire redundant overrides; constrain/replace free-form groups (D3); build `why_can()`; kill remaining hardcoded matrix mirrors.
- **Fix `check-perm-sync.mjs`'s blind spot**: it merges the full package matrix into `clientGrants` before diffing, so it can only ever catch a local module *over*-granting vs canonical, never *under*-granting. Found 2026-07-08 when it didn't flag a stale `EQUIPMENT_MATRIX.apprentice`.

## Standing rules
- Gate on **permissions, never role names**. Additive roles only — never rename `manager`.
- Before broadening any grant canonically: check the enforcement-site inventory. A `PermKey` used by more than one app is suite-global — verify blast radius in every consumer, not just the one you're editing.
- Auth-touching changes never land in a cutover week.
- **This file was accidentally lost once already** (2026-07-08, a concurrent session's activity in this same non-worktree checkout wiped untracked files between writes) — recreated from the authoring session's own transcript. If you're reading a version that looks stale, check `sessions/2026-07-08.md` and the eq-roles/eq-shell PR history before trusting it blindly.

# Enforcement-site inventory — 2026-07-08

Phase 0 deliverable of the [Access-Model Plan](ACCESS-MODEL-PLAN.md). Answers,
per `PermKey`: **who actually enforces this, and does the same key mean the
same thing everywhere it's checked?** This is what D2's promotion calls were
based on, and it's the seed of Phase 3's `why_can()`.

## Headline finding: PermKeys are suite-global, but not every consumer derives from the package

The canonical package (`@eq-solutions/roles`) is genuinely the source of truth
for the *server-side enforcement boundary* everywhere it's actually wired in.
But there are **three independent mirror layers** discovered this session,
none of which had been catalogued before:

1. **eq-shell's client matrix** (`src/permissions/matrix.ts`) — composes
   admin/audit perms *live* from the package (`rolesAdminAudit()` filters
   `ROLES_MATRIX`), but intake/equipment/gm-reports/cards/service/field/quotes
   are **hand-maintained local files** (`src/modules/<module>/permissions.ts`)
   that happen to match the package by convention, not by import. Plus an
   `ops.*` module with **no package equivalent at all** (`OPS_PERMS`,
   `src/permissions/matrix.ts:102`).
2. **`AccessControlPage.tsx` `ROLE_DEFAULTS`** (line ~114) — a *second*,
   independent hand-copy of the whole matrix, used only for the admin UI's
   display defaults.
3. **`netlify/functions/tenant-role-perms.ts` `OVERRIDABLE_PERM_KEYS`**
   (line 42) — a hardcoded allow-list of which keys a tenant may override.
   Deliberately excludes `admin.*`/`audit.*` (a real, good security boundary,
   not drift) — but it's a fourth place that has to be remembered whenever the
   canonical module list changes.

**Why this matters:** as of today, all of these happen to agree (spot-checked
`equipment`/`service`/`cards`/`field`/`quotes` module files against canonical
— zero pre-existing drift found). But nothing *enforces* that agreement except
one CI script (`scripts/check-perm-sync.mjs`) that does an exact-match diff
between the installed package and the client mirrors — which is why any
canonical matrix change requires the eq-shell dependency to be bumped in
lockstep, or CI fails (this gated the Phase 0 sequencing: eq-roles must merge
+ tag before the matching eq-shell PR can land, not the other way round).

## The `service.create` overload — the reason D2 stayed conservative

`service.create`/`service.close` are the same string in two apps with two
different blast radii:

- **eq-shell**: gates whether the *Service* nav tile shows a create/close
  action (`src/modules/service/permissions.ts` — `SERVICE_MATRIX`, matches
  canonical exactly: manager/supervisor get all three, employee/apprentice
  view-only).
- **EQ Service (the actual CMMS app)**: `lib/utils/roles.ts` `canWrite(role)`
  checks `can(role, 'service.create')` — and that same boolean gates **asset
  and customer mutation actions** across `app/(app)/assets/actions.ts`,
  `app/(app)/customers/[id]/contact-actions.ts`, and others (~520 usages
  overall route through `can()`/`isAdmin()`/`canWrite()`, confirmed fully
  canonical, no ad-hoc bypass — Service is a clean consumer, this isn't a
  Service bug).

SKS's live `tenant_role_override` grants `employee → service.create +
service.close`. That's a legitimate choice **for SKS's Shell UI**. Promoting
it to the canonical default would silently hand every employee in every
tenant asset/customer-edit rights inside Service — a real, cross-app
behaviour change hiding behind what looks like a Shell-only UI tweak.
**Conclusion: this key needs splitting by app (e.g. `service.create` vs a
Shell-only `service.raise_wo`) before it can ever be safely broadened. Tracked
for Phase 3.**

## The Cards conflation — four representations, confirmed independently

1. **The worker app itself** (Flutter) — role-agnostic for core features;
   reads `eq_role` for exactly 2 UI gates (join-QR visibility), both
   manager/supervisor-only, both display-only (not access control).
2. **A permission module** in the canonical matrix + Shell's client mirror —
   `cards.view`/`cards.onboard`. Now marked `deprecated` (this PR).
3. **A tenant entitlement** — `org_module_entitlements.cards` (unaffected,
   correct home for "does this tenant have Cards").
4. **An admin flag** — `org_memberships.role='admin'` gates the Cards admin
   UI (Flutter's `org_admin_provider.dart`) *and* a jvkn storage RLS policy
   (`org_admins_read_member_licence_photos` on `licence-photos`) *and* the
   connection-request notification email lookup. **Three consumers, not one**
   — Phase 2 must migrate all three or something (most likely the email
   notification, since it's easiest to overlook) silently breaks.

Live check (2026-07-08): 3 `org_memberships.role='admin'` rows exist —
Royce + EQ Dev only. The 10 SKS `eq_role='manager'` users are **not**
org-admins under the current flag. Confirms the two "admin" concepts already
disagree in production, not just in theory.

## Quotes — corrects an earlier wrong assumption

Earlier session notes assumed EQ Ops/quotes was unbuilt ("Future" per suite
state). **Wrong** — `src/modules/quotes/permissions.ts` is a real, live,
in-sync module matrix (verified byte-identical to canonical: manager gets all
3 perms, supervisor view+create, employee view-only, apprentice/labour_hire/
subcontractor none). SKS's `supervisor → quotes.approve` override is real and
untouched by this Phase 0 pass — no strong safety evidence yet to promote it
canonically, and unlike `equipment.view` there's no documented "this should be
broad" rationale in the module's own comments to lean on.

## `apprentice → intake.view` — a plan correction, not an execution

The original Phase 0 scope ("consider dropping apprentice's `intake.view`
default, since SKS denies it") was reconsidered and **reversed** on reading
Shell's own code: `src/modules/intake/permissions.ts`'s doc comment
explicitly frames `intake.view` as deliberately broad-by-design ("view by
default for all... gating tightens later when the bulk-import UI lands").
Removing it based on one tenant's one denial would have overridden a
documented product decision, not fixed a wrong default. Left alone; SKS's
denial override stands as legitimate tenant-specific tightening.

## What this changes for later phases
- **Phase 2 (one admin)**: exactly 3 consumers of `org_memberships.role`
  to migrate, now named. No more are expected but re-grep before landing.
- **Phase 3 (guardrails)**: split `service.create`/`service.close` by app
  before ever promoting a Service-affecting grant canonically. Consider
  whether Shell's client-matrix architecture (module-local mirrors) should
  be collapsed to derive from the package directly, closing the class of
  risk this inventory exists to catch. The `ops.*` module has no canonical
  home yet — decide whether it's promoted or stays permanently Shell-local.

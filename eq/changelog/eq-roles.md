---
title: eq-roles — Changelog
owner: Royce Milmlow
last_updated: 2026-08-08
scope: eq-roles (@eq-solutions/roles package) append-only history, mirrored from the repo's own CHANGELOG.md
read_priority: reference
status: live
---

# eq-roles changelog

## 2026-08-08 — canonical security-groups HTML export (no version bump — tooling/docs only)
- Answers "give me a full HTML export of security groups across the whole suite": `scripts/export-security-groups.mjs` generates a full HTML export (role matrix, permission matrix, default security groups) straight from `roles.json`, run via `npm run export:html`. The canonical half of the ask — a separate live per-tenant data pull was delivered outside this repo.
- README: added the missing `project_managers` row to the default-groups table, and — after a correction — a caveat on eq-field's adoption status that accurately reflects the legacy raw-PIN staff/supervisor squash as confirmed dead (server-gated unreachable since PR #575), not an active fallback.
- [PR #20](https://github.com/eq-solutions/eq-roles/pull/20), merged.

## 2026-07-27 — v2.5.8, new permission: ops.view_supplier_credentials
- Royce asked to make Suppliers' login/password columns Security-Groups-controlled instead of hardcoded to Manager/Supervisor. Found the DB-side gate (`eq_list_suppliers`, ehow migration 0195, live since 2026-07-21) already checked for this exact permission key via `extra_perms` — it just didn't exist yet in the roles package for anyone to grant.
- Added `ops.view_supplier_credentials` to `roles/model.json` (default roles: manager, supervisor — matches the existing hardcoded behaviour exactly, so nothing changes until someone actively grants it to anyone else). Rebuilt all derived artefacts. [PR #19](https://github.com/eq-solutions/eq-roles/pull/19), merged.
- Consumed by eq-shell [PR #1047](https://github.com/eq-solutions/eq-shell/pull/1047) same day — pin bump only, no new eq-shell migration needed.

## 2026-07-26 — v2.5.7, labour_hire promoted to equipment.view (access-model Phase 3)
- Audited all 10 live SKS `tenant_role_overrides` on jvkn against the locked 2026-07-08 `ACCESS-MODEL-PLAN.md` decisions. 9 of 10 already had a resolution on record; `labour_hire`/`equipment.view` was the one row with no precedent — not part of the earlier apprentice-only promotion, not a Cards-onboarding artifact.
- Royce's call: promote it — viewing equipment isn't sensitive. Added `labour_hire` to `equipment.view`'s role list in `roles/model.json`, rebuilt all derived artefacts (`roles.ts`/`.js`/`.json`, module slices, `lib/eq_roles.dart`), updated the `labour_hire` coverage test. 102/102 tests. [PR #18](https://github.com/eq-solutions/eq-roles/pull/18), merged.
- Consumed by eq-shell PR #1023 same day; confirmed live on core.eq.solutions (deploy `f24db117`) before the now-redundant SKS override row for the same grant was deleted.

## 2026-07-26 — v2.5.6, field.manage_people (mgr+sup)
- First Phase 3 guardrails conversion: eq-field's worker-record actions (add/edit/remove/restore/hard-delete, PIN management) had no matching canonical key. Added `field.manage_people`, manager + supervisor, matching `field.manage_roster`'s tier — preserves today's `isManager`-gated behaviour rather than narrowing it.

## 2026-07-26 — v2.5.5, real Dart package
- Added `pubspec.yaml`, moved the Dart emit to `lib/eq_roles.dart` so `pub`'s git-dependency resolution (as used by eq-cards for `eq_design_tokens`) can actually resolve this repo. No content change to the generated artefact itself.

## 2026-07-26 — v2.5.4, ops.view_suppliers / ops.manage_suppliers
- Promoted 2 keys eq-shell's client matrix already declared for its Suppliers directory UI but which never existed in the package; closed the interim `ops.manage_rates` reuse in `suppliers-mutate.ts`. `service.create`/`service.close`/`quotes.approve` deliberately not split this round — SKS has live overrides on all three; splitting is only actionable once/if a canonical broadening is proposed.

Full detail (all releases) in the repo's own `CHANGELOG.md`.

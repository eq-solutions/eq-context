---
title: eq-roles — Changelog
owner: Royce Milmlow
last_updated: 2026-07-26
scope: eq-roles (@eq-solutions/roles package) append-only history, mirrored from the repo's own CHANGELOG.md
read_priority: reference
status: live
---

# eq-roles changelog

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

---
date: 2026-06-15
topic: SKS Field staff — root-cause fix + full roster load via the canonical pipeline
tier: EQ (SKS tenant work)
status: done
---

# SKS Field staff load — 2026-06-15

Continuation of the worker-platform-architecture session. Goal: get a
correct, live staff list in EQ Field for SKS, the right way.

## Outcome

EQ Field went from **0 → 67 SKS staff** visible, all correctly tenant-tagged,
approved, deduped, with licences intact.

## What was wrong (verified live)

EQ Field reads the SKS tenant (`7dee117c`) in `ehow` (sks-canonical). Staff
weren't showing for two compounding reasons:

1. **Tenant mis-tag.** `workers-canonical-sync` (jvkn edge fn) hard-coded the
   tenant constant to `dcb71d03` — the **EQ/core** tenant, not SKS. Every
   synced worker landed on the wrong shelf. 39/40 staff were mis-tagged.
2. **Approval gate.** The function never set `field_approved`; the
   `field_people` view requires `field_approved IS TRUE OR NULL`; all rows
   were `false` → hidden even when tenant was right.

Earlier in the session I was also misled by stale local docs (the
`C:\Projects\CLAUDE.md` deploy map and an unloaded substrate) — corrected by
loading the substrate and verifying against live DBs. EQ Field's DB is
`ktmj` (the EQ demo tenant); SKS data is `ehow`; jvkn is control-only.

## What was done

1. **Fixed + deployed** `workers-canonical-sync` v4: tenant → `7dee117c`,
   `field_approved = true`, `employment_type` mapped from `eq_role`.
2. **Re-synced** the existing 35 via touching `jvkn.workers` (pipeline-correct).
3. **Cleanup:** deleted test-pilot + Emma Curth at source; re-pointed Collin
   Toohey's 7 licences off his dead dup onto his live row; removed the dup;
   kept Daniel Bower.
4. **Loaded 32 missing** into `jvkn.workers` (E.164 phones, mapped roles) →
   synced to ehow. Final: 48 Direct / 11 Apprentice / 8 Labour Hire = 67.
5. **`on_roster`**: added column (default true) + exposed in `field_people`;
   seeded 57 on / 10 off (office/management off, field supervisors on).
6. **Apprentice `year_level`** set for all 11 (from CSV Year column).

## Substrate

- New: [eq/field/staff-site-visibility-model.md](../eq/field/staff-site-visibility-model.md) (PR #26, merged).
- Decision logged: `ops/decisions.md` 2026-06-15 (this work) + phone-dedup entry.

## Still open

- **on_roster app filter** in `eq-field` (roster grid) — code + deploy.
- **Login hook** (phone-dedup) — workers still can't sign in. Separate track.
- **Sites** — curate `field_enabled` from 591 → live.
- **Daniel Bower** — confirm leaver.
- `workers-canonical-sync` single-tenant — generalise before a 2nd tenant syncs.

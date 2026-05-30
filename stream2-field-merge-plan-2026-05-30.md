---
title: Stream 2 — EQ Field + SKS Merge Plan
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Phased plan to unify EQ Field + SKS into one codebase (SKS as tenant; data stays separate)
read_priority: standard
status: live
---

# Stream 2 — EQ Field + SKS merge: execution plan

**Part of the "One Spine" sprint. Created 2026-05-30.**
**Status: PLAN. Code-merging is GATED behind a freeze (Phase 0) — both repos are currently hot.**

## Decisions locked (2026-05-30)
- **Surviving codebase = `eq-solutions/eq-field` (EQ Field).** SKS folds in as a **tenant**. One codebase serves both, routed by existing tenant detection.
- **`sks-canonical` (Supabase `ehowgjardagevnrluult`, created 2026-05-24) = control plane** for shared/canonical entities (mirrors `eq-canonical-internal` for EQ). **`sks-labour` (`nspbmirochztcjijmcrx`) stays the operational DB** for SKS roster/timesheets/leave. → **No mass operational-data migration; light ETL only.**
- This **deliberately reverses the 2026-05-20 split** (Field CLAUDE.md "do not port EQ↔SKS"). Royce-authorised for this sprint; that rule is superseded for the merge work, then the docs get updated.
- **Entities stay separate**: separate Supabase projects, separate credentials. The merge is *codebase* unification, not a data merge.

## Current state (precise, 2026-05-30)
| | EQ Field (surviving) | SKS NSW Labour (folding in) |
|---|---|---|
| Repo | `eq-solutions/eq-field` | `eq-solutions/sks-nsw-labour` |
| Version | v3.5.24 (now Plus Jakarta Sans + tokens, Stream 1) | v3.10.37 |
| Stack | vanilla HTML/JS/CSS, lazy-loader | vanilla HTML/JS/CSS, all-at-boot |
| Scripts | 42 | 38 |
| Operational DB | `ktmjmdzqrogauaevbktn` (eq-solves-field) | `nspbmirochztcjijmcrx` (sks-labour) |
| Site | eq-solves-field.netlify.app | sks-nsw-labour.netlify.app |
| **Live worktrees now** | 2 (phase1-eq-role-wiring, musing-mcnulty) | **5** (blissful-dirac, frosty-albattani, funny-satoshi, heuristic-jemison, **pipeline-ui**) |

- **SKS-only modules (~9):** `pipeline.js`, `pipeline-import.js`, `pipeline-resource.js`, `safety.js`, `safety-dashboard.js`, `teams.js`, `project-hours.js`, `xlsx.full.min.js` (+ `analytics-TODO-hooks.md`)
- **EQ-only modules (~12):** `apprentice-widget`, `forecast`, `diary`, `projects`, `region-filter`, `site-reports`(×3), `lazy-loader`, `tender-pipeline`, `toolbox`, `virtual-table`
- Tenant detection already exists in `app-state.js` (`_detectTenantSlug`, `TENANT_SUPABASE`, `TENANT_DISABLED_TABLES`).
- Known schema gotcha: SKS core IDs `bigint`, EQ `uuid` — already handled by `String()` coercion in code.

---

## Phases

### Phase 0 — Freeze & prep (HARD GATE — do not start merging before this)
- Land or close the in-flight worktrees in BOTH repos (esp. SKS `pipeline-ui`, mid-change on a module we must merge).
- Declare a freeze window on both repos.
- Tag a merge-base on each `origin/main`. Snapshot SKS changelog v3.5→v3.10.37 for the Phase-3 carry-forward list.
- Backfill on-disk migrations: SKS pipeline migrations were applied via MCP but not committed (Field CLAUDE.md open loop) — capture full migration state first.

### Phase 1 — Tenant-safety groundwork in EQ Field (no SKS code yet, low risk)
- **Boot branding → CSS vars:** replace hardcoded inline colours in `index.html` with vars set early by `app-state.js` (apply before paint) so SKS navy/purple `#1F335C`/`#7C77B9` vs EQ sky don't flash. Use the Stream-1 tenant-theme contract (`design_theming_architecture`: accent + logo + strip, `white_label_enabled`); SKS gets `white_label_enabled = true`.
- **Tenant detection:** add `sks-nsw-labour.netlify.app → sks` to the hostname map; add `sks` to `TENANT_SUPABASE` (`nspbmirochztcjijmcrx`).
- **Lazy-loader:** ensure every module (incl. incoming SKS ones) loads via the lazy manifest, not at boot.

### Phase 2 — Port SKS-only modules (tenant-gated)
- `pipeline.js` / `pipeline-import.js` / `pipeline-resource.js` → **namespace** to avoid colliding with EQ's `tender-pipeline.js`; gate behind `TENANT.slug === 'sks'` (or `pipeline_enabled` flag).
- `safety.js` / `safety-dashboard.js` → tenant-gated; add safety tables (`prestarts`, `toolbox_talks`) to the **EQ-tenant** `TENANT_DISABLED_TABLES` so EQ doesn't 404.
- `teams.js` → tenant-gated.
- `project-hours.js` → was removed from EQ (v3.4.71); SKS still uses it. Re-add **SKS-gated only**.
- `xlsx.full.min.js` → SKS bundles SheetJS inline, EQ uses CDN. Pick one; if CDN, update CSP in BOTH `netlify.toml` AND `_headers` (Field rule).

### Phase 3 — Reconcile SKS's 11-release lead
- Diff SKS v3.5.x→v3.10.37 against EQ; carry forward shared-core fixes/features EQ lacks (excluding the SKS-specific modules already handled in Phase 2). Land incrementally, smoke per change.

### Phase 4 — Data wiring (LIGHT — control-plane model)
- `sks-labour` stays operational; **no roster/timesheet migration.**
- Wire the unified app to read shared/canonical entities from `sks-canonical` where appropriate (mirror EQ's `eq-canonical-internal` usage). Define exactly which entities are canonical for SKS (org/site/staff master, licences — confirm during phase).
- bigint/uuid handled by existing `String()` coercion; normalise "SKS Direct" → "Direct" on read/write where canonical.

### Phase 5 — Cutover & retire
- Point `sks-nsw-labour.netlify.app` at the unified `eq-field` repo (tenant detection serves SKS branding/modules/DB).
- Smoke BOTH tenants exhaustively (auth, roster, timesheets, leave, SKS pipeline + safety, EQ apprentice/forecast/regions).
- Archive `eq-solutions/sks-nsw-labour` repo read-only.
- Update CLAUDE.md in both repos to the unified model (supersede the split note).

---

## Risks & mitigations
| Risk | Mitigation |
|---|---|
| Both repos hot (5+ worktrees) → conflicts | **Phase 0 freeze gate**; all work in isolated worktrees off `origin/main` |
| Wrong-brand flash at boot | Phase 1 CSS-var branding before paint |
| SKS pipeline vs EQ tender-pipeline name collision | Namespace + tenant-gate (Phase 2) |
| EQ tenant 404s on SKS-only tables | `TENANT_DISABLED_TABLES` (Phase 2) |
| Merging a module that's changing under me (pipeline-ui worktree) | Freeze gate; merge SKS pipeline only after that work lands |
| Reversing the documented split | Explicit Royce authorisation; update docs in Phase 5 |
| bigint/uuid | Existing `String()` coercion; no mass migration (control-plane decision) |

## Rollback
Keep `sks-nsw-labour` repo + site live until the unified build is proven. Tenant detection isolates EQ — the EQ tenant is unaffected throughout. Revert = repoint the SKS Netlify site back to the old repo.

## Execution rules (carried from Stream 1)
- Branch from `origin/main`, isolated worktrees, explicit staging, verify PR diff is only intended files, gate on green deploy-preview, smoke both tenants. No deploy/merge without explicit Royce go. Version-stamp every Field release (app-state.js + sw.js + index.html banner). See memory `feedback_shared_clone_git_guards`.

## RECON FINDING (2026-05-30) — re-scopes the plan

EQ Field's `origin/main` **already is a full multi-tenant codebase with complete SKS support** (retained from the pre-split shared codebase):
- `app-state.js`: `HOSTNAME_MAP['sks-nsw-labour.netlify.app']='sks'`, `_detectTenantSlug()` resolves sks, `TENANT_SUPABASE.sks`, `TENANT_DISABLED_TABLES.sks`, full `TENANT_BRANDING.sks` (real SKS logos from R2, codes `2026`/`SKSNSW`, group aliases `SKS Direct→Direct`, gate disclaimer, fallback mgr pw), `applyTenantBranding()` → `body.tenant-sks`.
- `base.css`: SKS palette already CSS vars — `--navy #1F335C`, `--purple #7C77B9` (used), plus EQ `--blue #3DA8D8`.

**Consequence:** Phase 1 (tenant-safety groundwork: branding-to-CSS-vars / detection / disabled-tables) is **~80% pre-existing** — do NOT rebuild it. The real work re-scopes to:
- **P1' Staleness audit — DONE 2026-05-30. Verdict: config NOT stale.** SKS's live `TENANT_BRANDING.sks` (logos, codes 2026/SKSNSW, aliases, disclaimer) is byte-identical to EQ Field's retained copy. Both repos are the same multi-tenant base; EQ Field's app-state is the larger superset (636 vs 528 lines — has tier/demo-trades/melbourne). Divergence is **modules/features only** (SKS v3.10.40 vs EQ v3.5.24), not tenant config. → merge = port modules + reconcile + cutover; no config refresh needed.
- **P2 Port SKS-only modules** — recon + **wired-state ground-truth done 2026-05-30** (table below). Revised order (safest first, project-hours dropped): **safety → teams → pipeline**. ⚠ The assumed easy "pattern-setter" (project-hours) evaporated on verification — every remaining port is substantial (≥446ln) and all require an SKS-boot → EQ-lazy conversion, so they want careful/supervised execution, **not** unattended auto-merge.
  - ~~`project-hours.js` (189 ln)~~ — **DROPPED — not a port.** Ground-truth: it is a **dead orphan in BOTH repos** — in SKS it has no live `<script>` tag (only a comment ref at `index.html:1269`), is **not** in `sw.js` PRECACHE, and is **not** lazy-loaded; in EQ it was **deliberately deleted** at v3.5.11 (overnight dead-code audit: *"orphan from the v3.4.71 feature removal that left the file behind"*). Re-adding it would re-introduce code EQ chose to remove. EQ already retains the `ph.*` perms + `feat_project_hours_v1` flag default + `sites.track_hours` column, so **cutover loses no functionality.** Revival as a live feature was **declined by Royce (2026-05-30 — "leave it dead")**, so it stays out of the merge entirely.
  - `safety.js`+`safety-dashboard.js` (1259 ln) — dedicated surface; add `prestarts`/`toolbox_talks` to `TENANT_DISABLED_TABLES.eq`.
  - `teams.js` (448 ln) — **coupled** (woven into roster/contacts/schedule, STATE-heavy) → reconcile carefully.
  - `pipeline.js`+`pipeline-import.js`+`pipeline-resource.js` (2439 ln) — `SKS_PIPELINE` namespace (low collision w/ EQ `tender-pipeline`), but huge + SKS `pipeline-ui` worktree recently active → do LAST, after that work lands.
  - Per-port checklist: copy from sks-nsw-labour origin/main → reconcile cross-version deps (SKS v3.10 vs EQ v3.5) → **convert SKS boot `<script>` tag → EQ lazy-loader manifest entry** + nav (tenant/flag-gated) → disabled-tables for EQ → add to EQ `sw.js` PRECACHE → version bump → smoke BOTH tenants. Worktree `claude/field-merge-phase1`.

  **Verified wired-state in SKS `origin/main` (ground-truth 2026-05-30):**

  | Module | Lines | SKS live `<script>`? | SKS `sw.js` precache? | EQ Field has file? | Port verdict |
  |---|---|---|---|---|---|
  | `project-hours.js` | 189 | ❌ comment only (`:1269`) | ❌ | ❌ deleted v3.5.11 | **NO PORT — dead in both** |
  | `teams.js` | 446 | ✅ `:64` | ✅ | ❌ | port — **coupled**, careful |
  | `safety.js` | 989 | ✅ `:89` | ✅ | ❌ | port — dedicated surface |
  | `safety-dashboard.js` | 270 | ✅ `:90` | ❌ | ❌ | port (with safety.js) |
  | `pipeline-import.js` | 376 | ✅ `:85` | ✅ | ❌ | port (with pipeline) |
  | `pipeline.js` | 583 | ✅ `:86` | ✅ | ❌ | port — `SKS_PIPELINE` ns |
  | `pipeline-resource.js` | 1480 | ✅ `:87` | ✅ | ❌ | port — largest, do last |

  Method note: a `grep` count of `src="scripts/<m>.js"` over-counts — the v3.4.71 history comment block embeds the string for project-hours/etc. Confirm with an anchored `^[[:space:]]*<script src=` match **and** the `sw.js` PRECACHE list before calling a module "live".
- **P3 Reconcile** the rest of the 11-release delta. (unchanged)
- **P4 light canonical wiring.** (unchanged)
- **P5 Cutover** — point `sks-nsw-labour.netlify.app` at the EQ Field repo, smoke both tenants, retire old repo. (unchanged)

Worktree for this work: `claude/field-merge-phase1` off `origin/main`.

## References
- Sprint: `eq-context/sprint-2026-05-30-one-spine.md` · Audit: `eq-context/design-audit-2026-05-30.md`
- Memory: `project_field_merge_tenant_model`, `design_theming_architecture`, `feedback_shared_clone_git_guards`
- Supabase: sks-canonical `ehowgjardagevnrluult` · sks-labour `nspbmirochztcjijmcrx` · eq-solves-field `ktmjmdzqrogauaevbktn`

---
title: Autonomous Sprint — State
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Per-repo + Supabase reality snapshot, CI guards, and known hazards for the sprint
read_priority: critical
status: live
---

# Autonomous Sprint — STATE (current reality; refresh at sprint start)

Snapshot 2026-05-30. **Verify before relying on the git/worktree lines** — they drift. The Supabase map + SKS-live flags are stable.

> ## ⏩ POST-SPRINT UPDATE — end of 2026-05-30 (supersedes the table rows below where they conflict)
> The "everything-then-cutover" fan-out completed. Current reality:
> - **eq-solves-field** → **v3.5.29 on `main`**, clean. All SKS-only modules ported, **triple tenant-gated to `sks`** (EQ provably unaffected): `safety` (#138), `teams` (#139), `sks-pipeline*` (#140), + 10 B3 reconcile fixes (#141). My worktree removed; clone on main.
> - **eq-shell** → consumes **`@eq-solutions/roles`** (C2 #70 — replaces hand-defined matrix, perms verified identical) **and `@eq-solutions/ui`** (#71 — Table+Skeleton; Button still CSS-classes = follow-up). `claude/c3-auth-spike` (#72) is a **no-deploy reference spike** (live auth untouched). Prior equipment-intake session appears settled.
> - **eq-solves-service** → consumes `@eq-solutions/ui` (#205, re-exports; `transpilePackages` set).
> - **eq-cards** → tokens consolidated (#10 — dead `EqSpacingTokens` dropped, barrel export).
> - **NEW packages:** **`@eq-solutions/roles`** (public github.com/eq-solutions/eq-roles — consumed by Shell) + **`@eq-solutions/ui`** (public github.com/eq-solutions/eq-ui — Button/Skeleton/Table, token-only — consumed by Shell+Service). Both alongside `@eq-solutions/tokens`. Design pillar = COMPLETE.
> - **Branch tidy-up:** 108 old merged branches deleted across eq-field/shell/service/cards; unmerged/open + reference branches kept.
> - **Remaining = Royce-driven:** B4 canonical wiring (cutover-phase), B3 medium/high (#5 schema, #11 structural, #13 DB-migration), E1 Cards rebuild, ⛔ C4 auth cutover, **B5 cutover = LAST (SKS-live)**. SKS-live (`nspbmirochztcjijmcrx`) untouched throughout.

## Repos
| repo | GitHub | prod target | branch state @ snapshot | notes |
|------|--------|-------------|--------------------------|-------|
| **eq-shell** | eq-solutions/eq-shell (public) | **core.eq.solutions** (auth hub) on `main` | main synced; **ACTIVE other sessions** | worktrees: `affectionate-yonath` (85 uncommitted!), `equipment-finish`, `festive-burnell`, `naughty-heyrovsky`, `equipment-qr-hierarchy`(#69). Build `pnpm run build`. Hotspot file: `src/pages/TenantHome.tsx`. |
| **eq-solves-field** | eq-solutions/eq-field (public) | eq-solves-field.netlify.app on `main` | idle ~17h; main behind 2 | EQ-side of the merge. Stale worktree `musing-mcnulty` (5 uncommitted). My `claude/field-merge-phase1` worktree staged. Vanilla HTML/JS/CSS; version-stamp every release. |
| **sks-nsw-labour** | eq-solutions/sks-nsw-labour | **sks-nsw-labour.netlify.app = SKS LIVE — DO NOT DEPLOY** | idle ~18h; ahead1/behind3 | 5 stale worktrees incl `pipeline-ui`. Source of the SKS-only modules to PORT (read from `origin/main`). |
| **eq-solves-service** | Milmlow/eq-solves-service | eq-solves-service.netlify.app on `main` | #203/#204 merged; local main diverged (leave) | Next 16. `npm run check` before push. CI `data-quality audit` fails on expired `SUPABASE_ACCESS_TOKEN` (known, unrelated). Worktree `charming-dirac` dormant (committed). |
| **eq-cards** | Milmlow/eq-cards | (Flutter app) | **clean**, idle ~18h, no worktrees | safest repo to work in. NOT SKS. |
| **eq-intake** | (home of `@eq/*`) | n/a (vendored into eq-shell) | **main ahead 23 unpushed**; active worktree `clever-roentgen` (6 uncommitted) | changes here must be **re-vendored into eq-shell**. |
| **eq-roles** | not yet remote | n/a (package) | local git only, 1 commit | `C:\Projects\eq-roles`. Push pending Royce OK (new public repo). |
| **eq-design-tokens** | eq-solutions/eq-design-tokens (**public**) | n/a (package) | v1.0.0 tag | consumed by Shell/Field/Service via git-dep. |

## Supabase projects (org `sqjyblkiqonyrdobaucn`, ap-southeast-2)
| ref | name | role | access |
|-----|------|------|--------|
| `jvknxcmbtrfnxfrwfimn` | eq-canonical | control plane (browser-facing: intake events, list RPCs) | browser via VITE_SUPABASE_URL |
| `zaapmfdkgedqupfjtchl` | eq-canonical-internal | EQ tenant data plane (`app_data.*`, commit RPCs) | **server-only** via Netlify functions |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | EQ Field tenant DB | per app-state |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Service DB | per repo |
| `ehowgjardagevnrluult` | sks-canonical | SKS control plane (created 2026-05-24) | server-side; SKS tenant id `7dee117c-98bd-4d39-af8c-2c81d02a1e85` |
| `nspbmirochztcjijmcrx` | sks-labour | **SKS LIVE operational DB** | **READ-ONLY / AVOID — SKS live** |

**Two-plane rule:** browser talks only to the control plane; tenant data (`app_data.*`) is server-only via Netlify functions (`getTenantDataClientById`). Browser cannot call tenant RPCs directly.

## CI guards
| guard | repo | status |
|-------|------|--------|
| token drift-guard | eq-solves-field | ✅ `.github/workflows/tokens-drift.yml` |
| token drift-guard | eq-cards (dart) | ⚪ not built (deferred w/ A4) |
| **dup-migration guard** | eq-solves-service | ⚪ **spec'd, not built** (RULES §6) — broke twice; build first |

## Known hazards (don't re-trip these)
- Sequential `00xx` migrations collide across parallel agents → **timestamps only** (RULES §3). `eq-solves-service 0110` taken.
- Branching from local `main` drags other sessions' commits → **branch from `origin/main`** (RULES §2).
- Stale worktrees hold uncommitted work → **never prune without confirming committed** (RULES §2).
- `eq-shell src/pages/TenantHome.tsx` edited by PRs #64/#65/#68/#69 → coordinate.

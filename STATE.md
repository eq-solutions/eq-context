---
title: Autonomous Sprint — State
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Per-repo + Supabase reality snapshot, CI guards, and known hazards for the sprint
read_priority: critical
status: live
---

# Autonomous Sprint — STATE (current reality; refresh at sprint start)

Snapshot 2026-05-30. **Verify before relying on the git/worktree lines** — they drift. The Supabase map + SKS-live flags are stable.

> ## ⏩ POST-SPRINT UPDATE — end of 2026-05-30 (Sprint 1 + Sprint 2 Waves 1–2 ALL MERGED; supersedes the table rows below where they conflict)
> The "everything-then-cutover" fan-out + Sprint 2 completed. Current reality:
> - **eq-solves-field** → **v3.5.33 on `main`**, clean. SKS-only modules ported + **triple tenant-gated to `sks`** (EQ provably unaffected): `safety` (#138), `teams` (#139), `sks-pipeline*` (#140) + 10 B3 reconcile fixes (#141). **Wave 1 #143 (v3.5.31):** timesheet pre-fill, multi-week export, hard-delete leave, roster copy-week, audit-log field-fix. **Wave 2 #144 (v3.5.32):** roster PDF/print, dashboard gap-card, calendar person-filter, apprentice year auto-advance. **Batch #145 (v3.5.33):** weekly site-attendance report, roster bulk assign/clear, mobile roster swipe (pages the *week*), + **print.css EQ/SKS tenant-brand fix** (EQ deep default, navy only under `body.tenant-sks`). Worktrees cleaned. **EQ-tenant no-migration backlog now ~exhausted** — next Field work needs a parked migration, the #20 PIN/auth fix, or net-new scope (see `field-feature-backlog-2026-05-30.md` BUILD STATUS).
> - **eq-shell** → consumes **`@eq-solutions/roles`** (C2 #70 — perms verified identical) **and `@eq-solutions/ui` fully** (#71 Table+Skeleton; **#73 Button across all 14 surfaces** + eq-ui v1.0.1 bordered ghost). **Wave 2 #75:** iframe errors→`EqError`, retry loading-state, null-tenant notice, NotFound plain-English + aria. `claude/c3-auth-spike` (#72) = no-deploy reference (live auth untouched).
>   - **2026-05-31 (C4 console):** **PR #79 MERGED → main `9905be5`, LIVE + smoke-verified** (`core.eq.solutions/.netlify/functions/verify-shell-session` → 401): intake-commit server-authz (was wide open to any signed-in user), 3 UI button/token bugs, `friendlyError`, `docs/cross-app-audit.md`. Added `netlify/functions/_shared/permissions.ts` (re-defines matrix = Rule §5 divergence, identical-to-canonical, reconcile via C8). **PR #80 OPEN/MERGEABLE — ⛔ auth-gated:** TS strict + TOTP rate-limit. **PR #78 (canonical reconciliation) also MERGED → main.** Open eq-shell PRs: #80 (auth-gated), #72 (spike, no-merge), #69 (equipment), #64 (AI briefing).
> - **eq-solves-service** → consumes `@eq-solutions/ui` (#205). **Wave 1 #206:** pre-visit tech-brief + 4 quality fixes. **Wave 2 #207:** defect detail+photos, analytics cuts (in-app, not RPC), canonical-export fill stubs, asset detail `/assets/[id]`, calibration reminders, skip-nav, detail loading. `npm run check` clean, 201/201 vitest.
> - **eq-cards** → tokens consolidated (#10). Cards worker-first rebuild (E1) deferred → now directed by the worker-credentials model (below).
> - **2026-05-31 — WORKER-CREDENTIALS MODEL DECIDED (design):** worker data lives in the **worker-house** (`eq-canonical-internal` `worker_*`), first-class `worker_id`, SKS-seed-via-Intake as the verification event (evidence-on-file → top trust tier). Build order: worker-house + reminders FIRST, snapshot/live-link/grant SECOND. **Supersedes the Cards-rewire per-business-tenant assumption — do NOT flip Cards `gateway` yet.** Record: `eq/identity/worker-credentials-model-2026-05-31.md`; sprint: SPRINT-BOARD Stream G.
> - **Packages:** **`@eq-solutions/roles`** (public — consumed by Shell) + **`@eq-solutions/ui` v1.0.1** (public, bordered ghost — consumed by Shell+Service) + `@eq-solutions/tokens`. Design pillar = COMPLETE. ⚠ A concurrent session is tagging these (`eq-roles v1.0.0`, `eq-ui v1.0.1`) + moving consumers `#main`→consume-by-tag (also owns the literal `STATE.md` row-33 fix this round).
> - **Branch tidy-up:** 108 old merged branches + all Wave-2 branches deleted across eq-field/shell/service/cards; unmerged/open + reference branches kept.
> - **HELD — Royce-gated (features ship dormant until you act):** 3 DB migrations NOT run — licence-expiry (`people.licence_expiry` @ `ktmjmdzqrogauaevbktn`), timesheet-approval (`approved`/`approved_by`/`approved_at` on `timesheets`), audit-log-UI (`target_id`/`target_name` on `audit_log`). Plus B4 canonical wiring, ⛔ C4 auth cutover, **B5 cutover = LAST (SKS-live)**. SKS-live (`nspbmirochztcjijmcrx`) untouched throughout.
> - **EYEBALL (low-risk, post-merge):** (1) F-W2-4 apprentice auto-advance batch-mutates real rows — test on one apprentice before broad use; (2) **#145 print colours** — confirm browser Print-preview shows EQ-deep on an EQ tenant + navy on SKS (cascade-verified via `body.tenant-sks`, but browser print pixels not machine-provable); (3) **#145 mobile swipe** pages the *week* (the one-day-view premise was stale) — isolated ~70-line block, easy to retune. (print.css SKS-navy follow-up = DONE in #145.)

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

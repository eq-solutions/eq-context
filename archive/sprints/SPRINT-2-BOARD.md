---
title: Sprint 2 — Board
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Sprint 2 backlog (Cards worker-first rebuild + EQ Field/Service feature pushes + quality/UX polish); discovery → Royce-select → build
read_priority: critical
status: live
---

# Sprint 2 — BOARD

**Sprint 1** (design consistency + Field/SKS codebase merge + auth/roles foundation) = ✅ **COMPLETE** — see [`SPRINT-BOARD.md`](SPRINT-BOARD.md). Cutover (B4 / B5 / C4) stays Royce-gated and separate.

Royce selected 4 streams (2026-05-30). **Phase 0 = DISCOVERY** — read-only agents propose ranked backlogs/plans → Royce selects what to build → fan out build agents (each a reviewed PR, EQ-safe, **never SKS-live**).

## Streams
| id | stream | phase | discovery doc | notes |
|----|--------|-------|---------------|-------|
| **S2-A** | Cards worker-first rebuild (E1) | 🔵 discovery | `archive/sprints/cards-rebuild-plan-2026-05-30.md` | rebuild eq-cards on the worker-first model; folds in A4 tokens + `@eq-solutions/ui` patterns; needs Royce product steer |
| **S2-B** | EQ Field feature push | 🔵 discovery | `field-feature-backlog-2026-05-30.md` | ranked roster/resource feature backlog (staff/licences/availability/assignments/time/shutdowns) |
| **S2-C** | EQ Service (CMMS) feature push | 🔵 discovery | `service-feature-backlog-2026-05-30.md` | ranked maintenance/defect/report feature backlog |
| **S2-D** | Quality + UX polish | 🔵 discovery | `quality-polish-backlog-2026-05-30.md` | error/empty/loading states, a11y, perf, mobile polish, suite-wide; folds in #73 + substrate drift |

## Build Wave 1 — IN FLIGHT (2026-05-30; Royce selected Field + Service + Quality; Cards deferred)
- ✅ **S2-B Field batch (6) MERGED** (#143, Field **v3.5.31**). Timesheet pre-fill + multi-week export + hard-delete leave + roster copy-week + audit-log fix (was a `who`/`manager_name` field bug silently dropping auth-audit events — no migration needed). Licence-expiry ships **dormant**. ⚠ **PENDING ROYCE MIGRATION** (apply to activate licence-expiry alerts): `ALTER TABLE people ADD COLUMN IF NOT EXISTS licence_expiry date;` on `ktmjmdzqrogauaevbktn`.
- ✅ **S2-C Service batch MERGED** (#206). **4 of 5 "features" were ALREADY BUILT** (discovery doc over-stated the gaps — Service is more complete than thought). Net new: pre-visit **tech-brief** (inline schedule editor + Resend email w/ `.ics`, graceful-degrade on no RESEND key) + 4 quality fixes (Modal + SlidePanel focus traps, global `:focus-visible`, loading.tsx ×5 + error.tsx boundary). CI green.
- 🔵 **S2-D-shell Shell quality (A4 focus-visible + Z2 live-feed bug)** — `claude/s2-shell-quality` (worktree `eq-shell-s2-wt`).
- ✅ **#73 MERGED** (2026-05-30) — Shell now consumes `@eq-solutions/ui` Button across the app (14 files) + eq-ui **v1.0.1** (`886c5de`, bordered ghost) pinned via `pnpm-lock.yaml`. Royce approved the preview; squash-merged. Design pillar fully closed on Shell.
- ✅ **Substrate-drift docs** — eq/pending.md §EQ Shell superseded-banner (two-plane + GTM-removed); non-negotiables.md ADR sprint-scope pointer.
- ⏸ **S2-A Cards MVP** — deferred (Royce: not building now).

All build agents report for review (no auto-merge); merges gate on green; tidy branches.

## Build Wave 2 — ✅ COMPLETE, ALL MERGED (2026-05-30; Royce: "merge everything")
Discovery agent extracted next-ranked **unbuilt** items per stream (Wave-1-built + already-built excluded). Full doc: `archive/sprints/sprint2-wave2-shortlist-2026-05-30.md`. Royce selected Field core (4) + Service (5) + Quality (6); did NOT select the 2 migration-gated Field items (F-W2-5/F-W2-6) → **HELD**. 3 build agents fanned out (one PR per repo, gate-on-green) → **all merged**:
- ✅ **Field #144 (v3.5.32)** — F-W2-1 roster PDF/print · F-W2-2 dashboard gap-card · F-W2-3 calendar person-filter · F-W2-4 apprentice year auto-advance (`people.year_level` exists → shipped; manager-gated; real cert labels preserved). Dup-ID + `node --check` clean.
- ✅ **Service #207** — S-W2-1 defect detail+photos · S-W2-2 analytics cuts (**in-app, not RPC** → stays migration-free) · S-W2-3 canonical-export fill stubs · S-W2-4 asset detail `/assets/[id]` · S-W2-5 calibration reminders · Q-W2-1 skip-nav · Q-W2-5 detail loading.tsx (1 already-built skipped). `npm run check` clean, 201/201 vitest.
- ✅ **Shell #75** — Q-W2-2 iframe errors→`EqError` · Q-W2-3 retry loading-state+aria · Q-W2-4 null-tenant notice · Q-W2-6 NotFound plain-English + sync-bar aria. `pnpm run build` clean, no auth touched.
- ✅ **#73** — Shell Button across 14 surfaces + eq-ui v1.0.1 bordered ghost. Design pillar closed on Shell.

**EYEBALL (low-risk, post-merge):** (1) F-W2-4 batch-mutates real apprentice rows — test on one apprentice (1→2) before broad use; (2) eq-field `print.css` SKS-navy `#1F335C` on shared EQ/SKS stylesheet → brand follow-up (spawned as a task).
**Lesson:** Service discovery over-claimed gaps 10× total (4 Wave 1 + 6 Wave 2) — always verify against live code before building.

> **⚠ CONCURRENT SESSION (2026-05-30) — semver/tagging work overlaps these repos.** A separate session is doing dependency-hygiene: tag `eq-roles v1.0.0` (`2bc5573`) + `eq-ui v1.0.1` (`886c5de`); repoint **eq-shell** + **eq-solves-service** `package.json` from `#main`→consume-by-tag (`#v1.0.0`/`#v1.0.1`) + relock; add a "consume-by-tag, never `#main`" rule to `AUTONOMOUS-SPRINT-RULES.md` + fix stale `STATE.md` row 33. **Complementary, not colliding** (they own the *dep/version* layer; this session owns the *feature/component* layer — different files). Coordination: (1) **#73 already adopted eq-ui 886c5de in Shell's lockfile** → their Shell change reduces to the `package.json` spec line; (2) my Wave-2 agents do NOT touch `package.json`/lockfile, so no dep race; (3) **both sessions write eq-context — pull before push**; (4) `STATE.md` row 33 + `AUTONOMOUS-SPRINT-RULES.md` are owned by that session this round — this session left them untouched.

> **⚠ Service is more complete than the discovery doc claimed.** The Wave-2 agent verified each candidate against the live `eq-solves-service` codebase and found **6 MORE already-built** items wrongly listed as gaps: site-access edit UI (`SiteForm.tsx`), all 4 notification event-types firing, field-sync admin trigger (`IntegrationsClient.tsx`), renewal-pack page, portal scope register, scope-from-work derive wizard. **Lesson reinforced (from #206): always verify Service "gaps" against code before building.**

**Field core (4, zero-risk, no migration):** F-W2-1 roster PDF/print · F-W2-2 dashboard gap-alerts card · F-W2-3 leave-calendar person filter · F-W2-4 apprentice year auto-advance (manager-gated batch write).
**Field migration-gated (2):** F-W2-5 timesheet approval + bulk-approve (needs `approved`/`approved_by`/`approved_at` on `timesheets`) · F-W2-6 searchable audit-log UI (needs `target_id`/`target_name` on `audit_log`). → ship dormant + flag SQL (licence-expiry pattern), or hold.
**Service (5, additive — RPCs/read-only, no schema change):** S-W2-1 defect detail page + photo attachments · S-W2-2 analytics per-customer/per-tech cuts · S-W2-3 canonical-export fill stubs (nsx_test/rcd_test/contract_scope/pm_calendar) · S-W2-4 asset detail `/assets/[id]` · S-W2-5 instrument calibration-due reminders (cron extension).
**Quality (6, all S):** Q-W2-1 Service skip-nav (WCAG 2.4.1) · Q-W2-2 unify Shell iframe errors onto `EqError` · Q-W2-3 `EqError` retry loading-state + aria-label · Q-W2-4 dashboard null-tenant "workspace not ready" notice · Q-W2-5 detail-page `loading.tsx` (maintenance/[id] + sites/[id] + 3 testing routes) · Q-W2-6 Shell NotFound jargon fix + sync-bar aria.

## Rules (carried from Sprint 1 — see `AUTONOMOUS-SPRINT-RULES.md`)
Branch from `origin/main`; isolated worktrees; **reviewed PRs** — no auto-merge to a core surface on visible / behavior / auth changes without Royce's look; EQ-safe (tenant-gate SKS-only code); **timestamp migrations**; **never touch SKS-live** (`nspbmirochztcjijmcrx`); gate on green deploy-preview; tidy branches as we go.

## Carry-over from Sprint 1
- **#73 Shell Button** — held (Royce preview check; borderless-vs-bordered ghost) → folds into S2-D.
- **B4 canonical wiring + B3 #13** (audit-revert migration) — held for cutover.
- **Substrate drift** (eq/pending.md two-plane/GTM stale) + **non-negotiables/§7 ADR-pointer** — Royce decision-grade → S2-D candidates.

## How this runs
Phase 0 discovery docs land → Royce picks the build items per stream → Phase 1 build agents fan out (reviewed PRs) → review/merge/tidy, same as Sprint 1.

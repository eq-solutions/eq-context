---
title: EQ Tier — Index
owner: Royce Milmlow
last_updated: 2026-08-10
scope: EQ Solutions work — products, decisions, build state
read_priority: critical
status: live
---

# EQ Tier

Default load when working on any EQ Solutions topic. Lead module per
post-cull strategy (29 April 2026): **EQ Field**. Build strategy
(updated 2026-06-02): we build EQ for ourselves (SKS NSW) because it's
a good product. Sequencing is by the trust ladder + Royce's go — **not**
gated on outside validation. The old 5-outside-subbie GTM gate is dead
(see `ops/decisions.md` 2026-06-02).

## EQ substrate map

Every canonical EQ file as a full URL — clickable from `/context/claude`:

- [eq/pending.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/pending.md) — EQ-only to-do list
- [eq/products.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/products.md) — EQ live product status
- [eq/cards/canonical-migration/plan.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/cards/canonical-migration/plan.md) — Cards §18 close-out: move Cards data to eq-canonical, retire standalone Supabase, SSO via shared JWT (active workstream 2026-05-20)
- [eq/canonical-readiness/plan.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/canonical-readiness/plan.md) — Canonical layer readiness plan: bring eq-canonical to the shape needed to host Intake + Field + Quotes as first-class modules. **EXECUTED 2026-05-20** — all 6 work units shipped (42 entities across 5 modules)
- [eq/canonical-readiness/spine.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/canonical-readiness/spine.md) — **The trust spine**: which 6 of 55 `app_data` tables must be identical/trusted across tenants vs free to vary. Foundation for the coherence rung + drift guard (2026-06-02)
- [eq/sprints/2026-05-20-S1-canonical-lockin.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/sprints/2026-05-20-S1-canonical-lockin.md) — Sprint S1: canonical-readiness lock-in + ship-ready. 10 items, 1-week, security rotations + PostgREST schema exposure + first functional Core dropzone + Cards iframe deploy (draft 2026-05-20)
- [eq/canonical-readiness/audit-2026-05-21.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/canonical-readiness/audit-2026-05-21.md) — Honest audit of core.eq.solutions post-S3. Top issues: EntityImportPanel hangs the renderer; home screen reads as admin dashboard not platform; intake legacy has no topbar. **All 8 items shipped + verified in browser 2026-05-21**.
- `eq/templates.md` — forward-pointer; re-checked 2026-07-20, still does not exist — will be created when the first EQ deliverable template is captured

## Strategic focus (2026 Q2)

- **Building for ourselves.** EQ is built for SKS NSW because it's a good
  product. No outside-validation gate (killed 2026-06-02).
- **Sequencing** is by the trust ladder + Royce's go — not by waiting for
  external users.
- **EQ Field** remains the lead module; Shell / Service / Intake / Cards
  build in parallel.
- **Target market** = ALL trade subcontractors (electrical, mechanical,
  fire, hydraulic, civil) — not narrowed to electrical.

## Files

| Path | Purpose |
|---|---|
| `progress/README.md` | EQ progress tracking — index + how to use `progress/current.md`, `progress/customers.md`, `progress/decisions-log.md`, `progress/year-goals.md` |
| `progress/current.md` | Weekly rolling commercial/product/strategic update toward the 2026 year-end EQ evaluation |
| `progress/customers.md` | Design partners / pilots / commercial conversations register |
| `progress/decisions-log.md` | Portfolio/FDE-narrative judgment calls — narrower than `ops/decisions.md` |
| `progress/year-goals.md` | Draft year-end evaluation criteria — live goal stays in `system/TODAY.md` |
| `pending.md` | EQ-only to-do list |
| `pending-archive.md` | Done items rotated out of pending.md nightly (`scripts/rotate_pending.py`) — historical record only |
| `verify-queue.md` | Items only blocked on Royce's own live click-through — the build itself is already done, rotated out of pending.md by `scripts/rotate_pending.py` |
| `documents/internal-signoff-register-design-2026-08-01.md` | Internal document sign-off register — design + build-plan; steps 1-5 (register view) live, reminder cron + rollout past the pilot still open |
| `documents/internal-signoff-register-sprint-2026-08-04.md` | Internal document sign-off register — hardening sprint, companion to the design doc above; T1 (per-signer RLS scoping) blocked on an identity-model call, deferred by Royce |
| `cards/portable-trade-identity-audit-2026-07-20.md` | Cards portable-trade-identity audit — first-slice item 1 closed, items 2–4 + Path A/B/C await Royce |
| `products.md` | EQ live product status |
| `active.md` | Live-state snapshot (staff/site/licence counts) — cross-check against products.md before quoting a headcount, they've drifted before |
| `punch-list-2026-06-02.md` | 2026-06-02 punch list — several items superseded, treat as historical unless re-confirmed live |
| `field-eq-core-only-plan.md` | Plan: EQ tenant is Core-only, closes the demo login gate |
| `go-live-runbook.md` | Go-live runbook |
| `field/multi-tenancy/` | EQ Field MT plan + explainer (active reference) |
| `field/permissions/field-shell-security-groups-2026-06-05.md` | 2026-06-05 permission-groups audit — superseded by `identity/enforcement-site-inventory-2026-07-08.md`, kept for history |
| `field/staff-site-visibility-model.md` | Staff/site visibility model |
| `cards/canonical-migration/plan.md` | EQ Cards §18 close-out (active 2026-05-20) |
| `cards/worker-platform-direction-2026-06-15.md` | Cards worker-platform direction |
| `canonical-readiness/plan.md` | Canonical layer readiness for Intake/Field/Quotes ports (draft 2026-05-20) |
| `canonical-readiness/spine.md` | The trust spine — which tables must be identical across tenants |
| `canonical-readiness/audit-2026-05-21.md` | Post-S3 honest audit, all items shipped |
| `canonical-readiness/audit-existing-tables.md` | Existing-table audit |
| `canonical-readiness/canonical-target-model-2026-06-24.md` | Canonical target model |
| `canonical-readiness/canonical-consolidation-roadmap-2026-06-25.md` | Consolidation roadmap |
| `canonical-readiness/contract-scope-canonical-design-2026-06-15.md` | Contract-scope canonical design |
| `canonical-readiness/labour-hire-rates-canonical-design-2026-07-04.md` | Labour-hire rates canonical design |
| `canonical-readiness/plan-control-plane-governance-and-card-read-2026-06-25.md` | Control-plane governance + Cards read plan |
| `canonical-readiness/plan-eq-service-migration-apply-gate-2026-07-03.md` | EQ Service migration apply-gate plan |
| `canonical-readiness/service-consumes-canonical-spine-2026-06-16.md` | Service-consumes-canonical-spine design |
| `canonical-readiness/ticket-field-licence-read-2026-06-25.md` | Field licence-read ticket |
| `identity/IDENTITY-MODEL.md` | **Current source of truth** for Shell auth/session/canonical identity — check this first on any auth-adjacent work |
| `identity/ACCESS-MODEL-PLAN.md` | Access-model program plan (permission keys, RLS) |
| `identity/PHASE-1F-PLAN.md` | Phase 1.F plan — **shipped 2026-05-20**, historical, superseded by IDENTITY-MODEL.md |
| `identity/enforcement-site-inventory-2026-07-08.md` | Current permission-enforcement site inventory, supersedes the 06-05 field/permissions audit |
| `identity/gate-a-decision-2026-06-03.md` | Gate A decision record |
| `identity/identity-convergence-target-2026-06-04.md` | Identity convergence target design |
| `identity/onboarding-portable-identity-2026-06-04.md` | Portable-identity onboarding design |
| `identity/service-canonical-identity-seam-2026-06-25.md` | Service/canonical identity seam design |
| `identity/worker-credentials-model-2026-05-31.md` | Worker credentials model |
| `identity/worker-onboarding-flows.md` | Who enters what, per app — answers "who uploads onboarding info" per scenario (Shell/Field/Service/Cards), names the one real gap (Shell↔Field worker duplication, parked in eq-field's own ADR) |
| `identity/parity-harness/phase1-parity-note-2026-07-10.md` | Phase 1 parity-harness note |
| `ops/EQ-OPS-ARCHITECTURE.md` | **Read before touching `app_data.quote`, `app_data.jobs`, `job_number`, or the Kanban stage taxonomy** — EQ Ops scope, its relationship to NSW Comms and EQ Field, and the quote-to-job data model |
| `design/claude-design-context.md` | Claude Design "start with context" brief for EQ brand |
| `sprints/2026-05-20-S3-polish-and-audit.md` | Sprint S3 polish + audit doc, historical |
| `changelog/*.md` | Per-product changelogs — **all 4 duplicate pairs resolved 2026-07-19**. `shell.md`/`service.md`/`cards.md` were abandoned (stopped 3-19 days before their twin) — each carries a "Superseded" banner; use `eq-shell.md`/`eq-service.md`/`eq-cards.md`. `field.md` and `eq-field.md` had both been actively written for months in parallel — 18 PRs that only existed in `eq-field.md` were merged into `field.md` at their correct dates; `eq-field.md` now carries a "Merged" banner listing what moved. `field.md` is canonical going forward. Plus `changelog/eq-context.md` and `changelog/eq-intake.md`, which have no duplicate, and the newer single-copy logs `eq-roles.md`, `eq-ui.md`, `eq-receipts.md`, and `eq-solves-service.md`. |

## Killed / deferred (do not reference as live products)

See `eq/products.md` → "Killed / Deferred" section for the canonical list — not
restated here to avoid a third copy (CLAUDE.md §9 and this file both used to
duplicate it independently).
- **AHD** — parked to 2027 (changelog at `/archive/changelog-ahd.md`)

**EQ Quotes** — retired (Flask v1 at quotes.eq.solutions shut down; replaced by EQ Ops). The 2026-05-19 un-deferral was superseded when EQ Ops was designated as the replacement.

## Brand

EQ Design Brief v1.3 is canonical. Two logo variants only (Blue, White).
Sky #3DA8D8 logo mark, never recoloured. Plus Jakarta Sans (web), Aptos
Display (print). See `rules/brand-eq.md` for full spec.

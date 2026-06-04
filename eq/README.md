---
title: EQ Tier — Index
owner: Royce Milmlow
last_updated: 2026-06-03
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

The complete, authoritative file index lives in the **Files** table below —
single source, kept in step with the folder. (Two `overnight-*-2026-05-21.md`
links previously listed here were dead — the files were never committed — and
have been removed.)

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

Complete index of the EQ tier (rebuilt 2026-06-04 to match the folder). Each
path is fetchable at `…/functions/v1/context/eq/<path>`.

| Path | Purpose |
|---|---|
| `pending.md` | EQ-only to-do list |
| `products.md` | EQ live product status |
| `punch-list-2026-06-02.md` | EQ punch list (2026-06-02) |
| `field/multi-tenancy/plan.md` | EQ Field multi-tenancy plan (active reference) |
| `cards/canonical-migration/plan.md` | EQ Cards §18 close-out — Cards → eq-canonical |
| `canonical-readiness/plan.md` | Canonical layer readiness for Intake/Field/Quotes (EXECUTED 2026-05-20) |
| `canonical-readiness/spine.md` | The trust spine — which app_data tables must stay identical across tenants |
| `canonical-readiness/audit-2026-05-21.md` | Post-S3 honest audit of core.eq.solutions (shipped) |
| `canonical-readiness/audit-existing-tables.md` | Audit of existing eq-canonical tables |
| `identity/IDENTITY-MODEL.md` | Authoritative EQ identity model |
| `identity/worker-credentials-model-2026-05-31.md` | Worker-owned portable credentials model (decided design) |
| `identity/onboarding-portable-identity-2026-06-04.md` | Low-friction onboarding + portable identity (draft/proposed) |
| `identity/PHASE-1F-PLAN.md` | Identity Phase 1F build plan |
| `identity/gate-a-decision-2026-06-03.md` | Gate A — worker auth provisioning decision |
| `design/claude-design-context.md` | Design context for Claude Design / mockups |
| `sprints/2026-05-20-S1-canonical-lockin.md` | Sprint S1 — canonical lock-in (historical) |
| `sprints/2026-05-20-S3-polish-and-audit.md` | Sprint S3 — polish + audit (historical) |
| `changelog/field.md` | EQ Field append-only history |
| `changelog/eq-context.md` | Substrate self-changelog |
| `templates.md` | Forward-pointer — does not exist yet (first EQ template captured here) |

## Killed / deferred (do not reference as live products)

- **EQ Variations** — killed 2026-04-29
- **EQ Compliance / EQ Ops** — killed 2026-04-29
- **EQ Expenses** — demoted to internal SKS tool (no longer an EQ product)
- **AHD** — parked to 2027 (changelog at `/archive/changelog-ahd.md`)

EQ Quotes was deferred 2026-04-29 but un-deferred 2026-05-19 — see
`eq/products.md` and `ops/decisions.md` 2026-05-19 entry. Reinstated as
position 4 in the EQ Shell module-mounting queue.

## Brand

EQ Design Brief v1.3 is canonical. Two logo variants only (Blue, White).
Sky #3DA8D8 logo mark, never recoloured. Plus Jakarta Sans (web), Aptos
Display (print). See `rules/brand-eq.md` for full spec.

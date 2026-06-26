---
title: EQ Tier — Index
owner: Royce Milmlow
last_updated: 2026-06-13
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
- `eq/templates.md` — forward-pointer; file does not exist yet, will be created when the first EQ deliverable template is captured

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
| `pending.md` | EQ-only to-do list |
| `products.md` | EQ live product status |
| `field/multi-tenancy/` | EQ Field MT plan + explainer (active reference) |
| `field/permissions/` | EQ Field role/permission matrix |
| `cards/canonical-migration/plan.md` | EQ Cards §18 close-out (active 2026-05-20) |
| `canonical-readiness/plan.md` | Canonical layer readiness for Intake/Field/Quotes ports (draft 2026-05-20) |
| `changelog/field.md` | EQ Field append-only history |
| `changelog/eq-context.md` | Substrate self-changelog |

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

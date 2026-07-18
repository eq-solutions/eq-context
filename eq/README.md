---
title: EQ Tier — Index
owner: Royce Milmlow
last_updated: 2026-07-16
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
- `eq/templates.md` — forward-pointer; re-checked 2026-07-16, still does not exist — will be created when the first EQ deliverable template is captured

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
| `changelog/*.md` | Per-product changelogs — **known duplication issue**: shell/service/cards each currently have two parallel changelog files (e.g. `changelog/shell.md` vs `changelog/eq-shell.md`), only one of which is kept current. Check both until consolidated; flagged as a follow-up. |

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

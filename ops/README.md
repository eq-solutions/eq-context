---
title: OPS Tier — Index
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Operational support — entities, finance, legal, admin
read_priority: standard
status: live
---

# OPS Tier

Operational support that affects EQ and SKS but isn't either.
Loaded **on explicit request**, not by default — the whole point of
tier separation is that OPS noise doesn't surface during EQ or SKS
build sessions.

Topics: entity register, financial architecture (AHD, Delta cliff, CDC
PSI), tax positions, IP, Webb Financial admin, decisions log.

## OPS substrate map

Every canonical OPS file as a full URL — clickable from `/context/claude`:

- [ops/pending.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/ops/pending.md) — Webb tax, infra blockers, substrate-discipline items
- [ops/entities.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/ops/entities.md) — entity register, bank accounts, registrations, key contacts
- [ops/financial-architecture.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/ops/financial-architecture.md) — AHD design, Delta Elcom cliff, CDC PSI position
- [ops/decisions.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/ops/decisions.md) — append-only decisions log (ADR format) — covers all tiers

## Files

| Path | Purpose |
|---|---|
| `pending.md` | Webb tax, infra blockers, substrate-discipline items |
| `entities.md` | Entity register, bank accounts, registrations, key contacts |
| `decisions.md` | Append-only decisions (ADR format) — covers all tiers |
| `financial-architecture.md` | AHD design, Delta Elcom cliff, CDC PSI position |

## When to load OPS

- Tax / accounting question (Webb Financial work)
- Entity decisions (incorporation, trust, SMSF)
- Trademark / IP work
- Financial architecture review (Delta cliff, AHD)
- Substrate-level concerns (eq-context audit, sync issues)
- Any time `state/entities.md` would have been needed under the old structure

Otherwise, leave OPS out of the load.

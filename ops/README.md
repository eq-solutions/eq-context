---
title: OPS Tier — Index
owner: Royce Milmlow
last_updated: 2026-06-08
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

- [ops/pending.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/pending.md) — Webb tax, infra blockers, substrate-discipline items
- [ops/entities.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/entities.md) — entity register, bank accounts, registrations, key contacts
- [ops/financial-architecture.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/financial-architecture.md) — AHD design, Delta Elcom cliff, CDC PSI position
- [ops/decisions.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/decisions.md) — append-only decisions log (ADR format) — covers all tiers
- [ops/security-register.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/security-register.md) — live security findings register (P0/P1/P2), across all tiers

## Files

| Path | Purpose |
|---|---|
| `pending.md` | Webb tax, infra blockers, substrate-discipline items |
| `entities.md` | Entity register, bank accounts, registrations, key contacts |
| `decisions.md` | Append-only decisions (ADR format) — covers all tiers |
| `financial-architecture.md` | AHD design, Delta Elcom cliff, CDC PSI position |
| `security-register.md` | Live security findings register (P0/P1/P2) — check for open P0s before any cross-tier work |

## When to load OPS

- Tax / accounting question (Webb Financial work)
- Entity decisions (incorporation, trust, SMSF)
- Trademark / IP work
- Financial architecture review (Delta cliff, AHD)
- Substrate-level concerns (eq-context audit, sync issues)
- Any time `state/entities.md` would have been needed under the old structure

Otherwise, leave OPS out of the load.

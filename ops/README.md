---
title: OPS Tier — Index
owner: Royce Milmlow
last_updated: 2026-05-04
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

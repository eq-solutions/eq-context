---
title: Session — Role Step-Up Charters + generator
date: 2026-07-05
tier: SKS
owner: Royce Milmlow
---

# 2026-07-05 — Role Step-Up Charters (promotion charters)

## Built
7 SKS-branded charters (.docx, docx-js): Collin Toohey (Site Foreman), Rhys Scott (Site Supervisor), William Brown (Field Service Supervisor), Simon Bramall (Data Centre Account Manager), Matthew Miller (Data Centre Site Manager), David Boyd (Site Manager), Luke Wheeler (Field Service Manager). New `sks-charters` generator (data-driven, per-person JSON, client-name lint).

## Format decided — "Role Step-Up Charter"
Two-way accountability doc, not a JD. Pairs "what you step up to" with "what SKS commits in return"; dual signature; 30/60/90 checkpoints; EQ voice. Captured in sks/templates.md.

## Lessons
docx-js: forced PageBreak renders a blank page in Word (LibreOffice hides it — Word paginates taller). Fix: no hard breaks; cantSplit:true on table rows.

## Decisions
- Collin's delivered charter retains "BGIS" (real client) — Royce chose to leave that one; generator lint forces placeholders going forward.
- David Boyd — qualification path left generic pending Royce's steer.
- Luke Wheeler — actual promotion is Field Service Manager, superseding the prior "Schneider Account Lead formalise" framing; active.md corrected.

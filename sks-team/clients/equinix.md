---
title: SKS-TEAM — Equinix Client Reference
owner: Royce Milmlow
last_updated: 2026-05-15
scope: Equinix-specific terminology, site codes, and language patterns for SKS NSW Operations documents
read_priority: standard
status: live
audience: SKS NSW Operations team members' AI sessions
---

# Equinix — Client Reference

Apply this knowledge when any document (quote, variation, MOP, scope, email) is for an Equinix site.

---

## Site codes — Australia

| Code | Location |
|---|---|
| SY1 | Sydney — Ultimo |
| SY3 | Sydney — Alexandria |
| SY4 | Sydney — Mascot |
| SY6 | Sydney — Eastern Creek |
| SY7 | Sydney — Eastern Creek (expansion) |
| ME1 | Melbourne — Port Melbourne |
| ME2 | Melbourne — Deer Park |
| PE1 | Perth — Malaga |
| BN1 | Brisbane — Bowen Hills |

Always use the site code + specific location detail in scope documents. E.g. "Equinix SY3, Level 2, Suite 4A" not just "Equinix SY3".

---

## Key terminology

| Term | Meaning |
|---|---|
| IBX | Individual Business Exchange — the facility itself (e.g. "SY3 IBX") |
| CUFT | Customer Fitout — Equinix-managed fitout project for a customer's cage/suite |
| Smart Hands | Equinix on-site technicians (not SKS staff) |
| MMR | Meet-Me Room — interconnection/cross-connect room |
| Cage | Customer's physical space within the data hall |
| Suite | Larger enclosed customer space |
| Cross-connect | Physical cable link between two customer cages or to the MMR |
| PDU | Power Distribution Unit — in-rack power strip |
| Busway / Busbar | Overhead power distribution rail above the data hall |
| BMS | Building Management System — Equinix-managed, SKS does not touch without explicit approval |
| DCIM | Data Centre Infrastructure Management platform |
| Hot aisle / Cold aisle | Airflow management layout — works must maintain containment integrity |

---

## Quote language

**Opening paragraph (use this exact text):**
> Thank you for the opportunity to provide a quotation for the works at [Site Code, e.g. Equinix SY3]. The following proposal sets out our scope, pricing, and clarifications in line with the Equinix MSA.

**Scope references:** Always reference the site code and specific location (level, cage, aisle). E.g.:
> "Supply and install cable containment on Level 2 of Equinix SY3 data hall, Rows 4–6, cold aisle."

**Clarifications to add for Equinix works (in addition to standard baseline):**
- All works to be performed in accordance with Equinix IBX site rules and Smart Hands requirements
- After-hours access window to be confirmed with Equinix Smart Hands prior to works commencing
- SKS to coordinate isolations and system access with Equinix duty engineer

---

## MOP requirements

Equinix requires a MOP to be submitted via the **IBX portal** before any planned works on live infrastructure. Key points:
- Submit MOP via the IBX portal for the relevant site (SY3, SY6, etc.)
- Obtain portal approval reference before works commence
- Reference the portal submission ID in the MOP document
- Emergency contact on site: Equinix Smart Hands duty contact (varies by site — confirm with client contact)
- MOPs must include: pre-work checklist, emergency contacts, rollback procedure, and hold points with client sign-off

---

## Variation language

**Basis of claim — Equinix-instructed variation:**
> Works were instructed by [Equinix Contact Name], [Title], Equinix [Site], on [Date] via [instruction method]. These works fall outside the original scope defined in [Quote Ref].

Note: Equinix Smart Hands cannot instruct variations on SKS's scope — the instruction must come from the Equinix Project Manager or Customer (CUFT customer). If Smart Hands gave the instruction, confirm with the PM before issuing the variation claim.

---

## After-hours

Most live data centre works at Equinix are after-hours (outside standard business hours). When drafting:
- Add to Clarifications: *"Pricing based on after-hours works — [start time] to [end time]. Standard hours pricing available on request."*
- After-hours rates are the user's responsibility to specify — do not apply a rate or multiple.

---

## Key contacts

Not stored here — client contacts change frequently. Ask the user for the relevant Equinix Project Manager or CUFT contact for each job. Do not reference contacts from training data.

---
title: Knowledge — Document Templates
owner: Royce Milmlow
last_updated: 2026-04-15
scope: Standard templates and document formats for SKS and EQ work
read_priority: reference
status: live
---

# Knowledge — Document Templates

Living record of standard document formats. When building a new document,
check here first — don't reinvent.

---

## SKS Quotation Template (v1 — April 2026)

**Format:** A4 .docx, built with docx-js (Node)
**Font:** Arial throughout
**Colour:** SKS Navy #003366 for headers, white text on navy cells
**Footer:** SKS Technologies Pty Ltd | ABN 80 006 455 699 | Page N

**Structure (in order):**

1. **Header** — SKS Technologies / Electrical | Data | Communications, navy rule
2. **Title** — "QUOTATION" centred
3. **Details Table** — 4-column grid:
   - Quotation No / Date
   - Project / Rev
   - Client / Attention
   - Client Ref / Validity (default 30 days)
   - Site / Prepared By
4. **Scope of Works & Pricing Table** — columns: Item | Description | Qty | Unit | Rate | Total
   - Alternating row shading
   - Summary rows: Subtotal (ex GST) / GST / TOTAL (inc GST)
5. **Inclusions** — tick bullet list (✓)
6. **Exclusions** — cross bullet list (✗)
7. **Clarifications & Assumptions** — numbered list
8. **Photo Register** — 2-column table with:
   - Embedded images (room photos, floor plans)
   - Captions below each image
   - Placeholder slots for additional photos
9. **Acceptance Block** — table: Client Name / Signature / Date / Purchase Order No.

**Standard Exclusions (always include unless scope says otherwise):**
- Data cabling (unless specified)
- Builder's work, penetrations, patching
- Ceiling tile removal/reinstatement (by others)
- Asbestos / hazardous materials
- After-hours / weekend work
- Permit to work fees / inductions
- Works not specifically described
- Fire stopping / fire-rated penetrations
- BMS integration / programming

**Standard Clarifications:**
- Pricing based on provided drawings/photos
- Access assumed during standard hours (Mon–Fri 7am–3:30pm)
- Ceiling space access assumed for cable routing
- Final locations confirmed on-site before 1st fix
- All electrical work to AS/NZS 3000:2018
- Valid for 30 days

**First use:** SY5-4 Level 2 FLX61 quote for Erilyan (Sabrina Lowe), 15 April 2026

---

## Client Context Blocks

These are reusable context blocks for the three primary client relationships.
Paste the relevant block at session start when producing documents for that client.

### Equinix Australia
- Sites: SY5 (St Peters), SY6 (Ultimo)
- Submission: Word doc, SKS branded, itemised scope + exclusions
- Terminology: IBX, CUFT, MOP, ITP — always use Equinix terminology
- Change management: Reference IBX site code in subject/title, include revision block
- Contract basis: MSA in place, variations as lump sum unless directed
- Procurement via: Erilyan (contract administrator) — Sabrina Lowe, Daniel Palmer

### Schneider Electric
- Role: Schneider is principal contractor on data centre projects
- Document types: Subcontractor quotes, MOPs/JSAs, commissioning packs, variation claims
- Terminology: Align to Schneider project numbering and WBS structure

### SKS Internal
- Document types: QA packages/ITPs, site safety packs, operational SOPs, training records
- Software: Workbench (job/project management) — never reference SimPRO

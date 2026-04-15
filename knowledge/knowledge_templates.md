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

## SKS Quotation Template (v3 — April 2026)

**Format:** A4 .docx, built with docx-js (Node)
**Font:** Arial throughout
**Brand colour:** SKS Navy #1F335C
**Logo:** White+Text variant from R2 (`SKS_Logo_White_Text_Clean.png`)
**Footer:** SKS Technologies Pty Ltd | ABN 80 006 455 699 | sks.com.au | Page N

**Layout (matches Royce's Word template screenshot):**

1. **Navy banner** — full-width navy cell, "QUOTATION" left (white, 24pt bold), SKS white logo right
2. **Details block** — simple tab-stop label/value lines (NO table borders, NO navy cell backgrounds):
   - Date / Quote Reference / Attention / Project / Scope / Prepared by / Contact
3. **Section headers** — navy left-bar (12pt border) + light grey (#F2F2F2) background cell
4. **Sections (numbered):**
   - **1. Scope of Works** — brief italic paragraph + bullet list of key deliverables
   - **2. Pricing** — 2-column table only (Description + Amount ex GST)
     - Rows: Labour / Materials / Subcontractors-Equipment
     - Summary: Subtotal (grey bg, navy text) / GST / TOTAL (navy bg, white text)
   - **3. Inclusions** — tick bullet list (✓)
   - **4. Exclusions** — cross bullet list (✗)
   - **5. Clarifications** — numbered list
   - **6. Photo Register** — 2-column table, embedded images + captions + placeholder slots
   - **7. Acceptance** — navy label / white value table (Client Name / Signature / Date / PO Number)

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
- Payment terms: 30 days from date of invoice

**Key difference from earlier template versions:**
- v1/v2 used 7 numbered sections with 6-column pricing (Item/Desc/Qty/Labour/Materials/Total),
  navy cell backgrounds on details table, "SKS TECHNOLOGIES | ELECTRICAL QUOTATION" text header,
  and sign-off with estimator left + acceptance right.
- v3 matches the current Word template: simpler 2-column pricing, cleaner details layout,
  navy banner with logo, section headers with left-bar accent.

**First use:** SY5-4 Level 2 FLX61 quote for Erilyan (Sabrina Lowe), 15 April 2026

---

## Client Context Blocks

Reusable context blocks for the three primary client relationships.
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

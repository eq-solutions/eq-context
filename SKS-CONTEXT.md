---
title: SKS Technologies — AI Session Context
owner: Royce Milmlow
last_updated: 2026-04-18
scope: SKS-specific context for AI sessions working on SKS deliverables
read_priority: critical
status: live
---

# SKS Technologies — AI Session Context

---

## Company

**SKS Technologies** is an electrical contractor based in Castle Hill, NSW, specialising in data centre electrical work across Sydney and NSW. Delta Elcom was acquired by SKS in January 2026; the NSW operations sit within SKS under the Delta Elcom integration.

Customer base: major data centre operators and hyperscale clients (referred to in all outputs as "Data Centre Client A", "Tier 1 Client", etc. — never by real name).

---

## My Role

**Royce Milmlow** — NSW Operations Manager. I oversee quoting, project delivery, commercial management, and day-to-day operations for NSW. Report line is to SKS leadership.

---

## Team (NSW)

- Simon Bramall — Project Manager
- Leif Lundberg, Jack Cluff, Federico Sander, Nathan Anderson — Job / Project Managers
- Matthew Miller — Equinix supervisor
- ~55 field staff on the SKS Labour roster
- Mark Brame — Delta Elcom (invoice recipient, Castle Hill)

---

## Active Projects (Apr 2026)

| Project | Status |
|---------|--------|
| AWS SYD053 PDC Acceleration | Live — 20-week programme (soft start 23 Mar 2026, target PC 21 Aug 2026), 3,220+ WHIP installations |
| AirTrunk SYD3 transformer commissioning | Active — 29 × 2250kVA kiosks, ~$1.18M inc GST |
| NEXTDC S3 tender | Tender phase — Artarmon, quantity takeoff from 11 IFT-1 drawings |
| Equinix SY6 CUFT | Active — multi-contractor annual test, two-day programme |
| DigiCo busway/busduct | Active — dispute with head contractor over tap off box quantities. VAR-003 (15 Dec) + Feb parts list are defensive anchors. |
| Equinix SY5 COLO 14 | Testing documentation complete |
| Telstra SLDC emergency lighting | 514 Stanilite NEXUS fittings replacement programme |

---

## Systems & Tools

| Purpose | Tool |
|---------|------|
| Job / project management | **Workbench** (replaced SimPRO; replaced legacy Excel cost tracking) |
| File storage | OneDrive (SKS corporate Microsoft 365) |
| Quoting | Excel estimator + SKS Quote Template v3 (.docx, docx-js) |
| SKS Labour tracking | sks-nsw-labour.netlify.app (internal PWA, Supabase-backed) |
| Endpoint security | ThreatLocker on SKS corporate laptops — blocks Python, .bat, unapproved exes. Tailscale blocked. |

---

## Quoting Workflow

1. **RFQ comes in** — usually email (sometimes .msg), with scope notes + BOQ/attachments.
2. **Scope review** — reference prior similar quotes and estimators for pricing guidance.
3. **Build estimator** — Excel estimator workbook, using prior patterns as a base.
4. **Produce quote document** — SKS Quote Template v3 (.docx) — navy #1F335C banner, Arial, White+Text logo from R2, 2-column pricing table, left-bar section headers. See `knowledge/knowledge_templates.md`.
5. **Assign quote number** — **Manually from Workbench.** This cannot be automated. Hard constraint.
6. **Send to customer** — Reviewed, numbered, and sent by Royce.

Full template specification: `knowledge/knowledge_templates.md` (SKS Quotation Template v3).

---

## Client Conventions

### Equinix Australia
- Sites: SY5, SY6 (and ongoing expansion)
- Terminology: IBX, CUFT, MOP, ITP — always use Equinix terminology
- Procurement via Erilyan (Sabrina Lowe, Daniel Palmer)
- MSA in place; variations as lump sum unless directed

### Schneider Electric
- Principal contractor on data centre projects
- Document types: subcontractor quotes, MOPs/JSAs, commissioning packs, variation claims
- Align to Schneider project numbering and WBS

### DigiCo
- Active dispute — VAR-003 (15 Dec) and Feb parts list are the defensive anchors
- All outputs referencing this project must be reviewed before sending

---

## SKS Brand

| Token | Hex |
|-------|-----|
| Dark Blue | #1F335C |
| Purple | #7C77B9 |
| Slate | #566686 |
| Light | #F0F7F7 |

**Font:** Arial throughout (SKS docs stay Arial — unlike EQ which uses Plus Jakarta Sans / Aptos)

**Logo assets (R2 — sks-assets bucket):**

| File | URL |
|------|-----|
| Colour + Text | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Text_Clean.png` |
| White + Text | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_White_Text_Clean.png` |
| Colour Arrows | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Arrows_Clean.png` |
| White Arrows | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_White_Arrows_Clean.png` |

---

## What AI Should Help With

- Read incoming scope emails and attached XLSX/PDF files — extract scope details, quantities, drawing references.
- Reference prior estimators to suggest labour hours, materials, and pricing based on similar past jobs.
- Draft estimator structure in Excel, pre-populated based on scope, ready for Royce's review.
- Produce quote documents using SKS Quote Template v3 (docx-js).
- Produce project management documents: MOPs, JSAs, ITPs, QA packs, test registers, commissioning documentation, photo registers, variation claims, scope of works.
- Preserve institutional knowledge — surface relevant decisions, rates, and notes from past quotes.
- AI always presents work as a **draft for Royce's review** before anything reaches the customer.

---

## Hard Constraints

- **Quote numbers must be assigned manually from Workbench.** AI must never generate, suggest, or auto-assign.
- **Never use real client names in outputs** — use placeholders.
- **Never touch SKS Labour Supabase (`nspbmirochztcjijmcrx`) unless Royce explicitly says "SKS live".** This is live production data for ~55 staff.
- **All final documents go through Royce before reaching the customer.**
- Never distribute tools that depend on Python, .bat, or .exe — ThreatLocker blocks them. Single-file HTML + Cloudflare Worker is the pattern.

---

## Reference

- Full entity register, brand rules, deployment guardrails: `CLAUDE.md` and `rules/`
- Document templates: `knowledge/knowledge_templates.md`
- SKS Labour App technical detail: `SKS_LABOUR_APP.md` in the sks-nsw-labour repo

---
title: SKS — Active Projects (Rolling)
owner: Royce Milmlow
last_updated: 2026-07-05
scope: Current SKS NSW projects, refreshed when projects start/finish
read_priority: critical
status: live
---

# SKS Active Projects (Rolling)

~55 field NSW staff. Job/project tool: **Workbench**. **Never name real
clients** in outputs — use placeholders ("Data Centre Client A", "Tier 1
Client", "Healthcare Client").

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

## Systems & Tools

| Purpose | Tool |
|---------|------|
| Job / project management | **Workbench** |
| File storage | OneDrive (SKS corporate Microsoft 365) |
| Quoting | Excel estimator + SKS Quote Template v3 (.docx, docx-js) |
| SKS Labour tracking | sks-nsw-labour.netlify.app (internal PWA, Supabase-backed) |
| Endpoint security | ThreatLocker on SKS corporate laptops — blocks Python, .bat, unapproved exes. Tailscale blocked. |

---

## NSW Structural State (updated 2026-06-01)

### Operating reality

- Royce's effective scope is now **State GM-shaped** despite Operations Manager title
- **Richo (Michael Richardson)** now structurally engaged — Dino reports to him,
  giving Richo skin in the NSW game. Monthly cadence with Royce established.
- **Dino Cabal** joined as Comms Growth lead — peer to Royce, reports to Richo.
  Primary risk: sales velocity outpacing delivery bench. Watch the sold→delivered handoff.
- **Scott Hotson** accepted Operations Lead — Client Services. Start date TBC.
  Reports to Royce. First 90 days: diagnose → surface → first plays.
- **Mark Brame** read updated post-dinner: capable of context-appropriate engagement
  when stakes are visible. Default plan still routes around for operational detail.

### People conversations in motion

| Person | Conversation | Owner | Stage |
|---|---|---|---|
| Simon Bramall | Equinix Account Lead formal title + pay | Royce | Charter drafted 2026-07-05 |
| Luke Wheeler | Field Service Manager promotion | Royce | Charter drafted 2026-07-05 |
| Koos Otto | HV Technical Lead role redesign | Royce | Book |
| Leif Lundberg | Senior Comms Advisor reframe | Royce | Book |
| Huon Henne | Comms shadow pairing | Royce | Book |
| Ben Ritchie | PM pathway conversation | Royce | Coffee booked |
| Wayne Rowe | Dignified exit | Mark (Royce supports) | Not started |
| Charlotte White | Project Coordinator scope | Royce | Book |

### Disciplines (NSW)

| Discipline | Key people |
|---|---|
| Electrical | Majority of field + PMs + supervisors |
| Comms | Leif Lundberg, Huon Henne, Jack Cluff, Wayne Rowe (Digico) |
| AV | Michael Zoghbi |

### Rejected patterns (do not re-suggest)

The following were explicitly tested against external AI opinions (Grok + ChatGPT)
and rejected for Royce's context:

- Friday 3:30pm closeout ritual — wrong for electrical ops Fridays
- Daily voice dump on a fixed schedule — rejected, trigger-based preferred
- Microsoft ecosystem purity for capture — iPhone-native (Apple Notes) is correct
- Email windows twice daily — socially unrealistic in ops contracting
- Role-collision frame (EQ vs SKS) — Royce explicitly said EQ is parked, operator mode is priority
- Five-layer operating system — cut to three triggers

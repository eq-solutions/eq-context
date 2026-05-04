---
title: SKS Tier — Index
owner: Royce Milmlow
last_updated: 2026-05-04
scope: SKS Technologies work — operations, projects, team, tools
read_priority: critical
status: live
---

# SKS Tier

Default load when working on any SKS Technologies topic.

**SKS Technologies** is an electrical contractor based in Castle Hill, NSW,
specialising in data centre electrical work across Sydney and NSW. Delta
Elcom was acquired by SKS in January 2026; the NSW operations sit within
SKS under the Delta Elcom integration.

**Royce Milmlow** is NSW Operations Manager — quoting, project delivery,
commercial management, day-to-day NSW operations.

---

## Hard Constraints (SKS-specific)

- **Quote numbers must be assigned manually from Workbench.** AI must
  never generate, suggest, or auto-assign.
- **Never use real client names in outputs** — use placeholders
  ("Data Centre Client A", "Tier 1 Client", "Healthcare Client").
- **Never touch SKS Labour Supabase (`nspbmirochztcjijmcrx`) unless
  explicitly told "SKS live".** Live production data for ~55 staff.
- **All final documents go through Royce before reaching the customer.**
- Never distribute tools that depend on Python, .bat, or .exe —
  ThreatLocker blocks them. Single-file HTML + Cloudflare Worker is
  the pattern.

(See `rules/non-negotiables.md` for full hard rules across both tiers.)

---

## What AI Should Help With

- Read incoming scope emails and attached XLSX/PDF files — extract scope
  details, quantities, drawing references.
- Reference prior estimators to suggest labour hours, materials, and
  pricing based on similar past jobs.
- Draft estimator structure in Excel, pre-populated based on scope, ready
  for Royce's review.
- Produce quote documents using SKS Quote Template v3 (docx-js).
- Produce project management documents: MOPs, JSAs, ITPs, QA packs, test
  registers, commissioning documentation, photo registers, variation
  claims, scope of works.
- Preserve institutional knowledge — surface relevant decisions, rates,
  and notes from past quotes.
- AI always presents work as a **draft for Royce's review** before
  anything reaches the customer.

---

## Files

| Path | Purpose |
|---|---|
| `pending.md` | SKS-only to-do list |
| `active.md` | Rolling active projects (current quarter) |
| `team.md` | NSW team |
| `products.md` | SKS live tools (Labour, Receipt Tracker) |
| `templates.md` | Quote v3 spec + client context blocks |
| `changelog/labour.md` | SKS Labour app history |

## Reference

- Brand spec (palette, fonts, logo URLs): `rules/brand.md`
- Deployment guardrails: `rules/deployment.md`
- Stack defaults: `rules/stack.md`
- SKS Labour App technical detail: `SKS_LABOUR_APP.md` in the
  sks-nsw-labour repo (not this one)

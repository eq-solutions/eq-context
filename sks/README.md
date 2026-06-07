---
title: SKS Tier — Index
owner: Royce Milmlow
last_updated: 2026-06-08
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

## SKS app systems — the split (as of 2026-05-20)

The SKS roster / timesheet / field app runs on **two separate systems** during
the cutover. Do not conflate them:

| | **Standalone — legacy** | **EQ Field · SKS tenant — the focus** |
|---|---|---|
| Site | `sks-nsw-labour.netlify.app` | `core.eq.solutions/field` · `field.sks.eq.solutions` |
| Repo | `eq-solutions/sks-nsw-labour` | `eq-solutions/eq-field` (tenant slug `sks`) |
| Dev status | **FROZEN** — no new features; kept warm/parallel, short-term only | **ACTIVE — all new SKS development happens here** |

- **All new SKS app work goes to the EQ Field SKS tenant** (`eq-field` repo).
  Do **not** build features in the standalone repo, and do **not** port between
  them — the auto-port model was killed at the 2026-05-20 split.
- ⚠️ **Both currently share ONE database** (`nspbmirochztcjijmcrx` = SKS live).
  The per-tenant DB decouple / canonical migration is **not done yet** — so the
  EQ Field SKS tenant's saves still write the same live DB as the standalone.
  Any doc claiming the SKS tenant is on `sks-canonical` / `ehowg` is aspirational;
  it's on `nspb` today. Full verified DB picture:
  `DATA-PLANES-SOURCE-OF-TRUTH.md` (eq-field repo).
- Cutover (repoint the tenant onto its own DB, then decommission the standalone)
  is **Royce-gated — no date set**; the standalone stays warm in the meantime.

---

## SKS substrate map

Every canonical SKS file as a full URL — clickable from `/context/claude`:

- [sks/pending.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks/pending.md) — SKS-only to-do list
- [sks/active.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks/active.md) — rolling active projects (current quarter)
- [sks/templates.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks/templates.md) — Quote v3 spec + client context blocks
- [sks/team.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks/team.md) — NSW team

Separate audience — only fetch when explicitly authoring or reviewing team-facing guidance:

- [sks-team/README.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks-team/README.md)
- [sks-team/quoting.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks-team/quoting.md)

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

- Brand spec (palette, fonts, logo URLs): `rules/brand-sks.md`
- Deployment guardrails: `rules/deployment.md`
- Stack defaults: `rules/stack.md`
- SKS Labour App technical detail: `SKS_LABOUR_APP.md` in the
  sks-nsw-labour repo (not this one)

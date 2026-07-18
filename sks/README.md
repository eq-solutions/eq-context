---
title: SKS Tier — Index
owner: Royce Milmlow
last_updated: 2026-07-16
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
| Dev status | **STILL ACTIVE — retirement intended, date not set** (confirmed 2026-07-16). Receiving real feature work (PR #67 / v3.10.98, 2026-07-15). Don't assume it's frozen. | **ACTIVE — all new SKS development happens here** |

- **New SKS app work goes to the EQ Field SKS tenant** (`eq-field` repo) where possible. The standalone repo is still taking feature work too — it's not yet safe to treat as feature-frozen. Don't port between them — the auto-port model was killed at the 2026-05-20 split.
- ⚠️ **DB cutover is in progress.** Directory data (people, sites, managers) is live on `sks-canonical` / `ehow` (`ehowgjardagevnrluult`). Operational data (schedule, timesheets) is not yet migrated — those tables are empty on ehow. Standalone (`nspb` / `sks-nsw-labour.netlify.app`) is the **eventual retirement target — no date set as of 2026-07-16**, still live and under active development. The `DATA-PLANES-SOURCE-OF-TRUTH.md` in eq-field predates this migration (verified 2026-06-07) and is now stale on the directory migration status.

---

## SKS substrate map

Every canonical SKS file as a full URL — clickable from `/context/claude`:

- [sks/pending.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/pending.md) — SKS-only to-do list
- [sks/active.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/active.md) — rolling active projects (current quarter)
- [sks/templates.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/templates.md) — Quote v3 spec + client context blocks (Royce's own docx-js pipeline — see sks-team/quoting.md for the separate team-facing SharePoint-template pipeline)
- [sks/team.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/team.md) — NSW team
- [sks/products.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/products.md) — SKS app product status
- [sks/brand-kit-tests.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/brand-kit-tests.md) — brand-artefact test log
- [sks/changelog/labour.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/changelog/labour.md) — SKS Labour app changelog

Separate audience — only fetch when explicitly authoring or reviewing team-facing guidance:

- [sks-team/README.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks-team/README.md)
- [sks-team/quoting.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks-team/quoting.md)

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
| `brand-kit-tests.md` | Brand-artefact test log |

## Reference

- Brand spec (palette, fonts, logo URLs): `rules/brand-sks.md`
- Deployment guardrails: `rules/deployment.md`
- Stack defaults: `rules/stack.md`
- SKS Labour App technical detail: `SKS_LABOUR_APP.md` in the
  sks-nsw-labour repo (not this one)

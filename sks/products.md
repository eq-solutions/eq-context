---
title: SKS Tier — Products
owner: Royce Milmlow
last_updated: 2026-07-16
scope: Live SKS internal tools
read_priority: standard
status: live
---

# SKS Tier — Products

Internal tools used by SKS Technologies. Not commercial products — this
is operational tooling for the NSW office.

---

## SKS Labour App — standalone (LEGACY, eventual retirement target)

**Status:** Live and **still receiving real feature work** (confirmed 2026-07-16,
e.g. PR #67 / v3.10.98, 2026-07-15) — not frozen, despite the 2026-05-20 split
intending new SKS app work to target the EQ Field SKS tenant
(`eq-solutions/eq-field`, served at `core.eq.solutions/field` ·
`field.sks.eq.solutions`) instead. Do not port features between them (the
auto-port model was killed at the split). Cutover + decommission is
Royce-gated — **no date set as of 2026-07-16.** See `sks/README.md` →
"SKS app systems — the split".
**URL:** sks-nsw-labour.netlify.app
**Repo:** eq-solutions/sks-nsw-labour — **own dedicated repo since 2026-05-20**, main branch only
**Architecture:** Single-page PWA, vanilla JS (modularised), Supabase
backend, Netlify Functions for PIN auth + email + AI agent
**Supabase project:** nspbmirochztcjijmcrx (sks-labour) — **LIVE
PRODUCTION DATA, DO NOT TOUCH unless "SKS live" is explicit.** ⚠️ The EQ Field
SKS tenant currently shares THIS SAME DB (canonical decouple not done — see
`DATA-PLANES-SOURCE-OF-TRUTH.md` in the eq-field repo).
**Users:** ~55 SKS NSW field staff and supervisors

**Key details:**
- Staff PIN: `2026` (read-only + staff timesheet self-entry)
- Supervisor password: `SKSNSW` (full edit)
- Service worker: network-first for JS/CSS/HTML, cache-first for icons
- Netlify Site ID: bd00e7db-09a4-4f0e-a996-105cd63b0c8b
- SKS tenant org_id: 1eb831f9-aeae-4e57-b49e-9681e8f51e15

**Reference:** see `SKS_LABOUR_APP.md` in the sks-nsw-labour repo for
full technical details.

---

## SKS Receipt Tracker

**Status:** Beta (local / battle-testing)
**Architecture:** Cloudflare Worker + SheetJS + single HTML
**Pending:** Worker deploy, battle-test, broader staff rollout

---

## SKS Field Reports (v29) — **flagged for retirement**

**Status:** Live but on retirement watch — being absorbed into EQ Field's Site Reports module
**URL:** sks-field-reports.netlify.app
**Original author:** Ben Ritchie
**Architecture:** Separate Netlify site; standalone forms for Prestart / Toolbox Talk / Daily Diary / Weekly Site Report

**Retirement plan (Path C — see `ops/decisions.md` 2026-05-13):**
- Workflows being absorbed into EQ Field's Site Reports sub-module (v3.4.69+).
- **Prestart MVP** shipped to EQ Field demo 2026-05-13 (v3.4.69).
- **Toolbox Talk MVP** shipped to EQ Field demo 2026-05-14 (v3.4.75). `toolbox_talks` table on BOTH Supabases.
- **Daily Site Diary MVP** shipped to EQ Field demo 2026-05-13 (v3.4.77). `site_diaries` table on EQ Supabase only — SKS application gated on Royce "SKS live" go.
- **Site Reports HUB** in PR #85 (v3.5.2, not yet merged) — collapses the three sidebar entries into one.
- Weekly Site Report still to come (~6-8 days, premature until one supervisor uses all three current workflows weekly).
- Ben's preview path: `eq-solves-field.netlify.app/?tenant=sks` — SKS branding + SKS Supabase data on the demo build (so submissions land in SKS-labour Supabase tables, not EQ demo).
- This SKS internal tool retires only once EQ Field reaches **parity on all 4 workflows** AND Ben + Royce sign off.
- Collaboration, not replacement — Ben's MVP shapes the EQ implementation; co-author credit / consulting engagement TBD with Webb Financial.

**Pre-retirement housekeeping:**
- Cleanup any test rows Ben writes during trial before sunset:
  - `DELETE FROM prestarts WHERE works_scope LIKE 'Test%' OR created_by = '<test name>';`
  - `DELETE FROM toolbox_talks WHERE topic LIKE 'Test%' OR created_by = '<test name>';`
- Communicate retirement window to SKS supervisors before pulling the plug.

---

## EQ Expenses (internal SKS tool — not an EQ product)

Demoted from EQ product status 2026-04-29. Internal SKS Flask tool only,
not a commercial offering. No active changelog (deleted in 2026-05-04
refactor — start fresh `sks/changelog/expenses.md` if/when next touched).

**Architecture:** Cloudflare Worker proxy (anthropic-proxy) + single index.html
**Key rule:** API key lives in worker env var only — never in frontend

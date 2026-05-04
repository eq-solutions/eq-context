---
title: SKS Tier — Products
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Live SKS internal tools
read_priority: standard
status: live
---

# SKS Tier — Products

Internal tools used by SKS Technologies. Not commercial products — this
is operational tooling for the NSW office.

---

## SKS Labour App (v3.4.3)

**Status:** Live
**URL:** sks-nsw-labour.netlify.app
**Repo:** eq-solutions/eq-field-app, **main branch only**
**Architecture:** Single-page PWA, vanilla JS (modularised), Supabase
backend, Netlify Functions for PIN auth + email + AI agent
**Supabase project:** nspbmirochztcjijmcrx (sks-labour) — **LIVE
PRODUCTION DATA, DO NOT TOUCH unless "SKS live" is explicit**
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

## EQ Expenses (internal SKS tool — not an EQ product)

Demoted from EQ product status 2026-04-29. Internal SKS Flask tool only,
not a commercial offering. No active changelog (deleted in 2026-05-04
refactor — start fresh `sks/changelog/expenses.md` if/when next touched).

**Architecture:** Cloudflare Worker proxy (anthropic-proxy) + single index.html
**Key rule:** API key lives in worker env var only — never in frontend

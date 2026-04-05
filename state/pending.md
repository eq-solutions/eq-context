# State — Pending Actions

Last updated: 2026-04-05

Items are grouped by workstream. Tick off or remove when done.
Add new items at the time they arise — not reconstructed later.

---

## SKS Receipt Tracker
- [ ] Deploy Cloudflare Worker (anthropic-proxy) — follow DEPLOY.md
- [ ] Paste Worker URL into Settings on each test PC
- [ ] Battle-test: receipt scanning accuracy (photo + PDF)
- [ ] Battle-test: weekly Excel export opens cleanly in Excel
- [ ] Battle-test: data survives browser cache clear
- [ ] Share index.html with other SKS staff for broader testing

## EQ Field App
- [ ] Netlify env var cleanup — delete SECRET_SALT, STAFF_HASH, MANAGER_HASH
- [ ] Clear Supabase rate_limits table on demo branch

## EQ Property Solutions / AHD
- [ ] TFN receipt from ATO
- [ ] Correct ABR business activity code to 6711 (residential property operators)
- [ ] Engage solicitor for ISA, MIS Position Paper, EISP sign-off
- [ ] First property acquisition — Adelaide North corridor
- [ ] Government engagement letter (NSW Treasurer) — after first bonus paid

## Tax & Entities (Webb Financial)
- [ ] FY24/25 tax lodgement — personal
- [ ] FY24/25 tax lodgement — CDC Solutions
- [ ] FY24/25 tax lodgement — HHT
- [ ] FY24/25 tax lodgement — MFT / Allcraft
- [ ] Personal vehicle depreciation amendment (~$33,800 refund)
- [ ] Emma FY23/24 ITR amendment (once HHT trust return confirmed lodged)
- [ ] EQ Property Solutions TFN receipt

## EQ Brand & Legal
- [ ] EQ trademark: monitor for publication after 18 August 2026
- [ ] EQ trademark: monitor 2-month opposition period after publication
- [ ] EQ business name renewal — November 2026
- [ ] Milmlow Holdings / MFT / Allcraft review — September 2026

## EQ Solves — Compliance (v1.1)
- [ ] Auto-recurring work orders
- [ ] Multi-site filtering
- [ ] Audit trail

## Context & Infrastructure
- [ ] Connect GitHub MCP to Claude account (Settings → Integrations)
- [ ] Create eq-context repo in eq-solutions org (private)
- [ ] Commit initial eq-context folder structure to repo
- [ ] Confirm Supabase MCP connected and working in chat sessions

---

## Completed (recent)
- [x] SKS Receipt Tracker v2.0 built — single HTML, Cloudflare Worker, SheetJS export (2026-04-05)
- [x] Cloudflare Worker (worker.js) written — generic Anthropic proxy, shared across all apps (2026-04-05)
- [x] eq-context folder structure created — CLAUDE.md + rules/ + state/ + knowledge/ + sessions/ (2026-04-05)
- [x] EQ trademark accepted early by IP Australia (2026-04-01)
- [x] EQ Property Solutions incorporated (2026-03-14)
- [x] EQ business name transferred to CDC Solutions (2026-03-15)

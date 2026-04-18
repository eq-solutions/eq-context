---
title: State — Pending Actions
owner: Royce Milmlow
last_updated: 2026-04-18
scope: Live to-do list across all workstreams; overwrite in place
read_priority: critical
status: live
---

# State — Pending Actions

Items grouped by workstream. Tick off or remove when done.

---

## Infrastructure — Live Blockers

- [ ] **GitHub MCP write access** — 403 on all writes to `milmlow` and `eq-solutions` orgs. Fix at `github.com/settings/installations`. Until resolved, all GitHub writes are manual via browser or Cowork.

## SKS Operations — Infrastructure (HIGH RISK)

- [ ] SKS Labour Supabase backup strategy — no scheduled backups, ~55 staff depend on the app (project: nspbmirochztcjijmcrx)
- [ ] Resend email deliverability issue — unresolved
- [ ] Netlify rollback tagged release for SKS Labour

## SKS Commercial — Live

- [ ] DigiCo busway/busduct dispute — consolidate defensive position (VAR-003 15 Dec + Feb parts list)
- [ ] NEXTDC S3 tender — pricing workbook / submission
- [ ] AirTrunk SYD3 transformer commissioning — documentation pack
- [ ] Equinix SY6 CUFT — programme structure finalisation
- [ ] AWS SYD053 — ongoing WHIP install programme (3,220+)

## SKS Receipt Tracker

- [ ] Deploy Cloudflare Worker (anthropic-proxy) — follow DEPLOY.md
- [ ] Battle-test: receipt scanning, Excel export, data persistence
- [ ] Broader SKS staff testing

## EQ Solves Service — PRIMARY BUILD

- [ ] Resolve GitHub MCP write access (see Infrastructure above) — current blocker
- [ ] Continue sprint cadence (22 sprints to date, 80 Vitest tests)

## EQ Field App

- [ ] Netlify env var cleanup — delete SECRET_SALT, STAFF_HASH, MANAGER_HASH
- [ ] Clear Supabase rate_limits table on demo branch (ktmjmdzqrogauaevbktn)
- [ ] Write fresh Cowork brief for EQ Field (guardrails, demo branch rules)

## EQ Expenses

- [ ] Cloudflare Worker proxy — end-to-end test with real receipt
- [ ] Full EQ branding pass (bugs first)

## EQ GTM — PRIORITY

- [ ] Identify first 5 external paying customers for EQ Field
- [ ] Send outreach message to first target (trade business outside SKS)
- [ ] Build sales motion — stop building features before first external user

## Tax & Entities (Webb Financial)

- [ ] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft
- [ ] Personal vehicle depreciation amendment (~$33,800 refund)
- [ ] Emma FY23/24 ITR amendment
- [ ] EQ Property Solutions TFN receipt

## EQ Brand & Legal

- [ ] EQ trademark: monitor publication after 18 August 2026
- [ ] EQ business name renewal — November 2026
- [ ] Milmlow Holdings / MFT / Allcraft review — September 2026

---

## Parked — Revisit 2027

### Australian Housing Dividend (AHD)

Parked from public-facing materials; revisit for capital activation by 2027. Keep structure warm but not active.

- [ ] TFN receipt from ATO
- [ ] Correct ABR business activity code to 6711
- [ ] Engage solicitor for ISA, MIS Position Paper, EISP sign-off
- [ ] First property acquisition — Adelaide North corridor / SE QLD fallback
- [ ] Government engagement letter (NSW Treasurer) — post first bonus paid

---

## Completed (recent)

- [x] Full context repo audit + rewrite — 2026-04-18
- [x] EQ Design Brief v1.3 published (17 Apr 2026, supersedes v1.2)
- [x] eq-context GitHub Action expanded to sync all subdirs — 2026-04-12
- [x] CLAUDE.md rewritten to reflect current reality — 2026-04-12
- [x] GitHub Action sync confirmed firing correctly — 2026-04
- [x] MD best-practice pass (frontmatter, AGENTS.md, cross-LLM portability) — 2026-04-10
- [x] SKS Labour caching strategy fixed (service worker) — 2026-04-11
- [x] SKS favicon set built (ico, apple-touch, 192, 512) — 2026-04-11
- [x] EQ Expenses offline-first HTML built — 2026-04-09
- [x] Cloudflare Tunnel on Beelink (beelink.eq.solutions) — 2026-04-10
- [x] Google Drive lane decision: EQ → Drive, SKS → OneDrive — 2026-04-09
- [x] Claude use review — 8.5/10, gaps: GTM + MD discipline — 2026-04-12
- [x] EQ trademark accepted by IP Australia — 2026-04-01
- [x] EQ Property Solutions incorporated — 2026-03-14
- [x] Contacts list rebranded Delta Elcom → SKS Technologies (44 staff) — 2026-03/04
- [x] SKS Quote Template v3 built — 2026-04-15

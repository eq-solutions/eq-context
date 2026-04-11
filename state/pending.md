---
title: State — Pending Actions
owner: Royce Milmlow
last_updated: 2026-04-12
scope: Live to-do list across all workstreams; overwrite in place
read_priority: critical
status: live
---

# State — Pending Actions

Items grouped by workstream. Tick off or remove when done.

---

## SKS Operations — Infrastructure (HIGH RISK)
- [ ] Supabase backup strategy — no scheduled backups, 50 staff depend on SKS Labour app
- [ ] Resend email deliverability issue — unresolved
- [ ] Netlify rollback tagged release for SKS Labour

## SKS Receipt Tracker
- [ ] Deploy Cloudflare Worker (anthropic-proxy) — follow DEPLOY.md
- [ ] Battle-test: receipt scanning, Excel export, data persistence
- [ ] Broader SKS staff testing

## EQ Field App
- [ ] Netlify env var cleanup — delete SECRET_SALT, STAFF_HASH, MANAGER_HASH
- [ ] Clear Supabase rate_limits table on demo branch
- [ ] Write fresh Cowork brief for EQ Field (guardrails, demo branch rules)

## EQ Expenses
- [ ] Cloudflare Worker proxy — end-to-end test with real receipt
- [ ] Full EQ branding pass (bugs first)

## EQ GTM — PRIORITY
- [ ] Identify first 5 external paying customers for EQ Field
- [ ] Send outreach message to first target (trade business outside SKS)
- [ ] Build sales motion — stop building features before first external user

## EQ Property Solutions / AHD
- [ ] TFN receipt from ATO
- [ ] Correct ABR business activity code to 6711
- [ ] Engage solicitor for ISA, MIS Position Paper, EISP sign-off
- [ ] First property acquisition — Adelaide North corridor / SE QLD fallback

## Tax & Entities (Webb Financial)
- [ ] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft
- [ ] Personal vehicle depreciation amendment (~$33,800 refund)
- [ ] Emma FY23/24 ITR amendment
- [ ] EQ Property Solutions TFN receipt

## EQ Brand & Legal
- [ ] EQ trademark: monitor publication after 18 August 2026
- [ ] EQ business name renewal — November 2026
- [ ] Milmlow Holdings / MFT / Allcraft review — September 2026

## Context & Infrastructure
- [ ] Confirm GitHub Action fires and syncs sessions/ + state/ correctly after this update
- [ ] Revoke temporary GitHub PATs once MCP confirmed working

---

## Completed (recent)
- [x] eq-context GitHub Action expanded to sync all subdirs — 2026-04-12
- [x] CLAUDE.md rewritten to reflect current reality — 2026-04-12
- [x] MD best-practice pass (frontmatter, AGENTS.md, cross-LLM portability) — 2026-04-10
- [x] SKS Labour caching strategy fixed (service worker) — 2026-04-11
- [x] SKS favicon set built (ico, apple-touch, 192, 512) — 2026-04-11
- [x] EQ Expenses offline-first HTML built — 2026-04-09
- [x] Cloudflare Tunnel on Beelink (beelink.eq.solutions) — 2026-04-10
- [x] Google Drive lane decision: EQ → Drive, SKS → OneDrive — 2026-04-09
- [x] Claude use review — 8.5/10, gaps: GTM + MD discipline — 2026-04-12
- [x] EQ trademark accepted by IP Australia — 2026-04-01
- [x] EQ Property Solutions incorporated — 2026-03-14

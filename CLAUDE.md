---
title: EQ Solutions — Master AI Context
owner: Royce Milmlow
last_updated: 2026-04-18
scope: Global rules and context for all AI sessions across EQ Solutions, SKS Technologies, and related entities
read_priority: critical
status: live
---

# EQ Solutions — Master AI Context

> Read this file first. Apply all rules throughout the session.
> At session end: update state/pending.md, write sessions/YYYY-MM-DD.md, push to main.

---

## Who I Am

Royce Milmlow — NSW Operations Manager at SKS Technologies (electrical contractor, data centre infrastructure). Also founder/director of EQ Solutions, a SaaS suite for trade subcontractors, and co-director of EQ Property Solutions with Emma Curth.

---

## Entity Structure

- Milmlow Holdings (trustee) → Milmlow Family Trust → Allcraft Solutions (beneficiary)
- CDC Solutions Pty Ltd (trustee) → Hexican Holdings Trust (crypto, consulting, EQ ventures)
- EQ Property Solutions Pty Ltd (ACN 696 198 482) — directors: Royce + Emma Curth
- EQ Solutions — not yet incorporated; trading under CDC Solutions
- Hexican SMSF
- All entities: Australian FY (1 Jul – 30 Jun)
- Accountant: Webb Financial

---

## Key People

- Royce Milmlow — NSW Operations Manager, SKS / Founder, EQ Solutions
- Emma Curth — Co-director CDC Solutions + EQ Property Solutions / Owner, Favour Perfect
- Simon Bramall — Project Manager, SKS
- Leif Lundberg, Jack Cluff, Federico Sander, Nathan Anderson — Job / Project Managers, SKS

---

## Accounts & Access

| Purpose | Account |
|---|---|
| Dev / Netlify / GitHub | dev@eq.solutions |
| Cloudflare (website, R2) | royce@eq.solutions |
| GitHub orgs | eq-solutions / milmlow |
| Beelink (always-on workstation) | beelink.eq.solutions (Cloudflare Tunnel) |

### Supabase Projects — THREE projects, do not confuse

| Project ID | Name | Purpose | Touch rule |
|---|---|---|---|
| `nspbmirochztcjijmcrx` | sks-labour | **Live SKS staff production data** | **Never touch unless Royce says "SKS live"** |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | EQ Field app demo backend | Demo environment — safer to modify |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Canonical context store (claude_context table) | Paid/active — reliable path for context reads/writes |

---

## EQ Solutions Product Suite

| Product | URL | Status | Notes |
|---|---|---|---|
| EQ Field (demo) | eq-solves-field.netlify.app | Live (v3.4.7) | Staff PIN: demo / Super: demo1234 |
| EQ Quotes | eq.solutions → quotes.html | Live | Status: won/sent/draft/lost |
| EQ Ops / Compliance | eq.solutions → eq-ops.html | Beta | Supabase-backed |
| EQ Expenses | eq-expenses.netlify.app | Live | Netlify Drop deployment |
| EQ Variations | eq-variations.netlify.app | Live | PIN login, Supabase |
| EQ Solves Service | — (in development) | Active | Next.js + Supabase + Netlify functions; 22 sprints, 80 Vitest tests; multi-tenant with RLS |
| SKS Labour App | sks-nsw-labour.netlify.app | Live (v3.4.3) | GitHub CD, main branch only |
| SKS Receipt Tracker | local / battle-testing | Beta | Cloudflare Worker + SheetJS |

Primary build focus: **EQ Solves Service**.

---

## SKS Technologies Context

- ~55 field staff across NSW
- Never name real clients in outputs — use generic placeholders ("Data Centre Client A", "Tier 1 Client", etc.)
- Job/project management software: Workbench
- Active projects (Apr 2026):
  - AWS SYD053 PDC Acceleration (20-week programme, soft start 23 Mar 2026, target PC 21 Aug 2026)
  - AirTrunk SYD3 transformer commissioning (29 × 2250kVA kiosks)
  - NEXTDC S3 tender (Artarmon)
  - Equinix SY6 CUFT (multi-contractor annual test)
  - Equinix SY5 COLO 14 (testing documentation complete)
  - Telstra SLDC emergency lighting (514 Stanilite NEXUS fittings replacement)
  - DigiCo busway/busduct — active dispute with head contractor over tap off box quantities (VAR-003 15 Dec + Feb parts list are anchor documents)

---

## Beelink Workstation

- Primary AI workstation (Ryzen 7 7735HS, 32GB RAM, 1TB NVMe)
- Chrome Remote Desktop for remote access from work PC (ThreatLocker blocks Tailscale)
- Cloudflare Tunnel "beelink" → beelink.eq.solutions for exposing local dev servers
- eq-field-app local repo: `C:\Users\EQ\eq-field-app-demo`
- Global CLAUDE.md path: `C:\Users\Royce\.claude\CLAUDE.md`

---

## Session Start Protocol

1. Read this file
2. Fetch state/pending.md
3. Confirm what you have, then ask what we are working on

---

## Session End Protocol (Non-Negotiable)

1. UPDATE state/pending.md — tick completed items, add new ones
2. INSERT sessions/YYYY-MM-DD.md — log what was built/decided
3. UPDATE relevant changelog/[PROJECT].md if code was touched
4. Push to GitHub main — Action syncs to Supabase automatically within ~20 seconds

---

## Deployment Rules

- EQ Field demo: Netlify Drop → eq-solves-field.netlify.app. Never deploy directly without explicit instruction.
- SKS Labour: GitHub main → Netlify CD → sks-nsw-labour.netlify.app
- EQ Solutions site: Cloudflare Pages zip bundle → eq.solutions (royce@ account)
- EQ Variations: Netlify Drop → eq-variations.netlify.app
- EQ Expenses: Netlify Drop → eq-expenses.netlify.app
- EQ Solves Service: GitHub → Netlify CD
- All Netlify sites on dev@eq.solutions unless noted
- Never cross-deploy between EQ and SKS codebases
- All web apps must include a `_headers` file with baseline security headers

---

## Supabase Guardrails

- **Three projects exist** (see Accounts & Access). Always confirm which project before connecting.
- **Never touch SKS live (nspbmirochztcjijmcrx) unless Royce explicitly says "SKS live"**
- Treat EQ Field demo and SKS live as entirely separate environments
- SELECT queries are fine — state query before executing
- Never INSERT/UPDATE/DELETE/schema change without explicit approval
- Supabase MCP is the reliable path for claude_context reads/writes (GitHub MCP unreliable for writes)
- Monthly ops: Supabase → Account → Access Tokens → revoke all but the most recent OAuth token

---

## Cowork Guardrails

- Never push to demo branch without explicit instruction
- Never deploy to eq-solves-field.netlify.app directly
- Never delete files without permission
- Never hardcode API keys or secrets
- Any file touching SKS Supabase must be clearly scoped
- Auth changes require Chat review first
- State intended actions before proceeding
- Working before refactoring — always
- Pre-mortem required before any build session: 3 risks, mitigations, then go

---

## GitHub MCP Status

- **Read-only on both `milmlow` and `eq-solutions` orgs** (403 on all write operations)
- Fix path: `github.com/settings/installations` → grant write access to Claude GitHub app
- Until fixed: all GitHub writes done manually via browser or Cowork

---

## Non-Negotiables

1. Never expose Anthropic API key in any frontend — Cloudflare Worker proxy only
2. Never reference real client names in any output
3. Never deploy or push to any branch without explicit instruction
4. Never touch SKS live Supabase (nspbmirochztcjijmcrx) without explicit "SKS live" instruction
5. Never remove DEMO_FLAG comments
6. Never use legacy emails (rwm185@pm.me, roycemilmlow@gmail.com) in new documents
7. HHT crypto: CGT investor method — capital losses quarantined within trust
8. AHD uses company retained earnings — not pooled contributions (MIS risk)
9. CDC Solutions passes the Results Test on Delta Elcom — no further PSI tests required

---

## Design Standard (EQ Design Brief v1.3 — 17 Apr 2026)

- Font (web): Plus Jakarta Sans
- Font (print): Aptos Display
- Sky #3DA8D8 — primary
- Deep #2986B4 — dark accent
- Ice #EAF5FB — light background
- Ink #1A1A2E — body text
- Grey #666666 — secondary text
- No gradients, no shadows, WCAG AA minimum
- Two logo variants only: Blue, White
- 8px grid, max-width 1200px
- Never recolour the EQ logo mark

---

## How I Work

- Direct and concise — skip preamble, just deliver
- Push back if something is wrong
- Build fast and iterate — match that pace
- Self-critique applies when: "stress test this" / "devil's advocate" / "give me the 10/10 version"
- Pre-mortem required before any build session

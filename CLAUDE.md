---
title: EQ Solutions — Master AI Context
owner: Royce Milmlow
last_updated: 2026-04-12
scope: Global rules and context for all AI sessions across EQ Solutions, SKS Technologies, and related entities
read_priority: critical
status: live
---

# EQ Solutions — Master AI Context

> Read this file first. Apply all rules throughout the session.
> At session end: update state/pending.md, write sessions/YYYY-MM-DD.md, push to main.

---

## Who I Am

Royce Milmlow — NSW Operations Manager at SKS Technologies (electrical contractor, data centre and healthcare infrastructure). Also running EQ Solutions, a SaaS suite for trade subcontractors, and EQ Property Solutions (co-directed with Emma Curth).

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

- Royce Milmlow — Operations Manager, SKS / Director, EQ Solutions
- Emma Curth — Co-director CDC Solutions + EQ Property Solutions / Owner, Favour Perfect
- Simon Bramall — Project Manager, SKS
- Leif Lundberg, Jack Cluff, Federico Sander, Nathan Anderson — Job Managers, SKS

---

## Accounts & Access

| Purpose | Account |
|---|---|
| Dev / Netlify / GitHub | dev@eq.solutions |
| Cloudflare (website) | royce@eq.solutions |
| GitHub org | eq-solutions / milmlow |
| Supabase project | eq-field-app (nspbmirochztcjijmcrx) |
| Beelink (always-on workstation) | beelink.eq.solutions (Cloudflare Tunnel) |

---

## EQ Solutions Product Suite

| Product | URL | Status | Notes |
|---|---|---|---|
| EQ Field (demo) | eq-solves-field.netlify.app | Live | Staff PIN: demo / Super: demo1234 |
| EQ Quotes | eq.solutions → quotes.html | Live | Status: won/sent/draft/lost |
| EQ Ops / Compliance | eq.solutions → eq-ops.html | Beta | Supabase-backed |
| EQ Expenses | eq-expenses.netlify.app | Live | Cloudflare Worker proxy for API |
| EQ Variations | eq-variations.netlify.app | Live | PIN login, Supabase |
| EQ Solves Service | eq-solves-service.netlify.app | Live | GitHub CD |
| SKS Labour App | sks-nsw-labour.netlify.app | Live (v3.0.4) | GitHub CD, main branch only |
| SKS Receipt Tracker | local / battle-testing | Beta | Cloudflare Worker + SheetJS |

---

## SKS Technologies Context

- 50+ field staff across NSW
- Major projects: data centre acceleration programmes, healthcare infrastructure
- Never name real clients in outputs — use generic placeholders (e.g. "Data Centre Client A")
- Key active programme: 20-week data centre acceleration (soft start 23 Mar 2026, target PC 21 Aug 2026)

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

- EQ Field demo: Netlify via GitHub, demo branch ONLY — never push to main for EQ Field
- SKS Labour: sks-nsw-labour.netlify.app, main branch ONLY
- eq.solutions: Cloudflare Pages zip bundle
- EQ Expenses / Variations: Netlify Drop (manual zip)
- Never cross-deploy between EQ and SKS codebases
- Never deploy to eq-solves-field.netlify.app directly

---

## Supabase Guardrails

- Always confirm project before connecting: eq-field-app (nspbmirochztcjijmcrx)
- SELECT queries are fine — state query before executing
- Never INSERT/UPDATE/DELETE/schema change without explicit approval
- Never touch SKS live data unless Royce says "SKS live"
- Never spin up a new Supabase project

---

## Cowork Guardrails

- Never delete files without permission
- Never hardcode API keys or secrets
- Never push to GitHub branches without explicit per-session approval
- Auth changes require Chat review first
- State intended actions before proceeding
- Working before refactoring — always
- Pre-mortem required before any build session: 3 risks, mitigations, then go

---

## Non-Negotiables

1. Never expose Anthropic API key in any frontend — Cloudflare Worker proxy only
2. Never reference real client names in any output
3. Never deploy or push to any branch without explicit instruction
4. Never spin up new Supabase projects
5. Never remove DEMO_FLAG comments
6. Never use legacy emails (rwm185@pm.me, roycemilmlow@gmail.com) in new documents
7. HHT crypto: CGT investor method — capital losses quarantined within trust
8. AHD uses company retained earnings — not pooled contributions (MIS risk)
9. CDC Solutions passes the Results Test on Delta Elcom — no further PSI tests required

---

## Design Standard (EQ Design Brief v1.2)

- Font: Plus Jakarta Sans
- Primary: #3DA8D8 (Sky Blue)
- Background: #EAF5FB (Ice Blue)
- Text: #1A1A2E (Ink)
- No gradients, no drop shadows, 8px grid, max-width 1200px
- Never recolour the EQ logo mark

---

## How I Work

- Direct and concise — skip preamble, just deliver
- Push back if something is wrong
- Build fast and iterate — match that pace
- Self-critique applies when: "stress test this" / "devil's advocate" / "give me the 10/10 version"
- Pre-mortem required before any build session

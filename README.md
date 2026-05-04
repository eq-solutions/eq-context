---
title: eq-context — Repository README
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Human-readable entry point for the eq-context repository
read_priority: reference
status: live
---

# eq-context

Private context repository for EQ Solutions, SKS Technologies, and related entities —
used by any LLM assistant (Claude chat, Cowork, Code; Cursor; Codex; Perplexity;
ChatGPT; Gemini; future tools) to maintain continuity across sessions.

**Tier-separated as of 2026-05-04** — `/eq`, `/sks`, `/ops`, `/system`, `/archive`.
Sessions ask "EQ or SKS focus?" at the start so context loads cleanly.

**Entry points:**
- `CLAUDE.md` — master context (Claude Code auto-loads this)
- `AGENTS.md` — equivalent entry point for non-Claude tools
- `COWORK-PROMPT.md` — Cowork session starter (paste at start of each session)
- `system/md-style.md` — style guide for writing or updating any MD in this repo

## How it works

Every assistant conversation that produces new knowledge, decisions, or state changes
ends with "update the MD". The assistant commits only the files that changed, with a
clear commit message describing what was added. A GitHub Action syncs all changed
files to the canonical Supabase context store (`urjhmkhbgaxrofurpbgc`) within
~20 seconds.

## Structure

```
CLAUDE.md                    ← Master index — assistants read this first, always
AGENTS.md                    ← Tool-neutral equivalent entry point
COWORK-PROMPT.md             ← Cowork session starter
README.md                    ← This file (human-focused)

rules/
  non-negotiables.md         ← Hard rules that override everything
  brand.md                   ← Colours, fonts, logo rules (EQ Design Brief v1.3)
  deployment.md              ← Deployment guardrails
  stack.md                   ← Default technology stack

eq/                          ← EQ Solutions tier
  README.md                  ← EQ tier index
  pending.md                 ← EQ-only to-do list
  products.md                ← EQ live products (Field, Service)
  field/
    multi-tenancy/           ← MT plan + explainer (active reference)
    permissions/             ← Role/permission matrix
  changelog/
    field.md                 ← EQ Field history
    eq-context.md            ← Substrate self-changelog

sks/                         ← SKS Technologies tier
  README.md                  ← SKS tier index
  pending.md                 ← SKS-only to-do list
  products.md                ← SKS live products (Labour, Receipt Tracker)
  active.md                  ← Rolling active projects
  team.md                    ← NSW team
  templates.md               ← Quote v3 + client context blocks
  changelog/
    labour.md                ← SKS Labour app history

ops/                         ← Operational support
  README.md                  ← OPS tier index
  pending.md                 ← Webb, infra, substrate-discipline items
  entities.md                ← Entity register, accounts, registrations
  decisions.md               ← Append-only decisions (ADR format)
  financial-architecture.md  ← AHD, Delta cliff, CDC PSI

system/                      ← Substrate itself
  README.md                  ← System tier index
  architecture.md            ← Tech architecture (Cloudflare, Supabase)
  infrastructure.md          ← Project IDs, accounts, Beelink
  lessons.md                 ← Tech gotchas (append-only)
  md-style.md                ← MD writing standard (slimmed)
  onboarding.md              ← First-time tutorial

archive/                     ← Parked or deferred — not loaded by default
  README.md                  ← What's in here and why
  changelog-eq-quotes.md     ← EQ Quotes (deferred 6mo)
  changelog-ahd.md           ← AHD (parked to 2027)

sessions/
  YYYY-MM-DD.md              ← Append-only daily logs
  archive/                   ← Older than 30 days

scripts/
  install-hooks.ps1          ← Pre-commit hook installer

.github/workflows/
  sync-context.yml           ← GitHub → Supabase sync
```

## Update frequency

| File / folder | How often |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | Only when structure or rules change |
| `rules/*` | Rarely — annual review (28 April) |
| `*/pending.md` | Every session in the relevant tier |
| `*/products.md` | When product status changes |
| `ops/entities.md` | When entity/infrastructure changes |
| `system/architecture.md` | When how something is built changes |
| `ops/decisions.md` | Append when a decision is made |
| `system/lessons.md` | Append when a lesson is learned |
| `*/changelog/*.md` | Append when product code is touched |
| `sessions/*` | Every session (new file per ISO date) |
| `archive/*` | Almost never — only on reactivation |

## Never do

- Edit main branch directly for large changes — use a session update workflow
- Delete old session logs — they are the audit trail
- Merge state and rules — they have different update frequencies for a reason
- Cross-pollute tiers — EQ context goes in `/eq`, SKS in `/sks`. Don't mix.
- Reference parked products as live — see CLAUDE.md "Killed / deferred" section

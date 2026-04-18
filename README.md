---
title: eq-context — Repository README
owner: Royce Milmlow
last_updated: 2026-04-18
scope: Human-readable entry point for the eq-context repository
read_priority: reference
status: live
---

# eq-context

Private context repository for EQ Solutions, SKS Technologies, and related entities —
used by any LLM assistant (Claude chat, Cowork, Code; Cursor; Codex; Perplexity;
ChatGPT; Gemini; future tools) to maintain continuity across sessions.

**Entry points:**
- `CLAUDE.md` — master context (Claude Code auto-loads this)
- `AGENTS.md` — equivalent entry point for non-Claude tools
- `AI-RULES.md` — universal AI session rules
- `SKS-CONTEXT.md` — SKS-specific context for SKS deliverables
- `COWORK-PROMPT.md` — Cowork session starter (paste at start of each session)
- `MD_BEST_PRACTICES.md` — style guide for writing or updating any MD in this repo

## How it works

Every assistant conversation that produces new knowledge, decisions, or state changes
ends with "update the MD". The assistant commits only the files that changed, with a
clear commit message describing what was added. A GitHub Action syncs all changed
files to the canonical Supabase context store (`urjhmkhbgaxrofurpbgc`) within
~20 seconds.

## Structure

```
CLAUDE.md                      ← Master index — assistants read this first, always
AGENTS.md                      ← Tool-neutral equivalent entry point
AI-RULES.md                    ← Universal AI session rules
SKS-CONTEXT.md                 ← SKS-specific context
COWORK-PROMPT.md               ← Cowork session starter
MD_BEST_PRACTICES.md           ← Style standard for writing/updating any MD in this repo
rules/
  deployment.md                ← Deployment guardrails, never break these
  brand.md                     ← Colours, fonts, logo rules (EQ Design Brief v1.3 canonical)
  non-negotiables.md           ← Hard rules that override everything
  stack.md                     ← Default technology stack
state/
  products.md                  ← Current status of every product (overwrite in place)
  pending.md                   ← Active to-do list — updated every session
  entities.md                  ← Business entities, accounts, Supabase projects, contacts
knowledge/
  architecture.md              ← Why and how things are built
  decisions.md                 ← Key decisions and reasoning (append only)
  lessons.md                   ← Technical gotchas (append only)
  knowledge_templates.md       ← Reusable document templates (SKS quotes, client blocks)
sessions/
  YYYY-MM-DD.md                ← What happened each session (append only, one per date)
changelog/
  [PROJECT].md                 ← Per-product append-only history
.github/workflows/
  sync-context.yml             ← GitHub → Supabase sync action
```

## Update frequency

| File | How often |
|------|-----------|
| CLAUDE.md | Only when structure or rules change |
| rules/* | Rarely — deliberate decisions only |
| state/pending.md | Every session |
| state/products.md | When product status changes |
| state/entities.md | When entity/infrastructure changes |
| knowledge/architecture.md | When how something is built changes |
| knowledge/decisions.md | Append when a key decision is made |
| knowledge/lessons.md | Append when a new lesson is learned |
| knowledge/knowledge_templates.md | When a document template changes |
| sessions/* | Every session (new file per ISO date) |
| changelog/* | Append when product code is touched |

## Never do

- Edit main branch directly for large changes — use a session update workflow
- Delete old session logs — they are the audit trail
- Merge state and rules — they have different update frequencies for a reason
- Rename existing files — create new + archive old via frontmatter (see MD_BEST_PRACTICES §10)

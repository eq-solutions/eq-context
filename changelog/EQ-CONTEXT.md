---
title: Changelog — EQ Context Repo
owner: Royce Milmlow
last_updated: 2026-04-18
scope: Append-only history of changes to the eq-context repository itself
read_priority: reference
status: live
---

# Changelog — EQ Context Repo

## [2026-04-18] Full Sweep Audit and Rewrite
**Built by:** Royce Milmlow + assistant
**Changes:**
- Supabase section across CLAUDE.md, state/entities.md, rules/deployment.md, rules/non-negotiables.md, knowledge/architecture.md rewritten to reflect three projects (sks-labour live, eq-solves-field demo, eq-solves-service-dev context store) — replaces old "one project" rule
- EQ Design Brief bumped v1.2 → v1.3 in CLAUDE.md; rules/brand.md rewritten around v1.3 (two logo variants, WCAG AA, Aptos Display for print)
- R2 logo URLs (SKS + EQ) captured in rules/brand.md
- SKS active project list added to CLAUDE.md (AWS SYD053, AirTrunk SYD3, NEXTDC S3, Equinix SY6, DigiCo)
- EQ Solves Service promoted to primary build in state/products.md
- AHD moved to Parked status in state/pending.md (revisit 2027)
- GitHub MCP 403 status surfaced as live infrastructure blocker across CLAUDE.md, deployment rules, pending.md
- Beelink workstation spec captured (Ryzen 7 7735HS, 32GB, 1TB NVMe, Chrome Remote Desktop, Cloudflare Tunnel)
- `_headers` security file requirement formalised
- Non-negotiables rule #4 rewritten: "never touch SKS live Supabase" replaces "never spin up new Supabase project"
- Real-client-names rule promoted to non-negotiable
- Two new decision log entries appended (v1.3 adoption, three-project split)
**Status:** Repo rewritten; SKS Labour + EQ Field version numbers pending Royce confirmation before push

## [2026-04-10] MD Best Practices and Cross-LLM Portability Pass
**Built by:** Royce Milmlow + assistant
**Changes:**
- Added `MD_BEST_PRACTICES.md` — cross-LLM style guide (YAML frontmatter, tool-agnostic phrasing, ISO dates, token budgets, Perplexity-specific guidance)
- Added `AGENTS.md` at repo root as a tool-neutral entry point alongside `CLAUDE.md`
- YAML frontmatter added to every MD file in the repo
- Replaced `Claude (Anthropic)` with `assistant` across changelogs for tool-neutrality
- Stripped expired `claude.ai/chat/...` session URLs from changelog entries
- Split responsibility between `knowledge/architecture.md` (what is built) and `knowledge/decisions.md` (why it was chosen)
- Bumped `last_updated` to 2026-04-10 across all files
**Status:** Repo conforms to MD_BEST_PRACTICES v1.0

## [2026-04-06] Live Context System - GitHub MCP Setup
**Session:** Cowork session
**Built by:** Royce Milmlow + assistant
**Changes:**
- GitHub PAT generated for Claude Desktop
- MCP config created for Claude Desktop Chat mode
- CLAUDE.md updated with Live Context Rule
- Changelog folder created and backfilled from session history
- Repo cloned to Beelink at C:\Users\EQ\eq-context
**Status:** Cowork pushing via git, Chat mode MCP pending verification

## [2026-04-05] MD System Built
**Built by:** Royce Milmlow + assistant
**Changes:**
- eq-context folder structure created (CLAUDE.md + rules/ + state/ + knowledge/)
- Four Claude projects created with MD files uploaded
- GLOBAL_CLAUDE.md placed on Beelink
- Self-critique prompts baked into global instructions
**Status:** System live - GitHub auto-sync was pending

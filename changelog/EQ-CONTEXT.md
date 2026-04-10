---
title: Changelog — EQ Context Repo
owner: Royce Milmlow
last_updated: 2026-04-10
scope: Append-only history of changes to the eq-context repository itself
read_priority: reference
status: live
---

# Changelog — EQ Context Repo

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

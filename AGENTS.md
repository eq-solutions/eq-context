---
title: AGENTS.md — Entry Point for Any LLM Tool
owner: Royce Milmlow
last_updated: 2026-04-10
scope: All assistants (Claude, Cursor, Codex, Perplexity, ChatGPT, Gemini, any future tool)
read_priority: critical
status: live
---

# AGENTS.md

This repository (`eq-context`) is the single source of truth for all EQ
Solutions, SKS Technologies, and related-entity project context.

Any assistant starting a session in this repo should read files in this
order:

1. `CLAUDE.md` — global rules and guardrails (tool-neutral despite the
   filename; retained so Claude Code auto-loads it).
2. `state/pending.md` — what's currently outstanding.
3. `changelog/[PROJECT].md` — the changelog for whichever project the
   current task touches.
4. `MD_BEST_PRACTICES.md` — the style standard for writing or updating
   any file in this repo.

Then confirm context before taking any action.

`CLAUDE.md` and `AGENTS.md` are equivalent entry points — same rules
apply regardless of which tool is loading the session.

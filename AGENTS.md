---
title: AGENTS.md — Entry Point for Any LLM Tool
owner: Royce Milmlow
last_updated: 2026-05-04
scope: All assistants (Claude, Cursor, Codex, Perplexity, ChatGPT, Gemini, any future tool)
read_priority: critical
status: live
---

# AGENTS.md

This repository (`eq-context`) is the single source of truth for all EQ
Solutions, SKS Technologies, and related-entity project context.

The repo is **tier-separated**: `/eq`, `/sks`, `/ops`, `/system`, `/archive`.
Default loads are tier-specific to avoid cross-contamination.

Any assistant starting a session in this repo should read files in this order:

0. `system/onboarding.md` — first-time read only. Skip if you've worked in
   this repo before. ~5 minute walkthrough.
1. `CLAUDE.md` — global rules and guardrails (tool-neutral despite the
   filename; retained so Claude Code auto-loads it).
2. **Ask: "EQ session or SKS session?"** before loading further context.
3. Load tier defaults:
   - EQ → `eq/README.md` + `eq/pending.md`
   - SKS → `sks/README.md` + `sks/pending.md` + `sks/active.md`
   - OPS work → `ops/` files only when explicitly relevant
4. `system/md-style.md` — the style standard for writing or updating
   any file in this repo.

Then confirm context before taking any action.

## Working principle — finish what you start

Every recommendation, suggestion, or pending action surfaced during a
session must be either completed before session close or explicitly
deferred to the relevant tier's `pending.md` with a date. Half-applied
work is the failure mode this principle prevents — see
`rules/non-negotiables.md` §0 (Session Discipline).

`CLAUDE.md` and `AGENTS.md` are equivalent entry points — same rules
apply regardless of which tool is loading the session.

## Asking questions

**Universal rule, no exceptions:** every question to Royce must have
pre-populated answer options. Never open-ended. Applies across all chats,
consoles, sessions, projects, and tools. He restated this multiple times
and treats violations as a real friction point.

**Two valid renderings — prefer the first when the tool is loaded:**

1. **Clickable cards** — the AskUserQuestion tool. 1–4 questions per call,
   2–4 options each. Lead with the recommended option suffixed
   `(Recommended)`. Don't include an "Other" option — the tool auto-adds
   one.

2. **Inline numbered text (fallback)** — when AskUserQuestion isn't
   loaded:

   ```
   **[Question]**

   1. (recommended) <option A — one line>
   2. <option B — one line>
   3. <option C — one line>
   4. Free text — describe what you want

   Reply with `1`, `2`, `3`, or free text.
   ```

**Hard rules:**
- Recommended option always first.
- One line per option — reasoning lives above the list, not in the bullets.
- ALWAYS include a free-text fallback so the multiple-choice doesn't trap
  him.
- Use this even for binary yes/no.
- Use this even for "what should we name this?" — suggest 2–3 names plus
  free text.
- NEVER ask "what would you like to do?" / "how should I approach this?"
  without pre-populating options.

**Always explain before you ask.** For any technical, strategic, or
non-trivial decision, write a short briefing in the chat *before* the
question. The briefing covers: what the question means in plain language,
what's true today and why we're choosing, what each option implies in
practice, what you recommend and why. The clickable options are the
*summary* of that briefing, not a substitute for it.

Pattern: **chat text first** (context + reasoning + recommendation), then
the question (the tickable summary). Never invert this.

**The only acceptable exception:** statements continuing the user's
instruction, not actual questions. ("I'm doing X" is fine; "Should I do
X?" needs options.)

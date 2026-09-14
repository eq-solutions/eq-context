---
title: Claude Cowork — Session Starter
owner: Royce Milmlow
last_updated: 2026-09-14
scope: Paste-in bootstrap prompt for Cowork sessions — pointer to CLAUDE.md, no separate rules
read_priority: reference
status: live
---

# Claude Cowork — Session Starter

Paste everything below this line into Cowork at the start of a session.

---

## SESSION START

Read this file in full from disk as your complete behavioural contract for this session:

`C:\Projects\eq-context\CLAUDE.md`

**Read it from the local clone, never `raw.githubusercontent.com`.** That URL is CDN-cached and has served this exact file 8+ days stale with a 200 OK and no error — invisible unless you already know the answer. Reading from disk is the only mechanism that can't silently lie. If the file looks like it might be out of date (references something you know has since changed), say so and ask me to run `git pull` in that folder before you proceed — you can't run git yourself in the Cowork sandbox.

**Write access:** Cowork has filesystem write access to the local clone, governed by `pre_tool_use.py`'s guardrails (200-line edit block, NUL-fill scan on `C:\Projects` writes) — and, as of 2026-09-14, confirmed GitHub MCP write access straight to `main`, which those guardrails don't cover (see `ops/security-register.md` SEC-78). Treat an MCP-mediated write with the same caution as an ungated `git push`: fine for routine, reviewed substrate updates; confirm with Royce first for anything else.

Follow every instruction in `CLAUDE.md` exactly. It contains the session-start sequence, the tier question, the tone rules, the question-asking rules, the templates-first rule, the hard rules that override everything, the Cowork-specific sandbox rules (§11), and the session-end protocol.

Confirm you've read it by summarising the contract in one sentence, plus the file's `last_updated` date. Then start at Step 3 of the session-start sequence (the tier question).

That's it. Everything else lives in `CLAUDE.md` — no separate Cowork rules to track.

---
title: Chat Bootstrap Prompt
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Paste at the start of every Claude Chat (claude.ai) session. Replaces the old Supabase context cache approach (retired 2026-06-22).
read_priority: reference
status: live
---

# Chat Bootstrap Prompt

Paste the block below as your first message in a new Claude Chat session.

---

```
Fetch and read: https://raw.githubusercontent.com/eq-solutions/eq-context/main/CLAUDE.md

Follow §1 exactly. Notes before you start:

1. Context source is GitHub raw URLs only. The Supabase context cache
   (project eq-solves-service-dev / table context_files) was deleted
   2026-06-22. Never fetch context from a Supabase URL.

2. After I answer the tier question, also fetch:
   https://raw.githubusercontent.com/eq-solutions/eq-context/main/digest.md
   Lead with anything in the "Needs you" section before asking what
   we're working on.

3. Before any build task, run the session gate (CLAUDE.md Rule 0.6):
   - Show me digest.md "Needs you" and "Pulse" sections
   - Fetch system/worktree-registry.md and list active worktrees for the target repo
   - Ask me to paste: git -C C:\Projects\<repo> branch -a && git status
   - State the brief: what exists / what's broken / what changes / constraints
   - Wait for my confirmation before writing anything

4. At session end, run §10 close protocol:
   - List what was built, decided, deferred
   - Draft the sessions/YYYY-MM-DD.md entry
   - Show me the exact pending.md changes needed
   - Output git commands for me to run — you cannot push from Chat
```

---

## What this replaces

The old approach fetched context from a Supabase edge function at `eq-solves-service-dev`. That project was deleted 2026-06-22. GitHub raw URLs are CDN-backed and token-free — no sync step needed.

## What Chat can't do (vs Claude Code)

| | Claude Code | Chat |
|---|---|---|
| brief-gate enforcement | ✅ guard.js blocks | ✗ — paste step 3 manually |
| /brief skill | ✅ | ✗ — described in step 3 above |
| /close skill | ✅ | ✗ — described in step 4 above |
| git push | ✅ | ✗ — outputs commands for you to run |

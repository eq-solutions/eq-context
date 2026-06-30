---
title: Cowork Bootstrap Prompt
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Paste at the start of every Cowork session. Replaces the old Supabase context cache approach (retired 2026-06-22).
read_priority: reference
status: live
---

# Cowork Bootstrap Prompt

Paste the block below as your first message (or system prompt) in a new Cowork session.

---

```
Fetch and follow: https://raw.githubusercontent.com/eq-solutions/eq-context/main/CLAUDE.md

Context source: GitHub raw URLs only. The Supabase context cache
(project eq-solves-service-dev / table context_files) was deleted
2026-06-22. Never fetch context from a Supabase URL.

Session gate — run before any Edit/Write:
- Fetch digest.md and system/worktree-registry.md from GitHub
- Ask me to paste: git -C C:\Projects\<repo> branch -a && git status
- State the brief (what exists / what's broken / what changes / constraints)
- Wait for my confirmation before writing anything

Session close — run at end:
- Draft the pending.md changes (show me the diff)
- Draft sessions/YYYY-MM-DD.md entry
- Output ALL git commands as a single .bat file for me to run on the host
- NEVER run git directly from the Cowork sandbox against C:\Projects\*
  — it creates orphan .git/index.lock files that require manual cleanup
```

---

## Git constraint (Cowork-specific)

Cowork runs in a sandbox. Running `git` against `C:\Projects\*` from inside Cowork creates lock files that corrupt the repo state. Always emit a `.bat` or `.ps1` file for Royce to run on the host machine instead.

Claude Code on the Beelink can run git directly — this constraint is Cowork-only.

## What this replaces

The old approach fetched context from a Supabase edge function at `eq-solves-service-dev`. That project was deleted 2026-06-22.

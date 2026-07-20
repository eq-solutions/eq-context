---
title: Task Brief Template
owner: Royce Milmlow
last_updated: 2026-07-20
scope: Copy-paste template for Claude session handoffs — fill from live system, not docs
read_priority: critical
status: live
---

# Task Brief Template

Copy this block at the start of any non-trivial handoff to Claude.
Do not fill from memory or docs — verify each field against the live system first.

---

## Task Brief

**What exists** *(run `list_tables` / `git branch -a` / check deployed state before filling)*

<!-- Describe the current state as it actually is — tables, functions, components, branches -->

**What's broken or missing**

<!-- The specific gap — not "auth is broken" but "the OTP hook in eq-shell/src/auth/otp.ts doesn't close on success" -->

**What changes**

<!-- Scope to file / function / table level. Tighter = fewer correction rounds. -->

**Constraints**

<!-- Things not to touch, must-maintain compatibility, auth/deploy rules, entity separation (EQ ↔ SKS) -->

---

## Checklist before handing off

- [ ] Verified against live Supabase (not the state snapshot)
- [ ] Checked `git branch -a` — no in-flight branch already doing this
- [ ] Checked `eq-context/system/worktree-registry.md` if parallel work is involved
- [ ] Scope is tight enough that Claude won't need to guess

---

*Reference: Rule 0.6 in `C:\Projects\CLAUDE.md` · Worktree registry: `eq-context/system/worktree-registry.md`*

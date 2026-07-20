---
title: SYSTEM — Auto-PR Scope (the leash)
owner: Royce Milmlow
last_updated: 2026-07-20
scope: What an automated fix-finding agent may touch, what it may never touch, and what it must always do. Machine-read by hooks/auto_pr_guard.py — this file IS the enforced boundary, not a description of one.
read_priority: critical
status: live
---

# Auto-PR Scope — the leash

This is the boundary from the 2026-07-20 "self-improving substrate" conversation
(`sessions/2026-07-20.md`, session 9). The steelman for automation that finds and
fixes its own drift was real. The counter-argument was also real: if the same
model deciding what to fix also decides whether the fix is safe to land, that's
the model grading its own homework on exactly the judgment most likely to be
wrong. So the boundary lives here, outside the acting model, enforced by
`hooks/auto_pr_guard.py` — a hook, not a prompt instruction. A rogue or
mistaken agent run cannot write outside this file's `ALLOW` list or push to
`main` even if it decides to, the same way `pre_tool_use.py` makes truncation
physically impossible rather than merely discouraged.

**This file cannot expand itself.** It is in its own `DENY` list. Any change to
scope requires a normal human-reviewed PR, same as everything else here — the
leash cannot lengthen itself.

## The three rules, unconditionally

1. **Allowlist, not denylist.** A path must match `ALLOW` to be touched at all.
   `DENY` exists for defense-in-depth on the highest-stakes files, not as the
   primary gate — if it's not in `ALLOW`, it's already blocked by default.
2. **Every auto-PR carries a test that fails before the fix and passes after.**
   Not "CI didn't break" — a specific, added-or-modified assertion that would
   have caught the exact bug being fixed. "Nothing broke" is not evidence of
   anything; a red-then-green test is.
3. **Never merges. Never pushes to `main`. Never force-pushes.** Opens a PR and
   stops. A human — Royce, or a session he's driving — makes every landing
   decision, same as the classifier already blocks self-merge on PRs today.
   This automation extends that existing guardrail; it does not route around it.

## Scope, first pass — deliberately narrow

Chosen after the 2026-07-20 conversation: wider than "docs and CI labels only,"
narrower than "generated-content scripts + everything else." Expand later, by
track record, the same way hooks get promoted in `system/failures.md` — never
by argument alone, including the argument in this paragraph.

```
ALLOW:
.github/scripts/**/*.py
archive/**
system/lessons.md
*.md

DENY:
CLAUDE.md
AGENTS.md
CHAT-PROMPT.md
COWORK-PROMPT.md
README.md
system/auto-pr-scope.md
hooks/**
supabase/migrations/**
ops/security-register.md
ops/entities.md
ops/financial-architecture.md
eq/pending.md
sks/pending.md
sks/active.md
ops/pending.md
digest.md
suite-state.md
system/TODAY.md
.github/workflows/**
```

**Why `*.md` and not `archive/**` alone:** the first-pass scope only let an
agent write *into* `archive/` — it never covered deleting the *source* file at
root, which is what an actual "move a root file into archive" task requires
(`git mv`/`rm` on the root copy). Found by trying to dogfood the original
scope on 2026-07-20 and having it correctly block the very task it was meant
to enable. `*.md` (single star — matches root-level files only, never crosses
a `/`, so `eq/pending.md` and friends are untouched) widens ALLOW to cover
that source deletion, with the highest-stakes root `.md` files pulled back out
via explicit DENY below.

**Why each exclusion, briefly:**
- `CLAUDE.md`/`AGENTS.md`/`CHAT-PROMPT.md`/`COWORK-PROMPT.md`/`README.md` —
  the behavioral contract plus the repo's own front door. "Never allowed to
  write in the farmer's ink" (`system/substrate-plan-v2.md`'s own fable). Full
  human review, always, no exception path.
- `hooks/**` — this is the enforcement layer. A bug in a self-proposed hook
  change could weaken the guard protecting everything else. Too meta for a
  first pass; revisit only after the narrower scope has a real track record.
- `supabase/migrations/**`, the security register, entities, financial
  architecture — live-system or business-judgment content. Never mechanical.
- `eq/pending.md`, `sks/pending.md`, `sks/active.md`, `ops/pending.md` — high
  collision risk (edited by concurrent sessions constantly, see
  `system/lessons.md` "concurrent writer") and require contextual judgment
  about what's actually done, not pattern-matching. `archive/**` is the safer
  analogous target for the file-sprawl problem instead.
- `digest.md`, `suite-state.md`, `system/TODAY.md` — generated output or
  live-verified facts, not source. Fixing generator bugs belongs in
  `.github/scripts/**`; the generated files themselves are never hand-edited.
- `.github/workflows/**` — Actions permissions/secrets/triggers live here.
  Field-level inspection (allow a label fix, deny a `permissions:` change)
  is a real future improvement, not built yet — excluded wholesale until it is.

## How this gets used

`hooks/auto_pr_guard.py` only activates when `EQ_AUTO_PR_MODE=1` is set —
normal interactive Claude Code sessions are unaffected. No scheduled or
automated run against this repo exists yet as of 2026-07-20; this file and its
guard are the leash, built and tested *before* anything is put on it, not after.

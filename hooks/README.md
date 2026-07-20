---
title: hooks — rung 4 guards (enforcement layer)
owner: Royce Milmlow
last_updated: 2026-07-12
scope: What the pre_tool_use and session_start hooks enforce, why fail-closed, how to install and test them
read_priority: standard
status: live
---

# hooks/ — rung 4. Prevention, not documentation.

These are the guards that cannot be forgotten. They live **here**, in the governed,
versioned, CI-checked repo — not in a `.claude/` folder outside version control.
`settings.template.json` is a **thin pointer**; it contains wiring and no facts.

| Hook | Rung | Kills |
|---|---|---|
| `session_start.py` | 4 | **F1** — stale substrate read (8–12d, 200 OK, no error). Prints freshness, Needs-you, goals status, and any guard overdue for promotion. Reads the **local clone, never a URL** — the URL is what lied. |
| `pre_tool_use.py` | 4 | **F2 / F6** — Edit/Write silently truncating (F2) and `>>` append NUL-filling (F6) long files on the virtiofs mount. Also blocks `git` from the Cowork sandbox (orphan `index.lock`). **Fail-closed.** Linux-sandbox-scoped; no-ops on Windows (on the Beelink `guard.js` is the active write-guard). |
| `session_end.py` | 4 | Section 10 (Session End Protocol) sitting at rung 1 — an agent had to *remember* to commit, push, and log the session, the exact "read it and still didn't fire" failure class F2 already proved doesn't hold. Reports dirty tree / unpushed main / a day with commits but no `sessions/<date>.md`. **Fail-open, loud** — informational only, never blocks Stop (no destroyed data at stake to justify fail-closed, and a Stop hook that traps someone mid-exit is its own Loop of Despair). Built 2026-07-20, ahead of a recorded ledger entry — see `system/failures.md` note before treating it as a normal rung-2→4 promotion. |
| `auto_pr_guard.py` | 4 | The leash for a future auto-PR-finding agent (2026-07-20 "self-improving substrate" conversation, `sessions/2026-07-20.md` session 9). Only active when `EQ_AUTO_PR_MODE=1` — inert for normal interactive sessions. Enforces `system/auto-pr-scope.md`'s ALLOW/DENY list (default-deny; the scope file cannot expand itself, it's in its own DENY list), and unconditionally blocks pushing to main, merging a PR, or force-pushing regardless of what the scope file says. **Fail-closed** on any parse error or missing scope file — a guard that can't find its own leash does not get to decide it's off it. No scheduled/automated run exists yet; this is the guardrail built and tested *before* anything runs under it. |

## Install (Beelink)

The freshness gate must load for **every** session — not only ones launched at the
`C:\Projects` umbrella root. Wire `session_start.py` in **user** settings so it is global:

- Add the `SessionStart` pointer from `settings.template.json` to
  **`C:\Users\EQ\.claude\settings.json`** (user scope — applies to every repo + worktree).

Installing only at `C:\Projects\.claude\settings.json` fires the gate **solely** for
sessions started at the umbrella root; repo-scoped and worktree sessions never see it.
That gap was live until 2026-07-12 — the gate existed but silently did not run for most
sessions, the exact "guard that isn't wired" failure class the ladder exists to kill.

Then start a fresh session — the gate prints before the tier question.

`session_end.py` needs the same user-scope `Stop` wiring (the block is already in
`settings.template.json` — copy it across the same way). Until that copy happens it
exists only in the governed repo, not in force: check `C:\Users\EQ\.claude\settings.json`
against the template before assuming it's live.

## Why fail-closed

The first version of `pre_tool_use.py` returned 0 lines for a path it couldn't resolve,
so a 308-line Edit sailed straight through. **It failed open, silently** — the exact bug
class the hook exists to kill. Caught only because the adversarial suite tested it.

**A guard that fails open without saying so is worse than no guard**: it produces the
feeling of safety and none of it. If we cannot prove a write is safe, we block. The cost
of a false block is one heredoc. The cost of a false allow is a destroyed file that
reports success.

## Testing

Run the adversarial suite before trusting any change to these files:

```bash
bash hooks/adversarial_test.sh
```

Every failure that ever escapes in real life gets **added to the suite**. The system's own
history becomes its test corpus. That is the part that compounds.

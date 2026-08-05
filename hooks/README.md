---
title: hooks — rung 4 guards (enforcement layer)
owner: Royce Milmlow
last_updated: 2026-08-05
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
| `session_start.py` | 4 | **F1** — stale substrate read (8–12d, 200 OK, no error). Prints freshness, Needs-you, goals status, any guard overdue for promotion, and (2026-08-05) **core.hooksPath resolution** — flags F10, three distinct mechanisms that all produced the identical "pre-commit silently doesn't run" symptom (2026-05-24 wrong directory, 2026-08-04 shadow copy at `.git/hooks` via F8, 2026-08-05 a `--worktree` override shadowing a correct `--local` value). Warn-only, not a block — F10 itself stays at rung 1 until something actually prevents the wrong value from taking effect. Reads the **local clone, never a URL** — the URL is what lied. |
| `pre_tool_use.py` | 4 | **F2 / F6 / F7 / F9** — Edit/Write silently truncating (F2) and `>>` append NUL-filling (F6) long files on the virtiofs mount; a git merge/stash-pop round-trip NUL-filling a file by some other means (F7, 2026-07-31); concurrent-session git races corrupting the shared eq-context checkout (F9, 2026-08-04) — bare `git commit` sweeping up another session's staged files, and rebase/merge/pull racing on HEAD/index/refs. Also blocks `git` from the Cowork sandbox (orphan `index.lock`). **Fail-closed.** F2/F6/the git-lock block are Linux-sandbox-scoped; no-ops on Windows (on the Beelink `guard.js` is the active write-guard for those — though as of 2026-07-31 `guard.js` still carries no NUL-byte logic of its own, see `system/failures.md` → F7 for the open question that leaves). **F7 and F9's own checks are NOT sandbox-scoped** — they run on any platform ahead of any Bash/PowerShell git verb (F9 additionally scoped to the ONE shared checkout by exact path, so the private clone it recommends as the fix is never itself blocked). Tool matching widened to `Bash` + `PowerShell` throughout (previously `Bash`-only). |
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

`pre_tool_use.py` carried the identical gap from the day it was written — wired
only at `C:\Projects\.claude\settings.json` (root scope), never moved. It stayed
invisible for months because most of its checks (F2/F6/the git-lock block) are
Linux-sandbox-only and no-op on Windows regardless of wiring — until F7's
NUL-scan (2026-07-31) and F9's shared-checkout checks (2026-08-04) shipped as
the first checks here deliberately **not** sandbox-gated, meant to run on every
Beelink session no matter where it launched. F9 recurred within 24h (2026-08-05,
commit `2104668`, a session launched inside a worktree — `system/failures.md` →
F9, recurrence 4) before anyone moved the wiring. Fixed 2026-08-05:
`pre_tool_use.py` now runs from **`C:\Users\EQ\.claude\settings.json`** too,
alongside `guard.js`, matcher widened to include `PowerShell` (root scope's own
matcher never had it — a second, smaller case of the same "the code supports
it, the wiring lagged" pattern). `C:\Projects\.claude\settings.json` now wires
nothing — see its own `_comment`. `settings.template.json` corrected to match.

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
python hooks/adversarial_test.py
```

CI-authoritative (`.github/workflows/adversarial-suite.yml`) and the fuller suite —
also covers `session_end.py` and `auto_pr_guard.py`, whose fixtures don't translate
cleanly to bash. `hooks/adversarial_test.sh` covers `pre_tool_use.py` + the
`session_start.py` gate only, in bash, for a quick check with no Python fixtures:

```bash
bash hooks/adversarial_test.sh
```

Both must pass before trusting a change here. (2026-08-05: `adversarial_test.sh` was
briefly deleted, then restored the same day — see `eq/pending.md` for the full story,
including the reasoning for keeping it and a testing bug the restore itself caught.)

Every failure that ever escapes in real life gets **added to the suite**. The system's own
history becomes its test corpus. That is the part that compounds.

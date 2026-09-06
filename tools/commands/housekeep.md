---
title: "/housekeep command backup — End-of-session housekeeping"
owner: Royce Milmlow
last_updated: 2026-09-06
scope: Durability backup of Royce's user-level Claude Code /housekeep command — source of truth is ~/.claude/commands/housekeep.md, not this file
read_priority: reference
status: live
---

End-of-session housekeeping. Run all steps in order. Be thorough — this is the last thing that happens before the session closes.

**Standing rule: fix, don't flag.** If you find something broken or stale during housekeep, fix it in this session. Only use `spawn_task` for things that are genuinely out of scope (production deploys, auth flow changes, cross-entity actions, decisions only Royce can make). Everything else — uncommitted files, stale CLAUDE.md entries, orphaned worktree directories, memory drift — gets fixed now.

The test: if you'd write "you may want to..." or "worth noting...", that's a flag. Rewrite it as an action instead.

---

## 1. Session summary
Produce a concise bullet list of everything done this session: decisions made, code shipped, DB changes applied, issues fixed. Be specific (commit SHAs, migration numbers, RPC names). This becomes the handoff note for the next session.

## 2. Memory — update
For every meaningful thing that happened this session:
- Create or update the relevant detail `.md` file in `C:\Users\EQ\.claude\projects\<current-project>\memory\`
- Update `MEMORY.md` index so the entry reflects current reality
- If a memory entry is now stale or superseded by this session's work, correct it
- Use the `consolidate-memory` skill to merge duplicates and prune stale entries

## 3. Tasks — clean up
- Mark any completed work as `completed`
- Delete tasks that are no longer relevant
- If new follow-on work was identified this session, create tasks for it now so nothing falls through

## 4. Repo health — check ALL key repos (not just ones touched this session)

Run the following for **each** of: `eq-shell`, `eq-field`, `eq-solves-service`, `eq-cards`, `eq-context`:

```
git -C <path> branch --show-current   # MUST be main — if not, switch it
git -C <path> status --short          # MUST be clean — if not, commit or stash
git -C <path> log --oneline -3        # confirm commits look right
git -C <path> log --oneline "origin/main..HEAD"  # any unpushed commits?
```

**If the checkout is on a stale feature branch:** check if the PR is merged (`gh pr view <branch>`). If merged, `git checkout main && git pull`. If still open, leave it and note in handoff.

**If there are uncommitted changes:** commit them (don't leave orphaned edits — they get included in unrelated future commits). A change sitting in the working tree is not tracked; it will bite the next session.

**If there are unpushed commits on main:** push them.

**Worktree check (eq-shell + eq-field only):**
Run `git worktree list` and cross-check against the active worktree table in `C:\Projects\CLAUDE.md`. For each worktree:
- If the branch is merged and the PR is closed: `git worktree remove --force <path>` (or robocopy-empty + manual delete for Windows MAX_PATH).
- If locked by another process: create a self-deleting `.ps1` cleanup script alongside the repo — do NOT leave a bare "delete manually" comment.

## 5. Substrate health — verify the live system
Check the things we touched are actually working:

**Supabase (eq-canonical `jvknxcmbtrfnxfrwfimn`):**
- Run a quick smoke query on any tables or RPCs changed this session to confirm they exist and respond correctly
- Check for any failed migrations: `SELECT * FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 5`

**Deploys:**
- Check CI/deploy status via `gh run list --repo <repo> --limit 3` for each touched repo
- Flag if a deploy is still in-progress or failed

**Other MCP substrate (Sentry, PostHog, Netlify):**
- Only check if something was changed there this session

## 6. CLAUDE.md / context files — fix drift

**PR status reconciliation (always run this):**
For each repo in scope, run:
```
gh pr list --repo eq-solutions/<repo> --state open --json number,title,headRefName
```
Cross-check against the open PR entries in `C:\Projects\CLAUDE.md`. For any PR listed as OPEN in CLAUDE.md that is actually merged or closed: update CLAUDE.md to reflect the merged state (add the merge commit SHA). For any PR not listed in CLAUDE.md that is genuinely open: add it.

**Worktree table in CLAUDE.md:**
Update the "eq-shell main checkout" block and "Active locked worktrees" table to reflect current reality. If a worktree was removed this session, delete its row.

**General drift:**
If anything else discovered this session contradicts or is missing from `CLAUDE.md`, the project `CLAUDE.md`, or `eq-context/`:
- **Fix it now** — edit the file directly. Drift compounds; leaving it for next session makes the next session wrong.
- Only defer if the fix requires a decision you can't make (business logic, auth changes, cross-entity actions).

## 7. Handoff
End with a single "Next session starts here" block:
- Current branch and commit SHA for each key repo
- Any open PRs with their status
- The single most important thing to pick up next
- Any time-sensitive items (expiring tokens, pending deploys, open decisions)

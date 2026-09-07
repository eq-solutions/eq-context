---
title: Worktree Registry
owner: Royce Milmlow
last_updated: 2026-09-07
scope: Active and stale git worktrees — check before creating a new one
read_priority: critical
status: live
---

# Worktree Registry

Agents MUST add a row to Active before creating a worktree.
Check this file first — if your target repo/area is already claimed, coordinate before starting.

**Protocol:**
1. Read this file before any `git worktree add`
2. Add your row to Active (folder, branch, session ID or agent name, date)
3. When done: delete the row (or move to Stale if unmerged-but-idle), then log
   what happened in `system/worktree-registry-archive.md` -- not here. This
   file stays Active/Stale only.
4. Never edit a worktree that isn't yours (see Rule in `C:\Projects\CLAUDE.md`)

**Root cause of the eq-solves-service shared-checkout collisions (found + fixed 2026-07-23):**
A real linked git worktree has its own `.git` FILE at its root (a ~70-byte gitdir
pointer — e.g. `.claude/worktrees/eqsvc-loadtime-ux/.git`). Two paths under
eq-solves-service's `.claude/worktrees/` — `asset-import-export-1fe110` and
`unruffled-noyce-657c65` — turned out to have **no `.git` of their own at all**.
They were never created via `git worktree add`; they're plain nested folders.
Any git command run from inside one silently walks up to the **parent repo's**
`.git` and mutates its shared branch/working tree — which is exactly how two
concurrent sessions each believing they're isolated collided (one session's
uncommitted edit appearing in another's `git status`, the checked-out branch
changing mid-task). `unruffled-noyce-657c65` holds nothing (empty `.claude`
dir only) and is safe to delete whenever someone has `rm -rf` permission —
this session's classifier blocked the delete. `asset-import-export-1fe110`
similarly holds no files of its own (just `.claude`/`.next`) — the actual
uncommitted work sessions have found "in" it lives in the **root checkout**
(`C:\Projects\eq-solves-service`), not the subfolder. **Fix shipped:** `~/.claude/hooks/guard.js`
now has a `detect-fake-worktree` rule (rules 1b/1c) that force-blocks any Edit/Write
OR git-touching Bash/PowerShell command whose (effective) path matches
`/worktrees/<name>/` or `<name>-wt/` but whose root has no `.git` — tested
against both known-fake dirs (blocks) and two real worktrees, one of each path
shape (passes clean). **Extended 2026-08-05 (rule 1c)** to also cover
Bash/PowerShell — the original rule (1b) only ever fired on Edit/Write, so a
`git commit`/`git rebase`/etc. run directly from inside one of these sailed
through unchecked until then; 1c resolves the command's effective cwd the same
way `pre_tool_use.py`'s F9 check and this file's own rule 9 already do (tracks
an in-command `cd`/`-C`, doesn't trust `data.cwd` alone). Non-git shell
commands and `git worktree add` itself stay unblocked, so fixing a path is
never gated. **This does not retroactively fix the two
existing fake folders** — it only stops future silent edits into them (or any
new ones like them) from mutating the wrong checkout. If a session gets
assigned one of these two paths, treat it as: work is actually happening in
the root `eq-solves-service` checkout, verify `git status`/`git branch` there
before editing, or spin up a real worktree elsewhere instead.

---

## Active (do not touch)

`C:\Projects\eq-field\.claude\worktrees\documents-to-sign-feature-3035a3 (eq-field)` | `claude/apprentices-tab-security-603749` (folder name is now stale — was detached HEAD when first logged) | re-checked live minutes after first being logged here, already reclaimed by another session for unrelated work | 2026-08-28 | **NOT TOUCHED** — no longer the mystery-commit case originally flagged (that HEAD is gone, replaced by real work on a real branch). Ordinary active work now, same as the two rows below — logged here only because this file's own age-out sweep hasn't run yet.

`C:\Projects\eq-field\.claude\worktrees\site-contact-mapping-fix (eq-field)` | `claude/site-contact-mapping-fix` | found live during the same audit (owning session unknown) — clean tree, branch has since taken a further commit | 2026-08-28 | **NOT TOUCHED** — [PR #821](https://github.com/eq-solutions/eq-field/pull/821) OPEN, not merged (v3.5.592 — site contact info silently dead since v3.5.551). Active work.

`C:\Projects\eq-field\.claude\worktrees\supervisor-list-population-9e6715 (eq-field)` | `claude/roster-project-code-picker` (was `claude/multi-project-site-display-1483e9` / PR #822 when first logged — branch has since moved on) | found live during the same audit (owning session unknown) — clean tree | 2026-08-28 | **NOT TOUCHED** — still reads as live work closing the Field-side half of the `site_projects` wiring gap already on record (Core built the read+write UI, zero Field code consumed it originally).


`C:\Projects\eq-shell-join-tenant-ratelimit (eq-shell)` | `claude/join-tenant-rate-limit` | session b2e0fcec-2328-4eed-88f1-4900baf6ea21 — adding rate-limiting to shell-join-tenant.ts (no throttle on this self-serve registration endpoint, unlike its shell-login-phone-otp.ts sibling); same root-checkout collision as the row above (root was mid-use by a concurrent session on `claude/entity-view-gate-crm-read-rpcs`), hence a sibling worktree instead of working in root | 2026-09-01 | active — will move to Stale (or delete the row + worktree) once the PR is open and reviewed.

---

## Stale (verify branch merged before pruning)

_None currently._

---

## Pruning a stale worktree

```powershell
# Verify branch is merged before deleting
git -C C:\Projects\eq-shell branch --merged main | Select-String "branch-name"

# Remove worktree (from the repo root, not the worktree folder)
# Note: git worktree remove errors with "Filename too long" on deep Windows paths.
# Fallback: remove git ref manually then robocopy-empty the directory.
$empty = "$env:TEMP\empty_rob"; New-Item -ItemType Directory $empty -Force | Out-Null
robocopy $empty "C:\Projects\<folder>" /MIR /NFL /NDL /NJH /NJS /NP
Remove-Item "C:\Projects\<folder>" -Recurse -Force
```

---

**Full pruning history:** `system/worktree-registry-archive.md`. **Budget:**
this file should stay under ~150 lines -- if it's bigger, history is leaking
back in; check Protocol step 3 above is being followed.

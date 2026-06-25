---
title: Worktree Registry
owner: Royce Milmlow
last_updated: 2026-06-25
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
3. When done: move row to Stale or delete it
4. Never edit a worktree that isn't yours (see Rule in `C:\Projects\CLAUDE.md`)

---

## Active (do not touch)

| Folder | Branch | Agent / Session | Claimed | Status |
|--------|--------|-----------------|---------|--------|
| .claude/worktrees/wf_f1c4afc6-761-4 | claude/d33a-icon-rail-d51-ui | workflow agent | 2026-06-07 | locked |
| .claude/worktrees/agent-a3e8cad7de9a023fc | claude/quality-polish-shell | agent | 2026-06-07 | locked |
| .claude/worktrees/agent-a15dd68d59734b633 | worktree-agent-a15dd68d59734b633 | agent | 2026-06-07 | locked |

---

## Stale (verify branch merged before pruning)

| Folder | Branch | Agent / Session | Notes |
|--------|--------|-----------------|-------|
| .claude/worktrees/magical-bouman-3bd9c9 | main | housekeep session 2026-06-25 | Active session worktree (main branch). Can be removed after Claude Code closes. |
| .claude/worktrees/elastic-meninsky-efd6a1 | claude/elastic-meninsky-efd6a1 | unknown agent | No open PR. Unlocked but Permission Denied on remove — file lock held. Run `cleanup-stale-worktrees.ps1` in eq-shell root after closing Claude Code. |

---

## Recently pruned (2026-06-25)

15 orphaned local branches (no physical worktree dirs) deleted 2026-06-25:

| Branch | Notes |
|--------|-------|
| worktree-agent-a07832911731d680f | orphaned git ref only; dir never existed or already gone |
| worktree-agent-a0ff1a79e00f10b44 | orphaned git ref only |
| worktree-agent-a1016b614c561791a | orphaned git ref only |
| worktree-agent-a1e0b26c21febd3e5 | orphaned git ref only |
| worktree-agent-a22abb40f8237438a | orphaned git ref only |
| worktree-agent-a317aa6661a5f7c28 | orphaned git ref only |
| worktree-agent-a31895260dee4ab1b | orphaned git ref only |
| worktree-agent-a3e8cad7de9a023fc | orphaned git ref only |
| worktree-agent-a84649015a012d2a5 | orphaned git ref only |
| worktree-wf_f1c4afc6-761-4 | orphaned git ref only (worktree is on claude/d33a-icon-rail-d51-ui) |
| worktree-wf_0dccb7b6-553-6 | ref re-deleted (was listed as pruned 2026-06-22 but ref survived) |
| worktree-wf_0dccb7b6-553-8 | ref re-deleted (same as above) |
| worktree-agent-a1505563b4d31152d | ref re-deleted (was listed as pruned 2026-06-22 but ref survived) |
| worktree-agent-a4618efa0ee02cddc | ref re-deleted (same as above) |
| worktree-agent-ac706c691af65192a | ref re-deleted (same as above) |

## Recently pruned (2026-06-22)

The following worktrees were confirmed merged and removed:

| Folder | Branch | PR |
|--------|--------|----|
| .claude/worktrees/priceless-galileo-4131c2 | fix/sks-contact-links-pk | merged to main |
| .claude/worktrees/loving-blackburn-0b7cba | claude/worker-invite-email | PR #436 merged |
| .claude/worktrees/wf_0dccb7b6-553-6 | claude/polish-sentry-fixes | PR #394 merged |
| .claude/worktrees/wf_0dccb7b6-553-8 | claude/polish-admin-pages | PR #395 merged |
| eq-shell-intake-wt | claude/ui-1.5.0 | merged to main |
| eq-shell-button-wt | claude/eq-ui-shell-button | already gone |
| eq-shell-cleanup-wt | claude/b2-b6-b10-cleanup | already gone |
| eq-shell-w2-wt | claude/s2-shell-wave2 | already gone |
| eq-shell-ocr-wt | claude/ocr-parse-auth-gate | already gone |
| .claude/worktrees/jovial-hamilton-68009e | orphaned (2026-06-18) | git ref removed; dir removed 2026-06-22 |
| .claude/worktrees/vigilant-haslett-5bbbfb | orphaned (2026-06-16) | git ref removed; dir removed 2026-06-22 |

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

*Last updated: 2026-06-22*

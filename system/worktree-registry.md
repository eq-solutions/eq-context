---
title: Worktree Registry
owner: Royce Milmlow
last_updated: 2026-07-04
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
| C:\Projects\eqsvc-retire-wt (eq-solves-service) | chore/retire-offsite-backup | Claude (issue #60 — retire eq-service backup.yml, superseded by eq-context) | 2026-07-04 | DONE — eq-service PR #438 MERGED; worktree + branch pruned |
| .claude/worktrees/tenant-hard-delete (eq-shell) | claude/tenant-hard-delete | Claude (Tenants page — hard-delete archived tenants) | 2026-07-04 | DONE — PR #642 MERGED `b7e87ad`, deployed + verified live; dir removable |
| .claude/worktrees/provision-stuck-cancel (eq-shell) | claude/provision-stuck-cancel | Claude (Tenants page — cancel/clear a stuck data-plane provisioning job) | 2026-07-04 | DONE — PR #641 MERGED (rebased on top of the concurrent hard-delete PR #642); dir removed |
| .claude/worktrees/tenant-page-admin-actions (eq-shell) | claude/provision-tenant-background-fn | Claude (fix: provision-tenant 504 — convert to background fn) | 2026-07-03 | DONE — PR #627 MERGED 09:47:09Z; dir removable |
| .claude/worktrees/dreamy-meninsky-7082ba (eq-shell) | claude/dreamy-meninsky-7082ba | STALE ROW — dir was reused by another session (now on claude/field-nomination-views-security-invoker); this row no longer describes its contents | 2026-07-03 | reused — do not trust folder name |
| .claude/worktrees/provision-identity (eq-cards) | claude/provision-identity | Claude (chip task_28defc38, Cards provision name/email) | 2026-07-03 | DONE — PR #118 open; dir removable after merge |
| .claude/worktrees/quote-pdf-fix (eq-shell) | claude/quote-pdf-fix | Claude (chip task_d40bcb24, Ops PDF export) | 2026-07-03 | DONE — PR #615 open; dir removable after merge |
| .claude/worktrees/ops-site-create-edit (eq-shell) | claude/ops-site-create-edit | Claude (Ops site create/edit session a81fe5c3) | 2026-07-03 | DONE — PR #616 open; dir removable after merge |
| .claude/worktrees/objective-pike-977d2a (eq-cards) | claude/fix-onboarding-flags-and-ocr-signal | Claude (eq-cards session, phone-dedup + UI polish + onboarding-flag fix) | 2026-07-09 | ACTIVE — found this dir's reflog carrying unrelated branches (worker-identity-track-b, notify-connection-name, share-licence-comment) from a concurrent session sharing the same folder; re-based own work onto a fresh branch off origin/main to avoid collision. Flagging for visibility — this folder is NOT exclusively this session's. |
| C:\Projects\eq-field-roster-save-fix (eq-field) | claude/roster-save-409-fix | Claude (port SKS roster save 409 self-heal fix to EQ Field — SKS v3.10.88) | 2026-07-10 | DONE — PR #423 MERGED (v3.5.272); root C:\Projects\eq-field checkout had unrelated uncommitted work (scripts/audit.js, scripts/supabase.js audit-revert canon patching) from another session, so used a fresh worktree off origin/main instead of touching root; dir removable |

---

## Stale (verify branch merged before pruning)

| Folder | Branch | Agent / Session | Notes |
|--------|--------|-----------------|-------|
| C:\Projects\eq-intake-ledger-wt | claude/ledger-checksum-stamp | Claude (quality-guardian session) | Work done, pushed, eq-intake PR #58 open. Worktree removal was classifier-blocked — safe to `git -C C:\Projects\eq-intake worktree remove ..\eq-intake-ledger-wt` after merge. |

---

## Recently pruned (2026-06-30)

Branch audit + prune: 166 local + 96 remote merged/redundant branches deleted (215→49 local). 5 orphaned worktree dirs removed + `git worktree prune`. Only `clever-wilson-161a7a` remains registered.

| Folder | Branch | Notes |
|--------|--------|-------|
| .claude/worktrees/sharp-gauss-e31cdd (eq-shell) | claude/sharp-gauss-e31cdd | **Stale Active row — branch actually merged via PR #549 + #553 (2026-06-30).** Dir held only vendored eq-intake/node_modules, no unique work. Branch deleted; directory removed 2026-06-30. |
| .claude/worktrees/determined-gauss-626b33 (eq-shell) | — | Empty husk (8K), no .git link, no matching branch. Directory removed 2026-06-30. |
| .claude/worktrees/eager-elion-6ebfcb (eq-shell) | — | Empty husk (8K), no .git link, no matching branch. Directory removed 2026-06-30. |
| .claude/worktrees/wonderful-dubinsky-41d96f (eq-shell) | claude/wonderful-dubinsky-41d96f | Empty husk (8K); **branch KEPT (active, unmerged)** — commits safe in object store, dir was just leftover. Directory removed 2026-06-30. |
| .claude/worktrees/determined-edison-d6f176 (eq-shell) | — | Re-appeared empty husk (8K); previously listed pruned 2026-06-28. Directory removed 2026-06-30. |

---

## Recently pruned (2026-06-28)

| Folder | Branch | Notes |
|--------|--------|-------|
| .claude/worktrees/determined-edison-d6f176 (eq-shell) | determined-edison-d6f176 | Emptied 2026-06-28 robocopy; directory removed 2026-06-28 housekeep |
| .claude/worktrees/sharp-kapitsa-93278c (eq-field) | claude/sharp-kapitsa-93278c | Emptied 2026-06-28 robocopy; directory removed 2026-06-28 housekeep |
| .claude/worktrees/objective-khorana-7248db (eq-shell) | claude/objective-khorana-7248db | PR #510 merged; directory removed 2026-06-28 housekeep |

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

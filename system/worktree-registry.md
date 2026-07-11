---
title: Worktree Registry
owner: Royce Milmlow
last_updated: 2026-07-11
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
| C:\Projects\eq-shell-cpledger-wt (eq-shell) | claude/tombstone-cross-plane-migrations | Claude (foreman: control-plane ledger + follow-ups) | 2026-07-11 | DONE — #729 (ledger doc) MERGED; 2026_06_27b revoke APPLIED to live jvkn (verified true→false); #730 (tombstone 3 cross-plane files) MERGED `b952ecb`. Worktree + local branch pruned 2026-07-11. (eq-field net #438 worktree also already pruned.) |
| C:\Projects\eq-shell-perf-tier1-wt (eq-shell) | claude/perf-cold-open-tier1 | Claude (foreman: nav-speed Tier 1) | 2026-07-11 | ACTIVE — **PR #740 OPEN** (immutable `/assets/*` cache + gate/sample analytics to cut the ~3.2s cold-open). tsc -b + vite build + eslint green. Branch = Netlify preview only; NO production deploy until Royce merges. Worktree kept (may reuse for Tier 2). |
| .claude/worktrees/sks-comms-resource-mgmt-7563e2 (eq-shell) | claude/comms-fortnight | Claude (NSW Comms Moves 1 / 1.5 / 2b / 2c / 3 / 4 / 5) | 2026-07-10 | ALL 7 MERGED: Move 1 #727 (d7e7787, 0169+153-job backfill live); 1.5+2b #731 (7013d34, filters + crew-booking→schedule_entries); 2c #738 (6a51784, fortnight capacity grid); 3 #741 (39ef617, roster=single crew source); 4 #742 (b4e9829, fortnight job agenda); **5 #744 MERGED (squash `9838993`) — comms-crew tag (0170 + is_crew + ManageCrew picker)**; 0170 APPLIED to ehow 02:05Z (table live, RLS-on/0-policy). **6 #747 MERGED (squash `03a723f`) — fortnight declutter (hide idle rows + this-week default).** ✅ **Staff-dedupe merge DONE + VERIFIED** (Royce's go): 16 Cards stub rows retired, 19 licences + 2 timesheets repointed, 2 logins moved → picker now 93/93/0 dupes. Reversal snapshot in transcript. Root-cause (Cards match-on-onboard) still open → task chip. Next: NV1-as-licence, cutover. |
| C:\Projects\eq-field-boot-overlay-wt (eq-field) | claude/field-boot-overlay-strand | Claude (fix stuck "Loading…" spinner — initApp() overlay stranding: guard 6 secondary loaders + finally-guaranteed hide + early isLeave() fallback) | 2026-07-10 | ✅ DONE — PR #435 MERGED (squash b0bc2c7, v3.5.284; rebased over #434 which took 3.5.283). Worktree + local/remote branch removed. |
| .claude/worktrees/contacts-segment-columns (eq-field) | claude/field-handoff-selfheal | Claude (dir reused after contacts PR #430 merged — Field handoff self-heal: silent-restore 'accepted' posts + REQUEST_SHELL_TOKEN boot recovery) | 2026-07-10 | DONE — PR #431 MERGED (v3.5.280), verified live on field.eq.solutions. Dir still checked out on the merged branch (harmless); removable. |
| .claude/worktrees/field-handoff-recovery (eq-shell) | claude/field-handoff-recovery | Claude (Shell twin: booted-no-hash grace window + one-shot auto-remint in FieldIframe.tsx) | 2026-07-10 | DONE — PR #718 MERGED (main c08ad61), CI green, Netlify auto-deploy. Worktree dir + branch removed. Follow-up nit: task_0ccec6e4 (restore-failed message reachability). |
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
| C:\Projects\eq-field-pipeline-pagination-wt (eq-field) | claude/pipeline-pagination-fix | Claude (paginate sks-pipeline.js/sks-pipeline-resource.js tender_enrichment/nominations/pending_schedule/tender_phases — same v3.10.91 pattern as SKS PR #58) | 2026-07-10 | DONE — PR #427 open (v3.5.276); root C:\Projects\eq-field checkout again has unrelated uncommitted work (scripts/audit.js, scripts/sks-pipeline.js) from another concurrent session, used a fresh worktree off origin/main instead; dir removable after merge |
| .claude/worktrees/contacts-segment-columns (eq-field) | claude/contacts-segment-columns | Claude (Contacts segment-aware columns: registry refactor + per-Group defaults + columns picker) | 2026-07-10 | DONE — PR #430 MERGED (v3.5.279; re-stamped twice — 277+278 taken by concurrent releases #428/#429 mid-review), verified live on field.eq.solutions; branch deleted; dir removable. Root-checkout collision note: a concurrent session committed onto this branch via the shared root checkout before the worktree isolated it — pattern is recurring (3rd time today), consider making worktrees mandatory for eq-field. |
| C:\Projects\eq-field-bootperf (eq-field) — REMOVED | claude/field-boot-perf (merged) | Claude (foreman: per-app nav-speed — Field boot) | 2026-07-11 | DONE — **PR #452 MERGED** (squash `8d3eca6`, v3.5.296) → field.eq.solutions deploying. JSZip idle-load + index.html `no-store`→`no-cache` + print.css media="print" + jvkn preconnect. Worktree + local branch removed 2026-07-11. |
| C:\Projects\eq-svc-bootperf (eq-solves-service) — REMOVED | claude/service-boot-perf (merged) | Claude (foreman: per-app nav-speed — Service boot) | 2026-07-11 | DONE — **PR #494 MERGED** (squash `356d743`) → Service deploying. Lazy-load posthog-js off the critical bundle + Sentry `bundleSizeOptimizations`. Merged with the known-flaky integration test red — `tsc + next build` passed (CLAUDE.md fact #6). Worktree + local branch removed 2026-07-11. |

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

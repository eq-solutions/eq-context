---
title: Worktree Registry
owner: Royce Milmlow
last_updated: 2026-07-12
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
| ~~C:\Projects\eq-intake-mergepanel-wt (eq-intake)~~ REMOVED | claude/mergepanel-demo-ui (merged, deleted) | Claude (wire MergePanel Preview/Confirm UI into IntakeHealthHome — library layer was already merged via PRs #67-71, only the demo UI wiring was missing) | 2026-07-16 | DONE — **PR [#72](https://github.com/eq-solutions/eq-solves-intake/pull/72) MERGED** (squash `937d9dd` → eq-solves-intake main, Royce's go after demo click-through). Worktree + branch pruned. |
| ~~C:\Projects\eq-shell-tenant-drift-wt (eq-shell)~~ REMOVED | fix/tenant-drift-resilience (merged, deleted) | Claude (harden check-tenant-drift.mjs against one unreachable tenant killing the required gate for every PR) | 2026-07-16 | DONE — **PR [#878](https://github.com/eq-solutions/eq-shell/pull/878) MERGED** (squash `37b805a` → main) → core.eq.solutions auto-deploying. `fingerprint()`'s per-tenant Management API call is now caught individually instead of throwing uncaught out of `mapWithConcurrency`; only errors matching a known dead-project signature are treated as informational "unreachable" (a real SQL/schema bug on a live tenant still fails loud) — muster (single lens, codex-rescue unavailable) flagged both the blanket-catch risk and an inconsistent `--reference`-to-dead-tenant hard-fail, both fixed before merge. Root eq-shell checkout was mid-collision with a concurrent session (branch had switched to `chore/remove-dead-vendored-platform-apps` under me) — isolated the work into this worktree via stash rather than disturb the shared root. Worktree + branch pruned. |
| ~~C:\Projects\eqsvc-terms-takedown-wt (eq-solves-service)~~ REMOVED | claude/terms-page-takedown (merged, deleted) | Claude (temporarily unpublish /terms — Adam/SKS meeting prep, unreviewed legal draft) | 2026-07-16 | DONE — **PR [#543](https://github.com/eq-solutions/eq-service/pull/543) MERGED** (squash `b587d84` → main) → eq-service.netlify.app auto-deploying. `/terms` now `notFound()`s; prior content preserved in git history for restore after legal review. Worktree removed. |
| ~~C:\Projects\eq-shell-dupes-merge-wt (eq-shell)~~ REUSED | claude/dupes-tab-merge (merged) → claude/dupes-usage-check | Claude (wire merge into the Sites Dupes tab, then a usage-based survivor pick) | 2026-07-16 | **PR #876 MERGED** (`3c4831e`, migration 0186 `eq_site_advisory_flag_pair`, APPLIED to ehow). Same worktree reused for a follow-up: **PR [#880](https://github.com/eq-solutions/eq-shell/pull/880) OPEN** — migration 0187 (`eq_site_dupe_usage`), usage-first survivor pick, unlocks 3+-row dupe groups. All gates green incl. the drift gate (fixed by a concurrent session, #878). **NOT merged — Royce's call.** |
| ~~C:\Projects\eq-intake-dupes-merge-wt (eq-intake)~~ REUSED | claude/dupes-tab-merge-client (merged) → claude/dupes-usage-check-client | Claude (flagSitePairForMerge, then getSiteDupeUsage) | 2026-07-16 | **PR #71 MERGED** (`b48cbdd`). Same worktree reused for a follow-up: **PR [#73](https://github.com/eq-solutions/eq-solves-intake/pull/73) OPEN** — fully green (15/15 tests). **NOT merged — Royce's call.** |
| ~~C:\Projects\eq-shell-site-merge-wt (eq-shell)~~ REMOVED | claude/site-merge-rpc (merged, deleted) | Claude (site-duplicate merge RPC — migration 0185) | 2026-07-15 | DONE — **PR [#868](https://github.com/eq-solutions/eq-shell/pull/868) MERGED** (squash `c3a337f`, Royce's "merge both, no review" go) → core.eq.solutions auto-deploying. `eq_site_merge_preview`/`eq_site_merge_execute`: repoints ~26 FK tables into `app_data.sites` from loser→survivor, soft-retires the loser, requires a recorded 'same' verdict + active 'manager' role. Validated live via BEGIN…ROLLBACK on ehow, zero trace left. Console: Preview→Confirm merge flow, gated by new `intake.sites.merge` permission (manager-only). Paired eq-solves-intake **PR #70 MERGED** (`previewSiteMerge`/`executeSiteMerge` client wrappers, 6/6 tests). **Migration 0185 APPLIED to ehow 09:23Z** (Royce's "merge and deploy" go, via tenant-migrate.yml workflow_dispatch) — `eq_site_merge_preview`/`eq_site_merge_execute`/`site_resolution_merge_log` confirmed live on ehow. Same dispatch also applied to `eq` tenant. `favour-perfect` tenant failed on an UNRELATED pre-existing migration (0184 — `pg_cron` extension not installed on that project) — chip task_2a98bf3b. Both worktrees + branches pruned. |
| ~~C:\Projects\eqsvc-cal-renum-wt (eq-solves-service)~~ REMOVED | claude/calibration-consolidation-backfill | Claude (eq-service #534 backfill renumber 0183→0186 + ledger reconcile) | 2026-07-14 | DONE — ephemeral worktree pruned same session. #534 rebased onto main + backfill renamed `0183_`→`0186_` (pushed `9cde375`); `service._eq_migrations` reconciled with a `0186_backfill_asset_calibration_from_assets.sql` row (out-of-band apply, sha256 `e6be587d…`). Ledger now mirrors repo 1:1 → `apply-service-migrations` shows 0 pending. PR #534 green on real gates (tsc+build, Plan). **NOT merged — Royce's call.** Backfill data already live (18 rows). Temp local branch `claude/cal-backfill-renum-tmp` deleted. |
| ~~C:\Projects\eq-shell-cal-phase3-wt (eq-shell)~~ REMOVED | claude/calibration-phase3-shell-consumers (merged, deleted) | Claude (calibration Phase 3 — 3 legacy consumers) | 2026-07-14 | DONE — **PR [#861](https://github.com/eq-solutions/eq-shell/pull/861) MERGED** (squash `b1f7267`, Royce's explicit deploy go) → core.eq.solutions deployed. Retired legacy `assets` calibration reads/writes: canonical-api `WRITABLE_FIELDS.assets` (drop 3 fields), entity-patch `asset` (drop next_service_due), briefing-engine `fetchServiceDue` (read asset_calibration.calibration_due). Rebased over #860 (audit-2b, same 3 files, no conflict); tsc -b + vite build + all CI green. Paired eq-service **#534 MERGED** by Royce (`42c9ae4`) — backfill live (18 rows), ledger reconciled (`0186_backfill…`). Worktree + local/remote branch pruned. |
| ~~C:\Projects\eq-shell-docs-resend-wt (eq-shell)~~ REMOVED | claude/docs-resend-live (merged, deleted) | Claude (docs: Resend-live truthing across runbooks + comments) | 2026-07-14 | DONE — **PR [#850](https://github.com/eq-solutions/eq-shell/pull/850) MERGED** (admin-squash `ff2f3d0` → main, Royce's go) → core.eq.solutions auto-deploying. Docs + comments only, no behaviour change. Admin-bypass was needed because the required drift gate was red on an UNRELATED live SKS violation (`service.instrument_calibration_events` RLS-disabled, issue #851, chip task_2c8986b2) — my PR had zero schema content. Isolated off origin/main via stash→worktree to avoid entangling with the concurrent `claude/compliance-register-xlsx` checkout. Worktree + local/remote branch pruned. |
| ~~C:\Projects\eq-shell\.claude\worktrees\adjudicate-0183 (eq-shell)~~ PRUNABLE | claude/site-adjudicate-0183 (merged, deleted) | Claude (site-resolver learning loop — migration 0183 + vendored console) | 2026-07-14 | DONE — **PR #848 MERGED** (squash `654cf6f`) → core.eq.solutions auto-deploying. Migration **0183** (append-only `site_resolution_verdict` + `eq_site_advisory_adjudicate` RPC + summary verdict-join), validated BEGIN…ROLLBACK on ehow (4/4 probes). Drift gate cleared (the calibration-view red was #849, concurrent). **0183 apply = One Pipe, GATED ON ROYCE — not yet dispatched** (classifier blocked auto-dispatch as prod). Worktree prunable. |
| ~~C:\Projects\eq-intake\.claude\worktrees\adjudicate-console (eq-intake)~~ PRUNABLE | claude/site-adjudicate-console (merged, deleted) | Claude (site-resolver learning loop — @eq/intake adjudicate writer + adjudicable console) | 2026-07-14 | DONE — **PR #68 MERGED** (squash) → eq-intake main. `adjudicateSiteAdvisory()` writer + verdict types + 9 tests; SiteAdvisoryPanel Same/Different/Unsure buttons. check:packages + test green. Vendored into eq-shell #848. Worktree prunable. |
| .claude/worktrees/unruffled-noyce-657c65 (eq-solves-service) | claude/balloon-years-majors-feature-ce639a (merged) | Claude (balloon-years + asset frequency chips) | 2026-07-13 | DONE — **PR #526 MERGED** (squash `a588776` → main, Royce's go) → eq-service.netlify.app auto-deploying. Two features: (1) balloon years — per-asset `major_due_year` on service.asset_local (migration **0182 APPLIED to ehow** + advisors clean) + rollup to contract_scopes year_totals, with pre-fill-from-contract + recompute guard; (2) per-asset maintenance frequency chips (M/Q/6M/A/…) on the Assets register + detail. Also cleared two types-drift blockers: asset_local (mine, 0182) + service.instruments canonical_id/cert_url (pre-existing 0180/#525 drift). tsc+build green; integration test red = known flake. Worktree + branch prunable after deploy verify. |
| C:\Projects\eq-field-mobile-polish-wt (eq-field) | claude/mobile-ui-polish | Claude (mobile device-pass polish batch — items 1/3/4/5/7/8/9) | 2026-07-13 | ACTIVE — **PR [#474](https://github.com/eq-solutions/eq-field/pull/474) OPEN** (v3.5.314). Seven device-pass fixes: [1] drop ◉ glyph on the "this week" `<option>`; [3] **root-cause** "↑ Saving…" pill hang — a 4xx write threw without releasing `_pendingWriteCount` (supabase.js) + 15s watchdog; [4] week-nav jumped across gaps (13.07→20.04) — picker now seeds a symmetric ±16-wk contiguous window (browser-proven: prev=06.07, max neighbour gap=7d); [5] Labour Hire stat-card wrench→hard-hat; [7] remove Timesheets helper paragraph; [8] hide EQ Agent FAB; [9] retire Prestart dual-source banner. Rebased through the #471/#472/#473 release train (main was 3.5.310→313 mid-session). node --check clean, preview green. NO deploy until Royce merges. Worktree prunable after merge. |
| ~~C:\Projects\eq-field-mobile-overflow-wt (eq-field)~~ PRUNABLE | claude/mobile-overflow-clamp (merged) | Claude (mobile-reflow slice 3 — overflow-x:clip body guard) | 2026-07-13 | DONE — **PR #471 MERGED** (`8776777`, v3.5.310) → field.eq.solutions LIVE. CSS-only `overflow-x: clip` on html,body (both @media 768px + pointer:coarse shell-mode); browser-verified 0px page overflow + #mobile-nav stays fixed. Worktree + branch prunable. |
| ~~C:\Projects\eq-field-prestart-mobile-wt + eq-field-prestart-feedback-wt~~ REMOVED (eq-field) | claude/prestart-mobile-submit + claude/prestart-add-feedback (both merged, deleted) | Claude (mobile prestart couldn't-submit — device pass 2026-07-13) | 2026-07-13 | DONE — **#468 (`6333737`, v3.5.308)** Submit explains why it's blocked + `_qPersist` surfaces server rejections; **#473 (`330c285`, v3.5.313)** crew-add "Added <name>" toast + scroll + retire "What's new". Both MERGED (Royce's go) → field.eq.solutions LIVE. #473 rebased through the #469→#472 concurrent mobile-reflow release train. Both worktrees + branches pruned. See memory [[mobile-foundation-program]]. LESSON: eq-field version stamps are same-line conflict magnets + auto-merge is DISABLED. |
| ~~C:\Projects\eq-shell-crm-sitecontact-wt (eq-shell)~~ REMOVED | claude/crm-add-site-contact-link (merged, deleted) | Claude (fix: add_site writes contact_site_links site_contact so contact sticks without an Edit) | 2026-07-12 | DONE — **PR #770 MERGED** (squash `de1be77` → main, Royce's go) → core.eq.solutions auto-deploying. Isolated off origin/main to dodge a shared-root collision with a concurrent phone-E164 agent (branch claude/crm-contacts-phone-e164, since merged as #769 `6c542a2`); restored their HEAD first so their commit landed on their own branch. Worktree + local/remote branch pruned 2026-07-12. |
| C:\Projects\eq-shell (ROOT checkout — no worktree) | claude/crm-contacts-phone-e164 (merged; remote deleted, local remains) | Claude (CRM-contacts phone→E.164: toAuE164 on contacts.mobile_phone) | 2026-07-12 | DONE — **PR #769 MERGED** (squash `6c542a2` → main, Royce's go) → core.eq.solutions (deploy `6a52e03a` ready) + **live-verified**: edited Rhos Thomas (Digital Realty) via Edit-contact UI, typed `0429 315 657` → DB stored `+61429315657`, updated_at bumped. Change = crm-write add_contact/update_contact + entity-insert/entity-patch contact branch; canonical-api M2M gateway left as-is (matches staff precedent). Backfill applied live: ehow 25 + zaap 100 → 100% E.164. Worked in shared ROOT (no worktree); hit the recurring shared-checkout branch race with the concurrent #770 agent (row above) — root HEAD drifted onto their branch mid-session then restored to mine, committed with branch-verify guards. Local branch still checked out at root (harmless, squash-merged — prunable). |
| C:\Projects\eq-shell-cpledger-wt (eq-shell) | claude/tombstone-cross-plane-migrations | Claude (foreman: control-plane ledger + follow-ups) | 2026-07-11 | DONE — #729 (ledger doc) MERGED; 2026_06_27b revoke APPLIED to live jvkn (verified true→false); #730 (tombstone 3 cross-plane files) MERGED `b952ecb`. Worktree + local branch pruned 2026-07-11. (eq-field net #438 worktree also already pruned.) |
| C:\Projects\eq-shell-perf-tier1-wt (eq-shell) | claude/perf-cold-open-tier1 | Claude (foreman: nav-speed Tier 1) | 2026-07-11 | ACTIVE — **PR #740 OPEN** (immutable `/assets/*` cache + gate/sample analytics to cut the ~3.2s cold-open). tsc -b + vite build + eslint green. Branch = Netlify preview only; NO production deploy until Royce merges. Worktree kept (may reuse for Tier 2). |
| .claude/worktrees/sks-comms-resource-mgmt-7563e2 (eq-shell) | claude/comms-fortnight | Claude (NSW Comms Moves 1 / 1.5 / 2b / 2c / 3 / 4 / 5) | 2026-07-10 | ALL 7 MERGED: Move 1 #727 (d7e7787, 0169+153-job backfill live); 1.5+2b #731 (7013d34, filters + crew-booking→schedule_entries); 2c #738 (6a51784, fortnight capacity grid); 3 #741 (39ef617, roster=single crew source); 4 #742 (b4e9829, fortnight job agenda); **5 #744 MERGED (squash `9838993`) — comms-crew tag (0170 + is_crew + ManageCrew picker)**; 0170 APPLIED to ehow 02:05Z (table live, RLS-on/0-policy). **6 #747 MERGED (squash `03a723f`) — fortnight declutter (hide idle rows + this-week default).** ✅ **Staff-dedupe merge DONE + VERIFIED** (Royce's go): 16 Cards stub rows retired, 19 licences + 2 timesheets repointed, 2 logins moved → picker now 93/93/0 dupes. Reversal snapshot in transcript. Root-cause (Cards match-on-onboard) still open → task chip. **7 #748 MERGED (squash `8e10d3c`, net −107 lines) — crew = Field's existing 'Comms' team (11) NOT the parallel sks_comms_crew; read-only in comms + "manage in Field" hint; 0171 drops the redundant table (dispatch whenever).** Next: NV1-as-licence, cutover. |
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
| ~~C:\Projects\eq-shell-staffdup-wt (eq-shell)~~ REMOVED | claude/staff-dup-sync-match (deleted) | Claude (staff-dup root-cause Part A) | 2026-07-11 | NO-OP — verify-live found the worker→staff identity-match fix ALREADY shipped + deployed (eq-shell #724 `b6669c0`, live as workers-canonical-sync v8). Nothing to build. Worktree + branch pruned. |
| ~~C:\Projects\eq-cards-staffdup-wt (eq-cards)~~ REMOVED | fix/staff-dup-onboarding-match (merged, deleted) | Claude (staff-dup root-cause: phone/email adopt in eq_cards_admin_upsert_worker) | 2026-07-11 | DONE — **PR #147 MERGED** (squash `92f9f94`→main). Migration 0089 APPLIED LIVE to eq-canonical (Royce's go, version `20260711054738`); worktree + local/remote branch pruned. Data cleanup also done: 2 dup stub workers deleted + 5 orphan logins pruned (0 dup-worker groups remain). |

---

## Recently pruned (2026-07-16 — 20 worktrees across 5 repos)

Full audit: every active worktree in eq-shell, eq-intake, eq-field, eq-cards, eq-solves-service checked for merged branch + clean tree before removal. Two `git worktree remove` calls without `--force` hit an interrupted-timeout mid-removal on the shared eq-shell root (heavy concurrent-session churn that session — root branch changed under the operator mid-task); recovered via `git worktree prune` + manual `rm -rf` of the orphaned leftover disk content once confirmed no longer git-registered.

| Folder | Repo | Branch | Merged as |
|--------|------|--------|-----------|
| 767-wire-check-css | eq-shell | armada/767-wire-check-css | PR #783 |
| .claude/worktrees/advisory-rpc | eq-shell | claude/advisory-rpc-anon-revoke | PR #832 |
| .claude/worktrees/dark-doc-logo | eq-shell | claude/dark-doc-logo | PR #866 |
| .claude/worktrees/sentry-fixes | eq-shell | claude/sentry-fixes | PR #673 |
| eq-shell-perf-tier1-wt | eq-shell | claude/perf-cold-open-tier1 | PR #740 |
| .claude/worktrees/eq-ops-mobile-view-af44a3 | eq-shell | (detached) | PR #875 (content match, squash) |
| eq-shell-onelogin-wt | eq-shell | main | pre-emptied husk, force-removed w/ Royce's go |
| .claude/worktrees/compassionate-goldberg-734468 | eq-shell | (detached) | pre-emptied husk, force-removed w/ Royce's go |
| eq-intake-export-tmp | eq-intake | (detached) | PR #71 (content match) |
| .claude/worktrees/advisory-console | eq-intake | claude/site-advisory-console | PR #67 |
| .claude/worktrees/ai-adjudicator | eq-intake | claude/ai-site-adjudicator | PR #69 |
| .claude/worktrees/jovial-rubin-0d0004 | eq-intake | claude/jovial-rubin-0d0004 | PR #41 |
| .claude/worktrees/sy9-duplicate-sites-6bab8b | eq-intake | claude/sy9-duplicate-sites-6bab8b | PR #66 |
| eq-field-pipeline-pagination-wt | eq-field | claude/pipeline-pagination-fix | PR #427 |
| eq-field-roster-save-fix | eq-field | claude/roster-save-409-fix | PR #423 |
| eq-field-sec | eq-field | claude/sec-cron-fn-auth | PR #463 |
| .claude/worktrees/contacts-segment-columns | eq-field | main | PR #430 |
| .claude/worktrees/wonderful-davinci-94d063 | eq-field | claude/one-login-field | PR #477 (content match, squash) |
| .claude/worktrees/provision-identity | eq-cards | claude/provision-identity | PR #118 |
| .claude/worktrees/asset-import-export-1fe110 | eq-solves-service | claude/asset-import-export-1fe110 | PR #529 |
| .claude/worktrees/unruffled-noyce-657c65 | eq-solves-service | main | already broken/dangling — `git worktree prune` |

**Left alone (do not touch without checking first):**
- eq-shell: `accept-invite-phonestub` (PR #862 open), `eq-shell-dupes-merge-wt` (uncommitted migration 0187 WIP), `.claude/worktrees/eq-roles-enterprise-eval-177343` (uncommitted migration 0186 WIP), `eq-shell-revendor-intake-wt` (PR #879 open)
- eq-intake: `eq-intake-dupes-merge-wt` (real uncommitted diff beyond its merged PR), `eq-intake-backport-wt` (new, concurrent session)
- eq-field: `eq-field-guard` (PR #466 open), `.claude/worktrees/bold-volhard-645dd7` on branch `land-472` (2 commits ahead of main, **never pushed, no PR** — flag before ever touching), `.claude/worktrees/unruffled-torvalds-03ce2f` (PR #375 merged + clean tree, but carries 2 untracked audit `.md` files that were never explicitly named for deletion — Royce's call to clear by hand)
- eq-shell also spawned several brand-new worktrees mid-session from other concurrent agents (`app-naming-wt`, `brand-handoff`, `frozen-window-issue-58b6b2`, `labour-hire-agency-grouped`, `labour-hire-modal-focus`, `sks-comms-resource-mgmt-7563e2`) — not evaluated, not touched.
- `.claude/worktrees/eq-ops-mobile-view-af44a3` (eq-shell) is down to an empty 8K husk but Windows reports the directory "busy" (file lock) — harmless, needs a machine-level look to actually delete, not a git issue.

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

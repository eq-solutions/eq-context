---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-03
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-03 07:41 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-03 07:40 UTC → 2026-07-03 07:41 UTC)

- Merged: eq-shell [#603](https://github.com/eq-solutions/eq-shell/pull/603) fix(customers): Places address widget mounts reliably on fir
- Merged: eq-shell [#602](https://github.com/eq-solutions/eq-shell/pull/602) Pending-count badge on the Number-reuse-checks admin tile
- Merged: eq-shell [#599](https://github.com/eq-solutions/eq-shell/pull/599) fix(staff): "Has gaps" chip → "Has expired" (expired-only)
- Merged: eq-shell [#598](https://github.com/eq-solutions/eq-shell/pull/598) Admin screen: number-reuse checks (recycled-phone review que
- Merged: eq-shell [#597](https://github.com/eq-solutions/eq-shell/pull/597) Route create-worker-invite through the canonical worker reso
- Merged: eq-shell [#590](https://github.com/eq-solutions/eq-shell/pull/590) fix(security): close access-control escalation + CSRF gaps
- Merged: eq-shell [#589](https://github.com/eq-solutions/eq-shell/pull/589) chore(armada): increase lighthouse budget to 6 issues / 600s
- Merged: eq-solves-service [#418](https://github.com/eq-solutions/eq-service/pull/418) fix(ci): harden apply-service-migrations.yml's merge-notify 

## ⚠ Needs you (3)

- 🟠 **Sentry new error** — `eq-shell` [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/)
- 🟠 **Sentry new error** — `eq-field` [Error: 400: {"code":"23502","details":null,"hint":null,"mess](https://eq-solutions.sentry.io/issues/131921038/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 2 | 0d |
| eq-solves-service | ✓ success | -1d ago | 3 | 3d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/) | 6 | 2026-07-03 |
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-07-01 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
| eq-cards | [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/) | 1 | 2026-07-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/131636027/) | 1 | 2026-07-02 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-03 | eq-shell | [#622](https://github.com/eq-solutions/eq-shell/pull/622) Tenants page: edit tier/modules, archive/reactivate |
| 2026-07-03 | eq-shell | [#621](https://github.com/eq-solutions/eq-shell/pull/621) fix(ops): remove broken per-column Status filter in table view |
| 2026-07-03 | eq-shell | [#619](https://github.com/eq-solutions/eq-shell/pull/619) fix(field-iframe): preserve deep-linked ?tab= on initial tenant a |
| 2026-07-03 | eq-shell | [#613](https://github.com/eq-solutions/eq-shell/pull/613) feat(customers): batch delete/archive for sites |
| 2026-07-03 | eq-shell | [#614](https://github.com/eq-solutions/eq-shell/pull/614) feat(staff): Add-to-roster action — dedupe-first roster-only crea |
| 2026-07-03 | eq-shell | [#616](https://github.com/eq-solutions/eq-shell/pull/616) feat(ops): create and edit sites from the EQ Ops quote form |
| 2026-07-03 | eq-shell | [#615](https://github.com/eq-solutions/eq-shell/pull/615) fix(ops): quote PDF download/email returned 404 for every quote — |
| 2026-07-03 | eq-shell | [#612](https://github.com/eq-solutions/eq-shell/pull/612) fix(governance): adopt quality-guardian tables — tenant-JWT polic |
| 2026-07-03 | eq-shell | [#617](https://github.com/eq-solutions/eq-shell/pull/617) Harden self-serve tenant provisioning: transactional RPC, phone-b |
| 2026-07-03 | eq-shell | [#606](https://github.com/eq-solutions/eq-shell/pull/606) feat(intake): review-queue tab (port from eq-intake #55) |
| 2026-07-03 | eq-shell | [#610](https://github.com/eq-solutions/eq-shell/pull/610) fix(audit): grant audit_log id-sequence to service_role; surface  |
| 2026-07-03 | eq-shell | [#605](https://github.com/eq-solutions/eq-shell/pull/605) fix(staff): approve-path fixes — clearer 404 + don't drop the lic |
| 2026-07-03 | eq-shell | [#609](https://github.com/eq-solutions/eq-shell/pull/609) fix(staff): pending-connections roster-name fallback never matche |
| 2026-07-03 | eq-shell | [#608](https://github.com/eq-solutions/eq-shell/pull/608) fix(governance): contact-tables gate red — relkind-aware 0155, qu |
| 2026-07-03 | eq-shell | [#607](https://github.com/eq-solutions/eq-shell/pull/607) fix(staff): confirm before discarding an unsaved licence review |
_Showing 15 of 130 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Delete stale remote branch `claude/staff-add-to-roster`** — a concurrent session's branch-switch in the shared checkout caused the first push attempt to land on the wrong branch pointing at an unrelated commit; recovered by opening the PR from `-v2` instead, but the stale remote ref is still there (`git push origin --delete claude/staff-add-to-roster`) and the classifier blocked the agent from deleting it. _(added 2026-07-03, needs your call)_
- **Merge eq-intake #58** — ledger checksum convention (the live rows are already backfilled by hand; merging just lands the convention in the repo so future self-inserts don't regress). Still open, mergeable, not blocking anything now the gate is clean. _(added 2026-07-03, needs your call)_
- **Work the 137-item review queue** — the tab is live; trades/links/formats are one-click, emergency contacts need info Royce has to source. _(added 2026-07-03, needs your call)_
- **sql/061_steward_commit_batch.sql — staged, NOT applied** — server-side `eq_steward_commit_batch` RPC (service-role-only, whitelist + event lifecycle inside) for steward run 002; apply when a second run is wanted. _(added 2026-07-03)_
- **Fix 12 contacts missing first/last name** — surfaced by the first accurate health run (contacts 206/218 complete); the dashboard tidy flow can fix them one by one. _(added 2026-07-03)_
- **Remove worktree `.claude/worktrees/ops-site-create-edit`** — now that #616 is merged, safe to `git -C C:\Projects\eq-shell worktree remove .claude/worktrees/ops-site-create-edit`. _(added 2026-07-03)_
- **Commit eq-intake/CLAUDE.md** — left untracked (eq-intake tree dirty on `feat/armada-sprint-polish`); fold into whichever branch lands next. _(added 2026-07-03)_
- **Coordinated `--reconcile-ledger`** — after go-live settles: renames/stamps the 16 bare 0103–0116/0141 rows, drops `057` + go-live hand rows. Run only WITH eq-intake (their numbering reads the live ledger). _(added 2026-07-03)_
- **Tenant-migrate run 28638433643 was dispatched then CANCELLED** — dispatched from the #608 branch on the stale premise that a live apply was needed to green the gate; the newer session-state showed #608 is code-only, and applying unmerged branch migrations risks checksum/ledger mess. Nothing was applied (cancelled at the production-approval gate, never approved). Post-merge apply of 0155/0156 from main is the normal One Pipe dispatch — separate explicit call. _(added 2026-07-03, needs your call)_
- **Renew Huon Henne's LVR** — ops action, not code: expired 2025-10-08 (268 days), staff active + on-roster. The dashboard + alerts panel now show it as critical; the ticket itself is the safety issue. **Also surfaced by the first guardian run: a second LVR expires in 29 days and an electrical licence in 25 days.** _(added 2026-07-03, needs your call)_
_…and 199 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Book monthly check-in cadence with Richo (Michael Richardson)
- Tell Mark about catch-up conversations before starting (casual, no fanfare)
- Confirm Scott Hotson start date + written offer
- Schedule Simon Bramall catch-up — Equinix Account Lead conversation
- Hold Ben Ritchie coffee — first/second week back
_…and 15 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-03 | [eq-shell: batch site delete/archive built (PR #613 open, merge blocked)](sessions/2026-07-03.md) |
| 2026-07-02 | [Token lint ratchet merged; staff licence resync endpoint shipped](sessions/2026-07-02.md) |
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-03 07:41 UTC._

---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-03
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-03 05:34 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-03 02:19 UTC → 2026-07-03 05:34 UTC)

- Merged: eq-shell [#610](https://github.com/eq-solutions/eq-shell/pull/610) fix(audit): grant audit_log id-sequence to service_role; sur
- Merged: eq-shell [#609](https://github.com/eq-solutions/eq-shell/pull/609) fix(staff): pending-connections roster-name fallback never m
- Merged: eq-shell [#608](https://github.com/eq-solutions/eq-shell/pull/608) fix(governance): contact-tables gate red — relkind-aware 015
- Merged: eq-shell [#606](https://github.com/eq-solutions/eq-shell/pull/606) feat(intake): review-queue tab (port from eq-intake #55)
- Merged: eq-shell [#605](https://github.com/eq-solutions/eq-shell/pull/605) fix(staff): approve-path fixes — clearer 404 + don't drop th
- Merged: eq-shell [#595](https://github.com/eq-solutions/eq-shell/pull/595) feat(access-control): recent-activity panel on the page itse
- Merged: eq-shell [#594](https://github.com/eq-solutions/eq-shell/pull/594) Simpler worker onboarding + stop duplicate stubs
- Merged: eq-shell [#593](https://github.com/eq-solutions/eq-shell/pull/593) fix(security): block unattributed direct DELETE on app_data.

## ⚠ Needs you (2)

- 🟠 **Sentry new error** — `eq-shell` [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/)
- 🟠 **Sentry new error** — `eq-cards` [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 6 | 0d |
| eq-solves-service | ✓ success | 0d ago | 3 | 3d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 1 | 0d |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/) | 5 | 2026-07-02 |
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-07-01 |
| eq-cards | [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/) | 1 | 2026-07-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/131636027/) | 1 | 2026-07-02 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-03 | eq-shell | [#606](https://github.com/eq-solutions/eq-shell/pull/606) feat(intake): review-queue tab (port from eq-intake #55) |
| 2026-07-03 | eq-shell | [#610](https://github.com/eq-solutions/eq-shell/pull/610) fix(audit): grant audit_log id-sequence to service_role; surface  |
| 2026-07-03 | eq-shell | [#605](https://github.com/eq-solutions/eq-shell/pull/605) fix(staff): approve-path fixes — clearer 404 + don't drop the lic |
| 2026-07-03 | eq-shell | [#609](https://github.com/eq-solutions/eq-shell/pull/609) fix(staff): pending-connections roster-name fallback never matche |
| 2026-07-03 | eq-shell | [#608](https://github.com/eq-solutions/eq-shell/pull/608) fix(governance): contact-tables gate red — relkind-aware 0155, qu |
| 2026-07-03 | eq-shell | [#607](https://github.com/eq-solutions/eq-shell/pull/607) fix(staff): confirm before discarding an unsaved licence review |
| 2026-07-03 | eq-solves-service | [#412](https://github.com/eq-solutions/eq-service/pull/412) Governed migration-apply pipeline + service invariants gate (0168 |
| 2026-07-03 | eq-solves-intake | [#61](https://github.com/eq-solutions/eq-solves-intake/pull/61) fix(guardian): health-score field lists use real app_data columns |
| 2026-07-03 | eq-solves-intake | [#60](https://github.com/eq-solutions/eq-solves-intake/pull/60) fix(guardian): auth by privilege probe, not service-key string eq |
| 2026-07-03 | eq-solves-intake | [#59](https://github.com/eq-solutions/eq-solves-intake/pull/59) chore(guardian): nightly cron 17:00 UTC (03:00 AEST) per Royce 20 |
| 2026-07-03 | eq-solves-intake | [#55](https://github.com/eq-solutions/eq-solves-intake/pull/55) feat(intake): DAMA composite score + steward run 001 + review-que |
| 2026-07-02 | eq-shell | [#603](https://github.com/eq-solutions/eq-shell/pull/603) fix(customers): Places address widget mounts reliably on first op |
| 2026-07-02 | eq-shell | [#602](https://github.com/eq-solutions/eq-shell/pull/602) Pending-count badge on the Number-reuse-checks admin tile |
| 2026-07-02 | eq-shell | [#601](https://github.com/eq-solutions/eq-shell/pull/601) Customers/Staff legibility + EQ Ops board fixes + design-token cl |
| 2026-07-02 | eq-shell | [#600](https://github.com/eq-solutions/eq-shell/pull/600) fix(customers): migrate address autocomplete to new Places API (f |
_Showing 15 of 128 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Fix 12 contacts missing first/last name** — surfaced by the first accurate health run (contacts 206/218 complete); the dashboard tidy flow can fix them one by one. _(added 2026-07-03)_
- **Merge eq-shell PR #616** (Ops site create/edit) — merge auto-deploys core.eq.solutions; remove worktree `.claude/worktrees/ops-site-create-edit` after merge. _(added 2026-07-03, needs your call)_
- **Decide handling for guardian go-live hand-inserted ledger rows** — `062_queue_rpcs` (and any further 058–062 applies) trip #608's detector → gate red repo-wide (#610 currently affected). Options: eq-intake stops self-inserting mid-go-live (per its new CLAUDE.md), delete the hand rows once go-live settles, or bump `LEDGER_INTEGRITY_CUTOFF` in `check-tenant-drift.mjs`. _(added 2026-07-03, needs your call)_
- **Commit eq-intake/CLAUDE.md** — left untracked (eq-intake tree dirty on `feat/armada-sprint-polish`); fold into whichever branch lands next. _(added 2026-07-03)_
- **Coordinated `--reconcile-ledger`** — after go-live settles: renames/stamps the 16 bare 0103–0116/0141 rows, drops `057` + go-live hand rows. Run only WITH eq-intake (their numbering reads the live ledger). _(added 2026-07-03)_
- **Admin-merge PR #610 in the GitHub UI** — only red is the pre-existing drift gate (#608 fixes it); merge auto-deploys core.eq.solutions with the error-logging change. _(added 2026-07-03, needs your call)_
- **Tenant-migrate run 28638433643 was dispatched then CANCELLED** — dispatched from the #608 branch on the stale premise that a live apply was needed to green the gate; the newer session-state showed #608 is code-only, and applying unmerged branch migrations risks checksum/ledger mess. Nothing was applied (cancelled at the production-approval gate, never approved). Post-merge apply of 0155/0156 from main is the normal One Pipe dispatch — separate explicit call. _(added 2026-07-03, needs your call)_
- **Structural fix proposed for the underlying confusion** — eq-solves-service has no CI-gated apply pipeline for its own `supabase/migrations/*.sql` (writes straight to ehow, same plane eq-shell's One Pipe governs). Full findings + 3 sized options in [`eq-context/eq/canonical-readiness/plan-eq-service-migration-apply-gate-2026-07-03.md`](canonical-readiness/plan-eq-service-migration-apply-gate-2026-07-03.md) — recommends a small dispatch-gated workflow scoped to just ehow (mirrors `tenant-migrate.yml` but simpler, one target DB) plus reusing eq-shell's anon-grant/policy-lint check as a pre-merge gate in eq-service's own CI. A parallel, already-tracked gap exists for eq-cards on jvkn ([`plan-control-plane-governance-and-card-read-2026-06-25.md`](canonical-readiness/plan-control-plane-governance-and-card-read-2026-06-25.md)) — kept separate, different plane. Nothing implemented; chip `task_02f3f8d0` filed for the build once you pick a direction. _(added 2026-07-03, needs your call — pick an option in the plan doc)_
- **Renew Huon Henne's LVR** — ops action, not code: expired 2025-10-08 (268 days), staff active + on-roster. The dashboard + alerts panel now show it as critical; the ticket itself is the safety issue. **Also surfaced by the first guardian run: a second LVR expires in 29 days and an electrical licence in 25 days.** _(added 2026-07-03, needs your call)_
- **Send Huon** the connection-email reply + before/after graphic. _(added 2026-07-02)_
_…and 198 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-03 | [eq-shell: licence-review discard guard (PR #607, merged + deployed live)](sessions/2026-07-03.md) |
| 2026-07-02 | [Token lint ratchet merged; staff licence resync endpoint shipped](sessions/2026-07-02.md) |
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-03 05:34 UTC._

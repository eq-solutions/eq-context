---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-03
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-03 02:19 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-02 13:48 UTC → 2026-07-03 02:19 UTC)

- Merged: eq-shell [#607](https://github.com/eq-solutions/eq-shell/pull/607) fix(staff): confirm before discarding an unsaved licence rev
- Merged: eq-shell [#592](https://github.com/eq-solutions/eq-shell/pull/592) Equipment: inline assign-to-staff dropdown
- Merged: eq-shell [#589](https://github.com/eq-solutions/eq-shell/pull/589) chore(armada): increase lighthouse budget to 6 issues / 600s
- Merged: eq-shell [#588](https://github.com/eq-solutions/eq-shell/pull/588) style(tokens): promote hex-colour lint rule to error; add st
- Merged: eq-shell [#587](https://github.com/eq-solutions/eq-shell/pull/587) fix(security): lock down worker_dedup_archive_20260630 on jv
- Merged: eq-shell [#586](https://github.com/eq-solutions/eq-shell/pull/586) style(tokens): semantics pass — raw semantic hex → CSS token
- Merged: eq-shell [#585](https://github.com/eq-solutions/eq-shell/pull/585) refactor(staff): Phase E — extract MatrixView + SplitPanel i
- Merged: eq-shell [#581](https://github.com/eq-solutions/eq-shell/pull/581) style(ui): roll Warm Sand neutrals repo-wide (Direction-D)
- ✅ Needs you: 3 → 2

## ⚠ Needs you (2)

- 🟠 **Sentry new error** — `eq-shell` [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/)
- 🟠 **Sentry new error** — `eq-cards` [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 2 | 0d |
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
| 2026-07-03 | eq-shell | [#607](https://github.com/eq-solutions/eq-shell/pull/607) fix(staff): confirm before discarding an unsaved licence review |
| 2026-07-02 | eq-shell | [#603](https://github.com/eq-solutions/eq-shell/pull/603) fix(customers): Places address widget mounts reliably on first op |
| 2026-07-02 | eq-shell | [#602](https://github.com/eq-solutions/eq-shell/pull/602) Pending-count badge on the Number-reuse-checks admin tile |
| 2026-07-02 | eq-shell | [#601](https://github.com/eq-solutions/eq-shell/pull/601) Customers/Staff legibility + EQ Ops board fixes + design-token cl |
| 2026-07-02 | eq-shell | [#600](https://github.com/eq-solutions/eq-shell/pull/600) fix(customers): migrate address autocomplete to new Places API (f |
| 2026-07-02 | eq-shell | [#598](https://github.com/eq-solutions/eq-shell/pull/598) Admin screen: number-reuse checks (recycled-phone review queue) |
| 2026-07-02 | eq-shell | [#597](https://github.com/eq-solutions/eq-shell/pull/597) Route create-worker-invite through the canonical worker resolver |
| 2026-07-02 | eq-shell | [#599](https://github.com/eq-solutions/eq-shell/pull/599) fix(staff): "Has gaps" chip → "Has expired" (expired-only) |
| 2026-07-02 | eq-shell | [#596](https://github.com/eq-solutions/eq-shell/pull/596) fix(customers): Add-site address autocomplete fills suburb/state |
| 2026-07-02 | eq-solves-service | [#411](https://github.com/eq-solutions/eq-service/pull/411) Canonical audit 2026-07-02: SoT drift guard, Shell-nav Calendar/D |
| 2026-07-02 | eq-solves-service | [#410](https://github.com/eq-solutions/eq-service/pull/410) Contacts canonical cutover — views + INSTEAD OF triggers (0167) |
| 2026-07-02 | eq-cards | [#117](https://github.com/eq-solutions/eq-cards/pull/117) Migration hygiene: dup-number CI guard + apply runbook; clear 007 |
| 2026-07-02 | eq-cards | [#113](https://github.com/eq-solutions/eq-cards/pull/113) Track B: unify worker-identity resolution (jvkn control-plane) |
| 2026-07-02 | eq-cards | [#116](https://github.com/eq-solutions/eq-cards/pull/116) chore(share-licence): drop stale NOT YET DEPLOYED note |
| 2026-07-02 | eq-cards | [#115](https://github.com/eq-solutions/eq-cards/pull/115) fix(connections): source worker name from the workers table acros |
_Showing 15 of 122 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Guardian go-live on ehow, in order:** apply `sql/058` → apply `sql/059` → `supabase functions deploy quality-guardian` → `select vault.create_secret('<service_role key>','edge_service_role_key')` → apply `sql/060` (registers the nightly cron) → optional manual POST smoke + check `eq_quality_runs`. Auto-mode classifier correctly blocks agent-applied prod SQL; until 058 lands, the strip shows correct counts but `alerts_failed` stays non-zero. _(added 2026-07-03, needs your call)_
- **Cron hour check before applying 060** — registers 01:00 UTC = 11:00 AEST (midday-ish); pre-dawn alternative `0 17 * * *` = 03:00 AEST offered — say which. _(added 2026-07-03, needs your call)_
- **Renew Huon Henne's LVR** — ops action, not code: expiry 2025-10-08, staff active + on-roster. The dashboard will now show it as critical; the ticket itself is the safety issue. _(added 2026-07-03, needs your call)_
- **eq-quotes-embed-quotes cron is firing hourly with a NULL Authorization header** — its Vault secret `quotes_cron_secret` is gone (ehow Vault is completely EMPTY), and `'Bearer ' || NULL` nulls the whole header, so the hourly POST to eq-quotes-sks.fly.dev has been going out unauthenticated. Restore the secret or unschedule the job (Quotes is retired → EQ Ops). Chip `task_9aec631d` filed. _(added 2026-07-03, needs your call)_
- **Send Huon** the connection-email reply + before/after graphic. _(added 2026-07-02)_
- **Resolve the pending "432470463 · No licences yet" connection request** on core.eq.solutions/sks/staff — nameless self-signup from before the name-gate; approve/decline + nudge to add details. _(added 2026-07-02)_
- **Define the required-credential policy** (what SKS actually requires) + decide whether to add a worker **trade field** — the two blockers before the gaps engine can ship. _(added 2026-07-02)_
- **Migration runbook** — load order (staff+sites → teams → team_members → schedule_entries → timesheets → leave/locks), crosswalk-completion checklist, the two unpivot specs, two-gate reconciliation. Offered, not built. _(added 2026-07-02)_
- **Complete the identity crosswalk** — 25 unlinked people + 11 unlinked sites + 9/6/6 unmatched names need a human who knows these people; pay-critical, no automation. _(added 2026-07-02, needs your call)_
- **Build the canonical reconciliation gate** — name-resolution report (0 red before load) + pay reconciliation (hours/person/week source-vs-canonical identical through one full pay cycle). The `migration_baseline`/`eq_migration_counts` machinery already exists to hang this on. _(added 2026-07-02)_
_…and 193 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-03 | [quality-guardian resurrected: tenant context + cron fix built, PR #57 merged (production go pending)](sessions/2026-07-03.md) |
| 2026-07-02 | [Token lint ratchet merged; staff licence resync endpoint shipped](sessions/2026-07-02.md) |
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-03 02:19 UTC._

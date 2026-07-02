---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-02
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-02 13:48 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-02 11:48 UTC → 2026-07-02 13:48 UTC)

- Merged: eq-shell [#595](https://github.com/eq-solutions/eq-shell/pull/595) feat(access-control): recent-activity panel on the page itse
- Merged: eq-shell [#594](https://github.com/eq-solutions/eq-shell/pull/594) Simpler worker onboarding + stop duplicate stubs
- Merged: eq-shell [#593](https://github.com/eq-solutions/eq-shell/pull/593) fix(security): block unattributed direct DELETE on app_data.
- Merged: eq-shell [#591](https://github.com/eq-solutions/eq-shell/pull/591) chore: remove profile settings page
- Merged: eq-shell [#590](https://github.com/eq-solutions/eq-shell/pull/590) fix(security): close access-control escalation + CSRF gaps
- Merged: eq-shell [#584](https://github.com/eq-solutions/eq-shell/pull/584) fix(ops): PDF import — real spinner + apply default markup
- Merged: eq-shell [#583](https://github.com/eq-solutions/eq-shell/pull/583) feat(reports): manual "mark done" on the forecasts tab
- Merged: eq-shell [#582](https://github.com/eq-solutions/eq-shell/pull/582) style(ui): Warm Sand neutrals in CSS files — closes the mobi

## ⚠ Needs you (3)

- 🟠 **Sentry new error** — `eq-shell` [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/)
- 🟠 **Sentry new error** — `eq-cards` [minified:I3: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)
- 🟠 **Sentry new error** — `eq-cards` [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 5 | 3d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 2 | 0d |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/) | 4 | 2026-07-02 |
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-07-01 |
| eq-cards | [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/) | 1 | 2026-07-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/131636027/) | 1 | 2026-07-02 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-02 | eq-shell | [#603](https://github.com/eq-solutions/eq-shell/pull/603) fix(customers): Places address widget mounts reliably on first op |
| 2026-07-02 | eq-shell | [#602](https://github.com/eq-solutions/eq-shell/pull/602) Pending-count badge on the Number-reuse-checks admin tile |
| 2026-07-02 | eq-shell | [#601](https://github.com/eq-solutions/eq-shell/pull/601) Customers/Staff legibility + EQ Ops board fixes + design-token cl |
| 2026-07-02 | eq-shell | [#600](https://github.com/eq-solutions/eq-shell/pull/600) fix(customers): migrate address autocomplete to new Places API (f |
| 2026-07-02 | eq-shell | [#598](https://github.com/eq-solutions/eq-shell/pull/598) Admin screen: number-reuse checks (recycled-phone review queue) |
| 2026-07-02 | eq-shell | [#597](https://github.com/eq-solutions/eq-shell/pull/597) Route create-worker-invite through the canonical worker resolver |
| 2026-07-02 | eq-shell | [#599](https://github.com/eq-solutions/eq-shell/pull/599) fix(staff): "Has gaps" chip → "Has expired" (expired-only) |
| 2026-07-02 | eq-shell | [#596](https://github.com/eq-solutions/eq-shell/pull/596) fix(customers): Add-site address autocomplete fills suburb/state |
| 2026-07-02 | eq-cards | [#117](https://github.com/eq-solutions/eq-cards/pull/117) Migration hygiene: dup-number CI guard + apply runbook; clear 007 |
| 2026-07-02 | eq-cards | [#113](https://github.com/eq-solutions/eq-cards/pull/113) Track B: unify worker-identity resolution (jvkn control-plane) |
| 2026-07-02 | eq-cards | [#116](https://github.com/eq-solutions/eq-cards/pull/116) chore(share-licence): drop stale NOT YET DEPLOYED note |
| 2026-07-02 | eq-cards | [#115](https://github.com/eq-solutions/eq-cards/pull/115) fix(connections): source worker name from the workers table acros |
| 2026-07-02 | eq-cards | [#114](https://github.com/eq-solutions/eq-cards/pull/114) fix(ci): move web image-compress behind a conditional import |
| 2026-07-02 | eq-cards | [#112](https://github.com/eq-solutions/eq-cards/pull/112) fix(cards): connection-email deep-link + unblock profile save RPC |
| 2026-07-02 | eq-solves-intake | [#56](https://github.com/eq-solutions/eq-solves-intake/pull/56) fix(intake): licence strip fail-open — expired licences must surf |
_Showing 15 of 121 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Merge PR #603** (first-open mount-race fix) — CI green, one-function change; production deploy is Royce's click (classifier blocks agent merge of the auth hub). Without it autocomplete still works, just occasionally needs a modal reopen on first use after a page load. _(added 2026-07-02, needs your call)_
- **Send Huon** the connection-email reply + before/after graphic. _(added 2026-07-02)_
- **Resolve the pending "432470463 · No licences yet" connection request** on core.eq.solutions/sks/staff — nameless self-signup from before the name-gate; approve/decline + nudge to add details. _(added 2026-07-02)_
- **Define the required-credential policy** (what SKS actually requires) + decide whether to add a worker **trade field** — the two blockers before the gaps engine can ship. _(added 2026-07-02)_
- **Migration runbook** — load order (staff+sites → teams → team_members → schedule_entries → timesheets → leave/locks), crosswalk-completion checklist, the two unpivot specs, two-gate reconciliation. Offered, not built. _(added 2026-07-02)_
- **Complete the identity crosswalk** — 25 unlinked people + 11 unlinked sites + 9/6/6 unmatched names need a human who knows these people; pay-critical, no automation. _(added 2026-07-02, needs your call)_
- **Build the canonical reconciliation gate** — name-resolution report (0 red before load) + pay reconciliation (hours/person/week source-vs-canonical identical through one full pay cycle). The `migration_baseline`/`eq_migration_counts` machinery already exists to hang this on. _(added 2026-07-02)_
- **Verify SKS `tenant_id` live** (`7dee117c-98bd-4d39-af8c-2c81d02a1e85` per suite-state) before any load — must be stamped explicitly on every row (JWT default won't resolve on a service-role insert). _(added 2026-07-02)_
- **Agenda for tomorrow's meeting with the 7 Claude-using guys** — decide champions vs builders vs testers, guardrails before keys. Offered, not built. _(added 2026-07-02, needs your call)_
- **Name the EQ↔SKS data-ownership arrangement** before Cards runs all of SKS NSW — whose worker data, under what arrangement, what happens if Royce leaves. Cross-entity governance landmine; name it while it's friendly. _(added 2026-07-02, needs your call)_
_…and 191 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-02 | [Token lint ratchet merged; staff licence resync endpoint shipped](sessions/2026-07-02.md) |
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-02 13:48 UTC._

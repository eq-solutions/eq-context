---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-30 08:18 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-30 00:03 UTC → 2026-06-30 08:18 UTC)

- Merged: eq-shell [#551](https://github.com/eq-solutions/eq-shell/pull/551) fix(audit): stamp actor on Field/Service toggle + calibratio
- Merged: eq-shell [#550](https://github.com/eq-solutions/eq-shell/pull/550) feat(crm): sites inline toggle table + apply-all + A-Z conta
- Merged: eq-shell [#547](https://github.com/eq-solutions/eq-shell/pull/547) feat(audit): extend Tenant Activity Log to contact link tabl
- Merged: eq-shell [#532](https://github.com/eq-solutions/eq-shell/pull/532) fix(iframes): suppress Sentry errors from background pre-war
- Merged: eq-shell [#531](https://github.com/eq-solutions/eq-shell/pull/531) fix(auth): resend Shell invite instead of blocking
- Merged: eq-shell [#530](https://github.com/eq-solutions/eq-shell/pull/530) fix(auth): promote Cards-worker stub on invite accept
- Merged: eq-shell [#529](https://github.com/eq-solutions/eq-shell/pull/529) feat(eq-ops): clickable status badge in quote detail panel
- Merged: eq-shell [#525](https://github.com/eq-solutions/eq-shell/pull/525) fix(gm-reports): refresh uploaded_at on re-upload
- ✅ Needs you: 4 → 3

## ⚠ Needs you (3)

- 🟠 **Sentry new error** — `eq-cards` [minified:iF: ServerFailure(42883): operator does not exist: ](https://eq-solutions.sentry.io/issues/131103567/)
- 🟠 **Sentry new error** — `eq-shell` [EQ Field handoff HTTP 403](https://eq-solutions.sentry.io/issues/130938311/)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100659/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ✓ success | 0d ago | 7 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [minified:iF: ServerFailure(42883): operator does not exist: uuid = text](https://eq-solutions.sentry.io/issues/131103567/) | 6 | 2026-06-29 |
| eq-shell | [EQ Field handoff HTTP 403](https://eq-solutions.sentry.io/issues/130938311/) | 3 | 2026-06-29 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100659/) | 2 | 2026-06-30 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/131100658/) | 2 | 2026-06-30 |
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-shell | [captureServerError](https://eq-solutions.sentry.io/issues/130413967/) | 2 | 2026-06-29 |
| eq-shell | [EQ Service iframe did not load within timeout](https://eq-solutions.sentry.io/issues/130169257/) | 2 | 2026-06-29 |
| eq-shell | [EQ Field handoff network error: Load failed](https://eq-solutions.sentry.io/issues/130061083/) | 2 | 2026-06-29 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-30 | eq-shell | [#551](https://github.com/eq-solutions/eq-shell/pull/551) fix(audit): stamp actor on Field/Service toggle + calibration edi |
| 2026-06-30 | eq-shell | [#550](https://github.com/eq-solutions/eq-shell/pull/550) feat(crm): sites inline toggle table + apply-all + A-Z contacts |
| 2026-06-30 | eq-shell | [#547](https://github.com/eq-solutions/eq-shell/pull/547) feat(audit): extend Tenant Activity Log to contact link tables |
| 2026-06-30 | eq-solves-service | [#378](https://github.com/eq-solutions/eq-service/pull/378) feat(ui): branded 404 page — app/not-found.tsx |
| 2026-06-30 | eq-field | [#368](https://github.com/eq-solutions/eq-field/pull/368) v3.5.208 — canonical wiring: Safety module fully wired for SKS |
| 2026-06-30 | eq-field | [#367](https://github.com/eq-solutions/eq-field/pull/367) fix(canonical): field_sites filters active too (archived sites re |
| 2026-06-30 | eq-field | [#366](https://github.com/eq-solutions/eq-field/pull/366) v3.5.207 — canonical wiring: Roster/Leave realtime + Teams wire + |
| 2026-06-30 | eq-field | [#365](https://github.com/eq-solutions/eq-field/pull/365) chore(canonical): record digest opt-out migration (field_managers |
| 2026-06-29 | eq-shell | [#546](https://github.com/eq-solutions/eq-shell/pull/546) fix(staff): profile review state matches the table badge |
| 2026-06-29 | eq-shell | [#545](https://github.com/eq-solutions/eq-shell/pull/545) fix(staff): match existing staff stub on Cards approval instead o |
| 2026-06-29 | eq-shell | [#544](https://github.com/eq-solutions/eq-shell/pull/544) fix(staff): licence review stops flipping back to re-review for p |
| 2026-06-29 | eq-shell | [#543](https://github.com/eq-solutions/eq-shell/pull/543) Gate the Service mint with @eq-solutions/contracts (mint side) |
| 2026-06-29 | eq-shell | [#542](https://github.com/eq-solutions/eq-shell/pull/542) feat(customers): customer-level Field/Service toggles in the head |
| 2026-06-29 | eq-shell | [#541](https://github.com/eq-solutions/eq-shell/pull/541) feat(customers): site street address + Field/Service toggles per  |
| 2026-06-29 | eq-shell | [#540](https://github.com/eq-solutions/eq-shell/pull/540) fix(customers): Add Site 500 — remove non-existent site_contact_i |
_Showing 15 of 110 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **`service.sites` filter `active`** — mirror the field_sites fix in eq-solves-service (`AND s.active = true`). Spawned as task chip. Latent leak (0 rows today) _(added 2026-06-30)_
- **Merge eq-field `claude/field-sites-active-filter`** to record the field_sites migration (DB already applied) _(added 2026-06-30)_
- **Activity Log — name resolution for link events** (link rows carry only ids; feed shows "Contact ↔ site" without names) _(added 2026-06-30)_
- **Onboarding name-only stub match panel** — force admin confirmation when a name_close candidate exists (null-email/no-phone stubs can't auto-match) _(added 2026-06-30)_
- **Run first `shipwright` build** of #377 — in a dedicated Claude Code session rooted in eq-service (skills load from its `.claude/skills/`; can't be driven from another repo's session). Runbook in SETUP-NOTES + today's session log _(added 2026-06-30)_
- **crows-nest `/loop`** — needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`); don't arm until one clean manual cycle is observed _(added 2026-06-30)_
- **Add `test: vitest run`** to eq-service `.armada/config.json` once a clean cycle is seen + unit-test green verified _(added 2026-06-30)_
- **auth_handoff Sentry alert** — native rule on `canary=auth_handoff` AND `level=error` (catches real-user slug_unresolved/no_email; the probe already covers secret drift). MCP is read-only for alert rules → 2-min UI action (recipe on file), or build the watcher-as-code _(added 2026-06-30)_
- **Contracts versioning discipline** — both repos pin `#v0.1.0`; on any contract change, bump the package + tag + update BOTH consumer pins together. The compile gate only holds when the pins match _(added 2026-06-30)_
- **Add eq-contracts to the suite-state cron** repo list so the new package shows in the nightly snapshot _(added 2026-06-30)_
_…and 146 more · [eq/pending.md](eq/pending.md)_

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
| 2026-06-30 | [Tenant Activity Log shipped (audit by domain, not storage)](sessions/2026-06-30.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
| 2026-06-28 | [EQ Service batch-create fix](sessions/2026-06-28-batch-create-fix.md) |
| 2026-06-27 | [2026-06-27 — Usability sprint + security gate promotion](sessions/2026-06-27-usability-sprint.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-30 08:18 UTC._

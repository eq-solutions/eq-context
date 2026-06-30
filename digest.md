---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-30 17:29 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-30 17:08 UTC → 2026-06-30 17:29 UTC)

- Merged: eq-shell [#568](https://github.com/eq-solutions/eq-shell/pull/568) fix(staff): pending connections — admin notify, reject email
- Merged: eq-shell [#567](https://github.com/eq-solutions/eq-shell/pull/567) fix(staff): show name for existing staff in pending connecti
- Merged: eq-shell [#564](https://github.com/eq-solutions/eq-shell/pull/564) refactor(pdf): @react-pdf/renderer replaces Puppeteer + chro
- Merged: eq-shell [#513](https://github.com/eq-solutions/eq-shell/pull/513) fix(docs): correct stale EQ_SECRET_SALT guidance — HMAC reti
- Merged: eq-shell [#474](https://github.com/eq-solutions/eq-shell/pull/474) fix(transport): iframe origin hardening — SKS token refresh,
- Merged: eq-shell [#469](https://github.com/eq-solutions/eq-shell/pull/469) fix(auth): phone OTP login no longer requires a second TOTP 
- Merged: eq-shell [#467](https://github.com/eq-solutions/eq-shell/pull/467) fix(auth): provision shell_control.users on Cards worker app
- Merged: eq-shell [#455](https://github.com/eq-solutions/eq-shell/pull/455) fix(vendor): repair eq-intake PR #449 build regressions
- ✅ Needs you: 1 → 0

## ✓ Needs you (0)

**Nothing flagged — every EQ repo green, no aging PRs, substrate honest.** ✓

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-30 | eq-shell | [#568](https://github.com/eq-solutions/eq-shell/pull/568) fix(staff): pending connections — admin notify, reject email, pho |
| 2026-06-30 | eq-shell | [#567](https://github.com/eq-solutions/eq-shell/pull/567) fix(staff): show name for existing staff in pending connections |
| 2026-06-30 | eq-shell | [#566](https://github.com/eq-solutions/eq-shell/pull/566) fix(ui): iOS spinner animation — will-change: transform on all CS |
| 2026-06-30 | eq-shell | [#564](https://github.com/eq-solutions/eq-shell/pull/564) refactor(pdf): @react-pdf/renderer replaces Puppeteer + chromium |
| 2026-06-30 | eq-shell | [#565](https://github.com/eq-solutions/eq-shell/pull/565) fix(staff): matrix full licence names in headers + mobile polish |
| 2026-06-30 | eq-shell | [#563](https://github.com/eq-solutions/eq-shell/pull/563) fix(equipment): cert import 500 — send cert URLs, not bytes, to b |
| 2026-06-30 | eq-shell | [#562](https://github.com/eq-solutions/eq-shell/pull/562) refactor(ui): route brand hexes through @eq tokens (105 across 19 |
| 2026-06-30 | eq-shell | [#552](https://github.com/eq-solutions/eq-shell/pull/552) fix(staff): training matrix licence numbers + CSV export + employ |
| 2026-06-30 | eq-solves-service | [#383](https://github.com/eq-solutions/eq-service/pull/383) feat(app): branded public 'What's New' page (/whats-new) |
| 2026-06-30 | eq-solves-service | [#380](https://github.com/eq-solutions/eq-service/pull/380) feat(app): add branded error boundaries (error.tsx + global-error |
| 2026-06-30 | eq-solves-service | [#381](https://github.com/eq-solutions/eq-service/pull/381) fix(canonical): filter service.sites view by active = true |
| 2026-06-30 | eq-solves-service | [#378](https://github.com/eq-solutions/eq-service/pull/378) feat(ui): branded 404 page — app/not-found.tsx |
| 2026-06-30 | eq-field | [#380](https://github.com/eq-solutions/eq-field/pull/380) v3.5.216 — edge function canonical rewrite (ehow compatibility) |
| 2026-06-30 | eq-field | [#379](https://github.com/eq-solutions/eq-field/pull/379) security(zaap): revoke residual anon grants on worker-PII tables |
| 2026-06-30 | eq-field | [#378](https://github.com/eq-solutions/eq-field/pull/378) v3.5.215 — Supervisor Notes live on SKS + Teams realtime |
_Showing 15 of 107 · full record in [sessions/](sessions/)_

## Pending (EQ)

- EQ Cards: ARMADA lighthouse — PR #109 was merged before `armada:lighthouse` label applied; Calum's system likely needs an open PR. New open PR with label OR Calum runs manually _(added 2026-06-30)_
- EQ Cards: Contact John Angangan to retry signup — duplicate-worker fix (migrations 0062/0063) is now live _(added 2026-06-30)_
- EQ Cards: Wrap `eq_cards_find_pending_invite` RPC call (`otp_screen.dart:163`) into `WorkerSelfRepository` data layer — low priority, no behaviour change _(added 2026-06-30)_
- **EQ Ops active jobs view** — roster tab pulling from `app_data.jobs` (customer, site, job no, days active, value); not built _(added 2026-06-30)_
- **EQ Ops home tile** — Shell home tile with overdue follow-ups, stale quotes, active jobs; not built _(added 2026-06-30)_
- **Field crew on job** — workers in Field see their assigned job; requires eq-field repo changes _(added 2026-06-30)_
- **`issues.*` PermKeys activation** — Phase 3 when Issues UI ships for EQ plane; currently deferred constants _(added 2026-06-30)_
- **3 docs-spike branches KEPT — Royce's call to delete** — `claude/design-system-tokens` (41d; early @eq/tokens design spec + design-audit-2026-05-20.md), `claude/epic-ellis-987f75` (23d; single SCHEMA-GOVERNANCE.md note), `claude/vigilant-cray-4e074e` (36d; HANDOFF-*.md session notes). These hold **unique unmerged docs not in main** — superseded, but deleting unmerged work needs your sign-off. Likely all 3 safe to `git branch -D` _(added 2026-06-30)_
- **nspbmir anon-PII audit** — NOT done (per Royce "don't touch nspbmir"); eq-guard blocks SKS-live from EQ sessions anyway → needs a dedicated SKS-context session _(added 2026-06-30)_
- **God-component extraction** (StaffPage MatrixView/SplitPanel out of the 2,094-line file) — still deferred: needs a running-app session to verify layout (tsc catches imports, not render); the #562 same-file conflict is now cleared (merged) _(added 2026-06-30)_
_…and 149 more · [eq/pending.md](eq/pending.md)_

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
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
| 2026-06-29 | [SKS data reset + maintenance check page parallelization](sessions/2026-06-29.md) |
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
| 2026-06-28 | [EQ Service batch-create fix](sessions/2026-06-28-batch-create-fix.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-30 17:29 UTC._

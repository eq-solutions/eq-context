---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-02
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-02 11:06 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-01 18:55 UTC → 2026-07-02 11:06 UTC)

- Merged: eq-shell [#599](https://github.com/eq-solutions/eq-shell/pull/599) fix(staff): "Has gaps" chip → "Has expired" (expired-only)
- Merged: eq-shell [#598](https://github.com/eq-solutions/eq-shell/pull/598) Admin screen: number-reuse checks (recycled-phone review que
- Merged: eq-shell [#597](https://github.com/eq-solutions/eq-shell/pull/597) Route create-worker-invite through the canonical worker reso
- Merged: eq-shell [#596](https://github.com/eq-solutions/eq-shell/pull/596) fix(customers): Add-site address autocomplete fills suburb/s
- Merged: eq-shell [#595](https://github.com/eq-solutions/eq-shell/pull/595) feat(access-control): recent-activity panel on the page itse
- Merged: eq-shell [#594](https://github.com/eq-solutions/eq-shell/pull/594) Simpler worker onboarding + stop duplicate stubs
- Merged: eq-shell [#580](https://github.com/eq-solutions/eq-shell/pull/580) style(staff): Warm Sand neutrals pilot on StaffPage (Directi
- Merged: eq-shell [#578](https://github.com/eq-solutions/eq-shell/pull/578) refactor(staff): extract + unit-test pure StaffPage logic (P
- ⚠ Needs you: 1 → 3 (new items)

## ⚠ Needs you (3)

- 🟠 **Sentry new error** — `eq-shell` [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/)
- 🟠 **Sentry new error** — `eq-cards` [minified:I3: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)
- 🟠 **Sentry new error** — `eq-cards` [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 3 | 3d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | 0d |
| eq-solves-intake | ? unknown | ? | 1 | 0d |

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
| 2026-07-02 | eq-shell | [#598](https://github.com/eq-solutions/eq-shell/pull/598) Admin screen: number-reuse checks (recycled-phone review queue) |
| 2026-07-02 | eq-shell | [#597](https://github.com/eq-solutions/eq-shell/pull/597) Route create-worker-invite through the canonical worker resolver |
| 2026-07-02 | eq-shell | [#599](https://github.com/eq-solutions/eq-shell/pull/599) fix(staff): "Has gaps" chip → "Has expired" (expired-only) |
| 2026-07-02 | eq-shell | [#596](https://github.com/eq-solutions/eq-shell/pull/596) fix(customers): Add-site address autocomplete fills suburb/state |
| 2026-07-02 | eq-cards | [#116](https://github.com/eq-solutions/eq-cards/pull/116) chore(share-licence): drop stale NOT YET DEPLOYED note |
| 2026-07-02 | eq-cards | [#115](https://github.com/eq-solutions/eq-cards/pull/115) fix(connections): source worker name from the workers table acros |
| 2026-07-02 | eq-cards | [#114](https://github.com/eq-solutions/eq-cards/pull/114) fix(ci): move web image-compress behind a conditional import |
| 2026-07-02 | eq-cards | [#112](https://github.com/eq-solutions/eq-cards/pull/112) fix(cards): connection-email deep-link + unblock profile save RPC |
| 2026-07-02 | eq-solves-intake | [#54](https://github.com/eq-solutions/eq-solves-intake/pull/54) fix(intake): flag low-sample entities on the health dashboard |
| 2026-07-01 | eq-shell | [#594](https://github.com/eq-solutions/eq-shell/pull/594) Simpler worker onboarding + stop duplicate stubs |
| 2026-07-01 | eq-shell | [#595](https://github.com/eq-solutions/eq-shell/pull/595) feat(access-control): recent-activity panel on the page itself |
| 2026-07-01 | eq-shell | [#592](https://github.com/eq-solutions/eq-shell/pull/592) Equipment: inline assign-to-staff dropdown |
| 2026-07-01 | eq-shell | [#590](https://github.com/eq-solutions/eq-shell/pull/590) fix(security): close access-control escalation + CSRF gaps |
| 2026-07-01 | eq-shell | [#593](https://github.com/eq-solutions/eq-shell/pull/593) fix(security): block unattributed direct DELETE on app_data.asset |
| 2026-07-01 | eq-shell | [#591](https://github.com/eq-solutions/eq-shell/pull/591) chore: remove profile settings page |
_Showing 15 of 117 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Verify Add-site autocomplete live** after the #596 deploy — on core.eq.solutions → Add site, type an address, confirm Suburb/State fill. If not, clear-cache redeploy. _(added 2026-07-02)_
- **EQ Cards address autocomplete = greenfield** — Cards worker address entry (`profile_edit_screen.dart` + `profile_fill_from_licence_screen.dart`) is manual text + static state dropdown; NO Places, no package, no key. "Should already be done" = it isn't. Flutter web, so the Shell JS pattern doesn't port directly. _(added 2026-07-02)_
- **Track B (worker identity resolver)** — being shipped by a concurrent session (eq-cards PR #113 migrations 0070–0073 + eq-shell PRs #597/#598). DEPLOY ORDER: apply eq-cards `0073` via the governed pipeline BEFORE eq-shell #597 ships (else the new RPC 404s). Needs Royce deploy approval. _(added 2026-07-02)_
- **Manual verification on a real device** that the welcome-scan flow now succeeds on the first attempt (not just on retry). _(added 2026-07-02)_
- **Send Huon** the connection-email reply + before/after graphic. _(needs your call)_
- **App-side `P0023` message polish (chip session)** — the name-gate on `eq_cards_submit_access_request` is live server-side, but the Flutter mapping of `P0023`→friendly message was drafted then rolled back; a blocked worker currently sees raw `ServerFailure(500): Add your name…`. Rides the next gated Cards deploy. _(added 2026-07-02)_
- **Live-verify `cards-export-licences`, `comms-jobs`, `admin-audit` actually 403 on a disallowed Origin** — blocked this session by a sandbox DNS failure, not urgent (same code as 2 already-confirmed endpoints) but not yet directly proven. _(needs a retry, low priority)_
- **Confirm the activity panel actually shows an event** — carried over unchanged from the prior close; still needs Royce to make one real change on `/admin/access-control` and check the panel. _(needs your call)_
- **Confirm the activity panel actually shows an event** — toggle a role permission or edit a group on `/admin/access-control` and check the new "Recent activity" section renders it. _(needs your call — still open)_
- **Verify `ANTHROPIC_API_KEY` is actually live on sks-canonical for the Ask tab** — code is real and correctly wired, but no Edge Function invocations in the last 24h of logs; needs Royce to type one question into the live Ask tab and report back. _(needs your call)_
_…and 183 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-02 11:06 UTC._

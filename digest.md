---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-29
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-29 19:32 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-29 19:30 UTC → 2026-06-29 19:32 UTC)

- Merged: eq-shell [#527](https://github.com/eq-solutions/eq-shell/pull/527) feat(gm-reports): carry forward invoice run statuses to new 
- Merged: eq-shell [#526](https://github.com/eq-solutions/eq-shell/pull/526) fix(gm-reports): clamp invoice popover to viewport right edg
- Merged: eq-shell [#519](https://github.com/eq-solutions/eq-shell/pull/519) fix(staff): employment type dropdown + hide retired quotes m
- Merged: eq-shell [#518](https://github.com/eq-solutions/eq-shell/pull/518) feat(admin): EQ Service admin tiles in Shell Admin hub
- Merged: eq-shell [#517](https://github.com/eq-solutions/eq-shell/pull/517) feat(crm): site Maps link + Places autocomplete (key-gated)
- Merged: eq-shell [#516](https://github.com/eq-solutions/eq-shell/pull/516) fix(staff): approval 500 + subcontractor role + audit harden
- Merged: eq-shell [#515](https://github.com/eq-solutions/eq-shell/pull/515) feat(crm): site address + contact picker
- Merged: eq-shell [#514](https://github.com/eq-solutions/eq-shell/pull/514) fix(equipment): cert-import-parse-background 500 — return Re

## ⚠ Needs you (3)

- 🔴 **Substrate drift** — DRIFT: supabase eq-solves-field (ktmjmdzqrogauaevbktn): claimed LIVE but reality looks DEAD
- 🟠 **Sentry new error** — `eq-shell` [EQ Field handoff HTTP 403](https://eq-solutions.sentry.io/issues/130938311/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 6 | 1d |
| eq-field | ✓ success | 26d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff HTTP 403](https://eq-solutions.sentry.io/issues/130938311/) | 3 | 2026-06-29 |
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-shell | [captureServerError](https://eq-solutions.sentry.io/issues/130413967/) | 2 | 2026-06-29 |
| eq-shell | [EQ Service iframe did not load within timeout](https://eq-solutions.sentry.io/issues/130169257/) | 2 | 2026-06-29 |
| eq-shell | [EQ Field handoff network error: Load failed](https://eq-solutions.sentry.io/issues/130061083/) | 2 | 2026-06-29 |
| eq-cards | [minified:CW: AuthRetryableFetchException(message: ClientException: Failed to fet](https://eq-solutions.sentry.io/issues/130861353/) | 1 | 2026-06-28 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-29 | eq-shell | [#542](https://github.com/eq-solutions/eq-shell/pull/542) feat(customers): customer-level Field/Service toggles in the head |
| 2026-06-29 | eq-shell | [#541](https://github.com/eq-solutions/eq-shell/pull/541) feat(customers): site street address + Field/Service toggles per  |
| 2026-06-29 | eq-shell | [#540](https://github.com/eq-solutions/eq-shell/pull/540) fix(customers): Add Site 500 — remove non-existent site_contact_i |
| 2026-06-29 | eq-shell | [#539](https://github.com/eq-solutions/eq-shell/pull/539) feat(audit): Tenant Activity Log — who changed what on the canoni |
| 2026-06-29 | eq-shell | [#536](https://github.com/eq-solutions/eq-shell/pull/536) fix: staff edit 500, audit log, employment type, Add Site modal |
| 2026-06-29 | eq-shell | [#538](https://github.com/eq-solutions/eq-shell/pull/538) feat(notifications): range-based worker reminders + SMS opt-out |
| 2026-06-29 | eq-shell | [#537](https://github.com/eq-solutions/eq-shell/pull/537) fix(notifications): repoint licence-expiry scheduler to eq-canoni |
| 2026-06-29 | eq-shell | [#534](https://github.com/eq-solutions/eq-shell/pull/534) polish(shell): staff approval fixes, compliance pack, site/custom |
| 2026-06-29 | eq-shell | [#535](https://github.com/eq-solutions/eq-shell/pull/535) fix(equipment): cert-import 500 — read body before waitUntil + ad |
| 2026-06-29 | eq-shell | [#533](https://github.com/eq-solutions/eq-shell/pull/533) fix(auth): upsert membership to handle existing inactive rows |
| 2026-06-29 | eq-shell | [#532](https://github.com/eq-solutions/eq-shell/pull/532) fix(iframes): suppress Sentry errors from background pre-warm ifr |
| 2026-06-29 | eq-shell | [#531](https://github.com/eq-solutions/eq-shell/pull/531) fix(auth): resend Shell invite instead of blocking |
| 2026-06-29 | eq-shell | [#530](https://github.com/eq-solutions/eq-shell/pull/530) fix(auth): promote Cards-worker stub on invite accept |
| 2026-06-29 | eq-shell | [#529](https://github.com/eq-solutions/eq-shell/pull/529) feat(eq-ops): clickable status badge in quote detail panel |
| 2026-06-29 | eq-shell | [#528](https://github.com/eq-solutions/eq-shell/pull/528) fix(cards): overwrite stale workers.staff_id on approval |
_Showing 15 of 110 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Verify header→GUC actor capture** — confirm `actor_id` populates on the first real UI edit; if it shows "Automatic", the change still logs but who-attribution needs a follow-up _(added 2026-06-30)_
- **Activity Log — team & access events** — invites / role-changes as app-level writes to the tenant plane (no spine row to trigger on) _(added 2026-06-30)_
- **Activity Log — link-table triggers** — contact_customer_links, contact_site_links _(added 2026-06-30)_
- **Platform Security Log / operator console** — sign-ins/2FA audit (jvkn), operator-only, separate from the tenant page _(added 2026-06-30)_
- **Set Twilio env on eq-shell Netlify** — `EQ_SMS_PROVIDER=twilio` + `TWILIO_ACCOUNT_SID/AUTH_TOKEN/FROM_NUMBER`; SMS is log-only until then (email works) _(added 2026-06-29)_
- **Set `SCHEDULER_TEST_SECRET`** on eq-shell Netlify to use the test endpoint _(added 2026-06-29)_
- **Set SKS compliance email** at core.eq.solutions/sks/settings to activate the employer 7-day alert _(added 2026-06-29)_
- **Field-only workers** (ehow `app_data.licences`, no Cards wallet) not covered by the scheduler _(added 2026-06-29)_
- **Employer 7-day alert still exact-day** (worker path hardened to range-based; Monday digest is the backstop) _(added 2026-06-29)_
- **Worker→new-company bridge** (worker-vouched provision token + Cards "invite my employer" screen) — Phase 3, only if companies pull; touches provisioning/auth (Royce sign-off) _(added 2026-06-29)_
_…and 129 more · [eq/pending.md](eq/pending.md)_

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

✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-29 19:32 UTC._

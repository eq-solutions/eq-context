---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-06-29
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-06-29 03:13 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-06-29 03:08 UTC → 2026-06-29 03:13 UTC)

- Merged: eq-shell [#529](https://github.com/eq-solutions/eq-shell/pull/529) feat(eq-ops): clickable status badge in quote detail panel
- Merged: eq-shell [#514](https://github.com/eq-solutions/eq-shell/pull/514) fix(equipment): cert-import-parse-background 500 — return Re
- Merged: eq-shell [#512](https://github.com/eq-solutions/eq-shell/pull/512) chore: drop public.sks_quotes_* legacy tables + fix stale ca
- Merged: eq-shell [#509](https://github.com/eq-solutions/eq-shell/pull/509) feat(equipment): async cert import — background function + B
- Merged: eq-shell [#507](https://github.com/eq-solutions/eq-shell/pull/507) fix(equipment): Haiku + hard deadline to beat Netlify 26s wa
- Merged: eq-shell [#506](https://github.com/eq-solutions/eq-shell/pull/506) fix(equipment): cert import bundles without @eq/schemas (was
- Merged: eq-shell [#504](https://github.com/eq-solutions/eq-shell/pull/504) fix(equipment): surface the real cert-import error (no more 
- Merged: eq-shell [#503](https://github.com/eq-solutions/eq-shell/pull/503) feat(crm): entityCapabilities policy map (archive/delete/mer

## ⚠ Needs you (3)

- 🔴 **Substrate drift** — DRIFT: supabase eq-solves-field (ktmjmdzqrogauaevbktn): claimed LIVE but reality looks DEAD
- 🟠 **Sentry new error** — `eq-cards` [minified:CW: AuthRetryableFetchException(message: ClientExce](https://eq-solutions.sentry.io/issues/130861353/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 1 | 0d |
| eq-field | ✓ success | 25d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Cards iframe did not fire onLoad within 30s](https://eq-solutions.sentry.io/issues/130446042/) | 2 | 2026-06-29 |
| eq-cards | [minified:CW: AuthRetryableFetchException(message: ClientException: Failed to fet](https://eq-solutions.sentry.io/issues/130861353/) | 1 | 2026-06-28 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-06-29 | eq-shell | [#529](https://github.com/eq-solutions/eq-shell/pull/529) feat(eq-ops): clickable status badge in quote detail panel |
| 2026-06-29 | eq-shell | [#528](https://github.com/eq-solutions/eq-shell/pull/528) fix(cards): overwrite stale workers.staff_id on approval |
| 2026-06-29 | eq-shell | [#527](https://github.com/eq-solutions/eq-shell/pull/527) feat(gm-reports): carry forward invoice run statuses to new perio |
| 2026-06-29 | eq-shell | [#526](https://github.com/eq-solutions/eq-shell/pull/526) fix(gm-reports): clamp invoice popover to viewport right edge (pr |
| 2026-06-29 | eq-shell | [#525](https://github.com/eq-solutions/eq-shell/pull/525) fix(gm-reports): refresh uploaded_at on re-upload |
| 2026-06-29 | eq-shell | [#524](https://github.com/eq-solutions/eq-shell/pull/524) fix(gm-reports): clamp invoice popover to viewport right edge |
| 2026-06-29 | eq-shell | [#513](https://github.com/eq-solutions/eq-shell/pull/513) fix(docs): correct stale EQ_SECRET_SALT guidance — HMAC retired 2 |
| 2026-06-29 | eq-shell | [#523](https://github.com/eq-solutions/eq-shell/pull/523) fix(identity): update tenant-routing comment — EQ Solutions slug  |
| 2026-06-28 | eq-shell | [#522](https://github.com/eq-solutions/eq-shell/pull/522) fix(auth): audit log writes + users page shows all tenant members |
| 2026-06-28 | eq-shell | [#521](https://github.com/eq-solutions/eq-shell/pull/521) feat(equipment): multi-document cert import batching — one AI cal |
| 2026-06-28 | eq-shell | [#520](https://github.com/eq-solutions/eq-shell/pull/520) fix(build): TS errors blocking Netlify — SMS fields + mapSite + E |
| 2026-06-28 | eq-shell | [#519](https://github.com/eq-solutions/eq-shell/pull/519) fix(staff): employment type dropdown + hide retired quotes module |
| 2026-06-28 | eq-shell | [#518](https://github.com/eq-solutions/eq-shell/pull/518) feat(admin): EQ Service admin tiles in Shell Admin hub |
| 2026-06-28 | eq-shell | [#517](https://github.com/eq-solutions/eq-shell/pull/517) feat(crm): site Maps link + Places autocomplete (key-gated) |
| 2026-06-28 | eq-shell | [#516](https://github.com/eq-solutions/eq-shell/pull/516) fix(staff): approval 500 + subcontractor role + audit hardening |
_Showing 15 of 110 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **gitleaks pre-commit hook** — prevent PAT exposure in substrate history _(added 2026-06-28)_
- **Update C:\Projects\.git-credentials** files with new PAT after rotation _(added 2026-06-28)_
- **Token refresh smoke test** — shorten TTL locally to confirm ShellTokenRefresh fires (4h is hard to test live) _(added 2026-06-28)_
- **gitleaks pre-commit hook** — prevent PAT exposure in substrate history
- **Update C:\Projects\.git-credentials** files with new PAT after rotation
- Remaining items carried from 2026-06-18 (see below)
- **Curate `sites.field_enabled`** — 591 all enabled → trim to live jobs
- **Login hook** (phone-dedup) — workers still can't sign in (separate track; `ops/decisions.md`).
- **Curate `sites.field_enabled`** — 591 all enabled → trim to live jobs.
- **Daniel Bower** — confirm leaver / remove.
_…and 112 more · [eq/pending.md](eq/pending.md)_

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
| 2026-06-28 | [Brain 10/10: substrate coherence + automation layer](sessions/2026-06-28-brain-10-10.md) |
| 2026-06-28 | [EQ Service batch-create fix](sessions/2026-06-28-batch-create-fix.md) |
| 2026-06-27 | [2026-06-27 — Usability sprint + security gate promotion](sessions/2026-06-27-usability-sprint.md) |
| 2026-06-27 | [Substrate-coherence sprint — honesty CI + security gate + digest + Node 24 bump](sessions/2026-06-27-substrate-coherence-sprint.md) |
| 2026-06-26 | [Session: Safety docs footer parity](sessions/2026-06-26-footer-parity.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-06-29 03:13 UTC._

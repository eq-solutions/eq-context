---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-13
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-13 09:35 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-13 09:30 UTC → 2026-07-13 09:35 UTC)

- Merged: eq-shell [#800](https://github.com/eq-solutions/eq-shell/pull/800) fix(auth): create auth.users before shell user on invite acc
- Merged: eq-shell [#799](https://github.com/eq-solutions/eq-shell/pull/799) feat(labour-hire): add 'week' rate unit for once-a-week char
- Merged: eq-shell [#792](https://github.com/eq-solutions/eq-shell/pull/792) feat(comms): crew-gaps strip — where the labour issues are, 
- Merged: eq-shell [#791](https://github.com/eq-solutions/eq-shell/pull/791) fix(comms): job list fills the window + job numbers never tr
- Merged: eq-shell [#790](https://github.com/eq-solutions/eq-shell/pull/790) fix(security): protect plant_equipment from customer-asset i
- Merged: eq-shell [#788](https://github.com/eq-solutions/eq-shell/pull/788) fix(comms): make the job list readable — wrap Work, wider pa
- Merged: eq-shell [#787](https://github.com/eq-solutions/eq-shell/pull/787) fix(security): scope anon's read of public.organisations to 
- Merged: eq-shell [#786](https://github.com/eq-solutions/eq-shell/pull/786) fix(security): revoke anon write grants on jvkn control-plan

## ⚠ Needs you (4)

- 🟠 **PR aging 7d** — eq-solves-service [#459](https://github.com/eq-solutions/eq-service/pull/459) "chore(deps-dev): bump @vitejs/plugin-react from 6.0.1 to 6.0.3"
- 🟠 **PR aging 7d** — eq-solves-service [#458](https://github.com/eq-solutions/eq-service/pull/458) "chore(deps): bump tailwind-merge from 3.5.0 to 3.6.0"
- 🟠 **PR aging 7d** — eq-solves-service [#456](https://github.com/eq-solutions/eq-service/pull/456) "chore(deps-dev): bump tailwindcss from 4.2.2 to 4.3.2"
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 3d |
| eq-solves-service | ✓ success | 0d ago | 5 | 7d |
| eq-field | ✓ success | -1d ago | 2 | 1d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/) | 19 | 2026-07-08 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-13 | eq-shell | [#808](https://github.com/eq-solutions/eq-shell/pull/808) refactor(labour-hire): drop #805 focus workaround now Modal fix s |
| 2026-07-13 | eq-shell | [#658](https://github.com/eq-solutions/eq-shell/pull/658) fix(dashboard): surface pending staff connections on home sidebar |
| 2026-07-13 | eq-shell | [#807](https://github.com/eq-solutions/eq-shell/pull/807) chore(deps): bump @eq-solutions/ui to v1.10.1 (Modal focus-trap f |
| 2026-07-13 | eq-shell | [#806](https://github.com/eq-solutions/eq-shell/pull/806) feat(mobile): foundation envelope fixes + first-touch polish |
| 2026-07-13 | eq-shell | [#805](https://github.com/eq-solutions/eq-shell/pull/805) fix(labour-hire): Add-rate modal loses focus on every keystroke |
| 2026-07-13 | eq-shell | [#804](https://github.com/eq-solutions/eq-shell/pull/804) feat(labour-hire): weekly cost grouped by agency — concise 4-colu |
| 2026-07-13 | eq-shell | [#803](https://github.com/eq-solutions/eq-shell/pull/803) fix(labour-hire): weekly cost was dropping 'Travel & Fares' / 'ME |
| 2026-07-13 | eq-shell | [#802](https://github.com/eq-solutions/eq-shell/pull/802) fix(labour-hire): modal focus loss + wide weekly-cost table + tol |
| 2026-07-13 | eq-shell | [#801](https://github.com/eq-solutions/eq-shell/pull/801) feat(labour-hire): Redundancy in the weekly cost + agency/rate-ty |
| 2026-07-13 | eq-solves-service | [#519](https://github.com/eq-solutions/eq-service/pull/519) fix(import): dedupe register Asset# within a batch + import spinn |
| 2026-07-13 | eq-solves-service | [#517](https://github.com/eq-solutions/eq-service/pull/517) chore(deps): bump @eq-solutions/ui v1.9.0 → v1.10.1 (Modal focus- |
| 2026-07-13 | eq-solves-service | [#516](https://github.com/eq-solutions/eq-service/pull/516) feat(import/assets): skip plan-less register rows by default + as |
| 2026-07-13 | eq-field | [#474](https://github.com/eq-solutions/eq-field/pull/474) v3.5.314 — mobile device-pass polish (week nav, save pill, icons, |
| 2026-07-13 | eq-field | [#473](https://github.com/eq-solutions/eq-field/pull/473) fix(field): visible confirmation on crew add + retire "What's new |
| 2026-07-13 | eq-field | [#472](https://github.com/eq-solutions/eq-field/pull/472) v3.5.312 — mobile reflow slice 2: Dashboard / Job Numbers / Leave |
_Showing 15 of 115 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Royce device-confirm the Field add-crew fix on his phone** once v3.5.308 deploys — the exact mobile add-crew mechanism (Add button under keyboard vs `list=` datalist intercepting the tap) was unproven from code; Enter-to-add is the safe slice, may still need a CSS/layout pass. _(added 2026-07-13)_
- **Field mobile-first reflow (simple, must respect security groups)** — the real remaining crew-mobile work; lives in eq-field. Parked eq-shell native-page mobile (Customers/Ops master-detail, nav-model unification, PWA-standalone install — auth-hub cookie risk) explicitly deprioritized per Royce ("Field is focus"). _(added 2026-07-13)_
- **Royce phone-smoke slices 1–3 inside the Core iframe (`?tenant=sks`)** — the three reflowed screens + the clamp on a real device; the embedded iframe is the one surface Claude can't drive from here. _(added 2026-07-13)_
- **Full `.eqh-tile` markup migration onto `.eqf-mcard`** — slice 1 only token-aligned the home launcher tiles at the CSS level (no `home.js` change) to dodge a collision with the then-open #469, which has since merged. The tile can now be migrated properly onto the shared primitive markup. Low priority — it's a launcher tile, not a data card, so a full migration is optional cleanup, not a fix. _(added 2026-07-13)_
- **One-login BUILD (P1–P5) — NOT started (explore/plan only)**: P1 identity-via-Core, P2 Core mobile home (My Card + Field tiles), P3 canonical completeness RPC (the one net-new piece), P4 grace-gate, P5 migrate SKS + harden. P1 auth is lower near-term value (SKS already logs in via Core) AND overlaps eq-shell's in-flight mobile-foundation branch — coordinate before building. _(added 2026-07-13, needs your go — auth-flow change)_
- **Correct the stale "63 SKS invites" figure** wherever referenced — live = 20 shell user_invites + 2 worker_invites; SKS org_memberships 34; workers 89 (87 unique phones, 39 auth-linked). _(added 2026-07-13)_
- **Dependabot PR #466 open** — auto-patches eq-field CI action versions. Low-risk, Royce to merge. _(added 2026-07-13)_
- **Pre-existing (NOT security): Field reminder/digest/TAFE features are missing config secrets (`TENANT_UUID` etc.) on ehow** → they'd error on a real run, so may not be working. Royce to decide if they're meant to be live. _(added 2026-07-13)_
- **Security roadmap PARKED behind a trigger** — Trust-page draft + `security-register.md` in `scratchpad/`. Phase 1 = Royce's alert click-list + rotate the jvkn service key + GitHub Dependabot/secret-scanning org-wide. SOC 2 / rented 24/7 monitoring (MDR) / Cloudflare WAF (apps are direct-to-Netlify, not behind CF) PARKED until a real deal, a 3rd tenant, or EQ goes external. _(added 2026-07-13)_
- **Leif still needs to accept** — his invite is valid/unused (token regenerated 2026-07-13, expires 07-20). Royce sending him the link + the how-to page (`scratchpad/leif-signin-howto.html`, artifact `de35bebb`). _(added 2026-07-13)_
_…and 329 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
- **eq-shell PR #681 needs review + merge** — fix is already live on ehow (applied directly ahead of the PR); the PR just brings the source-controlled migration back in sync. _(added 2026-07-06)_
_…and 53 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-13 | [SKS plant & equipment restored after a manual asset-register wipe; 2FA grace unchanged](sessions/2026-07-13.md) |
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
| 2026-07-12 | [Session — Substrate Plan v2 (the notebook that tells the truth)](sessions/2026-07-12-substrate-plan-v2.md) |
| 2026-07-11 | [CEO meeting prep for SKS Labour → Cards is the strategic standout](sessions/2026-07-11.md) |
| 2026-07-11 | [The read path lied, and NSW isn't finishing work](sessions/2026-07-11-substrate-delivery-and-nsw-audit.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-13 09:35 UTC._

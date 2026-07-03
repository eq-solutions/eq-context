---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-03
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-03 09:47 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-03 07:54 UTC → 2026-07-03 09:47 UTC)

- Merged: eq-shell [#627](https://github.com/eq-solutions/eq-shell/pull/627) fix(provisioning): convert provision-tenant to a background 
- Merged: eq-shell [#626](https://github.com/eq-solutions/eq-shell/pull/626) fix(admin): resolve --eq-ink to a real hex value for the wor
- Merged: eq-shell [#625](https://github.com/eq-solutions/eq-shell/pull/625) feat(security): view security_invoker invariant (CHECK 7) + 
- Merged: eq-shell [#624](https://github.com/eq-solutions/eq-shell/pull/624) fix(provisioning): tenant_routing NOT NULL columns block eve
- Merged: eq-shell [#623](https://github.com/eq-solutions/eq-shell/pull/623) fix(intake): re-vendor field-name + plain-English fixes from
- Merged: eq-shell [#608](https://github.com/eq-solutions/eq-shell/pull/608) fix(governance): contact-tables gate red — relkind-aware 015
- Merged: eq-shell [#601](https://github.com/eq-solutions/eq-shell/pull/601) Customers/Staff legibility + EQ Ops board fixes + design-tok
- Merged: eq-shell [#600](https://github.com/eq-solutions/eq-shell/pull/600) fix(customers): migrate address autocomplete to new Places A

## ⚠ Needs you (3)

- 🟠 **Sentry new error** — `eq-shell` [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/)
- 🟠 **Sentry new error** — `eq-field` [SyntaxError: Unexpected end of input](https://eq-solutions.sentry.io/issues/131931795/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 3 | 4d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Invalid hex color: var(--eq-ink)](https://eq-solutions.sentry.io/issues/131632698/) | 6 | 2026-07-03 |
| eq-cards | [minified:I3: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-07-01 |
| eq-field | [SyntaxError: Unexpected end of input](https://eq-solutions.sentry.io/issues/131931795/) | 2 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
| eq-cards | [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/) | 1 | 2026-07-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/131636027/) | 1 | 2026-07-02 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-03 | eq-shell | [#627](https://github.com/eq-solutions/eq-shell/pull/627) fix(provisioning): convert provision-tenant to a background funct |
| 2026-07-03 | eq-shell | [#626](https://github.com/eq-solutions/eq-shell/pull/626) fix(admin): resolve --eq-ink to a real hex value for the worker Q |
| 2026-07-03 | eq-shell | [#623](https://github.com/eq-solutions/eq-shell/pull/623) fix(intake): re-vendor field-name + plain-English fixes from eq-s |
| 2026-07-03 | eq-shell | [#625](https://github.com/eq-solutions/eq-shell/pull/625) feat(security): view security_invoker invariant (CHECK 7) + field |
| 2026-07-03 | eq-shell | [#624](https://github.com/eq-solutions/eq-shell/pull/624) fix(provisioning): tenant_routing NOT NULL columns block every Pr |
| 2026-07-03 | eq-shell | [#620](https://github.com/eq-solutions/eq-shell/pull/620) fix(ci): check-migration-hygiene.mjs skips SQL line comments |
| 2026-07-03 | eq-shell | [#618](https://github.com/eq-solutions/eq-shell/pull/618) fix(security): reassert security_invoker on field_managers + nomi |
| 2026-07-03 | eq-shell | [#622](https://github.com/eq-solutions/eq-shell/pull/622) Tenants page: edit tier/modules, archive/reactivate |
| 2026-07-03 | eq-shell | [#621](https://github.com/eq-solutions/eq-shell/pull/621) fix(ops): remove broken per-column Status filter in table view |
| 2026-07-03 | eq-shell | [#619](https://github.com/eq-solutions/eq-shell/pull/619) fix(field-iframe): preserve deep-linked ?tab= on initial tenant a |
| 2026-07-03 | eq-shell | [#613](https://github.com/eq-solutions/eq-shell/pull/613) feat(customers): batch delete/archive for sites |
| 2026-07-03 | eq-shell | [#614](https://github.com/eq-solutions/eq-shell/pull/614) feat(staff): Add-to-roster action — dedupe-first roster-only crea |
| 2026-07-03 | eq-shell | [#616](https://github.com/eq-solutions/eq-shell/pull/616) feat(ops): create and edit sites from the EQ Ops quote form |
| 2026-07-03 | eq-shell | [#615](https://github.com/eq-solutions/eq-shell/pull/615) fix(ops): quote PDF download/email returned 404 for every quote — |
| 2026-07-03 | eq-shell | [#612](https://github.com/eq-solutions/eq-shell/pull/612) fix(governance): adopt quality-guardian tables — tenant-JWT polic |
_Showing 15 of 129 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **12 contacts missing first/last name, categorized** — 2 safely inferable from email pattern (Pashon Jima at ap.equinix.com → last name "Jima"; Benoit Kon at digi-co.com.au → last name "Kon"), 1 data-import bug (company name "Metronode" landed in `first_name` with a garbled fragment in `position` — needs a real fix, not a name), 1 unrecoverable ("Rafael", no email/signal), 8 are role/department mailboxes ("Accounts", "Payables", "Reception") not people — filling a `last_name` for those would be fabricating data. Declined to hand-write any of this via raw SQL (bypasses the governed audit path this whole day's work has been about) — needs your call on fix path (dashboard tidy flow, once the Tidy-tab Edit lands live, is now a real option for the 2 inferable ones). _(added 2026-07-03, needs your call)_
- **Licence renewals surfaced by the quality-guardian run** — Huon Henne's LVR (CRT850747) expired 2025-10-08, 268 days overdue, critical; Rhys Scott's electrical licence (371332C) expires in 25 days; Brian Griffin-Colls' LVR (UETDRMP007) expires in 29 days. Can't action from here — needs the actual updated licence documents from each person. _(added 2026-07-03, needs your call)_
- **137-item review queue is not agent-workable** — checked before bulk-approving anything: every item across every category, including the "one-click" trade/link/format ones, is explicitly low/medium confidence with the adjudication panel that built the queue having already declined to auto-commit ("per-person trade unproven, confirm," "adjudication panel rejected auto-commit 0/3," "not resolvable from canonical data"). There's no genuinely mechanical subset — every item needs someone who knows the specific person/customer. _(added 2026-07-03, needs your call)_
- **Browser verification of the new Tidy-tab Edit/Suggest + Dupes multi-group fix** — no component-test infra exists for `@eq/intake-demo` (no testing-library/jsdom), and no live authenticated session was available to click through it. Verified via strict `tsc -b` + full existing test suites + careful code tracing only. Next session with a live login: open a Tidy tab with gaps, Edit one inline, Suggest one, confirm only the intended row changes; open Dupes and confirm more than one duplicate group can now show per field; confirm Site Name renders on the Sites Gaps/All view. _(added 2026-07-03, needs your call)_
- **Mandatory prod dry run** — `shell_control.provision_tokens` is still 0 rows ever as of session close. Generate a real link (test org + spare phone) through Admin → Tenants, walk it through Cards including the phone-mismatch rejection, confirm the workspace lands correctly and the `tenant_slug` handoff opens the right tenant, then archive the test tenant via the new #622 UI. **Do this before sending a link to a real prospect.** _(added 2026-07-03, needs your call)_
- **`EQ_PLATFORM_NOTIFY_EMAIL`** — optional Netlify env var, not yet set. If set, you get an email whenever a provision link is redeemed. No redeploy needed — functions read it live. _(added 2026-07-03, needs your call)_
- **Delete stale remote branch `claude/staff-add-to-roster`** — a concurrent session's branch-switch in the shared checkout caused the first push attempt to land on the wrong branch pointing at an unrelated commit; recovered by opening the PR from `-v2` instead, but the stale remote ref is still there (`git push origin --delete claude/staff-add-to-roster`) and the classifier blocked the agent from deleting it. _(added 2026-07-03, needs your call)_
- **Merge eq-intake #58** — ledger checksum convention (the live rows are already backfilled by hand; merging just lands the convention in the repo so future self-inserts don't regress). Still open, mergeable, not blocking anything now the gate is clean. _(added 2026-07-03, needs your call)_
- **Work the 137-item review queue** — the tab is live; trades/links/formats are one-click, emergency contacts need info Royce has to source. _(added 2026-07-03, needs your call)_
- **sql/061_steward_commit_batch.sql — staged, NOT applied** — server-side `eq_steward_commit_batch` RPC (service-role-only, whitelist + event lifecycle inside) for steward run 002; apply when a second run is wanted. _(added 2026-07-03)_
_…and 207 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- At least one SKS person ("Collin ... Toohey") has no record in canonical `app_data.staff`, blocking their leave submissions — data-ops backfill needed, not a code fix _(added 2026-07-03)_
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- Book monthly check-in cadence with Richo (Michael Richardson)
- Tell Mark about catch-up conversations before starting (casual, no fanfare)
_…and 18 more · [sks/pending.md](sks/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-03 09:47 UTC._

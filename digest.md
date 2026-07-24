---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-24
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-24 01:34 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-24 01:24 UTC → 2026-07-24 01:34 UTC)

- Merged: eq-shell [#986](https://github.com/eq-solutions/eq-shell/pull/986) feat(customers): show what matched a search result
- Merged: eq-shell [#984](https://github.com/eq-solutions/eq-shell/pull/984) fix(customers): backfill market_vertical from customer_group
- Merged: eq-shell [#982](https://github.com/eq-solutions/eq-shell/pull/982) fix(modals): apply useOverlayClickOutside across remaining b
- Merged: eq-shell [#980](https://github.com/eq-solutions/eq-shell/pull/980) fix(sites): address autocomplete hid saved addresses + doubl
- Merged: eq-shell [#977](https://github.com/eq-solutions/eq-shell/pull/977) feat(customers,ops): market vertical, invoice email, end cli
- Merged: eq-shell [#975](https://github.com/eq-solutions/eq-shell/pull/975) fix(identity): list-members backfills name/email from app_da
- Merged: eq-shell [#973](https://github.com/eq-solutions/eq-shell/pull/973) perf(quotes): bound the Ops pipeline fetch, add a real count
- Merged: eq-shell [#972](https://github.com/eq-solutions/eq-shell/pull/972) fix(ops): Suppliers column widths + stale cross-tenant JWT c

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-solves-service` [UnrecognizedActionError: Server Action "4073d2dc7728208efb4f](https://eq-solutions.sentry.io/issues/122209933/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 2d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 10 | 2026-07-23 |
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 6 | 2026-07-23 |
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 4 | 2026-07-23 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-24 | eq-shell | [#1001](https://github.com/eq-solutions/eq-shell/pull/1001) feat(ops): Excel-style multiselect filters + fix labour-hire futu |
| 2026-07-24 | eq-shell | [#999](https://github.com/eq-solutions/eq-shell/pull/999) fix(quotes): Coupa import shows import outcome + job title |
| 2026-07-24 | eq-shell | [#998](https://github.com/eq-solutions/eq-shell/pull/998) feat(customers,quotes): customer-level default End Client |
| 2026-07-24 | eq-shell | [#996](https://github.com/eq-solutions/eq-shell/pull/996) fix+feat(quotes): Coupa PO import — fix the broken write path, re |
| 2026-07-24 | eq-shell | [#997](https://github.com/eq-solutions/eq-shell/pull/997) feat(quotes): suggest the customer's last End Client on new quote |
| 2026-07-24 | eq-solves-service | [#601](https://github.com/eq-solutions/eq-service/pull/601) feat(maintenance): Excel-style checklist filters on the Assets ta |
| 2026-07-23 | eq-shell | [#995](https://github.com/eq-solutions/eq-shell/pull/995) docs(ledger): record reconcile_worker_sync migration as applied |
| 2026-07-23 | eq-shell | [#994](https://github.com/eq-solutions/eq-shell/pull/994) chore(migrations): codify eq_reconcile_worker_sync() + support ta |
| 2026-07-23 | eq-shell | [#993](https://github.com/eq-solutions/eq-shell/pull/993) fix(workers-canonical-sync): stop nightly reconciler from un-arch |
| 2026-07-23 | eq-shell | [#992](https://github.com/eq-solutions/eq-shell/pull/992) fix(auth): self-heal shell login for staff approved before Cards  |
| 2026-07-23 | eq-shell | [#991](https://github.com/eq-solutions/eq-shell/pull/991) fix(ops): job-creation export never actually populated the new fi |
| 2026-07-23 | eq-shell | [#990](https://github.com/eq-solutions/eq-shell/pull/990) fix(login): rename stale Quotes tile to Ops |
| 2026-07-23 | eq-shell | [#989](https://github.com/eq-solutions/eq-shell/pull/989) fix(quotes): simplify quote-detail panel; rebuild Coupa PO import |
| 2026-07-23 | eq-shell | [#988](https://github.com/eq-solutions/eq-shell/pull/988) chore(migrations): renumber 0197_quote_list_pagination_counts ->  |
| 2026-07-23 | eq-shell | [#987](https://github.com/eq-solutions/eq-shell/pull/987) perf(customers): run the 3 customer-detail lookups in parallel |
_Showing 15 of 109 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **What's the actual remaining pain point for direct employees, now that the Cards→Field pipe is confirmed live end-to-end?** Asked Royce directly — is it that head office doesn't trust/re-checks Field data before their manual Upvise upload, or a different gap not yet found. Not answered yet this session. _(added 2026-07-24)_
- **Follow-up: `guard.js` itself is unversioned and untested.** It lives at `~/.claude/hooks/guard.js`, outside any git repo, with zero test coverage (beyond the ad hoc verification above) — unlike `hooks/*.py` in this repo, which are governed/versioned/CI-checked (`hooks/README.md`). Its own header cites a spec file (`system/operating-model-roadmap.md`) that doesn't exist. Worth eventually mirroring guard.js into this repo (versioned source of truth, deployed copy on the Beelink) so it gets the same test-before-trust discipline as the Python hooks. Not fixed this session — separate, larger scope. _(added 2026-07-24)_
- **Not yet confirmed by Royce that the 5 originally-reported people stay archived overnight.** Everything above is verified via the live function version + the fix's own logic, not a "come back tomorrow and check" from Royce himself yet. _(added 2026-07-24)_
- **`eq_reconcile_worker_sync()` (the nightly dispatcher itself, jvkn `pg_cron` job id 2) still isn't tracked in any repo migration** — a governance gap independent of the bug above, not touched by this fix. Not urgent now that the harmful write is gone, but worth bringing under the normal migration pipeline at some point. _(added 2026-07-24)_
- **Not yet confirmed working end-to-end by Royce.** He tested once and got no receipts in the zip — root-caused to him re-downloading a *pre-existing* Past Exports history row generated before this session's fix (immutable — old rows never gain the bundling retroactively), not a code bug. Live-pulled the deployed function source to confirm the real fix is active. Told him to click "Generate claim form" again for a fresh `.zip` and report back — session ended before that confirmation came in. _(added 2026-07-24)_
- **The purchase-order matching database update applied live under one filename, then had to be renamed to avoid clashing with someone else's unrelated update — the tracking record on both company databases still shows the old name.** The fix itself is live and working correctly either way; this is a pure bookkeeping mismatch. Needs one more approval click from Royce (`Tenant migrations (One Pipe)` workflow, "Reconcile tenant ledgers" option) to tidy up the record. _(added 2026-07-24)_
- **Still needs a real click-through by Royce** — this round was verified by re-running his own failed data through the fix directly and by the usual build/test checks, but nobody has run a fresh file through the *redesigned* review screen live yet. _(added 2026-07-24)_
- **Royce hasn't yet downloaded a fresh Run-Sheet to eyeball the fixed logo himself** — verified by generating and inspecting a sample file directly against the real SKS logo, not by his own click-through. _(added 2026-07-23)_
- **Not yet click-tested live in the browser** — all 5 Job Creation fields (B17/B27/B28/B29/B30) are wired and deployed, but nobody has actually set them on a real customer/job and pulled a fresh export to confirm every cell lands right. _(added 2026-07-23)_
- **Not yet click-tested live** — build-verified only; nobody has actually searched for a site/contact/contract on the real Customers page and confirmed the right label shows. _(added 2026-07-23)_
_…and 437 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Needs a real click-through before trusting it fully** — set a Market Vertical + invoice email on a real customer, then pull a fresh Job Creation export on one of their jobs and check the 3 cells actually come out right. _(added 2026-07-23)_
- **Still open — Royce to confirm: does SKS Indigenous Technologies need its own isolation** (separate from the state/division access model), given it's a distinct MD-led entity that may carry its own compliance obligations (e.g. Indigenous procurement certification)? Flagged, not answered. _(added 2026-07-23)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
- Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_
_…and 66 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 2661 | 453 | 11 |
| [SKS](sks/pending.md) | 514 | 76 | 85 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-24 | [EQ Ops quote-detail panel simplified + Coupa PO import rebuilt against the real export](sessions/2026-07-24.md) |
| 2026-07-23 | [Closed the crm-write/canonical-api entitlement design pass: no gate needed](sessions/2026-07-23.md) |
| 2026-07-22 | [SKS Safety: Incidents/Near Miss tab + Prestart copy-from-last, EQ Field regression found & fixed](sessions/2026-07-22.md) |
| 2026-07-21 | [eq-shell had its own copy of the licence-privacy gap; found, fixed, deployed, and smoke-tested](sessions/2026-07-21.md) |
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-24 01:34 UTC._

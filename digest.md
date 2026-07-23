---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-23
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-23 09:06 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-23 08:54 UTC → 2026-07-23 09:06 UTC)

- Merged: eq-shell [#982](https://github.com/eq-solutions/eq-shell/pull/982) fix(modals): apply useOverlayClickOutside across remaining b
- Merged: eq-shell [#968](https://github.com/eq-solutions/eq-shell/pull/968) fix(staff): resync from Cards can no longer skip already-syn
- Merged: eq-shell [#967](https://github.com/eq-solutions/eq-shell/pull/967) feat(identity-health): detect duplicate Shell accounts acros
- Merged: eq-shell [#958](https://github.com/eq-solutions/eq-shell/pull/958) Security: enforce module entitlement at the iframe-SSO minte
- Merged: eq-shell [#957](https://github.com/eq-solutions/eq-shell/pull/957) ci: one-time workflow to apply Sentry alert rules
- Merged: eq-shell [#955](https://github.com/eq-solutions/eq-shell/pull/955) fix(field-iframe): retry the handoff timeout path instead of
- Merged: eq-shell [#952](https://github.com/eq-solutions/eq-shell/pull/952) fix(ci): CHECK 2 anon-grant invariant excludes views — fixes
- Merged: eq-shell [#951](https://github.com/eq-solutions/eq-shell/pull/951) fix(cards): Cards-approved staff got a Shell membership born

## ⚠ Needs you (6)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-solves-service` [UnrecognizedActionError: Server Action "4073d2dc7728208efb4f](https://eq-solutions.sentry.io/issues/122209933/)
- 🟠 **Sentry new error** — `eq-shell` [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 3 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 3 | 2026-07-22 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-23 | eq-shell | [#982](https://github.com/eq-solutions/eq-shell/pull/982) fix(modals): apply useOverlayClickOutside across remaining backdr |
| 2026-07-23 | eq-shell | [#979](https://github.com/eq-solutions/eq-shell/pull/979) fix(quotes): simplify quote-detail panel to high-value info |
| 2026-07-23 | eq-shell | [#980](https://github.com/eq-solutions/eq-shell/pull/980) fix(sites): address autocomplete hid saved addresses + doubled su |
| 2026-07-23 | eq-shell | [#977](https://github.com/eq-solutions/eq-shell/pull/977) feat(customers,ops): market vertical, invoice email, end client + |
| 2026-07-23 | eq-shell | [#978](https://github.com/eq-solutions/eq-shell/pull/978) fix(quotes): follow-up removal, contact consolidation, two-row ac |
| 2026-07-23 | eq-shell | [#976](https://github.com/eq-solutions/eq-shell/pull/976) fix(quotes): simplify EQ Ops quote panel actions + status filter, |
| 2026-07-23 | eq-shell | [#975](https://github.com/eq-solutions/eq-shell/pull/975) fix(identity): list-members backfills name/email from app_data.st |
| 2026-07-23 | eq-shell | [#974](https://github.com/eq-solutions/eq-shell/pull/974) fix(staff): compliance pack export stuck re-downloading the first |
| 2026-07-23 | eq-solves-service | [#600](https://github.com/eq-solutions/eq-service/pull/600) fix(reports): correct colour logo + stable alignment in report he |
| 2026-07-23 | eq-solves-service | [#599](https://github.com/eq-solutions/eq-service/pull/599) fix(maintenance,reports): stop-crashing site lookup, resolve cano |
| 2026-07-23 | eq-solves-service | [#598](https://github.com/eq-solutions/eq-service/pull/598) fix(admin/users): add missing subcontractor entry to role label m |
| 2026-07-23 | eq-solves-service | [#597](https://github.com/eq-solutions/eq-service/pull/597) feat(maintenance): make Site and the check name editable on the c |
| 2026-07-23 | eq-solves-service | [#596](https://github.com/eq-solutions/eq-service/pull/596) fix(errors): gracefully recover from stale server-action IDs post |
| 2026-07-23 | eq-solves-service | [#595](https://github.com/eq-solutions/eq-service/pull/595) fix(maintenance): show check title on Kanban cycle cards |
| 2026-07-23 | eq-solves-service | [#594](https://github.com/eq-solutions/eq-service/pull/594) fix(reports): render tenant logo on Compliance Report |
_Showing 15 of 114 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Not yet click-tested live in the browser** — build/tests/lint all verified clean, but nobody has actually opened Edit Customer, set a Market Vertical, or pulled a fresh Job Creation export to confirm the 3 fields land in the right cells. _(added 2026-07-23)_
- **Client ID (B27) and Market Segment (B28) on the same export are still never filled** — same gap, just not part of what was asked this session. Worth a follow-up if full parity matters. _(added 2026-07-23)_
- **Identity model needs a second dimension: division, not just tenant/role.** The SKS org chart shows state alone doesn't match how the business actually reports — VIC's headcount splits across national functional divisions (Major Projects, Data Centre Solutions, AV, HV) that cut across every state. Recommended direction (not yet built): keep the single-tenant model (don't fork Supabase projects per state — see `system/architecture.md` Control Layer section for why physical separation is reserved for separate *customers*, not sub-units of one), but extend the JWT claim set to carry `state`/`region` **and** `division`, with a layered exec view (State GM → Regional GM → Divisional GM → Group exec) rather than the current flat `is_platform_admin` bypass. _(added 2026-07-23)_
- **No live access-revoke exists.** Role/entitlement changes only take effect on next login today (`IDENTITY-MODEL.md` §6.3) — SKS's stated requirement for a national rollout is instant ("push of a button"). Needs a real design: likely a per-request `users.active`/`deactivated_at` check instead of relying solely on the cached session cookie. _(added 2026-07-23)_
- **Cards' scope needs defining against Upvise.** Royce's call: Cards supplements Upvise, doesn't replace it — Upvise stays the system of record for employment data, Cards owns onboarding/qualifications. That boundary (what Cards owns vs. what stays in Upvise, and whether/how they sync) isn't designed yet. _(added 2026-07-23)_
- **The 3 open P0 security findings (SEC-1 PII leak, SEC-9 leaked service_role key, SEC-10 plaintext API keys) matter more now than the usual priority read** — Royce agreed they should close regardless of the scale question; at 55 users they're bad, at a national headcount any one is a reportable breach, not an internal fix-it item. Already tracked in `ops/security-register.md` — flagging here so the scale conversation doesn't let them drift. _(added 2026-07-23)_
- **No off-platform backup exists for ehow** (SKS's live tenant data) — only Supabase's native 7-day PITR. Target design already exists in `system/infrastructure.md` ("Backup strategy — target state") but isn't built. Royce: budget/appetite exists "if this progresses." _(added 2026-07-23)_
- **A wrong first theory got spun off as its own task before it was disproven** — an early chip pointed at the wrong screen entirely (a different, internal eq-shell user list), and that chip was already started as its own session before the live-database check ruled it out. That session was never tracked down to stop it — it may still be running against a bug that doesn't actually exist. Worth a look for a stray, pointless eq-shell PR later and closing it out if one shows up. _(added 2026-07-23)_
- **A completely unrelated, real in-progress session got stopped by accident** while chasing the item above (mistaken identity, caught and corrected same session) — the EQ Ops quotes-screen cleanup (removing old Win/Lost buttons, tidying the status filter, sticky totals on the quote form). Nothing was lost — the changes are sitting safely un-saved in their own folder — but it needs manually reopening from the Archived sessions list to pick back up. _(added 2026-07-23)_
- None of this session's UI changes (the check page's Site fix/inline editors, the Kanban card titles) were eyeballed live in a real browser — verification was code-level (type-checking + full build) only, since these pages sit behind Royce's own login. Worth a quick click-through next time he's in the app. _(added 2026-07-23)_
_…and 435 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3450 | 451 | 633 |
| [SKS](sks/pending.md) | 514 | 76 | 85 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-23 | [Closed the crm-write/canonical-api entitlement design pass: no gate needed](sessions/2026-07-23.md) |
| 2026-07-22 | [SKS Safety: Incidents/Near Miss tab + Prestart copy-from-last, EQ Field regression found & fixed](sessions/2026-07-22.md) |
| 2026-07-21 | [eq-shell had its own copy of the licence-privacy gap; found, fixed, deployed, and smoke-tested](sessions/2026-07-21.md) |
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-23 09:06 UTC._

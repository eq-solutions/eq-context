---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-01
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-01 01:57 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-01 01:48 UTC → 2026-08-01 01:57 UTC)

- Merged: eq-shell [#1148](https://github.com/eq-solutions/eq-shell/pull/1148) feat(auth): heads-up toast when the existing 5-min role poll
- Merged: eq-shell [#1147](https://github.com/eq-solutions/eq-shell/pull/1147) docs: flag the function-grant landmine behind EQ-CARDS-1C
- Merged: eq-shell [#1142](https://github.com/eq-solutions/eq-shell/pull/1142) chore(intake): re-vendor eq-intake/eq-platform — trades sett
- Merged: eq-shell [#1141](https://github.com/eq-solutions/eq-shell/pull/1141) perf(shell): fetchpriority=low on prewarmed iframes + pause 
- Merged: eq-shell [#1140](https://github.com/eq-solutions/eq-shell/pull/1140) chore(intake): re-vendor eq-intake/eq-platform — Dupes archi
- Merged: eq-shell [#1137](https://github.com/eq-solutions/eq-shell/pull/1137) fix(intake): site-merge manager gate checked the wrong ident
- Merged: eq-shell [#1136](https://github.com/eq-solutions/eq-shell/pull/1136) fix(quotes): sync canonical job status for every pipeline st
- Merged: eq-shell [#1134](https://github.com/eq-solutions/eq-shell/pull/1134) fix(audit): workers-canonical-sync attributes real actors

## ⚠ Needs you (2)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (95)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to click through live**: sign in on core.eq.solutions and confirm Cards/Field/Service each load past "Authorising…" — needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: sign in as a non-manager, try a manager-only action, confirm a "denied" row actually lands in the audit log. Needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_
- **EQ** · **Royce to confirm on Richard's own phone**: the page loads without the error screen, the bottom bar shows Home + Field only, and Service/Ops are reachable via the account menu. _(added 2026-07-31)_
- **EQ** · **Royce to click through the new paste-import resolve screen live** — built and type/build-checked clean, but not clicked through in a real browser session (no test login available in this environment). Paste a batch with an unmatched asset ID, try linking one and creating another, confirm the resulting check comes out right. _(added 2026-07-31)_
- **EQ** · **Royce to spot-check a live PM Check Report and NSX Test Report from a site with an uploaded photo** — verified via generated samples with a placeholder image, not yet against a real production report. _(added 2026-08-01)_
- **EQ** · **Royce to click through live** — trigger a failed-then-fixed site merge and confirm it now works; open the Contacts/Staff Dupes tab, archive one flagged duplicate and dismiss another as "not a duplicate," confirm both stick; add a trade in the new Trades screen and confirm it shows up in the Review Queue's trade picker. Needs sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live**: change a quote's status through each of the 5 stages and confirm the job record follows each time; set a Target period on a quote and confirm the badge shows correctly in both the detail panel and the board view. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** — trigger a failed site merge in the Duplicate Sites panel and confirm the error now shows; open the Remediation Queue, find a duplicate flag, click Archive, confirm the record goes inactive and drops off the list. Claude can't do this step itself — it requires signing in, which falls under the hard rule against entering credentials on the user's behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live** on a mobile-width view (~375px or a phone): open Field/Service and confirm the top bar is gone (just the bottom tab bar); open Ops/Comms and confirm nothing changed; from Field/Service, tap Home and confirm Settings/2FA/Sign-out are still reachable there. Note: a related eq-field fix landed 2026-07-31 (v3.5.388) for a home-label clipping issue caught on the same phone-screenshot pass — worth confirming both together. _(added 2026-07-31)_
- **EQ** · **Royce to confirm live**: once the deploy lands on core.eq.solutions, reload the dashboard and confirm Huon Henne no longer appears under "Licences expiring" on the Compliance & safety card. _(added 2026-07-30)_
- **EQ** · **Moahmmed Elsayed's `photo_id`-typed licence row (number `0140988080`) not yet corrected** — unlike Maylin Ung's case (a driver's-licence-format number, fixed directly), this number doesn't match a recognisable pattern; needs Royce to confirm the actual document type before the DB row is corrected. _(added 2026-07-29)_
- **EQ** · **Royce to click through live**: invite a labour-hire worker with the box unchecked, confirm they land on a Field-free home screen and can't reach Field directly; then invite/sign in a normal worker (box left checked) and confirm nothing changed for them. Bundled with the three click-through items below into one live-testing pass — see that section's deferred note. _(added 2026-07-30)_
_…and 83 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 1 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 17 | 2026-08-01 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 12 | 2026-07-31 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 6 | 2026-07-30 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 5 | 2026-07-31 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 4 | 2026-07-23 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 3 | 2026-07-28 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-01 | eq-shell | [#1159](https://github.com/eq-solutions/eq-shell/pull/1159) chore(intake): re-vendor eq-intake/eq-platform — closes 3 Dependa |
| 2026-08-01 | eq-shell | [#1158](https://github.com/eq-solutions/eq-shell/pull/1158) chore(deps): bump brace-expansion overrides to close 2 CVEs |
| 2026-08-01 | eq-shell | [#1157](https://github.com/eq-solutions/eq-shell/pull/1157) chore(deps): migrate react-router-dom v7 to react-router v8, bump |
| 2026-08-01 | eq-shell | [#1156](https://github.com/eq-solutions/eq-shell/pull/1156) Re-vendor eq-intake/eq-platform to 27bc7b5 |
| 2026-08-01 | eq-shell | [#1154](https://github.com/eq-solutions/eq-shell/pull/1154) feat(security): audit-log every permission denial via requirePerm |
| 2026-08-01 | eq-shell | [#1155](https://github.com/eq-solutions/eq-shell/pull/1155) feat(auth): close 3 remaining ONE LOGIN onboarding gaps |
| 2026-08-01 | eq-shell | [#1153](https://github.com/eq-solutions/eq-shell/pull/1153) security: CSP hardening, permission audit-trail logging, close 2  |
| 2026-08-01 | eq-shell | [#1152](https://github.com/eq-solutions/eq-shell/pull/1152) fix(auth): connect-wallet approval now checks existing documents |
| 2026-08-01 | eq-shell | [#1149](https://github.com/eq-solutions/eq-shell/pull/1149) feat(auth): role-tagged self-join links for Apprentice/Labour hir |
| 2026-08-01 | eq-shell | [#1151](https://github.com/eq-solutions/eq-shell/pull/1151) fix(security): gate the supplier directory read to manager/superv |
| 2026-08-01 | eq-solves-service | [#666](https://github.com/eq-solutions/eq-service/pull/666) feat(admin/media): extend multi-customer picker to Edit; Edit now |
| 2026-08-01 | eq-solves-service | [#665](https://github.com/eq-solutions/eq-service/pull/665) docs(perf): close out dashboard_duration canary check |
| 2026-08-01 | eq-solves-service | [#664](https://github.com/eq-solutions/eq-service/pull/664) fix(reports): fix latent customers-update-trigger bug; add multi- |
| 2026-08-01 | eq-solves-service | [#663](https://github.com/eq-solutions/eq-service/pull/663) feat(admin/media): customer-logo uploads now actually apply to th |
| 2026-08-01 | eq-field | [#598](https://github.com/eq-solutions/eq-field/pull/598) v3.5.403 — Fix: Sentry EQ-FIELD-10, Dashboard map lost a boot rac |
_Showing 15 of 129 · full record in [sessions/](sessions/)_

## Pending (EQ)

- `quote-email.ts` has no permission gate — needs a decision on which perm key should cover it _(added 2026-08-01)_
- `retention-purge.ts`'s live account-deletion path relies solely on Netlify's platform-level scheduled-function-invocation restriction, no app-level guard behind it _(added 2026-08-01)_
- `TENANT_ROUTING_MASTER_KEY` rotation still outstanding — same single-key-no-rotation class as the `EQ_SECRET_SALT` item below _(added 2026-08-01)_
- Signing out of Shell doesn't propagate to the embedded Field/Service/Cards iframe sessions _(added 2026-08-01)_
- Session revocation gap: cookies minted before the `jti` field existed skip the revocation check entirely, and a revocation-check DB error fails open _(added 2026-08-01)_
- No build cache (Turborepo or similar) — every CI run rebuilds the full workspace from scratch _(added 2026-08-01)_
- CSP still allows `style-src 'unsafe-inline'` — removing it needs a full browser-tested pass, not a blind strip _(added 2026-08-01)_
- `is_platform_admin` is an unscoped bypass with no step-up/MFA gate on sensitive actions _(added 2026-08-01)_
- No resource- or relationship-level authorization — permission checks are role-based only, nothing checks whether a user actually owns/manages the specific record being acted on _(added 2026-08-01)_
- Schema drift gate only runs every 3 hours — an out-of-band change can sit undetected that long _(added 2026-08-01)_
_…and 361 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
_…and 66 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2858 | 474 | 62 | 12 |
| [SKS](sks/pending.md) | 424 | 83 | 5 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 5 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-01 | [Confirmed the "no Supabase connector" finding, then closed a real EQ-tenant roster gap found via a backlog sweep](sessions/2026-08-01.md) |
| 2026-07-31 | [Quote events now stamp app_source='ops' instead of the retired app name (continuation of 2026-07-30)](sessions/2026-07-31.md) |
| 2026-07-30 | [`__personal__` tenant "retired" doc claim corrected against live data](sessions/2026-07-30.md) |
| 2026-07-30 | [guard.js selftest fixed; ~/.claude brought under version control](sessions/2026-07-30-guard-selftest-claude-git.md) |
| 2026-07-29 | [eq-receipts: fixed a duplicate-detection blind spot, added invoice number as a stronger match](sessions/2026-07-29.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-01 01:57 UTC._

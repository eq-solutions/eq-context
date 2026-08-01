---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-01
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-01 06:41 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-01 06:19 UTC → 2026-08-01 06:41 UTC)

- Merged: eq-shell [#1158](https://github.com/eq-solutions/eq-shell/pull/1158) chore(deps): bump brace-expansion overrides to close 2 CVEs
- Merged: eq-shell [#1155](https://github.com/eq-solutions/eq-shell/pull/1155) feat(auth): close 3 remaining ONE LOGIN onboarding gaps
- Merged: eq-shell [#1152](https://github.com/eq-solutions/eq-shell/pull/1152) fix(auth): connect-wallet approval now checks existing docum
- Merged: eq-shell [#1151](https://github.com/eq-solutions/eq-shell/pull/1151) fix(security): gate the supplier directory read to manager/s
- Merged: eq-shell [#1150](https://github.com/eq-solutions/eq-shell/pull/1150) fix(auth): mint-cards-otp returns 422 for no-email users, no
- Merged: eq-shell [#1149](https://github.com/eq-solutions/eq-shell/pull/1149) feat(auth): role-tagged self-join links for Apprentice/Labou
- Merged: eq-shell [#1146](https://github.com/eq-solutions/eq-shell/pull/1146) feat(mobile): simplified 2-tab nav for supervisors/managers,
- Merged: eq-shell [#1145](https://github.com/eq-solutions/eq-shell/pull/1145) feat(auth): gate Field JWT on earned access, not just allowe

## ⚠ Needs you (2)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (101)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Royce to click through live**: open New Quote, attach a couple of files before finishing the form, submit, confirm the files show up on the created quote. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: open the Duplicate Sites panel as a non-manager and confirm Preview now shows; mark a row Unsure with a note and confirm it saves and displays; confirm a real merge now succeeds end-to-end (Preview → Confirm) now that the permission fix is live. _(added 2026-08-01)_
- **EQ** · **Royce to click through live on a real device** — confirm the "take a photo" sheet feels right end to end (camera opens, OCR reads the card, fallback link works). Note: the code merged this morning but wasn't actually live yet when Royce first tried it — this repo's deploy isn't automatic on merge, and nobody had triggered one. Deployed and confirmed live later the same day. _(added 2026-08-01, updated 2026-08-01)_
- **EQ** · **Royce to click through live**: sign in on core.eq.solutions and confirm Cards/Field/Service each load past "Authorising…" — needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: open Intake as a signed-in user and confirm the page actually renders (not just that the site responds) — needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_
- **EQ** · **`CoreHome.tsx` is a fully-built, unrouted home-page prototype** ("EQ Intelligence" decision-queue, canonical-graph visualization) sitting dead in the tree, running on hardcoded fake data. Never imported anywhere. Needs Royce's call: revive as the real home page, or delete — not something to guess at _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: sign in as a non-manager, try a manager-only action, confirm a "denied" row actually lands in the audit log. Needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_
- **EQ** · **Royce to confirm on Richard's own phone**: the page loads without the error screen, the bottom bar shows Home + Field only, and Service/Ops are reachable via the account menu. _(added 2026-07-31)_
- **EQ** · **Royce to click through the new paste-import resolve screen live** — built and type/build-checked clean, but not clicked through in a real browser session (no test login available in this environment). Paste a batch with an unmatched asset ID, try linking one and creating another, confirm the resulting check comes out right. _(added 2026-07-31)_
- **EQ** · **Royce to spot-check a live PM Check Report and NSX Test Report from a site with an uploaded photo** — verified via generated samples with a placeholder image, not yet against a real production report. _(added 2026-08-01)_
- **EQ** · **Royce to click through live** — trigger a failed-then-fixed site merge and confirm it now works; open the Contacts/Staff Dupes tab, archive one flagged duplicate and dismiss another as "not a duplicate," confirm both stick; add a trade in the new Trades screen and confirm it shows up in the Review Queue's trade picker. Needs sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-07-31)_
- **EQ** · **Royce to click through live**: change a quote's status through each of the 5 stages and confirm the job record follows each time; set a Target period on a quote and confirm the badge shows correctly in both the detail panel and the board view. _(added 2026-07-31)_
_…and 89 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 19 | 2026-08-01 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 12 | 2026-07-31 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-field | [Error: no-tenant-id](https://eq-solutions.sentry.io/issues/138007377/) | 7 | 2026-08-01 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 6 | 2026-07-30 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 5 | 2026-07-31 |
| eq-field | [Error: 404: {"code":"PGRST202","details":"Searched for the function public.get_s](https://eq-solutions.sentry.io/issues/138015513/) | 4 | 2026-08-01 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-01 | eq-shell | [#1173](https://github.com/eq-solutions/eq-shell/pull/1173) fix(brand): correct stale SKS navy #1F335C to live #203060 |
| 2026-08-01 | eq-shell | [#1171](https://github.com/eq-solutions/eq-shell/pull/1171) fix(intake): eq_site_advisory_flag_pair missing authenticated gra |
| 2026-08-01 | eq-shell | [#1172](https://github.com/eq-solutions/eq-shell/pull/1172) fix(ui): consolidate toast feedback, honest-disable unbuilt bulk  |
| 2026-08-01 | eq-shell | [#1170](https://github.com/eq-solutions/eq-shell/pull/1170) feat(quotes): allow attaching files while creating a new quote |
| 2026-08-01 | eq-shell | [#1169](https://github.com/eq-solutions/eq-shell/pull/1169) chore(intake): replace manual re-vendor steps with a script |
| 2026-08-01 | eq-shell | [#1168](https://github.com/eq-solutions/eq-shell/pull/1168) fix(intake): eq_site_merge_execute missing authenticated grant |
| 2026-08-01 | eq-shell | [#1167](https://github.com/eq-solutions/eq-shell/pull/1167) chore(intake): re-vendor eq-schemas package.json — closes ajv Dep |
| 2026-08-01 | eq-shell | [#1166](https://github.com/eq-solutions/eq-shell/pull/1166) fix(security): session revocation fails closed on a DB lookup err |
| 2026-08-01 | eq-shell | [#1165](https://github.com/eq-solutions/eq-shell/pull/1165) fix(security): quote-email gate, iframe sandbox docs, real tsc in |
| 2026-08-01 | eq-shell | [#1164](https://github.com/eq-solutions/eq-shell/pull/1164) fix(auth): recovery-email nudge never cleared; show/hide toggle o |
| 2026-08-01 | eq-shell | [#1163](https://github.com/eq-solutions/eq-shell/pull/1163) fix(security): correct a mistaken audit finding on retention-purg |
| 2026-08-01 | eq-shell | [#1162](https://github.com/eq-solutions/eq-shell/pull/1162) chore(intake): re-vendor eq-platform root config — closes 3 resid |
| 2026-08-01 | eq-shell | [#1161](https://github.com/eq-solutions/eq-shell/pull/1161) fix(intake): duplicate React instance breaking /intake in product |
| 2026-08-01 | eq-shell | [#1160](https://github.com/eq-solutions/eq-shell/pull/1160) fix(auth): capture email during role-tagged self-join |
| 2026-08-01 | eq-shell | [#1159](https://github.com/eq-solutions/eq-shell/pull/1159) chore(intake): re-vendor eq-intake/eq-platform — closes 3 Dependa |
_Showing 15 of 133 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Worth checking separately**: the tool that rolls database changes out to every company's system may have a bug where an instruction placed right after defining a new function can silently not run, even though the file it's in is marked as successfully applied. Only caught because this one case got tested by hand — there could be others sitting the same way undetected. Not investigated further. _(added 2026-08-01)_
- **Saving/updating records through one part of the database layer has no real type-checking behind it** — turns out this is already known, tracked work (the app's own 30-day plan lists it), not a fresh find: the auto-generated database description file only covers the app's default section, but this data actually lives in a different section the file never describes, so the "trust me" overrides are a deliberate stand-in, not an accident. Confirmed live: the record it reads/writes from isn't a plain table, it's a view with its own custom save-behaviour attached — so even generating a fuller description file may not fully close the gap without extra work. Affects roughly 17 places. Needs the proper database tool run with the right settings (not available through the tools used this session), then each of the 17 spots checked by hand. _(added 2026-08-01, corrected 2026-08-01 — see below)_
- **Photo → AI Risk Suggestions** (the secondary feature from the original review — supervisor takes site photos, AI suggests hazards, human confirms which to add) — deliberately not started. Needs its own go/no-go before scoping further: real per-call API spend, a new Netlify Function (would clone `eq-agent.js`'s existing auth/rate-limit shape), and site photos leaving the tenant boundary to Anthropic's API. _(added 2026-08-01)_
- **eq-cards / eq-design-tokens / sks-charters / eq-website**: alerts just switched on, the very first scan came back clean on all 4 — worth a second look in a day or two in case that first scan didn't fully finish rather than assuming it's actually clean. _(added 2026-08-01)_
- **eq-receipts' react-router move hasn't been clicked through live** — the build is clean and Netlify's own preview built it successfully, but nobody has actually navigated the real app (Dashboard → Review → Verify, sidebar links) since the change. Worth a quick manual pass. _(added 2026-08-01)_
- `TENANT_ROUTING_MASTER_KEY` rotation still outstanding — same single-key-no-rotation class as the `EQ_SECRET_SALT` item below. Royce: leave deferred (reconfirmed 2026-08-01, not silence — no change wanted) _(added 2026-08-01)_
- CSP still allows `style-src 'unsafe-inline'` — removing it is a multi-day styling refactor (React's `style` prop is itself inline styling), not a strip-and-test; needs its own session _(added 2026-08-01)_
- `is_platform_admin` is an unscoped bypass with no step-up/MFA gate on sensitive actions — a new auth feature. Royce: scope it as its own session, no build yet (reconfirmed 2026-08-01) _(added 2026-08-01)_
- No resource- or relationship-level authorization — permission checks are role-based only, nothing checks whether a user actually owns/manages the specific record being acted on. Architectural, needs its own design pass _(added 2026-08-01)_
- No down-migration/rollback path for schema migrations — a schema-governance policy decision, not a code fix _(added 2026-08-01)_
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
| [EQ](eq/pending.md) | 2966 | 477 | 89 | 12 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-01 06:41 UTC._

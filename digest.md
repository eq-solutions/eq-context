---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-02
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-02 19:23 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-02 19:14 UTC → 2026-08-02 19:23 UTC)

- Merged: eq-shell [#1195](https://github.com/eq-solutions/eq-shell/pull/1195) feat(auth): trim worker-add dropdown to 2 items, surface gen
- Merged: eq-shell [#1177](https://github.com/eq-solutions/eq-shell/pull/1177) feat(auth): self-join links v2 — approval gate, expiry, all 
- Merged: eq-shell [#1176](https://github.com/eq-solutions/eq-shell/pull/1176) fix(intake): pnpm/action-setup can't auto-detect version wit
- Merged: eq-shell [#1173](https://github.com/eq-solutions/eq-shell/pull/1173) fix(brand): correct stale SKS navy #1F335C to live #203060
- Merged: eq-shell [#1172](https://github.com/eq-solutions/eq-shell/pull/1172) fix(ui): consolidate toast feedback, honest-disable unbuilt 
- Merged: eq-shell [#1169](https://github.com/eq-solutions/eq-shell/pull/1169) chore(intake): replace manual re-vendor steps with a script
- Merged: eq-shell [#1167](https://github.com/eq-solutions/eq-shell/pull/1167) chore(intake): re-vendor eq-schemas package.json — closes aj
- Merged: eq-solves-service [#683](https://github.com/eq-solutions/eq-service/pull/683) fix(reports): PM report supervisor/contact fields ignored th

## ⚠ Needs you (3)

- 🔴 **Sentry new error** — `eq-field` [Error: no-tenant-id](https://eq-solutions.sentry.io/issues/138007377/)
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (109)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. _(added 2026-08-03)_
- **EQ** · **Sentry EQ-FIELD-10 recurred on this same PR's preview deploy — tracked, not fixed.** [no-tenant-id](https://eq-solutions.sentry.io/issues/138007377/), 26 events / 3 users, 2026-08-01→02, `deploy-preview-622--eq-field.netlify.app` (demo tenant, v3.5.429). Confirmed by reading the code: the dashboard map's bounded JWT-tenant-id retry (v3.5.403 — 4 tries × 1500ms) fully exhausted before the Shell→Field JWT handoff landed. Real race, not fresh noise — substatus is *regressed* (previously marked resolved). Not caused by this PR's actual diff (filter row / map default / table sizing) — more likely surfaced by preview's colder function starts than production sees. Degrades gracefully on exhaustion ("Map unavailable right now", self-heals next render). **Royce's call 2026-08-03: track only, no fix yet** — preview-only so far, not confirmed on production traffic, TODAY.md goals still unset so nothing forces this now. Two fix directions if it recurs on production: widen the retry budget/interval, or have the map card listen for the Shell→Field JWT-ready event instead of polling a fixed schedule. _(added 2026-08-03)_
- **EQ** · **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
- **EQ** · **Staff duplicate handling — still Archive-only, needs your call before any build.** A real staff merge fans out into Field-owned operational tables (timesheets, schedule, licences, dispatch) — per the durable architecture rule, that can't be rebuilt Shell-side; it needs Field-repo coordination, which is a scope decision, not something to default on. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open a site, assign a supervisor from its own contact list, save, reload, confirm it sticks; toggle "Show archived" on the Sites list and confirm it filters/tags correctly. Needs a real sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-08-02)_
- **EQ** · **Royce to check `admin/users/migrate` for SKS against the 44-workers number above** — the invite screen and the 44 are counted two different ways (one by tenant employee record, one by Cards worker record), so they may not match exactly. Worth confirming they're the same gap before assuming the invite screen alone closes it. _(added 2026-08-02)_
- **EQ** · Royce to spot-check a generated PM Asset Report live for a site that has a photo on file — confirm the band + photo layout looks right. _(added 2026-08-02)_
- **EQ** · **Royce to test the licence-photo-scan flow on a real phone.** Built 7 synthetic test photos (6 different licence/certificate types, all fake data, all under one name so they test as multiple licences on a single account, plus one deliberately rotated/lower-quality shot) and sent them over to email to a test phone. Results not yet known — worth checking whether this also exercises the still-open credential issue above. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open New Quote, attach a couple of files before finishing the form, submit, confirm the files show up on the created quote. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: open the Duplicate Sites panel as a non-manager and confirm Preview now shows; mark a row Unsure with a note and confirm it saves and displays; confirm a real merge now succeeds end-to-end (Preview → Confirm) now that the permission fix is live. _(added 2026-08-01)_
- **EQ** · **Royce to click through live**: sidebar logo and the admin Media Library page (grid + edit modal) for a tenant with a logo set — confirm images still render correctly after the switch above. _(added 2026-08-01)_
- **EQ** · **Royce to click through live on a real device** — confirm the "take a photo" sheet feels right end to end (camera opens, OCR reads the card, fallback link works). Note: the code merged this morning but wasn't actually live yet when Royce first tried it — this repo's deploy isn't automatic on merge, and nobody had triggered one. Deployed and confirmed live later the same day. _(added 2026-08-01, updated 2026-08-01)_
_…and 97 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

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
| eq-field | [Error: no-tenant-id](https://eq-solutions.sentry.io/issues/138007377/) | 26 | 2026-08-02 |
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 19 | 2026-08-01 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 13 | 2026-08-01 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 7 | 2026-08-02 |
| eq-field | [Error: 404: {"code":"PGRST202","details":"Searched for the function public.get_s](https://eq-solutions.sentry.io/issues/138015513/) | 4 | 2026-08-01 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 4 | 2026-07-23 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-02 | eq-shell | [#1195](https://github.com/eq-solutions/eq-shell/pull/1195) feat(auth): trim worker-add dropdown to 2 items, surface general  |
| 2026-08-02 | eq-shell | [#1193](https://github.com/eq-solutions/eq-shell/pull/1193) fix(auth): self-join adds a membership in the new tenant, not jus |
| 2026-08-02 | eq-shell | [#1194](https://github.com/eq-solutions/eq-shell/pull/1194) chore(control-plane): backfill missing source for eq_cards_is_pla |
| 2026-08-02 | eq-shell | [#1180](https://github.com/eq-solutions/eq-shell/pull/1180) feat(documents): internal document sign-off register schema (tena |
| 2026-08-02 | eq-shell | [#1192](https://github.com/eq-solutions/eq-shell/pull/1192) fix(auth): self-join fixes — worker row, email-drop notice, photo |
| 2026-08-02 | eq-shell | [#1191](https://github.com/eq-solutions/eq-shell/pull/1191) chore(intake): auto re-vendor eq-intake/eq-platform |
| 2026-08-02 | eq-shell | [#1190](https://github.com/eq-solutions/eq-shell/pull/1190) feat(intake): Contact resolver + merge (migrations 0233/0234) |
| 2026-08-02 | eq-shell | [#1189](https://github.com/eq-solutions/eq-shell/pull/1189) feat(auth): join-links controls — edit expiry, join counts, code  |
| 2026-08-02 | eq-shell | [#1188](https://github.com/eq-solutions/eq-shell/pull/1188) fix(auth): self-join provisioning 500s on email collision, misrep |
| 2026-08-02 | eq-shell | [#1187](https://github.com/eq-solutions/eq-shell/pull/1187) chore(intake): auto re-vendor eq-intake/eq-platform |
| 2026-08-02 | eq-shell | [#1186](https://github.com/eq-solutions/eq-shell/pull/1186) feat(auth): delete self-join links, not just deactivate |
| 2026-08-02 | eq-shell | [#1185](https://github.com/eq-solutions/eq-shell/pull/1185) feat(auth): collapse worker-add header into one button + a menu |
| 2026-08-02 | eq-shell | [#1183](https://github.com/eq-solutions/eq-shell/pull/1183) chore(intake): auto re-vendor eq-intake/eq-platform |
| 2026-08-02 | eq-shell | [#1184](https://github.com/eq-solutions/eq-shell/pull/1184) feat(auth): per-role QR codes on the self-join links page |
| 2026-08-02 | eq-shell | [#1181](https://github.com/eq-solutions/eq-shell/pull/1181) feat(auth): surface self-join approvals in the Staff pending pane |
_Showing 15 of 133 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Neither change has been clicked through live** — Supabase OTP auth gated this session out of the real app, no test login available. Same underlying gap as the still-open react-router click-through below — worth doing both in the same real-device pass. _(added 2026-08-03)_
- **The map's `invalidateSize()` fix (v3.5.431) hasn't been confirmed against the real failure context.** It only reproduces inside a Shell-embedded iframe (`core.eq.solutions/sks/field`) with real SKS data — this session's browser tooling had no path to Core auth to check it directly. The fix is standard, low-risk Leaflet practice regardless, but worth confirming on a genuinely fresh (not manually re-panned) dashboard load next time you're in there. _(added 2026-08-02)_
- **Not swept: whether any of the other ~22 canonical objects (defects, contract_scopes, job_plans, maintenance_checks, etc.) have the same "trigger references a column the view doesn't expose" bug class.** This fix only covered the three objects (`customers`, `sites`, `assets`) touched by the 2026-07-27 change — no broader check across all canonical objects has been done. _(added 2026-08-02)_
- Royce is checking directly whether EQ Intake can push timesheets into Workbench (SKS's own payroll tool) — none of the 12 export formats target it today. _(added 2026-08-02)_
- **A rare licence-photo-scanning failure needs a credential check, not a code fix.** Traced to a security key eq-shell uses to talk to another system possibly being out of date. Notably, this is the *second* time this exact symptom (401 on licence-photo scanning) has shown up — 2026-07-23's version (task_d94af51d) was a stale deploy, this one looks like a different cause. Needs you to confirm/refresh the key rather than guess. _(added 2026-08-02)_
- **Found the likely root cause behind both duplicate-identity bugs above: phone numbers are stored in inconsistent formats across two systems** (e.g. `+61439109013` in one place, `0439109013` or `61408164924` in another, for the same person). Confirmed in 3 separate records. Whatever matches people up by phone number during signup/linking probably fails silently when the formats don't match, creating a stray empty account instead of recognizing the existing person — this will keep recurring until someone normalizes phone numbers before comparing them. Needs its own investigation session to find the exact code path and fix it at the source, not just clean up after it each time. _(added 2026-08-02)_
- **Worth checking separately**: the tool that rolls database changes out to every company's system may have a bug where an instruction placed right after defining a new function can silently not run, even though the file it's in is marked as successfully applied. Only caught because this one case got tested by hand — there could be others sitting the same way undetected. Not investigated further. _(added 2026-08-01)_
- **Saving/updating records through one part of the database layer has no real type-checking behind it** — turns out this is already known, tracked work (the app's own 30-day plan lists it), not a fresh find: the auto-generated database description file only covers the app's default section, but this data actually lives in a different section the file never describes, so the "trust me" overrides are a deliberate stand-in, not an accident. Confirmed live: the record it reads/writes from isn't a plain table, it's a view with its own custom save-behaviour attached — so even generating a fuller description file may not fully close the gap without extra work. Affects roughly 17 places. Needs the proper database tool run with the right settings (not available through the tools used this session), then each of the 17 spots checked by hand. _(added 2026-08-01, corrected 2026-08-01 — see below)_
- **Photo → AI Risk Suggestions** (the secondary feature from the original review — supervisor takes site photos, AI suggests hazards, human confirms which to add) — deliberately not started. Needs its own go/no-go before scoping further: real per-call API spend, a new Netlify Function (would clone `eq-agent.js`'s existing auth/rate-limit shape), and site photos leaving the tenant boundary to Anthropic's API. _(added 2026-08-01)_
- **eq-cards / eq-design-tokens / sks-charters / eq-website**: alerts just switched on, the very first scan came back clean on all 4 — worth a second look in a day or two in case that first scan didn't fully finish rather than assuming it's actually clean. _(added 2026-08-01)_
_…and 365 more · [eq/pending.md](eq/pending.md)_

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
_…and 65 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3096 | 492 | 122 | 12 |
| [SKS](sks/pending.md) | 424 | 83 | 5 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 5 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-03 | [EQ-FIELD-10 Sentry triage: tracked, not fixed (Royce's call)](sessions/2026-08-03.md) |
| 2026-08-02 | [eq-solves-service: PM reports were showing the wrong "supervisor" and blank contact details, never wired to the real site-supervisor feature](sessions/2026-08-02.md) |
| 2026-08-01 | [Confirmed the "no Supabase connector" finding, then closed a real EQ-tenant roster gap found via a backlog sweep](sessions/2026-08-01.md) |
| 2026-07-31 | [Quote events now stamp app_source='ops' instead of the retired app name (continuation of 2026-07-30)](sessions/2026-07-31.md) |
| 2026-07-30 | [`__personal__` tenant "retired" doc claim corrected against live data](sessions/2026-07-30.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-02 19:23 UTC._

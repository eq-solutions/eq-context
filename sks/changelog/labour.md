---
title: Changelog — SKS Labour
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Append-only history of changes to the SKS Labour scheduling app
read_priority: reference
status: live
---

# Changelog — SKS Labour

## [2026-07-15] Timesheet total double-count fix, invisible mobile roster header, Pipeline/Resources hidden
**Built by:** assistant + Royce Milmlow
- **v3.10.97 (PR #66, `51544ad`, live)** — two fixes. (1) Timesheet weekly total double-counted a roster A/L day: the day's leave status comes from `schedule`, its hours from `timesheets`, and a stale entry left behind by an earlier "Fill Week" run was hidden behind the leave pill but still summed into the total (plus the paid-leave 8h added for the same day) — TAFE days had a same-day guard for this since v3.10.84, paid leave never did. New `_tsWorkedHrs()` skips roster-leave days, wired into every total surface (row, apprentice, in-place save, CSV export); cleared the one affected DB row (Jack Trusler, wk 13.07.26, the only occurrence found). (2) Mobile Weekly Roster header (Name/Mon–Fri) rendered invisible below 768px — the sticky-header CSS re-backgrounded the cells for the scroll effect without resetting the inherited white header text from the desktop navy header; added explicit `color: var(--navy)`.
- **v3.10.98 (PR #67, `fbeeeec`, live)** — Pipeline + Resources nav hidden from all managers (previously visible to any manager-mode user via `edit-only`). Nav-only change; pages, data, and `scripts/pipeline*.js` untouched.
**Status:** Both live on sks-nsw-labour.netlify.app. EQ Field flagged for the same header-CSS pattern (background task, independent session, result not yet known).

## [2026-07-12] "Database not working" outage → root fix, resilience, timesheet UX, and prevention (first CI)
**Built by:** assistant + Royce Milmlow
- **v3.10.92 (PR #59, `2e38315`, live)** — ROOT FIX for the ~2-day silent outage. v3.10.90 paginated `team_members`/`timesheet_locks` via `sbFetchAll()` with no `orderBy`, so both defaulted to `order=id` — neither has an `id` column → 400 on every load. One 400 in `loadFromSupabase()`'s all-or-nothing `Promise.all` froze the whole sync on the last cached snapshot (writes still 200'd, so saves looked fine; the 400 was a handled rejection → 0 `error_thrown`, invisible). Passed each table's real PK.
- **v3.10.93 (PR #60, `0f68678`, live)** — made the sync failure-resilient. Split tables into load-critical (abort → keep last-good snapshot) vs optional (`.catch(()=>[])`, preserve last-known). Degraded syncs now observable — toast + `sync_degraded` PostHog event + console breadcrumb, transition-guarded.
- **v3.10.94 (PR #61, `84abe48`, live)** — timesheet UX: (1) hours-missing red flag (kills the phantom `placeholder="8"`; a job with blank hours goes red `?`), (2) weekend auto-show (any week with Sat/Sun data reveals the weekend columns), (3) Sunday week-rollover fix (all four week-Monday formulas aligned to ISO `-((getDay()+6)%7)` — app advances Monday, not Sunday).
- **v3.10.95 (PR #63, `b8cd308`, live)** — prevention: fail-loud `sbFetchAll` (throws instead of defaulting to `order=id`); degrade email alert to ops (`_alertSyncDegraded`, throttled 1/device/day, SKS-only); **bootstrap smoke test + first CI** (`scripts/smoke/bootstrap-smoke.mjs` + `.github/workflows/smoke.yml`) asserting every bootstrap read 2xx on push to main.
- **v3.10.96 (PR #65, `6f3eccc`, deploying)** — LOGIN FIX: supervisors stopped dropping to view-only after a reload. Supervisor status was held in a one-shot `eq_auto_admin` flag that `initApp` consumed; the durable logged-in flag survived reloads but the role didn't, so the SW auto-reload (fires every deploy) re-ran boot with the flag gone → view-only. Fix: durable `eq_role` written at every login path and read on every boot (Option 1); SW-activated reload deferred to a non-disruptive moment instead of an instant flash (Option 3). `scripts/auth.js` + `index.html`; no change to how anyone logs in. One-time: currently-logged-in supervisors log out/in once to seat the durable role.
**Status:** All live on sks-nsw-labour.netlify.app. EQ Field audited — the resilience layers aren't required there now (it can't freeze; `_loadSafe` + #459); logged to the merge-time parity checklist instead. EQ Field's login differs (Shell JWT) — its role-persistence gets its own check at merge, not a copy of the SKS fix.

## [2026-07-10] Roster save reliability — two bugs behind one "Save failed" toast + schedule retention + full pagination sweep
**Built by:** assistant + Royce Milmlow
- **v3.10.88 (PR #55, merged + live)** — roster save self-heals the duplicate-key (409) race. `saveCellToSB`'s POST-insert path now catches `UNIQUE(name,week,org_id)`, fetches the existing server row, and PATCHes the edited day onto it instead of showing "Save failed — check connection". Root cause of Collin Toohey's report — a stale local cache colliding with a server row it didn't know about.
- **v3.10.89 (PR #56, merged + live)** — `schedule?select=*` initial load no longer silently truncated at 1000 rows. New `sbFetchAll()` pages through with explicit `order=id`. The table had crossed the PostgREST default cap (1,069 rows); the dropped rows were the newest inserts = far-future weeks, which is exactly what Simon Bramall reported (roster entries more than a month out failing/blank).
- **Live retention (nspb, Royce-approved)** — new `schedule_archive` (RLS-locked, no app access); one-time archive-then-delete of 681 rows >4 weeks past (live table 1,069 → 388); recurring weekly cron `schedule-4wk-retention-archive` (Sun 03:00 UTC) enforces the 4-week window going forward. Keeps the live table permanently under the row cap (~142 rows/month growth).
- **v3.10.90 (PR #57, merged + live)** — same-day follow-up sweep: paginated `timesheets` (both `loadFromSupabase()` and the standalone `timesheets.js` loader), `team_members`, `timesheet_locks`, and `leave_requests` (`scripts/leave.js`) with the same `sbFetchAll()` pattern as v3.10.89. None of these had crossed 1000 rows yet — fixed proactively rather than waiting for a repeat incident. Ported the same day to eq-field as PR #425 (v3.5.274).
- **v3.10.91 (PR #58, merged + live)** — pagination sweep continued: `tender_enrichment`/`nominations` (both `pipeline.js` and `pipeline-resource.js`), `pending_schedule`, and the tender-import diff read in `pipeline-import.js` were capped with a generous `limit=N` stopgap but are meant to be complete datasets — same silent-drop risk as schedule/timesheets, now paginated. `sbFetchAll()` gained an `orderBy` param (`tender_enrichment` has no `id` column, only `tender_id`). Deliberately left `audit_log`/`prestarts`/`toolbox_talks` alone — those caps are an intentional "show the most recent N" UI display, not a full-load bug. Ported the same day to eq-field as PR #427 (v3.5.276).

## [2026-07-08] TAFE timesheet prefill — 4 iterative ships + labour-hire agency filter
**Built by:** assistant + Royce Milmlow
- **v3.10.82** — TAFE days no longer mute the timesheet during a configured TAFE holiday (payroll could not enter real hours on the break week). `_tsDayStatus` made holiday-aware via a shared `isTafeHolidayCell()` helper in `tafe.js`.
- **v3.10.83** — soft "🎓 TAFE break" hint on the (now editable) holiday-week TAFE cell so it didn't look like the prefill vanished.
- **v3.10.84** — superseded both: every apprentice TAFE day renders as an editable cell pre-filled with `TAFE`/8h you type a real job over. Stays `workable:false` (completion/40h unchanged); 8h counted via `_tafeHrs`, made entry-aware (job OR hours) so overwriting never double-counts.
- **v3.10.85 (final, Royce-approved)** — the prefill is driven by each apprentice's nominated `people.tafe_day`, not just roster-typed TAFE — so their TAFE day prepopulates every week incl. future weeks. Roster content still wins (site keeps day workable; leave mutes); nominated-day default only fills an empty cell.
- **v3.10.86** — labour-hire agency filter on Timesheets: new Agency dropdown next to Group narrows the list to one agency's people for print/export; built from the `people.agency` tag on active LH workers. `↓ Export CSV`/`↓ Payroll Report` now honour the on-screen filters and the filename carries an agency suffix. Agency data tidy on nspb (2 rows): `Madigans`→`Madagins`, `core`→`Core`.
- **v3.10.87** — Jose Quintanilla "still labour hire" fixed: he'd been moved LH→Direct but kept his `agency` tag, leaking him into the new agency filter. Cleared his nspb agency manually + shipped the guard — `savePerson()` forces `agency` empty for non-LH people and hides the field, so non-LH people can no longer carry an agency. Ported the same day to eq-field (`savePersonToSB()`, v3.5.269).
**Status:** All live on sks-nsw-labour.netlify.app. Ported to eq-field v3.5.263→269 (see field.md).

## [2026-04-28] Add Contact button on Contacts page (cherry-picked from EQ Field demo)
**Built by:** Royce Milmlow + assistant
**Commit:** `4f03227` on `main` (cherry-pick of `f372a43`); originally PR #25 on Milmlow/eq-field-app
**Changes:** "＋ Add Contact" button added to the Contacts page filter row. Reuses existing modal-manager + saveManager flow; no new code paths, no migration, no permission change. One-line diff to `index.html`. Cherry-picked from EQ Field demo branch where it shipped via PR #24.
**Why:** UX parity — the page-contacts page (nav: Contacts) showed staff/people but had no Add affordance. Add button only existed on page-managers (Supervision).
**Status:** Live on sks-nsw-labour.netlify.app post-Netlify-deploy.

## [2026-04-11] Service Worker Caching and Favicon Set
**Built by:** Royce Milmlow + assistant
**Changes:**
- Service worker caching strategy fixed — network-first for JS/CSS/HTML, cache-first for icons
- Full SKS favicon set built (ico, apple-touch, 192, 512)
**Status:** Live

## [2026-04-04] Connector Guardrails and Redundancy Review
**Built by:** Royce Milmlow + assistant
**Changes:**
- Connector guardrails documented
- Redundancy gaps identified (no Supabase backups, single point of failure)
**Status:** Live at sks-nsw-labour.netlify.app

## [2026-03-01] SKS Labour Forecast Live
**Built by:** Royce Milmlow + assistant
**Changes:**
- Single-file HTML/JS app with Supabase backend
- Supports 50+ field staff scheduling
- Positive day-one reception from field staff
**Status:** Live at sks-nsw-labour.netlify.app (moved from EQ-FIELD.md changelog — this entry always belonged here)

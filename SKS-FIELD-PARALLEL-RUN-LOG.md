---
title: SKS Field — Parallel Run Log
owner: Royce Milmlow
scope: Weekly mismatch log for the EQ Field / SKS Labour parallel-entry proving run
last_updated: 2026-07-26
read_priority: high
status: live
---

# SKS Field — Parallel Run Log

Companion to `SKS-CUTOVER-CRITICAL-PATH.md` (the "⚠ UPDATE 2026-07-11" section — cutover method is
manual re-entry, not automated migration). This file is the mismatch log that plan calls for and
didn't yet have: *"Enter independently, then compare — don't key EQ Field to force a match... Log
every mismatch."* It's also the clean-weeks counter toward the stop condition.

## How this works

1. Each week, enter that week's roster + timesheets into **EQ Field** independently — i.e. from the
   same source information a supervisor would normally use, not by copying what's already sitting in
   SKS Labour to force a match. The divergence between the two systems is the whole point.
2. After the week closes, compare EQ Field's entries against SKS Labour's for the same week.
3. Add a row to the log below for that week — every mismatch found, however small, plus a clean/dirty
   verdict.
4. **Not solo** (per the plan's proving discipline): at least one real supervisor entering their own
   crew's data, not just one person doing it centrally. Note who entered in the row.

## Stop condition

**Target: 3–4 consecutive clean weeks** (plan's recommendation) across a full roster + timesheet cycle
before cutting SKS over to EQ Field as the system of record. Consecutive means consecutive — a dirty
week resets the count to zero, it doesn't just pause it.

**Current clean-week streak: 0** (not yet started — first tracked week is the next one entered below.)

## Verified baseline (2026-07-26, before this run started)

Checked live against `ehow` (Supabase project `ehowgjardagevnrluult`) rather than assumed from prior
docs, which had gone stale:

- `field_schedule`: 1,012 rows (2026-06-22 → 2026-10-30, includes forward roster planning)
- `field_timesheets`: 138 rows (2026-06-29 → 2026-07-24)
- `field_people`: 90 · `field_sites`: 46 · `field_teams`: 7 · `field_job_numbers`: 27
- Real entry activity has been minimal: **1 Timesheet audit-log action in the last 14 days**, against
  an 86-row timesheet burst the week of 2026-07-06 that looks like a one-time backfill, not organic
  weekly entry. The parallel run decided 2026-07-11 did not get sustained — this log exists so the
  restart doesn't stall the same way silently.
- Auth/RLS checked and confirmed sound: `field_*` views carry an inert `anon SELECT` grant (view-level
  artifact), but every underlying base table (`schedule_entries`, `timesheets`, `leave_requests`,
  `site_diaries`, `toolbox_talks`) has RLS enabled with policies scoped to `{authenticated}` + tenant
  match only — no policy exists for `anon`, so the grant is unreachable. Not a blocker to this run;
  worth a P3 hygiene cleanup (revoke the unused grant) separately, not urgent.

## Weekly log

| Week (Mon date) | Entered by | Site(s)/crew | Mismatches found | Verdict | Notes |
|---|---|---|---|---|---|
| _(next week goes here)_ | | | | | |

<!--
Row template — copy this in for each new week:
| YYYY-MM-DD | Name | Site/crew | - describe each mismatch, one per line, or "None" | Clean / Dirty | anything else worth remembering |
-->

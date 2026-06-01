---
title: EQ Field — Feature Backlog 2026-05-30
owner: Royce Milmlow
last_updated: 2026-05-30
scope: EQ-tenant feature backlog for EQ Solves Field (eq-solutions/eq-field), ranked by value × low-effort. SKS-only modules excluded. Read-only planning artefact.
read_priority: standard
status: live
---

# EQ Field — Feature Backlog (2026-05-30)

Codebase read on v3.5.30 (`main`, `C:\Projects\eq-solves-field`). Sources:
- `index.html` changelog banner (v3.5.x series)
- All `scripts/*.js` — partial reads of every module
- `CLAUDE.md` "Known weak spots / TODO" section
- `eq/pending.md`, `eq/products.md`, `SPRINT-BOARD.md`, `STATE.md` in `eq-context`

SKS-specific features (safety, teams, sks-pipeline) are already ported and tenant-gated. This backlog focuses on **EQ-tenant value** — things an outside trade business would pay for or that reduce day-to-day friction for whoever manages Field.

---

## ✅ BUILD STATUS (updated 2026-06-01 — after PR #153 v3.5.49)

**Built & merged:** #1 timesheet pre-fill, #3 multi-week export, #4 hard-delete leave, #6 calendar person-filter, #7 roster copy-week, #8 dashboard gap-alerts, **#9 roster bulk-ops (#145)**, #13 apprentice year auto-advance, **#14 weekly site-attendance report (#145)**, #16 roster PDF/print, **#17 mobile roster swipe (#145 — pages the week)**, #19 audit-log schema-fix. Plus a **print.css EQ/SKS tenant-brand fix** (#145). **#20 PIN from app_config** → **PR #153 merged 2026-06-01**: `verify-pin.js` reads from Supabase `app_config` first, env var fallback. **Requires `TENANT_ORG_UUID` Netlify env var to activate** (EQ: `1eb831f9-aeae-4e57-b49e-9681e8f51e15`). Also PR #153: **L5 SW update toast** — `controllerchange` listener shows bottom-centre toast with "Reload" button (v3.5.49).
**Built but DORMANT** (UI ships inert; needs a parked migration to activate): #12 licence-expiry alerts.
**PARKED — migration-gated (Royce):** #2 timesheet approval, #5 leave balance, #10 staff unavailability, #11 self-serve availability portal, #15 audit-log UI. #18 supervisor timesheet tile is blocked on #2.
**Net:** no-migration EQ-tenant backlog exhausted. Next Field work requires a parked migration run, `TENANT_ORG_UUID` Netlify env var for PR #153 to take effect, or net-new scope.

---

## Ranking methodology

Score = **value to a paying EQ tenant** (1–5) × **(1 / effort)** where effort is S=1, M=0.5, L=0.25. Features with identical scores are ordered by risk (lower risk first). "Additive" means zero change to existing code paths; "shared" means it touches code used by multiple modules.

---

## Theme 1 — Timesheets

### 1. Smart timesheet pre-fill from roster (S)

**What:** When a supervisor opens timesheets for a week, auto-populate each person's job number from their roster entries for that week. The site abbreviation in `schedule` already maps 1:1 to a job number via `job_numbers` table. One button or auto-fill on week-change.

**Why:** Explicit TODO in `CLAUDE.md` — "Smart timesheet defaults — pre-fill this week from last week's roster. Single biggest workflow time-saver." Timesheets and roster are already linked conceptually but the fill is manual. This is the most repeated supervisor task.

**Effort:** S — `getPersonSchedule(name, week)` already returns the full row; `_getActiveJobs()` already exists. Wire: for each person, look up the roster day code, find matching job number, call `saveTsCell`. New function, no existing code changed.

**Risk:** Low. Additive — new "Pre-fill from roster" button alongside existing ">> Week" button. No schema change.

**Code touch:** `timesheets.js` (additive), `index.html` (one button in ts toolbar).

---

### 2. Timesheet approval schema migration + full approval workflow (M)

**What:** The `timesheets` table is missing `approved`, `approved_by`, `approved_at` columns on the EQ Supabase. The approval chip (`_tsApprovalChip`) already renders gracefully when the columns are absent. Apply the migration, then expose: (a) bulk approve-week button for supervisors, (b) approved state locked against edits.

**Why:** The UI already exists with graceful degradation (`CLAUDE.md` v3.5.30 #5 note: "Schema migration held for Royce's cutover window"). Labour-hire and apprentice timesheets need an approval sign-off before payroll — this is the missing close loop. Current state: timesheets can be exported but there is no record of who reviewed them.

**Effort:** M — migration is 3 columns; bulk-approve button is new; edit-lock is one guard in `saveTsCell` and `onTsCellChange`. The approval chip is already coded.

**Risk:** Medium. Requires a DB migration on `ktmjmdzqrogauaevbktn`. No auth change. Schema migration is additive (new nullable columns). The graceful-degrade path already tested.

**Code touch:** `migrations/` (new SQL), `timesheets.js` (edit-lock guard + bulk-approve button), shared approval-chip already in place.

---

### 3. Timesheet multi-week export / payroll summary (S)

**What:** Current `exportTsCSV()` and `exportTsPayroll()` only export the currently-displayed week. Add a date-range picker that lets a supervisor export e.g. last 4 weeks in one CSV download. The bulk-export path `_loadFullDataForExport()` bypasses the sliding-window and already exists.

**Why:** Labour-hire agencies and payroll systems need fortnightly or monthly summaries. Today supervisors export week-by-week and stitch them. This is the logical next step after the sliding-window S1 fix that specifically preserved a full-table export path for this exact purpose.

**Effort:** S — `_loadFullDataForExport()` already fetches the full dataset. Add a date-range input to the export modal, filter the already-loaded data, call the existing CSV builder.

**Risk:** Low. Additive. No schema change. The full-fetch path is already tested.

**Code touch:** `timesheets.js` (export modal + filter logic), `index.html` (date-range inputs in export modal).

---

## Theme 2 — Leave management

### 4. Hard-delete leave requests (supervisor-only) (S)

**What:** Explicit TODO in `CLAUDE.md` — "Hard-delete leave requests — currently only Withdraw and Archive. Royce asked for a real delete option (supervisor-only, with confirm)." Add a Delete button on the leave detail / respond modal that fires a `DELETE` on `leave_requests?id=eq.<id>` after a confirm dialog.

**Why:** Archived requests accumulate forever. Some requests are test entries or erroneous submissions that should be purged, not preserved. The existing confirm modal pattern (`modal-confirm`) is already wired. Archive is reversible; delete is the "actually gone" escape valve supervisors need.

**Effort:** S — one new button, one `sbFetch` DELETE call, one `auditLog` entry, re-render. The confirm-modal pattern is reused exactly as in `confirmClearWeek`.

**Risk:** Low. Additive button behind `isManager` gate. No schema change. Already has archive as a safer default.

**Code touch:** `leave.js` (one new function + button in leave card), `index.html` (no structural change needed — uses existing confirm modal).

---

### 5. Leave balance / entitlement tracker (M)

**What:** Store and display a per-person annual leave balance (accrued days, days taken this year). When leave is approved and written to schedule, decrement the balance. Show a balance column on the leave list and on each person's contact card.

**Why:** Currently EQ Field tracks leave requests but has no concept of entitlement. Supervisors have to cross-reference their HRIS or spreadsheet to know if a person has leave remaining. This is a core labour-hire workflow gap — the system approves leave it can't actually verify is owed.

**Effort:** M — new column `leave_balance_days` on `people`, a running tally updated on approval, and a display column. No new table needed. One migration, two render updates.

**Risk:** Medium. DB migration on `people` table. Leave approval flow (`respondLeave`) touches an additional column. Not a breaking change to existing flow — balance is informational first, enforced later.

**Code touch:** `migrations/` (new column), `leave.js` (decrement on approval), `people.js` (display on contact card), `index.html` (leave list column).

---

### 6. Leave calendar — person filter (S)

**What:** The leave calendar (`calendar.js`) currently shows all people across all days. Add a person-search/filter so a supervisor can zoom into one person's leave history across months without scanning the full grid.

**Why:** The calendar view is already built but becomes cluttered with 30+ people. A single-person filter would make it the go-to view for answering "when is James next on leave?" without jumping to the list.

**Effort:** S — existing `calDayData` build loop already iterates `STATE.people`; add one filter input that gates the `STATE.people.forEach` in `renderCalendar`. No schema change.

**Risk:** Low. Additive filter, no data-path changes.

**Code touch:** `calendar.js` (one filter input + guard), `index.html` (filter input element).

---

## Theme 3 — Roster / scheduling

### 7. Roster copy-week (duplicate a week to another week) (S)

**What:** "Copy week" button in the roster editor that duplicates all schedule entries for the current week into a target week. The target week is selected from the existing `globalWeek` dropdown. Saves re-entering a stable roster every week.

**Why:** Most construction sites run the same roster week-to-week with minor adjustments. The current workflow is to fill each person manually or use "Fill Week" per person. A whole-roster copy shortcut is the most-requested roster time-saver in similar tools. The roster editor already has Fill Week per-person; this is the batch equivalent.

**Effort:** S — iterate `getWeekSchedule(currentWeek)`, call `saveRowToSB` for each row with the target week. New modal for week selection. No schema change.

**Risk:** Low. Additive. Uses existing `saveRowToSB`. Warn + skip if target week already has data.

**Code touch:** `roster.js` (new copy function), `index.html` (copy button + target week picker modal).

---

### 8. Roster conflict / gap alerts on dashboard (S)

**What:** The dashboard already highlights unrostered weekday cells in amber (`needsAttention` flag in `renderRoster`). Promote this data to the main Dashboard page as an alert card: "N people have unrostered days this week" with a list of names. Currently this information only appears inside the roster editor grid — supervisors have to actively look.

**Why:** A supervisor should see the gap count on dashboard load, not discover it mid-roster. The underlying computation is already done in `renderRoster`; it just doesn't surface to the Dashboard. This turns a passive visual into an actionable alert.

**Effort:** S — extract the gap-count logic from `renderRoster` into a shared helper, call it from `renderDashboard` to render an alert card. No schema change.

**Risk:** Low. Additive — new card on dashboard, no changes to existing roster rendering.

**Code touch:** `roster.js` (extract helper), `dashboard.js` (new gap-alert card).

---

### 9. Roster bulk-clear / bulk-assign for selected people (M)

**What:** A multi-select interface on the roster editor where a supervisor checks a set of people, then assigns the same site code or clears all their entries for the week. Currently "Fill Week" is per-person and "Clear Week" is per-person. Batch equivalent for the roster (analogous to the existing `openTsBatch()` in timesheets).

**Why:** Public holidays and site shutdowns affect all people at once. Clearing 30 people one-by-one is the most tedious weekly operation. The timesheet batch modal pattern is proven and directly reusable.

**Effort:** M — new modal pattern (reuse `modal-ts-batch` approach), iterate selected people, call existing `saveRowToSB`. Moderate DOM wiring but no new concepts.

**Risk:** Low. Uses existing write path. Additive modal. No schema change.

**Code touch:** `roster.js` (new batch function + modal), `index.html` (new modal, one batch button).

---

## Theme 4 — Labour-hire portal / availability

### 10. Staff availability / unavailability flags (M)

**What:** A per-person flag for "unavailable from/to" — separate from leave requests (which are workflow-heavy). Simple admin-set "unavailable" marker with a date range and reason (injury/training/notice period). Show on roster as a blocked indicator, block assignment on those days.

**Why:** Labour-hire supervisors need to flag workers who are off-hire, injured, or on notice without going through the leave approval workflow. Currently there is no mechanism for this. The people model has `archived` (permanent) but nothing for temporary unavailability. This is a core labour-hire workflow gap.

**Effort:** M — new `unavailability` table (person_id, date_start, date_end, reason, org_id) or a JSONB field on `people`. Render in roster as a blocked cell. New modal on the contact card.

**Risk:** Medium. New table or schema change. Roster render needs an unavailability check.

**Code touch:** `migrations/` (new table), `people.js` (set unavailability modal), `roster.js` (render blocked indicator), `dashboard.js` (count unavailable people).

---

### 11. Labour-hire portal self-serve availability (L)

**What:** A staff-facing page (visible when logged in with a staff PIN) where a worker can mark themselves available or unavailable for upcoming weeks, and view their upcoming schedule. Currently staff can only see "My Schedule" on the home tile. This adds a write path — "I'm available week of X" — that feeds into the supervisor's scheduling view.

**Why:** Labour-hire businesses constantly chase workers for availability. A self-serve input surface removes a daily phone/SMS round-trip. The mobile staff home screen (v3.5.0) already surfaces My Schedule; availability submission is the natural next step on the same surface.

**Effort:** L — new `staff_availability` table, staff-facing form, supervisor-facing availability summary view. Non-trivial but architecturally additive (staff-PIN-gated, new page, new table).

**Risk:** Medium-high. New DB table, new auth-gated write path for non-supervisor users. Requires care with the existing staff PIN vs manager PIN model.

**Code touch:** `migrations/` (new table), new `availability.js` script, `home.js` (staff tile), `index.html` (new page + nav entry gated to staff role).

---

## Theme 5 — Licences / compliance

### 12. Licence expiry alerts on dashboard and contacts (S)

**What:** EQ Cards (the companion app) tracks licence expiry dates. EQ Field's `people` table has a `licence` text field but no expiry date. Add `licence_expiry` date column to `people`, display a warning badge on the Contacts page for expiring/expired licences (e.g. within 30 days), and add an alert card to the Dashboard.

**Why:** An electrician with an expired licence cannot legally work on site. Today EQ Field has no way to surface this risk — it relies on manual checking or EQ Cards. Adding a lightweight expiry field to the people record bridges the gap without requiring the full Cards workflow. Critical for a labour-hire business selling compliance.

**Effort:** S — one nullable column, one badge in `_personActions` / contacts render, one dashboard alert card. No new table.

**Risk:** Low. DB migration is one nullable `date` column on `people`. Additive display.

**Code touch:** `migrations/` (new column), `people.js` (expiry badge in contacts), `dashboard.js` (expiry alert card).

---

### 13. Apprentice year auto-advance (annual) (S)

**What:** A one-click "Advance all apprentices to next year" action under the Apprentices section (or Import-Export). Bumps `people.year_level` for all non-4th-year apprentices at the start of a new calendar/training year. Currently `year_level` is updated manually per person.

**Why:** Apprentices advance through year levels annually. Today a supervisor manually edits each apprentice's year field. With even 5-10 apprentices this is error-prone. The `yearFromLicence` / `year_level` field is already in the model — this is a batch operation on existing data.

**Effort:** S — new supervisor-only action button, `sbFetch` PATCH with a filter on `group='Apprentice' AND year_level < 4`, confirm dialog, audit log entry. No schema change.

**Risk:** Low. Additive batch write, behind `isManager` gate + confirm modal. Existing `String()`-coerce pattern covers the uuid/bigint id difference.

**Code touch:** `apprentices.js` or `import-export.js` (one new batch function), `index.html` (one button).

---

## Theme 6 — Reporting

### 14. Weekly site attendance report (PDF/printable) (M)

**What:** A printable weekly report: for each site this week, list the assigned people, their job numbers (from timesheets if available), and headcount per day. Format suitable for emailing to a site foreman or client. The Site Reports HUB already exists for Prestart/Toolbox/Diary; this is a roster-level summary distinct from those workflows.

**Why:** Labour-hire clients often require a weekly labour schedule confirmation. Today supervisors export CSV and reformat it. A one-click "Print / PDF weekly report" button on the Dashboard or Roster would eliminate 30+ minutes of formatting per week.

**Effort:** M — `window.print()` on a purpose-built HTML render, or `exportTsCSV` extended with a site-grouped layout. No new table. A print stylesheet already exists conceptually from the leave print path in `leave.js`.

**Risk:** Low. Purely additive export. No schema change, no new auth path.

**Code touch:** `dashboard.js` or `roster.js` (new print render function), `index.html` (print button + print styles).

---

### 15. Audit log UI — searchable history (M)

**What:** A dedicated Audit Log page that queries `audit_log` from Supabase and renders a searchable, filterable table: filter by actor, module (Roster / Leave / Timesheet), date range, and person. Currently `auditLog()` is called throughout but there is no in-app surface to read the log — it goes silently to the DB.

**Why:** Supervisors and labour-hire businesses need a paper trail. "Who changed this roster entry?" is asked constantly after a dispute. The function `auditLog()` is called 50+ times across the codebase; the data is accumulating but invisible. The existing `audit.js` file exists (6957 bytes) — this surfaces what it already writes.

**Effort:** M — `audit.js` already exists; read its current state, add a query UI with filters. No new table.

**Risk:** Low. Read-only query of existing table. The schema mismatch noted in `CLAUDE.md` (`target_id`/`target_name` columns missing or mismatched with `verify-pin.js`) should be noted and a fix bundled.

**Code touch:** `audit.js` (extend with search/filter UI), `index.html` (existing audit page section).

---

### 16. Export roster to PDF / print view (S)

**What:** A print-formatted view of the current week's roster grid — site colour codes, person names, all 7 days — suitable for posting on a site whiteboard. Currently the roster grid is screen-only; printing it produces a broken table.

**Why:** Site supervisors still print and laminate rosters. "Print roster" is one of the most common requests in any labour management tool. The print media query work does not currently exist for the roster table.

**Effort:** S — CSS print media query + a `@media print` rule that hides sidebar/topbar/buttons and formats the roster table for A4. No JS change.

**Risk:** Low. CSS-only. Zero risk to existing functionality.

**Code touch:** `styles/base.css` or a new `styles/print.css` (add print media query), `index.html` (optional: add Print button that calls `window.print()`).

---

## Theme 7 — Mobile UX

### 17. Mobile roster grid — swipe to next day (S)

**What:** On mobile (viewport < 768px), the roster currently shows one day at a time with `←` / `→` arrows via `stepRosterDay()`. Add touch/swipe gesture support so swiping left/right advances the day. The day-paging logic is already built; this adds a gesture binding.

**Why:** The roster is the most-used mobile surface. Tapping arrows repeatedly is slow on mobile; swipe is the natural gesture. The `rosterActiveDay` / `stepRosterDay` infrastructure is already there.

**Effort:** S — add `touchstart` / `touchend` listeners to the roster content div; call `stepRosterDay(±1)` if horizontal swipe distance exceeds threshold. ~20 lines.

**Risk:** Low. Purely additive event listeners. No data-path changes.

**Code touch:** `roster.js` (swipe listeners in `renderRoster` mount or `initApp`), no schema change.

---

### 18. Supervisor mobile home — timesheets completion count tile (S)

**What:** The supervisor home screen (v3.5.1) has an action strip for leave + prestarts but the "Timesheets to review" count was explicitly dropped from MVP ("Timesheets to review" count dropped from MVP — no review-state column). Now that the approval schema migration is planned (item 2 above), wire the count: call `updateTsStats()` result to drive a badge on the Timesheets tile.

**Why:** Completing the action strip was an explicit design decision deferred only because the approval schema wasn't applied. Once item 2 ships, this is a 30-minute follow-on. Supervisors need a single-glance "N timesheets not yet approved" signal on the home screen.

**Effort:** S — depends on item 2. Once `approved` column exists, the accessor `eqGetTsUnapprovedCount` mirrors the pattern of `eqGetPendingLeaveCount`. One function + one tile badge update.

**Risk:** Low. Additive. Gated on item 2 schema landing.

**Code touch:** `timesheets.js` (new accessor function), `home.js` (wire count into supervisor tile).

---

## Theme 8 — Infra / DX

### 19. Audit log schema fix (audit_log target_id / target_name columns) (S)

**What:** `CLAUDE.md` schema gotchas: "`audit_log` schema doesn't currently match what `verify-pin.js` writes — known issue, the table needs `target_id`/`target_name` columns or the fn needs to drop them. Auth audit logging silently fails." Fix the schema or the function — either add the missing columns to `audit_log` or drop them from the `verify-pin.js` INSERT.

**Why:** Auth events (failed PINs, supervisor unlocks) are the most important audit trail entries. They are currently silently dropping. This is a correctness gap, not a feature.

**Effort:** S — one migration adding two nullable `text` columns, or a one-line edit to `verify-pin.js` to omit the fields.

**Risk:** Low. Either path is additive or removes failing writes. No user-visible change.

**Code touch:** `migrations/` (add columns to `audit_log`) OR `netlify/functions/verify-pin.js` (drop the two fields from the INSERT).

---

### 20. PIN double-source-of-truth fix (verify-pin reads Supabase directly) (M)

**What:** Explicit `CLAUDE.md` TODO: "PIN double-source-of-truth — same PIN lives in Supabase `app_config` AND Netlify env vars `STAFF_CODE`/`MANAGER_CODE`. They drift if you change one without the other. Right cleanup: refactor `verify-pin.js` to read Supabase `app_config` directly via `AUDIT_SB_URL`/`AUDIT_SB_KEY`."

**Why:** This is an operational hazard — a PIN change in Supabase won't propagate until someone also updates Netlify env vars. For a multi-tenant future, per-tenant PINs must come from the DB, not from a monolithic env var. This is the highest-value infra cleanup.

**Effort:** M — `verify-pin.js` needs a Supabase fetch at auth time, error handling, and a fallback. The env var fallback pattern (`AUDIT_SB_URL`/`AUDIT_SB_KEY`) is already defined.

**Risk:** Medium. Touches the auth backbone. Must be tested end-to-end on the demo deploy before merging. No user-visible change if done correctly.

**Code touch:** `netlify/functions/verify-pin.js` (DB read instead of env var compare), `index.html` / `auth.js` (no change needed — auth flow unchanged).

---

## Ranked summary table

| Rank | Feature | Theme | Effort | Risk | Additive? |
|------|---------|-------|--------|------|-----------|
| 1 | Smart timesheet pre-fill from roster | Timesheets | S | Low | Yes |
| 2 | Hard-delete leave requests | Leave | S | Low | Yes |
| 3 | Timesheet multi-week export | Timesheets | S | Low | Yes |
| 4 | Roster copy-week | Roster | S | Low | Yes |
| 5 | Licence expiry alerts | Licences | S | Low | Yes |
| 6 | Audit log schema fix | Infra | S | Low | Partial fix |
| 7 | Export roster to PDF/print | Reporting | S | Low | Yes |
| 8 | Roster conflict/gap alerts on dashboard | Roster | S | Low | Yes |
| 9 | Leave calendar person filter | Leave | S | Low | Yes |
| 10 | Apprentice year auto-advance | Licences | S | Low | Yes |
| 11 | Mobile roster swipe gesture | Mobile | S | Low | Yes |
| 12 | Timesheet approval schema + workflow | Timesheets | M | Medium | Partial (migration) |
| 13 | Audit log UI — searchable history | Reporting | M | Low | Yes |
| 14 | Weekly site attendance report | Reporting | M | Low | Yes |
| 15 | Roster bulk-clear / bulk-assign | Roster | M | Low | Yes |
| 16 | Leave balance / entitlement tracker | Leave | M | Medium | Partial (migration) |
| 17 | Supervisor mobile timesheets tile | Mobile | S | Low | Yes (depends on #12) |
| 18 | Staff unavailability flags | Labour-hire | M | Medium | Partial (migration) |
| 19 | PIN double-source-of-truth fix | Infra | M | Medium | Shared (auth backbone) |
| 20 | Staff availability self-serve portal | Labour-hire | L | Med-High | Partial (new table) |

---

## Recommended first batch

These 6 features can be built sequentially in ~3–4 days total, none touch the auth backbone, none require a risky DB migration, and all are directly supervisor-facing value visible in a demo:

| # | Feature | Why first |
|---|---------|-----------|
| 1 | Smart timesheet pre-fill from roster | Highest workflow impact; pure JS, no DB |
| 2 | Hard-delete leave requests | Explicit long-standing TODO; 30-min build |
| 3 | Timesheet multi-week export | Payroll integration unlock; reuses existing path |
| 4 | Roster copy-week | Eliminates the most repetitive roster task |
| 5 | Licence expiry alerts | Compliance story for demo conversations; 1 migration + display |
| 6 | Audit log schema fix | Correctness gap; unblocks the audit log UI |

Build order within the batch: 6 (fix the silent failure first) → 1 → 3 → 2 → 4 → 5.

After the first batch, the natural second wave is the approval workflow (#12), audit log UI (#13), and roster print view (#7) — each builds on infrastructure laid by the first batch.

---

## Explicitly out of scope (per brief)

- SKS safety / teams / pipeline modules (already ported and tenant-gated)
- B5 cutover (SKS live — Royce-gated)
- Auth re-platform (C4 — gated)
- EQ Shell Phase 2 (GTM-gated)
- Project Hours revival (Royce decided "leave dead" 2026-05-30)

---

## Open loops this backlog depends on

From `eq/pending.md` and `CLAUDE.md` — these must land before or alongside certain features above:

- Apply `migrations/2026-05-15_rate_limit_buckets_v1.sql` to `ktmjmdzqrogauaevbktn` (pending — not blocking backlog features directly)
- `clash_detected` PostHog event wire-up in `tender-pipeline.js` (separate Tender Pipeline concern)
- `pending_schedule` table decision (Tender Pipeline — separate concern)

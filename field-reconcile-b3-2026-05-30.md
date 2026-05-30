---
title: "EQ Field + SKS Merge — B3 Shared-Core Reconcile"
owner: Royce Milmlow
last_updated: 2026-05-30
scope: "Shared core scripts diverged between sks-nsw-labour (v3.10.x) and eq-solves-field (v3.5.28). Read-only analysis — no code changes."
read_priority: standard
status: live
---

# B3 Shared-Core Reconcile — EQ Field vs SKS NSW Labour

## Context

SKS NSW Labour has an 11-release lead over EQ Field (v3.10.40 vs v3.5.28). This analysis covers only the **shared core modules** present in both repos. It identifies bug fixes and feature improvements made in SKS that EQ Field lacks, then ranks them for carry-forward priority.

**What was diffed:**
`utils.js`, `roster.js`, `timesheets.js`, `home.js`, `batch.js`, `audit.js`, `import-export.js`, `managers.js`, `sites.js`, `people.js`, `dashboard.js`, `leave.js`, `presence.js`, `realtime.js`, `app-state.js`, `supabase.js`, `analytics.js`, `auth.js`, `calendar.js`, `jobnumbers.js`, `tafe.js`, `digest-settings.js`, `flags.js`, `sw.js`, `index.html` (shared logic sections).

**What was excluded:**
SKS-only modules (safety, teams, pipeline/pipeline-resource, project-hours) and EQ-only modules (apprentice-widget, forecast, diary, projects, region-filter, site-reports*, tender-pipeline, tender-parser, toolbox, lazy-loader, virtual-table).

---

## Ranked Carry-Forward Table

Items are ranked **value × low-risk first** — the safest high-value fixes at the top.

| # | File(s) | What SKS Fixed / Added | Why EQ Wants It | Risk to EQ | Effort |
|---|---------|------------------------|-----------------|------------|--------|
| 1 | `utils.js` | **WCAG keyboard nav on all modals** (v3.5.7–v3.5.8): `openModal`/`closeModal` now stack focus triggers, restore focus to the opener on close, trap Tab inside the topmost dialog, and handle ESC via `closeModal` (so focus restores correctly, not just `.classList.remove`). Also stamps `role="dialog"` + `aria-modal="true"` on first open. | EQ Field has none of this. Currently: modal closes dump focus to `<body>`, Escape just yanks `.open` off the class, Tab leaks into the background page. Directly impacts keyboard-only and screen-reader users. WCAG 2.4.3 + 2.1.1. | **Low** — pure addition; existing `openModal(id)` / `closeModal(id)` call sites are unchanged. Worst failure mode: Safari focus quirk, which is caught in a try/catch. | S (1 session) |
| 2 | `index.html` (polling loop), `realtime.js` | **Suppress 30s poll flicker when realtime is live** (v3.10.37): `startPolling`'s interval skips `refreshData()` while `isRealtimeConnected()` returns true. `isRealtimeConnected()` is one exported function in `realtime.js` that reads `_rtSocket.readyState === WebSocket.OPEN`. | EQ Field's `startPolling` does **not** have this guard. Every 30 s, whether or not a live WebSocket is carrying the data, the app re-fetches all data and re-renders every visible table — causing the roster/timesheets grid to flash. Realtime is enabled on EQ Field. This is a visible regression every session. | **Low** — additive guard. If realtime drops the poll resumes automatically. Two-line change to `index.html` + a single export in `realtime.js`. | XS (< 1h) |
| 3 | `sw.js` + `index.html` (SW handler) | **Auto-reload on SW update** (v3.10.21): On `activate`, the SW broadcasts `{ type: 'SW_ACTIVATED' }` to all open tabs. The page's `serviceWorker.addEventListener('message')` handler calls `window.location.reload()` on receipt. | EQ Field's `sw.js` calls `self.clients.claim()` but never sends the message. The page's SW listener only handles `FLUSH_WRITE_QUEUE`. Net effect: after every deploy, users run stale JS until they do a hard-refresh. The EQ Field CLAUDE.md explicitly lists "Service Worker auto-update toast" as a TODO — SKS has already solved it cleanly. | **Low** — two targeted additions: one `self.clients.matchAll` + `forEach postMessage` in `sw.js activate`, one `if SW_ACTIVATED` branch in the SW message listener in `index.html`. The `FLUSH_WRITE_QUEUE` path is untouched. | XS (< 1h) |
| 4 | `timesheets.js` | **5-day default view with weekend toggle** (v3.10.36): Timesheets default to Mon–Fri only. A button labelled "⊞ Weekends" (with a dot indicator when weekend data exists for the week) expands to Sat+Sun. `STATE.tsShowWeekends` is persisted in `localStorage`. | EQ Field always renders 7-day columns regardless of whether the week has any weekend entries. For any company without weekend rosters the Sat/Sun columns are always empty noise. `STATE.tsShowWeekends: null` is already declared in EQ Field's `app-state.js` — the wiring is just absent. | **Low** — `STATE.tsShowWeekends` is already a declared STATE field in EQ Field (line 371 of app-state.js). The toggle and `_showWE` column-filter logic are self-contained additions to the render path. | S (1 session) |
| 5 | `timesheets.js` | **Approval initials chip + leave-week pre-approval** (v3.10.35 + v3.10.25): Approved timesheet rows show a green initials badge (e.g. "RM") with hover text "Approved by Royce Milmlow". Unapproved rows show a faint ○ to tap. Leave-only weeks (no hours row yet) can be pre-approved by tapping the ○, which creates a stub timesheet row with `approved: true` so there's never a false "missing" count. | EQ Field has no approval indicators at all. Supervisors can approve (`timesheetApprove` function exists) but nothing visual confirms it per-row. For accounts review and payroll sign-off this is the primary pain point — you cannot tell at a glance which rows have been checked. | **Med** — requires the `approved`, `approved_by`, `approved_at` columns to exist on `timesheets` table. EQ's DB may not have them (SKS got them via a migration in the v3.10.x cycle). Need to check EQ's Supabase schema before porting. The JS logic itself is additive. | M (schema check + 1 session) |
| 6 | `timesheets.js` | **Collapsible group rows** (v3.10.31): Groups (Direct / Apprentice / Labour Hire) start collapsed; tap the group header to expand. State persisted in localStorage via `TS_GROUPS_LS_KEY`. | EQ Field always renders all rows expanded. For large rosters (Melbourne demo: 577 people) this is a scroll-and-render issue. Even for 50-person SKS, supervisors said it helped them focus on the one group they're checking. | **Low** — fully self-contained. The collapse state is a `Set` in a module-level `const`, written/read from localStorage. The render loop just skips `_tsCollapsedGroups.has(p.group)` rows. No changes to data shape or API calls. | S (1 session) |
| 7 | `timesheets.js` | **TAFE days count toward apprentice 40h total** (v3.10.7): `_tsApprenticeTotal()` adds 8h for each day the apprentice's roster shows a TAFE/training code. The total is used for the red/green completion indicator. | EQ Field calculates apprentice totals from entered hours only. If an apprentice has 3 site days + 2 TAFE days, EQ shows 24h entered (below 40h → red incomplete) when the true total is 40h. Wrong completion signal for apprentices every week. | **Low** — the `_tsDayStatus(name, week, d).tafeLabel` helper already exists in EQ Field (TAFE detection is in `roster.js`). This is a 12-line function wrapping the existing total helper. | XS (< 1h) |
| 8 | `timesheets.js` | **Scroll position preserved after cell save** (v3.10.40): `saveTsCell` captures `window.scrollY` and `.ts-table-scroll.scrollLeft` before triggering `renderTimesheets()`, then restores them afterward. | EQ Field scrolls back to the top of the page every time a job code or hours value is saved. In a 50-person table this means the supervisor has to scroll back down after every keystroke confirmation. Confirmed by the SKS commit message: "The full DOM rebuild was resetting scroll to 0 every time." | **Low** — two read + two write lines wrapped around the existing `renderTimesheets()` call. Completely isolated. | XS (< 1h) |
| 9 | `timesheets.js` | **Completion count fix** (`_tsRowStatus` applied to weekly tracker) (v3.10.26 + v3.10.25): The completion counter in the week summary header now counts rows as complete when `_tsRowStatus` returns `complete`, `on-leave`, or `tafe`. Previously the raw check missed leave/TAFE rows, showing them as incomplete. | EQ Field has the same raw check and will miscount completion for leave and TAFE weeks. The "Incomplete" filter chip shows phantom incomplete counts. | **Low** — one `_tsRowStatus` call replacing a direct hours check. `_tsRowStatus` exists in EQ Field (the function is shared). | XS (< 1h) |
| 10 | `home.js` | **Fuzzy gate-name matching in `getLoggedInName()`** (v3.10.12): If the name in `sessionStorage.eq_logged_in_name` doesn't exactly match any `STATE.people` entry, falls back to case-insensitive prefix/substring matching. | EQ Field's `getLoggedInName()` returns the raw sessionStorage string only — no fallback. If a staff member typed a short name at the gate (e.g. "Phil") but their record is "Philip Smith", the home screen shows "Nothing rostered" for them every time. | **Low** — self-contained inside `home.js`'s IIFE. No impact on auth or data. | XS (< 1h) |
| 11 | `home.js` | **`typeof STATE`/`typeof isManager` guards replacing `window.STATE`/`window.isManager`** (v3.10.23): SKS moved all `window.STATE &&` references to `typeof STATE !== 'undefined' &&`. Both patterns work but `typeof` is safer in strict-mode environments and avoids the double-access (first check `window.STATE`, then `STATE.currentWeek` without the window prefix — which throws in some edge cases). Also removes the brief "Nothing rostered" flash that preceded the STATE hydration fix. | EQ Field's `home.js` uses the `window.STATE` pattern throughout. In practice both work — but the v3.10.23 fix was specifically for a bug where `window.isManager` was undefined and broke the supervisor home rendering entirely. | **Low/Med** — purely defensive, but requires line-by-line review against EQ Field's own home.js (which has EQ-specific tile logic SKS doesn't have). SKS's home.js has diverged structurally (different tile set, different supervisor action strip). | M (careful merge, not a paste) |
| 12 | `home.js` | **Weekend shift-lookup guard** (v3.10.14): When `initApp` runs on Saturday/Sunday, `STATE.currentWeek` is bumped to next Monday. The home screen now detects this and starts the shift search from Monday (index 0) rather than today's weekday index (5 or 6), which was always out-of-range, producing "Nothing rostered" all weekend. | EQ Field's home screen doesn't guard for this. Staff who open the app on a weekend see "Nothing rostered" regardless of what Monday's roster says. | **Low** — a two-line guard inside the shift-search loop. But the structural divergence of the home.js IIFEs means this needs careful placement, not a paste. | S (targeted port) |
| 13 | `audit.js` | **Audit revert capability** (v3.4.76): `auditLog()` now accepts an `opts` object with `{before, after, target_table, target_id, target_field}`. `openAuditLog()` probes whether the DB table has been migrated (by checking for `before_value` on the first row) and gates the Revert button accordingly. `revertAuditEntry(id)` reverses the original write and stamps `is_reverted`. | EQ Field's `audit.js` does not pass `opts` to `auditLog`, has no schema probe, no per-row Revert button, and no `revertAuditEntry`. The SKS version preserves backwards compatibility with pre-migration schemas (the probe returns `null` on empty results and hides the UI). | **High** — requires a DB migration on EQ's `audit_log` table (add 6 columns + `is_reverted` boolean). The EQ CLAUDE.md already notes that "audit_log schema doesn't currently match what verify-pin.js writes". This compounds that technical debt. The JS side is safe; the migration is the risk. | L (migration + JS + testing) |
| 14 | `batch.js` | **`PEOPLE_GROUPS` constant used instead of inline array** (minor): SKS's `buildBatchPeopleList()` reads `PEOPLE_GROUPS` (defined in `app-state.js`) rather than hardcoding `['Direct', 'Apprentice', 'Labour Hire']`. | EQ Field hardcodes the array. If the group list ever changes (e.g. adding a "Supervisor" group) EQ's batch picker won't update automatically. | **Low** — one-line change. But it's a minor correctness issue, not a bug. | XS (< 15 min) |
| 15 | `import-export.js` | **`BUG-016`: `toCSV` defined explicitly** — prevents silent collision if `utils.js` ever defines a different version. | Low-severity; the function is identical in both. Belt-and-braces clarity only. | **Low** — no behaviour change. | XS |

---

## Not Applicable to EQ — SKS-Only Behaviour

The following changes in the v3.10.x SKS cycle must **not** be ported because they are SKS-tenant-specific or reference safety/teams modules that are gated to `sks` in EQ Field:

| SKS Version | What it does | Why not for EQ |
|-------------|--------------|----------------|
| v3.10.28 | Home: Prestart + Toolbox tiles for staff | Requires safety module (tenant-gated to `sks`). EQ's home tile set is different. |
| v3.10.29 | Safety dashboard compliance report | Safety module is SKS-only. |
| v3.10.34 | Teams: multi-select filter pill row | Teams module is SKS-only. `personInActiveTeam()` doesn't exist in EQ. |
| v3.10.38 | Auth: EQ Core parallel login + Shell handoff polish | This was done on SKS's version of the handoff — EQ Field already has the canonical version of this (v3.5.9–v3.5.12). Do not re-import. |
| v3.10.31 | Timesheets: teams filter inside the TS group pills | Depends on `personInActiveTeam()` from teams module. The collapse-group and Direct-group parts are portable (items 6 and below). The teams-filter part is not. |
| v3.10.32/33 | Timesheets: "fix SKS Direct group matching" / "fix Direct group matching" | These commits specifically fixed a bug where the old group filter excluded "Direct Employee" rows because the group string was `'Direct Employee'` not `'Direct'`. In EQ Field the group string is canonically `'Direct'` (matches `PEOPLE_GROUPS`). This is a SKS-data-specific fix that doesn't apply to EQ. |
| v3.10.4 | Push notifications: roster change alerts for staff | Web Push requires VAPID keys and a push server. EQ doesn't have this infrastructure yet. Not wrong to port eventually, but it's a new feature sprint, not a reconcile item. |
| v3.10.6 | Employee mobile: clean topbar, no irrelevant nav | SKS's mobile nav has a different 4-item bar (v3.10.16). EQ's mobile nav is different. |

---

## Recommended First Batch (safe, apply together)

These are low-risk, additive, and independently valuable. None require a DB migration or structural merge:

1. **#2 — Realtime poll suppress** (`index.html` + `realtime.js`) — eliminates the 30s roster flash. Two lines.
2. **#3 — SW auto-reload** (`sw.js` + `index.html`) — ends the hard-refresh requirement after every deploy. Four lines.
3. **#7 — TAFE counts toward apprentice 40h** (`timesheets.js`) — correctness fix; wrong completion signal every week for apprentice rows.
4. **#8 — Scroll position after cell save** (`timesheets.js`) — eliminates one of the most frustrating daily UX bugs in timesheets.
5. **#9 — Completion count fix** (`timesheets.js`) — stop false "incomplete" counts for leave/TAFE weeks.
6. **#4 — 5-day default view** (`timesheets.js`) — `STATE.tsShowWeekends` is already wired; just needs the toggle UI and column filter.
7. **#6 — Collapsible TS groups** (`timesheets.js`) — self-contained, no schema dependency.
8. **#10 — Fuzzy gate-name matching in home.js** — one targeted function replacement inside the IIFE.
9. **#14 — `PEOPLE_GROUPS` in batch.js** — trivial one-liner.

**Combine items #3–#9 into a single "timesheets + SW polish" PR** (they're all low-risk and logically cohesive). Items #2 and #1 can be separate PRs.

---

## Needs Careful Review Before Porting

| Item | Why careful | Precondition |
|------|-------------|--------------|
| **#1 — Modal keyboard nav** (`utils.js`) | Touches the global `openModal`/`closeModal` — every modal in the app is affected. Needs a full smoke-test of every modal (Leave request, People edit, Sites edit, Supervisors edit, Batch fill, Audit, etc.) across keyboard and touch. | None — but allocate a full smoke-test session after landing. |
| **#5 — Approval chips + pre-approve leave** (`timesheets.js`) | Requires `approved`, `approved_by`, `approved_at` columns on the `timesheets` table in EQ's Supabase. Run `select column_name from information_schema.columns where table_name = 'timesheets'` first. If columns are missing, write the migration before the JS. | Schema check + migration (if needed). |
| **#11 — `typeof` STATE guards in home.js** | EQ and SKS home.js have structurally diverged tile sets. Cannot paste — must apply as a diff. Requires reading both files in parallel and applying only the guard pattern, not the SKS tile/nav structure. | Side-by-side diff session. |
| **#12 — Weekend shift-lookup guard** (`home.js`) | Same structural divergence as #11. Two lines in the right place, but the right place differs between the repos. | Same as #11 — combine into one careful home.js session. |
| **#13 — Audit revert** (`audit.js`) | DB migration on live EQ Supabase. The table is already mismatched per CLAUDE.md. Needs a migration written to `migrations/`, applied via MCP, and verified before JS lands. The JS itself is safe (schema-probed, backwards compatible). | Schema migration approved and applied first. |

---

## Summary

- **Total carry-forward candidates identified:** 15
- **High-risk items:** 1 (#13 audit revert — requires DB migration on live EQ)
- **Medium-risk items:** 3 (#5 approval chips — schema dependency; #11 home.js STATE guards — structural merge; #12 weekend fix — structural merge)
- **Low-risk items:** 11 (all others — additive, self-contained, schema-free)
- **SKS-specific, must not port:** 8 items (safety tiles, teams filter variants, push notifications, Direct-Employee string fix)

All 15 items are **EQ behaviour changes** (not tenant-gated) so each one goes through Royce's per-item approval before a PR is opened.

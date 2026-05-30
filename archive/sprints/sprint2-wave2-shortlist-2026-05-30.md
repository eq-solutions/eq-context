---
title: "EQ Sprint 2 — Wave-2 Shortlist"
owner: Royce Milmlow
last_updated: 2026-05-30
scope: "EQ Field, EQ Service, Quality/Polish — next-ranked unbuilt items after Wave-1 delivery"
read_priority: standard
status: live
---

# EQ Sprint 2 — Wave-2 Shortlist

Wave-1 items excluded per brief. Service items verified against the live App Router
codebase (`C:\Projects\eq-solves-service`) before inclusion — see **Already-Built
Exclusions (Service)** section at the end.

Effort: **S** = half-day, **M** = 1–2 days, **L** = 3+ days.
Migration flag = DB change needed but not planned here; flag only.

---

## Stream 1 — EQ Field (next 6, ranked)

### F-W2-1 · Export roster to PDF / print view
**What:** CSS `@media print` rules that hide sidebar/topbar/buttons and render the
roster grid A4-ready. One optional "Print roster" button calling `window.print()`.

**Why:** Site supervisors print and laminate rosters. The screen-only grid produces
a broken table when printed. Pure CSS — zero risk to existing functionality.

**Effort:** S
**Risk:** Low — CSS-only, no JS data path touched.
**Additive vs shared:** Additive (new stylesheet block).
**Migration needed:** No.

---

### F-W2-2 · Roster conflict / gap alerts on dashboard
**What:** Extract the gap-count logic already inside `renderRoster` into a shared
helper. Call it from `renderDashboard` to surface an alert card: "N people have
unrostered days this week" with a name list.

**Why:** Unrostered-day detection is already computed inside the roster editor but
invisible on the dashboard. Turns a passive visual into a proactive daily signal
for supervisors.

**Effort:** S
**Risk:** Low — additive dashboard card; no changes to roster rendering.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### F-W2-3 · Leave calendar — person filter
**What:** One filter input on the leave calendar that gates the `STATE.people.forEach`
loop in `renderCalendar` to a single person. Makes the calendar the go-to view for
"when is James next on leave?" without scanning a 30+ person grid.

**Why:** Calendar view already built; useful but cluttered at scale. Single-person
filter is the obvious usability unlock.

**Effort:** S
**Risk:** Low — additive filter, no data-path changes.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### F-W2-4 · Apprentice year auto-advance
**What:** One supervisor-only "Advance all apprentices to next year" button.
Fires a batch PATCH on `people` where `group='Apprentice' AND year_level < 4`.
Confirm dialog + audit log. Uses the existing `isManager` gate.

**Why:** Manual per-person year-level edits are error-prone with 5–10 apprentices.
`year_level` field already exists; this is a 30-minute batch operation on existing
data.

**Effort:** S
**Risk:** Low — additive write behind `isManager` gate + confirm modal.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### F-W2-5 · Timesheet approval schema + bulk-approve workflow
**What:** Apply the migration adding `approved`, `approved_by`, `approved_at` nullable
columns to the `timesheets` table. Expose: (a) bulk approve-week button for
supervisors, (b) edit-lock guard in `saveTsCell` when `approved = true`. The
approval chip `_tsApprovalChip` already renders gracefully without the columns.

**Why:** The UI already exists with graceful degradation (CLAUDE.md v3.5.30 #5).
Labour-hire timesheets need an approval sign-off before payroll — this is the
missing close loop.

**Effort:** M
**Risk:** Medium — DB migration required.
**Additive vs shared:** Partial (migration + edit-lock touches shared `saveTsCell`).
**Migration needed:** Yes — 3 nullable columns on `timesheets` table
(`ktmjmdzqrogauaevbktn`). Flag before running.

---

### F-W2-6 · Audit log UI — searchable history
**What:** Extend `audit.js` (already 6957 bytes) with a query UI: filter by actor,
module (Roster / Leave / Timesheet), date range, person. Read-only query of the
existing `audit_log` table. Bundle the `target_id` / `target_name` schema fix
(E3 from quality backlog) as a prerequisite.

**Why:** `auditLog()` is called 50+ times across the codebase; the data accumulates
but is invisible. Supervisors need "who changed this roster entry?" for dispute
resolution.

**Effort:** M
**Risk:** Low — read-only query surface. Schema fix is additive.
**Additive vs shared:** Additive.
**Migration needed:** Yes — add `target_id text` and `target_name text` nullable
columns to `audit_log` (or drop them from `verify-pin.js` insert). Flag before
running.

---

## Stream 2 — EQ Service (next 5, verified unbuilt)

### S-W2-1 · Defect detail page + photo attachments
**What:** Add `/defects/[id]` — full-page defect record with photo/attachment
support (`AttachmentList` component already exists; `attachments` table and Storage
bucket already exist). Surface defects properly on `/portal/defects` (route exists
but is sparse).

**Why:** Defects currently live in a flat expand-in-list interaction — no shareable
URL, no photo evidence, no customer portal link. A detail page unlocks: portal
deep-link, photo evidence for the customer report, and a work-order follow-up URL.

**Effort:** M
**Risk:** Low — no schema change; attachments table supports polymorphic links.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### S-W2-2 · Analytics — per-customer and per-technician cuts
**What:** Add (a) customer + date-range filter matching the Reports page pattern,
(b) a per-technician table (checks completed / overdue / avg time-to-complete),
(c) server-side RPCs to replace the full-table pulls. Pattern exists in
`get_customer_period_summary` (migration 0099) and `get_dashboard_counts`
(migration 0100) — the analytics page just hasn't adopted it.

**Why:** Current KPI tiles are tenant-wide and undifferentiated. The two questions
Royce asks in every account review — "how is SY6 tracking?" and "who is our slowest
tech?" — cannot be answered today.

**Effort:** M
**Risk:** Low — new RPCs + filter UI, no schema change.
**Additive vs shared:** Additive.
**Migration needed:** No (new read-only RPCs only; additive migration).

---

### S-W2-3 · Canonical export — fill the stubs
**What:** In `lib/admin/canonical-export.ts`, implement the four stub exporters:
`nsx_test`, `rcd_test`, `contract_scope`, `pm_calendar`. Follow the pattern of
existing `exportAcbTest`, `exportMaintenanceCheck`.

**Why:** The `/admin/backup` route is currently incomplete for most entities. A
backup that omits NSX test results, RCD records, and PM calendar is not a usable
backup. Hard dependency for the Field merge (Stream D3) and eventual canonical sync.

**Effort:** M
**Risk:** Low — pure data transformation; existing exporters are the template.
**Additive vs shared:** Additive (fills existing surface).
**Migration needed:** No.

---

### S-W2-4 · Asset detail page
**What:** Add `/assets/[id]` — asset metadata, linked maintenance checks (last 3),
linked tests (ACB/NSX/RCD), open defects, attachment list, calibration history.
All source data exists; no new schema needed.

**Why:** Today you cannot answer "what is the full test history for CB-12 at SY4?"
without scrolling through the check list. An asset-level history view is standard
CMMS expectation and a prerequisite for QR label scanning (S-W2-5).

**Effort:** M
**Risk:** Low — pure read aggregation page.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### S-W2-5 · Instrument calibration due reminders
**What:** Extend the `dispatch-notifications` cron to check `instruments` where
`calibration_due < now() + interval '30 days'` and send the responsible user a
bell + email reminder. Add a "Calibration Due Soon" filter on the Instruments page.

**Why:** An out-of-calibration instrument used on-site generates invalid test results
— regulatory exposure for both EQ/SKS and the customer. The instruments table and
`calibration_due` column exist; the notification cron runs daily. Closes a compliance
gap at near-zero build cost.

**Effort:** S
**Risk:** Low — cron extension + one filter; same Resend dependency as supervisor
digest.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

## Stream 3 — Quality / Polish (next 6, ranked)

Wave-1 already shipped: A1 (Modal focus trap), A2 (SlidePanel focus trap), A3
(Service global focus-visible), A4 (Shell global focus-visible), E1 partial
(loading.tsx for dashboard/customers/job-plans/contacts/maintenance + error.tsx),
Z2 (TenantHome live-feed fix), L3 (briefing loading state decoupled).

### Q-W2-1 · A5 — Service sidebar skip-navigation link
**What:** Add a visually-hidden skip link `<a href="#main-content">Skip to content</a>`
that becomes visible on focus to the Service sidebar. Keyboard users can then bypass
the 12-item nav.

**Why:** Without a skip link, keyboard users must tab through every sidebar item on
every page load — WCAG 2.4.1 compliance gap.

**Effort:** S
**Risk:** None.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### Q-W2-2 · E2 — Unify iframe load-failure UX in Shell
**What:** Standardise all four iframe error states (`ServiceIframe`, `CardsIframe`,
`FieldIframe`, `QuotesIframe`) onto `EqError` with `onRetry`. Currently all four
differ slightly.

**Why:** Inconsistent error surfaces undermine trust in the shell. One pattern is
easier to maintain and test.

**Effort:** S
**Risk:** None.
**Additive vs shared:** Shared (touches four Shell components).
**Migration needed:** No.

---

### Q-W2-3 · E4 — EqError retry button — loading state + aria-label
**What:** Add `aria-label="Try again"` and a disabled/loading state to the `onRetry`
button in `EqError` so double-clicks don't fire multiple fetches.

**Why:** Currently the button has no feedback after click and no keyboard label.
Quick accessibility + correctness fix.

**Effort:** S
**Risk:** None.
**Additive vs shared:** Shared (`EqError` used in multiple places).
**Migration needed:** No.

---

### Q-W2-4 · E5 — Dashboard null-tenant "workspace not ready" notice
**What:** In Service `dashboard/page.tsx`, when `tenantId` is null and the user is
not an admin, surface a minimal "workspace not ready" notice instead of KPI cards
full of zeros.

**Why:** A read-only user with a broken membership currently sees a page full of
zero-value KPIs with no signal that setup is incomplete.

**Effort:** S
**Risk:** Low — additive conditional render.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### Q-W2-5 · L2 — Detail page loading.tsx (maintenance/[id], sites/[id], testing detail routes)
**What:** Add `loading.tsx` files for `/maintenance/[id]`, `/sites/[id]`, and the
three testing detail routes (`/testing/acb/[testId]`, `/testing/nsx/[testId]`,
`/testing/rcd/[id]`). `PageSkeleton` is already available.

**Why:** The `/maintenance/[id]` page is the most-used surface in Service. It
fetches check + assets + linked tests + attachments in parallel with no loading
state — blank white during SSR. Six 5-line files.

**Effort:** S
**Risk:** None.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

### Q-W2-6 · U3 + U4 — Shell NotFound jargon fix + sync bar aria
**What:** (a) `NotFound.tsx` — replace architecture-jargon copy ("42 canonical
entities") with plain English ("Import rosters and staff"). (b) Sync bar dots in
`TenantHome` — add `aria-hidden` to decorative dots; add a meaningful `aria-label`
to the parent status container.

**Why:** CLAUDE.md voice rule: no architecture jargon on user-facing surfaces.
Sync bar dots have no screen-reader meaning and emit raw "●" characters.

**Effort:** S (two 5-minute fixes bundled)
**Risk:** None.
**Additive vs shared:** Additive.
**Migration needed:** No.

---

## Already-Built Exclusions (Service) — Verified 2026-05-30

The following backlog items were listed in `service-feature-backlog-2026-05-30.md`
but were **found already implemented** in the live codebase and must be excluded from
all waves:

| Backlog item | What was claimed missing | What was found |
|---|---|---|
| Site access fields edit UI (backlog #2) | "not exposed in SiteForm" | `SiteForm.tsx` lines 344–372 already contain all four fields (`gate_code`, `parking_notes`, `after_hours_phone`, `safety_notes`) with defaultValue wiring |
| Notification firing — `defect_raised` (backlog #4) | "absent from `createDefectAction`" | `actions.ts` line 1499–1507 calls `notifyDefectRaised()`; `check_assigned` fires at lines 671–674 and 810–813; `check_due_soon` and `check_overdue` are both handled in `dispatch-notifications/route.ts` |
| Field sync admin UI trigger (backlog #7) | "no trigger button" | `IntegrationsClient.tsx` line 52 calls `syncSitesFromFieldAction`; the integrations page is fully wired |
| Renewal pack UI entry point (backlog #8) | "no page.tsx exists" | `app/(app)/commercials/renewal-pack/` contains `page.tsx`, `RenewalPackForm.tsx`, and `actions.ts`; the page is built |
| Customer portal scope register (backlog #15) | "add a read-only Scope Register" | `app/(portal)/portal/scope/page.tsx` exists and queries `contract_scopes` with FY grouping and included/excluded display |
| Scope-from-Work Derive (backlog #17) | "currently a dead link" | `app/(app)/commercials/contract-scopes/derive/` contains `page.tsx`, `DerivedScopeWizard.tsx`, and `actions.ts`; the route is built |

These six items are **excluded from all Wave planning**.

---

## Build order suggestion (within Wave 2)

**Field:** F-W2-1 → F-W2-2 → F-W2-3 → F-W2-4 (all S, no DB) → F-W2-5 (M, migration) → F-W2-6 (M, migration)

**Service:** S-W2-5 (S, quick win) → S-W2-1 (M, defect detail) → S-W2-2 (M, analytics) → S-W2-3 (M, export stubs) → S-W2-4 (M, asset detail)

**Quality:** Q-W2-1 → Q-W2-5 (highest WCAG + UX value) → Q-W2-2 → Q-W2-3 → Q-W2-4 → Q-W2-6

Note F-W2-5 (timesheet approval) and F-W2-6 (audit log UI) both require DB migrations — flag to Royce before running either. F-W2-5 also unlocks the supervisor mobile timesheets tile (F rank 17, deferred to Wave 3 as a follow-on).

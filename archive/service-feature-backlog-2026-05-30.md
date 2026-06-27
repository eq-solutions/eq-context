---
title: "EQ Service — Feature Backlog 2026-05-30"
owner: Royce Milmlow
last_updated: 2026-06-01
scope: EQ Solves Service (eq-solves-service) — ranked feature candidates for the next push
read_priority: standard
status: live
---

# EQ Service — Feature Backlog

Ranked by value × effort (high value + low effort = top). Evidence sourced from a
read-only audit of `C:\Projects\eq-solves-service` (app/, components/, lib/,
supabase/migrations/, docs/) and `C:\Projects\eq-context` (eq/products.md,
eq/pending.md, SPRINT-BOARD.md, STATE.md).

**PPM canonical realignment (Stream E2) is noted but PAUSED per the sprint board — it
appears as a flagged item at the end, not in the main ranking.**

---

## ✅ BUILD STATUS (updated 2026-06-01)

**Done this sprint:**
- **#2 Site Access Fields — edit UI** → PR #223 merged. Four fields (`gate_code`, `after_hours_phone`, `parking_notes`, `safety_notes`) in SiteForm collapsible section.
- **#3 Defect Detail Page** → PR #223 merged. `/defects/[id]` route + `DefectRow.tsx` links. Photo attachments deferred (AttachmentList wiring = M effort).
- **#1 Pre-visit Tech Brief (label)** → PR #220: label updated from "Scheduled Start" to "Planned Visit". Phase 1 email/ICS = still open.

**Found already done in prior sessions (PRs #205–#213):**
- **#4 Notifications** — `defect_raised` + `check_assigned` both wired in actions.
- **#5 Analytics cuts** — per-customer date filter + per-tech table already live.
- **#6 Canonical Export (NSX/RCD)** — all stubs filled; backup complete.
- **#7 Field Sync admin UI** — "Sync sites from EQ Field" button + last-synced display live on Integrations page.
- **Portal defects** — `/portal/defects` fully populated.

**Still open / Royce-gated:**
- **#1 ICS email** — Resend template + `.ics` builder (needs `RESEND_API_KEY` in Netlify env)
- **#8 Renewal Pack UI** — page.tsx still missing
- **#9 Defect → WO email** — Resend call-site in `createDefectAction` not yet added
- **#10 Delta WO dry-run** — validation task, Royce runs on SKS tenant
- **#11 Asset Detail** — `/assets/[id]` still needed
- **#12–#20** — all deferred; see Group 4 below
- **PPM canonical realignment (E2)** — ⏸ still paused

---

## Context snapshot (what the codebase already has)

Before ranking, the material gaps and half-built surfaces identified in the audit:

| Surface | State |
|---|---|
| Defects register | Built (list + expand-to-edit rows) — no detail page, no photo attachments, no customer-portal visibility beyond the `/portal/defects` stub |
| Pre-visit tech brief | `scheduled_start_at` column added (migration 0096), Phase 0 schema only — no UI to set the visit time, no ICS/email generation |
| Notifications | Bell + email preferences form built — `email_enabled` wired but actual Resend delivery for events (not just digest) is incomplete; `defect_raised` in the opt-out list but the event firing is absent from `createDefectAction` |
| Canonical export | `contact`, `attachment`, `maintenance_plan`, `nsx_test`, `rcd_test`, `contract_scope`, `pm_calendar` exporters are stubs — return 0 rows |
| Field sync | One-way pull (`syncSitesFromFieldAction`) built for sites, stamped with `canonical_field_id` + `field_synced_at` — no UI in the Integrations page to trigger it |
| Defect detail / work order | No `/defects/[id]` route; defects surface only in the flat list expand |
| Portal | Reports + Variations + Scope pages live; Defects portal page exists (`/portal/defects`) but is sparse |
| Commercials / Renewal Pack | Action exists (`generateCustomerRenewalPack`) — no UI entry point beyond the hub card that links to an unbuilt `/commercials/renewal-pack` route |
| Scope derive | `/commercials/contract-scopes/derive` card on the Commercials hub — route does not exist |
| Commercial scope import | `/commercials/contract-scopes/import` — route unclear; contract-scope CSV import exists at `/contract-scope` already |
| Delta WO import dry-run | Pending per `eq/pending.md` — live dry-run on SKS tenant with Aug 2025 file not yet done |
| Site access fields | Added in migration 0105 (`gate_code`, `parking_notes`, `after_hours_phone`, `safety_notes`); SiteContextCard already reads them — no editing UI on the site form |
| Analytics | Built but pulls full-table counts (no server-side date windowing); no per-customer or per-technician cut |
| Canonical asset bridge | Stream D3 on the sprint board — dormant branch, not pushed |

---

## Ranked Backlog

### Group 1 — Mobile / Field-tech UX (highest daily-driver impact)

---

#### 1. Pre-visit Tech Brief — Phase 1 UI + email/ICS

**What.** Wire the `scheduled_start_at` column (already migrated, migration 0096)
into an inline date-time editor on `/maintenance/[id]`. When saved, send the
assigned technician a "You're on for X" email via Resend with the site address,
access notes, and an `.ics` calendar attachment. The data layer (`SiteContextCard`,
`after_hours_phone`, `gate_code`, `parking_notes`, `safety_notes`) is already
surfaced on the check page.

**Why.** The CMMS's biggest real-world friction for a field tech is "I forgot the
site details / I'm at the wrong entrance". The schema is done; the site-context
card already renders address + access notes on-screen. Adding the visit-scheduling
step and the ICS email converts a read-only info panel into an actionable dispatch
workflow. This is the feature that turns EQ Service from a compliance tracker into
a genuine CMMS dispatch tool.

**Effort.** S — inline date-time input on CheckDetailPage + `updateCheckScheduledStartAction`
server action + small Resend template with ICS builder. All dependencies are in
place.

**Risk.** Low. Email delivery depends on Resend being wired (env var `RESEND_API_KEY`
must be set — same dependency as the supervisor digest). No schema change needed.

**Shared vs additive.** Additive — no existing flows broken.

---

#### 2. Site Access Fields — Edit UI on SiteForm

**What.** Four columns landed in migration 0105 (`gate_code`, `parking_notes`,
`after_hours_phone`, `safety_notes`) and are already read by `SiteContextCard` on
the check page. They are not exposed in the site form (`app/(app)/sites/SiteForm.tsx`).
Add a collapsible "Access & Safety" section to the site form so admins can fill
them in.

**Why.** The SiteContextCard is already rendering these fields — a tech navigating
to their check page today sees a blank section where the access codes should be.
Every site that lacks this data is a silent gap in the pre-visit brief (feature #1
above). This is a direct dependency for #1 to provide real value.

**Effort.** XS — four `<FormInput>` fields in an existing form, one server action
update (already handles other site fields), no migration needed.

**Risk.** Very low. Pure additive form fields.

**Shared vs additive.** Additive.

---

#### 3. Defect Detail Page + Photo Attachments

**What.** Add `/defects/[id]` — a full-page defect record. Move the expand-in-list
edit panel to the detail page. Add photo/attachment support (the `attachments` table
and Supabase Storage bucket already exist; `AttachmentList` is a reusable component).
Surface defects on the `/portal/defects` page (the route exists but is sparse).

**Why.** Defects are a core CMMS output — every maintenance check can generate them.
Right now they live in a flat expand-in-list interaction that cannot hold photos,
cannot be shared as a URL, and cannot be surfaced properly to the customer in the
portal. A detail page unlocks: link from the customer portal, photo evidence for
the customer report, and a shareable URL for work-order follow-up.

**Effort.** M — detail page + attachment wiring + portal page. `AttachmentList`
is already built. The defect CRUD actions exist.

**Risk.** Low. No schema change needed; attachments table supports polymorphic links
already.

**Shared vs additive.** Additive.

---

### Group 2 — Reporting / Exports (customer-facing value + SKS sales motion)

---

#### 4. Notification Events — Complete the Firing

**What.** The notification preferences form (`NotificationPreferencesForm`) has
`defect_raised` in the opt-out list. The `createNotification` function exists. But
`createDefectAction` in `app/(app)/maintenance/actions.ts` does not call it. Wire:
`defect_raised` on defect create, `check_assigned` on assign, `check_due_soon` on
the scheduled cron, `check_overdue` on status flip. The preferences form and bell
already handle display and opt-out.

**Why.** Notifications are table stakes for any CMMS. The bell drops to zero value
if it only fires on check-complete (the only current trigger). For SKS/Equinix:
a supervisor needs to know when a tech raises a defect so corrective work can be
scheduled before the customer sees it.

**Effort.** S — three to four `createNotification()` call-sites in existing actions,
no schema change. The cron for `check_due_soon` has a route at
`/api/cron/supervisor-digest`; extending it to the bell-notification path is
straightforward.

**Risk.** Low. The notification table, RLS, and bell UI already exist.

**Shared vs additive.** Additive.

---

#### 5. Analytics — Per-customer and Per-technician Cuts

**What.** The Analytics page currently pulls all data across the tenant and does
in-memory aggregation (full-table fetch, no server-side windowing). Add:
(a) customer + date-range filter matching what the Reports page already has,
(b) a per-technician table showing checks completed / overdue / average time-to-complete,
(c) server-side aggregation (RPCs) to replace the `LIMIT 10000` full-table pulls.

**Why.** The existing KPI tiles are tenant-wide and undifferentiated — they can't
answer "how is SY6 tracking?" or "who is our slowest tech?". These are the two
questions Royce asks most in an account review. The `get_customer_period_summary`
RPC (migration 0099) and `get_dashboard_counts` (migration 0100) show the pattern
already exists — the analytics page just hasn't adopted it yet.

**Effort.** M — two new RPCs + filter UI + per-tech table. No schema change.

**Risk.** Low. Performance improvement + information gain, no data risk.

**Shared vs additive.** Additive.

---

#### 6. Canonical Export — Fill the Stubs (NSX, RCD, Contract Scope, PM Calendar)

**What.** In `lib/admin/canonical-export.ts`, `nsx_test`, `rcd_test`,
`contract_scope`, and `pm_calendar` return stub objects (0 rows, "exporter not yet
implemented"). Contact and attachment exporters are also stubs. Write the actual
mapping functions following the pattern of the existing `exportAcbTest`,
`exportMaintenanceCheck` etc.

**Why.** The `/admin/backup` and `/api/admin/export` routes are currently incomplete
for most entities. A backup that omits NSX test results, RCD records, and PM
calendar is not a usable backup. For the Field merge (Stream D3) and eventual
canonical sync, correct export shapes are a hard dependency.

**Effort.** M — data mapping functions only, no schema changes.

**Risk.** Low. Pure data transformation; existing exporters are the template.

**Shared vs additive.** Additive (fills existing surface).

---

### Group 3 — Workflow Completions (half-built surfaces)

---

#### 7. Field Sync — Admin UI Trigger

**What.** `syncSitesFromFieldAction` (in `app/(app)/admin/integrations/actions.ts`)
is complete — it calls the Field API, upserts sites, stamps `canonical_field_id` and
`field_synced_at`. The Admin hub has an Integrations card but the `/admin/integrations`
page likely has no trigger button. Surface a "Sync sites from EQ Field" button with
last-synced timestamp.

**Why.** The EQ Field → Service site-sync is the first real cross-app data bridge.
Without a UI to trigger it, admins have no way to pull updated sites after Field
onboards a new customer or renames a site. The action is production-ready.

**Effort.** S — one page with a button + server action call + last-synced display.
The action is already written.

**Risk.** Low — depends on `FIELD_API_URL` and `EQ_SECRET_SALT` being set in Netlify
env vars. Graceful error handling is already in the action.

**Shared vs additive.** Additive.

---

#### 8. Renewal Pack — UI Entry Point

**What.** `generateCustomerRenewalPack` in `lib/reports/customer-renewal-pack.ts`
exists. The action wrapper in `app/(app)/commercials/renewal-pack/actions.ts` exists.
The `/commercials/renewal-pack` URL is referenced in the Commercials hub card —
but no `page.tsx` exists for it. Build the page: customer picker, FY selector,
optional executive summary override, format toggle (DOCX/PDF), generate button.

**Why.** The renewal pack is the commercial artefact that drives FY contract
renewals — the most direct revenue-protection output the app can produce. It's gated
on `commercial_features_enabled` so it doesn't surface to free-tier tenants. The
generator is built; the UI is the missing last step.

**Effort.** S — a single page with a form; the action is already complete.

**Risk.** Low. The underlying report generator is the only real complexity and it
already exists.

**Shared vs additive.** Additive (completes an existing commercial workflow).

---

#### 9. Defect → Work Order Raised Email

**What.** When a defect is created or promoted to `in_progress`, send a concise
email to the assigned-to user and (optionally) the customer contact. Template:
defect title, severity, site, asset, link to the portal defect view. Re-uses the
Resend wiring from the supervisor digest.

**Why.** Currently defects are silent — they sit in the list and nothing notifies
anyone. For multi-tech teams (SKS has 6+) this means defects raised on-site by
Technician A are invisible to Supervisor B until someone checks the list. The email
closes the loop.

**Effort.** S — one Resend template + trigger in `createDefectAction` /
`updateDefectAction`. No schema change.

**Risk.** Low. Same dependency as #4 (Resend key).

**Shared vs additive.** Additive.

---

#### 10. Delta WO Import — Live SKS Dry-Run + Duplicate Blocker Validation

**What.** Per `eq/pending.md`: "Delta WO import — live dry-run on SKS tenant with
Aug 2025 file: confirm ~250 rows resolve, MVSWBD fuzzy prompt fires, LBS
unknown-code prompt works, commit succeeds, re-upload triggers duplicate blocker."
This is a validation task (no code if it passes) or a targeted bug-fix sprint if
it reveals issues.

**Why.** The import wizard is the primary data-entry path for SKS's entire Equinix
maintenance portfolio. If the duplicate blocker or fuzzy-match prompts misfire on
a real file, every subsequent import is at risk. This is a correctness gate, not
a feature.

**Effort.** S — run the test. If clean: just a verified config. If not: targeted
fixes to the parser/wizard.

**Risk.** Medium if deferred — import bugs compound as more data accumulates.

**Shared vs additive.** Maintenance of an existing feature.

---

### Group 4 — New CMMS capabilities

---

#### 11. Asset Detail Page

**What.** The Assets page (`/assets`) has a list, grouped view, and form — but no
`/assets/[id]` detail page. Add one: asset metadata, linked maintenance checks
(last 3), linked tests (ACB/NSX/RCD), open defects, attachment list, calibration
history for instruments. The data all exists; no new schema needed.

**Why.** Technicians, supervisors, and customers need an asset-level history view.
Today you can see what happened in a check, but you cannot answer "what is the
full test history for CB-12 at SY4?" without scrolling through the check list.
This is the standard expectation in any CMMS.

**Effort.** M — new route + data joins. All source tables already exist.

**Risk.** Low. Pure read-only aggregation page.

**Shared vs additive.** Additive.

---

#### 12. Inspection / Generic Checklist Module

**What.** Add a `kind='inspection'` to `maintenance_checks` (or a new
`inspection_checks` table following the existing pattern). Surface a simple
configurable checklist: item + yes/no/na + photo + notes. Cover use cases:
pre-energisation safety checks, toolbox-talk sign-on, EWP inspection, ladder
inspection.

**Why.** SKS runs statutory pre-start checks and EWP/ladder inspections that are
currently paper or EQ Field forms. A light checklist module in EQ Service lets
the supervisor link them directly to a maintenance check — so the compliance
artefact (customer report) can include the inspection record without a manual
attachment step.

**Effort.** L — new DB table + kind extension + form + report section.

**Risk.** Medium — adds a new entity type to an already wide schema. Scope
creep risk if feature is under-specified before build.

**Shared vs additive.** Additive (new module).

---

#### 13. Time Tracking on Checks

**What.** Add a per-technician time log to each maintenance check: start time,
end time, technician, activity type (travel / on-site / admin). Surface on the
check detail page (collapsible section, tech-editable). Roll up to a per-customer
actuals panel. Schema: `check_time_entries(check_id, user_id, start_at, end_at, activity_type)`.

**Why.** Labour cost is the dominant variable in an electrical maintenance contract.
SKS currently has no way to compare quoted hours (from EQ Quotes) with actuals
(from EQ Service). Time tracking in Service is the last piece of the
quote-to-close loop. It also feeds the Commercials / Renewal Pack with real
delivery cost data.

**Effort.** M — new table + migrations + form + rollup query + analytics card.

**Risk.** Medium — labour data is sensitive (can expose productivity conversations).
Needs clear role gating (technician can log own time; only admin sees actuals).

**Shared vs additive.** Additive (new module). High integration value with EQ Quotes.

---

#### 14. Bulk Report Export (per-customer, per-FY)

**What.** From the Reports or Analytics page, add a "Download all reports for
[Customer] — [FY]" action. Generates one ZIP containing all completed-check PDFs
for the selected customer and financial year. Uses the existing `report_deliveries`
table and the Storage bucket signed-URL pattern.

**Why.** At end-of-FY, Equinix / Jemena ask for the full compliance evidence pack.
Today Royce manually downloads individual PDFs. A bulk export would collapse this
to one click and is a strong retention/renewal signal ("EQ just made my audit prep
30 minutes instead of 3 hours").

**Effort.** M — zip-on-demand server action, signed-URL fetch for each PDF, stream
response.

**Risk.** Low-medium — ZIP generation from signed URLs at scale requires a careful
timeout/streaming strategy. Netlify Functions have a 10s response limit; needs
background job or chunked approach.

**Shared vs additive.** Additive.

---

#### 15. Customer Portal — Scope Register View

**What.** The customer portal already has Reports + Variations pages. Add a read-only
Scope Register: "Here is everything that's in your contract this FY, and here's
what's excluded." Reads from `contract_scopes` filtered to the customer's tenant +
current FY. Zero write operations from the portal.

**Why.** Transparency builds trust. Scope disputes are the leading cause of variation
friction. A customer who can self-serve their scope register generates fewer "what's
included?" queries and fewer disputed variation invoices. The data already exists.

**Effort.** S — one portal page, read-only query, no schema change.

**Risk.** Low — read-only. The portal auth pattern (magic link session) is already
established.

**Shared vs additive.** Additive (extends existing portal).

---

#### 16. PM Calendar — Recurring Schedule Generator

**What.** The PM calendar (`pm_calendar` table) currently requires entries to be
created one at a time or via the batch check wizard. Add a "Generate recurring
schedule" action: pick a customer, a set of job plans, a financial year, and a
frequency — and the system generates a full FY of calendar entries (e.g. 16 Jemena
sites × 2 annual visits = 32 entries in 2 minutes).

**Why.** Jemena has 16 sites on a 6-monthly cycle — entering 32 calendar entries
manually is a half-day task every FY. The `BatchCreateForm` already creates checks
from a frequency/date preview; extending that logic to create PM calendar entries
(not just checks) is the natural next step.

**Effort.** M — server action + form UI + preview grid. No schema change.

**Risk.** Low. Additive to existing calendar and batch-check patterns.

**Shared vs additive.** Additive.

---

#### 17. Scope-from-Work Derive

**What.** Complete the `/commercials/contract-scopes/derive` route (currently a
dead link in the Commercials hub). Logic: scan all completed maintenance checks for
a customer + FY, aggregate the job plan items covered, and propose a contract scope
for next FY. Supervisor reviews + confirms before writing to `contract_scopes`.

**Why.** This is the "Build Scope from Work" card on the Commercials hub — it's
been designed and linked but not built. For a service company without a pre-existing
scope template (new customer), this turns 12 months of maintenance data into a
first-pass contract scope automatically.

**Effort.** M-L — aggregation query + review UI + confirm-and-write action.

**Risk.** Medium — the derived scope is a commercial suggestion, not ground truth.
Needs clear "this is a suggestion, review before confirming" UX copy and a
supervisor role gate.

**Shared vs additive.** Additive.

---

#### 18. Instrument Calibration Due Reminders

**What.** Extend the notification cron to check `instruments` where
`calibration_due < now() + interval '30 days'` and send the responsible user
a reminder via the bell + email. Add a Calibration Due Soon filter on the
Instruments page.

**Why.** An out-of-calibration test instrument used on-site generates invalid test
results — regulatory exposure for both EQ/SKS and the customer. The instruments
table and calibration_due column exist; the notification cron runs daily. This
closes a compliance gap that costs nothing to fix but could cost significant
rework to remediate after the fact.

**Effort.** S — cron extension + notification call + one filter on the instruments
page.

**Risk.** Low.

**Shared vs additive.** Additive.

---

#### 19. QR Code / Asset Label Generator

**What.** Add a "Print QR labels" button on the Assets page (individual asset and
bulk by site). Each label encodes a URL to `/assets/[id]` (requires #11 above).
Generate a PDF layout sized for 38mm × 25mm labels (standard Dymo / Brother roll).
On scan, a logged-in tech sees the asset detail and can start a check from there.

**Why.** In data-centre environments, assets live behind raised floors and in dense
cabinets — a technician matching a physical breaker to a CMMS record by name is
error-prone. QR labels on assets close this loop. This is a feature that MaintainX
and UpKeep both advertise in their CMMS comparisons.

**Effort.** M — PDF label generator (can reuse the docx/pdf pipeline or a simple
client-side canvas renderer) + route handler.

**Risk.** Low — no schema change. Depends on #11 (asset detail page) for the scan
destination to be useful.

**Shared vs additive.** Additive. Depends on #11.

---

#### 20. Overdue Auto-Escalation

**What.** Extend the `check_overdue` notification to include an escalation path:
after N days overdue (configurable per tenant, default 7), send the
supervisor/admin a summary of all overdue checks grouped by site. Currently the
overdue status is set by status checks in the app layer — no automated push.

**Why.** Without escalation, overdue checks are silent failures. The dashboard shows
a count, but no one receives a push. SKS's SLA with Equinix includes response
commitments; an automated escalation gives supervisors advance warning before a
contractual breach.

**Effort.** M — cron extension + escalation threshold in `tenant_settings` + email
template.

**Risk.** Low. Extends the existing cron pattern.

**Shared vs additive.** Additive.

---

## Summary table

| Rank | Feature | Group | Effort | Value driver |
|------|---------|-------|--------|-------------|
| 1 | Pre-visit Tech Brief — Phase 1 UI + ICS email | Mobile UX | S | Daily driver for every field tech |
| 2 | Site Access Fields — edit UI | Mobile UX | XS | Dependency for #1; zero wasted screen |
| 3 | Defect Detail Page + Photo Attachments | Mobile UX | M | Evidence for customer + portal sharing |
| 4 | Notification Events — complete firing | Workflow | S | Bell/email worthless without call-sites |
| 5 | Analytics — per-customer + per-tech cuts | Reporting | M | Account reviews, performance mgmt |
| 6 | Canonical Export — fill stubs | Reporting | M | Backup completeness + D3 bridge |
| 7 | Field Sync — Admin UI trigger | Workflow | S | Activates built cross-app bridge |
| 8 | Renewal Pack — UI entry point | Workflow | S | Completes built commercial generator |
| 9 | Defect → Work Order email | Workflow | S | Closes silent-defect gap |
| 10 | Delta WO Import — live SKS dry-run | Validation | S | Correctness gate on primary import path |
| 11 | Asset Detail Page | New capability | M | History view; dependency for QR |
| 12 | Inspection / Generic Checklist | New capability | L | Statutory pre-starts in Service |
| 13 | Time Tracking on Checks | New capability | M | Quote-to-actual loop; feeds Quotes |
| 14 | Bulk Report Export (per-customer, FY) | Reporting | M | End-of-FY compliance pack, 1 click |
| 15 | Customer Portal — Scope Register | Portal | S | Scope transparency → fewer disputes |
| 16 | PM Calendar — Recurring Schedule Generator | New capability | M | FY schedule in minutes not hours |
| 17 | Scope-from-Work Derive | Workflow | M-L | New-customer contract scaffolding |
| 18 | Instrument Calibration Reminders | Compliance | S | Regulatory exposure closure |
| 19 | QR Code / Asset Label Generator | New capability | M | Field accuracy; MaintainX parity |
| 20 | Overdue Auto-Escalation | Workflow | M | SLA breach prevention |

---

## Recommended First Batch

**Recommended sequencing for the next sprint (2–3 days of focused work):**

The first batch should be the S-effort items that are dependencies or completions of
already-built surfaces — zero new schema introductions, maximum visible impact for
field users and SKS:

| Priority | Feature | Justification |
|---|---|---|
| 1 | **Site Access Fields — edit UI (#2)** | XS effort, unlocks #1 and is a visible blank on the SiteContextCard today |
| 2 | **Pre-visit Tech Brief — Phase 1 UI + ICS (#1)** | S effort, single biggest daily-driver improvement for field tech workflow |
| 3 | **Notification Events — complete firing (#4)** | S effort, makes the entire notification system functional vs cosmetic |
| 4 | **Renewal Pack — UI entry point (#8)** | S effort, generator already built — purely a missing page |
| 5 | **Field Sync — Admin UI trigger (#7)** | S effort, action already built — purely a missing UI trigger |

All five are S or XS effort. None requires a new DB migration. All close visible
gaps where the infrastructure is built but the last connection is missing. This
batch is deliverable in one focused session without touching auth, the testing
modules, or any SKS-live data.

**After batch 1:** move to M-effort items #3 (defect detail), #5 (analytics cuts),
and #10 (Delta WO dry-run) in the following sprint.

---

## Flagged but paused — PPM Canonical Realignment (Stream E2)

Per the sprint board (`SPRINT-BOARD.md` E2): "PPM canonical realignment — PAUSED.
Canonical PPM model misaligned with SKS ACB/NSX breaker workflow; revisit before
rebuilding any PPM dashboard."

This is a real architectural gap — the `job_plans` + `maintenance_checks` model
was built for PPM checklists, and the ACB/NSX workflow uses it as a container for
a fundamentally different data shape (test workflow steps, not repeatable task
lists). The misalignment means:

- The Kanban board conflates PPM checks and test-bench checks in the same columns
- The `BatchCreateForm` frequency logic doesn't make sense for ACB/NSX
- Any PPM compliance dashboard that aggregates across check kinds will double-count

**Recommendation:** do not build any new PPM dashboard, PPM reporting, or calendar
scheduling features that span both PPM and test kinds until this model decision
is made. Features #16 (PM Calendar generator) and any future PPM compliance KPIs
should be scoped to `kind='maintenance'` only until E2 is resolved.

No action needed now — flag this before any sprint touching the PPM model.

---

*Generated from a read-only audit of eq-solves-service and eq-context. No code,
no git, no edits were made to any file during this analysis.*

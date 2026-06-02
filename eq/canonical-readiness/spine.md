---
title: EQ Canonical — The Trust Spine
owner: Royce Milmlow
last_updated: 2026-06-02
scope: Which canonical app_data tables must be identical/trusted across tenants vs free to vary per tenant
read_priority: critical
status: live
---

# EQ Canonical — The Trust Spine

Derived 2026-06-02 from the live `app_data` schema on **sks-canonical**
(`ehowgjardagevnrluult`), by reference-column analysis.

## Why this doc exists

The roadmap to "ask the system anything and trust the answer" rests on a
**trust ladder**: coherence → surfacing → ask-anything → gating (see memory
`project_eq_north_star_vision`). Rung 0 (coherence) needs a precise answer to
one question: *which tables must mean the same thing in every tenant?* That
set is the **spine**. The full schema ships uniformly to every tenant;
anything a specific business needs beyond the standard lives in extension
columns — we build software around the business via extensions, not by
diverging the shared schema.

The headline: **out of 55 `app_data` tables, only 6 are true cross-app
shared entities.** The "must align" set is small. Tenants are not locked into
a 55-table mould.

## Important substrate fact: no enforced foreign keys

There are **zero enforced FK constraints between `app_data` tables**.
Relationships are by convention (id columns), almost certainly so Intake's
`jsonb_populate_record` loads aren't blocked by FK ordering. Consequence:
integrity is currently guaranteed only by the intake process, not the DB —
nothing physically stops a bad reference today. This is the gap the coherence
rung closes.

## The 6 spine entities

The nouns more than one app joins to (referenced-by count = distinct
`app_data` tables carrying that `*_id`):

| Entity | Referenced by | Role | Rung served |
|---|---|---|---|
| **sites** | 18 | Biggest hub — field, service, quotes, safety | 0 / 1 / 3 |
| **staff** | 10 | Identity for HR, licences, scheduling | 0 / 3 |
| **customers** | 7 | CRM root — contacts, sites, jobs, quotes, tenders | 0 / 1 |
| **assets** | 5 | Service, testing, safety | 0 / 1 |
| **contacts** | 3 | CRM | 0 |
| **licences** | →staff | The compliance gate ("who can work where") | **3** |

## The 3 structural spine columns

Carried by nearly every canonical table — the real backbone:

- **`tenant_id`** (53 tables) — tenancy partition.
- **`intake_id`** (46 tables) — provenance/lineage; the "no silent drops"
  guarantee made physical (every row knows which intake event created it).
- **`external_id`** (17 tables) — crosswalk to source systems (SimPRO etc).

## App-local tables (~49 — shipped uniformly, used where they apply)

NOT spine. Shipped to **every** tenant in the same uniform schema; a tenant
simply doesn't use the clusters that don't apply to it. Per-tenant variation
is the rare exception via extension columns, not divergence of the standard:

- **Quotes:** quote, quote_line_item, quote_attachment, quote_email_outbox, quote_status_history, rate_library, scope_template
- **Tenders:** tenders, tender_enrichments, tender_nominations, tender_review_decisions, tender_import_runs
- **Service:** service_visits, service_task_completions, asset_defects, asset_test_results
- **Field / HR:** timesheets, leave_requests, leave_balances, leave_approval_logs, rotations, schedule_entries, schedule_change_logs, skills_ratings, apprentice_profiles, quarterly_reviews, tafe_calendars, checkins, buddy_checkins, engagement_logs, feedback_entries
- **Safety:** swms, jsa_records, itp_records, prestart_checks, toolbox_talks, site_diaries, incidents, weekly_reports
- **Infra/reports:** gm_report_jobs, gm_report_periods, briefing_actions, briefing_cache, canonical_events, api_intake_calls, tenant_app_configs, _eq_migrations

## Recommended coherence move

Enforce referential integrity on the **6 spine entities only** (one
migration), leave the other ~49 loose. "Thin spine fiercely guarded,
everything else free" as actual DDL. This is the foundation the drift-CI
guard then protects.

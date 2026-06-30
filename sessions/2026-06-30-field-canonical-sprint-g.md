---
title: "2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211"
owner: Royce Milmlow
last_updated: 2026-06-30
read_priority: reference
status: live
---

# 2026-06-30 (part g) — EQ Field canonical sprint: v3.5.207–v3.5.211

## Context

Continuation of the overnight security audit + canonical wiring execution that started earlier this
session (v3.5.199–v3.5.206). Goal: 0 deferred tasks before session close.

## What shipped

### v3.5.207 — Roster/Leave realtime + Teams canonical wire (PR #368)
- `field_teams` / `field_team_members` views created on ehow (INSTEAD OF INSERT/UPDATE/DELETE triggers)
- Realtime: `supabase_realtime` publication populated with `app_data.schedule_entries` + `app_data.leave_requests`
- `realtime.js` channel targets updated to canonical base-table names
- Dead `worker_id` column references cleaned from `app-state.js`

### v3.5.208 — Safety module fully wired (PR #369)
- `public.site_audits` + `public.site_audit_items` created on ehow (never existed despite v3.5.193 changelog claim)
- Authenticated CRUD granted on all 5 safety tables (`prestarts`, `toolbox_talks`, `site_diaries`, `site_audits`, `site_audit_items`)
- JWT_INPLACE routing wired for safety cluster in `supabase.js`
- BEFORE INSERT triggers stamp `tenant_id` on the 3 public.* safety tables

### v3.5.209 — JWT routing gap fix (PR #370)
- Bucket-B tables (`job_numbers`, `regions`, `projects`, `project_targets`) restored to `JWT_TABLES` (v3.5.195 regression)
- `roster_presence` removed from JWT_TABLES (table doesn't exist on ehow)
- `tender_phases` / `nomination_clashes` added to JWT_TABLES
- `GRANT SELECT ON nomination_clashes TO authenticated` applied

### v3.5.210 — Apprentice cluster fully wired (PR #371)
- 7 new `public.*` tables on ehow: `competencies`, `skills_ratings`, `feedback_entries`, `feedback_requests`, `rotations`, `quarterly_reviews`, `apprentice_journal`
- `apprentice_profiles`: org_id NOT NULL default + RLS policy + authenticated CRUD grant
- 6 standard electrical competencies seeded
- 2 direct anon-fetch calls in `apprentices.js` replaced with `sbFetch`

### v3.5.211 — Canonical cleanup (PR #372)
- `public.pending_schedule` created on ehow (Tender Pipeline Push-to-Roster staging table, was missing)
- `app_data.field_schedule/field_timesheets/field_leave_requests`: SECURITY DEFINER → SECURITY INVOKER
  - Root cause: DEFINER views with no role-level grants blocked authenticated role before base-table RLS could evaluate → Roster/Timesheets/Leave silently empty for SKS
- Data tab (`nav-data`, `ditem-data`) gated off for SKS — import/restore would overwrite canonical data
- Dead `worker_id` mirror PATCH removed from `syncAllToCanonical()` in `people.js`
- `roster_presence` removed from `ORG_TABLES` (table never existed on ehow)

## Migrations applied to ehow

- `20260630_field_operational_views_security_invoker.sql` — ALTER VIEW SECURITY INVOKER
- `20260630_pending_schedule_canonical.sql` — CREATE TABLE + RLS + grants

(Teams, Safety, Apprentice tables applied via Supabase MCP in v3.5.207–210 sessions)

## Decisions made

- **Supervisor Notes** → retire for SKS (worker-first; UI already gated v3.5.205)
- **Push-to-Roster** → create `pending_schedule` (vs soft-launch without table)
- **Data tab** → hide entirely for SKS (import/restore risk on live canonical data)
- **AUDIT_SB_KEY** → update to ehow service_role (Royce to do in Netlify UI — OPEN)

## Action required (Royce)

1. **Netlify `eq-solves-field` → set `AUDIT_SB_KEY` to ehow service_role key**
   - Currently anon key → verify-pin audit writes 401 silently → 0 auth event rows in `audit_log`
   - Name stays `AUDIT_SB_KEY`, only the value changes

## Remaining open (not closed this sprint)

- `audit_log`: `verify-pin.js`/`eq-agent.js` still need `org_id` stamped in POST body (separate from the key fix)
- `app_data.staff.user_id` backfill (~61 SKS staff unresolved)
- `field_managers` write path for SKS (INSTEAD OF trigger or retarget needed)
- frame-ancestors tightening (deferred by decision)
- app_config PIN key-scoping (hygiene; PINs gate nothing)

## Production state at close

EQ Field v3.5.211 live on `field.eq.solutions` / `core.eq.solutions/sks/field`.
SKS canonical wiring: all major clusters wired (Roster ✅ · Leave ✅ · Timesheets ✅ · Teams ✅ · Safety ✅ · Apprentices ✅ · Recognitions ✅ · Tender Pipeline ✅ · Resources ✅).
Outstanding: AUDIT_SB_KEY env var (Royce/Netlify).

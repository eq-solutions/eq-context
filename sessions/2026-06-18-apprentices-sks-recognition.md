---
title: "2026-06-18 — Apprentices SKS unlock + Recognition philosophy"
owner: Royce Milmlow
date: 2026-06-18
apps: eq-field
status: closed
---

# Session — 2026-06-18

## What was built

### v3.5.161 — Nav: Safety group + hide PIN Management (PR #303)
- Site Audits, Safety (Prestarts/Toolbox), Safety Report → single collapsible "Safety ▾" group
- Auto-expands for SKS tenant
- PIN Management (`nav-pins`) hidden — orphaned without labour hire login tier

### Acknowledgments on SKS tenant
- `acknowledgments` table applied to ehowgjardagevnrluult
- One-tap peer recognition now live for SKS at core.eq.solutions/sks/field
- Access: Contacts → person profile → eye icon → "Acknowledge [Name]"

### CLAUDE.md architecture fix (PR #302)
- Corrected long-running confusion between sks-nsw-labour standalone and EQ Field SKS tenant
- Added SKS disambiguation block (ehow = EQ Field SKS tenant; nspb = standalone — never touch)
- Canonical-driven tenant resolution documented and verified against live canonical DB

### v3.5.162 — Apprentices: SKS tenant unlock (PR #304)
- 11 DB tables created in ehow: apprentice_profiles, apprentice_journal, skills_ratings,
  competencies, feedback_entries, feedback_requests, rotations, buddy_checkins,
  quarterly_reviews, engagement_log, checkins
- Schema adaptation: person_id/supervisor_id/buddy_id = bigint (SKS people.id = bigint vs EQ uuid)
- 11 standard electrical competencies seeded
- canonical module_entitlements: all 11 apprentice modules → enabled=true for SKS org
- GRANT SELECT/INSERT/UPDATE/DELETE on all tables to anon (migration: grant_apprentice_tables_to_anon)
- Nav: nav-apprentices + ditem-apprentices removed from SKS hide list

### v3.5.163 — Apprentices: fix year level pre-fill (PR #305)
- openSetupProfile() was hardcoding year level '1' before the person lookup
- Fix: reads person.year_level from STATE.people after lookup; one line, correct result

## Decisions made

### Human Recognition Philosophy
- Steelmanned the apprentice feature against the filter question
- Confirmed: journal private by default (per-entry share toggle), feedback apprentice-initiated,
  no streaks/gamification, generous check-in thresholds
- Acknowledged design limit: tool amplifies culture, cannot create it
- Quarterly reviews — table exists in DB but UI not built. Visibility question deferred:
  should the apprentice know who can see their quarterly review before participating?

### Nav simplification
- Safety group collapse: correct — reduces visual noise for SKS daily driver
- PIN Management: hidden (orphaned), not deleted — element remains in DOM

## Outstanding
- Quarterly reviews UI: decide visibility model before building
- Acknowledgments end-to-end smoke test on SKS
- on_roster roster grid filter (carried from 2026-06-15)
- EQ_SECRET_SALT rotation on eq-solves-field

### docs: CLAUDE.md schema correction (PR #308)
- Corrected stale "people.id / managers.id are bigint on SKS" rule
- The canonical adapter views (app_data.field_people / field_managers) expose uuid IDs on the SKS EQ Field tenant
- New rule: all person-referencing columns (person_id, supervisor_id, buddy_id) are uuid on both tenants
- Documents the 2026-06-18 incident: apprentice_profiles created with bigint → 400s on save → fixed by migration fix_apprentice_profiles_uuid_columns

## Versions shipped
| Version | PR | Description |
|---|---|---|
| v3.5.161 | #303 | Nav: Safety group + hide PIN Management |
| v3.5.162 | #304 | Apprentices: SKS tenant unlock |
| v3.5.163 | #305 | Apprentices: fix year level pre-fill on setup |
| docs | #308 | CLAUDE.md: correct schema gotcha — person IDs are uuid on both tenants |

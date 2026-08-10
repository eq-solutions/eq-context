---
title: Apprentices cluster — corrected scope
owner: Royce Milmlow
last_updated: 2026-08-11
scope: Corrects the stale "largest debt, 42 days untouched" framing in eq/pending.md against live-verified reality. Research/scoping only — nothing built from this doc.
read_priority: standard
status: live
---

# Apprentices cluster — corrected scope

**Headline: the debt is much smaller than `pending.md` claimed.** The original
bullet (`eq/pending.md`, added 2026-06-30) described work as still outstanding
that was actually shipped **the same day it was logged** — the overnight
session that wrote the bullet continued into a follow-on sprint that closed
most of it (PR #371, v3.5.210, "Apprentice cluster fully wired"), and the
bullet was never updated to match. Verified live against ehow
(`ehowgjardagevnrluult`), not just the migration file.

---

## What's actually done, verified live

All 8 tables exist on `public.*`, with real data and correct security:

| Table | Rows | RLS | Grants |
|---|---|---|---|
| `apprentice_profiles` | 2 | tenant-scoped read/write policies | authenticated only, no anon |
| `competencies` | 6 (seeded) | ditto | ditto |
| `skills_ratings` | 0 | ditto | ditto |
| `feedback_entries` | 0 | ditto | ditto |
| `feedback_requests` | 0 | ditto | ditto |
| `rotations` | 0 | ditto | ditto |
| `quarterly_reviews` | 0 | ditto | ditto |
| `apprentice_journal` | 0 | ditto | ditto |

Supabase's own security advisor flags **zero issues** on any of the 8. The
actual feature — `eq-field/scripts/apprentices.js`, 2,501 lines — is live in
production on `field.eq.solutions`: profile setup, Skills Passport, structured
supervisor feedback with follow-ups, apprentice-initiated feedback requests,
a private-by-default journal, site rotations, quarterly reviews, batch
year-advancement. Not a stub.

So of the original bullet's five clauses — "missing tables," "grants,"
"org RLS" are done. Two remain.

---

## Resolved, 2026-08-11

1. **`field_*` canonical-twin views — decided: not needed.** Royce's call:
   leave the in-place pattern as-is. Nothing's broken today; the other
   clusters got twinned for fleet-wide consistency, not because this pattern
   failed. Not a gap — a deliberate choice.
2. **2 orphan `apprentice_profiles` rows — deleted.** Verified live before
   deleting: both created 2026-06-18/19 during initial testing
   (`goals_updated_by: 'Royce Milmlow'`), both pointing at
   `person_id = 6b8badf5-38bb-40b0-a20b-3266be052a7f`, confirmed zero matches
   in `app_data.field_people`. Removed via `DELETE ... WHERE id IN (1, 2)`,
   table now empty (0 rows) — clean, no real apprentice affected.

**This item is now fully closed.** Nothing further to track.

**One footgun worth knowing regardless of the answer above:** a second,
unrelated schema already uses the *same table names* under `app_data.*` —
that's EQ Intake's dormant bulk-import target schema, completely different
column shapes, 0 rows, never used for apprentices (SKS's data was entered
live through the UI). Anyone building the twins must mirror the `public.*`
shape, not this dormant one — the name collision is a real trap.

---

## If the twin build is wanted — phased plan

Only Phases 2–3 touch auth/RLS and need Royce's direct review. Everything
else is safe, ordinary work.

| Phase | What | Size | Needs Royce's auth review? |
|---|---|---|---|
| 0 | Close the stale `pending.md` bullet + changelog footer (this doc does that); delete the 2 orphan rows (after a 1-line confirm); remove 3 dead table-name references from `eq-field/scripts/app-state.js` (`buddy_checkins`/`checkins`/`engagement_log` — already unreferenced, zero runtime effect) | Small | No (except the delete confirm) |
| 1 | Decide scope — does the twin build actually happen? | — | **Yes — this is the decision itself** |
| 2 | Build 8 `app_data.field_<name>` views over the 8 `public.*` tables — `SECURITY INVOKER` (not `DEFINER` — the v3.5.211 incident this same sprint was caused by a `DEFINER` view with no role grants silently emptying Roster/Timesheets/Leave), `INSTEAD OF` triggers, RLS mirroring the existing JWT-tenant-claim pattern exactly. Do not reuse the dormant Intake `app_data.*` shape. | Medium | **Yes** |
| 3 | Cut `eq-field/scripts/supabase.js`'s `JWT_INPLACE_TABLES` → `JWT_TABLES` for the 8 apprentice tables; verify `Content-Profile`/`Accept-Profile: app_data` routing; smoke-test against the 2 live profiles before/after, on a flag or off-hours | Small–Medium | **Yes** |
| 4 | Verification pass — re-run `tests/apprentices-rules.test.js`, click through the live 11-apprentice roster post-cutover | Small | No |
| 5 | Retire the now-redundant `public.*` grants/RLS once the twin path is confirmed stable, or leave both live for one release as a fallback (matches how Tender Pipeline currently does this) | Small | No |

**Overall: Medium effort if the twin build is wanted, not the "Large,
dedicated session" the stale note implied** — the actual hard, risky work
(table creation, grants, RLS, the live feature itself) is already done.

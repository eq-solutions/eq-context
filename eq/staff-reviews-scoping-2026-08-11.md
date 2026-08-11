---
title: Staff resource management (reviews, skills, progress) — scoping
owner: Royce Milmlow
last_updated: 2026-08-11
scope: Audit + design for a manager-only staff review/skills feature in EQ Field, requested by Royce as Operations Manager. Scoping only — no migration applied, no code written yet.
read_priority: high
status: draft
---

# Staff resource management — scoping

Royce (as NSW Operations Manager, not in his EQ-founder capacity) asked to audit what's
already there for tracking staff reviews, progress, and skills/weaknesses, "for my eyes
only to start with." Live-verified against both production databases before designing
anything, per this repo's own Rule 0.5 — the first draft of this doc was wrong in one
important way (see "Corrected finding" below) and got fixed before Royce acted on it.

---

## What's actually live today

EQ Field already ships a complete, working review/skills subsystem — **`scripts/apprentices.js`**
(2,500 lines) — but it's scoped to apprentices only. The tables (`public.` schema on both
ehow/sks-canonical and eq-canonical-internal):

| Table | What it holds |
|---|---|
| `competencies` | a generic skill catalog (6 seeded, e.g. "Safety Awareness") |
| `skills_ratings` | person × competency × 1-5 rating × period × rater type (self/tradesman) |
| `quarterly_reviews` | structured periodic review: improved / plateauing / off-track, focus areas, actions, notes |
| `feedback_entries` | ad hoc feedback: did-well / needs-improve / trust-next / follow-up, with resolution tracking |
| `apprentice_profiles` | apprentice-only extras: year level, goals, buddy/supervisor links |
| `rotations`, `buddy_checkins`, `engagement_log` | placement history, check-ins |

Permission keys for exactly this (`app.view_skills`, `app.edit_skills`, `app.quarterly_review`,
`app.manage_rotations`) are already declared in `permission-matrix.js` — just never wired to
anything beyond the coarse "is a manager" check.

### Corrected finding — this has never actually been used

The first pass of this audit (based on reading the code and migration files) described this
as "a complete, live, working implementation." **That's true of the code, false of the
usage.** Direct live query against both `ehow` and `eq-canonical-internal`: every one of
`skills_ratings`, `quarterly_reviews`, `feedback_entries`, `apprentice_profiles` has **zero
rows, on both databases.** The audit log confirms zero write events, ever, on any of them.
Only the 6-item competency list was ever seeded. Royce confirmed the reason: no bug, no
rollout failure — apprentices genuinely haven't had a review cycle yet.

**This is good news for risk, not bad news for the plan.** There's no real review history to
protect during a migration — this is closer to a fresh build reusing a proven table shape
than a risky live-data change.

### The other wrinkle: duplicate schemas

Every one of these tables exists **twice** — once under `public.*` (what the live app
actually reads/writes) and once under `app_data.*` (a separate, apparently-unused
canonicalisation mirror that eq-shell's own docs list as "Field alone builds against" with
zero UI usage anywhere in Shell). Confirmed which copy is real by tracing `sbFetch()`'s
routing logic in `eq-field/scripts/supabase.js`: these table names aren't in `JWT_TABLES`,
so they never route through the `app_data` JWT path — they hit `public.*` directly. **Any
new work targets `public.*`.** The `app_data.*` copies are dead weight; left alone here, not
this doc's problem to clean up.

---

## The design this points to

`apprentice_profiles` already has a `person_id` (uuid) column pointing straight at the real
staff table — confirmed by tracing `apprentices.js`'s own code (`person_id === person.id`
against `STATE.people`, which resolves through `app_data.field_people`, a view that is a
straight `SELECT staff_id AS id, ... FROM app_data.staff`). And `quarterly_reviews.apprentice_id`
is already typed `uuid` — it can't correctly reference `apprentice_profiles.id` (which is
`bigint`), so it was arguably always meant to be person-keyed, not apprentice-keyed.

**The generalization is smaller than it looks:** add a real `person_id` to the two
`bigint`-keyed tables, point everything at `app_data.staff.staff_id` (the canonical,
Shell-owned staff table — this suite's established rule: staff data lives in `app_data.*`,
Field reads/writes it, never rebuilt elsewhere). `apprentice_profiles` stays exactly as-is,
apprentice-specific, no longer a required stepping-stone for a review to exist.

### Draft migration (not applied — for review)

```sql
-- skills_ratings: currently keyed to apprentice_profiles.id (bigint). Add a real
-- person-scoped key so a rating can exist for any staff member.
ALTER TABLE public.skills_ratings
  ADD COLUMN person_id uuid REFERENCES app_data.staff(staff_id);

-- feedback_entries: same shape, same fix.
ALTER TABLE public.feedback_entries
  ADD COLUMN person_id uuid REFERENCES app_data.staff(staff_id);

-- quarterly_reviews: apprentice_id is already uuid-shaped correctly — just give it
-- the real FK now that the target is confirmed, and rename for clarity since nothing
-- depends on the old name yet (zero rows).
ALTER TABLE public.quarterly_reviews
  RENAME COLUMN apprentice_id TO person_id;
ALTER TABLE public.quarterly_reviews
  ADD CONSTRAINT quarterly_reviews_person_id_fkey
  FOREIGN KEY (person_id) REFERENCES app_data.staff(staff_id);
```

`apprentice_id` stays on `skills_ratings`/`feedback_entries` untouched (nullable, apprentice
flows keep working exactly as coded) — `person_id` is additive, not a replacement, so
`apprentices.js` needs zero changes to keep functioning. A new all-staff screen would write
`person_id` only; the two columns simply serve different callers.

**Not yet confirmed:** which pipeline actually applies eq-field migrations live (eq-shell's
schema changes go through the governed `tenant-migrate.yml` One Pipe — need to confirm
whether eq-field uses the same mechanism or its own, before this can actually be applied).
Flagged as an open item for the build step, not a blocker on this scoping doc.

### Access — "for my eyes only to start with"

Direct precedent already exists: `field.manage_pipeline` and `field.view_all_crews` are
both manager-only by Royce's own explicit past request (`permission-matrix.js`). Same
pattern: one new key (e.g. `field.manage_staff_reviews`), gated further to just Royce's own
account for phase one (an explicit email/user-id check layered on top of the permission
check, same shape Shell uses for `is_platform_admin`-plus-email on its own admin routes) —
widen to `manager` generally later if it proves useful.

### UI — new screen, not a rename of the apprentice one

Apprentices have fields (year level, TAFE day, RTO) that don't apply to a supervisor or a
site foreman. Cleanest path: a new "Staff Reviews" screen using `apprentices.js`'s UI
*pattern* as a template — competency ratings, a quarterly-review form, ad hoc feedback log,
a trend view (rating-over-time per competency, which `apprentices.js` already computes for
apprentices via `avgRating()`) — pointed at the full staff list (`app_data.field_people`,
66 people today) instead of the apprentice-only subset. Not a copy-paste of the existing
file; a generalized sibling.

---

## What this doc is not

No migration has been applied. No code has been written. This is the scoping pass Royce
asked for before deciding whether to build — the next step, if he confirms, is a real PR
(migration + permission key + screen) on its own branch, held for explicit review the same
way every other change this session has been.

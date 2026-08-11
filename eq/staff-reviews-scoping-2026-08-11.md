---
title: Staff resource management (reviews, skills, progress) — scoping
owner: Royce Milmlow
last_updated: 2026-08-11
scope: Audit, design, build, and live migration for a manager-only staff review/skills feature in EQ Field, requested by Royce as Operations Manager. Built and merged (eq-field #677/#678/#679); migration applied live 2026-08-11. Screen click-through is the only remaining open step.
read_priority: high
status: live
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

## Built — 2026-08-11, same day, held for review

Royce confirmed the direction via `/decide` (both pre-build checks — eq-field's migration
pipeline, RLS/triggers on the 4 tables — came back clean, see below). Built same session:
[eq-field PR #677](https://github.com/eq-solutions/eq-field/pull/677) (draft) —
`scripts/staff-reviews.js`, the `STAFF_REVIEWS_ALLOWLIST` pilot gate (reused
`PILOT_SIGN_ALLOWLIST`'s exact email, not a new one — see that pattern's own "don't gate on
royce@eq.solutions" caveat), and the draft migration SQL.

**One design change from the plan above:** the original idea was a new `field.manage_*`
permission key. Live investigation found a closer, already-proven precedent —
`PILOT_SIGN_ALLOWLIST` (`index.html`) already does exactly "visible to one person," three
layers deep (nav-hiding, `showPage()` direct-nav refusal, render-time self-check). Reused
that mechanism directly rather than inventing a permission-matrix key for a single-person
pilot — cheaper, and it's the codebase's own established answer to this exact question.

**Pre-build checks, resolved:**
- eq-field has no governed migration-apply pipeline (unlike eq-shell/eq-service) — every
  migration is hand-applied via the Supabase MCP `apply_migration` tool, then committed to
  the repo as a record afterward, per this repo's own `CLAUDE.md`. Confirmed via full
  `.github/workflows/` sweep (8 workflows, none touch Supabase/SQL) and `git log` on the
  existing migration files' own headers.
- All 5 tables (`skills_ratings`, `quarterly_reviews`, `feedback_entries`,
  `apprentice_profiles`, `competencies`) have RLS enabled, 2 policies each, **zero
  triggers** — nothing hidden that an `ALTER TABLE` could disturb.

**Real drift caught mid-build, not assumed away:** the live eq-field root checkout was 17
commits behind main, including one that decomposed `apprentices.js` (2,500 → 1,931 lines,
feedback/rating modals moved to `apprentices-reviews-rotations.js`) and one that mandates
worktree isolation for exactly this reason. Re-verified the current file layout before
writing anything — the earlier "UI pattern" citations above were already stale by the time
of the build. Also found `scripts/build-bundles.mjs`'s drift guard fires on any
`lazy-loader.js` edit (a hand-merged `core-bundle-b1.js` needs regenerating in lockstep) —
caught and fixed before commit, not left for CI to catch.

Code verification: 26/26 existing tests pass, 0 eslint errors/warnings, syntax-checked
including the exact inline `<script>` block in `index.html`, PR CI green. **Checked against
the real Netlify deploy preview** (not just the sandbox, which can't boot the app at all) —
app boots clean, zero console errors, `nav-staff-reviews` correctly renders `display:none`
for a non-allowlisted session, gate fails closed exactly as designed.

**PR #677 merged and deployed live** — real production check on `field.eq.solutions` after
merge: `APP_VERSION` reads `3.5.483`, zero console errors, gate still correctly hidden for
the unauthenticated session that checked it.

## Migration — applied live, 2026-08-11, after one real bug caught first

Royce asked directly to apply the migration same session ("can you do it now"). Before
running anything, re-verified the design one more time and found a real problem in the
original plan: `quarterly_reviews`'s column was going to be **renamed** (`apprentice_id` →
`person_id`), reasoning it was "just a correction" since the column was already
`uuid`-typed. That reasoning was incomplete — `apprentices-reviews-rotations.js`'s
`saveQuarterlyReview()` still builds its insert as `{ apprentice_id: profile.person_id, ... }`
and POSTs it. A rename would have silently broken every future real apprentice
quarterly-review save until that file was also updated — caught before this was ever run
against a live database, not after. Fixed to **ADD** `person_id` instead
([eq-field PR #678](https://github.com/eq-solutions/eq-field/pull/678)), matching the other
two tables exactly. `apprentice_id` stays untouched everywhere.

Applying it live surfaced one more real asymmetry, also caught before it caused a problem:
`public.quarterly_reviews` **doesn't exist on `zaap` (eq-canonical-internal) at all** — only
on `ehow`. `apprentices.js`'s own fetch for that table already wraps the call in
`.catch(() => [])` for exactly this reason — a pre-existing gap on the `eq` tenant, not
introduced by this change, not expanded here.

**Final applied state, live-verified after:**
| Database | skills_ratings | feedback_entries | quarterly_reviews |
|---|---|---|---|
| ehow (sks-canonical) | ✅ person_id added | ✅ person_id added | ✅ person_id added |
| zaap (eq-canonical-internal) | ✅ person_id added | ✅ person_id added | — table doesn't exist |

Every `apprentice_id` column confirmed untouched on both databases after applying. The
screen's own save flow still needs a real allowlisted click-through (Royce's own next step)
— that part genuinely can't be verified from here.

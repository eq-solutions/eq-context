---
title: Worker Identity Linker — Spec
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Spec for linking canonical workers to auth.users — 2026-06-07
read_priority: reference
status: archived
---

# Worker Identity Linker — Spec
*2026-06-07 · Status: APPROVED FOR BUILD*

---

## Diagnosis

### What exists in jvkn (ground truth, verified today)

| Table | Rows | State |
|---|---|---|
| `public.workers` | 37 | Pre-populated from Workbench migration — names, emails, phones, roles all correct. **35 have no `user_id`** — orphaned from auth. |
| `public.worker_credentials` | unknown | The Cards unverified-ticket staging table. Worker enters ticket → sits here until promoted. |
| `public.licences` | unknown | Verified/promoted tickets. `user_id` soft-ref to shell_control.users.id. **Nothing pre-seeded.** |
| `public.worker_invites` | unknown | **Cards-side** invite. Has `profile_data` JSONB + `licences_data` JSONB + `worker_id`. The pre-population mechanism. Currently unused for SKS. |
| `shell_control.user_invites` | ~46 | **Shell-side** invite. Gives PIN access + entitlements. Created by migrate page. No reference to `workers.id`. |
| `shell_control.users` | 5 managers, 0 workers | Auth records. Workers haven't claimed invites yet. |

### The two parallel invite flows

```
Path A — Shell (access):
  migrate page → shell_control.user_invites → accept-invite → shell_control.users
  Result: worker can log in, set PIN, see tiles. Profile is blank. Cards is empty.

Path B — Cards (profile):
  public.worker_invites (profile_data, licences_data) → ClaimInviteScreen → workers.user_id set
  Result: Cards pre-populated with name, trade, licence placeholders.
  Status: NEVER TRIGGERED for SKS workers.
```

These two paths don't intersect. A worker who completes Path A gets Shell access but an empty Cards. Path B has never been kicked off for anyone.

### What's right about the architecture

- ✅ `workers` is a global portable identity — no tenant_id. Tradies move between employers, their credentials travel with them.
- ✅ `worker_credentials` → `licences` promotion pipeline — staged verification is correct.
- ✅ `public.worker_invites.profile_data` JSONB — the right mechanism for pre-population, already built.
- ✅ Shell as control plane, canonical jvkn as single source of truth.
- ✅ 37 workers already populated with correct real-world data. We don't need to re-enter anything.

### What's broken or missing

1. ❌ `shell_control.user_invites` has no `worker_id` column — Shell invite doesn't reference the canonical worker.
2. ❌ `accept-invite.ts` doesn't set `workers.user_id` after creating the shell user.
3. ❌ No `public.worker_invites` records created for SKS — the profile pre-population mechanism is wired but never fired.
4. ❌ `workers` has no `staff_id` column — no hard link to `ehowg.app_data.staff` for Field SSO.
5. ❌ 35 of 37 workers are orphaned — `user_id = null` even though their shell invites exist or are ready.
6. ❌ Simon Bramall's invite was created directly in `shell_control.user_invites` but no corresponding `public.worker_invites` was created — he'll land with access but empty Cards.

### The transfer of info — correct answer

```
Workbench → app_data.staff (ehowg)          [operational Field record: roster, timesheets]
          → public.workers (jvkn)            [canonical identity: already seeded from migration]
          → public.worker_invites (jvkn)     [pre-population payload: profile_data + licences_data JSONB]

Invite flow (unified):
  Migrate page generates BOTH:
    shell_control.user_invites (worker_id → workers.id)
    public.worker_invites     (worker_id, profile_data from workers+staff, licences_data)

  One claim link sent → worker opens → accept-invite → sets PIN → shell user created
    → workers.user_id set (link established)
    → worker_invites claimed → Cards pre-populated on first open
```

The data is already there. The pipeline to deliver it isn't.

---

## Schema additions (Phase 1 — migrations)

### M1: Add `worker_id` to `shell_control.user_invites`

```sql
ALTER TABLE shell_control.user_invites 
  ADD COLUMN worker_id uuid REFERENCES public.workers(id) ON DELETE SET NULL;
```

### M2: Add FK constraint to `workers.user_id`

Currently `workers.user_id` is a soft reference — no FK. Link it properly:

```sql
ALTER TABLE public.workers
  ADD CONSTRAINT workers_user_id_fkey 
  FOREIGN KEY (user_id) REFERENCES shell_control.users(id) ON DELETE SET NULL;
```

### M3: Add `staff_id` to `workers` (for Field SSO)

No FK (cross-DB, ehowg ↔ jvkn can't enforce at DB level — soft ref is correct):

```sql
ALTER TABLE public.workers
  ADD COLUMN staff_id uuid;  -- soft ref to ehowg.app_data.staff.staff_id

CREATE INDEX workers_staff_id_idx ON public.workers(staff_id);
```

---

## Migrate page changes (Phase 2)

When generating invites, the migrate page (`/sks/admin/users/migrate`) currently:
- Reads `app_data.staff` (ehowg)
- Creates `shell_control.user_invites` (jvkn)

It should additionally:
1. **Look up** matching `public.workers` record by email (already exists for all 35 ready workers)
2. **Set** `user_invites.worker_id = workers.id`
3. **Create** `public.worker_invites` for each worker with:
   - `worker_id` → the matched workers.id
   - `org_id` → SKS org id
   - `profile_data` JSONB from `workers` record (first_name, last_name, phone, email, role)
   - `licences_data` JSONB from `app_data.staff` (trade, level, employment_type — seeded as "confirm these" placeholders)
   - `expires_at` → same 14 days as shell invite
4. **Embed both tokens** in a single claim URL (or link them so one claim triggers both)

### Role selector

Add a `role` dropdown per row on the migrate page (employee / supervisor / manager) before sending. Defaults to the employment_type mapping but editable. Writes to both `user_invites.role` and `workers.role`.

### Status column

Show per-worker status: Invited / Claimed / No email / Already has account. Derived from:
- `shell_control.user_invites.accepted_at IS NOT NULL` → Claimed
- `shell_control.users` matching by email → Already has account
- `email IS NULL` → No email

---

## accept-invite.ts changes (Phase 3)

After the shell user is created and the session is established:

```typescript
// If the invite has a worker_id, link the canonical worker to the new shell user
if (invite.worker_id) {
  await sb.from('workers')
    .update({ user_id: newShellUser.id })
    .eq('id', invite.worker_id);

  // Also claim the corresponding worker_invite if one exists
  const { data: workerInvite } = await sb
    .from('worker_invites')
    .select('id, profile_data, licences_data')
    .eq('worker_id', invite.worker_id)
    .is('claimed_at', null)
    .single();

  if (workerInvite) {
    await sb.from('worker_invites')
      .update({ claimed_at: new Date().toISOString(), claimed_by: newShellUser.id })
      .eq('id', workerInvite.id);
    // profile_data and licences_data are now readable by Cards on first open
  }
}
```

---

## Cards first-open experience (Phase 4)

When a worker opens Cards after claiming their Shell invite, Cards should:

1. Call `GET /workers/me` (or read from jvkn directly) → `workers` record where `user_id = auth.uid()`
2. If `workers` record exists with name/phone pre-populated → show "Welcome [first_name]. We've pre-filled what we know — confirm your details."
3. If corresponding `worker_invites` record has `licences_data` → seed licence placeholders with status `pending_confirmation`

This replaces the blank onboarding with a confirm-your-details flow.

---

## Backfill plan (Phase 5 — run once, safe to re-run)

For the 35 existing orphaned workers:

```sql
-- Link workers.user_id for any shell users that already exist (by email match)
UPDATE public.workers w
SET user_id = u.id
FROM shell_control.users u
WHERE u.email = w.email
  AND w.user_id IS NULL
  AND u.tenant_id = '7dee117c-98bd-4d39-af8c-2c81d02a1e85'; -- SKS

-- Set staff_id from ehowg (cross-DB — run as two separate queries, match by email)
-- Step 1: get email→staff_id map from ehowg (run against ehowgjardagevnrluult)
-- Step 2: update workers.staff_id in jvkn
-- (Can't do in one query — cross-DB. Script handles this.)
```

---

## UI improvements (alongside Phase 2)

### accept-invite page
- Fix footer leaking route name ("accept-invite") → show "© EQ Solutions 2026" only
- "An account with this email already exists" → add a "Sign in instead →" button that routes to `/{tenant}/login`
- Apply the same card layout as the PIN setup screen (already styled)

### admin/users — delete/archive
- Add kebab menu per user row: Archive (soft-delete, sets `active = false` on shell_control.users) and Remove invite (deletes unclaimed invite)
- Gate on `admin.manage_users` permission
- Archived users can't log in but their data is preserved. Show in a collapsed "Archived" section.

---

## Simon Bramall — immediate fix

His shell invite exists but no `worker_invites` record was created. Do now:

```sql
-- Get Simon's workers.id and create a worker_invites record
INSERT INTO public.worker_invites (id, org_id, token, profile_data, worker_id, expires_at)
SELECT 
  gen_random_uuid(),
  '{{sks_org_id}}',  -- the SKS org id from organisations table
  gen_random_uuid(),
  jsonb_build_object(
    'first_name', w.first_name, 'last_name', w.last_name,
    'phone', w.phone, 'email', w.email, 'role', w.role
  ),
  w.id,
  now() + interval '14 days'
FROM public.workers w
WHERE w.email = 'simon.bramall@sks.com.au';

-- Also patch his shell invite to include worker_id (once M1 migration runs)
```

---

## What NOT to build

- ❌ Don't try to hard-link ehowg ↔ jvkn at the DB level — cross-DB FKs don't work in Supabase. Soft refs (staff_id as uuid, no constraint) are correct.
- ❌ Don't merge the two invite tables into one — they serve different purposes. Shell invite = access credentials. Worker invite = profile payload. Keep them separate, link them.
- ❌ Don't pre-seed licences from trade data yet — trades workers have many licences we don't know about. Seed the profile (name, role, trade) but let them enter/scan their own licences. The `licences_data` JSONB can carry "we know you're an electrician — add your electrical licence" as a prompt, not a pre-created record.
- ❌ Don't build this as a batch script — the invite flow is the right trigger point. Backfill only for the 35 already-orphaned workers.

---

## Build order

| Step | What | File(s) | Gate |
|---|---|---|---|
| 1 | M1 + M2 + M3 migrations | Supabase MCP apply | Non-breaking, additive |
| 2 | accept-invite: set workers.user_id + claim worker_invite | eq-shell | No deploy needed until merged |
| 3 | Migrate page: lookup worker_id + create worker_invites + role selector | eq-shell | Same PR as step 2 |
| 4 | Backfill script: link existing 35 workers | SQL via MCP | After step 1 |
| 5 | accept-invite UI polish + admin archive | eq-shell | Same PR |
| 6 | Cards first-open profile confirm | eq-cards | Separate PR |

Steps 1–5 ship as one eq-shell PR. Step 6 is a Cards PR after.

---

## Success criteria

- [ ] Worker accepts Shell invite → `workers.user_id` is set immediately
- [ ] Cards opened after claim → worker sees their name pre-filled, not a blank form
- [ ] Migrate page shows role selector + live status per worker
- [ ] Archived workers can't log in; their data is intact
- [ ] Simon Bramall can accept his existing invite and land with pre-populated profile
- [ ] `workers.staff_id` populated for all 37 workers (enables Field SSO arc later)

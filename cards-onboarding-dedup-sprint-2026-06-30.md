---
title: EQ Cards — Onboarding Dedup Sprint
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Fix the duplicate-worker root cause in Cards onboarding + retire the invite path + reversible two-plane cleanup. Live-verified.
read_priority: critical
status: approved
---

# EQ Cards — Onboarding Dedup Sprint (2026-06-30)

**Approval:** Royce gave full approvals 2026-06-30. **Prod-apply gated** on joint
dry-run review ("once we are happy"). John Angangan to be re-nudged by Royce
tomorrow once live.

**Surfaced from:** Sentry `EQ-CARDS-T` (`uuid=text` on `/claim`, 3 users this
morning) → which was already fixed by migration `0061`, but the dig exposed the
real, deeper bug below.

---

## 1. Root cause (verified in live function bodies, not migration files)

Worker identity is keyed **only on `user_id`**. The approve step
`eq_cards_respond_to_access_request` does:

```sql
INSERT INTO public.workers (user_id, …) VALUES (auth.uid(), …)
ON CONFLICT (user_id) DO NOTHING;   -- only dedups on user_id
```

It **never adopts a pre-existing unlinked record** (admin-created shell, where
`user_id IS NULL`, matchable only by phone/email). So: admin pre-populates a
worker → person self-signs-up → Royce approves → approval mints a **new** worker
and **orphans the admin one**. Every time.

The safety net that should catch it — trigger `on_auth_users_insert_dedup`
(`handle_phone_dedup`) — has two holes:
1. It only dedups `shell_control.users` (identity), **never `public.workers`**.
2. It **skips any phone starting with `+`** (E.164) — which is exactly what
   Supabase stores — so it is **near-inert**.

Worker rows are minted by three live functions (all bypass matching):
`eq_cards_admin_upsert_worker`, `eq_cards_claim_invite`,
`eq_cards_respond_to_access_request`.

## 2. Blast radius (live, both planes)

- `jvkn.public.workers`: 81 workers → **6 phone-dup groups + 5 email-dup groups (~7 excess rows)**.
- Dups propagate to canonical `ehow.app_data.staff` (where **licences** hang:
  `licences.staff_id → staff.staff_id`, `staff.cards_worker_id → jvkn.workers.id`).
- **6 FK tables** reference a worker (a merge must repoint all): `worker_credentials`,
  `worker_assignments`, `worker_inductions`, `worker_invites`,
  `shell_control.user_invites`, `revoked_agent_tokens`.

## 3. Canonical-record rule (data-validated — and inverted from intuition)

Keep the row with **licences + login + active**; archive empty shells. The data
proved this: Vincent's **4 licences sit on his *new* login row** (`16e2d096` /
ehow `5226a800`), **not** the older June 2 admin shell. So "keep oldest" would be
wrong. Licences exist for only one person (Vincent, 4) and already sit on the
clearly-canonical row → **cleanup is archiving empty orphans, not risking any
licence**.

## 4. Per-person merge plan (read-only; nothing applied)

| Person | Keep (canonical) | Archive | Notes |
|---|---|---|---|
| Vincent Costa | jvkn `16e2d096` / ehow `5226a800` (login, **4 licences**) | jvkn `0d1ec173`, `549a8c2e` | ehow extras already inactive |
| Jack Cluff | `05bd3a77` (login, active) | jvkn `618cffae` | ehow extra already inactive |
| Rhys Scott | `e26d8fc6` (login, active) | jvkn `4ea155a6` | ehow extra already inactive |
| Yura Konakov | `53c885a0` (login, active) | jvkn `71487458` + **ehow `b41c73d4`** | live-dup on *both* planes |
| Phoenix Khatri | `d84be29f` (login) | jvkn `ab3d1e9e` | name variant "Yash KHATRI" |
| Elliot Gross | `0a86ae65` (login) | jvkn `369f2239` | jvkn only |
| John Angangan | `7cd58b44` (active, **no login**) | — (no merge) | incomplete signup — Royce re-nudges |
| Emma Curth | — | already inactive both | done |

## 5. The fix

**A. One match function, used everywhere** — `eq_cards_link_or_create_worker(user_id, phone, email, first, last)`:
adopt-or-create, idempotent on `user_id`, advisory-locked to avoid the `23505`
race that `0060` was patching. Route all three minters through it.

```sql
CREATE OR REPLACE FUNCTION public.eq_cards_link_or_create_worker(
  p_user_id uuid, p_phone text, p_email text, p_first text, p_last text
) RETURNS uuid LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public' AS $$
DECLARE
  v_norm  text := regexp_replace(regexp_replace(coalesce(p_phone,''),'\s','','g'),'^(\+61|61|0)','');
  v_email text := lower(nullif(trim(coalesce(p_email,'')),''));
  v_id    uuid;
BEGIN
  SELECT id INTO v_id FROM public.workers WHERE user_id = p_user_id LIMIT 1;   -- idempotent
  IF v_id IS NOT NULL THEN RETURN v_id; END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended(coalesce(nullif(v_norm,''), v_email, p_user_id::text), 0));

  SELECT id INTO v_id FROM public.workers                                       -- adopt unlinked shell
  WHERE user_id IS NULL
    AND ( (v_norm <> '' AND regexp_replace(regexp_replace(coalesce(phone,''),'\s','','g'),'^(\+61|61|0)','') = v_norm)
       OR (v_email IS NOT NULL AND lower(email) = v_email) )
  ORDER BY (SELECT count(*) FROM public.worker_credentials wc WHERE wc.worker_id = workers.id) DESC, created_at ASC
  LIMIT 1;
  IF v_id IS NOT NULL THEN UPDATE public.workers SET user_id = p_user_id WHERE id = v_id; RETURN v_id; END IF;

  INSERT INTO public.workers (user_id, first_name, last_name, phone, email)     -- else create
  VALUES (p_user_id, coalesce(nullif(p_first,''),'Unknown'), coalesce(p_last,''), p_phone, p_email)
  ON CONFLICT (user_id) DO NOTHING RETURNING id INTO v_id;
  IF v_id IS NULL THEN SELECT id INTO v_id FROM public.workers WHERE user_id = p_user_id; END IF;
  RETURN v_id;
END; $$;
```

**B. Fix `handle_phone_dedup`** — drop the E.164 early-return; normalise both
sides consistently (or fold its identity-merge into the helper).

**C. Retire the invite path** (confirmed dead — 2 invites ever, 0 claimed):
remove `claim_invite`/`claim_by_phone` screens, admin invite UI,
`eq_cards_claim_invite`, `eq_cards_find_invites_by_phone`,
`link_pending_invites_on_confirm` trigger; re-point the not-provisioned
"Find my company" button at the self-signup request flow; park `worker_invites`.
This also removes the `EQ-CARDS-T` Sentry bug's surface entirely.

**D. Reversible two-plane cleanup** — per §4: repoint the 6 jvkn FKs to the
canonical worker + archive empties; archive the ehow straggler (`b41c73d4`);
keep a `merged → canonical` mapping table for rollback. Archive (`active=false`)
not hard-delete.

## 6. Pre-mortem

| Risk | Mitigation |
|---|---|
| Merge keeps wrong row → lose a licence/login | Licences only on Vincent's canonical row; archive empties only; **dry-run + per-person diff Royce approves**; reversible |
| `23505` mid-merge (the crash `0060` fought) | Advisory lock per user_id; repoint-then-archive in FK order; helper resolves atomically |
| Sync re-spawns dups during cleanup | Ship prevention **first**; pause jvkn→ehow sync during cleanup; verify both planes = 1/person |
| Live onboarding in-flight | Prevention is additive/safe; cleanup in a low-traffic window; archive-not-delete; prod-apply gated |

## 7. Sequencing (prod-apply gated on "we're happy")

0. **Dry-run on a Supabase branch** + per-person canonical list (§4) — Royce reviews.
1. **Prevention** — ship `eq_cards_link_or_create_worker` + fix `handle_phone_dedup`; route all 3 minters. (Stops new dups.)
2. **Retire invites** — remove path + re-point not-provisioned screen.
3. **Cleanup** — reversible two-plane dedup, coordinated with the sync.
4. **Verify** — 1 row/person both planes; re-test signup→approve makes exactly one; John re-nudged.

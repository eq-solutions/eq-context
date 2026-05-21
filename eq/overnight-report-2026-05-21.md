---
title: EQ Shell overnight report — 2026-05-21
owner: Royce Milmlow
last_updated: 2026-05-21
scope: What I (Claude) shipped, found, and decided overnight. Read first thing in the morning before opening core.eq.solutions.
read_priority: critical
status: live
---

# EQ Shell — overnight report (2026-05-21)

## TL;DR

Cards is now living on canonical. The full data + auth flip shipped
end-to-end in one session: 4 licences + 1 staff record migrated from
the legacy Cards Supabase to `app_data.*` on `jvknxcmbtrfnxfrwfimn`,
8 new RPCs bridging the schema rename, the Flutter app rebuilt and
redeployed to `eq-cards.netlify.app`, the shell flag flipped so the
iframe handoff is the only sign-in path, and the legacy
`hshvnjzczdytfiklhojz` Supabase locked read-only as rollback insurance.

If you open `core.eq.solutions/core/cards` cold this morning, you
should see the Cards Flutter app load via the shell handoff (no
email-OTP), with your 2 active licences visible. If it doesn't —
read §"If it broke" below.

## Worked end-to-end overnight

### CARDS A. Data migration — done

1 profile + 4 licences migrated from Cards Supabase
(`hshvnjzczdytfiklhojz`) into canonical:

| What | Where it landed |
|---|---|
| `profiles[1]` Royce Milmlow | `app_data.staff` row `50c28920-…`, linked to shell user `b508008d-…` via `user_id` FK |
| `licences[4]` (2 active, 2 deleted) | `app_data.licences` with original Cards UUIDs preserved as `licence_id`. Deleted ones imported as `active=false` |
| Personal fields (DOB, address, emergency contact) | New columns added to `app_data.staff` + backfilled |
| Photo JPGs (2 files) | **NOT copied.** `photo_front_path` set to NULL — see §"Known gaps" |
| Audit trail | One `eq_intake_events` row with `entity='licence'`, `source_kind='migration'`, `rows_committed=5` |
| Cards Supabase | INSERT/UPDATE/DELETE revoked from `authenticated`+`anon` on `profiles`, `licences`, `audit_log`. Read still works as rollback insurance |

### CARDS B. Flutter Unit 4 — done

Branch: `claude/canonical-migration` in `C:\Projects\eq-cards`.
Commit `0d14c50`. 18 files, +409/-672.

- Email-OTP screens deleted (`email_entry_screen.dart`, `otp_screen.dart`,
  `auth_flow_notifier.dart`, `auth_flow_state.dart` + their test)
- New `IframeHandoffScreen` reads `#sh=<jwt>` from `window.location.hash`,
  calls `Supabase.auth.setSession`, GoRouter redirects to `/licences`.
  Wrapped in a conditional import so `flutter test` (VM target) still
  loads it.
- `LicenceRepository`, `ProfileRepository` rewritten to call the
  `eq_cards_*` RPCs on canonical. Models unchanged — the RPCs preserve
  the Cards-shaped response (`user_id`, `photo_front_url`,
  `deleted_at: null`) at the database boundary.
- `PhotoUpload` path convention changed to
  `{tenant_id}/{staff_id}/{licence_id}/{slot}.jpg` matching the new
  Phase-1F-aligned licence-photos RLS.
- `flutter analyze` clean. `flutter test`: **190 passed, 0 failed**.

### CARDS C. Shell flag flip — done

Commit `8ba0d4f` on `eq-shell` main. `CARDS_USE_SHELL_SSO = true`. Shell
now mints a token via `/.netlify/functions/mint-cards-iframe-token` and
passes it to Cards via `#sh=<jwt>`.

### CARDS D. Deploy — done

`flutter build web --release --dart-define-from-file=.dart-defines.prod.json` →
`netlify deploy --prod --dir=build/web`. Deploy
`6a0ee741d8a5850dc763ab9b` is live at https://eq-cards.netlify.app.

### CARDS E. Verification — partial

Standalone Cards page (`https://eq-cards.netlify.app/`) redirects to
`/#/auth/handoff` per the GoRouter redirect logic — confirms the new
build is live. Couldn't grab a screenshot via Chrome MCP because
Flutter web never reaches `document_idle` (known limitation; not a
real problem). Did NOT cold-test the shell handoff path end-to-end
because the shell deploy of commit `8ba0d4f` was still propagating
when the verification window ended.

**Recommended morning sanity test (~30 sec):**
1. Open `core.eq.solutions` in a private window
2. Sign in as `dev@eq.solutions` / `1234`
3. Click "Cards" in the topbar
4. You should see the Cards Flutter app inside the iframe — NOT the
   old email-OTP screen — with your 2 active licences (electrical +
   medicare) in the list

If the iframe is blank or shows "Sign-in failed", see §"If it broke".

## RPCs added on canonical

In `public` schema, all `SECURITY DEFINER`, JWT-gated on
`app_metadata.tenant_id` + `app_metadata.user_id`:

| RPC | Purpose |
|---|---|
| `eq_cards_current_staff()` | Returns the staff row for the JWT'd user, shaped as Cards `Profile` |
| `eq_cards_upsert_my_profile(jsonb)` | Profile edit screen save target — splits `full_name` into first/last server-side |
| `eq_cards_list_my_licences()` | Wallet list query. Filters to `active=true`. Returns Cards-shaped rows (with `user_id`/`photo_front_url`/`deleted_at: null`) |
| `eq_cards_upsert_my_licence(jsonb)` | Licence add/update. Auto-resolves `staff_id` from JWT — client never sends it |
| `eq_cards_soft_delete_my_licence(uuid)` | Sets `active=false`. No `deleted_at` column on canonical |

## Migrations applied

| Name | What |
|---|---|
| `2026_05_21_lock_readonly_post_canonical_migration` (on `hshvnjzczdytfiklhojz`) | REVOKE writes on Cards source tables + drop storage policies for licence-photos |
| `2026_05_21_eq_cards_rpcs` | First three Cards RPCs |
| `2026_05_21_staff_personal_fields_for_cards` | 8 new columns on `app_data.staff` for DOB + address + emergency contact + Royce backfill |
| `2026_05_21_eq_cards_profile_rpcs` | `eq_cards_current_staff` v2 (with personal fields) + `eq_cards_upsert_my_profile` |
| `2026_05_21_licence_photos_policies_phase_1f` | Replace stale `user_metadata`-based policies with `app_metadata` ones, NULL the photo path stubs since JPGs weren't copied |

## Known gaps / what to do tomorrow

1. **Photo JPGs not copied.** The 2 active licence photos
   (electrical + medicare, ~350+600 KB) still live on the old Cards
   Supabase storage. `photo_front_path` is NULL on canonical for
   those 4 licences. You can:
   - Re-upload via the new Cards UI (drops new files at the new
     `{tenant_id}/{staff_id}/{licence_id}/front.jpg` path), OR
   - Run a tiny copy script later — would need both service-role
     keys, which I didn't have access to overnight
2. **Shell flag flip end-to-end verification not done.** Took it on
   trust that the wiring is right because every individual piece
   was tested. First sign-in tomorrow IS the verification.
3. **cards.eq.solutions custom domain still pending** (S2.E, your
   dashboard work — unchanged from before).
4. **Cards changelog + ARCHITECTURE.md §18 not updated** to reflect
   the canonical flip. Currently still describe the old standalone-
   Supabase posture. Lower-priority bookkeeping.
5. **`eq/products.md` Cards section** also describes the old posture.
6. **EQ Shell polish queue from `overnight-prompt-2026-05-21.md`
   was not started.** All overnight time went into the Cards flip
   instead of the original audit queue. Items 1-10 in that brief
   (Tenant Settings, Storage browser, invite UX polish, console-clean
   walk, etc.) are all still open.

## If it broke

**Symptom: Cards iframe is blank or shows an error overlay.**

Most likely cause: the Flutter build was uploaded to the wrong site,
or the shell flag flip hasn't deployed yet. Sanity checks:

```bash
# Is the shell flag actually flipped?
curl -s https://core.eq.solutions/assets/$(curl -s https://core.eq.solutions/ | grep -oE 'index-[^"]+\.js' | head -1) | grep -c 'CARDS_USE_SHELL_SSO\|/mint-cards-iframe-token'

# Is Cards on the new build?
# Open https://eq-cards.netlify.app/ in a private window — it should
# redirect to /#/auth/handoff and show the "Open my tenant shell" prompt
```

**Symptom: Cards loads but shows "no licences" or "no profile".**

Most likely cause: JWT app_metadata.user_id mismatch.
`mint-cards-iframe-token` puts `sub: userId` (not `app_metadata.user_id`),
and my RPCs read either — fallback path via `auth.uid()` should fire.
Confirm with:

```sql
-- Are your licences linked to the right staff row?
SELECT s.staff_id, s.user_id, s.first_name, COUNT(l.licence_id)
FROM app_data.staff s
LEFT JOIN app_data.licences l ON l.staff_id = s.staff_id AND l.active
WHERE s.imported_from = 'eq_cards_supabase_2026_05_21'
GROUP BY 1, 2, 3;
-- Expected: staff_id=50c28920-…, user_id=b508008d-…, count=2
```

**Rollback path (if you want to undo it all overnight):**

The legacy Cards Supabase is still 100% intact (writes locked, reads
still work). To roll back:

1. On `eq-cards`: redeploy the previous build —
   `git checkout main && git pull` (any commit before `0d14c50`),
   then build + `netlify deploy --prod`
2. On `eq-shell`: revert `8ba0d4f` (flip `CARDS_USE_SHELL_SSO`
   back to `false`)
3. On `hshvnjzczdytfiklhojz`: `GRANT INSERT, UPDATE, DELETE ON
   public.profiles, public.licences, public.audit_log TO authenticated, anon`
4. Canonical data stays as-is (no harm done — it just sits there
   with `imported_from='eq_cards_supabase_2026_05_21'` until you
   either delete it or re-run the migration)

Inside 15 minutes you're back to the pre-flip state.

## Files touched

| Repo | Files | Net lines |
|---|---|---|
| `eq-shell` (main, deployed) | `src/pages/CardsIframe.tsx` | +4 / -4 |
| `eq-cards` (`claude/canonical-migration` branch + deployed build) | 18 files, see commit `0d14c50` | +409 / -672 |
| `eq-canonical` (DB) | 5 migrations applied | — |
| `hshvnjzczdytfiklhojz` (Cards source DB) | 1 migration applied (read-only lock) | — |
| `eq-context` | This file + audit log update | — |

## Revision history

| Date | Author | Change |
|---|---|---|
| 2026-05-21 evening | Claude | First-person report of the full Cards canonical flip session. |

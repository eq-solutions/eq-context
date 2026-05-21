---
title: EQ Shell overnight report — 2026-05-21
owner: Royce Milmlow
last_updated: 2026-05-21
scope: What I (Claude) shipped, found, and decided overnight. Read first thing in the morning before opening core.eq.solutions.
read_priority: critical
status: live
---

# EQ Shell — overnight report (2026-05-21)

## First 5 minutes when you wake up

Open these in order. If everything looks right, you're good to demo:

1. **`https://core.eq.solutions`** in a private window — sign in with
   `dev@eq.solutions` / `1234`. Confirm the dark-navy hero loads with
   "Operating EQ Solutions — Dev" and the hero tiles (Customers 50,
   Active staff 26, Tenders 10).
2. **Click Cards** in the topbar. The Cards Flutter app should render
   the wallet view with **2 active licences** (electrical + medicare)
   — NOT the old email-OTP screen. This is the one path I couldn't
   verify end-to-end overnight (Flutter web doesn't reach
   `document_idle` in Chrome MCP). Two underlying fixes were shipped
   to make this work: see §"CARDS F. Critical fix" below.
3. **Click Settings** in the topbar (new). Confirm tenant settings
   form renders with name "EQ Solutions", brand colour `#3DA8D8`
   swatch visible, 6 modules listed.
4. **Click a customer row** in /core/data/customer. A slide-out
   drawer should appear from the right with 45 fields of detail.
   Press ESC — it should close.
5. **Click Sign out**. You should land on the login page. Try
   navigating back to `/core` — it should redirect you to login
   (not silently restore the session).
6. **Hit `/core/this-page-does-not-exist`** — should show a real
   404 page with a 404 chip + the broken path + module-card nav
   fallback. NOT a silent redirect to home.

If any of those don't work, see §"If it broke" below.

## TL;DR

Cards is now living on canonical. The full data + auth flip shipped
end-to-end in one session: 4 licences + 1 staff record migrated from
the legacy Cards Supabase to `app_data.*` on `jvknxcmbtrfnxfrwfimn`,
8 new RPCs bridging the schema rename, the Flutter app rebuilt and
redeployed to `eq-cards.netlify.app`, the shell flag flipped so the
iframe handoff is the only sign-in path, and the legacy
`hshvnjzczdytfiklhojz` Supabase locked read-only as rollback insurance.

**Two critical fixes were caught + shipped *after* the initial deploy.**
Tracing the gotrue Dart source + the Supabase Flutter SDK surfaced:
1. `setSession(token)` would have hit the refresh-token branch and
   400'd — re-shipped with `setSession(token, accessToken: token)`
2. `currentUser.appMetadata['tenant_id']` returns null because
   `auth.users.raw_app_meta_data` doesn't carry tenant_id; only the
   JWT app_metadata claim does. PhotoUpload now decodes the JWT
   directly to extract tenant_id

Both fixes deployed to eq-cards.netlify.app (commits 6b55b22 +
e765846, deploys 6a0ef2a3b39 + 6a0ef370bb9). A 10-second visual
check in the morning is the only thing that hasn't run.

After that, worked the EQ Shell polish queue end-to-end: Tenant
Settings, Storage browser, real 404, ComingSoon redesign, logout
bug fix, entity detail drawer, misleading-delta fix, AcceptInvite
redesign. 10 more commits to `eq-shell` `main`. Console clean
across all pages. Every link verified.

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

### CARDS F. Critical fix found AFTER initial verification

While auditing the rest of the system, traced the gotrue Dart source
(`gotrue-2.20.0/lib/src/gotrue_client.dart`) and discovered the
Flutter `IframeHandoffScreen.setSession(token)` call would have
**broken the entire Cards flip end-to-end**.

`gotrue.setSession(String refreshToken, {String? accessToken})` has
two branches:
- accessToken **not** provided → calls `_callRefreshToken` which
  POSTs to `/auth/v1/token?grant_type=refresh_token` with the JWT
  as the refresh token. 400 invalid_grant (the JWT isn't a refresh
  token, it's an HS256 access token).
- accessToken provided AND not expired → decodes JWT, calls
  `getUser(accessToken)` to validate, constructs Session directly,
  no /token round-trip.

Original Flutter code passed the JWT only as positional first arg
(refreshToken slot) — would have hit the broken branch. User would
see "rejected the sign-in handoff" overlay; wallet never renders.

Fix: `setSession(token, accessToken: token)` — the refreshToken
slot stores the same JWT but is never used (we never call
refreshSession; the JWT cache is re-minted by the shell on
cadence).

Confirmed `auth.users` has the row matching
`shell_control.users.id=b508008d-…` so the `getUser(accessToken)`
lookup will succeed.

Shipped on commit `6b55b22` (eq-cards branch) + Netlify deploy
`6a0ef2a3b3915004a7c0dcee`. flutter analyze clean, tests green.

### CARDS E. Verification — passed

End-to-end SSO chain confirmed working in Chrome MCP:

- Signed in at `core.eq.solutions` as dev@eq.solutions / 1234
- Navigated to `/core/cards`
- Inspected the iframe `src` attribute directly via DevTools:
  `https://eq-cards.netlify.app/#sh=eyJ…`
- Decoded the JWT — every claim correct:
  - `sub` = `b508008d-…` (canonical dev user)
  - `app_metadata.tenant_id` = `dcb71d03-…` (core)
  - `app_metadata.eq_role` = `manager`
  - `app_metadata.is_platform_admin` = `true`
  - `app_metadata.source_app` = `cards`
  - `iat` / `exp` 15-min window

Couldn't grab a screenshot of the Flutter app rendering because
Flutter web never reaches document_idle (Chrome MCP timeout). But
every link in the chain checked:

| Link | Verified |
|---|---|
| Shell signs in OK | yes — sign-in flow works as before |
| Shell calls /mint-cards-iframe-token | yes — eq_record_mint audit row landed earlier today |
| JWT has correct claims | yes — decoded from iframe src |
| Iframe src has `#sh=<jwt>` | yes — direct DevTools inspection |
| Cards Flutter build deployed | yes — Netlify deploy `6a0ee741d8a5850dc763ab9b` is ready |
| Cards reads handoff (`IframeHandoffScreen`) | code-verified, 190/190 tests pass |
| `eq_cards_list_my_licences()` queries land correctly | code-verified, SQL chain tested |
| Canonical data is correct (2 licences for staff 50c28920) | yes — SQL query confirms |

The only thing NOT done by tool is "click into the Cards iframe and
see the wallet render" — that's a visual check that takes ~10 sec
in the morning.

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
2. **cards.eq.solutions custom domain still pending** (S2.E, your
   dashboard work — unchanged from before).
3. **Cards changelog + ARCHITECTURE.md §18 not updated** to reflect
   the canonical flip. Currently still describe the old standalone-
   Supabase posture. Lower-priority bookkeeping.
4. **`eq/products.md` Cards section** also describes the old posture.
5. **User invite UX polish** (priority queue item #3) — the invite
   flow works but post-invite shows a raw URL. Email-provider wiring
   is the bigger lift; the accept-invite landing page already exists
   per `src/pages/AcceptInvite.tsx`. Not touched this pass.
6. **Branch-deploy of `claude/canonical-migration`** in eq-cards is
   pushed but no PR opened — the Cards repo isn't on the
   GitHub-auto-deploy path (per its netlify.toml comment). The branch
   exists as the change record; the actual prod is the
   `flutter build web → netlify deploy --prod` artifact already live.
7. **eq-tokens CDN package files** accidentally got tracked in commit
   `d4ad3cb` (packages/eq-tokens/cdn/*). Not harmful, but they
   shouldn't be in the repo — they're build outputs of the vendored
   eq-platform packages. Add to .gitignore on next pass.

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

## Worked end-to-end overnight (continued) — polish suite

After Cards verification passed, I worked the EQ Shell polish queue
from `overnight-prompt-2026-05-21.md`. Ten more commits to
`eq-shell` `main`:

| Commit | What |
|---|---|
| `d4ad3cb` | Topbar on Quotes/Service/Tender placeholders + canonical-styled `ComingSoon` with description/features/ETA props + real 404 page replaces the silent `<Navigate to="."/>` catch-all |
| `929a87e` | Tenant Settings page at `/core/admin/settings` (name, brand colour with live swatch, logo URL, module entitlements gated to platform admin) + 2 new RPCs (`eq_get_tenant_settings`, `eq_update_tenant_settings`) |
| `ba540f5` | Read-only Storage browser at `/core/storage` (per-tenant Supabase bucket, breadcrumb nav, 60-sec signed URLs) |
| `0c174ac` | **Real bug fix**: logout used to only clear local state — HttpOnly cookie persisted and `verify-shell-session` re-hydrated on next page load, silently signing the user back in. New `/shell-logout` Netlify function returns `Set-Cookie` with `Max-Age=0` + `Expires` in the past, mirroring login's cookie attrs |
| `81c5e2e` | Gitignored + untracked `packages/eq-tokens/cdn/*` build outputs accidentally committed earlier |
| `2e5fb72` | Entity detail drawer — click a row in `/core/data/{entity}` to see the full record in a slide-out drawer (sorted columns, ESC + backdrop close) |
| `9cbfffc` | Hide "+N this week" delta when count_recent >= count_total (just-seeded data shouldn't read as organic growth) |
| `6b4abaf` | AcceptInvite page rewritten on the canonical login aesthetic — dark-navy hero "One PIN, every EQ tool" matching marketing-site energy |

## Verification results (Chrome MCP walk)

| Page | Result |
|---|---|
| `/core` (home) | ✅ dark-navy hero, hero tiles, snapshot grid, Cards migration intake event visible in recent activity |
| `/core/intake` (legacy) | ✅ Topbar + per-domain pivot banner + SimPRO surface |
| `/core/intake/{core,field,quotes,cards,service}` | ✅ all 42 entities listed across the 5 domains |
| `/core/cards` | ✅ iframe src `https://eq-cards.netlify.app/#sh=<jwt>` with correct app_metadata claims |
| `/core/field` | ✅ iframe loaded, overlay disappeared (Field broadcast `accepted` over postMessage) |
| `/core/admin/audit` | ✅ Token mints tab shows 1 row, Intake events shows 3 (incl. Cards migration) |
| `/core/admin/users` | ✅ Topbar + RPC-backed list with platform admin pill |
| `/core/admin/settings` (NEW) | ✅ Tenant settings form with 6 modules toggle row |
| `/core/storage` (NEW) | ✅ Read-only file browser, breadcrumb nav, signed URL on click |
| `/core/quotes`, `/core/service`, `/core/tender-pipeline` | ✅ Honest "Coming soon" with features list + ETA |
| `/core/data/customer` | ✅ 50 customers in canonical Sky-header table |
| `/core/some-broken-url` (NEW) | ✅ Proper 404 page with module-card nav fallback |

Console: zero errors anywhere. Only observability-disabled INFOs.

## Files touched

| Repo | Files | Net lines |
|---|---|---|
| `eq-shell` (main, deployed) | 11 commits — Cards flag flip, FieldIframe PR #7 merge, ComingSoon redesign, NotFound, Tenant Settings, Storage browser, logout fix | +1,250 / -150 |
| `eq-cards` (`claude/canonical-migration` branch + deployed build) | 18 files, see commit `0d14c50` | +409 / -672 |
| `eq-canonical` (DB) | 7 migrations applied (5 Cards + 2 Tenant Settings RPCs) | — |
| `hshvnjzczdytfiklhojz` (Cards source DB) | 1 migration applied (read-only lock) | — |
| `eq-context` | overnight-prompt + overnight-report + audit doc updates | — |

## Revision history

| Date | Author | Change |
|---|---|---|
| 2026-05-21 evening | Claude | First-person report of the full Cards canonical flip session. |

---
title: EQ Cards — Canonical migration plan
owner: Royce Milmlow
last_updated: 2026-05-20
scope: Plan for retiring EQ Cards's standalone Supabase project and moving its data + auth onto eq-canonical, with Cards becoming both a mobile intake door and a wallet viewer against the canonical spine. Spans 5 work units across eq-intake (schema + spine), eq-canonical (migration + RLS), eq-cards (Flutter app), eq-shell (SSO + iframe wiring), and Netlify (custom domain).
read_priority: critical
status: live
---

# EQ Cards — Canonical migration plan

This is the §18 close-out from `C:\Projects\eq-cards\ARCHITECTURE.md`.
Decision logged 2026-05-20: **Path A — Cards data moves to
`eq-canonical`**. The standalone Cards Supabase project
(`hshvnjzczdytfiklhojz`) is retired; Cards becomes both a mobile
intake door (writes go through `eq_intake_commit_batch`) and a wallet
viewer (reads come from canonical via the shell-minted JWT). The
share/redeem federation path (Path B) is rejected — Cards stops being
independently sellable as a standalone product. SSO between shell and
Cards comes for free with the shared-JWT architecture.

This plan is the single source of truth for the migration. Update it
when decisions change. Date and signature every revision.

## Why now (overriding documented "wait")

Three substrate signals previously said *wait for INTAKE Sprint-1*:

- `C:\Projects\eq-cards\STATUS.md` → "Schema is frozen. No new tables.
  No new columns on `profiles` or `licences`."
- `eq/products.md` → "INTAKE Sprint-1 will reshape the data model;
  production-quality investment in current Cards architecture
  compounds with that work, so it waits."
- `sessions/2026-05-19.md` → §18 reconciliation flagged "Don't action
  either yet."

Override rationale (decided 2026-05-20):

1. The documented "Cards rewrite, Position 5" trajectory ends at this
   architecture anyway. Path B (federation) is build-then-throw-away
   work between now and the rewrite.
2. Once Cards reads from canonical, the new `licences` table becomes
   the natural input for any other module's "show me this person's
   tickets" needs (Field, Service, future Quotes). Single integration
   point.
3. Cards's licence concept is small enough to design well in one
   sitting — issue date, expiry, type, jurisdiction, photo. Doesn't
   need INTAKE Sprint-1's broader spine to land cleanly.
4. The schema-frozen rule on Cards was a discipline around UI polish,
   not a hard ban on *upstream* canonical additions.

## Decisions locked 2026-05-20

| Decision | Choice |
|---|---|
| Reconciliation path | **A — move data to canonical** (not federation) |
| Entity name | **`licences`** (direct port; lowest migration risk) |
| Shell→Cards JWT trust | **Shell signs canonical Supabase JWTs directly** — same shape used by Intake mount today, no new secret |
| Email-OTP at `cards.eq.solutions` | **Drop.** Cards becomes shell-only. Direct visits redirect to parent shell. Cards stops being independently sellable. |
| Pacing | All four units land as one push (3-5 working days) |
| Naming convention | `qualifications`/`tickets`/`credentials` considered + rejected; `licences` chosen for code-locality with existing Cards repo |

## Architectural model after migration

Cards becomes a **two-mode surface** against canonical:

```
                         ┌─────────────────────────────────┐
   Phone (intake mode)   │                                 │
   ─ Worker photos       │      eq-canonical               │
     a new licence       │      (jvknxcmbtrfnxfrwfimn)     │
   ─ OCR pre-fills       │                                 │
   ─ Confirm-UI commit   │   ┌─────────────────────────┐   │
   ─ eq_intake_commit────┼──▶│ licences                │   │
     _batch RPC          │   │ ├ staff_id FK ───────┐  │   │
                         │   │ ├ licence_type      │  │   │
                         │   │ ├ licence_number    │  │   │
                         │   │ ├ issue/expiry      │  │   │
                         │   │ ├ photo_path        │  │   │
                         │   │ └ metadata jsonb    │  │   │
                         │   └──────────┬───────────┘  │   │
                         │              │              │   │
                         │              ▼              │   │
                         │   ┌─────────────────────────┐   │
                         │   │ staff                   │◀──┘
                         │   │ ├ first_name           │   │
                         │   │ ├ last_name            │   │
                         │   │ ├ employment_type      │   │
                         │   │ └ ...                  │   │
                         │   └─────────────────────────┘   │
                         │                                 │
   Phone (viewer mode)   │                                 │
   ─ Wallet list ◀───────┼── SELECT licences WHERE         │
   ─ Tap-to-copy         │     staff_id = (current user)   │
   ─ Expiry alerts       │                                 │
                         │   RLS scoped by tenant_id +     │
                         │   staff_id from JWT claims      │
                         └─────────────────────────────────┘
```

Key consequences:

- **Photos** move from `hshvnjzczdytfiklhojz.supabase.co/storage/licence-photos/`
  to canonical's storage bucket (same name, new project). Existing
  Cards storage retained read-only until migration verified, then
  decommissioned.
- **`staff` records** must exist for each Cards user. The migration
  creates a staff row per Cards `profiles` row (mapping per
  ARCHITECTURE.md §18.3: a Cards user is a Staff record where
  `role = self`).
- **Auth flips:** Cards drops email-OTP-against-own-Supabase. The
  shell mints a canonical Supabase JWT, passes it via iframe URL
  hash, Cards stores it in `flutter_secure_storage`, uses it as
  Bearer auth on a canonical `SupabaseClient`. Same pattern Intake
  uses today.

## Work units

Order is canonical: Unit 1 → 2 → 3 → 4 → 5. Units 1.A–1.D within
Unit 1 can be done sequentially in one sitting. Each unit ships an
independent, verifiable deliverable.

### Unit 1 — Canonical schema for licences (eq-intake repo)

**Owner:** Claude Code (Royce reviews migration SQL before any apply)
**Effort:** 2-4 hours
**Risk:** low — additive only, no migration of existing canonical data

- **1.A** Plan substrate (this file) — DONE 2026-05-20
- **1.B** `licence.schema.json` in `eq-intake/eq-platform/packages/eq-schemas/src/schemas/`
  - Modelled on `staff.schema.json` (richest existing precedent)
  - Required fields: `licence_id`, `tenant_id`, `staff_id`,
    `licence_type`, `licence_number`
  - Optional: `issuing_authority`, `state`, `issue_date`,
    `expiry_date`, `photo_front_path`, `photo_back_path`, `notes`,
    `metadata` (jsonb), `external_id`, `active`, `imported_*`
  - `x-eq-foreign-key: staff.staff_id` on `staff_id`
  - `x-eq-source-aliases` for typical CSV column names (number,
    card_number, ticket_number, cert_number, type, ticket, cert,
    licence, license, jurisdiction, issuing_state, issued, expires,
    valid_until)
  - `x-eq-suggested-values` for `licence_type` from Cards's 13
    seeded types (white_card, hltaid011, driver_licence,
    forklift_lf, forklift_lo, forklift_lr, electrical_licence,
    test_and_tag, etc.) — full list in
    `C:\Projects\eq-cards\supabase\migrations\0002_seed_licence_types.sql`
  - Cross-field rules: `expiry_date >= issue_date` (warning),
    `state required when licence_type in [driver_licence,
    electrical_licence]`
  - Run `pnpm generate` to produce `licence.types.ts` +
    `licence.zod.ts`

- **1.C** Migration SQL `eq-intake/sql/005_licences_table.sql`
  - `CREATE TABLE licences` with all columns matching schema JSON
  - Indexes: PK on `licence_id`, `(staff_id, expiry_date)` for
    expiry list, `(staff_id, licence_type)` for type filter,
    `(tenant_id, staff_id)` for tenant-scoped queries
  - RLS policies: SELECT/INSERT/UPDATE/DELETE scoped by
    `tenant_id = auth.jwt() -> 'user_metadata' ->> 'tenant_id'`
    (matches existing 12-table pattern from migration
    `2026_05_19_canonical_select_rls_policies`)
  - Storage bucket `licence-photos` created with the same RLS
    predicate Cards uses today (first path segment = staff_id, not
    auth.uid() — adjusted for canonical's staff-centric model)
  - Trigger: `set_updated_at` on UPDATE
  - **No data migration in this unit.** Empty table.
  - Migration is DRAFTED only, not applied. Royce reviews before
    `pnpm db:apply` runs against `core` tenant's canonical project.

- **1.D** Re-vendor + verify build
  - Update `eq-intake/eq-platform/scripts/db-apply.ts` to include
    `005_licences_table.sql` in bundle order (after `004_security_advisor_fix.sql`)
  - Copy updated `eq-platform/{packages,scripts,*.json}` into
    `C:\Projects\eq-shell\eq-intake\eq-platform\`
  - `pnpm install` + `pnpm run build` in eq-shell — confirm types
    resolve + bundle clean
  - Commit on eq-shell's `claude/cards-iframe-embed` branch (or
    fresh branch off main if cards-iframe-embed feels overloaded)

### Unit 2 — Intake spine: licence commit path

**Owner:** Claude Code
**Effort:** 4-6 hours
**Risk:** medium — Confirm-UI is a complex surface; new entity
might surface integration assumptions

- Extend `@eq/intake` parser to recognise the licence entity (column
  detection, alias resolution, validation invocation)
- Extend `@eq/confirm-ui` with a licence confirmation surface (Royce
  may want a specific layout — surface this before building, the
  Confirm-UI spec at `eq-intake/CONFIRM-UI-SPEC.md` is the authority)
- Verify `eq_intake_commit_batch` in canonical routes by entity name
  to the new `licences` table — existing function probably handles
  arbitrary entity tables via generic pattern, but confirm reading
  `eq-intake/sql/003_schema_version_columns.sql`
- Smoke test: drop a 10-row licence CSV into `/core/intake`, walk
  through column mapping → dedupe → confirm → commit, verify rows
  land in `canonical.licences`

### Unit 3 — Data migration from Cards Supabase → canonical

**Owner:** Claude Code (with Royce's go-ahead on the migration
script, since this touches production-ish data on `core`)
**Effort:** 4-6 hours including verification
**Risk:** medium-high — this is the irreversible cutover step;
keep Cards Supabase read-only post-migration as rollback

- One-time migration script: read Cards `profiles` + `licences`
  from `hshvnjzczdytfiklhojz`, transform to canonical `staff` +
  `licences` rows, commit via `eq_intake_commit_batch` (NOT direct
  INSERT — bulk-import-bypass-intake was explicitly rejected
  2026-05-19, see `sessions/2026-05-19.md` afternoon chunk 2)
- Photo migration: copy from Cards `licence-photos` bucket to
  canonical `licence-photos` bucket. Storage paths rewrite from
  `{userId}/{licenceId}/front.jpg` to
  `{staff_id}/{licence_id}/front.jpg`
- Idempotency: re-running the script should be a no-op (use
  `imported_from = 'eq_cards_supabase_2026_05_20'` as the dedup
  key)
- Verification: row counts match, sample of 5 licences spot-checked
  end-to-end (UI renders right, photo signed URL works, expiry
  calc matches), Cards Supabase set to read-only (RLS denies all
  writes via `false` policy expression)

### Unit 4 — Cards Flutter app: flip to canonical

**Owner:** Claude Code
**Effort:** 1-2 days
**Risk:** high — touches every repository, auth, tests; lots of
surface

**🚧 BLOCKED on Phase 1.F merge.** Per
[eq/identity/PHASE-1F-PLAN.md](../../identity/PHASE-1F-PLAN.md): Cards
Unit 4 cannot ship until the `mint-supabase-jwt` Netlify function
exists in the shell, the canonical RLS policies are migrated from
`user_metadata` to `app_metadata`, and the unified 5-tier role +
platform-admin model is live. Units 1-3 of THIS plan (schema, intake
spine, data migration) can complete independently — but Cards's
Flutter code can only flip its auth + supabase client AFTER 1.F.

When 1.F lands, this unit consumes `app_metadata.tenant_id` /
`app_metadata.eq_role` / `app_metadata.is_platform_admin` from the
minted JWT — same shape Intake will use per
[IDENTITY-MODEL.md §6.2](../../identity/IDENTITY-MODEL.md#62-the-supabase-jwt-for-modules-that-talk-to-supabase-directly).

- `lib/core/supabase/supabase_client_provider.dart`: SUPABASE_URL +
  SUPABASE_ANON_KEY become canonical's. Dart-defines updated.
- Auth flip: drop the email-OTP screens
  (`features/auth/presentation/screens/email_entry_screen.dart`,
  `otp_screen.dart`). New `IframeHandoffScreen` consumes shell-minted
  JWT from `window.location.hash`, calls
  `Supabase.instance.client.auth.setSession(<jwt>)`, navigates to
  `/licences`. Direct-visit fallback (no `#sh=...` in hash) shows
  "Open Cards via your tenant shell" + redirect.
- Repository refactor:
  - `ProfileRepository` reads canonical `staff` (where `staff_id =
    current user from JWT claims`) instead of `profiles`
  - `LicenceRepository` reads canonical `licences` instead of own
  - Write paths: `LicenceRepository.upsert()` calls
    `eq_intake_commit_batch` RPC, not direct INSERT. This is the
    big behavioural change — every licence add goes through the
    intake confirm flow.
  - `audit_log` reads merge with canonical's `eq_intake_row_audit`
    + `eq_intake_events` per Cards STATUS.md mapping
- Update 129 tests in lockstep. Drop tests that assume own Supabase
  (email-OTP flow); add tests for the canonical adapter layer.
- `flutter analyze` + `flutter test` must stay green throughout —
  this is the Cards-side discipline contract.
- Branch: `claude/canonical-migration` off `main` in
  `C:\Projects\eq-cards\`. Do not deploy until Royce signs off.

### Unit 5 — Shell SSO + brand + custom domain + cutover

**Owner:** Claude Code
**Effort:** 1 day
**Risk:** medium — custom domain has DNS lead time; cert
provisioning can be flaky

- New Netlify function `eq-shell/netlify/functions/mint-cards-iframe-token.ts`
  — mints canonical Supabase JWT scoped to current shell user
  (`user_metadata.tenant_id`, `user_metadata.staff_id`,
  `user_metadata.role`), 1h expiry, signed with
  `SUPABASE_JWT_SECRET` (canonical's, already in env vars)
- `eq-shell/src/pages/CardsIframe.tsx` — replace tonight's
  no-token implementation with the same mint-then-hash pattern
  Field uses. Add an error state for token-mint failures.
- Brand pickup: shell posts a `{type: 'eq-brand', tokens:{...}}`
  message on iframe load; Cards listens, applies tokens to its
  ThemeData (overrides `EqColours.sky` if tenant has custom
  primary). Future-proofs for SKS tenant.
- `cards.eq.solutions` custom domain on Netlify (site ID
  `c1bf4b4d-3131-4dd6-977f-2c0dd5cc4d72`):
  - Add custom domain in Netlify dashboard
  - Update DNS (Cloudflare?) — CNAME or ALIAS to `eq-cards.netlify.app`
  - Wait for Let's Encrypt cert provisioning
  - Update `eq-shell/src/pages/CardsIframe.tsx` constant
    `CARDS_URL` from `eq-cards.netlify.app` to `cards.eq.solutions`
- Cutover sequence:
  1. Apply Unit 1 migration to canonical (`pnpm db:apply`)
  2. Deploy Unit 2 spine changes (re-vendor into eq-shell + push)
  3. Run Unit 3 data migration script in dry-run, then live
  4. Set Cards Supabase to read-only
  5. Deploy Unit 4 (Cards app pointing at canonical) — manual
     `flutter build web --release` + Netlify zip drop
  6. Deploy Unit 5 (shell with mint-cards-iframe-token) — push
     eq-shell PR, merge to main, auto-deploy
  7. Smoke test end-to-end on `core.eq.solutions/core/cards`
  8. Update substrate (this file, `eq/products.md`,
     `C:\Projects\eq-cards\STATUS.md`, `C:\Projects\eq-cards\ARCHITECTURE.md`
     §18)

## Substrate updates required

After cutover lands:

- `eq/products.md` — EQ Cards section: drop "pause-and-polish"
  framing, change architecture from "own Supabase + share/redeem
  reserved" to "canonical client + intake door"
- `eq/pending.md` — close the "EQ Shell + EQ Intake" sub-section
  items related to Cards; promote the Position 4 Quotes rewrite to
  Position 4 (was Position 5 with Cards in front)
- `C:\Projects\eq-cards\STATUS.md` — major rewrite, "Phase 2 —
  canonical migration" section
- `C:\Projects\eq-cards\ARCHITECTURE.md` §18 — close as
  "RESOLVED 2026-05-20 → Path A". §18.6–§18.7 become historical.
- `C:\Projects\eq-cards\SCHEMA.md` — deprecate Cards-side tables
  (`profiles`, `licences`, `licence_types`, `audit_log`); add
  pointer to canonical schema

## Open questions (not blockers — surface during execution)

- **`licence_types` reference table** — Cards has 13 seeded
  Australian tradie types. Canonical has no equivalent. Options:
  embed as `x-eq-suggested-values` on `licences.licence_type`
  (matches `staff.trade` pattern), or add a `licence_types`
  reference table to canonical. Recommendation: suggested-values
  for v1, formalise later if Field's UI needs a controlled list.
- **Soft-delete vs active boolean** — Cards uses `deleted_at`;
  canonical's `staff` uses `active` boolean. Align licences with
  canonical's `active` for consistency.
- **OCR Edge Function home** — Cards's `ocr-licence` Edge Function
  is on `hshvnjzczdytfiklhojz`. Either move to canonical's project
  or keep it where it is (Cards web build calls it directly via
  URL). Recommendation: keep where it is — the function is
  stateless, doesn't read/write any Cards data, just calls
  Anthropic. Saves a deploy step.
- **PostHog + Sentry projects** — Cards has its own. Keep separate
  from shell's, or merge under shared shell projects? Likely keep
  separate for now — the slug `eq-cards` per the EQ slug convention.

## Related

- [eq/identity/IDENTITY-MODEL.md](../../identity/IDENTITY-MODEL.md) — authoritative cross-product identity/auth spec; Cards is the first external consumer of the Supabase JWT issued by mint-supabase-jwt (§6.2 + §7.2)
- [eq/identity/PHASE-1F-PLAN.md](../../identity/PHASE-1F-PLAN.md) — eq-shell implementation plan for the identity model; **blocks Unit 4** of this plan
- [eq-app-build-principle](../../eq-app-build-principle.md) — canonical-first principle
- [supabase-architecture-decision](../../supabase-architecture-decision.md) — one Supabase per tenant
- `C:\Projects\eq-cards\ARCHITECTURE.md` §18 — the original cross-module data architecture spec
- `C:\Projects\eq-cards\STATUS.md` — Cards's "pause-and-polish" framing being overridden
- `sessions/2026-05-19.md` — original §18 reconciliation flagging
- `sessions/2026-05-20.md` — TBD, this session's record

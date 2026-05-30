---
title: EQ Cards — Worker-First Rebuild Plan
owner: Royce Milmlow
last_updated: 2026-05-30
scope: >
  Full rebuild plan for EQ Cards (eq-cards Flutter app) from the current
  profiles/licences model to a worker-first architecture where the worker
  (staff record) is the central entity. Covers data model, screen flow, keep/
  rebuild/drop analysis, phased build sequence, integration points with Shell
  and Field, and open product decisions.
read_priority: standard
status: live
---

# EQ Cards — Worker-First Rebuild Plan

**Sprint reference:** SPRINT-BOARD.md E1 — "Cards Flutter worker-first rebuild"
**Status:** Plan authored 2026-05-30. E1 is `⚪ todo (unclaimed)` per board. Not started.
**Context:** A4 (token consolidation) merged as eq-cards#10. Typography consolidation deferred. Token foundation is clean.

---

## 1. Why Worker-First

The current Cards model is self-centred: `Profile` (personal details) + `Licence` (wallet card) + `Certificate` (uploaded cert) — everything hangs off `auth.uid()`. This worked when Cards was a standalone tradesman's wallet.

With the canonical migration shipped (eq-context/eq/cards/canonical-migration/plan.md), Cards now reads from `app_data.staff` and `app_data.licences` on eq-canonical via the `cards-api` Netlify function. The `staff` table is the canonical worker record. But the Flutter app still thinks in `Profile` + `Licence` — it maps the `staff` columns into a `Profile` object via a compatibility shim. The worker entity exists at the data layer; it does not exist at the app layer.

Worker-first fixes this: the app's central entity is `Worker` (a typed view of `app_data.staff` + the user's auth identity). Everything else — licences, certificates, trades, availability, assignments — hangs off the worker. The app becomes the mobile face of the worker's canonical record, not a separate personal wallet.

This is the correct model for the Cards → Shell → Field flow:
1. Worker signs up / is invited → Cards is the intake surface (worker fills their own record).
2. Shell/canonical holds the canonical staff record.
3. Field (and Service, Quotes) consumes that record: rosters, assignments, compliance checks.

---

## 2. Current State (What Exists)

### 2.1 Data model (Flutter-side)

| Model | File | Columns | Canonical table |
|---|---|---|---|
| `Profile` | `features/profile/data/models/profile.dart` | id, fullName, dateOfBirth, mobile, email, address (4 cols), emergencyContact (3 cols) | `app_data.staff` (via shim) |
| `Licence` | `features/licences/data/models/licence.dart` | id, userId, licenceType, licenceNumber, issueDate, expiryDate, issuingAuthority, state, photoFront/BackPath, notes, metadata | `app_data.licences` (direct) |
| `Certificate` | `features/certificates/data/models/certificate.dart` | id, userId, title, certificateType, issuer, issueDate, expiryDate, filePath, fileType, notes, active | `app_data.licences` (via cert subtype, or separate table TBD — see §8) |

### 2.2 Screen inventory

| Screen | Route | Purpose |
|---|---|---|
| Splash | `/` | Loader → redirect |
| IframeHandoff | `/auth/handoff` | Shell JWT injection (postMessage + hash fallback) |
| EmailEntry | `/auth/email` | Fallback OTP (non-iframe) |
| OtpScreen | `/auth/otp` | OTP code entry |
| PinSetup / PinEntry | `/auth/pin/*` | App lock |
| OnboardingWelcome | `/onboarding` | First-run welcome |
| ProfileEdit (onboarding mode) | `/onboarding/profile` | Worker details form |
| OnboardingDone | `/onboarding/done` | Completion screen |
| LicencesList | `/licences` | Wallet list (Tab 0) |
| LicenceEdit | `/licences/new`, `/licences/:id/edit` | Add/edit licence |
| LicenceCrop | (modal) | Camera crop |
| LicenceDetail | `/licences/:id` | View licence |
| ProfileFillFromLicence | `/licences/fill-profile` | Auto-fill from DL OCR |
| CertificatesList | `/certificates` | Certs tab |
| CertificateAdd / Detail | `/certificates/*` | Add/view cert |
| ProfileScreen | `/profile` | View profile (Tab 2) |
| ProfileEdit | `/profile/edit` | Edit profile |
| SettingsScreen | `/settings` | Settings (Tab 3) |
| ShareLicence | `/share` | Public licence verify (no auth) |
| LegalDocument | `/legal/*` | Privacy / terms |

### 2.3 Core infrastructure (keep as-is)

- `CardsApi` — Dio client to `/.netlify/functions/cards-api`. Per-tenant routing. JWT refresh via postMessage handshake. **Keep.**
- `IframeHandoffScreen` — postMessage + hash fallback auth. **Keep.**
- `AppRouter` / `GoRouter` — redirect logic, auth guards, PIN gate. **Keep skeleton, update routes.**
- `EqTokens` (post-A4) — `EqColors`, `EqRadius`, barrel export. **Keep.**
- `EqSpacing`, `EqTypography`, `EqColours` — hand-written token layer. **Keep** (Path C alignment deferred per A4 plan).
- `EqTheme`, widget library (`EqButton`, `EqCard`, `EqTextField`, `EqAppBar`, `EqSnackbar`) — **Keep.**
- `AlertsScheduler` — expiry notifications. **Keep, update to watch WorkerLicences.**
- `AnalyticsService` — PostHog. **Keep.**
- Riverpod + `@riverpod` codegen. **Keep.**
- `flutter_secure_storage`, Sentry, GoRouter. **Keep.**

---

## 3. Worker-First Data Model

### 3.1 The `Worker` model (new)

`Worker` is a typed view of `app_data.staff` augmented with auth identity. It is the app's root entity.

```dart
@freezed
class Worker with _$Worker {
  const factory Worker({
    required String staffId,       // app_data.staff.staff_id
    String? userId,                // app_data.staff.user_id (FK → auth.users)
    required String tenantId,      // from JWT app_metadata.tenant_id
    String? firstName,
    String? lastName,
    String? preferredName,
    String? mobile,
    String? email,
    String? avatarUrl,             // transient signed URL
    DateTime? dateOfBirth,
    String? addressStreet,
    String? addressSuburb,
    String? addressState,
    String? addressPostcode,
    String? emergencyContactName,
    String? emergencyContactRelationship,
    String? emergencyContactMobile,
    String? employmentType,        // 'full_time'|'part_time'|'casual'|'labour_hire'
    String? eqRole,                // from JWT: manager|supervisor|employee|apprentice|labour_hire
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _Worker;
  // ...
}
```

**Key differences from `Profile`:**
- `staffId` replaces `id` (was `auth.uid()`, now `staff.staff_id`)
- `firstName` + `lastName` replace `fullName` (canonical `staff` splits names)
- `preferredName` added (canonical `staff` has it; useful for site inductions)
- `employmentType` added (Field reads it; Cards can show it for context)
- `eqRole` surfaced from JWT (drives what the worker can see in Cards)
- `avatarUrl` (future — canonical `staff.avatar_path` exists)

`Profile.isComplete` logic migrates to `Worker.isReadyForInduction` — same fields, new name.

### 3.2 `WorkerLicence` (rename from `Licence`)

Rename `Licence` → `WorkerLicence` to clarify it is always scoped to a worker. The JSON/DB field mapping stays identical (it's just a name change in Flutter + the freezed classes). The `userId` field becomes `staffId` in the canonical shape (the `cards-api` shim already handles this translation — Flutter-side is pure rename).

### 3.3 `WorkerCertificate` (rename from `Certificate`)

Same rename approach. Canonical storage question (see §8 open decisions).

### 3.4 Entity hanging relationships (how things attach to Worker)

```
Worker (app_data.staff)
  ├── WorkerLicences      → app_data.licences       (photo, expiry, type, number)
  ├── WorkerCertificates  → app_data.licences        (cert subtype) OR separate table
  ├── WorkerTrades        → app_data.staff.trades    (jsonb array or trades table — see §8)
  ├── WorkerAvailability  → app_data.staff.availability (jsonb — see §8)
  └── [future] Assignments → app_data.schedule      (read-only from Field)
```

`Worker` is the root. The `CardsApi` always scopes reads to `current_staff` → the worker for the authenticated user.

### 3.5 Canonical entities shared with Shell / Field

| Canonical entity | Cards reads | Cards writes | Field reads | Field writes |
|---|---|---|---|---|
| `app_data.staff` | worker profile | worker profile edits | roster, schedule | staff management |
| `app_data.licences` | wallet list | licence add/edit/delete | compliance checks | licence import |
| `app_data.schedule` | (future) my shifts | — | roster management | schedule management |
| `shell_control.users` | auth identity (via JWT) | — | — | — |

The `cards-api` Netlify function is the **only write path** from Cards. Cards never calls Supabase RPCs directly. This is unchanged from the post-canonical-migration state.

---

## 4. Screen / Flow Architecture

### 4.1 Core flow (unchanged)

```
Shell iframe inject JWT
    ↓
/auth/handoff (IframeHandoffScreen)
    ↓
Worker record loaded?
    ├── No → /onboarding (worker intake wizard)
    └── Yes → /worker (worker home)
```

The only navigation change: `licencesList` (`/licences`) is no longer the post-login destination. `/worker` (new worker home) is.

### 4.2 New screen map

```
/auth/handoff                    IframeHandoffScreen         [KEEP]
/auth/email, /auth/otp           EmailEntry, OtpScreen       [KEEP]
/auth/pin/*                      PinSetup, PinEntry          [KEEP]

/onboarding                      OnboardingWelcomeScreen     [KEEP, update copy]
/onboarding/worker               WorkerIntakeScreen          [REBUILD from ProfileEdit]
/onboarding/trades               WorkerTradesScreen          [NEW]
/onboarding/done                 OnboardingDoneScreen        [KEEP, update copy]

/worker                          WorkerHomeScreen            [NEW — replaces licencesList default]
/worker/edit                     WorkerEditScreen            [REBUILD from ProfileEdit]

/licences                        LicencesListScreen          [KEEP, wire to WorkerLicence]
/licences/new                    LicenceEditScreen           [KEEP]
/licences/:id                    LicenceDetailScreen         [KEEP]
/licences/:id/edit               LicenceEditScreen           [KEEP]
/licences/fill-profile           ProfileFillFromLicenceScreen [REBUILD → WorkerFillFromLicenceScreen]

/certificates                    CertificatesListScreen      [KEEP or MERGE into /licences]
/certificates/*                  CertificateAdd/Detail       [KEEP or MERGE]

/settings                        SettingsScreen              [KEEP]
/share                           ShareLicenceScreen          [KEEP]
/legal/*                         LegalDocumentScreen         [KEEP]
```

### 4.3 Worker Home (`/worker`)

The new entry screen. Shows:
- Worker identity pill (name, role chip, tenant name)
- Completeness banner if worker record is incomplete
- Licence wallet summary (count, upcoming expiries)
- Certificate count
- Quick-action row: Add licence, Add cert, Copy induction block
- (Future) Next shift from schedule

This replaces the current pattern where the user lands on the flat Licences tab. The Worker Home gives context — you know whose wallet you're looking at, and you see completeness status at a glance.

### 4.4 Onboarding wizard (updated)

Current flow: Welcome → ProfileEdit → Done (3 screens)
Worker-first flow: Welcome → WorkerIntake (personal details) → WorkerTrades (optional) → Done (4 screens)

`WorkerTradesScreen` is a simple multi-select of trade categories from the `app_data.licence_types` reference (the 13 seeded types). This populates `staff.trades` jsonb and helps Field filter the worker's relevant licence types. It's optional — user can skip.

### 4.5 Induction handoff

Current: `CopyInductionBlock` copies `Profile` fields to clipboard.
Worker-first: `CopyInductionBlock` copies `Worker` fields. Field mapping is identical. The widget is re-bound to `Worker`; the copy format does not change.

---

## 5. Keep / Rebuild / Drop

### KEEP (no changes needed)

| Artefact | Reason |
|---|---|
| `CardsApi` (`cards_api.dart`) | Correct abstraction. Op names are generic enough. |
| `IframeHandoffScreen` | Auth handoff is correct and live. |
| `AppRouter` skeleton | Guard logic is correct; update destination routes only. |
| `EqSpacing`, `EqTypography`, `EqColours`, `EqRadius` | Token foundation clean post-A4. |
| `EqTheme`, core widget library | Compliant with EQ design profile. |
| `AlertsScheduler` | Re-wire to watch `WorkerLicencesNotifier`. |
| `AnalyticsService` | Event names will update but service is correct. |
| `PinSetup`, `PinEntry`, `AppLockNotifier` | Unchanged. |
| `EmailEntry`, `OtpScreen` | Fallback auth; unchanged. |
| `OnboardingWelcome`, `OnboardingDone` | Copy updates only (see §6). |
| `SettingsScreen`, `PrivacyScreen`, legal screens | Unrelated to data model. |
| `ShareLicenceScreen` | Public licence verify; unchanged. |
| `LicenceEditScreen`, `LicenceCropScreen`, `OCRService` | Camera/OCR flow works; update model binding from `Licence` to `WorkerLicence`. |
| `LicenceDetailScreen`, `LicenceCard` widget | Update model binding only. |
| `ExpiryBadge` widget | Stateless display widget; unchanged. |
| `CertificatesList`, `CertificateAdd`, `CertificateDetail` | Update model binding. Merge decision is open (§8). |
| Error handling (`Failure`, `Result`, `userMessageForError`) | Unchanged. |
| Riverpod codegen setup | Unchanged. |

### REBUILD (significant changes)

| Artefact | What changes |
|---|---|
| `Profile` model | Replace entirely with `Worker`. Same fields + additions. |
| `ProfileRepository` | Replace with `WorkerRepository`. Reads `current_staff` from `CardsApi`. |
| `ProfileNotifier` | Replace with `WorkerNotifier`. Watches `WorkerRepository`. |
| `ProfileEditScreen` | Replace with `WorkerEditScreen`. Same form structure; bind to `Worker`. Split `firstName`/`lastName`. |
| `ProfileFillFromLicenceScreen` | Rename to `WorkerFillFromLicenceScreen`. Update model binding. |
| `ProfileScreen` | Replace with `WorkerHomeScreen`. New layout with summary cards. |
| `CompleteProfileBanner` | Rename to `WorkerCompletenessBanner`. Update `isComplete` check to `Worker.isReadyForInduction`. |
| `ProfileFieldRow` | Generalise to `FieldRow` (already near-generic). |
| `CopyInductionBlock` | Update field binding from `Profile` to `Worker`. |
| `HomeShellScreen` | Update bottom nav to: Licences · Certs · Worker · Settings. (Tab 2 label changes from "Profile" to "Worker" or "Me".) |
| `LicenceRepository` | Rename `userId` → `staffId` in payload. Bind to `WorkerLicence`. |
| `LicencesListNotifier` | Update to watch `workerProvider` for staffId. |
| Onboarding flow | Add `WorkerTradesScreen` as step 2 (optional). |

### DROP

| Artefact | Why |
|---|---|
| `profile.dart` (model + freezed files) | Replaced by `worker.dart`. |
| `profile_repository.dart` | Replaced by `worker_repository.dart`. |
| `profile_notifier.dart` | Replaced by `worker_notifier.dart`. |
| Email OTP screens (if iframe-only decision confirmed) | Cards Unit 4 already dropped these conceptually; they remain as fallback. Royce calls if they should be fully removed. |
| `auth_repository.dart` email path (partial) | Only if email OTP is dropped. |

---

## 6. Phased Build Sequence

### Phase 0 — Pre-work (0.5 day, no user-visible change)

1. Add `worker.dart` model (freezed) alongside existing `profile.dart`. Do not remove `Profile` yet.
2. Extend `CardsApi` with `upsertMyWorker(payload)` — same shape as `upsertMyProfile` but column names match canonical `staff`.
3. Verify `currentStaff()` returns all fields the new `Worker` model needs. If not, update the `cards-api` Netlify function (eq-shell) to include missing columns.

**Shippable:** no UI change. Verify `Worker.fromJson` round-trips correctly against live `currentStaff()` response.

### Phase 1 — Worker record (MVP slice) (1.5 days)

1. `WorkerRepository` — wraps `CardsApi.currentStaff()` + `CardsApi.upsertMyWorker()`.
2. `WorkerNotifier` — Riverpod provider, replaces `profileNotifierProvider`.
3. `WorkerEditScreen` — rebuild of `ProfileEditScreen`. Split `fullName` field into `firstName` + `lastName` rows; add `preferredName` (optional). All other fields identical.
4. Update `AppRouter` redirect logic: replace `profileNotifierProvider` watch with `workerNotifierProvider`. Post-login destination changes from `/licences` to `/worker` (new `WorkerHomeScreen`).
5. `WorkerHomeScreen` (simple v1): worker name + role chip + "your wallet" section linking to `/licences`. No stats yet.
6. Update onboarding: `/onboarding/worker` points to `WorkerEditScreen` with `isOnboarding: true`.
7. Update `CompleteProfileBanner` → `WorkerCompletenessBanner`: bind to `Worker.isReadyForInduction`.

**Shippable:** worker can sign in, see `WorkerHomeScreen`, edit their canonical `staff` record, and have the completeness banner reflect live data. Licences/certs tabs unaffected — they still read from `WorkerLicence` (already live).

**Keep `Profile` model and repo in place** — remove after Phase 2 verifies nothing references it.

### Phase 2 — Model rename + binding update (1 day)

1. Rename `Licence` → `WorkerLicence`. Run `dart fix` across all callsites.
2. Rename `Certificate` → `WorkerCertificate`.
3. Update `LicenceRepository`, `LicencesListNotifier`, `LicenceEditScreen`, `LicenceDetailScreen`, `LicenceCard`, `ExpiryBadge` to use `WorkerLicence`.
4. Update `CertificateRepository`, `CertificatesListNotifier` to use `WorkerCertificate`.
5. Update `CopyInductionBlock` to bind to `Worker`.
6. Update `AlertsScheduler` to watch `workerLicencesNotifierProvider` (already watches `licencesListNotifierProvider` — rename only).
7. Delete `profile.dart`, `profile_repository.dart`, `profile_notifier.dart` (and freezed/g.dart generated files).
8. Run `flutter analyze` + `flutter test`. Must stay green.

**Shippable:** clean model surface. No user-visible change.

### Phase 3 — Worker Home enrichment (0.5 day)

1. `WorkerHomeScreen` v2: add licence wallet summary card (count by status: valid / expiring / expired), certificate count, Quick-action strip (Add licence, Copy induction block).
2. `WorkerCompletenessBanner` — move from Licences tab to Worker Home (currently on `LicencesListScreen` via `CompleteProfileBanner`; keep a compact version on licences too).
3. Update onboarding welcome copy: "Your employer invited you to EQ Cards" vs "Welcome to EQ Cards" (bind to `initialOrgNameProvider` as today, copy updated to say "set up your worker profile" not "set up your wallet").

**Shippable:** Worker Home feels like a real home screen, not a stub.

### Phase 4 — Trades + availability (0.5 day, optional for MVP)

1. `WorkerTradesScreen` — multi-select from licence type list. Writes `staff.trades` jsonb via `upsertMyWorker`.
2. Insert as Step 2 in onboarding wizard (after personal details, before Done).
3. Surface trades on `WorkerHomeScreen` as a compact chip row.

**Shippable:** Field can see worker's declared trades. Royce decides if this is MVP or Phase 4.

---

## 7. Integration Points

### 7.1 Shell auth (no change required)

`IframeHandoffScreen` already handles postMessage + hash fallback. The JWT carries `app_metadata.tenant_id`, `app_metadata.eq_role`, `staff_id` (if present in JWT claims). The worker-first rebuild consumes these the same way. No Shell changes needed.

### 7.2 `cards-api` Netlify function (minor extension)

Current ops: `current_staff`, `list_my_licences`, `upsert_my_licence`, `soft_delete_my_licence`, `upsert_my_profile`.

Worker-first needs:
- `current_staff` — verify it returns all `Worker` fields (firstName, lastName, preferredName, employmentType, etc.). Extend if needed.
- `upsert_my_worker` — new op (or rename `upsert_my_profile` to `upsert_my_worker` with broader column list). Writes `app_data.staff` columns.
- `list_my_licences` — unchanged.
- `upsert_my_licence` — unchanged.
- `soft_delete_my_licence` — unchanged.

The Netlify function extension is a 1-day task in `eq-shell`, separate from the Flutter rebuild. It must land before Phase 1 of the Flutter rebuild can ship.

### 7.3 Canonical handoff to Field

When a worker fills their profile in Cards and their `app_data.staff` record is updated, Field picks it up the next time it reads the roster (Field reads `app_data.staff` for its own tenant via the same canonical). No event or webhook needed — it is a shared DB row.

The worker-first rebuild makes this handoff accurate: `staff.first_name` / `staff.last_name` / `staff.mobile` / `staff.date_of_birth` written by Cards, read by Field. Today's shim writes back to `staff` indirectly via `upsert_my_profile` — the rebuild makes this direct and explicit.

### 7.4 Field consumption

Field reads `app_data.licences` to show a worker's tickets in the roster view (compliance check). This is already live post-canonical migration. Worker-first does not change the data; it makes the Flutter app aware that licences are associated with a `staff` record, not a freestanding user profile.

---

## 8. Open Product Decisions (Royce Must Call)

These are the questions the rebuild cannot resolve without Royce's input. Ordered by blocking impact.

### D1 — Certificates table: keep separate or merge into `app_data.licences`? (BLOCKING Phase 2)

**Context:** The current `Certificate` model writes to a `certificates` table in the now-read-only legacy Cards Supabase. Post-canonical migration, the plan was to store certificates as a `licence_type` subtype in `app_data.licences` (there are certificate types in the 13 seeded types: `first_aid`, `lv_cpr`, `working_at_heights`, `white_card`, etc.). But the Flutter app still has a separate `CertificateRepository` and a separate Certificates tab.

**Options:**
1. **(recommended) Merge into licences.** Drop the Certificates tab. Everything is a `WorkerLicence` — the `licenceType` distinguishes "card" (driver licence, electrical licence, white card) from "cert" (first aid, working at heights). One tab: "Wallet". One model. Reduces app surface area by ~30%.
2. **Keep separate.** Certificates stay as a separate entity. Requires a `certificates` table on canonical (not currently there). Requires a `list_my_certificates` / `upsert_my_certificate` op in `cards-api`. Adds ~1 day to the rebuild.
3. **Separate tab, same table.** Display them in two tabs but store in `app_data.licences`. The tab split is a UI filter on `certificateType` vs licence subtypes. Medium complexity.

**Recommendation:** Option 1 (merge). The distinction between "licence" and "certificate" is a UX label, not a data distinction — both have a type, a number/title, an issuer, an expiry, and a photo/file. The wallet concept covers both. Simplifies the canonical schema and the Flutter app.

### D2 — `WorkerTradesScreen` in MVP or Phase 4? (BLOCKING Phase 4 scope decision)

**Context:** Workers can declare their trade categories (which types of licences/tickets are relevant to them). This writes `staff.trades` jsonb. Useful for Field to filter the roster by trade. Not critical for the wallet or induction-copy use cases.

**Options:**
1. **(recommended) Phase 4 / post-MVP.** Workers can add licences directly; their trades are inferred from what they add. The explicit declaration is a nice-to-have for Field's roster filter.
2. **MVP (Phase 1).** Include as Step 2 of onboarding. Simplest form: a multi-select of the 13 licence type categories.

### D3 — Worker Home tab label: "Worker", "Me", or keep "Profile"? (UI copy)

**Context:** The bottom nav currently shows "Profile" for Tab 2. Worker-first makes the tab about the worker's canonical record, not a personal profile. 

**Options:**
1. **(recommended) "Me"** — Short, scan-friendly, common in mobile apps. Avoids jargon.
2. **"Worker"** — Accurate to the domain model. Slightly technical for the nav label.
3. **Keep "Profile"** — No nav change. Simplest.

### D4 — Email OTP fallback: keep or drop?

**Context:** Cards is shell-only post-Unit 4. The email OTP path (`/auth/email`, `/auth/otp`, `EmailEntryScreen`, `OtpScreen`) is a fallback for non-iframe access. Direct visits to `cards.eq.solutions` currently show an OTP sign-in or a "visit your portal" message.

**Options:**
1. **(recommended) Keep as fallback.** Costs nothing. Useful during dev (direct URL testing) and for native builds.
2. **Drop.** Remove `EmailEntryScreen` and `OtpScreen`. Direct visits redirect to `core.eq.solutions`. Cleaner app surface but removes the dev fallback.

### D5 — Worker availability: in Cards scope or Field-only?

**Context:** `app_data.staff` could carry an `availability` jsonb (which days/shifts a worker is available). Cards could let workers set their own availability. Field would then read it when building the roster.

**Options:**
1. **(recommended) Field-only for now.** Supervisors set availability in Field; workers don't self-manage it in Cards at MVP. Revisit if a worker requests it.
2. **Cards scope, Phase 4+.** Worker sets their own availability in Cards. Simple yes/no per day-of-week.

---

## 9. Keep vs Rebuild vs Drop — Summary Table

| Feature / file | Decision | Phase |
|---|---|---|
| `CardsApi` | Keep | - |
| `IframeHandoffScreen` | Keep | - |
| `AppRouter` | Keep skeleton; update destination + routes | Ph 1 |
| Token layer (EqSpacing/Typography/Colours/Radius) | Keep (A4 done) | - |
| Core widget library | Keep | - |
| `AlertsScheduler` | Keep; re-wire provider | Ph 2 |
| `AnalyticsService` | Keep | - |
| `Profile` model | **Drop** | Ph 2 |
| `ProfileRepository` | **Drop** | Ph 2 |
| `ProfileNotifier` | **Drop** | Ph 2 |
| `ProfileEditScreen` | **Rebuild** as `WorkerEditScreen` | Ph 1 |
| `ProfileFillFromLicenceScreen` | **Rebuild** as `WorkerFillFromLicenceScreen` | Ph 2 |
| `ProfileScreen` | **Rebuild** as `WorkerHomeScreen` | Ph 1 |
| `CompleteProfileBanner` | **Rebuild** as `WorkerCompletenessBanner` | Ph 1 |
| `CopyInductionBlock` | **Rebuild** (bind to `Worker`) | Ph 2 |
| `ProfileFieldRow` | Rename to `FieldRow`, keep | Ph 2 |
| `Licence` model | Keep; rename to `WorkerLicence` | Ph 2 |
| `LicenceRepository` | Keep; update staffId binding | Ph 2 |
| `LicencesListNotifier` | Keep; update provider watch | Ph 2 |
| Licence screens / widgets | Keep; update model binding | Ph 2 |
| `Certificate` model | **Merge into `WorkerLicence`** or keep (D1) | Ph 2 |
| `CertificateRepository` | Drop if D1=merge; keep if separate | Ph 2 |
| Certificate screens | Drop/merge if D1=merge; keep if separate | Ph 2 |
| `HomeShellScreen` (nav) | Keep; update Tab 2 label | Ph 1 |
| `OnboardingWelcome` | Keep; update copy | Ph 1 |
| `OnboardingDone` | Keep; update copy | Ph 1 |
| `WorkerTradesScreen` | New (D2) | Ph 4 |
| `SettingsScreen` | Keep | - |
| `ShareLicenceScreen` | Keep | - |
| Legal screens | Keep | - |
| PIN auth screens | Keep | - |
| Email OTP screens | Keep as fallback (D4) | - |

---

## 10. Design Constraints

All rebuilt / new screens conform to the EQ design profile:

- **Font:** Plus Jakarta Sans via `EqTypography.fontFamily`
- **Colours:** `EqColors.sky` / `EqColors.deep` / `EqColors.ice` / `EqColors.ink` — no raw hex
- **Spacing:** `EqSpacing.xs/sm/md/lg/xl/xxl` — no raw numbers
- **Radius:** `EqRadius.card` (8), `EqRadius.input` (6), `EqRadius.chip` (4) — no raw numbers
- **No shadows.** No gradients. Background: `EqColors.white` or `EqColors.ice`.
- **Linear/Notion aesthetic:** clean horizontal rules, ice fill on inputs, ink text on white surfaces.
- **Typography consolidation** (Path C from cards-token-consolidation-2026-05-30.md) deferred. Do not attempt during this rebuild.

`WorkerHomeScreen` layout target: plain list with a compact worker identity block at top, then a "Wallet" section heading and a count pill, then "Certificate" (or "All Docs") section. No cards-within-cards nesting.

---

## 11. Effort Estimate

| Phase | Effort | Blocker |
|---|---|---|
| Phase 0 — Pre-work | 0.5 day | Verify `cards-api` response shape |
| `cards-api` extension (eq-shell) | 0.5–1 day | Needs D1 decision on cert table |
| Phase 1 — Worker record (MVP) | 1.5 days | D3 (nav label, minor) |
| Phase 2 — Model rename + binding | 1 day | D1 decision |
| Phase 3 — Worker Home enrichment | 0.5 day | — |
| Phase 4 — Trades (optional) | 0.5 day | D2 decision |
| **Total MVP (Ph 0 + api + Ph 1 + Ph 2 + Ph 3)** | **~4.5 days** | D1 + D3 |
| **Total full** | **~5 days** | D1 + D2 + D3 |

---

## 12. Integration with Sprint Board

Per SPRINT-BOARD.md, E1 is `⚪ todo (unclaimed)`. When ready to start:

1. Update E1 row: `owner = <agent>`, `branch = claude/worker-first-rebuild`, status `🔵 in-progress`.
2. Branch from `origin/main` (eq-cards). Do not start from the existing `claude/canonical-migration` branch (it's the Unit 4 migration, already merged).
3. Phases 0 → 1 → 2 → 3 ship as separate PRs (not one giant PR). Each PR has a green `flutter analyze` + `flutter test` gate.
4. The `cards-api` extension (eq-shell) is a parallel track in eq-shell — it lands before or concurrent with Phase 1.
5. Per memory `feedback_shared_clone_git_guards`: branch from origin/main, stage explicitly, verify PR diff, gate on green. eq-cards has concurrent agent sessions active.

---

## 13. Related Files

- `C:\Projects\eq-cards\lib\` — Flutter source
- `C:\Projects\eq-context\eq\cards\canonical-migration\plan.md` — canonical migration (Units 1-5, mostly executed)
- `C:\Projects\eq-context\eq\identity\IDENTITY-MODEL.md` — 5-tier role model, JWT shape
- `C:\Projects\eq-context\eq\canonical-readiness\plan.md` — canonical entity inventory (app_data.staff, app_data.licences)
- `C:\Projects\eq-context\cards-token-consolidation-2026-05-30.md` — A4 token work (done) + Path C notes
- `C:\Projects\eq-context\design-audit-2026-05-30.md` — design token audit (Stream 1)
- `C:\Projects\eq-context\SPRINT-BOARD.md` — E1 board item
- `eq-shell/netlify/functions/cards-api.ts` — Netlify function to extend for `upsert_my_worker`

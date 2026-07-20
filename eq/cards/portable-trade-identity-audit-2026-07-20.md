---
title: EQ Cards — Portable Trade Identity Audit
owner: Royce Milmlow
last_updated: 2026-07-20
scope: Response to the "EQ Cards — From Credential Wallet to Portable Trade Identity" agent brief (2026-07-20). Current-state audit + design recommendation. No implementation performed — this is the required output before any build decision.
read_priority: critical
status: awaiting Royce's decision on recommended first slice
---

# EQ Cards — Portable Trade Identity Audit

Response to the agent brief delivered 2026-07-20 (`eq-cards-brief.pdf`). Primary repo `eq-cards`; investigation also touched `eq-shell`, `eq-field`, and live queries against eq-canonical (Supabase project `jvknxcmbtrfnxfrwfimn`). `sks-nsw-labour` was not touched. Every claim below was verified against live code and/or live data this session — none of it is carried over from older docs without a spot-check (one existing doc, the 2026-06-15 iframe ADR, was already found stale earlier today and corrected separately; the same discipline was applied here).

No implementation has been done. Per the brief's own instruction, this stops at the recommendation.

---

## 1. Current-state product and architecture map

**Identity — two parallel records, loosely bridged, no verification anywhere.**
`public.profiles` (self-service wallet identity, keyed 1:1 to `auth.users.id`) — 53 rows, patchy (47/53 have a name, 33/53 a DOB, 30/53 an email, 31/53 an address). One `full_name` field only — no legal-vs-preferred split. `public.workers` (admin-managed, 94 rows) does split `first_name`/`last_name`/`preferred_name`, and has a nullable `user_id` for pre-claim stub workers. The two are bridged only by `workers.user_id = auth.users.id` once a worker claims their record. No field on either table indicates a verified identity — phone-OTP at signup is the closest thing to verification, and it verifies contact-method control, not the name itself.

**Duplicate-identity handling — detects, never repairs.**
Two independent detectors: a phone-dedup trigger (migration `0040`, `shell_control.users` layer, auto-merges same-person GoTrue duplicates) and `identity_collision_flags` (added via `eq_cards_link_or_create_worker`, migration `0062`) which flags a cross-provider duplicate (e.g. Shell email invite vs Cards phone-OTP for the same human) but never merges — 0 live rows, so it's untested-by-volume. `eq-shell`'s `check-identity-collisions.ts` reads the same table daily and raises a Sentry alert for a human to reconcile manually — its own header states "ALERT-ONLY — this NEVER merges or deletes." There is no automated repair path anywhere in the suite for this class of duplicate.

**Credentials — three tables, one of them a fully-built but completely unused pipeline.**
`licences` (154 rows, worker-owned, free-text `licence_type`, `is_private`, `never_expires`, sparse `metadata` jsonb) and `certificates` (15 rows, simpler, no `is_private`/`metadata`) are the live wallet. A third table, `worker_credentials` (admin-side, keyed to `workers.id`, richer 30-value credential-type enum including a `status` enum of `active`/`expired`/`pending_renewal`, and a `promoted_licence_id` FK clearly designed to promote an admin-entered credential into the worker's own `licences` on claim) has **zero live rows**. The schema for exactly the "evidence strength" concept the brief asks for already exists and has never been used. No column anywhere (`licences`, `certificates`, `worker_credentials`) records verification source or confidence, despite OCR extraction existing as a separate, disconnected side-channel (`ocr_usage`, 116 calls logged, no link back to which licence row it touched).

**Company connections — two tracks, disconnect is correctly server-enforced today (after a real fix).**
Worker self-signup (`eq_cards_submit_access_request` → `org_access_requests`, pending/approved/declined/cancelled) and employer-initiated (`eq_cards_request_worker_access`) both resolve into `org_memberships` (`pending`/`active`/`revoked` — no separate "past relationship" state; the row persists with a status flip, not a delete). Live: 45 access requests (40 approved, 3 cancelled, 2 declined), 46 memberships (45 active, 1 revoked). Disconnect (`eq_cards_revoke_org_access`) originally (migration `0030`) only flipped the Shell-layer SSO membership and left `public.org_memberships` active — meaning a "disconnected" company kept real RLS read access to the worker's licences. Migration `0036` fixed this to also revoke `org_memberships`, which is what the RLS policy (`is_org_admin_of`) actually checks. This is now correct, but it shipped wrong first and was caught later — worth remembering, see risk #1 below.

**What a connected company can actually see — the one live gap that matters most.**
RLS on `licences`: `is_org_admin_of(user_id) OR user_id = auth.uid()`. **This policy does not filter on `is_private`.** `is_private` is only enforced in the public `share-licence` edge function (404s a private licence for an anonymous link). A worker who marks a licence private believing it's hidden from their employer is wrong — their connected org's admin can see it via the normal admin worker-detail screen. This is a live, unannounced gap between the product's implied promise and its actual behaviour.

**Worker-controlled sharing — real, but "controlled" overstates it.**
The public QR/link share (`share-licence` edge function) exposes exactly six fields (type, number, state, issuing authority, expiry, holder name) — no photos, DOB, or address — and correctly 404s if the licence is private. But there is no revoke mechanism: once shared, the link works forever (gated only by a 128-bit unguessable UUID) until the worker deletes the licence entirely; flipping `is_private` after the fact stops new fetches but doesn't invalidate anyone who already has the link. A full self-export (`data_export.dart`) does exist — profile + all licences + 1-hour signed photo URLs — satisfying the Privacy Policy's §9 access-rights promise.

**worker_house — narrower than its name suggests.**
Not a broad employer-facing aggregate. It's a thin credential-list data source feeding the expiry-alert scheduler only. The actual employer view of a worker's credentials is the direct `licences` RLS read described above (plus an empty `worker_credentials` panel, since that table has no data yet).

**Consent — real, but not versioned.**
`consent_gate.dart` gates on a single `profiles.consented_at` timestamp with no policy-version field. If the Privacy Policy changes, nobody who already consented is re-prompted — despite the Policy's own §13 promising re-notice for material changes.

**Deletion — the Policy overstates what the code does.**
Policy §8: "hard-deleted within 30 days." Code (`eq_cards_delete_account`): anonymizes the `profiles` row in place — nulls name/mobile/email/DOB/address/emergency contact, sets `deleted_at` — but the row is never actually removed (0 of 53 profiles currently have `deleted_at` set; no cron purges `profiles` at all). Licences *do* get hard-purged 30 days after soft-delete (a real cron, migration `0052`), but retain `licence_type`/`expiry_date` even in the interim "for org audit." `worker_credentials` (the org's own HR staging data) is explicitly untouched by design, matching the in-app disclosure.

**"Read audit" — corrects a standing memory note.** Migration `0054` (`eq_cards_log_read_event`) logs the *worker's own* actions (viewed/shared their own licence), not third-party access. There is no "who looked at my data" feature anywhere in the app. An earlier working note describing this as an access audit was wrong; corrected as part of this investigation.

**Notifications / passive expiry signal — already exists, don't rebuild.**
`_WalletHealthCard` + per-item `ExpiryBadge` already surface expiry urgency at the top of the main wallet screen (confirmed earlier this session — this is exactly the "you are ready, nothing needs your attention" default state the brief asks for in Phase 4). Real device-push notifications (`flutter_local_notifications`) are dead code on the only platform that ships (web-only, no native build pipeline) — email/SMS reminders cover reach today.

**Architecture — Cards already owns the substrate; this is not blocked by cross-app ownership.**
Worker identity/credential tables (`profiles`, `workers`, `licences`, `certificates`, `worker_credentials`, `identity_collision_flags`) all live in `public.*` on eq-canonical (`jvknxcmbtrfnxfrwfimn`) — Cards' own schema, a **different Supabase project** from the `app_data.*`-on-ehow rule that governs sites/customers/assets. Shell's role toward workers is auth/session/tenant-scope only, via `shell_control.*` on the same project — both the Shell-iframe path and Cards' native phone-OTP path resolve identity through the same `shell_control.users` table (confirmed live). Tenant isolation is enforced via the membership graph (`org_memberships` + `is_org_admin_of()`), not a raw `tenant_id` column on every table (Storage paths are the one place `tenant_id` is used directly, in the object key). `eq-field` reads eq-canonical directly through a server-side proxy (`canon-read.js`) with server-derived `org_id` — the client can't spoof it. **Conclusion: a portable identity does not require new cross-app plumbing. The data already lives in one place Cards controls.**

---

## 2. What already exists and must not be rebuilt

- The credential wallet itself — licence/certificate CRUD, OCR extraction, photo storage, expiry tracking.
- Company connection request/approval/revocation — both tracks, and disconnect is now correctly server-enforced.
- Public QR/link sharing with `is_private` gating (for the public-link case specifically — the employer-view gap is separate, see §1).
- Full self-export — data portability in the literal sense already exists as a manual export.
- The passive "you're ready" surface — `_WalletHealthCard` + `ExpiryBadge` on the main wallet screen. Do not build a second "alerts inbox" on top of this (this was nearly done in error earlier this session and caught by reading the actual code first).
- `required_by_org_strip` / `credential_gaps_repository` — already the "smallest useful question, framed as invitation not compliance" pattern the brief describes for Phase 3. Extend this, don't replace it.
- **`worker_credentials`** — schema for exactly the evidence-confidence tiering the brief asks for already exists, unused. This is the cheapest possible starting point for Phase 2/3 rather than a new table.
- Duplicate-identity detection (both layers) — extend the alerting, don't build a third detector.

---

## 3. The minimum portable-identity model

**Essential now**
- Legal name + preferred name on the *self-service* identity too (`profiles` currently has neither split — `workers` does). A worker who never had an admin pre-create them has no preferred-name field at all today.
- A single canonical identifier doctrine, not a new identifier. Recommend formally documenting `auth.users.id` (i.e. `profiles`) as canonical once claimed, with `workers` as the admin-side pre-claim shadow that resolves to it — this is close to the current behaviour already; it needs naming as doctrine, not rebuilding.
- Licences/certificates as they exist.
- **Evidence-confidence tiers** — the single biggest structural gap between "wallet" and "trusted identity." Every credential today carries equal weight regardless of whether it was OCR-extracted, hand-typed, or (hypothetically) admin-witnessed. Cheapest path: activate the dormant `worker_credentials.status`-style tiering, or a small enum on `licences` — self-declared / OCR-extracted / admin-confirmed / issuer-verified.
- Current company connections (exists).
- Worker-controlled sharing, but with a real revoke capability added — "controlled" currently only means "controls whether a *new* share can start," not "controls an existing share." That gap should close alongside any messaging that calls this "portable, worker-controlled" identity.
- **The `is_private` employer-view fix is a prerequisite, not a nice-to-have** — a portable identity built on a sharing model that already doesn't do what it says would be building trust on a broken promise.

**Useful later**
- Past company relationships surfaced positively to the worker (today only exists implicitly as a `revoked` status, never shown to the worker as "here's where you've worked").
- Inferred work exposure via the Phase 3 passive-evidence model — genuinely valuable, but the largest net-new build, and depends on roster/site/crew data that lives in `eq-field`, not `eq-cards`.
- Worker development interests.

**Dangerous or unnecessary right now**
- Anything that aggregates evidence into a score, ranking, or readiness percentage — the brief explicitly rules this out ("no hidden score"), and it's the natural failure mode of an evidence-confidence system if not deliberately constrained to per-credential labels only.
- "Readiness for a particular site/role" as a Cards feature — this is squarely resources/dispatch territory, which the suite's own architecture rule assigns to `eq-field` exclusively ("Resources, hours, availability, licences, dispatch, shutdowns → EQ Field only. Never rebuild these in another app."). If ever built, it belongs in Field, not Cards.
- A third worker identity model. Two (`profiles`/`workers`) already exist, barely reconciled. Consolidate toward one canonical doctrine — never add a third.

---

## 4. Three product paths

**A — Conservative (hardening only).** Fix the two live gaps found this session: employer-view `is_private` filtering, and the delete-account policy/code mismatch (either the Policy text or the code needs to change — Royce's call which direction). Add revoke-capability to sharing. No new "portable identity" concept surfaced to the worker yet. Single repo, but touches RLS and the consent/deletion path — both gated by the brief's own "stop before" list.

**B — Balanced (recommended).** Everything in A, plus: activate evidence-confidence tiers using the existing dormant schema, surfaced as a small badge on the existing licence card (not a new screen); consolidate the existing wallet + profile + connections screens into one coherent "My Trade Profile" surface per Phase 4 rather than adding new modules; and — per the brief's explicit instruction to recommend one compounding feature, not all three — the one recommended is the sharing/revoke improvement, since it's the smallest, most directly worker-empowering, and fixes a gap already found rather than speculating on a new one.

**C — Ambitious (defer).** The full passive-evidence + proposed-truth engine (Phase 3's four mechanisms) — inferring exposure from roster/site/crew activity. This needs `eq-field` data (crew, site, roster) that Cards doesn't hold, making it genuinely cross-repo, and needs new legal disclosures the org already knows it owes (APP 1.7 automated-decision-making update, flagged in the Policy itself as due before December 2026 — see §8). This is the "grand platform rewrite" the brief explicitly says not to do yet. Recommend deferring until Path B's evidence-tier foundation has shipped and is actually being used.

---

## 5. Trade-offs

| | Path A | Path B | Path C |
|---|---|---|---|
| Repos touched | eq-cards only | eq-cards only | eq-cards + eq-field (+ legal) |
| Needs Royce sign-off on | RLS policy change, consent/deletion flow | Same as A, plus new sharing permission | Auth-adjacent data sharing across repos, new legal disclosures |
| New legal exposure | Minimal (closing existing gaps reduces exposure) | Small — evidence-confidence labelling should be reviewed but doesn't claim new authority | Real — inferred-experience claims need new consent language, timed against an obligation already owed |
| User-visible change | None (fixes are invisible corrections) | Small, additive (a badge, a consolidated screen, a revoke button) | Large — a genuinely new capability the worker will notice and need to trust |
| Risk if skipped | Live privacy gap and a false Policy claim keep sitting there | Wallet stays a wallet — fine, but doesn't move toward the stated thesis | N/A — this is the "don't do it yet" option |

---

## 6. Recommended first slice

Matches the brief's own recommended-first-slice test almost exactly, because getting there means making an existing implicit promise actually true rather than building something new:

1. Fix the `is_private` gap so a connected company genuinely cannot see a licence the worker marked private (currently: `licences_read` RLS policy in Supabase).
2. Resolve the delete-account mismatch — either the Privacy Policy's "hard-deleted within 30 days" claim needs to become true in code, or the Policy needs to be corrected to describe the actual anonymize-in-place behaviour. Recommend the former if feasible (it's what a worker would reasonably expect), but this is a legal-risk call, not a technical one — flagging for Royce, not deciding here.
3. Add revoke capability to the public share link.
4. Add a 4-tier evidence-confidence label (self-declared / OCR-extracted / admin-confirmed / issuer-verified) to the existing `licences`/`worker_credentials` schema, surfaced as a small badge — no new screen.

After this slice, the brief's own success test — "a worker joins once, their identity resolves correctly, their licences are immediately available, and the correct company can see only the information needed to mobilise them" — becomes actually true, not just apparently true.

---

## 7. Affected repositories and likely files

**eq-cards only** for the recommended first slice:
- `supabase/migrations/` — new migration for the `is_private` RLS fix and the evidence-confidence column.
- `supabase/functions/share-licence/` and `share_licence_screen.dart` — revoke capability.
- `lib/features/settings/` (delete-account flow) — pending Royce's direction on §6.2.
- `lib/features/licences/presentation/widgets/expiry_badge.dart` and the licence card widgets — evidence-confidence badge.
- `assets/legal/privacy-policy.md` — if the Policy is corrected rather than the code.

No `eq-shell` or `eq-field` changes required for the recommended slice — confirmed by the architecture findings in §1. Path C, if ever pursued, would need `eq-field` (roster/site/crew data).

---

## 8. Privacy and legal questions (for an Australian privacy/technology lawyer — not decided here)

1. The Policy states accounts are "hard-deleted within 30 days"; the code anonymizes in place and never removes the row. Does the current code already breach the stated Policy, and does fixing the Policy text (rather than the code) create any retrospective exposure for the gap having existed?
2. Consent is not versioned — if the Policy changes materially, is the existing unversioned `consented_at` still valid consent under APP, or does it need active re-consent?
3. The Policy already flags an owed APP 1.7 automated-decision-making disclosure update (due before December 2026). Should the evidence-confidence tiering (Path B) and any future inferred-work-evidence feature (Path C) be bundled into that same update, or handled separately?
4. Labelling a credential "self-declared" vs "issuer-verified" — does this labelling itself create any new liability (e.g. implying EQ Solutions verified something it didn't, or conversely disclaiming responsibility for something a worker relied on)?
5. The public share link has no revoke/expiry mechanism today — once shared, it's accessible indefinitely via an unguessable URL. Does "worker-controlled sharing" as described in Terms §9 need clarifying language about what "control" actually covers (future access vs already-distributed links)?
6. Cross-company portability isn't addressed anywhere in the current Policy/Terms — if Path B/C ship, does the existing "sharing to one site/employer" framing in §9 need to become a distinct, separately-consented "portable identity" concept?
7. `worker_credentials` (an org's own HR data about a worker) is explicitly excluded from account deletion — is that boundary (employer's own records vs the worker's wallet) correctly and clearly stated to workers today?

---

## 9. Three-risk pre-mortem

1. **A fixed gap regresses silently.** The `org_memberships` revoke bug (disconnect not actually revoking RLS access) shipped once, was caught later, and got fixed — the exact same failure shape as the `is_private` gap found today (a control that exists in the UI/one code path but isn't enforced where it actually matters). The connections feature has zero automated test coverage (confirmed earlier this session). Recommend a regression test for both the disconnect-revocation and the `is_private` fix specifically, not just a manual check.
2. **Evidence-confidence tiers quietly become a score.** The brief explicitly forbids a hidden score or competency checklist. The natural next request, once tiers exist, will be "can we roll these up into a readiness percentage" — that's precisely the line the brief draws. Recommend documenting, as a hard rule alongside the feature itself, that tiers are per-credential display labels only and are never aggregated, summed, or exposed as a single number anywhere.
3. **"Portable" oversells what's actually true today.** Terms §9 already states that once a worker shares data, "the data is in the third party's hands, we have no control" — and an employer's own `worker_credentials` records survive a worker's account deletion by design. A worker told this is now a "portable trade identity" could reasonably expect more continuity and control than the system currently honestly provides. Recommend keeping any user-facing language for Path B precise about what actually persists and what doesn't, rather than adopting the "portable identity" framing externally before the gaps in §1/§6 are closed.

---

## 10. Definition of done (for the recommended first slice)

- A connected company's admin view cannot render a licence where `is_private = true` (verified by a real query as an org-admin role, not just a UI check).
- The delete-account behaviour and the Privacy Policy's description of it match each other exactly — whichever direction Royce decides.
- A worker can revoke a previously-shared public licence link, and a revoked link stops resolving.
- Every licence/credential shows a confidence label pulled from real data (not a placeholder), covering all 154 live licence rows without requiring backfill guesswork — self-declared as the default for anything with no other signal.
- No aggregate score, percentage, or ranking exists anywhere in the new UI.
- Regression tests exist for the `is_private` fix and the disconnect-revocation behaviour.
- Nothing above required a schema change to `profiles`/`workers` identity model, a new identity table, or any `eq-shell`/`eq-field` change — if any of those turn out to be necessary, that's a sign the slice grew past what was scoped here and needs a fresh stop-and-check.

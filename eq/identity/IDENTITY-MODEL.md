---
title: EQ Solutions — Unified Identity & Permissions Model
owner: Royce Milmlow
last_updated: 2026-08-24
scope: Authoritative cross-product reference. Every present and future EQ Solutions product (Field, Quotes, Cards, Service, Intake, Tender Pipeline, anything that follows) conforms to this model. Governs the 5-tier role system, the platform-admin escape hatch, naming conventions for roles and permission keys, the invite flow, session lifecycle, the JWT shape that lets modules talk directly to Supabase, and (§3.3) identity data ownership between the control layer and tenant planes.
read_priority: critical
status: live
---

# EQ Solutions — Unified Identity & Permissions Model

**Status:** Live v1, 2026-05-20. (Promoted from Draft when Phase 1.F shipped — see commit history on `claude/phase-1f-identity-foundation`.)

**Tenant slug update 2026-06-29:** EQ Solutions company tenant slug renamed from `core` to `eq` (jvkn `shell_control.tenants`). Shell and Service now agree on `eq`. Any reference to Shell slug `core` for the EQ Solutions tenant is stale. Worker identity anchors (Cards stubs with no Shell credentials) remain in `shell_control.users` but are excluded from the admin users RPC by `email IS NOT NULL` filter.

**Correction 2026-07-30 (live-verified against jvknxcmbtrfnxfrwfimn):** the line above previously read "`__personal__` ghost tenant retired — all users homed in their primary employer tenant." That is false — retracted, not just stale. Live query of `shell_control.user_tenant_memberships` found 47 active rows against the `__personal__` tenant, created continuously through 2026-07-29 (the day before this correction), several tied to real named SKS employees. What actually happened 2026-06-28 was narrower: the `shell_control.tenants` row for `__personal__` was set `active=false`, which only removes it from admin/audit sweeps that filter `is_personal=false` (`eq-shell/netlify/functions/check-duplicate-shell-accounts.ts`, `check-dangling-staff-pointers.ts`, `licence-expiry-scheduler.ts`). It never stopped new memberships.
`__personal__` is in fact a permanent, deliberate architectural feature, not a retired one: eq-cards' "Policy 1" (`supabase/migrations/0038_claim_invite_personal_tenant.sql`, decided 2026-06-17, live unchanged in the current `eq_cards_claim_invite`/`eq_cards_auto_provision` bodies through migration `0072`/`0076` as of 2026-07-27) makes `__personal__` the permanent **home** tenant for every Cards worker — the claiming org's tenant is added additively via a second active membership row + `last_active_tenant_id`, never replacing the personal one. Of the 47 live rows: 40 also hold exactly one active org membership (expected dual-membership under Policy 1), 6 hold only the personal membership (Cards signups that never claimed an org), 1 (a platform admin) holds 3 others.
Net: this doc's own §11.2 backlog item ("Multi-tenant membership... v2 candidate... not yet built") is itself stale — eq-cards has shipped exactly that (one user, two simultaneous active tenant memberships) since 2026-06-17. Treat §11.2's "not yet built" framing as unverified against eq-cards until someone reconciles the two.
**Resolved 2026-07-30 (Royce) — see §11.3 below.** Cards is the personal identity/control layer: every person gets one Cards identity they own, and tenant membership is additive and optional on top of it — a user may hold active membership in more than one tenant at once by choice. This formally supersedes §11 item 2's original "one user, one tenant" decision.
**Correction 2026-08-23 (Royce's ratification, live-verified against jvkn + ehow + zaap):** this document had **no statement of identity data ownership** — and §3.2 actively asserted the opposite of the built system, calling operational person records "independent and managed per-module." Retracted; see §3.2's inline note and the new **§3.3**. The rule is now recorded: **the control layer (`jvkn`) wins on who a person is; a tenant plane reflects that and owns only the employment relationship.** This was the design intent all along — the reflection machinery implementing it (trigger → signed webhook → edge function, plus a nightly reconcile and dead-letter ledger) has been running in production since 2026-07-24 but was built directly in the database and codified only afterwards, so no repo and no doc described it. A session on 2026-08-23 read this file, concluded from §3.2 that nothing had been built, and began scoping a replacement before the live system was checked. §3.3 exists so that cannot recur.

**Implementation owner (shell side):** see [eq/identity/PHASE-1F-PLAN.md](./PHASE-1F-PLAN.md).
**Scope:** Authoritative reference for every present and future EQ Solutions product (Field, Quotes, Cards, Service, Intake, Tender Pipeline, and anything that follows). Every new module shipped under the EQ shell must conform to this document.

---

## 1. The principle in one sentence

A user signs in once at `<tenant>.eq.solutions`. From that moment, their identity — who they are, what role they hold, what modules they can touch — is **the same across every EQ product** for the life of that session.

## 2. Why this exists

The SaaS stack EQ is positioning against treats permissions as a per-app problem. SharePoint has one model. Simpro has another. Every bespoke tool has a third. The same human ends up with different access in each, naming conventions don't line up between products, and admins can't reason about access in one place.

By owning the shell across every EQ product, we offer a **single unified identity layer**:

- One login. One session. One role.
- `supervisor` means the same thing in Quotes as it does in Field.
- A permission key like `cards.issue` is structurally the same as `quotes.approve` — readable, predictable, auditable.
- An admin invites a user once with the right role; the user has consistent access everywhere from day one.

This consistency is itself a product feature.

## 3. The five tiers

| # | Role key | Label | Business meaning |
|---|---|---|---|
| 1 | `manager` | Manager | Tenant owner. Full control of the tenant's data, users, and module entitlements. Typically the business owner or operations lead. |
| 2 | `supervisor` | Supervisor | Team-level operations. Approves work, reviews team output, manages day-to-day for a group of employees. |
| 3 | `employee` | Employee | Default working role. Performs their assigned work in each module. Reads what they need, writes their own contributions. |
| 4 | `apprentice` | Apprentice | Employee-equivalent baseline, with apprentice-specific tooling (training records, mentor visibility). Limited write scope on commercial data. |
| 5 | `labour_hire` | Labour Hire | Minimal access. Sees their own roster, submits their own timesheet, nothing else. Treated as transient by default. |

Roles are **ordered** for readability but enforcement is **not** inheritance-based. A manager only "has" everything because the permission matrix lists everything against `manager`, not because of an implicit "manager inherits supervisor inherits employee" rule. This keeps every permission decision explicit and auditable.

### 3.1 Platform admin (orthogonal)

`users.is_platform_admin: boolean` — separate boolean alongside the role. When true, the user is EQ Solutions internal staff with cross-tenant access. The shell's `useCan()` helper short-circuits to `true` for any permission key when this is set. Single audit point for "this user can do this across every tenant."

Examples of who gets `is_platform_admin = true`: EQ Solutions support staff troubleshooting a customer issue, EQ Solutions ops staff doing onboarding, Royce.

`is_platform_admin` does **not** replace the role. A platform admin still has a role (typically `manager`) — the boolean is layered on top.

### 3.2 The auth entity vs the operational entity

Role lives on **`users`** — the auth entity (someone who logs in via `shell-login`). Operational entities like **`staff`** (a tradie working on a site, holding qualifications, appearing on rosters), **`people`** in EQ Field's legacy model, or any other person-shaped record in a module's domain, are *separate tables*.

A `user` row may correspond to a `staff` row via a `staff.user_id` FK when the person is both an authenticated user **and** an operational worker. But:

- Not every `staff` is a `user`. A labour_hire person captured for a project might never log into the shell — they exist as a `staff` row only.
- Not every `user` is `staff`. A `manager` who only configures things and never appears on a roster exists as a `user` row only.

The role + permission system gates **what the logged-in `user` can do**. When the two are linked (one human is both), `staff.user_id` is the join.

> **Correction 2026-08-23 (live-verified against jvknxcmbtrfnxfrwfimn + ehowgjardagevnrluult).** This section previously ended: *"The data model around `staff` and other operational entities is independent and managed per-module against `eq-canonical`."* **That is retracted, not merely stale.** It was never true of the built system, and reading it caused a session to conclude that no identity reflection existed and to begin scoping a replacement for machinery that has been running in production for a month. Operational person records are **not** independent per-module. `jvkn` is the control layer of identity truth; tenant planes hold a reflection of it. See §3.3.

### 3.3 Identity ownership — who wins when two copies disagree

**The rule: the control layer wins.** `jvkn` (`eq-canonical`) owns who a person *is*. A tenant data plane (`ehow`, `zaap`) holds a **reflection** of that, plus the facts that belong to that employer alone. A tenant never owns a person's identity; it owns the employment relationship.

| Fact | Owner | Truth lives in | Tenant plane may |
|---|---|---|---|
| Who the person is — name, DOB, contact details, address, emergency contact | The worker | `jvkn.public.workers` (fed by `jvkn.public.profiles` from Cards) | **read** — and propose a correction upward |
| What they hold — licences, credentials | The worker | `jvkn.public.licences` | **read** |
| Their relationship to *this* employer — `on_roster`, `employment_type`, `agency`, `job_title`, supervisor flags, crew membership, rostering, timesheets | The employer | tenant `app_data.*` | **write** — authoritative, never overwritten by canonical |

Two conditions make this rule workable rather than merely declarative. Both are load-bearing:

1. **The upward correction path must be complete.** When an operator corrects a person's details in Shell, that correction must reach `jvkn`, not just the local copy — otherwise "the control layer wins" degrades into "operators cannot fix anything."

   **Audited 2026-08-23 — the path is INCOMPLETE. One confirmed gap:**

   | Operator surface | Writes identity to tenant | Writes upward to jvkn | Sets lock |
   |---|---|---|---|
   | `entity-patch.ts` — edit an existing person | yes | **yes** (`email`/`phone` → `public.workers` since 2026-08-18; `name` → `shell_control.users` since 2026-08-23) | yes |
   | `staff-create.ts` — add a person to the roster | yes — `email`/`phone` on **both** the insert branch (L183-195) and the reactivate-in-place branch (L152-168) | **no** | no |

   `staff-create.ts` was therefore a one-way leak into the tenant plane: an operator adds someone, types their contact details, and canonical never learns them. This is the mechanism that produces null-`email` rows on `public.workers` for people whose employer plainly holds an address — 8 such rows were found and hand-backfilled on 2026-08-23. Not immediately destructive (the edge function's unlocked merge is fill-if-missing, so the tenant value survives the next sync) but it guarantees canonical drifts stale, which is the precise failure this rule exists to prevent.

   **CLOSED 2026-08-23 — eq-shell PR #1544.** `staff-create.ts`'s reactivate-in-place branch now mirrors `entity-patch.ts`'s upward write. Its insert branch deliberately does **not** push: a genuinely new person has no `public.workers` row to update, and minting one there is the duplicate-identity hazard that produced the Phoenix Khatri duplicate (2026-07-05). Canonical identity is created by the Cards claim/approval path, which matches on normalised phone + email before inserting; `workers-canonical-sync`'s `findStaffId()` then adopts the waiting tenant row. **A Shell-created person existing only on the tenant plane until they go through Cards is a known and accepted state, not a leak** — but it does mean §3.3's first row ("who the person is → owned by the worker, truth in jvkn") is aspirational for that person until their canonical record exists.

   **New convention, set by the same PR:** an upward write is the *substitute* for a lock, not a companion to it. `staff-create.ts` writes the operator's value to canonical and deliberately sets **no** lock — having made canonical agree, there is no disagreement left to freeze. Compare `entity-patch.ts`, which still sets one; there the lock is defensible as a safety net for its own best-effort upward write failing. Prefer correcting the source over fencing off the copy.

   **Audit completed 2026-08-23 — every remaining candidate traced to source, live catalog queried (not just code).** The 2-row table above covered 2 of ~20 candidate eq-shell functions; this pass closed the rest, plus the DB-side surface a code grep can't see at all (§3.3.1 already flagged this as unaudited). Full table:

   | Surface | Plane | Writes identity? | Upward to jvkn? | Sets lock? | Conforms? |
   |---|---|---|---|---|---|
   | `entity-patch.ts` | eq-shell | email/phone/name (yes); **date_of_birth/address_\* — no path, own comment admitted it** | partial | email/phone locks only | ⚠️ was gap, **closed 2026-08-23** (below) |
   | `staff-create.ts` | eq-shell | email/phone (reactivate branch) | yes | no (by design) | ✅ (PR #1544) |
   | `worker-profile-push.ts` | eq-shell | email/phone/name, jvkn-internal | N/A (already at jvkn) | reads, doesn't set | ✅ (PR #1544) |
   | `cards-approve-staff.ts` | eq-shell + tenant | full identity **only when seeding a brand-new stub from canonical**; never overwrites an existing stub's identity fields | N/A (correct direction — seeds tenant from canonical) | no | ✅ conforms |
   | `shell-login-phone-otp.ts` | eq-shell, jvkn-internal (3 self-heal paths) | name/email/phone, sourced from jvkn's own records | N/A | no | ✅ conforms |
   | `staff-licence-backfill.ts` | eq-shell → jvkn `public.licences` | credentials only, written to jvkn directly | N/A | no | ✅ conforms |
   | `staff-resync-licences.ts`, `licence-push.ts` | eq-shell → tenant | credentials only, one-way jvkn→tenant mirror | N/A | no | ✅ conforms |
   | `licence-ocr-commit.ts` | eq-shell → jvkn + tenant mirror | DOB fill-if-missing written to jvkn first | N/A | no | ✅ conforms |
   | `staff-record-licence-review.ts` | eq-shell, jvkn `cards_field_approvals` | review metadata only, no identity content | N/A | no | ✅ conforms (out of scope — not identity) |
   | `staff-teams.ts` | eq-shell → tenant | crew/team structure — employer-owned | N/A | no | ✅ textbook employer-owned case |
   | `backfill-worker-links.ts` | eq-shell | link/FK columns only, no identity content | N/A | no | ✅ not in scope (link resolution, not content) |
   | `delete-user.ts` | eq-shell, jvkn DELETE | blocks the delete while any tenant employment link still exists | N/A | N/A | ✅ clean example |
   | `push-document-audience.ts`, `comms-jobs.ts` | eq-shell | none — matched the original `from('staff')` grep on an unrelated SELECT | N/A | N/A | false positives, not writers |
   | `app_data.field_people_iud()` (INSTEAD OF trigger) | **ehow only — does not exist on zaap** | first_name/last_name/email/phone/date_of_birth/emergency_contact_name, full UPDATE | **no — none** | N/A | ❌ **new gap, biggest finding — fix built** (below) |
   | `sync_staff_to_field()` (AFTER trigger) | ehow only | mirrors `app_data.staff` into a second local table, `public.people` | N/A — tenant-internal | N/A | not a §3.3 violation, but an unexplained second copy; purpose/live-reader unconfirmed |
   | `eq_cards_upsert_my_profile`/`eq_cards_upsert_my_licence` + 3 siblings | ehow **and** zaap | would write full identity bypassing jvkn entirely if called | N/A (would bypass, not just fail to push) | no | inert — confirmed `service_role`-only on both planes, no caller found in eq-shell/eq-cards source; almost certainly a pre-canonical-Cards fossil, cleanup candidate not a live risk |
   | `eq_update_staff()` | ehow | name/email/phone/trade/level/employment_type | yes | no | already remediated by eq-shell itself (0172 fixed a clobber bug, 0245 revoked down to service_role-only) — closed loop |
   | Hygiene triggers (`audit_staff_*`, `staff_normalise_phones`, `staff_normalise_employment_type`, `staff_derive_dob_from_cards`, `staff_guard_reactivation`, `staff_stamp_deactivated_at`, `staff_touch_updated_at`, `field_people_removed_iud`, `field_people_worker_id_iu`, `field_team_members_iud`, `field_team_supervisors_iud`, `eq_leaver_retention_run`, `eq_archive_duplicate_record`) | ehow (+zaap where checked) | various, none touch cross-plane identity ownership | N/A | N/A | ✅ conform |

   Confirmed previously (not re-audited): `labour-hire-candidate-review.ts` + all `labour-hire-*.ts` (read-only), `workers-canonical-sync` (eq-cards, §3.3.1/§3.3.2 above).

   **Two real gaps found, both fixed same session (not yet merged/deployed):**
   - `entity-patch.ts`'s `date_of_birth`/`address_*` gap closed by extending its existing email/phone canonical-sync block — eq-shell [PR #1555](https://github.com/eq-solutions/eq-shell/pull/1555).
   - `field_people_iud()` (Field's own Add Person/Edit Roster write path on ehow) had **zero** upward path — the same class of gap PR #1544 closed twice for Shell, never audited for Field's DB-side write because it's invisible to a code grep. Fix mirrors `sync_worker_to_canonical()`'s own jvkn→edge-function pattern, reversed: a vault secret + `net.http_post` from the trigger to a new eq-shell endpoint, `field-identity-push.ts` (Field has no Netlify function in its own write path to piggyback on). eq-field [PR #761](https://github.com/eq-solutions/eq-field/pull/761) (trigger) + eq-shell PR #1555, second commit (receiver). **Inert until two secrets are created out-of-band** (`field_identity_push_secret` on ehow's vault, `FIELD_IDENTITY_PUSH_SECRET` on eq-shell's Netlify env) — deliberately not done yet, needs explicit go, same posture as every other jvkn-identity-adjacent change.

2. **A disagreement lock is a transient signal, not an ownership claim.** `app_data.staff.{email,phone,employment_type}_locked_by_shell` (tenant migrations `0224`/`0255`) freeze a local value so a nightly resync cannot flip-flop it. That is a **holding pen** — it prevents oscillation, it never resolves anything. Resolution always means correcting `jvkn`. A lock should therefore be visible as a worklist and should clear once canonical agrees.

**Evidence the rule was affordable, and the cleanup that followed (live, 2026-08-23):** all 22 `email_locked_by_shell` rows on `ehow` held a value **identical to** `jvkn.public.workers.email` — zero live divergence to arbitrate. Verified rigorously before acting: email compared case-insensitively, phone compared on **normalised** form via `shell_control.normalise_au_phone` (a raw string compare would have manufactured false conflicts, since jvkn was not yet normalised). 13 of the 22 locked a personal address canonical already agreed with — the lock fires whenever an operator touches the field, including merely to fill a blank, so it is **not** a deliberate ownership assertion — and those 13 permanently prevented that worker from ever updating their own address at that employer. The single genuine conflict the lock model was built for (Ben Ritchie, 2026-07-28) was resolved on 2026-08-23 by correcting `jvkn`, which is exactly what this rule prescribes.

**All 22 contact locks were cleared on 2026-08-23** (`email_locked_by_shell` and `phone_locked_by_shell` → `false` for every active `ehow` staff row; 22 → 0), on the strength of that verification. Under this rule a lock over a value canonical already agrees with protects nothing and only blocks the worker.

**Structural fix built 2026-08-23, not yet merged/deployed.** `employment_type` is an **employer-owned** field by the table above, so canonical should never move it — but `workers-canonical-sync` derived it from `jvkn.workers.role` and overwrote it on every merge unless locked (`employment_type_locked_by_shell`), the lock compensating for a sync reaching into a field it never owned. eq-cards [PR #293](https://github.com/eq-solutions/eq-cards/pull/293) stops the merge path writing the column at all — same treatment `field_approved`/`active` already got in this exact function — while still setting a sensible default on genuine INSERT (nothing to protect on a brand-new row). `employment_type_locked_by_shell` and `entity-patch.ts`'s write to it are left in place, now permanently inert once this ships: a lock over a field nothing overwrites just never fires, and removing them is a separate, no-op-risk cleanup this pass didn't need.

**Explicitly not adopted:** a separate employer-owned `work_email` column. The work-vs-personal split that would justify it does not exist in live data — all 9 work-domain locks match canonical, which already holds the work address for those people.

#### 3.3.1 How the reflection actually runs

Named here because it was built directly in the database and retro-codified a month later (`eq-shell/supabase/migrations/2026_07_24_reconcile_worker_sync_codify.sql`), which is why it is invisible from the repos and absent from this document until now.

- `jvkn.public.workers` carries an AFTER INSERT/UPDATE/DELETE trigger `worker_canonical_sync` → `sync_worker_to_canonical()` → signed `pg_net` webhook → Supabase **edge function `workers-canonical-sync`** (sourced in **eq-cards**, deployed on jvkn) → writes `ehow.app_data.staff` with the ehow service-role key. It honours the provenance locks above, matches identity by `cards_worker_id` → `user_id` → normalised phone → email, adopts dangling links, and diffs before writing.
- `pg_cron` `reconcile-worker-sync` (02:35 UTC) → `eq_reconcile_worker_sync()` re-projects the full set nightly; `audit-worker-sync-dispatch` (02:50) writes a dead-letter ledger to `worker_sync_dispatch`. A licence twin runs at 03:05/03:20.
- The reverse leg — Cards profile save → `app_data.staff` — is `eq-shell/netlify/functions/worker-profile-push.ts`.

**Known limits, not yet closed:**
- `workers-canonical-sync` **hardcodes** `EHOW_URL` and `SKS_TENANT_ID`. "The control layer is identity truth" is therefore true for exactly one tenant today and cannot onboard a second without a change. `worker-profile-push.ts` already demonstrates the right shape (`getTenantDataClientById` over active memberships).

  > ⚠️ **This is not merely a scaling limit — it actively mis-files people, demonstrated live 2026-08-23.** Because the tenant is hardcoded, `workers-canonical-sync`'s INSERT branch puts **any** jvkn worker with no matching SKS staff row onto **SKS's roster**, regardless of who they actually are. Applying `2026_08_23e`'s phone backfill fired the `worker_canonical_sync` trigger for 65 changed rows; one of them (worker `9043532b`, a Cards user with a login and **zero** `org_memberships`, unrelated to SKS) had no SKS staff row, so the sync created one — active, `field_approved = true`, on-roster — and it appeared immediately in SKS's Field Contacts and roster. Reverted the same session (`2026_08_23f`), zero dependent records, ~10 minutes exposure.
  >
  > **Why this had never happened before, and why that is load-bearing:** the nightly reconcile (`eq_reconcile_worker_sync`) is scoped `where staff_id is not null` — it only ever re-projects *already-linked* workers, so it structurally cannot insert a stranger. The **trigger** has no such scoping and fires on every worker UPDATE. The safety everyone had been relying on lives in the cron's WHERE clause, not in the sync itself.
  >
  > **Consequence for anyone doing bulk work on `public.workers`:** any mass UPDATE will insert every unlinked worker into SKS. 39 of 105 workers currently have no active SKS membership. Treat a bulk write to that table as a roster-modifying operation until the tenant is resolved per-worker from `org_memberships`.

- **`worker_canonical_sync`'s AFTER-trigger fan-out is not a read-only projection.** It can INSERT (above), so "the receiving function is idempotent and diffs before writing" — true of its merge path — must not be used to argue a fan-out is harmless. Verify what an unmatched row would do before triggering one at scale.

#### 3.3.2 Why the hardcoded tenant cannot be fixed by a lookup (audited 2026-08-23)

The obvious remedy for the hardcoded `SKS_TENANT_ID` is "resolve the tenant from the worker's org instead." **That is not currently possible: at the instant the sync runs, no tenant linkage for that worker exists in any table.** Established by tracing the two most recent genuine labour-hire onboards end to end.

**Who actually creates the staff row — settled from code, not timing.** `labour-hire-candidate-review.ts` contains **zero** writes to `app_data.staff`. Its RPC `eq_ops_review_labour_hire_candidate` does not create the worker either — its own comment states it links *"the pre-created stub worker by exact id (no phone/email matching involved)"*. None of the 22 `labour-hire-*` Netlify functions INSERT into `public.workers` or `app_data.staff`; all are reads. The `workers` INSERT happens at **intake** (via one of `eq_cards_admin_upsert_worker` / `eq_cards_find_or_create_worker_for_invite` / `eq_cards_link_or_create_worker` — the only three functions on jvkn that insert into that table), which fires `worker_canonical_sync` with `TG_OP = 'INSERT'`, and **the edge function's insert branch creates the staff row.**

**Therefore: deleting the insert branch would break labour-hire onboarding.** It is not dead weight. (Note it is not the *only* creator — `cards-approve-staff.ts` writes `app_data.staff` directly for the Cards approval path — but it is the sole creator for the labour-hire/stub-worker path.)

**The ordering problem, which is the real blocker:**

| Event | Conor Horgan | Nelson Sareto |
|---|---|---|
| `public.workers` row created (intake) | `22:55:42.836` | `22:56:07.369` |
| **`app_data.staff` row created (this sync)** | `22:55:43.153` | `22:56:07.620` |
| `public.labour_hire_candidates` row created | `22:55:48.484` | `22:56:12.379` |
| `public.worker_invites` row created | later, at approval | later, at approval |
| `public.org_memberships` row | **never** (both `user_id IS NULL`) | **never** |

The candidate row — the **first** record anywhere naming the org — lands ~5 seconds *after* the staff row already exists. So every candidate lookup source is written after the fact: `org_memberships` (absent entirely here, and separately proven unreliable — see §3.3.1's note on the 5 login-holders without SKS membership, three of them real SKS staff), `labour_hire_candidates`, and `worker_invites` alike.

**Consequence:** the hardcoded constant is not laziness — it is currently the only thing that answers a question the data cannot yet answer. It is also why this is **actively wrong the moment a second tenant exists**: every intake, for any customer, would file the person onto SKS.

**De-hardcoding therefore requires a design change, not a substitution.** Three viable shapes were on the table:
1. **Carry the tenant with the event** — intake knows the org; put it on the worker row (a nullable `origin_org_id`) or into the webhook payload, so the sync is told rather than guessing.
2. **Reorder** — write the candidate/invite link *before* the `workers` INSERT, making a lookup genuinely possible.
3. **Move creation** — have intake create the staff row itself (as `cards-approve-staff.ts` already does for its path) and retire the sync's insert branch.

**Shape 1 chosen and built 2026-08-23, not yet merged/deployed.** `public.workers` gains a nullable `origin_org_id`, stamped by `labour-hire-candidate-intake` — the exact intake path behind the Conor Horgan/Nelson Sareto incident above, which already resolves `orgId` before creating the worker row. `workers-canonical-sync`'s INSERT branch now refuses to create a staff row when a stamped `origin_org_id` names a non-SKS org; unstamped rows (self-signup, invite-claim, `eq_cards_admin_upsert_worker`, anything pre-existing) keep today's behaviour and still file onto SKS, since it's the only real destination that exists. eq-cards [PR #293](https://github.com/eq-solutions/eq-cards/pull/293). This makes the hardcode **safe**, not gone — a second tenant still needs its own destination (URL + service-role key) wired in when one actually exists, which stays real, deliberately deferred future work, not solved here. `eq_cards_find_or_create_worker_for_invite`/`eq_cards_link_or_create_worker`/`eq_cards_admin_upsert_worker` deliberately not wired to stamp it in this pass — see the migration's own comment for why each was left alone.

Until every intake path stamps it (or a second tenant's own destination is wired in), treat `workers-canonical-sync` as **still effectively single-tenant**, and treat any bulk write to `public.workers` as a roster-modifying operation (§3.3.1).
- `eq-field/scripts/people-canonical-link.js` attempts to create canonical worker stubs **directly from the browser using jvkn's anon key**. `anon` holds no privilege on `public.workers`, so every call 401s and is silently swallowed — it fails closed and is not a live exposure, but it is dead code whose silent failure masks itself. Either give it a server-side path or delete it.
- `postgres_fdw` was evaluated for this seam and **deliberately rejected** (it would place jvkn credentials inside a tenant DB) — see `eq/identity/service-canonical-identity-seam-2026-06-25.md`. Do not reach for it.

#### 3.3.3 Shared DB objects — functions two pipelines can both fully replace

**Registry, verified live 2026-08-24.** A handful of `app_data` functions on ehow are created and edited by BOTH eq-field's own hand-applied `supabase/migrations/*.sql` AND eq-shell's governed One Pipe (`tenant-migrate.yml` → `supabase/tenant-migrations/*.sql`). This table is the source of truth for that list — eq-shell's CLAUDE.md and eq-field's CLAUDE.md both reference it rather than restating it; keep any copy there in sync with this one, not the reverse.

| Function | Plane | Why both repos touch it |
|---|---|---|
| `field_people_iud` | ehow only | INSTEAD OF trigger behind Field's Add Person/Edit Roster — eq-field owns the tenant-side permission gates (licence/agency/hire_company/rating/active/field_approved/user_id), eq-shell owns the upward identity push (§3.3 above) |
| `field_people_removed_iud` | ehow only | Twin trigger for the archived/removed roster (Restore, hard-delete) |
| `field_teams_iud`, `field_team_members_iud`, `field_team_supervisors_iud` | ehow only | Crew-scoping write path (eq-field feature); zaap has no `app_data.teams` at all |
| `eq__guard_timesheet_status`, `eq__guard_leave_status` | ehow only | Status-transition gates on timesheets/leave |

**The mechanism.** Postgres has no partial-body `ALTER FUNCTION` — every touch to any of these is a full `CREATE OR REPLACE FUNCTION`, so whichever pipeline applies last silently wins. The two pipelines don't even share a ledger: eq-field's hand-applied migrations land in the standard `supabase_migrations.schema_migrations`; eq-shell's One Pipe writes its own `app_data._eq_migrations`. Neither pipeline's tooling reads the other's.

**Confirmed to happen for real, 2026-08-23/24.** eq-field PR #761 added the upward-identity-push block to `field_people_iud()` (§3.3 above), merged 09:33 UTC. eq-shell's `0270`/`0271` (a P0 trigger-reattach recovery + 3 permission gates, unrelated in intent, same day) independently rebuilt the same function from the pre-push baseline at 08:35–08:52 UTC — before PR #761 merged, so this wasn't even a live clobber, just two pipelines converging on the same object with zero visibility into each other. PR #761's migration then sat merged-but-never-applied, stale, for most of a day — a live landmine that would have silently reverted 0270/0271's three security gates if hand-applied as written. Restored by eq-shell `0273` (PR #1567, merged 2026-08-24) once someone happened to notice; not yet dispatched to ehow (separate explicit step, same posture as every other jvkn-identity-adjacent change).

**Mitigation shipped 2026-08-24 (surfaces the collision, doesn't block it — neither pipeline can tell a real eq-field addition apart from its own intended change):**
- eq-shell `scripts/migrate-tenants.mjs` — before applying any migration whose SQL fully replaces a registry function, fetches the function's current live `pg_get_functiondef` and surfaces it (fingerprint in the PR-visible plan output, full text in the CI log) so whoever approves the `tenant-migrate.yml` dispatch can diff it by eye first.
- eq-field `tests/migration-shared-fn-guard.test.js` — CI lint requiring any committed migration that touches a registry function to carry a header comment acknowledging it's shared, pointing back to this table.
- Neither closes the gap completely: eq-field has no live-DB CI at all (migrations are hand-applied, by design — see its own CLAUDE.md), so its side is a forcing-function at commit time, not a live check. Dispatch to ehow stays the human gate.

## 4. Naming conventions — non-negotiable

Every new EQ product follows the same conventions. No locally-invented role names, no app-specific permission key shapes.

### 4.1 Role keys

Use exactly the strings in §3: `manager`, `supervisor`, `employee`, `apprentice`, `labour_hire`. Lower case, snake_case where needed. No app may introduce alternates (`viewer`, `editor`, `owner`, `staff`, `admin` are all forbidden).

If an app feels it needs a new role tier, that's a conversation to add it here — not a conversation to fork the model locally.

### 4.2 Permission keys

Shape: `<module>.<verb>[_<scope>]`

- `<module>` — the module slug (`field`, `quotes`, `cards`, `service`, `intake`, `tender`). Lowercase, singular.
- `<verb>` — the action being gated (`view`, `create`, `edit`, `delete`, `approve`, `import`, `export`, `issue`, `assign`, ...). Present tense, lowercase.
- `_<scope>` — optional scope qualifier when the same verb means different things at different scopes (`_self`, `_team`, `_tenant`, `_all`). Use sparingly; default scope is the most natural one for the verb.

Examples (illustrative, not exhaustive):

| Key | Meaning |
|---|---|
| `field.view_dashboard` | See the EQ Field dashboard |
| `quotes.approve` | Approve a quote (tenant-wide default scope) |
| `cards.issue_team` | Issue cards to one's own team |
| `cards.view_wallet` | See one's own wallet of qualifications |
| `service.create_workorder` | Create a new service work order |
| `intake.import` | Import data via the intake module |
| `tender.view` | See the tender pipeline |

Same verb across modules should mean the same kind of operation. If `quotes.approve` means "give a final sign-off that releases the artefact downstream," then `tender.approve` should mean the equivalent for tenders — not "tick a checkbox somewhere in the UI."

### 4.3 Where perm keys live in code

Each module declares its own perm keys in its own folder:

```
src/modules/<module-name>/permissions.ts
```

The shell composes them at build time into a master `Record<EqRole, Set<PermKey>>`. No module's perm keys live in another module's file. No module's perm keys live in a database table.

A module's `permissions.ts` exports two things:

1. The list of perm keys this module owns (a `const` array, so TypeScript can derive a literal union type).
2. The matrix — for each of the 5 roles, the subset of this module's perm keys that the role holds.

The shell's `useCan()` is a synchronous lookup: `useCan('field.view_dashboard')` → reads the role from `SessionContext` → looks up the master map → returns boolean. No async, no fetch, no flash on render.

## 5. The invite flow

An admin invites a user. That's where role + module entitlements are set.

1. Admin navigates to `Settings → Users → Invite User` on the shell.
2. Admin chooses: email address, role (one of the 5 tiers), module entitlements (which of the tenant's modules the user can access).
3. Shell creates a `users` row (active = false, no pin_hash yet) and sends an email with a one-time link to a "set your PIN" landing page.
4. User clicks the link, chooses a PIN, lands in the shell signed in.
5. From that first session forward, the role and entitlements are part of who they are. Editable by an admin afterwards, but always present.

The role is **not** something the user chooses or can change about themselves. It's part of how the admin who invited them defined their place in the tenant.

### 5.1 Editing a user later

`Settings → Users → <user> → Edit` lets an admin change the role, toggle module entitlements, deactivate the user. Changes reach an already-open session automatically within a few minutes, not just on next login — see the §6.3 correction.

## 6. Session lifecycle and propagation

When a user logs in, two artefacts get minted:

### 6.1 The shell session cookie

Signed into the `eq_shell_session` cookie (HttpOnly, Secure, SameSite=Lax, Domain=`.eq.solutions`, 7-day TTL). The payload:

```ts
{
  user_id: string,
  tenant_id: string,
  role: 'manager' | 'supervisor' | 'employee' | 'apprentice' | 'labour_hire',
  is_platform_admin: boolean,
  exp: number  // epoch ms
}
```

This is the source the shell reads. `SessionContext` exposes it plus the hydrated `user`, `tenant`, and `entitlements` to every component in the tree.

### 6.2 The Supabase JWT (for modules that talk to Supabase directly)

Some modules don't run in-shell — they have their own runtime (the Cards Flutter app, a future native iOS app, etc.) and they hit Supabase directly. RLS is the gate. For RLS to work, the JWT they present must carry the same identity the shell holds.

The shell's `/.netlify/functions/mint-supabase-jwt` endpoint mints a Supabase-format JWT signed with the project's JWT secret. The payload follows Supabase's convention:

```ts
{
  sub: user_id,                  // Supabase auth.uid()
  aud: 'authenticated',
  role: 'authenticated',         // Supabase's *Postgres* role, NOT the EQ tier
  app_metadata: {
    tenant_id: string,
    eq_role: 'manager' | 'supervisor' | 'employee' | 'apprentice' | 'labour_hire',
    is_platform_admin: boolean
  },
  exp: number,                   // epoch seconds, short TTL (15 min default)
  iat: number
}
```

RLS policies on `eq-canonical` read `auth.jwt() -> 'app_metadata' ->> 'tenant_id'` to scope rows to a tenant, and `auth.jwt() -> 'app_metadata' ->> 'eq_role'` for role-gated reads/writes.

The JWT is **short-lived** (15-minute default) and **refreshable** via the shell session cookie. Modules call `mint-supabase-jwt` at startup and again before the JWT expires; they never store it long-term.

Note: `role: 'authenticated'` in the JWT is Supabase's Postgres-role slot — required by Supabase's gotrue/postgrest stack. The EQ tier ("supervisor" etc.) goes into `app_metadata.eq_role`, never into the top-level `role` field, to avoid collision.

### 6.3 Propagation timing

**Correction 2026-07-31 (code-verified against `eq-shell/src/App.tsx`):** the two paragraphs below claim role/entitlement changes only take effect on next login and that live propagation "would require... polling the server... both fight the 'session is the single source' principle." That's false — the polling this text says was rejected has been shipped since 2026-05-24, predating this doc's own last edit by six weeks. `SessionProvider` runs a 5-minute `setInterval` that re-calls `verify-shell-session` and silently rewrites the in-memory session (`setSession(s)`) with whatever role/entitlements/JWT the DB currently holds — no page navigation or re-login required. An admin demoting `supervisor` → `employee` reaches that user's open tab within 5 minutes, automatically. The **only** genuinely next-login-only case is a user who was never active in a live tab to begin with (closed the app, no poll running). No websocket exists or is needed; this was already the "live propagation" path the original text said the architecture had traded away.

Original text, retained for history, **retracted, not just stale**:

~~Role and entitlement changes take effect on the user's **next login**, not in their current session. This is an explicit trade. Live propagation would require either polling the server or a websocket connection sending role-changed events — both fight the "session is the single source" principle. The trade for that simplicity is: when an admin demotes a user from `supervisor` to `employee`, the change applies on their next sign-in. Deactivating a user *does* propagate on next request (the session lookup checks `users.active`).~~

~~The Supabase JWT, being short-lived, propagates role changes within at most one JWT TTL (15 min) — but it still requires the user's session to refresh against the cookie first, so the effective propagation is "next login."~~

## 7. Bridging already-shipped surfaces

Three surfaces predate or co-exist with this model and need explicit bridges:

### 7.1 EQ Field (iframe — handoff)

> **⚠️ Updated 2026-06-24 (live-verified against eq-shell + eq-solves-field source) — the HMAC handoff described below is SUPERSEDED.**
> Per the Phase 3 cutover (see [archive/auth-phase4-hmac-retirement-runbook.md](../../archive/auth-phase4-hmac-retirement-runbook.md) — archived 2026-08-15 as the completed-cutover record; do **not** read its `status:` field as evidence, it said `live` in frontmatter while the body said "DRAFT — not yet approved for execution"), the Field iframe handoff is now a **short-lived Supabase JWT**, not an HMAC token:
> - **Mint:** eq-shell `netlify/functions/token-exchange.ts` — HS256, signed with `SUPABASE_JWT_SECRET`, **60-second TTL**, `source_app = field:<slug>`, built from `session.tenant_id` (active tenant). The HMAC `mint-iframe-token.ts` / `signShellToken` is **dead code** — no caller, file absent; only referenced in comments.
> - **Token mode** (SKS — host off `.eq.solutions`): iframe src `https://eq-field.netlify.app/?tenant=<slug>#sh=<jwt>&cid=<uuid>`. Field `verify-pin.js` (action `verify-shell-token`) verifies the JWT with `SUPABASE_JWT_SECRET` and skips the PIN gate.
> - **Cookie mode** (Field on `.eq.solutions`, e.g. `field.eq.solutions`): src `?tenant=<slug>&shell=1&cid=<uuid>` — the shared `eq_shell_session` cookie rides; `verify-pin` reads it (no `#sh=`).
> - `cid` (correlation id) rides **alongside** `#sh=` (never inside the signed token) for Shell→Field Sentry threading.
> - The 5-tier → 2-tier role mapping below still applies, but it is carried in the JWT's `app_metadata`, not in `mint-iframe-token.ts`.
>
> **Correction 2026-07-05:** the line below ("still stale elsewhere") is itself now stale — checked both named files directly. eq-shell's `CLAUDE.md` already correctly states the Field HMAC handoff is retired dead code (its own "don't touch without checking downstream" table names `token-exchange.ts` as the replacement). eq-field's `CLAUDE.md` doesn't describe the old `mint-iframe-token` path at all — its only HMAC mention is the unrelated, still-current session-cookie signing. Neither needs a correction.

> **⚠️ Added 2026-07-05 (live-verified against eq-field source) — a THIRD, separate PIN system exists and was being conflated with §11.1's Shell PIN.** §11.1 below ("PIN stays for v1") is Shell/Core's own bcrypt-hashed `users.pin_hash` login — correct, current, unrelated to this note. This note is about **eq-field's standalone tenant-wide PIN gate** — a pre-SSO legacy mechanism, ~1,271 lines across `scripts/auth.js` (`checkPin`, `checkStaffTsLogin`), `scripts/people.js` (PIN management admin UI), `verify-pin.js`, and `index.html`. Three parts: (1) shared STAFF_CODE/MANAGER_CODE + name-picker gate, (2) per-worker 4-digit staff-timesheet PIN, (3) supervisor PIN-management screen.
> - **Status for SKS: retired in practice.** All three parts are explicitly code-blocked for the SKS tenant (`_lockGateForCoreOnly()` in auth.js, matching guards in the staff-TS and PIN-management paths) — SKS authenticates exclusively via the JWT/cookie handoff described above. Confirmed live 2026-07-05.
> - **Status for the `eq` demo tenant: still the ONLY way in.** Demo has no Shell/JWT integration configured, so it depends entirely on this legacy PIN gate. **The code cannot be physically deleted without first giving demo an alternative auth path (or accepting demo breaks).** This is the actual blocker on a full code-level retirement, not a decision that's still open — the SKS-facing retirement is already done; the demo-tenant dependency is the remaining piece.
> - `demo-trades` / `melbourne` tenants were removed from canonical 2026-06-28 and no longer reach any of this.
> - **Distinct from `sks-nsw-labour` the standalone repo** (`eq-solutions/sks-nsw-labour`, deploys `sks-nsw-labour.netlify.app`) — a completely separate codebase (pre-2026-05-20 split) with its **own independent PIN implementation, still actively used in production today.** Retiring eq-field's gate has no bearing on that repo. See `eq/active.md` and `sks/pending.md` for that retirement's own (separate, still-open) status.

*Historical (2026-05-24 plan — see callout above for live state):*

EQ Field is loaded via iframe with a 60-second HMAC handoff token from `/.netlify/functions/mint-iframe-token`. The token currently carries `{ kind, name, role: 'staff' | 'supervisor', exp }`.

**Bridge:** extend the token to carry `eq_role` (full 5-tier value) and `is_platform_admin`. EQ Field's `verify-pin` (action `verify-shell-token`) gets a follow-up patch to read both. Field's existing 2-tier internal gate becomes a derived view of the 5-tier model:

| EQ canonical role | EQ Field internal role |
|---|---|
| `manager` or `is_platform_admin = true` | `supervisor` (Field-side) |
| `supervisor` | `supervisor` (Field-side) |
| `employee` / `apprentice` / `labour_hire` | `staff` (Field-side) |

This mapping lives in `mint-iframe-token.ts` and is the only place Field's narrower model leaks into the shell. When Field is decommissioned (Phase 4 of the overall shell plan), the mapping deletes.

**Current status (2026-05-24):** Bridge not yet live. EQ Field's permission system currently runs as a standalone JS shim — `window.EQ_PERMS` (`eq-solves-field/scripts/permission-matrix.js` + `scripts/permissions.js`) — that predates the Shell integration. Phase 1.B (shell token validation in `verify-pin.js`) is designed and ready but `mint-iframe-token` has not yet extended the token to carry `eq_role`. Until Phase 1.B ships: EQ Field's legacy scripts are the active runtime; `useCan()` is unused there. When Phase 1.B completes, Field's permission keys move to `src/modules/field/permissions.ts` in eq-shell and the legacy scripts are deleted.

### 7.2 EQ Cards (Flutter app — Supabase JWT)

Cards talks to Supabase directly from its Flutter runtime. It receives a shell-minted Supabase JWT (see §6.2) via the iframe URL hash on first load, stores it in `flutter_secure_storage`, and refreshes it before expiry by calling `mint-supabase-jwt` through a postMessage bridge to the shell. RLS on `eq-canonical` enforces tenant + role scoping; Cards never trusts client-side checks.

See the Cards canonical-migration plan at [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) for the Cards-side implementation. Cards is the first consumer of `mint-supabase-jwt`.

### 7.3 EQ Intake (in-shell module)

Intake runs inside the shell, not in an iframe. It reads `SessionContext` directly via `useSession()` + `useCan()`. For Supabase calls that need RLS, it uses the same `mint-supabase-jwt` flow as Cards — but invoked in-process by the shell, not via postMessage.

## 8. Tenant entitlements vs role permissions

Two layers, both required:

1. **Tenant entitlement** (`module_entitlements` table) — does this tenant have access to this module at all? Set per tenant. If `quotes` is not in the tenant's entitlements, no user in that tenant sees Quotes, regardless of role.
2. **Role permission** (in-code matrix) — given the tenant has the module, what can this specific user do inside it?

A module is **visible and reachable** when the tenant's entitlement says yes. Specific actions inside it are gated by role.

Example: SKS Technologies has `cards` enabled (tenant entitlement). Within SKS, a `manager` can issue cards (`cards.issue`), a `supervisor` can view team cards (`cards.view_team`), a `labour_hire` sees nothing (no `cards.*` perms for that role).

## 9. What this model is not

- **Not** a per-app permission system. There is one model; every app conforms.
- **Not** RBAC + ABAC. It's straight role-based with explicit per-role permission lists. No attribute-based rules (no "users in region X can see records tagged Y") — if a feature needs that level of granularity, that's a conversation to extend the model deliberately, not a conversation to fork it.
- **Not** dynamic / database-backed. The matrix is static, committed to the repo, versioned by git. No admin UI for "edit what supervisors can do" — those edits land as PRs, get reviewed, and ship in a release.
- **Not** Supabase-Auth-managed. We don't use Supabase's `auth.users` table for our identity. We mint our own JWTs against `shell_control.users` on `eq-canonical`. RLS reads `app_metadata.tenant_id` and `app_metadata.eq_role` from the JWT we sign. This means we own the auth surface end-to-end; trade is that Supabase magic-link / OAuth flows are not available without bridging code we'd have to write.

## 10. Hard rules — checklist for any new module

Every new module PR that adds a gated screen or action must:

- [ ] Declare its perm keys in `src/modules/<module>/permissions.ts`
- [ ] Follow the `<module>.<verb>[_<scope>]` naming
- [ ] Gate every gated UI surface with `useCan()` or `<Gate>`
- [ ] Confirm `module_entitlements` row exists for every tenant that should see the module (one-line migration alongside the module's first PR)
- [ ] Update §4.2 of this doc if introducing a new verb that doesn't appear in any existing module yet (so future modules can reuse it consistently)
- [ ] Never read role from anywhere except `useSession()` (in-shell) or `app_metadata.eq_role` (in modules talking to Supabase directly)
- [ ] Never call out to fetch permissions at runtime
- [ ] If the module runs outside the shell (Flutter, native, etc.), present a fresh `mint-supabase-jwt`-issued token on every Supabase call; refresh before expiry

## 11. Open questions — resolved 2026-05-20

The five §11 questions that flagged uncertainty in the draft were all settled by Phase 1.F's pre-flight assumptions and the shipped implementation. Recorded here so future readers can see the rationale, not as live questions.

1. ~~**PIN vs password.**~~ **Decided: PIN stays for v1.** Bcrypt-hashed (cost factor 10), 4–12 letters or digits. Re-evaluate post-pilot if a tenant manager requests password+MFA — see §11.2 below for the upgrade-path hooks.
2. ~~**Multi-tenant membership.**~~ **Superseded 2026-07-30 (Royce) — see §11.3.** The 2026-05-20 "one user, one tenant, `users.tenant_id` a single FK" decision below is retracted, not just stale. **New decision: Cards is the personal identity/control layer.** Every person gets exactly one Cards identity (one `shell_control.users` row) that they own — homed at the `__personal__` tenant. Tenant membership is additive and optional on top of that identity: a user may choose to join one or more tenants, tracked as active rows in `shell_control.user_tenant_memberships`, never by cloning the `users` row. *(Original 2026-05-20 text, superseded: "one user belongs to one tenant... if a real cross-tenant use case appears, the model becomes two `users` rows linked by email — not a single row with multiple tenant IDs.")*
3. ~~**Role granularity beyond 5.**~~ **Decided: 5 tiers correct for v1.** AHD programme uses the existing tiers without exception (apprentice + employee + supervisor cover the field). 6th tier added only via a deliberate model bump.
4. ~~**Self-service invite acceptance.**~~ **Decided: PIN only on the landing page.** Display name comes from the invite payload; editable by an admin later via `/admin/users/<id>`. Keeps the landing form to one field — finishable in 5 seconds on a phone.
5. ~~**JWT TTL and refresh strategy.**~~ **Decided: 15-minute default, refresh-on-demand via `/.netlify/functions/mint-supabase-jwt`.** Cards's Flutter app (first external consumer, see Cards canonical-migration plan Unit 4) caches the most-recent JWT in `flutter_secure_storage` + refreshes opportunistically when online. If real-world Cards use shows 15 min is too tight for patchy-signal scenarios, bump to 60 min and document the trade in §11.5 web considerations.

## 11.2 v2 backlog — deliberate model bumps for later

When any of these arrive, they ship as a v2 of this doc (deliberate version bump, every module re-pins to v2 in their `permissions.ts`).

- ~~**Multi-tenant membership**~~ — **DECIDED AND LIVE, moved out of backlog 2026-07-30 — see §11.3.** Cards is the personal identity/control layer; a user may hold active membership in more than one tenant at once, additively, via `shell_control.user_tenant_memberships` — not the "separate `users` rows" shape originally anticipated here. Shipped as eq-cards' "Policy 1" (2026-06-17) and now formally ratified as the model. Remaining open scope, still genuinely backlog: an **admin-initiated** path to grant a user membership in a second tenant directly from the Shell admin UI (today, joining a second tenant only happens via Cards — an invite claim or an access request the worker initiates themselves).
- **Password + MFA replacement of PIN** — driven by an enterprise customer requirement. The invite/landing flow extends to accept email-link OR PIN-set on first acceptance.
- **6th role tier** — driven by a real product need. Default first-pass for a "contractor" or "external auditor" tier would slot between employee and labour_hire.
- **Audit log of permission decisions** — every `useCan()` call logged for forensics. Adds runtime cost; only worth it once a tenant manager asks "who clicked what when."
- **Dynamic / DB-backed matrix** — currently the matrix is static + version-pinned in code. A future admin UI for editing per-tenant grants would land here.

## 11.3 Reconciliation 2026-07-30 — §11 item 2 / §11.2 vs shipped eq-cards Policy 1 — RESOLVED

**Decided by Royce, 2026-07-30: "Cards is for everyone = control layer = they own their info. If they choose to they can join multiple tenants."**

That's the model, stated plainly:

- **Cards is the personal identity / control layer for every person**, not a per-tenant app. Anyone gets a Cards identity — it isn't gated behind belonging to a company first.
- **A person owns their own information.** The `__personal__` home tenant is that ownership made concrete in the data model: licences, credentials, and the identity row itself live there, independent of any employer.
- **Joining a tenant is a choice, and a person can make that choice more than once.** Membership in an org tenant is additive on top of the personal identity, not a replacement for it — so holding active membership in more than one tenant at the same time is intended behaviour, not a side effect to be tolerated.

This formally supersedes the 2026-05-20 "one user, one tenant" decision in §11 item 2. What follows is the factual record of how the already-shipped eq-cards implementation lines up with this decision — useful for anyone building the next module against this model, not an open question anymore.

**What the doc said (§11 item 2, decided 2026-05-20, now superseded):** one `users` row per person, `users.tenant_id` a single FK. If cross-tenant access were ever needed, the anticipated shape was **two `users` rows linked by `email`** — never a single row holding multiple tenant IDs.

**What §11.2 anticipated as the v2 backlog item:** the same "separate `users` rows + tenant-switcher" shape, gated behind a deliberate version bump with every module re-pinning to v2.

**What eq-cards actually shipped (`eq-cards/supabase/migrations`, verified by reading the SQL directly, not inferred from commit messages):**

- **`0038_claim_invite_personal_tenant.sql`** (decided 2026-06-17, "Policy 1"): on invite claim, `eq_cards_claim_invite` sets the single `shell_control.users` row's home `tenant_id` to `__personal__` (via `COALESCE` — never overwrites an existing home) and `last_active_tenant_id` to the claiming org. It then inserts **two** active `shell_control.user_tenant_memberships` rows for that one user: one for `__personal__`, one for the org — both carrying the invite-derived role.
- **`0055_auto_provision_always_ensure_personal_wallet.sql`**: widens this beyond Cards-invited workers. `eq_cards_auto_provision` now ensures the personal membership row exists for **any** user who opens Cards at all, including a Core-first Shell manager who already has an org `tenant_id` — so the affected population isn't just "Cards workers," it's "anyone who has ever opened Cards." Note in passing: this path hardcodes the personal membership's `role` to `'employee'` regardless of the user's real role (a manager gets an `'employee'`-role row on their personal tenant) — a minor shipped inconsistency, flagged here for completeness, not fixed in this pass since it's a code change outside this doc's scope.
- **`0072_route_claim_and_access_through_resolver.sql`**: routes worker creation through a dedup resolver to stop duplicate stub workers. The tenant/membership logic itself is copied verbatim from 0038 — no change to Policy 1's shape.
- **`0076_recycled_phone_review_guard.sql`** (file is 0076, internal header still reads "0071" — a pre-existing renumbering artifact, not something this pass touches): unrelated recycled-phone-number dedup guard. Notable only because its own comment independently asserts *"the `__personal__` tenant is retired"* — the same false claim this doc's 2026-07-30 correction (above) already retracted, now confirmed to have spread into eq-cards' migration commentary too. Not fixed here — out of scope (no eq-cards code/migration changes in this pass) but worth a follow-up note in eq-cards if anyone edits that file next.

Live counts as of 2026-07-30 (jvknxcmbtrfnxfrwfimn): 47 active `__personal__` memberships, 40 of which also hold exactly one other active org membership right now (Policy 1's steady state), 6 personal-only (signed up, never claimed an org), 1 platform admin with 3 others.

**What this does *not* break:** §6's session/JWT contract is untouched. A session still carries exactly one active `tenant_id` at a time (`last_active_tenant_id` / the workspace switcher) — role and permission enforcement per session works exactly as this doc describes. Policy 1 changes the underlying *membership* data model, not the *session* shape.

**Why the shipped shape is the right one, not just an acceptable one:** the mechanism eq-cards built — one `users` row, home `tenant_id` = `__personal__`, N active `user_tenant_memberships` rows — is a closer fit to "a person owns their identity and chooses which tenants to join" than either shape this doc originally considered. "Two `users` rows linked by email" (§11 item 2's fallback) would have meant a person's identity forks per tenant, which contradicts "they own their info" — there'd be no single row that *is* the person. A join table with one identity row and N membership rows is exactly the structure "one identity, N chosen affiliations" calls for.

**Consequences of this decision, for whoever builds the next module:**

- Any module design that assumes "a user belongs to exactly one tenant" is now wrong. Read the user's *active* tenant from `last_active_tenant_id` (the current session/workspace), never assume it's the only membership `user_tenant_memberships` holds for that user.
- §11.2's "multi-tenant membership" backlog item is **no longer backlog** — moved to decided/live (see the strikethrough there). The remaining genuinely-open piece is admin-initiated cross-tenant grants (today, joining a second tenant only happens via Cards, worker-initiated).
- ~~The 0055 migration's role-hardcoding on the personal membership row~~ **Fixed 2026-07-30, then verified inert: eq-cards PR [#188](https://github.com/eq-solutions/eq-cards/pull/188) / migration `0111`, applied live to jvkn.** The fix itself was correct (the personal row now self-heals to the user's real role instead of always `'employee'`), but the *justification* was overclaimed — traced all three consumers of role/tenant claims (`custom_access_token_hook`, `mint-supabase-jwt.ts`, `tenant-resolution.ts`) and confirmed none of them read the personal tenant's `user_tenant_memberships.role` for enforcement: RLS's `app_metadata.eq_role` always comes from the flat `shell_control.users.role`, and Shell's phone-OTP login explicitly excludes `__personal__` from its per-tenant role read because the tenant record itself is `active=false`. So this was data-hygiene (an honest column beats a deliberately-false one, even unread), not a functional/security fix — kept applied on that basis, not reverted, per Royce's explicit call after a steelman of both.
- Per this doc's own versioning rule, a decision that changes the identity/membership model this materially is a candidate for a formal v2 bump (role list / naming / payload shape changes trigger one) — recorded here as a live decision either way, but a deliberate version bump with modules re-pinning is a separate, later step, not done in this pass.

**v2-bump question raised and closed 2026-07-30 (Royce):** considered whether §11.3's multi-tenant membership decision was big enough to warrant a formal v1→v2 bump. Decided **no, stays inline v1** — checked against the versioning rule below and the doc's own §6 confirms the session/JWT payload shape is untouched, so the literal trigger conditions aren't met. Also checked whether the "modules pin to a version" mechanism the rule describes actually exists: it doesn't — grepped `permissions.ts` across eq-shell, eq-cards, eq-solves-service, eq-field; eq-shell's files cite this doc by section number in comments only (no version constant anywhere), eq-cards and eq-solves-service have no `permissions.ts` at all, and eq-field is still on its legacy `window.EQ_PERMS` shim, not on this model yet. A bump today would be a label with nothing to enforce it. Revisit when a real trigger (password+MFA, 6th tier, or the admin-grant flow flagged in §11.2) lands, and fold this membership change into that bump then.

---

**Versioning:** this doc gets a version bump (v1 → v2) any time the role list, naming conventions, session payload shape, or JWT shape changes. Modules pin themselves to a version in their `permissions.ts` so a breaking change is visible in PR review.

**Related:**
- [eq/identity/onboarding-portable-identity-2026-06-04.md](./onboarding-portable-identity-2026-06-04.md) — **proposed extension (2026-06-04):** low-friction onboarding + portable worker identity. Pulls §11.2 multi-tenant-membership forward and flags a GoTrue-vs-own-mint (§9) reconciliation. A deliberate v2 bump of this doc when its Phase 2 lands — not yet applied.
- [eq/identity/identity-convergence-target-2026-06-04.md](./identity-convergence-target-2026-06-04.md) — **convergence target (2026-06-04):** names `shell_control.{users, user_tenant_memberships}` as the one identity+membership truth and schedules retiring `public.org_memberships`/`profiles`. Makes the §3.2 auth-vs-operational split explicit on the membership side.
- [eq/identity/PHASE-1F-PLAN.md](./PHASE-1F-PLAN.md) — eq-shell implementation plan for this model
- [eq/cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) — Cards is the first consumer of the Supabase JWT (§6.2 + §7.2)
- [eq/field/permissions/](../field/permissions/) — EQ Field's original 5-tier matrix; this doc supersedes it as the cross-product spec, Field becomes a derived view (§7.1)
- [eq/field/multi-tenancy/](../field/multi-tenancy/) — EQ Field's multi-tenancy plan; §1.5 of that doc is where the 5-tier system first appeared

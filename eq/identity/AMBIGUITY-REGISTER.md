---
title: Identity & Tenant Ambiguity Register
owner: Royce Milmlow
last_updated: 2026-09-15
scope: Every place in the suite that decides "which person is this?" or "which tenant is this?" when the answer is not clean — and what it does when it can't tell
read_priority: high
status: live
---

# Identity & Tenant Ambiguity Register

## Why this file exists

Between 2026-07 and 2026-09 the suite hit at least six separate live incidents —
duplicate logins for one person, test rows landing in another company's roster,
an invite attaching to a stranger's account. Each was investigated from scratch,
root-caused to a different function, and patched individually.

They are all the same bug:

> **When the system cannot cleanly determine which identity or which tenant
> something belongs to, there is no shared policy for what happens next.**
> Roughly fifty places each answer that question their own way. Most guess
> silently.

This register is the list nobody had. It exists so the *next* incident starts
from a page instead of from zero.

**It is a register, not a spec.** It records what each site does today. The
policy below is a proposal, not an adopted standard — see "Decisions needed".

## How to read the Verified column

Control-plane function bodies are known to drift from their migration files —
`eq-shell/supabase/CONTROL-PLANE-LEDGER.md` documents a whole "Supersession"
section of functions where live is *ahead of* the repo. So provenance matters:

| Tag | Means |
|---|---|
| **LIVE** | Verified against the running system on 2026-09-15 — `pg_get_functiondef`/row counts for DB objects, `git show origin/main:<path>` for app code |
| **FIXED** | Closed by a merged PR, named |
| **OPEN** | Has an owner/PR/task, named |
| **✅ GONE** | The described behaviour no longer exists; row kept so the claim isn't re-reported |

> ### Verification pass — 2026-09-15: all 26 `SRC` rows checked
>
> The register originally carried 26 rows tagged `SRC` (committed source only,
> never checked against the running system). All 26 have now been verified and
> the tag is retired. **Result: 22 confirmed, 3 stale, 1 materially changed.**
>
> **Method, and it matters — two different checks:**
> - **DB objects** → `pg_get_functiondef` pattern checks against the actual plane
>   (jvkn, ehow, zaap, madagins — all four reachable).
> - **App code** → `git show origin/main:<path>`, deliberately **not** the working
>   tree. The original sweep read the shared checkouts, and eq-shell's root was
>   sitting on a feature branch with uncommitted changes at the time, so anything
>   read from it could have reflected work-in-progress rather than `main`.
>
> **What the failure rate tells you.** The app-code rows were **11/11 correct**.
> Every failure was a DB row, and every one was *same-day staleness* — behaviour
> retired by a migration that landed hours after the sweep — not faulty analysis.
> So the original sweep's reasoning held up; what it couldn't do was stay current.
> That is the argument for re-verifying before acting, not for distrusting the
> register.
>
> **Two corrections outside the SRC set fell out of the same pass**, both
> consequential: `field_people_iud`'s INSERT fallback is **closed**, not partially
> guarded (Shape 1 row 1), and the real remaining Shape 1 exposure is
> `field_people_removed_iud`, which no plane guards.

One entry in the first sweep was a **false positive** caught exactly this way:
`eq_cards_submit_access_request` was reported as doing an unbounded
`UPDATE public.workers SET user_id = auth.uid()`. The live body does not touch
`workers` at all — the finding came from `2026_06_25c`, which the ledger already
records as superseded. It is listed below under Corrected, deliberately, so
nobody re-reports it.

---

## Shape 1 — Fabricating a tenant when the claim is missing

The most damaging shape: a missing tenant claim produces a *plausible* tenant
instead of an error, so wrong-tenant data looks like ordinary data.

| Site | Repo | On missing/untrusted claim | Verified |
|---|---|---|---|
| `app_data.field_people_iud()` INSERT | eq-field | `coalesce(v_tid, '<that plane's own tenant uuid>')` — writes a real roster row to that tenant. Caused the SKS demo-candidate leak (2026-09-10) and its recurrence (2026-09-15) | ✅ **CLOSED — verified across all planes 2026-09-15.** The `20260910` guard raises immediately after `v_tid` is read (char 541) and the hardcoded uuid sits at char 3442, so the fallback is **unreachable dead code**, not a partial guard. Confirmed present on **ehow** and **madagins**; the function **does not exist on zaap** at all. This row previously read "OPEN / partial guard" — that was wrong |
| `field_people_iud()` UPDATE/DELETE | eq-field | `coalesce(v_tid, tenant_id)` — the tenant predicate becomes a tautology, so the write is unscoped | LIVE — but moot on ehow/madagins: the INSERT-path guard above raises before any branch reaches it |
| **`field_people_removed_iud()`** | eq-field | Same `coalesce(v_tid, tenant_id)` tautology — restore/purge of a removed person runs unscoped. **This is now the real remaining exposure in Shape 1**, not `field_people_iud`: verified live 2026-09-15, it has **no null-tenant guard on any plane** (ehow, zaap, madagins all lack the `refusing to default this write` raise). It was never the headline, so the guard rollout passed it by | 🔴 **OPEN — LIVE** |
| `_eq_intake_check_tenant_match()` | eq-shell (jvkn) | **Guard fails open.** `(auth.jwt()->…->>'tenant_id')::uuid <> p_tenant_id` is NULL when the claim is absent, so the `IF` never fires and the tenant check silently passes. **But it has zero callers on jvkn** — see the note below; fixing it alone changes nothing | **LIVE** |
| `eq_intake_find_template_by_signature(p_tenant_id, …)` | eq-shell (jvkn) | The *actually reachable* version of the row above: `authenticated`-executable, `SECURITY DEFINER`, takes a caller-supplied tenant id and never compares it to the caller's claim. Cross-tenant read of intake templates | **LIVE** |
| `custom_access_token_hook` phone-fallback | eq-cards (live copy) | Falls back to phone match when the uid lookup misses; `tenant_id = coalesce(last_active_tenant_id, tenant_id)` | **OPEN** — [eq-shell #1925](https://github.com/eq-solutions/eq-shell/pull/1925), awaiting Royce |
| `resolveTenantRoute` | eq-cards | `originOrgId ?? defaultOrgId` — a null origin silently defaults to SKS | LIVE |
| `verify-pin.js` ~789 | eq-field | Signed claim's tenant not in `DATA_TENANT_IDS` → falls back to **client-supplied** `body.tenantSlug`; mismatch is warn-only, does not block | LIVE |
| `app-state.js` ~127 | eq-field | Unmatched hostname → `find(slug==='eq') || allOrgs[0]` — an arbitrary org if no `eq` exists | LIVE |
| `shell-handoff-provision.ts` ~133 | eq-shell | A *failed* memberships fetch defaults the session to the user's home tenant (often `__personal__`) | LIVE |
| `staff-resync-licences.ts` ~111 | eq-shell | `body.tenant_id ?? session.tenant_id` — caller-supplied tenant, silent default | LIVE |
| `eq_cards_auto_provision`, `eq_cards_claim_invite` | eq-cards | Default to the `is_personal = true` tenant, chosen by `LIMIT 1` | LIVE |
| `send-digest-test.js` ~80 | eq-field | Unset env → hardcoded SKS uuid | LIVE |

**The intake guard is dead code — checked 2026-09-15 before touching it.** A
caller search on jvkn (`pg_get_functiondef ~* '_eq_intake_check_tenant_match'`)
returns **zero** callers. Every call site in the repo lives inside the vendored
`eq-intake/eq-platform` tree, and the guard is *deliberately stripped* on tenant
planes — `supabase/tenant-migrations/0005_intake_cards_rpc.sql` and
`docs/ARCHITECTURE-V2.md` both state why ("the tenant DB is single-tenant").

That makes the one-line fix risk-free *and* inert on its own. The reachable gap
is a different function. Of the nine intake functions on jvkn:

- `eq_intake_rollback` — `authenticated` + `SECURITY DEFINER` + unvalidated
  tenant param, but **always raises** since `2026_07_28_fix_eq_intake_rollback_dead_calls.sql`. Inert.
- `eq_intake_event_rows` — reads the JWT claim itself. Correct.
- **`eq_intake_find_template_by_signature`** — the only one both reachable by a
  user and unguarded.

Severity is low (intake is near-dormant — `eq_intake_events` has three rows
ever; templates are import column-mappings, not people data) but the cross-tenant
read is real. **Lesson worth keeping: fixing the guard blind would have hardened
dead code and closed the ticket with the reachable path untouched.**

> ### ⚠ Corrected 2026-09-15, later the same day — "near-dormant" was wrong
>
> The paragraphs above led to a proposal to **delete** the jvkn intake surface
> as vestigial. Royce authorised that deletion; it was stopped at the
> blast-radius check and **nothing was dropped**. The proposal is withdrawn.
>
> The surface is **live**. Per-function, against real eq-shell app code
> (`src/`, `netlify/`, excluding vendored and generated trees):
>
> | Function | App callers |
> |---|---|
> | `eq_intake_rollback` | 1 — `AdminAuditPage.tsx` Rollback button |
> | `eq_intake_event_rows` | 1 |
> | `_eq_intake_record_committed` | 2 |
> | `eq_intake_template_track_use` / `_track_outcome` | 0, but **each has a trigger attached** |
>
> Plus `intake-commit.ts`, `intake-stage.ts`, `intake-staging-approve.ts` and
> `_shared/intake-modules.ts`. eq-solves-intake is actively developed. Dropping
> this would have broken the Rollback button and two triggers on the shared
> control plane.
>
> **Why the call was wrong — this is the reusable part, and it applies to every
> SRC/LIVE row in this register.** The "zero callers" evidence was a
> `pg_get_functiondef` search across `pg_proc`. That finds **SQL functions
> calling SQL functions** and is structurally blind to application code invoking
> an RPC over PostgREST. A DB-internal caller search is not a caller search. It
> was then compounded by reading `tenant-migrations/0005` and `0027`'s drops as
> "dead", when they mean the opposite: intake runs on the **control** plane, so
> tenant planes correctly strip it.
>
> **What survives:** `_eq_intake_check_tenant_match` genuinely has zero callers
> in both the DB *and* app code, so the fail-closed fix (`2026_09_15c`, applied
> and behaviourally verified) remains correct and inert exactly as described.
> `eq_intake_find_template_by_signature` is also uncalled in both — its
> `authenticated` EXECUTE grant is a real but much smaller **grant-tightening**
> question, explicitly **not** a deletion one.
>
> **Before proposing any deletion from this register, check app callers as well
> as DB callers.** Two independent searches, or the finding is not established.

**Counter-example worth copying:** `eq-field/netlify/functions/canon-read.js` ~160
refuses and reports to Sentry when the session carries no `tenant_slug`, rather
than falling back to Origin or body. This is the shape the rest should match.

## Shape 2 — Two candidates, one picked silently

`LIMIT 1` where the correct answer is "stop and ask".

| Site | Repo | Tie-break | Verified |
|---|---|---|---|
| `eq_cards_find_or_create_worker_for_invite` | eq-cards | `ORDER BY (w.user_id IS NOT NULL) DESC` — **prefers an already-claimed worker**, so an invite can attach to someone else's account. Writes no flag row | **OPEN** — holds on >1 via [eq-cards #361](https://github.com/eq-solutions/eq-cards/pull/361); the refusal is logged as `invite.worker_match_ambiguous` by [eq-shell #1934](https://github.com/eq-solutions/eq-shell/pull/1934). Both awaiting Royce. Not user-reachable (`service_role`-only since `0136`) — an admin-flow correctness bug, not a security hole |
| `eq_cards_link_or_create_worker` | eq-cards | Ranks by credential count then `created_at`, `LIMIT 1` | **LIVE** (does write `identity_collision_flags`) |
| `roster-match.ts` `findRosterMatch` | eq-shell | `matches.find(active) ?? matches[0]` | LIVE |
| `accept-invite.ts` ~269 | eq-shell | `phoneStubs?.[0]` — first of N phone-variant matches, no ambiguity check | LIVE |
| `resolve_invite_auth_identity` | eq-shell | Oldest auth user wins | LIVE |
| `eq__caller_staff_id`, `eq__caller_actor_staff_id` | eq-field | `LIMIT 1` with no `ORDER BY` — two staff rows sharing a `user_id` resolve arbitrarily | LIVE |
| `eq_cards_admin_upsert_worker` | eq-cards | Same silent tie-break | LIVE |
| `backfill-worker-links.ts` ~161 | eq-shell | Builds an email→user Map; duplicate emails last-write-wins | LIVE |

## Shape 3 — Ambiguity resolved by doing nothing, invisibly

Safer than guessing, but indistinguishable from success.

| Site | Repo | Behaviour | Verified |
|---|---|---|---|
| ~~`link_pending_invites` email branch~~ | eq-cards | **STALE — retired 2026-09-15** by `2026_09_15_link_pending_invites_retire_dead_branches.sql`. Verified live: the body no longer references `org_memberships` at all; only the worker-stub link from eq-cards `0070` remains | ✅ GONE |
| `workers-canonical-sync` `findStaffId` | eq-cards | ≥2 adoptable → no match → creates a new record instead | LIVE |
| `cards-approve-staff.ts` `findExistingStaff` | eq-shell | Anything but exactly one match falls through and mints a duplicate `staff_id` | LIVE |
| `field_teams_iud`, `field_team_members_iud`, `field_team_supervisors_iud` — DELETE | eq-field | Null claim → `= NULL` → matches zero rows → **reported as success** | LIVE |

## Shape 4 — Errors swallowed, so the failure mode is "allow"

| Site | Repo | Behaviour | Verified |
|---|---|---|---|
| `custom_access_token_hook` | eq-cards/eq-shell | Whole body wrapped `EXCEPTION WHEN OTHERS → RETURN event` — any error silently mints a token with no claims. **Still true, re-verified live 2026-09-15.** One change since first written: as of [#1925](https://github.com/eq-solutions/eq-shell/pull/1925) the phone-fallback path writes `identity_recycle_review` (`match_path='jwt_fallback'`), so that *fallback* is now visible — the blanket swallow wrapped around it is not | LIVE |
| `tg_fulfil_access_requests_on_claim` | eq-shell | All errors swallowed | LIVE |
| `eq__caller_uid` | eq-field | Swallows exceptions → NULL, which downstream reads as a visibility decision | LIVE |
| `_shared/field-person.js` ~36 | eq-field | Every failure path returns `null` with **no logging at all**; the caller then substitutes a display name derived from the email local-part | LIVE |

## Shape 5 — Unbounded claim

| Site | Repo | Behaviour | Verified |
|---|---|---|---|
| ~~`link_pending_invites` org_memberships branch~~ | eq-cards | **STALE — retired 2026-09-15**, same migration. Verified live: `pg_get_functiondef ~* 'org_memberships'` → false. The unbounded UPDATE no longer exists | ✅ GONE |
| `shell-login-phone-otp.ts` email self-heal | eq-shell | Claimed every worker row sharing the email, fire-and-forget with errors discarded | **FIXED** (gated) by [#1923](https://github.com/eq-solutions/eq-shell/pull/1923) — now requires `email_confirmed_at`. The unbounded `.eq('email').is('user_id',null)` update itself is unchanged; worth a second look |

### Corrected — reported but NOT live

| Site | Reported | Actual |
|---|---|---|
| `eq_cards_submit_access_request` | Unbounded `UPDATE public.workers SET user_id = auth.uid()` claiming every worker with the phone | **Not live.** Live body does not touch `workers`. Finding came from `2026_06_25c`, superseded per CONTROL-PLANE-LEDGER. Do not re-report |

## Shape 6 — The target pattern (holds for review)

**Three** sites write to a review queue (was four — see the retired row). Only the
first actually **stops**.

| Site | Queue | Stops? | Verified |
|---|---|---|---|
| `handle_phone_dedup()` — stale >90d, and live-duplicate branches | `identity_recycle_review` | **Yes** — inherits nothing, holds | **LIVE** |
| ~~`link_pending_invites` phone branch~~ | ~~`identity_recycle_review`~~ | **STALE — retired 2026-09-15.** Verified live: no longer references the queue at all | ✅ GONE |
| `fn_link_worker_on_user_create` | `phone_link_review` | **No — flags the phone disagreement, then claims the worker anyway** | LIVE |
| `eq_cards_link_or_create_worker` | `identity_collision_flags` | **No — flags the collision, then provisions the duplicate anyway** | **LIVE** |

### The queues themselves were unwatched

Verified live 2026-09-15: of the three queues, only `identity_collision_flags`
had a scheduled reader (`check-identity-collisions.ts`).

| Queue | State when checked |
|---|---|
| `phone_link_review` | 1 row `pending` since 2026-08-20 — **26 days**, nobody aware |
| `identity_recycle_review` | 1 row total, **inserted by hand** on 2026-09-14 during incident reconciliation — the trigger has never filed one |
| `identity_collision_flags` | 2 rows, both resolved |

**Closed** by [eq-shell #1927](https://github.com/eq-solutions/eq-shell/pull/1927)
— merged 2026-09-15 as `1db2922a`. Adds `check-review-queues.ts` (21:55 UTC,
alert-only, leads with the oldest row's age).

The recycle queue's emptiness is the sharper lesson: with no reader, *"the
detector works"* and *"the detector has never fired"* were indistinguishable
for months.

---

## Policy — ADOPTED 2026-09-15 (rule 2 staged)

Royce's call, 2026-09-15: adopt rules 1, 3 and 4 now; rule 5 was already
satisfied by #1927; **stage rule 2**.

> **Ambiguity is a stop condition, not a default-value problem.**

1. ✅ **ADOPTED — Never fabricate a tenant.** If the tenant cannot be
   established from a trusted signed claim, raise. Do not fall back to
   own-tenant, home-tenant, personal-tenant, an Origin header, a request-body
   field, or a hardcoded uuid. A routing mistake should fail loudly rather
   than quietly become another tenant's data.
2. 🕓 **STAGED — One match links; zero or many holds.** Any identity match that
   resolves to ≠1 candidate writes a review row and stops. `LIMIT 1` as a
   tie-break on a *person* is never correct. Accepted in principle; rollout
   deferred because it changes behaviour at ~8 sites and will surface latent
   duplicate data currently being absorbed silently. First site to land it:
   `eq_cards_find_or_create_worker_for_invite` (decision 2 below).
3. ✅ **ADOPTED — A flag is not a decision.** If a collision is worth
   recording, it is worth stopping for. "Log it and proceed" is the worst of
   both — it creates the duplicate *and* the paperwork, and Shape 6 shows two
   sites doing exactly that today.
4. ✅ **ADOPTED — Guards fail closed.** `EXCEPTION WHEN OTHERS → RETURN event`
   on an auth hook converts any error into "allow". Catch narrowly or not at
   all.
5. ✅ **IN FORCE — Every review queue has a watcher.** Satisfied by #1927; keep
   it true when adding a queue.

**What adoption means in practice:** these are review criteria for new work, not
a mandate to retrofit all ~50 sites. A new or edited site that breaks rules 1,
3 or 4 should be pushed back on. Existing violations get fixed as they are
touched, or when they cause an incident — not in a sweep.

## Decisions — all six settled 2026-09-15

| # | Decision | Royce's call | State |
|---|---|---|---|
| 1 | `_eq_intake_check_tenant_match` fails open | **Check callers first, then fix** | Checked: **zero callers** — fix is inert on its own. Real target is `eq_intake_find_template_by_signature` (see Shape 1 note). Fix + wiring pending |
| 2 | `eq_cards_find_or_create_worker_for_invite` prefers an already-claimed worker | **Stop and ask when >1 match** | **Built, awaiting merge.** [eq-cards #361](https://github.com/eq-solutions/eq-cards/pull/361) raises on >1; [eq-shell #1934](https://github.com/eq-solutions/eq-shell/pull/1934) catches it, writes `invite.worker_match_ambiguous` to `shell_control.audit_log` and returns an actionable 409. Design call resolved — no new queue. See the note below |
| 3 | The `coalesce`-to-own-tenant fault, present in every tenant's templated copy | **Roll out company by company** | **Scope shrank sharply on verification (2026-09-15).** For `field_people_iud` the rollout is already **done**: guarded on ehow *and* madagins, and the function doesn't exist on zaap. The remaining work is a **different function** nobody had flagged — `field_people_removed_iud`, unguarded on all three planes. `task_9b876f68` should be re-briefed against that, not the original target |
| 4 | [#1925](https://github.com/eq-solutions/eq-shell/pull/1925) — `custom_access_token_hook` phone-fallback logging | **Merge** | Merging on green; all checks pass except the Netlify preview |
| 5 | Should admin-invite capture a phone number? | **Make it required** | Pending — `invite-user.ts` plus the admin invite form |
| 6 | Adopt the policy | **Adopt rules 1/3/4 now, stage rule 2** | Done — see the Policy section above |

**Decision 2 — what "ask" turned out to mean.** The durable record cannot be
written by the function. `RAISE` aborts the RPC's transaction, so any flag row the
function inserted would roll back with the refusal that caused it, and jvkn has no
dblink or autonomous-transaction path around that. So the function raises and the
*caller* logs, on its own service client in a separate transaction — the same shape
`shell-join-tenant.ts` already uses for `login.join_register_rejected`, and the same
reason `writeAuditLog` deliberately bypasses `public.eq_write_audit_log` ("silent drop
issues"). `shell_control.identity_recycle_review` was rejected for the reasons in the
Shape 6 notes: `new_user_id`/`source_user_id` are both NOT NULL with no auth identity
in existence at invite time, and `eq_list_recycle_reviews()` INNER JOINs
`shell_control.users` on `source_user_id`, so a forced row would never render on the
Number Reviews page.

Sequencing is eq-shell first (Royce, 2026-09-15): the catch is inert until the
migration applies, so shipping it first means no refusal is ever unlogged. Merging
eq-cards does **not** apply the migration — `jvkn-control-plane-apply.yml` is
`workflow_dispatch`-only; verify against the live DB, not a green check.

**Live-verified 2026-09-15, after the PRs were written.** `pg_get_functiondef` on
jvkn returns a body **identical to `0073`** — no drift — and
`has_function_privilege` confirms `anon=false`, `authenticated=false`,
`service_role=true`. So the severity calibration holds: admin-flow correctness bug,
not a security hole.

**Blast radius, measured rather than guessed.** Rule 2's rollout was deferred partly
because it "will surface latent duplicate data currently being absorbed silently."
For this function that is now a number: of **107** workers on jvkn there are exactly
**two** ambiguous groups.

| Group | Key | Rows | Reaches the resolver? |
|---|---|---|---|
| A | shared **email** (`…@sks.com.au`) | an email-only stub (2026-06-15, unclaimed) + the same person's claimed account (2026-08-18) — same initials, one human | **Yes** — the phone pre-check never looks at email |
| B | shared **phone** | two rows, **both claimed** — two auth identities on one number | No — `eq_cards_worker_claimed_by_phone` already 409s on it first |

So in practice `0173` changes the outcome for **one** identity today, and group A is a
plain duplicate of one person rather than a genuine collision. Merging that stub into
the claimed record is the right resolution; until it is merged, that person cannot be
re-invited. Worth doing before or shortly after applying, not because the refusal is
wrong but because it is the refusal working on data that should not exist.

Group B is the more interesting one and is *not* addressed here: two claimed identities
sharing a phone is exactly `handle_phone_dedup`'s territory, and it is being absorbed
silently by the pre-check's 409 rather than filed anywhere.

**Left open deliberately — needs Royce.** Only the `>1` case is closed. *Exactly one
match that is already claimed by a different user* still links silently. That
behaviour is deliberate in `0073` (a multi-org tradie must reuse their real row), and
refusing it would block legitimate re-invites of someone who already has an account —
a different change with a different blast radius. Partly mitigated already:
`eq_cards_worker_claimed_by_phone` (2026_09_09b) 409s first on the same normalisation,
but it only checks the **phone**, so a claimed row matched by **email** still links.

Related but separately tracked: **SEC-71** (2FA enforcement is client-side only —
`shell-login.ts` issues a full session regardless of `requires_totp_enrollment`),
already open with a 2026-12-04 review date, and `task_4ae84033`
(`link_pending_invites_on_confirm`'s `WHEN` clause only fires on
`email_confirmed_at`, so its phone branch may never have run for the 21 of 93
jvkn users who are phone-only).

## Maintaining this

- Add a row when you touch any site that answers "which person" or "which
  tenant". Don't start a second list.
- Re-verify **LIVE** rows before acting on them — they were true on 2026-09-15
  and this file will drift like every other.
- Promote a row to **FIXED** only with a merged PR number next to it.

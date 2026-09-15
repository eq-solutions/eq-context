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
| **`field_people_removed_iud()`** | eq-field | Same `coalesce(v_tid, tenant_id)` tautology on the UPDATE and DELETE predicates — with a null claim it collapses to `tenant_id = tenant_id`, so the statement is not tenant-scoped. Unguarded on **all three** planes (ehow, zaap, madagins), and trigger-wired on all three. The guard rollout passed it by because it was never the headline | 🟠 **OPEN — LIVE, but NOT browser-reachable.** *Severity corrected 2026-09-15 — this row first read 🔴 implying an open door; that was written from DB-pattern evidence without checking reachability, the same mistake shape as the intake-vestigial call earlier the same day.* Measured, not reasoned: with a null tenant claim an `authenticated` caller sees **0 rows** through `app_data.field_people_removed`, because the view is `security_invoker` and RLS on `app_data.staff` scopes on the *same* expression (`tenant_id = …->>'tenant_id'` → `= NULL` → deny), so no `OLD` row exists and the trigger never fires. A `service_role` caller sees **36**. **The live vector is therefore a service-role/definer caller with no tenant claim — RLS bypassed, tautology reached** — which is exactly the class behind the original phantom-roster incident (mis-minted JWT, eq-shell side). Worth guarding as defence-in-depth on a path that has already bitten once; not an open door. **✅ FIXED 2026-09-15 — guard applied to all three planes** ([eq-field #991](https://github.com/eq-solutions/eq-field/pull/991)), anchor-spliced per plane so each body's own shape survived (zaap kept its `0274` comment and its lack of the `denied_perms` veto; ehow and madagins kept theirs). Grants unchanged at `service_role`-only. Proven behaviourally on ehow against a real row, in rolled-back transactions: null claim now raises `P0001 … refusing to default this write`, valid claim still writes (Restore path intact). Note for anyone repeating this: the first behavioural attempt ran on **zaap, which has 0 rows in that view**, so the UPDATE matched nothing, the trigger never fired, and the clean no-error result looked exactly like a pass — it was vacuous and was redone on ehow |
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
| `eq_cards_find_or_create_worker_for_invite` | eq-cards | Was `ORDER BY (w.user_id IS NOT NULL) DESC` — **preferred an already-claimed worker**, so an invite could attach to someone else's account, with no flag row | **FIXED** — [eq-cards #361](https://github.com/eq-solutions/eq-cards/pull/361) (`0173`) holds on >1; [eq-shell #1934](https://github.com/eq-solutions/eq-shell/pull/1934) logs `invite.worker_match_ambiguous` + returns a 409. Applied to jvkn 2026-09-15 09:30:58Z, verified live: guard present, `LIMIT 1` gone, grants still `service_role`-only |
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
| `handle_phone_dedup()` — stale >90d, and live-duplicate branches | `identity_recycle_review` | **Yes** — inherits nothing, holds — but see the coverage note under decision 2's group B: it stops the shapes it can *see*, and `public.workers` is not one of them | **LIVE** |
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

## Decisions — six settled 2026-09-15, two more opened by same-day investigation

Rows 1, 4 and 5 below were left showing intermediate states from earlier in the
day after the underlying work had already finished — corrected 2026-09-15
(later pass) rather than at the time, so anyone reading only this table saw
"pending" for things that were done. Rows 7–8 are new, not part of the
original six — the Group A/B investigation under decision 2 surfaced a real
duplicate (resolved) and a genuine open product question (not resolved).

| # | Decision | Royce's call | State |
|---|---|---|---|
| 1 | `_eq_intake_check_tenant_match` fails open | **Check callers first, then fix** | **Fix applied and behaviourally verified** — [eq-shell #1929](https://github.com/eq-solutions/eq-shell/pull/1929) merged, migration hand-applied same day (ledger-corrected in [#1931](https://github.com/eq-solutions/eq-shell/pull/1931) after a `merge ≠ applied` mistake). "Wiring" was never done, deliberately: checking further found the fix has zero callers (inert by design) and the actually-reachable function, `eq_intake_find_template_by_signature`, is a **separate, smaller, still-open question** — tighten its `authenticated` EXECUTE grant, or leave it — genuinely Royce's call, not chased further today |
| 2 | `eq_cards_find_or_create_worker_for_invite` prefers an already-claimed worker | **Stop and ask when >1 match**, then (2026-09-15) **close the email half too** | **Both halves shipped and live.** `>1` via [eq-cards #361](https://github.com/eq-solutions/eq-cards/pull/361) (`0173`) + [eq-shell #1934](https://github.com/eq-solutions/eq-shell/pull/1934); email via [eq-shell #1935](https://github.com/eq-solutions/eq-shell/pull/1935), applied through the governed `control-plane-migrate.yml` dispatch, deploy published 09:54:52Z. Full verification trail, including a caught `plan:true`-dispatch-looked-like-an-apply near-miss, is in the note below. Audit logging for both pre-check refusals is in progress, [#1940](https://github.com/eq-solutions/eq-shell/pull/1940) (open). The investigation into what this change would newly block also found two real live duplicate-identity groups — see decisions 7 and 8 |
| 3 | The `coalesce`-to-own-tenant fault, present in every tenant's templated copy | **Roll out company by company** | **Closed.** Scope shrank on verification: `field_people_iud` was already done (guarded on ehow + madagins, doesn't exist on zaap). The real remaining gap, `field_people_removed_iud`, was unguarded on all three and is now fixed everywhere via [eq-field #991](https://github.com/eq-solutions/eq-field/pull/991), re-briefed as `task_e0ba7aba` (superseded `task_9b876f68`) and verified behaviourally. Royce's call, once severity was shown to be service-role-only: all three planes in one pass |
| 4 | [#1925](https://github.com/eq-solutions/eq-shell/pull/1925) — `custom_access_token_hook` phone-fallback logging | **Merge** | **Merged** — `a06bc609` |
| 5 | Should admin-invite capture a phone number? | **Make it required** | **Merged** — [eq-shell #1928](https://github.com/eq-solutions/eq-shell/pull/1928), `2cb574e5`. Presence required on any path that issues a new invite; not required on the branch that only adds an existing account to a tenant (mints no new identity) |
| 6 | Adopt the policy | **Adopt rules 1/3/4 now, stage rule 2** | Done — see the Policy section above |
| 7 | **New, found investigating decision 2's blast radius.** Group A: one real person held two worker rows (an unclaimed 2026-06-15 email stub + their claimed 2026-08-18 account) — a plain duplicate, not a genuine collision, and the new `>1`-match guard would have blocked re-inviting them | **Merge the stub into the claimed row** | **Done.** Royce's explicit go. Stub `b1ec35fb` deleted, `cb49cbf5` kept — full precondition/postcondition verification in the eq-context session log, following `merge-william-brown-duplicate-identity.sql`'s methodology with the "repoint ehow first" step correctly identified as not applicable here (separate `staff_id`s, not shared). jvkn: 107 → 106 workers, zero email-duplicate groups remain |
| 8 | **New, found the same investigation. Group B: a genuine, still-open product question**, not a bug. One SKS person has two accounts sharing one phone — a "work" identity (email signup, SKS tenant) and a "wallet" identity (phone-OTP signup, `__personal__` tenant). This is the **normal, common shape** (35 of 81 claimed workers on jvkn have this same work+wallet split) — the phone-sharing is what makes it *look* like the duplicate-detection problem this whole register is about, but it structurally is not one | **Not yet asked** | **Open.** *Should one human have one worker row spanning employer + personal wallet, or two?* Everything downstream depends on the answer: if one-row-per-human is the model, this is a real defect and a `public.workers`-level detector is justified; if work/wallet are deliberately separate, this was never a collision, the phone pre-check (`eq_cards_worker_claimed_by_phone`) is already behaving correctly, and no detector should be built against it. Zero credentials on either row today, so nothing is diverging and there is no urgency — but a detector built before this is answered would either fire on all 35 legitimate wallet rows, or miss the real cases. `identity_recycle_review` cannot see this shape at all regardless of the answer: it only ever reads `auth.users.phone`/`shell_control.users.phone`, never `public.workers.phone` — a coverage gap, separate from whether Group B itself is a bug |

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

**The ledger was behind, not the database.** The plan run listed five pending
migrations rather than one. `0169`–`0172` turned out to be **already live** — hand-applied
via MCP and never stamped — so the real run re-ran four migrations whose bodies were
already in place. It was safe only because all five were pure `CREATE OR REPLACE
FUNCTION` with no standalone DML: every `UPDATE`/`INSERT` in them sits *inside* a function
body as code, so nothing re-backfilled. Check that before any catch-up apply — "pending"
in this pipeline means "unstamped", which is not the same as "not applied", and a
migration carrying top-level DML would have re-run it. (A sixth, `0174`, merged while the
run was queued and was swept in.)

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
| A | shared **email** (`…@sks.com.au`) | an email-only stub (2026-06-15, unclaimed) + the same person's claimed account (2026-08-18) — same initials, one human | **Was yes** — the phone pre-check never looked at email. **Merged 2026-09-15, group A no longer exists** (see below) |
| B | shared **phone** | two rows, **both claimed** — two auth identities on one number | No — `eq_cards_worker_claimed_by_phone` already 409s on it first |

So in practice `0173` changed the outcome for **one** identity, and group A was a plain
duplicate of one person rather than a genuine collision.

**Group A merged 2026-09-15, on Royce's explicit go — jvkn now has zero email-duplicate
groups (107 → 106 workers).** Worker `b1ec35fb` (the unclaimed stub) deleted, `cb49cbf5`
(claimed) kept. Nothing needed carrying across: the keeper was already a strict superset —
same name and email, plus the phone — and the stub held zero credentials, assignments,
inductions, invites, collision flags and licences. Its 31 `worker_sync_dispatch` telemetry
rows went with it; `audit_log` was left alone (append-only, and an accurate record of what
that identity did).

Followed `eq-shell/scripts/merge-william-brown-duplicate-identity.sql`, including its rule
that the loser is **DELETE**d and never UPDATEd — an UPDATE fires the sync's upsert branch,
whose `findStaffId` probes all miss, and it then inserts a fresh staff row.

**Why that script's load-bearing "repoint ehow first" step did not apply here** — worth
recording, because the two cases look identical and are not. William's two workers shared
**one** `staff_id`, so deleting the loser while ehow still pointed at it would have
deactivated his live row. Group A's workers had **separate** staff rows (`381fbd81` stub,
`13969d35` keeper), so the AFTER DELETE trigger's
`.eq("cards_worker_id", …)` deactivation could only ever match the stub's row, which was
already `active=false`. Confirmed after the fact: the keeper's ehow row is still
`active=true`.

**Left dangling on purpose.** ehow staff row `381fbd81` still carries a `cards_worker_id`
pointing at the deleted worker. Nulling it would look like tidying and is the wrong move:
`findStaffId`'s probes 3 and 4 only consider rows where `cards_worker_id IS NULL`, so
blanking it would make this dead row *adoptable* by a future sync and re-link it to somebody
else. The dangling pointer is what keeps it inert.

### Group B — investigated 2026-09-15. It is *not* `handle_phone_dedup`'s territory.

The note above originally read: "two claimed identities sharing a phone is exactly
`handle_phone_dedup`'s territory, and it is being absorbed silently by the pre-check's
409 rather than filed anywhere." The second half is correct. **The first half is wrong,
and that is the finding** — the trigger did not fail to file this. It cannot see it.
Three independent reasons, any one of which alone is sufficient:

1. **Wrong table.** `handle_phone_dedup()` never reads `public.workers`. It matches
   `NEW.phone` against `auth.users.phone` and `shell_control.users.phone` only. Group B
   is a collision between two `public.workers.phone` values. It becomes visible to the
   trigger only if the same duplication is *also* mirrored onto `shell_control.users`.
2. **INSERT-only, so a phone that arrives later is never re-checked.** Confirmed by the
   live `pg_get_triggerdef` captured in `2026_09_15_backfill_auth_users_dedup_triggers.sql`:
   `on_auth_users_insert_dedup` is `AFTER INSERT ON auth.users` — there is no
   `UPDATE OF phone`. It fires once per auth identity, at creation, and only if the phone
   is present at that instant; the body's first statement is
   `IF NEW.phone IS NULL OR NEW.phone = '' THEN RETURN NEW`. An identity created by email
   signup, admin provisioning or invite-claim — with the phone landing on
   `public.workers` — exits on line one and is never revisited.
3. ~~**The lookup that would have caught it post-dates the row.**~~ **Overtaken by the
   live read — see below.** This was written as the timing argument: the third lookup
   (`2026_08_30c`, live account via `shell_control.users.phone`) post-dates the 2026-08-20
   row by ten days. True, but **not the operative cause, and weaker than reason 1** — that
   lookup would not have caught it either. Verified on jvkn 2026-09-15: the work identity
   has `auth.users.phone` **NULL** *and* `shell_control.users.phone` **NULL**. The number
   exists **only** on `public.workers.phone`. So reason 1 is not one of three contributing
   causes — it is the whole story, and it is still live today with `2026_08_30c` applied.

And `2026_08_30c` **is not retroactive** — it changed what a future INSERT can find, and
nothing swept the collisions it newly made detectable. There is also no uniqueness guard
to fall back on: no unique index or constraint on `public.workers.phone` exists in any
migration (`2026_08_23e` normalises the *format* on write, nothing more).

**The lesson sharpens the one already recorded above.** "The queues themselves were
unwatched" is now closed by [#1927](https://github.com/eq-solutions/eq-shell/pull/1927).
This is the next layer: a watcher on a queue proves the queue is read, **not** that the
detector feeding it covers the shape you think it covers. `identity_recycle_review` will
keep reporting zero for group B no matter how reliably it is watched, and that zero will
keep looking like good news. Coverage is a separate property from watchedness, and only
coverage was ever asserted for this queue — never tested.

### Resolved live 2026-09-15 — one human, and possibly not a collision at all

Supabase MCP became available later in the same session; every claim below is a live
read of jvkn, not inference.

**It is one human, duplicated — not two humans sharing a number.**

| | Work identity | Wallet identity |
|---|---|---|
| worker | `5e9d6e83` (2026-06-15) | `406d2b0f` (2026-08-20) |
| shell name | Zemi Asri | Mohamed Zemi Asri Bin Mohamed Azri |
| tenant | `7dee117c` (SKS) | `279a6da0` (**personal-wallet sentinel**) |
| auth | email, `phone_confirmed=false` | phone OTP, `email_confirmed=false` |
| `auth.users.phone` / `shell_control.users.phone` | **NULL / NULL** | set / set |
| active | true | false |
| last sign-in | 2026-09-09 | 2026-09-09 |
| credentials / invites | 0 / 0 | 0 / 1 |

The short name is the long name. Same person, signing into both on the same day.

**Scale: it is a one-off, not a class.** The full sweep over all workers on jvkn returns
**exactly one** normalised-phone group with >1 row — this one. Nothing else is hiding
behind the 409.

**The reframe that matters.** 35 of the 81 claimed worker rows are owned by
personal-wallet (sentinel-tenant) identities, so a wallet identity *separate from* a work
identity is the **normal, common pattern** — not an anomaly. What is unique here is one
human holding both, on one number. That makes the open question a **product** question,
not a data one:

> Should one human have **one** worker row spanning employer and personal wallet, or
> **two**?

Nobody has decided this, and every technical option depends on the answer. If the model
is one-row-per-human, this is a real defect and a workers-level detector is justified. If
work and wallet are deliberately separate rows, **this was never a collision**,
`eq_cards_worker_claimed_by_phone`'s 409 is behaving correctly, and group B should be
**reclassified rather than fixed**. One answer flips the whole thing.

**Both leads from the first pass: closed, both negative.**

- `shell_control.phone_link_review`'s pending 2026-08-20 row is a **different user and a
  different pair of phones**. The shared date was coincidence — group B was filed
  **nowhere**, in any queue.
- `identity_recycle_review` still holds exactly one row: the by-hand `phone_orphan` from
  the 2026-09-14 Aditi reconciliation. The trigger has still never filed one.

**Not resolved, deliberately — and cheap to leave.** Zero credentials on either row, so
nothing is diverging today and no data is at risk; the cost of the split is purely future.
It is also the cheapest a merge will ever be, and gets expensive the moment either row
accrues a credential. Decision protocol run 2026-09-15 recommended **answering the product
question before merging or building a detector**: a merge without it is a guess on
customer identity data (wrong-survivor risk is real — the active row is the one with no
credentials), and a detector built against n=1 would fire on all 35 legitimate wallet rows
and become the next unwatched queue.

**Leads from the first pass — both now run and closed (kept for the reasoning trail).**

- `shell_control.phone_link_review`'s single pending row has sat since **2026-08-20** —
  the same date group B's second row was created. `fn_link_worker_on_user_create` matches
  a worker **by email** (`lower(w.email) = lower(NEW.email)`, `LIMIT 1`), writes that row
  when the phones disagree, then claims the worker anyway. That is a *different* shape
  from group B (email-matched, phone-mismatched — not phone-matched), so the shared date
  may be coincidence. But if it is the same person, then group B was filed after all —
  in the other queue, by the site that flags-then-proceeds. Worth ruling in or out first.
- **Most likely explanation, untested at the time — since CONFIRMED:** row 1 (named,
  `@sks.com.au`) plus row 2 (no name, no email, phone-signup shape) reads as one person
  who later signed up themselves by phone, not two humans on one number. The live read
  confirmed this exactly: `shell_control.users` gives row 2 the same person's full legal
  name. What the guess missed is that row 2's tenant is the **personal-wallet sentinel**,
  which is what turns a merge into a product question rather than a cleanup.

**Recycled-number policy — partial, and the gap is Royce's call, not an invention.** A
*mechanism* policy exists for the recycle case and is live: `handle_phone_dedup()`'s
`[0071]` guard holds anything whose matched source has not been seen in 90 days. There is
no policy at all for the case group B actually represents. And group B turns out **not**
to be a shared-number case at all (it is one human with a work identity and a wallet
identity), so the shared-number policy question is **still open and still unevidenced** —
no live example of two different humans on one number exists on jvkn today.
`2026_09_15_recycle_review_phone_dup_no_graft.sql` names the intended direction in its own
header: a consent-gated flow where the affected worker confirms it themselves, mirroring
`eq_cards_request_worker_access` — explicitly "a real build, scoped separately, not rushed
into this migration." Until that exists, group B has no defined resolution path.

**Not resolved here, deliberately.** No identity was merged, deleted or re-pointed:
customer-data migration and auth-flow changes are Royce's call under the global authority
model, and jvkn is the shared control plane every tenant depends on.

**The email half — decided 2026-09-15, built.** This was left open for Royce because
refusing an already-claimed *single* match is a product decision, not a bug fix: `0073`
deliberately reuses a claimed row so a multi-org tradie keeps one identity, and refusing
outright would block legitimate re-invites. **Royce's call: option (a′)** — close it at
the pre-check, leave the resolver alone. Built as
[eq-shell #1935](https://github.com/eq-solutions/eq-shell/pull/1935)
(`eq_cards_worker_claimed_by_email` + a second pre-check in `create-worker-invite.ts`).
**Open, not merged; migration not applied** — `control-plane-migrate.yml`'s `apply` job is
`workflow_dispatch` only, and its push job only comments a dispatch link.

**Option (a) as originally written could not be built, and the reason is worth keeping.**
The register proposed extending the pre-check "keeping the existing consent-gated
Connect-existing routing." That routing cannot carry an email match — it is phone-keyed
end to end:

- the admin form's 409 handler calls `sendConnectRequestForThisPhone(phone)`
- `eq_cards_request_worker_access(p_org_id, p_phone, p_note)` has **no email parameter**;
  it matches `auth.users.phone`
- on a miss it does **not** raise — it inserts an `org_access_requests` row with
  `worker_user_id = NULL`

On this path the phone matched nobody by definition, so reusing code `existing_account`
would have filed a pending request addressed to no one and reported it to the admin as
sent — strictly worse than the silent link it was meant to fix. #1935 therefore returns a
**distinct** code, `existing_account_email`, which falls through to the form's existing
generic branch (`setErr(detail ?? errMap[raw] ?? raw)`), so no client change is needed —
the same shape #1934 uses for `ambiguous_identity_match`.

**Why the blast radius is smaller than it looks.** Phone is already mandatory at this
endpoint (`create-worker-invite.ts`, `if (!rawPhone) return json(400, …)`), so the phone
pre-check already runs on *every* invite. A multi-org tradie re-invited on their real
mobile is therefore *already* turned away and routed to consent-gated Connect existing
today. #1935 makes email behave the way phone already does rather than adding a new class
of refusal, and `0073`'s "reuse the real row, never spawn a parallel one" intent is
untouched — Connect existing reuses that same row, with consent. The cost is one real
friction case: an admin inviting a genuinely new person who shares a company email gets a
clear 409. Email is optional on the form, so re-submitting without it is the workaround,
and the `detail` string says so.

**Normalisation is byte-identical to the resolver's**, deliberately: `lower(w.email)`
against `lower(NULLIF(TRIM(COALESCE(p_email,'')), ''))` — the stored column lowercased but
**not** trimmed. A positive in the pre-check therefore always agrees with what the resolver
would itself match. Trimming `w.email` in the helper would 409 on rows the resolver would
not match.

> ⚠️ **Sequencing.** The Netlify function calls the new RPC, so the migration must be
> applied **before or with** the deploy. Merge-then-forget leaves every invite that
> carries an email failing on `Failed to check existing accounts`.

**CLOSED — the email half is LIVE, 2026-09-15.** `eq_cards_worker_claimed_by_email`
applied to jvkn **09:49:46Z**; [eq-shell #1935](https://github.com/eq-solutions/eq-shell/pull/1935)
merged 09:48:30Z and its deploy **published 09:54:52Z** (Netlify `commit_ref` = `9ba99644`,
state `ready` — verified by commit ancestry, not elapsed time). The migration landed **five
minutes before** the code that calls it went live, so the 500 window never opened.

Function verified live: `STABLE`, not `SECURITY DEFINER`, `service_role` EXECUTE only
(`authenticated` and `anon` both false) — identical posture to its phone sibling. Behaviour
spot-checked against real rows: a claimed worker's email → true, uppercased → true,
space-padded → true, an *unclaimed* stub's email → false, unknown/empty/NULL → false.
**74 of jvkn's 107 workers are claimed and carry an email**, so this refusal has a real
surface rather than a hypothetical one.

> ### ⚠️ A warning in an earlier version of this note was WRONG — recorded because the
> ### reasoning failure is reusable
>
> That version said dispatching `control-plane-migrate.yml` "would replay all 12"
> un-ledgered eq-shell migrations, against the replay hazards
> `eq-shell/supabase/CONTROL-PLANE-LEDGER.md` names (its items 3 and 4). **It would not.**
> The real dispatch applied **exactly 1 migration, skipped 165, failed 0**
> ([run 34954639340](https://github.com/eq-solutions/eq-shell/actions/runs/34954639340)) —
> `migrate-control-plane.mjs` skips anything holding a ledger row, so the named hazards were
> never reachable. Two mistakes produced that warning: a `string_agg` ledger query whose
> result came back **truncated**, read as if it were complete; and treating
> `CONTROL-PLANE-LEDGER.md`'s header claim — "This tree has **no CI apply path**: files are
> applied by hand" — as current. **That header is stale.** There is a CI apply path, it is
> `control-plane-migrate.yml`, and it works.
>
> **The real hazard sits elsewhere, and it is worth keeping.** Those 12 files got their
> ledger rows at **09:40:22–09:40:44Z** from a `--bootstrap` run
> ([34953767228](https://github.com/eq-solutions/eq-shell/actions/runs/34953767228)), whose
> own banner reads *"will stamp unrecorded files as already-applied, **run no SQL**."* That is
> exactly what `migrate-control-plane.mjs`'s header warns against: *"running it again after
> real new migrations have been added (and not yet applied) would wrongly mark them applied
> too."* A file stamped that way is **permanently invisible to the pipeline** and will never
> run. **Checked, and this time it was benign:** all 11 non-`0173` files were verified live
> by object existence or function-body marker (`trg_sync_tenants`, `trg_sync_organisations_tier`,
> `eq_cards_cancel_my_access_request`, `organisations.tenant_id NOT NULL`,
> `on_auth_users_insert_dedup`, the recycle-review phone column, `_eq_intake_check_tenant_match`'s
> fail-closed body, plus `v_requested_field_slug` / `archived` / `v_email_match_count` /
> `review_not_pending` markers in the four replace-only ones). Every one already applied by
> hand — the bootstrap only papered over records, not behaviour. **Next time nobody may check.**
> Treat `--bootstrap` on this tree as a one-time cutover, never a way to quiet a dirty plan.
>
> **Also corrected: `0173`'s own provenance.** The 09:08 eq-cards dispatch cited by an earlier
> version of this row ran with `plan: true` — it printed "5 pending", changed nothing, and
> still concluded **success**. `0173` really landed 09:30:58Z. A green workflow is not evidence
> a migration applied; the function body is.

**Still filed nowhere: the pre-check 409s themselves.** Neither the phone check nor the
new email one writes an audit row, so "this person already has an account" refusals are
absorbed silently. That is the half of the Group B note below which that investigation
confirmed as correct, and #1935 does not change it — it deliberately mirrors its phone
sibling's shape. #1934 logs only the `>1` refusal. Tracked separately.

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

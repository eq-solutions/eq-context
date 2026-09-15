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
| **LIVE** | Queried against the running database on 2026-09-15 (`pg_get_functiondef` or a real row count) |
| **SRC** | Read from committed source only. For jvkn `public`/`shell_control` functions, treat as a lead — live may differ |
| **FIXED** | Closed by a merged PR, named |
| **OPEN** | Has an owner/PR/task, named |

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
| `app_data.field_people_iud()` INSERT | eq-field | `coalesce(v_tid, '<that plane's own tenant uuid>')` — writes a real roster row to that tenant. Caused the SKS demo-candidate leak (2026-09-10) and its recurrence (2026-09-15) | **OPEN** — partial guard in `20260910_field_people_iud_null_tenant_guard.sql`; general fix is `task_9b876f68` |
| `field_people_iud()` UPDATE/DELETE | eq-field | `coalesce(v_tid, tenant_id)` — the tenant predicate becomes a tautology, so the write is unscoped | SRC |
| `field_people_removed_iud()` | eq-field | same tautology — restore/purge of a removed person runs unscoped | SRC |
| `_eq_intake_check_tenant_match()` | eq-shell (jvkn) | **Guard fails open.** `(auth.jwt()->…->>'tenant_id')::uuid <> p_tenant_id` is NULL when the claim is absent, so the `IF` never fires and the tenant check silently passes. **But it has zero callers on jvkn** — see the note below; fixing it alone changes nothing | **LIVE** |
| `eq_intake_find_template_by_signature(p_tenant_id, …)` | eq-shell (jvkn) | The *actually reachable* version of the row above: `authenticated`-executable, `SECURITY DEFINER`, takes a caller-supplied tenant id and never compares it to the caller's claim. Cross-tenant read of intake templates | **LIVE** |
| `custom_access_token_hook` phone-fallback | eq-cards (live copy) | Falls back to phone match when the uid lookup misses; `tenant_id = coalesce(last_active_tenant_id, tenant_id)` | **OPEN** — [eq-shell #1925](https://github.com/eq-solutions/eq-shell/pull/1925), awaiting Royce |
| `resolveTenantRoute` | eq-cards | `originOrgId ?? defaultOrgId` — a null origin silently defaults to SKS | SRC |
| `verify-pin.js` ~789 | eq-field | Signed claim's tenant not in `DATA_TENANT_IDS` → falls back to **client-supplied** `body.tenantSlug`; mismatch is warn-only, does not block | SRC |
| `app-state.js` ~127 | eq-field | Unmatched hostname → `find(slug==='eq') || allOrgs[0]` — an arbitrary org if no `eq` exists | SRC |
| `shell-handoff-provision.ts` ~133 | eq-shell | A *failed* memberships fetch defaults the session to the user's home tenant (often `__personal__`) | SRC |
| `staff-resync-licences.ts` ~111 | eq-shell | `body.tenant_id ?? session.tenant_id` — caller-supplied tenant, silent default | SRC |
| `eq_cards_auto_provision`, `eq_cards_claim_invite` | eq-cards | Default to the `is_personal = true` tenant, chosen by `LIMIT 1` | SRC |
| `send-digest-test.js` ~80 | eq-field | Unset env → hardcoded SKS uuid | SRC |

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
| `eq_cards_find_or_create_worker_for_invite` | eq-cards | `ORDER BY (w.user_id IS NOT NULL) DESC` — **prefers an already-claimed worker**, so an invite can attach to someone else's account. Writes no flag row | **LIVE** |
| `eq_cards_link_or_create_worker` | eq-cards | Ranks by credential count then `created_at`, `LIMIT 1` | **LIVE** (does write `identity_collision_flags`) |
| `roster-match.ts` `findRosterMatch` | eq-shell | `matches.find(active) ?? matches[0]` | SRC |
| `accept-invite.ts` ~269 | eq-shell | `phoneStubs?.[0]` — first of N phone-variant matches, no ambiguity check | SRC |
| `resolve_invite_auth_identity` | eq-shell | Oldest auth user wins | SRC |
| `eq__caller_staff_id`, `eq__caller_actor_staff_id` | eq-field | `LIMIT 1` with no `ORDER BY` — two staff rows sharing a `user_id` resolve arbitrarily | SRC |
| `eq_cards_admin_upsert_worker` | eq-cards | Same silent tie-break | SRC |
| `backfill-worker-links.ts` ~161 | eq-shell | Builds an email→user Map; duplicate emails last-write-wins | SRC |

## Shape 3 — Ambiguity resolved by doing nothing, invisibly

Safer than guessing, but indistinguishable from success.

| Site | Repo | Behaviour | Verified |
|---|---|---|---|
| `link_pending_invites` email branch | eq-cards | Claims only when exactly one match; 0 or >1 silently skipped, no flag | SRC |
| `workers-canonical-sync` `findStaffId` | eq-cards | ≥2 adoptable → no match → creates a new record instead | SRC |
| `cards-approve-staff.ts` `findExistingStaff` | eq-shell | Anything but exactly one match falls through and mints a duplicate `staff_id` | SRC |
| `field_teams_iud`, `field_team_members_iud`, `field_team_supervisors_iud` — DELETE | eq-field | Null claim → `= NULL` → matches zero rows → **reported as success** | SRC |

## Shape 4 — Errors swallowed, so the failure mode is "allow"

| Site | Repo | Behaviour | Verified |
|---|---|---|---|
| `custom_access_token_hook` | eq-cards/eq-shell | Whole body wrapped `EXCEPTION WHEN OTHERS → RETURN event` — any error silently mints a token with no claims | SRC |
| `tg_fulfil_access_requests_on_claim` | eq-shell | All errors swallowed | SRC |
| `eq__caller_uid` | eq-field | Swallows exceptions → NULL, which downstream reads as a visibility decision | SRC |
| `_shared/field-person.js` ~36 | eq-field | Every failure path returns `null` with **no logging at all**; the caller then substitutes a display name derived from the email local-part | SRC |

## Shape 5 — Unbounded claim

| Site | Repo | Behaviour | Verified |
|---|---|---|---|
| `link_pending_invites` org_memberships branch | eq-cards | Unbounded `UPDATE` claiming all pending invites matching | SRC |
| `shell-login-phone-otp.ts` email self-heal | eq-shell | Claimed every worker row sharing the email, fire-and-forget with errors discarded | **FIXED** (gated) by [#1923](https://github.com/eq-solutions/eq-shell/pull/1923) — now requires `email_confirmed_at`. The unbounded `.eq('email').is('user_id',null)` update itself is unchanged; worth a second look |

### Corrected — reported but NOT live

| Site | Reported | Actual |
|---|---|---|
| `eq_cards_submit_access_request` | Unbounded `UPDATE public.workers SET user_id = auth.uid()` claiming every worker with the phone | **Not live.** Live body does not touch `workers`. Finding came from `2026_06_25c`, superseded per CONTROL-PLANE-LEDGER. Do not re-report |

## Shape 6 — The target pattern (holds for review)

Four sites write to a review queue. Only the first actually **stops**.

| Site | Queue | Stops? | Verified |
|---|---|---|---|
| `handle_phone_dedup()` — stale >90d, and live-duplicate branches | `identity_recycle_review` | **Yes** — inherits nothing, holds | **LIVE** |
| `link_pending_invites` phone branch | `identity_recycle_review` | Yes | SRC |
| `fn_link_worker_on_user_create` | `phone_link_review` | **No — flags the phone disagreement, then claims the worker anyway** | SRC |
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
| 2 | `eq_cards_find_or_create_worker_for_invite` prefers an already-claimed worker | **Stop and ask when >1 match** | Pending. First application of staged rule 2. Needs a design call: there is no review queue for this case today, so "ask" has to mean something concrete to the admin |
| 3 | The `coalesce`-to-own-tenant fault, present in every tenant's templated copy | **Roll out company by company** | Relayed to `task_9b876f68`, which already owns it. Not duplicated here |
| 4 | [#1925](https://github.com/eq-solutions/eq-shell/pull/1925) — `custom_access_token_hook` phone-fallback logging | **Merge** | Merging on green; all checks pass except the Netlify preview |
| 5 | Should admin-invite capture a phone number? | **Make it required** | Pending — `invite-user.ts` plus the admin invite form |
| 6 | Adopt the policy | **Adopt rules 1/3/4 now, stage rule 2** | Done — see the Policy section above |

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

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
| `_eq_intake_check_tenant_match()` | eq-shell (jvkn) | **Guard fails open.** `(auth.jwt()->…->>'tenant_id')::uuid <> p_tenant_id` is NULL when the claim is absent, so the `IF` never fires and the tenant check silently passes | **LIVE** |
| `custom_access_token_hook` phone-fallback | eq-cards (live copy) | Falls back to phone match when the uid lookup misses; `tenant_id = coalesce(last_active_tenant_id, tenant_id)` | **OPEN** — [eq-shell #1925](https://github.com/eq-solutions/eq-shell/pull/1925), awaiting Royce |
| `resolveTenantRoute` | eq-cards | `originOrgId ?? defaultOrgId` — a null origin silently defaults to SKS | SRC |
| `verify-pin.js` ~789 | eq-field | Signed claim's tenant not in `DATA_TENANT_IDS` → falls back to **client-supplied** `body.tenantSlug`; mismatch is warn-only, does not block | SRC |
| `app-state.js` ~127 | eq-field | Unmatched hostname → `find(slug==='eq') || allOrgs[0]` — an arbitrary org if no `eq` exists | SRC |
| `shell-handoff-provision.ts` ~133 | eq-shell | A *failed* memberships fetch defaults the session to the user's home tenant (often `__personal__`) | SRC |
| `staff-resync-licences.ts` ~111 | eq-shell | `body.tenant_id ?? session.tenant_id` — caller-supplied tenant, silent default | SRC |
| `eq_cards_auto_provision`, `eq_cards_claim_invite` | eq-cards | Default to the `is_personal = true` tenant, chosen by `LIMIT 1` | SRC |
| `send-digest-test.js` ~80 | eq-field | Unset env → hardcoded SKS uuid | SRC |

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

Closed by [eq-shell #1927](https://github.com/eq-solutions/eq-shell/pull/1927),
which adds `check-review-queues.ts` (21:55 UTC, alert-only, leads with the
oldest row's age).

The recycle queue's emptiness is the sharper lesson: with no reader, *"the
detector works"* and *"the detector has never fired"* were indistinguishable
for months.

---

## Proposed policy — NOT YET ADOPTED

Offered for Royce's decision. Nothing below has been applied beyond #1927.

> **Ambiguity is a stop condition, not a default-value problem.**

1. **Never fabricate a tenant.** If the tenant cannot be established from a
   trusted signed claim, raise. Do not fall back to own-tenant, home-tenant,
   personal-tenant, an Origin header, a request-body field, or a hardcoded
   uuid. A routing mistake should fail loudly rather than quietly become
   another tenant's data.
2. **One match links; zero or many holds.** Any identity match that resolves to
   ≠1 candidate writes a review row and stops. `LIMIT 1` as a tie-break on a
   *person* is never correct.
3. **A flag is not a decision.** If a collision is worth recording, it is worth
   stopping for. "Log it and proceed" is the worst of both — it creates the
   duplicate *and* the paperwork, and Shape 6 shows two sites doing exactly
   that today.
4. **Guards fail closed.** `EXCEPTION WHEN OTHERS → RETURN event` on an auth
   hook converts any error into "allow". Catch narrowly or not at all.
5. **Every review queue has a watcher.** True as of #1927; keep it true when
   adding a queue.

Rule 2 is the expensive one and should be staged: it changes behaviour at ~8
sites and will surface latent duplicate data that is currently being silently
absorbed. Rules 1, 3, 4 are mostly additive.

## Decisions needed from Royce

| # | Decision | Why it needs you |
|---|---|---|
| 1 | `_eq_intake_check_tenant_match` fails open — fix is roughly one line (`IS DISTINCT FROM` plus an explicit null check) | It is a *security guard*. Tightening it will start rejecting any caller that legitimately has no tenant claim — unknown blast radius until we look at who calls it |
| 2 | `eq_cards_find_or_create_worker_for_invite` prefers an already-claimed worker | Changing the `ORDER BY` changes which human an invite attaches to. Product call, not a refactor |
| 3 | `task_9b876f68` — the general "coalesce to own tenant" fix, across every tenant's templated copy, not a SKS-only patch | Touches every tenant plane; needs a staged rollout decision |
| 4 | [#1925](https://github.com/eq-solutions/eq-shell/pull/1925) — `custom_access_token_hook` phone-fallback logging | Already open, already awaiting your go |
| 5 | Should admin-invite (`invite-user.ts`) capture a phone number? | The original question from the Aditi duplicate-login investigation. Phone is the only key `handle_phone_dedup` can match on, so an admin-invited person is structurally invisible to it. Still never formally put to you |
| 6 | Adopt the policy above, in whole or in part | Rules 1/3/4 are cheap. Rule 2 is the one with real blast radius |

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

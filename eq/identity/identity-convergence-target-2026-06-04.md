---
title: EQ — Identity Convergence Target
owner: Royce Milmlow
last_updated: 2026-06-04
scope: Declares the ONE canonical identity + membership record for the EQ suite and the retire-list / demolition schedule for the overlapping stores. Companion to IDENTITY-MODEL.md (the model) and onboarding-portable-identity-2026-06-04.md (the onboarding direction). Purpose — convert identity-store accretion into directed motion: every future change is checked against this target.
read_priority: high
status: live
related:
  - eq/identity/IDENTITY-MODEL.md
  - eq/identity/onboarding-portable-identity-2026-06-04.md
---

# EQ — Identity Convergence Target

**Status:** accepted.

**Status:** Accepted direction, authorised by Royce 2026-06-04. This sets the *destination*; execution is scheduled (below), not immediate. The point is cheap and now: stop building sideways.

## 1. Why this exists

A 2026-06-04 live audit of eq-canonical found a person's identity/access smeared across **six** stores, with the membership fact stored **twice and already divergent**. Without a declared truth, every onboarding/login change adds coupling the eventual unification must unwind. This doc names the truth so future work moves *toward* it.

### Live evidence (eq-canonical, 2026-06-04)
| Store | Role today | Rows |
|---|---|---|
| `auth.users` (GoTrue) | login transport | 7 |
| `shell_control.users` | identity authority | 5 |
| `shell_control.user_tenant_memberships` | membership (login side) | 5 users |
| `public.org_memberships` | membership (Cards side) | 4 users |
| `public.workers` | operational HR record | 38 (1 claimed) |
| `public.profiles` | legacy claim model (0010) remnant | 1 |

`auth.users`↔`shell_control.users` email drift = **0** (not currently drifting). Phones mapping to >1 auth uid = **0** (the ambiguity is latent, not yet live — see §5). The membership split (**5 vs 4**) is legacy seeded data; the Phase-1 claim bridge writes both copies *in sync*, so it is a static inconsistency to schedule away, not an active bleed.

## 2. The canonical target

| Concern | Canonical home | Everything else |
|---|---|---|
| **Identity** (who this human is) | `shell_control.users` | `auth.users` = GoTrue **transport only** (disposable; one human may have several auth uids, reconciled into one `shell_control.users`) |
| **Membership** (which tenants, what role) | `shell_control.user_tenant_memberships` | `public.org_memberships` = **retire** → becomes a *view* over the canonical table |
| **Operational HR record** (qualifications, contacts, roster data) | `public.workers` | linked to identity by `workers.user_id` → `shell_control.users.id`; **not** an identity store |
| **Profile (legacy)** | — | `public.profiles` = **retire** (fold any live data into `workers`) |

One-liner: **`shell_control.{users, user_tenant_memberships}` is the identity+membership truth. `auth.users` is transport. `public.workers` is the HR record linked by `user_id`. `public.org_memberships` + `public.profiles` are on the retire-list.**

This is consistent with `IDENTITY-MODEL.md` (§3.2 auth-entity-vs-operational-entity; §6 session/JWT) — it makes the membership side of that model explicit and schedules the duplicates out.

## 3. Rules going forward (the cheap guardrail)

1. **No new identity or membership store** without updating this doc and §2.
2. **Writes of identity/membership facts target the canonical home.** A non-canonical copy must be a *derived* view or be explicitly justified as a temporary bridge with a retirement line in §4.
3. **Reads should migrate to the canonical home** as RLS/policies are touched (opportunistic, not a big-bang).
4. Every onboarding/login PR states which row of §2 it writes and confirms it moves *toward* the target, not sideways.

## 4. Demolition schedule (execute with real-usage evidence, not before)

Deliberately **deferred** — pilot velocity first; harden once the model is proven (per the "build for ourselves / don't out-build the load" principles in `ops/decisions.md`).

- **P-now (done):** Phase-1 claim bridge creates the `shell_control` identity + membership on claim (this is durable — the hook in P2 *reads* it). See onboarding doc + eq-cards migration `0016`.
- **P2-a — `public.org_memberships` → view** over `shell_control.user_tenant_memberships`; migrate Cards RLS reads. Removes the double-write / 5-vs-4 divergence.
- **P2-b — enable `custom_access_token_hook`** on eq-canonical (after resolving GoTrue-vs-own-mint, onboarding doc §5.3) so the JWT carries `tenant_id` natively for all methods; **retire the per-method `shell-login-phone-otp` exchange**.
- **P3 — retire `public.profiles`**; confirm no remaining reads; fold the 1 legacy row into `workers`.

Sequence note: P2-a and P2-b are independent and can interleave; both want real pilot usage first.

## 5. Open risks / watch-items

- **RLS dependence on `public.*`.** If Cards' row-security leans so hard on `public.org_memberships`/`workers` that `shell_control`-as-truth is impractical, the target shifts. Validate as RLS is touched (P2-a is the test). Current evidence (and IDENTITY-MODEL) says shell_control is right.
- **Phone-as-reconciliation-key.** 0 multi-uid phones today, but the seed case (Royce: phone set on the email-seeded uid `7e4426bb`, while phone-OTP authenticates as `39c95a01`, reconciled only by phone-match) shows the latent failure. The claim bridge's "phone collision → NULL" guard is a *silent* disable of phone-login on exactly that ambiguity — acceptable for pilot, a landmine at scale. Revisit under P2-b.
- **Role default = `employee`.** The claim bridge defaults every bridged worker to `employee`. Correct for SKS's own team (pilot); **over-permissioned for actual labour-hire tradies** (`labour_hire` tier). Fix before any outside-SKS / labour-hire rollout: the invite should carry the intended role and the bridge should honour it (default to the *safest* tier when unknown).

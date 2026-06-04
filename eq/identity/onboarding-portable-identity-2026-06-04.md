---
title: EQ — Low-Friction Onboarding & Portable Worker Identity
owner: Royce Milmlow
last_updated: 2026-06-04
scope: Cross-product design for how a worker enters EQ (Cards-first), carries one identity across employers, and progressively secures it. Extends eq/identity/IDENTITY-MODEL.md — pulls its §11.2 multi-tenant-membership v2 item forward and flags the GoTrue/own-mint reconciliation. Governs onboarding friction, consent, recovery, and where identity-lifecycle policy lives.
read_priority: high
status: proposed
related:
  - eq/identity/IDENTITY-MODEL.md (authoritative model this extends)
  - product-adoption-strategy (memory) — admin pre-populates, workers consume
  - eq-phone-otp-login-wiring (memory) — the live Cards phone-OTP chain
---

# EQ — Low-Friction Onboarding & Portable Worker Identity

**Status:** Proposed direction, authorised by Royce 2026-06-04 (conversation steelman/critique). Implementation is **phased** (below); Phases 2–3 trigger a deliberate v2 bump of `IDENTITY-MODEL.md` when they land.

## 1. The goal in one sentence

A tradie goes from "tap a link / get a text" to "seeing their cards" in the fewest possible steps — no password, no email gauntlet, no app-store install — and is asked for more (email/password) only later, only when its value is self-evident.

## 2. The principle: friction floor, not friction zero

The objective is **lowest friction *above a necessary floor*** — not lowest friction absolute. The floor is set by the payload: Cards holds licences, right-to-work, emergency contacts — sensitive PII under the Australian Privacy Principles. Friction below the floor is not a feature; it is deferred liability (wrong person sees a stranger's licences; lost-SIM lockout from sensitive records; unsustainable SMS cost/dependency).

Friction is **distributed across actors**. Cutting the worker's first-screen friction can raise admin friction (enter every mobile perfectly) or support friction (lockouts). Minimise *total system* friction, not the worker's first screen alone. (The `phone = null` defect that broke phone-OTP login on 2026-06-04 was exactly this failure mode.)

## 3. The model decided

### 3.1 Portable identity, not per-employer record
One human = **one identity** with **many tenant memberships**. A tradie doing labour hire for SKS this week and another firm next week logs into the **same** EQ Cards and sees both gigs; licences carry across. This pulls `IDENTITY-MODEL.md` §11.2 ("multi-tenant membership", currently v2 backlog) forward as the direction. Note the live `shell_control` schema **already has `user_tenant_memberships`** — the capability is partly built ahead of the doc (verify-first: live wins).

This makes **phone-as-personal-anchor correct, not a compromise**: the mobile belongs to the *person*, so it is a sensible portable key — subject to the assurance caveat in §6.

### 3.2 Authorisation vs login convenience (decoupled)
- The **claim code** an admin issues is the *authorisation event* — high-assurance proof that this human may see this worker's record. One-time, low-friction (tap a link).
- The **phone** is the *convenience credential* for getting back in. Repeatable, low-friction.
- **Email is a recovery channel, captured optionally early — not a login requirement.** This is the single highest-leverage, lowest-cost addition: it removes the lost-SIM catastrophe without touching first-run friction.

### 3.3 Consent per employer (with data scoping)
When a second employer's claim resolves to an existing identity, **the worker approves** the new membership — and the approval scopes *what that employer sees* (licences + right-to-work, not emergency contacts or another employer's notes). The tickbox is two controls in one: a data-sharing gate **and** a soft assurance check. (It guards the worker from rogue *employers*; it does **not** guard the identity from a rogue *phone holder* — see §6.)

### 3.4 Email/password forced by **event, not timer**
Never hard-block the core action (showing a card). Nag, banner, degrade — but the wallet always opens. Hard-require a recovery email only at **risk events** where its value is self-evident:
- phone-number change ("add an email so you don't lose your cards"),
- adding a 2nd employer ("secure the cards you're about to carry between employers"),
- export / data movement.

A calendar deadline (the "14-day wall") is rejected: it lands at random — often the worst — moments (on a roof, needing to show a ticket) and manufactures churn. Frame every prompt as **recovery value**, never "complete your account."

### 3.5 Lifecycle policy lives in the control layer
Decompose "policy" into three homes:
1. **Rules (definition)** → control plane (`shell_control.platform_config` or a policy table). Configuration, not code. Change policy without shipping an app. **No app hardcodes "14 days" or "require email."**
2. **State (where each user is)** → control plane (`shell_control.users` + membership/consent tables).
3. **Enforcement (acting on it)** → distributed but **read-only against the control layer.** The **Shell** evaluates ("is this identity compliant / what's required next") and **projects the verdict into the JWT via the `custom_access_token_hook`** (signed, consistent across the suite). Apps react to a flag (`recovery_required`, `grace_expires_at`, `consent_pending`); they never re-derive policy.

**Security guardrail:** a UI wall is a *nag*; any genuine gate (e.g. block export until recovery email set) must **also** be enforced server-side in the control-plane RPC/RLS — never trust the client. Most of the list is nags; data-movement is a real gate.

**Naming guard:** this is `eq-canonical` → `shell_control` (browser *control* plane), **not** `eq-canonical-internal` (server-only *data* plane). Identity/lifecycle is control-plane.

## 4. Phased build (right schema now, enforcement later)

Don't out-build the load. Get the data model right immediately so nothing needs migrating; defer the policy engine until usage demands it.

**Phase 1 — thin slice (pilot, now)**
- Phone-OTP login + claim flow + **optional recovery-email capture** (pre-fillable by admin; nag only).
- Persist phone, recovery email, and consent records in `shell_control` so portability/consent/recovery *can* exist.
- No policy engine, no consent-scoping UI yet. Goal: activation + learning.

**Phase 2 — hook + control-plane policy**
- **Enable `custom_access_token_hook` on eq-canonical** → `tenant_id` (and lifecycle flags) native in the JWT for *all* login methods; **retire the per-method shell-exchange bridges** (the `shell-login-phone-otp` bridge that broke on 2026-06-04).
- Move lifecycle rules+state into `shell_control`; Shell evaluates and projects flags.
- This is the deliberate **v2 bump of `IDENTITY-MODEL.md`** (multi-tenant membership formalised; §11.2 promoted from backlog).

**Phase 3 — consent-scoping, recovery, event-forcing**
- Per-employer consent with data-visibility scoping.
- Event-driven email forcing (§3.4).
- Full recovery flow (self-service via email; admin re-issue claim as employer-scoped fallback).
- Server-enforced gates (RLS/RPC) for the real gates; UI nags read the flag.

## 5. Open questions to design deliberately (not assume)

1. **Identity resolution** — "same human, second employer" assumes reliable matching. Phone is convenient but a **weak uniqueness anchor** (carriers recycle numbers; handsets are shared). The consent tickbox covers the worker's side; the **matching rule itself** (when employer B's claim resolves to an existing identity) is unspecified and is the most likely spot for a data-exposure bug at scale. Needs a real design — likely claim-code-binds-to-identity + worker confirmation, with phone as a hint, not the key.
2. **Recovery flow** — portability makes recovery a **platform** responsibility (no single employer owns the identity). "Lost phone, prove it's you, get back in" is currently hand-wavy. It is the next design debt; becomes support-load + security surface at scale.
3. **GoTrue vs own-mint reconciliation (load-bearing).** `IDENTITY-MODEL.md` §9 states identity is **"Not Supabase-Auth-managed"** — own JWTs minted against `public.users`. But Cards' phone-OTP path **uses Supabase GoTrue** (`signInWithOtp(phone)`, `verifyOTP(sms)`) to deliver/verify the code, creating an `auth.users` row, then swaps the session for a shell-minted JWT. So GoTrue is currently an **OTP transport**, while identity *authority* stays `shell_control.users`. The open decision: keep GoTrue strictly as transport (auth.users is disposable), or accept `auth.users` as a parallel store (risk: it drifts from `shell_control.users`). This must be reconciled before Phase 2, because the token hook runs inside GoTrue's mint path. **Docs lag reality here — verify against live before building.**

## 6. Threat/assurance note

Portability *raises* the assurance floor: a recycled phone number that resolves to a portable identity exposes licences aggregated across **every** employer the real person worked for — bigger blast radius than a single-employer view. The property that delivers low friction (one portable key) is the same one that raises the security bar. Both must be designed; optimising one and ignoring the other is the trap.

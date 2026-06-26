---
title: EQ Cards — Worker Platform Direction
owner: Royce Milmlow
last_updated: 2026-06-15
scope: Design record for the decision that Cards is the worker-facing EQ platform and Core is employer-only. Covers the three UX models considered, the chosen direction, the immediate build (tenant tile), and the long-term roadmap.
read_priority: critical
status: live
---

# EQ Cards — Worker Platform Direction

Decision logged 2026-06-15. ADR entry in [ops/decisions.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/decisions.md).

## The problem this resolves

Cards was embedded in Shell as an iframe. This produced three unsolvable problems:

1. **Auth seam**: Shell has an HttpOnly cookie session; Cards has a GoTrue JWT session. They cannot share a session. `gotrue_dart` 2.20+ rejects shell-minted JWTs (calls `getUser()` on `setSession()`, requires a real `auth.sessions` row). Every workaround (postMessage handoff, server-side `createSession`, HMAC relay) either violates the ownership model or fails at the Dart layer.

2. **Ownership inversion**: An employer's control-plane app (Shell) hosting a worker's canonical-layer app (Cards) means the employer's system can grant, deny, or limit access to the worker's own wallet. Wrong model.

3. **Audience mismatch**: Shell is desktop-first and employer-facing. Cards is a mobile PWA and worker-facing. Embedding a mobile app in a desktop admin interface creates UX compromises in both directions.

The root cause: the iframe approach assumed Cards is a feature of Shell. It is not. Cards is a separate product for a different audience.

## Three models considered

### Model A — Cards as home, tenant tile links to Core/Field (chosen)

Worker installs the Cards PWA. Their wallet is the primary view. If they are aligned with an employer tenant (e.g. SKS), a "Your workplace" tile appears at the bottom with a link to the employer's portal (`core.eq.solutions/sks`). Tapping it opens the portal in a new tab.

```
Cards (worker's home)
├── Wallet — licences, certs, employment record
└── Your workplace
    └── SKS Technologies → opens core.eq.solutions/sks
```

**Why chosen:** Wallet is permanent. The job is temporary. Workers install Cards once; employer affiliations come and go as tiles. Matches the ownership model exactly. The auth seam (separate sessions) is acceptable — 30-day sessions mean re-authentication is rare in practice.

### Model B — Core/Field as home, Cards linked as a section

Field is the daily work tool (timesheets, roster, availability). Cards is a tile inside Field linking to the wallet.

**Rejected:** Most workers join via an employer invitation, so Field feels like the natural entry point. But the wallet lives inside the employer's app — this inverts the ownership model. The worker's personal wallet should not be accessed through their employer's portal.

### Model C — Two fully standalone PWAs, one identity

Cards and Field are both installed on the worker's home screen. Each links to the other at the bottom. No "home" app — just two tools for two jobs. Same phone number authenticates both.

**Viable long-term state, not the immediate build.** When Field has a mature mobile worker-facing experience, C is the natural end state. Right now Field does not have a standalone worker mobile app, so C requires building Field from scratch for mobile. The tenant tile (Model A) is the bridge until then.

## Chosen direction: Model A

### Platform map

| | Core (`core.eq.solutions`) | Cards (`cards.eq.solutions`) |
|---|---|---|
| Audience | Employers, admins, schedulers | Workers, tradies |
| Stack | React SPA | Flutter PWA |
| Primary device | Desktop | Mobile |
| Auth | Shell HttpOnly cookie session | GoTrue phone OTP + `custom_access_token_hook` |
| Identity backing | `shell_control.users` | `shell_control.users` (same table) |
| Owns | Tenant config, dispatch, compliance, org admin | Worker identity, wallet, credentials, consent |
| Links to | Cards (read-only employer view of worker data, consent-gated, future) | Core/Field (tenant tile, link-out) |

### The two-auth-path model

Both paths are backed by `shell_control.users`. The phone number is the shared identity key.

```
Worker authenticates to Cards
→ GoTrue phone OTP
→ auth.users row in eq-canonical
→ custom_access_token_hook reads shell_control.users
→ JWT carries tenant_id, eq_role
→ 30-day refresh token (session persists across app opens)

Worker authenticates to Shell (for Field)
→ Shell OTP flow → shell_control.users lookup
→ HttpOnly eq_shell_session cookie
→ Shell routes to tenant context (e.g. /sks → Field)
→ Session persists independently of Cards session
```

These are separate sessions. The phone number guarantees they resolve to the same `shell_control.users` row. The worker does not need both sessions active simultaneously in normal use — they use Cards for their wallet, they use Shell when their employer requires Field access.

### Auth seam explicitly accepted

The two-auth-path model is not a gap to close. It is the correct model given:
- Different stacks (React vs Flutter Dart) prevent a shared session without platform-level bridges
- The ownership model prohibits Shell creating or controlling Cards sessions
- The practical friction is low (30-day sessions → re-auth ~monthly per app)

If future data shows re-authentication is a real drop-off point (measurable via Sentry/PostHog), the phone-hint auto-OTP approach is the first thing to trial: Shell postMessages the worker's phone to Cards; Cards pre-fills and auto-fires the OTP; worker enters one code. This is possible without violating the ownership model (Shell provides a hint, not a credential; Cards authenticates the worker independently).

## Immediate build: tenant tile

### What to add

**DB:** One column on `shell_control.tenants`:
```sql
ALTER TABLE shell_control.tenants
  ADD COLUMN IF NOT EXISTS portal_url text;

-- Seed SKS
UPDATE shell_control.tenants
SET portal_url = 'https://core.eq.solutions/sks'
WHERE slug = 'sks';
```

**Cards app:** A "Your workplace" section at the bottom of the wallet screen, reading from the worker's active `user_tenant_memberships`. One tile per non-personal tenant, showing the tenant name and a link-out arrow. Tapping opens `portal_url` in a new tab (or system browser on mobile). Hidden entirely for workers with only a personal wallet (no employer affiliation).

**Shell:** Remove `CardsIframe.tsx` from the Shell nav. Replace the Cards tile in the employer nav with a plain external link to `cards.eq.solutions` (for admin staff who want to see the worker-facing app). The `/auth/handoff` route in Cards can remain as a no-op (it redirects to sign-in if no session) but the iframe embedding is gone.

### What NOT to build yet

- Shared session / auto-sign-in from Cards to Shell (30-day sessions make this low priority)
- Employer verification of wallet data from within Cards (consent model — Phase 2 of worker-credentials)
- Worker timesheet entry in Cards (Field's worker features migrate to Cards over time — not this sprint)

## Long-term roadmap signal

As the platform matures, Field's worker-facing features migrate to Cards:

| Feature | Today | Long-term |
|---|---|---|
| View licence wallet | Cards | Cards |
| View job assignments | Shell/Field (employer pushes) | Cards (worker pull, employer push notifications) |
| Submit timesheet | Shell/Field | Cards |
| Set availability | Shell/Field | Cards |
| Employer contact / messaging | Not built | Cards |

Field and Shell retain the employer-admin view of these records. The canonical layer (`eq-canonical-internal` worker-house) is the exchange point: Field writes job assignments and timesheet approvals to worker-house; Cards reads them. The worker never needs to enter Shell to do their job.

This is not a near-term build commitment — it is the direction signal that informs how new worker-facing features are sequenced. If a feature is worker-facing and mobile, it goes in Cards, not in Shell.

## Related decisions and docs

- [ops/decisions.md — 2026-06-15 entry](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/decisions.md) — ADR
- [ops/decisions.md — 2026-06-04 portable identity](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/decisions.md) — upstream decision this extends
- [eq/identity/worker-credentials-model-2026-05-31.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/identity/worker-credentials-model-2026-05-31.md) — ownership model
- [eq/identity/IDENTITY-MODEL.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/identity/IDENTITY-MODEL.md) — v2 bump needed to reflect two-auth-path model
- [eq/cards/canonical-migration/plan.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/eq/cards/canonical-migration/plan.md) — superseded re: SSO/iframe; canonical data migration still in progress

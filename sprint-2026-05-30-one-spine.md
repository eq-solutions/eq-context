---
title: EQ Suite Sprint — One Spine
owner: Royce Milmlow
last_updated: 2026-05-30
scope: The cross-app design/merge/auth sprint plan (Design → Field → Auth)
read_priority: standard
status: live
---

# EQ Suite Sprint — "One Spine"

**Created:** 2026-05-30
**Owner:** Royce Milmlow
**Theme:** Stop maintaining the same thing five different ways. One token source, one codebase per product, one identity spine.
**Shape:** 3 streams, sequenced — **Design → Field → Auth**. Each lands before the next starts. Auth runs last *and* gets an early cheap spike to de-risk it.

**Decisions locked (2026-05-30):**
- Field merge = **codebase only**. SKS is a tenant; SKS data lives in the **SKS Canonical**, not EQ's DB. (Entities stay separate.)
- Auth = **staged re-platform** onto Supabase Auth (approved over harden-in-place).
- Design = **audit-first**, then wire.
- Sequence = Design → Field → Auth.

---

## Discovery findings (ground truth, 2026-05-30)

### Auth — current state
- Login: email + **4-digit PIN**, bcrypt, in `eq-shell/netlify/functions/shell-login.ts`. Optional phone OTP / TOTP.
- Session: 7-day token signed with **HMAC-SHA256** (`EQ_SECRET_SALT`), `eq_shell_session` cookie (Domain=.eq.solutions).
- **5 tiers** (`eq-shell/src/session.ts:30`): `manager` / `supervisor` / `employee` / `apprentice` / `labour_hire`. Permission matrix in `src/permissions/matrix.ts`. `is_platform_admin` flag is orthogonal (short-circuits `useCan()`).
- Separate axes: tenant tier (`trial|standard|advanced|enterprise`), tenant subscription.
- **THREE cross-app handoff modes:** (A) domain cookie SSO, (B) 60s HMAC iframe token (`mint-iframe-token.ts`, hardcoded slug allow-list `['eq','demo-trades','melbourne','sks']`), (C) Supabase JWT (15min, RLS via `app_metadata`).
- Pain: roles defined in ~5 places; **Field lossily maps 5 tiers → 2** (`staff|supervisor`); each app re-implements auth; no shared auth package; inconsistent TTLs.

### Design — current state
- `@eq-solutions/tokens` v1.0.0 is well-built: emits CSS / TS / Tailwind preset / Dart. Tier-aware overrides. CI-enforced in its own repo.
- **Zero apps import it.** All vendor/copy:
  - Shell — hand-ported CSS vars into `src/index.css` (byte-identical now, will drift).
  - Service — vendors `lib/tokens/tokens.css` (Tailwind v4 `@theme`).
  - Cards — vendors `tokens.dart`.
  - **Field — no tokens, on DM Sans not Plus Jakarta Sans (off-brand).**

### Field vs SKS — current state
- ~90% shared ancestry, both vanilla HTML/JS/CSS, identical migrations to the 2026-05-20 split.
- **SKS ahead ~11 releases** (v3.10.37 vs EQ v3.5.23).
- SKS-only modules: `teams`, `pipeline*` (3 files), `safety` + `safety-dashboard`, `project-hours`.
- EQ-only: apprentice tier, regions, forecasting, lazy-loader, site-reports.
- Tenant routing already exists: `TENANT_SUPABASE` map + hostname detection in `app-state.js`.
- Separate Supabase projects: EQ `ktmjmdzqrogauaevbktn`, SKS `nspbmirochztcjijmcrx`.
- **ID mismatch:** SKS core IDs `bigint`, EQ `uuid` (code already coerces with `String()`).

---

## Stream 1 — Design (audit → wire) · FIRST, lowest risk

Not a design problem — an **adoption** problem. One language pasted into five rotting copies.

**Deliverables:**
1. Formal audit doc — per-app consumption method, brand-match, drift risk.
2. Wire real imports of `@eq-solutions/tokens`; delete vendored copies:
   - Shell → `@import` package, remove duplicated vars.
   - Service → import from `node_modules`, delete `lib/tokens/tokens.css`.
   - Cards → consume `tokens.dart` as dependency.
   - **Field → switch DM Sans → Plus Jakarta Sans, adopt token vars** (most visible brand fix).
3. CI drift-guard — fail any PR committing `tokens.*` outside the source repo.
4. Component audit (deferred output) — rank duplicated components (buttons/tables/forms) as brief for a *later* `@eq-solutions/ui` sprint. Look, don't build.

**Why first:** visually inert (colours already identical), and gives Field a clean brand baseline before SKS merges in.

---

## Stream 2 — EQ Field merge (one codebase, SKS as tenant) · SECOND

Codebase unifies; entities stay separate. SKS data → SKS Canonical.

**Hard parts:**
1. Boot-time branding — extract hardcoded inline colours to CSS vars set first in boot (cleaner now that Stream 1 is on tokens). Avoids wrong-brand flash.
2. Boot strategy — merge onto **EQ's lazy-loader**, add SKS modules to manifest (keep perf).
3. Module collisions — namespace + tenant-gate SKS `pipeline*` vs EQ `tender-pipeline`.
4. Safety module — bring in tenant-gated; add its tables to EQ's disabled-table list.
5. Data ETL → SKS Canonical — ID-mapping table for bigint→uuid; migrate people → schedule → timesheets/leave in FK order; normalise "SKS Direct" → "Direct".

**Deliverables:** one repo serving both tenants; SKS's 11-release lead reconciled; branding/boot/modules tenant-safe; SKS data in SKS Canonical via audited migration. Both tenants smoke-tested every step.

**Sizing:** heaviest stream — the ETL and the 11-release reconciliation dominate, not the merge mechanics.

---

## Stream 3 — Login (staged re-platform) · LAST, with early spike

Separate **identity** / **authorization** / **enforcement** (current system tangles all three).

**Target architecture:**
1. Retire the 4-digit PIN as primary; **passkeys-first (WebAuthn)**, magic-link as recovery, PIN as transition fallback only.
2. **Supabase Auth = single IdP per entity.** EQ suite uses one; SKS is its own IdP on SKS Canonical (reinforces entity separation).
3. **One token model** — drop hand-rolled HMAC; embedded apps get identity via shared parent session + a single **token-exchange edge function** (verify-JWT-at-edge → mint project-scoped Supabase JWT).
4. **One role registry** → custom JWT claims via Auth Hook (`app_metadata.eq_role`, `tenant_id`, `is_platform_admin`) → **enforced by RLS everywhere**. Centralized governance, distributed enforcement. 5 tiers unchanged, defined once. Field finally sees all five.

**Why:** new apps get SSO/MFA/full role model for free; kills 5-places-to-edit and Field's lossy 5→2 mapping.

**Staging (auth changes need explicit deploy approval):**
- This sprint (early, cheap, alongside Streams 1–2): build the **shared role registry now** (pure upside, helps Stream 2); spike Supabase-Auth-IdP + passkey in a branch; produce side-by-side comparison.
- Then: shadow-run (new spine issues tokens alongside old, verify parity) → cut over app-by-app behind a flag → retire HMAC last.
- **No production auth change ships without explicit go.**

**Deliverables this sprint:** working spike + comparison; shared role registry in production (safe, foundational); staged cutover plan approved before any app flips.

---

## How the streams reinforce each other
- Shared role registry (Stream 3 spike) is what Field needs to adopt all 5 tiers → feeds Stream 2.
- Tokens-on-Field (Stream 1) gives the merge a clean brand baseline and makes boot-time branding trivial.
- Risky auth cutover blocks nothing in Streams 1–2 — by design.

---

## Definition of done (10/10)
- Every app imports the token package; CI makes drift impossible; Field on-brand.
- One EQ Field codebase; SKS runs as a tenant from it; SKS data in SKS Canonical; both tenants pass smoke tests.
- Supabase-Auth spike proven; role registry live; passkey path demonstrated; staged cutover plan signed off.

## References
- Memory: `project_field_merge_tenant_model`, `project_auth_target_architecture`, `design_eq_profile`, `project_eq_canonical_internal`, `open_loops`.
- Global rules: auth changes need explicit deploy approval; entities never mixed; working-before-refactoring.

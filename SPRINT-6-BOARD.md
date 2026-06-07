---
title: "Sprint 6 Board — EQ Field Auth Hardening: Retire the Anon Model"
owner: Royce Milmlow
last_updated: 2026-06-04
scope: Sprint 6 task board
read_priority: reference
status: live
---

# Sprint 6 Board — EQ Field Auth Hardening: Retire the Anon Model

**Started:** 2026-06-03
**Theme:** Move EQ Field off the public `anon` key onto per-user identity, rewrite RLS to be identity/tenant-scoped, retire the legacy open grants — and in doing so **align the canonical spine** and **unblock the SKS go-live**.

> **The keystone.** One finding gates three goals. EQ Field talks to Supabase with the **public `anon` key** and **no per-user identity** (`auth.uid()` is always null). ~22 `public.*` tables on the EQ tenant are anon `SELECT/INSERT/UPDATE/DELETE` via `USING(true)` — **including `app_config`, which holds plaintext staff/manager PIN codes.** Closing this:
> 1. removes a **live auth-bypass + data-tamper exposure** (on the legacy `public.*` tables), and
> 2. is the **prerequisite to roll EQ Field onto the SKS tenant and cut SKS live**.
>
> **Correction (2026-06-03, measured):** an earlier draft said the EQ tenant *lacks* the `tenant_isolation` RLS. That was a guard artifact, not reality — the guard exact-matched policy *decomposition*. Measured: **the canonical `app_data` spine is already RLS-on + tenant-gated on BOTH tenants** (zaap and ehow). The real anon exposure is on the **legacy `public.*`** tables (e.g. `app_config` — T1 below), which the in-progress remediation migrates onto the already-isolated `app_data`. The guard was upgraded to a **semantic `effective_rls`** comparison (eq-shell #157): real spine drift is now **18 items = 5 columns** (`briefing/gm tenant_id` text↔uuid + 2 nullability), not 165. Closing those 5 columns takes `--strict-spine` to green.
>
> Fix it once, unlock all three. **The RLS that secures Field is the same policy shape that aligns the spine.**

---

## Current status — 2026-06-04

**Governance half (the canonical spine) — DONE + ENFORCED.**
- One Pipe (gated runner + ledger reconciler), scope-aware **semantic** drift guard, EOL determinism — shipped (eq-shell #156, #157).
- `0034` (fold migration 048 ON-DELETE) + `0035` (reconcile the final 5 spine columns: `briefing/gm tenant_id` text→uuid, `contacts.customer_id` → nullable, `licences.licence_number` → NOT NULL) — **applied to BOTH tenants** via the gated pipe, canary `core` → `sks`, 2026-06-04. (Canary caught a policy-dependency bug in `0035` on `core`; fixed in #161 before SKS was touched.)
- `check-tenant-drift --strict-spine` → **GREEN** (spine identical across tenants) and now **enforced in CI** (#162) — spine drift fails the drift check.
- **Open toggle (Royce):** `main` is unprotected; making "Schema drift + anon-grant invariant" a *Required* check (Settings → Branches) turns the red check into a hard merge-block. Optional — it puts a live-DB check in the merge path.

**Security half (Field `anon` → `authenticated`) — IN PROGRESS, owned by a concurrent session** (`focused-brattain`, eq-field `main`): Field now mints a tenant-scoped `authenticated` Supabase JWT; `app_data.staff` granted to `authenticated` (anon denied) behind tenant-isolation RLS; "Phase 2 repeats per surface." Stream 0 audit fixes (supervisor fail-open, hardcoded codes) already on `main`; PR #175 closed as redundant. **Do not duplicate this surface.**

**Still live (not yet closed):** **T1** — `zaap.public.app_config` is anon-readable and holds the staff/manager codes (Field validates them client-side via the anon key). Closing it = the server-side-validation work below (Stream 0.2 / Stream 1), in the concurrent session's lane. The codes are also in git history → **rotate them** regardless of the access fix.

**Key correction (don't relitigate):** the canonical `app_data` spine was *already* RLS-on + tenant-gated on both tenants — the earlier "165 RLS gaps" were a guard artifact (exact-matching policy decomposition), fixed by the semantic `effective_rls` comparison. The real anon exposure is the **legacy `public.*`** tables only.

---

## Threat model — what an attacker holding the shipped anon key can do TODAY

The anon key is embedded in the browser bundle (necessarily — it's the client credential). With it, an unauthenticated attacker can hit the Supabase REST API directly and:

| # | Attack | Mechanism | Impact |
|---|--------|-----------|--------|
| T1 | **Harvest plaintext PINs → impersonate any user** | `GET public.app_config` (anon SELECT, `USING(true)`) returns staff/manager codes | **Auth bypass** — full account takeover of any role on any org |
| T2 | **Tamper/destroy config** | anon `INSERT/UPDATE/DELETE/TRUNCATE` on `app_config` | Lock users out, alter branding/entitlements, denial of service |
| T3 | **Read all operational data across orgs** | anon SELECT `USING(true)` on `people`, `timesheets`, `rosters`, `feedback_entries`, `apprentice_journal`, etc. | **Cross-tenant data leak** (PII: names, hours, reviews) |
| T4 | **Write/delete operational rows** | anon write grants on the above | Falsify timesheets, delete people/sites, corrupt records |
| T5 | **Blast-radius growth** | shared Supabase project, tenant-agnostic anon key | Every new org added to a shared project widens T3/T4 |

**T1 is the active critical**: a secret (PIN) is readable by the role every visitor holds. Severity: **HIGH/CRITICAL**, exploitable now.

_Live evidence (read-only, 2026-06-03, zaap/eq-canonical-internal): `public.app_config` → anon `{SELECT,INSERT,UPDATE,DELETE,TRUNCATE}`, `open_policies=1` (`USING(true)`). 22 `public.*` tables anon-reachable; 25 tracked in the guard's `KNOWN_LEGACY_ANON` burn-down._

---

## Definition of Done (end state)

- [ ] Every Field→Supabase request carries a **per-user Supabase JWT** (Shell-minted or PIN-session-minted) — `auth.jwt()` non-null with `tenant_id` + `role`.
- [ ] RLS on all data tables is **identity/tenant-scoped** — zero `USING(true)` on data tables.
- [ ] Secrets (`people.pin`, codes) are **never client-reachable** — service-role functions only; client sees a `has_pin` boolean.
- [ ] `anon` has **zero grants** on data tables — `KNOWN_LEGACY_ANON` burned to **0**.
- [ ] Field runs on **canonical `app_data`** on the tenant DBs; legacy `public.*` retired.
- [ ] `check-tenant-drift --strict-spine` → **exit 0**, wired as a **required blocking** CI gate; declarative snapshot v1.0 committed.
- [ ] **SKS tenant provisioned with secured Field** via the One Pipe; **SKS cut live** on per-user auth.

---

## Guiding principles (non-negotiable)

1. **Working before refactoring.** Field stays up the entire way. No big-bang. Each surface cuts over behind a flag.
2. **Defense in depth.** Identity **and** RLS **and** server-side sensitive reads **and** least-privilege grants — not any one alone.
3. **The guard is the proof.** Nothing is "done" until the anon-grant invariant + `--strict-spine` say so. No vibes.
4. **One Pipe only.** All schema/RLS lands via the gated `migrate-tenants` runner — never hand-applied single-tenant SQL.
5. **Reversible increments.** Every grant/RLS change has a tested rollback (re-grant + restore policy). Canary one tenant before the fleet.
6. **Auth deploys need explicit approval.** Per global rule — no auth change deploys without Royce's go-ahead.

---

## Streams

### Stream 0 — Stop the bleeding (ship first; no architecture change required)
*Goal: kill the critical (T1/T2) and land the already-coded quick-wins, before the larger rebuild.*

| ID | Task | Acceptance |
|----|------|-----------|
| S0.1 | Review + merge the existing audit branch `claude/security-audit-2026-05-31` (#3 timing-safe HMAC compares, #5 host-scoped `?tenant=` allowlist — both coded, unmerged) | Branch merged; CI green |
| S0.2 | **Plaintext PINs out of client reach.** Stop fetching PIN codes to the browser; verify PINs only in `verify-pin.js` (server); apply `2026-05-31_staff_pin_verify.sql` | No PIN value in any client payload/bundle (grep gate); gate + staff-TS login still work via server path |
| S0.3 | **Revoke anon WRITE on `app_config`** (INSERT/UPDATE/DELETE/TRUNCATE) immediately; reads move behind a service-role boot function | anon-grant check: `app_config` not anon-writable; Field still boots and reads config via the function |

**Gate:** anon-grant invariant shows `app_config` no longer anon-writable and PINs not client-reachable. **T1/T2 closed.**

---

### Stream 1 — Identity foundation (the linchpin; half-built already)
*Goal: every Field session carries a Supabase JWT so `auth.jwt()` exists. This is the prerequisite for all real RLS.*

| ID | Task | Acceptance |
|----|------|-----------|
| S1.1 | Field obtains the **Shell-minted `aud=field` Supabase JWT** on session start (Shell handoff path already exists; `eq-shell/netlify/functions/token-exchange.ts` already mints it, signed with `SUPABASE_JWT_SECRET`) and uses it as the Supabase bearer | Shell-originated sessions send the user JWT to Supabase |
| S1.2 | `scripts/supabase.js`: send the **user JWT** (not the bare anon key) on authenticated requests; silent refresh before expiry | All `sbFetch` data calls carry the JWT |
| S1.3 | **PIN-only (non-Shell) sessions** also get identity: `verify-pin.js` mints an equivalent scoped Supabase JWT (signed `SUPABASE_JWT_SECRET`, carrying `tenant_id`+`role`) so *every* Field session — Shell or PIN — has `auth.jwt()` | Both login paths produce a JWT with `tenant_id`/`role` |
| S1.4 | TTL/refresh: the `aud=field` token is 60s today (iframe window). Lengthen for standalone Field sessions or add silent refresh so long sessions don't drop mid-use | No mid-session auth expiry in a normal shift |

**Gate:** `auth.jwt()` non-null server-side on every Field request; `tenant_id`/`role` present.

---

### Stream 2 — Identity-scoped RLS (the convergence with schema governance)
*Goal: rewrite `USING(true)` → tenant/role-scoped. This is the SAME `tenant_isolation` policy SKS already carries and the EQ tenant lacks → closes 165/175 spine diffs.*

| ID | Task | Acceptance |
|----|------|-----------|
| S2.1 | Author **canonical RLS migrations** (One Pipe): `tenant_isolation` `USING (tenant_id = ((auth.jwt()->'app_metadata'->>'tenant_id')::uuid))` on every spine data table — matching SKS's existing policy set | `--strict-spine` spine-policy diffs → 0 |
| S2.2 | **Role-scoped** policies where the model needs them (e.g. manager-vs-nominee draft-tender visibility — the gap noted in SKS-CUTOVER item #3) | Manager sees drafts; nominee doesn't, enforced in-DB |
| S2.3 | Apply via the **gated One Pipe**, **canary one tenant first** (a demo tenant), then fleet | Field reads/writes only its own tenant's data; negative test (wrong-tenant JWT) denied |

**Gate:** `--strict-spine` policy diffs eliminated; cross-tenant read provably denied.

---

### Stream 3 — Sensitive data goes server-side (least exposure)
*Goal: secrets never transit the client at all.*

| ID | Task | Acceptance |
|----|------|-----------|
| S3.1 | Revoke anon/authenticated **SELECT on `people.pin`** (+ any secret columns); expose verification via a service-role RPC/function with explicit checks (finding #2 Phase 2) | `anon`/`authenticated` cannot SELECT `pin`; gate + timesheet flows work via server path |
| S3.2 | Client reads a **`has_pin` boolean projection**, never the value | No PIN value reaches the client |

**Gate:** no secret column is client-selectable; flows still work.

---

### Stream 4 — Retire anon (least privilege)
*Goal: the `anon` role ends with zero grants on data tables. Tracked by the guard's burn-down list.*

| ID | Task | Acceptance |
|----|------|-----------|
| S4.1 | **Table-by-table**: as each surface is confirmed working on the user JWT, **revoke anon grants** on that table; update `KNOWN_LEGACY_ANON` (25 → … → 0) | Burn-down decreases each cutover; no Field regression |
| S4.2 | Drop the now-dead `USING(true)` policies once anon is revoked | No `USING(true)` left on data tables |

**Gate:** anon-grant invariant **clean with an empty `KNOWN_LEGACY_ANON`** on all canonical projects.

---

### Stream 5 — Canonical Field schema + spine column reconcile
*Goal: bring the secured Field schema into the canonical lineage and finish the spine.*

| ID | Task | Acceptance |
|----|------|-----------|
| S5.1 | Resolve Field's **own half-migration**: un-prefixed ↔ `field_*` with live data on both (verified 2026-06-03: `tenders`=10/`field_tenders`=323; `timesheets`=75/`field_timesheets`=0). Pick canonical shape per table, migrate data, retire dupes | One table family per domain; row counts reconciled; no data loss |
| S5.2 | Capture the secured `field_*` schema as **canonical One-Pipe migrations** (so fresh tenants + SKS get it uniformly) | `field` module schema authored in `supabase/tenant-migrations/` |
| S5.3 | Reconcile the **5 spine column diffs**: `briefing_actions/briefing_cache/gm_report_periods.tenant_id` (`text`→`uuid`), `contacts.customer_id` + `licences.licence_number` nullability — forward-migrate to the canonical choice | `--strict-spine` column diffs → 0 |

**Gate:** `--strict-spine` fully clean across all tenants.

---

### Stream 6 — Enforce + cut over (the payoff)
*Goal: lock the spine as a blocking gate and bring SKS live on secured Field.*

| ID | Task | Acceptance |
|----|------|-----------|
| S6.1 | Flip `check-tenant-drift --strict-spine` to a **required blocking** CI check; commit declarative **canonical snapshot v1.0** | Spine drift can no longer merge |
| S6.2 | **Provision the SKS tenant** with the secured Field schema via the gated One Pipe; validate | SKS tenant carries `field_*` + identity RLS; smoke passes |
| S6.3 | **SKS cutover**: Field live on the SKS tenant on per-user auth; decommission the legacy SKS NSW Labour anon path | SKS users on secured EQ Field; legacy retired |

**Gate:** SKS live on secured Field; spine blocking-enforced; anon retired.

---

## Verification gates (the sprint is not done until ALL are green)

- **anon-grant invariant:** 0 violations, `KNOWN_LEGACY_ANON` empty, on all three canonical projects.
- **`check-tenant-drift --strict-spine`:** exit 0 (spine identical), wired as required.
- **Negative tests:** wrong-tenant JWT → denied; expired JWT → denied; bare anon key → denied on data tables; secret columns → not selectable.
- **Field smoke (per tenant):** boot → PIN **and** Shell login → read+write own data → leave email → agent chat.
- **Secret scan:** no plaintext code/PIN/secret in any client bundle or network payload (CI grep gate).

---

## Sequencing & canary safety

```
S0 (stop bleeding) ─▶ S1 (identity) ─▶ S2 (RLS) ─▶ S3 (server-side secrets) ─▶ S4 (retire anon) ─▶ S5 (canonicalise) ─▶ S6 (enforce + SKS live)
        │ ship now            │ linchpin        │ convergence w/ spine
        └─ T1/T2 closed       └─ auth.jwt()     └─ closes 165/175 spine diffs
```

- **Canary order for every fleet apply:** a **demo tenant → `core` (EQ internal) → SKS last.** SKS is the customer; it goes last, after the model is proven twice.
- **Rollback per step:** RLS/grant changes are reversible (re-grant + restore policy); applied via the gated One Pipe with `--slug` for a single-tenant canary.
- **Auth deploys:** explicit Royce approval before each (global rule).

---

## Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| 60s `aud=field` JWT TTL vs long Field shifts → mid-session expiry | Silent refresh (S1.4) + a fit-for-purpose standalone-Field TTL |
| ~27K LOC client; every `sbFetch` must carry the JWT | Phase per module behind a flag; the anon key keeps working until each surface flips |
| Half-migrated Field data (S5.1) — migration risk | Snapshot + row-count validation per table; One-Pipe gated apply, canary first |
| Realtime tables (`roster_presence`, `checkins`) under new RLS | Verify realtime subscriptions honour identity RLS in the canary |
| Breaking login during the auth rebuild | Keep PIN path working throughout; Stream 0/1 are additive, not replacing, until S4 |

---

## Already in place (foundations this sprint stands on)

- ✅ **Shell mints `aud=field` Supabase JWTs** (`eq-shell/netlify/functions/token-exchange.ts`) — Stream 1 linchpin is half-built.
- ✅ **`SUPABASE_JWT_SECRET` set on Netlify** (Sprint 5, 2026-06-03) — Field functions can verify/mint identity JWTs.
- ✅ **One Pipe + gated apply + ledger reconciler + scope-aware guard** (eq-shell #156 merged, #157 open) — the delivery rails **and** the verification gates this sprint is measured by.
- ✅ **Security audit quick-wins coded** (`eq-solves-field@claude/security-audit-2026-05-31`) — Stream 0.1 is review-and-merge.
- ✅ **Threat surface mapped** (this doc) + live exposure quantified.

---

## Reference

- EQ Field security audit: `eq-solves-field/SECURITY-REMEDIATION-HANDOFF.md` (findings #1–#6), `SKS-CUTOVER-STATUS.md` (item #3 per-user auth decision).
- Schema governance: `eq-shell/SCHEMA-GOVERNANCE.md` (spine model, `--strict-spine`, the 175-diff worklist).
- Guard burn-down: `eq-shell/scripts/check-tenant-drift.mjs` → `KNOWN_LEGACY_ANON` (25 tables) + `--strict-spine`.
- Field data plane: browser → `ktmjmdzqrogauaevbktn` (EQ) / `nspbmirochztcjijmcrx` (SKS); routing via canonical `jvknxcmbtrfnxfrwfimn`. Canonical tenant data planes: `zaapmfdkgedqupfjtchl` (EQ), `ehowgjardagevnrluult` (SKS).
- This sprint's north star (Royce, 2026-06-03): perfect EQ Field → secure it → roll to SKS tenant → cut SKS live.

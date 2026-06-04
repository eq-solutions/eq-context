# Weekend Merge Runbook — Consolidate + Deploy (#2) + EQ Anon Remediation (#3)

**Prepared:** 2026-06-04 · **For:** the weekend merge window
**Scope:** #2 (consolidate + deploy in-flight work) and #3 (finish the EQ-tenant anon→authenticated remediation + close T1).
**OUT of scope this weekend:** #1 SKS go-live (Field on the SKS tenant) — **not ready**, has large prerequisites. See `SKS-CUTOVER-CRITICAL-PATH.md`. Do not attempt #1 in a weekend window.

> Low-traffic weekend = good deploy window. The goal is **execution, not improvisation** — every step below has a gate, a smoke test, and a rollback. Stop at the first red gate.

---

## ⚠️ Must-verify BEFORE any deploy (preflight findings, 2026-06-04)

| # | Finding | Action before deploy |
|---|---------|----------------------|
| P1 | **`SUPABASE_JWT_SECRET` is NOT present on eq-field / eq-service.** The account-level var exists but is **not inherited** by these sites (Netlify account vars aren't auto-inherited). They carry `ZAAP_JWT_SECRET` + `DATA_JWT_ENABLED` (the remediation's new per-tenant secret). | **Confirm with the current auth code / the remediation owner (`focused-brattain`)** whether Field/Service still need `SUPABASE_JWT_SECRET` (Phase-3 iframe JWT from Shell) or have moved to `ZAAP_JWT_SECRET`. If still needed → set it as a **site-level** var on each (account-level won't reach them). **Do not blindly set it** — it may have been intentionally retired. |
| P2 | **eq-field PR #156 is CONFLICTING** with main. | Rebase/resolve before merge, or drop from this weekend. |
| P3 | eq-context PRs #7/#8 show **failing CI**. | Other agents' docs PRs — not blockers; leave to their owners. |
| P4 | All 3 sites are **manual-deploy** (`auto_publish` off). | Deploys are explicit — a merge alone does NOT deploy. Trigger each deploy deliberately. |

`EQ_SECRET_SALT` confirmed present on all three sites. All three currently `ready`.

---

## Merge candidates (verify CI green at merge time)

| Repo | PR | What | State (2026-06-04) |
|------|----|------|--------------------|
| eq-solves-service | #232 | host-based SameSite for Shell SSO cookies (kills double-login) | checks green; mergeable computing — **good candidate** |
| eq-field | #156 | shift.started canonical event scheduler | **CONFLICTING — rebase first** |
| eq-context | #7, #8 | docs (worker-creds, Direction D) | failing CI — other agents', skip |

*(eq-shell has no open PRs — the spine governance work all landed and is CI-enforced.)*

---

## Pre-merge gate (go / no-go)

- [ ] Each candidate PR: **CI green** + **mergeable** (no CONFLICT) at merge time.
- [ ] eq-shell spine gate: any spine-touching PR passes `--strict-spine` (now a required check).
- [ ] P1 resolved (JWT secret question answered).
- [ ] You have the rollback for each item (below) open in a tab.

If any box is unchecked → **no-go for that item.** Partial is fine; ship what's green.

---

## Merge + deploy order

Do these **one at a time**, verifying each before the next.

1. **eq-solves-service #232** (SSO cookie fix) → merge to main → **deploy eq-service** (manual) → smoke: log in via Shell, confirm **no double-login**, confirm a Service page loads in the iframe.
2. **eq-field #156** (only if rebased + green) → merge → **deploy eq-field** → smoke: boot Field, PIN/Shell login, the shift.started scheduler fires.
3. **#3 EQ anon remediation** (if the concurrent agent lands the burn-down): merge their PR(s) → deploy eq-field → smoke: Field reads/writes its own tenant data on the **authenticated** path (not anon); a bare anon key is denied on a remediated table.

Between each: check the site's Netlify deploy went `ready` (not `error` — we hit a pnpm install failure on eq-service earlier; if a deploy errors, see Rollback).

---

## Smoke tests (run after each deploy)

- **Shell auth (Phase 3):** magic-link login → iframe handoff → Field + Service accept the JWT. Script: `eq-shell/scripts/smoke-test-phase3.mjs` (needs the jvkn service_role key as `SVC_KEY`).
- **Service SSO:** single login (no double), Service iframe renders.
- **Field:** boot + login (PIN and Shell) + read/write own data + leave email + agent chat.
- **Anon denial (after #3):** a remediated `app_data` table returns `insufficient_privilege` to a bare anon key.

---

## Rollback (per step)

- **Bad deploy:** Netlify → the site → Deploys → **Publish** the previous `ready` deploy (instant revert). Sites are manual-publish, so the old deploy is still live until you publish the new one — low risk.
- **Bad merge (code):** `git revert <merge-sha>` on main → redeploy.
- **DB / RLS (only if #3 touches schema):** all tenant DB changes go through the gated One Pipe and are transactional per tenant. To revert a grant/policy: re-run the inverse via a new migration (never hand-SQL). The runner halts on failure, so nothing half-applies.
- **Secrets:** if you set `SUPABASE_JWT_SECRET` site-level (P1) and it breaks something, delete the site-level var to fall back.

---

## #3 tail — T1 (do regardless of the merge)

`zaap.public.app_config` is anon-readable and holds the staff/manager codes (Field validates them client-side via anon). Two actions, independent of any deploy:
1. **Rotate the codes** — they're compromised (anon-readable + in git history). New values in `app_config`. **Your action.**
2. Closing the *access* (revoking anon read on `app_config`) needs the server-side code-validation move — that's in the remediation's lane, not a config flip (Field would break login without it).

---

## Definition of "weekend done"

- [ ] eq-service SSO fix shipped + smoke-passed.
- [ ] eq-field #156 shipped (if rebased) or cleanly deferred.
- [ ] EQ anon burn-down advanced/closed (concurrent agent) + smoke-passed.
- [ ] Codes rotated.
- [ ] No site in `error`; all smoke tests green.
- [ ] #1 (SKS) explicitly **not** attempted — scheduled as its own project.

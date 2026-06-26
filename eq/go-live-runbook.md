---
title: EQ Core — Weekend Go-Live Runbook
owner: Royce Milmlow
last_updated: 2026-06-05
scope: Taking EQ Core (core.eq.solutions = eq-shell, iframing Field/Service/Cards/Quotes) live. Grounded in live-system checks 2026-06-05.
read_priority: critical
status: live
---

# EQ Core — Weekend Go-Live Runbook

**Host topology:** `core.eq.solutions` = **eq-shell** (Netlify). It embeds Field, Service,
Cards, Quotes and SKS-Labour as iframes, authed via a `Domain=.eq.solutions` shell cookie
(cookie mode) or a 60s minted HMAC token (legacy/token mode). Source of truth for the iframe
allow-list is Shell's CSP `frame-src` in `eq-shell/netlify.toml`.

> Provenance: §A verified against live systems on 2026-06-05 (PostHog EU `162632`,
> canonical Supabase `jvknxcmbtrfnxfrwfimn`, repo configs). Items marked ❓ could not be
> verified from the dev box (Netlify MCP offline) — confirm before flipping.

## A. ✅ Verified green (checked 2026-06-05)

- ✅ **Canonical DB healthy & populated** — `jvknxcmbtrfnxfrwfimn`: workers 38,
  worker_credentials 779, worker_invites 37, tenants 4, organisations 4, licences 5.
  Every table RLS-enabled.
- ✅ **Canonical security** — 0 ERROR advisors; no RLS-disabled tables, no exposed
  `auth.users`, no security-definer views.
- ✅ **Logout hygiene** — `posthog.reset()` present in all 3 apps (Shell
  `observability.ts:207`, Field `auth.js:246`, Service `analytics.ts:51`).
- ✅ **Auth handoff flow** — code-confirmed: Shell mints HMAC token → `shell-bridge`
  → `verifyOtp` → Supabase session.
- ✅ **Service iframe cookie SSO — engineered.** `lib/auth/shell-cookies.ts` host-gates
  the cookie policy (`.eq.solutions` → `SameSite=Lax`; `netlify.app` → `SameSite=None`).
  Inert until the domain flips, so already safe to ship. See cutover runbook in
  eq-solves-service: `docs/runbooks/shell-service-domain-cutover.md`.
- ✅ **CSP both sides** — Shell `frame-src` allows `service.eq.solutions`; Service
  `_headers` `frame-ancestors` allows `*.eq.solutions`.
- ✅ **Real usage & retention** (PostHog) — ~19 sticky users, flat retention tail,
  cross-app handoff exercised 155× in 30 days. Demand is real.

## B. 🔴/🟠 Open gates — close BEFORE the flip

### B-1. 🔴 Complete the Service domain cutover (kills the double-login)
The iframe SSO only works when Service is served from **`service.eq.solutions`** (same-site).
On `eq-solves-service.netlify.app` it is cross-site and Safari/Chrome block the cookie →
user bounced to a second login. Follow `shell-service-domain-cutover.md`. Status of its
pre-flight checklist as of 2026-06-04:

- ❓ **`EQ_SECRET_SALT` parity (Shell vs Service) — THE #1 GO/NO-GO.** Must be byte-identical.
  If it differs, cookie verify returns null, fast-path falls through, and the double-login
  *persists looking exactly like the fix failed*. Service side confirmed present; **Shell-side
  comparison never done.** Verify first.
- ✅ `service.eq.solutions` custom domain on Service (confirmed 06-04).
- ❓ DNS/TLS live — `curl -I https://service.eq.solutions` returns 200/3xx with valid cert
  (run from a real network).
- ❓ `NEXT_PUBLIC_SITE_URL` on Service → `https://service.eq.solutions` (was netlify.app).
- ❓ Supabase Auth URL allowlist (project `ehowgjardagevnrluult`, sks-canonical —
  Service's DB since the 2026-06-08 migration; old `urjhmkhbgaxrofurpbgc` deleted
  2026-06-22) includes `https://service.eq.solutions`, or the OTP exchange is rejected.
- Then: set `VITE_SERVICE_URL=https://service.eq.solutions` in **Shell** Netlify env + redeploy.

### B-2. ✅ Anon SECURITY DEFINER RPCs — AUDITED 2026-06-05, essentially clear
Pulled all four live definitions from canonical and traced the true-anon (`auth.uid()`=NULL)
path. **Not a launch blocker.** Three are correctly self-authorising; one optional hardening:
- ✅ `eq_cards_delete_account()` — every write is `WHERE id/user_id = auth.uid()`; anon →
  matches zero rows (no-op). Can only ever soft-delete the caller's own account. Safe.
- ✅ `eq_cards_get_worker_hr_record()` — `WHERE user_id = auth.uid()`; anon returns nothing.
  Only ever returns your own record. Safe.
- ✅ `eq_cards_preview_invite(uuid)` — token-gated preview, non-sensitive fields (org/worker
  name, count, expiry). Intentional and safe.
- 🟠 `eq_cards_claim_invite(uuid)` — token-gated but does **not** reject `auth.uid() IS NULL`.
  A true-anon caller knowing a valid unclaimed token could burn the invite (set `claimed_at`)
  and create an orphaned `workers` row (`user_id=NULL`). Low/medium (needs a secret token).
  **Optional hardening (pre- or post-launch):** add at the top of the function —
  `IF auth.uid() IS NULL THEN RAISE EXCEPTION 'auth_required' USING ERRCODE = '28000'; END IF;`

### B-3. 🟠 MFA posture — make a conscious call
Cookie mode sets `eq_shell_bridge`, which makes Service **skip its TOTP** and trust Shell.
Shell's primary factor is a **PIN** (TOTP optional, no `aal` claim) → a PIN-only user reaches
the Service CMMS **single-factor**. Either knowingly accept this for launch (documented as a
convenience), or gate Service behind mandatory Shell-TOTP for the relevant roles. Long-term:
add an `aal`/`mfa_satisfied` claim to `eq_shell_session` and bypass per-app MFA only when
asserted (see cutover runbook §MFA).

### B-4. ✅ Naming flag — RESOLVED (Service migrated off the dev-named project)
This asked whether Service prod was wrongly pointed at the `eq-solves-service-*dev*`
project (`urjhmkhbgaxrofurpbgc`). Resolved: Service migrated to `ehowgjardagevnrluult`
(sks-canonical, `service.*` schema) on 2026-06-08, and the old project was deleted
2026-06-22. Service prod auth now targets ehow — confirm its allowlist (gate B-1 above).

### B-5. 🟠 Branch hygiene — confirm what ships
As of 2026-06-05: eq-shell on `claude/b4-validate` (dirty), eq-solves-field on
`revert/licence-admin`. Whatever deploys must come from the intended release branch, not
these in-flight ones.

## C. Cutover / deploy sequence (each step reversible; each deploy = explicit approval)

1. Close every 🔴/🟠 in §B; merge release branches; CI + `check:perms` green.
2. **Deploy Service** (inert on netlify.app; readies the new host).
3. Stand up `service.eq.solutions` end-to-end (domain + cert + salt + `NEXT_PUBLIC_SITE_URL`
   + Supabase URL allowlist).
4. **Verify in isolation** — point a Shell *preview's* `VITE_SERVICE_URL` at the new host,
   sign in, confirm **zero** second-login in **both Safari and Chrome**.
5. **Flip Shell prod** — set `VITE_SERVICE_URL=https://service.eq.solutions`, redeploy Shell.
6. Run §D smoke tests **before** announcing.
7. Soak a few days, then retire Service's dead token paths.

## D. Post-deploy smoke tests (the real user path)

- [ ] Sign in at `core.eq.solutions` → lands on `/{tenant}` dashboard
- [ ] **Field iframe** loads *and is logged in*
- [ ] **Service iframe** loads *and is logged in* ← the B-1 risk; test Safari + Chrome
- [ ] Cards + Quotes iframes load
- [ ] Log out → session cleared in all panes
- [ ] Second user / second tenant → no cross-tenant data bleed

## E. Rollback

- **Service cutover:** unset / revert `VITE_SERVICE_URL` on Shell → instantly back to
  netlify.app token-mode. Nothing one-way until the dead-path cleanup.
- **Shell / Field:** Netlify instant rollback to the prior deploy, per site, independently.
- **DB:** no destructive migration in this release → no DB rollback needed. Pin the prior
  Shell deploy for 48h.

## F. Watch (first 48h)

- **PostHog** — real-user count, auth funnel (signin → handoff → dashboard), `error_thrown`.
- **Sentry** — `eq-shell` / `eq-service` issue spikes.
- **Known-noise baseline** — the "refused to merge an already identified user" warning is
  *expected* (deferred cross-app distinct_id fix — see spawned task). Don't chase it during
  launch. Field's pageviews all logging as `/` is also expected (deferred SPA-capture fix).

## Deferred (post-launch, already spun off as tasks)

- Unify cross-app PostHog distinct_id (Shell UUID vs Field `tenant:handle` vs Service id).
- Fix EQ Field double `$pageview` capture (SPA logs ~80% of pageviews as `/`).

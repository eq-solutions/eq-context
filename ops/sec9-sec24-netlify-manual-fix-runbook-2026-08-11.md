---
title: SEC-9 dev-context clear + SEC-24 re-store — manual Netlify runbook
owner: Royce Milmlow
last_updated: 2026-08-11
scope: Literal step-by-step checklist for the two open Netlify env-var findings that need a human's hands — Claude Code's safety classifier blocks writing security settings regardless of explicit permission, same as SEC-12/18/19's precedent.
read_priority: normal
status: live
---

# SEC-9 dev-context clear + SEC-24 re-store — manual runbook

Two different problems, two different fixes. Neither is a rotation — both are
same-value corrections. ~15 minutes total across 3 Netlify projects.
Full finding detail: [security-register.md](security-register.md) SEC-9 / SEC-24.

---

## Part A — SEC-24: `QUOTES_CRON_SECRET` (eq-shell only)

**Problem:** stored `is_secret: false` — plaintext in all 4 deploy contexts.
**Fix pattern:** same as SEC-12/18/19 — note the value, delete, recreate
identical, tick "contains sensitive values" this time.

1. Netlify dashboard → **eq-shell** project → Site settings → Environment variables
2. Find `QUOTES_CRON_SECRET`
3. Click to reveal/copy the current value (all contexts should be identical)
4. Delete the var
5. Recreate it with the exact same value, all contexts, and tick **"Contains
   secret values"** (this is what sets `is_secret: true`)
6. Confirm: reopening the var should now show it masked

☐ Done

---

## Part B — SEC-9: clear the `dev`-context value on 17 vars

**Problem:** these vars are already correctly `is_secret: true` — the bug is
platform-level: Netlify never masks the `dev` context regardless of that
flag, so the raw value is readable via any `dev`-context API/CLI read.
**Fix pattern:** different from Part A — do NOT delete-and-recreate the
whole var (that resets all 4 contexts and risks a typo breaking prod). Just
**clear the one `dev`-context value**, leaving branch-deploy/deploy-preview/
production untouched. Vars that already have an empty `dev` value (e.g.
`FIELD_SUPABASE_SERVICE_ROLE_KEY`, `EQ_SERVICE_API_KEY`) don't leak — that's
the target end-state for all 17 below.

**For each var:** Site settings → Environment variables → click the var →
find the `dev` context row → clear its value (leave other contexts as-is) → Save.

### eq-shell (11 vars)
☐ `EQ_SERVICE_HANDOFF_KEY`
☐ `EQ_SHELL_BRIDGE_SECRET`
☐ `SKS_SUPABASE_JWT_SECRET`
☐ `SUPABASE_JWT_SECRET`
☐ `EQ_QUOTES_HANDOFF_KEY`
☐ `CANONICAL_API_KEY_SERVICE`
☐ `SUPABASE_SERVICE_ROLE_KEY` — this is the jvkn/eq-canonical key, same one
  SEC-9's main finding is about (pasted into a chat 2026-07-12). Clearing
  `dev` here doesn't close that original exposure — rotation runbook
  (`sec9-jvkn-key-rotation-runbook-2026-07-27.md`) is the real fix for that
  part, whenever you pick a window. This checkbox just stops the ongoing leak.
☐ `EQ_PLATFORM_ADMIN_KEY`
☐ `CANONICAL_API_KEY_FIELD`
☐ `EQ_SESSION_SALT`
☐ `EQ_SHELL_JWT_SECRET`

### eq-field (1 var)
☐ `SKS_JWT_SECRET`

### eq-service (5 vars)
☐ `SUPABASE_SERVICE_ROLE_KEY` — points at the already-deleted `urjh` project.
  Dead-key hygiene, not a live risk, but clear it anyway for consistency.
☐ `EQ_PLATFORM_ADMIN_KEY`
☐ `EQ_SECRET_SALT`
☐ `EQ_SHELL_JWT_SECRET`
☐ `CANONICAL_API_KEY_SERVICE`

---

## After both parts

- Re-run a `getAllEnvVars` check on all 3 sites (or ask Claude Code to, next
  session) to confirm: `QUOTES_CRON_SECRET` now masks in all contexts, and
  the 17 vars above return empty/masked `dev` values instead of plaintext.
- Update `security-register.md`: SEC-24 → closed; SEC-9's `dev`-context
  addendum → closed (the underlying jvkn key exposure itself stays open
  until you separately run the rotation runbook).
- eq-cards was not swept for this same `dev`-context pattern — worth a
  one-off check next time you're in that project's Netlify settings, since
  it wasn't re-verified after SEC-18 closed there.

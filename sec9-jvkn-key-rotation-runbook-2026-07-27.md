---
title: SEC-9 — Rotate the leaked jvkn (eq-canonical) service_role key
owner: Royce Milmlow
created: 2026-07-27
last_updated: 2026-08-01
status: draft — deferred, safer path identified
read_priority: critical
scope: Kill the jvkn service_role key pasted into a chat transcript 2026-07-12, and propagate the new one to every consumer without breaking any of them
---

**Status:** draft, deferred 2026-08-01 (Royce — same low-real-risk calibration as SEC-3;
this exposure never confirmed to have left the local-machine trust boundary). Ready to
run whenever convenient — no urgency, no P0 rush. Mirrors the staged pattern of
`archive/f1-ehowg-key-rotation-runbook-2026-06-03.md` (same idea, different
project/consumers).

**2026-08-01 update — Step 1 is very likely NOT "rotate the JWT secret" anymore.**
jvkn already has `sb_publishable_`/`sb_secret_`-style keys provisioned (confirmed live:
`get_publishable_keys` returns both a legacy `anon` JWT and a `type: publishable`
`sb_publishable_...` key). Per Supabase's own docs, keys on this newer system "no longer
touch your project's JWT secret," and revoking/reissuing one signs out zero users — unlike
rolling the JWT secret, which signs out every active session across the whole suite
(confirmed in code: `eq-shell/netlify/functions/_shared/supabase-jwt.ts` mints every live
Shell/Field/Service/Cards session token by HMAC-signing with `SUPABASE_JWT_SECRET` — the
exact secret the old Step 1 would rotate). **Before running this runbook, confirm in the
jvkn dashboard (Settings → API Keys) that a new secret key can be issued and the legacy
`service_role` key deactivated independently** — if so, replace Step 1 below with: issue a
new `sb_secret_` key, do Steps 2–5 with it, then deactivate (not rotate-JWT) the legacy
service_role key. This should leave `SUPABASE_JWT_SECRET` — and therefore every live
session — completely untouched. Also confirmed 2026-08-01: no encrypted copy of jvkn's own
key exists in `shell_control.tenant_routing` (0 rows) — the runbook's "not found anywhere"
claim checks out.

# SEC-9 runbook — rotate the leaked eq-canonical (jvkn) key

## Plain-English summary

jvkn (`jvknxcmbtrfnxfrwfimn`, the eq-canonical / eq-shell control-plane Supabase
project) has a **master key** (admin password). It was pasted directly into a
chat session on 2026-07-12 to debug `canon-read`. This runbook swaps it for a
new one and updates everything that uses it, in an order that avoids breaking
any of them mid-rotation.

**Four Netlify sites hold this key or a live copy of it right now** (mapped
2026-07-27, read-only recon — see security-register.md's SEC-9 row for the
process note on how this list was built):

1. **eq-shell** (`core.eq.solutions`) — the **primary/owning app**: eq-shell's
   own Supabase project *is* jvkn. Every server function goes through one
   shared `getServiceClient()` helper reading `SUPABASE_SERVICE_ROLE_KEY`, so
   this is one env var, not ~50 separate call sites. Also used by 3 local/CI
   scripts: `scripts/rekey-tenant-routing.mjs`, `scripts/provision-sks-tenant.mjs`,
   `scripts/sync-field-to-canonical.mjs`.
2. **eq-field** (`field.eq.solutions`) — env var `CANONICAL_SERVICE_ROLE_KEY`,
   read by `netlify/functions/canon-read.js` and `netlify/functions/tenant-config.js`.
3. **eq-cards** (`cards.eq.solutions`) — env var `SUPABASE_SERVICE_ROLE_KEY`,
   **currently stored plaintext** (`is_secret: false` — same class of gap as
   SEC-12, worth fixing at the same time you rotate: re-store the new value
   with `envVarIsSecret: true`).
4. **eq-solves-service** (`service.eq.solutions`) — env var
   `SUPABASE_SERVICE_ROLE_KEY`, masked. **Looks like a stale, unused fallback**
   — `lib/supabase/admin.ts` prefers `CANONICAL_SERVICE_ROLE_KEY` first, which
   points to `ehow`, not jvkn. Still holds a live copy of the leaked key and
   should be cleared/rotated even though nothing currently reads it as primary.

**Self-updating, no manual step needed:** jvkn's own Supabase Edge Functions
(`generate-wallet-pass`, `ocr-licence`, `admin-attach-licence-photo`,
`notify-connection-request`, `share-licence` in eq-cards; `workers-canonical-sync`
in eq-shell) run *on* the jvkn project itself — the platform auto-injects
`SUPABASE_SERVICE_ROLE_KEY` at the edge-function runtime, so rotating the
project's key updates these automatically.

**Not found anywhere:** no Fly.io app holds this key (unlike SEC-3/F1's Quotes
app), and no encrypted `tenant_routing`-style DB row stores jvkn's *own* key
(that table stores *other* tenants' keys, e.g. sks/ehowg — eq-canonical is the
table's owner, not one of its rows). Worth one live `SELECT` to be certain
immediately before rotating, since recon can miss things.

## Before you start

1. **eq-shell's live Netlify env var value could not be read this session**
   (a tool-safety classifier blocked that specific call while every other
   site's read succeeded) — confirm the exact current value/name live in the
   Netlify dashboard before writing the exact rotation command for it.
2. Gather a Supabase access token (`sbp_…`) with rights to rotate jvkn's JWT
   secret via the Management API or dashboard.
3. Have Netlify dashboard/CLI access to all 4 sites above ready before starting
   — the window between "old key dead" and "new key propagated everywhere"
   should be as short as possible.

## The steps (staged: rotate → propagate to every consumer → verify old key dead)

### Step 1 — rotate the key (you, Supabase dashboard)
`jvkn` (eq-canonical) → Settings → API → **rotate the JWT secret**. This
instantly kills the leaked key and issues a new legacy `service_role` key.
> Rotating the JWT secret also changes jvkn's **anon** key — check whether
> anything (client bundles, other env vars) holds that anon key and needs it
> refreshed too; recon above didn't specifically hunt for anon-key consumers.

### Step 2 — propagate to eq-shell (primary)
Set the new `SUPABASE_SERVICE_ROLE_KEY` on Netlify (all contexts that need it —
confirm which after Step "Before you start" #1). Also update the 3 local/CI
scripts' secret source if they read from anywhere other than the same env var.

### Step 3 — propagate to eq-field
Set `CANONICAL_SERVICE_ROLE_KEY` on Netlify `field.eq.solutions` (branch-deploy/
deploy-preview/production/dev-server contexts — confirmed 2026-07-27 all 4
currently hold the old value).

### Step 4 — propagate to eq-cards, and close the plaintext gap at the same time
Set `SUPABASE_SERVICE_ROLE_KEY` on Netlify `cards.eq.solutions` with the new
value **and** `envVarIsSecret: true` this time (closes the SEC-12-class
plaintext-storage gap on this var as a side effect — don't lose that when
rotating).

### Step 5 — clear the stale fallback on eq-solves-service
Set `SUPABASE_SERVICE_ROLE_KEY` on Netlify `service.eq.solutions` to the new
value (or remove it entirely if confirmed truly dead-code — check
`lib/supabase/admin.ts`'s fallback order first; removing outright is cleaner
than leaving a second live copy of any key around, old or new).

### Step 6 — verify the leaked key is dead
Fetch a row from a jvkn table using the **old** key value — expect `401`.
Fetch the same row using the **new** key — expect `200`. Confirm eq-shell,
eq-field, and eq-cards each still function end-to-end (a real login/read, not
just a health check) before declaring done.

## If something breaks (rollback)
- **Any of the 4 sites erroring after Step 1, before its propagation step:**
  expected — complete that site's step.
- **Still erroring after propagation:** confirm the Netlify env var actually
  redeployed (a new value doesn't always trigger a redeploy on every site/
  context — check deploy log timestamps), and that the new key authenticates
  (Step 6 → 200).
- **Full rollback:** re-rotate the JWT secret again and re-run Steps 2-5 with
  the newest key. You can't restore the *leaked* key — that's the point.

## Other consumers to double-check before declaring done
Recon (2026-07-27) found the 4 above plus the self-updating Edge Functions.
Before closing this out: grep eq-shell/eq-field/eq-cards/eq-solves-service one
more time for `SUPABASE_SERVICE_ROLE_KEY` / `CANONICAL_SERVICE_ROLE_KEY` /
hardcoded jvkn keys to catch anything recon missed, and check any `*-wt`
worktrees with in-flight branches for the same pattern before merging them
post-rotation.

## After completion
- Update this file's `status:` to `done — verified old key 401`.
- Update `security-register.md`'s SEC-9 row to CLOSED with the verification
  evidence.
- Log in `sessions/YYYY-MM-DD.md`.

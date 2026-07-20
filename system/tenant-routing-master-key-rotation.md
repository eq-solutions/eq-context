---
title: SECURITY — TENANT_ROUTING_MASTER_KEY rotation runbook
owner: Royce Milmlow
last_updated: 2026-07-20
scope: AES-256-GCM master key for tenant service-role key encryption — prerequisites, re-encryption procedure, rollback, emergency path
read_priority: reference
status: live
---

> **Not re-reviewed since the 2026-07-16 `favour-perfect` incident** (see `suite-state.md`
> Key Decisions) — that tenant's `shell_control.tenant_routing` row is now `suspended`
> after its Supabase project was deleted mid-flight. This runbook doesn't model a
> `suspended` row anywhere below. Flagging the gap explicitly rather than asserting the
> procedure still holds — Royce to confirm before relying on this runbook if a rotation
> is ever needed while any tenant sits in a non-`active` routing state.

# SECURITY — TENANT_ROUTING_MASTER_KEY rotation runbook

## What this key is

`TENANT_ROUTING_MASTER_KEY` is a 32-byte AES-256-GCM master key stored as a
Netlify env var on **eq-shell only**. It is the single key that encrypts and
decrypts the Supabase `service_role` key for every tenant stored in
`shell_control.tenant_routing` on the **eq-canonical control plane**
(Supabase project ref: `jvknxcmbtrfnxfrwfimn`).

Encryption is implemented in `eq-shell/netlify/functions/_shared/encryption.ts`
(`encryptSecret` / `decryptSecret`). Decryption happens at request time inside
`fetchRoutingBySlug` in `tenant-routing.ts`. Every warm function instance caches
the decrypted result for up to 5 minutes (`CACHE_TTL_MS = 5 * 60 * 1000`).

Per-row storage in `shell_control.tenant_routing`:

| Column | Content |
|---|---|
| `service_role_key_ciphertext` | hex-encoded AES-256-GCM ciphertext |
| `service_role_key_iv` | hex-encoded 96-bit random IV (fresh per encryption call) |
| `service_role_key_tag` | hex-encoded 128-bit authentication tag |

The re-encryption script is `eq-shell/scripts/rekey-tenant-routing.mjs`. It was
used for the ad-hoc rotation on 2026-06-02. This runbook documents the full
procedure so future rotations are deliberate and auditable.

## Blast radius

One master key decrypts every tenant simultaneously. A compromised master key
gives an attacker the `service_role` key for every tenant's Supabase data-plane
project — unrestricted API access, RLS bypassed.

If compromise is suspected:
- Treat all tenant `service_role` keys as exposed.
- Rotate the master key AND rotate each tenant's Supabase `service_role` key
  separately (via Supabase Management API, per tenant). This runbook covers
  the master key rotation only.

---

## 1. Prerequisites

### Access required

| Requirement | Where |
|---|---|
| Netlify account with **eq-shell** env var write access | netlify.com — eq-shell site |
| Supabase personal access token (`sbp_...`) with read access to eq-canonical (`jvknxcmbtrfnxfrwfimn`) and all tenant data-plane projects | supabase.com — Account — Access Tokens |
| Platform-admin session on the running eq-shell deploy (for health-check call) | core.eq.solutions — log in as platform admin |
| Vault write access (1Password or equivalent) | — |
| Node.js 18+ on a local, trusted machine | for running `rekey-tenant-routing.mjs` |

### Tools

- `node` (18+) — for the rekey script
- `openssl` or `node -e` — for generating a new key
- Netlify CLI (optional alternative to UI): `netlify env:set`
- Access to Supabase SQL editor on eq-canonical (`jvknxcmbtrfnxfrwfimn`) for pre-rotation verification

---

## 2. Pre-rotation verification

Confirm the current key is working before touching anything.

### 2a. Count tenant rows and confirm none are missing

Run in the Supabase SQL editor on **eq-canonical** (`jvknxcmbtrfnxfrwfimn`),
schema `shell_control`:

```sql
SELECT
  t.slug,
  tr.tenant_id,
  tr.status,
  tr.supabase_project_ref,
  length(tr.service_role_key_ciphertext) AS ciphertext_len
FROM shell_control.tenant_routing tr
JOIN shell_control.tenants t ON t.id = tr.tenant_id
ORDER BY t.slug;
```

Note the exact row count. Every row must be re-encrypted. If any row has a
NULL `service_role_key_ciphertext`, investigate before proceeding — the rekey
script will fail on it.

### 2b. Verify the current key decrypts correctly

Call the health endpoint as a platform admin on the live deploy:

```
GET https://core.eq.solutions/.netlify/functions/tenant-routing-health
```

(Requires a valid platform-admin session cookie from core.eq.solutions.)

Expected response:

```json
{
  "ok": true,
  "tenants": [
    { "slug": "sks", "reachable": true, "table_counts": { ... } },
    ...
  ]
}
```

The `tenant-routing-health.ts` function calls `getTenantDataClient` for each
tenant and reports `reachable: true` if the data-plane connection succeeds.
Any `"reachable": false` with `"error": "misconfigured: ..."` indicates a
decryption failure with the current key — stop, diagnose, and do not proceed
with rotation until all tenants are reachable.

---

## 3. Rotation procedure

**Pick a low-traffic window.** Tenant routing will briefly fail between the
database update and the Netlify deploy going live — any request that tries to
decrypt a row re-encrypted with the new key while the env var still holds the
old key will throw `TenantRoutingMisconfiguredError`. The gap is typically
30–60 seconds (Netlify deploy time).

### 3a. Save the current key to the vault

Before doing anything else, copy the current value of `TENANT_ROUTING_MASTER_KEY`
from the Netlify UI (eq-shell — Site configuration — Environment variables)
directly into the vault:

- Vault entry: `TENANT_ROUTING_MASTER_KEY (eq-shell AES-256-GCM master key) — OLD [date]`
- Include the date saved and note it is the pre-rotation value

Never echo the key to a terminal, paste it into chat, log it, or commit it.

### 3b. Generate a new key

```sh
openssl rand -hex 32
```

Or equivalently:

```sh
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

This produces a 64-character hex string encoding 32 bytes — the exact format
`getMasterKey()` in `encryption.ts` expects. Copy the output immediately into
the vault as a **new entry**:

- Vault entry: `TENANT_ROUTING_MASTER_KEY (eq-shell AES-256-GCM master key) — PENDING [date]`

Do not close the vault or clear your clipboard until after step 3e.

### 3c. Re-encrypt all tenant_routing rows

Use `eq-shell/scripts/rekey-tenant-routing.mjs`. The script operates on **one
tenant slug at a time** — run it once per slug.

**Critical:** when called without `--master-key`, the script generates a
**different** new key for each run. Always supply `--master-key=<new-hex-key>`
(the key from step 3b) so all tenants share the same key.

For each tenant slug from step 2a (e.g. `sks`, `core`, etc.):

```sh
SUPABASE_ACCESS_TOKEN=sbp_<your-token> \
  node scripts/rekey-tenant-routing.mjs \
  --slug=<tenant-slug> \
  --master-key=<64-char-hex-from-step-3b>
```

Preview SQL without writing (dry run):

```sh
SUPABASE_ACCESS_TOKEN=sbp_<your-token> \
  node scripts/rekey-tenant-routing.mjs \
  --slug=<tenant-slug> \
  --master-key=<64-char-hex-from-step-3b> \
  --dry-run
```

What the script does per slug:

1. Fetches the eq-canonical control-plane service-role key via the Supabase
   Management API (`GET /v1/projects/jvknxcmbtrfnxfrwfimn/api-keys`).
2. Resolves `slug → tenant_id` via `shell_control.tenants` (PostgREST with
   `Accept-Profile: shell_control`).
3. Reads `supabase_project_ref` from `shell_control.tenant_routing`.
4. Fetches the data-plane `service_role` key from Management API
   (`GET /v1/projects/<data-plane-ref>/api-keys`) — fresh, not from the
   encrypted DB column, so the current master key is not needed.
5. Encrypts the fresh key with your `--master-key` (AES-256-GCM, fresh random
   12-byte IV per call via `randomBytes(12)`).
6. PATCHes `shell_control.tenant_routing` with the new
   `service_role_key_ciphertext`, `service_role_key_iv`, `service_role_key_tag`
   (PostgREST PATCH with `Content-Profile: shell_control`).

Confirm each run prints `→ DB updated ✓`. If any slug fails, **do not proceed
to step 3d** — a partially re-encrypted database with the old env var still
set is safe (old key still decrypts old rows). A partially re-encrypted
database after the new env var is set is broken.

Verify the count of slugs processed matches step 2a.

### 3d. Set the new key in Netlify

After all rows show `DB updated ✓`:

**Netlify UI:**
1. netlify.com — eq-shell — Site configuration — Environment variables.
2. Find `TENANT_ROUTING_MASTER_KEY`.
3. Edit. Replace the value with the new 64-char hex key.
4. Scope: **All scopes** (Production + Deploy Previews).
5. Save.

**Netlify CLI alternative:**
```sh
netlify env:set TENANT_ROUTING_MASTER_KEY <new-64-char-hex> --context production,deploy-preview
```

### 3e. Deploy eq-shell

The new env var is snapshotted at build time — it only takes effect once a new
deploy is live.

Netlify UI: Deploys — Trigger deploy — Deploy site.

Or via CLI (from eq-shell repo root):
```sh
netlify deploy --prod
```

Wait for the deploy to complete (green status). Do not proceed to verification
until the deploy is live.

### 3f. Verify all tenants load correctly

Wait 5 minutes after the deploy goes live for the 5-minute in-memory routing
cache (`CACHE_TTL_MS = 5 * 60 * 1000` in `tenant-routing.ts`) to expire across
all warm function instances. The cache holds already-decrypted `service_role_key`
values in the `cacheBySlug` and `cacheById` Maps — they must expire before
function instances will re-decrypt with the new key.

Alternatively, call `flushRoutingCache()` via an admin endpoint if one is
exposed — it clears `cacheBySlug`, `cacheById`, `tenantClients`, and
`tenantRpcClients` immediately.

Then call the health endpoint again:

```
GET https://core.eq.solutions/.netlify/functions/tenant-routing-health
```

Expected: `"ok": true` and every tenant reports `"reachable": true`.

Spot-check by making a live API call through Shell that exercises
`getTenantDataClient` or `getTenantRpcClientById` for at least one real tenant
(e.g. loading a tenant session that hits the data plane).

If any tenant shows `"reachable": false`, proceed to section 4 (Rollback).

---

## 4. Rollback procedure

### When to roll back

- One or more tenants show `"reachable": false` after the deploy is live and
  the 5-minute cache has expired.
- Sentry error: `decryptSecret: authentication failed (wrong key or tampered ciphertext)`.

### Rollback is not a simple env-var revert

After step 3c the database rows are already re-encrypted with the **new** key.
Reverting the env var to the old key would leave all rows unreadable (old key
cannot decrypt new ciphertext). Rollback means re-running the rekey script
using the old key.

### Rollback steps

1. Retrieve the old key from the vault entry saved in step 3a.

2. For each tenant slug, re-run the rekey script with the **old** key:

   ```sh
   SUPABASE_ACCESS_TOKEN=sbp_<your-token> \
     node scripts/rekey-tenant-routing.mjs \
     --slug=<tenant-slug> \
     --master-key=<old-64-char-hex>
   ```

   This fetches fresh service-role keys from the Management API and
   re-encrypts them under the old master key.

3. In Netlify, restore `TENANT_ROUTING_MASTER_KEY` to the old key.

4. Trigger a new deploy.

5. Wait 5 minutes (or flush cache), then verify via the health endpoint.

6. Investigate why the new-key deploy failed before retrying the rotation.
   Common causes: wrong key pasted into Netlify UI, a slug missed in step 3c,
   Netlify deploy picking up a cached build with the old env var.

---

## 5. Post-rotation steps

After successful verification:

1. **Update the vault.** Delete the `— PENDING` and `— OLD` entries. Create
   one clean entry:
   - Name: `TENANT_ROUTING_MASTER_KEY (eq-shell AES-256-GCM master key)`
   - Value: the new 64-char hex key (pasted from Netlify UI)
   - Fields: Netlify site (eq-shell, Production + Deploy Previews), rotation
     date, who rotated, link to this runbook
   - Access: restrict to owner + anyone with Netlify deploy access to eq-shell

2. **Record the rotation date.** Update the `last_updated` field in this
   runbook's front matter and add a row to the Rotation history table at the
   bottom of this file.

3. **Delete any intermediate files.** If you saved any local scripts or notes
   during the rotation, delete them now. Do not commit them to any repo.

4. **Clear shell history** if the key appeared in any terminal command. On
   macOS/Linux: `history -d <line>` or `history -c`. The key should not have
   appeared if you passed it via `--master-key=` flag, but verify.

---

## 6. Emergency rotation procedure

Use when the key is suspected or confirmed compromised and speed matters over
ceremony.

The rekey script fetches fresh service-role keys from the Supabase Management
API — it does not need to decrypt existing DB ciphertext. You can proceed
without the old key.

1. **Generate a new key immediately:**
   ```sh
   openssl rand -hex 32
   ```
   Copy to clipboard and vault (`— PENDING`) in one motion.

2. **Run the rekey script for every tenant slug** — run in parallel if you
   have multiple slugs (separate terminal tabs or background processes):

   ```sh
   SUPABASE_ACCESS_TOKEN=sbp_<token> \
     node scripts/rekey-tenant-routing.mjs \
     --slug=sks --master-key=<new-hex> &

   SUPABASE_ACCESS_TOKEN=sbp_<token> \
     node scripts/rekey-tenant-routing.mjs \
     --slug=core --master-key=<new-hex> &

   wait
   ```

3. **Set the new env var in Netlify** (can be done while scripts run if you
   have a second window open):
   ```sh
   netlify env:set TENANT_ROUTING_MASTER_KEY <new-hex>
   ```

4. **Trigger a deploy immediately** after all scripts show `→ DB updated ✓`.

5. **Verify** via health endpoint once deploy is live.

6. **After recovery** — if the old key was genuinely compromised, also rotate
   each tenant's Supabase `service_role` key via the Management API
   (`POST /v1/projects/<ref>/api-keys/refresh` — per tenant, outside this
   runbook). The rekey script uses the current live key fetched from the
   Management API, but if that key is also exposed, it must be cycled too.

7. **Notify affected tenants** if there is any evidence of data access using
   the compromised key.

---

## Caching note (reference)

`tenant-routing.ts` caches resolved routing for 5 minutes per warm function
instance. The cache holds decrypted `service_role_key` values in module-level
Maps: `cacheBySlug`, `cacheById`, `tenantClients`, `tenantRpcClients`. After a
deploy:

- **Wait 5 minutes** — natural expiry, no action needed.
- **Or call `flushRoutingCache()`** via a platform-admin endpoint if instant
  propagation is needed. This clears all four Maps.

`invalidateRoutingCache(slugOrId)` can flush a single tenant (used by
`provision-tenant.ts` after provisioning). For rotation, `flushRoutingCache()`
is appropriate as all tenants are affected.

---

## Cadence

**Default: rotate on suspected compromise or personnel change, not on a
fixed calendar.**

Mandatory rotation triggers:

- Any suspected key exposure (key visible in logs, chat, commit, screenshot,
  or shell history)
- Netlify account compromise
- Departing person who had Netlify env var write access to eq-shell
- Contractor offboarding with Netlify access

Once the procedure has been drilled end-to-end at least once, an **annual**
rotation is reasonable. Do not adopt a calendar cadence before that.

---

## Rotation history

| Date | Reason | Who | Notes |
|---|---|---|---|
| 2026-06-02 | Key mismatch fix (ad-hoc) | Royce Milmlow | No documented procedure at the time — this runbook written retroactively |

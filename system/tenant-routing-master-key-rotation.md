---
title: SECURITY — TENANT_ROUTING_MASTER_KEY rotation runbook
owner: Royce Milmlow
last_updated: 2026-06-02
scope: AES-256-GCM master key for tenant service-role key encryption — backup, re-encryption procedure, cache flush, cadence
read_priority: reference
status: live
---

# SECURITY — TENANT_ROUTING_MASTER_KEY rotation runbook

## What this key is

`TENANT_ROUTING_MASTER_KEY` is a 32-byte AES-256-GCM master key stored as a
Netlify env var on **eq-shell only**. It is the single key that encrypts and
decrypts the Supabase `service_role` key for every tenant stored in the
`tenant_routing` table on the **eq-canonical control plane** (Supabase project
ref: `jvknxcmbtrfnxfrwfimn`).

Encryption mechanics live in
`eq-shell/netlify/functions/_shared/encryption.ts`:

- Algorithm: AES-256-GCM (authenticated encryption)
- IV: 96-bit, randomly generated per encryption call (`randomBytes(12)`)
- Auth tag: 128-bit
- Each row in `tenant_routing` stores three columns:
  `service_role_key_ciphertext`, `service_role_key_iv`, `service_role_key_tag`

Because one master key decrypts every tenant row, **a Shell compromise is a
full-platform compromise** — all tenant `service_role` keys are exposed.

## Blast radius

Every tenant simultaneously. If the master key is compromised:

- An attacker can decrypt the `service_role` key for every tenant in
  `tenant_routing`, giving them unrestricted API access to every tenant's
  Supabase data-plane project.
- Immediate action required: re-encrypt all rows with a new key AND rotate the
  key before an attacker can exploit any decrypted credentials.
- Suspected exposure (even partial) requires treating all tenant
  `service_role` keys as compromised — notify affected tenants and initiate
  Supabase service-role key rotation per tenant alongside this procedure.

## Where it lives

| Location | Context | Role |
|---|---|---|
| Netlify env — **eq-shell** | Production | Minter and decryptor for all tenant routing |
| Netlify env — **eq-shell** | Deploy Previews | Minter and decryptor in preview deploys |
| **(gap) no vault backup** | — | If Netlify is wiped, value is unrecoverable |

**First action before any rotation:** copy the current value from the Netlify UI
directly into the team vault (1Password / Bitwarden — whichever EQ standardises
on). Never echo it to a terminal, paste it into a chat, log it, or commit it.
This document must never contain the value.

Vault entry contents:

- name: `TENANT_ROUTING_MASTER_KEY (eq-shell AES-256-GCM master key)`
- the 64-char hex value — pasted from Netlify UI directly
- Netlify site: eq-shell (Production + Deploy Previews)
- last-rotated date, who rotated, link to this runbook
- access restricted to owner + anyone with Netlify deploy access

## Caching note

`tenant-routing.ts` caches resolved routing rows for **5 minutes per warm
function instance** (`CACHE_TTL_MS = 5 * 60 * 1000`). The cache holds the
already-decrypted `service_role_key`. After rotating the master key and
re-encrypting all rows, the cache must expire before function instances will
re-decrypt with the new key.

Options after redeploying eq-shell:

1. **Wait 5 minutes** — all warm instances expire their caches naturally.
2. **Call `flushRoutingCache()`** from a trusted admin endpoint — this clears
   `cacheBySlug`, `cacheById`, `tenantClients`, and `tenantRpcClients` maps
   immediately. Prefer this if you need instant propagation.

## Rotation procedure

### Constraints

- The re-encryption of all rows and the Netlify env var update must happen in
  the same maintenance window. A row re-encrypted with the new key while the
  env var still holds the old key will fail to decrypt on the next request.
- Do not rotate under load. There is a brief window between re-encrypting rows
  and the Netlify redeploy going live; any request that hits a row encrypted
  with the new key before the env var is updated will fail. Pick a low-traffic
  window and work quickly.

### Step-by-step

1. **Pick a low-traffic window.** Inform the team that tenant routing may
   briefly fail during the transition.

2. **Read ALL rows** from `tenant_routing` on eq-canonical
   (`jvknxcmbtrfnxfrwfimn`). Capture `tenant_id`,
   `service_role_key_ciphertext`, `service_role_key_iv`,
   `service_role_key_tag` for every row. Do not skip any row — a missed row
   will become unreadable once the env var is updated.

3. **Decrypt each row** with the current key using the Node.js helper below
   (see Re-encrypt helper). Keep decrypted values only in a secure in-memory
   variable — never write them to disk, logs, or chat.

4. **Generate a new key:**

   ```sh
   openssl rand -hex 32
   ```

   Copy the output immediately into the vault. Do not keep it in shell history
   (run the command from a script or clear history after). This is your new
   `TENANT_ROUTING_MASTER_KEY`.

5. **Re-encrypt each decrypted `service_role` key** with the new master key
   using the same AES-256-GCM approach. Each re-encryption generates a fresh
   random IV — do not reuse the old IV. See the helper below.

6. **Update all `tenant_routing` rows** with the new
   `service_role_key_ciphertext`, `service_role_key_iv`,
   `service_role_key_tag` values. All rows must be updated before the next
   step. Verify the row count matches what you read in step 2.

7. **Set the new key** as the Netlify env var on eq-shell — both Production
   and Deploy Previews. Name: `TENANT_ROUTING_MASTER_KEY`.

8. **Redeploy eq-shell.** The new key is snapshotted into the deploy; it only
   takes effect once the deploy goes live.

9. **Wait 5 minutes** for in-memory cache expiry across all warm function
   instances, or call `flushRoutingCache()` via a platform-admin endpoint if
   you need immediate effect.

10. **Verify** by hitting the tenant-routing-health endpoint
    (`eq-shell/.netlify/functions/tenant-routing-health` — platform-admin
    access required). All tenants should report `reachable: true`. Spot-check
    a live tenant API call through Shell to confirm decryption is working.

11. **Update the vault entry** with the new value and today's rotation date.
    Delete any intermediate files or scripts used during rotation.

### Do NOT during rotation

- Do not rotate under load — there is an unavoidable gap between row
  re-encryption and the Netlify deploy going live.
- Do not skip any `tenant_routing` row — a missed row becomes permanently
  unreadable after the env var is updated.
- Do not store the key in git, logs, chat, shell history, or any file
  committed to the repo.
- Do not keep decrypted `service_role` keys in any persistent storage.

## Re-encrypt helper

Run this Node.js snippet in a **local, trusted** environment to decrypt and
re-encrypt a single `tenant_routing` row. The script mirrors the exact
AES-256-GCM mechanics from `encryption.ts`.

```js
// re-encrypt-row.js — run locally, never commit
// Usage: OLD_KEY=<hex> NEW_KEY=<hex> node re-encrypt-row.js
//
// Supply one row at a time, or wrap in a loop over all rows.
// Set OLD_KEY and NEW_KEY as environment variables — do not hard-code them.

const { createCipheriv, createDecipheriv, randomBytes } = require('node:crypto');

const ALGORITHM = 'aes-256-gcm';
const IV_BYTES = 12;
const TAG_BYTES = 16;

function decrypt(oldKeyHex, ciphertextHex, ivHex, tagHex) {
  const key  = Buffer.from(oldKeyHex.trim(), 'hex');
  const ct   = Buffer.from(ciphertextHex, 'hex');
  const iv   = Buffer.from(ivHex, 'hex');
  const tag  = Buffer.from(tagHex, 'hex');
  const dec  = createDecipheriv(ALGORITHM, key, iv);
  dec.setAuthTag(tag);
  return Buffer.concat([dec.update(ct), dec.final()]).toString('utf8');
}

function encrypt(newKeyHex, plaintext) {
  const key = Buffer.from(newKeyHex.trim(), 'hex');
  const iv  = randomBytes(IV_BYTES);
  const enc = createCipheriv(ALGORITHM, key, iv);
  const ct  = Buffer.concat([enc.update(plaintext, 'utf8'), enc.final()]);
  const tag = enc.getAuthTag();
  return {
    ciphertext: ct.toString('hex'),
    iv:         iv.toString('hex'),
    tag:        tag.toString('hex'),
  };
}

// --- Replace these with values from the tenant_routing row ---
const OLD_KEY       = process.env.OLD_KEY;
const NEW_KEY       = process.env.NEW_KEY;
const CIPHERTEXT    = '<service_role_key_ciphertext from DB>';
const IV            = '<service_role_key_iv from DB>';
const TAG           = '<service_role_key_tag from DB>';
// -------------------------------------------------------------

if (!OLD_KEY || !NEW_KEY) {
  console.error('Set OLD_KEY and NEW_KEY env vars. Do not hard-code keys.');
  process.exit(1);
}

const plaintext = decrypt(OLD_KEY, CIPHERTEXT, IV, TAG);
const reEncrypted = encrypt(NEW_KEY, plaintext);

console.log('New ciphertext:', reEncrypted.ciphertext);
console.log('New iv:        ', reEncrypted.iv);
console.log('New tag:       ', reEncrypted.tag);
// Use these three values to UPDATE the row in tenant_routing.
// Then discard this script. Do not commit it.
```

Wrap the decrypt/encrypt pair in a loop over all rows fetched from
`tenant_routing` in step 2, collecting the new `{ ciphertext, iv, tag }` per
`tenant_id` before writing any updates to the database. Only start writing
once all rows are re-encrypted in memory — this minimises the window where
some rows use the old key and others use the new key.

## Alerting follow-up (backlog item — do not build here)

`eq-shell/netlify/functions/tenant-routing-health.ts` is an on-demand probe.
It is not scheduled and does not alert on failure. Recommended as a separate
backlog item: schedule this probe as a cron (e.g. every 5 minutes) and alert
via Sentry or PagerDuty when any tenant reports unreachable. This would have
caught any post-rotation decryption failure automatically rather than requiring
manual verification in step 10.

## Cadence

**Default: rotate on suspected compromise or personnel change, not on a fixed
calendar.**

Mandatory triggers:

- Any suspected exposure of the key (logs, chat, commit, screenshot)
- A departing person who had Netlify access to eq-shell env vars
- Netlify account compromise
- Contractor offboarding with Netlify access

Once a re-encrypt helper script exists (see above) and the procedure has been
drilled end-to-end, an **annual** rotation is reasonable. Do not adopt a
calendar cadence until the procedure is scripted and tested — an untested
rotation under pressure is a reliability risk.

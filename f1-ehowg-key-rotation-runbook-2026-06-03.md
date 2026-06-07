---
title: F1 — Rotate the exposed ehowg (sks-canonical) service_role key
owner: Royce Milmlow
created: 2026-06-03
last_updated: 2026-06-07
status: live
read_priority: critical
scope: Kill the leaked SKS-canonical service_role key and swap the new one into both consumers
---

**Status:** ready-to-run (P0, Royce-gated).

# F1 runbook — rotate the leaked SKS database key

## Plain-English summary

The SKS database (`ehowg…` = sks-canonical) has a **master key** (admin password).
It leaked and — verified 2026-06-03 — **it still works**. This runbook swaps it
for a new one and updates the two things that use it, in the order that avoids
breaking them.

**Two things use this key right now:**
1. **The Quotes app** (`eq-quotes-sks` on Fly) — Fly secret `SUPABASE_SERVICE_ROLE_KEY`.
2. **The routing layer** (`shell_control.tenant_routing` in eq-canonical) — the
   `sks` row (`tenant_id = 7dee117c-98bd-4d39-af8c-2c81d02a1e85`), key stored
   encrypted.

If you switch off the old key **before** giving these two the new one, both break.
So: rotate → swap into both → confirm old key is dead.

## Verified state that triggered this (2026-06-03)
- Leaked legacy `service_role` JWT still authenticates: read a live SKS row, **HTTP 200**
  (bad-key control returns 401). Key `iat` ≈ 2026-05-24, unchanged → never rotated.
- Both consumers still hold the legacy key (`tenant_routing` `status_changed_at` = 2026-05-24;
  Quotes Fly secret `SUPABASE_SERVICE_ROLE_KEY` present, no `sb_secret` migration).

## Before you start — gather two secrets (no downtime yet)
1. **Existing master key** — Netlify → eq-shell site → Environment variables →
   `TENANT_ROUTING_MASTER_KEY` → context **production** → reveal & copy.
   (The CLI masks it; you must reveal it in the web UI.)
2. **Supabase access token** — dashboard → Account → Access Tokens → create/copy
   an `sbp_…` token (the CI one may be expired).

## The steps (downtime starts at step 1, ~1 min for Quotes)

### Step 1 — rotate the key (you, Supabase dashboard)
`ehowg` (sks-canonical) → Settings → API → **rotate the JWT secret**.
This instantly kills the leaked key and issues a new legacy `service_role` key.
> Rotating the JWT secret also changes the ehowg **anon** key — that's expected;
> step 3b refreshes it in the routing row.

### Step 2 — swap new key into Quotes (Fly secret)
Fetches the new key via the authed Supabase CLI and sets it (value never printed):
```bash
NEWKEY=$(supabase projects api-keys --project-ref ehowgjardagevnrluult -o json \
  | python -c "import sys,json;print([k['api_key'] for k in json.load(sys.stdin) if k['id']=='service_role'][0])")
flyctl secrets set SUPABASE_SERVICE_ROLE_KEY="$NEWKEY" -a eq-quotes-sks
```
`flyctl secrets set` redeploys eq-quotes-sks (~30–60s). Quotes back up after this.

### Step 3a — re-encrypt the new key into the routing row (you)
Uses the project's own re-key script. `--master-key` with your **existing** key means
**no eq-shell redeploy** — only the database row changes:
```bash
cd C:\Projects\eq-shell
SUPABASE_ACCESS_TOKEN=sbp_YOURTOKEN node scripts/rekey-tenant-routing.mjs --slug=sks --master-key=PASTE_EXISTING_MASTER_KEY
```
The script auto-fetches the new ehowg service_role key (Management API), re-encrypts it,
and PATCHes the `sks` routing row. Expect `→ DB updated ✓`.

> If you OMIT `--master-key`, the script generates a NEW master key and prints it —
> you must then set it on eq-shell Netlify (production) and redeploy eq-shell. Avoid
> this unless you want to rotate the master key too.

### Step 3b — refresh the routing row's anon key (public; safe to do via SQL)
The rotation changed ehowg's anon key. Update the plaintext `supabase_anon_key`:
```bash
NEWANON=$(supabase projects api-keys --project-ref ehowgjardagevnrluult -o json \
  | python -c "import sys,json;print([k['api_key'] for k in json.load(sys.stdin) if k['id']=='anon'][0])")
echo "$NEWANON"   # anon key is public — safe to paste into an UPDATE
```
Then UPDATE `shell_control.tenant_routing` SET `supabase_anon_key` = '<NEWANON>'
WHERE `tenant_id` = '7dee117c-98bd-4d39-af8c-2c81d02a1e85' (via Supabase MCP or SQL editor).

### Step 4 — verify the leaked key is dead
```bash
KEY=$(supabase projects api-keys --project-ref ehowgjardagevnrluult -o json \
  | python -c "import sys,json;print([k['api_key'] for k in json.load(sys.stdin) if k['id']=='service_role'][0])")
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://ehowgjardagevnrluult.supabase.co/rest/v1/sks_quotes_customers?select=id&limit=1" \
  -H "apikey: $KEY" -H "Authorization: Bearer $KEY"
```
This fetches the **new** key, so it returns **200** (proves the new key works). To prove
the **old leaked** key is dead, run the same curl with the old key value — expect **401**.
The decisive operational signal: Quotes + Service→SKS write-through keep working after
steps 2–3, and the old key value no longer authenticates.

## If something breaks (rollback)
- **Quotes erroring after step 1, before step 2:** that's the expected ~1-min window —
  complete step 2.
- **Quotes still erroring after step 2:** confirm the Fly secret deployed
  (`flyctl secrets list -a eq-quotes-sks` — check `SUPABASE_SERVICE_ROLE_KEY` digest changed),
  and that the new key authenticates (step 4 → 200).
- **Service→SKS write-through failing:** step 3a didn't take — re-run it; check the
  master key matches what eq-shell production holds.
- **Full rollback:** re-rotate the JWT secret again and re-run steps 2–3 with the newest key.
  (You can't restore the *leaked* key — that's the point.)

## Other consumers to double-check
Known consumers are the two above. If anything else holds the ehowg service_role key
directly (search for `SUPABASE_SERVICE_ROLE_KEY` / hardcoded ehowg keys in eq-shell
functions, other Fly apps), update them too before declaring done.

## After completion
- Update `STATE.md` top block + `SPRINT-BOARD.md` F1 row → 
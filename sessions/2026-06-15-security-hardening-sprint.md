---
date: 2026-06-15
topic: Security hardening sprint — eq-shell (PRs #369/#370) + eq-cards deployed
tier: EQ
status: done
---

# Security hardening sprint — 2026-06-15

Continued from the SKS Field staff load session (same date). Full sprint with
blanket authorisation from Royce ("merge and finish anything you deem worth it
— full approvals").

## Completed

### eq-shell

**PR #369 — anthropic-proxy + workers-canonical-sync (merged)**
- `anthropic-proxy.ts`: added session cookie auth + narrowed CORS to
  `*.eq.solutions`. Was an open relay on the server Anthropic API key.
- `workers-canonical-sync/index.ts`: first-time git tracking of the live jvkn
  edge function (v4). Fixes SKS tenant constant (dcb71d03 → 7dee117c) and adds
  `field_approved=true` on all synced workers.

**PR #370 — mint-iframe-token H1 fix (merged)**
- Non-platform-admin users are now bound to their Shell tenant's
  `field_tenant_slug` when requesting Field iframe tokens. Platform admins
  retain full picker. 403 on mismatch.

**M1 — ENFORCE_IFRAME_ORIGIN=true**
- Set as Netlify env var on eq-shell (production/functions scope). Origin check
  now enforcing (was report-only).

**EQ Field v3.5.151**
- `loadCanonicalStaffMap` now filters `&on_roster=eq.true` so off-roster staff
  don't appear in the scheduling grid.

### eq-cards (committed + deployed to cards.eq.solutions)

**Migrations committed (all already live on jvkn):**
- `0032`: `_verify_pin_throttled()` — exponential backoff 1–60 min on PIN
  brute-force (`pin_failed_attempts`/`pin_locked_until` on `shell_control.users`)
- `0033`: REVOKE EXECUTE on `sync_worker_to_canonical` +
  `sync_credential_to_canonical` from public/anon/authenticated
- `0034`: per-slug rate limit on `eq_cards_lookup_invite_by_phone` (50 req/10 min)

**New dart code:**
- `InviteLookupApi`: routes invite-by-phone lookups through Shell `cards-api`
  gateway (per-attacker IP throttle) instead of direct anon Supabase RPC
- `RateLimitedFailure`: new sealed subclass + user-facing message
  ("Too many attempts. Try again in N minutes.")
- `ClaimByPhoneScreen`: now surfaces `userMessageForError()` on failure

**CSP:**
- Removed stale `cdnjs.cloudflare.com` from `script-src` + `style-src` in
  `web/_headers`. Nothing in the app loads from that CDN.

## Verified (no fix needed)

- **jvkn `custom_access_token_hook`**: live, correctly injects `tenant_id` /
  `eq_role` / `is_platform_admin` into JWT claims for all 5 workers who have
  authenticated.
- **Phone dedup**: 0 duplicate phones in `auth.users` on jvkn. Hook is clean.
- **Workers pipeline**: 68 jvkn workers → 68 ehow staff (all with
  `cards_worker_id`). Sync pipeline is correct end-to-end.

## Still open (Royce decisions required)

- **63 uninvited workers** — have rows in jvkn.workers but no worker_invite
  records. Cannot sign in to Cards until invites are created and sent (SMS to
  63 real people). Royce to trigger.
- **Roster data entry** — ehow has 0 schedule_entries, 0 timesheets,
  0 leave_requests. Supervisors can see staff but nothing to schedule.
  Royce confirmed: start fresh on ehow, no migration from nspb.
- **Daniel Bower** — in Field but not on the authoritative SKS staff list.
  Needs Royce confirmation before archiving.

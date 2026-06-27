---
title: Canonical Wiring — Activation Status & Morning Continuation
date: 2026-06-07 (EOD)
status: archived
companion: canonical-wiring-deploy-runbook-2026-06-07.md (the plan); this doc (what actually happened + what's left)
owner: Royce Milmlow
last_updated: 2026-06-22
scope: Canonical wiring activation log — what shipped 2026-06-07 and what remained gated
read_priority: reference
---

# Canonical Wiring — Activation Status (2026-06-07 EOD)

The 6-step canonical wiring program is **deployed and live across all five surfaces.** The reference
layer is now durably fed (transactional outboxes + retry on every writer), the quote→job spine exists
end-to-end, and it self-heals (reconcile sweeps). Three items remain — all need secret values I cannot
read, so they are yours to finish in the morning. None block each other; the system is in a clean,
non-broken state.

---

## 1. Deployed & live (verified against the running system)

| Surface | Schema (live) | Code | How it was verified |
|---|---|---|---|
| **eq-shell** | `0043_jobs_canonical_upsert_index` → `jobs_tenant_external_id_uidx` on **core + sks** | PR #223 merged → Netlify (core.eq.solutions) | index present via SQL on both planes; `canonical-api` returns 401 (live) |
| **Service** | `0122_canonical_outbox` on urjh (RLS on, 0 policies) | PR #249 + #250 merged → Netlify (service.eq.solutions) | Sentry release = merge SHA on live site; drain/reconcile routes return 401 (auth enforced, reachable) |
| **Quotes** | `035_canonical_outbox` on ehow (RLS on, 0 policies) | Fly deploy ✅ (eq-quotes-sks) | `/healthz` 200; `/api/cron/drain-canonical-outbox` 401 |
| **Field** | n/a (code-only retry) | `shift-events` edge fn → nspb (SKS-live) | `supabase functions deploy` exit 0; bundle compiled |
| **eq-context** | — | docs PRs #22 merged to main | this file + audit + runbook on main |

What each piece does:
- **Service / Quotes outbox**: a write to canonical that fails transiently (network/5xx/429/408) is enqueued
  and replayed by a scheduled drainer with exponential backoff until delivered or `dead`. The hub upserts
  idempotently on `(tenant_id, external_id)`, so replays are safe.
- **eq-shell `quote-job-consumer`** (15-min): reads `quote.accepted` events and PUTs `app_data.jobs`
  (`external_id='eq-quotes:job:<quote_id>'`) — the quote→job spine.
- **Reconcile sweeps** (daily): re-sync any customer/site with `canonical_id IS NULL` — drift backstop.
- **Field `shift.started`**: now retries the canonical emit (4 attempts, 1/3/7s backoff) instead of a
  single best-effort fetch.

---

## 2. Three bugs caught and fixed during activation

Each would have failed silently in production:

1. **eq-shell migration ledger self-insert** — the jobs-index migration self-inserted a bare-named,
   null-checksum row into `app_data._eq_migrations` (the runner is the sole ledger writer; a self-insert
   creates a twin it never reconciles — the exact failure `0039` hit). Stripped it; hygiene CI green.
   *(Royce then renamed `0040→0043` to clear the duplicate-prefix collision with `0040_assets_assigned_to`.)*

2. **Service migration `0099` version collision** — main was already at `0121`; the outbox migration reused
   `0099` and duplicate-keyed `schema_migrations` (integration test failed). Renumbered to `0122`; aligned
   the live urjh ledger row.

3. **Service cron routes blocked by the auth proxy** — `canonical-outbox-drain` / `reconcile-canonical`
   were not in `PUBLIC_PATHS` (lib/auth/mfa-routing.ts), so `proxy.ts` 307-redirected the scheduler's POST
   to `/auth/signin` and **the outbox would never have drained**. Added them (handlers still enforce
   `Bearer CRON_SECRET` internally). Caught by a live HTTP probe post-deploy; fix #250 confirmed live
   (routes now 401, not 307).

---

## 3. Outstanding — your actions (need secret values I cannot read)

### 3a. `QUOTES_CRON_SECRET` on eq-shell Netlify  ·  2-minute paste
The eq-shell Quotes schedulers (`canonical-outbox-quotes-scheduler` 5-min, `canonical-reconcile-quotes-scheduler`
daily) call the Quotes app with this bearer. It must equal Quotes' existing `CRON_SECRET` (a Fly secret —
I can't read its value).
- Set `QUOTES_CRON_SECRET` in **eq-shell → Netlify → env vars** = Quotes' `CRON_SECRET`.
- Until set: those two schedulers 401 harmlessly. Quotes' own inline enqueue + reconcile still work; only
  the cross-app *scheduled* drain waits.

### 3b. Field cron — `shift-events` is deployed but DORMANT  ·  gated (SKS-live + secrets)
The edge fn is on nspb, but **nothing triggers it** — on nspb there is no `shift-events-daily` cron job, no
`trigger_shift_events` helper, and `app_config` has neither `shift_events_fn_url` nor `shift_events_fn_token`.
The retry-hardened code is staged only. To actually turn it on (recipe is in
`eq-solves-field/migrations/2026-06-02_shift_events_cron.sql`):
1. Set the function's secrets (Supabase dashboard → Edge Functions → shift-events):
   `CANONICAL_API_URL=https://core.eq.solutions`, `CANONICAL_API_KEY_FIELD=<value from eq-shell Netlify>`,
   `CANONICAL_TENANT_SLUG=sks`. **Without `CANONICAL_API_KEY_FIELD` the fn dry-runs and emits nothing.**
2. Seed `public.app_config` on nspb with `shift_events_fn_url` and `shift_events_fn_token` (service-role JWT).
3. Apply the cron migration to nspb.
4. Test: `SELECT public.trigger_shift_events(true);` (dry-run, no canonical write).
Decision for you: this is a net-new SKS-live scheduled job. I left it gated rather than firing it overnight.
Tell me "wire the field cron" + drop the key/JWT and I'll do steps 1–4.

### 3c. Keystone E2E — confirm quote → job  ·  needs a test quote (or the SHELL key)
Currently `app_data.jobs` on the sks plane = **0 rows** (no quote accepted since activation, so the consumer
has no event yet — expected, not a fault). To prove it:
- **Option A (real):** accept a test quote in Quotes → within ≤15 min check on ehow:
  `select external_id, quote_id, title from app_data.jobs where external_id like 'eq-quotes:job:%';` → expect a row.
- **Option B (fast smoke):** drop me `CANONICAL_API_KEY_SHELL` and I'll `PUT` a test job through the hub
  (`{resource:'jobs', external_id:'eq-quotes:job:<test-uuid>', quote_id:'<uuid>', title:'smoke'}`,
  `X-Tenant: sks`) → expect 201, then delete it.

---

## 4. Follow-up (logged as a background task, not blocking)
- **`integration.yml` CI is broken repo-wide on Service** — `supabase start` fails at "Updating vector
  buckets" with a 409 ("Vector service not configured"), on **every** PR and main since ~Jun 6. Unrelated to
  this work; needs a Supabase-CLI pin or a `config.toml` vector/storage fix. (This is why #249's integration
  check was red — its migration + typecheck both passed.)

---

## 5. State of git (all merged to main)
- eq-shell #223 (canonical wiring), Service #249 (outbox) + #250 (cron auth fix), Quotes #35 (outbox),
  Field #228 (retry), eq-context #22 (docs) — **all merged.**
- Live data fixes from earlier in the day (WS2 site backfill, WS1 stubs, quote canonical_ids on ehow) are
  applied and reversible (rollbacks recorded in the WS docs).

**Bottom line:** everything that could be safely completed without your secrets is done and verified. The
three remaining items are teed up above — each is a short, well-scoped step.

---
title: OPS — Secrets Inventory
owner: Royce Milmlow
last_updated: 2026-08-08
scope: Names, owner app, environment, and where-set for every real secret across the EQ/SKS Netlify projects. No values — this is the map, not the vault. Companion to ops/security-register.md (incident/finding history) and the Grok-authored "Secrets & Environment Variables" guide (Google Drive, 2026-08-08), which recommends exactly this file.
read_priority: high
status: live
---

# Secrets Inventory

One place to see *what* secrets exist and *where they live* — never what they
are. Values are never written here. Built 2026-08-08 from a live
`getAllEnvVars` sweep of 4 of 5 core Netlify projects (eq-cards blocked by
the Netlify tool's own safety classifier this pass — not yet reconfirmed,
rows below carry the last confirmed date instead). Full incident history for
any row marked with a SEC-* ID lives in
[`ops/security-register.md`](security-register.md).

**Delivery layer for all rows below:** Netlify per-site environment
variables (Site settings → Environment variables), scope usually
`builds`/`functions`/`runtime`. See the PDF for the fuller layer model
(browser / Netlify / Supabase Edge/Vault / GitHub Actions / local / password
manager) — this file only covers the Netlify layer, which is where every
open finding to date has been.

**Rotation cadence (per the PDF's guidance, not yet formally adopted):** API
keys (Resend, Anthropic, Twilio, Google) → 90 days. Infra secrets (Supabase
service_role, JWT secrets) → 180 days. Any row flagged below (open SEC-* /
not masked) → immediate, once Royce actions it.

---

## eq-shell (`core.eq.solutions`, site `a3473f83-7c82-4f1e-872d-aa96eaa55172`)

| Secret name | Masked? | Where set | Notes |
|---|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY` | ⚠ leaks via `dev` | Netlify (all contexts) | jvkn/eq-canonical service_role. **SEC-9** — confirmed leaking via `dev` context today despite `is_secret:true`. |
| `EQ_SHELL_JWT_SECRET` | ⚠ leaks via `dev` | Netlify (all contexts) | Signs every session JWT suite-wide. **SEC-9 addendum.** |
| `EQ_QUOTES_HANDOFF_KEY` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** `dev-server` context is empty (clean) — only `dev` leaks. |
| `CANONICAL_API_KEY_SERVICE` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `CANONICAL_API_KEY_FIELD` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `EQ_PLATFORM_ADMIN_KEY` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `EQ_SESSION_SALT` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `EQ_SERVICE_HANDOFF_KEY` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `EQ_SHELL_BRIDGE_SECRET` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `SKS_SUPABASE_JWT_SECRET` | ⚠ leaks via `dev` | Netlify (all contexts) | **SEC-9 addendum.** |
| `SUPABASE_JWT_SECRET` | ⚠ leaks via `dev` | Netlify (all contexts) | jvkn legacy JWT secret. **SEC-9 addendum.** |
| `QUOTES_CRON_SECRET` | ✗ not masked, all contexts | Netlify | **SEC-24 — OPEN.** Full plaintext including production. |
| `GOOGLE_DOC_AI_CREDENTIALS` | ✓ masked | Netlify (production) | Full GCP service-account JSON. `dev` context empty — clean. |
| `SUPABASE_ACCESS_TOKEN` | ✓ masked | Netlify | Used by `security_audit.py`'s advisor-audit step. `dev` empty. |
| `CANONICAL_API_KEY_QUOTES` | ✓ masked | Netlify (all) | Single-context var, no separate `dev` value. |
| `CANONICAL_API_KEY_SHELL` | ✓ masked | Netlify (production) | No `dev` context exists for this one. |
| `RESEND_API_KEY` | ✓ masked | Netlify (all) | |
| `ANTHROPIC_API_KEY` | ✓ masked | Netlify (production) | No `dev` context exists for this one. |
| `TWILIO_AUTH_TOKEN` | ✓ masked | Netlify | `dev` empty. |
| `EQ_SECRET_SALT` | ✓ masked | Netlify (all) | Single-context var. |
| `TENANT_ROUTING_MASTER_KEY` | ✓ masked | Netlify | `dev` empty. |
| `FIELD_SUPABASE_SERVICE_ROLE_KEY` | ✓ masked | Netlify | `dev` empty. |
| `SCHEDULER_TEST_SECRET` | ✓ masked | Netlify | `dev` empty. |
| `EQ_SERVICE_API_KEY` | ✓ masked | Netlify | `dev` empty. |
| `VITE_SUPABASE_ANON_KEY` | ✓ masked | Netlify (all) | Anon key — meant to be public in the browser regardless. |
| `VITE_GOOGLE_MAPS_KEY` | ✗ not flagged secret | Netlify (all) | Client-side, domain-restricted by design — low real sensitivity, but worth a `is_secret` tick for hygiene. |

---

## eq-field (`field.eq.solutions`, site `554a0f1f-d524-4677-98c6-08e7c1edc92b`)

| Secret name | Masked? | Where set | Notes |
|---|---|---|---|
| `SKS_JWT_SECRET` | ⚠ leaks via `dev` | Netlify (all contexts) | Same value as eq-shell's `SKS_SUPABASE_JWT_SECRET`. **SEC-9 addendum.** |
| `EQ_FIELD_HANDOFF_KEY` | ✗ not masked, all contexts | Netlify | **SEC-18 — still open**, unchanged since 2026-07-30. |
| `LEAVE_CANONICAL_JWT_SECRET` | ✓ masked | Netlify | No `dev` context on this var at all — clean. |
| `RESEND_API_KEY` | ✓ masked | Netlify | `dev` empty. |
| `AUDIT_SB_KEY` | ✓ masked | Netlify | |
| `EQ_SECRET_SALT` | ✓ masked | Netlify | `dev` empty on this site — clean, unlike eq-shell/eq-service. |
| `SUPABASE_JWT_SECRET` | ✓ masked | Netlify | `dev` empty. |
| `CANONICAL_SERVICE_ROLE_KEY` | ✓ masked | Netlify | `dev` empty. |
| `ZAAP_JWT_SECRET` | ✓ masked | Netlify | `dev` empty. |
| `EHOW_SERVICE_ROLE_KEY` | ✓ masked | Netlify | No `dev` context configured. |
| `STAFF_CODE` / `MANAGER_CODE` | n/a | Netlify | Shared app-level access codes, not credentials in the classic sense — lower sensitivity, not `is_secret`-flagged by design. |

---

## eq-service (`service.eq.solutions`, site `6af7bce6-9d4c-4567-88fa-783abf5eb041`)

| Secret name | Masked? | Where set | Notes |
|---|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY` | ⚠ leaks via `dev` | Netlify | **Points at the deleted `urjh` project** — dead var, cleanup candidate, not a live risk. |
| `EQ_PLATFORM_ADMIN_KEY` | ⚠ leaks via `dev` | Netlify | **SEC-9 addendum.** |
| `EQ_SECRET_SALT` | ⚠ leaks via `dev` | Netlify | **SEC-9 addendum.** |
| `EQ_SHELL_JWT_SECRET` | ⚠ leaks via `dev` | Netlify | **SEC-9 addendum.** |
| `CANONICAL_API_KEY_SERVICE` | ⚠ leaks via `dev` | Netlify | **SEC-9 addendum.** |
| `EQ_SERVICE_HANDOFF_KEY` | ✗ not masked, single context | Netlify | **SEC-18 — still open.** |
| `EQ_SERVICE_JWT_SECRET` | ✗ not masked, all contexts | Netlify | **SEC-18 — still open.** |
| `EQ_SERVICE_API_KEY` | ✗ not masked, all contexts | Netlify | **SEC-18 — still open.** |
| `EQ_SHELL_BRIDGE_SECRET` | ✓ masked | Netlify | No `dev` context on this site — clean. |
| `CANONICAL_SERVICE_ROLE_KEY` | ✓ masked | Netlify | ehow/sks-canonical service_role — the live DB behind Service + Field. `dev` empty. |
| `RESEND_API_KEY` | ✓ masked | Netlify | `dev` empty. |
| `GITHUB_TOKEN` | ✓ masked | Netlify (production) | |
| `SENTRY_AUTH_TOKEN` | ✓ masked | Netlify | `dev` empty. |
| `SITE_CREDENTIALS_KEY` | ✓ masked | Netlify | No `dev` context. |
| `SUPABASE_JWT_SECRET` | ✓ masked | Netlify | No `dev` context on this site. |
| `CRON_SECRET` | ✓ masked | Netlify | `dev` empty. |
| `EQ_SESSION_SALT` | ✓ masked | Netlify | `dev` empty. |
| `UNSUBSCRIBE_SECRET` | ✓ masked | Netlify | `dev` empty. |

---

## sks-nsw-labour (`sks-nsw-labour.netlify.app`, site `bd00e7db-09a4-4f0e-a996-105cd63b0c8b`)

| Secret name | Masked? | Where set | Notes |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | ✓ masked | Netlify | **SEC-10 — closed 2026-07-30**, `dev` empty, re-verified clean today. |
| `RESEND_API_KEY` | ✓ masked | Netlify | **SEC-10 — closed 2026-07-30**, `dev` empty, re-verified clean today. |
| `EQ_SECRET_SALT` | ✓ masked | Netlify | `dev` empty, re-verified clean today. |
| `STAFF_CODE` / `MANAGER_CODE` | n/a | Netlify | Shared app-level access codes. |

Under the "don't touch sks-nsw-labour" freeze (**SEC-1**) — nothing here needs
action, listed for completeness only.

---

## eq-cards — NOT RE-VERIFIED 2026-08-08

Netlify tool's own classifier blocked the live read this pass. Last confirmed
via **SEC-18** (2026-07-27/30): `SUPABASE_SERVICE_ROLE_KEY` (jvkn control
plane) and `SUPABASE_JWT_SECRET` were re-stored masked and verified `is_secret:
true`; `EQ_SECRET_SALT` and `EQ_SESSION_SALT` were flagged exposed and **left
open** ("still not touched" per the register). Treat this whole site as
**unverified** until re-swept — do not assume the `dev`-context bug is absent
here just because it wasn't re-checked.

## Other Netlify projects (checked, low/no risk)

`eq-receipts` — `VITE_SUPABASE_URL` (plain URL, not a secret) and
`VITE_SUPABASE_ANON_KEY` (`is_secret:true`, and an anon key is meant to be
public regardless) — no real secret. `sks-comms`, `eq-core-design`,
`knx-job-folder`, `life-tracking` — zero env vars configured, nothing to
expose (confirmed via SEC-18, not re-checked today, low-churn hobby
projects).

---

## Open actions (manual-hands-only, Royce via Netlify dashboard/CLI)

1. **Re-store `QUOTES_CRON_SECRET`** (eq-shell) as masked, same value — closes SEC-24.
2. **Clear the `dev`-context value** on the 17 vars flagged "⚠ leaks via `dev`" above (eq-shell ×11, eq-field ×1, eq-service ×5) — leave branch-deploy/deploy-preview/production untouched. This is the actual fix for SEC-9's confirmed leak pattern; re-storing as masked (already done) does not fix it.
3. **Re-verify eq-cards** once the Netlify tool stops declining the read, or check it directly via the Netlify dashboard.
4. **Delete the dead `SUPABASE_SERVICE_ROLE_KEY`** on eq-service pointing at the deleted `urjh` project — hygiene, not urgent.

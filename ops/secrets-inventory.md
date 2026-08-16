---
title: OPS — Secrets Inventory
owner: Royce Milmlow
last_updated: 2026-08-16
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

## The big picture: redundancy + importance

Added 2026-08-10, on Royce's ask to see this as one picture rather than a
per-site checklist. Two things below: which secrets are actually the *same*
value wearing different names across apps, and a tier for every real secret
ranking "what happens if this specific one leaks" — independent of whether
it currently is leaking.

### Confirmed shared values (one secret, multiple names/apps)

First 3 rows are stated as fact because a prior session's `getAllEnvVars`
read explicitly compared them and said so in plain English — not inferred
from name similarity. Full detail in `security-register.md` SEC-9/SEC-18.
Remaining 4 rows were confirmed 2026-08-16 by Royce directly — his own
words were "assume"/"no idea but assume same," not an independently
verified value comparison, so treat as high-confidence working assumptions
rather than the same rigor as the first 3.

| Real secret | Appears as | If it leaks |
|---|---|---|
| Shell's session-signing JWT secret | eq-shell `SUPABASE_JWT_SECRET` = eq-shell `EQ_SHELL_JWT_SECRET` = eq-service `EQ_SHELL_JWT_SECRET` | Forge a valid login session for **any** user, on any app in the suite — the top secret in the whole inventory. |
| SKS/ehow tenant JWT secret | eq-shell `SKS_SUPABASE_JWT_SECRET` = eq-field `SKS_JWT_SECRET` = eq-service `EQ_SERVICE_JWT_SECRET` | Forge a valid SKS-tenant session across Shell/Field/Service. |
| jvkn control-plane service_role key | eq-shell `SUPABASE_SERVICE_ROLE_KEY` = eq-cards `SUPABASE_SERVICE_ROLE_KEY` | Full read/write on the control-plane DB, bypasses every RLS policy — **SEC-9, closed 2026-08-16.** |
| ehow/sks-canonical service_role key | eq-service `CANONICAL_SERVICE_ROLE_KEY` = eq-field `CANONICAL_SERVICE_ROLE_KEY` = eq-field `EHOW_SERVICE_ROLE_KEY` = eq-shell `FIELD_SUPABASE_SERVICE_ROLE_KEY` | Full read/write on the ehow/sks-canonical DB behind Field + Service, bypasses every RLS policy. 4 names, 1 value — the most duplicated secret in the suite. Royce: never generated separate keys, it's the one default Supabase issued. |
| Platform admin key | eq-shell `EQ_PLATFORM_ADMIN_KEY` = eq-service `EQ_PLATFORM_ADMIN_KEY` | Admin-level access wherever this key is checked, on both apps that hold it. |
| Resend account key | `RESEND_API_KEY` on eq-shell, eq-field, eq-service, sks-nsw-labour | Sends transactional email on the EQ Resend account — spam/phishing risk, not data access. |
| Anthropic API key | `ANTHROPIC_API_KEY` on eq-shell, sks-nsw-labour | Runs up Royce's Claude API bill — sks-nsw-labour is frozen either way, low real exposure. |

### Suite-wide by design (not a bug, but worth a deliberate call)

`EQ_SECRET_SALT` is set — under the identical name — on **all five** apps
(eq-shell, eq-field, eq-service, eq-cards, sks-nsw-labour). `EQ_SESSION_SALT`
(eq-shell, eq-service, eq-cards — confirmed same-value 2026-08-16, Royce's
assumption, not independently checked) is the same pattern on 3 of them.
This is the exact pattern the PDF's rule 3 warns against ("reuse one master
key across every app 'for convenience'"). It may be intentional (a
suite-wide salt has a legitimate use case) — **decided 2026-08-16: keep
both shared for now**, no split planned unless raised again.

### Everything else, ranked by blast radius

Tier = what happens if *this specific secret* leaks, regardless of current
masking status. Tier 1 = suite-wide compromise. Tier 4 = low real stakes.

**Tier 1 — full compromise, suite-wide or DB-wide**

| Secret | App(s) | What it actually does |
|---|---|---|
| `GOOGLE_DOC_AI_CREDENTIALS` | eq-shell | Full Google Cloud service-account JSON (incl. private key) — direct GCP API access, not scoped to just this app. Register already calls this the most serious single item found. |
| `TENANT_ROUTING_MASTER_KEY` | eq-shell | Reads/writes the control-plane table that maps every tenant to its database — compromise here can redirect where any tenant's data actually goes. |
| *(plus the 3 confirmed-shared-value clusters above)* | | |

**Tier 2 — one app or one flow compromised, not the whole suite**

| Secret | App(s) | What it actually does |
|---|---|---|
| `EQ_SHELL_BRIDGE_SECRET` | eq-shell, eq-service | Authenticates the Shell↔Service session-bridge handoff. |
| `EQ_SERVICE_HANDOFF_KEY` | eq-shell, eq-service | Authenticates the Shell→Service iframe handoff specifically. |
| `EQ_QUOTES_HANDOFF_KEY` | eq-shell | Authenticates the (retired) Shell→Quotes handoff — candidate for deletion now Quotes is dead. |
| `EQ_FIELD_HANDOFF_KEY` | eq-field | Authenticates the Shell→Field iframe handoff — **SEC-18, still not masked.** |
| `CANONICAL_API_KEY_SERVICE` / `_FIELD` / `_SHELL` / `_QUOTES` | eq-shell | Per-consumer keys for pulling canonical (Shell-owned) data — one key per consuming app, the *correct* version of the pattern the salt/admin-key rows above get wrong. |
| `SITE_CREDENTIALS_KEY` | eq-service | Encrypts/authenticates stored third-party site credentials inside Service. |
| `LEAVE_CANONICAL_JWT_SECRET` | eq-field | Signs the token used for the Field↔canonical leave-request sync. |
| `ZAAP_JWT_SECRET` | eq-field | Session/token secret scoped to the zaap (EQ-tenant) canonical plane. |
| `AUDIT_SB_KEY` / `AUDIT_SB_URL` | eq-field | Credentials for the separate audit-log Supabase project. |

**Tier 3 — real cost if leaked, but bounded (account abuse, not a data breach)**

| Secret | App(s) | What it actually does |
|---|---|---|
| `RESEND_API_KEY` | eq-shell, eq-field, eq-service, sks-nsw-labour | Sends transactional email on the EQ Resend account — leak means spam/phishing sent as EQ, not data access. |
| `ANTHROPIC_API_KEY` | eq-shell, sks-nsw-labour | Anthropic API billing account — leak means someone runs up Royce's Claude API bill. |
| `TWILIO_AUTH_TOKEN` / `TWILIO_ACCOUNT_SID` | eq-shell | SMS sending (OTP, notifications) — leak means SMS sent/billed on Royce's account. |
| `GITHUB_TOKEN` | eq-service | CI/deploy-time GitHub access, scoped to this app's build. |
| `SENTRY_AUTH_TOKEN` | eq-service | Uploads source maps / manages Sentry config for this project only. |
| `SUPABASE_ACCESS_TOKEN` | eq-shell | Supabase *management*-API token used by `security_audit.py`'s advisor step — not a database key itself. |
| `QUOTES_CRON_SECRET` | eq-shell | Authenticates the Quotes-retirement cron calling Shell's own functions — **SEC-24, not masked.** |
| `CRON_SECRET` | eq-service | Same purpose as above, already correctly masked here. |
| `SCHEDULER_TEST_SECRET` | eq-shell | Test-only auth for a scheduler endpoint. |
| `UNSUBSCRIBE_SECRET` | eq-service | Signs one-click unsubscribe links so they can't be forged/enumerated. |
| `EQ_SERVICE_JWT_SECRET` / `EQ_SERVICE_API_KEY` | eq-service | Service's own signing secret / API key — **SEC-18, still not masked.** |

**Tier 4 — low stakes even leaked**

| Secret | App(s) | What it actually does |
|---|---|---|
| `EQ_SECRET_SALT` / `EQ_SESSION_SALT` | all apps | Hashing salts — strengthen other credentials, aren't independently exploitable on their own. |
| `VITE_SUPABASE_ANON_KEY` (all variants) | all apps | The public anon key — meant to be visible in the browser, RLS is the real gate. |
| `VITE_GOOGLE_MAPS_KEY` | eq-shell | Client-side, Google-domain-restricted by design. |
| `STAFF_CODE` / `MANAGER_CODE` | eq-field, sks-nsw-labour | Shared demo-tier access codes, confirmed genuinely different values per app — not a redundancy case. |

eq-cards was re-verified live 2026-08-16 (see its own section below) — full
7-var list, all previously-open items now closed. Not re-ranked into the
tables above because its only Tier 1/2 secrets are the two already covered
by the confirmed-shared-value cluster table; the rest are Tier 4 or n/a.

---

## eq-shell (`core.eq.solutions`, site `a3473f83-7c82-4f1e-872d-aa96eaa55172`)

| Secret name | Masked? | Where set | Notes |
|---|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | jvkn/eq-canonical service_role. **SEC-9 — closed.** |
| `EQ_SHELL_JWT_SECRET` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | Signs every session JWT suite-wide. **SEC-9 — closed.** |
| `CANONICAL_API_KEY_SERVICE` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | **SEC-9 — closed.** |
| `CANONICAL_API_KEY_FIELD` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | **SEC-9 — closed.** |
| `EQ_PLATFORM_ADMIN_KEY` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | **SEC-9 — closed.** |
| `EQ_SESSION_SALT` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | **SEC-9 — closed.** |
| `SKS_SUPABASE_JWT_SECRET` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | **SEC-9 — closed.** |
| `SUPABASE_JWT_SECRET` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | jvkn legacy JWT secret. **SEC-9 — closed.** |
| `EQ_QUOTES_HANDOFF_KEY` | **DELETED 2026-08-16** | — | Confirmed dead + retiring `mint-quotes-iframe-token.ts` call deliberately left to fail loud now instead of minting on a leaking secret. |
| `EQ_SERVICE_HANDOFF_KEY` | **DELETED 2026-08-16** | — | Confirmed no live caller in eq-shell or eq-service — dead code, not masked-and-kept. |
| `EQ_SHELL_BRIDGE_SECRET` | **DELETED 2026-08-16** | — | Confirmed no live caller — dead code, not masked-and-kept. |
| `QUOTES_CRON_SECRET` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | **SEC-24 — closed.** |
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
| `SKS_JWT_SECRET` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify (all contexts) | Same value as eq-shell's `SKS_SUPABASE_JWT_SECRET`. **SEC-9 — closed.** |
| `EQ_FIELD_HANDOFF_KEY` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | **SEC-18 — closed.** |
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
| `SUPABASE_SERVICE_ROLE_KEY` | **DELETED 2026-08-16** | — | Pointed at the deleted `urjh` project — dead var, no live use. The code-level fallback to it was separately removed in eq-solves-service PR #734 (open, not yet merged). |
| `EQ_PLATFORM_ADMIN_KEY` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify | **SEC-9 — closed.** |
| `EQ_SECRET_SALT` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify | **SEC-9 — closed.** |
| `EQ_SHELL_JWT_SECRET` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify | **SEC-9 — closed.** |
| `CANONICAL_API_KEY_SERVICE` | ✓ masked, `dev` cleared (fixed 2026-08-16) | Netlify | **SEC-9 — closed.** |
| `EQ_SERVICE_HANDOFF_KEY` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | **SEC-18 — closed.** |
| `EQ_SERVICE_JWT_SECRET` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | **SEC-18 — closed.** |
| `EQ_SERVICE_API_KEY` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | **SEC-18 — closed.** |
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

## eq-cards (`cards.eq.solutions`, site `c1bf4b4d-3131-4dd6-977f-2c0dd5cc4d72`) — re-verified 2026-08-16

Full live re-sweep via Netlify's `getEnvVars` API (the classifier that
blocked earlier attempts this month didn't trigger this pass). Found a
worse variant of SEC-9/SEC-18 that the 07-30 sweep missed: **`is_secret:
true` does not retroactively purge a value stored before the flag was
set.** `SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_JWT_SECRET` had been
"re-stored masked" in July and the flag was genuinely `true` — but the
per-context values underneath predated that toggle and were still
plaintext-readable via the API in **every context including production**,
not just `dev`. These are the two highest-tier secrets in the whole
inventory (jvkn service_role + the suite-wide session-signing secret), so
this was the most serious live finding of the 2026-08-16 sweep. Fixed the
same session via delete+recreate (the only reliable fix — a bare toggle
doesn't clear pre-existing values, on this site or any other row in this
file toggled the same way before today).

| Secret name | Masked? | Where set | Notes |
|---|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | jvkn control-plane service_role — same value as eq-shell's copy. Was plaintext-readable in every context incl. production until today. |
| `SUPABASE_JWT_SECRET` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | Suite-wide session-signing secret — the top secret in the whole inventory. Same leak, same fix. |
| `EQ_SESSION_SALT` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | Tier 4, low stakes, closed anyway. |
| `EQ_SECRET_SALT` | ✓ masked, all contexts (fixed 2026-08-16, delete+recreate) | Netlify | Suite-wide salt, same pattern. |
| `POSTHOG_API_KEY` | ✗ not flagged secret — correct as-is | Netlify (builds scope) | `phc_...` — PostHog's public project key, compiled into the client bundle via `--dart-define` (`scripts/netlify_build.sh`), same pattern as `SUPABASE_ANON_KEY`. Meant to be public. |
| `POSTHOG_HOST` | n/a | Netlify (builds scope) | URL, not a secret. |
| `SUPABASE_URL` | n/a | Netlify (builds scope) | URL, not a secret. |

## Other Netlify projects (checked, low/no risk)

`eq-receipts` — `VITE_SUPABASE_URL` (plain URL, not a secret) and
`VITE_SUPABASE_ANON_KEY` (`is_secret:true`, and an anon key is meant to be
public regardless) — no real secret. `sks-comms`, `eq-core-design`,
`knx-job-folder`, `life-tracking` — zero env vars configured, nothing to
expose (confirmed via SEC-18, not re-checked today, low-churn hobby
projects).

---

## Open actions

**Closed 2026-08-16** — full live walkthrough across all 4 Netlify sites:
SEC-9 (17 dev-context leaks: eq-shell ×11, eq-field ×1, eq-service ×5),
SEC-18 (eq-field/eq-service ×4 never-masked vars), SEC-24
(`QUOTES_CRON_SECRET`), the dead `SUPABASE_SERVICE_ROLE_KEY` on eq-service,
3 dead eq-shell vars deleted outright (`EQ_QUOTES_HANDOFF_KEY`,
`EQ_SERVICE_HANDOFF_KEY`, `EQ_SHELL_BRIDGE_SECRET`), and eq-cards'
previously-unverified site (found + closed a worse variant of SEC-9/18 in
the process — see eq-cards section above).

**Also closed 2026-08-16:** all 5 previously-suspected clusters confirmed
by Royce directly (ehow service_role key, platform admin key, Resend key,
`EQ_SESSION_SALT`, `ANTHROPIC_API_KEY`) — moved into the confirmed tables
above. His answers were "assume"/"no idea but assume same," not an
independently verified value comparison — high-confidence, not certain.

**Still open:**

1. **ProtonPass entry** for the real secrets that have no vendor source of
   truth — partial as of 2026-08-16, not complete. See the EQ Secrets Map
   artifact's master list for the full 35-row checklist.
2. **PR merge decisions** — eq-shell #1375, eq-solves-service #734+#732,
   eq-field #703, eq-cards #250 are all open, Royce's call, none merged.

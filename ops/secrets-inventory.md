---
title: OPS — Secrets Inventory
owner: Royce Milmlow
last_updated: 2026-08-11
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

These are stated as fact because a prior session's `getAllEnvVars` read
explicitly compared them and said so in plain English — not inferred from
name similarity. Full detail in `security-register.md` SEC-9/SEC-18.

| Real secret | Appears as | If it leaks |
|---|---|---|
| Shell's session-signing JWT secret | eq-shell `SUPABASE_JWT_SECRET` = eq-shell `EQ_SHELL_JWT_SECRET` = eq-service `EQ_SHELL_JWT_SECRET` | Forge a valid login session for **any** user, on any app in the suite — the top secret in the whole inventory. |
| SKS/ehow tenant JWT secret | eq-shell `SKS_SUPABASE_JWT_SECRET` = eq-field `SKS_JWT_SECRET` = eq-service `EQ_SERVICE_JWT_SECRET` | Forge a valid SKS-tenant session across Shell/Field/Service. |
| jvkn control-plane service_role key | eq-shell `SUPABASE_SERVICE_ROLE_KEY` = eq-cards `SUPABASE_SERVICE_ROLE_KEY` | Full read/write on the control-plane DB, bypasses every RLS policy — **SEC-9**, still open. |

### Suspected shared values — not yet confirmed, worth a value-suffix check

Same apparent purpose, same or near-same name, but nobody has explicitly
compared the actual values yet. Flagging rather than asserting, after this
file's own 2026-08-08 correction for guessing wrong once already.

**2026-08-11 — deliberately not verified via Netlify API.** A masked-suffix
comparison was scoped as a sprint task, then dropped before running it:
Netlify only returns a comparable value through the leaking `dev` context
(SEC-9) — the correctly-masked contexts (production/branch-deploy/
deploy-preview) come back as a literal `****`, no suffix, nothing to
compare. Any comparison read would therefore reproduce the exact
`dev`-context leak SEC-9 already logged twice, for a hygiene question, not
a security fix. Per SEC-9's own standing process fix ("future
credential-consumer mapping should be scoped to env-var names/presence
only, never fetch/print/decode actual values"), this needs Royce's own
answer instead — he set these values originally and can confirm
same-or-different in one line with zero exposure.

Also confirmed live this session: eq-cards' Netlify project is genuinely
live, not disconnected — git-triggered Netlify builds were turned off
2026-07-29 (PR #186), but GitHub Actions' `deploy.yml` zip-uploads the
Flutter web build to the same Netlify project via API, and its real
Netlify Functions (`shell-verify.js` etc.) still run there. So eq-cards'
env vars are live, in-use credentials, not orphaned — SEC-9/SEC-18's
eq-cards rows stand as written. The planned retry of eq-cards' env-var
read was dropped for the same reason as the cluster comparison above —
same leaking call, no new information it would actually buy.

| Suspected cluster | Appears as | Why suspected |
|---|---|---|
| ehow/sks-canonical service_role key | eq-service `CANONICAL_SERVICE_ROLE_KEY`, eq-field `CANONICAL_SERVICE_ROLE_KEY`, eq-field `EHOW_SERVICE_ROLE_KEY`, eq-shell `FIELD_SUPABASE_SERVICE_ROLE_KEY` | All four are named and positioned as "the ehow service_role key" and eq-field alone has *two* separately-named vars for what looks like one purpose. If confirmed, this is the single most duplicated secret in the suite — up to 4 names for 1 value. |
| Platform admin key | eq-shell `EQ_PLATFORM_ADMIN_KEY`, eq-service `EQ_PLATFORM_ADMIN_KEY` | Identical name, and an "admin key" is inherently one credential by definition — very likely one value, not independently confirmed. |
| Resend account key | `RESEND_API_KEY` on eq-shell, eq-field, eq-service, sks-nsw-labour | Same name on 4 sites. The PDF's own rule 3 ("prefer separate keys per app") suggests this *should* be 4 different keys — if it's actually 1 shared key, that's the redundancy finding; if genuinely 4 separate keys that happen to share a var name, no issue. |

### Suite-wide by design (not a bug, but worth a deliberate call)

`EQ_SECRET_SALT` is set — under the identical name — on **all five** apps
(eq-shell, eq-field, eq-service, eq-cards, sks-nsw-labour). This is the
exact pattern the PDF's rule 3 warns against ("reuse one master key across
every app 'for convenience'"). It may be intentional (a suite-wide salt has
a legitimate use case), but nobody has made that call explicitly — it's
just always been this way. Worth Royce deciding once: keep it shared, or
split it per-app next time any of these five get touched.

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

eq-cards is excluded from every table above except the confirmed-shared-value
one — its full var list hasn't been re-verified since 2026-07-30 (Netlify
tool declined the read twice this month), so ranking it would be guessing.

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

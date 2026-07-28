---
title: OPS — Security Register
owner: Royce Milmlow
last_updated: 2026-07-28
scope: Single tracked register of open security findings across the EQ/SKS Supabase surface — advisor output + live probes + known P0s. This is the ONLY security-register.md in the repo — a same-named file mentioned in eq/pending.md lives in a local scratchpad/ folder for an unrelated Trust-page/SOC2 draft, not tracked in git.
read_priority: critical
status: live
---

# Security Register

One place for every open security finding across the six Supabase projects.
Generated 2026-06-05 from live `get_advisors` + `scripts/rls_probe.py` +
`scripts/security_audit.py`, merged with the known P0 runbooks. Re-run those
tools to refresh; close items here as they're fixed.

**Gating:** `.github/workflows/security-audit.yml` runs the probe (no secret)
and the advisor audit (`SUPABASE_ACCESS_TOKEN` secret — not yet set) weekly +
on demand. The probe baselines known leaks (`rls_probe.py` `KNOWN_LEAKS`) so CI
fails on **new** exposure while keeping the open ones visible.

## Priority list

| ID | Severity | Finding | Project | Status |
|---|---|---|---|---|
| SEC-1 | **P0 — live PII leak** | Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` | sks-labour (LIVE — confirmed by Royce 2026-07-16 still active, retirement date NOT set) | **STILL OPEN, deliberately not engineered around.** **Reaffirmed 2026-07-20 (Royce): "SKS NSW Labour is not to be touched — we are keeping it going while we build Field."** Same standing decision as 2026-06-05 (below), restated after this session got as far as verifying live `pg_policies` and staging a Stage 2 RLS-hardening migration before being stopped — no engineering changes land on sks-nsw-labour, full stop, until Field replaces it. Fix stays decommission-at-cutover, not interim hardening. Nothing was written to `nspbmirochztcjijmcrx` or the sks-nsw-labour Netlify project this session — read-only verification only. |
| SEC-3 | **P3 — hygiene (downgraded from P0 2026-07-20)** | `ehowg` service_role key never rotated (F1) — **no confirmed leak vector found**, unrotated ≠ leaked | sks-canonical (LIVE) | **OPEN, hygiene priority.** Investigated 2026-07-20: the only evidence for "leaked" across the whole substrate is the key still being *valid* (unrotated since 2026-05-24) — no incident, no leak vector, no exposed-location ever documented. A **later, more careful analysis** (`cross-app-linkage-sprint-2026-06-07.md`) explicitly downgraded this: *"tenant_routing key concentration... No live exposure today; high cost if it leaks."* Corroborates the eq-field punch-list's own June note that the "exposed" flag looked stale. **Royce's call 2026-07-20: downgrade, rotate at a calm moment, not a rushed weekend window.** Rotation runbook (`f1-ehowg-key-rotation-runbook-2026-06-03.md`) still valid whenever it happens. |
| SEC-9 | **P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27** | A different service_role key (`jvkn`/eq-canonical) was pasted directly into a chat session 2026-07-12 to fix `canon-read` | eq-canonical (LIVE) | **OPEN.** Unlike SEC-3, this exposure IS confirmed — plaintext in a chat transcript is a real leak vector, not a hygiene item. **Royce's call 2026-07-20: same priority and rotation window as SEC-3** rather than treating separately. Rotate both together whenever that window lands. **2026-07-27: a consumer-mapping subagent (run to draft the missing rotation runbook — see below) was flagged by the Claude Code security classifier for "credential materialization" — it decoded a live jvkn service_role JWT's payload (role/ref claims) while searching Netlify env vars for consumers, and that decoded output is part of this session's tool-call record.** Not confirmed as a full second leak: a JWT payload is base64, not encrypted, and decoding it reveals only claims (`role: service_role`, `ref: jvkn...`) already described in plain English in this very row — that's materially different from the *encoded bearer token itself* (the three dot-joined segments that actually authenticate) appearing in output. The final summary I received back only showed masked fragments (`…wp9o`); I have no visibility into the subagent's own raw tool-call outputs to confirm whether the full token string appeared there too. Recorded honestly rather than assumed either way. **Process fix applied going forward:** any future credential-consumer mapping should be scoped to env-var *names/presence* only, never fetch/print/decode actual values. |
| SEC-10 | **P0 — confirmed exposure** | `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is_secret: false` — not masked in Netlify's own UI/API either), full values returned by a routine env-var read 2026-07-20 and now sitting in a chat transcript, same leak-vector class as SEC-9 | sks-nsw-labour (Netlify, LIVE) | **OPEN.** Found by accident while prepping SEC-1's JWT-minter env vars (that prep is now moot — see SEC-1, app is not being touched). Credential storage, not app config — **technically not covered by the "don't touch sks-nsw-labour" freeze**, but rotation itself is a separate action requiring your own console.anthropic.com / resend.com access. `EQ_SECRET_SALT`'s `dev`-context value came back unmasked too (its `production`/`branch-deploy`/`deploy-preview` values are correctly masked — only `dev` isn't). **Royce's call 2026-07-20: rotate at another time.** **2026-07-27: in practice, Royce declined to touch this site at all** ("I'm not touching sks-nsw-labour") when offered the same-value re-mask alongside SEC-12 — so this stays open under the broader freeze in practice, regardless of the technical distinction drawn above. Live-verified 2026-07-27: `ANTHROPIC_API_KEY`/`RESEND_API_KEY` still `is_secret: false`, unchanged since April; `EQ_SECRET_SALT`'s `dev` context still plaintext. When eventually done: set the new values with `is_secret: true`, closing the plaintext-storage gap too, and re-check whether any other project has the same pattern on a real credential. |
| SEC-2 | ~~P1~~ **CLOSED** | RLS policy `tenant_isolation` trusts end-user-editable `user_metadata` (advisor ERROR) | eq-canonical-internal | **CLOSED 2026-07-21 — was already fixed, register was stale.** See Detail. |
| SEC-4 | P3 — hardening | `anon`-executable SECURITY DEFINER `eq_cards_*` fns | eq-canonical | **VERIFIED not exploitable** 2026-06-05 (auth.uid()/token-guarded). Post-launch: revoke anon EXECUTE on the 3 that don't need it. |
| SEC-5 | P3 — hygiene | always-true (`USING/WITH CHECK = true`) write policies | eq-solves-field, eq-canonical-internal | **VERIFIED latent** 2026-06-05 — anon holds NO table grant, policies unreachable. Post-launch cleanup. |
| SEC-6 | P2 | `context_proposals` anon INSERT has length caps but no volume throttle | eq-substrate | OPEN — needed before the queue has a consumer |
| SEC-7 | P3 | `function_search_path_mutable` (search_path not pinned) | several projects | OPEN — hygiene, fix at next touch |
| SEC-8 | P3 | `pg_net` extension installed in `public` schema | sks-labour | OPEN — moot once sks-labour retired |
| SEC-11 | **P3 — accepted, docs corrected (downgraded from P1 2026-07-23)** | `tenant-migrate.yml`'s `production` GitHub Environment has **zero protection rules** (`protection_rules: []`, confirmed via `gh api repos/eq-solutions/eq-shell/environments/production` 2026-07-23) despite the workflow's own header comment and prior session memory both asserting "gated behind the `production` Environment so it PAUSES for a human approve click... `production` environment with Royce as required reviewer — CREATED 2026-06-03." | eq-shell (GitHub Actions/repo config) | **ACCEPTED, not fixing — Royce's call 2026-07-23.** Found live: dispatched `tenant-migrate.yml` (migration 0199, whole fleet) on Royce's "dispatch tenant-migrate.yml" — the `Apply to all tenants` job ran straight through in ~15s with no approval pause, applying live DDL to both zaap and ehow. Attempted the fix (`gh api --method PUT .../environments/production` with Royce/`Milmlow` id `271704382` as required reviewer) — **rejected, HTTP 422: "Please ensure the billing plan supports the required reviewers protection rule."** Required-reviewer environment protection needs GitHub Team/Enterprise Cloud (or a public repo); this private repo doesn't have it. Royce's call: don't pay for the plan upgrade — `Milmlow` is the only repo collaborator with dispatch access anyway (confirmed via `gh api repos/.../collaborators` — one entry), so a reviewer gate would only ever be "Royce clicks twice," not a real access boundary. **Fixed instead:** corrected the false claim in `tenant-migrate.yml`'s header + inline comments (PR [#985](https://github.com/eq-solutions/eq-shell/pull/985), OPEN) so nobody trusts a safety net that isn't there. Real safeguard going forward: deliberate manual dispatch only, no second-click gate. |
| SEC-12 | ~~P0~~ **CLOSED 2026-07-27** | Several real secrets on **eq-shell's own** Netlify project stored with `is_secret: false` — full plaintext returned on any routine env-var read/API call, unmasked in Netlify's own UI | eq-shell (Netlify, LIVE, site `a3473f83-7c82-4f1e-872d-aa96eaa55172`, core.eq.solutions) | **CLOSED 2026-07-27 — Royce re-stored all 8 himself, live-verified.** `getAllEnvVars` re-checked directly: `GOOGLE_DOC_AI_CREDENTIALS`, `EQ_PLATFORM_ADMIN_KEY`, `EQ_SHELL_JWT_SECRET`, `SKS_SUPABASE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`, `EQ_QUOTES_HANDOFF_KEY`, `CANONICAL_API_KEY_FIELD`, `EQ_SESSION_SALT` all now `is_secret: true`, all timestamped 2026-07-27T06:57–07:02Z. Same-value re-store confirmed, not a rotation — both eq-shell and sks-nsw-labour deploys checked `ready` immediately after, no outage. Original finding detail below, retained for history. Was: **OPEN.** Found 2026-07-26 during the SKS NSW onboarding security review, while checking `ENFORCE_IFRAME_ORIGIN` (confirmed separately: set to `true` in production — SEC-11-adjacent CSRF gap is enforced, not a hole). A `getAllEnvVars` read surfaced, all currently `is_secret: false`: `GOOGLE_DOC_AI_CREDENTIALS` (full Google service-account JSON incl. RSA private key, production context — **the most serious of the set**, grants direct GCP API access if leaked), `EQ_PLATFORM_ADMIN_KEY`, `EQ_SHELL_JWT_SECRET`, `SKS_SUPABASE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`, `EQ_QUOTES_HANDOFF_KEY`, `CANONICAL_API_KEY_FIELD`, `EQ_SESSION_SALT` — all identical plaintext value across every context (dev/branch-deploy/deploy-preview/production) except `GOOGLE_DOC_AI_CREDENTIALS` (production only). Do not confuse `EQ_SESSION_SALT` (this finding) with `EQ_SECRET_SALT` (a distinct, similarly-named var already correctly `is_secret: true` on this same site). **Remediation attempted, blocked by design:** a same-value re-store (upsert with `envVarIsSecret: true`, no rotation) via the Netlify MCP was **blocked by the Claude Code safety classifier** as "modifying security settings" — this is a manual-hands-only fix, not something any Claude Code session can complete regardless of explicit permission. **Royce must do this himself** via the Netlify dashboard (Site settings → Environment variables → per key: note the current value, delete, recreate with the identical value, tick "contains sensitive values" this time) or the Netlify CLI. Same-value re-store, not rotation — changing any value breaks live signing (in-flight JWTs, handoff tokens) immediately. Rotation is a separate, larger decision (mirrors the SEC-9/SEC-3 "rotate whenever convenient" pattern) — not needed just to close the plaintext-storage gap. |
| SEC-13 | ~~P2~~ **CLOSED 2026-07-27** | Same public-schema default-grant footgun as SEC-4, never previously audited on the tenant data planes — 39 anon-executable SECURITY DEFINER functions on zaap (12 on ehow, exact subset), the Ops/Quotes RPC surface | eq-canonical-internal (EQ tenant, zaap) + sks-canonical (SKS tenant, ehow) | **CLOSED same session — found, fixed, and live-verified.** See Detail. |
| SEC-14 | **P3 — accepted, docs corrected (same class as SEC-11, different repo)** | `apply-service-migrations.yml`'s `production` GitHub Environment has no required-reviewer rule (`protection_rules` branch-policy only, confirmed via `gh api repos/eq-solutions/eq-service/environments/production` 2026-07-28) despite the workflow's own header comment asserting it "PAUSES for a human approve click before any live DDL." | eq-service (GitHub Actions/repo config) | **ACCEPTED, not fixing — same reasoning as SEC-11.** Found live: dispatched `apply-service-migrations.yml` on Royce's "go ahead" for PR #619's 2 reconciled migrations — the `Apply to ehow` job ran straight through in 18s with no approval pause, applying both to live ehow. No harm done (the SQL was already dry-run verified safe in a rolled-back transaction before merge). Same root cause as SEC-11: required-reviewer environment protection needs GitHub Team/Enterprise Cloud or a public repo; this private repo has neither. `Milmlow` is the only repo collaborator with dispatch access (confirmed via `gh api repos/.../collaborators` — one entry), so a reviewer gate would only ever be "click twice," not a real access boundary — not paying for a plan upgrade. **Fixed instead:** corrected the false claim in `apply-service-migrations.yml`'s header comment (PR [#620](https://github.com/eq-solutions/eq-service/pull/620)) so nobody trusts a safety net that isn't there. **Wider sweep done 2026-07-28:** checked all 14 org repos (`gh search code "environment:" --filename ".yml"` per repo + `gh repo list` to confirm none were missed) for any other environment-gated workflow. Found exactly one more cluster: eq-context's 7 backup/verify/restore-drill workflows, all on a `production-ops` environment with the same branch-policy-only protection (confirmed via `gh api repos/eq-solutions/eq-context/environments/production-ops`) — but their own comments already say so accurately ("NO required reviewers... never paused waiting for an approval"), no false claim there. No other repo uses environment gating at all. This class of finding is now closed as fully swept, not just the two instances found by accident. |
| SEC-15 | ~~P2~~ **CLOSED 2026-07-28 (same class as SEC-13)** | `public.rls_introspection()` — ad-hoc SECURITY DEFINER diagnostic dumping every `public`/`service` table's RLS state + every policy's full qual/with_check, no tenant scoping — found live with EXECUTE granted to `anon`+`authenticated`. No migration file, no `_eq_migrations` ledger row, no caller anywhere in the codebase: created out-of-band, same root cause as SEC-13 (a fresh instance appearing *after* SEC-13 seeded the sks-canonical baseline to empty, i.e. the drift gate catching a new violation exactly as designed, not a gap in that fix). Root cause traced separately: eq-service's own migration `0192` had recreated the function with `REVOKE ALL FROM PUBLIC` only, dropping the explicit `anon, authenticated` naming an earlier migration required — ehow's `public`-schema default privileges (which only ever covered tables, never functions, in the 2026-06-07 lockdown) auto-granted EXECUTE back on the fresh `CREATE`. | sks-canonical (ehow) — confirmed absent on zaap (EQ tenant), ehow-only | **CLOSED — two sessions independently fixed the identical live exposure via two separate governed pipelines, ~85s apart, no conflict (both idempotent REVOKE/GRANT):** eq-shell [#1061](https://github.com/eq-solutions/eq-shell/pull/1061) (`0219_revoke_anon_rls_introspection.sql` via `tenant-migrate.yml`, dispatch run 30334947428, merged as `a950bbe1`) and eq-service [#622](https://github.com/eq-solutions/eq-service/pull/622) (`0194_revoke_rls_introspection_anon_grant.sql` via `apply-service-migrations.yml`, merged as `619dd5e6`). Both merged and live-reverified: `has_function_privilege('anon', 'public.rls_introspection()', 'EXECUTE')` now `false`, `service_role` still `true`. Not added to `FUNC_EXEC_ANON_ALLOW` — correctly locked to service_role, no anon use case (SQL-console/ops-script diagnostic only). Real cost was duplicate engineering effort across two repos, not a live risk. **Open, not closed here — see SEC-16, CLOSED 2026-07-28.** |
| SEC-16 | ~~P2~~ **CLOSED 2026-07-28** | Root cause behind SEC-4/SEC-13/SEC-15 recurring three times: nothing stopped a brand-new SECURITY DEFINER function from being born anon-executable. `ALTER DEFAULT PRIVILEGES ... ON FUNCTIONS ... REVOKE FROM PUBLIC` (mirroring the 2026-06-07 table lockdown) does not work on this platform — see the "SEC-15 — root-cause investigation" writeup below for the full 3-line-of-evidence diagnosis (Postgres' own `acldefault('f', ...)` includes `PUBLIC`; Supabase's own docs confirm new functions get `anon`/`authenticated`/`service_role` granted by default; empirically reproduced on both ehow and zaap). | jvkn (control), zaap (EQ tenant), ehow (SKS tenant) — all three | **CLOSED — a working mechanism exists after all, just not a "setting": a `ddl_command_end` event trigger** (`eq_enforce_function_privacy`), re-asserting `REVOKE ALL FROM PUBLIC, anon, authenticated; GRANT EXECUTE TO service_role` on every function landing in a guarded schema (`public`+`service` on zaap/ehow, `public`+`shell_control` on jvkn) immediately after creation. Verified compatible with an explicit follow-up `GRANT` for a legitimate anon/authenticated RPC (the trigger fires on the `CREATE`/`ALTER FUNCTION` command itself; a later `GRANT` is a separate command, unaffected). Each guard runs in its own exception handler — a bug here can only skip one function, never block an unrelated migration. eq-shell [#1070](https://github.com/eq-solutions/eq-shell/pull/1070) (tenant migration `0220`, applied via `tenant-migrate.yml` to zaap+ehow, dispatch run 30337989873) + control-plane migration applied to jvkn via Supabase MCP, ledgered in `CONTROL-PLANE-LEDGER.md` (eq-shell [#1072](https://github.com/eq-solutions/eq-shell/pull/1072)). Live-verified on all three planes post-apply with a real (non-transactional) test function each: `anon=false`, `service_role=true`. **Corrects the "SEC-15 — root-cause investigation" conclusion below** ("there is no available setting that prevents this at creation time") — true for settings/default-privileges specifically, but an event trigger is a different mechanism and does work. |

## Weekend tasks (Field go-live + cutover)

- **SEC-1 — decommission SKS Labour.** Field replaces it; once Field is live, take
  SKS Labour offline / pause project `nspbmirochztcjijmcrx` / disable its anon
  access so the PII leak can't outlive the app. **Explicit checklist line — not
  assumed.** Remove from `rls_probe.py KNOWN_LEAKS` once done. Still blocked on
  an actual retirement date — sks-nsw-labour confirmed still active 2026-07-16,
  no date set. **Reaffirmed 2026-07-20: no interim hardening either** — the app
  stays untouched, not just unretired, until Field replaces it.

  **Decommission checklist (drafted 2026-07-26, no date set — gates not yet met):**
  Full cutover mechanics are `SKS-CUTOVER-CRITICAL-PATH.md` Phase E; this is the
  narrower "is it actually safe to set a date" gate, checked live before writing
  anything actionable:
  1. ☐ **Proving run hits its stop condition** — `SKS-FIELD-PARALLEL-RUN-LOG.md`'s
     own rule: 3-4 *consecutive* clean weeks of parallel roster+timesheet entry.
     **Current streak: 0 — not yet started** (verified live 2026-07-26; the
     2026-07-11-decided run never got sustained, real entry activity had dropped
     to ~1 audit-log action/14 days before this log restarted it). A dirty week
     resets the counter to zero, not just pauses it.
  2. ☐ **VIC scale-jump question resolved** — the NSW proof is sized at ~300
     users; VIC's next expansion is already ~700-1,000, a materially bigger jump
     than anything NSW will have proven. Open, undecided (`eq/pending.md`).
  3. ☐ **Rollout sign-off owner named** — "who signs off on a cutover this size"
     is still unanswered (Royce, 2026-07-23: "no idea about sign-off yet").
  4. ☐ **The 44 SKS workers still on the standalone app get an actual migration
     date**, not just a count — 48 already cut over as of 2026-06-06 per
     `eq/pending.md`, but the remaining 44 have no plan attached, only a tally.
  5. ✅ **EQ Field's two live untriaged errors — FIXED 2026-07-27, v3.5.358
     (eq-field [PR #542](https://github.com/eq-solutions/eq-field/pull/542),
     squash `ee0767c`), live on field.eq.solutions.** `SyntaxError: Identifier
     'INCIDENT_TYPES' has already been declared` (Sentry 136548558) was a
     duplicate top-level `const INCIDENT_TYPES` in both `scripts/diary.js` and
     `scripts/incidents.js` (Incidents/Near-Miss, shipped 2026-07-22) —
     classic-script lazy-loading shares one global scope, so whichever loaded
     second threw at parse time and aborted the module. Renamed diary.js's to
     `DIARY_INCIDENT_TYPES`. `ReferenceError: openLeaveRequest is not defined`
     (Sentry 130706295) was a lazy-load race: `showPage()` unhides the Leave
     page before its async `leave.js` lazy-load resolves, so a fast click on
     "+ New Request" could fire before the function existed — added
     `openLeaveRequestSafe()`, reusing the existing dashboard-strip lazy-load
     guard pattern. Verified `node --check` clean on both touched scripts, plus
     real browser loads (both script orderings, and the exact leave-button
     race) on both `serve` and the live Netlify deploy preview — zero errors.
  6. ☐ Once 1-5 are clear: set the actual retirement date, then run Phase E's
     mechanical steps (repoint SKS Field surface → parallel-run/soak → take
     `nspbmirochztcjijmcrx` offline → disable its anon key → strike SEC-1 from
     `rls_probe.py KNOWN_LEAKS`).

  **Bottom line (2026-07-26): premature to set a date today.** Gate 1 alone
  (0/3-4 clean weeks) rules it out regardless of the other four.
- ~~SEC-2 — fix `eq_intake_rate_limits` RLS.~~ **Already done — closed 2026-07-21, see Detail.**

## Rotate whenever convenient (not weekend-critical, per Royce's 2026-07-20 call)

- **SEC-9 — rotate the jvkn (eq-canonical) service_role key first or alongside SEC-3.** Confirmed exposure (pasted into a chat transcript 2026-07-12). No runbook exists yet — write one before rotating (mirror the SEC-3/F1 runbook's staged pattern: new key → propagate to consumers → disable legacy).
- **SEC-3 — F1 key rotation.** Per `f1-ehowg-key-rotation-runbook-2026-06-03.md`. Downgraded 2026-07-20 (no confirmed leak, hygiene priority) — do this at a calm moment, not a rushed weekend window. Staged: new key → propagate to Quotes Fly secret + re-encrypt `tenant_routing` → disable legacy → re-test legacy GET = 401. Do NOT disable legacy before both consumers hold the new key.

## Post-launch hardening (after the freeze)

- **SEC-4** — `REVOKE EXECUTE ... FROM anon` on `eq_cards_claim_invite`,
  `eq_cards_delete_account`, `eq_cards_get_worker_hr_record` (keep `preview_invite`
  anon — it's the pre-auth invite preview). Confirm the Cards client calls
  claim/delete post-auth first.
- **SEC-5** — drop the always-true `anon`/`public` write policies on
  eq-solves-field + eq-canonical-internal and replace with tenant/owner-scoped
  ones. Latent today (no grants) but a single stray `GRANT` would arm them.

## Detail

### SEC-1 — sks-labour public key reads staff PII (P0, LIVE)
`scripts/rls_probe.py` 2026-06-05: a `GET` with the **public** publishable key
returned rows from `public.people`, `public.timesheets`, `public.leave_requests`,
and `public.audit_log` (5,752 rows). The anon key ships in the SKS Labour
browser app, so anyone who extracts it can read staff personal data. Root cause:
SKS Labour is the pre-canonical anon-model app.
**Decision 2026-06-05 (Royce):** EQ Field replaces SKS Labour at this weekend's
go-live → do **not** invest in RLS-hardening a retiring app. **Fix = decommission
at cutover:** take SKS Labour offline / pause project `nspbmirochztcjijmcrx` /
disable its anon key. ⚠️ The leak is **live until the old app is actually off** —
a "redundant but still running" app is a classic forgotten exposure. Make this an
explicit cutover checklist line. Remove from `rls_probe.py KNOWN_LEAKS` once done.

**Note 2026-06-27:** sks-labour was dropped from the automated EQ gate —
`rls_probe.py` is now EQ-only (the gate is EQ-focused, and the local tooling
blocks probing the SKS-live project). This did **not** resolve SEC-1: the leak is
live until SKS Labour is decommissioned. SEC-1 is now tracked **manually** here,
not by CI — a green gate no longer implies SEC-1 is closed. Close it when the app
is actually off.

**Note 2026-07-20:** a session got as far as re-verifying live `pg_policies`,
confirming the `sks` org id, and staging a Stage 2 RLS-hardening migration
(additive `authenticated` policies alongside the existing `anon` ones) before
Royce stopped it: *"SKS NSW Labour is not to be touched — we are keeping it
going while we build Field."* This restates, not reverses, the 2026-06-05
decision above — worth recording explicitly since an earlier prompt this same
session had framed it as an open choice between "harden now" and "accept
pending retirement," which wasn't the real choice on offer. Nothing was
applied — no SQL ran, no env var changed, PR #34 (dark Stage-1 minter) is
still open/unmerged on `sks-nsw-labour` and should stay that way. The 4
draft SQL/runbook files in `~/.claude/plans/nspbmir-*` remain exactly that:
drafts, not a queued plan.

### SEC-2 — eq-canonical-internal RLS trusts user_metadata (CLOSED 2026-07-21)
Originally: `app_data.eq_intake_rate_limits` policy `tenant_isolation` referenced
`auth.user_metadata`, which end users can edit — a forgeable-tenant bypass.

**Closed, not fixed this session — it turned out to already be fixed.** Asked to
action this finding 2026-07-21; live-verified via `pg_policies` on both tenant
planes (zaap `eq-canonical-internal` and ehow `sks-canonical`) before touching
anything, per this repo's own Rule 0.5 (verify live before building). Both
`app_data.eq_intake_rate_limits` **and** `app_data.api_intake_calls` already key
`tenant_isolation` on `app_metadata`, not `user_metadata`, on both planes.
Traced to eq-shell's canonical `supabase/tenant-migrations/0023_intake_infra.sql`
(the original SKS→canonical port — header literally says "corrected from SKS's
user_metadata") plus `0178_intake_rate_limit_harden.sql` (a later
source-reconciliation that also pinned `search_path` on the two rate-limit
definer RPCs and wrapped the claim in `(SELECT …)` for planner caching). This
register and `security_audit.py`'s `ACCEPTED_ERRORS` were simply never updated
after those migrations shipped — the finding had been stale since whenever 0023
first went live. `ACCEPTED_ERRORS` entry removed same session. eq-intake's own
`sql/029_rate_limiting.sql` + `sql/032_api_audit_log.sql` (pre-port staging
copies, never self-serve applyable — see that repo's CLAUDE.md) still show the
superseded `user_metadata` version; annotated with a pointer to the real fix
rather than rewritten, since they're an intentional historical record of what
was ported *from*.

### SEC-3 — F1: exposed ehowg service_role key still live (P0)
Full runbook: `f1-ehowg-key-rotation-runbook-2026-06-03.md`. The leaked
sks-canonical service_role key is still valid. Rotate the JWT secret / disable
the legacy key — but only after propagating the new key to BOTH consumers
(Quotes Fly secret + `tenant_routing` re-encrypt), or live Quotes + canonical
routing break. Royce-gated.

### SEC-4 — anon-executable SECURITY DEFINER functions (P3, VERIFIED not exploitable)
eq-canonical exposes 4 `eq_cards_*` functions to anon as SECURITY DEFINER.
**Verified 2026-06-05 (read `pg_proc.prosrc`):** all are safe for an anon caller —
`get_worker_hr_record`, `claim_invite`, `delete_account` all filter/act on
`auth.uid()`, which is NULL for anon (so `user_id = auth.uid()` matches **zero
rows** and updates touch nothing); `preview_invite` is gated by a secret invite
token (intended pre-auth preview). No live data/mutation path for anon. **Action
(post-launch hygiene):** `REVOKE EXECUTE FROM anon` on the three that have no
anon use case (keep `preview_invite`), after confirming the Cards client calls
claim/delete while authenticated.

### SEC-5 — always-true write-RLS policies (P3, VERIFIED latent)
`rls_policy_always_true` on many tables in eq-solves-field and
eq-canonical-internal (and sks-labour). **Verified 2026-06-05
(`has_table_privilege`):** on both EQ DBs, `anon` holds **no** SELECT/INSERT/
UPDATE/DELETE grant on people, timesheets, leave_requests, sites, projects,
schedule, audit_log — so the always-true `anon`/`public` policies are
**unreachable** (PostgREST 401s before RLS). Not an active hole; the probe
confirms anon reads = 401/empty on these. **Risk:** a single stray `GRANT ... TO
anon` would instantly arm every always-true policy. **Action (post-launch):**
drop the always-true policies and replace with tenant/owner-scoped ones so the
table can never leak even if a grant is added.

### SEC-13 — anon-executable SECURITY DEFINER functions on tenant data planes (CLOSED 2026-07-27)
Same class of bug as SEC-4 (Supabase grants `EXECUTE` to `anon`+`authenticated`
explicitly at `CREATE FUNCTION` time in the `public` schema — a separate
mechanism from the `PUBLIC` pseudo-role; `REVOKE ... FROM PUBLIC` alone does
not remove it), but SEC-4 only ever covered the control plane (jvkn). The
tenant data planes (zaap/ehow) had never been checked for this — the drift
gate's function-EXECUTE invariant (`scripts/check-tenant-drift.mjs`) had a
maintained `FUNC_EXEC_ANON_ALLOW` baseline for jvkn only; zaap/ehow reported
"no allow-list baseline — seed to enforce" and were silently unaudited by CI.

**Found while investigating an unrelated finding same session:** an eq-shell
PR's CI run surfaced `my_admin_org_ids()` (jvkn) anon-executable, fixed via
eq-cards PR #180 + migration `0107_lock_my_admin_org_ids_exec.sql`. That
prompted a direct SQL audit of the two tenant planes, which had never had
this check run against them at all.

**Verification method:** read every function body, not assumed from names.
Live-queried `has_function_privilege('anon', ..., 'EXECUTE')` against both
planes immediately before writing the fix (not the earlier triage snapshot).
37 of the 39 zaap functions (12 of ehow) derive tenant scope from the
caller's JWT (`current_setting('request.jwt.claims', true)` / `auth.jwt()` →
`tenant_id`, both NULL for an anonymous caller) and fail closed — an anon
call reads zero rows or hits an explicit `RAISE EXCEPTION`. Real
exploitability was low; this was a defense-in-depth close, not a live
breach.

**Two confirmed legitimate exceptions**, left untouched: `eq_get_portal_quote(text)`
/ `eq_respond_portal_quote(text,text,text,text)` — the customer-facing quote
portal, gated by an unguessable share token
(`app_data.quote_share_links.token = p_token AND is_active`), not auth. An
external customer clicks an emailed link and never logs into EQ Shell.

**A separate, distinct governance-drift finding surfaced in the same audit:**
`eq_mark_expired_quotes()` (zero-arg cron sweep, no tenant filter) had
already been correctly migrated to `service_role`-only twice
(`0099_quote_expiry_rpc.sql`, `0111_eq_mark_expired_quotes_v2.sql`), both
confirmed applied in `app_data._eq_migrations` on zaap (2026-06-15
08:12:57/08:13:19 UTC) — yet live grants still showed `anon` holding
`EXECUTE` before this fix, with no later migration touching the function
again. Most likely an out-of-band change outside the One Pipe sometime after
2026-06-15 — the **mechanism/actor is unidentified**, only the drift itself
is confirmed and re-closed. Worth keeping in mind as a precedent: a
correctly-migrated function is not guaranteed to stay fixed without the CI
baseline described below.

**Fix:** eq-shell `supabase/tenant-migrations/0211_close_anon_exec_gap_ops_quotes_rpcs.sql`
(the 39/12-function REVOKE+re-GRANT, tolerant of ehow's smaller subset via
`EXCEPTION WHEN undefined_function`) + `0212_fix_eq_update_customer_anon_exec_signature.sql`
(0211's own signature list had 10 args for `eq_update_customer`; the real
function takes 11 — the exception handler swallowed the mismatch silently on
both planes, caught by live re-verification immediately after 0211 applied,
exactly the risk flagged before building). PR
[#1028](https://github.com/eq-solutions/eq-shell/pull/1028), merged and
dispatched to both zaap and ehow via `tenant-migrate.yml` same session.
Live-reverified after both migrations: zaap holds only the 2 portal
functions anon-executable, ehow holds zero.

**Also seeds `FUNC_EXEC_ANON_ALLOW` baselines for both tenant planes** in
`check-tenant-drift.mjs` (`eq-canonical-internal (EQ tenant)`: the 2 portal
signatures; `sks-canonical (SKS tenant)`: empty set) — the drift gate now
actually enforces this class of bug on the tenant planes going forward
instead of reporting "no baseline." Confirmed: PR #1028's drift-gate check
initially failed post-migration-draft (live state hadn't caught up yet),
then passed clean after the migrations were dispatched — same
dispatch-before-merge sequencing as SEC-11's workflow.

**Related, still open:** SEC-4 (jvkn, the original 4-function instance of
this same footgun) remains unfixed — "VERIFIED not exploitable," never
revoked. This session's three fixes of the identical pattern
(`my_admin_org_ids`, the zaap 39, the ehow 12), all applied with zero
incidents, are a working precedent for finally closing SEC-4 too. Not
actioned this session — flagged here, not fixed, since it wasn't the
task in hand.

### SEC-15 — root-cause investigation: why `ALTER DEFAULT PRIVILEGES` can't prevent this recurring (2026-07-28)
Follow-up to SEC-15's close: Royce approved (`/decide` pass) building a plane-wide
`ALTER DEFAULT PRIVILEGES ... REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC` on
ehow/zaap/jvkn to stop this exact class of bug (SEC-4/13/15) recurring a
fourth time. **Live-tested in a rolled-back transaction on ehow before
committing anything (Rule 0.5) — it's a no-op.** The `pg_default_acl` catalog
row updates correctly (confirmed via direct `SELECT`), but a freshly
`CREATE FUNCTION`'d function's real ACL still carries `PUBLIC=EXECUTE` and
`anon`/`authenticated` can still call it. No migration was shipped.

**Root cause, confirmed via 3 independent lines of evidence:**
1. Postgres' own compiled-in default differs by object type — queried
   `acldefault('f', 'postgres')` → `{=X/postgres, postgres=X/postgres}`
   (bare `=` = `PUBLIC`) vs. `acldefault('r', 'postgres')` (tables) →
   `{postgres=arwdDxtm/postgres}`, no `PUBLIC` entry at all. **New functions
   get `PUBLIC EXECUTE` by default in vanilla Postgres; new tables get
   nothing** — exactly why the 2026-06-07 table lockdown worked cleanly and
   has no function-side equivalent that behaves the same way.
2. Supabase's own docs (fetched via the Supabase MCP's `search_docs`,
   lint `0028_anon_security_definer_function_executable`) state it
   explicitly: *"Postgres' default function ACL is EXECUTE to PUBLIC, and
   Supabase additionally grants default privileges for new functions to
   anon, authenticated, service_role."* Stated as platform behavior, not a
   per-project misconfiguration.
3. Empirically reproduced the failure 3 ways on ehow (plain schema, a
   fresh scratch schema created solely for the test, and with an explicit
   companion `GRANT ... TO service_role` to force a non-null ACL — all
   still leaked `PUBLIC`) and confirmed it's not ehow-specific by running
   the identical test against zaap (EQ tenant) — same result. Ruled out the
   obvious visible mechanisms first: `cron.job` has 4 unrelated jobs (none
   touch grants), and all 4 SQL-level `ddl_command_end` event triggers
   (`pg_get_functiondef`'d directly) only fire for `pg_cron`/`pg_net`/
   `pg_graphql` extension installation, not general `CREATE FUNCTION`.
   `session_preload_libraries` = `supautils` — Supabase's own closed-source
   platform-policy extension (its GUC settings show it already enforces
   `policy_grants`/`drop_trigger_grants`/`reserved_roles` for the same kind
   of platform-wide policy) — the most likely actual enforcement point, but
   its C source isn't inspectable, so this is inference from behavior +
   docs, not a read of the mechanism itself.

**Conclusion: there is no available setting that prevents this at creation
time on this platform.** The only thing that reliably works is what
SEC-4/13/15 already did — an explicit `REVOKE`/`GRANT` run directly on the
function *after* it's created (verified clean: `rls_introspection()`'s own
ACL is `{postgres=X, service_role=X}`, no `PUBLIC`, because it was fixed
this way). **The drift gate catching each new instance same-day (3-for-3
so far) isn't a stopgap for a better fix — it is the permanent mitigation
here.** Nothing shipped; the draft migration file was written, tested, and
deleted without committing. `ops/pending.md`'s "rls_introspection()
anon-EXECUTE leak" entry has the same writeup.

**Update, same day (SEC-16, CLOSED):** the conclusion above is correct that no
*default-privilege setting* prevents this — but a different mechanism does.
A `ddl_command_end` event trigger (`eq_enforce_function_privacy`), which
re-runs the same explicit REVOKE/GRANT idiom immediately after every
`CREATE`/`ALTER FUNCTION` in the guarded schemas, was built, live-tested
(compatible with legitimate anon-callable RPCs' own follow-up `GRANT`), and
shipped to all three planes. See SEC-16 for the full detail — the drift gate
is no longer the only mitigation, this closes the door at creation time.

### SEC-6 — context_proposals volume throttle (P2)
Length caps applied (migration `context_proposals`), but anon can still insert
many small rows. Add a per-session/IP throttle (edge function) before the queue
gets a consumer, or restrict INSERT to authenticated.

### SEC-7 / SEC-8 — hygiene (P3)
`function_search_path_mutable` on assorted functions — add `SET search_path =
public, pg_temp` at next edit (see `system/lessons.md`). `pg_net` in `public` on
sks-labour — relocate to an `extensions` schema.

## Clean projects (probe + advisors, 2026-06-05)
- eq-canonical, eq-canonical-internal, sks-canonical, eq-solves-field,
  eq-substrate: public-key reads all `401`/empty (no anon read leak).
- ERROR-level advisors: only SEC-2. All other advisor output is WARN/INFO
  (SECURITY DEFINER-callable-by-authenticated, permissive policies, search_path).

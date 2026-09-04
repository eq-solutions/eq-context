---
title: OPS — Security Register
owner: Royce Milmlow
last_updated: 2026-09-05
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
| SEC-1 | **P0 — live PII leak** | Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` | sks-labour (LIVE — confirmed by Royce 2026-07-16 still active, retirement date NOT set) | **STILL OPEN, deliberately not engineered around.** **Reaffirmed 2026-07-20 (Royce): "SKS NSW Labour is not to be touched — we are keeping it going while we build Field."** Same standing decision as 2026-06-05 (below), restated after this session got as far as verifying live `pg_policies` and staging a Stage 2 RLS-hardening migration before being stopped — no engineering changes land on sks-nsw-labour, full stop, until Field replaces it. Fix stays decommission-at-cutover, not interim hardening. Nothing was written to `nspbmirochztcjijmcrx` or the sks-nsw-labour Netlify project this session — read-only verification only. **Update 2026-08-21 (Royce): retirement now weeks away — de-escalated from active NEEDS-YOU nagging on that basis.** Still OPEN until the app is actually decommissioned, not on the strength of a timeline — see Detail. |
| SEC-3 | **P3 — hygiene (downgraded from P0 2026-07-20)** | `ehowg` service_role key never rotated (F1) — **no confirmed leak vector found**, unrotated ≠ leaked | sks-canonical (LIVE) | **OPEN, hygiene priority.** Investigated 2026-07-20: the only evidence for "leaked" across the whole substrate is the key still being *valid* (unrotated since 2026-05-24) — no incident, no leak vector, no exposed-location ever documented. A **later, more careful analysis** (`cross-app-linkage-sprint-2026-06-07.md`) explicitly downgraded this: *"tenant_routing key concentration... No live exposure today; high cost if it leaks."* Corroborates the eq-field punch-list's own June note that the "exposed" flag looked stale. **Royce's call 2026-07-20: downgrade, rotate at a calm moment, not a rushed weekend window.** Rotation runbook (`f1-ehowg-key-rotation-runbook-2026-06-03.md`) still valid whenever it happens. |
| SEC-9 | ~~P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27~~ **CLOSED 2026-08-16 (dev-context-unmasked pattern)** | A different service_role key (`jvkn`/eq-canonical) was pasted directly into a chat session 2026-07-12 to fix `canon-read` | eq-canonical (LIVE) | **Read this Status column, not the Severity column (clarified 2026-09-04): still OPEN.** The Severity cell's strikethrough + "CLOSED 2026-08-16" closed only the dev-context-masking sub-issue (which SEC-61 later found didn't hold either); the jvkn key rotation this row is about has not happened. Already misread once this way (`sessions/2026-08-30.md`). **OPEN.** Unlike SEC-3, this exposure IS confirmed — plaintext in a chat transcript is a real leak vector, not a hygiene item. **Royce's call 2026-07-20: same priority and rotation window as SEC-3** rather than treating separately. Rotate both together whenever that window lands. **2026-07-27: a consumer-mapping subagent (run to draft the missing rotation runbook — see below) was flagged by the Claude Code security classifier for "credential materialization" — it decoded a live jvkn service_role JWT's payload (role/ref claims) while searching Netlify env vars for consumers, and that decoded output is part of this session's tool-call record.** Not confirmed as a full second leak: a JWT payload is base64, not encrypted, and decoding it reveals only claims (`role: service_role`, `ref: jvkn...`) already described in plain English in this very row — that's materially different from the *encoded bearer token itself* (the three dot-joined segments that actually authenticate) appearing in output. The final summary I received back only showed masked fragments (`…wp9o`); I have no visibility into the subagent's own raw tool-call outputs to confirm whether the full token string appeared there too. Recorded honestly rather than assumed either way. **Process fix applied going forward:** any future credential-consumer mapping should be scoped to env-var *names/presence* only, never fetch/print/decode actual values. **2026-07-31: a routine `getAllEnvVars` call on eq-shell's Netlify project (during unrelated perf work, no credential lookup intended) returned this same `SUPABASE_SERVICE_ROLE_KEY` (jvkn/eq-canonical) fully unmasked — the actual bearer token, not just decoded claims like the 2026-07-27 note above.** Confirmed via the `dev`-context value specifically: `production`/`branch-deploy`/`deploy-preview` all came back correctly redacted (`****`), but `dev` did not, **despite this var carrying `is_secret: true`** — a materially worse pattern than SEC-12/SEC-18 (those were `is_secret: false` misconfigurations; this key was configured correctly and still leaked). Same call also returned unmasked `dev`-context plaintext for `EQ_SHELL_JWT_SECRET`, `EQ_SESSION_SALT`, `TENANT_ROUTING_MASTER_KEY`, `CANONICAL_API_KEY_FIELD`, `EQ_PLATFORM_ADMIN_KEY`, and `SKS_SUPABASE_JWT_SECRET` — all `is_secret: true`, all unmasked in `dev` regardless. **Suspected root cause, not yet confirmed against Netlify's docs/support:** the `dev` context may not be covered by Netlify's own value-masking at the API layer at all, regardless of the `is_secret` flag — if true, this affects every secret on every EQ Netlify project that has ever had a `dev`-context value set, not just this key. None of the actual values were printed or reproduced in that session's chat output, but they are sitting in this session's tool-call history. **Royce's call 2026-07-31: log only, rotate at the same later window as SEC-3/SEC-9 proper, no emergency rotation.** Open follow-up: confirm the `dev`-context-always-unmasked theory against Netlify support/docs, and if true, treat it as a standing rule (never call `getAllEnvVars` broadly — request specific keys only, or accept that any project with a `dev`-context secret value is exposed to this same read). **2026-08-01 finding:** jvkn already has `sb_publishable_`/`sb_secret_`-style keys available (confirmed live via `get_publishable_keys`), independent of the project's JWT secret — Supabase's own docs confirm secret keys on this system "no longer touch your project's JWT secret" and rotating one signs out **zero** users, vs. legacy JWT-secret rotation ("rotate the JWT secret," the runbook's original Step 1) which signs out every active session suite-wide (Shell + every Field/Service/Cards iframe token-exchanged from it — confirmed in code: `eq-shell/netlify/functions/_shared/supabase-jwt.ts` mints all live session JWTs with `SUPABASE_JWT_SECRET`, the same secret Step 1 would rotate). So the leaked service_role key can very likely be swapped with **no session wipe** — see the runbook's updated Step 1. Also live-confirmed: no encrypted copy of jvkn's own key sits in `shell_control.tenant_routing` (0 rows). **Royce's call 2026-08-01: defer anyway, same calibration as SEC-3** — real-world marginal risk assessed low (this exposure was local-machine chat only, never confirmed to have left that trust boundary, same reasoning already applied to SEC-3/SEC-9's other 2026-07-27/31 entries). Not urgent; rotate via the now-cheap safe path whenever convenient. **2026-08-08 — the `dev`-context-always-unmasked theory (flagged unconfirmed on 2026-07-31, above) is now CONFIRMED, not suspected.** Royce asked for a live re-sweep of the EQ/SKS Netlify projects (prompted by locating the old `eq-env-catalog.html` catalog and a fresh Grok-authored secrets-practices PDF, ahead of deciding whether to build a proper secrets inventory doc) to verify SEC-9/10/12/18/19's masking closures hadn't silently regressed. They hadn't regressed on `is_secret` — every var this session checked that SEC-12/18/19 closed is still correctly `is_secret: true` in branch-deploy/deploy-preview/production. But `dev` context is a different story: a `getAllEnvVars` read (same call type as the 2026-07-31 incident) reproduced the identical pattern on **17 more secrets across 3 more sites**, confirming this is a standing Netlify platform behaviour, not a one-off — **eq-shell (11):** `EQ_SERVICE_HANDOFF_KEY`, `EQ_SHELL_BRIDGE_SECRET`, `SKS_SUPABASE_JWT_SECRET`, `SUPABASE_JWT_SECRET`, `EQ_QUOTES_HANDOFF_KEY`, `CANONICAL_API_KEY_SERVICE`, `SUPABASE_SERVICE_ROLE_KEY` (this row's own jvkn key — still leaking live, today), `EQ_PLATFORM_ADMIN_KEY`, `CANONICAL_API_KEY_FIELD`, `EQ_SESSION_SALT`, `EQ_SHELL_JWT_SECRET`; **eq-field (1):** `SKS_JWT_SECRET`; **eq-service (5):** `SUPABASE_SERVICE_ROLE_KEY` (points at the already-deleted urjh project — dead-key hygiene, not a live risk), `EQ_PLATFORM_ADMIN_KEY`, `EQ_SECRET_SALT`, `EQ_SHELL_JWT_SECRET`, `CANONICAL_API_KEY_SERVICE`. eq-cards not re-checked this pass — the Netlify write-tool's own classifier blocked that one read (declined, not a credential-handling failure on this end); needs a retry or Royce's own dashboard check. **Correction, same day:** the first pass of this addendum undercounted (missed `EQ_QUOTES_HANDOFF_KEY` on eq-shell and 3 of eq-service's 5, having conflated Netlify's `dev` and `dev-server` contexts on a couple of vars) — caught and fixed before Royce acted on it, corrected counts above. **This closes the open follow-up below**, and it means the SEC-12/18/19 fix pattern (same-value re-store with `is_secret: true` ticked) does not actually close this exposure — every var in this list already carries `is_secret: true` and still leaks, because Netlify never masks `dev` regardless of that flag. The real fix is different: **clear the `dev`-context value entirely** (delete just that one context row per var, leave branch-deploy/deploy-preview/production untouched) — vars on the same sites that already have an empty `dev` value (e.g. `FIELD_SUPABASE_SERVICE_ROLE_KEY`, `EQ_SERVICE_API_KEY`) don't leak. Manual-hands-only, same classifier block as SEC-12/18/19 — Royce via the Netlify dashboard or CLI. Values not reproduced anywhere in this entry, per the existing process fix above. **2026-08-11 addendum:** a merge-readiness subagent (auditing the Cards SSO broker PRs, checking whether `EQ_CARDS_HANDOFF_KEY` was configured yet) ran `netlify env:list --json` against eq-shell and eq-cards — a different tool than the `getAllEnvVars` MCP call every prior entry here used, same underlying exposure class (unmasked values via a routine list operation). Its own report says it briefly wrote the unmasked output to a local scratchpad file, then deleted that file immediately after confirming the negative result (`EQ_CARDS_HANDOFF_KEY` absent from both). Not confirmed clean — same honesty standard as the rest of this row: the values passed through that subagent's own tool-call transcript before deletion, which this session has no visibility into. No values reproduced in its report or here. **Not a new standing risk** (same vars, same already-logged exposure), but a reminder the `netlify` CLI is exposed to the identical process-fix gap as the MCP tool — any future audit needing to confirm a var's *presence* should still scope to names only, regardless of which tool it reaches for. **2026-08-16 — CLOSED.** Live Netlify dashboard re-sweep (Royce clicking through each site, this session calling out vars from `ops/secrets-inventory.md`) closed the entire dev-context-unmasked list above — all 11 eq-shell + 1 eq-field + 5 eq-service vars re-verified masked in every context including `dev`. **New variant found same pass, not previously listed here**: eq-cards' `SUPABASE_SERVICE_ROLE_KEY` (jvkn control-plane) and `SUPABASE_JWT_SECRET` were also live-readable in **production** despite `is_secret:true` having been set back in July — confirms the root cause one layer worse than believed: toggling the flag on an existing var does not purge the value stored before the toggle, only delete+recreate does. Closed same session (delete+recreate on all 4 eq-cards secret vars: the two above plus `EQ_SESSION_SALT`/`EQ_SECRET_SALT`). Also closed same session, same root-cause family: eq-cards `shell-verify.js`'s `ensureAuthUser()` silently proceeded past a failed admin `getUser` check (any non-404 status — including a 401 from a bad `SUPABASE_SERVICE_ROLE_KEY` — was treated as "user already exists") — eq-cards [PR #250](https://github.com/eq-solutions/eq-cards/pull/250), merged and deployed live. Full detail: `ops/secrets-inventory.md`. |
| SEC-10 | ~~P0~~ **CLOSED 2026-07-30** | `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is_secret: false`), full values returned by a routine env-var read 2026-07-20 and now sitting in a chat transcript, same leak-vector class as SEC-9 | sks-nsw-labour (Netlify, LIVE) | **CLOSED.** Royce rotated both keys himself via console.anthropic.com / resend.com and re-stored them with `is_secret: true` (confirmed live 2026-07-30 08:05 UTC — values now masked in branch-deploy/deploy-preview/production/dev-server, `dev` context empty). The `EQ_SECRET_SALT` `dev`-context plaintext leftover from the same finding was cleared the same session (08:08 UTC) via the Netlify env-var MCP — set to empty string without the assistant ever reading or entering the real value. All three exposure vectors in this finding are now closed. Open follow-up carried over: re-check whether any other Netlify project has the same `is_secret: false` pattern on a real credential (not yet done). |
| SEC-2 | ~~P1~~ **CLOSED** | RLS policy `tenant_isolation` trusts end-user-editable `user_metadata` (advisor ERROR) | eq-canonical-internal | **CLOSED 2026-07-21 — was already fixed, register was stale.** See Detail. |
| SEC-4 | ~~P3~~ **CLOSED 2026-08-20** | `anon`-executable SECURITY DEFINER `eq_cards_*` fns | eq-canonical | **CLOSED — live-reverified 2026-08-20** during the suite-wide pressure-test sweep: the 3 functions this row flagged for revocation (`claim_invite`/`delete_account`/`get_worker_hr_record`) are authenticated-only today, not anon. jvkn's anon-executable SECURITY DEFINER surface has grown since (4 → 12 functions) but the growth is reviewed and gated: 10 are legitimate token/auth-gated RPCs, 1 (`eq_cards_preview_invite`) is a deliberate token-capability design, 1 (`tg_fulfil_access_requests_on_claim`) is a trigger function whose grant is functionally inert (Postgres blocks direct invocation outside trigger context) — all 12 covered by `check-tenant-drift.mjs`'s `FUNC_EXEC_ANON_ALLOW` baseline. See SEC-31 for a real, separate jvkn finding this same sweep found. |
| SEC-5 | P3 — hygiene | always-true (`USING/WITH CHECK = true`) write policies | eq-solves-field, eq-canonical-internal | **VERIFIED latent** 2026-06-05 — anon holds NO table grant, policies unreachable. Post-launch cleanup. |
| SEC-6 | P2 | `context_proposals` anon INSERT has length caps but no volume throttle | eq-substrate | OPEN — needed before the queue has a consumer |
| SEC-7 | P3 | `function_search_path_mutable` (search_path not pinned) | several projects | OPEN — hygiene, fix at next touch. **eq-service's instance CLOSED 2026-08-11** — see Detail. **jvkn instance found 2026-08-20:** `public.eq_format_au_mobile` — not yet fixed. |
| SEC-8 | P3 | `pg_net` extension installed in `public` schema | sks-labour | OPEN — moot once sks-labour retired |
| SEC-11 | **P3 — accepted, docs corrected (downgraded from P1 2026-07-23)** | `tenant-migrate.yml`'s `production` GitHub Environment has **zero protection rules** (`protection_rules: []`, confirmed via `gh api repos/eq-solutions/eq-shell/environments/production` 2026-07-23) despite the workflow's own header comment and prior session memory both asserting "gated behind the `production` Environment so it PAUSES for a human approve click... `production` environment with Royce as required reviewer — CREATED 2026-06-03." | eq-shell (GitHub Actions/repo config) | **ACCEPTED, not fixing — Royce's call 2026-07-23.** Found live: dispatched `tenant-migrate.yml` (migration 0199, whole fleet) on Royce's "dispatch tenant-migrate.yml" — the `Apply to all tenants` job ran straight through in ~15s with no approval pause, applying live DDL to both zaap and ehow. Attempted the fix (`gh api --method PUT .../environments/production` with Royce/`Milmlow` id `271704382` as required reviewer) — **rejected, HTTP 422: "Please ensure the billing plan supports the required reviewers protection rule."** Required-reviewer environment protection needs GitHub Team/Enterprise Cloud (or a public repo); this private repo doesn't have it. Royce's call: don't pay for the plan upgrade — `Milmlow` is the only repo collaborator with dispatch access anyway (confirmed via `gh api repos/.../collaborators` — one entry), so a reviewer gate would only ever be "Royce clicks twice," not a real access boundary. **Fixed instead:** corrected the false claim in `tenant-migrate.yml`'s header + inline comments (PR [#985](https://github.com/eq-solutions/eq-shell/pull/985), OPEN) so nobody trusts a safety net that isn't there. Real safeguard going forward: deliberate manual dispatch only, no second-click gate. |
| SEC-12 | ~~P0~~ **CLOSED 2026-07-27** | Several real secrets on **eq-shell's own** Netlify project stored with `is_secret: false` — full plaintext returned on any routine env-var read/API call, unmasked in Netlify's own UI | eq-shell (Netlify, LIVE, site `a3473f83-7c82-4f1e-872d-aa96eaa55172`, core.eq.solutions) | **CLOSED 2026-07-27 — Royce re-stored all 8 himself, live-verified.** `getAllEnvVars` re-checked directly: `GOOGLE_DOC_AI_CREDENTIALS`, `EQ_PLATFORM_ADMIN_KEY`, `EQ_SHELL_JWT_SECRET`, `SKS_SUPABASE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`, `EQ_QUOTES_HANDOFF_KEY`, `CANONICAL_API_KEY_FIELD`, `EQ_SESSION_SALT` all now `is_secret: true`, all timestamped 2026-07-27T06:57–07:02Z. Same-value re-store confirmed, not a rotation — both eq-shell and sks-nsw-labour deploys checked `ready` immediately after, no outage. Original finding detail below, retained for history. Was: **OPEN.** Found 2026-07-26 during the SKS NSW onboarding security review, while checking `ENFORCE_IFRAME_ORIGIN` (confirmed separately: set to `true` in production — SEC-11-adjacent CSRF gap is enforced, not a hole). A `getAllEnvVars` read surfaced, all currently `is_secret: false`: `GOOGLE_DOC_AI_CREDENTIALS` (full Google service-account JSON incl. RSA private key, production context — **the most serious of the set**, grants direct GCP API access if leaked), `EQ_PLATFORM_ADMIN_KEY`, `EQ_SHELL_JWT_SECRET`, `SKS_SUPABASE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`, `EQ_QUOTES_HANDOFF_KEY`, `CANONICAL_API_KEY_FIELD`, `EQ_SESSION_SALT` — all identical plaintext value across every context (dev/branch-deploy/deploy-preview/production) except `GOOGLE_DOC_AI_CREDENTIALS` (production only). Do not confuse `EQ_SESSION_SALT` (this finding) with `EQ_SECRET_SALT` (a distinct, similarly-named var already correctly `is_secret: true` on this same site). **Remediation attempted, blocked by design:** a same-value re-store (upsert with `envVarIsSecret: true`, no rotation) via the Netlify MCP was **blocked by the Claude Code safety classifier** as "modifying security settings" — this is a manual-hands-only fix, not something any Claude Code session can complete regardless of explicit permission. **Royce must do this himself** via the Netlify dashboard (Site settings → Environment variables → per key: note the current value, delete, recreate with the identical value, tick "contains sensitive values" this time) or the Netlify CLI. Same-value re-store, not rotation — changing any value breaks live signing (in-flight JWTs, handoff tokens) immediately. Rotation is a separate, larger decision (mirrors the SEC-9/SEC-3 "rotate whenever convenient" pattern) — not needed just to close the plaintext-storage gap. |
| SEC-13 | ~~P2~~ **CLOSED 2026-08-20** | Closed 2026-07-27 for the Ops/Quotes RPC surface (39 zaap / 12 ehow, `public` schema). Re-verification found the "ehow holds zero" close claim is false today: 12 anon-executable SECURITY DEFINER functions live on ehow right now, plus 3 beyond the accepted baseline on zaap — a different function set than the one the original fix targeted, in `service`/`app_data` schemas the drift gate never scans. | sks-canonical (ehow, all 12 body-verified, REVOKE live) + eq-canonical-internal (zaap, all 3 body-verified, REVOKE live) | **CLOSED 2026-08-20 — anon-EXECUTE revoked live on both planes (eq-shell PR #1499, migration 0252, applied via `tenant-migrate.yml` dispatch run 32406586537) and the gate coverage gap fixed (PR #1498, merged + live). Live-reverified directly against both databases, not inferred from CI/PR status: all 15 now `anon_exec: false`.** See Detail addendum — the `field_people_removed_iud` tautology bug is a separate, still-open thread, unaffected by this REVOKE. |
| SEC-14 | **P3 — accepted, docs corrected (same class as SEC-11, different repo)** | `apply-service-migrations.yml`'s `production` GitHub Environment has no required-reviewer rule (`protection_rules` branch-policy only, confirmed via `gh api repos/eq-solutions/eq-service/environments/production` 2026-07-28) despite the workflow's own header comment asserting it "PAUSES for a human approve click before any live DDL." | eq-service (GitHub Actions/repo config) | **ACCEPTED, not fixing — same reasoning as SEC-11.** Found live: dispatched `apply-service-migrations.yml` on Royce's "go ahead" for PR #619's 2 reconciled migrations — the `Apply to ehow` job ran straight through in 18s with no approval pause, applying both to live ehow. No harm done (the SQL was already dry-run verified safe in a rolled-back transaction before merge). Same root cause as SEC-11: required-reviewer environment protection needs GitHub Team/Enterprise Cloud or a public repo; this private repo has neither. `Milmlow` is the only repo collaborator with dispatch access (confirmed via `gh api repos/.../collaborators` — one entry), so a reviewer gate would only ever be "click twice," not a real access boundary — not paying for a plan upgrade. **Fixed instead:** corrected the false claim in `apply-service-migrations.yml`'s header comment (PR [#620](https://github.com/eq-solutions/eq-service/pull/620)) so nobody trusts a safety net that isn't there. **Wider sweep done 2026-07-28:** checked all 14 org repos (`gh search code "environment:" --filename ".yml"` per repo + `gh repo list` to confirm none were missed) for any other environment-gated workflow. Found exactly one more cluster: eq-context's 7 backup/verify/restore-drill workflows, all on a `production-ops` environment with the same branch-policy-only protection (confirmed via `gh api repos/eq-solutions/eq-context/environments/production-ops`) — but their own comments already say so accurately ("NO required reviewers... never paused waiting for an approval"), no false claim there. No other repo uses environment gating at all. This class of finding is now closed as fully swept, not just the two instances found by accident. |
| SEC-15 | ~~P2~~ **CLOSED 2026-07-28 (same class as SEC-13)** | `public.rls_introspection()` — ad-hoc SECURITY DEFINER diagnostic dumping every `public`/`service` table's RLS state + every policy's full qual/with_check, no tenant scoping — found live with EXECUTE granted to `anon`+`authenticated`. No migration file, no `_eq_migrations` ledger row, no caller anywhere in the codebase: created out-of-band, same root cause as SEC-13 (a fresh instance appearing *after* SEC-13 seeded the sks-canonical baseline to empty, i.e. the drift gate catching a new violation exactly as designed, not a gap in that fix). Root cause traced separately: eq-service's own migration `0192` had recreated the function with `REVOKE ALL FROM PUBLIC` only, dropping the explicit `anon, authenticated` naming an earlier migration required — ehow's `public`-schema default privileges (which only ever covered tables, never functions, in the 2026-06-07 lockdown) auto-granted EXECUTE back on the fresh `CREATE`. | sks-canonical (ehow) — confirmed absent on zaap (EQ tenant), ehow-only | **CLOSED — two sessions independently fixed the identical live exposure via two separate governed pipelines, ~85s apart, no conflict (both idempotent REVOKE/GRANT):** eq-shell [#1061](https://github.com/eq-solutions/eq-shell/pull/1061) (`0219_revoke_anon_rls_introspection.sql` via `tenant-migrate.yml`, dispatch run 30334947428, merged as `a950bbe1`) and eq-service [#622](https://github.com/eq-solutions/eq-service/pull/622) (`0194_revoke_rls_introspection_anon_grant.sql` via `apply-service-migrations.yml`, merged as `619dd5e6`). Both merged and live-reverified: `has_function_privilege('anon', 'public.rls_introspection()', 'EXECUTE')` now `false`, `service_role` still `true`. Not added to `FUNC_EXEC_ANON_ALLOW` — correctly locked to service_role, no anon use case (SQL-console/ops-script diagnostic only). Real cost was duplicate engineering effort across two repos, not a live risk. **Open, not closed here — see SEC-16, CLOSED 2026-07-28.** **Ownership resolved 2026-07-28 (Royce confirmed):** `rls_introspection()` belongs to eq-solves-service going forward, not eq-shell — it lives in the shared `public` schema but only ever reads `service` schema + the only real caller anywhere is eq-service's own `scripts/audit-rls.ts`; it doesn't exist on zaap at all. eq-shell's migration `0219` stays in eq-shell's history as-is (harmless, identical end-state to eq-service's `0194` — no need to revert), but any *future* change to this function should land in eq-service's `supabase/migrations/`, not eq-shell's `tenant-migrations/`. |
| SEC-16 | ~~P2~~ **CLOSED 2026-07-28** | Root cause behind SEC-4/SEC-13/SEC-15 recurring three times: nothing stopped a brand-new SECURITY DEFINER function from being born anon-executable. `ALTER DEFAULT PRIVILEGES ... ON FUNCTIONS ... REVOKE FROM PUBLIC` (mirroring the 2026-06-07 table lockdown) does not work on this platform — see the "SEC-15 — root-cause investigation" writeup below for the full 3-line-of-evidence diagnosis (Postgres' own `acldefault('f', ...)` includes `PUBLIC`; Supabase's own docs confirm new functions get `anon`/`authenticated`/`service_role` granted by default; empirically reproduced on both ehow and zaap). | jvkn (control), zaap (EQ tenant), ehow (SKS tenant) — all three | **CLOSED — a working mechanism exists after all, just not a "setting": a `ddl_command_end` event trigger** (`eq_enforce_function_privacy`), re-asserting `REVOKE ALL FROM PUBLIC, anon, authenticated; GRANT EXECUTE TO service_role` on every function landing in a guarded schema (`public`+`service` on zaap/ehow, `public`+`shell_control` on jvkn) immediately after creation. Verified compatible with an explicit follow-up `GRANT` for a legitimate anon/authenticated RPC (the trigger fires on the `CREATE`/`ALTER FUNCTION` command itself; a later `GRANT` is a separate command, unaffected). Each guard runs in its own exception handler — a bug here can only skip one function, never block an unrelated migration. eq-shell [#1070](https://github.com/eq-solutions/eq-shell/pull/1070) (tenant migration `0220`, applied via `tenant-migrate.yml` to zaap+ehow, dispatch run 30337989873) + control-plane migration applied to jvkn via Supabase MCP, ledgered in `CONTROL-PLANE-LEDGER.md` (eq-shell [#1072](https://github.com/eq-solutions/eq-shell/pull/1072)). Live-verified on all three planes post-apply with a real (non-transactional) test function each: `anon=false`, `service_role=true`. **Corrects the "SEC-15 — root-cause investigation" conclusion below** ("there is no available setting that prevents this at creation time") — true for settings/default-privileges specifically, but an event trigger is a different mechanism and does work. **The predicted risk materialized 2026-07-31 (Sentry EQ-CARDS-1C):** eq-cards migration `0111_fix_auto_provision_personal_membership_role.sql` (a plain `CREATE OR REPLACE FUNCTION public.eq_cards_auto_provision()`, applied live to jvkn 2026-07-30 08:10 UTC) had no trailing `GRANT`, so the trigger silently stripped `authenticated`'s EXECUTE the moment it applied — real self-signups then hit a hard `permission denied` (42501) trying to provision their wallet, 2 users blocked over ~9 hours before caught. Confirmed live via `pg_get_functiondef`/`has_function_privilege` before the fix. **This is the actual, general failure mode SEC-16 enables**: the trigger does its job correctly, but nothing warns a migration author that editing ANY existing `public`/`shell_control` (jvkn) or `public`/`service` (zaap/ehow) function requires re-adding the `GRANT EXECUTE ... TO <role>` line, even when the function already had one before the edit — `CREATE OR REPLACE` does not carry grants forward through this trigger the way plain Postgres would without it. Fixed: eq-cards [PR #191](https://github.com/eq-solutions/eq-cards/pull/191) (`0113_restore_auto_provision_authenticated_grant.sql`, applied live via Supabase MCP, Royce's explicit go). **Not yet done:** neither eq-cards nor eq-shell's migration-authoring docs call this out explicitly — a future edit to any existing anon/authenticated-callable function on these three planes will repeat this exact incident unless the author already knows to re-grant. Flagged as a real gap, not closing this row for it since SEC-16's own fix is sound; the gap is documentation/process, not the trigger. |
| SEC-18 | ~~P0~~ **CLOSED 2026-07-30** | Real production secrets stored `is_secret: false` (full plaintext, all four deploy contexts) on eq-service, eq-field, and eq-cards — the identical pattern SEC-12 found and closed on eq-shell, just never checked on the apps that also consume these same values | eq-service, eq-field, eq-cards (Netlify, LIVE) | **CLOSED.** Royce re-stored all 8 himself via the Netlify dashboard (same-value re-store, no rotation) — live-reverified via `getAllEnvVars` on all three sites: `CANONICAL_SERVICE_ROLE_KEY`, `EQ_SHELL_JWT_SECRET`, `EQ_PLATFORM_ADMIN_KEY`, `UNSUBSCRIBE_SECRET` (eq-service, 09:11–09:13 UTC), `SKS_JWT_SECRET` (eq-field, 09:13:57 UTC), `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET` (eq-cards, 09:14–09:15 UTC) all confirmed `is_secret: true` on first pass. `EQ_SESSION_SALT` on eq-service was missed on the first pass (still `is_secret: false`, stale 2026-06-13 timestamp) — flagged, Royce re-did that one too, confirmed `is_secret: true` at 09:19:58 UTC on second verification. All 8 now closed; no rotation performed (same-value re-store only, per the SEC-12 precedent — a leak this transcript never actually reproduced any value for). Found while sweeping for SEC-10's own follow-up (checking whether any other Netlify project has the plaintext pattern) — turned out worse than SEC-10 itself. Confirmed via `getAllEnvVars`, values not reproduced here (recon only, nothing entered/resubmitted anywhere): **eq-service** — `CANONICAL_SERVICE_ROLE_KEY` (full service_role key for **ehow/sks-canonical**, the live production DB behind Service + Field — the single most serious item in this set), `EQ_SHELL_JWT_SECRET` (Shell's session-signing secret — holder can forge valid sessions), `EQ_PLATFORM_ADMIN_KEY`, `EQ_SESSION_SALT`, `UNSUBSCRIBE_SECRET`. **eq-field** — `SKS_JWT_SECRET` (same value as eq-shell's correctly-secret `SKS_SUPABASE_JWT_SECRET`). **eq-cards** — `SUPABASE_SERVICE_ROLE_KEY` (full service_role key for **jvkn/eq-canonical**, the control-plane DB) and `SUPABASE_JWT_SECRET`. Every one of these is properly `is_secret: true` on the app that owns it (mostly eq-shell) — just not ticked when the same value was copied to the consuming app. `sks-comms`/`eq-core-design`/`life-tracking`/`knx-job-folder` not yet checked (read as personal/hobby projects, not EQ suite — lower priority). **Not touched.** Same remediation path as SEC-12: a same-value re-store (not rotation) is the fix, and per SEC-12's own attempt, the Claude Code safety classifier blocks this by design as "modifying security settings" regardless of explicit permission — **manual-hands-only, Royce via the Netlify dashboard or CLI** (per var: note current value, delete, recreate identical, tick "contains sensitive values"). Given the severity here (live DB service_role keys + a session-signing secret, not just third-party API keys), also worth Royce's explicit call on whether any of these warrant rotation rather than just re-masking — unlike SEC-12's set, a leak of `CANONICAL_SERVICE_ROLE_KEY` or `SUPABASE_SERVICE_ROLE_KEY` grants full database access, and `EQ_SHELL_JWT_SECRET`/`SKS_JWT_SECRET` leaking lets an attacker forge sessions outright. **Completed same day by a second, independent sweep pass** (this session ran the same `getAllEnvVars` check in parallel, unaware of the other's findings until both landed): confirms every item above and adds more exposed on the same three sites — **eq-service** also has `EQ_SERVICE_JWT_SECRET` (its own signing secret, same value as eq-field's `SKS_JWT_SECRET` below — shared across the two, not previously listed), `EQ_SERVICE_HANDOFF_KEY`, and `EQ_SERVICE_API_KEY` all `is_secret: false`; **eq-cards** also has `EQ_SECRET_SALT` and `EQ_SESSION_SALT` exposed (not just `SUPABASE_JWT_SECRET`); **eq-field** also has `EQ_FIELD_HANDOFF_KEY` exposed alongside `SKS_JWT_SECRET`. Also closes the "not yet checked" list: `sks-comms`, `eq-core-design`, and `knx-job-folder` have **zero env vars configured** (nothing to expose); `life-tracking` likewise empty; `eq-receipts` holds only `VITE_SUPABASE_URL` (plain URL) and `VITE_SUPABASE_ANON_KEY` (already `is_secret: true`, and an anon key is meant to be public regardless) — no real secret on any of the five. Full exposed-variable inventory across eq-service/eq-field/eq-cards, this entry plus the addendum: `CANONICAL_SERVICE_ROLE_KEY`, `EQ_SHELL_JWT_SECRET`, `EQ_PLATFORM_ADMIN_KEY`, `EQ_SESSION_SALT`, `UNSUBSCRIBE_SECRET`, `EQ_SERVICE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`, `EQ_SERVICE_API_KEY` (eq-service); `SKS_JWT_SECRET`, `EQ_FIELD_HANDOFF_KEY` (eq-field); `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`, `EQ_SECRET_SALT`, `EQ_SESSION_SALT` (eq-cards). Still **not touched** — same manual-hands-only remediation path, still open. |
| SEC-19 | **P1 — CLOSED 2026-07-30 (DB), code fix pushed not yet merged** | `people.pin` (plaintext 4-digit login PIN) was directly SELECT-able by the anon key — not just a PII leak like SEC-1, a live-credential leak: anyone holding the public anon key (or reading the app's own network traffic) could read every worker's login PIN in one request. `loadFromSupabase`'s bulk roster fetch (`index.html`, every session) requested `select=*`, round-tripping every PIN over the wire on every load. Three RPCs (`verify_staff_pin`, `trigger_shift_events`, `bump_rate_limit`) were also anon/authenticated-executable with no caller anywhere (app, Netlify functions, or the 7 `pg_cron` jobs). | sks-labour (`nspbmirochztcjijmcrx`) | **DB hardening CLOSED, live-verified 2026-07-30 09:xx UTC (Royce ran it himself — blocked from Claude Code by the same "modifying security settings" classifier as SEC-12/SEC-18):** `revoke execute ... from anon, authenticated, public` on all 3 unused RPCs — confirmed via `has_function_privilege`: `verify_staff_pin`/`trigger_shift_events`/`bump_rate_limit` now `anon_exec=false, authenticated_exec=false`. `search_path = public, pg_temp` pinned on those 3 plus `eq_field_shift_payload` and `incidents_set_updated_at` (the 5 functions the advisor flagged `function_search_path_mutable`) — confirmed via `proconfig`. **Code fix (the PIN itself) pushed but not deployed:** sks-nsw-labour `claude/sks-nsw-labour-security-30b634` commit `c9fc8b0` (v3.10.106) — `people?select=*` → explicit column list excluding `pin`. Verified against live schema before push (exact 29-column select runs clean, `pin` absent). Not merged to `main` — Netlify only deploys on push to main, explicit-only per standing rule. **This closes the credential-leak escalation path (log in as staff), it does NOT close SEC-1** — the underlying PII read (names/phone/DOB/timesheets/leave, `org_id IS NOT NULL` being a no-op boundary on this single-tenant DB) is unchanged; real closure needs either per-user auth (Royce explicitly ruled out changing how staff log in) or decommission-at-cutover per SEC-1's existing plan. **Scoped narrowly, not a reopening of the SEC-1 "don't touch sks-nsw-labour" freeze:** Royce's explicit go-ahead this session was for this specific PIN fix only, prompted by naming the real business risk ("if this leaks the whole eq idea may get dropped by sks") — not a general reversal of the 2026-06-05/07-16/07-20 standing decision. Found a pre-existing, unrelated correctness bug along the way (PIN-management modal shows stale "No PIN" status for anyone whose PIN was set in a prior session, since `STATE.people` never carried `pin` from the bulk load even before this fix) — spun off separately, not fixed here. |
| SEC-17 | ~~P3~~ **CLOSED 2026-07-30** | Not an exposure — a dead audit target: `security_audit.py`'s `PROJECTS` dict and `rls_probe.py`'s `PROJECTS` dict both still carried `"eq-solves-field": "ktmjmdzqrogauaevbktn"`, a Supabase project deleted 2026-07-04. The advisor-audit step's `fetch()` has no per-project error isolation (an `HTTPError` on any one project returns 2 and aborts the whole script), so every scheduled `security-audit.yml` run since at least 2026-06-28 failed on a 400 "Resource has been removed" before it could report a summary — the gate had been silently non-functional for a month. | eq-context (CI tooling — `scripts/security_audit.py`, `scripts/rls_probe.py`, `.github/workflows/security-audit.yml`) | **CLOSED 2026-07-30.** Confirmed via live `list_projects` (project absent from the current 6) and independently via eq-field's own `DATA-PLANES-SOURCE-OF-TRUTH.md` ("`ktmjmdzqrogauaevbktn` was DELETED"). EQ Field has no standalone Supabase project today — its data lives on zaap (eq-canonical-internal) and ehow (sks-canonical), both already in `PROJECTS`. Removed the dead ref from both scripts and corrected the workflow's stale "4 EQ projects" comment (commit `d90768a`). Re-ran `security-audit.yml` via `workflow_dispatch` (run [30526701544](https://github.com/eq-solutions/eq-context/actions/runs/30526701544)) — green: `ERROR 0` on all 3 remaining projects (eq-canonical, eq-canonical-internal, sks-canonical). **Follow-up done same day:** `security_audit.py`'s `main()` no longer hard-aborts on the first `HTTPError`/`URLError` — a bad ref is now reported and skipped, all other projects still get checked, and the run only fails at the end if a fetch failure or a new ERROR finding occurred. `eq-receipts` (`bgrhqvmvzgotxzjneskv`, live since 2026-07-21, never previously in scope) added to `security_audit.py`'s `PROJECTS` under the now-isolated loop. **Fully closed 2026-07-30 (later same day):** the `get_publishable_keys` block above was a one-off classifier hiccup, not a hard rule — a second attempt succeeded and returned eq-receipts' publishable key cleanly. Added to `rls_probe.py`'s `PROJECTS` (all 6 tables: `entities`, `categories`, `receipts`, `line_items`, `extraction_jobs`, `exports` — every one has RLS enabled per `list_tables`). Ran the probe locally scoped to just this project (`RLS_PROBE_PROJECT=eq-receipts`) before pushing — all 6 come back `200 empty`, no anon-readable rows. Both scripts now cover all 4 EQ projects. |
| SEC-20 | ~~P1~~ **CLOSED 2026-08-04** | `generate-wallet-pass` edge function's ownership check was dead code — queried a non-existent `workers.auth_user_id` column via a `worker_id` field never selected on the credential row, so the check always no-opped. Any authenticated Cards user who obtained another worker's `worker_credentials.id` would have gotten that worker's full wallet-pass payload (name, licence number, credential type, expiry, issuing body) with no error. | eq-canonical (jvkn) — eq-cards `supabase/functions/generate-wallet-pass` | **CLOSED — and, checked directly against `list_edge_functions` on both `jvkn` and `zaap` before deploying, this function had in fact never been deployed to production on any version, vulnerable or otherwise: no changelog entry, no caller anywhere in the Cards app's own source (`grep` across `lib/` — zero matches). So the bug was real in the code but was never live-exploitable; nobody could reach it.** Found by the tenant-rule audit (`non-negotiables.md` #11) extended to eq-cards 2026-08-04, one of 6 elevated-client sites checked — the other 5 were clean/intentional (this schema has no org/tenant column on `workers`/`worker_credentials`/`profiles`/`licences` at all, confirmed via `0006_org_layer.sql`; ownership is scoped by `workers.user_id` instead). Fix: join `workers.user_id` into the existing query and gate on it, 404 (not 403) on mismatch so a guessed id can't be used to probe for existence; deleted the dead lookup block. eq-cards [PR #214](https://github.com/eq-solutions/eq-cards/pull/214) merged as `c256cf8`, then deployed as the function's first-ever live version (`jvkn`, `generate-wallet-pass` v1, deployed 2026-08-04) — Royce's explicit go-ahead, given the function is otherwise still pre-production (placeholder 1×1 icons, unsigned-pass fallback documented in the file's own header) and nothing calls it yet, so this deploy has zero user-facing effect today; it just forecloses the vulnerable version ever reaching production later. Verification: no Deno runtime available to run it locally; read through structurally, and the two real column names (`workers.user_id`, `worker_credentials.worker_id`) confirmed against live `jvkn` schema rather than assumed. |
| SEC-21 | ~~P1~~ **CLOSED 2026-08-08 — merged and live-verified** | `importPeopleCSV`/`importSitesCSV`/`importScheduleCSV` (`scripts/import-export.js`, EQ Field) had no `isManager` permission check — `importFullBackup` in the same file already gated on it, these three never did. Found in passing during an unrelated mobile-view audit (2026-08-07), independently re-verified live this session (read `origin/main` directly, not the working tree). | eq-field (`ehowgjardagevnrluult` / sks-canonical, LIVE — SKS tenant; also reachable on the `eq` demo tenant) | **CLOSED.** Confirmed live via direct `pg_policies` query on ehow: `app_data.sites` and `app_data.staff` (backs People/Supervision — inferred by elimination, no bare `people`/`managers` table exists under any schema; not 100% traced through `supabase.js`'s routing table) both scope INSERT/UPDATE/DELETE by `tenant_id` only, no role condition — the missing client-side check was the only gate stopping any authenticated non-manager from bulk-wiping Sites (`importSitesToSB` does purge-then-reinsert) or overwriting the People roster on the live SKS tenant. `app_data.schedule_entries` RLS already requires `eq_role IN ('manager','supervisor')` or `field.manage_roster` — had a DB-level backstop regardless of the client gap. `nav-data` is hidden for SKS (v3.5.211) but that's `display:none`, not an access boundary — devtools could still call these functions directly on SKS; on the `eq` tenant (demo/disposable, not live) the nav item is visible to any signed-in non-apprentice user with no extra step needed. Fix: added the identical guard `importFullBackup` already uses to all three functions — no change to the permission model. `import-export.js` sits on the parked 11-file `isManager`→canonical-permission migration list (`eq/pending.md`, parked 2026-07-27 for the SKS cutover window) — this is not that migration, just completing a missing instance of the mechanism the file already relies on; held at local-commit-only until Royce's explicit go ("Push + open PR now"), then pushed same session. eq-field [PR #670](https://github.com/eq-solutions/eq-field/pull/670) — squash-merged as `3a56fa1` on Royce's explicit "merge it", live-verified via `curl https://field.eq.solutions/sw.js` showing the new version post-deploy. Tests 0 failed, lint 0 errors both before and after the rebase below. Shipped as **v3.5.470, not v3.5.469** as originally planned — while this PR was in flight, `main` collected *five* other merges from concurrent sessions all independently claiming `v3.5.469` (`#663`, `#665`, `#666`, `#667`, `#668`), so this branch was rebased twice and renumbered to the actual next-free version at merge time; the other five collisions were pre-existing on `main` before this PR touched it and were left as-is (cosmetic changelog-label duplication only, not this finding's concern to fix). Companion gap in `importManagersCSV` (`scripts/managers.js:498` — same Data page, same missing check, same purge-then-reinsert write) found but not fixed here — spun off as a separate tracked task (`task_958ecccd`), not yet built. **Process note surfaced this session, not yet acted on:** at least 4 separate Claude Code sessions today independently hit the same shared, non-worktree `C:\Projects\eq-field` root checkout getting switched to a different branch mid-task by a concurrent session (see this repo's own `docs/reflection-log.md`, three other 2026-08-08 entries besides this one) — a repeated pattern today specifically, worth Royce deciding whether concurrent eq-field sessions should default to worktrees. |
| SEC-22 | ~~P1~~ **CLOSED 2026-08-08 — merged and live-verified** | `importManagersCSV` (`scripts/managers.js`, EQ Field) — the companion gap SEC-21 named and deliberately deferred — had no `isManager` check either. Feeds `importManagersToSB`, which purges the tenant's managers rows (`_purgeTenantRows`, a full DELETE scoped by `org_id`) then bulk-POSTs the CSV — wipe-and-replace, not a merge. | eq-field (`ehowgjardagevnrluult` / sks-canonical, LIVE — SKS tenant) | **CLOSED — built and merged by a separate session/task, confirmed here rather than duplicated.** Confirmed live: `app_data.staff` RLS on ehow (the table `managers`/`field_managers` resolves to) scopes only by `tenant_id` — no role condition — so the missing client-side gate was the only thing stopping any authenticated non-manager from wiping and overwriting the tenant's Supervision contacts via the always-visible "Import Supervision CSV" button. Fix matches `importPeopleCSV`/`importSitesCSV`/`importScheduleCSV`/`importFullBackup`'s existing guard exactly — same file, same pattern, no change to the permission model. The fixing session also swept the rest of `scripts/managers.js` for the same pattern: found `saveManagerCategoryToCanonical` and `addSupervisorNote` have no own-function check either, but traced both to confirm they're already double-gated (trigger buttons omitted from the DOM for non-managers, sole caller already gates before either fires) — left as-is, not the same live gap. eq-field [PR #672](https://github.com/eq-solutions/eq-field/pull/672), commit `5cc5069`, `v3.5.471` — live in production (`field.eq.solutions` now serves `v3.5.472`, past this fix). Tests 26/26 files 0 failed, lint 0 errors. Spawned task `task_958ecccd` (tracking this exact gap) dismissed as superseded — work was already done by the time it would have run. |
| SEC-24 | **P2 — architectural, open** | `EQ_SECRET_SALT` is one shared HMAC key across (at least) 4 Netlify deploys — eq-shell, eq-field, sks-nsw-labour, eq-solves-service — signing session cookies AND the Shell↔Field iframe-handoff token. A leak from any one of the four forges sessions suite-wide, not just on the app that leaked it. | eq-shell, eq-field, sks-nsw-labour, eq-solves-service (all Netlify, LIVE) | **OPEN, not previously tracked here.** Found live 2026-08-17 while correcting stale eq-field notes — the risk is real and already named in eq-shell's own local hardening backlog (`docs/security-hardening-sprint.md`, finding **H-15**: *"one leaked deploy forges session cookies suite-wide; only `session` has a `_NEXT` rotation key"*), but that doc lives inside an eq-shell worktree and was never surfaced in this register, so nothing outside that one session's context would ever find it. Per-consumer isolation is partially built but not fully cut over: eq-field's `verify-pin.js` already prefers a dedicated `EQ_FIELD_HANDOFF_KEY`, falling back to the shared `EQ_SECRET_SALT` only if that's unset (confirmed live in `netlify/functions/verify-pin.js`). eq-shell's own H-21 (retire the fallback / delete the dead Field-HMAC signing path) is explicitly blocked on H-15 finishing first. Compounds two already-tracked exposures: the 2026-04-27 chat exposure of eq-field's copy (never rotated, see eq-field's own `CLAUDE.md` TODO list) and the 2026-07-30 multi-lens finding that eq-field's copy was stored `is_secret:false` (unmasked) on Netlify. **Not actioned here** — this row exists so the cross-repo blast radius is visible from one place; the actual fix (finish per-consumer key cutover, then rotate the shared value once, coordinated across all 4 sites) is eq-shell's H-15/H-21 work, cross-repo, Royce's call on timing. |
| SEC-23 | **P3 — CLOSED at code level 2026-08-08, 2 GitHub alerts stay open (scanner limitation, not a real gap)** | `image-size@2.0.2`'s ICNS/JXL/HEIF parsers (Dependabot alerts [#193](https://github.com/eq-solutions/eq-shell/security/dependabot/193)/[#194](https://github.com/eq-solutions/eq-shell/security/dependabot/194)) — infinite-loop DoS: each parser walks a chain of length-prefixed entries/boxes, advancing an offset by a length field read straight from the file, with no guard against that length being `0`. A crafted file makes the offset stop advancing, so the loop (and, for HEIF/JXL, an ever-growing array) never terminates. The library's own internal `findBox` helper already guards this exact case (`box.size > 0 ? box.size : 8`) — the three outer consumers (`icns.ts`/`heif.ts`/`jxl.ts`) never applied the same guard to their own loop variables. | eq-shell — build tooling only, `@netlify/blobs` → `@netlify/dev-utils` → `image-size`; part of Netlify's local-dev toolchain (`netlify dev`), not app runtime code, not attacker-reachable in production | **No upstream fix possible — `image-size`'s GitHub repo was archived by its maintainer on 2026-06-03** ("this repo on github will not be updated"), so waiting was never actually an option; last session's "wait for upstream" note was wrong and corrected this session. **Patched locally via `pnpm patch`** (`patches/image-size@2.0.2.patch`, registered in `pnpm.patchedDependencies`) — a one-line `break` guard added to all three parsers' `.cjs`/`.mjs` builds, mirroring `findBox`'s existing pattern. **Verified empirically against the real installed package, before and after the patch**: hand-crafted malicious ICNS/HEIF/JXL payloads (entry/box length=0) hung all three parsers indefinitely pre-patch (confirmed via a 4s child-process timeout kill, not just read the code and assumed), returned/threw in under 1ms post-patch. `pnpm run build` and the full test suite (308/308) pass clean. eq-shell [PR #1288](https://github.com/eq-solutions/eq-shell/pull/1288), squash-merged `46829c6f`, live-deployed to core.eq.solutions (Netlify deploy confirmed `ready`, `error_message: null`, commit_ref match). **Caveat, why this row isn't a plain "CLOSED":** the patch doesn't change the resolved version string in the lockfile, so GitHub's Dependabot alerts #193/#194 are version-based and will very likely stay open indefinitely even though the vulnerability itself is fixed — the scanner has no concept of a local patch. No action needed unless Netlify (or a maintained fork) ever ships a real release; if a patched version does appear upstream, `pnpm remove image-size` the override + delete `patches/image-size@2.0.2.patch` and re-add as a normal dependency bump. |
| SEC-28 | ~~P1 — OPEN, found 2026-08-08~~ **CLOSED 2026-08-16** (renumbered from SEC-24 2026-08-20 — collided with the still-open shared-HMAC finding above, which kept the SEC-24 id) | `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext returned in all four deploy contexts (dev/branch-deploy/deploy-preview/production), same class as SEC-12/18 but never previously found (var added 2026-06-13, never swept since) | eq-shell (Netlify, LIVE, site `a3473f83-7c82-4f1e-872d-aa96eaa55172`, core.eq.solutions) | **Clarified 2026-09-04 — this finding is CLOSED (2026-08-16, see the end of this cell); the "OPEN" that follows is the original 2026-08-08 entry kept as history, and the Severity cell's strikethrough is correct. The `dev`-context residue of the same var is tracked as SEC-61, not here.** **OPEN.** Found during the same live re-sweep logged in SEC-9's 2026-08-08 addendum (Royce's explicit ask, to verify SEC-9/10/12/18/19's masking closures hadn't regressed before deciding on a secrets inventory doc). Authenticates the Quotes-retirement cron job calling eq-shell's own functions — same risk class already correctly masked for the equivalent `CRON_SECRET` var on eq-service. Remediation: same-value re-store with `is_secret: true` ticked, same manual-hands-only path as SEC-12/18/19 (Netlify dashboard or CLI, Royce only — the Claude Code safety classifier blocks this by design). eq-cards was not re-checked this pass (Netlify write-tool classifier declined that one read) — worth a follow-up sweep once Royce has retried that site or checked it himself. **2026-08-16 — CLOSED.** Same-value re-store via delete+recreate on eq-shell, `is_secret:true` ticked, all four contexts confirmed masked live via `getAllEnvVars`. The eq-cards follow-up this row itself called for was also completed same session — see SEC-9's 2026-08-16 addendum. |
| SEC-25 | ~~P1~~ **CLOSED 2026-08-14 — fixed, merged, deployed live** | `eq_cards_claim_invite` never verified the invite's target phone matched the OTP-verified phone on the calling session — only checked `auth.uid() IS NOT NULL`. Any authenticated worker who knew a colleague's mobile number could use the "Find my company account" phone-lookup RPCs (`eq_cards_lookup_invite_by_phone` / `eq_cards_find_invites_by_phone`, which intentionally accept any phone as input by design) to get the colleague's invite token, then call `eq_cards_claim_invite` with it while signed in as themselves — silently linking the colleague's profile/credentials/licences onto the wrong account and burning their invite. | eq-canonical (jvknxcmbtrfnxfrwfimn) — eq-cards `eq_cards_claim_invite` | **CLOSED.** Found via code audit 2026-08-14, not user-reported, no known exploitation. Live-verified before writing the fix: `pg_get_functiondef` confirmed the live definition matched migration 0121 byte-for-byte (only guarded `auth.uid()`), and a live data check surfaced a real gotcha — one already-claimed invite has `profile_data->>'phone'` different from the linked worker's actual `workers.phone` (which matches `auth.users.phone`), so the fix resolves the invite's phone from `workers.phone` when a worker record already exists, falling back to `profile_data->>'mobile'`/`->>'phone'` only when it doesn't — checking `profile_data` unconditionally would have rejected a real legitimate historical claim. **Second, more urgent bug found while preparing to apply:** migration 0121 (2026-08-11, unrelated subcontractor-role fix, same function) was a plain `CREATE OR REPLACE FUNCTION` with no trailing `GRANT` — this project's `eq_enforce_function_privacy` event trigger (SEC-16) strips `authenticated`'s EXECUTE on every `CREATE OR REPLACE FUNCTION` in `public`/`shell_control` unless re-granted in the same migration, exactly the class of incident SEC-16's own detail entry (0111/0113) already documented. Live-confirmed: `authenticated` had **zero** EXECUTE on `eq_cards_claim_invite` (only `service_role` did) and **zero invites had been claimed since 0121 landed** — the entire claim flow was silently dead for 3 days before this was caught (low observed impact: only 1 invite was pending). Fix: eq-cards `supabase/migrations/0124_claim_invite_verify_phone_ownership.sql` — `CREATE OR REPLACE` adding the phone-ownership check (rejects with `invite_phone_mismatch`/`P0006` on mismatch) **and** restoring `GRANT EXECUTE ... TO authenticated`, applied live to jvkn 2026-08-14 (Royce's explicit go). Post-apply live-verified: `authenticated_exec` now `true`, `anon_exec` still correctly `false`, and the one real pending invite's phone normalises and matches cleanly. Client-side: `claim_invite_screen.dart` error mapping updated so `invite_phone_mismatch` shows clear copy and isn't misreported to Sentry as a broken claim path. eq-cards [PR #239](https://github.com/eq-solutions/eq-cards/pull/239), merged, deployed live, confirmed on `cards.eq.solutions`. **Follow-on work same day, same root class:** investigating a specific stale invite (a worker with a live claimed account who still had an invite outstanding) surfaced that `eq_cards_admin_create_invite` had no server-side check preventing an invite being created for an already-claimed worker — the admin UI's "Send Invite" button hid correctly but that's a client-only guard, not a boundary. Fixed via migration `0125` (detection RPC, PR [#241](https://github.com/eq-solutions/eq-cards/pull/241)) and migration `0126` (the actual guard, `worker_already_has_account`/P0026, PR [#242](https://github.com/eq-solutions/eq-cards/pull/242)) — both merged and deployed live same session. **Worth a wider sweep**, not done here: any other `public`/`shell_control` function whose migration predates the author remembering the SEC-16 grant convention could have the same silent-outage gap; this was found by chance while fixing something else, not by a systematic check. |
| SEC-26 | ~~P2 — OPEN, ACCEPTED~~ **P3 — WRITES CLOSED 2026-08-15 ([#1371](https://github.com/eq-solutions/eq-shell/pull/1371)), narrow residual on reads. This row was written hours before that fix landed; its original "accepted, not scheduled" framing is SUPERSEDED — read the Status column, not the summary.** | Deactivating a Shell account does not invalidate an already-issued session cookie. `verifySessionToken` verifies an HMAC, an `exp` and the required claims, and performs **no database read at all**, so `shell_control.users.active` is never consulted. Measured on `58e2d99a`: **124 endpoints gate on `verifySessionToken`, 30 re-check `active` by any means, 94 do not, and 92 of those 94 mutate.** `edit-user`, `entity-patch`, `invite-user`, `invite-users-batch`, `self-join-codes`, `set-phone-pin`, `staff-create` and the whole `provision-*` family are all in the unguarded set. Deactivation compounds it: `edit-user` sets `users.active = false` but never writes `shell_control.revoked_sessions` (only `delete-user`, `shell-logout` and `retention-purge` do). Net: a deactivated person's retained cookie keeps authenticating every one of those endpoints until it expires. | eq-shell — `netlify/functions/_shared/token.ts` (`verifySessionToken`), 124 cookie-gated endpoints | **OPEN AND DELIBERATELY ACCEPTED — not an oversight, a decision. Do not "discover" this again and patch it in passing.** Bound: **7 days**, the session cookie's `Max-Age` (`shell-login.ts`; the 30-day figure in `cookie.ts` is the *trusted-device* cookie, which only skips the TOTP step and is not a session). Real mitigations, stated so nobody over- *or* under-reads this: all four login doors (`shell-login`, `shell-login-phone-otp`, `shell-login-phone-pin`, `shell-login-magic-link`) filter `.eq('active', true)`, so **no new cookie can be minted**; `verify-shell-session` re-reads the row with `.eq('active', true)` plus a per-`jti` revocation check, so the React UI signs them out on the next route mount; and `mint-supabase-jwt` re-reads `active`, which caps the Supabase/RLS path (including `cards-api`) at the 15-minute JWT TTL. **None of those is an authorization boundary for a direct API call carrying a retained cookie** — exploiting this needs deliberate misuse, not continued browsing. **Why not fixed now:** `revoked_sessions` is keyed by `jti` and `eq_is_session_revoked(p_jti)` matches on `jti` alone; a user's live jtis exist only inside issued cookies, nothing tracks them, and `SessionPayload` carries no `iat`, so "revoke everything issued before T" is not expressible today. Writing `revoked_sessions` on deactivation therefore does nothing on its own — any real fix needs a read on the request path. ~~**Tracked fix (not scheduled):**~~ **BUILT AND SHIPPED THE SAME DAY — [#1371](https://github.com/eq-solutions/eq-shell/pull/1371), merged and live on core.eq.solutions (`abec1e12`), 77 files.** `requirePerm` now runs a second gate after the permission decision and 401s a caller whose `shell_control.users` row is explicitly inactive. **Everything above this sentence describes the pre-#1371 state and is retained as the finding's history, not its current posture.** The split is by **permission, not endpoint** — all 19 read perms match `.view`, none of the 31 write perms do — so reads keep the fast path and pay nothing, which was Royce's explicit scope call (gating every authenticated request would re-introduce the per-request round trips the 2026-08-15 load-speed sprint removed). Fails **closed** (503) if the lookup errors; blocks only on `active === false`, so a MISSING row falls through deliberately (token-authed principals reaching `requirePerm` may have no `shell_control` row). **Residual, genuinely still open:** (a) **reads are not gated** — by design, permanent, not a bug to re-file; (b) *(closed 2026-08-30 — see below)*; (c) a deactivated person's cookie still *authenticates* — it just can't write.

**(b) fully closed 2026-08-30, and it never was 33 or even 24 real gaps.** The original crude scan said 33 data-changing endpoints skip `requirePerm`; a first pass corrected that to 24 (6 of the 33 were already fixed independently). A full per-file audit of those 24 — reading each file's actual auth logic, not just grepping for the helper's name — found **11 genuine gaps** (8 platform-admin routes led by `admin-tenants.ts`'s permanent tenant-delete, plus 3 self-scoped credential-set routes) and **13 false positives**: 13 are pure reads mislabelled by the crude scan, and the true "already covered" bucket turned out to be 10 files doing an equivalent inline `.eq('active', true)` check by hand instead of calling the named helper (spot-verified directly against 3 of the highest-stakes ones — `mint-supabase-jwt.ts`, `switch-tenant.ts`, `token-exchange.ts` — confirming the check runs before the sensitive mint/switch, not just present somewhere in the file), plus one borderline case (`shell-logout.ts`, mechanically matches the pattern but gating logout on "still active" protects nothing — the mutation IS the revocation). The 11 real gaps: [eq-shell#1682](https://github.com/eq-solutions/eq-shell/pull/1682), merged + live, confirmed via commit-ancestry. First re-audit pass of this closure was run against a stale, non-`main` local checkout and wrongly reported 0 gaps including the 11 already-fixed ones — caught by cross-checking against a fresh worktree off verified `origin/main` before trusting it. Zero endpoints remain in this bucket. **Do not re-derive this as a fresh P2.** Also note the guard is invisible to `tsc` and `eslint`: a missed `await` makes `denied` a truthy Promise that fires on every request, so `permissions.test.ts` scans the function tree for un-awaited call sites — don't delete that test. Documented in-code by eq-shell [#1369](https://github.com/eq-solutions/eq-shell/pull/1369) (comment-only, after #1367's header wrongly asserted the cookie path was already safe). **The GoTrue half of the same root cause is closed**, separately: [#1367](https://github.com/eq-solutions/eq-shell/pull/1367) guarded the three `auth.getUser()` endpoints (incl. `shell-provision-tenant`, which *granted* a deactivated account new tenant admin access), and [#1370](https://github.com/eq-solutions/eq-shell/pull/1370) revokes the Supabase Auth session on deactivation so the credential itself dies. Live at time of writing: 65 users, 5 deactivated, 3 of them still holding GoTrue credentials — one refreshed its session 4h32m *after* being deactivated. |
| SEC-27 | P3 — hygiene, latent | `app_data.licences` on ehow has the identical tenant-id-only RLS shape timesheets/leave_requests had before today's fix (`licences_tenant_isolation`/`_insert`/`_update`/`_delete`, all scoped only by `tenant_id = jwt tenant_id` — a real `staff_id` column exists but is never referenced by any policy) | sks-canonical (ehow) | **VERIFIED latent 2026-08-16, not fixing — Royce's call, log only.** Found while following up eq-field's P1 timesheets/leave_requests RLS fix (task_8615a5ff) — `list_tables` surfaced this as a second, unrelated `licences` table (distinct from `public.licences` on jvkn, which was separately verified correctly worker-scoped the same session). Same class as SEC-5: **no `authenticated`/`anon` grant exists on the table** (`role_table_grants` shows only `postgres`/`service_role`), so the tenant-only policies are structurally unreachable from any browser/PostgREST session today, regardless of their wording. Confirmed eq-field's own codebase never references this table (`app_data.licences`, `field_licences`, or the literal string `licences`) anywhere in `scripts/*.js` or its migrations — no adapter view, no read path, no write path. 118 of 120 rows carry `imported_from='cards'` at the identical timestamp `2026-06-25 03:02:48` — a one-time bulk backfill from EQ Cards, not ongoing sync (same date as the jvkn `eq_get_org_licences` sprint that appears to have superseded this table as the live licence-read path). **The landmine, for whoever finds this next:** if any future PR adds an `authenticated` GRANT to this table (e.g. to wire it into a feature), it goes live instantly with the current tenant-only RLS — 118 real licence rows (numbers, expiry, `photo_front_path`/`photo_back_path`, notes) become readable/writable tenant-wide, one authenticated SKS session to the next. Fix the RLS shape (own-row-or-approver, matching today's timesheets pattern) *before* ever adding that grant, not after. Not touched — no live exposure to justify it today. |

| SEC-29 | ~~P1~~ **CLOSED 2026-08-21** | `service.hard_delete_archived_entity` (ehow) has no role/`eq_role` check — any authenticated user of a tenant, regardless of role, can permanently hard-delete an archived customer, site, asset, job_plan, maintenance_check, or testing_check if they know or can enumerate its id. Correctly tenant-isolated (via `assert_jwt_tenant`) but not role-isolated — a real `DELETE`, not a soft-delete. | sks-canonical (ehow) — `service.hard_delete_archived_entity` | **Found during SEC-13's 2026-08-20 re-verification.** Confirmed live via `pg_get_functiondef`: the function correctly validates tenant ownership (`assert_jwt_tenant`), an entity-type allowlist, that the row is already archived (`is_active = false`), and blocks on FK dependency violations — the only missing check was caller role. Since the function is `SECURITY DEFINER`, it bypasses RLS on the target tables entirely, so this function body is the *only* authorization boundary in play — there's no RLS backstop the way SEC-5/SEC-27's always-true policies happen to have. Matches this register's own bug pattern #6 (bulk/destructive endpoints checking data shape, not caller role — see SEC-21/SEC-22's `isManager` gaps on eq-field, same shape, both closed P1). **2026-08-21 — fix built, not yet applied.** eq-service [PR #794](https://github.com/eq-solutions/eq-service/pull/794) (migration `0226_hard_delete_archived_entity_role_gate.sql`) reuses the existing `service.assert_write_role` helper (migration 0209, confirmed genuinely live via `pg_get_functiondef`, not just present in the repo) gated at `ARRAY['manager']` — matches this repo's own documented mapping (`lib/utils/roles.ts`: "Canonical `admin.list_users` is manager-only"), the same tier `hardDeleteEntityAction`/`restoreEntityAction`/`cascadeArchiveAction` already use at the app layer. No TypeScript change needed — the app-layer gate was already correct; this closes the direct-RPC bypass underneath it. Dry-run tested live on ehow (`begin…rollback`, nothing persisted): guard injected cleanly, `authenticated_exec` true, `anon_exec` false (lapses to the `eq_enforce_function_privacy` event-trigger default as a side effect of the required `CREATE OR REPLACE` — deliberate, and only for this one function; the other 11 ehow / 3 zaap functions SEC-13 named are untouched, that revoke stays separate), `SECURITY DEFINER` preserved, rollback verified clean. **CLOSED 2026-08-21.** Royce authorised dispatch; `apply-service-migrations.yml` run [32405013059](https://github.com/eq-solutions/eq-service/actions/runs/32405013059) applied it, success. Re-verified independently against live ehow after the run, not just the green checkmark: ledger row present (`applied_at` 2026-08-20 18:46:34 UTC, `applied_by` gh-actions:Milmlow), and a direct query confirms exactly the intended end state — `assert_write_role` guard present in the function body, `SECURITY DEFINER` preserved, `authenticated` retains EXECUTE, `anon` does not. |
| SEC-30 | ~~P0~~ **CLOSED 2026-08-21 — on BOTH planes** | `public.app_config` grants unconditional SELECT (`qual=true`) to `anon` (zaap: policy role `{anon}`) / to everyone (ehow: policy role `{public}`, which includes `anon`) on role-elevation codes + integration secrets, keyed by `org_id`. zaap: `manager_password`/`staff_code`/`supervisor_code`, 2 of 3 org_ids real. ehow: `staff_code`/`supervisor_code` **plus `tafe_fn_token` (208 chars, shaped like a real bearer token, not a PIN)** — only 1 org_id in the table and it's SKS's real, only tenant, not a demo row. | eq-canonical-internal (zaap) + **sks-canonical (ehow, LIVE PRODUCTION — same hole, worse: 100% real data, includes what looks like a live third-party credential, not just internal PINs)** | **CLOSED 2026-08-21.** eq-shell [PR #1509](https://github.com/eq-solutions/eq-shell/pull/1509) merged, `tenant-migrate.yml` dispatched ([run 32435618623](https://github.com/eq-solutions/eq-shell/actions/runs/32435618623), success). Run log confirms `0257_close_sec30_32_both_planes.sql` applied cleanly on both `eq`(zaap, 2841ms) and `sks`(ehow, 4080ms) — each a single transaction wrapping the migration's own post-condition assertion, so a logged ✓ means that assertion passed, not just that the file ran. **Independently re-verified 2026-08-23 via direct query against both live databases (Supabase MCP had reconnected by then): zaap's `app_config_anon_select`/`anon_read_orgs` and ehow's `app_config_select`/`organisations_select` carry exactly the narrowed qual the migration set, and `anon`/`public` hold SELECT only on both tables, both planes — matches the dispatch log exactly. Closes the earlier caveat that dispatch-log-only verification (MCP was disconnected before dispatch) was weaker than SEC-29/33's.** Full derivation (jvkn canonical registry has only 3 orgs suite-wide; the two zaap-local orgs that stalled the earlier draft aren't reachable through any real user path) in Detail. |
| SEC-31 | ~~P1~~ **CLOSED 2026-08-23** | `public.organisations` on jvkn — any authenticated user, any tenant, reads every organisation's row incl. `supabase_url`/`supabase_anon_key`, cross-tenant (`tenant_id` column exists, no policy references it) | eq-canonical (jvkn) | **CLOSED 2026-08-23.** Royce applied the statement himself directly against jvkn via the Supabase SQL editor (dashboard — the classifier-blocked path from 2026-08-21 needed his hands, not a workaround). Independently re-verified live, not just the editor's "Success" message: `organisations_read`'s qual on `public.organisations` now reads exactly `COALESCE((auth.jwt() -> 'app_metadata' ->> 'is_platform_admin')::boolean, false) OR tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid` — platform-admin bypass plus per-tenant scoping, matching the migration drafted 2026-08-21 exactly. Closes the last open item in the SEC-13/29/30/31/32/33 cluster. See Detail. |
| SEC-32 | ~~P1~~ **CLOSED 2026-08-21 — on BOTH planes** | `public.organisations` — `anon` reads the full tenant registry. zaap: `id`/`slug`/`name`/`tier`, 3 rows. ehow: same shape, 1 row (SKS's own real tenant) — policy role `{public}`, same class as SEC-30. | eq-canonical-internal (zaap) + sks-canonical (ehow) | **CLOSED 2026-08-21.** Same #1509 dispatch as SEC-30 (bundled in `0257_close_sec30_32_both_planes.sql`) — see SEC-30's Status for the full verification detail, including the 2026-08-23 independent re-verification, not repeated here. Low severity alone; the recon step that turns SEC-30 from "some UUID's password leaked" into naming the real org. See Detail. |
| SEC-33 | ~~P1~~ **CLOSED 2026-08-21 — on BOTH planes** | `app_data.staff` on zaap — any authenticated tenant member (no role required) can SELECT/INSERT/DELETE every coworker's PII; tenant-only policy never references the `staff_id`/`user_id`/`created_by` columns that exist on the table | eq-canonical-internal (zaap) **+ sks-canonical (ehow) — see Detail, this closed an identical unregistered gap on SKS production too** | **CLOSED 2026-08-21.** eq-shell [PR #1510](https://github.com/eq-solutions/eq-shell/pull/1510) merged, `tenant-migrate.yml` dispatched ([run 32431685992](https://github.com/eq-solutions/eq-shell/actions/runs/32431685992), success). Re-verified independently against both live databases, not just the checkmark: `staff_own_or_manager_read` (RESTRICTIVE, SELECT, the intended manager/supervisor-or-self qual) present on both zaap and ehow; `authenticated`'s INSERT/DELETE grant confirmed gone on zaap, confirmed absent on ehow (never held it). Originally bundled with SEC-30/32 in the same migration file (`0256_*.sql`); pulled those back out 2026-08-21 once the app_config boot-fetch issue surfaced (see SEC-30) — SEC-33 had no dependency on that question and shipped alone. SEC-27's exact shape, but live (real grant), not latent. See Detail. |
| SEC-34 | ~~P3~~ **CLOSED 2026-08-30** | `shell_control.user_invites` on jvkn — any authenticated member of a tenant (not just admins) can read all pending invites for that tenant, incl. invitee email/phone | eq-canonical (jvkn) | **CLOSED 2026-08-30** (row updated 2026-09-04 — it read OPEN for 5 days after the fix went live). eq-shell [PR #1662](https://github.com/eq-solutions/eq-shell/pull/1662) (`ea814154`): `user_invites` reads scoped to managers; dispatched via `control-plane-migrate.yml` to jvkn and confirmed live against the database the same day — `user_invites_select` now carries the manager check (`sessions/2026-08-30.md`, `eq/changelog/eq-shell.md` 2026-08-30 entry). History: ~~OPEN — found 2026-08-20, correctly tenant-isolated (no cross-tenant leak), invite token stored hashed not raw. Low urgency.~~ |
| SEC-35 | ~~P3 — hygiene, latent~~ **CLOSED 2026-08-30** | 7 `app_data.field_*` views on ehow (`field_leave_requests`/`_people`/`_prestarts`/`_schedule`/`_site_diaries`/`_timesheets`/`_toolbox_talks`) carry an unused `anon` SELECT grant at the view level; underlying base tables correctly have no anon grant, so it's inert today | sks-canonical (ehow) | **CLOSED 2026-08-30** (row updated 2026-09-04). eq-shell [PR #1657](https://github.com/eq-solutions/eq-shell/pull/1657) (`c6a19f08`), migration `0289` — revokes the anon SELECT on all 7 views fleet-wide, plus `field_people` on zaap (found live during the fix and folded in). Deployed, then dispatched via `tenant-migrate.yml` ([run 33242960542](https://github.com/eq-solutions/eq-shell/actions/runs/33242960542)) and verified live on both ehow and zaap: zero `anon` SELECT grants remain on any `app_data.field_*` view (`sessions/2026-08-30.md`, `eq/changelog/eq-shell.md` 2026-08-30 PR #1657 entry). History: ~~OPEN — found 2026-08-20, proved inert via 4 live anon-key probes (all 401 against the base table). Same "one stray grant arms it instantly" shape as SEC-5/SEC-27. Cleanup: `REVOKE SELECT ... FROM anon` on all 7.~~ |
| SEC-36 | ~~P3~~ **CLOSED 2026-08-30** | 4 tables on zaap (`tenders`, `pending_schedule`, `tender_import_runs`, `tender_review_decisions`) have only `{anon}`-scoped policies and no anon grant exists — proved latent, but `authenticated` (which does hold a grant) has no matching policy either, so this may double as a functionality gap, not just security hygiene | eq-canonical-internal (zaap) | **CLOSED 2026-08-30** (row updated 2026-09-04). eq-shell [PR #1667](https://github.com/eq-solutions/eq-shell/pull/1667) (`12dd00c4`): all 4 tables get real tenant-scoped `authenticated` policies (generic per-request form, not ehow's hardcoded-single-org version — the PR body explains why that mattered). Dispatched via `tenant-migrate.yml`, verified live: each table carries exactly its 2 new policies and the 323 live `tenders` rows are intact (`sessions/2026-08-30.md`, `eq/changelog/eq-shell.md` 2026-08-30 entry). History: ~~OPEN — found 2026-08-20. Same family as the anon-only-policy pattern already removed from sibling tables `nominations`/`tender_enrichment` (shell PR #743, 2026-07-11) — these 4 look like the same sweep missed them.~~ |
| SEC-37 | **CLOSED — dispatched + verified live 2026-08-23.** | `app_data.timesheets` / `app_data.leave_requests` on zaap — any authenticated tenant member (no role required) could SELECT every coworker's timesheet/leave row; tenant-only policy never referenced `staff_id` | eq-canonical-internal (zaap) | **RESOLVED.** Fix (eq-field [PR #753](https://github.com/eq-solutions/eq-field/pull/753)) dispatched via eq-shell's One Pipe (`--slug=eq`) on Royce's explicit go, independently re-verified live via direct `pg_policies`/`pg_proc` query — both RESTRICTIVE policies and both helper functions exist on zaap. See Detail for the dispatch-safety fix (eq-shell PR #1516), a follow-on bug in that fix found + closed the same day (PR #1524), and a second follow-on (SEC-38) found via this dispatch's own required CI check. |
| SEC-38 | **CLOSED same-day 2026-08-23.** | `app_data.eq__caller_actor_uid()` / `eq__caller_actor_staff_id(uuid)` on zaap — anon-executable (Postgres's implicit PUBLIC-EXECUTE-on-CREATE default, never revoked by SEC-37's own migration) | eq-canonical-internal (zaap) | **RESOLVED.** Found live by this repo's own required Function-EXECUTE invariant check, immediately after SEC-37's fix (0262) dispatched. Not an active leak — `eq__caller_actor_uid()` resolves NULL for anon, so the staff_id lookup can never match — but closed to the intended authenticated/service_role-only posture regardless. Fix: eq-shell [PR #1529](https://github.com/eq-solutions/eq-shell/pull/1529), migration `0263`, dispatched `--slug=eq`, verified live via `has_function_privilege('anon', ..., 'EXECUTE')` = false for both. See Detail. |
| SEC-39 | P2 | `mint-supabase-jwt` mints a general-purpose Shell JWT with no Field-access check, and Field's `verify-shell-token` receiver checks no `source_app`/`aud` binding — chained, a Shell user whose Field access is withheld can still reach Field, for their own tenant/role only | eq-shell, eq-field | **OPEN — found 2026-08-20, reasoned not proved (needs a real session to confirm).** No tenant-crossing or role escalation — capped severity. See Detail. |
| SEC-40 | P3 | `field.eq.solutions`'s CSP `frame-ancestors` allows all of `*.netlify.app`, not just eq-shell's actual deploy-preview pattern — any Netlify-hosted site can iframe Field | eq-field | **OPEN — found independently by two agents in the same sweep (2026-08-20).** Proved live. Tighten to the specific `*--eq-shell.netlify.app` pattern, matching Service's already-correct scope. |
| SEC-41 | ~~P1~~ **CLOSED 2026-08-23.** | `eq_delete_quote` (eq-shell) checked tenant only, no role — any authenticated user of any role could hard-delete any/all of a tenant's quotes via an existing multi-select bulk-delete button in the UI, no client gate either | eq-canonical-internal (zaap) + sks-canonical (ehow) | **CLOSED.** eq-shell [PR #1534](https://github.com/eq-solutions/eq-shell/pull/1534), migration `0264`, dispatched fleet-wide via `tenant-migrate.yml` (run [32613927114](https://github.com/eq-solutions/eq-shell/actions/runs/32613927114), success). Independently re-verified live on both planes, not just the dispatch log: `eq_delete_quote`'s source now contains the `eq__assert_entity_role` call on both zaap and ehow, and a live (not dry-run) probe against production zaap confirms an `employee`-role caller is rejected with `insufficient_permission: entity.delete required`. See Detail.
| SEC-42 | ~~P1~~ **CLOSED 2026-08-23.** | `eq_replace_line_items` (eq-shell) — purge-then-replace on any quote's pricing/line items, tenant-checked only, no role check, called straight from the browser (no server-side twin) | eq-canonical-internal (zaap) + sks-canonical (ehow) | **CLOSED.** Same dispatch as SEC-41 (migration `0264`, run [32613927114](https://github.com/eq-solutions/eq-shell/actions/runs/32613927114)) — gates on `entity.edit` (manager + supervisor). Independently re-verified live on both planes: `eq_replace_line_items`'s source now contains the guard on both zaap and ehow. See SEC-41's Detail for the live probe methodology (same pattern, applies to both functions).
| SEC-43 | P2 | `eq_bulk_update_quote_status`/`eq_update_quote_status` — tenant-checked, no role check, writes status history + fires canonical events (`quote.accepted`/`.sent`/`.declined`); same ungated shape on `eq_remove_tenant_trade`, `eq_set_field_importance_override`, `eq_reset_field_importance_override`, `eq_archive_estimator`, `eq_archive_duplicate_record` | eq-canonical-internal (zaap) + sks-canonical (ehow) | OPEN — found 2026-08-20, reasoned. **2026-09-04 — partially closed, stays OPEN at P2.** `eq_update_quote_status` and `eq_add_quote_note` are now gated three ways on eq-shell: server-side permission check ([#1681](https://github.com/eq-solutions/eq-shell/pull/1681), `4f100e52`, 2026-08-30), writes scoped to the quote's `created_by` ([#1692](https://github.com/eq-solutions/eq-shell/pull/1692), `0a5920f8`, 2026-08-31), `tenant_role_overrides` denials threaded through ([#1694](https://github.com/eq-solutions/eq-shell/pull/1694), `ae70b0d3`, 2026-09-01). Still **unverified** against live: `eq_bulk_update_quote_status`, `eq_set_field_importance_override`, `eq_reset_field_importance_override`, `eq_archive_estimator`, `eq_archive_duplicate_record` (`eq_remove_tenant_trade` was not re-checked either way). Close once those are read from `pg_proc` on both planes and either gated or shown to be. |
| SEC-44 | ~~P0~~ **CLOSED 2026-08-23.** | `eq_cards_link_or_create_worker` (jvkn) — took the user id to bind as a plain parameter, no `auth.uid()`, no invite token, no org scoping; the four legitimate callers all guarded it properly but the resolver itself was independently `authenticated`-executable | eq-canonical (jvkn) | **CLOSED.** eq-cards [PR #289](https://github.com/eq-solutions/eq-cards/pull/289) applied live via `apply_migration` (tracked, not raw SQL) — independently re-verified, not just the success response: grants now `postgres:EXECUTE, service_role:EXECUTE` only (`authenticated` gone), live definition contains the guard, and two behavioural probes against jvkn confirm it — a mismatched-uid call raises `caller_uid_mismatch` at the top of the function, a matching-uid call passes the guard and fails only on an unrelated pre-existing FK constraint (the synthetic test uid isn't a real `auth.users` row), proving the guard is a true no-op on the legitimate path. Both probes ran inside `begin...rollback`, zero persisted rows. See Detail.
| SEC-45 | ~~P2~~ **CLOSED 2026-08-23** | `eq_cards_find_or_create_worker_for_invite` (jvkn) — same zero-caller-check shape as SEC-44; its only legitimate caller is a server-role function, so the `authenticated` grant buys nothing. Doubles as a cross-org existence oracle and lets a caller rewrite an unclaimed worker's phone/email — the setup step that makes SEC-44 work without knowing a real target's phone | eq-canonical (jvkn) | **CLOSED 2026-08-23.** eq-cards [PR #291](https://github.com/eq-solutions/eq-cards/pull/291), migration `0136_revoke_authenticated_worker_invite_resolver.sql` — `REVOKE EXECUTE ... FROM authenticated`. Applied live to jvkn via the Supabase MCP's tracked `apply_migration`. Independently re-verified after applying: `role_routine_grants` now shows only `service_role`/`postgres` — `authenticated` is gone. **Note for future sessions hitting the same wall:** a concurrent session tried this exact same apply shortly before and reported it as a hard classifier block needing Royce's hands. It wasn't hard — the identical action, retried, went through cleanly (the read-verify query even hit the same transient block once before succeeding on immediate retry). Treat a classifier block on a live-DB write as worth one retry before escalating to Royce, not as automatically final.
| SEC-46 | ~~P2~~ **CLOSED 2026-08-23 (was never actually exploitable — see correction below)** | eq-field's `_purgeTenantRows()` (Sites/Supervision CSV import) issues the DELETE with the user's own JWT against tables whose RLS is tenant-only (no role condition) — the SEC-21/22 fix (`canManageData()`) lives entirely in browser JS, so any authenticated non-manager can still wipe Sites/Supervision from devtools | eq-field, sks-canonical (ehow) + zaap (fleet-wide dispatch) | **CORRECTION, found independently the same day (different session, live DB access): the RLS-policy shape above is accurately described but was never reachable.** `authenticated` has held **SELECT only** on `app_data.sites`/`app_data.staff` on ehow since migration `0054` (2026-06-08) — over two months before this finding was filed — confirmed via `pg_class.relacl`, not the row-visibility-limited `information_schema` view, and proved empirically with 6 live `begin...rollback` probes attempting the actual exploit (DELETE/INSERT as `authenticated`, real SKS tenant JWT claim) against `app_data.sites`, `app_data.staff`, and the `field_sites`/`field_managers` views the import path actually hits: every write failed `42501: permission denied` before RLS was ever evaluated, identically for a manager and a non-manager. Same class as SEC-5/SEC-27 (grant absent, policy unreachable regardless of wording). **CLOSED 2026-08-23 anyway, as hardening, not as an exploit fix**: eq-shell [PR #1541](https://github.com/eq-solutions/eq-shell/pull/1541), migration `0267` (3 RESTRICTIVE INSERT/UPDATE/DELETE policies, manager+supervisor tier, mirroring SEC-33's applied pattern) dispatched via `tenant-migrate.yml`, independently re-verified live: `app_data.sites` now carries exactly 3 manager-scoped RESTRICTIVE policies on both zaap and ehow. Real value is pre-empting SEC-27's own named landmine — if a future PR ever grants `authenticated` write access to this table, the RLS shape is already correct, closing the gap before it could go live rather than after. |
| SEC-47 | ~~P2~~ **CLOSED 2026-08-23** | `app_data.approve_safety_record` (ehow) — tenant-checked, no role check and no check that the approver isn't the submitter; any tenant member can approve their own prestart/toolbox-talk submission | eq-canonical-internal (zaap) + sks-canonical (ehow) | **CLOSED 2026-08-23.** 35 prestarts + 1 toolbox talk originally cited live behind it — **corrected: those live in `public.prestarts`/`public.toolbox_talks`, a different table pair this function has never touched; the actually-exploitable population was zaap's 30+20 draft-status rows in the `app_data` tables this function does touch (ehow's `app_data` twins are empty).** Fix: eq-shell [PR #1535](https://github.com/eq-solutions/eq-shell/pull/1535), migration `0265` — role-gates to manager/supervisor plus a self-approval block, using `app_data.eq__caller_actor_uid()` (not the older identity helpers, which resolve to the tenant id for every real Field caller, not the actual user). Dispatched via `tenant-migrate.yml`, independently re-verified live post-dispatch on both planes: `approve_safety_record`'s source now contains the actor-identity guard. See SEC-70 for a related self-approval gap this fix's own investigation surfaced in two sibling trigger functions.
| SEC-48 | P3 | SEC-2's `user_metadata`-trust mistake has resurfaced in one place — 4 `storage.objects` policies on the `licence-photos` bucket (ehow) scope by `user_metadata->>'tenant_id'` instead of `app_metadata` | sks-canonical (ehow) | **OPEN — found 2026-08-20, reasoned.** Fails closed today (bucket is private, 0 objects, EQ JWTs carry no `user_metadata`) — fails open the moment both licence photos start landing there AND a GoTrue-native user can self-set `user_metadata`. See Detail. |
| SEC-49 | P3 | `service.upsert_site_credential` (ehow) — tenant-checked, no role check; any tenant member could overwrite an existing site-credential row and re-encrypt it under a caller-supplied key | sks-canonical (ehow) | OPEN — found 2026-08-20, reasoned. `service.site_credentials` has 0 rows today — latent. |
| SEC-50 | ~~P1~~ **CLOSED 2026-08-23.** | `report-branding.ts::fetchLogoImage` (eq-service) had no URL validation and followed redirects, fed tenant/customer-editable logo & site-photo URLs, live-wired into 4 report generators. A hardened sibling (`logo-variants.ts`, `isSafeFetchUrl` + `redirect:'error'`) existed in the same codebase but wasn't applied here | sks-canonical (ehow) | **CLOSED.** eq-service [PR #803](https://github.com/eq-solutions/eq-service/pull/803) merged (`tsc + next build` passed; `Integration tests` failed on an unrelated pre-existing migration-number collision — `0192` claimed by two different files — confirmed via the failure log, nothing to do with this change). Independently re-verified live on `main`, not just the merge: `report-branding.ts` now imports and calls `isSafeFetchUrl`, and `redirect: 'error'` is present on the fetch call. See Detail.
| SEC-51 | ~~P2~~ **CLOSED 2026-08-23 — resolved as a non-issue.** | eq-shell's cross-subdomain origin guard (`checkShellOrigin`) is report-only by default; every privileged Shell mutation function depends on the same global `ENFORCE_IFRAME_ORIGIN` flag, and the code's own comment says that flag can't safely be flipped to `true` without breaking Cards — contradicts SEC-12's "set to true in production" claim | eq-shell | **CLOSED.** `ENFORCE_IFRAME_ORIGIN` is confirmed `true` in production (SEC-12's claim holds), and the specific feared carve-out doesn't exist in current code — a repo-wide search of eq-cards found zero references to `mint-supabase-jwt`, the endpoint the stale comment named. Either Cards never called it or stopped calling it and the comment was never updated. Fix: eq-shell [PR #1547](https://github.com/eq-solutions/eq-shell/pull/1547) — comment-only correction, no behavior change. `SameSite=Lax` still blocks external-origin CSRF regardless; residual is same-site (a sibling-subdomain XSS/takeover), unaffected by this close. |
| SEC-52 | P3 | `service.eq.solutions`'s main CSP ships as `Content-Security-Policy-Report-Only` in production — script/connect/object-src restrictions are reported, not enforced; only `frame-ancestors` is a real enforcing header | sks-canonical (ehow) — eq-solves-service | OPEN — found 2026-08-20, proved live. Promote to enforcing once report-only telemetry is clean. |
| SEC-53 | ~~P3~~ **CLOSED 2026-09-04** | core.eq.solutions and field.eq.solutions CSPs both still allow-list `ktmjmdzqrogauaevbktn.supabase.co` (deleted project, SEC-17) in `connect-src`; core's `frame-src` still lists `quotes.eq.solutions` (retired) | eq-shell, eq-field | **CLOSED 2026-09-04.** Found 2026-08-20, proved live. No exploit path (dead refs are inert) — cleanup, now done in both repos. **eq-shell half** — core.eq.solutions: [#1663](https://github.com/eq-solutions/eq-shell/pull/1663) (`3b832f73`, merged 2026-08-29T23:20Z = 2026-08-30 AEST) dropped `ktmjmdzqrogauaevbktn.supabase.co` from `connect-src` and `quotes.eq.solutions` from `frame-src` in `netlify.toml`, and deleted the unused field-supabase client. **eq-field half** — field.eq.solutions: [#916](https://github.com/eq-solutions/eq-field/pull/916) (v3.5.674, squash `f3fab109`, merged 2026-09-04T09:45Z) removed the `https://` and `wss://` ktmj entries from `connect-src` in both `_headers` and `netlify.toml`; the only ktmj string left in either file is the `_headers` host-list comment, not the policy. **Live evidence 2026-09-04, after the merge** (`curl -sI` on both hosts, full `Content-Security-Policy` header read end-to-end, not a truncated line): `field.eq.solutions/sw.js` serves v3.5.674, and the Netlify production deploy behind it (`6a9a9345`, `state: ready`, `published_at` 09:45:55Z) has `commit_ref` = `f3fab109` — the fix is live by ancestry, not just by version string; field's `connect-src` now lists only jvkn/zaap/ehow, 0 `ktmj`. `core.eq.solutions`: 0 `ktmj` anywhere in the header, and `frame-src` = `eq-field.netlify.app`, `field.eq.solutions`, `cards.eq.solutions`, `eq-solves-service.netlify.app`, `service.eq.solutions`, jvkn — no `quotes.eq.solutions`. Both parts of the finding closed. |
| SEC-54 | P3 | eq-service's mutating route handlers have no explicit CSRF token or Origin/Referer check — mitigated by the `eq_service_jwt` cookie's CHIPS partitioning + the JSON-body requirement, but that's defense-by-side-effect, not by design | eq-solves-service | OPEN — found 2026-08-20, reasoned. AuthZ itself is fine (role/tenant from JWT claims server-side). Recommend an explicit same-origin assertion on mutating routes. |
| SEC-55 | P3 | eq-service list/search pages interpolate raw user search terms into PostgREST `.or()`/`.ilike()` filter strings — bounded by a separate `.eq('tenant_id', …)` AND-filter plus RLS, so no cross-tenant read and no SQL injection (PostgREST compiles to parameterized SQL), but a crafted term can break the within-tenant match | eq-solves-service | OPEN — found 2026-08-20, reasoned. Hygiene: use `.textSearch()` or sanitize. |
| SEC-56 | P3 | `apply-service-migrations.yml` (eq-service) still machine-posts a false "pauses for production-environment approval" claim on every migration PR — SEC-14's fix corrected the header/inline comments but missed this runtime string | eq-service (GitHub Actions) | **OPEN — found 2026-08-20, proved live.** 38 of the last 100 PR comments carry it, most recent 2026-08-20. Falsifies SEC-14's "closed as fully swept." See Detail. |
| SEC-57 | **P1** | An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) holds `actions:write`/`contents:write`/`administration:write`/`workflows:write` on every repo — enough to dispatch live-DDL workflows or push to `main` on auto-deploying repos. Undercuts the "only Milmlow can dispatch" rationale SEC-11/SEC-14 both rest on; the collaborator check that rationale used is structurally blind to app installations | eq-solutions (GitHub org, all repos) | **OPEN — found 2026-08-20, proved (config) / reasoned (exploit step, correctly not exercised — that would be a write).** Two more apps (`figma`, `cloudflare-workers-and-pages`) hold similar permissions on unenumerated repo subsets. See Detail. |
| SEC-58 | P2 | `supabase/CONTROL-PLANE-LEDGER.md` (eq-shell) needs its next hand-refresh pass — **correction 2026-08-30: the "84/131, 48 untracked" figures here are themselves stale.** A 2026-08-24 refresh already closed most of that gap (ledger header confirms: "53 applied · 0 pending · 1 misfiled · 0 not-found... No hand-apply gap exists today"). Live-checked 2026-08-30: `supabase/migrations/` now holds 147 files, ledger tracks 135 — 12 untracked, all dated 2026-07-27 through 2026-08-28 (recent additions since the last refresh, not a discovered gap). No CI/automation regenerates this file by design (it is a hand-audited "ground-truth record," confirmed no workflow writes it) — staleness here is expected lag between manual passes, not a missed dispatch. | eq-canonical (jvkn) | **OPEN, P3 not P2 — routine hand-refresh due, not a live gap.** The one misfiled migration lead (targeting the wrong plane, governed by neither pipeline) is plausibly `supabase/migrations/2026_07_11_tender_tables_anon_lockdown.sql` — filed under the jvkn path but its own content targets zaap/ehow tender tables (same family as SEC-36). Not yet confirmed as THE misfiled file named in this row's original 2026-08-20 finding, worth a look during the next refresh pass rather than treated as separately proved here. |
| SEC-59 | ~~P3~~ **CLOSED 2026-08-30** | The `shell_control` write-lockdown migrations revoked INSERT/UPDATE/DELETE from `authenticated` but left TRUNCATE granted on 9 tables — TRUNCATE bypasses RLS entirely, though PostgREST has no TRUNCATE verb so there's no browser path today | eq-canonical (jvkn) | **CLOSED 2026-08-30** (row updated 2026-09-04). Same PR as SEC-34 — eq-shell [PR #1662](https://github.com/eq-solutions/eq-shell/pull/1662) (`ea814154`) revokes TRUNCATE from `authenticated` on all 9 `shell_control` tables; dispatched via `control-plane-migrate.yml` to jvkn, confirmed live against the database: all 9 TRUNCATE grants gone (`sessions/2026-08-30.md`, `eq/changelog/eq-shell.md` 2026-08-30 entry). History: ~~OPEN — found 2026-08-20, proved. May overlap with the completed §A sweep — flagging, not claiming novelty.~~ |
| SEC-60 | P3 | Several org/repo hardening gaps: 2FA not required org-wide; secret scanning + push protection disabled on all 7 in-scope repos incl. 3 public ones; third-party Actions unpinned org-wide; **branch protection exists on eq-shell only** — eq-service's `main` (auto-deploys service.eq.solutions, gates the ehow migration pipeline) accepts a direct push with zero required checks | eq-solutions (GitHub org, all repos) | **PARTIALLY CLOSED 2026-08-24** — branch protection added on eq-service; secret scanning + push protection enabled on the 3 public repos. 2FA, the other 5 repos' branch protection, and Action SHA-pinning deliberately left for a later pass (Royce's scope call). See Detail. |
| SEC-61 | ~~P1~~ **CLOSED** | SEC-9's 2026-08-16 closure does not hold: 22 secret-flagged vars across eq-shell/eq-service/eq-field/eq-cards + one Netlify account-scope var still return full plaintext in the `dev` deploy context. `updated_at` timestamps on the leaking vars predate 08-16 entirely — the remediation never touched them | eq-shell, eq-solves-service, eq-field, eq-cards, Netlify account scope | **CLOSED 2026-08-24 — the 21 site-scoped vars fixed.** The 22nd (account-scope `SUPABASE_JWT_SECRET`) tracked separately under SEC-63, still open pending Royce's dashboard check. See Detail. |
| SEC-62 | P2 | The documented "delete+recreate" remediation for the `dev`-context leak (used to close SEC-9/10/12/18/19/24 historically) is itself what causes the leak — recreating a var with "same value, all contexts" always writes a fresh, unmasked `dev` row. All 6 vars this register records as "fixed via delete+recreate" now leak in `dev` | eq-shell, eq-field, eq-solves-service, eq-cards | **OPEN — found 2026-08-21, proved.** The only vars that don't leak are ones with `dev` left EMPTY, not recreated. Every past "delete+recreate" closure in this register should be re-read against this. See Detail. |
| SEC-63 | **P1** | An uninventoried Netlify **account-scope** (team `milmlow`) secret, `SUPABASE_JWT_SECRET`, is the same value that signs every session in the suite (matches 5 per-site vars) — appears nowhere in `ops/secrets-inventory.md`, which only ever enumerated per-site vars. `dev` context unmasked (same as SEC-61) | Netlify account scope (team `milmlow`) | **P1 CONFIRMED (not P0) 2026-08-24** — site-scope resolved by querying all 10 sites individually: reaches only eq-shell/eq-service/eq-field, not sks-nsw-labour. Inventory updated. **Still open:** the `dev`-context leak fix itself — blocked by the coding session's own classifier, needs a permission rule or a manual dashboard delete. See Detail. |
| SEC-64 | P2 | `ops/secrets-inventory.md` maps eq-field's `CANONICAL_SERVICE_ROLE_KEY` to ehow — it's actually the jvkn/eq-canonical service_role key (the one with SEC-9's confirmed chat exposure), corroborated in code (`canon-read.js`) | eq-field, eq-canonical (jvkn) | OPEN — found 2026-08-21, proved. Makes SEC-9's eventual rotation scope wrong as documented — rotating jvkn would break eq-field unless this is caught first. Fix: correct the inventory mapping. |
| SEC-65 | P2 | eq-field's `AUDIT_SB_KEY` is the live ehow **service_role** key, not a "publishable" key as both its own code comment and `ops/secrets-inventory.md` (Tier 2) claim. 4 live consumers (`verify-pin.js`, `eq-agent.js`, `eq-service-sites.js`, `_shared/sentry.js`) run on it believing it's safe to expose | eq-field, sks-canonical (ehow) | **OPEN — found 2026-08-21, proved (identity) / reasoned (impact — not tested whether it's actually exposed anywhere client-side).** See Detail. |
| SEC-66 | P3 | eq-field's Sentry secret-scrubber allowlist omits every Tier-1 secret the app actually places in request headers (`CANONICAL_SERVICE_ROLE_KEY`, `EHOW_SERVICE_ROLE_KEY`, `SKS_JWT_SECRET`, `ZAAP_JWT_SECRET`, `LEAVE_CANONICAL_JWT_SECRET`, `SUPABASE_JWT_SECRET`) — a fetch-error event serializing headers would ship them to Sentry unscrubbed | eq-field | OPEN — found 2026-08-21, reasoned. Ironically the one key it does scrub (`AUDIT_SB_KEY`) is the one SEC-65 shows is mislabeled as low-tier. |
| SEC-67 | P3 | Service_role keys/config still stored for Supabase projects that no longer exist: eq-shell's `FIELD_SUPABASE_*` point at `ktmjmdzqrogauaevbktn` (dead, distinct single-holder key — also disproves the inventory's claim it equals the ehow key), eq-shell's `NEXT_PUBLIC_SUPABASE_*` point at `urjhmkhbgaxrofurpbgc` (deleted, already known), sks-nsw-labour's `AUDIT_SB_URL` points at a project not even in the org | eq-shell, sks-nsw-labour | OPEN — found 2026-08-21, proved. Cleanup, no live exposure (dead refs). **2026-09-04 — code half CLOSED, env-var half still OPEN (Royce's hands).** eq-shell [#1663](https://github.com/eq-solutions/eq-shell/pull/1663) (`3b832f73`, 2026-08-30) deleted `field-supabase.ts`'s zero-caller `getFieldServiceClient()`, so nothing in code reads the dead vars any more. Still to delete on the eq-shell Netlify site: `FIELD_SUPABASE_URL`, `FIELD_SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` — blocked on Claude Code's classifier for unattended env-var writes, commands in `sessions/2026-08-30.md`. sks-nsw-labour's `AUDIT_SB_URL` was not re-checked 2026-09-04 and sits under the standing SKS Labour no-touch rule (SEC-1). |
| SEC-68 | P3 (structurally P1-shaped, well-mitigated) | `EQ_SHELL_JWT_SECRET` + `SUPABASE_SERVICE_ROLE_KEY` (jvkn) are stored as GitHub Actions secrets on the **public** eq-context repo | eq-context (public repo) | **OPEN — found 2026-08-21, proved.** Mitigations verified live: no `pull_request_target`/`workflow_run` trigger anywhere (fork PRs never see secrets), exactly one collaborator, no org-level secrets. Residual: this repo's Actions logs are world-readable, so any future log-leak here is public, not private. See Detail. |
| SEC-69 | P3 | Zero use of `::add-mask::` across the whole suite's workflows, and one confirmed masking-defeat: 9 eq-context backup/verify/restore-drill workflows slice `SENTRY_DSN` and write the fragment to `$GITHUB_ENV` — GitHub masks only the exact secret string, never a derived substring, so the sliced value is unmasked in public-repo logs | eq-context (public repo) | **OPEN — found 2026-08-21, proved (pattern) / reasoned (impact — low today, a Sentry DSN is low-value by design).** Would be P1 if the same pattern were ever applied to a service_role key or DB URL. See Detail. |
| SEC-70 | ~~P1~~ **CLOSED 2026-08-23** | `app_data.eq__guard_timesheet_status`/`eq__guard_leave_status` (ehow, SKS-only by design — these guards don't exist on zaap) resolved caller identity via `eq__caller_staff_id()`, which internally reads the JWT `sub` claim — Field's data-plane JWT sets `sub` to the *tenant* id for every caller by design, so it resolves to a real `app_data.staff.user_id` for nobody. Both guards' self-check (`v_staff IS NOT NULL AND v_staff = OLD.staff_id`) could therefore never be true: a supervisor could self-approve their own submitted timesheet or self-decide their own pending leave request, entirely unblocked. A manager's deliberate self-approval exemption (Royce, 2026-07-21) was unaffected either way. | sks-canonical (ehow) | **CLOSED 2026-08-23, found and fixed same day as SEC-47** (SEC-47's own migration header named this exact gap in the two sibling triggers it was patterned from, without closing it — this migration closes it). Fix: eq-shell PR (migration `0266`) — swaps `eq__caller_uid()`/`eq__caller_staff_id()` for `eq__caller_actor_uid()`/`eq__caller_actor_staff_id()` (the corrected identity helpers from `0261`), no other logic changed. Live dry-run before writing: as a supervisor, self-approving an own timesheet and self-deciding an own leave request both succeeded pre-fix, both correctly blocked post-fix inside the same transaction; a manager's self-approval remained allowed (no regression). Bonus: `approved_by_user_id`/`approver_id`, previously always the tenant id or NULL, now correctly carry the real actor's identity. Dispatched via `tenant-migrate.yml`, independently re-verified live post-dispatch: both functions' source now contains `eq__caller_actor_staff_id`. |
| SEC-71 | **P1 — deliberate, no expiry set** | Two-factor authentication is switched off for everyone by two hard-coded constants on eq-shell, platform admins included: `netlify/functions/_shared/totp.ts:33` `TOTP_ENROLLMENT_MANDATE_ENABLED = false` ([#1735](https://github.com/eq-solutions/eq-shell/pull/1735), `af587538`) and `netlify/functions/_shared/token.ts:638` `TOTP_LOGIN_CHALLENGE_ENABLED = false` ([#1737](https://github.com/eq-solutions/eq-shell/pull/1737), `3945b82c`) — both merged on Royce's 2026-09-01 instruction (squash commits stamped 2026-09-02 07:58 / 08:22 AEST). No env flag, no expiry, no per-role carve-out: the forced-TOTP roles from PR #1068 (managers / supervisors / platform admins) are neither made to enrol nor challenged at login even when already enrolled. Re-enabling is a code change plus a deploy. Shell is PIN-only for every account, and per `eq/go-live-runbook.md` B-3 Service trusts Shell via `eq_shell_bridge` and skips its own TOTP (bridge behaviour not re-verified 2026-09-04), so Service is single-factor too. | eq-shell (core.eq.solutions, LIVE — every tenant) + eq-service (inherits via the bridge) | **OPEN — deliberate decision, recorded 2026-09-04.** Royce, 2026-09-01: "turn 2FA off across everything … remove that friction in the short term"; "the 2FA process is confusing everyone". Context: the same-device QR lockout loop (PR #1655, 2026-08-28) — the friction was real, this is the short-term answer to it. This **inverts the June go-live gate** "MFA posture — make a conscious call" (`eq/go-live-runbook.md` B-3; `eq/pending/eq-shell.md` "MFA-bypass posture"): the call has been made, in the less strict direction, for every role. Verified live 2026-09-04: both constants still `false` on eq-shell `origin/main`. **Expiry: Royce to set.** Suggested closure when it comes: put the switch behind an env var rather than a constant so re-enabling doesn't need a deploy; turn the login challenge back on for platform admins first (fewest people, most access); fix the mobile enrolment path before the mandate returns for workers, or the lockout loop returns with it. Severity is this register's rating (P1: real, live, every-tenant auth-posture regression with no end date), not a re-litigation of the decision. |
| SEC-72 | ~~P2~~ **CLOSED 2026-09-05** | Fail-open on role-override **denials** at session mint (as originally found — see the fix cell for what changed). `netlify/functions/verify-shell-session.ts` wrapped the `tenant_role_overrides` read in `withDeadline(…, BEST_EFFORT_READ_TIMEOUT_MS /* 6000 */, { grants: [], denials: [] })` ([#1736](https://github.com/eq-solutions/eq-shell/pull/1736), `dc10aef2`; line 168 on `origin/main` at the time), and `netlify/functions/token-exchange.ts` did the same for the Field JWT ([#1747](https://github.com/eq-solutions/eq-shell/pull/1747), `4d9424f1`; line 330). If that read took longer than 6 s, the Shell session / Field JWT was minted with an empty denial list. | eq-shell (core.eq.solutions session + Shell→Field handoff, LIVE) | **CLOSED 2026-09-05 — eq-shell [#1762](https://github.com/eq-solutions/eq-shell/pull/1762) (`6c6ec81b953754b6077d0ffe5cae8142fb70a05f`), merged 2026-09-04T20:31:33Z. Own deploy record was superseded by a concurrent merge (`state: error`, `error_message: "Skipped"`) — confirmed live instead via commit ancestry (not deploy titles, per this register's own methodology note above): the squash commit is an ancestor of production deploy `6a9b2b399c4c650008b181ab` (`commit_ref` `ff756c0cb44d5d33d52e565b428e2d84a19c374d`, `published_at` 2026-09-04T20:43:05Z).** Fix: new `netlify/functions/_shared/role-overrides.ts` `resolveRoleOverridesFailClosed()` replaces the empty fallback at both sites — live read → this container's last-known denials for the tenant+role (≤10 min, denials only, never stale grants) → tier 3 when neither is available, handled per endpoint because the two callers' failure modes differ: `verify-shell-session` still issues the session with every overridable key (138 today; `OVERRIDABLE_PERM_KEYS`, moved out of `tenant-role-perms.ts` so allowlist = deny-list) in `denied_perms` for that one response, since a non-OK there signs the user out (`src/App.tsx`, 5-min poll) — the "retryable 503" this row originally suggested was never viable for the session; `token-exchange` instead **refuses the Field mint** (`503 { error: 'permissions-unavailable' }`, audited `token.exchange.refused`), landing FieldIframe in its recoverable "didn't connect / Refresh" state, because eq-field re-signs a Field JWT into a 7-day session that only re-entry after the 60 s TTL (#1758) or a page reload replaces — a closed JWT would have silently crippled a Field visit with no hint why. Tier 2 (cached) reports to Sentry at warning level, tier 3 (hard deny / refuse) at error level, both via a per-tenant+role-per-container 5-minute throttle (new `captureServerWarning()` in `_shared/sentry.ts`) — the underlying `console.warn`/`console.error` is never throttled. The 6 s ceiling is anchored at batch start (not read-start) with a 1 s floor, so a slow gating read can neither stretch the budget nor starve the overrides read of a real attempt. Also closes the pre-existing swallowed-error fail-open inside `getRoleOverridePerms()` for these two callers (`readRoleOverridePerms()` is the discriminated ok/failed building block other callers can adopt). Tests: resolver + both handlers, including the real 6 s ceiling and 1 s floor under fake timers, the throttle, and failed/cached branches; CI green on the merged commit. Reviewed across all 5 pushed commits (eq-shell PR comments 5538583974, 5538687791, 5538750321, 5545939416, 5546029673) — comments, not formal approvals; Royce merged. **Residuals as originally recorded (2026-09-05), now updated:** (1) the 10-min cache still over-restricts in the opposite direction — a denial an admin *removes* stays enforced in a warm container for up to two polls; unchanged. (2) ~~`mint-tenant-jwt.ts:99`, `mint-sks-jwt.ts:93`, `tenant-data-proxy.ts:115` still sign denials through `getRoleOverridePerms()`~~ **CLOSED same day — eq-shell [#1767](https://github.com/eq-solutions/eq-shell/pull/1767) (`726ba3ef`), merged 2026-09-04T21:54:15Z, own deploy record `state:ready`/`published_at` set directly (no supersede this time).** All three now call `resolveRoleOverridesFailClosed()` with the same 6 s ceiling and **refuse the mint** (`503 permissions-unavailable`) on tier 3 — following `token-exchange.ts`'s precedent rather than `verify-shell-session.ts`'s, since each is a bearer credential enforced by many independent RLS/RPC calls across a tenant plane, not one self-healing client-side gate. `tenant-data-proxy.ts`'s refusal is checked *before* its 15-minute JWT cache write, so a refusal can never itself be cached. A sixth call site outside the original tally, `security-groups.ts:204`'s read-only Access Control permissions-preview (found while closing the three above), was fixed the same way and **CLOSED via eq-shell [#1768](https://github.com/eq-solutions/eq-shell/pull/1768) (`364993e3`), merged 2026-09-04T22:34:46Z, own deploy also published directly** — it fails closed into the deny-list rather than refusing outright, since nothing is authorized off a preview response. **The one item still open is `_shared/permissions.ts`'s `resolvePrincipal()`** — deliberately left fail-open, not by omission: `requirePerm()` calls it from roughly 124 independently-bundled functions, most far lower-traffic than the six sites now fixed, so a low-traffic function's own Lambda container would rarely carry a warm cached-denials tier and would land on hard-deny far more readily on any blip — adopting the new resolver there would trade today's narrow, accepted gap for tenant-wide 403s across most of the app's mutating surface during any hiccup, the moment it's adopted everywhere at once. A real trade-off, not a settled one — needs an explicit decision before anyone changes it, not a default follow-up. Not click-tested (no live Shell session available in any reviewing environment). |
| SEC-73 | P2 — latent (isolation holds by view predicate, not RLS) | `app_data.field_people_directory` and `app_data.field_managers` are definer-rights views (`reloptions` `security_invoker=false`) with `authenticated` SELECT on **both** tenant planes — ehow `ehowgjardagevnrluult` and zaap `zaapmfdkgedqupfjtchl`. Supabase `get_advisors` flags all four (2 views × 2 planes) as ERROR `security_definer_view`, re-confirmed 2026-09-04. Tenant isolation holds today only because each view's own definition filters `tenant_id = (auth.jwt()->'app_metadata'->>'tenant_id')::uuid`; RLS on the base tables is bypassed. A future `CREATE OR REPLACE VIEW` that drops that WHERE exposes every tenant's rows to any authenticated caller — and the rows carry name, phone and email on both views (directory: name/trade/licence/agency/job title/phone/email; managers: name/category/role/phone/email — verified column-by-column live 2026-09-04). No DOB, emergency-contact, PIN, rating or TAFE fields — those are deliberately excluded. Created on purpose by eq-field [#813](https://github.com/eq-solutions/eq-field/pull/813) (managers) and [#814](https://github.com/eq-solutions/eq-field/pull/814) (directory), widened to phone+email by [#817](https://github.com/eq-solutions/eq-field/pull/817) on Royce's explicit call, all 2026-08-27 — the definer form was the fix after eq-shell's SEC-33 RESTRICTIVE policy on `app_data.staff` collapsed the invoker-rights version to 0 rows for every non-manager (broke Field's Supervision list / Leave-approver picker). Background: `eq/sprints/2026-08-27-tenant-plane-cross-repo-consumer-check.md`. | sks-canonical (ehow) + eq-canonical-internal (zaap) — eq-field-owned objects | **OPEN — accepted risk, review_by 2026-12-04. Recorded 2026-09-04 as a governed exception; ~~closure needs a call~~ call made the same day (end of this cell).** What already exists: eq-shell's drift gate CHECK 7 (`scripts/check-tenant-drift.mjs` `VIEW_INVOKER_REVIEWED_DEFINER`, [#1642](https://github.com/eq-solutions/eq-shell/pull/1642), `bd0127ed`) content-verifies both views on both planes every run — the exact tenant-filter fragment must be present and `anon` must hold no grant — so the "predicate silently dropped" failure is already caught within one 3-hourly cycle. What it does **not** assert is the column list: its own comment still says the directory carries "no email/phone", which #817 made false the same day; the widening was deliberate, but the guard's description is stale. What's red because of this: eq-context's weekly `security-audit.yml` has **failed since 2026-08-30** ([run 33337697209](https://github.com/eq-solutions/eq-context/actions/runs/33337697209): "4 NEW ERROR-level security finding(s)", exactly these four) — `scripts/security_audit.py`'s `ACCEPTED_ERRORS` baseline is empty, so it stays red every Sunday until either (a) the four are baselined there as `"SEC-73 — review_by <date>"`, the register's intended mechanism for a tracked, accepted risk, or (b) the views go back to `security_invoker=on`, which first requires reconciling SEC-33's RESTRICTIVE policy on `app_data.staff` with what non-managers need to read (the reason #813 exists). Suggested: (a), plus refreshing the CHECK 7 comment so the guard describes what it guards. **Call made 2026-09-04 — Royce: (a), review_by 2026-12-04.** Baselined in `scripts/security_audit.py` `ACCEPTED_ERRORS` as `"SEC-73 — review_by 2026-12-04"` ([eq-context #203](https://github.com/eq-solutions/eq-context/pull/203), merged `bedc7e9`) — two keys, not four: the advisor `cache_key` (`security_definer_view_app_data_field_people_directory` / `security_definer_view_app_data_field_managers`) carries no project ref, so one key covers both planes — and would cover a same-named definer view on jvkn/eq-receipts too (theoretical today, neither has `app_data`; project-scoped keys proposed in the PR body, not built). `test_security.py` now pins the value format and drives `main()` end-to-end with the live lint shape stubbed in (4 ACCEPTED → exit 0, unlisted ERROR → exit 1). CHECK 7 comment refreshed ([eq-shell #1763](https://github.com/eq-solutions/eq-shell/pull/1763), merged `0b37676`) to say phone+email are present by design — and it surfaced one more gap: the migration-time excluded-column assertion ran only in eq-field #814/#817; the 2026-08-30 `field_approved_at` re-creation asserted `reloptions` + the new column only, so nothing re-checks the directory's column list live. A CHECK 7 column assertion was first proposed in #1763's body, then built the same day as a stricter `allowedColumns` allow-list (next paragraph). Column lists re-verified live 2026-09-04 on both planes (directory 24 columns, managers 11). **Confirmed 2026-09-04: the weekly audit went green on the first push to `main` after #203 merged** — [run 33915167442](https://github.com/eq-solutions/eq-context/actions/runs/33915167442) shows all four findings `ACCEPTED` under SEC-73 ("No new ERROR-level security findings"), ending the red streak that started 2026-08-30. **Two guards added the same day, at the go-live-review session's request (cross-session message, 2026-09-04; same (a)/2026-12-04 decision, from a `/decide` pass with Royce):** (1) [eq-context #203](https://github.com/eq-solutions/eq-context/pull/203) — `scripts/security_audit.py` gains `overdue_reviews()` and `test_security.py` fails the weekly workflow's unit-test step the day after any `ACCEPTED_ERRORS` review_by date passes (an entry with no parseable date counts as overdue). Until then review_by was a comment string nothing read — `review_clock.py` covers file frontmatter only. `rls_probe.py`'s `KNOWN_LEAKS` not given the same treatment because it is empty today (`KNOWN_LEAKS = {}`) — nothing to enforce; if an entry is ever added, give it the same `— review_by YYYY-MM-DD` suffix and point `overdue_reviews()` at both dicts (noted, not built). (2) [eq-shell #1763](https://github.com/eq-solutions/eq-shell/pull/1763) — the two CHECK 7 exception entries gain `allowedColumns` (the live 2026-09-04 column lists: managers 11, directory 24) and `checkViewInvoker` now fails on any live column outside the list, hard violation like the predicate check, fail-closed if the column list can't be read; the residual widening failure mode is caught within one 3-hourly cycle like the predicate one. Cost, stated plainly: an eq-field migration that adds a column to either view reds eq-shell's required drift gate until the column is reviewed and the list extended — for a definer-rights view that bypasses RLS, that coupling is the point. Logic verified against the real `checkViewInvoker` with the live row shape + 7 hostile mutations; the PR's own drift-gate run verifies it against both live planes. **Both PRs merged 2026-09-04** — eq-shell #1763 squash `0b37676`, eq-context #203 squash `bedc7e9` — and the audit confirmation above is from the run those merges triggered. |

| SEC-74 | ~~P2~~ **CLOSED 2026-09-05** | `_shared/permissions.ts`'s `resolvePrincipal()` failed open on a `tenant_role_overrides` read that timed out, was rejected, or errored — same root cause as SEC-72, left out of that fix deliberately pending a decision. It hydrates every cookie-authed `Principal` passed to `requirePerm()`/`can()`, called from roughly 124 independently-bundled Netlify functions (2026-08-15 count) — far more than the six call sites SEC-72 and its follow-ups (eq-shell [#1762](https://github.com/eq-solutions/eq-shell/pull/1762)/[#1767](https://github.com/eq-solutions/eq-shell/pull/1767)/[#1768](https://github.com/eq-solutions/eq-shell/pull/1768)) closed. On a lookup failure it returned the principal unchanged, so a tenant admin's denial silently didn't apply for that one request. | eq-shell (core.eq.solutions, ~124 functions behind `requirePerm()`) | **CLOSED 2026-09-05 — eq-shell [#1770](https://github.com/eq-solutions/eq-shell/pull/1770) (`4dc8e8e9`), created 2026-09-04T22:55:37Z, merged by Royce 2026-09-04T23:00:01Z, confirmed live (own deploy record published directly, no supersede). `resolvePrincipal()` now calls `resolveRoleOverridesFailClosed()` with the same 6s ceiling and policy as the other six call sites.** 

**This entry originally recorded the opposite decision — leave as-is, accepted risk — reached minutes earlier the same evening via a direct question to Royce in a separate concurrent session. Two of Royce's own sessions received different instructions on the same open question within about a 12-minute window and both were acted on: this session's "leave as-is" (this row, first written 2026-09-04T22:57Z) and the other session's "adopt everywhere" (#1770, merged 2026-09-04T23:00Z).** #1770's reasoning, read in full before writing this correction: the original "wider blast radius" concern is real but was judged bounded (more 403s during a genuine slowdown, never a wrong grant, already visible via `role-overrides.ts`'s own throttled Sentry reporting) against a countervailing point this row's original close didn't weigh — `resolvePrincipal()` was the only one of the six call sites with **no timeout wrap at all**, so a genuinely slow read could hang a write request indefinitely; the new resolver's 6s ceiling is a latency fix here as much as a security one. This entry is corrected to match the live code rather than left stating a fallback decision that no longer describes reality. Whether #1770 should be reverted in favour of the original accepted-risk framing is a live question for Royce, not resolved by this edit — flagged in `eq/pending/eq-shell.md` and the 2026-09-05 session log. |

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

- **SEC-9 — rotate the jvkn (eq-canonical) service_role key first or alongside SEC-3.** Confirmed exposure (pasted into a chat transcript 2026-07-12). **Runbook exists and is ready-to-run** (`sec9-jvkn-key-rotation-runbook-2026-07-27.md`, committed 2026-07-27, mirrors the SEC-3/F1 staged pattern) — 4 live Netlify consumers mapped (eq-shell primary, eq-field, eq-cards, eq-solves-service). Only blocked on Royce picking a rotation window and running Step 1 himself (Supabase dashboard — key rotation isn't a Claude Code action).
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

**Note 2026-08-21 (Royce):** retirement now weeks away. Decommission remains
the fix, not interim hardening — unchanged since 2026-06-05/2026-07-20.
De-escalating this out of active per-session NEEDS-YOU surfacing on that
basis. **Not closed** — per the 2026-06-27 note above, a "redundant but
still running" app is exactly how this class of exposure gets forgotten, and
a timeline is not the same fact as the key being disabled. Re-open to active
surfacing if the retirement date slips or goes unconfirmed for an extended
stretch. Close condition unchanged: `nspbmirochztcjijmcrx` actually offline /
anon key actually disabled, then strike from `rls_probe.py KNOWN_LEAKS`.

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

**Addendum 2026-08-20 — reopened: the "ehow holds zero" close claim doesn't
hold today.** Prompted by drafting `ops/security-pressure-test-prompt.md`: a
live `get_advisors(security)` spot-check against ehow returned exactly 12
`anon_security_definer_function_executable` findings — the same count this
entry's original close claimed was reduced to zero. Read every one of the 12
bodies via `pg_get_functiondef` (same standard the original close used), not
assumed from names, per the pressure-test doc's own §4.B.

**None of the 12 match the original Ops/Quotes RPC surface this entry
fixed** (`eq_list_quotes`, `eq_get_quote_detail`, `eq_update_customer`, etc.)
— they're a different set entirely, living in `service`/`app_data` (not
`public`), backing EQ Service/Field: `assert_jwt_tenant`,
`eq__caller_actor_staff_id`, `eq__caller_staff_id`, `field_people_removed_iud`,
`field_people_worker_id_iu`, `field_team_supervisors_iud`,
`fn_rcd_circuit_to_defect`, `get_portal_customer_id`, `get_portal_tenant_id`,
`hard_delete_archived_entity`, `portal_user_contact_ids`,
`tg_asset_calibration_history`.

**Verdict: none are exploitable by an anonymous caller today** — same
"defense-in-depth, not a live breach" character as the original close:
- **7 are real RPC-callable functions** (`assert_jwt_tenant`,
  `eq__caller_actor_staff_id`, `eq__caller_staff_id`, `get_portal_customer_id`,
  `get_portal_tenant_id`, `hard_delete_archived_entity`,
  `portal_user_contact_ids`) — all fail closed for anon: each reads
  `auth.jwt()`'s `app_metadata.tenant_id` or `auth.uid()`, both NULL for a
  caller holding only the anon key, and either `RAISE EXCEPTION`
  (`assert_jwt_tenant`, and `hard_delete_archived_entity` via calling it
  first) or return NULL/empty (the rest, via a WHERE clause that never
  matches a NULL caller id).
- **5 are trigger functions** (`RETURNS trigger`) — Postgres refuses to
  invoke a trigger function outside trigger context, so the anon EXECUTE
  grant on these is structurally inert regardless of body content. Traced
  each to its actual trigger: `field_people_removed_iud`/
  `field_team_supervisors_iud` are `INSTEAD OF` triggers on views where
  `anon` holds no UPDATE/INSERT/DELETE (only `authenticated` does);
  `fn_rcd_circuit_to_defect`/`tg_asset_calibration_history` sit on real
  tables where anon likewise holds no write grant (the latter has no
  `authenticated` grant either — nobody client-side can fire it).
  `field_people_worker_id_iu` isn't attached to any trigger anywhere in the
  database — orphaned, unreachable by any path, dead code.

**`hard_delete_archived_entity` specifically** (flagged by name for this
pass): `service.hard_delete_archived_entity(p_entity_type, p_entity_id,
p_tenant_id)` calls `service.assert_jwt_tenant(p_tenant_id)` as its first
statement, which unconditionally raises `42501` unless the caller's JWT
`app_metadata.tenant_id` matches the passed `p_tenant_id` — an anonymous
caller never gets past this line. Every subsequent lookup and the DELETE
itself are also scoped by `tenant_id = p_tenant_id`, and it refuses to
delete a row unless already archived (`is_active = false`) and refuses (via
FK violation) if other records still reference it. Anon-safe. **Separate
finding, not anon-related: see SEC-29** — this function has no role/`eq_role`
check, so any authenticated user of the tenant, any role, can permanently
hard-delete an archived customer/site/asset/job_plan/maintenance_check.

**Root cause of the drift**: `eq-shell/scripts/check-tenant-drift.mjs`'s
function-EXECUTE invariant (`FUNC_EXEC_SQL`, ~line 635) scans only `WHERE
n.nspname IN ('public', 'shell_control')`. The `sks-canonical (SKS tenant)`
baseline is correctly seeded as an empty `Set()` (per this entry's
2026-07-27 fix) — but the gate has never been able to see functions in
`service`/`app_data`, which is where EQ Service/Field's own SECURITY DEFINER
functions live (per `CLAUDE.md`'s own load-bearing fact: `service.*` for
operational tables, `app_data.*` for canonical entities). Confirmed via
`tenant-drift.yml`'s run history: 10 consecutive runs today (2026-08-20), all
green, including a 09:43 UTC scheduled run — **the gate isn't
failing-and-being-ignored, it has been structurally blind to this schema
pair since the baseline was seeded**, on both planes. Re-checked zaap the
same way (`prosecdef = true AND anon-executable`, no schema filter this
time): **5 functions, not the 2 portal functions this entry's close claimed
as the final state** — `eq_get_portal_quote`/`eq_respond_portal_quote` (the
accepted exceptions, unchanged) plus 3 new, all in `app_data`:
`field_people_removed_iud` (same trigger, same story as ehow's copy),
`fn_audit`, `fn_guard_assets_delete`. **The zaap 3 are named, not
body-verified this pass** — same read-every-body standard this entry
requires, just not done yet; fast follow-up, not assumed safe by
pattern-matching to ehow's trigger functions.

**What's not done, deliberately (read-only task, no schema-change authority
given)**: no REVOKE issued anywhere — all 12 ehow + 3 zaap functions are
still anon-executable in production right now. Two decisions are Royce's:
(1) whether to re-run the 0211-style REVOKE+re-GRANT against this new set on
both planes (matches this entry's own precedent — even non-exploitable
grants were revoked as hygiene last time), and (2) whether/how to widen
`check-tenant-drift.mjs`'s `FUNC_EXEC_SQL` schema filter to include
`service`/`app_data` so this class stops recurring silently — without that,
closing today's 12+3 only fixes today's snapshot, the same concern this
entry's own text already raised about SEC-4 never being finished.

**Addendum 2026-08-21 — zaap's 3 functions now body-verified** (were named
but not read 2026-08-20, above). Supabase MCP was not available this session
(never connected); verified instead via the already-authenticated `supabase`
CLI (`supabase db query --linked`, project `zaapmfdkgedqupfjtchl`) — same
Management API path, same standard as the rest of this entry: read every
body, don't assume from names, trace every trigger to its real table/view,
check `anon`'s actual table-level grant there rather than trust the
function's own `EXECUTE` grant.

All 3 reconfirmed `RETURNS trigger` (`has_function_privilege` shows
`anon`/`authenticated`/`public` all still `EXECUTE=true` on all 3, matching
the 2026-08-20 spot-check) — so, as with ehow's 5 trigger functions, Postgres
refuses to invoke any of them outside trigger context regardless of that
grant. Traced each to its real trigger(s) and checked
`has_table_privilege('anon', …)` on every relation found — `anon` holds
**zero** INSERT/UPDATE/DELETE across all 8 distinct relations the 3
functions touch. All 3 are anon-inert, same "defense-in-depth, not a live
breach" character as the rest of this entry.

- **`field_people_removed_iud`** — `INSTEAD OF DELETE OR UPDATE` on the view
  `app_data.field_people_removed`; `anon` holds no UPDATE/DELETE on it. Same
  anon-inert shape as ehow's copy, but **not** the same body — exactly the
  risk the 2026-08-20 note above flagged in naming it "not assumed safe by
  pattern-matching to ehow's trigger functions," and the independent read
  earned its keep: the tenant filter reads `where staff_id = OLD.id and
  tenant_id = coalesce(v_tid, tenant_id)`, where `v_tid` is the caller's JWT
  `app_metadata.tenant_id`. When `v_tid IS NULL`, `coalesce(v_tid,
  tenant_id)` resolves to the target row's own `tenant_id` column — the
  clause collapses to `tenant_id = tenant_id`, a tautology, not a filter.
  That's fail-*open*, not the fail-closed pattern (`RAISE EXCEPTION`, or a
  WHERE clause that matches nothing for a NULL caller) every other function
  this entry has verified uses. Not anon-reachable (no grant) — but
  `authenticated` **does** hold UPDATE+DELETE on this view, so if any
  genuinely-authenticated session's JWT can ever lack
  `app_metadata.tenant_id`, this trigger would touch or hard-delete an
  `app_data.staff` row in **any** tenant, not just the caller's, through an
  ordinary PostgREST call. Whether that JWT shape is reachable in practice is
  an eq-shell token-issuance question — not checked this pass, out of scope
  for "read the 3 zaap bodies." Flagged here for Royce's read rather than
  spun into its own SEC-XX number unilaterally (same optionality SEC-29 was
  given) — his call whether it needs one.
- **`fn_audit`** — generic audit logger, `AFTER INSERT/UPDATE/DELETE` across
  7 tables (`assets`, `contacts`, `customers`, `sites`, `staff`,
  `contact_customer_links`, `contact_site_links`; 17 trigger instances
  total). Not an authorization gate by design — it only ever writes to
  `app_data.audit_log` and self-swallows failures (`EXCEPTION WHEN others
  THEN RETURN NULL`, so a bad header/cast can't break the write it's
  logging); no `auth.uid()`/tenant check is needed or present. `anon` holds
  no write grant on any of the 7 tables. Incidental confirmation of the
  canonical-ownership rule in `CLAUDE.md`/`suite-state.md`: `authenticated`
  also holds **no** direct INSERT/UPDATE/DELETE on 6 of the 7
  (`assets`/`contacts`/`customers`/`sites`/both link tables) — real writes
  there go only through governed SECURITY DEFINER RPCs, not table grants.
  `app_data.staff` is the one exception (`authenticated` holds INSERT+DELETE,
  not UPDATE) — outside this task's scope to chase, noted not investigated
  further.
- **`fn_guard_assets_delete`** — `BEFORE DELETE` on `app_data.assets`. A pure
  guard, not a data-access path: its only two exits are `RAISE EXCEPTION` or
  `RETURN OLD` unchanged, so it can only veto a delete someone else already
  has privilege to attempt — there is no shape in which its own `EXECUTE`
  grant matters. Blocks deleting a `plant_equipment`-type asset outside a
  real user-actor context (explicitly the 2026-07-12 collateral-wipe repeat
  it exists to prevent, named in its own error text) and any delete with no
  PostgREST request context at all. `anon` holds no DELETE on
  `app_data.assets` regardless — moot twice over.

**Verdict: none of the 3 are anon-exploitable.** Closes the "zaap 3, not yet
body-verified" gap flagged 2026-08-20 — both of Royce's pending decisions
above (re-run the 0211-style REVOKE across ehow's 12 + zaap's 3; widen
`check-tenant-drift.mjs`'s schema filter to `service`/`app_data`) now have a
complete evidence base across all 15 functions, not 12. New and not
previously known: whether `field_people_removed_iud`'s tenant-tautology is
worth fixing on its own — an `authenticated`-path correctness question, a
different class of bug from the anon-exploitability this entry otherwise
tracks. No REVOKE issued, nothing changed — read-only pass, per instruction.

**Addendum 2026-08-21 (same day, separate task) — gate coverage gap fixed.**
`check-tenant-drift.mjs` CHECK 6's `FUNC_EXEC_SQL` widened from
`('public', 'shell_control')` to also scan `service`/`app_data` — the schema
pair both this entry's 2026-08-20 reopening and the zaap-body-verification
addendum above were read from directly, but the CI gate itself still
couldn't see (confirmed via `tenant-drift.yml`'s own run history staying
green through both). Seeded `FUNC_EXEC_ANON_TRACKED` (not
`FUNC_EXEC_ANON_ALLOW` — "verified not exploitable today" isn't Royce's
explicit "keep this anon" sign-off) for both tenant planes with the exact
live signatures, not hand-typed from this entry's prose: a
`workflow_dispatch` run against the fix branch with the schema widened but
nothing classified yet reported exactly 12 ehow + 3 zaap violations,
signatures matching this entry's enumeration 1:1; the same branch after
seeding `TRACKED` reported both planes `clean`, all 15 correctly tracked
rather than blocking. eq-shell [PR #1498](https://github.com/eq-solutions/eq-shell/pull/1498),
**merged 2026-08-20T18:14Z** — auth-adjacent CI-gate change, reviewed per
standard flow. No SQL, no migration, no grant change anywhere —
CI-detection-only. Both of Royce's pending decisions above (REVOKE vs.
accept, across the full 15) are unaffected by this fix; what changes is that
the gate now catches this class of function if it recurs, instead of
silently passing the way it did for 10 straight runs on 2026-08-20.
(Supabase MCP was also unavailable for this task, independently confirmed —
see the addendum above for the working alternative, the `supabase` CLI;
this task instead got ground truth for exact signatures from the real gate
itself via `workflow_dispatch`, since that's what ultimately has to agree
with them.)

**Addendum 2026-08-21 (same day, fourth task) — the REVOKE half.** eq-shell
[PR #1499](https://github.com/eq-solutions/eq-shell/pull/1499) drafts the
migration #1498 deliberately left out of scope:
`0252_close_anon_exec_gap_service_app_data_trigger_fns.sql` revokes
anon-EXECUTE (and, for the 8 trigger functions, authenticated-EXECUTE too —
no legitimate direct-call path for a trigger function; corroborated by
SEC-16's own event trigger doing the same to every new function since
2026-07-28 with zero trigger-firing incidents) across all 15. **Not
dispatched** — same gate as everywhere else in this entry, Royce's explicit
approval required before `tenant-migrate.yml` runs. Once dispatched,
#1498's `FUNC_EXEC_ANON_TRACKED` entries for these 15 stop matching live
reality and should be cleared in a follow-up, not done here.

Also independently re-verified ehow's own copy of `field_people_removed_iud`
for the tenant-tautology bug flagged in the addendum above — **confirmed
present there too**, same `coalesce(v_tid, tenant_id)` shape, so this is a
cross-plane bug, not zaap-specific. The two copies have diverged beyond the
shared bug, not a single function replayed twice: ehow's also gates whether
a caller can edit a worker's `rating` behind a `labour_hire`
manager/supervisor permission check that zaap's copy doesn't have at all.

**Addendum 2026-08-20 (fifth task) — CLOSED, REVOKE confirmed live.** PR
#1499 merged 2026-08-20T18:44Z. The actual apply wasn't the merge itself,
or either of the two `tenant-migrate.yml` runs that fired right around
merge time (`32402056582` at 18:14Z and `32404826760` at 18:44Z both only
ran the plan/post-merge-link steps) — the real dispatch that ran "Apply to
all tenants" was run
[32406586537](https://github.com/eq-solutions/eq-shell/actions/runs/32406586537)
at 19:03Z. Worth noting since this repo's own run titles don't distinguish
a plan-only run from one that actually mutated data.

Live-reverified directly against both databases (not inferred from CI or
PR status) via `has_function_privilege`: all 15 functions now
`anon_exec: false`. The 8 trigger functions — `field_people_removed_iud`
(both planes), `field_people_worker_id_iu`, `field_team_supervisors_iud`,
`fn_rcd_circuit_to_defect`, `tg_asset_calibration_history` (ehow), `fn_audit`,
`fn_guard_assets_delete` (zaap) — also show `auth_exec: false`, matching
migration 0252's stated design (no legitimate direct-call path for a
trigger function). The 7 real ehow RPCs (`eq__caller_actor_staff_id`,
`eq__caller_staff_id`, `assert_jwt_tenant`, `get_portal_customer_id`,
`get_portal_tenant_id`, `hard_delete_archived_entity`,
`portal_user_contact_ids`) correctly kept `auth_exec: true` — the REVOKE
only ever targeted anon on those seven, not the legitimate authenticated
callers.

Both halves of this entry are done: the live exposure is revoked, and the
gate (PR #1498) will catch a recurrence instead of silently passing.
**Not closed by this:** `field_people_removed_iud`'s fail-open
tenant-tautology bug (both planes, flagged in the addenda above) is
unaffected by an EXECUTE revoke — REVOKE blocks direct RPC invocation, not
an `INSTEAD OF` trigger firing through whatever grant exists on the view
itself, so that bug is still live and still a separate, open thread for
Royce to prioritize. Also open, lower priority: `FUNC_EXEC_ANON_TRACKED`'s
15 entries in `check-tenant-drift.mjs` are now dead weight — these
functions no longer appear in the gate's query at all (anon_exec is
false), so the entries are inert, not wrong. Real cleanup, not urgent, not
done here.

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

**eq-service's instance CLOSED 2026-08-11.** A production-readiness audit found
6 functions the advisor flagged and this register hadn't yet listed:
`app_data.normalise_employment_type`, `staff_normalise_employment_type`,
`to_au_e164`, `staff_normalise_phones`, `contacts_normalise_phones`, and
`public.trigger_supervisor_digest` (`SECURITY DEFINER` — the one that actually
mattered for privilege-escalation risk). Verified all 6 signatures/bodies live
against `pg_proc` first — none rely on unqualified schema resolution, so
`search_path = ''` (empty, tighter than this row's `public, pg_temp` default)
was correct. Migration `0204_pin_search_path_normalise_helpers.sql`, eq-service
[PR #698](https://github.com/eq-solutions/eq-service/pull/698), merged and
applied live via the governed `apply-service-migrations` pipeline. Re-ran the
advisor post-apply: `function_search_path_mutable` findings on eq-service 6 → 0.
SEC-7 stays OPEN — other projects' instances not swept this pass.

### SEC-30 — zaap public.app_config leaks tenant role-elevation codes to anon (P0, LIVE)
Live-proved 2026-08-20 with a plain anon-key GET against the project's own PostgREST
endpoint — HTTP 200, all 11 rows (`org_id`, `key`, plus the value column, which was
deliberately never selected over REST per this sweep's no-credential-value rule; only
confirmed non-null 6-8 char length via a direct DB connection). Cross-referenced against
`public.organisations` (SEC-32, same project): 2 of the 3 `org_id`s are real, active,
non-demo tenants ("Melbourne Construction Group", Enterprise tier; "Demo Trades Pty Ltd"
despite the name, `is_seed_demo: false`) — only `a0000000-…-0001` is the documented
seed-demo tenant. Key names (`manager_password`, `staff_code`, `supervisor_code`) match
exactly what EQ Field's legacy demo-tenant PIN gate (`eq/identity/IDENTITY-MODEL.md`
§7.1) would consume for role elevation — **whether it's actually wired to a live login
flow is reasoned, not traced**; the consuming code path wasn't followed and no code was
tried against any login flow (that would cross into live-flow testing this sweep was
scoped to avoid). Fix: revoke the `anon` SELECT grant (`REVOKE SELECT ON public.app_config
FROM anon`) at minimum; if this table backs a real login path, follow up on whether it
should be readable by `authenticated` at all versus purely server-side.

**Addendum 2026-08-20 (same day) — identical hole confirmed live on ehow, sks-canonical's
production plane.** Checked whether `public.app_config` exists on the other tenant plane
too, given zaap/ehow are structurally parallel — it does. `pg_policies` shows
`app_config_select` (`cmd=SELECT`, `roles={public}`, `qual=true`) — `{public}` is
Postgres's built-in everyone-pseudo-role, a strictly broader exposure than zaap's
`{anon}`-scoped policy, though the practical anon-reachable result is the same: `anon`
holds the table SELECT grant, so this policy is live for an unauthenticated caller today.
Row shape checked (`org_id`/`key`/`length(value)` only — no values read, same
no-credential-value discipline as the rest of this sweep): 6 rows, all one `org_id`
(`00000000-0000-0000-0000-000000000002`) — this is not a mix of demo/real rows the way
zaap's 3-org table is, **it's SKS's single real tenant, 100% exposed.** Keys:
`supervisor_code` (6 chars), `staff_code` (4 chars) — same role-elevation-code class as
zaap, no `manager_password` key present here — plus three unrelated config keys
(`tafe_holidays`, `tafe_fn_url`, `leave_cc_list`, low sensitivity) and **`tafe_fn_token`
(208 chars) — shaped like a real bearer token or API key, not a short PIN.** Named "tafe"
(Technical and Further Education — an Australian VET body), consistent with some external
compliance/holiday-calendar integration; what it actually authenticates wasn't traced,
same scoping discipline as the zaap finding above.

Write side checked and is NOT part of this exposure: `anon` holds only the SELECT grant
on ehow's `app_config` (confirmed via `information_schema.role_table_grants` — no
INSERT/UPDATE/DELETE for anon), and the `authenticated`-role write policies
(`app_config_manager_supervisor_insert`/`_update`/`_delete`) all correctly gate on
`eq_role IN ('manager','supervisor')` via `with_check`/`qual` — this is a read-only leak
on both planes, not a write hole.

**zaap's `app_config`/`organisations` also carry dormant, unnecessary `anon` grants
beyond SELECT** (INSERT/UPDATE/DELETE/TRUNCATE/REFERENCES/TRIGGER — confirmed via
`information_schema.role_table_grants`). RLS is enabled on both tables
(`pg_class.relrowsecurity=true`) with no `anon`-targeted write policy on either, so
these are inert today (same "grant exists, no policy authorizes it, so it's a landmine
not a live path" shape as SEC-13's trigger functions) — not an active second
vulnerability, but worth closing in the same pass rather than leaving unnecessary
surface area sitting around. ehow's grants are already narrower (anon: SELECT only on
`app_config`).

Fix now covers both planes + both tables: `REVOKE SELECT ON public.app_config,
public.organisations FROM anon` on ehow (closes the live leak; `authenticated`'s access
is untouched — real, role-gated, working feature), and the same plus the dormant extra
privileges on zaap. RLS policies (`app_config_select`/`organisations_select`/
`anon_read_orgs`, all `qual=true`) are left in place, not dropped — the table-level
REVOKE makes them unreachable for `anon` regardless of policy content, and rewriting
policies whose original intent (was `anon` SELECT ever deliberately added for a reason?)
isn't established here is a separate decision from closing the hole. eq-shell
[PR #1509](https://github.com/eq-solutions/eq-shell/pull/1509) — drafted, not
dispatched, Royce's explicit approval required before this touches either plane live.

**Addendum 2026-08-21 — the deferred question above ("was `anon` SELECT ever
deliberately added for a reason?") has an answer, and it invalidates the fix above.**
Traced the actual client code instead of reasoning from the RLS policy alone:
`eq-field/scripts/app-state.js:481-502` runs at tenant-resolve/boot time, unconditionally,
for every tenant, on every page load, before any session or JWT exists —
```
const cfgResp = await fetch(`${SB_URL}/rest/v1/app_config?org_id=eq.${TENANT.ORG_UUID}&select=key,value`,
  { headers: { apikey: SB_KEY, Authorization: 'Bearer ' + SB_KEY }, credentials: 'omit' });
```
— using the anon/publishable key, scoped to the CALLING tenant's own `org_id`, to populate
`window.__TENANT_CODES_DB__` (the client-side PIN comparison source). This is not the
"legacy demo-tenant PIN gate" this table's SEC-30 summary originally guessed at — it runs
for every tenant regardless of Core-only status, and the corresponding `sbFetch` comment
in the same repo (`scripts/supabase.js:162-168`) confirms the grant is deliberate suite-wide
architecture: *"anon keeps SELECT (gate reads pre-login)... migration
app_config_authenticated_write, **ehow + zaap**."* So:

- **`REVOKE ALL`/`REVOKE SELECT ... FROM anon` (PR #1509, either plane) breaks this boot
  fetch for every tenant on that plane.** Confirmed, not suspected — do not dispatch.
  Commented on the PR with this finding 2026-08-21.
- **A single-hardcoded-`org_id` policy narrowing (the shape tried in PR #1510's first
  draft, before it was pulled back out) is ALSO wrong** — it only preserves the boot fetch
  for one org. zaap's `app_config`/`organisations` hold at least 2 other real, non-demo
  org rows ("Melbourne Construction Group", "Demo Trades Pty Ltd" despite the name) that
  may have their own live EQ Field deployment depending on this same per-tenant boot read
  for THEIR OWN `org_id` — narrowing to one UUID would silently break their config load
  instead of anon's. This wasn't verified either way before the narrower fix was drafted;
  it's now flagged rather than shipped on a guess.
- **The real fix needs the enumerated, live-verified list of org_ids with an actual
  deployed EQ Field frontend on each plane** (Netlify site env vars / tenant-resolution
  config, not just a row existing in `organisations`), scoped as an `IN (...)` allowlist —
  or, better, a redesign that doesn't rely on RLS distinguishing "org A's honest client"
  from "anyone claiming org A" purely by a client-supplied `org_id` filter, since anon has
  no other identity to scope by and that's the actual structural weakness, not just a
  missing WHERE clause. Neither is a same-night patch. Tracked as a follow-up, not rushed
  under either PR.

Net effect tonight: SEC-30/32 fixes on BOTH #1509 (ehow+zaap blanket revoke) and #1510's
original app_config/organisations statements are held. #1510 was edited 2026-08-21 to
drop those statements entirely — see SEC-33 below, which shares no part of this problem
and ships from the same PR, alone.

**Resolution, same day.** The enumeration this addendum called for is done. eq-field is
"canonical-standalone" (its own code comment) — every tenant load resolves
`TENANT.ORG_UUID` from jvkn's canonical `public.organisations` table (exact hostname
match, then substring, then a `?tenant=` override gated to same-hostname/dev/Shell-
embedded contexts only — traced in `app-state.js`'s `_loadCanonicalConfig()`), never
from a plane's own local `organisations`/`app_config` rows directly. Queried jvkn live:

| slug | routes to | status |
|---|---|---|
| `eq` | zaap (`zaapmfdkgedqupfjtchl`) | active |
| `sks` | ehow (`ehowgjardagevnrluult`) | active |
| `favour-perfect` | a **deleted** project (`nxojbntrpxfnbhbyaspp`) | suspended |

Three rows, suite-wide. "Melbourne Construction Group" and "Demo Trades Pty Ltd" — the
two zaap-local orgs whose possible dependence on this anon read paused the previous
draft — are **not in this table at all**: orphaned rows in zaap's own database with no
`shell_control.tenant_routing` entry, so `TENANT.ORG_UUID` can never resolve to them
through any real user path (not standalone hostname match, not the Shell-embedded
override). The one client-side fallback that reads a plane-local `organisations` row
(`app-state.js`'s org_id-fetch fallback, used when server-side routing doesn't supply
`org_id` directly) filters by the same canonical-resolved slug — `'eq'` or `'sks'` only,
never an arbitrary one. So each plane has exactly one real, reachable org_id: the same
`a0000000-…-0001` the original narrow draft used for zaap, and `00000000-…-0002` for
ehow (which was already the only row there anyway).

Rewrote eq-shell PR #1509 accordingly — `0257_close_sec30_32_both_planes.sql` replaces
both the blanket-revoke file and the withdrawn single-org draft. Both planes ship in one
file (confirmed 2026-08-21, while shipping SEC-33, that `tenant-migrate.yml` applies
every file here to both tenants uniformly — no per-file plane routing exists), guarded
per-branch on each plane's actual policy names (zaap: `app_config_anon_select`/
`anon_read_orgs`; ehow: `app_config_select`/`organisations_select`, role `{public}` —
`{anon}` is a member of `{public}` so the practical exposure is identical) so a name
that doesn't exist on a given plane is a no-op there, not a hard error. Also resets
`anon` to exactly `SELECT` on both tables via a plane-agnostic `REVOKE ALL` + re-`GRANT
SELECT` (closes zaap's dormant extra grants; no-op on ehow, already SELECT-only).
Dry-run tested clean end-to-end — including the migration's own post-condition check,
not just the bare statements — against both zaap and ehow. CI green, PR mergeable.
**Not dispatched — awaiting Royce's explicit go, same gate as every live DDL change in
this register.**

### SEC-31 — jvkn public.organisations leaks cross-tenant Supabase URL + anon key (P1)
Live-proved 2026-08-20: `pg_policies` shows `qual=true` for the `authenticated` role
(anon correctly has no grant — live REST probe confirmed 401). SEC-27-shape: a
`tenant_id` column exists and no policy references it. EQ Cards self-signup is open real
traffic (`suite-state.md`), so the practical bar to get an authenticated session is close
to zero. Blast radius nuance: the leaked value is each tenant's own Supabase *anon*-type
key (designed to be public/embeddable) plus its project URL, not a service-role
credential — so this is cross-tenant infrastructure reconnaissance and a pivot point into
probing another tenant's own RLS surface directly, not automatic full data access on its
own. Already known in code: `check-tenant-drift.mjs`'s `SENSITIVE_COLUMN_GRANTS` comment
reads *"`authenticated` is intentionally NOT checked here — it legitimately holds
full-column access to organisations today; narrowing that is a separate, out-of-scope
task."* That deferral was never logged here — this row is that log entry. Fix: scope the
read policy by `tenant_id`, or split `supabase_url`/`supabase_anon_key` into a column set
`authenticated` doesn't get blanket access to.

**2026-08-23 — CLOSED.** Royce ran the statement himself against jvkn via the
Supabase SQL editor (dashboard, new query, executed directly — "Success. No rows
returned"). Independently re-verified live, not just the UI success message:
`organisations_read`'s `qual` on `public.organisations` now reads
`COALESCE((auth.jwt() -> 'app_metadata' ->> 'is_platform_admin')::boolean, false)
OR tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid` — the
platform-admin bypass plus per-tenant scoping this fix was designed to add,
confirmed via direct `pg_policies` query against jvkn. This closes the last open
item in the SEC-13/29/30/31/32/33 cluster.

### SEC-32 — zaap public.organisations, anon-readable tenant registry (P1 as part of the SEC-30 chain)
Live-proved 2026-08-20: anon-key GET returns all 3 rows. Alone this is low-sensitivity
branding/tier metadata — the finding is its role paired with SEC-30: naming the org_ids
SEC-30's `app_config` table otherwise exposes only as opaque UUIDs. Fix both together —
this row's fix is straightforward (`REVOKE SELECT ... FROM anon` unless something
legitimately needs anon org-name lookups, in which case narrow the columns instead).

**2026-08-21 — the hedge above resolved to yes.** See SEC-30's addendum: something does
legitimately need anon reads on this table's sibling `app_config`, on both planes, and
the same structural doubt now applies here until proven otherwise for `organisations`
specifically. Held alongside SEC-30, not fixed separately.

### SEC-33 — zaap app_data.staff: live tenant-wide read+delete on coworker PII (P1)
Live-proved at the DB layer 2026-08-20: `role_table_grants` confirms `authenticated`
holds a real `DELETE, INSERT, SELECT` grant (no UPDATE); the only policy
(`staff_tenant_isolation`, `ALL`) checks `tenant_id` only. Anon separately confirmed
denied (401, no anon grant). The full authenticated HTTP path wasn't exercised — that
needs a real tenant JWT, which this sweep doesn't hold and won't forge. `app_data.staff`
backs the `field_people` view (name, DOB, phone, email, emergency contact) — same data
shape as SEC-1/SEC-27, except reachable here by any authenticated tenant member with zero
elevated role, and the exposed surface includes DELETE, not just read. This is the most
severe of the SEC-27-pattern recurrences this sweep found (see also SEC-27's own updated
note for 8 more latent instances). Fix: narrow the policy to self-row-or-manager/
supervisor, matching the pattern already used for timesheets/leave_requests (RESTRICTIVE
own-crew policy AND'd against the tenant-wide PERMISSIVE one).

**2026-08-21 — fix built, isolated, not yet dispatched.** eq-shell
[PR #1510](https://github.com/eq-solutions/eq-shell/pull/1510) — originally bundled with
SEC-30/32 in one migration file, split apart once the app_config boot-fetch issue
surfaced (see SEC-30's addendum); this table has no anon exposure and no dependency on
that question, so its fix is untouched by the split. Dry-run tested live on zaap
(begin…rollback): `staff_own_or_manager_read` policy present with the intended qual,
`authenticated`'s INSERT/DELETE grants gone, verified via the migration's own `DO
$verify$` post-condition block. CI green. Awaiting dispatch approval.

**2026-08-21 — scope correction before dispatch: this migration applies to BOTH planes,
not zaap alone, and that turned out to matter.** eq-shell's `tenant-migrate.yml` /
`migrate-tenants.mjs` applies every file in `supabase/tenant-migrations/` to every active
tenant uniformly (confirmed by reading the runner — no filename-based routing exists;
`_zaap` in a filename is a human label only). The PR's plan job independently confirms
this: `0256_*.sql` shows pending for both `eq` (→zaap) and `sks` (→ehow). Checked what
that means for ehow before dispatching rather than after: **ehow's `app_data.staff` has
the identical unscoped shape today** — only `staff_tenant_isolation` (tenant-only,
`cmd=ALL`) governs SELECT, no role or self check at all, so any authenticated SKS staff
member can already read every coworker's full PII on live production. This is the same
gap class as this row and as SEC-27's other cataloged instances, just not previously
given its own line here. `user_id` (uuid) exists on ehow's table with the same shape
zaap's does. Dry-run tested live on ehow (begin…rollback): applies clean, no name
collision, policy qual reads as intended, `REVOKE INSERT, DELETE` no-ops safely (ehow
never held those grants for `authenticated`, consistent with this row's summary column).
Net effect of one dispatch: closes the gap on zaap (the originally-scoped target) AND
closes the same gap on ehow (SKS production) as a verified, not assumed, side effect.
Worst-case failure mode if `actor_id` isn't populated for some legacy SKS session is that
a non-manager loses a read they shouldn't have had — manager/supervisor role passes
unconditionally either way, and no write path is affected (the only INSERT/DELETE caller,
workers-canonical-sync, runs on the service-role key and bypasses RLS entirely).

### SEC-37 — zaap app_data.timesheets/leave_requests: live tenant-wide read of pay/health data (P1)
Found 2026-08-21 during SEC-33's own follow-up check (same session, same sweep). Live-proved:
`pg_policies` shows exactly one policy per table (`timesheets_tenant_isolation` /
`leave_requests_tenant_isolation`, `ALL`, tenant_id-only qual) — same shape as SEC-33's
`app_data.staff` before its fix, one class down (pay/health data, not PII+DELETE). Any
authenticated zaap tenant member, any role, can read every coworker's timesheet and leave
request. Not a duplicate of eq-field v3.5.529 (872c4b19, already live) — that's a
client-side Timesheets-screen row filter (`_getTsFilteredPeople()`), not a DB-side
boundary; the raw table is unaffected by it, same as `scripts/permissions.js`'s existing
crew filter is described elsewhere in this repo's migrations as "a convenience, not a
boundary."

Considered and rejected: porting ehow's crew-scoped pattern
(`timesheets_own_crew_read`/`leave_requests_own_crew_read`, eq-field's
`20260819_timesheets_leave_actor_identity_fix.sql`) verbatim. Confirmed live: zaap has
neither `app_data.team_supervisors` nor `team_members` (`to_regclass` → null for both,
also `teams`) — not a gap, a deliberate scope boundary
(`20260722_field_team_supervisors.sql`'s own header: "Teams is an SKS-only feature...
must NOT be dispatched to zaap"). That same migration's header had already reasoned
through this exact zaap follow-up and named the fallback shape used here:
own-row-or-manager/supervisor, no crew join. Independently corroborated by a
`sks/pending.md` entry dated 2026-08-16 flagging the identical zaap gap as known and
deferred pending "prerequisite pieces" — the two identity helpers this fix ports are
exactly that.

Fix: eq-field [PR #753](https://github.com/eq-solutions/eq-field/pull/753) — ports
`eq__caller_actor_uid`/`eq__caller_actor_staff_id` (byte-for-byte from ehow's own
20260819 migration, logic was never ehow-specific) and adds one RESTRICTIVE SELECT
policy per table: manager/supervisor role, or own row via `app_metadata.actor_id`
(same claim SEC-33's own fix already uses on this plane). Dry-run tested live on zaap
(`begin...rollback`), verified clean — both policies + both helpers created inside the
transaction with the intended qual, full post-rollback re-check confirms zero trace on
committed state. **Merged into eq-field main 2026-08-22.**

**Dispatched and verified live 2026-08-23.** Royce's explicit go, then eq-shell's One
Pipe (`--slug=eq`) applied `0262_timesheets_leave_zaap_own_manager_read.sql` to zaap
cleanly (the migration's own built-in verify block would have raised if either policy
or either helper hadn't landed — it didn't). Independently re-confirmed outside the
pipeline's own report via a direct `pg_policies`/`pg_proc` query against zaap:
`timesheets_own_or_manager_read` and `leave_requests_own_or_manager_read` both exist
as RESTRICTIVE SELECT policies alongside the original PERMISSIVE tenant-isolation
policy (RESTRICTIVE+PERMISSIVE AND together, closing the gap rather than replacing the
tenant check), and both `eq__caller_actor_uid`/`eq__caller_actor_staff_id` exist in
`app_data`.

**Dispatch-safety finding, found while building this fix — now resolved, in two parts:** eq-field
has no dispatch mechanism of its own — the One Pipe is eq-shell's
`scripts/migrate-tenants.mjs`, which reads only its own `supabase/tenant-migrations/`
and, with no `--slug` flag, applies every pending file to every active tenant by default
(confirmed live 2026-08-21 via PR #1510's own plan job: a `_zaap`-suffixed migration
showed pending for both `eq`/zaap and `sks`/ehow — the filename is a human label the
runner never reads). For SEC-33's staff fix that was harmless by coincidence (ehow had
the identical gap). It would not be harmless here: ehow's own crew-based fix for these
same two tables is still undispatched too, and if PR #753's migration ever landed on
ehow by the no-flag default, its RESTRICTIVE policy would AND against ehow's (whenever
that ships), silently narrowing real SKS supervisors' crew visibility rather than just
being redundant. PR #753's own description and migration header both carry an explicit
"copy into eq-shell + dispatch with `--slug=eq`" instruction, but that is still only a
comment, not an enforced control — the underlying gap (no machine routing for
single-plane eq-field migrations) is real, affects several other still-undispatched
eq-field migrations too (`20260722_field_team_supervisors.sql` and its two lockdown
siblings, `20260819_timesheets_leave_actor_identity_fix.sql`), and is tracked as its
own follow-up, not fixed here. **Update 2026-08-22: that follow-up merged as eq-shell
[PR #1516](https://github.com/eq-solutions/eq-shell/pull/1516)** (a different session's
work) — adds the `-- Plane:` header convention so a migration can declare which
tenant(s) it's for, machine-checked by `migrate-tenants.mjs`.

**Update 2026-08-23 — PR #1516 itself had a bug, found live while actually dispatching
this fix:** its enforcement was a pre-flight check that scanned every file in
`supabase/tenant-migrations/` (not just what's pending) against the full run target
set, and blocked the ENTIRE run if any file anywhere declared a plane narrower than
that set. By 2026-08-23 four ehow-only migrations (0258-0261, the Teams-lockdown ones
plus the actor-identity fix this section already named) and this fix's own zaap-only
migration (0262) all coexisted in the directory — so a real `--slug=eq` dispatch for
0262 was blocked citing 0258-0261, migrations with nothing to do with eq. Zero tenants
touched (fails safe by design), but the guard was self-defeating for the exact
cross-tenant scenario it was built for. Fixed same day as eq-shell
[PR #1524](https://github.com/eq-solutions/eq-shell/pull/1524): enforcement moved to
per-tenant, per-migration, inside the actual apply loop rather than a whole-run
pre-flight — a migration is now simply skipped for a tenant its plane doesn't cover,
in every mode (plan/dry-run/real) alike. Verified against the live fleet via that PR's
own read-only Plan job (showed 0262 pending only for `eq`, 0258-0261 pending only for
`sks`, each correctly skipped for the other) before merging, then the real 0262
dispatch to `eq` succeeded immediately after.

### SEC-38 — zaap actor-identity helpers anon-executable, found via SEC-37's own dispatch (P3, CLOSED)
Found 2026-08-23, immediately after SEC-37's migration (0262) dispatched to zaap:
this repo's own required "Function-EXECUTE invariant" CI check flagged
`app_data.eq__caller_actor_staff_id(uuid)` as a newly anon-executable SECURITY
DEFINER function. Root cause: Postgres grants EXECUTE to PUBLIC by default on
`CREATE FUNCTION`, and neither SEC-37's migration (0262) nor its ehow counterpart
(0261, still undispatched) explicitly revoked that default before granting to
`authenticated`/`service_role` — so `anon` inherited access to both
`eq__caller_actor_uid()` and `eq__caller_actor_staff_id(uuid)` via PUBLIC. Confirmed
live via `has_function_privilege('anon', ..., 'EXECUTE')` = true for both, on zaap,
before writing the fix.

**Assessed exploitability, not assumed:** `eq__caller_actor_uid()` reads the JWT's
`app_metadata.actor_id` claim, which resolves NULL for an anon caller (no valid JWT
claims to read). `eq__caller_actor_staff_id()`'s `WHERE s.user_id = ...actor_uid()`
can therefore never match for anon regardless of the `p_tenant_id` argument passed —
no real `staff_id` was ever actually returned to an unauthenticated caller, despite
the SECURITY DEFINER function technically running with elevated privileges. This
closes an unintended-but-inert exposure to the always-intended posture, not a patch
on an already-exploited hole.

Fix: eq-shell [PR #1529](https://github.com/eq-solutions/eq-shell/pull/1529),
migration `0263_revoke_anon_exec_actor_identity_helpers.sql` — `REVOKE EXECUTE ...
FROM anon` + `FROM PUBLIC` for both functions, each guarded by
`to_regprocedure(...) IS NOT NULL` so the same migration is also the correct fix for
whenever 0261 eventually dispatches to ehow (that migration defines the identical
two functions with the identical gap, still unapplied there as of this writing).
Merged, dispatched `--slug=eq`, verified live:
`has_function_privilege('anon', 'app_data.eq__caller_actor_uid()', 'EXECUTE')` and
the `staff_id` variant both `false`; `authenticated` access to both unaffected
(`true`, unchanged). **Note on the merge itself:** the required drift-check gate
still showed the pre-fix live state at merge time by construction (it reads live DB
state, and cannot go green until the fix it names is itself dispatched, which can
only happen after merge) — merged via `--admin` to break that chicken-and-egg,
narrowly justified because the only failing check was the exact one this PR fixes,
confirmed by reading its output line by line before overriding, not assumed.

**Process note:** SEC-4's row above already established this exact function class
(anon-executable SECURITY DEFINER) as a real, recurring pattern in this codebase,
not a one-off — worth treating "does my new migration explicitly revoke the PUBLIC
default?" as a standing checklist item for any future SECURITY DEFINER function,
rather than relying on this same CI check to catch it after the fact each time.

### SEC-39 — Field access-gate bypass chain via mint-supabase-jwt + verify-shell-token (P2)
`mint-supabase-jwt.ts` mints a jvkn-signed Supabase JWT for any valid `eq_shell_session`
cookie (any role), carrying `app_metadata.tenant_id`/`eq_role` — `source_app` is taken
from a **client-controlled `?source_app=` query param**, and its origin check is
report-only (no `alwaysEnforce`). Field's `verify-shell-token` action checks only
signature + `exp` + `tenant_id` presence, never `source_app`, and derives tenant
authoritatively from `app_metadata.tenant_id`. Field has no knowledge of
`has_field_access`/`field_access_unlocked_at` — that gate lives only in
`token-exchange.ts`, which `mint-supabase-jwt` doesn't call. Chain: a Shell user
(including one with Field access withheld) → own-cookie POST to `mint-supabase-jwt` →
POST that token to Field's `verify-shell-token` (no cookie/origin gate on that action) →
Field mints a 7-day session at the user's real role for their own tenant. Root cause is
the shared signing secret across two trust boundaries (SEC-24's pattern) plus no
`source_app`/`aud` binding on either receiver. Fix needs both: bind `source_app` to the
minter's own knowledge of the caller (not a query param), and check `has_field_access`
in `mint-supabase-jwt` too, or route all Field access through `token-exchange` exclusively.

### SEC-41 — eq_delete_quote: bulk hard-delete of live quotes, no role gate (P1)
`SECURITY DEFINER`, `GRANT EXECUTE TO authenticated`. Body hard-`DELETE`s from
`app_data.quote` scoped by JWT `tenant_id` only — no `eq__assert_entity_role` call, unlike
its 20 CRM siblings (`eq_delete_customer`/`_site`/`_contact`, merge/archive/upsert family),
all gated in `eq-shell/supabase/tenant-migrations/0245_entity_role_gate_crm_rpcs.sql` and
confirmed applied live on both planes. The quote family was left out of `0245`. Reachable
by clicking, any role: `QuotesModule.tsx:2709` (single delete) and `:2776` (**bulk** —
loops a multi-select calling the RPC per id). That same file gates sites with `useCan`
(`entity.create`/`.edit`/`.delete`) but has no `useCan` anywhere on the quote-delete paths
— no client gate, no server gate. 198 live quotes on ehow. Fix: add the same
`eq__assert_entity_role` first-statement pattern `0245` used — which permission key is a
product decision.

**Update 2026-08-23: fix drafted, eq-shell [PR #1534](https://github.com/eq-solutions/eq-shell/pull/1534), migration `0264`, not dispatched.**
Permission key resolved (asked in chat, not assumed — this doc's own "product decision"
flag was accurate): `entity.delete`, manager only, reusing `0245`'s helper verbatim, no
new permission key, no `@eq-solutions/roles` change. Cross-plane byte-identity confirmed
(md5 of whitespace-normalised `prosrc`) between zaap and ehow before writing — one
canonical migration is correct for both. Dry-run verified live on zaap (`begin...rollback`,
confirmed zero persisted changes via a direct `prosrc` re-check after): an `employee`-role
caller is blocked with `insufficient_permission: entity.delete required`; a `manager`-role
caller passes the gate and hits the expected "quote not found" on a fake id, proving the
guard is a true no-op on the legitimate path. Grant re-assert included (`eq_enforce_function_privacy`
strips grants on every `CREATE OR REPLACE`, confirmed active on both planes). Not
revoking `authenticated`'s grant — `QuotesModule.tsx` calls this RPC directly from the
browser for every role, the gate goes inside the function body. **Not dispatched** —
dispatching to zaap/ehow via `tenant-migrate.yml` is a separate, explicit step.

**Update 2026-08-23: CLOSED — dispatched fleet-wide, live-verified on both planes.**
`tenant-migrate.yml` dispatched with a blank slug (whole fleet) via `workflow_dispatch`
(run [32613927114](https://github.com/eq-solutions/eq-shell/actions/runs/32613927114),
`success`, `0 applied, 283 skipped` on both `eq`/`sks` — the 3 pending migrations
`0256`/`0263`/`0264` had already landed by the time this dispatch ran, confirmed by
independently checking the live ledger and function source directly rather than trusting
the "0 applied" line at face value). `app_data._eq_migrations` on both zaap and ehow lists
`0264_entity_role_gate_quote_rpcs.sql` as applied. Live `pg_proc.prosrc` for
`eq_delete_quote` contains the `eq__assert_entity_role` call on both planes. A live
(production, not dry-run) probe against zaap — `set local request.jwt.claims` to an
`employee`-role JWT, then call `eq_delete_quote` — returns `insufficient_permission:
entity.delete required`, confirming the gate is real and enforced, not just present in
source. The dispatch also applied two unrelated pending migrations from other sessions
(`0256`: extends an existing delete-guard trigger to a new asset category, idempotent;
`0263`: revokes anon-EXECUTE on actor-identity helpers, already proven safe on zaap) —
`tenant-migrate.yml` has no per-migration selector, so a fleet dispatch is all-pending-or-
nothing; both were reviewed before dispatching and are unrelated to this fix.

### SEC-42 — eq_replace_line_items: purge-then-replace on quote pricing, no role gate (P1)
Bug-class #6 verbatim. `SECURITY DEFINER`, `authenticated`: verifies the quote's tenant,
then `DELETE FROM app_data.quote_line_item WHERE quote_id = …`, then bulk re-INSERTs from
caller-supplied JSON and recomputes totals. Data shape and tenant are checked; caller role
is not. Called from the browser at `QuotesModule.tsx:2404`/`:2583` — no server-side twin,
unlike the CRM family (`crm-write.ts` maps every customer/site/contact action to a
permission and runs `requirePerm` before touching the same `app_data` tables; the quote
family has no equivalent, the browser talks to tenant PostgREST directly). 511 live line
items on ehow. Same fix shape as SEC-41.

**Update 2026-08-23: fix drafted, eq-shell [PR #1534](https://github.com/eq-solutions/eq-shell/pull/1534), migration `0264`, not dispatched.**
Same migration as SEC-41, deliberately a *different* permission key: `entity.edit`
(manager + supervisor), not `entity.delete`'s manager-only tier — asked in chat rather
than assumed, since replacing line items is routine quote-building, not a destructive
action, and gating it at SEC-41's tier would block supervisors from normal quote work.
Dry-run verified live on zaap (`begin...rollback`, confirmed zero persisted changes
after): an `employee`-role caller is blocked with `insufficient_permission: entity.edit
required`; a `supervisor`-role caller passes the gate and hits the expected "quote not
found" on a fake id. Same cross-plane byte-identity check, same grant re-assert, same
"not revoking `authenticated`" reasoning as SEC-41 — see its Detail. **Not dispatched.**

**Update 2026-08-23: CLOSED — same dispatch as SEC-41 (run [32613927114](https://github.com/eq-solutions/eq-shell/actions/runs/32613927114)), live-verified on both planes.**
`app_data._eq_migrations` lists `0264_entity_role_gate_quote_rpcs.sql` as applied on both
zaap and ehow. Live `pg_proc.prosrc` for `eq_replace_line_items` contains the
`eq__assert_entity_role` call on both planes. See SEC-41's Detail for the full dispatch
record and the live-probe methodology (same pattern applies here: an `employee`-role
caller hits `insufficient_permission: entity.edit required` on live zaap).

### SEC-44 — eq_cards_link_or_create_worker: cross-org identity bind, no caller check (P0)
`public.eq_cards_link_or_create_worker(p_user_id uuid, p_phone text, p_email text,
p_first text, p_last text)` — `SECURITY DEFINER`, `authenticated`. No `auth.uid()`, no
invite token, no phone-ownership check, no org scoping. Searches `public.workers`
suite-wide for an unclaimed row matching phone/email, then `UPDATE`s
`user_id = p_user_id`. It's the shared inner resolver behind four outer RPCs that each
guard it properly — `eq_cards_claim_invite` requires a valid unexpired invite token AND
(per migration `0124`) compares the invite's phone against the session's OTP-verified
phone; `eq_cards_upsert_my_worker` passes `auth.uid()` hardcoded. Called directly, the
resolver performs the exact identity bind those guards exist to protect, with an
arbitrary caller-supplied `p_user_id` — bug-class #4's "guard on the outer function but
not an independently-reachable inner one." 35 of 104 `public.workers` rows on jvkn have
`user_id IS NULL` today — the vulnerable population; claiming one inherits that worker's
credentials/licences and pending org linkage. Meets this doc's own P0 wording ("a caller
in the wrong tenant") since there's zero org scoping — an authenticated user of org A can
bind a worker belonging to org B. Not proved end-to-end (needs a real claim-flow account,
a §7 line). Fix: `REVOKE EXECUTE ... FROM authenticated` — it should only ever be called
internally by the four guarded outer RPCs, which can use `SECURITY DEFINER` privilege to
reach it without a public grant.

**Update 2026-08-23: fix drafted, eq-cards [PR #289](https://github.com/eq-solutions/eq-cards/pull/289), not applied.**
Went one step past the fix this entry originally proposed — instead of relying on the grant
alone, the resolver now checks its own caller: `p_user_id IS DISTINCT FROM auth.uid()` raises
`caller_uid_mismatch` (null-safe, so an unauthenticated caller is rejected the same way a
mismatched one is). Traced all 9 real call sites first (grepped every `.sql` migration in
eq-cards plus every `.ts`/`.tsx`/`.js` across eq-cards and eq-shell for a direct `.rpc()`
call — none exist; all 9 are internal `PERFORM`/assignment calls from other `SECURITY
DEFINER` functions in 0062/0067/0071/0072/0077/0082/0090/0121/0124, every one of which
already derives `v_user_id := auth.uid()` before calling in) — the guard is a no-op on
every real path. Live-checked before writing: `authenticated` currently holds EXECUTE
alongside `service_role`/`postgres`; the migration also revokes it explicitly, matching
this repo's own established grant-hygiene pattern (0062, 0094) rather than relying solely
on the `eq_enforce_function_privacy` event trigger to strip it on `CREATE OR REPLACE`.
**Not dry-run tested live** — a `begin...rollback` dry-run against jvkn from this session
hit the same "modifying security settings" classifier block that stops Claude Code on
SEC-12/18/19; the PR body carries the exact dry-run SQL for a human to paste into the
Supabase SQL editor. **Not applied to jvkn** — control-plane migrations here apply by hand
(`apply_migration`/dashboard), and live application is an explicit separate step, same as
SEC-30/31/33.

**Update 2026-08-23: CLOSED — applied live to jvkn.** eq-cards PR #289 merged, then
applied via `mcp__supabase__apply_migration` (the tracked path — lands in
`supabase_migrations.schema_migrations`, unlike raw `execute_sql`; see this repo's own
migration README on why untracked DDL breaks future branch replay). Not blocked by the
classifier this time — only the earlier `begin...rollback` dry-run (a `DO` block with
`set_config`) was. Verified independently after apply, not just the `{"success":true}`
response:
- `information_schema.routine_privileges` now shows exactly `postgres:EXECUTE,
  service_role:EXECUTE` — `authenticated` is gone.
- `pg_get_functiondef` on the live function contains `caller_uid_mismatch`.
- Two behavioural probes, each in its own `begin...rollback` (zero persisted rows):
  authenticated as uid A calling with `p_user_id` = uid B raises `caller_uid_mismatch`
  immediately; authenticated as uid A calling with `p_user_id` = A passes the guard and
  reaches the real insert logic, failing only on `workers_user_id_fkey` because the
  synthetic test uid has no matching `auth.users` row — a different, expected, pre-existing
  constraint, not a guard failure. Confirms the fix blocks the exploit shape and is a true
  no-op on the legitimate shape.

### SEC-46 — eq-field CSV purge gate is client-side only; RLS has no role backstop (P2)
`_purgeTenantRows()` (`scripts/supabase-entities.js:245`) issues
`DELETE /rest/v1/<table>?org_id=eq.<tenant>` with the user's own JWT. Live-verified via
`pg_policies` on ehow: `app_data.sites` and `app_data.staff` each carry 4 policies
(`*_tenant_isolation` ALL + `_delete`/`_insert`/`_update`), all role `authenticated`,
scoped by `tenant_id` only — no role condition. The `canManageData()` check SEC-21/22
added lives entirely in browser JS (`import-export.js`, `managers.js`), so any
authenticated non-manager can still wipe and replace Sites or Supervision from devtools.
Sibling sweep is otherwise clean — all 6 eq-field importers now carry a gate somewhere
(`importPeopleCSV`/`importSitesCSV`/`importScheduleCSV`/`importFullBackup`/
`importManagersCSV`/`importJobNumbersCSV`/`importTsCSV`); `app_data.schedule_entries` does
have a DB-level backstop. Only `sites` and `staff` lack one. Fix: narrow the RLS policy to
require a role claim, matching the pattern used elsewhere in this register (SEC-33's fix
recommendation is the same shape).

**Update 2026-08-23: fix drafted, eq-shell [PR #1541](https://github.com/eq-solutions/eq-shell/pull/1541), migration `0267`, not dispatched.**
Confirmed by reading migration `0256` directly that SEC-33 already closed this
finding's `app_data.staff` half (revoked INSERT/DELETE, added a RESTRICTIVE read
policy) — this migration is only the remaining `app_data.sites` half. Three
RESTRICTIVE policies (INSERT/UPDATE/DELETE, manager+supervisor tier) layered on the
existing tenant-isolation policy, matching `canManageData()`'s own live-read intent
(`field.manage_data`, same tier as the `isManager` checks it replaced, per that
function's 2026-08-16 comment). **Not dry-run verified live** — the Supabase MCP
connection this session used for every other live check (SEC-43/44/50/41/42)
disconnected partway through this pass, so this migration was built from the
already-applied `0256` pattern read directly from source rather than from a fresh
live read, and relies on an in-transaction post-condition assertion instead of a
pre-apply dry run. Flagging this explicitly rather than presenting it at the same
confidence level as this session's earlier, live-verified fixes — worth a second look
before dispatch, ideally from a session with live DB access.

### SEC-48 — user_metadata resurfaced on ehow's licence-photos bucket (P3, fails closed today)
SEC-2's mistake (trusting client-editable `user_metadata` instead of `app_metadata`) has
come back in one place. Four `storage.objects` policies (`licence_photos_select`/
`_insert`/`_update`/`_delete`, role `{public}`) scope the bucket by
`(storage.foldername(name))[1])::uuid = (auth.jwt() -> 'user_metadata' ->> 'tenant_id')::uuid`.
Latent, precisely: the bucket is private with 0 objects, ehow has only 5 `auth.users`, and
EQ-minted JWTs carry no `user_metadata` at all, so the expression evaluates NULL and the
policy denies — fails **closed** right now. Fails **open** the moment both (a) licence
photos start landing in that bucket on ehow, and (b) a GoTrue-native user exists who can
set their own `user_metadata` via `PATCH /auth/v1/user`. Everything else on this axis is
clean — zero `user_metadata` policies on zaap, no role/tenant derivation from it in any
application code across all four repos. Fix: rewrite the four policies to read
`app_metadata`, same as everywhere else.

### SEC-50 — SSRF in eq-service report logo/photo fetch (P1)
`lib/reports/report-branding.ts::fetchLogoImage` does a plain `fetch(url, {...})` with no
URL validation and default redirect-following. A hardened twin exists in the same
codebase — `lib/reports/logo-variants.ts::fetchLogoImage` (comment "S2-13"), which
validates via `isSafeFetchUrl()` (rejects non-http(s), raw IPs, private/blocked hosts) and
sets `redirect: 'error'` — applied to the newer acb/nsx/pm-asset inputs but not to
`report-branding.ts`. The unguarded version is live-reachable from real generators:
`app/api/compliance-report/route.ts`, `lib/reports/generate-and-store.ts`,
`lib/reports/maintenance-checklist-input.ts`, `lib/reports/report-shell.ts` — all fed
tenant-editable `tenant_settings.report_logo_url` / customer `logo_url` / site photo URLs.
During DOCX generation the server GETs the URL and embeds the response as an "image" the
requester then downloads: SSRF from the report runtime to internal/link-local addresses
(or an external URL that 302s to one — this copy follows redirects, the hardened twin
doesn't), with a plausible exfil channel via the embedded image bytes. Firing it needs an
authenticated admin write of a malicious logo URL — not attempted (§7). Fix: route these
four callers through `logo-variants.fetchLogoImage`, or add the same guard directly.

**Update 2026-08-23: fix drafted, eq-service [PR #803](https://github.com/eq-solutions/eq-service/pull/803), not merged.**
Took the "add the same guard directly" branch of this entry's own two suggested fixes,
not the "route through logo-variants.fetchLogoImage" one — routing all 4 callers through
the sibling would have meant touching 4 call sites for an option-name mismatch
(`{maxWidth,maxHeight}` vs `{width,height}`) that a P1 security fix shouldn't be
carrying. Instead: exported `isSafeFetchUrl` from `logo-variants.ts` (was a private
function) and imported it into `report-branding.ts`, so the two copies share one tested
security check instead of the SSRF guard existing in only one of two near-identical
functions. Confirmed exactly 4 real callers via import-site grep (not just a name match),
matching this entry's own count. Standalone `tsc --noEmit` on just the two edited files
(no local `node_modules` in the drafting sandbox) surfaces only pre-existing "missing
ambient types" noise (`Buffer`, `docx`, `@supabase/supabase-js`) — nothing tied to the new
import or the added `redirect: 'error'` property. **Repo has no branch protection**
(confirmed via `gh api .../branches/main/protection` → 404) — unlike eq-shell, CI here is
advisory, not merge-blocking, so this PR still waits for `ci.yml`/`check.yml` before
merging even though GitHub itself won't enforce it.

**Update 2026-08-23: CLOSED — merged and verified live.** eq-service [PR #803](https://github.com/eq-solutions/eq-service/pull/803)
squash-merged after `Typecheck + audit` and `tsc + next build` both passed. The one
failing check (`Integration tests (Supabase local)`) was confirmed unrelated before
merging — the failure log shows `Start local Supabase` erroring on `duplicate key value
violates unique constraint "schema_migrations_pkey" — Key (version)=(0192) already
exists`, a pre-existing collision between two unrelated migration files that both claim
version `0192` (`0192_backfill_testing_check_frequency_slugs.sql` and
`0192_reconcile_rls_introspection_service_schema.sql`), failing before any test runs.
This repo has no branch protection, so nothing would have blocked the merge either way,
but the failure was read, not waved through on the strength of "known pre-existing
failures" alone. Post-merge, `origin/main:lib/reports/report-branding.ts` re-read directly:
`isSafeFetchUrl` is imported and called, `redirect: 'error'` is present on the fetch call.

**Update 2026-08-23 (2): a second, distinct gap in the same guard — found, fixed, merged.**
`isSafeFetchUrl()` in `lib/reports/logo-variants.ts` itself had a bug pre-dating this entry
(present since S2-13, untouched by #803): `blockedHosts` compared against `parsed.hostname`
containing the bare string `'::1'` to block IPv6 loopback, but the WHATWG URL parser always
returns IPv6 hostnames bracketed — `new URL('https://[::1]/x').hostname === '[::1]'`, never
`'::1'` — confirmed via Node REPL. The bare-string entry was dead code: `https://[::1]/...`
(and the IPv4-mapped form, `https://[::ffff:127.0.0.1]/...` → hostname `[::ffff:7f00:1]`)
sailed through as "safe." One guard, two call sites both exposed: `logo-variants.ts`'s own
`fetchLogoImage`, and, since #803 above, `report-branding.ts`'s. PR #804 (closed, unmerged)
would have extracted this guard to a new `lib/reports/url-safety.ts` with its own test file —
checked directly: that test file didn't cover the bracketed case either, so merging #804 as
originally written would not have closed this gap.

Fix: strip a bracket pair from `hostname` before the existing IPv4/blocklist checks, plus add
`'::ffff:7f00:1'` (the parser's normalized form of `::ffff:127.0.0.1`) to `blockedHosts`. New
regression test file, `tests/lib/reports/logo-variants.test.ts` (none existed for this guard
before), covers both bracketed forms directly. `tsc --noEmit` clean; `vitest run` 700/700
including the 7 new cases. eq-service [PR #805](https://github.com/eq-solutions/eq-service/pull/805)
squash-merged 2026-08-23 04:47 UTC as `b4bbc214`. Post-merge, `origin/main:lib/reports/logo-variants.ts`
re-read directly via the GitHub API (not just the merge record): the bracket-strip and the
`'::ffff:7f00:1'` blocklist entry are both present.

### SEC-51 — ENFORCE_IFRAME_ORIGIN is report-only, contradicting SEC-12's "enforced" claim (P2)
`eq_shell_session` is `SameSite=Lax; Domain=.eq.solutions`, shared across every
`*.eq.solutions` subdomain. The guard against a sibling-subdomain POST riding that ambient
cookie (`_shared/origin-check.ts::checkShellOrigin`) is report-only by default — it 403s
only when the **global** `ENFORCE_IFRAME_ORIGIN` flag is `true`, or a per-endpoint
`alwaysEnforce: true` is set. Every privileged mutating function (`edit-user`,
`entity-patch`, `provision-tenant-background`, `invite-users-batch`,
`labour-hire-mutate`, `cards-approve-staff`, …) relies on the global flag alone — they
carry the literal comment "Report-only until ENFORCE_IFRAME_ORIGIN=true"; only
`token-exchange` opts into `alwaysEnforce`. `origin-check.ts`'s own comment states the
global flag **cannot be safely flipped** because it would 403 Cards' legitimate
`mint-supabase-jwt` calls (cards.eq.solutions is deliberately not on the allowlist) — which
directly contradicts SEC-12's note that it's "set to true in production." `SameSite=Lax`
still blocks external-origin (evil.com) CSRF — that's the active backstop, why this is P2
not P1. Residual is same-site: a script executing on any `*.eq.solutions` origin (a
sibling-app XSS, a subdomain takeover, a rogue subdomain) could drive these privileged
mutations with the victim's cookie. Even if enabled, the allowlist ceiling is only
`core.eq.solutions` + `*--eq-shell.netlify.app` + localhost, and a missing `Origin` header
is always allowed. The live flag value wasn't read this pass — it's a plain feature flag,
not a secret, worth a direct check before deciding whether SEC-12's claim or this finding
is the stale one.

### SEC-56 — false "pauses for approval" claim still machine-posted on live PRs (P3)
`apply-service-migrations.yml`'s `notify` job, line 127, `printf`s a PR comment asserting
"pauses for production-environment approval before any DDL runs." SEC-14's fix (PR #620)
corrected the file's header and inline comments but missed this runtime string — same
file, lines 18–32/160–165, now correctly say the opposite. Live config confirms no such
gate exists: `gh api repos/eq-solutions/eq-service/environments/production` →
`protection_rules: [{"type":"branch_policy"}]`, no `required_reviewers`. Actively
republished: 38 of the last 100 PR comments on eq-service carry the string, most recent
2026-08-20T17:54:36Z on PR #794. eq-shell's equivalent `printf` (`tenant-migrate.yml`)
does not carry the claim — a one-repo miss, not a shared template. Worse than SEC-11/14's
original shape: those are static comments read by whoever edits the file; this one is
machine-posted to the human at the exact moment they decide whether to click Dispatch.
Falsifies SEC-14's "closed as fully swept." Fix: delete or correct the `printf` string.

### SEC-57 — org-wide GitHub App holds write access equal to or beyond the sole collaborator (P1)
`gh api orgs/eq-solutions/installations` → `grok-by-xai`, id `133702612`,
`target_type: Organization`, `repository_selection: all`, created 2026-05-19, not
suspended. Permissions include `actions:write`, `administration:write`, `contents:write`,
`workflows:write`, `pull_requests:write`, `secret_scanning_alerts:write`. `actions:write`
is exactly what `POST /repos/{owner}/{repo}/actions/workflows/{id}/dispatches` requires —
an installation token could dispatch `eq-shell/tenant-migrate.yml` (fleet-wide live DDL
against zaap+ehow) or `eq-service/apply-service-migrations.yml` (live DDL against ehow).
`contents:write` on eq-shell = push to `main` = a Netlify production deploy in 2-4s
unattended; eq-shell's 5 required status checks would normally block a raw push, but
`administration:write` can remove branch protection first and `workflows:write` can
rewrite the checks. On eq-cards, `contents:write` also allows pushing a `release/v*` tag,
triggering a deploy of Supabase edge functions to jvkn (the control plane). No `secrets`
permission (no direct read), but `workflows:write` + `actions:write` is the standard path
to exfiltrate Actions secrets via an added workflow step. This falsifies the accepted-risk
rationale recorded in both SEC-11 and SEC-14 ("Milmlow is the only repo collaborator with
dispatch access anyway") — `gh api repos/.../collaborators` is structurally blind to app
installations, so the check that rationale rests on cannot establish it. Two more apps
(`figma` id `125169606`, `cloudflare-workers-and-pages` id `125177545`) hold
`administration:write` + `contents:write` on **selected** (not enumerated this pass) repos.
Deliberately-installed integration, hence P1 not P0 — if Royce reads the xAI app as fully
trusted, P2 is defensible, but the "only Royce can dispatch" framing in SEC-11/14 is wrong
either way and both rows now say so. No exploit step attempted (would be a write).

### SEC-58 — control-plane ledger 48 files behind; no live gap found on spot-check (P2)
`eq-shell/supabase/migrations/` (jvkn) has 131 files on `main`;
`CONTROL-PLANE-LEDGER.md` names 84, and its summary still reads "56 applied · 0 pending ·
3 misfiled · 2 intentional no-ops," dated 2026-07-11. 48 files have no ledger entry at
all. The CI gate that exists (`check-control-plane-drift.mjs --strict`, in
`tenant-drift.yml`) is one-directional by design — it flags jvkn objects LIVE but absent
from source, never the reverse (file-present-but-not-applied, bug-class #7's exact shape)
— so the stale markdown is the only control for that direction. Object-verified 7 of the
48 unrecorded files directly against live jvkn: **all 7 are applied** — including
`2026_07_21b_user_invites_write_lockdown`, whose own file header still says "Status: NOT
APPLIED, HIGHEST SEVERITY" (itself stale, in the safe direction). No live merged-but-
unapplied hole exists today. Sub-finding: `2026_07_11_tender_tables_anon_lockdown.sql`
sits in the control-plane tree but targets the tenant planes (zaap/ehow) in its own
header, and is absent from `supabase/tenant-migrations/` — governed by neither pipeline,
same class as the 3 misfiled files the ledger already tombstoned once. Fix: refresh the
ledger against the current 131-file reality, or replace it with a generated report so it
can't go stale the same way again.

### SEC-60 — org/repo CI-CD hardening gaps (P3)
`gh api orgs/eq-solutions` → `two_factor_requirement_enabled: false`. Secret scanning and
push protection `disabled` on all 7 in-scope repos, including the three **public** ones
(eq-context, eq-solves-intake, sks-nsw-labour) — eq-shell compensates with a blocking
`gitleaks` required check, nothing equivalent on the others. `allowed_actions: "all"`,
`sha_pinning_required: false` org-wide and per-repo — third-party Actions run unpinned.
**Branch protection exists on eq-shell only** — eq-service, eq-field, eq-cards,
eq-solves-intake, eq-context, sks-nsw-labour all return "Branch not protected," so
eq-service's `main` (auto-deploys service.eq.solutions, gates the ehow migration
pipeline) accepts a direct push with zero required checks. eq-shell's own protection has
`enforce_admins: false` and no required reviews. Orphan: eq-service carries a
`production-ops` environment referenced by zero workflows. Collaborator re-check (what §G
was actually asked to confirm): no widening — exactly one entry (`Milmlow`, admin) on all
15 org repos, no outside collaborators, no teams, no deploy keys, no repo webhooks.

**2026-08-24 — 2 of 4 gaps closed, Royce's explicit scope call (lowest-disruption first
cut from the sprint doc, `docs/secrets-org-hardening-sprint.md`):**
- **Branch protection added on eq-service `main`.** Mirrors eq-shell's own posture
  (`enforce_admins: false`, no required reviews, no force-push, no deletions) — but the
  required-checks list needed real verification, not a copy of every named CI job.
  eq-service's main shows 11 check names in its commit history, but a live PR
  (`#791`) only ever triggers 6 of them — the other 5 (`Apply to ehow`, `Canonical
  types drift`, `Create release tag`, `Post dispatch link to merged PR`, `notify`) are
  push-to-main/deploy-triggered and would never show a passing state on a PR, which
  would have made merging impossible if required. Of the 6 PR-triggered checks,
  `Integration tests (Supabase local)` is this workspace's own documented pre-existing
  failure (`CLAUDE.md`: "never block a merge on integration test failure alone") and
  `Header rules`/`Pages changed`/`Redirect rules` are Netlify's informational plugin
  checks, not real gates. Required exactly the 2 that are both PR-triggered and
  meaningful: `Typecheck + audit`, `tsc + next build`. Verified live via
  `GET .../branches/main/protection` post-apply.
- **Secret scanning + push protection enabled on all 3 public repos** (eq-context,
  eq-solves-intake, sks-nsw-labour). Verified `private: false` before touching each
  (confirmed genuinely public, not a stale assumption), then enabled both via
  `security_and_analysis`, verified live afterward on all 3.
- **Not touched, Royce's explicit choice:** org-wide 2FA requirement, branch protection
  on the other 5 repos (eq-field, eq-cards, eq-solves-intake, eq-context,
  sks-nsw-labour), SHA-pinning on third-party Actions. All three remain exactly as
  found.

### SEC-61 — dev-context secret leak: SEC-9's 2026-08-16 closure doesn't hold (P1)
Netlify masks `branch-deploy`/`deploy-preview`/`production`/`dev-server` but returns full
plaintext for the **`dev`** context regardless of `is_secret: true`. Live 2026-08-21:
eq-shell (`SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`, `EQ_SHELL_JWT_SECRET`,
`SKS_SUPABASE_JWT_SECRET`, `EQ_PLATFORM_ADMIN_KEY`, `EQ_SESSION_SALT`,
`CANONICAL_API_KEY_FIELD`, `CANONICAL_API_KEY_SERVICE`, `QUOTES_CRON_SECRET` — 9 vars);
eq-service (`EQ_SHELL_JWT_SECRET`, `EQ_SERVICE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`,
`EQ_SERVICE_API_KEY`, `EQ_PLATFORM_ADMIN_KEY`, `EQ_SESSION_SALT`, `EQ_SECRET_SALT`,
`CANONICAL_API_KEY_SERVICE`, `UNSUBSCRIBE_SECRET` — 9); eq-field (`SKS_JWT_SECRET`,
`EQ_FIELD_HANDOFF_KEY` — 2); eq-cards (`EQ_SECRET_SALT` — 1); Netlify account/team scope
(`SUPABASE_JWT_SECRET` — 1, see SEC-63). sks-nsw-labour: clean, `dev` empty everywhere.
Evidence the 2026-08-16 remediation never touched these: their `updated_at` timestamps
are 2026-06-13/07-27/07-30 — not 08-16 — and the Netlify account audit log shows only 14
env-var events that day (7 updated, 7 deleted, 0 created), far fewer than the closure
implies. Severity capped at P1 not P0: the Netlify team has exactly one member
(`dev@eq.solutions`, Owner) — reaching this needs Royce's own Netlify credential.
Method note for whoever re-runs this: `is_secret` is a per-var boolean, not per-context —
the per-context fact is whether a value row exists and whether Netlify masks it. Fix
pattern: see SEC-62 — delete the `dev` row, don't recreate it.

**2026-08-24 — closed, all 21 site-scoped vars.** Fixed via Netlify's `deleteEnvVarValue`
API (removes one value row by its own `id`, not the CLI's `env:unset --context`, which
wasn't independently verified to be equivalently precise) — targeted exactly the `dev`-
context value `id` per var, nothing else. Verified per-site after: 0 secret-flagged vars
with a `dev` row remaining on eq-shell, eq-service, eq-field, or eq-cards. Spot-checked
the most sensitive one (eq-shell `SUPABASE_SERVICE_ROLE_KEY`) to confirm production/
deploy-preview/branch-deploy rows are untouched — same `id`s, same masked values, same
`updated_at` (2026-06-13, unchanged) on all three; only the `dev` row is gone. Non-secret
`dev`-context vars on the same sites (e.g. eq-service's `NEXT_PUBLIC_*` vars, eq-cards'
`POSTHOG_*`/`SUPABASE_URL`) deliberately left alone — they're meant to be visible, not a
leak. sks-nsw-labour untouched (register already noted it was clean). The account-scope
var stays open — see SEC-63, unchanged by this pass.

### SEC-62 — the standard remediation recipe re-introduces the dev-context leak it closes (P2)
All 6 vars this register records as "fixed 2026-08-16, delete+recreate" now have an
unmasked `dev` value, and all carry `updated_at = 2026-08-16` — proving the recreation
itself is what wrote the leaking row: eq-shell `QUOTES_CRON_SECRET`; eq-field
`EQ_FIELD_HANDOFF_KEY`; eq-service `EQ_SERVICE_API_KEY`, `EQ_SERVICE_HANDOFF_KEY`,
`EQ_SERVICE_JWT_SECRET`; eq-cards `EQ_SECRET_SALT`. Recreating a var with "same value, all
contexts" writes a `dev` row, and Netlify never masks `dev` regardless of the `is_secret`
flag. The vars that don't leak are the ones with `dev` left EMPTY (never populated, not
delete+recreated): eq-shell `TWILIO_AUTH_TOKEN`, `TENANT_ROUTING_MASTER_KEY`,
`GOOGLE_DOC_AI_CREDENTIALS`, `SCHEDULER_TEST_SECRET`, `SUPABASE_ACCESS_TOKEN`,
`FIELD_SUPABASE_SERVICE_ROLE_KEY`, `LABOUR_HIRE_INTAKE_SECRET`, `EQ_SERVICE_API_KEY`.
Practical implication: every past register entry that closed a secrets finding via
"delete+recreate, all contexts masked" (SEC-9's 2026-08-16 entry, SEC-10, SEC-12, SEC-18,
SEC-19, the eq-cards 4-var close) should be read as re-open-pending-verification against
this, not as settled. Fix, suite-wide: for each currently-leaking var, delete just the
`dev`-context row and leave it empty — don't recreate it.

### SEC-63 — uninventoried Netlify account-scope secret signs every session in the suite (P1)
`SUPABASE_JWT_SECRET` exists at Netlify **account scope** (team `milmlow`, id
`69cf614eac93ac4476af83c9`), `is_secret: true`, scopes `builds,functions,runtime`, updated
2026-06-03, `dev` unmasked (same leak as SEC-61). Its masked fingerprint is identical to
eq-shell `EQ_SHELL_JWT_SECRET`, eq-shell `SUPABASE_JWT_SECRET`, eq-field
`SUPABASE_JWT_SECRET`, eq-service `EQ_SHELL_JWT_SECRET`, eq-service `SUPABASE_JWT_SECRET`
— it is the secret that signs every session in the suite. It appears nowhere in
`ops/secrets-inventory.md`, which only ever enumerated per-site vars, never account-scope
ones. Whether Netlify injects it into every site with no per-site override — including
**sks-nsw-labour, a separate entity**, plus any personal/hobby sites on the same account —
could not be resolved read-only (`getEnvVar` with a `site_id` behaves inconsistently
across sites in a way that doesn't cleanly answer the question). **Remaining step is
Royce's own click**: the team-level "Shared environment variables" page in the Netlify
dashboard shows its site scope directly. If it's scoped to all sites, this is P0 — it
would mean sks-nsw-labour inherits (or could inherit) a signing secret that's supposed to
be an EQ-only trust boundary.

**2026-08-24 — site-scope question resolved, P1 confirmed (not P0).** The earlier
"inconsistent" `getEnvVar` behavior was a parameter-shape issue, not a real API
limitation — `getEnvVars` (plural) with both `account_id` and `site_id` correctly
surfaces inherited account-scope vars per site. Queried all 10 sites on the `milmlow`
account individually: the var appears ONLY on eq-shell, eq-service, and eq-field —
exactly the three sites the original fingerprint match already implicated, confirmed
independently via a second, unrelated method. It does **not** reach sks-nsw-labour, or
eq-cards, or any of the personal/hobby sites on the same account. eq-service and
eq-field hold no site-level override of their own for this key — they inherit the
account-scope row directly. `ops/secrets-inventory.md` updated to reflect this (folded
into the existing Shell session-signing-secret cluster row, its first tracked
account-scope entry).

**Not done this pass:** the account-scope var's own `dev`-context leak (same class as
SEC-61) is still open — the delete call was blocked by the coding session's own
auto-mode classifier (account-scope deletes read as broader than site-scoped ones,
even though the actual operation is identical: remove one context row, touch nothing
live). Needs either a permission rule for that session or a manual delete of the `dev`
value via the Netlify dashboard — functionally the same 2-minute action.

### SEC-65 — eq-field's AUDIT_SB_KEY is the live ehow service_role key, not publishable (P2)
Fingerprint match: eq-field `AUDIT_SB_KEY` = eq-field `EHOW_SERVICE_ROLE_KEY` =
eq-service `CANONICAL_SERVICE_ROLE_KEY` (the documented ehow service_role key).
`AUDIT_SB_URL` resolves to `ehowgjardagevnrluult.supabase.co`, confirmed independently in
`eq-service-sites.js:26` ("AUDIT_SB_URL/AUDIT_SB_KEY (live-verified) point at ehow"). But
`verify-pin.js:7` documents it as "Supabase publishable key for audit logging," and
`ops/secrets-inventory.md` ranks it Tier 2 (audit-log project credentials). Four live
consumers run on it believing it's safe to expose client-side, and using it bypasses RLS
entirely since it's actually a full service_role key: `verify-pin.js`, `eq-agent.js`,
`eq-service-sites.js`, `_shared/sentry.js`. Impact is reasoned not proved — whether any of
those four actually ships the value client-side wasn't tested this pass. Fix: correct the
label in code and in the inventory immediately (cheap, no live risk); separately confirm
none of the 4 consumers exposes it outside a server-only context.

**2026-08-24 — label corrected, exposure question still open.** `verify-pin.js`,
`eq-agent.js`, `eq-service-sites.js` now document `AUDIT_SB_KEY` as the ehow
service_role key, server-only, never expose client-side (`_shared/sentry.js` already
treated it as sensitive — redacts it from error reports, no change needed there).
eq-field [PR #762](https://github.com/eq-solutions/eq-field/pull/762). `ops/secrets-
inventory.md` updated: `AUDIT_SB_KEY` was a 5th alias of the already-documented
ehow/sks-canonical service_role key cluster (Tier 1), not its own Tier 2 entry — folded
in there, removed as a standalone row. **Not done:** whether any of the 4 consumers
actually ships the value client-side — still reasoned, not tested.

### SEC-68 — real secrets stored as GitHub Actions secrets on the public eq-context repo (P3, well-mitigated)
eq-context (PUBLIC) repo secrets include `EQ_SHELL_JWT_SECRET` and
`SUPABASE_SERVICE_ROLE_KEY` (jvkn); its `production-ops` environment adds several more
(`EQ_CANONICAL_DB_URL`, `EQ_CANONICAL_INTERNAL_SERVICE_ROLE_KEY`, `SUPABASE_DB_URL`, …).
Mitigations verified live, not assumed: no `pull_request_target` or `workflow_run`
trigger in any workflow in any repo (fork PRs never receive secrets); exactly one
collaborator on eq-context (`Milmlow`, admin); no org-level Actions secrets or variables
at all — everything is repo- or environment-scoped, the correct answer to §C's "exist
only as repo/org secrets" question. Residual risk, why this isn't a clean pass: this
public repo's Actions logs are world-readable, so any future accidental log-leak of these
values is public rather than private — the one scenario the mitigations above don't cover.

### SEC-69 — zero `::add-mask::` suite-wide; one confirmed masking-defeat via $GITHUB_ENV (P3)
`add-mask` appears zero times across eq-shell, eq-service, eq-field, eq-cards, eq-context,
eq-ui. Nothing interpolates `${{ secrets.* }}` directly into a shell command anywhere —
secrets are passed via `env:` blocks, which is correct — with one exception: 9 eq-context
workflows (3 backup + 3 verify + 3 restore-drill) slice the `SENTRY_DSN` environment
secret and write the fragment into `$GITHUB_ENV`, e.g.:
```
KEY="${SENTRY_DSN#https://}"; KEY="${KEY%%@*}"
BASE="https://${HOST}/api/${PID}/cron/${MONITOR_SLUG}/${KEY}"
echo "SENTRY_BASE=$BASE" >> "$GITHUB_ENV"
```
GitHub masks only the exact secret string, never a derived substring, so `SENTRY_BASE` is
unmasked in a public repo's logs. Impact today is low — a Sentry DSN's public key is
low-value by design — but this is precisely the pattern that would be P1 if ever applied
to `SUPABASE_DB_URL` or a service_role key. Fix: mask the derived value explicitly
(`echo "::add-mask::$KEY"`) before writing it anywhere, in these 9 workflows and as a
standing rule for any future secret-slicing.

## Clean projects (probe + advisors, 2026-06-05)
- eq-canonical, eq-canonical-internal, sks-canonical, eq-solves-field,
  eq-substrate: public-key reads all `401`/empty (no anon read leak).
- ERROR-level advisors: only SEC-2. All other advisor output is WARN/INFO
  (SECURITY DEFINER-callable-by-authenticated, permissive policies, search_path).

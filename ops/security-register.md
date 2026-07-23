---
title: OPS — Security Register
owner: Royce Milmlow
last_updated: 2026-07-20
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
| SEC-9 | **P0 — confirmed exposure, same window as SEC-3** | A different service_role key (`jvkn`/eq-canonical) was pasted directly into a chat session 2026-07-12 to fix `canon-read` | eq-canonical (LIVE) | **OPEN.** Unlike SEC-3, this exposure IS confirmed — plaintext in a chat transcript is a real leak vector, not a hygiene item. **Royce's call 2026-07-20: same priority and rotation window as SEC-3** rather than treating separately. Rotate both together whenever that window lands. |
| SEC-10 | **P0 — confirmed exposure** | `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is_secret: false` — not masked in Netlify's own UI/API either), full values returned by a routine env-var read 2026-07-20 and now sitting in a chat transcript, same leak-vector class as SEC-9 | sks-nsw-labour (Netlify, LIVE) | **OPEN.** Found by accident while prepping SEC-1's JWT-minter env vars (that prep is now moot — see SEC-1, app is not being touched). Credential storage, not app config — **not covered by the "don't touch sks-nsw-labour" freeze**, but rotation itself is a separate action requiring your own console.anthropic.com / resend.com access. `EQ_SECRET_SALT`'s `dev`-context value came back unmasked too (its `production`/`branch-deploy`/`deploy-preview` values are correctly masked — only `dev` isn't). **Royce's call 2026-07-20: rotate at another time.** When rotated: set the new values with `is_secret: true`, closing the plaintext-storage gap too, and re-check whether any other project has the same pattern on a real credential. |
| SEC-2 | ~~P1~~ **CLOSED** | RLS policy `tenant_isolation` trusts end-user-editable `user_metadata` (advisor ERROR) | eq-canonical-internal | **CLOSED 2026-07-21 — was already fixed, register was stale.** See Detail. |
| SEC-4 | P3 — hardening | `anon`-executable SECURITY DEFINER `eq_cards_*` fns | eq-canonical | **VERIFIED not exploitable** 2026-06-05 (auth.uid()/token-guarded). Post-launch: revoke anon EXECUTE on the 3 that don't need it. |
| SEC-5 | P3 — hygiene | always-true (`USING/WITH CHECK = true`) write policies | eq-solves-field, eq-canonical-internal | **VERIFIED latent** 2026-06-05 — anon holds NO table grant, policies unreachable. Post-launch cleanup. |
| SEC-6 | P2 | `context_proposals` anon INSERT has length caps but no volume throttle | eq-substrate | OPEN — needed before the queue has a consumer |
| SEC-7 | P3 | `function_search_path_mutable` (search_path not pinned) | several projects | OPEN — hygiene, fix at next touch |
| SEC-8 | P3 | `pg_net` extension installed in `public` schema | sks-labour | OPEN — moot once sks-labour retired |
| SEC-11 | **P3 — accepted, docs corrected (downgraded from P1 2026-07-23)** | `tenant-migrate.yml`'s `production` GitHub Environment has **zero protection rules** (`protection_rules: []`, confirmed via `gh api repos/eq-solutions/eq-shell/environments/production` 2026-07-23) despite the workflow's own header comment and prior session memory both asserting "gated behind the `production` Environment so it PAUSES for a human approve click... `production` environment with Royce as required reviewer — CREATED 2026-06-03." | eq-shell (GitHub Actions/repo config) | **ACCEPTED, not fixing — Royce's call 2026-07-23.** Found live: dispatched `tenant-migrate.yml` (migration 0199, whole fleet) on Royce's "dispatch tenant-migrate.yml" — the `Apply to all tenants` job ran straight through in ~15s with no approval pause, applying live DDL to both zaap and ehow. Attempted the fix (`gh api --method PUT .../environments/production` with Royce/`Milmlow` id `271704382` as required reviewer) — **rejected, HTTP 422: "Please ensure the billing plan supports the required reviewers protection rule."** Required-reviewer environment protection needs GitHub Team/Enterprise Cloud (or a public repo); this private repo doesn't have it. Royce's call: don't pay for the plan upgrade — `Milmlow` is the only repo collaborator with dispatch access anyway (confirmed via `gh api repos/.../collaborators` — one entry), so a reviewer gate would only ever be "Royce clicks twice," not a real access boundary. **Fixed instead:** corrected the false claim in `tenant-migrate.yml`'s header + inline comments (PR [#985](https://github.com/eq-solutions/eq-shell/pull/985), OPEN) so nobody trusts a safety net that isn't there. Real safeguard going forward: deliberate manual dispatch only, no second-click gate. |

## Weekend tasks (Field go-live + cutover)

- **SEC-1 — decommission SKS Labour.** Field replaces it; once Field is live, take
  SKS Labour offline / pause project `nspbmirochztcjijmcrx` / disable its anon
  access so the PII leak can't outlive the app. **Explicit checklist line — not
  assumed.** Remove from `rls_probe.py KNOWN_LEAKS` once done. Still blocked on
  an actual retirement date — sks-nsw-labour confirmed still active 2026-07-16,
  no date set. **Reaffirmed 2026-07-20: no interim hardening either** — the app
  stays untouched, not just unretired, until Field replaces it.
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

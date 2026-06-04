---
title: EQ Platform — DB-Verified Live State (2026-06-03)
owner: Royce Milmlow
last_updated: 2026-06-03
scope: Ground-truth snapshot of the EQ platform, verified against live systems
read_priority: critical
status: live
---
# EQ platform — VERIFIED live state (2026-06-03)

> **Read this before assuming something isn't built.** Every fact below was checked against the **live system** (Supabase queries, deployed apps, git branches) on 2026-06-03 — not from design docs. Design docs, STATE files, and recon summaries **lag reality**: repeatedly during the 2026-06-03 session, things assumed "not built" were already built or in-flight. **This snapshot will drift — re-verify against live before relying on it.** When live and docs disagree, **live wins.**

## Canonical / data homes (verified by DB inspection)
- **eq-canonical = `jvknxcmbtrfnxfrwfimn`** is the LIVE home for EQ Cards + the worker model. Legacy Cards project `hshvnjzczdytfiklhojz` was **decommissioned 2026-05-24** (per eq-cards `.dart-defines*`).
- **The worker-house EXISTS and is POPULATED** in eq-canonical `public`: `workers` (38), `worker_credentials` (779), `worker_invites` (37), `tenants` (4), `org_memberships`, `licences`, `licence_types` (13). The **SKS "Technology NSW" team is already seeded** (migration `0013`). The training-matrix import was effectively already done — do NOT build an importer for it.
- **`org.id == tenant.id`** (1:1, same UUID per slug — e.g. sks = `…0002`). A worker's `org_id` IS their `tenant_id`.
- Other projects: eq-canonical-internal `zaapmfdkgedqupfjtchl` · sks-canonical `ehowgjardagevnrluult` · sks-labour (SKS Field tenant) `nspbmirochztcjijmcrx` · eq-solves-field `ktmjmdzqrogauaevbktn`.

## Auth (verified)
- `custom_access_token_hook` is **ENABLED** on eq-canonical (since ~2026-05-24). It stamps `tenant_id`/`eq_role` from **`shell_control.users`** (~5 rows — managers only).
- **Workers (`public.workers`) are NOT in `shell_control.users`** → email/phone OTP sign-in gets no `tenant_id` → "No workspace access" → 0 of 37 invites claimed. **This is "GATE A."** Decision: `eq/identity/gate-a-decision-2026-06-03.md` (Option A — provision at claim).

## In-flight (verified by git — do NOT fork these)
- eq-cards branch **`claude/otp-tenant-fix`**: admin onboarding + worker schema + claim flow + a phone-OTP→shell-JWT auth fix. Migrations live: **0010–0015**. `eq_cards_claim_invite` promotes `worker_credentials`→`licences` once at claim. The GATE A fix should be reconciled ONTO this branch, not a new one.

## Deploy topology (verified)
- **`core.eq.solutions/sks/field` is served by the `sks-nsw-labour` repo (v3.10.x)** — SEPARATE from `eq-solves-field` (v3.5.x). sks-nsw-labour *ports* features from eq-field; they are NOT the same deploy.
- The SKS-Field **PIN re-prompt** = sks-nsw-labour `verify-pin` vs the shell's Supabase JWT — likely just a **missing `SUPABASE_JWT_SECRET`** env on the SKS-Field Netlify site.

## Security (verified — already remediated)
- sks-canonical (`ehowgjardagevnrluult`): RLS **ON**, anon grants **revoked** (fixed in the 2026-05-31 audit). The "RLS off + open key" framing is **stale**. Remaining: a service_role key in a local gitignored `.env` (`eq-quotes-port`) used by `eq-quotes-sks` on Fly — rotate as hygiene.

## To move worker-creds live (Royce-gated)
phone list ×~60 · evidence export (scans + numbers + expiries) · **GATE A** auth sign-off · security key rotation (hygiene). The worker-owned-credentials architecture is the **locked design** (`eq/identity/worker-credentials-model-2026-05-31.md`, owner: Royce) — Phase 1 (seed + self-maintain) build is just blocked on those inputs; Phase 2 (live-link grants / multi-employer / "subbie with N contractors") is deferred until a 2nd business consumes.

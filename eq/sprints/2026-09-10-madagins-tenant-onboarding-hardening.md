---
title: Sprint — madagins tenant-onboarding hardening
owner: Royce Milmlow
last_updated: 2026-09-10
scope: eq-field/eq-shell/eq-cards SKS-hardcode audit + madagins live-health check
read_priority: standard
status: live
---

**This is a continuation, not a parallel track.** The primary record for
madagins onboarding is [`eq/sprints/2026-09-09-tenant-onboarding-sprint.md`](2026-09-09-tenant-onboarding-sprint.md)
(Royce-directed, six `/decide` passes, the actual tenant-isolation call) plus
`eq/sprints/2026-09-09-provisioning-completeness-followup.md`. This session
didn't know that doc existed until late in its own audit — read it first if
picking this up next, rather than treating anything below as the origin
story.

# Sprint: madagins tenant-onboarding hardening — 2026-09-10

**Trigger:** a session confirming Royce's mental model of the per-tenant SaaS
architecture ("fix once in Field, every tenant gets it; data stays isolated
per tenant") ran the live tenant check to verify it, and found a second real
tenant — **madagins** — had gone active the day before (2026-09-09),
undocumented in any substrate file. `/decide` on the architecture question
flagged "no onboarding runbook" as the biggest make-it-work risk; this sprint
was scoped to pressure-test that against madagins specifically.

**Headline correction, stated plainly because it was said out loud mid-session
and needs to survive past the correction itself:** this session initially
characterized madagins's onboarding as evidence the architecture "just
works." That was wrong. `eq-shell/scripts/check-provisioning-completeness.mjs`'s
own header (written 2026-09-09) says provisioning **failed twice** against a
from-scratch project and calls it "the still-stuck eq-tenant-madagins
project." Treat that framing, not the first one, as what happened.

**Second correction, found mid-audit:** most of what this session went
looking for was already known. digest.md's "Waiting on you" (2026-09-09) already
lists 3 of the exact gaps this audit re-derived (apprentice-module tenant
fallback, `sites.js`/`managers.js` string-gating on `'sks'`,
`check-tenant-drift.mjs`'s fixed project list) as deferred pending Royce's
call. eq-field alone has **6+ active branches/worktrees** already working
this exact seam: `chore/madagins-provision-verify`,
`claude/canon-read-madagins`, `claude/tenant-provision-generator[-hardening]`,
`claude/tenant-provision-security-fixes`, `worktree-madagins-security-invoker-fix`,
plus 5 PRs merged 2026-09-09/10 (#971–#975). **This is not a fresh discovery —
it's a large, already-in-flight, multi-session effort.** A future session
picking this up should check those branches before re-doing this audit.

---

## Verified live state of madagins (as of 2026-09-10)

| Layer | Check | Result |
|---|---|---|
| Control plane | `shell_control.tenants` / `tenant_routing` (jvkn) | Active, own dedicated project `ornndtbdkxfsewspbrwk` (region ap-southeast-2) — tenant isolation rule holding, not just on paper |
| Extensions | `pg_cron`, `pg_net` | ✓ present (pg_cron was missing initially, manually re-enabled to unblock provisioning) |
| Extensions | `vector` | ✗ **missing** — impact not checked this session |
| Schemas | `shell_control`, `wipe_backup` | Both absent. `wipe_backup` expected absent (SKS legacy backup cruft). `shell_control`'s absence impact is unclear — not confirmed whether ehow's local copy is load-bearing or vestigial |
| Core tables | `app_data.{customers,sites,staff,teams,team_members}` | ✓ all present |
| Service | `service` schema | Only 5 tables (vs. dozens on ehow) — eq-solves-service's own migration pipeline has not run against this project |
| Service — resolved | Is this a gap? | **No — confirmed with Royce: madagins will not require EQ Service.** Deliberate, same sequencing precedent as SKS's own Stage-1 go-live (`eq-shell/docs/runbooks/sks-go-live.md` hid the Service tile at launch too). No action needed. |

**Not completed this session:** the authoritative full diff needs
`node scripts/check-provisioning-completeness.mjs --ref=ornndtbdkxfsewspbrwk`
run for real (needs `SUPABASE_ACCESS_TOKEN`, not available in this shell) —
this session's spot-checks cover only the specific objects the script's own
header names, not its complete ~62-object reference-tenant diff.

**Doc drift found in passing:** `eq-shell/docs/runbooks/sks-go-live.md`'s Step
0 SQL targets `shell_control.module_entitlements` — that table is actually at
`public.module_entitlements` (a second, newer-looking `public.org_module_entitlements`
also exists, not investigated). The runbook would error if run verbatim today.

---

## Hardcode sweep — eq-field / eq-shell / eq-cards

Grepped all three repos for the SKS tenant UUID (`7dee117c-98bd-4d39-af8c-2c81d02a1e85`)
and ehow's project ref (`ehowgjardagevnrluult`). ~190 files matched; the
overwhelming majority are legitimate (migrations scoped to SKS by design,
tests, changelog prose). **Caught and corrected a staleness bug in this
sweep itself:** eq-field's local checkout was several commits behind
`origin/main` when the first pass ran, and the missing commits touched
`supabase.js` and `verify-pin.js` directly — both were re-read against
current `origin/main` before anything below was written down as a finding.

### Fixed this session
- **`eq-field/_headers` (CSP)** — `connect-src`/`wss:` allowlisted
  jvkn+zaap+ehow only, not ornn. Any direct browser→Supabase fetch to
  madagins's own project was silently CSP-blocked. Fixed, committed, pushed,
  PR opened: [eq-field#976](https://github.com/eq-solutions/eq-field/pull/976).
  **Not merged** — Royce's call.

### Already known, already logged (digest.md "Waiting on you", 2026-09-09) — not re-actioned here
- `check-tenant-drift.mjs`'s `TENANT_DATA_PLANES`/`CANONICAL_PROJECTS` lists
  are hardcoded to exactly zaap+ehow — confirmed still true, re-read fresh
  from `origin/main` (not the stale local copy). This is the main
  multi-tenant governance tool (anon-grant violations, cross-tenant drift,
  security-definer view checks) and it currently has **zero coverage of
  madagins**. Deferred pending Royce's call per digest.md — not this
  session's to resolve.
- eq-field's Apprentice-module unrecognized-tenant fallback, and
  `sites.js`/`managers.js` gating Shell-ownership on the literal string
  `'sks'` — both already flagged, both already deferred pending Royce.

### New finding, not yet in digest.md's known list
- **`eq-field/scripts/{roster,timesheets,leave}-adapter.js`** each carry a
  `CANONICAL_{ROSTER,TS,LEAVE}_DB_REFS = ['ehowgjardagevnrluult']`
  "ground-truth fallback" for a known Shell-embed restore bug (v3.5.286).
  Comments explicitly reasoned about only 2 tenants ("can never over-trigger
  on eq/zaap"). Confirmed these 3 files were **not** touched by the commits
  eq-field's stale checkout was missing, so this reading is current. Madagins
  gets no equivalent protection if it hits the same restore bug — degrades to
  primary-path behaviour rather than crashing, so lower severity than the CSP
  gap, but same root cause (built when there was one tenant, never revisited).
  Not fixed this session — flagging for the same pass that generalizes
  `check-tenant-drift.mjs`, since it's the same shape of fix.

### Needs Royce's call, not a bug
- **`eq-shell/netlify/functions/comms-jobs.ts` and `comms-weekly-digest.ts`**
  hardcode `SKS_TENANT_ID` for the Comms crew-roster feature. Unclear whether
  Comms is meant to ever be tenant-generic, or is intentionally SKS-only like
  SKS NSW Labour. Not actioned — needs a product decision, not a code fix.

### Checked, confirmed fine — no action needed
- `verify-pin.js`'s `DATA_TENANT_IDS` map is hardcoded to `eq`+`sks` by
  default but has a working `DATA_TENANT_IDS_JSON` env-var override already
  built in (same pattern as `CORE_ONLY_TENANTS_JSON`). Needs confirming
  that's actually set for madagins on Netlify — a config check, not a code
  change.
- `sksSupabaseClient.ts` / `mint-sks-jwt.ts` — explicitly labelled
  `sks-legacy` last-resort fallback (tried only if `proxy`/`routed` both
  fail), not a silent bug.
- `supabase.js`'s `JWT_INPLACE_TENANTS` — already generalized to an empty
  set; the real mechanism (`JWT_INPLACE_TABLES`) is table-keyed, not
  tenant-keyed.
- `provision-sks-tenant.mjs` — historical one-time script, superseded by
  `provision-tenant-background.ts`.

---

## What this sprint did NOT cover

- eq-solves-service's own source — not cloned anywhere under `C:\Projects`
  this session could find. Not pursued further once Service was confirmed
  out of scope for madagins, but worth locating before any *future* tenant
  that does need Service onboards.
- The full `check-provisioning-completeness.mjs` reference-tenant diff
  (needs the management API token).
- Whether `DATA_TENANT_IDS_JSON` / `CORE_ONLY_TENANTS_JSON` are actually set
  for madagins on eq-field's Netlify deployment.

## Suggested next owner

Given how much of this is already mid-flight elsewhere, the highest-value
next step is probably **reconciling this doc against the existing
`tenant-provision-*` branches** rather than opening new work from it — several
of the "needs Royce's call" items here may already have an answer sitting in
one of those branches' own PR descriptions.

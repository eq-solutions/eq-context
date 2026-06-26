---
title: Plan — close control-plane governance + the consent-gated card read
owner: Royce Milmlow
last_updated: 2026-06-25
scope: Two-workstream plan to close control-plane governance and the consent-gated Field card read, written to run around active console work
read_priority: high
status: live
stage: "PLAN — coordination-aware (consoles live elsewhere). Execute the control-plane steps only when a control-plane console is free; the rest is safe in parallel."
relates_to: canonical-consolidation-roadmap-2026-06-25.md (Phase 0), ticket-field-licence-read-2026-06-25.md
---

# Plan: control-plane governance + the consent-gated card read

The world-class version of the eq-shell follow-up. Two workstreams. Written to run
**around** active console work, not race it.

## North stars (measure every step against these)
- **The worker owns their card** → the gate is the worker's **consent**
  (`org_access_requests.sharing_scope`), NOT the employer's need or passive membership.
- **Defined throughout** → no live control-plane object exists outside source control;
  drift fails CI.

## Verified anchors (2026-06-25, read-only, zero-collision)
- **Drift is systemic, not a one-off.** `eq_get_org_licences`, `eq_field_get_worker_summary`,
  `eq_get_licences_expiring_within` are ALL live in jvkn and absent from eq-shell source.
  (`eq_get_org_licences` is mine — applied via MCP this session; tracked in jvkn history,
  never reached eq-shell source. Same drift class.)
- **The consent control already exists and is granular:** `org_access_requests`
  = `(org_id, worker_user_id, status, requested_by, responded_at, sharing_scope, …)`.
  The worker grants an org a **scope**. 7 rows live.
- **But reads don't honor it yet.** `eq_get_org_licences` gates on `org_memberships`
  (passive association: `invited_by/accepted_at/role/status`, 14 rows), NOT on
  `sharing_scope`. So the worker's explicit grant isn't enforced on any read path today.
- jvkn control-plane migrations live in `eq-shell/supabase/migrations/` (`YYYY_MM_DD_<name>.sql`).

## Decisions Royce owns
| # | Decision | Recommendation |
|---|---|---|
| **D1** | Build the consent-gated worker-summary read (un-blank RTW/emergency in Field)? | **Yes** |
| **D2** | Gate target: passive `org_membership` (matches today's licence read) **or** the worker's `sharing_scope` grant? | **`sharing_scope`** — it's the worker-owns-card answer; membership is only an interim if scope semantics need work |
| **D3** | CI drift gate: warn-only or fail-build on control-plane drift? | **Fail-build**, switched on *after* the reconciliation makes source clean |

## Workstream A — close Phase 0 (control plane = defined throughout)
- **A1 · Reconcile the drift** — one eq-shell PR that commits every live-but-unsourced
  jvkn object (the 3 RPCs above + whatever a live-vs-source diff finds). Mechanical,
  idempotent (`CREATE OR REPLACE`). *Needs a free control-plane console.*
- **A2 · CI drift gate** — extend the existing drift check (`check-tenant-drift.mjs`)
  to flag jvkn objects not in source → fail the build. *Author now (new script, safe);
  enable after A1 makes source clean.*
- **A3 · Process rule** — all control-plane changes via the governed pipe only; no
  ad-hoc MCP applies (me included). Record in eq-shell CLAUDE.md.
- **Done when:** jvkn source == live, and new drift fails CI.

## Workstream B — the consent-gated card read (B2 → unified)
- **B0 · Nail `sharing_scope` semantics** (type, values, how it should gate). *Read-only,
  safe now.* Determines B1's gate precisely.
- **B1 · Build the gated read** — `eq_field_get_worker_summary_v2(p_org_id, p_worker_id)`
  returning RTW + emergency, gated on the worker's `sharing_scope` grant (per B0/D2).
  Mirrors `eq_get_org_licences`. eq-shell migration, governed. *Needs a free console.*
- **B2 · Wire Field to v2** — `eq-field scripts/people.js _fetchWorkerSummary` → v2.
  Un-blanks the RTW/emergency panel. *eq-field PR — my lane, independent, but inert
  until B1 lands.*
- **B3 · Converge (north star, later)** — fold licences + RTW + emergency + identity
  into ONE `sharing_scope`-gated card read; retrofit the licence read off passive
  membership onto `sharing_scope`. Field calls one seam; the worker flips one switch.
- **Done when:** the RTW/emergency panel works in Field, gated on the worker's revocable consent.

## Coordination matrix (consoles are live — this is the important part)
| Lane | Steps | When |
|---|---|---|
| **SAFE NOW — zero console collision** | B0 (read-only jvkn) · author A2's script · author B1 spec · keep this plan current | Anytime, me |
| **NEEDS A FREE CONTROL-PLANE CONSOLE** (touches jvkn / eq-shell `main` your console is on) | A1 reconcile · A2 enable · B1 v2 migration | When consoles settle, or you in-console |
| **MY LANE — independent repo** | B2 Field PR (eq-field) | After B1 lands (inert before that) |

**Critical path:** D2 → B0 → B1 → B2(Field). A1 → A2 runs in parallel. The only hard
serialization is "don't run A1/B1 while a console is mid-flight on eq-shell `main`."

## What I can do right now without touching your consoles
B0 (sharing_scope semantics), the v2 spec, the CI-gate approach, and this plan. Every
control-plane apply waits for a free console — by design.

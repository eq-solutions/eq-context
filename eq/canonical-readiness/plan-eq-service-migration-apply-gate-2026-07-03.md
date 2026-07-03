---
title: Plan — a governed apply path for eq-solves-service's own tenant-plane migrations
owner: Royce Milmlow
last_updated: 2026-07-03
scope: Findings + recommendation for closing the apply-governance gap in eq-solves-service's supabase/migrations/ lineage (writes to ehow, same tenant plane eq-shell's One Pipe governs)
read_priority: high
status: proposal — awaiting Royce's decision, nothing implemented
relates_to: SCHEMA-GOVERNANCE.md (eq-shell), eq-intake/CLAUDE.md Rule 2 (schema ownership table), plan-control-plane-governance-and-card-read-2026-06-25.md (same shape of problem, jvkn control plane instead of ehow tenant plane), sessions/2026-07-03.md
---

# Plan: a governed apply path for eq-solves-service's own migrations

Triggered by the 2026-07-03 eq-shell drift-gate incident: the gate went red on
`service.customer_contacts`/`service.site_contacts` (ehow), and the first read was
"rogue out-of-band change." It wasn't — it was **eq-solves-service migration
`0167_contacts_canonical_cutover.sql`, merged via PR #410, a completely legitimate,
documented, reviewed change.** Verified byte-for-byte against the live DB. The
confusion was structural, not a rule-breaking incident, which is the point of this doc.

## Verified anchors (2026-07-03, read-only)

- **eq-solves-service's `supabase/migrations/` targets the exact same database**
  eq-shell's tenant-migrate.yml governs: `ehowgjardagevnrluult` (confirmed via
  `.env.local` + `SUPABASE_PROJECT_REF` in `.github/workflows/canonical-types-drift.yml`).
  This is not a separate sandbox — it's the SKS tenant plane.
- **eq-solves-service has no CI step that applies its migrations anywhere.** Grepped
  every workflow (`ci`, `check`, `integration`, `canonical-types-drift`, `data-quality`,
  `backup`, `notify-substrate`, `supabase-advisors`) for a supabase-apply step. None
  exists. `0167` reached live ehow via a developer running the Supabase CLI (or MCP)
  by hand, sometime after PR #410 merged (2026-07-02T20:13:23Z) — no dispatch, no
  `production`-environment human-approval gate like eq-shell's.
- **eq-intake's new CLAUDE.md (this session) already codifies the ownership boundary**
  and treats this as settled, correctly: `service.*` is eq-solves-service's own
  lineage, distinct from `app_data.*` (eq-shell's One Pipe). **That boundary is not
  the gap.** The gap is that the `service.*` lineage has an author-and-review step
  (PR review) but no apply-gate step — merge and "live" are two different unguarded
  moments with nothing checking what happens between them.
- **eq-shell's drift gate scans all of ehow**, not just `app_data.*` — CHECK 2
  (anon-grant) and CHECK 5 (policy-lint) are schema-agnostic by design (a real
  security invariant doesn't care which repo owns the table). That's correct and
  should stay. But it means an eq-service migration can trip a REQUIRED eq-shell
  gate — blocking every eq-shell PR — with zero warning to whoever wrote it, and no
  way for them to have caught it before merging their own PR.
- **A parallel, structurally identical gap exists in eq-cards**, on a *different*
  plane: eq-cards' `supabase/migrations/` targets `jvknxcmbtrfnxfrwfimn` (the
  control plane), and per its own RUNBOOK.md, schema there is "managed directly in
  eq-canonical" via ad hoc MCP applies — no migration-apply CI at all. This is
  **already tracked** in `plan-control-plane-governance-and-card-read-2026-06-25.md`
  (Workstream A: "all control-plane changes via the governed pipe only; no ad-hoc
  MCP applies"). Not duplicating that plan here — flagging that it's the same shape
  of problem on a sibling database, in case the fix ends up shared tooling.

## What actually went wrong here (precisely)

Nothing at the DDL level. The failure was **cross-repo visibility**: eq-shell's gate
has no way to know "a migration merged in eq-service 7 hours ago is why ehow's shape
just changed." It only sees the resulting live state, with no author, no PR link, no
context — so a green-lit, reviewed schema change and a rogue hand-edit look identical
to the gate. That indistinguishability is the actual bug, not the DDL itself.

## Decisions Royce owns

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | Should eq-service's `service.*` migrations get their own dispatch-gated apply pipeline (mirroring `tenant-migrate.yml`), reuse a shared one, or stay manual with a lighter guard? | (a) Own gated pipeline, (b) fold into eq-shell's existing pipe (cross-repo — awkward, eq-shell would need read access to eq-service's repo), (c) stay manual, add a pre-merge local check + a merged-but-unapplied lag detector | **(a)**, scoped small — see Workstream below |
| **D2** | Should eq-service's CI run the same anon-grant/RLS-policy-lint invariant on its own diff before merge, so this class of issue is caught locally instead of surfacing as an unrelated eq-shell gate failure? | Yes / No | **Yes** — cheap, reuses eq-shell's existing script, catches the exact failure mode that happened here |
| **D3** | Same question for eq-cards / jvkn (already tracked separately) — bundle into one push, or keep as two independent efforts on their own timelines? | Bundle / keep separate | **Keep separate** — different plane, different plan already exists, no reason to couple them |

## Recommended shape (small, not a rebuild)

**D1 answer, sized down:** eq-service doesn't need eq-shell's full apparatus
(fleet-runner across every tenant, `tenant_routing` lookup, ledger reconcile) — it
writes to exactly one database. A minimal version:

1. **New workflow in eq-solves-service**, `apply-service-migrations.yml`, mirroring
   `tenant-migrate.yml`'s shape but simplified to one target (`ehowgjardagevnrluult`):
   - PR → read-only plan job (which of `supabase/migrations/*.sql` are pending on live
     ehow, by filename, same style as eq-shell's ledger check).
   - `workflow_dispatch` → apply job, gated behind a `production` GitHub Environment
     with Royce as required reviewer (same primitive eq-shell already uses — cheap to
     replicate, no new infra).
   - This closes the actual hole: right now "merged" and "live" have no audit trail
     connecting them at all.

2. **D2, immediately actionable, no new infra:** eq-shell's `check-tenant-drift.mjs`
   anon-grant + policy-lint checks (CHECK 2 / CHECK 5) are self-contained scripts
   against the Management API. eq-solves-service's CI can call the *same script*
   (vendored or as a shared npm package) scoped to its own PR diff — fails the
   eq-service PR locally, before merge, instead of eq-shell's gate discovering it
   after the fact with no context. This is the fix that would have caught `0167`
   as a heads-up ("this migration will make `check-tenant-drift.mjs` see an anon
   grant on a view — that's fine here, security_invoker handles it, but confirm")
   rather than a mystery three-repo chase.

3. **Cheap fallback if 1 is too much right now:** a scheduled check (or a step in
   eq-shell's existing drift-gate run) that diffs eq-service's `supabase/migrations/`
   directory names (read via the GitHub API, no auth to eq-service's DB needed)
   against what's live on ehow, and posts a warning if a migration has been merged
   >N hours without landing. Doesn't gate anything, just removes the surprise.

**Not recommended:** funneling eq-service's migrations through eq-shell's own
`tenant-migrations/` folder (option b). That inverts the ownership model
eq-intake's CLAUDE.md just correctly settled (`service.*` is eq-service's own
surface) and would make every EQ Service schema change a cross-repo PR.

## What this does NOT change

- The `service.*` vs `app_data.*` ownership boundary (eq-intake CLAUDE.md Rule 2) —
  that's correct as written.
- eq-shell's drift gate scope — it should keep scanning all of ehow regardless of
  which repo owns which table; that's the safety net, not the bug.
- Nothing here implies `0167` should be reverted or redone. It's live, correct, and
  already codified into eq-shell's own lineage (`0156_adopt_contact_canonical_views.sql`,
  invoker+grants only, no duplicated DDL).

## Status

Proposal only. No workflow authored, no live database touched. Chip filed for the
follow-up build once Royce picks a direction: `task_02f3f8d0` (background task,
"Define governed migration-apply path for eq-solves-service").

---
title: eq-canonical reference classification
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Classification of every eq-canonical string ref across the EQ repos
read_priority: reference
status: live
---

# eq-canonical reference classification — 2026-05-31

Companion to `roles-canonical-audit-2026-05-31.md`. Classifies every `eq-canonical` string ref
(the "needs update" repos from §A of that audit) by whether it's a real runtime problem.
**Read this before any eq-canonical integration work — it replaces the scary raw counts with the
actual (small) action list.**

Reminder: `eq-canonical` (jvknxcmbtrfnxfrwfimn) = browser control plane; `eq-canonical-internal`
(zaapmfdkgedqupfjtchl) = server-only data plane. The question per ref is "is it correct in
context," NOT "is it the old name."

## Headline

**Across eq-shell, eq-cards, eq-intake, eq-solves-field: zero confirmed runtime references that
point the wrong plane.** The ~145 raw string hits classify almost entirely as correct-in-context
runtime usage or narrative docs. Real action list:

| Item | Repo | Action | Owner |
|---|---|---|---|
| `netlify/functions/cards-approve-staff.ts:212` — comment says "record approval in eq-canonical" but code writes `cards_field_approvals`; confirm which DB it actually targets | eq-shell | **Eyeball** — the only genuine ambiguity found in the whole sweep | whoever holds eq-shell |
| ~8 tenant-migration comments (`supabase/tenant-migrations/0001–0010`) say "shared eq-canonical" as the schema's origin — substance correct, wording confusing in a tenant-plane file | eq-shell | Optional comment-clarity polish | low priority |
| ~140 narrative refs (READMEs, ARCHITECTURE, RUNBOOK, CHANGELOG, handoffs) | all | Defer; mostly accurate. **eq-context narrative refs are owned by an active session — don't touch** | deferred |

## Per-repo

**eq-shell** — 128 refs. Runtime: 52 correct (control-plane RPCs, auth hooks, cross-tenant audit,
storage buckets, sync scripts that read control plane → write tenant), **0 real bugs**, 1
ambiguous (cards-approve-staff.ts:212, above). The 8 the finder first tagged "fix" are
tenant-migration *comments* referencing the schema's origin on shared eq-canonical — substance
correct, wording confusing. 67 narrative refs deferred.

**eq-cards** — 7 runtime refs, all correct (Flutter reads the browser control plane via
`eq_cards_*` RPCs by design; CSP `connect-src` correctly allows `jvknxcmbtrfnxfrwfimn`). 38
narrative. Zero fixes.

**eq-intake** — 5 refs. 3 correctly target `eq-canonical-internal` (worker-pool edge fn + env), 2
are SQL comments. Zero fixes.

**eq-solves-field** — 7 refs, all correct. The brand-new `2026-05-31_canonical_tenant_registry.sql`
correctly targets eq-canonical (config registry, EQ-corp-owned) and explicitly notes it is NOT a
data-plane / SKS-prod target. Boot config read from control plane is correct. Zero fixes.

## So what

The "eq-canonical cleanup" is **not a migration project.** It is: verify one comment/code mismatch
in eq-shell, optionally tidy some migration comments, leave the docs. The two-project split is
already correctly implemented across the suite — the risk was only in *misreading* it (e.g. a
blanket find-replace), which this classification removes.

> Caveat: classifications are a point-in-time read by fan-out agents; the single AMBIGUOUS item is
> left for human eyes precisely because the agent couldn't resolve it from context.

---
title: Cross-App Linkage — Remediation Plan
date: 2026-06-07
status: archived
companion_to: cross-app-linkage-audit-2026-06-07.md
owner: Royce Milmlow
rule: every executable step below is GATED. Nothing here has been run. Tenant-plane DDL goes through the
  One Pipe (eq-shell tenant-migrate.yml); nspb via sks-nsw-labour repo; ktmj via eq-solves-field repo.
  SKS-live (nspb) is untouchable without an explicit "SKS live" instruction. Auth changes need chat review.
last_updated: 2026-06-22
scope: Remediation plan for cross-app linkage gaps found 2026-06-07 — superseded by live wiring
read_priority: reference
---

# Cross-App Linkage — Remediation Plan (2026-06-07)

Turns the [audit](cross-app-linkage-audit-2026-06-07.md) into an ordered, mechanism-aware playbook. The canonical
model is **already built** (`ehow.app_data` is fully FK-wired) — the work is **populating bridge columns, choosing
single owners, and finishing the in-flight Field anon-remediation** — not redesigning schema.

**Nothing in this file has been executed.** Each item states: *what · mechanism (which repo/pipe) · gate · verify*.

## Reconciliation with existing tracks (not new work)

- The S1/S2 anon-write exposure is the **known trailing edge** of the Field anon-remediation
  (`eq/pending.md` 2026-06-03 PM: 22 EQ/`zaap` surfaces secured; *"SKS inherits the Goal-1 pattern when its
  anon-remediation runs"*; *`ktmj` = dead cold-backup, slated for downgrade+pause*). This plan supplies the **exact
  remaining worklist**, not a new discovery.
- The `shift.started` durable emitter (`sessions/2026-06-07.md` parts A/B) is the first real cross-app event
  emitter — consistent with the audit's "event bus is HTTP→canonical-api" finding.
- GATE A decision already exists (`eq/identity/gate-a-decision-2026-06-03.md`, Option A — provision-at-claim).

---

## Priority 1 — Worker → identity → Field-person (the worker trace)

**Why first:** highest leverage. Unlocks "trace a worker from Cards → roster → timesheet." Verified empty:
`workers.user_id` 4/38, `app_data.staff.cards_worker_id` 1/50, `ktmj.people.worker_id` 0/605.

> **⚠ SUPERSEDED — this priority is already owned.** An **APPROVED-FOR-BUILD** spec exists:
> [`worker-identity-linker-spec-2026-06-07.md`](worker-identity-linker-spec-2026-06-07.md) (concurrent session). It
> covers GATE A + the worker→staff link end-to-end (M1 `user_invites.worker_id`, M2 FK `workers.user_id`→shell user,
> M3 `workers.staff_id` soft-ref to `app_data.staff`, unified invite flow, `accept-invite.ts` linking, Phase-5
> backfill). **Defer to that spec — do not build P1 in parallel.** Two reconciliation notes for whoever runs it:
> (1) it matches workers↔staff/users by **email** (cleaner than my phone suggestion; "no email" is a handled status);
> (2) it adds `workers.staff_id` (jvkn→ehowg) while `app_data.staff.cards_worker_id` (ehowg→jvkn) **already exists** —
> decide whether both soft-ref columns are maintained or one is canonical, so the link isn't half-populated in each
> direction. The items below (1a/1b) are subsumed by that spec; kept only as the audit's cross-reference.

**1a. Resolve GATE A (auth — CHAT-REVIEW GATED).**
- What: provision workers into `shell_control.users` at invite-claim so OTP sign-in carries a `tenant_id`.
- Mechanism: reconcile the GATE A fix **onto** eq-cards branch `claude/otp-tenant-fix` (per verified-state — do not
  fork), not a new branch. `eq_cards_claim_invite` already writes `shell_control.users` + `user_tenant_memberships`.
- Gate: **auth change → review in chat before deploy** (hard rule §7). Decision is Option A (already logged).
- Verify: `select count(*) from shell_control.users;` rises past 5; `select count(*) from workers where user_id is not null;` rises past 4 as invites are claimed.

**1b. Backfill `app_data.staff.cards_worker_id` (cross-project reconcile — GATED).**
- What: link existing canonical tenant `staff` (50) ↔ eq-canonical `workers` (38) by a stable key.
- Match key (in priority order): phone (E.164) → exact normalized name → manual. **No reliable shared key exists
  today** — `workers.staff_id` is 0/38 and `staff.cards_worker_id` 1/50, so this is a one-time reconciliation, not a
  trigger. Confirm the match key with Royce before running (phone collisions are the known landmine — audit §6).
- Mechanism: one-time script reading both projects (service-role), writing only `app_data.staff.cards_worker_id`
  on `ehow`/`zaap` via the canonical-api or a gated migration. **Not** a blanket UPDATE.
- Gate: Royce approves the match key + a dry-run diff (which staff↔worker pairs) before any write.
- Verify: `select count(*) from app_data.staff where cards_worker_id is not null;` on `ehow`.

**1c. Repoint OR retire the Cards→Field approval bridge (see Priority 4 — do 4 first).**

---

## Priority 2 — Single canonical customer + backfill `canonical_id`

**Why:** customer identity is fragmented across `ehow.public.sks_customers` (520), `ehow.public.sks_quotes_customers`
(520), `ehow.app_data.customers` (389), + nspb copies. `sks_quotes_customers.canonical_id` is **0/520** in the live
store, so a quote's customer can't be joined to the CRM/Service customer.

**2a. Decide the system-of-record (DECISION — Royce).**
- Recommended: **`ehow.app_data.customers`** is the canonical SoR (it's the convergence target, carries `tenant_id`
  + `external_id`, and is what Service/Shell already write to). `sks_customers`/`sks_quotes_customers` become the
  Quotes-app local cache that carries `canonical_id` back to it.
- Alternative: keep `sks_customers` as SoR (less churn for the Flask app, but leaves Service/CMMS on a different
  customer table). The audit recommends `app_data.customers`.

**2b. Backfill `sks_quotes_customers.canonical_id` (single-project UPDATE — GATED, low risk).**
- What: within `ehow`, match `sks_quotes_customers` → the chosen SoR by `external_id` / `workbench_customer_id` /
  normalized company name, and stamp `canonical_id`.
- Mechanism: the Quotes app **already has** `canonical_customers.upsert_customer()` + a `backfill_customers()` helper
  (audit §4). Prefer running that backfill over hand-SQL so the app's dedupe logic owns it.
- Gate: dry-run the match counts first (how many resolve cleanly vs need review).
- Verify: `select count(*) from sks_quotes_customers where canonical_id is not null;` → target 520/520.

---

## Priority 3 — Site → customer backfill

**Why:** only **28/591** `app_data.sites` carry a `customer_id`, so the 4808 assets hanging off those sites can't roll
up to a customer.

- What: populate `app_data.sites.customer_id` from `sites.external_customer_id` → `customers.external_id`.
- Mechanism: single-project UPDATE on `ehow` (and `zaap` for EQ), or via the canonical-api site upsert path.
- Gate: depends on **Priority 2** (need deduped customer ids first); dry-run unmatched count.
- Verify: `select count(*) from app_data.sites where customer_id is not null;` on `ehow`.

---

## Priority 4 — Repoint the Cards → Field approval bridge (smallest, do early)

**Why:** Shell `cards-approve-staff.ts` writes approved staff into **`ktmj` (legacy, dead)** `people`/`qualifications`
(`FIELD_SUPABASE_URL` = ktmj), but live Field reads `zaap.app_data` (EQ) / `nspb` (SKS). Only 2 rows in
`shell_control.cards_field_approvals`, 0 populated in ktmj — the bridge is effectively misdirected.

- What: route approvals into the **canonical tenant plane** (`app_data.staff` + `app_data.licences`, which already
  carry `cards_worker_id` / `cards_credential_id`) instead of the legacy ktmj project. This *is* the worker→staff link
  from Priority 1 — doing it here makes 1b mostly automatic for new approvals.
- Mechanism: eq-shell code/env change (`FIELD_SUPABASE_URL` → tenant routing, or write via `canonical-api`). eq-shell
  repo, its own branch, normal PR + the gated deploy.
- Gate: **confirm the live Field plane per tenant** (zaap for EQ, nspb for SKS) before repointing; no deploy without
  Royce. Sequence: **repoint bridge → THEN decommission ktmj** (Priority 7b) — not the reverse.
- Verify: a test approval lands in `ehow.app_data.staff` with `cards_worker_id` set; ktmj receives nothing.

---

## Priority 5 — Quote → Job entity (the missing link; needs a decision)

**Why:** the headline "quote → job → timesheet" trace is **impossible** — `app_data.jobs` = 0 and `app_data.quote` = 0,
and live quotes sit in a different table (`ehow.public.sks_quotes`, the Flask app). There is no work-order concept with
data anywhere.

**5a. DECISION (architectural — Royce):** who owns "job / work-order"? Options:
- (i) Field owns it (jobs = confirmed tenders/schedule) — fits the resources model.
- (ii) A new thin canonical `jobs` writer triggered by `quote.accepted`.
- (iii) Defer — accept no quote→job trace until a real workflow needs it.

**5b. IF (ii):** on `quote.accepted` (event already emitted by Quotes → canonical-api), create an `app_data.jobs` row
with `customer_id` + `site_id` resolved (Priorities 2–3) and `quote_id` set (the soft column already models this).
- Mechanism: a handler in eq-shell `canonical-api` (it already writes `app_data.jobs`). Gated deploy.
- Verify: `select count(*) from app_data.jobs where quote_id is not null;` > 0.
- Effort: **LARGE** — don't start before the SoR decisions (P2) and the owner decision (5a).

---

## Priority 6 — Field-live (nspb) into the canonical plane (SKS cutover)

**Why:** SKS operational reality (`nspb.public.people` 60 / `schedule` 761 / `timesheets` 183) lives outside the
convergence target; only `nspb.people.canonical_id` (49/60) bridges it. Already a 5-phase gated project.

- Mechanism: `SKS-CUTOVER-CRITICAL-PATH.md` — nspb DDL via the **sks-nsw-labour repo** (separate entity).
- Gate: **SKS-live — untouchable without an explicit "SKS live" instruction.** Sequenced by the cutover plan, not here.
- Effort: **LARGE**.

---

## Priority 7 — Security remediation (S1/S2 from the audit)

These are the **remaining un-secured surfaces** of the Field anon-remediation. RLS is ON everywhere; the issue is
always-true write policies + the legacy anon read path. **Do NOT blanket-drop** — these policies are load-bearing for
the not-yet-migrated tables; dropping a write policy before its table is on the JWT path breaks the running app.
Per-table, coordinated with the app's Phase-1 migration.

**7a. nspb (SKS LIVE) — GATED on "SKS live", via sks-nsw-labour repo.** Finish the Goal-1 pattern (JWT twin →
revoke anon) per table, then drop these always-true write policies (exact, verified 2026-06-07):

| Table | Policies to retire (after JWT migration) |
|---|---|
| `audit_log` | `anon_insert` (INSERT, check=true) |
| `nominations` | `anon_insert_nominations`, `anon_update_nominations`, `anon_delete_nominations` |
| `prestarts` | `prestarts_insert_tenant`, `prestarts_update_tenant`, `prestarts_delete_tenant` |
| `site_diaries` | `site_diaries_insert_tenant`, `site_diaries_update_tenant`, `site_diaries_delete_tenant` |
| `toolbox_talks` | `toolbox_talks_insert_tenant`, `toolbox_talks_update_tenant`, `toolbox_talks_delete_tenant` |
| `tender_enrichment` | `anon_insert_tender_enrichment`, `anon_update_tender_enrichment`, `anon_delete_tender_enrichment` |
| `roster_presence` | `presence_update_anon`, `presence_delete_anon` |

(SELECT-only anon policies on `tenders`/`teams`/`pipeline_events`/etc. are read-exposure — lower priority; close with
the same migration. `verify_staff_pin` anon-EXECUTE is by-design pre-login — keep, ensure `bump_rate_limit` rate-limits it.)
The tenant-named policies (`*_tenant`) give **no** isolation — their USING/CHECK are literally `true`. Replace with a
real predicate, e.g. `tenant_id = (auth.jwt() ->> 'tenant_id')::uuid` (mirror a secured twin).

**7b. ktmj (legacy EQ Field DB) — via eq-solves-field repo, AFTER Priority 4.** This DB is the dead cold-backup
(`pending.md` 2026-06-04). Once the Cards bridge is repointed (P4) and no consumer remains, **pause/decommission it**
(already a pending Royce-action) — that closes the exposure wholesale. If it must stay live, drop the anon write
policies on the PII tables: `people_anon_update/delete`, `managers_anon_update/delete`, `timesheets_anon_update/delete`,
`leave_requests_anon_update/delete`, `schedule_anon_update/delete`, `sites_anon_update/delete`,
`anon_insert_field_customers`, `anon_insert_field_waitlist`, plus the `{public}` ALL policies on
`apprentice_journal`/`feedback_requests` and the `*_anon_*` set on `apprentice_profiles`/`buddy_checkins`/
`engagement_log`/`feedback_entries`/`project_targets`/`projects`/`regions`/`rotations`/`skills_ratings`/
`staff_availability`/`quarterly_reviews`.

**7c. ehow / jvkn — lower priority, by-design or low-blast.** ehow's 16 `authenticated`-executable `SECURITY DEFINER`
funcs (`eq_upsert_*`, `eq_archive_*`, `eq_delete_*`) — review whether `authenticated` should call delete/archive
directly or only via the app. jvkn's 4 anon-executable `eq_cards_*` RPCs — **audit `eq_cards_get_worker_hr_record`
and `eq_cards_delete_account` internal authz** (they touch HR / account deletion). Move `vector`/`pg_net` out of
`public` on ehow/nspb (cosmetic). RLS-enabled-no-policy tables are service-role-only = safe (the canonical posture,
per `sessions/2026-06-07.md` part B).

**7d. Service DB (`urjhmkhbgaxrofurpbgc`) — run a `get_advisors` pass.** Not audited (outside the 4 IDs); holds
customers/sites/assets. One read-only advisor run closes the blind spot.

---

## Suggested execution order

`P4 (repoint bridge, small)` → `P1a (GATE A, auth-gated)` → `P1b + P2 + P3 (backfills, low-risk, unlock the trace)`
→ `P7b (decommission ktmj — closes S1)` → `P7a (SKS anon-remediation — closes S2, gated)` → `P5 (job entity — needs
decision)` → `P6 (SKS cutover)`.

Two MEDIUM-effort moves (P1 worker identity, P2 customer identity) unlock most of the suite-wide trace. P5/P6 are the
LARGE, decision-first items.

## What is NOT done (and why)

No live DB writes, no DDL, no app-repo edits, no deploys, no commits/pushes — all blocked by the hard rules until you
explicitly green-light each (and "SKS live" for anything touching nspb). This file + the audit are the reviewable
artifacts; say the word and I'll execute the safe subset (e.g. dry-run backfill diffs, the Service advisor pass, or
draft the eq-shell bridge PR).

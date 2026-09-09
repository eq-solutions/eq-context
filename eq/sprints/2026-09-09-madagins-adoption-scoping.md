---
title: Madagins adoption scoping — from provisioned to actively used
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Scoping pass on "getting Madagins actively using EQ" — Royce's stated forward focus at the close of tonight's tenant-provisioning thread (sessions/2026-09-09.md, "tenant-provisioning followups closed out" entry: "SKS work remains the primary focus; also wants to build out Madagins' own profile and get them actively using EQ day-to-day"). Deliberately a new doc, not appended to eq/sprints/2026-09-09-tenant-onboarding-sprint.md — see "Why a new doc" below. Everything under "Live state" was re-verified directly against jvkn (eq-canonical) and Madagins' own dedicated Supabase project (ornndtbdkxfsewspbrwk) this session, not restated from prior docs' claims.
read_priority: high
status: live
---

# Madagins adoption scoping

Scoping only, per instruction — nothing built, no schema/auth changes, no migration dispatch. SKS remains the primary focus; this is secondary and parallel, not urgent. `TODAY.md` GOALS are unset, so nothing here is framed against a deadline that doesn't exist.

## Decided (2026-09-09, via this scoping pass)

- **The adoption gap is Royce's to close, not engineering's.** He'll reach out to Michelle/Aditi directly rather than have EQ pre-seed starter data or lean on Cards' self-serve intake to prompt it. Nothing spawned for this.
- **Madagins does not get the `service` module for now.** Field+Cards+Intake is the intended scope, matching what's actually live today. Migration `0311` (the CMMS/Service-table baseline — see below) stays merged-not-dispatched; revisit only if this changes.

## Why a new doc, not appended to `tenant-onboarding-sprint.md`

That doc (and its siblings `tenant-provisioning-review.md` / `-followups.md`) track the **infrastructure** side of tonight's incident — decided/built engineering items (isolation model, tier-sync trigger, RLS fixes, migration numbering). This doc is about a different question: **is anyone at Madagins actually using the product**, which turns out to be almost entirely non-technical. Bolting it onto the engineering sprint would conflate "is the schema correct" with "has a human logged in and done something" — different audiences, different owners. Cross-referenced below, not duplicated.

## 1. What "Madagins actively using EQ" concretely means — live-verified tonight

### Real admin user, actually logged in? No — confirmed live, not assumed.

Queried `auth.users` on jvkn directly for the two Madagins manager accounts:

| Email | Created | Last sign-in | Gap |
|---|---|---|---|
| aditi@madagins.com.au | 2026-09-09 00:58:28 | 2026-09-09 00:59:15 | 47 sec |
| accounts@madagins.com.au (Michelle) | 2026-09-09 01:08:41 | 2026-09-09 01:09:14 | 33 sec |

`last_sign_in_at` is the *most recent* sign-in, not a count — a value this close to `created_at` means the only sign-in either account has ever had is the automatic one bundled into account creation/invite-acceptance. **Nobody at Madagins has come back and used the product since being set up.** This confirms, with a live timestamp rather than a doc claim, what several sessions today already suspected (`eq/pending/eq-field.md`: "no session has actually signed in as a real madagins user through Core yet").

### Entitled modules — confirmed live, corrects the assumption in tonight's brief

Queried `org_module_entitlements` on jvkn directly:

| Module | Enabled |
|---|---|
| cards | ✅ true |
| field | ✅ true |
| intake | ✅ true |
| comms | ❌ false |
| ops | ❌ false |
| quotes | ❌ false |
| service | ❌ false |

Tonight's task brief assumed "should be field + intake only" — live data shows **three** modules on: cards, field, intake. That's the right set for a labour-hire/field-ops customer (Cards is the worker-onboarding/intake surface, Field is day-to-day ops) and matches Royce's own confirmed call that "NSW Comms" stays SKS-only. Nothing to fix here — flagging only because the brief's assumption was slightly off and the task asked to confirm live rather than take it on faith.

### Who actually has tenant access

Queried `shell_control.user_tenant_memberships` on jvkn, joined to `auth.users`:

| Email | Role | Active |
|---|---|---|
| royce.milmlow@sks.com.au | manager | true |
| accounts@madagins.com.au (Michelle Moore) | manager | true |
| aditi@madagins.com.au (Aditi Rajbhandari) | manager | true |
| saretonelson@gmail.com (Nelson Sareto) | labour_hire | true |
| conorhorgan25@gmail.com (Conor Horgan) | labour_hire | true |

All 5 active, all correctly roled. Access itself is not the blocker.

### The comms/customer-success angle

Everything above is a fact I can check; **none of it is something I can fix.** The gap is "has a human at Madagins used the product," and closing that needs Royce (or someone he delegates) to actually talk to Michelle or Aditi. No code change moves this number. **Royce's call, confirmed tonight: he'll reach out directly** — see Decided above.

## 2. The real gap between "provisioned" and "onboarded"

### Infrastructure — solid, confirmed live tonight

- `shell_control.tenant_routing`: present, `status: active`, correct project ref (`ornndtbdkxfsewspbrwk`). The present/missing "flapping" documented earlier today across ~6-8 concurrent sessions is **not currently manifesting** — re-verify if picking this up much later, but as of tonight it's stable.
- Tier: `shell_control.tenants.tier = advanced`, `organisations.tier = Advanced` — the two now agree (case-normalised via `initcap()`), confirming the `eq-cards#352` sync trigger is live and actually working, not just merged.
- RLS: scanned every table across `public`/`app_data`/`service`/`shell_control` on Madagins' own project (~130 tables) — **100% RLS-enabled**, no anon-writable gaps. `get_advisors` (security) returned only generic, fleet-wide-pattern findings (1 `ERROR`-level "Security Definer View" of a kind common across this whole codebase's adapter views, a few `WARN`-level function/extension hygiene items) — nothing Madagins-specific or urgent enough to act on tonight.
- Migration ledger (`app_data._eq_migrations`): 327 applied rows, consistent with the day's governed catch-up dispatches.
- Field staff records: `app_data.staff` = 5 rows, matching all 5 people above — confirms `tenant-provisioning-review.md`'s "Resolved — Field staff records created" claim against the live table, not just the doc's word for it.
- eq-field's own 77-migration schema replay (Teams, leave, schedule, roster, licences): confirmed fully applied and correctly parameterised with Madagins' own org_id/tenant_id (not SKS's) via a same-day commit picked up mid-session (`47a601f6`) — `app_data` object count 132, `field_leave_requests`' shape live-verified. Not a lingering gap.

### The actual gap — the workspace itself is empty

Live row counts on Madagins' own project, `app_data` schema:

| Table | Rows |
|---|---|
| customers | 0 |
| sites | 0 |
| jobs | 0 |
| schedule_entries | 0 |
| teams / team_members | 0 / 0 |
| timesheets | 0 |
| prestart_checks | 0 |
| toolbox_talks | 0 |
| staff | 5 |
| licences | 8 |

Staff exist; almost nothing else does. **Even if Michelle logged in right now, EQ Field would show her an empty workspace** — no sites, no customers, no jobs, no crew. This is the concrete shape of "provisioned but not onboarded": the infrastructure is sound, but there is no actual business data for anyone to act on yet. Royce is handling this directly (see Decided) rather than having EQ pre-seed it or lean on Cards' self-serve flow — worth him knowing exactly how empty it is going in.

### CMMS/Service tables — confirmed still missing; the fix is eq-shell's migration `0311`, not eq-field PR #959

Tonight's brief attributed the ~20-25 missing CMMS/Service tables (`maintenance_checks`, `defects`, `check_assets`, `rcd_tests`/`nsx_tests`/`acb_tests`, `instruments`, `pm_schedule`, `job_plans`) to eq-field PR #959. **Correcting that against the primary docs and live schema**: PR #959 (`generate-tenant-provision-sql.mjs`) is eq-field's *own* 77-migration replay tool — Field's Teams/leave/schedule/roster data, the separate gap confirmed resolved directly above. It was never about the CMMS tables.

The actual fix for the CMMS/Service tables is **eq-shell's migration `0311`** (`0311_app_data_legacy_baseline_and_tenant_members.sql`, PR #1842, merged) — reconstructed from ehow's live schema by an eq-shell session, reviewed, confirmed merged-but-not-dispatched to any tenant (`tenant-migrate.yml`'s apply step shows `skipped` on the merge commit). Live scan of Madagins' project confirms all ~25 target objects are genuinely still absent.

**Confirmed tonight: not needed.** The `service` module entitlement is `false` — Madagins isn't scoped to use EQ Service, so this gap doesn't block anything. Per Decided above, `0311` stays merged-not-dispatched; revisit only if Royce decides to entitle Madagins to Service later.

## 3. Ranked next steps

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | Get a real first login + first site/customer/job in front of Michelle or Aditi | **Royce actioning directly** | Confirmed tonight — see Decided. Highest-leverage item; zero engineering content. |
| 2 | Decide whether Madagins ever gets the `service` module | **Confirmed: not now** | See Decided. Revisit only if this changes. |
| 3 | Dispatch migration `0311` to madagins | **On hold** — tied to #2 | See `tenant-provisioning-followups.md` §1. Not needed while Service stays out of scope. |
| 4 | Add madagins to `check-tenant-drift.mjs`'s `CANONICAL_PROJECTS` | Buildable now (code) + needs Royce (CI secret) | Already tracked, `tenant-provisioning-followups.md` §2. Small, not urgent. |
| 5 | Formalize the live-applied 37-object `public`-schema baseline as a committed migration | Buildable now | Housekeeping — protects the *next* from-scratch tenant, not Madagins itself. Already tracked. |

Items 3-5 are pre-existing, already-tracked items surfaced by earlier sessions tonight — repeated here only for ranking, not re-investigated. Nothing new was found that needs a fresh spawned task: the one live-verification detail that isn't already written down anywhere (the empty-workspace row counts) fed directly into Royce's own call above, not a bug for engineering.

## Cross-references

- `eq/sprints/2026-09-09-tenant-onboarding-sprint.md` — Cards-side gaps, tier-sync mechanism (confirmed live above), isolation-model decision.
- `eq/sprints/2026-09-09-tenant-provisioning-review.md` — the four live-gap incident review, resolution log, the five-disconnected-paths structural finding.
- `eq/sprints/2026-09-09-tenant-provisioning-followups.md` — current needs-you/deferred list for the migration-numbering and drift-check items.
- `eq/pending/eq-field.md` "madagins tenant" entry, and its `47a601f6` follow-up — origin of the "no real sign-in yet" finding (still true) and confirmation that eq-field's own 77-migration replay (PR #959) is fully resolved and unrelated to the CMMS-table gap.
- `sessions/2026-09-09.md` — full day's narrative; "tenant-provisioning followups closed out" entry is the direct source of tonight's ask.

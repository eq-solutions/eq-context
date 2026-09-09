---
title: Tenant provisioning review — Madagins incident, process gaps, recommendations
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Full review of today's Madagins provisioning, requested by Royce directly ("it feels VERY clunky... learn from today's mistakes"). Synthesizes the chat review with eq/sprints/2026-09-09-tenant-onboarding-sprint.md and eq/sprints/2026-09-09-provisioning-completeness-followup.md (both live-verified, not restated — those two stay the build-tracking source for their own numbered items) plus a fresh live Supabase/GitHub check at write time. Not a replacement for either sprint doc — a cross-reference plus the parts they don't cover (env vars, email config, DR/backup scope, the code-level provisioning-path map).
read_priority: high
status: live
---

# Tenant provisioning review — Madagins

## Summary

Madagins (`madagins.com.au`) is EQ's first tenant provisioned from scratch against the *current* migration history — sks and eq both had their data planes hand-built before this pipeline existed, so nothing ever exercised the "brand-new tenant" path for real until today. It surfaced that the path was never actually complete: no single mechanism creates a working tenant end to end, a large chunk of schema predates the tracked migration system entirely, and several sessions worked the same tenant concurrently today with no coordination, at one point undoing an already-confirmed-working fix. None of this is a regression — it's the first real load-test of automation that was always partial.

## Live state, verified directly (not from any doc) — four confirmed gaps

| # | Gap | Verified | Source |
|---|---|---|---|
| 1 | `shell_control.tenant_routing` has no row for Madagins — `organisations` LEFT JOIN returns null for `supabase_project_ref`/`status`/`provisioned_at` | Live query, jvkn | This session |
| 2 | `app_data._eq_migrations` on Madagins' own project (`ornndtbdkxfsewspbrwk`) has RLS disabled — Supabase advisor flags CRITICAL, anon-writable | Live `list_tables` advisory, Madagins project | This session |
| 3 | `ALLOWED_FIELD_TENANT_SLUGS` in `token-exchange.ts:42` is `['eq','demo-trades','melbourne','sks']` — madagins isn't in it (it *is* in the separate `KNOWN_TENANT_SLUGS`) | `git show origin/main:...`, eq-shell | This session |
| 4 | Tier split-brain: `shell_control.tenants.tier` = `advanced` (what the real admin UI set), `organisations.tier` = `Standard` (its schema default — what EQ Field actually reads for gating) | Live query, jvkn | This session |

None of these were built to fix here — the session log documents at least two prior sessions colliding on this exact tenant today, one undoing the other's confirmed-working fix, so a third parallel fix attempt right now was judged more likely to add confusion than resolve it. **A worktree/branch named `claude/verify-madagins-rls-fix` was found active in `git worktree list` while landing this doc** — possibly another session already on gap #2 specifically; its diff couldn't be inspected from this session's own isolated worktree (git refused the cross-branch read). Worth Royce checking directly rather than assuming either way, especially given #2 and #1 may already be in motion elsewhere.

Item #1 was already tracked in `digest.md`'s "Waiting on you" (the ledger-correction item) before this review; #2–#4 are new findings from this pass. Note the sprint-doc history on #1 specifically: `eq/sprints/2026-09-09-tenant-onboarding-sprint.md`'s item #5 retraction says the routing row *was* populated correctly earlier today, then verified gone by this session — consistent with the session log's own account of a later reset wiping it.

## The core structural finding: five disconnected paths, not one

| Path | What it does | Used for Madagins? |
|---|---|---|
| Admin → Tenants UI → `admin-tenants.ts` | Control-plane rows (tenants/organisations/entitlements/tenant_config), default security groups, auto-joins creator | ✅ |
| `provision-tenant-background.ts` | Creates the Supabase project via Management API (automated, ~14 min poll to `ACTIVE_HEALTHY`), applies a **minimal** bootstrap only (schemas, ledger table, PostgREST exposure, now `pg_cron`) | ✅ |
| `tenant-migrate.yml` / `migrate-tenants.mjs` (manual dispatch) | Applies the full ~300-file canonical "One Spine" migration set | ✅, hand-triggered, failed 189/300 in on the pg_cron gap |
| eq-field's own ~76-77 migrations, no CI apply path | Hand-classified every time — which need tenant-ID substitution, which to exclude | ✅, built by hand today |
| `shell_control.provision_tenant()` via EQ Cards' `/provision?token=...` | The one **atomic** path — creates Shell identity + Cards-side `organisations`/`org_memberships` admin row together, built specifically so a tenant can't "look provisioned but be unusable in Cards" | ❌ — which is exactly why Cards has no admin for Madagins (see `tenant-onboarding-sprint.md` decision #2/#6) |

`admin-tenants.ts` and `provision-tenant-background.ts` fire as two independent, unorchestrated calls from the same UI action — nothing chains them to the migration dispatch or to Cards' atomic path. A sixth, dead path is still actively misleading: `README.md:257-259` links `docs/runbooks/onboard-trial-tenant.md` + `onboard-trial-tenant.mjs`/`provision-tenant.mjs` as "one command" — last touched 2026-06-04/08, calls none of the functions above.

## Schema defaults — the real numbers

Today's fleet migration dispatch died at **migration 189 of ~300** because `pg_cron` wasn't enabled — every existing tenant (sks, eq) had it hand-enabled years before this pipeline existed, so nothing needed to enable it programmatically until today's from-scratch tenant hit it. Same shape as `pg_net`, patched ad hoc live with one `CREATE EXTENSION` statement.

The deeper gap, from `check-provisioning-completeness.mjs`'s first live run (`eq/sprints/2026-09-09-provisioning-completeness-followup.md` §3): **2 more untracked extensions** (`vector`, `pg_net`), **2 live-only schemas** (`shell_control`, `wipe_backup` — the former's presence on the *tenant* plane specifically is flagged as worth confirming isn't itself a mistake), **~71 live-only tables**, **~65 live-only functions** — none created by any tracked migration. `KNOWN_LIVE_ONLY`, the script's own triage allowlist, ships empty on purpose; nothing's sorted yet into "fine to ignore" vs. "needs a real migration."

**The actual fix already exists as draft SQL** — `0308_legacy_public_schema_baseline.sql` (37 objects) + `0309_app_data_legacy_baseline_and_tenant_members.sql` (63 objects), ~4,700 lines, sitting uncommitted in worktree `eq-shell-wt-pgcron`. Deliberately held back, not because nobody got to it — both files' own headers self-document real correctness bugs:
- Most RLS policies hardcode ehow's own tenant/org UUIDs as literals — applied as-is to any tenant that isn't SKS, these ~37 objects come back **permanently zero-access, service-role only**, for real users.
- At least 3 self-documented migration-ordering bugs: `0257` and `0260` still crash a from-scratch tenant *before* either new file would even run — landing this pair does not, by itself, fix the crash that motivated it.
- Both `0308` and `0309` collided with other same-day merges ([eq-shell #1829](https://github.com/eq-solutions/eq-shell/pull/1829) `sites.deleted_at`, [#1833](https://github.com/eq-solutions/eq-shell/pull/1833) `wipe_backup` RLS) — needs renumbering to `0310`/`0311` at land time, and re-checking again then.

Separately: **Madagins is 50 migrations behind `main`** (currently at `0257`). A blank dispatch to catch it up would silently apply 49 other, unreviewed migrations — security/RLS/role-gate changes among them. Needs a deliberate decision, not a default dispatch.

**Fixed today, actually merged** (verified via `gh pr view`, not the doc): pg_cron on new-project bootstrap ([eq-shell #1834](https://github.com/eq-solutions/eq-shell/pull/1834), merged 06:47:48 UTC). **Landed, not yet acted on**: the completeness-audit script itself ([eq-shell #1832](https://github.com/eq-solutions/eq-shell/pull/1832), informational-only). **Real, drafted, correctly held**: the 0308/0309 legacy-baseline pair above.

## Redundancy — two different things, don't conflate

**Infrastructure DR** (`system/dr-backups.md`) is solid: ehow/jvkn/zaap all get daily offsite R2 backups, daily automated restore-verify, quarterly automated restore-drills, proven 4-6s RTOs. Its entire scope is those **three shared platform databases** — confirmed both from the doc's own project table and from `provision-tenant-background.ts`'s actual Management API call, which sends no backup/PITR parameter and has no `tenant_routing` column for one. **Every new dedicated-per-tenant Supabase project, Madagins included, is outside this system by construction** until someone deliberately adds it.

**A separate "redundancy review"** (`eq/sprints/2026-09-09-redundancy-review-followups.md`, same day by coincidence) is bus-factor/access redundancy — Netlify's single owner with no second admin, GitHub org-admin membership unverified, registrar-lock/Cloudflare MFA never independently checked. Unrelated to Madagins; almost every item there needs Royce's own hands in a dashboard.

## Env vars

The part that matters most is well-designed: the new project's URL/anon key/service-role key are never Netlify vars — written into `shell_control.tenant_routing`, service-role key AES-256-GCM-encrypted. Scales fine per-tenant.

What doesn't: three hardcoded per-tenant slug lists, each needing a manual PR for every new tenant —

- `KNOWN_TENANT_SLUGS` ([`_shared/tenant-routing.ts:389`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/_shared/tenant-routing.ts#L389)) — updated for madagins today.
- `ALLOWED_FIELD_TENANT_SLUGS` ([`token-exchange.ts:42`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/token-exchange.ts#L42)) — **not** updated (live gap #3 above).
- `SCHEDULER_TENANT_SLUGS` / `QUOTE_JOB_TENANTS` (Netlify env vars) — a forgotten append means that tenant's scheduled jobs silently never run, no error surfaced anywhere.

This exact pattern was already fixed once, for a different call site: `canonical-api.ts` moved off a hardcoded tenant map onto a `shell_control.app_tenant_scope` **table** specifically "so onboarding a tenant is a data change, not a code deploy." Never extended to the two lists above.

## Email sending settings

Fully global, no per-tenant concept anywhere in code: one `EQ_EMAIL_PROVIDER`, one `RESEND_API_KEY`, one `EMAIL_FROM` (default `EQ Solutions <noreply@eq.solutions>`). Every tenant's transactional email — Madagins included — sends from the same identity today. Plumbing fact and a live product question: does a customer named `madagins.com.au` get `@eq.solutions` emails indefinitely, or does per-tenant sending identity become a thing at some point?

## The coordination lesson — three documented instances today, not one

1. **The schema wipe.** Session A's v2 provisioning script ran clean, Royce confirmed it ("thats done"). Session B, working the same tenant without visibility into A's fix, treated it as still broken and reset it — wiping `public` back to zero and dropping the `tenant_routing` row (live gap #1 above). Full account: `sessions/2026-09-09.md`, final entry.
2. **The architectural call made without review.** A session ran `/decide` and wrote "shared ehow by default, dedicated project as opt-in" into `tenant-onboarding-sprint.md` as **Decided** — before Royce had seen it. He rejected it outright, emphatically, once he did (now the global CLAUDE.md non-negotiable on tenant isolation). Already retracted in the doc itself; nothing outstanding here, but it's the clearest single example in today's incident of a session converging on an architecture decision without Royce in the loop first.
3. **A pending.md section that just disappeared.** The original write-up of the pg_cron/legacy-baseline follow-ups lived in `eq/pending/eq-shell.md` (commit `76d7e4d8`). By the time `provisioning-completeness-followup.md` was started, that section was gone from the live file — not archived, not in `eq/pending-archive.md`, just gone. Confirmed independently while landing this doc: commit `49f38487`, on `main` as of this write, is titled "restore genuinely-open items from 3 sections lost to today's F17 clobber cascade" — the same failure (F17, closed same day per `system/failures.md`) that this finding traces to. Worth knowing the fix for the *mechanism* landed today too, not just this one symptom.

## What's already fixed or decided today (credit where due)

| Item | Status |
|---|---|
| pg_cron enabled on new-tenant bootstrap | **Merged** — [eq-shell #1834](https://github.com/eq-solutions/eq-shell/pull/1834) |
| Provisioning-completeness audit script | **Merged**, informational-only — [eq-shell #1832](https://github.com/eq-solutions/eq-shell/pull/1832) |
| `workers-canonical-sync` generalized off SKS/ehow hardcode, cross-tenant-leak test added | **Merged + deployed** — [eq-cards #348](https://github.com/eq-solutions/eq-cards/pull/348) |
| Tenant-isolation model: dedicated-per-tenant, never shared | **Decided** (after the correction above) — now a global non-negotiable |
| Cards-side admin zero-member gap: lazy self-seed | **Decided**, not yet built — `tenant-onboarding-sprint.md` #2/#6 |
| `organisations.tier` / `shell_control.tenants.tier` sync | **Confirmed live bug** (this review), fix decided not yet built — `tenant-onboarding-sprint.md` #3/#7 |
| Multi-org-admin picker truncation (`org_admin_provider.dart`) | Found, not yet built — `tenant-onboarding-sprint.md` #8 |
| Legacy-baseline migrations (0308/0309→0310/0311) | Drafted, correctly held on real unresolved bugs — `provisioning-completeness-followup.md` §1 |
| eq-field tenant-provisioning SQL generator | Open, not merged — [eq-field #959](https://github.com/eq-solutions/eq-field/pull/959) |
| Auto-generating the missing-object prerequisite block | Not built — the generator only warns today |
| Stale `onboard-trial-tenant` runbook | Not touched — still actively misleading in `README.md` |
| `safe_commit.py` concurrent-clobber gap (F17) that caused finding #3 above | **Closed same day** — `system/failures.md` F17 |

## Recommendations — for Royce's call, none built here

1. Settle Madagins' live state (the four gaps above) in one sequential pass before any further session touches that tenant — check `claude/verify-madagins-rls-fix` first, it may already be in progress.
2. Chain `admin-tenants.ts` → `provision-tenant-background.ts` → migration dispatch into one flow instead of independently-fired calls.
3. Triage `check-provisioning-completeness.mjs`'s ~136-item live-only inventory into `KNOWN_LIVE_ONLY` — that's what turns it from a warning into something that can gate a bad provision.
4. Extend the `app_tenant_scope`-table pattern to `ALLOWED_FIELD_TENANT_SLUGS` and the scheduler slug lists.
5. Decide whether dedicated tenant projects join the DR system, and whether per-tenant email identity is worth building.
6. Fix or delete the stale `onboard-trial-tenant` runbook.
7. Land the 0308/0309 legacy-baseline pair only after its two self-documented bugs (hardcoded UUIDs, migration ordering) are actually resolved — not as a default merge.

## Cross-references

- `sessions/2026-09-09.md` — full incident narrative, multiple entries across the day.
- `eq/sprints/2026-09-09-tenant-onboarding-sprint.md` — decisions #1-3, build items #4-9 (Cards-side gaps, tier sync, isolation model).
- `eq/sprints/2026-09-09-provisioning-completeness-followup.md` — the pg_cron/legacy-baseline PR split, the live-only inventory triage plan.
- `system/dr-backups.md`, `system/infra-redundancy-scoping-2026-08-11.md`, `eq/sprints/2026-09-09-redundancy-review-followups.md` — DR and bus-factor redundancy (the other "redundancy").
- `digest.md` "Waiting on you" — the falsely-stamped ledger item, tracked separately.
- `system/failures.md` F17 — the concurrent-clobber bug behind coordination lesson #3.

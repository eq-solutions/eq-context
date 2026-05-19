---
title: EQ Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-19
scope: EQ Solutions to-do list; overwrite in place
read_priority: critical
status: live
---

# EQ Tier — Pending

EQ Solutions work only. SKS items live in `sks/pending.md`. OPS items
(entities, tax, infra) in `ops/pending.md`.

---

## EQ Solves Field — LEAD MODULE

**Multi-tenancy plan locked 2026-04-27** — see
`eq/field/multi-tenancy/plan.md` for living spec.

**Validation gate:** 5 outside-SKS trade subbies on Field demo before
any further build investment.

- [ ] Identify first 5 outside-SKS trade subbies for demo engagement
- [ ] Send outreach message to first target (trade business outside SKS)
- [ ] Build sales motion — stop building features before first external user
- [ ] Netlify env var cleanup — delete SECRET_SALT, STAFF_HASH, MANAGER_HASH
      (folds into Phase 1 role-system migration when implementation starts —
      single change instead of two)
- [ ] Clear Supabase rate_limits table on demo branch (ktmjmdzqrogauaevbktn)
- [ ] Write fresh Cowork brief for EQ Field (guardrails, demo branch rules)

### Tender Pipeline — SKS promotion (blocked)

Shipped to demo 2026-05-14 (v3.4.79 → v3.4.84 across patches). Do NOT
promote to `main`/SKS until all three are cleared:

- [ ] Apply migrations 001 + 002 to SKS Supabase (`nspbmirochztcjijmcrx`)
- [ ] Remove pipeline tables from `TENANT_DISABLED_TABLES.sks` in
      `scripts/app-state.js`
- [ ] Backfill `migrations/` on disk from `list_migrations` MCP
      (applied via MCP only — not on disk)

Open Tender Pipeline items (demo):

- [ ] Wire `clash_detected` PostHog event (reserved in
      `tender-pipeline.js`, not yet firing)
- [ ] Decide `pending_schedule` table fate — currently written but
      bypassed (Confirm Curve writes direct to `schedule`). Either
      promote it to a real CM-editable staging queue with a second
      approval page, or drop it and treat `schedule` as the single
      source of truth
- [ ] Lazy-load SheetJS if first-load bundle size becomes a problem
      (~250KB added)

### Phase 1 — implementation (in progress on `claude/hopeful-wright-058c8b`)

5 commits past `demo` tip on feature branch; not merged.

- [x] `scripts/flags.js` PostHog wrapper — commit `e9b4706`
- [ ] `feat_project_hours_v1` flag in EQ PostHog project (`phc_zXpRxm6Q…`),
      default off, targeted at Royce only first **(Royce manual step)**
- [x] `sites.track_hours` + `sites.budget_hours` SQL written —
      `migrations/2026-04-27_sites_track_hours.sql` (commit `8b6bdb1`)
- [ ] Apply that migration to `ktmjmdzqrogauaevbktn` via Supabase MCP /
      Studio **(Royce manual step — review SQL first)**
- [x] Project-hours UI scaffolding: self-mounting burn-down panel —
      commit `89f96dc`. Activates when both gates open (PostHog flag on +
      `EQ_PERMS.can('ph.view_dashboard')` true). Graceful empty / coming-soon
      states until migration is applied.
- [x] `eq_role` Postgres enum + `people.role` column SQL written —
      `migrations/2026-04-27_eq_role_enum_people_role.sql` (commit `8b6bdb1`).
      Header includes verification queries to run before applying.
- [ ] Apply that migration to `ktmjmdzqrogauaevbktn` **(Royce manual step —
      verify pre-conditions in header first)**
- [ ] `verify-pin.js` rewrite: tenant slug from URL path → `tenant_id` lookup;
      single tenant PIN from `organisations.tenant_pin`; role from
      `people.role`; mints Supabase-native JWT with `app_metadata.tenant_id`
      and `app_metadata.eq_role` **(auth change — needs Chat review per
      `rules/non-negotiables.md`)**
- [x] `scripts/permission-matrix.js` (matrix v1) + `scripts/permissions.js`
      (`EQ_PERMS.can()` + `.role()` + `.list()`) — commits `f2d0e91`, `b367eb1`
- [x] Strategy decided: existing `isManager` global stays; `EQ_PERMS` reads
      it as primary today-path signal. Legacy migration is opportunistic,
      not a sweep (97 occurrences ruled out wholesale refactor).
- [x] PR [#23](https://github.com/Milmlow/eq-field-app/pull/23) merged to
      `demo` (merge commit `996a895`, 2026-04-27 09:36 UTC). Netlify
      auto-deploy triggered. Verify Project Hours panel appears on
      eq-solves-field.netlify.app once deploy lands.

### Phase 2 — multi-tenancy foundation (gated on customer trigger)

Do **not** start until one of these fires:

- First self-serve trial signup is on a calendar
- ~3 customers manually provisioned and per-customer ops cost is biting

Items when triggered:

- [ ] FK + NOT NULL + CHECK constraints on all 14+ `org_id` columns
- [ ] RLS policies, per-table behind a kill switch (`mt_rls_strict` flag),
      lowest-traffic table first
- [ ] Edge function audit (`supervisor-digest`, `ts-reminder`) — service-role
      bypasses RLS, so `org_id` filter discipline must be explicit in queries
- [ ] Demo-mode redesign — currently bypasses Supabase entirely; must hit a
      sandboxed real tenant for self-serve trials
- [ ] Routing infrastructure (Cloudflare Worker proxy on
      `eq.solutions/field/*` OR `field.eq.solutions` subdomain on Netlify)

---

## EQ Solves Service

- [ ] **Delta WO import — live dry-run** on SKS tenant with Aug 2025 file:
      confirm ~250 rows resolve, MVSWBD fuzzy prompt fires, LBS unknown-code
      prompt works, commit succeeds, re-upload triggers duplicate blocker
- [ ] Full-repo file-header backfill (EQ-IP-Register P2 #7 scope A) —
      dedicated session
- [ ] Continue sprint cadence (22 sprints to date, 80 Vitest tests)

---

## CRITICAL — Rotate GitHub PATs (substrate exposure)

Discovered 2026-05-19: `system/infrastructure.md` was tracking the literal
values of all 3 GitHub PATs in plaintext from at least 2026-05-15. GitHub
push-protection caught the pattern when this commit re-touched the file
and rejected the push. Older commits in the substrate history likely
contain the same values and were pushed before push-protection caught up.

**Treat all 3 as compromised regardless of which got "removed" from
`.git-credentials.*` files** — they've been on GitHub.

- [ ] **Revoke all 3 PATs** in GitHub Settings → Developer settings →
      Personal access tokens. Labels: "EQ Solutions", "Milmlow",
      "Milmlow alt".
- [ ] **Issue one new fine-grained PAT** to replace EQ Solutions (the
      other two were duplicates / stale).
- [ ] Update `C:\Projects\.git-credentials.eq-solutions` and
      `C:\Projects\.git-credentials` on the Beelink with the new value.
- [ ] **Verify push works** on eq-context against this commit if the
      auto-push hook didn't already.
- [ ] **Substrate hardening** — consider adding `gitleaks` (or similar)
      pre-commit hook on the eq-context repo so secret-scan happens
      locally before push.

---

## EQ Shell + EQ Intake (per-tenant Supabase rollout)

Two-Supabase architecture confirmed 2026-05-19 (see `system/architecture.md`
"Control Plane + Per-Tenant Data Planes"):

- `eq-shell-control` (`hxwitoveffxhcgjvubbd`) — shared, live, used by
  EQ Shell Netlify functions.
- `eq-canonical` (`jvknxcmbtrfnxfrwfimn`, renamed 2026-05-19 from
  `eq-demo-canonical`) — reference data plane, live, used by EQ Intake.
- `sks-canonical-eq` — planned, not yet provisioned.

### Dedupe-on-ingest skill (intake feature)

Decision logged 2026-05-19 in `ops/decisions.md` ("Dedupe Is Intake's
Job, Not Per-App"). When EQ Intake ingests a CRM export, the
collapse-dupes step (e.g. "47 rows of Equinix Australia Pty Ltd →
1 customer + 47 sites") happens inside intake via the Confirm-UI,
not inside the app reading the data. Implementation detail to be
added to `eq-intake/CONFIRM-UI-SPEC.md` as a new section.

- [ ] **Extend `eq-intake/CONFIRM-UI-SPEC.md`** with a "Dedupe
      confirmation step" section (confidence tiers, screen sketch,
      signature caching). Companion to the existing column-mapping
      confirmation spec.
- [ ] **Implement the dedupe step in the intake pipeline** — runs
      AFTER column-mapping is confirmed, BEFORE the commit_batch
      call. Two confidence tiers (HIGH = exact normalized name
      match, MEDIUM = fuzzy match needing review).
- [ ] **Test against the SimPRO bundle** — 524 customer-site rows
      should collapse to ~150 unique customer rows + 524 site rows
      in canonical.

### EQ Shell Phase 1.B (Netlify wire-up)

- [ ] Confirm Phase 1.B status — Royce reported "almost working" on
      2026-05-19; not picked up this session, sitting in
      `C:\Projects\eq-shell\.claude\worktrees\angry-morse-56771d`
      on branch `claude/angry-morse-56771d`.

### eq-demo-canonical — security advisor cleanup (open)

Diagnosed 2026-05-19. 17 advisor warnings, fix drafted but not applied.

- [ ] **Apply migration 004 to `eq-demo-canonical`** —
      `C:\Projects\eq-intake\sql\004_security_advisor_fix.sql`
      rewritten 2026-05-19 to grant EXECUTE to `authenticated`
      (not `service_role` — see session log for why). Paste into the
      Supabase SQL editor for the project and Run.
- [ ] **Toggle leaked-password protection** in eq-demo-canonical
      dashboard → Authentication → Providers → Email → enable
      HaveIBeenPwned check.
- [ ] **Commit + push the two eq-intake edits** —
      `sql/004_security_advisor_fix.sql` and
      `eq-platform/scripts/db-apply.ts` are uncommitted in
      `C:\Projects\eq-intake` (no auto-push hook on that repo, no
      GitHub remote either per `system/infrastructure.md`).
- [ ] **Smoke-test intake commit after applying 004** — through the
      signed-in shell, an intake commit through the demo path should
      still succeed (authenticated grant retained). An anon-key curl
      to the same RPC should now return 403.
- [ ] **Decide on server-side commit RPC migration** — the 4
      remaining "Signed-In Users Can Execute SECURITY DEFINER"
      warnings clear only if the commit moves to a Netlify Function
      (service-role) AND the in-function `auth.jwt()` tenant check
      is rewritten. Deferred — no urgency until `sks-canonical-eq`
      is provisioned with real users.

### sks-canonical-eq provisioning (gated, not started)

- [ ] Provision `sks-canonical-eq` Supabase project (Sydney /
      `ap-southeast-2`).
- [ ] Run `pnpm db:apply` from `eq-platform/` to regenerate
      `all-migrations.sql` with 004 bundled (`db-apply.ts` updated
      2026-05-19).
- [ ] Paste `all-migrations.sql` into the new project's SQL editor.
- [ ] Add Royce as the first user with `user_metadata.tenant_id`
      set to the SKS tenant uuid.
- [ ] Drop SKS credentials into the Netlify env vars for the
      production shell deployment.

---

## EQ GTM — PRIORITY (gates further build)

- [ ] First outreach message sent (trade business outside SKS)
- [ ] First demo booking confirmed
- [ ] 5/5 validation gate cleared

---

## EQ Brand & Legal

- [ ] EQ-IP-Register P1 #1 — IP-clarity email to SKS Technologies
      (formalise arm's-length commercial relationship for EQ Solves Service)
- [ ] EQ-IP-Register P1 #2 — repo visibility audit (confirm
      `eq-solves-service` private; flip any that drifted)
- [ ] EQ-IP-Register P1 #3 — Webb TM brief for software classes 9 + 42
- [ ] EQ trademark: monitor publication after 18 August 2026
- [ ] EQ business name renewal — November 2026
- [ ] 

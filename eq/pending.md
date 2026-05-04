---
title: EQ Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-04
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

## EQ GTM — PRIORITY (gates further build)

- [ ] First outreach message sent (trade business outside SKS)
- [ ] First demo booking confirmed
- [ ] 5/5 validation gate cleared

---

## EQ Brand & Legal

- [ ] EQ-IP-Register P1 #1 — IP-clarity email to SKS Technologies
      (formalise arm's-length commercial relationship for EQ Solves Service)
- [ ] EQ-IP-Register P1 #2 — repo visibility audit (confirm
      `eq-solves-service`, `eq-solves-assets` private; flip any that drifted)
- [ ] EQ-IP-Register P1 #3 — Webb TM brief for software classes 9 + 42
- [ ] EQ trademark: monitor publication after 18 August 2026
- [ ] EQ business name renewal — November 2026

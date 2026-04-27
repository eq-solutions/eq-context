---
title: State — Pending Actions
owner: Royce Milmlow
last_updated: 2026-04-27
scope: Live to-do list across all workstreams; overwrite in place
read_priority: critical
status: live
---

# State — Pending Actions

Items grouped by workstream. Tick off or remove when done.

---

## Infrastructure — Live Blockers

- [ ] **OAuth GitHub MCP connector** — consent-screen auto-login loop blocks org-picker flow for `claude.ai` chat. Cowork writes are unblocked via PATs (2026-04-19); this item only gates the chat surface. Fix: revoke prior OAuth grant at `github.com/settings/applications`, sign out, reconnect from Claude desktop.
- [ ] **PAT rotation** — Milmlow + eq-solutions fine-grained PATs expire 2026-05-19. Calendar reminder set for 2026-05-16.

## SKS Operations — Infrastructure (HIGH RISK)

- [ ] SKS Labour Supabase backup strategy — no scheduled backups, ~55 staff depend on the app (project: nspbmirochztcjijmcrx)
- [ ] Resend email deliverability issue — unresolved
- [ ] Netlify rollback tagged release for SKS Labour

## SKS Commercial — Live

- [ ] DigiCo busway/busduct dispute — consolidate defensive position (VAR-003 15 Dec + Feb parts list)
- [ ] NEXTDC S3 tender — pricing workbook / submission
- [ ] AirTrunk SYD3 transformer commissioning — documentation pack
- [ ] Equinix SY6 CUFT — programme structure finalisation
- [ ] AWS SYD053 — ongoing WHIP install programme (3,220+)

## SKS Receipt Tracker

- [ ] Deploy Cloudflare Worker (anthropic-proxy) — follow DEPLOY.md
- [ ] Battle-test: receipt scanning, Excel export, data persistence
- [ ] Broader SKS staff testing

## EQ Solves Service — PRIMARY BUILD

- [ ] **Delta WO import — live dry-run** on SKS tenant with Aug 2025 file: confirm ~250 rows resolve, MVSWBD fuzzy prompt fires, LBS unknown-code prompt works, commit succeeds, re-upload triggers duplicate blocker
- [ ] Full-repo file-header backfill (EQ-IP-Register P2 #7 scope A) — dedicated session
- [ ] Continue sprint cadence (22 sprints to date, 80 Vitest tests)

## EQ Field App

**Multi-tenancy plan locked 2026-04-27** — see
`sessions/2026-04-27.md` for decisions and
`eq-solves-field/.claude/worktrees/hopeful-wright-058c8b/MULTI-TENANCY-PLAN.md`
for the living spec.

- [ ] Netlify env var cleanup — delete SECRET_SALT, STAFF_HASH, MANAGER_HASH
      (folds into Phase 1 role-system migration when implementation starts —
      single change instead of two)
- [ ] Clear Supabase rate_limits table on demo branch (ktmjmdzqrogauaevbktn)
- [ ] Write fresh Cowork brief for EQ Field (guardrails, demo branch rules)

### Phase 1 — implementation (pending Royce go-ahead)

Locked plan; not yet started. Starts when Royce gives the word.

- [ ] `scripts/flags.js` PostHog wrapper (loaded after `analytics.js`)
- [ ] `feat_project_hours_v1` flag in EQ PostHog project (`phc_zXpRxm6Q…`),
      default off, targeted at Royce only first
- [ ] `sites.track_hours` + `sites.budget_hours` migration on
      `ktmjmdzqrogauaevbktn`
- [ ] Project-hours UI: supervisor "Project Hours" tab with burn-down per
      tracked site
- [ ] `eq_role` Postgres enum + `people.role` column migration
- [ ] `verify-pin.js` rewrite: tenant slug from URL path → `tenant_id` lookup;
      single tenant PIN from `organisations.tenant_pin`; role from
      `people.role`; mints Supabase-native JWT with `app_metadata.tenant_id`
      and `app_metadata.eq_role`
- [ ] `scripts/core/permissions.js` (`EQPerms.can()`) + matrix v1 JSON
      embedded in `scripts/core/permission-matrix.js`
- [ ] Existing `role === 'supervisor'` UI checks migrated to `EQPerms.can(...)`

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

## EQ Expenses

- [ ] Cloudflare Worker proxy — end-to-end test with real receipt
- [ ] Full EQ branding pass (bugs first)

## EQ GTM — PRIORITY

- [ ] Identify first 5 external paying customers for EQ Field
- [ ] Send outreach message to first target (trade business outside SKS)
- [ ] Build sales motion — stop building features before first external user

## Tax & Entities (Webb Financial)

- [ ] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft
- [ ] Personal vehicle depreciation amendment (~$33,800 refund)
- [ ] Emma FY23/24 ITR amendment
- [ ] EQ Property Solutions TFN receipt

## EQ Brand & Legal

- [ ] EQ-IP-Register P1 #1 — IP-clarity email to SKS Technologies (formalise arm's-length commercial relationship for EQ Solves Service)
- [ ] EQ-IP-Register P1 #2 — repo visibility audit (confirm `eq-solves-service`, `eq-solves-assets` private; flip any that drifted)
- [ ] EQ-IP-Register P1 #3 — Webb TM brief for software classes 9 + 42
- [ ] EQ trademark: monitor publication after 18 August 2026
- [ ] EQ business name renewal — November 2026
- [ ] Milmlow Holdings / MFT / Allcraft review — September 2026

---

## Parked — Revisit 2027

### Australian Housing Dividend (AHD)

Parked from public-facing materials; revisit for capital activation by 2027. Keep structure warm but not active.

- [ ] TFN receipt from ATO
- [ ] Correct ABR business activity code to 6711
- [ ] Engage solicitor for ISA, MIS Position Paper, EISP sign-off
- [ ] First property acquisition — Adelaide North corridor / SE QLD fallback
- [ ] Government engagement letter (NSW Treasurer) — post first bonus paid

---

## Completed (recent)

- [x] MD failsafe stack added — eq-context/.gitignore, .githooks/pre-commit, .github/workflows/md-health.yml, scripts/install-hooks.ps1, MD_BEST_PRACTICES.md §17, daily Cowork audit task — 2026-04-26
- [x] eq-context audit cleanup — duplicate session removed, _cleanup-patch folder retired, drafts/ folder added, accidental binary zip purged — 2026-04-26
- [x] Conflict markers from stash-pop resolved in CLAUDE.md, state/pending.md, state/products.md — 2026-04-26
- [x] Delta/Equinix WO Excel import **merged to main** in eq-solves-service — parser + levenshtein fuzzy match + preview/commit actions + wizard UI + WO# on PM report; migrations 0049 (job_plan_aliases) + 0050 (WO# unique idx) applied; 38/38 tests passing, tsc clean, advisors 0 new ERROR — 2026-04-19
- [x] IP Protection scaffolding **merged to main** in eq-solves-service — EQ footer, sticky attribution, `/terms`, login splash, migration 0048, headers on entry points — 2026-04-19
- [x] Migration 0048 (`public._meta` ownership marker) applied to eq-solves-service-dev — 2026-04-19
- [x] GitHub PATs issued (Milmlow + eq-solutions, fine-grained, 30-day) — first Cowork → GitHub push succeeded — 2026-04-19
- [x] Full context repo audit + rewrite — 2026-04-18
- [x] EQ Design Brief v1.3 published (17 Apr 2026, supersedes v1.2)
- [x] eq-context GitHub Action expanded to sync all subdirs — 2026-04-12
- [x] CLAUDE.md rewritten to reflect current reality — 2026-04-12
- [x] GitHub Action sync confirmed firing correctly — 2026-04
- [x] MD best-practice pass (frontmatter, AGENTS.md, cross-LLM portability) — 2026-04-10
- [x] SKS Labour caching strategy fixed (service worker) — 2026-04-11
- [x] SKS favicon set built (ico, apple-touch, 192, 512) — 2026-04-11
- [x] EQ Expenses offline-first HTML built — 2026-04-09
- [x] Cloudflare Tunnel on Beelink (beelink.eq.solutions) — 2026-04-10
- [x] Google Drive lane decision: EQ → Drive, SKS → OneDrive — 2026-04-09
- [x] Claude use review — 8.5/10, gaps: GTM + MD discipline — 2026-04-12
- [x] EQ trademark accepted by IP Australia — 2026-04-01
- [x] EQ Property Solutions incorporated — 2026-03-14
- [x] Contacts list rebranded Delta Elcom → SKS Technologies (44 staff) — 2026-03/04
- [x] SKS Quote Template v3 built — 2026-04-15

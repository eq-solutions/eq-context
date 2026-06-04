---
title: EQ Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-06-05
scope: EQ Solutions to-do list; overwrite in place
read_priority: critical
status: live
---

# EQ Tier — Pending

EQ Solutions work only. SKS items live in `sks/pending.md`. OPS items
(entities, tax, infra) in `ops/pending.md`.

---

## ⏩ Session close — 2026-06-05

**Completed (EQ Field):**
- v3.5.73 — job numbers on the weekly schedule (project→job, derived onto roster grid + My Schedule). PR [#186](https://github.com/eq-solutions/eq-field/pull/186), merged, live.
- v3.5.74 — per-cell job **pin** for multi-job sites (Edit Roster pick-list; pin > project primary > none). PR [#187](https://github.com/eq-solutions/eq-field/pull/187), merged, live.

**Deferred (next step, Royce-gated):**
- [ ] Auto-fill labour-hire/apprentice Field timesheets from the roster job pin (the invoice-reconciliation path). Held deliberately — touches the accounts reconciliation.

**Rollout note:** a site only offers a job pick-list when its jobs are tagged to it (Job Numbers → Site, `job_numbers.site_name`).

**⚠ Correction to a carried-forward action (below):** the "Downgrade/pause `ktmjmdzqrogauaevbktn`" item is **BLOCKED** — verified 2026-06-05 that this DB is still the **live EQ data plane** (serves all projects/sites/jobs/people/schedule; the zaap `app_data.field_*` twins are empty). Pausing it takes EQ Field down. Do not action until the canonical reseed/cutover lands.

---

## ⏩ Session close — 2026-06-04

**Completed (EQ Field):**
- v3.5.72 — removed the "Pick a demo tenant" workspace picker; EQ Field now boots straight into the default `eq` tenant (PR [#185](https://github.com/eq-solutions/eq-field/pull/185), merged, live). Demo tiers still reachable via `?tenant=demo-trades` / `?tenant=melbourne`.

**Pending Royce-actions (carried forward):**
- [ ] Downgrade old EQ DB `ktmjmdzqrogauaevbktn` → free tier in Supabase dashboard, then pause it (paid projects can't be paused via API)
- [ ] `TENANT_ORG_UUID` Netlify env var for eq-solves-field EQ site (blocks U6 PIN)
- [ ] Revoke old `gho_...` PAT at github.com/settings/tokens
- [ ] Drift CI secrets in eq-shell GitHub repo settings
- [ ] HaveIBeenPwned toggle in eq-canonical Supabase Auth settings

---

## ⏩ Session close — 2026-06-03 (PM) — EQ Field anon-remediation Phase 2 + SKS sync

**Completed (all prod-verified; EQ repo only, no cross-deploy):**
- **Phase 2 (Goal 1 — secure same-shape):** 22 Field surfaces moved off the anon key onto the
  authenticated data-plane JWT + RLS via `app_data.field_<name>` twins (`LIKE public.*` + tenant_id,
  anon revoked, granted authenticated). anon REVOKED on all 22 `public.*` (prod anon→401).
  v3.5.62 (11 surfaces) → v3.5.63 (tender pipeline, 323 rows preserved) → v3.5.64 (close leak +
  bucket-B + realtime). PRs #170–172.
- **Dropped 9 dead/empty Field tables** on EQ/zaap (bucket-D). Foreign tables (workers/worker_*/
  qualifications, organisations) left untouched (shared DB).
- **realtime.js** repointed to the secured twins via the data JWT (publication set).
- **SKS sync v3.10.50–51 ported** (timesheet jump-to-top fix + Resources this-week strip). v3.5.65, PR #173.
- Migrations on disk in eq-field/migrations/ (applied via MCP to zaap).

**Decision:** Goal 1 = close the hole only, NOT re-home onto canonical (lossy; canonical isn't a
superset — no pin/role, no region/project). The B5 canonical unification stays a separate track.

**Backlog (deferred, Royce-gated):**
- [ ] **`app_config` PIN-read auth refactor** — last real anon leak; can't be JWT-gated (gate reads
      it pre-login). Needs login-touching change to stop the browser reading PINs.
- [ ] **Realtime browser verification** — repointed but not eyeballed (EQ demo twins empty); fails
      safe to 30s poll.
- [ ] **Drop the revoked `public.*` husks + `public.tenders` fallback** once confident (anon already
      revoked — not leaking).
- [ ] **Apprentices module** — neither wired nor dropped (not in use); secure-or-retire when needed.
- [ ] SKS (separate repo/DB) inherits the Goal-1 pattern when its anon-remediation runs.

---

## ⏩ Session close — 2026-06-03

**Completed (EQ Field pipeline/Resources sprint — all live; mirrored to SKS standalone):**
- Resources: Remove/archive job (v3.5.53–54, BUG-009 modal-confirm fix)
- Pipeline: value + probability sliders + Keep/Discard triage (v3.5.55)
- Pipeline: Estimator + Builder filters (v3.5.56)
- Resources: edit confirmed-job details + pipeline Start-date tag (v3.5.57)
- Resources: editing workers/duration rebuilds the labour plan (v3.5.58)
- Pipeline import: email-form estimator normalisation + one-time SQL dedupe both DBs (v3.5.59)
- EQ pipeline data migrated `ktm` → `eq-canonical-internal` (pipeline only; roster intentionally NOT migrated — Royce: not relevant)
- SKS standalone kept in lockstep: v3.10.44 → v3.10.49
- Smartsheet import reviewed — parse→preview→confirm gate confirmed safe; no change needed

**Pending Royce-actions (carried forward + new):**
- [ ] **NEW:** Downgrade old EQ DB `ktmjmdzqrogauaevbktn` → free tier in Supabase dashboard, then pause it (paid projects can't be paused via API). Dead cold-backup, unused by live EQ Field.
- [ ] `TENANT_ORG_UUID` Netlify env var for eq-solves-field EQ site (blocks U6 PIN)
- [ ] Revoke old `gho_...` PAT at github.com/settings/tokens
- [ ] Drift CI secrets in eq-shell GitHub repo settings
- [ ] HaveIBeenPwned toggle in eq-canonical Supabase Auth settings

---

## ⏩ Session close — 2026-06-02

**Completed this session:**
- Tenant model confirmed + documented (STATE.md / architecture.md / infrastructure.md)
- `tenant_routing` gap fixed — canonical-api routing now live end-to-end (sks → sks-canonical)
- EQ Quotes wiring audited ✅; stale `SUPABASE_URL` removed from fly.toml
- EQ Service canonical wiring audited ✅ (write-through live, 4 export stubs non-blocking)
- eq-solves-field CLAUDE.md committed to main
- eq-shell build fixed (cap_exceeded union + never cast in errorSummary) — `core.eq.solutions` live

**Pending Royce-actions (carried forward):**
- [ ] `TENANT_ORG_UUID` Netlify env var for eq-solves-field EQ site (blocks U6 PIN)
- [ ] Revoke old `gho_...` PAT at github.com/settings/tokens
- [ ] Drift CI secrets in eq-shell GitHub repo settings
- [ ] HaveIBeenPwned toggle in eq-canonical Supabase Auth settings
- [x] Merge eq-roles PR `bold-boyd-e6afae` → publish v1.3.0 ✅ 2026-06-02 (v1.3.0 tagged, eq-shell bumped to #v1.3.0)

---

## 🟦 Autonomous Sprint — SOURCE OF TRUTH (read first if running sprint work)

Parallel autonomous agents coordinate through three root files (added 2026-05-30):
- `SPRINT-BOARD.md` — full backlog + claim/ownership (claim before you start)
- `AUTONOMOUS-SPRINT-RULES.md` — diverge-proof conventions (branch from origin/main, **timestamp migrations**, SKS-live untouchable, full-auto EQ deploy, auth gated)
- `STATE.md` — per-repo + Supabase reality + known hazards

Autonomy policy: `ops/decisions.md` 2026-05-30. Session log: `sessions/2026-05-30.md`.

**Drift resolved (2026-06-02):** the GTM gate was killed (we build for ourselves — see `ops/decisions.md` 2026-06-02) and the stale gate language was purged from the forward docs. The "two-Supabase obsolete / single canonical" framing is also stale — reality is the two-plane split (`eq-canonical` + `eq-canonical-internal`). `STATE.md` carries current reality.

---

## EQ Design System — consolidation (plan 2026-05-31)

Foundation shipped (One Spine, Stream A): `@eq-solutions/tokens` v1.0 consumed (not vendored) across Shell/Service/Field/Cards; `@eq-solutions/ui` v1.0.1 = Button/Skeleton/Table. Full plan + model: `design-system-consolidation-2026-05-31.md`, `ops/decisions.md` 2026-05-31. Remaining (board rows A7–A12):

- [ ] **A7** eq-ui Modal + ConfirmDialog (fold in a11y A1/A2 from `quality-polish-backlog-2026-05-30.md`)
- [ ] **A8** eq-ui FormInput
- [ ] **A9** eq-ui StatusBadge + KindPill
- [ ] **A10** eq-ui Card + Toast + Tabs (resolve ghost-border → Option B)
- [ ] **A11** Font self-host in the shared package (supersedes per-app P5)
- [ ] Confirm the pin-by-tag migration landed (eq-ui v1.0.1 / eq-roles tags); move any `#main` consumers to `#vX`
- [ ] Add 2 drift items to `quality-polish-backlog-2026-05-30.md`: Service emoji-in-Lucide (~7 files), Service `RouteProgress` cyan→indigo gradient — **verify vs origin/main first**
- [x] **A12** Claude Design context bundle — `eq/design/claude-design-context.md` created + issued to Claude Design 2026-05-31
- [x] Quotes (Flask) decision — **leave at 85%**, no investment (React rewrite supersedes, ~2–3mo)

---

## EQ Solves Field — LEAD MODULE

**Multi-tenancy plan locked 2026-04-27** — see
`eq/field/multi-tenancy/plan.md` for living spec.

**No validation gate.** EQ is built for ourselves (SKS NSW) because it's
a good product — build investment is sequenced by the trust ladder +
Royce's go, not by outside-customer validation (gate killed 2026-06-02,
see `ops/decisions.md`).
- [x] Netlify env var cleanup — confirmed clean 2026-05-29 (prior session
      deleted hashes; only `EQ_SECRET_SALT` + active vars remain)
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
- [x] `verify-pin.js` Phase 1 wiring (2026-05-29) — PIN path now derives and
      returns `eq_role` ('supervisor'/'employee'); all 3 auth paths store
      `eq_role` in `window.EQ_SESSION.app_metadata.eq_role`; shipped as
      **v3.5.23, PR #135** on eq-solutions/eq-field.
      **Royce: smoke deploy-preview then squash-merge PR #135.**
      Full verify-pin rewrite (tenant-slug → DB lookup, per-user JWT) is
      Phase 2 multi-tenancy work — still gated.
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

## EQ Shell + EQ Intake

> **⚠ SUPERSEDED (2026-05-30) — the architecture + gate notes in this section are STALE; `STATE.md` carries current reality.** (1) The **two-plane** model is current, NOT "single canonical": browser → `eq-canonical` (control plane) + tenant data **server-only** in `eq-canonical-internal` (`zaapmfdkgedqupfjtchl`). The "Two-Supabase obsolete / single canonical" copy below is itself now obsolete. (2) The **GTM validation gate was REMOVED** — do NOT block Shell Phase 2 (or any EQ work) on outside-customer validation (see `ops/decisions.md` + memory `feedback_gtm_intent`). Historical detail below kept for record only.

**Status as of 2026-05-20:** Phase 1.E + 1.F shipped (single canonical
Supabase, Intake module live at `/core/intake`, Unified Identity, RLS
swept to `app_metadata`). Phase 2 paused — no further shell modules
until the GTM validation gate clears (see EQ GTM PRIORITY section
below) OR a paying customer specifically asks for one.

**Two-Supabase architecture is OBSOLETE** as of Phase 1.E (2026-05-19).
Current state:

- `eq-canonical` (`jvknxcmbtrfnxfrwfimn`) — single canonical project
  holding both shell control tables (`tenants`, `users`,
  `module_entitlements`) and tenant application data (13 canonical
  entity tables incl. `licences` added 2026-05-20 part-c). Region
  `ap-southeast-2`.
- `eq-shell-control` (`hxwitoveffxhcgjvubbd`) — **DECOMMISSIONED**
  2026-05-19 per `sessions/2026-05-19.md`.
- `sks-canonical-eq` — planned, not provisioned. Gated on GTM
  validation gate, not on shell readiness.

### Critique action items — deferred to Phase 2 resumption

Three external-model critiques (Claude / Grok / ChatGPT) shopped
2026-05-20 part-d. The actions below are real risks the architecture
carries today. They DO NOT ship until Phase 2 resumes (GTM gate
clears, or a paying customer requests a new module). Priority order
= highest blast-radius first.

- [ ] **Dual-salt rotation support for `EQ_SECRET_SALT`** — both
      shell-side `mint-iframe-token` and Field-side validator accept
      salt-A and salt-B; mint with salt-B; redeploy both; wait for
      token TTL; remove salt-A. Without this, a salt leak forces a
      coordinated outage to rotate. Shared secret across two Netlify
      projects is the single highest-blast-radius risk in the stack.
- [ ] **Dual-secret support in `verify-shell-session`** for
      `SUPABASE_JWT_SECRET` rotation. Same rationale.
- [ ] **`revoked_sessions` table** + shorten JWT TTL from 1 hour to
      ~30 minutes. Without this you cannot kill an active session
      before its TTL expires.
- [ ] **Schema split** — `shell_control.*` (tenants/users/
      module_entitlements) vs `app_data.*` (canonical entities) in
      the same `eq-canonical` project. `CREATE SCHEMA` +
      `search_path` update. Free now, saves ~3 weeks when a regional
      secondary is needed.
- [ ] **Per-domain RPC decomposition** — split
      `eq_intake_commit_batch` before it accumulates 5 module
      branches. Per-entity validators in a shared library; per-domain
      RPCs call the library. Currently 1 mega-RPC handles all
      mutation; this is the chokepoint all three critiques flagged.
- [ ] **Canonical → Field one-way sync rule** documented + enforced
      with a Supabase trigger for shared concepts (staff, sites,
      schedule_entries). Never the reverse. Otherwise dual-write
      pain during iframe-purgatory becomes uncontrolled.
- [ ] **Token-mint audit log** (tenant_id, IP, timestamp) with a
      Sentry threshold alert per `https://mcp.sentry.dev/mcp/eq-solutions/eq-shell`.
      Today there's no detection mechanism for a stolen salt.
- [ ] **Build-time hash check** for the vendored `@eq/*` packages so
      a stale vendor can't silently ship through Netlify.
- [ ] **`STABLE SECURITY DEFINER` wrapper** for the `tenant_id` UUID
      cast read in every RLS predicate (perf optimisation for the
      day load matters).
- [ ] **Iframe retirement deadline decision** — Grok pushed 9 months,
      Claude said 3 years is a roadmap not purgatory, ChatGPT said
      4 years is the modal failure mode. Pick a number, write it
      somewhere, hold to it. Not a code task; a strategic decision
      Royce makes when Phase 2 resumes.

Full critique synthesis + the items already shipped (so we don't
re-litigate them) is in [sessions/2026-05-20-part-d.md](../sessions/2026-05-20-part-d.md).

### Substrate-drift note (2026-05-20 part-d)

The `eq-shell/README.md` Phase 2 row said "Tender Pipeline first"
through 2026-05-20. This was a stale claim — Tender Pipeline is a
Field sub-module, not a flagship shell module. The README has been
corrected. Going forward: when writing critique prompts or briefing
external models against the shell, read the substrate actively, do
not just copy what the README says — and check for drift signals
(passing pivots that have hardened into "platform doctrine"
language).

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

### EQ Shell Phase 1.B (Netlify wire-up) — DONE

- [x] Phase 1.B (Netlify wire-up), 1.C (Field-side `?sh=` handler),
      1.D (end-to-end smoke), 1.E (single-canonical consolidation),
      1.F (Unified Identity + `app_metadata` RLS sweep) — all
      shipped by 2026-05-20. `core.eq.solutions` live, Intake module
      at `/core/intake` running the `@eq/*` engine end-to-end.

### eq-demo-canonical — security advisor cleanup (open)

Diagnosed 2026-05-19. 17 advisor warnings, fix drafted but not applied.

- [ ] **Apply migration 004 to `eq-demo-canonical`** —
      `C:\Projects\eq-intake\sql\004_security_advisor_fix.sql`
      rewritten 2026-05-19 to grant EXECUTE to `authenticated`
      (not `service_role` — see session log for why). Paste into the
      Supabase SQL editor for the project and Run.
- [ ] **Toggle leaked-password protection** in eq-canonical (`jvknxcmbtrfnxfrwfimn`)
      dashboard → Authentication → Settings → enable HaveIBeenPwned check.
      **(Royce manual step)**
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

## EQ Cards — canonical flip follow-ups (shipped 2026-05-21)

- [ ] **Licence p

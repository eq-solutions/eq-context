---
title: EQ Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-06-08
scope: EQ Solutions to-do list; overwrite in place
read_priority: critical
status: live
---

# EQ Tier — Pending

EQ Solutions work only. SKS items live in `sks/pending.md`. OPS items
(entities, tax, infra) in `ops/pending.md`.

---

## ⏩ Session close — 2026-06-08 — EQ Field Sentry crash fixes

**Completed:**
- [x] **v3.5.99 verified live** — EQ-FIELD-3 (isLeave) + EQ-FIELD-4 (auditLog) confirmed
      resolved in Sentry; no new occurrences since deploy. Both marked resolved with notes.
- [x] **v3.5.100 shipped + live** — EQ-FIELD-5 (siteColor + getSiteName + isAbsence
      lazy-load race in dashboard.js). PR #230, merged, smoked, production verified.
- [x] **All Sentry eq-field issues resolved** — 0 unresolved. Dashboard lazy-load race
      fully closed for all roster.js dependants.
- [x] **eq-context updated** — sessions/2026-06-08.md, eq/changelog/field.md (v3.5.99 +
      v3.5.100 entries), eq/pending.md.

**EQ Field live version:** v3.5.100

**Deferred (carry forward):**
- [ ] Deploy-preview auth gate (zaap anon-revoked) — `demo-trades` on previews 401s on
      name list. Use `?tenant=demo` to bypass for smoke. Pre-existing, deferred 2026-06-06.
- [ ] eq-context sks/ local edits still uncommitted (`sks/README.md`, `sks/products.md`)
      — Royce to commit via GitHub web UI or emit .bat.
- [ ] eq-context itself — commit + push this session's updates (auto-push hook or manual).

---

## ⏩ Session close — 2026-06-07 (PM) — Cross-app linkage audit

Live-verified map of Cards/Shell/Field/Service/Quotes linkage (4 Supabase projects + 5 repos, read-only).
Full report: [`cross-app-linkage-audit-2026-06-07.md`](../cross-app-linkage-audit-2026-06-07.md).
Gated playbook: [`cross-app-linkage-remediation-plan-2026-06-07.md`](../cross-app-linkage-remediation-plan-2026-06-07.md).
Sprint (steelman-corrected, 10/10): [`cross-app-linkage-sprint-2026-06-07.md`](../cross-app-linkage-sprint-2026-06-07.md) — 7 workstreams, 4 waves, pre-mortem.

**Headline:** canonical model (`ehow.app_data`) is FK-wired but its linking rows are empty (`jobs`=0, `quote`=0);
worker→staff link 1/50, customer `canonical_id` 0/520 in live ehow, sites→customer 28/591. Asset sync (4808) works.

**Prioritised actions (all Royce-gated — see plan for mechanism/verify):**
- [ ] **P4 (small, do first):** repoint Cards→Field approval bridge off legacy `ktmj` → live plane (`app_data.staff`). eq-shell repo, PR + gated deploy. **Then** decommission ktmj.
- [ ] **P1a:** resolve GATE A onto eq-cards `claude/otp-tenant-fix` (Option A). **Auth — chat-review before deploy.**
- [ ] **P1b:** backfill `app_data.staff.cards_worker_id` (confirm match key — phone collisions are the landmine; dry-run first).
- [~] **P2:** customer convergence — **PARTIAL APPLIED 2026-06-07** (`_ws1-customer-dedup-2026-06-07.md`): Tier S 38
      stub customers retired (dup-groups 117→80); 28 quotes `canonical_id` linked (1:1-both-sides). **Remaining:** decide
      SoR (rec `app_data.customers`); Tier A merge (26, supervised); Tier C (50 ambiguous) + quotes-side N:1 dedup via
      Intake; 99 dangling sites need source re-import. Note: `sks_quotes_customers.canonical_id` is UNIQUE (1:1) vs N:1 data.
- [x] **P3:** backfill `app_data.sites.customer_id` — **APPLIED 2026-06-07 (ehow)**: 440 sites linked (28→468),
      assets→customer 4769/4808 (99.2%). Reversible; record in `_ws2-site-customer-backfill-2026-06-07.md`. Remaining
      123 sites wait on P2 (customer dedup); `zaap` (30 sites) not yet run.
- [ ] **P5 (decision):** who owns "job/work-order"? `app_data.jobs`=0 → no quote→job trace until decided.
- [ ] **P7a:** SKS anon-remediation (nspb) — exact policy worklist in plan §7a. **SKS-live, gated.**
- [ ] **P7b:** ktmj anon-write policies close via the pause/decommission already pending (after P4).
- [ ] **P7d:** run a `get_advisors` pass on the EQ Service DB `urjhmkhbgaxrofurpbgc` (not yet audited).
- [x] Audit internal authz of jvkn anon RPCs `eq_cards_get_worker_hr_record`, `eq_cards_delete_account` —
      **CLEARED 2026-06-07**: both `SECURITY DEFINER` but scoped to `auth.uid()`; anon has no uid → harmless. Non-issue.

**Drift corrected (live wins):** `architecture.md` "jvkn = no operational data" is false (it's the worker house);
creds 779→737, invites 37→58 since 06-03; `0028_contact_customer_links` IS present on SKS (291 rows).
## SKS Live — roles / security-groups track (2026-06-07)

Parallel to the Field schema/data cutover below. Full plan + agent prompts (A–E): [`sks-live-sprint-2026-06-07.md`](../sks-live-sprint-2026-06-07.md). Live-verified 2026-06-07: `shell_control` has 9 groups / 16 perms / **0** user assignments; tenant `sks` = 3 × manager.

- [ ] **eq-roles** — merge PR #7 → tag `v2.3.0` (unblocks the eq-shell dep bump). *(Royce)*
- [ ] **eq-shell** — converge `c2-shell-roles` + `sks-field-host` into one trunk (Prompt A; Royce picks trunk).
- [ ] **eq-shell Phase 2** — wire group perms into the session as `extra_perms` via `resolveEffectivePermissions` (Prompt B).
- [ ] **eq-shell Phase 3** — `AdminSecurityGroups` page; first write moves `user_security_groups` off 0 rows (Prompt C).
- [ ] **eq-shell Phase 4** — walk ONE real SKS user end-to-end; first-ever `user_security_groups` row (Prompt D).
- [ ] **Phase 5 hardening** — `contact_customer_links` explicit `WITH CHECK` (`::uuid` cast) + CI policy-lint + eq-roles no-orphan-keys test (Prompt E).

---

## ⏩ Session close — 2026-06-06 — SKS tenant LIVE on EQ Field + JWT/RLS Track 2 staged + Teams uuid fix

**SKS is now usable on the EQ Field build** at `field.sks.eq.solutions` (eq-field **v3.5.83**). Big correction vs the earlier draft of this block: **`DATA_JWT_ENABLED` is ON deploy-wide**, so SKS runs on the AUTHED JWT path post-login (not anon parity), and STEP 1 is load-bearing.

**Completed (EQ Field, prod-verified):**
- **v3.5.82 — SKS pipeline JWT+RLS carrier (B5 Track 2)** (PR [#195](https://github.com/eq-solutions/eq-field/pull/195)). Per-tenant data-JWT secret resolver + in-place carrier (`JWT_INPLACE_TENANTS={sks}` → `public.*` on SKS's own Supabase).
- **STEP 1 RLS (authed policies) APPLIED to SKS prod** (migration `sks_pipeline_rls_step1_additive`; 22 `field_authed_*` policies; anon untouched/intact). **Load-bearing** — with the flag on, this is what lets SKS read its own data post-login. **Do NOT roll back.** Dry-run-validated on a disposable Supabase branch first.
- **v3.5.83 — gate anon-fallback fix** (PR [#199](https://github.com/eq-solutions/eq-field/pull/199)). Fixed the empty-gate lock-out (pre-login `sbFetch` of JWT_TABLES couldn't mint → now falls back to anon). Verified live: gate lists 69 SKS names.
- **v3.5.81 — Teams id-type fix for uuid tenants** (PR [#196](https://github.com/eq-solutions/eq-field/pull/196); dup #197 closed).
- **Canonical hostname** for `sks` = `field.sks.eq.solutions` (was repointed to `sks-field.netlify.app` then finalised to the custom domain).
- **Track-2 migration files** PR'd ([#200](https://github.com/eq-solutions/eq-field/pull/200), docs/SQL only): STEP1 (applied), STEP2 lockdown (deferred), PRE-SNAPSHOT, original marked superseded.
- **`core.eq.solutions` → SKS Field WORKING** — eq-shell [#189](https://github.com/eq-solutions/eq-shell/pull/189) (merged + live). The admin auto-route honored a sticky `localStorage` last-pick over the URL tenant, so `/sks/field` loaded the empty EQ tenant; fixed so the active shell tenant wins. Verified live (loads `field.sks.eq.solutions` + sks even with last-pick=eq).
- **SKS-canonical drift fixed:** `app_data.eq_intake_rate_limits` RLS gate `user_metadata`→`app_metadata` on `ehow` (aligned to core; source migration `0023_intake_infra.sql` already correct — SKS had drifted out-of-band). Unblocked the eq-shell schema-drift CI gate.

**Pre-go-live hardening pass (2026-06-06) — advisors swept on nspbmi/ehow/jvkn + dual-write + DEFINER audits:**
- **Dual-write silent-data-loss FIXED (was HIGH).** EQ Field writes `people.employment_type/rto/hire_company` + `sites.project_id`; SKS lacked them → every person/site edit from EQ Field would 400 and silently drop. Added the 4 nullable columns to SKS prod (`nspbmirochztcjijmcrx`), matching the EQ plane. **Smoke a person + site edit post-merge of #202.**
- **SSO "view only" + Teams create FIXED + MERGED** — eq-field [#202](https://github.com/eq-solutions/eq-field/pull/202) (v3.5.85, live): cookie SSO path grants supervisor to platform admins (parity w/ token path); `teams`+`team_members` added to ORG_TABLES (org_id NOT NULL stamping).
- **Team DELETE FIXED + MERGED** — eq-field [#203](https://github.com/eq-solutions/eq-field/pull/203) (v3.5.86, live): `deleteTeam` removes `team_members` links before the team (SKS FK isn't ON DELETE CASCADE → delete had 400'd on any team with members).
- **SKS-canonical rate-limit DEFINER fns hardened (live):** `eq_check/increment_intake_rate_limit` trusted a caller-supplied `p_tenant_id` (cross-tenant) + mutable search_path → pinned search_path + revoked EXECUTE from public/anon/authenticated (sole caller is the api-intake edge fn on service_role). 
- **Audits clean elsewhere:** the 17 other ehow DEFINER RPCs are JWT-tenant-scoped (safe); the 4 anon-callable control-plane Cards DEFINER fns are auth.uid()/token-gated (safe — advisor pattern, not a hole). Control plane has NO anon exposure of registry/config/entitlements.
- **Track-2 SQL artifacts merged** — eq-field [#200](https://github.com/eq-solutions/eq-field/pull/200) (record only).

**Royce decisions (2026-06-06):**
- ❌ **PITR DECLINED** — $100/mo/project too expensive at this scale. Weekly backups stand; ~14-day worst-case RPO accepted (consistent with the existing SKS backup decision). Cheap alt on file if wanted: daily `pg_dump` → storage.
- ❌ **Key rotation DECLINED** for now — `EQ_SECRET_SALT` (exposed shared master key) + `GOOGLE_DOC_AI_CREDENTIALS` rotation deferred at Royce's call; risk accepted. Runbook (`eq-secret-salt-rotation-runbook-2026-06-06.md`) stays on file.

**Remaining for SKS go-live (Royce-gated):**
- [ ] Functional click-through smoke on `core.eq.solutions/sks/field` (supervisor): **person edit + site edit + team create + team delete** (confirm the dual-write/teams fixes) → pipeline / import / resources / roster / safety against SKS data.
- [ ] Cutover **soak** 24–48h with the standalone (`sks-nsw-labour`, v3.10.59) kept warm → then **retire** the standalone.
- [ ] **Track 2 STEP 2 (anon lockdown)** — DEFERRED until the standalone is retired. Then move `AUDIT_SB_KEY` → service_role and drop the `audit_log` anon-insert carve-out.
- [ ] **Onboarding** — invite-claim rollout (only 1 of 36 workers linked; 0/56 invites claimed). Upstream eq-shell #183/#175.

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

## ⏩ Session close — 2026-06-05 (part b) — PostHog MCP + EQ Core go-live readiness

**Done:**
- **PostHog MCP connected** (claude.ai OAuth connector → `mcp.posthog.com`, EU, project 162632). Live-queried. *(Connector is mislabeled "Github" in the connector list — rename when convenient.)*
- **Data read:** ~19 real sticky users (not the inflated 419 UUIDs), growing usage, flat retention tail. Auth surface most-exercised.
- **Go-live readiness verified vs LIVE systems** → no structural blockers. Canonical DB healthy + RLS-clean + 0 ERROR advisors; auth/iframe-SSO engineered; anon RPCs audited (3 clear, 1 optional `claim_invite` null-guard).
- **`eq/go-live-runbook.md`** written + committed — live-verified weekend runbook.

**Go-live gates (weekend) — see `eq/go-live-runbook.md` §B:**
- [ ] 🔴 **`EQ_SECRET_SALT` parity** Shell vs Service — silent #1 go/no-go, never compared
- [ ] Finish **Service domain cutover** (DNS/TLS, `NEXT_PUBLIC_SITE_URL`, Supabase URL allowlist); confirm Service prod project (`urjhmkhbgaxrofurpbgc` lists as "-dev")
- [ ] 🟠 **MFA-bypass posture** — PIN-only Shell → Service single-factor; accept or gate behind mandatory Shell-TOTP

**Deferred (spun off as post-launch tasks):**
- [ ] Unify cross-app PostHog distinct_id (Shell UUID / Field `tenant:handle` / Service id) — fixes the "refused to merge" warning + the inflated user count
- [ ] Fix EQ Field double `$pageview` capture (SPA logs ~80% of pageviews as `/`)
- [ ] Optional: add `auth.uid() IS NULL` guard to `eq_cards_claim_invite`

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
      promote it to a real CM-e
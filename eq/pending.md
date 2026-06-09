---
title: EQ Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-06-10
scope: EQ Solutions to-do list; overwrite in place
read_priority: critical
status: live
---

# EQ Tier — Pending

EQ Solutions work only. SKS items live in `sks/pending.md`. OPS items in `ops/pending.md`.

*Pruned 2026-06-10: stripped all-done session-close blocks and superseded May architecture sections. Full history in sessions archive.*

---

## ⚠ Immediate / Time-sensitive

- [ ] **⚠ Worker invites expire 2026-06-15** — 25 workers have pending invites. Remind field staff to check email and accept their EQ Shell invite.
- [ ] **2 workers with no staff match** — emma_curth@outlook.com, hexperfect@outlook.com. Create staff records in EQ Field or correct emails.
- [ ] **8 workers with no email** — populate email in eq-canonical `public.workers` to enable linking.
- [ ] **Delete `C:\Users\EQ\eq-credentials-ref.html`** after importing to password manager.

---

## Sprint 7 — EQ Service cutover follow-on

Schema + data migrated to ehow; env vars swapped; repo on `eq-solutions/eq-service`.

- [ ] **Smoke test (Royce)** — sign in via Shell OTP at service.eq.solutions, confirm checks/tests/defects visible, create a test check → lands in ehow tenant `7dee117c`. Shell SSO fixed 2026-06-09 (4 bugs, deploy 6a27f277).
- [ ] **Service SSO smoke** — fresh incognito → `core.eq.solutions` → Shell login → click Service → dashboard loads without login prompt.
- [ ] **PR #257** — merge to main (triggers deploy) once smoke test passes.
- [ ] **Post-verification (do NOT before smoke test):** redirect service.eq.solutions → core (5.2), revoke urjh service-role keys (5.4), decommission old Netlify site (5.3).
- [ ] **`canonical_field_id` gap** — all 37 SKS Service sites have `canonical_field_id = NULL`. Bridge from EQ Service sites to EQ Field dispatch not wired. Separate task, not blocking cutover.
- [ ] **Scheduler/route migration (4.4)** — `supervisor-digest` + `pre-visit-brief` schedulers depend on Next.js `/api/cron/*` routes in eq-service; needs route-hosting decision before moving to eq-shell.

---

## SKS Live — roles / security-groups track

Full plan + agent prompts (A–E): `sks-live-sprint-2026-06-07.md`. Live-verified 2026-06-07: `shell_control` has 9 groups / 16 perms / 0 user assignments; tenant `sks` = 3 × manager.

- [ ] **eq-roles** — merge PR #7 → tag `v2.3.0` (unblocks the eq-shell dep bump). *(Royce)*
- [ ] **eq-shell** — converge `c2-shell-roles` + `sks-field-host` into one trunk (Prompt A; Royce picks trunk).
- [ ] **eq-shell Phase 2** — wire group perms into the session as `extra_perms` via `resolveEffectivePermissions` (Prompt B).
- [ ] **eq-shell Phase 3** — `AdminSecurityGroups` page; first write moves `user_security_groups` off 0 rows (Prompt C).
- [ ] **eq-shell Phase 4** — walk ONE real SKS user end-to-end; first-ever `user_security_groups` row (Prompt D).
- [ ] **Phase 5 hardening** — `contact_customer_links` explicit `WITH CHECK` (`::uuid` cast) + CI policy-lint + eq-roles no-orphan-keys test (Prompt E).

---

## SKS Field go-live — remaining gates

- [ ] Functional click-through smoke on `core.eq.solutions/sks/field` (supervisor): **person edit + site edit + team create + team delete** → pipeline / import / resources / roster / safety against SKS data.
- [ ] Cutover **soak** 24–48h with standalone (`sks-nsw-labour`, v3.10.59) kept warm → then **retire** standalone.
- [ ] **Track 2 STEP 2 (anon lockdown)** — deferred until standalone retired. Then move `AUDIT_SB_KEY` → service_role and drop the `audit_log` anon-insert carve-out.
- [ ] **Onboarding** — invite-claim rollout (only 1 of 36 workers linked; 0/56 invites claimed). Upstream eq-shell #183/#175.

---

## Cross-app linkage follow-on

Full audit/plan: `cross-app-linkage-audit-2026-06-07.md`, `cross-app-linkage-sprint-2026-06-07.md`.

- [~] **P2 customer convergence** — Partial 2026-06-07 (38 stubs retired, 28 quotes linked). Remaining: decide SoR (rec `app_data.customers`); Tier A merge (26, supervised); Tier C (50 ambiguous) + quotes-side N:1 dedup via Intake; 99 dangling sites need source re-import.
- [ ] **P7a** SKS anon-remediation (`nspbmirochztcjijmcrx`) — exact policy worklist in plan §7a. **SKS-live, gated.**
- [ ] **P7b** `ktmj` anon-write policies — close via the pause/decommission already pending (after P4 bridge).
- [ ] **P7d** run `get_advisors` pass on EQ Service DB `urjhmkhbgaxrofurpbgc` (not yet audited; may be moot if Sprint 7 cutover completes + urjh decommissioned — confirm first).
- [ ] **WS1 remainder** — 481 ambiguous customers need human dedup via EQ Intake (Tier A 26 supervised + Tier C 50 ambiguous + quotes-side N:1).

---

## Go-live gates (uncleared from 2026-06-05 readiness check)

- [ ] 🔴 **`EQ_SECRET_SALT` parity** Shell vs Service — silent go/no-go, never compared. Check before launch.
- [ ] **Service domain cutover** — DNS/TLS, `NEXT_PUBLIC_SITE_URL`, Supabase URL allowlist; confirm Service prod project (`urjhmkhbgaxrofurpbgc` lists as "-dev"). *(Blocked on Sprint 7 smoke test passing first.)*
- [ ] 🟠 **MFA-bypass posture** — PIN-only Shell → Service single-factor; accept or gate behind mandatory Shell-TOTP.

**Deferred post-launch:**
- [ ] Unify cross-app PostHog distinct_id (Shell UUID / Field `tenant:handle` / Service id) — fixes inflated user count.
- [ ] Fix EQ Field double `$pageview` capture (SPA logs ~80% of pageviews as `/`).
- [ ] Optional: add `auth.uid() IS NULL` guard to `eq_cards_claim_invite`.

---

## EQ Design System — component build

Foundation shipped (One Spine, Stream A): `@eq-solutions/tokens` v1.0 + `@eq-solutions/ui` v1.0.1 = Button/Skeleton/Table. Full plan: `design-system-consolidation-2026-05-31.md`.

- [ ] **A7** eq-ui Modal + ConfirmDialog (fold in a11y A1/A2 from `quality-polish-backlog-2026-05-30.md`)
- [ ] **A8** eq-ui FormInput
- [ ] **A9** eq-ui StatusBadge + KindPill
- [ ] **A10** eq-ui Card + Toast + Tabs (resolve ghost-border → Option B)
- [ ] **A11** Font self-host in the shared package (supersedes per-app P5)
- [ ] Confirm pin-by-tag migration landed (eq-ui v1.0.1 / eq-roles tags); move `#main` consumers to `#vX`.
- [ ] Add 2 drift items to `quality-polish-backlog-2026-05-30.md`: Service emoji-in-Lucide (~7 files), Service `RouteProgress` cyan→indigo gradient.

---

## EQ Field

**Deploy-preview auth gate:** zaap anon-revoked; `demo-trades` previews 401s on name list. Use `?tenant=demo` to bypass for smoke. Pre-existing, deferred 2026-06-06.

**Deferred features:**
- [ ] Auto-fill labour-hire/apprentice timesheets from roster job pin (accounts reconciliation path — held deliberately).

**Tender Pipeline — SKS promotion (blocked):**
- [ ] Apply migrations 001 + 002 to SKS Supabase (`nspbmirochztcjijmcrx`).
- [ ] Remove pipeline tables from `TENANT_DISABLED_TABLES.sks` in `scripts/app-state.js`.
- [ ] Backfill `migrations/` on disk from `list_migrations` MCP.

**Tender Pipeline — demo open items:**
- [ ] Wire `clash_detected` PostHog event (reserved in `tender-pipeline.js`, not yet firing).
- [ ] Decide `pending_schedule` table fate — promote to CM-editable staging queue or drop, treat `schedule` as SoT.
- [ ] Lazy-load SheetJS if first-load bundle size becomes a problem (~250KB added).

**Phase 1 — Royce manual steps (on `claude/hopeful-wright-058c8b`, 5 commits past demo):**
- [ ] `feat_project_hours_v1` flag in EQ PostHog project (`phc_zXpRxm6Q…`), default off, targeted at Royce only first.
- [ ] Apply `migrations/2026-04-27_sites_track_hours.sql` to `ktmjmdzqrogauaevbktn` via Supabase MCP / Studio (review SQL first).
- [ ] Apply `migrations/2026-04-27_eq_role_enum_people_role.sql` to `ktmjmdzqrogauaevbktn` (verify pre-conditions in header first).

**Phase 2 — multi-tenancy foundation:** gated on customer trigger (first self-serve trial or ~3 customers manually provisioned). Do not start until then.

**Housekeeping:**
- [ ] Clear Supabase rate_limits table on demo branch (`ktmjmdzqrogauaevbktn`).
- [ ] Write fresh Cowork brief for EQ Field (guardrails, demo branch rules).
- [ ] Downgrade old EQ DB `ktmjmdzqrogauaevbktn` → free tier in Supabase dashboard, then pause it.

---

## EQ Service

- [ ] **Delta WO import — live dry-run** on SKS tenant with Aug 2025 file: confirm ~250 rows resolve, MVSWBD fuzzy prompt fires, LBS unknown-code prompt works, commit succeeds, re-upload triggers duplicate blocker.
- [ ] Full-repo file-header backfill (EQ-IP-Register P2 #7 scope A) — dedicated session.
- [ ] Continue sprint cadence (22 sprints to date, 80 Vitest tests).

---

## EQ Shell / EQ Intake — deferred architecture items

*The ⚠ SUPERSEDED block from earlier versions has been removed. Current reality is in `STATE.md`.*

**eq-demo-canonical security advisor (diagnosed 2026-05-19, not yet applied):**
- [ ] Apply migration 004 to `eq-demo-canonical` — `C:\Projects\eq-intake\sql\004_security_advisor_fix.sql` (grants EXECUTE to `authenticated`). Paste into Supabase SQL editor and Run.
- [ ] Toggle HaveIBeenPwned protection in eq-canonical (`jvknxcmbtrfnxfrwfimn`) dashboard → Auth → Settings.
- [ ] Commit + push two eq-intake edits — `sql/004_security_advisor_fix.sql` and `eq-platform/scripts/db-apply.ts` are uncommitted in `C:\Projects\eq-intake`.
- [ ] Smoke-test intake commit after applying 004.
- [ ] Decide server-side commit RPC migration — 4 remaining `authenticated_security_definer` warnings clear only if commit moves to a Netlify Function (service-role). Deferred until `sks-canonical-eq` provisioned with real users.

**sks-canonical-eq provisioning (gated, not started):**
- [ ] Provision `sks-canonical-eq` Supabase project (Sydney / `ap-southeast-2`).
- [ ] Run `pnpm db:apply` from `eq-platform/` to regenerate `all-migrations.sql` with 004 bundled.
- [ ] Paste `all-migrations.sql` into the new project's SQL editor.
- [ ] Add Royce as the first user with `user_metadata.tenant_id` set to the SKS tenant uuid.
- [ ] Drop SKS credentials into the Netlify env vars for the production shell deployment.

**Deferred architecture critique items** (don't ship until Phase 2 resumes):
- [ ] Dual-salt rotation support for `EQ_SECRET_SALT`.
- [ ] Dual-secret support in `verify-shell-session` for `SUPABASE_JWT_SECRET` rotation.
- [ ] `revoked_sessions` table + shorten JWT TTL from 1 hour to ~30 minutes.
- [ ] Schema split — `shell_control.*` vs `app_data.*` (free now, saves ~3 weeks when regional secondary needed).
- [ ] Per-domain RPC decomposition — split `eq_intake_commit_batch` before 5 module branches accumulate.
- [ ] Canonical → Field one-way sync rule documented + enforced with a Supabase trigger.
- [ ] Token-mint audit log (tenant_id, IP, timestamp) with Sentry threshold alert.
- [ ] Build-time hash check for vendored `@eq/*` packages.
- [ ] Iframe retirement deadline decision — strategic call Royce makes when Phase 2 resumes.

---

## EQ Cards

*(Section was truncated in prior file — restore from sessions/2026-05-21.md in archive if needed.)*

---

## CRITICAL — Rotate GitHub PATs

Discovered 2026-05-19: `system/infrastructure.md` tracked literal PAT values in plaintext. Treat all 3 as compromised.

- [ ] **Revoke all 3 PATs** — GitHub Settings → Developer settings → Personal access tokens. Labels: "EQ Solutions", "Milmlow", "Milmlow alt".
- [ ] **Issue one new fine-grained PAT** to replace EQ Solutions.
- [ ] Update `C:\Projects\.git-credentials.eq-solutions` and `C:\Projects\.git-credentials` on Beelink.
- [ ] **Substrate hardening** — add `gitleaks` (or similar) pre-commit hook on eq-context repo.

---

## Royce manual actions (consolidated)

Recurring items that need Royce to act, not Claude:

- [ ] `TENANT_ORG_UUID` Netlify env var for eq-solves-field EQ site (blocks U6 PIN).
- [ ] Revoke old `gho_...` PAT at github.com/settings/tokens.
- [ ] Drift CI secrets in eq-shell GitHub repo settings.
- [ ] HaveIBeenPwned toggle in eq-canonical (`jvknxcmbtrfnxfrwfimn`) Supabase Auth settings.
- [ ] eq-context sks/ local edits still uncommitted (`sks/README.md`, `sks/products.md`) — commit via GitHub web UI or emit .bat.

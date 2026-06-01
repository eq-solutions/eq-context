---
title: Autonomous Sprint — Board
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Full sprint backlog + ownership/claims across all EQ streams; the coordination contract
read_priority: critical
status: live
---

# Autonomous Sprint — BOARD (single source of truth for who's doing what)

**Read [`AUTONOMOUS-SPRINT-RULES.md`](AUTONOMOUS-SPRINT-RULES.md) first, then [`STATE.md`](STATE.md).**
**Claim an item before starting:** set its `owner` + `branch` + status to 🔵 in-progress. Don't start an item whose repo+files are already claimed.

Legend: ✅ done · 🔵 in-progress (claimed) · ⚪ todo (unclaimed) · ⛔ Royce-gated · ⏸ paused
Last refreshed: 2026-05-31.

## 🎯 SPRINT 3 — Next big sprint (priority cut, 2026-05-31)
Consolidates **every** outstanding finding from the 2026-05-31 deep-dive + cross-app audit + canonical/worker-creds design. Detail in the streams below; this is the sequencing. Owners per the carve-out (C4 = eq-shell src+auth; C-CANON = data-plane; Cards/Field/Service consoles per repo). ⛔ = Royce-gated.

**P0 — live security (first):**
- **I1** ⛔ plaintext access codes in client JS — Field (`2026`) + SKS Labour (`SKSNSW`) → move server-side *(SKS Labour = SKS-live)*
- **I2** ⛔ RLS holes — Quotes (off) + SKS Labour (9 permissive/disabled tables) → lock down
- **F1** ⛔ rotate exposed `ehowg` service_role key (you rotate → I propagate)

**P1 — security + correctness (eq-shell, C4):**
- **B2** ~15 ad-hoc role checks → `can()` · **B4** consolidate 5 `verify*Token` → one · **B11** `ai-briefing` cache + typed session + drop `?? ''`
- **I3** port `friendlyError` to the other 4 apps · **I4** ⛔ fix Quotes broken expiry-cron (prod)

**P1 — worker-creds Phase 1 (Stream G, ⛔ gated on your inputs):** G1 schema+worker_id+phone-claim · G3 SKS seed via Intake · G4 Cards reminders · G2 Cards gateway → worker-house

**P2 — invisible-tech / design (C4 + design consoles):**
- **B8** gm-reports silent failures (redo — branch reverted) · **B5** tokenize gm-reports · **B6** dedup buttons → `<Button>` · **B9** App.css de-sprawl
- **A7–A12** eq-ui components + font self-host · **I5** gradients/shadows sweep + SKS Labour DM Sans → Plus Jakarta

**P2 — structural (roles):** C5 split `@eq-solutions/roles` → C7 Field adopt · C6 Service matrix · C8 Shell mirror reconcile (absorbs **B12**)

**P3 — housekeeping:** B10 ⛔ delete dead stubs (your permission) · Stream D asset-intake (in-flight) · migrate the 4 held plans → eq-context, then prune

> **✅ SPRINT 1 + SPRINT 2 (Waves 1–2) COMPLETE — 2026-05-30.** Sprint 2 detail + all merged Wave-1/2 PRs are in [`SPRINT-2-BOARD.md`](SPRINT-2-BOARD.md); current per-repo reality is the [`STATE.md`](STATE.md) POST-SPRINT block. **Held for Royce:** 3 dormant-feature migrations (licence-expiry, timesheet-approval, audit-log-UI) + B4 canonical wiring + ⛔ C4 auth cutover + **B5 SKS-live cutover (LAST)**. The Sprint-1 fan-out record below is retained for history.
>
> **🧭 CONVERGENCE DIRECTIVE (2026-05-31, Royce) — collapse parallel consoles to ONE driver.**
> Multiple consoles diverged onto the same roles/canonical/design questions today (see the four
> `*-2026-05-31*` analysis files in eq-context). Royce's call: **C4 (the eq-shell review/hardening
> console) is the SOLE DRIVER from here.** Every other console: **commit your WIP to its branch and
> STOP** — do not start new items. Resume only when C4 hands an item back on the board.
>
> **RESOLVED BLOCKER — roles package shape (Royce 2026-05-31):** `@eq-solutions/roles` is currently
> Shell-shaped (its permission *matrix* IS Shell's, lifted verbatim — see `field-roles-findings-2026-05-31.md`).
> Decision = **SPLIT the package into (a) shared tier-list + `is_platform_admin` convention, and
> (b) per-app permission matrices.** This unblocks Field + Service adoption AND legitimises the
> Shell server-side mirror (below). All roles work sequences behind this split (rows C5–C8).
>
> **eq-shell ALREADY SHIPPED this session (fold into the record):**
> - **PR #79 MERGED → main (`9905be5`), live + smoke-verified (401):** intake-commit server-authz
>   (was wide open), 3 UI button/token bugs, `friendlyError` (no raw Supabase errors to users),
>   `docs/cross-app-audit.md`. ⚠️ Introduced `netlify/functions/_shared/permissions.ts` which
>   **re-defines the role matrix** (verified identical to `@eq-solutions/roles`) — a Rule §5
>   "don't re-define the matrix" divergence, justified (can't import across the tsconfig boundary)
>   but to be **reconciled by the package split** (C8). PR #78 (canonical reconciliation) also merged.
> - **PR #80 OPEN, MERGEABLE — ⛔ auth-gated (Rule §1):** B1 TS `strict` (0 fallout) + B3 TOTP
>   rate-limit. Awaiting Royce review+deploy.
>
> **🔀 SANCTIONED PARALLEL — ONE canonical-layer console (Royce 2026-05-31).** The DB/data-plane
> track (Part D / Stream F below) runs as the SINGLE exception to "C4 sole driver," because its
> file domain is disjoint from C4's. **Strict carve-out — neither console crosses the line:**
>
> | Path / surface | Owner |
> |---|---|
> | `supabase/**` (migrations, tenant-migrations, staged), `scripts/*.mjs` (migrate-tenants, check-tenant-drift, provision-tenant, re-encrypt), `netlify/functions/_shared/encryption.ts` + `tenant-routing.ts`, `canonical-api.ts`, Supabase MCP (all 3 projects) | **C-CANON** (canonical console) |
> | `src/**`, `netlify/functions/_shared/{permissions,token,supabase-jwt,cookie}.ts`, auth fns (`shell-login`, `challenge-totp`, `mint-*`, `intake-commit`), `tsconfig*.json`, CSS/design | **C4** |
> | `_shared/supabase.ts` (service client — read by both, rarely edited) | **coordinate** — edit only with a board note |
>
> C-CANON works on its own branch off updated `main`, commits incrementally, **deploys/pushes-to-main NOTHING without Royce** (same gates). Its live-SKS + staged items stay ⛔. If it needs a file in C4's column (or vice-versa), STOP and coordinate on the board — do not cross.
>
> **🟦 ACTIVE FAN-OUT (Code session, 2026-05-30) — "everything then cutover last".** Royce authorized full fan-out. **Wave 1 RESULTS:** A4 Cards ✅ **merged** (Milmlow/eq-cards#10); A5b `@eq-solutions/ui` ✅ **created** (public github.com/eq-solutions/eq-ui — Button done, token-only; Skeleton+Table building now); C2 Shell→roles ✅ **MERGED** (#70, Royce-approved — exhaustive 5×15 permission-equivalence, auth/session untouched). **Wave 2 PROGRESS:** ✅ B2c teams merged (Field v3.5.27); ✅ Service wiring merged (#205); ✅ Shell wiring merged (#71 — ice headers, Royce-approved). **🎨 DESIGN PILLAR COMPLETE** — tokens + `@eq-solutions/ui` (Button/Skeleton/Table) across Shell/Field/Service/Cards (Shell Button-as-React = minor follow-up). **🧩 B2 MODULE PORTS COMPLETE** — B2b safety + B2c teams + B2d pipeline all merged to Field main (v3.5.28), tenant-gated to sks, EQ-safe (review caught/fixed the dup-ID issues). The Field+SKS **codebase** merge is done bar cutover. ✅ **C3 auth spike done** ([#72](https://github.com/eq-solutions/eq-shell/pull/72) — verified **live-auth-untouched** (zero diff on session.ts/functions/LoginPage), additive `src/spike/`, builds clean. **No-deploy spike for reference — NOT for merge.** Supabase-side setup (WebAuthn, tenant_members, Custom-Access-Token-Hook w/ exception guard, RLS) documented for Royce to apply). ✅ **B3 reconcile analysis done** (`field-reconcile-b3-2026-05-30.md` — 15 ranked carry-forward fixes: 11 low-risk/additive, 3 medium, 1 high-risk (live-EQ DB migration), 8 must-not-port). ✅ **B3-apply MERGED** (#141 — Field **v3.5.29**, 10 reconcile fixes incl. SW auto-reload + TAFE-40h). **🏁 NON-CUTOVER BACKLOG COMPLETE.** 🧹 **Tidy-up done:** 108 old **merged** branches closed across eq-field/shell/service/cards (unmerged/open + c3 reference kept); Field worktree removed + clone back on main; STATE.md refreshed. **Follow-up wave IN FLIGHT (Royce-selected):** 🔵 B3 #11 home.js + #5 approval-chips (one Field PR, `claude/b3-followup-home-approval`, v3.5.30; #5 schema-gated → graceful-degrade if EQ lacks `approved` cols, NO migration); 🔵 Shell Button → eq-ui Button (`claude/eq-ui-shell-button`, isolated worktree `eq-shell-button-wt`, visible-change review). **HELD for cutover (Royce 2026-05-30):** B4 canonical wiring + B3 #13 audit-revert (needs live-EQ DB migration). **Deferred:** E1 Cards worker-first rebuild. ⛔ C4 auth cutover. **B5 cutover = LAST** (SKS-live, Royce-trigger). **Remaining (cutover-phase / gated):** B3-apply (Royce-reviewed), B4 canonical wiring (do with cutover), ⛔ C4 auth cutover, **B5 cutover = LAST (SKS-live, Royce-trigger)**. Don't grab these items.

---

## Stream A — Design / tokens
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| A1 | Shell consume @eq-solutions/tokens | eq-shell | ✅ | #66 merged | live |
| A2 | Field tokens + Plus Jakarta Sans + drift-guard | eq-solves-field | ✅ | #136 merged | live |
| A3 | Service de-vendor + 0097 cleanup | eq-solves-service | ✅ | #203, #204 merged | live |
| A4 | Cards token consolidation | eq-cards | ✅ | **merged Milmlow/eq-cards#10** | Path A: deleted dead `EqSpacingTokens`/`EqTypographyTokens` (0 callsites), barrel-export `EqSpacing`; spacing values identical, `dart analyze` clean. Typography deferred (values diverge). |
| A5 | Component audit doc (→ future @eq-solutions/ui) | eq-shell + eq-solves-service | ⚪ | — | read-only research; rank duplicated buttons/tables/forms |
| A6 | Field `base.css` legacy vars → `--eq-*` | eq-solves-field | ✅ | **merged #137 → main (v3.5.26)** | bridged with `var()` fallbacks → zero visual change. Live. |
| A7 | eq-ui: Modal + ConfirmDialog (incl. a11y A1/A2) | eq-ui + consumers | ✅ | eq-ui v1.1.0 PR #1 | Modal+ConfirmDialog in 9-component contract; focus-trap, role=dialog, scroll-lock |
| A8 | eq-ui: FormInput | eq-ui + consumers | ✅ | eq-ui v1.1.0 PR #1; eq-shell D5.1 #95; eq-service D5.2 #212 | FormInput with label/error/hint; 29 Service callsites |
| A9 | eq-ui: StatusBadge + KindPill | eq-ui + consumers | ✅ | eq-ui v1.1.0 PR #1 | Shipped in kit; domain model mismatch in Shell/Service → local patterns kept |
| A10 | eq-ui: Card + Toast + Tabs | eq-ui + consumers | ✅ | eq-ui v1.1.0 PR #1 | All three in kit; ghost-border Option B resolved in v1.1.1 (hover border) |
| A11 | Font self-host in shared layer | eq-design-tokens | ⚪ | — | deferred; P5 Shell fixed (removed render-blocking import in #116) |
| A12 | Claude Design context bundle | eq-context + eq-design-tokens | ✅ | this session | `eq/design/claude-design-context.md` created + issued to Claude Design 2026-05-31 |

## Stream B — EQ Field + SKS merge (codebase only; data stays separate)
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| B0 | Re-scope + staleness audit | — | ✅ | this session | EQ Field already multi-tenant w/ SKS support; config NOT stale → merge = port modules + cutover |
| B1 | Tenant-safety groundwork | eq-solves-field | ✅ | (pre-existing) | branding/detection/disabled-tables already in EQ Field |
| B2a | ~~Port `project-hours.js`~~ → **resolved: NO PORT** | eq-solves-field | ✅ | this session (verified) | **Ground-truth 2026-05-30:** dead in BOTH — unwired orphan in SKS (no live `<script>`/precache; only a comment ref) AND EQ **deliberately deleted** the file at v3.5.11 (dead-code audit). Re-adding = re-introducing removed dead code → not done. Perms/flag/history already at parity, so cutover loses nothing. **Royce 2026-05-30: leave dead** — no revival. |
| B2b | Port `safety.js` + `safety-dashboard.js` | eq-solves-field | ✅ | **merged #138 → main (v3.5.26)** | Ported tenant-gated to `sks`; triple-gated → **EQ provably unaffected** (verified: no dup IDs, sks-only reveal, disabled-tables). Review caught + fixed a dup-ID defect (safety list IDs collided with EQ site-reports). **Cutover TODOs (B5):** (1) safety form modals not transplanted — safety.js refs EQ's `#modal-prestart`/`#prestart-form-body` etc.; SKS needs own namespaced modals or reconcile; (2) `toolbox_talks` may need adding to `ORG_TABLES` if it has `org_id`; (3) SKS path unsmoked — validate at cutover; (4) safety list IDs namespaced `#safety-prestart-list/-toolbox-list` (diverges from SKS safety.js). |
| B2c | Port `teams.js` | eq-solves-field | ⚪ | — | **Verified LIVE in SKS** (boot tag ln 64, precached): 446ln. **Coupled** into roster/contacts/schedule — reconcile carefully. Boot-load → lazy. |
| B2d | Port `pipeline*` (×3) | eq-solves-field | ⚪ | — | **Verified LIVE in SKS** (boot tags ln 85-87, precached): import 376 + pipeline 583 + resource 1480 = 2439ln. `SKS_PIPELINE` ns. Needs local `xlsx.full.min.js` (SKS CSP blocks CDN). Boot → lazy. Do LAST (SKS `pipeline-ui` worktree recently active). |
| B3 | Reconcile SKS 11-release delta | eq-solves-field | ⚪ | — | fixes SKS has that EQ lacks |
| B4 | Light canonical wiring → `sks-canonical` | eq-solves-field | ⚪ | — | control-plane reads only; no operational migration |
| B5 | **CUTOVER** repoint sks-nsw-labour.netlify.app | infra | ⛔ | — | **ROYCE-GATED — touches SKS live. Do not run.** |

> **Module-state ground-truth (verified 2026-05-30, read-only).** The recon premise "SKS-only modules are live in SKS → port them" holds for B2b/B2c/B2d (all are live boot-loaded `<script>` tags + precached in SKS) but was **wrong for B2a** (project-hours is a dead orphan in *both* repos). **Lesson for the next agent:** verify a module is actually *wired* in SKS (live tag / precache / nav) before porting — don't trust the file's mere existence. **Structural note:** SKS loads all modules at boot; EQ Field uses a lazy-loader (v3.5.21+). Every B2 port must convert SKS boot-load → EQ lazy-manifest, not just copy the file + tag.
>
> **✅ RESOLVED 2026-05-30 — project-hours stays dead.** Royce chose *"leave it dead"*: B2a is closed as a no-op and the burn-down panel will **not** be revived or carried into the merge. The residual `ph.*` perms + `feat_project_hours_v1` flag default + `sites.track_hours` column are harmless and may stay (or be swept in a future dead-code pass). No further action.

## Stream C — Auth re-platform
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| C1 | Role registry `@eq-solutions/roles` | eq-roles (new) | ✅ | **pushed: eq-solutions/eq-roles (public)** | built + verified; matrix matches Shell |
| C1b | Create public `eq-roles` repo + push | eq-roles | ✅ | Royce-approved 2026-05-30 | live at github.com/eq-solutions/eq-roles (main) |
| C2 | Wire Shell to consume @eq-solutions/roles | eq-shell | ✅ | **merged #70 → main** (Royce-approved) | Swapped hand-defined `EqRole`+admin/audit MATRIX → `@eq-solutions/roles`; module matrices stay local. **Exhaustive 5×15 permission-equivalence (all IDENTICAL)**, build clean, auth/session untouched. Live on core hub. |
| C3 | Supabase-Auth IdP + passkey spike | eq-shell | ⚪ | — | spike branch; no prod auth change |
| C4 | Staged auth cutover (shadow → app-by-app → retire HMAC) | all | ⛔ | — | **auth deploy = Royce-gated (Rule §1)** |
| C5 | **Split `@eq-solutions/roles`: tier-list + convention ⟂ per-app matrices** | eq-roles | 🔵 | C4 / TBD branch | **DECIDED 2026-05-31 (Royce).** Blocks C6/C7/C8. Package exports: shared `EqRole`+`is_platform_admin`+`can(matrix,…)` helper shape; each app supplies its own matrix. Tag a new MAJOR (consumers pin by tag, not #main — coordinate w/ the tag-migration session). NOT started — design first. |
| C6 | Service role-mapping proposal (read-only) | eq-solves-service | 🔵 | C4 | **Reframed by C5:** not a role→role remap — canonical has NO service/CMMS perms, so Service needs its own matrix module under the split. Earlier fan-out got Service↔canonical backwards (`roles-canonical-audit` §C) — proposal must be source-verified. Output = decision input, implement nothing. Sequence AFTER C5 shape is known. |
| C7 | Field roles adoption (tier-list only) | eq-solves-field | ⚪ | (C4, queued) | Tier names already match; adopt shared tier-list from C5, keep Field's own matrix. Real work = auth-gated `verify-pin.js` token-fidelity fix (`field-roles-findings-2026-05-31.md`) → ⛔ Rule §1. Decisions: `regional_manager` placement, does Field need `is_platform_admin`. |
| C8 | Reconcile Shell server-mirror onto split package | eq-shell | ⚪ | (C4, queued) | Replace the hand-mirrored MATRIX in `netlify/functions/_shared/permissions.ts` (PR #79) with a consume-by-tag of the C5 shared shape, resolving the Rule §5 divergence. |

## Stream D — Equipment / asset intake (in flight from other sessions)
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| D1 | QR labels + asset hierarchy | eq-shell | 🔵 | `claude/equipment-qr-hierarchy` (#69) | mergeable; sequence vs #64 `TenantHome` conflict |
| D2 | AI enrichment / dup-detect / site-match / photo / PDF | eq-intake | 🔵 | `claude/clever-roentgen-3a3688` | then **re-vendor into eq-shell** (Rule §4) |
| D3 | Bridge canonical assets → EQ Service maintenance | eq-solves-service | 🔵 (dormant) | `claude/charming-dirac-72bcb0` | **canonical_id back-ref migration must be a TIMESTAMP, not `0110`** (taken). Build type-clean, not pushed. |

## Stream E — Cards / canonical / PPM
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| E1 | Cards Flutter worker-first rebuild | eq-cards | ⚪ | — | old profiles/licences → worker-first; fold in A4 token fix. NOT SKS. |
| E2 | PPM canonical realignment | (canonical) | ⏸ | — | **paused** — canonical PPM model misaligned with SKS ACB/NSX breaker workflow; revisit before rebuilding any PPM dashboard |
| E3 | eq-service observability keys (PostHog/Sentry) | eq-solves-service | ⛔ | — | Royce's task (Netlify env vars) |

---

## Stream F — Canonical layer (DB / data-plane) · owner C-CANON (sanctioned parallel)
Part D of the eq-shell hardening roadmap. PR #78 reconciliation already MERGED + LIVE (`f78e428`).
Verify every claim live via Supabase MCP — never trust docs over the DB. Detail: memory
`canonical-layer-reconciliation` + `docs/FINAL-SPRINT.md`.

| id | item | repo / surface | status | notes |
|----|------|----------------|--------|-------|
| F1 | **Rotate exposed `ehowg` service_role key** | Supabase + Shell + Fly | ⛔🔵 | **P1 SECURITY.** Royce rotates in the dashboard FIRST; then propagate the new key to 3 consumers: (1) re-encrypt into `shell_control.tenant_routing` (ehowg row) under `TENANT_ROUTING_MASTER_KEY` — author a one-off script per `_shared/encryption.ts` + `provision-tenant.mjs`, Royce runs it; (2) `eq-quotes-sks` Fly secret `CANONICAL_SUPABASE_KEY`; (3) any other ehowg service-role consumer. **Never echo/commit the key.** Build the script; Royce executes. |
| F2 | gm/briefing `tenant_id` reshape (expand+contract) | `supabase/staged/sks_gm_briefing_reshape_*` | ⛔ | Deploy-coupled with `upload-gm-report.ts` onConflict change. Parity, not security. Royce-gated. |
| F3 | SKS safety-RPC hardening | `supabase/staged/sks_safety_rpc_hardening.sql` | ⛔ | `approve/submit_safety_record` trust caller-supplied `p_tenant_id`. Apply when SKS goes multi-tenant or the Field caller is confirmed. |
| F4 | SKS Service CMMS reconcile | `scripts/check-tenant-drift.mjs` → SQL | ⛔ | Run drift gate first for the work-list (older `ppm_*` path vs branch 0020/0021). |
| F5 | Track B — Quotes → canonical-api + retire `sks_*` silo + `shell_control.eq_intake_*` retirement | eq-quotes + Shell | ⛔ | **WOULD BREAK LIVE QUOTES** — needs the staged cutover. Ties to the eq-quotes console chip. LAST. |

## Stream G — Worker-owned credentials (EQ Cards · worker-house) · DESIGN DONE 2026-05-31
Model + decisions: [`eq/identity/worker-credentials-model-2026-05-31.md`](eq/identity/worker-credentials-model-2026-05-31.md).
Worker data lives in the **worker-house** (`eq-canonical-internal` `worker_*`), worker-keyed, first-class `worker_id`.
**Supersedes the Cards-rewire per-business-tenant assumption — do NOT flip Cards `gateway` until G2 lands.**
Phase 1 = seed + self-maintenance (build now, pending Royce inputs); Phase 2 = snapshot + live-link + grant (deferred to business #2).

| id | item | repo / surface | status | notes |
|----|------|----------------|--------|-------|
| G0 | Model + 5 locked decisions | eq-context | ✅ | this session; reconciled w/ IDENTITY-MODEL §3.2/§11.2 + Cards PR #12 |
| G1 | `worker_*` schema + first-class `worker_id` + phone-keyed claim | eq-canonical-internal (C-CANON) | ⛔⚪ | Phase 1. Needs phone list. Timestamped migration. |
| G2 | Cards `gateway`/live-link → worker-house (not business DB) | eq-shell `cards-api.ts` + eq-cards | ⛔⚪ | Reconcile PR #12. **Don't flip transport until done.** |
| G3 | SKS 60-worker seed via Intake (= verification event) | eq-intake | ⛔⚪ | Phase 1. Per-credential trust tier from evidence found. Needs evidence export. |
| G4 | Cards self-maintenance + **renewal reminder engine (live at launch)** | eq-cards | ⛔⚪ | Phase 1. Non-negotiable: stale seeded data is a liability. Folds in E1. |
| G5 | Phase 2 — snapshot + live-link + grant/revoke + cross-tenant trust | canonical + Cards + Shell | ⏸ | Deferred until business #2 needs an SKS-verified worker. |

> **Royce-gated inputs (block G1–G4, not the design):** evidence export (scans+numbers+expiries ×60), phone numbers ×60, auth-hook GATE A, `sks-canonical` security lock (F1-adjacent). See the model doc's "Royce-gated inputs".
> **Ownership:** G1/G3 = data-plane (C-CANON carve-out); G2 spans C4 + Cards; G4 = Cards. Coordinate per the carve-out table. **E1 (Stream E) now feeds G4.**

## Stream H — eq-shell hardening backlog (2026-05-31 deep-dive) · owner C4
Roadmap: `~/.claude/plans/distributed-dazzling-curry.md` + memory `eq-hardening-roadmap`. **Shipped this session:** A1–A3 (#79), B1+B3 (#80), B7 (#81). Remaining:

| id | item | bar | size | status | notes |
|----|------|-----|------|--------|-------|
| B2 | retrofit ~15 ad-hoc role checks → `can()`/`requirePerm` | 🔒 | M | ✅ | PR #120 merged — `useCan('admin.list_users')` + security groups PR #123 |
| B4 | consolidate 5 `verify*Token` fns → `verifyToken(kind)` | 🔒 | S | ⚪ | still open |
| B5 | tokenize `gm-reports/index.tsx` (~118 inline → classes/tokens) | 🎨 | M | ⚪ | still open |
| B6 | delete dup `.eq-btn-*`; migrate call-sites → `<Button>` | 🎨 | S | ✅ | PR #120 — removed `.eq-btn-*` CSS classes; PR #116 ComingSoon fixed |
| B8 | surface gm-reports silent archive/delete + detail-load failures | ✅ | S | ⚪ | still open (branch reverted — redo) |
| B9 | ~800 lines page CSS out of App.css → co-located + tokenize | 🎨 | M | ⚪ | still open |
| B10 | delete dead `modules/cards.tsx` + `modules/service.tsx` stubs | ✅ | S | ✅ | PR #120 merged — stubs deleted |
| B11 | `ai-briefing` Cache-Control private + typed `entity-actions` + drop `?? ''` | 🔒 | S | ⚪ | still open |
| B12 | single-source the permission matrix (client+server) | 🔒 | M | ✅ | PR #108 merged — `check-perm-sync.mjs` reads `@eq-solutions/roles` directly; C8 reconcile (permissions.ts) still open |

## Stream I — cross-app remediation (`eq-shell/docs/cross-app-audit.md`) · per-repo, gated
11 agents, adversarially verified, across Field/Cards/Service/Quotes/SKS-Labour. None fully canonical-conformant.

| id | item | apps | bar | status | notes |
|----|------|------|-----|--------|-------|
| I1 | plaintext access codes in client JS | Field (`2026`), SKS Labour (`SKSNSW`) | 🔒 | ⛔ | **P0.** Move server-side. SKS Labour = SKS-live. |
| I2 | permissive/disabled RLS | SKS Labour (9 tables), Quotes (off) | 🔒 | ⛔ | **P0.** Per-tenant scoped keys + RLS on. |
| I3 | raw backend errors → users | all 5 | 👻🔒 | ⚪ | port the `friendlyError` pattern |
| I4 | expiry-cron broken in prod | Quotes | ✅ | ⛔ | ties to Quotes console chip + F5 |
| I5 | gradients/shadows + non-brand font | all (+ SKS Labour DM Sans) | 🎨 | ⚪ | brand sweep → Plus Jakarta, no gradients/shadows |
| I6 | OTP sessions lack `app_metadata.tenant_id` | Cards | 🔒 | ⛔ | **reframed by Stream G** (Cards → worker-house); auth-hook GATE A |

> **Refuted (don't chase):** Field `salt info.txt` "committed secret" — untracked + gitignored, never committed (verify caught it).
> **3 remediation chips already in separate consoles** (SKS Labour / Cards / Quotes) — fold their results into this stream.

## Migration-number ledger (timestamp from now on — see Rule §3)
- `eq-solves-service`: `0110` taken (`0110_performance_level_hf.sql`). All new migrations → `YYYYMMDDHHMMSS_*`.

## How to update this board
Edit the row you own as status changes. When done, set ✅ + the merged PR. Keep "Last refreshed" current. This file + RULES + STATE are the contract — if reality and the board disagree, fix the board.

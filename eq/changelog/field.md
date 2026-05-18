---
title: Changelog — EQ Solves Field
owner: Royce Milmlow
last_updated: 2026-05-19
scope: Append-only history of changes to the EQ Solves Field product
read_priority: reference
status: live
---

# Changelog — EQ Solves Field

## [2026-05-18 overnight] Phase 1.B wire-up + docs hygiene + Phase 2 spike
**Built by:** Claude (autonomous overnight run, Royce reviews in the morning)
**Brief:** "EQ Shell" overnight prompt — Phase 1.B + docs hygiene + Phase 2 spike, open PRs only, NEVER merge.
**Branches:**
- `claude/phase-1-b-wire-up` on `eq-solutions/eq-shell` → [PR #1](https://github.com/eq-solutions/eq-shell/pull/1)
- `claude/audit-doc-hygiene-2026-05-18` on `Milmlow/eq-field-app` → [PR #107](https://github.com/Milmlow/eq-field-app/pull/107)
- `claude/phase-2-spike-tender-pipeline` on `eq-solutions/eq-shell` → [PR #2](https://github.com/eq-solutions/eq-shell/pull/2)
**Companion changes (no new infra; uses Phase 1.A's provisioned resources):**
- Supabase migration `2026_05_18_phase_1b_pin_hash_and_service_role_policies` applied to `eq-shell-control` (`hxwitoveffxhcgjvubbd`): adds `users.pin_hash TEXT`, plus service-role-only ALL policies on `tenants` / `users` / `module_entitlements`. HONEST CAVEAT in migration header — not the long-term `auth.uid()` shape; precedent set in `2026-05-13_roster_presence_rls_tighten.sql` + `2026-05-18_tender_rls_tighten.sql`.

**Changes:**
- **Phase 1.B wire-up (PR #1 on eq-shell):** Three TS Netlify functions — `shell-login` (POST email + bcrypt PIN → sets `eq_shell_session` cookie on `.eq.solutions`, signed with shared `EQ_SECRET_SALT`), `verify-shell-session` (GET → hydrates user/tenant/entitlements; 401 on invalid; rejects if cookie tenant_id no longer matches canonical), `mint-iframe-token` (POST → 60s shell-token in the exact shape Phase 1.C's `verifyShellToken` expects). React Router shell: `SessionProvider` hydrates on mount, `RequireSession` guards `/:tenantSlug/*`, `ModuleGate` enforces entitlements per route. `BrandProvider` writes tenant `brand_color` to `--eq-brand` CSS custom property (Q6 lock). `FieldIframe` POSTs to `mint-iframe-token` and embeds `https://eq-solves-field.netlify.app/#sh=<token>`. Cards / Intake / Quotes / Service / Tender Pipeline ship as separate lazy chunks per Q5 (vite build verified). Shared HMAC helpers + lazy service-role Supabase client in `netlify/functions/_shared/`. **Do NOT auto-merge** — auth surface change.
- **Docs hygiene (PR #107 on eq-field-app):** AUDIT-REVIEW.md — moved FINDING #S1 + FINDING #S2 from open to closed with full per-PR breakdowns (PRs #89/#91/#92/#95 for the four phases / three workstreams), added new "Session — 2026-05-18 → 2026-05-19" iteration log entry covering Phase A+B+C+D + EQ Shell pivot + 1.A/1.B/1.C work. SPRINT-PLAN.md — ticked the four "Order to tackle" workstreams as shipped (S1/U2/SEC2/S2), updated U2 + S2 status blocks, added new "EQ Shell" section pointing at `EQ-SHELL-DESIGN.md`. DEMO-VS-LIVE.md — refreshed deploy-snapshot table to HEAD `7249833` post-PR #104, added v3.5.7 → v3.5.9 / EQ Shell Phase 1.C section. ~157 lines net; within auto-merge bar but left open per the brief.
- **Phase 2 spike (PR #2 on eq-shell):** 5 placeholder routes under `/<tenant>/tender-pipeline/{import|kanban|review|enrichment|curve}`, each a `React.lazy()` chunk. Each stub documents the vanilla source line range in `scripts/tender-pipeline.js` (import: 276-540, kanban: 542-750, enrichment: 752-961, review: 963-1455, curve: 1457-1900) + the deps to use during the proper migration. Added Phase 2 stack deps: `@dnd-kit/core`, `@dnd-kit/sortable`, `@tanstack/react-table`, `react-hook-form`. Branched off `main` (NOT off Phase 1.B) so the two PRs are reviewable independently.

**Decisions punted to Royce (morning):**
1. **Netlify env vars on the `eq-shell` project** — must set before functions run: `EQ_SECRET_SALT` (SAME value as eq-solves-field; HMAC handshake breaks if different), `SUPABASE_URL` (`https://hxwitoveffxhcgjvubbd.supabase.co`), `SUPABASE_SERVICE_ROLE_KEY` (from Supabase dashboard — service-role key not readable via MCP).
2. **Netlify ↔ GitHub link on `eq-shell`** — project provisioned empty in Phase 1.A, still not connected. Royce wires after reviewing PR #1.
3. **Logout endpoint on eq-shell** — Phase 1.B's logout button just navigates to `/`; the HttpOnly cookie expires in 7d. Adding `shell-logout` that sends `Set-Cookie: ...; Max-Age=0` is a small follow-up.
4. **Rate limiting on `shell-login`** — same gap eq-solves-field's verify-pin had pre-SEC2 (PR #99). Extend the same `rate_limit_buckets` RPC pattern to this surface in a follow-up.

**Deferred / out-of-scope:**
- DNS for `*.eq.solutions` — per the brief guardrail (no DNS changes).
- NVDA / VoiceOver U2 verification — outside the Claude harness.
- SKS prod ports (S1 / U2 / SEC2 etc.) remain in PR #93 + DEMO-VS-LIVE.md decision matrix; left for explicit Royce instruction.
- Per-user `auth.uid()`-based RLS on the canonical Supabase — waits for the day client-side Supabase access matters (Phase 2+).
- End-to-end smoke (Phase 1.D) — needs Netlify deploy live + env vars set. Royce runs after morning review.

**Status:** Three PRs open, none merged. eq-field-app/demo HEAD unchanged (`7249833`). eq-solutions/eq-shell main unchanged. `eq-shell-control` Supabase has one new migration applied (pin_hash + service-role policies). No version banner / APP_VERSION / sw.js bumps on EQ Field — overnight run touched only the docs files on demo, and the v3.5.9 banner ship is still PR #106 (Phase 1.C). Next session resumes from Royce's morning review of PRs #1, #107, #2 — with env vars set + Netlify GitHub link wired, Phase 1.D end-to-end smoke can run.

## [2026-05-18] Phase D EQ Shell — design locked + Phase 1.A scaffold provisioned
**Built by:** Royce Milmlow + assistant
**Brief:** Phase D of `NEW-WINDOW-PROMPT-melbourne-ready.md` (design pivot per the cowork EQ Shell architecture)
**Branches:** `claude/phase-d-eq-shell-design` (PR #104, merged 13:25Z)
**Companion repos / projects (new):**
- GitHub: [`eq-solutions/eq-shell`](https://github.com/eq-solutions/eq-shell) (private, main branch, Vite + React + TS scaffold pushed)
- Supabase: `eq-shell-control` (id `hxwitoveffxhcgjvubbd`, region ap-southeast-2, EQ Solutions org, $10/mo)
- Netlify: `eq-shell` (id `a3473f83-7c82-4f1e-872d-aa96eaa55172`, milmlow team, `eq-shell.netlify.app`)
**Changes:**
- **Design locked (PR #104):** All 10 architecture questions resolved. EQ Shell is Vite + React + TypeScript, hosted at `*.eq.solutions` on Netlify with a canonical Supabase (`eq-shell-control`) for tenants / users / module_entitlements / branding. Cookie auth on `*.eq.solutions` for React modules; URL-hash HMAC token for the cross-domain EQ Field iframe. EQ Field stays vanilla and embedded via iframe initially; Tender Pipeline migration to React shell-routes is Phase 2 (the wedge); surface-by-surface Field migration is Phase 3+ as each needs rework. Auto-merge bar declined; Royce reviewed + merged manually.
- **Phase 1.A scaffolding provisioned:** Three real-world resources created in one pass — (1) `eq-solutions/eq-shell` GitHub repo (private, default Vite react-ts template plus a real README documenting the design + companion infra), (2) `eq-shell-control` Supabase project in Sydney (Royce confirmed $10/mo cost; canonical schema v1 applied with `tenants` / `users` / `module_entitlements` tables + `_touch_updated_at` trigger function with explicit `search_path = ''` to satisfy the database linter; RLS enabled on all three with no policies yet — deny-by-default until Phase 1.B's auth model lands), (3) `eq-shell` Netlify project on the milmlow team (empty container; needs GitHub integration + custom domain configured via dashboard — manual handoff to Royce per Netlify UI's better DX for these settings).
- **Substrate observation:** the cowork message Royce surfaced mid-session about Tender Pipeline's fortnightly review meeting being "the product, not the screen" reframed Phase D's scope. Adoption signal of "6 fortnightlies + 30 notes at month 3" is now preserved in the design doc as the Phase 2 success metric. Tender Pipeline's existing vanilla implementation (v3.4.79-83) lives on until the React port is shipped + soaked for ~2 weeks — no cutover risk.
**Status:** PR #104 merged to demo. Three new infra resources alive. Phase 1.B (wire-up: shell-login + verify-shell-session + mint-iframe-token Netlify functions + React shell with login + tenant-home + iframe-Field route) is the natural next session. Two open items deliberately handed off to Royce: (1) link the `eq-solutions/eq-shell` GitHub repo to the `eq-shell` Netlify project via the dashboard's auto-deploy integration, (2) configure the `*.eq.solutions` wildcard custom domain DNS. Both are 2-minute UI flows that the Netlify MCP doesn't cleanly cover.

## [2026-05-18] Phase C Melbourne prep — U2 accessibility cleared + Phase D design opened
**Built by:** Royce Milmlow + assistant
**Brief:** `NEW-WINDOW-PROMPT-melbourne-ready.md` (Phase C of 5 + Phase D design pivot)
**Branches:** `claude/v3.5.7-u2-axe-fixes` (PR #102, merged), `claude/v3.5.8-u2-manual-pass` (PR #103 closed → re-opened as PR #105, merged), `claude/phase-d-eq-shell-design` (PR #104 open — design doc only)
**Changes:**
- **v3.5.7 — U2 Phase 2 (PR #102, merged 12:52Z):** axe-core 4.11.4 auto-flagged WCAG 2.1 AA findings against the live demo landing — 23 violations across 2 rules (21 × color-contrast serious, 2 × select-name critical). New text-safe CSS vars (`--green-text` #15803D, `--amber-text` #B45309, `--purple-text` #5B53A8 — brand variables kept for backgrounds and accents). Class-level updates to `.pill-green` / `.pill-amber` / `.stat-card-sub` / `.nav-label` + `.sidebar-footer`. Inline contrast bumps on sidebar dark-navy text (rgba(.32–.4) → rgba(.7–.75)), Pipeline/Trial NEW badges (cyan-500 → cyan-300), Job Numbers/Apprentices BETA badges. `aria-label` on `#globalWeek` and `#dash-group-filter` selects. Re-ran axe-core against the deploy preview — **0 violations**, 21 passes. Behaviour-preserving + additive; qualified for the brief's auto-merge bar but Royce reviewed and merged manually.
- **v3.5.8 — U2 Phase 3 (PR #105, merged 12:53Z; originally PR #103 stacked on #102, GitHub auto-closed when #102's branch was deleted, rebased + re-opened):** the manual-pass portion that axe-core can't catch. `scripts/utils.js` — `openModal`/`closeModal` refactored with `_modalTriggerStack`: stash trigger on open, restore focus to it on close, nested-modal aware (LIFO). `role="dialog"` + `aria-modal="true"` stamped lazily on first open. Tab keydown handler cycles focus inside the top-most open `.modal-overlay` (WCAG 2.4.3 + 2.1.1). Backdrop-click + ESC-to-close route through `closeModal` so focus restore fires. `#toast` in index.html gets `role="status"` + `aria-live="polite"` + `aria-atomic="true"`. NVDA spot-check explicitly flagged as owed to Royce — the one verification step that can't run from the Claude harness.
- **Netlify env-var updates (out-of-PR, Royce-authorised):** set `RATE_LIMIT_V2=on` (functions scope, production context) to activate PR #99's distributed rate-limit RPC path on the EQ Netlify deploy. Then surfaced a pre-existing config bug: `verify-pin.js` reads `AUDIT_SB_URL` / `AUDIT_SB_KEY` env vars but only `LEAVE_SB_URL` / `LEAVE_SB_KEY` had been set — audit logging from the gate function had been silently no-op for some time, and the new `bumpRateLimitRPC` inherited the same short-circuit. Added `AUDIT_SB_URL` + `AUDIT_SB_KEY` env vars (same values as `LEAVE_*`, scope=functions, context=all). Next verify-pin cold start activates both audit logging and the RPC path. Long-term: rename in code to a single source-of-truth name (separate small PR).
- **Phase D design pivot — `EQ-SHELL-DESIGN.md` (PR #104 open):** the brief's Phase D framing (tenant onboarding admin flow inside EQ Field) is materially obsolete. Royce surfaced a different architecture mid-session: EQ Shell at `<tenant>.eq.solutions` hosting Cards / Intake / Quotes / Service / Field as lazy-loaded modules, with a "canonical layer per tenant" managing config + entitlements + branding at the shell layer. Drafted 177-line design doc capturing: ASCII topology, 10 open questions (Q1-Q10) that block code (highest-stakes: Q2 — EQ Field as React port vs iframe vs Web Component embed), proposed MVP shape (3-5 sessions, EQ Field as iframe child initially, canonical Supabase for tenant config only, no wizard MVP), explicit "what this doc does NOT propose". Doc-only PR; Royce reviews + answers Q1-Q4 (the four that unblock everything) before code starts.
- **AUDIT-REVIEW.md / SPRINT-PLAN.md / DEMO-VS-LIVE.md NOT updated** in this PR set — the Phase A+B summary PR #101 already covered through Phase B. A separate hygiene pass (Phase C closures + Phase D pivot recorded) is recommended when convenient; left for a future session to keep these PRs scoped.
**Status:** Demo on v3.5.8 (HEAD = `83cad05`). axe-core auto-flagged WCAG 2.1 AA = 0 violations on landing. Behind-gate surfaces (modal flows, etc.) wired with focus/aria semantics but await NVDA spot-check. Phase D design PR #104 open; awaiting Royce's Q1-Q4 answers before code. Phase E (post-Phase D) not started.

## [2026-05-18] Phase A+B Melbourne prep — security backlog cleared on demo
**Built by:** Royce Milmlow + assistant
**Brief:** `NEW-WINDOW-PROMPT-melbourne-ready.md` (Phases A + B of 5)
**Branches:** `claude/melbourne-scale-verify` (Phase A, PR #97 open), `claude/sec3-tender-rls-rewrite` (PR #98, merged), `claude/sec2-phase-d-rate-limit` (PR #99, merged), `claude/sec1-magic-link-ttl-48h` (PR #100, merged), `claude/melbourne-session-2026-05-18-summary` (this doc-update PR)
**Changes:**
- **Phase A — Scale verification (PR #97 open):** Drove Claude-in-Chrome against `eq-solves-field.netlify.app/?seed500`. Verified live: Contacts virtualisation (498 people / 43 `<tr>` in DOM via `EQVirtualTable`), Edit Roster + Roster view `content-visibility: auto` on 498 rows each, sliding-window helpers wired (`_getVisibleWeekRange` returns 9 weeks), Tender Pipeline `EQ_TENDER_PIPELINE.loadAll()` returns 323 tenders + 12 nominations, mobile home tile flag default-on. Limitations recorded honestly: EQ tenant short-circuits Supabase so live `week=in.(...)` only exercised on SKS port (PR #93); supervisor home variant deferred (requires supervisor unlock). New doc `MELBOURNE-VERIFY-2026-05-18.md`.
- **Phase B1 — FINDING #SEC3 closed (PR #98, merged 11:33:17Z):** New migration `migrations/2026-05-18_tender_rls_tighten.sql`. All 24 placeholder `_anon_*` policies on the 6 tender tables replaced. 4 tables with direct `org_id` (tenders/tender_import_runs/tender_review_decisions/pending_schedule) gated on `org_id IS NOT NULL`. 2 tables without (nominations/tender_enrichment) gated on `EXISTS (tender_id → tenders.org_id IS NOT NULL)`. HONEST CAVEAT in migration header (mirrors `2026-05-13_roster_presence_rls_tighten.sql` precedent): EQ Field's anon-key auth model can't enforce `auth.uid()`-based RLS — cross-tenant read by anyone with the anon key remains structural until Wave 5+ SSO. The brief's prescribed `TO authenticated USING (auth.uid()...)` pattern was a wrong premise; surfaced and adjusted mid-session. Migration applied to EQ Supabase via MCP; app post-tighten still reads 323 tenders + 12 nominations.
- **Phase B2 — FINDING #SEC2 Phase D closed (PR #99, merged 11:33:29Z):** Migration `2026-05-15_rate_limit_buckets_v1.sql` activated — applied to EQ demo Supabase via MCP, RPC sanity-tested (5x true, 6th false), header updated from "DO NOT APPLY" to "Applied 2026-05-18". `netlify/functions/verify-pin.js` wired with env-var feature flag `RATE_LIMIT_V2`: when off (current state), serves the in-memory `attempts={}` path unchanged; when on, distributed `bump_rate_limit` RPC bucket lockout supersedes in-memory (kills the cold-start bypass that was the original finding). Belt-and-braces fallback: RPC blip falls through to in-memory. Tenant derived from request Origin (`sks` / `eq` / `unknown`). New client helper `bumpRateLimit(key, max, windowSeconds)` in `scripts/supabase.js` for future defence-in-depth use. **Activation requires setting `RATE_LIMIT_V2=on` in eq-solves-field Netlify env vars** — not auto-flipped by the merge.
- **Phase B3 — FINDING #SEC1 closed (PR #100, merged 11:33:38Z):** `LEAVE_ACTION_TTL_MS` dropped from `7 * 24 * 60 * 60 * 1000` to `48 * 60 * 60 * 1000` in both `netlify/functions/send-email.js` and `supabase/functions/supervisor-digest/index.ts`. `approve-leave.js` header comment updated to match. Was parked 2026-05-13 with risk accepted; unparked for Melbourne procurement posture. Newly-minted approve/reject links expire after 48h; already-minted links keep their original `exp` until they hit it.
- `AUDIT-REVIEW.md` — session log entry appended; #SEC1/#SEC2/#SEC3 moved to Closed/shipped findings.
- `SPRINT-PLAN.md` — §SEC2 status block updated (Phase D ✅ shipped). §SEC1 in out-of-scope list updated (✅ shipped via PR #100).
- `DEMO-VS-LIVE.md` — Tender Pipeline SEC3 section rewritten (closed), §9 SEC2 section rewritten (closed pending env-var flip), "Risks on live" section updated, deploy snapshot table updated to post-#100 HEAD (`c9cde43`).
**Status:** Phase A doc PR (#97) still open — Royce's call. Phases B1/B2/B3 all merged to `demo`. Phase B GATE passed. `RATE_LIMIT_V2` env var NOT set; Phase D's RPC path is dormant code until that flip. SKS prod unaffected by any of this work — separate rollout decision per finding when Royce calls "SKS live". Phase C (FINDING #U2 accessibility, ~5-6h split across axe-core auto-fixes + manual focus/keyboard/aria-live pass) awaiting green-light. Phase D (tenant onboarding admin flow) is design-first; brief has four open questions (E1-E4) requiring Royce decisions.

## [2026-05-15] SEC2 design — rate-limit-buckets migration file (PENDING)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/sec2-rate-limit-buckets-design` → `demo` (PR #90)
**Changes:**
- New `migrations/2026-05-15_rate_limit_buckets_v1.sql` — `public.rate_limit_buckets` table + `public.bump_rate_limit(p_key, p_max, p_window_seconds)` RPC + RLS denial-by-default (service-role bypass). SQL lifted verbatim from `SPRINT-PLAN.md` §SEC2 per SPRINT-QUESTIONS Q9 default.
- File marked **PENDING** in top-comment header: DO NOT call `mcp__*__apply_migration` / `mcp__*__execute_sql`. Phase D consumes it when server-side role checks land, alongside wiring `bump_rate_limit()` into `netlify/functions/verify-pin.js` (replaces in-memory `attempts = {}` map flagged as FINDING #SEC2).
- `SPRINT-PLAN.md` §SEC2 — status block: Phase 1 ✅ shipped, Phase D ⏳ pending.
- `AUDIT-REVIEW.md` — FINDING #SEC2 moved from Open → Tracked findings with pointer to the migration file.
**Status:** SQL file on demo `migrations/` directory. **Not applied to EQ demo or SKS prod Supabase.** Phase D unblocks the actual fix.

## [2026-05-15] v3.5.3 — S1 sliding-window queries (Melbourne scaling unblocked)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.5.3-s1-sliding-window` → `demo` (PR #89, merge `8890efd`; supersedes closed PR #88)
**Changes:**
- Resolves AUDIT-REVIEW FINDING #S1 (HIGH severity) — the single biggest Melbourne scaling blocker. `schedule?select=*` and `timesheets?select=*` were unscoped; at 577 ppl × 52 weeks (~30k rows) the page load + every 30s poll pulled 5–10MB. Unusable above ~100 users.
- All 5 phases bundled. Phase 1 — `STATE.loadedWeeks = new Set()` + `_getVisibleWeekRange()` helper (9-week window centred on current week). Phase 2 — `loadFromSupabase` + `loadTimesheets` now use `&week=in.(visibleWeeks)`. Phase 3 — `_loadWeeks(weekKeys)` lazy-loads on `onWeekChange` with adjacent ±4 prefetch + inline "↻ Loading…" indicator. Phase 4 — `_evictDistantWeeks()` caps `loadedWeeks` at 16, drops furthest-from-current first. Phase 5 — dashboard investigation confirmed no-op (renderDashboard + updateTopStats both scope to `STATE.currentWeek`).
- Bulk exports split off — `_loadFullDataForExport()` returns un-scoped snapshot; `exportScheduleCSV` pre-fetches via the helper. Single-week exports untouched (already scoped).
- Defaults applied per SPRINT-QUESTIONS: Q1 (±4 weeks / 9 visible), Q2 (always prefetch adjacent), Q3 (bulk-exports full-fetch on demand), Q4 (investigate dashboard first), Q5 (DEMO ONLY — SKS port after 3–5 days clean soak).
- Realtime channel still org-scoped (FINDING #S3 parked) — out-of-window updates dropped client-side; user sees them on next nav to that week.
**Status:** Live on demo. SKS prod (sks-nsw-labour) untouched, still on v3.4.73 — soak clock for v3.5.4 SKS port starts 2026-05-15.

## [2026-05-15] v3.5.2 — Site Reports HUB (collapses Prestart / Toolbox / Diary)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.5.2-site-reports-hub` → `demo` (PR #85, merge `e4985c5`)
**Changes:**
- New `scripts/site-reports-hub.js` — single "Site Reports" sidebar entry lands on a HUB page with three status cards (Prestart · today / Toolbox · this week / Diary · today). Tap-through routes to the existing workflow via `showPage('prestart' | 'toolbox' | 'diary')`. Pre-loads all three caches in parallel on first render so counts are live.
- Three original sidebar entries (Prestart / Toolbox / Diary) **hidden** (inline `style="display:none"`), not deleted — deep-links + v3.5.0 staff home-tile Pre-starts tile still work.
- Count accessors added to each workflow module: `window.eqGetPrestartsTodayCount()`, `window.eqGetToolboxWeekCount()`, `window.eqGetDiariesTodayCount()`. SKS Prestart card suppressed via `TENANT_DISABLED_TABLES.sks`.
- Permissions: HUB always renders. Each card tap-through hits the underlying workflow which already enforces `reports.{prestart,toolbox,diary}.view` via `EQ_PERMS` — no double-gating needed in HUB.
**Status:** Live on demo. Weekly Site Report (next Site Reports milestone, ~6–8 days work) gated on at least one supervisor actually using all three workflows weekly.

## [2026-05-15] v3.5.1 — Mobile-first home tile screen: supervisor variant
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.5.1-supervisor-home` → `demo` (PR #83, merge `c215571`)
**Changes:**
- Phase 2 of the mobile-first nav rollout (Phase 1 was v3.5.0 staff). Supervisors on mobile (viewport <768px, `isManager === true`, `home_screen_v1` flag on) land on a six-tile home screen plus action strip: "Needs you today · N leave to approve · N pre-start". Empty state shows a green "All clear" panel.
- TILES — Schedule, Timesheets, Leave, Pre-starts, Team, Reports. Decision G1: STATUS badges only on tiles (e.g. "New" on Pre-starts) — counts live exclusively on the action strip.
- COG DRAWER — supervisor variant adds Edit roster / Sites / Job numbers / Apprentices / Supervision / Import-Export / Audit log on top of the staff drawer.
- Action-strip data: `window.eqGetPendingLeaveCount()` (in leave.js) + `window.eqGetPrestartsDraftCount()` (in site-reports.js, distinct from HUB's `eqGetPrestartsTodayCount` — different semantics). "Timesheets to review" count **dropped** from MVP — timesheets have no review-state column.
- ROUTING — `initApp()` gets a parallel supervisor branch mirroring v3.5.0 staff. Desktop supervisor (≥768px) or flag-off keeps existing sidebar shell — no regression for the 90% of supervisor work happening at a desk.
- Reuses `home_screen_v1` flag (no separate flag). Draft `_proposals/mobile-first-nav/phase-2-supervisor-home.js` stamped SHIPPED IN v3.5.1 header.
**Status:** Live on demo. SKS sees this on mobile too since flag default-on for both tenants.

## [2026-05-15] Audit + CI chores (no version bump)
**Built by:** Royce Milmlow + assistant
**Branches:** `claude/audit-slash-command` (PR #86, merge `e8ff20c`), `claude/u2-axe-ci-scaffold` (PR #87, merge `a005104`), `claude/audit-session-summary-2026-05-15` (PR #84, merge `067576c`)
**Changes:**
- `.claude/commands/audit-multi-lens.md` (PR #86) — on-demand `/audit-multi-lens` replacement for the dead cloud `/schedule`. Mirrors `REVIEW-MULTI-LENS.md` v1 three-perspective format, produces dated artifact in `_reviews/multi-lens/`.
- `.github/workflows/accessibility-audit.yml` (PR #87) — U2 Phase 1. Manual `workflow_dispatch` (no cron). Tenant dropdown `eq` | `sks`. axe-core CLI via npx; WCAG 2.0/2.1 A/AA; JSON + HTML reports uploaded as artifacts. CI report doubles as procurement-gate documentation.
- `AUDIT-REVIEW.md` Session entry for 2026-05-15 (PR #84) — captures state-of-the-world corrections + schema-correction table for the supervisor home draft.
**Status:** All three merged into demo same session. Axe workflow available to trigger manually any time; no auto-runs.


## [2026-05-14] v3.5.0 — Mobile-first home tile screen (staff role, flag-gated)
**Built by:** Royce Milmlow + assistant (separate session)
**Branch:** `claude/v3.5.0-mobile-home` → `demo` (commits `6fe968c`, `89072b6`, `375a72f`, `b512c84`)
**Changes:**
- New `scripts/home.js` (~362 lines) — mobile-first tile screen for STAFF role. Four tiles: My Schedule, Timesheets, Leave, Pre-starts. Next-shift pill (decision B1). Cog drawer (slide-up sheet) for everything-else nav. PostHog page-view fires from here.
- New `styles/home.css` (~315 lines) — tile grid, pill, drawer, loading skeleton, offline banner. Hidden on viewport ≥ 768px (desktop staff keep existing shell).
- New PostHog flag `home_screen_v1` in `scripts/flags.js`. Default ON as of `b512c84` (after eyeballing the staff flow on phone). Routing fires only when (a) flag enabled (b) `role==='staff'` (c) viewport <768px.
- New `index.html` mount `<div id="page-home">`, `PAGE_TITLES.home`, dispatch in `renderCurrentPage`, routing in `initApp()` to choose home vs schedule landing.
- EQ blue diamond favicons (recoloured from navy `#1F335C` to EQ blue `#3DA8D8` gradient) shipped in same version.
- **v3.4.84 pipeline UI polish FOLDED IN** (commit message confirms): PM/Supervisor dropdowns now pull from `STATE.managers` (was `STATE.people`); Pipeline Dashboard + Review queue Stage/Dept filters; nomination name lookups check managers first then people. The orphan `CHANGELOG-v3.4.84.md` file remained on disk as historical doc; no separate version was published.
- Decisions baked in per `_proposals/mobile-first-nav/MOBILE-FIRST-NAV-PROPOSAL.md` v1.1: A1 (staff mobile only), B1 (next-shift pill), C1 (Pre-starts hidden on SKS via `TENANT_DISABLED_TABLES`), D (labels), E (greeting personality), H1 (greeting once per day then date), I1 (live counts on schedule + timesheets only).
**Status:** Live on demo. SKS prod still on v3.4.73 (flag default-on for both tenants but supervisor variant not in v3.5.0 — Phase 2 in #83).

## [2026-05-14] v3.4.83 — Tender Pipeline: onclick fix + Dashboard + job fields + session close + Promote UX
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.83-pipeline-polish` → `demo` (commit `82123ff`)
**Changes:** Quality-of-life cleanup on the Tender Pipeline kanban: card onclick fixed for some edge cases, dashboard refinements, additional job fields surfaced, review-session close UX clarified, Promote-to-Schedule flow tightened. Pure UX polish — no schema changes.
**Status:** Live on demo. SKS untouched (Tender Pipeline is demo-only).

## [2026-05-14] v3.4.82 — Tender Pipeline: drag-and-drop kanban + Review = decision queue
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.82-pipeline-dnd` → `demo` (commits `0ca5956`, `36bd23e` for the missed changelog)
**Changes:** Drag-and-drop on the Tender Pipeline kanban (stage transitions via DnD). "Review" surface restructured into a decision queue rather than a list. The v3.4.82 changelog commit was missed in the original push (sandbox /tmp path quirk) and landed in a follow-up `36bd23e`.
**Status:** Live on demo.

## [2026-05-14] v3.4.81 — Tender Sync actually working + What's New refresh
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.81-tender-sync-fix` → `demo` (commit `36e4009`)
**Changes:**
- Tender Sync (Excel import) was DOA after v3.4.80 because the cdnjs URL pointed at xlsx 0.20.3 which cdnjs doesn't host. Pinned to xlsx 0.18.5 (last cdnjs-hosted build, same API surface).
- "What's New" banner refreshed — was stuck on v3.4.22-era content (digest, birthdays, timesheet bar). Now surfaces recent shipments: Tender Pipeline, Daily Site Diary, Toolbox Talks. WHATSNEW_KEY bumped to v3.4.81 so every user sees the banner once.
**Status:** Live on demo.

## [2026-05-14] v3.4.80 — CSP hotfix: unblock SheetJS for Tender Sync
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.80-csp-fix` → `demo` (commit `9e7d901`)
**Changes:** Tender Sync (v3.4.79) was DOA on live demo — SheetJS CDN script blocked by CSP. Two CSP definitions live in the repo (`_headers` and inline meta tag); both relaxed to permit the SheetJS cdnjs origin. Real fix but not THE fix — v3.4.81 had to pin the actual cdnjs URL since the original 0.20.3 path 404'd.
**Status:** Live on demo.

## [2026-05-14] v3.4.79 — Tender Pipeline module (new workstream)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.79-tender-pipeline` → `demo` (PR #82, squash merge `b587b78`)
**Changes:**
- New `scripts/tender-pipeline.js` (~1900 lines at ship time, ~2000 after the v3.4.80-84 patches landed) — kanban for tracking tender opportunities through stages (watch → confirmed → likely → won/lost). Drag-and-drop transitions, enrichment slide-over, nomination model, review queue.
- New `scripts/tender-parser.js` — Excel ingestion via SheetJS (xlsx). Parses tender intake spreadsheets into `tender_import_runs` rows. CSP needed v3.4.80 hotfix before this actually worked end-to-end.
- New Supabase migration creating `tenders`, `tender_enrichment`, `nominations`, `nomination_clashes` (view), `tender_import_runs`, `tender_review_decisions`, `pending_schedule`. DEMO ONLY — SKS tenant has these in `TENANT_DISABLED_TABLES.sks` so the fetches no-op.
- New sidebar entries: Pipeline Dashboard, Pipeline (kanban), Fortnightly Review, Tender Sync. Pipeline Dashboard surfaces stage-by-stage counts + filters.
**Status:** Live on demo. Not in any earlier brief — was Royce's mid-week pivot. Five subsequent versions of polish (v3.4.80–84) landed within 36 hours.

## [2026-05-13] v3.4.77 — Site Reports v3: Daily Site Diary MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.77-diary` → `demo` (PR #81, squash merge `ceec471`)
**Changes:**
- New `scripts/diary.js` (~700 lines) — third workflow in Site Reports, sibling to Prestart and Toolbox. Consumes `scripts/site-reports-shared.js` (v3.4.76) for photo / signature / offline-queue controllers; only diary-specific logic remains in this file: weather JSONB, shift_type (day / night / split), repeating sections for work_areas / delays / incidents / visitors, free-text materials_received / equipment_status / notes.
- New migration `2026-05-13_site_diaries_v1.sql` — `site_diaries` table with same RLS + realtime pattern as `prestarts` and `toolbox_talks`. Photos JSONB included from day 1.
- `permission-matrix.js` updated — `reports.diary.{view,create,submit,sign}` added.
- New sidebar entry "Diary" under "Testing (DO NOT USE)", BETA chip, next to Prestart and Toolbox.
- Hub/dashboard restructure DEFERRED again (now three workflows exist — trigger condition reached — but soak first; HUB ships in PR #85 not yet merged).
**Status:** Live on demo. SKS untouched (diary tables not yet applied to SKS Supabase).

## [2026-05-13] v3.4.76 — Site Reports refactor: extract shared photos / signature / queue
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.76-shared-refactor` → `demo` (PR #80, squash merge `306525d`)
**Changes:**
- New `scripts/site-reports-shared.js` (~470 lines) — factory functions extracting the helpers that had been copy-pasted between Prestart (v3.4.69) and Toolbox (v3.4.75):
  - `createPhotoController(config)` — photo upload, list render, captions, lightbox, max-N enforcement.
  - `createSignatureController(config)` — canvas-based signature pad, attendance roster, sign / unsign / clear.
  - `createOfflineQueue(config)` — localStorage-backed write queue with replay listener.
  - `injectMobileStyle(prefix)` — mobile responsive CSS, one-shot per prefix.
- `scripts/site-reports.js` — Prestart drops ~310 lines of duplicated helpers. Keeps Prestart-specific: HRCW categories, crew shape, dual-source notice.
- `scripts/toolbox.js` — Toolbox drops ~290 lines of duplicated helpers. Keeps Toolbox-specific: topic / safety_message / items_reviewed / attendance.
- Refactor lands BEFORE Diary (v3.4.77) so the third workflow starts lean.
**Status:** Live on demo. No schema or behaviour change — purely structural cleanup.

## [2026-05-14] v3.4.75 — Site Reports v2: Toolbox Talk MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.75-toolbox` → `demo` (PR #77, squash merge `66e03a9`)
**Changes:**
- New `scripts/toolbox.js` (~810 lines) — sibling to `scripts/site-reports.js`. Photo / signature pad / offline write queue copy-pasted with `toolbox` / `_tbx` prefixes. Refactor target: extract shared helpers to `site-report-shared.js` once Daily Diary (v3) lands.
- New migration `2026-05-14_toolbox_talks_v1.sql` — `toolbox_talks` table with same RLS + realtime pattern as `prestarts`. Photos JSONB included from day 1 (Prestart needed a follow-up — not repeating).
- `permission-matrix.js` v1.2 — `reports.toolbox.{view,create,submit,sign}` added. Manager + supervisor get all four; employee / apprentice / labour_hire get `.sign` only (mirrors prestart shape).
- New sidebar entry "Toolbox" under Testing (DO NOT USE), BETA chip, next to Prestart.
- Version bump tuple: `index.html` banner + `scripts/app-state.js` `APP_VERSION` + `sw.js` CACHE all → `v3.4.75`. `sw.js` PRECACHE list includes `/scripts/toolbox.js`.
- **Migrations applied 2026-05-14 to BOTH Supabase projects:**
  - `ktmjmdzqrogauaevbktn` (eq-solves-field) ✓
  - `nspbmirochztcjijmcrx` (sks-labour) ✓ — applied per Royce's explicit "SKS live" go so Ben Ritchie can preview via `eq-solves-field.netlify.app/?tenant=sks`

**Schema differences from `prestarts` (deliberate):**
- `facilitator` (not `sks_rep`) — toolbox column names must be tenant-neutral. Prestart's `sks_rep` is a legacy leak not repeated in new tables.
- `meeting_date` / `meeting_time` (not `briefing_date` / `briefing_time`) — toolbox = scheduled meeting, not pre-shift briefing.
- `attendance` (not `crew`) — toolbox audiences include subbies, clients, visitors. Same JSONB shape as `prestarts.crew` so signature pad code is reusable.
- Toolbox-specific fields: `topic`, `safety_message`, `items_reviewed`, `open_actions`, `next_meeting`.

**Why:** Path C absorption (see `ops/decisions.md` 2026-05-13) — second workflow folded in from Ben Ritchie's `sks-field-reports.netlify.app` v29. Prestart shipped as v3.4.69; Toolbox is the second of four (Diary + Weekly to follow). Lessons applied: v3.4.54 per-action inflight guards, v3.4.55 id-coercion via `String()` for tenant-portable PKs, v3.4.56 audit failures surfaced via `console.warn` (offline queue).

**Brief drift caught:** The outstanding-build brief claimed v3.4.69 was demo's tip; reality was v3.4.74. Branch renumbered mid-session from `claude/v3.4.74-toolbox` → `claude/v3.4.75-toolbox`. The `ops/decisions.md` 2026-05-13 entry about demo version-number coordination now has two same-day events confirming the pattern (v3.4.67→v3.4.69 rebase AND v3.4.74→v3.4.75 rename).

**Status:** Live on demo (`eq-solves-field.netlify.app`) post-Netlify-deploy. Hub/dashboard restructure deferred (≥2 workflows now exist but each soaks separately first). NOT deployed to SKS prod (`sks-nsw-labour.netlify.app`) — `main` branch untouched.

## [2026-05-13] v3.4.74 — ESC-to-close on modals (accessibility quick-win)
**Built by:** Royce Milmlow + assistant (Night 1 audit auto-merge)
**Branch:** `claude/audit-night1-all-angles` → `demo` then `main` (PR #73)
**Changes:**
- Global `keydown` listener added in `scripts/utils.js`. Closes only the TOP-MOST open modal per press so confirm-on-top-of-edit stacks peel back rather than blowing both away.
- Behaviour-preserving, <50 lines, no auth / no RLS change — auto-merge bar met.
**Why:** Surfaced by the Night 1 manual audit run (`AUDIT-REVIEW.md`, usability angle, FINDING #U1). Modals already closed on backdrop-click and ✕-button; ESC did nothing — standard keyboard convention violation. First step of a broader accessibility pass needed for Melbourne enterprise procurement (FINDING #U2 covers `aria-*` coverage gap).
**Status:** Live on both demo and SKS prod. 7 other audit findings opened for Royce review (see `AUDIT-REVIEW.md`).

## [2026-05-13] v3.4.73 — widen week-picker so "(this week)" no longer truncates
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.73-week-pill-width` → `demo` then cherry-picked to `main` (PR #69)
**Changes:**
- Removed `max-width:80px` on `#globalWeek`; `<select>` now sizes to widest option (~150px).
- Mobile unaffected — `.topbar-week` still uses `flex:1`.
**Why:** SKS topbar dropdown was cutting "◉ DD.MM.YY (this week)" to "(t...s)" on prod.
**Status:** Live on both demo and SKS prod.

## [2026-05-13] v3.4.72 — skip render when polled data hasn't changed (kills flash)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.72-skip-render-on-unchanged` → `demo` then `main` (PR #67)
**Changes:**
- New `_computeStateSignature()` builds sort-stable signature over people / managers / sites / schedule / timesheets / leaveRequests.
- `refreshData()` diffs post-load signature against last rendered; only calls `renderCurrentPage` on actual change.
- Manual ↻ Sync still renders unconditionally for visual feedback. Signature seeded after initial load so first poll doesn't fake-trigger.
**Why:** Constant flashing on SKS prod — 30-second background poll was doing full innerHTML swap unconditionally, causing scroll jump + focus drop even with no data delta.
**Status:** Live on both demo and SKS prod. Idle background poll is now a silent no-op.

## [2026-05-13] v3.4.71 — remove Project Hours panel + fix EQ→SKS logo flash
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.70-supervisor-fixes` → `demo` then `main` (PR #64; bundled with v3.4.70)
**Changes:**
- Removed `#project-hours-panel` + script tag. Kept `scripts/project-hours.js` (parked) + `sites.track_hours` column on EQ.
- New `earlyBootBranding()` IIFE in `scripts/app-state.js` fires on DOMContentLoaded, detects slug synchronously, applies `TENANT_BRANDING` before first paint.
- `loadTenantConfig` still runs at onload for Supabase-driven access codes; `applyTenantBranding` idempotent so second call just refreshes.
**Why:** (1) Project Hours panel surfaced 'schema not applied' warnings on SKS where the migration hadn't run, added nothing useful. (2) SKS users saw EQ sky-blue logo for 200-600ms before SKS dark-blue snapped in — cause was async `loadTenantConfig()` from `window.onload` despite branding data being static per tenant.
**Status:** Live on both demo and SKS prod.

## [2026-05-13] v3.4.70 — supervisor dob/start_date + Excel date import + archive
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.70-supervisor-fixes` → `demo` then `main` (PR #64)
**Changes:**
- `migrations/2026-05-13_managers_dob_start_date_archived.sql` adds `dob_day`, `dob_month`, `start_date`, `archived` on `managers`; `archived` on `people`. **Applied to BOTH Supabase projects on 2026-05-13.**
- `import-export.js`: `_parseCsvBirthday` now matches DD/MM/YYYY; new `_parseStartDate` handles ISO + DD/MM/YYYY + Excel serial numbers.
- Supervisor modal exposes DOB + start_date. Both filter rows get "Show archived" toggle. Active/archived render-tint + handlers wired in `managers.js` / `people.js`. Badges count active rows only.
- `supabase.js`: `saveManagerToSB` sends new columns; `savePersonToSB` sends `archived`; new `archiveManagerInSB` + `archivePersonInSB` helpers via PostgREST PATCH.
**Why:** Royce CSV review 2026-05-13 surfaced: supervisors had no DOB/start_date (people had since v3.4.16), Excel uploads rejected DD/MM/YYYY + serial dates, no reversible archive (only hard delete via `deleted_at`). Contacts↔Supervisors double-up confirmed by design (Wave 4).
**Status:** Live on both demo and SKS prod. Behaviour-preserving for existing rows.

## [2026-05-13] v3.4.69 — Site Reports module + Prestart MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.67-prestart` → `demo` (PR #62) — rebased on top of v3.4.68 role-system, so the branch name keeps the original v3.4.67 label but the merge ships as v3.4.69. v3.4.67 was never released.
**Changes:**
- New "Site Reports" sidebar entry under "Testing (DO NOT USE)" section with BETA chip. v1 ships Prestart only — toolbox / diary / weekly follow the same pattern.
- Photos: max 8 per record, camera+gallery on mobile, resized to 1600px / JPEG-q70, stored inline as base64 in `prestarts.photos` JSONB. Lightbox + captions.
- Signature pad: HTML5 canvas modal, touch + mouse, DPR-aware. Saved as base64 PNG into `crew[i].signature_image`; idempotent re-tap preserved (v3.4.54 lesson).
- Offline write queue: `navigator.onLine` + try/catch around `sbFetch`; localStorage-backed queue replays on `'online'` event + page load. Per-tenant scoped. Visible pending pill in form footer.
- Mobile responsive: form grid collapses to 1 column < 640px; modal goes full-screen; signature canvas bumps to 260px for finger signing.
- Dual-source notice: dismissible yellow banner directing users away from `sks-field-reports.netlify.app`.
- **Migrations applied 2026-05-13 to BOTH Supabase projects:**
  - `2026-05-13_site_reports_v1.sql` — `prestarts` table + RLS + realtime
  - `2026-05-13_prestarts_photos.sql` — `ADD COLUMN photos jsonb`
**Why:** Path C absorb (see `ops/decisions.md` 2026-05-13) — workflows from Ben Ritchie's `sks-field-reports.netlify.app` v29 fold into EQ Field as a commercial sub-module. Prestart is the first of four (Toolbox / Diary / Weekly to follow). Lessons applied: v3.4.54 per-action inflight guards, v3.4.55 id-coercion for bigint/uuid PK portability, v3.4.56 audit failures surfaced via `console.warn` not silenced.
**Status:** Live on demo only (`eq-solves-field.netlify.app`). NOT deployed to SKS prod — gated on Ben Ritchie sign-off + Royce explicit go. 5 modified, 3 new files, ~1130 line diff.

## [2026-05-13] v3.4.68 — Phase B + C role system foundation (DEMO ONLY soak)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.68-role-system-clean` → `demo` (PR #63)
**Changes:**
- `scripts/permissions.js`: new `resolveSessionRole()` (Phase C).
- Call wired into `initApp()` + supervisor PIN unlock + lock-out.
- 5 handler gates migrated to `EQ_PERMS.can()` (Phase B v1):
  - `leave.js`: `respondLeave` / `archiveLeaveRequest` / `unarchiveLeaveRequest`
  - `timesheets.js`: `fillTsWeekFromMon` / `sendTsReminder`
- All 5 perms behaviour-preserving in both supervisor + manager tiers.
- Phase A schema applied to BOTH Supabase projects on 2026-05-13.
**Why:** Royce flagged Phase B+C risk on SKS prod; chose to ship to demo this week for a 5-7 day soak before porting. PIN-unlock-wins rule preserves today's behaviour — anyone with the supervisor PIN keeps full supervisor access regardless of DB role. Phase D will tighten this server-side later (~2 weeks, planned early June).
**Status:** Demo only. SKS stays on `isManager` binary model until demo soak passes. Plan ref: `MELBOURNE-SCALE-DESIGN.md §7 Q3`.

## [2026-04-28] Add Contact button cherry-picked to main (SKS) — PR #25
**Built by:** Royce Milmlow + assistant
**Branch:** `fix/add-contact-main` → `main` (merge commit `4f03227`,
cherry-pick of `f372a43` from demo)
**Why:** Same repo Milmlow/eq-field-app; demo branch deploys to
eq-solves-field.netlify.app (EQ Field demo), main branch deploys to
sks-nsw-labour.netlify.app (SKS LIVE — ~55 staff). The button only
shipped to demo via PR #24, so SKS staff didn't get it. Cherry-pick
brings just that one-line UX fix to main without dragging the rest
of Phase 1 (flags, perms, project-hours, role enum) onto SKS.
**Status:** Merged. Netlify auto-deploy to sks-nsw-labour.netlify.app
in flight at 2026-04-28.

## [2026-04-28] Add Contact button wired into Contacts page (PR #24)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/hopeful-wright-058c8b` → `demo` (merge commit `5105517`)
**Changes:**
- `index.html` page-contacts filter row gets a "＋ Add Contact"
  button calling existing `openAddManager()` (managers.js:109).
  No new code paths — reuses the existing modal-manager + saveManager
  flow that already lived on the Supervision page.
- Both demo (SEED) and live (eq) tenants get the button — `managers`
  is in `ORG_TABLES`, not in any `TENANT_DISABLED_TABLES` entry.
- One-line diff to a single file. No JS changes, no migration, no
  permission shape change.

**Why:** The page-contacts page (nav: "Contacts" ◉) showed staff/people
but lacked an Add affordance — anyone looking for "where do I add a
contact" landed there and saw nothing. Add button only existed on
page-managers (nav: "Supervision" ☎). UX parity fix.

**Status:** Live on eq-solves-field.netlify.app post-Netlify-deploy
(~1 min after merge).

## [2026-04-27] Phase 1 implementation kickoff — flags, perms helper, migrations
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/hopeful-wright-058c8b` (not merged to demo — awaiting review)
**Changes (5 commits past `0145c78`):**
- `e9b4706` — `scripts/flags.js` PostHog feature-flag wrapper exposing
  `window.EQ_FLAGS.isEnabled()` + `variant()`. Safe defaults, no-op until
  a flag is created in the EQ PostHog project (`phc_zXpRxm6Q…`).
- `f2d0e91` — `scripts/permission-matrix.js` + `scripts/permissions.js`.
  Matrix v1 embedded as static JS; `window.EQ_PERMS.can(permKey)` reads
  the current role.
- `8b6bdb1` — Two SQL migrations written (NOT applied):
  - `migrations/2026-04-27_sites_track_hours.sql` — `track_hours` boolean
    + `budget_hours numeric` on `public.sites`
  - `migrations/2026-04-27_eq_role_enum_people_role.sql` — `eq_role`
    Postgres enum + `people.role` column with manager-table backfill
    pattern. Header includes verification queries to run before applying.
- `b367eb1` — `EQ_PERMS.getRole()` reads `window.isManager` as primary
  today-path role signal (durable for page lifetime), falling back to
  sessionStorage flags. Plan revised: 97 `isManager` references across
  `scripts/`/`index.html` rules out a wholesale refactor — strangler
  pattern instead, migrate opportunistically when touching files.
- `89f96dc` — `scripts/project-hours.js` + placeholder div before
  `</body>`. Self-mounting "Project Hours" burn-down panel — activates
  only when `feat_project_hours_v1` flag is on AND `EQ_PERMS.can('ph.view_dashboard')`
  is true. Renders per-site Budget / Used / Remaining / % used with
  colour treatment (sky / amber / red). Graceful states for "migration
  not applied yet", "no tracked sites", and network errors. Client-side
  aggregation over timesheets for v1.

**Next manual steps required (Royce):**
- Create `feat_project_hours_v1` flag in EQ PostHog project (default off,
  cohort = your `distinct_id` only)
- Apply both migrations to `ktmjmdzqrogauaevbktn` via Supabase MCP /
  Studio after running the verification queries in the role-enum header.
  Do NOT apply to `nspbmirochztcjijmcrx` (SKS live).
- Open PR `claude/hopeful-wright-058c8b` → `demo` when ready to merge.

**Status:** Code shipped to feature branch only. No Netlify deploy. No
Supabase changes. SKS Labour untouched.

## [2026-04-27] Multi-tenancy + dev-workflow plan locked (planning only, no code shipped)
**Built by:** Royce Milmlow + assistant
**Changes:**
- Living plan document captured at
  `eq-solves-field/.claude/worktrees/hopeful-wright-058c8b/MULTI-TENANCY-PLAN.md`.
- Three strategic decisions locked:
  - Sprint scope = Phase 1 only (PostHog flags + project-hours feature + 5-tier
    role system). Phase 2 deferred to first self-serve trial signup OR ~3
    customers manually provisioned.
  - Tenancy lives inside `ktmjmdzqrogauaevbktn` only; SKS Labour
    (`nspbmirochztcjijmcrx`) untouched.
  - Auth: Supabase-native JWT minted in `verify-pin.js` with
    `app_metadata.tenant_id` and `app_metadata.eq_role`; PIN UX preserved.
- Tenant URL convention locked: `eq.solutions/field/<slug>/`. Path-based slug
  resolution, single shared Netlify site, no subdomains.
- 5-tier role system designed (`manager > supervisor > employee > apprentice >
  labour_hire`) with `eq_role` Postgres enum and `people.role` column.
- Single PIN per tenant on `organisations.tenant_pin`; per-role PIN env var
  pattern dropped.
- Permission matrix HTML built at
  `eq-context/eq/field/permissions/permission-matrix.html` plus v1
  JSON snapshot at `permissions-by-role-v1.json` (manager 56 / supervisor 36 /
  employee 13 / apprentice 17 / labour_hire 5).
- First PostHog flag designed: `feat_project_hours_v1` gates new project-hours
  burn-down feature with `sites.track_hours` + `sites.budget_hours`.

**Status:** Plan complete. No code touched. Phase 1 implementation pending
explicit Royce go-ahead.

## [2026-04-05] Demo Mode, Seed Data and Network Error Suppression
**Built by:** Royce Milmlow + assistant
**Changes:**
- Demo mode implemented - bypasses Supabase auth when tenant slug is eq
- 18 generic staff, 7 generic sites, 5 weeks of schedule seeded
- Network error toasts suppressed in demo mode
- Cowork guardrail issue documented
**Status:** Live on eq-solves-field.netlify.app (demo branch)

## [2026-04-05] Cloudflare Pages Deployment Architecture Locked
**Built by:** Royce Milmlow + assistant
**Changes:**
- Deployment architecture confirmed and locked
- Rule: never cross-deploy between targets
**Status:** Architecture documented

## [2026-04-04] Redundancy and Failover Gap Assessment
**Built by:** Royce Milmlow + assistant
**Changes:**
- Full infrastructure assessment across Netlify, Supabase, Resend, GitHub
- Gaps identified: Supabase single point of failure, no backups, no tagged release
**Status:** Gaps identified - NOT yet resolved

## [2026-03-31] White-Label Commercialisation Review
**Built by:** Royce Milmlow + assistant
**Changes:**
- EQ Field Ops commercialisation roadmap built (85-item Excel workbook)
- White-label conversion estimated at 2-3 hours
**Status:** Planning complete - not yet executed

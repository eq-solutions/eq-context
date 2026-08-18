---
title: EQ Intake — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-18
scope: EQ Intake engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Intake — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)
- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---

## eq-solves-intake: the data-cleaning queue actually shrinks as you work it now, plus a bad-merge error fixed (2026-08-16)
*Royce flagged three problems with the review queue from screenshots: decided duplicate rows just sat there cluttering the list forever with no way to fix a wrong answer, a duplicate-contacts merge threw a raw error on screen, and the "unknown trade" list had no way to fix several people at once. Built and merged, then self-reviewed the same work and fixed six more bugs the review turned up before calling it done.*

- [x] The duplicate-contacts merge crash is fixed — clicking "confirm merge" on a pair already merged elsewhere used to throw a raw error with no way out; it now just shows "already merged" and moves on.
- [x] Deciding on a duplicate (same/different) now actually removes it from the working list instead of cluttering the screen forever — and there's a "change answer" link if a decision needs correcting.
- [x] The "trade unknown" list can now be fixed in bulk — tick several people, pick one trade, approve them all in one click, instead of one at a time.
- [x] Self-review of that work (two independent passes) found six more real bugs before shipping: a stale note that could attach itself to the wrong answer, a leftover draft note that could reappear, a bulk-approve button that could silently do nothing, and a bulk-approve failure that hid the actual reason it failed. All six fixed and confirmed working live, not just typechecked.
- [x] eq-solves-intake [PR #116](https://github.com/eq-solutions/eq-solves-intake/pull/116) and [PR #117](https://github.com/eq-solutions/eq-solves-intake/pull/117), both merged, CI green.

**Deferred:**
- [ ] **A merged duplicate can still show up looking "active" again after a page reload** — the screen doesn't fully know a pair was already merged until it's clicked into once. The real fix needs a small database change in EQ Shell (not this app), so it's fully scoped (exact change, which table, which migration number) but deliberately not built yet — spun off as its own follow-up rather than done inside this session, per Royce's call to leave it for that follow-up to pick up. _(added 2026-08-16)_

---

## ⏩ Session close — 2026-08-08 (eq-intake) — suite-wide Intake role audit, 4 decisions made

*Followed the Overview/To Do polish pass (#111) and the fuzzy-match Reconcile fix (#112) with a cross-repo audit of where `@eq/intake` actually gets used across the suite — verified live against eq-shell, eq-solves-service, eq-field, eq-cards, not assumed from docs. Shipped the one clean win (eq-shell's Contacts dedup now reuses Intake's matcher instead of a private copy, #1287) and walked the rest of the gap list through with Royce one by one.*

**Completed:**
- Published a suite-wide "where does EQ Intake actually get used" report (per-app verdicts, a relationship diagram, ranked gaps, ranked advice) — built off 4 parallel research agents checking real code in eq-shell, eq-solves-service, eq-field, eq-cards rather than assuming from docs.
- `suite-state.md` "What Owns What" gained an Import/write-time tooling row — Intake was previously undocumented as a suite component.
- eq-solves-intake [PR #113](https://github.com/eq-solutions/eq-solves-intake/pull/113): exported `dice`/`identityKeyFor`/`HIGH_SIM` from the public barrel (prerequisite for reuse elsewhere).
- eq-shell [PR #1287](https://github.com/eq-solutions/eq-shell/pull/1287): re-vendored `eq-intake/eq-platform` (picked up #111/#112/#113) + swapped `CustomersPage.tsx`'s private Dice matcher for the shared one. Merged, live on `core.eq.solutions`.

**Decided (Royce, this session):**
- **EQ Ops's PDF imports (quotes, subcontractor pricing, labour-hire) stay a separate Claude-direct pipeline, not migrated onto Intake.** Deliberate — pricing-table extraction from supplier PDFs is a different problem than entity reconciliation. Not an oversight; don't re-flag as a gap.
- **EQ Service's four importers (commercial-sheet, asset-register, Jemena RCD, Maximo Delta WO) are NOT being migrated onto Intake's path.** The 2026-05-19 `docs/architecture/2026-05-19-shell-intake-integration.md` plan stays unexecuted by choice, not neglect — Royce's gut ("is there value in changing what's working?") plus a real technical reason: Service's own Levenshtein job-plan-code matcher solves a differently-shaped problem (short codes, not names) than Intake's Dice matcher, so the clean-swap case that justified the eq-shell fix doesn't hold here. Don't re-propose the full migration without a new reason (a live bug, not architecture tidiness).
- **ABN validation in EQ Service: not now.** Flagged as a cheap, independent, zero-risk win (Service stores/displays ABN but never validates it) — Royce declined for now. Revisit if it ever causes a real problem.
- **`enrich.ts`/`dedup.ts` in eq-intake stay dormant — not required at the moment.** Investigated properly first (the 2026-07-02 backlog note calling them "unused" was wrong — they're real, wired into `@eq/confirm-ui`'s `store.ts`, tested, and hardened against a real past incident, issue #47). Checked eq-solves-service's actual asset-register importer as the natural consumer: it already does its own exact-match duplicate detection (Asset #/name, both within-batch and against-existing) — so no gap there beyond a missing serial-number check. It does **zero** AI gap-filling though: `criticality` and `ppm_frequency` are never set on newly-imported assets (asset_type is fine, sourced from the job-plan link). That's the one genuinely real, unaddressed opportunity here — Royce's call was to leave it for now regardless. Don't re-raise without a reason someone actually needs criticality/ppm_frequency populated.
- **`ANTHROPIC_API_KEY` on sks-canonical: not yet.** Still the blocker for Intake's Ask tab / gap-suggest / AI-adjudication. Royce's call, not a build task. _(long-open item, unchanged — see the 2026-07-02 block below)_

---

## ✅ EQ Intake — the duplicate console became a decision surface (2026-07-14, BUILT + MERGED + APPLIED FLEET-WIDE + LIVE-VERIFIED)
*The write-time resolver (0179) caught dupes and the console (#67) showed them, but read-only — a human could SEE a flagged duplicate, not DECIDE. This closes the loop: every flagged row is now adjudicable (Same/Different/Unsure), and the verdict is captured as an append-only LABEL — the fuel a future match model learns from. Records the human's call only; merges nothing. The jump from "a report" to "a decision surface", and step one of the learning flywheel.*
- [ ] **Seed one realistic flagged pair on ehow for a hands-on demo.** Console currently has 0 flagged rows — nothing real has tripped the write-time resolver yet, so there's nothing to click through end-to-end. Offered to insert one synthetic advisory row; correctly blocked by the auto-mode classifier as a write to shared production SKS data without Royce's explicit go — needs his yes. _(added 2026-07-15)_

---

## ✅ EQ Intake — duplicate-site detector was blind to inactive rows (the SY9 silent-failure) (2026-07-13, MERGED + DEPLOYED)
*The SY9 customer silently vanished from Service because its one correctly-linked site row was inactive, and the "Scan for possible duplicates" tool filtered inactive rows out before clustering — so the tool meant to catch it couldn't see it. Live SY9 data reconciled by hand first (activated the correct row, retired 3 dupes, repointed 8 roster entries + 1 quote onto the survivor).*
- [ ] **3 site pairs/groups still need Royce's manual pick, not auto-seeded: SYD10, SYD11, M5 Motorway East.** Plus the 3 three-row groups (North Shore/Port Macquarie/St George Private Hospital) — no clear 2-way survivor without a human choosing. Now that usage-check (below) is built, these might resolve automatically once it's applied — re-check before assuming they still need manual review. _(added 2026-07-16)_

---

## ✅ EQ Intake — write-time site resolver (advisory) shipped + duplicate estate healed (2026-07-13, MERGED + APPLIED LIVE)
*The companion to the SY9 detector fix: instead of only catching dupes on a dashboard scan after the fact, a check now sits at the moment a site is BORN. Advisory mode — it records what it would decide, merges/blocks nothing — so the open "how strict is a match" call gets made on real evidence, and it can't over-confidently merge two real sites. Plus the existing duplicate estate (SY3–SY7, SY1/2) healed.*
- [ ] **Enforcing phase + the match-key decision — DEFERRED, gated on advisory evidence.** The resolver only WATCHES today. Flipping it to enforce (redirect a duplicate write onto the existing site) is a later one-branch change, and it needs Royce's business call on how strict a match is — address-match-now vs mandate-a-canonical-code (the eq-shell#781 fork). Let `app_data.site_resolution_advisory` fill on ~2 weeks of real traffic first; that count is also the CEO-facing "duplicates prevented" metric (`select outcome, confidence, count(*) … group by 1,2`). **Update 2026-07-14:** the console is now adjudicable (0183) — human verdicts accumulate in `app_data.site_resolution_verdict`, so the match-key call can be made on *labelled* evidence (and eventually self-calibrate) rather than raw advisory counts. See the 2026-07-14 learning-loop section at top. _(added 2026-07-13)_

---

## ⏩ Session close — 2026-07-03 (eq-intake, steward session) — steward run 001 + review-queue tab SHIPPED end-to-end (PRs #54/#55 + shell #606, live on core.eq.solutions)

*Same thread as the 2026-07-02 "dashboard audit + health-score fix" block below — continued through the steward remediation run, the queue build, and the production ship.*

**Completed (all live and verified):**

**Decided (Royce):**
- Steward authority: fix-or-queue, one-sentence-defensible commits only, never merge/delete duplicates — 19/21 committed, 2 dropped by adversarial review.
- "You do the SQL yourself / merge the rest / no mistakes" → agent applied 062 + merged PR #55; Royce merged #606 himself over the (diagnosed-unrelated) red gate and ran the ledger backfill when the classifier held the agent out.

**Deferred (added 2026-07-03):**
- [ ] **Work the 137-item review queue** — the tab is live; trades/links/formats are one-click, emergency contacts need info Royce has to source. _(added 2026-07-03, needs your call)_
- [ ] **sql/061_steward_commit_batch.sql — staged, NOT applied** — server-side `eq_steward_commit_batch` RPC (service-role-only, whitelist + event lifecycle inside) for steward run 002; apply when a second run is wanted. _(added 2026-07-03)_

**Notes (load-bearing):**
- **After 0156, `app_data.eq_remediation_queue` is service-role-only (no browser grants/policies)** — the queue UI works ONLY through the 062 SECURITY DEFINER RPCs (`eq_queue_list/open_event/close_event/resolve`, JWT-tenant-scoped, `authenticated`-granted). Never add direct table reads from the browser; that's the 0156 posture.
- **eq-intake ledger self-inserts must stamp `checksum='eq-intake-lineage'`** (PR #58 convention) or every eq-shell PR goes red via #608's CHECK 3.
---

## ⏩ Session close — 2026-07-03 (eq-intake) — guardian go-live EXECUTED on ehow; alert pipeline live end-to-end (PRs #59/#60/#61)

*Second close for this thread — the earlier block below ("licence strip trust failure") built the fixes; this one ran the production go-live and hardened it live.*

**Completed (all live on ehow, each step verified):**

**Decided (Royce):**
- "Authorize me here" → agent runs the prod applies/deploys for this chain (per-action classifier sign-off pattern worked: each new prod action re-asked).
- Nightly cron at **03:00 AEST** (pre-dawn, results ready before the workday).
- Deploy v3 + re-smoke: approved.

**Deferred (added 2026-07-03):**
- [ ] **Fix 12 contacts missing first/last name** — surfaced by the first accurate health run (contacts 206/218 complete); the dashboard tidy flow can fix them one by one. _(added 2026-07-03)_
- **Note, not a new item:** the go-live applies added three more hand-inserted `_eq_migrations` rows (**058/059/060**, via the INSERTs inside the merged migration files) to the set covered by the already-open decision item in the steward-drift block below ("Decide handling for guardian go-live hand-inserted ledger rows") — same options, now 058–060 + 062.

**Notes (load-bearing):**
- **ehow gotcha:** the platform-injected `SUPABASE_SERVICE_ROLE_KEY` inside Edge Functions is NOT byte-identical to the dashboard's legacy service_role key on this project. Never gate on string equality with it — prove privilege via a service_role-only RPC (pattern now in quality-guardian).
- **Key-safe smoke pattern:** fire the same `net.http_post` the cron runs (Authorization read from `vault.decrypted_secrets` inside the DB) via MCP `execute_sql` with `{"triggered_by":"manual"}` — prod keys never pass through chat/transcript.
- The dashboard-side `health-score.ts` field lists were already correct (verified 2026-06-24) — the guardian's inline copy had drifted from day one (PR #33).
---

## ⏩ Session close — 2026-07-02 (eq-intake) — dashboard audit + marketing brief + health-score fix

**Completed (eq-intake, repo `eq-solves-intake`, PR #53 merged to main):**

**Decided:**
- Royce chose the "commit fix #1, then live-test #2" path over building further ideas blind.
- Rubric-ranked idea #9 (cross-app "Dispatch Readiness" dimension pulling in Field data) scored lowest despite highest strategic alignment — blocked by Field's schedule/timesheet tables being empty and by cross-repo/cross-schema scope; not worth building yet.

**Deferred (added 2026-07-02):**
- [ ] **Verify `ANTHROPIC_API_KEY` is actually live on sks-canonical for the Ask tab** — code is real and correctly wired, but no Edge Function invocations in the last 24h of logs; needs Royce to type one question into the live Ask tab and report back. _(needs your call)_
- [ ] **Wire up or delete `enrich.ts` / `dedup.ts`** — both fully built, exported, unused. _(added 2026-07-02)_
- [ ] **Health score history/trend** — no time-series snapshot exists; score is point-in-time only, no way to show "up/down since last week." _(added 2026-07-02)_
- [ ] **Lineage/provenance in EntityDrillDown** — `commitBundleToCanonical` already captures `sourceFilename`; not surfaced in the UI. _(added 2026-07-02)_
- [ ] **(big swing) Nightly digest cron** — reuse the `PRE_VISIT_BRIEF_CRON` pattern to push a daily score-delta + top-3-actions email instead of requiring the dashboard to be opened. _(added 2026-07-02)_
- [ ] **(big swing) Autopilot batch gap-fill** — `gap-suggest.ts` already does AI per-field suggestions one row at a time via `EntityDrillDown`; batch it so e.g. "68 staff missing trade" can be approved in one sitting. _(added 2026-07-02)_
- [ ] **(big swing, lowest-ranked) Cross-app "Dispatch Readiness" dimension** — extend the health score past Intake's own tables to include Field's schedule/availability emptiness; also the natural next step for suite-wide "ask anything" via the same Edge Function pattern. _(added 2026-07-02)_

**Notes (load-bearing):**
- **eq-solves-intake has at least 3 live working trees**: the main checkout `C:\Projects\eq-intake`, worktree `jovial-rubin-0d0004`, and worktree `nifty-feynman-7e97ce` (this session's). Mid-session I accidentally edited the main checkout instead of the assigned worktree — caught it before committing (the main checkout had unrelated uncommitted work from another process on `feat/armada-sprint-polish`: `.armada/config.json`, several `vite.config.ts`/`vitest.config.ts` files, a new untracked `eq-platform/apps/` — none of it mine, all left untouched), reverted my two accidental edits there, redid them in the correct worktree. Future eq-intake sessions should double-check `pwd`/git branch before editing when multiple worktrees are active.
- **`@eq/intake`'s published types come from `dist/index.d.ts` (tsup build), not source** — editing `src/*.ts` in this package requires an `npx tsup` rebuild before consuming packages like `eq-intake-demo` will see the new types; the package `node_modules/@eq/intake` is a workspace symlink to source, but `package.json#types` points at `dist`.
- **This worktree (`nifty-feynman-7e97ce`) had no `node_modules` installed at all** — needed a temporary (accidentally non-symlink, actual-copy) `node_modules` to typecheck; cleaned up after. If revisiting this worktree, either run `pnpm install` properly or symlink carefully (confirm with `fsutil reparsepoint query` that `ln -s` actually produced a link, not a copy, on this machine).
---

## ⏩ Session close — 2026-06-30 (ARMADA on eq-intake) — pre-bake + 4 clean fleet cycles

**Completed (eq-intake / repo `eq-solutions/eq-solves-intake`, all merged to main):**

**Decided (Royce):** set ARMADA up on eq-intake; hand-merge the cycle output as it goes; on #46, investigate-then-remove the app duplicates (not fix); wrap polishing once library verified clean.

**Deferred (added 2026-06-30):**
- [ ] **Arm crows-nest `/loop` on eq-intake** — 4 clean manual cycles now observed; still needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`) + Royce's go _(added 2026-06-30)_
- [ ] **Add `test:` gate** to eq-intake `.armada/config.json` (e.g. `pnpm -C eq-platform test`) — unit tests green across packages, just not wired into the fleet gate yet _(added 2026-06-30)_
- [ ] **(optional, needs your call)** Harden build-before-test workspace-wide so the stale-dist bug class (root of #47) can't recur — source-resolution or build-ordering across all packages _(added 2026-06-30)_
- [ ] **(optional, needs your taste)** Archive stale root planning docs (`PLAN-*`, `OVERNIGHT-REVIEW-*`, `CONDUIT-AUDIT-*`) into `_archive/` _(added 2026-06-30)_

**Notes (load-bearing):**
- eq-intake has **no root `package.json`** — the pnpm workspace lives in `eq-platform/`; fleet gate = `pnpm -C eq-platform check:packages`. **CI workflow added 2026-07-12** (`.github/workflows/ci.yml`, PR #64) — see the 2026-07-12 session-close entry below; this note previously said "no CI workflows in the repo", which is why it's corrected here rather than left stale.
- Vendored ARMADA skills are **local-only in the main checkout** `C:\Projects\eq-intake\.claude\` — run ARMADA from a session rooted at the repo root, NOT a `*-wt` worktree, or `/lighthouse` etc. won't resolve.
- PHASE-0 monorepo migration is **abandoned**; `apps/eq-service`/`apps/eq-shell` are gone from eq-intake. eq-service = `eq-solves-service` repo, eq-shell = `eq-shell` repo (live, shipping daily).
---


---
title: EQ Intake — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-15
scope: EQ Intake engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Intake — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

**Budget:** ~500 lines. `- [x]` items already auto-rotate out nightly via `scripts/rotate_pending.py`; past this line count even so, propose moving the oldest stale open items to `eq/pending-archive.md`. (`rules/tidy-protocol.md` Step 5, 2026-09-07.)

---

## eq-solves-intake: apply-migrations.mjs retired — resolves the eq_migrations/_eq_migrations ledger question from the entry below (2026-09-15, third session same day)
*Closes the still-open question the entry below names at its line 30 (`task_36ed655a`) — reached via a separately-spawned copy of the same question (`task_56b3f80c`), also started by Royce. See the load-bearing note below: this was independently duplicate-spawned, not a planned follow-up.*

**Completed:**
- Investigated via git archaeology: `app_data._eq_migrations` (leading underscore) is the real, live ledger — every migration 013–065 inserts into it, `sql/README.md` confirms it's shared with eq-shell ("the One Pipe"), and CLAUDE.md Rule 1 names it correctly. `scripts/apply-migrations.mjs` (created 2026-05-28, commit `f6f2f91`) tracked a separate, self-invented `app_data.eq_migrations` (no underscore) instead — wrong from the day it was written (two days *after* the underscore convention was already established by migration 013), not a later drift.
- Ran `/brief` before any edit (this session's first `Edit` call was correctly blocked by the brief-gate hook — hadn't run it yet). Surfaced: `digest.md` 3 commits behind at read time; the live, unrelated `_eq_migrations` row-corruption on `eq-tenant-madagins` (already owned, untouched here); branch `claude/retire-stale-migration-script` (different file — `migrate-cards-to-canonical.mjs` — no overlap, checked directly).
- Mid-brief, found the concurrent session's fix (`03188fa`, for `sql/seed-schemas.ts`'s identical missing-dependency bug) had incidentally made `apply-migrations.mjs`'s import resolve too. Re-verified live, then dropped "it doesn't even run" from the reasoning — the Rule 2 policy violation (self-applying to live tenant planes via a shadow ledger table) was the real, load-bearing reason regardless of whether the import happened to work.
- Royce confirmed the brief ("go ahead"). Deleted `scripts/apply-migrations.mjs`; removed its `migrate`/`migrate:dry` scripts from `eq-platform/package.json`; rewrote `SPRINT-SUMMARY.md`'s migration-apply docs to point at eq-shell's `tenant-migrate.yml` pipe per Rule 2.
- Closed the live-DB question definitively once a Supabase MCP connection became available mid-session: `execute_sql` against `information_schema.tables` confirmed on **both** ehow and zaap that `app_data.eq_migrations` (no underscore) was never created on either — the script never successfully ran, anywhere, ever.
- Committed (`053c4f4`, only the 3 relevant files — left the working tree's unrelated `.claude/settings.local.json` edit untouched) and pushed to `main` on Royce's explicit "push it". `origin/main` tip confirmed as `053c4f4`.

**Deferred:**
- [ ] **Migration 033's `app_data.eq_exec_sql` RPC (SECURITY DEFINER, arbitrary-SQL exec) is now orphaned** — it existed only to support `apply-migrations.mjs`, now deleted. Low risk (already gated on the service-role key), but dropping/revoking it is a live-plane DDL change that belongs in eq-shell's migration pipe per Rule 2, not a drive-by here. _(added 2026-09-15)_

**Notes (load-bearing):**
- **This was independently duplicate-spawned work — not a planned follow-up.** The entry below logs this exact question as `task_36ed655a`, "Royce started it separately, still running as of that close." This session's copy of the same question was spawned separately as `task_56b3f80c` — also started by Royce (`dismiss_task` confirmed: "already started by the user"). Tried to find and message the `task_36ed655a` session before writing this: `ListAgents` showed a live `eq-solves-intake-50 [fc2d0d]` peer (started ~12h ago), but `list_sessions` had no title match for it — the same wall the entry below already hit trying to reach a different peer. **If `task_36ed655a`'s session is still active: this is already done.** `app_data.eq_migrations` vs `_eq_migrations` is resolved, `scripts/apply-migrations.mjs` is deleted, `053c4f4` is live on `origin/main` — re-doing this would be wasted work at best, a conflicting decision at worst.
- **Distinguish from the entry below's `seed-schemas.ts` call** ("wire it up" — add the dependency, don't retire). That was Royce's answer for a *different* script doing a different job (schema-registry seeding, not live-plane migration apply). `apply-migrations.mjs`'s retirement wasn't a "does it run" call, it was a Rule 2 policy call (`sql/` is staging-only, not self-serve applyable to live tenant planes) — the two scripts landing on opposite fates is deliberate, not inconsistent.

---

## eq-solves-intake: seed-schemas.ts's missing dependency fixed and shipped — closes the deferred item in the entry below (2026-09-15, second session same day)

*Closes the `sql/seed-schemas.ts` deferred item in the schema-sync entry directly below — reached independently, in a separate concurrent session working the same repo. Royce answered the "add the dependency vs. retire the script" question directly (structured question, not the background task that entry names): **wire it up.***

**Completed:**
- Added a `package.json` at the eq-solves-intake repo root — `@supabase/supabase-js` + `tsx`, a `seed:schemas` npm script. This is the correct fix location, not a stylistic choice: `eq-platform/` is a **sibling** of `sql/` and `scripts/`, not their ancestor, so nothing installed inside `eq-platform` (a pnpm workspace of its own, `packages/*` only) is ever on Node's module-resolution path for either directory. `demos/package.json` already proved the standalone-package.json pattern works in this repo.
- Same fix, confirmed as a side effect (identical unresolvable import, same directory): `scripts/apply-migrations.mjs` — this repo's actual `migrate`/`migrate:dry` runner — now runs (`--dry-run` lists all 54 migrations instead of `ERR_MODULE_NOT_FOUND`). `scripts/migrate-cards-to-canonical.mjs` shares the identical import; not exercised live (it writes real data).
- Updated `sql/seed-schemas.ts`'s header comment to the working run command. Committed (`03188fa`, only the 3 relevant files — left the working tree's unrelated `.claude/settings.local.json` edit untouched) and pushed to `main`.
- Verified live: `npm run seed:schemas` now reaches the real `SUPABASE_URL`/`SUPABASE_SERVICE_KEY` guard instead of dying at import.

**Notes (load-bearing):**
- **Likely duplicate/conflicting concurrent work — needs Royce to check, not something this session could resolve itself.** The entry below spawned `task_d667cade` for this exact question ("add the dependency vs. retire the script"), started by Royce in a separate local session, in this same shared (non-worktree-isolated) checkout. As of this close, that checkout still shows live unstaged changes this session didn't make — `eq-platform/package.json` modified, `SPRINT-SUMMARY.md` modified, `scripts/apply-migrations.mjs` deleted — consistent with a background session still mid-implementation of the same fix, independently of Royce's direct answer here. Two risks if so: (1) duplicated effort on an already-shipped, already-verified fix; (2) if its approach adds the dependency to `eq-platform/package.json` specifically, that can't work for the reason above (sibling, not ancestor) — it would look plausible and still not fix `sql/seed-schemas.ts`. Tried to identify and message that session directly (`ListAgents` showed two live `eq-solves-intake` peers; `list_sessions` couldn't positively resolve either to a session id) — couldn't reach it with confidence, flagging here and to Royce directly instead of guessing.
- Separate, still-open, unrelated question spawned this session: `apply-migrations.mjs`'s own docstring says it tracks migrations in `app_data.eq_migrations` — this repo's own `CLAUDE.md` Rule 1 says the single ledger writer is `app_data._eq_migrations` (leading underscore, eq-shell's). Same table under drifted names, or two unrelated tables — not established. Spawned as `task_36ed655a`, Royce started it separately, still running as of this close.

---

## eq-solves-intake: schema-sync CI gate added; site.schema.json customer_id reconciled; two stale script/doc references fixed (2026-09-15)
*Closes the follow-up flagged in the 2026-09-14 contact.schema.json close below (`task_cd08e566`) — "this repo keeps two hand-maintained schema copies with no automated check they stay in sync." Built the check, then used it to find and fix live drift the same session.*

**Completed:**
- Investigated before assuming a simple "keep two copies in sync" fix would fit: root `schemas/` (34 files) and eq-platform's vendored `packages/eq-schemas/src/schemas/` (46 files) share only 16 filenames — 18 root-only (intake-only CMMS entities), 30 eq-platform-only (quoting/labour-hire, for other apps). Neither generates from the other. Ruled out a single-source-of-truth restructure on that basis.
- Shipped `scripts/check-schema-sync.mjs` (structural JSON diff over the 16 shared names, ignores harmless key reordering) + `scripts/schema-sync-exceptions.json` (justified, dated carve-outs) + a new independent `schema-sync` CI job. `main` @ `abd33db`.
- Running it immediately found live drift on `site.schema.json`'s `customer_id` — the field the 2026-09-09 close below deliberately left out of scope. Verified live via Supabase MCP against ehow + zaap rather than guessing: root's `x-eq-fk-fuzzy-match-on` field `code` is real but 0% populated on both live tenants (0/49 ehow, 0/50 zaap), `customer_entity_legal_name` doesn't exist as a column at all; eq-platform's `company_name`/`external_id` are both real and populated (90% on ehow). Also traced `@eq/validation`'s `fk-resolver.ts` and confirmed the `customer.`/`customers.` table-name prefix is discarded entirely at runtime (`.split('.').pop()`) — the real question was always column names, not the prefix people had been going back and forth on. Reconciled root to match eq-platform exactly, regenerated `types/site.d.ts`. `main` @ `6d0c55b`.
- Two adjacent stale references found while tracing which code actually consumes root `schemas/`, fixed separately: `sql/seed-schemas.ts`'s `SCHEMA_DIR` resolved outside the repo entirely (looks relocated at some point without updating the path math); `edge-functions/api-intake/index.ts`'s integration-builder doc comment still pointed at the pre-rename `eq-intake` GitHub path. `main` @ `bfe33ef`.
- All three commits pushed; CI green on both jobs (run `34883822939`, 1m27s build + 11s schema-sync).

**Deferred:**
- [ ] **`sql/seed-schemas.ts` still can't actually run even with its path fixed** — `@supabase/supabase-js` isn't a dependency anywhere in eq-platform's pnpm workspace or at the repo root, so the import fails before any of the script's own logic runs (confirmed safely: ran it with fake, non-resolving credentials, fails at module resolution before any network call). eq-platform already has a differently-designed, currently-wired alternative (`db-apply.ts`, generates SQL to paste into the Supabase SQL editor). Needs a decision — add the dependency and wire up an npm script, or retire this script — not picked unilaterally. Spawned as `task_d667cade`; Royce started it in a separate session, still running as of this close. _(added 2026-09-15)_

**Notes (load-bearing):**
- **The "two hand-maintained schema copies" problem is now guarded, not just fixed once more.** `check-schema-sync.mjs` runs on every push/PR; the 4 manual reconciliations in the 6 days before this session (this file's 2026-09-09 and 2026-09-14 entries, plus `asset.schema.json`) should be the last ones needed for *silent* drift specifically. A genuinely contested field still needs a human/live-data call and an entry in `scripts/schema-sync-exceptions.json`, not a bypassed check.
- **Root `schemas/` has fewer live runtime consumers than this file's own 2026-09-14 entry implied.** `edge-functions/api-intake/index.ts` only references the schema path in a doc comment — it doesn't load the file. Worth checking before assuming a root schema edit reaches a running edge function without a redeploy of something else.
- **This session's `/brief` flag used the pre-fix, dated filename** (`eq-brief-<date>-<session-id>.flag`), even though `close.md`'s Step 6 expected the dateless format. Not a real doc inconsistency: a concurrent eq-field session's 2026-09-15 log (third entry, same file) confirms the dated format was deliberately dropped mid-day to fix a local-vs-UTC day-boundary bug, and that a fresh `/brief` load picks up the corrected format automatically. This session's second `/brief` call returned "instructions unchanged" — Skill-tool caching served this session's original (pre-fix) copy both times, not a live discrepancy between the two docs. This close deletes both possible filenames to be safe regardless.

---

## eq-solves-intake: contact.schema.json's customer_id reverted to nullable — corrected a same-day-scoped regression from fdf0055 (2026-09-14)
*Spotted in passing while fixing an unrelated fixture-drift bug (PR #124). `contact.schema.json` required `customer_id` as a non-null string — contradicted eq-shell tenant-migration 0035 (2026-06-03, governed One Pipe), which deliberately dropped NOT NULL on `app_data.contacts.customer_id` fleet-wide because SKS legitimately has contacts with no customer link. Investigated fully rather than assumed either side was right.*

**Completed:**
- Read the intake commit path (`commit-canonical.ts`'s `resolveCustomerFk`) — confirmed it already gates unresolvable rows into explicit `fk_no_match` rejections before they reach schema validation, independent of the schema's `required` array. This fix doesn't touch that gate.
- Found two independently-shipped, currently-live write paths that assume nullable: `eq_upsert_contact` (migration 0245, the RPC behind Shell's own "add contact" UI) defaults `p_customer_id` to `NULL` with no guard; `eq_tidy_orphan_check` (adopted via migration 0304) treats `customer_id IS NULL` as a normal, correctable state, not a broken one.
- Discovered, via the mandatory `/brief` gate, that a same-day commit (`fdf0055`, 2026-09-09) had already flipped this exact field to required/non-null, citing a live check against ehow — a direct contradiction with migration 0035. Traced why: 0035 is filed under a generic "spine reconciliation" filename with no "contact" in it, easy to miss on a targeted search.
- Re-verified live via Supabase MCP `execute_sql` against both ehow and zaap: `customer_id` is nullable on both planes right now, and ehow currently holds 1 live contact with a null `customer_id` (down from the 53 migration 0035 was written against — Tidy/orphan-check has been resolving them over the last 3 months). A NOT NULL constraint cannot coexist with an existing null row, so this is a real row proving the column, not just schema metadata.
- Fixed both copies (root `schemas/contact.schema.json` and the vendored `eq-platform/packages/eq-schemas/src/schemas/contact.schema.json`, kept byte-identical per this repo's existing convention) — `customer_id` back to `type: ["string", "null"]`, out of `required`. Regenerated `types/contact.d.ts`.
- Full verification: eq-schemas (3/3), eq-validation (318/318, incl. `samples-validation.test.ts`), eq-intake-demo (50/50, incl. `commit-canonical.test.ts`), eq-intake (164/166, 2 pre-existing skips) — all green, typecheck clean. Committed + pushed directly to `main` (`5a75a16`); CI green (run `34832601563`, 2m11s).

**Notes (load-bearing):**
- **A targeted/filename-based search for DB-constraint history on a specific column is not enough — grep migration file *content*, not just filenames.** `fdf0055`'s live check missed migration 0035 for exactly this reason. Applies to any future "does the live DB match this schema/type" question in this repo.
- **This repo keeps two hand-maintained copies of every canonical schema** (root `schemas/` + vendored `eq-platform/packages/eq-schemas/src/schemas/`) with no automated check that they stay in sync — this is now the 3rd file (after `site.schema.json`, `asset.schema.json`) to need a manual "reconcile drift" fix this month, and `contact.schema.json` specifically has now drifted and been re-fixed twice in 5 days. Flagged as a follow-up task (`task_cd08e566`) — not built this session.
- Full commit-message trail (exact migration numbers, RPC names, test counts) lives in eq-solves-intake commit `5a75a16` itself — not duplicated here.

---

## eq-solves-intake: site.schema.json + asset.schema.json drift reconciled against live systems; stale fuzzy-match-reconcile branch deleted (2026-09-09)
*Closed out the deferred item from the 2026-09-09 contact.schema.json close below (`task_672eb4fa`) — eq-platform's `site.schema.json` copy had a real coerce feature and an accurate `client_name` description that root was missing/wrong about.*

**Completed:**
- `country`: verified `coerceCountry`/`country-iso-alpha2` is real, implemented (`eq-validation/src/coerce-country.ts`) and wired into the dispatcher (`validate.ts:443`) — root was missing the hint for a working feature. Reconciled to match eq-platform.
- `client_name`: root wrongly marked it `x-eq-deprecated`. Verified live against ehow (`app_data.sites`, 255 rows) — the column is actively written by the current `eq_upsert_site` RPC (migration `0245`, security-hardened 2026-08-15, nothing since supersedes it) on both insert and upsert-merge paths; 0/255 rows currently populated, which is evidence of low adoption, not deprecation (a truly deprecated field wouldn't get carefully-maintained upsert-merge logic in an Aug-15 hardening pass). Reconciled to eq-platform's plain, accurate description.
- Root's separate `customer_id`/`x-eq-fk-fuzzy-match-on` drift on the same file left untouched — deliberately out of scope, and contested by the stale branch below.
- Regenerated `types/site.d.ts`. eq-solves-intake `main` @ `8dccda0`, pushed.
- **Bonus find, same pattern:** checked all 34 schema files for the same root-vs-eq-platform drift. 18 "missing in eq-platform" files are deliberate curation (eq-platform's `@eq/schemas` is a canonical cross-app subset, not a full mirror — confirmed via its own package.json description and a clean thematic split), not drift. `asset.schema.json` was real drift though — eq-platform's `x-eq-source-aliases` were a strict superset across ~17 properties (e.g. `model` was missing `part_number`/`product_code`/`catalogue_no`). Reconciled root to match byte-for-byte, regenerated `types/asset.d.ts`. `main` @ `9c6b542`, pushed.
- **`claude/fuzzy-match-reconcile` branch deleted** — traced its one commit (`be27825`) against current main and found it fully superseded: its core engine changes are byte-identical to what already landed via PR #112/#113 (with main's version *better* — a documented perf fix main has that the branch doesn't), and its two schema-file hunks were actively regressive (would have reverted the `customer.company_name` fix and re-added `simpro_*` aliases main already removed). No open PR existed for it. Deleted on Royce's confirm.

**Notes (load-bearing):**
- Session was interrupted by a computer shutdown mid-task (after the brief was stated, before the edit landed) — resumed cleanly on restart via the same `/brief` gate, no work lost.
- Investigating this incidentally surfaced a "No suitable key or wrong key type" error on EQ Shell's Review Queue (tenant `madagins`) — turned into a separate, much larger eq-shell thread. See `eq/pending/eq-shell.md`'s matching entry, not tracked here.

---

## eq-solves-intake: full product review + duplicate-scan perf fix shipped live; RPC column-projection drafted (2026-09-07)
*Royce: "I want to get on top of eq intake once and for all... it takes >30 seconds to load... I do not see what it does." Full review found the real cause: the screen he'd been opening (`@eq/intake-demo`, standalone `pnpm dev`) is a component test harness that happens to share its "One-screen Intake — the actual product" banner with the genuinely real, production-wired copy mounted inside eq-shell at `/intake` — same source file, two contexts, no visual difference between them. The engine underneath (validation, fuzzy matching, AI layer) verified independently solid — tiered models, human-confirms-everything, injection-hardened prompts, a health score that already caught and fixed a real false-positive against live SKS data. Full write-up delivered to Royce as a file.*

*Redirected into a live perf bug once Royce opened the real screen and hit it — screenshotted "Scan for possible duplicates" hanging on real data.*

**Completed:**
- `duplicate-detect.ts` — the O(n²) fuzzy-dedup pass rebuilt both records' bigram sets from scratch on every pairwise comparison instead of once per candidate. Live assets table is 2,854 rows (confirmed against ehow) — ~4M wasted rebuilds. Fixed; full suite green (164 tests); benchmarked side-by-side against the original: ~7.7s → ~1.3s for the comparison pass, ~8.7s → ~1.7s full scan, byte-identical output verified. eq-solves-intake `main` @ `6e1e2f2`.
- Re-vendored into eq-shell ([PR #1792](https://github.com/eq-solutions/eq-shell/pull/1792)), merged, confirmed live on core.eq.solutions via deploy-ancestry check.
- Diagnosed the other half of "every button takes an eternity": `eq_tidy_read_entity` fetches every column of every row, called independently by 4 separate functions (health score, licence-expiry, duplicate scan, stale-record check) with no sharing between them. Fix designed as column projection, not literal pagination — all 4 callers need a whole-table fact (a completeness fraction, a full staleness count), so LIMIT/OFFSET wouldn't cut payload. `duplicate-detect.ts`'s completeness tie-break deliberately excluded from projection — it needs every column.
- First drafted the migration in this repo's own `sql/` staging folder (`065_...`, commit `9abd761`) before finding eq-shell's `SCHEMA-GOVERNANCE.md`: this repo's `sql/` folder is the explicitly-deprecated pre-One-Pipe pattern for tenant schema. Re-authored properly as eq-shell `supabase/tenant-migrations/0303_tidy_read_entity_columns.sql` — a new function (`eq_tidy_read_entity_columns`), not a signature change to the existing one (would create an ambiguous Postgres overload on any existing 1-arg call). [PR #1797](https://github.com/eq-solutions/eq-shell/pull/1797), merged.

**Deferred:**
- [ ] **The demo-vs-real confusion itself is still unfixed** — `eq-intake-demo`'s `App.tsx` still stacks the "engineering scenarios... not the product" banner directly under "the actual product," and `mock-supabase.ts` still silently no-ops on RPCs it doesn't implement. Options laid out in the review (make the demo say what it is / wire it to real Supabase read-only / leave it) — Royce's call on which, if any. _(added 2026-09-07)_

**Notes (load-bearing):**
- **eq-shell vendors this repo, it doesn't depend on it live** — `eq-shell/eq-intake/` is a physical copy (`scripts/revendor-intake.mjs`), not a submodule, because this repo is private and Netlify can't clone private submodules for the build. A push here does nothing to production until someone re-vendors.
- **GitHub MCP connector can't reach `eq-solutions/eq-shell`** — 404 on both reads and writes, confirmed live 2026-09-07; `gh` CLI works fine with the same account. Use `gh` for anything GitHub-side on eq-shell specifically.

---

## eq-solves-intake: the data-cleaning queue actually shrinks as you work it now, plus a bad-merge error fixed (2026-08-16)
*Royce flagged three problems with the review queue from screenshots: decided duplicate rows just sat there cluttering the list forever with no way to fix a wrong answer, a duplicate-contacts merge threw a raw error on screen, and the "unknown trade" list had no way to fix several people at once. Built and merged, then self-reviewed the same work and fixed six more bugs the review turned up before calling it done.*

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

---
title: Changelog — EQ Context Repo
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Append-only history of changes to the eq-context repository itself
read_priority: reference
status: live
---

# Changelog — EQ Context Repo

## [2026-06-07] SKS Live roles sprint doc added (live-verified)

**Built by:** Royce Milmlow + Claude Code

- `sks-live-sprint-2026-06-07.md` (new, root) — source-of-truth handoff for the **roles / security-groups track** of SKS Live: repo/action table, order of operations, and agent prompts A–E. Sibling to `SKS-CUTOVER-CRITICAL-PATH.md` (the Field schema/data track) — the two are parallel workstreams, cross-linked, not overlapping.
- Live-verified before saving: project refs (`sks-canonical`/`eq-canonical`/`eq-canonical-internal`/`sks-labour`), `shell_control` group counts (9 groups / 16 perms / 0 assignments), `user_security_groups` columns, tenant `sks` = 3 × manager, and the `contact_customer_links` `with_check=null` Phase-5 finding. GitHub-side claims (PR #7, branch divergence) left flagged as leads.
- Two drift fixes baked into the prompts: Phase 3 writes `assigned_by`/`assigned_at`; Phase 5 `WITH CHECK` casts `::uuid` to match the existing qual.
- Session log: `sessions/2026-06-07.md`.

## [2026-05-30] Dead-weight audit + CI greening (3 PRs)

**Built by:** Royce Milmlow + assistant (Claude Code)

- **Hooks (#2):** removed superseded `hooks/` dir + `install-hooks.bat` (v2 mechanism, superseded 2026-05-24 by `.githooks/` + `scripts/install-hooks.ps1`); corrected stale pointers in `system/git-automation.md` + `ops/pending.md`.
- **Archive (#2):** moved 9 spent/deferred 2026-05-30 sprint working docs → `archive/sprints/` (git-rename, history kept), logged in `archive/README.md`; redirected live pointers in `SPRINT-2-BOARD.md`. Kept `SPRINT-BOARD.md` (live-wired), the 3 S2 backlogs, and `auth-spike` (C4 reference) as not-dead.
- **Scripts (#3):** removed 2 spent one-shot scripts — `push-sks-team.bat` + `cleanup-worktrees.bat` (the latter superseded by the generic `cleanup-worktrees.ps1`).
- **CI green (#4):** fixed 11 pre-existing frontmatter violations (prose in `status:` → valid enum + lossless `**Status:**` body note; missing `read_priority`; 4 stray `<!-- source -->` comments stripped) and relaxed the session-filename rule to allow `YYYY-MM-DD-<part>.md` across `md-health.yml` + `.githooks/pre-commit` + `system/md-style.md`. `Frontmatter validation` + `MD health` had been red on `main` since before this work; now green.
- Empty `hooks/` + `resume/` dirs removed; 3 merged branches pruned (local + remote). No broken links; substrate synced.

## [2026-05-24] Substrate maintenance pass — overnight artefacts deleted, Cards gaps promoted

**Built by:** Royce Milmlow + assistant

- `eq/overnight-prompt-2026-05-21.md` + `eq/overnight-report-2026-05-21.md` — deleted. One-time artefacts; known-gaps content promoted to `eq/pending.md` before deletion.
- `eq/pending.md` — new `## EQ Cards` section added with 3 open follow-up items from the 2026-05-21 Cards canonical flip (photo migration, custom domain, branch cleanup). Trailing blank list item removed.
- `eq/products.md` — stale overnight-report reference in the Cards section replaced with `eq/pending.md §EQ Cards`.
- `eq/changelog/eq-context.md` (this file) — 2026-05-21 Cards flip entry + this maintenance entry added.
- `ops/pending.md` — PAT rotation note updated (PATs expired 2026-05-19); stale "Beelink return" deferral note removed.
- `archive/sessions-2026-04.md` — created; 8 April sessions rolled up to one-liners.
- `sessions/2026-04-{05,10,12,15,18,19,27,28}.md` — removed from GitHub (>30 days old, value already in tier files).
- `system/lessons.md` — `core.hooksPath` gotcha lesson added.
- 14 orphaned Supabase rows deleted (8 April sessions + 6 stale file renames).
- Substrate: 80 → 67 rows post-cleanup.

## [2026-05-21] EQ Cards — canonical flip (Flutter app + SSO handoff)

**Built by:** assistant (overnight autonomous session, Royce asleep)
**Repos touched:** `eq-solutions/eq-shell` (2 commits), `eq-cards` (1 commit on `claude/canonical-migration`)

**What changed:**

- Flutter app rebuilt to read from `app_data.licences` + `app_data.staff` on eq-canonical (`jvknxcmbtrfnxfrwfimn`) via 8 new `eq_cards_*` RPCs that bridge the column rename (`user_id → staff_id`, `photo_*_url → photo_*_path`, `deleted_at → active=false`).
- Shell flag `CARDS_USE_SHELL_SSO=true` added (`commit 8ba0d4f`). `mint-cards-iframe-token` Netlify function mints a JWT; Flutter app receives it in the iframe URL hash — no more email-OTP flow.
- `IframeHandoffScreen` built in Flutter to pick up the token and bootstrap the session.
- Verified end-to-end: decoded JWT confirmed correct staff/licence chain in Chrome MCP session.
- Legacy Cards Supabase (`hshvnjzczdytfiklhojz`) left as read-only rollback insurance pending photo migration.

**Known gaps (open in `eq/pending.md` §EQ Cards):**
- Licence photo JPGs not migrated — `photo_front_path` NULL on canonical.
- `cards.eq.solutions` custom domain not yet aliased on Netlify.
- `claude/canonical-migration` branch not yet merged/deleted.

## [2026-05-23] Sprint S3 — EQ Shell polish + audit + visible features

**Built by:** Claude (autonomous session, Royce asleep)
**Repos touched:** `eq-solutions/eq-shell` (3 commits), `eq-solutions/eq-intake` (1 commit, supplemental seed)

**What changed:**

**eq-shell:**
- `TenantHome.tsx` — full dashboard rebuild: dark-navy hero strip, hero number tiles with delta labels, Snapshot stat-card grid, recent intake activity feed, module grid with Live/Soon chips, Quick Actions section (6 actions). Fixed nested `<main>` structure.
- `App.tsx` — all plain "Loading…" divs replaced with Skeleton-based states in RequireSession, RootRoute, and Suspense boundaries.
- `AdminAuditPage.tsx` — rollback UX replaced `prompt()/alert()` with a proper modal (textarea for reason, Cancel/Confirm, error + success display).
- `AdminTenantSettings.tsx` — copy polish: "Tenant settings" → "Settings", "Tenant name" → "Business name", "module" → "app"; jargon stripped from hint text.
- `Topbar.tsx` — role-gated nav items via `useCan('admin.list_users')` + `useCan('audit.view')` + `useCan('admin.review_cards')`. "New staff" nav item added for card reviewers.
- `AdminCardsFeed.tsx` — refactored from card-per-row to standard eq-table layout with name/email search + per-row busy state.
- Copy sweep across NotFound, AdminUserList, AdminInviteUser, EntityBrowserPage: jargon removed, plain-English copy throughout.
- `tender_pipeline` removed from MODULES array (module removed per CLAUDE.md 2026-05-23).

**eq-intake:**
- `sql/012_s3_supplemental_seed.sql` — 25 licences (real Australian licence types), 22 prestart checks, 14 toolbox talks seeded against core tenant. All marked `imported_from = 'sprint_s3_seed_2026_05_20'`. Idempotent DO block.

**eq-context (this repo):**
- `eq/sprints/2026-05-20-S3-polish-and-audit.md` — execution record appended.
- `eq/products.md` — EQ Shell section updated to post-S3 state.
- `eq/changelog/eq-context.md` (this file) — S3 entry added.

**Build:** Green on all pushes. core.eq.solutions auto-deployed from eq-shell `main`.

## [2026-05-07] sks-team/ Tier Sync Repair + Edge Function Path Fix
**Built by:** Royce Milmlow + assistant
**Context:** Holiday-laptop session. Started as a small "fix one MD file" request and escalated into a full substrate-incident investigation when content turned out to be wrong, sync turned out to be broken, and the public edge function turned out to be partially blind to the post-2026-05-04 tier structure.

**Content fixes (3 MD files):**
- `sks/team.md` — was a duplicate of `sks-team/README.md` content (wrong file pasted into wrong path during 2026-05-04 refactor). Rewritten as actual NSW Operations team roster: Mark Brame (NSW GM), Royce, John Ryan (NSW Construction Mgr), Sharon Maroni; PMs Koos Otto, Ian Marston, Benjamen Ritchie, Leif Lundberg, Jack Cluff; Estimator John McKee; Supervisors Todd Wilson, Wayne Rowe, Collin Toohey, Luke Wheeler, Matt Miller, Simon Bramall, David Boyd. Names sourced from `SKS business advice` chat (today, post demo-strip) — not from `userMemories` which carried stale Federico Sander / Nathan Anderson references that aren't on the current bench.
- `sks-team/README.md` — replaced lowercase `readme.md`. Rule 1 violations (cross-references to `ops/decisions.md`) removed. Rule 3 ("Public-readable") clarified: "team-safe content only" — no labour rates, no client commercial terms, names yes / commercials no.
- `sks-team/quoting.md` §5 — estimator quick-pick rewritten. John McKee (NSW estimator) promoted to top of the list. Federico Sander removed (not on current bench). Simon Bramall removed from PM list (he's now Leading Hand/Supervisor, not PM).

**Sync workflow bug (the meat):**
- Discovered that `sks-team/quoting.md` and `sks-team/README.md` had been in GitHub since 2026-05-04 but had **never synced to Supabase**. Workflow ran green for every push that touched those files. Verification job inside the workflow passed. But direct query against `context_files` showed zero `sks-team/*` rows.
- Root cause: `.github/workflows/sync-context.yml` has two duplicate path lists. The YAML `on.push.paths:` filter (deciding *whether* the workflow triggers) included `sks-team/**`. The Python `SUBDIR_PATTERNS` glob list (deciding *what files the script actually reads*) did NOT include `sks-team/**/*.md`. So the workflow triggered, ran, found no `sks-team/*` files via glob, and exited green having silently skipped the entire tier.
- Fix: added `"sks-team/**/*.md"` to `SUBDIR_PATTERNS`. End-to-end verified with a test commit — `sks-team/*` rows now sync within ~30 seconds.
- Lesson logged in `system/lessons.md` 2026-05-07: workflow has duplicate state, drift caused this incident, future-hardening item logged in `ops/pending.md` to either derive one list from the other or add a CI check.

**Edge function bug (incidental discovery during the same investigation):**
- Public Supabase edge function at `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/<slug>` was written for the original flat 5-slug substrate (`eq`, `sks`, `cowork`, `rules`, `agents`). When 2026-05-04 refactor moved everything to tier-separated paths, the edge function was never updated. It used `pathParts[pathParts.length - 1]` to extract the slug — meaning `/context/sks-team/quoting.md` resolved to slug `quoting.md` and 404'd because no such row exists.
- Cowork session-start protocol fetches `/context/claude` (single segment, still works). Tier-deep fetches from chat, ChatGPT, Grok all 404'd silently for ~3 days.
- Fix deployed: edge function v3 → v4 (project `urjhmkhbgaxrofurpbgc`). Slug now constructed by joining everything after `context/`, with a fallback that tries `<slug>/README.md` when single-segment slugs don't resolve directly. So `/context/eq` → falls back to `eq/README.md` (tier index), `/context/sks-team/quoting.md` resolves directly, `/context/claude` continues to work via direct match.
- Lesson logged in `system/lessons.md` 2026-05-07.

**Same-day reconciliation (chat → Supabase → GitHub):**
- During the investigation, three corrected files were written directly to Supabase via MCP (chat-to-Supabase emergency path per `rules/non-negotiables.md` Substrate section).
- After the workflow fix landed, GitHub was uploaded with the same three patched files. Sync ran clean, GitHub canonical content now matches Supabase content. Drift closed same-day per substrate rule.

**Substrate state at session close:**
- 44 rows in `context_files`, all syncing reliably from GitHub `main`
- `sks-team/*` tier reachable via public edge function for the first time
- Workflow + edge function now consistent with post-2026-05-04 tier structure
- Two new lessons logged (workflow path-list drift, edge function path handling)
- Two new pending items logged (collapse workflow duplicate state, edge-function checklist for structure changes)

**Honest score:** good substrate-incident response — direct query caught what workflow status didn't, fix at structural level (workflow patch + edge function deploy), reconciled to GitHub same day, lessons logged. The original "fix one MD file" framing was wrong; the underlying issue was substrate plumbing, not content. Spotting that early is worth more than the speed of the content fix.

## [2026-04-28] Substrate-Discipline Closeout — Trigger Fix, Documentation, Audit Cadence
**Built by:** Royce Milmlow + assistant
**Commits:** `27b7f69` (substrate corrections), `fedfaba` (sync workflow defence-in-depth), plus the closeout commit that includes this entry

**Substrate corrections (3 MD files):**
- `knowledge/decisions.md` — three 2026-04-28 entries: context_files schema authoritative, GitHub canonical, "done" defined as fresh updated_at.
- `knowledge/lessons.md` — three new lessons: memory drift on substrate names, update-discipline lapse, false-implementation pattern + verification SQL pattern.
- `state/pending.md` — new "Substrate Discipline — IMMEDIATE" section captured 6 items.

**Substrate freshness fix (the meat):**
- DB trigger `context_files_set_updated_at` applied to `urjhmkhbgaxrofurpbgc.public.context_files` — `BEFORE UPDATE FOR EACH ROW` stamps `updated_at = NOW()`. Before this, the column's `DEFAULT now()` only fired on INSERT, and the GitHub Action's PostgREST upsert (which only sends slug/filename/content) left `updated_at` frozen forever. The freshness signal was structurally unreliable for any file edited after first sync — including the 2026-04-27 audit's "17/30 stale" finding, which was inflated by this bug masking real edits.
- `.github/workflows/sync-context.yml` — `import datetime` + `updated_at` field now sent in the upsert payload (defence-in-depth if the trigger is ever dropped).
- Verification job appended to the same workflow: after the upsert loop, queries the synced slugs and fails the workflow if any has `updated_at < (now − 60s)`. Machine-enforces "done" semantics.

**Substrate documentation closeout:**
- `rules/non-negotiables.md` — new "Substrate" section between Session Discipline and Code & Deployment: GitHub canonical, updated_at as freshness signal of record.
- `knowledge/architecture.md` — fixed stale row caption (`claude_context table` → `context_files`); added "eq-context Substrate" subsection (schema, sync flow, trigger, co-tenant rationale).
- `AGENTS.md` + `CLAUDE.md` — ported the global "always use clickable card UI for questions" rule into the project substrate so it doesn't depend on a user's machine-local global CLAUDE.md being loaded.
- `knowledge/lessons.md` — annotated "Update Discipline Lapsed" lesson with retroactive note about the trigger bug.

**Scheduled audit:**
- Local scheduled task `eq-context-substrate-audit` registered: Fri 9am AEST cron, runs the substrate audit query, surfaces only stale rows.

**Status:** Trigger live, workflow enhanced, all `state/pending.md` "Substrate Discipline — IMMEDIATE" boxes ticked.

**Late-evening iteration — six commits past `7aa4dfb`:**
- `9643440` — `CLAUDE.md` slimmed 211 → 125 lines (40%). Removed sections duplicating content in `state/entities.md`, `state/products.md`, `rules/deployment.md`, `rules/non-negotiables.md`, `rules/brand.md`. Replaced with a "Where things live" navigation table. The substrate non-negotiable shipped earlier the same day made the duplications a liability rather than redundancy.
- `f45b672` — UTF-8 BOM stripped from 7 `changelog/*.md` files. Cosmetic data cleanup; the pre-commit hook fixed earlier already tolerates the BOM.
- `d0bfd57` — `.claude/settings.json` created with a 4-entry permissions allowlist via the `fewer-permission-prompts` skill: `get_advisors`, `list_migrations`, `mark_chapter`, `netlify-project-services-reader`. Read-only MCP tools that fired ≥3 times in recent transcripts. `execute_sql` (104 prompts — most-used MCP) skipped per skill conservatism, flagged for manual review (not in this commit). Same commit also added a Stop-event hook enforcing Session End Protocol §1.
- `beeaa71` — **Stop hook removed.** External chat-surface review applied Goodhart's law: blocking on "did pending.md change" would manufacture compliance theatre. Substrate freshness (mechanical) and session-end completeness (judgment) are different problems; one mechanism shouldn't enforce both. The trigger + workflow verification job + Friday audit are the right enforcement and were already shipped.
- `7a21a50` — MD_BEST_PRACTICES §17.10 added: tool-attribution drift in substrate prose. Codifies the pre-2026-04-26 "Royce Milmlow + assistant" convention. Pre-commit hook gains a WARN-level check flagging vendor-brand AI tool names in newly-added MD content (full pattern in `.githooks/pre-commit`; example list in MD_BEST_PRACTICES §17.10). Excludes README, MD_BEST_PRACTICES, drafts/, .github/, .githooks/.
- `bb86f24` — Tool-attribution sweep: 7 lines across 5 files restored to "+ assistant". Pre-commit WARN ran clean on the sweep itself (additions don't trigger), proving the hook only catches NEW drift on cleanup commits.

**Audit-trail close (this entry):** the six commits above shipped without corresponding updates to `sessions/2026-04-28.md`, `state/pending.md`, or this changelog. External review caught it. This sub-section + matching updates to the session log and pending.md close the gap. Lesson recorded: the substrate-correcting-self loop has to keep including the substrate logs themselves; otherwise the discipline the work enforces lapses in the meta-process of enforcing it.

**Refined decisions:**
- AGENTS.md has evolved past the "thin pointer" framing of MD_BEST_PRACTICES §1 — it's now the canonical cross-LLM entry point carrying the asking-questions rule. §1 updated to reflect this.
- §17.10 gains a one-sentence slogan ("Substrate prose is tool-neutral. Reference the action, not the actor.") plus an exception clause (Anthropic primitives like `AskUserQuestion` and MCP tool IDs are OK in substrate prose; vendor brands are not).

**Honest score on the night's work:** 9.0–9.3/10 per external review, after the audit-trail and codification gaps closed. Self-graded 9.86 was overstated; external review put it at 8.5/10 before this audit-trail close, which was fair.

**Sync-gap close (post-audit-trail):** verification of the audit-trail commit revealed that `MD_BEST_PRACTICES.md` had never synced to Supabase — the workflow's `ROOT_FILES` dict didn't include it. The file is THE substrate style standard yet wasn't reachable from the assistant-readable cache. Added to `ROOT_FILES` with slug `md_best_practices`. First sync occurs on this commit.

## [2026-04-18] Full Sweep Audit and Rewrite
**Built by:** Royce Milmlow + assistant
**Changes:**
- Supabase section across CLAUDE.md, state/entities.md, rules/deployment.md, rules/non-negotiables.md, knowledge/architecture.md rewritten to reflect three projects (sks-labour live, eq-solves-field demo, eq-solves-service-dev context store) — replaces old "one project" rule
- EQ Design Brief bumped v1.2 → v1.3 in CLAUDE.md; rules/brand.md rewritten around v1.3 (two logo variants, WCAG AA, Aptos Display for print)
- R2 logo URLs (SKS + EQ) captured in rules/brand.md
- SKS active project list added to CLAUDE.md (AWS SYD053, AirTrunk SYD3, NEXTDC S3, Equinix SY6, DigiCo)
- EQ Solves Service promoted to primary build in state/products.md
- AHD moved to Parked status in state/pending.md (revisit 2027)
- GitHub MCP 403 status surfaced as live infrastructure blocker across CLAUDE.md, deployment rules, pending.md
- Beelink workstation spec captured (Ryzen 7 7735HS, 32GB, 1TB NVMe, Chrome Remote Desktop, Cloudflare Tunnel)
- `_headers` security file requirement formalised
- Non-negotiables rule #4 rewritten: "never touch SKS live Supabase" replaces "never spin up new Supabase project"
- Real-client-names rule promoted to non-negotiable
- Two new decision log entries appended (v1.3 adoption, three-project split)
**Status:** Repo rewritten; SKS Labour + EQ Field version numbers pending Royce confirmation before push

## [2026-04-10] MD Best Practices and Cross-LLM Portability Pass
**Built by:** Royce Milmlow + assistant
**Changes:**
- Added `MD_BEST_PRACTICES.md` — cross-LLM style guide (YAML frontmatter, tool-agnostic phrasing, ISO dates, token budgets, Perplexity-specific guidance)
- Added `AGENTS.md` at repo root as a tool-neutral entry point alongside `CLAUDE.md`
- YAML frontmatter added to every MD file in the repo
- Replaced `Claude (Anthropic)` with `assistant` across changelogs for tool-neutrality
- Stripped expired `claude.ai/chat/...` session URLs from changelog entries
- Split responsibility between `knowledg
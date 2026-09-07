---
title: Substrate Tidy Protocol
owner: Royce Milmlow
last_updated: 2026-09-07
scope: On-demand pressure-release pass for the substrate itself — prunes rule/file bloat, never runs on a mandatory cadence
read_priority: high
status: live
---

# Substrate Tidy Protocol

**Purpose:** counter the substrate's default trajectory, which is growth. Every past
incident here became a permanent, universal rule or a permanently-growing file; almost
nothing decays. This pass makes that growth visible run-over-run and prunes it — with
Royce's sign-off, not silently — while explicitly protecting the small set of rules that
are actually load-bearing.

**Trigger phrases:** `/tidy`, "clean up the substrate", "is this getting too heavy",
"prune the rules". Royce-triggered only — **never** add this to a mandatory session-start
or session-close sequence. A mandatory cadence is itself one more standing rule, which is
exactly the failure mode this protocol exists to counter.

**Distinct from `/housekeep`.** Housekeep fixes drift found *during* a working session —
uncommitted files, stale PR status, a wrong CLAUDE.md fact — as a by-product of the work
just done, every single close. Tidy is a deliberate, separate pass over the rule system
and the standing files *themselves*, asking whether each one is still earning the cost of
being reloaded every session. Don't fold one into the other: housekeep's cadence (every
close) is too frequent for a structural prune to mean anything — nothing has changed
enough between two consecutive closes to be worth re-classifying.

---

## 1. Measure first

Line-count:
- Every file mandatorily loaded at session start: root `CLAUDE.md`, `system/TODAY.md`,
  `system/punch-list.md`, `digest.md`.
- Every file that's previously been split or evicted for size: `eq/pending/*.md`,
  `system/lessons.md`, `system/failures.md`, `rules/*.md`.

Compare against the **Pass Log** at the bottom of this file. The point isn't a one-time
count — it's catching the regrowth curve before it's a crisis again, the way
`eq/pending.md` regrew from a 491KB single-file split back to ~4,900 lines across shards
within three weeks.

## 2. Classify every rule, not just every file

For each rule in `CLAUDE.md` + `rules/*.md`, tag it:

- **HARD** — prevents irreversible harm (credentials, deploy approval, tenant isolation,
  destructive ops, money, auth changes). Leave verbatim regardless of age. Don't even
  propose trimming these.
- **PREFERENCE** — style, tone, workflow. Keep the rule; compress the prose once the rule
  itself is clear. Prefer the `/gap`, `/decide`, `/reflect` shape — a short trigger file
  that points at one tracked protocol doc — over embedding the full logic inline the way
  `/close` and `/housekeep` do (which is why those two need a separate durability-backup
  system that the other three don't).
- **SCAR TISSUE** — exists because of one dated incident: a "Corrected on…" note, an
  F-numbered failure, a named regression. If it's over ~90 days old and hasn't recurred,
  propose collapsing the write-up to one changelog line + a link, not a standing paragraph
  that everyone reloads every session.

Propose every cut with a before/after diff. Nothing gets deleted without a yes — this pass
recommends, it doesn't unilaterally edit.

## 3. Distrust rules that already failed once while looking compliant

Flag any rule whose own text admits a past version "passed re-verification while being
wrong" (the eq-shell deploy note is the known instance). Those need the check itself
redesigned, not just trimmed — the old version proved that looking rigorous and being
correct aren't the same thing in this substrate.

## 4. Check automation against what it claims to be

For anything labeled nightly / scheduled / cron-driven: pull its actual commit timestamps
(`git log --format='%H %ad' --date=iso -- <path>`) and confirm it fires on the cadence it
claims — not more, not less. A mismatch here is worse than no automation: it's a green
banner sitting over a process that isn't doing what it says.

## 5. Enforce the budgets that already exist, and give one to what doesn't

`suite-state.md` already evicts to a stated budget ("kept 30 most recent, evicted 37" is
written into the file itself). Apply the same pattern to anything purely additive today —
`system/lessons.md`, `system/failures.md`, any `eq/pending/<repo>.md` past ~500 lines:
propose what falls into an archive file, and write the line budget into the file so the
next pass has a number to check against, not a feeling.

## 6. Answer the actual question, at the end, plainly

State it directly: is the substrate lighter after this pass than before it? And
separately — did this pass change the *mechanism* that caused the growth, or only the
content? A prune that doesn't touch the mechanism just resets the clock.

---

## Pass Log

| Date | Root CLAUDE.md | TODAY+punch-list+digest | rules/*.md | eq/pending/* | lessons.md | failures.md | hooks/* | worktree-registry.md† | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-07 | 316 | 430 | 1,192 | 4,919 | 405 | 257 | 3,643 | 647L / 368.5KB (pre-split) | Baseline. Protocol created after Royce asked whether the substrate had gotten too structured; same-day `git log` showed 14 of the 15 most recent commits were automated bookkeeping (7× session-close, 3× nightly digest, 2× nightly suite-state-refresh), 1 was product work. Same session also caught `/brief` itself carrying 3 defects (a `$ARGUMENTS`-into-empty-heading bug shared with `/gap`/`/decide`/`/reflect`, no check that `digest.md` itself was current, and a Step 2 that depended on a 368.5KB registry file too large to read) — all fixed same session. No classification pass (steps 2–6) run yet — this row is measurement only. |
| 2026-09-07 (b) | 317 | 430 | 1,426* | 4,807 | 405 | 257 | 3,643 | 96 | First real classification pass (steps 2–6), same day. *rules/*.md includes this file (+100) plus ~134 lines of organic growth across the other 10 files since the baseline row a few hours earlier — not re-diffed line-by-line, noted rather than chased. `eq/pending/*` dropped (a concurrent session pruned eq-solves-service's backlog, 30 items closed, live-verified — first observed evidence this side of the substrate can shrink on its own, unprompted by this protocol). **Verdict: rule content itself is already disciplined** — `non-negotiables.md`, `agentic-coding.md`, `admin-feature-baseline.md`, `reflection-protocol.md` are lean and mostly HARD; the brand files are dense but that's reference data (hex codes, dimensions), not bloat. Nothing found is over the 90-day scar-tissue threshold yet (youngest incident-narrative candidates measured at close: 2d, 23d, 23d, 30d, 53d old) — this pass proposed 2 small cuts anyway (one dead carve-out that doesn't need the age test; one cross-file duplication between this repo and the user's global `~/.claude/CLAUDE.md`) rather than force a bigger result to look thorough. Both pending Royce's yes. **Mechanism note:** this pass didn't change the growth mechanism, only classified current content — the real standing bloat (`eq/pending/*`, `lessons.md`, `failures.md`) is unchanged from baseline and still has no enforced budget; still open, not solved by this pass. `worktree-registry.md` column added same day, after a concurrent session (`task_d0ceeaf5`) split the file and wrote a ~150-line budget into it directly — closes a gap a different concurrent session flagged in `ops/pending.md` before this row was even written. |
| 2026-09-07 (c) | 317 | 430 | 1,296 | 4,807 | 410 | 263 | 3,262 | 96 | Confirm-and-close pass on (b)'s 2 proposed cuts, same day — not a fresh reclassification (steps 2–4 were already substantially run today across concurrent sessions; see (b) row and `sessions/2026-09-07.md`'s cadence-fix entry for Step 4's automation-cadence check). Independently re-verified both cuts rather than trusting the summary. **Cut 1 (eq-shell note duplication): already resolved before this pass reached it** — a concurrent session trimmed the global `~/.claude/CLAUDE.md` copy to a pointer at `rules/deployment.md` between this pass starting and checking, and did it correctly: kept the one paragraph that wasn't actually duplicated (the manual-deploy `git archive` workaround) rather than dropping or duplicating it — confirmed `rules/deployment.md` still doesn't carry that paragraph, so nothing needed there either. **Cut 2 (EQ Quotes stale status): still live, fixed** — `rules/deployment.md` said "deferred ~6 months" against `suite-state.md`'s canonical RETIRED and `stack.md`'s already-correct wording; now matches. **Step 5's still-open finding, closed:** confirmed via grep across every `.github/scripts/*.py` and `scripts/*.py` that `lessons.md`/`failures.md` have zero rotation mechanism (only `rotate_pending.py`/`dedupe_pending_archive.py` exist, both `eq/pending`-scoped). `lessons.md` already had a manual precedent (`archive/lessons-history.md`, from a 2026-07-12 trim) — its new budget formalizes that pattern. `failures.md` had no precedent at all — its new budget establishes one, same split shape as `worktree-registry-archive.md`. Neither file is near its new threshold today (lessons 410/500, failures 263/400) — nothing evicted, just a number for the next pass to check against. `rules/*.md` total (1,296) isn't directly comparable to (b)'s 1,426 — origin/main took on more concurrent edits to other rules files in between; not re-diffed line-by-line given the volume of same-day concurrent activity. `hooks/*` dropped further (3,643→3,262, -381 since baseline) — observed, not investigated; out of Step 2's scope (CLAUDE.md + rules/*.md only). **Answering Step 6 for the whole day, not just this pass:** substrate is materially lighter than this morning's baseline — `worktree-registry.md` 368.5KB→6.3KB, `hooks/*` -381 lines, `eq/pending/*` -112, and the 2 duplication/staleness cuts above. Mechanism did change in 2 places (`worktree-registry.md`'s Protocol step 3 + budget; `lessons.md`/`failures.md`'s new budgets), not just content — but `eq/pending/*` still has no stated per-shard ceiling (it does already have automated per-item eviction via `rotate_pending.py`, unlike the other two before today, so the gap left is narrower: a number, not a missing mechanism). |

† Budgets stated directly in each file: `system/worktree-registry.md` ~150 lines (added 2026-09-07), `system/lessons.md` ~500 lines and `system/failures.md` ~400 lines (both added 2026-09-07 (c)). `eq/pending/*` remains the one column with no stated per-shard line-count ceiling — see `ops/pending.md`.

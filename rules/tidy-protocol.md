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

| Date | Root CLAUDE.md | TODAY+punch-list+digest | rules/*.md | eq/pending/* | lessons.md | failures.md | hooks/* | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-09-07 | 316 | 430 | 1,192 | 4,919 | 405 | 257 | 3,643 | Baseline. Protocol created after Royce asked whether the substrate had gotten too structured; same-day `git log` showed 14 of the 15 most recent commits were automated bookkeeping (7× session-close, 3× nightly digest, 2× nightly suite-state-refresh), 1 was product work. Same session also caught `/brief` itself carrying 3 defects (a `$ARGUMENTS`-into-empty-heading bug shared with `/gap`/`/decide`/`/reflect`, no check that `digest.md` itself was current, and a Step 2 that depended on a 368.5KB registry file too large to read) — all fixed same session. No classification pass (steps 2–6) run yet — this row is measurement only. |

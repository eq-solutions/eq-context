---
title: The Notebook That Tells the Truth — Substrate Plan v2
owner: royce (pending confirmation — this file is `asserted` until he adopts it)
type: asserted
asserted_on: 2026-07-12
last_updated: 2026-07-12
scope: Proposed programme to make the EQ substrate self-verifying — facts close against the live DB, guards against escaped failures, goals against Royce
read_priority: standard
expires_on: 2026-08-12
verify: human
supersedes: system/substrate-a-plus-plan.md
status: draft
---

# The Notebook That Tells the Truth

## The fable

There was once a farmer with too many fields and one clever notebook. The notebook could write in itself, which was useful, because the farmer was busy. Each night it wrote down what had happened on the farm, and each morning it told the farmer what mattered.

One day the farmer noticed the notebook kept saying: *"Hurry — every apple must be sold by harvest day."* He stopped. "Who wrote that?" The notebook checked. The farmer hadn't. The farmhands hadn't. Nobody had — or rather, someone had once, long ago, perhaps as a guess, and a small beetle named Tick, whose only job was stamping today's date on every page so the pages looked fresh, had been re-stamping it every night. The guess wore a new date every morning. It looked like the truest thing in the book. Twelve fences had been mended in a hurry because of a sentence nobody owned.

The farmer didn't burn the notebook. He taught it three things.

**First: a fresh stamp is not the truth.** From then on, every sentence had to say *who said it* and *until when it could be trusted*. Sentences that expired turned pale, and the notebook asked at breakfast, "Do you still mean this?" — and if the farmer said no, the sentence died. An empty page, the notebook learned, is more honest than a confident guess.

**Second: there are only three judges.** If a sentence was about the farm — how many apples, which cow was sick — the notebook had to go and *count the apples*. Not check its own pages. Count. If a sentence was about the notebook's own rules — a gate that had let the goat through — the *hole in the fence* was the judge: wherever the goat had actually escaped, the fence grew stronger in that exact spot, and never grew weaker again. And if a sentence was about what the farmer *wanted*, only the farmer could say. The notebook could suggest, in pencil. It was never allowed to write in the farmer's ink.

**Third: don't make the farmer come to you.** The farmer had been finding scraps everywhere — notes in coat pockets, chalk on the barn door — each scrap sure of something slightly different. The scraps were burned. The pockets now held one line: *"It's in the notebook."* And instead of waiting to be opened, the notebook spoke at breakfast: two or three lines, only the things that truly needed a farmer. One morning it said, "Someone finished a maintenance round, for the first time ever." The farmer smiled. He hadn't even asked.

On its last page the notebook kept a list titled **"Things I still cannot see."** It was the page the farmer trusted most.

---

## Ground verified before writing (2026-07-12, live SQL on ehow)

- `app_data.maintenance_checks`: **16 created** (14 scheduled, 1 cancelled, 1 overdue — latest created today), **0 completed, ever**. TODAY.md's cached "14" already lags by two. The table is a cache; the query is the source. Stated as a fact, not a priority — goals are UNSET.
- **A live F5, found this session:** the global `~/.claude/CLAUDE.md` auto-loaded into every Cowork session still instructs *"Fetch and read raw.githubusercontent.com/.../CLAUDE.md"* — the exact read path that served 8–12-day-stale content on 2026-07-11 (F1). Only the pasted brief overrode it. F5 is not historical. It is running right now.

## Design rules (one per oracle)

1. **Facts close against the live DB.** Anything numeric carries its own SQL and is re-run nightly by machine. Machine-verified outcomes may auto-commit — the oracle is external, so the loop is safe. Everything else is propose-only.
2. **Guards close against escaped failures.** The ratchet (`failures.md` + `guard-ratchet.yml` + `adversarial_test.py`) stays the engine: every escape becomes a ledger entry and a permanent test; recurrence forces a promotion *proposal*. The system argues; Royce decides.
3. **Goals close against Royce, in conversation.** No agent writes a goal, promotes its own claim, or merges its own rule change. Royce's entire interface is chat questions with options. If a plan step requires him to open, run, or read anything, the step is redesigned or cut.

Plus one meta-rule: **net-negative machinery.** Every phase must retire more moving parts than it adds. Sixteen workflows watching the repos is how F4 happened while everything was green.

---

## Failure → guard map

| Failure | Guard after this plan | Rung | Phase |
|---|---|---|---|
| F1 stale read path | session gate (built) + courier keeps clone ≤24h behind origin | 4 | Day 0 / P5 |
| F2 Edit/Write truncation | `pre_tool_use.py` (built, 18 tests) | 4 | done |
| F3 unowned goal | claims ledger: typed, owned, expiring; agents cannot promote | 3 | P2 |
| F4 product unwatched | nightly product pulse + morning push on transitions | 3 | P3 |
| F5 shadow memories | pointer-only layers + `memory-coverage.yml` + gate self-check | 3/2 | Day 0 / P4 |
| F6 append NUL-fill | `pre_tool_use.py` (built) | 4 | done |

---

## Day 0 — stop the live misdirection *(30 min, agent only)*

The two ungoverned pointer files are actively routing agents to the path that lied:

- Rewrite `~/.claude/CLAUDE.md` (global) to a pure pointer: *"Read `C:\Projects\eq-context\CLAUDE.md` from the local clone. Never fetch raw URLs for context."* Zero facts. Done by Claude Code natively on the Beelink (it is not on the corrupting mount, but propose-only discipline applies — Royce approves the diff in chat).
- Prune Cowork auto-memory to pointers: its current entries carry Supabase project IDs and product-strategy facts — exactly F5-shaped. Each becomes "see eq-context / verify live."

**Acceptance (F1/F5):** a fresh session with *no pasted brief*, asked "where do you read CLAUDE.md from?", answers *the local clone* — and its loaded context contains no raw-URL instruction. Added to the adversarial suite as a manual checklist item (it cannot be automated from inside the repo — named in residual risks).
**Oracle:** escaped failures F1/F5.
**Royce does:** approves one diff in chat. Nothing else.

---

## Phase 2 — Truth: the claims ledger *(2 agent-days)*

One machine-owned file, `system/claims.yml`. Every load-bearing claim:

```yaml
- id: live-db-is-ehow
  claim: "Live DB for EQ Service/Field is ehow (ehowgjardagevnrluult)"
  type: verified        # goal | verified | asserted | inferred | stale
  owner: royce
  asserted_on: 2026-06-22
  verify: sql           # sql | human
  query: "select count(*) from app_data.maintenance_checks"
  value: 16
  last_verified: 2026-07-12
  expires_on: 2026-10-12
```

**Mechanics:**
- **One** nightly workflow, `substrate-nightly.yml` (folds claim-verify, claim-expiry, digest build, and Phase 3's pulse — not three new workflows):
  - runs every `verify: sql` claim against the live DB. Match → bump `last_verified`, auto-commit (machine oracle — safe). Mismatch → demote to `stale`, add to digest **Needs you**. Never edits claim text.
  - any `verify: human` claim past `expires_on` → **"confirm or kill"** in Needs you. Goals with no `expires_on` fail CI.
- **Promotion guard (CI):** a diff of `claims.yml` in which any claim's type transitions to `verified` is legal only when authored by the nightly workflow or accompanied by a recorded Royce answer. Agent commits can only add `asserted`/`inferred`. This mechanically blocks the collusion loop (an agent verifying its own assertion) — the hallucination amplifier.
- **Confidence inheritance:** the session gate prints the ledger summary (`n verified · n asserted · n stale · goals UNSET/set`), and `CLAUDE.md` §7 gains one line: quote a claim with its type — *"16 checks (verified 2026-07-12)"*, never *"16 checks."* Behavioural (rung 1–2) — named in residual risks.
- **Goals** enter only through Royce's chat words: agent transcribes as `type: goal, status: proposed`; his confirmation click makes it live. TODAY.md's GOALS section becomes a rendered view of the ledger, not a second copy.

**Acceptance (F3):** plant a goal with `expires_on` in the past → next nightly run *and* next session gate surface "confirm or kill" to Royce. Plant a `verify: sql` claim with a wrong value → demoted to `stale` and lands in Needs you by morning. Both become permanent adversarial-suite tests.
**Oracle:** live DB for facts; Royce for goals.
**Royce does:** answers occasional "confirm or kill" questions in chat. Never sees YAML.

---

## Phase 3 — Pulse: watch the product, push the truth *(1 agent-day)*

Product signals become `verify: sql` claims in the same ledger, refreshed by the same nightly run — F4's fix inherits Phase 2's machinery for free:

- maintenance checks completed (1d / 7d / all-time) and created
- non-Royce human writes, 7d (**excluding `source='system'`** — 2,494 automated writes will flatter every metric)
- prestarts / toolbox talks / site audits, 7d
- distinct active users, 7d
- substrate health: stale claims, CI red, courier age

**Transition detection, not thresholds:** the digest keeps yesterday's values; any zero→nonzero or nonzero→zero flip on a product signal goes to **Needs you**. The first-ever completed check reaches Royce the same morning, unprompted. No goals exist, so nothing is ranked — flips are surfaced as *facts that changed*.

**Delivery:** a scheduled morning task posts 2–3 lines in chat, leading with Needs you. Quiet day = one line. Nothing waits in a file (the 07-11 drift warning sat unread in a file for 12 days).

**Known gap, stated not smuggled:** adoption is currently unmeasurable — `service.profiles.last_login_at` is written only by the retired standalone signin; Shell SSO never writes it. Ledger carries this as an explicit `unmeasurable` claim; the instrumentation fix is a proposed build task for a normal session, gated by Rule 0.6.

**Acceptance (F4):** plant a flatline flip in the digest input → it appears in the next morning push. Real-world test: the day a check is completed, Royce is told without asking; any day one isn't, that fact is one visible line. Added to the suite.
**Oracle:** live DB.
**Royce does:** reads a short chat message at breakfast.

---

## Phase 4 — One notebook: collapse the shadows *(1 agent-day)*

| Layer | Target state |
|---|---|
| `eq-context` | The only place facts live. Governed, versioned, CI-checked. |
| `~/.claude/CLAUDE.md` | Pointer only (Day 0). |
| `C:\Projects\CLAUDE.md` | Pointer + repo map. Its duplicated rules and load-bearing facts move home or die. |
| Cowork preferences box | Empty (done 07-11). Gate self-check keeps it empty. |
| Cowork auto-memory / Chat memory | Pointers only (Day 0 for existing facts; discipline thereafter). |
| Per-repo `.claude/` | Tooling config only. |

- `memory-coverage.yml`: greps repo-resident layers for fact-shapes (Supabase project refs, deadlines, URLs, counts) outside eq-context → CI red.
- Out-of-repo layers (preferences box, Chat memory, auto-memory) are invisible to CI. The session gate therefore instructs the agent: compare loaded shadow context against the clone; contradictions get flagged and proposed for deletion. Rung 2, honestly labelled.
- **Retire `auto-bump-frontmatter`.** It is the beetle: it manufactures freshness, and freshness is the counterfeit currency this whole failure class trades in. Dates come from real commits.
- Workflow consolidation: 16 → target ≤8. Every retired workflow named in the PR. `CLAUDE.md` goes on a diet toward ≤200 lines — the gate already performs §1 mechanically, so the prose that duplicates it goes.

**Acceptance (F5):** plant a Supabase project ID in `C:\Projects\CLAUDE.md` → CI fails. Plant a contradicting fact in auto-memory → the next session gate flags it. Both added to the suite (the second as a scripted gate test).
**Oracle:** escaped failure F5; Royce approves each rewrite (propose-only PRs).
**Royce does:** approves diffs in chat.

---

## Phase 5 — The courier: no more .bat files *(1 agent-day + one decision)*

Today, closing a session means emitting a `.bat` for Royce to run — visible tech, and the reason the clone can lag origin (F1's mirror image: a stale clone lies exactly like a stale CDN).

- A Beelink-native scheduled task: `git -C C:\Projects\eq-context pull → commit staged substrate changes → push`. Scope-locked: **eq-context only, main only**, commit prefix `courier:`. Installed once by Claude Code running natively — Royce types nothing.
- The session gate reports courier age: *"courier last ran 6h ago."* A silent courier is announced, never assumed (the lesson of the guard that failed open).
- Requires one recorded decision: exempt eq-context (only) from the "never push without instruction" rule. Goes in `ops/decisions.md` with Royce as owner.

**Acceptance (F1):** make the clone lag origin by >24h → the gate flags it at next session start. And: the next session that changes the substrate ends with **zero** commands for Royce to run. Suite gains a courier-staleness test.
**Oracle:** Royce (it is a permission decision), then the failure ledger.
**Royce does:** answers one yes/no in chat. After that: nothing, ever.

---

## What Royce actually does, in total

Answers roughly six questions in chat: adopt this plan; approve the Day 0 pointer rewrites; approve the memory collapse PRs; the courier decision; the morning-push schedule; and — only if and when he wants — a goal. No files, no scripts, no ledgers, no configs, no dashboards. If any step above turns out to need more than a chat answer, that step is wrong and gets redesigned.

## Cost

| Item | Effort |
|---|---|
| Day 0 | 0.5 agent-day |
| Phase 2 — claims ledger | 2 agent-days |
| Phase 3 — product pulse | 1 agent-day |
| Phase 4 — memory collapse + consolidation | 1 agent-day |
| Phase 5 — courier | 1 agent-day |
| **Total** | **~5.5 agent-days · ~6 chat answers from Royce** |

Net machinery: −8 workflows, −1 date-stamping bot, −6 fact-bearing shadow memories; +1 nightly workflow, +1 ledger, +1 courier. There is no deadline; sequence is Day 0 first (live harm), then 2 → 3 → 4 → 5, each usable alone.

---

## What this still won't catch

1. **A verified falsehood.** If the query measures the wrong thing — wrong table, wrong filter, schema drift — the ledger faithfully records a wrong number as `verified`, nightly. This is the floor. Rule 0.5 (verify the live system by hand before building) is supported by this plan, never replaced.
2. **Confirmation theatre.** A "confirm or kill" that Royce clicks through unread is an owned lie instead of an unowned one. Mitigation: anything numeric must be `verify: sql`; humans confirm only goals and intent, and rarely.
3. **Out-of-repo shadow memories.** The preferences box, Chat memory, and this platform's own auto-loaded instructions cannot be watched by CI — only self-policed by the agent carrying them (rung 2), and a new tool tomorrow is a new ungoverned layer on day one. This session proved it: the stale-URL instruction was auto-loaded today and only the pasted brief caught it.
4. **Habituation.** The morning push dies the day it becomes noise. Rule: Needs you >5 items means the fix is triage, not scrolling. If Royce stops reading it, the system has no louder channel — and will not invent one.
5. **Green rot.** The adversarial suite tests the guards; nothing tests that the suite still runs against reality (a renamed hook file makes every test vacuously pass). Partial mitigation: the gate prints suite age and count; a shrinking count is a flag.
6. **Confidence laundering in prose.** Inheritance of claim types through an agent's *sentences* is behavioural, not mechanical. An agent can still say "16 checks" without the tag. Rung 1–2, recorded as such in `failures.md` the first time it escapes.
7. **The product itself.** This system can now tell Royce, every morning, that ten people log in and nobody can finish a maintenance round. It cannot make the completion path work. Watching is not fixing — and with goals UNSET, it is not even a priority until Royce says it is.

---

*The one-line version: the notebook may only believe the orchard, the holes in the fence, and the farmer — and it speaks at breakfast, in pencil.*

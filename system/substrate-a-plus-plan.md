---
title: Substrate A+ — Plan to a Self-Verifying Memory System
owner: Royce Milmlow
last_updated: 2026-07-11
scope: The programme to take the EQ substrate from B+ (excellent machinery, broken delivery) to A+ (self-verifying, self-expiring, adversarially tested)
read_priority: high
status: archived
superseded_by: system/substrate-plan-v2.md (2026-07-12)
expires_on: 2026-08-11
verify: human
---

# Substrate A+ — Plan

**Grade today: B−. After the 2026-07-11 fixes: B+. This plan is the path to A+.**

A+ is not "more documentation" or "more workflows". You already have more workflows than most funded engineering orgs. A+ is a memory system with three properties nobody currently has together:

1. **It cannot be silently wrong** — every load-bearing claim carries provenance, an owner, and an expiry.
2. **Its rules are physics, not prose** — enforced at the point of action, not written upstream of it.
3. **It proves this about itself, continuously** — an adversarial suite that plants failures and asserts they are caught.

---

## The benchmark: five real failures from 2026-07-11

The plan is measured against these. Not against a rubric. If a phase does not make one of these **structurally impossible**, it is not in the plan.

| # | Failure | Why every existing safeguard missed it |
|---|---|---|
| **F1** | `raw.../main/CLAUDE.md` served **8 days stale**, `digest.md` **12 days stale** — 200 OK, no error. | The §1 fallback triggers on *errors*. A stale cache hit is not an error. |
| **F2** | `Edit` **silently truncated** `CLAUDE.md` (308 → 277 lines, §12/§13 gone). Tool reported success. | The lesson existed in `lessons.md` — buried 300 lines in as "Bonus 2". It was read and still didn't fire. |
| **F3** | **"1 August 2026"** governed every session decision for two weeks from `read_priority: critical` — and its owner did not recognise it. | Freshness checks verify *recency*. Nothing verifies *truth* or *ownership*. `auto-bump-frontmatter` would have kept it looking fresh forever. |
| **F4** | `maintenance_checks`: **14 created, 0 ever completed.** Nothing surfaced it. | 16 workflows watch the repos. **Zero watch the product.** |
| **F5** | The **Cowork preferences box** — unversioned, unaudited — **overrode** the canonical contract and fed an agent stale substrate. | One governed memory. **Six ungoverned ones.** CI covers the one that was correct. |

**The through-line: the system knows the truth and cannot get it to you — and where it can, it cannot tell you whether the truth is still true.**

---

## Phase 0 — Stop the bleeding *(30 min, today)*

- [ ] **Hold `system/TODAY.md` out of the push** until the 1 August question is answered. It currently launders an unowned goal into a freshly-dated, "live-DB verified" file. **This is F3 being actively made worse.**
- [ ] Push `CLAUDE.md`, `system/lessons.md`, `sessions/2026-07-11-*.md`.
- [ ] **Delete the Cowork preferences patch.** (Claude settings → Preferences.) It is redundant and it caused F1.

**Acceptance:** the canonical contract is correct on `main`, and no shadow memory contradicts it.

---

## Phase 1 — Enforcement: turn prose into physics *(1 day)*

**Rationale:** until rules are enforced mechanically, every later phase decays back to prose. This phase is first because it is what makes the rest durable.

| Hook | Does | Kills |
|---|---|---|
| `SessionStart` | Prints: `digest.md` age · **Needs you** · expired claims · `git branch -a` on target repo. Unskippable. Costs zero ceremony tokens. | **F1** (loud), replaces the 13-step §1/§0.6 ritual that gets skipped |
| `PreToolUse` | **Blocks** `Edit`/`Write` on any file >200 lines under the `C:\Projects` mount. **Blocks** `git` from the Cowork sandbox. | **F2** — impossible, not "documented" |
| `PostToolUse` | After any write: `wc -l` before/after, assert no unexplained shrinkage. | **F2** — belt and braces; catches silent truncation even if a path is missed |

**Acceptance test:** attempt to `Edit` a 300-line file from Cowork. It must **fail**, not succeed-and-truncate. Attempt a session start with a 12-day-old digest. It must **stop**, not proceed.

**Also:** the §1 ritual collapses from 13 steps to a hook + one tier question. Ceremony becomes free.

---

## Phase 2 — Truth: typed claims with provenance and expiry *(2 days)* ← **this is the A+**

**The novel piece.** Nobody has solved this. It is what makes a substrate trustworthy rather than merely fresh.

Every load-bearing claim carries:

```yaml
claim: "Live DB is ehow (ehowgjardagevnrluult)"
type: verified          # goal | verified | asserted | inferred
owner: royce
asserted_on: 2026-06-22
verify: sql             # human | sql | api | ci
query: "select 1"       # machine-verifiable claims carry their own check
expires_on: 2026-09-22
```

**Three rules that make it work:**

1. **Goals expire fast; facts get re-verified.** A `type: goal` with no reconfirmation **dies automatically** and surfaces as *"Royce — confirm or kill: 1 August deadline."* F3 becomes impossible: the phantom would have expired on 2026-07-28 and been escalated, not silently obeyed.
2. **Agents cannot promote their own claims.** Anything an agent writes is `asserted`. Only `verify: sql` (machine, re-run nightly) or explicit human sign-off promotes to `verified`. **This blocks the collusion failure** where an agent writes a fact and then "verifies" it.
3. **Confidence is inherited, not laundered.** An agent quoting a claim must carry its type: *"5 users (asserted 2026-06-28, unverified)"* — never *"5 users."* Today I quoted `TODAY.md`'s guesses with the same confidence as live SQL. **The substrate gave me no way to tell the difference. That is the bug.**

**New CI:**
- `claim-expiry.yml` — fails on any expired load-bearing claim. Runs nightly + on merge.
- `claim-verify.yml` — for every `verify: sql` claim, **runs the query and diffs it against the stated value.** A substrate that checks itself against reality every night.

**Acceptance test:** plant a `type: goal` with `expires_on` in the past. CI must fail and it must reach Royce. Plant a `verify: sql` claim with a wrong number. CI must catch the discrepancy.

---

## Phase 3 — Delivery: push, don't store *(0.5 day)*

**Rationale:** F4. You have 16 workflows watching your repos and none watching your business. `substrate-honesty` wrote "✗ Drift detected" into a file nobody opened for 12 days.

- [ ] **Product signals in `digest.md`** — the numbers that decide the quarter, not the numbers that decide a PR:
  - maintenance checks **completed** today / 7d *(currently 0, always 0)*
  - **non-Royce** human writes, 7d *(exclude `source='system'` — 2,494 automated writes flatter every metric you have)*
  - prestarts / toolbox / site audits, 7d
  - distinct active users, 7d
  - expired claims, drift, CI red
- [ ] **A morning push** — scheduled task or live artifact. **Needs you** reaches you; it does not wait in a file.

**Acceptance test:** the day a maintenance check is first completed, you find out **without asking**. Equally: on any day one *isn't*, that is visible.

---

## Phase 4 — Governance: collapse the shadow memories *(0.5 day)*

**Rationale:** F5. Seven memory layers. One governed.

| Layer | Target state |
|---|---|
| `eq-context` substrate | **The only place facts live.** Governed, versioned, CI-checked. |
| `~/.claude/CLAUDE.md` (global) | **Thin pointer. Zero facts.** "Read `eq-context/CLAUDE.md`. Obey it." |
| `C:\Projects\CLAUDE.md` (project) | **Thin pointer + repo map only.** No rules — they duplicate and drift from §7. |
| **Cowork preferences box** | **Empty.** |
| Cowork auto-memory, Chat memory | Pointers only. No facts. |
| Per-repo `.claude/` | Tooling config only. |

- [ ] `memory-coverage.yml` — CI asserts no fact-shaped content outside `eq-context` (Supabase project IDs, URLs, deadlines, counts).

**Acceptance test:** grep every memory layer for a Supabase project ID. Exactly one repo may contain them.

---

## Phase 5 — Prove it: the adversarial suite *(0.5 day)* ← **this is what makes it A+ and not A**

**Regression testing for your brain.** Nobody does this.

`substrate-adversarial.yml` deliberately plants each of the five 2026-07-11 failures and **asserts the system catches every one**:

| Test | Plants | Must be caught by |
|---|---|---|
| F1 | a stale substrate read | Phase 1 `SessionStart` freshness gate |
| F2 | a truncating long-file write | Phase 1 `PreToolUse` / `PostToolUse` |
| F3 | an expired, unowned `type: goal` | Phase 2 `claim-expiry` |
| F4 | a product metric flatlining at 0 | Phase 3 digest signal |
| F5 | a shadow memory contradicting canonical | Phase 4 `memory-coverage` |

Any failure that ever escapes in real life gets **added to the suite**. The system's own history becomes its test corpus. **This is the property that compounds** — every mistake makes it permanently harder to repeat.

---

## What this plan still will not catch

An A+ system knows its residual risk. **Naming these is part of the grade.**

1. **Confirmation theatre.** A `verify: human` claim that you rubber-stamp without checking is no better than an unowned one. *Mitigation:* anything numeric must carry `verify: sql`. Humans confirm **goals and intent**; machines verify **facts**. Never the reverse.
2. **The plan itself goes stale.** *Mitigation:* this file carries `expires_on: 2026-08-11` and `verify: human`. **It is subject to its own rules.** If it is not reconfirmed, `claim-expiry` will kill it and tell you.
3. **A well-formed lie from a trusted source.** If a live query returns a number and the *schema* is wrong, the substrate faithfully records a verified falsehood. *Mitigation:* none. This is the floor. It is why Rule 0.5 — verify the live system — is not replaced by any of this, only supported by it.
4. **You stop reading the pushes.** Every alerting system dies this way. *Mitigation:* keep **Needs you** short enough to always be read. If it exceeds ~5 items, the fix is triage, not a longer list.

---

## Sequence and cost

| Phase | Effort | Kills | Order rationale |
|---|---|---|---|
| 0 — Stop the bleeding | 30 min | active harm | Do now. |
| 1 — Enforcement (hooks) | 1 day | F1, F2 | First: without it, everything later decays to prose. |
| 2 — Truth (claims) | 2 days | **F3** | The A+. Depends on Phase 1 to be enforced. |
| 3 — Delivery (push) | 0.5 day | F4 | Depends on Phase 2 for expiry signals. |
| 4 — Governance | 0.5 day | F5 | Independent; can run parallel. |
| 5 — Adversarial suite | 0.5 day | regression | Last: needs 1–4 to test against. |

**~4.5 days.** Phases 0 and 1 alone (1.5 days) fix everything that actively bit you today.

**If a hard deadline is real:** do 0 and 1 only. Everything else waits, and the completion-path problem (14 checks started, 0 finished) outranks all of it.
**If it is not:** run the whole programme. It is genuinely ahead of the field, and it compounds.

---

## The one-line version

**Stop building a system that stores what you know. Build one that tells you when what you know has stopped being true.**

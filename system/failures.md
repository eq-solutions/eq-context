---
title: SYSTEM — Failure Ledger (the ratchet's memory)
owner: Royce Milmlow
last_updated: 2026-07-11
scope: Every failure that escaped the safeguards, with the rung its guard currently sits at. Machine-read by guard-ratchet.yml. Append-only for entries; rung/count are mutable.
read_priority: high
status: live
---

# SYSTEM — Failure Ledger

**This is the memory of the ratchet.** Every failure that got past the safeguards is recorded here with the rung its guard sits at. When a failure **recurs**, its guard must climb.

The ratchet only tightens. It is driven by reality — a failure that actually happened — never by opinion.

## The enforcement ladder

| Rung | Form | Catches |
|---|---|---|
| **0** | unknown | nothing |
| **1** | lesson in `lessons.md` (prose) | only if the agent reads *and* recalls it at the right instant |
| **2** | session-start checklist item | usually |
| **3** | CI check | **after** the damage |
| **4** | **hook** — enforced at the point of action | **before** the damage. Prevention. |

**The rule:** `recurrences >= 2 AND rung < 4` ⇒ `guard-ratchet.yml` opens an issue proposing promotion.
**Propose-only** (Royce, 2026-07-11) — the ratchet never merges its own changes. It argues; you decide.

> **Why prose is rung 1, not rung 3.** On 2026-07-11 the truncation lesson (F2) *existed* in `lessons.md`. The assistant *read* `lessons.md` that session. It **still truncated `CLAUDE.md`.** Knowledge that requires an agent to have retained 455 lines and recall the right one at the right moment is not a safeguard. It is hope with a timestamp.

---

## Ledger

```yaml
failures:
  - id: F1
    title: Substrate read path served 8-12 day stale content, 200 OK, no error
    first_seen: 2026-07-11
    recurrences: 1
    rung: 4
    target_rung: 4
    guard: "hooks/session_start.py — SessionStart gate (rung 4, built 2026-07-11)"
    detected_by: "human — git reflog contradicted the fetched file"
    cost: "near-revert of the 2026-07-03 contract rewrite; two false headline findings"
    note: "The §1 fallback cannot catch this — it triggers on errors, and a stale cache hit is not an error."

  - id: F2
    title: Edit/Write silently truncates long files on the C:\Projects virtiofs mount
    first_seen: 2026-05-24
    recurrences: 2
    rung: 4
    target_rung: 4
    guard: "hooks/pre_tool_use.py — PreToolUse block, fail-closed (rung 4, built 2026-07-11)"
    detected_by: "wc -l after the write"
    cost: "CLAUDE.md truncated 308->277 lines, §12/§13/End destroyed. Tool reported success."
    note: "PROMOTED 2026-07-11 — the ratchet's first closed loop. It demanded promotion; the hook was built; it went quiet. Prose failed twice; the hook cannot be forgotten."

  - id: F3
    title: A goal nobody owned governed every session for two weeks from a read_priority critical file
    first_seen: 2026-07-11
    recurrences: 1
    rung: 3
    target_rung: 3
    guard: "TODAY.md GOALS UNSET + claim-expiry.yml (rung 3, built 2026-07-12) — fails CI on an unowned/undated/expired goal"
    detected_by: "human — Royce asked 'what's that deadline? why are you mentioning it?'"
    cost: "an assistant repeatedly told Royce to defer work against a phantom deadline"
    note: "Every check passed green. auto-bump-frontmatter was faithfully keeping the phantom looking fresh. Freshness != truth. claim-expiry.yml built 2026-07-12 — F3's guard climbed 1->3; a goal now cannot sit in TODAY.md undated, unowned, or past expiry without failing CI."

  - id: F4
    title: Nothing watches the product — and the metric raised to prove it was itself over-read
    first_seen: 2026-07-11
    recurrences: 1
    rung: 0
    target_rung: 3
    guard: "PLANNED, NOT YET BUILT -> product signals in digest.md (rung 3), framed as TRANSITIONS not thresholds"
    detected_by: "human — an ad-hoc live SQL query; corrected 2026-07-12 by a second, due-date-aware query"
    cost: "REAL GAP: zero monitoring of any product signal. But the alarm that surfaced it — '14/16 created, 0 ever completed, the core workflow has never worked' — was OVER-READ. Verified live 2026-07-12: of 16 checks, 10 are live and ALL future-dated (earliest due 2026-08-06; 8 are RCD compliance seeds due 2027); the only past-due rows are soft-deleted; nothing has even been started. 0 completions is a young, forward-scheduled system, not a broken completion path."
    note: "The lesson doubled. (1) Nothing watched the product — still true, still rung 0. (2) The very first metric used to raise the alarm was un-verified against due-dates — the exact 'verified falsehood' the plan (residual risk #1) calls its floor. Mitigation: the pulse must watch TRANSITIONS (did the 2026-08-06 check complete WHEN DUE?), never a pre-due backlog. Real soft signals to watch instead of the completion count: prestarts stalled (30, last 07-04), safety modules at 0, 31 non-Royce writes/14d, last_login_at never written."

  - id: F5
    title: An ungoverned shadow memory overrode the canonical contract
    first_seen: 2026-07-11
    recurrences: 1
    rung: 0
    target_rung: 3
    guard: "none -> memory-coverage.yml (rung 3) + collapse shadow memories to thin pointers"
    detected_by: "human — traced backwards from F1"
    cost: "the Cowork preferences patch routed an agent to a stale URL instead of the authoritative local clone"
    note: "Seven memory layers. One governed. The CI audits the memory that was CORRECT. The patch written to prevent drift is what caused it."

  - id: F6
    title: Append (>>) NUL-fills files on the C:\Projects virtiofs mount
    first_seen: 2026-07-11
    recurrences: 1
    rung: 4
    target_rung: 4
    guard: "hooks/pre_tool_use.py — blocks >> to any mount path (rung 4, built 2026-07-11)"
    detected_by: "NUL-byte scan after the write — wc -l reported a SANE line count"
    cost: "3,955 NUL bytes written into system/lessons.md. Two lessons destroyed. File became binary."
    note: "Found while fixing F2 — and it INVALIDATED the F2 fix. The old lesson said 'prefer cat >> over Edit for appends'. That advice was WRONG and it corrupted the file. Only FULL REWRITE (cat >) is safe. wc -l alone will not catch this: the NUL-fill made the file LARGER."
```

---

## How to add a failure

When something escapes the safeguards — **not** when it is merely annoying, but when a guard that should have caught it did not:

1. Append an entry. `recurrences: 1`, `rung:` = whatever the guard sits at **today** (be honest; prose is rung 1).
2. If an `id` already exists for this failure class, **increment `recurrences`** — do not add a new entry. Recurrence is the whole signal.
3. `guard-ratchet.yml` does the rest. It proposes; Royce disposes.

**Do not close a failure by writing a lesson.** A lesson is rung 1. If it already had a lesson and recurred, the lesson is the thing that failed.

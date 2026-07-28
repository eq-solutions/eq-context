---
title: Decision Protocol
owner: Royce Milmlow
last_updated: 2026-07-28
scope: On-demand structured pass for choosing between options — steelman, pre-mortem, value-check, feasibility-check
read_priority: high
status: live
---

# Decision Protocol

An on-demand structured pass for weighing a choice, mid-session, while still in the technical weeds. Replaces reaching for varying ad-hoc phrasing ("steelman this" / "no mistakes" / "high value?" / "will this actually work") with one consistent set of checks.

**Distinct from `rules/reflection-protocol.md`.** Reflection audits a **finished output** against substrate before it ships (four checks: substrate conflict, vagueness, domain pushback, scope). This protocol runs **before** a choice is made — it's for deciding, not for auditing what's already written. Reflection is mandatory for its trigger categories; this protocol is always on-demand — nothing forces it.

**Trigger phrases:** "steelman this", "no mistakes", "high value?", "will this work", "run the decision protocol", or `/decide` in Claude Code / Cowork (`~/.claude/commands/decide.md` — a thin pointer to this file). Any tool that has read this file can run it from the phrases alone; the slash command is a Claude-Code-only convenience, not a requirement.

---

## The six steps

### 1. Frame it

State in one line: what's actually being decided, and what "good" means here — a goal, a constraint, a deadline. Fix a fuzzy frame before evaluating options; a well-evaluated answer to the wrong question is still wrong.

If the claimed goal traces back to `system/TODAY.md` GOALS and that section is UNSET, say so plainly — don't borrow urgency from an old file or invent one. An unset goal means step 4 has no yardstick, and that must be stated, not smoothed over.

### 2. Steelman

Give the strongest honest version of:
- the leading option (the best case someone who believed in it would make, not a strawman)
- the strongest alternative, including "do nothing" / "do it later" if that's genuinely live

If there's only one option on the table, steelman the case for *not* doing it — that's the alternative.

### 3. No-mistakes pass (pre-mortem)

Assume the leading option was chosen and it went wrong six months from now. What broke?

- 2-3 concrete failure modes, not generic risk categories.
- Flag anything **irreversible** separately — data loss, deployed auth changes, cross-entity actions, live production writes. Irreversible risks need a mitigation before proceeding, not just a note.
- Same bar as `CLAUDE.md` §4's "pre-mortem before building" — this generalizes it to any choice, not just builds.

### 4. High-value check

Value against the step-1 goal, weighed against effort and what it displaces. Three honest outcomes, pick one:

- **Yes** — clearly worth the effort against the stated goal.
- **No** — clearly not; say why, don't soften it.
- **Can't tell** — the goal isn't concrete enough to rank against. This is common and fine — surfacing it is the useful output, not a failure.

### 5. Make-it-work check

Strip the steelman gloss. Under the real constraints (time, access, who has to execute it, what's already in flight) — does the leading option actually ship, or does it just look good on paper? Name the single biggest blocker to it actually working, if one exists.

### 6. The call

One paragraph, no hedging:
- The recommendation.
- The one or two reasons it beats the step-2 alternative.
- The crux — what fact, if it turned out false, would flip this answer.

---

## Output format

Six short labeled sections, 1-3 lines each. Not an essay — if a step has nothing to add ("no irreversible risks here"), say that in one line and move on. Total should read in under a minute.

**Scale to the decision.** A trivial or reversible call (file naming, wording, which of two near-identical options) doesn't need all six sections spelled out — a one- or two-line gut check that touches the load-bearing points is enough. Reserve the full six-section output for calls that are irreversible, cross-entity, or genuinely uncertain. Running full ceremony on a small decision is the failure mode this protocol exists to avoid, not a sign of thoroughness.

---

## Why this exists

Royce already ran all four checks (steelman / pre-mortem / value / feasibility) informally, triggered by whichever phrase he remembered in the moment — inconsistent coverage, and nothing that traveled between tools. This file is the single substrate copy every tool reads via `CLAUDE.md` §8, so the same pass runs the same way in Chat, Code, Cowork, ChatGPT, or Grok — the same consistency mechanism `CLAUDE.md` §3 already uses for templates. (2026-07-28)

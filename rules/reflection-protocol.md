---
title: Reflection Protocol
owner: Royce Milmlow
last_updated: 2026-07-23
scope: Mandatory pre-finalization self-critique gate for high-stakes outputs
read_priority: high
status: live
---

# Reflection Protocol

A mandatory one-pass self-critique before finalizing certain outputs. Distinct from the on-demand self-critique in `CLAUDE.md` §4 ("stress test this" / "devil's advocate" / "10/10 version") — that one fires on request; this one fires automatically for the categories below, without being asked.

**Enforcement is partial, and the split is deliberate, not an oversight.**

- **EQ Field build commits ARE mechanically gated.** `~/.claude/hooks/guard.js`'s `reflection-gate` rule blocks `git commit` in `eq-field` whenever eq-field files are staged without a paired `docs/reflection-log.md` entry in the same commit. The `/reflect` command (`~/.claude/commands/reflect.md`) runs the four checks and stages that entry. This fires at commit time, not at every edit — a deliberate choice: gating every `Edit` call fires on trivial WIP edits long before any real decision exists to reflect on, and can't see the chat discussion where the actual decision gets made anyway. Commit time is the last checkpoint before it's final, and it makes the log durable and PR-visible instead of a disposable flag only this machine ever sees. Skippable via `EQ_SKIP_REFLECT=1`, same escape-hatch convention as the existing brief-gate.
- **SKS ops/commissioning docs and any chat-only output stay self-reported, not by oversight but by mechanical limit.** A `PreToolUse` hook only ever sees tool calls — it cannot see chat prose, and most SKS deliverables (a quote, an emailed summary, a Word doc handed to Mark Brame) have no reliable file-path signature a hook could key on. There is no version of this rule that closes that gap without either false-positiving on unrelated files or requiring content-understanding no hook has. For those two categories, this is still the same trust-the-model's-honesty gap `system/TODAY.md` already learned to distrust (`system/lessons.md`, "The Substrate Contained a Goal Nobody Owned") — know that going in, don't let the existence of a gate for EQ Field imply the other two categories are covered too.
- **What the gate does NOT verify, even for EQ Field:** content quality. A lazy one-line "nothing changed, looks fine" entry technically satisfies it. The gate forces a paper trail to exist and ship in the PR where a human reviewer can see it — it does not grade whether the reasoning behind it was any good.
- **`guard.js` itself is unversioned.** It lives at `~/.claude/hooks/guard.js`, outside any git repo, with no test coverage — unlike `hooks/*.py` in this repo, which are governed, versioned, and CI-checked (see `hooks/README.md`). The `reflection-gate` rule was added there, same as the rest of that file. Tracked as a follow-up in `eq/pending.md`, not fixed here.

---

## When this gate applies

MUST run before finalizing:
- EQ Field feature/build decisions
- SKS operational docs, commissioning reports, or scheduling outputs
- Any output that will be read by someone outside this session (Mark Brame, SKS team, EQ stakeholders)

SHOULD be skipped for: routine formatting, straightforward status pulls, simple lookups.

---

## The four checks

1. **Substrate conflict** — does this contradict anything in `/eq`, `/sks`, `/ops`, or `/system`? If yes, substrate wins — flag it explicitly, don't quietly reconcile.
2. **Vagueness check** — any claim that sounds confident but isn't backed by a substrate fact or explicit input? Flag or cut it.
3. **Domain pushback** — what would Mark Brame (ops) or a tradie end-user (EQ Field) actually object to here? Say it, don't soften it.
4. **Scope check** (EQ Field only) — does this go beyond "SKS-internal validation first"? If it reaches toward deprioritised builds (Ops, Variations, Quotes), stop and flag.

---

## Output format

State the critique findings briefly before the revised output — 2-4 bullet lines: what was checked, what changed (if anything). Not a separate essay.

If nothing changed, say so. Do not manufacture a critique for the sake of it.

**One pass only.** Do not loop reflection multiple times — diminishing returns past pass one, and repeated critique on the same output tends to introduce noise rather than catch real problems.

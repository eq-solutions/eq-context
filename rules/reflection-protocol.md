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

**Compliance here is self-reported, not enforced.** There is no CI check or hook verifying a session actually ran these checks — only the model's own honesty about what changed. Treat this the same way `system/TODAY.md` treats its own goals section: a doc that looks authoritative but isn't backed by verification is a known failure shape in this substrate (`system/lessons.md`, "The Substrate Contained a Goal Nobody Owned"). Don't let this file's presence substitute for actually running the checks.

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

---
title: SYSTEM — MD Style Standard
owner: Royce Milmlow
last_updated: 2026-08-08
scope: Style standard for all MD files in eq-context
read_priority: reference
status: live
---

# SYSTEM — MD Style Standard

Slimmed 2026-05-04 from MD_BEST_PRACTICES.md (498 → ~90 lines). Updated
2026-08-08 to close two enum drifts against live practice (see below) and
add pending/session-log/fact-ownership guidance that existed in practice
but was never written down. Only the rules AIs need to apply. Historical
reasoning lives in git history.

---

## Frontmatter — required on every file

```yaml
---
title: <short human title>
owner: <person responsible>
last_updated: 2026-05-30
scope: <one line — who/what this applies to>
read_priority: critical | high | standard | reference
status: draft | live | archived | deprecated
---
```

`read_priority` lets a session-start script load `critical` files first
when the context window is tight. `high` sits between `critical` and
`standard` — daily-operational files (digest, failures, DR runbooks)
that aren't session-start-blocking but matter more than plain reference
material.

`status: deprecated` is enforced by the F8 pre-commit hook alongside the
other three values — this enum drifted out of sync with that hook after
it shipped 2026-08-04; fixed here.

---

## Tool-neutral writing

Substrate prose references *actions*, not *actors*. The same file is
read by Claude, ChatGPT, Cursor, Cowork, Code, Grok, future tools — naming
one tool dates the file.

| Avoid | Prefer |
|-------|--------|
| "Claude must…" | "The assistant must…" |
| "Ask Claude to…" | "At session start…" |
| "Cowork updated the schema" | "Schema updated to…" |

**Exception:** Anthropic-primitive references (`AskUserQuestion`, MCP tool
IDs, specific worker names) are fine — those are concrete artifacts, not
vendor branding.

Slogan: *Substrate prose is tool-neutral. Reference the action, not the actor.*

---

## File update rules

| File type | Discipline |
|---|---|
| `*/pending.md` | Overwrite in place. Tick or remove items when done. Cap active open items (see Pending hygiene below). |
| `*/products.md` | Overwrite in place. Refresh status when products change. |
| `ops/decisions.md` | **Append-only.** Never delete an entry — supersede or deprecate. |
| `system/lessons.md` | **Append-only.** New lessons go at the bottom. |
| `*/changelog/*.md` | **Append-only.** Per-product history. |
| `sessions/*.md` | **Append-only.** One file per ISO date; same-day sessions append with a `---` divider. Never edit a prior day's entries. |
| `system/architecture.md` | Overwrite when how something is built changes. |
| `rules/*.md` | Rare. Annual review only — see `ops/decisions.md` 2026-04-28. |
| `system/TODAY.md` | Goals are human-owned only. Assistants MUST NOT write goals — propose only. |

---

## Pending hygiene

`pending.md` is a work queue, not a diary.

- **Active open cap (proposed target, not yet confirmed):** EQ ≤ 100 real
  engineering items; SKS ≤ 40; OPS ≤ 30. *(Flagged here as proposed, not
  settled — confirm before treating as an enforced number.)*
- "Waiting on Royce / click-test" items belong in a clearly tagged
  section or separate file so they don't dilute engineering backlog —
  `verify-queue.md` already exists for this per-tier.
- Items with no activity for 45+ days must be killed, deferred with a
  new date, or promoted — `digest.md`'s "Aging 45d+" column already
  tracks this signal; this rule is what to *do* about it.
- Done items must be rotated out via the existing `rotate_pending.py`
  path. Unrotated done history is noise.

---

## Sessions

`sessions/YYYY-MM-DD.md` (or `sessions/YYYY-MM-DD-<part>.md`) is a
decision-and-outcome log, not a transcript. Required shape, matching
what's actually in use across the substrate today:

```markdown
# Session YYYY-MM-DD — <one-line outcome>

## Built
- What actually changed, one line per item.

## Decided
- Decisions confirmed by Royce, one line each.

## Deferred
- Items flagged but not built, with reason.

## Notes
Anything that would otherwise be lost — constraints discovered,
substrate corrections, gotchas.
```

Do not paste long narratives that belong in a product changelog.
Changelogs are the durable product history; sessions point at them.

---

## ADR format for `ops/decisions.md`

Every entry:

```markdown
## YYYY-MM-DD — Title

**Status:** Accepted | Superseded by YYYY-MM-DD <title> | On Hold | Deprecated | Proposed

**Decision:** What was decided.
**Why:** Reasoning at the time.
**Alternatives considered:**
- Option X (rejected because Y).
**Implications:** What this means going forward.
```

Append-only. When a decision is superseded, the new decision's title is
appended to the old entry's Status line; both entries remain.

---

## RFC 2119 in `rules/*`

- **MUST / MUST NOT** — absolute.
- **SHOULD / SHOULD NOT** — strong default; document deviations.
- **MAY** — permitted.

A meaning-altering rewrite is a decision-grade change — surface via the
relevant tier's `pending.md`, not committed inline.

---

## Cross-references

When pointing at another file, use the path from repo root: `eq/pending.md`,
`ops/decisions.md`, `system/architecture.md`. Never relative paths.

When citing a section: `ops/decisions.md` 2026-04-28 (date-suffixed
section title) or `rules/non-negotiables.md §0` for numbered sections.

**`sks-team/` is the exception:** files in that tier MUST NOT cross-reference
any other tier — they stand alone. If a fact in `sks-team/` is needed from
elsewhere (e.g. brand colours from `rules/brand-sks.md`), copy the fact in rather
than linking. The cost of duplication is the price of separability — the
tier needs to extract cleanly to its own substrate later, and cross-references
make that mechanical move into a rewrite.

---

## One fact, one home

If a fact already has a home, point at it. Do not restate it in a second file.

| Kind of fact | Home |
|---|---|
| Hard behavioural rule | `rules/non-negotiables.md` or `rules/agentic-coding.md` |
| Product status | `eq/products.md` / `sks/products.md` |
| Decision | `ops/decisions.md` |
| Lesson / gotcha | `system/lessons.md` |
| Open work | tier `pending.md` |
| Product history | `*/changelog/*.md` |
| Session outcome | `sessions/YYYY-MM-DD.md` (short; points elsewhere) |

Duplication creates two answers and no way to tell which drifted.

---

## Naming

- Sessions: `sessions/YYYY-MM-DD.md`, or `sessions/YYYY-MM-DD-<part>.md` when a day spans multiple sessions (ISO date prefix required)
- Changelogs: `eq/changelog/<product>.md` or `sks/changelog/<product>.md`
- Drafts: short slug + date if needed, e.g. `eq/field/multi-tenancy/`
- Archive: descriptive single file, e.g. `archive/changelog-eq-quotes.md`

Never rename existing files in-place — create new + archive old via
frontmatter `status: archived`.

---

## Length discipline

| Signal | Action |
|---|---|
| File grows past ~one screen for its job | Split into linked sub-files |
| `pending.md` open items exceed the tier cap | Rotate aging / low-signal items to archive |
| Session log becomes a novel | Cut to decisions + outcomes; durable history goes in the product changelog |

Files read at session start (`CLAUDE.md`, `AGENTS.md`, tier `README.md`,
`pending.md`, `active.md`, `digest.md`, `system/TODAY.md`) must stay
scannable. Long files quietly stop being read; short, focused files
compound value.

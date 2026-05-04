---
title: SYSTEM — MD Style Standard
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Style standard for all MD files in eq-context
read_priority: reference
status: live
---

# SYSTEM — MD Style Standard

Slimmed 2026-05-04 from MD_BEST_PRACTICES.md (498 → ~90 lines). Only the
rules AIs need to apply. Historical reasoning lives in git history.

---

## Frontmatter — required on every file

```yaml
---
title: <short human title>
owner: <person responsible>
last_updated: YYYY-MM-DD
scope: <one line — who/what this applies to>
read_priority: critical | standard | reference
status: draft | live | archived
---
```

`read_priority` lets a session-start script load `critical` files first
when the context window is tight.

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
| `*/pending.md` | Overwrite in place. Tick or remove items when done. |
| `*/products.md` | Overwrite in place. Refresh status when products change. |
| `ops/decisions.md` | **Append-only.** Never delete an entry — supersede or deprecate. |
| `system/lessons.md` | **Append-only.** New lessons go at the bottom. |
| `*/changelog/*.md` | **Append-only.** Per-product history. |
| `sessions/*.md` | **Append-only.** One file per ISO date. Never edit past sessions. |
| `system/architecture.md` | Overwrite when how something is built changes. |
| `rules/*.md` | Rare. Annual review only — see `ops/decisions.md` 2026-04-28. |

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

---

## Naming

- Sessions: `sessions/YYYY-MM-DD.md` (ISO date, one file per session day)
- Changelogs: `eq/changelog/<product>.md` or `sks/changelog/<product>.md`
- Drafts: short slug + date if needed, e.g. `eq/field/multi-tenancy/`
- Archive: descriptive single file, e.g. `archive/changelog-eq-quotes.md`

Never rename existing files in-place — create new + archive old via
frontmatter `status: archived`.

---

## Length discipline

Files that AIs read at session start (`CLAUDE.md`, `AGENTS.md`,
tier `README.md`, `pending.md`, `active.md`) **must fit on one screen
when scanned**. If a file grows past one screen, split into linked
sub-files. The substrate compounds value when files stay short and
focused; long files quietly stop being read.

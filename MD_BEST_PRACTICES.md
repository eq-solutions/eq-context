---
title: MD Best Practices — Cross-LLM Context Files
owner: Royce Milmlow
last_updated: 2026-04-10
scope: All MD files in eq-context and any future context repos (EQ, SKS, AHD)
read_priority: reference
status: v1.0
---

# MD Best Practices — Cross-LLM Context Files

Direction for writing Markdown context files that work equally well across
Claude (Chat, Cowork, Code), Perplexity, ChatGPT, Gemini, Cursor, and any
other LLM tool that may read this repo in the future.

The goal is one source of truth that any model can parse without
tool-specific tricks.

---

## 1. Naming and entry points

The industry is converging on `AGENTS.md` as the canonical root file that
any LLM tool can load first (Cursor, OpenAI Codex, JetBrains, and others
already recognise it). Claude Code still looks for `CLAUDE.md`.

**Recommendation for this repo:**

- Keep `CLAUDE.md` (Claude Code auto-loads it).
- Add `AGENTS.md` at root as a thin pointer — one paragraph that says
  "start by reading CLAUDE.md, then state/pending.md". Do not duplicate
  content; symlinks break on Windows so use a pointer file.
- `README.md` stays human-focused (for future contributors).

Result: Claude, Cursor, Codex, Perplexity and any human all land somewhere
sensible without reading a tool-specific name.

---

## 2. Frontmatter (YAML) on every file

Every context file should open with a small YAML block. It is invisible
to most renderers, parseable by every LLM, and gives a machine-readable
header for search, filtering, and validation.

Minimum fields:

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

## 3. Write tool-agnostic, not Claude-specific

Current `CLAUDE.md` says things like "Claude reads this first". That still
works but locks thinking to one tool. Prefer neutral phrasing so the same
file is usable in Perplexity or a future model without rewrites.

| Avoid | Prefer |
|-------|--------|
| "Claude must…" | "The assistant must…" |
| "Ask Claude to…" | "At session start…" |
| "Claude in Chrome will…" | "When using a browser-capable agent…" |
| Tool-specific file names in prose | Relative paths: `state/pending.md` |

Exception: tool-specific behaviour (e.g. "Claude Code uses git CLI") stays
in a dedicated section clearly marked as tool-specific.

---

## 4. Structure: hierarchical, not sprawling

One concern per file. The current split (`rules/`, `state/`, `knowledge/`,
`sessions/`, `changelog/`) is already correct — keep it. Guardrails:

- **H1 = file title only.** One H1 per file, same as the YAML title.
- **H2 = major section.** Never skip levels (no H1 → H3).
- **Tables for registers.** Entities, accounts, site registry, palettes.
  Tables compress well and every LLM parses them cleanly.
- **Bullets for rules.** Numbered only when order matters (e.g. a protocol).
- **Horizontal rules (`---`) between sections.** Helps models chunk cleanly.
- **Keep any single file under ~400 lines.** If it grows, split by concern.

---

## 5. Top-load the critical rules

Models weight earlier tokens more heavily. First 20 lines of any
"rules" file should be the things that must never be violated. Detail,
rationale and edge cases come after.

`rules/non-negotiables.md` already does this well — model the rest on it.

---

## 6. Dates: absolute, ISO 8601, always

Never "last Thursday", "yesterday", "next quarter". Always `YYYY-MM-DD`.

- `last_updated` in frontmatter every file.
- Section-level dates in append-only logs (lessons, decisions, sessions,
  changelog).
- When the user says "Thursday", convert to the ISO date before writing.

Reason: context files are re-read weeks or months later by a model that
has no memory of when "Thursday" was.

---

## 7. Append-only vs. living state

Treat files as one of three types — and never mix them:

| Type | Examples | Rule |
|------|----------|------|
| **Rules** | `rules/*.md`, `CLAUDE.md` | Rarely change. Each change is deliberate. |
| **State** | `state/pending.md`, `state/products.md` | Overwrite in place — only current truth. |
| **Logs** | `knowledge/lessons.md`, `knowledge/decisions.md`, `sessions/*`, `changelog/*` | Append only. Never delete or edit historical entries. |

Mixing these is the most common failure mode: decisions get overwritten,
state gets stale, or rules get "temporary" exceptions that stick.

---

## 8. Token budget per file

Rough targets for this repo:

- `CLAUDE.md` / `AGENTS.md`: **under 2000 tokens** (~300 lines). Currently
  fine. Delegate detail to subfiles.
- `rules/*`: under 150 lines each.
- `state/*`: as short as possible — it is current state, not history.
- Logs: no limit (append only), but split by year if they exceed ~1000
  lines.

If `CLAUDE.md` grows, the first instinct should be "extract to subfile",
not "add a new H2".

---

## 9. Line width and formatting hygiene

- **Wrap prose at ~100 chars** for clean git diffs and readable blame.
- **Never use tabs.** Two-space indent inside lists.
- **No emoji in rules or registers.** They are token-heavy, render
  inconsistently across tools, and add nothing searchable. Acceptable in
  session logs where personality is wanted.
- **Use fenced code blocks** with language tags for any snippet (` ```yaml `,
  ` ```bash `) — improves model parsing.
- **Relative links only** (`state/pending.md`), never absolute GitHub URLs
  that break on local clones.

---

## 10. Stable slugs — never rename files

Once a file exists at `knowledge/decisions.md`, it stays there forever.
Renaming breaks every existing reference from memory, from commit
messages, and from cross-tool links.

If a file's purpose drifts, create a new file and mark the old one
`status: archived` in frontmatter — do not rename.

---

## 11. Session-start protocol should be universal

The current protocol is Claude-specific. Generalise it:

> At session start, any assistant working on EQ/SKS context should:
> 1. Read `CLAUDE.md` (or `AGENTS.md` — they are equivalent entry points)
> 2. Read `state/pending.md`
> 3. Read any `changelog/[PROJECT].md` relevant to the work being requested
> 4. Confirm context before taking any action

This works for Claude Code, Cowork, Chat, Cursor, Codex, Perplexity
research mode, or a human contributor.

---

## 12. Writing for Perplexity specifically

Perplexity ingests public content via URL and cites paragraph-level.
If any of this repo ever becomes public (AHD white papers, EQ product
docs), these rules apply:

- **Lead with the answer, then the reasoning.** Perplexity quotes the
  first strong sentence under a heading.
- **One idea per paragraph.** No walls of text.
- **Factual claims get a source link inline** — Perplexity preserves
  links when citing.
- **Tables and lists get cited as units** — keep rows self-contained
  (don't say "see row above").

For internal files that stay private this is lower priority, but adopting
the style costs nothing and makes future publication trivial.

---

## 13. Things to stop doing

Based on review of the current repo (2026-04-10):

1. **`Last updated:` dates drifting.** Several files still show 2026-04-05
   even though the system was updated on 2026-04-06. Either bump on every
   edit or remove the line and rely on git.
2. **Session URLs pasted into changelogs.** `claude.ai/chat/...` links
   expire and leak. Use a short session ID or drop them.
3. **Two competing "Why" sections** between `knowledge/architecture.md`
   and `knowledge/decisions.md` — overlap by ~60%. Rule going forward:
   **decisions** = the call + alternatives, **architecture** = the
   current state of how it works. Migrate, do not duplicate.
4. **Mixed H1 styles.** Some files use `# Rules — Deployment`, others
   `# State — Pending Actions`. Pick one convention (recommended:
   `# <Category> — <Subject>`) and apply uniformly.

---

## 14. Validation checklist (run before committing any MD change)

- [ ] YAML frontmatter present and `last_updated` is today
- [ ] One H1 only
- [ ] All dates in ISO 8601
- [ ] No Claude-specific phrasing in a file meant to be tool-agnostic
- [ ] Tables used for any structured/tabular data
- [ ] No tool-specific URLs (claude.ai, cursor.sh, etc.) in living docs
- [ ] File is under its token budget
- [ ] Append-only files were appended to, not edited in place
- [ ] No emoji in rules/registers
- [ ] Relative links only

---

## 15. Migration plan for this repo

Ordered by impact, low effort first:

1. Add `AGENTS.md` pointer file at root (5 minutes).
2. Add YAML frontmatter to all existing files with correct
   `last_updated` bumped to 2026-04-10 (30 minutes).
3. Run a pass to replace "Claude" with "the assistant" everywhere except
   `CLAUDE.md` Session Start Protocol (15 minutes).
4. Split `knowledge/architecture.md` and `knowledge/decisions.md` per
   rule in §13.3 (60 minutes).
5. Add this file (`MD_BEST_PRACTICES.md`) to `CLAUDE.md` as a reference
   link so future sessions know the standard exists.

---

## 16. What this replaces

Nothing is deleted by this document. It is the style guide that every
other MD file in the repo should be measured against going forward.

---
title: EQ UI — Changelog
owner: Royce Milmlow
last_updated: 2026-07-26
scope: eq-ui (@eq-solutions/ui) append-only history — substrate summary of merges. The package's own CHANGELOG.md (Changesets-generated) is the authoritative version history; this file is for cross-repo context.
read_priority: reference
status: live
---

# eq-ui changelog

## 2026-07-26 (PR #33, Tooltip/EmptyState/Pagination — published v1.12.0)
- **PR #33 (MERGED, `b8a0304`) — added Tooltip, EmptyState, and Pagination components, closing three real gaps in the shared library found while building the kitchen-sink reference.** Originated as a Claude Design handoff (real TSX/CSS against the repo's own conventions, not mockups); reviewed by actually copying the files in and running the real toolchain rather than trusting the handoff's own self-description. Found and fixed two real issues before merging: a `jsx-a11y/no-static-element-interactions` lint failure in Tooltip (Escape-key handling had been on a non-interactive `<span>`'s `onKeyDown` — moved to a document-level listener matching `DropdownMenu`'s existing close-on-Escape pattern) and a props-shape mismatch (EmptyState/Pagination didn't extend native HTML attributes or forward refs/rest props, unlike sibling components `Card`/`StatusBadge` — now aligned). All three components use existing `--eq-*` tokens only, no new tokens introduced. `npm run check` (typecheck + check:tokens + lint + test) green, 43/43 tests passing; manually verified live in the `npm run dev` kitchen-sink preview (Tooltip hover/focus, Pagination click-through, no console errors). Published as `@eq-solutions/ui@1.12.0` via the existing Changesets → GitHub Packages pipeline.

---
title: EQ UI — Changelog
owner: Royce Milmlow
last_updated: 2026-08-12
scope: eq-ui (@eq-solutions/ui) append-only history — substrate summary of merges. The package's own CHANGELOG.md (Changesets-generated) is the authoritative version history; this file is for cross-repo context.
read_priority: reference
status: live
---

# eq-ui changelog

## 2026-08-12 (PR #38, MultiSelect — open, not yet merged)
- **PR #38 (OPEN, CI green)** — new `MultiSelect` component: trigger + popover checklist for picking a set of discrete values, chips for 1-2 selections collapsing to a count for 3+, search box past 8 options, density-aware. Deliberately standalone — doesn't share code with Table's own filter popover, decided via a full `/decide` pass rather than assumed (the code-sharing question was the actually risky/unverified part of the original sprint scope; the general-purpose component itself was low-risk). `npm run check` green, 89/89 tests. axe caught a real bug in development: `role="listbox"` requires `role="option"` children, not native checkboxes — fixed to `role="group"`. Not merged yet — Royce needs to do it himself (same classifier restriction all session).

## 2026-08-12 (PR #36/#37, EmptyState variants + density mode + DateRangePicker — published v1.14.0)
- **PR #36 (MERGED) — three additive components/props, scoped against live repo state rather than the design-direction doc's own claims** (doc had drifted: EmptyState's action slot was already shipped, only 2 of 16 components had a density hook despite the doc's stated rule).
  - `EmptyState` gets a `variant` prop (`filtered`/`error`/`no-access`) with default icons; `error` gets the red token tone. `default` unchanged.
  - `density?: 'comfortable'|'compact'` added to FormInput, Pagination, StatusBadge, KindPill, DropdownMenu, matching Table's existing `data-density` convention. Button and Card deliberately excluded — already have equivalent control via `size`/`padding`.
  - New `DateRangePicker` component — trigger + popover calendar, 5 presets, `min`/`max` bounds, density-aware. No new dependency (native `Date`/`Intl.DateTimeFormat`, no date-fns).
  - Backfilled README sections for EmptyState, Pagination, DropdownMenu (none existed since #32/#33).
  - `npm run check` green, 77/77 tests. Version Packages PR [#37](https://github.com/eq-solutions/eq-ui/pull/37) merged same day, published as `@eq-solutions/ui@1.14.0` — confirmed via the release workflow's own publish log, not assumed.

## 2026-07-27 (PR #34/#35, Table column reorder + composite-column filters — published v1.13.0)
- **PR #34 (MERGED) — Table's Columns popover gets move-up/move-down reorder buttons**, order persisted to localStorage alongside the existing show/hide state (`persistKey`). Chose buttons over native drag-and-drop deliberately — full keyboard/touch support, and native HTML5 drag-and-drop doesn't work reliably in the jsdom test environment this package tests against.
- Same PR adds two new optional `TableColumn` props, **`filterValue`** and **`exportValue`** — let a composite column (e.g. a merged "Contact" cell built from two underlying fields) participate correctly in global search, the per-column text filter, and CSV export. Previously these silently fell back to a nonexistent `row[key]`, matching no search/filter and exporting a blank cell (the pre-existing "Licences & review" column in eq-shell's Staff table has exactly this gap today, unfixed — not in scope for this PR).
- Prompted by eq-shell's Staff table: Royce asked to simplify the table and make columns reorderable. `npm run check` (typecheck + tokens + lint + vitest) green, 47/47 tests (4 new: reorder + boundary disabling, filterValue-driven search, exportValue-driven CSV). Changeset included (minor). Version Packages PR [#35](https://github.com/eq-solutions/eq-ui/pull/35) merged same day, published as `@eq-solutions/ui@1.13.0`.
- Consumed by eq-shell [PR #1051](https://github.com/eq-solutions/eq-shell/pull/1051) same day (open, not yet merged as of session close).

## 2026-07-26 (PR #33, Tooltip/EmptyState/Pagination — published v1.12.0)
- **PR #33 (MERGED, `b8a0304`) — added Tooltip, EmptyState, and Pagination components, closing three real gaps in the shared library found while building the kitchen-sink reference.** Originated as a Claude Design handoff (real TSX/CSS against the repo's own conventions, not mockups); reviewed by actually copying the files in and running the real toolchain rather than trusting the handoff's own self-description. Found and fixed two real issues before merging: a `jsx-a11y/no-static-element-interactions` lint failure in Tooltip (Escape-key handling had been on a non-interactive `<span>`'s `onKeyDown` — moved to a document-level listener matching `DropdownMenu`'s existing close-on-Escape pattern) and a props-shape mismatch (EmptyState/Pagination didn't extend native HTML attributes or forward refs/rest props, unlike sibling components `Card`/`StatusBadge` — now aligned). All three components use existing `--eq-*` tokens only, no new tokens introduced. `npm run check` (typecheck + check:tokens + lint + test) green, 43/43 tests passing; manually verified live in the `npm run dev` kitchen-sink preview (Tooltip hover/focus, Pagination click-through, no console errors). Published as `@eq-solutions/ui@1.12.0` via the existing Changesets → GitHub Packages pipeline.

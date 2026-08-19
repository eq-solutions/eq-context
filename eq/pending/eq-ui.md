---
title: EQ UI — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-19
scope: EQ UI engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ UI — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-ui: design-direction sprint (EmptyState variants, density mode, DateRangePicker) + suite-wide version bump (2026-08-12)

- [ ] Inline-edit primitives for Table — still deferred, needs its own spike on whether Table's cell/row model can support it cleanly; `Table.tsx` is already 1,265 lines. _(added 2026-08-12)_
- [ ] Whether Table's own column filters should ever be rebuilt on top of the new `MultiSelect` component — low priority, only worth revisiting if the inline-edit spike above happens anyway and touches the same filter code. Not blocking anything; `MultiSelect` shipped standalone (eq-ui PR [#38](https://github.com/eq-solutions/eq-ui/pull/38)) specifically so it didn't have to wait on this. _(added 2026-08-12)_

---

## eq-ui: two Table/Skeleton PRs open from an eq-shell Staff-table session (2026-08-19)

- [ ] [PR #40](https://github.com/eq-solutions/eq-ui/pull/40) — opt-in `multiSlicer` prop on `Table` (click-to-toggle, AND-combined slicer chips) for eq-shell's Staff page. Default `false`, verified against all 8 existing `slicers=` call sites in eq-shell (2 use controlled `activeSlicer`/`onSlicerChange` — unaffected). typecheck/lint/tests clean. Needs Royce's merge sign-off, then the Changesets version-packages PR, then eq-shell's pin bump. _(added 2026-08-19)_
- [ ] [PR #41](https://github.com/eq-solutions/eq-ui/pull/41) — `Skeleton` shimmer-sweep animation replacing the opacity pulse, plus a `prefers-reduced-motion` fallback the old pulse never had. Applies to every existing `Skeleton` usage automatically once released — no prop change. Same release-pipeline dependency as #40. _(added 2026-08-19)_

---


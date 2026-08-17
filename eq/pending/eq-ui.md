---
title: EQ UI — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-17
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


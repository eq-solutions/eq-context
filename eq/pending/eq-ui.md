---
title: EQ UI — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-20
scope: EQ UI engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ UI — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-ui: Table's "Show columns" popover ran past the bottom of the screen — root-caused, fixed, PR open (2026-08-20)
*Royce, from a screenshot of eq-shell's Staff page: the "Show columns" dropdown gets cut off when the table's filtered to be smaller. Investigated rather than guessed — same session that had just added a 12th column to that same list.*

- [x] **Root cause**: the popover is portalled to `document.body` (already solves an ancestor's `overflow-y:auto` clipping it) but had no cap on its own height. Its `top` is a fixed pixel offset below the trigger button, with nothing bounding how far the column list can extend below that — a short/filtered table, or just a long enough column list (now 12 for Staff), pushes it past the bottom of the viewport with no way to scroll to the rest.
- [x] **Fix**: cap `maxHeight` to the space actually available below the button, `overflow-y: auto` on the popover — correct regardless of row count or column count, not just the specific case reported.
- [x] Verified with a real install, not the local pre-commit hook (which silently no-ops without `node_modules` and was reporting a false blocking error on every edit) — `npm run typecheck` clean, `eslint` on the touched file clean (1 pre-existing unrelated warning). Confirmed the one typecheck failure seen along the way (`src/test-utils/axe.ts`, a pnpm/TS module-resolution quirk) is pre-existing on unmodified `origin/main`, not caused by this change.
- [x] Changeset added (patch). eq-ui [PR #49](https://github.com/eq-solutions/eq-ui/pull/49), built in an isolated worktree (root checkout was occupied by another session earlier today).

**Deferred:**
- [ ] **Not merged** — Royce's call, same as everything else this session.
- [ ] **Not click-tested live** — no consuming app available in this environment to open Staff, filter it small, and confirm the popover now scrolls instead of clipping. _(added 2026-08-20)_
- [ ] **eq-shell's `@eq-solutions/ui` pin still needs a manual bump** once this ships a version/tag — see `eq/pending/eq-shell.md` (2026-08-20) for the eq-shell-side half of this. _(added 2026-08-20)_

---

## eq-ui: design-direction sprint (EmptyState variants, density mode, DateRangePicker) + suite-wide version bump (2026-08-12)

- [ ] Inline-edit primitives for Table — still deferred, needs its own spike on whether Table's cell/row model can support it cleanly; `Table.tsx` is already 1,265 lines. _(added 2026-08-12)_
- [ ] Whether Table's own column filters should ever be rebuilt on top of the new `MultiSelect` component — low priority, only worth revisiting if the inline-edit spike above happens anyway and touches the same filter code. Not blocking anything; `MultiSelect` shipped standalone (eq-ui PR [#38](https://github.com/eq-solutions/eq-ui/pull/38)) specifically so it didn't have to wait on this. _(added 2026-08-12)_

---


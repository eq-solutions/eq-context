---
title: Sprint — Resourcing / Shell Conversations close-out
owner: Royce Milmlow
last_updated: 2026-08-13
scope: Remaining items from the Shell Conversations + Resourcing dashboard thread (2026-08-11 → 2026-08-13) — everything still open after the build work landed
read_priority: standard
status: live
duration_estimate: All Royce-gated — no further build required to close R1-R3; R4/R5 are future scope, not this sprint
shipped: R1
pending: R2 (click-through), R3 (team linking)
---

# Sprint — Resourcing / Shell Conversations close-out

**Status:** in flight — opened 2026-08-13. The build phase (Conversations log, permission hardening, Resourcing dashboard, draft org chart, team/supervisor write path, desktop Table swap) is fully merged. What's left is Royce actions only — no more build.

---

## Objective

Close out the loose ends from the Shell Conversations + Resourcing feature arc so the section can archive out of `pending.md`. Nothing here needs new code — R1-R3 are: merge the last PR, click through the feature live once, and use the write path already shipped to link the remaining unlinked staff to teams.

---

## In-scope items

### R1 — Merge PR #1324 (Resourcing desktop → eq-ui Table)

**Why:** Swapped the Resourcing desktop view from a hand-rolled grouped-card list to eq-ui's `Table` component — sortable columns, per-column filters, global search, column show/hide (persisted per user), CSV export. Mobile view untouched. This was the scoped ask ("do the Table swap first, hold off on the rest") — the rollup/trend/"my reports" ideas raised alongside it were deliberately not built (see Out of scope below).

**Status:** ✅ Done — merged 2026-08-13 (`4590831d`), branch deleted. Netlify auto-deploy to core.eq.solutions triggered on merge; not yet click-through verified (see R2).

**Action:** ~~Royce reviews + merges~~ [eq-shell PR #1324](https://github.com/eq-solutions/eq-shell/pull/1324) — done.

**DoD:** Merged to `main` ✅. Live on core.eq.solutions — pending Netlify deploy confirmation.

**Blast radius:** UI-only change to one page (`StaffResourcingPage.tsx`), gated behind the existing `staff.manage_conversations` permission (held by exactly one user today). No schema or auth changes.

---

### R2 — Royce's live click-through

**Why:** No sandbox in this environment has Supabase credentials, so nothing in this arc has been exercised through the real UI yet — every fix has been verified by build + live-DB query, not by a signed-in session. Carried in `pending.md` since 2026-08-11 through every subsequent fix.

**Action:** From a real Shell session as `royce.milmlow@sks.com.au`:
1. Log a conversation (Check-in, Development Review, and a Casual note) on a staff record
2. Add a rating
3. Assign someone off the Unassigned list on the org chart
4. Open Resourcing desktop view (once R1 lands) — confirm sort/filter/search/column-toggle/CSV export all work against real data

**DoD:** All four confirmed working, or a specific breakage reported back.

**Blast radius:** None — read/write against your own tenant, all already-shipped code paths.

---

### R3 — Link the remaining unlinked staff to teams

**Why:** The org chart is explicitly labelled draft because team links were never a required field on staff records. First measured 2026-08-11 at 32 of 88 active staff with no team link; live re-check today (2026-08-13) shows **35 of 103** — the gap hasn't closed on its own and the active headcount has grown, so it'll keep growing until someone works through it. The write path (`staff.manage_teams`, PR #1321) has existed since 2026-08-13 specifically to fix this — this item is just using it.

**Action:** Royce drags the 35 unlinked staff onto their teams via the org chart's assignment UI.

**DoD:** 0 unlinked active staff, org chart draft label can come off.

**Blast radius:** None — data entry only, through the already-shipped write path.

---

## Out of scope (deliberately parked)

| Item | Why parked | Next sprint? |
|---|---|---|
| Proactive "overdue for review" nudges | Deliberately held per `/decide` 2026-08-12 — no conversation data exists yet for staleness to mean anything. Revisit once R2 produces real data. | After R2 |
| Resourcing rollup/trend view ("who's overdue across the team") | Raised in the original 2026-08-13 discussion alongside the Table swap; Royce explicitly said "do the Table swap first, hold off on the rest." Not scoped or estimated. | Royce-driven |
| "My reports" manager-scoped view | Same discussion, same hold. | Royce-driven |
| Org chart: pull teams from Field instead of Shell's own drag-and-drop | Discussed and settled 2026-08-13, not deferred — Field's `field_teams`/`field_team_members` are read-only views over the *same* `app_data.teams`/`team_members` tables Shell's org chart already edits. Rebuilding against Field would mean editing a view of your own data through a second UI. Current design (Shell owns the write, Field inherits it live) is correct as-is — no action item. | N/A — closed by design |

## Sprint success criteria

- [x] R1 — PR #1324 merged, deploying to core.eq.solutions
- [ ] R2 — Royce's click-through done, nothing broken (or breakage reported + fixed)
- [ ] R3 — 0 unlinked active staff on the org chart

## Where to start

R1 first (five-minute review + merge, unblocks the Table half of R2). Then R2 and R3 can happen in either order — R3 doesn't depend on R1.

---

## Related

- [eq/pending.md](../pending.md) — source section: "Shell Conversations built end-to-end"
- [eq/shell-conversations-scoping-2026-08-11.md](../shell-conversations-scoping-2026-08-11.md) — full history and data model behind this thread
- [eq-shell PR #1324](https://github.com/eq-solutions/eq-shell/pull/1324) — R1
- [eq-shell PR #1321](https://github.com/eq-solutions/eq-shell/pull/1321) — the team/supervisor write path R3 uses

---
title: Archive
owner: Royce Milmlow
last_updated: 2026-07-12
scope: Parked, deferred, and historical content kept out of default AI load
read_priority: reference
status: live
---

# Archive

Content that should not load in default AI sessions but is preserved for
git history and potential reactivation. AIs read `/archive/` only when
explicitly directed.

| File | Why archived | When to revisit |
|---|---|---|
| `changelog-eq-quotes.md` | Historical Flask v1 changelog. Note: EQ Quotes was un-deferred 2026-05-19 and briefly live, but was RETIRED in 2026 — replaced by EQ Ops. See `eq/products.md` "Killed / Deferred" for current status | Superseded — EQ Ops is the successor, no revival planned |
| `changelog-ahd.md` | AHD parked to 2027 capital activation | 2027 capital activation review |
| `GROK.md` | Grok not part of the active workflow (2026-07-12); pointed at `STATE.md`/`SPRINT-BOARD.md`, archived same day | If Grok sessions resume — rewire its `STATE.md` pointer to `suite-state.md` first |
| `direction-d-state.md` | Direction D design-system + IA wave appears dormant — zero inbound references found across governed docs (2026-07-12) | If the wave resumes, refresh against live state before reinstating |
| `lessons-history.md` | Full narratives for `system/lessons.md` entries that were either fully dead (pre-GitHub Supabase substrate mechanisms) or duplicated in full elsewhere (`system/failures.md`, `system/TODAY.md`, `hooks/README.md`) — trimmed 2026-07-12 to a short rule + pointer in `lessons.md` per the "one fact, one home" rule | Read directly whenever the full story behind a rule is wanted, not just the rule — not really "revivable", this is the permanent home for the long version |

## Sprint working docs — `sprints/`

One-shot planning, audit, and reconcile docs from the 2026-05-30 autonomous
sprint, kept for git history after their plans executed and merged. Read only
when explicitly tracing how a 2026-05-30 decision was made.

| File | Why archived |
|---|---|
| `sprints/component-audit-2026-05-30.md` | Component audit — executed |
| `sprints/design-audit-2026-05-30.md` | Design-token audit — design pillar complete |
| `sprints/cards-token-consolidation-2026-05-30.md` | Cards token work (#10) — merged |
| `sprints/field-reconcile-b3-2026-05-30.md` | B3 reconcile analysis — 10 fixes merged (#141) |
| `sprints/stream2-field-merge-plan-2026-05-30.md` | Field/SKS codebase merge plan — merged (v3.5.33) |
| `sprints/sprint-2026-05-30-one-spine.md` | Sprint framing doc — sprint closed |
| `sprints/sprint2-wave2-shortlist-2026-05-30.md` | Wave-2 shortlist — all selected items merged |
| `sprints/cards-rebuild-plan-2026-05-30.md` | Cards worker-first rebuild plan — S2-A deferred ("not building now"); revive if E1 resumes |
| `sprints/RESUME-2026-05-21.md` | One-time session resume prompt (2026-05-21) — superseded by `STATE.md` |
| `sprints/STATE.md` | Autonomous Sprint coordination mode retired 2026-07-12 — superseded by `suite-state.md` (auto-refreshed) + `digest.md` |
| `sprints/SPRINT-BOARD.md` | Autonomous Sprint coordination mode retired 2026-07-12 — claim/ownership now via normal PRs, no board |

## How to revive archived content

1. Move the file out of `/archive/` into the appropriate tier folder.
2. Update `status:` in frontmatter from `archived` to `live`.
3. Update `last_updated:` to today.
4. Add an entry to `ops/decisions.md` recording the revival.
5. Push and verify Supabase sync.

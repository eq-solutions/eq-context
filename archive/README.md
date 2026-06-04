---
title: Archive
owner: Royce Milmlow
last_updated: 2026-06-04
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
| `changelog-eq-quotes.md` | Historical Flask v1 changelog. EQ Quotes was un-deferred 2026-05-19 and is now live first-round core (`eq/products.md`) | Reinstate as `eq/changelog/quotes.md` when the React rewrite begins |
| `changelog-ahd.md` | AHD parked to 2027 capital activation | 2027 capital activation review |
| `sessions-2026-04.md` | April 2026 session logs, rolled off the 30-day window | Tracing an April decision |
| `auth-spike-2026-05-30.md` | One-shot Supabase-Auth IdP + passkeys spike | If the auth re-platform resumes |
| `design-system-consolidation-2026-05-31.md` | Design-system consolidation analysis (snapshot) | Design-system rework |
| `eq-canonical-classification-2026-05-31.md` | eq-canonical table classification audit (snapshot) | Re-auditing canonical exposure |
| `field-roles-findings-2026-05-31.md` | Field roles findings + cross-app decision (snapshot) | Roles model changes |
| `roles-canonical-audit-2026-05-31.md` | Roles + eq-canonical audit (snapshot) | Roles model changes |
| `sks-anon-exposure-audit-2026-05-31.md` | SKS canonical anon-exposure audit (snapshot) | Re-auditing SKS RLS |

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
| `sprints/SPRINT-2-BOARD.md` | Sprint 2 board — waves complete |
| `sprints/sprint-2026-05-31-design-system.md` | Design-system component buildout sprint (A7–A11) — snapshot |

## How to revive archived content

1. Move the file out of `/archive/` into the appropriate tier folder.
2. Update `status:` in frontmatter from `archived` to `live`.
3. Update `last_updated:` to today.
4. Add an entry to `ops/decisions.md` recording the revival.
5. Push and verify Supabase sync.

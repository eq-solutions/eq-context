---
title: Archive
owner: Royce Milmlow
last_updated: 2026-07-16
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
| `auth-spike-2026-05-30.md` | Auth re-platform spike (Supabase Auth IdP + passkeys) — one-shot exploration doc | If a passkey/IdP migration is proposed again, read this first for prior analysis |
| `canonical-wiring-activation-status-2026-06-07.md` | Point-in-time activation status + morning-continuation notes from the 2026-06-07 canonical wiring push — superseded by live state | Historical only — check suite-state.md for current canonical wiring status |
| `eq-canonical-classification-2026-05-31.md` | One-shot reference classification of the eq-canonical Supabase project's tables/data | If eq-canonical's schema classification needs re-deriving, read this as a prior baseline |
| `f1-ehowg-key-rotation-runbook-2026-06-03.md` | Runbook for rotating the exposed ehowg (sks-canonical) service_role key — the F1 finding | Read before any future ehowg key rotation, even though this specific F1 rotation is presumably closed |
| `service-feature-backlog-2026-05-30.md` | EQ Service feature backlog snapshot, 2026-05-30 — superseded by eq/pending.md's live backlog | Historical only — eq/pending.md is current |
| `sessions-2026-04.md` | Session logs, April 2026 | Historical record, no revival path — see `sessions/` for current session logs |
| `sks-anon-exposure-audit-2026-05-31.md` | SKS canonical anon-exposure audit + canonical RPC hardening — one-shot security audit doc | Read before any future anon-exposure audit as a prior baseline; check `ops/security-register.md` for current open findings |

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
| `sprints/SPRINT-2-BOARD.md` | Sprint 2 coordination board — sprint closed, same retirement as `SPRINT-BOARD.md` |
| `sprints/SPRINT-5-BOARD.md` | Sprint 5 coordination board — sprint closed, same retirement as `SPRINT-BOARD.md` |
| `sprints/SPRINT-6-BOARD.md` | Sprint 6 coordination board — sprint closed, same retirement as `SPRINT-BOARD.md` |
| `sprints/SPRINT-7-BOARD.md` | Sprint 7 coordination board — sprint closed, same retirement as `SPRINT-BOARD.md` |
| `sprints/SPRINT-BOARD.md` | Autonomous Sprint coordination mode retired 2026-07-12 — claim/ownership now via normal PRs, no board |

## How to revive archived content

1. Move the file out of `/archive/` into the appropriate tier folder.
2. Update `status:` in frontmatter from `archived` to `live`.
3. Update `last_updated:` to today.
4. Add an entry to `ops/decisions.md` recording the revival.
5. Push to `main` — live immediately, no sync step (retired 2026-06-22).

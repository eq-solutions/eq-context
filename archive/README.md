---
title: Archive
owner: Royce Milmlow
last_updated: 2026-07-20
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
| `WEEKEND-MERGE-RUNBOOK.md` | One-off runbook for the 2026-06-04 weekend merge window — every candidate in it long resolved | Historical only |
| `_ws1-customer-dedup-2026-06-07.md` | Already self-marked `status: archived` — record of the 38-row Tier-S customer dedup actually applied 2026-06-07 | Read only as the exact rollback record if that dedup is ever questioned |
| `_ws2-site-customer-backfill-2026-06-07.md` | Already self-marked `status: archived` — record of the 440-row site→customer backfill actually applied 2026-06-07 | Rollback record only |
| `canonical-wiring-deploy-runbook-2026-06-07.md` | Already self-marked `status: archived` — the 6-step canonical wiring program it activates shipped long ago | Historical only |
| `cross-app-linkage-audit-2026-06-07.md` | Already self-marked `status: archived` — point-in-time snapshot superseded by live state | Historical only — companion `cross-app-linkage-remediation-plan-2026-06-07.md` (still at root) links here for the original audit |
| `cross-app-linkage-sprint-2026-06-07.md` | Already self-marked `status: archived` ("now complete") — its one remaining open item (Tier A/C customer dedup) is tracked directly in `eq/pending.md` | Historical only |
| `design-system-consolidation-2026-05-31.md` | Verified live 2026-07-20: every listed component (Modal/FormInput/StatusBadge/Card/Toast/Tabs) ships in `eq-ui` v1.10.0, font self-hosted via `@fontsource` — `eq/pending.md`'s open checkboxes were stale, not a real gap | Historical only |
| `field-roles-findings-2026-05-31.md` | No live pointer found anywhere (`pending.md`/`digest.md`/`suite-state.md`) — the Field auth-token-fidelity fix it raised was never picked up | Read if that specific fix is ever revisited |
| `platform-architecture-audit-2026-06-02.md` | Already self-marked `status: archived` — F1/F3 findings superseded by the newer secret-rotation runbooks | Historical only |
| `quality-polish-backlog-2026-05-30.md` | No live pointer outside the (also archived) design-system doc; remaining items (U5/M4/M5/L4/C1/Z1) minor and untracked | Historical only |
| `roles-canonical-audit-2026-05-31.md` | No live pointer found — the open Service-role-mapping decision it surfaced was never picked up | Read if that decision is ever revisited |
| `security-secret-rotation-runbook-2026-05-31.md` | Superseded by the newer `eq-secret-salt-rotation-runbook-2026-06-06.md` (still live at root) | Historical only |
| `sprint-2026-05-31-design-system.md` | Never-authorised draft build plan for the same component work confirmed complete in `eq-ui` v1.10.0 | Historical only |
| `sprint-2026-06-08-ui-consistency.md` | Remaining tasks were version-bump busywork (tokens v1.3.1, eq-ui v1.1.2) long since superseded by many later bumps (eq-ui now v1.10.0) | Historical only |
| `worker-identity-linker-spec-2026-06-07.md` | Already self-marked `status: archived` — `eq/pending.md` confirms "DONE 2026-06-09, PR merged" | Historical only |

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

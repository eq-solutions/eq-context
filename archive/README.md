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
| `changelog-cards-dead-twin.md` | EQ Cards changelog, stops 2026-06-30. Own scope line already said "duplicates eq/changelog/cards.md ... Consolidate, flagged as a follow-up" — that follow-up, done 2026-08-15. `eq-cards.md` (309 lines, current) is the live changelog | Superseded by `eq/changelog/eq-cards.md`, `superseded_by:` frontmatter added |
| `changelog-eq-field-dead-twin.md` | EQ Field's own frontmatter already read "RETIRED — every entry below is now in eq/changelog/field.md ... do not append", stamped 2026-07-19 (commit merging its 18 unique PRs into `field.md`). Physically archived 2026-08-15, 6 weeks after that commit, closing the gap between "marked retired" and "actually moved". **Note (2026-08-17): the "naming inverted / field.md is canonical" claim below this row was true when written and is now stale** — `field.md` itself was retired the same day, see `changelog-field-dead-twin.md` | Superseded by `eq/changelog/eq-field.md` (not `field.md` — that pointer chain moved one more hop, 2026-08-17) |
| `changelog-field-dead-twin.md` | The OTHER half of the Field pair: `field.md` was the 1954-line canonical log this table's own `changelog-eq-field-dead-twin.md` row pointed at — until a fresh `eq-field.md` was recreated after that 2026-07-19 merge and diverged again (5 unique entries, PR #703/#705/#709/#710/#711, never folded back in). Merged into one file 2026-08-17, keeping the repo-slug name (`eq-field.md`) per the convention every other product changelog already uses. Archived same day, no gap this time | Superseded by `eq/changelog/eq-field.md` |
| `changelog-shell-dead-twin.md` | EQ Shell changelog, stops 2026-07-14, own scope line already said "duplicates eq/changelog/shell.md ... this file is the one actually kept current" | Superseded by `eq/changelog/eq-shell.md` (1170 lines, current) |
| `changelog-service-dead-twin.md` | EQ Solves Service changelog, stops 2026-07-13, own scope line already said "Superseded by eq-service.md going forward — see banner below" | Superseded by `eq/changelog/eq-service.md`. Not to be confused with the SEPARATE `eq-solves-service-dead-twin.md` below — this file predates and is unrelated to that one |
| `changelog-eq-solves-service-dead-twin.md` | The genuinely-unresolved live pair `eq/README.md` flagged 2026-08-15 (`eq-service.md` + `eq-solves-service.md`, both appended 2026-08-14 by different sessions, both self-marked `UNRECONCILED PAIR`, deliberately left unmerged pending Royce's own call per `sessions/2026-08-11.md`). That call was made 2026-08-17: merge both by date rather than pick a survivor — 244 distinct PR references across both, all preserved in `eq-service.md`. Archived the same day the merge landed | Superseded by `eq/changelog/eq-service.md` |
| `field-feature-backlog-2026-05-30.md` | Archived 2026-08-15, the strongest of this batch: **zero live citers**. Its stated authority, `eq/punch-list-2026-06-02.md`, is itself `status: archived` and self-headed "Mostly SUPERSEDED as of 2026-07-16"; every other inbound was `archive/` or `sessions/`. It reads a `v3.5.30` codebase and Field shipped `v3.5.486`. Its own body: "no-migration EQ-tenant backlog exhausted." | Only if someone wants the pre-v3.5.469 Field wishlist verbatim — check it against live code first, it was already 12-of-16 wrong once |
| `access-model-cluster1-build-plan-2026-07-16.md` | Archived 2026-08-15 — the work shipped the same day it was planned. Its own header says "treat this file as the historical plan, not current status"; `suite-state.md` records cluster 1 Phase 4 CLOSED with migrations 0188/0189/0190 re-verified live on both planes via `pg_proc`. | Never as status — read only as the design rationale behind those three migrations |
| `dashboard-signals-build-plan-2026-07-16.md` | Archived 2026-08-15 — shipped and live. Frontmatter still said `status: draft` and the body "Status: spec, not started", both stale; `eq/changelog/eq-shell.md` records PR #886 merged (`13a6386`), deploy `6a592f6` ready, smoke-checked live. A shipped spec is a historical record. | Never as status — read as the spec behind PR #886 |
| `eq-secret-salt-rotation-runbook-2026-06-06.md` | Archived 2026-08-15 as a **superseded decision record**. README's justification ("`eq/pending.md` records the rotation as DECLINED") was false — that decision had rotated into `eq/pending-archive.md`. **Caveat: `EQ_SECRET_SALT` is NOT dead** — still an active session-signing fallback in `token.ts`, and it appears in SEC-9's 2026-08-08 dev-context leak list. Archived because the *decision* moved, not because the key went away. | If SEC-9 rotation revisits the salt — the mechanics here are still accurate |
| `auth-phase4-hmac-retirement-runbook.md` | Archived 2026-08-15 as the **completed-cutover record**. `suite-state.md` confirms legacy HMAC retired (`validateLegacyToken()` removed, PR #326) and `mint-iframe-token` deleted (PR #430); the body still read "Status: DRAFT — not yet approved for execution", which was flatly wrong. Same treatment its sibling `cross-app-linkage-audit-2026-06-07.md` already had. **Caveat: only the iframe-HMAC half is done** — Phase 4's stated goal also included retiring `EQ_SECRET_SALT`, which is still live. | If the salt-retirement half is ever picked up — that part was never executed |
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

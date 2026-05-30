---
title: Autonomous Sprint — Board
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Full sprint backlog + ownership/claims across all EQ streams; the coordination contract
read_priority: critical
status: live
---

# Autonomous Sprint — BOARD (single source of truth for who's doing what)

**Read [`AUTONOMOUS-SPRINT-RULES.md`](AUTONOMOUS-SPRINT-RULES.md) first, then [`STATE.md`](STATE.md).**
**Claim an item before starting:** set its `owner` + `branch` + status to 🔵 in-progress. Don't start an item whose repo+files are already claimed.

Legend: ✅ done · 🔵 in-progress (claimed) · ⚪ todo (unclaimed) · ⛔ Royce-gated · ⏸ paused
Last refreshed: 2026-05-30.

---

## Stream A — Design / tokens
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| A1 | Shell consume @eq-solutions/tokens | eq-shell | ✅ | #66 merged | live |
| A2 | Field tokens + Plus Jakarta Sans + drift-guard | eq-solves-field | ✅ | #136 merged | live |
| A3 | Service de-vendor + 0097 cleanup | eq-solves-service | ✅ | #203, #204 merged | live |
| A4 | Cards token consolidation | eq-cards | ⚪ | — | **Decision needed:** Cards has parallel `EqSpacing`/`EqSpacingTokens`; re-vendor would dup-class compile-error. Bundle with E1. NOT SKS. |
| A5 | Component audit doc (→ future @eq-solutions/ui) | eq-shell + eq-solves-service | ⚪ | — | read-only research; rank duplicated buttons/tables/forms |
| A6 | Field `base.css` legacy vars → `--eq-*` | eq-solves-field | 🔵 | Code session / `claude/field-merge-phase1` | bundle with B-stream Field work to avoid overlap |

## Stream B — EQ Field + SKS merge (codebase only; data stays separate)
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| B0 | Re-scope + staleness audit | — | ✅ | this session | EQ Field already multi-tenant w/ SKS support; config NOT stale → merge = port modules + cutover |
| B1 | Tenant-safety groundwork | eq-solves-field | ✅ | (pre-existing) | branding/detection/disabled-tables already in EQ Field |
| B2a | ~~Port `project-hours.js`~~ → **resolved: NO PORT** | eq-solves-field | ✅ | this session (verified) | **Ground-truth 2026-05-30:** dead in BOTH — unwired orphan in SKS (no live `<script>`/precache; only a comment ref) AND EQ **deliberately deleted** the file at v3.5.11 (dead-code audit). Re-adding = re-introducing removed dead code → not done. Perms/flag/history already at parity, so cutover loses nothing. **Royce 2026-05-30: leave dead** — no revival. |
| B2b | Port `safety.js` + `safety-dashboard.js` | eq-solves-field | 🔵 | Code session / `claude/field-merge-phase1` | **Verified LIVE in SKS** (boot tags ln 89-90; safety.js precached): 989 + 270 = ~1259ln. Dedicated surface. Port = SKS boot-load → EQ lazy-loader + **tenant-gate to `sks` (EQ never loads)** + add `prestarts`/`toolbox_talks` to `TENANT_DISABLED_TABLES.eq`. |
| B2c | Port `teams.js` | eq-solves-field | ⚪ | — | **Verified LIVE in SKS** (boot tag ln 64, precached): 446ln. **Coupled** into roster/contacts/schedule — reconcile carefully. Boot-load → lazy. |
| B2d | Port `pipeline*` (×3) | eq-solves-field | ⚪ | — | **Verified LIVE in SKS** (boot tags ln 85-87, precached): import 376 + pipeline 583 + resource 1480 = 2439ln. `SKS_PIPELINE` ns. Needs local `xlsx.full.min.js` (SKS CSP blocks CDN). Boot → lazy. Do LAST (SKS `pipeline-ui` worktree recently active). |
| B3 | Reconcile SKS 11-release delta | eq-solves-field | ⚪ | — | fixes SKS has that EQ lacks |
| B4 | Light canonical wiring → `sks-canonical` | eq-solves-field | ⚪ | — | control-plane reads only; no operational migration |
| B5 | **CUTOVER** repoint sks-nsw-labour.netlify.app | infra | ⛔ | — | **ROYCE-GATED — touches SKS live. Do not run.** |

> **Module-state ground-truth (verified 2026-05-30, read-only).** The recon premise "SKS-only modules are live in SKS → port them" holds for B2b/B2c/B2d (all are live boot-loaded `<script>` tags + precached in SKS) but was **wrong for B2a** (project-hours is a dead orphan in *both* repos). **Lesson for the next agent:** verify a module is actually *wired* in SKS (live tag / precache / nav) before porting — don't trust the file's mere existence. **Structural note:** SKS loads all modules at boot; EQ Field uses a lazy-loader (v3.5.21+). Every B2 port must convert SKS boot-load → EQ lazy-manifest, not just copy the file + tag.
>
> **✅ RESOLVED 2026-05-30 — project-hours stays dead.** Royce chose *"leave it dead"*: B2a is closed as a no-op and the burn-down panel will **not** be revived or carried into the merge. The residual `ph.*` perms + `feat_project_hours_v1` flag default + `sites.track_hours` column are harmless and may stay (or be swept in a future dead-code pass). No further action.

## Stream C — Auth re-platform
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| C1 | Role registry `@eq-solutions/roles` | eq-roles (new) | ✅ | local git only | built + verified; matrix matches Shell |
| C1b | Create public `eq-roles` repo + push | eq-roles | ⛔ | — | new public repo → flag before creating (Rule §1) |
| C2 | Wire Shell to consume @eq-solutions/roles | eq-shell | ⚪ | — | replace hand-defined EqRole + MATRIX; needs eq-shell quiet |
| C3 | Supabase-Auth IdP + passkey spike | eq-shell | ⚪ | — | spike branch; no prod auth change |
| C4 | Staged auth cutover (shadow → app-by-app → retire HMAC) | all | ⛔ | — | **auth deploy = Royce-gated (Rule §1)** |

## Stream D — Equipment / asset intake (in flight from other sessions)
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| D1 | QR labels + asset hierarchy | eq-shell | 🔵 | `claude/equipment-qr-hierarchy` (#69) | mergeable; sequence vs #64 `TenantHome` conflict |
| D2 | AI enrichment / dup-detect / site-match / photo / PDF | eq-intake | 🔵 | `claude/clever-roentgen-3a3688` | then **re-vendor into eq-shell** (Rule §4) |
| D3 | Bridge canonical assets → EQ Service maintenance | eq-solves-service | 🔵 (dormant) | `claude/charming-dirac-72bcb0` | **canonical_id back-ref migration must be a TIMESTAMP, not `0110`** (taken). Build type-clean, not pushed. |

## Stream E — Cards / canonical / PPM
| id | item | repo | status | owner / branch | notes |
|----|------|------|--------|----------------|-------|
| E1 | Cards Flutter worker-first rebuild | eq-cards | ⚪ | — | old profiles/licences → worker-first; fold in A4 token fix. NOT SKS. |
| E2 | PPM canonical realignment | (canonical) | ⏸ | — | **paused** — canonical PPM model misaligned with SKS ACB/NSX breaker workflow; revisit before rebuilding any PPM dashboard |
| E3 | eq-service observability keys (PostHog/Sentry) | eq-solves-service | ⛔ | — | Royce's task (Netlify env vars) |

---

## Migration-number ledger (timestamp from now on — see Rule §3)
- `eq-solves-service`: `0110` taken (`0110_performance_level_hf.sql`). All new migrations → `YYYYMMDDHHMMSS_*`.

## How to update this board
Edit the row you own as status changes. When done, set ✅ + the merged PR. Keep "Last refreshed" current. This file + RULES + STATE are the contract — if reality and the board disagree, fix the board.

---
title: Direction D — State Tracker (ARCHIVED)
owner: Royce Milmlow
last_updated: 2026-07-12
scope: Living state doc for the Direction D design-system + IA wave. Updated after each task closes.
read_priority: reference
status: archived
---

> **ARCHIVED 2026-07-12 — no inbound references found (checked all governed docs);
> the Direction D wave this tracked appears dormant.** Kept for git history. If this
> wave resumes, reinstate and refresh against live state first.

# Direction D — State Tracker

Direction D is the design-system consolidation and IA clean-up wave for the EQ suite.
This file records the current status of each task, package versions, open PRs, and
blocking decisions. Update it when a task closes or a PR merges.

---

## Package versions (current as of 2026-06-01)

| Package | Version | Released | Key changes |
|---|---|---|---|
| `@eq-solutions/tokens` | **v1.2.0** | 2026-05-31 | Warm-sand ramp, 5 new brand tokens (`--eq-sand-*`), global a11y CSS (`prefers-reduced-motion`, focus-visible ring) |
| `@eq-solutions/ui` | **v1.1.1** | 2026-06-01 | Ghost Button hover border (`border-color: var(--eq-gray-300)`) — at-rest border was already in v1.0.1 |

Previous: tokens v1.0.0 / v1.1.0, ui v1.0.1 / v1.1.0

---

## Task status

### D0 — Token foundation

| Task | Status | Notes |
|---|---|---|
| D0.5-1 Audit hosted eq-tokens.css consumers | Done | |
| D0.5-2 De-drift the file | Done | |
| D0.5-3 Make it un-driftable | Done | Drift-guard in place |
| D0.5-4 Drift-guard + document | Done | |
| D0.6 Complete token package vs handoff | Done | tokens v1.2.0 merged 2026-05-31 — warm-sand ramp, 5 new brand tokens, global a11y CSS |

### D1 — Token consumption across apps

| Task | Status | Notes |
|---|---|---|
| D1 Field — re-vendor tokens v1.1.0 | Done | |
| D1 Cards — Flutter Dart tokens v1.1.0 | Done | |

### D2 — Icon system (Lucide, scoped)

**ADR:** `eq-shell/docs/adr-001-icons.md` — Accepted 2026-05-31

Decision: Lucide is the icon family. Adoption is scoped — React apps (Shell + Service) use Lucide for all meaningful icons; Field adopts opportunistically on new/touched screens; Cards keeps Material Icons (no retrofit).

| Task | Status | Notes |
|---|---|---|
| D2.1 Lucide ADR + CLAUDE.md guidance | Done | ADR at `eq-shell/docs/adr-001-icons.md` |
| D2.2 eq-shell meaningful-glyph sweep | Done | eq-shell Lucide sweep complete; PR #93 merged |
| D2.3 Service meaningful-glyph sweep | Done | eq-solves-service Lucide sweep complete |
| D2.4 Field Lucide availability (no sweep) | Done | Helper available; no mass conversion on live SKS-critical app |

### D3 — Net-new screens + density

| Task | Status | Notes |
|---|---|---|
| D3.1 Specs for 4 net-new screens | **Done** | Specs locked 2026-06-01. All decisions confirmed. |
| D3.2 Compact density mode | **Done** | eq-shell PR #96 merged 2026-06-01 |
| D3.3 Build net-new screens | **Done** | All 4 specs shipped: icon-rail (PR #106 + #119 gap-fills), service-do (PR #215), calendar (PR #220), cards-ocr (PRs #102/#103 — already on main). |

### D4 — Records IA

| Task | Status | Notes |
|---|---|---|
| D4.1 Records-into-Shell IA audit | **Done** | `eq-shell/docs/d4-1-ia-audit.md` |
| D4.2 IA + migration spec | **Done** | `eq-shell/docs/specs/d4-2-ia-migration-spec.md`; all OQ-1–OQ-6 resolved 2026-06-01 |
| D4.3 Records IA build (phased) | **Phase 1+2 done** | Phase 1: HubLayout `iframe` prop already renders IconRail only (no HubSidebar) — solved by PR #106. Phase 2: PR #115 merged 2026-06-01 — EntityBrowserPage sidebarRecords fixed + Staff/Licences added to sidebar |

Resolved OQs (2026-06-01):
- **OQ-1:** Yes, Field nav-suppression removal (v3.5.40) was intentional. Shell suppresses HubSidebar via `iframe` prop on HubLayout. No Field deploy needed.
- **OQ-2:** Keep both surfaces (`/equipment` + `/data/asset`) with clearer labels. Merge is D4.3+ scope.
- **OQ-3:** No — EQUIPMENT section covers it. Assets stay out of RECORDS.
- **OQ-4:** No sidebar in Flask Quotes — no action needed.
- **OQ-5:** Defer Service `/records` hub decision until Phase 1+2 stable.
- **OQ-6:** Phase 1 required no Field deploy (Shell-only change).

### D5 — Consumer adoption of eq-ui v1.1.0

| Task | Status | Notes |
|---|---|---|
| D5.1 eq-shell adopt eq-ui v1.1.0 | **Done** | PR #95 merged. Also: Skeleton adoption in App.tsx + LicenceOcrPage via PR #106. |
| D5.2 eq-solves-service adopt eq-ui v1.1.0 | **Done** | PR #212 merged — FormInput re-export (29 callsites). StatusBadge/KindPill/ConfirmDialog/Tabs skipped (incompatible domain models — see findings). |

**D5.1 inline sweep findings (eq-shell — all skipped, no clean replacements):**
- `gm-reports/index.tsx` — inline Badge uses loss/watch/ok values; doesn't map to StatusBadge's open/in-progress/overdue/closed/await
- `equipment/index.tsx` — StatusChip (overdue/soon/ok/none) doesn't map to KindPill (preventive/corrective/inspection); Button already used
- `EntityBrowserPage.tsx` — Button already used; two-step confirm uses intentional local state, not a ConfirmDialog drop-in
- No custom tab strips found in shell src
- FormInput candidates have `<select>` siblings or form-level errors — each needs a targeted per-file PR
- live-dot already uses `var(--eq-brand)` — no raw `#38BDF8` found in shell src

**D5.2 skipped (eq-solves-service — incompatible domain models):**
- StatusBadge: local domain model uses not-started/complete/blocked/active/inactive; kit uses open/in-progress/overdue/closed/await
- KindPill: Service check types (maintenance/acb/nsx/rcd/general) vs kit work-order kinds (preventive/corrective/inspection)
- ConfirmDialog: local is a promise-based `useConfirm()` provider; kit is prop-driven — architecturally incompatible
- Tabs: all tab strips use router `<Link>` elements or embed icons/status indicators outside the kit TabItem interface

### D6 — Housekeeping

| Task | Status | Notes |
|---|---|---|
| D6.1 live-dot token check | Done | Confirmed `var(--eq-brand)` in use; no raw hex found in shell src |
| D6.2 Field CLAUDE.md Lucide note | **Done** | security-audit branch had no CLAUDE.md conflicts — note added 2026-06-01. File is local-exclude only (not committed by design). |
| D6.3 Rotate exposed eq-solves-service GitHub token | Done | Remote URL cleaned. User must revoke old PAT at `github.com/settings/tokens`. |
| D6.4 eq-context Direction-D doc update | Done | This file |

---

## Open PRs summary

All Direction D PRs merged as of 2026-06-01. No open PRs.

Merged PRs (this wave):
| PR | Repo | Task |
|---|---|---|
| #95 | eq-shell | D5.1 ui v1.1.0 bump |
| #96 | eq-shell | D3.2 density mode |
| #106 | eq-shell | D3.3a icon rail + D5.1 Skeleton (also completes D4.3 Phase 1) |
| #111 | eq-shell | Hotfix: TS build errors + conflict markers |
| #114 | eq-shell | B12: perm drift guard full matrix |
| #115 | eq-shell | D4.3 Phase 2: EntityBrowser sidebarRecords + Staff/Licences |
| #116 | eq-shell | Quality polish: L3 briefing skeleton · U3 jargon · P5 Google Fonts · U2 ComingSoon |
| #117 | eq-shell | C3: TenantPicker hex → CSS vars |
| #118 | eq-shell | M1: TenantPicker responsive padding |
| #119 | eq-shell | D3.3 icon rail gap-fills (Q4 Quotes trial tooltip) · P1 dashboard 60s cache · P2 lazy briefing · M2 mobile sidebar drawer |
| #122 | eq-shell | eq-ui v1.1.1 bump |
| #2 | eq-ui | Ghost Button hover border · v1.1.1 |
| #212 | eq-solves-service | D5.2 ui v1.1.0 + FormInput |
| #215 | eq-solves-service | D3.3b Service Do screen |
| #217 | eq-solves-service | M3 SlidePanel mobile · C2 defects token swap · 7 loading.tsx |
| #218 | eq-solves-service | E5 dashboard empty state |
| #219 | eq-solves-service | Z3 reports empty state |
| #220 | eq-solves-service | D3.3 calendar Direction D reskin · P4 defect count RPC · pre-visit brief label |
| #222 | eq-solves-service | eq-ui v1.1.1 bump |
| #223 | eq-solves-service | Site access edit fields · defect detail page + DefectRow links |
| #153 | eq-solves-field | v3.5.49 — L5 SW update toast · U6 PIN from app_config |

---

## References

- `eq-context/design-system-consolidation-2026-05-31.md` — consolidation plan (Royce-reviewed)
- `eq-context/sprint-2026-05-31-design-system.md` — A7–A11 sprint proposal (DRAFT, not authorised)
- `eq-shell/docs/adr-001-icons.md` — D2 icon system ADR
- `eq-shell/docs/d4-1-ia-audit.md` — D4.1 IA audit
- `eq-shell/docs/specs/d4-2-ia-migration-spec.md` — D4.2 IA migration spec
- `eq-shell/docs/specs/` — D3.1 net-new screen specs

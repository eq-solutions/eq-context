---
title: Direction D — State Tracker
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Living state doc for the Direction D design-system + IA wave. Updated after each task closes.
read_priority: high
status: live
---

# Direction D — State Tracker

Direction D is the design-system consolidation and IA clean-up wave for the EQ suite.
This file records the current status of each task, package versions, open PRs, and
blocking decisions. Update it when a task closes or a PR merges.

---

## Package versions (current as of 2026-05-31)

| Package | Version | Released | Key changes |
|---|---|---|---|
| `@eq-solutions/tokens` | **v1.2.0** | 2026-05-31 | Warm-sand ramp, 5 new brand tokens (`--eq-sand-*`), global a11y CSS (`prefers-reduced-motion`, focus-visible ring) |
| `@eq-solutions/ui` | **v1.1.0** | 2026-05-31 | 9-component contract complete: Button, Skeleton, Table, Modal, ConfirmDialog, FormInput, StatusBadge, KindPill, Card, Toast, Tabs |

Previous: tokens v1.0.0 / v1.1.0, ui v1.0.1

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
| D3.1 Specs for 4 net-new screens | **Awaiting review** | Specs written to `eq-shell/docs/specs/` — see D3.2 PR (eq-shell #96); awaiting Royce sign-off before D3.3 build |
| D3.2 Compact density mode | **PR open** | eq-shell PR #96 open (also carries token v1.2.0 bump); eq-design-tokens PR #3 open |
| D3.3 Build net-new screens | Blocked on D3.1 review | |

Open PRs:
- `https://github.com/eq-solutions/eq-design-tokens/pull/3`
- `https://github.com/eq-solutions/eq-shell/pull/96`

### D4 — Records IA

| Task | Status | Notes |
|---|---|---|
| D4.1 Records-into-Shell IA audit | **Written** | `eq-shell/docs/d4-1-ia-audit.md` — in docs PR (awaiting Royce review) |
| D4.2 IA + migration spec | **Written** | `eq-shell/docs/specs/d4-2-ia-migration-spec.md` — in docs PR (awaiting Royce review) |
| D4.3 Records IA build (phased) | Blocked on D4.2 review | Open questions OQ-1 through OQ-6 in the spec must be answered first |

Key open questions for D4.3 (from D4.2 spec):
- **OQ-1:** Was v3.5.40 Field nav-suppression removal intentional?
- **OQ-2:** Assets — consolidate two Shell surfaces or keep separate?
- **OQ-3:** Should Assets appear in Shell sidebar RECORDS section?
- **OQ-4:** EQ Quotes sidebar status when embedded?
- **OQ-5:** Service `/records` hub after Phase 2?
- **OQ-6:** Timing and deployer for Phase 1 Field deploy?

### D5 — Consumer adoption of eq-ui v1.1.0

| Task | Status | Notes |
|---|---|---|
| D5.1 eq-shell adopt eq-ui v1.1.0 | **PR open** | eq-shell PR #95 — `package.json` bumped from `#v1.0.1` to `#v1.1.0`; build clean. Inline sweep skipped (see findings below). |
| D5.2 eq-solves-service adopt eq-ui v1.1.0 | **PR open** | eq-solves-service PR #212 — `package.json` pin moved from `#main` to `#v1.1.0`; `FormInput.tsx` replaced with thin re-export covering 29 callsites; `tsc --noEmit` clean. |

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

Open PRs:
- `https://github.com/eq-solutions/eq-shell/pull/95`
- `https://github.com/Milmlow/eq-solves-service/pull/212`

### D6 — Housekeeping

| Task | Status | Notes |
|---|---|---|
| D6.1 live-dot token check | Done | Confirmed `var(--eq-brand)` in use; no raw hex found in shell src |
| D6.2 Field CLAUDE.md Lucide note | **Blocked** | Waiting for security-audit branch to land on eq-solves-field before adding CLAUDE.md note |
| D6.3 Rotate exposed eq-solves-service GitHub token | Done | Remote URL cleaned. User must revoke old PAT at `github.com/settings/tokens`. |
| D6.4 eq-context Direction-D doc update | Done | This file |

---

## Open PRs summary

| PR | Repo | Task | Status |
|---|---|---|---|
| [#95](https://github.com/eq-solutions/eq-shell/pull/95) | eq-shell | D5.1 ui v1.1.0 bump | Open |
| [#96](https://github.com/eq-solutions/eq-shell/pull/96) | eq-shell | D3.2 density mode + token bump | Open |
| [#3](https://github.com/eq-solutions/eq-design-tokens/pull/3) | eq-design-tokens | D3.2 token changes | Open |
| [#212](https://github.com/Milmlow/eq-solves-service/pull/212) | eq-solves-service | D5.2 ui v1.1.0 + FormInput | Open |
| docs PR TBC | eq-shell | D3.1 specs + D4.1 audit + D4.2 IA spec | To be created |

---

## References

- `eq-context/design-system-consolidation-2026-05-31.md` — consolidation plan (Royce-reviewed)
- `eq-context/sprint-2026-05-31-design-system.md` — A7–A11 sprint proposal (DRAFT, not authorised)
- `eq-shell/docs/adr-001-icons.md` — D2 icon system ADR
- `eq-shell/docs/d4-1-ia-audit.md` — D4.1 IA audit
- `eq-shell/docs/specs/d4-2-ia-migration-spec.md` — D4.2 IA migration spec
- `eq-shell/docs/specs/` — D3.1 net-new screen specs

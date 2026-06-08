---
title: EQ Design System — Consolidation Plan
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Finish the design-system consolidation begun in the One Spine sprint — eq-ui component buildout, font self-host, Claude Design wiring, standing ADR
read_priority: standard
status: live
---

# EQ Design System — Consolidation Plan — 2026-05-31

**Follow-on to the One Spine sprint** (`design-audit-2026-05-30.md`, `component-audit-2026-05-30.md`). A fresh read-only audit of every surface on 2026-05-31 confirms the foundation is built and Stream A largely shipped. This plan covers only the *delta* to make the whole suite seamless and to bring Claude Design into the loop. **Consolidate-and-finish, not build.**

> **Caveat:** the 2026-05-31 audit read local clones, some behind `origin/main` (`STATE.md` warns the git lines drift). Items below are marked **verify-first** where the board shows a merged PR that may already cover them.

## Bottom line

The hard part is done. `@eq-solutions/tokens` v1.0 is the single source of truth (one JSON → CSS / TS / Tailwind preset / Dart), theming is decided (3 layers), and tokens + the first three shared components (Button / Skeleton / Table) ship across Shell / Service / Field / Cards — the board's "Design Pillar COMPLETE." What remains: (1) the rest of the shared component library, (2) two systemic fixes (font, distribution-by-tag), (3) wiring Claude Design to the foundation, (4) recording the model as a standing decision.

## Already shipped (reference)

- Tokens consumed (not vendored): Shell #66, Service #203/#204, Field #136 (+ DM Sans → **Plus Jakarta Sans**), Cards #10.
- `@eq-solutions/ui` v1.0.1 = Button / Skeleton / Table — consumed by Shell (#71/#73) + Service (#205).
- Theming DECIDED (`design-audit-2026-05-30.md` §Theming): 3 layers, `white_label_enabled` gate, `[data-theme]` identity vs `[data-tier]` tier.
- Pin-by-tag migration (eq-ui v1.0.1 / eq-roles v1.0.0) in flight from a concurrent session — **confirm landed** before relying on it.

## The standing model (→ ADR, `ops/decisions.md` 2026-05-31)

"One template for everything" is real at the **token layer** and per-stack at the **component layer**:

- **Tokens — everywhere.** One JSON source compiles to CSS / TS / Tailwind / Dart, so React, vanilla JS, Flutter and Flask consume the *same* values. This is what makes the suite seamless. Already true.
- **Components — per stack.** A React component package can't serve Flask or Flutter. So: `@eq-solutions/ui` (React) for Shell + Service; Field (vanilla) and Quotes (Flask) consume the token CSS + a thin local layer; Cards (Flutter) consumes the Dart token output + Flutter widgets.
- **Distribution — pin by tag, never vendor** (already `AUTONOMOUS-SPRINT-RULES.md` §5). Every drifted surface in both audits was a copied-not-pinned one.
- **"One template for everything" = token-level seamless + per-stack components.** Not one component set. That is the achievable, correct shape.

## Remaining work

### 1. Finish `@eq-solutions/ui` (the #1 lever)

Brief already written: `component-audit-2026-05-30.md` (ranked extraction order). Button / Skeleton / Table done. Remaining, **promoting Service's best-in-class versions to the package, then adopting in Shell**:

| Order | Component | Source | Note |
|---|---|---|---|
| 1 | Modal + ConfirmDialog | Service | **Fold in the A1/A2 accessibility fixes** (focus trap, `role="dialog"`, scroll lock) from the polish backlog — do it once, at the package level, not per app. |
| 2 | FormInput (label+error+hint) | Service | ~40 Service sites; Shell has none. |
| 3 | StatusBadge + KindPill | Service | Map Shell's `ok/warn/err/info/mute` → Service's typed `StatusKind`. |
| 4 | Card | Service | Trivial; its absence makes every Shell page re-invent padding/border. |
| 5 | Toast | Service | Direct lift; Shell has no equivalent. |
| 6 | Tabs | greenfield | Neither app has a real component; design from Service's token-aligned pattern. |

Each: extract → tag a new eq-ui version → bump consumers by tag. Resolve the **ghost-border decision** (polish backlog, PR #73 carry-over — recommended Option B: 1px border in the eq-ui ghost variant) with the Button/Card pass.

### 2. Two systemic fixes

- **Self-host Plus Jakarta Sans once, consumed by all.** Today every app loads it from the Google Fonts CDN (the spec wants self-hosted; polish-backlog P5 fixes only Shell, per-app). Ship the woff2 + an `@font-face` block from the shared layer — inside `@eq-solutions/tokens` or a sibling `@eq-solutions/fonts` asset package — so every pinned consumer self-hosts for free. One fix supersedes the per-app approach. (Package boundary is the only open question; the principle is self-host-once.)
- **Finish the pin-by-tag migration.** Confirm the in-flight eq-ui / eq-roles tag migration landed; move any remaining `#main` consumers to `#vX`. Reproducible builds, no surprise drift.

### 3. Wire Claude Design to the foundation (the original goal)

Make on-brand mocks automatic. Assemble a **"start with context" bundle** = the `eq-design-tokens` repo (tokens + Tailwind preset) + the `design_eq_profile` brief (type, spacing, components, icon systems, copy, hard don'ts). Point Claude Design at that bundle so every mock comes out on-brand by construction. The loop: bundle → Claude Design mock → build with `@eq-solutions/ui` → seamless. Complements the Figma connector (both point at the same source).

- Deliverable: `eq/design/claude-design-context.md` — the canonical paste-in brief, kept in sync with the tokens repo. **(Done 2026-05-31; issued to Claude Design.)**

### 4. Verify-then-fix drift (not already in the polish backlog)

The 2026-05-31 audit surfaced two items absent from `quality-polish-backlog-2026-05-30.md`. **Verify against `origin/main` first** (local clones may be behind):

- **Service: emoji mixed into a Lucide app** (~7 files — `ReportSettingsForm`, `dashboard`, `ContractScopeBanner`, report/email libs). Mixing icon systems is a hard-don't. Replace UI-surface emoji (✓ ✕ ⚠️) with Lucide; leave dev-facing / email-template strings.
- **Service: `RouteProgress` cyan→indigo gradient** (`#0ea5e9 → #3b82f6 → #6366f1`). Off-palette gradient on a UI element. Replace with solid `var(--eq-sky)`.

Everything else the 2026-05-31 audit flagged (Shell login palette, Service raw Tailwind status colours, Field `--eq-grey` contrast, font) is already tracked in the polish backlog (C2 / C3 / C1 / P5 / U1 / U4). **Add the two above to that backlog rather than duplicating here.**

### 5. Quotes (Flask) — decided

`eq-quotes-port` is ~85% token-aligned with its own `tokens.css`, but it is slated for replacement by a React module under Shell (~2–3 months — `ops/decisions.md` 2026-05-19). **Decision (Royce 2026-05-31): leave at 85%, no investment** — the rewrite supersedes it.

## Governance

- Sprint 1 + 2 are complete; this is a **new wave** (Stream A rows A7–A12), not part of the closed sprint scope.
- **Nothing here touches auth or SKS live** — the two permanent carve-outs (`AUTONOMOUS-SPRINT-RULES.md` §0/§1) are unaffected. This is EQ-side, package-and-UI only.

## References

- `design-audit-2026-05-30.md` · `component-audit-2026-05-30.md` · `quality-polish-backlog-2026-05-30.md`
- `ops/decisions.md` 2026-05-31 (this model) · `AUTONOMOUS-SPRINT-RULES.md` §5
- `eq/design/claude-design-context.md` (Claude Design brief)
- Memory: `design_eq_profile`, `project_design_system_state`
- Packages: `@eq-solutions/tokens` v1.3+ · `@eq-solutions/ui` v1.2+

---

## Addendum — 2026-06-08: barrel CSS + peer dep (eq-ui v1.2.0)

**Problem:** React apps had to make two separate CSS imports — once for `@eq-solutions/tokens/tokens.css` and separately discover that component CSS exists. Missed imports caused unstyled components with no build error.

**Fix shipped in eq-ui v1.2.0:**

1. `src/index.css` — barrel stylesheet: imports `tokens.css` then all 10 component CSS files.
2. `./styles` package export alias pointing to `src/index.css`.
3. `@eq-solutions/tokens` moved from `dependencies` → `peerDependencies >=1.3.1` — consuming app controls the token version (and must list it explicitly).

**Canonical import for any React EQ app (eq-shell, eq-service, etc.):**

```css
/* In your app's root CSS — one line covers everything */
@import "@eq-solutions/ui/src/index.css";
/* or equivalently: */
@import "@eq-solutions/ui/styles";
```

**Apps must still list `@eq-solutions/tokens` as a direct dep** (satisfies the peer dep requirement, and is needed for `tokens.ts` JS values in chart/canvas code).

**eq-shell** already updated to use the barrel import (2026-06-08). eq-service follows at T8.

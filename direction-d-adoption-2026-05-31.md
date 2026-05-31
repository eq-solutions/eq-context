---
title: Direction D ("Warm Sand") — Adoption Plan & Token Reconciliation
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Map the Claude Design "Direction D" handoff back into @eq-solutions/tokens and sequence the suite-wide reskin + net-new screens + IA. The visual/reskin layer that complements the component buildout in design-system-consolidation-2026-05-31.md.
read_priority: standard
status: draft
---

# Direction D ("Warm Sand") — Adoption Plan — 2026-05-31

> ⚠ **DRAFT — proposal, not authorised for execution.** Per `AUTONOMOUS-SPRINT-RULES.md`, a fresh Royce "go" is required before any build / PR / merge / deploy. This plan changes **brand-visible** values across every app and carries **four Royce-level decisions** (see §3). Review, decide the gates, then claim.

## What this is

Direction D is the **output** of the Claude Design loop opened by the consolidation plan §3 / board row **A12**: the `eq/design/claude-design-context.md` brief was issued to Claude Design, and Direction D ("Warm Sand") is what came back — delivered as a handoff bundle (`design_handoff_eq_design_system/`: README, CLAUDE.md, `eq-tokens.css`, Component Kit, `eq-data.js`).

It is a **spec, not a drop-in.** Its token file uses different names than our pipeline (`--sky`/`--g50`/`--ok-fg` vs `--eq-sky`/`--eq-gray-50`/`--eq-success-text`). This plan reconciles those names + values into the real `@eq-solutions/tokens` source and sequences the rollout.

**Relationship to the existing plans:** `design-system-consolidation-2026-05-31.md` + `sprint-2026-05-31-design-system.md` cover the **component layer** (finish `@eq-solutions/ui`: Modal/FormInput/StatusBadge/Card/Toast/Tabs, font self-host). Direction D is the **visual + screens + IA layer**. They compose: the token reskin (D0/D1 below) lands underneath the component work; the net-new screens (D3) are built *with* those components. Reuse the same model (tokens-everywhere / components-per-stack / pin-by-tag) and the same carve-outs (no auth deploys without Royce; SKS untouchable).

## Bottom line

The token delta is **smaller than the handoff looks**, because the canonical package already moved partway:

- **Brand (sky/deep/ice/ink)** — Direction D leaves these **unchanged**. The hex→token cleanup already shipped this sprint (eq-shell #85/#86) is valid groundwork — every tokenised surface reskins for free.
- **Status colours** — Direction D's `success #15803D / warning #B45309 / error #B91C1C` **already match `@eq-solutions/tokens` v1.0** (`--eq-success-text` / `--eq-warning-text` / `--eq-error-text`). No package change needed. (They do NOT match eq-shell's stale `public/eq-tokens.css` — see §4 drift.)
- **Genuinely new in Direction D:** (1) the **warm-sand neutral ramp**, (2) the **clay** secondary accent, (3) a few **additive** brand tokens (amber, slate, live). Plus three non-token decisions: **Lucide everywhere**, **compact-density default**, **records-into-Shell IA**.

## §1 — Token reconciliation map (handoff → `@eq-solutions/tokens`)

Edit `eq-design-tokens/tokens/*.json`, then `npm run build` (the `.css`/`.ts`/Tailwind/Dart outputs are generated — never hand-edit `tokens.css`).

### Brand — unchanged (no action)
| Handoff | Pipeline | Value | Action |
|---|---|---|---|
| `--sky` | `--eq-sky` | `#3DA8D8` | none |
| `--deep` / `--sky-deep` | `--eq-deep` | `#2986B4` | none |
| `--ice` | `--eq-ice` | `#EAF5FB` | none |
| `--ink` | `--eq-ink` | `#1A1A2E` | none |
| `--grey` | `--eq-grey` | `#666666` | none |
| `--white` | `--eq-white` | `#FFFFFF` | none |

### Neutral ramp — **CHANGE** (cool grey → warm sand). The big visible delta.
| Pipeline token | v1.0 (cool) | Direction D (warm sand) |
|---|---|---|
| `--eq-gray-50` | `#F9FAFB` | `#F6F3EE` |
| `--eq-gray-100` | `#F3F4F6` | `#EFEAE1` |
| `--eq-gray-200` (default border) | `#E5E7EB` | `#E4DDD2` |
| `--eq-gray-300` (input border) | `#D1D5DB` | `#D4CCBE` |
| `--eq-gray-400/500/600` | `#9CA3AF`/`#6B7280`/`#4B5563` | **unchanged** (text greys stay neutral for contrast) |

> Direction D warms **surfaces/borders** (50–300) but keeps **text greys** (400–600) neutral. Honour that split — warming the text greys would fail contrast.

### Status — already aligned (no action)
| Pipeline | Value | Handoff | Match? |
|---|---|---|---|
| `--eq-success-text` | `#15803D` | `#15803D` | ✅ |
| `--eq-warning-text` | `#B45309` | `#B45309` | ✅ |
| `--eq-error-text` | `#B91C1C` | `#B91C1C` | ✅ |
| `--eq-success/warning/error-bg` | `#F0FDF4`/`#FFFBEB`/`#FEF2F2` | same | ✅ |

### Additions — **NEW tokens**
| New token (proposed name) | Value | Role |
|---|---|---|
| `--eq-clay` | `#A8572B` | secondary **brand** warmth accent — eyebrows/section accents, **~5% usage, never status** |
| `--eq-clay-deep` | `#8A4521` | clay hover |
| `--eq-clay-bg` | `#FBF1E9` | clay tint surface |
| `--eq-amber` / `--eq-amber-deep` | `#F59E0B` / `#B45309` | (amber-deep already == warning-text; dedupe — reference `--eq-warning-text`) |
| `--eq-slate` | `#94A3B8` | (likely == existing `--eq-text-faint`; dedupe before adding) |
| `--eq-live` | `#38BDF8` | live / sync indicator (Shell already uses `--eq-sky-rgb` tints for this — confirm we need a distinct token) |

> **Dedupe pass required:** amber-deep, slate, and live overlap existing tokens. Add only what's genuinely new (clay family is the real addition); alias the rest to avoid a second source of truth.

### Type / spacing / radii / shadow / motion — unchanged
Direction D's scale, 8px grid, radii (chip 4 / input 6 / card 8 / shell 12 / pill 9999), flat-static-cards rule, 150ms motion, and focus ring all match `@eq-solutions/tokens` v1.0 already. No action.

## §2 — Sequenced waves

**D0 — Land Direction D in the token source** *(repo: `eq-design-tokens`; serial; tag after)*
- Edit `tokens/*.json`: warm-sand ramp (gray-50→300), clay family, deduped additions. `npm run build`. Cut `@eq-solutions/tokens` **v1.1**.
- Visual diff the generated `tokens.css`; confirm only the intended deltas.
- **Gate:** §3-A (warm sand) + §3-B (clay) must be decided first.

**D0.5 — Fix the eq-shell stale-token drift** *(repo: eq-shell; see §4)*
- Regenerate/replace `eq-shell/public/eq-tokens.css` from the v1.1 package so the served `/eq-tokens.css` stops shipping the old `#16A34A`/`#D97706`/`#DC2626` status set. This *also* lands Direction D for Shell + every app that `@import`s the hosted file. **Note:** this shifts tokenised status greens/ambers on the **live GM Reports financial dashboard** — stage behind a deploy-preview and eyeball.

**D1 — Cascade reskin (per app, parallel once v1.1 exists)** *(pin by tag)*
- Shell / Service / Field / Cards bump to tokens v1.1. Warm-sand + clay propagate automatically to every token-referencing surface. Per-app visual QA on preview.
- Quotes: **leave at 85%** (consolidation plan §5 — React rewrite supersedes it).

**D2 — Icon unification → Lucide everywhere** *(gated — §3-C)*
- Direction D retires "Field = Unicode glyphs." This **contradicts the current per-app icon rule** in the design brief + repo CLAUDE.mds. Biggest single-app effort (Field is vanilla JS). Do not start without §3-C decided.

**D3 — Net-new screens** *(build with `@eq-solutions/ui`, after the component sprint A7–A11)*
- Service **Do** (action-first), Service **Calendar** (week view), Cards **OCR onboarding** (scan licence → auto-fill; licences/certs only), suite **icon-rail** (expand-on-hover cross-app switcher).

**D4 — IA restructure** *(highest-coordination, last)*
- Move Customers / Sites / Contacts / Equipment / GM Reports to the **Shell canonical layer** (apps reference, don't home them); resolve the double left-menu. Aligns with the canonical-first principle but touches routing across Shell + Field + Service — its own mini-spec.

## §3 — Decisions for Royce (gates)

- **A — Warm-sand ramp.** Adopt the taupe surface/border ramp suite-wide? (This is the headline visible change. Reversible via token revert, but it touches every app at once.)
- **B — Clay accent.** Add `--eq-clay` as the sparing secondary brand accent? (Currently zero clay in the suite; it's net-new brand vocabulary.)
- **C — Lucide everywhere.** Retire Field's Unicode glyphs for Lucide, making icons uniform? This **overrides** the standing "never mix, Field=Unicode" rule — needs an explicit ADR + a CLAUDE.md update across repos.
- **D — Records-into-Shell IA.** Confirm Customers/Sites/Contacts/Equipment/Reports home in the Shell canonical layer (D4). Big, but matches the architecture.
- *(Dark mode stays deferred per the handoff.)*

## §4 — Drift found (fix regardless of Direction D)

`eq-shell/public/eq-tokens.css` (the file Shell serves at `/eq-tokens.css`, `@import`ed by other apps) is **hand-maintained and stale** vs the canonical package:

| Token | Stale shell copy | Canonical v1.0 |
|---|---|---|
| success | `#16A34A` | `#15803D` |
| warning | `#D97706` | `#B45309` |
| danger/error | `#DC2626` | `#B91C1C` |
| neutrals/text | cool (`#F5F4F0`, `#64748B`, `#E2E8F0`) | (package uses gray-scale + status set) |

This is a second source of truth that has already drifted. **D0.5 regenerates it from the package** — fixing the drift and landing Direction D in one move. (Also closes part of the "3 different status greens" noted during the gm-reports tokenisation: package `#15803D` becomes canonical; gm-reports inline `#1E7E4A` should be retired to `var(--eq-success-text)` in a follow-up.)

## §5 — Risks & carve-outs

- **Auth / SKS:** untouched. Pure visual + screens + IA. (D4 routing changes are nav-level, not auth.)
- **Live financial dashboard:** D0.5 + D1 shift tokenised status colours on GM Reports (live at core.eq.solutions/sks/reports). Stage behind previews; have Royce eyeball.
- **All-at-once blast radius:** a token-source change reskins every app simultaneously. That's the point (seamless), but it means D0/D0.5 are not "small" — preview every consumer before merge.
- **Net-new screens depend on the component sprint** (A7–A11): build D3 *after* Modal/FormInput/Card/etc. land, or they'll re-roll primitives.

## Open questions

- [ ] Decisions §3 A–D.
- [ ] Token v1.1 dedupe: confirm amber-deep/slate/live alias to existing tokens vs new.
- [ ] D0.5: regenerate `public/eq-tokens.css` from the package as a build step (stop hand-maintaining it) — agree?
- [ ] Does D4 (IA) want its own spec doc before any code?

## References
- `design-system-consolidation-2026-05-31.md` · `sprint-2026-05-31-design-system.md` · `component-audit-2026-05-30.md`
- `eq/design/claude-design-context.md` (the A12 brief that produced this handoff)
- Handoff bundle: `design_handoff_eq_design_system/` (README, CLAUDE.md, eq-tokens.css)
- Source: `@eq-solutions/tokens` v1.0 (`eq-design-tokens/tokens/*.json` → generated `tokens.css`)
- `AUTONOMOUS-SPRINT-RULES.md` · `STATE.md` · `SPRINT-BOARD.md` · `ops/decisions.md`
- Groundwork shipped this session: eq-shell #85 (gm-reports brand tokens), #86 (5 more shell surfaces)

---
title: EQ Suite Design Audit
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Per-app design-token adoption audit + theming architecture decision
read_priority: reference
status: live
---

# EQ Suite Design Audit — 2026-05-30

**Stream 1 of the "One Spine" sprint. Audit-first, by Royce's call.**
**Bottom line: you don't have a design problem, you have an adoption problem.** The canonical token package `@eq-solutions/tokens` v1.0.0 is well-built and emits CSS / TS / Tailwind preset / Dart from one JSON source. **No app imports it as a dependency.** Every app re-creates or copies the output, and the copies have started to diverge — most visibly in *variable naming* and in Field's *font*.

---

## Per-app state

| App | Stack | How it gets tokens | Brand match | Font | Verdict |
|---|---|---|---|---|---|
| **eq-design-tokens** | JSON → CSS/TS/Tailwind/Dart | *source of truth* | canonical | Plus Jakarta Sans | ✅ CANONICAL |
| **eq-shell** | React 19 + Vite (pnpm ws) | **hand-ported** CSS vars in `src/index.css` | values match | Plus Jakarta Sans | ⚠️ DRIFT — duplicate values + **divergent var names** |
| **eq-solves-service** | Next 16 + Tailwind v4 | **vendored** copy `lib/tokens/tokens.css` (`@import`) | matches | Plus Jakarta Sans (`next/font`) | ⚠️ VENDORED — manual re-copy to update |
| **eq-cards** | Flutter / Dart | **vendored** `lib/core/theme/eq_tokens.dart` | matches | Plus Jakarta Sans | ⚠️ VENDORED — manual re-copy; needs pubspec dep |
| **eq-solves-field** | Vanilla HTML/JS/CSS | **none** — hardcoded in `styles/base.css` | partial (sky only) | **DM Sans** ❌ | ❌ OFF-BRAND + no token system |
| **eq-quotes** | docs/templates | n/a | n/a | n/a | — not a code app |
| **eq-intake** | Node monorepo | unclear (schema-focused) | unclear | unclear | 🔍 needs a look when touched |

`grep "@eq-solutions/tokens"` across every `package.json` in `C:\Projects` → **1 hit, the package's own.** Zero consumers.

---

## The critical finding: naming has diverged, not just values

Shell's hand-port kept the *brand-six* names identical but renamed everything else. A naive "import the package, delete the copy" would break **104 `var(--…)` references** in Shell's `App.css`.

| Concept | Shell `index.css` | `@eq-solutions/tokens` | Status |
|---|---|---|---|
| Brand sky/deep/ice/ink/grey/white | `--eq-sky` … | `--eq-sky` … | ✅ identical |
| Neutral scale | `--gray-50..600` | `--eq-gray-50..600` | ❌ prefix differs |
| Status | `--status-success-bg` / `-fg` | `--eq-success-bg` / `--eq-success-text` | ❌ name differs |
| Shadows | `--shadow-sm` / `-lg` | `--eq-shadow-sm` / `-lg` | ❌ prefix differs |
| Font stack | `--eq-font` | `--eq-font-stack` | ❌ name differs |
| Surfaces | `--eq-bg`, `--eq-bg-subtle`, `--eq-border`, `--eq-border-strong` | *(not defined)* | ❌ Shell-only |
| Tenant accent | `--eq-brand`, `--eq-brand-deep` | `--eq-tier-accent` (+ `[data-tier]`) | ⚠️ different model |
| Spacing / radii / type scale / motion / focus | *(absent — uses literals)* | full token set | ➕ package is richer |

**Implication for wiring order:** each app needs an *alias-bridge* layer, not a swap. Import the package as the value source; map the app's legacy names onto the package tokens; delete only the literal values. Zero visual regression if aliases are correct.

---

## Consolidation plan (ranked, lowest-risk first)

### 1. Shell — alias-bridge (do first)
- Add `@eq-solutions/tokens` dependency (git dep `github:eq-solutions/eq-design-tokens#v1.0.0`, the README's intended path).
- `@import "@eq-solutions/tokens/tokens.css"` at top of `src/index.css`.
- Replace literal values with aliases: `--gray-200: var(--eq-gray-200)`, `--shadow-sm: var(--eq-shadow-sm)`, `--status-success-fg: var(--eq-success-text)`, `--eq-font: var(--eq-font-stack)`, etc.
- Keep Shell-only vars (`--eq-bg`, `--eq-border-strong`, `--eq-brand*`) — they layer on top.
- **Risk:** Shell is the auth hub; App.css has 104 legacy refs. Mitigated entirely by the alias-bridge. Verify build + eyeball login/hub before merge. **No deploy without Royce's go.**
- **Open infra decision:** Netlify must be able to clone `eq-design-tokens` at build. If the repo is public → works as-is. If private → needs a Netlify GitHub token/deploy key, OR publish the package to a private registry. Confirm before merge.

### 2. Service — de-vendor
- Add the dependency; change `@import "../lib/tokens/tokens.css"` → `@import "@eq-solutions/tokens/tokens.css"`; delete `lib/tokens/tokens.css`. Service already uses the package's `--eq-*` names, so this is close to a clean swap.

### 3. Cards — Flutter dep
- Blocked on the package gaining a `pubspec.yaml` (noted as a TODO in `eq_tokens.dart`). Until then, keep the vendored Dart but add the CI drift-guard so it can't silently rot. Smallest near-term win = just the guard.

### 4. Field — font + token system (biggest visible win)
- Switch DM Sans → Plus Jakarta Sans (`index.html` font link + `styles/*.css` font-family refs).
- Field is vanilla (no bundler), so it can't `import` the package. Consume `tokens.css` directly (copy with a CI guard, or add a tiny build step). Decide approach when we get to it.
- This is the single most visible brand correction in the suite, and it gives the Stream-2 SKS merge a clean brand baseline.

### 5. CI drift-guard (do alongside #1)
- Fail any PR that commits a generated `tokens.css` / `tokens.ts` / `tokens.dart` *outside* the `eq-design-tokens` repo. Makes drift structurally impossible going forward.

### 6. Component audit (DEFERRED OUTPUT — look, don't build)
- Rank duplicated components across Shell + Service (buttons, tables, forms, status pills) as the brief for a *later* `@eq-solutions/ui` sprint. Notable existing components to fold in: Service's `StatusBadge`, `Sidebar`, `TestDetailHeader`, `DataTable`. Not built this sprint.

---

## Notes / gotchas surfaced during audit
- Shell loads Plus Jakarta Sans via a render-blocking `@import url(fonts.googleapis…)`; Service already removed its equivalent for perf. Consider aligning Shell to the `next/font`-style preconnect approach — but that's perf scope, not token scope; don't fold it into the wiring PR.
- The package is tier-aware (`[data-tier="standard|advanced|enterprise"]`). Shell already sets tier from the JWT claim — adopting the package means tier theming works for free downstream.
- `eq-quotes` is a docs/template repo, not an app — out of scope. `eq-intake` styling is unclear; flag for a look when next touched.

---

## Theming architecture (DECIDED 2026-05-30)

EQ brand vs tenant brand — three layers, two axes. Formalises the 3 ad-hoc tenant-branding implementations (Shell `--eq-brand`, Service report auto-darken, Field boot injection) into one contract owned by the token package.

**Layers:**
1. **Foundation (locked):** spacing, radii, type scale, motion, focus, neutrals, status. Never themeable — this is the Linear/Notion feel. Identical for all tenants.
2. **EQ brand (default skin):** sky/deep/ice/ink. Unset tenant = looks like EQ. **EQ-owned chrome (Shell login, nav, suite frame) is hard-locked to EQ.**
3. **Tenant theme (whitelisted overrides):** primary accent + auto-derived deep (adjustHex ~-0.20) + logo + app name + optional brand-strip colour. Contrast-validated (AA vs white + ink). Nothing else.

**Axes:** Identity (accent+logo, via `[data-theme="<tenant>"]` set at runtime from canonical store — same machinery as `[data-tier]`) is separate from Tier (billing). 

**Gate:** per-tenant **`white_label_enabled` flag** unlocks theming — NOT tier. SKS on; demo tenants on; ordinary tenants EQ-branded.

**Scope chosen:** accent + logo + brand-strip (middle option).

**Action items this adds to the token package:**
- Split the tenant-identity axis from the tier axis (currently `--eq-tier-accent` is keyed on `[data-tier=enterprise]`). Introduce `[data-theme]` for identity; keep `[data-tier]` for tier deltas.
- Define the themeable contract: which vars are tenant-overridable + the derivation (auto-deep) + contrast-validation rules.
- Runtime applier reads tenant theme (accent/logo/strip + `white_label_enabled`) from the canonical store and sets `[data-theme]` + the override vars on root.

---

## Stream 1 execution status (2026-05-30)

| App | Action | Result |
|---|---|---|
| **eq-design-tokens** | made the repo **public** (was private) | unblocks git-dep for all Netlify builds |
| **Shell** | consume `@eq-solutions/tokens` via alias-bridge | ✅ **merged + live** on core.eq.solutions (PR #66). Build-verified, zero visual change, tier deltas intact |
| **Service** | de-vendor → `@import "@eq-solutions/tokens/tokens.css"` | 🟡 **PR #203 open, build/typecheck/preview green, HELD.** Blocked by a *pre-existing* dup `0097` migration that fails the integration job on every PR (not my change). Merge once that's fixed. Vendored `lib/tokens/tokens.css` left in place pending OK to delete |
| **Field** | DM Sans → **Plus Jakarta Sans** + vendor `styles/tokens.css` + **CI drift guard** | ✅ **merged + live** (v3.5.24, PR #136). Biggest visible brand fix. Done in an isolated worktree to avoid the concurrent sessions |
| **Cards** | investigated; precise diagnosis | 🔶 **deferred — parallel systems, needs a consolidation decision (NOT a re-vendor).** The vendored `eq_tokens.dart` defines `EqColors`(used ×13)+`EqRadius`(used ×2) AND `EqSpacingTokens`/`EqTypographyTokens` (**unused/dead**). The app actually uses its **own** `EqSpacing` (`eq_spacing.dart`) + `EqTypography` (`eq_typography.dart`) classes — 36 files. Re-vendoring the package Dart (which defines `EqSpacing`/`EqTypography`) would **collide** with those → duplicate-class compile errors. Fix = decide whether Cards adopts the package's spacing/typography (delete its own + re-point) or keeps them; pair with the package's pending `pubspec.yaml`. |

**Drift-guard scope clarified:** Shell + Service now consume the package directly (no vendored copy in the build path → cannot drift). The CI drift-guard is only meaningful where a copy is unavoidable: **Field (shipped ✅)** and **Cards (deferred, see above)**.

**Open follow-ups out of this stream:**
1. Fix Service's dup-`0097` migration → merge PR #203 → then delete the orphaned `lib/tokens/tokens.css`.
2. Cards: reconcile Dart class names, then de-vendor/guard (pair with `pubspec.yaml`).
3. Field var bridge: migrate `base.css` legacy vars (`--ink` …) onto `--eq-*` (a later pass; font + token availability landed now).
4. Component audit (the deferred 'look, don't build' output) — ranked duplicate-component list as the brief for a later `@eq-solutions/ui` sprint.

**Execution note:** the C:\Projects repos are under concurrent multi-agent git access — guards applied (branch from origin/main, isolated worktrees, explicit staging, PR-diff verification, gate on green). See memory `feedback_shared_clone_git_guards`.

## References
- Sprint: `eq-context/sprint-2026-05-30-one-spine.md`
- Memory: `design_eq_profile`, `project_field_merge_tenant_model`
- Package: `github.com/eq-solutions/eq-design-tokens` @ v1.0.0

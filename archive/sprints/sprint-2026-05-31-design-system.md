---
title: Sprint — EQ Design System Component Buildout (A7–A11)
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Dated design-system sprint doc (archived snapshot)
read_priority: reference
status: archived
---
---
title: Sprint — EQ Design System Component Buildout (A7–A11)
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Finish @eq-solutions/ui (Modal/FormInput/StatusBadge/Card/Toast/Tabs) + self-host the font; written for a second console to review and execute
read_priority: standard
status: draft
---

# Sprint — EQ Design System Component Buildout (A7–A11)

> ⚠ **DRAFT — confirm with Royce before claiming or executing.**
> This sprint is **not yet authorised for full-auto.** The `ops/decisions.md` 2026-05-30 autonomy ADR (full-auto EQ build→PR→merge→deploy on green) was scoped to the **One Spine sprint, now complete**. A fresh "go" from Royce is required before any build / PR / merge / deploy under this sprint. Until then, treat this as a proposal: review it, sanity-check the open questions at the bottom, confirm with Royce, then claim.

## Goal

Finish the shared React component library so Shell + Service stop re-rolling primitives — completing the "seamless suite" at the component layer. Tokens + Button / Skeleton / Table already shipped (One Spine). This sprint extracts the remaining six primitives and self-hosts the font.

- **Why this is the lever:** Service carries ~45 local UI components; Shell rolls many from scratch. Every one is a future drift source. Promoting them into `@eq-solutions/ui` collapses the duplication.
- **Model + plan:** `ops/decisions.md` 2026-05-31 (tokens everywhere / components per-stack / pin-never-vendor), `design-system-consolidation-2026-05-31.md`.
- **Component sources, ranked:** `component-audit-2026-05-30.md`.
- **Board rows:** `SPRINT-BOARD.md` Stream A, A7–A11 (A12 already ✅).

## Already done — do NOT redo

- `@eq-solutions/tokens` v1.0 consumed (not vendored) across Shell / Service / Field / Cards.
- `@eq-solutions/ui` v1.0.1 = **Button / Skeleton / Table**, live in Shell + Service.
- A12 Claude Design context bundle — `eq/design/claude-design-context.md`.

## Pre-flight (every agent, before touching code)

1. Read `AUTONOMOUS-SPRINT-RULES.md`, then `STATE.md`, then `SPRINT-BOARD.md`.
2. **Claim your board row** (A7–A11): set `owner` + `branch` + 🔵 before starting. Don't start a row whose repo-area is already claimed.
3. **Branch from `origin/main` in an isolated worktree.** Stage explicitly (never `git add -A`). Verify the PR diff is only your files. Gate on the green deploy preview before merge.
4. **Carve-outs (unchanged):** no auth-flow deploys without Royce; SKS live untouchable. *This sprint touches neither* — pure package + UI work, no migrations.

## Two hard constraints (read before building anything)

1. **No Tailwind in the package.** `@eq-solutions/ui` ships SOURCE (`.tsx` + `.css` using `var(--eq-*)` tokens), consumed by git tag. **Shell cannot use Tailwind** (Vite + CSS modules). So every component must be styled with **token-based CSS** — the existing Button / Skeleton / Table pattern — NOT Tailwind utility strings. Service's source components use Tailwind `eq-*` utilities; extraction means **porting that styling to token CSS**, not copy-paste. Match the existing eq-ui conventions exactly (prop shapes, file layout, CSS class naming).
2. **eq-ui is a single-owner serial stream.** It's ONE repo; parallel agents editing it collide on version tags + the `index.ts` export surface. **Serialise the package work** — one component (one PR) at a time into eq-ui, each ending in a new tag (`vX`). *Consumer adoption* (Shell + Service) can then fan out in parallel per app once the tag exists. Never run two eq-ui PRs concurrently.

## Work items

### A7 — Modal + ConfirmDialog  [priority 1]
- **Source:** Service `components/ui/ConfirmDialog.tsx` (best-in-class — focus trap, Escape, scroll lock, `alertdialog` role), `Modal.tsx` (weakest — Escape only), `SlidePanel.tsx`.
- **Do:** Extract ConfirmDialog as the reference; bring Modal + SlidePanel up to the same a11y standard — focus trap, `role="dialog"` + `aria-modal`, body scroll lock, focus restore on close (this also closes polish-backlog **A1 + A2**). Portal-based. Token CSS.
- **Consumers:** Shell has **no** modal primitive (fills a gap); Service re-exports + drops its local copies.
- **Risk:** Low for Shell (additive). Medium for Service (swap ~5 Modal call sites) — keep the API stable.

### A8 — FormInput
- **Source:** Service `components/ui/FormInput.tsx` (~32 lines, label + error + hint, token-aligned). ~40 import sites in Service.
- **Do:** Port to token CSS; keep the prop API identical (40 sites). Shell adopts (it currently inlines inputs in `App.css`).
- **Consumers:** Shell (new), Service (re-export — API must not churn).
- **Risk:** Low–Medium (Service blast radius is the 40 sites; identical API = clean swap).

### A9 — StatusBadge + KindPill
- **Source:** Service `components/ui/StatusBadge.tsx` (typed `StatusKind` union, tone / size / dot props), `KindPill.tsx`.
- **Do:** Extract to token CSS; map Shell's CSS pills (`.eq-pill--ok/warn/err/info/mute`) onto the typed `StatusKind`.
- **Consumers:** Shell (replace CSS pills with the component), Service (re-export).
- **Risk:** Low; minor status-vocabulary mapping.

### A10 — Card + Toast + Tabs  (+ resolve ghost-border)
- **Card:** Service `components/ui/Card.tsx` (trivial). Shell has none — its absence makes every page re-invent padding/border.
- **Toast:** Service `components/ui/Toast.tsx` (`ToastProvider` + `useToast`, portal, auto-dismiss). Shell has none → direct lift.
- **Tabs:** greenfield (neither app has a real component) — design from Service's `border-b-2 border-eq-sky` pattern, token CSS.
- **Ghost-border:** apply polish-backlog PR #73 decision → **Option B**: add `border: 1px solid var(--eq-gray-200)` to the eq-ui Button **ghost** variant; Shell's `.eq-btn-ghost` becomes a passthrough.
- **Risk:** Low (Card/Toast are lifts; Tabs is a small greenfield).

### A11 — Font self-host  [independent — can run in parallel]
- **Do:** Ship Plus Jakarta Sans (woff2, the 400–800 weights in use) + an `@font-face` block from the **shared layer** so every pinned consumer self-hosts. Decide the package boundary: bundle into `@eq-solutions/tokens` (tokens.css gains `@font-face`) **or** a sibling `@eq-solutions/fonts` (design-token purists keep binaries out of tokens).
- **Consumers:** each app drops its Google-Fonts load — Shell (polish-backlog **P5** `@import`), Field (`index.html` link), Service (`next/font` → self-host), Cards (pubspec).
- **Risk:** Low; a perf + offline-resilience win. Runs in `eq-design-tokens`, independent of the eq-ui stream.

## Sequencing

- **eq-ui stream (serial, tag after each):** A7 → A8 → A9 → A10. One PR at a time; cut a new `@eq-solutions/ui` tag after each merges.
- **Consumer adoption (parallel per app):** once a component's tag exists, Shell-adopt and Service-adopt are independent PRs and can run concurrently — but watch the eq-shell hotspot `src/pages/TenantHome.tsx` (multiple prior PRs collide there; check `STATE.md`).
- **A11 (font):** parallel from day one — different repo (`eq-design-tokens`), no eq-ui dependency.

## Side quests (EQ-side, low-risk — fold in if capacity)

- **Confirm the pin-by-tag migration landed** (eq-ui v1.0.1 / eq-roles tags; move any `#main` consumers → `#vX`). ⚠ A concurrent session already owns this — **coordinate, don't double-claim.**
- **Add two drift items to `quality-polish-backlog-2026-05-30.md`** — Service emoji-in-Lucide (~7 files) + Service `RouteProgress` cyan→indigo gradient. **Verify vs `origin/main` first** (the 2026-05-31 audit read possibly-stale local clones).

## Definition of done

**Per component:**
- In eq-ui, token-based CSS, typed props matching existing conventions, exported from `index.ts`.
- New `@eq-solutions/ui` tag cut.
- Shell: local version replaced, `pnpm run build` clean, eyeballed (these are visible changes → visible-change review).
- Service: re-export swapped, `npm run check` + vitest green.
- Green deploy preview before merge. No auth / SKS touched.

**Sprint:**
- A7–A11 merged + live on EQ; all consumers pinned to the new eq-ui tag; ghost-border resolved; board rows A7–A11 → ✅.

## For the reviewing console — confirm before "go"

- [ ] Sequencing sound? (serial eq-ui stream, parallel consumer adoption, font in parallel)
- [ ] Anything here already in flight by another session? Check `STATE.md` worktrees (eq-shell `TenantHome` hotspot; eq-solves-service `charming-dirac`; eq-intake `clever-roentgen`).
- [ ] Ghost-border = **Option B** (1px border in eq-ui ghost) — agree, or keep borderless?
- [ ] Font package boundary — `@eq-solutions/tokens` vs new `@eq-solutions/fonts`?
- [ ] **Authorisation:** confirm with Royce that this sprint may run full-auto (build→PR→merge→deploy on green). The 2026-05-30 ADR does NOT cover it — it was scoped to the completed sprint.

## References

- `design-system-consolidation-2026-05-31.md` · `component-audit-2026-05-30.md` · `quality-polish-backlog-2026-05-30.md`
- `ops/decisions.md` 2026-05-31 (model) + 2026-05-30 (autonomy ADR — scope note above)
- `AUTONOMOUS-SPRINT-RULES.md` · `STATE.md` · `SPRINT-BOARD.md` Stream A
- `eq/design/claude-design-context.md` · memory `design_eq_profile`, `project_design_system_state`

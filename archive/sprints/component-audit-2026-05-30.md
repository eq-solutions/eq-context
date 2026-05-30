---
title: Component Duplication Audit — EQ Shell + EQ Service
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Read-only audit ranking duplicated UI primitives for a future @eq-solutions/ui package
read_priority: reference
status: live
---

## Summary

Both apps carry parallel implementations of the same UI primitives. EQ Service has a richer, more mature component library (`components/ui/`) using Tailwind utility classes with `eq-*` color tokens (`eq-sky`, `eq-deep`, `eq-ice`, `eq-ink`, `eq-grey`). EQ Shell uses inline styles (mostly hardcoded hex values) and CSS class names (`App.css`) — it imports `@eq-solutions/tokens` at the CSS level but its TSX components do not yet consume those tokens directly.

Token alignment status:
- **EQ Service** (`components/ui/`): fully token-aligned via Tailwind's `eq-*` color aliases (defined in `lib/tokens/tokens.css`, consumed via Tailwind config). All components use `text-eq-ink`, `bg-eq-sky`, etc.
- **EQ Shell** (`src/components/`): tokens are imported in `index.css` via `@eq-solutions/tokens/tokens.css`, but the TSX components use inline styles with raw hex values (e.g. `#1A1A2E`, `#E2EAF0`, `#EEF2F7`). The CSS layer (`App.css`) uses `var(--eq-*)` correctly; the React layer does not.

Eight primitive categories were assessed. Six have clear duplication warranting extraction.

---

## Ranked Duplication Table

| # | Primitive | EQ Shell location | EQ Service location | Usage count (Service) | Token-aligned? | Divergence | Rank |
|---|-----------|-------------------|---------------------|----------------------|----------------|------------|------|
| 1 | **Button** | `App.css` `.eq-btn-primary`, `.eq-btn-ghost` (CSS only, no TSX component) | `components/ui/Button.tsx` | ~74 import sites across 66 files | Service: yes. Shell: CSS tokens, no TSX component | Shell has no typed TSX component at all; Service has `variant` + `size` + `loading` props, Tailwind classes | **High** |
| 2 | **Table** | `src/components/EqTable.tsx` | `components/ui/DataTable.tsx` | ~25 import sites (DataTable) + CSS `.eq-table` class used widely | Shell: hardcoded hex. Service: token-aligned | Same sort logic; Service adds filterable columns, row selection, row click; Shell uses inline styles with raw hex; header colour is `#1A1A2E` in Shell vs `bg-eq-ice` in Service | **High** |
| 3 | **Skeleton** | `src/components/Skeleton.tsx` | `components/ui/Skeleton.tsx` | ~10 import sites (Skeleton) | Shell: CSS tokens via `.eq-skeleton` class. Service: Tailwind `animate-pulse bg-gray-200` | Shell: uses CSS class variants (`eq-skeleton--row/card/text`), `<span>` elements, shimmer animation via CSS. Service: Tailwind `animate-pulse`, `<div>`, shape prop (`text/line/circle/card`); also ships `SkeletonRows` + `SkeletonCards` composites | **High** |
| 4 | **Modal / Dialog** | `App.css` — no standalone TSX component; modals are ad-hoc per-page | `components/ui/Modal.tsx`, `components/ui/ConfirmDialog.tsx` | `Modal`: ~5 import sites; `ConfirmDialog` provider mounted at app root | Shell: no typed component. Service: fully typed with portal, Escape handling, backdrop-click, focus trap (ConfirmDialog), `destructive` variant | Shell has no reusable modal primitive — extraction fills a gap rather than reconciling divergence | **High** |
| 5 | **Badge / Pill** | `App.css` `.eq-pill`, `.eq-pill--ok/warn/err/info/mute`; `.eq-hub-tile__badge`; `.eq-module-card__chip` (CSS only) | `components/ui/StatusBadge.tsx`, `components/ui/KindPill.tsx` | StatusBadge: ~15+ sites; KindPill: ~8 sites | Service: token-aligned. Shell: CSS tokens via `var(--status-*)` | Service has typed `StatusKind` union, `tone`, `size`, `dot` props. Shell has CSS classes only, no TSX wrapper; status values are a loose convention | **Med** |
| 6 | **Route Progress Bar** | `src/components/RouteProgressBar.tsx` | `components/ui/NavigationProgress.tsx` | Service: 1 mount site in layout | Shell: CSS animation classes (`eq-progress-bar--running/done`). Service: `bg-eq-sky` Tailwind, inline `width` style | Same behaviour; Shell ties to React Router `useLocation`; Service ties to Next.js `usePathname`/`useSearchParams`. Color token used in Service; raw CSS transition in Shell | **Med** |
| 7 | **Card** | No TSX component; cards are ad-hoc divs in pages | `components/ui/Card.tsx` | ~3 direct import sites; layout pattern used everywhere | Service: token-aligned (`border-gray-200`, `bg-white`, `rounded-lg`). Shell: no component | Trivial component, but its absence in Shell means every page re-invents padding/border | **Low** |
| 8 | **Form Inputs** | No TSX component; inputs are styled in `App.css` and inlined per-page | `components/ui/FormInput.tsx` | ~40 direct import sites across 40 files | Service: token-aligned (`border-gray-200`, `focus:border-eq-deep`, `focus:ring-eq-sky/20`). Shell: no component | Service ships label + error + hint compositing. Shell has no typed component | **Med** |

---

## Tabs

Both apps implement a tab/nav pattern but not as a shared component:

- **Shell** (`App.css`): `.eq-tabs` / `.eq-tab` / `.eq-tab--active` — border-bottom highlight using `var(--eq-brand)` (token-aligned at CSS layer). No TSX wrapper.
- **Service** (`app/(app)/testing/TestingNav.tsx`): inline tab pattern using `border-b-2 border-eq-sky` Tailwind classes. No shared `Tabs` TSX component.

Both are ad-hoc implementations of the same pattern. A shared `<Tabs>` component does not yet exist in either app — this is a greenfield extraction rather than reconciliation.

---

## Toast

Shell has no toast/notification system. Service has a complete `components/ui/Toast.tsx` with `ToastProvider`, `useToast()` hook, portal rendering, auto-dismiss, and `success/error/info` kinds. Extraction here is a direct lift from Service with no Shell counterpart to reconcile.

---

## Recommended Extraction Order

Ordered by **value × inverse difficulty** (high reuse, low cost first):

### 1. Button (Priority: extract immediately)
- **Why first**: Shell has zero TSX Button component; everything is CSS classes. Service has the definitive implementation with loading state, variants, and sizes across 66 files. Extraction = promote `components/ui/Button.tsx` to the package, then update Shell to import and use it (replacing `.eq-btn-primary` / `.eq-btn-ghost` inline usage).
- **Cost**: Low. Service component is already token-aligned, well-typed, and tested at scale. Shell needs a `cn` / Tailwind dependency or the package needs a CSS-vars variant.
- **Files to start**: `C:\Projects\eq-solves-service\components\ui\Button.tsx` → `@eq-solutions/ui/Button`

### 2. Skeleton (Priority: extract next)
- **Why second**: Used in 10 Shell pages + Service; both implementations are simple and do the same thing. Service's Tailwind approach (`animate-pulse`) is cleaner than Shell's shimmer-gradient CSS animation, but the API (`shape` vs `variant`) needs a unified prop name. Low code complexity, high surface area.
- **Reconciliation needed**: Rename prop (`variant` in Shell → `shape` in Service); pick one animation approach (recommend Tailwind `animate-pulse` as it's token-free). Shell's `count` repeat prop is useful to keep.
- **Files to start**: `C:\Projects\eq-shell\src\components\Skeleton.tsx`, `C:\Projects\eq-solves-service\components\ui\Skeleton.tsx`

### 3. Table (Priority: extract after Button + Skeleton)
- **Why third**: Both apps have a fully working sortable table — highest-value primitive. But Shell's `EqTable` hardcodes hex values throughout (7 raw hex/rgba literals), while Service's `DataTable` is fully token-aligned. Service also has more features (filterable columns, row selection, row click). Extraction needs Shell's `EqTable` to be refactored to tokens first, then merged with Service's DataTable feature set.
- **Reconciliation needed**: 
  - Align prop naming: Shell uses `data`/`rowKey`/`rowStyle`, Service uses `rows`/`getRowId`/`onRowClick` — pick one convention.
  - Shell: replace `background: '#1A1A2E'` with `var(--eq-ink)`, `#E2EAF0` → `var(--eq-gray-200)`, `#EEF2F7` → `var(--eq-gray-100)`, `#6B7A99` → `var(--eq-grey)`.
  - Merge feature sets: add Service's filterable + selectable + onRowClick to the extracted component.
- **Files to start**: `C:\Projects\eq-shell\src\components\EqTable.tsx`, `C:\Projects\eq-solves-service\components\ui\DataTable.tsx`

### 4. Modal / ConfirmDialog (Priority: fills Shell gap)
- Shell has no modal primitive. Service's `Modal.tsx` + `ConfirmDialog.tsx` are production-grade with accessibility (focus trap, Escape, body scroll lock, `alertdialog` role). Lift both directly.
- **Files to start**: `C:\Projects\eq-solves-service\components\ui\Modal.tsx`, `C:\Projects\eq-solves-service\components\ui\ConfirmDialog.tsx`

### 5. FormInput (Priority: fills Shell gap)
- Shell has no input component. Service's `FormInput.tsx` is small (32 lines), fully token-aligned, ships label/error/hint — a clean lift.
- **File**: `C:\Projects\eq-solves-service\components\ui\FormInput.tsx`

### 6. StatusBadge / Pill (Priority: after core primitives)
- Shell's pill system is CSS-only with a looser status vocabulary. Service's `StatusBadge` has a typed `StatusKind` union and two tone variants. Some mapping work needed to align Shell's `ok/warn/err/info/mute` to Service's `complete/overdue/blocked/in-progress/inactive`.
- **Files to start**: `C:\Projects\eq-solves-service\components\ui\StatusBadge.tsx`, `C:\Projects\eq-solves-service\components\ui\KindPill.tsx`

### 7. Toast (Priority: Shell adoption only)
- Direct lift from Service. Shell has no equivalent. No reconciliation needed.
- **File**: `C:\Projects\eq-solves-service\components\ui\Toast.tsx`

### 8. Tabs (Priority: greenfield — lower urgency)
- Neither app has a proper TSX Tabs component. Both inline the pattern. Design a shared `<Tabs>` component from scratch using Service's `border-b-2 border-eq-sky` token-aligned pattern as the visual baseline.

---

## Key Technical Notes

1. **Shell cannot use Tailwind today.** EQ Shell is a Vite + React + CSS-modules project. `@eq-solutions/ui` will need to ship either (a) plain CSS custom-property styles, or (b) a separate CSS bundle compiled from Tailwind. The cleanest path for the package is `var(--eq-*)` inline props or a pre-compiled CSS file — not raw Tailwind class strings.

2. **Service vendor-copies tokens.** `C:\Projects\eq-solves-service\lib\tokens\tokens.css` is a local copy of `@eq-solutions/tokens`. Shell imports the package directly. When the UI package ships, both apps should import from `@eq-solutions/tokens` (not the local copy) and `@eq-solutions/ui`.

3. **Shell EqTable is the only active Shell component with a direct Service counterpart and hardcoded values** — it's the highest-priority token-alignment fix before extraction.

4. **Service Button is used at 66 import sites** — the highest usage count of any primitive in the audit. It is the single highest-leverage extraction candidate.

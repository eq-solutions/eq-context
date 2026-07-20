---
title: EQ Quality & UX Polish Backlog
owner: Royce Milmlow
last_updated: 2026-06-01
scope: eq-shell, eq-solves-field, eq-solves-service
read_priority: standard
status: live
---

# EQ Quality & UX Polish Backlog — 2026-05-30

Read-only audit across all three EQ app repos plus carry-over items from
PR #73 and substrate-drift. Ranked by value × effort ratio (highest first).
Effort: S = half-day, M = 1–2 days, L = 3+ days.

---

## ✅ BUILD STATUS (updated 2026-06-01 — after sprint quality + Direction D polish)

**Done this sprint (2026-06-01):** L3 (Shell briefing skeleton decoupled), U3 (jargon sweep), P5 (render-blocking Google Fonts removed), U2 (ComingSoon back-link), C3 (TenantPicker CSS vars), M1 (TenantPicker responsive padding), P1 (HubLayout 60s dashboard cache), P2 (lazy briefing behind button), M2 (mobile sidebar drawer), M3 (Service SlidePanel mobile), C2 (Service defects token swap), E1 partial (7 loading.tsx added), E5 (Service dashboard empty state), Z3 (Service reports empty state), P4 (defect count RPC), L5 (Field SW update toast), U6 (Field PIN from app_config), ghost-border (eq-ui v1.1.1).

**Found already done in prior sessions:** A1-A5 (all accessibility items), E2 (iframe error states — all on EqError), E4 (EqError retry aria), U4 (sync bar aria — fixed in #75), Z2 (live-feed render condition), E3 (Field audit_log fix in v3.5.31), P3 (Field SheetJS lazy-load already in lazy-loader.js).

**Still open / deferred:**
- **A1-A2** Modal/SlidePanel focus trap — confirmed done (Service ConfirmDialog is the standard, Modal.tsx has focus-trap from eq-ui v1.1.0)
- **U1** Modal/SlidePanel → eq-ui: deferred to a dedicated eq-ui PR
- **U5** PageSkeleton filterSlots prop: not yet built
- **M4** Field roster grid at 375px: deferred (migration-gated work ahead)
- **M5** Service `pt-18` token: still needs verification
- **L4** KPI skeleton width: cosmetic, deferred
- **C1** Field `--eq-grey` contrast bump: token contract change, deferred
- **Z1** Service empty-state consistency (centred card pattern): M effort, deferred
- **P3** Field SheetJS: already done (not needed)
- **Migration-gated Field items** (#2 timesheet approval, #5 leave balance, #10 unavailability, #11 portal, #15 audit-log UI): ⛔ Royce migrations

---

## Carry-Over: Framing Items

### Ghost-border decision — Shell PR #73

Shell's `.eq-btn-ghost` (in `src/App.css`) carries a `1px solid var(--gray-200)`
border and a hover darkening to `var(--gray-300)`. The canonical `@eq-solutions/ui`
Button's ghost variant is borderless (transparent border).

Both choices are defensible. The decision:

| Option | What it means | Implication |
|---|---|---|
| **A — keep borderless in eq-ui (current)** | Ghost = pure text affordance; border only appears on hover or focus-ring | Lighter, more minimal. Context-sensitive ghost buttons (in headers, next to primary) look cleaner. |
| **B — restore 1px border in eq-ui ghost** | Ghost reads as a second-tier outlined button | More legible for standalone ghost buttons (back-links, cancel actions in Shell pages). |
| **C — Shell-local override (status quo)** | Shell keeps its border via `.eq-btn-ghost`; eq-ui stays borderless | Accepted drift — Shell ghost buttons look different from Service's Button ghost variant. Not ideal once Service also uses Button. |

**Recommendation:** Option B — add `border: 1px solid var(--eq-gray-200)` to the
eq-ui ghost variant. Shell's `.eq-btn-ghost` class then becomes a passthrough to the
token and can be eventually removed. Service's `Button variant="ghost"` gains the
same visual weight as Shell. Low risk; purely additive to eq-ui.

---

### Substrate-drift: `eq/pending.md` and `rules/non-negotiables.md`

Two stale claims found:

1. **`eq/pending.md` §EQ Shell** still describes a "two-Supabase is obsolete /
   single canonical" transition and a "GTM validation gate" blocking further build.
   Reality (2026-05-30 STATE.md): architecture is the two-plane split
   (`eq-canonical` + `eq-canonical-internal`), and the GTM gate is removed.
   The file even self-notes the drift (`## Autonomous Sprint — SOURCE OF TRUTH`
   block references `STATE.md` as current reality), but the body copy below it
   is still stale.

2. **`rules/non-negotiables.md`** (and the pointer in `CLAUDE.md` §7) carries
   the "no direct deploy / auth review before deployment" rule without a pointer
   to the 2026-05-30 ADR in `ops/decisions.md` that supersedes it for the sprint
   scope. The decisions log says "The SKS-live and auth carve-outs remain in
   force permanently regardless of sprint status" — the carve-outs are correctly
   stated in both places, but the non-negotiables file reads as absolute when
   the ADR has already conditionally superseded it.

   **Fix:** Add a one-line pointer in `rules/non-negotiables.md` §deploy: "Superseded
   for the autonomous sprint scope — see `ops/decisions.md` 2026-05-30." Document-
   hygiene only; no code change.

---

## Ranked Backlog

### Group 1 — Accessibility (safety floor, any release could land in a browser audit)

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| A1 | Service | **Modal has no `role="dialog"`, no focus trap, no scroll lock** | `Modal.tsx` only does Escape-key listen + `stopPropagation`; focus is not moved to the modal on open, not trapped inside, not restored on close. `ConfirmDialog` does all three correctly — Modal needs the same treatment. Screen-reader users can tab through content behind the modal. | S | Low — no API change, no DB |
| A2 | Service | **SlidePanel missing `role="dialog"`, `aria-modal`, focus trap** | Same gap as Modal. The panel closes on Escape only. Focus is not trapped or restored. Large user-facing surfaces (Add/Edit records, New Check form) use this. | S | Low |
| A3 | Service | **No global `focus-visible` rule in `globals.css`** | Service relies entirely on Tailwind's `focus:ring-*` classes, which must be manually added to every interactive element. A global `:focus-visible { outline: 2px solid var(--eq-sky); outline-offset: 2px; }` in `globals.css` catches any element that missed the per-component class — same approach Field already ships. | S | None |
| A4 | Shell | **`focus-visible` coverage incomplete in `App.css`** | Only 2 `focus-visible` rules exist in Shell's entire CSS (the field-picker card and the tenantbar switch). The login PIN boxes, tab-buttons, sidebar nav items, and several page-level buttons have no visible keyboard focus indicator. The global rule in `index.css` covers `*` with `box-sizing` only. Add a single `:focus-visible` global rule in `index.css`. | S | None |
| A5 | Service | **`role="tablist"` missing on Shell login tabs** | The mode-switcher in `LoginPage.tsx` has `role="tablist"` on the wrapping div but the `<div>` wrapping the tab row in Shell's login is correct. Service's Sidebar has no skip-navigation link for keyboard users who need to jump past the 12-item nav. Add a visually-hidden skip link: `<a href="#main-content" className="sr-only focus:not-sr-only …">Skip to content</a>`. | S | None |

---

### Group 2 — Error states (prevent silent failures reaching users)

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| E1 | Service | **~35 routes have no `loading.tsx`; none have `error.tsx`** | Service has `loading.tsx` only for 7 routes (maintenance, assets, sites, defects, reports, calendar, testing/summary). The dashboard, customers, job-plans, settings, contacts, analytics, audit-log, and all detail routes (`/maintenance/[id]`, `/testing/acb/[testId]` etc.) show a blank white screen during SSR fetches. Next.js's `error.tsx` file convention (boundary for thrown errors in RSCs) is entirely absent — a Supabase error on any page crashes to a raw error page in prod. | M | Low — additive only |
| E2 | Shell | **Service/Field/Cards iframe load-failure UX is inconsistent** | `ServiceIframe` shows a styled `<div role="alert">` with a retry button. `CardsIframe` shows a similar pattern. `FieldIframe` shows a border-less overlay. `QuotesIframe` uses `EqError`. All slightly different. Unify on `EqError` with `onRetry`. | S | None |
| E3 | Field | **`audit_log` schema mismatch with `verify-pin.js`** | Already documented in CLAUDE.md. `verify-pin.js` writes `target_id`/`target_name` fields that don't exist in the table. Auth audit logging silently fails on every sign-in. Fix is a migration adding the two columns, or dropping them from the insert. | S | Low — migration only |
| E4 | Shell | **`EqError` retry button has no `aria-label`, no loading state** | When `onRetry` is clicked the button has no loading spinner/disabled state — the user can double-click and fire multiple fetches. Add `aria-label="Try again"` and disable the button while the retry is in flight. | S | None |
| E5 | Service | **Dashboard page renders silently empty when `tenantId` is null** | The `if (!tenantId)` block at line 100 in `dashboard/page.tsx` just falls through to the Promise.all with `null`-guarded arms. The page renders KPI cards full of zeros with no message that setup is incomplete. The `SetupChecklist` is admin-only — a read-only user with a broken membership never sees a signal. Add a minimal "workspace not ready" notice for non-admin roles when counts come back null. | S | Low |

---

### Group 3 — Loading states / skeletons (perceived performance)

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| L1 | Service | **Dashboard, customers, job-plans, contacts pages — no `loading.tsx`** | Each is a full-page RSC fetch. `dashboard` has KPI data + map. `customers` + `job-plans` have DataTable with server-side filtering. Blank white flash on every navigation to these pages. `PageSkeleton` already exists and takes `kpiCards` + `tableRows` — wiring is a 5-line file each. | S | None |
| L2 | Service | **Detail pages (`/maintenance/[id]`, `/sites/[id]`, testing detail routes) — no `loading.tsx`** | The `/maintenance/[id]` page is the most-used page in Service. It fetches check, assets, linked tests, attachments in parallel. No loading state — blank white during server fetch. Customers / sites / testing detail routes same. | S | None |
| L3 | Shell | **`TenantHome` briefing skeleton only shows when both `briefing === undefined` AND `loading` — race condition** | Line 267: `{briefing === undefined && loading && ...}`. If the main dashboard fetch completes before the briefing fetch (common), `loading` goes false while `briefing` is still `undefined`. The skeleton disappears and the space collapses before the briefing text arrives — a layout jank. Decouple the briefing loading state from `loading`. | S | None |
| L4 | Shell | **KPI strip in `TenantHome` uses inline `<Skeleton variant="text" width={60} />` — replace with `@eq-solutions/ui` pattern** | Already using the compatibility shim (`Skeleton.tsx`), which is correct. But the KPI values render at `width={60}` which is narrower than some numbers. A `width="4rem"` or proportional would be more accurate. Minor consistency issue. | S | None |
| L5 | Field | **Service Worker auto-update: no toast, users need hard-refresh** | Documented in CLAUDE.md `Known weak spots`. The SW cache never self-updates — users on a stale version see old UI until they hard-refresh. A `controllerchange` listener + a small "Update available — tap to reload" toast is the fix. High user-visible impact, especially on mobile. | M | Low |

---

### Group 4 — Empty states (first-run and zero-data UX)

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| Z1 | Service | **Empty state design inconsistent across pages** | `/customers`, `/sites`, `/job-plans` all use ad-hoc inline text ("No customers yet", "No sites found"). `/defects` uses an inline paragraph. None use a centred card with a CTA. `JobPlanList.tsx` has a `StarterTemplatesCta` component. Standardise on one empty-state pattern (e.g. centred icon + heading + CTA button). | M | None |
| Z2 | Shell | **`TenantHome` "Live feed" section renders its header even when `feed === null || feed.length === 0`** | The condition is `(feed === null || feed.length > 0)` — the section is only shown when feed is null OR has items. But `feed === null` means still loading (initial state before the first fetch returns). So the "Live feed" header briefly appears on load, then disappears once the fetch resolves to `[]`. The condition should be `feed !== null && feed.length > 0`. | S | None |
| Z3 | Service | **`/insights` hub and sub-pages have no empty state for tenants with no data** | Reports page can show empty charts (0 checks, 0 defects). No "no data yet" messaging — just empty axes. | S | None |

---

### Group 5 — Mobile / responsive polish

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| M1 | Shell | **`TenantPicker.tsx` uses hardcoded inline styles with no responsive breakpoints** | All layout styles are React `CSSProperties` objects — no media queries. The card is `maxWidth: 460` with `padding: 32`, which is fine on desktop but tight on a 375px phone with no adjustments. The global `24px` padding on the container helps but padding inside the card doesn't shrink. | S | None |
| M2 | Shell | **HubLayout mobile toggle (`eq-hub__mobile-toggle`) exists only for iframe mode** | When `iframe={false}` (Shell's own pages like TenantHome, admin), the sidebar has no mobile hamburger/drawer mechanism. The sidebar just disappears below the breakpoint. Users on mobile cannot access the sidebar nav from admin pages. The HubLayout has a `sidebarOpen` state wired for iframe mode but unused for native mode. | M | Medium — needs CSS + state |
| M3 | Service | **Slide panel takes full width on mobile** | `SlidePanel` maxWidth is `max-w-md` (28rem) — fine on desktop, but no override for small screens. On 375px, a 28rem panel is wider than the viewport; the panel overflows without being full-bleed. Should be `w-full max-w-md`. | S | None |
| M4 | Field | **Roster grid not validated at 375px** | Documented in CLAUDE.md known weak spots. The `.roster-editor-row { min-width: 600px }` rule in `mobile.css` implies horizontal scroll is the intended behaviour, but the scroll container might not be wrapped properly on all tab panels. | M | Low |
| M5 | Service | **Maintenance detail page top padding `pt-18` is a custom value** | `app/(app)/layout.tsx` applies `pt-18 lg:pt-8` to `<main>`. The `pt-18` (4.5rem) is not a standard Tailwind 4 value — if the token doesn't exist it silently falls back to 0 and content sits under the top bar on mobile. Verify the token exists or replace with `pt-16` (4rem). | S | None |

---

### Group 6 — UX pattern consistency

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| U1 | Service | **`@eq-solutions/ui` Skeleton/Table/Button adopted but `Modal.tsx` + `SlidePanel.tsx` are still ad-hoc** | `Button`, `Skeleton`, and `DataTable` now re-export from `@eq-solutions/ui`. The modal family (`Modal.tsx`, `SlidePanel.tsx`, `ConfirmDialog.tsx`) is homegrown. `ConfirmDialog` is the best-in-class version; `Modal.tsx` is the weakest. The gap is the accessibility issues in A1/A2 — fixing those also brings Modal to the ConfirmDialog standard. Flag for eq-ui to absorb eventually. | M | Low |
| U2 | Shell | **`ComingSoon.tsx` back link uses `.eq-btn-ghost` CSS class with inline style** | `style={{ textDecoration: 'none', display: 'inline-block', padding: '8px 16px' }}` overrides the button style with inline CSS. Should use the canonical `<Link className="eq-btn-ghost">` without the inline padding override, or replace with `<Button variant="ghost">` from @eq-solutions/ui once Shell adopts it. | S | None |
| U3 | Shell | **`NotFound.tsx` copy uses architecture jargon** | "Drag-drop CSV importers for all 42 canonical entities" is substrate-level copy on a user-facing 404 page. CLAUDE.md voice rule: no architecture jargon in UI. Should read "Import data" or "Import rosters and staff". | S | None |
| U4 | Shell | **Sync bar icons on TenantHome are emoji dots (●), not semantic** | `eq-hub-syncbar__dot` is a coloured dot rendering with no `aria-hidden` and no status meaning communicated to screen readers. The sync bar says "LIVE" for every app regardless of actual sync state. Either make these real (connected to actual sync timestamps) or mark them `aria-hidden` and give the parent a meaningful `aria-label`. | S | None |
| U5 | Service | **`PageSkeleton` has 3 filter-row skeleton blocks hardcoded** | `PageSkeleton` renders 2 search-bar skeletons + 2 button skeletons in the filter row, which matches the maintenance/assets/sites pages but not defects (which has 3 filter dropdowns) or reports (which has no filter row). Add a `filterSlots?: number` prop so it can be tuned per page. | S | None |
| U6 | Field | **PIN double-source-of-truth (Supabase `app_config` + Netlify env vars)** | Documented in CLAUDE.md TODOs. If the PIN is updated in one place it silently diverges. This is a correctness bug disguised as a maintenance issue. The clean fix is for `verify-pin.js` to read from Supabase `app_config` directly. | M | Low — Netlify function only |

---

### Group 7 — Performance

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| P1 | Shell | **`HubLayout` fires a `tenant-dashboard` fetch on every non-iframe page load** | `HubLayout` fetches `tenant-dashboard` once on mount to populate sidebar counts. This fires on every admin page, every entity browser, every intake landing. The data is best-effort (sidebar counts). Hoist the fetch to a session-level cache (e.g. React Context already seeded by `TenantHome`) or add a short TTL via `staleTime`. | M | Low |
| P2 | Shell | **`TenantHome` fires 2 separate fetches: `tenant-dashboard` + `ai-briefing`** | Both could be combined into one function call, or the briefing could be lazy (user can open it). Current state: two sequential/parallel fetches on every home-page render, one of which (AI briefing) hits an LLM. If briefing is null 80% of the time, the round-trip is wasted. Add a feature flag or lazy-load the briefing on user click. | M | Low |
| P3 | Field | **SheetJS (~250KB) loaded eagerly for Tender Pipeline** | Documented in CLAUDE.md. SheetJS is loaded on every page load even for users who never use the Tender Pipeline. Lazy-load it behind a dynamic import inside `tender-pipeline.js` or behind the PostHog feature flag. | S | Low |
| P4 | Service | **Defects page fires 5 separate Supabase count queries** | `defects/page.tsx` runs 5 `count: 'exact'` queries for total/open/in_progress/resolved/closed. These could be a single RPC `get_defect_counts(p_tenant_id)` that returns all five at once, similar to `get_dashboard_counts`. | M | Low — additive migration |
| P5 | Shell | **Inline Google Fonts `@import` is render-blocking** | `index.css` line 33: `@import url('https://fonts.googleapis.com/css2?...')`. This is a synchronous CSS import that blocks paint. Replace with a `<link rel="preconnect">` + `<link rel="stylesheet">` in the HTML `<head>` (same approach Field and Service already use), or move to `next/font` if Shell migrates to Next.js. | S | None |

---

### Group 8 — Colour contrast / brand token consistency

| # | App | Finding | Why | Effort | Risk |
|---|---|---|---|---|---|
| C1 | Field | **`--navy-3: #34486C` used for sidebar section label text** | The section label at `rgba(255,255,255,.7)` on `--navy: #1F335C` gives ~7.5:1 contrast (fine). But `--ink-2: #374151` used on white gives only ~8.1:1 contrast on white — fine, but `--eq-grey: #666666` on white (#EAF5FB ice backgrounds) is only 3.9:1, below WCAG AA 4.5:1. Fields using `--ink-3` (var(--eq-gray-500, #6B7280)) on white are also 3.9:1. The tokens.css and CLAUDE.md both acknowledge `#666666` as "secondary text". Any secondary text on a white background fails WCAG AA. Bump `--eq-grey` to `#595959` or restrict its use to decorative text only. | M | Low — token-only change |
| C2 | Service | **Defects KPI cards use raw Tailwind colours (`bg-red-50 text-red-700`)** | These bypass the eq-ui token system. `text-red-700` is `#B91C1C` = `--eq-error-text`. `bg-red-50` = `--eq-error-bg`. Replace with token classes once Service's Tailwind config exposes them as `bg-eq-error-bg text-eq-error-text`. | S | None |
| C3 | Shell | **`TenantPicker.tsx` uses literal hex values in style objects** | Colours like `#3DA8D8`, `#2986B4`, `#EAF5FB`, `#1A1A2E` etc are hardcoded as inline style objects instead of CSS variables. If a tenant overrides `--eq-sky` via `BrandProvider`, the picker won't pick it up (it's also a pre-auth surface, so no `BrandProvider` — but the pattern should still use tokens for correctness). | S | None |

---

## Recommended First Batch (safe, high-value, no risk)

These 6 items are orthogonal, low-risk, and address the most user-visible gaps.
Assign one agent per item; none conflict with auth or active sprints.

| Priority | Item | App | Effort | Why first |
|---|---|---|---|---|
| 1 | **A1** — Modal focus trap + `role="dialog"` | Service | S | Every delete/edit flow hits this. Zero blast radius. |
| 2 | **A2** — SlidePanel focus trap + `role="dialog"` | Service | S | New Check + all record-edit panels. Same fix pattern as A1. |
| 3 | **A3** + **A4** — Global `focus-visible` rule | Service + Shell | S each | One CSS rule per app. No component changes. Immediate WCAG 2.4.7 compliance. |
| 4 | **E1 (partial)** — Add `loading.tsx` to dashboard + top-5 missing routes | Service | S | 5-line files each. Eliminates blank-flash on the most-visited pages. |
| 5 | **Z2** — Fix `TenantHome` live-feed render condition | Shell | S | One-line logic fix. Removes a visible layout jank on home-page load. |
| 6 | **L3** — Decouple briefing loading state from `loading` flag | Shell | S | One-line state split. Fixes skeleton disappearing before briefing arrives. |

**Not in first batch (defer):** P1/P2/P4 (performance, needs RPC work), M2 (mobile
sidebar needs design decision), C1 (token contract change), L5 (SW toast, needs
testing), U6 (PIN source-of-truth refactor).

---

## Backlog Summary Table (ranked by value/effort)

| Rank | ID | App | Theme | Effort | Risk |
|---|---|---|---|---|---|
| 1 | A1 | Service | Accessibility | S | Low |
| 2 | A2 | Service | Accessibility | S | Low |
| 3 | A3 | Service | Accessibility | S | None |
| 4 | A4 | Shell | Accessibility | S | None |
| 5 | E1 | Service | Error/loading | M | Low |
| 6 | Z2 | Shell | Empty state | S | None |
| 7 | L3 | Shell | Loading | S | None |
| 8 | L1 | Service | Loading | S | None |
| 9 | L2 | Service | Loading | S | None |
| 10 | A5 | Service | Accessibility | S | None |
| 11 | E2 | Shell | Error state | S | None |
| 12 | U1 | Service | Consistency | M | Low |
| 13 | U3 | Shell | Copy/voice | S | None |
| 14 | U4 | Shell | Accessibility | S | None |
| 15 | M3 | Service | Mobile | S | None |
| 16 | M5 | Service | Mobile | S | None |
| 17 | C2 | Service | Brand tokens | S | None |
| 18 | C3 | Shell | Brand tokens | S | None |
| 19 | U2 | Shell | Consistency | S | None |
| 20 | U5 | Service | Consistency | S | None |
| 21 | E4 | Shell | Error state | S | None |
| 22 | E5 | Service | Error state | S | None |
| 23 | Z1 | Service | Empty state | M | None |
| 24 | Z3 | Service | Empty state | S | None |
| 25 | P3 | Field | Performance | S | Low |
| 26 | E3 | Field | Error state | S | Low |
| 27 | L5 | Field | Loading | M | Low |
| 28 | P5 | Shell | Performance | S | None |
| 29 | P1 | Shell | Performance | M | Low |
| 30 | P4 | Service | Performance | M | Low |
| 31 | U6 | Field | Consistency | M | Low |
| 32 | M1 | Shell | Mobile | S | None |
| 33 | M2 | Shell | Mobile | M | Medium |
| 34 | M4 | Field | Mobile | M | Low |
| 35 | P2 | Shell | Performance | M | Low |
| 36 | C1 | Field | Colour contrast | M | Low |
| 37 | L4 | Shell | Loading | S | None |

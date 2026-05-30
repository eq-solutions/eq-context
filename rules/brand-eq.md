---
title: EQ Brand — Rules & Assets
owner: Royce Milmlow
last_updated: 2026-05-24
scope: EQ Solutions brand specification — colours, fonts, logos, usage rules
read_priority: critical
status: live
---

# EQ Brand Rules

Canonical brand spec for all EQ Solutions outputs (UI surfaces, marketing, documents, emails). Design Brief version: **v1.3**.

Programmatic source: `eq-design-tokens` (`C:\Projects\eq-design-tokens`) — JSON → CSS/TS/Dart/Tailwind. This file governs intent and rules; the token files govern exact values.

---

## 1. Logo Files — R2 CDN (definitive source)

Base URL: `https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/`

| File | Use case |
|---|---|
| `EQ_logo_blue_transparent.svg` | Primary — on white/light backgrounds (sky `#3DA8D8` mark) |
| `EQ_logo_white_transparent.svg` | On dark backgrounds (`--eq-ink`, sidebar, dark shells) |

**Two approved variants only.** No black variant. No colour-modified variants.

**Rules:**
- Minimum size: 24px tall. Clear space = logo height on all sides.
- Never recolour, stretch, skew, shadow, outline, or gradient the mark.
- Blue variant on light backgrounds only. White variant on dark (`--eq-ink`, `--eq-deep`) only.
- Never place the blue logo on a dark background — switch to white.
- Never place on busy photography.

---

## 2. Colour Palette

### Brand tokens (CSS custom properties)

| Token | Hex | Use |
|---|---|---|
| `--eq-sky` | `#3DA8D8` | Primary — logo, headings, CTAs, icon fills, table headers |
| `--eq-deep` | `#2986B4` | Hover state for anything blue; secondary headings |
| `--eq-ice` | `#EAF5FB` | Page/card tint; table header alternate fill |
| `--eq-ink` | `#1A1A2E` | Body text, dark sidebar — never pure black |
| `--eq-grey` | `#666666` | Secondary text, labels, metadata |
| `--eq-white` | `#FFFFFF` | Text on blue/ink surfaces |

### Neutral scale

`#F9FAFB` (gray-50) · `#F3F4F6` (gray-100) · `#E5E7EB` (gray-200, default border) · `#D1D5DB` (gray-300, input border) · `#9CA3AF` (gray-400) · `#6B7280` (gray-500) · `#4B5563` (gray-600)

### Status colours (never as brand)

| State | Background | Text |
|---|---|---|
| Success | `#F0FDF4` | `#15803D` |
| Warning | `#FFFBEB` | `#B45309` |
| Error | `#FEF2F2` | `#B91C1C` |

**WCAG AA pairings:** Ink on White (18.1:1) ✓ · Ink on Ice (16.2:1) ✓ · White on Deep Blue (4.6:1) ✓. Sky on White (3.0:1) — large text (18pt+) and UI components only, never body copy.

---

## 3. Typography

| Use | Font | Weight | Notes |
|---|---|---|---|
| All UI / web text | Plus Jakarta Sans (variable) | 200–800 | Self-hosted |
| Display / print fallback | Aptos Display → Aptos → Arial | — | Non-web environments |
| Form labels | Plus Jakarta Sans | 600 | 11–12px, UPPERCASE, tracking 0.06em, `--eq-grey` |
| Body default | Plus Jakarta Sans | 400 | 14px / 1.5 line-height / `--eq-ink` |

**Type scale (px):** xs 11 · sm 12 · base 14 · md 15 · lg 18 · xl 22 · 2xl 28 · 3xl 36 · 4xl 48

**Tracking:** Display + large headings — tight (-0.01em to -0.02em). Body and labels — default.

---

## 4. Layout & Spacing

**Grid:** 8-pixel base, 4px half-step. Steps: 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64. Max content width: 1200px centred.

**Radii:**

| Surface | Radius |
|---|---|
| Chips | 4px |
| Pills (badges, avatars) | 9999px |
| Buttons, inputs | 6px |
| Cards | 8px |
| Large shell cards | 12px |

**Borders:** 1px solid `#E5E7EB` on cards, inputs, and table rows. No coloured left-border accents — Field's site-card colour band is data, not decoration.

---

## 5. Shadows & Motion

**Shadows — floating UI only** (modals, popovers, drawers, FABs). Static cards: flat with 1px border only.

| Token | Value | Use |
|---|---|---|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04)` | Sidebar, raised card |
| `--shadow-lg` | `0 10px 40px rgba(0,0,0,0.15)` | Modals |

**Motion:** 150ms ease default. No bounce. Transitions are colour/border swaps, not translate. Sidebar drawer (mobile): 300ms transform. Spinner: 0.7s linear rotate.

**Hover / focus / active states:**
- Primary button: `#3DA8D8` → `#2986B4` (colour swap only — no opacity change, no shrink)
- Ghost on dark: transparent → `rgba(255,255,255,0.10)`
- Ghost on light: transparent → `#F9FAFB`
- Focus ring: `0 0 0 2px rgba(61,168,216,0.40)`, 2px offset — required on every input

---

## 6. Component Rules

| Component | Spec |
|---|---|
| **Cards** | bg white or ice · border 1px `#E5E7EB` · radius 8 (12 for big shells) · padding 16 small / 20–24 default · no shadow unless floating |
| **Buttons** | Primary = `--eq-sky` fill / white text · ghost = transparent / 1px `#E5E7EB` / ink text · pills for filters and status |
| **Inputs** | 1px `#D1D5DB` border · radius 6 · 40px tall (44px mobile) · focus = `--eq-deep` border + sky-20 ring |
| **Tables** | Header: `--eq-sky` fill + WHITE text (non-negotiable — "blue on white / white on blue is the cornerstone"). Zebra rows: `#F9FAFB` on even. |
| **Sidebar** | Service: 224px (collapsed 64) · Field: 220px · bg `--eq-ink` · sticky top · nav items 500wt |
| **Topbar** | Field: 48px white + bottom border · Service mobile: 56px ink fill |
| **Mobile** | Bottom nav 60px (Field) · FAB 44px circle (`--eq-ink` fill, bottom-right) |

---

## 7. Iconography

**Two parallel systems — never mixed within a single app:**

| App | System | Notes |
|---|---|---|
| EQ Service | Lucide line icons (`lucide-react`) | Stroke 2, never filled. 16px nav · 20px mobile · 28px empty-state. `currentColor`. Dark sidebar: `text-white/60` → `text-white` on active. |
| EQ Field, SKS Labour | Unicode glyphs & emoji | Rendered from OS font (`font-family: inherit`). Do not substitute Lucide. |
| Marketing, documents | Lucide-style PNG exports | No emoji in marketing or customer-facing docs. |

---

## 8. Copy & Content Rules

- **Casing:** Sentence case for UI labels ("Job plans", "Add person"). Title Case for product names only ("EQ Solves — Field"). UPPERCASE only for: form labels (Service), eyebrows, table headers, status pills.
- **Voice:** "You" to the user. Imperative for actions ("Submit request", "Add site"). Third-person for system notifications. Avoid "I" / "we" except in privacy notices.
- **Punctuation:** Em dash with spaces — Australian house style. Ellipses for loading ("Signing in…"). Bullet separator · in footers. Arrow → for forward nav.
- **Numbers:** 24-hour time. Dates: `06.04.26` internally, "Thu 17 Apr" in UI. Hours decimal (7.5). Currency AUD `$1,250.00`.

**Banned jargon → plain English alternative:**

| Banned | Use instead |
|---|---|
| canonical | "shared" / "linked across apps" / drop |
| tenant | "your business" / "your organisation" |
| entity | the specific noun — customer, site, job, staff |
| entitlement | "what's enabled" / drop |
| module | "app" / "section" |
| intake | "import" / "add data" |
| schema / RPC / JWT / RLS / SSO | never in UI — describe the action instead |

---

## 9. Hard Don'ts

- **No new brand colours.** Do not invent accent or tint colours outside the token set.
- **No recoloured logo.** Blue variant on dark → switch to white. No black variant.
- **No drop shadows on static cards.** Floating UI only.
- **No gradients as page backgrounds.** The only canonical gradient is the Service sign-in left panel: `linear-gradient(135deg, #1A1A2E 0%, #2986B4 100%)` with ~4% white-logo watermark.
- **No mixed icon systems within a single app.**
- **No coloured left-border accents on cards.**
- **No pure black** — use `--eq-ink` everywhere.
- **No stock photography, illustrations, textures, or patterns.**
- **No parallax, scroll-linked animation, confetti, or glassmorphism.**
- **No EQ tokens in SKS outputs.** Plus Jakarta Sans and `#3DA8D8` must never appear in SKS customer-facing documents.

---

## 10. Brand Preflight Check

Before presenting any EQ customer-facing or marketing output, confirm in chat:

```
Brand check: ✓ logo ✓ palette ✓ fonts ✓ flat ✓ no jargon
```

| # | Check | Pass criteria |
|---|---|---|
| 1 | **Logo** | One of the two approved R2 SVGs. Correct variant for background (blue on light, white on dark). |
| 2 | **Palette** | Only brand tokens used for fills. No invented colours. No SKS palette (`#1F335C`, `#7C77B9`). |
| 3 | **Fonts** | Plus Jakarta Sans on all web/UI. Aptos Display as print fallback. No Roboto or Calibri on EQ surfaces. |
| 4 | **Flat** | No box-shadow on static cards. No gradients except the one canonical Service sign-in exception. |
| 5 | **No jargon** | No banned words on any user-facing surface. Admin UIs included. |

---

## 11. Programmatic Source

All token values live in `eq-design-tokens` — distributed as an npm package via `github.com/eq-solutions/eq-design-tokens`.

Import into EQ apps as CSS vars, TypeScript constants, Dart constants, or Tailwind preset. **Never hard-code hex values inline** — map to tokens. CI fails if generated outputs (`tokens.css`, `tokens.ts`, `tokens.dart`, `tailwind.preset.cjs`) diverge from JSON source.

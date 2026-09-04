---
title: Claude Design — EQ Context & Working Brief
owner: Royce Milmlow
last_updated: 2026-09-04
scope: Paste-in context bundle so Claude Design produces on-brand EQ UI (A12 of the design-system consolidation)
read_priority: reference
status: live
---

# Claude Design — EQ Context & Working Brief

Canonical "start with context" brief for fine-tuning EQ UI in Claude Design. Paste the block below at the start of a session (or attach this file). Keep it in sync with the `eq-design-tokens` repo + the `design_eq_profile` memory. Token values below mirror `@eq-solutions/tokens` **v1.3.3** — re-read from `tokens/base/*.json` on `origin/main` 2026-09-04 (Shell pins v1.3.2; `@eq-solutions/ui` is v1.16.4).

> **Re-verified 2026-09-04.** The 2026-05-31 version of this brief predated Direction D (tokens v1.1, 2026-05-31): it still listed the cool-grey neutral ramp (`#E5E7EB` borders) and a three-component UI library. Both were wrong for months. Note for the next reviewer: `rules/brand-eq.md` (Design Brief v1.3) still carries that pre-Direction-D neutral ramp at its lines 53/96/123 — the tokens repo is the cross-stack source of truth per the 2026-05-31 ADR (`ops/decisions.md`), so brand-eq.md needs the same correction; flagged, not changed here.

---

```
EQ SOLUTIONS — DESIGN SYSTEM CONTEXT & WORKING BRIEF
(Paste at the start of a Claude Design session. Self-contained.)

WHO I AM / WHAT WE'RE DOING
I'm fine-tuning the UI of the EQ Solutions product suite — a family of apps for
electrical/trades field operations (Shell — incl. the EQ Ops quoting/jobs module —
Field, Service, Cards, Intake). They must read as ONE product. You're my design
collaborator: help me refine existing screens and mock new ones, always on-brand.
Reference the design tokens below by name; never invent colours, type sizes, or
spacing. If I ask for something that breaks a rule below (a gradient, a card shadow,
a new accent colour, mixed icons), say so and show me the EQ-correct alternative
instead of just complying.

RIGHT NOW I'M WORKING ON: [app + screen/component — fill in each session]

WHERE THE DESIGN SYSTEM IS AT (status, 2026-09-04)
- Foundation is shipped and canonical: one token source (@eq-solutions/tokens v1.3.3)
  compiles to CSS (vanilla vars + a Tailwind v4 @theme block + tier selectors + a
  compact-density block), TypeScript, and a Flutter/Dart package; fonts.css
  self-hosts Plus Jakarta Sans. Every app consumes the same values. The
  colours/type/spacing below are the live values — treat them as fixed.
- Shared React component library (@eq-solutions/ui v1.16.4) — LIVE today:
  Button, FormInput, StatusBadge, KindPill, Card, Modal + ConfirmDialog, Tabs,
  Toast (ToastProvider/useToast), Skeleton (+SkeletonRows/SkeletonCards), Spinner,
  Table (+TableBulkAction), DropdownMenu, EmptyState, Pagination, Tooltip,
  DateRangePicker, MultiSelect, AppShell / AppSidebar / AppRail.
  When you mock, compose from these primitives — don't invent new ones.
- Theming: a locked base layer (spacing/radii/type/neutrals/status — never
  themeable) plus tier deltas under [data-tier="standard|advanced|enterprise"].
  Shell sets data-tier from the tenant's JWT tier claim; apps stay tier-unaware.
  Only Enterprise overrides anything today: --eq-tier-accent (tenant accent,
  defaults to sky) and --eq-shadow-elevated (richer floating shadow). Brand tokens
  (sky/deep/ice/ink) never vary by tier. EQ-owned chrome (login, nav, suite frame)
  is always EQ-blue. Assume Standard tier / EQ default unless I say otherwise.

THE FEEL (one line)
Sky blue on ink, set in Plus Jakarta Sans, on an 8px grid, on warm-sand neutrals.
Flat, calm, clear. The clarity of Linear/Notion — not the complexity of legacy
trade software. Every element earns its place.

COLOUR TOKENS (the only brand colours — don't add to these)
- sky    #3DA8D8  primary: logo, headings, CTAs, icon fills
- deep   #2986B4  hover for anything blue; secondary headings (alias: skyDeep)
- ice    #EAF5FB  page/card tint; table header alt fill
- ink    #1A1A2E  body text, dark sidebar — never pure black
- grey   #666666  secondary text, labels, metadata
- white  #FFFFFF  text on blue/ink surfaces
- amber  #F59E0B  attention emphasis only (hover/deeper: amberDeep #B45309) — never as
         success/error
- slate  #94A3B8  muted text / faint metadata on light surfaces
- live   #38BDF8  the LIVE / sync indicator dot only
Accent (Direction D warmth, ~5% of any screen, brand only, never status):
  clay #A8572B · clayDeep #8A4521 (hover) · clayBg #FBF1E9 (tint surface) —
  eyebrows and section accents.
Neutrals — WARM SAND (Direction D), not cool grey:
  gray-50 #F6F3EE · 100 #EFEAE1 · 200 #E4DDD2 (default border) · 300 #D4CCBE
  (input border) · 400 #9CA3AF (text grey — stays neutral) · 500 #6B7280 · 600 #4B5563
Status (pass/fail/attention only — never as brand):
  success bg #F0FDF4 / text #15803D · warning bg #FFFBEB / text #B45309 ·
  error bg #FEF2F2 / text #B91C1C
Contrast: ink on white/ice and white on deep-blue pass AA. Sky on white is for
large text (18px+) and UI only — never body copy.

TYPOGRAPHY
Font: Plus Jakarta Sans.
Stack: 'Plus Jakarta Sans','Aptos Display','Aptos',Arial,sans-serif.
Scale (px): xs 11 · sm 12 · base 14 · md 15 · lg 18 · xl 22 · 2xl 28 · 3xl 36 · 4xl 48
Weights: 400 regular · 500 medium · 600 semibold · 700 bold · 800 black
Body: 14px / line-height 1.5 / 400 / ink. Headings: tight tracking (-0.01 to -0.02em).
Form-field labels: 12px, 600, UPPERCASE, letter-spacing 0.06em, colour grey.

SPACING / RADII / BORDERS / SHADOWS / MOTION
Spacing — 8px grid (4 = half-step): 4 8 12 16 20 24 32 40 48 64.
  Max content width 1200px, centred.
  Compact density ([data-density="compact"]): row pad 8, cell pad 6/12, card pad 12,
  body 12px — for dense tables only.
Radii — 4 chip · 6 buttons/inputs · 8 cards · 12 large shell cards · 9999 pills/avatars.
Borders — 1px solid #E4DDD2 on cards, rows, dividers; inputs 1px #D4CCBE.
  No coloured left-border accents.
Shadows — floating UI only (modals, popovers, drawers, FABs). Static cards sit FLAT
  with a 1px border.  sm: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04)  ·
  lg: 0 10px 40px rgba(0,0,0,.15)  ·  elevated = lg (Enterprise overrides it)  ·
  overlay/backdrop: rgba(26,26,46,.45) (ink at 45%).
Motion — 150ms default, ease cubic-bezier(0.4,0,0.2,1), no bounce. Animate
  colour/border/opacity, not position — the one exception is the sidebar drawer
  (300ms). Spinner: 700ms per revolution.
  Focus ring REQUIRED on every input: 0 0 0 2px rgba(61,168,216,.40), 2px offset.
  Input focus: border → deep, sky ring at 40%.

COMPONENT RULES
- Cards: white or ice, 1px #E4DDD2 border, radius 8 (12 for big shells),
  padding 16 (small) / 20–24 (default), no shadow unless floating.
- Buttons: primary = sky fill / white text, hover → deep (colour swap, no shrink).
  Ghost = transparent / 1px #E4DDD2 / ink text. Pill chips for filters + status.
- Inputs: 1px #D4CCBE border, radius 6, 40px tall (44 mobile),
  focus = deep border + sky ring.
- Tables: header row = sky fill + WHITE text. This is the cornerstone —
  blue-on-white / white-on-blue. Zebra rows gray-50 or plain white. Inline sort arrows.
- Sidebar: dark (ink), ~220px, nav items 500 weight; inside embedded module pages
  Shell collapses it to a 52px hover rail. Topbar: light, 48–56px, bottom border.
  Mobile: bottom tab bar (Field, Shell embedded), FAB 44px circle ink fill.
- Tap targets: 44px minimum on mobile — every button, toggle and row action.

PER-APP CONVENTIONS (tell me which I'm in; defaults differ)
- Shell — the hub/login + cross-app frame, and home of EQ Ops (quotes/jobs
  Kanban). React (Vite), plain CSS on tokens + @eq-solutions/ui — no Tailwind.
  Lucide icons. The most "EQ-blue" surface; chrome is always EQ.
- Service — CMMS (maintenance/defects/reports). Next.js 16 + Tailwind v4.
  Lucide line icons (stroke 2, never filled). Denser, data-heavy.
- Field — rosters/timesheets/sites/safety. Vanilla HTML/JS/CSS, no build step,
  consumes tokens.css directly. Icons are inline Lucide SVG paths (desktop nav and
  the mobile drawer since v3.5.316); a handful of legacy Unicode glyphs remain —
  do not add more.
- Cards — onboarding intake + licence wallet. Flutter (Material 3) + the Dart
  token package. Mobile-first.
- Intake — in-Shell module (import / dedup / ask). Same rules as Shell.
Icon rule: Lucide everywhere (Shell/Service/Intake via lucide-react, Field via
  inline SVG). NEVER mix icon systems within one app.

COPY & VOICE
- Sentence case for UI labels and headings ("Add person", "Job plans"). UPPERCASE
  only for field labels, eyebrows, table headers, status pills.
- Plain English. NO internal jargon in UI copy (no "canonical", "tenant", "schema",
  "entity"). Say "workspace", "site", "person", "import".
- Address the user as "you". Imperative for actions ("Submit request").
- Em dash with spaces — Australian style. Ellipsis for loading ("Signing in…").
  Arrow → for forward nav.
- 24-hour time. Dates "Thu 17 Apr". Hours decimal (7.5). Currency AUD $1,250.00.

HARD DON'TS
- No new brand colours. No recolouring the logo (blue on light, white on dark,
  never black).
- No gradients as backgrounds (single exception: the Service sign-in left panel).
- No drop shadows on static cards — floating UI only.
- No mixing icon systems in one app. No coloured left-border accents on cards.
- No pure black (use ink #1A1A2E). No cool-grey borders (#E5E7EB is retired —
  use the warm-sand ramp). No stock photos, illustrations, textures, glassmorphism,
  parallax, or confetti.
- No filler content or decorative icons. If a screen feels empty, solve it with
  layout, not clutter.

LOGO
Two variants only — blue #3DA8D8 on light, white on dark. Min size 24px,
clear space = logo height. Canonical URLs are the tokens' assets.logo.* values:
blue:  https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/eq-blue-on-transparent-cropped.svg
white: https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/eq-white-on-transparent-cropped.svg
(The older EQ_logo_blue_transparent.svg / EQ_logo_white_transparent.svg files at the
same host still resolve; prefer the token URLs.)

HOW TO WORK WITH ME
- Reference the tokens above by value; don't invent. For any new screen, show the
  token mapping you used.
- When I ask for something off-spec, push back briefly and show the EQ-correct version.
- Keep it flat, calm, confident. Sentence case, plain English, every element earning
  its place.
- If you remember one thing: clean, confident, blue — on warm sand.
```

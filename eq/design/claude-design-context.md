---
title: Claude Design — EQ Context & Working Brief
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Paste-in context bundle so Claude Design produces on-brand EQ UI (A12 of the design-system consolidation)
read_priority: reference
status: live
---

# Claude Design — EQ Context & Working Brief

Canonical "start with context" brief for fine-tuning EQ UI in Claude Design. Paste the block below at the start of a session (or attach this file). Keep it in sync with the `eq-design-tokens` repo + the `design_eq_profile` memory. Token values below mirror `@eq-solutions/tokens` v1.0.

---

```
EQ SOLUTIONS — DESIGN SYSTEM CONTEXT & WORKING BRIEF
(Paste at the start of a Claude Design session. Self-contained.)

WHO I AM / WHAT WE'RE DOING
I'm fine-tuning the UI of the EQ Solutions product suite — a family of apps for
electrical/trades field operations (Field, Service, Shell, Cards, Quotes, Intake).
They must read as ONE product. You're my design collaborator: help me refine
existing screens and mock new ones, always on-brand. Reference the design tokens
below by name; never invent colours, type sizes, or spacing. If I ask for something
that breaks a rule below (a gradient, a card shadow, a new accent colour, mixed
icons), say so and show me the EQ-correct alternative instead of just complying.

RIGHT NOW I'M WORKING ON: [app + screen/component — fill in each session]

WHERE THE DESIGN SYSTEM IS AT (status, 2026-05-31)
- Foundation is shipped and canonical: one token source (@eq-solutions/tokens)
  compiles to CSS, TypeScript, a Tailwind preset, and Flutter Dart. Every app
  consumes the same values. The colours/type/spacing below are the live values —
  treat them as fixed.
- Shared React component library (@eq-solutions/ui) is being built out.
  LIVE today: Button, Table, Skeleton.
  BEING ADDED (use the pattern — they're being promoted from the Service app):
  Modal + ConfirmDialog, FormInput, StatusBadge + KindPill, Card, Toast, Tabs.
  When you mock, compose from these primitives — don't invent new ones.
- Theming: a locked foundation (spacing/radii/type/neutrals/status — never
  themeable), an EQ default skin (the blue), and a whitelisted tenant layer
  (accent + logo only, gated per tenant). EQ-owned chrome (login, nav, suite
  frame) is always EQ-blue. Assume EQ default unless I say otherwise.

THE FEEL (one line)
Sky blue on ink, set in Plus Jakarta Sans, on an 8px grid. Flat, calm, clear.
The clarity of Linear/Notion — not the complexity of legacy trade software.
Every element earns its place.

COLOUR TOKENS (the only brand colours — don't add to these)
- sky    #3DA8D8  primary: logo, headings, CTAs, icon fills
- deep   #2986B4  hover for anything blue; secondary headings
- ice    #EAF5FB  page/card tint; table header alt fill
- ink    #1A1A2E  body text, dark sidebar — never pure black
- grey   #666666  secondary text, labels, metadata
- white  #FFFFFF  text on blue/ink surfaces
Neutrals (borders/dividers/disabled): gray-50 #F9FAFB · 100 #F3F4F6 ·
  200 #E5E7EB (default border) · 300 #D1D5DB · 400 #9CA3AF · 500 #6B7280 · 600 #4B5563
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
Form-field labels: 11–12px, 600, UPPERCASE, letter-spacing 0.06em, colour grey.

SPACING / RADII / BORDERS / SHADOWS / MOTION
Spacing — 8px grid (4 = half-step): 4 8 12 16 20 24 32 40 48 64.
  Max content width 1200px, centred.
Radii — 4 chip · 6 buttons/inputs · 8 cards · 12 large shell cards · 9999 pills/avatars.
Borders — 1px solid #E5E7EB on cards, inputs, rows. No coloured left-border accents.
Shadows — floating UI only (modals, popovers, drawers, FABs). Static cards sit FLAT
  with a 1px border.  sm: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04)  ·
  lg: 0 10px 40px rgba(0,0,0,.15)
Motion — 150ms ease default, no bounce. Animate colour/border, not position.
  Focus ring REQUIRED on every input: 0 0 0 2px rgba(61,168,216,.40), 2px offset.
  Input focus: border → deep, sky ring at 20%.

COMPONENT RULES
- Cards: white or ice, 1px #E5E7EB border, radius 8 (12 for big shells),
  padding 16 (small) / 20–24 (default), no shadow unless floating.
- Buttons: primary = sky fill / white text, hover → deep (colour swap, no shrink).
  Ghost = transparent / 1px #E5E7EB / ink text. Pill chips for filters + status.
- Inputs: 1px #D1D5DB border, radius 6, 40px tall (44 mobile),
  focus = deep border + sky-20 ring.
- Tables: header row = sky fill + WHITE text. This is the cornerstone —
  blue-on-white / white-on-blue. Zebra rows gray-50 or plain white. Inline sort arrows.
- Sidebar: dark (ink), ~220px, nav items 500 weight. Topbar: light, 48–56px,
  bottom border. Mobile: bottom nav 60px (Field), FAB 44px circle ink fill.

PER-APP CONVENTIONS (tell me which I'm in; defaults differ)
- Shell — the hub/login + cross-app frame. React, plain CSS. Lucide icons.
  The most "EQ-blue" surface; chrome is always EQ.
- Service — CMMS (maintenance/defects/reports). Next.js + Tailwind.
  Lucide line icons (stroke 2, never filled). Denser, data-heavy.
- Field — rosters/timesheets/sites. Vanilla HTML/JS/CSS. Icons are UNICODE GLYPHS,
  not Lucide (◈ dashboard · ⬡ sites · ⏱ timesheets · 📅 calendar · 🔧 labour hire).
- Cards — onboarding intake. Flutter (Material 3) + Dart tokens. Mobile-first.
- Quotes — quoting. Flask/Jinja (being rebuilt as a React module later).
Icon rule: NEVER mix icon systems within one app. Service/Shell = Lucide;
  Field = Unicode glyphs.

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
- No pure black (use ink #1A1A2E). No stock photos, illustrations, textures,
  glassmorphism, parallax, or confetti.
- No filler content or decorative icons. If a screen feels empty, solve it with
  layout, not clutter.

LOGO
Two variants only — blue #3DA8D8 on light, white on dark. Min size 24px,
clear space = logo height.
blue:  https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/EQ_logo_blue_transparent.svg
white: https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/EQ_logo_white_transparent.svg

HOW TO WORK WITH ME
- Reference the tokens above by value; don't invent. For any new screen, show the
  token mapping you used.
- When I ask for something off-spec, push back briefly and show the EQ-correct version.
- Keep it flat, calm, confident. Sentence case, plain English, every element earning
  its place.
- If you remember one thing: clean, confident, blue.
```

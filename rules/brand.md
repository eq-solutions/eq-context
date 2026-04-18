---
title: Rules — Brand
owner: Royce Milmlow
last_updated: 2026-04-18
scope: EQ, EQ Property, and SKS brand palettes, typography, and logo rules
read_priority: standard
status: live
canonical_ref: EQ Design Brief v1.3 (17 Apr 2026, supersedes v1.2)
---

# Rules — Brand

EQ Design Brief v1.3 (17 Apr 2026) is the canonical brand reference.
Two logo variants only: Blue and White. Never recolour, never gradient, never shadow.

---

## EQ Parent Brand

| Token | Hex | Usage |
|-------|-----|-------|
| EQ Sky | #3DA8D8 | Primary. Logo mark, headlines, CTAs, key UI elements |
| EQ Deep | #2986B4 | Dark accent. Hover states, borders, secondary headings |
| EQ Ice | #EAF5FB | Light tint. Backgrounds, card fills, table headers |
| EQ Ink | #1A1A2E | Primary body text |
| EQ Grey | #666666 | Secondary text, labels, captions |
| White | #FFFFFF | Backgrounds, reversed text on blue |

**EQ Sky #3DA8D8 is the parent mark colour — never recoloured for any subsidiary.**
Subsidiary palettes vary supporting colours only. The logo mark stays Sky always.

Accessibility: WCAG AA minimum on all colour combinations.

---

## EQ Property Solutions Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Property Navy | #1B2A4A | Primary / headers |
| Slate Blue | #2E4A7A | Accent / H2 |
| Property Gold | #C9A84C | Premium highlight, key figures |
| Mist | #E8EDF5 | Background tint |

---

## SKS Technologies Palette (for SKS-branded tools)

| Token | Hex |
|-------|-----|
| Dark Blue | #1F335C |
| Purple | #7C77B9 |
| Slate | #566686 |
| Light | #F0F7F7 |

---

## Typography

| Context | Typeface |
|---------|----------|
| Web / digital | Plus Jakarta Sans (Google Fonts) |
| Word / PowerPoint / print | Aptos Display |

**CSS stack:** `font-family: 'Plus Jakarta Sans', 'Aptos Display', 'Aptos', Arial, sans-serif`

**Type scale (documents):**
- Page/Section Title: Bold, 18–22pt, #3DA8D8
- Heading 1: Bold, 16pt, #3DA8D8
- Heading 2: Bold, 13pt, #2986B4
- Body: Regular, 11–12pt, #1A1A2E
- Caption/Label: Regular, 9–10pt, #666666
- Button/CTA: Bold, 11pt, White on #3DA8D8

---

## Logo Rules

- **Two approved variants only:** Blue (#3DA8D8) on white | White on blue/dark
- Never recolour, add gradients, drop shadows, outlines, or effects
- Never stretch, skew, or distort
- Never place on busy photographic backgrounds
- Always use transparent-background SVGs for production work
- Never upload transparent PNG to Claude chat — always reference R2 URL
- SVG source files held in the EQ assets project workspace (rename to .txt for upload into Claude.ai — see `knowledge/lessons.md`)

### EQ Logo Assets (R2 — eq-assets bucket, dev@eq.solutions)

Base URL: `https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/`

| File | Use |
|------|-----|
| `EQ_logo_blue_transparent.svg` | Web (primary) |
| `EQ_logo_white_transparent.svg` | Web (reversed) |
| `EQ_logo_blue_transparent.png` | Raster fallback |
| `EQ_logo_blue_transparent@2x.png` | Retina raster |
| `EQ_logo_white_transparent.png` | Raster reversed |
| `EQ_logo_white_transparent@2x.png` | Retina raster reversed |

### SKS Logo Assets (R2 — sks-assets bucket)

| File | URL |
|------|-----|
| Colour + Text | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Text_Clean.png` |
| White + Text | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_White_Text_Clean.png` |
| Colour Arrows | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Arrows_Clean.png` |
| White Arrows | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_White_Arrows_Clean.png` |

---

## Design Principles

- No gradients. No drop shadows. Linear/Notion aesthetic.
- 8px spacing grid (8, 16, 24, 32, 48, 64px)
- Max content width: 1200px centred
- Blue on white / white on blue is the visual cornerstone — avoid low-contrast combos
- Every element must earn its place — white space is intentional
- Table header rows: EQ Sky fill (#3DA8D8) with white text
- WCAG AA minimum

---

## Address Rules

- 173 Chuter Ave, Sans Souci NSW 2219 is for **legal/statutory documents only**
- Never appears in presentations, one-pagers, social assets, or marketing materials

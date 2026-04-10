---
title: Rules — Brand
owner: Royce Milmlow
last_updated: 2026-04-10
scope: EQ, EQ Property, and SKS brand palettes, typography, and logo rules
read_priority: standard
status: live
---

# Rules — Brand

---

## EQ Parent Brand

| Token | Hex | Usage |
|-------|-----|-------|
| EQ Sky Blue | #3DA8D8 | Primary. Logo mark, headlines, CTAs, key UI elements |
| EQ Deep Blue | #2986B4 | Dark accent. Hover states, borders, secondary headings |
| EQ Ice Blue | #EAF5FB | Light tint. Backgrounds, card fills, table headers |
| EQ Ink | #1A1A2E | Primary body text |
| EQ Mid Grey | #666666 | Secondary text, labels, captions |
| White | #FFFFFF | Backgrounds, reversed text on blue |
| Black | #000000 | Monochrome logo only — never as a brand colour digitally |

**EQ Sky Blue #3DA8D8 is the parent mark colour — never recoloured for any subsidiary.**
Subsidiary palettes vary supporting colours only. The logo mark stays Sky Blue always.

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
| Word / PowerPoint documents | Aptos Display |

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

- Three approved variants: Blue (#3DA8D8) on white | White on blue/dark | Black on white (print only)
- Never recolour, add gradients, drop shadows, outlines, or effects
- Never stretch, skew, or distort
- Never place on busy photographic backgrounds
- Always use transparent-background SVGs for production work
- SVG source files held in the EQ assets project workspace (rename to .txt for upload
  into Claude.ai — see `knowledge/lessons.md` for the .svg upload workaround)
- PNG raster exports exist but are legacy — SVG is source of truth

---

## Design Principles

- No gradients. No drop shadows. Linear/Notion aesthetic.
- 8px spacing grid (8, 16, 24, 32, 48, 64px)
- Max content width: 1200px centred
- Blue on white / white on blue is the visual cornerstone — avoid low-contrast combos
- Every element must earn its place — white space is intentional
- Table header rows: EQ Sky Blue fill (#3DA8D8) with white text

---

## Address Rules

- 173 Chuter Ave, Sans Souci NSW 2219 is for **legal/statutory documents only**
- Never appears in presentations, one-pagers, social assets, or marketing materials

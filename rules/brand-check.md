<!-- source: rules/brand-check.md | synced: 2026-05-21 -->

---
title: SKS Brand — Preflight Check
owner: Royce Milmlow
last_updated: 2026-05-21
scope: Mandatory checklist before presenting any SKS customer-facing output
read_priority: critical
status: live
---

# SKS Brand Preflight Check

Run this checklist on every customer-facing output (quote, MOP, scope, letter, report, presentation, email signature, HTML) **before** presenting it to Royce. If any item is ✗, fix it before showing.

The check is six lines. It exists because the brand spec in `rules/brand.md` is comprehensive but only enforced by Claude remembering to apply it. This is the second-line catch.

---

## The Six Checks

| # | Check | Pass criteria |
|---|---|---|
| 1 | **Logo source** | Image URL is one of the four R2 URLs: `SKS_Logo_Colour_Arrows_Clean.png`, `SKS_Logo_Colour_Text_Clean.png`, `SKS_Logo_White_Arrows_Clean.png`, `SKS_Logo_White_Text_Clean.png`. No local files. No alternate hosts. |
| 2 | **Logo aspect ratio** | Arrows variant width:height = 1.230:1 (2000×1626). Text variant width:height = 2.766:1 (2000×723). Height derived from width using these ratios — never set independently. |
| 3 | **Palette is correct** | Primary fills are Dark Blue `#1F335C` or White only. Purple `#7C77B9` appears only on CTAs / buttons / accent rules, never as a primary fill or background. No EQ tokens (Plus Jakarta Sans, Sky `#3DA8D8`, Ice `#EAF5FB`). |
| 4 | **Fonts are correct** | Headings: Roboto (all outputs; if recipient lacks Roboto, Word fallback to Calibri is acceptable). Body in docx: Calibri Regular (Word default, universally installed). Body in PDF/web: Roboto Regular (fonts embedded in PDFs we generate). HTML links to `sks-brand.css` and uses `var(--sks-font-heading)` / `var(--sks-font-body)`. Word docs inherit from `SKS_Master.docx` named styles (SKSTitle/SKSH1/SKSBody/etc.). |
| 5 | **Flat — no gradients, no shadows** | No `linear-gradient`, no `radial-gradient`, no `box-shadow`, no `text-shadow`, no Word drop-shadow effects, no glow on logo. SKS visual language is flat. |
| 6 | **Footer + placeholders** | Footer present with `SKS Technologies Pty Ltd \| ABN 51 168 906 956 \| 27/10 Gladstone Rd, Castle Hill NSW 2154 \| (02) 9659 9199`. Real client names (Equinix, AirTrunk, AWS, Schneider, etc.) replaced with placeholders ("Data Centre Client A", "Tier 1 Client", "Healthcare Client"). |

---

## How to run the check

Before presenting the output, write a single line in chat:

```
Brand check: ✓ logo ✓ ratio ✓ palette ✓ fonts ✓ flat ✓ footer
```

If any check fails, mark it ✗ and explain in one line what was found and fixed:

```
Brand check: ✓ logo ✓ ratio ✗ palette → had purple as primary fill, changed to Dark Blue
✓ fonts ✓ flat ✓ footer
```

This makes the brand-check status visible to Royce in one glance. It's the cheapest possible enforcement layer — a few hundred tokens — but it catches the failure modes that `rules/brand.md` and the artefacts can't.

---

## What this check does NOT replace

- `rules/brand.md` — the full spec, colours, hex codes, layout hierarchy.
- `sks-brand.css` at `pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/sks-brand.css` — the canonical stylesheet for HTML.
- `SKS_Master.docx` at `pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Master.docx` — the named-styles template for Word.
- `sks/templates.md` — document-specific structure (e.g. Quote v3 has its own section sequence).

The check is a final gate, not the spec itself. If a check fails repeatedly across sessions, that's a signal to upgrade the spec, the CSS, or the template — not just the check.

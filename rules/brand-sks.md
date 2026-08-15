---
title: SKS Brand — Rules & Assets
owner: Royce Milmlow
last_updated: 2026-08-15
scope: SKS Technologies brand specification — colours, fonts, logos, usage rules
read_priority: critical
status: live
---

# SKS Brand Rules

Canonical brand spec for all SKS Technologies outputs (quotes, MOPs, reports, presentations, HTML, PDF). Reference Source: SKS Brand Style Guide v1.0 (Apr 2025).

---

## 1. Logo Files — R2 CDN (definitive source)

Base URL: `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/`

| File | Use case |
|---|---|
| `SKS_Logo_Colour_Arrows_Clean.png` | Primary — arrows + text, on white/light backgrounds |
| `SKS_Logo_Colour_Text_Clean.png` | Wide text-only variant, on white/light backgrounds |
| `SKS_Logo_White_Arrows_Clean.png` | Arrows + text, on dark backgrounds |
| `SKS_Logo_White_Text_Clean.png` | Wide text-only variant, on dark backgrounds |

**Never process from local source files. Always pull from R2.**

### Logo dimensions (VERIFIED 2026-05-19 from R2)

| Variant | Native size (px) | Aspect ratio | Derive height from |
|---|---|---|---|
| **Arrows** (Colour + White) | 2000 × 1626 | **1.230:1** | `height = width / 1.230` |
| **Text** (Colour + White) | 2000 × 723 | **2.766:1** | `height = width / 2.766` |

**Critical:** Text variant is *wide and short*, not tall. Common bug: assuming the Text variant has a similar ratio to Arrows — it does not. If unsure, fetch the file and check actual dimensions with PIL before placing.

**Rules:**
- Never alter aspect ratio. Never set width and height independently.
- Always derive height from the chosen width using the correct ratio for the variant.
- Applies to all document types (docx, pptx, HTML, PDF, email signatures).

### Logo backgrounds

- White logo variants → dark backgrounds (e.g. Dark Blue `#203060`).
- Colour logo variants → white or light backgrounds (e.g. Light Blue `#F0F7F7`).
- On busy backgrounds (e.g. photography), use the **white backing frame** pattern from the Style Guide (logo in a white box, placed in top-left/right or bottom-left/right corner of the document). Frame the primary logo rather than dropping to the secondary.

### Logo — do not

- Add or alter colours.
- Add extra elements (badges, taglines, decorations).
- Disproportionately size (squash or stretch).
- Add a coloured background fill directly behind the logo (use a white frame instead).
- Rotate.
- Place directly on busy backgrounds without a frame.

---

## 2. Colour Palette

### Primary

| Name | Hex | RGB | CMYK | PMS |
|---|---|---|---|---|
| Dark Blue | `#203060` | 32, 48, 96 | ⚠ needs print source | ⚠ needs print source |
| White | `#FFFFFF` | 255, 255, 255 | — | — |
| Purple (accent) | `#7C77B9` | 124, 119, 185 | 56, 55, 0, 0 | PMS 272C |

> **Dark Blue corrected 2026-08-15 — screen values only.** The hex was
> `#1F335C` here and had drifted; the live canonical value is `#203060`,
> re-verified this date by direct query of
> `organisations.branding.palette.primary` on eq-canonical (`jvkn…`). The code
> was fixed repo-wide weeks earlier (eq-shell PR #1173, eq-field email
> templates) — **this spec, the thing that tells you what to build, was not.**
> That is failure F14 exactly, and it is why this file now carries a review
> clock.
>
> Hex and RGB are safe: RGB is a mechanical conversion of the hex. **CMYK
> `98, 85, 37, 28` and PMS 2955 are not.** They were specified against
> `#1F335C` and cannot be recalculated from a new hex — press profile and paper
> stock decide them. They are marked ⚠ rather than silently carried over
> (which would pair print values with a colour they were never measured for) or
> invented. **Get them from the SKS brand/print source before any printed
> collateral goes out.** Screen output is unaffected.
>
> Two other values in this file were derived from the old hex and have the same
> problem: Slate Blue `#34486C` (90% tint) and Dusty Blue `#566686` (75% tint).
> Recomputed from `#203060` they would be ≈`#364670` and ≈`#586488`, but they
> are left as-is pending the same source — a guessed tint is still a guess.
> Charcoal `#373D58` and Onyx `#3E3E48` are labelled as shades of Dark Blue but
> are not arithmetically derivable from either hex, so they appear to be
> independent brand colours and are untouched.
>
> **Unresolved — the purple. Royce's call, deliberately not made here.**
> Canonical carries `palette.deep = 8070C0` for this tenant while this file
> documents the accent purple as `#7C77B9`. Two readings, and the evidence
> genuinely splits:
>
> - *It is drift.* The key names are EQ's schema, and for the EQ tenant `deep`
>   (`2986B4`) is a darker shade of `primary` (`3DA8D8`) — same hue. For SKS,
>   `deep` (`8070C0`) is **purple**, not a darker navy, so structurally it is
>   filling the accent-colour slot. On that reading `8070C0` is live and
>   `#7C77B9` is stale, same story as Dark Blue above.
> - *It is not.* The 2026-07-30 correction — the one that verified `primary`
>   against live and caught the `#1F335C` drift — states the purple as
>   `#7C77B9` in the same breath. A human looked at both and changed only one.
>   `#7C77B9` is also paired with PMS 272C, a real print spec.
>
> Not changed, because a wrong purple ships into customer-facing collateral and
> the cost of guessing exceeds the cost of asking. Resolve it by checking the
> SKS brand source, not by inference from key names.

**Usage:** Dark Blue and White are the foundation, alternating for contrast. Purple is an accent only — interactive elements (buttons, CTAs), not a primary fill.

### Secondary (use sparingly, supporting role)

| Name | Hex | Notes |
|---|---|---|
| Light Blue | `#F0F7F7` | Background tint for sections / table rows |
| Slate Blue (90% tint of Dark Blue) | `#34486C` | Subheading / body text on light backgrounds |
| Dusty Blue (75% tint of Dark Blue) | `#566686` | Muted text, secondary captions |
| Charcoal (25% shade) | `#373D58` | — |
| Onyx (70% shade) | `#3E3E48` | — |
| Black | `#000000` | Page numbers, footer rules |
| Grey | `#808285` | Dividers, icon strokes |
| Indigenous Purple | `#573B8F` | **Only** for applications directly tied to that brand |

---

## 3. Typography

| Use | Font | Weight |
|---|---|---|
| Headings (all outputs) | Roboto | Black |
| Subheaders (all outputs) | Roboto | Bold |
| Body text — PDF and web | Roboto | Regular |
| Body text — Word (.docx) | Calibri | Regular |
| Logo font | Source Sans Pro | — |

**Why Calibri for docx body** (decided 2026-05-21): editable .docx files are sent to recipients (Equinix, Schneider, Erilyan) whose workstations may not have Roboto installed. Word silently substitutes missing fonts and the layout drifts. Calibri is the Word default since Office 2007 and is universally available on Win/Mac Office — zero install friction, zero layout risk. PDFs we generate ourselves embed Roboto, so the risk doesn't apply there. Roboto headings in docx accept the same fallback risk, but heading text is short enough that substitution doesn't reflow layout meaningfully.

**Substitution policy:**
- Web/HTML: load Roboto from Adobe Fonts / Google Fonts. If not feasible, fall back to **Plus Jakarta Sans** (EQ standard) only for internal EQ work, never for SKS customer-facing.
- Never substitute the logo font — it's baked into the logo file.

---

## 4. Primary Brand Element — The Arrows

The double-chevron arrows from the logo are a brand asset in their own right. Use only in **Dark Blue** or **Light Blue**.

### Arrow rules

- Always point right (it's a directional asset symbolising forward movement).
- Reversed direction (pointing left) is **only** permitted for the Solid Overlay and Split Overlay treatments on photographic backgrounds — never for floating or corner image arrows.
- Never colour purple, grey, or any non-brand colour.
- Never change the internal spacing between the two chevrons.
- Never display a single arrow.
- Never convert to outlines.
- Never rotate.

### Arrow asset variants

| Variant | Use case | Fill |
|---|---|---|
| Solid Overlay Arrow | Large background element with photo, blending-mode overlay (50–85% opacity) | Solid fill, blend = Overlay |
| Split Overlay Arrow | Two arrows with central split, layered effect | 100% fill + 50–85% opacity overlay |
| Floating Image Arrow | Image-filled arrow, stretches horizontally (x-axis only) | Image fill only — never solid colour |
| Corner Image Arrow | Image-filled arrow tucked into a corner, straight edge aligned to document edge | Image fill only |

---

## 5. Imagery Style

- Blue-toned / blue-highlighted photography to align with primary palette.
- Subjects: technology (devices, screens, coding), connectivity (satellites, networks, fibre), infrastructure (cityscapes, server stacks, data centres), workspaces (modern office, teams), energy and movement (time-lapse, data streams, abstract motion).
- Avoid: warm-toned imagery, stock-photo clichés (handshakes, generic office), human-only imagery without a technology context.

---

## 6. Icons

SKS maintains an icon library specific to its industries. Request the compressed folder from internal marketing — icons must come from this set, not third-party libraries (Lucide, Font Awesome, etc.) for customer-facing collateral. Internal tools may use Lucide where workflow demands.

---

## 7. Document Hierarchy — Default Layout

For Word / PDF customer-facing outputs:

| Element | Spec |
|---|---|
| Page size | US Letter (12240 × 15840 DXA) or A4 |
| Margins | 1 inch / 1440 DXA all sides |
| Header logo | Top-right, Colour Arrows variant, ~160–220 px wide |
| Title | Roboto Black, Dark Blue `#203060`, 18 pt |
| Subtitle / strap | Roboto Bold, Slate Blue `#34486C`, 11 pt, with 1.5pt Purple `#7C77B9` underline rule |
| Body | Calibri Regular (docx) or Roboto Regular (PDF), Dark Blue `#203060`, 11 pt |
| Table headers | Dark Blue `#203060` fill, White text, bold |
| Table body rows | Alternating White and Light Blue `#F0F7F7` |
| Table borders | `#CCCCCC` thin |
| Footer | Centred, Slate Blue `#34486C`, 8 pt, with Dark Blue top rule |
| Footer content | `SKS Technologies Pty Ltd  \|  ABN 51 168 906 956  \|  27/10 Gladstone Rd, Castle Hill NSW 2154  \|  (02) 9659 9199` |

**Preflight:** Before presenting any customer-facing output, run the checklist in [rules/brand-check.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/rules/brand-check.md).

---

## 8. Common Mistakes — Caught in Past Sessions

- **Wrong logo aspect ratio for Text variant** (memory had 1456 × 812 / 1.793:1, actual is 2000 × 723 / 2.766:1). Always verify file dimensions, never trust prior numbers. Fixed 2026-05-19.
- Using Purple as a primary fill instead of an accent — Purple is for CTAs/buttons only.
- Using gradients or drop shadows — neither is in the SKS visual language. Flat colour only.
- Mixing EQ design tokens (Plus Jakarta Sans, Sky `#3DA8D8`) into SKS customer-facing documents. EQ ≠ SKS.
- Placing the logo directly on a busy background without a white frame.

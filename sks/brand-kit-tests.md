---
title: SKS Brand Kit — Test Prompts
owner: Royce Milmlow
last_updated: 2026-05-21
scope: Canonical regression-test prompts for the SKS brand kit (sks-brand.css + SKS_Master.docx + rules/brand-check.md). Re-run any time brand drift is suspected, or after any change to the three artefacts.
read_priority: reference
status: live
---

# SKS Brand Kit — Test Prompts

Two paste-ready prompts that exercise the SKS brand kit end-to-end. Both are designed to run in a **fresh** Claude session (Chat, Cowork, or a new Claude Code window in a non-brand-kit folder) — never in a session that's already loaded with brand-kit context, because the in-session priors bias the result.

| Prompt | Tests | Pass criteria |
|---|---|---|
| 1. Happy path | All three artefacts produce a correct HTML page + Word quote; brand-check fires before each | Brand-check line appears once per deliverable; HTML uses var(--sks-\*) + R2 CSS link + Roboto from Google Fonts; docx opens in Word with Roboto headings, Calibri body, ABN footer |
| 2. Failure modes | Each of the 6 brand-check rules catches a deliberate violation | All 6 violations produce ✗ on the matching check item; no false negatives (all-✓ on a violating snippet) |

Run Prompt 1 first. If it passes, run Prompt 2. If Prompt 1 fails, fix what's broken before running Prompt 2 (otherwise failure-mode results may conflate happy-path bugs with enforcement bugs).

The naturalistic counterpart to these is the "monitor first 5 SKS outputs" item in [sks/pending.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks/pending.md) — watch organic SKS quote/MOP/letter sessions for the brand-check line. These prompts are the *active* test; the pending-item watch is the *passive* test. Both have a role.

---

## Prompt 1 — Happy-path test

Paste this into a fresh session.

````
SKS session — brand kit deployment validation.

Context: a brand kit was deployed on 2026-05-21. Three artefacts now own SKS brand enforcement:
- sks-brand.css       https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/sks-brand.css
- SKS_Master.docx     https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Master.docx
- rules/brand-check.md  https://raw.githubusercontent.com/eq-solutions/eq-context/main/rules/brand-check.md

Task: produce two small test deliverables that exercise all three artefacts end-to-end.

DELIVERABLE 1 — SKS HTML page
- Title "SKS Brand Kit Test — 2026-05-21"
- Heading "Test successful", a 3-column 2-row sample table, a paragraph in body style
- Footer: SKS Technologies Pty Ltd | ABN 51 168 906 956 | 27/10 Gladstone Rd, Castle Hill NSW 2154 | (02) 9659 9199
- MUST link to the R2 sks-brand.css above
- MUST include Google Fonts Roboto link (preconnect + stylesheet for weights 400/700/900)
- MUST use var(--sks-*) tokens — no inline hex codes
- Save to a file if you have filesystem access, else present as a code block I can copy

DELIVERABLE 2 — SKS Word quote
- Header: QUOTATION banner (Dark Blue), white SKS Text logo top-right
- Quote ref: TEST-001, date: 2026-05-21, attention: Test Recipient
- Scope (2 lines): "Test quote to validate brand kit deployment. Single line item only."
- Pricing: 1 line "Test labour @ $1,000 ex GST" + Subtotal / GST / TOTAL
- 3 standard exclusions of your pick (see sks/templates.md if you have substrate access)
- Acceptance block
- MUST be built from SKS_Master.docx as the template — download from R2, use the SKSTitle / SKSH1 / SKSH2 / SKSBody named styles
- Save the resulting .docx; tell me the file path

BRAND CHECK — for EACH deliverable
- Before presenting, fetch rules/brand-check.md and apply the 6 checks
- Output the single-line "Brand check: ✓ logo ✓ ratio ✓ palette ✓ fonts ✓ flat ✓ footer"
- For each ✓, give one-line evidence (e.g. "✓ palette — only var(--sks-dark-blue) and var(--sks-white) used as fills")

If anything blocks you (R2 returns non-200, the docx template won't open, substrate URLs fail, docx skill unavailable) — STOP and tell me. Don't guess values.

I'll judge pass/fail by: HTML renders in browser with Roboto and SKS colours; docx opens in Word with Roboto headings + Calibri body + correct footer with ABN; brand-check line appears once before each deliverable; no EQ tokens, no purple fills, no gradients/shadows anywhere.
````

### What "pass" looks like

- The reply contains exactly two `Brand check: ✓ ...` lines (one per deliverable) — proves the discipline fired.
- The HTML you receive has `<link rel="stylesheet" href="https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/sks-brand.css">` and a Google Fonts Roboto link, uses `var(--sks-dark-blue)` / `var(--sks-purple)` etc., never inline hex codes. Open it in a browser — fonts should render as Roboto, colours should match the spec.
- The `.docx` opens in Word. Heading text renders in Roboto (or Calibri fallback if the recipient lacks Roboto — that's the policy). Body renders in Calibri. Footer shows `ABN 51 168 906 956`.
- No EQ tokens (no Plus Jakarta Sans, no `#3DA8D8`), no purple as a primary fill, no gradients, no shadows.

### What "fail" looks like

- No brand-check line → discipline didn't fire; substrate hook is broken or the session ignored it.
- HTML inlines hex codes → the session didn't actually use the CSS, just generated styles from memory.
- docx body in Arial or Times New Roman → didn't use SKS_Master.docx as the template.
- Footer missing ABN → either fetched a cached pre-2026-05-21 copy or skipped the brand-check.

---

## Prompt 2 — Failure-mode test

Paste this into the same session (or another fresh one) **after Prompt 1 has passed**.

````
SKS session — brand-check enforcement test.

Context: rules/brand-check.md (https://raw.githubusercontent.com/eq-solutions/eq-context/main/rules/brand-check.md) is the 6-line preflight that catches SKS brand violations. This test deliberately introduces one violation at a time to confirm each check fires.

Task: produce 6 tiny HTML snippets (a single paragraph each is fine). Snippet N must violate ONLY brand-check item N and pass the other 5. After each, run brand-check and the result MUST mark item N as ✗ with one-line evidence.

THE SIX VIOLATIONS:

1. Logo source — <img src="/local/sks-logo.png"> (local path; should be an R2 URL)
2. Logo aspect ratio — <img src="https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Text_Clean.png" width="200" height="200"> (Text variant is 2.766:1 so width=200 should give height≈72, not 200)
3. Palette — background: #7C77B9 on a table header (purple is accent-only, never primary fill)
4. Fonts — font-family: 'Plus Jakarta Sans' applied to body text (EQ token leak)
5. Flat — box-shadow: 0 2px 6px rgba(0,0,0,0.2) on a card or logo
6. Footer + placeholders — footer reading "SKS Technologies Pty Ltd | 27/10 Gladstone Rd, Castle Hill NSW 2154 | (02) 9659 9199" (ABN missing) OR a real client name in the output (e.g. "Equinix SY5", "AirTrunk SYD3")

For each snippet:
- Show the HTML (≤10 lines)
- Run brand-check
- Brand-check line example: "Brand check: ✓ logo ✓ ratio ✗ palette → purple #7C77B9 used as table-header fill, must be Dark Blue ✓ fonts ✓ flat ✓ footer"
- The ✗ must land on item N and ONLY item N — the other 5 items in the same snippet should be ✓

PASS: all 6 violations caught (one ✗ per snippet, on the right item).
FAIL: any violation passes with all ✓ — that's a false negative and means brand-check has a gap.

If you find a false negative, report which check failed and what evidence brand-check should have used to catch it — we'll fix the check.
````

### What "pass" looks like

- 6 brand-check lines, each with exactly one ✗ on the matching item, the other 5 ✓.
- Evidence after each ✗ is concrete (cites the actual offending value or path, not generic).

### What "fail" looks like

- Any snippet returns all 6 ✓ — that's a false negative. The check missed a real violation. Capture the gap, fix the check.
- A snippet returns ✗ on the wrong item — the check fired but for the wrong reason. Less serious than a false negative but means the evidence text is misleading.

### Predicted weak spots (grade against these)

- **Check #2 (aspect ratio)** — hardest to enforce mechanically. Requires *computing* the width:height ratio against the variant constants (1.230:1 for Arrows, 2.766:1 for Text), not just scanning for forbidden strings. If a 200×200 Text variant passes, that's the top fix priority.
- **Check #6 (footer + placeholders)** — two failure modes folded into one check (missing ABN; real client name). If catching one and missing the other becomes a pattern, split into 6a and 6b.

---

## When to re-run

- After any edit to `sks-brand.css`, `SKS_Master.docx`, or `rules/brand-check.md`.
- After any edit to `rules/brand-sks.md` §3 (Typography) or §7 (Document Hierarchy) — those drive the artefacts.
- After a Claude tool upgrade (new Chat version, new Cowork plugin, etc.) — to confirm the bootstrap still works.
- Quarterly, as a regression check, even with no known changes — silent drift in dependency behaviour is real.

If a test fails and the fix is a substrate edit, also add to [ops/decisions.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/ops/decisions.md) so future-you knows *why* the change was made, not just what.

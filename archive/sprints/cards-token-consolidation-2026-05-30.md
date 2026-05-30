---
title: Cards Token Consolidation — Decision Prep
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Investigate EqSpacing/EqSpacingTokens duplication in eq-cards; propose consolidation paths + recommendation
read_priority: reference
status: live
---

## Summary

eq-cards carries two parallel Dart token systems in `lib/core/theme/`. One is hand-written and actively used across ~34 files. The other is a vendored copy of the generated `tokens.dart` from `eq-design-tokens`, but uses renamed class names (`EqSpacingTokens`, `EqTypographyTokens`) to avoid a compile-time duplicate-class error. The vendored copy is currently **unused** in the app — it sits as dead code.

The good news: the naming collision problem is already partially self-inflicted. The `tokens.dart` generated file uses `EqSpacing` and `EqTypography` as class names (identical to the hand-written ones). The vendored-in copy renamed them to `EqSpacingTokens`/`EqTypographyTokens` as a workaround, but then was never wired up. That leaves the app carrying dead code and the risk of divergence over time.

---

## 1. Where Each System Is Defined

### System A — Hand-written (USED)

| File | Class | What it exposes |
|---|---|---|
| `lib/core/theme/eq_spacing.dart` | `EqSpacing` (abstract) | `xs=4, sm=8, md=16, lg=24, xl=32, xxl=48` — 6 named semantic aliases |
| `lib/core/theme/eq_typography.dart` | `EqTypography` (abstract) | `fontFamily`, 5 composed `TextStyle` constants: `headingXL/L/M`, `bodyL/M`, `label` — each includes `fontSize`, `fontWeight`, `color`, and `height` where relevant |
| `lib/core/theme/eq_colours.dart` | `EqColours` | Brand + status colour palette |
| `lib/core/theme/eq_theme.dart` | `EqTheme` | Flutter `ThemeData` wiring, references `EqTypography` and `EqColours` |

### System B — Vendored Generated (UNUSED)

| File | Class | What it exposes |
|---|---|---|
| `lib/core/theme/eq_tokens.dart` | `EqSpacingTokens` | Numeric scale: `s1=4, s2=8, s3=12, s4=16, s5=20, s6=24, s8=32, s10=40, s12=48, s16=64` — 10 positional values |
| `lib/core/theme/eq_tokens.dart` | `EqTypographyTokens` | `fontFamily`, 9 raw `double` font-size steps (`xs–xl4`), 5 `FontWeight` constants (`regular/medium/semi/bold/black`). No composed `TextStyle` objects. |
| `lib/core/theme/eq_tokens.dart` | `EqColors` | Same brand + neutral + status palette (note: `EqColors` vs `EqColours` — different spelling) |
| `lib/core/theme/eq_tokens.dart` | `EqRadius` | Semantic radius constants |

The `eq_tokens.dart` file was copied from `C:\Projects\eq-design-tokens\tokens.dart` and its class names manually renamed from `EqSpacing`→`EqSpacingTokens` and `EqTypography`→`EqTypographyTokens` to avoid the duplicate-class compile error.

### Upstream Generator

`C:\Projects\eq-design-tokens\build.mjs` emits `tokens.dart` (the source). The Dart output classes are named `EqSpacing`, `EqColors`, `EqRadius`, `EqTypography` — these collide with the hand-written `EqSpacing`, `EqTypography`, `EqColours`. No pubspec.yaml in `eq-design-tokens`; it is not yet a proper Flutter package dependency. eq-cards has **no `eq-design-tokens` dependency** in its `pubspec.yaml` — the vendored file is a manual file copy only.

---

## 2. Usage Count and Representative Callsites

The import search (`import.*eq_spacing|eq_typography|eq_tokens`) found **34 files** in `lib/`. The grep over actual token symbols found:

- `EqSpacing.*` references: **335 occurrences** across **29 files**
- `EqTypography.*` references: spread across the same ~29 files (combined with spacing counts above)
- `EqSpacingTokens` / `EqTypographyTokens`: **0 usages** outside their own definition file — confirmed dead code

Representative callsite files:
- `lib/core/theme/eq_theme.dart` — wires `EqTypography` named styles into `ThemeData.textTheme`
- `lib/core/widgets/eq_button.dart`, `eq_card.dart`, `eq_text_field.dart`, `eq_app_bar.dart` — core widget library
- `lib/features/licences/presentation/screens/licences_list_screen.dart` — 53 references (heaviest consumer)
- `lib/features/licences/presentation/screens/licence_detail_screen.dart` — 31 references
- `lib/features/settings/presentation/screens/settings_screen.dart` — 35 references
- `lib/features/licences/presentation/widgets/licence_card.dart` — 19 references

---

## 3. Value Divergence Analysis

This is the critical question. The two systems expose **different APIs** and **partially different values**.

### Spacing

| Token name (hand-written) | Value | Equivalent in generated (`EqSpacingTokens`) | Match? |
|---|---|---|---|
| `EqSpacing.xs` | 4.0 | `EqSpacingTokens.s1 = 4` | YES (same value, different name) |
| `EqSpacing.sm` | 8.0 | `EqSpacingTokens.s2 = 8` | YES |
| `EqSpacing.md` | 16.0 | `EqSpacingTokens.s4 = 16` | YES |
| `EqSpacing.lg` | 24.0 | `EqSpacingTokens.s6 = 24` | YES |
| `EqSpacing.xl` | 32.0 | `EqSpacingTokens.s8 = 32` | YES |
| `EqSpacing.xxl` | 48.0 | `EqSpacingTokens.s12 = 48` | YES (same value, different name) |
| *(no equivalent)* | — | `EqSpacingTokens.s3 = 12` | NEW (no hand-written equivalent) |
| *(no equivalent)* | — | `EqSpacingTokens.s5 = 20` | NEW |
| *(no equivalent)* | — | `EqSpacingTokens.s10 = 40` | NEW |
| *(no equivalent)* | — | `EqSpacingTokens.s16 = 64` | NEW |

**Spacing verdict: values are identical; naming convention differs (semantic aliases vs. numeric positional scale). No visual change risk on direct value mapping.**

Note: `EqSpacing.xxl` is used in 2 files (`certificates_list_screen.dart`, `licences_list_screen.dart`). The generated scale has `s12=48` as the match — this would need a mapping or alias.

### Typography

This is where the systems genuinely diverge in **kind**, not just naming.

| Dimension | Hand-written `EqTypography` | Generated `EqTypographyTokens` |
|---|---|---|
| API shape | Composed `TextStyle` objects with `fontSize + fontWeight + color + height` baked in | Raw `double` font-size primitives + `FontWeight` constants — no `TextStyle`, no `color` |
| Font sizes used | `headingXL=32, headingL=24, headingM=20, bodyL=17, bodyM=15, label=13` | `xs=11, sm=12, base=14, md=15, lg=18, xl=22, xl2=28, xl3=36, xl4=48` |
| Color baked in? | YES — `EqColours.ink` on headings/body, `EqColours.grey` on label | NO — no colors; raw primitives only |
| `height` baked in? | YES — `bodyL/M` have `height: 1.4` | NO |
| Font size overlap | `bodyM=15` maps to `md=15` | `headingM=20` has no equivalent (between `lg=18` and `xl=22`) |
| `headingXL=32` | Hand-written | Generated has `xl3=36` and `xl2=28` — 32 is absent |
| `headingL=24` | Hand-written | Generated has no 24 step |
| `bodyL=17` | Hand-written | Generated has no 17 step |
| `label=13` | Hand-written (13px) | Generated has no 13 step (`sm=12`, `base=14`) |

**Typography verdict: genuine divergence. The generated tokens are font-size primitives; the hand-written ones are fully-composed `TextStyle` objects. You cannot rename-swap without losing baked-in colors and line heights. This is NOT a safe rename — it would require reconstructing `TextStyle` compositions from the primitive scale. Also, font-size values do not map 1:1 (headingXL=32 vs. nearest xl2=28/xl3=36).**

### Colors

Both systems carry identical brand colors (same hex values). Naming differs: `EqColours` (hand-written, used) vs. `EqColors` (generated, unused). Values match.

---

## 4. Generated Dart Output Format

The `build.mjs` Dart emitter (section 7, lines 519–603) generates:

```dart
class EqSpacing {
  EqSpacing._();
  static const double s1 = 4;   // positional numeric names
  ...
}

class EqTypography {
  EqTypography._();
  static const String fontFamily = 'PlusJakartaSans';
  static const double xs = 11;  // raw font-size doubles
  ...
  static const FontWeight regular = FontWeight.w400;
}
```

Key facts for decision-making:
- The emitter names the classes `EqSpacing` and `EqTypography` — the **same** as the hand-written classes. Any future fresh import of the generated file will compile-error without intervention.
- The emitter is fully under EQ control (`build.mjs` is in `C:\Projects\eq-design-tokens`). Class names, structure, and constants can be changed by editing the build script.
- There is no pubspec.yaml in `eq-design-tokens` — it cannot be added as a Flutter git dependency today. Vendoring via file copy is the only current mechanism.
- The `tokens.dart` output already has `EqRadius` which does not exist in the hand-written system at all — this is a net-new capability the generated system adds.

---

## 5. Consolidation Paths

### Path A — Alias Bridge (low risk, medium effort, temporary)

**Approach:** Keep the hand-written `EqSpacing`/`EqTypography` untouched. In `eq_tokens.dart`, delete `EqSpacingTokens`/`EqTypographyTokens` (dead code) and instead add `typedef` aliases or delegation constants that map the generated names to the hand-written ones — or vice-versa.

Concretely: rename `EqSpacingTokens` back to `EqSpacing` would cause a compile error. Instead, make the generated file a **thin re-export** — delete the current `eq_tokens.dart` content, and add:

```dart
// In eq_tokens.dart — bridge only
export 'eq_spacing.dart';    // re-exports EqSpacing
export 'eq_typography.dart'; // re-exports EqTypography
export 'eq_colours.dart';    // re-exports EqColours
// Plus EqRadius (new, no conflict) and any future generated primitives
class EqRadius { ... }  // from generated tokens, safe to add
```

This removes the dead code risk, makes `eq_tokens.dart` a single import barrel for the rest of the app, and defers the deeper API question.

**Tradeoffs:**
- PRO: Zero visual change. Zero callsite churn. Compiles immediately.
- PRO: Removes `EqSpacingTokens`/`EqTypographyTokens` dead code.
- PRO: Adds `EqRadius` as a usable constant (currently absent from hand-written system).
- CON: Hand-written classes remain the source of truth — still not driven by the token JSON.
- CON: Does not solve the re-vendor problem — next time you copy `tokens.dart` you'll still get naming collisions unless you edit `build.mjs`.

**Effort:** ~1 hour. Safe to do standalone before E1.

---

### Path B — Codemod Replace (medium risk, medium-high effort, permanent)

**Approach:** Update `build.mjs` to emit the generated Dart file with the hand-written naming convention (semantic aliases for spacing, composed `TextStyle` objects for typography). Then codemod the 34 consumer files from `EqSpacing.xs/sm/md/lg/xl/xxl` to the generated `s1/s2/s4/s6/s8/s12` names, and rebuild `EqTypography` inside `tokens.dart` as composed styles.

This is harder than it looks because:
1. The spacing codemod itself is mechanical — 6 aliases → 6 positional names, 335 sites. An IDE find-replace handles this in 10 minutes.
2. The typography codemod is non-trivial: the generated system has no `bodyL`, `bodyM`, `headingXL` etc. You would need to decide on font sizes first (e.g. is `headingM` 20px or 18px? — the generated scale has no 20px step).
3. The `EqTypography.headingXL/L/M` composed styles also bake in `EqColours.ink`. The generated system has no color concept. You must either bake it in during generation or reconstruct it manually after the rename.

**Tradeoffs:**
- PRO: Single source of truth after completion. Future `npm run build` → copy `tokens.dart` → done.
- PRO: Eliminates all hand-written token files.
- CON: Font sizes may visually change if the mapping is not exact (e.g. bodyL=17 has no generated equivalent; nearest is md=15 or lg=18 — both are wrong).
- CON: Typography requires schema design decisions, not just a rename. Not safe to batch.
- CON: 335 callsites across 34 files — high PR noise, merge conflict risk with any parallel work.

**Effort:** Spacing codemod is ~2 hours. Typography rebuild requires a design decision + ~1 day. Total: 1–2 days. Should not be done standalone before E1 — too much churn for a mid-sprint.

---

### Path C — Regenerate with Cards-Compatible Output (low risk long-term, but requires build.mjs changes)

**Approach:** Edit `build.mjs`'s `buildDart()` function to emit class names and API shape that exactly match what Cards needs — specifically: use semantic alias names (`xs, sm, md, lg, xl, xxl`) for spacing and emit composed `TextStyle` constants for typography. The JSON token values drive the numbers; the emitter drives the API shape.

This means `tokens.dart` would emit:

```dart
class EqSpacing {
  static const double xs  = 4;   // spacing.1
  static const double sm  = 8;   // spacing.2
  static const double md  = 16;  // spacing.4
  static const double lg  = 24;  // spacing.6
  static const double xl  = 32;  // spacing.8
  static const double xxl = 48;  // spacing.12
}
```

And for typography, `buildDart()` would need access to the color tokens to emit `TextStyle` objects, which crosses a design concern into the token emitter — this is doable but requires intentional decisions (what does `headingXL` mean in token JSON terms?).

**Tradeoffs:**
- PRO: True single source of truth. Future regeneration is drop-in compatible with Cards.
- PRO: Spacing path is fully safe — values unchanged, names unchanged after one-time alignment.
- PRO: Adds any new tokens (radius, motion, focus) automatically on next build.
- CON: Typography emitter change requires adding semantic composition logic (headings, body, label) to `build.mjs` — non-trivial, and introduces Flutter-specific concerns into the token build.
- CON: Requires agreement on what "headingM" means at the token-JSON level. Currently the JSON has no semantic labels — only a numeric scale.
- CON: Spacing emitter change is easy but breaks the positional naming that other non-Flutter consumers (TS, CSS) rely on for their own conventions. Would need to emit both shapes or make the Flutter emitter a separate section.

**Effort:** Spacing regeneration change ~2 hours. Typography semantic layer in JSON + emitter is a 0.5-1 day design task. Best scoped as part of E1 or a dedicated "EQ Design Tokens v2" epic.

---

## 6. Recommendation

**Do Path A now (standalone), plan Path C for E1.**

### Immediate (standalone, ~1 hour):
1. Delete the body of `lib/core/theme/eq_tokens.dart`.
2. Replace it with a barrel export of the three hand-written files plus the `EqRadius` class (copied from the generated output — no naming conflict, adds genuine value).
3. This removes the dead `EqSpacingTokens`/`EqTypographyTokens` classes that are the root cause of the "re-vendor would dup-class compile-error" blocker.
4. Result: the sprint blocker is cleared, no callsite changes needed, no visual risk.

### As part of E1 Cards worker-first rebuild:
Bundle Path C's spacing half (emit semantic aliases from JSON → align `build.mjs` Dart output). This is safe because spacing values are identical — it is purely a naming alignment. Typography is a bigger design decision (semantic labels in JSON, composed styles in emitter) and should be scoped as a separate token-system task, not bundled into the E1 rebuild itself unless E1 is explicitly rebuilding the widget layer from scratch.

### Do NOT do Path B standalone:
The 335-site codemod + font-size decision + typography reconstruction is too much churn for a pre-E1 cleanup. It would conflict with any parallel feature work and introduces visual-change risk on the typography side.

---

## 7. Risk Flags

| Risk | Severity | Notes |
|---|---|---|
| `EqSpacing.xxl` (48px) has no direct named alias in generated scale | LOW | `s12=48` is the correct mapping. Only 2 callsites. |
| Typography font sizes diverge (e.g. `headingXL=32` vs. nearest `xl2=28`/`xl3=36`) | HIGH | Do not attempt a mechanical rename for typography. Requires explicit design sign-off. |
| `EqColours` vs `EqColors` spelling conflict | LOW | Both exist in the codebase; hand-written `EqColours` is used. No collision risk today since `EqColors` in `eq_tokens.dart` is dead. Path A removes it. |
| `eq-design-tokens` has no `pubspec.yaml` | MEDIUM | Cannot be added as a proper Flutter git dependency. Any re-vendor requires a manual file copy and a check of class name collisions. Path A + Path C alignment eliminates this risk. |
| E1 parallel work during consolidation | MEDIUM | If E1 rebuilds widget files, it will touch the same 34 files. Coordinate: Path A first (no callsite changes), then E1, then Path C spacing alignment post-E1. |

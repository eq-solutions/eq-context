---
title: Sprint — UI Consistency Closure (EQ Suite)
owner: Royce Milmlow
created: 2026-06-08
last_updated: 2026-06-22
scope: Close all remaining UI consistency gaps across Shell, Service, Field, Cards, Intake
status: live
read_priority: reference
---

# Sprint — UI Consistency Closure

## What this sprint closes

Audit session (2026-06-08) found the following state across the suite:

| App | Token adoption | Component adoption | Gap severity |
|---|---|---|---|
| EQ Shell | ✅ tokens v1.3.1 + ui v1.1.1 | ✅ | None |
| EQ Service | ✅ tokens v1.3.1 + ui v1.1.1 | ✅ | None |
| EQ Field | ✅ tokens v1.3.1 (vendored, CI-guarded) | n/a (vanilla HTML) | Trivial — 2 inline hex fallbacks |
| EQ Cards | ⚠ vendored eq_tokens.dart v1.1.0 | n/a (Flutter) | 3 inline hex + stale vendor |
| EQ Intake (format-ui) | ⚠ no package dep — local :root copy | n/a (React) | 21 hard-coded hex values, wrong font |
| eq-ui (package itself) | ⚠ references tokens v1.2.0 | — | One version behind |
| eq-design-tokens | ✅ | — | No pubspec.yaml (Flutter git dep blocked) |

## Already done in this session (do NOT redo)

- [x] **eq-ui** `package.json`: tokens dep bumped `v1.2.0 → v1.3.1`
- [x] **eq-cards** `eq_tokens.dart`: version comment updated v1.1.0 → v1.3.1; added `skyDeep`, `amber`, `amberDeep`, `slate`, `live`, `overlayDark`
- [x] **eq-cards** `eq_colours.dart`: added `gray200`, `successBg`, `errorBg`, `warningBg`, `overlayDark`
- [x] **eq-cards** `share_licence_screen.dart`: `Color(0xFFFEF2F2)` → `EqColours.errorBg`, `Color(0xFFF0FDF4)` → `EqColours.successBg`, `Color(0xFFE5E7EB)` → `EqColours.gray200`
- [x] **eq-cards** `licence_detail_screen.dart`: `Color(0xCC000000)` → `EqColours.overlayDark`
- [x] **eq-intake** `@eq/format-ui/src/styles.css`: 21 hard-coded hex replaced with CSS vars, Plus Jakarta Sans added, `:root` token block added
- [x] **eq-design-tokens** `pubspec.yaml`: created (enables Flutter git dep)
- [x] **eq-design-tokens** `lib/eq_design_tokens.dart`: created (Flutter package entry point)
- [x] **eq-design-tokens** `build.mjs`: updated to emit `lib/eq_design_tokens.dart` on every build

## Remaining work

### T1 — eq-ui: install updated dep + typecheck (15 min)
**Repo:** eq-ui  
**Who:** console / agent  
**Steps:**
1. `npm install` to pull tokens v1.3.1
2. `npm run typecheck` — confirm clean
3. Tag `v1.1.2`, push tag
4. PR description: "bump @eq-solutions/tokens v1.2.0 → v1.3.1"

**Acceptance:** typecheck passes, tag pushed.

---

### T2 — eq-cards: wire proper Flutter git dep (30 min)
**Repo:** eq-cards  
**Who:** console / agent  
**Context:** `eq-design-tokens` now has `pubspec.yaml` + `lib/eq_design_tokens.dart`. The vendored copy in `eq_tokens.dart` can be retired once the pub dep is wired.  
**Steps:**
1. In `pubspec.yaml` add under `dependencies`:
   ```yaml
   eq_design_tokens:
     git:
       url: https://github.com/eq-solutions/eq-design-tokens
       ref: v1.3.1
   ```
2. Run `flutter pub get`
3. Replace `export 'eq_spacing.dart'` barrel in `eq_tokens.dart` with import from the package
4. Verify `flutter analyze` clean
5. PR: "wire eq_design_tokens Flutter git dep (retire manual vendor)"

**Acceptance:** `flutter pub get` succeeds, analyze clean, no hard-coded hex remaining in `lib/`.

---

### T3 — eq-cards: resolve deferred typography consolidation (45 min)
**Repo:** eq-cards  
**Context:** `eq_tokens.dart` line 20 defers unifying EqTypography scales (app uses 32/24/20/17/15/13px custom ladder; token source uses xl4/xl3/xl2/xl/lg/md/base/sm/xs). No active conflict but drift risk.  
**Files:** `lib/core/theme/eq_typography.dart`, `lib/core/theme/eq_tokens.dart`  
**Steps:**
1. Audit `eq_typography.dart` — map each app scale step to the nearest token value
2. Replace hand-coded pixel values with `EqTypography.*` constants from tokens
3. Fix the circular export: move `EqColors` inline into `eq_colours.dart` so `eq_tokens.dart` can barrel-export `eq_typography.dart`
4. `flutter analyze` clean

**Acceptance:** no hand-written font size literals in `eq_typography.dart`; barrel export works.

---

### T4 — eq-intake: wire @eq-solutions/tokens as package dep (20 min)
**Repo:** eq-intake  
**Context:** `@eq/format-ui` now has a correct `:root` CSS block (fixed in this session). Long-term it should consume the package rather than maintain a local copy — same as Shell and Service.  
**Files:** `eq-platform/packages/eq-format-ui/package.json`, `src/styles.css`  
**Steps:**
1. Add `"@eq-solutions/tokens": "github:eq-solutions/eq-design-tokens#v1.3.1"` to `eq-format-ui/package.json`
2. In `src/styles.css`, replace the hand-maintained `:root` block with `@import '@eq-solutions/tokens/tokens.css';` (remove local var definitions)
3. Verify `@eq/intake-demo` and `@eq/shell` already import tokens.css or equivalent — no double-load
4. `pnpm build` / `pnpm typecheck` clean in workspace

**Acceptance:** no local `:root` colour block in format-ui; tokens sourced from package.

---

### T5 — eq-field: replace inline hex fallbacks (10 min)
**Repo:** eq-solves-field  
**Context:** Two files use inline JS to set colours with hex fallbacks rather than pure CSS vars.  
**Files:** `sks-pipeline.js:165`, `sks-pipeline-resource.js:692`  
**Steps:**
1. Open each line, replace `#3da8d8` / literal hex with `var(--eq-sky)` etc. in the JS string
2. Check any other `#3da` / `#2986` / `#1a1a` occurrences in inline JS: `grep -r "3da8d8\|2986b4\|1a1a2e" src/`
3. Smoke-test locally

**Acceptance:** zero hard-coded EQ hex values in JS; only CSS var references.

---

### T6 — eq-design-tokens: tag v1.3.1 with pubspec + lib/ (10 min)
**Repo:** eq-design-tokens  
**Context:** pubspec.yaml and lib/ were added in this session but no tag has been cut that includes them.  
**Steps:**
1. Commit: `feat(flutter): add pubspec.yaml + lib/ entry point for Flutter git dep`
2. Tag `v1.3.1` (or `v1.3.2` if v1.3.1 already exists as a tag without these files)
3. Push tag

**Acceptance:** `flutter pub get` in eq-cards resolves the git dep cleanly.

---

### T7 — eq-intake: audit @eq/intake-demo and @eq/shell CSS for stale hex (20 min)
**Repo:** eq-intake  
**Context:** The audit confirmed these two packages define `--eq-*` vars correctly in their `:root`. This task validates there are no stale hex values leaking through elsewhere.  
**Steps:**
1. `grep -r "#3da8d8\|#2986b4\|#eaf5fb\|#1a1a2e" eq-platform/packages/eq-intake-demo/src eq-platform/packages/eq-shell/src`
2. For any hits outside a `:root` definition block, replace with the appropriate CSS var
3. Also check `eq-platform/packages/eq-confirm-ui/src` — not audited

**Acceptance:** zero stray hex literals outside `:root` blocks in all four intake packages.

---

### T8 — eq-shell + eq-service: bump to eq-ui v1.1.2 when cut (10 min)
**Repo:** eq-shell, eq-solves-service  
**Depends on:** T1 (v1.1.2 tag)  
**Steps:**
1. Update both `package.json`: `@eq-solutions/ui` ref → `#v1.1.2`
2. `npm install` + typecheck in each
3. PR per repo (or combined if trivial)

**Acceptance:** both apps on eq-ui v1.1.2.

---

### T9 — design system: self-host Plus Jakarta Sans (45 min)
**Repo:** eq-design-tokens or eq-solves-assets  
**Context:** Field loads Plus Jakarta Sans from Google Fonts (`index.html:45`). Intake loads it from Google Fonts too. Shell/Service inherit via tokens. Self-hosting removes the external CDN dependency and avoids GDPR exposure on EU tenants.  
**Steps:**
1. Download Plus Jakarta Sans WOFF2 files (weights 400, 500, 600, 700, 800) from Google Fonts or Fontsource
2. Host in `eq-solves-assets` under `fonts/plus-jakarta-sans/`
3. Add `@font-face` block to `tokens.css` (or a new `fonts.css` in eq-design-tokens)
4. Update Field `index.html` to load from assets URL instead of Google Fonts
5. Update Intake `@eq/shell/src/styles.css` and `@eq/intake-demo/src/styles.css` similarly
6. Test on a slow network profile (DevTools throttle)

**Acceptance:** no google.com/googleapis.com requests on page load in Field, Shell, or Service; font renders correctly.

---

### T10 — CI: add token-drift guard to eq-cards (30 min)
**Repo:** eq-cards  
**Context:** EQ Field has a CI workflow (`tokens-drift.yml`) that validates the vendored tokens.css against the package on every PR. EQ Cards has no equivalent — the vendored `eq_tokens.dart` can silently drift.  
**Depends on:** T2 (ideally fully retired once git dep is wired — if T2 is done, this becomes a much simpler "verify pub get resolves" check)  
**Steps:**
1. If T2 is complete: add a CI step that runs `flutter pub get` and `flutter analyze` on every PR — pub resolution will fail if the git dep ref is stale
2. If T2 is NOT complete: add a workflow that runs `node build.mjs` in eq-design-tokens and diffs the output against `eq_tokens.dart` — fail on drift

**Acceptance:** any divergence between eq-design-tokens source and eq-cards Flutter constants causes a PR check failure.

---

## Dependency order

```
T6 (tag) → T2 (Cards git dep) → T3 (Cards typography)
                              → T10 (Cards CI — simpler path)
T1 (eq-ui tag) → T8 (Shell + Service bump)
T4 (format-ui dep) — independent
T5 (Field inline hex) — independent
T7 (Intake hex audit) — independent (after T4 ideally)
T9 (font self-host) — independent, any time
```

## Done definition

Suite is 10/10 consistent when:
- [ ] All apps reference `@eq-solutions/tokens` as a package (not a copy)
- [ ] Zero hard-coded EQ brand hex values outside generated/vendored token files
- [ ] Plus Jakarta Sans self-hosted, no Google Fonts CDN calls
- [ ] eq-cards fully on Flutter git dep (no manual vendor step)
- [ ] CI guards drift in eq-cards and eq-field
- [ ] eq-ui and all consumers pinned to same tokens version (v1.3.1+)

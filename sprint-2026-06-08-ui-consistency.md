---
title: Sprint — UI Consistency Closure (EQ Suite)
owner: Royce Milmlow
created: 2026-06-08
last_updated: 2026-06-08
scope: Close all remaining UI consistency gaps across Shell, Service, Field, Cards, Intake
status: active
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
- [x] **eq-ui** `src/index.css`: barrel stylesheet created — imports `@eq-solutions/tokens/tokens.css` then all 10 component CSS files in one shot
- [x] **eq-ui** `package.json`: `@eq-solutions/tokens` moved from `dependencies` → `peerDependencies >=1.3.1`; `./styles` export alias added; tokens added to `devDependencies` for local dev; bumped to v1.2.0
- [x] **eq-shell** `src/index.css`: replaced `@import "@eq-solutions/tokens/tokens.css"` with `@import "@eq-solutions/ui/src/index.css"`
- [x] **eq-solves-service** `app/globals.css`: replaced tokens import with `@import "@eq-solutions/ui/src/index.css"`; removed inline `#3DA8D8` fallback from `:focus-visible` rule
- [x] **eq-solves-service** `package.json`: bumped `@eq-solutions/ui` → `#v1.2.0` (T8 complete)
- [x] **eq-solves-field** `scripts/sks-pipeline.js`: replaced `accent-color:#3DA8D8` (×2) with `accent-color:var(--eq-sky)` (T5 partial)
- [x] **eq-solves-field** `scripts/sks-pipeline-resource.js`: replaced `color:#3DA8D8` with `color:var(--eq-sky)` (T5 complete)
- [x] **eq-design-tokens** `build.mjs`: synced `PKG_VERSION` to `1.3.3`; rebuilt all artefacts
- [x] **eq-design-tokens** `package.json`: bumped version `1.3.2 → 1.3.3`
- [x] **eq-design-tokens** `CHANGELOG.md`: added entries for 1.3.1, 1.3.2, 1.3.3 (previously undocumented)

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

### T5 — eq-field: replace inline hex fallbacks ✅ DONE
**Files fixed:**
- `sks-pipeline.js:165,169` — `accent-color:#3DA8D8` → `accent-color:var(--eq-sky)` (×2)
- `sks-pipeline.js:286` — `#EAF5FB`/`#2986B4` tag span → CSS vars
- `sks-pipeline-resource.js:692` — `color:#3DA8D8` → `color:var(--eq-sky)`
- `sks-pipeline-resource.js:1495,1496` — border + heading color → CSS vars
- `roster.js:1214` — onfocus/onblur borderColor → CSS vars

**Knowingly left as hex (can't use CSS vars):**
- `timesheets.js` — print HTML template (separate document, no `:root`)
- `leave.js`, `managers.js`, `timesheets.js:2551`, `tender-pipeline.js` — chart color maps (literal values required by chart library)
- `safety.js`, `site-reports-shared.js` — canvas `ctx.strokeStyle` (canvas API, no CSS var support)

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

### T7 — eq-intake: audit @eq/intake-demo for stale hex ✅ DONE
**Repo:** eq-intake  
**Context:** The audit confirmed these two packages define `--eq-*` vars correctly in their `:root`. This task validates there are no stale hex values leaking through elsewhere.  
**Steps:**
1. `grep -r "#3da8d8\|#2986b4\|#eaf5fb\|#1a1a2e" eq-platform/packages/eq-intake-demo/src eq-platform/packages/eq-shell/src`
2. For any hits outside a `:root` definition block, replace with the appropriate CSS var
3. Also check `eq-platform/packages/eq-confirm-ui/src` — not audited

**Acceptance:** zero stray hex literals outside `:root` blocks in all four intake packages.

---

### T8 — eq-shell + eq-service: bump to eq-ui v1.2.0 ✅ DONE
**Repo:** eq-shell, eq-solves-service  
**Depends on:** eq-ui v1.2.0 tag  
**Steps:**
1. Update both `package.json`: `@eq-solutions/ui` ref → `#v1.2.0`
2. In each app's root CSS, replace `@import "@eq-solutions/tokens/tokens.css"` with `@import "@eq-solutions/ui/src/index.css"` (or `@import "@eq-solutions/ui/styles"`)
3. Verify `@eq-solutions/tokens` is still listed as a direct dep (peer dep requirement); keep it — needed for tokens.ts TS values
4. `npm install` + typecheck in each
5. PR per repo (or combined if trivial)

**Acceptance:** both apps on eq-ui v1.2.0; single CSS import; no duplicate tokens import.

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
- [x] All React apps reference `@eq-solutions/tokens` as a package (not a copy) — Shell, Service, Intake ✓
- [x] All React apps use the barrel CSS import (`@eq-solutions/ui/src/index.css`) — Shell ✓, Service ✓
- [x] Zero hard-coded EQ brand hex in vanilla JS (Field) — T5 complete ✓
- [x] eq-ui and all consumers on tokens v1.3.3+ / ui v1.2.0+
- [ ] eq-intake-demo: zero hardcoded EQ hex in TSX files (T7 — in progress)
- [ ] Plus Jakarta Sans self-hosted, no Google Fonts CDN calls (T9 — deferred)
- [ ] eq-cards fully on Flutter git dep — T2 (needs tag v1.3.3 + flutter pub get)
- [ ] eq-cards typography consolidation — T3 (after T2)
- [ ] CI guards drift in eq-cards — T10 (after T2)
- [ ] Git tags: eq-design-tokens v1.3.3 · eq-ui v1.2.0 (manual — push tags after code review)

## Remaining manual steps (code complete, needs git ops)

```
1. eq-design-tokens: tag v1.3.3, push
2. eq-ui: tag v1.2.0, push
3. T2: eq-cards pubspec.yaml — wire Flutter git dep (ref: v1.3.3)
4. T3: eq-cards typography consolidation
5. T9: self-host Plus Jakarta Sans (separate session — download woff2 + CDN)
6. T10: eq-cards CI drift guard (after T2)
```

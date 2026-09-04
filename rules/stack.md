---
title: Rules — Default Stack
owner: Royce Milmlow
last_updated: 2026-09-04
scope: Default technology stack and output preferences for all EQ and SKS work
read_priority: critical
status: live
---

# Rules — Default Stack

Default stack for any new work. Do not deviate without stating a reason.

---

## Technology

| Layer | Default |
|-------|---------|
| Frontend | Vite + React + Tailwind |
| Backend | Supabase (auth, database, edge functions, storage) |
| Deploy | Netlify |
| Source of truth | GitHub org `eq-solutions` — every active repo lives there (checked 2026-09-04: 15 org repos; the personal `Milmlow` account holds only `claude-code-config`). Local folder names can differ from repo names — `C:\Projects\eq-solves-service` is `eq-solutions/eq-service`. |
| Language | TypeScript — always |
| AI calls | Server-side proxy only — the API key never ships in a frontend file. What the live apps actually use: eq-shell `netlify/functions/anthropic-proxy.ts` (Intake), eq-field `netlify/functions/eq-agent.js`, EQ Receipts a Supabase Edge Function with the key in Vault. The shared Cloudflare Worker `anthropic-proxy` (`ops/decisions.md`, `rules/deployment.md`) was built for the single-HTML tools and is not what the suite apps call; its current liveness was not re-verified this pass (needs Cloudflare access). |

Never suggest adding a new tool or service without explaining why it beats
what is already in the stack. Working before refactoring — always.

---

## Output Formats

| Deliverable | Format |
|-------------|--------|
| Internal docs, specs, notes | Markdown |
| Customer-facing (SKS quotes, O&M manuals, reports) | Word or PDF |
| Code | Full files — never `// rest unchanged` or truncation |
| Prompts | Copy-paste ready |
| Specs | Written for a founder, not an enterprise team |

---

## Exceptions

Verified against each repo's `origin/main` on 2026-09-04.

- **EQ Service** (`eq-solutions/eq-service`, local folder `eq-solves-service`)
  is **Next.js 16** (`^16.2.10`, App Router, TypeScript strict, Tailwind v4,
  React 19, Vitest), not Vite. Deliberate exception — Next.js was already
  shipping at production complexity when this rules file was written. First
  commercial customer: SKS Technologies. Stack: Next.js + Supabase RLS +
  Resend + docx + exceljs + Netlify CD.
- **EQ Shell** (`eq-solutions/eq-shell`) is Vite 8 + React 19 + TypeScript 6,
  but **no Tailwind** — styling is plain CSS on `@eq-solutions/tokens`
  (pinned v1.3.2) + `@eq-solutions/ui` (pinned v1.16.4), per the design-system
  ADR (`ops/decisions.md`, 2026-05-31: tokens are the cross-stack source of
  truth, shared components are per-stack). Lucide icons. Read "Tailwind" in
  the default row as *permitted*, not required, for React surfaces built on
  the design system.
- **EQ Field** (`eq-solutions/eq-field`) is **vanilla HTML/JS with no build
  step** — one `index.html` + `scripts/*.js` + `styles/*.css`, Netlify
  Functions server-side, deploys from `main`. It cannot consume npm packages
  (it takes the tokens as a CSS file, `styles/tokens.css`). Not tech debt: it
  is the live SKS production app, chosen for zero-build deploys. Do not
  propose a React/Vite migration without a specific reason.
- **EQ Cards** (`eq-solutions/eq-cards`) is **Flutter / Dart** (Riverpod
  state, `flutter build web`), not React — the only mobile-grade client in
  the suite, chosen for the camera / OCR / offline path a web SPA does not
  give cheaply. **The gate is the widget-test suite, not `flutter analyze`
  alone.** On 2026-07-21 four real wallet-card crashes were caught by widget
  tests *after* static analysis had passed clean. Any change to Cards MUST
  run the widget suite before it is called done. See
  `rules/agentic-coding.md`.
- **EQ Receipts** (`eq-solutions/eq-receipts`, Supabase project
  `bgrhqvmvzgotxzjneskv`) is on the default stack (Vite + React + TS +
  Tailwind, Netlify) but is a private single-owner tool for Royce's entity
  group — **not part of the EQ suite**; it never touches eq-canonical or
  SKS-live.
- **Legacy single-HTML tools** (EQ Expenses, SKS Receipt Tracker — internal,
  not EQ products) stay vanilla JS + single `index.html`. Do not migrate them
  to React unless there is a specific reason. **EQ Quotes** (Flask/Python at
  `quotes.eq.solutions`) is **retired and decommissioned** — replaced by EQ
  Ops inside Shell (`eq/products.md`); it is not a stack to build on.
- **SKS NSW Labour** (`eq-solutions/sks-nsw-labour`) is vanilla JS + Supabase
  by design — the chosen PWA architecture, now retiring in favour of EQ
  Field. No engineering changes while it drains.

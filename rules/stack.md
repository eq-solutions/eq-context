---
title: Rules — Default Stack
owner: Royce Milmlow
last_updated: 2026-08-04
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
| Source of truth | GitHub (org: eq-solutions, with personal Milmlow account for active EQ products — see Exceptions) |
| Language | TypeScript — always |
| AI proxy | Cloudflare Worker `anthropic-proxy` (shared across all apps) |

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

- **EQ Solves Service** (`Milmlow/eq-solves-service`) is **Next.js 16**
  (App Router, TypeScript strict, Tailwind v4), not Vite. Deliberate
  exception to the Vite default — Next.js was already shipping at
  production complexity (169 commits, 80+ Vitest tests, 22 sprints) when
  this rules file was written. First commercial customer: SKS
  Technologies. Stack: Next.js + Supabase RLS + Resend + docx-js +
  Netlify CD. Confirmed by repo README inspection 2026-05-13.
- **EQ Cards** (`eq-solutions/eq-cards`) is **Flutter / Dart** (Riverpod
  state, `flutter build web`), not React — the only mobile-grade client in
  the suite, chosen for the camera / OCR / offline path a web SPA does not
  give cheaply. **The gate is the widget-test suite, not `flutter analyze`
  alone.** On 2026-07-21 four real wallet-card crashes were caught by widget
  tests *after* static analysis had passed clean. Any change to Cards MUST
  run the widget suite before it is called done. See
  `rules/agentic-coding.md`.
- Legacy single-HTML apps (EQ Quotes, EQ Expenses, SKS Receipt Tracker,
  early EQ Field prototype) stay vanilla JS + single `index.html`. Do not
  migrate them to React unless there is a specific reason.
- SKS Labour App (`sks-nsw-labour`) is vanilla JS + Supabase by design —
  this is not tech debt, it is the chosen architecture for the PWA.

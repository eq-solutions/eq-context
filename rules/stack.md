---
title: Rules — Default Stack
owner: Royce Milmlow
last_updated: 2026-05-13
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

## Design system imports (React apps)

```css
/* Root CSS — one import covers tokens + all component styles */
@import "@eq-solutions/ui/src/index.css";
```

Both `@eq-solutions/tokens` and `@eq-solutions/ui` must be listed as direct deps in `package.json`. Tokens is a peer dep of ui (app controls the version) and is also needed directly for `tokens.ts` JS values.

Do not import `@eq-solutions/tokens/tokens.css` separately — the barrel covers it.

---

## Exceptions

- **EQ Solves Service** (`Milmlow/eq-solves-service`) is **Next.js 16**
  (App Router, TypeScript strict, Tailwind v4), not Vite. Deliberate
  exception to the Vite default — Next.js was already shipping at
  production complexity (169 commits, 80+ Vitest tests, 22 sprints) when
  this rules file was written. First commercial customer: SKS
  Technologies. Stack: Next.js + Supabase RLS + Resend + docx-js +
  Netlify CD. Confirmed by repo README inspection 2026-05-13.
- Legacy single-HTML apps (EQ Quotes, EQ Expenses, SKS Receipt Tracker,
  early EQ Field prototype) stay vanilla JS + single `index.html`. Do not
  migrate them to React unless there is a specific reason.
- SKS Labour App (`sks-nsw-labour`) is vanilla JS + Supabase by design —
  this is not tech debt, it is the chosen architecture for the PWA.

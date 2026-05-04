---
title: Rules — Default Stack
owner: Royce Milmlow
last_updated: 2026-05-04
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
| Source of truth | GitHub (org: eq-solutions) |
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

- Legacy single-HTML apps (EQ Quotes, EQ Expenses, SKS Receipt Tracker,
  early EQ Field prototype) stay vanilla JS + single `index.html`. Do not
  migrate them to React unless there is a specific reason.
- SKS Labour App (`sks-nsw-labour`) is vanilla JS + Supabase by design —
  this is not tech debt, it is the chosen architecture for the PWA.

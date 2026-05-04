---
title: Rules — Deployment
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Deployment guardrails for EQ and SKS sites and infrastructure
read_priority: critical
status: live
---

# Rules — Deployment

---

## Site Registry

> Killed/deferred sites are not listed. EQ Variations and EQ Compliance/Ops
> are killed (29 Apr 2026). EQ Expenses is now an internal SKS tool only.
> EQ Quotes is deferred ~6 months. See `/archive/` for historical context.

| Site | Deploy method | Account | Who triggers |
|------|---------------|---------|--------------|
| eq-solves-field.netlify.app (LEAD MODULE) | Netlify Drop (manual zip) | dev@eq.solutions | Explicit instruction only |
| sks-nsw-labour.netlify.app | GitHub main → Netlify CD | dev@eq.solutions | NEVER from EQ codebase |
| eq.solutions | Cloudflare Pages zip upload | royce@eq.solutions | Explicit instruction only |
| EQ Solves Service | GitHub → Netlify CD | dev@eq.solutions | Explicit instruction only |

---

## Hard Rules

- NEVER cross-deploy. EQ files never go to SKS. SKS files never go to EQ.
- NEVER push to any branch or deploy without explicit instruction from Royce.
- NEVER touch sks-nsw-labour.netlify.app from any EQ codebase or session.
- NEVER remove DEMO_FLAG comments — they mark live re-enable points.
- NEVER deploy to eq-solves-field.netlify.app directly.
- Auth changes require full chat review before any deployment.
- Working before refactoring — never restructure while a bug is being fixed.

---

## Required: `_headers` Security File

Every Netlify or Cloudflare Pages site must ship with a `_headers` file containing baseline security headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (or `SAMEORIGIN` where needed)
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

---

## Cloudflare

- eq.solutions is on Cloudflare Pages (GoDaddy = domain registrar only, nothing else)
- Cloudflare account: royce@eq.solutions
- R2 buckets: `sks-assets`, `eq-assets`
- Anthropic proxy worker: `anthropic-proxy` — ONE worker shared across all apps
- Worker env var: ANTHROPIC_API_KEY (encrypted) — never in any frontend file
- Adding a new app that needs AI: point it at the existing worker, do not create a new one
- Cloudflare Tunnel "beelink" → beelink.eq.solutions for exposing local dev servers

---

## Supabase

- **Three projects exist** — always confirm which one before connecting:
  - `nspbmirochztcjijmcrx` = **sks-labour (LIVE SKS DATA, DO NOT TOUCH)**
  - `ktmjmdzqrogauaevbktn` = eq-solves-field (demo)
  - `urjhmkhbgaxrofurpbgc` = eq-solves-service-dev (canonical context store)
- Never run INSERT, UPDATE, DELETE, or schema changes without explicit approval
- SELECT queries are fine — state the query before executing
- Never touch SKS live data unless Royce explicitly says "SKS live"
- Supabase MCP is the reliable path for `context_files` reads/writes (GitHub MCP unreliable for writes). GitHub is canonical for `eq-context`; direct Supabase writes are emergency-only and must reconcile to GitHub the same day.
- Monthly ops: Supabase → Account → Access Tokens → revoke all but the most recent OAuth token

---

## GitHub

- Orgs: `eq-solutions` (all repos private) and personal `milmlow`
- **GitHub MCP is read-only on both orgs (403 on all write operations).** Fix at `github.com/settings/installations`.
- Until MCP fixed: all writes via browser or Cowork
- Large file API uploads: write JSON payload (base64) to temp file, use `--data @/tmp/payload.json` (inline `-d` fails for large files)
- Always include `branch` param and existing file's blob SHA in PUT requests
- eq-field-app repo: auto-deploys to sks-nsw-labour.netlify.app on push to `main`

---

## Distribution Pattern for Internal Tools

- Preferred: single index.html + Cloudflare Worker proxy
- Avoids: ThreatLocker blocks, email security flags, Python install requirements
- Never bundle .bat or .exe files — they trigger email scanners
- If file distribution is blocked: host as static file on Cloudflare Pages and share URL

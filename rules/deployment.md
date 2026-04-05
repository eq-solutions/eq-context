# Rules — Deployment

Last updated: 2026-04-05

---

## Site Registry

| Site | Repo branch | Deploy method | Who triggers |
|------|-------------|---------------|--------------|
| eq-solves-field.netlify.app | demo | GitHub → Netlify auto | Explicit instruction only |
| sks-nsw-labour.netlify.app | main | GitHub → Netlify auto | NEVER from EQ codebase |
| eq.solutions | N/A | Cloudflare Pages zip upload | Explicit instruction only |

---

## Hard Rules

- NEVER cross-deploy. EQ files never go to SKS. SKS files never go to EQ.
- NEVER push to any branch or deploy without explicit instruction from Royce.
- NEVER touch sks-nsw-labour.netlify.app from any EQ codebase or session.
- NEVER remove DEMO_FLAG comments — they mark live re-enable points.
- Auth changes require full chat review before any deployment.
- Working before refactoring — never restructure while a bug is being fixed.

---

## Cloudflare

- eq.solutions is on Cloudflare Pages (GoDaddy = domain registrar only, nothing else)
- Anthropic proxy worker: `anthropic-proxy` — ONE worker shared across all apps
- Worker env var: ANTHROPIC_API_KEY (encrypted) — never in any frontend file
- Adding a new app that needs AI: point it at the existing worker, do not create a new one

---

## Supabase

- ONE project for everything: **eq-field-app** (ID: nspbmirochztcjijmcrx, Sydney)
- Covers EQ demo products AND SKS tools — never spin up a separate project
- Separate tenants using table prefixes (e.g. sks_, eq_) or schemas
- Always confirm which project before connecting — it is always eq-field-app
- Never run INSERT, UPDATE, DELETE, or schema changes without explicit approval
- SELECT queries are fine — state the query before executing
- Never touch SKS live data unless Royce explicitly says "SKS live"

---

## GitHub

- Org: eq-solutions (all repos private)
- Large file API uploads: write JSON payload (base64) to temp file, use `--data @/tmp/payload.json`
  Inline `-d` flag fails for large files
- Always include `branch` param and existing file's blob SHA in PUT requests
- eq-field-app repo: auto-deploys to both Netlify sites on push to respective branches

---

## Distribution Pattern for Internal Tools

- Preferred: single index.html + Cloudflare Worker proxy
- Avoids: ThreatLocker blocks, email security flags, Python install requirements
- Never bundle .bat or .exe files — they trigger email scanners
- If file distribution is blocked: host as static file on Cloudflare Pages and share URL

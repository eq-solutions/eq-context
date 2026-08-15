---
title: Rules — Deployment
owner: Royce Milmlow
last_updated: 2026-08-15
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

> Updated 2026-05-20 after the SKS Live split: `sks-nsw-labour.netlify.app`
> now deploys from its own dedicated repo `eq-solutions/sks-nsw-labour`,
> not from `eq-solutions/eq-field/main` as previously. See `ops/decisions.md`
> "2026-05-20 — Split SKS Live Out of eq-field Into Dedicated Repo".

> **Live URLs and per-app status live in `suite-state.md`** (auto-refreshed
> nightly) — read them there, not here. This table carries only the durable
> deploy facts: which repo, which branch, and who may trigger. It listed a
> dead URL (`eq-solves-field.netlify.app`) as the lead module until 2026-08-04.

| App | Source repo | Branch | Deploy method | Account | Who triggers |
|------|-------------|--------|---------------|---------|--------------|
| EQ Shell | `eq-solutions/eq-shell` | `main` | GitHub push → Netlify CD — **merging to `main` IS the deploy** (auto, live 2-4s later, unattended; see note below) | dev@eq.solutions | Explicit instruction only — **and the approval gate bites at the merge click** |
| EQ Field | `eq-solutions/eq-field` | `main` (was `demo` until 2026-05-20 rename) | GitHub push → Netlify CD | dev@eq.solutions | Explicit instruction only |
| EQ Service | `eq-solutions/eq-service` (local folder `eq-solves-service`) | `main` | GitHub push → Netlify CD | dev@eq.solutions | Explicit instruction only |
| EQ Cards | `eq-solutions/eq-cards` | `main` | Netlify (deploy NOT automatic on merge — must be triggered) | dev@eq.solutions | Explicit instruction only |
| SKS NSW Labour | `eq-solutions/sks-nsw-labour` (split out 2026-05-20) | `main` | GitHub push → Netlify CD | dev@eq.solutions | NEVER from an EQ codebase |
| eq.solutions (marketing) | (manual zip) | — | Cloudflare Pages zip upload | royce@eq.solutions | Explicit instruction only |

---

## Hard Rules

- NEVER cross-deploy. EQ files never go to SKS. SKS files never go to EQ.
- NEVER push to any branch or deploy without explicit instruction from Royce.
- NEVER touch sks-nsw-labour.netlify.app from any EQ codebase or session.
- NEVER remove DEMO_FLAG comments — they mark live re-enable points.
- NEVER deploy an EQ Field site directly — it deploys from `eq-field` on push to `main`, on explicit instruction only.
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

- **Always confirm which project before connecting.** The live footprint is the
  Control Layer + per-tenant model — `system/architecture.md` is the authority
  for *why*; this list is the operational guardrail:
  - `nspbmirochztcjijmcrx` = **sks-labour — LIVE SKS DATA, DO NOT TOUCH** unless Royce explicitly says "SKS live"
  - `jvknxcmbtrfnxfrwfimn` = eq-canonical — control plane only (tenant registry, config, entitlements). Never a data store.
  - `zaapmfdkgedqupfjtchl` = eq-canonical-internal — EQ tenant data plane
  - `ehowgjardagevnrluult` = sks-canonical ("ehow") — SKS tenant data plane; sole live DB for EQ Service and EQ Field
  - **DELETED, never reference as live:** `urjhmkhbgaxrofurpbgc` (eq-solves-service-dev, deleted 2026-06-22 — was the context store; the substrate is now the GitHub repo itself) and `ktmjmdzqrogauaevbktn` (eq-solves-field, confirmed gone 2026-06-30)
- Never run INSERT, UPDATE, DELETE, or schema changes without explicit approval
- SELECT queries are fine — state the query before executing
- Never touch SKS live data unless Royce explicitly says "SKS live"
- The `eq-context` substrate is the GitHub repo itself — edit MD files, commit, push to `main`. There is no `context_files` table or Supabase cache (retired 2026-06-22); assistants read via raw URLs (`raw.githubusercontent.com/eq-solutions/eq-context/main/<path>`).
- Monthly ops: Supabase → Account → Access Tokens → revoke all but the most recent OAuth token

---

## GitHub

- Orgs: `eq-solutions` (mix of public + private; check each repo) and personal `milmlow`
- **GitHub MCP is read-only on both orgs (403 on all write operations).** Fix at `github.com/settings/installations`.
- Until MCP fixed: all writes via browser or Cowork
- Large file API uploads: write JSON payload (base64) to temp file, use `--data @/tmp/payload.json` (inline `-d` fails for large files)
- Always include `branch` param and existing file's blob SHA in PUT requests
- `eq-solutions/sks-nsw-labour` repo (split out 2026-05-20): auto-deploys on push to `main`
- `eq-solutions/eq-field` repo: auto-deploys on push to `main` (branch formerly `demo` — renamed 2026-05-20 after the SKS Live split)
- **Auto-deploy on push is not universal.** `eq-cards` and `eq-receipts` both need a manual Netlify trigger despite carrying a `netlify.toml` that implies otherwise — a merged PR on those repos is not a live change. Confirm the deploy, don't infer it.
- **`eq-shell` is the opposite trap, and it is the one that bites harder.** Merging a PR to `main` **does** trigger a Netlify production build, live on core.eq.solutions **2-4 seconds later, unattended**. There is no gap between "merge it" and "ship it" on this repo. **Never say something is "merged but not live" here.** Treat every eq-shell merge approval as a production-deploy approval — this is what makes the auth-change review rule bite at the *merge* click, not at some later step. Trigger is Netlify's own GitHub App (installation `121276861`), not a repo webhook and not a workflow. Verified 2026-08-15 across 13 consecutive merges → 13 production deploys spanning 15 hours and multiple concurrent sessions.
  - **Do not re-derive this from `deploy_source` or `cdp_enabled_contexts`.** A stale note claimed the opposite and survived two re-verifications because its two observations are still literally true — `cdp_enabled_contexts` really is `["deploy-preview"]` and production deploys really do report `deploy_source: "api"`. The *inference* was false: `"api"` does not mean "a human triggered it". **Correlate merge timestamps against deploy `created_at` instead:** `npx netlify api listSiteDeploys --data '{"site_id":"a3473f83-7c82-4f1e-872d-aa96eaa55172","per_page":40}'`
  - **"My deploy succeeded" ≠ "my code is live", and neither implies the other.** Concurrent merges make Netlify supersede in-flight production builds (`state: "error"`, `error_message: "Skipped"`) — those commits still ship inside a later build. The inverse also happens. **The check is commit ancestry against whatever is actually serving:** take `commit_ref` from the newest `state: "ready"` / `context: "production"` row, then `git merge-base --is-ancestor <my-sha> <live-commit_ref>`. Don't infer liveness from deploy titles — a skipped deploy still carries its commit's title.

---

## Distribution Pattern for Internal Tools

- Preferred: single index.html + Cloudflare Worker proxy
- Avoids: ThreatLocker blocks, email security flags, Python install requirements
- Never bundle .bat or .exe files — they trigger email scanners
- If file distribution is blocked: host as static file on Cloudflare Pages and share URL

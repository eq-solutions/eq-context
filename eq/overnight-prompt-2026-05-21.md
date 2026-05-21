---
title: EQ Shell overnight autonomous brief — 2026-05-21
owner: Royce Milmlow
last_updated: 2026-05-21
scope: Self-directed multi-hour work session. Goal is to take core.eq.solutions from "audit-fix complete" to "demonstrably works end-to-end" — fewer broken edges, more polish, more honest product feel. No new modules, no auth refactors, no destructive changes.
read_priority: critical
status: ready to paste at session start
---

# EQ Shell — overnight autonomous brief

You (Claude) are running this session on Royce's behalf while he is
asleep. He is the founder of EQ Solutions, NSW Ops Manager at SKS
Technologies. He has explicitly asked you to **audit, improve, and
make decisions on your own** to get EQ Shell to a state that works
well enough to demo to executives.

This file is the brief. Read it once at session start, then go. Don't
ask for confirmation on the things this file authorises. Do ask on
the things it doesn't.

---

## 1. Where things stand right now (2026-05-21 evening, Sydney time)

- `core.eq.solutions` (eq-shell repo, `main` branch, Netlify auto-deploy)
  is live with: login, dark-navy home hero, Topbar, 6-module grid,
  per-domain intake (42 entities), entity browser, audit log, admin
  user management, Cards iframe, Field iframe with handoff overlay.
- All 8 items from `eq/canonical-readiness/audit-2026-05-21.md` are
  shipped and verified.
- Open PRs: none. Working tree: clean. Migrations: all applied.
- Tenant: `core` (slug `core`, id `dcb71d03-858d-488a-b8e6-b76b404d25d6`).
- Sign-in: `dev@eq.solutions` / PIN `1234`. Manager + platform_admin.
- 50 seeded customers, 25 staff, 10 tenders, plus the rest of the
  snapshot grid populated.

You verified all of this in Chrome MCP at the end of the previous
session. Trust that the bar is "everything I tested earlier works."

---

## 2. Mission — what "works" means

**The bar:** a trade-subcontractor manager could land on the login
page, sign in, and spend 30 minutes poking around `core.eq.solutions`
without hitting an error, a dead end, an obviously placeholder page,
or a piece of UI that contradicts the eq.solutions marketing brand.

Specifically:

- Every link in the Topbar lands somewhere meaningful, not a
  placeholder or 500 error.
- Every entity card in the per-domain intake pages either accepts a
  CSV or honestly says "wiring lands in Sprint X".
- Every admin page (audit, users, settings) renders with the canonical
  styling (Plus Jakarta Sans, Sky #3DA8D8, dark-navy hero where it
  belongs, no purple, no Stripe-grey dashboards).
- No bare `eq-login`/`eq-shell` legacy class blocks. Use
  `eq-page`, `eq-table`, `eq-pill`, `eq-btn-primary`, etc.
- No 404, 500, "Could not find table" or similar in normal flows.
- No console errors on page load for any of the verified pages.

**Out of bar for this session:** mobile responsiveness, performance
under realistic data volumes, email-delivery wiring, the Cards Flutter
flip (S4 — leave it alone), the EQ Field demo site itself (separate
repo, separate concern).

---

## 3. Authority — what you can do without asking

You can:

1. **Make and push commits to `eq-shell` `main`** — Netlify auto-deploys.
   Commit messages must end with the Claude co-author footer per
   `CLAUDE.md`. Each commit must build clean (`pnpm build` ok).
2. **Apply Supabase migrations** via the MCP `apply_migration` tool on
   project `jvknxcmbtrfnxfrwfimn` (eq-canonical). Use snake_case names
   prefixed `2026_05_21_` (or the current date). RPCs in `public`
   schema, gates on JWT app_metadata claims (`tenant_id`, `eq_role`,
   `is_platform_admin`), `SECURITY DEFINER`, `search_path` set
   explicitly (see existing RPCs for the pattern).
3. **Create and push commits to `eq-context` `main`** — substrate docs,
   plan updates, audit logs. Auto-syncs to the Supabase context API.
4. **Run the build, run TypeScript checks**, browse pages in Chrome MCP,
   read Sentry, read Supabase logs, read Netlify env.
5. **Verify your own work** by browsing the deployed site in Chrome MCP
   after each push. Do this routinely — every commit you push, walk
   the affected page to confirm it works.
6. **Update `eq/canonical-readiness/audit-2026-05-21.md`** with any new
   findings + their resolutions. Keep it as the running ledger.
7. **Delete the test row** if you write a probe row to any audit table.
   Always clean up after diagnostic work.
8. **Close stale tasks** in the task list. Create new ones for follow-ups
   you discover.

You CAN'T do (per `CLAUDE.md` — global non-negotiables):

- Touch SKS infrastructure (`nspbmirochztcjijmcrx` Supabase, the
  `sks-nsw-labour.netlify.app` repo, the eq.solutions Cloudflare zip,
  anything in `C:\Projects\eq-property-solutions`, etc.). EQ-only.
- Auth changes without explicit approval. JWT shape, cookie format,
  session TTL, mint endpoints, RLS policies on identity tables, role
  enum, platform_admin flag — all off limits unless I authorise here.
  (You already know the JWT shape: `app_metadata.tenant_id`,
  `app_metadata.eq_role`, `app_metadata.is_platform_admin`.)
- Delete files without explicit permission. Rename/refactor fine.
- Skip git hooks / sign without GPG / force-push.
- Rotate any secrets (Royce explicitly opted out of PAT/Sentry rotation).
- Deploy Cards Flutter to canonical (task #25 is deferred until Royce
  triages it).
- Push to ANY branch other than `main` of `eq-shell` or `eq-context`.
- Cross-deploy.

---

## 4. Working method

**Loop:** audit → pick highest-value fix → ship it → verify in Chrome
MCP → log it → repeat.

**Discipline:**

- ONE thing at a time. Don't bundle five fixes into one commit. One
  commit per logical change. Keeps the audit ledger honest.
- After EVERY push: open the affected page in Chrome MCP and confirm
  it still works AND the fix landed. The Netlify deploy takes 60–90s.
- Read the existing code BEFORE writing new code. The two bugs you
  caught in the verification walk (#6 RPC routing, #8 admin
  schema-cache) both came from misunderstanding the Phase 1.F schema
  split. Don't repeat that.
- Prefer the existing pattern. If `eq_browse_entity` already exists
  in `public` as the way to read app_data tables, mirror it. Don't
  invent new conventions.
- Use canonical design tokens (`--eq-sky`, `--eq-deep`, `--eq-ice`,
  `--eq-ink`, `--eq-grey`, `--eq-white`, `--eq-border`, plus the
  `--gray-N` neutrals). Never invent new ones like `--eq-line`.
- Use Plus Jakarta Sans. No purple. No gradients. No shadows on static
  cards.
- 8-pixel grid. Radii 4/6/8/12/9999.
- Tables: Sky `#3DA8D8` thead background, WHITE uppercase text. This
  is from `eq-solutions-design.prompt.md` and is non-negotiable.

**When you find a bug you don't know how to fix:**

- Diagnose it (read the code, read the SQL, read the network panel).
- Write up what you found in the audit doc with severity tag and a
  proposed fix path.
- Move on — don't get stuck.

---

## 5. Priority queue — work through these in order

These are the known polish items from the audit + things spotted
during the verification walk. Order is by visible impact, not effort.

1. **Tenant Settings page** (`/core/admin/settings`). Currently
   doesn't exist. Should let a manager edit tenant name + brand colour
   + module entitlements. Use the existing `eq_get_tenant_user`
   pattern for the RPC. Server writes go through a new Netlify
   function that uses service-role + the existing role check.
2. **Storage browser** (`/core/storage/{bucket}`). Per-tenant Supabase
   buckets already exist (S2.C). Build a simple list/upload/download
   UI for files. Read-only first; uploads if time.
3. **User invite flow polish**. The invite endpoint works but the
   post-invite UX shows a raw URL. Build a proper "Accept invite"
   landing at `/invite/{token}` that lets the new user set their
   PIN and lands them on tenant home.
4. **Quotes module placeholder**. `/core/quotes` shows "Soon" but
   actually serves QuotesModule which is mostly empty. Either build
   a real placeholder ("EQ Quotes is in development. Here's what's
   coming.") or wire up the basic list view from the existing
   schema.
5. **Service module placeholder**. Same as Quotes.
6. **Tender Pipeline placeholder**. Same.
7. **Verify EQ Field iframe handoff** end-to-end with the new
   postMessage overlay (commit 5c9cb60 + companion eq-field v3.5.12).
   Sign out, sign back in, navigate to /core/field, confirm overlay
   disappears within 5s.
8. **Console-clean check**. Walk every page in Chrome MCP and
   confirm zero console errors. Capture and fix anything found.
9. **404 / unknown route**. `/core/asdf` currently does what? Verify
   it has a sensible "Page not found" with a way back to home.
10. **Logout flow**. Verify Sign out clears cookies, lands on login,
    and signing back in still works.

Treat this as a backlog, not a contract. If something else seems
higher value once you're in the code, do that instead and note why
in the commit message.

---

## 6. Definition of done for the session

**Leave Royce three things in the morning:**

1. **A clean `main` on `eq-shell`** — no half-shipped work, no broken
   build, no obvious regressions.
2. **An updated audit ledger** at
   `eq/canonical-readiness/audit-2026-05-21.md` — every fix you
   shipped logged with commit SHA, every new issue you found logged
   with severity, every item you punted on logged with why.
3. **A morning report** at
   `eq/overnight-report-2026-05-21.md` — 2-3 paragraphs covering:
   what you shipped, what you discovered, what you decided NOT to do
   and why, the one or two things you'd recommend Royce look at first
   when he sits down.

**Don't:**

- Open a chat asking him to verify things at 3 AM.
- Spawn agents that need login walkthroughs he can't respond to.
- Touch his personal accounts (PostHog, Sentry, Microsoft Clarity) —
  those are wired via env vars he set up; just push code that uses
  them.
- Decide to "just refactor the whole brand system real quick" — you
  have permission to polish, not to invent new architecture.

---

## 7. Quick reference — paths, conventions, gotchas

- **Repos:** `C:\Projects\eq-shell` (shell), `C:\Projects\eq-context`
  (substrate), `C:\Projects\eq-intake` (intake package, vendored),
  `C:\Projects\eq-cards` (cards, separate deploy).
- **Supabase project:** `jvknxcmbtrfnxfrwfimn` (eq-canonical). Tenant
  `dcb71d03-858d-488a-b8e6-b76b404d25d6` (slug `core`).
- **Schemas:** `shell_control.*` (auth, control plane), `app_data.*`
  (entity layer), `public.*` (RPCs only — PostgREST exposes this).
- **Service client gotcha:** `_shared/supabase.ts` sets
  `db.schema='shell_control'`. So `sb.rpc('foo')` looks in
  `shell_control.foo`. For RPCs in `public`, use
  `sb.schema('public').rpc('foo', ...)`. Don't fall into this again.
- **Client gotcha:** PostgREST only exposes `public`. Browser code can
  ONLY `.from(table)` against `public` schema. Anything in
  `shell_control` needs a public RPC wrapper.
- **JWT claims:** `app_metadata.tenant_id` (uuid),
  `app_metadata.eq_role` (text), `app_metadata.is_platform_admin`
  (boolean). Use these in `SECURITY DEFINER` RPC gates.
- **Design spec:** `C:\Users\EQ\Downloads\eq-solutions-design.prompt.md`
  is the canonical brand brief. Re-read it before any visual change.
- **Test-data RPCs in `public`:** `eq_browse_entity`,
  `eq_tenant_dashboard_counts`, `eq_recent_intake_events`,
  `eq_list_module_entities`, `eq_list_tenant_users`,
  `eq_get_tenant_user`, `eq_recent_mint_audit`, `eq_record_mint`.

---

## 8. Sentry / Sentry / observability

- DSNs live in Netlify env vars (`VITE_SENTRY_DSN`,
  `VITE_POSTHOG_KEY`, `VITE_CLARITY_PROJECT_ID`). Currently NONE are
  set on the shell deploy — the observability layer logs
  "disabled — X not set" on every page load. That's by design until
  Royce wires them. Don't try to set them. Don't push code that
  hard-codes any DSN.
- The Sentry MCP server (`mcp.sentry.dev/mcp/eq-solutions/eq-shell`)
  is loaded for this session if you need to triage real issues. Most
  likely it shows zero issues — the dev env doesn't have Sentry on
  yet.

---

## 9. If something feels off, default to NOT shipping

The bar is "Royce wakes up to a better shell, not a broken one." If
you can't verify a fix in Chrome MCP, revert it. If you can't decide
between two designs, pick the one closer to the eq.solutions marketing
site and ship that — never block on a decision overnight.

If you somehow break the deploy (build fails, Netlify red, login
broken), **stop and write a recovery commit immediately** rather than
keeping going. A broken `main` first thing in the morning is worse
than three half-finished features.

---

## 10. Start signal

Begin by:
1. Reading this entire file once.
2. Reading `eq/canonical-readiness/audit-2026-05-21.md` for the
   current punch-list state.
3. Reading `eq/pending.md` for outstanding items.
4. Then opening `core.eq.solutions` in Chrome MCP, signing in as
   `dev@eq.solutions` / `1234`, and walking the priority queue from
   §5.

Make decisions. Move with discipline. Leave a clean `main` and a
written morning report.

Good night, Royce.

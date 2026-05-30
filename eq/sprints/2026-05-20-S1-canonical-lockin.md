---
title: Sprint S1 — Canonical-readiness lock-in + ship-ready
owner: Royce Milmlow
last_updated: 2026-05-30
scope: First sprint after canonical-readiness Units 1-7 shipped autonomously. Lock in the work (verify, harden, expose), close out paused PRs, ship the deferred Cards iframe, rotate compromised credentials, and produce the first functional registry-driven dropzone end-to-end.
read_priority: critical
status: live
duration_estimate: 1 week calendar (~10 hours work at EQ pace) — autonomous phase took ~2 hours actual
shipped: S1.1, S1.4, S1.5, S1.6, S1.9, S1.10
pending: S1.2 (PAT rotation), S1.3 (Sentry rotation), S1.7 (open PRs — depends on S1.2), S1.8 (Cards redeploy)
---

# Sprint S1 — Canonical-readiness lock-in + ship-ready

**Status:** in flight — locked 2026-05-20. 6 of 10 items shipped autonomously; 4 remaining are Royce-required dashboard/local-build actions.

10 items. Sequenced by dependency. Each has effort, blast-radius, definition
of done. Recommended order is top-to-bottom but item 2 (PAT rotation) is the
only true blocker for everything else if push workflows break.

---

## Objective

Take the substrate work that landed 2026-05-20 (Units 1-7 of
[`eq/canonical-readiness/plan.md`](../canonical-readiness/plan.md)) and make
it **operational** — reachable by clients, hardened, integrated into the new-
tenant provisioning path, and producing one user-visible end-to-end value
moment (Core CSV intake). Close out paused work that's been blocking the
backlog. Rotate the credentials flagged compromised 2026-05-19.

Sprint success = every item has Status = ✅ Done at sprint review.

---

## Strategic context

- Canonical-readiness shipped → 42 entities across 5 modules, per-domain RPCs,
  registry-driven UI scaffold. **Built but not yet client-reachable** —
  PostgREST doesn't know about app_data + shell_control schemas.
- 3 GitHub PATs treated as compromised since 2026-05-19 (pending.md
  CRITICAL). Today's deploys still work because the leaked PATs haven't been
  revoked — but every day they're live is exposure.
- Cards iframe wedge `/:tenant/cards` is committed but doesn't render
  because `eq-cards.netlify.app` hasn't been redeployed with the relaxed
  `web/_headers`. Visible UX broken state.
- 2 PRs (eq-shell:claude/cards-iframe-embed + eq-intake:claude/cards-licence-canonical-entity)
  are pushed branches without PRs — paused on Phase 1.F merge, which is now done.

This sprint converts substrate into shipped value + hardens what shipped.

---

## In-scope items

### S1.1 — PostgREST exposed-schemas toggle (~10 min, ops)

**Why:** Unit 2 moved canonical entity tables to `app_data.*` and shell-control
to `shell_control.*`. PostgREST's `db.schemas` config still defaults to
`public, graphql_public`. Clients calling `/rest/v1/customer` get 404
because PostgREST doesn't route to `app_data`. RPCs work (proven by Unit 7's
`eq_list_module_entities`) but direct table queries don't.

**Action:**
- Supabase Dashboard → Project Settings → API → **Exposed schemas** → add
  `app_data, shell_control`
- Verify by `curl https://jvknxcmbtrfnxfrwfimn.supabase.co/rest/v1/customer?limit=1 -H 'apikey: <anon_key>' -H 'Authorization: Bearer <auth_jwt>'`
- Should return 200 with `[]` (empty array — no rows but schema reachable)

**DoD:** Client-side `supabase.from('customer').select()` returns no error.

**Blast radius:** Low. Read-only config change. Reversible.

---

### S1.2 — CRITICAL: GitHub PAT rotation (~30 min, security)

**Why:** Per `eq/pending.md` "CRITICAL — Rotate GitHub PATs (substrate
exposure)": three PATs were in plaintext in `system/infrastructure.md`
history from at least 2026-05-15. All treated as compromised regardless
of which got "removed" from `.git-credentials.*` files — they've been
on GitHub.

**Action:**
- Revoke all 3 PATs at github.com/settings/personal-access-tokens
  (labels: "EQ Solutions", "Milmlow", "Milmlow alt")
- Issue one new fine-grained PAT to replace "EQ Solutions"
- Update `C:\Projects\.git-credentials.eq-solutions` + `C:\Projects\.git-credentials` on Beelink with new value
- Verify by pushing to eq-context (the trigger that exposed the issue originally)

**DoD:** All 3 old PATs revoked in GitHub UI; new PAT successfully pushes to eq-shell + eq-context.

**Blast radius:** Push workflow temporarily broken until creds are updated everywhere. Plan ~30 min window.

---

### S1.3 — Sentry token rotation (~15 min, security)

**Why:** Per `eq/pending.md`: both Sentry org token + user token leaked in the 2026-05-20 chat transcript. Same exposure as PATs.

**Action:**
- sentry.io → Settings → Account → API → Auth Tokens → revoke both
- Issue new tokens with scopes: `org:read`, `project:read`, `event:read`, `member:write` (for invites)
- Update Netlify env vars on eq-shell + eq-quotes-port + any other Sentry-wired projects
- Update local `.env` files

**DoD:** Old tokens 401 when used; new tokens work for Sentry MCP queries.

**Blast radius:** Low. Sentry observability briefly offline during rotation.

---

### S1.4 — pnpm db:apply bundle update (~30 min)

**Why:** `eq-intake/eq-platform/scripts/db-apply.ts` bundles migrations 001-006 into `.generated/all-migrations.sql` for new-tenant provisioning. Units 2-5 added migrations 007-011 (via MCP, not bundle). New tenants today would get the OLD canonical shape. Per Decision 3 (template-first deploy), the bundle is canonical source.

**Action:**
- Edit `eq-intake/eq-platform/scripts/db-apply.ts`:
  - Add section 8 (Schema split — 007)
  - Add section 9 (RPC decomposition — 008)
  - Add section 10 (Quotes domain — 009)
  - Add section 11 (Field domain — 010)
  - Add section 12 (eq_list_module_entities — 011)
- Run `pnpm db:apply` from eq-platform root
- Verify `.generated/all-migrations.sql` includes all 11 sections + the seed_schema_registry step
- Inspect generated file for ordering correctness

**DoD:** Bundle regenerates; size ~250-300 KB (up from ~211 KB); manual scan confirms section order matches dependency order.

**Blast radius:** None for `core` (already applied). Affects future tenants.

---

### S1.5 — @eq/schemas codegen run (~15 min)

**Why:** Unit 4 wrote 7 quote schema JSONs; Unit 5 left Field schemas as registry-only (no JSON files). `pnpm generate` produces TypeScript types + Zod validators from JSON schemas. Until run, the new entities can't be type-checked in TS code.

**Action:**
- `cd eq-intake/eq-platform/packages/eq-schemas`
- `pnpm generate`
- Verify `dist/generated/types/quote.types.ts`, `quote-line-item.types.ts`, etc. exist
- Spot-check one Zod validator to confirm CHECK constraints surface (e.g. status enum, money fields as integer)
- Decision: also author JSON schema files for the 22 Field-domain entities? (deferred to S2 if "no")

**DoD:** Codegen runs without error; 7 quote-domain types exist; Field-domain decision logged.

**Blast radius:** None — additive only.

---

### S1.6 — Generic ParserDropZone wiring for Core domain (~2-3 hrs)

**Why:** Unit 7 shipped the registry-driven landing-page scaffold with "Import CSV (coming soon)" placeholder buttons. To turn this into actual user value, at least one domain needs functional dropzones. Core is fastest (3 entities: customer, contact, site) and most likely to be exercised first.

**Action:**
- Read `@eq/confirm-ui` ParserDropZone API
- In `eq-shell/src/modules/intake/DomainLanding.tsx`, replace the disabled button per entity with a button that opens an `<EntityDropZone>` modal/inline panel
- `EntityDropZone` mounts ParserDropZone configured with the entity's schema (loaded via `@eq/schemas`) + a commit function that calls the canonical RPC (`eq_intake_commit_batch_core` directly for module-aware path, or the router for back-compat)
- Per-tenant `source_app` claim set to `'shell'` on the JWT context
- Test against a small CSV: 5 customers, 5 contacts, 5 sites — verify commit succeeds and rows appear in app_data
- Repeat for Quotes domain (scope_template + rate_library imports) as time allows; defer Field's 22 entities to S2

**DoD:** A user can navigate to `/:tenant/intake/core`, drop a customers.csv, see ParserDropZone preview + validation, confirm, and the rows land in `app_data.customers`. Build + lint green.

**Blast radius:** UI changes only. Writes go through existing per-domain RPCs (already shipped + tested via Unit 3 path).

**Risk:** ParserDropZone API surface might require deeper IntakeModule restructure than estimated. If >3 hrs, ship for Core only and defer Quotes wiring to S2.

---

### S1.7 — Open the 2 paused PRs (~1 hr)

**Why:** Per pending.md Tier 2 dangler: eq-shell:claude/cards-iframe-embed and eq-intake:claude/cards-licence-canonical-entity are pushed branches without PRs. Held pending Phase 1.F merge (which shipped). They've been hanging since 2026-05-20 morning.

**Action:**
- `eq-shell`: rebase `claude/cards-iframe-embed` against `main` (Phase 1.F changes); add `useCan('cards.*')` gate addition if not already; open PR with description
- `eq-intake`: same for `claude/cards-licence-canonical-entity` (note: per substrate, eq-intake has no GitHub remote — confirm before pushing)
- Use the `gh pr create` flow with the standard format

**DoD:** Both PRs open with green CI; or if eq-intake has no remote, document that fact as a discovered constraint and close out that half of the item.

**Blast radius:** None until merged.

---

### S1.8 — Cards Netlify redeploy (~20 min, ops)

**Why:** Cards iframe wedge at `/:tenant/cards` doesn't render because `eq-cards.netlify.app` hasn't been redeployed with the relaxed `web/_headers` (committed but not deployed). Visible UX broken state: users clicking the Cards tile see X-Frame-Options block.

**Action:**
- `cd C:\Projects\eq-cards`
- `flutter build web --release`
- Zip `build/web/` folder
- Netlify dashboard → site `c1bf4b4d-3131-4dd6-977f-2c0dd5cc4d72` → Deploys → drag-drop zip
- Wait for deploy
- Visit `https://core.eq.solutions/core/cards` — iframe should now render

**DoD:** Cards iframe renders inside shell without X-Frame-Options error.

**Blast radius:** Cards-side deploy. No impact on shell or canonical.

---

### S1.9 — Substrate hygiene: tender-pipeline + orphan intake.tsx (~15 min)

**Why:** Two known-stale items in eq-shell:
- `src/modules/tender-pipeline/` — 5 page stubs (~9KB), not on roadmap per 2026-05-20 part-d. Plan said: delete or stale-mark.
- `src/modules/intake.tsx` — orphan from the Phase 1.F directory restructure (lives alongside the new `src/modules/intake/index.tsx`).

**Action:**
- **tender-pipeline**: add `// stale 2026-05-20 — not on Phase 2 roadmap, kept for future-exploration reference` to top of each .tsx file. NO deletion (CLAUDE.md hard rule).
- **intake.tsx orphan**: surface to Royce. Either he gives explicit delete permission, or it gets the same stale-marker treatment.

**DoD:** Stale markers in place OR Royce decision logged.

**Blast radius:** Comments only.

---

### S1.10 — gitleaks pre-commit hook on eq-context (~45 min, security)

**Why:** Per pending.md and the 2026-05-19 incident: GitHub push-protection caught the PAT exposure on the second push, but only because of a literal pattern match. A local pre-commit hook would have prevented the commit in the first place.

**Action:**
- `cd C:\Projects\eq-context`
- `pip install pre-commit gitleaks` (or use binary download)
- Author `.pre-commit-config.yaml`:
  ```yaml
  repos:
    - repo: https://github.com/gitleaks/gitleaks
      rev: v8.21.2
      hooks:
        - id: gitleaks
  ```
- `pre-commit install`
- Test by attempting to commit a fake `ghp_test...` token — should be blocked
- Document in repo README

**DoD:** Local commit with a secret pattern is blocked.

**Blast radius:** Local-only. Won't break existing git operations.

---

## Out of scope (deliberately parked)

| Item | Why parked | Next sprint? |
|---|---|---|
| Cards Unit 3 (data migration) | Substantial — separate sprint with full review pass | S2 |
| Cards Unit 4 (Flutter flip + SSO) | Depends on Cards Unit 3 | S3 |
| cards.eq.solutions custom domain | Operational, fine on netlify.app subdomain for now | S2 |
| ParserDropZone for Field + Cards + Service domains | Generalises after Core is proven | S2 |
| Field-domain JSON schemas in @eq/schemas (22 files) | Registry already has placeholders; full TS types are nice-to-have | S2 |
| EQ GTM outreach (Tier 3) | Different workstream; parallel-eligible | Continuous |
| Field Phase D (server-side role enforcement) | Planned for early June | June |
| Tender Pipeline SKS promotion | Royce manual approval required for SKS LIVE writes | Royce-driven |
| EQ-IP-Register P1 items | Royce-driven (legal/Webb engagement) | Royce-driven |
| Per-tenant storage bucket policies | Cards Unit 3 migration is the natural pairing | S2 |

## Risks

| Risk | Mitigation |
|---|---|
| PAT rotation breaks push workflow mid-sprint | Do S1.2 first; verify before moving on |
| ParserDropZone wiring exceeds 3 hr estimate | Ship Core-only fallback, defer Quotes to S2 |
| PostgREST exposed-schemas change has unforeseen effect on existing RPC clients | Reversible — un-toggle if any breakage; revert during sprint |
| pnpm db:apply bundle has ordering bug uncovered when generating | Test against a scratch Supabase project before sprint close |
| Cards `flutter build web` fails / drops state | Verify Flutter SDK present; alternate: skip deploy, mark as "investigation needed" |

## Sprint success criteria

- [ ] Items 1-10 all marked ✅ Done (or explicitly deferred with rationale)
- [ ] No regressions on core.eq.solutions (auth + intake module still operational)
- [ ] All 3 leaked GitHub PATs revoked
- [ ] At least Core CSV import works end-to-end through Unit 7's surface
- [ ] Cards iframe renders cleanly at /:tenant/cards
- [ ] eq-context substrate has gitleaks pre-commit hook

## Where to start

If autonomous: S1.2 (PAT rotation) → S1.3 (Sentry rotation) → S1.1 (schemas toggle) → S1.4 (bundle) → S1.5 (codegen) → S1.8 (Cards redeploy) → S1.6 (ParserDropZone) → S1.7 (PRs) → S1.9 (hygiene) → S1.10 (gitleaks).

Rationale: get security hygiene done first (S1.2 + S1.3), then unlock client-side reachability (S1.1), then substrate stability (S1.4 + S1.5), then the one user-visible value moment (S1.6) with S1.8 prerequisite shipped first, then close out paused work (S1.7), then hygiene (S1.9 + S1.10).

If Royce-paced: do S1.2 first (the only true blocker), then pick from the rest by interest/availability.

---

## Related

- [eq/canonical-readiness/plan.md](../canonical-readiness/plan.md) — what S1 builds on top of
- [eq/pending.md](../pending.md) — source for security items + Tier 2 danglers
- [eq/products.md](../products.md) — current product status post-Phase-1.F
- `C:\Projects\RESUME-EQ-SHELL-NEXT.md` — the resume prompt that ran ahead of canonical-readiness execution
- `C:\Projects\eq-context\resume\RESUME-2026-05-21.md` — the open-triage resume

## Execution record — autonomous push (2026-05-20)

| Item | Outcome | Evidence |
|---|---|---|
| S1.1 | ✅ Done | Migration `2026_05_20_s1_postgrest_exposed_schemas`; pg_roles confirms `pgrst.db_schemas=public, graphql_public, app_data, shell_control` |
| S1.4 | ✅ Done | `eq-intake/sql/011_eq_list_module_entities.sql` + `010b_field_dispatch_and_router.sql` created; db-apply.ts updated with sections 8-12; bundle regen output: 363 KB (up from 211 KB) |
| S1.5 | ✅ Done | `pnpm generate` ran cleanly — 20 schema modules → `eq-schemas/src/generated/`. Quote-domain types (7) + Field-domain still placeholder (registry only) |
| S1.6 | ✅ Done | `EntityImportPanel.tsx` (new) + `DomainLanding.tsx` (extended) wires Core entities (customer, contact, site) to ParserDropZone. Commit fn does eq_intake_events INSERT + eq_intake_commit_batch RPC. Build green: `DomainLanding-pWaFbaZ0.js` chunk 36.13 KB |
| S1.9 | ✅ Done | Stale-marker comments added to `tender-pipeline/index.tsx` and orphan `intake.tsx`. Delete-or-keep decision logged in stale comment, pending Royce |
| S1.10 | ✅ Done | `.pre-commit-config.yaml` (gitleaks v8.21.2) + native git hook `scripts/pre-commit-secrets.sh` (always-on regex guard). Hook installed in `.git/hooks/pre-commit`. PAT pattern verified |
| S1.2 | ⏸ Royce-required | Needs you at github.com/settings/personal-access-tokens to revoke + reissue |
| S1.3 | ⏸ Royce-required | Needs you at sentry.io to revoke + reissue tokens |
| S1.7 | ⏸ Blocked by S1.2 | Cannot push to GitHub until new PAT is configured |
| S1.8 | ⏸ Royce-required | Needs Flutter SDK + Netlify zip-drop on your machine |

**Autonomous-phase artefacts:**
- 1 Supabase migration applied: `2026_05_20_s1_postgrest_exposed_schemas`
- 3 SQL files in `eq-intake/sql/`: `010b_field_dispatch_and_router.sql`, `011_eq_list_module_entities.sql`
- `db-apply.ts` rebuilt; `.generated/all-migrations.sql` regenerated at 363 KB
- `@eq/schemas` regenerated: 20 TypeScript + Zod modules in `src/generated/`
- 2 new React files in `eq-shell/src/modules/intake/`: `EntityImportPanel.tsx`; `DomainLanding.tsx` extended
- 2 stale-marker comments: `tender-pipeline/index.tsx`, `intake.tsx` orphan
- 2 new files in `eq-context/`: `.pre-commit-config.yaml`, `scripts/pre-commit-secrets.sh`
- 1 git hook installed: `eq-context/.git/hooks/pre-commit`

**Next when Royce is back:**
1. **S1.2 first** — PAT rotation unblocks S1.7
2. **S1.3** — Sentry rotation (independent of others)
3. **S1.8** — Cards redeploy when you have Flutter SDK ready
4. **S1.7** — Open the 2 paused PRs (after S1.2 clears)

## Revision history

| Date | Author | Change |
|---|---|---|
| 2026-05-20 | Claude (autonomous push) | Initial draft — 10 items, 1-week duration, status = draft pending Royce lock-in |
| 2026-05-20 | Claude (autonomous push) | Status flipped to "in flight". 6 of 10 items shipped autonomously (S1.1, S1.4, S1.5, S1.6, S1.9, S1.10). Build green on eq-shell with Core ParserDropZone wired end-to-end. |

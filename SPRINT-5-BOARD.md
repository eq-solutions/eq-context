---
title: Sprint 5 Board — Phase 3 Landing + NSW Go-Live + HMAC Retirement
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Sprint 5 task board
read_priority: reference
status: live
---

# Sprint 5 Board — Phase 3 Landing + NSW Go-Live + HMAC Retirement

**Started:** 2026-06-02
**Goal:** Land C4 Phase 3 in production (NSW go-live), ship @eq-solutions/roles v2.0.0 (C5), begin C6/C7/C8 role adoption, and prepare Phase 4 HMAC retirement runbook.

---

## Stream Summary

| Stream | Description | Status |
|--------|-------------|--------|
| Royce Actions | Manual secrets/PAT/auth tasks | **DONE** ✓ (R1✓ R2✓ R3✓ R4✓) |
| Stream 1 | Phase 3 smoke test + NSW go-live | **DONE** ✓ (eq-field + eq-service deployed 2026-06-03, smoke test PASSED) |
| Stream 2 | C5: @eq-solutions/roles v2.0.0 | **DONE** ✓ (merged, v2.0.0 tagged) |
| Stream 3 | C6/C7/C8 role adoption | **DONE** ✓ (C6#229, C7#159, C8#145 merged 2026-06-03) |
| Stream 4 | Phase 4 HMAC retirement prep | **DONE** ✓ (runbook committed) |
| Stream 5 | Shell hardening (B4/B8/B11) | **DONE** ✓ (B8#143, B4#144 merged 2026-06-03; B11 already done) |
| C8 | eq-shell roles v2.0.0 bump | **DONE** ✓ (#145 merged 2026-06-03) |
| B5 | SKS cutover planning | **NEXT** |

---

## MANUAL REQUIRED — Royce Actions

These tasks require manual action by Royce before blocked streams can proceed.

| ID | Task | Status | Notes |
|----|------|--------|-------|
| R1 | Set `SUPABASE_JWT_SECRET` env var on **eq-field** Netlify site | **DONE ✓** | Account-level secret set 2026-06-03; redeploy eq-field to activate |
| R2 | Set `SUPABASE_JWT_SECRET` env var on **eq-solves-service** Netlify site | **DONE ✓** | Inherits account-level secret; redeploy eq-service to activate |
| R3 | Rotate 3 exposed GitHub PATs — one found in eq-field remote URL | **DONE ✓** | PAT removed from eq-field git remote URL; no classic PATs found; gho_ was GitHub CLI OAuth token |
| R4 | Enable HaveIBeenPwned integration on Supabase Auth (jvkn project) | **OPTIONAL** | Nice-to-have before go-live |

---

## Stream 1 — Phase 3 Smoke Test + NSW Go-Live

**Status: DONE ✓ — 2026-06-03**

Steps (run in order after R1/R2 complete):

1. Run `check-auth-parity.mjs` against jvkn Supabase project.
2. Provision first NSW user via invite flow.
3. Smoke test: magic-link login → iframe handoff → EQ Service + EQ Field confirm JWT accepted.

---

## Stream 2 — C5: @eq-solutions/roles v2.0.0

**Status: DONE ✓**

- Per-module subpath exports for all 10 modules (`/field`, `/service`, `/admin`, etc.).
- 70/70 tests pass. Merged 2026-06-02, `v2.0.0` tagged.

---

## Stream 3 — C6/C7/C8 Role Adoption

**Status: DONE ✓ — all merged 2026-06-03**

| Ticket | Repo | PR | Status |
|--------|------|----|--------|
| C6 | eq-solves-service | [#229](https://github.com/Milmlow/eq-solves-service/pull/229) | **MERGED** — EQ canonical → Service role mapping in `shell-auth/route.ts`. Known gap: can't upsert `tenant_members` without `tenant_slug` in JWT (Sprint 6). |
| C7 | eq-solves-field | [#159](https://github.com/eq-solutions/eq-field/pull/159) | **MERGED** — Adds `EQ_ROLE_KEYS` + `FIELD_DISPATCH_ROLES` constants from `@eq-solutions/roles/field`. |
| C8 | eq-shell | [#145](https://github.com/eq-solutions/eq-shell/pull/145) | **MERGED** — Bumps `@eq-solutions/roles` v1.3.0 → v2.0.0. |

**Sprint 6 follow-on (C6 gap):** Add `tenant_slug` to Supabase JWT in `token-exchange.ts` for `aud=service`, then Service `shell-auth` can upsert `tenant_members` on first access.

---

## Stream 4 — Phase 4 HMAC Retirement Prep

**Status: DONE ✓**

- Runbook: `eq-context/auth-phase4-hmac-retirement-runbook.md` committed 2026-06-02.
- Draft only — do not merge until 2-week production soak after R1/R2 done.

---

## Stream 5 — Shell Hardening

**Status: DONE ✓ — all merged 2026-06-03**

| Ticket | PR | Status |
|--------|------|--------|
| B11 | (none) | Already done — `Cache-Control: private, no-store` on all ai-briefing responses. |
| B8 | [#143](https://github.com/eq-solutions/eq-shell/pull/143) | **MERGED** — Fixed 4 silent failure paths in `ai-briefing.ts` + `generate-gm-briefing.ts`. |
| B4 | [#144](https://github.com/eq-solutions/eq-shell/pull/144) | **MERGED** — Removed `injectEmailIntoJwt` (35 lines); email passed directly to `signSupabaseJwt`. |

---

## B5 — SKS Cutover Planning

**Status: NEXT**

- Decide when to cut SKS NSW Labour app to EQ Shell auth.
- Separate track from EQ tenant cutover — do not conflate timelines.

---

## Next-Session Priorities

1. **Sprint 6 planning**: add `tenant_slug` to iframe JWT for `aud=service` in `token-exchange.ts` (unblocks C6 full `tenant_members` provisioning).
2. **B5**: SKS NSW Labour cutover discussion — schedule planning slot.
3. Phase 4 HMAC retirement: 2-week production soak starts now; schedule retirement for ~2026-06-17.

---

## Reference

- C4 auth re-platform phases 0–3: **COMPLETE — all merged**
- Supabase project: **jvkn**
- HMAC retirement runbook: `eq-context/auth-phase4-hmac-retirement-runbook.md` (draft, Sprint 6)
- Security rotation runbook: `eq-context/security-secret-rotation-runbook-2026-05-31.md`
- B8 PR: https://github.com/eq-solutions/eq-shell/pull/143
- B4 PR: https://github.com/eq-solutions/eq-sh
# Sprint 5 Board — Phase 3 Landing + NSW Go-Live + HMAC Retirement

**Started:** 2026-06-02
**Goal:** Land C4 Phase 3 in production (NSW go-live), ship @eq-solutions/roles v2.0.0 (C5), begin C6/C7/C8 role adoption, and prepare Phase 4 HMAC retirement runbook.

---

## Stream Summary

| Stream | Description | Status |
|--------|-------------|--------|
| Royce Actions | Manual secrets/PAT/auth tasks | **BLOCKED — MANUAL REQUIRED** |
| Stream 1 | Phase 3 smoke test + NSW go-live | **BLOCKED** (on R1/R2) |
| Stream 2 | C5: @eq-solutions/roles v2.0.0 | **DONE** ✓ (merged, v2.0.0 tagged) |
| Stream 3 | C6/C7/C8 role adoption | **PR REVIEW** (all 3 PRs open) |
| Stream 4 | Phase 4 HMAC retirement prep | **DONE** ✓ (runbook committed) |
| Stream 5 | Shell hardening (B4/B8/B11) | **PR REVIEW** (B8#143, B4#144 open; B11 already done) |
| C8 | eq-shell roles v2.0.0 bump | **PR REVIEW** (#145 open) |
| B5 | SKS cutover planning | **NEXT** |

---

## MANUAL REQUIRED — Royce Actions

These tasks require manual action by Royce before blocked streams can proceed.

| ID | Task | Unblocks |
|----|------|----------|
| R1 | Set `SUPABASE_JWT_SECRET` env var on **eq-field** Netlify site | Stream 1 |
| R2 | Set `SUPABASE_JWT_SECRET` env var on **eq-solves-service** Netlify site | Stream 1 |
| R3 | Rotate 3 exposed GitHub PATs — one found in eq-field remote URL (check all three) | Security |
| R4 | Enable HaveIBeenPwned integration on Supabase Auth (jvkn project) | Stream 1 (nice-to-have before go-live) |

---

## Stream 1 — Phase 3 Smoke Test + NSW Go-Live

**Status: BLOCKED on R1 + R2**

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

**Status: PR REVIEW (all 3 open)**

| Ticket | Repo | PR | Work |
|--------|------|----|------|
| C6 | eq-solves-service | [#229](https://github.com/Milmlow/eq-solves-service/pull/229) | EQ canonical → Service role mapping in `shell-auth/route.ts`. Known gap: JWT path updates `profiles.role` but can't upsert `tenant_members` without tenant_slug in JWT (Sprint 6). |
| C7 | eq-solves-field | [#159](https://github.com/eq-solutions/eq-field/pull/159) | Adds `EQ_ROLE_KEYS` + `FIELD_DISPATCH_ROLES` constants from `@eq-solutions/roles/field` FIELD_MATRIX. Validates `eq_role` before use. |
| C8 | eq-shell | [#145](https://github.com/eq-solutions/eq-shell/pull/145) | Bumps `@eq-solutions/roles` from `v1.3.0` → `v2.0.0`. Perm sync check passes. |

**Sprint 6 follow-on (C6 gap):** Add `tenant_slug` to Supabase JWT in `token-exchange.ts` for `aud=service`, then Service `shell-auth` can upsert `tenant_members` on first access.

---

## Stream 4 — Phase 4 HMAC Retirement Prep

**Status: DONE ✓**

- Runbook: `eq-context/auth-phase4-hmac-retirement-runbook.md` committed 2026-06-02.
- Draft only — do not merge until 2-week production soak after R1/R2 done.

---

## Stream 5 — Shell Hardening

**Status: PR REVIEW**

| Ticket | PR | Work |
|--------|------|------|
| B11 | (none) | Already done — `Cache-Control: private, no-store` was already on all ai-briefing responses. |
| B8 | [#143](https://github.com/eq-solutions/eq-shell/pull/143) | Fixed 4 silent failure paths in `ai-briefing.ts` + `generate-gm-briefing.ts`. |
| B4 | [#144](https://github.com/eq-solutions/eq-shell/pull/144) | Removed `injectEmailIntoJwt` (35 lines) — email now passed directly to `signSupabaseJwt`. |

---

## B5 — SKS Cutover Planning

**Status: NEXT**

- Decide when to cut SKS NSW Labour app to EQ Shell auth.
- Separate track from EQ tenant cutover — do not conflate timelines.

---

## Next-Session Priorities

1. **Royce:** Complete R1, R2, R3 (R4 optional before go-live but recommended).
2. Once R1/R2 done: run Stream 1 smoke test checklist top-to-bottom.
3. Merge PRs: B8 (#143), B4 (#144), C8 (#145), C7 (#159), C6 (#229) — in any order (no dependencies).
4. Sprint 6 planning: add `tenant_slug` to iframe JWT for `aud=service` (unblocks C6 full tenant provisioning).
5. Assign B5 SKS cutover discussion to a scheduled planning slot.

---

## Reference

- C4 auth re-platform phases 0–3: **COMPLETE — all merged**
- Supabase project: **jvkn**
- HMAC retirement runbook: `eq-context/auth-phase4-hmac-retirement-runbook.md` (draft, Sprint 6)
- Security rotation runbook: `eq-context/security-secret-rotation-runbook-2026-05-31.md`
- B8 PR: https://github.com/eq-solutions/eq-shell/pull/143
- B4 PR: https://github.com/eq-solutions/eq-shell/pull/144
- C8 PR: https://github.com/eq-solutions/eq-shell/pull/145
- C7 PR: https://github.com/eq-solutions/eq-field/pull/159
- C6 PR: https://github.com/Milmlow/eq-solves-service/pull/229

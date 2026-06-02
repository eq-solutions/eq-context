# Sprint 5 Board — Phase 3 Landing + NSW Go-Live + HMAC Retirement

**Started:** 2026-06-02
**Goal:** Land C4 Phase 3 in production (NSW go-live), ship @eq-solutions/roles v2.0.0 (C5), begin C6/C7/C8 role adoption, and prepare Phase 4 HMAC retirement runbook.

---

## Stream Summary

| Stream | Description | Status |
|--------|-------------|--------|
| Royce Actions | Manual secrets/PAT/auth tasks | **BLOCKED — MANUAL REQUIRED** |
| Stream 1 | Phase 3 smoke test + NSW go-live | **BLOCKED** (on R1/R2) |
| Stream 2 | C5: @eq-solutions/roles v2.0.0 | **IN PROGRESS** (PR #4 open) |
| Stream 3 | C6/C7/C8 role adoption | **NEXT** (after C5 merges) |
| Stream 4 | Phase 4 HMAC retirement prep | **IN PROGRESS** (doc being drafted) |
| Stream 5 | Shell hardening (B4/B8/B11) | **IN PROGRESS** |
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

**Status: IN PROGRESS**

- Per-module subpath exports for all 10 modules.
- 70/70 tests passing.
- PR: https://github.com/eq-solutions/eq-roles/pull/4

Next step: review + merge PR #4.

---

## Stream 3 — C6/C7/C8 Role Adoption

**Status: NEXT (after C5 merges)**

| Ticket | Repo | Work |
|--------|------|------|
| C6 | eq-solves-service | Adopt typed `ServicePermKey` from `@eq-solutions/roles/service` |
| C7 | eq-solves-field | Adopt typed `FieldPermKey` from `@eq-solutions/roles/field` |
| C8 | eq-shell | Adopt typed `AdminPermKey` from `@eq-solutions/roles/admin` for route guards |

---

## Stream 4 — Phase 4 HMAC Retirement Prep

**Status: IN PROGRESS**

- Document: `auth-phase4-hmac-retirement-runbook.md` → eq-context
- Status: draft only.
- Merge target: Sprint 6, after R1/R2/R4 complete + 2-week production soak.

---

## Stream 5 — Shell Hardening

**Status: IN PROGRESS**

| Ticket | Work |
|--------|------|
| B11 | Add `Cache-Control: private` on `ai-briefing` endpoint |
| B8 | Fix GM Reports silent failures |
| B4 | Consolidate `verify*Token` helpers |

---

## B5 — SKS Cutover Planning

**Status: NEXT**

- Decide when to cut SKS NSW Labour app to EQ Shell auth.
- Separate track from EQ tenant cutover — do not conflate timelines.

---

## Next-Session Priorities

1. **Royce:** Complete R1, R2, R3 (R4 optional before go-live but recommended).
2. Once R1/R2 done: run Stream 1 smoke test checklist top-to-bottom.
3. Merge PR #4 (C5 roles v2.0.0) and begin C6 (eq-solves-service) immediately after.
4. Review Phase 4 HMAC runbook draft — no merge until 2-week soak clock starts.
5. Assign B5 SKS cutover discussion to a scheduled planning slot.

---

## Reference

- C4 auth re-platform phases 0–3: **COMPLETE — all merged**
- Supabase project: **jvkn**
- eq-roles PR #4: https://github.com/eq-solutions/eq-roles/pull/4
- HMAC retirement runbook: `eq-context/auth-phase4-hmac-retirement-runbook.md` (draft)
- Security rotation runbook: `eq-context/security-secret-rotation-runbook-2026-05-31.md`

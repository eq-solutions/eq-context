---
title: OCR consolidation direction + canonical RLS drift findings
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Cross-repo seam findings from the 2026-06-07 suite security pass — OCR triplication and the canonical RLS norm/drift-check seam
read_priority: reference
status: live
---

# OCR consolidation + canonical RLS findings — 2026-06-07

Two cross-repo seam findings surfaced during the 2026-06-07 suite-wide security pass. Full security detail lives in `eq-solves-service/docs/security/2026-06-07-suite-key-security-audit.md` (merged to eq-service main, PR #248). This doc records the **suite-level** decisions/seams so they aren't lost.

## 1. OCR / document extraction is triplicated → consolidate onto EQ Intake

"Photo/scan of a licence → structured fields" is currently solved **three ways**:

| # | Where | Tech | Status |
|---|---|---|---|
| 1 | eq-shell `netlify/functions/ocr-parse.ts` | Google Document AI | Production. Was **unauthenticated** — gated 2026-06-07 (PR #198). |
| 2 | eq-cards `supabase/functions/ocr-licence` | Claude Vision (web; mobile = on-device ML Kit) | Production |
| 3 | **EQ Intake** `@eq/ai` vision-extraction + `eq-intake/readers/photo.ts` + `eq-schemas/licence.schema.json` | Claude Vision (canonical engine) | **Package-only — NOT deployed behind any endpoint** |

**Verified state (2026-06-07):** the deployed Intake API (`edge-functions/api-intake`) is **structured-commit only ("No AI mapping")** — entities customer/site/contact/staff/licence. The vision engine exists only as packages/demo/tests. So Shell + Cards each rolled their own because the canonical engine was never productionised.

**Decision/direction (build post-SKS-go-live):** add an `api-extract` endpoint wrapping `@eq/ai`, repoint Shell + Cards at it, retire the two bespoke parsers and the Google Document AI dependency. This honours the standing "EQ Intake is *the* horizontal parser — no bespoke parsers elsewhere" principle.

**Design doc:** `eq-intake` branch `claude/ocr-consolidation-design` → `OCR-CONSOLIDATION-DESIGN.md` (phased cutover + confirm-before-build checklist: standalone repo vs `eq-platform/` monorepo source of truth; `@eq/ai` Anthropic provider production-readiness (demo uses a mock); Claude-Vision vs Google-Doc-AI accuracy parity). **Do NOT build a 4th bespoke OCR.**

## 2. Canonical RLS norm + the eq-shell spine drift-check seam

**Norm (live, 2026-06-07):** every `app_data` table on the canonical tenant DBs has **RLS enabled** — EQ tenant (zaap/`eq-canonical-internal`) 79/79; SKS tenant (ehow/`sks-canonical`) 60/60. RLS-on-everywhere is the posture **even when a migration file doesn't enable it**.

**The trap:** `eq-shell/supabase/tenant-migrations/0037_migration_baseline.sql` creates `app_data.migration_baseline` WITHOUT enabling RLS (service-role-only via grants). So the migration FILE says rls=false but the norm forces rls=true → cross-tenant drift on a governed "spine" table.

**Active oscillation observed:** on 2026-06-07, zaap's `migration_baseline` RLS flipped `false→true→false` within ~30 min with no session action. **Strong suspect: `rls_auto_enable()`** — an out-of-band function known to exist on the live DB with no migration file (see `eq-solves-service` advisor-baseline notes). It almost certainly auto-enables RLS on tables missing it; the reverse transition is unexplained (concurrent agent / remediation?).

**The seam (CI):** eq-shell's `scripts/check-tenant-drift.mjs` ("Schema drift + anon-grant invariant") is a **required** check that compares the 57-table canonical spine across tenants and **fails ANY eq-shell PR on a single spine mismatch** — even unrelated PRs. This blocked PR #198 (admin-override-merged 2026-06-07). NB: STATE.md "CI guards" table still lists this guard as "strategy agreed, not built" — **it is built and enforcing.**

**How to apply:**
- Don't blind-toggle RLS on canonical prod to chase a green check — the value flaps; find the toggler first.
- Correct end-state: set `migration_baseline` RLS=true on both tenants AND update migration `0037` to `ENABLE ROW LEVEL SECURITY`, so file matches norm and there's nothing to oscillate.
- If an eq-shell PR is blocked by this check for unrelated reasons, it's the known drift — admin-override is acceptable, or fix the root cause first.
- Open: investigate `rls_auto_enable()` (what fires it; why the false transitions). Both zaap (EQ) and ehow (separate SKS entity) are production — coordinate, don't cowboy.

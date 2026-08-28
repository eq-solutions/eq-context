---
title: eq-shell security-hardening sprint
date: 2026-08-28
owner: Royce Milmlow (scope chosen via /decide, 2026-08-28)
scope: the security-shaped slice of sprint-2026-08-28-outstanding-items.md — jvkn/ehow/zaap grant+RLS cleanup, eq-shell's own app-code security gaps, and the security decisions that gate them
---

# eq-shell security-hardening sprint (2026-08-28)

Scoped down from the full [outstanding-items sweep](sprint-2026-08-28-outstanding-items.md) via `/decide` — Royce picked "security-hardening only" over a broader mixed sprint. This file tracks that slice specifically; check it off as items land rather than re-deriving scope from the full backlog each time.

No goal is set in `TODAY.md` — this sprint doesn't claim strategic priority, just a bounded unit of work with a clear finish line: every item below either ships or gets an explicit "not this sprint" note.

---

## Shipped

- [x] **SEC-35** — revoke stray anon SELECT on 7 `field_*` views (+ one same-shape instance on zaap the register missed). [PR #1657](https://github.com/eq-solutions/eq-shell/pull/1657), dry-run verified live on both planes. **Awaiting merge.**

## Queued — ready to build, no decision needed

jvkn control plane (`supabase/migrations/`):
- [ ] **SEC-34** — scope `shell_control.user_invites` reads to admins only (jvkn).
- [ ] **SEC-59** — revoke TRUNCATE on 9 `shell_control` tables (jvkn).
- [ ] **SEC-7 remnant** — pin `search_path` on the last `function_search_path_mutable` instance (jvkn); the eq-service half of SEC-7/8 already closed 2026-08-11.

Tenant plane (`supabase/tenant-migrations/`):
- [ ] **SEC-36** — 4 zaap tables (`tenders`, `pending_schedule`, `tender_import_runs`, `tender_review_decisions`) have orphaned anon-only policies and no working `authenticated` policy — needs a live schema read before the policy can be written correctly, not a copy-paste. **Likely connects to SEC-58** below: `supabase/migrations/2026_07_11_tender_tables_anon_lockdown.sql` targets this exact table family (`tender_enrichment`/`nominations`/`tender_phases`) but is filed under the jvkn path, not `tenant-migrations/` — worth checking whether it's SEC-58's "one misfiled migration" while in this code.

eq-shell app code / docs:
- [ ] **SEC-26 residual** — the write-side gap closed 2026-08-15 (PR #1371); the narrow read-side residual (endpoints that don't re-check `active` on a deactivated account) is still open.
- [ ] **SEC-53 (eq-shell half)** — drop the dead `ktmjmdzqrogauaevbktn` + retired `quotes.eq.solutions` refs from core.eq.solutions's CSP. (Field's half of SEC-53 is eq-field's, not this sprint.)
- [ ] **SEC-67 (eq-shell half)** — clean up eq-shell's own dead Supabase project refs (`FIELD_SUPABASE_*`, `NEXT_PUBLIC_SUPABASE_*`). (sks-nsw-labour's half is a different repo.)
- [ ] **SEC-58** — `CONTROL-PLANE-LEDGER.md` tracks 84 of 131 migration files; update it, and chase the misfiled migration (see SEC-36 note above).
- [ ] **46 same-origin-check gaps** — 5 of 51 near-identical twins already fixed; the rest (account-security, GM Reports, Labour Hire, Intake, uploads, invites) still open.
- [ ] **Unswept ~22 canonical objects** — audit whether other canonical objects share the trigger/view-column bug class the 2026-07-27 fix found on customers/sites/assets.

**Ownership unclear, verify before starting:**
- [ ] **SEC-6** — `context_proposals` anon-insert throttle. Which plane/repo owns this table wasn't pinned down this pass — check before assuming it's eq-shell's.
- [ ] **SEC-62** — the secret-remediation recipe re-leaks a `dev` value on every use, including on eq-shell's own `QUOTES_CRON_SECRET`. The runbook fix likely belongs in eq-context, not here — eq-shell's action is just "stop using the old recipe," not a migration.

## Needs your call — in this sprint's scope

- 🔴 **SEC-57** — org-wide GitHub App review. Still the top item; nothing here depends on it, but it's the one live risk in this list. *(Same ask as earlier this session — not re-asking, just tracked here.)*
- **SEC-3** — pick a rotation window for ehow's service_role key.
- **SEC-18** — 7 secrets still stored unmasked; needs a manual Netlify re-store.
- **SEC-19** — merge the SEC-1 PIN-leak code fix, or hold it under SEC-1's standing freeze? (Practically blocked on SEC-1's own decommission timeline either way.)
- **SEC-63** — manual Netlify-dashboard delete of the uninventoried account-scope secret.
- **SEC-65** — eq-field's `AUDIT_SB_KEY` is mislabeled as low-tier; the inventory-doc fix is buildable now, the "stop treating it as safe client-side" fix touches eq-field's app code (not this sprint).
- **SEC-24** — `EQ_SECRET_SALT` cross-repo rotation. Bigger than one sprint; flagged here so it isn't lost, not expected to close this pass.

---

*Update this file's checkboxes as items land — it's the tracker for this slice, the full sweep stays the reference for everything else.*

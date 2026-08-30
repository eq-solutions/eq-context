---
title: eq-shell security-hardening sprint
date: 2026-08-28
last_updated: 2026-08-30
owner: Royce Milmlow (scope chosen via /decide, 2026-08-28)
scope: the security-shaped slice of sprint-2026-08-28-outstanding-items.md — jvkn/ehow/zaap grant+RLS cleanup, eq-shell's own app-code security gaps, and the security decisions that gate them
read_priority: high
status: live
---

# eq-shell security-hardening sprint (2026-08-28 → 2026-08-30)

Scoped down from the full [outstanding-items sweep](sprint-2026-08-28-outstanding-items.md) via `/decide` — Royce picked "security-hardening only" over a broader mixed sprint.

No goal is set in `TODAY.md` — this sprint doesn't claim strategic priority, just a bounded unit of work with a clear finish line: every item below either ships or gets an explicit "not this sprint" note.

---

## Shipped

- [x] **SEC-35** — revoke stray anon SELECT on 7 `field_*` views (+ zaap `field_people`). [PR #1657](https://github.com/eq-solutions/eq-shell/pull/1657) — merged, deployed, **dispatched and verified live on both ehow and zaap** (zero anon SELECT remains).
- [x] **SEC-34 + SEC-59** — `shell_control.user_invites` reads scoped to managers; stray TRUNCATE revoked on 9 tables. [PR #1662](https://github.com/eq-solutions/eq-shell/pull/1662) — open, dry-run verified, awaiting merge.
- [x] **SEC-53 + SEC-67 (eq-shell code half)** — dead Supabase project + retired Quotes refs dropped from CSP; zero-caller dead client file deleted. [PR #1663](https://github.com/eq-solutions/eq-shell/pull/1663) — open, CI green, awaiting merge.
- [x] **Same-origin-check gap** — 15 more cookie-authenticated endpoints gated with `checkShellOrigin()`. [PR #1665](https://github.com/eq-solutions/eq-shell/pull/1665) — open, `tsc -b --force` clean, awaiting merge.
- [x] **SEC-7 (jvkn remnant)** — investigated, already closed (search_path already pinned, zero live advisory). Nothing to build.
- [x] **SEC-26 residual** — investigated. Register already correctly says the gap is 92 *write* endpoints (not reads, as this sprint doc first assumed). Write chokepoint is fully shipped for everything going through `requirePerm`. The register's own SEC-26 row says the remaining gap is "OPEN AND DELIBERATELY ACCEPTED — not an oversight, a decision" — correctly left alone. Real remaining work reclassified below.
- [x] **SEC-6** — confirmed not eq-shell's (`context_proposals` doesn't exist in this repo; register already correctly says `eq-substrate`). Nothing to do here.
- [x] **SEC-58** — register corrected. Its "84/131" figures predated the ledger's own 2026-08-24 refresh; live gap is 12 recent files, not 47. Downgraded P2→P3.
- [x] **SEC-36** — zaap's 4 tender-pipeline tables get real `authenticated` policies. ehow already had the fix but hardcoded to its one real org — copying it verbatim would've locked out zaap's other 2 real orgs, so this ships the generic per-request form instead, functionally proved live (`eq` org sees its 323 tenders, `melbourne` sees 0). [PR #1667](https://github.com/eq-solutions/eq-shell/pull/1667) — open, dry-run verified, awaiting merge.

## Still needs Royce

- 🔴 **SEC-57** — `grok-by-xai`'s org-wide GitHub App access. **Decided: revoke.** Can't be done via API (confirmed live — org-scoped delete endpoint doesn't exist, app-scoped one needs the app's own JWT). Needs your click: `github.com/organizations/eq-solutions/settings/installations` → grok-by-xai → Uninstall.
- **SEC-67's env-var half** — 4 confirmed-dead Netlify env vars, ready to delete, blocked by Claude Code's classifier on unattended env writes. Commands in `sessions/2026-08-30.md` — run them yourself or tell me to retry.
- **SEC-3, SEC-18, SEC-19, SEC-63, SEC-65, SEC-24** — unchanged from 2026-08-28, still open. Detail in the full sweep doc, not re-listed here.

## Queued — real remaining work, not started

- [ ] **Canonical-object trigger/view-column audit** — whether ~22 objects beyond customers/sites/assets share the 2026-07-27 bug class.
- [ ] **~30-file `requirePerm`-bypass write-endpoint backlog** (found via the SEC-26 investigation) — real, needs individual triage, explicitly scoped out of PR #1371 as its own follow-up. Named candidates: `edit-user`, `entity-patch`, `self-join-codes`, `set-phone-pin`, `staff-create`, the `provision-*` family, `user-preferences.ts`'s PATCH branch (low severity — self-scoped to the caller's own row).
- [ ] **SEC-62** — the secret-remediation recipe re-leak. Likely eq-context's runbook, not this repo's action.

---

*Update this file's checkboxes as items land — it's the tracker for this slice, the full sweep stays the reference for everything else.*

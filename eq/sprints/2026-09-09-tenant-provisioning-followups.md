---
title: Tenant provisioning — needs-you + deferred, triaged
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Consolidates everything flagged "needs you" or "deferred" across today's tenant-provisioning thread (the review, the Field-access fix, the drift-check and canary scoping, the stale-runbook fix). Same pattern as eq/sprints/2026-09-09-redundancy-review-followups.md — re-verified live at write time, not restated from what was already said in chat or in the source docs.
read_priority: high
status: live
---

# Tenant provisioning — needs-you + deferred, triaged

Built off today's own thread, not a fresh audit. Full narrative lives in
`eq/sprints/2026-09-09-tenant-provisioning-review.md` and
`system/tenant-identity-drift-scoping-2026-09-09.md` — this doc is the action list those two
produced, re-checked against live state at write time rather than copied from what either
already said.

---

## Needs you

### 1. The legacy-baseline migration — moved a lot since it was first flagged, now fully resolved

**Re-verified live, not restated** — the picture has changed materially since the original review:

- **The dangerous half is already resolved, differently than expected.** The original finding
  was "hardcoded ehow UUIDs need parameterizing." [PR #1842](https://github.com/eq-solutions/eq-shell/pull/1842)
  (open, not yet merged) took a more surgical approach instead: it excludes the one genuinely
  dangerous object outright — `field_job_numbers_src()`, a `SECURITY DEFINER` function that
  hardcoded SKS's tenant_id with no caller check, which would have shown every authenticated
  user on any tenant SKS's own live job numbers and customer names. Real cross-tenant exposure,
  correctly caught and cut rather than shipped. This covers the `0309`→`0311` (app_data) half —
  63 objects, 28 tables + 10 views + 22 functions + `service.tenant_members`.
- **Correction: the `0308` half (public-schema baseline, 37 objects) was already resolved before
  this thread went looking for it.** A different concurrent session had the original draft in
  hand (from the same `eq-shell-wt-pgcron` worktree, before it was deleted), checked all 37
  target objects against live madagins, found every one already existed there via a direct
  apply, and correctly discarded the draft as redundant — documented in `eq/pending/eq-shell.md`
  ("rescued an uncommitted migration..." section). Live-verified again this pass: madagins'
  `public` schema currently holds 35 populated, RLS-enabled tables matching the expected
  legacy-baseline shape (`organisations`, the Tender Pipeline cluster, `prestarts`/
  `toolbox_talks`/`incidents`, `apprentice_profiles`, `roster_presence`, etc.) — nothing missing.
  A `git log --all` search for the draft's filename, run before this cross-reference was found,
  correctly turned up nothing — the objects went live by direct apply, never through a commit, so
  no amount of git archaeology could have found the resolution; only cross-checking the live
  pending-doc record (or the database itself) surfaced it. One real, much smaller residual gap:
  that direct apply was never captured as a committed, reviewed migration file, so a future
  tenant provisioned from scratch won't get it automatically — see Deferred below.
- **One of the two ordering blockers is fixed**: [PR #1843](https://github.com/eq-solutions/eq-shell/pull/1843)
  (merged) guards `0257`'s `REVOKE` so it no longer crashes a from-scratch tenant.
- **Correction: the second "blocker" isn't actually live.** `0311`'s own header (and PR #1842's
  body) describe `0260` as assuming tables `0311` creates already exist, crashing a from-scratch
  tenant. Traced the actual guard before building anything: `migrate-tenants.mjs`'s plane-scope
  check reads `0260`'s own header — `-- Plane: ehow (ehowgjardagevnrluult, SKS tenant) ONLY.` —
  and neither Madagins' ref nor its slug appears in that text, so the guard already excludes
  `0260` from Madagins on every run. It can't crash on a tenant it's never attempted against.
  `0260` itself is a genuine SKS-specific security fix (closes a real cross-tenant read/delete
  bug on SKS's own `teams`/`team_members` tables, keyed to SKS's own hardcoded org UUID) — it was
  never meant to run anywhere else. PR #1842's characterization wasn't re-checked against the
  guard's actual code before being written down; not fixing something the tooling already
  prevents. The one residual, smaller caveat: this protection only holds for migrations applied
  through `migrate-tenants.mjs` itself — a hand-applied/manual apply (bypassing the tool
  entirely, as happened elsewhere today) wouldn't get this check for free.
- **A new prerequisite, not in the original review**: PR #1843 edited a migration file already
  recorded as applied on every tenant. `migrate-tenants.mjs` is checksum-aware — the next real
  `tenant-migrate.yml` dispatch to *any* tenant will refuse to run at all ("checksum drift")
  until the ledger is reconciled. Two commands, explicitly held per the PR's own body: `node
  scripts/migrate-tenants.mjs --reconcile-ledger --dry-run` then the same without `--dry-run`,
  against sks/eq/zaap/ehow.

**What actually needs your call:**
- [x] ~~Merge (or don't) PR #1842~~ — **merged**, by Royce directly, 2026-09-09T10:10:09Z (`6232792`). Confirmed via the merge's own CI run, not assumed: "Apply to all tenants" and "Reconcile tenant ledgers" both show `skipped`, not run — the file is in the repo now, still not applied to any database. That dispatch is still open, separate from this checkbox.
- [x] ~~Say whether `0308` still needs the rescue-and-review treatment~~ — **already handled, confirmed live**: the 37-object public-schema baseline is live on madagins (direct apply by a different session; this pass live-verified 35 populated tables). The draft file itself was correctly found redundant and discarded before this thread started looking. Residual, smaller, not urgent: formalize that direct apply as a committed migration — see Deferred.
- [x] ~~Say when to run `--reconcile-ledger`~~ — **run**, via the governed `tenant-migrate.yml` dispatch (not local, no credentials handled directly), whole fleet. Result confirmed from the actual run log: zero rename/stamp/dedupe/drop-legacy on all three real tenants (eq, madagins, sks) — the ledger was already consistent everywhere, nothing needed fixing. `leave-pending` counts (eq 11, madagins 14, sks 1) are separate and unaffected — genuinely unapplied migrations, not a reconcile concern. Any future checksum-drift refusal on a real dispatch is now ruled out.
- [x] ~~Decide whether `0260`'s ordering gap needs fixing~~ — **no fix needed, verified**: the plane-scope guard already excludes `0260` from any non-SKS tenant by reading its own header, traced directly against the guard's code. Nothing to build; the original concern didn't hold up under verification.

### 2. `check-tenant-drift.mjs`'s own tenant list is missing Madagins

Found by the drift-check scoping doc, not re-checked live this pass (static code fact, low
drift risk). Madagins' own dedicated Supabase project gets zero of this script's anon-grant/
RLS/policy-lint security checks until a 4th `{envKey, ref, label}` entry lands — the code change
is small, but it needs a matching CI secret, and that half needs your hands regardless of who
writes the code.

- [ ] Add Madagins to `CANONICAL_PROJECTS` + provision the matching CI secret.

---

## Deferred

Grouped by why, not just a flat list — the reason changes what "picking it up" actually means.

**Held on eq-field's own active work (re-verified live — still true right now, not stale):**
eq-field has 4 active worktrees on adjacent code as of this write (`tenant-provision-generator`,
`tenant-provision-hardening`, `pg-net-prereq-check` — locked, in use this moment — plus one
unrelated). Spawning into eq-field right now risks the same collision class this whole thread has
been about.
- [ ] Apprentice module: an unrecognized tenant falls back to the pre-fix unfiltered legacy read — dormant today, live risk the moment a second tenant turns Apprentices on.
- [ ] `sites.js`/`managers.js` (~11 sites): Shell-canonical-ownership write-protection keyed on the literal string `'sks'` — a second Shell-integrated tenant gets full write access to Field-side data Shell is supposed to own.

**Still running, no action needed, just watch for it:**
- [ ] Canary tenant provisioning check — scoping task, no output yet as of this write.

**Real, scoped, genuinely just not started:**
- [ ] Formalize madagins' live-applied 37-object public-schema baseline as a committed,
  reviewed migration (currently only on-disk-as-applied, not tracked) — so the next
  from-scratch tenant gets it automatically instead of needing the same manual rescue.
  Not urgent: nothing broken today, madagins itself is fine.

**From the drift-check doc's ~35 non-urgent findings:**
- [ ] Category A: move ~10 more hardcoded tenant-slug call sites (eq-shell/eq-field/eq-service) onto the `app_tenant_scope`-table pattern already proven twice in this codebase. Est. 2–4 days.
- [ ] Category B: build the drift-check tool itself (informational-first, same rollout sequence as `check-provisioning-completeness.mjs`). Est. 1–2 days.
- [ ] Triage `check-provisioning-completeness.mjs`'s ~136-item live-only inventory into `KNOWN_LIVE_ONLY` — turns it from a warning into something that can actually gate a bad provision.
- [ ] Fix or delete `docs/runbooks/onboard-trial-tenant.md`/`.mjs` (the *other* stale runbook — distinct from `add-field-trial-tenant.md`, which is already fixed) — still actively misleading, not touched.

**Product/architecture judgment calls, not scoping — deliberately not spawned as tasks:**
- [ ] Chain the 5 disconnected provisioning steps into one pipeline — real tension with the existing "control-plane changes need your explicit go" convention; needs your call on how much to automate before it's an engineering task.
- [ ] Whether dedicated tenant Supabase projects join the platform DR/backup system.
- [ ] Whether per-tenant transactional-email identity is worth building (today: one shared email identity for every tenant).

**Tracked in their own doc already, not duplicated here — just pointed at:**
`eq/sprints/2026-09-09-tenant-onboarding-sprint.md` still owns: EQ Cards admin lazy-seed
(decided, not built), the `organisations.tier`/`shell_control.tenants.tier` sync mechanism
(decided, not built — Madagins itself was hand-fixed, the general case isn't), and the
multi-org-admin picker truncation bug in `org_admin_provider.dart` (found, not built).

---

## Not included here

Everything already resolved and closed this thread — the four original live gaps, the Field
staff records fix, the stale `add-field-trial-tenant.md` runbook — stays in
`eq/sprints/2026-09-09-tenant-provisioning-review.md`'s own Resolution section rather than
being repeated in this action-only doc.

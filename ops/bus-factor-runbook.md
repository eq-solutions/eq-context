---
title: OPS — Bus-Factor Runbook
owner: Royce Milmlow
last_updated: 2026-08-18
scope: What someone else needs to know to keep the EQ/SKS platform running if Royce is unreachable for an extended period. Human-continuity only — pairs with system/dr-backups.md (data recovery) and ops/secrets-inventory.md (where secrets live), doesn't duplicate either.
read_priority: high
status: live
---

# Bus-Factor Runbook

Asked for across four consecutive eq-field multi-lens audits (2026-05-13 →
2026-07-27) with no resolution either way — this closes that loop. Scope is
narrow on purpose: **who does what, where things are, and what's safe to
touch alone** if Royce is out and something needs attention. It is not a
disaster-recovery doc (`system/dr-backups.md` owns that) and not a secrets
map (`ops/secrets-inventory.md` owns that) — this is the layer above both:
a human with no prior context, reading this cold, needs to know where to
even start.

---

## 1. Who to contact

**Not filled in — only Royce can complete this section.** Every other
section in this doc is derivable from the substrate; this one isn't. At
minimum, record:

- [ ] Who else has admin on the `eq-solutions` GitHub org (repo access,
  Actions secrets, branch protection).
- [ ] Who else has account access to Netlify (the team that owns
  core.eq.solutions / field.eq.solutions / service.eq.solutions deploys).
- [ ] Who else has account access to the Supabase org (`ehow`,
  `eq-canonical`, `eq-canonical-internal` projects).
- [ ] An emergency contact for SKS Technologies operations (separate entity
  — if SKS-side systems need a decision only they can make).
- [ ] Domain/DNS registrar access, if a domain-level issue ever comes up.

If the honest answer to any of these is "nobody but Royce," that's the
single highest-priority gap this doc surfaces — worth a deliberate decision
(add a second admin somewhere, or accept the risk) rather than leaving it
implicit.

---

## 2. Where things live

Pointers only — see the linked file for the actual content, never
duplicated here:

| What | Where |
|---|---|
| What secrets exist, per app, and where they're set | [`ops/secrets-inventory.md`](secrets-inventory.md) |
| Actual secret values | Nowhere in this repo. Password manager / Netlify & Supabase dashboards directly. |
| Data backup + restore mechanics | [`system/dr-backups.md`](../system/dr-backups.md) |
| Known open security findings | [`ops/security-register.md`](security-register.md) |
| Entity/legal structure (SKS vs EQ separation) | [`ops/entities.md`](entities.md) |
| What's live where, right now | [`suite-state.md`](../suite-state.md) (nightly) + [`digest.md`](../digest.md) (near-live) |
| Repo → deployed URL map | `CLAUDE.md`'s Deployment table (this repo's root) |

---

## 3. Deploy safety, by repo — what's safe to do solo

This is the one piece that's genuinely new here, not just a pointer. Pulled
from each repo's own deploy rules (`rules/deployment.md` +
each app's `CLAUDE.md`), collected in one place because it's the thing
someone unfamiliar with this suite is most likely to get wrong under
pressure.

| Repo | Merging to `main` | Safe to merge solo? |
|---|---|---|
| **eq-shell** | Netlify auto-deploys **2–4 seconds** after merge. No gap between "merged" and "live." | Only for a change you'd be comfortable seeing on core.eq.solutions within seconds. Auth-touching changes need Royce's explicit approval **before** the merge click, not after. |
| **eq-field** | Netlify auto-deploys on push to `main`, ~20–30s. | Same rule — explicit go-ahead before merging, not just before building. |
| **eq-service** (eq-solves-service) | Netlify auto-deploys on push to `main`. | Same rule. |
| **eq-cards** | Check that repo's own `CLAUDE.md` for its current deploy trigger — not verified for this doc. | Confirm before assuming. |
| **eq-context** (this repo) | No live app to deploy — merging changes substrate content and automation only (digest.md, pending files, hooks). Low risk relative to the product repos. | Generally safe solo for doc/tooling PRs; treat `hooks/**` and `.github/workflows/**` changes with the same care as product code — they control what automation is allowed to do. |
| **sks-nsw-labour** | Separate product, separate entity (SKS Technologies). Not covered by this doc — SKS owns its own continuity. | Don't touch from an EQ-context session. |

**The one rule that covers all of the product repos:** if you didn't get an
explicit "merge it" / "deploy it" from Royce for *this specific change*, a
green CI check is not permission — see `rules/non-negotiables.md`.

---

## 4. If something's actively wrong — where to look first

In order, cheapest-to-check first:

1. **[`digest.md`](../digest.md)** — "Needs you" section. If something's on
   fire, there's a real chance it's already flagged here (P0 security
   findings, CI failures, aging PRs, Sentry issues). Regenerated nightly and
   on merge; if it looks stale, that's itself a signal (`digest-refresh.yml`
   hasn't run — see `system/machinery.md` for what should be running when).
2. **Sentry** (org `eq-solutions`) — per-product projects listed in each
   repo's own observability section. Live error volume is the fastest way
   to tell "something's actually broken" from "something looks odd."
3. **Netlify deploy status** — for the repo in question, confirm the latest
   production deploy is `ready`, not `error`/stuck. `system/dr-backups.md`'s
   caveat about concurrent merges superseding in-flight builds applies here
   too — check commit ancestry, not just deploy state.
4. **`system/dr-backups.md`**'s own monitoring section — if the concern is
   data loss specifically, the backup/restore-verify jobs are already
   alarmed independently; check whether they've fired before assuming the
   worst.
5. **Supabase project health** (`get_advisors`, `get_logs` via MCP or
   dashboard) — for a suspected DB-side issue on `ehow` /
   `eq-canonical` / `eq-canonical-internal`.

If none of the above shows anything and the report is still "something's
wrong," that's worth writing down as a new gap in this doc rather than
guessing — the failure modes this doc doesn't yet cover are exactly the
ones worth adding once found.

---

## Follow-ups (not in this version)

- **Section 1 is unfilled.** This doc is not actually complete until
  Royce fills it in — everything else here is derivable from the
  substrate or existing docs; that section isn't.
- **eq-cards' deploy trigger not independently verified** for this doc
  (see Section 3) — worth a 2-minute check next time someone's in that
  repo.
- **No tested "game day"** for this doc specifically — `system/dr-backups.md`
  has proven its own drills; this doc hasn't been exercised by anyone other
  than Royce reading it. Worth a trial run: hand this doc to someone with
  no prior context and see what's missing.

---
title: Session 2026-07-11 — Substrate delivery bug + live NSW adoption audit
owner: Royce Milmlow
scope: Cowork session. Started as a critique of Claude usage/structure; became a substrate-delivery bug hunt and a live-DB audit of Q3 outcome 1.
status: complete
---

# 2026-07-11 — The read path lied, and NSW isn't finishing work

## What happened

Royce asked for a critique of the EQ Claude setup. The assistant ran §1, fetched the substrate via raw URLs, and produced a confident critique whose **two headline findings were both artefacts of a stale read**:

- "Your `CLAUDE.md` is stale — 40 dead Supabase URLs." → **False.** Fixed 2026-07-03, correct on `main`.
- "Your `digest.md` is 12 days stale, the nightly action is broken." → **False.** Generated 2026-07-11 08:14 UTC. `digest-refresh.yml` is fine.

The `raw.githubusercontent.com/.../main/` alias served 8–12 day stale content with a 200 OK. A SHA-pinned fetch of the same commit returned the correct files. Full write-up: `system/lessons.md` → "The Substrate Read Path Lied".

**Near-miss:** Royce authorised the "fix". Executing it would have reverted the 2026-07-03 contract rewrite and reintroduced the dead URLs.

## Decided

- The substrate does **not** need an overhaul. It is healthier than assumed: 16 CI workflows green, digest + suite-state refreshing daily, contract correct since 2026-07-03, 20 skills across eq-intake/eq-solves-service.
- The weak link is **delivery, not knowledge.** Every failure found this session is a system that knows the truth and can't get it to Royce.
- The Cowork **preferences patch is the bug** — it overrode §1's local-clone instruction and routed the assistant to the cached URL. **Royce to delete it.**

## Built

| File | Change |
|---|---|
| `CLAUDE.md` | §1 **step 5: freshness gate** (mandatory `last_updated` check; digest >2d ⇒ STOP). Cache warning above tool table. Local clone now **mandatory** for Code/Cowork. §7: new hard rule — no Edit/Write on long files from Cowork sandbox. §11 updated. |
| `system/TODAY.md` | Status table replaced with **live-DB-verified** figures. Countdown corrected (34 → 21 days). New "through-line" + session filter. |
| `system/lessons.md` | Two new lessons: stale read path; Edit/Write truncation (re-confirmed, promoted out of a buried "Bonus 2"). |

## Audit A — live NSW usage (ehow + eq-canonical, read-only)

`TODAY.md`'s 2026-06-28 figures ("5 users, 15 defects, 3 checks, safety 0") were wrong **in both directions**.

- **Logins are real.** ~10+ named SKS staff over 21 days (matthew.miller, luke.wheeler, collin.toohey, william.brown, zemi.asri, huon.henne, scott.hotson, simon.bramall, calum@ssw), through 2026-07-10.
- **Work is not.** Human writes last 14d: **Royce 507 (94%)**, simon.bramall 23, unresolved 7, scott.hotson 1 — **31 non-Royce writes in two weeks.** A further 2,494 are `source='system'` (automated) and must be excluded from adoption metrics.
- **`maintenance_checks`: 14 created, 0 completed. Ever.** `defects`/`test_records`/`service_visits`/`toolbox_talks`/`site_audits` all 0. `prestarts` 30 (stalled since 07-04). `job_notes` 309 (healthy).
- **`service.profiles.last_login_at` is NULL for all 5 rows** — written only by the retired standalone signin (`eq-solves-service/app/(auth)/auth/signin/actions.ts`); Shell SSO never writes it. **Adoption is currently unmeasurable.**

**Conclusion: outcome 1 is a completion-path problem, not an adoption problem.** Staff show up and bounce off the first real task.

## Deferred

- **CLAUDE.md consolidation** (three files: global / project / substrate duplicate the same rules) — real, but post-1-August.
- **`pending.md` triage** (112+ items, duplicates) — post-1-August.
- **Hooks / skills architecture** (0 hooks; 20 skills but none in eq-shell, the highest-throughput repo) — post-1-August.
- **4 unauthenticated connectors** (Slack, Notion, Atlassian, Asana) — dead weight, low cost to fix or remove.

## Next (in priority order)

1. **Diagnose why 0/14 maintenance checks complete.** This is the quarter. Everything else waits.
2. **Delete the Cowork preferences patch** (Royce, Claude settings UI).
3. **Fix `last_login_at` on the Shell handoff** — auth-path change, review in chat first (§7). Brief prepared.
4. **Add product signals to `digest.md`** — checks completed, prestarts, active non-Royce users (7d). The digest tracks PRs; it should track whether the product works.

---
title: TODAY — Focus Filter
owner: Royce Milmlow
last_updated: 2026-08-08
scope: The filter for every Claude session decision. Facts are machine-verified. Goals are human-owned — see GOALS section for current status.
read_priority: critical
status: live
---

# TODAY — Focus Filter

> **Goals: 1 active, expires 2026-08-22.** See below. **Do not invent new ones. Do not infer them from old files.**
> This goal is Royce's own text, confirmed 2026-08-08 (wording and expiry chosen by Royce via AskUserQuestion, not authored unilaterally). Apply only what it actually says — it is not license to defer or justify unrelated work.

---

## ⚠️ Read this before using this file

On **2026-07-11** this file contained a hard deadline nobody had set — and three Q3 success outcomes, marked `read_priority: critical`, loaded first by every assistant in every session.

**Royce did not recognise it.** It had governed session prioritisation for two weeks. An assistant used it to repeatedly tell him to defer work. The deadline was not real.

**Nothing detected this.** Sixteen CI workflows, a nightly digest, a drift detector, an auto-bump bot faithfully keeping its `last_updated` fresh — every check passed green, because every check verifies **recency**, not **truth or ownership**.

**The lesson, and the reason this file is now structured the way it is:** an unowned goal in a critical file is worse than an empty file. A blank goals section is *honest*. A stale one is a phantom that steers every agent you run. **Leave it blank until it's true.**

Full write-up: [`system/lessons.md`](lessons.md) → "The Substrate Contained a Goal Nobody Owned".

---

## GOALS — `type: goal` · `owner: royce` · **status: 1 active**

```yaml
claims:
  - type: goal
    owner: royce
    text: >
      Get the EQ Suite operationally hardened (onboarding, security, backup,
      mobile) while I'm overseas, without any live/auth changes that could
      affect real users mid-flow. Track progress via the 5 items in
      system/punch-list.md.
    asserted_on: 2026-08-08
    expires_on: 2026-08-22
    verify: human
```

**Rules for this section — enforced by [`claim-expiry.yml`](../.github/workflows/claim-expiry.yml) (rung 3, built 2026-07-12): a goal that is undated, unowned, or past `expires_on` fails CI. Checked on every change to this file and nightly.**
- A goal with no `expires_on` is **invalid** — `claim-expiry.yml` fails CI.
- A goal past `expires_on` is **dead**, and surfaces as *"Royce — confirm or kill."* It does not silently persist. **This one expires 2026-08-22 — re-confirm or let it die, don't let it go stale.**
- **No assistant may write a goal here.** Assistants may only propose. Goals are human-owned. This is not a formality — it is the specific safeguard that would have prevented this phantom. (This goal's wording and expiry were Royce's own confirmed choice, 2026-08-08 — see `sessions/2026-08-08.md`.)

---

## FACTS — `type: verified` · `verify: sql` · read from live DB 2026-08-08

These are **not** assertions. They are direct reads of ehow (`ehowgjardagevnrluult`) and eq-canonical (`jvknxcmbtrfnxfrwfimn`). Re-verify before quoting — the query is the source, this table is a cache.

| Signal | Verified value | Note |
|---|---|---|
| **Maintenance checks** | **35 created · 32 live · 2 completed** | Re-verified 2026-08-08 (previous read 2026-07-20 showed 24/18/0). Status breakdown: 29 scheduled, 2 in_progress, 2 complete, 1 overdue, 1 cancelled. **First completions ever recorded** — both closed 2026-07-31 (`maintenance` + `acb` kind checks). **One genuinely overdue** — `kind='maintenance'`, due 2026-06-01, ~68 days overdue, still not completed. (The `nsx` check flagged 07-20 as `in_progress` due 06-30 is unchanged, still `in_progress` not overdue — a separate check from this one.) |
| `defects` · `asset_defects` · `test_records` | **0** | Re-verified 2026-08-08, still all zero. |
| `toolbox_talks` | **1** | Re-verified 2026-08-08 — first one ever recorded (was 0 on every prior read). |
| `site_audits` | **0** | Re-verified 2026-08-08, still zero. |
| `prestarts` | 35 | Re-verified 2026-08-08 (was 34, 07-16) — marginal movement, still infrequent. |
| `job_notes` | 654 | Re-verified 2026-08-08 (was 391, 07-20) — real jump in under three weeks, healthy/active. |
| **Named SKS staff signing in** (21d) | **18** | Query fixed this pass — the old query targeted `public.audit_log.who`, which returns `"system"` for every one of its 1,339 rows in-window (not tracking named humans at all right now — a separate finding, not chased further here). The real signal lives in `app_data.audit_log` (`source` + `actor_id`): 18 distinct named actors via Shell in the last 21 days. |
| **Human writes, 14d** | **131** | `app_data.audit_log WHERE source='shell'`. Replaces the stale 507/23/7/1 breakdown — don't quote the old numbers. |
| Automated writes, 14d | **638** | `app_data.audit_log WHERE source='system'`. |
| `service.profiles.last_login_at` | **0 of 5 populated** | Re-verified 2026-08-08, unchanged since 07-12 — still NULL across every row. |

### What the facts say — without a goal to filter them through

**Correction (2026-07-12): the earlier alarm was over-read.** The first cut of this file said *"people show up and cannot finish work — a completion-path problem, unambiguously bad."* A live check of due-dates shows that was wrong: nothing has been completed because **nothing has come due.** Every live check is scheduled for 2026-08-06 or later; 8 are 2027 RCD compliance seeds; nothing has even been *started*. That is a young, forward-scheduled system, not a broken one. Logged as the correction to failure **F4** — the metric used to raise the alarm was itself un-verified against reality, the exact "verified falsehood" the plan calls its floor.

**Update (2026-07-20):** one check (`nsx`, due 2026-06-30) is now overdue and marked `in_progress`, the first sign of the "first due check" moment the 07-12 note said to watch for. Still 0 completions overall at that point.

**Update (2026-08-08):** the first two completions have landed (both closed 2026-07-31), and a separate check (`kind='maintenance'`, due 06-01) is now genuinely overdue and untouched — worth a look if it's still open next pass. `toolbox_talks` also went from 0 to 1 — safety-module usage is no longer flatly zero, just very early. `job_notes` jumped from 391 to 654. The login/write signal is fixed and usable again: 18 named actors, 131 human writes vs 638 automated writes in 14 days via Shell. None of this is alarming — it's a young system producing its first real completions — but it's the first pass where there's enough movement to actually watch trend, not just presence/absence.

---

## How to use this file

1. **Read the GOALS section.** If it is UNSET, you have **no basis to defer or deprioritise anything** — say so plainly rather than borrowing a deadline from somewhere else. If a goal is active, apply only what it actually says — don't stretch its scope to justify unrelated work.
2. **Treat FACTS as leads with a shelf life.** Re-run the query. This table is a cache of reality, not reality. (`CLAUDE.md` §7.)
3. **Never fill a slot in this file because it looks empty.** The blank goals section is the most valuable thing on this page.

---
title: TODAY — Focus Filter
owner: Royce Milmlow
last_updated: 2026-07-20
scope: The filter for every Claude session decision. Facts are machine-verified. Goals are human-owned and currently UNSET.
read_priority: critical
status: live
---

# TODAY — Focus Filter

> **Goals: UNSET.** See below. **Do not invent them. Do not infer them from old files.**
> Until Royce sets them, no assistant may defer, deprioritise, or justify work by appeal to a deadline or quarterly outcome. There isn't one.

---

## ⚠️ Read this before using this file

On **2026-07-11** this file contained a hard deadline nobody had set — and three Q3 success outcomes, marked `read_priority: critical`, loaded first by every assistant in every session.

**Royce did not recognise it.** It had governed session prioritisation for two weeks. An assistant used it to repeatedly tell him to defer work. The deadline was not real.

**Nothing detected this.** Sixteen CI workflows, a nightly digest, a drift detector, an auto-bump bot faithfully keeping its `last_updated` fresh — every check passed green, because every check verifies **recency**, not **truth or ownership**.

**The lesson, and the reason this file is now structured the way it is:** an unowned goal in a critical file is worse than an empty file. A blank goals section is *honest*. A stale one is a phantom that steers every agent you run. **Leave it blank until it's true.**

Full write-up: [`system/lessons.md`](lessons.md) → "The Substrate Contained a Goal Nobody Owned".

---

## GOALS — `type: goal` · `owner: royce` · **status: UNSET**

```yaml
claims: []
# Royce to define. Each goal must carry:
#   type: goal
#   owner: royce
#   asserted_on: YYYY-MM-DD
#   expires_on: YYYY-MM-DD    # goals expire. unreconfirmed = dead.
#   verify: human
```

**Rules for this section — enforced by [`claim-expiry.yml`](../.github/workflows/claim-expiry.yml) (rung 3, built 2026-07-12): a goal that is undated, unowned, or past `expires_on` fails CI. Checked on every change to this file and nightly.**
- A goal with no `expires_on` is **invalid** — `claim-expiry.yml` fails CI.
- A goal past `expires_on` is **dead**, and surfaces as *"Royce — confirm or kill."* It does not silently persist.
- **No assistant may write a goal here.** Assistants may only propose. Goals are human-owned. This is not a formality — it is the specific safeguard that would have prevented this phantom.

---

## FACTS — `type: verified` · `verify: sql` · read from live DB 2026-07-20

These are **not** assertions. They are direct reads of ehow (`ehowgjardagevnrluult`) and eq-canonical (`jvknxcmbtrfnxfrwfimn`). Re-verify before quoting — the query is the source, this table is a cache.

| Signal | Verified value | Note |
|---|---|---|
| **Maintenance checks** | **24 created · 18 live · 0 completed** | Re-verified 2026-07-20 (previous read 2026-07-12 showed 16/10/0). 15 scheduled, 2 in_progress, 1 cancelled. **One check is now overdue and in progress** — `kind='nsx'`, due 2026-06-30, status `in_progress`, not completed. Not investigated further this pass — worth a look if it's still open next check. Still 0 completed overall. |
| `defects` · `asset_defects` · `test_records` | **0** | Re-verified 2026-07-20, still all zero. |
| `toolbox_talks` · `site_audits` | **0** | Not re-verified this pass — carried from 2026-07-12 read. |
| `prestarts` | 34 | last 2026-07-16 (was 30, last 2026-07-04) — some movement, still infrequent. |
| `job_notes` | 391 | last 2026-07-20 — healthy, active. |
| **Named SKS staff signing in** (21d) | *not re-verified this pass* | Carried from 2026-07-12 read (~10+ named logins) — the query used a column name (`actor_email`) that no longer matches the live schema; needs a fresh query written against the current `audit_log` columns before re-quoting. |
| **Human writes, 14d** | *not re-verified this pass* | Same schema mismatch as above — don't quote the old 507/23/7/1 breakdown as current. |
| Automated writes, 14d | *not re-verified this pass* | Same. |
| `service.profiles.last_login_at` | *not re-verified this pass* | Carried from 2026-07-12 (NULL, all 5 rows) — plausible still true (Shell SSO's write path hasn't changed that anyone's logged), but not re-queried. |

### What the facts say — without a goal to filter them through

**Correction (2026-07-12): the earlier alarm was over-read.** The first cut of this file said *"people show up and cannot finish work — a completion-path problem, unambiguously bad."* A live check of due-dates shows that was wrong: nothing has been completed because **nothing has come due.** Every live check is scheduled for 2026-08-06 or later; 8 are 2027 RCD compliance seeds; nothing has even been *started*. That is a young, forward-scheduled system, not a broken one. Logged as the correction to failure **F4** — the metric used to raise the alarm was itself un-verified against reality, the exact "verified falsehood" the plan calls its floor.

**Update (2026-07-20):** that framing needs one adjustment, not a reversal — one check (`nsx`, due 2026-06-30) is now overdue and marked `in_progress`, the first sign of the "first due check" moment the 07-12 note said to watch for. Still 0 completions overall; still not a broken-workflow signal, just the first real data point since the seed. **What IS genuinely open** (soft signals, not a crisis, stated as facts not priorities): whether NSW is capturing *near-term* operational work at all — `prestarts` still infrequent (34 total, last 07-16), safety modules still at 0, and the login/write breakdown needs a fresh query (see table above) before it can be quoted again. These are worth **watching** (the product pulse), not **alarming** about.

---

## How to use this file

1. **Read the GOALS section.** If it is UNSET, you have **no basis to defer or deprioritise anything.** Say so plainly rather than borrowing a deadline from somewhere else.
2. **Treat FACTS as leads with a shelf life.** Re-run the query. This table is a cache of reality, not reality. (`CLAUDE.md` §7.)
3. **Never fill a slot in this file because it looks empty.** The blank goals section is the most valuable thing on this page.

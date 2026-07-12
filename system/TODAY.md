---
title: TODAY — Focus Filter
owner: Royce Milmlow
last_updated: 2026-07-12
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

## FACTS — `type: verified` · `verify: sql` · read from live DB 2026-07-11

These are **not** assertions. They are direct reads of ehow (`ehowgjardagevnrluult`) and eq-canonical (`jvknxcmbtrfnxfrwfimn`). Re-verify before quoting — the query is the source, this table is a cache.

| Signal | Verified value | Note |
|---|---|---|
| **Maintenance checks** | **16 created · 10 live · 0 completed** | Re-verified 2026-07-12 against due-dates. All 10 live checks are **future-dated** (earliest due 2026-08-06; 8 are RCD compliance seeds due 2027). 6 are soft-deleted. **0 completed = nothing has come due, NOT a broken workflow.** First real completion signal: **2026-08-06**. |
| `defects` · `asset_defects` · `test_records` · `service_visits` · `toolbox_talks` · `site_audits` | **0** | all zero |
| `prestarts` | 30 | last 2026-07-04 — stalled |
| `job_notes` | 309 | last 2026-07-10 — healthy |
| **Named SKS staff signing in** (21d) | **~10+** | matthew.miller, luke.wheeler, collin.toohey, william.brown, zemi.asri, huon.henne, scott.hotson, simon.bramall, calum@ssw. **Logins are real.** |
| **Human writes, 14d** | **Royce 507 (94%)** · simon.bramall 23 · unresolved 7 · scott.hotson 1 | **31 non-Royce writes in two weeks.** |
| Automated writes, 14d | 2,494 (`source='system'`) | **Exclude from every adoption metric or you will flatter yourself.** |
| `service.profiles.last_login_at` | NULL, all 5 rows | Written only by the **retired** standalone signin. Shell SSO never writes it. **Adoption is currently unmeasurable.** |

### What the facts say — without a goal to filter them through

**Correction (2026-07-12): the earlier alarm was over-read.** The first cut of this file said *"people show up and cannot finish work — a completion-path problem, unambiguously bad."* A live check of due-dates shows that was wrong: nothing has been completed because **nothing has come due.** Every live check is scheduled for 2026-08-06 or later; 8 are 2027 RCD compliance seeds; nothing has even been *started*. That is a young, forward-scheduled system, not a broken one. Logged as the correction to failure **F4** — the metric used to raise the alarm was itself un-verified against reality, the exact "verified falsehood" the plan calls its floor.

**What IS genuinely open** (soft signals, not a crisis, stated as facts not priorities): whether NSW is capturing *near-term* operational work at all — `prestarts` stalled at 30 (last 2026-07-04), safety modules at 0, only 31 non-Royce human writes in 14 days, and adoption itself unmeasurable because `last_login_at` is never written by Shell SSO. These are worth **watching** (the product pulse), not **alarming** about. The next moment that matters: **2026-08-06** — does the first due check get completed?

---

## How to use this file

1. **Read the GOALS section.** If it is UNSET, you have **no basis to defer or deprioritise anything.** Say so plainly rather than borrowing a deadline from somewhere else.
2. **Treat FACTS as leads with a shelf life.** Re-run the query. This table is a cache of reality, not reality. (`CLAUDE.md` §7.)
3. **Never fill a slot in this file because it looks empty.** The blank goals section is the most valuable thing on this page.

---
title: TODAY — Focus Filter
owner: Royce Milmlow
last_updated: 2026-07-11
scope: The filter for every Claude session decision. Facts are machine-verified. Goals are human-owned and currently UNSET.
read_priority: critical
status: live
---

# TODAY — Focus Filter

> **Goals: UNSET.** See below. **Do not invent them. Do not infer them from old files.**
> Until Royce sets them, no assistant may defer, deprioritise, or justify work by appeal to a deadline or quarterly outcome. There isn't one.

---

## ⚠️ Read this before using this file

On **2026-07-11** this file contained a hard deadline — *"34 days to 1 August 2026"* — and three Q3 success outcomes, marked `read_priority: critical`, loaded first by every assistant in every session.

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

**Rules for this section (enforced by `claim-expiry.yml`):**
- A goal with no `expires_on` is **invalid** — CI fails.
- A goal past `expires_on` is **dead**, and surfaces as *"Royce — confirm or kill."* It does not silently persist.
- **No assistant may write a goal here.** Assistants may only propose. Goals are human-owned. This is not a formality — it is the specific safeguard that would have prevented the 1 August phantom.

---

## FACTS — `type: verified` · `verify: sql` · read from live DB 2026-07-11

These are **not** assertions. They are direct reads of ehow (`ehowgjardagevnrluult`) and eq-canonical (`jvknxcmbtrfnxfrwfimn`). Re-verify before quoting — the query is the source, this table is a cache.

| Signal | Verified value | Note |
|---|---|---|
| **Maintenance checks created** | **14** | |
| **Maintenance checks completed** | **0. Ever.** | **The core product workflow has never once been completed.** |
| `defects` · `asset_defects` · `test_records` · `service_visits` · `toolbox_talks` · `site_audits` | **0** | all zero |
| `prestarts` | 30 | last 2026-07-04 — stalled |
| `job_notes` | 309 | last 2026-07-10 — healthy |
| **Named SKS staff signing in** (21d) | **~10+** | matthew.miller, luke.wheeler, collin.toohey, william.brown, zemi.asri, huon.henne, scott.hotson, simon.bramall, calum@ssw. **Logins are real.** |
| **Human writes, 14d** | **Royce 507 (94%)** · simon.bramall 23 · unresolved 7 · scott.hotson 1 | **31 non-Royce writes in two weeks.** |
| Automated writes, 14d | 2,494 (`source='system'`) | **Exclude from every adoption metric or you will flatter yourself.** |
| `service.profiles.last_login_at` | NULL, all 5 rows | Written only by the **retired** standalone signin. Shell SSO never writes it. **Adoption is currently unmeasurable.** |

### What the facts say — without a goal to filter them through

**People show up and cannot finish work.** Ten staff log in. Fourteen checks get started. Zero get completed. That is not an adoption problem — it is a **completion-path problem**, and it is the only thing in this file that is both verified and unambiguously bad.

It is stated here as a **fact, not a priority.** Priorities require goals, and there are none. If Royce wants this to be the priority, it goes in the GOALS section above with an owner and an expiry — like everything else.

---

## How to use this file

1. **Read the GOALS section.** If it is UNSET, you have **no basis to defer or deprioritise anything.** Say so plainly rather than borrowing a deadline from somewhere else.
2. **Treat FACTS as leads with a shelf life.** Re-run the query. This table is a cache of reality, not reality. (`CLAUDE.md` §7.)
3. **Never fill a slot in this file because it looks empty.** The blank goals section is the most valuable thing on this page.

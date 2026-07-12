---
title: Session — Substrate Plan v2 (the notebook that tells the truth)
date: 2026-07-12
tool: Cowork
tier: OPS (substrate)
---

# 2026-07-12 — Substrate Plan v2

**Built:**
- `system/substrate-plan-v2.md` — fable + phased plan (Day 0, P2 claims ledger, P3 product pulse, P4 memory collapse, P5 courier). Supersedes `system/substrate-a-plus-plan.md` (frontmatter marked).
- `morning-pulse` scheduled task (Cowork, daily 07:05) — live-SQL product/substrate pulse, leads with Needs-you, read-only, 2–3 lines max. Interim F4 fix until P3's nightly workflow lands.

**Verified live before writing (ehow):**
- `app_data.maintenance_checks`: **16 created / 0 completed ever** (14 scheduled, 1 cancelled, 1 overdue; latest created 2026-07-12). TODAY.md's cached "14" already lagged by two.

**Found (live F5, this session):** the global `~/.claude/CLAUDE.md` still instructs *"Fetch raw.githubusercontent.com/.../CLAUDE.md"* — the exact F1 read path. Only the pasted session brief overrode it. Fix is Day 0 of the plan (pointer-only rewrite, Claude Code native, Royce approves diff).

**Decided (Royce, in-chat):**
- Adopt plan v2 into eq-context. ✔ written
- Courier: eq-context exempted from no-auto-push (eq-context/main only, `courier:` prefix). Logged in `ops/decisions.md` 2026-07-12. Build is P5.
- Morning pulse daily. ✔ scheduled
- Goals: **left UNSET.** Nothing invented, nothing borrowed.

**Deferred (all propose-only, no deadline — goals are UNSET):**
- Day 0 execution: rewrite `~/.claude/CLAUDE.md` to pointer; prune Cowork auto-memory to pointers.
- P2 claims ledger (`system/claims.yml` + `substrate-nightly.yml` + promotion guard + suite tests).
- P4: retire `auto-bump-frontmatter`; `memory-coverage.yml`; workflow consolidation 16→≤8; CLAUDE.md diet ≤200 lines.
- P5 courier install (Claude Code native on Beelink).
- Adoption instrumentation (`last_login_at` never written by Shell SSO — adoption unmeasurable) — build task, Rule 0.6 gated.

**Writes this session** (all single-cp via /tmp, wc -l + tail + NUL-scan verified): `system/substrate-plan-v2.md` (new, 193 lines), `system/substrate-a-plus-plan.md` (frontmatter only), `ops/decisions.md` (courier entry), `ops/pending.md`, this file. No git run from sandbox.

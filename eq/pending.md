---
title: EQ Tier — Pending Actions (index)
owner: Royce Milmlow
last_updated: 2026-08-17
scope: This file used to hold every EQ-tier pending item across all 9+ repos in one 3741-line doc. Split 2026-08-17 into eq/pending/<repo>.md, one file per repo (mirroring the existing eq/changelog/<repo>.md convention), because a session in one repo had to wade through every other repo's backlog to find its own — and the felt size of "509 open items" was really 5+ separate, much smaller queues counted as one.
read_priority: critical
status: live
---

# EQ Tier — Pending (index)

Each EQ repo now has its own pending file:

- [eq/pending/eq-shell.md](pending/eq-shell.md)
- [eq/pending/eq-cards.md](pending/eq-cards.md)
- [eq/pending/eq-field.md](pending/eq-field.md)
- [eq/pending/eq-solves-service.md](pending/eq-solves-service.md)
- [eq/pending/eq-solves-intake.md](pending/eq-solves-intake.md)
- [eq/pending/eq-design-tokens.md](pending/eq-design-tokens.md)
- [eq/pending/eq-ui.md](pending/eq-ui.md)
- [eq/pending/eq-receipts.md](pending/eq-receipts.md)
- [eq/pending/eq-context.md](pending/eq-context.md) — the substrate/tooling repo itself
- [eq/pending/cross-repo.md](pending/cross-repo.md) — work genuinely spanning 2+ repos as one unit, plus suite-wide/governance items with no single owning repo
- [eq/pending/sks.md](pending/sks.md) — SKS-tagged items that had been sitting in this file despite the standing convention that SKS work lives in `sks/pending.md`; flagged here, not auto-merged into that file

New items go in the file for the repo that owns the work. If genuinely 2+ repos, use `cross-repo.md`.

SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

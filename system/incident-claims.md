---
title: Incident Claims Registry
owner: Royce Milmlow
last_updated: 2026-07-30
scope: Lightweight "session X is already on incident Y" lock — checked automatically at session start against the digest's Needs You list. Stops the same finding being independently investigated by 2-3 concurrent sessions on the same day.
read_priority: high
status: live
---

# Incident Claims Registry

**Why this exists:** the same-day session log has repeatedly shown two or
three separate sessions independently chasing the identical finding before
converging (e.g. the `rls_introspection` anon-exec finding — SEC-9's
neighbourhood — was investigated from scratch by at least 3 sessions).
Nothing broke, but it burned hours of redundant work per incident. Unlike
`system/worktree-registry.md` (pure documentation convention — nothing
triggers a worktree-registry check automatically), this file gets a real
mechanical assist: `hooks/session_start.py` reads it every session and
cross-references it against `digest.md`'s "Needs you" list, printing a
`CLAIMS` warning at the top of the session gate when there's overlap.

**Protocol:**
1. Before starting non-trivial investigation or a fix on a flagged finding
   (a `SEC-N` row, an `F-N` failure, a named Sentry issue, anything that
   would otherwise show up in digest.md's "Needs you"), check this file —
   or just read the `CLAIMS` line the session gate already printed.
2. If a live (non-stale) claim exists for the same ID: don't start an
   independent investigation from scratch. Read the claiming session's
   notes first — coordinate, wait, or confirm you're doing something
   genuinely different before proceeding.
3. Claim it: add a row to the Active table before you start.
4. Release it: delete the row when you're done (fixed, closed, or
   abandoned) — or update the Notes column if handing off mid-investigation.
5. **Staleness:** a claim older than 6 hours with no update is presumed
   abandoned (a session died, or forgot to release) — `session_start.py`
   marks it `STALE` rather than treating it as binding, but its Notes are
   still worth reading before duplicating the investigation from zero.

**ID column:** use the existing register ID if one exists (`SEC-N` from
`ops/security-register.md`, `F-N` from `system/failures.md`) so the
auto-match in `session_start.py` finds it via substring match against the
digest's "Needs you" text. For anything without a register ID (a raw Sentry
issue, an ad-hoc finding), use a short distinctive slug that will literally
appear in the digest line for that item.

---

## Active

| ID | Claimed by (session) | Since (UTC ISO) | Notes |
|---|---|---|---|

_No active claims. Add a row before starting non-trivial investigation of a flagged finding; delete it when done._

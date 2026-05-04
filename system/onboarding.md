---
title: SYSTEM — Onboarding
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Tutorial introduction for any new assistant or human entering this repo
read_priority: optional
status: live
---

# SYSTEM — Onboarding

> First-time read only. If you've worked in this repo before, skip this
> and read `CLAUDE.md` and `AGENTS.md` instead.
> ~5 minute read. After it, you should be able to make a substantive
> edit and verify it landed.

---

## What this repo is

`eq-context` is the canonical project-context store for two domains:
SKS Technologies (electrical contractor, NSW data centre + healthcare)
and EQ Solutions (SaaS for trade subcontractors).

Tier-separated: `/eq`, `/sks`, `/ops`, `/system`, `/archive`. Sessions
ask "EQ or SKS focus?" before loading context.

---

## How it works mechanically

GitHub is canonical. Supabase is a runtime cache.

- Edit MD files locally → commit → push to `main`.
- A GitHub Action mirrors changed files into Supabase table
  `context_files` (project `urjhmkhbgaxrofurpbgc`).
- Other assistants read from Supabase via MCP. Round-trip: ~20 seconds.

A Postgres trigger refreshes `updated_at` on every UPDATE — so the
timestamp is the freshness signal of record. A workflow verification
job fails the push if any synced file's `updated_at` doesn't move
within 60 seconds.

---

## How to make a change

1. Decide which **tier** owns the change (eq / sks / ops / system).
2. Decide which file owns the fact within that tier (each fact has one home).
3. Edit the MD file. Update `last_updated:` in frontmatter to today.
4. Commit and push to `main`: `context(YYYY-MM-DD): <what changed>`.
5. **Verify.** Wait 30 seconds. Run the SQL below. Confirm `updated_at` reflects today.

If verification fails, the workflow's verification job has already
failed the run. Investigate before claiming done.

---

## What "done" means

A change is **not done** until the Supabase row's `updated_at` reflects
it. Terminal output is not done. A commit hash is not done. "Looks good"
is not done. The row is the deliverable.

This rule exists because three "implementation complete" claims in one
session on 2026-04-27/28 all turned out to be false on measurement.
See `system/lessons.md` "False-Implementation Pattern" for the full retro.

---

## Verification SQL

After any push, run via Supabase MCP on project `urjhmkhbgaxrofurpbgc`:

```sql
SELECT slug, updated_at, NOW() - updated_at AS age
FROM context_files
WHERE slug IN ('<files-you-changed>')
ORDER BY updated_at DESC;
```

`age` should be under 60 seconds for everything you touched.

For a periodic substrate audit (catches stale files):

```sql
SELECT slug, updated_at, NOW() - updated_at AS age
FROM context_files
WHERE
  (slug LIKE '%/pending.md' AND updated_at < NOW() - INTERVAL '7 days')
  OR (slug LIKE 'system/%' AND updated_at < NOW() - INTERVAL '14 days')
  OR (slug LIKE '%/changelog/%' AND updated_at < NOW() - INTERVAL '30 days')
ORDER BY updated_at ASC;
```

Each row is a "needs update or explicit no-change confirmation".

---

## After reading this

If you can answer these, you're ready:

1. What is the canonical source of truth for eq-context?
2. What does "done" mean in this repo?
3. What's the first question to ask at session start? (Hint: which tier?)
4. Where do new decisions go and what format do they take?
5. How would you verify a change you just made was actually applied?

If you can't, re-read or ask. Welcome to the substrate.

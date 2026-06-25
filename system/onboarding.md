---
title: SYSTEM — Onboarding
owner: Royce Milmlow
last_updated: 2026-05-07
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

Tier-separated: `/eq`, `/sks`, `/sks-team`, `/ops`, `/system`, `/archive`. Sessions
ask "EQ or SKS focus?" before loading context.

`/sks-team/` is a different audience from the rest — it serves SKS team members'
AI sessions (canonical quoting guidance, etc.), not Royce's own sessions. Files
in that tier stand alone with no cross-references to other tiers, so the tier can
extract cleanly to its own substrate later if needed.

---

## How it works mechanically

GitHub is the substrate — canonical and serving layer in one.

- Edit MD files locally → commit → push to `main`.
- That's it. The repo is public, so assistants read files directly from it
  via raw URLs: `https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>`
  (the legacy `/context/claude` alias maps to `CLAUDE.md`).

There is no cache and no sync step — a merged commit is live immediately, and
the file on `main` is the freshness signal of record. (Historical: a Supabase
edge cache mirrored files into a `context_files` table until its host project
was deleted 2026-06-22; that path is retired.)

---

## How to make a change

1. Decide which **tier** owns the change (eq / sks / sks-team / ops / system).
2. Decide which file owns the fact within that tier (each fact has one home).
3. Edit the MD file. Update `last_updated:` in frontmatter to today.
4. Commit and push to `main`: `context(YYYY-MM-DD): <what changed>`.
5. **Verify.** Confirm the change is on `main` (pushed, not just committed
   locally) — e.g. the raw URL returns your new content.

A local commit that never reached `main` is not live. Investigate before
claiming done.

---

## What "done" means

A change is **not done** until it is on `main` and the raw URL serves it.
Terminal output is not done. A local commit that wasn't pushed is not done.
"Looks good" is not done. The file live on `main` is the deliverable.

This rule exists because three "implementation complete" claims in one
session on 2026-04-27/28 all turned out to be false on measurement.
See `system/lessons.md` "False-Implementation Pattern" for the full retro.

---

## Verification

After any push, confirm `main` serves the new content (replace `<path>`):

```bash
curl -s https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path> | head
```

If the raw URL doesn't reflect your change, it isn't on `main` yet.

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

---
title: Archive
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Parked, deferred, and historical content kept out of default AI load
read_priority: reference
status: live
---

# Archive

Content that should not load in default AI sessions but is preserved for
git history and potential reactivation. AIs read `/archive/` only when
explicitly directed.

| File | Why archived | When to revisit |
|---|---|---|
| `changelog-eq-quotes.md` | EQ Quotes deferred ~6 months (per 2026-04-29 cull) | When EQ Field hits 20 paying customers |
| `changelog-ahd.md` | AHD parked to 2027 capital activation | 2027 capital activation review |

## How to revive archived content

1. Move the file out of `/archive/` into the appropriate tier folder.
2. Update `status:` in frontmatter from `archived` to `live`.
3. Update `last_updated:` to today.
4. Add an entry to `ops/decisions.md` recording the revival.
5. Push and verify Supabase sync.

---
title: Sprint — Trade multi-value array, eq-field coordination
owner: Royce Milmlow
last_updated: 2026-08-14
scope: Scoping only — not started. Converts app_data.staff.trade from text to a real text[] array so a worker can be tagged with more than one trade at the database level, matching the multi-select already shipped in eq-shell (PR #1346, comma-separated text as an interim). Requires a paired eq-field migration because trade is read/written directly by eq-field's own field_people compatibility views and triggers, not just by eq-shell.
read_priority: standard
status: draft
duration_estimate: Unscoped in days — needs its own eq-field session to read live trigger definitions and eq-field's own Trade UI before estimating.
---

# Sprint — Trade multi-value array, eq-field coordination

**Status:** scoped only. No code written, no migration drafted, no branch opened. This document is the handoff brief for whoever picks this up — read it fully before touching either repo.

---

## Objective

Royce asked (2026-08-14, off a Staff list screenshot) why Trade only ever shows one value when workers routinely do more than one (electrical + comms). The immediate fix shipped same day: eq-shell [PR #1346](https://github.com/eq-solutions/eq-shell/pull/1346), Trade as a multi-select stored as comma-separated text on the existing `staff.trade` column — zero schema change, ships same session.

That's an interim shape, not the end state. Royce's explicit direction for the real fix: **`app_data.staff.trade` becomes a proper `text[]` array** — and it must stay canonical. `app_data.staff` is the one true staff record, read by both eq-shell and eq-field; this migration must not fork a second, eq-field-local representation of trade (a cache table, a duplicated column, a sync job). Same column, same table, both apps reading/writing it directly, exactly as today — only the column's type changes.

---

## What exists (verified live, 2026-08-14 — not from migration-file comments)

**Both canonical planes, checked directly via Supabase MCP `execute_sql`:**

| Fact | ehow (SKS) | zaap (EQ) |
|---|---|---|
| `app_data.staff.trade` type | `text` | `text` |
| `app_data.field_people` view exists, `security_invoker=on` | yes | yes |
| `app_data.field_people_removed` view exists, `security_invoker=on` | yes | yes |
| `field_people_iud_trg` (write trigger on `field_people` itself) | **present** | **absent** |
| `field_people_worker_id_iu_trg` (extra guard trigger on `field_people`) | present (ehow-only, per `field-people-iud-guard-list` history — added by eq-field#518) | absent |
| `field_people_removed_iud_trg` | present | present |

**The ehow/zaap asymmetry on `field_people_iud_trg` is a real, previously-undocumented finding from this session** — SKS's `field_people` view is fully writable (insert/update) through the trigger; EQ's own `field_people` view on zaap has no such trigger, only the `_removed` twin does. This means:
- The known incident history (3 prior `security_invoker` resets, per `field-people-iud-guard-list`) is entirely an **ehow-side** risk — that's where the live write trigger is.
- **Not yet verified:** how eq-field's own UI writes Trade for an EQ-tenant person if `field_people` isn't writable there. Either EQ's Field UI writes to `app_data.staff` directly (bypassing the view), or Trade editing for EQ's own workforce doesn't go through this path at all, or it's simply not offered. **First thing the eq-field session must confirm before writing any migration.**

**eq-shell's own write paths to `trade` (both need checking, only one confirmed touched by #1346):**
- `netlify/functions/entity-patch.ts` — raw `.from('staff').update(patch)` via the Supabase JS client. This is what the Staff list's inline multi-select (PR #1346) uses. Comma-text aware already; would need to send an array instead once the column changes.
- `public.eq_update_staff(p_staff_id uuid, ..., p_trade text DEFAULT NULL, ...)` — a separate RPC, still live on ehow with `p_trade text`. **Not touched by #1346.** Caller not yet identified this session (possibly eq-field itself, possibly an older/parallel Shell path) — the eq-field session must trace every caller before deciding whether this RPC needs an array-aware signature too.

**Live data (ehow, `app_data.staff`, checked 2026-08-14):** `trade` non-null on 22 of 101 rows, all single values (`electrical`×21, `communications`×1) — no existing comma-separated or multi-value data to migrate. The backfill step is trivial (`text` → `ARRAY[trade]` where not null, `NULL` → `NULL`).

---

## What's blocking a direct column-type change

Postgres refuses `ALTER TABLE app_data.staff ALTER COLUMN trade TYPE text[]` while `field_people`/`field_people_removed` depend on that column via a plain `SELECT trade` — the views must be dropped and recreated (or `CREATE OR REPLACE`d) in the same operation. That recreation is exactly the moment that's already gone wrong 3 times in eq-field's own history: `CREATE OR REPLACE VIEW` resets the *entire* `reloptions` list, not just the changed columns, so `security_invoker = on` — the actual tenant-isolation control on these views — silently flips back off unless every future `CREATE OR REPLACE` repeats it inline. See eq-field's own `20260728000210_field_people_labour_hire_rating.sql` incident note and `eq-context` memory `field-people-iud-guard-list` for the full history (licence/agency → hire_company → user_id, three separate leaks of this shape).

Sequencing risk on top of the view risk: if the column changes before eq-field's trigger/view/frontend are updated, eq-field's next write 500s (string into an array column). If eq-field changes first, its trigger writes an array into a still-`text` column and *that* 500s instead. They have to land together, not just "eq-shell migrates, eq-field catches up later."

---

## Canonical-truth constraint (non-negotiable, per Royce)

`app_data.staff` stays the single canonical staff table. This migration is a **type change on an existing canonical column**, not a new data model. Specifically ruled out:
- No eq-field-local `trade` cache, mirror, or shadow table.
- No sync job reconciling two copies.
- No new "Field's version of trade" vs "Shell's version of trade" — one column, one array, both apps read and write the same value directly, exactly like today.

If a design under consideration during the eq-field session would introduce a second source of truth for trade, that's the wrong design regardless of how it simplifies the migration — stop and re-scope rather than build it.

---

## Proposed execution sequence (draft — the eq-field session should confirm/revise, not treat as fixed)

1. **eq-field session starts with drift-check, not a plan.** Re-run the live queries in "What exists" above against both planes at session start (state may have moved since 2026-08-14) — read `pg_get_functiondef` for `field_people_iud()` and `field_people_removed_iud()` on both planes, don't trust this doc's copy.
2. **Resolve the zaap asymmetry.** Find how (or whether) EQ-tenant Field UI edits Trade today. This determines whether zaap needs a new trigger built from scratch (different risk profile — no existing incident history to learn from) or genuinely has nothing to touch.
3. **Trace every live caller of `eq_update_staff`** (both `p_trade` param and any other RPC touching this column) — decide in scope whether it needs an array-aware signature or is dead/superseded.
4. **Draft eq-field's migration**: rebuild `field_people` / `field_people_removed` with `trade` projected as `text[]`, rebuild `field_people_iud()` (and the zaap equivalent, once step 2 resolves what that looks like) to read/write an array, **repeating `WITH (security_invoker = on)` inline in the same `CREATE OR REPLACE VIEW` statement** — do not rely on a separate `ALTER VIEW` run once. DDL-replay-test in a rolled-back transaction against ehow first, per this repo's own governance.
5. **Decide eq-field's own UI treatment** of a multi-value trade (comma display, its own multi-select, or first-value-only) — eq-field's call, not eq-shell's.
6. **Draft eq-shell's tenant-migration** (One Pipe, `supabase/tenant-migrations/`) converting `staff.trade` to `text[]` with the trivial backfill above, applied through `tenant-migrate.yml` to both zaap and ehow together — not by hand, not via the Supabase MCP directly (see this repo's DDL governance rules).
7. **Update eq-shell's own write path**: `entity-patch.ts`'s trade handling already produces comma-separated strings (PR #1346) — swap to sending/receiving a real array; drop the split/join logic in `InlineMultiSelectCell` once the column itself is the array.
8. **Land both migrations in the same maintenance window**, verify against live on both planes (column type, view `security_invoker`, a real write through each app) before calling it done — not "CI is green," an actual read/write round-trip on a real record in a low-traffic window.

---

## Constraints

- Don't touch `app_data.staff` DDL from eq-shell alone — this is a two-repo coordinated change, full stop.
- No canonical DDL outside each repo's own governed migration pipeline (eq-shell: `tenant-migrate.yml` One Pipe; eq-field: its own migration convention) — no hand-applied fixes via the Supabase MCP, even as a "temporary" step.
- Every `CREATE OR REPLACE VIEW` on `field_people`/`field_people_removed` must repeat `WITH (security_invoker = on)` in the same statement — this is the single most important line in this entire document, given the 3-incident history.
- No eq-field-local duplicate of trade data — see canonical-truth constraint above.
- Don't start this from an eq-shell session — it needs its own eq-field-rooted session (or a session with both repos deliberately in scope, per `C:\Projects\CLAUDE.md` Rule 0).

---

## Where to start

Next session: `/brief eq-field`, then re-verify this doc's "What exists" table live before writing anything. Not scheduled — Royce's call on when.

## Related

- [eq-shell PR #1346](https://github.com/eq-solutions/eq-shell/pull/1346) — the interim comma-separated-text fix, live now
- `eq-context` memory: `field-people-iud-guard-list` — the 3-incident history this migration has to avoid repeating
- `eq-field/supabase/migrations/20260728000210_field_people_labour_hire_rating.sql` — most recent rebuild of these exact views/triggers, good reference for the correct `security_invoker` pattern
- [sessions/2026-08-14.md](../../sessions/2026-08-14.md) (part 20) — full session log for the original fix + this scoping

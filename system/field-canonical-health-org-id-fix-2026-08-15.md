---
title: Fix field_canonical_health() — org_id/tenant_id column drift
owner: Royce Milmlow
last_updated: 2026-08-15
kind: state
scope: Live RPC fix for ehow (sks-canonical) — needs Royce's own hands, the Claude Code safety classifier blocks live-DB writes from this session regardless of permission granted.
read_priority: high
status: live
---

# Fix `field_canonical_health()` — a nightly refresh has been silently failing

## What's broken

`suite-state.md`'s "Field Data Plane" table has read `app_data.field_people = 66`
every night since some point after a column migration, while the live table
holds **83** rows — confirmed by direct query 2026-08-15.

Root cause: `public.field_canonical_health()` on **ehow**
(`ehowgjardagevnrluult`) filters four of its eight counts by `org_id`, but
`field_schedule`, `field_timesheets`, `prestarts`, and `toolbox_talks` were
migrated to `tenant_id` at some point and the function was never updated.
Calling it today throws:

```
ERROR: 42703: column "org_id" does not exist
QUERY: ... FROM app_data.field_schedule WHERE org_id = sks_org_id
```

`.github/scripts/refresh_suite_state.py` wraps this call in a bare
`except Exception as e: print(f"  WARNING: ...", file=sys.stderr)` — so the
whole nightly workflow **exits green** while silently leaving the Field
table frozen at whatever it last successfully wrote. The file's top-level
`last_updated` still advances every night, so it reads as current. This is
the exact "generated file looks fresh while one section is dead" shape
`system/failures.md` F14 was written to catch — except F14's guard checks
staleness of `last_updated`, which this bug doesn't trip, because most of
the file DOES refresh correctly every night. Only this one embedded query
is dead.

## Why this session can't fix it

Attempted the live `CREATE OR REPLACE FUNCTION` fix directly — **blocked by
the Claude Code safety classifier** as a live-database write, same posture
as SEC-9/SEC-24's Netlify fixes. Not a permission question; manual-hands
only.

## The fix — run this on ehow (`ehowgjardagevnrluult`)

```sql
CREATE OR REPLACE FUNCTION public.field_canonical_health()
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'app_data'
AS $function$
DECLARE
  sks_tenant_id  uuid := '7dee117c-98bd-4d39-af8c-2c81d02a1e85';
  sks_org_id     uuid := '00000000-0000-0000-0000-000000000002';
  result         jsonb;
BEGIN
  SELECT jsonb_build_object(
    'people',        (SELECT count(*)::int FROM app_data.field_people      WHERE tenant_id = sks_tenant_id),
    'sites',         (SELECT count(*)::int FROM app_data.field_sites        WHERE tenant_id = sks_tenant_id),
    'managers',      (SELECT count(*)::int FROM app_data.field_managers     WHERE tenant_id = sks_tenant_id),
    'schedule',      (SELECT count(*)::int FROM app_data.field_schedule     WHERE tenant_id = sks_tenant_id),
    'timesheets',    (SELECT count(*)::int FROM app_data.field_timesheets   WHERE tenant_id = sks_tenant_id),
    'prestarts',     (SELECT count(*)::int FROM public.prestarts            WHERE tenant_id = sks_tenant_id),
    'toolbox_talks', (SELECT count(*)::int FROM public.toolbox_talks        WHERE tenant_id = sks_tenant_id),
    'site_audits',   (SELECT count(*)::int FROM public.site_audits          WHERE org_id    = sks_org_id)
  ) INTO result;
  RETURN result;
END;
$function$;
```

**Only `site_audits` keeps `org_id`** — verified live 2026-08-15, that
table genuinely still carries `org_id`, not `tenant_id`. Every other table
in this function already migrated. Don't blanket-replace `org_id` with
`tenant_id` across all eight lines; only the four named above are wrong.

**Verify after applying:**

```sql
select field_canonical_health();
-- expect: {"people": 83, "sites": ..., "managers": 19, "schedule": ..., ...}
```

Then either wait for the next nightly `suite-state-refresh.yml` run, or
dispatch it by hand (`gh workflow run suite-state-refresh.yml`) to pick up
the corrected count immediately.

## Companion fix already shipped (this session, no live-DB access needed)

`refresh_suite_state.py`'s silent `except` now emits a GitHub Actions
`::error::` annotation instead of a stderr-only warning, so a future
version of this exact bug surfaces in the workflow run summary instead of
requiring someone to notice a stale number by hand. See that script's own
comment at the fix site.

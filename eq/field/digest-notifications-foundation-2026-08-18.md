---
title: EQ Field — Digest & Notifications Foundation (design)
owner: Royce Milmlow
last_updated: 2026-08-18
scope: Scoped design for making the weekly supervisor digest editable, built as a general notification-subscription foundation rather than a one-off digest editor. Not yet built — this is the spec a build session executes against.
read_priority: high
status: live
---

# EQ Field — Digest & Notifications Foundation

Royce's brief: "investigate an elegant, professional but simple solution
here that's scalable — notifications via Field is something we can build
on." That last clause is the actual design constraint: this isn't "make
the digest editable," it's "make the *first* editable notification, in a
shape that doesn't need re-architecting for the second one."

Re-checked live before writing this (2026-08-18): the trigger condition
from the 2026-08-14 hold — real edits to the 3 existing leave-email
templates — is still unmet. All three carry `updated_by: null`, untouched
since they shipped. That doesn't block this design; it's why this is a
spec, not a shipped migration — see "What this doc is not," below.

---

## The actual gap (recap)

Two things are missing today, and they're different problems:

1. **The digest's content isn't editable.** It's built from live data (a
   status table, a progress bar, section links), so "editable" can't mean
   swapping in a flat text template the way the 3 leave emails work.
2. **The audience is fixed to Supervisors.** Both the digest and the
   separate ad-hoc notify-list only ever pull recipients from people
   flagged Supervisor. There's no way to add someone who wants visibility
   without being an operational supervisor — an owner, an account manager,
   a client contact.

(2) is the one worth solving generally. It's the actual foundation.

---

## Design

### New table: `notification_subscriptions`

The one new table this needs, and the actual scalable primitive — every
future notification type (not just the digest) reads from this instead of
hardcoding "who gets told."

```sql
create table public.notification_subscriptions (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null,
  person_id uuid not null,       -- references people/managers; confirm the
                                  -- right FK target at build time (see Open
                                  -- questions)
  channel text not null,         -- 'weekly_digest' today; anything else later
  enabled boolean not null default true,
  added_by text,
  added_at timestamptz not null default now()
);
```

- `channel` is a free-text key, not an enum — a new notification type is a
  new value here, not a schema change. Mirrors how `email_templates` uses
  `template_key` the same way already.
- Supervisors keep getting the digest automatically (unchanged, no
  subscription row needed) — this table is for *additional* recipients,
  same "additive, don't touch the existing default" pattern used
  everywhere else in this app's permission model.
- RLS: same `org_id`-scoped `authenticated` pattern as every other
  hardened `public.*` SKS table (`audit_log`, `acknowledgments`) — see
  eq-field's own `CLAUDE.md` schema-gotchas section for the exact template
  to copy (`ack_tenant_read`/`ack_tenant_write`).

### Digest section toggles: reuse `app_config`, no new table

The digest's dynamic blocks (licence expiries, leave requests, timesheet
flags) get an on/off toggle + a short custom intro line each — not raw
HTML editing. This doesn't need its own table: `app_config.value` is
already `text`, already org-scoped, already the pattern used for PIN
codes. One key, JSON-encoded:

```
key = 'digest_sections'
value = '{"licence_expiries":{"enabled":true,"intro":""},
          "leave_requests":{"enabled":true,"intro":""},
          "timesheet_flags":{"enabled":true,"intro":""}}'
```

Parsed client-side and server-side the same way other JSON-shaped config
already gets handled in this codebase. No migration beyond a row insert
with a sane default (all sections on, no custom intro — today's actual
behaviour, so shipping this changes nothing until someone touches it).

### UI: extends the existing digest-settings screen, doesn't replace it

`scripts/digest-settings.js` already exists and already has the
opt-in/opt-out pattern for individual supervisors. Two additions, same
screen:

- **"Also notify"** — a person/contact picker that writes rows to
  `notification_subscriptions` (channel = `weekly_digest`). Reuses
  whatever picker component already backs a similar list elsewhere in the
  app (Batch Fill's team picker is the closest existing pattern) rather
  than building a new one.
- **"Sections"** — a checkbox + short text field per section, reading and
  writing the `digest_sections` app_config key above.

### Backend: `supervisor-digest` edge function, two small changes

1. Recipient query becomes `(people flagged Supervisor) UNION (people with
   an enabled notification_subscriptions row for channel='weekly_digest')`
   instead of just the Supervisor flag.
2. Before rendering each section, check `digest_sections[section].enabled`
   — skip the block if off, prepend the custom `intro` text if set.

No change to the cron trigger, the auth model, or anything else the
function currently does.

---

## Why this is "elegant, simple, scalable" and not three separate builds

- **One new table**, general-purpose from day one — the next notification
  type (a licence-expiry alert to an account manager, say) is a new
  `channel` value and a UI checkbox, not a new table and a new migration.
- **Zero new tables for the content-editing half** — `app_config` already
  does exactly this job for exactly this kind of org-level setting.
- **Nothing about today's behaviour changes** until someone actually
  touches a toggle or adds a subscriber — the defaults reproduce the
  current fixed behaviour exactly, so this ships with no visible change on
  its own.

---

## What this doc is not

Not a shipped migration, not tested code. Royce asked to *investigate* the
shape of this — this is that investigation, structured so a build session
can execute directly against it rather than re-deriving the design. The
actual `CREATE TABLE`, the edge-function diff, and the UI changes are the
next concrete step, not done in this pass — this is real production email
delivery + a live database, and this doc alone hasn't been through this
repo's own review-before-ship discipline for auth/data-model changes.

## Open questions for the build session

- **`person_id`'s real FK target** — confirm against the live schema
  whether Contacts and Supervisors resolve to the same identity table on
  ehow, or two different ones; the subscription table needs to point at
  whichever one a person picker in the UI actually returns.
- **Contacts vs. people** — "an account manager" or "a client contact" may
  not be a `people` row at all today. If Contacts is a separate entity,
  confirm it can carry a subscription row the same way, or scope v1 to
  people/supervisors only and note Contacts as a fast-follow.
- **Unsubscribe path** — a lightweight self-service "stop notifying me"
  isn't scoped here; v1 assumes additions/removals go through the settings
  screen by an admin, not by the recipient themselves.

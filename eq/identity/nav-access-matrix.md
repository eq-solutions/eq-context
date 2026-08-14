---
title: EQ Suite — Navigation Access Matrix: Who Sees What, and How It's Enforced
owner: Royce Milmlow
last_updated: 2026-08-14
scope: Punch-list SUITE-1 (nav-simplification pass) — a deliberate, suite-wide record of which nav items are visible to which roles and by what mechanism, so the pattern is a design decision instead of four independent accidents.
read_priority: standard
status: live
---

# EQ Suite — Navigation Access Matrix

One place that states, per app, who sees which nav items and what actually
enforces that — not the design intent, the real mechanism in the code.
Written 2026-08-14 from a live code-level audit of all four repos (eq-shell,
eq-field, eq-solves-service, eq-cards), triggered by a UX-simplification
pass. Every app already does heavy progressive disclosure by role — that's
the right instinct. What this doc records is that it's currently done four
different ways, none of them shared, and that's already caused real drift
(see below).

---

## The mechanisms in use today

| App | Mechanism | Granularity |
|---|---|---|
| **Shell** | `useCan('perm.key')` — permission hooks sourced from `@eq-solutions/roles` | Per nav item |
| **Field** | CSS class `.edit-only` toggled by `isManager` (`auth.js` `toggleManagerMode()`); separate tenant gate (`ORG_SLUG === 'sks'`); separate tier gate (Standard/Advanced/Enterprise); separate apprentice-tier JS strip (`app-state.js`) | Per nav item, but four independent gates stacked, not one system |
| **Service** | `role === 'manager'` / `role === 'employee'` checks inline in `buildNavSections`; separate tenant feature toggles (`calendar_enabled`, `defects_enabled`, `commercial_features_enabled`) | Per nav item, mixes role gating and feature-flag gating in one function |
| **Cards** | `role == 'manager' \|\| role == 'supervisor'` checks written per-widget, not centralized; separate org-admin/platform-admin provider checks | Per widget — the same eligibility check has been retyped in more than one place |

Shell's is the most structured (one hook, one source of truth per permission
key). The other three work, but each is a bespoke stack of conditions with
no shared vocabulary for "who can see this."

---

## Per app: who sees what

### EQ Shell
Base employee role sees Records (Customers, Staff, Plant & equipment if
`equipment.view`), Apps (Field/Service/Cards/Comms if tenant-entitled),
Account (2FA) — roughly 7-8 destinations. Resourcing needs
`staff.manage_conversations` (a group grant, not a role — currently no role
has it by default). Admin needs any of `admin.list_users` /
`intake.view` / `ops.view_rates` / `ops.view_suppliers`, gated as one
umbrella for the whole section, not per-tile inside it. Platform needs
`is_platform_admin`. Mobile collapses further again per cohort (a
"field-first" tenant flag, and a separate `mobileSimplified`
manager/supervisor cohort) — a third layer of visibility rules on top of the
two above.

### EQ Field
Stack of four independent gates: manager (`isManager`, hides via CSS
`display:none` — nav-hidden only, not always route-guarded, see the open
security finding on this below), tenant (`sks` vs `eq`), subscription tier,
and a separate apprentice-tier strip that removes most of the nav wholesale
rather than composing with the other three.

### EQ Service
`role === 'employee'` hides Do/Records/Insight from technicians;
`role === 'manager'` required for Admin. A second, unrelated axis —
per-tenant feature toggles — controls the same sidebar function, so reading
`buildNavSections` means tracking both role and tenant config to know what
renders.

### EQ Cards
Manager/supervisor eligibility (`role == 'manager' || role == 'supervisor'`)
was written inline in more than one widget instead of being one shared
check — see the drift entry below, the first concrete cost of that.

---

## Where this has already caused real drift

Found in the 2026-08-14 nav audit — the exact failure mode this doc exists
to prevent: a gate changed or added in one place, not mirrored in the
sibling surface that needed the same rule.

- **Cards** — the workspace switcher and manager join-QR card were
  implemented twice (Profile and Settings), independently, because there was
  no single shared widget to reuse. Confirmed via git history: the QR card
  was added to Settings only (PR #66); the Profile copy was pasted in later
  during a tab-nav merge (PR #75) instead of importing what already existed.
  De-dupe in flight this session (`eq-cards` PR #243).
- **Field** — desktop's "Add Person" button had no manager gate; the mobile
  drawer's equivalent item did. Same action, two surfaces, two different
  rules, because each surface's gate was hand-written separately. Fix in
  flight this session.
- **Service** — the Shell-embedded nav bar is a second, hand-maintained copy
  of the standalone sidebar's nav list. It silently fell behind — missing
  Today, Search, and Settings entirely, not gated out, just never added when
  the embedded bar was last touched. Fix in flight this session.

Three for three: every drift found traces to the same root cause — no
shared source of truth for "what's in the nav and who can see it," so each
surface (desktop/mobile, standalone/embedded, Profile/Settings) reinvents
the list and the gate by hand.

**Separately, not a nav-consistency issue but found in the same pass:**
Field's manager-only pages are hidden from nav via CSS only — several have
no server/JS-level access check behind them, so a direct link still opens
them for a worker. Tracked as its own hardening task, not a UX fix — see
`system/security-register.md`-adjacent tracking, not repeated here.

---

## Recommendation — not decided, this is a record, not a chosen path

Two ways to close the gap, in order of cost:

1. **A shared, roles-derived nav-visibility config each app imports.**
   Heaviest option — requires every app's stack to consume a common format.
   Field is the hard case: it has no package manager or build step, so it
   can't `import` from `@eq-solutions/roles` the way Shell and Service do
   today; it would need its own lightweight adapter.
2. **A lighter checklist, not automated:** when a nav item is added or its
   gate changes, this doc's per-app section states the pattern to copy, and
   whichever surfaces exist for that app (desktop + mobile, standalone +
   embedded) must both be checked in the same PR. Cheaper, doesn't prevent
   drift automatically, but gives review something concrete to check against
   instead of relying on someone remembering the sibling surface exists.

Not built either way. This doc records the current state and the drift
already found and fixed — it doesn't pick a direction. That's Royce's call.

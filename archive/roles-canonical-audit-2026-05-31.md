---
title: Roles + eq-canonical Audit (2026-05-31)
owner: Royce Milmlow
last_updated: 2026-05-31
scope: Roles/canonical audit (archived snapshot)
read_priority: reference
status: archived
---
# Roles + eq-canonical audit — 2026-05-31

**Source:** ad-hoc fan-out (2 read-only `Explore` agents over 9 EQ repos) + manual verification
against source. Run as a demonstration of the audit-fan-out pattern. Everything below is
**verified against source** unless marked otherwise.

> ⚠️ One agent verdict in this audit was confidently **wrong** (see §C). Treat fan-out
> conclusions as *leads*, not facts, until checked against source.

---

## A. `eq-canonical` references — it is NOT a rename

`eq-context/STATE.md` (registry, lines 40–41) is authoritative: these are **two separate live
Supabase projects**, not an old/new name for one thing.

| ref | name | role | access |
|---|---|---|---|
| `jvknxcmbtrfnxfrwfimn` | `eq-canonical` | **control plane** — browser-facing (intake events, list RPCs) | browser via `VITE_SUPABASE_URL` |
| `zaapmfdkgedqupfjtchl` | `eq-canonical-internal` | **EQ tenant data plane** (`app_data.*`, commit RPCs) | **server-only** via Netlify functions |

**Implication:** a blanket find-and-replace `eq-canonical` → `eq-canonical-internal` would
repoint browser code at the server-only data plane. **Do not do it.** Each reference must be
classified: correctly pointing at the control plane (leave) or wrongly at the data plane (fix).

**Repos containing `eq-canonical` strings** (raw hit counts, mostly docs/config — NOT a change-list):

- `eq-shell` (~60 — config, scripts, migrations, runbooks)
- `eq-cards` (~30 — docs + source + scripts)
- `eq-context` (~50 — narrative docs, low risk)
- `eq-intake` (SQL migration comments; edge fn already uses `-internal`)
- `eq-solves-field` (5 — `index.html` + a migration dated 2026-05-31)
- **Clean / absent:** `eq-design-tokens`, `eq-roles`, `eq-solves-service`, `eq-ui`, `sks-nsw-labour`

## B. Roles registry (`@eq-solutions/roles`) consumption

**Canonical model** (`eq-roles/roles/model.json`, v1.0.0) — 5 roles:
`manager · supervisor · employee · apprentice · labour_hire` (+ orthogonal `is_platform_admin`),
15 permissions across admin/audit/intake/equipment/reports.

| App | Consumes pkg? | Local model | Match to canonical |
|---|---|---|---|
| `eq-shell` | ✅ pinned `#main` (branch) | composes on top of pkg | n/a — reference consumer |
| `eq-solves-service` | ❌ | `super_admin · admin · supervisor · technician · read_only` (`lib/types/index.ts:3`) | **DIFFERENT** — only `supervisor` overlaps |
| `eq-solves-field` | ❌ | `manager · supervisor · employee · apprentice · labour_hire` (`scripts/permission-matrix.js`) | **names match** (but see note) |
| `eq-cards` | ❌ | none — no role logic | n/a |

Notes:
- **Shell pin = `#main`, not a tag.** A concurrent session is mid-migration moving consumers
  `#main` → consume-by-tag (`STATE.md:20`). **Owned — do not touch the roles/ui pins.**
- **Field:** role *names* match canonical, but a prior memory noted a "lossy 2-tier mapping" in
  Field. Confirm how Field actually uses roles before assuming a drop-in.
- **Service:** genuinely different semantic set (`super_admin/admin/technician/read_only` have no
  canonical equivalent) → migration needs a **mapping decision**, not a mechanical swap.

## C. Verification corrections (why this section exists)

The fan-out's roles agent asserted *"Service tiers identical to canonical — clean swap; Field
differs."* **Both backwards.** It never read `eq-roles/model.json`; it assumed Service's
`super_admin/...` set was canonical. Verified reality: canonical = `manager/.../labour_hire`, so
**Field's names match and Service's don't.**

On the record: fan-out gives breadth fast and cheap, but agent *verdicts* are leads, not facts.
The catch here cost one source read; shipping the verdict would have sent a window to do an
impossible "mechanical swap."

## D. Open decisions (Royce)

1. **Service role mapping** — decide how `super_admin/admin/supervisor/technician/read_only` map
   onto canonical `manager/supervisor/employee/apprentice/labour_hire` (or whether Service stays a
   documented variant). A read-only proposal can be drafted in a separate window — see handoff.
2. **Field** — confirm real role usage (the "lossy 2-tier mapping") before treating name-match as
   a drop-in.
3. **eq-canonical cleanup** — only after classifying each ref control-plane vs data-plane. Not a
   rename.
4. **Roles/ui tag-pinning** — owned by a concurrent session; leave alone.

# Core dashboard — signals board · build plan

**Date:** 2026-07-16 · **Owner:** Royce · **Status:** spec, not started
**Source:** dashboard reimagining session (2026-07-16) + live schema recon (ehow / zaap) + concept mockup `claude.ai/code/artifact/7a743d11`
**Aligns with:** [`access-model-cluster1-build-plan-2026-07-16.md`](access-model-cluster1-build-plan-2026-07-16.md) — this board is a consumer of the granular perm keys that plan introduces.

---

## Goal

Replace the current Core dashboard's prose brief + raw activity feed with a **scan-first signals board** that surfaces what canonical already computes and throws away. The board answers *"what needs me now"* across the apps, filtered per person by security group.

**Focus, in order: compliance → outstanding works (Service) → operations (crew).** Commercials are deliberately NOT a focus (see the governing principle). No pipeline view, no dollar aggregates.

---

## Governing principle — authority-scoped signals

> **A signal is only as loud as canonical's authority over the thing it describes.**

| Canonical's relationship to the data | What the board may do |
|---|---|
| **Owns the record** (compliance, service works, roster) | Speak with confidence — counts, countdowns, cross-app joins |
| **Partially mirrors** it (quote workflow state) | No aggregates, no forecasts. At most one unambiguous workflow nudge that is purely an EQ Ops step. |
| **Isn't the home** (revenue, invoicing, full commercials) | Say nothing. The board never implies it is the source of truth. |

**Why money is out:** Core is not the system of record for commercials — the real books live elsewhere — so any pipeline or revenue total it renders is partial by construction, i.e. confidently wrong. A quiet board beats a wrong one. Commercial *workflow* state that EQ Ops genuinely owns (a won quote with no job number) survives only as a gated nudge, phrased as a count + action, never a figure. See Appendix.

**Values rule for this whole document:** it encodes *relationships and sources*, never figures. No dollar amount, headcount, or threshold is baked in. What renders is whatever the tenant's data says that day; every band shows an honest empty state when a field isn't populated. Adoption fills data; it never reshapes the framework.

---

## The three bands

Each band is composed of signals the briefing engine (`netlify/functions/_shared/briefing-engine.ts`) **already fetches and currently discards** — so this is surfacing, not new plumbing.

### A · Compliance & safety *(EQ Cards + Field — canonical owns it)*
- Licences expired / expiring — countdown, not a total. Source: `app_data.licences`.
- Notifiable incidents open — the safety flag. Source: `app_data.incidents` (`notifiable_to_regulator`).
- **Rostered but non-compliant** — the hero cross-app join: a person on this week's roster whose credential has lapsed = *cannot legally be on site*. Source: `schedule_entries` × `licences`. Neither Field nor Cards knows this alone; canonical does. No money in it.

### B · Outstanding works *(EQ Service — canonical owns it)*
- Maintenance checks overdue.
- Open defects, by severity. Source: `app_data.asset_defects`.
- Service / calibration due. Source: `app_data.asset_calibration`.
- *Build-time verification:* confirm where Service work-orders live on the tenant plane (an `app_data`/`service` table vs `canonical_events` maintenance signals) before wiring the "checks overdue" tile.

### C · Operations & crew *(EQ Field — canonical owns it)*
- **Deployable crew** — supply waterfall: `staff.active` − rostered − on-leave − licence-lapsing-in-window. The licence-lapse subtraction is the value; the absolute bench is secondary. Source: `staff` × `schedule_entries` × `licences`.
- On today / on leave.
- **Horizon toggle: this-week / 2-week.** (This-week is dense today; 2-week becomes meaningful as rostering adoption improves — we build both, we don't hide the sparse one.)
- **Demand overlay** — `jobs.crew_required` for confirmed jobs whose window intersects the horizon; coverage from `schedule_entries.job_id` assignments; verdict = deployable − unmet demand. *Requires the migration below.* Uniform on both planes; empty-state until crew numbers are entered.

**Priority queue** sits above the three bands and ranks across them (compliance / safety first, operational gaps second). It reuses the existing `briefing_actions` dismissal memory. Money items never enter the ranking for anyone without the commercial perm.

---

## Endpoint & architecture

New Netlify function **`netlify/functions/signals.ts`** (GET, session-authed, per-tenant):

```
{ ok, generated_at, bands: { compliance?, works?, crew?, commercial_nudge? } }
```

- **Numbers from SQL, not AI.** The board renders from `/signals` directly — no Claude in the path, so it's instant and can't hallucinate. The AI brief becomes a thin narrative layer that consumes the *same* fetchers.
- **Server-side perm gate.** A band the caller can't see is never queried and never serialized — not hidden in the browser. This is the "function-gated / governed" pattern from the 2026-07-16 visibility audit; tenant-only RLS + UI hiding is the exposure we're closing.
- Needs a small server-side `can()` → port the ~6-line `useCan` logic into `netlify/functions/_shared/permissions.ts` (role matrix + `extra_perms`/`denied_perms` off the session). Reusable; the README already assumes it exists.
- Data via the service-role tenant client + direct `app_data` selects, exactly as `briefing-engine.ts` does today. **No new migrations for the three bands** (the one migration is band C's demand overlay, below).
- **Single-source rule:** any quote-status logic **imports from `src/modules/quotes/taxonomy.ts`** (locked by `taxonomy.test.ts`) — never a hardcoded status literal. Hardcoded literals are the root cause of the live briefing bug (`task_2f107212`, being fixed separately). Enabling refactor: promote the 5-stage board grouping out of `QuotesModule.tsx` (`STATUS_FILTERS`) into `taxonomy.ts` so the board and `/signals` consume one definition.

---

## Security-group gating (feature-level, v1)

Per-band gate via `useCan()` on the narrowest fitting key. Where cluster-1 introduces a better-fit granular key, the band adopts it — making this board a natural consumer of that work.

| Band | Gate (target) | Interim (until cluster-1 ships) |
|---|---|---|
| A · Compliance | `field.view_licences` (cluster-1) | `field.view` |
| B · Outstanding works | `service.view` | — (exists) |
| C · Operations / crew | `field.view` | — (exists). Hours/rates never shown, so `field.view_hours` / `field.view_rates` not required. |
| Appendix · commercial nudge | `quotes.view` | — (exists). No dollars shown → `ops.view_margins` not required. |

---

## Data sources — verified live (2026-07-16)

Structural facts confirmed against the live planes (recorded so the build doesn't re-assume):

- `quote`, `licences`, `staff`, `schedule_entries`, `sites`, `customers`, `jobs`, `asset_defects`, `asset_calibration`, `incidents` — present on **ehow (SKS)** in `app_data`.
- `tenders` / `tender_nominations` exist **only on zaap (EQ)**, dropped on ehow. → band C demand must NOT read tenders; it reads `jobs`.
- `app_data.jobs` (both planes) has `quote_id, status, started_at, target_completion, job_number` but **no crew-requirement column** → the one migration below.
- `schedule_entries.job_id` exists → crew-to-job coverage is already computable.
- EQ Ops quote board = **5 stages** from `STATUS_FILTERS` rolling up 16 status slugs; the taxonomy is the single source.

---

## Sequencing

- **Phase 0 — enabling refactor:** promote the 5-stage grouping into `taxonomy.ts`; add `_shared/permissions.ts` server `can()`. (Also unblocks the `task_2f107212` briefing fix.)
- **Phase 1 — the three bands:** `/signals` + bands A, B, C (supply side) + priority queue. All real on both planes today, no migrations.
- **Phase 2 — band C demand + migration:** add `app_data.jobs.crew_required` (via the One Pipe, both planes; confirm zaap `jobs` shape first), wire the coverage/shortfall verdict + horizon toggle's demand line.
- **Phase 3 — commercial nudge (Appendix):** gated, workflow-only.

---

## Constraints / do-not-touch

- **Build in a fresh `main`-based eq-shell worktree.** The `eq-ops-mobile-view` worktree drifted to a detached HEAD with no `netlify/` mid-session (concurrent-agent race) — do not build there.
- **No canonical DDL by hand.** The band-C column goes through `tenant-migrate.yml` (One Pipe), both planes, never the dashboard.
- **Every fetcher tolerates an absent table** (ehow has no `tenders`) exactly as `fetchNativePipeline` does (`42P01` / `PGRST205` → silent absence).
- **Deploy = push to `main` → Netlify auto-deploy. Explicit instruction only.**
- **No `field.view_hours` / `field.view_rates` / cost columns** anywhere in these bands — that's cluster-1's sensitive-read territory, out of scope here.

---

## Appendix — the one commercial nudge (gated, Phase 3)

The single money-adjacent item the authority principle permits: *"N quotes are won but have no job number."* It is a pure EQ Ops workflow step (create the job), phrased as a count + action, **no dollar amount, nothing about invoicing** (invoicing is external, so canonical can't be authoritative about it). Statuses sourced from `taxonomy.ts` (`verbal-win` + `won-awaiting-job-no`), gated behind `quotes.view`. Off the default board; appears only for commercial roles.

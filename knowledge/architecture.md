---
title: Knowledge — Architecture
owner: Royce Milmlow
last_updated: 2026-04-10
scope: Current state of how systems are built and how they fit together
read_priority: standard
status: live
---

# Knowledge — Architecture

Describes how systems are currently built. For the *decision* behind each
choice (alternatives considered, reasoning at the time), see
`knowledge/decisions.md`. This file is the "what", decisions.md is the "why".

---

## One Cloudflare Worker for Everything

**Decision:** Single `anthropic-proxy` worker shared across EQ Expenses, SKS Receipt Tracker,
and any future tools that need Anthropic API access.

**Why:** The worker does exactly one job — receive a request, attach the API key, forward it.
Nothing about that job is app-specific. One worker means one API key to manage, one deployment
to maintain, and zero friction when adding new apps.

**Implication:** Never create a per-app worker. Point new tools at the existing URL.

---

## One Supabase Project for Everything

**Decision:** eq-field-app (nspbmirochztcjijmcrx, Sydney) is the single Supabase project
for all workstreams — EQ products and SKS tools alike.

**Why:** Separate projects multiply management overhead (separate API keys, separate billing,
separate dashboards) for no architectural benefit at current scale.
Tenant separation via table prefixes (sks_, eq_) or schemas is sufficient and reversible.

**Implication:** Never spin up a new Supabase project. If a table feels crowded, add a prefix.

---

## Single-File HTML as Distribution Format

**Decision:** Internal tools are built as single index.html files with a Cloudflare Worker proxy.

**Why:** Solves three real problems simultaneously:
1. ThreatLocker and corporate endpoint security blocks Python, .exe, .bat files
2. Email security filters flag zip files containing executables
3. No IT involvement needed — open a file in Chrome, done

**Tradeoff:** localStorage instead of a real database, at least initially.
**Migration path:** localStorage → Supabase is a contained change. Data shape stays identical;
only read/write functions change. Design data models for Supabase from day one.

---

## localStorage First, Supabase When Ready

**Decision:** New tools start with localStorage, migrate to Supabase when multi-user
or cross-device sync is genuinely needed.

**Why:** localStorage removes all backend complexity during battle-testing.
Real usage reveals what the data model actually needs — designing for Supabase upfront
often means designing the wrong schema.

**When to migrate:** When any of these are needed:
- Multiple users with separate records
- Cross-device sync (start on work PC, continue on phone)
- Manager/approval workflow
- Automated email submission

---

## EQ Solves Field — URL-Based Tenant Detection

**Decision:** Tenant is detected from the URL subdomain/slug, not from login.

**Why:** Avoids auth complexity for field staff who just need to clock on.
Trade-off is that demo mode is controlled by a tenant slug ("eq") that bypasses Supabase entirely.
DEMO_FLAG comments mark every point that needs to be re-enabled for live tenants.

---

## AHD — New Build Preference

**Decision:** Target new build / house-and-land packages over established property.

**Why three reasons compound:**
1. Stamp duty savings (significant on $500K+)
2. Stronger depreciation schedules (Division 40/43 on new build)
3. Housing crisis alignment — new builds add supply; supports government engagement narrative

**Specific finding:** Two $500K new builds outperform one $750K established property
on every employee-relevant metric (yield, depreciation, per-employee bonus impact).

---

## CDC Solutions — PSI / Results Test

**Decision:** No further PSI testing required for CDC Solutions.

**Why:** CDC passes the Results Test on the Delta Elcom engagement:
- Milestone-based fees (not time-based)
- Liability sits with CDC (not Royce personally)
- Results Test pass means other PSI tests are irrelevant

---

## Delta Elcom Consulting — The Cliff

**Context:** Consulting fees via CDC Solutions are milestone-based invoicing through to INV-009
in January 2028 (final invoice). FY2028/29 is the "cliff" — consulting income drops to zero.

**Implication for planning:** CDC tax position changes dramatically from FY29.
AHD property income needs to be building before the cliff arrives.
Division 7A minimum yearly repayment ~$82,096/year from FY26/27 (first due 30 June 2027).

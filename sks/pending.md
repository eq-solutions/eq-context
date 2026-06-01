---
title: SKS — Pending
owner: Royce Milmlow
last_updated: 2026-06-01
scope: SKS Technologies operational TODO list
read_priority: critical
status: live
---

# SKS Pending

## Done (pruned summary — full history in git log)

- [x] EQ Quotes Supabase port — full Flask rewrite (v50+)
- [x] Fly.io deployment → quotes.eq.solutions
- [x] Cloudflare CNAME (proxy off), custom domain live
- [x] Migrations 001–019 applied to SKS live
- [x] Word doc generator (`app/documents/`) — SKS template + pack/unpack
- [x] Quote register filters — estimator dropdown, customer text, site text
- [x] Inline HTMX status select on quotes list (per-status badge colours)
- [x] Bulk status change
- [x] eq:toast listener — auto-dismissing flash banners
- [x] Customers list — "Job defaults" filter (missing ABN / invoice email / market vertical / end client)
- [x] Customers list — inline contact edit with datalist autocomplete
- [x] Cover page wrap — project name wraps at 24 chars/line
- [x] canonical-vs-alias customer model (v63 Path B)
- [x] Job Creation Template generator (xlsx download)
- [x] Cost-on-line-items, per-line margin chip, budget sheet
- [x] Clickable status journey nodes (v65)
- [x] Static asset cache-busting via content hash (`static_v()` helper)
- [x] Speed pass (v73–v75, 2026-05-23): parallel list queries, TTL-cached lookups, RPC fallback pattern for letter counts / sources / estimator initials
- [x] EQ Field sync (v78, 2026-05-24): migration 022 (`canonical_field_id` + `field_synced_at`), `/integrations/` admin + HTMX sync button, customer list badge, EQ Field `eq-service-sites.js` Netlify Function
- [x] UI collapsible accordions (2026-05-25): clarifications + subcontractors + one-off sections folded by default on quote form; labour and materials always expanded
- [x] OneOffCost Word row (2026-05-25): separate `{{OneOffCost}}` token in template_v3.docx between Subcontractors and Subtotal; row stripped when zero (legacy quotes unaffected); migration 023 (`scope_template_type`)
- [x] Smart-quote corruption fix (2026-05-25): U+201C/U+201D curly quotes in setup/contacts/customers routes.py caused SyntaxError on startup — fixed across all 3 files
- [x] Fly.io redeployment (2026-05-25): confirmed deploy method is `flyctl deploy` (not local Docker); Dockerfile restored after accidental removal; quotes.eq.solutions cert verified issued

## Apply when ready (no code change needed)

_Nothing pending — migrations 001–023 all applied._

## Done (this session — 2026-06-01)

- [x] Scott Hotson offer issued and accepted — Operations Lead, Client Services
- [x] Dino Cabal reporting line confirmed — reports to Richo (not Royce)
- [x] Ben Ritchie holiday email sent — pathway conversation booked
- [x] Personal operating system designed and set up:
  - Apple Notes "Brain Dump" note + Siri shortcut (voice capture)
  - iPhone widget for text capture
  - Outlook Tier 1 auto-flag + Read Later rules + Focused Inbox
  - Three Claude sweep prompts saved (standard / quick / end-of-week)
- [x] SKS NSW Delivery board designed — MS Planner, 6 time-buckets, 6 labels, 30 starter tasks seeded (PDF setup guide built)
- [x] NSW interactive org chart built — HTML, 61 people, discipline split (Electrical/Comms), discuss flags, filter strip. Ready for Mark meeting.
- [x] Talent acquisition playbook drafted — relationship-warming, trigger-watching, pace-matching with Dino

## Pending (added 2026-06-01)

- [ ] Book monthly check-in cadence with Richo (Michael Richardson)
- [ ] Tell Mark about catch-up conversations before starting (casual, no fanfare)
- [ ] Confirm Scott Hotson start date + written offer
- [ ] Schedule Simon Bramall catch-up — Equinix Account Lead conversation
- [ ] Hold Ben Ritchie coffee — first/second week back
- [ ] Schedule Simon + Matt three-way (Equinix rhythm + scope clarity)
- [ ] Koos Otto role redesign conversation — HV Technical Lead framing
- [ ] Pair Huon Henne with Leif as comms shadow — frame as deployment
- [ ] Launch weekly construction PM standup (Royce chairs initially, Ben presents LOTO)
- [ ] Set up MS Planner board (setup PDF at `SKS_NSW_Delivery_Planner_Setup.pdf`)
- [ ] Leif → Senior Comms Advisor reframe — demand-driven framing
- [ ] Wayne Rowe exit conversation — Mark to own
- [ ] Charlotte White → Project Coordinator scope definition

## Tools built (2026-06-01) — reference

| Deliverable | File | Format |
|---|---|---|
| NSW Operating Plan v2 | `SKS_NSW_Operating_Plan_v2.html` | HTML |
| Interactive org chart | `SKS_NSW_Org_Chart_Interactive.html` | HTML |
| Personal operating system setup | `Royce_Operating_System_Setup.pdf` | PDF |
| MS Planner delivery system setup | `SKS_NSW_Delivery_Planner_Setup.pdf` | PDF |
| Scott Hotson JD | `Scott_Hotson_Operations_Lead_SKS.docx` | Word |

## Active (in progress or blocked)

- [ ] **Workbench customer CSV import** — export from Workbench, map columns, dry-run first:
  `python scripts/import_workbench_customers.py customers.csv --dry-run`

## Test suite (pre-existing failures, not this session's scope)

The following tests were broken before this sprint and remain so:

- [ ] **Rewrite `test_calc.py`** — 24 tests still on int-cents model; money moved to Decimal
- [ ] **Rewrite `test_quotes_service.py`** — 3 tests need RPC-aware shape
- [ ] **Rewrite `test_schema.py`** — 6 tests expect SQLite file; need Supabase stub
- [ ] **Update `test_validation.py`** — section rename + Decimal math
- Target: ~91+ tests green on every commit (currently 91 green, 15 pre-existing failures)

## Open conversations (deferred from handoff-2026-05-22)

| # | Topic | Notes |
|---|---|---|
| 1c | **Smarter contact dedup** | Manual merge of any two contacts, phone-aware auto-detection |
| 2 | **Stop SimPRO mirroring at source** | Change next SimPRO sync to stop the customer × site denormalisation |
| 3 | **Per-customer cost-split ratio (Budget)** | Equinix ÷1.1, Ramsay ×0.4, etc. Add 5th customer column |
| 4 | **Auto-email Job Creation Template + status flip on download** | Verbal Win → Won-Awaiting Job No on send |
| 5 | **ABR API integration for ABN auto-fill** | abr.business.gov.au free lookup, "Look up ABN" button per customer |
| 6 | **Smart AI enrichment for customer fields** | Claude API: market_vertical + end_client from name; alias propagation |
| 7 | **Backfill missing invoice emails + ABNs** | After #5+#6 land |
| 8 | **Phase 3: drop legacy contact columns after soak** | **Phase 1 done 2026-05-23** (migration 021): `primary_contact_id` live, 323/518 FKs set. **Phase 2 done 2026-05-23** (v77): app reads via FK with legacy fallback, inline picker writes `contact_id`, dual-write soak started. **Phase 3 (v79):** migration 023 (was "022" — renumbered after EQ Field sync consumed 022) `DROP COLUMN contact, email, phone`; remove fallback branches. Safe after ≥24h soak. |
| E | **Group-level pagination on /customers** | 2-step query: DISTINCT names → fetch rows per page. PERF TODO in `customers.py:list_for_admin_grouped`. Trigger: >5k customers OR p95 >800ms after speed pass |

## Known gaps the team will hit

1. **ABN blank on every generated Job Creation Template** — paste once per customer via `/customers/<id>` → "Job creation defaults" → "ABN" inline edit
2. **Invoice email blank for Ramsay, Schneider, Metronode, 3/9 Equinix** — same path
3. **Cost data NULL on quotes before v62** — estimators should re-enter Cost values when editing older quotes

## Untouched substrate items

(Separate from EQ Quotes — preserve)

- [ ] Bring apprentice module from demo to SKS Labour prod
- [ ] Scale EQ Field App for Melbourne office demo
- [ ] R2 backup audit/download from Beelink desktop
- [ ] Scott Hotson hire finalisation
- [ ] One-on-one catch-up sessions with 8 key staff
- [ ] Comms portfolio growth under Royce

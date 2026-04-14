---
title: State — Products
owner: Royce Milmlow
last_updated: 2026-04-10
scope: Current live status of every EQ and SKS product
read_priority: standard
status: live
---

# State — Products

---

## EQ Solves — Field (v3.0.0)
**Status:** Live (demo branch)
**URL:** eq-solves-field.netlify.app
**Repo:** eq-solutions/eq-field-app (private), demo branch
**Working file:** index_demo.html
**Architecture:** PWA, URL-based tenant detection, Supabase backend (eq-field-app)
**Demo:**
- Tenant slug: "eq" (bypasses Supabase)
- Staff PIN: "demo" / Supervisor PIN: "demo1234"
- 18 generic staff, 7 generic sites, 5 weeks schedule from 06.04.26
- Network error toasts suppressed in demo mode
**Pending:**
- Netlify env var cleanup (delete SECRET_SALT, STAFF_HASH, MANAGER_HASH)
- Supabase rate_limits table clear on demo branch
- Multi-tenant scaling
- Stripe payments integration

---

## EQ Solves — Quotes (v1.8 Pro)
**Status:** Live
**URL:** eq.solutions/solves → quotes.html
**Architecture:** Single HTML file, vanilla JS, localStorage
**Key details:**
- Title is "EQ Solves — Quotes" — do not change
- Status values: "won" / "sent" / "draft" / "lost" (never "accepted")
- Demo: 6 quotes, 5 clients, 5 labour rates, 10 materials
- Setup overlay starts hidden
- v1.7 retired

---

## EQ Solves — Compliance (Beta, formerly EQ Ops)
**Status:** Beta
**URL:** eq.solutions → eq-ops.html
**Architecture:** Supabase-backed, Resend email notifications
**Content:** 27 items across 5 clients; 26 templates across 5 categories
- QA & Inspection, Compliance & Certificates, Site Safety (WHS),
  Project Administration, Meetings & Communications
**Demo:** bypasses Supabase auth via DOMContentLoaded block (DEMO_FLAG marked)
**Pending v1.1:**
- Auto-recurring work orders
- Multi-site filtering
- Audit trail

---

## EQ Expenses
**Status:** Live
**Architecture:** Cloudflare Worker proxy (anthropic-proxy) + single index.html
**Key rule:** API key lives in worker env var only — never in frontend

---

## Australian Housing Dividend (AHD)
**Status:** Pre-acquisition
**Entity:** EQ Property Solutions Pty Ltd (ACN 696 198 482, ABN 82 696 198 482)
**Structure:** Corporate property investment; rental income distributed as tenure-linked
  annual bonuses to CDC Solutions employees
**Bonus multiplier:** 1.0× at 1–2 years → 3.0× at 10+ years
**Target market:** Adelaide North corridor (SA) primary; Toowoomba (QLD) fallback
**Preference:** New build / house-and-land packages (stamp duty, depreciation, housing crisis alignment)
**Lending:** Corporate at 90% LVR via Liberty Financial or Pepper Money
**Legal docs pending solicitor review:** Intercompany Services Agreement, MIS Position Paper,
  Employee Incentive Scheme Policy v1.1
**Pending:**
- First property acquisition
- Solicitor engagement (ISA, MIS opinion, EISP)
- Government engagement letter (NSW Treasurer) ~6 months after first bonus paid

- 
## SKS Labour App (v3.3.7)
**Status:** Live
**URL:** sks-nsw-labour.netlify.app
**Repo:** eq-solutions/eq-field-app, **main branch only**
**Architecture:** Single-page PWA, vanilla JS (modularised into ~17 script files),
  Supabase backend, Netlify Functions for PIN auth + email + AI agent
**Users:** ~55 SKS NSW field staff and supervisors
**Key details:**
- Staff PIN: `2026` (read-only + staff timesheet self-entry)
- Supervisor password: `SKSNSW` (full edit)
- Service worker: network-first for JS/CSS/HTML, cache-first for icons (fixed in v3.3.7)
- Netlify Site ID: bd00e7db-09a4-4f0e-a996-105cd63b0c8b
- SKS tenant org_id: 1eb831f9-aeae-4e57-b49e-9681e8f51e15
**Reference:** see `SKS_LABOUR_APP.md` in the sks-nsw-labour repo for full technical details

---

## EQ Solves — Service
**Status:** Live
**URL:** eq-solves-service.netlify.app
**Architecture:** Single HTML file, Supabase backend
**Deploy:** GitHub CD

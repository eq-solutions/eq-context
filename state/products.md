---
title: State — Products
owner: Royce Milmlow
last_updated: 2026-04-18
scope: Current live status of every EQ and SKS product
read_priority: standard
status: live
---

# State — Products

---

## EQ Solves — Service (PRIMARY BUILD)

**Status:** Active development
**Architecture:** Next.js + Supabase + Netlify serverless functions
**Supabase project:** urjhmkhbgaxrofurpbgc (eq-solves-service-dev)
**Scale:** Production-level complexity, multi-tenant with Supabase RLS
**Test coverage:** 80 Vitest tests
**Sprint cadence:** 22 sprints to date
**Deploy:** GitHub → Netlify CD
**Blocker:** GitHub MCP write access (403) — fix at `github.com/settings/installations`

---

## EQ Solves — Field (v3.4.7)

**Status:** Live (demo branch)
**URL:** eq-solves-field.netlify.app
**Repo:** eq-solutions/eq-field-app (private), demo branch
**Working file:** index_demo.html
**Architecture:** PWA, URL-based tenant detection
**Supabase project:** ktmjmdzqrogauaevbktn (eq-solves-field) — bypassed in demo mode
**Deploy:** Netlify Drop (manual)
**Demo:**
- Tenant slug: "eq" (bypasses Supabase)
- Staff PIN: "demo" / Supervisor PIN: "demo1234"
- Generic SEED data (staff, sites, schedule)
- Network error toasts suppressed in demo mode
**Local repo (Beelink):** `C:\Users\EQ\eq-field-app-demo`
**Pending:**
- Netlify env var cleanup (delete SECRET_SALT, STAFF_HASH, MANAGER_HASH)
- Supabase rate_limits table clear on demo branch
- Multi-tenant scaling
- Stripe payments integration

---

## EQ Solves — Quotes (v1.8 Pro)

**Status:** Live
**URL:** eq.solutions → quotes.html
**Architecture:** Single HTML file, vanilla JS, localStorage
**Deploy:** Cloudflare Pages zip → eq.solutions (royce@ account)
**Key details:**
- Title is "EQ Solves — Quotes" — do not change (intentional)
- Status values: "won" / "sent" / "draft" / "lost" (never "accepted")
- Demo: 6 quotes, 5 clients, 5 labour rates, 10 materials
- Setup overlay starts hidden

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
**URL:** eq-expenses.netlify.app
**Architecture:** Cloudflare Worker proxy (anthropic-proxy) + single index.html
**Deploy:** Netlify Drop (manual zip)
**Key rule:** API key lives in worker env var only — never in frontend

---

## EQ Variations

**Status:** Live
**URL:** eq-variations.netlify.app
**Architecture:** PIN login, Supabase
**Deploy:** Netlify Drop

---

## SKS Labour App (v3.4.3)

**Status:** Live
**URL:** sks-nsw-labour.netlify.app
**Repo:** eq-solutions/eq-field-app, **main branch only**
**Architecture:** Single-page PWA, vanilla JS (modularised), Supabase backend, Netlify Functions for PIN auth + email + AI agent
**Supabase project:** nspbmirochztcjijmcrx (sks-labour) — **LIVE PRODUCTION DATA, DO NOT TOUCH**
**Users:** ~55 SKS NSW field staff and supervisors
**Key details:**
- Staff PIN: `2026` (read-only + staff timesheet self-entry)
- Supervisor password: `SKSNSW` (full edit)
- Service worker: network-first for JS/CSS/HTML, cache-first for icons
- Netlify Site ID: bd00e7db-09a4-4f0e-a996-105cd63b0c8b
- SKS tenant org_id: 1eb831f9-aeae-4e57-b49e-9681e8f51e15
**Reference:** see `SKS_LABOUR_APP.md` in the sks-nsw-labour repo for full technical details

---

## SKS Receipt Tracker

**Status:** Beta (local / battle-testing)
**Architecture:** Cloudflare Worker + SheetJS + single HTML
**Pending:** Worker deploy, battle-test, broader staff rollout

---

## Australian Housing Dividend (AHD) — PARKED

**Status:** Parked from public-facing materials; revisit 2027 for capital activation
**Entity:** EQ Property Solutions Pty Ltd (ACN 696 198 482, ABN 82 696 198 482)
**Structure:** Corporate property investment; two-pillar (Build and Earn); pilot = single residential property
**Bonus multiplier:** 1.0× at 1–2 years → 3.0× at 10+ years
**Target market:** Adelaide North corridor (SA) primary; Toowoomba (QLD) fallback
**Preference:** New build / house-and-land packages (stamp duty, depreciation, housing crisis alignment)
**Lending:** Corporate at 90% LVR via Liberty Financial or Pepper Money
**Legal docs pending solicitor review:** Intercompany Services Agreement, MIS Position Paper, Employee Incentive Scheme Policy v1.1

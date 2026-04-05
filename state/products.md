# State — Products

Last updated: 2026-04-05

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

## SKS Receipt Tracker (v2.0)
**Status:** Battle-testing
**Architecture:** Cloudflare Worker (shared anthropic-proxy) + single index.html + localStorage
**Distribution:** Share index.html directly or host as static file
**Export:** Weekly SKS-format Excel claim + FY summary (SheetJS, client-side)
**Pending:**
- Deploy Cloudflare Worker (anthropic-proxy)
- Configure Worker URL in Settings on each PC
- Battle-test: receipt scanning accuracy, weekly export, Excel compatibility
- Future: migrate localStorage → Supabase (eq-field-app, sks_ prefix) for multi-user

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

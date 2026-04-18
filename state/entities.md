---
title: State — Entities and Accounts
owner: Royce Milmlow
last_updated: 2026-04-18
scope: Entity register, bank accounts, registrations, infrastructure, contacts
read_priority: standard
status: live
---

# State — Entities and Accounts

---

## Key People

| Person | Role | Email | TFN |
|--------|------|-------|-----|
| Royce Wayne Milmlow | Founder EQ; NSW Ops Manager SKS | royce@eq.solutions | 148 480 381 |
| Emma Curth | Co-director CDC & EQ Property | — | 403 767 415 |
| Andrew (Webb Financial) | Tax agent | — | Agent 25818815 |

Royce Director ID: 036 71246 96371 17

---

## Entity Register

| Entity | ACN | ABN | TFN | Notes |
|--------|-----|-----|-----|-------|
| CDC Solutions Pty Ltd | 651 962 935 | 40 651 962 935 | 667 941 602 | GST-registered; trading as EQ |
| EQ Property Solutions Pty Ltd | 696 198 482 | 82 696 198 482 | Pending | Wholly-owned sub of CDC; inc. 14 Mar 2026 |
| Hexican Holdings Trust | — | 78 416 884 155 | 600 774 166 | ONGOING crypto vehicle; CGT investor; NOT winding down |
| Hexican Retirement SMSF | — | 19 430 978 586 | 695 444 143 | Members: Royce & Emma; trustee: Hexican Retirement Pty Ltd |
| Hexican Retirement Pty Ltd | 652 967 621 | — | — | SMSF trustee |
| Milmlow Holdings Pty Ltd | 644 247 870 | — | — | Trustee of Milmlow Family Trust; Royce sole director; review Sept 2026 |
| Milmlow Family Trust | — | 45 912 584 600 | — | Active |
| Allcraft Solutions Pty Ltd | 644 256 806 | 93 644 256 806 | — | Corporate beneficiary of MFT |
| Favour Perfect | — | 16 443 133 034 | — | Emma's sole trader entity |

---

## Bank Accounts

| Entity | Bank | BSB | Account |
|--------|------|-----|---------|
| CDC Solutions | NAB | 082-356 | 32 366 3466 |
| EQ Property Solutions | NAB | 082-356 | 969576812 |
| Hexican Retirement SMSF | ANZ | 012-141 | 1134-00385 (name: Hexican Retirement Pty Ltd ATF Hexican SMSF) |

---

## Key Registrations

| Item | Detail |
|------|--------|
| EQ Trademark | TM No. 2635095; Classes 35 & 36; filed 18 Mar 2026; accepted early 1 Apr 2026 |
| EQ Business Name | Transferred to CDC Solutions 15 Mar 2026; ref 1-YKBH77R; valid to Nov 2026 |
| GST | CDC Solutions registered |

---

## Infrastructure Accounts

| Service | Account | Notes |
|---------|---------|-------|
| Supabase | Three projects (see table below) | Do NOT assume one project anywhere |
| GitHub | eq-solutions org + milmlow user | All repos private; MCP is read-only (403 on writes) |
| Cloudflare | royce@eq.solutions | Pages + Workers + R2 (sks-assets, eq-assets buckets) |
| GoDaddy | — | Domain registrar only |
| Netlify | dev@eq.solutions | All Netlify sites (EQ + SKS) |
| Beelink | beelink.eq.solutions (Cloudflare Tunnel) | Ryzen 7 7735HS, 32GB RAM, 1TB NVMe; Chrome Remote Desktop |

### Supabase Projects

| Project ID | Name | Purpose | Access rule |
|---|---|---|---|
| `nspbmirochztcjijmcrx` | sks-labour | **Live SKS staff production data** | **Never touch unless "SKS live" is explicit** |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | EQ Field demo backend | Demo environment |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Canonical context store (claude_context table) | Paid/active; primary path for context reads/writes |

---

## Key Contacts

| Person | Role | Notes |
|--------|------|-------|
| Mark Brame | Delta Elcom | Invoice recipient; Unit 27/10 Gladstone Rd Castle Hill NSW 2154 |

---

## SKS Team (NSW)

| Person | Role |
|--------|------|
| Simon Bramall | Project Manager |
| Leif Lundberg | Job / Project Manager |
| Jack Cluff | Job / Project Manager |
| Federico Sander | Job / Project Manager |
| Nathan Anderson | Job / Project Manager |
| Matthew Miller | Equinix supervisor |

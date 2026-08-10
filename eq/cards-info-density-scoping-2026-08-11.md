---
title: EQ Cards — Information Density Scoping
owner: Royce Milmlow
last_updated: 2026-08-11
scope: Scope which EQ Cards screens over-show info by default and what should collapse behind a tap — feeds a future build session, no code changed
read_priority: normal
status: live
---

# EQ Cards — Information Density Scoping

Punch-list #4 (`system/punch-list.md`): "Cards is very heavy on information —
simplify or collapse unless a user clicks around." This scopes it: which
screens, what stays visible by default, what collapses. Research only — no
code touched this session.

## Method

Read every screen under `lib/features/*/presentation/screens/` in eq-cards
(`C:\Projects\eq-cards`), sized by line count, plus the app shell/router
(`lib/core/shell/home_shell_screen.dart`, `lib/core/router/app_router.dart`)
to confirm what's actually reachable. Two bottom-nav tabs: **Wallet**
(`licences_list_screen.dart`) and **Profile** (`profile_screen.dart`).
Everything else is reached by tapping through from one of those two.

## Priority ranking

| Screen | File | Lines | Verdict |
|---|---|---|---|
| Wallet (home) | `licences/presentation/screens/licences_list_screen.dart` | 2,022 | **The outlier — real fix needed** |
| Licence detail | `licences/presentation/screens/licence_detail_screen.dart` | 1,088 | One concrete fix (metadata rows), otherwise fine |
| Settings | `settings/presentation/screens/settings_screen.dart` | 1,224 | Standard grouped-rows list, self-hides by role — not the problem |
| Licence add/edit form | `licences/presentation/screens/licence_edit_screen.dart` | 1,429 | Out of scope — active task, not a browse screen |
| Profile | `profile/presentation/screens/profile_screen.dart` | 764 | Fine as-is |
| Worker HR record | `workers/presentation/screens/worker_hr_record_screen.dart` | 210 | Already a model — no change |
| Connect to a company | `connections/presentation/screens/connect_to_company_screen.dart` | 380 | Fine as-is |
| Show (QR display) / Share (public verify) | `show_screen.dart` (271) / `share_licence_screen.dart` (321) | — | Already a model — no change |

---

## 1. Wallet (home tab) — HIGH, the real target

`lib/features/licences/presentation/screens/licences_list_screen.dart`

### Current default state (populated wallet)

Scrolling straight down, before the user reaches their own licence list:

1. AppBar — title, scan button, Add button
2. Offline banner (only when offline)
3. Wallet health card — **already** collapses to one quiet line when
   everything's valid (good existing pattern, no change needed)
4. "Needs attention" — header + up to 4 urgent tiles, full-size
5. Pending connections banner
6. Required-by-org strip (org asks for a credential you don't have yet)
7. Setup checklist card (3 steps: add a ticket / complete profile / connect
   to employer)
8. Outgoing requests banner
9. Wallet completion nudge (shows when <6 items and no org requirements)
10. Add-to-home-screen nudge
11. Search + filter bar
12. Full licence list — **including the same urgent items from step 4, a
    second time**
13. Wallet ID card (name, role, company, worker ID, issued date, Show
    button) — at the very bottom

Items 4–10 already self-hide when their own condition isn't met — that part
of the code is well-written and the build comment even documents a
deliberate priority order for them. The actual problem is what happens when
several are true **at once**, which is exactly the new/mid-setup worker this
punch-list item is about: an org that requires a White Card they haven't
uploaded yet, one pending connection, and a wallet with 3 licences produces
**7 stacked cards** (health, needs-attention, pending-connections,
required-by-org, setup-checklist, completion-nudge, add-to-home) before the
user reaches their own wallet content — some of which then repeats a second
time further down.

### Proposed split

**Stays always visible:**
- Wallet health card, as-is (already collapses when healthy)
- Urgent items (expiring/expired) — shown **once**, not twice
- The licence list itself, with expiry badges and the renew CTA inline —
  never hide these, they're the safety/compliance content
- Search/filter bar — but only once the list is long enough to need it (see
  below)

**Collapse behind a tap:**
- Merge the five "nudge" cards — pending connections, required-by-org,
  setup checklist, outgoing requests, completion nudge — into **one
  collapsible "To do" summary**. Collapsed by default to a single line
  ("3 things need a look") with a chevron; tapping expands it in place to
  the individual cards, in their existing priority order. Nothing gets
  hidden permanently, it's one tap away, and the worst case drops from 5
  stacked cards to 1.
- Add-to-home-screen nudge — already the lowest-priority item; fold it into
  the same collapsed summary instead of its own separate strip.
- Search/filter bar — hide until item count crosses the threshold the code
  already uses elsewhere on this screen (`items.length < 6`, currently
  gating the completion nudge) — no reason to show search/filter chrome for
  a 2-licence wallet.
- Wallet ID card — leave its content as-is, it's already compact (avatar,
  name, role, company/ID/issued row, a "Show" button). Move it from the
  bottom of the list to a collapsed strip near the top (name + "Show ID"
  button), with the full card one tap away via the existing `ShowScreen`.
  Today a user has to scroll past their entire wallet to reach their own ID.

**Never hide:** expiry badges on tiles, the renew CTA on expiring/expired
items, the health-card counts. These already render inline on every tile —
no change needed, just don't let the collapse work touch them.

### De-dupe

Urgent items currently render twice: once in "Needs attention" (top 4) and
again in the full filtered list below. Keep "Needs attention" as a pinned
top section (surfacing what's expiring first is the right instinct) and
exclude those same items from the main list beneath it, so nothing repeats.

### Size: Medium

No new data or providers needed — every piece of data (credential gaps,
counts, pending/outgoing requests) is already fetched and rendered
somewhere on this screen today. The work is a new collapsible-summary
wrapper widget, reordering existing widgets into/out of it, and removing
the tile duplication. Touches one screen file plus possibly one small new
shared widget. No backend change.

---

## 2. Licence detail — LOW, one concrete fix

`lib/features/licences/presentation/screens/licence_detail_screen.dart`

Single-record detail view: Number, Issued, Expires (with expiry badge),
State, Issuing authority, then `_metadataRowsFor(licence)` — **every key in
the licence's `metadata` map, unbounded** — then Notes. Rows only render
when the field has a value, which is already correct collapsing for the
core fields.

The one real gap: `_metadataRowsFor` has no cap. A licence type with several
OCR-extracted metadata fields (e.g. an electrical licence with
class/endorsements/conditions) renders every one of them as an equal-weight
row mixed in with the core identifying fields, with no visual distinction
between "the licence" and "extra scanned detail."

**Proposal:** cap metadata rows to the first 2–3 by default, with a "Show N
more details" row that expands the rest in place. Number / Issued / Expires
/ State / Authority always stay visible (identifying + compliance info);
metadata is genuinely secondary.

Note: this screen has three interchangeable layouts (`_LinearDetail` /
`_WalletDetail` / `_PhotoFirstDetail`) gated by a user-facing
Settings → Design picker (`core/design/design_version.dart`) — a
deliberate, already-shipped feature letting a worker pick their preferred
visual style, not dead code or an A/B leftover. Any fix here needs applying
identically across all three variants, since metadata rows render the same
way in each.

### Size: Small

---

## 3. Profile — LOW, fine as-is

`lib/features/profile/presentation/screens/profile_screen.dart`

Already well-sectioned: avatar header, personal-details card (6 fields;
blanks show a dash rather than being hidden, which is fine — it's the
user's own record), workspaces (only shown when 2+ tenants), team/join-QR
(only for managers/supervisors), companies, account. Sections that don't
apply already collapse to nothing. No change proposed.

---

## 4. Worker HR record (APP 12 self-service) — model, no change

`lib/features/workers/presentation/screens/worker_hr_record_screen.dart`

Already exactly the pattern the punch-list item is asking for elsewhere:
Personal / Address / Emergency contact / Right-to-work sections, each one
collapsing to nothing (`_Section` returns `SizedBox.shrink()`) when none of
its fields are populated. Worth using as the reference pattern when
building the Wallet fix in §1.

---

## 5. Connect to a company — LOW, fine as-is

`lib/features/connections/presentation/screens/connect_to_company_screen.dart`

Short and single-purpose: a scope choice (full vs basic sharing) plus a list
of companies to apply to. Not dense. No change proposed.

---

## 6. Settings — LOW, not the target

`lib/features/settings/presentation/screens/settings_screen.dart` (1,224
lines — second-largest file in the app, but a settings screen is expected
to be a long list)

Standard grouped-rows pattern (Admin / Platform / Team / Workspaces /
Account / Design / Privacy / Legal / Help & feedback), and each section
already conditionally hides for the audience it doesn't apply to (Admin and
Platform sections only for admins, Team/Workspaces only when relevant).
It's long because it's a settings list a user navigates via scroll-and-tap,
not a dashboard meant to be read in full on open — that's the correct
interaction model already. No change proposed.

---

## 7. Show / Share screens — model, no change

`licences/presentation/screens/show_screen.dart` (fullscreen high-contrast
site-gate display) and `share_licence_screen.dart` (public no-auth
verification page). Both already minimal by design — name, type, number,
expiry, nothing else. Cited here as the existing house style for "show only
what the moment needs" — the target to bring the Wallet screen closer to.

---

## Out of scope this pass

- **Licence add/edit form** (`licence_edit_screen.dart`, 1,429 lines) — a
  form the user actively fills in for one task, not a browse/dashboard
  screen. Progressive disclosure of optional fields could be its own
  scoping exercise if it comes up separately.
- **Admin screens** (`admin_worker_detail_screen.dart`,
  `admin_members_screen.dart`, `platform_console_screen.dart`) —
  admin/platform-admin-only audience, not the everyday worker experience
  the original brain-dump was about.
- `card_screen.dart` (710 lines, `features/card/`) — appears to be dead
  code: the router redirects the legacy `/card` route straight to the
  Wallet tab (its own comment says "3→2 tab merge") and nothing else in the
  app references `CardScreen`. Not part of this density scoping; flagged
  separately for cleanup.

## Recommended build order

1. Wallet nudge-stack collapse + de-dupe (§1) — this is the actual "very
   heavy on information" complaint.
2. Metadata-row cap on licence detail (§2) — small, same spirit, cheap to
   ship alongside #1.
3. Everything else in this doc — no action needed.

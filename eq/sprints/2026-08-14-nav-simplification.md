---
title: Sprint — Suite-wide Navigation Simplification
owner: Royce Milmlow
last_updated: 2026-08-14
scope: Code-level nav/menu audit across Shell/Field/Service/Cards, Royce's picks off the resulting decision sheet, and the fixes built same-session. Triggered by "how do we make the average user experience feel easier" — what would Atlassian/Microsoft do at this stage.
read_priority: standard
status: live
duration_estimate: Closed. All 7 buildable items merged (CARD-1, SHELL-1/2/3/4, FIELD-2, SERVICE-1/2). SUITE-1 doc written. FIELD-1 reviewed and closed with no action — the audit's framing was wrong, the split was a deliberate prior decision, not cruft. CARD-2/FIELD-3 confirmed no action.
shipped: CARD-1 (eq-cards#243), SHELL-1 (eq-shell#1344), SHELL-2/3/4 (eq-shell#1343), FIELD-2 (eq-field#697), SERVICE-1 (eq-service#730), SERVICE-2 (eq-service#729) — all merged. SUITE-1 doc merged (eq-context#155).
pending: none — sprint closed.
---

# Sprint — Suite-wide Navigation Simplification

**Status:** closed. All 7 buildable items merged. SUITE-1 doc merged. FIELD-1 reviewed and closed with no action after a pre-build check found the audit's own framing was wrong — see its entry below. CARD-2/FIELD-3 confirmed no action, as decided on the sheet.

---

## Objective

Royce asked, after a long production-readiness push: is a user manual worth writing, and what would a company like Atlassian or Microsoft do at this stage to make the suite feel easier to use. The answer was: cut menu depth and fix drift before writing anything — a manual documents complexity that shouldn't exist in the first place. That became a full code-level nav audit of all four live apps (not a docs read — the running code), a decision sheet Royce triaged item-by-item, and same-session builds for everything he marked "Do it."

---

## How the audit was run

Four parallel agents read the actual navigation source in each repo (not `eq/products.md`, not old sprint docs) and produced a structured inventory: every top-level nav item, how each is gated, and anything that looked redundant or dead. Findings were published as an interactive decision sheet (artifact, saved to Royce's OneDrive) — 14 items, each with a recommendation, effort/risk tags, and a Do it / Later / Skip control plus a notes field. Royce triaged the whole list in one pass and copied his decisions back into chat.

**Destination counts found** (base role → manager/admin):

| App | Base role | Manager / admin |
|---|---|---|
| Shell | 7–8 (mobile as few as 2) | +9 sidebar items → 16 AdminHub tiles |
| Field | 12 (apprentice: 5) | 21–22 |
| Service | 8 standalone / 5 embedded | +8 tiles |
| Cards | 2 tabs + 1 settings push | + Team admin / Platform console |

---

## In-scope items

### CARD-1 — Cards Profile/Settings duplicate widgets

**Why:** Settings re-implemented the workspace switcher and manager join-QR card that already live on Profile. Confirmed via git history: accidental — the QR card was added to Settings only (PR #66), the Profile copy was pasted in later during a 3→2 tab nav merge (PR #75) instead of reusing what existed.

**Done.** Removed from Settings, kept on Profile. [eq-cards PR #243](https://github.com/eq-solutions/eq-cards/pull/243) — **pushed, open.**

**Status:** ✅ Done, PR open.

---

### SHELL-1 — Reports had two doors, now a real landing page

**Why:** AdminHub's "Reports" tile (gated on the umbrella Admin-section permission) and MobileTabBar's "GM Reports" tab (gated `reports.view`) both landed on the exact same page — today `/reports` was entirely the GM Reports module, nothing else. Royce's direction, reframing the original small fix: "we need a report homepage and then a GM report as an option."

**Verified before building, not assumed:** `GmReportsModule` already wraps all its content in `<Gate perm="reports.view">` (`gm-reports/index.tsx:1300`), so inserting an index page in front of it changes no permission behaviour — confirmed by reading the code, not inferred.

**Built:** new `ReportsIndex` page at `src/pages/ReportsIndex.tsx`, matching AdminHub's existing tile-grid visual pattern. Route split: `/reports` (exact) → `ReportsIndex`; `/reports/gm/*` → `GmReportsModule` (unchanged internally, still its own lazy chunk). One live card today: "GM Reports." AdminHub's tile and MobileTabBar's tab both still point at bare `/reports` — no gate changes on either. A third door (a `⌘K` command-palette "Reports" entry, found during the build, not in the original audit) also correctly lands on the new index with no change needed.

**Done.** [eq-shell PR #1344](https://github.com/eq-solutions/eq-shell/pull/1344) — merged.

**Status:** ✅ Merged.

---

### SHELL-2 — Admin sidebar undersold AdminHub

**Why:** Sidebar's Admin section listed 9 items; the "Overview" link it contains actually opens AdminHub, which renders 16 tiles — including a full parallel Service admin set never mentioned in the sidebar at all.

**Built:** lowest-risk fix, per the original recommendation's explicit scope constraint — relabelled "Overview" → "All admin tools" (`HubSidebar.tsx:154`) so the link signals it's the full index, not a redundant home button. Did not restructure the sidebar to list all 16 tiles — that was explicitly out of scope for this pass.

**Done.** [eq-shell PR #1343](https://github.com/eq-solutions/eq-shell/pull/1343), commit `5f1f518f` — merged.

**Status:** ✅ Merged.

---

### SHELL-3 — "Import Coupa" named a vendor in a nav label

**Why:** A literal customer/vendor name was baked into a nav menu label inside Ops's "More" dropdown — contra the product-copy-genericization rule already applied everywhere else in the suite.

**Done:** relabelled to "Import purchase orders" (`QuotesModule.tsx:7092`), verified against the actual import behaviour first. [eq-shell PR #1343](https://github.com/eq-solutions/eq-shell/pull/1343), commit `2144a141` — merged (same PR as SHELL-2, one cleanup batch).

**Status:** ✅ Merged.

---

### SHELL-4 — Dead `/quotes`, `/eq-quotes` redirect routes

**Why:** Two routes doing nothing but `Navigate` to `/ops`, kept for old bookmarks — not in any menu, nothing to simplify by removing them. Royce's explicit call, overriding the original "leave as-is" recommendation: *"Remove these references - save finding them again and again."*

**Done:** both routes deleted (`App.tsx:782-784`). Grepped first to confirm nothing else in the repo constructs a link expecting the redirect. [eq-shell PR #1343](https://github.com/eq-solutions/eq-shell/pull/1343), commit `8e134384` — merged (same PR as SHELL-2/3).

**Status:** ✅ Merged.

---

### FIELD-2 — Add Person: visible to workers on desktop, gated on mobile

**Why:** Desktop's "Add Person" button had no manager/supervisor gate; the mobile drawer's equivalent item did — same action, inconsistent rule per surface. Royce: "Supervisor and manager will be adding people."

**Verified before building:** Field doesn't track manager and supervisor as separate flags — `isManager` is a single "supervision unlocked" flag already covering both (PIN-unlock path checks `role === 'supervisor'` against a broad category allowlist; Shell-JWT handoff grants it for any non-employee role). So "supervisor or manager" maps directly onto the existing `.edit-only` mechanism — no new gating logic needed, just applying the class desktop was missing.

**Done:** added `edit-only` to the desktop button (`index.html`, was line 11361). Mobile's equivalent was already correct. Version-stamp bumped and a reflection-log entry added, matching this repo's own convention for permission-gating fixes. 27/27 tests pass, bundle-check clean. [eq-field PR #697](https://github.com/eq-solutions/eq-field/pull/697) — merged, **live on field.eq.solutions**.

Landed as v3.5.498, not v3.5.497 as first built — a concurrent hotfix (Email Templates nav visibility, #696) claimed 3.5.497 on `main` first. Rebased on top of it, kept both changelog/reflection-log entries, renumbered, re-ran the full test suite (27/27) and bundle-check clean, force-pushed, then merged.

**Found in passing, spun off separately (not built here):** 3 more buttons with the identical ungated bug — Contacts "Add Contact," Managers "Add Contact," Editor "Add Person." Flagged as its own background task; **that task ran and merged separately** as [eq-field PR #698](https://github.com/eq-solutions/eq-field/pull/698) (v3.5.499).

**Status:** ✅ Merged, live.

---

### SERVICE-1 — Same shape as SHELL-2, one Admin row hiding 8 tiles

**Why:** Service's Admin sidebar entry hides Users, Workspace Settings, Media Library, Report Settings, Archive, Audit Log, Imports, Backup, Activity behind one row — same undersell pattern as Shell.

**Held, then built.** `app/(app)/admin/page.tsx` had an active branch, `fix/admin-hub-role-gate`, from Royce's own separately-running security task (adding a read-side role check). Held to avoid a merge collision; started once that branch merged as [eq-service PR #728](https://github.com/eq-solutions/eq-service/pull/728). The actual fix landed in `components/ui/Sidebar.tsx`, not `admin/page.tsx` — relabelled the sidebar's single "Admin" link (which sat directly under an identically-worded "Admin" section header) to "All admin tools," same fix as SHELL-2, no collision with #728 after all once the real edit location was found.

**Done.** [eq-service PR #730](https://github.com/eq-solutions/eq-service/pull/730) — merged. `tsc --noEmit` clean.

**Status:** ✅ Merged.

---

### SERVICE-2 — Embedded nav had fewer stops than standalone

**Why:** The Shell-embedded top bar for Service silently omitted Today, Search, and Settings — not gated out, just never added when that bar was last touched, so it hand-drifted out of sync with the standalone sidebar.

**Done:** added the three missing items, each carrying the exact gating condition its standalone-sidebar counterpart uses (e.g. Insight/Records both check `role !== 'employee'`), not just added visually. Stayed clear of `admin/page.tsx` per the same SERVICE-1 collision-avoidance. `tsc --noEmit` clean. [eq-service PR #729](https://github.com/eq-solutions/eq-service/pull/729) — merged, **live on service.eq.solutions**.

**Status:** ✅ Merged, live.

---

### SUITE-1 — Nav-access matrix, written down on purpose

**Why:** Field and Shell already do heavy progressive disclosure by role — via three (really four, once Field's own internal stack is counted) independently-built mechanisms with no shared vocabulary. Every drift item above (Cards' duplicate widgets, Field's Add Person, Service's embedded nav) traces to exactly that: a gate added or changed on one surface, never mirrored on its sibling.

**Done:** [eq/identity/nav-access-matrix.md](../identity/nav-access-matrix.md) — per-app mechanism table, the three drift incidents as concrete evidence, and two options (shared config vs. a lighter review checklist) left open as Royce's call, not decided here.

**Status:** ✅ Done, this commit.

---

### FIELD-1 — Site Audits and Records, one page split into two entries

**Why (original framing, wrong):** the initial code-level audit found both routing through the same underlying safety page/tab and called the split "historical reasons" — implying leftover cruft, not a real design choice.

**Correction (2026-08-14, before building):** Royce asked to start this after initially marking it "Later." Before touching code, checked `index.html`'s own changelog (v3.5.342) rather than build from the audit's framing alone — it directly contradicts it. Site Audits and Records were originally tabs inside one page; Royce explicitly asked for them to become separate flat sidebar entries instead, rejecting the merged/tabbed layout on purpose: *"Prestarts/Toolboxes/Site Audits/Records/Report/Test Equipment should ALL be direct entries under one collapsible Safety group — not a separate 'Site Reports' hub tile plus a 'Safety' tile whose own page had internal Site Audits/Records tabs."* This is a previously-made, deliberate UX decision, not an oversight — merging them back would reverse it, not fix anything.

**Not built.** Surfaced the correction and asked before proceeding rather than build against a decision already on record. Royce's call, informed: leave them separate.

**Status:** ✅ Reviewed, closed — no action. Not the same as "Skip" above (CARD-2/FIELD-3, where the recommendation itself was to leave alone) — this one reverses what the decision sheet said, because the decision sheet's own premise was wrong.

---

### CARD-2 / FIELD-3 — Reviewed, left alone

- **CARD-2** — `/card`, `/certificates` dead redirects: kept specifically for live SMS/email onboarding links (Cards is taking real signup traffic). Real risk to remove, zero UX benefit. Royce: Skip.
- **FIELD-3** — Diary / PIN Management / Site Reports hub orphaned code: already fully invisible in nav; PIN Management explicitly held for a future labour-hire tier. Code hygiene, not a UX change, and touches a real data model (`site_diaries`). Royce: Skip.

**Status:** ⏸ Confirmed no action, both.

---

## Not part of this sprint, found in passing

Two access-control gaps turned up as a side effect of reading the nav code closely — different workstream (hardening, not UX), spun off as their own background tasks the same session, both **already running independently, started by Royce directly**:

- **Field** — several manager-only pages are nav-hidden via CSS only, with no server/JS route guard behind them (a direct link still opens them for a worker). Branch: `claude/route-access-guards`.
- **Service** — `/admin/*` pages have no read-side gate, only the mutations inside are checked. Branch: `fix/admin-hub-role-gate` (this is the branch SERVICE-1 above is sequenced behind).

Not tracked further here — they're their own thread.

---

## Substrate finding, also not part of this sprint

While pulling this sprint doc's template, found the shared `C:\Projects\eq-context` checkout is **41 commits behind `origin/main`** with three files (`digest.md`, `suite-state.md`, this repo's own sprint-doc template) sitting mid-merge-conflict (`git status` shows `UU`), and three more files (`sessions/2026-08-03.md`, `sessions/2026-08-13.md`, `system/failures.md`) with literal `<<<<<<<` conflict markers already **committed into history**, not just a dirty working tree. A repo-level guard (`guard.js`'s `stale-main-gate`, added after an 2026-08-08/09 incident with the same shape) correctly blocked a direct commit on that stale `main` — but its worktree-detection regex only matches paths containing `/worktrees/` or ending `-wt`, so a worktree created anywhere else (e.g. the session scratchpad directory) gets misclassified as "not a worktree" and blocked too. Worked around by relocating to the `<repo>\.claude\worktrees\<name>` convention every other repo already used this session. Both are real, separate findings — not fixed here, flagged for their own pass.

---

## Sprint success criteria

- [x] CARD-1 — de-duped, [eq-cards#243](https://github.com/eq-solutions/eq-cards/pull/243) merged
- [x] SHELL-1 — Reports landing page, [eq-shell#1344](https://github.com/eq-solutions/eq-shell/pull/1344) merged
- [x] SHELL-2 — AdminHub relabel, [eq-shell#1343](https://github.com/eq-solutions/eq-shell/pull/1343) merged
- [x] SHELL-3 — vendor name removed from nav label, same PR, merged
- [x] SHELL-4 — dead redirects deleted, same PR, merged
- [x] FIELD-2 — Add Person gated to supervisor+manager, [eq-field#697](https://github.com/eq-solutions/eq-field/pull/697) merged, live
- [x] SERVICE-1 — Admin sidebar relabel, [eq-service#730](https://github.com/eq-solutions/eq-service/pull/730) merged
- [x] SERVICE-2 — embedded nav parity, [eq-service#729](https://github.com/eq-solutions/eq-service/pull/729) merged, live
- [x] SUITE-1 — nav-access-matrix.md written, [eq-context#155](https://github.com/eq-solutions/eq-context/pull/155) merged
- [x] FIELD-1 — reviewed after Royce asked to start it; found the split was a deliberate prior decision (v3.5.342), not cruft — closed with no action, corrected on the record above
- [x] CARD-2 / FIELD-3 — confirmed no action

## Where to start

Sprint's closed — every item resolved one way or another. What's still open, not part of this sprint: Field's 3-more-ungated-buttons follow-up (already merged as eq-field#698, separate task), and the eq-context stale-checkout/conflict-marker finding (spun off as its own task, running in a separate session as of this doc).

---

## Related

- [eq-context/eq/identity/nav-access-matrix.md](../identity/nav-access-matrix.md)
- [eq-cards PR #243](https://github.com/eq-solutions/eq-cards/pull/243) — merged, Profile/Settings de-dupe
- [eq-shell PR #1344](https://github.com/eq-solutions/eq-shell/pull/1344) — merged, Reports landing page
- [eq-shell PR #1343](https://github.com/eq-solutions/eq-shell/pull/1343) — merged, AdminHub relabel + vendor-name fix + dead-route deletion
- [eq-field PR #697](https://github.com/eq-solutions/eq-field/pull/697) — merged, live, Add Person gating fix
- [eq-field PR #698](https://github.com/eq-solutions/eq-field/pull/698) — merged, live, the 3-more-buttons follow-up
- [eq-service PR #729](https://github.com/eq-solutions/eq-service/pull/729) — merged, live, embedded nav parity
- [eq-service PR #730](https://github.com/eq-solutions/eq-service/pull/730) — merged, Admin sidebar relabel
- [eq-context PR #155](https://github.com/eq-solutions/eq-context/pull/155) — merged, nav-access-matrix.md

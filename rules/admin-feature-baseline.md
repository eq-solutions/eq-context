---
title: Admin Feature Baseline
owner: Royce Milmlow
last_updated: 2026-08-04
scope: Minimum bar for a new admin/data-management surface (upload, list, lifecycle, export) before calling it done — check eq-ui first, most of it already exists
read_priority: high
status: live
---

# Admin Feature Baseline

Any new admin surface that manages a list of records — upload, register/list, lifecycle, export — should clear this bar before being called finished. Written after the Document Sign-off Register's first real critique (2026-08-04, Royce clicking through the live Upload & push / Register / Templates tabs) found the same handful of gaps a fresh admin build keeps re-discovering from scratch: no archive path, no bulk action, no pagination, a hardcoded taxonomy, an empty state with no way out.

**Distinct from `rules/non-negotiables.md`.** Those are hard rules that block work outright (security, auth, entities). This is a quality bar — missing an item here doesn't block shipping, but every miss should be a conscious call flagged in the PR or the session log, not a silent gap someone re-discovers by clicking around later. Same spirit as `CLAUDE.md`'s Completion Standard: resolve it, defer it with a reason, or say why it doesn't apply — silence isn't one of the options.

---

## Check eq-ui first — most of this already exists

Before building any of the below from scratch, check whether `@eq-solutions/ui` already has it. As of 2026-08-04 it does, for three of the six — the Document Sign-off Register shipped without reaching for any of them:

- **Empty states** → `EmptyState` — the `action` prop takes a `<Button>`. Ship the button; a bare sentence telling someone what to do without a way to do it is half a fix.
- **Scale past a handful of rows** → `Pagination`.
- **Archive / delete** → `ConfirmDialog` (set `destructive: true` for anything that removes or closes something out), paired with `DropdownMenu` for the row-level trigger.

The other three below aren't eq-ui's job — they're backend or product decisions, listed here so they get asked, not because a component fixes them.

---

## The six

1. **Lifecycle action.** Can a record be archived or removed, not just created? Check the data model actually supports it before assuming it needs a migration — `app_data.documents.status` already had `active`/`archived` on the sign-off register; the UI just never exposed it. Schema and UI drift apart otherwise.
2. **Bulk, not just one-at-a-time.** Acting on N records shouldn't cost N trips through the same form. Doesn't have to ship on day one — but the single-record path shouldn't quietly become the permanent ceiling because nobody asked.
3. **Export scope.** If a feature can export or report, can the user choose *what* goes in — a person, a date range, a subset — or is it always everything? All-or-nothing is a real limit the first time someone needs less than everything.
4. **Configurable, not hardcoded.** Any picker or taxonomy a real user will eventually want to extend (a type list, a category set) needs a path to add one without a code deploy — even if that path starts as "ask an admin to edit a table," not a full settings UI.
5. **Scale past the demo case.** Does the list view hold up past a handful of rows, not just the one real record it shipped with? `Pagination` exists in eq-ui for exactly this — a flat unpaginated list is the default failure mode, not a neutral starting point.
6. **Smart intake where the file already has the answer.** If an uploaded file plausibly contains a title, date, or reference number, that's a candidate for auto-fill (OCR or similar) instead of a blank form every time. Precedent: eq-cards' licence OCR. Not a default requirement — a prompt to ask the question, since not every document type benefits.

---

## How to use this

Run down this list at the point a new admin surface first gets scoped — the `CLAUDE.md` Task Brief step, before writing code. For each item: **built**, **deliberately deferred with a reason**, or **not applicable, here's why**. Log the deferred/not-applicable calls in the PR description or the session log so a later click-through finds a documented decision, not a rediscovered gap.

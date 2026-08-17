---
title: EQ Receipts — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-17
scope: EQ Receipts engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Receipts — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-receipts: Exports archive/delete + PDF page-splitting shipped, deploy pipeline gaps found (2026-07-28)

- [ ] **eq-receipts' Netlify site doesn't auto-deploy on push to `main`** despite `netlify.toml` and the app's own kickoff doc assuming it does — every deploy this session needed a manual trigger. The Netlify MCP's own CLI-proxy deploy path 404'd reproducibly (three times now); the dashboard's manual "Trigger deploy" is the only confirmed-working path right now. Root cause not investigated — worth fixing so this doesn't need manual triggering forever. _(added 2026-07-28)_
  - **Correction (2026-07-29):** a same-day session merged a PR via `gh pr merge` and Netlify auto-deployed cleanly within a minute of the merge commit, no manual trigger needed — confirmed live via the Netlify MCP's deploy record (commit ref matched exactly, build succeeded, secret scan clean). Only retested the PR-merge path, not the original direct-push-to-main repro, so leaving this open rather than closing outright — but the auto-deploy pipeline itself is evidently not broken end-to-end.

---

## EQ Receipts: tax-invoice watchlist labels cleaned up, expense-claim submission tracking + receipts bundled into export downloads (2026-07-24)
*Royce first asked why the Dashboard's "Invalid tax invoice watchlist" showed raw codes like `missing_or_invalid_abn` instead of plain English — fixed by reusing a label map that already existed in VerifyCard but wasn't shared. Then asked for two real features: a way to know an expense claim has actually been submitted (not just generated), and for the receipt images/PDFs to be bundled into the export download alongside the spreadsheet. Both built, merged, and deployed.*
- Watchlist labels: extracted VerifyCard's `ISSUE_LABELS` into shared `src/lib/taxInvoiceRules.ts`, added a compact `ISSUE_LABELS_SHORT` variant, Dashboard now renders each flag as its own small chip instead of one raw-code string. PR #1 merged.
- Submission tracking: `exports.submitted_at` (nullable timestamp, migration `0008_export_submitted.sql`) + a "Mark submitted" toggle on the Past Exports list.
- Receipt bundling: new shared `supabase/functions/_shared/receiptZip.ts` helper. SKS Weekly Claim and the Excel format of CSV-by-entity now download as a `.zip` (spreadsheet + `receipts/` folder of the original images/PDFs) instead of a bare spreadsheet — matches the pattern the existing Full Backup feature already used. CSV format left untouched, per Royce's literal wording ("when you download the excel"). PR #2 merged.
- [ ] **Not yet confirmed working end-to-end by Royce.** He tested once and got no receipts in the zip — root-caused to him re-downloading a *pre-existing* Past Exports history row generated before this session's fix (immutable — old rows never gain the bundling retroactively), not a code bug. Live-pulled the deployed function source to confirm the real fix is active. Told him to click "Generate claim form" again for a fresh `.zip` and report back — session ended before that confirmation came in. _(added 2026-07-24)_

---

## EQ Receipts: closed all 4 deferred gaps from yesterday's competitive review (2026-07-23)
*Royce said "sprint all outstanding items" against yesterday's close-card deferred list. The 2 items needing Royce's own logins (email-in setup, Phase 3 timed test) stayed open — everything code-side got built.*
- Build clean, verified in a live preview (Inbox/Review/Exports/Verify all load, no console errors) — no exports existed yet in the dev session to click-test the new bulk-download UI itself, so that one's unexercised until Royce has 2+ real exports to select.
- [ ] Phase 3 gate remains open — see the 2026-07-22 entry below. (Email-in capture is resolved — see 2026-07-23 entry: decided against for now, not a technical block.)

---

## EQ Receipts: fixed a broken login, then added quick-approve, email-in receipts, and auto-tagging by vendor (2026-07-22)
*Standalone receipt tracker for Royce personally (CDC Solutions / Hexican Holdings Trust / Milmlow Family Trust / Personal / SKS Technologies) — separate from the main EQ suite, single user. Ran most of the day: finished a visual reskin, fixed a login outage, then three feature builds Royce asked for directly, closing with a live competitive check against Dext.*
- [ ] **Phase 3 gate still open** — clearing one real week of receipts end-to-end in under 10 minutes, to prove the whole thing actually works day-to-day. Only Royce can run this one. _(added 2026-07-22, carried over from earlier)_

---


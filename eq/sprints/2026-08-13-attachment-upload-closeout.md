---
title: Sprint — Attachment Upload / Quote Documents close-out
owner: Royce Milmlow
last_updated: 2026-08-13
scope: Remaining items from the upload-size-limit + direct-to-storage attachment thread (2026-08-12 → 2026-08-13) — everything still open after the build work landed
read_priority: standard
status: live
duration_estimate: A1 needs Royce's live repro; A2-A5 are investigation/decision items, no urgent build
shipped: A0 (8-file honest-limit fix, dead-bucket cleanup, download-retry fix)
pending: A1 (live upload bug), A2-A5 (parked investigation items)
---

# Sprint — Attachment Upload / Quote Documents close-out

**Status:** in flight — opened 2026-08-13. The build phase (suite-wide honest upload limits, direct-to-storage signed-upload flow for quote attachments, dead-bucket cleanup, Download Quote retry fix) is merged. What's left: one live bug needs Royce's repro, and four items were surfaced during research but deliberately parked.

---

## Objective

Close out the loose ends from the "5-10MB attachment fails on quotes" incident so the thread can archive out of `pending.md`. One real bug is still open (A1); everything else is a parked decision, not a build task.

---

## In-scope items

### A0 — Shipped this session (context, not an action item)

- Suite-wide fix: 8 Netlify functions claimed 10-20MB upload limits that were unreachable (~4.5MB real ceiling from Netlify's 6MB Lambda payload cap) — now fail honestly instead of a misleading "check your connection" error. [PR #1307](https://github.com/eq-solutions/eq-shell/pull/1307) — merged, live.
- Quote attachments (drawings/PDFs/emails for reference) rebuilt as a direct-to-browser-to-Storage signed-upload flow, raising the real ceiling to 50MB (matches the live bucket's own limit). [PR #1310](https://github.com/eq-solutions/eq-shell/pull/1310) — open, see A1.
- 2 dead Supabase Storage buckets (leftover from an earlier CMMS migration) deleted after audit confirmed nothing live pointed at them.
- Unrelated bug found via Sentry while root-causing the incident — "Download Quote" failing on a transient network drop with no retry — fixed. [PR #1317](https://github.com/eq-solutions/eq-shell/pull/1317) — **merged 2026-08-13** (`ab0b31e`).

---

### A1 — Diagnose Royce's live upload issue on PR #1310

**Why:** Royce reported "issues" testing the new 50MB direct-to-storage flow live. CORS and deployment were both explicitly checked and ruled out as causes. No further hypothesis is possible without the actual browser error — this is the one item in the thread that isn't a decision, it's a missing repro.

**Status:** ⏳ Blocked on Royce — PR #1310 CI is green (typecheck/lint/tests/gitleaks/schema-drift all pass, deploy preview builds clean) and it's mergeable, but it has not been confirmed working against a real upload.

**Action:** From the [deploy preview](https://deploy-preview-1310--eq-shell.netlify.app) or a local `netlify dev` session, attach a 5-10MB file to a quote and, if it fails, capture the browser console error + Network tab request/response for the failed call (`attachment-upload-init` or the direct `uploadToSignedUrl` PUT to Supabase Storage).

**DoD:** Either a successful upload confirmed, or a specific error message/status code to root-cause against.

**Blast radius:** None yet — PR #1310 not merged, no live behaviour change until then.

---

### A2 — `job-plan-references` cleanup is eq-solves-service's, not eq-shell's

**Why:** Found while auditing the dead buckets. First pass concluded it was a dead vendored-scaffold artifact inside eq-shell only; corrected after Royce pushed back — the real, currently-live feature and its migrations (`0029_job_plan_reference_images.sql`, `0030_drop_reference_images.sql`) live in **eq-solves-service**'s own repo, not eq-shell.

**Action:** If this needs cleanup, it's a separate eq-solves-service task — out of scope for eq-shell entirely.

**Status:** Parked — no eq-shell action.

---

### A3 — `app_data.quote_attachment` table on ehow — investigated, decision needed

**Why:** Surfaced during the bucket audit. Now fully investigated:

- **0 rows** on ehow (live SKS plane) — never received data.
- It's schema-live and wired into the generic intake commit pipeline (`0009_intake_quotes_rpc.sql`, table→module routing in `intake-modules.ts`) as a valid target table, so it's not orphaned scaffolding in the DDL sense.
- But the feature it sounds like it backs — the "N files" badge on each quote row — is actually served by a **different** table. `eq_list_quote_attachment_counts()` (the RPC `QuotesModule.tsx` calls for that badge) reads `app_data.attachments WHERE entity_type = 'quote'`, never touches `quote_attachment` at all. Same is true for the attachment feature itself — `AttachmentList.tsx` and both the old and new (PR #1310) upload paths all write to `app_data.attachments`, not `quote_attachment`.
- **`docs/ARCHITECTURE-V2.md:500` marks `quote_attachment` "✅ Live" — that line is stale/wrong.** It hasn't been the live path since `app_data.attachments` (the generic entity-attachment table) took over.

**Read:** the table is either (a) genuinely dead — an earlier quote-attachment design superseded by the generic `attachments` table and never cleaned up, or (b) still the intended target for a specific intake producer (e.g. a Cards/PDF-parse path) that just hasn't fired in SKS production yet. Didn't chase (b) further — would mean tracing eq-intake's own emit logic, out of scope for this pass.

**Action:** Royce call — drop via governed migration (One Pipe, not by hand) if (a), or leave it and fix the stale doc line either way.

**Status:** Investigated — decision needed, not a further-digging task.

---

### A4 — Convert other upload paths to direct-to-storage

**Why:** Raised during the "what are industry leaders doing" research pass — the same signed-upload pattern now used for quote attachments (PR #1310) would also remove the artificial ~4.5MB Netlify Lambda ceiling from the 8 files fixed honestly in PR #1307 (staff licences, asset certs, document versions, worker-invite credentials, etc.). Real but not urgent — those paths work correctly today, just capped lower than ideal.

**Action:** Royce call on priority — no incident is currently blocked on this.

**Status:** Parked — deferred, real project not yet scoped.

---

### A5 — Malware / content-scanning gap on uploads

**Why:** Noted during the same research pass — neither the old function-relay uploads nor the new direct-to-storage flow scan file content before it lands in Storage. Industry-standard for a bucket accepting arbitrary user files, but no incident has surfaced from this yet.

**Action:** Royce call on priority.

**Status:** Parked — not built, not scoped.

---

### A6 — Total Supabase Storage capacity/quota

**Why:** Royce asked once during the discussion ("what about as a total capacity") — never actually checked.

**Checked:** Org (`EQ Solutions`) is on the **Pro plan**. Actual Storage usage, queried live:

| Plane | Bucket | Objects | Used |
|---|---|---|---|
| ehow (SKS) | `attachments` | 28 | 14 MB |
| ehow (SKS) | `logos` | 18 | 6.8 MB |
| ehow (SKS) | `compliance-packs` / `licence-photos` / `safety-photos` | 0 | — |
| zaap (EQ) | `compliance-packs` / `tenant-logos` / `safety-photos` | 0 | — |

**~21 MB total across both tenant planes.** Not a capacity concern at any realistic scale — Pro-plan storage allowances are measured in the hundreds of GB, and current usage is five orders of magnitude below that. The one number this MCP can't pull is the exact byte quota / overage rate on the current plan — that's a billing-dashboard figure, not a query. Not worth chasing unless usage actually grows; flagging so it isn't re-asked as if unknown.

**Status:** ✅ Done — no action needed, usage is trivial.

---

## Sprint success criteria

- [x] A0 — suite-wide honest limits, dead buckets, download-retry: shipped
- [ ] A1 — Royce's live repro done, upload confirmed working (or bug found + fixed)
- [x] A2 — confirmed out of scope for eq-shell (no action needed here)
- [ ] A3 — investigated (0 rows, superseded by `app_data.attachments`, docs stale); Royce call on drop vs. leave
- [ ] A4 — Royce call: scope or drop
- [ ] A5 — Royce call: scope or drop
- [x] A6 — capacity numbers pulled and logged — ~21MB total, no concern

## Where to start

A1 first — it's the only item blocking PR #1310 from merging. A2 needs no action. A3/A6 are quick checks either of us can do async. A4/A5 need Royce's call before any build starts.

---

## Related

- [eq-context/eq/pending.md](../pending.md)
- [eq-shell PR #1307](https://github.com/eq-solutions/eq-shell/pull/1307) — honest upload limits, merged
- [eq-shell PR #1310](https://github.com/eq-solutions/eq-shell/pull/1310) — direct-to-storage quote attachments, open, blocked on A1
- [eq-shell PR #1317](https://github.com/eq-solutions/eq-shell/pull/1317) — Download Quote retry fix, merged 2026-08-13
- [eq-context/sessions/2026-08-13.md](../../sessions/2026-08-13.md) — full session log

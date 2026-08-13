---
title: Sprint — Attachment Upload / Quote Documents close-out
owner: Royce Milmlow
last_updated: 2026-08-13
scope: Remaining items from the upload-size-limit + direct-to-storage attachment thread (2026-08-12 → 2026-08-13) — everything still open after the build work landed
read_priority: standard
status: live
duration_estimate: Only A1 and A5 still open. A1 needs Royce's live repro (or it stays closed by default). A5 is parked on Royce's own vendor account signup, revisit ~2026-08-20.
shipped: A0, A3, A4, A6 — all built and live. A2 confirmed out of scope.
pending: A1 (unconfirmed original bug, no repro), A5 (parked, vendor picked, waiting on Royce's account signup)
---

# Sprint — Attachment Upload / Quote Documents close-out

**Status:** mostly closed. A0/A2/A3/A4/A6 are done. A1 stays open until Royce confirms the original upload issue is actually fixed (or it resurfaces). A5 is parked — vendor decided, waiting on Royce to create the account — revisit no earlier than 2026-08-20.

---

## Objective

Close out the loose ends from the "5-10MB attachment fails on quotes" incident so the thread can archive out of `pending.md`. One real bug is still open (A1); everything else is a parked decision, not a build task.

---

## In-scope items

### A0 — Shipped this session (context, not an action item)

- Suite-wide fix: 8 Netlify functions claimed 10-20MB upload limits that were unreachable (~4.5MB real ceiling from Netlify's 6MB Lambda payload cap) — now fail honestly instead of a misleading "check your connection" error. [PR #1307](https://github.com/eq-solutions/eq-shell/pull/1307) — merged, live.
- Quote attachments (drawings/PDFs/emails for reference) rebuilt as a direct-to-browser-to-Storage signed-upload flow, raising the real ceiling to 50MB (matches the live bucket's own limit). [PR #1310](https://github.com/eq-solutions/eq-shell/pull/1310) — **merged by Royce 2026-08-13 10:51, live.** See A1.
- 2 dead Supabase Storage buckets (leftover from an earlier CMMS migration) deleted after audit confirmed nothing live pointed at them.
- Unrelated bug found via Sentry while root-causing the incident — "Download Quote" failing on a transient network drop with no retry — fixed. [PR #1317](https://github.com/eq-solutions/eq-shell/pull/1317) — **merged 2026-08-13** (`ab0b31e`).

---

### A1 — Diagnose Royce's live upload issue on PR #1310

**Why:** Royce reported "issues" testing the new 50MB direct-to-storage flow live. CORS and deployment were both explicitly checked and ruled out as causes. No further hypothesis was possible without the actual browser error.

**Status:** Royce merged PR #1310 directly on GitHub, 2026-08-13 10:51 — live on core.eq.solutions (confirmed via smoke check post-deploy). No repro was ever provided, so **whether the original reported issue is actually resolved is unconfirmed** — Royce's own call to proceed, not a diagnosed fix. Leaving this open until a real upload is confirmed working, or closing outright if Royce says the issue's gone.

**Action (if it resurfaces):** attach a 5-10MB file to a quote on core.eq.solutions and, if it fails, capture the browser console error + Network tab request/response for the failed call (`attachment-upload-init` or the direct `uploadToSignedUrl` PUT to Supabase Storage).

**DoD:** Confirmed working live, or a specific error to root-cause against.

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

**Decided (2026-08-13):** drop it — no known reason to keep it, no downside to removing it.

**Done:** [eq-shell PR #1331](https://github.com/eq-solutions/eq-shell/pull/1331) — governed drop migration (`0244_drop_quote_attachment.sql`), plus removed the two dead code references that would otherwise point at a now-gone table (`intake-modules.ts` routing map, `sync-tenant-data.mjs` table list), plus the doc fix. **Merged 2026-08-13 (`e81e77c9`), live** — confirmed via post-deploy smoke check.

**Status:** ✅ Done.

---

### A4 — Convert other upload paths to direct-to-storage

**Why:** Raised during the "what are industry leaders doing" research pass — the same signed-upload pattern now used for quote attachments (PR #1310) would also remove the artificial ~4.5MB Netlify Lambda ceiling from the 8 files fixed honestly in PR #1307. Real but not urgent — those paths work correctly today, just capped lower than ideal.

**Scoped 2026-08-13.** Read all 8 against the reference pattern (`attachment-upload-init.ts`/`attachment-upload-commit.ts`). Checked Sentry for the last 90 days first — **zero size-related failures on any of the 8**, unlike quote attachments where a real incident triggered this whole thread. This is preventive, not incident-driven.

3 of 8 aren't storage functions at all — `staff-licence-ocr.ts`, `ocr-parse.ts`, `labour-hire-parse.ts` never touch Storage, they proxy raw bytes straight to an OCR/vision API (Claude document block, Google Document AI, Claude vision tool-use respectively). Direct-to-storage doesn't apply to them on its own.

Of the remaining 5 (all storage-writing):

| Function | Effort | Real upside? |
|---|---|---|
| `upload-document-version.ts` | Moderate — needs re-fetch-after-upload to keep the server-side SHA-256 anti-tamper hash computed on the server, not trust a client-supplied one | **Yes** — scanned sign-off register PDFs plausibly already hit the 4MB wall, same size class as quote attachments |
| `upload-asset-cert.ts` | Trivial — simplest of the 8, doesn't even insert a DB row | No — certs are typically <2MB |
| `staff-licence-replace-photo.ts` | Trivial — near-identical shape to the reference pattern | No — phone photos are typically 1–3MB |
| `staff-licence-backfill.ts` | Moderate — 2-file case (front/back), dedupe logic wraps the upload | No — same size class as above |
| `create-worker-invite.ts` | Moderate — needs a batch/multi-file signed-upload pattern (up to 10 credentials per invite) for marginal benefit, since the combined cap already forces small individual files | Marginal |

**Recommendation:** if this gets built at all, do `upload-document-version.ts` alone first — it's the one path with a real, plausible size problem, matching the same justification that made the quote-attachments fix worth it. Leave the other 4 alone unless one of them actually starts failing — no evidence any currently do.

**Done 2026-08-13.** Built `upload-document-version.ts`'s conversion — [eq-shell PR #1334](https://github.com/eq-solutions/eq-shell/pull/1334), merged + live (`49f92c14`). New `document-version-upload-init.ts`/`-commit.ts`, same two-step shape as the quote-attachments flow. Two things worth remembering if this pattern gets reused again: the `content_hash` (what a signer's attestation binds to) has to be recomputed server-side by re-downloading the upload, since the commit function never sees the bytes as they land — and the parent `documents` row is deliberately NOT created until after the upload is confirmed, to avoid the same orphaned-row class of bug as A3's dangling rows. The other 4 storage-writing paths (licence photos, asset certs) stay untouched — no evidence any of them need it.

**Status:** ✅ Done.

---

### A5 — Malware / content-scanning gap on uploads

**Why:** Noted during the same research pass — neither the old function-relay uploads nor the new direct-to-storage flow scan file content before it lands in Storage. Industry-standard for a bucket accepting arbitrary user files, but no incident has surfaced from this yet.

**Scoped 2026-08-13.** Confirmed no existing scanning infra anywhere in the suite (grepped for virus/malware/clamav/scan across eq-shell — no real hits). Neither Supabase Storage nor Netlify offer built-in AV scanning; this would be a new external integration.

**Where it plugs in:** `attachment-upload-commit.ts` already has the right hook — it does a post-upload verification step today (downloads `.msg`/`.eml` files to check their byte signature before finalizing). A malware-scan call is the same shape: scan after upload, before the DB row is inserted; delete + reject on a positive.

**Vendor options:**
- **Cloudmersive Virus Scan API** — has a real free tier built for exactly this ("scan a file upload"), single API call, clean/infected response. Best fit for a serverless function.
- **VirusTotal API** — broader AV-engine coverage (70+), but the free tier's rate limit (4 req/min) is tight for a production gate, not just a lookup tool.
- **Self-hosted ClamAV** — no per-scan cost or vendor lock-in, and no file content leaves EQ's own infrastructure (a real point in its favour for customer documents) — but needs persistent compute (a small always-on service, e.g. Fly.io/Railway), which Netlify Functions can't provide. More ops overhead for less integration work.

**The real blocker isn't build effort — it's picking and signing up for a vendor.** Implementation itself is small (one shared helper + a call in the existing commit function). This needs Royce to choose (and, for anything beyond a free tier, approve a cost) before any code gets written.

**Recommendation:** pilot on quote attachments only (`attachment-upload-commit.ts`) — the highest-risk path, since it explicitly accepts arbitrary external files (drawings, PDFs, emails from outside the company). Don't build it into all 8 upload paths from A4 up front; extend later if the pilot's worth keeping.

**Vendor picked 2026-08-13: Cloudmersive.** VirusTotal ruled out — its free/consumer tier may share submitted files with its partner/researcher ecosystem, which is a real problem for client quote documents (drawings, contracts, site plans), not a hypothetical. Self-hosted ClamAV has the better privacy story (nothing leaves EQ's infrastructure) but means standing up the one piece of persistent, always-on compute in an otherwise fully serverless stack, for a feature scanning single-digit files a month — solving a scale problem that doesn't exist yet. Cloudmersive is a standard B2B API vendor (no data-sharing surprise), fits the serverless architecture with zero new infra, and its free tier comfortably covers current volume (13 quote attachments, total, ever). Migration to self-hosted later is a small change if volume or sensitivity ever justifies it — same call site, swap what's behind it.

**Critique of the direction, not just the vendor** (asked for explicitly, worth keeping on record):
- Signature-based scanning is a floor, not a shield — catches commodity malware, does nothing against something novel or targeted. Don't let "we scan uploads" become a blanket reassurance.
- The actual risk isn't "malware runs on our server" — nothing in eq-shell executes an uploaded file, it sits in Storage until a person opens it later. The real exposure is a colleague downloading an external subcontractor's file and opening it on their own machine. Given that, this is a sound direction, not security theatre — just be clear on what it protects.
- Given that threat model, `.msg`/`.eml`/Word/Excel from quote attachments (external subcontractors sending Office documents) is the sharpest edge, not licence photos or asset certs. Basic AV scanning helps here but a macro-aware check would help more — not a blocker for the pilot, worth remembering as the natural next step if this proves worth keeping.
- Fail-open vs. fail-closed needs a real decision: at this volume, fail open with a Sentry alert on every skip — rejecting a legitimate upload because a third-party scanning API hiccuped is worse than the marginal risk, and nothing else in the suite scans uploads today either.
- Genuinely low-urgency — near-zero volume, no incident, no compliance driver. Worth building because it's cheap and closes a real gap, not because anything's on fire.

**Parked 2026-08-13 — "remind me next week."** Vendor picked, design settled (pilot on quote attachments, fail-open + Sentry alert on skip), nothing built. Blocked on Royce signing up for a Cloudmersive account and generating an API key himself — account creation is not something Claude does, even with a go-ahead. **Revisit no earlier than 2026-08-20** — logged as a dated deferred item in `eq/pending.md` so it resurfaces via the nightly digest's "Needs you" section, the same mechanism already used for every other "come back to this" item in this substrate.

**Action:** Royce signs up for Cloudmersive, gets an API key, hands it over — then this is a small, fast build (one shared helper + a call in the existing commit function).

**Status:** ⏸ Parked — vendor decided, not built. Revisit ~2026-08-20.

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
- [ ] A1 — PR #1310 merged + live 2026-08-13, but the original reported issue was never confirmed fixed (no repro provided) — leave open until Royce confirms or it resurfaces
- [x] A2 — confirmed out of scope for eq-shell (no action needed here)
- [x] A3 — dropped, [PR #1331](https://github.com/eq-solutions/eq-shell/pull/1331) merged + live 2026-08-13
- [x] A4 — scoped, `upload-document-version.ts` built, [PR #1334](https://github.com/eq-solutions/eq-shell/pull/1334) merged + live 2026-08-13
- [ ] A5 — ⏸ parked 2026-08-13, vendor decided (Cloudmersive), waiting on Royce's account signup — **revisit ~2026-08-20**
- [x] A6 — capacity numbers pulled and logged — ~21MB total, no concern
- [x] Bonus — 19 dangling `app_data.attachments` rows found + deleted on ehow, reconciliation check shipped to catch a repeat: [PR #1333](https://github.com/eq-solutions/eq-shell/pull/1333), merged + live

## Where to start

Everything buildable is done. A1: confirm it's actually fixed, or report what's still broken. A5: sign up for Cloudmersive, hand over an API key, and it's a small fast build — but not before ~2026-08-20 per Royce's own "remind me next week."

---

## Related

- [eq-context/eq/pending.md](../pending.md)
- [eq-shell PR #1307](https://github.com/eq-solutions/eq-shell/pull/1307) — honest upload limits, merged
- [eq-shell PR #1310](https://github.com/eq-solutions/eq-shell/pull/1310) — direct-to-storage quote attachments, merged + live
- [eq-shell PR #1331](https://github.com/eq-solutions/eq-shell/pull/1331) — dropped `quote_attachment`, merged + live
- [eq-shell PR #1317](https://github.com/eq-solutions/eq-shell/pull/1317) — Download Quote retry fix, merged 2026-08-13
- [eq-shell PR #1333](https://github.com/eq-solutions/eq-shell/pull/1333) — attachment row/file reconciliation check, merged + live
- [eq-shell PR #1334](https://github.com/eq-solutions/eq-shell/pull/1334) — document-version uploads direct-to-storage (A4), merged + live
- [eq-context/sessions/2026-08-13.md](../../sessions/2026-08-13.md) — full session log

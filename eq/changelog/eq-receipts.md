---
title: Changelog — EQ Receipts
owner: Royce Milmlow
scope: Append-only history of changes to the EQ Receipts product. Standalone single-user app (Royce personally) — separate from the core EQ suite (Cards/Shell/Field/Service).
read_priority: reference
status: live
---

# Changelog — EQ Receipts

## [2026-07-22] Login outage fixed, quick-approve, email-in capture, vendor auto-tagging
- **Neumorphism reskin completed** across every page (soft/embossed shadow system, replacing the standard EQ brand look — this app is a documented single-user exception). `ba422e9`.
- **Fixed login**: `eq.solutions` apex MX record was missing, breaking inbound mail to Royce's real Microsoft 365 mailbox — root-caused via Supabase auth logs + live DNS + Cloudflare audit log, restored the MX record via Cloudflare API. Also hit Supabase's built-in mailer's hard 2-emails/hour cap; walked Royce through switching to Resend as custom SMTP.
- **`job_no` field added to Verify's SKS panel.** `5547757`. The column was already read by every export path (SKS claim, CSV/Excel, archive) but had no UI to set it.
- **Batch + individual Approve / Force approve / Delete on the Review grid.** `961ee6a`. Checkbox selection; Approve respects the existing `verified_requires_core` DB constraint; Force approve only bypasses the client-side reconciliation-math check — entity/category/date/total stay hard-required at the Postgres level regardless.
- **`receive-email` Edge Function**: Resend inbound webhook (`email.received`), Svix-signature-verified (HMAC-SHA256, timestamp-skew-checked), deployed with `verify_jwt=false`. One receipt per image/PDF attachment, reuses the existing extraction pipeline (`_shared/extraction.ts`). Idempotent via a `source_filename = email:{email_id}:{filename}` existence check. `e91482f`. **Not yet live** — needs Royce to add a Resend receiving domain + webhook + API key, and 4 Supabase Edge Function secrets (`RESEND_API_KEY`, `RESEND_WEBHOOK_SECRET`, `RECEIPTS_OWNER_ID`, `RECEIVING_ADDRESS`).
- **Supplier memory**: new `supplier_defaults()` Postgres function (migration `0006_supplier_defaults.sql`) — exact vendor-name match first, falls back to the pg_trgm similarity already indexed on `vendor_name`. Wired into all three receipt-creation paths (extract-receipt sync, poll-batch, receive-email) so new receipts arrive pre-tagged with entity/category/job_no. VerifyCard's older ad-hoc exact-match-only client lookup replaced with a call to the same function. `22365a1`.
- Competitive check against Dext Prepare's live feature set (web search, not memory): confirmed email-in + supplier-rules were the two real gaps; explicitly ruled out bank-feed matching and per-line-item cost-center splitting as not worth building for a single-user tool.
- Reference: Supabase project `bgrhqvmvzgotxzjneskv` (Sydney). Cloudflare zone `2f2d7f7ada9a48b7ca98c1c32faeb4a0` for `eq.solutions`. Single app owner id `6f215ac2-b20d-418c-96fc-d870e70f580e`.

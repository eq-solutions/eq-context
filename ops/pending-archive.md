---
title: OPS Tier — Pending Actions Archive
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Done items rotated out of ops/pending.md nightly by scripts/rotate_pending.py to keep the live doc scannable. Nothing here is actionable — pure historical record (also covered in changelogs and sessions/*.md). Append-only, in rotation order.
read_priority: reference
status: archived
---

# OPS Tier — Pending (Archive)

Done items and fully-closed session write-ups rotated out of `ops/pending.md`.
If you're looking for something to action, it's not here — check `ops/pending.md`.
A "(rotated YYYY-MM-DD ...)" note on a section header means only that
section's done items live here; its open items stayed in `ops/pending.md`.

---

## Infrastructure — Live Blockers (rotated 2026-07-27 — open items remain in pending.md)

- [x] **PAT rotation — DONE 2026-06-28** — new PATs generated and deployed, old ones confirmed revoked. See `sessions/2026-06-28-brain-10-10.md` (date corrected 2026-07-21 — was misdated 2026-06-15, no session log existed for that date; 06-28 is the actual confirming log).

---

## Tax & Entities (Webb Financial) (rotated 2026-07-27)

- [x] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft — CLOSED 2026-06-15
- [x] Personal vehicle depreciation amendment (~$33,800 refund) — CLOSED 2026-06-15
- [x] Emma FY23/24 ITR amendment — CLOSED 2026-06-15
- [x] EQ Property Solutions TFN receipt — CLOSED 2026-06-15
- [x] Milmlow Holdings / MFT / Allcraft review — September 2026 — CLOSED 2026-06-15

---

## Multi-Repo Push Automation (rotated 2026-07-27 — open items remain in pending.md)

- [x] **eq-solves-field push blocked on `demo` branch** — **[CLOSED 2026-07-27 — moot — the 2026-05-20 eq-field/SKS-Live split renamed local demo->main and rewired Netlify; eq-field's origin is now eq-solutions/eq-field, not the old Milmlow/eq-field-app:demo remote]**
  2026-05-14 `push-all.bat` attempted push of local `demo` to
  `Milmlow/eq-field-app:demo`, rejected as non-fast-forward (remote has
  commits we don't). §11 hard rule also says never push `demo` without
  explicit instruction. Decisions needed: (a) `git pull --rebase origin
  demo` and re-push, or (b) switch local to `main` for the SKS labour
  app surface and push there, or (c) skip until the EQ Field branch
  strategy is settled. **Royce to call.**
- [x] **Personal global rules `C:\Users\EQ\.claude\CLAUDE.md` **[CLOSED 2026-07-27 — already corrected — this session's own loaded global CLAUDE.md shows the fixed table (field.eq.solutions -> eq-field -> main, sks-nsw-labour.netlify.app -> SKS NSW Labour -> main)]**
      deployment table is stale (post-split)** —
  Royce's personal global rules still show
  `sks-nsw-labour.netlify.app` as deploying from "EQ Field (demo)"
  repo on `demo` branch. After today's split that row should read
  `eq-solutions/sks-nsw-labour` on `main`, and the eq-solves-field
  row should read `eq-solutions/eq-field` on `main` (renamed from
  demo 2026-05-20). Not substrate-visible — Royce-manual edit in
  his personal global rules.

---

## Cross-Tool Consistency — Original Reason for 2026-05-04 Refactor (rotated 2026-07-27 — open items remain in pending.md)

- [x] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` / `CHAT-PROMPT.md` (paste-once-per-session prompts fetching the raw GitHub URLs — the "canonical Supabase URLs" in the original framing are gone; edge cache retired 2026-06-22). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools." **[CLOSED 2026-07-27 — both files written, root-exempt list updated in `scripts/index_drift.py`]**

---

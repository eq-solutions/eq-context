---
title: Sprint — eq-shell reliability follow-ups (stale chunks + handoff render gap)
owner: Royce Milmlow
last_updated: 2026-09-14
scope: Two of the three items deferred from the 2026-09-13 Sentry review, re-verified live before scoping — see "Why only two" below
read_priority: standard
status: live
---

# Sprint: eq-shell reliability follow-ups — 2026-09-14

## Where this came from

The 2026-09-13 Sentry review ([`sessions/2026-09-13.md`](../../sessions/2026-09-13.md)) deferred
three items rather than fix them same-session. Before turning all three into a sprint, each
was re-checked live against current Sentry state (2026-09-14) — the instruction was "ensure
they are worth chasing first," and one of them wasn't.

## Why only two

**EQ-FIELD-1N — dropped, marked resolved, not in this sprint.** Re-checked live: zero new
occurrences since 2026-09-10T06:55Z, unchanged across 4+ days and past two subsequent
production deploys (including both of yesterday's own merges). Same CSP-gap shape as
EQ-FIELD-1Q (fixed by eq-field#976) — reads as a stale service-worker cache outliving the
deploy by a few hours on one device, not a code gap. Marked resolved in Sentry 2026-09-14
rather than carried into a sprint on a hypothesis that was never actually confirmed wrong.

Also re-confirmed both 2026-09-13 fixes are genuinely live before scoping any of this:
`commit_ref` on both sites' current Netlify deploys matches the merge commits exactly
(eq-field `0f5e3ead`, eq-shell `2efddef5`), both `state: ready`, both secret-scan clean.

---

## Item 1 (higher priority) — EQ-SHELL-21: Field accepts the handoff but never reports 'rendered'

**Current state, re-checked 2026-09-14 (was 6/6 on 2026-09-13):**

| | 2026-09-13 | 2026-09-14 |
|---|---:|---:|
| Occurrences | 6 | **9** |
| Users impacted | 6 | **9** |
| Last seen | 2026-09-11 | **2026-09-13T21:44** |

Every occurrence has a distinct user (occurrences == users impacted, both checks) — this is
spreading across different people, not one person retrying, and it grew 50% in under 3 days.
Not dormant — actively live.

**The 2026-09-13 diagnosis is likely incomplete, not wrong.** That session traced one full
event end-to-end and found a memory-saver iframe restore whose *second* boot cycle (after an
already-successful first render) didn't finish inside its own notice window — a real,
specific mechanism, and eq-shell#1896 (mint-timing floor) deliberately did not touch it since
it's a different cause.

The newest occurrence (2026-09-13T21:44, iPhone/Mobile Safari again) does **not** show that
same reload-after-render pattern — its `steps` trace is a single, un-interrupted attempt:
fast mint (1.48s) → boot → accepted (9.0s) → 10s draw-notice with `rendered` still false, no
second `iframe-load` step at all. Whatever's stalling `rendered` here is happening on the
*first* pass, not after a restore.

**What this means for scope:** don't assume the fix is "handle the memory-saver restore
case" and stop there — that's one confirmed mechanism, but at least one occurrence doesn't
fit it. Needs several more event traces pulled and compared (not just one) before committing
to a single root cause. Both examples seen so far are iPhone/Mobile Safari — worth explicitly
checking whether this is disproportionately an iOS-WebKit issue (matches this whole cluster's
recurring theme: backgrounding/suspension behaving differently on iOS) or just because SKS's
field staff skew toward iPhone.

**Suggested first step:** pull the full event list for this issue (not just the latest), group
by whatever's observable in each trace (reload-after-render vs. single-pass stall, browser/OS,
elapsed time to 'accepted'), and only then decide whether this is one bug or several.

---

## Item 2 — EQ-SHELL-1P / EQ-SHELL-22: stale JS chunk after a deploy — CLOSED, already fixed

**Correction (2026-09-14, before any code was written for this item):** everything below this
line was wrong about "no existing coverage." Re-verifying live before starting the build (per
the substrate's own duplicate-work rule) surfaced three already-merged PRs this section never
checked — #1523, #1528, and **[eq-shell#1826](https://github.com/eq-solutions/eq-shell/pull/1826)**
(merged 2026-09-08, three days *before* this doc was written). #1826's own description names
EQ-SHELL-1P and EQ-SHELL-22 explicitly as its motivation: `ChunkErrorBoundary` +
`installChunkLoadRejectionGuard` (`src/lib/chunkReload.ts`) already self-heal a stale chunk via
a silent reload, built out incrementally for the sibling EQ-SHELL-1S/10 issues — the one gap
was Firefox's distinct wording for this same failure (`'text/html' is not a valid JavaScript
MIME type`), which #1826 closed with one more matcher clause.

**Confirmed fixed, not just merged:** both [EQ-SHELL-1P](https://eq-solutions.sentry.io/issues/EQ-SHELL-1P)
and [EQ-SHELL-22](https://eq-solutions.sentry.io/issues/EQ-SHELL-22) already show `resolved` in
Sentry; zero occurrences since 2026-09-11 across several deploys since; eq-shell's entire
unresolved-issue list (checked live 2026-09-14) has nothing chunk/MIME-related. The handful of
occurrences between #1826 merging and 2026-09-11 read as tabs that already had the pre-fix
bundle loaded before that deploy — the one population this exact class of fix structurally
can't reach until that tab reloads on its own; that population draining out is exactly what
"quiet since 2026-09-11" looks like from a working fix, not a coincidence.

**Where the miss came from:** the original check below only ruled out one plausibly-named
branch (`chunk-prefetch-catch`) and never searched for the real mechanism, which lives under a
differently-named issue family (EQ-SHELL-1S) with its own branch names. Royce confirmed
closing this out rather than building anything further — no code needed.

<details>
<summary>Original (incorrect) write-up, kept for the record</summary>

**Current state, re-checked 2026-09-14:** unchanged since 2026-09-11 (4 occurrences, 2 users,
same incident pair — EQ-SHELL-1P is the custom telemetry capture, EQ-SHELL-22 is the raw JS
exception, same trace_id, same moment). Dormant for 3 days now, including through yesterday's
own eq-shell deploy.

**Dormant is expected, not evidence it's fixed.** This is the classic SPA stale-chunk failure:
a user has a tab open when a deploy replaces a lazy-loaded chunk's content hash; their next
in-app navigation requests the old hash, the server has nothing to serve at that path, the SPA
fallback route serves `index.html` instead of a 404, and the browser throws `'text/html' is
not a valid JavaScript MIME type` trying to execute it as a module. This only fires for someone
whose tab survives across a deploy *and* who then navigates to a not-yet-loaded chunk — bursty
by nature, not continuous. It will recur on some future deploy; going quiet for a few days
proves nothing.

**Already checked, not a duplicate:** the plausible-looking `chunk-prefetch-catch` branch is
confirmed 3 weeks stale and unrelated (verified by diff against main 2026-09-13, not assumed
from the name) — this genuinely has no existing coverage.

**Suggested shape of the fix** (standard pattern for this exact failure class, not yet
scoped in detail): wrap the router's lazy-loaded route imports in a handler that detects this
specific failure mode (a dynamic `import()` rejecting, or the MIME-type error specifically)
and triggers a full page reload — a fresh load fetches the current `index.html`, which
references the current chunk hashes, resolving the staleness. Needs care to avoid a reload
loop if the failure has some other cause.

</details>

---

## Sequencing

EQ-SHELL-21 was the only real remaining item — actively growing, every occurrence a real
broken experience for a real person. Fixed same day via `DRAW_NOTICE_MS` (see
`eq/pending/eq-shell.md`'s matching entry). EQ-SHELL-1P/22 turned out already closed (above) —
sequencing moot, there was nothing to schedule.

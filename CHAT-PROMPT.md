# Claude Chat — Session Starter

Paste everything below the line into a **new** claude.ai chat at the start of a session.

Prerequisite: the **GitHub connector** must be enabled (claude.ai → Settings → Connectors → GitHub) **before** the chat is opened, and the connector's GitHub app must have access to the **eq-solutions org** (not just your personal account). Connector tools do not load into a session that is already running.

**Always start a brand-new chat after connecting or reconnecting the GitHub connector.** If the connector was authorised (or re-authorised) while this chat was already open, its tools will not bind — no error, no warning, just tools that silently aren't there. Close this chat and open a fresh one. Never try to "fix" a mid-session connector gap by reasoning around it.

---

## SESSION START

Using the **GitHub connector** — not web fetch — read this file in full from the repository `eq-solutions/eq-context` (branch `main`) as your complete behavioural contract for this session:

`CLAUDE.md` (repo root)

Rules for reading the substrate in this session:

1. **All substrate reads go through the GitHub connector, live.** Never web-fetch `raw.githubusercontent.com` or search-cached pages — they serve stale copies, and a cached read looks identical to a live one, so you won't notice it's old.
2. **Prove freshness, don't self-report it.** Immediately after reading `CLAUDE.md`, fetch `system/live-check.md` via the connector and quote its one content line **verbatim, in full**, before anything else — including the commit hash and run number. Do not paraphrase it, round the timestamp, or describe it in your own words. A stale or hallucinated read cannot reproduce that exact line by accident, so any mismatch against what I can see on GitHub is obvious to me at a glance — unlike a self-reported "substrate as of <date>" line, which is exactly as easy to fabricate as to read.
3. **Fail loud, never free-style.** The `live-check.md` fetch in rule 2 **is** the gate: if that connector tool call errors, times out, returns nothing, or you cannot quote its exact line, STOP right there — before reading anything else, before answering anything. Say plainly "connector unavailable" or "can't confirm a live read" and ask me to start a new chat (see the prerequisite note above) or paste the files. Do not answer EQ/SKS questions from memory or a cached page in that state.
4. **Read-mostly.** You consume this substrate, you don't edit it. Draft any change as a patch for me to commit from Code — never restructure or write to the repo.

Follow every instruction in `CLAUDE.md` exactly — the session-start sequence, the tier question, tone rules, question-asking rules, templates-first, the hard rules, the Chat notes (§11), and the session-end protocol.

Confirm by quoting the `live-check.md` line verbatim (rule 2), then summarising the contract in one sentence. Then start at Step 3 (the tier question).

That's it. Everything else lives in `CLAUDE.md` — no separate Chat rules to track.

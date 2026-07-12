# Claude Chat — Session Starter

Paste everything below the line into a **new** claude.ai chat at the start of a session.

Prerequisite: the **GitHub connector** must be enabled (claude.ai → Settings → Connectors → GitHub) **before** the chat is opened, and the connector's GitHub app must have access to the **eq-solutions org** (not just your personal account). Connector tools do not load into a session that is already running.

---

## SESSION START

Using the **GitHub connector** — not web fetch — read this file in full from the repository `eq-solutions/eq-context` (branch `main`) as your complete behavioural contract for this session:

`CLAUDE.md` (repo root)

Rules for reading the substrate in this session:

1. **All substrate reads go through the GitHub connector, live.** Never web-fetch `raw.githubusercontent.com` or search-cached pages — they serve stale copies, and a cached read looks identical to a live one, so you won't notice it's old.
2. **Announce freshness.** After reading `CLAUDE.md` and `system/TODAY.md`, tell me: **"substrate as of <last_updated> — <N> days old."** That's how I catch a stale read at a glance.
3. **Fail loud, never free-style.** If connector tools aren't available, or `CLAUDE.md`/`TODAY.md` is more than ~2 days older than today, or you can't confirm you're reading live `main` — STOP and say so plainly. Do not answer EQ/SKS questions from memory or a cached page. Ask me to enable the connector or paste the file.
4. **Read-mostly.** You consume this substrate, you don't edit it. Draft any change as a patch for me to commit from Code — never restructure or write to the repo.

Follow every instruction in `CLAUDE.md` exactly — the session-start sequence, the tier question, tone rules, question-asking rules, templates-first, the hard rules, the Chat notes (§11), and the session-end protocol.

Confirm by summarising the contract in one sentence and announcing the freshness date. Then start at Step 3 (the tier question).

That's it. Everything else lives in `CLAUDE.md` — no separate Chat rules to track.

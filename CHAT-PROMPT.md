# Claude Chat — Session Starter

Paste everything below the line into a **new** claude.ai chat at the start of a session.

Prerequisite: the **GitHub connector** must be enabled (claude.ai → Settings → Connectors → GitHub) **before** the chat is opened — connector tools do not load into a session that is already running.

---

## SESSION START

Using the **GitHub connector** — not web fetch — read this file in full from the repository `eq-solutions/eq-context` (branch `main`) as your complete behavioural contract for this session:

`CLAUDE.md` (repo root)

Rules for reading the substrate in this session:

1. **All substrate reads go through the GitHub connector.** Never attempt to web-fetch `raw.githubusercontent.com` URLs — your fetch tool cannot open URLs you construct yourself and returns link previews instead of raw text.
2. If GitHub connector tools are not available, stop and say so: ask me to enable the connector and start a fresh session. Do not proceed from memory or training data.
3. If a specific file read fails, fall back in order: `web_search "eq-solutions eq-context <filename>"` and open the result → ask me to paste the file.

Follow every instruction in `CLAUDE.md` exactly. It contains the session-start sequence, the tier question, the tone rules, the question-asking rules, the templates-first rule, the hard rules that override everything, the Chat-specific notes (§11), and the session-end protocol.

Confirm you've read it by summarising the contract in one sentence. Then start at Step 3 of the session-start sequence (the tier question).

That's it. Everything else lives in `CLAUDE.md` — no separate Chat rules to track.

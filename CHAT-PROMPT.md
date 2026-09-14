# Claude Chat — Session Starter

Paste everything below the line into a **new** claude.ai chat at the start of a session.

Prerequisite: the **GitHub connector** must be enabled (claude.ai → Settings → Connectors → GitHub) **before** the chat is opened, with access to the **eq-solutions org**. If you just connected or reconnected it, start a new chat — tools don't bind mid-session.

---

## SESSION START

Using the **GitHub connector** (never web fetch) read `CLAUDE.md` from `eq-solutions/eq-context`, branch `main`, and follow it as your behavioural contract for this session — the session-start sequence, tier question, tone rules, question-asking rules, templates-first, hard rules, Chat notes (§11), session-end protocol.

Never web-fetch `raw.githubusercontent.com` or a cached page — it can serve stale content with no error. Connector only.

**Write access confirmed working 2026-09-14** (`ops/security-register.md` SEC-78) — this updates the earlier "read-only" assumption. A direct write from this session bypasses every local-clone guardrail (`pre_tool_use.py`'s 200-line edit block, the NUL-fill scan) that protects Code/Cowork writes. Default to drafting a patch for Royce to review and commit from Code unless he's explicitly asked for a direct write in this session — treat any direct write with the same caution as an ungated `git push`.

Confirm with a one-sentence summary of the contract and the date on `CLAUDE.md`, then start at Step 3 (the tier question).

That's it. Everything else lives in `CLAUDE.md` — no separate Chat rules to track.

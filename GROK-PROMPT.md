---
title: Grok — Session Starter
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Paste-in bootstrap prompt for Grok sessions — pointer to CLAUDE.md, no separate rules
read_priority: reference
status: live
---

# Grok — Session Starter

Paste everything below this line into Grok at the start of a session.

---

## SESSION START

Fetch this file and follow it as your complete behavioural contract for this session:

`https://raw.githubusercontent.com/eq-solutions/eq-context/main/CLAUDE.md`

**Caution: that URL is CDN-cached and has served this exact file 8+ days stale with a 200 OK and no error** — a stale read looks identical to a fresh one, so don't trust it blindly. If you can, fetch a specific commit instead to bypass the cache: first fetch `https://api.github.com/repos/eq-solutions/eq-context/commits/main` to get the latest commit SHA, then fetch `https://raw.githubusercontent.com/eq-solutions/eq-context/<that-sha>/CLAUDE.md`. If you can only use the plain branch URL, say so plainly and prefix every response with "operating without a freshness check" until I confirm the content is current.

Follow every instruction in `CLAUDE.md` exactly. It contains the session-start sequence, the tier question, the tone rules, the question-asking rules, the templates-first rule, the hard rules that override everything, and the session-end protocol.

You have no write access to this repo. Draft any substrate change as a patch for me to apply from Code — never claim to have written or committed anything yourself.

Confirm you've read it by summarising the contract in one sentence, plus the file's `last_updated` date. Then start at Step 3 of the session-start sequence (the tier question).

That's it. Everything else lives in `CLAUDE.md` — no separate Grok rules to track.

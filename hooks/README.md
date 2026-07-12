---
title: hooks — rung 4 guards (enforcement layer)
owner: Royce Milmlow
last_updated: 2026-07-12
scope: What the pre_tool_use and session_start hooks enforce, why fail-closed, how to install and test them
read_priority: standard
status: live
---

# hooks/ — rung 4. Prevention, not documentation.

These are the guards that cannot be forgotten. They live **here**, in the governed,
versioned, CI-checked repo — not in a `.claude/` folder outside version control.
`settings.template.json` is a **thin pointer**; it contains wiring and no facts.

| Hook | Rung | Kills |
|---|---|---|
| `session_start.py` | 4 | **F1** — stale substrate read (8–12d, 200 OK, no error). Prints freshness, Needs-you, goals status, and any guard overdue for promotion. Reads the **local clone, never a URL** — the URL is what lied. |
| `pre_tool_use.py` | 4 | **F2** — Edit/Write silently truncating long files on the virtiofs mount. Also blocks `git` from the Cowork sandbox (orphan `index.lock`). **Fail-closed.** |

## Install (Beelink)

```
copy C:\Projects\eq-context\hooks\settings.template.json C:\Projects\.claude\settings.json
```

Then start a fresh session — hooks load at session start.

## Why fail-closed

The first version of `pre_tool_use.py` returned 0 lines for a path it couldn't resolve,
so a 308-line Edit sailed straight through. **It failed open, silently** — the exact bug
class the hook exists to kill. Caught only because the adversarial suite tested it.

**A guard that fails open without saying so is worse than no guard**: it produces the
feeling of safety and none of it. If we cannot prove a write is safe, we block. The cost
of a false block is one heredoc. The cost of a false allow is a destroyed file that
reports success.

## Testing

Run the adversarial suite before trusting any change to these files:

```bash
bash hooks/adversarial_test.sh
```

Every failure that ever escapes in real life gets **added to the suite**. The system's own
history becomes its test corpus. That is the part that compounds.

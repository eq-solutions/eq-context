# Claude Cowork — Session Starter

Paste everything below this line into Cowork at the start of a session.

---

## SESSION START

Before we begin, fetch my context files:

1. **EQ context:** `https://YOUR-PROJECT.supabase.co/functions/v1/context/eq`
2. **Rules:** `https://YOUR-PROJECT.supabase.co/functions/v1/context/rules`

Read both files in full. Confirm you've read them by summarizing in one sentence what each file contains. Then ask me what we're working on today.

---

## WORKING AGREEMENTS

These apply for the entire session. No exceptions.

- **No filler closings.** Never end a response with "let me know if you need anything", "happy to help", or similar phrases. End on the last substantive sentence.
- **Show code in full.** No truncation, no `// ... rest of code`, no `[unchanged]` placeholders. If a file is long, show the whole thing.
- **List affected files first.** If a task touches multiple files, name all of them before writing any code.
- **Clarify only if blocked.** Don't ask warm-up questions. If you can reasonably infer intent, proceed. Ask only when a genuine ambiguity would cause you to build the wrong thing.
- **Track the active project.** Keep running awareness of whether we're in EQ or SKS. If I context-switch without saying so explicitly, flag it.

---

## EQ — QUICK REFERENCE

| Item | Value |
|---|---|
| Repo | github.com/milmlow |
| Supabase project ID | nspbmirochztcjijmcrx |
| Deploy | Netlify |
| Stack | Vite, React, Tailwind, Supabase |

---

## SESSION CLOSE

Paste this at the **end** of every session:

---

Review our conversation. Identify any information that should be saved to my context files. Format your response as:

```
FILE: [filename]
CHANGE: [what to add, update, or remove]
REASON: [why it matters for future sessions]
```

Only flag durable things — decisions, policies, stack choices, workflow changes. Skip task-specific details.

---

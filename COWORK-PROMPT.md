# Claude Cowork — Session Starter

Paste everything below this line into Cowork at the start of a session.

---

## SESSION START

Before we begin, fetch my context files from the canonical store:

1. **Master context:** `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/eq` (maps to CLAUDE.md)
2. **AI rules:** `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/rules` (maps to AI-RULES.md)
3. **Pending state:** `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/state/pending.md`

Read all three in full. Confirm you've read them by summarising in one sentence what each contains. Then ask me what we're working on today.

---

## WORKING AGREEMENTS

These apply for the entire session. No exceptions.

- **Finish what you start.** Every recommendation made or accepted in this session must be completed before close, or explicitly deferred to `state/pending.md` with a date. No half-applied work. (See `rules/non-negotiables.md` §0.)
- **No filler closings.** Never end a response with "let me know if you need anything", "happy to help", or similar. End on the last substantive sentence.
- **Show code in full.** No truncation, no `// ... rest of code`, no `[unchanged]` placeholders. If a file is long, show the whole thing.
- **List affected files first.** If a task touches multiple files, name all of them before writing any code.
- **Clarify only if blocked.** Don't ask warm-up questions. If you can reasonably infer intent, proceed. Ask only when a genuine ambiguity would cause you to build the wrong thing.
- **Track the active project.** Keep running awareness of whether we're in EQ or SKS. If I context-switch without saying so explicitly, flag it.
- **Pre-mortem before building.** 3 risks + mitigations stated before any build session starts.

---

## INFRASTRUCTURE QUICK REFERENCE

### Supabase — THREE projects, do not confuse

| Project ID | Name | Use |
|---|---|---|
| `nspbmirochztcjijmcrx` | sks-labour | **LIVE SKS DATA — never touch without explicit "SKS live" instruction** |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | EQ Field demo backend |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Canonical context store (this one) |

### GitHub
- Orgs: `eq-solutions` (primary) + personal `milmlow`
- **MCP is read-only (403 on writes).** All writes manual via browser or Cowork until fixed at `github.com/settings/installations`.

### Deploy map
- EQ Field → Netlify Drop → eq-solves-field.netlify.app
- SKS Labour → GitHub main → Netlify CD → sks-nsw-labour.netlify.app
- EQ Solves Service → GitHub → Netlify CD
- eq.solutions → Cloudflare Pages zip
- EQ Expenses / EQ Variations → Netlify Drop

### Stack
Vite + React + Tailwind + Supabase + Netlify + TypeScript (always). Legacy single-HTML apps stay vanilla JS by design — do not migrate without reason.

---

## COWORK GUARDRAILS

- Never push to demo branch without explicit instruction
- Never deploy to eq-solves-field.netlify.app directly
- Never delete files without permission
- Never hardcode API keys or secrets
- Any file touching SKS Supabase must be clearly scoped
- Auth changes require Chat review before deployment
- State intended actions before proceeding
- Working before refactoring — always
- Every Netlify/Cloudflare Pages site ships with a `_headers` security file

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

Then:
1. UPDATE `state/pending.md` — tick completed items, add new ones
2. INSERT `sessions/YYYY-MM-DD.md` — log what was built/decided
3. UPDATE relevant `changelog/[PROJECT].md` if code was touched
4. Push to GitHub main — Action syncs to Supabase automatically within ~20 seconds

---

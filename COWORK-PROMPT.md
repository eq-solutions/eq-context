# Claude Cowork — Session Starter

Paste everything below this line into Cowork at the start of a session.

---

## SESSION START

Before we begin, fetch my context files from the canonical store:

1. **Master context:** `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/claude` (maps to CLAUDE.md)
2. **Cross-LLM rules:** `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/agents` (maps to AGENTS.md)

Read both in full. Confirm you've read them by summarising in one sentence what each contains.

**Then ask:** "Is this an EQ session or an SKS session?"

Based on the answer:
- **EQ session:** also fetch `eq/README.md` and `eq/pending.md`
- **SKS session:** also fetch `sks/README.md`, `sks/pending.md`, and `sks/active.md`
- **Cross-tier:** fetch both. State explicitly which tier owns the work.

Then ask what we're working on today.

---

## WORKING AGREEMENTS

These apply for the entire session. No exceptions.

- **Tier discipline.** Once we've named the tier, don't surface other-tier content unprompted. If something OPS-relevant comes up (entities, tax, infra), explicitly load `/ops/` files — don't pull from memory.
- **Finish what you start.** Every recommendation made or accepted in this session must be completed before close, or explicitly deferred to the relevant tier's `pending.md` with a date. No half-applied work. (See `rules/non-negotiables.md` §0.)
- **No filler closings.** Never end a response with "let me know if you need anything", "happy to help", or similar. End on the last substantive sentence.
- **Show code in full.** No truncation, no `// ... rest of code`, no `[unchanged]` placeholders. If a file is long, show the whole thing.
- **List affected files first.** If a task touches multiple files, name all of them before writing any code.
- **Clarify only if blocked.** Don't ask warm-up questions. If you can reasonably infer intent, proceed. Ask only when a genuine ambiguity would cause you to build the wrong thing.
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

### Deploy map (post-cull, 2026-05-04)
- EQ Field → Netlify Drop → eq-solves-field.netlify.app (LEAD MODULE)
- SKS Labour → GitHub main → Netlify CD → sks-nsw-labour.netlify.app
- EQ Solves Service → GitHub → Netlify CD
- eq.solutions → Cloudflare Pages zip

### Killed / deferred (do not reference as live)
- EQ Variations, EQ Compliance, EQ Ops — killed
- EQ Quotes — deferred 6mo
- EQ Expenses — internal SKS tool only
- AHD — parked to 2027

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
FILE: [tier]/[filename]
CHANGE: [what to add, update, or remove]
REASON: [why it matters for future sessions]
```

Only flag durable things — decisions, policies, stack choices, workflow changes. Skip task-specific details.

Then:
1. UPDATE relevant `[tier]/pending.md` — tick completed items, add new ones
2. INSERT `sessions/YYYY-MM-DD.md` — log what was built/decided
3. UPDATE relevant `[tier]/changelog/*.md` if code was touched
4. Push to GitHub main — Action syncs to Supabase automatically within ~20 seconds

---

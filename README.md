# eq-context

Private context repository for EQ Solutions — used by Claude (chat, Cowork, Code)
to maintain continuity across sessions.

## How it works

Every conversation with Claude that produces new knowledge, decisions, or state changes
ends with "update the MD". Claude commits only the files that changed, with a clear
commit message describing what was added.

## Structure

```
CLAUDE.md                  ← Master index — Claude reads this first, always
rules/
  deployment.md            ← Deployment guardrails, never break these
  brand.md                 ← Colours, fonts, logo rules
  non-negotiables.md       ← Hard rules that override everything
state/
  products.md              ← Current status of every product
  pending.md               ← Active to-do list — updated every session
  entities.md              ← Business entities, accounts, contacts
knowledge/
  architecture.md          ← Why things are built the way they are
  lessons.md               ← Technical gotchas — append only
  decisions.md             ← Key decisions and their reasoning
sessions/
  YYYY-MM-DD.md            ← What happened each session
```

## Update frequency

| File | How often |
|------|-----------|
| CLAUDE.md | Only when structure changes |
| rules/* | Rarely — deliberate decisions only |
| state/pending.md | Every session |
| state/products.md | When product status changes |
| knowledge/lessons.md | When a new lesson is learned |
| knowledge/decisions.md | When a key decision is made |
| sessions/* | Every session (new file per date) |

## Never do

- Edit this repo on the main branch directly for large changes — use a session update
- Delete old session logs — they are the audit trail
- Merge state and rules — they have different update frequencies for a reason

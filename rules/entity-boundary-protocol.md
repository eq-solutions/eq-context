# Entity Boundary Protocol

**Trigger:** any task that touches repos, credentials, or data from both EQ Solutions and SKS Technologies in the same change; any task selecting a deploy target; any task reading or writing a Supabase key.

## Why this exists

SKS Technologies and EQ Solutions are separate legal entities sharing one Claude Code workspace (`C:\Projects`). The rule — "never mix code, credentials, or data," "NEVER cross-deploy" — is one line in global `CLAUDE.md`, easy to skip under task pressure. The naming in this workspace actively works against it (see Gotchas).

## Steps

1. **Classify every repo touched this task by entity** before writing anything:

   | Entity | Repos |
   |---|---|
   | EQ Solutions | eq-cards, eq-intake, eq-shell, eq-field, eq-solves-service, eq-roles, eq-ui, eq-design-tokens, eq-context, eq-solves-assets |
   | SKS Technologies | sks-nsw-labour |

   If a task's file list spans both rows, stop and flag it before continuing — this is the case the rule exists for.

2. **Classify every credential/DB connection touched, the same way.** Two SKS-adjacent systems are not the same thing — conflating them is its own failure mode:
   - **ehow** (`ehowgjardagevnrluult`) — the EQ Suite's shared canonical DB. SKS Technologies is a *tenant* inside it (tenant ID `7dee117c-98bd-4d39-af8c-2c81d02a1e85`), alongside a demo tenant. This is EQ-owned infrastructure serving SKS as a customer.
   - **SKS live Supabase** (`nspbmirochztcjijmcrx`) — SKS Technologies' own separate system. Per `eq-context/CLAUDE.md` Hard Rules: do not touch it unless Royce explicitly says "SKS live."

   Don't infer which is meant from context — if a task says "SKS" and touches Supabase, confirm which of the two before running anything against it.

3. **Never cross-deploy.** A repo classified EQ in step 1 deploys only to its own EQ-suite URL (see `deploy-topology-protocol.md` for *which* URL — not *when*, that's `rules/deployment.md`); a repo classified SKS deploys only to `sks-nsw-labour.netlify.app`. If a task's instructions imply otherwise, that's a signal to stop and confirm, not a green light.

4. **State the classification before acting** — which entity owns each repo/credential touched, and explicit confirmation nothing crosses the line — not a silent assumption.

## Gotchas

- **A path segment is not an entity signal.** `core.eq.solutions/sks/field` is a path under an EQ Solutions domain, served by the EQ-owned `eq-field` repo — SKS is the *tenant*, not the *owner*. See `deploy-topology-protocol.md` incident 1. The literal string "sks" in a URL has already caused this exact misclassification once.
- **"SKS" in a request is ambiguous between two Supabase projects** — ehow (EQ-owned, SKS-as-tenant) and the SKS live project (SKS-owned, standalone). Resolve which one before writing a query, not after.
- **Cross-entity is usually invisible in a diff.** A PR that touches one eq-* repo and reads a value from an SKS-owned source (or vice versa) can look completely ordinary in review. The check has to happen at classification time (step 1), not by hoping it looks wrong later.

# Deploy Topology Protocol

**Trigger:** any task that names a live URL (`core.eq.solutions`, `field.eq.solutions`, `service.eq.solutions`, `sks-nsw-labour.netlify.app`, `eq.solutions`), asks "which repo serves X", or precedes a deploy/build decision.

## Why this exists

Two confirmed incidents, same failure shape — assuming deploy topology from naming instead of verifying it:

1. **`core.eq.solutions/sks/field` mixup** (corrected 2026-08-23) — the path contains "sks", but it's served by **eq-field** (an EQ repo; SKS is its pilot tenant, not its owner), not the separate `sks-nsw-labour` repo. Verified live: sidebar showed eq-field's own feature set, the page read "Loading EQ Field…", and a real write round-tripped to `app_data.field_people` on ehow.
2. **`eq-solves-field.netlify.app` / `eq-solves-service.netlify.app`** — both read as the obvious Netlify site name for their repo. Both are wrong: `eq-solves-field.netlify.app` has been dead since mid-2026 (real domain: `field.eq.solutions`); `eq-solves-service.netlify.app` was never the live domain at all — the Netlify site's internal name is `eq-service`, the custom domain is `service.eq.solutions`.

Naming similarity is not evidence. Verify.

## Scope note

This protocol covers repo/domain **ownership** only. It does not cover deploy mechanics or timing for any repo — that subject lives solely in `rules/deployment.md`; this file does not restate it.

## Steps

1. **Confirm which repo owns the site** from `system/infrastructure.md` / `eq-context/CLAUDE.md`'s "Where Things Live" table as a starting lead, not a final answer.

2. **If the task references a *path* under a domain** (e.g. a Shell-embedded path, `core.eq.solutions/ops`), don't infer the owning repo from the path segment's name. Load the app (browser or `curl`) and read what actually renders — page title, sidebar feature set, a distinguishing string. That's what caught incident 1.

3. **If the task references a Netlify subdomain** (`*.netlify.app`), don't assume it matches the repo name. Confirm via the Netlify MCP (`netlify-project-services-reader` / `netlify-deploy-services-reader`) which project owns that site and what its custom domain actually is — site *name* and site *domain* are independently set and have already diverged twice.

4. **State the verified repo before acting** — confirmed live, not assumed from a table or from naming.

## Gotchas

- A path segment matching an entity name does not mean that entity's repo serves it. See incident 1.
- A Netlify site's internal *name* is not its custom *domain*. Both incidents above hinged on exactly this gap.
- `eq-solves-field.netlify.app` is dead. Never deploy to it, never treat it as a source of truth for "what's live."
- This overlaps `entity-boundary-protocol.md` at exactly the path-mixup case in incident 1 — a URL that looks SKS-owned but is EQ-served. Run both checks when a task crosses a URL and an entity line at once.

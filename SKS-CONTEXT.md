# CLAUDE.md — EQ Solutions

**Owner:** Royce · EQ Solutions · GitHub: [milmlow](https://github.com/milmlow)  
**Stack:** Vite · React · Tailwind · Supabase · Netlify

---

## Start of every session

1. Read this file first — always.
2. Check if a `/docs` folder exists. If it does, read `EQ-CONTEXT.md` and `AI-RULES.md` before starting any work.

---

## Hard rules

- Always use **TypeScript**. No plain JS files.
- Never **truncate code** — write every file in full, no `// ... rest unchanged` shortcuts.
- Never modify **package.json** without flagging the change and getting confirmation first.
- Never switch **package managers** — stay on `npm` unless explicitly told otherwise.
- The **Supabase client** lives in `/src/lib/supabase.ts`. Do not recreate or duplicate it elsewhere.
- Use **`.env.local`** for all local environment variables. Never hardcode API keys or secrets.
- Before any **database change** (migrations, schema edits, RLS policies): state exactly what you're changing and why, then wait for confirmation before proceeding.
- Never push directly to **`main`** without flagging it first.

---

## Repo structure

```
/src
  /components
  /pages
  /lib          ← supabase.ts lives here
  /hooks
  /types
/docs           ← EQ-CONTEXT.md and AI-RULES.md live here
/public
CLAUDE.md       ← you are here
```

---

## Git discipline

| Type | Prefix |
|---|---|
| New feature | `feat:` |
| Bug fix | `fix:` |
| Context / docs | `context:` |
| Refactor | `refactor:` |

**Branch naming:** `feature/description` or `fix/description`

---
title: SYSTEM — Git Automation for eq-context
owner: Royce Milmlow
last_updated: 2026-07-16
scope: How auto-push, credential helpers, and hooks are wired for the substrate repo
read_priority: reference
status: live
---

# SYSTEM — Git Automation for eq-context

The eq-context substrate is the source of truth. Every edit must reach GitHub
`main`, where it is live immediately via raw URLs — there is no Supabase cache
and no sync step (see "Substrate serving" below). This file documents how that
happens automatically and how to recover when the automation breaks.

---

## The Loop

```
edit file → git commit → post-commit hook → git push → GitHub main →
live immediately via raw URLs (raw.githubusercontent.com/eq-solutions/eq-context/main/<path>)
```

Hands-on steps: **edit + commit only**. Everything else runs by itself.

---

## Post-Commit Hook

`.githooks/post-commit` is a POSIX shell script tracked in the repo. It runs
after every commit and pushes `main` to `origin`. Feature branches are
skipped so exploratory work doesn't auto-publish.

Activation per clone (one-time):

```powershell
cd C:\Projects\eq-context
.\scripts\install-hooks.ps1
```

That runs `git config core.hooksPath .githooks` — git then resolves hooks from
the in-repo directory directly. No copying into `.git/hooks`. Cloning
fresh and forgetting to re-run `install-hooks.ps1` is the only way to
end up without the hook.

### Bypass for a single commit

```bat
set SKIP_AUTOPUSH=1
git commit -m "WIP: don't broadcast yet"
set SKIP_AUTOPUSH=
```

### Disable entirely

```bat
git config --unset core.hooksPath
```

### Failure modes the hook handles

- **Not on main** → silently skips (intentional)
- **Push fails** → commit stays local, prints recovery hints, exits clean
- **Auth fails** → likely PAT expiry, see `ops/pending.md` rotation reminder

A failed push never undoes a commit. The commit is yours; the push is
best-effort.

---

## Credential Helpers (Per-URL)

Git on this machine uses per-URL credential helpers so two GitHub
identities can coexist without prompts:

| URL pattern | Identity | Credential source |
|---|---|---|
| `https://github.com/eq-solutions/*` | eq-solutions org PAT | `%USERPROFILE%\.git-credentials` |
| `https://github.com/Milmlow/*` | Milmlow user PAT | `%USERPROFILE%\.git-credentials` |

Both PATs are fine-grained. **Current security status lives in
`system/infrastructure.md` → "GitHub PATs" — as of that file's last edit
all 3 tokens were flagged compromised (committed to substrate 2026-05-15→19,
caught by GitHub push-protection) with an unresolved rotation checklist.
The "expire 2026-05-19" framing here was stale and is removed — don't infer
from it that rotation happened.** Verify current token status against
`infrastructure.md` and the actual credential files before assuming either
"routine" or "resolved."

### How they're wired

`%USERPROFILE%\.git-credentials` holds entries of the form:

```
https://<username>:<pat>@github.com
```

…one per identity. Git's built-in `store` helper reads from this file by
default when `credential.helper = store` is set globally:

```bat
git config --global credential.helper store
```

For more aggressive separation (e.g. pointing at a different file per
URL), per-URL `credential.<url>.helper` entries can be set in
`~/.gitconfig`. The 2026-05-14 setup uses the simpler shared-file
approach — both identities live in one `.git-credentials`, git picks
the right one based on the host:user combination in the remote URL.

### Verifying

```bat
git config --global --get credential.helper
git config --global --get-regexp credential
```

Both should return at minimum `store`. The first push after rotation
will repopulate the credentials file if it's missing.

### Never check this into the repo

`.git-credentials` lives in `%USERPROFILE%`, not in the repo. It contains
PATs in plaintext. If it ever appears under `C:\Projects\eq-context`,
delete it immediately and rotate the PATs — assume leaked.

---

## Push Failure Recovery

Most common failures and the one-line fix:

| Error | Cause | Fix |
|---|---|---|
| `[rejected] non-fast-forward` | Remote has commits you don't | `git pull --rebase && git push` |
| `Repository not found` | Wrong remote URL OR PAT lacks repo scope | Check `git remote -v` against actual GitHub repo |
| `Authentication failed` / 401 | PAT expired or revoked | Rotate PAT, update `%USERPROFILE%\.git-credentials` |
| `Permission denied (publickey)` | Remote is SSH not HTTPS | `git remote set-url origin https://...` |
| Push hangs forever | Credentials prompt waiting in background | Kill, re-run from a terminal that supports prompts |

---

## Multi-Repo Push (eq-cards, eq-solves-field)

`push-all.bat` at the repo root pushes the three EQ repos in sequence:
eq-context (priority), eq-cards, eq-solves-field.

This is a **manual fallback** — the per-repo post-commit hooks are the
primary mechanism. Use `push-all.bat` when you've batch-committed across
multiple repos and want a single command to ship them all.

Hooks for eq-cards and eq-solves-field are NOT installed yet — only
eq-context has been wired. Adding per-repo hooks is a pending item.

---

## Substrate serving (no sync)

There is no sync job. The substrate *is* the public GitHub repo — assistants read
files directly via raw URLs
(`https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>`), so a push
to `main` is live immediately. The former `sync-context.yml` Action (which upserted
markdown into a `context_files` table in Supabase project `urjhmkhbgaxrofurpbgc`,
eq-solves-service-dev) is retired — that project was deleted 2026-06-22. See
`system/architecture.md` for the current model and `system/lessons.md` for the
historical footguns (duplicate path lists, edge-function path handling).

Verification after any push — confirm `main` serves the new content:

```bash
curl -s https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path> | head
```

---

## What's Deliberately Not Automated

- **Commit messages** — every commit is intentional; no auto-message generation
- **File watching / auto-commit** — would create noisy history; substrate is content, not artefacts
- **Branch creation** — main is the only auto-published branch by design
- **PAT rotation** — manual, calendar-reminded

The boundary is: commits are deliberate human decisions, propagation is automatic.

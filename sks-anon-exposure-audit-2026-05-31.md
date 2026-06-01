# SKS canonical anon-exposure audit + canonical RPC hardening — 2026-05-31

**Status:** changes applied to sks-canonical (prod), verified safe. EQ control plane assessed (no action). Several follow-ups open.
**Author:** session via Supabase MCP (`dev@eq.solutions`). **Not committed by that session** — placed in eq-context for the branch owner to commit.

## TL;DR
A Supabase security-advisor triage on **sks-canonical** (`ehowgjardagevnrluult`) expanded into an anon-exposure audit across all three canonical projects. The one real hole — anyone with the SKS anon key could read/write/delete all SKS Quotes data — is **closed**. The EQ control plane was swept and is **sound** (auth table protected). No app breakage (verified via live logs).

## What changed on sks-canonical (3 migrations, all committed cleanly in DB)
1. **`pin_search_path_sks_quotes_functions`** — pinned `search_path = public` on 8 `sks_quotes_*` functions (advisor `0011`). No behaviour change.
2. **`secdef_caller_tenant_guard`** (= `eq-intake/sql/030`, merged via PR eq-solutions/eq-solves-intake#21) — 4 `SECURITY DEFINER` RPCs (`eq_read_customers_by_intake`, `eq_read_staff_by_intake`, `app_data.submit_safety_record`, `app_data.approve_safety_record`) now self-gate on the JWT tenant; `service_role`/server bypasses. Closes a cross-tenant read/write gap (advisor `0029`). Applied to **sks-canonical only** — the EQ tenant doesn't host these RPCs yet.
3. **`revoke_anon_auth_grants_sks_quotes`** — `revoke all ... from anon, authenticated` on 13 `sks_quotes_*` tables + `audit_log`. **This is the main fix.** Those tables had full anon grants + an `org_isolation` policy keyed to a *constant* `org_id` (no caller check) = anon key holder could read/alter/delete all SKS quoting data. Quotes uses `service_role` (bypasses grants), so unaffected. Verified: anon 0 privs, authenticated 0 privs, service_role full on all 14.

## Audit result across the 3 canonical projects
- **sks-canonical (`ehowgjardagevnrluult`)** — hole above, now fixed. RLS is ON for all 80 tables (the old "RLS off" framing was stale). Residual: `eq_schema_registry` `USING(true)` read (trivial).
- **eq-canonical (`jvknxcmbtrfnxfrwfimn`, control plane, core.eq.solutions)** — **no critical exposure.** `shell_control` IS REST-exposed and anon has grants on `shell_control.users` (bcrypt PINs) / `tenants` / `module_entitlements`, **BUT** their `USING(true)` policies are `TO service_role`, so RLS default-denies anon → auth table safe. No anon-writable table anywhere. Only anon reads = `public.organisations` (org/tenant list), `public.module_entitlements` (module map), `eq_schema_registry` — read-only, low-sensitivity, via deliberate `*_anon_select` policies (likely pre-auth bootstrap).
- **eq-canonical-internal (`zaapmfdkgedqupfjtchl`)** — **clean.** Every anon-granted table is caller-scoped.

## Verified safe (live logs, post-change)
All 3 migrations committed cleanly; zero permission/RLS errors after; Quotes (`python-httpx`/service_role) getting 200s on `sks_quotes*`/`audit_log`/`sks_staff` (estimator picker) incl. latest entries. **Unrelated pre-existing bug noted** (NOT from these changes): Quotes POST to `/rest/v1/audit_log` 400s with `invalid input syntax for type bigint` — app sends a UUID into `audit_log.actor_id` (bigint); audit row silently dropped. Worth a separate fix in eq-quotes-port.

## Instant rollback (if Quotes ever misbehaves)
```sql
grant all on
  public.sks_quotes, public.sks_quotes_customers, public.sks_quotes_contacts,
  public.sks_quotes_contact_links, public.sks_quotes_config, public.sks_quotes_rates,
  public.sks_quotes_rate_presets, public.sks_quotes_materials, public.sks_quotes_scope_templates,
  public.sks_quotes_status_history, public.sks_quotes_vocab, public.sks_quotes_documents,
  public.sks_quotes_attachments, public.audit_log
  to anon, authenticated;
```

## Open follow-ups
1. **Keystone / "don't forget":** extend `eq-shell/scripts/check-tenant-drift.mjs` with the anon-grant invariant ("no table reachable by anon/authenticated without a caller-scoped policy; control tables service_role-only") and **schedule** it across all 3 canonical projects. The advisor missed both the `sks_quotes_*` hole and the org-list reads — this gate would catch future drift.
2. **Version-control the revoke** as a migration in eq-quotes-port (`migrations/` dir exists). Applied to DB, not yet in git.
3. **Decisions to make:** (a) rotate the SKS anon key + check `audit_log`/data for prior abuse (constant-org policy + open grants means prior exploit is possible but unprovable retroactively); (b) confirm-or-tighten the EQ `*_anon_select` reads on jvkn (org list / module map) — intended bootstrap, or lock down?
4. **Migration cutover unverified:** sks-canonical is the active authoritative store for quotes data (by design per `eq-quotes/scripts/migrate_to_canonical.py` + live traffic), but whether **sks-labour** (`nspbmirochztcjijmcrx`) still holds a stale second copy was not checked.

## Pointers
- Migration code: `eq-intake/sql/030_secdef_caller_tenant_guard.sql`
- Lockdown plan (Quotes anon path was service_role, so revoke was low-risk): `~/.claude/plans/sks-quotes-anon-lockdown.md`
- Likely related concurrent work: `security-secret-rotation-runbook-2026-05-31.md` (this repo, untracked) — the anon-key rotation in #3a may belong there.

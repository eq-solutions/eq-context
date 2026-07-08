#!/usr/bin/env node
// Access-model parity harness — computes a deterministic effective-permissions
// snapshot for every (user, tenant) grant row, so a change to the canonical
// matrix, tenant overrides, or group perms can be diffed before/after.
//
// Usage:
//   node compute-snapshot.mjs raw-grants-<date>.json > snapshot-<date>.json
//
// Input: raw grant rows (see raw-grants-2026-07-08.json) — one row per active
// (user, tenant) membership: { user_id, tenant_id, role, is_platform_admin,
// group_perms[], tenant_grants[], tenant_denies[] }.
//
// Output: sorted per-user effective-permission list + a whole-file hash, so
// "no diff" is a single string comparison, not a manual read-through.
//
// Requires @eq-solutions/roles to be resolvable — run from within C:\Projects\eq-roles
// (or anywhere with it in node_modules / a linked workspace).

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolveEffectivePermissions } from '@eq-solutions/roles';

const inputPath = process.argv[2];
if (!inputPath) {
  console.error('Usage: node compute-snapshot.mjs <raw-grants.json>');
  process.exit(1);
}

const rows = JSON.parse(readFileSync(inputPath, 'utf8'));

const results = rows.map((r) => {
  const effective = resolveEffectivePermissions({
    role: r.role,
    groupPerms: [...(r.group_perms ?? []), ...(r.tenant_grants ?? [])],
    isPlatformAdmin: r.is_platform_admin === true,
    revokes: r.tenant_denies ?? [],
  });
  return {
    user_id: r.user_id,
    tenant_id: r.tenant_id,
    role: r.role,
    is_platform_admin: r.is_platform_admin === true,
    effective_perms: [...effective].sort(),
  };
}).sort((a, b) => (a.tenant_id + a.user_id).localeCompare(b.tenant_id + b.user_id));

const canonical = JSON.stringify(results);
const hash = createHash('sha256').update(canonical).digest('hex');

const summary = {
  generated_at_note: 'stamp manually — Date.now() unavailable in this harness context',
  input: inputPath,
  row_count: results.length,
  hash,
  results,
};

console.log(JSON.stringify(summary, null, 2));

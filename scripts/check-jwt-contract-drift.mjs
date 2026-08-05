#!/usr/bin/env node
/**
 * Shell→Service JWT handoff contract drift guard (cross-repo).
 *
 * Why this exists: the `app_metadata` claim shape of the Shell→Service login-
 * handoff JWT is declared across THREE places:
 *   - eq-shell MINTS it       — SupabaseJwtClaims.app_metadata, still a local,
 *                               independently-declared interface
 *                               (netlify/functions/_shared/supabase-jwt.ts)
 *   - eq-service CONSUMES it  — ServiceJwtClaims.app_metadata, now typed as
 *                               `ShellHandoffClaims & { <local additive keys> }`
 *                               (lib/auth/service-jwt.ts)
 *   - @eq-solutions/contracts — ShellHandoffClaims, the shared base type
 *                               eq-service imports (index.ts)
 * A rename or drop on the mint side breaks Service login at runtime (the user is
 * bounced to a login screen, or lands in an empty app) with nothing failing at
 * PR time in either repo. eq-service's own `canonical-types-drift` guard covers
 * its DB↔types seam; this covers the cross-repo CONTRACT seam neither repo's CI
 * can see. Same philosophy: scheduled, read-only, surface-don't-block.
 *
 * 2026-08-06 update: eq-service migrated its consume-side type to import
 * `ShellHandoffClaims` from `@eq-solutions/contracts` instead of declaring the
 * full shape locally — this is the "durable fix" this file's previous version
 * called out below, and it's why this guard started failing (exit 2): the old
 * regex expected a plain `app_metadata: { ... }` object literal and couldn't
 * see keys behind `app_metadata: ShellHandoffClaims & { ... }`. eq-shell has
 * NOT made the matching move yet — SupabaseJwtClaims is still a local,
 * independently-declared interface — so the shared package does NOT yet make
 * this canary redundant, it just moved WHERE part of the consume-side shape
 * lives. This guard now reads all three sources and unions eq-service's local
 * additive keys with @eq-solutions/contracts' ShellHandoffClaims keys to get
 * the full consumed set, same mint-vs-consume comparison as before.
 *
 * Caveat this version does NOT cover: eq-shell and eq-service each pin
 * `@eq-solutions/contracts` independently (`github:eq-solutions/eq-contracts#vX.Y.Z`
 * in package.json, not a workspace link) — tsc in eq-service only checks
 * against WHATEVER TAG eq-service has pinned, not against eq-shell's pin or
 * the package's latest tag. This script reads the contract package from its
 * `main` branch (verified 2026-08-06: identical commit to the `v0.1.0` tag
 * both repos currently pin), a reasonable proxy but not a pin-skew check. If
 * eq-shell ever migrates to import ShellHandoffClaims too, the REAL remaining
 * risk becomes "the two repos pin different contract tags" — neither this
 * script nor either repo's own tsc catches that. Worth a follow-up guard at
 * that point, not before.
 *
 * What it does: fetches all three files from raw GitHub (main), extracts the
 * `app_metadata` key set the mint side sets and the full key set the consume
 * side (local + shared package) requires, and diffs them:
 *   - CONSUMER expects a key the MINT side never sets → ❌ broken contract, exit 1
 *     (Service reads `undefined` at runtime — a real login / empty-app break).
 *   - MINT sets a key the CONSUMER doesn't read → informational. Known-intentional
 *     asymmetries (see KNOWN_MINT_ONLY) are acknowledged; anything else is ⚠️
 *     "new mint key Service hasn't adopted".
 *   - Any interface/claim block can't be located → ❌ exit 2 (moved/renamed/
 *     restructured — this guard must be updated; failing loud beats a silent
 *     false-pass).
 *
 * Read-only HTTPS GETs against raw.githubusercontent.com. Dependency-free
 * (global fetch, Node 18+). eq-shell/eq-service/eq-contracts are private
 * repos, so this needs GH_TOKEN (EQ_CONTEXT_PAT) set — raw.githubusercontent.com
 * accepts a bearer token for private-repo content the same way the Contents
 * API does.
 *
 * Upgrade path: once eq-shell also imports ShellHandoffClaims directly (no
 * local SupabaseJwtClaims.app_metadata redeclaration), `tsc` in each repo
 * becomes a real per-repo gate and this canary's structural half retires —
 * see the pin-skew caveat above for what would still be missing at that point.
 *
 * Local testing: set SHELL_SRC_FILE / SERVICE_SRC_FILE / CONTRACT_SRC_FILE to
 * local file paths to bypass the network (e.g. with tampered fixtures).
 */

import { readFileSync, appendFileSync } from 'node:fs'

const SOURCES = {
  mint: {
    label: 'eq-shell SupabaseJwtClaims',
    url: 'https://raw.githubusercontent.com/eq-solutions/eq-shell/main/netlify/functions/_shared/supabase-jwt.ts',
    iface: 'SupabaseJwtClaims',
    envOverride: 'SHELL_SRC_FILE',
  },
  consume: {
    label: 'eq-service ServiceJwtClaims',
    url: 'https://raw.githubusercontent.com/eq-solutions/eq-service/main/lib/auth/service-jwt.ts',
    iface: 'ServiceJwtClaims',
    envOverride: 'SERVICE_SRC_FILE',
  },
  contract: {
    label: '@eq-solutions/contracts ShellHandoffClaims',
    url: 'https://raw.githubusercontent.com/eq-solutions/eq-contracts/main/index.ts',
    iface: 'ShellHandoffClaims',
    envOverride: 'CONTRACT_SRC_FILE',
  },
}

// Keys the mint side legitimately sets that the Service consumer intentionally
// does NOT read — acknowledged, never flagged as drift:
//   source_app  — mint provenance (which surface minted the token)
//   extra_perms — Field-only security-group grants (Service has no use for them)
//   worker_id   — canonical worker identity; eq-shell's own SupabaseJwtClaims
//                 comment states it's omitted for aud='service' by design
//                 (Service derives identity from tenant_id + sub, not a worker row)
const KNOWN_MINT_ONLY = new Set(['source_app', 'extra_perms', 'worker_id'])

const fmt = (arr) => arr.map((k) => '`' + k + '`').join(', ')

function printReport(lines) {
  const report = lines.join('\n')
  console.log(report)
  if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, report + '\n')
}

async function loadSource(src) {
  const override = process.env[src.envOverride]
  if (override) return readFileSync(override, 'utf8')
  const token = process.env.GH_TOKEN
  const headers = token ? { Authorization: `Bearer ${token}` } : {}
  const res = await fetch(src.url, { headers })
  if (!res.ok) {
    throw new Error(`Could not fetch ${src.label} — HTTP ${res.status} from ${src.url}. Repo/path renamed, repo is private and GH_TOKEN is unset/lacks access, or GitHub raw is down. Update scripts/check-jwt-contract-drift.mjs.`)
  }
  return res.text()
}

/**
 * Find `interface <name> { ... }` in `lines` and return its [startLine,
 * endLine] (both inclusive, 0-indexed) by brace-depth scanning from the
 * declaration. Comments are stripped first so a stray brace in prose never
 * mis-tracks depth. Returns null if the interface isn't found or its braces
 * never balance (block never closes before EOF).
 */
function findInterfaceBody(lines, interfaceName) {
  const start = lines.findIndex((l) => new RegExp(`interface\\s+${interfaceName}\\b`).test(l))
  if (start < 0) return null
  let depth = 0
  for (let i = start; i < lines.length; i++) {
    for (const ch of lines[i].replace(/\/\/.*$/, '')) {
      if (ch === '{') depth++
      else if (ch === '}') {
        depth--
        if (depth === 0) return [start, i]
      }
    }
  }
  return null
}

/** Top-level `key:` / `key?:` names directly inside an interface body (depth 1, no nesting). */
function extractTopLevelKeys(lines, [start, end]) {
  const keys = new Set()
  let depth = 0
  for (let i = start; i <= end; i++) {
    const line = lines[i].replace(/\/\/.*$/, '')
    if (depth === 1) {
      const k = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:/)
      if (k) keys.add(k[1])
    }
    for (const ch of line) {
      if (ch === '{') depth++
      else if (ch === '}') depth--
    }
  }
  return keys
}

/**
 * Keys nested inside an `app_metadata: <optional type ref, e.g. "Foo &">? { ... }`
 * field within an interface body. Matches both a plain object literal
 * (`app_metadata: { ... }`) and an intersection with an imported base type
 * (`app_metadata: ShellHandoffClaims & { ... }`) — anything between the colon
 * and the opening brace is treated as a type reference to ignore. Returns null
 * if no such field is found (interface restructured — fail loud, don't guess).
 */
function extractAppMetadataKeys(lines, [start, end]) {
  let inMeta = false
  let depth = 0
  const keys = new Set()
  for (let i = start; i <= end; i++) {
    const line = lines[i].replace(/\/\/.*$/, '')
    if (!inMeta) {
      if (/app_metadata\s*:[^{};\n]*\{/.test(line)) { inMeta = true; depth = 1 }
      continue
    }
    if (depth === 1) {
      const k = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:/)
      if (k) keys.add(k[1])
    }
    for (const ch of line) {
      if (ch === '{') depth++
      else if (ch === '}') { depth--; if (depth === 0) return keys }
    }
  }
  return keys.size ? keys : null
}

async function run() {
  let mintSrc, consumeSrc, contractSrc
  try {
    ;[mintSrc, consumeSrc, contractSrc] = await Promise.all([
      loadSource(SOURCES.mint),
      loadSource(SOURCES.consume),
      loadSource(SOURCES.contract),
    ])
  } catch (e) {
    printReport(['# Shell→Service JWT contract drift', '', `**❌ ${e.message}**`])
    return 2
  }

  const mintLines = mintSrc.split(/\r?\n/)
  const consumeLines = consumeSrc.split(/\r?\n/)
  const contractLines = contractSrc.split(/\r?\n/)

  const mintBody = findInterfaceBody(mintLines, SOURCES.mint.iface)
  const consumeBody = findInterfaceBody(consumeLines, SOURCES.consume.iface)
  const contractBody = findInterfaceBody(contractLines, SOURCES.contract.iface)

  const out = ['# Shell→Service JWT contract drift', '']

  if (!mintBody || !consumeBody || !contractBody) {
    const missing = [
      !mintBody ? `\`${SOURCES.mint.iface}\` (${SOURCES.mint.label})` : null,
      !consumeBody ? `\`${SOURCES.consume.iface}\` (${SOURCES.consume.label})` : null,
      !contractBody ? `\`${SOURCES.contract.iface}\` (${SOURCES.contract.label})` : null,
    ].filter(Boolean).join(' and ')
    out.push(`**❌ Could not locate ${missing}.** The interface moved or was renamed — update scripts/check-jwt-contract-drift.mjs so the contract stays guarded.`)
    printReport(out)
    return 2
  }

  const mintKeys = extractAppMetadataKeys(mintLines, mintBody)
  const consumeLocalKeys = extractAppMetadataKeys(consumeLines, consumeBody)
  const contractKeys = extractTopLevelKeys(contractLines, contractBody)

  if (!mintKeys || (!consumeLocalKeys && contractKeys.size === 0)) {
    const missing = [
      !mintKeys ? `\`app_metadata\` field in ${SOURCES.mint.label}` : null,
      !consumeLocalKeys && contractKeys.size === 0 ? `\`app_metadata\` field in ${SOURCES.consume.label} or any keys in ${SOURCES.contract.label}` : null,
    ].filter(Boolean).join(' and ')
    out.push(`**❌ Could not locate ${missing}.** The claim shape moved or was restructured — update scripts/check-jwt-contract-drift.mjs so the contract stays guarded.`)
    printReport(out)
    return 2
  }

  const consumeKeys = new Set([...(consumeLocalKeys ?? []), ...contractKeys])

  const missingFromMint = [...consumeKeys].filter((k) => !mintKeys.has(k)).sort()
  const mintOnly = [...mintKeys].filter((k) => !consumeKeys.has(k)).sort()
  const unexpectedMintOnly = mintOnly.filter((k) => !KNOWN_MINT_ONLY.has(k))
  const acknowledgedMintOnly = mintOnly.filter((k) => KNOWN_MINT_ONLY.has(k))
  const broken = missingFromMint.length > 0

  out.push(
    broken
      ? `**❌ Contract broken — Service expects ${missingFromMint.length} claim(s) the Shell mint never sets.** Service reads these as \`undefined\` at runtime (login / empty-app break). Fix the mint side or the consumer type.`
      : '**✅ Contract intact** — every claim Service consumes is set by the Shell mint.',
    '',
  )
  if (missingFromMint.length) {
    out.push('## ❌ Consumed but never minted (regression)')
    out.push(`- ${SOURCES.consume.label} (+ ${SOURCES.contract.label}) declares, ${SOURCES.mint.label} omits: ${fmt(missingFromMint)}`, '')
  }
  if (unexpectedMintOnly.length) {
    out.push('## ⚠️ Minted but not consumed (new — adopt or allowlist)')
    out.push(`- ${SOURCES.mint.label} sets, consumer ignores: ${fmt(unexpectedMintOnly)}`)
    out.push('  If intentional (another consumer needs it), add it to KNOWN_MINT_ONLY in this script.', '')
  }
  if (acknowledgedMintOnly.length) {
    out.push(`_Acknowledged mint-only (by design): ${fmt(acknowledgedMintOnly)}._`)
  }
  out.push(`_Compared ${mintKeys.size} minted vs ${consumeKeys.size} consumed \`app_metadata\` keys (${contractKeys.size} from @eq-solutions/contracts, ${consumeLocalKeys ? consumeLocalKeys.size : 0} local to ${SOURCES.consume.label})._`)
  printReport(out)
  return broken ? 1 : 0
}

// Set exitCode and let the event loop drain — never call process.exit() right
// after fetch(), which races undici's keep-alive socket teardown and trips a
// libuv assertion on Windows (src/win/async.c). The process exits cleanly once
// the idle sockets close.
process.exitCode = await run()

#!/usr/bin/env node
/**
 * Shell→Service JWT handoff contract drift guard (cross-repo).
 *
 * Why this exists: the `app_metadata` claim shape of the Shell→Service login-
 * handoff JWT is declared INDEPENDENTLY in two repos, with no shared type:
 *   - eq-shell MINTS it     — SupabaseJwtClaims.app_metadata
 *                             (netlify/functions/_shared/supabase-jwt.ts)
 *   - eq-service CONSUMES it — ServiceJwtClaims.app_metadata
 *                             (lib/auth/service-jwt.ts)
 * A rename or drop on the mint side breaks Service login at runtime (the user is
 * bounced to a login screen, or lands in an empty app) with nothing failing at
 * PR time in either repo. eq-service's own `canonical-types-drift` guard covers
 * its DB↔types seam; this covers the cross-repo CONTRACT seam neither repo's CI
 * can see. Same philosophy: scheduled, read-only, surface-don't-block.
 *
 * What it does: fetches both files from raw GitHub (main), extracts the
 * `app_metadata` key set each side declares, and diffs them:
 *   - CONSUMER expects a key the MINT side never sets → ❌ broken contract, exit 1
 *     (Service reads `undefined` at runtime — a real login / empty-app break).
 *   - MINT sets a key the CONSUMER doesn't read → informational. Known-intentional
 *     asymmetries (see KNOWN_MINT_ONLY) are acknowledged; anything else is ⚠️
 *     "new mint key Service hasn't adopted".
 *   - Either interface can't be located → ❌ exit 2 (file moved/renamed — this
 *     guard must be updated; failing loud beats a silent false-pass).
 *
 * Read-only HTTPS GETs against public raw.githubusercontent.com. Dependency-free
 * (global fetch, Node 18+). No secret needed — eq-solutions repos are public.
 *
 * Upgrade path: the durable fix is a shared `@eq-solutions/contracts` package
 * exporting ONE claim type imported by both repos, so `tsc` becomes the gate.
 * This canary is the lean first cut until that exists.
 *
 * Local testing: set SHELL_SRC_FILE / SERVICE_SRC_FILE to local file paths to
 * bypass the network (e.g. with tampered fixtures).
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
}

// Keys the mint side legitimately sets that the Service consumer intentionally
// does NOT read — acknowledged, never flagged as drift:
//   source_app  — mint provenance (which surface minted the token)
//   extra_perms — Field-only security-group grants (Service has no use for them)
const KNOWN_MINT_ONLY = new Set(['source_app', 'extra_perms'])

const fmt = (arr) => arr.map((k) => '`' + k + '`').join(', ')

function printReport(lines) {
  const report = lines.join('\n')
  console.log(report)
  if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, report + '\n')
}

async function loadSource(src) {
  const override = process.env[src.envOverride]
  if (override) return readFileSync(override, 'utf8')
  const res = await fetch(src.url)
  if (!res.ok) {
    throw new Error(`Could not fetch ${src.label} — HTTP ${res.status} from ${src.url}. Repo/path renamed, or GitHub raw is down. Update scripts/check-jwt-contract-drift.mjs.`)
  }
  return res.text()
}

/**
 * Extract the top-level key names of
 *   interface <name> { ... app_metadata: { <keys> } ... }
 * Brace-depth scanner that strips `//` comments first, so commented field docs
 * and the header's example claim block never pollute the set. Returns a Set, or
 * null if the interface / its app_metadata block can't be located.
 */
function extractAppMetadataKeys(srcText, interfaceName) {
  const lines = srcText.split(/\r?\n/)
  let i = lines.findIndex((l) => new RegExp(`interface\\s+${interfaceName}\\b`).test(l))
  if (i < 0) return null
  const keys = new Set()
  let inMeta = false
  let depth = 0
  for (; i < lines.length; i++) {
    const line = lines[i].replace(/\/\/.*$/, '') // drop line/trailing comments
    if (!inMeta) {
      if (/app_metadata\s*:\s*\{/.test(line)) { inMeta = true; depth = 1 }
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
  return keys.size ? keys : null // block never closed → treat as not-found
}

async function run() {
  let mintSrc, consumeSrc
  try {
    ;[mintSrc, consumeSrc] = await Promise.all([loadSource(SOURCES.mint), loadSource(SOURCES.consume)])
  } catch (e) {
    printReport(['# Shell→Service JWT contract drift', '', `**❌ ${e.message}**`])
    return 2
  }

  const mintKeys = extractAppMetadataKeys(mintSrc, SOURCES.mint.iface)
  const consumeKeys = extractAppMetadataKeys(consumeSrc, SOURCES.consume.iface)
  const out = ['# Shell→Service JWT contract drift', '']

  if (!mintKeys || !consumeKeys) {
    const missing = [
      !mintKeys ? `\`${SOURCES.mint.iface}\` (${SOURCES.mint.label})` : null,
      !consumeKeys ? `\`${SOURCES.consume.iface}\` (${SOURCES.consume.label})` : null,
    ].filter(Boolean).join(' and ')
    out.push(`**❌ Could not locate ${missing}.** The interface moved or was renamed — update scripts/check-jwt-contract-drift.mjs so the contract stays guarded.`)
    printReport(out)
    return 2
  }

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
    out.push(`- ${SOURCES.consume.label} declares, ${SOURCES.mint.label} omits: ${fmt(missingFromMint)}`, '')
  }
  if (unexpectedMintOnly.length) {
    out.push('## ⚠️ Minted but not consumed (new — adopt or allowlist)')
    out.push(`- ${SOURCES.mint.label} sets, ${SOURCES.consume.label} ignores: ${fmt(unexpectedMintOnly)}`)
    out.push('  If intentional (another consumer needs it), add it to KNOWN_MINT_ONLY in this script.', '')
  }
  if (acknowledgedMintOnly.length) {
    out.push(`_Acknowledged mint-only (by design): ${fmt(acknowledgedMintOnly)}._`)
  }
  out.push(`_Compared ${mintKeys.size} minted vs ${consumeKeys.size} consumed \`app_metadata\` keys._`)
  printReport(out)
  return broken ? 1 : 0
}

// Set exitCode and let the event loop drain — never call process.exit() right
// after fetch(), which races undici's keep-alive socket teardown and trips a
// libuv assertion on Windows (src/win/async.c). The process exits cleanly once
// the idle sockets close.
process.exitCode = await run()

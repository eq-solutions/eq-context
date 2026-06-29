#!/usr/bin/env node
/**
 * Synthetic Shell→Service handoff probe (secret-drift canary).
 *
 * Catches the most catastrophic handoff failure — eq-service's EQ_SHELL_JWT_SECRET
 * drifting from the secret eq-shell signs handoff JWTs with (→ EVERY real login
 * 401s) — BEFORE a user hits it. The reactive auth-handoff canary (eq-service #373)
 * only fires on a victim's failed login; this fires proactively on a schedule.
 *
 * How: mint a short-lived HS256 JWT signed with the reference secret, carrying a
 * fully contract-valid synthetic identity for the live tenant slug, and POST it to
 * eq-service /api/shell-auth.
 *   - Secret matches  → 200 (handoff validated end-to-end). HEALTHY.
 *   - Secret mismatch → 401 invalid-token (signature rejected). ALERT — the
 *                       catastrophic case; every real login is failing right now.
 *   - 403 service-account-not-found → the live tenant slug stopped resolving
 *                       (de-provisioned / renamed?). ALERT.
 *   - 5xx / network → transient; retried once, then ALERT.
 *
 * Non-mutating: the synthetic token carries NO brand_color, so the 200 path mints
 * only a stateless JWT (returned in a Set-Cookie header, discarded by the probe)
 * and performs NO DB write. No session is persisted. It resolves the REAL tenant,
 * so it does NOT fire the slug_unresolved canary — no Sentry noise on healthy runs.
 *
 * Dependency-free (node:crypto, global fetch). No real identity, no session kept.
 *
 * Env:
 *   EQ_SHELL_JWT_SECRET  - the secret eq-shell signs handoff JWTs with (= the value
 *                          set as EQ_SHELL_JWT_SECRET on eq-service's Netlify site).
 *                          ⚠ ON ROTATION update this reference too, or the probe
 *                          false-alarms. (A zero-copy alternative is an eq-shell
 *                          scheduled function using its native SUPABASE_JWT_SECRET.)
 *   PROBE_TENANT_SLUG    - (optional) live tenant slug to resolve. Default 'sks'.
 *   SHELL_AUTH_URL       - (optional) endpoint. Default https://service.eq.solutions/api/shell-auth
 *
 * Skips cleanly (exit 0, advisory) if EQ_SHELL_JWT_SECRET is unset — add it to
 * eq-context GitHub secrets to arm the probe.
 */

import { createHmac } from 'node:crypto'
import { appendFileSync } from 'node:fs'

const SECRET = process.env.EQ_SHELL_JWT_SECRET || ''
const ENDPOINT = process.env.SHELL_AUTH_URL || 'https://service.eq.solutions/api/shell-auth'
const TENANT_SLUG = process.env.PROBE_TENANT_SLUG || 'sks'

function b64url(s) {
  return Buffer.from(s).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}

function mintProbeToken(secret) {
  const header = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const now = Math.floor(Date.now() / 1000)
  const payload = b64url(JSON.stringify({
    sub: 'handoff-probe-synthetic',
    exp: now + 120,
    app_metadata: {
      tenant_id: 'handoff-probe',          // remapped via slug; just needs to be present
      eq_role: 'employee',                 // lowest privilege; never used (no session kept)
      email: 'handoff-probe@eq.solutions', // synthetic identity
      tenant_slug: TENANT_SLUG,            // resolves → 200; no brand_color → no DB write
    },
  }))
  const sig = createHmac('sha256', secret).update(`${header}.${payload}`).digest('base64url')
  return `${header}.${payload}.${sig}`
}

function emit(lines, code) {
  const report = lines.join('\n')
  console.log(report)
  if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, report + '\n')
  process.exitCode = code
}

async function postOnce(token) {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token }),
  })
  let error
  try { error = JSON.parse(await res.text())?.error } catch { /* non-JSON body */ }
  return { status: res.status, error }
}

async function run() {
  if (!SECRET) {
    return emit([
      '# Shell→Service handoff probe', '',
      '**⏭ Skipped** — `EQ_SHELL_JWT_SECRET` not set. Add it to eq-context GitHub secrets (the value eq-shell signs handoff JWTs with) to arm the probe.',
    ], 0)
  }

  const token = mintProbeToken(SECRET)

  // One retry on transient failure (network / 5xx). Auth results (200/401/403) are
  // deterministic — classified immediately, no retry.
  let r
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      r = await postOnce(token)
    } catch (e) {
      if (attempt === 2) {
        return emit(['# Shell→Service handoff probe', '', `**❌ ALERT — could not reach ${ENDPOINT}** after ${attempt} attempts: ${e.message}.`], 1)
      }
      continue
    }
    if (r.status >= 500 && attempt === 1) continue // transient server error → retry once
    break
  }

  if (r.status === 200) {
    return emit(['# Shell→Service handoff probe', '', `**✅ Healthy** — handoff validated end-to-end against \`${ENDPOINT}\` (tenant \`${TENANT_SLUG}\`). EQ_SHELL_JWT_SECRET matches between eq-shell and eq-service.`], 0)
  }
  if (r.status === 401) {
    return emit([
      '# Shell→Service handoff probe', '',
      '**❌ ALERT — handoff secret mismatch.**',
      `eq-service rejected a token signed with the reference secret (HTTP 401 \`${r.error ?? ''}\`). EQ_SHELL_JWT_SECRET on eq-service no longer matches eq-shell's signing secret — **every real login is 401ing right now.** Check the secret on both Netlify sites (and this probe's reference copy, if it was just rotated).`,
    ], 1)
  }
  if (r.status === 403) {
    return emit([
      '# Shell→Service handoff probe', '',
      `**❌ ALERT — tenant \`${TENANT_SLUG}\` not resolving** (HTTP 403 \`${r.error ?? ''}\`). The signature was accepted (secret OK) but the slug maps to no active service.tenants row — de-provisioned or renamed?`,
    ], 1)
  }
  return emit([
    '# Shell→Service handoff probe', '',
    `**❌ ALERT — unexpected response: HTTP ${r.status} \`${r.error ?? ''}\`.** Expected 200. Could be a 500 (misconfig) or a contract change that rejected the probe token. Investigate.`,
  ], 1)
}

await run()

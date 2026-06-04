-- ============================================================
-- Migration: context_proposals
-- Date: 2026-05-14
-- Purpose: single-writer proposal queue for eq-context edits
--
-- Background:
-- eq-context is touched by three surfaces (Chat, Cowork, Code) and
-- racing local-filesystem commits caused drift and line-ending noise.
-- The new model is: Cowork is the only direct writer to main; other
-- surfaces propose edits via this table, which Cowork (or a scheduled
-- task) picks up and turns into atomic commits.
--
-- This is intentionally a queue, not a fancy collab system — keep
-- diff-and-apply discipline; review is human, not automated.
--
-- STATUS: APPLIED 2026-06-04 to the substrate project
-- (urjhmkhbgaxrofurpbgc) via Supabase migration `context_proposals`.
-- Table created empty; live posture verified — RLS on, anon INSERT-only,
-- anon SELECT revoked on both table and view.
--
-- HARDENING (2026-06-04): the anon INSERT path is reachable by anyone
-- holding the public anon key (it ships to browsers). Guards applied:
--   1. Per-column length CHECK constraints cap a single proposal's
--      footprint so the table can't be used for storage exhaustion.
--   2. The dead "proposer can read own" policy is removed (it keyed on
--      a JWT claim anon inserts never carry — it enforced nothing).
--   3. context_proposals_pending is security_invoker=true and has
--      SELECT revoked from anon/authenticated — a plain view would run
--      as owner and leak EVERY pending proposal past the table's RLS.
--   4. SELECT revoked from anon/authenticated on the base table too
--      (reads are service-role only).
-- Residual risk: volume (many small rows). RLS cannot rate-limit;
-- the consumer (scheduled task / Cowork poll, NOT YET BUILT) must add a
-- per-session/IP throttle, or INSERT should be restricted to authenticated.
-- ============================================================

create extension if not exists pgcrypto;

create table if not exists context_proposals (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),

  -- Where the proposal came from
  source text not null check (source in ('chat', 'cowork', 'code', 'api', 'other')),
  session_id text,           -- Cowork session or chat thread id
  proposer_email text,       -- best-effort attribution

  -- What the proposal targets
  target_path text not null, -- repo-relative, e.g. 'sks/active.md'
  current_sha text,          -- SHA of target file at time of proposal (optimistic check)

  -- The proposal itself
  change_type text not null default 'replace'
    check (change_type in ('replace', 'append', 'patch', 'create', 'delete')),
  proposed_content text,     -- full content for 'replace'/'create'; null for 'delete'
  patch_diff text,           -- unified diff for 'patch'
  rationale text,            -- human-readable why

  -- Review workflow
  status text not null default 'pending'
    check (status in ('pending', 'accepted', 'rejected', 'merged', 'superseded')),
  reviewed_at timestamptz,
  reviewed_by text,
  review_note text,

  -- Outcome
  github_commit_sha text,
  github_pr_url text,

  -- Free-form attribution / metadata
  metadata jsonb not null default '{}'::jsonb,

  -- Footprint caps — a single proposal cannot be used to exhaust storage.
  -- 256 KiB of content is far above any real MD edit; rationale/notes are
  -- prose-sized. Reject oversized payloads at write time.
  constraint proposed_content_len check (proposed_content is null or length(proposed_content) <= 262144),
  constraint patch_diff_len       check (patch_diff is null       or length(patch_diff)       <= 262144),
  constraint rationale_len        check (rationale is null         or length(rationale)        <= 8192),
  constraint review_note_len      check (review_note is null       or length(review_note)      <= 8192),
  constraint target_path_len      check (length(target_path) <= 512)
);

create index if not exists idx_context_proposals_status_created
  on context_proposals (status, created_at desc);

create index if not exists idx_context_proposals_target
  on context_proposals (target_path);

create index if not exists idx_context_proposals_source
  on context_proposals (source);

-- ============================================================
-- RLS: anyone with the anon key can INSERT (propose); only the
-- service role can update/delete/select-all. This matches the
-- pattern in the existing edge function for /functions/v1/context.
-- ============================================================
alter table context_proposals enable row level security;

-- Anyone can propose. Footprint is bounded by the *_len CHECK constraints
-- above; per-volume throttling is the consumer's job (see hardening note
-- in the header) — RLS cannot rate-limit.
drop policy if exists "anyone can propose" on context_proposals;
create policy "anyone can propose"
  on context_proposals
  for insert
  with check (true);

-- NOTE: the former "proposer can read own" SELECT policy was removed
-- 2026-06-04. It keyed on request.jwt.claims->>'session_id', but anon
-- inserts carry no such claim, so it granted read to no one — dead policy
-- masquerading as access control. Proposers do not read back through RLS;
-- the consumer (service role) reads the queue. If read-back is ever needed,
-- implement it through the edge function with an explicit token, not RLS.

-- Service role bypasses RLS automatically; no policy needed.

-- Reads are service-role only. Revoke the default SELECT grant so anon /
-- authenticated cannot even attempt to read the queue (RLS already returns
-- zero rows, but this removes the grant entirely — defence in depth).
revoke select on context_proposals from anon, authenticated;

-- ============================================================
-- Convenience view: pending queue sorted oldest-first.
-- security_invoker=true is LOAD-BEARING: a default (owner-rights) view
-- bypasses the base table's RLS, so anon could read every pending proposal
-- through it. With security_invoker the view honours the caller's RLS.
-- SELECT is also revoked from anon/authenticated as belt-and-suspenders.
-- ============================================================
create or replace view context_proposals_pending
  with (security_invoker = true) as
  select
    id,
    created_at,
    source,
    session_id,
    proposer_email,
    target_path,
    change_type,
    rationale,
    -- preview first 200 chars
    left(coalesce(proposed_content, patch_diff, ''), 200) as preview
  from context_proposals
  where status = 'pending'
  order by created_at asc;

revoke all on context_proposals_pending from anon, authenticated;

-- ============================================================
-- Application notes (not enforced in DB):
--
-- 1. The runtime context cache (/functions/v1/context/<slug>) reads
--    from GitHub via the existing sync-context workflow. This table
--    does NOT feed it directly — proposals only become canonical
--    after Cowork commits them to main.
--
-- 2. A scheduled task (or manual Cowork action) polls
--    context_proposals_pending each morning, presents to Royce, and
--    on accept: writes the file, commits, pushes; updates the row
--    with status='merged' + github_commit_sha.
--
-- 3. current_sha is an optimistic-lock check — if the file has moved
--    since the proposal was made, surface a conflict for human review
--    instead of clobbering.
-- ============================================================

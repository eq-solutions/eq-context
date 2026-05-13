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
  metadata jsonb not null default '{}'::jsonb
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

-- Anyone can propose
drop policy if exists "anyone can propose" on context_proposals;
create policy "anyone can propose"
  on context_proposals
  for insert
  with check (true);

-- Proposer can read their own (by session_id match)
drop policy if exists "proposer can read own" on context_proposals;
create policy "proposer can read own"
  on context_proposals
  for select
  using (
    session_id is not null
    and session_id = current_setting('request.jwt.claims', true)::jsonb->>'session_id'
  );

-- Service role bypasses RLS automatically; no policy needed.

-- ============================================================
-- Convenience view: pending queue sorted oldest-first
-- ============================================================
create or replace view context_proposals_pending as
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

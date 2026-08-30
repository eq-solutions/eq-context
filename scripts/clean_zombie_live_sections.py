#!/usr/bin/env python3
"""Remove zombie content from a live eq/pending/<repo>.md file, using its
matching eq/pending-archive.md entries as proof of what was already safely
recorded.

Why this exists (2026-08-30): the same pending-rotate.yml bug that caused
duplicate archive copies (see dedupe_pending_archive.py) also means the live
per-repo files were never actually trimmed -- rotate_pending.py correctly
computed each night's removal and it correctly landed in the archive, but
the corresponding removal from the live file never got committed. Unlike
the archive (pure duplication, safe to collapse), the live file needs a
different treatment: a section can be a WHOLE zombie (fully done, a matching
archive entry already exists, the whole section should simply not be here)
or a MIXED zombie (still has genuine open work, but some of its done items
were already successfully archived and should no longer also be sitting
here).

This does NOT decide what's "done" -- rotate_pending.py already decided
that, correctly, every night; the proof is that the exact section title and
exact done-item text already exists in the archive. This script only
replays the removal half that never committed. A done item with no matching
archive entry is left completely alone -- it hasn't been through a
successful rotation attempt yet, and this script doesn't pre-empt
rotate_pending.py's own (now-fixed) job.

Safety model:
- A live section's dedup KEY is its header text (live sections never carry
  a "(rotated ...)" stamp themselves -- only archive copies do).
- For every archive section whose key matches, collect every "- [x] ..."
  bullet BLOCK (the checkbox line plus any indented continuation lines) it
  contains, verbatim.
- In the live section, any done-item block whose exact text (all lines,
  including continuations) appears in that collected set is a confirmed
  zombie -- remove it.
- Any done-item block NOT found in the archive is left untouched.
- A section left with zero open/in-progress/done items after zombie removal
  is dropped entirely (a true whole-zombie). A section with open or
  in-progress items remaining keeps its header/intro/open/in-progress
  content exactly, with only the confirmed-zombie done blocks removed.
- Hard conservation asserts, same discipline as rotate_pending.py and
  dedupe_pending_archive.py: every open/in-progress line survives
  byte-identical; every removed done-block's text existed in the archive
  before removal; every done-block NOT removed either wasn't in the archive
  or is preserved byte-identical.

Run:  python scripts/clean_zombie_live_sections.py <live-path> [--dry-run]
      <live-path> is repo-root relative, e.g. eq/pending/eq-shell.md
      Archive path is always eq/pending-archive.md (repo-root relative).
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_PATH = ROOT / "eq" / "pending-archive.md"

ROTATED_RE = re.compile(r"\s*\(rotated \d{4}-\d{2}-\d{2}[^)]*\)\s*$")
OPEN_RE = re.compile(r"^- \[ \]")
PARTIAL_RE = re.compile(r"^- \[~\]")
DONE_RE = re.compile(r"^- \[[xX]\]")
CONT_RE = re.compile(r"^\s+\S")


def split_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[: i + 1], lines[i + 1:]
    return [], lines


def split_sections(body):
    preamble, sections, current = [], [], None
    for line in body:
        if line.startswith("## "):
            if current is not None:
                sections.append(current)
            current = [line]
        elif current is None:
            preamble.append(line)
        else:
            current.append(line)
    if current is not None:
        sections.append(current)
    return preamble, sections


def key(header):
    return ROTATED_RE.sub("", header).strip()


def bullet_blocks(section):
    """Yield (start, end_exclusive, kind) -- kind in 'open','partial','done'."""
    i = 0
    while i < len(section):
        line = section[i]
        is_open = bool(OPEN_RE.match(line))
        is_partial = bool(PARTIAL_RE.match(line))
        is_done = bool(DONE_RE.match(line))
        if not (is_open or is_partial or is_done):
            i += 1
            continue
        j = i + 1
        while j < len(section) and CONT_RE.match(section[j]):
            j += 1
        kind = "done" if is_done else ("partial" if is_partial else "open")
        yield i, j, kind
        i = j


def build_archive_index(archive_lines):
    """key -> set of verbatim done-block texts (each block's lines joined
    with '\\n') across every archive section sharing that key."""
    _, body = split_frontmatter(archive_lines)
    _, sections = split_sections(body)
    index = {}
    for sec in sections:
        k = key(sec[0])
        blocks = index.setdefault(k, set())
        for s, e, kind in bullet_blocks(sec):
            if kind == "done":
                blocks.add("\n".join(sec[s:e]))
    return index


def clean_text(live_text, archive_text):
    """Pure cleanup of one live file's text against the archive index.

    Returns (new_text_or_None, report). new_text is None when nothing
    changed.
    """
    archive_index = build_archive_index(archive_text.split("\n"))

    lines = live_text.split("\n")
    frontmatter, body = split_frontmatter(lines)
    preamble, sections = split_sections(body)

    open_before = [l for sec in sections for s, e, k in bullet_blocks(sec)
                   if k in ("open", "partial") for l in sec[s:e]]
    # Counts BLOCKS (one per "- [x]" marker line), matching
    # zombie_blocks_removed's own unit -- not every line inside a block,
    # which would over-count any done item with continuation lines.
    done_before = sum(1 for sec in sections for _, _, k in bullet_blocks(sec)
                       if k == "done")

    kept_sections = []
    whole_zombies_dropped = 0
    zombie_blocks_removed = 0
    sections_touched = 0

    for sec in sections:
        k = key(sec[0])
        zombie_texts = archive_index.get(k)
        if not zombie_texts:
            kept_sections.append(sec)
            continue

        blocks = list(bullet_blocks(sec))
        has_open_or_partial = any(kind in ("open", "partial") for _, _, kind in blocks)

        drop_idx = set()
        removed_here = 0
        for s, e, kind in blocks:
            if kind != "done":
                continue
            text = "\n".join(sec[s:e])
            if text in zombie_texts:
                drop_idx.update(range(s, e))
                removed_here += 1

        if removed_here == 0:
            kept_sections.append(sec)
            continue

        sections_touched += 1
        zombie_blocks_removed += removed_here

        if not has_open_or_partial and removed_here == sum(1 for _, _, kd in blocks if kd == "done"):
            # every done block in this section was a confirmed zombie, and
            # there was no open/partial work -- the whole section goes.
            whole_zombies_dropped += 1
            continue

        new_sec = [l for i, l in enumerate(sec) if i not in drop_idx]
        kept_sections.append(new_sec)

    new_body = list(preamble)
    for sec in kept_sections:
        new_body.extend(sec)
    new_text = "\n".join(frontmatter + new_body)
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    if not new_text.endswith("\n"):
        new_text += "\n"

    report = {
        "sections_total": len(sections),
        "sections_touched": sections_touched,
        "whole_zombies_dropped": whole_zombies_dropped,
        "zombie_blocks_removed": zombie_blocks_removed,
        "done_before": done_before,
    }

    if sections_touched == 0:
        return None, report

    # ── conservation invariants ──
    open_after = [l for sec in kept_sections for s, e, k2 in bullet_blocks(sec)
                  if k2 in ("open", "partial") for l in sec[s:e]]
    assert open_after == open_before, (
        "clean-zombie: open/partial items changed -- aborting, nothing written "
        f"({len(open_before)} -> {len(open_after)})"
    )
    done_after = sum(1 for sec in kept_sections for _, _, k2 in bullet_blocks(sec)
                      if k2 == "done")
    assert done_after + zombie_blocks_removed == done_before, (
        f"clean-zombie: done-item conservation failed "
        f"({done_before} before != {done_after} kept + {zombie_blocks_removed} removed)"
    )

    return new_text, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("live_path")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    live_path = ROOT / args.live_path
    live_text = live_path.read_text(encoding="utf-8")
    archive_text = ARCHIVE_PATH.read_text(encoding="utf-8")

    new_text, report = clean_text(live_text, archive_text)

    print(f"--- Clean zombies: {args.live_path} ---")
    print(f"  {report['sections_total']} live sections, {report['sections_touched']} touched")
    print(f"  {report['whole_zombies_dropped']} whole zombie section(s) dropped")
    print(f"  {report['zombie_blocks_removed']} confirmed-zombie done-item block(s) removed")
    print(f"  done-item lines before: {report['done_before']}")

    if new_text is None:
        print("\n  nothing to do")
        return 0

    if not args.dry_run:
        assert "\x00" not in new_text, "NUL byte in output -- aborting"
        live_path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"\n  wrote {args.live_path}")
    else:
        print("\n  (dry run — nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

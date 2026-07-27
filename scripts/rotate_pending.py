#!/usr/bin/env python3
"""Rotate done items out of pending.md files — per-item, not per-session.

Why this exists (2026-07-27 backlog analysis): eq/pending.md hit 478 open +
163 done-unrotated items because the only rotation the file ever had was a
one-off manual chore (commit 121cc5b, 2026-07-24) whose rule — "a session
moves to the archive only when it has ZERO open items left" — let a single
trailing 'Royce to confirm X' line trap a whole finished session's write-up
in the live doc forever. 19 mixed sessions were holding 84 done items
hostage on that rule alone.

New rule, enforced here nightly (pending-rotate.yml):
- A section whose checkbox items are ALL done moves to the archive whole,
  narrative intact (the old rule, now automated).
- A MIXED section keeps its header, intro, and open items in the live file;
  its done items move to the archive under a copy of the section header.
- Sections newer than --grace-days (default 3, dated from the (YYYY-MM-DD)
  suffix on the section header) are left alone, so follow-on sessions keep
  same-week narrative context. Undated sections count as old.

Conservation invariants (hard-asserted, the run fails rather than lose a line):
- every open item present before is present, byte-identical, after;
- done items removed from live == done items appended to archive;
- a NUL scan on every written file (the F2/F6 silent-corruption class).

Run: python scripts/rotate_pending.py [--dry-run] [--grace-days N]
"""
import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIRS = [
    ("eq/pending.md", "eq/pending-archive.md", "EQ"),
    ("sks/pending.md", "sks/pending-archive.md", "SKS"),
    ("ops/pending.md", "ops/pending-archive.md", "OPS"),
]

OPEN_RE = re.compile(r"^- \[ \]")
DONE_RE = re.compile(r"^- \[[xX]\]")
CONT_RE = re.compile(r"^\s+\S")  # indented continuation line of a bullet
HEADER_DATE_RE = re.compile(r"\((?:[^)]*\b)?(\d{4}-\d{2}-\d{2})\)")

ARCHIVE_FRONTMATTER = """---
title: {tier} Tier — Pending Actions Archive
owner: Royce Milmlow
last_updated: {today}
scope: Done items rotated out of {live} nightly by scripts/rotate_pending.py to keep the live doc scannable. Nothing here is actionable — pure historical record (also covered in changelogs and sessions/*.md). Append-only, in rotation order.
read_priority: reference
status: archived
---

# {tier} Tier — Pending (Archive)

Done items and fully-closed session write-ups rotated out of `{live}`.
If you're looking for something to action, it's not here — check `{live}`.
A "(rotated YYYY-MM-DD ...)" note on a section header means only that
section's done items live here; its open items stayed in `{live}`.

---
"""


def split_frontmatter(lines):
    """Return (frontmatter_lines, body_lines). Frontmatter may be absent."""
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[: i + 1], lines[i + 1:]
    return [], lines


def split_sections(body):
    """Split body lines into (preamble, [section_line_lists]).

    A section runs from its '## ' heading to just before the next '## '
    heading; '###' subheadings and '---' separators stay inside the section
    they follow.
    """
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


def bullet_blocks(section):
    """Yield (start, end_exclusive, kind) for checkbox bullets in a section.

    kind is 'open' or 'done'. A bullet block is its '- [ ]'/'- [x]' line plus
    any immediately-following indented continuation lines.
    """
    i = 0
    while i < len(section):
        line = section[i]
        kind = "open" if OPEN_RE.match(line) else "done" if DONE_RE.match(line) else None
        if kind is None:
            i += 1
            continue
        j = i + 1
        while j < len(section) and CONT_RE.match(section[j]):
            j += 1
        yield i, j, kind
        i = j


def section_date(section):
    """Most recent date on the section header, or None if undated."""
    dates = []
    for m in re.finditer(r"(\d{4}-\d{2}-\d{2})", section[0]):
        try:
            dates.append(datetime.strptime(m.group(1), "%Y-%m-%d").date())
        except ValueError:
            pass
    return max(dates) if dates else None


def strip_trailing_separators(section):
    """Drop trailing blank lines and '---' rules so a moved section can be
    re-terminated cleanly in the archive."""
    out = list(section)
    while out and out[-1].strip() in ("", "---"):
        out.pop()
    return out


def rotate_text(text, tier, live_name, grace_days, today):
    """Pure rotation of one file's text.

    Returns (new_live_text_or_None, archive_append_text, summary). new_live is
    None when nothing moved.
    """
    lines = text.split("\n")
    frontmatter, body = split_frontmatter(lines)
    preamble, sections = split_sections(body)

    open_before = [l for l in lines if OPEN_RE.match(l)]
    done_before = sum(1 for l in lines if DONE_RE.match(l))

    cutoff = today - timedelta(days=grace_days)
    kept_sections, archived_chunks = [], []
    moved_done = 0
    full_moves = partial_moves = 0

    for section in sections:
        blocks = list(bullet_blocks(section))
        has_open = any(k == "open" for _, _, k in blocks)
        has_done = any(k == "done" for _, _, k in blocks)
        sec_date = section_date(section)
        in_grace = sec_date is not None and sec_date > cutoff

        if not has_done or in_grace:
            kept_sections.append(section)
            continue

        if not has_open:
            # Fully closed — move the whole section, narrative intact.
            chunk = strip_trailing_separators(section)
            chunk[0] = chunk[0].rstrip() + f" (rotated {today})"
            archived_chunks.append(chunk)
            moved_done += sum(1 for l in chunk if DONE_RE.match(l))
            full_moves += 1
            continue

        # Mixed — keep header/intro/open items live, archive the done blocks.
        done_ranges = [(s, e) for s, e, k in blocks if k == "done"]
        moved = []
        for s, e in done_ranges:
            moved.extend(section[s:e])
        drop = {i for s, e in done_ranges for i in range(s, e)}
        kept = [l for i, l in enumerate(section) if i not in drop]
        kept_sections.append(kept)
        header = section[0].rstrip() + (
            f" (rotated {today} — open items remain in {live_name})"
        )
        archived_chunks.append([header, ""] + moved)
        moved_done += sum(1 for l in moved if DONE_RE.match(l))
        partial_moves += 1

    summary = {
        "tier": tier,
        "open": len(open_before),
        "done_before": done_before,
        "moved": moved_done,
        "full": full_moves,
        "partial": partial_moves,
    }
    if moved_done == 0:
        return None, "", summary

    # ── rebuild live file ──
    new_fm = [
        re.sub(r"^last_updated:.*$", f"last_updated: {today}", l)
        for l in frontmatter
    ]
    new_body = list(preamble)
    for sec in kept_sections:
        new_body.extend(sec)
    new_live = "\n".join(new_fm + new_body)
    # Collapse the 3+ consecutive blank lines removed blocks leave behind.
    new_live = re.sub(r"\n{4,}", "\n\n\n", new_live)
    if not new_live.endswith("\n"):
        new_live += "\n"

    # ── build archive append ──
    append = []
    for chunk in archived_chunks:
        append.extend(chunk)
        append.extend(["", "---", ""])
    append_text = "\n".join(append)

    # ── conservation invariants — fail loudly rather than lose a line ──
    open_after = [l for l in new_live.split("\n") if OPEN_RE.match(l)]
    assert open_after == open_before, (
        f"{tier}: open items changed during rotation "
        f"({len(open_before)} -> {len(open_after)}) — aborting, nothing written"
    )
    done_after_live = sum(1 for l in new_live.split("\n") if DONE_RE.match(l))
    assert done_after_live + moved_done == done_before, (
        f"{tier}: done-item conservation failed "
        f"({done_before} before != {done_after_live} live + {moved_done} moved)"
    )
    done_in_append = sum(1 for l in append_text.split("\n") if DONE_RE.match(l))
    assert done_in_append == moved_done, (
        f"{tier}: archive append holds {done_in_append} done items, expected {moved_done}"
    )
    return new_live, append_text, summary


def rotate_file(live_path, archive_path, tier, grace_days, today, dry_run):
    """Rotate one pending/archive pair on disk. Returns a summary dict."""
    text = live_path.read_text(encoding="utf-8")
    live_rel = f"{live_path.parent.name}/{live_path.name}"
    new_live, append_text, summary = rotate_text(
        text, tier, live_path.name, grace_days, today)
    if new_live is None:
        return summary

    if archive_path.exists():
        archive_text = archive_path.read_text(encoding="utf-8")
        archive_text = re.sub(
            r"^last_updated:.*$", f"last_updated: {today}",
            archive_text, count=1, flags=re.M,
        )
        if not archive_text.endswith("\n"):
            archive_text += "\n"
        new_archive = archive_text + "\n" + append_text
    else:
        new_archive = (
            ARCHIVE_FRONTMATTER.format(tier=tier, today=today, live=live_rel)
            + "\n" + append_text
        )

    for name, content in ((live_path.name, new_live), (archive_path.name, new_archive)):
        assert "\x00" not in content, f"{tier}: NUL byte in {name} — aborting"

    if not dry_run:
        live_path.write_text(new_live, encoding="utf-8", newline="\n")
        archive_path.write_text(new_archive, encoding="utf-8", newline="\n")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--grace-days", type=int, default=3,
                    help="leave sections dated within the last N days alone (default 3)")
    args = ap.parse_args(argv)
    today = date.today()

    any_moved = False
    for live_rel, archive_rel, tier in PAIRS:
        live_path = ROOT / live_rel
        if not live_path.exists():
            print(f"{tier}: {live_rel} missing — skipped")
            continue
        s = rotate_file(live_path, ROOT / archive_rel, tier, args.grace_days,
                        today, args.dry_run)
        verb = "would move" if args.dry_run else "moved"
        print(f"{tier}: {s['open']} open kept · {verb} {s['moved']}/{s['done_before']} done "
              f"({s['full']} whole sections, {s['partial']} mixed)")
        any_moved = any_moved or s["moved"] > 0
    if not any_moved:
        print("Nothing to rotate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

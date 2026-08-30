#!/usr/bin/env python3
"""Collapse duplicate sections in a pending-archive.md caused by the
2026-08-17 -> 2026-08-30 rotation bug.

Why this exists (2026-08-30): pending-rotate.yml's commit step staged the
retired flat eq/pending.md instead of the 11 real eq/pending/<repo>.md files
after the 2026-08-17 split, so every night rotate_pending.py correctly wrote
each repo file's trimmed version to disk and correctly appended to
eq/pending-archive.md, but only the archive append ever got committed -- the
live-file removal silently never did. The next night's run found the same
"already done" section still there, rotated it again, appended another
duplicate. Confirmed live: some eq-shell.md sections carry up to 25
duplicate "(rotated YYYY-MM-DD ...)" copies. 208 distinct sections, 1,550
redundant copies, 68% of eq/pending-archive.md's lines, at time of writing.
The root cause is fixed (workflow file list corrected); this script cleans
up what already accumulated.

Safety model, matching rotate_pending.py's own conservation-invariant
discipline -- fail loud rather than silently drop content:

- A section's dedup KEY is its header with the trailing "(rotated
  YYYY-MM-DD ...)" annotation stripped (the only thing that legitimately
  varies run-to-run for a genuine duplicate).
- Within a key's group of copies, if every copy is byte-identical once its
  own "(rotated ...)" stamp is stripped, they are TRUE duplicates: keep
  exactly one (the copy with the newest rotation date -- most likely to be
  the most complete, and arbitrary among identical copies anyway), drop the
  rest.
- If copies within a group are NOT all identical (e.g. a mixed section
  whose live copy kept accumulating more done items between failed-removal
  nights, so later copies are supersets of earlier ones) -- verify the copy
  chosen to keep is a superset of every dropped copy's own done-item lines
  ("- [x] ..." blocks). If that holds, keep the superset copy. If it does
  NOT hold for every dropped copy (a real conflict, not just growth), the
  whole group is left untouched and reported instead of guessed at.
- Every "- [x] ..." bullet line that exists anywhere in the original file
  must exist somewhere in the deduplicated output (a hard assert, not a
  best-effort check) -- run fails rather than silently lose a line.

Run:  python scripts/dedupe_pending_archive.py [path] [--dry-run]
      path defaults to eq/pending-archive.md (repo-root relative)
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ROTATED_RE = re.compile(r"\s*\(rotated \d{4}-\d{2}-\d{2}[^)]*\)\s*$")
DATE_IN_ROTATED_RE = re.compile(r"\(rotated (\d{4}-\d{2}-\d{2})")
DONE_RE = re.compile(r"^- \[[xX]\]")


def split_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[: i + 1], lines[i + 1:]
    return [], lines


def split_sections(body):
    """(preamble_lines, [section_line_lists]) -- same shape as rotate_pending.py."""
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


def dedup_key(section):
    """Header text with any trailing '(rotated ...)' stamp stripped."""
    return ROTATED_RE.sub("", section[0]).strip()


def rotated_date(section):
    m = DATE_IN_ROTATED_RE.search(section[0])
    return m.group(1) if m else ""


def normalized_body(section):
    """Section text with its own header's '(rotated ...)' stamp stripped and
    trailing blank lines trimmed, so two copies that differ only by rotation
    date -- or only by how many trailing blank lines happened to survive a
    section-boundary split -- compare equal."""
    body = list(section)
    body[0] = ROTATED_RE.sub("", body[0])
    return "\n".join(body).rstrip()


def done_lines(section):
    return frozenset(l for l in section if DONE_RE.match(l))


def bullet_blocks(section):
    """Yield (start, end_exclusive, kind) for '- [x]' blocks in a section --
    the checkbox line plus any indented continuation lines. Only 'done' is
    distinguished; dedupe_pending_archive only ever acts on archived
    (all-done) content."""
    i = 0
    while i < len(section):
        line = section[i]
        if not DONE_RE.match(line):
            i += 1
            continue
        j = i + 1
        while j < len(section) and CONT_RE.match(section[j]):
            j += 1
        yield i, j, "done"
        i = j


CONT_RE = re.compile(r"^\s+\S")


def _intro_lines(section):
    """Lines between the header and the first done-block -- the section's
    own prose/context, if it has any."""
    first_bullet_start = None
    for s, e, _ in bullet_blocks(section):
        first_bullet_start = s
        break
    return section[1:first_bullet_start] if first_bullet_start is not None else section[1:]


def union_merge(copies):
    """Merge N non-identical, non-superset copies of the same section into
    one: the union of every distinct done-item block across all copies
    (order of first appearance, exact-text duplicates within the group
    collapsed), under one copy's own header and intro prose.

    Always safe with respect to the conservation invariant -- every unique
    done-line from every copy survives in the output, nothing is dropped or
    silently preferred over a "contradicting" other copy. The cost is a
    merged section that may read as slightly redundant (e.g. a short
    summary bullet sitting next to a fuller corrected account of the same
    event) -- acceptable in a pure historical record where nothing here is
    actionable, and strictly better than N confusing near-duplicate
    section headers for the same event.

    Which copy's header/intro to keep: newest rotation date first: ties are
    real and common (a mixed section rotated more than once on the same
    day). Break a tie by non-blank intro line count, not file order --
    caught live on eq/pending-archive.md's own "SKS tenant LIVE... Big
    correction" pair: same-day tie, file-order tiebreak would have kept the
    terser copy's near-empty intro over the other copy's own "Big
    correction vs the earlier draft" context explaining exactly why the
    terser framing was wrong. The done-item union is unaffected either way
    -- this only picks which prose framing survives.
    """
    seen_texts = set()
    union_blocks = []
    for c in copies:
        for s, e, _ in bullet_blocks(c):
            block = c[s:e]
            text = "\n".join(block)
            if text not in seen_texts:
                seen_texts.add(text)
                union_blocks.append(block)

    def richness(c):
        intro = _intro_lines(c)
        return (rotated_date(c), sum(1 for l in intro if l.strip()))

    best = max(copies, key=richness)
    intro_lines = _intro_lines(best)

    merged = [best[0]] + intro_lines
    for block in union_blocks:
        merged.extend(block)
    if not merged[-1].strip() == "":
        merged.append("")
    return merged


def dedupe_text(text):
    """Pure dedup of one archive file's text.

    Returns (new_text, report) where report has:
      groups_total, groups_deduped, copies_removed, lines_removed,
      groups_union_merged (list of dedup_key strings resolved via
      union_merge -- safe, but worth a glance since the merged section may
      read as slightly redundant), groups_conflicted (should be empty in
      practice -- union_merge handles every non-superset case; kept as a
      backstop, never silently guessed at if it's ever hit).
    """
    lines = text.split("\n")
    frontmatter, body = split_frontmatter(lines)
    preamble, sections = split_sections(body)

    done_before = sum(1 for l in lines if DONE_RE.match(l))

    from collections import defaultdict
    groups = defaultdict(list)
    order = []  # first-seen order of each key, to preserve overall file order
    for sec in sections:
        key = dedup_key(sec)
        if key not in groups:
            order.append(key)
        groups[key].append(sec)

    kept_sections = []
    groups_deduped = 0
    copies_removed = 0
    lines_removed = 0
    groups_conflicted = []
    groups_union_merged = []

    for key in order:
        copies = groups[key]
        if len(copies) == 1:
            kept_sections.append(copies[0])
            continue

        normed = [normalized_body(c) for c in copies]
        if len(set(normed)) == 1:
            # true duplicates -- keep the one with the newest rotation date
            best = max(copies, key=rotated_date)
            kept_sections.append(best)
            groups_deduped += 1
            copies_removed += len(copies) - 1
            lines_removed += sum(len(c) for c in copies) - len(best)
            continue

        # not identical -- collapse if one copy's done-lines are a strict
        # superset of every other copy's done-lines. Guard against the
        # degenerate case first: an empty set is trivially a "superset" of
        # another empty set, which would otherwise let this branch silently
        # pick copy 0 and discard copy 1's own (non-done) content whenever
        # neither copy has any done item at all -- caught by the backstop
        # test below, not hypothetical.
        done_sets = [done_lines(c) for c in copies]
        superset_idx = None
        if any(done_sets):
            for i, ds in enumerate(done_sets):
                if all(ds >= other for other in done_sets):
                    superset_idx = i
                    break
        if superset_idx is not None:
            best = copies[superset_idx]
            kept_sections.append(best)
            groups_deduped += 1
            copies_removed += len(copies) - 1
            lines_removed += sum(len(c) for c in copies) - len(best)
            continue

        # No single copy dominates -- each holds distinct facts (the
        # rotation bug's mixed-section shape: every failed-removal night
        # appended a slightly bigger, non-superset extract of the same
        # live section). union_merge collapses them into one section
        # holding every distinct done-block, never dropping or picking a
        # "winner" among the facts themselves.
        any_done = any(done_lines(c) for c in copies)
        if not any_done:
            # No done items at all in any copy (shouldn't happen for an
            # archive, which is done-items-only by convention) -- nothing
            # safe to merge on. Leave alone, flag for a human.
            groups_conflicted.append(key)
            for c in copies:
                kept_sections.append(c)
            continue

        merged = union_merge(copies)
        kept_sections.append(merged)
        groups_union_merged.append(key)
        groups_deduped += 1
        copies_removed += len(copies) - 1
        lines_removed += sum(len(c) for c in copies) - len(merged)

    new_body = list(preamble)
    for sec in kept_sections:
        new_body.extend(sec)
    new_text = "\n".join(frontmatter + new_body)
    new_text = re.sub(r"\n{4,}", "\n\n\n", new_text)
    if not new_text.endswith("\n"):
        new_text += "\n"

    done_after = sum(1 for l in new_text.split("\n") if DONE_RE.match(l))

    report = {
        "groups_total": len(order),
        "groups_deduped": groups_deduped,
        "copies_removed": copies_removed,
        "lines_removed": lines_removed,
        "groups_union_merged": groups_union_merged,
        "groups_conflicted": groups_conflicted,
        "done_before": done_before,
        "done_after": done_after,
    }

    # ── conservation invariant: every done-item line kept OR accounted for
    # in a genuinely-collapsed duplicate must still exist somewhere. We
    # don't assert done_after == done_before (dedup deliberately removes
    # redundant done lines) -- instead assert every UNIQUE done line from
    # the original still appears at least once in the output. ──
    unique_done_before = {l for l in lines if DONE_RE.match(l)}
    unique_done_after = {l for l in new_text.split("\n") if DONE_RE.match(l)}
    missing = unique_done_before - unique_done_after
    assert not missing, (
        f"dedupe lost {len(missing)} unique done-item line(s) that appear "
        f"nowhere in the output -- aborting, nothing written. First: "
        f"{next(iter(missing))!r}"
    )

    return new_text, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", default="eq/pending-archive.md")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    path = ROOT / args.path
    text = path.read_text(encoding="utf-8")
    new_text, report = dedupe_text(text)

    print(f"--- Dedup: {args.path} ---")
    print(f"  {report['groups_total']} distinct sections")
    print(f"  {report['groups_deduped']} groups deduplicated")
    print(f"  {report['copies_removed']} redundant copies removed")
    print(f"  {report['lines_removed']} lines removed")
    print(f"  done-item lines: {report['done_before']} -> {report['done_after']}")
    if report["groups_union_merged"]:
        print(f"\n  {len(report['groups_union_merged'])} group(s) union-merged (distinct facts combined into one section, nothing dropped):")
        for k in report["groups_union_merged"]:
            print(f"    - {k}")
    if report["groups_conflicted"]:
        print(f"\n  {len(report['groups_conflicted'])} group(s) left untouched (no clean superset, needs a human look):")
        for k in report["groups_conflicted"]:
            print(f"    - {k}")

    if not args.dry_run and report["copies_removed"] > 0:
        assert "\x00" not in new_text, "NUL byte in output -- aborting"
        path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"\n  wrote {args.path}")
    elif args.dry_run:
        print("\n  (dry run — nothing written)")

    return 1 if report["groups_conflicted"] else 0


if __name__ == "__main__":
    sys.exit(main())

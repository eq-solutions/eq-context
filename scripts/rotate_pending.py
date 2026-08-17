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

2026-08-01 addition (backlog dive with Royce): even with the above, eq/
pending.md had grown to 368KB / 2966 lines. Root cause: a section with real
build work fully shipped but ONE trailing "Royce to click through live"
line stayed live forever, because that line is genuinely still open — the
old rule has no way to tell "still needs building" apart from "just needs
your own sign-in to confirm". 15 sections were being held live by exactly
one such straggler. Fix: a plain "- [ ]" bullet whose text matches
VERIFY_RE (Royce to click-through/confirm/spot-check/eyeball live, etc.) is
now classified 'verify', not 'open'. A section with zero genuine 'open'
bullets left now rotates out whole even if it still has verify bullets —
the done items go to the archive as before, and the verify items move to a
new per-tier verify-queue.md instead of pinning the write-up in the live
file. Mixed sections (real open work still there too) are untouched — the
verify line stays put with the rest of that section's unfinished work; this
only fires once nothing is left to build.

Conservation invariants (hard-asserted, the run fails rather than lose a line):
- every genuinely-open item present before is present, byte-identical, after;
- done items removed from live == done items appended to archive;
- verify items removed from live == verify items appended to the queue;
- a NUL scan on every written file (the F2/F6 silent-corruption class).

Run: python scripts/rotate_pending.py [--dry-run] [--grace-days N]
"""
import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# eq/pending.md split 2026-08-17 into one file per repo (eq/pending/<repo>.md)
# — see eq/pending.md's own frontmatter for why. EQ's "live" side is now a
# LIST of files, all rotating into the same shared eq/pending-archive.md and
# eq/verify-queue.md (the split only separates open engineering backlog by
# repo; done/verify items stay tier-unified, matching how "Waiting on you" in
# digest.md has always displayed EQ/SKS/OPS as one combined list rather than
# splitting the queue itself by repo too). SKS/OPS are unaffected — still
# single-file, wrapped in a one-element list so main()'s loop shape is the
# same for every tier.
EQ_LIVE_FILES = [
    "eq/pending/eq-shell.md",
    "eq/pending/eq-cards.md",
    "eq/pending/eq-field.md",
    "eq/pending/eq-solves-service.md",
    "eq/pending/eq-solves-intake.md",
    "eq/pending/eq-design-tokens.md",
    "eq/pending/eq-ui.md",
    "eq/pending/eq-receipts.md",
    "eq/pending/eq-context.md",
    "eq/pending/cross-repo.md",
    "eq/pending/sks.md",
]

PAIRS = [
    (EQ_LIVE_FILES, "eq/pending-archive.md", "eq/verify-queue.md", "EQ"),
    (["sks/pending.md"], "sks/pending-archive.md", "sks/verify-queue.md", "SKS"),
    (["ops/pending.md"], "ops/pending-archive.md", "ops/verify-queue.md", "OPS"),
]

OPEN_RE = re.compile(r"^- \[ \]")
PARTIAL_RE = re.compile(r"^- \[~\]")  # in-progress marker, e.g. "- [~] partially applied"
DONE_RE = re.compile(r"^- \[[xX]\]")
CONT_RE = re.compile(r"^\s+\S")  # indented continuation line of a bullet
HEADER_DATE_RE = re.compile(r"\((?:[^)]*\b)?(\d{4}-\d{2}-\d{2})\)")

# A '- [ ]' block whose only remaining blocker is Royce's own live sign-in/
# click-through, not more building. Conservative on purpose — a false
# positive would wrongly rotate a section with real work still open, so
# every phrase here is one actually used across eq/sks/ops pending.md for
# exactly this class of item (checked against the live files 2026-08-01,
# not guessed).
#
# Widened 2026-08-15 — a residue-sample review found 16 items in this exact
# category the original pattern missed, all real: "Not click-tested on a
# real phone", "Live click-through not done", "Live click-test still not
# done anywhere across this whole thread", "Royce's own click-through".
# The original only matched "Royce to click-through" (that specific prefix)
# or "click through live/production" (space, not hyphen) — real usage
# varies the grammar ("Royce's click-through" vs "Royce to click-through")
# and compounds "click" with "test" as often as "through" ("not click-
# tested", "click-test"). Same discipline as the original: every new
# alternative below is a phrase confirmed present in eq/pending.md, not a
# generic "confirm"/"verify" catch-all — a loose "confirm" match was tried
# first and false-positived on "EQ Field/SKS Labour... confirmed live,
# corrected a stale memory", an unstarted planning item with zero build
# done, the exact shape this regex must never rotate.
VERIFY_RE = re.compile(
    r"Royce to (click[\s-]through|confirm|spot-check|eyeball)"
    r"|Royce'?s?( own)? click[\s-]through"
    r"|click[\s-]tested live"
    r"|click(?:ed)? through (live|production)"
    r"|(no|not) (yet )?click[\s-]?(tested|through|test)"
    r"|live click[\s-](through|test)"
    r"|no test login"
    r"|needs? sign-?in"
    r"|off-limits for Claude"
    r"|Claude can.?t (do|perform) this",
    re.I,
)

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

QUEUE_FRONTMATTER = """---
title: {tier} Tier — Verify Queue
owner: Royce Milmlow
last_updated: {today}
scope: Items whose only remaining blocker is your own live sign-in/click-through — the underlying work is already built, merged, and (unless the line itself says otherwise) live. Moved here from {live} by scripts/rotate_pending.py once a session's real build work is fully done, so a stale "click through to confirm" line no longer pins a whole finished write-up in the live pending doc.
read_priority: high
status: live
---

# {tier} Tier — Verify Queue

Nothing left to build on anything below — every line just needs you to
actually open the app and check it. Delete the line once you've confirmed
it. If something's actually broken, that's real signal — flag it back as
a bug rather than just deleting the line.

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

    kind is 'open', 'verify', or 'done'. A bullet block is its '- [ ]'/
    '- [x]' line plus any immediately-following indented continuation
    lines.

    '- [~]' (in progress / partially applied) always counts as 'open' — it
    must never be archived or queued alongside done/verify items, and its
    presence must stop a section from being treated as fully closed.
    Missing this was a real bug (found 2026-07-27): a section holding only
    a '[~]' item plus already-done items was wrongly whole-section-archived
    as "fully done".

    A plain '- [ ]' block is reclassified 'verify' when its text matches
    VERIFY_RE — the only thing left blocking it is Royce's own live
    click-through, not more building. This lets a section whose real build
    work is fully done rotate out of the live file even while a "confirm
    this live" line is still open; the line itself moves to
    verify-queue.md instead of vanishing (see rotate_text). Added
    2026-08-01 after a backlog review found 15 sections pinned live by
    exactly one such straggler line.
    """
    i = 0
    while i < len(section):
        line = section[i]
        is_partial = bool(PARTIAL_RE.match(line))
        is_open = bool(OPEN_RE.match(line))
        is_done = bool(DONE_RE.match(line))
        if not (is_partial or is_open or is_done):
            i += 1
            continue
        j = i + 1
        while j < len(section) and CONT_RE.match(section[j]):
            j += 1
        if is_done:
            kind = "done"
        elif is_partial:
            kind = "open"
        elif VERIFY_RE.search("\n".join(section[i:j])):
            kind = "verify"
        else:
            kind = "open"
        yield i, j, kind
        i = j


def classify_lines_globally(lines):
    """(open_lines, verify_lines) — every bullet-block line in the two
    non-done categories, flattened, in document order.

    Used only to build rotate_text's before/after conservation invariants.
    Section boundaries don't affect bullet_blocks (a '## ' header or blank
    line always ends a block, same as any other non-continuation line), so
    running it on a whole file is equivalent to summing it per-section.
    """
    open_lines, verify_lines = [], []
    for s, e, k in bullet_blocks(lines):
        if k == "open":
            open_lines.extend(lines[s:e])
        elif k == "verify":
            verify_lines.extend(lines[s:e])
    return open_lines, verify_lines


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

    Returns (new_live_text_or_None, archive_append_text, summary). new_live
    is None when nothing moved. summary["queue_append"] holds any
    verify-item text to append to the tier's verify-queue.md (empty string
    when none moved this run).
    """
    lines = text.split("\n")
    frontmatter, body = split_frontmatter(lines)
    preamble, sections = split_sections(body)

    open_before, verify_before = classify_lines_globally(lines)
    done_before = sum(1 for l in lines if DONE_RE.match(l))

    cutoff = today - timedelta(days=grace_days)
    kept_sections, archived_chunks, queue_chunks = [], [], []
    moved_done = moved_verify = 0
    full_moves = partial_moves = 0

    for section in sections:
        blocks = list(bullet_blocks(section))
        has_open = any(k == "open" for _, _, k in blocks)
        has_verify = any(k == "verify" for _, _, k in blocks)
        has_done = any(k == "done" for _, _, k in blocks)
        sec_date = section_date(section)
        in_grace = sec_date is not None and sec_date > cutoff

        if (not has_done and not has_verify) or in_grace:
            kept_sections.append(section)
            continue

        if not has_open:
            # No genuine open work left — the whole section can leave the
            # live file. Done items go to the archive as before; any
            # verify (Royce-to-click-through) items go to the queue
            # instead of riding along, since they're a different kind of
            # "not done" — the build is finished, only a live confirm
            # remains.
            verify_ranges = [(s, e) for s, e, k in blocks if k == "verify"]
            verify_lines = []
            for s, e in verify_ranges:
                verify_lines.extend(section[s:e])
            drop = {i for s, e in verify_ranges for i in range(s, e)}
            chunk = [l for i, l in enumerate(section) if i not in drop]
            chunk = strip_trailing_separators(chunk)
            chunk[0] = chunk[0].rstrip() + f" (rotated {today})"
            archived_chunks.append(chunk)
            moved_done += sum(1 for l in chunk if DONE_RE.match(l))
            full_moves += 1
            if verify_lines:
                queue_chunks.append((section[0][3:].rstrip(), verify_lines))
                moved_verify += len(verify_ranges)
            continue

        # Mixed — real open work remains. Keep header/intro/open items
        # (including any verify lines — still tied to a section with
        # genuine unfinished work, so leave them where they are; a
        # smaller, safer scope than also splitting mixed sections).
        # Archive the done blocks as before.
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
        "moved_verify": moved_verify,
        "full": full_moves,
        "partial": partial_moves,
        "queue_append": "",
    }
    if moved_done == 0 and moved_verify == 0:
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

    # ── build verify-queue append ──
    queue = []
    for header_text, verify_lines in queue_chunks:
        queue.append(f"**From:** {header_text}")
        queue.append("")
        queue.extend(verify_lines)
        queue.extend(["", "---", ""])
    queue_append_text = "\n".join(queue)
    summary["queue_append"] = queue_append_text

    # ── conservation invariants — fail loudly rather than lose a line ──
    open_after, verify_after_live = classify_lines_globally(new_live.split("\n"))
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
    verify_in_queue = sum(1 for l in queue_append_text.split("\n") if OPEN_RE.match(l))
    assert len(verify_after_live) + verify_in_queue == len(verify_before), (
        f"{tier}: verify-item conservation failed "
        f"({len(verify_before)} before != {len(verify_after_live)} still live + "
        f"{verify_in_queue} moved to queue)"
    )
    assert verify_in_queue == moved_verify, (
        f"{tier}: queue append holds {verify_in_queue} verify items, expected {moved_verify}"
    )
    return new_live, append_text, summary


def rotate_file(live_path, archive_path, queue_path, tier, grace_days, today, dry_run):
    """Rotate one pending/archive/queue trio on disk. Returns a summary dict."""
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

    queue_append = summary.get("queue_append", "")
    new_queue = None
    if queue_append:
        if queue_path.exists():
            queue_text = queue_path.read_text(encoding="utf-8")
            queue_text = re.sub(
                r"^last_updated:.*$", f"last_updated: {today}",
                queue_text, count=1, flags=re.M,
            )
            if not queue_text.endswith("\n"):
                queue_text += "\n"
            new_queue = queue_text + "\n" + queue_append
        else:
            new_queue = (
                QUEUE_FRONTMATTER.format(tier=tier, today=today, live=live_rel)
                + "\n" + queue_append
            )

    to_write = [(live_path.name, new_live), (archive_path.name, new_archive)]
    if new_queue is not None:
        to_write.append((queue_path.name, new_queue))
    for name, content in to_write:
        assert "\x00" not in content, f"{tier}: NUL byte in {name} — aborting"

    if not dry_run:
        live_path.write_text(new_live, encoding="utf-8", newline="\n")
        archive_path.write_text(new_archive, encoding="utf-8", newline="\n")
        if new_queue is not None:
            queue_path.write_text(new_queue, encoding="utf-8", newline="\n")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--grace-days", type=int, default=3,
                    help="leave sections dated within the last N days alone (default 3)")
    args = ap.parse_args(argv)
    today = date.today()

    any_moved = False
    for live_rels, archive_rel, queue_rel, tier in PAIRS:
        for live_rel in live_rels:
            live_path = ROOT / live_rel
            if not live_path.exists():
                print(f"{tier}: {live_rel} missing — skipped")
                continue
            s = rotate_file(live_path, ROOT / archive_rel, ROOT / queue_rel, tier,
                            args.grace_days, today, args.dry_run)
            verb = "would move" if args.dry_run else "moved"
            print(f"{tier} ({live_rel}): {s['open']} open kept · "
                  f"{verb} {s['moved']}/{s['done_before']} done "
                  f"({s['full']} whole sections, {s['partial']} mixed) · "
                  f"{verb} {s['moved_verify']} verify item(s) to queue")
            any_moved = any_moved or s["moved"] > 0 or s["moved_verify"] > 0
    if not any_moved:
        print("Nothing to rotate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

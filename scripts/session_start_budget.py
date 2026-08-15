#!/usr/bin/env python3
"""Cap what a session pays to start.

Why (2026-08-15). CLAUDE.md section 1 step 4 mandated reading the tier
`pending.md` at every session start. eq/pending.md had grown 17 KB -> 91 -> 360
-> 491 across four months, so that one line was costing ~125,000 tokens before
the session's first question -- about 82% of everything loaded, and more than
the whole rest of the substrate combined.

Nothing caught it. Every nightly job was green: rotation ran and succeeded, the
file just grew faster than rotation could shrink it (+157 KB in the 18 days
before this was noticed, while rotate_pending.py ran every night). Growth of an
auto-loaded file is invisible to every check that looks at *correctness*.

So this measures the one thing nobody was measuring: the total cost of the read
chain CLAUDE.md actually mandates. It fails loudly when the chain gets fat, and
the failure names the file that grew.

The point is not the exact number. It is that the number has an owner and a
tripwire, because the previous arrangement -- a sweep with no ratchet -- is how
the substrate got here. See system/failures.md: a fix that is not regenerated or
ratcheted decays.

Run:  python scripts/session_start_budget.py
Gate: exits 1 when over budget. Set SESSION_BUDGET_REPORT=1 to always exit 0.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Every file CLAUDE.md section 1 step 4 tells a session to read before it does
# anything. Keep this list in step with that section -- if you add a mandated
# read there and not here, the budget silently stops covering it.
ALWAYS = [
    "CLAUDE.md",
    "suite-state.md",
    "digest.md",
    "system/TODAY.md",
    "system/punch-list.md",
]

# Worst-case tier load, counted on top of ALWAYS. Cross-tier reads two, so the
# budget is measured against the heaviest single combination rather than an
# average that no real session pays.
TIERS = {
    "EQ": ["eq/README.md"],
    "SKS": ["sks/README.md", "sks/active.md"],
    "OPS": ["ops/README.md"],
}

# Bytes. ~4 bytes/token is the usual rough conversion, so 140 KB is ~35k tokens.
# Chosen with headroom over the 2026-08-15 measurement (~94 KB / ~24k tokens)
# so normal growth does not cry wolf, but well under the ~614 KB the chain cost
# when pending.md was mandated.
TOTAL_BUDGET = 140 * 1024

# No single mandated file should dominate the chain. suite-state.md and
# digest.md are both generated and both append-heavy, which is exactly the
# shape that got away last time.
PER_FILE_BUDGET = 40 * 1024


def size(rel):
    try:
        return os.path.getsize(os.path.join(ROOT, rel))
    except OSError:
        return None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    failures = []
    missing = []

    print("--- Session-start budget (CLAUDE.md section 1 step 4) ---\n")

    always_total = 0
    rows = []
    for rel in ALWAYS:
        b = size(rel)
        if b is None:
            missing.append(rel)
            continue
        always_total += b
        rows.append((rel, b))

    worst_tier, worst_extra = None, 0
    for tier, files in TIERS.items():
        extra = 0
        for rel in files:
            b = size(rel)
            if b is None:
                missing.append(rel)
                continue
            extra += b
        if extra > worst_extra:
            worst_tier, worst_extra = tier, extra
            worst_rows = [(r, size(r)) for r in files if size(r) is not None]

    for rel, b in rows + (worst_rows if worst_tier else []):
        flag = "  OVER" if b > PER_FILE_BUDGET else ""
        print(f"  {b/1024:8.1f} KB  ~{b//4:>7,} tok  {rel}{flag}")
        if b > PER_FILE_BUDGET:
            failures.append(
                f"{rel} is {b/1024:.1f} KB, over the {PER_FILE_BUDGET/1024:.0f} KB per-file cap"
            )

    total = always_total + worst_extra
    print(
        f"\n  worst-case tier: {worst_tier} (+{worst_extra/1024:.1f} KB)"
        f"\n  TOTAL {total/1024:.1f} KB  ~{total//4:,} tokens"
        f"  (budget {TOTAL_BUDGET/1024:.0f} KB / ~{TOTAL_BUDGET//4:,} tokens)"
    )

    if total > TOTAL_BUDGET:
        failures.append(
            f"session-start chain is {total/1024:.1f} KB, over the "
            f"{TOTAL_BUDGET/1024:.0f} KB budget by {(total-TOTAL_BUDGET)/1024:.1f} KB"
        )

    if missing:
        # A mandated read that does not exist is its own bug -- CLAUDE.md
        # pointed at eq/templates.md for months and it had never existed.
        for rel in missing:
            failures.append(f"{rel} is listed as a mandated read but does not exist")

    print()
    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        print(
            "\n  Trim the file that grew, or move it off the mandated-read list and\n"
            "  make it search-on-demand -- that is what was done to the tier\n"
            "  pending.md on 2026-08-15. Raising the number is the last resort,\n"
            "  not the first: the budget only works while it can still fail."
        )
        if os.environ.get("SESSION_BUDGET_REPORT") == "1":
            print("\n  (SESSION_BUDGET_REPORT=1 -- reporting only, not gating)")
            return 0
        return 1

    print("OK — session-start chain is within budget")
    return 0


if __name__ == "__main__":
    sys.exit(main())

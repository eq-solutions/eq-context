#!/usr/bin/env python3
"""Unit tests for the pure classifier in changelog_duplicates.py.

No filesystem beyond a throwaway tempdir per test.

Run:  python scripts/test_changelog_duplicates.py
"""
import os
import sys
import tempfile

from changelog_duplicates import classify, group_status, scan, slug


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    # --- slug -------------------------------------------------------------
    f += check("bare name", slug("field.md"), "field")
    f += check("eq- prefix strips", slug("eq-field.md"), "field")
    f += check("eq-solves- strips as one unit, not eq- twice", slug("eq-solves-service.md"), "service")
    # The ordering bug this guards: if "eq-" were tried before "eq-solves-",
    # "eq-solves-service" would strip to "solves-service", a slug that would
    # never match plain "service.md" or "eq-service.md" -- the whole duplicate
    # pair would go undetected, silently, which is exactly the failure this
    # file exists to catch.
    f += check("eq-solves- match is not shadowed by eq-", slug("eq-solves-service.md"), slug("eq-service.md"))
    f += check("no extension is tolerated", slug("field"), "field")

    # --- classify -----------------------------------------------------------
    f += check(
        "superseded_by pointing at a real sibling is marked",
        classify("shell.md", "---\nsuperseded_by: eq-shell.md\n---\n", {"shell.md", "eq-shell.md"}),
        (True, "superseded_by: eq-shell.md"),
    )
    marked, reason = classify(
        "shell.md", "---\nsuperseded_by: nonexistent.md\n---\n", {"shell.md", "eq-shell.md"}
    )
    f += check("superseded_by pointing at a non-sibling fails", marked, False)
    f += check("...names the dangling target", "nonexistent.md" in reason, True)

    f += check(
        "UNRECONCILED PAIR marker is honoured without frontmatter",
        classify("x.md", "# eq-solves-service changelog\nUNRECONCILED PAIR with eq-service.md\n", {"x.md", "y.md"}),
        (True, "UNRECONCILED PAIR marker present"),
    )
    f += check(
        "marker is case-insensitive",
        classify("x.md", "unreconciled pair, see twin", {"x.md", "y.md"})[0],
        True,
    )
    marked, reason = classify("x.md", "# just a changelog\n## 2026-08-14\n- did a thing\n", {"x.md", "y.md"})
    f += check("a plain file with no marker fails", marked, False)
    f += check("...says which two things are missing", "superseded_by" in reason and "UNRECONCILED" in reason, True)

    # A file with NO frontmatter block at all must not crash the parser --
    # eq/changelog/*.md is exempt from frontmatter-check.yml's required-key
    # schema, so a bare '# Title' changelog with no --- block is a real,
    # legal shape in this folder, not a hypothetical.
    marked, reason = classify("bare.md", "# eq-solves-service changelog\n\n## 2026-08-14\n- stuff\n", {"bare.md"})
    f += check("frontmatter-less file does not crash, just fails cleanly", marked, False)

    # --- group_status: the actual pass/fail rule ---------------------------
    # A single bare (canonical) file plus N validly-pointing dead twins is the
    # real 2026-07-19 shape (shell.md -> eq-shell.md) and must be clean.
    f += check(
        "one canonical + one dead twin -> clean",
        group_status(
            ["shell.md", "eq-shell.md"],
            {"shell.md": "---\nsuperseded_by: eq-shell.md\n---\n", "eq-shell.md": "---\ntitle: X\n---\n"},
        ),
        [],
    )
    # One canonical + TWO dead twins (a product could retire two names over
    # time) must also be clean -- the rule is "exactly one bare", not "exactly
    # two files".
    f += check(
        "one canonical + two dead twins -> clean",
        group_status(
            ["a.md", "b.md", "c.md"],
            {
                "a.md": "---\ntitle: canonical\n---\n",
                "b.md": "---\nsuperseded_by: a.md\n---\n",
                "c.md": "---\nsuperseded_by: a.md\n---\n",
            },
        ),
        [],
    )
    # Both sides UNRECONCILED -- the real eq-service.md/eq-solves-service.md
    # fix -- must be clean.
    f += check(
        "fully unreconciled pair -> clean",
        group_status(
            ["eq-service.md", "eq-solves-service.md"],
            {
                "eq-service.md": "---\nscope: UNRECONCILED PAIR\n---\n",
                "eq-solves-service.md": "# log\nUNRECONCILED PAIR, see twin.\n",
            },
        ),
        [],
    )
    # THE regression this file exists to catch: two live files, same product,
    # neither self-aware. Must name both.
    probs = group_status(
        ["eq-service.md", "eq-solves-service.md"],
        {
            "eq-service.md": "---\ntitle: X\n---\n## 2026-08-14\n- a\n",
            "eq-solves-service.md": "# log\n## 2026-08-14\n- b\n",
        },
    )
    f += check("two silent live twins -> two problems", len(probs), 2)
    f += check("...names eq-service.md", any("eq-service.md" in p for p in probs), True)
    f += check("...names eq-solves-service.md", any("eq-solves-service.md" in p for p in probs), True)
    # A dangling superseded_by is reported. It also does NOT vouch for
    # eq-shell.md as canonical -- only a VALID target counts as an
    # endorsement, so a typo'd pointer leaves eq-shell.md just as unexplained
    # as if shell.md had said nothing at all. Two problems, not one: this is
    # more noise for a human (who can obviously tell eq-shell.md is fine) but
    # it is the honest state from the tool's-eye view, and it disappears the
    # moment the typo is fixed to point at the real file.
    probs = group_status(
        ["shell.md", "eq-shell.md"],
        {"shell.md": "---\nsuperseded_by: nonexistent.md\n---\n", "eq-shell.md": "---\ntitle: X\n---\n"},
    )
    subjects = {p.split(":", 1)[0] for p in probs}
    f += check("dangling pointer + unvouched canonical -> two problems", len(probs), 2)
    f += check("...names the dangling file", "shell.md" in subjects, True)
    f += check("...also names the unvouched bare file", "eq-shell.md" in subjects, True)

    # THE regression a mutation test caught while building this rule: strip
    # the marker from ONE side of an otherwise-fine unreconciled pair. Under
    # an earlier "at most one bare file is fine" rule, the now-bare file was
    # presumed canonical purely by being alone -- nothing checked that its
    # sibling (still just "unreconciled", not "superseded_by X") actually
    # endorsed it. Must fail, naming only the file that went silent.
    probs = group_status(
        ["eq-service.md", "eq-solves-service.md"],
        {
            "eq-service.md": "---\nscope: UNRECONCILED PAIR, see twin\n---\n",
            "eq-solves-service.md": "# log\n## 2026-08-14\n- x\n",  # marker stripped
        },
    )
    subjects = {p.split(":", 1)[0] for p in probs}
    f += check("marker silently dropped from one side of a live pair -> caught", len(probs), 1)
    f += check("...names only the file that went silent", subjects, {"eq-solves-service.md"})
    # A two-file mutual-pointer cycle (each claims to be superseded BY the
    # other) is a contrived, not a real-observed, shape -- and forcing it to
    # fail is what conflicted with the real 3-file case below in an earlier
    # version. Zero bare files means zero silent duplicates, which is the
    # only thing this scan promises to catch, so this passes clean.
    probs = group_status(
        ["a.md", "b.md"],
        {"a.md": "---\nsuperseded_by: b.md\n---\n", "b.md": "---\nsuperseded_by: a.md\n---\n"},
    )
    f += check("mutual superseded_by, no bare files -> clean (not this scan's job)", probs, [])

    # THE real live shape (eq/changelog/'s "service" slug, 2026-08-15): three
    # files, one dead pointer plus a genuinely unresolved live pair. Neither
    # of the two old shapes ("exactly one bare" / "everyone unreconciled")
    # fits this on its own -- bare-counting handles it directly.
    f += check(
        "one dead pointer + two unreconciled live files -> clean",
        group_status(
            ["service.md", "eq-service.md", "eq-solves-service.md"],
            {
                "service.md": "---\nsuperseded_by: eq-service.md\n---\n",
                "eq-service.md": "---\nscope: UNRECONCILED PAIR, see eq-solves-service.md\n---\n",
                "eq-solves-service.md": "# log\nUNRECONCILED PAIR with eq-service.md.\n",
            },
        ),
        [],
    )
    # Same three-file group, but eq-service.md carries no UNRECONCILED marker
    # this time -- and that is fine, ONE problem, not two. service.md's own
    # 'superseded_by: eq-service.md' is itself a valid, independent form of
    # vouching: it explicitly names eq-service.md as the surviving file,
    # which is exactly as strong a signal as the marker would be. The marker
    # and a real inbound pointer are two different ways to be "explained";
    # a file only needs one. eq-solves-service.md has neither and nobody
    # points at it, so it alone is the problem.
    probs = group_status(
        ["service.md", "eq-service.md", "eq-solves-service.md"],
        {
            "service.md": "---\nsuperseded_by: eq-service.md\n---\n",
            "eq-service.md": "---\ntitle: EQ Service\n---\n",
            "eq-solves-service.md": "# log\n## 2026-08-14\n- x\n",
        },
    )
    subjects = {p.split(":", 1)[0] for p in probs}
    f += check("dead pointer vouches for its target -> only the truly silent file is flagged", len(probs), 1)
    f += check("...eq-service.md is vouched-for, not flagged", "eq-service.md" in subjects, False)
    f += check("...eq-solves-service.md is the one silent file, flagged", "eq-solves-service.md" in subjects, True)

    # --- scan (the real regression this file guards) -----------------------
    def make_dir(files):
        d = tempfile.mkdtemp(prefix="eq-changelog-")
        for name, content in files.items():
            with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                fh.write(content)
        return d

    # A single file per product: no problems, regardless of content.
    d = make_dir({"context.md": "# just a log\n## 2026-08-01\n- x\n"})
    groups, problems = scan(d)
    f += check("solo file group -> no problems", problems, [])
    f += check("solo file group -> counted", groups, {"context": ["context.md"]})

    # scan() itself just needs to prove it wires group_status() up per-slug
    # across a real directory -- group_status's own tests above cover the
    # actual pass/fail rules.
    d = make_dir({
        "eq-service.md": "---\ntitle: EQ Service\n---\n## 2026-08-14\n- PR merged\n",
        "eq-solves-service.md": "# eq-solves-service changelog\n## 2026-08-14\n- PR merged\n",
        "context.md": "# solo, unrelated product\n",
    })
    groups, problems = scan(d)
    f += check(
        "scan groups by slug across the directory",
        {s: sorted(members) for s, members in groups.items()},
        {"service": ["eq-service.md", "eq-solves-service.md"], "context": ["context.md"]},
    )
    f += check("scan surfaces the group_status problems, slug-prefixed", len(problems), 2)
    f += check("...prefixed with the slug", all(p.startswith("service:") for p in problems), True)
    f += check("solo product contributes no problems", any("context" in p for p in problems), False)

    # Missing directory must report, not crash.
    groups, problems = scan("/definitely/not/a/real/path")
    f += check("missing directory reports instead of crashing", groups, {})
    f += check("...with a problem string", len(problems), 1)

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()

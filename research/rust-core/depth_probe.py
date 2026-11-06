"""RUST-CORE-0 phase 0, D1: the front end's actual expression limits, and how deep a law line it makes.

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/depth_probe.py

His D1 ruling (REREAD-7, recorded in RULINGS.md): measure the actual front-end expression-depth limit; keep 130
provisionally until measurement; do not silently substitute 99. His H (REREAD-8): W14(c) is 91 in draft 9, the
candidate limit, not a proven maximum, until REREAD-9 has tried to write a deeper line; a deeper one goes back to him.
W14(c) bounds a law line's parentheses, counted lexically. This probe measures, through the front end itself
(`orlog.front.compile_bytes`, run, never edited):
1. the two expression limits at their edges, a case on each side: the tree depth of a statement, and the nesting of
   atoms (parentheses, minus, not, phrases);
2. the deepest law line the front end writes, over a search of statement families built to be deep, with the text
   that reaches it, and that text one level deeper and with a longer chain, each refused (REREAD-8, ZA8: the family
   whose innermost level has no parentheses of its own reaches 91);
3. the deepest law line among LAW-SUFFICIENCY's laws and the checker's fixtures.

What it does not show: that no text makes a deeper line. The search gives a lower bound, by a witness; the upper
bound is a derivation (LAW-FORMAT-0 draft 9, section 8, W14(c)), not a measurement. A line deeper than 91 found by the
search is reported, and the probe fails. Off the gate; MEASURED, never ESTABLISHED."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.front import compile_bytes  # noqa: E402


def depth(line):
    """W14(c)'s count (LAW-FORMAT-0 section 8): parentheses outside strings, a backslash skipping the next byte."""
    d = m = 0
    in_s = esc = False
    for ch in line:
        if in_s:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_s = False
        elif ch == '"':
            in_s = True
        elif ch == "(":
            d += 1
            m = max(m, d)
        elif ch == ")":
            d -= 1
    return m


def prog(*stmts):
    head = ["Title: Depth.", "§1 Let w be 1.5.", "§2 Let k be 2.", "§3 Let b be true."]
    return ("\n".join(head + ["§%s %s" % s if isinstance(s, tuple) else "§%d %s" % (i + 4, s)
                              for i, s in enumerate(stmts)]) + "\n").encode()


def compile_text(*stmts):
    c = compile_bytes(prog(*stmts))
    if not c.ok:
        return None, str(c.error)
    return max(depth(ln) for ln in c.law.decode("utf-8").split("\n")), None


def chain(n):
    """A Fix variable under n postfix conversions: each adds a tree level and no nesting."""
    return "w" + " as an integer as a fixed" * (n // 2) + (" as an integer" if n % 2 else "")


def alternating(levels, tail):
    """levels nested Fix sums, each over an Int conversion of the next (a promote at every level), over a chain."""
    e = chain(tail)
    for _ in range(levels):
        e = "w plus (%s) as an integer" % e
    return e


def alternating_open(levels, tail):
    """The same, the innermost level a sum over the chain, with no parentheses of its own (REREAD-8, ZA8)."""
    e = "w plus " + chain(tail)
    for _ in range(levels):
        e = "w plus (%s) as an integer" % e
    return e


FAMILIES = [("closed", alternating), ("open", alternating_open)]


FORMS = [
    ("a Let's value", lambda e: ["Let x be %s." % e]),
    ("an inline If's condition", lambda e: ["If w is less than %s, say 1." % e]),
    ("an inline Unless's condition", lambda e: ["Unless w is less than %s, say 1." % e]),
    ("a clause If's condition, with a block", lambda e: ["If w is less than %s, do the following." % e, ("4.1", "Say 1.")]),
    ("a clause Unless's condition, with a block", lambda e: ["Unless w is less than %s, do the following." % e,
                                                             ("4.1", "Say 1.")]),
    ("an Int compared at the top, clause Unless", lambda e: ["Unless w is less than (%s) as an integer, do the following."
                                                             % e, ("4.1", "Say 1.")]),
    ("an inline statement's value in an If's arm", lambda e: ["If b, set w to %s." % e]),
]


def main():
    out = []

    def say(s=""):
        out.append(s)
        print(s, flush=True)

    say("D1: THE FRONT END'S EXPRESSION LIMITS, AND THE DEEPEST LAW LINE IT WRITES (research/rust-core/depth_probe.py)")
    with open(os.path.join(ROOT, "src", "orlog", "syntax.py"), "rb") as f:
        say("src/orlog/syntax.py sha256 %s" % hashlib.sha256(f.read()).hexdigest())
    say()
    say("== 1. The two limits, at their edges (a Let's value)")
    edges = [("tree depth: 62 conversions (a tree 64 deep)", "Let x be %s." % chain(62), True),
             ("tree depth: 63 conversions (a tree 65 deep)", "Let x be %s." % chain(63), False),
             ("nesting: 23 parentheses (24 atoms deep)", "Let x be %sk%s." % ("(" * 23, ")" * 23), True),
             ("nesting: 24 parentheses (25 atoms deep)", "Let x be %sk%s." % ("(" * 24, ")" * 24), False)]
    held = 0
    for name, st, want in edges:
        d, err = compile_text(st)
        ok = (d is not None) == want
        held += ok
        say("  %-46s %s  [%s]" % (name, "accepted, deepest law line %d" % d if d is not None else "refused, " + err,
                                  "as expected" if ok else "NOT AS EXPECTED"))
    say()
    say("== 2. The deepest law line, by form and family (levels of promoted conversions 0-24, a conversion chain below,")
    say("   0-63; the innermost level closed in parentheses, or open)")
    best_all = (0, None, None, None)
    for fam, build in FAMILIES:
        for name, form in FORMS:
            best = (0, None)
            for levels in range(25):
                for tail in range(64):
                    d, err = compile_text(*form(build(levels, tail)))
                    if d is not None and d > best[0]:
                        best = (d, (levels, tail))
            say("  %-6s %-46s %d  (levels %d, chain %d)" % (fam, name, best[0], best[1][0], best[1][1]))
            if best[0] > best_all[0]:
                best_all = (best[0], "%s, %s" % (name, fam), (form, build), best[1])
    form, build = best_all[2]
    levels, tail = best_all[3]
    say("  deepest found: %d, in %s (levels %d, chain %d). Its statements:" % (best_all[0], best_all[1], levels, tail))
    for st in form(build(levels, tail)):
        say("    %s" % (st if isinstance(st, str) else "§%s %s" % st))
    edges2 = 0
    for what, args in (("one level more", (levels + 1, tail)), ("a chain two longer", (levels, tail + 2))):
        d, err = compile_text(*form(build(*args)))
        edges2 += d is None
        say("    %-20s %s  [%s]" % (what, "accepted, deepest law line %d" % d if d is not None else "refused, " + err,
                                    "as expected" if d is None else "NOT AS EXPECTED"))
    say()
    say("== 3. LAW-SUFFICIENCY's laws and the checker's fixtures")
    sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
    sys.path.insert(0, HERE)
    import common
    from closure_tests import fixtures
    import format_check
    texts = common.accepted() + fixtures()
    corpus = max(max(depth(ln) for ln in compile_bytes(t[2]).law.decode("utf-8").split("\n")) for t in texts)
    fix = max(max(depth(ln) for ln in compile_bytes(t.encode("utf-8")).law.decode("utf-8").split("\n"))
              for _, t in format_check.FIXTURES)
    say("  %d texts: deepest law line %d; %d fixture laws: deepest %d" % (len(texts), corpus, len(format_check.FIXTURES), fix))
    say()
    deeper = best_all[0] > 91
    say("D1 MEASURED: the limits held at their edges %d of 4, the deepest line's own edges %d of 2; the deepest law line "
        "found is %d (a witness, a lower bound)%s;" % (held, edges2, best_all[0],
                                                       ", DEEPER THAN W14(c): it goes to the owner (his H)" if deeper else ""))
    say("the upper bound 91 derived in draft 9's section 8 is REASONED, not measured; W14(c) is 91, the candidate limit "
        "(his H), until REREAD-9 has tried to write a deeper line")
    sys.exit(0 if held == 4 and edges2 == 2 and not deeper else 1)


if __name__ == "__main__":
    main()

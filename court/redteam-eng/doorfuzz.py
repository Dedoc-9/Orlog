"""Fuzz the door's retraction claim: canon(canon(x)) == canon(x), with no repair on the second pass.

  python -B doorfuzz.py N
Prints every counterexample (minimised by deleting characters while the property still fails).
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.canon import canonicalize  # noqa: E402

ALPHA = (['§1 ', 'Say ', 'Let x be ', 'Note:', 'Title:', '  Note:', ' Note:', ' ', '  ', '"', '""',
          '“', '”', '„', '″', '‘', '’', '′', ' ', '\t', ' ', '　',
          'e', 'x', '1', '.', ',', ';', '=', '<', '́', '̸', 'K', ';', '−', '×',
          '≤', '≠', '‍', '\r', '\r\n', '\n', 'é', 'é', 'Å', 'Å', '﻿'])


def check(raw):
    c1 = canonicalize(raw)
    if c1.text is None:
        return None
    c2 = canonicalize(c1.text.encode("utf-8"))
    if c2.text != c1.text or c2.repairs or c2.refusals:
        return (c1.text, c2.text, [e["rule"] for e in c2.events if e["cls"] != "NOTE"])
    return None


def minimise(s):
    changed = True
    while changed:
        changed = False
        for i in range(len(s)):
            t = s[:i] + s[i + 1:]
            if t and check(t.encode("utf-8")):
                s = t
                changed = True
                break
    return s


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    seen = set()
    bad = 0
    for _ in range(n):
        s = "".join(rng.choice(ALPHA) for _ in range(rng.randint(1, 14)))
        r = check(s.encode("utf-8"))
        if r:
            m = minimise(s)
            if m not in seen:
                seen.add(m)
                bad += 1
                print("COUNTEREXAMPLE %r -> first %r -> second %r %s" % ((m,) + check(m.encode("utf-8"))))
    print("door retraction fuzz: %d inputs, %d distinct minimal counterexamples" % (n, bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())

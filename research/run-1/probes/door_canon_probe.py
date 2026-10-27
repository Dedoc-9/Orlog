"""EXPERIMENTAL RESEARCH PROBE. It is not the door and not a gate row, and nothing in the program reads it; its
output is evidence/run1-door-canon.txt.

A transfer of the session probe's method (research/run-1/probes/cut0_session.py: one canonical form, mutations of
every input) onto Orlog's own door and parser, where DESIGN-BRIEF.md's H2 (the door and the parser read an indented
Note: or Title: line apart) is still open.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/door_canon_probe.py

Properties of each mutant:
- P1, idempotence: a text the door accepts, given to the door again, comes back the same with no repair (so its law
  seal is the raw text's: compile_bytes parses the door's text);
- P2, agreement: every line the door reads as free text (after Note: or Title:) the parser reads as a Note or a
  Title, and the converse;
- P3, totality: the door and the front end answer every input with a verdict, never an exception.

Two sweeps, because what a sweep can find is what its mutations can make:
- single: every replacement of one byte by one of ten ASCII bytes, every deletion and every duplication, over the
  examples and the court's fixtures. It cannot make an indented Note:, which needs an insertion or a two-byte space.
- door-aware: over the smaller texts, every insertion and every replacement of one character drawn from each class the
  door repairs or refuses (an NBSP, a zero-width space, a joiner, curly and single quotes, a bidi control, a Hangul
  filler, a dash, a combining mark), with a space, a tab, an LF and a straight quote.
Then H2's repair, the door reading the marker at column one as the parser does, run in memory over the door-aware
sweep and over every COMPAT-0 frozen text, with every frozen verdict it changes named. Nothing under src/ is edited.

It passes when the door-aware sweep finds H2's split in the door as built (the sweep can see the defect), finds no
property broken under the repair, and the single sweep finds nothing else. A frozen verdict the repair changes is a
finding to settle, printed, not a failure of the probe.
"""
import base64
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog import canon                                          # noqa: E402
from orlog.front import compile_bytes                           # noqa: E402

ORIGINAL_MARKER = canon._context_marker
ASCII = [c.encode() for c in " \n\t\".:Na1"]
DOOR_CLASSES = [chr(c).encode("utf-8") for c in (0x00A0, 0x200B, 0x200D, 0x201C, 0x201D, 0x2018, 0x202E, 0x3164,
                                                  0x2013, 0x0301)] + [b" ", b"\t", b"\n", b'"']


def column_one_marker(line):
    """H2's repair: the marker counts only at column one, as syntax.parse_program reads it."""
    for m in ("Note:", "Title:"):
        if line.startswith(m):
            return len(m)
    return None


def parser_free(line):
    return line.startswith("Note:") or line.startswith("Title:")


def check(raw):
    out = []
    try:
        c = canon.canonicalize(raw)
    except Exception as e:
        return ["P3-door-raised %s" % type(e).__name__]
    try:
        compile_bytes(raw)
    except Exception as e:
        out.append("P3-front-raised %s" % type(e).__name__)
    if c.text is None:
        return out
    try:
        again = canon.canonicalize(c.text.encode("utf-8"))
    except Exception as e:
        return out + ["P3-door-raised-on-its-own-output %s" % type(e).__name__]
    if again.text != c.text or any(e["cls"] in ("REPAIR", "REFUSE") for e in again.events):
        out.append("P1-not-idempotent")
    for line in c.text.split("\n"):
        if (canon._context_marker(line) is not None) != parser_free(line):
            out.append("P2-split")
            break
    return out


def single(raw):
    for i in range(len(raw)):
        for c in ASCII:
            if c[0] != raw[i]:
                yield raw[:i] + c + raw[i + 1:]
        yield raw[:i] + raw[i + 1:]
        yield raw[:i] + raw[i:i + 1] + raw[i:]


def door_aware(raw):
    text = raw.decode("utf-8")
    for i in range(len(text) + 1):
        for c in DOOR_CLASSES:
            yield (text[:i] + c.decode("utf-8") + text[i:]).encode("utf-8")
            if i < len(text):
                yield (text[:i] + c.decode("utf-8") + text[i + 1:]).encode("utf-8")


def sweep(bases, mutate):
    counts, first, n = {}, {}, 0
    for name, raw in bases:
        for m in mutate(raw):
            n += 1
            for f in check(m):
                counts[f] = counts.get(f, 0) + 1
                first.setdefault(f, (name, m))
    return n, counts, first


def frozen_verdicts():
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    out = {}
    for t in doc["texts"]:
        c = compile_bytes(base64.b64decode(t["b64"]))
        out[t["id"]] = c.law_seal if c.ok else "REFUSED %s line %s" % (c.error.code, c.error.line)
    return out


def texts(patterns):
    out = []
    for pattern in patterns:
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            with open(path, "rb") as fh:
                out.append((os.path.relpath(path, ROOT).replace(os.sep, "/"), fh.read()))
    return out


def show(counts, first):
    print("  properties broken: %s" % (", ".join("%s %d" % kv for kv in sorted(counts.items())) or "none"))
    for f, (name, m) in sorted(first.items()):
        line = next((l for l in m.decode("utf-8", "replace").split("\n") if "Note:" in l or "Title:" in l), "")
        print("  first %s: a mutant of %s, line %r" % (f, name, line[:50]))


def main():
    big = texts(("examples/*.orl", "examples/*/*.orl", "tests/fixtures/court/*.orl"))
    small = texts(("tests/fixtures/court/*.orl", "examples/spellings/*.orl"))
    print("== single: every one-byte replacement (10 ASCII bytes), deletion and duplication of %d texts" % len(big))
    n1, c1, f1 = sweep(big, single)
    print("  mutants %d" % n1)
    show(c1, f1)
    print("== door-aware: every insertion and replacement of one character of the door's classes, %d smaller texts"
          % len(small))
    n2, c2, f2 = sweep(small, door_aware)
    print("  mutants %d (the door as built)" % n2)
    show(c2, f2)
    print("== H2's repair in memory: the door reads the marker at column one")
    before = frozen_verdicts()
    canon._context_marker = column_one_marker
    try:
        n3, c3, f3 = sweep(small, door_aware)
        after = frozen_verdicts()
    finally:
        canon._context_marker = ORIGINAL_MARKER
    print("  door-aware mutants %d (the door repaired)" % n3)
    show(c3, f3)
    changed = sorted(k for k in before if before[k] != after[k])
    print("  COMPAT-0's %d frozen texts whose verdict the repair changes: %d" % (len(before), len(changed)))
    for k in changed:
        print("    %s: %s -> %s (a finding to settle in tests/compat/settled.json, with its reason and amendment)" % (
            k, before[k], after[k]))
    sees = c2.get("P2-split", 0) > 0
    ok = sees and not c3 and not {k for k in c1 if k != "P2-split"} and not {k for k in c2 if k != "P2-split"}
    print("DOOR CANON PROBE %s: the door-aware sweep %s H2's split in the door as built (%d mutants); the single sweep "
          "finds %s; the repair breaks %s and changes %d frozen verdict(s)" % (
              "HELD" if ok else "FAILED", "finds" if sees else "DOES NOT FIND", c2.get("P2-split", 0),
              ", ".join(sorted(c1)) or "nothing", ", ".join(sorted(c3)) or "nothing", len(changed)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

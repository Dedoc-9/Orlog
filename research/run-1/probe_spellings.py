"""What version 0 does with each candidate spelling for RUN-1's new forms (research for RULINGS.md; a measurement, not a
test). A new form is safe for COMPAT-0 only where v0 refuses SYNTAX at the statement itself. Anywhere else, the form
would change what v0 does with an existing text: a call to an unknown procedure, or a refusal elsewhere. The probe also
scans COMPAT-0's 3,361 frozen texts for any line a candidate form would capture.

  PYTHONHASHSEED=0 python -B research/run-1/probe_spellings.py
"""
import base64
import gzip
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.front import compile_bytes  # noqa: E402
from orlog.syntax import RESERVED  # noqa: E402

# (role, statement, needs children)
CANDIDATES = [
    ("port, read each tick", "Let thrust be given each tick as a fixed.", False),
    ("port, read each tick", "Let thrust be read each tick as a fixed.", False),
    ("port, read each tick", "Receive thrust as a fixed.", False),
    ("port, read each tick", "Take thrust each tick as a fixed.", False),
    ("port, read once", "Let gravity be given as a fixed.", False),
    ("port, read once", "Let gravity be given once as a fixed.", False),
    ("port, other types", "Let jumped be given each tick as a truth value.", False),
    ("port, other types", "Let name be given as a text.", False),
    ("port, other types", "Let count be given each tick as an integer.", False),
    ("tick block", "Each tick, do the following.", True),
    ("tick block", "At each tick, do the following.", True),
    ("tick block", "On each tick, do the following.", True),
    ("tick block", "For each tick, do the following.", True),
    ("tick block, with a budget", "Each tick, at most 100000 operations, do the following.", True),
]

# the captured lines: what each candidate form would match in an existing text (case-insensitive, after the label)
CAPTURES = [
    ("Let X be given ...", re.compile(r"^let \S+ be given\b", re.I)),
    ("Let X be read each tick ...", re.compile(r"^let \S+ be read each tick\b", re.I)),
    ("Each tick, ...", re.compile(r"^each tick\b", re.I)),
    ("At each tick, ...", re.compile(r"^at each tick\b", re.I)),
    ("Receive / Take ... (call-shaped)", re.compile(r"^(receive|take) \S+", re.I)),
]


def first_word_reserved(stmt):
    return stmt.split()[0].lower() in RESERVED


def probe(stmt, children):
    lines = ["§1 " + stmt] + (["§1.1 Say 1."] if children else [])
    c = compile_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    if c.ok:
        return "ACCEPTED", "accepted"
    at = "at the statement" if c.error.line == 1 else "at line %s" % c.error.line
    return c.error.code, "%s %s" % (c.error.code, at)


def frozen_lines():
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    for t in doc["texts"]:
        text = base64.b64decode(t["b64"]).decode("utf-8", "replace")
        for line in text.split("\n"):
            m = re.match(r"^\s*§\S+\s+(.*)$", line)
            if m:
                yield t["id"], m.group(1)


def main():
    print("== what version 0 does with each candidate (a minimal program: the statement, and a child if a block)")
    for role, stmt, children in CANDIDATES:
        code, said = probe(stmt, children)
        safe = code == "SYNTAX" and said.endswith("at the statement")
        print("  %-26s %-58s first word %-9s v0: %-28s %s" % (
            role, stmt, "reserved" if first_word_reserved(stmt) else "NOT reserved", said,
            "SAFE" if safe else "UNSAFE: v0 gives it a meaning or another refusal"))
    print("== lines of COMPAT-0's frozen texts that a candidate form would capture")
    hits = {name: [] for name, _ in CAPTURES}
    for ident, stmt in frozen_lines():
        for name, rx in CAPTURES:
            if rx.match(stmt):
                hits[name].append((ident, stmt))
    for name, found in hits.items():
        print("  %-36s %d line(s)%s" % (name, len(found), "" if not found else ": " + "; ".join(
            "%s: %s" % (i, s[:60]) for i, s in found[:4])))
    print("== 'tick' is a variable name in the corpus: never reserve it")
    for ident, stmt in frozen_lines():
        if ident.startswith("corpus/examples/fall.orl") and re.search(r"\btick\b", stmt):
            print("  %s: %s" % (ident, stmt[:70]))
            break


if __name__ == "__main__":
    main()

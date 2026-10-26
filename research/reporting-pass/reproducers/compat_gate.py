"""What tests/compat.py's verdicts rest on beyond the texts' bytes.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/compat_gate.py

Everything runs on a copy of tests/compat/ under work/reporting-pass/compat-copy/ (compat.HERE pointed at it); the
tracked files are read, never written.

(a) A baseline row removed. The header names 3,361 texts and the texts file holds 3,361; `compare` walks the baseline,
    so a frozen text with no row is never computed against anything, and `check` prints HELD over the rest. Run as the
    gate runs (cmd_check, --jobs 8) on the copy with one row removed; the self-test's compat row's own test applied to
    that output.
(b) A difference, then its rows removed. The self-test's plant reserve-tick makes fall.orl's frozen versions differ
    (compat.py selftest's own plant, in process, over the 361 texts that are not mutants, as its selftest computes
    them). Their rows removed from the baseline, the same computation reads every text the same.
(c) A settled entry with no reason and no amendment. compat/README.md says a declared change is {"id", "now",
    "reason", "amendment"}; `compare` reads only "now". Under the same plant, entries holding only id and now settle
    every difference.
(d) compat's receipt_core is not the arbiter's rule (its docstring says it is); whether that leniency reaches a verdict.
"""
import argparse
import json
import os
import re
import shutil
import sys

import _common as C

C.require_env()
sys.path.insert(0, os.path.join(C.ROOT, "tests"))
import compat  # noqa: E402

COPY = os.path.join(C.WORK, "compat-copy")


def make_copy(drop=()):
    if os.path.isdir(COPY):
        shutil.rmtree(COPY)
    shutil.copytree(os.path.join(C.ROOT, "tests", "compat"), COPY)
    path = os.path.join(COPY, "baseline-v0.jsonl")
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8").split("\n")
    rows = [l for l in lines[1:] if l]
    kept = [l for l in rows if json.loads(l)["id"] not in drop]
    with open(path, "wb") as fh:
        fh.write(("\n".join([lines[0]] + kept) + "\n").encode("utf-8"))
    compat.HERE = COPY
    return len(rows) - len(kept)


def part_a():
    head, base = compat.load_baseline("v0")
    victim = sorted(base)[0]
    removed = make_copy(drop={victim})
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = compat.cmd_check(argparse.Namespace(version="v0", jobs=8))
    out = buf.getvalue()
    doc, _ = compat.load_texts("v0")
    m = re.search(r"^  same (\d+), newly accepted (\d+), settled (\d+), skipped (\d+), differ (\d+), input changed (\d+)",
                  out, re.M)
    n = re.search(r"; (\d+) texts;", out)
    row_ok = code == 0 and "COMPAT-0 HELD" in out and m is not None and n is not None   # tests/selftest.py compat_rows
    print("== (a) one baseline row removed (%s; %d removed); header count %d; texts file %d texts" % (
        victim, removed, head["count"], len(doc["texts"])))
    for l in out.splitlines():
        print("   | " + l)
    print("   exit %d; the self-test's compat row would read %s" % (code, "PASS" if row_ok else "FAIL"))
    return code == 0 and "COMPAT-0 HELD" in out and row_ok


def planted_results():
    """compat.py selftest's own plant reserve-tick, computed as its selftest computes (in process, no mutants)."""
    import orlog.syntax as syntax
    doc, _ = compat.load_texts("v0")
    head, base = compat.load_baseline("v0")
    texts = compat.selftest_texts(doc)
    syntax.RESERVED.add("tick")
    try:
        results = compat.compute(texts, head["budgets"])
    finally:
        syntax.RESERVED.discard("tick")
    return texts, {t["id"]: base[t["id"]] for t in texts}, results


def part_b_c():
    compat.HERE = os.path.join(C.ROOT, "tests", "compat")
    texts, sub, results = planted_results()
    v = compat.compare(sub, results, texts, {})
    differ = sorted(i for i, (k, _, _) in v.items() if k == "differs")
    print("== (b) plant reserve-tick: %d of %d texts differ (%s)" % (len(differ), len(v), ", ".join(differ)))
    trimmed = {i: r for i, r in sub.items() if i not in differ}
    v2 = compat.compare(trimmed, results, texts, {})
    counts = {}
    for k, _, _ in v2.values():
        counts[k] = counts.get(k, 0) + 1
    print("   their rows removed: %s; the gate's test (differs + input changed) = %d -> %s" % (
        counts, counts.get("differs", 0) + counts.get("input-changed", 0),
        "HELD" if counts.get("differs", 0) + counts.get("input-changed", 0) == 0 else "BROKEN"))
    b = not counts.get("differs") and not counts.get("input-changed")
    bare = {i: {"id": i, "now": v[i][2]} for i in differ}       # no reason, no amendment
    v3 = compat.compare(sub, results, texts, bare)
    settled = sorted(i for i, (k, _, _) in v3.items() if k == "settled")
    left = sorted(i for i, (k, _, _) in v3.items() if k == "differs")
    print("== (c) settled entries holding only id and now (no reason, no amendment): %d settled, %d differ" % (
        len(settled), len(left)))
    print("   an entry as written: %s" % json.dumps(bare[differ[0]], sort_keys=True)[:160])
    return b, bool(settled) and not left


def part_d():
    from orlog.interp import Interp
    from orlog.front import compile_bytes
    from orlog import arbiter
    comp = compile_bytes(C.read("examples/collatz.orl"))
    good = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run().receipt()
    variants = {"as written": good, "CR LF": good.replace(b"\n", b"\r\n"), "no final LF": good[:-1],
                "head renamed": good.replace(b"orlog-receipt 0", b"orlog-receipt 9", 1)}
    print("== (d) compat.receipt_core against arbiter.receipt_core, on collatz's reference receipt:")
    reaches = False
    for name, b in variants.items():
        c, a = compat.receipt_core(b), arbiter.receipt_core(b)
        same_sha = c is not None and compat.sha(c) == compat.sha(compat.receipt_core(good))
        print("   %-12s compat: %-9s arbiter: %-9s compat's sha equal to the good one's: %s" % (
            name, "a core" if c is not None else "None", "a core" if a is not None else "None", same_sha))
        reaches |= name != "as written" and same_sha
    print("   the leniency reaches a verdict: %s (every variant hashes differently, so it reads DIFFERS)" % reaches)
    return reaches


def main():
    a = part_a()
    b, c = part_b_c()
    d = part_d()
    compat.HERE = os.path.join(C.ROOT, "tests", "compat")
    shutil.rmtree(COPY, ignore_errors=True)
    print("COMPAT GATE: (a) HELD with a row removed: %s; (b) a difference hidden by removing its rows: %s; "
          "(c) settled without reason or amendment: %s; (d) receipt_core leniency reaches a verdict: %s" % (a, b, c, d))
    return 0


if __name__ == "__main__":
    sys.exit(main())

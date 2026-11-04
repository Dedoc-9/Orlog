"""Compare what two texts of a closed law show when run: python -B tools/observe/observe.py OLD.orl NEW.orl

A law takes no input today, so one run is its whole behaviour and this comparison is exact, not a sample. It chooses no
preservation relation: that is OPEN by the owner's ruling, so every candidate is reported and none is called the verdict.
Exit: 0 reported, 1 a text refused at compile, 2 usage. python -B tools/observe/observe.py --selftest checks the comparison."""
import difflib
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.arbiter import Arbiter  # noqa: E402

PLANT = None


def exact(old, new):
    return old == new


def prefix(old, new):
    if PLANT == "prefix-is-subsequence":
        return subsequence(old, new)
    return new[:len(old)] == old


def subsequence(old, new):
    it = iter(new)
    return all(line in it for line in old)


RELATIONS = (("exact", exact), ("prefix", prefix), ("subsequence", subsequence))


def changed(old, new):
    """Only the lines that differ, "- " old and "+ " new, aligned so that one inserted line reads as one line."""
    if PLANT == "diff-positional":
        out = []
        for i in range(max(len(old), len(new))):
            a, b = old[i:i + 1], new[i:i + 1]
            if a != b:
                out += ["- " + x for x in a] + ["+ " + x for x in b]
        return out
    out = []
    for op, i, j, k, m in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if op != "equal":
            out += ["- " + x for x in old[i:j]] + ["+ " + x for x in new[k:m]]
    return out


def run(raw, wd):
    """-> (law bytes, status, output lines), or (None, refusal, None) when the text does not compile."""
    comp, w, ref = Arbiter(wd, backends=()).arbitrate(raw, "t")
    if not comp.ok:
        return None, "%s at line %s" % (w["refusal"]["code"], w["refusal"]["line"]), None
    if ref is None:
        return comp.law, "NO VERDICT: stopped by the host's budget", None
    r = w["reference"]
    status = r["status"] + (" " + str(r["code"]) if r.get("code") else "")
    return comp.law, status, bytes(ref.out).decode("utf-8").split("\n")[:-1]


def compare(old, new):
    with tempfile.TemporaryDirectory() as wd:
        a, b = run(old, wd), run(new, wd)
    if a[0] is None or b[0] is None:
        return {"refused": (a[1] if a[0] is None else None, b[1] if b[0] is None else None)}
    rows = {"same law": a[0] == b[0], "old status": a[1], "new status": b[1], "same status": a[1] == b[1],
            "old lines": a[2], "new lines": b[2]}
    rows["law diff"] = changed(a[0].decode("utf-8").split("\n"), b[0].decode("utf-8").split("\n"))
    if a[2] is not None and b[2] is not None:
        for name, f in RELATIONS:
            rows[name] = f(a[2], b[2])
        rows["output diff"] = changed(a[2], b[2])
    return rows


def src(*lines):
    return "".join("§%d %s\n" % (i + 1, x) for i, x in enumerate(lines)).encode("utf-8")


# hand-worked before the first run: (name, old, new, exact, prefix, subsequence)
CASES = (
    ("unchanged", src("Say 1.", "Say 2."), src("Say 1.", "Say 2."), True, True, True),
    ("output added at the end", src("Say 1."), src("Say 1.", "Say 2."), False, True, True),
    ("output added at the start", src("Say 2."), src("Say 1.", "Say 2."), False, False, True),
    ("output changed", src("Say 1."), src("Say 2."), False, False, False),
    ("output removed", src("Say 1.", "Say 2."), src("Say 1."), False, False, False),
    ("output reordered", src("Say 1.", "Say 2."), src("Say 2.", "Say 1."), False, False, False),
    ("another law, the same output", src("Say 1 + 1."), src("Say 2."), True, True, True),
)


def selftest():
    global PLANT
    bad = 0
    for name, old, new, *want in CASES:
        r = compare(old, new)
        got = [r.get(n) for n, _ in RELATIONS]
        ok = got == want
        bad += not ok
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    r = compare(src("Say 1 + 1."), src("Say 2."))
    ok = r["same law"] is False
    bad += not ok
    print("%s the law is reported apart from the output" % ("PASS" if ok else "FAIL"))
    # the lines are equal and every relation holds on them, while the run now refuses: why the status is reported apart
    r = compare(src("Say 1."), src("Say 1.", "Say 1 / 0."))
    ok = r["old status"] == "COMPLETED" and r["new status"].startswith("REFUSED") and r["exact"] is True
    bad += not ok
    print("%s a run's refusal is reported apart from its lines: %s" % ("PASS" if ok else "FAIL", r["new status"]))
    r = compare(src("Say x."), src("Say 1."))
    ok = "refused" in r and r["refused"][1] is None and "exact" not in r
    bad += not ok
    print("%s a text refused at compile has no comparison" % ("PASS" if ok else "FAIL"))
    # hand-worked: one line added at the start is one line of diff; one literal changed is one clause of the law
    r = compare(src("Say 2."), src("Say 1.", "Say 2."))
    ok = r["output diff"] == ["+ 1"]
    bad += not ok
    print("%s one inserted line reads as one line" % ("PASS" if ok else "FAIL"))
    r = compare(src("Say 1.", "Say 2."), src("Say 1.", "Say 3."))
    d = r["law diff"]
    ok = len(d) == 2 and d[0].startswith("- ") and d[1].startswith("+ ") and "2" in d[0] and "3" in d[1] and r["output diff"] == ["- 2", "+ 3"]
    bad += not ok
    print("%s the law diff names the one changed clause" % ("PASS" if ok else "FAIL"))
    r = compare(src("Say 1 + 1."), src("Say 2."))
    ok = r["output diff"] == [] and r["law diff"] != [] and r["same status"] is True
    bad += not ok
    print("%s another law, the same output: a law diff and no output diff" % ("PASS" if ok else "FAIL"))
    r = compare(src("Say 1."), src("Say 1.", "Say 1 / 0."))
    ok = r["same status"] is False and r["output diff"] == []
    bad += not ok
    print("%s a status that changed with no output diff is said" % ("PASS" if ok else "FAIL"))
    PLANT = "diff-positional"
    caught = compare(src("Say 2."), src("Say 1.", "Say 2."))["output diff"] != ["+ 1"]
    PLANT = None
    bad += not caught
    print("%s plant diff-positional caught" % ("PASS" if caught else "FAIL"))
    PLANT = "prefix-is-subsequence"
    caught = compare(src("Say 2."), src("Say 1.", "Say 2."))["prefix"] is not False
    PLANT = None
    bad += not caught
    print("%s plant prefix-is-subsequence caught" % ("PASS" if caught else "FAIL"))
    print("OBSERVE SELFTEST %s" % ("FAILED" if bad else "PASSED"))
    return 1 if bad else 0


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) != 2:
        print(__doc__)
        return 2
    old, new = (open(p, "rb").read() for p in argv)
    r = compare(old, new)
    if "refused" in r:
        for label, code in zip(("old", "new"), r["refused"]):
            if code:
                print("%s REFUSED %s" % (label, code))
        return 1
    for k in ("same law", "old status", "new status", "same status"):
        print("%-12s %s" % (k, r[k]))
    for line in r["law diff"]:
        print("  law    " + line)
    if "exact" not in r:
        print("no output comparison: a run had no output to compare")
        return 0
    print("%-12s %d, %d" % ("lines", len(r["old lines"]), len(r["new lines"])))
    print("the old output is preserved under each candidate relation (none is chosen; the relation is OPEN):")
    for n, _ in RELATIONS:
        print("  %-12s %s" % (n, "holds" if r[n] else "does not hold"))
    for line in r["output diff"]:
        print("  output " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""R8's switch, `court.REFUSED_EVALUATION_CHECK`, is read by `orl.py court` at its shipped value, and set explicitly by
every row that tests R8, so no row sees the shipped value.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/r8_default.py

1. The lines that set the switch, in tests/selftest.py and tests/court_monotone.py (each sets it before each reading
   and puts it back to True after).
2. The court with the shipped value flipped to False (src/orlog/court.py, that one line, in a copy of orl.py and src/
   under work/reporting-pass/r8-default-tree/), run as a person runs it: `orl.py court tests/fixtures/r8/omit.orl
   --backends python`. Beside it the same command on the tree as it stands.
3. The same planted module read the way the self-test's R8 rows read it (the switch set True first): the row's reading
   does not depend on the shipped value. And read the way orl.py reads it (the switch untouched), with every claim's
   seal ratified in memory: DP-5's reading, GROUNDED.
court_mutants.py's plant r8-default-off runs the whole self-test on that flipped value: 169/169.
"""
import os
import re
import shutil
import subprocess
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402

FLIP = [("REFUSED_EVALUATION_CHECK = True", "REFUSED_EVALUATION_CHECK = False")]


def setters():
    for rel in ("tests/selftest.py", "tests/court_monotone.py", "orl.py"):
        text = C.read(rel).decode("utf-8").split("\n")
        hits = [(i + 1, l.strip()) for i, l in enumerate(text) if "REFUSED_EVALUATION_CHECK" in l]
        print("   %s: %s" % (rel, "; ".join("line %d: %s" % h for h in hits) if hits else "never names the switch"))


def cli(tree, wd):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-B", os.path.join(tree, "orl.py"), "court",
                        os.path.join(C.ROOT, "tests", "fixtures", "r8", "omit.orl"), "--backends", "python",
                        "--workdir", wd, "--ledger", os.path.join(C.WORK, "no-such-ledger.jsonl")],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    keep = [l.strip() for l in r.stdout.splitlines() if l.strip().split(" ")[0] in ("evaluation", "support")]
    sand = re.search(r'"sandwich": "([^"]*)"', r.stdout)
    return r.returncode, keep, sand.group(1) if sand else "?"


def main():
    print("1. where the switch is set:")
    setters()
    tree = os.path.join(C.WORK, "r8-default-tree")
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(os.path.join(C.ROOT, "src"), os.path.join(tree, "src"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copyfile(os.path.join(C.ROOT, "orl.py"), os.path.join(tree, "orl.py"))
    path = os.path.join(tree, "src", "orlog", "court.py")
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")
    assert text.count(FLIP[0][0]) == 1
    with open(path, "wb") as fh:
        fh.write(text.replace(*FLIP[0]).encode("utf-8"))
    wd = C.workdir("r8-default")
    for name, root in (("as it stands", C.ROOT), ("shipped value False", tree)):
        code, keep, sand = cli(root, wd)
        print("2. orl.py court omit.orl, %s: exit %d; %s; sandwich %s" % (name, code, "; ".join(keep), sand))
    mod = C.planted("court", FLIP)
    comp, w, ref = Arbiter(wd, backends=("python",)).arbitrate(C.read("tests/fixtures/r8/omit.orl"), "r8d-omit")
    rec, led = parse_receipt(ref.receipt()), C.ledger_all(comp)
    mod.REFUSED_EVALUATION_CHECK = True               # what tests/selftest.py's r8_rows does before its reading
    as_row = mod.panel(comp, w, rec, led)["rows"][0]
    mod.REFUSED_EVALUATION_CHECK = False              # the shipped value under the plant, as orl.py reads it
    as_cli = mod.panel(comp, w, rec, led)["rows"][0]
    print("3. the planted module, read as the R8 row reads it: %s; %s" % (as_row["evaluation"], as_row["grounding"]))
    print("   read as orl.py reads it, every seal ratified (in memory): %s; %s; %s" % (
        as_cli["evaluation"], as_cli["support"], as_cli["grounding"]))
    print("   the court as built, as orl.py reads it: %s" % COURT.panel(comp, w, rec, led)["rows"][0]["grounding"])
    shutil.rmtree(tree, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

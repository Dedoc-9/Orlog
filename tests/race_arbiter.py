"""The use-case review's race: two different programs arbitrated many times at once in one shared work folder. Before
each arbitration had a run folder of its own, this gave false dissents. A measurement, not a test; the self-test
holds a smaller form of it as a row.

  PYTHONHASHSEED=0 python -B tests/race_arbiter.py [N] [THREADS]
"""
import concurrent.futures
import os
import shutil
import sys
import traceback

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.arbiter import Arbiter  # noqa: E402

WD = os.path.join(ROOT, "build", "race")
A = "§1 Let x be 6.\n§2 Say x times 7.\n".encode("utf-8")
B = "§1 Let y be 5.\n§2 Say y plus 1.\n".encode("utf-8")


def one(k):
    try:
        comp, w, ref = Arbiter(WD).arbitrate(A if k % 2 else B, "case")
        if w["build_failed"]:
            return "BUILD-FAILED: " + " ".join(w["mismatch_notes"][0]["detail"][:160].split())
        return w["dissent_kind"]
    except Exception:
        return "TRACEBACK " + traceback.format_exc().splitlines()[-1]


def main(n=48, threads=16):
    shutil.rmtree(WD, ignore_errors=True)
    os.makedirs(WD)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        outcomes = list(ex.map(one, range(n)))
    counts = {}
    for o in outcomes:
        counts[o] = counts.get(o, 0) + 1
    print("%d concurrent arbitrations (%d threads) in one work folder: %s" % (n, threads, counts))
    left = [x for x in os.listdir(WD) if x.startswith("arb-")]
    print("run folders left behind:", len(left))
    return 0 if counts == {"NONE": n} and not left else 1


if __name__ == "__main__":
    sys.exit(main(*[int(x) for x in sys.argv[1:3]]))

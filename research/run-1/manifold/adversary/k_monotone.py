"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

Cut monotonicity, the lemma F1 breaks: on one run, the continuation of an earlier point contains the continuation of a
later one, since the earlier point's continuation passes through the later point. So for a point p before the cut,
K(p) must contain K(cut), or a refusal at p would hold a claim that a refusal at the cut withholds, with the same
completed evaluations (A26 / A27 in k_attacks.txt).

For each random law of k_fuzz.py's generator that refuses, the probe's CutInterp is run with a snapshot of its frames
taken at the entry of each of the last 40 statements before the cut (the statement entered as the top frame, as if it
refused). K of each snapshot is computed by the probe's own `continuation`, and must contain K at the real cut.
Each violation is classified: does the snapshot hold a While frame whose fuel bit is spent? Then the same is run with
F1's repair (k_repairs.continuation_while_free), which must leave no violation.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/k_monotone.py [N] [SEED]
"""
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
sys.path.insert(0, HERE)
import cut0_claims as P                                                   # noqa: E402
from k_fuzz import Gen                                                    # noqa: E402
from k_repairs import continuation_while_free                             # noqa: E402
from orlog.front import compile_bytes                                     # noqa: E402
from orlog.interp import HostStop                                         # noqa: E402
from orlog.syntax import While                                            # noqa: E402

KEEP = 40


class SnapInterp(P.CutInterp):
    def __init__(self, *a, **k):
        P.CutInterp.__init__(self, *a, **k)
        self.snaps = []

    def stmt(self, c, s):
        if self.cut is None:
            # "arm": None added 2026-10-26, the snapshot's one change since the adversary's run: the probe's F3 repair
            # gave every frame an "arm" (the If arm whose condition is judged), and at a statement's entry it is None,
            # as CutInterp itself sets it. Without the key, continuation() raises KeyError on the repaired probe.
            self.snaps.append([dict(f) for f in self.frames] + [{"clause": c, "stmt": s, "more": None, "arm": None}])
            if len(self.snaps) > KEEP:
                self.snaps.pop(0)
        return P.CutInterp.stmt(self, c, s)


def spent_while(frames):
    return any(isinstance(f["stmt"], While) and f["more"] is False for f in frames[:-1])


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    rng = random.Random(seed)
    t0 = time.time()
    laws = points = 0
    viol = {"as it stands": [0, 0, None], "F1 repaired": [0, 0, None]}    # [violations, with a spent While, example]
    for _ in range(n):
        raw = Gen(rng).law()
        comp = compile_bytes(raw)
        if not comp.ok:
            continue
        it = SnapInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=10 ** 5)
        try:
            it.run()
        except HostStop:
            continue
        if it.cut is None or not comp.an.claims:
            continue
        laws += 1
        for label, cont in (("as it stands", P.continuation), ("F1 repaired", continuation_while_free)):
            k_cut = cont(comp.prog, it.cut)
            for snap in it.snaps[:-1]:                    # the last snapshot is the cut's own statement
                if label == "as it stands":
                    points += 1
                missing = k_cut - cont(comp.prog, snap)
                if missing:
                    v = viol[label]
                    v[0] += 1
                    v[1] += spent_while(snap)
                    if v[2] is None or len(raw) < len(v[2][0]):
                        v[2] = (raw, P.descriptor(snap), P.descriptor(it.cut), sorted(missing))
    print("== cut monotonicity over %d random refusing laws, seed %d, %d earlier points (%.0f s)" % (
        laws, seed, points, time.time() - t0))
    for label, (count, spent, ex) in viol.items():
        print("   %s: %d points whose K misses part of K at the cut; with a spent While bit in the point's frames: %d"
              % (label, count, spent))
        if ex:
            raw, d1, d2, missing = ex
            print("   the shortest: point [%s], cut [%s], claims missing %s\n%s" % (
                d1, d2, missing, "\n".join("      " + l for l in raw.decode("utf-8").split("\n")[:-1])))


if __name__ == "__main__":
    main()

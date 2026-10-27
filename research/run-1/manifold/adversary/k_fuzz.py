"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

Random version-0 laws against CUT-0's K. Each law that compiles and refuses is read by the probe's `judge()` and run
through the dynamic continuation oracle (cont_oracle.py, written apart from K). A claim the cut rule holds that some
continuation evaluates again is a counterexample under that continuation's semantics:

  S1, one return: a counterexample is a defect of K's implementation (K is meant to contain S1's continuation);
  S2, every refusal returns: a counterexample shows where K honours a later guard (expected: only a While frame whose
      fuel bit is spent, finding F1); any other is a new defect.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/k_fuzz.py [N] [SEED]

The generator covers: rules (Define with a proviso), Musts, If / Otherwise, if / Otherwise chains (block and inline),
inline Perform, inline claims in both arms of one clause, procedures performed from loops and from other procedures,
For loops with expression and refusing bounds, While loops with refusing conditions and small fuel.
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
from cont_oracle import witnesses                                         # noqa: E402
from orlog.front import compile_bytes                                     # noqa: E402
from orlog.interp import HostStop, Interp                                 # noqa: E402
from orlog.syntax import While                                            # noqa: E402


class Gen:
    def __init__(self, rng):
        self.r = rng
        self.loops = 0
        self.procs = []

    def k(self, lo=0, hi=4):
        return str(self.r.randint(lo, hi))

    def cond(self, lv):
        c = ["x is less than %s" % self.k(1, 4), "x equals %s" % self.k(), "y is even", "item x of xs equals 1",
             "item y of xs equals 1", "r is positive", "the quotient of 6 by (x minus %s) is positive" % self.k(),
             "y is less than %s" % self.k(1, 4)]
        if lv:
            v = self.r.choice(lv)
            c += ["%s equals %s" % (v, self.k(1, 3)), "item %s of xs equals 1" % v]
        return self.r.choice(c)

    def claim(self, lv):
        c = ["x is at least 0", "y is at least 0", "item x of xs equals 1", "r is positive",
             "x is at most %s" % self.k(1, 4), "y is at most %s" % self.k(1, 4)]
        if lv:
            c += ["%s is positive" % self.r.choice(lv)]
        return "we claim that %s" % self.r.choice(c)

    def risky(self, lv):
        c = ["the quotient of 6 by (x minus %s)" % self.k(), "item x of xs", "item y of xs", "r", "x"]
        if lv:
            c += ["item %s of xs" % self.r.choice(lv)]
        return self.r.choice(c)

    def inline(self, lv):
        c = [self.claim(lv), self.claim(lv), "increase x by 1", "increase y by 1", "say %s" % self.risky(lv),
             "it must hold that %s" % self.cond(lv)]
        if self.procs:
            c += ["perform %s" % self.r.choice(self.procs)] * 2
        return self.r.choice(c)

    def stmts(self, lv, depth, n):
        out = []
        for _ in range(n):
            out += self.stmt(lv, depth)
        return out

    def body(self, lv, depth):
        return self.stmts(lv, depth + 1, self.r.randint(1, 3))

    def stmt(self, lv, depth):
        r = self.r.random()
        if depth >= 3 or r < 0.40:
            s = self.inline(lv)
            return [(s[0].upper() + s[1:] + ".", [])]
        if r < 0.55:
            a = "If %s, %s" % (self.cond(lv), self.inline(lv))
            if self.r.random() < 0.4:
                a += "; otherwise, %s" % self.inline(lv)
            return [(a + ".", [])]
        if r < 0.70:
            out = [("If %s, do the following." % self.cond(lv), self.body(lv, depth))]
            if self.r.random() < 0.5:
                if self.r.random() < 0.5:
                    out.append(("Otherwise, if %s, do the following." % self.cond(lv), self.body(lv, depth)))
                else:
                    out.append(("Otherwise, if %s, %s." % (self.cond(lv), self.inline(lv)), []))
            if self.r.random() < 0.5:
                if self.r.random() < 0.5:
                    out.append(("Otherwise, do the following.", self.body(lv, depth)))
                else:
                    out.append(("Otherwise, %s." % self.inline(lv), []))
            return out
        if r < 0.85:
            self.loops += 1
            v = "i%d" % self.loops
            lo = self.r.choice(["1", "1", "x", "y"])
            hi = self.r.choice(["1", "2", "3", "x plus 1", "y", "the quotient of 6 by (x minus %s)" % self.k(),
                                "item x of xs"] + (["item %s of xs" % lv[-1]] if lv else []))
            return [("For each %s from %s to %s, do the following." % (v, lo, hi), self.body(lv + [v], depth))]
        if r < 0.95:
            return [("While %s, at most %s times, do the following." % (self.cond(lv), self.k(1, 4)),
                     self.body(lv, depth))]
        if self.procs:
            return [("Perform %s." % self.r.choice(self.procs), [])]
        return [("Increase x by 1.", [])]

    def law(self):
        top = [("Let xs be a list of %s copies of 1." % self.k(1, 4), []), ("Let x be %s." % self.k(0, 3), []),
               ("Let y be %s." % self.k(0, 3), []),
               ("Define r as x plus 1, provided that x is less than %s." % self.k(1, 5), [])]
        for j in range(self.r.randint(0, 3)):
            name = "p%d" % (j + 1)
            top.append(("To %s, do the following." % name, self.stmts([], 1, self.r.randint(1, 3))))
            self.procs.append(name)
        top += self.stmts([], 0, self.r.randint(1, 4))
        lines = []

        def emit(nodes, prefix):
            for i, (text, kids) in enumerate(nodes, 1):
                lab = "%s%d" % (prefix, i)
                lines.append("§%s %s" % (lab, text))
                emit(kids, lab + ".")
        emit(top, "")
        return ("".join(l + "\n" for l in lines)).encode("utf-8")


def while_spent(comp):
    """Whether the cut holds a While frame whose fuel bit is spent (more False), read from the probe's own CutInterp."""
    it = P.CutInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=10 ** 5).run()
    return any(isinstance(f["stmt"], While) and f["more"] is False for f in (it.cut or []))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261026
    rng = random.Random(seed)
    t0 = time.time()
    stats = {"generated": 0, "compiled": 0, "refused": 0, "stopped": 0, "completed": 0, "claims judged": 0,
             "held by the cut": 0, "withheld by the cut (done)": 0}
    errors = {}
    s1_bad, s2_bad, s2_other, crash, imprecise = [], [], [], [], 0
    for _ in range(n):
        g = Gen(rng)
        raw = g.law()
        stats["generated"] += 1
        comp = compile_bytes(raw)
        if not comp.ok:
            code = str(comp.error).split(" ")[0]
            errors[code] = errors.get(code, 0) + 1
            continue
        stats["compiled"] += 1
        try:
            it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=10 ** 5).run()
        except HostStop:
            stats["stopped"] += 1
            continue
        if not it.status.startswith("REFUSED") or not comp.an.claims:
            stats["completed"] += 1
            continue
        stats["refused"] += 1
        try:
            status, out, desc = P.judge(raw, 10 ** 5)
        except Exception as e:                              # the probe itself failing is a finding
            crash.append((raw, repr(e)))
            continue
        wit = witnesses(comp)
        cut_frames = None
        for k, (lab, ev, built, site, cut, done) in out.items():
            stats["claims judged"] += 1
            stats["held by the cut"] += cut
            stats["withheld by the cut (done)"] += done and not cut
            if done and not cut and k not in wit["S1"] and k not in wit["S2"]:
                imprecise += 1
            if cut and k in wit["S1"]:
                s1_bad.append((raw, desc, lab))
            elif cut and k in wit["S2"]:
                (s2_bad if while_spent(comp) else s2_other).append((raw, desc, lab))
    print("== %d random version-0 laws, seed %d (%.0f s)" % (n, seed, time.time() - t0))
    for k, v in stats.items():
        print("   %-28s %d" % (k, v))
    print("   compile refusals by code: %s" % ", ".join("%s %d" % kv for kv in sorted(errors.items())))
    print("== held by the cut, yet evaluated again by a one-return (S1) continuation: %d" % len(s1_bad))
    for raw, desc, lab in s1_bad[:5]:
        print("   cut [%s] claim %s\n%s" % (desc, lab, raw.decode("utf-8")))
    print("== held by the cut, evaluated again only by an every-return (S2) continuation, a spent loop bit in the cut: "
          "%d" % len(s2_bad))
    if s2_bad:
        raw, desc, lab = min(s2_bad, key=lambda x: len(x[0]))
        print("   the shortest: cut [%s] claim %s\n%s" % (desc, lab, raw.decode("utf-8")))
    print("== the same, with no spent loop bit in the cut (a defect other than F1): %d" % len(s2_other))
    for raw, desc, lab in s2_other[:5]:
        print("   cut [%s] claim %s\n%s" % (desc, lab, raw.decode("utf-8")))
    print("== the probe raised: %d" % len(crash))
    for raw, e in crash[:3]:
        print("   %s\n%s" % (e, raw.decode("utf-8")))
    print("== withheld by the cut with every evaluation true, no tried continuation reaching it (candidates): %d"
          % imprecise)
    print("K-FUZZ: S1 counterexamples %d; S2 counterexamples %d (spent bit %d, other %d); probe crashes %d" % (
        len(s1_bad), len(s2_bad) + len(s2_other), len(s2_bad), len(s2_other), len(crash)))


if __name__ == "__main__":
    main()

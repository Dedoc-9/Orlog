"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

F5: the probe's acceptance arithmetic (research/run-1/probes/cut0_claims.py, main: `gained`, `r8`, `r8_cut`, and
`ok = ... gained == 0 and r8_cut == r8 ...`) applied, line for line, to this adversary's A23 and A23' (two claims on
one clause), whose cut-rule readings the dynamic continuation oracle confirms (k_attacks.txt).

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/k_criteria.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
sys.path.insert(0, HERE)
import cut0_claims as P                                                   # noqa: E402
import k_attacks as A                                                     # noqa: E402

cases = {n.split(" ")[0]: l for n, l in A.CASES}
for key in ("A23", "A23'"):
    status, out, desc = P.judge(P.law(*cases[key]))
    gained = r8 = r8_cut = 0
    for lab, ev, built, site, cut, done in out.values():         # the probe's own accumulation, lines 356-363
        r8 += done and not built
        r8_cut += done and not built and not cut
        gained += cut and not built
    print("%s cut [%s]: gained %d (the probe requires 0); R8's class %d, withheld by the cut %d (the probe requires "
          "equal): the probe's verdict on a corpus holding this law would be %s" % (
              key, desc, gained, r8, r8_cut, "HELD" if gained == 0 and r8 == r8_cut else "FAILED"))

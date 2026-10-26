"""A certificate's cost reading over an evaluation that refused.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/cost_over_refusal.py

The receipt's claim line counts a claim's cost only when its evaluation finishes (interp.py, Claim: `acc[2] += cost`
after the condition returns). R8 names the evaluation that refused and withholds the claim; the court still prints
the cost line and the CHEAPER / NOT CHEAPER reading from the finished evaluations alone.

The text: a certificate claim of a loop §3, evaluated in a loop to 17 over a 16-item list, so its 17th evaluation
refuses inside its condition (DP-5's shape). An instrumented reference counts the operations the claim's evaluations
spent, the refused one included. The loop's length N is searched for a law where counting the refused evaluation
moves the reading across the 1/2 line; the reading the court prints is set beside the one the operations spent give.
"""
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import parse_receipt  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp, Stop  # noqa: E402
from orlog.syntax import Claim  # noqa: E402

TEXT = ("Note: a certificate claim whose 17th evaluation refuses inside its condition.\n"
        "§1 Let xs be a list of 16 copies of 1.\n§2 Let s be 0.\n§3 For each j from 1 to %d, do the following.\n"
        "§3.1 Increase s by j.\n§4 For each i from 1 to 17, do the following.\n"
        "§4.1 We claim that s is positive and item i of xs equals 1, by the certificate of §3.\n")


class Counting(Interp):
    """The reference, counting every operation spent inside a claim's condition, finished or not."""
    spent = 0

    def stmt(self, c, s):
        if not isinstance(s, Claim):
            return Interp.stmt(self, c, s)
        start = self.ops + 1          # the claim's own statement count, as interp.py's `start`
        try:
            return Interp.stmt(self, c, s)
        finally:
            self.spent += self.ops - start


def reading(cost, ref_cost):
    if ref_cost == 0:
        return "CLAUSE NOT RUN"
    return "CHEAPER" if cost * COURT.CHEAP_RATIO[1] <= ref_cost * COURT.CHEAP_RATIO[0] else "NOT CHEAPER"


def main():
    shown = None
    for n in range(1, 200):
        raw = (TEXT % n).encode("utf-8")
        comp = compile_bytes(raw)
        it = Counting(comp.prog, comp.an, comp.law_seal, comp.text_seal)
        try:
            it.run()
        except Stop:
            pass
        rec = parse_receipt(it.receipt())
        line = [l for l in rec if l.startswith("claim ")][0].split(" ")
        cost, ref_cost = int(line[5]), int(line[7])
        if reading(cost, ref_cost) != reading(it.spent, ref_cost):
            shown = (n, comp, rec, cost, ref_cost, it.spent, it.status)
            break
    if shown is None:
        print("no loop length up to 199 moves the reading; the undercount is still the refused evaluation's cost")
        return 0
    n, comp, rec, cost, ref_cost, spent, status = shown
    p = COURT.panel(comp, {"dissent_kind": "NONE", "backends": {"reference": {}}}, rec, [])
    r = p["rows"][0]
    print("loop length %d; reference %s" % (n, status))
    print("   evaluation   %s" % r["evaluation"])
    print("   cost         %s" % r["cost"])
    print("   cost_reading %s" % r["cost_reading"])
    print("   the claim's evaluations spent %d counted operations, the refused one included (the line says %d); "
          "with them the reading is %s" % (spent, cost, reading(spent, ref_cost)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

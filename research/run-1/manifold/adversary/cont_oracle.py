"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

A dynamic continuation oracle for CUT-0, written apart from research/run-1/probes/cut0_claims.py's `continuation`.
It does not compute K. It runs version 0's reference interpreter to its first refusal and then, instead of stopping,
lets the refusing operation return a substitute value and runs on, counting the claims whose evaluation completes
after the cut. Two semantics for what follows the cut:

  S1: the first refusal returns; any later refusal stops the run (one return only);
  S2: every refusal returns (the run continues past every guard), bounded by a step budget.

Each substitute value gives one real continuation, so the oracle UNDER-approximates the set of continuations: a claim
it sees evaluated after the cut is a witness that the run could still evaluate it (under S1 or S2), and a claim that
CUT-0 holds while the oracle sees it evaluated is a counterexample to K's over-approximation under that semantics.
It cannot prove K precise or sound; it can only refute.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog import numeric_ref as N                                       # noqa: E402
from orlog.interp import HostStop, Interp, Stop                          # noqa: E402
from orlog.syntax import Item, ListOf, RemoveLast, SetS, Change          # noqa: E402

# Substitute values a refused operation may return. Small integers steer `equals`/`less than` both ways; 1 << 32 is
# one in fixed point; a float is made from the same integer when an argument is a float.
SUBS = (0, 1, 2, 3, -1, 5, 1 << 32)


class ContInterp(Interp):
    def __init__(self, *a, mode="S1", sub=0, after_budget=20000, **k):
        Interp.__init__(self, *a, **k)
        self.mode, self.sub, self.after_budget = mode, sub, after_budget
        self.cut_taken = False
        self.at_cut = None              # claim evaluation counts at the cut
        self.cut_code = None

    # every refusal goes through here
    def refuse(self, code, clause):
        if self.cut_taken and self.mode == "S1":
            Interp.refuse(self, code, clause)          # a second refusal stops the run (S1)
        self.ev(b"R", clause, code.encode("ascii"))
        if not self.cut_taken:
            self.cut_taken = True
            self.cut_code = (code, clause)
            self.at_cut = [list(c) for c in self.claims]
            self.budget = self.ops + self.after_budget  # bound the continuation (S2 may loop)
        return None                                     # the refusing operation returns

    def subst(self, args=(), typ=None):
        if typ == "float" or any(isinstance(a, float) for a in args):
            return float(self.sub)
        if typ == "bool":
            return bool(self.sub & 1)
        if typ == "text":
            return b""
        if isinstance(typ, tuple):
            return []
        return int(self.sub)

    def num(self, fn, clause, *args):
        try:
            return fn(*args)
        except N.Refusal as r:
            self.refuse(r.code, clause)
            return self.subst(args)

    def eval(self, cid, e):
        if isinstance(e, Item):
            k = self.eval(cid, e.index)
            self.ops += 1
            lst = self.env[e.var.id]
            if not 1 <= k <= len(lst):
                self.refuse("INDEX-OUT-OF-RANGE", cid)
                return self.subst(typ=e.type)
            return lst[k - 1]
        if isinstance(e, ListOf):
            n = self.eval(cid, e.count)
            v = self.eval(cid, e.value)
            self.ops += 1
            if n < 0:
                self.refuse("NEGATIVE-LENGTH", cid)
                return []
            if n > N.LIST_MAX:
                self.refuse("LIST-TOO-LONG", cid)
                return [v] * 4
            return [v] * n
        return Interp.eval(self, cid, e)

    def convert(self, mode, target, src, a, cid):
        try:
            return Interp.convert(self, mode, target, src, a, cid)
        except (OverflowError, ValueError, TypeError):
            return self.subst(typ=target)

    def rule(self, cid, name):
        self.ops += 1
        clauses = self.an.rules[name]
        beats = self.an.overrides[name]
        applicable = []
        for c in clauses:
            d = c.stmt
            if d.proviso is None or self.eval(cid, d.proviso):
                applicable.append(c)
        ids = set(c.id for c in applicable)
        maximal = [c for c in applicable if not any(c.id in beats[o] for o in ids if o != c.id)]
        if not maximal:
            self.refuse("RULE-UNDEFINED", cid)
            return self.subst(typ=self.an.rule_types.get(name))
        vals = [self.eval(cid, c.stmt.expr) for c in maximal]
        for v in vals[1:]:
            if not (v == vals[0]):
                self.refuse("RULE-CONFLICT", cid)
                return vals[0]
        return vals[0]

    def stmt(self, c, s):
        if isinstance(s, (SetS, Change, RemoveLast)):
            try:
                return Interp.stmt(self, c, s)
            except IndexError:
                if not self.cut_taken:
                    raise
                return None                              # the refused store or removal is skipped
        return Interp.stmt(self, c, s)

    def evaluated_after_cut(self):
        """Claim ids whose evaluation completed after the cut (the open one included, if it completed)."""
        if self.at_cut is None:
            return set()
        return {i for i, (now, then) in enumerate(zip(self.claims, self.at_cut)) if now[0] > then[0]}

    def refuted_after_cut(self):
        """Claim ids with an evaluation after the cut that read false."""
        if self.at_cut is None:
            return set()
        return {i for i, (now, then) in enumerate(zip(self.claims, self.at_cut))
                if now[0] - then[0] > now[1] - then[1]}


def continue_after(comp, mode, sub, budget=10 ** 6):
    """Run to the first refusal, return the substitute, continue under mode; the set of claims evaluated after."""
    it = ContInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget, mode=mode, sub=sub)
    try:
        it.seq(it.prog.top)
    except Stop:
        pass
    except HostStop:
        pass
    except RecursionError:
        pass
    return it.cut_code, it.evaluated_after_cut(), it.refuted_after_cut()


def witnesses(comp, modes=("S1", "S2"), refuted=False):
    """{mode: set of claim ids some substitute's continuation evaluated again after the cut}; with refuted=True also
    {mode + '-refuted': the ids some continuation evaluated again and found false}."""
    out = {}
    for m in modes:
        seen, false = set(), set()
        for sub in SUBS:
            _, ev, rf = continue_after(comp, m, sub)
            seen |= ev
            false |= rf
        out[m] = seen
        if refuted:
            out[m + "-refuted"] = false
    return out

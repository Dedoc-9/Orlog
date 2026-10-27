"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

Three checks on research/run-1/probes/cut0_claims.py, each with its plant (the probe as it stands):

1. Instrument fidelity (F4). The probe's CutInterp replaces the reference's For and While and so skips the
   reference's budget check at their entry. Under a host budget the instrumented reference and the reference part.
   The probe's own `equivalence()` is run on three laws with small budgets; it must report them different.
2. The fuel-bit repair (F1). K with every While frame allowed to repeat (the probe's own "no-count" plant restricted
   to While) is run on the probe's 13 cases, on this adversary's A26 / A27 pairs and on the probe's corpus: the cases
   must read as the probe requires, A26 and A27 must be withheld, and the cost on the corpus is counted.
3. The descriptor repair (F2). The open mark carries the claim's id: A23 and A23' must then differ.
4. The instrument repair (F4): CutInterp checks the budget at a For's and a While's entry, as the reference does.
5. The If-arm repair (F3): the cut records which arm's condition refused, and K takes that arm and the arms after it
   (and the Otherwise), not the arms whose conditions already read false. Every claim it gains is put to the dynamic
   continuation oracle (cont_oracle.py), which must not see it evaluated again.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/k_repairs.py
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
from orlog.front import compile_bytes                                     # noqa: E402
from orlog.interp import HostStop, Interp                                 # noqa: E402
from orlog.syntax import Claim, For, IfS, While                          # noqa: E402
from cont_oracle import witnesses                                         # noqa: E402

ORIGINAL = P.continuation
BASE = P.CutInterp


def continuation_while_free(prog, cut):
    """F1's repair: a While frame below the top may always repeat (its condition is unknown, and a FUEL-EXHAUSTED
    refusal in the continuation is passed exactly as the C6 repair passes it at the top). For frames keep their bit."""
    patched = [dict(f, more=True) if isinstance(f["stmt"], While) else f for f in cut]
    return ORIGINAL(prog, patched)


def descriptor_with_ids(cut):
    out = []
    for f in cut:
        st = f["stmt"]
        tag = "%s" % f["clause"].label
        if isinstance(st, (For, While)):
            tag += "+" if f["more"] else "."
        elif isinstance(st, Claim):
            tag += "!%d" % st.id
        out.append(tag)
    return " ".join(out)


def fidelity():
    laws = [
        ("an empty For at the end, budget 0", P.law("S1 Let x be 1.", "S2 For each i from 2 to 1, do the following.",
                                                    "S2.1 Say i."), 0),
        ("a For with a body, budget 0", P.law("S1 Let x be 1.", "S2 For each i from 1 to 2, do the following.",
                                              "S2.1 Say i."), 0),
        ("a While with a body, budget 0", P.law("S1 Let x be 1.", "S2 While x is less than 3, at most 5 times, do the "
                                                "following.", "S2.1 Increase x by 1."), 0),
    ]
    print("== 1. the instrumented reference against the reference under a host budget (the probe's equivalence())")
    for name, raw, budget in laws:
        rows = []
        for cls in (Interp, P.CutInterp):
            it = cls(*(lambda c: (c.prog, c.an, c.law_seal, c.text_seal))(compile_bytes(raw)), trace=True,
                     budget=budget)
            try:
                it.run()
                rows.append("%s: %s, %d events" % (cls.__name__, it.status, it.events))
            except HostStop as h:
                rows.append("%s: STOPPED-BY-HOST after %d ops, %d events" % (cls.__name__, h.ops, it.events))
        n, stopped, differ = P.equivalence([(name, raw, budget)])
        print("   %s\n      %s\n      %s\n      equivalence(): texts %d, stopped alike %d, different %d" % (
            name, rows[0], rows[1], n, stopped, len(differ)))


def reading(raw):
    return tuple(v[4] for _, v in sorted(P.judge(raw)[1].items()))


def per_claim(got, want):
    """Added 2026-10-26, with the two loops that call it: a case of the probe may now require a reading per claim
    (A23 and A23', added after this script was written), and the first claim's reading was compared with the whole
    table, which never matches. Compare claim by claim then, as the probe does; a single requirement keeps the
    comparison as it was, against the first claim."""
    if isinstance(want, dict):
        return got, tuple(want[k] for k in sorted(want))
    return got[0], want


def words(v):
    if isinstance(v, tuple):
        return "/".join("held" if x else "withheld" for x in v)
    return "held" if v else "withheld"


def fuel_repair():
    print("== 2. K with every While frame free to repeat (F1's repair) against the probe as it stands (the plant)")
    bad = 0
    for name, raw, want, _ in P.CASES:
        P.continuation = continuation_while_free
        got = reading(raw)
        P.continuation = ORIGINAL
        got, want = per_claim(got, want)
        ok = got == want
        bad += not ok
        print("   %-6s repaired %s; the probe requires %s %s" % (name.split(" ")[0], words(got), words(want),
                                                                  "" if ok else "<- DIFFERS"))
    cases = {n.split(" ")[0]: l for n, l in A.CASES}
    for key in ("A16", "A26", "A26'", "A27", "A27'"):
        raw = P.law(*cases[key])
        plant = reading(raw)
        P.continuation = continuation_while_free
        fixed = reading(raw)
        P.continuation = ORIGINAL
        print("   %-5s the probe as it stands %s; repaired %s" % (
            key, "held" if plant[0] else "withheld", "held" if fixed[0] else "withheld"))
    lost = n = 0
    rows = []
    for ident, raw, budget in P.corpus():
        comp = compile_bytes(raw)
        if not comp.ok or not comp.an.claims:
            continue
        try:
            a = P.judge(raw, budget)[1]
            P.continuation = continuation_while_free
            b = P.judge(raw, budget)[1]
        except HostStop:
            continue
        finally:
            P.continuation = ORIGINAL
        for k in a:
            n += 1
            if a[k][4] != b[k][4]:
                lost += 1
                rows.append("   %s %s: as it stands %s, repaired %s" % (ident, a[k][0], a[k][4], b[k][4]))
    print("   the corpus: %d claims, %d read differently under the repair%s" % (n, lost,
                                                                             ("\n" + "\n".join(rows)) if rows else ""))
    print("   the probe's 13 cases under the repair: %d differ from what the probe requires" % bad)


def descriptor_repair():
    print("== 3. the descriptor with the open claim's id (F2's repair)")
    cases = {n.split(" ")[0]: l for n, l in A.CASES}
    for key in ("A23", "A23'"):
        raw = P.law(*cases[key])
        comp = compile_bytes(raw)
        it = P.CutInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
        print("   %-5s as specified [%s]; with the id [%s]; readings %s" % (
            key, P.descriptor(it.cut), descriptor_with_ids(it.cut), reading(raw)))


class FaithfulCutInterp(BASE):
    """F4's repair: the reference's budget check at every statement's entry, For and While included."""

    def stmt(self, c, s):
        if isinstance(s, (For, While)) and self.budget is not None and self.ops > self.budget:
            raise HostStop(self.ops, self.budget)
        return BASE.stmt(self, c, s)


class ArmCutInterp(FaithfulCutInterp):
    """F3's instrument: an If frame records the index of the arm whose condition is being evaluated (None once an arm
    or the Otherwise runs). The reference's IfS, replicated, as the probe replicates For and While."""

    def stmt(self, c, s):
        if not isinstance(s, IfS):
            return FaithfulCutInterp.stmt(self, c, s)
        if self.budget is not None and self.ops > self.budget:
            raise HostStop(self.ops, self.budget)
        frame = {"clause": c, "stmt": s, "more": None, "arm": 0}
        self.frames.append(frame)
        try:
            for idx, (cond, b, ac) in enumerate(s.arms):
                frame["arm"] = idx
                self.ops += 1
                if self.eval(ac.id, cond):
                    frame["arm"] = None
                    self.body(ac, b)
                    return
            frame["arm"] = None
            if s.els is not None:
                self.body(s.els[1], s.els[0])
        finally:
            self.frames.pop()


def continuation_arms(prog, cut):
    top = cut[-1]
    if not (isinstance(top["stmt"], IfS) and top.get("arm") is not None):
        return ORIGINAL(prog, cut)
    r = P.Reach(prog)
    s = top["stmt"]
    k = set()
    for _, b, _ in s.arms[top["arm"]:]:
        k |= r.arm(b)
    if s.els is not None:
        k |= r.arm(s.els[0])
    neutral = dict(top, stmt=None)                   # the frames below, as the probe walks them
    return k | ORIGINAL(prog, cut[:-1] + [neutral])


def fidelity_repair():
    print("== 4. the instrument with the budget check at For and While (F4's repair)")
    laws = [P.law("S1 Let x be 1.", "S2 For each i from 2 to 1, do the following.", "S2.1 Say i."),
            P.law("S1 Let x be 1.", "S2 For each i from 1 to 2, do the following.", "S2.1 Say i."),
            P.law("S1 Let x be 1.", "S2 While x is less than 3, at most 5 times, do the following.",
                  "S2.1 Increase x by 1.")]
    saved = P.CutInterp
    P.CutInterp = FaithfulCutInterp
    try:
        n, stopped, differ = P.equivalence([("b%d" % i, raw, 0) for i, raw in enumerate(laws)])
        print("   budget 0, three laws: texts %d, stopped %d, different %d" % (n, stopped, len(differ)))
        n, stopped, differ = P.equivalence(P.corpus())
        print("   the probe's corpus: texts %d, stopped %d, different %d" % (n, stopped, len(differ)))
    finally:
        P.CutInterp = saved


def arm_repair():
    print("== 5. K from the refusing arm onward (F3's repair)")
    cases = {n.split(" ")[0]: l for n, l in A.CASES}
    saved = P.CutInterp

    def both(raw, budget=10 ** 8):
        a = P.judge(raw, budget)[1]
        P.CutInterp, P.continuation = ArmCutInterp, continuation_arms
        try:
            b = P.judge(raw, budget)[1]
        finally:
            P.CutInterp, P.continuation = saved, ORIGINAL
        return a, b
    bad = 0
    for name, raw, want, _ in P.CASES:
        a, b = both(raw)
        got, want = per_claim(tuple(v[4] for _, v in sorted(b.items())), want)
        bad += got != want
    print("   the probe's 13 cases under the repair: %d differ from what the probe requires" % bad)
    for key in ("A08", "A09", "A10", "A20", "A21"):
        raw = P.law(*cases[key])
        a, b = both(raw)
        print("   %-4s as it stands %s; repaired %s" % (key, [v[4] for v in a.values()], [v[4] for v in b.values()]))
    gained, unsound = 0, []
    for ident, raw, budget in P.corpus() + [(k, P.law(*l), 10 ** 8) for k, l in cases.items()]:
        comp = compile_bytes(raw)
        if not comp.ok or not comp.an.claims:
            continue
        try:
            a, b = both(raw, budget)
        except HostStop:
            continue
        g = [k for k in a if b[k][4] and not a[k][4]]
        lost = [k for k in a if a[k][4] and not b[k][4]]
        assert not lost, (ident, lost)
        if g:
            gained += len(g)
            w = witnesses(comp)
            unsound += [(ident, k) for k in g if k in w["S1"] or k in w["S2"]]
    print("   the corpus and this adversary's cases: %d claims gained, %d of them evaluated again by a continuation "
          "(must be 0)%s" % (gained, len(unsound), (": %s" % unsound) if unsound else ""))


if __name__ == "__main__":
    fidelity()
    fuel_repair()
    descriptor_repair()
    fidelity_repair()
    arm_repair()

"""EXPERIMENTAL RESEARCH PROBE. It is not the contract and not the court, and nothing in the program reads it; the
proposal it supports is research/run-1/CUT-0.md, and its output is evidence/run1-cut0-claims.txt.

CUT-0 on version 0: the causal cut captured from the reference itself, and the claim rule it gives, against the
site-based rule of CONTRACT-DRAFT.md §8.4 (research/run-1/probes/completeness_probe.py).

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/cut0_claims.py

The cut is the run's dynamic position when it refuses: the stack of statements executing; each For with whether
passes remain; each If whose condition refused with which arm's condition it was; and the claim whose evaluation was
open, by its id. Its continuation K is everything the run could still have executed had the refusing operation
returned, **with every later refusal also read as passable (reading S2)**: values are unknown, refusals are ignored,
and only a loop's normal exit is exact (a For's counter against its bound). The rule:

  a claim is held when every completed evaluation is true, it is not open at the cut, and K cannot evaluate it.

K is over-approximated from the frames outward:
- the rest of each frame's block;
- a For's next passes when its frame says passes remain;
- a While's next passes always (its fuel check is a refusal, so S2 passes it);
- an If whose condition refused, from the refused arm onward;
- a procedure's body when K performs it;
- a return only to the frame below (the actual caller).

The first form held a claim behind a spent While's fuel. Found by the manifold debate's adversary on 2026-10-26
(research/run-1/manifold/ADVERSARY.md, F1), it read lower While frames as stopping at the fuel check and the top one
as passing it. Reading S2 is the one consistent repair, and a refusal caused by an input can no longer raise a
claim's standing.

Research code: a subclass of the reference that records frames and replicates For, While and If exactly, the
reference's host-budget check included. Every receipt, trace and host stop it gives is checked against the unmodified
reference's, at the texts' own budgets and at budgets that stop them part-way. Nothing in the program reads it.
"""
import base64
import gzip
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
import completeness_probe as SITE                               # noqa: E402
from orlog.front import compile_bytes                           # noqa: E402
from orlog.interp import HostStop, Interp, enc_value            # noqa: E402
from orlog.syntax import BLOCK, Claim, Define, Decimals, For, IfS, Perform, ProcDef, While  # noqa: E402

PLANT = None
# Plants, each caught by its own cases:
#   "context-free"      a procedure's end returns after every Perform of it (the site rule's return)
#   "no-count"          a For always may repeat, its counter ignored
#   "no-open"           an open evaluation is not seen
#   "header-bit"        a loop whose own clause refused re-enters only if its bit says passes remain (the first C6 defect)
#   "while-bit"         a While below the top repeats only if fuel remains (reading S1 below the top: F1)
#   "all-arms"          an If whose condition refused may run any arm, those already read false included (F3)
#   "descriptor-no-id"  the cut's open-claim mark names the clause, not the claim (F2)
#   "no-entry-check"    the instrumented reference skips the host-budget check at a loop's or an If's entry (F4)
#   "shallow-reach"     K stops at a Perform inside a procedure: an under-approximation cut at a depth (LINEAGE.md)


class CutInterp(Interp):
    def __init__(self, *a, **k):
        Interp.__init__(self, *a, **k)
        self.frames, self.cut = [], None

    def refuse(self, code, clause):
        if self.cut is None:
            self.cut = [dict(f) for f in self.frames]
        Interp.refuse(self, code, clause)

    def stmt(self, c, s):
        if PLANT != "no-entry-check" and self.budget is not None and self.ops > self.budget:
            raise HostStop(self.ops, self.budget)                # the reference's check at every statement's entry
        frame = {"clause": c, "stmt": s, "more": None, "arm": None}
        self.frames.append(frame)
        try:
            if isinstance(s, For):              # the reference's For, with the frame told whether passes remain
                self.ops += 1
                lo = self.eval(c.id, s.lo)
                hi = self.eval(c.id, s.hi)
                k = lo
                frame["more"] = k < hi
                while k <= hi:
                    self.ops += 1
                    self.env[s.var.id] = k
                    self.ev(b"A", c.id, struct.pack(">I", s.var.id) + enc_value(k, "int"))
                    frame["more"] = k < hi
                    self.seq(c.children)
                    if k == hi:
                        break
                    k += 1
            elif isinstance(s, While):          # the reference's While, with the frame told whether fuel remains
                n = 0
                frame["more"] = True
                while True:
                    self.ops += 1
                    if not self.eval(c.id, s.cond):
                        break
                    if n == s.fuel:
                        self.refuse("FUEL-EXHAUSTED", c.id)
                    n += 1
                    frame["more"] = n < s.fuel
                    self.seq(c.children)
            elif isinstance(s, IfS):            # the reference's If chain, with the frame told which arm is judged
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
            else:
                Interp.stmt(self, c, s)
        finally:
            self.frames.pop()


class Reach:
    """What a sequence of clauses may execute, as claim ids, without leaving it (static, values ignored)."""

    def __init__(self, prog):
        self.prog, self.memo = prog, {}
        self.procs = {c.stmt.name: c for c in prog.top if isinstance(c.stmt, ProcDef)}
        self.depth = 0

    def proc(self, name):
        if name not in self.memo:
            self.memo[name] = set()
            self.depth += 1
            self.memo[name] = self.seq(self.procs[name].children)
            self.depth -= 1
        return self.memo[name]

    def inline(self, b):
        if isinstance(b, Claim):
            return {b.id}
        if isinstance(b, Perform):
            if PLANT == "shallow-reach" and self.depth > 0:
                return set()                       # the plant: a Perform inside a procedure is not followed
            return self.proc(b.name)
        return set()

    def arm(self, b):
        return self.seq(b[1].children) if isinstance(b, tuple) and b[0] == BLOCK else self.inline(b)

    def arms_from(self, st, first):
        out = set()
        for _, b, _ in st.arms[first:]:
            out |= self.arm(b)
        if st.els is not None:
            out |= self.arm(st.els[0])
        return out

    def stmt(self, x):
        st = x.stmt
        if isinstance(st, (ProcDef, Define, Decimals)):
            return set()
        if isinstance(st, (For, While)):
            return self.seq(x.children)
        if isinstance(st, IfS):
            return self.arms_from(st, 0)
        return self.inline(st)

    def seq(self, clauses):
        out = set()
        for x in clauses:
            if not x.absorbed:
                out |= self.stmt(x)
        return out

    def after(self, x):
        """The rest of x's block after x, the If chain x heads skipped as a unit."""
        sib = x.parent.children if x.parent is not None else self.prog.top
        return self.seq(sib[sib.index(x) + 1:])


def may_repeat(frame):
    """Under reading S2: a For repeats only while passes remain (its normal exit is exact); a While always may (its
    condition is unknown and its fuel check, a refusal, is passable)."""
    if isinstance(frame["stmt"], For):
        return PLANT == "no-count" or bool(frame["more"])
    if PLANT == "while-bit":
        return bool(frame["more"])
    return True


def continuation(prog, cut):
    """Claim ids the run could still evaluate, the open one included, from the cut's frames (outermost first)."""
    r = Reach(prog)
    top = cut[-1]
    s = top["stmt"]
    k = set()
    if isinstance(s, Claim) and PLANT != "no-open":
        k.add(s.id)                                               # the claim's own evaluation is open
    elif isinstance(s, IfS):                                     # a condition refused: that arm onward may still run
        k |= r.arms_from(s, 0 if PLANT == "all-arms" or top["arm"] is None else top["arm"])
    elif isinstance(s, (For, While)) and (PLANT != "header-bit" or top["more"] is not False):
        # the loop's own clause refused (its bounds, its condition, its fuel check): had the refusing operation
        # returned, the next thing it guards is a pass of the body
        k |= r.seq(top["clause"].children)
    elif isinstance(s, Perform):
        k |= r.proc(s.name)                                       # a Perform's own operation refused: its body was next
    for i in range(len(cut) - 1, -1, -1):
        c = cut[i]["clause"]
        outer = cut[i - 1] if i > 0 else None
        if outer is not None and outer["clause"] is c:
            continue                                              # an inline statement of the frame below
        k |= r.after(c)
        if outer is None:
            break
        if isinstance(outer["stmt"], (For, While)) and may_repeat(outer):
            k |= r.seq(outer["clause"].children)
        if PLANT == "context-free" and isinstance(outer["stmt"], Perform):
            for site in [x for x in prog.clauses if isinstance(x.stmt, Perform) and x.stmt.name == outer["stmt"].name]:
                k |= r.after(site) | r.proc(outer["stmt"].name)
    return k


def descriptor(cut):
    """The cut as the court would need it, and no more: each frame's clause; a For's bit (+ passes remain, . none); a
    While as w (S2 needs no bit); the If arm whose condition refused (?n); the open claim by its id (!n)."""
    out = []
    for f in cut:
        st = f["stmt"]
        tag = "%s" % f["clause"].label
        if isinstance(st, For):
            tag += "+" if f["more"] else "."
        elif isinstance(st, While):
            tag += "w"
        elif isinstance(st, IfS) and f["arm"] is not None:
            tag += "?%d" % f["arm"]
        elif isinstance(st, Claim):
            tag += "!" if PLANT == "descriptor-no-id" else "!%d" % st.id
        out.append(tag)
    return " ".join(out)


def judge(raw, budget=10 ** 8):
    """(status, {claim id: (label, evaluation, as built, site rule, cut rule, completed all true)}, descriptor)."""
    comp = compile_bytes(raw)
    assert comp.ok, comp.error
    plain = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
    it = CutInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
    assert it.receipt() == plain.receipt(), "the instrumented reference wrote another receipt"
    lines = SITE.parse_receipt(it.receipt("reference"))
    status, site, rows = SITE.readings(comp, lines)
    k = continuation(comp.prog, it.cut) if it.cut is not None else set()
    done = {}                                    # the completed evaluations, from the receipt: R8 is not consulted
    for l in lines:
        if l.startswith("claim "):
            p = l.split(" ")
            done[int(p[1])] = int(p[3]) > 0 and int(p[3]) == int(p[4])
    out = {}
    for cs in comp.an.claims:
        i = cs.stmt.id
        built, site_held = site[i][0], site[i][1]
        out[i] = (rows[i]["clause"], rows[i]["evaluation"], built, site_held, done.get(i, False) and i not in k,
                  done.get(i, False))
    return status, out, descriptor(it.cut) if it.cut else "-"


def law(*lines):
    """A law from lines whose leading S stands for the section sign."""
    return "".join(("§" + l[1:] if l.startswith("S") else l) + "\n" for l in lines).encode("utf-8")


PROC = ["S1 Let xs be a list of 1 copies of 5.", "S2 Let n be {n0}.", "S3 To check, do the following.",
        "S3.1 Increase n by 1.", "S3.2 We claim that n is positive, by the owner.", "S3.3 Let y be item n of xs.",
        "S4 Perform check.", "S5 Perform check."]
NESTED = ["S1 Let xs be a list of 1 copies of 5.", "S2 Let n be {n0}.", "S3 To inner, do the following.",
          "S3.1 Increase n by 1.", "S3.2 We claim that n is positive, by the owner.", "S3.3 Let y be item n of xs.",
          "S4 To outer, do the following.", "S4.1 Perform inner.", "S4.2 Perform inner.", "S5 Perform outer."]
LOOP = ["S1 Let xs be a list of {m} copies of 1.", "S2 For each i from 1 to 20, do the following.",
        "S2.1 We claim that i is positive, by the owner.", "S2.2 Let y be item i of xs."]
OPEN = ["S1 Let xs be a list of 1 copies of 1.", "S2 For each i from 1 to 2, do the following.",
        "S2.1 We claim that item i of xs equals 1, by the owner."]
BRANCH = ["S1 Let xs be a list of {m} copies of 1.", "S2 For each i from 1 to 20, do the following.",
          "S2.1 If i is 1, we claim that i is positive, by the owner.", "S2.2 Let y be item i of xs."]
FUEL = ["S1 Let i be 0.", "S2 While i is less than 10, at most 3 times, do the following.", "S2.1 Increase i by 1.",
        "S2.2 We claim that i is positive, by the owner."]
# The Round D adversary's version-0 fixtures (research/run-1/ADVERSARY-ROUND-D.md, Findings 21 and 22 and case (v)), and
# the manifold adversary's (research/run-1/manifold/ADVERSARY.md: F1, F2's A23, F3's A09), inlined so that this probe
# reads nothing under work/, which git ignores.
D02 = ["S1 Let i be 0.", "S2 While i is less than 5, at most 10 times, do the following.", "S2.1 Increase i by 1.",
       "S2.2 We claim that i is positive.", "S2.3 If i equals 3, say i divided by 0."]
D03 = ["S1 Let x be 2.", "S2 To step, do the following.", "S2.1 Say 10 divided by (x minus 1).", "S3 Perform step.",
       "S4 We claim that x equals 2.", "S5 Set x to 1.", "S6 Perform step."]
D08 = ["S1 Let i be 0.", "S2 While i is less than 5, at most 10 times, do the following.", "S2.1 Increase i by 1.",
       "S2.2 If i equals 1, we claim that i is positive.", "S2.3 If i equals 3, say i divided by 0."]
D11 = ["S1 Let x be 0.", "S2 To probe, do the following.", "S2.1 If x is positive, do the following.",
       "S2.1.1 Say 1 divided by (x minus 1).", "S2.2 Otherwise, do the following.", "S2.2.1 We claim that x is zero.",
       "S3 Perform probe.", "S4 Set x to 1.", "S5 Perform probe."]
F1 = ["S1 Let i be 0.", "S2 Let d be {d}.", "S3 While i is less than 10, at most 3 times, do the following.",
      "S3.1 Increase i by 1.", "S3.2 We claim that i is at most 3, by the owner.", "S3.3 If i equals 3, say 1 divided by d."]
A23 = ["S1 Let xs be a list of 2 copies of 1.", "S2 Let c be {c}.", "S3 For each i from 1 to 3, do the following.",
       "S3.1 If (i equals 1) equals c, we claim that item i of xs equals 1; otherwise, we claim that item i of xs "
       "equals 1."]
A09 = ["S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
       "S2.1 If i equals 2, we claim that i is positive.", "S2.2 Otherwise, if item i of xs equals 1, say 0.",
       "S2.3 Otherwise, say 1."]
F4 = ["S1 Let a be 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1.",
      "S2 While a is less than 0, at most 3 times, do the following.", "S2.1 Say a."]
# From the lineage report (research/run-1/manifold/LINEAGE.md): the owner's earlier designs hold reaches cut at a depth
# (Dentatus's depth-6 frontier, Ursprung's exactly-H walk), and none of the plants above under-approximates K that way.
# The claim is reachable from the refusal only through a procedure performed inside another.
L1 = ["S1 Let xs be a list of 1 copies of 1.", "S2 Let n be 0.", "S3 To inner, do the following.",
      "S3.1 We claim that n is at most 1, by the owner.", "S4 To outer, do the following.", "S4.1 Perform inner.",
      "S5 Perform outer.", "S6 Increase n by 2.", "S7 Let y be item n of xs.", "S8 Perform outer."]

# (name, law, what the cut rule must read: one bool, or a bool per claim id; the plant whose reading must differ on it)
CASES = [
    ("C1 two calls; the second refuses after the claim", law(*[l.format(n0=0) for l in PROC]), True,
     "context-free"),
    ("C1' the same, one literal apart: the first call refuses", law(*[l.format(n0=1) for l in PROC]), False, None),
    ("C2 a loop, refused at pass 17 of 20, the claim before", law(*[l.format(m=16) for l in LOOP]), False,
     None),
    ("C2' the same, one literal apart: refused at pass 20 of 20", law(*[l.format(m=19) for l in LOOP]), True,
     "no-count"),
    ("C3 nested calls; inner's second call refuses after the claim", law(*[l.format(n0=0) for l in NESTED]), True,
     "context-free"),
    ("C3' the same, one literal apart: inner's first call refuses", law(*[l.format(n0=1) for l in NESTED]), False,
     None),
    ("C4 the claim's own evaluation refuses, on the last pass", law(*OPEN), False, "no-open"),
    ("C5 a claim in an arm that runs on pass 1 only, refused at pass 20 of 20", law(*[l.format(m=19) for l in BRANCH]),
     True, "no-count"),
    ("C6 a While refused FUEL-EXHAUSTED: the refused check guarded a fourth pass", law(*FUEL), False, "header-bit"),
    ("D02 a While's claim, refused on pass 3 of a loop that would run 5", law(*D02), False, None),
    ("D03 a top-level claim between two calls, the second refuses", law(*D03), True, "context-free"),
    ("D08 a claim guarded to pass 1, refused on pass 3 (withheld: conservative by design)", law(*D08), False, None),
    ("D11 an Otherwise arm's claim, the second call refuses in the other arm", law(*D11), True, "context-free"),
    ("F1 a While's last allowed pass refuses on an input (d = 0): the fuel check guards a refuting pass",
     law(*[l.format(d=0) for l in F1]), False, "while-bit"),
    ("F1' the same, one literal apart (d = 1): the run reaches the fuel check", law(*[l.format(d=1) for l in F1]),
     False, None),
    ("A23 two claims on one clause, the second open (c = true)", law(*[l.format(c="true") for l in A23]),
     {0: True, 1: False}, None),
    ("A23' one literal apart, the first open (c = false)", law(*[l.format(c="false") for l in A23]),
     {0: False, 1: True}, None),
    ("A09 an Otherwise-if condition refuses on the last pass; the claim's arm read false before it", law(*A09), True,
     "all-arms"),
    ("L1 the claim reachable after the refusal only through a procedure performed inside another", law(*L1), False,
     "shallow-reach"),
]


def readings_of(name, raw):
    status, out, desc = judge(raw)
    return status, desc, {k: v for k, v in sorted(out.items())}


def corpus():
    """Every frozen text of COMPAT-0, the court's fixtures, the examples and this probe's cases, with their budgets."""
    import glob
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    with open(os.path.join(ROOT, "tests", "compat", "baseline-v0.jsonl"), "rb") as fh:
        budgets = json.loads(fh.read().decode("utf-8").split("\n", 1)[0])["budgets"]
    sources = [(t["id"], base64.b64decode(t["b64"]), budgets[t["kind"]]) for t in doc["texts"]]
    for pattern in ("tests/fixtures/*/*.orl", "examples/*.orl", "examples/*/*.orl"):
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            with open(path, "rb") as fh:
                sources.append((os.path.relpath(path, ROOT).replace(os.sep, "/"), fh.read(), 10 ** 8))
    sources += [(name.split(" ")[0], raw, 10 ** 8) for name, raw, _, _ in CASES]
    sources.append(("F4-host-stop-at-a-While", law(*F4), 4))
    return sources


def run_both(comp, budget):
    results = []
    for cls in (Interp, CutInterp):
        it = cls(comp.prog, comp.an, comp.law_seal, comp.text_seal, trace=True, budget=budget)
        try:
            it.run()
            results.append(("ran", it.receipt(), tuple(it.trace)))
        except HostStop as h:
            results.append(("stopped", h.ops, tuple(it.trace)))
    return results


def equivalence(sources):
    """The instrumented reference against the reference: at each text's own budget, and at a third and two thirds of
    the operations its run takes, so that host stops fall part-way. The same receipt bytes, the same trace line for
    line, the same host stop. Returns (runs compared, host stops among them, the runs that differ)."""
    n = stopped = 0
    differ = []
    for ident, raw, budget in sources:
        comp = compile_bytes(raw)
        if not comp.ok:
            continue
        first = run_both(comp, budget)
        budgets = [budget]
        if first[0][0] == "ran":
            total = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run().ops
            budgets += [b for b in (total // 3, 2 * total // 3) if 0 < b < total]
        for i, b in enumerate(budgets):
            results = first if i == 0 else run_both(comp, b)
            n += 1
            stopped += results[0][0] == "stopped"
            if results[0] != results[1]:
                differ.append("%s at budget %d" % (ident, b))
    return n, stopped, differ


def main():
    global PLANT
    bad = 0
    print("== the cases (version 0; a pair marked ' is its case one literal apart, a read-once port's stand-in)")
    results = {}
    for name, raw, want, _ in CASES:
        status, desc, out = readings_of(name, raw)
        results[name.split(" ")[0]] = (desc, out)
        wants = want if isinstance(want, dict) else {k: want for k in out}
        ok = all(out[k][4] == wants[k] for k in out)
        bad += not ok
        print("%s\n   run %s; cut [%s]" % (name, status, desc))
        for k, (lab, ev, built, site, cut, _) in out.items():
            print("   %s#%d %s: as built %s; site rule %s; cut rule %s%s" % (
                lab, k, ev[:60], *("held" if v else "withheld" for v in (built, site, cut)),
                "" if cut == wants[k] else "   <- EXPECTED " + ("held" if wants[k] else "withheld")))
    print("== pairs the site rule reads alike and the cut tells apart")
    for a, b in (("C1", "C1'"), ("C2", "C2'"), ("C3", "C3'")):
        (_, ra), (_, rb) = results[a], results[b]
        ra, rb = list(ra.values())[0], list(rb.values())[0]
        same_site, differ_cut = ra[3] == rb[3], ra[4] != rb[4]
        print("   %s / %s: site rule %s, cut rule %s" % (a, b, "alike" if same_site else "DIFFERS",
                                                       "tells them apart" if differ_cut else "ALIKE"))
        bad += not (same_site and differ_cut)
    da, db = results["A23"][0], results["A23'"][0]
    print("   A23 / A23': descriptors %s (%s / %s)" % ("differ" if da != db else "ALIKE", da, db))
    bad += da == db
    print("== plants, each read on the cases that must catch it")
    caught = 0
    plants = sorted({p for *_, p in CASES if p}) + ["descriptor-no-id", "no-entry-check"]
    for plant in plants:
        PLANT = plant
        if plant == "descriptor-no-id":
            hits = ["A23/A23'"] if readings_of("", CASES[[c[0].split(" ")[0] for c in CASES].index("A23")][1])[1] == \
                readings_of("", CASES[[c[0].split(" ")[0] for c in CASES].index("A23'")][1])[1] else []
        elif plant == "no-entry-check":
            comp = compile_bytes(law(*F4))
            r = run_both(comp, 4)
            hits = ["F4"] if r[0] != r[1] else []
        else:
            hits = []
            for name, raw, want, p in CASES:
                if p != plant:
                    continue
                out = readings_of(name, raw)[2]
                wants = want if isinstance(want, dict) else {k: want for k in out}
                if any(out[k][4] != wants[k] for k in out):
                    hits.append(name.split(" ")[0])
        PLANT = None
        caught += bool(hits)
        print("   plant %-17s %s" % (plant, ("caught on " + ", ".join(hits)) if hits else "NOT CAUGHT"))
    sources = corpus()
    print("== the instrumented reference against the reference: own budgets, and a third and two thirds of each run")
    n, stopped, differ = equivalence(sources)
    print("   runs %d (host stops among them: %d): receipts, traces and host stops identical in %d, different in %d%s"
          % (n, stopped, n - len(differ), len(differ), (": " + ", ".join(differ[:10])) if differ else ""))
    print("== every claim of COMPAT-0's frozen texts, the court's fixtures and the examples that ran")
    n_c = held = cut_withheld = site_withheld = 0
    gains, unexplained, r8_exact, r8_exact_cut, r8_possible, r8_possible_held = [], [], 0, 0, 0, 0
    rows = []
    case_ids = {c[0].split(" ")[0] for c in CASES} | {"F4-host-stop-at-a-While"}
    for ident, raw, budget in sources:
        comp = compile_bytes(raw)
        if not comp.ok or not comp.an.claims or ident in case_ids:
            continue
        try:
            status, out, desc = judge(raw, budget)
        except HostStop:
            continue
        for k, (lab, ev, built, site, cut, done) in out.items():
            n_c += 1
            held += built
            site_withheld += built and not site
            cut_withheld += built and not cut
            if done and not built and "REFUSED at evaluation" in ev:
                r8_exact += 1
                r8_exact_cut += not cut
            if done and not built and "may come from" in ev:
                r8_possible += 1
                r8_possible_held += cut
            if cut and not built:
                gains.append("%s %s" % (ident, lab))
                if "may come from" not in ev:
                    unexplained.append("%s %s" % (ident, lab))
            if site != cut or built != cut:
                rows.append("   %s %s: as built %s, site rule %s, cut rule %s" % (
                    ident, lab, *("held" if v else "withheld" for v in (built, site, cut))))
    print("   claims %d, held as built %d, withheld by the site rule %d, by the cut %d" % (
        n_c, held, site_withheld, cut_withheld))
    print("   R8's exact class (an evaluation refused partway): %d, withheld by the cut too: %d" % (
        r8_exact, r8_exact_cut))
    print("   R8's possible class (a refusal at a clause that holds another arm): %d, held by the cut: %d" % (
        r8_possible, r8_possible_held))
    print("   gains over the court as built: %d, each in R8's possible class with the frames showing another claim "
          "open: %d unexplained" % (len(gains), len(unexplained)))
    print("\n".join(rows) if rows else "   no reading differs")
    ok = bad == 0 and caught == len(plants) and not unexplained and r8_exact_cut == r8_exact and not differ
    print("CUT-0 CLAIMS %s: %d of %d cases as required, pairs and descriptors told apart, plants %d/%d, %d gains (%d "
          "unexplained), R8's exact class %d/%d, the instrumented reference identical in %d of %d runs (%d host stops)"
          % ("HELD" if ok else "FAILED", len(CASES) - min(bad, len(CASES)), len(CASES), caught, len(plants),
             len(gains), len(unexplained), r8_exact_cut, r8_exact, n - len(differ), n, stopped))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

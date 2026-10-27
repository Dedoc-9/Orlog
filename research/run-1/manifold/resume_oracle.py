"""RESEARCH SCRIPT (the manifold debate's proponent, 2026-10-26). Nothing in the program reads it; it edits nothing.

A test-only resumption oracle for CUT-0's claim continuation (research/run-1/probes/cut0_claims.py).

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/resume_oracle.py            (check: the record)
  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/resume_oracle.py search     (minimise and print)

CUT-0 defines K as what the run could still have evaluated had the refusing operation returned. The oracle makes that
hypothetical run. `Resumed` is the probe's own CutInterp (the reference with frames recorded) in which the first
refusal does not raise: the refusing operation returns, and the reference's own code goes on.
- an integer arithmetic refusal (numeric_ref raises inside `num`) returns a value v;
- an INDEX-OUT-OF-RANGE in `item k of xs` (a list of integers) returns v;
- CLAIM-REFUTED and MUST-FAILED return after their statement's evaluation, which completed;
- FUEL-EXHAUSTED returns, and the reference's While goes on to the pass the check guarded.
Any other refusal at the cut is not modelled: the run is counted and set aside. Up to the cut the resumed run is the
plain reference (checked: the same trace event for event; the probe's cut frame for frame). After the cut it is the
reference's code with one value substituted. Three readings of what follows:
- R1: only the cut's refusal returns; a later refusal ends the hypothetical run (the probe's first form, reading S1);
- Rnofuel: every later refusal returns too, FUEL-EXHAUSTED excepted;
- Rinf: every later refusal returns (the probe's reading S2 since its revision of 2026-10-26).
O is the set of claims evaluated (a completed 'C' event) after the cut, united over the values V. A claim in O and not
in K is an unsoundness counterexample under that reading; a claim in K and in no O is a precision loss.

K is the probe's continuation as it stands (reading S2). The first form (a While below the top repeats only while fuel
remains; an If whose condition refused may run every arm) is this script's copy under two of the probe's own plants,
`while-bit` and `all-arms`, each held equal to the probe's.
"""
import hashlib
import os
import random
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
import cut0_claims as C                                          # noqa: E402
from orlog import numeric_ref as N                               # noqa: E402
from orlog.front import compile_bytes                            # noqa: E402
from orlog.interp import HostStop, Interp                        # noqa: E402
from orlog.syntax import Claim, For, IfS, Item, Perform, While   # noqa: E402

V = (-2, -1, 0, 1, 2, 3, 4, 9)   # every class of family G's atoms over y; 9 runs a For past every c (PROPONENT.md 3)
BUDGET = 20000                   # the reference run's host budget, counted operations
RESUME_BUDGET = 5000             # a resumed run's
ORACLE_PLANT = None              # "no-resume", "one-value", "abandon-statement": the oracle made wrong on purpose
VALUE_CODES = {"DIVISION-BY-ZERO", "INEXACT-DIVISION", "OVERFLOW", "INDEX-OUT-OF-RANGE"}
PLAIN_CODES = {"CLAIM-REFUTED", "MUST-FAILED", "FUEL-EXHAUSTED"}
LAWS = os.path.join(HERE, "laws")
MODES = ("R1", "Rnofuel", "Rinf")


class Unmodelled(Exception):
    pass


class Abandon(Exception):
    pass


class Resumed(C.CutInterp):
    def __init__(self, *a, value=None, mode="R1", **k):
        C.CutInterp.__init__(self, *a, **k)
        self.value, self.mode = value, mode
        self.cut_code = None
        self.after = set()
        self.item_refusal = False
        self.abandon_depth = None

    def refuse(self, code, clause):
        first = self.cut is None
        if first:
            self.cut = [dict(f) for f in self.frames]
            self.cut_code = code
            if code not in VALUE_CODES | PLAIN_CODES or (code == "INDEX-OUT-OF-RANGE" and not self.item_refusal):
                raise Unmodelled(code)
            if ORACLE_PLANT == "no-resume":
                Interp.refuse(self, code, clause)
            if ORACLE_PLANT == "abandon-statement":
                self.abandon_depth = len(self.frames) - 1
                raise Abandon()
            return
        later = code in VALUE_CODES | PLAIN_CODES and not (code == "INDEX-OUT-OF-RANGE" and not self.item_refusal)
        if later and (self.mode == "Rinf" or (self.mode == "Rnofuel" and code != "FUEL-EXHAUSTED")):
            return
        Interp.refuse(self, code, clause)

    def num(self, fn, clause, *args):
        try:
            return fn(*args)
        except N.Refusal as r:
            if not fn.__name__.startswith("i_"):
                raise Unmodelled(fn.__name__)
            self.refuse(r.code, clause)
            return self.value

    def eval(self, cid, e):
        if isinstance(e, Item):                     # the reference's Item, the refusal able to return a value
            k = self.eval(cid, e.index)
            self.ops += 1
            lst = self.env[e.var.id]
            if not 1 <= k <= len(lst):
                if e.var.type != ("list", "int"):
                    raise Unmodelled("item of %r" % (e.var.type,))
                self.item_refusal = True
                self.refuse("INDEX-OUT-OF-RANGE", cid)
                self.item_refusal = False
                return self.value
            return lst[k - 1]
        return C.CutInterp.eval(self, cid, e)

    def stmt(self, c, s):
        if ORACLE_PLANT != "abandon-statement":
            return C.CutInterp.stmt(self, c, s)
        depth = len(self.frames)
        try:
            return C.CutInterp.stmt(self, c, s)
        except Abandon:
            if depth == self.abandon_depth:
                return None                         # the plant: the refusing statement is skipped as a whole
            raise

    def ev(self, kind, clause, payload):
        Interp.ev(self, kind, clause, payload)
        if kind == b"C" and self.cut is not None:
            self.after.add(struct.unpack(">I", payload[:4])[0])


# ------------------------------------------------------------------ K: a copy of the probe's continuation, with plants
K_PLANT = None
K_PLANTS_UNSOUND = ("no-open", "header-bit", "while-bit", "top-after-missing", "outer-loop-never", "refused-arm-only",
                    "proc-empty", "else-missing", "no-return", "depth-cut")
K_PLANTS_PRECISION = ("context-free", "no-count", "all-arms")
PROBE_PLANTS = ("context-free", "no-count", "no-open", "header-bit", "while-bit", "all-arms")


class PReach(C.Reach):
    def proc(self, name):
        if K_PLANT == "proc-empty":
            return set()
        return C.Reach.proc(self, name)

    def stmt(self, x):
        if K_PLANT == "depth-cut" and isinstance(x.stmt, (For, While, IfS)):
            return set()                            # a reach cut off at the first nested block (LINEAGE.md, 4)
        return C.Reach.stmt(self, x)

    def arms_from(self, st, first):
        if K_PLANT == "else-missing":
            out = set()
            for _, b, _ in st.arms[first:]:
                out |= self.arm(b)
            return out
        return C.Reach.arms_from(self, st, first)


def may_repeat(frame, plant):
    if isinstance(frame["stmt"], For):
        return plant == "no-count" or bool(frame["more"])
    if plant in ("while-bit", "first-form"):
        return bool(frame["more"])
    return True


def continuation_copy(prog, cut, plant=None):
    """cut0_claims.continuation line for line (held equal to it, unplanted and under the probe's plants), with this
    script's plants as hooks. "first-form" is the probe's plants while-bit and all-arms at once."""
    global K_PLANT
    K_PLANT = plant
    try:
        r = PReach(prog)
        top = cut[-1]
        s = top["stmt"]
        k = set()
        if isinstance(s, Claim) and plant != "no-open":
            k.add(s.id)
        elif isinstance(s, IfS):
            first = 0 if plant in ("all-arms", "first-form") or top["arm"] is None else top["arm"]
            if plant == "refused-arm-only":
                k |= r.arm(s.arms[first][1])
            else:
                k |= r.arms_from(s, first)
        elif isinstance(s, (For, While)) and (plant != "header-bit" or top["more"] is not False):
            k |= r.seq(top["clause"].children)
        elif isinstance(s, Perform):
            k |= r.proc(s.name)
        first_frame = True
        for i in range(len(cut) - 1, -1, -1):
            c = cut[i]["clause"]
            outer = cut[i - 1] if i > 0 else None
            if outer is not None and outer["clause"] is c:
                continue
            if not (plant == "top-after-missing" and first_frame):
                k |= r.after(c)
            first_frame = False
            if outer is None:
                break
            if isinstance(outer["stmt"], (For, While)) and plant != "outer-loop-never" and may_repeat(outer, plant):
                k |= r.seq(outer["clause"].children)
            if plant == "context-free" and isinstance(outer["stmt"], Perform):
                for site in [x for x in prog.clauses if isinstance(x.stmt, Perform)
                             and x.stmt.name == outer["stmt"].name]:
                    k |= r.after(site) | r.proc(outer["stmt"].name)
            if plant == "no-return" and isinstance(outer["stmt"], Perform):
                break
        return k
    finally:
        K_PLANT = None


def probe_continuation(prog, cut, plant=None):
    C.PLANT = plant
    try:
        return C.continuation(prog, cut)
    finally:
        C.PLANT = None


def probe_descriptor(cut, plant=None):
    C.PLANT = plant
    try:
        return C.descriptor(cut)
    finally:
        C.PLANT = None


# ------------------------------------------------------------------ one law, judged and resumed
def claim_labels(comp):
    return {cs.stmt.id: cs.label for cs in comp.an.claims}


def frames_key(cut):
    return [(f["clause"].id, type(f["stmt"]).__name__, f["more"], f.get("arm")) for f in cut]


def resume(comp, value, mode, budget=None):
    it = Resumed(comp.prog, comp.an, comp.law_seal, comp.text_seal, trace=True, value=value, mode=mode,
                 budget=RESUME_BUDGET if budget is None else budget)
    try:
        it.run()
        end = it.status
    except HostStop:
        end = "HOST-STOP"
    except Unmodelled as u:
        end = "UNMODELLED %s" % u
    return it, end


def analyse(raw, values=None, plants=()):
    """None if the text does not compile; else a dict of the run, its cut, the K's and the oracle's sets."""
    comp = compile_bytes(raw)
    if not comp.ok:
        return None
    plain = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, trace=True, budget=BUDGET)
    ref = C.CutInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal, trace=True, budget=BUDGET)
    stops = []
    for it in (plain, ref):
        try:
            it.run()
            stops.append(False)
        except HostStop:
            stops.append(True)
    if any(stops):
        return {"kind": "host-stop", "instr_ok": stops[0] == stops[1]}
    out = {"kind": "completed" if ref.cut is None else "refused", "comp": comp, "status": ref.status,
           "instr_ok": plain.receipt() == ref.receipt() and plain.trace == ref.trace}
    if ref.cut is None:                         # with nothing refused, the resumed interpreter is the reference
        it, end = resume(comp, 1, "R1")
        out["receipt_ok"] = end == plain.status and it.receipt() == plain.receipt()
        return out
    code = ref.status.split(" ")[1]
    out["code"] = code
    out["desc"] = probe_descriptor(ref.cut)
    out["desc_noid"] = probe_descriptor(ref.cut, "descriptor-no-id")
    out["K"] = probe_continuation(comp.prog, ref.cut)
    out["K_copy"] = continuation_copy(comp.prog, ref.cut)
    out["K_first"] = continuation_copy(comp.prog, ref.cut, "first-form")
    out["K_plants"] = {p: continuation_copy(comp.prog, ref.cut, p) for p in plants}
    out["K_probe_plants"] = {p: probe_continuation(comp.prog, ref.cut, p) for p in plants if p in PROBE_PLANTS}
    out["done"] = {i: acc[0] > 0 and acc[0] == acc[1] for i, acc in enumerate(ref.claims)}
    out["open"] = ref.cut[-1]["stmt"].id if isinstance(ref.cut[-1]["stmt"], Claim) else None
    if values is None:
        values = V
    if ORACLE_PLANT == "one-value":
        values = (1,)
    vals = values if code in VALUE_CODES else (None,)
    out["values"] = vals
    out["prefix_ok"] = True
    out["cut_ok"] = True
    out["ends"] = {}
    for mode in MODES:
        o = set()
        # a cut that returns no value needs one R1 run; past it, a later refusal may need a value
        for v in (vals if mode == "R1" or code in VALUE_CODES else values):
            it, end = resume(comp, v, mode)
            if end.startswith("UNMODELLED"):
                out["kind"] = "unmodelled"
                out["why"] = end
                return out
            o |= it.after
            out["ends"].setdefault(mode, []).append(end)
            out.setdefault("per_value_" + mode, []).append(frozenset(it.after))
            if end == "HOST-STOP":                  # bounded, not closed: did the set still grow in the last half?
                half, _ = resume(comp, v, mode, RESUME_BUDGET // 2)
                out["truncated"] = out.get("truncated", 0) + 1
                out["growing"] = out.get("growing", 0) + (half.after != it.after)
            if mode == "R1":
                n = len(plain.trace)
                if it.trace[:n - 1] != plain.trace[:n - 1]:
                    out["prefix_ok"] = False
                if it.cut is None or frames_key(it.cut) != frames_key(ref.cut):
                    out["cut_ok"] = False
        out["O_" + mode] = o
    return out


def held_by(r, K):
    return {i for i, d in r["done"].items() if d and i not in K}


def held_oracle(r, mode):
    return {i for i, d in r["done"].items() if d and i != r["open"] and i not in r["O_" + mode]}


# ------------------------------------------------------------------ the hand-worked cases
def law(*lines):
    return "".join(("§" + l[1:] if l.startswith("S") else l) + "\n" for l in lines).encode("utf-8")


VAL = ["S1 Let x be 0.", "S2 Let y be 1.", "S3 Set y to x divided by x.", "S4 If y is positive, say y.",
       "S5 Otherwise, do the following.", "S5.1 We claim that y is at most 0."]
FUELOUT = ["S1 Let x be 0.", "S2 While x is less than 9, at most 2 times, do the following.", "S2.1 Increase x by 1.",
           "S2.2 We claim that x is positive.", "S2.3 Say 6 divided by (x minus 2)."]
PROBE_CASES = {name.split(" ")[0]: raw for name, raw, _, _ in C.CASES}
# (name, the claims (labels) some R1 resumption evaluates after the cut, the same under Rinf): worked by hand
HAND_EXPECT = [
    ("C1", set(), set()),          # the second call refused after its claim; it returns to the end of the law
    ("C1'", {"3.2"}, {"3.2"}),     # the first call refused; the second evaluates the claim, then refuses item 3
    ("C2", {"2.1"}, {"2.1"}),      # pass 17 refused; pass 18 evaluates the claim
    ("C2'", set(), set()),         # pass 20 of 20 refused; nothing remains
    ("C3", set(), set()),          # inner's second call refused; inner returns to outer's end, outer to the law's
    ("C3'", {"3.2"}, {"3.2"}),     # inner's first call refused; its second call evaluates the claim
    ("C4", {"2.1"}, {"2.1"}),      # the open evaluation completes, whatever item 2 returns
    ("C5", set(), set()),          # pass 20 of 20 refused; the arm's claim ran on pass 1 only
    ("C6", {"2.2"}, {"2.2"}),      # the fuel check returns; the fourth pass evaluates the claim
    ("D02", {"2.2"}, {"2.2"}),     # pass 3's division returns; passes 4 and 5 evaluate the claim
    ("D03", set(), set()),         # the second call's division returns; nothing follows it
    ("D08", set(), set()),         # passes 4 and 5 skip the claim's guard (K holds it: conservative)
    ("D11", set(), set()),         # the second call's division returns; the Otherwise arm is not run again
    ("F1", set(), {"3.2"}),        # d = 0: R1 stops at the fourth fuel check; Rinf passes it and evaluates i = 4
    ("F1'", {"3.2"}, {"3.2"}),     # d = 1: the cut is that fuel check; it returns into pass 4
    ("A23", {"3.1"}, {"3.1"}),     # the Otherwise arm's claim (id 1), open on pass 3, completes
    ("A23'", {"3.1"}, {"3.1"}),    # the If arm's claim (id 0), open on pass 3, completes
    ("A09", set(), set()),         # pass 3's Otherwise-if condition returns: arm 1 or the Otherwise, never arm 0
    ("VAL", {"5.1"}, {"5.1"}),     # x divided by x returns v; v at most 0 takes the Otherwise arm
    ("FUELOUT", set(), {"2.2"}),   # pass 2 of 2 refused; R1 stops at the next fuel check, Rinf passes it
]
HAND_RAW = dict(PROBE_CASES, VAL=law(*VAL), FUELOUT=law(*FUELOUT))


def run_hand(report):
    rows = []
    for name, exp1, expinf in HAND_EXPECT:
        r = analyse(HAND_RAW[name])
        lab = claim_labels(r["comp"])
        got1, gotinf = {lab[i] for i in r["O_R1"]}, {lab[i] for i in r["O_Rinf"]}
        ok = got1 == exp1 and gotinf == expinf and r["prefix_ok"] and r["cut_ok"] and r["instr_ok"]
        sound = r["O_Rinf"] <= r["K"]
        rows.append((name, ok, sound))
        if report:
            print("  %-8s %-30s cut [%s]  K %s  first form %s  O(R1) %s  O(Rinf) %s  %s%s" % (
                name, r["status"], r["desc"], sorted(lab[i] for i in r["K"]) or "-",
                sorted(lab[i] for i in r["K_first"]) or "-", sorted(got1) or "-", sorted(gotinf) or "-",
                "as worked" if ok else "EXPECTED %s / %s" % (sorted(exp1) or "-", sorted(expinf) or "-"),
                "" if sound else "  UNSOUND (Rinf)"))
    return rows


# ------------------------------------------------------------------ the families
class Node:
    __slots__ = ("text", "kids")

    def __init__(self, text, kids=None):
        self.text, self.kids = text, kids or []

    def copy(self):
        return Node(self.text, [k.copy() for k in self.kids])


def render(nodes, c, note=None):
    lines = [] if note is None else ["Note: " + note]

    def walk(ns, pre):
        for i, n in enumerate(ns, 1):
            lab = pre + (i,)
            lines.append("§" + ".".join(map(str, lab)) + " " + n.text.replace("{c}", str(c)))
            walk(n.kids, lab)
    walk(nodes, ())
    return "".join(l + "\n" for l in lines).encode("utf-8")


def size(nodes):
    return sum(1 + size(n.kids) for n in nodes)


INC, REF, CLT = "Increase x by 1.", "Set y to (x minus {c}) divided by (x minus {c}).", "We claim that x is at least 0."
HEAD = lambda: [Node("Let x be 0."), Node("Let y be 1.")]           # noqa: E731


def family_e():
    """EXHAUSTIVE family E: Let x, Let y, To p (a body of 1-2 leaves), then two statements from S1."""
    leaves = [INC, REF, CLT]
    b1 = [[a] for a in leaves] + [[a, b] for a in leaves for b in leaves]
    s1 = [[Node(l)] for l in leaves]
    s1 += [[Node("For each i from 1 to 2, do the following.", [Node(t) for t in b])] for b in b1]
    s1 += [[Node("While x is less than 3, at most 2 times, do the following.", [Node(t) for t in b])] for b in b1]
    s1 += [[Node("If x is even, do the following.", [Node(a)]), Node("Otherwise, do the following.", [Node(b)])]
           for a in leaves for b in leaves]
    s1 += [[Node("If x is even, we claim that x is at least 0; otherwise, set y to (x minus {c}) divided by "
                 "(x minus {c}).")]]
    s1 += [[Node("Perform p.")]]
    out = []
    for bp in b1:
        for a in s1:
            for b in s1:
                out.append(HEAD() + [Node("To p, do the following.", [Node(t) for t in bp])]
                           + [n.copy() for n in a] + [n.copy() for n in b])
    return out


CONDS = ["x is even", "x is odd", "y is positive", "y equals 1", "x is less than {c}", "x is at least 2",
         "(x minus {c}) divided by (x minus {c}) equals 1"]
INLINE = ["increase x by 1", "we claim that x is at least 0", "we claim that y equals 1",
          "set y to (x minus {c}) divided by (x minus {c})", "say y", "set y to item (x plus 1) of xs",
          "we claim that (x minus {c}) divided by (x minus {c}) equals 1"]
LEAVES_G = [INC, INC, REF, REF, CLT, CLT, "We claim that y equals 1.", "We claim that x is less than {c}.",
            "We claim that (x minus {c}) divided by (x minus {c}) equals 1.", "It must hold that x is not {c}.",
            "Say y.", "Set y to item (x plus 1) of xs."]


def g_stmts(rng, depth, ctx):
    """One statement of family G, as one or more sibling nodes."""
    if depth == 0 or rng.random() < 0.55:
        pick = rng.randrange(len(LEAVES_G) + len(ctx["procs"]) * 2)
        if pick >= len(LEAVES_G):
            return [Node("Perform %s." % ctx["procs"][(pick - len(LEAVES_G)) // 2])]
        return [Node(LEAVES_G[pick])]
    kind = rng.choice(["if", "if", "inline", "ifref", "for", "fory", "forref", "while", "whileref"])
    inl = INLINE + ["perform %s" % p for p in ctx["procs"]]
    if kind == "if":
        out = [Node("If %s, do the following." % rng.choice(CONDS), g_block(rng, depth - 1, ctx, 1, 2))]
        if rng.random() < 0.4:
            out.append(Node("Otherwise, if %s, do the following." % rng.choice(CONDS), g_block(rng, depth - 1, ctx, 1, 2)))
        if rng.random() < 0.6:
            out.append(Node("Otherwise, do the following.", g_block(rng, depth - 1, ctx, 1, 2)))
        return out
    if kind == "inline":
        form = rng.randrange(3)
        if form == 0:
            return [Node("If %s, %s." % (rng.choice(CONDS), rng.choice(inl)))]
        if form == 1:
            return [Node("If %s, %s; otherwise, %s." % (rng.choice(CONDS), rng.choice(inl), rng.choice(inl)))]
        return [Node("Unless %s, %s." % (rng.choice(CONDS), rng.choice(inl)))]
    if kind == "ifref":
        out = [Node("If (x minus {c}) divided by (x minus {c}) equals 1, do the following.",
                    g_block(rng, depth - 1, ctx, 1, 2))]
        if rng.random() < 0.6:
            out.append(Node("Otherwise, do the following.", g_block(rng, depth - 1, ctx, 1, 2)))
        return out
    ctx["var"] += 1
    v = "i%d" % ctx["var"]
    if kind == "for":
        return [Node("For each %s from 1 to %d, do the following." % (v, rng.choice([1, 2, 3])),
                     g_block(rng, depth - 1, ctx, 1, 3))]
    if kind == "fory":
        return [Node("For each %s from 1 to y, do the following." % v, g_block(rng, depth - 1, ctx, 1, 3))]
    if kind == "forref":
        return [Node("For each %s from 1 to (x minus {c}) divided by (x minus {c}) plus 1, do the following." % v,
                     g_block(rng, depth - 1, ctx, 1, 3))]
    w, f = rng.choice([2, 4, 6]), rng.choice([1, 2, 3, 5])
    head = ("While x is less than %d, at most %d times, do the following." % (w, f) if kind == "while" else
            "While (x minus {c}) divided by (x minus {c}) equals 1 and x is less than %d, at most %d times, do the "
            "following." % (w, f))
    return [Node(head, [Node(INC)] + g_block(rng, depth - 1, ctx, 0, 2))]


def g_block(rng, depth, ctx, lo, hi):
    out = []
    for _ in range(rng.randint(lo, hi)):
        out += g_stmts(rng, depth, ctx)
    return out


def family_g(n, seed):
    """MEASURED family G: n programs drawn with random.Random(seed); procedures p, q, r (each may perform those before
    it), a list xs of c copies of 1 whose item (x plus 1) refuses once x reaches c."""
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        ctx = {"procs": [], "var": 0}
        nodes = HEAD() + [Node("Let xs be a list of {c} copies of 1.")]
        for name, chance in (("p", 0.7), ("q", 0.5), ("r", 0.4)):     # each may perform the ones before it
            if rng.random() >= chance:
                break
            nodes.append(Node("To %s, do the following." % name, g_block(rng, 2, ctx, 1, 3)))
            ctx["procs"].append(name)
        nodes += g_block(rng, 3, ctx, 1, 4)
        if size(nodes) <= 32:
            out.append(nodes)
    return out


# ------------------------------------------------------------------ measurement over a family
CS = range(0, 7)
COUNTERS = ("runs", "noncompile", "completed", "host-stop", "unmodelled", "refused", "instr_bad", "receipt_bad",
            "prefix_bad", "cut_bad", "copy_differs", "probe_plant_differs", "truncated", "truncated_all", "growing",
            "value_dependent", "claims",
            "held_now", "held_first", "held_r1", "held_rinf", "unsound_now_r1", "unsound_now_rinf",
            "verdict_unsound_now_r1", "verdict_unsound_now_rinf", "unsound_first_r1", "unsound_first_rinf",
            "first_rinf_fuel_only", "verdict_unsound_first_rinf", "first_not_now", "first_not_now_in_rinf",
            "now_not_first", "now_not_first_in_rinf", "withheld_not_r1", "withheld_not_r1_in_rinf",
            "withheld_not_rinf", "open_refuted", "k_now", "k_now_minus_rinf", "desc_classes", "desc_collide",
            "desc_noid_classes", "desc_noid_collide", "pairs", "flip_cut", "flip_oracle", "flip_both", "flip_cut_only",
            "flip_oracle_only")


def measure(templates, cs, values, plants, base=0):
    st = {k: 0 for k in COUNTERS}
    st["templates"] = len(templates)
    st["codes"] = {}
    st["plant_unsound"] = {p: 0 for p in plants}
    st["plant_kminuso"] = {p: 0 for p in plants}
    first = {}
    for ti, nodes in enumerate(templates, base):
        per_c, by_desc, by_noid = {}, {}, {}
        for c in cs:
            raw = render(nodes, c)
            st["runs"] += 1
            r = analyse(raw, values=values, plants=plants)
            if r is None:
                st["noncompile"] += 1
                continue
            st["instr_bad"] += not r["instr_ok"]
            if r["kind"] != "refused":
                st[r["kind"]] += 1
                st["receipt_bad"] += r["kind"] == "completed" and not r["receipt_ok"]
                continue
            st["refused"] += 1
            st["codes"][r["code"]] = st["codes"].get(r["code"], 0) + 1
            st["prefix_bad"] += not r["prefix_ok"]
            st["cut_bad"] += not r["cut_ok"]
            st["copy_differs"] += r["K"] != r["K_copy"]
            st["probe_plant_differs"] += sum(r["K_probe_plants"][p] != r["K_plants"][p] for p in r["K_probe_plants"])
            st["truncated"] += sum(e == "HOST-STOP" for e in r["ends"]["R1"])
            st["truncated_all"] += r.get("truncated", 0)
            st["growing"] += r.get("growing", 0)
            st["value_dependent"] += len(set(r["per_value_R1"])) > 1
            K, KF, o1, onf, oinf = r["K"], r["K_first"], r["O_R1"], r["O_Rnofuel"], r["O_Rinf"]
            hn, hf = held_by(r, K), held_by(r, KF)
            h1, hinf = held_oracle(r, "R1"), held_oracle(r, "Rinf")
            per_c[c] = (hn, hinf, set(r["done"]))
            by_desc.setdefault(r["desc"], set()).add(frozenset(K))
            by_noid.setdefault(r["desc_noid"], set()).add(frozenset(K))
            st["claims"] += len(r["done"])
            st["held_now"] += len(hn)
            st["held_first"] += len(hf)
            st["held_r1"] += len(h1)
            st["held_rinf"] += len(hinf)
            st["k_now"] += len(K)
            st["k_now_minus_rinf"] += len(K - oinf)
            if o1 - K:
                st["unsound_now_r1"] += 1
                first.setdefault("unsound_now_r1", (ti, c))
            if oinf - K:
                st["unsound_now_rinf"] += 1
                first.setdefault("unsound_now_rinf", (ti, c))
            st["verdict_unsound_now_r1"] += bool(hn & o1)
            st["verdict_unsound_now_rinf"] += bool(hn & oinf)
            st["unsound_first_r1"] += bool(o1 - KF)
            if oinf - KF:
                st["unsound_first_rinf"] += 1
                st["first_rinf_fuel_only"] += not (onf - KF)
                first.setdefault("first_rinf", (ti, c))
            st["verdict_unsound_first_rinf"] += bool(hf & oinf)
            for i in hf - hn:
                st["first_not_now"] += 1
                st["first_not_now_in_rinf"] += i in oinf
                first.setdefault("first_not_now", (ti, c))
            for i in hn - hf:
                st["now_not_first"] += 1
                st["now_not_first_in_rinf"] += i in oinf
                first.setdefault("now_not_first", (ti, c))
            for i, d in r["done"].items():
                if d and i in K and i != r["open"]:
                    if i not in o1:
                        st["withheld_not_r1"] += 1
                        st["withheld_not_r1_in_rinf"] += i in oinf
                    if i not in oinf:
                        st["withheld_not_rinf"] += 1
                        first.setdefault("withheld_not_rinf", (ti, c))
            if r["open"] is not None and r["code"] == "CLAIM-REFUTED":
                st["open_refuted"] += 1
            for p in plants:
                if oinf - r["K_plants"][p]:
                    st["plant_unsound"][p] += 1
                    first.setdefault("plant " + p, (ti, c))
                st["plant_kminuso"][p] += len(r["K_plants"][p] - oinf)
        st["desc_classes"] += len(by_desc)          # within one template, is K a function of the descriptor?
        st["desc_collide"] += sum(len(v) > 1 for v in by_desc.values())
        st["desc_noid_classes"] += len(by_noid)
        st["desc_noid_collide"] += sum(len(v) > 1 for v in by_noid.values())
        for c in cs:                                # one literal apart: the refusal moved by one value of x
            if c in per_c and c + 1 in per_c:
                (hn0, ho0, d0), (hn1, ho1, d1) = per_c[c], per_c[c + 1]
                for i in sorted(d0 & d1):
                    fc, fo = (i in hn0) != (i in hn1), (i in ho0) != (i in ho1)
                    st["pairs"] += 1
                    st["flip_cut"] += fc
                    st["flip_oracle"] += fo
                    st["flip_both"] += fc and fo
                    st["flip_cut_only"] += fc and not fo
                    st["flip_oracle_only"] += fo and not fc
                    if fc and not fo:
                        first.setdefault("flip_cut_only", (ti, c))
    return st, first


_FAMILIES = {}


def family(which):
    if which not in _FAMILIES:
        _FAMILIES[which] = family_e() if which == "E" else family_g(*which[1:])
    return _FAMILIES[which]


def _chunk(args):
    which, lo, hi, values, plants = args
    return measure(family(which)[lo:hi], CS, values, plants, base=lo)


def measure_parallel(which, n, values, plants, jobs=8, chunk=250):
    """measure() over [0, n) in chunks, in a process pool; merged in chunk order, so the result is the serial one."""
    import multiprocessing
    tasks = [(which, lo, min(lo + chunk, n), values, plants) for lo in range(0, n, chunk)]
    with multiprocessing.Pool(jobs) as pool:
        parts = pool.map(_chunk, tasks)
    st, first = parts[0]
    for s2, f2 in parts[1:]:
        for key, v in s2.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    st[key][k2] = st[key].get(k2, 0) + v2
            else:
                st[key] += v
        for key, v in f2.items():
            if key not in first or v < first[key]:
                first[key] = v
    return st, first


def print_stats(st, plants):
    print("  templates %d, runs %d: not compiling %d, completed %d, stopped by the host %d, cut not modelled %d, "
          "refused %d" % (st["templates"], st["runs"], st["noncompile"], st["completed"], st["host-stop"],
                          st["unmodelled"], st["refused"]))
    print("  refusals by code: %s" % ", ".join("%s %d" % kv for kv in sorted(st["codes"].items())))
    print("  validity: CutInterp against the plain reference (receipt, trace, host stop) differs in %d runs; the "
          "resumed interpreter's receipt on completed runs differs in %d; its trace before the cut in %d; its cut in "
          "%d; this script's copy of K against cut0_claims.continuation differs in %d runs, under the probe's plants "
          "in %d; refused runs whose O(R1) depends on the value %d" % (
              st["instr_bad"], st["receipt_bad"], st["prefix_bad"], st["cut_bad"], st["copy_differs"],
              st["probe_plant_differs"], st["value_dependent"]))
    print("  bounded, not closed: resumptions stopped by the host budget %d (under R1 %d); of them, whose claim set "
          "still grew in the second half of the budget %d" % (st["truncated_all"], st["truncated"], st["growing"]))
    print("  claims at the cuts %d; held by K (the probe, reading S2) %d, by the first form %d; by the oracle: under "
          "R1 %d, under Rinf %d" % (st["claims"], st["held_now"], st["held_first"], st["held_r1"], st["held_rinf"]))
    print("  SOUNDNESS of K: runs with a claim evaluated after the cut and not in K: under R1 %d, under Rinf %d; runs "
          "with a claim K holds evaluated again: under R1 %d, under Rinf %d" % (
              st["unsound_now_r1"], st["unsound_now_rinf"], st["verdict_unsound_now_r1"],
              st["verdict_unsound_now_rinf"]))
    print("  the first form: runs unsound under R1 %d; under Rinf %d (vanishing when FUEL-EXHAUSTED alone is not "
          "resumed: %d), with a claim it holds evaluated again %d" % (
              st["unsound_first_r1"], st["unsound_first_rinf"], st["first_rinf_fuel_only"],
              st["verdict_unsound_first_rinf"]))
    print("  the revision's effect on verdicts: claims the first form holds and K withholds %d (of them evaluated "
          "again under Rinf %d); claims K holds and the first form withholds %d (evaluated again under Rinf %d)" % (
              st["first_not_now"], st["first_not_now_in_rinf"], st["now_not_first"], st["now_not_first_in_rinf"]))
    print("  PRECISION of K: |K| summed %d, |K minus O(Rinf)| %d; claims K withholds (completed true, not open) that "
          "no Rinf resumption evaluates again %d; that no R1 resumption evaluates again %d, of which %d only past a "
          "later refusal" % (st["k_now"], st["k_now_minus_rinf"], st["withheld_not_rinf"], st["withheld_not_r1"],
                             st["withheld_not_r1_in_rinf"]))
    print("  cuts at a refuted claim (in K as open, its evaluation complete and false) %d" % st["open_refuted"])
    print("  THE DESCRIPTOR: (template, descriptor) classes %d, holding two different K %d; with the probe's "
          "descriptor-no-id (the first form's) %d classes, holding two different K %d" % (
              st["desc_classes"], st["desc_collide"], st["desc_noid_classes"], st["desc_noid_collide"]))
    print("  ONE LITERAL APART (c and c+1 both refused, a claim's verdict compared): pairs %d; K's verdict flips %d, "
          "the Rinf oracle's %d; both %d, K's alone %d, the oracle's alone %d" % (
              st["pairs"], st["flip_cut"], st["flip_oracle"], st["flip_both"], st["flip_cut_only"],
              st["flip_oracle_only"]))
    for p in plants:
        print("  plant %-18s runs unsound under Rinf %6d   |K minus O(Rinf)| %7d" % (
            p, st["plant_unsound"][p], st["plant_kminuso"][p]))


# ------------------------------------------------------------------ minimisation
def paths(nodes, pre=()):
    for i, n in enumerate(nodes):
        yield pre + (i,)
        yield from paths(n.kids, pre + (i,))


def edit(nodes, path, op):
    nodes = [n.copy() for n in nodes]
    lst = nodes
    for j in path[:-1]:
        lst = lst[j].kids
    i = path[-1]
    if op == "delete":
        del lst[i]
    else:
        lst[i:i + 1] = lst[i].kids
    return nodes


def minimise(nodes, c, pred):
    """Delete or hoist one node at a time while pred holds, to a fixpoint; then the smallest c that keeps it."""
    changed = True
    while changed:
        changed = False
        for op in ("delete", "hoist"):
            for p in list(paths(nodes)):
                cand = edit(nodes, p, op)
                if cand and pred(cand, c):
                    nodes, changed = cand, True
                    break
            if changed:
                break
    for c2 in CS:
        if pred(nodes, c2):
            return nodes, c2
    return nodes, c


def refused(nodes, c, plants=()):
    r = analyse(render(nodes, c), plants=plants)
    return r if r is not None and r.get("kind") == "refused" else None


def pred_unsound(mode, plant=None):
    def p(nodes, c):
        r = refused(nodes, c, (plant,) if plant else ())
        return bool(r) and bool(r["O_" + mode] - (r["K_plants"][plant] if plant else r["K"]))
    return p


def pred_first_rinf(nodes, c):
    r = refused(nodes, c)
    return bool(r) and bool(held_by(r, r["K_first"]) & r["O_Rinf"])


def pred_withheld_not_rinf(nodes, c):
    r = refused(nodes, c)
    return bool(r) and any(d and i in r["K"] and i != r["open"] and i not in r["O_Rinf"] for i, d in r["done"].items())


def pred_first_not_now(nodes, c):
    r = refused(nodes, c)
    return bool(r) and bool((held_by(r, r["K_first"]) - held_by(r, r["K"])) - r["O_Rinf"])


def pred_flip(nodes, c):
    """K's verdict on some claim flips between c and c+1 while the Rinf oracle's does not."""
    r0, r1 = refused(nodes, c), refused(nodes, c + 1)
    if not (r0 and r1):
        return False
    return any(((i in held_by(r0, r0["K"])) != (i in held_by(r1, r1["K"])))
               and ((i in held_oracle(r0, "Rinf")) == (i in held_oracle(r1, "Rinf")))
               for i in r0["done"].keys() & r1["done"].keys())


# ------------------------------------------------------------------ the regression laws (hand-checked, frozen here)
# file; K's labels (the probe as it stands, reading S2); the first form's; O(R1); O(Rinf); the claims K holds; the
# plant this law must catch (or None); what it is. Each row worked by hand (PROPONENT.md, section 4) before it was run.
REGRESSION = [
    ("later-refusal.orl", {"2.1"}, {"2.1"}, set(), {"2.1"}, set(), None,
     "precision: pass 1's first division refuses; every R1 resumption refuses again at the second"),
    ("guard.orl", {"2.1"}, {"2.1"}, set(), set(), set(), None,
     "precision: pass 2 refuses; pass 3 does not satisfy the claim's guard (the Round D adversary's D08, smaller)"),
    ("fuel-bit.orl", {"2.2"}, set(), set(), {"2.2"}, set(), None,
     "the first form held the claim (R1: the next fuel check refuses); K withholds it (Rinf passes the check)"),
    ("s2-price.orl", {"2.2"}, set(), set(), set(), set(), None,
     "fuel-bit one literal apart (bound 2): K withholds; no resumption evaluates the claim again (S2's price)"),
    ("refuted-open.orl", {"2"}, {"2"}, set(), set(), set(), None,
     "K reads a refuted claim as open; never held either way, so no verdict moves"),
    ("plant-no-open.orl", {"2"}, {"2"}, {"2"}, {"2"}, set(), "no-open", "the open evaluation completes after the cut"),
    ("plant-header-bit.orl", {"2.1"}, {"2.1"}, {"2.1"}, {"2.1"}, set(), "header-bit",
     "the fuel check returns and runs the pass it guarded"),
    ("plant-top-after-missing.orl", {"4"}, {"4"}, {"4"}, {"4"}, set(), "top-after-missing",
     "the refusing clause's block goes on"),
    ("plant-outer-loop-never.orl", {"4.1"}, {"4.1"}, {"4.1"}, {"4.1"}, set(), "outer-loop-never",
     "a For's pass left runs"),
    ("plant-if-first-arm.orl", {"3.1"}, {"3.1"}, {"3.1"}, {"3.1"}, set(), "refused-arm-only",
     "a refused condition returning anything but 1 takes the Otherwise arm"),
    ("plant-proc-empty.orl", {"3.1"}, {"3.1"}, {"3.1"}, {"3.1"}, set(), "proc-empty", "Perform p runs p's claim"),
    ("plant-else-missing.orl", {"4.1"}, {"4.1"}, {"4.1"}, {"4.1"}, set(), "else-missing",
     "after the fuel check returns, x is 3, odd: the Otherwise arm"),
    ("plant-no-return.orl", {"5"}, {"5"}, {"5"}, {"5"}, set(), "no-return",
     "p returns to its caller, which goes on to section 5"),
    ("fuel-bit.orl", {"2.2"}, set(), set(), {"2.2"}, set(), "while-bit",
     "the probe's own plant while-bit (the first form's lower While) is caught here under Rinf"),
]


def check_laws():
    rows = []
    for fname, k_exp, kf_exp, o_exp, oinf_exp, held_exp, plant, what in REGRESSION:
        with open(os.path.join(LAWS, fname), "rb") as fh:
            raw = fh.read()
        ok_bytes = b"\r" not in raw and raw.endswith(b"\n")
        r = analyse(raw, plants=(plant,) if plant else ())
        lab = claim_labels(r["comp"])
        k, kf = {lab[i] for i in r["K"]}, {lab[i] for i in r["K_first"]}
        o1, oinf = {lab[i] for i in r["O_R1"]}, {lab[i] for i in r["O_Rinf"]}
        held = {lab[i] for i in held_by(r, r["K"])}
        ok = (ok_bytes and k == k_exp and kf == kf_exp and o1 == o_exp and oinf == oinf_exp and held == held_exp
              and r["prefix_ok"] and r["cut_ok"] and r["instr_ok"])
        caught = None
        if plant:
            caught = bool(r["O_Rinf"] - r["K_plants"][plant])
            ok = ok and caught
        rows.append((fname, ok))
        print("  %s %-28s %-30s cut [%s]  K %s  first %s  O(R1) %s  O(Rinf) %s  held %s%s\n     %s" % (
            "PASS" if ok else "FAIL", fname, r["status"], r["desc"], sorted(k) or "-", sorted(kf) or "-",
            sorted(o1) or "-", sorted(oinf) or "-", sorted(held) or "-",
            ("  plant %s %s" % (plant, "caught" if caught else "NOT CAUGHT")) if plant else "", what))
    return rows


def check_alias():
    """The adversary's F2, rebuilt here: x = 0 opens the Otherwise arm's claim (id 1) on pass 3, after the If arm's
    claim (id 0) ran true on pass 1; x = 2 opens the If arm's claim on pass 3, after the other ran true on passes 1
    and 2. Worked by hand: under descriptor-no-id one descriptor; with the id, two; K {1} and {0}; held {0} and {1}."""
    rs = []
    for fname in ("desc-alias-0.orl", "desc-alias-2.orl"):
        with open(os.path.join(LAWS, fname), "rb") as fh:
            rs.append(analyse(fh.read()))
    r0, r2 = rs
    got = (r0["K"], r2["K"], held_by(r0, r0["K"]), held_by(r2, r2["K"]))
    ok = (r0["desc_noid"] == r2["desc_noid"] and r0["desc"] != r2["desc"] and got == ({1}, {0}, {0}, {1})
          and r0["O_Rinf"] <= r0["K"] and r2["O_Rinf"] <= r2["K"])
    print("  %s desc-alias-0/2: descriptors without the id [%s] and [%s]; with it [%s] and [%s]; K (claim ids) %s and "
          "%s; held %s and %s; O(Rinf) %s and %s" % (
              "PASS" if ok else "FAIL", r0["desc_noid"], r2["desc_noid"], r0["desc"], r2["desc"],
              *[sorted(x) for x in got], sorted(r0["O_Rinf"]), sorted(r2["O_Rinf"])))
    return ok


def main():
    global ORACLE_PLANT
    search = len(sys.argv) > 1 and sys.argv[1] == "search"
    n_g, seed = 10000, 26102026
    with open(C.__file__, "rb") as fh:
        print("== the probe read: research/run-1/probes/cut0_claims.py sha256 %s" % hashlib.sha256(fh.read()).hexdigest())
    print("== the hand-worked cases: the claims (labels) some resumption evaluates after the cut, R1 and Rinf")
    hand = run_hand(True)
    print("== the oracle's own plants, each read on the hand-worked cases (it must fail at least one)")
    oracle_caught = 0
    for plant in ("no-resume", "one-value", "abandon-statement"):
        ORACLE_PLANT = plant
        rows = run_hand(False)
        ORACLE_PLANT = None
        failed = [n for n, ok, _ in rows if not ok]
        oracle_caught += bool(failed)
        print("  plant %-18s %s" % (plant, ("caught on " + ", ".join(failed)) if failed else "NOT CAUGHT"))
    plants = K_PLANTS_UNSOUND + K_PLANTS_PRECISION
    print("== family E (EXHAUSTIVE over its declared grammar; c in 0..6; values {0, 1}: y is never read in E)")
    fam_e = family("E")
    st_e, first_e = measure_parallel("E", len(fam_e), (0, 1), plants)
    print_stats(st_e, plants)
    print("== family G (MEASURED: %d programs from random.Random(%d); c in 0..6; values %s)" % (n_g, seed, V))
    fam_g = family(("G", n_g, seed))
    st_g, first_g = measure_parallel(("G", n_g, seed), n_g, V, plants)
    print_stats(st_g, plants)
    caught_k = [p for p in K_PLANTS_UNSOUND if st_e["plant_unsound"][p] + st_g["plant_unsound"][p] > 0]
    caught_prec = [p for p in K_PLANTS_PRECISION if st_e["plant_kminuso"][p] + st_g["plant_kminuso"][p] >
                   st_e["k_now_minus_rinf"] + st_g["k_now_minus_rinf"]]
    print("== K's plants: unsound ones caught by a counterexample under Rinf %d/%d; precision ones caught by a larger "
          "|K minus O(Rinf)| %d/%d" % (len(caught_k), len(K_PLANTS_UNSOUND), len(caught_prec), len(K_PLANTS_PRECISION)))
    if search:
        print("== minimised witnesses (search mode)")
        jobs = [("unsound_now_rinf", pred_unsound("Rinf")), ("unsound_now_r1", pred_unsound("R1")),
                ("first_rinf", pred_first_rinf), ("first_not_now", pred_first_not_now),
                ("withheld_not_rinf", pred_withheld_not_rinf), ("flip_cut_only", pred_flip)]
        jobs += [("plant " + p, pred_unsound("Rinf", p)) for p in K_PLANTS_UNSOUND]
        for key, pred in jobs:
            src = first_e.get(key) and ("E", first_e[key]) or first_g.get(key) and ("G", first_g[key])
            if not src:
                print("  %s: none found" % key)
                continue
            fam = fam_e if src[0] == "E" else fam_g
            ti, c = src[1]
            nodes, c2 = minimise(fam[ti], c, pred)
            print("  %s (from %s template %d, c %d): %d clauses, c %d" % (key, src[0], ti, c, size(nodes), c2))
            sys.stdout.write("    " + render(nodes, c2).decode("utf-8").replace("\n", "\n    ") + "\n")
    print("== the regression laws in laws/ (hand-checked; each a version-0 law, LF, written in binary)")
    laws = check_laws()
    laws.append(("desc-alias", check_alias()))
    ok = (all(r[1] for r in hand) and all(r[2] for r in hand) and oracle_caught == 3
          and len(caught_k) == len(K_PLANTS_UNSOUND) and len(caught_prec) == len(K_PLANTS_PRECISION)
          and all(r[1] for r in laws)
          and sum(st[k] for st in (st_e, st_g) for k in ("instr_bad", "receipt_bad", "prefix_bad", "cut_bad",
                                                          "copy_differs", "probe_plant_differs")) == 0)
    print("RESUMPTION ORACLE %s: hand cases %d/%d, oracle plants %d/3, K plants %d/%d unsound and %d/%d precision, "
          "laws %d/%d; K unsound under Rinf: E %d G %d runs, under R1: E %d G %d; claims K holds that a resumption "
          "evaluates again (Rinf): E %d G %d" % (
              "HELD" if ok else "FAILED", sum(r[1] for r in hand), len(hand), oracle_caught, len(caught_k),
              len(K_PLANTS_UNSOUND), len(caught_prec), len(K_PLANTS_PRECISION), sum(r[1] for r in laws), len(laws),
              st_e["unsound_now_rinf"], st_g["unsound_now_rinf"], st_e["unsound_now_r1"], st_g["unsound_now_r1"],
              st_e["verdict_unsound_now_rinf"], st_g["verdict_unsound_now_rinf"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

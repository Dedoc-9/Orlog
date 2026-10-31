"""LAW-SUFFICIENCY-0, test 1: the read set against the sealed set (SHEET.md, test 1).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/test1_reads.py

A recorder swaps every object of a compiled law (the program, its clauses, nodes, variables, claim sites and the
analysis) for a subclass that logs each attribute read as (class, attribute), and logs them by phase:
- run: what Interp reads, from its construction to its receipt;
- seal: what law_bytes(prog, an) reads;
- backend: what the lowering and the three generators read (reported only; they decide nothing here).
R_run - R_seal are the candidates. Each is classified derivable, with its derivation written below, or not derivable.
Section 1's static table is checked against the trace. The recorder is shown inert: P and the law bytes are the same
with it as without it. Its two plants are run after the real pass."""
import sys
from collections import defaultdict

import common
from orlog import interp
from orlog.front import compile_bytes
from orlog.lower import Lowered
from orlog import gen_py, gen_c, gen_rs
from orlog.arbiter import C_RT, RS_RT
from orlog.sema import Analysis, ClaimSite, VarInfo, law_bytes
from orlog.syntax import Clause, Node, Program

EXPR = {"Num", "Str", "BoolLit", "Var", "Bin", "Un", "Conv", "Item", "Length", "ListOf", "ListLit", "Seal", "Cat"}
TABLE = {("Change", "elem"), ("Clause", "cost_tracked"), ("Clause", "children"), ("VarInfo", "type"),
         ("Analysis", "rules"), ("Analysis", "overrides"), ("Analysis", "claims")}       # the sheet's section 1
DERIVATIONS = {
    ("Change", "elem"): "the variable's type, or its element type when the change writes an index (sema.py:147-155)",
    ("Clause", "cost_tracked"): "true exactly for a clause that a claim's (certificate N ...) names (sema.py:215-219)",
    ("Clause", "children"): "the clauses whose parent id is this clause's, in clause order",
    ("Program", "top"): "the clauses whose parent id is 0, in clause order",
    ("VarInfo", "type"): "the type of the let's expression, or int for a for's counter (sema.py:124-125, 176)",
    ("Analysis", "rules"): "the define lines of each name, in clause order (sema.py:71-75)",
    ("Analysis", "overrides"): "each define's (over id ...) list, closed transitively (sema.py:476-493)",
    ("Analysis", "claims"): "the claim lines ordered by their written claim id (sema.py:212-213)",
    ("ClaimSite", "id"): "the clause the claim stands in: its line's, or for an inline claim its arm's or else's",
}
BACKEND_ONLY = {                # read by the backends alone: written here, and never run, since D does not build them
    ("Analysis", "vars"): "every let's and for's variable, in the order of their ids (sema.py:97-98)",
    ("Analysis", "rule_types"): "each rule's type, the type of its first define's expression (sema.py:243-248)",
    ("VarInfo", "top"): "a let in a top-level clause, outside any inline body; never a for's counter (sema.py:97)",
}
EXPR_TYPE = ("the expression's type: written for a literal, a binary or unary operator and a list; the target for a "
             "conversion; a variable's or rule's type; text for a string, the seal and cat; int for a length; the "
             "list's element type for an item; a list of the value's type for list-of")

PHASE = [None]
LOG = defaultdict(set)          # (phase, class, attribute) -> ids of the texts where it was read
DROP = set()                    # the recorder's plant: classes whose reads it drops
TEXT = [None]
_REC = {}


def recording(cls):
    if cls not in _REC:
        base = cls.__name__

        def __getattribute__(self, name):
            if PHASE[0] is not None and not name.startswith("__") and base not in DROP:
                LOG[(PHASE[0], base, name)].add(TEXT[0])
            return object.__getattribute__(self, name)
        _REC[cls] = type("Rec" + base, (cls,), {"__slots__": (), "__getattribute__": __getattribute__})
    return _REC[cls]


def wrap(*roots):
    """Swap every reachable object of the law for its recording subclass; containers are walked, not wrapped."""
    seen, stack = set(), list(roots)
    while stack:
        o = stack.pop()
        if id(o) in seen or o is None or isinstance(o, (str, bytes, int, float, bool)):
            continue
        seen.add(id(o))
        if isinstance(o, (list, tuple, set, frozenset)):
            stack.extend(o)
        elif isinstance(o, dict):
            stack.extend(o.keys())
            stack.extend(o.values())
        elif isinstance(o, (Node, Clause, Program, VarInfo, ClaimSite, Analysis)):
            if hasattr(o, "__dict__"):
                stack.extend(vars(o).values())
            for k in getattr(type(o), "__slots__", ()):
                try:
                    stack.append(object.__getattribute__(o, k))
                except AttributeError:
                    pass
            o.__class__ = recording(type(o))


def classify(pair):
    if pair in DERIVATIONS:
        return "derivable", DERIVATIONS[pair]
    if pair[0] in EXPR and pair[1] == "type":
        return "derivable", EXPR_TYPE
    return "NOT DERIVABLE", "no derivation from the law bytes is written for it"


def one_pass(texts, label):
    """Record every text; return the inertness faults (P or the law bytes changed by the recorder)."""
    LOG.clear()
    faults = []
    for ident, kind, raw, budget in texts:
        plain = compile_bytes(raw)
        p_plain = common.run(plain.prog, plain.an, plain.law_seal, plain.text_seal, budget)
        comp = compile_bytes(raw)
        wrap(comp.prog, comp.an)
        TEXT[0] = ident
        PHASE[0] = "run"
        p_rec = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget)
        PHASE[0] = "seal"
        law = law_bytes(comp.prog, comp.an)
        PHASE[0] = "backend"
        low = Lowered(comp)
        gen_py.generate(low)
        gen_c.generate(low, C_RT)
        gen_rs.generate(low, RS_RT)
        PHASE[0] = None
        if p_rec != p_plain or law != plain.law:
            faults.append("%s: the recorder changed %s" % (ident, "P" if p_rec != p_plain else "the law bytes"))
    return faults


def sets():
    by = defaultdict(dict)
    for (phase, cls, attr), ids in LOG.items():
        by[phase][(cls, attr)] = ids
    return by["run"], by["seal"], by["backend"]


def report(texts, say):
    faults = one_pass(texts, "real")
    r_run, r_seal, r_back = sets()
    say("texts: %d (every accepted text, once by its bytes)" % len(texts))
    say("the recorder inert (P and the law bytes as without it): %s" % ("yes, on every text" if not faults else faults))
    say("R_run: %d (class, attribute) pairs; R_seal: %d; read by the backends: %d" % (len(r_run), len(r_seal), len(r_back)))
    cand = sorted(set(r_run) - set(r_seal))
    say()
    say("== R_run - R_seal: %d candidates, each classified" % len(cand))
    undecided = []
    for pair in cand:
        verdict, why = classify(pair)
        say("   %-10s %-24s on %3d texts  %s: %s" % (pair[0], pair[1], len(r_run[pair]), verdict, why))
        if verdict != "derivable":
            undecided.append(pair)
    say()
    say("== the sheet's static table against the trace")
    for pair in sorted(TABLE):
        say("   %-10s %-14s %s" % (pair[0], pair[1], "traced in R_run - R_seal" if pair in cand else
                                   ("traced, but also read by the law bytes" if pair in r_run else "NOT TRACED")))
    extra = [p for p in cand if p not in TABLE]
    say("   traced in R_run - R_seal and not in the table: %d %s" % (len(extra), ["%s.%s" % p for p in extra]))
    say()
    say("== R_seal - R_run: sealed, and never read by the run (%d)" % len(set(r_seal) - set(r_run)))
    say("   %s" % ", ".join("%s.%s" % p for p in sorted(set(r_seal) - set(r_run))))
    say()
    back = sorted(set(r_back) - set(r_seal))
    say("== read by the backends and not by the law bytes (reported, deciding nothing): %d" % len(back))
    for pair in back:
        verdict, why = classify(pair)
        if pair in BACKEND_ONLY:
            verdict = "derivable as written, not run (D does not build it): " + BACKEND_ONLY[pair]
        say("   %-10s %-24s %s" % (pair[0], pair[1], verdict))
    return cand, undecided, faults


def main():
    lines = []

    def say(s=""):
        lines.append(s)
        print(s, flush=True)

    texts = common.accepted()
    say("LAW-SUFFICIENCY-0, TEST 1: THE READ SET AGAINST THE SEALED SET (research/law-sufficiency/test1_reads.py)")
    cand, undecided, faults = report(texts, say)
    say()
    say("== the falsifier: a candidate that is not derivable and whose perturbation, the law bytes fixed, changes P")
    if undecided:
        say("   INCONCLUSIVE: %d candidates have no written derivation, and no perturbation is automated: %s"
            % (len(undecided), ["%s.%s" % p for p in undecided]))
    else:
        say("   every candidate is derivable by a written derivation: nothing to perturb (test 3 runs the derivations)")

    say()
    say("== plants: each run alone, after the real pass; each must be reported as stated before it ran")
    results = []
    # plant 1: the interpreter made to read an unsealed field, a clause's source line
    orig = interp.Interp.stmt

    def stmt_reading_line(self, c, s):
        c.line
        return orig(self, c, s)
    interp.Interp.stmt = stmt_reading_line
    try:
        one_pass(texts, "plant 1")
    finally:
        interp.Interp.stmt = orig
    r_run, r_seal, _ = sets()
    got = ("Clause", "line") in set(r_run) - set(r_seal) and classify(("Clause", "line"))[0] != "derivable"
    results.append(got)
    say("   plant 1, Interp reads Clause.line: expected listed in R_run - R_seal as not derivable: %s"
        % ("CAUGHT" if got else "MISSED"))
    # plant 2: the recorder made to drop the reads of one class, Change
    DROP.add("Change")
    try:
        one_pass(texts, "plant 2")
    finally:
        DROP.clear()
    r_run, r_seal, _ = sets()
    got = ("Change", "elem") not in r_run
    results.append(got)
    say("   plant 2, the recorder drops Change's reads: expected the table's Change.elem reported NOT TRACED: %s"
        % ("CAUGHT" if got else "MISSED"))
    say()
    ok = not faults and all(results)
    say("TEST 1 %s: %d candidates, %d derivable by a written derivation, %d without one; the recorder inert; plants %d of %d"
        % ("HELD" if ok and not undecided else ("INCONCLUSIVE" if ok else "FAILED"), len(cand), len(cand) - len(undecided),
           len(undecided), sum(results), len(results)))
    sys.exit(0 if ok and not undecided else 1)


if __name__ == "__main__":
    main()

"""LAW-SUFFICIENCY-1: the four closure experiments (SHEET-1.md), each against the prediction written there.

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/closure_tests.py

- E1: the rounded conversion, on three fixtures, by decoder.py (LAW-SUFFICIENCY-0's D) and by decoder1.py (D1).
- E2: the order of a rule's definitions, on four fixtures and by a plant in the parsed path.
- E3: D1's backend-only derivations against the analysis's, on the 290 texts and the seven fixtures.
- E4: the three generators on the parsed and on D1's decoded law, and every decoded program built and run by the
  arbiter's own build and run.
Nothing here writes outside work/law-sufficiency-arbiter/ (git-ignored), where the arbiter keeps its builds."""
import concurrent.futures
import copy
import os
import sys

import common
import decoder
import decoder1
from orlog.arbiter import Arbiter, generate
from orlog.front import compile_bytes
from orlog.lower import Lowered
from orlog.seal import seal_words
from orlog.sema import law_bytes

FIXTURES = os.path.join(common.HERE, "fixtures")
WORK = os.path.join(common.ROOT, "work", "law-sufficiency-arbiter")
BACKENDS = ("python", "c99", "rust")
OUT = []


def say(s=""):
    OUT.append(s)
    print(s, flush=True)


def fixture(name):
    with open(os.path.join(FIXTURES, name), "rb") as f:
        return f.read()


def fixtures():
    table = common.budgets()
    return [("fixtures/" + n, "fixture", fixture(n), table["fixture"]) for n in sorted(os.listdir(FIXTURES))
            if n.endswith(".orl")]


def status(p):
    for ln in p.split("\n"):
        if ln.startswith("status "):
            return ln[len("status "):]
    return p


def decode_run(mod, comp, budget):
    try:
        prog, an = mod.decode(comp.law)
    except Exception as e:
        return None, "DECODE-FAILED %s: %s" % (type(e).__name__, e)
    return (prog, an), common.run(prog, an, common.sha(comp.law), comp.text_seal, budget)


def conversions(prog):
    """Every Conv in a decoded program's statements and expressions, as (mode, target, source type)."""
    out, stack = [], [c.stmt for c in prog.clauses if c.stmt is not None]
    seen = set()
    while stack:
        n = stack.pop()
        if id(n) in seen or n is None:
            continue
        seen.add(id(n))
        if isinstance(n, (list, tuple)):
            stack.extend(n)
            continue
        if not hasattr(n, "fields"):
            continue
        if type(n).__name__ == "Conv":
            out.append((n.mode, n.target, n.a.type))
        for k in n.fields:
            stack.append(getattr(n, k, None))
    return out


class Shim:
    """The decoded law, as the lowering and the generators read a compiled law."""

    def __init__(self, prog, an, comp):
        self.prog, self.an, self.law = prog, an, comp.law
        self.law_seal = common.sha(comp.law)
        self.text_seal = comp.text_seal
        self.seal_words = seal_words(self.law_seal)


# ------------------------------------------------------------------ E1
def e1():
    say("== E1: the rounded conversion (three fixtures)")
    ok = True
    paths = set()
    for name in ("e1-rounded-fixed.orl", "e1-rounded-floats.orl", "e1-rounded-refuses.orl"):
        comp = compile_bytes(fixture(name))
        p = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, common.budgets()["fixture"])
        for label, mod in (("D", decoder), ("D1", decoder1)):
            got, pd = decode_run(mod, comp, common.budgets()["fixture"])
            rt = got is not None and law_bytes(*got) == comp.law
            if got is not None and label == "D":
                paths |= set((m, t, s) for m, t, s in conversions(got[0]) if m == "rounded")
            same = pd == p
            ok = ok and same and rt
            say("   %-24s %-2s parsed %-30s decoded P %s, round trip %s" % (
                name, label, status(p), "equal" if same else "DIFFERS (%s)" % common.first_difference(p, pd),
                "exact" if rt else "DIFFERS"))
    want = {("rounded", t, s) for t, s in (("int", "fix"), ("int", "float"), ("fix", "int"), ("fix", "float"),
                                            ("float", "int"), ("float", "fix"))}
    say("   rounded paths decoded by D: %d of 6 %s" % (len(paths & want), sorted("%s<-%s" % (t, s) for _, t, s in paths)))
    ok = ok and paths >= want
    comp = compile_bytes(fixture("e1-rounded-fixed.orl"))
    decoder1.PLANT = "rounded-as-as"
    try:
        _, pd = decode_run(decoder1, comp, common.budgets()["fixture"])
    finally:
        decoder1.PLANT = None
    caught = status(pd) == "REFUSED INEXACT-CONVERSION 1"
    say("   plant, D1 reads rounded as as: predicted REFUSED INEXACT-CONVERSION 1, got %s: %s"
        % (status(pd), "AS PREDICTED" if caught else "NOT AS PREDICTED"))
    return ok, caught


# ------------------------------------------------------------------ E2
E2_PREDICTED = {"e2-provisos.orl": "REFUSED DIVISION-BY-ZERO 3", "e2-provisos-swapped.orl": "REFUSED OVERFLOW 3",
                "e2-values.orl": "REFUSED DIVISION-BY-ZERO 3", "e2-values-swapped.orl": "REFUSED OVERFLOW 3"}


def e2():
    say("== E2: the order of a rule's definitions (SPEC §6: left to right, in clause order)")
    ok = True
    seals = {}
    b = common.budgets()["fixture"]
    for name, want in E2_PREDICTED.items():
        comp = compile_bytes(fixture(name))
        seals[name] = comp.law_seal
        p = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, b)
        _, pd = decode_run(decoder1, comp, b)
        good = status(p) == want and status(pd) == want
        ok = ok and good
        say("   %-24s predicted %-28s parsed %-28s decoded %-28s %s" % (name, want, status(p), status(pd),
                                                                         "AS PREDICTED" if good else "NOT AS PREDICTED"))
    for a, s in (("e2-provisos.orl", "e2-provisos-swapped.orl"), ("e2-values.orl", "e2-values-swapped.orl")):
        differ = seals[a] != seals[s]
        ok = ok and differ
        say("   %s and %s: law seals %s" % (a, s, "differ" if differ else "EQUAL"))
    plant_ok = True
    for name in ("e2-provisos.orl", "e2-values.orl"):
        comp = compile_bytes(fixture(name))
        for n in comp.an.rules:
            comp.an.rules[n].reverse()
        law_fixed = law_bytes(comp.prog, comp.an) == comp.law
        p = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, b)
        _, pd = decode_run(decoder1, comp, b)
        good = law_fixed and status(p) == "REFUSED OVERFLOW 3" and status(pd) == "REFUSED DIVISION-BY-ZERO 3"
        plant_ok = plant_ok and good
        say("   plant, an.rules reversed in %-22s law bytes %s; parsed %s (predicted REFUSED OVERFLOW 3); decoded %s "
            "(predicted REFUSED DIVISION-BY-ZERO 3): %s" % (name, "fixed" if law_fixed else "MOVED", status(p), status(pd),
                                                           "AS PREDICTED" if good else "NOT AS PREDICTED"))
    return ok, plant_ok


# ------------------------------------------------------------------ E3
def var_view(an):
    return [(v.id, v.type, v.top) for v in an.vars]


def e3(texts):
    say("== E3: D1's backend-only derivations against the analysis (an.vars with each id, type and top; an.rule_types)")
    rows = {"vars equal": 0, "rule_types equal": 0, "decoded P equal": 0, "round trip exact": 0}
    fails = []
    for ident, kind, raw, budget in texts:
        comp = compile_bytes(raw)
        got, pd = decode_run(decoder1, comp, budget)
        if got is None:
            fails.append("%s: %s" % (ident, pd))
            continue
        prog, an = got
        checks = (("vars equal", var_view(an) == var_view(comp.an)),
                  ("rule_types equal", an.rule_types == comp.an.rule_types),
                  ("decoded P equal", pd == common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget)),
                  ("round trip exact", law_bytes(prog, an) == comp.law))
        for k, v in checks:
            if v:
                rows[k] += 1
            else:
                fails.append("%s: %s fails" % (ident, k))
    say("   on %d texts: %s" % (len(texts), ", ".join("%s %d" % kv for kv in rows.items())))
    for f in fails:
        say("   FAIL %s" % f)
    ok = not fails
    plants = []
    top_lets = sum(1 for ident, kind, raw, budget in texts if any(v.top for v in compile_bytes(raw).an.vars))
    inline_lets = sum(1 for ident, kind, raw, budget in texts if has_inline_top_let(compile_bytes(raw).prog))
    for plant, want, what in (("top-includes-inline", inline_lets, "texts with a let in an inline body of a top-level clause"),
                              ("top-always-false", top_lets, "texts with a top-level let")):
        decoder1.PLANT = plant
        try:
            n = 0
            for ident, kind, raw, budget in texts:
                comp = compile_bytes(raw)
                got, _ = decode_run(decoder1, comp, budget)
                if got is None or var_view(got[1]) != var_view(comp.an):
                    n += 1
        finally:
            decoder1.PLANT = None
        good = n == want and n > 0
        plants.append(good)
        say("   plant %-20s differs from the analysis on %d texts; %s: %d: %s"
            % (plant, n, what, want, "AS PREDICTED" if good else "NOT AS PREDICTED"))
    return ok, all(plants)


def has_inline_top_let(prog):
    """A let in an inline arm or else of a statement in a top-level clause (read from the parsed program)."""
    for c in prog.clauses:
        if c.parent is not None or c.stmt is None or type(c.stmt).__name__ != "IfS":
            continue
        bodies = [b for _, b, _ in c.stmt.arms] + ([c.stmt.els[0]] if c.stmt.els is not None else [])
        if any(type(b).__name__ == "Let" for b in bodies):
            return True
    return False


# ------------------------------------------------------------------ E4
def sources(comp_like):
    low = Lowered(comp_like)
    return {b: generate(b, low) for b in BACKENDS}


def e4(texts):
    say("== E4: the backends on D1's decoded law")
    same = {b: 0 for b in BACKENDS}
    differ = []
    progs = []
    refs = {}
    for k, (ident, kind, raw, budget) in enumerate(texts):
        comp = compile_bytes(raw)
        refs[ident] = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget)
        parsed = sources(comp)
        got, _ = decode_run(decoder1, comp, budget)
        dec = sources(Shim(got[0], got[1], comp))
        for b in BACKENDS:
            if parsed[b] == dec[b]:
                same[b] += 1
            else:
                differ.append("%s %s" % (ident, b))
            progs.append((k, ident, b, dec[b]))
    say("   generated programs byte-identical, parsed against decoded: %s, on %d texts"
        % (", ".join("%s %d" % (b, same[b]) for b in BACKENDS), len(texts)))
    for d in differ:
        say("   FAIL the generated program differs: %s" % d)
    os.makedirs(os.path.join(WORK, "runs"), exist_ok=True)
    arb = Arbiter(WORK)

    def build_run(item):
        k, ident, b, src = item
        try:
            cmd, how, key = arb.build(b, src)
            r = arb.run(cmd, "t%04d-%s" % (k, b), cwd=os.path.join(WORK, "runs"))
        except Exception as e:
            return ident, b, "BUILD-OR-RUN-FAILED %s" % type(e).__name__
        if r.get("receipt") is None:
            return ident, b, "NO RECEIPT (exit %s)" % r.get("exit")
        return ident, b, common.projection(r["receipt"])
    with concurrent.futures.ThreadPoolExecutor(4) as ex:
        results = list(ex.map(build_run, progs))
    agree = {b: 0 for b in BACKENDS}
    disagree = []
    for ident, b, p in results:
        if p == refs[ident]:
            agree[b] += 1
        else:
            disagree.append("%s %s: %s" % (ident, b, common.first_difference(refs[ident], p)))
    say("   each decoded program built and run by the arbiter, its P equal to the reference's parsed P: %s"
        % ", ".join("%s %d of %d" % (b, agree[b], len(texts)) for b in BACKENDS))
    for d in disagree:
        say("   FAIL %s" % d)
    ok = not differ and not disagree
    decoder1.PLANT = "top-always-false"
    try:
        n = 0
        for ident, kind, raw, budget in texts:
            comp = compile_bytes(raw)
            got, _ = decode_run(decoder1, comp, budget)
            if any(sources(comp)[b] != sources(Shim(got[0], got[1], comp))[b] for b in BACKENDS):
                n += 1
    finally:
        decoder1.PLANT = None
    top_lets = sum(1 for ident, kind, raw, budget in texts if any(v.top for v in compile_bytes(raw).an.vars))
    good = n == top_lets and n > 0
    say("   plant, D1's top always false: the generated programs differ on %d texts; texts with a top-level let: %d: %s"
        % (n, top_lets, "AS PREDICTED" if good else "NOT AS PREDICTED"))
    return ok, good


def main():
    base, fx = common.accepted(), fixtures()
    texts = base + fx
    say("LAW-SUFFICIENCY-1: THE FOUR CLOSURE EXPERIMENTS (research/law-sufficiency/closure_tests.py, SHEET-1.md)")
    say("texts: %d (LAW-SUFFICIENCY-0's %d and the %d fixtures)" % (len(texts), len(base), len(fx)))
    for name in ("decoder.py", "decoder1.py"):
        with open(os.path.join(common.HERE, name), "rb") as f:
            say("%s sha256 %s" % (name, common.sha(f.read())))
    say()
    verdicts = []
    for label, fn in (("E1", e1), ("E2", e2), ("E3", lambda: e3(texts)), ("E4", lambda: e4(texts))):
        ok, plants = fn()
        verdicts.append((label, ok, plants))
        say("   %s %s; its plants %s" % (label, "HELD" if ok else "FAILED", "as predicted" if plants else "NOT AS PREDICTED"))
        say()
    held = all(ok and plants for _, ok, plants in verdicts)
    say("LAW-SUFFICIENCY-1 %s: %s" % ("HELD" if held else "NOT HELD", "; ".join(
        "%s %s" % (label, "held" if ok and plants else "NOT HELD") for label, ok, plants in verdicts)))
    sys.exit(0 if held else 1)


if __name__ == "__main__":
    main()

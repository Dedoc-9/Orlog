"""The contract draft's §8.4 (research/run-1/CONTRACT-DRAFT.md), measured on version 0: a claim is not held when the
refusing clause can reach the claim's clause. Over COMPAT-0's frozen texts, the court's fixtures and the examples, it
counts which claims the court as built holds and the rule would withhold, and runs two plants that must change the
reading of tests/fixtures/court/hoisted_omit.orl.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/completeness_probe.py

Reachability is over the clauses, whatever the values (§8.4): a clause leads to its next sibling or its block's end;
a loop's body ends at the loop's head, which may enter the body or leave; an If may enter any arm or none; a Perform
enters the procedure's body, whose end returns after every Perform of that procedure. Research code: it is not the
court, and nothing reads it.
"""
import base64
import glob
import gzip
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog import court as C                                   # noqa: E402
from orlog.arbiter import parse_receipt                         # noqa: E402
from orlog.front import compile_bytes                           # noqa: E402
from orlog.interp import HostStop, Interp                       # noqa: E402
from orlog.syntax import BLOCK, For, IfS, Perform, ProcDef, While   # noqa: E402

FIXTURE = "FIXTURE written by research/run-1/probes/completeness_probe.py; not a person's act"
# The claim runs before the refusal in each pass; the 17th pass refuses with three passes left, each of which would
# have evaluated the claim again. Only the loop's return to its head reaches it.
LOOP_BEFORE = ("Note: the probe's own case: a claim before the refusal, in a loop with iterations left.\n"
               "§1 Let xs be a list of 16 copies of 1.\n"
               "§2 For each i from 1 to 20, do the following.\n"
               "§2.1 We claim that i is positive, by the owner.\n"
               "§2.2 Let y be item i of xs.\n").encode("utf-8")


class Graph:
    """Successor clauses of each clause id, built once per program. plant: 'no-back-edge' drops a loop's return to its
    head (reachability by textual order alone)."""

    def __init__(self, prog, plant=None):
        self.prog, self.plant = prog, plant
        self.procs = {c.stmt.name: c for c in prog.top if isinstance(c.stmt, ProcDef)}
        self.calls = {}                                          # procedure name -> the clauses after its calls
        self.succ = {}
        for c in prog.clauses:
            for call in self._performs(c):
                self.calls.setdefault(call.name, []).append(c)
        for c in prog.clauses:
            self.succ[c.id] = self._firsts(c) | self._next(c)

    def _siblings(self, c):
        return c.parent.children if c.parent is not None else self.prog.top

    def _arms(self, c):
        """(body, clause) of each arm of an If clause, its Otherwise clauses included."""
        st = c.stmt
        arms = [(b, k) for _, b, k in st.arms]
        if st.els is not None:
            arms.append(st.els)
        return arms

    def _performs(self, c):
        """Perform statements executed at clause c itself: its statement, or an inline arm of an If at c."""
        st = c.stmt
        if isinstance(st, Perform):
            return [st]
        if isinstance(st, IfS):
            return [b for b, k in self._arms(c) if isinstance(b, Perform)]
        return []

    def _enter(self, body, owner):
        if isinstance(body, tuple) and body[0] == BLOCK:
            return {body[1].children[0].id}
        if isinstance(body, Perform):
            return {self.procs[body.name].children[0].id}
        return set()

    def _firsts(self, c):
        st = c.stmt
        if isinstance(st, (For, While)):
            return {c.children[0].id}
        if isinstance(st, Perform):
            return {self.procs[st.name].children[0].id}
        if isinstance(st, IfS):
            out = set()
            for body, k in self._arms(c):
                if k is not c:
                    out.add(k.id)                                 # an Otherwise clause is visited when its arm runs
                else:
                    out |= self._enter(body, c)
            return out
        if c.absorbed:                                            # an Otherwise clause: its own arm's body
            head = self._head_if(c)
            return set().union(*[self._enter(b, k) for b, k in self._arms(head) if k is c] or [set()])
        return set()

    def _head_if(self, z):
        sib = self._siblings(z)
        i = sib.index(z)
        while sib[i].absorbed:
            i -= 1
        return sib[i]

    def _next(self, c):
        """Where control goes when clause c, or the If chain it heads or belongs to, completes."""
        if c.absorbed:
            c = self._head_if(c)
        if isinstance(c.stmt, ProcDef):                          # a definition executes nothing in sequence
            pass
        sib = self._siblings(c)
        i = sib.index(c) + 1
        while i < len(sib) and sib[i].absorbed:
            i += 1
        if i < len(sib):
            return {sib[i].id}
        return self._block_end(c.parent)

    def _block_end(self, owner):
        if owner is None:
            return set()                                          # the program's end
        st = owner.stmt
        if isinstance(st, (For, While)):
            return set() if self.plant == "no-back-edge" else {owner.id}
        if isinstance(st, ProcDef):
            out = set()
            for site in self.calls.get(st.name, []):
                out |= self._next(site)
            return out
        return self._next(owner)                                 # an If's arm, or an Otherwise clause's arm

    def reaches(self, s, c):
        if s == c:
            return True
        seen, todo = set(), list(self.succ[s])
        while todo:
            x = todo.pop()
            if x == c:
                return True
            if x not in seen:
                seen.add(x)
                todo.extend(self.succ[x])
        return False


def readings(comp, lines, plant=None):
    """claim id -> (held by the court as built, held under §8.4); support recomputed for both by the court's lfp."""
    witness = {"dissent_kind": "NONE", "backends": {"reference": {}}}
    ledger = [{"kind": "claim", "claim_seal": s, "note": FIXTURE, "_line": i + 1}
              for i, s in enumerate(C.claim_seals(comp).values())]
    rows = {r["claim"]: r for r in C.panel(comp, witness, lines, ledger)["rows"]}
    status = next((l[7:] for l in lines if l.startswith("status ")), "")
    parts = status.split(" ")
    refused_at = int(parts[2]) if parts[0] == "REFUSED" and len(parts) == 3 else None
    g = Graph(comp.prog, plant)
    recs = {}
    for l in lines:
        if l.startswith("claim "):
            p = l.split(" ")
            recs[int(p[1])] = (int(p[3]), int(p[4]))
    built, rule = {}, {}
    for site in comp.an.claims:
        k = site.stmt.id
        evals, trues = recs.get(k, (0, 0))
        held = rows[k]["evaluation"].startswith("true in")
        built[k] = held
        cut = refused_at is not None and plant != "never" and g.reaches(refused_at, site.id)
        rule[k] = held and not cut
    prem = {s.stmt.id: {comp.prog.by_label[p].stmt.id for p in s.stmt.premises} for s in comp.an.claims}
    ids = set(built)
    sup_built, _ = C.support_sets(ids, built, prem)
    sup_rule, _ = C.support_sets(ids, rule, prem)
    return status, {k: (built[k], rule[k], k in sup_built, k in sup_rule) for k in ids}, rows


def run(raw, budget):
    comp = compile_bytes(raw)
    if not comp.ok or not comp.an.claims:
        return comp, None
    try:
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
    except HostStop:
        return comp, None
    return comp, parse_receipt(it.receipt("reference"))


def main():
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    with open(os.path.join(ROOT, "tests", "compat", "baseline-v0.jsonl"), "rb") as fh:
        budgets = json.loads(fh.read().decode("utf-8").split("\n", 1)[0])["budgets"]
    sources = [(t["id"], base64.b64decode(t["b64"]), budgets[t["kind"]]) for t in doc["texts"]]
    for pattern in ("tests/fixtures/court/*.orl", "tests/fixtures/r8/*.orl", "examples/*.orl"):
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            with open(path, "rb") as fh:
                sources.append((os.path.relpath(path, ROOT).replace(os.sep, "/"), fh.read(), 10 ** 8))
    totals = {"claims": 0, "held as built": 0, "withheld by 8.4": 0, "support lost": 0, "support gained": 0,
              "held gained": 0}
    changed = []
    for ident, raw, budget in sources:
        comp, lines = run(raw, budget)
        if lines is None:
            continue
        status, r, rows = readings(comp, lines)
        for k, (b, n, sb, sn) in sorted(r.items()):
            totals["claims"] += 1
            totals["held as built"] += b
            totals["withheld by 8.4"] += b and not n
            totals["held gained"] += n and not b
            totals["support lost"] += sb and not sn
            totals["support gained"] += sn and not sb
            if (b, sb) != (n, sn):
                changed.append("  %s %s: run %s; as built %s, %s; under 8.4 %s, %s" % (
                    ident, rows[k]["clause"], status, "held" if b else "not held",
                    "WELL-FOUNDED" if sb else "not well-founded", "held" if n else "not held",
                    "WELL-FOUNDED" if sn else "not well-founded"))
    print("== every claim of COMPAT-0's frozen texts, the court's fixtures and the examples that ran")
    for k, v in totals.items():
        print("  %-18s %d" % (k, v))
    print("== readings that change")
    print("\n".join(changed) if changed else "  none")
    print("== plants, each read on the case that must catch it (the rule must withhold; the plant must hold)")
    with open(os.path.join(ROOT, "tests", "fixtures", "court", "hoisted_omit.orl"), "rb") as fh:
        hoisted = fh.read()
    cases = [("never", "tests/fixtures/court/hoisted_omit.orl", hoisted),
             ("no-back-edge", "a claim before the refusal, in a loop with iterations left (inline)", LOOP_BEFORE)]
    caught = 0
    for plant, name, raw in cases:
        comp, lines = run(raw, 10 ** 8)
        (k, (_, rule_held, _, _)), = readings(comp, lines)[1].items()
        (_, (_, plant_held, _, _)), = readings(comp, lines, plant)[1].items()
        hit = not rule_held and plant_held
        caught += hit
        print("  %s: the rule %s; plant %s %s: %s" % (
            name, "withholds" if not rule_held else "HOLDS", plant, "holds" if plant_held else "withholds",
            "caught" if hit else "NOT CAUGHT"))
    ok = totals["held gained"] == 0 and totals["support gained"] == 0 and caught == 2
    print("COMPLETENESS PROBE %s: %d withheld, 0 gained required (%d held gained, %d support gained), plants %d/2" % (
        "HELD" if ok else "FAILED", totals["withheld by 8.4"], totals["held gained"], totals["support gained"],
        caught))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

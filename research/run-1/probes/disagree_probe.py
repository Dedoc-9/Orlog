"""EXPERIMENTAL RESEARCH PROBE. It is not the contract, and nothing in the program reads it; the proposal it supports is
research/run-1/SETTLEMENT-DEBATE.md, and its output is evidence/run1-disagree.txt.

The disagreement set between the court as built (R8) and CUT-0, classified by the resumption oracle and by cause.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/disagree_probe.py

For every claim of every refused run where R8 and CUT-0 disagree (meet_probe.py's TIGHTER and LOOSER claims):

- **the oracle** (research/run-1/manifold/resume_oracle.py's `Resumed`, the reference in which the refusing operation
  returns): the run is resumed with each of its eight values (`V`), under Rinf (every later refusal returns too: reading
  S2) and under R1 (a later refusal ends it). This is CUT-0's own counterfactual (CUT-0.md section 2): the same law, the
  same inputs, the same reference code, with only the refusing operation's result supplied. Each claim is classed:
    REFUTED      evaluated again after the cut, and false in at least one resumption;
    CONFIRMED    evaluated again, and true in every resumption that evaluated it;
    UNREACHED    evaluated again in no resumption tried (within the eight values);
    UNRESOLVED   evaluated again in none, but a resumption stopped at its budget, so the set is not closed;
    UNMODELLED   the cut's refusal is one the oracle does not model.
  Under E2, REFUTED and CONFIRMED are both justified withholdings (the run could have evaluated the claim again);
  REFUTED is the part where R8's HELD is contradicted by a resumption. UNREACHED is CUT-0's conservatism, as far as the
  eight values show.
- **the cause**: which parts of K-hat hold the claim (a loop's next pass, the rest of a block, the refused If's arms
  onward, the loop's own clause refused, the open claim), as independent labels, and the claim's place (in a loop
  body, in a procedure, at the top level). A claim held by one part alone is released if that part is removed: the
  ablation.

The tagged continuation is checked equal to cut0_claims.continuation on every run, and the oracle's prefix to the
reference's trace (resume_oracle's own checks).
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "manifold"))
import completeness_probe as SITE                                 # noqa: E402
import cut0_claims as C                                          # noqa: E402
import resume_oracle as O                                        # noqa: E402
from orlog.front import compile_bytes                            # noqa: E402
from orlog.interp import HostStop, Interp                        # noqa: E402
from orlog.syntax import Claim, For, IfS, Perform, ProcDef, While  # noqa: E402

CLASSES = ("REFUTED", "CONFIRMED", "UNREACHED", "UNRESOLVED", "UNMODELLED")
PARTS = ("a For's next pass", "a While's next pass", "the rest of a block", "the refused If's arms onward",
         "the loop's own clause refused", "a Perform refused", "the open claim")


class ResumedT(O.Resumed):
    """The oracle's resumed reference, also keeping each later evaluation's result."""

    def __init__(self, *a, **k):
        O.Resumed.__init__(self, *a, **k)
        self.results = {}

    def ev(self, kind, clause, payload):
        O.Resumed.ev(self, kind, clause, payload)
        if kind == b"C" and self.cut is not None:
            self.results.setdefault(struct.unpack(">I", payload[:4])[0], set()).add(payload[4])


def resume(comp, value, mode):
    it = ResumedT(comp.prog, comp.an, comp.law_seal, comp.text_seal, value=value, mode=mode, budget=O.RESUME_BUDGET)
    try:
        it.run()
        end = it.status
    except HostStop:
        end = "HOST-STOP"
    except O.Unmodelled as u:
        end = "UNMODELLED %s" % u
    return it, end


def tagged(prog, cut):
    """cut0_claims.continuation, each claim it adds labelled with the part that adds it."""
    r = C.Reach(prog)
    top = cut[-1]
    s = top["stmt"]
    tags = {}

    def add(ids, part):
        for i in ids:
            tags.setdefault(i, set()).add(part)
    if isinstance(s, Claim):
        add({s.id}, "the open claim")
    elif isinstance(s, IfS):
        add(r.arms_from(s, 0 if top["arm"] is None else top["arm"]), "the refused If's arms onward")
    elif isinstance(s, (For, While)):
        add(r.seq(top["clause"].children), "the loop's own clause refused")
    elif isinstance(s, Perform):
        add(r.proc(s.name), "a Perform refused")
    for i in range(len(cut) - 1, -1, -1):
        c = cut[i]["clause"]
        outer = cut[i - 1] if i > 0 else None
        if outer is not None and outer["clause"] is c:
            continue
        add(r.after(c), "the rest of a block")
        if outer is None:
            break
        if isinstance(outer["stmt"], (For, While)) and C.may_repeat(outer):
            add(r.seq(outer["clause"].children),
                "a For's next pass" if isinstance(outer["stmt"], For) else "a While's next pass")
    return tags


def place(cs):
    """Where a claim stands: in a loop body, in a procedure, or at the top level (labels, not exclusive)."""
    out, c = set(), cs.clause.parent
    while c is not None:
        if isinstance(c.stmt, (For, While)):
            out.add("in a loop body")
        if isinstance(c.stmt, ProcDef):
            out.add("in a procedure")
        c = c.parent
    return out or {"at the top level"}


def classify(raw, budget):
    """The run's disagreeing claims, each as (side, class under Rinf, class under R1, parts, place), or None."""
    comp = compile_bytes(raw)
    if not comp.ok or not comp.an.claims:
        return None
    try:
        it = C.CutInterp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
        plain = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
    except HostStop:
        return None
    if it.cut is None:
        return None
    lines = SITE.parse_receipt(plain.receipt("reference"))
    _, site, _ = SITE.readings(comp, lines)
    tags = tagged(comp.prog, it.cut)
    k = C.continuation(comp.prog, it.cut)
    assert set(tags) == k, "the tagged continuation is not the probe's"
    done = {}
    for l in lines:
        if l.startswith("claim "):
            p = l.split(" ")
            done[int(p[1])] = int(p[3]) > 0 and int(p[3]) == int(p[4])
    sites = {cs.stmt.id: cs for cs in comp.an.claims}
    differ = {}
    for i in sorted(site):
        r8, cut = site[i][0], done.get(i, False) and i not in k
        if r8 != cut:
            differ[i] = "TIGHTER" if r8 else "LOOSER"
    if not differ:
        return {"runs": 1, "rows": []}
    code = it.status.split(" ")[1]
    seen = {"R1": {}, "Rinf": {}}
    stopped = {"R1": False, "Rinf": False}
    unmodelled = code not in O.VALUE_CODES | O.PLAIN_CODES
    if not unmodelled:
        vals = O.V if code in O.VALUE_CODES else (None,)
        for mode in ("R1", "Rinf"):
            for v in (vals if mode == "R1" or code in O.VALUE_CODES else O.V):
                res, end = resume(comp, v, mode)
                if end.startswith("UNMODELLED"):
                    unmodelled = True
                    break
                stopped[mode] |= end == "HOST-STOP"
                for cid, rs in res.results.items():
                    seen[mode].setdefault(cid, set()).update(rs)
            if unmodelled:
                break
    rows = []
    for i, side in differ.items():
        cls = {}
        for mode in ("R1", "Rinf"):
            if unmodelled:
                cls[mode] = "UNMODELLED"
            elif i in seen[mode]:
                cls[mode] = "REFUTED" if 0 in seen[mode][i] else "CONFIRMED"
            else:
                cls[mode] = "UNRESOLVED" if stopped[mode] else "UNREACHED"
        rows.append((side, cls["Rinf"], cls["R1"], frozenset(tags.get(i, ())), frozenset(place(sites[i]))))
    return {"runs": 1, "rows": rows}


def report(name, results):
    rows = [row for r in results if r for row in r["rows"]]
    tight = [r for r in rows if r[0] == "TIGHTER"]
    loose = [r for r in rows if r[0] == "LOOSER"]
    print("== %s: %d refused runs with claims, %d disagreements (TIGHTER %d, LOOSER %d)" % (
        name, sum(r["runs"] for r in results if r), len(rows), len(tight), len(loose)))
    for side, group in (("TIGHTER", tight), ("LOOSER", loose)):
        if not group:
            continue
        for col, mode in ((1, "Rinf"), (2, "R1")):
            print("   %s under %-4s: %s" % (side, mode, ", ".join(
                "%s %d" % (c, sum(1 for r in group if r[col] == c)) for c in CLASSES)))
    if tight:
        print("   TIGHTER by part of K-hat (claims held there; held there alone, which the part's removal releases):")
        for part in PARTS:
            n = sum(1 for r in tight if part in r[3])
            if n:
                alone = [r for r in tight if r[3] == frozenset([part])]
                print("      %-32s %6d; alone %6d (%s)" % (part, n, len(alone), ", ".join(
                    "%s %d" % (c, sum(1 for r in alone if r[1] == c)) for c in CLASSES if any(r[1] == c for r in alone))))
        print("   TIGHTER by the claim's place:")
        for pl in ("in a loop body", "in a procedure", "at the top level"):
            grp = [r for r in tight if pl in r[4]]
            if grp:
                print("      %-32s %6d (%s)" % (pl, len(grp), ", ".join(
                    "%s %d" % (c, sum(1 for r in grp if r[1] == c)) for c in CLASSES if any(r[1] == c for r in grp))))
        combos = {}
        for r in tight:
            combos.setdefault(r[3], []).append(r[1])
        print("   TIGHTER by the exact set of parts (joint), largest first:")
        for parts, cl in sorted(combos.items(), key=lambda kv: (-len(kv[1]), sorted(kv[0]))):
            print("      %6d  {%s}: %s" % (len(cl), "; ".join(sorted(parts)), ", ".join(
                "%s %d" % (c, cl.count(c)) for c in CLASSES if c in cl)))
    return rows


def main():
    out = {}
    corpus = [classify(raw, budget) for _, raw, budget in C.corpus()]
    out["corpus"] = report("the cases, COMPAT-0's frozen texts, the fixtures and the examples", corpus)
    for which, templates in (("E", O.family_e()), ("G", O.family_g(10000, 26102026))):
        res = [classify(O.render(nodes, c), O.BUDGET) for nodes in templates for c in O.CS]
        out[which] = report("family %s" % which, res)
    rows = [r for g in out.values() for r in g]
    tight = [r for r in rows if r[0] == "TIGHTER"]
    loose = [r for r in rows if r[0] == "LOOSER"]
    n = {c: sum(1 for r in tight if r[1] == c) for c in CLASSES}
    nl = {c: sum(1 for r in loose if r[1] == c) for c in CLASSES}
    print("DISAGREEMENT CLASSIFIED: TIGHTER %d under Rinf: %s; LOOSER %d: %s" % (
        len(tight), ", ".join("%s %d" % (c, n[c]) for c in CLASSES), len(loose),
        ", ".join("%s %d" % (c, nl[c]) for c in CLASSES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

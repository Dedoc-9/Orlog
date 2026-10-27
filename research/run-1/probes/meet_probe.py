"""EXPERIMENTAL RESEARCH PROBE. It is not the contract, and nothing in the program reads it; the proposal it supports is
research/run-1/SETTLEMENT-DEBATE.md, and its output is evidence/run1-meet.txt.

The meet of the court as built (R8) and CUT-0: a claim is held only when both rules hold it.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/meet_probe.py

Every claim of every refused run is read three ways: by the court as built (R8, `src/orlog/court.py`'s panel, through
completeness_probe.readings), by CUT-0 (every completed evaluation true and not in K-hat, cut0_claims.continuation), and
by their meet. Support is the court's own least fixed point (court.support_sets) over each reading's held claims.

Checks:
- the classes, claim by claim: both held; both withheld; TIGHTER (R8 holds, CUT-0 withholds: what the meet adds to R8);
  LOOSER (CUT-0 holds, R8 withholds: CUT-0's gains, which the meet forgoes);
- the meet is never looser than R8: no claim held, and no claim supported, that R8 does not hold or support. The first
  is the meet's definition; the second is T8 (withholding never raises a standing), measured here run by run;
- the plant `join` (either rule's hold is enough) must hold or support a claim R8 does not, wherever CUT-0 gains.

Sources: this probe's cases (cut0_claims.CASES), COMPAT-0's frozen texts, the fixtures and the examples, and the
manifold debate's families E and G.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "manifold"))
import completeness_probe as SITE                                 # noqa: E402
import cut0_claims as C                                          # noqa: E402
from orlog import court as CT                                    # noqa: E402
from orlog.front import compile_bytes                            # noqa: E402
from orlog.interp import HostStop, Interp                        # noqa: E402

PLANT = None    # "join": a claim is held when either rule holds it


def readings(raw, budget):
    """{claim id: (R8 held, CUT-0 held, combined held, R8 supported, combined supported)} of a refused run, or None."""
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
    assert it.receipt() == plain.receipt(), "the instrumented reference wrote another receipt"
    lines = SITE.parse_receipt(plain.receipt("reference"))
    _, site, _ = SITE.readings(comp, lines)
    k = C.continuation(comp.prog, it.cut)
    done = {}
    for l in lines:
        if l.startswith("claim "):
            p = l.split(" ")
            done[int(p[1])] = int(p[3]) > 0 and int(p[3]) == int(p[4])
    ids = set(site)
    r8 = {i: site[i][0] for i in ids}
    cut = {i: done.get(i, False) and i not in k for i in ids}
    comb = {i: (r8[i] or cut[i]) if PLANT == "join" else (r8[i] and cut[i]) for i in ids}
    prem = {s.stmt.id: {comp.prog.by_label[p].stmt.id for p in s.stmt.premises} for s in comp.an.claims}
    sup_r8, _ = CT.support_sets(ids, r8, prem)
    sup_comb, _ = CT.support_sets(ids, comb, prem)
    return {i: (r8[i], cut[i], comb[i], i in sup_r8, i in sup_comb) for i in ids}


def new_stats():
    return {"runs": 0, "claims": 0, "both held": 0, "both withheld": 0, "TIGHTER": 0, "LOOSER": 0,
            "held above R8": 0, "supported above R8": 0}


def tally(rd, st, looser_at=None, name=None):
    if rd is None:
        return
    st["runs"] += 1
    for i, (r8, cut, comb, s8, sc) in sorted(rd.items()):
        st["claims"] += 1
        if r8 and cut:
            st["both held"] += 1
        elif not r8 and not cut:
            st["both withheld"] += 1
        elif r8:
            st["TIGHTER"] += 1
        else:
            st["LOOSER"] += 1
            if looser_at is not None:
                looser_at.append("%s claim %d" % (name, i))
        st["held above R8"] += comb and not r8
        st["supported above R8"] += sc and not s8


def survey(label):
    out = {}
    print("== %s" % label)
    st, looser = new_stats(), []
    for ident, raw, budget in C.corpus():
        tally(readings(raw, budget), st, looser, ident)
    print("   the cases, COMPAT-0's frozen texts, the fixtures and the examples: %s" % st)
    if looser:
        print("   LOOSER at: %s" % ", ".join(looser))
    out["corpus"] = st
    import resume_oracle as O
    for which, templates in (("E", O.family_e()), ("G", O.family_g(10000, 26102026))):
        s = new_stats()
        for nodes in templates:
            for c in O.CS:
                tally(readings(O.render(nodes, c), O.BUDGET), s)
        out[which] = s
        print("   family %s: %s" % (which, s))
    return out


def main():
    global PLANT
    meet = survey("the meet: held only when R8 and CUT-0 both hold")
    tot = {k: sum(meet[g][k] for g in meet) for k in new_stats()}
    PLANT = "join"
    join = survey("the plant join: held when either holds (must rise above R8 wherever CUT-0 gains)")
    PLANT = None
    jtot = {k: sum(join[g][k] for g in join) for k in new_stats()}
    never_looser = tot["held above R8"] == 0 and tot["supported above R8"] == 0
    caught = jtot["held above R8"] > 0 and jtot["held above R8"] == tot["LOOSER"]
    ok = never_looser and caught
    print("MEET PROBE %s: %d refused runs, %d claims; the meet never above R8 (%d held, %d supported); TIGHTER %d, "
          "LOOSER %d; the join rises above R8 on %d claims, its plant %s" % (
              "HELD" if ok else "FAILED", tot["runs"], tot["claims"], tot["held above R8"], tot["supported above R8"],
              tot["TIGHTER"], tot["LOOSER"], jtot["held above R8"], "caught" if caught else "NOT CAUGHT"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

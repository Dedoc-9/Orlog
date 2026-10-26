"""The court plants that court_mutants.py reports as surviving the self-test are not equivalent mutants: on a small
fixture each planted court reads something the court as built does not.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/unguarded_held.py

Each case runs one fixture through the arbiter (python backend; c99 too for the INCOMPLETE case), then reads the same
receipt, witness and ledger (every claim's seal ratified, in memory) with the court as built and with the planted copy
(src/orlog/court.py with one line replaced, loaded in memory). A case prints both readings and NOT EQUIVALENT when they
differ. The file on disk is never written.
"""
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402

HELD = 'held = hit is None and r["evals"] > 0 and r["trues"] == r["evals"] and row["integrity"] == "AGREED"'
PLANTS = {
    "held-ignores-integrity": [(HELD, 'held = hit is None and r["evals"] > 0 and r["trues"] == r["evals"]')],
    "held-ignores-refutation": [(HELD, 'held = hit is None and r["evals"] > 0 and row["integrity"] == "AGREED"')],
    "held-ignores-unreached": [(HELD, 'held = hit is None and r["trues"] == r["evals"] and row["integrity"] == "AGREED"')],
    "agreed-always": [('agreed = witness.get("dissent_kind") == "NONE" and bool(witness.get("backends"))',
                       'agreed = True')],
    "sandwich-ignores-dissent": [('    elif not agreed:\n        sandwich = "VACUOUS (the backends did not all agree)"\n',
                                  '')],
    "summary-grounded-counts-all": [('"grounded": sum(1 for r in out if r["grounding"] == "GROUNDED"),',
                                     '"grounded": len(out),')],
    "summary-well-founded-counts-unsupported": [
        ('"well_founded": sum(1 for r in out if r["support"] == "WELL-FOUNDED"),',
         '"well_founded": sum(1 for r in out if r["support"] in ("WELL-FOUNDED", "UNSUPPORTED")),')],
}


def arbitrate(name, fixture, backends=("python",), **kw):
    arb = Arbiter(C.workdir("unguarded"), backends=backends, **kw)
    comp, w, ref = arb.arbitrate(C.fixture(fixture), "ug-" + name)
    return comp, w, parse_receipt(ref.receipt())


def reading(court, comp, w, rec):
    p = court.panel(comp, w, rec, C.ledger_all(comp))
    rows = C.show_rows(p)
    s = p["summary"]
    return rows + ["summary: sandwich=%s; well_founded=%d; grounded=%d; unsupported=%d; unreached=%d" % (
        s["sandwich"], s["well_founded"], s["grounded"], s["unsupported"], s["unreached"])]


def case(title, plant, comp, w, rec):
    real = reading(COURT, comp, w, rec)
    mod = C.planted("court", PLANTS[plant])
    got = reading(mod, comp, w, rec)
    differ = real != got
    print("== %s, plant %s (dissent kind %s, agreeing [%s], dissenting [%s], did not build [%s])" % (
        title, plant, w["dissent_kind"], ",".join(w["agreeing"]), ",".join(w["dissenting"]),
        ",".join(w.get("build_failed", []))))
    for a, b in zip(real, got):
        print("   court   %s" % a)
        if a != b:
            print("   planted %s" % b)
    print("   %s" % ("NOT EQUIVALENT: the planted court reads differently" if differ else
                     "EQUIVALENT here: the planted court reads the same"))
    return differ


def main():
    results = {}
    # R1, CONTESTED: the self-test's reference plant, a claim true in every execution
    with_ref = dict(reference_patch=C.reference_truncates_quotient)
    comp, w, rec = arbitrate("contested", "contested_true.orl", **with_ref)
    results["held-ignores-integrity (CONTESTED)"] = case("a contested run", "held-ignores-integrity", comp, w, rec)
    results["agreed-always"] = case("a contested run", "agreed-always", comp, w, rec)
    results["sandwich-ignores-dissent"] = case("a contested run", "sandwich-ignores-dissent", comp, w, rec)
    # R1, INCOMPLETE: a backend that did not build (the self-test's honesty row, on collatz)
    comp, w, rec = arbitrate("incomplete", "contested_true.orl", backends=("python", "c99"),
                             mutate=lambda b, src: src + "\nthis is not C\n" if b == "c99" else src)
    results["held-ignores-integrity (INCOMPLETE)"] = case("a backend that did not build", "held-ignores-integrity",
                                                          comp, w, rec)
    # a claim false at its first evaluation, every backend agreeing
    comp, w, rec = arbitrate("refuted", "refuted_claim.orl")
    results["held-ignores-refutation"] = case("a refuted claim", "held-ignores-refutation", comp, w, rec)
    results["summary-well-founded-counts-unsupported"] = case("a refuted claim",
                                                              "summary-well-founded-counts-unsupported", comp, w, rec)
    results["summary-grounded-counts-all"] = case("a refuted claim", "summary-grounded-counts-all", comp, w, rec)
    # R7: a claim never evaluated
    comp, w, rec = arbitrate("unreached", "unreached.orl")
    results["held-ignores-unreached"] = case("an unreached claim", "held-ignores-unreached", comp, w, rec)
    print("NOT EQUIVALENT: %d of %d (%s)" % (sum(results.values()), len(results),
                                             ", ".join(k for k, v in results.items() if not v) or "every case differs"))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

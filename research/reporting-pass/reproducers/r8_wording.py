"""R8's split between 'exact' and 'possible', against where each clause's evaluations actually happen.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/r8_wording.py

refusal_in_claim reads 'exact' only when the claim is its clause's own statement. A plain Otherwise clause keeps its
RawIf as its statement (syntax._attach_otherwise), so its inline claim reads 'possible', and the court prints that the
refusal "may come from the condition or the other arm its clause holds". The reference evaluates nothing else under an
Otherwise clause's id: no condition (an else arm has none, interp.IfS) and no other arm (the arms before it are their
own clauses). The trace says which statement refused: the last event before the R event.

Each case: the reading R8 gives, and the events of the reference's trace at the refusing clause in its last iteration.
"""
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import parse_receipt  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402

CASES = [
    ("a plain Otherwise clause's claim refuses (fixtures/otherwise_claim.orl)", C.fixture("otherwise_claim.orl")),
    ("an 'Otherwise, if' clause: its own condition refuses", (
        "§1 Let xs be a list of 16 copies of 1.\n§2 For each i from 1 to 17, do the following.\n§2.1 If false, say 0.\n"
        "§2.2 Otherwise, if item i of xs equals 1, we claim that true, by the owner.\n").encode("utf-8")),
    ("an If's own clause: its condition refuses (tests/fixtures/r8/inline_condition.orl)",
     C.read("tests/fixtures/r8/inline_condition.orl")),
    ("a claim that is its clause's statement (tests/fixtures/r8/omit.orl)", C.read("tests/fixtures/r8/omit.orl")),
    ("control: the If's condition before an Otherwise refuses, and the status names the If's own clause", (
        "§1 Let xs be a list of 16 copies of 1.\n§2 For each i from 1 to 17, do the following.\n"
        "§2.1 If item i of xs equals 0, say 0.\n§2.2 Otherwise, we claim that true, by the owner.\n").encode("utf-8")),
]


def main():
    miswords = 0
    for title, raw in CASES:
        comp = compile_bytes(raw)
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, trace=True).run()
        p = COURT.panel(comp, {"dissent_kind": "NONE", "backends": {"python": {}}}, parse_receipt(it.receipt()), [])
        code, clause = it.status.split(" ")[1], int(it.status.split(" ")[2])
        site = [s for s in comp.an.claims if s.id == clause]
        hit = COURT.refusal_in_claim(site[0], (code, clause)) if site else None
        labels = {c.id: c.label for c in comp.prog.clauses}
        print("== %s" % title)
        print("   status %s (clause %d is §%s); the claim's clause holds %s; R8 reads %r" % (
            it.status, clause, labels.get(clause, "?"), type(site[0].clause.stmt).__name__ if site else
            "no claim (the refusing clause holds none)", hit))
        for r in p["rows"]:
            print("   %s %s" % (r["clause"], r["evaluation"]))
        if hit == "possible" and type(site[0].clause.stmt).__name__ == "RawIf" and raw.find(b"Otherwise, we") >= 0:
            miswords += 1
            print("   -> the clause is a plain Otherwise: it evaluates no condition and holds no other arm, so the "
                  "refusal can only have come from the claim; the reading's 'may come from the condition or the "
                  "other arm' names a condition and an arm that clause does not have")
    print("R8 WORDING: %d reading(s) name a condition or an arm the clause does not hold" % miswords)
    return 0


if __name__ == "__main__":
    sys.exit(main())

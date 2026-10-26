"""What the court's summary line (the last line `orl.py court` prints) can tell apart.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/summary_absorbs.py

Five one-claim texts whose claim is not held for five different reasons, each read by the court (python backend; the
contested one under the self-test's reference plant). The summary keys are claims, well_founded, circular, unreached,
unsupported, grounded, sandwich, ledger_entries: a claim that was refuted, one R8 withholds, one whose run the backends
contested, one whose backend did not build and one whose premise was never evaluated are all counted `unsupported`.
"""
import json
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402

PREMISE = ("Note: a claim whose premise is never evaluated.\n§1 Let a be 1.\n§2 If a equals 2, do the following.\n"
           "§2.1 We claim that a equals 2, by the owner.\n§3 We claim that a equals 1, by the owner, given §2.1.\n")


def main():
    wd = C.workdir("summary")
    cases = [
        ("refuted", C.fixture("refuted_claim.orl"), {}),
        ("withheld by R8", C.read("tests/fixtures/r8/omit.orl"), {}),
        ("contested", C.fixture("contested_true.orl"), {"reference_patch": C.reference_truncates_quotient}),
        ("a backend did not build", C.fixture("contested_true.orl"),
         {"backends": ("python", "c99"), "mutate": lambda b, s: s + "\nthis is not C\n" if b == "c99" else s}),
        ("its premise unreached", PREMISE.encode("utf-8"), {}),
    ]
    lines = {}
    for name, raw, kw in cases:
        kw = dict(kw)
        backends = kw.pop("backends", ("python",))
        comp, w, ref = Arbiter(wd, backends=backends, **kw).arbitrate(raw, "sum-" + name.split(" ")[0])
        p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
        s = dict(p["summary"])
        last = [r for r in p["rows"]][-1]
        print("== %s: the claim reads %s; %s" % (name, last["evaluation"][:60], last["support"]))
        print("   summary %s" % json.dumps(s, sort_keys=True))
        s.pop("sandwich")
        lines[name] = json.dumps(s, sort_keys=True)
    told = len(set(lines.values()))
    print("SUMMARY: %d distinct summaries (sandwich aside) for %d different reasons a claim is not held" % (
        told, len(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

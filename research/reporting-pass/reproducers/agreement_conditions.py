"""The arbiter's agreement predicate has four conditions: a receipt, its core equal to the reference's, the output file
equal to the reference's output, and exit status 0. court_mutants.py plants the removal of the last two, and the
pre-E7 comparison in place of the second; this shows that no one of the three plants is an equivalent mutant.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/agreement_conditions.py

Three Python backends are made through the arbiter's own mutate hook (the generated source, edited in memory):
  exit-5        the runtime writes its output and receipt whole, as always, then exits with status 5;
  extra-byte    the runtime appends bytes to its output file after the receipt's output-sha256 was computed, so the
                receipt is right and the file is not;
  crlf-receipt  the runtime writes its receipt with CR LF line ends (red team E7's first case).
Each is arbitrated by the arbiter as built and by a planted copy (src/orlog/arbiter.py with the one condition changed,
loaded in memory). NOT EQUIVALENT when the two verdicts differ.
"""
import sys

import _common as C

C.require_env()
from orlog.arbiter import Arbiter  # noqa: E402

COND = 'and r.get("out") == bytes(ref.out) and r.get("exit") == 0)'
CORE = 'ok = (r.get("receipt") is not None and receipt_core(r["receipt"]) == ref_core and ref_core is not None'
PLANTED = {"agreement-ignores-exit": [(COND, 'and r.get("out") == bytes(ref.out))')],
           "agreement-ignores-output": [(COND, 'and r.get("exit") == 0)')],
           "agreement-lenient-receipts": [(CORE, 'ok = (r.get("receipt") is not None and parse_receipt(r["receipt"]) '
                                                 '== parse_receipt(ref.receipt())')]}
FINISH = '        self._receipt("COMPLETED")\n        _sys.exit(0)'
CLOSE = '        self.out.close()\n        if self.trace is not None:\n            self.trace.close()'
LF = 'fh.write(("\\n".join(lines) + "\\n").encode("ascii"))'
MUTANTS = {
    "exit-5": (FINISH, '        self._receipt("COMPLETED")\n        _sys.exit(5)'),
    "extra-byte": (CLOSE, '        self.out.write(b"planted extra bytes\\n")\n' + CLOSE),
    "crlf-receipt": (LF, 'fh.write(("\\r\\n".join(lines) + "\\r\\n").encode("ascii"))'),
}
PAIRS = (("agreement-ignores-exit", "exit-5"), ("agreement-ignores-output", "extra-byte"),
         ("agreement-lenient-receipts", "crlf-receipt"))


def mutate_with(old, new):
    def m(backend, src):
        if backend != "python":
            return src
        if src.count(old) != 1:
            raise SystemExit("the generated source holds the mutant's anchor %d times" % src.count(old))
        return src.replace(old, new)
    return m


def verdict(arbiter_cls, mutant):
    old, new = MUTANTS[mutant]
    arb = arbiter_cls(C.workdir("agreement"), backends=("python",), mutate=mutate_with(old, new))
    comp, w, ref = arb.arbitrate(C.read("examples/collatz.orl"), "ag-" + mutant)
    b = w["backends"]["python"]
    return "%s agreeing [%s] dissenting [%s] (backend exit %s, status %s)" % (
        w["dissent_kind"], ",".join(w["agreeing"]), ",".join(w["dissenting"]), b.get("exit"), b.get("status"))


def main():
    differ = 0
    for plant, mutant in PAIRS:
        mod = C.planted("arbiter", PLANTED[plant])
        real, got = verdict(Arbiter, mutant), verdict(mod.Arbiter, mutant)
        print("== backend %s, plant %s" % (mutant, plant))
        print("   arbiter %s" % real)
        print("   planted %s" % got)
        print("   %s" % ("NOT EQUIVALENT" if real != got else "EQUIVALENT here"))
        differ += real != got
    print("NOT EQUIVALENT: %d of %d" % (differ, len(PAIRS)))
    return 0 if differ == len(PAIRS) else 1


if __name__ == "__main__":
    sys.exit(main())

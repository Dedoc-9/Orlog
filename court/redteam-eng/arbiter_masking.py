"""Does a backend's build failure hide a REFERENCE-DISSENT?

The reference is planted wrong (its quotient truncates: the self-test's own plant, reference_truncates_quotient).
Python and C99 agree with each other against it. Run 1: backends python,c99 -> REFERENCE-DISSENT, as designed.
Run 2: the same, plus a Rust backend whose source is planted not to compile. The two compiled backends still agree
with each other against the reference; a sound arbiter still says REFERENCE-DISSENT.
  python -B arbiter_masking.py
"""
import contextlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog import numeric_ref as N  # noqa: E402
from orlog.arbiter import Arbiter  # noqa: E402


@contextlib.contextmanager
def reference_truncates_quotient():
    saved = N.i_quot

    def trunc(a, b):
        if b == 0:
            raise N.Refusal("DIVISION-BY-ZERO")
        q = abs(a) // abs(b)
        return N.chk(q if (a < 0) == (b < 0) else -q)
    N.i_quot = trunc
    try:
        yield
    finally:
        N.i_quot = saved


def break_rust(b, src):
    return src + "\nthis is not rust\n" if b == "rust" else src


def main():
    prog = "§1 Say the quotient of -7 by 2.\n".encode("utf-8")
    wd = os.path.join(HERE, "work", "arbiter-masking")
    a1 = Arbiter(wd, backends=("python", "c99"), reference_patch=reference_truncates_quotient)
    comp, w, ref = a1.arbitrate(prog, "mask-1")
    print("run 1 backends python,c99:      dissenting %s  kind %s" % (w["dissenting"], w["dissent_kind"]))
    a2 = Arbiter(wd, backends=("python", "c99", "rust"), reference_patch=reference_truncates_quotient,
                 mutate=break_rust)
    comp, w, ref = a2.arbitrate(prog, "mask-2")
    print("run 2 + rust that fails to build: dissenting %s  kind %s  (notes: %s)"
          % (w["dissenting"], w["dissent_kind"], [n["kind"] for n in w["mismatch_notes"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

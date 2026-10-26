"""Plants a backend whose receipt is NOT byte-identical to the reference's, and asks the arbiter.

Each plant changes only how the Python backend writes its receipt (the contract: LF only, byte-identical
except the backend line, RUNTIME-SPEC 1 and 7). A sound arbiter must list the backend as dissenting.
  python -B arbiter_plants.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.arbiter import Arbiter  # noqa: E402

PROG = "§1 Let n be 6.\n§2 Say n times 7.\n".encode("utf-8")

ORIG = '            fh.write(("\\n".join(lines) + "\\n").encode("ascii"))'
PLANTS = {
    "receipt-crlf": '            fh.write(("\\r\\n".join(lines) + "\\r\\n").encode("ascii"))',
    "receipt-no-final-newline": '            fh.write(("\\n".join(lines)).encode("ascii"))',
    "receipt-extra-backend-line": '            fh.write(("\\n".join(lines[:6] + ["backend ops 0 trust me"] + lines[6:]) + "\\n").encode("ascii"))',
}


def main():
    wd = os.path.join(HERE, "work", "arbiter-plants")
    for name, repl in PLANTS.items():
        def mutate(b, src, repl=repl):
            if b != "python":
                return src
            assert ORIG in src, "the plant's anchor moved"
            return src.replace(ORIG, repl, 1)
        arb = Arbiter(wd, backends=("python", "c99"), mutate=mutate)
        comp, w, ref = arb.arbitrate(PROG, "plant-" + name)
        rec = open(os.path.join(wd, "plant-%s-python.receipt" % name), "rb").read()
        same = rec == ref.receipt().replace(b"backend reference", b"backend python")
        print("%-28s receipt byte-identical to the reference's (backend line aside): %-5s  arbiter: agree %s dissent %s"
              % (name, same, w["agreeing"], w["dissenting"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

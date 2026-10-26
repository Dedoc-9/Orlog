"""E11: runs the C99 backend of collatz.orl with its files in a folder named after the language, prints exit and stderr.

  python -B e11_c_stderr.py
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.arbiter import Arbiter  # noqa: E402


def main():
    wd = os.path.join(HERE, "work", "ØRLǪG")
    arb = Arbiter(wd, backends=("c99",))
    comp, w, ref = arb.arbitrate(open(os.path.join(ROOT, "examples", "collatz.orl"), "rb").read(), "collatz")
    print("arbiter summary for c99:", w["backends"]["c99"])
    exe = [p for p in glob.glob(os.path.join(wd, "cache", "c99-*.exe"))
           if os.path.exists(p[:-4] + ".c") and comp.seal_words.encode() in open(p[:-4] + ".c", "rb").read(400)][0]
    r = arb.run([exe], "collatz-c99-probe")
    print("exit %d, stderr %r" % (r["exit"], r["stderr"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

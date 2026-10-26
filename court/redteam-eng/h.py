"""Red-team harness: compile one .orl file, run the reference and the backends, print what differs.

  python -B h.py FILE.orl [--backends python,c99] [--show] [--trace]
Writes only under court/redteam-eng/work.
"""
import argparse
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--backends", default="python,c99")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--workdir", default=os.path.join(HERE, "work"))
    a = ap.parse_args()
    raw = open(a.file, "rb").read()
    try:
        comp = compile_bytes(raw)
    except Exception:
        print("FRONT END CRASHED (uncaught exception, no refusal):")
        traceback.print_exc(limit=3, file=sys.stdout)
        return 3
    if not comp.ok:
        print("REFUSED %s at line %s: %s" % (comp.error.code, comp.error.line, comp.error.msg))
        return 1
    print("law %s (%s)" % (comp.law_seal[:16], comp.seal_words))
    arb = Arbiter(a.workdir, backends=tuple(a.backends.split(",")))
    name = os.path.splitext(os.path.basename(a.file))[0]
    comp, w, ref = arb.arbitrate(raw, name)
    print("reference: %s  ops %d  events %d" % (ref.status, ref.ops, ref.events))
    print("agree %s  dissent %s  kind %s" % (w["agreeing"], w["dissenting"], w["dissent_kind"]))
    for n in w["mismatch_notes"]:
        print("  NOTE", n)
    for b, s in w["backends"].items():
        print("  %-7s %s" % (b, s))
    if a.show:
        print("--- reference output ---")
        sys.stdout.write(bytes(ref.out).decode("utf-8", "replace"))
        print("--- reference receipt ---")
        sys.stdout.write(ref.receipt().decode())
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Runs one program's Python backend (as the arbiter builds it) and prints its exit status and stderr tail.

  python -B show_stderr.py FILE.orl
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.arbiter import Arbiter, generate  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.lower import Lowered  # noqa: E402


def main():
    raw = open(sys.argv[1], "rb").read()
    comp = compile_bytes(raw)
    arb = Arbiter(os.path.join(HERE, "work", "stderr"), backends=("python",))
    cmd, how, key = arb.build("python", generate("python", Lowered(comp)))
    r = arb.run(cmd, "stderr-probe")
    print("python backend exit %d; stderr tail:" % r["exit"])
    print("\n".join(r["stderr"].strip().splitlines()[-3:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

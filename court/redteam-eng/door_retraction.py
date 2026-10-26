"""E18: the door applied twice. A retraction would give the same text, with no repair on the second pass.

  python -B door_retraction.py [FILE]      (default: E18_door_not_idempotent.raw)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.canon import canonicalize  # noqa: E402


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "E18_door_not_idempotent.raw")
    raw = open(path, "rb").read()
    c1 = canonicalize(raw)
    print("raw     %r" % raw.decode("utf-8"))
    print("pass 1  %r  events %s" % (c1.text, [(e["cls"], e["rule"]) for e in c1.events]))
    c2 = canonicalize(c1.text.encode("utf-8"))
    print("pass 2  %r  events %s" % (c2.text, [(e["cls"], e["rule"]) for e in c2.events]))
    print("fixed point: %s" % (c2.text == c1.text and not c2.repairs))
    return 0


if __name__ == "__main__":
    sys.exit(main())

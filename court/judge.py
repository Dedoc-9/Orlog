"""The judge: the court's own record, decided by Orlog's court engine (Dung's grounded semantics).

The record is court/record.json:
  {"arguments": {"ID": {"by": "doctrine|prosecution-logic|prosecution-novelty|redteam|twin|defence|judge",
                        "text": "..."}},
   "attacks": [["ATTACKER", "TARGET"], ...]}
A doctrine claim stands (IN) only if every finding against it is itself defeated by an argument that
stands; it falls (OUT) if an argument that stands attacks it; otherwise it is UNDECIDED and goes to the
owner. The judge writes the attack relation; the engine decides it. The verdict is schedule-independent
(least fixed point) and says nothing about truth: it is standing under the record as written.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from orlog.court import grounded_extension  # noqa: E402


def main():
    with open(os.path.join(HERE, "record.json"), "rb") as fh:
        rec = json.loads(fh.read().decode("utf-8"))
    args = set(rec["arguments"])
    attacks = set((a, b) for a, b in rec["attacks"])
    unknown = sorted(x for pair in attacks for x in pair if x not in args)
    if unknown:
        print("UNKNOWN ARGUMENTS IN ATTACKS:", unknown)
        return 2
    inn, out, und = grounded_extension(args, attacks)
    lines = []
    for status, group in (("IN", inn), ("OUT", out), ("UNDECIDED", und)):
        for a in sorted(group):
            info = rec["arguments"][a]
            lines.append("%-9s %-14s %-20s %s" % (status, a, info["by"], info["text"]))
    text = "\n".join(lines) + "\n"
    with open(os.path.join(HERE, "VERDICT.txt"), "wb") as fh:
        fh.write(text.encode("utf-8"))
    sys.stdout.write(text)
    doctrine = [a for a in args if rec["arguments"][a]["by"] == "doctrine"]
    print("doctrine claims: %d IN, %d OUT, %d UNDECIDED" % (
        sum(1 for a in doctrine if a in inn), sum(1 for a in doctrine if a in out),
        sum(1 for a in doctrine if a in und)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

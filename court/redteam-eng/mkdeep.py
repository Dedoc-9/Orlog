"""Writes deep-structure candidates: a long If chain, and deeply nested loops (valid programs)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cand")


def chain(n):
    lines = ["§1 Let x be %d." % n, "§2 If x = 0, say 0."]
    for k in range(1, n + 1):
        lines.append("§%d Otherwise, if x = %d, say %d." % (k + 2, k, k))
    return "\n".join(lines) + "\n"


def nested_for(depth):
    lines = []
    label = []
    for d in range(depth):
        label.append("1")
        lines.append("§%s For each i%d from 1 to 1, do the following." % (".".join(label), d))
    label.append("1")
    lines.append("§%s Say \"deep\"." % ".".join(label))
    return "\n".join(lines) + "\n"


def write(name, text):
    with open(os.path.join(OUT, name), "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("wrote", name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n in (90, 110, 300):
        write("c22_if_chain_%d.orl" % n, chain(n))
    for d in (40, 60):
        write("c23_nested_for_%d.orl" % d, nested_for(d))

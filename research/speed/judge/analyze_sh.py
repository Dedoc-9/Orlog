"""The judge's measurement for research/speed, read back: the four executions' agreement and operation counts from the
arbiter's witnesses, and the Q31.32 values' error against binary64 evaluated from the same lattice directions.
  PYTHONHASHSEED=0 python -B research/speed/judge/analyze_sh.py
"""
import json
import math
import os
from fractions import Fraction

# the judge's scripts live in research/speed/judge/; what they make and read lives in work/speed-judge/, which
# git ignores
HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "work",
                                     "speed-judge"))
RUNS = os.path.join(HERE, "runs")
ULP = Fraction(1, 1 << 32)


def witness(path):
    with open(path, "rb") as fh:
        w = json.loads(fh.read().decode("utf-8"))["data"]
    b = w["backends"]
    cores = {name: (v.get("receipt_core_sha256", v.get("receipt_sha256")), v["ops"], v["events"],
                    v["trace_head"], v["output_sha256"])
             for name, v in b.items()}
    return w, cores


def agreement(name, path):
    w, cores = witness(path)
    same = len(set(cores.values())) == 1
    ops = int(next(iter(cores.values()))[1])
    print("%-10s dissent %-5s agreeing %-20s receipt cores identical: %s  ops %d  events %s" % (
        name, w["dissent_kind"], ",".join(w["agreeing"]), "yes" if same else "NO", ops,
        next(iter(cores.values()))[2]))
    return ops


def basis64(i, j, k):
    n = math.sqrt(i * i + j * j + k * k)
    x, y, z = i / n, j / n, k / n
    pi = math.pi
    c0 = 1 / (2 * math.sqrt(pi))
    c1 = math.sqrt(3 / (4 * pi))
    c2 = 0.5 * math.sqrt(15 / pi)
    c3 = 0.25 * math.sqrt(5 / pi)
    c4 = 0.25 * math.sqrt(15 / pi)
    return [c0, c1 * y, c1 * z, c1 * x, c2 * x * y, c2 * y * z, c3 * (3 * z * z - 1), c2 * x * z, c4 * (x * x - y * y)]


def main():
    print("== agreement across the four executions (the reference and python, c99, rust)")
    agreement("say R4", os.path.join(RUNS, "witness-say-r4.json", "sh_say_r4.witness.json"))
    o4 = agreement("sum R4", os.path.join(RUNS, "witness", "sh_sum_r4.witness.json"))
    o8 = agreement("sum R8", os.path.join(RUNS, "witness", "sh_sum_r8.witness.json"))
    n4, n8 = 9 ** 3 - 1, 17 ** 3 - 1
    print("== cost in counted operations (exact)")
    print("  R4: %d directions, %d ops, %.1f ops a direction overall" % (n4, o4, o4 / n4))
    print("  R8: %d directions, %d ops, %.1f ops a direction overall" % (n8, o8, o8 / n8))
    print("  by difference (R8 - R4): %.1f ops a direction, the loop's own steps included" % ((o8 - o4) / (n8 - n4)))
    print("== error of the Q31.32 values against binary64 at the same direction (R4, every value said)")
    worst = [Fraction(0)] * 9
    where = [None] * 9
    total = 0
    with open(os.path.join(RUNS, "show-say-r4.txt"), "rb") as fh:
        for raw in fh.read().decode("utf-8").splitlines():
            parts = raw.split()
            if len(parts) != 12 or parts[0] == "directions":
                continue
            i, j, k = (int(p) for p in parts[:3])
            fix = [Fraction(p) for p in parts[3:]]
            ref = basis64(i, j, k)
            total += 1
            for m in range(9):
                e = abs(fix[m] - Fraction(ref[m]))
                if e > worst[m]:
                    worst[m], where[m] = e, (i, j, k)
    print("  directions read: %d" % total)
    for m in range(9):
        print("  Y%d  worst |error| %.3e = %.2f units of 2^-32, at %s" % (m, float(worst[m]), float(worst[m] / ULP),
                                                                        where[m]))
    print("  overall worst: %.2f units of 2^-32 (%.3e)" % (float(max(worst) / ULP), float(max(worst))))


if __name__ == "__main__":
    main()

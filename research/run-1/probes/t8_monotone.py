"""T8 (ROUNDS.md): withholding held claims never raises a claim's support. The court's own support_sets is checked
against the lemma over every premise graph of up to three claims, every set of held claims and every set withheld
from it, and over a fixed sample of four-claim graphs.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/t8_monotone.py

The lemma, proved in ROUNDS.md: for base' a subset of base, lfp' is a subset of lfp and gfp' a subset of gfp, so a
claim's standing (2 well-founded, 1 circular, 0 otherwise) never rises. The plant drops a withheld claim from its
dependents' premises, a court that reads a withheld premise as no premise; the check must find a graph it breaks,
and prints the smallest.
"""
import itertools
import os
import random
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.court import support_sets                            # noqa: E402


def standing(ids, base, prem):
    lo, hi = support_sets(ids, base, prem)
    return {c: 2 if c in lo else 1 if c in hi else 0 for c in ids}, lo, hi


def violations(n, prem, base, withheld, plant):
    ids = set(range(n))
    before, lo, hi = standing(ids, {c: c in base for c in ids}, prem)
    after_prem = {c: prem[c] - withheld for c in ids} if plant else prem
    after, lo2, hi2 = standing(ids, {c: c in base and c not in withheld for c in ids}, after_prem)
    return not (lo2 <= lo and hi2 <= hi and all(after[c] <= before[c] for c in ids))


def graphs(n):
    pairs = [(a, b) for a in range(n) for b in range(n)]
    for bits in range(1 << len(pairs)):
        prem = {c: set() for c in range(n)}
        for k, (a, b) in enumerate(pairs):
            if bits >> k & 1:
                prem[a].add(b)
        yield prem


def subsets(s):
    s = sorted(s)
    for r in range(len(s) + 1):
        yield from (set(x) for x in itertools.combinations(s, r))


def run(plant):
    checked, bad, smallest = 0, 0, None
    for n in (1, 2, 3):
        for prem in graphs(n):
            for base in subsets(range(n)):
                for w in subsets(base):
                    checked += 1
                    if violations(n, prem, base, w, plant):
                        bad += 1
                        size = (n, sum(len(v) for v in prem.values()), len(w))
                        if smallest is None or size < smallest[0]:
                            smallest = (size, n, {k: sorted(v) for k, v in prem.items()}, sorted(base), sorted(w))
    rnd = random.Random(0)
    sample = 0
    for _ in range(20000):
        n = 4
        prem = {c: {d for d in range(n) if rnd.random() < 0.35} for c in range(n)}
        base = {c for c in range(n) if rnd.random() < 0.7}
        w = {c for c in base if rnd.random() < 0.4}
        sample += 1
        bad += violations(n, prem, base, w, plant)
    return checked, sample, bad, smallest


def main():
    checked, sample, bad, _ = run(False)
    print("the court's support_sets: %d cases exhaustive (up to 3 claims), %d sampled (4 claims): %d violations" % (
        checked, sample, bad))
    pc, ps, pbad, smallest = run(True)
    if smallest:
        _, n, prem, base, w = smallest
        print("plant (a withheld premise read as none): %d violations; the smallest: %d claim(s), premises %s, held %s, "
              "withheld %s" % (pbad, n, prem, base, w))
    else:
        print("plant: NOT CAUGHT")
    ok = bad == 0 and pbad > 0
    print("T8 MONOTONE %s" % ("HELD" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

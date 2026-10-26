"""The court's R8 (a refused evaluation is not held), measured over COMPAT-0's frozen texts and R8's own fixtures: how
many readings it changes, and that it changes them in one direction only.

  PYTHONHASHSEED=0 python -B tests/court_monotone.py [--jobs N]

For every text, the reference runs it under COMPAT-0's budget, every claim's seal is ratified by a fixture line, and
the court reads the run twice, with R8 off (the court before the repair) and on. The witness is made agreed, so the
comparison isolates the court's rules from the arbiter. The frozen texts give the blast radius on what exists: measured
on 2026-10-26, it was nothing, since no frozen text refuses inside a claim's condition. That is a coverage gap, not a
pass: R8's class is exercised by its four fixtures (tests/fixtures/r8/), and the plant is required to be caught there.

The invariant held (one-sidedness): a rule of the court that changes a verdict may only ever withhold. No claim may
gain WELL-FOUNDED or GROUNDED from R8; it may lose them. Each loss is counted by its reason:
- exact: the claim's own evaluation refused;
- possible: an inline claim whose clause refused;
- through premises: the claim itself is unchanged, and a premise lost its standing.

The plant reads the two courts the other way round, the court after the repair as "before", so that a court granting
what R8 withholds, R8 reverted, shows as gains. It must be caught.
"""
import argparse
import gzip
import base64
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "src")
BUDGET = 10 ** 6
FIXTURE = "FIXTURE written by tests/court_monotone.py; not a person's act"


def readings(raw):
    """[(claim label, before, after)] for one text, each reading (evaluation, support, grounding); None if refused."""
    from orlog import court as C
    from orlog.front import compile_bytes
    from orlog.interp import HostStop, Interp
    from orlog.arbiter import parse_receipt
    comp = compile_bytes(raw)
    if not comp.ok or not comp.an.claims:
        return None
    try:
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=BUDGET).run()
    except HostStop:
        return None
    lines = parse_receipt(it.receipt("reference"))
    seals = C.claim_seals(comp)
    ledger = [{"kind": "claim", "claim_seal": s, "note": FIXTURE, "_line": i + 1} for i, s in enumerate(seals.values())]
    witness = {"dissent_kind": "NONE", "backends": {"reference": {}}}
    out = {}
    for check in (False, True):
        C.REFUSED_EVALUATION_CHECK = check
        try:
            rows = C.panel(comp, witness, lines, ledger)["rows"]
        finally:
            C.REFUSED_EVALUATION_CHECK = True
        out[check] = [(r["clause"], (r["evaluation"], r["support"], r["grounding"])) for r in rows]
    return [(label, before, after) for (label, before), (_, after) in zip(out[False], out[True])]


def _work(item):
    ident, b64 = item
    return ident, readings(base64.b64decode(b64))


def _init():
    sys.path.insert(0, SRC)


def standing(r):
    return r[1] == "WELL-FOUNDED", r[2] == "GROUNDED"


def compare(results, swap=False):
    """Counts of claims, of changed readings, of gains (must be none) and of losses by reason."""
    claims, changed, gained, lost = 0, [], [], {"exact": [], "possible": [], "through premises": []}
    for ident, rows in sorted(results.items()):
        for label, before, after in rows or ():
            if swap:
                before, after = after, before
            claims += 1
            if before == after:
                continue
            changed.append((ident, label, before, after))
            wf0, gr0 = standing(before)
            wf1, gr1 = standing(after)
            if (wf1 and not wf0) or (gr1 and not gr0):
                gained.append((ident, label, before, after))
            elif (wf0 and not wf1) or (gr0 and not gr1):
                why = ("exact" if "REFUSED at evaluation" in after[0] else
                       "possible" if "REFUSED at its clause" in after[0] else "through premises")
                lost[why].append((ident, label, before, after))
    return claims, changed, gained, lost


def report(name, results):
    texts = sum(1 for r in results.values() if r)
    claims, changed, gained, lost = compare(results)
    print("== %s: %d texts, %d ran with claims, %d claims, every seal ratified (fixture), the witness agreed" % (
        name, len(results), texts, claims))
    print("  readings changed: %d; standings gained (WELL-FOUNDED or GROUNDED): %d; lost: %d" % (
        len(changed), len(gained), sum(len(v) for v in lost.values())))
    for why, rows in lost.items():
        print("    lost, %s: %d" % (why, len(rows)))
        for ident, label, before, after in rows[:6]:
            print("      %s %s: was %s, %s, %s; now %s" % (ident, label, before[0], before[1], before[2],
                                                         "; ".join(after)))
    for ident, label, before, after in gained[:6]:
        print("    GAINED %s %s: was %s; now %s" % (ident, label, "; ".join(before), "; ".join(after)))
    return len(changed), len(gained), sum(len(v) for v in lost.values())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args(argv)
    sys.path.insert(0, SRC)
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    items = [(t["id"], t["b64"]) for t in doc["texts"]]
    if a.jobs > 1:
        import multiprocessing
        with multiprocessing.get_context("spawn").Pool(a.jobs, initializer=_init) as pool:
            frozen = dict(pool.map(_work, items, chunksize=16))
    else:
        frozen = dict(_work(i) for i in items)
    fixdir = os.path.join(ROOT, "tests", "fixtures", "r8")
    fixtures = {}
    for fn in sorted(os.listdir(fixdir)):
        with open(os.path.join(fixdir, fn), "rb") as fh:
            fixtures["fixture/r8/" + fn] = readings(fh.read())
    f_changed, f_gained, f_lost = report("COMPAT-0's frozen texts (the blast radius on what exists)", frozen)
    if f_changed == 0:
        print("  R8 changes nothing here: no frozen text refuses inside a claim's condition. A coverage gap, not a "
              "pass: R8's class is exercised by its fixtures below")
    x_changed, x_gained, x_lost = report("R8's fixtures (tests/fixtures/r8/)", fixtures)
    planted = compare(fixtures, swap=True)[2] + compare(frozen, swap=True)[2]
    caught = len(planted) > 0
    print("plant r8-reverted (the courts read the other way round: a court granting what R8 withholds): %s, %d "
          "standing(s) gained" % ("CAUGHT" if caught else "NOT CAUGHT", len(planted)))
    ok = f_gained == 0 and x_gained == 0 and x_lost > 0 and caught
    print("COURT R8 ONE-SIDED: %d gained, %d lost (frozen texts %d, fixtures %d)" % (
        f_gained + x_gained, f_lost + x_lost, f_lost, x_lost) if ok else "COURT R8 NOT ONE-SIDED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

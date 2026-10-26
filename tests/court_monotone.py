"""The court's R8 (a refused evaluation is not held), measured over COMPAT-0's frozen texts and the court's fixtures:
how many readings it changes, and that it changes them in one direction only.

  PYTHONHASHSEED=0 python -B tests/court_monotone.py [--jobs N]

For every text, the reference runs it under COMPAT-0's budget for its kind, every claim's seal is ratified by a fixture
line, and the court reads the run twice: with R8 off (the court before the repair) and as shipped (panel's default, the
value orl.py reads). The witness is made agreed, so the comparison isolates the court's rules from the arbiter. The
frozen texts give the blast radius on what exists: measured on 2026-10-26, it was nothing, since no frozen text refuses
inside a claim's condition. That is a coverage gap, not a pass: R8's class is exercised by its fixtures
(tests/fixtures/r8/), beside the court's others (tests/fixtures/court/).

The invariant held (one-sidedness): a rule of the court that changes a reading may only ever withhold. A reading is
ordered three ways, and no claim may rise in any of them under R8:
- support: UNSUPPORTED and UNREACHED below CIRCULAR below WELL-FOUNDED;
- grounding: UNGROUNDED below GROUNDED;
- held: an evaluation that reads "true in n of n" above every other.
Each loss is counted by its reason:
- exact: the claim's own evaluation refused;
- possible: an inline claim whose clause refused;
- through premises: the claim's own evaluation is unchanged, and a premise lost its standing.
Every changed reading must be counted as a gain or a loss; one counted as neither is a comparator that cannot see it.

Two plants, each of which must be caught (the reporting pass's finding 12 replaced a plant that read this measurement
backwards, and so tested only the comparator):
- standing-without-circular: the comparator before the repair, which read WELL-FOUNDED and GROUNDED only, so that a move
  out of CIRCULAR was counted neither way. cycle_refusal.orl's two moves must then go uncounted.
- a court that grants: the shipped court with a refuted claim counted as held, read as the court after R8. It must
  show gains, on the fixtures.
"""
import argparse
import gzip
import base64
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "src")
FIXTURE_BUDGET = 10 ** 6
FIXTURE = "FIXTURE written by tests/court_monotone.py; not a person's act"
FIXTURE_DIRS = ("r8", "court")
GRANTS = [('        held = hit is None and r["evals"] > 0 and r["trues"] == r["evals"] and agreed\n',
           '        held = hit is None and r["evals"] > 0 and agreed\n')]


def budgets():
    """COMPAT-0's budgets by kind, from its baseline's header (corpus 10^7, the others 10^6)."""
    with open(os.path.join(ROOT, "tests", "compat", "baseline-v0.jsonl"), "rb") as fh:
        return json.loads(fh.read().decode("utf-8").split("\n", 1)[0])["budgets"]


def readings(raw, budget, granting=False):
    """[(claim label, before, after)] for one text, each reading (evaluation, support, grounding); None if refused or
    stopped. before: R8 off; after: the court as shipped, or with granting the planted court that grants."""
    from orlog import court as C
    from orlog.front import compile_bytes
    from orlog.interp import HostStop, Interp
    from orlog.arbiter import parse_receipt
    comp = compile_bytes(raw)
    if not comp.ok or not comp.an.claims:
        return None
    try:
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
    except HostStop:
        return None
    lines = parse_receipt(it.receipt("reference"))
    seals = C.claim_seals(comp)
    ledger = [{"kind": "claim", "claim_seal": s, "note": FIXTURE, "_line": i + 1} for i, s in enumerate(seals.values())]
    witness = {"dissent_kind": "NONE", "backends": {"reference": {}}}
    after_court = C
    if granting:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from plants import planted
        after_court = planted("src/orlog/court.py", GRANTS)
    before = C.panel(comp, witness, lines, ledger, r8=False)["rows"]
    after = after_court.panel(comp, witness, lines, ledger)["rows"]
    reading = lambda r: (r["evaluation"], r["support"], r["grounding"])
    return [(b["clause"], reading(b), reading(a)) for b, a in zip(before, after)]


def _work(item):
    ident, b64, budget = item
    return ident, readings(base64.b64decode(b64), budget)


def _init():
    sys.path.insert(0, SRC)


def standing(r, circular=True):
    """The three orders, as a tuple of ranks; without circular, the comparator before the repair (a plant)."""
    support = 2 if r[1] == "WELL-FOUNDED" else (1 if r[1].startswith("CIRCULAR") and circular else 0)
    return support, r[2] == "GROUNDED", r[0].startswith("true in")


def compare(results, circular=True):
    """Counts of claims, of changed readings, of gains (must be none), of losses by reason, and of changed readings
    counted neither way (must be none)."""
    claims, changed, gained, neither = 0, [], [], []
    lost = {"exact": [], "possible": [], "through premises": []}
    for ident, rows in sorted(results.items()):
        for label, before, after in rows or ():
            claims += 1
            if before == after:
                continue
            changed.append((ident, label, before, after))
            s0, s1 = standing(before, circular), standing(after, circular)
            if any(y > x for x, y in zip(s0, s1)):
                gained.append((ident, label, before, after))
            elif any(y < x for x, y in zip(s0, s1)):
                why = ("exact" if "REFUSED at evaluation" in after[0] else
                       "possible" if "REFUSED at its clause" in after[0] else "through premises")
                lost[why].append((ident, label, before, after))
            else:
                neither.append((ident, label, before, after))
    return claims, changed, gained, lost, neither


def report(name, results):
    texts = sum(1 for r in results.values() if r)
    claims, changed, gained, lost, neither = compare(results)
    print("== %s: %d texts, %d ran with claims, %d claims, every seal ratified (fixture), the witness agreed" % (
        name, len(results), texts, claims))
    print("  readings changed: %d; standings gained: %d; lost: %d; counted neither way: %d" % (
        len(changed), len(gained), sum(len(v) for v in lost.values()), len(neither)))
    for why, rows in lost.items():
        print("    lost, %s: %d" % (why, len(rows)))
        for ident, label, before, after in rows[:8]:
            print("      %s %s: was %s, %s, %s; now %s" % (ident, label, before[0], before[1], before[2],
                                                         "; ".join(after)))
    for ident, label, before, after in gained[:6]:
        print("    GAINED %s %s: was %s; now %s" % (ident, label, "; ".join(before), "; ".join(after)))
    for ident, label, before, after in neither[:6]:
        print("    COUNTED NEITHER WAY %s %s: was %s; now %s" % (ident, label, "; ".join(before), "; ".join(after)))
    return len(changed), len(gained), sum(len(v) for v in lost.values()), len(neither)


def fixture_texts():
    out = {}
    for d in FIXTURE_DIRS:
        folder = os.path.join(ROOT, "tests", "fixtures", d)
        for fn in sorted(os.listdir(folder)):
            with open(os.path.join(folder, fn), "rb") as fh:
                out["fixture/%s/%s" % (d, fn)] = fh.read()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args(argv)
    sys.path.insert(0, SRC)
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    by_kind = budgets()
    items = [(t["id"], t["b64"], by_kind[t["kind"]]) for t in doc["texts"]]
    if a.jobs > 1:
        import multiprocessing
        with multiprocessing.get_context("spawn").Pool(a.jobs, initializer=_init) as pool:
            frozen = dict(pool.map(_work, items, chunksize=16))
    else:
        frozen = dict(_work(i) for i in items)
    raws = fixture_texts()
    fixtures = {k: readings(v, FIXTURE_BUDGET) for k, v in raws.items()}
    f_changed, f_gained, f_lost, f_neither = report("COMPAT-0's frozen texts (the blast radius on what exists)", frozen)
    if f_changed == 0:
        print("  R8 changes nothing here: no frozen text refuses inside a claim's condition. A coverage gap, not a "
              "pass: R8's class is exercised by its fixtures below")
    x_changed, x_gained, x_lost, x_neither = report("the court's fixtures (tests/fixtures/r8/, tests/fixtures/court/)",
                                                    fixtures)
    cycle = [r for r in compare({k: v for k, v in fixtures.items() if k.endswith("/cycle_refusal.orl")})[3].values()]
    cycle_lost = sum(len(r) for r in cycle)
    blind = compare(fixtures, circular=False)[4]
    plant_blind = len(blind) > 0
    print("plant standing-without-circular (the comparator read WELL-FOUNDED and GROUNDED only): %s, %d changed "
          "reading(s) counted neither way" % ("CAUGHT" if plant_blind else "NOT CAUGHT", len(blind)))
    granting = {k: readings(v, FIXTURE_BUDGET, granting=True) for k, v in raws.items()}
    gains = compare(granting)[2]
    plant_grants = len(gains) > 0
    print("plant court-grants-a-refuted-claim (a court that grants, read as the court after R8): %s, %d standing(s) "
          "gained" % ("CAUGHT" if plant_grants else "NOT CAUGHT", len(gains)))
    ok = (f_gained == 0 and x_gained == 0 and f_neither == 0 and x_neither == 0 and x_lost > 0 and cycle_lost == 2
          and plant_blind and plant_grants)
    print("COURT R8 ONE-SIDED: %d gained, %d lost (frozen texts %d, fixtures %d; cycle_refusal.orl %d)" % (
        f_gained + x_gained, f_lost + x_lost, f_lost, x_lost, cycle_lost) if ok else "COURT R8 NOT ONE-SIDED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

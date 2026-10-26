"""Three ways tests/court_monotone.py can read ONE-SIDED, or CAUGHT, without having looked.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/monotone_blind.py

(a) CIRCULAR is not a standing to it. `standing()` reads only WELL-FOUNDED and GROUNDED, so a claim that moves between
    CIRCULAR and UNSUPPORTED (held, or not) is counted neither gained nor lost. On fixtures/cycle_refusal.orl R8 moves
    two claims from CIRCULAR to UNSUPPORTED; read the other way round (the plant's direction: a court granting what R8
    withholds) the same two claims gain "held", and the comparison counts 0 gained.
(b) Its budget is not COMPAT-0's. The docstring says "the reference runs it under COMPAT-0's budget"; the code gives
    every text 10^6 counted operations, and COMPAT-0 gives the corpus 10^7. A text stopped by the host returns None and
    is counted with the texts that have no claims, without a word.
(c) Its plant is the measurement read backwards. `compare(results, swap=True)` gains are exactly `compare(results)`'s
    losses, claim for claim, so "plant r8-reverted: CAUGHT" holds whenever anything was lost, which `ok` already
    requires: the plant cannot fail on its own.
"""
import base64
import gzip
import json
import os
import sys

import _common as C

C.require_env()
sys.path.insert(0, os.path.join(C.ROOT, "tests"))
import court_monotone as M  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import HostStop, Interp  # noqa: E402


def part_a():
    res = {"fixtures/cycle_refusal.orl": M.readings(C.fixture("cycle_refusal.orl"))}
    print("== (a) fixtures/cycle_refusal.orl, read with R8 off and on (court_monotone.readings):")
    for label, before, after in res["fixtures/cycle_refusal.orl"]:
        print("   %s: R8 off %s | R8 on %s" % (label, "; ".join(before), "; ".join(after)))
    claims, changed, gained, lost = M.compare(res)
    print("   compare: %d claims, %d readings changed, %d gained, %d lost" % (
        claims, len(changed), len(gained), sum(len(v) for v in lost.values())))
    s_claims, s_changed, s_gained, s_lost = M.compare(res, swap=True)
    print("   the plant's direction (swap): %d readings changed, %d gained -> the plant would read %s on this text" % (
        len(s_changed), len(s_gained), "CAUGHT" if s_gained else "NOT CAUGHT"))
    held_moved = sum(1 for _, _, b, a in changed if b[1].startswith("CIRCULAR") != a[1].startswith("CIRCULAR"))
    return len(changed) > 0 and not gained and not s_gained and held_moved > 0


def part_b():
    with open(os.path.join(C.ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    with open(os.path.join(C.ROOT, "tests", "compat", "baseline-v0.jsonl"), "rb") as fh:
        head = json.loads(fh.read().decode("utf-8").split("\n")[0])
    print("== (b) court_monotone.BUDGET = %d for every text; COMPAT-0's budgets: %s" % (M.BUDGET, head["budgets"]))
    dropped = []
    for t in doc["texts"]:
        if head["budgets"][t["kind"]] == M.BUDGET:
            continue
        comp = compile_bytes(base64.b64decode(t["b64"]))
        if not comp.ok or not comp.an.claims:
            continue
        try:
            Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=M.BUDGET).run()
        except HostStop as e:
            it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=head["budgets"][t["kind"]]).run()
            dropped.append((t["id"], len(comp.an.claims), e.ops, it.ops, it.status))
    for ident, n, at, ops, st in dropped:
        print("   %s: %d claim(s); stopped by court_monotone's budget at %d ops; under COMPAT-0's it runs %d ops, %s"
              % (ident, n, at, ops, st))
    print("   texts with claims that court_monotone drops without a word: %d (%d claims)" % (
        len(dropped), sum(d[1] for d in dropped)))
    return dropped


def part_c():
    fixdir = os.path.join(C.ROOT, "tests", "fixtures", "r8")
    res = {fn: M.readings(open(os.path.join(fixdir, fn), "rb").read()) for fn in sorted(os.listdir(fixdir))}
    res["fixtures/cycle_refusal.orl"] = M.readings(C.fixture("cycle_refusal.orl"))
    lost = {(i, l) for rows in M.compare(res)[3].values() for i, l, _, _ in rows}
    gained_swapped = {(i, l) for i, l, _, _ in M.compare(res, swap=True)[2]}
    print("== (c) over R8's four fixtures and cycle_refusal.orl: lost %d, the plant's gains %d, the same claims: %s" % (
        len(lost), len(gained_swapped), lost == gained_swapped))
    return lost == gained_swapped


def main():
    a = part_a()
    b = part_b()
    c = part_c()
    print("BLIND: (a) %s; (b) %d text(s) dropped; (c) plant = mirror of the losses: %s" % (
        "a CIRCULAR change counted neither way" if a else "not shown", len(b), c))
    return 0


if __name__ == "__main__":
    sys.exit(main())

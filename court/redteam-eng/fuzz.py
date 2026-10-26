"""Differential fuzzing: random valid programs, the reference against the backends, every disagreement kept.

  python -B fuzz.py START COUNT [--backends python,c99] [--jobs 12] [--gen fuzzgen]
Writes programs that disagree (or that crash the front end or the arbiter) to work/fuzz/hits/, and one JSON line
per program to work/fuzz/log-START-COUNT.jsonl.
"""
import argparse
import concurrent.futures as cf
import importlib
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)

FZ = os.path.join(HERE, "work", "fuzz")


def one(args):
    seed, backends, genname = args
    from orlog.arbiter import Arbiter
    from orlog.front import compile_bytes
    gen = importlib.import_module(genname)
    raw = gen.generate(seed)
    rec = {"seed": seed, "gen": genname}
    try:
        comp = compile_bytes(raw)
    except Exception as e:
        rec.update(kind="FRONT-CRASH", err="%s: %s" % (type(e).__name__, e))
        return rec, raw
    if not comp.ok:
        rec.update(kind="FRONT-REFUSED", code=comp.error.code, line=comp.error.line, msg=comp.error.msg[:200])
        return rec, raw
    arb = Arbiter(os.path.join(FZ, "w"), backends=backends)
    try:
        comp, w, ref = arb.arbitrate(raw, "%s-%d" % (genname, seed))
    except Exception:
        rec.update(kind="ARBITER-CRASH", err=traceback.format_exc()[-800:])
        return rec, raw
    rec.update(kind="DISSENT" if w["dissenting"] else "AGREE", status=ref.status, ops=ref.ops, events=ref.events,
               dissent=w["dissenting"], dkind=w["dissent_kind"], notes=w["mismatch_notes"])
    return rec, raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start", type=int)
    ap.add_argument("count", type=int)
    ap.add_argument("--backends", default="python,c99")
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--gen", default="fuzzgen")
    a = ap.parse_args()
    os.makedirs(os.path.join(FZ, "hits"), exist_ok=True)
    backends = tuple(a.backends.split(","))
    log = os.path.join(FZ, "log-%s-%d-%d.jsonl" % (a.gen, a.start, a.count))
    counts = {}
    statuses = {}
    t0 = time.time()
    with open(log, "w", encoding="utf-8") as lf, cf.ProcessPoolExecutor(a.jobs) as ex:
        for rec, raw in ex.map(one, [(s, backends, a.gen) for s in range(a.start, a.start + a.count)]):
            counts[rec["kind"]] = counts.get(rec["kind"], 0) + 1
            if rec["kind"] in ("AGREE", "DISSENT"):
                st = rec["status"].split(" ")[0] + (" " + rec["status"].split(" ")[1] if " " in rec["status"] else "")
                statuses[st] = statuses.get(st, 0) + 1
            lf.write(json.dumps(rec, sort_keys=True) + "\n")
            if rec["kind"] != "AGREE" and rec["kind"] != "FRONT-REFUSED":
                with open(os.path.join(FZ, "hits", "%s-%s-%d.orl" % (rec["kind"], a.gen, rec["seed"])), "wb") as fh:
                    fh.write(raw)
                print(rec["kind"], rec["seed"], json.dumps(rec)[:400])
    print("ran %d programs in %.0f s: %s" % (a.count, time.time() - t0, json.dumps(counts, sort_keys=True)))
    print("reference status: %s" % json.dumps(statuses, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""R8's coverage over COMPAT-0's frozen texts: for every claim of every text, where its run ended and what the court
before R8 read, so that "R8 changes nothing on the frozen texts" can be told apart: no claim's evaluation ever refused,
or some did and none read held anyway.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/r8_coverage.py

Each text is run by the reference under COMPAT-0's budget for its kind; every claim's seal is ratified by a fixture
line and the witness made agreed, as tests/court_monotone.py does, so that the count isolates the court's rules. "The
court before R8" is panel(..., r8=False). A claim is put in exactly one class:
- dp5: the run refused at the claim's own clause with a code other than CLAIM-REFUTED (R8's class), and its finished
  evaluations were all true;
- dp5-not-held: the same refusal, with an earlier evaluation false (cannot occur: a false evaluation refuses first);
- refuted: the run refused CLAIM-REFUTED at the claim;
- held-refused-elsewhere: every finished evaluation true, and the run refused at another clause (the reporting
  pass's open question: whether such a claim stays held is the owner's to rule);
- held-completed: every evaluation true, the run completed;
- unreached: never evaluated.
"""
import base64
import gzip
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
FIXTURE = "FIXTURE written by research/r8_coverage.py; not a person's act"


def main():
    from orlog import court as C
    from orlog.arbiter import parse_receipt
    from orlog.front import compile_bytes
    from orlog.interp import HostStop, Interp
    with open(os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz"), "rb") as fh:
        doc = json.loads(gzip.decompress(fh.read()).decode("utf-8"))
    with open(os.path.join(ROOT, "tests", "compat", "baseline-v0.jsonl"), "rb") as fh:
        budgets = json.loads(fh.read().decode("utf-8").split("\n", 1)[0])["budgets"]
    texts = {"all": 0, "compile refused": 0, "no claim": 0, "stopped by the host": 0, "ran with claims": 0}
    runs = {}
    classes = {k: [] for k in ("dp5", "dp5-not-held", "refuted", "held-refused-elsewhere", "held-completed",
                               "unreached", "other")}
    witness = {"dissent_kind": "NONE", "backends": {"reference": {}}}
    for t in doc["texts"]:
        texts["all"] += 1
        comp = compile_bytes(base64.b64decode(t["b64"]))
        if not comp.ok:
            texts["compile refused"] += 1
            continue
        if not comp.an.claims:
            texts["no claim"] += 1
            continue
        try:
            it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budgets[t["kind"]]).run()
        except HostStop:
            texts["stopped by the host"] += 1
            continue
        texts["ran with claims"] += 1
        lines = parse_receipt(it.receipt("reference"))
        status = next((l[7:] for l in lines if l.startswith("status ")), "")
        parts = status.split(" ")
        refusal = (parts[1], int(parts[2])) if parts[0] == "REFUSED" else None
        runs[status.split(" ")[0] if not refusal else "REFUSED " + refusal[0]] = runs.get(
            status.split(" ")[0] if not refusal else "REFUSED " + refusal[0], 0) + 1
        ledger = [{"kind": "claim", "claim_seal": s, "note": FIXTURE, "_line": i + 1}
                  for i, s in enumerate(C.claim_seals(comp).values())]
        old = {r["claim"]: r for r in C.panel(comp, witness, lines, ledger, r8=False)["rows"]}
        new = {r["claim"]: r for r in C.panel(comp, witness, lines, ledger)["rows"]}
        recs = {}
        for l in lines:
            if l.startswith("claim "):
                p = l.split(" ")
                recs[int(p[1])] = (int(p[3]), int(p[4]))
        for site in comp.an.claims:
            k = site.stmt.id
            evals, trues = recs.get(k, (0, 0))
            at_claim = refusal is not None and refusal[1] == site.id
            item = (t["id"], old[k]["clause"], status, old[k]["evaluation"], old[k]["support"], old[k]["grounding"],
                    new[k]["evaluation"], new[k]["support"], new[k]["grounding"])
            if evals == 0:
                classes["unreached"].append(item)
            elif at_claim and refusal[0] == "CLAIM-REFUTED":
                classes["refuted"].append(item)
            elif at_claim:
                classes["dp5" if trues == evals else "dp5-not-held"].append(item)
            elif trues == evals and refusal is not None:
                classes["held-refused-elsewhere"].append(item)
            elif trues == evals:
                classes["held-completed"].append(item)
            else:
                classes["other"].append(item)
    print("== COMPAT-0's frozen texts")
    for k, v in texts.items():
        print("  %-22s %d" % (k, v))
    print("  runs of the texts with claims, by how they ended: %s" % ", ".join(
        "%s %d" % (k, v) for k, v in sorted(runs.items())))
    print("== every claim, by class (seals ratified, the witness agreed)")
    for k, v in classes.items():
        print("  %-24s %d" % (k, len(v)))
    for k in ("dp5", "dp5-not-held", "held-refused-elsewhere", "other"):
        for ident, clause, status, oe, os_, og, ne, ns, ng in classes[k]:
            print("    %s %s %s: run %s; before R8: %s, %s, %s; with R8: %s, %s, %s" % (
                k, ident, clause, status, oe, os_, og, ne, ns, ng))
    dp5 = classes["dp5"]
    print("R8 COVERAGE: %d claim(s) in R8's class (%d read held and %d GROUNDED before R8); %d held in a run refused "
          "elsewhere; %d refuted; %d held in a completed run; %d unreached" % (
              len(dp5), len(dp5), sum(1 for x in dp5 if x[5] == "GROUNDED"), len(classes["held-refused-elsewhere"]),
              len(classes["refuted"]), len(classes["held-completed"]), len(classes["unreached"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())

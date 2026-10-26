"""Orlog OL-0 command line.

  python orl.py run FILE... [--backends python,c99,rust] [--witness DIR]
  python orl.py check FILE            the door, the law, the seals, the literal notes
  python orl.py court FILE [--ledger PATH]
  python orl.py stamp FILE            writes FILE.stamped: check syllables and the seal line
  python orl.py ratify FILE --claim LABEL --note TEXT [--ledger PATH]      a person's act
  python orl.py ratify-theorem NAME --note TEXT [--ledger PATH]            a person's act
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.arbiter import Arbiter, BACKENDS, witness_artifact, parse_receipt  # noqa: E402
from orlog.court import panel, court_artifact, read_ledger, claim_seals, LedgerBroken  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.seal import stamp  # noqa: E402

DEFAULT_LEDGER = os.path.join(ROOT, "ratified.jsonl")


def read(path):
    with open(path, "rb") as fh:
        return fh.read()


def cmd_check(a):
    comp = compile_bytes(read(a.file))
    for e in comp.canon.events:
        print("door %-6s %-22s L%s C%s %s -> %s  (%s)" % (e["cls"], e["rule"], e["line"], e["col"], e["raw"] or "-",
                                                          e["canon"] or "-", e["reason"]))
    if not comp.ok:
        print("REFUSED %s at line %s: %s" % (comp.error.code, comp.error.line, comp.error.msg))
        return 1
    print("raw-seal  %s" % comp.raw_seal)
    print("text-seal %s" % comp.text_seal)
    print("law-seal  %s (%s)" % (comp.law_seal, comp.seal_words))
    for n in comp.an.notes:
        print("note %s §%s: %s stored as %s (%s)" % (n["note"], n["clause"], n["literal"], n["stored"], n["rule"]))
    print("clauses %d, claims %d, line checks verified %d" % (len(comp.prog.clauses), len(comp.an.claims),
                                                               comp.prog.line_checks))
    return 0


def cmd_run(a):
    backends = tuple(a.backends.split(",")) if a.backends else BACKENDS
    wd = a.workdir or os.path.join(ROOT, "build", "runs")
    os.makedirs(wd, exist_ok=True)
    arb = Arbiter(wd, backends=backends)
    worst = 0
    for f in a.files:
        name = os.path.splitext(os.path.basename(f))[0]
        comp, w, ref = arb.arbitrate(read(f), name)
        if not comp.ok:
            print("%-18s REFUSED %s at line %s" % (name, w["refusal"]["code"], w["refusal"]["line"]))
            worst = max(worst, 1)
            continue
        if ref is None:                     # the host's budget stopped the reference: no verdict, no receipt
            print("%-18s law %s  %s" % (name, comp.seal_words, w["mismatch_notes"][0]["detail"]))
            worst = max(worst, 3)
            continue
        line = "%-18s law %s  ref %s  agree [%s]  dissent [%s] %s" % (
            name, comp.seal_words, w["reference"]["status"], ",".join(w["agreeing"]), ",".join(w["dissenting"]),
            w["dissent_kind"]) + ("  did not build [%s]" % ",".join(w["build_failed"]) if w["build_failed"] else "")
        line += "  stopped by the host [%s]" % ",".join(w["stopped"]) if w.get("stopped") else ""
        print(line)
        for n in w["mismatch_notes"]:
            print("    NOTE %s" % json.dumps(n, sort_keys=True))
        if a.show:
            sys.stdout.write(bytes(ref.out).decode("utf-8"))
        if a.witness:
            os.makedirs(a.witness, exist_ok=True)
            art = witness_artifact(w)
            with open(os.path.join(a.witness, name + ".witness.json"), "wb") as fh:
                fh.write(json.dumps(art, indent=1, sort_keys=True, ensure_ascii=True).encode("ascii"))
        if w["dissenting"] or w.get("build_failed") or w.get("stopped"):
            worst = max(worst, 2)
    return worst


def cmd_court(a):
    wd = a.workdir or os.path.join(ROOT, "build", "runs")
    arb = Arbiter(wd, backends=tuple(a.backends.split(",")) if a.backends else BACKENDS)
    comp, w, ref = arb.arbitrate(read(a.file), os.path.splitext(os.path.basename(a.file))[0])
    if not comp.ok:
        print("REFUSED", w["refusal"])
        return 1
    if ref is None:
        print(w["mismatch_notes"][0]["detail"])
        return 3
    try:
        ledger = read_ledger(a.ledger or DEFAULT_LEDGER)
    except LedgerBroken as e:               # fail closed: no reading of a broken ledger, never a traceback
        print(str(e))
        return 1
    p = panel(comp, w, parse_receipt(ref.receipt()), ledger)
    for r in p["rows"]:
        print("%s  %s" % (r["clause"], r["text"][:110]))
        for k in ("channel", "integrity", "evaluation", "theorem", "ratification", "cost", "cost_reading",
                  "external_bits", "support", "cycle", "grounding"):
            if k in r:
                print("    %-13s %s" % (k, r[k]))
    print("summary", json.dumps(p["summary"], sort_keys=True))
    if a.json:
        with open(a.json, "wb") as fh:
            fh.write(json.dumps(court_artifact(comp, p), indent=1, sort_keys=True).encode("ascii"))
    return 0


def cmd_stamp(a):
    comp = compile_bytes(read(a.file))
    if not comp.ok:
        print("REFUSED", comp.error)
        return 1
    text = stamp(comp.text)
    lines = [l for l in text.split("\n") if not l.startswith("Sealed:")]
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("Sealed: %s." % comp.seal_words)
    out = a.file + ".stamped"
    with open(out, "wb") as fh:
        fh.write(("\n".join(lines) + "\n").encode("utf-8"))
    print("wrote", out)
    return 0


def append_ledger(path, entry):
    with open(path, "ab") as fh:
        fh.write((json.dumps(entry, sort_keys=True, ensure_ascii=True) + "\n").encode("ascii"))
        fh.flush()
        os.fsync(fh.fileno())


def cmd_ratify(a):
    if not a.note:
        print("a ratification needs --note: say what you checked")
        return 1
    comp = compile_bytes(read(a.file))
    if not comp.ok:
        print("REFUSED", comp.error)
        return 1
    seals = claim_seals(comp)
    if a.claim_id is not None:
        cid = a.claim_id
    else:
        c = comp.prog.by_label.get((a.claim or "").lstrip("§"))
        cid = getattr(getattr(c, "stmt", None), "id", None) if c is not None and type(c.stmt).__name__ == "Claim" \
            else None
    if cid not in seals:
        print("no claim there (give --claim LABEL for a clause whose own statement is a claim, or --claim-id N)")
        return 1
    append_ledger(a.ledger or DEFAULT_LEDGER, {"kind": "claim", "claim_seal": seals[cid], "law_seal": comp.law_seal,
                                               "claim_id": cid, "note": a.note, "by": "a person at this console"})
    print("ratified claim %d (%s)" % (cid, seals[cid][:16]))
    return 0


def cmd_ratify_theorem(a):
    if not a.note:
        print("a ratification needs --note: say what you checked")
        return 1
    append_ledger(a.ledger or DEFAULT_LEDGER, {"kind": "theorem", "name": a.name, "note": a.note,
                                               "by": "a person at this console"})
    print("ratified theorem:", a.name)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="orl")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check")
    p.add_argument("file")
    p = sub.add_parser("run")
    p.add_argument("files", nargs="+")
    p.add_argument("--backends")
    p.add_argument("--workdir")
    p.add_argument("--witness")
    p.add_argument("--show", action="store_true")
    p = sub.add_parser("court")
    p.add_argument("file")
    p.add_argument("--backends")
    p.add_argument("--ledger")
    p.add_argument("--workdir")
    p.add_argument("--json")
    p = sub.add_parser("stamp")
    p.add_argument("file")
    p = sub.add_parser("ratify")
    p.add_argument("file")
    p.add_argument("--claim")
    p.add_argument("--claim-id", type=int, dest="claim_id")
    p.add_argument("--note")
    p.add_argument("--ledger")
    p = sub.add_parser("ratify-theorem")
    p.add_argument("name")
    p.add_argument("--note")
    p.add_argument("--ledger")
    a = ap.parse_args(argv)
    return {"check": cmd_check, "run": cmd_run, "court": cmd_court, "stamp": cmd_stamp, "ratify": cmd_ratify,
            "ratify-theorem": cmd_ratify_theorem}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

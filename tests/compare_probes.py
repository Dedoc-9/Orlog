"""Run the clean-room twin's 163 probes (twin/probes/, expectations worked by hand from SPEC v0.1 §11) through the
reference implementation, and print every difference. The probes and their expectations were written by the twin's
author, who never read this implementation.

Where SPEC §13 settled a reading against the twin's, twin/probes/settled.json says so, probe by probe, with the
settled code and the reason; the twin's expected.json is left as its author wrote it. A settled probe is reported by
name and counted apart; it passes only if the reference gives the settled code.

  python tests/compare_probes.py
"""
import hashlib
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402

PROBES = os.path.join(ROOT, "twin", "probes")


def compare(expected=None, settled=None):
    """(same, kept, diffs, total, error): probes identical, settled probes the reference meets, the differences, and
    a message when settled.json does not match the twin's own expectations (or None)."""
    if expected is None:
        with open(os.path.join(PROBES, "expected.json"), "rb") as fh:
            expected = json.loads(fh.read().decode("utf-8"))
    if settled is None:
        with open(os.path.join(PROBES, "settled.json"), "rb") as fh:
            settled = json.loads(fh.read().decode("utf-8"))
    for name, s in settled.items():
        if expected[name].get("refused") != s["twin"]:
            return 0, [], [], len(expected), ("SETTLED %s: the twin's expectation is %r, not the %r settled.json says "
                                              "it is" % (name, expected[name].get("refused"), s["twin"]))
    diffs, same, kept = [], 0, []
    for name, exp in sorted(expected.items()):
        if name in settled:
            exp = dict(exp, refused=settled[name]["settled"])
        with open(os.path.join(PROBES, name + ".orl"), "rb") as fh:
            raw = fh.read()
        comp = compile_bytes(raw)
        got = {}
        if not comp.ok:
            got["refused"] = comp.error.code
        else:
            it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
            rec = it.receipt().decode("ascii").splitlines()
            out = bytes(it.out)
            got = {"status": it.status, "ops": it.ops, "events": it.events, "output": out.decode("utf-8"),
                   "output_bytes": len(out), "output_sha256": hashlib.sha256(out).hexdigest(),
                   "claims": [l for l in rec if l.startswith("claim ")]}
        keys = ["refused"] if "refused" in exp else ["status", "ops", "events", "output", "output_bytes",
                                                     "output_sha256", "claims"]
        bad = [(k, exp.get(k), got.get(k)) for k in keys if exp.get(k) != got.get(k)]
        if bad:
            diffs.append((name, exp.get("items"), exp.get("what"), bad))
        elif name in settled:
            kept.append(name)
        else:
            same += 1
    return same, kept, diffs, len(expected), None


def main():
    with open(os.path.join(PROBES, "settled.json"), "rb") as fh:
        settled = json.loads(fh.read().decode("utf-8"))
    same, kept, diffs, total, error = compare(settled=settled)
    if error:
        print(error)
        return 1
    for name in kept:
        s = settled[name]
        print("SETTLED %s: the twin read %s; %s settles %s, which the reference gives" %
              (name, s["twin"], s["amendment"], s["settled"]))
    for name, items, what, bad in diffs:
        print("DIFF %s (items %s): %s" % (name, items, what))
        for k, e, g in bad:
            print("     %s: %s %r, reference gives %r" % (k, "settled" if name in settled else "twin expects", e, g))
    print("PROBES %d/%d identical between the twin's hand-worked expectations and the reference; %d settled against "
          "the twin's reading by SPEC §13; %d different" % (same, total, len(kept), len(diffs)))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())

"""The witness's receipt hashes: what a person comparing them would conclude.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/witness_receipt_sha.py

The verdict is decided by receipt_core (exact bytes). The witness's per-backend summary is made by `_summary`, which
hashes parse_receipt's lines: split on any line break, every 'backend ' line dropped, joined by LF with no final LF.
The reference's `receipt_sha256` is the sha256 of its whole receipt.
  1. An agreeing run: the reference's receipt_sha256 against the python backend's.
  2. A python backend whose runtime writes its receipt with CR LF line ends (the arbiter's mutate hook): the arbiter
     calls it dissenting (red team E7's repair), and the witness's fields for it are set beside an agreeing run's.
"""
import json
import sys

import _common as C

C.require_env()
from orlog.arbiter import Arbiter  # noqa: E402

LF = 'fh.write(("\\n".join(lines) + "\\n").encode("ascii"))'
CRLF = 'fh.write(("\\r\\n".join(lines) + "\\r\\n").encode("ascii"))'


def crlf(backend, src):
    if backend != "python":
        return src
    if src.count(LF) != 1:
        raise SystemExit("anchor found %d times" % src.count(LF))
    return src.replace(LF, CRLF)


def main():
    raw = C.read("examples/collatz.orl")
    _, good, _ = Arbiter(C.workdir("wsha"), backends=("python",)).arbitrate(raw, "ws-good")
    _, bad, _ = Arbiter(C.workdir("wsha"), backends=("python",), mutate=crlf).arbitrate(raw, "ws-crlf")
    g, b = good["backends"]["python"], bad["backends"]["python"]
    print("1. agreeing run (%s): reference receipt_sha256 %s, python's %s: %s" % (
        good["dissent_kind"], good["reference"]["receipt_sha256"][:16], g["receipt_sha256"][:16],
        "equal" if good["reference"]["receipt_sha256"] == g["receipt_sha256"] else "DIFFERENT, though they agree"))
    print("2. CR LF receipt: %s, dissenting [%s]" % (bad["dissent_kind"], ",".join(bad["dissenting"])))
    same = []
    for k in ("status", "output_sha256", "events", "trace_head", "ops", "exit", "receipt_sha256"):
        eq = g.get(k) == b.get(k)
        same.append(eq)
        print("   %-15s agreeing run %-18s CR LF run %-18s %s" % (k, str(g.get(k))[:16], str(b.get(k))[:16],
                                                               "same" if eq else "differs"))
    note = [n for n in bad["mismatch_notes"] if n.get("backend") == "python"]
    print("   mismatch note: %s" % json.dumps(note[0].get("detail") if note else None))
    print("WITNESS: every summary field of the dissenting backend equals the agreeing run's: %s" % all(same))
    return 0


if __name__ == "__main__":
    sys.exit(main())

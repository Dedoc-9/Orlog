"""LEDGER-BROKEN covers a line that is not JSON or not an object. A line that is a JSON object of the wrong shape is
read, and the court then raises.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/ledger_malformed.py

Each ledger below is one line, written under work/reporting-pass/ledgers/ (a fixture file, not a person's act, and not
the default ledger). For each: court.read_ledger's answer, then `orl.py court examples/collatz.orl --backends python
--ledger FILE`: its exit status, whether it refused LEDGER-BROKEN, and whether it ended in a traceback.
"""
import json
import os
import subprocess
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402

LINES = {
    "claim-without-seal": {"kind": "claim", "note": "FIXTURE"},
    "theorem-without-name": {"kind": "theorem", "note": "FIXTURE"},
    "seal-not-a-string": {"kind": "claim", "claim_seal": ["ab"], "note": "FIXTURE"},
    "control-torn": None,       # the case LEDGER-BROKEN was built for
}


def main():
    d = os.path.join(C.WORK, "ledgers")
    os.makedirs(d, exist_ok=True)
    wd = C.workdir("ledger")
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    tracebacks = 0
    for name, entry in LINES.items():
        path = os.path.join(d, name + ".jsonl")
        with open(path, "wb") as fh:
            fh.write(b'{"kind": "claim", "claim_se' if entry is None else
                     (json.dumps(entry, sort_keys=True) + "\n").encode("ascii"))
        try:
            got = "read %d entr%s" % (len(COURT.read_ledger(path)), "y" if len(COURT.read_ledger(path)) == 1 else "ies")
        except COURT.LedgerBroken as e:
            got = str(e)
        r = subprocess.run([sys.executable, "-B", os.path.join(C.ROOT, "orl.py"), "court",
                            os.path.join(C.ROOT, "examples", "collatz.orl"), "--backends", "python", "--workdir", wd,
                            "--ledger", path], capture_output=True, text=True, encoding="utf-8", env=env)
        tb = "Traceback" in r.stderr
        last = (r.stderr.strip().splitlines() or [""])[-1]
        print("== %-22s read_ledger: %s" % (name, got))
        print("   orl.py court: exit %d; LEDGER-BROKEN: %s; traceback: %s%s" % (
            r.returncode, r.stdout.startswith("LEDGER-BROKEN"), tb, (" (" + last + ")") if tb else ""))
        tracebacks += tb and entry is not None
    print("LEDGER LINES READ AND THEN RAISED: %d of %d malformed objects (the torn control refuses LEDGER-BROKEN)" % (
        tracebacks, len(LINES) - 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

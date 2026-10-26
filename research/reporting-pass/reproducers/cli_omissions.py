"""What `orl.py court` computes and does not print.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/cli_omissions.py

(a) The CONSTANT note (red team E5, TRIAGE's tautology airlock) is in the panel's row as `condition`; cmd_court prints a
    fixed list of keys that does not hold `condition`. The text: fixtures/constant_claim.orl, one claim that reads no
    variable and one that does. The self-test's CONSTANT row reads the panel in process, never the command's output.
(b) AGREED among whom: `orl.py court examples/collatz.orl` with --backends python and with python,c99,rust; the two
    printed readings compared byte for byte, and the two --json artifacts with their chain hash set aside.
"""
import json
import os
import subprocess
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402


def court(args):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-B", os.path.join(C.ROOT, "orl.py"), "court"] + args, capture_output=True,
                       text=True, encoding="utf-8", env=env)
    return r.returncode, r.stdout


def main():
    wd = C.workdir("cli-omit")
    nothing = os.path.join(C.WORK, "no-such-ledger.jsonl")
    path = os.path.join(C.FIXTURES, "constant_claim.orl")
    comp, w, ref = Arbiter(wd, backends=("python",)).arbitrate(C.fixture("constant_claim.orl"), "co-const")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    print("(a) the panel's rows, in process:")
    for r in p["rows"]:
        print("    %s condition: %s" % (r["clause"], r.get("condition", "(none)")[:70]))
    code, out = court([path, "--backends", "python", "--workdir", wd, "--ledger", nothing])
    print("    orl.py court prints CONSTANT: %s (exit %d); its printed lines for the constant claim:" % (
        "CONSTANT" in out, code))
    for l in out.splitlines()[:9]:
        print("    | " + l)
    collatz = os.path.join(C.ROOT, "examples", "collatz.orl")
    outs, arts = {}, {}
    for b in ("python", "python,c99,rust"):
        j = os.path.join(C.WORK, "court-%s.json" % b.replace(",", "-"))
        code, outs[b] = court([collatz, "--backends", b, "--workdir", wd, "--ledger", nothing, "--json", j])
        with open(j, "rb") as fh:
            art = json.loads(fh.read().decode("ascii"))
        art.pop("chain_hash", None)
        arts[b] = json.dumps(art, sort_keys=True)
    print("(b) orl.py court examples/collatz.orl, --backends python against python,c99,rust:")
    print("    printed readings byte-identical: %s; --json artifacts identical but for the chain hash: %s" % (
        outs["python"] == outs["python,c99,rust"], arts["python"] == arts["python,c99,rust"]))
    print("    integrity lines: %s" % sorted({l.strip() for l in outs["python"].splitlines()
                                              if l.strip().startswith("integrity")}))
    print("    a backend's name anywhere in the printed reading: %s" % any(
        n in outs["python,c99,rust"] for n in ("python", "c99", "rust")))
    return 0


if __name__ == "__main__":
    sys.exit(main())

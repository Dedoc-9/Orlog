"""What the court's reading and orl.py's exit statuses say about a run that did not complete.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/refusal_hidden.py

Part 1, in process (the python backend; every claim's seal ratified by an in-memory fixture line, as the self-test's R8
rows do). For each text: the reference's status, then each claim's reading, the summary, and whether the word REFUSED
or the refusal's code appears anywhere in what `orl.py court` prints for it (the same keys, printed the same way).
  tests/fixtures/r8/omit.orl     DP-5's fixture: R8 withholds the claim (the control)
  fixtures/hoisted_omit.orl      the same loop with the item read hoisted into a Let: the same refusal, one clause
                                 earlier, so no evaluation of the claim began at the 17th iteration
  fixtures/must_after_claim.orl  a claim that held, then a run-time assertion that failed

Part 2, the command line, as a person runs it (a ledger path that does not exist, so nothing is ratified):
  orl.py court and orl.py run on must_after_claim.orl: their exit statuses
  orl.py court and orl.py run with --backends c99 and no clang on PATH: a backend that did not build
"""
import os
import shutil
import subprocess
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402

KEYS = ("channel", "integrity", "evaluation", "theorem", "ratification", "cost", "cost_reading", "external_bits",
        "support", "cycle", "grounding")   # what cmd_court prints, in its order


def printed(p):
    """The lines orl.py's cmd_court prints for a panel (orl.py, cmd_court)."""
    import json
    lines = []
    for r in p["rows"]:
        lines.append("%s  %s" % (r["clause"], r["text"][:110]))
        lines += ["    %-13s %s" % (k, r[k]) for k in KEYS if k in r]
    lines.append("summary " + json.dumps(p["summary"], sort_keys=True))
    return lines


def part1():
    arb = Arbiter(C.workdir("hidden"), backends=("python",))
    texts = [("tests/fixtures/r8/omit.orl", C.read("tests/fixtures/r8/omit.orl")),
             ("fixtures/hoisted_omit.orl", C.fixture("hoisted_omit.orl")),
             ("fixtures/must_after_claim.orl", C.fixture("must_after_claim.orl"))]
    hidden = 0
    for name, raw in texts:
        comp, w, ref = arb.arbitrate(raw, "hid-" + os.path.basename(name)[:-4])
        p = COURT.panel(comp, w, parse_receipt(ref.receipt()), C.ledger_all(comp))
        out = printed(p)
        code = ref.status.split(" ")[1] if ref.status.startswith("REFUSED") else None
        says = any("REFUSED" in l or (code and code in l) for l in out)
        print("== %s: reference %s; agreeing [%s]" % (name, ref.status, ",".join(w["agreeing"])))
        for l in C.show_rows(p):
            print("   " + l)
        s = p["summary"]
        print("   summary: sandwich %s, well_founded %d, grounded %d" % (s["sandwich"], s["well_founded"], s["grounded"]))
        print("   the court's printed reading %s" % ("names the refusal" if says else
                                                   "NEVER NAMES THE REFUSAL (no 'REFUSED', no %s)" % code))
        hidden += (ref.status.startswith("REFUSED") and not says)
    return hidden


def cli(args, env=None):
    e = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    if env:
        e.update(env)
    r = subprocess.run([sys.executable, "-B", os.path.join(C.ROOT, "orl.py")] + args, capture_output=True, text=True,
                       encoding="utf-8", env=e)
    return r.returncode, r.stdout, r.stderr


def part2():
    wd = C.workdir("cli")
    nothing = os.path.join(C.WORK, "no-such-ledger.jsonl")
    must = os.path.join(C.FIXTURES, "must_after_claim.orl")
    found = 0
    code, out, err = cli(["court", must, "--backends", "python", "--workdir", wd, "--ledger", nothing])
    print("== orl.py court fixtures/must_after_claim.orl --backends python: exit %d; 'REFUSED' or 'MUST-FAILED' in its "
          "output: %s" % (code, "REFUSED" in out or "MUST-FAILED" in out))
    for l in out.splitlines():
        if l.strip().split(" ")[0] in ("§2", "integrity", "evaluation", "support", "grounding", "summary"):
            print("   | " + l)
    found += code == 0 and "MUST-FAILED" not in out
    code, out, err = cli(["run", must, "--backends", "python", "--workdir", wd])
    print("== orl.py run fixtures/must_after_claim.orl --backends python: exit %d" % code)
    print("   | " + out.strip())
    found += code == 0 and "REFUSED MUST-FAILED" in out
    clang = shutil.which("clang")
    if clang is None:
        print("== no clang on PATH here: the build-failure case is not run")
        return found, 2
    bad = os.path.normcase(os.path.dirname(clang))
    path = os.pathsep.join(p for p in os.environ.get("PATH", "").split(os.pathsep) if os.path.normcase(p) != bad)
    collatz = os.path.join(C.ROOT, "examples", "collatz.orl")
    wd2 = C.workdir("cli-noclang")      # a work folder of its own, so no cached C build can answer for clang
    shutil.rmtree(os.path.join(wd2, "cache"), ignore_errors=True)
    code_c, out_c, _ = cli(["court", collatz, "--backends", "c99", "--workdir", wd2, "--ledger", nothing],
                           env={"PATH": path})
    code_r, out_r, _ = cli(["run", collatz, "--backends", "c99", "--workdir", wd2], env={"PATH": path})
    integ = [l.strip() for l in out_c.splitlines() if l.strip().startswith("integrity")]
    print("== examples/collatz.orl --backends c99 with clang's folder removed from PATH")
    print("   orl.py run   exit %d | %s" % (code_r, out_r.strip().splitlines()[0] if out_r.strip() else ""))
    print("   orl.py court exit %d | %s" % (code_c, integ[0] if integ else out_c.strip()[:200]))
    found += code_c == 0 and code_r == 2
    return found, 3


def main():
    hidden = part1()
    found, cases = part2()
    print("REFUSAL NOT NAMED BY THE COURT'S READING: %d of 2 refused runs (the R8 control names its own)" % hidden)
    print("EXIT 0 OVER A REFUSAL OR A FAILED BUILD: %d of %d command-line cases" % (found, cases))
    return 0


if __name__ == "__main__":
    sys.exit(main())

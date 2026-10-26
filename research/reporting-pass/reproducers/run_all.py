"""Run the reporting pass's reproducers and record each one's output as evidence, headed by its command and tree.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/run_all.py [--out DIR] [--with-mutants]

Each reproducer runs in a process of its own (from the repository's root); its stdout and stderr go to
DIR/<name>.txt (default research/reporting-pass/evidence/). court_mutants.py takes about a quarter of an hour, so it
runs only with --with-mutants. The header names the HEAD commit, whether the working tree differs from it, and the
sha256 of each reporting file as it stood, so that a later reader can tell which code the output describes.
"""
import argparse
import datetime
import hashlib
import os
import platform
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
QUICK = ["unguarded_held", "agreement_conditions", "r8_default", "refusal_hidden", "provenance_cache",
         "witness_receipt_sha", "summary_absorbs", "cost_over_refusal", "compat_gate", "monotone_blind",
         "r8_wording", "ledger_malformed", "cli_omissions", "r8_exact_sites"]
FILES = ["src/orlog/court.py", "src/orlog/arbiter.py", "src/orlog/interp.py", "orl.py", "tests/selftest.py",
         "tests/compat.py", "tests/court_monotone.py"]


def header(name):
    head = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout
    dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--untracked-files=no"], capture_output=True,
                           text=True).stdout.strip()
    lines = ["# command: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/%s.py" % name,
             "# tree: %s%s" % (head.strip(), " plus uncommitted changes to tracked files (the R8 repair, as it stood)"
                               if dirty else ""),
             "# host: %s, CPython %s; %s" % (platform.system(), platform.python_version(),
                                             datetime.date.today().isoformat())]
    for f in FILES:
        with open(os.path.join(ROOT, f), "rb") as fh:
            lines.append("# sha256 %s  %s" % (hashlib.sha256(fh.read()).hexdigest()[:16], f))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "reporting-pass", "evidence"))
    ap.add_argument("--with-mutants", action="store_true")
    ap.add_argument("--only", help="comma-separated reproducer names")
    a = ap.parse_args(argv)
    if os.environ.get("PYTHONHASHSEED") != "0":
        print("set PYTHONHASHSEED=0")
        return 2
    os.makedirs(a.out, exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    names = QUICK + (["court_mutants"] if a.with_mutants else [])
    if a.only:
        names = a.only.split(",")
    for name in names:
        r = subprocess.run([sys.executable, "-B", os.path.join(HERE, name + ".py")], cwd=ROOT, env=env,
                           capture_output=True, text=True, encoding="utf-8")
        body = r.stdout + ("--- stderr ---\n" + r.stderr if r.stderr.strip() else "") + "exit %d\n" % r.returncode
        with open(os.path.join(a.out, name + ".txt"), "wb") as fh:
            fh.write((header(name) + body).encode("utf-8"))
        print("%-22s exit %d, last line: %s" % (name, r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:110]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

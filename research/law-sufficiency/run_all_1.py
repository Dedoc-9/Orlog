"""LAW-SUFFICIENCY-1: run the closure experiments twice and write their evidence (SHEET-1.md).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/run_all_1.py

closure_tests.py runs twice, one run after the other. Its two outputs, with CR LF made LF, must be byte-identical. The
second run finds the arbiter's builds of the first in its cache, which the arbiter checks against its records before
using. The evidence goes to evidence/law-sufficiency-1.txt: header lines starting '#', then the output, LF only. The
runner refuses to write if HEAD is not the starting commit, or if src/, tests/ or vectors/ differ from it."""
import hashlib
import os
import platform
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
CODE = ["common.py", "decoder.py", "decoder1.py", "closure_tests.py", "run_all_1.py"]
ENV = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("RUN-ALL-1: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("RUN-ALL-1: src/, tests/ or vectors/ differ from the starting commit")
    fx = os.path.join(HERE, "fixtures")
    code = "; ".join("%s %s" % (f, sha(os.path.join(HERE, f))[:16]) for f in CODE)
    fixtures = "; ".join("%s %s" % (f, sha(os.path.join(fx, f))[:16]) for f in sorted(os.listdir(fx)) if f.endswith(".orl"))
    runs = []
    for _ in (1, 2):
        p = subprocess.run([sys.executable, "-B", os.path.join(HERE, "closure_tests.py")], cwd=ROOT, env=ENV,
                           capture_output=True)
        runs.append((p.returncode, p.stdout.replace(b"\r\n", b"\n"), p.stderr.replace(b"\r\n", b"\n")))
    (rc1, o1, e1), (rc2, o2, e2) = runs
    same = o1 == o2 and rc1 == rc2
    head = [
        "# command: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/closure_tests.py",
        "# tree: %s plus the uncommitted research/law-sufficiency/ files (src/, tests/ and vectors/ unchanged); %s, "
        "CPython %s; %s; exit %d; run twice, %s" % (BASE[:7], platform.system(), platform.python_version(),
                                                   time.strftime("%Y-%m-%d"), rc1, "identical" if same else "NOT IDENTICAL"),
        "# code sha256 (first 16 hex): %s" % code,
        "# fixtures sha256 (first 16 hex): %s" % fixtures,
        "# EXPERIMENTAL RESEARCH, off the gate (research/law-sufficiency/SHEET-1.md): MEASURED on these texts and these "
        "plants only, never ESTABLISHED; not a ruling",
    ]
    if e1 or e2:
        head.append("# stderr, first run: %d bytes; second run: %d bytes (the first kept below the output)" % (len(e1), len(e2)))
    body = o1 + ((b"\n--- stderr of the first run\n" + e1) if e1 else b"")
    with open(os.path.join(ROOT, "evidence", "law-sufficiency-1.txt"), "wb") as f:
        f.write(("\n".join(head) + "\n").encode("utf-8") + body)
    last = o1.rstrip(b"\n").split(b"\n")[-1].decode("utf-8")
    print("closure_tests.py exit %d, twice %s: %s" % (rc1, "identical" if same else "NOT IDENTICAL", last))
    sys.exit(0 if rc1 == 0 and same else 1)


if __name__ == "__main__":
    main()

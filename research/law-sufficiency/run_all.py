"""LAW-SUFFICIENCY-0: run each of the three tests twice and write its evidence (SHEET.md, "What it would cost").

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/run_all.py

Each test runs twice, one run after the other. Its two outputs, with CR LF made LF, must be byte-identical. The
evidence is written to evidence/law-sufficiency-test{1,2,3}.txt: header lines starting '#' (the command, the tree, the
code's sha256, the date, the exit status and whether the two runs agree), then the output, LF only. The runner refuses
to write if the starting commit is not HEAD, or if src/, tests/ or vectors/ differ from it."""
import hashlib
import os
import platform
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
TESTS = [("test1_reads.py", "law-sufficiency-test1.txt"), ("test2_equal_seal.py", "law-sufficiency-test2.txt"),
         ("test3_decoder.py", "law-sufficiency-test3.txt")]
CODE = ["common.py", "decoder.py", "test1_reads.py", "test2_equal_seal.py", "test3_decoder.py", "run_all.py"]
ENV = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("RUN-ALL: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("RUN-ALL: src/, tests/ or vectors/ differ from the starting commit")
    code = "; ".join("%s %s" % (f, sha(os.path.join(HERE, f))[:16]) for f in CODE)
    host = "%s, CPython %s" % (platform.system(), platform.python_version())
    verdicts = []
    for script, out in TESTS:
        runs = []
        for _ in (1, 2):
            p = subprocess.run([sys.executable, "-B", os.path.join(HERE, script)], cwd=ROOT, env=ENV,
                               capture_output=True)
            runs.append((p.returncode, p.stdout.replace(b"\r\n", b"\n"), p.stderr))
        (rc1, o1, e1), (rc2, o2, e2) = runs
        same = o1 == o2 and rc1 == rc2
        last = o1.rstrip(b"\n").split(b"\n")[-1].decode("utf-8")
        head = [
            "# command: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/%s" % script,
            "# tree: %s plus the uncommitted research/law-sufficiency/ files (src/, tests/ and vectors/ unchanged); "
            "%s; %s; exit %d; run twice, %s" % (BASE[:7], host, time.strftime("%Y-%m-%d"), rc1,
                                               "identical" if same else "NOT IDENTICAL"),
            "# code sha256 (first 16 hex): %s" % code,
            "# EXPERIMENTAL RESEARCH, off the gate (research/law-sufficiency/SHEET.md): MEASURED on these texts and "
            "these plants only, never ESTABLISHED; not a ruling",
        ]
        if e1 or e2:
            head.append("# stderr, first run: %d bytes; second run: %d bytes (kept below the output)" % (len(e1), len(e2)))
        body = o1 + ((b"\n--- stderr of the first run\n" + e1.replace(b"\r\n", b"\n")) if e1 else b"")
        with open(os.path.join(ROOT, "evidence", out), "wb") as f:
            f.write(("\n".join(head) + "\n").encode("utf-8") + body)
        verdicts.append((script, rc1, same, last))
        print("%-22s exit %d, twice %s: %s" % (script, rc1, "identical" if same else "NOT IDENTICAL", last), flush=True)
    ok = all(rc == 0 and same for _, rc, same, _ in verdicts)
    print("LAW-SUFFICIENCY-0 %s" % ("RUN: all three tests held, each run twice identically" if ok else "RUN: NOT ALL HELD"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

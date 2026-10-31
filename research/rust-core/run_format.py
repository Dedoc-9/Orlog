"""RUST-CORE-0 phase 0: run LAW-FORMAT-0's checker twice and write its evidence.

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/run_format.py

Draft 9's run since his ruling on REREAD-9's disposition (SHEET.md Amendment 13) goes to
evidence/rust-core-format-9-r9.txt, plant_reverts.py's to evidence/rust-core-format-9-r9-reverts.txt,
ref_run_paths.py's to evidence/rust-core-ref-run-paths-9-r9.txt, ref_run_variants.py's to
evidence/rust-core-ref-run-variants-9-r9.txt and depth_probe.py's (his D1 and H) to evidence/rust-core-depth-9-r9.txt,
each run twice. Draft 9's earlier records stay as they are: the -9 files (Amendment 11) and the -9-zb files (Amendment
12) (his ruling on ZB3 and ZB5: "preserve the old records and hashes so the change is auditable"; his D9: "From this
point forward, preserve every hash-identified input before overwriting it.").
evidence/rust-core-format.txt and -1.txt to -7.txt (with -4- to -7-reverts.txt, and rust-core-ref-run-paths.txt and -7)
stay the records of drafts 0 to 7 (the owner's word: the first draft and its records are kept intact). It refuses to write if HEAD is not the starting
commit, or if src/, tests/ or vectors/ differ from it."""
import hashlib
import os
import platform
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
ENV = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
OUT = os.path.join(ROOT, "evidence", "rust-core-format-9-r9.txt")
OUT_REVERTS = os.path.join(ROOT, "evidence", "rust-core-format-9-r9-reverts.txt")
OUT_PATHS = os.path.join(ROOT, "evidence", "rust-core-ref-run-paths-9-r9.txt")
OUT_VARIANTS = os.path.join(ROOT, "evidence", "rust-core-ref-run-variants-9-r9.txt")
OUT_DEPTH = os.path.join(ROOT, "evidence", "rust-core-depth-9-r9.txt")
CODE = ("LAW-FORMAT-0-DRAFT-9.md", "format_check.py", "plant_reverts.py", "ref_run.py", "ref_run_paths.py",
        "ref_run_variants.py", "depth_probe.py", "run_format.py", "vectors-as-integer.txt", "vectors-as-integer.manifest")


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("RUN-FORMAT: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("RUN-FORMAT: src/, tests/ or vectors/ differ from the starting commit")
    code = "; ".join("%s %s" % (f, sha(os.path.join(HERE, f))[:16]) for f in CODE)
    ok = True
    for script, out, what in (("format_check.py", OUT, "these laws and these plants only"),
                              ("plant_reverts.py", OUT_REVERTS, "these plants and these undoings only"),
                              ("ref_run_paths.py", OUT_PATHS, "these runs of the reference runner only"),
                              ("ref_run_variants.py", OUT_VARIANTS, "these changes of the runner and its check only"),
                              ("depth_probe.py", OUT_DEPTH, "these texts through the front end only, a lower bound by a witness")):
        runs = []
        for _ in (1, 2):
            p = subprocess.run([sys.executable, "-B", os.path.join(HERE, script)], cwd=ROOT, env=ENV,
                               capture_output=True)
            runs.append((p.returncode, p.stdout.replace(b"\r\n", b"\n"), p.stderr))
        (rc1, o1, e1), (rc2, o2, e2) = runs
        same = o1 == o2 and rc1 == rc2
        head = [
            "# command: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/%s" % script,
            "# tree: %s plus the uncommitted research files (src/, tests/ and vectors/ unchanged; the contract vectors "
            "sha256 %s); %s, CPython %s; %s; exit %d; run twice, %s" % (
                BASE[:7], sha(os.path.join(ROOT, "vectors", "runtime-vectors.txt"))[:16], platform.system(),
                platform.python_version(), time.strftime("%Y-%m-%d"), rc1, "identical" if same else "NOT IDENTICAL"),
            "# code and data sha256 (first 16 hex): %s" % code,
            "# RUST-CORE-0 phase 0, LAW-FORMAT-0 draft 9, off the gate: MEASURED on %s, never ESTABLISHED; evidence "
            "for the format, not its authority; not a ruling" % what,
        ]
        if e1 or e2:
            head.append("# stderr, first run: %d bytes; second run: %d bytes" % (len(e1), len(e2)))
        with open(out, "wb") as f:
            f.write(("\n".join(head) + "\n").encode("utf-8") + o1)
        print("%s exit %d, twice %s: %s" % (script, rc1, "identical" if same else "NOT IDENTICAL",
                                            o1.rstrip(b"\n").split(b"\n")[-1].decode("utf-8")))
        ok = ok and rc1 == 0 and same
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

"""Does the C backend leak lists (rt_c/NOTES.md finding 8)? A 2,000,000-item list is stored into another variable
N times, and the generated program's peak memory is read for N = 4 and N = 32. A measurement, not a test.

  PYTHONHASHSEED=0 python -B tests/e21_list_leak.py

History (prosecutor F15): the script was written in the session's work folder while E21 was repaired, and its
before and after figures (evidence/e21-lists-before.txt, -after.txt) were taken there. It imports child_peak from
tests/selftest.py, which commit 7186e50 does not have, so it could not have run unmodified on that commit. It is
tracked from this commit on, so that its figures can be taken again.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import selftest  # noqa: E402
from orlog.arbiter import generate  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.lower import Lowered  # noqa: E402

MB = 1 << 20
for n in (4, 32):
    lines = ["§1 Let xs be a list of 2000000 copies of 1.", "§2 Let ys be a list of 1 copies of 0.",
             "§3 For each k from 1 to %d, do the following." % n, "§3.1 Set ys to xs.", "§4 Say the length of ys."]
    comp = compile_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    assert comp.ok, comp.error
    src = generate("c99", Lowered(comp))
    tmp = tempfile.mkdtemp(prefix="orlog-listleak-")
    try:
        with open(os.path.join(tmp, "p.c"), "wb") as fh:
            fh.write(src.encode("utf-8"))
        subprocess.run(["clang"] + selftest.C_FLAGS + ["p.c", "-o", "p.exe"], cwd=tmp, capture_output=True)
        rc, pk = selftest.child_peak([os.path.join(tmp, "p.exe"), "out.bin", "receipt.txt"], tmp)
        print("lists: N=%-3d exit %d  c99 peak commit %4d MiB" % (n, rc, pk // MB))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

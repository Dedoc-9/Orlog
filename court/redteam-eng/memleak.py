"""Peak memory of the C99 and Python backends on a loop that rebuilds one 16 MiB text N times.

The program holds one text at a time (the reference and Python free the old one); the C runtime's orl_s_take
copies are never freed (rt_c/NOTES.md finding 8), so the C peak grows by about 16 MiB per iteration.
Windows only (GetProcessMemoryInfo on the child's handle after it exits).
  python -B memleak.py
"""
import ctypes
import ctypes.wintypes as wt
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.arbiter import Arbiter  # noqa: E402


class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t), ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t)]


def peak(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    p.wait()
    pmc = PMC()
    pmc.cb = ctypes.sizeof(PMC)
    ok = ctypes.windll.psapi.GetProcessMemoryInfo(wt.HANDLE(int(p._handle)), ctypes.byref(pmc), pmc.cb)
    return p.returncode, (pmc.PeakPagefileUsage if ok else -1)


def program(n):
    lines = ["§1 Let t be \"x\".", "§2 For each i from 1 to 24, do the following.",
             "§2.1 Set t to t followed by t.", "§3 Let n be 0.",
             "§4 While n is less than %d, at most %d times, do the following." % (n, n + 1),
             "§4.1 Increase n by 1.", "§4.2 Set t to t followed by \"\".", "§5 Say n."]
    return ("\n".join(lines) + "\n").encode("utf-8")


def main():
    wd = os.path.join(HERE, "work", "memleak")
    for n in (5, 20, 40):
        arb = Arbiter(wd, backends=("python", "c99"))
        comp, w, ref = arb.arbitrate(program(n), "leak-%d" % n)
        row = ["N=%-3d ref %s agree %s" % (n, ref.status, w["agreeing"])]
        for b in ("c99", "python"):
            src = [p for p in glob.glob(os.path.join(wd, "cache", "%s-*.%s" % (b, "c" if b == "c99" else "py")))
                   if comp.seal_words.encode() in open(p, "rb").read(600)][0]
            cmd = [os.path.splitext(src)[0] + ".exe"] if b == "c99" else [sys.executable, "-I", "-B", src]
            rc, pk = peak(cmd + [os.path.join(wd, "m.out"), os.path.join(wd, "m.receipt")])
            row.append("%s peak commit %4d MiB (exit %d)" % (b, pk // (1 << 20), rc))
        print("  ".join(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())

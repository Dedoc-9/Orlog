"""Software timings for the judge's spherical-harmonic laws (research/speed): the compiled C and Rust programs the
arbiter built, each run as a fresh process, R = 4 against R = 16, so that the difference divided by the extra
directions is the marginal cost of one direction with the process's start taken out. Also the reference interpreter
in this process, R = 4 against R = 16. Software timings on this host, never a frame rate or a latency.
  PYTHONHASHSEED=0 python -B research/speed/judge/time_sh.py [runs]
"""
import glob
import os
import statistics
import subprocess
import sys
import tempfile
import time

# the judge's scripts live in research/speed/judge/; what they make and read lives in work/speed-judge/, which
# git ignores
HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "work",
                                     "speed-judge"))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CACHE = os.path.join(HERE, "runs", "cache")
sys.path.insert(0, os.path.join(ROOT, "src"))

N_DIR = {4: 9 ** 3 - 1, 16: 33 ** 3 - 1}


def exe_for(backend, r, tmp):
    """The cached executable whose output says the directions of R."""
    want = "directions %d " % N_DIR[r]
    for exe in sorted(glob.glob(os.path.join(CACHE, backend + "-*.exe"))):
        out, rec = os.path.join(tmp, "o.txt"), os.path.join(tmp, "r.txt")
        subprocess.run([exe, out, rec], capture_output=True)
        with open(out, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
        if text.startswith(want) and "sums" in text and len(text.splitlines()) == 1:
            return exe
    raise SystemExit("no cached %s build says %r" % (backend, want))


def time_exe(exe, runs, tmp):
    out, rec = os.path.join(tmp, "o.txt"), os.path.join(tmp, "r.txt")
    ts = []
    for _ in range(runs):
        t0 = time.perf_counter()
        subprocess.run([exe, out, rec], capture_output=True)
        ts.append(time.perf_counter() - t0)
    return ts


def time_reference(r, runs):
    """The reference interpreter in this process, as the arbiter calls it (arbiter.py: Interp(...).run())."""
    from orlog.front import compile_bytes
    from orlog.interp import Interp
    with open(os.path.join(HERE, "sh_sum_r%d.orl" % r), "rb") as fh:
        comp = compile_bytes(fh.read())
    ts = []
    for _ in range(runs):
        t0 = time.perf_counter()
        Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
        ts.append(time.perf_counter() - t0)
    return ts


def show(label, ts):
    q = statistics.quantiles(ts, n=10)
    print("  %-28s n %3d  median %9.3f ms  p10 %9.3f  p90 %9.3f" % (label, len(ts), 1e3 * statistics.median(ts),
                                                                     1e3 * q[0], 1e3 * q[-1]))
    return statistics.median(ts)


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    info = time.get_clock_info("perf_counter")
    print("clock perf_counter, resolution %.3g s, monotonic %s" % (info.resolution, info.monotonic))
    extra = N_DIR[16] - N_DIR[4]
    with tempfile.TemporaryDirectory(dir=os.path.join(HERE, "runs")) as tmp:
        for backend in ("c99", "rust"):
            e4, e16 = exe_for(backend, 4, tmp), exe_for(backend, 16, tmp)
            time_exe(e4, 3, tmp), time_exe(e16, 3, tmp)          # warm the file cache
            print("== %s, each run a fresh process (output and receipt written)" % backend)
            m4 = show("R 4  (%d directions)" % N_DIR[4], time_exe(e4, runs, tmp))
            m16 = show("R 16 (%d directions)" % N_DIR[16], time_exe(e16, runs, tmp))
            print("  marginal: %.3f us a direction (median difference over %d extra directions)" % (
                1e6 * (m16 - m4) / extra, extra))
    print("== the reference interpreter, in this process (no process start)")
    r4 = show("R 4  (%d directions)" % N_DIR[4], time_reference(4, 5))
    r16 = show("R 16 (%d directions)" % N_DIR[16], time_reference(16, 5))
    print("  marginal: %.3f us a direction (median difference over %d extra directions)" % (
        1e6 * (r16 - r4) / extra, extra))


if __name__ == "__main__":
    main()

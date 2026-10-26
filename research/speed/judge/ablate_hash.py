"""An ablation for research/speed, not an execution of Ørlǫg: the C programs the arbiter generated for the judge's
spherical-harmonic laws (R = 4 and R = 16), rebuilt with the arbiter's own flags, once as generated and once with the
event hash chain's SHA-256 calls removed (orl__ev_begin, orl__ev_put, orl__ev_end). The patched program's receipt is
wrong by construction; only its time is read. What it asks: of the marginal cost of one direction, how much is the
per-event commitment and how much the arithmetic. Software timings on this host.
  PYTHONHASHSEED=0 python -B research/speed/judge/ablate_hash.py [runs]
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
CACHE = os.path.join(HERE, "runs", "cache")
OUT = os.path.join(HERE, "ablate")
C_FLAGS = ["-std=c99", "-O2", "-ffp-contract=off", "-fno-fast-math", "-Wall", "-Wno-unused-variable",
           "-Wno-unused-but-set-variable", "-Wno-unused-function"]          # src/orlog/arbiter.py, C_FLAGS
N_DIR = {4: 9 ** 3 - 1, 16: 33 ** 3 - 1}
CUTS = ["orl__sha_init(&x->h);", "orl__sha_update(&x->h, orl__head, 32);", "orl__sha_update(&x->h, hd, 9);",
        "orl__sha_update(&x->h, p, n);", "orl__sha_final(&x->h, orl__head);"]


def source_for(r, tmp):
    want = "directions %d " % N_DIR[r]
    for exe in sorted(glob.glob(os.path.join(CACHE, "c99-*.exe"))):
        out, rec = os.path.join(tmp, "o.txt"), os.path.join(tmp, "r.txt")
        subprocess.run([exe, out, rec], capture_output=True)
        with open(out, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
        if text.startswith(want) and len(text.splitlines()) == 1:
            return exe[:-4] + ".c"
    raise SystemExit("no cached c99 build for R %d" % r)


def build(src_text, name):
    path = os.path.join(OUT, name + ".c")
    with open(path, "wb") as fh:
        fh.write(src_text.encode("utf-8"))
    exe = os.path.join(OUT, name + ".exe")
    r = subprocess.run(["clang"] + C_FLAGS + [path, "-o", exe], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("build failed: %s\n%s" % (name, r.stderr[-2000:]))
    return exe


def timed(exe, runs, tmp):
    out, rec = os.path.join(tmp, "o.txt"), os.path.join(tmp, "r.txt")
    for _ in range(3):
        subprocess.run([exe, out, rec], capture_output=True)
    ts = []
    for _ in range(runs):
        t0 = time.perf_counter()
        subprocess.run([exe, out, rec], capture_output=True)
        ts.append(time.perf_counter() - t0)
    with open(out, "rb") as fh:
        said = fh.read().decode("utf-8", "replace").split(" sums")[0]
    return statistics.median(ts), said


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    os.makedirs(OUT, exist_ok=True)
    info = time.get_clock_info("perf_counter")
    print("clock perf_counter, resolution %.3g s; %d runs a cell, the median; each run a fresh process" % (
        info.resolution, runs))
    extra = N_DIR[16] - N_DIR[4]
    with tempfile.TemporaryDirectory(dir=OUT) as tmp:
        med = {}
        for r in (4, 16):
            with open(source_for(r, tmp), "rb") as fh:
                text = fh.read().decode("utf-8")
            cut = text
            for c in CUTS:
                if cut.count(c) != 1:
                    raise SystemExit("expected one %r in the generated C, found %d" % (c, cut.count(c)))
                cut = cut.replace(c, "/* ablated */")
            for arm, src in (("as generated", text), ("hash removed", cut)):
                exe = build(src, "r%d-%s" % (r, "gen" if arm == "as generated" else "nohash"))
                med[(r, arm)], said = timed(exe, runs, tmp)
                print("  R %-2d %-13s median %9.3f ms   (%s)" % (r, arm, 1e3 * med[(r, arm)], said))
        for arm in ("as generated", "hash removed"):
            print("  marginal, %-13s %.3f us a direction" % (arm, 1e6 * (med[(16, arm)] - med[(4, arm)]) / extra))


if __name__ == "__main__":
    main()

"""The graybox's walk onto and off a ledge, checked three ways and reported apart:
  1. the Orlog reference interpreter versus the clean-room twin (twin/twin.py), by byte equality of output;
  2. both implementations versus the exact prediction in PREDICTION.txt (a mathematical comparison);
  3. the Orlog reference versus Verdandi's own rules-1 tick (graybox/tick_ref.py), driven through the same scenario,
     bit for bit (an implementation comparison, not physical validation).

This is the repository version: it resolves the compiler and the twin relative to the repository root, reads the
program from examples/stepwalk.orl, loads the requested tick_ref.py explicitly (no sys.modules reuse), reports source
provenance (the loaded tick_ref.py sha256 and, when available, both git HEADs), and fails loudly on a row-count
mismatch before comparing rows.

  python -B research/stepwalk/compare.py                        # the prediction and the clean-room twin
  python -B research/stepwalk/compare.py --verdandi DIR         # and the bit-level comparison with tick_ref.py
  python -B research/stepwalk/compare.py --verdandi DIR --plant NAME   # a planted defect, which must end NOT HELD, exit 1

Plants (bytes changed in memory before compile; examples/stepwalk.orl is untouched):
  step-shrunk    : step 0.55 -> 0.45; the step-down follow (branch B) fails, the grounded guard trips.
  ledge-interval : the ground's upper edge 4.35 -> 4.30; the mount lands one tick late, diverging from tick_ref.
Run from the repository root with PYTHONHASHSEED=0 (PYTHONUTF8=1 if stdout is redirected). It writes nothing.
The recorded run is evidence/stepwalk-tick-ref.txt.
"""
import hashlib
import importlib.util
import os
import struct
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))            # research/stepwalk -> research -> repository root
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.canon import canonicalize          # noqa: E402
from orlog.front import compile_bytes          # noqa: E402
from orlog import interp                        # noqa: E402

TICKS = 125
PRED_MOUNT, PRED_DOWN = 64, 118                 # from PREDICTION.txt, written first


def bits(x):
    return struct.pack(">d", x).hex()


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git_head(d):
    try:
        out = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


PLANTS = {
    "step-shrunk":    (b"Let step be 0.55.", b"Let step be 0.45."),
    "ledge-interval": (b"z is less than 4.35", b"z is less than 4.30"),
}


def load_twin():
    spec = importlib.util.spec_from_file_location("stepwalk_twin", os.path.join(ROOT, "twin", "twin.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse(out_bytes):
    rows = []
    for line in out_bytes.decode("ascii").splitlines():
        n, z, feet, vy = line.split(" ")
        fz, ff, fv = Fraction(z), Fraction(feet), Fraction(vy)
        z, feet, vy = float(fz), float(ff), float(fv)
        assert Fraction(z) == fz and Fraction(feet) == ff and Fraction(vy) == fv, "a said value is not a binary64"
        rows.append((int(n), z, feet, vy))
    return rows


def orlog_run(plant=None):
    with open(os.path.join(ROOT, "examples", "stepwalk.orl"), "rb") as fh:
        raw = fh.read()
    if plant is not None:
        old, new = PLANTS[plant]
        assert raw.count(old) == 1, "the plant's text is not in the program once"
        raw = raw.replace(old, new)
    comp = compile_bytes(raw)
    assert comp.ok, comp.error
    it = interp.Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
    ref_out = bytes(it.out)
    # the clean-room twin: its own front end, on the door's canonical text
    twin = load_twin()
    canon = canonicalize(raw)
    trt, tstatus = twin.execute(twin.compile_text(canon.text, comp.law_seal), comp.law_seal)
    twin_out = bytes(trt.out)
    twin_ok = twin_out == ref_out and tstatus == it.status
    print("the clean-room twin: status %s (reference %s); twin output sha256 %s; reference output sha256 %s"
          % (tstatus, it.status, hashlib.sha256(twin_out).hexdigest(), hashlib.sha256(ref_out).hexdigest()))
    print("   twin vs reference, by byte equality of output and equal status: %s" % twin_ok)
    return comp.law_seal, it.status, parse(ref_out), parse(twin_out), twin_ok


def transitions(rows):
    mount = next((n for n, z, f, v in rows if f == 0.5), None)
    down = next((n for n, z, f, v in rows if mount is not None and n > mount and f == 0.0), None)
    return mount, down


def against_prediction(name, rows):
    mount, down = transitions(rows)
    feet_ok = (all(f == 0.0 for n, z, f, v in rows if n < PRED_MOUNT)
               and all(f == 0.5 for n, z, f, v in rows if PRED_MOUNT <= n < PRED_DOWN)
               and all(f == 0.0 for n, z, f, v in rows if n >= PRED_DOWN))
    vy_ok = all(v == 0.0 for n, z, f, v in rows)
    ok = mount == PRED_MOUNT and down == PRED_DOWN and feet_ok and vy_ok and len(rows) == TICKS
    print("%s against the prediction (mathematical comparison)" % name)
    print("   mount tick %s (predicted %d); step-down tick %s (predicted %d); rows %d (expected %d)"
          % (mount, PRED_MOUNT, down, PRED_DOWN, len(rows), TICKS))
    print("   feet 0 before mount, 0.5 while mounted, 0 after step-down: %s; vy 0 every tick: %s" % (feet_ok, vy_ok))
    print("   %s" % ("HELD" if ok else "NOT HELD"))
    return ok


def load_tickref(verdandi):
    path = os.path.join(verdandi, "graybox", "tick_ref.py")
    if not os.path.isfile(path):
        raise SystemExit("tick_ref.py not found at %s" % path)
    print("Verdandi graybox/tick_ref.py: sha256 %s; git HEAD %s" % (sha256_file(path), git_head(verdandi) or "unknown"))
    spec = importlib.util.spec_from_file_location("stepwalk_tickref", path)   # explicit load; no sys.modules reuse
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tickref_run(T):
    conv = {"collision": {"w": 1, "h": 8, "cell": 1, "tops": [0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0]},
            "canonical": {"spawns": {"A": {"x": 0, "z": 7, "yaw": 0}, "B": {"x": 0, "z": 7, "yaw": 0}},
                          "objective": None, "targets": []}}
    world = T.World(conv)
    s = T.State.new(world, "A")
    s.x, s.z, s.feet, s.vy, s.yaw, s.pitch, s.on_ground = 0.5, 7.52, 0.0, 0.0, 0.0, 0.0, True
    rows = []
    for n in range(1, TICKS + 1):
        T.tick(world, s, {"f": True})
        rows.append((n, s.z, s.feet, s.vy))
    return rows


def main(argv):
    verdandi = plant = None
    args = list(argv)
    while args:
        flag = args.pop(0)
        if flag == "--verdandi" and args and verdandi is None:
            verdandi = args.pop(0)
        elif flag == "--plant" and args and plant is None and args[0] in PLANTS:
            plant = args.pop(0)
        else:
            raise SystemExit(__doc__)
    print("Orlog repository git HEAD %s" % (git_head(ROOT) or "unknown"))
    law, status, o, twin_rows, twin_ok = orlog_run(plant)
    print("examples/stepwalk.orl%s: law seal %s, reference %s, %d ticks said"
          % (" with the plant " + plant if plant else "", law, status, len(o)))
    ok = len(o) == TICKS and status == "COMPLETED" and twin_ok
    ok = against_prediction("Orlog reference", o) and ok
    ok = against_prediction("clean-room twin (its own parsed output)", twin_rows) and ok
    if verdandi is None:
        print("bit-level comparison with Verdandi's tick_ref.py: NOT RUN (no --verdandi given)")
    else:
        T = load_tickref(verdandi)
        t = tickref_run(T)
        print("bit-level comparison with Verdandi's tick_ref.py (implementation comparison, not physical validation)")
        print("   Orlog rows %d; tick_ref rows %d" % (len(o), len(t)))
        if len(o) != len(t):
            print("   ROW COUNT MISMATCH: rows not compared -- NOT HELD")
            ok = False
        else:
            diff = [n for (n, a, b, c), (_, d, e, f) in zip(o, t)
                    if bits(a) != bits(d) or bits(b) != bits(e) or bits(c) != bits(f)]
            print("   ticks whose z, feet or vy differ in any bit: %d %s" % (len(diff), diff[:10]))
            ok = (not diff) and against_prediction("tick_ref.py", t) and ok
    print("STEPWALK %s" % ("HELD" if ok else "NOT HELD"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

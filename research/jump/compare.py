"""The vertical jump, checked two ways: examples/jump.orl against the exact prediction in PREDICTION.txt, and, when a
Verdandi checkout is given, against Verdandi's own rules-1 tick (graybox/tick_ref.py), bit for bit.

  python -B research/jump/compare.py                          # the prediction only
  python -B research/jump/compare.py --verdandi DIR           # and the bit-level comparison (DIR: a Verdandi tree)
  python -B research/jump/compare.py --verdandi DIR --plant NAME   # a planted defect, which must end NOT HELD

The plants change the program's bytes in memory before it is compiled (the file is not touched): explicit-euler swaps
clauses 7.2 and 7.3; gravity-ulp sets gravity one ulp above 20. Each must end JUMP NOT HELD, exit 1.

Run from the repository's root with PYTHONHASHSEED=0. It writes nothing. The recorded run is evidence/jump-tick-ref.txt,
against Verdandi b441a1e5ccc33351ed0307a7062bd65423b3db90.

Two comparisons, reported apart. Bit-level agreement with tick_ref.py is an implementation comparison, not physical
validation. Agreement with the prediction is a mathematical comparison: the prediction is exact rational arithmetic,
independent of both implementations but not of their author.
"""
import hashlib
import importlib.util
import math
import os
import struct
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog.canon import canonicalize  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog import interp  # noqa: E402

TICKS = 100
PRED_MAX, PRED_TICKS, CONT = Fraction(287, 240), [41, 42], Fraction(49, 40)


def bits(x):
    return struct.pack(">d", x).hex()


PLANTS = {
    "explicit-euler": (b"7.2. Set vy to vy - gravity * step.\n7.3. Set feet to feet + vy * step.\n",
                       b"7.2. Set feet to feet + vy * step.\n7.3. Set vy to vy - gravity * step.\n"),
    "gravity-ulp": (b"Let gravity be 20.0.", b"Let gravity be 20.000000000000004."),
}


def orlog_run(plant=None):
    with open(os.path.join(ROOT, "examples", "jump.orl"), "rb") as fh:
        raw = fh.read()
    if plant is not None:
        old, new = PLANTS[plant]
        assert raw.count(old) == 1, "the plant's text is not in the program once"
        raw = raw.replace(old, new)
    comp = compile_bytes(raw)
    assert comp.ok, comp.error
    it = interp.Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
    # the clean-room twin (twin/twin.py), whose front end is its own, on the door's canonical text
    spec = importlib.util.spec_from_file_location("orlog_twin", os.path.join(ROOT, "twin", "twin.py"))
    twin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(twin)
    canon = canonicalize(raw)
    trt, tstatus = twin.execute(twin.compile_text(canon.text, comp.law_seal), comp.law_seal)
    print("the clean-room twin: %s, output %s the reference's (sha256 %s)"
          % (tstatus, "equal to" if bytes(trt.out) == bytes(it.out) and tstatus == it.status else "DIFFERENT FROM",
             hashlib.sha256(bytes(it.out)).hexdigest()))
    twin_ok = bytes(trt.out) == bytes(it.out) and tstatus == it.status
    rows = []
    for line in bytes(it.out).decode("ascii").splitlines():
        n, feet, vy = line.split(" ")
        # Orlog says a Float as its exact decimal expansion, so the Fraction is the binary64 value exactly
        fx, fv = Fraction(feet), Fraction(vy)
        x, v = float(fx), float(fv)
        assert Fraction(x) == fx and Fraction(v) == fv, "a said value is not exactly a binary64"
        rows.append((int(n), x, v))
    return comp.law_seal, it.status, rows, twin_ok


def tickref_run(verdandi):
    sys.path.insert(0, os.path.join(verdandi, "graybox"))
    import tick_ref as T
    conv = {"collision": {"w": 3, "h": 3, "cell": 4, "tops": [0] * 9},
            "canonical": {"spawns": {"A": {"x": 1, "z": 1, "yaw": 0}, "B": {"x": 1, "z": 1, "yaw": 0}},
                          "objective": None, "targets": []}}
    world = T.World(conv)
    s = T.State.new(world, "A")
    assert s.feet == 0.0 and s.vy == 0.0 and s.on_ground
    rows = []
    for n in range(1, TICKS + 1):
        T.tick(world, s, {"jump": True} if n == 1 else {})
        rows.append((n, s.feet, s.vy))
    return rows


def against_prediction(name, rows):
    mx = max(r[1] for r in rows)
    at = [r[0] for r in rows if r[1] == mx]
    land = next((r[0] for r in rows if r[0] > 1 and r[1] == 0.0), None)
    ulp = Fraction(abs(mx - math.nextafter(mx, 0)))
    e = Fraction(mx) - PRED_MAX
    ok = at == PRED_TICKS and abs(e) <= 8 * ulp
    print("%s against the prediction (mathematical comparison)" % name)
    print("   maximum feet %r (bits %s) at tick(s) %s; predicted 287/240 at ticks 41 and 42" % (mx, bits(mx), at))
    print("   measured - 287/240 = %.3e (%.2f ulp); continuous apex 49/40 - measured = %.12f; predicted 7/240 = %.12f"
          % (float(e), float(e / ulp), float(CONT - Fraction(mx)), float(Fraction(7, 240))))
    print("   vy at tick 42: %r (0 in exact arithmetic); first tick back on the ground: %s" % (rows[41][2], land))
    print("   %s: maximum at the predicted ticks and within 8 ulp of 287/240" % ("HELD" if ok else "NOT HELD"))
    return ok


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
    law, status, o, twin_ok = orlog_run(plant)
    print("examples/jump.orl%s: law seal %s, reference %s, %d ticks said"
          % (" with the plant " + plant if plant else "", law, status, len(o)))
    ok = len(o) == TICKS and status == "COMPLETED" and twin_ok
    ok = against_prediction("Orlog", o) and ok
    if verdandi is None:
        print("bit-level comparison with Verdandi's tick_ref.py: NOT RUN (no --verdandi given)")
    else:
        t = tickref_run(verdandi)
        diff = [n for (n, a, b), (_, c, d) in zip(o, t) if bits(a) != bits(c) or bits(b) != bits(d)]
        print("bit-level comparison with Verdandi's tick_ref.py (implementation comparison, not physical validation)")
        print("   ticks compared %d; ticks whose feet or vy differ in any bit: %d %s" % (min(len(o), len(t)), len(diff),
                                                                                   diff[:10]))
        ok = against_prediction("tick_ref.py", t) and ok and not diff and len(t) == len(o)
    print("JUMP %s" % ("HELD" if ok else "NOT HELD"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

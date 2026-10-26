"""Generate the runtime conformance vectors from the reference (numeric_ref).

The vectors are the contract between the reference semantics and the three
runtimes. They are derived from exact rationals; the runtimes implement the
same rules with bit-level algorithms and must reproduce every line.

Line format (ASCII, LF):  <op> <arg> <arg> ... => <result>
  i:<int>   x:<raw int>   f:<16 hex digits, the binary64 bits>   b:0|1
  s:<the printed text, verbatim to end of line>    hex:<bytes>
  !CODE     a refusal
"""
import hashlib
import os
import random
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orlog import numeric_ref as N  # noqa: E402

rng = random.Random(20261025)
out = []


def fb(x):
    return "f:%016X" % N.f_bits(x)


def emit(op, args, fn):
    try:
        r = fn()
    except N.Refusal as e:
        out.append("%s %s => !%s" % (op, " ".join(args), e.code))
        return
    out.append("%s %s => %s" % (op, " ".join(args), r))


INTS = [0, 1, -1, 2, -2, 3, -3, 7, -7, 10, -10, 255, 1 << 31, -(1 << 31), (1 << 31) - 1,
        1 << 32, -(1 << 32), 1 << 53, (1 << 53) + 1, -(1 << 53) - 1, 1 << 62, -(1 << 62),
        N.I64_MAX, N.I64_MIN, N.I64_MAX - 1, N.I64_MIN + 1, 3037000499, 3037000500, -3037000500]


def rint():
    k = rng.choice([4, 8, 16, 31, 32, 33, 48, 62, 63])
    v = rng.getrandbits(k)
    return -v if rng.random() < 0.5 else v


ints = INTS + [rint() for _ in range(60)]

# ---- Int
for a in ints[:40]:
    emit("i_neg", ["i:%d" % a], lambda: "i:%d" % N.i_neg(a))
    emit("i_abs", ["i:%d" % a], lambda: "i:%d" % N.i_abs(a))
    emit("i_isqrt", ["i:%d" % a], lambda: "i:%d" % N.i_isqrt(a))
pairs = [(a, b) for a in INTS for b in INTS[:12]] + [(rint(), rint()) for _ in range(300)]
pairs += [(rint(), rng.choice([1, -1, 2, -2, 3, -3, 5, 7, -7, 1 << 32, N.I64_MIN, N.I64_MAX])) for _ in range(200)]
for a, b in pairs:
    A, B = "i:%d" % a, "i:%d" % b
    for name, f in (("i_add", N.i_add), ("i_sub", N.i_sub), ("i_mul", N.i_mul), ("i_div", N.i_div),
                    ("i_quot", N.i_quot), ("i_rem", N.i_rem)):
        emit(name, [A, B], lambda f=f: "i:%d" % f(a, b))
for a, b in pairs[:60]:
    emit("i_max", ["i:%d" % a, "i:%d" % b], lambda: "i:%d" % N.i_max(a, b))
    emit("i_min", ["i:%d" % a, "i:%d" % b], lambda: "i:%d" % N.i_min(a, b))

# ---- Fix
ONE = N.ONE
FIX = [0, 1, -1, ONE, -ONE, ONE // 2, -(ONE // 2), ONE + ONE // 2, -(ONE + ONE // 2), 3 * ONE, 2 * ONE,
       1 << 31, -(1 << 31), 3 << 31, -(3 << 31), 5 << 31, N.I64_MAX, N.I64_MIN, N.I64_MAX - 1,
       N.I64_MIN + 1, 1 << 62, -(1 << 62), 1 << 47, 429496730, 6074001000, 1 << 33, 3 << 33, -(1 << 33)]
fix = FIX + [rint() for _ in range(60)]
for n in INTS:
    emit("x_from_i", ["i:%d" % n], lambda: "x:%d" % N.x_from_i(n))
for a in fix[:50]:
    A = "x:%d" % a
    emit("x_neg", [A], lambda: "x:%d" % N.x_neg(a))
    emit("x_abs", [A], lambda: "x:%d" % N.x_abs(a))
    emit("x_sqrt", [A], lambda: "x:%d" % N.x_sqrt(a))
    emit("x_trunc", [A], lambda: "i:%d" % N.x_trunc(a))
    emit("x_round", [A], lambda: "i:%d" % N.x_round(a))
    for rd in (0, 1):
        emit("x_to_f", [A, "b:%d" % rd], lambda rd=rd: fb(N.x_to_f(a, bool(rd))))
fpairs = [(a, b) for a in FIX for b in FIX[:14]] + [(rint(), rint()) for _ in range(300)]
fpairs += [(rng.getrandbits(40) - (1 << 39), rng.getrandbits(40) - (1 << 39)) for _ in range(300)]
for a, b in fpairs:
    A, B = "x:%d" % a, "x:%d" % b
    for name, f in (("x_add", N.x_add), ("x_sub", N.x_sub), ("x_mul", N.x_mul), ("x_div", N.x_div)):
        emit(name, [A, B], lambda f=f: "x:%d" % f(a, b))
for a, b in fpairs[:40]:
    emit("x_max", ["x:%d" % a, "x:%d" % b], lambda: "x:%d" % N.x_max(a, b))
    emit("x_min", ["x:%d" % a, "x:%d" % b], lambda: "x:%d" % N.x_min(a, b))

# ---- Float
F = N.f_from_bits
FLOATS = [0.0, -0.0, 1.0, -1.0, 0.1, -0.1, 1.0 / 3, 0.5, 1.5, 2.5, -2.5, 3.5, -0.5, 2.0 ** 53, 2.0 ** 53 + 2,
          2.0 ** 63, -(2.0 ** 63), 9223372036854774784.0, F(0x1), F(0x000FFFFFFFFFFFFF), F(0x0010000000000000),
          F(0x7FEFFFFFFFFFFFFF), float("inf"), float("-inf"), F(0x7FF8000000000000), F(0xFFF8000000000000),
          F(0x7FF0000000000001), F(0x7FF4000000000000), 1e300, 1e-300, 123456.789, 4294967296.0,
          2.0 ** -32, 3 * 2.0 ** -33, 2.0 ** 31, -(2.0 ** 31) - 0.5, 1.0e16, 0.3, 7.0, 49.0, 2.0]


def rfloat():
    c = rng.random()
    if c < 0.6:
        return F(rng.getrandbits(64))
    if c < 0.9:
        return rng.uniform(-1e6, 1e6)
    return float(rng.randint(-1000, 1000)) / rng.choice([1, 2, 4, 8, 3, 10])


floats = FLOATS + [rfloat() for _ in range(120)]
for x in floats:
    X = fb(x)
    emit("f_neg", [X], lambda: fb(N.f_neg(x)))
    emit("f_abs", [X], lambda: fb(N.f_abs(x)))
    emit("f_sqrt", [X], lambda: fb(N.f_sqrt(x)))
    emit("f_trunc", [X], lambda: "i:%d" % N.f_trunc(x))
    emit("f_round", [X], lambda: "i:%d" % N.f_round(x))
    emit("fmt_f", [X], lambda: "s:" + N.fmt_f(x))
    for rd in (0, 1):
        emit("f_to_x", [X, "b:%d" % rd], lambda rd=rd: "x:%d" % N.f_to_x(x, bool(rd)))
fl_pairs = [(a, b) for a in FLOATS[:26] for b in FLOATS[:26]] + [(rfloat(), rfloat()) for _ in range(400)]
for a, b in fl_pairs:
    A, B = fb(a), fb(b)
    for name, f in (("f_add", N.f_add), ("f_sub", N.f_sub), ("f_mul", N.f_mul), ("f_div", N.f_div),
                    ("f_max", N.f_max), ("f_min", N.f_min)):
        emit(name, [A, B], lambda f=f: fb(f(a, b)))
    emit("f_lt", [A, B], lambda: "b:%d" % (a < b))
    emit("f_eq", [A, B], lambda: "b:%d" % (a == b))
for n in ints:
    for rd in (0, 1):
        emit("f_from_i", ["i:%d" % n, "b:%d" % rd], lambda rd=rd: fb(N.f_from_i(n, bool(rd))))

# ---- printing
for n in ints:
    emit("fmt_i", ["i:%d" % n], lambda: "s:" + N.fmt_i(n))
for a in fix:
    emit("fmt_x", ["x:%d" % a], lambda: "s:" + N.fmt_x(a))

# ---- SHA-256
for msg in [b"", b"abc", b"a" * 55, b"a" * 56, b"a" * 64, b"a" * 119, b"a" * 1000,
            bytes(range(256)), "Ørlǫg lays down law".encode("utf-8")]:
    out.append("sha256 hex:%s => hex:%s" % (msg.hex(), hashlib.sha256(msg).hexdigest()))

body = "\n".join(out) + "\n"
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vectors")
os.makedirs(dst, exist_ok=True)
with open(os.path.join(dst, "runtime-vectors.txt"), "wb") as fh:
    fh.write(body.encode("ascii"))
print("vectors:", len(out), "sha256:", hashlib.sha256(body.encode("ascii")).hexdigest())

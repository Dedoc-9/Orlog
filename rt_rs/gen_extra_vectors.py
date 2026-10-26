"""Extra differential vectors for the Rust runtime, from numeric_ref, in the official line format.

usage: python -B gen_extra_vectors.py OUT [SEED]

Not the conformance vectors (vectors/runtime-vectors.txt is the contract and is never edited); a
denser random sample of the same operations, weighted toward the hard parts: subnormal and huge
floats for exact printing, values near rounding ties, conversions at their limits. The harness
reads it unchanged: test_rt OUT.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from orlog import numeric_ref as N  # noqa: E402

out_path = sys.argv[1]
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
out = []
F = N.f_from_bits


def fb(x):
    return "f:%016X" % N.f_bits(x)


def emit(op, args, fn):
    try:
        r = fn()
    except N.Refusal as e:
        out.append("%s %s => !%s" % (op, " ".join(args), e.code))
        return
    out.append("%s %s => %s" % (op, " ".join(args), r))


def rbits():
    """Random binary64 bits, every exponent region represented."""
    c = rng.random()
    sign = rng.getrandbits(1) << 63
    if c < 0.25:
        return sign | rng.getrandbits(52)                                  # subnormal
    if c < 0.35:
        return sign | (rng.randrange(2046 - 60, 2047) << 52) | rng.getrandbits(52)   # huge
    if c < 0.75:
        return sign | (rng.randrange(1023 - 70, 1023 + 70) << 52) | rng.getrandbits(52)  # near 1
    if c < 0.8:
        return sign | (0x7FF << 52) | rng.getrandbits(52)                  # inf / NaN
    return rng.getrandbits(64)


def rint():
    k = rng.choice([1, 2, 8, 20, 31, 32, 33, 52, 53, 54, 62, 63, 64])
    v = rng.getrandbits(k)
    if k == 64:
        v -= 1 << 63
    elif rng.random() < 0.5:
        v = -v
    return max(N.I64_MIN, min(N.I64_MAX, v))


def rtie():
    """A Fix raw near a rounding tie of x_mul/x_round."""
    base = rint() & ~0xFFFFFFFF
    return max(N.I64_MIN, min(N.I64_MAX, base + rng.choice([0x7FFFFFFF, 0x80000000, 0x80000001, 0, 1])))


for _ in range(6000):
    x = F(rbits())
    X = fb(x)
    emit("fmt_f", [X], lambda: "s:" + N.fmt_f(x))
    emit("f_trunc", [X], lambda: "i:%d" % N.f_trunc(x))
    emit("f_round", [X], lambda: "i:%d" % N.f_round(x))
    emit("f_sqrt", [X], lambda: fb(N.f_sqrt(x)))
    emit("f_neg", [X], lambda: fb(N.f_neg(x)))
    emit("f_abs", [X], lambda: fb(N.f_abs(x)))
    for rd in (0, 1):
        emit("f_to_x", [X, "b:%d" % rd], lambda rd=rd: "x:%d" % N.f_to_x(x, bool(rd)))
# floats that f_to_x / f_round meet at their limits: k / 2^s near 2^31 and near ties
for _ in range(3000):
    s = rng.randrange(0, 60)
    m = rng.getrandbits(53)
    x = m / (1 << s) if rng.random() < 0.5 else -(m / (1 << s))
    X = fb(x)
    emit("f_round", [X], lambda: "i:%d" % N.f_round(x))
    for rd in (0, 1):
        emit("f_to_x", [X, "b:%d" % rd], lambda rd=rd: "x:%d" % N.f_to_x(x, bool(rd)))
for _ in range(4000):
    a, b = F(rbits()), F(rbits())
    A, B = fb(a), fb(b)
    for name, f in (("f_add", N.f_add), ("f_sub", N.f_sub), ("f_mul", N.f_mul), ("f_div", N.f_div),
                    ("f_max", N.f_max), ("f_min", N.f_min)):
        emit(name, [A, B], lambda f=f: fb(f(a, b)))
for _ in range(5000):
    a = rint() if rng.random() < 0.7 else rtie()
    A = "x:%d" % a
    emit("fmt_x", [A], lambda: "s:" + N.fmt_x(a))
    emit("x_sqrt", [A], lambda: "x:%d" % N.x_sqrt(a))
    emit("x_round", [A], lambda: "i:%d" % N.x_round(a))
    emit("x_trunc", [A], lambda: "i:%d" % N.x_trunc(a))
    for rd in (0, 1):
        emit("x_to_f", [A, "b:%d" % rd], lambda rd=rd: fb(N.x_to_f(a, bool(rd))))
    n = rint()
    emit("i_isqrt", ["i:%d" % n], lambda: "i:%d" % N.i_isqrt(n))
    emit("fmt_i", ["i:%d" % n], lambda: "s:" + N.fmt_i(n))
    for rd in (0, 1):
        emit("f_from_i", ["i:%d" % n, "b:%d" % rd], lambda rd=rd: fb(N.f_from_i(n, bool(rd))))
for _ in range(6000):
    a = rint() if rng.random() < 0.7 else rtie()
    b = rint() if rng.random() < 0.8 else rng.choice([1, -1, 2, -2, 3, 1 << 32, -(1 << 32), N.I64_MIN, 0])
    A, B = "x:%d" % a, "x:%d" % b
    for name, f in (("x_add", N.x_add), ("x_sub", N.x_sub), ("x_mul", N.x_mul), ("x_div", N.x_div)):
        emit(name, [A, B], lambda f=f: "x:%d" % f(a, b))
    A, B = "i:%d" % a, "i:%d" % b
    for name, f in (("i_add", N.i_add), ("i_sub", N.i_sub), ("i_mul", N.i_mul), ("i_div", N.i_div),
                    ("i_quot", N.i_quot), ("i_rem", N.i_rem)):
        emit(name, [A, B], lambda f=f: "i:%d" % f(a, b))
# exact divisions, so that i_div's quotient path (not only its refusals) is sampled
for _ in range(2000):
    b = rint() or 1
    q = rint() >> rng.randrange(0, 64)
    a = q * b
    if N.I64_MIN <= a <= N.I64_MAX:
        emit("i_div", ["i:%d" % a, "i:%d" % b], lambda: "i:%d" % N.i_div(a, b))

with open(out_path, "wb") as fh:
    fh.write(("\n".join(out) + "\n").encode("utf-8"))
print("extra vectors:", len(out))

"""RUST-CORE-0: supplementary vectors for `as an integer` (x_as_i, f_as_i), the owner's ruling A2(a) of 2026-10-30.

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_as_int_vectors.py

It writes research/rust-core/vectors-as-integer.txt in the contract file's line grammar, and its provenance in
research/rust-core/vectors-as-integer.manifest. The contract file, vectors/runtime-vectors.txt, is not read and not
touched. These vectors are supplementary test evidence, not a change to the version-0 contract (his condition 5). The
core's author receives the vector file, never this script or numeric_ref.py (his condition 4).

Line grammar, as src/gen_vectors.py writes the contract file: `<op> <arg> ... => <result>`, with:
- `x:<raw int>` for a Fix;
- `f:<16 uppercase hex digits, the binary64 bits>` for a Float;
- `i:<int>` for an Int;
- `!CODE` for a refusal."""
import hashlib
import os
import random
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog import numeric_ref as N   # noqa: E402

SEED = 20261030
OUT = os.path.join(HERE, "vectors-as-integer.txt")
MANIFEST = os.path.join(HERE, "vectors-as-integer.manifest")


def fbits(x):
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def ffrom(b):
    return struct.unpack("<d", struct.pack("<Q", b))[0]


def line(op, arg, fn):
    try:
        r = "i:%d" % fn()
    except N.Refusal as e:
        r = "!%s" % e.code
    return "%s %s => %s" % (op, arg, r)


def main():
    rng = random.Random(SEED)
    one = N.ONE
    out = []
    # x_as_i: a Fix's raw value, exact when its 32 fraction bits are zero
    raws = [0, 1, -1, one, -one, one + 1, -one - 1, one // 2, -(one // 2), 3 * one, -3 * one, N.I64_MAX, N.I64_MIN,
            ((1 << 31) - 1) * one, -(1 << 31) * one, ((1 << 31) - 1) * one + 1, N.I64_MIN + 1, one - 1, -(one - 1)]
    for _ in range(80):
        k = rng.randrange(-(1 << 31), 1 << 31)
        raws.append(k * one)
        raws.append(k * one + rng.randrange(1, one))
    seen = set()
    for a in raws:
        if a in seen or not (N.I64_MIN <= a <= N.I64_MAX):
            continue
        seen.add(a)
        out.append(line("x_as_i", "x:%d" % a, lambda a=a: N.x_as_i(a)))
    # f_as_i: NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW
    floats = [0.0, -0.0, 1.0, -1.0, 0.5, -0.5, 1.5, -2.5, 2.0 ** 52 + 0.5, 2.0 ** 53, -(2.0 ** 53), 2.0 ** 62,
              2.0 ** 63, -(2.0 ** 63), 2.0 ** 63 - 1024.0, -(2.0 ** 63) - 2048.0, 1e300, -1e300, 5e-324, -5e-324,
              2.2250738585072014e-308, float("inf"), float("-inf"), 1.7976931348623157e308]
    nans = [0x7FF8000000000000, 0xFFF8000000000000, 0x7FF0000000000001, 0x7FF4000000000000]
    for _ in range(80):
        k = rng.randrange(-(1 << 62), 1 << 62)
        floats.append(float(k))
        floats.append(rng.uniform(-1e18, 1e18))
        floats.append(ffrom(rng.getrandbits(64)))
    bits_seen = set()
    for b in [fbits(x) for x in floats] + nans:
        if b in bits_seen:
            continue
        bits_seen.add(b)
        x = ffrom(b)
        out.append(line("f_as_i", "f:%016X" % b, lambda x=x: N.f_as_i(x)))
    data = ("\n".join(out) + "\n").encode("ascii")
    with open(OUT, "wb") as f:
        f.write(data)

    def sha(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    refusals = sum(1 for ln in out if "=> !" in ln)
    manifest = [
        "vectors-as-integer.txt: supplementary vectors for `as an integer` (RUST-CORE-0, the owner's ruling A2(a), 2026-10-30)",
        "status: supplementary test evidence; not a change to the version-0 contract nor to the reference's authority",
        "command: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_as_int_vectors.py",
        "generator: research/rust-core/gen_as_int_vectors.py sha256 %s" % sha(os.path.abspath(__file__)),
        "numeric reference: src/orlog/numeric_ref.py sha256 %s (x_as_i, f_as_i)" % sha(os.path.join(ROOT, "src", "orlog", "numeric_ref.py")),
        "seed: %d (random.Random)" % SEED,
        "output: vectors-as-integer.txt sha256 %s; %d lines: x_as_i %d, f_as_i %d; %d of them refusals" % (
            hashlib.sha256(data).hexdigest(), len(out), sum(1 for ln in out if ln.startswith("x_as_i")),
            sum(1 for ln in out if ln.startswith("f_as_i")), refusals),
        "codes: %s" % ", ".join("%s %d" % (c, sum(1 for ln in out if ln.endswith("!" + c)))
                                for c in ("NOT-FINITE", "INEXACT-CONVERSION", "OVERFLOW")),
        "contract file: vectors/runtime-vectors.txt, not read, not changed",
    ]
    with open(MANIFEST, "wb") as f:
        f.write(("\n".join(manifest) + "\n").encode("ascii"))
    print("\n".join(manifest))


if __name__ == "__main__":
    main()

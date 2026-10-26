"""Check the conformance vectors against witnesses that numeric_ref did not compute.

  PYTHONHASHSEED=0 python -B tests/vectors_independent.py [--vectors PATH]

numeric_ref.py generated every line of vectors/runtime-vectors.txt, and both runtimes were made to reproduce those
lines. So far the vectors have defined the semantics without being checked against anything else. This script holds
them to three witnesses, reported side by side; no one of them is the verdict alone:

1. **The derivation** (tests/numeric_oracle.py). Every line is derived again, by a different method, from RUNTIME-SPEC
   sections 2 and 3 and IEEE 754, and compared byte for byte. Then numeric_ref, as it runs now, is compared with the
   derivation on the same arguments.
2. **The hand table** below. Each case's expected value was worked by hand, with its working beside it, and was
   written down rather than computed by any program. Each case is compared with the derivation, with numeric_ref, and
   with the vectors where they hold that case.
3. **Published digests.** SHA-256 of the empty message and of "abc", as NIST publishes them.

**Plants.** The check fails unless every plant is caught:
- a vector line corrupted;
- numeric_ref rounding half away from zero;
- numeric_ref keeping a NaN's payload;
- numeric_ref taking C's truncated remainder;
- the derivation's import fence breached.

The three numeric_ref plants are the point: they are mistakes that numeric_ref and vectors regenerated from it would
share, which no comparison between the two can find.
"""
import argparse
import ast
import hashlib
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
from orlog import numeric_ref as N  # noqa: E402  (the system under test, never a source of expected values)
import numeric_oracle as O  # noqa: E402

I64_MIN, I64_MAX = -(1 << 63), (1 << 63) - 1
HALF, ONE = 1 << 31, 1 << 32          # inputs only: raw Fix 0.5 and 1.0

# (op, arguments in the vectors' notation, the expected result written by hand, the working)
HAND = [
    # ---- Int: Euclidean quotient and remainder (SPEC section 8), exact division, the edges of i64
    ("i_quot", "i:-7 i:2", "i:-4", "-7 = 2*(-4) + 1 with 0 <= 1 < 2 (C's / gives -3)"),
    ("i_rem", "i:-7 i:2", "i:1", "the same division: r = -7 - 2*(-4) = 1 (C's % gives -1)"),
    ("i_quot", "i:7 i:-2", "i:-3", "7 = (-2)*(-3) + 1, 0 <= 1 < 2"),
    ("i_rem", "i:7 i:-2", "i:1", "the same division"),
    ("i_quot", "i:-7 i:-2", "i:4", "-7 = (-2)*4 + 1, 0 <= 1 < 2"),
    ("i_rem", "i:-7 i:-2", "i:1", "the same division"),
    ("i_quot", "i:%d i:-1" % I64_MIN, "!OVERFLOW", "q = 2^63, one past the largest Int"),
    ("i_rem", "i:%d i:-1" % I64_MIN, "i:0", "r = 0: the remainder exists where the quotient overflows"),
    ("i_div", "i:7 i:2", "!INEXACT-DIVISION", "7/2 = 3.5 is not an integer"),
    ("i_div", "i:-10 i:2", "i:-5", "exact"),
    ("i_div", "i:255 i:0", "!DIVISION-BY-ZERO", "a zero divisor, tested first"),
    ("i_div", "i:%d i:-1" % I64_MIN, "!OVERFLOW", "-2^63 / -1 = 2^63: exact, and out of range"),
    ("i_add", "i:%d i:1" % I64_MAX, "!OVERFLOW", "(2^63 - 1) + 1 = 2^63"),
    ("i_neg", "i:%d" % I64_MIN, "!OVERFLOW", "-(-2^63) = 2^63"),
    ("i_abs", "i:%d" % I64_MIN, "!OVERFLOW", "|-2^63| = 2^63"),
    ("i_isqrt", "i:%d" % I64_MAX, "i:3037000499",
     "3037000499^2 = 9223372030926249001 <= 2^63 - 1 < 3037000500^2 = 9223372037000250000"),
    ("i_isqrt", "i:-1", "!NEGATIVE-SQRT", "a negative argument"),
    ("i_mul", "i:3037000500 i:3037000500", "!OVERFLOW", "9223372037000250000 > 9223372036854775807"),
    ("i_mul", "i:3037000499 i:3037000499", "i:9223372030926249001", "the square worked above, in range"),
    # ---- Fix (raw r stands for r / 2^32): half-even at every tie, both signs
    ("x_mul", "x:%d x:1" % (3 * HALF), "x:2", "1.5 times raw 1 is 1.5 raw units: a tie between 1 and 2; even is 2"),
    ("x_mul", "x:%d x:1" % (5 * HALF), "x:2", "2.5 raw units: a tie between 2 and 3; even is 2"),
    ("x_mul", "x:%d x:1" % (-3 * HALF), "x:-2", "-1.5 raw units: a tie between -2 and -1; even is -2"),
    ("x_mul", "x:%d x:-1" % (5 * HALF), "x:-2", "-2.5 raw units: a tie between -3 and -2; even is -2"),
    ("x_mul", "x:1 x:%d" % HALF, "x:0", "raw 1 times 0.5: half a raw unit, a tie between 0 and 1; even is 0"),
    ("x_mul", "x:-1 x:%d" % HALF, "x:0", "minus half a raw unit: a tie between -1 and 0; even is 0"),
    ("x_mul", "x:%d x:%d" % (3 * HALF, HALF), "x:3221225472", "1.5 * 0.5 = 0.75 exactly, and 0.75 * 2^32 = 3221225472"),
    ("x_mul", "x:%d x:%d" % (I64_MAX, 2 * ONE), "!OVERFLOW", "the largest Fix times 2"),
    ("x_div", "x:%d x:%d" % (ONE, 3 * ONE), "x:1431655765", "1/3: 2^32/3 = 1431655765.33..., to 1431655765"),
    ("x_div", "x:%d x:%d" % (2 * ONE, 3 * ONE), "x:2863311531", "2/3: 2^33/3 = 2863311530.66..., to 2863311531"),
    ("x_div", "x:%d x:%d" % (-ONE, 3 * ONE), "x:-1431655765", "-1/3: the rounding is symmetric"),
    ("x_div", "x:1 x:%d" % (3 * ONE), "x:0", "raw 1 divided by 3: a third of a raw unit, to 0"),
    ("x_div", "x:%d x:%d" % (I64_MAX, 2 * ONE), "x:4611686018427387904",
     "(2^63 - 1)/2 = 4611686018427387903.5: a tie; 4611686018427387903 is odd, so 2^62"),
    ("x_div", "x:%d x:%d" % (I64_MIN + 1, 2 * ONE), "x:-4611686018427387904", "the same tie, negative"),
    ("x_div", "x:%d x:0" % ONE, "!DIVISION-BY-ZERO", "a zero divisor"),
    ("x_div", "x:%d x:%d" % (I64_MAX, HALF), "!OVERFLOW", "the largest Fix divided by 0.5"),
    ("x_from_i", "i:%d" % HALF, "!OVERFLOW", "2^31 * 2^32 = 2^63"),
    ("x_from_i", "i:%d" % -HALF, "x:-9223372036854775808", "-2^31 * 2^32 = -2^63, the smallest raw value"),
    ("x_from_i", "i:%d" % (HALF - 1), "x:9223372032559808512", "(2^31 - 1) * 2^32 = 2^63 - 2^32"),
    ("x_sqrt", "x:%d" % (2 * ONE), "x:6074000999",
     "isqrt(2^33 * 2^32) = isqrt(2^65): 6074000999^2 = 36893488135852998001 <= 2^65 = 36893488147419103232 "
     "< 6074001000^2 = 36893488148001000000"),
    ("x_sqrt", "x:-1", "!NEGATIVE-SQRT", "a negative argument"),
    ("x_round", "x:%d" % (3 * HALF), "i:2", "1.5 to even: 2"),
    ("x_round", "x:%d" % (5 * HALF), "i:2", "2.5 to even: 2"),
    ("x_round", "x:%d" % (-3 * HALF), "i:-2", "-1.5 to even: -2"),
    ("x_round", "x:%d" % -HALF, "i:0", "-0.5 to even: 0"),
    ("x_round", "x:%d" % HALF, "i:0", "0.5 to even: 0"),
    ("x_trunc", "x:%d" % (-3 * HALF), "i:-1", "-1.5 toward zero: -1"),
    ("x_trunc", "x:-1", "i:0", "-2^-32 toward zero: 0"),
    # ---- Float, by bits: rounding ties, overflow, subnormals, signed zeros, NaN
    ("f_add", "f:3FB999999999999A f:3FC999999999999A", "f:3FD3333333333334",
     "0.1 = 7205759403792794 * 2^-56 and 0.2 = 14411518807585588 * 2^-56; the sum is 21617278211378382 * 2^-56 = "
     "5404319552844595.5 units of 2^-54: a tie; the even significand 5404319552844596 is 0x13333333333334"),
    ("f_add", "f:3FF0000000000000 f:3CA0000000000000", "f:3FF0000000000000",
     "1 + 2^-53 lies halfway between 1 (even significand) and 1 + 2^-52 (odd): 1"),
    ("f_add", "f:3FF0000000000000 f:3CB8000000000000", "f:3FF0000000000002",
     "1 + 3*2^-53 is 1.5 ulps above 1: a tie between significands ...1 and ...2; even is ...2"),
    ("f_add", "f:7FEFFFFFFFFFFFFF f:7FEFFFFFFFFFFFFF", "f:7FF0000000000000",
     "2 * MAX = (2^53 - 1) * 2^972 is representable only with an exponent past the largest: +inf"),
    ("f_add", "f:7FEFFFFFFFFFFFFF f:7C90000000000000", "f:7FF0000000000000",
     "MAX + 2^970 lies halfway between MAX (odd significand) and 2^1024: the tie goes to even, past the largest "
     "finite value: +inf"),
    ("f_add", "f:7FEFFFFFFFFFFFFF f:3FF0000000000000", "f:7FEFFFFFFFFFFFFF", "1 is far below half an ulp of MAX"),
    ("f_div", "f:3FF0000000000000 f:4008000000000000", "f:3FD5555555555555",
     "1/3 lies in [1/4, 1/2), ulp 2^-54: 2^54/3 = 6004799503160661.33..., to 6004799503160661 = 0x15555555555555"),
    ("f_div", "f:3FF0000000000000 f:0000000000000000", "f:7FF0000000000000", "1 / +0 = +inf"),
    ("f_div", "f:3FF0000000000000 f:8000000000000000", "f:FFF0000000000000", "1 / -0 = -inf"),
    ("f_div", "f:BFF0000000000000 f:0000000000000000", "f:FFF0000000000000", "-1 / +0 = -inf"),
    ("f_div", "f:0000000000000000 f:0000000000000000", "f:7FF8000000000000", "0/0 is NaN, written canonically"),
    ("f_mul", "f:0000000000000001 f:3FE0000000000000", "f:0000000000000000",
     "2^-1074 * 0.5 = 2^-1075, halfway between 0 and 2^-1074: even is 0"),
    ("f_mul", "f:0000000000000001 f:3FF8000000000000", "f:0000000000000002",
     "1.5 * 2^-1074: halfway between 1 and 2 steps of 2^-1074; even is 2"),
    ("f_mul", "f:8000000000000001 f:3FE0000000000000", "f:8000000000000000",
     "-2^-1075 rounds to a zero of its own sign: -0"),
    ("f_sqrt", "f:4000000000000000", "f:3FF6A09E667F3BCD",
     "sqrt(2) = 0x1.6A09E667F3BCC908... (the first 64 fraction bits are SHA-512's initial H0, 0x6a09e667f3bcc908); "
     "after 52 bits come 0x908..., more than half: up to 0x1.6A09E667F3BCD"),
    ("f_sqrt", "f:8000000000000000", "f:8000000000000000", "sqrt(-0) = -0"),
    ("f_sqrt", "f:BFF0000000000000", "f:7FF8000000000000", "sqrt(-1) is NaN, written canonically"),
    ("f_sqrt", "f:7FF0000000000000", "f:7FF0000000000000", "sqrt(+inf) = +inf"),
    ("f_neg", "f:FFF8000000000000", "f:7FF8000000000000", "a NaN in, the canonical NaN out"),
    ("f_neg", "f:7FF8000000000000", "f:7FF8000000000000",
     "negation flips the sign bit to 0xFFF8...; the semantics writes every NaN as 0x7FF8..."),
    ("f_add", "f:FFF8000000000000 f:3FF0000000000000", "f:7FF8000000000000",
     "a NaN operand gives a NaN, written canonically whatever the operand's sign or payload"),
    ("f_mul", "f:7FF0000000000000 f:0000000000000000", "f:7FF8000000000000",
     "infinity times zero is invalid: a NaN, written canonically (x86-64's default NaN is 0xFFF8...)"),
    ("f_neg", "f:0000000000000000", "f:8000000000000000", "-(+0) = -0: the sign bit flips"),
    ("f_max", "f:8000000000000000 f:0000000000000000", "f:0000000000000000", "-0 > +0 is false, so b: +0"),
    ("f_max", "f:0000000000000000 f:8000000000000000", "f:8000000000000000", "+0 > -0 is false, so b: -0"),
    ("f_max", "f:FFF8000000000000 f:3FF0000000000000", "f:3FF0000000000000", "NaN > 1 is false, so b: 1"),
    ("f_max", "f:3FF0000000000000 f:FFF8000000000000", "f:FFF8000000000000",
     "1 > NaN is false, so b: the NaN as given, not canonicalized"),
    ("f_lt", "f:7FF8000000000000 f:3FF0000000000000", "b:0", "NaN is unordered"),
    ("f_eq", "f:7FF8000000000000 f:7FF8000000000000", "b:0", "NaN equals nothing, itself included"),
    ("f_eq", "f:0000000000000000 f:8000000000000000", "b:1", "+0 = -0"),
    ("f_lt", "f:8000000000000000 f:0000000000000000", "b:0", "-0 < +0 is false"),
    ("f_round", "f:4004000000000000", "i:2", "2.5 to even: 2"),
    ("f_round", "f:C004000000000000", "i:-2", "-2.5 to even: -2"),
    ("f_round", "f:400C000000000000", "i:4", "3.5 to even: 4"),
    ("f_round", "f:3FE0000000000000", "i:0", "0.5 to even: 0"),
    ("f_round", "f:BFE0000000000000", "i:0", "-0.5 to even: 0"),
    ("f_trunc", "f:C004000000000000", "i:-2", "-2.5 toward zero: -2"),
    ("f_round", "f:7FF0000000000000", "!NOT-FINITE", "+inf"),
    ("f_trunc", "f:43E0000000000000", "!OVERFLOW", "2^63 is one past the largest Int"),
    ("f_trunc", "f:C3E0000000000000", "i:-9223372036854775808", "-2^63 is the smallest Int"),
    ("f_trunc", "f:43DFFFFFFFFFFFFF", "i:9223372036854774784", "the largest double below 2^63 is 2^63 - 1024"),
    ("f_from_i", "i:9007199254740993 b:0", "!INEXACT-CONVERSION", "2^53 + 1 needs 54 significant bits"),
    ("f_from_i", "i:9007199254740993 b:1", "f:4340000000000000",
     "2^53 + 1 lies halfway between 2^53 (even significand) and 2^53 + 2: 2^53"),
    ("f_from_i", "i:-9007199254740993 b:1", "f:C340000000000000", "the same tie, negative: -2^53"),
    ("f_from_i", "i:%d b:1" % I64_MAX, "f:43E0000000000000", "2^63 - 1 is 1 from 2^63 and 1023 from 2^63 - 1024: 2^63"),
    ("f_from_i", "i:%d b:0" % I64_MAX, "!INEXACT-CONVERSION", "2^63 - 1 needs 63 significant bits"),
    ("f_to_x", "f:3FE0000000000000 b:0", "x:2147483648", "0.5 * 2^32 = 2^31"),
    ("f_to_x", "f:3DF8000000000000 b:0", "!INEXACT-CONVERSION", "3*2^-33 * 2^32 = 1.5"),
    ("f_to_x", "f:3DF8000000000000 b:1", "x:2", "1.5 to even: 2"),
    ("f_to_x", "f:3DF0000000000000 b:0", "x:1", "2^-32 * 2^32 = 1"),
    ("f_to_x", "f:41E0000000000000 b:0", "!OVERFLOW", "2^31 * 2^32 = 2^63"),
    ("f_to_x", "f:7FF8000000000000 b:0", "!NOT-FINITE", "NaN"),
    ("x_to_f", "x:1 b:0", "f:3DF0000000000000", "raw 1 is exactly 2^-32: exponent -32, biased 991 = 0x3DF"),
    ("x_to_f", "x:%d b:0" % I64_MAX, "!INEXACT-CONVERSION", "(2^63 - 1)/2^32 needs 63 significant bits"),
    ("x_to_f", "x:%d b:1" % I64_MAX, "f:41E0000000000000",
     "2^31 - 2^-32 is 2^-32 below 2^31 and 2^-22 - 2^-32 above the double below 2^31: 2^31"),
    # ---- printing: exact decimals (RUNTIME-SPEC section 3)
    ("fmt_f", "f:3FB999999999999A", "s:0.1000000000000000055511151231257827021181583404541015625",
     "0.1 as a double is 7205759403792794 * 2^-56: its 56 decimals, trailing zeros removed"),
    ("fmt_f", "f:8000000000000000", "s:-0.0", "the sign bit decides"),
    ("fmt_f", "f:FFF8000000000000", "s:NaN", "a NaN prints NaN, whatever its sign bit"),
    ("fmt_f", "f:FFF0000000000000", "s:-Infinity", "negative infinity"),
    ("fmt_f", "f:4340000000000000", "s:9007199254740992.0", "2^53 is integral: '.0'"),
    ("fmt_x", "x:1", "s:0.00000000023283064365386962890625",
     "2^-32 = 5^32 / 10^32, and 5^32 = 23283064365386962890625 has 23 digits: 9 zeros come first"),
    ("fmt_x", "x:%d" % I64_MAX, "s:2147483647.99999999976716935634613037109375", "2^31 - 1, then 1 - 2^-32"),
    ("fmt_x", "x:%d" % I64_MIN, "s:-2147483648.0", "-2^31, integral"),
    ("fmt_x", "x:0", "s:0.0", "zero"),
    ("fmt_x", "x:%d" % (-3 * HALF), "s:-1.5", "-1.5"),
    ("fmt_i", "i:%d" % I64_MIN, "s:-9223372036854775808", "INT64_MIN, printed whole"),
]

# The smallest subnormal prints 1074 fraction digits. Not written out: what was worked by hand is that
# 2^-1074 = 5^1074 / 10^1074, that 5^1074 has floor(1074 * log10 5) + 1 = 751 digits (so 323 zeros come first),
# that its leading digits are those of 4.9406564584124654e-324, and that its last digit is 5.
SUBNORMAL = ("fmt_f", "f:0000000000000001")


def subnormal_ok(s):
    if not s.startswith("s:0."):
        return False
    frac = s[4:]
    return len(frac) == 1074 and frac[:323] == "0" * 323 and frac[323:340] == "49406564584124654" and frac[-1] == "5"


# Published digests (NIST: FIPS 180-2 Appendix B.1 for "abc"; the CAVP short-message vectors for the empty message)
DIGESTS = [
    ("sha256", "hex:", "hex:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("sha256", "hex:616263", "hex:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
]


# ------------------------------------------------------------------------------------------------ numeric_ref
def _ref_table():
    """numeric_ref called on decoded arguments, its result written in the vectors' notation. The module is looked up
    at call time, so a plant patched into numeric_ref is what runs."""
    F = N.f_from_bits

    def f(x): return "f:%016X" % N.f_bits(x)
    t = {}
    for name in ("i_add", "i_sub", "i_mul", "i_div", "i_quot", "i_rem", "i_max", "i_min"):
        t[name] = (lambda nm: lambda a, b: "i:%d" % getattr(N, nm)(a, b))(name)
    for name in ("i_neg", "i_abs", "i_isqrt"):
        t[name] = (lambda nm: lambda a: "i:%d" % getattr(N, nm)(a))(name)
    for name in ("x_add", "x_sub", "x_mul", "x_div", "x_max", "x_min"):
        t[name] = (lambda nm: lambda a, b: "x:%d" % getattr(N, nm)(a, b))(name)
    for name in ("x_neg", "x_abs", "x_sqrt", "x_from_i"):
        t[name] = (lambda nm: lambda a: "x:%d" % getattr(N, nm)(a))(name)
    for name in ("x_trunc", "x_round"):
        t[name] = (lambda nm: lambda a: "i:%d" % getattr(N, nm)(a))(name)
    for name in ("f_add", "f_sub", "f_mul", "f_div", "f_max", "f_min"):
        t[name] = (lambda nm: lambda a, b: f(getattr(N, nm)(F(a), F(b))))(name)
    for name in ("f_neg", "f_abs", "f_sqrt"):
        t[name] = (lambda nm: lambda a: f(getattr(N, nm)(F(a))))(name)
    for name in ("f_trunc", "f_round"):
        t[name] = (lambda nm: lambda a: "i:%d" % getattr(N, nm)(F(a)))(name)
    t["f_lt"] = lambda a, b: "b:%d" % (F(a) < F(b))          # the native comparisons (RUNTIME-SPEC section 2)
    t["f_eq"] = lambda a, b: "b:%d" % (F(a) == F(b))
    t["x_to_f"] = lambda a, rd: f(N.x_to_f(a, rd))
    t["f_to_x"] = lambda x, rd: "x:%d" % N.f_to_x(F(x), rd)
    t["f_from_i"] = lambda n, rd: f(N.f_from_i(n, rd))
    t["fmt_i"] = lambda n: "s:" + N.fmt_i(n)
    t["fmt_x"] = lambda a: "s:" + N.fmt_x(a)
    t["fmt_f"] = lambda x: "s:" + N.fmt_f(F(x))
    return t


REF = _ref_table()


def reference(op, args):
    try:
        return REF[op](*[O.parse_arg(a) for a in args])
    except N.Refusal as e:
        return "!" + e.code


# ------------------------------------------------------------------------------------------------ the witnesses
def read_vectors(path):
    rows = []
    with open(path, "rb") as fh:
        for k, raw in enumerate(fh.read().decode("ascii").split("\n"), 1):
            if not raw:
                continue
            left, result = raw.split(" => ", 1)
            parts = left.split(" ")
            rows.append((k, parts[0], tuple(parts[1:]), result))
    return rows


def check_file(rows):
    """Every line against the derivation. Returns (mismatches, per-op counts, lines not derived)."""
    bad, per_op, skipped = [], {}, []
    for k, op, args, result in rows:
        if op not in O.OPS:
            skipped.append((k, op))
            continue
        per_op[op] = per_op.get(op, 0) + 1
        got = O.derive(op, args)
        if got != result:
            bad.append((k, op, args, result, got))
    return bad, per_op, skipped


def check_reference(rows):
    """numeric_ref against the derivation, on every line's arguments."""
    bad = []
    for k, op, args, _ in rows:
        if op in O.OPS:
            want, got = O.derive(op, args), reference(op, args)
            if want != got:
                bad.append((k, op, args, want, got))
    return bad


def check_hand(index):
    """Each hand case against the derivation, numeric_ref and the vectors. Returns (failures, cases in the vectors)."""
    fails, present = [], 0
    for op, argstr, want, why in HAND:
        args = tuple(argstr.split(" "))
        for who, got in (("derivation", O.derive(op, args)), ("numeric_ref", reference(op, args))):
            if got != want:
                fails.append((op, argstr, who, want, got, why))
        if (op, args) in index:
            present += 1
            if index[(op, args)] != want:
                fails.append((op, argstr, "the vectors", want, index[(op, args)], why))
    op, argstr = SUBNORMAL
    for who, got in (("derivation", O.derive(op, (argstr,))), ("numeric_ref", reference(op, (argstr,))),
                     ("the vectors", index.get((op, (argstr,)), "absent"))):
        if not subnormal_ok(got):
            fails.append((op, argstr, who, "1074 digits, 323 zeros, 49406564584124654..., last 5", got[:60], ""))
    for op, argstr, want in DIGESTS:
        got = index.get((op, (argstr,)), "absent")
        if got != want:
            fails.append((op, argstr, "the vectors", want, got, "published digest"))
    return fails, present


ALLOWED_IMPORTS = {"fractions"}


def fence(source):
    """The derivation may import only fractions, and may hold no float: no float literal, no float(), no math."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += ["import " + a.name for a in node.names if a.name.split(".")[0] not in ALLOWED_IMPORTS]
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED_IMPORTS:
                found.append("from %s import" % node.module)
        elif isinstance(node, ast.Constant) and isinstance(node.value, float):
            found.append("float literal %r" % node.value)
        elif isinstance(node, ast.Name) and node.id in ("float", "math", "N", "numeric_ref"):
            found.append("name " + node.id)
    return found


# ------------------------------------------------------------------------------------------------ plants
def _half_away(fr):
    fr = Fraction(fr)
    q, r = divmod(abs(fr.numerator), fr.denominator)
    if 2 * r >= fr.denominator:
        q += 1
    return -q if fr < 0 else q


def _truncated_euclid(a, b):
    if b == 0:
        raise N.Refusal("DIVISION-BY-ZERO")
    q = abs(a) // abs(b)
    q = -q if (a < 0) != (b < 0) else q
    return q, a - b * q


REFERENCE_PLANTS = [
    ("reference-rounds-half-away", "round_half_even", _half_away),
    ("reference-keeps-nan-payloads", "f_canon", lambda x: x),
    ("reference-truncates-remainder", "_euclid", _truncated_euclid),
]


def run_plants(rows, index, source):
    """Each plant, and whether it was caught. A plant is caught only by a failure it causes."""
    out = []
    # 1. one vector line corrupted: the derivation must name exactly that line
    victim = next(r for r in rows if r[1] == "f_add" and r[3] not in ("f:0000000000000000", "f:8000000000000000")
                  and not r[3].startswith(("f:7FF", "f:FFF")))
    k, op, args, result = victim
    flipped = result[:-1] + "%X" % (int(result[-1], 16) ^ 1)
    corrupt = [r if r[0] != k else (k, op, args, flipped) for r in rows]
    bad = check_file(corrupt)[0]
    caught = len(bad) == 1 and bad[0][0] == k
    out.append(("vector-corrupted", caught, "line %d (%s %s => %s, last bit flipped): the derivation named %s"
                % (k, op, " ".join(args), result, ", ".join("line %d" % b[0] for b in bad) or "nothing")))
    # 2-4. a mistake inside numeric_ref, which vectors regenerated from it would share
    for name, attr, wrong in REFERENCE_PLANTS:
        saved = getattr(N, attr)
        setattr(N, attr, wrong)
        try:
            ref_bad = check_reference(rows)
            hand_bad = [f for f in check_hand(index)[0] if f[2] == "numeric_ref"]
        finally:
            setattr(N, attr, saved)
        first = hand_bad[0] if hand_bad else None
        out.append((name, bool(ref_bad) and bool(hand_bad),
                    "the derivation disagrees with the planted numeric_ref on %d argument sets; the hand table "
                    "fails %d case(s)%s" % (len(ref_bad), len(hand_bad),
                                            "; first %s %s: want %s, got %s" % (first[0], first[1], first[3], first[4])
                                            if first else "")))
    # 5. the fence: an import of the reference, and a float literal, each refused
    breaches = [fence(source + "\nimport orlog.numeric_ref\n"), fence(source + "\nTHIRD = 0.3333\n")]
    out.append(("fence-breached", all(breaches), "an added import of numeric_ref: %s; an added float literal: %s"
                % (breaches[0] or "not seen", breaches[1] or "not seen")))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", default=os.path.join(ROOT, "vectors", "runtime-vectors.txt"))
    a = ap.parse_args(argv)
    with open(a.vectors, "rb") as fh:
        body = fh.read()
    rows = read_vectors(a.vectors)
    index = {(op, args): res for _, op, args, res in rows}
    with open(os.path.join(HERE, "numeric_oracle.py"), "rb") as fh:
        source = fh.read().decode("utf-8")
    ok = True

    print("== vectors %s: %d lines, sha256 %s" % (os.path.relpath(a.vectors, ROOT).replace(os.sep, "/"), len(rows),
                                                 hashlib.sha256(body).hexdigest()[:16]))
    breach = fence(source)
    print("fence  tests/numeric_oracle.py imports %s, holds no float: %s" % (
        ", ".join(sorted(ALLOWED_IMPORTS)), "HELD" if not breach else "BREACHED " + "; ".join(breach)))
    ok &= not breach

    bad, per_op, skipped = check_file(rows)
    print("1. derivation vs the vectors: %d of %d lines derived, %d differ" % (sum(per_op.values()), len(rows), len(bad)))
    groups = {"Int": "i_", "Fix": "x_", "Float": "f_", "printing": "fmt_"}
    for g, p in groups.items():
        ops = sorted(o for o in per_op if o.startswith(p))
        print("     %-8s %5d lines over %d ops (%s)" % (g, sum(per_op[o] for o in ops), len(ops), " ".join(ops)))
    for b in bad[:10]:
        print("     DIFFERS line %d: %s %s => vectors %s, derivation %s" % (b[0], b[1], " ".join(b[2]), b[3], b[4]))
    print("     not derived: %d lines (%s): written by hashlib from the generator; two are checked against published "
          "digests below, and the runtimes' own SHA-256 code is held to all of them"
          % (len(skipped), ", ".join(sorted({s[1] for s in skipped}))))
    ok &= not bad
    rbad = check_reference(rows)
    print("   numeric_ref vs the derivation on the same arguments: %d of %d differ" % (len(rbad), sum(per_op.values())))
    for b in rbad[:10]:
        print("     DIFFERS line %d: %s %s => derivation %s, numeric_ref %s" % (b[0], b[1], " ".join(b[2]), b[3], b[4]))
    ok &= not rbad

    hfails, present = check_hand(index)
    print("2. hand table: %d cases worked by hand, each against the derivation and numeric_ref; %d of them are in "
          "the vectors; the smallest subnormal's print by its worked properties: %d failure(s)"
          % (len(HAND), present, len(hfails)))
    for f in hfails[:10]:
        print("     FAIL %s %s: %s says %s, worked by hand %s (%s)" % (f[0], f[1], f[2], f[4], f[3], f[5]))
    print("3. published SHA-256 digests (empty message, 'abc'): %s" % (
        "EQUAL" if not [f for f in hfails if f[0] == "sha256"] else "DIFFER"))
    ok &= not hfails

    for name, caught, detail in run_plants(rows, index, source):
        print("plant %s: %s; %s" % (name, "CAUGHT" if caught else "NOT CAUGHT", detail))
        ok &= caught

    print("does not show: that the specification is right, or that its authors read IEEE 754 rightly. One model "
          "family wrote numeric_ref, the derivation and this table, and a misreading of the specification shared "
          "by all three passes; the hand cases are the only witnesses worked outside a program, and they are few.")
    print("VECTORS AGREE WITH THE DERIVATION, THE HAND TABLE AND THE PUBLISHED DIGESTS" if ok else
          "VECTORS CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

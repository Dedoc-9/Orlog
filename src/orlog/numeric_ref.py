"""Orlog OL-0 numeric semantics, written by definition over exact rationals.

This module is the reference: every rule is stated as a mathematical value
(Fraction, int) and rounded once, at the end, by an explicit rule. The three
backends implement the same rules by bit-level algorithms; they are held to
this module by vectors and by the arbiter, never the other way round.

Types and their carriers:
  Int    a signed 64-bit integer; every result outside [-2^63, 2^63-1] refuses OVERFLOW
  Fix    a binary fixed-point number, raw int64 r standing for r / 2^32 (Q31.32)
  Float  an IEEE 754 binary64 value; every NaN produced by an arithmetic operation is
         replaced by the canonical quiet NaN 0x7FF8000000000000 (the replacement is part of
         the semantics). f_max and f_min return one of their operands unchanged, so a NaN
         given to them comes back as given; inside a program every value is already
         canonical, so this is visible only to callers of these functions directly (the
         vectors do this). Corrected 2026-10-25: an earlier docstring said "every NaN
         result", which f_max/f_min contradicted (found by the Rust runtime's author).
"""
import math
import struct
from fractions import Fraction

I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1
FRAC_BITS = 32
ONE = 1 << FRAC_BITS
CANON_NAN_BITS = 0x7FF8000000000000
LIST_MAX = 1 << 24
TEXT_MAX = 1 << 24


class Refusal(Exception):
    """A deterministic refusal: the run stops, and every backend must stop at
    the same event with the same code."""

    def __init__(self, code):
        Exception.__init__(self, code)
        self.code = code


def chk(v):
    if v < I64_MIN or v > I64_MAX:
        raise Refusal("OVERFLOW")
    return v


def round_half_even(fr):
    """The nearest integer to the rational fr; a tie goes to the even neighbour."""
    fr = Fraction(fr)
    q, r = divmod(fr.numerator, fr.denominator)   # floor: n = q*d + r, 0 <= r < d
    twice = 2 * r
    if twice > fr.denominator or (twice == fr.denominator and (q & 1)):
        q += 1
    return q


def trunc_toward_zero(fr):
    fr = Fraction(fr)
    q = abs(fr.numerator) // fr.denominator
    return q if fr.numerator >= 0 else -q


# ---------------------------------------------------------------- Int
def i_add(a, b): return chk(a + b)
def i_sub(a, b): return chk(a - b)
def i_mul(a, b): return chk(a * b)
def i_neg(a): return chk(-a)
def i_abs(a): return chk(abs(a))
def i_max(a, b): return a if a > b else b
def i_min(a, b): return a if a < b else b


def i_div(a, b):
    """'a divided by b' on Int: the exact quotient, or a refusal."""
    if b == 0:
        raise Refusal("DIVISION-BY-ZERO")
    if a % b != 0:
        raise Refusal("INEXACT-DIVISION")
    return chk(a // b)


def _euclid(a, b):
    if b == 0:
        raise Refusal("DIVISION-BY-ZERO")
    q = a // b
    r = a - b * q
    if r < 0:          # only when b < 0: move to the non-negative remainder
        q += 1
        r -= b
    return q, r        # a = b*q + r, 0 <= r < |b|  (Boute 1992, the Euclidean definition)


def i_quot(a, b):
    q, _ = _euclid(a, b)
    return chk(q)


def i_rem(a, b):
    _, r = _euclid(a, b)
    return r


def i_isqrt(a):
    if a < 0:
        raise Refusal("NEGATIVE-SQRT")
    return math.isqrt(a)


# ---------------------------------------------------------------- Fix (raw int64 = value * 2^32)
def x_from_i(n): return chk(n * ONE)
def x_add(a, b): return chk(a + b)
def x_sub(a, b): return chk(a - b)
def x_neg(a): return chk(-a)
def x_abs(a): return chk(abs(a))
def x_max(a, b): return a if a > b else b
def x_min(a, b): return a if a < b else b
def x_mul(a, b): return chk(round_half_even(Fraction(a * b, ONE)))


def x_div(a, b):
    if b == 0:
        raise Refusal("DIVISION-BY-ZERO")
    return chk(round_half_even(Fraction(a * ONE, b)))


def x_sqrt(a):
    """floor(sqrt(a / 2^32)) in units of 2^-32, that is isqrt(a * 2^32)."""
    if a < 0:
        raise Refusal("NEGATIVE-SQRT")
    return math.isqrt(a * ONE)


def x_trunc(a): return trunc_toward_zero(Fraction(a, ONE))     # -> Int
def x_round(a): return round_half_even(Fraction(a, ONE))       # -> Int


# ---------------------------------------------------------------- Float
_INF = float("inf")


def f_bits(x):
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def f_from_bits(b):
    return struct.unpack("<d", struct.pack("<Q", b & 0xFFFFFFFFFFFFFFFF))[0]


CANON_NAN = f_from_bits(CANON_NAN_BITS)


def f_canon(x):
    return CANON_NAN if x != x else x


def f_add(a, b): return f_canon(a + b)
def f_sub(a, b): return f_canon(a - b)
def f_mul(a, b): return f_canon(a * b)


def f_div(a, b):
    """IEEE 754 division, including division by a signed zero (Python raises there)."""
    if b == 0.0:
        if a != a or a == 0.0:
            return CANON_NAN
        neg = (math.copysign(1.0, a) < 0) != (math.copysign(1.0, b) < 0)
        return -_INF if neg else _INF
    return f_canon(a / b)


def f_neg(a): return f_canon(-a)
def f_abs(a): return f_canon(math.fabs(a))


def f_sqrt(a):
    if a != a or a < 0.0:
        return CANON_NAN
    return math.sqrt(a)          # IEEE: correctly rounded; sqrt(-0.0) = -0.0


def f_max(a, b): return a if a > b else b      # defined by the comparison, not by libm fmax
def f_min(a, b): return a if a < b else b


def _finite(x):
    if x != x or x in (_INF, -_INF):
        raise Refusal("NOT-FINITE")


def f_from_i(n, rounded=False):
    f = float(n)                                 # CPython: correctly rounded, ties to even
    if not rounded and Fraction(f) != n:
        raise Refusal("INEXACT-CONVERSION")
    return f


def f_trunc(x):
    _finite(x)
    return chk(math.trunc(x))


def f_round(x):
    _finite(x)
    return chk(round_half_even(Fraction(x)))


def x_to_f(a, rounded=False):
    exact = Fraction(a, ONE)
    f = a / ONE                                  # int / int true division: correctly rounded
    if not rounded and Fraction(f) != exact:
        raise Refusal("INEXACT-CONVERSION")
    return f


def x_as_i(a):
    """'as an integer' from Fix: exact, or INEXACT-CONVERSION (SPEC section 8; twin note 59)."""
    if a & (ONE - 1):
        raise Refusal("INEXACT-CONVERSION")
    return x_trunc(a)


def f_as_i(x):
    """'as an integer' from Float: NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW (SPEC section 8)."""
    _finite(x)
    if Fraction(x).denominator != 1:
        raise Refusal("INEXACT-CONVERSION")
    return chk(int(x))


def f_to_x(x, rounded=False):
    _finite(x)
    y = Fraction(x) * ONE
    if y.denominator != 1:
        if not rounded:
            raise Refusal("INEXACT-CONVERSION")
        return chk(round_half_even(y))
    return chk(y.numerator)


# ---------------------------------------------------------------- printing (exact decimals)
def _exact_decimal(fr):
    """fr >= 0 with a power-of-two denominator: every digit, nothing rounded."""
    n, d = fr.numerator, fr.denominator
    ip, rem = divmod(n, d)
    if rem == 0:
        return str(ip) + ".0"
    digits = []
    while rem:
        rem *= 10
        dig, rem = divmod(rem, d)
        digits.append(chr(48 + dig))
    return str(ip) + "." + "".join(digits)


def fmt_i(n): return str(n)


def fmt_x(a):
    s = _exact_decimal(Fraction(abs(a), ONE))
    return "-" + s if a < 0 else s


def fmt_f(x):
    if x != x:
        return "NaN"
    if x == _INF:
        return "Infinity"
    if x == -_INF:
        return "-Infinity"
    neg = f_bits(x) >> 63
    s = _exact_decimal(Fraction(abs(x)))
    return "-" + s if neg else s


def fmt_b(v): return "true" if v else "false"

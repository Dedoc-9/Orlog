"""A second derivation of OL-0's numeric semantics, used to check the conformance vectors.

numeric_ref.py generated every line of vectors/runtime-vectors.txt, and both runtimes were held to those lines, so
the vectors on their own define the semantics; they do not confirm it. This module derives the same results again,
from RUNTIME-SPEC sections 2 and 3 and IEEE 754-2019 alone. It never consults numeric_ref.

- It imports nothing from the language, and nothing that computes in floating point: no float, no math. The import
  fence in tests/vectors_independent.py holds that.
- Every Float is decoded from its bits into an exact rational. Every Float result is rounded once, by encode() below.
- Int and Fix rules are computed on sign and magnitude, with shifts. numeric_ref uses floor division over fractions.
- Printing uses RUNTIME-SPEC section 3's own method: the digits of m*5^k, with the point placed k digits from the
  right. numeric_ref uses long division.

What this buys is diversity of method against numeric_ref. It is not diversity of author: one model family wrote
both, and both read the same specification (DOCTRINE section 8). A misreading of the specification shared by the two
passes through. The hand-worked table in tests/vectors_independent.py stands against that, case by case.
"""
from fractions import Fraction

I64_MIN, I64_MAX = -(1 << 63), (1 << 63) - 1
ONE = 1 << 32                     # Fix: raw r stands for r / 2^32
CANON = 0x7FF8000000000000        # the one NaN an operation may produce
INF = 0x7FF0000000000000
SIGN = 1 << 63
DIGITS = "0123456789"


class Refused(Exception):
    def __init__(self, code):
        Exception.__init__(self, code)
        self.code = code


def checked(v):
    if v < I64_MIN or v > I64_MAX:
        raise Refused("OVERFLOW")
    return v


def isqrt(n):
    """floor(sqrt(n)) by Newton's method on integers (numeric_ref uses math.isqrt)."""
    if n < 0:
        raise ValueError(n)
    if n == 0:
        return 0
    x = 1 << ((n.bit_length() + 1) // 2)          # at least sqrt(n)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            break
        x = y
    if not (x * x <= n < (x + 1) * (x + 1)):
        raise AssertionError("isqrt %d" % n)
    return x


def half_even(num, den):
    """The integer nearest num/den (den > 0); a tie goes to the even one. Computed on the magnitude."""
    q, r = divmod(abs(num), den)
    if 2 * r > den or (2 * r == den and q & 1):
        q += 1
    return -q if num < 0 else q


def toward_zero(num, den):
    q = abs(num) // den
    return -q if num < 0 else q


# ------------------------------------------------------------------------------------------------ Int
def i_add(a, b): return checked(a + b)
def i_sub(a, b): return checked(a - b)
def i_mul(a, b): return checked(a * b)
def i_neg(a): return checked(-a)
def i_abs(a): return checked(-a if a < 0 else a)
def i_max(a, b): return a if a > b else b
def i_min(a, b): return a if a < b else b


def i_div(a, b):
    """Exact division: DIVISION-BY-ZERO, then INEXACT-DIVISION, then OVERFLOW (RUNTIME-SPEC section 2)."""
    if b == 0:
        raise Refused("DIVISION-BY-ZERO")
    if abs(a) % abs(b):
        raise Refused("INEXACT-DIVISION")
    q = abs(a) // abs(b)
    return checked(-q if (a < 0) != (b < 0) else q)


def euclid(a, b):
    """a = b*q + r with 0 <= r < |b|: truncated division first, then moved to the non-negative remainder."""
    if b == 0:
        raise Refused("DIVISION-BY-ZERO")
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    r = a - b * q                       # the truncated remainder: the sign of a, |r| < |b|
    if r < 0:
        q, r = (q - 1, r + b) if b > 0 else (q + 1, r - b)
    return q, r


def i_quot(a, b): return checked(euclid(a, b)[0])
def i_rem(a, b): return euclid(a, b)[1]


def i_isqrt(a):
    if a < 0:
        raise Refused("NEGATIVE-SQRT")
    return isqrt(a)


# ------------------------------------------------------------------------------------------------ Fix
def x_from_i(n): return checked(n << 32)
def x_add(a, b): return checked(a + b)
def x_sub(a, b): return checked(a - b)
def x_neg(a): return checked(-a)
def x_abs(a): return checked(-a if a < 0 else a)
def x_max(a, b): return a if a > b else b
def x_min(a, b): return a if a < b else b
def x_mul(a, b): return checked(half_even(a * b, ONE))


def x_div(a, b):
    if b == 0:
        raise Refused("DIVISION-BY-ZERO")
    num, den = a * ONE, b
    if den < 0:
        num, den = -num, -den
    return checked(half_even(num, den))


def x_sqrt(a):
    if a < 0:
        raise Refused("NEGATIVE-SQRT")
    return isqrt(a << 32)


def x_trunc(a): return toward_zero(a, ONE)
def x_round(a): return half_even(a, ONE)


# ------------------------------------------------------------------------------------------------ Float
def unpack(bits):
    """('nan',), ('inf', sign) or ('fin', sign, m, e) with the value (-1)^sign * m * 2^e."""
    sign, ex, frac = bits >> 63, (bits >> 52) & 0x7FF, bits & ((1 << 52) - 1)
    if ex == 0x7FF:
        return ("nan",) if frac else ("inf", sign)
    if ex == 0:
        return ("fin", sign, frac, -1074)            # zero or subnormal
    return ("fin", sign, frac | (1 << 52), ex - 1075)


def magnitude(u):
    m, e = u[2], u[3]
    return Fraction(m << e) if e >= 0 else Fraction(m, 1 << -e)


def value(u):
    """The exact signed value of a finite unpacked Float (a zero loses its sign here)."""
    v = magnitude(u)
    return -v if u[1] else v


def floor_log2(q):
    """e with 2^e <= q < 2^(e+1), for an exact rational q > 0."""
    n, d = q.numerator, q.denominator
    e = n.bit_length() - d.bit_length()               # floor(log2 q) is e or e - 1
    left = n << -e if e < 0 else n
    right = d << e if e > 0 else d
    return e - 1 if left < right else e


def encode(sign, mag):
    """The binary64 bits nearest (-1)^sign * mag, for an exact rational mag >= 0; a tie goes to the even
    significand (IEEE 754-2019 section 4.3.1); a result that rounds beyond the largest finite value is infinity
    (section 7.4); a result below the smallest subnormal rounds to a zero of the exact result's sign."""
    if mag == 0:
        return sign << 63
    e = floor_log2(mag)
    qe = max(e - 52, -1074)                            # the quantum: 53 significant bits, or the subnormal step
    n, d = mag.numerator, mag.denominator
    if qe >= 0:
        d <<= qe
    else:
        n <<= -qe
    m, r = divmod(n, d)
    if 2 * r > d or (2 * r == d and m & 1):
        m += 1
    if m == 0:
        return sign << 63
    if m == 1 << 53:                                   # the rounding carried into a new binade
        m, qe = m >> 1, qe + 1
    if m.bit_length() + qe > 1024:
        return (sign << 63) | INF
    if m < 1 << 52:
        if qe != -1074:
            raise AssertionError("a short significand above the subnormal range")
        return (sign << 63) | m
    return (sign << 63) | ((qe + 1075) << 52) | (m - (1 << 52))


def _key(u):
    if u[0] == "inf":
        return (-1, 0) if u[1] else (1, 0)
    return (0, value(u))


def f_lt(a, b):
    ua, ub = unpack(a), unpack(b)
    if ua[0] == "nan" or ub[0] == "nan":
        return False                                   # unordered: every comparison is false
    return _key(ua) < _key(ub)


def f_eq(a, b):
    ua, ub = unpack(a), unpack(b)
    if ua[0] == "nan" or ub[0] == "nan":
        return False
    return _key(ua) == _key(ub)                        # +0 and -0 are equal


def f_max(a, b): return a if f_lt(b, a) else b         # a > b ? a : b, the operand's bits unchanged
def f_min(a, b): return a if f_lt(a, b) else b


def f_neg(a): return CANON if unpack(a)[0] == "nan" else a ^ SIGN
def f_abs(a): return CANON if unpack(a)[0] == "nan" else a & (SIGN - 1)


def f_add(a, b):
    ua, ub = unpack(a), unpack(b)
    if ua[0] == "nan" or ub[0] == "nan":
        return CANON
    if ua[0] == "inf" and ub[0] == "inf":
        return CANON if ua[1] != ub[1] else (ua[1] << 63) | INF
    if ua[0] == "inf":
        return (ua[1] << 63) | INF
    if ub[0] == "inf":
        return (ub[1] << 63) | INF
    s = value(ua) + value(ub)
    if s == 0:
        # an exact zero is +0 under round-to-nearest, except (-0) + (-0) (IEEE 754-2019 section 6.3)
        both_negative_zeros = ua[1] and ub[1] and ua[2] == 0 and ub[2] == 0
        return SIGN if both_negative_zeros else 0
    return encode(1 if s < 0 else 0, abs(s))


def f_sub(a, b):
    return f_add(a, b ^ SIGN)                          # subtraction(x, y) is addition(x, -y): section 5.4.1


def f_mul(a, b):
    ua, ub = unpack(a), unpack(b)
    if ua[0] == "nan" or ub[0] == "nan":
        return CANON
    sign = ua[1] ^ ub[1]
    if ua[0] == "inf" or ub[0] == "inf":
        other = ub if ua[0] == "inf" else ua
        if other[0] == "fin" and other[2] == 0:
            return CANON                               # infinity times zero
        return (sign << 63) | INF
    return encode(sign, magnitude(ua) * magnitude(ub))


def f_div(a, b):
    ua, ub = unpack(a), unpack(b)
    if ua[0] == "nan" or ub[0] == "nan":
        return CANON
    sign = ua[1] ^ ub[1]
    if ua[0] == "inf":
        return CANON if ub[0] == "inf" else (sign << 63) | INF
    if ub[0] == "inf":
        return sign << 63
    if ub[2] == 0:
        return CANON if ua[2] == 0 else (sign << 63) | INF
    return encode(sign, magnitude(ua) / magnitude(ub))


def f_sqrt(a):
    u = unpack(a)
    if u[0] == "nan":
        return CANON
    if u[0] == "inf":
        return CANON if u[1] else INF
    if u[2] == 0:
        return a                                       # the square root of -0 is -0
    if u[1]:
        return CANON
    q = magnitude(u)
    qe = floor_log2(q) // 2 - 52                       # sqrt(q) / 2^qe lies in [2^52, 2^53)
    x = q * Fraction(1 << (-2 * qe)) if qe < 0 else q / Fraction(1 << (2 * qe))
    four = 4 * x
    t = isqrt(four.numerator // four.denominator)      # t = floor(2 * sqrt(x))
    n = (t + 1) // 2                                   # the nearest integer to sqrt(x) ...
    if t & 1 and four == t * t:                        # ... unless sqrt(x) is exactly a half (never, for binary64)
        n = t // 2 if (t // 2) % 2 == 0 else t // 2 + 1
    return encode(0, Fraction(n) * Fraction(1 << qe) if qe >= 0 else Fraction(n, 1 << -qe))


def _finite(u):
    if u[0] != "fin":
        raise Refused("NOT-FINITE")


def f_trunc(a):
    u = unpack(a)
    _finite(u)
    v = value(u)
    return checked(toward_zero(v.numerator, v.denominator))


def f_round(a):
    u = unpack(a)
    _finite(u)
    v = value(u)
    return checked(half_even(v.numerator, v.denominator))


def f_to_x(a, rounded):
    """NOT-FINITE; then x * 2^32 exact, or INEXACT-CONVERSION (half-even when rounded); then OVERFLOW."""
    u = unpack(a)
    _finite(u)
    y = value(u) * ONE
    if y.denominator == 1:
        return checked(y.numerator)
    if not rounded:
        raise Refused("INEXACT-CONVERSION")
    return checked(half_even(y.numerator, y.denominator))


def _to_float(exact, rounded):
    bits = encode(1 if exact < 0 else 0, abs(exact))
    if not rounded and value(unpack(bits)) != exact:
        raise Refused("INEXACT-CONVERSION")
    return bits


def f_from_i(n, rounded): return _to_float(Fraction(n), rounded)
def x_to_f(a, rounded): return _to_float(Fraction(a, ONE), rounded)


# ------------------------------------------------------------------------------------------------ printing
def fmt_i(n):
    m, out = -n if n < 0 else n, []
    while True:
        m, d = divmod(m, 10)
        out.append(DIGITS[d])
        if m == 0:
            break
    return ("-" if n < 0 else "") + "".join(reversed(out))


def _point(m, k):
    """The exact decimal of m * 2^-k (m >= 0): the digits of m * 5^k with the point k places from the right,
    every digit kept, trailing zeros removed, '.0' when integral (RUNTIME-SPEC section 3)."""
    if k <= 0:
        return fmt_i(m << -k) + ".0"
    digits = fmt_i(m * 5 ** k)
    if len(digits) <= k:
        digits = "0" * (k + 1 - len(digits)) + digits
    whole, frac = digits[:-k], digits[-k:].rstrip("0")
    return whole + "." + (frac or "0")


def fmt_x(a): return ("-" if a < 0 else "") + _point(-a if a < 0 else a, 32)


def fmt_f(a):
    u = unpack(a)
    if u[0] == "nan":
        return "NaN"
    if u[0] == "inf":
        return "-Infinity" if u[1] else "Infinity"
    return ("-" if u[1] else "") + _point(u[2], -u[3])  # the sign bit decides, so -0.0 prints '-0.0'


# ------------------------------------------------------------------------------------------------ the vector ops
# op -> (function, the tag its result is written with)
OPS = {
    "i_add": (i_add, "i"), "i_sub": (i_sub, "i"), "i_mul": (i_mul, "i"), "i_div": (i_div, "i"),
    "i_quot": (i_quot, "i"), "i_rem": (i_rem, "i"), "i_neg": (i_neg, "i"), "i_abs": (i_abs, "i"),
    "i_isqrt": (i_isqrt, "i"), "i_max": (i_max, "i"), "i_min": (i_min, "i"),
    "x_from_i": (x_from_i, "x"), "x_add": (x_add, "x"), "x_sub": (x_sub, "x"), "x_mul": (x_mul, "x"),
    "x_div": (x_div, "x"), "x_neg": (x_neg, "x"), "x_abs": (x_abs, "x"), "x_sqrt": (x_sqrt, "x"),
    "x_max": (x_max, "x"), "x_min": (x_min, "x"), "x_trunc": (x_trunc, "i"), "x_round": (x_round, "i"),
    "x_to_f": (x_to_f, "f"),
    "f_add": (f_add, "f"), "f_sub": (f_sub, "f"), "f_mul": (f_mul, "f"), "f_div": (f_div, "f"),
    "f_max": (f_max, "f"), "f_min": (f_min, "f"), "f_neg": (f_neg, "f"), "f_abs": (f_abs, "f"),
    "f_sqrt": (f_sqrt, "f"), "f_lt": (f_lt, "b"), "f_eq": (f_eq, "b"), "f_trunc": (f_trunc, "i"),
    "f_round": (f_round, "i"), "f_to_x": (f_to_x, "x"), "f_from_i": (f_from_i, "f"),
    "fmt_i": (fmt_i, "s"), "fmt_x": (fmt_x, "s"), "fmt_f": (fmt_f, "s"),
}


def parse_arg(tok):
    tag, _, v = tok.partition(":")
    if tag in ("i", "x"):
        return int(v)
    if tag == "f":
        return int(v, 16)
    if tag == "b":
        return v == "1"
    raise ValueError("an argument this module does not derive: %r" % tok)


def render(tag, r):
    if tag in ("i", "x"):
        return "%s:%d" % (tag, r)
    if tag == "f":
        return "f:%016X" % r
    if tag == "b":
        return "b:%d" % (1 if r else 0)
    return "s:" + r


def derive(op, args):
    """The result of one vector line as this module derives it, in the vectors' own notation."""
    fn, tag = OPS[op]
    try:
        return render(tag, fn(*[parse_arg(t) for t in args]))
    except Refused as e:
        return "!" + e.code

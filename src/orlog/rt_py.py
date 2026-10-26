# ---- ORLOG OL-0 PYTHON RUNTIME (pasted at the top of every generated Python program) ----
# Bit-level algorithms, written apart from the reference's rationals (numeric_ref.py).
import hashlib as _hashlib
import math as _math
import struct as _struct
import sys as _sys

_I64_MIN = -(1 << 63)
_I64_MAX = (1 << 63) - 1
_ONE = 1 << 32
_MASK32 = _ONE - 1
_HALF32 = 1 << 31
_TEXT_MAX = 1 << 24
_LIST_MAX = 1 << 24
_OUTPUT_MAX = 1 << 30
_CANON_NAN = _struct.unpack("<d", _struct.pack("<Q", 0x7FF8000000000000))[0]
_INF = float("inf")


def _fbits(x):
    return _struct.unpack("<Q", _struct.pack("<d", x))[0]


def _bitsf(b):
    return _struct.unpack("<d", _struct.pack("<Q", b & 0xFFFFFFFFFFFFFFFF))[0]


def _isqrt(n):
    """Digit-by-digit (base 4) integer square root: floor(sqrt(n)), n >= 0."""
    bit = 1 << ((n.bit_length() + 1) // 2 * 2)
    res = 0
    while bit > n and bit:
        bit >>= 2
    while bit:
        if n >= res + bit:
            n -= res + bit
            res = (res >> 1) + bit
        else:
            res >>= 1
        bit >>= 2
    return res


def _rhe_shift(mag, k):
    """Round a non-negative integer divided by 2^k, ties to even."""
    q = mag >> k
    r = mag & ((1 << k) - 1)
    half = 1 << (k - 1)
    if r > half or (r == half and (q & 1)):
        q += 1
    return q


def _rhe_div(n, d):
    """Round n / d (n >= 0, d > 0), ties to even."""
    q, r = divmod(n, d)
    if 2 * r > d or (2 * r == d and (q & 1)):
        q += 1
    return q


def _dec(mag_int, frac_num, frac_den_pow2):
    """Exact decimal of mag_int + frac_num / 2^frac_den_pow2 (frac_num < 2^k)."""
    s = str(mag_int)
    if frac_num == 0:
        return s + ".0"
    # frac_num / 2^k = frac_num * 5^k / 10^k : every digit, then strip trailing zeros
    k = frac_den_pow2
    digits = str(frac_num * (5 ** k)).rjust(k, "0").rstrip("0")
    return s + "." + digits


class Rt:
    def __init__(self, backend, law_hex, text_hex, claim_clauses, argv):
        if len(argv) < 3:
            _sys.stderr.write("usage: program OUTPUT RECEIPT [TRACE]\n")
            _sys.exit(2)
        self.backend, self.law_hex, self.text_hex = backend, law_hex, text_hex
        self.claim_clauses = list(claim_clauses)
        self.claims = [[0, 0, 0, 0, 0] for _ in claim_clauses]
        try:
            self.out = open(argv[1], "wb")
            self.receipt_path = argv[2]
            self.trace = open(argv[3], "wb") if len(argv) > 3 else None
        except OSError as e:
            _sys.stderr.write("cannot open: %s\n" % e)
            _sys.exit(2)
        self.out_hash = _hashlib.sha256()
        self.out_len = 0
        self.head = _hashlib.sha256(b"orlog-trace-0" + bytes.fromhex(law_hex)).digest()
        self.events = 0
        self.ops = 0
        self.buf = bytearray()
        self.buf_clause = 0

    # ---- events, receipt, refusal
    def _ev(self, kind, c, payload):
        self.head = _hashlib.sha256(self.head + kind + _struct.pack(">II", c, len(payload)) + payload).digest()
        self.events += 1
        if self.trace is not None:
            self.trace.write(("%d %s %d %s %s\n" % (self.events, kind.decode(), c,
                                                    payload.hex() if payload else "-", self.head.hex())).encode())

    def _receipt(self, status):
        lines = ["orlog-receipt 0", "backend " + self.backend, "law-seal " + self.law_hex,
                 "text-seal " + self.text_hex, "status " + status, "output-bytes %d" % self.out_len,
                 "output-sha256 " + self.out_hash.hexdigest(), "events %d" % self.events,
                 "trace-head " + self.head.hex(), "ops %d" % self.ops, "claims %d" % len(self.claim_clauses)]
        for i, cl in enumerate(self.claim_clauses):
            a = self.claims[i]
            lines.append("claim %d %d %d %d %d %d %d" % (i, cl, a[0], a[1], a[2], a[3], a[4]))
        lines.append("end")
        with open(self.receipt_path, "wb") as fh:
            fh.write(("\n".join(lines) + "\n").encode("ascii"))
        self.out.close()
        if self.trace is not None:
            self.trace.close()

    def refuse(self, code, c):
        self._ev(b"R", c, code.encode("ascii"))
        self._receipt("REFUSED %s %d" % (code, c))
        _sys.exit(0)

    def finish(self):
        self._receipt("COMPLETED")
        _sys.exit(0)

    def _chk(self, v, c):
        if v < _I64_MIN or v > _I64_MAX:
            self.refuse("OVERFLOW", c)
        return v

    # ---- Int
    def i_add(self, a, b, c): return self._chk(a + b, c)
    def i_sub(self, a, b, c): return self._chk(a - b, c)
    def i_mul(self, a, b, c): return self._chk(a * b, c)
    def i_neg(self, a, c): return self._chk(-a, c)
    def i_abs(self, a, c): return self._chk(-a if a < 0 else a, c)

    @staticmethod
    def i_max(a, b): return a if a > b else b

    @staticmethod
    def i_min(a, b): return a if a < b else b

    def i_div(self, a, b, c):
        if b == 0:
            self.refuse("DIVISION-BY-ZERO", c)
        q = abs(a) // abs(b)
        if q * abs(b) != abs(a):
            self.refuse("INEXACT-DIVISION", c)
        return self._chk(q if (a < 0) == (b < 0) else -q, c)

    def _euclid(self, a, b, c):
        if b == 0:
            self.refuse("DIVISION-BY-ZERO", c)
        q = abs(a) // abs(b)                      # truncated quotient's magnitude
        if (a < 0) != (b < 0):
            q = -q
        r = a - b * q                             # remainder with the sign of a
        if r < 0:
            if b > 0:
                q -= 1
                r += b
            else:
                q += 1
                r -= b
        return q, r

    def i_quot(self, a, b, c): return self._chk(self._euclid(a, b, c)[0], c)
    def i_rem(self, a, b, c): return self._euclid(a, b, c)[1]

    def i_isqrt(self, a, c):
        if a < 0:
            self.refuse("NEGATIVE-SQRT", c)
        return _isqrt(a)

    # ---- Fix (raw int64, value = raw / 2^32)
    def x_from_i(self, n, c): return self._chk(n << 32 if n >= 0 else -((-n) << 32), c)
    def x_add(self, a, b, c): return self._chk(a + b, c)
    def x_sub(self, a, b, c): return self._chk(a - b, c)
    def x_neg(self, a, c): return self._chk(-a, c)
    def x_abs(self, a, c): return self._chk(-a if a < 0 else a, c)

    @staticmethod
    def x_max(a, b): return a if a > b else b

    @staticmethod
    def x_min(a, b): return a if a < b else b

    def x_mul(self, a, b, c):
        mag = _rhe_shift(abs(a) * abs(b), 32)
        return self._chk(mag if (a < 0) == (b < 0) else -mag, c)

    def x_div(self, a, b, c):
        if b == 0:
            self.refuse("DIVISION-BY-ZERO", c)
        mag = _rhe_div(abs(a) << 32, abs(b))
        return self._chk(mag if (a < 0) == (b < 0) else -mag, c)

    def x_sqrt(self, a, c):
        if a < 0:
            self.refuse("NEGATIVE-SQRT", c)
        return _isqrt(a << 32)

    @staticmethod
    def x_trunc(a):
        q = abs(a) >> 32
        return q if a >= 0 else -q

    @staticmethod
    def x_round(a):
        q = _rhe_shift(abs(a), 32)
        return q if a >= 0 else -q

    def x_as_i(self, a, c):
        if a & _MASK32:
            self.refuse("INEXACT-CONVERSION", c)
        return Rt.x_trunc(a)

    def x_to_f(self, a, rounded, c):
        f = float(a)                              # CPython int -> float: nearest, ties to even
        if not rounded and int(f) != a:
            self.refuse("INEXACT-CONVERSION", c)
        return _math.ldexp(f, -32)                # exact: scaling by a power of two

    def f_to_x(self, x, rounded, c):
        if x != x or x in (_INF, -_INF):
            self.refuse("NOT-FINITE", c)
        n, d = x.as_integer_ratio()               # exact; d is a power of two
        num = n * _ONE
        if num % d:
            if not rounded:
                self.refuse("INEXACT-CONVERSION", c)
            mag = _rhe_div(abs(num), d)
            return self._chk(mag if num >= 0 else -mag, c)
        return self._chk(num // d, c)

    # ---- Float
    @staticmethod
    def f_canon(x): return _CANON_NAN if x != x else x

    @staticmethod
    def f_add(a, b): return Rt.f_canon(a + b)

    @staticmethod
    def f_sub(a, b): return Rt.f_canon(a - b)

    @staticmethod
    def f_mul(a, b): return Rt.f_canon(a * b)

    @staticmethod
    def f_div(a, b):
        if b == 0.0:
            if a != a or a == 0.0:
                return _CANON_NAN
            sa = _fbits(a) >> 63
            sb = _fbits(b) >> 63
            return -_INF if sa != sb else _INF
        return Rt.f_canon(a / b)

    @staticmethod
    def f_neg(a): return Rt.f_canon(-a)

    @staticmethod
    def f_abs(a): return Rt.f_canon(_bitsf(_fbits(a) & 0x7FFFFFFFFFFFFFFF))

    @staticmethod
    def f_sqrt(a):
        if a != a or a < 0.0:
            return _CANON_NAN
        return _math.sqrt(a)

    @staticmethod
    def f_max(a, b): return a if a > b else b

    @staticmethod
    def f_min(a, b): return a if a < b else b

    def f_from_i(self, n, rounded, c):
        f = float(n)
        if not rounded and int(f) != n:
            self.refuse("INEXACT-CONVERSION", c)
        return f

    def f_trunc(self, x, c):
        if x != x or x in (_INF, -_INF):
            self.refuse("NOT-FINITE", c)
        return self._chk(int(x), c)

    def f_round(self, x, c):
        if x != x or x in (_INF, -_INF):
            self.refuse("NOT-FINITE", c)
        n, d = x.as_integer_ratio()
        mag = _rhe_div(abs(n), d)
        return self._chk(mag if n >= 0 else -mag, c)

    def f_as_i(self, x, c):
        t = self.f_trunc(x, c)
        if float(t) != x:
            self.refuse("INEXACT-CONVERSION", c)
        return t

    # ---- printing
    @staticmethod
    def fmt_i(v): return str(v)

    @staticmethod
    def fmt_x(a):
        m = abs(a)
        s = _dec(m >> 32, m & _MASK32, 32)
        return "-" + s if a < 0 else s

    @staticmethod
    def fmt_f(x):
        b = _fbits(x)
        e = (b >> 52) & 0x7FF
        f = b & ((1 << 52) - 1)
        neg = "-" if b >> 63 else ""
        if e == 0x7FF:
            return "NaN" if f else neg + "Infinity"
        if e == 0:
            m, p = f, -1074
        else:
            m, p = f | (1 << 52), e - 1075
        if p >= 0:
            return neg + str(m << p) + ".0"
        k = -p
        return neg + _dec(m >> k, m & ((1 << k) - 1), k)

    # ---- text builder and output
    def s_reset(self, c):
        self.buf = bytearray()
        self.buf_clause = c

    def _app(self, piece):
        if len(self.buf) + len(piece) > _TEXT_MAX:
            self.refuse("TEXT-TOO-LONG", self.buf_clause)
        self.buf += piece

    def s_lit(self, b): self._app(b)
    def s_t(self, b): self._app(b)
    def s_i(self, v): self._app(Rt.fmt_i(v).encode())
    def s_x(self, v): self._app(Rt.fmt_x(v).encode())
    def s_f(self, v): self._app(Rt.fmt_f(v).encode())
    def s_b(self, v): self._app(b"true" if v else b"false")

    def s_list(self, tag, lst):
        self._app(b"[")
        for i, v in enumerate(lst):
            if i:
                self._app(b", ")
            if tag == "I":
                self.s_i(v)
            elif tag == "X":
                self.s_x(v)
            elif tag == "F":
                self.s_f(v)
            else:
                self.s_b(v)
        self._app(b"]")

    def s_take(self):
        return bytes(self.buf)

    def say(self, c):
        line = bytes(self.buf) + b"\n"
        if self.out_len + len(line) > _OUTPUT_MAX:
            self.refuse("OUTPUT-TOO-LONG", c)
        self.out.write(line)
        self.out_hash.update(line)
        self.out_len += len(line)
        self._ev(b"S", c, line)

    # ---- value encodings
    @staticmethod
    def _slot(tag, v):
        if tag in "IX":
            return _struct.pack(">q", v)
        if tag == "F":
            return _struct.pack(">Q", _fbits(Rt.f_canon(v)))
        return b"\x01" if v else b"\x00"

    @staticmethod
    def _enc(tag, v):
        if tag[0] == "L":
            e = tag[1]
            return b"L" + e.encode() + _struct.pack(">I", len(v)) + b"".join(Rt._slot(e, x) for x in v)
        if tag == "T":
            return b"T" + _struct.pack(">I", len(v)) + v
        return tag.encode() + Rt._slot(tag, v)

    def ev_assign(self, c, var, tag, v): self._ev(b"A", c, _struct.pack(">I", var) + Rt._enc(tag, v))
    def ev_item(self, c, var, k, tag, v): self._ev(b"E", c, _struct.pack(">IQ", var, k) + Rt._enc(tag, v))
    def ev_push(self, c, var, tag, v): self._ev(b"P", c, _struct.pack(">I", var) + Rt._enc(tag, v))
    def ev_pop(self, c, var, n): self._ev(b"Q", c, _struct.pack(">IQ", var, n))

    # ---- claims and musts
    def claim(self, i, c, r, cost, ref, refcost):
        self._ev(b"C", c, _struct.pack(">I", i) + (b"\x01" if r else b"\x00"))
        a = self.claims[i]
        a[0] += 1
        a[1] += 1 if r else 0
        a[2] += cost
        a[3], a[4] = ref, refcost
        if not r:
            self.refuse("CLAIM-REFUTED", c)

    def must(self, i, c, r):
        self._ev(b"M", c, _struct.pack(">I", i) + (b"\x01" if r else b"\x00"))
        if not r:
            self.refuse("MUST-FAILED", c)

    # ---- lists
    def l_new(self, n, v, c):
        if n < 0:
            self.refuse("NEGATIVE-LENGTH", c)
        if n > _LIST_MAX:
            self.refuse("LIST-TOO-LONG", c)
        return [v] * n

    def l_get(self, lst, k, c):
        if k < 1 or k > len(lst):
            self.refuse("INDEX-OUT-OF-RANGE", c)
        return lst[k - 1]

    def l_set(self, lst, k, v, c):
        if k < 1 or k > len(lst):
            self.refuse("INDEX-OUT-OF-RANGE", c)
        lst[k - 1] = v

    def l_push(self, lst, v, c):
        if len(lst) + 1 > _LIST_MAX:
            self.refuse("LIST-TOO-LONG", c)
        lst.append(v)

    def l_pop(self, lst, c):
        if not lst:
            self.refuse("EMPTY-LIST", c)
        lst.pop()
# ---- END OF RUNTIME ----

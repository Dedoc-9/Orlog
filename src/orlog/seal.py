"""Seals in words, and a check syllable per line.

Isopsephy reversed: the classical systems read words as numbers (abjad, isopsephy,
Katapayadi, chronograms); a seal reads a number (a sha256) as speakable words, so a
person can compare two seals aloud. The rendering is proquint-shaped (Wilkerson 2009):
consonant-vowel-consonant-vowel-consonant per 16 bits.

The abjad's weakness is that a sum is commutative: it cannot see two letters swapped.
The line check fixes exactly that. It folds a line's bytes with x o y = 2x + y over GF(2^8)
(polynomial 0x11B). Because 2 is not 0 or 1, that operation is a totally anti-symmetric
quasigroup (Damm's construction for prime-power orders), so the check changes under any
single byte substitution and any swap of two adjacent unequal bytes. It guards against
accidents of copying, never against an adversary: anyone can recompute it.
"""
import hashlib

CONS = "bdfghjklmnprstvz"
VOWS = "aiou"
FINS = "nrsl"
_Q = "[%s][%s][%s][%s][%s]" % (CONS, VOWS, CONS, VOWS, CONS)
PROQUINT_RE = "%s(?:-%s){3}" % (_Q, _Q)


def proquint16(v):
    return (CONS[(v >> 12) & 15] + VOWS[(v >> 10) & 3] + CONS[(v >> 6) & 15] +
            VOWS[(v >> 4) & 3] + CONS[v & 15])


def seal_words(hex64):
    """The first 64 bits of a sha256, as four proquints."""
    b = bytes.fromhex(hex64)[:8]
    return "-".join(proquint16((b[i] << 8) | b[i + 1]) for i in range(0, 8, 2))


def gmul2(x):
    x <<= 1
    if x & 0x100:
        x ^= 0x11B
    return x & 0xFF


def fold(data):
    acc = 0
    for byte in data:
        acc = gmul2(acc) ^ byte
    return acc


def syllable(v):
    return CONS[(v >> 4) & 15] + VOWS[(v >> 2) & 3] + FINS[v & 3]


def line_check(line_text):
    """The check syllable of a clause line (label to final period, no suffix)."""
    return syllable(fold(line_text.encode("utf-8")))


def stamp(text):
    """Return text with a fresh check syllable on every clause line."""
    import re
    from .syntax import LABEL_RE, CHECK_RE
    out = []
    for line in text.split("\n"):
        m = CHECK_RE.match(line)
        if m and LABEL_RE.match(m.group(1)):
            line = m.group(1)
        if LABEL_RE.match(line) and line.endswith("."):
            line = "%s [%s]" % (line, line_check(line))
        out.append(line)
    return "\n".join(out)


def damm_property_exhaustive():
    """x o y = 2x + y over GF(2^8): (c o x) o y == (c o y) o x implies x == y, for every c, x, y.
    Linear, so c cancels; checked over all 65,536 (x, y) at c = 0 and a sample of c."""
    for c in (0, 1, 0x53, 0xFF):
        for x in range(256):
            for y in range(256):
                lhs = gmul2(gmul2(c) ^ x) ^ y
                rhs = gmul2(gmul2(c) ^ y) ^ x
                if lhs == rhs and x != y:
                    return False
    return True


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()

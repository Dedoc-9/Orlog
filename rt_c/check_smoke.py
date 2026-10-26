"""Independent check of one smoke run (smoke.c).

Rebuilds the expected output, every event (kind, clause, payload), the hash
chain and the receipt from RUNTIME-SPEC.md's encodings (struct, hashlib) and
numeric_ref's own values and formatters, without the C runtime, and compares
them byte for byte with the files smoke.exe wrote.

  python -B check_smoke.py OUTPUT RECEIPT TRACE complete|refuse

Prints SMOKE CHECK PASSED (<mode>) and exits 0, or names the first difference
of each file and exits 1.
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from orlog import numeric_ref as N  # noqa: E402

CANON = 0x7FF8000000000000
WORD = "\u00d8rl\u01ebg".encode("utf-8")   # the 7 bytes smoke.c writes as ORLOG_WORD


def canon(bits):
    if (bits >> 52) & 0x7FF == 0x7FF and bits & ((1 << 52) - 1):
        return CANON
    return bits


def elem(tag, slot):
    """An element without its tag (list elements; the tail of a scalar)."""
    if tag in "IX":
        return struct.pack(">q", slot)
    if tag == "F":
        return struct.pack(">Q", canon(slot & 0xFFFFFFFFFFFFFFFF))
    if tag == "B":
        return bytes([1 if slot else 0])
    raise ValueError(tag)


def scalar(tag, slot):
    return tag.encode("ascii") + elem(tag, slot)


def u32(v):
    return struct.pack(">I", v)


def u64(v):
    return struct.pack(">Q", v)


def expected(mode):
    events = []
    output = bytearray()

    def say(c, text):
        line = text + b"\n"
        output.extend(line)
        events.append(("S", c, line))

    total = 0
    for i in range(1, 11):
        total = N.i_add(total, N.i_mul(i, i))
        events.append(("A", 3, u32(0) + scalar("I", total)))
    say(4, b"sum of squares 1..10 = " + N.fmt_i(total).encode())

    third_x = N.x_div(N.x_from_i(1), N.x_from_i(3))
    events.append(("A", 5, u32(1) + scalar("X", third_x)))
    say(5, b"one third as Fix = " + N.fmt_x(third_x).encode())

    third_f = N.f_div(1.0, 3.0)
    events.append(("A", 6, u32(2) + scalar("F", N.f_bits(third_f))))
    say(6, b"one third as Float = " + N.fmt_f(third_f).encode())
    inf = N.f_div(1.0, 0.0)
    nan = N.f_sub(inf, inf)
    events.append(("A", 6, u32(3) + scalar("F", N.f_bits(nan))))
    events.append(("A", 6, u32(4) + scalar("F", 0xFFF8000000000001)))
    say(6, " ".join([N.fmt_f(nan), N.fmt_f(inf), N.fmt_f(N.f_neg(0.0)),
                     N.fmt_f(N.f_from_bits(1))]).encode())

    events.append(("A", 7, u32(5) + scalar("B", 1)))
    say(7, b"flag = " + N.fmt_b(True).encode())

    events.append(("A", 8, u32(6) + b"T" + u32(len(WORD)) + WORD))
    say(8, b"text = " + WORD)

    lst = [0, 0, 0]
    lst[1] = 7
    events.append(("E", 9, u32(7) + u64(2) + scalar("I", 7)))
    lst.append(-5)
    events.append(("P", 9, u32(7) + scalar("I", -5)))
    lst.pop()
    events.append(("Q", 9, u32(7) + u64(len(lst))))
    events.append(("A", 9, u32(7) + b"LI" + u32(len(lst)) + b"".join(elem("I", s) for s in lst)))
    say(9, b"list = [" + ", ".join(N.fmt_i(s) for s in lst).encode() + b"]")
    fl = [N.f_bits(0.5), N.f_bits(-0.0), 0x7FF4000000000000]
    bl = [1, 0, 1]
    events.append(("A", 10, u32(8) + b"LF" + u32(3) + b"".join(elem("F", s) for s in fl)))
    events.append(("E", 10, u32(8) + u64(3) + scalar("F", fl[2])))
    events.append(("P", 10, u32(8) + scalar("F", fl[2])))
    events.append(("A", 10, u32(9) + b"LB" + u32(3) + b"".join(elem("B", s) for s in bl)))
    say(10, ("[" + ", ".join(N.fmt_f(N.f_from_bits(s)) for s in fl) + "] ["
             + ", ".join(N.fmt_b(s) for s in bl) + "]").encode())

    events.append(("M", 13, u32(0) + bytes([1])))
    events.append(("C", 11, u32(0) + bytes([1])))
    events.append(("C", 12, u32(1) + bytes([1])))
    events.append(("C", 12, u32(1) + bytes([1])))
    claims = [(11, 1, 1, 20, 3, 20), (12, 2, 2, 15, 8, 9)]
    status = "status COMPLETED"
    if mode == "refuse":
        say(14, b"about to overflow")
        events.append(("R", 14, b"OVERFLOW"))
        status = "status REFUSED OVERFLOW 14"

    law_hex = hashlib.sha256(b"smoke law").hexdigest()
    text_hex = hashlib.sha256(b"smoke text").hexdigest()
    head = hashlib.sha256(b"orlog-trace-0" + bytes.fromhex(law_hex)).digest()
    trace = []
    for n, (kind, clause, payload) in enumerate(events, 1):
        head = hashlib.sha256(head + kind.encode("ascii") + struct.pack(">II", clause, len(payload))
                              + payload).digest()
        trace.append("%d %s %d %s %s\n" % (n, kind, clause, payload.hex() if payload else "-", head.hex()))
    receipt = "".join(line + "\n" for line in (
        ["orlog-receipt 0", "backend c99", "law-seal " + law_hex, "text-seal " + text_hex, status,
         "output-bytes %d" % len(output), "output-sha256 " + hashlib.sha256(bytes(output)).hexdigest(),
         "events %d" % len(events), "trace-head " + head.hex(), "ops 22", "claims %d" % len(claims)]
        + ["claim %d %d %d %d %d %d %d" % ((k,) + c) for k, c in enumerate(claims)] + ["end"]))
    return bytes(output), "".join(trace).encode("ascii"), receipt.encode("ascii")


def first_difference(name, got, want):
    if got == want:
        return True
    gl, wl = got.split(b"\n"), want.split(b"\n")
    for k in range(max(len(gl), len(wl))):
        g = gl[k] if k < len(gl) else b"<missing>"
        w = wl[k] if k < len(wl) else b"<missing>"
        if g != w:
            print("%s differs at line %d:\n  got  %r\n  want %r" % (name, k + 1, g[:200], w[:200]))
            break
    return False


def main():
    if len(sys.argv) != 5 or sys.argv[4] not in ("complete", "refuse"):
        print(__doc__)
        return 2
    out_p, rc_p, tr_p, mode = sys.argv[1:5]
    w_out, w_tr, w_rc = expected(mode)
    with open(out_p, "rb") as fh:
        g_out = fh.read()
    with open(tr_p, "rb") as fh:
        g_tr = fh.read()
    with open(rc_p, "rb") as fh:
        g_rc = fh.read()
    ok = first_difference("output", g_out, w_out)
    ok = first_difference("trace", g_tr, w_tr) and ok
    ok = first_difference("receipt", g_rc, w_rc) and ok
    if ok:
        print("SMOKE CHECK PASSED (%s): output %d bytes, %d events, receipt equal"
              % (mode, len(g_out), g_tr.count(b"\n")))
        return 0
    print("SMOKE CHECK FAILED (%s)" % mode)
    return 1


if __name__ == "__main__":
    sys.exit(main())

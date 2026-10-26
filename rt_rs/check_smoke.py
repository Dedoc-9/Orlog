"""Check smoke.rs's files (output, trace, receipt) against RUNTIME-SPEC.md, independently.

usage: python -B check_smoke.py DIR    (DIR holds complete.*, chain.*, refute.* written by smoke)

The expected events and their payloads are built here from the spec's encodings (section 5, with
struct, big-endian), the expected values and printed text from src/orlog/numeric_ref.py, and the
chain with hashlib. Nothing is read from orlog_rt.rs. The chain run's trace-head is also compared
with head3 as printed by src/check_chain.py. Every file is compared byte for byte.
"""
import hashlib
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
sys.path.insert(0, SRC)
from orlog import numeric_ref as N  # noqa: E402

LAW = hashlib.sha256(b"law").hexdigest()
TEXT = hashlib.sha256(b"text").hexdigest()
CANON = 0x7FF8000000000000
ODD_NAN = 0x7FF0000000000001     # f_max(1.0, this NaN) is this NaN: 1.0 > NaN is false


def canon_bits(b):
    b &= 0xFFFFFFFFFFFFFFFF
    if (b >> 52) & 0x7FF == 0x7FF and b & ((1 << 52) - 1):
        return CANON
    return b


def u32(v):
    return struct.pack(">I", v)


def u64(v):
    return struct.pack(">Q", v)


def slot(tag, v):
    """A slot's bytes under its tag: I and X 8 bytes, F the canonical bits, B one byte."""
    if tag in "IX":
        return struct.pack(">q", v)
    if tag == "F":
        return u64(canon_bits(v))
    if tag == "B":
        return bytes([1 if v else 0])
    raise ValueError(tag)


def val(tag, v):
    return tag.encode() + slot(tag, v)


def assign(var, tag, v):
    return u32(var) + val(tag, v)


def assign_t(var, t):
    return u32(var) + b"T" + u32(len(t)) + t


def assign_l(var, tag, vs):
    return u32(var) + b"L" + tag.encode() + u32(len(vs)) + b"".join(slot(tag, v) for v in vs)


def item(var, index, tag, v):
    return u32(var) + u64(index) + val(tag, v)


def push(var, tag, v):
    return u32(var) + val(tag, v)


def pop(var, newlen):
    return u32(var) + u64(newlen)


def flag(ident, result):
    return u32(ident) + bytes([1 if result else 0])


def lst(tag, vs):
    """A list printed by its tag (section 3)."""
    def one(v):
        if tag == "I":
            return N.fmt_i(v)
        if tag == "X":
            return N.fmt_x(v)
        if tag == "F":
            return N.fmt_f(N.f_from_bits(v))
        return N.fmt_b(v)
    return "[" + ", ".join(one(v) for v in vs) + "]"


def says(first_clause, lines):
    return [("S", first_clause + i, (line + "\n").encode("utf-8")) for i, line in enumerate(lines)]


def run_complete():
    a = N.i_mul(6, 7)
    one, three = N.x_from_i(1), N.x_from_i(3)
    third = N.x_div(one, three)
    f = N.f_div(1.0, 3.0)
    nan = N.f_sqrt(-1.0)
    xs = [one, third, -(N.ONE // 2)]
    fs = [N.f_bits(0.5), N.f_bits(-0.0), ODD_NAN]
    bs = [1, 0, 1]
    lines = [
        "a = " + N.fmt_i(a),
        "third = %s, min = %s" % (N.fmt_x(third), N.fmt_x(N.I64_MIN)),
        "f = %s, nan = %s, -0 = %s, tiny = %s" % (N.fmt_f(f), N.fmt_f(nan), N.fmt_f(-0.0),
                                                  N.fmt_f(N.f_from_bits(1))),
        "%s %s %s" % (N.fmt_b(a == 42), N.fmt_b(False), "Ørlǫg"),
        " ".join([lst("I", [7, -5, 7]), lst("X", xs), lst("F", fs), lst("B", bs), lst("I", [])]),
        "",
    ]
    events = [
        ("A", 1, assign(0, "I", a)),
        ("A", 2, assign(1, "X", third)),
        ("A", 3, assign(2, "F", N.f_bits(f))),
        ("A", 3, assign(3, "F", N.f_bits(nan))),
        ("A", 3, assign(4, "F", ODD_NAN)),
        ("A", 4, assign(5, "B", a == 42)),
        ("A", 4, assign_t(6, "Ørlǫg".encode("utf-8"))),
        ("A", 5, assign_l(7, "I", [7, -5, 7])),
        ("P", 6, push(7, "I", 9)),
        ("E", 7, item(7, 2, "I", -5)),
        ("Q", 8, pop(7, 3)),
        ("A", 9, assign_l(8, "X", xs)),
        ("A", 9, assign_l(9, "F", fs)),
        ("A", 9, assign_l(10, "B", bs)),
        ("E", 9, item(9, 3, "F", ODD_NAN)),
        ("P", 9, push(10, "B", 0)),
    ] + says(10, lines) + [
        ("C", 20, flag(0, a == 42)),
        ("C", 20, flag(0, third < one)),
        ("M", 16, flag(0, True)),
    ]
    claims = [(20, 2, 2, 7, 31, 6), (21, 0, 0, 0, 0, 0)]
    return events, "COMPLETED", 15, claims


def run_chain():
    events = says(1, ["hello"]) + [
        ("A", 2, assign(0, "I", 42)),
        ("R", 3, b"OVERFLOW"),
    ]
    return events, "REFUSED OVERFLOW 3", 0, [(20, 0, 0, 0, 0, 0), (21, 0, 0, 0, 0, 0)]


def run_refute():
    events = says(1, ["before"]) + [
        ("C", 20, flag(0, True)),
        ("C", 21, flag(1, False)),
        ("R", 21, b"CLAIM-REFUTED"),
    ]
    return events, "REFUSED CLAIM-REFUTED 21", 3, [(20, 1, 1, 1, 2, 3), (21, 1, 0, 9, 30, 2)]


def expected_files(events, status, ops, claims):
    head = hashlib.sha256(b"orlog-trace-0" + bytes.fromhex(LAW)).digest()
    trace = []
    for n, (kind, clause, payload) in enumerate(events, 1):
        head = hashlib.sha256(head + kind.encode() + struct.pack(">II", clause, len(payload)) + payload).digest()
        trace.append("%d %s %d %s %s\n" % (n, kind, clause, payload.hex() if payload else "-", head.hex()))
    out = b"".join(p for k, _, p in events if k == "S")
    receipt = ["orlog-receipt 0", "backend rust", "law-seal " + LAW, "text-seal " + TEXT,
               "status " + status, "output-bytes %d" % len(out),
               "output-sha256 " + hashlib.sha256(out).hexdigest(), "events %d" % len(events),
               "trace-head " + head.hex(), "ops %d" % ops, "claims %d" % len(claims)]
    receipt += ["claim %d %d %d %d %d %d %d" % ((i,) + c) for i, c in enumerate(claims)]
    receipt.append("end")
    return out, "".join(trace).encode("ascii"), ("\n".join(receipt) + "\n").encode("ascii"), head.hex()


def compare(name, got, want):
    if got == want:
        return True
    gl, wl = got.split(b"\n"), want.split(b"\n")
    for i in range(max(len(gl), len(wl))):
        g = gl[i] if i < len(gl) else b"<none>"
        w = wl[i] if i < len(wl) else b"<none>"
        if g != w:
            print("FAIL %s line %d:\n  got  %r\n  want %r" % (name, i + 1, g[:300], w[:300]))
            break
    return False


def check_chain_head3():
    p = subprocess.run([sys.executable, "-B", os.path.join(SRC, "check_chain.py")],
                       capture_output=True, text=True, check=True)
    for line in p.stdout.splitlines():
        if line.startswith("head3 "):
            return line.split()[1]
    raise SystemExit("check_chain.py printed no head3")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    d = sys.argv[1]
    ok = True
    for mode, make in (("complete", run_complete), ("chain", run_chain), ("refute", run_refute)):
        events, status, ops, claims = make()
        out, trace, receipt, head = expected_files(events, status, ops, claims)
        good = True
        for ext, want in (("out", out), ("trace", trace), ("receipt", receipt)):
            with open(os.path.join(d, "%s.%s" % (mode, ext)), "rb") as fh:
                good &= compare("%s.%s" % (mode, ext), fh.read(), want)
        if mode == "chain":
            ref = check_chain_head3()
            if head != ref:
                print("FAIL chain: trace-head %s, check_chain.py head3 %s" % (head, ref))
                good = False
            else:
                print("chain trace-head equals check_chain.py head3 %s" % ref)
        print("%-8s %s (%d events, status %s)" % (mode, "PASS" if good else "FAIL", len(events), status))
        ok &= good
    print("SMOKE CHECK PASSED" if ok else "SMOKE CHECK FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

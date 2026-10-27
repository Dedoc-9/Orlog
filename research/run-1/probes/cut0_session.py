"""EXPERIMENTAL RESEARCH PROBE. It is not the contract, and nothing in the program reads it; the proposal it supports
is research/run-1/CUT-0.md, and its output is evidence/run1-cut0-session.txt.

CUT-0 on the session's side: a settler and reconciler for RUN-1's input boundary, as one transition system.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/cut0_session.py

The session's history is a sequence of events, and S_{n+1} = delta(S_n, e_n) is the only way the state moves:
- arrive(port, bytes): an arrival, numbered in order; the door, a pure function of the port's type and the bytes,
  judges it at once (A2: judge, then assign);
- assign(arrival, tick): the host puts an accepted arrival into the open tick, at most one per (tick, port);
- drop(arrival): the host declines an accepted arrival it will not assign;
- close(): the host closes the open tick. It runs only if every each-tick port holds an accepted arrival; otherwise it
  does not run, and the session ends NOT-RUN with the first missing port in declaration order;
- end(): the host ends the session normally, legal only when the open tick holds no assignment (END-PENDING) and every
  accepted arrival is assigned or dropped (END-UNDISPOSED). A tick that has begun to fill is closed, never discarded.
Any other move is illegal, and the verifier names the rule it breaks.

Three records, bound to one another:
- the input log, the history's projection, parsed by a strict canonical grammar (one byte form, or a named refusal);
- the receipt's core, a function of the input log alone: two histories with one input log share it (law-equivalence);
- the session record, `orlog-session 0`, binding the history's digest, the input log's digest and the core's digest
  (session provenance). A receipt attests a run over its input log; only a session record attests a session.

The execution is a stand-in law, not Orlog's: a prefix of 3 counted operations, then per tick 2 + a's integer part
operations, under `at most 5 operations`; an a of 13 refuses at its tick's second operation, an operation counted that
does not complete. It exists to check the reconciliation of 'T', the tick lines and the receipt.

Checked: named cases; every legal history of one port up to a declared depth (exhaustive over that finite domain);
named malformed logs, each refused with its code; every single-byte mutation of every distinct valid log of that
domain, each refused or accepted only if it is itself canonical; and plants, each caught by its own case.
"""
import hashlib
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.numeric_ref import I64_MAX, I64_MIN                  # noqa: E402

ONE = 1 << 32
PLANT = None    # "assign-refused", "hold-previous", "no-cause", "overwrite", "budget-uncounted", "end-anytime",
                # "lenient-hex", "after-end", "record-without-history", and from the manifold adversary's G-findings
                # (research/run-1/manifold/ADVERSARY.md): "no-source", "close-after-refusal", "door-dollar",
                # "a1-cause-under-a2"
POLICY = "A2"   # "A1": the host assigns before the door judges, and a refused assignment blocks its tick
PREFIX_OPS, BUDGET = 3, 5
CAUSES = ("INPUT-MISSING", "INPUT-REFUSED")   # INPUT-REFUSED is A1's alone (G3): under A2 the grammar refuses it


# ------------------------------------------------------------------ the door (CONTRACT-DRAFT.md §1.3, fixed ports)
FIXED = re.compile(r"^-?[0-9]+(\.[0-9]+)?$")


def door(raw):
    """('ok', raw value) or ('refused', code, detail): range before grid (the debate's D7)."""
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        return ("refused", "INPUT-SYNTAX", "")
    if not (FIXED.match(text) if PLANT == "door-dollar" else FIXED.fullmatch(text)):   # G2: $ matched before LF
        return ("refused", "INPUT-SYNTAX", "")
    r = Fraction(text) * ONE
    if r < I64_MIN or r > I64_MAX:
        return ("refused", "INPUT-RANGE", str(I64_MIN if r < I64_MIN else I64_MAX))
    if r.denominator != 1:
        lo = r.numerator // r.denominator
        return ("refused", "INPUT-GRID", "%d %d" % (lo, lo + 1))
    return ("ok", int(r))


# ------------------------------------------------------------------ the transition system
class Illegal(Exception):
    pass


class Session:
    def __init__(self, ports):
        self.ports = ports                      # each-tick ports, in declaration order
        self.arrivals = []                      # (port, bytes, door result)
        self.sources = []                       # each arrival's source label (G5: the history names who sent it)
        self.disposed = {}                      # arrival index -> ("assigned", t) or ("dropped",)
        self.slots = {}                         # port -> arrival index, for the open tick
        self.tick = 1                           # the open tick
        self.records = []                       # the ticks that will run: raw values in port order
        self.outcome = None                     # None (open), ("closed",), ("not-run", t, cause, port)
        self.refused = None                     # the tick whose run refused (G6: a live session runs each tick it closes)

    def step(self, e):
        if self.outcome is not None:
            raise Illegal("AFTER-END")
        kind = e[0]
        if self.refused is not None and kind != "end" and PLANT != "close-after-refusal":
            raise Illegal("RUN-REFUSED")                          # nothing after the run refused but the end (G6)
        if kind == "arrive":
            _, port, source, raw = e if len(e) == 4 else (e[0], e[1], "src", e[2])
            if port not in self.ports:
                raise Illegal("UNKNOWN-PORT")
            self.arrivals.append((port, raw, door(raw)))
            self.sources.append(source)
        elif kind in ("assign", "drop"):
            i = e[1]
            if not 0 <= i < len(self.arrivals):
                raise Illegal("NO-ARRIVAL")
            port, _, result = self.arrivals[i]
            if result[0] != "ok" and (kind == "drop" or (POLICY == "A2" and PLANT != "assign-refused")):
                raise Illegal("ASSIGN-REFUSED" if kind == "assign" else "DROP-REFUSED")
            if i in self.disposed:
                raise Illegal("DISPOSED-TWICE")
            if kind == "drop":
                self.disposed[i] = ("dropped",)
                return
            tick = e[2]
            if tick != self.tick:
                raise Illegal("ASSIGN-CLOSED" if tick < self.tick else "ASSIGN-AHEAD")
            if port in self.slots and PLANT != "overwrite":
                raise Illegal("SLOT-FILLED")
            self.slots[port] = i
            self.disposed[i] = ("assigned", tick)
        elif kind == "close":
            values = []
            for p in self.ports:
                i = self.slots.get(p)
                result = self.arrivals[i][2] if i is not None else None
                if result is not None and result[0] == "ok":
                    values.append(result[1])
                elif result is not None and PLANT == "assign-refused":
                    values.append(0)                              # the plant invents a value
                elif result is not None:                          # A1: a refused arrival was assigned
                    self.outcome = ("not-run", self.tick, "INPUT-REFUSED", p)
                    return
                elif PLANT == "hold-previous" and self.records:
                    values.append(self.records[-1][len(values)])
                else:
                    self.outcome = ("not-run", self.tick, "INPUT-MISSING", p)
                    return
            self.records.append(values)
            self.tick += 1
            self.slots = {}
            if execute(serialize(self.ports, self.records, None), self.ports)["status"].startswith("REFUSED"):
                self.refused = self.tick - 1
        elif kind == "end":
            if PLANT != "end-anytime" and self.refused is None:
                if self.slots:
                    raise Illegal("END-PENDING")
                if any(r[0] == "ok" and i not in self.disposed for i, (_, _, r) in enumerate(self.arrivals)):
                    raise Illegal("END-UNDISPOSED")
            self.outcome = ("closed",)
        else:
            raise Illegal("UNKNOWN-EVENT")

    def legal_moves(self, values):
        if self.outcome is not None:
            return []
        if self.refused is not None:
            return [("end",)]
        free = [i for i, (_, _, r) in enumerate(self.arrivals) if r[0] == "ok" and i not in self.disposed]
        moves = [("arrive", p, v) for p in self.ports for v in values]
        moves += [("assign", i, self.tick) for i in free if self.arrivals[i][0] not in self.slots]
        moves += [("drop", i) for i in free]
        moves.append(("close",))
        if PLANT == "end-anytime" or (not self.slots and not free):
            moves.append(("end",))
        return moves

    def dispositions(self):
        """Each arrival's one disposition, derived from the history alone."""
        out = []
        for i, (_, _, r) in enumerate(self.arrivals):
            if r[0] != "ok":
                out.append("refused %s" % r[1])
            elif i in self.disposed:
                d = self.disposed[i]
                out.append("assigned %d" % d[1] if d[0] == "assigned" else "dropped")
            else:
                out.append("open" if self.outcome is None and self.refused is None else
                           "unconsumed (the session ended)")
        return out


def settle(history, ports):
    s = Session(ports)
    for e in history:
        s.step(e)
    return s


# ------------------------------------------------------------------ the input log: one byte form, or a named refusal
def port_signature(ports):
    return hashlib.sha256(b"orlog-ports 0\n" + b"".join(b'(port "%s" fix each-tick)\n' % p.encode()
                                                          for p in ports)).hexdigest()


class Malformed(Exception):
    pass


def serialize(ports, records, end):
    """The canonical bytes of an input log: the only form parse_log accepts."""
    out = [b"orlog-inputs 0\n", b"ports %s\n" % port_signature(ports).encode(), b"door door-0\n"]
    for t, vals in enumerate(records, 1):
        out.append(b"t %d%s\n" % (t, b"".join(b" %016x" % (v & (2 ** 64 - 1)) for v in vals)))   # G1: no port
    if end is not None and PLANT == "no-cause":
        out.append(b"end %d\n" % len(records))
    elif end == ("closed",):
        out.append(b"end %d closed\n" % len(records))
    elif end is not None:
        _, t, cause, port = end
        out.append(b"end %d not-run %d %s %s\n" % (len(records), t, cause.encode(), port.encode()))
    return b"".join(out)


def input_log(s):
    """CONTRACT-DRAFT.md §2 with Round B's hex values: the history's projection, the only thing the law reads."""
    return serialize(s.ports, s.records, s.outcome)


DEC = re.compile(r"^(0|[1-9][0-9]*)$")
HEX16 = re.compile(r"^[0-9a-f]{16}$")


def parse_log(b, ports):
    """(records, end) from an input log's bytes, or Malformed with its code. The grammar is serialize's, exactly."""
    try:
        text = b.decode("ascii")
    except UnicodeDecodeError:
        raise Malformed("LOG-NOT-ASCII")
    if "\r" in text or not text.endswith("\n") or "\n\n" in text:
        raise Malformed("LOG-LINE")
    lines = text[:-1].split("\n")
    if lines[:1] != ["orlog-inputs 0"] or len(lines) < 3 or lines[2] != "door door-0":
        raise Malformed("LOG-HEADER")
    if not re.fullmatch(r"ports [0-9a-f]{64}", lines[1]):
        raise Malformed("LOG-HEADER")
    if lines[1][6:] != port_signature(ports):
        raise Malformed("PORT-SIGNATURE")
    records, end = [], None
    for line in lines[3:]:
        f = line.split(" ")
        if end is not None and PLANT != "after-end":
            raise Malformed("LOG-AFTER-END")
        if f[0] == "t":
            if len(f) != 2 + len(ports):
                raise Malformed("LOG-RECORD")
            if not DEC.fullmatch(f[1]) or int(f[1]) != len(records) + 1:
                raise Malformed("LOG-TICK")
            vals = []
            for h in f[2:]:
                if not HEX16.fullmatch(h) and not (PLANT == "lenient-hex" and re.fullmatch(r"[0-9a-fA-F]{16}", h)):
                    raise Malformed("LOG-RECORD")
                v = int(h, 16)
                vals.append(v - 2 ** 64 if v >= 2 ** 63 else v)
            records.append(vals)
        elif f[0] == "end":
            if len(f) < 3 or not DEC.fullmatch(f[1]) or int(f[1]) != len(records):
                raise Malformed("LOG-END")
            if f[2:] == ["closed"]:
                end = ("closed",)
            elif (len(f) == 6 and f[2] == "not-run" and DEC.fullmatch(f[3]) and int(f[3]) == len(records) + 1
                  and f[4] in (CAUSES if POLICY == "A1" or PLANT == "a1-cause-under-a2" else CAUSES[:1])
                  and f[5] in ports):
                end = ("not-run", int(f[3]), f[4], f[5])
            else:
                raise Malformed("LOG-END")
        else:
            raise Malformed("LOG-UNKNOWN")
    return records, end


# ------------------------------------------------------------------ the stand-in law, its receipt, the session record
def execute(log, ports):
    """The receipt's core fields, the 'T' events and the tick lines, from the input log alone."""
    records, end = parse_log(log, ports)
    c, executed, T, lines = PREFIX_OPS, PREFIX_OPS, [], []
    status = None
    for t, vals in enumerate(records, 1):
        T.append((t, c))
        a = vals[0] >> 32 if vals else 0
        work, refuse_at = 2 + a, (2 if a == 13 else None)
        tc = 0
        for op in range(1, work + 1):
            if tc + 1 == BUDGET + 1 and PLANT == "budget-uncounted":
                status = "REFUSED TICK-BUDGET"
                break
            tc += 1
            c += 1                                            # counted immediately before the operation (SPEC §7)
            if tc == BUDGET + 1:
                status = "REFUSED TICK-BUDGET"                # counted, refused before it executes
                break
            if op == refuse_at:
                status = "REFUSED OVERFLOW"                    # counted, and does not complete
                break
            executed += 1
        if status:
            break
        lines.append((t, tc))
    if status is None:
        if end is None:
            status = "LOG-OPEN"
        elif end == ("closed",):
            status = "COMPLETED"
        else:
            status = "NOT-RUN %d %s %s" % end[1:]
    tick_ops = c - T[-1][1] if T else 0
    core = "orlog-receipt 1\nstatus %s\nticks %d\nops %d\ntick-ops %d\ninput-log-sha256 %s\nend\n" % (
        status, len(T), c, tick_ops, hashlib.sha256(log).hexdigest())
    return {"status": status, "ticks": len(T), "ops": c, "executed": executed, "tick_ops": tick_ops, "T": T,
            "lines": lines, "core": core.encode(), "end": end}


def history_bytes(history):
    out = [b"orlog-history 0\n"]
    for e in history:
        if e[0] == "arrive":
            port, source, raw = (e[1], e[2], e[3]) if len(e) == 4 else (e[1], "src", e[2])
            if PLANT == "no-source":
                out.append(b"arrive %s %s\n" % (port.encode(), raw.hex().encode()))
            else:
                out.append(b"arrive %s %s %s\n" % (port.encode(), source.encode().hex().encode(), raw.hex().encode()))
        elif e[0] == "assign":
            out.append(b"assign %d %d\n" % (e[1], e[2]))
        elif e[0] == "drop":
            out.append(b"drop %d\n" % e[1])
        else:
            out.append(e[0].encode() + b"\n")
    return b"".join(out)


def session_record(history, ports):
    log = input_log(settle(history, ports))
    core = execute(log, ports)["core"]
    lines = [b"orlog-session 0\n"]
    if PLANT != "record-without-history":
        lines.append(b"history-sha256 %s\n" % hashlib.sha256(history_bytes(history)).hexdigest().encode())
    lines += [b"input-log-sha256 %s\n" % hashlib.sha256(log).hexdigest().encode(),
              b"receipt-core-sha256 %s\n" % hashlib.sha256(core).hexdigest().encode(), b"end\n"]
    return b"".join(lines)


def verify_session(history, log, core, record, ports):
    """BOUND, or the first link that fails: the history is legal, the log is its projection, the core is the log's,
    and the record names all three."""
    try:
        s = settle(history, ports)
    except Illegal as e:
        return "HISTORY-ILLEGAL %s" % e
    if input_log(s) != log:
        return "HISTORY-MISMATCH"
    try:
        if execute(log, ports)["core"] != core:
            return "CORE-MISMATCH"
    except Malformed as e:
        return "LOG-MALFORMED %s" % e
    return "BOUND" if session_record(history, ports) == record else "SESSION-MISMATCH"


def predicates(r):
    """The four statuses, each from facts of the run alone; exactly one must hold."""
    refused = r["status"].startswith("REFUSED")
    return {"REFUSED": refused,
            "LOG-OPEN": not refused and r["end"] is None,
            "COMPLETED": not refused and r["end"] == ("closed",),
            "NOT-RUN": not refused and r["end"] is not None and r["end"][0] == "not-run"}


def check_run(history, ports):
    """The rows every legal history must pass; returns the names of the rows it fails."""
    s = settle(history, ports)
    log = input_log(s)
    fails = []
    if input_log(settle(history, ports)) != log:
        fails.append("projection-is-a-function")
    try:
        if serialize(ports, *parse_log(log, ports)) != log:
            fails.append("log-round-trips")
    except Malformed:
        fails.append("projection-parses")
        return fails
    for port, raw, result in s.arrivals:
        if door(raw) != result:
            fails.append("door-replays")
    for e in history:                     # no assignment disappears: its tick ran, did not run, or is still open
        if e[0] == "assign" and not (e[2] <= len(s.records)
                                     or (s.outcome and s.outcome[0] == "not-run" and s.outcome[1] == e[2])
                                     or (s.outcome is None and e[2] == s.tick)):
            fails.append("no-assignment-disappears")
    if len(s.dispositions()) != len(s.arrivals):
        fails.append("one-disposition-each")
    assigned = {}                         # no value invented: each value is its (tick, port)'s accepted arrival's
    for e in history:
        if e[0] == "assign":
            assigned[(e[2], s.arrivals[e[1]][0])] = e[1]
    for t, vals in enumerate(s.records, 1):
        if any(assigned.get((t, p)) is None or s.arrivals[assigned[(t, p)]][2] != ("ok", v)
               for p, v in zip(ports, vals)):
            fails.append("no-value-invented")
            break
    r = execute(log, ports)
    if execute(log, ports)["core"] != r["core"]:
        fails.append("execution-is-a-function")
    held = [k for k, v in predicates(r).items() if v]
    if len(held) != 1 or not r["status"].startswith(held[0]):
        fails.append("statuses-partition")
    T, lines = r["T"], r["lines"]
    if T and T[0][1] != PREFIX_OPS:
        fails.append("T1-is-the-prefix")
    for (t, c), (t2, c2), (lt, lops) in zip(T, T[1:], lines):
        if c2 - c != lops:
            fails.append("T-differences-are-the-lines")
    if T and r["ops"] - T[-1][1] != r["tick_ops"]:
        fails.append("ops-minus-last-T-is-tick-ops")
    if not T and r["ops"] != PREFIX_OPS:
        fails.append("no-T-ops-is-the-prefix")
    if r["status"] == "REFUSED TICK-BUDGET" and r["tick_ops"] != BUDGET + 1:
        fails.append("budget-tick-counts-N+1")
    if r["executed"] != r["ops"] - (1 if r["status"].startswith("REFUSED") else 0):
        fails.append("executed-is-counted-less-the-refused")
    rec = session_record(history, ports)
    if verify_session(history, log, r["core"], rec, ports) != "BOUND":
        fails.append("session-binds")
    return fails


# ------------------------------------------------------------------ the named cases
A, AB = ["a"], ["a", "b"]
B = lambda s: s.encode()                                          # noqa: E731
CASES = [
    # (name, ports, history, expected status or the illegal rule, the plant this case must catch)
    ("S1 an invalid input, then a valid retry for the same tick", A,
     [("arrive", "a", B("1.1")), ("arrive", "a", B("1")), ("assign", 1, 1), ("close",), ("end",)],
     "COMPLETED", None),
    ("S1' a history that assigns the refused arrival itself", A,
     [("arrive", "a", B("1.1")), ("assign", 0, 1), ("close",), ("end",)],
     "illegal ASSIGN-REFUSED", "assign-refused"),
    ("S2 an invalid input and no retry", A, [("arrive", "a", B("1.1")), ("close",)],
     "NOT-RUN 1 INPUT-MISSING a", None),
    ("S2' a valid tick, then an invalid input and no retry", A,
     [("arrive", "a", B("1")), ("assign", 0, 1), ("close",), ("arrive", "a", B("1.1")), ("close",)],
     "NOT-RUN 2 INPUT-MISSING a", "hold-previous"),
    ("S3 one invalid and one valid input for one tick", AB,
     [("arrive", "a", B("1.1")), ("arrive", "b", B("1")), ("assign", 1, 1), ("close",)],
     "NOT-RUN 1 INPUT-MISSING a", None),
    ("S4 two arrivals for one port and one tick", A,
     [("arrive", "a", B("1")), ("arrive", "a", B("4")), ("assign", 0, 1), ("assign", 1, 1)],
     "illegal SLOT-FILLED", "overwrite"),
    ("S5 a retry after the host closed its tick", A,
     [("arrive", "a", B("1")), ("assign", 0, 1), ("close",), ("arrive", "a", B("4")), ("assign", 1, 1)],
     "illegal ASSIGN-CLOSED", None),
    ("S7 the budget: a tick of 6 operations under at most 5", A,
     [("arrive", "a", B("4")), ("assign", 0, 1), ("close",), ("end",)],
     "REFUSED TICK-BUDGET tick-ops 6", "budget-uncounted"),
    ("S8 the loophole: a tick begun (one of two ports assigned), then end", AB,
     [("arrive", "a", B("1")), ("assign", 0, 1), ("end",)],
     "illegal END-PENDING", "end-anytime"),
    ("S9 an accepted arrival neither assigned nor dropped, then end", A,
     [("arrive", "a", B("1")), ("end",)],
     "illegal END-UNDISPOSED", None),
    ("S10 the same arrival dropped, then end", A,
     [("arrive", "a", B("1")), ("drop", 0), ("end",)],
     "COMPLETED", None),
    ("S11 a tick whose run refuses, then a close: nothing after the refusal but the end (G6)", A,
     [("arrive", "a", B("13")), ("assign", 0, 1), ("close",), ("close",)],
     "illegal RUN-REFUSED", "close-after-refusal"),
    ("S12 a law with no each-tick port: two ticks, then end (G1)", [],
     [("close",), ("close",), ("end",)],
     "COMPLETED", None),
]

# Malformed logs, each from the canonical log of two ticks and a closed end, with the code it must be refused with.
SIG = port_signature(A)
GOOD = (b"orlog-inputs 0\nports " + SIG.encode() + b"\ndoor door-0\n"
        b"t 1 0000000100000000\nt 2 0000000200000000\nend 2 closed\n")
MALFORMED = [
    ("a duplicated end record", GOOD + b"end 2 closed\n", "LOG-AFTER-END", "after-end"),
    ("a record after the end", GOOD + b"t 3 0000000300000000\n", "LOG-AFTER-END", "after-end"),
    ("too few values", GOOD.replace(b"t 2 0000000200000000", b"t 2"), "LOG-RECORD", None),
    ("too many values", GOOD.replace(b"t 2 0000000200000000", b"t 2 0000000200000000 0000000200000000"),
     "LOG-RECORD", None),
    ("upper-case hex", GOOD.replace(b"0000000200000000", b"000000020000000A"), "LOG-RECORD", "lenient-hex"),
    ("short hex", GOOD.replace(b"0000000200000000", b"200000000"), "LOG-RECORD", None),
    ("not hex", GOOD.replace(b"0000000200000000", b"000000020000000g"), "LOG-RECORD", None),
    ("a tick number skipped", GOOD.replace(b"t 2 ", b"t 3 "), "LOG-TICK", None),
    ("a tick number repeated", GOOD.replace(b"t 2 ", b"t 1 "), "LOG-TICK", None),
    ("ticks from 0", GOOD.replace(b"t 1 ", b"t 0 ").replace(b"t 2 ", b"t 1 "), "LOG-TICK", None),
    ("a tick number with a leading zero", GOOD.replace(b"t 2 ", b"t 02 "), "LOG-TICK", None),
    ("an end count that is not the records'", GOOD.replace(b"end 2 closed", b"end 3 closed"), "LOG-END", None),
    ("a not-run tick that is not the next", GOOD.replace(b"end 2 closed", b"end 2 not-run 4 INPUT-MISSING a"),
     "LOG-END", None),
    ("an unknown cause", GOOD.replace(b"end 2 closed", b"end 2 not-run 3 INPUT-LATE a"), "LOG-END", None),
    ("an undeclared port", GOOD.replace(b"end 2 closed", b"end 2 not-run 3 INPUT-MISSING q"), "LOG-END", None),
    ("an end record without its cause", GOOD.replace(b"end 2 closed", b"end 2"), "LOG-END", None),
    ("CR LF line ends", GOOD.replace(b"\n", b"\r\n"), "LOG-LINE", None),
    ("no final line end", GOOD[:-1], "LOG-LINE", None),
    ("an empty line", GOOD.replace(b"t 2 ", b"\nt 2 "), "LOG-LINE", None),
    ("a trailing space", GOOD.replace(b"end 2 closed", b"end 2 closed "), "LOG-END", None),
    ("an unknown record kind", GOOD.replace(b"end 2 closed", b"note hello"), "LOG-UNKNOWN", None),
    ("another header version", GOOD.replace(b"orlog-inputs 0", b"orlog-inputs 1"), "LOG-HEADER", None),
    ("another port signature", GOOD.replace(SIG.encode(), port_signature(["b"]).encode()), "PORT-SIGNATURE", None),
    ("a non-ASCII byte", GOOD.replace(b"door door-0", b"door door-\xc3\xb8"), "LOG-NOT-ASCII", None),
    ("an A1-only cause under A2 (G3)", GOOD.replace(b"end 2 closed", b"end 2 not-run 3 INPUT-REFUSED a"), "LOG-END",
     "a1-cause-under-a2"),
]
OPEN_LOG = ("no end record: an open log, parsed, never refused", GOOD.replace(b"end 2 closed\n", b""))


def outcome_of(history, ports):
    try:
        s = settle(history, ports)
    except Illegal as e:
        return "illegal %s" % e
    try:
        r = execute(input_log(s), ports)
    except Malformed as e:
        return "its own projection refused %s" % e
    return r["status"] + (" tick-ops %d" % r["tick_ops"] if r["status"] == "REFUSED TICK-BUDGET" else "")


def refusal_of(b, ports=A):
    try:
        parse_log(b, ports)
    except Malformed as e:
        return str(e)
    return "ACCEPTED"


def run_cases():
    rows = []
    for name, ports, hist, want, _ in CASES:
        got = outcome_of(hist, ports)
        rows.append((name, got == want, "%s (expected %s)" % (got, want)))
    h1 = [("arrive", "a", B("1")), ("arrive", "a", B("2")), ("assign", 0, 1), ("close",), ("assign", 1, 2),
          ("close",), ("end",)]
    h2 = [("arrive", "a", B("1")), ("arrive", "a", B("2")), ("assign", 1, 1), ("close",), ("assign", 0, 2),
          ("close",), ("end",)]
    l1, l2 = input_log(settle(h1, A)), input_log(settle(h2, A))
    c1 = execute(l1, A)["core"]
    ok_pair = verify_session(h1, l1, c1, session_record(h1, A), A)
    bad_pair = verify_session(h1, l2, execute(l2, A)["core"], session_record(h2, A), A)
    rows.append(("S6 one set of arrivals, two schedules: two input logs, each bound to its history",
                 l1 != l2 and ok_pair == "BOUND" and bad_pair == "HISTORY-MISMATCH",
                 "logs %s; history 1 bound to its own: %s; to the other's: %s" % (
                     "differ" if l1 != l2 else "EQUAL", ok_pair, bad_pair)))
    global POLICY
    hostile = [("arrive", "a", B("1.1")), ("assign", 0, 1), ("close",)]
    POLICY = "A1"
    a1 = outcome_of(hostile, A)
    POLICY = "A2"
    a2 = outcome_of([("arrive", "a", B("1.1")), ("arrive", "a", B("1")), ("assign", 1, 1), ("close",), ("end",)], A)
    rows.append(("H  a hostile client's malformed message: A1 ends the session, A2 refuses only the message",
                 a1 == "NOT-RUN 1 INPUT-REFUSED a" and a2 == "COMPLETED" and outcome_of(hostile, A)
                 == "illegal ASSIGN-REFUSED", "A1 %s; A2 %s" % (a1, a2)))
    ha = [("arrive", "a", B("1")), ("assign", 0, 1), ("close",), ("end",)]
    hb = [("arrive", "a", B("1.1")), ("arrive", "a", B("1")), ("assign", 1, 1), ("close",), ("end",)]
    la, lb = input_log(settle(ha, A)), input_log(settle(hb, A))
    ca, cb = execute(la, A)["core"], execute(lb, A)["core"]
    ra, rb = session_record(ha, A), session_record(hb, A)
    crossed = verify_session(ha, la, ca, rb, A)
    rows.append(("X  one input log, two histories: one receipt core (law-equivalence), two session records "
                 "(provenance)", la == lb and ca == cb and ra != rb and crossed == "SESSION-MISMATCH",
                 "logs %s, cores %s, session records %s; history a with b's record: %s" % (
                     "equal" if la == lb else "DIFFER", "equal" if ca == cb else "DIFFER",
                     "differ" if ra != rb else "EQUAL", crossed)))
    hc = [("arrive", "a", B("1")), ("assign", 0, 1), ("close",), ("end",)]
    hn = [("arrive", "a", B("1")), ("assign", 0, 1), ("close",), ("close",)]
    lc, ln = input_log(settle(hc, A)), input_log(settle(hn, A))
    sc, sn = outcome_of(hc, A), outcome_of(hn, A)
    rows.append(("A3 closed after tick 1, or tick 2 not run: the end record tells them apart",
                 lc != ln and sc != sn, "%s / %s" % (sc, sn)))
    for name, b, want, _ in MALFORMED:
        got = refusal_of(b)
        rows.append(("M  " + name, got == want, "%s (expected %s)" % (got, want)))
    got = refusal_of(OPEN_LOG[1])
    rows.append(("M  " + OPEN_LOG[0], got == "ACCEPTED" and execute(OPEN_LOG[1], A)["status"] == "LOG-OPEN", got))
    d = door(b"1\n")
    rows.append(("D  the door refuses a value with a trailing line end (G2)", d[0] == "refused", repr(d)))
    hal = [("arrive", "a", "alice", B("1")), ("assign", 0, 1), ("close",), ("end",)]
    hma = [("arrive", "a", "mallory", B("1")), ("assign", 0, 1), ("close",), ("end",)]
    ral, rma = session_record(hal, A), session_record(hma, A)
    same_core = execute(input_log(settle(hal, A)), A)["core"] == execute(input_log(settle(hma, A)), A)["core"]
    rows.append(("G5 alice's 1 and mallory's 1: one receipt core, two session records", same_core and ral != rma,
                 "cores %s, session records %s" % ("equal" if same_core else "DIFFER",
                                                   "differ" if ral != rma else "EQUAL")))
    return rows


def exhaustive(depth, values, ports=None):
    """Every legal history of the ports up to depth events; returns (count, failed rows, the distinct logs)."""
    ports = A if ports is None else ports
    n, failed, logs = 0, {}, set()
    stack = [[]]
    while stack:
        h = stack.pop()
        n += 1
        for f in check_run(h, ports):
            failed[f] = failed.get(f, 0) + 1
        logs.add(input_log(settle(h, ports)))
        if len(h) < depth:
            for m in settle(h, ports).legal_moves(values):
                stack.append(h + [m])
    return n, failed, logs


def mutations(logs):
    """Every single-byte change of every log (a replacement by one of 8 bytes, a deletion, a duplication): each must be
    refused, or accepted only if it is itself the canonical form of what it parses to."""
    tried = refused = accepted = noncanonical = 0
    for log in sorted(logs):
        for i in range(len(log)):
            variants = [log[:i] + bytes([c]) + log[i + 1:] for c in b" \n0fFg-\r" if c != log[i]]
            variants += [log[:i] + log[i + 1:], log[:i] + log[i:i + 1] + log[i:]]
            for v in variants:
                tried += 1
                try:
                    parsed = parse_log(v, A)
                except Malformed:
                    refused += 1
                    continue
                accepted += 1
                if serialize(A, *parsed) != v:
                    noncanonical += 1
    return tried, refused, accepted, noncanonical


def main():
    global PLANT
    depth = 6
    values = [B("1"), B("1.1"), B("4"), B("13")]
    print("== the named cases (policy A2 unless said)")
    rows = run_cases()
    for name, ok, detail in rows:
        print("  %s %s\n     %s" % ("PASS" if ok else "FAIL", name, detail))
    n, failed, logs = exhaustive(depth, values)
    print("== every legal history of one port up to %d events, arrivals among %s" % (
        depth, ", ".join(v.decode() for v in values)))
    print("  histories %d, distinct input logs %d; rows failed: %s" % (
        n, len(logs), ", ".join("%s %d" % kv for kv in sorted(failed.items())) or "none"))
    for ports, d in (([], 6), (AB, 4)):
        n2, failed2, logs2 = exhaustive(d, values, ports)
        print("== every legal history of %s up to %d events: histories %d, distinct input logs %d; rows failed: %s" % (
            "no each-tick port" if not ports else "%d ports" % len(ports), d, n2, len(logs2),
            ", ".join("%s %d" % kv for kv in sorted(failed2.items())) or "none"))
        n += n2
        for k, v in failed2.items():
            failed[k] = failed.get(k, 0) + v
    tried, refused, accepted, noncanonical = mutations(logs)
    print("== every single-byte mutation of those %d logs" % len(logs))
    print("  tried %d: refused %d, accepted %d (each a canonical log of its own: %d not canonical)" % (
        tried, refused, accepted, noncanonical))
    print("== plants, each read on the case that must catch it")
    caught = 0
    plants = [("assign-refused", "S1'"), ("hold-previous", "S2'"), ("overwrite", "S4"), ("budget-uncounted", "S7"),
              ("end-anytime", "S8"), ("no-cause", "A3"), ("lenient-hex", "M  upper-case hex"),
              ("after-end", "M  a duplicated end record"), ("record-without-history", "X"),
              ("close-after-refusal", "S11"), ("door-dollar", "D "), ("no-source", "G5"),
              ("a1-cause-under-a2", "M  an A1-only cause under A2")]
    for plant, case in plants:
        PLANT = plant
        try:
            hit = not all(ok for name, ok, _ in run_cases() if name.startswith(case))
        except Malformed:                                     # the plant's own log is refused by the strict parser
            hit = True
        if plant == "end-anytime":                             # and the exhaustive search must find the loophole
            hit = hit and bool(exhaustive(4, values)[1].get("no-assignment-disappears"))
        if plant == "hold-previous":                           # and the exhaustive search must find the invention
            hit = hit and bool(exhaustive(4, values)[1].get("no-value-invented"))
        PLANT = None
        caught += bool(hit)
        print("  plant %-23s on %-28s %s" % (plant, case, "caught" if hit else "NOT CAUGHT"))
    ok = all(r[1] for r in rows) and not failed and noncanonical == 0 and caught == len(plants)
    print("CUT-0 SESSION %s: %d of %d cases, %d legal histories with no row failed, %d mutations with no "
          "non-canonical log accepted, plants %d/%d" % (
              "HELD" if ok else "FAILED", sum(r[1] for r in rows), len(rows), n, tried, caught, len(plants)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

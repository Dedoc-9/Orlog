"""The reference interpreter: the typed AST, walked, by definition.

This is the declared authority on a mismatch (the de Bruijn criterion: a small, readable
definition, not the fast path). It shares the front end with the backends (parsing, typing,
ids) but not the lowering: it evaluates the tree directly, left to right, with numbers
computed by numeric_ref over exact rationals. The compiled backends lower the same tree to
three-address code and compute with bit-level algorithms; the arbiter holds them to this.

Authority is DECLARED, not proven: if this interpreter is wrong and the three backends agree,
the arbiter still prefers it, and says so (REFERENCE-DISSENT). Integrity is not truth.
"""
import hashlib
import struct

from . import numeric_ref as N
from .seal import seal_words
from .syntax import (Num, Str, BoolLit, Var, Bin, Un, Conv, Item, Length, ListOf, ListLit, Seal, Cat,
                     Let, SetS, Change, Say, IfS, While, For, ProcDef, Perform, Must, Claim, Define, Append,
                     RemoveLast, Decimals, BLOCK)

TAG = {"int": b"I", "fix": b"X", "float": b"F", "bool": b"B"}
OUTPUT_MAX = 1 << 30


class Stop(Exception):
    def __init__(self, code, clause):
        Exception.__init__(self, code)
        self.code, self.clause = code, clause


class HostStop(Exception):
    """The host's budget of counted operations ran out. Not a refusal: the law said nothing, so there is no receipt
    and no event. Checked at every statement's entry, and no statement runs unbounded (expressions and rules hold no
    loops, and a loop's body is never empty), so a stop comes at the first statement past the budget, the same on
    every host (the use-case review found that nothing bounded a run, 2026-10-25)."""

    def __init__(self, ops, budget):
        Exception.__init__(self, "STOPPED-BY-HOST after %d counted operations (budget %d)" % (ops, budget))
        self.ops, self.budget = ops, budget


def enc_slot(v, t):
    if t in ("int", "fix"):
        return struct.pack(">q", v)
    if t == "float":
        return struct.pack(">Q", N.f_bits(N.f_canon(v)))
    return bytes([1 if v else 0])


def enc_value(v, t):
    if isinstance(t, tuple):
        e = t[1]
        return b"L" + TAG[e] + struct.pack(">I", len(v)) + b"".join(enc_slot(x, e) for x in v)
    if t == "text":
        return b"T" + struct.pack(">I", len(v)) + v
    return TAG[t] + enc_slot(v, t)


def fmt(v, t):
    if isinstance(t, tuple):
        return b"[" + b", ".join(fmt(x, t[1]) for x in v) + b"]"
    if t == "int":
        return N.fmt_i(v).encode("ascii")
    if t == "fix":
        return N.fmt_x(v).encode("ascii")
    if t == "float":
        return N.fmt_f(v).encode("ascii")
    if t == "bool":
        return N.fmt_b(v).encode("ascii")
    return v


def receipt_text(backend, law_hex, text_hex, status, out_len, out_sha, events, head, ops, claims, claim_clauses):
    lines = ["orlog-receipt 0", "backend " + backend, "law-seal " + law_hex, "text-seal " + text_hex,
             "status " + status, "output-bytes %d" % out_len, "output-sha256 " + out_sha,
             "events %d" % events, "trace-head " + head, "ops %d" % ops, "claims %d" % len(claim_clauses)]
    for i, cl in enumerate(claim_clauses):
        ev, tr, cost, rc, rcost = claims[i]
        lines.append("claim %d %d %d %d %d %d %d" % (i, cl, ev, tr, cost, rc, rcost))
    lines.append("end")
    return ("\n".join(lines) + "\n").encode("ascii")


class Interp:
    def __init__(self, prog, an, law_hex, text_hex, trace=False, budget=None):
        self.prog, self.an = prog, an
        self.law_hex, self.text_hex = law_hex, text_hex
        self.budget = budget
        self.ops = 0
        self.env = {}
        self.head = hashlib.sha256(b"orlog-trace-0" + bytes.fromhex(law_hex)).digest()
        self.events = 0
        self.out = bytearray()
        self.claims = [[0, 0, 0, 0, 0] for _ in an.claims]
        self.clause_cost = {}
        self.trace = [] if trace else None
        self.seal_text = seal_words(law_hex).encode("ascii")

    # -------------------------------------------------- events and refusals
    def ev(self, kind, clause, payload):
        self.head = hashlib.sha256(self.head + kind + struct.pack(">II", clause, len(payload)) + payload).digest()
        self.events += 1
        if self.trace is not None:
            self.trace.append("%d %s %d %s %s" % (self.events, kind.decode(), clause,
                                                 payload.hex() if payload else "-", self.head.hex()))

    def refuse(self, code, clause):
        self.ev(b"R", clause, code.encode("ascii"))
        raise Stop(code, clause)

    def num(self, fn, clause, *args):
        try:
            return fn(*args)
        except N.Refusal as r:
            self.refuse(r.code, clause)

    # -------------------------------------------------- running
    def run(self):
        try:
            self.seq(self.prog.top)
            status = "COMPLETED"
        except Stop as s:
            status = "REFUSED %s %d" % (s.code, s.clause)
        self.status = status
        return self

    def receipt(self, backend="reference"):
        return receipt_text(backend, self.law_hex, self.text_hex, self.status, len(self.out),
                            hashlib.sha256(bytes(self.out)).hexdigest(), self.events, self.head.hex(), self.ops,
                            self.claims, [c.id for c in self.an.claims])

    def seq(self, clauses):
        for c in clauses:
            if c.absorbed:
                continue
            if c.cost_tracked:
                start = self.ops
                self.stmt(c, c.stmt)
                self.clause_cost[c.id] = self.clause_cost.get(c.id, 0) + self.ops - start
            else:
                self.stmt(c, c.stmt)

    def body(self, c, b):
        if isinstance(b, tuple) and b[0] == BLOCK:
            self.seq(b[1].children)
        else:
            self.stmt(c, b)

    def stmt(self, c, s):
        cid = c.id
        if self.budget is not None and self.ops > self.budget:
            raise HostStop(self.ops, self.budget)
        if isinstance(s, (Define, ProcDef, Decimals)):
            return
        if isinstance(s, Let):
            self.ops += 1
            v = self.eval(cid, s.expr)
            if isinstance(s.var.type, tuple):
                v = list(v)
            self.env[s.var.id] = v
            self.ev(b"A", cid, struct.pack(">I", s.var.id) + enc_value(v, s.var.type))
        elif isinstance(s, SetS):
            self.ops += 1
            if s.index is None:
                v = self.eval(cid, s.expr)
                if isinstance(s.var.type, tuple):
                    v = list(v)
                self.env[s.var.id] = v
                self.ev(b"A", cid, struct.pack(">I", s.var.id) + enc_value(v, s.var.type))
            else:
                k = self.eval(cid, s.index)
                v = self.eval(cid, s.expr)
                lst = self.env[s.var.id]
                if not 1 <= k <= len(lst):
                    self.refuse("INDEX-OUT-OF-RANGE", cid)
                lst[k - 1] = v
                self.ev(b"E", cid, struct.pack(">IQ", s.var.id, k) + enc_value(v, s.var.type[1]))
        elif isinstance(s, Change):
            self.ops += 1
            t = s.elem
            if s.index is None:
                cur = self.env[s.var.id]
                v = self.eval(cid, s.expr)
                self.ops += 1
                new = self.arith("+" if s.sign == "+" else "-", t, cur, v, cid)
                self.env[s.var.id] = new
                self.ev(b"A", cid, struct.pack(">I", s.var.id) + enc_value(new, t))
            else:
                k = self.eval(cid, s.index)
                self.ops += 1
                lst = self.env[s.var.id]
                if not 1 <= k <= len(lst):
                    self.refuse("INDEX-OUT-OF-RANGE", cid)
                cur = lst[k - 1]
                v = self.eval(cid, s.expr)
                self.ops += 1
                new = self.arith("+" if s.sign == "+" else "-", t, cur, v, cid)
                lst[k - 1] = new
                self.ev(b"E", cid, struct.pack(">IQ", s.var.id, k) + enc_value(new, t))
        elif isinstance(s, Say):
            self.ops += 1
            v = self.eval(cid, s.expr)
            data = v if s.expr.type == "text" else fmt(v, s.expr.type)
            if len(data) > N.TEXT_MAX:
                self.refuse("TEXT-TOO-LONG", cid)
            line = bytes(data) + b"\n"
            if len(self.out) + len(line) > OUTPUT_MAX:
                self.refuse("OUTPUT-TOO-LONG", cid)
            self.out += line
            self.ev(b"S", cid, line)
        elif isinstance(s, IfS):
            for cond, b, ac in s.arms:
                self.ops += 1
                if self.eval(ac.id, cond):
                    self.body(ac, b)
                    return
            if s.els is not None:
                self.body(s.els[1], s.els[0])
        elif isinstance(s, While):
            n = 0
            while True:
                self.ops += 1
                if not self.eval(cid, s.cond):
                    break
                if n == s.fuel:
                    self.refuse("FUEL-EXHAUSTED", cid)
                n += 1
                self.seq(c.children)
        elif isinstance(s, For):
            self.ops += 1
            lo = self.eval(cid, s.lo)
            hi = self.eval(cid, s.hi)
            k = lo
            while k <= hi:
                self.ops += 1
                self.env[s.var.id] = k
                self.ev(b"A", cid, struct.pack(">I", s.var.id) + enc_value(k, "int"))
                self.seq(c.children)
                if k == hi:
                    break
                k += 1
        elif isinstance(s, Perform):
            self.ops += 1
            self.seq(s.proc.children)
        elif isinstance(s, Must):
            self.ops += 1
            r = bool(self.eval(cid, s.cond))
            self.ev(b"M", cid, struct.pack(">I", s.id) + bytes([int(r)]))
            if not r:
                self.refuse("MUST-FAILED", cid)
        elif isinstance(s, Claim):
            self.ops += 1
            start = self.ops
            r = bool(self.eval(cid, s.cond))
            cost = self.ops - start
            if s.oracle[0] == "certificate":
                rc, rcost = s.ref.id, self.clause_cost.get(s.ref.id, 0)
            else:
                rc, rcost = 0, 0
            self.ev(b"C", cid, struct.pack(">I", s.id) + bytes([int(r)]))
            acc = self.claims[s.id]
            acc[0] += 1
            acc[1] += int(r)
            acc[2] += cost
            acc[3], acc[4] = rc, rcost
            if not r:
                self.refuse("CLAIM-REFUTED", cid)
        elif isinstance(s, Append):
            self.ops += 1
            v = self.eval(cid, s.expr)
            lst = self.env[s.var.id]
            if len(lst) + 1 > N.LIST_MAX:
                self.refuse("LIST-TOO-LONG", cid)
            lst.append(v)
            self.ev(b"P", cid, struct.pack(">I", s.var.id) + enc_value(v, s.var.type[1]))
        elif isinstance(s, RemoveLast):
            self.ops += 1
            lst = self.env[s.var.id]
            if not lst:
                self.refuse("EMPTY-LIST", cid)
            lst.pop()
            self.ev(b"Q", cid, struct.pack(">IQ", s.var.id, len(lst)))
        else:
            raise AssertionError(s)

    # -------------------------------------------------- expressions
    def arith(self, op, t, a, b, cid):
        table = {
            "int": {"+": N.i_add, "-": N.i_sub, "*": N.i_mul, "/": N.i_div, "max": N.i_max, "min": N.i_min},
            "fix": {"+": N.x_add, "-": N.x_sub, "*": N.x_mul, "/": N.x_div, "max": N.x_max, "min": N.x_min},
            "float": {"+": N.f_add, "-": N.f_sub, "*": N.f_mul, "/": N.f_div, "max": N.f_max, "min": N.f_min},
        }
        return self.num(table[t][op], cid, a, b)

    def eval(self, cid, e):
        if isinstance(e, Num):
            return e.value
        if isinstance(e, Str):
            return e.value.encode("utf-8")
        if isinstance(e, BoolLit):
            return e.value
        if isinstance(e, Seal):
            return self.seal_text
        if isinstance(e, Var):
            if e.rule:
                return self.rule(cid, e.rule)
            v = self.env[e.var.id]
            return list(v) if isinstance(v, list) else v
        if isinstance(e, Bin):
            if e.op == "and":
                a = self.eval(cid, e.a)
                self.ops += 1
                return self.eval(cid, e.b) if a else False
            if e.op == "or":
                a = self.eval(cid, e.a)
                self.ops += 1
                return True if a else self.eval(cid, e.b)
            a = self.eval(cid, e.a)
            b = self.eval(cid, e.b)
            self.ops += 1
            if e.op in ("+", "-", "*", "/", "max", "min"):
                return self.arith(e.op, e.type, a, b, cid)
            if e.op == "quot":
                return self.num(N.i_quot, cid, a, b)
            if e.op == "rem":
                return self.num(N.i_rem, cid, a, b)
            if e.op == "==":
                return a == b
            if e.op == "!=":
                return a != b
            if e.op == "<":
                return a < b
            if e.op == ">":
                return a > b
            if e.op == "<=":
                return a <= b
            if e.op == ">=":
                return a >= b
            raise AssertionError(e.op)
        if isinstance(e, Un):
            a = self.eval(cid, e.a)
            self.ops += 1
            t = e.a.type
            if e.op == "not":
                return not a
            if e.op == "even":
                return a % 2 == 0
            if e.op == "odd":
                return a % 2 != 0
            if e.op == "zero":
                return a == 0
            if e.op == "positive":
                return a > 0
            if e.op == "negative":
                return a < 0
            fns = {"neg": {"int": N.i_neg, "fix": N.x_neg, "float": N.f_neg},
                   "abs": {"int": N.i_abs, "fix": N.x_abs, "float": N.f_abs},
                   "sqrt": {"int": N.i_isqrt, "fix": N.x_sqrt, "float": N.f_sqrt},
                   "trunc": {"fix": N.x_trunc, "float": N.f_trunc}}
            return self.num(fns[e.op][t], cid, a)
        if isinstance(e, Conv):
            a = self.eval(cid, e.a)
            self.ops += 1
            return self.convert(e.mode, e.target, e.a.type, a, cid)
        if isinstance(e, Cat):
            vals = [self.eval(cid, p) for p in e.parts]
            self.ops += len(e.parts) - 1
            buf = bytearray()
            for v, p in zip(vals, e.parts):
                piece = v if p.type == "text" else fmt(v, p.type)
                if len(buf) + len(piece) > N.TEXT_MAX:
                    self.refuse("TEXT-TOO-LONG", cid)
                buf += piece
            return bytes(buf)
        if isinstance(e, Item):
            k = self.eval(cid, e.index)
            self.ops += 1
            lst = self.env[e.var.id]
            if not 1 <= k <= len(lst):
                self.refuse("INDEX-OUT-OF-RANGE", cid)
            return lst[k - 1]
        if isinstance(e, Length):
            self.ops += 1
            return len(self.env[e.var.id])
        if isinstance(e, ListOf):
            n = self.eval(cid, e.count)
            v = self.eval(cid, e.value)
            self.ops += 1
            if n < 0:
                self.refuse("NEGATIVE-LENGTH", cid)
            if n > N.LIST_MAX:
                self.refuse("LIST-TOO-LONG", cid)
            return [v] * n
        if isinstance(e, ListLit):
            vals = [self.eval(cid, x) for x in e.items]
            self.ops += 1
            return vals
        raise AssertionError(e)

    def convert(self, mode, target, src, a, cid):
        if mode == "promote":
            return self.num(N.x_from_i, cid, a) if target == "fix" else self.num(N.f_from_i, cid, a, False)
        if target == "int":
            if mode == "rounded":
                return self.num(N.x_round if src == "fix" else N.f_round, cid, a)
            if src == "fix":
                if a & (N.ONE - 1):
                    self.refuse("INEXACT-CONVERSION", cid)
                return N.x_trunc(a)
            if a != a or a in (float("inf"), float("-inf")):
                self.refuse("NOT-FINITE", cid)
            if abs(a) < 2.0 ** 63 and a != int(a):
                self.refuse("INEXACT-CONVERSION", cid)
            return self.num(N.f_trunc, cid, a)
        if target == "fix":
            if src == "int":
                return self.num(N.x_from_i, cid, a)
            return self.num(N.f_to_x, cid, a, mode == "rounded")
        if src == "int":
            return self.num(N.f_from_i, cid, a, mode == "rounded")
        return self.num(N.x_to_f, cid, a, mode == "rounded")

    def rule(self, cid, name):
        self.ops += 1
        clauses = self.an.rules[name]
        beats = self.an.overrides[name]
        applicable = []
        for c in clauses:
            d = c.stmt
            if d.proviso is None or self.eval(cid, d.proviso):
                applicable.append(c)
        ids = set(c.id for c in applicable)
        maximal = [c for c in applicable if not any(c.id in beats[o] for o in ids if o != c.id)]
        if not maximal:
            self.refuse("RULE-UNDEFINED", cid)
        vals = [self.eval(cid, c.stmt.expr) for c in maximal]
        for v in vals[1:]:
            if not (v == vals[0]):
                self.refuse("RULE-CONFLICT", cid)
        return vals[0]

"""Three-address code -> one self-contained ISO C99 program (runtime header pasted at the top)."""
import os
import struct

from .lower import REFUSING

TAGC = {"int": "'I'", "fix": "'X'", "float": "'F'", "bool": "'B'"}
CTYPE = {"int": "int64_t", "fix": "int64_t", "float": "double", "bool": "int", "text": "orl_text", "u64": "uint64_t"}
SAFE = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ")


def ctype(t):
    return "orl_list" if isinstance(t, tuple) else CTYPE[t]


def cint(v):
    v = int(v)
    if v == -(1 << 63):
        return "(-INT64_C(9223372036854775807) - 1)"
    return "INT64_C(%d)" % v


def cstr(b):
    return "".join(chr(x) if x in SAFE else "\\%03o" % x for x in b)


def clit(t, v):
    if t in ("int", "fix"):
        return cint(v)
    if t == "float":
        return "orl_cf(UINT64_C(0x%016X))" % struct.unpack("<Q", struct.pack("<d", v))[0]
    if t == "bool":
        return "1" if v else "0"
    if t == "text":
        return "orl_t_lit(\"%s\", %du)" % (cstr(v), len(v))
    raise ValueError(t)


def default(t):
    if isinstance(t, tuple):
        return "{0, 0, 0}"
    return {"int": "0", "fix": "0", "u64": "0", "float": "0.0", "bool": "0", "text": "{0, 0}"}[t]


class CGen:
    def __init__(self, low, runtime_path):
        self.low = low
        self.runtime_path = runtime_path
        self.lines = []

    def var(self, vi):
        return "g_v%d" % vi.id if vi.top else "v%d" % vi.id

    def clause(self, c):
        return "clause" if c == "CLAUSE" else "%du" % c

    def arg(self, a):
        if isinstance(a, tuple) and a[0] == "flag":
            return str(a[1])
        return a

    def w(self, d, s):
        self.lines.append("    " * d + s)

    def to_slot(self, elem, x):
        if elem == "float":
            return "orl_f_bits(%s)" % x
        if elem == "bool":
            return "(int64_t)(%s != 0)" % x
        return x

    def from_slot(self, elem, x):
        if elem == "float":
            return "orl_bits_f(%s)" % x
        if elem == "bool":
            return "(%s != 0)" % x
        return x

    def block(self, d, instrs):
        for ins in instrs:
            self.ins(d, ins)

    def ins(self, d, ins):
        op = ins[0]
        if op == "tick":
            self.w(d, "orl_ops += 1;")
        elif op == "ops":
            self.w(d, "orl_ops += %d;" % ins[1])
        elif op == "const":
            self.w(d, "%s = %s;" % (ins[1], clit(ins[2], ins[3])))
        elif op == "read":
            vi = ins[2]
            if isinstance(vi.type, tuple):
                self.w(d, "%s = orl_l_copy(&%s);" % (ins[1], self.var(vi)))
            else:
                self.w(d, "%s = %s;" % (ins[1], self.var(vi)))
        elif op == "write":
            vi = ins[1]
            if vi.type == "text":       # the variable's slot owns its text: copy in, then free (E21)
                self.w(d, "orl_t_store(&%s, &g_ts%d, %s);" % (self.var(vi), vi.id, ins[2]))
            elif isinstance(vi.type, tuple):    # a list variable owns its buffer: copy in (E21, finding 8)
                self.w(d, "orl_l_store(&%s, %s);" % (self.var(vi), ins[2]))
            else:
                self.w(d, "%s = %s;" % (self.var(vi), ins[2]))
        elif op == "tmark":
            self.w(d, "size_t %s = orl_tmp_mark();" % ins[1])
        elif op == "trelease":
            self.w(d, "orl_tmp_release(%s);" % ins[1])
        elif op == "copy":
            self.w(d, "%s = %s;" % (ins[1], ins[2]))
        elif op == "set_u64":
            self.w(d, "%s = UINT64_C(%d);" % (ins[1], ins[2]))
        elif op == "snap":
            self.w(d, "%s = orl_ops;" % ins[1])
        elif op == "cost_add":
            self.w(d, "g_cost%d += orl_ops - %s;" % (ins[1], ins[2]))
        elif op == "ev_assign":
            cid, vi = ins[1], ins[2]
            t, v = vi.type, self.var(vi)
            if isinstance(t, tuple):
                self.w(d, "orl_ev_assign_l(%du, %du, %s, %s.v, %s.len);" % (cid, vi.id, TAGC[t[1]], v, v))
            else:
                fn = {"int": "i", "fix": "x", "float": "f", "bool": "b", "text": "t"}[t]
                self.w(d, "orl_ev_assign_%s(%du, %du, %s);" % (fn, cid, vi.id, v))
        elif op == "ev_item":
            cid, vi, k, v = ins[1:]
            e = vi.type[1]
            self.w(d, "orl_ev_item(%du, %du, (uint64_t)%s, %s, %s);" % (cid, vi.id, k, TAGC[e], self.to_slot(e, v)))
        elif op == "ev_push":
            cid, vi, v = ins[1:]
            e = vi.type[1]
            self.w(d, "orl_ev_push(%du, %du, %s, %s);" % (cid, vi.id, TAGC[e], self.to_slot(e, v)))
        elif op == "ev_pop":
            cid, vi = ins[1:]
            self.w(d, "orl_ev_pop(%du, %du, %s.len);" % (cid, vi.id, self.var(vi)))
        elif op == "call":
            t, fn, args, c = ins[1], ins[2], ins[3], ins[4]
            a = [self.arg(x) for x in args]
            if fn == "x_as_i":
                self.w(d, "if ((%s & INT64_C(0xFFFFFFFF)) != 0) orl_refuse(\"INEXACT-CONVERSION\", %s);"
                       % (a[0], self.clause(c)))
                self.w(d, "%s = orl_x_trunc(%s);" % (t, a[0]))
            elif fn == "f_as_i":
                self.w(d, "%s = orl_f_trunc(%s, %s);" % (t, a[0], self.clause(c)))
                self.w(d, "if (orl_f_from_i(%s, 1, %s) != %s) orl_refuse(\"INEXACT-CONVERSION\", %s);"
                       % (t, self.clause(c), a[0], self.clause(c)))
            elif fn in REFUSING:
                self.w(d, "%s = orl_%s(%s, %s);" % (t, fn, ", ".join(a), self.clause(c)))
            else:
                self.w(d, "%s = orl_%s(%s);" % (t, fn, ", ".join(a)))
        elif op == "cmp":
            t, o, ty, a, b = ins[1:]
            if ty == "text":
                self.w(d, "%s = %sorl_t_eq(%s, %s);" % (t, "" if o == "==" else "!", a, b))
            else:
                self.w(d, "%s = (%s %s %s);" % (t, a, o, b))
        elif op == "pred":
            t, o, ty, a = ins[1:]
            expr = {"even": "%s %% 2 == 0", "odd": "%s %% 2 != 0", "zero": "%s == 0",
                    "positive": "%s > 0", "negative": "%s < 0"}[o] % a
            self.w(d, "%s = (%s);" % (t, expr))
        elif op == "not":
            self.w(d, "%s = !%s;" % (ins[1], ins[2]))
        elif op == "if":
            self.w(d, "if (%s) {" % ins[1])
            self.block(d + 1, ins[2])
            if ins[3]:
                self.w(d, "} else {")
                self.block(d + 1, ins[3])
            self.w(d, "}")
        elif op == "loop":
            self.w(d, "for (;;) {")
            self.block(d + 1, ins[1])
            self.w(d, "}")
        elif op == "break_unless":
            self.w(d, "if (!%s) break;" % ins[1])
        elif op == "fuel":
            self.w(d, "if (%s == UINT64_C(%d)) orl_refuse(\"FUEL-EXHAUSTED\", %du);" % (ins[1], ins[2], ins[3]))
            self.w(d, "%s += 1;" % ins[1])
        elif op == "for":
            self.w(d, "if (%s <= %s) for (;;) {" % (ins[1], ins[2]))
            self.block(d + 1, ins[3])
            self.w(d, "}")
        elif op == "break_if_eq":
            self.w(d, "if (%s == %s) break;" % (ins[1], ins[2]))
        elif op == "incr":
            self.w(d, "%s = %s + 1;" % (ins[1], ins[1]))
        elif op == "perform":
            self.w(d, "%s();" % ins[1])
        elif op == "must":
            self.w(d, "orl_must(%du, %du, %s);" % (ins[1], ins[2], ins[3]))
        elif op == "claim":
            i, c, t, snap, ref = ins[1:]
            refcost = "g_cost%d" % ref if ref else "UINT64_C(0)"
            self.w(d, "orl_claim(%du, %du, %s, orl_ops - %s, %du, %s);" % (i, c, t, snap, ref, refcost))
        elif op == "say":
            c, t, ty = ins[1], ins[2], ins[3]
            self.w(d, "orl_s_reset(%du);" % c)
            self.part(d, t, ty)
            self.w(d, "orl_say(%du);" % c)
        elif op == "cat":
            t, parts, c = ins[1], ins[2], ins[3]
            self.w(d, "orl_s_reset(%s);" % self.clause(c))
            for p, ty in parts:
                self.part(d, p, ty)
            self.w(d, "%s = orl_s_take();" % t)
        elif op == "list_new":
            t, n, v, c = ins[1:]
            e = self.low_type(t)[1]
            self.w(d, "%s = orl_l_new(%s, %s, %s);" % (t, n, self.to_slot(e, v), self.clause(c)))
        elif op == "list_lit":
            t, items = ins[1], ins[2]
            e = self.low_type(t)[1]
            self.w(d, "{ int64_t orl_tmp[%d] = {%s}; %s = orl_l_from(%du, orl_tmp); }"
                   % (len(items), ", ".join(self.to_slot(e, x) for x in items), t, len(items)))
        elif op == "list_get":
            t, vi, k, c = ins[1:]
            e = vi.type[1]
            self.w(d, "%s = %s;" % (t, self.from_slot(e, "orl_l_get(&%s, %s, %s)" % (self.var(vi), k,
                                                                                      self.clause(c)))))
        elif op == "list_set":
            vi, k, v, c = ins[1:]
            e = vi.type[1]
            self.w(d, "orl_l_set(&%s, %s, %s, %s);" % (self.var(vi), k, self.to_slot(e, v), self.clause(c)))
        elif op == "list_push":
            vi, v, c = ins[1:]
            e = vi.type[1]
            self.w(d, "orl_l_push(&%s, %s, %s);" % (self.var(vi), self.to_slot(e, v), self.clause(c)))
        elif op == "list_pop":
            self.w(d, "orl_l_pop(&%s, %s);" % (self.var(ins[1]), self.clause(ins[2])))
        elif op == "list_len":
            self.w(d, "%s = orl_l_len(&%s);" % (ins[1], self.var(ins[2])))
        elif op == "rule":
            self.w(d, "%s = %s(%s);" % (ins[1], ins[2], self.clause(ins[3])))
        elif op == "maximal":
            m, a, killers = ins[1:]
            if killers:
                self.w(d, "%s = %s && !(%s);" % (m, a, " || ".join(killers)))
            else:
                self.w(d, "%s = %s;" % (m, a))
        elif op == "any":
            self.w(d, "%s = %s;" % (ins[1], " || ".join(ins[2])))
        elif op == "refuse_unless":
            self.w(d, "if (!%s) orl_refuse(\"%s\", %s);" % (ins[1], ins[2], self.clause(ins[3])))
        elif op == "rule_keep":
            have, val, v = ins[1], ins[2], ins[3]
            self.w(d, "if (!%s) { %s = %s; %s = 1; }" % (have, val, v, have))
        elif op == "rule_conflict":
            val, v, ty, c = ins[1:]
            eq = "orl_t_eq(%s, %s)" % (v, val) if ty == "text" else "(%s == %s)" % (v, val)
            self.w(d, "if (!%s) orl_refuse(\"RULE-CONFLICT\", %s);" % (eq, self.clause(c)))
        elif op == "return":
            self.w(d, "return %s;" % ins[1])
        else:
            raise AssertionError(ins)

    def part(self, d, t, ty):
        if isinstance(ty, tuple):
            self.w(d, "orl_s_list(%s, %s.v, %s.len);" % (TAGC[ty[1]], t, t))
        else:
            fn = {"int": "s_i", "fix": "s_x", "float": "s_f", "bool": "s_b", "text": "s_t"}[ty]
            self.w(d, "orl_%s(%s);" % (fn, t))

    def low_type(self, temp):
        return self.types[temp]

    def emit_fn(self, f, sig):
        self.types = dict(f.temps)
        self.w(0, "%s {" % sig)
        for vid, t in sorted(f.locals.items()):
            # a list local owns its buffer across calls (static: no recursion, so one live instance) (E21)
            self.w(1, "%s%s v%d = %s;" % ("static " if isinstance(t, tuple) else "", ctype(t), vid, default(t)))
        for name, t in f.temps:
            self.w(1, "%s %s = %s;" % (ctype(t), name, default(t)))
        self.block(1, f.body)
        self.w(0, "}")
        self.w(0, "")

    def program(self):
        low, comp = self.low, self.low.comp
        with open(self.runtime_path, "r", encoding="utf-8") as fh:
            runtime = fh.read()
        self.w(0, "/* Generated by the Orlog OL-0 C99 backend. Law %s (%s). */" % (comp.law_seal, comp.seal_words))
        self.lines.append(runtime.rstrip("\n"))
        self.w(0, "")
        self.w(0, "static double orl_cf(uint64_t b) { double d; memcpy(&d, &b, sizeof d); return d; }")
        claims = [c.id for c in comp.an.claims]
        self.w(0, "static const uint32_t ORL_CLAIM_CLAUSE[%d] = {%s};" % (max(1, len(claims)),
                                                                        ", ".join("%du" % c for c in claims) or "0u"))
        for v in low.top_vars:
            self.w(0, "static %s g_v%d = %s;" % (ctype(v.type), v.id, default(v.type)))
        # one slot per text variable, static even for locals: no recursion, so one live instance of each (E21)
        for v in comp.an.vars:
            if v.type == "text":
                self.w(0, "static orl_tslot g_ts%d = {NULL, 0};" % v.id)
        for c in low.cost_clauses:
            self.w(0, "static uint64_t g_cost%d = 0;" % c)
        for c, f in low.procs:
            self.w(0, "static void %s(void);" % f.name)
        for name, f in low.rules:
            self.w(0, "static %s %s(uint32_t clause);" % (ctype(f.ret), f.name))
        self.w(0, "")
        for name, f in low.rules:
            self.emit_fn(f, "static %s %s(uint32_t clause)" % (ctype(f.ret), f.name))
        for c, f in low.procs:
            self.emit_fn(f, "static void %s(void)" % f.name)
        self.emit_fn(low.main, "static void orl_main(void)")
        self.w(0, "int main(int argc, char **argv) {")
        self.w(1, "orl_init(argc, argv, \"c99\", \"%s\", \"%s\", %du, ORL_CLAIM_CLAUSE);"
               % (comp.law_seal, comp.text_seal, len(claims)))
        self.w(1, "orl_main();")
        self.w(1, "orl_finish();")
        self.w(1, "return 0;")
        self.w(0, "}")
        return "\n".join(self.lines) + "\n"


def generate(low, runtime_path):
    return CGen(low, runtime_path).program()

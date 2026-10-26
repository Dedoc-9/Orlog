"""Three-address code -> one self-contained Rust program (runtime pasted at the top)."""
import struct

from .lower import REFUSING

TAGR = {"int": "b'I'", "fix": "b'X'", "float": "b'F'", "bool": "b'B'"}
RTYPE = {"int": "i64", "fix": "i64", "float": "f64", "bool": "bool", "text": "Vec<u8>", "u64": "u64"}
# runtime functions that take no &mut self (RUNTIME-SPEC.md section 2)
ASSOC = {"i_max", "i_min", "x_trunc", "x_round", "x_max", "x_min", "f_canon", "f_add", "f_sub", "f_mul",
         "f_div", "f_neg", "f_abs", "f_sqrt", "f_max", "f_min"}
ATTRS = ("#![allow(unused_mut, unused_variables, unused_assignments, dead_code, unused_parens, "
         "non_snake_case, unreachable_code, unused_imports, clippy::all)]")


def rtype(t):
    return "Vec<i64>" if isinstance(t, tuple) else RTYPE[t]


def rint(v):
    v = int(v)
    if v == -(1 << 63):
        return "i64::MIN"
    return "%di64" % v


def rbytes(b):
    return "".join(chr(x) if (0x20 <= x < 0x7F and chr(x) not in "\"\\") else "\\x%02x" % x for x in b)


def rlit(t, v):
    if t in ("int", "fix"):
        return rint(v)
    if t == "float":
        return "f64::from_bits(0x%016Xu64)" % struct.unpack("<Q", struct.pack("<d", v))[0]
    if t == "bool":
        return "true" if v else "false"
    if t == "text":
        return "b\"%s\".to_vec()" % rbytes(v)
    raise ValueError(t)


def default(t):
    if isinstance(t, tuple):
        return "Vec::new()"
    return {"int": "0i64", "fix": "0i64", "u64": "0u64", "float": "0.0f64", "bool": "false",
            "text": "Vec::new()"}[t]


class RsGen:
    def __init__(self, low, runtime_path):
        self.low = low
        self.runtime_path = runtime_path
        self.lines = []

    def var(self, vi):
        return "st.v%d" % vi.id if vi.top else "v%d" % vi.id

    def clause(self, c):
        return "clause" if c == "CLAUSE" else "%du32" % c

    def arg(self, a):
        if isinstance(a, tuple) and a[0] == "flag":
            return "true" if a[1] else "false"
        return a

    def w(self, d, s):
        self.lines.append("    " * d + s)

    def to_slot(self, elem, x):
        if elem == "float":
            return "Rt::f_bits(%s)" % x
        if elem == "bool":
            return "(if %s { 1i64 } else { 0i64 })" % x
        return x

    def from_slot(self, elem, x):
        if elem == "float":
            return "Rt::bits_f(%s)" % x
        if elem == "bool":
            return "(%s != 0)" % x
        return x

    def block(self, d, instrs):
        for ins in instrs:
            self.ins(d, ins)

    def ins(self, d, ins):
        op = ins[0]
        if op == "tick":
            self.w(d, "rt.ops += 1;")
        elif op == "ops":
            self.w(d, "rt.ops += %d;" % ins[1])
        elif op == "const":
            self.w(d, "%s = %s;" % (ins[1], rlit(ins[2], ins[3])))
        elif op == "read":
            vi = ins[2]
            if isinstance(vi.type, tuple) or vi.type == "text":
                self.w(d, "%s = %s.clone();" % (ins[1], self.var(vi)))
            else:
                self.w(d, "%s = %s;" % (ins[1], self.var(vi)))
        elif op == "write":
            vi = ins[1]
            if isinstance(vi.type, tuple) or vi.type == "text":
                self.w(d, "%s = %s.clone();" % (self.var(vi), ins[2]))
            else:
                self.w(d, "%s = %s;" % (self.var(vi), ins[2]))
        elif op == "copy":
            t = self.types.get(ins[1])
            if t is not None and (isinstance(t, tuple) or t == "text"):
                self.w(d, "%s = %s.clone();" % (ins[1], ins[2]))
            else:
                self.w(d, "%s = %s;" % (ins[1], ins[2]))
        elif op == "set_u64":
            self.w(d, "%s = %du64;" % (ins[1], ins[2]))
        elif op == "snap":
            self.w(d, "%s = rt.ops;" % ins[1])
        elif op == "cost_add":
            self.w(d, "st.cost%d += rt.ops - %s;" % (ins[1], ins[2]))
        elif op == "ev_assign":
            cid, vi = ins[1], ins[2]
            t, v = vi.type, self.var(vi)
            if isinstance(t, tuple):
                self.w(d, "rt.ev_assign_l(%du32, %du32, %s, &%s);" % (cid, vi.id, TAGR[t[1]], v))
            elif t == "text":
                self.w(d, "rt.ev_assign_t(%du32, %du32, &%s);" % (cid, vi.id, v))
            else:
                fn = {"int": "i", "fix": "x", "float": "f", "bool": "b"}[t]
                self.w(d, "rt.ev_assign_%s(%du32, %du32, %s);" % (fn, cid, vi.id, v))
        elif op == "ev_item":
            cid, vi, k, v = ins[1:]
            e = vi.type[1]
            self.w(d, "rt.ev_item(%du32, %du32, %s as u64, %s, %s);" % (cid, vi.id, k, TAGR[e], self.to_slot(e, v)))
        elif op == "ev_push":
            cid, vi, v = ins[1:]
            e = vi.type[1]
            self.w(d, "rt.ev_push(%du32, %du32, %s, %s);" % (cid, vi.id, TAGR[e], self.to_slot(e, v)))
        elif op == "ev_pop":
            cid, vi = ins[1:]
            self.w(d, "rt.ev_pop(%du32, %du32, %s.len() as u64);" % (cid, vi.id, self.var(vi)))
        elif op == "call":
            t, fn, args, c = ins[1], ins[2], ins[3], ins[4]
            a = [self.arg(x) for x in args]
            if fn == "x_as_i":
                self.w(d, "if (%s & 0xFFFFFFFFi64) != 0 { rt.refuse(\"INEXACT-CONVERSION\", %s); }"
                       % (a[0], self.clause(c)))
                self.w(d, "%s = Rt::x_trunc(%s);" % (t, a[0]))
            elif fn == "f_as_i":
                self.w(d, "%s = rt.f_trunc(%s, %s);" % (t, a[0], self.clause(c)))
                self.w(d, "if rt.f_from_i(%s, true, %s) != %s { rt.refuse(\"INEXACT-CONVERSION\", %s); }"
                       % (t, self.clause(c), a[0], self.clause(c)))
            elif fn in ASSOC:
                self.w(d, "%s = Rt::%s(%s);" % (t, fn, ", ".join(a)))
            elif fn in REFUSING:
                self.w(d, "%s = rt.%s(%s, %s);" % (t, fn, ", ".join(a), self.clause(c)))
            else:
                raise AssertionError(fn)
        elif op == "cmp":
            t, o, ty, a, b = ins[1:]
            self.w(d, "%s = %s %s %s;" % (t, a, o, b))
        elif op == "pred":
            t, o, ty, a = ins[1:]
            zero = "0.0f64" if ty == "float" else "0i64"
            expr = {"even": "%s %% 2 == 0" % a, "odd": "%s %% 2 != 0" % a, "zero": "%s == %s" % (a, zero),
                    "positive": "%s > %s" % (a, zero), "negative": "%s < %s" % (a, zero)}[o]
            self.w(d, "%s = %s;" % (t, expr))
        elif op == "not":
            self.w(d, "%s = !%s;" % (ins[1], ins[2]))
        elif op == "if":
            self.w(d, "if %s {" % ins[1])
            self.block(d + 1, ins[2])
            if ins[3]:
                self.w(d, "} else {")
                self.block(d + 1, ins[3])
            self.w(d, "}")
        elif op == "loop":
            self.w(d, "loop {")
            self.block(d + 1, ins[1])
            self.w(d, "}")
        elif op == "break_unless":
            self.w(d, "if !%s { break; }" % ins[1])
        elif op == "fuel":
            self.w(d, "if %s == %du64 { rt.refuse(\"FUEL-EXHAUSTED\", %du32); }" % (ins[1], ins[2], ins[3]))
            self.w(d, "%s += 1;" % ins[1])
        elif op == "for":
            self.w(d, "if %s <= %s { loop {" % (ins[1], ins[2]))
            self.block(d + 1, ins[3])
            self.w(d, "} }")
        elif op == "break_if_eq":
            self.w(d, "if %s == %s { break; }" % (ins[1], ins[2]))
        elif op == "incr":
            self.w(d, "%s = %s + 1;" % (ins[1], ins[1]))
        elif op == "perform":
            self.w(d, "%s(st, rt);" % ins[1])
        elif op == "must":
            self.w(d, "rt.must(%du32, %du32, %s);" % (ins[1], ins[2], ins[3]))
        elif op == "claim":
            i, c, t, snap, ref = ins[1:]
            refcost = "st.cost%d" % ref if ref else "0u64"
            self.w(d, "{ let cost = rt.ops - %s; let refcost = %s; rt.claim(%du32, %du32, %s, cost, %du32, refcost); }"
                   % (snap, refcost, i, c, t, ref))
        elif op == "say":
            c, t, ty = ins[1], ins[2], ins[3]
            self.w(d, "rt.s_reset(%du32);" % c)
            self.part(d, t, ty)
            self.w(d, "rt.say(%du32);" % c)
        elif op == "cat":
            t, parts, c = ins[1], ins[2], ins[3]
            self.w(d, "rt.s_reset(%s);" % self.clause(c))
            for p, ty in parts:
                self.part(d, p, ty)
            self.w(d, "%s = rt.s_take();" % t)
        elif op == "list_new":
            t, n, v, c = ins[1:]
            e = self.types[t][1]
            self.w(d, "%s = rt.l_new(%s, %s, %s);" % (t, n, self.to_slot(e, v), self.clause(c)))
        elif op == "list_lit":
            t, items = ins[1], ins[2]
            e = self.types[t][1]
            self.w(d, "%s = vec![%s];" % (t, ", ".join(self.to_slot(e, x) for x in items)))
        elif op == "list_get":
            t, vi, k, c = ins[1:]
            e = vi.type[1]
            self.w(d, "%s = %s;" % (t, self.from_slot(e, "rt.l_get(&%s, %s, %s)" % (self.var(vi), k,
                                                                                    self.clause(c)))))
        elif op == "list_set":
            vi, k, v, c = ins[1:]
            e = vi.type[1]
            self.w(d, "rt.l_set(&mut %s, %s, %s, %s);" % (self.var(vi), k, self.to_slot(e, v), self.clause(c)))
        elif op == "list_push":
            vi, v, c = ins[1:]
            e = vi.type[1]
            self.w(d, "rt.l_push(&mut %s, %s, %s);" % (self.var(vi), self.to_slot(e, v), self.clause(c)))
        elif op == "list_pop":
            self.w(d, "rt.l_pop(&mut %s, %s);" % (self.var(ins[1]), self.clause(ins[2])))
        elif op == "list_len":
            self.w(d, "%s = %s.len() as i64;" % (ins[1], self.var(ins[2])))
        elif op == "rule":
            self.w(d, "%s = %s(st, rt, %s);" % (ins[1], ins[2], self.clause(ins[3])))
        elif op == "maximal":
            m, a, killers = ins[1:]
            if killers:
                self.w(d, "%s = %s && !(%s);" % (m, a, " || ".join(killers)))
            else:
                self.w(d, "%s = %s;" % (m, a))
        elif op == "any":
            self.w(d, "%s = %s;" % (ins[1], " || ".join(ins[2])))
        elif op == "refuse_unless":
            self.w(d, "if !%s { rt.refuse(\"%s\", %s); }" % (ins[1], ins[2], self.clause(ins[3])))
        elif op == "rule_keep":
            have, val, v = ins[1], ins[2], ins[3]
            t = self.types[val]
            src = "%s.clone()" % v if t == "text" else v
            self.w(d, "if !%s { %s = %s; %s = true; }" % (have, val, src, have))
        elif op == "rule_conflict":
            val, v, ty, c = ins[1:]
            self.w(d, "if !(%s == %s) { rt.refuse(\"RULE-CONFLICT\", %s); }" % (v, val, self.clause(c)))
        elif op == "return":
            self.w(d, "return %s;" % ins[1])
        else:
            raise AssertionError(ins)

    def part(self, d, t, ty):
        if isinstance(ty, tuple):
            self.w(d, "rt.s_list(%s, &%s);" % (TAGR[ty[1]], t))
        elif ty == "text":
            self.w(d, "rt.s_t(&%s);" % t)
        else:
            fn = {"int": "s_i", "fix": "s_x", "float": "s_f", "bool": "s_b"}[ty]
            self.w(d, "rt.%s(%s);" % (fn, t))

    def emit_fn(self, f, sig):
        self.types = dict(f.temps)
        self.w(0, "%s {" % sig)
        for vid, t in sorted(f.locals.items()):
            self.w(1, "let mut v%d: %s = %s;" % (vid, rtype(t), default(t)))
        for name, t in f.temps:
            self.w(1, "let mut %s: %s = %s;" % (name, rtype(t), default(t)))
        self.block(1, f.body)
        self.w(0, "}")
        self.w(0, "")

    def program(self):
        low, comp = self.low, self.low.comp
        with open(self.runtime_path, "r", encoding="utf-8") as fh:
            runtime = fh.read()
        self.w(0, ATTRS)
        self.w(0, "// Generated by the Orlog OL-0 Rust backend. Law %s (%s)." % (comp.law_seal, comp.seal_words))
        self.lines.append(runtime.rstrip("\n"))
        self.w(0, "")
        claims = [c.id for c in comp.an.claims]
        self.w(0, "const ORL_CLAIM_CLAUSE: [u32; %d] = [%s];" % (len(claims), ", ".join("%du32" % c for c in claims)))
        self.w(0, "struct St {")
        for v in low.top_vars:
            self.w(1, "v%d: %s," % (v.id, rtype(v.type)))
        for c in low.cost_clauses:
            self.w(1, "cost%d: u64," % c)
        self.w(0, "}")
        self.w(0, "impl St {")
        self.w(1, "fn new() -> St {")
        self.w(2, "St { %s }" % ", ".join(["v%d: %s" % (v.id, default(v.type)) for v in low.top_vars] +
                                          ["cost%d: 0u64" % c for c in low.cost_clauses]))
        self.w(1, "}")
        self.w(0, "}")
        self.w(0, "")
        for name, f in low.rules:
            self.emit_fn(f, "fn %s(st: &mut St, rt: &mut Rt, clause: u32) -> %s" % (f.name, rtype(f.ret)))
        for c, f in low.procs:
            self.emit_fn(f, "fn %s(st: &mut St, rt: &mut Rt)" % f.name)
        self.emit_fn(low.main, "fn orl_main(st: &mut St, rt: &mut Rt)")
        self.w(0, "fn main() {")
        self.w(1, "let mut rt = Rt::init(\"rust\", \"%s\", \"%s\", &ORL_CLAIM_CLAUSE);" % (comp.law_seal, comp.text_seal))
        self.w(1, "let mut st = St::new();")
        self.w(1, "orl_main(&mut st, &mut rt);")
        self.w(1, "rt.finish();")
        self.w(0, "}")
        return "\n".join(self.lines) + "\n"


def generate(low, runtime_path):
    return RsGen(low, runtime_path).program()

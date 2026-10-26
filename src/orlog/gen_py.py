"""Three-address code -> one self-contained Python program (runtime pasted at the top)."""
import os
import struct

from .lower import REFUSING

HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = {"int": "I", "fix": "X", "float": "F", "bool": "B", "text": "T"}


def tag_of(t):
    if isinstance(t, tuple):
        return "L" + TAGS[t[1]]
    return TAGS[t]


def pylit(t, v):
    if t in ("int", "fix"):
        return repr(int(v))
    if t == "float":
        return "_bitsf(0x%016X)" % struct.unpack("<Q", struct.pack("<d", v))[0]
    if t == "bool":
        return "True" if v else "False"
    if t == "text":
        return repr(bytes(v))
    raise ValueError(t)


class PyGen:
    def __init__(self, low):
        self.low = low
        self.lines = []

    def var(self, vi):
        return "st.v%d" % vi.id if vi.top else "v%d" % vi.id

    def clause(self, c):
        return "clause" if c == "CLAUSE" else str(c)

    def arg(self, a):
        if isinstance(a, tuple) and a[0] == "flag":
            return "True" if a[1] else "False"
        return a

    def w(self, depth, s):
        self.lines.append("    " * depth + s)

    def block(self, depth, instrs):
        if not instrs:
            self.w(depth, "pass")
            return
        for ins in instrs:
            self.ins(depth, ins)

    def ins(self, d, ins):
        op = ins[0]
        if op == "tick":
            self.w(d, "rt.ops += 1")
        elif op == "ops":
            self.w(d, "rt.ops += %d" % ins[1])
        elif op == "const":
            self.w(d, "%s = %s" % (ins[1], pylit(ins[2], ins[3])))
        elif op == "read":
            vi = ins[2]
            src = self.var(vi)
            self.w(d, "%s = list(%s)" % (ins[1], src) if isinstance(vi.type, tuple) else "%s = %s" % (ins[1], src))
        elif op == "write":
            self.w(d, "%s = %s" % (self.var(ins[1]), ins[2]))
        elif op in ("tmark", "trelease"):
            pass                        # the C backend's temp stack (E21); Python owns its texts by value
        elif op == "copy":
            self.w(d, "%s = %s" % (ins[1], ins[2]))
        elif op == "set_u64":
            self.w(d, "%s = %d" % (ins[1], ins[2]))
        elif op == "snap":
            self.w(d, "%s = rt.ops" % ins[1])
        elif op == "cost_add":
            self.w(d, "st.cost%d += rt.ops - %s" % (ins[1], ins[2]))
        elif op == "ev_assign":
            vi = ins[2]
            self.w(d, "rt.ev_assign(%d, %d, %r, %s)" % (ins[1], vi.id, tag_of(vi.type), self.var(vi)))
        elif op == "ev_item":
            vi = ins[2]
            self.w(d, "rt.ev_item(%d, %d, %s, %r, %s)" % (ins[1], vi.id, ins[3], tag_of(vi.type[1]), ins[4]))
        elif op == "ev_push":
            vi = ins[2]
            self.w(d, "rt.ev_push(%d, %d, %r, %s)" % (ins[1], vi.id, tag_of(vi.type[1]), ins[3]))
        elif op == "ev_pop":
            vi = ins[2]
            self.w(d, "rt.ev_pop(%d, %d, len(%s))" % (ins[1], vi.id, self.var(vi)))
        elif op == "call":
            t, fn, args, c = ins[1], ins[2], ins[3], ins[4]
            a = ", ".join(self.arg(x) for x in args)
            if fn in REFUSING:
                self.w(d, "%s = rt.%s(%s, %s)" % (t, fn, a, self.clause(c)))
            else:
                self.w(d, "%s = Rt.%s(%s)" % (t, fn, a))
        elif op == "cmp":
            t, o, ty, a, b = ins[1:]
            self.w(d, "%s = (%s %s %s)" % (t, a, o, b))
        elif op == "pred":
            t, o, ty, a = ins[1:]
            expr = {"even": "%s %% 2 == 0", "odd": "%s %% 2 != 0", "zero": "%s == 0",
                    "positive": "%s > 0", "negative": "%s < 0"}[o] % a
            self.w(d, "%s = (%s)" % (t, expr))
        elif op == "not":
            self.w(d, "%s = not %s" % (ins[1], ins[2]))
        elif op == "if":
            self.w(d, "if %s:" % ins[1])
            self.block(d + 1, ins[2])
            if ins[3]:
                self.w(d, "else:")
                self.block(d + 1, ins[3])
        elif op == "loop":
            self.w(d, "while True:")
            self.block(d + 1, ins[1])
        elif op == "break_unless":
            self.w(d, "if not %s:" % ins[1])
            self.w(d + 1, "break")
        elif op == "fuel":
            self.w(d, "if %s == %d:" % (ins[1], ins[2]))
            self.w(d + 1, "rt.refuse(\"FUEL-EXHAUSTED\", %d)" % ins[3])
            self.w(d, "%s += 1" % ins[1])
        elif op == "for":
            self.w(d, "if %s <= %s:" % (ins[1], ins[2]))
            self.w(d + 1, "while True:")
            self.block(d + 2, ins[3])
        elif op == "break_if_eq":
            self.w(d, "if %s == %s:" % (ins[1], ins[2]))
            self.w(d + 1, "break")
        elif op == "incr":
            self.w(d, "%s += 1" % ins[1])
        elif op == "perform":
            self.w(d, "%s(st, rt)" % ins[1])
        elif op == "must":
            self.w(d, "rt.must(%d, %d, %s)" % (ins[1], ins[2], ins[3]))
        elif op == "claim":
            i, c, t, snap, ref = ins[1:]
            refcost = "st.cost%d" % ref if ref else "0"
            self.w(d, "rt.claim(%d, %d, %s, rt.ops - %s, %d, %s)" % (i, c, t, snap, ref, refcost))
        elif op == "say":
            c, t, ty = ins[1], ins[2], ins[3]
            self.w(d, "rt.s_reset(%d)" % c)
            self.append_part(d, t, ty)
            self.w(d, "rt.say(%d)" % c)
        elif op == "cat":
            t, parts, c = ins[1], ins[2], ins[3]
            self.w(d, "rt.s_reset(%s)" % self.clause(c))
            for p, ty in parts:
                self.append_part(d, p, ty)
            self.w(d, "%s = rt.s_take()" % t)
        elif op == "list_new":
            self.w(d, "%s = rt.l_new(%s, %s, %s)" % (ins[1], ins[2], ins[3], self.clause(ins[4])))
        elif op == "list_lit":
            self.w(d, "%s = [%s]" % (ins[1], ", ".join(ins[2])))
        elif op == "list_get":
            self.w(d, "%s = rt.l_get(%s, %s, %s)" % (ins[1], self.var(ins[2]), ins[3], self.clause(ins[4])))
        elif op == "list_set":
            self.w(d, "rt.l_set(%s, %s, %s, %s)" % (self.var(ins[1]), ins[2], ins[3], self.clause(ins[4])))
        elif op == "list_push":
            self.w(d, "rt.l_push(%s, %s, %s)" % (self.var(ins[1]), ins[2], self.clause(ins[3])))
        elif op == "list_pop":
            self.w(d, "rt.l_pop(%s, %s)" % (self.var(ins[1]), self.clause(ins[2])))
        elif op == "list_len":
            self.w(d, "%s = len(%s)" % (ins[1], self.var(ins[2])))
        elif op == "rule":
            self.w(d, "%s = %s(st, rt, %s)" % (ins[1], ins[2], self.clause(ins[3])))
        elif op == "maximal":
            m, a, killers = ins[1:]
            self.w(d, "%s = %s and not (%s)" % (m, a, " or ".join(killers)) if killers else "%s = %s" % (m, a))
        elif op == "any":
            self.w(d, "%s = %s" % (ins[1], " or ".join(ins[2])))
        elif op == "refuse_unless":
            self.w(d, "if not %s:" % ins[1])
            self.w(d + 1, "rt.refuse(%r, %s)" % (ins[2], self.clause(ins[3])))
        elif op == "rule_keep":
            have, val, v = ins[1], ins[2], ins[3]
            self.w(d, "if not %s:" % have)
            self.w(d + 1, "%s = %s" % (val, v))
            self.w(d + 1, "%s = True" % have)
        elif op == "rule_conflict":
            val, v, ty, c = ins[1:]
            self.w(d, "if not (%s == %s):" % (v, val))
            self.w(d + 1, "rt.refuse(\"RULE-CONFLICT\", %s)" % self.clause(c))
        elif op == "return":
            self.w(d, "return %s" % ins[1])
        else:
            raise AssertionError(ins)

    def append_part(self, d, t, ty):
        if isinstance(ty, tuple):
            self.w(d, "rt.s_list(%r, %s)" % (TAGS[ty[1]], t))
        else:
            fn = {"int": "s_i", "fix": "s_x", "float": "s_f", "bool": "s_b", "text": "s_t"}[ty]
            self.w(d, "rt.%s(%s)" % (fn, t))

    def default(self, t):
        if isinstance(t, tuple):
            return "[]"
        return {"int": "0", "fix": "0", "u64": "0", "float": "0.0", "bool": "False", "text": "b''"}[t]

    def emit_fn(self, f, params):
        self.w(0, "def %s(%s):" % (f.name, params))
        for vid, t in sorted(f.locals.items()):
            self.w(1, "v%d = %s" % (vid, self.default(t)))
        for name, t in f.temps:
            self.w(1, "%s = %s" % (name, self.default(t)))
        self.block(1, f.body)
        self.w(0, "")

    def program(self):
        low = self.low
        comp = low.comp
        with open(os.path.join(HERE, "rt_py.py"), "r", encoding="utf-8") as fh:
            runtime = fh.read()
        self.w(0, "# Generated by the Orlog OL-0 Python backend. Law %s (%s)." % (comp.law_seal, comp.seal_words))
        self.lines.append(runtime.rstrip("\n"))
        self.w(0, "")
        self.w(0, "LAW_SEAL = %r" % comp.law_seal)
        self.w(0, "TEXT_SEAL = %r" % comp.text_seal)
        self.w(0, "CLAIM_CLAUSES = %r" % [c.id for c in comp.an.claims])
        self.w(0, "")
        self.w(0, "class St:")
        fields = ["v%d" % v.id for v in low.top_vars] + ["cost%d" % c for c in low.cost_clauses]
        self.w(1, "__slots__ = (%s)" % "".join("%r, " % f for f in fields))
        self.w(1, "def __init__(self):")
        if not fields:
            self.w(2, "pass")
        for v in low.top_vars:
            self.w(2, "self.v%d = %s" % (v.id, self.default(v.type)))
        for c in low.cost_clauses:
            self.w(2, "self.cost%d = 0" % c)
        self.w(0, "")
        for c, f in low.procs:
            self.emit_fn(f, "st, rt")
        for name, f in low.rules:
            self.emit_fn(f, "st, rt, clause")
        self.emit_fn(low.main, "st, rt")
        self.w(0, "if __name__ == \"__main__\":")
        self.w(1, "_rt = Rt(\"python\", LAW_SEAL, TEXT_SEAL, CLAIM_CLAUSES, _sys.argv)")
        self.w(1, "orl_main(St(), _rt)")
        self.w(1, "_rt.finish()")
        return "\n".join(self.lines) + "\n"


def generate(low):
    return PyGen(low).program()

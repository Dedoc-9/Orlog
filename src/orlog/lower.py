"""The typed law -> three-address code, shared by the three backends.

Evaluation order and operation counting are decided here, once: C leaves the order of
operand evaluation unspecified, so a refusal raised by one operand or the other could
differ between compilers if expressions were printed whole. Every operand is put into a
temporary, left to right, and every counted operation is an explicit tick.

The reference interpreter does not use this module: it walks the tree itself. A lowering
mistake therefore shows up as a mismatch against the reference, not as a shared error.
"""
from .syntax import (Num, Str, BoolLit, Var, Bin, Un, Conv, Item, Length, ListOf, ListLit, Seal, Cat,
                     Let, SetS, Change, Say, IfS, While, For, ProcDef, Perform, Must, Claim, Define, Append,
                     RemoveLast, Decimals, BLOCK)

ARITH = {
    "int": {"+": "i_add", "-": "i_sub", "*": "i_mul", "/": "i_div", "max": "i_max", "min": "i_min"},
    "fix": {"+": "x_add", "-": "x_sub", "*": "x_mul", "/": "x_div", "max": "x_max", "min": "x_min"},
    "float": {"+": "f_add", "-": "f_sub", "*": "f_mul", "/": "f_div", "max": "f_max", "min": "f_min"},
}
UNARY = {"neg": {"int": "i_neg", "fix": "x_neg", "float": "f_neg"},
         "abs": {"int": "i_abs", "fix": "x_abs", "float": "f_abs"},
         "sqrt": {"int": "i_isqrt", "fix": "x_sqrt", "float": "f_sqrt"},
         "trunc": {"fix": "x_trunc", "float": "f_trunc"}}
# which runtime functions can refuse (take a clause) -- the rest are pure
REFUSING = {"i_add", "i_sub", "i_mul", "i_div", "i_quot", "i_rem", "i_neg", "i_abs", "i_isqrt",
            "x_from_i", "x_add", "x_sub", "x_mul", "x_div", "x_neg", "x_abs", "x_sqrt",
            "x_to_f", "f_to_x", "f_from_i", "f_trunc", "f_round", "x_as_i", "f_as_i"}


class Fn:
    def __init__(self, name, kind, ret=None):
        self.name, self.kind, self.ret = name, kind, ret     # kind: main | proc | rule
        self.temps = []                                       # [(name, type)]
        self.locals = {}                                      # var id -> type
        self.body = []


class Lowered:
    def __init__(self, comp):
        self.comp = comp
        self.prog, self.an = comp.prog, comp.an
        self.top_vars = [v for v in self.an.vars if v.top]
        self.cost_clauses = [c.id for c in self.prog.clauses if c.cost_tracked]
        self.procs = []
        self.rules = []
        self.main = Fn("orl_main", "main")
        self.cur = None
        self.clause_id = 0
        self.marks = 0
        # names first: a procedure or a rule may use a rule (red team E2a, E2b: these crashed when assigned late)
        self.rule_fn = {name: "rule_%d" % cls[0].id for name, cls in self.an.rules.items()}
        for c in self.prog.top:
            if isinstance(c.stmt, ProcDef):
                f = Fn("proc_%d" % c.id, "proc")
                self.with_fn(f, lambda c=c: self.seq(c.children))
                self.procs.append((c, f))
        for name, cls in self.an.rules.items():
            f = Fn(self.rule_fn[name], "rule", self.an.rule_types[name])
            self.with_fn(f, lambda name=name: self.rule_body(name))
            self.rules.append((name, f))
        self.proc_fn = {c.id: f.name for c, f in self.procs}
        self.with_fn(self.main, lambda: self.seq(self.prog.top))

    # ---------------------------------------------- plumbing
    def with_fn(self, f, thunk):
        saved = self.cur, getattr(self, "out", None)
        self.cur, self.out = f, f.body
        thunk()
        self.cur, self.out = saved

    def temp(self, typ):
        name = "t%d" % len(self.cur.temps)
        self.cur.temps.append((name, typ))
        return name

    def emit(self, *ins):
        self.out.append(ins)

    def sub(self, thunk):
        saved = self.out
        self.out = []
        thunk()
        block, self.out = self.out, saved
        return block

    def var_ref(self, vi):
        if not vi.top:
            self.cur.locals[vi.id] = vi.type
        return vi

    def mark(self):
        """A mark on the temp stack (red team E21). Only the C backend acts on it: the temporaries a statement made
        are released back to its mark when it ends. Python and Rust own their texts by value and emit nothing."""
        name = "m%d" % self.marks
        self.marks += 1
        self.emit("tmark", name)
        return name

    # ---------------------------------------------- statements
    def seq(self, clauses):
        for c in clauses:
            if c.absorbed or isinstance(c.stmt, (Define, ProcDef, Decimals)):
                continue
            m = self.mark()
            if c.cost_tracked:
                s = self.temp("u64")
                self.emit("snap", s)
                self.stmt(c, c.stmt)
                self.emit("cost_add", c.id, s)
            else:
                self.stmt(c, c.stmt)
            self.emit("trelease", m)

    def body(self, c, b):
        if isinstance(b, tuple) and b[0] == BLOCK:
            self.seq(b[1].children)
        else:
            self.stmt(c, b)

    def stmt(self, c, s):
        cid = c.id
        if isinstance(s, Let) or (isinstance(s, SetS) and s.index is None):
            self.emit("tick")
            t = self.expr(cid, s.expr)
            vi = self.var_ref(s.var)
            self.emit("write", vi, t)
            self.emit("ev_assign", cid, vi)
        elif isinstance(s, SetS):
            self.emit("tick")
            k = self.expr(cid, s.index)
            v = self.expr(cid, s.expr)
            vi = self.var_ref(s.var)
            self.emit("list_set", vi, k, v, cid)
            self.emit("ev_item", cid, vi, k, v)
        elif isinstance(s, Change):
            op = ARITH[s.elem]["+" if s.sign == "+" else "-"]
            vi = self.var_ref(s.var)
            self.emit("tick")
            if s.index is None:
                cur = self.temp(s.elem)
                self.emit("read", cur, vi)
                v = self.expr(cid, s.expr)
                self.emit("tick")
                new = self.temp(s.elem)
                self.emit("call", new, op, [cur, v], cid)
                self.emit("write", vi, new)
                self.emit("ev_assign", cid, vi)
            else:
                k = self.expr(cid, s.index)
                self.emit("tick")
                cur = self.temp(s.elem)
                self.emit("list_get", cur, vi, k, cid)
                v = self.expr(cid, s.expr)
                self.emit("tick")
                new = self.temp(s.elem)
                self.emit("call", new, op, [cur, v], cid)
                self.emit("list_set", vi, k, new, cid)
                self.emit("ev_item", cid, vi, k, new)
        elif isinstance(s, Say):
            self.emit("tick")
            t = self.expr(cid, s.expr)
            self.emit("say", cid, t, s.expr.type)
        elif isinstance(s, IfS):
            self.if_chain(s)
        elif isinstance(s, While):
            n = self.temp("u64")
            self.emit("set_u64", n, 0)

            def loop_body():
                m = self.mark()      # one iteration's temporaries, its condition's among them (E21)
                self.emit("tick")
                cnd = self.expr(cid, s.cond)
                self.emit("break_unless", cnd)
                self.emit("fuel", n, s.fuel, cid)
                self.seq(c.children)
                self.emit("trelease", m)
            self.emit("loop", self.sub(loop_body))
        elif isinstance(s, For):
            self.emit("tick")
            lo = self.expr(cid, s.lo)
            hi = self.expr(cid, s.hi)
            k = self.temp("int")
            self.emit("copy", k, lo)
            vi = self.var_ref(s.var)

            def for_body():
                self.emit("tick")
                self.emit("write", vi, k)
                self.emit("ev_assign", cid, vi)
                self.seq(c.children)
                self.emit("break_if_eq", k, hi)
                self.emit("incr", k)
            self.emit("for", k, hi, self.sub(for_body))
        elif isinstance(s, Perform):
            self.emit("tick")
            self.emit("perform", "proc_%d" % s.proc.id)
        elif isinstance(s, Must):
            self.emit("tick")
            t = self.expr(cid, s.cond)
            self.emit("must", s.id, cid, t)
        elif isinstance(s, Claim):
            self.emit("tick")
            snap = self.temp("u64")
            self.emit("snap", snap)
            t = self.expr(cid, s.cond)
            ref = s.ref.id if s.oracle[0] == "certificate" else 0
            self.emit("claim", s.id, cid, t, snap, ref)
        elif isinstance(s, Append):
            self.emit("tick")
            v = self.expr(cid, s.expr)
            vi = self.var_ref(s.var)
            self.emit("list_push", vi, v, cid)
            self.emit("ev_push", cid, vi, v)
        elif isinstance(s, RemoveLast):
            self.emit("tick")
            vi = self.var_ref(s.var)
            self.emit("list_pop", vi, cid)
            self.emit("ev_pop", cid, vi)
        else:
            raise AssertionError(s)

    def if_chain(self, s):
        """Arms lowered iteratively behind a 'done' flag: constant nesting for a chain of any length. A nested
        else-if chain broke the Python backend at 110 arms and the lowering's own recursion at 3000 (red team E10)."""
        done = self.temp("bool")
        self.emit("const", done, "bool", False)

        def arm(cond, b, ac):
            self.emit("tick")
            t = self.expr(ac.id, cond)

            def taken():
                self.body(ac, b)
                self.emit("const", done, "bool", True)
            self.emit("if", t, self.sub(taken), [])

        def unless_done(thunk):
            nd = self.temp("bool")
            self.emit("not", nd, done)
            self.emit("if", nd, self.sub(thunk), [])

        for i, (cond, b, ac) in enumerate(s.arms):
            if i == 0:
                arm(cond, b, ac)
            else:
                unless_done(lambda cond=cond, b=b, ac=ac: arm(cond, b, ac))
        if s.els is not None:
            unless_done(lambda: self.body(s.els[1], s.els[0]))

    def rule_body(self, name):
        cls = self.an.rules[name]
        beats = self.an.overrides[name]
        rtype = self.an.rule_types[name]
        cid = "CLAUSE"          # the use site's clause, a parameter of the rule's function
        self.emit("tick")
        app = {}
        for c in cls:
            a = self.temp("bool")
            if c.stmt.proviso is None:
                self.emit("const", a, "bool", True)
            else:
                p = self.expr(cid, c.stmt.proviso)
                self.emit("copy", a, p)
            app[c.id] = a
        mx = {}
        for c in cls:
            m = self.temp("bool")
            killers = [app[o.id] for o in cls if o.id != c.id and c.id in beats[o.id]]
            self.emit("maximal", m, app[c.id], killers)
            mx[c.id] = m
        anym = self.temp("bool")
        self.emit("any", anym, [mx[c.id] for c in cls])
        self.emit("refuse_unless", anym, "RULE-UNDEFINED", cid)
        have = self.temp("bool")
        val = self.temp(rtype)
        self.emit("const", have, "bool", False)
        vals = []
        for c in cls:
            def eval_value(c=c):
                v = self.expr(cid, c.stmt.expr)
                vals.append((c.id, v))
                self.emit("rule_keep", have, val, v, rtype)
            self.emit("if", mx[c.id], self.sub(eval_value), [])
        seen = self.temp("bool")          # compare every later maximal value with the first, never the first with itself
        self.emit("const", seen, "bool", False)
        for c in cls:
            v = dict(vals)[c.id]
            later = [("rule_conflict", val, v, rtype, cid)]
            first = [("const", seen, "bool", True)]
            self.emit("if", mx[c.id], [("if", seen, later, first)], [])
        self.emit("return", val)

    # ---------------------------------------------- expressions
    def expr(self, cid, e):
        if isinstance(e, Num):
            t = self.temp(e.type)
            self.emit("const", t, e.type, e.value)
            return t
        if isinstance(e, Str):
            t = self.temp("text")
            self.emit("const", t, "text", e.value.encode("utf-8"))
            return t
        if isinstance(e, BoolLit):
            t = self.temp("bool")
            self.emit("const", t, "bool", e.value)
            return t
        if isinstance(e, Seal):
            t = self.temp("text")
            self.emit("const", t, "text", self.comp.seal_words.encode("ascii"))
            return t
        if isinstance(e, Var):
            if e.rule:
                t = self.temp(e.type)
                self.emit("rule", t, self.rule_fn[e.rule], cid)
                return t
            vi = self.var_ref(e.var)
            t = self.temp(e.type)
            self.emit("read", t, vi)
            return t
        if isinstance(e, Bin):
            if e.op in ("and", "or"):
                a = self.expr(cid, e.a)
                self.emit("tick")
                r = self.temp("bool")

                def take_b():
                    b = self.expr(cid, e.b)
                    self.emit("copy", r, b)
                if e.op == "and":
                    self.emit("if", a, self.sub(take_b), [("const", r, "bool", False)])
                else:
                    self.emit("if", a, [("const", r, "bool", True)], self.sub(take_b))
                return r
            a = self.expr(cid, e.a)
            b = self.expr(cid, e.b)
            self.emit("tick")
            if e.op in ("quot", "rem"):
                t = self.temp("int")
                self.emit("call", t, "i_quot" if e.op == "quot" else "i_rem", [a, b], cid)
                return t
            if e.op in ARITH["int"]:
                t = self.temp(e.type)
                self.emit("call", t, ARITH[e.type][e.op], [a, b], cid)
                return t
            t = self.temp("bool")
            self.emit("cmp", t, e.op, e.a.type, a, b)
            return t
        if isinstance(e, Un):
            a = self.expr(cid, e.a)
            self.emit("tick")
            if e.op == "not":
                t = self.temp("bool")
                self.emit("not", t, a)
                return t
            if e.op in ("even", "odd", "zero", "positive", "negative"):
                t = self.temp("bool")
                self.emit("pred", t, e.op, e.a.type, a)
                return t
            t = self.temp(e.type)
            self.emit("call", t, UNARY[e.op][e.a.type], [a], cid)
            return t
        if isinstance(e, Conv):
            a = self.expr(cid, e.a)
            self.emit("tick")
            t = self.temp(e.type)
            src, tgt, mode = e.a.type, e.target, e.mode
            if mode == "promote":
                if tgt == "fix":
                    self.emit("call", t, "x_from_i", [a], cid)
                else:
                    self.emit("call", t, "f_from_i", [a, ("flag", 0)], cid)
            elif tgt == "int":
                if mode == "rounded":
                    self.emit("call", t, "x_round" if src == "fix" else "f_round", [a], cid)
                else:
                    self.emit("call", t, "x_as_i" if src == "fix" else "f_as_i", [a], cid)
            elif tgt == "fix":
                if src == "int":
                    self.emit("call", t, "x_from_i", [a], cid)
                else:
                    self.emit("call", t, "f_to_x", [a, ("flag", int(mode == "rounded"))], cid)
            else:
                if src == "int":
                    self.emit("call", t, "f_from_i", [a, ("flag", int(mode == "rounded"))], cid)
                else:
                    self.emit("call", t, "x_to_f", [a, ("flag", int(mode == "rounded"))], cid)
            return t
        if isinstance(e, Cat):
            parts = [(self.expr(cid, p), p.type) for p in e.parts]
            self.emit("ops", len(parts) - 1)
            t = self.temp("text")
            self.emit("cat", t, parts, cid)
            return t
        if isinstance(e, Item):
            k = self.expr(cid, e.index)
            self.emit("tick")
            vi = self.var_ref(e.var)
            t = self.temp(e.type)
            self.emit("list_get", t, vi, k, cid)
            return t
        if isinstance(e, Length):
            self.emit("tick")
            vi = self.var_ref(e.var)
            t = self.temp("int")
            self.emit("list_len", t, vi)
            return t
        if isinstance(e, ListOf):
            n = self.expr(cid, e.count)
            v = self.expr(cid, e.value)
            self.emit("tick")
            t = self.temp(e.type)
            self.emit("list_new", t, n, v, cid)
            return t
        if isinstance(e, ListLit):
            items = [self.expr(cid, x) for x in e.items]
            self.emit("tick")
            t = self.temp(e.type)
            self.emit("list_lit", t, items)
            return t
        raise AssertionError(e)

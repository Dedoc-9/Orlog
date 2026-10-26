"""Static semantics: types, scopes, ids, promotions, rule priority, and the law's bytes.

Two identities are kept apart:
  text-seal  sha256 of the canonical text: the document (notes, title, wording, stamps)
  law-seal   sha256 of the typed law below: the meaning (what runs, with what values)
Rewording a note changes the first and not the second; changing 0.1 to 0.10 changes neither.
"""
import hashlib
import struct
from fractions import Fraction

from . import numeric_ref as N
from .syntax import (OrlogError, Num, Str, BoolLit, Var, Bin, Un, Conv, Item, Length, ListOf, ListLit, Seal, Cat,
                     Let, SetS, Change, Say, IfS, While, For, ProcDef, Perform, Must, Claim, Define, Append,
                     RemoveLast, Decimals, BLOCK)

NUMERIC = ("int", "fix", "float")
LOOP_NESTING_MAX = 16
ELEMS = ("int", "fix", "float", "bool")


def is_list(t):
    return isinstance(t, tuple) and t[0] == "list"


def tname(t):
    return "list of %s" % t[1] if is_list(t) else t


class ClaimSite:
    """One claim statement and the clause it stands in. Two inline claims can share a clause (court finding L17), so
    the court keys claims by their claim id; `id` stays the clause id that receipts print."""
    __slots__ = ("id", "label", "text", "clause", "stmt")

    def __init__(self, clause, stmt):
        self.id, self.label, self.text = clause.id, clause.label, clause.text
        self.clause, self.stmt = clause, stmt


class VarInfo:
    __slots__ = ("id", "name", "type", "top", "loop")

    def __init__(self, vid, name, typ, top, loop=False):
        self.id, self.name, self.type, self.top, self.loop = vid, name, typ, top, loop


class Analysis:
    def __init__(self, prog):
        self.prog = prog
        self.notes = []
        self.decimals = "fixed"
        self.decimals_clause = None
        self.first_decimal = None
        self.vars = []
        self.scopes = []
        self.procs = {}
        self.rules = {}
        self.rule_types = {}
        self.claims = []
        self.musts = []
        self.overrides = {}
        self.clause_of_stmt = {}
        self.loop_depth = 0

    def err(self, code, c, msg):
        raise OrlogError(code, c.line, "§%s: %s" % (c.label, msg))

    # -------------------------------------------------- driver
    def run(self):
        p = self.prog
        for c in p.clauses:
            if isinstance(c.stmt, Define):
                if c.parent is not None:
                    self.err("DEFINE-PLACE", c, "a Define stands at the top level")
                self.rules.setdefault(c.stmt.name, []).append(c)
        self.scopes = [{}]
        for c in p.top:
            if c.absorbed:
                continue
            self.clause(c)
        self._override_closure()
        return self

    def visible(self, name):
        for s in reversed(self.scopes):
            if name in s:
                return s[name]
        return None

    def declare(self, c, name, typ, loop=False):
        if self.visible(name) is not None:
            self.err("REDECLARED", c, "'%s' is already declared (shadowing is refused)" % name)
        if name in self.rules:
            self.err("REDECLARED", c, "'%s' already names a definition" % name)
        if name.lower() in self.procs:         # a procedure already defined, its name lowercased (SPEC §11 item 47)
            self.err("REDECLARED", c, "'%s' is the name of a procedure already defined" % name)
        vi = VarInfo(len(self.vars), name, typ, len(self.scopes) == 1, loop)
        self.vars.append(vi)
        self.scopes[-1][name] = vi
        return vi

    # -------------------------------------------------- statements
    def block(self, clauses):
        self.scopes.append({})
        for c in clauses:
            if not c.absorbed:
                self.clause(c)
        self.scopes.pop()

    def clause(self, c):
        self.cur = c
        self.stmt(c, c.stmt, top=c.parent is None)

    def body(self, c, b):
        if isinstance(b, tuple) and b[0] == BLOCK:
            self.block(b[1].children)
        else:
            self.scopes.append({})
            self.stmt(c, b, top=False)
            self.scopes.pop()

    def stmt(self, c, s, top):
        if isinstance(s, Let):
            t = self.expr(c, s.expr)
            s.var = self.declare(c, s.name, t)
        elif isinstance(s, SetS):
            # parts in written order (§13): 'Set item I of X to E' checks I, then X, then E
            if s.index is not None:
                self.want(c, s.index, "int")
            vi = self.lookup_var(c, s.name)
            if vi.loop:
                self.err("LOOP-VARIABLE", c, "a For's counter cannot be set")
            s.var = vi
            if s.index is not None:
                if not is_list(vi.type):
                    self.err("TYPE", c, "'%s' is not a list" % s.name)
                s.expr = self.assignable(c, s.expr, vi.type[1])
            else:
                s.expr = self.assignable(c, s.expr, vi.type)
        elif isinstance(s, Change):
            if s.index is not None:
                self.want(c, s.index, "int")
            vi = self.lookup_var(c, s.name)
            if vi.loop:
                self.err("LOOP-VARIABLE", c, "a For's counter cannot be changed")
            s.var = vi
            t = vi.type
            if s.index is not None:
                if not is_list(t):
                    self.err("TYPE", c, "'%s' is not a list" % s.name)
                t = t[1]
            if t not in NUMERIC:
                self.err("TYPE", c, "only a number can be increased or decreased")
            s.expr = self.assignable(c, s.expr, t)
            s.elem = t
        elif isinstance(s, Say):
            self.expr(c, s.expr)
        elif isinstance(s, IfS):
            for cond, b, ac in s.arms:
                self.want(ac, cond, "bool")
                self.body(ac, b)
            if s.els is not None:
                self.body(s.els[1], s.els[0])
        elif isinstance(s, While):
            self.enter_loop(c)              # its place first, as a To's (SPEC §14, the twin's round 3)
            self.want(c, s.cond, "bool")
            if not (1 <= s.fuel <= (1 << 62)):
                self.err("FUEL", c, "a While's bound is between 1 and 2^62")
            self.block(c.children)
            self.loop_depth -= 1
        elif isinstance(s, For):
            self.enter_loop(c)              # its place first (SPEC §14)
            self.want(c, s.lo, "int")
            self.want(c, s.hi, "int")
            self.scopes.append({})
            s.var = self.declare(c, s.name, "int", loop=True)
            self.block(c.children)
            self.loop_depth -= 1
            self.scopes.pop()
        elif isinstance(s, ProcDef):
            if not top:
                self.err("PROCEDURE-PLACE", c, "a procedure is defined at the top level")
            if s.name in self.procs:
                self.err("REDECLARED", c, "procedure '%s' is defined twice" % s.name)
            # §13, §5's rule read both ways: a procedure may not take the lowercased name of a visible variable (the
            # converse of item 47) or of any rule (rules are collected first)
            if any(v.lower() == s.name for scope in self.scopes for v in scope):
                self.err("REDECLARED", c, "procedure '%s' is the name of a visible variable" % s.name)
            if any(r.lower() == s.name for r in self.rules):
                self.err("REDECLARED", c, "procedure '%s' is the name of a definition" % s.name)
            saved = self.scopes
            self.scopes = [dict(self.scopes[0])]
            self.proc_ctx = c
            saved_loops, self.loop_depth = self.loop_depth, 0     # a procedure is its own function in every backend
            self.block(c.children)          # checked before the name exists: a body cannot perform itself
            self.loop_depth = saved_loops
            self.procs[s.name] = c
            self.proc_ctx = None
            self.scopes = saved
        elif isinstance(s, Perform):
            callee = self.procs.get(s.name)
            if callee is None:
                self.err("PERFORM-BEFORE-DEFINITION", c,
                         "'%s' is performed before (or inside) its own definition; recursion is refused" % s.name)
            s.proc = callee
        elif isinstance(s, Must):
            self.want(c, s.cond, "bool")
            s.id = len(self.musts)
            self.musts.append(c)
        elif isinstance(s, Claim):
            self.want(c, s.cond, "bool")
            s.id = len(self.claims)
            self.claims.append(ClaimSite(c, s))
            o = s.oracle
            if o[0] == "certificate":
                tgt = self.ref_clause(c, o[1])
                if tgt.id >= c.id or tgt.absorbed or isinstance(tgt.stmt, (ProcDef, Define, Decimals, Claim)):
                    self.err("CERTIFICATE-TARGET", c, "the certificate's clause must be an earlier, executed clause")
                tgt.cost_tracked = True
                s.ref = tgt
            elif o[0] == "agreement":
                for r in o[1:]:
                    tgt = self.ref_clause(c, r)
                    if tgt.id >= c.id:
                        self.err("AGREEMENT-TARGET", c, "the agreeing clauses must come earlier")
            for r in s.premises:
                tgt = self.ref_clause(c, r)
                if not isinstance(tgt.stmt, Claim):
                    self.err("PREMISE-TARGET", c, "a premise names another claim's clause")
        elif isinstance(s, Define):
            s.over = []                     # written first, checked first (§13)
            for r in s.overrides:
                tgt = self.ref_clause(c, r)
                if not isinstance(tgt.stmt, Define) or tgt.stmt.name != s.name:
                    self.err("NOTWITHSTANDING-TARGET", c, "§%s is not a definition of '%s'" % (r, s.name))
                s.over.append(tgt)
            # Unreachable, kept as a guard: declare() refuses any variable named as a rule, and rules are collected
            # before the walk, so no variable of this name can be visible here (found settling §13).
            if s.name in [v.name for v in self.vars] and self.visible(s.name):
                self.err("REDECLARED", c, "'%s' is a variable" % s.name)
            if s.name.lower() in self.prog.proc_names:      # §13: any procedure, as the To clause's check is any rule
                self.err("REDECLARED", c, "'%s' is the name of a procedure" % s.name)
            t = self.expr(c, s.expr)
            if s.name in self.rule_types and self.rule_types[s.name] != t:
                self.err("TYPE", c, "every definition of '%s' has one type" % s.name)
            if is_list(t):
                self.err("TYPE", c, "a definition's value is a single value")
            self.rule_types[s.name] = t
            if s.proviso is not None:
                self.want(c, s.proviso, "bool")
        elif isinstance(s, Append):
            got = self.expr(c, s.expr)      # 'Append E to X': E, then X, then whether E fits X (§13)
            vi = self.lookup_var(c, s.list)
            if not is_list(vi.type):
                self.err("TYPE", c, "'%s' is not a list" % s.list)
            s.var = vi
            s.expr = self.fit(c, s.expr, got, vi.type[1])
        elif isinstance(s, RemoveLast):
            vi = self.lookup_var(c, s.list)
            if not is_list(vi.type):
                self.err("TYPE", c, "'%s' is not a list" % s.list)
            s.var = vi
        elif isinstance(s, Decimals):
            if not top or self.decimals_clause is not None or self.first_decimal is not None:
                self.err("DECIMALS-PLACE", c, "say how decimals are read once, at the top, before any decimal")
            self.decimals = s.mode
            self.decimals_clause = c
        else:
            self.err("INTERNAL", c, "unknown statement %r" % s)

    def enter_loop(self, c):
        self.loop_depth += 1
        if self.loop_depth > LOOP_NESTING_MAX:
            self.err("LOOP-NESTING", c, "loops nest at most %d deep within one body: the Python backend's host allows "
                     "20 static blocks (red team E10b)" % LOOP_NESTING_MAX)

    def lookup_var(self, c, name):
        vi = self.visible(name)
        if vi is None:
            self.err("UNDECLARED", c, "'%s' is not declared here" % name)
        return vi

    def ref_clause(self, c, label):
        tgt = self.prog.by_label.get(label)
        if tgt is None:
            self.err("UNKNOWN-CLAUSE", c, "there is no §%s" % label)
        return tgt

    # -------------------------------------------------- expressions
    def want(self, c, e, t):
        got = self.expr(c, e)
        if got != t:
            self.err("TYPE", c, "expected %s, found %s" % (tname(t), tname(got)))

    def promote(self, e, t):
        p = Conv("promote", t, e)
        p.line, p.type = e.line, t
        return p

    def assignable(self, c, e, t):
        return self.fit(c, e, self.expr(c, e), t)

    def fit(self, c, e, got, t):
        """An expression already typed (as got) stored where a t is held: as it is, promoted, or TYPE."""
        if got == t:
            return e
        if got == "int" and t in ("fix", "float"):
            return self.promote(e, t)
        self.err("TYPE", c, "a %s cannot be stored where a %s is held" % (tname(got), tname(t)))

    def unify(self, c, e, typed=None):
        """Arithmetic operands: equal numeric types, or an Int promoted to the other side."""
        ta, tb = typed if typed is not None else (self.expr(c, e.a), self.expr(c, e.b))
        if ta == tb and ta in NUMERIC:
            return ta
        if ta == "int" and tb in ("fix", "float"):
            e.a = self.promote(e.a, tb)
            return tb
        if tb == "int" and ta in ("fix", "float"):
            e.b = self.promote(e.b, ta)
            return ta
        self.err("TYPE", c, "'%s' between %s and %s" % (e.op, tname(ta), tname(tb)))

    def expr(self, c, e):
        t = self._expr(c, e)
        e.type = t
        return t

    def _expr(self, c, e):
        if isinstance(e, Num):
            if "." not in e.text:
                v = int(e.text)
                if v > N.I64_MAX:
                    self.err("LITERAL-RANGE", c, "%s does not fit a 64-bit integer" % e.text)
                e.value = v
                return "int"
            if self.first_decimal is None:
                self.first_decimal = c
            exact = Fraction(e.text)
            if self.decimals == "fixed":
                raw = N.round_half_even(exact * N.ONE)
                if raw > N.I64_MAX:
                    self.err("LITERAL-RANGE", c, "%s does not fit Q31.32" % e.text)
                if Fraction(raw, N.ONE) != exact:
                    self.notes.append({"note": "LITERAL-ROUNDED", "clause": c.label, "literal": e.text,
                                       "stored": N.fmt_x(raw), "rule": "nearest Q31.32, ties to even"})
                e.value = raw
                return "fix"
            try:
                f = float(exact)        # CPython raises OverflowError beyond binary64 (found by the twin's notes, 38)
            except OverflowError:
                f = float("inf")
            if f == float("inf"):
                self.err("LITERAL-RANGE", c, "%s does not fit binary64" % e.text)
            if Fraction(f) != exact:
                self.notes.append({"note": "LITERAL-ROUNDED", "clause": c.label, "literal": e.text,
                                   "stored": N.fmt_f(f), "rule": "nearest binary64, ties to even"})
            e.value = f
            return "float"
        if isinstance(e, Str):
            if len(e.value.encode("utf-8")) > N.TEXT_MAX:
                self.err("LITERAL-RANGE", c, "a text literal is too long")
            return "text"
        if isinstance(e, BoolLit):
            return "bool"
        if isinstance(e, Seal):
            return "text"
        if isinstance(e, Var):
            vi = self.visible(e.name)
            if vi is not None:
                e.var, e.rule = vi, None
                return vi.type
            if e.name in self.rules:
                last = max(r.id for r in self.rules[e.name])
                ctx = getattr(self, "proc_ctx", None)
                at = ctx.id if ctx is not None else c.id
                if last >= at or e.name not in self.rule_types:
                    self.err("RULE-BEFORE-DEFINITION", c, "'%s' is used before all its definitions" % e.name)
                e.var, e.rule = None, e.name
                return self.rule_types[e.name]
            self.err("UNDECLARED", c, "'%s' is not declared here" % e.name)
        if isinstance(e, Bin):
            if e.op in ("+", "-", "*", "/", "max", "min"):
                return self.unify(c, e)
            if e.op in ("quot", "rem"):
                ta, tb = self.expr(c, e.a), self.expr(c, e.b)      # both operands, then the operator (§13)
                if ta != "int" or tb != "int":
                    self.err("TYPE", c, "quotient, remainder and modulo take integers")
                return "int"
            if e.op in ("<", ">", "<=", ">="):
                self.unify(c, e)
                return "bool"
            if e.op in ("==", "!="):
                ta, tb = self.expr(c, e.a), self.expr(c, e.b)
                if ta in NUMERIC and tb in NUMERIC:
                    self.unify(c, e, (ta, tb))      # typed once: re-typing a promoted operand crashed (red team E1)
                elif ta != tb or ta not in ("bool", "text"):
                    self.err("TYPE", c, "cannot compare %s with %s" % (tname(ta), tname(tb)))
                return "bool"
            if e.op in ("and", "or"):
                ta, tb = self.expr(c, e.a), self.expr(c, e.b)      # both operands, then the operator (§13)
                if ta != "bool" or tb != "bool":
                    self.err("TYPE", c, "'%s' joins two conditions" % e.op)
                return "bool"
        if isinstance(e, Un):
            ta = self.expr(c, e.a)
            if e.op == "not":
                if ta != "bool":
                    self.err("TYPE", c, "'not' takes a condition")
                return "bool"
            if e.op in ("even", "odd"):
                if ta != "int":
                    self.err("TYPE", c, "only an integer is even or odd")
                return "bool"
            if e.op in ("zero", "positive", "negative"):
                if ta not in NUMERIC:
                    self.err("TYPE", c, "only a number is zero, positive or negative")
                return "bool"
            if e.op in ("neg", "abs", "sqrt"):
                if ta not in NUMERIC:
                    self.err("TYPE", c, "'%s' takes a number" % e.op)
                return ta
            if e.op == "trunc":
                if ta not in ("fix", "float"):
                    self.err("TYPE", c, "the integer part is taken of a fixed or float number")
                return "int"
        if isinstance(e, Conv):
            ta = self.expr(c, e.a)
            if e.mode == "promote":
                return e.target
            ok = {("as", "int"): ("fix", "float"), ("as", "fix"): ("int", "float"),
                  ("as", "float"): ("int", "fix"), ("rounded", "int"): ("fix", "float"),
                  ("rounded", "fix"): ("int", "float"), ("rounded", "float"): ("int", "fix")}
            if ta not in ok[(e.mode, e.target)]:
                self.err("TYPE", c, "cannot convert %s %s %s" % (tname(ta), e.mode, e.target))
            return e.target
        if isinstance(e, Cat):
            for part in e.parts:
                self.expr(c, part)
            return "text"
        if isinstance(e, Item):
            self.want(c, e.index, "int")        # 'item I of X': I, then X (§13)
            vi = self.lookup_var(c, e.list)
            if not is_list(vi.type):
                self.err("TYPE", c, "'%s' is not a list" % e.list)
            e.var = vi
            return vi.type[1]
        if isinstance(e, Length):
            vi = self.lookup_var(c, e.list)
            if not is_list(vi.type):
                self.err("TYPE", c, "'%s' is not a list" % e.list)
            e.var = vi
            return "int"
        if isinstance(e, ListOf):
            self.want(c, e.count, "int")
            tv = self.expr(c, e.value)
            if tv not in ELEMS:
                self.err("TYPE", c, "a list holds integers, fixed, floats or truth values")
            return ("list", tv)
        if isinstance(e, ListLit):
            ts = [self.expr(c, x) for x in e.items]
            target = ts[0]
            for t in ts:
                if t != target:
                    if {t, target} <= set(NUMERIC) and "int" in (t, target):
                        target = t if target == "int" else target
                    else:
                        self.err("TYPE", c, "a list's items share one type")
            if target not in ELEMS:
                self.err("TYPE", c, "a list holds integers, fixed, floats or truth values")
            e.items = [x if x.type == target else self.promote(x, target) for x in e.items]
            return ("list", target)
        self.err("INTERNAL", c, "unknown expression %r" % e)

    # -------------------------------------------------- rule priority
    def _override_closure(self):
        for name, cls in self.rules.items():
            beats = {c.id: set(t.id for t in c.stmt.over) for c in cls}
            changed = True
            while changed:                       # transitive closure, a least fixed point
                changed = False
                for a in beats:
                    add = set()
                    for b in beats[a]:
                        add |= beats.get(b, set())
                    if not add <= beats[a]:
                        beats[a] |= add
                        changed = True
            for a in beats:
                if a in beats[a]:
                    c = self.prog.clauses[a - 1]
                    self.err("PRIORITY-CYCLE", c, "the notwithstanding clauses of '%s' form a cycle" % name)
            self.overrides[name] = beats


# ------------------------------------------------------------------ the law's canonical bytes
def _q(s):
    out = []
    for ch in s:
        if ch in '"\\':
            out.append("\\" + ch)
        elif 32 <= ord(ch) < 127:
            out.append(ch)
        else:
            out.append("\\u{%x}" % ord(ch))
    return '"' + "".join(out) + '"'


def _t(t):
    return "list-%s" % t[1] if is_list(t) else t


def law_expr(e):
    if isinstance(e, Num):
        if e.type == "float":
            return "(lit float %016x)" % struct.unpack("<Q", struct.pack("<d", e.value))[0]
        return "(lit %s %d)" % (e.type, e.value)
    if isinstance(e, Str):
        return "(str %s)" % _q(e.value)
    if isinstance(e, BoolLit):
        return "(lit bool %d)" % int(e.value)
    if isinstance(e, Seal):
        return "(seal)"
    if isinstance(e, Var):
        return "(rule %s)" % _q(e.rule) if e.rule else "(var %d)" % e.var.id
    if isinstance(e, Bin):
        return "(%s %s %s %s)" % (e.op, _t(e.type), law_expr(e.a), law_expr(e.b))
    if isinstance(e, Un):
        return "(%s %s %s)" % (e.op, _t(e.type), law_expr(e.a))
    if isinstance(e, Conv):
        return "(%s %s %s)" % (e.mode, e.target, law_expr(e.a))
    if isinstance(e, Cat):
        return "(cat %s)" % " ".join(law_expr(p) for p in e.parts)
    if isinstance(e, Item):
        return "(item %d %s)" % (e.var.id, law_expr(e.index))
    if isinstance(e, Length):
        return "(length %d)" % e.var.id
    if isinstance(e, ListOf):
        return "(list-of %s %s)" % (law_expr(e.count), law_expr(e.value))
    if isinstance(e, ListLit):
        return "(list %s %s)" % (_t(e.type), " ".join(law_expr(x) for x in e.items))
    raise ValueError(e)


def law_body(b):
    if isinstance(b, tuple) and b[0] == BLOCK:
        return "(block %d)" % b[1].id
    return law_stmt(b)


def law_stmt(s):
    if isinstance(s, Let):
        return "(let %d %s %s)" % (s.var.id, _q(s.name), law_expr(s.expr))
    if isinstance(s, SetS):
        idx = law_expr(s.index) if s.index is not None else "-"
        return "(set %d %s %s)" % (s.var.id, idx, law_expr(s.expr))
    if isinstance(s, Change):
        idx = law_expr(s.index) if s.index is not None else "-"
        return "(change %s %d %s %s)" % (s.sign, s.var.id, idx, law_expr(s.expr))
    if isinstance(s, Say):
        return "(say %s)" % law_expr(s.expr)
    if isinstance(s, IfS):
        arms = " ".join("(arm %d %s %s)" % (ac.id, law_expr(cond), law_body(b)) for cond, b, ac in s.arms)
        els = "(else %d %s)" % (s.els[1].id, law_body(s.els[0])) if s.els is not None else "-"
        return "(if %s %s)" % (arms, els)
    if isinstance(s, While):
        return "(while %d %s)" % (s.fuel, law_expr(s.cond))
    if isinstance(s, For):
        return "(for %d %s %s)" % (s.var.id, law_expr(s.lo), law_expr(s.hi))
    if isinstance(s, ProcDef):
        return "(procedure %s)" % _q(s.name)
    if isinstance(s, Perform):
        return "(perform %d)" % s.proc.id
    if isinstance(s, Must):
        return "(must %d %s)" % (s.id, law_expr(s.cond))
    if isinstance(s, Claim):
        o = s.oracle
        if o[0] == "certificate":
            orc = "(certificate %d%s)" % (s.ref.id, " " + _q(o[2]) if len(o) > 2 else "")
        elif o[0] == "theorem":
            orc = "(theorem %s)" % _q(o[1])
        elif o[0] == "agreement":
            orc = "(agreement %s)" % " ".join(o[1:])
        else:
            orc = "(%s)" % o[0]
        return "(claim %d %s %s (given %s))" % (s.id, law_expr(s.cond), orc, " ".join(s.premises))
    if isinstance(s, Define):
        prov = law_expr(s.proviso) if s.proviso is not None else "-"
        return "(define %s %s %s (over %s))" % (_q(s.name), law_expr(s.expr), prov,
                                                " ".join(str(t.id) for t in s.over))
    if isinstance(s, Append):
        return "(append %d %s)" % (s.var.id, law_expr(s.expr))
    if isinstance(s, RemoveLast):
        return "(remove-last %d)" % s.var.id
    if isinstance(s, Decimals):
        return "(decimals %s)" % s.mode
    raise ValueError(s)


def law_bytes(prog, an):
    lines = ["orlog-law 0", "(decimals %s)" % an.decimals]
    for c in prog.clauses:
        parent = c.parent.id if c.parent is not None else 0
        if c.absorbed:
            lines.append("(clause %d %d absorbed)" % (c.id, parent))
        else:
            lines.append("(clause %d %d %s)" % (c.id, parent, law_stmt(c.stmt)))
    return ("\n".join(lines) + "\n").encode("ascii")


def law_seal(prog, an):
    return hashlib.sha256(law_bytes(prog, an)).hexdigest()

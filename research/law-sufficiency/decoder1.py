"""LAW-SUFFICIENCY-1: the decoder D1 (SHEET-1.md, E3 and E4), a copy of decoder.py with the backend-only derivations.

decoder.py stays exactly as LAW-SUFFICIENCY-0 ran it. D1 adds three fields the backends read and the interpreter does
not, each derived from the law bytes:
- an.vars: every variable in id order;
- an.rule_types: each rule's first define's type;
- a variable's top: a let in a top-level clause, outside any inline body; a for's counter never.
Its plants are set only by closure_tests.py, and put back after.

D reads the law bytes and nothing else, and builds the program and the analysis that the reference interpreter runs.
It is written from the law grammar: src/orlog/sema.py's _q, _t, law_expr, law_stmt and law_bytes, read as a
specification. It derives every field the analysis makes and the law bytes do not write:
- each expression's type;
- a Change's elem;
- a variable's type;
- the clauses' children and the top;
- a clause's cost_tracked;
- the rules, their override closure and the claim sites.

It imports nothing of the front end, the analysis or the interpreter. It builds syntax.py's node classes, because the
interpreter dispatches on them by isinstance: that shared data type is a dependency this test does not attack, and its
findings say so. Clauses, variables, claim sites, the program and the analysis are D's own small classes."""
import struct

from orlog.syntax import (Num, Str, BoolLit, Var, Bin, Un, Conv, Item, Length, ListOf, ListLit, Seal, Cat, Let, SetS,
                          Change, Say, IfS, While, For, ProcDef, Perform, Must, Claim, Define, Append, RemoveLast,
                          Decimals)

PLANT = None            # set only by closure_tests.py's plant rows, and put back after them
BLOCK = "block"         # the interpreter compares a body's first item with this string
BINARY = {"+", "-", "*", "/", "max", "min", "quot", "rem", "==", "!=", "<", ">", "<=", ">=", "and", "or"}
UNARY = {"neg", "abs", "sqrt", "not", "trunc", "even", "odd", "zero", "positive", "negative"}
CONVERSIONS = {"as", "rounded", "promote"}
SEEN = {}               # form -> count, over every decode: what the decoder was exercised on


class DecodeError(Exception):
    pass


class Quoted:
    """A string of the law bytes, kept apart from a bare word."""
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value


class DClause:
    __slots__ = ("id", "parent", "absorbed", "stmt", "children", "cost_tracked")

    def __init__(self, cid):
        self.id, self.parent, self.absorbed, self.stmt = cid, None, False, None
        self.children, self.cost_tracked = [], False


class DVar:
    __slots__ = ("id", "type", "top")

    def __init__(self, vid, typ, top):
        self.id, self.type, self.top = vid, typ, top


class DSite:
    __slots__ = ("id",)         # the clause the claim stands in, which a receipt prints

    def __init__(self, cid):
        self.id = cid


class DProgram:
    def __init__(self):
        self.clauses, self.top = [], []


class DAnalysis:
    def __init__(self):
        self.decimals, self.rules, self.overrides, self.claims = None, {}, {}, []
        self.vars, self.rule_types = [], {}


# ------------------------------------------------------------------ reading the bytes
def tokens(line):
    out, i, n = [], 0, len(line)
    while i < n:
        ch = line[i]
        if ch == " ":
            i += 1
        elif ch in "()":
            out.append(ch)
            i += 1
        elif ch == '"':
            i += 1
            buf = []
            while True:
                if i >= n:
                    raise DecodeError("an unterminated string")
                ch = line[i]
                if ch == '"':
                    i += 1
                    break
                if ch == "\\":
                    nxt = line[i + 1:i + 2]
                    if nxt in ('"', "\\"):
                        buf.append(nxt)
                        i += 2
                    elif line.startswith("u{", i + 1):
                        j = line.index("}", i + 3)
                        buf.append(chr(int(line[i + 3:j], 16)))
                        i = j + 1
                    else:
                        raise DecodeError("an escape that is not \\\", \\\\ or \\u{...}")
                else:
                    buf.append(ch)
                    i += 1
            out.append(Quoted("".join(buf)))
        else:
            j = i
            while j < n and line[j] not in ' ()"':
                j += 1
            out.append(line[i:j])
            i = j
    return out


def tree(toks):
    stack = [[]]
    for t in toks:
        if t == "(":
            stack.append([])
        elif t == ")":
            if len(stack) < 2:
                raise DecodeError("a ')' with no '('")
            x = stack.pop()
            stack[-1].append(x)
        else:
            stack[-1].append(t)
    if len(stack) != 1 or len(stack[0]) != 1 or not isinstance(stack[0][0], list):
        raise DecodeError("a line that is not one form")
    return stack[0][0]


def typ(word):
    return ("list", word[len("list-"):]) if word.startswith("list-") else word


def word(x):
    if not isinstance(x, str):
        raise DecodeError("a word expected, found %r" % (x,))
    return x


def text(x):
    if not isinstance(x, Quoted):
        raise DecodeError("a string expected, found %r" % (x,))
    return x.value


def seen(kind):
    SEEN[kind] = SEEN.get(kind, 0) + 1


# ------------------------------------------------------------------ building, with every derived field
class Builder:
    def __init__(self, by_id):
        self.by_id = by_id
        self.vars = {}          # variable id -> DVar
        self.rule_types = {}    # rule name -> its value's type
        self.sites = {}         # claim id -> clause id
        self.inline = 0         # how deep in inline bodies the statement being built stands

    def clause(self, k):
        if k not in self.by_id:
            raise DecodeError("no clause %d" % k)
        return self.by_id[k]

    def var(self, k):
        if k not in self.vars:
            raise DecodeError("variable %d used before the law declares it" % k)
        return self.vars[k]

    # expressions: each node's type is derived and set, as the analysis sets it
    def expr(self, f):
        if not isinstance(f, list) or not f:
            raise DecodeError("an expression expected, found %r" % (f,))
        head = word(f[0])
        if head == "lit":
            seen("expr lit " + f[1])
            if f[1] == "float":
                e = Num(None)
                e.value = struct.unpack("<d", struct.pack("<Q", int(word(f[2]), 16)))[0]
                e.type = "float"
            elif f[1] == "bool":
                e = BoolLit(bool(int(word(f[2]))))
                e.type = "bool"
            elif f[1] in ("int", "fix"):
                e = Num(None)
                e.value = int(word(f[2]))
                e.type = f[1]
            else:
                raise DecodeError("a literal of type %r" % f[1])
            return e
        seen("expr " + (head if head not in BINARY | UNARY else ("binary" if len(f) == 4 else "unary")))
        if head == "str":
            e = Str(text(f[1]))
            e.type = "text"
        elif head == "seal":
            e = Seal()
            e.type = "text"
        elif head == "rule":
            name = text(f[1])
            if name not in self.rule_types:
                raise DecodeError("rule %r used before the law defines it" % name)
            e = Var(None)
            e.var, e.rule, e.type = None, name, self.rule_types[name]
        elif head == "var":
            e = Var(None)
            e.var = self.var(int(word(f[1])))
            e.rule, e.type = None, e.var.type
        elif head in CONVERSIONS:
            mode = "as" if PLANT == "rounded-as-as" and head == "rounded" else head
            e = Conv(mode, word(f[1]), self.expr(f[2]))
            e.type = e.target
        elif head in BINARY and len(f) == 4:
            e = Bin(head, self.expr(f[2]), self.expr(f[3]))
            e.type = typ(word(f[1]))
        elif head in UNARY and len(f) == 3:
            e = Un(head, self.expr(f[2]))
            e.type = typ(word(f[1]))
        elif head == "cat":
            e = Cat([self.expr(p) for p in f[1:]])
            e.type = "text"
        elif head == "item":
            e = Item(None, None)
            e.var = self.var(int(word(f[1])))
            e.index = self.expr(f[2])
            e.type = e.var.type[1]
        elif head == "length":
            e = Length(None)
            e.var = self.var(int(word(f[1])))
            e.type = "int"
        elif head == "list-of":
            e = ListOf(self.expr(f[1]), self.expr(f[2]))
            e.type = ("list", e.value.type)
        elif head == "list":
            e = ListLit([self.expr(x) for x in f[2:]])
            e.type = typ(word(f[1]))
        else:
            raise DecodeError("an expression headed %r" % head)
        return e

    def opt(self, f):
        return None if f == "-" else self.expr(f)

    def body(self, f, c):
        if isinstance(f, list) and f and f[0] == "block":
            return (BLOCK, self.clause(int(word(f[1]))))
        self.inline += 1
        try:
            return self.stmt(f, c)
        finally:
            self.inline -= 1

    def top(self, c):
        """A let's variable is top when it stands in a top-level clause and outside any inline body."""
        if PLANT == "top-always-false":
            return False
        if PLANT == "top-includes-inline":
            return c.parent is None
        return c.parent is None and self.inline == 0

    # statements; c is the clause the statement stands in (an arm's or an else's for an inline body)
    def stmt(self, f, c):
        head = word(f[0])
        seen("stmt " + head)
        if head == "let":
            e = self.expr(f[3])
            s = Let(text(f[2]), e)
            s.var = DVar(int(word(f[1])), e.type, self.top(c))
            self.vars[s.var.id] = s.var
        elif head == "set":
            s = SetS(None, self.opt(f[2]), self.expr(f[3]))
            s.var = self.var(int(word(f[1])))
        elif head == "change":
            s = Change(word(f[1]), None, self.opt(f[3]), self.expr(f[4]))
            s.var = self.var(int(word(f[2])))
            if PLANT == "elem-ignores-index":
                s.elem = s.var.type                     # the plant: the list's type, not its element's
            else:
                s.elem = s.var.type[1] if s.index is not None else s.var.type
        elif head == "say":
            s = Say(self.expr(f[1]))
        elif head == "if":
            arms = []
            for a in f[1:-1]:
                if word(a[0]) != "arm":
                    raise DecodeError("an if's part that is not an arm")
                ac = self.clause(int(word(a[1])))
                cond = self.expr(a[2])
                arms.append((cond, self.body(a[3], ac), ac))
            last = f[-1]
            if last == "-":
                els = None
            else:
                if word(last[0]) != "else":
                    raise DecodeError("an if's last part that is not an else or '-'")
                ec = self.clause(int(word(last[1])))
                els = (self.body(last[2], ec), ec)
            s = IfS(arms, els)
        elif head == "while":
            s = While(self.expr(f[2]), int(word(f[1])))
        elif head == "for":
            s = For(None, self.expr(f[2]), self.expr(f[3]))
            s.var = DVar(int(word(f[1])), "int", False)
            self.vars[s.var.id] = s.var
        elif head == "procedure":
            s = ProcDef(text(f[1]))
        elif head == "perform":
            s = Perform(None)
            s.proc = self.clause(int(word(f[1])))
        elif head == "must":
            s = Must(self.expr(f[2]))
            s.id = int(word(f[1]))
        elif head == "claim":
            cond = self.expr(f[2])
            o = f[3]
            kind = word(o[0])
            ref = None
            if kind == "certificate":
                ref = self.clause(int(word(o[1])))
                ref.cost_tracked = True                 # the clause a certificate names is the one whose cost it reads
                oracle = ("certificate", "") + ((text(o[2]),) if len(o) > 2 else ())
            elif kind == "theorem":
                oracle = ("theorem", text(o[1]))
            elif kind == "agreement":
                oracle = ("agreement",) + tuple(word(x) for x in o[1:])
            else:
                oracle = (kind,)
            given = f[4]
            if word(given[0]) != "given":
                raise DecodeError("a claim with no given part")
            s = Claim(cond, oracle, [word(x) for x in given[1:]])
            s.id, s.ref = int(word(f[1])), ref
            if s.id in self.sites:
                raise DecodeError("claim id %d twice" % s.id)
            self.sites[s.id] = c.id
        elif head == "define":
            name = text(f[1])
            e = self.expr(f[2])
            proviso = self.opt(f[3])
            over = f[4]
            if word(over[0]) != "over":
                raise DecodeError("a define with no over part")
            s = Define(name, e, proviso, None)
            s.over = [self.clause(int(word(x))) for x in over[1:]]
            self.rule_types.setdefault(name, e.type)
        elif head == "append":
            s = Append(self.expr(f[2]), None)
            s.var = self.var(int(word(f[1])))
        elif head == "remove-last":
            s = RemoveLast(None)
            s.var = self.var(int(word(f[1])))
        elif head == "decimals":
            s = Decimals(word(f[1]))
        else:
            raise DecodeError("a statement headed %r" % head)
        return s


def closure(direct):
    """Each clause's set of clauses it beats, closed transitively (a least fixed point)."""
    beats = {a: set(b) for a, b in direct.items()}
    changed = True
    while changed:
        changed = False
        for a in beats:
            add = set()
            for b in beats[a]:
                add |= beats.get(b, set())
            if not add <= beats[a]:
                beats[a] |= add
                changed = True
    return beats


def decode(law):
    """The law bytes -> (program, analysis), for the reference interpreter to run. Nothing but the bytes is read."""
    if not isinstance(law, bytes):
        raise DecodeError("the law is bytes")
    t = law.decode("ascii")
    if not t.endswith("\n"):
        raise DecodeError("the law bytes end with LF")
    lines = t[:-1].split("\n")
    if lines[0] != "orlog-law 0":
        raise DecodeError("not version 0's law bytes")
    head = tree(tokens(lines[1]))
    if head[0] != "decimals" or len(head) != 2:
        raise DecodeError("the second line is not the decimals line")
    an = DAnalysis()
    an.decimals = head[1]
    forms = [tree(tokens(ln)) for ln in lines[2:]]
    prog, by_id = DProgram(), {}
    for k, f in enumerate(forms, 1):
        if len(f) != 4 or f[0] != "clause" or int(word(f[1])) != k:
            raise DecodeError("clause line %d is not (clause %d parent statement)" % (k, k))
        c = DClause(k)
        by_id[k] = c
        prog.clauses.append(c)
    for f, c in zip(forms, prog.clauses):
        p = int(word(f[2]))
        if p:
            if not 0 < p < c.id:
                raise DecodeError("clause %d's parent %d does not come before it" % (c.id, p))
            c.parent = by_id[p]
            by_id[p].children.append(c)
        else:
            prog.top.append(c)
        if f[3] == "absorbed":
            c.absorbed = True
    b = Builder(by_id)
    for f, c in zip(forms, prog.clauses):
        if not c.absorbed:
            c.stmt = b.stmt(f[3], c)
    for c in prog.clauses:
        if isinstance(c.stmt, Define):
            an.rules.setdefault(c.stmt.name, []).append(c)
    for name, cls in an.rules.items():
        an.overrides[name] = closure({c.id: set(t.id for t in c.stmt.over) for c in cls})
    if sorted(b.sites) != list(range(len(b.sites))):
        raise DecodeError("the claim ids are not 0 to n-1")
    an.claims = [DSite(b.sites[k]) for k in range(len(b.sites))]
    if sorted(b.vars) != list(range(len(b.vars))):
        raise DecodeError("the variable ids are not 0 to n-1")
    an.vars = [b.vars[k] for k in range(len(b.vars))]
    an.rule_types = dict(b.rule_types)
    return prog, an

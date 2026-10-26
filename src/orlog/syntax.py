"""Canonical text -> clause tree -> statements (untyped AST).

A program is a sequence of clause lines. Blocks are made by legal outline numbering,
never by indentation: the children of §3 are §3.1, §3.2, ... The numbering must run
without a gap or a repeat, so it is itself a structural check: a lost or duplicated
clause is refused, as a ledger refuses a sequence break.
"""
import re

from .seal import line_check, PROQUINT_RE


class OrlogError(Exception):
    """A compile-time refusal: code, line, message."""

    def __init__(self, code, line, msg):
        Exception.__init__(self, "%s at line %s: %s" % (code, line, msg))
        self.code, self.line, self.msg = code, line, msg


# ------------------------------------------------------------------ AST
class Node:
    fields = ()

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__,
                           ", ".join("%s=%r" % (k, getattr(self, k, None)) for k in self.fields))


def node(name, fields):
    def __init__(self, *args):
        for k, v in zip(fields, args):
            setattr(self, k, v)
        for k in fields[len(args):]:
            setattr(self, k, None)
        self.type = None
        self.line = None
    return type(name, (Node,), {"fields": tuple(fields), "__init__": __init__})


# expressions
Num = node("Num", ["text"])
Str = node("Str", ["value"])
BoolLit = node("BoolLit", ["value"])
Var = node("Var", ["name"])
Bin = node("Bin", ["op", "a", "b"])            # + - * / quot rem max min == != < > <= >= and or cat
Un = node("Un", ["op", "a"])                   # neg abs sqrt not trunc even odd zero positive negative
Conv = node("Conv", ["mode", "target", "a"])   # mode as|rounded, target int|fix|float
Item = node("Item", ["list", "index"])
Length = node("Length", ["list"])
ListOf = node("ListOf", ["count", "value"])
ListLit = node("ListLit", ["items"])
Seal = node("Seal", [])
Cat = node("Cat", ["parts"])                   # a followed by b followed by c
# statements
Let = node("Let", ["name", "expr"])
SetS = node("SetS", ["name", "index", "expr"])          # index None for a plain variable
Change = node("Change", ["sign", "name", "index", "expr"])
Say = node("Say", ["expr"])
IfS = node("IfS", ["arms", "els"])            # arms: [(cond, body)], body: Stmt or ("block", clause)
RawIf = node("RawIf", ["kind", "cond", "then", "els"])  # kind: if|unless|otherwise|otherwise-if
While = node("While", ["cond", "fuel"])
For = node("For", ["name", "lo", "hi"])
ProcDef = node("ProcDef", ["name"])
Perform = node("Perform", ["name"])
Must = node("Must", ["cond"])
Claim = node("Claim", ["cond", "oracle", "premises"])
Define = node("Define", ["name", "expr", "proviso", "overrides"])
Append = node("Append", ["expr", "list"])
RemoveLast = node("RemoveLast", ["list"])
Decimals = node("Decimals", ["mode"])

BLOCK = "block"
NESTING_MAX = 24
EXPR_NEST_MAX = 24      # parentheses, unary minus, not, phrases: the parser's recursion and the Python backend's indent
AST_DEPTH_MAX = 64      # the expression tree's depth: later stages walk it recursively (red team E24, E25)


def ast_depth(root):
    """Depth of the tree of Nodes under root, computed without recursion."""
    best = 0
    stack = [(root, 1)]
    while stack:
        n, d = stack.pop()
        if isinstance(n, Node):
            best = max(best, d)
            for k in n.fields:
                stack.append((getattr(n, k, None), d + 1))
        elif isinstance(n, (list, tuple)):
            for x in n:
                stack.append((x, d))
    return best

RESERVED = set("""
let be set to say if then otherwise unless while at most least times do the following for each from perform it
must hold that we claim by given define as provided notwithstanding append remove last item of length list
copies is not and or plus minus divided quotient remainder modulo equals equal less greater than even odd zero
positive negative true false sum product larger smaller absolute value square root integer part float fixed
rounded followed this law seal computation theorem owner certificate agreement decimals are floats negation
increase decrease
""".split())

TOKEN_RE = re.compile(r"""
    (?P<ws>[ ]+)
  | (?P<ref>§[0-9]+(?:\.[0-9]+)*)
  | (?P<num>[0-9]+(?:\.[0-9]+)?)
  | (?P<str>"(?:[^"]|"")*")
  | (?P<word>[A-Za-z][A-Za-z0-9_]*)
  | (?P<op><=|>=|!=|[-+*/(),;:<>='])
""", re.X)

LABEL_RE = re.compile(r"^(?:§([0-9]+(?:\.[0-9]+)*)|([0-9]+(?:\.[0-9]+)*)\.)[ ]([^ ].*)$")
CHECK_RE = re.compile(r"^(.*\.)[ ]\[([a-z]{3})\]$")


class Tok:
    __slots__ = ("kind", "text", "low")

    def __init__(self, kind, text):
        self.kind, self.text, self.low = kind, text, text.lower()

    def __repr__(self):
        return "%s:%s" % (self.kind, self.text)


def lex(s, line):
    toks, pos = [], 0
    while pos < len(s):
        m = TOKEN_RE.match(s, pos)
        if not m:
            raise OrlogError("LEX", line, "cannot read %r" % s[pos:pos + 12])
        kind = m.lastgroup
        if kind != "ws":
            toks.append(Tok(kind, m.group(kind)))
        pos = m.end()
    return toks


# ------------------------------------------------------------------ clauses
class Clause:
    __slots__ = ("id", "label", "parts", "line", "text", "stmt", "children", "parent", "check", "absorbed",
                 "cost_tracked")

    def __init__(self, cid, label, line, text):
        self.id, self.label, self.line, self.text = cid, label, line, text
        self.parts = tuple(int(p) for p in label.split("."))
        self.stmt, self.children, self.parent, self.check = None, [], None, None
        self.absorbed, self.cost_tracked = False, False


class Program:
    def __init__(self):
        self.title = None
        self.clauses = []          # document order; clause.id = index + 1
        self.top = []              # top-level clauses
        self.seal = None           # the seal line's proquints, if any
        self.by_label = {}
        self.line_checks = 0
        self.proc_names = set()    # every top-level To clause's name, collected by the lexer before parsing


def _numbering_next(prev, cur):
    """The legal successors of label prev: next sibling, first child, or an ancestor's next sibling."""
    if prev is None:
        return cur == (1,)
    if cur == prev + (1,):
        return True
    for k in range(len(prev), 0, -1):
        if cur == prev[:k - 1] + (prev[k - 1] + 1,):
            return True
    return False


def parse_program(text):
    prog = Program()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    prev = None
    stack = []
    content_seen = False
    for ln, raw in enumerate(lines, 1):
        line = raw
        if line.strip() == "":
            continue
        if line.startswith("Note:"):
            continue
        if line.startswith("Title:"):
            if content_seen or prog.title is not None:
                raise OrlogError("TITLE-PLACE", ln, "a Title is the first line, and only one")
            prog.title = line[len("Title:"):].strip()
            if prog.title.endswith("."):
                prog.title = prog.title[:-1]
            content_seen = True
            continue
        if line.startswith("Sealed: "):        # the exact prefix, its space included: 'Sealed:x' is LINE-FORM (§13)
            m = re.match(r"^Sealed: (%s)\.$" % PROQUINT_RE, line)
            if not m:
                raise OrlogError("SEAL-FORM", ln, "write: Sealed: xxxxx-xxxxx-xxxxx-xxxxx.")
            if prog.seal is not None:          # within a line SEAL-FORM, then SEAL-PLACE (G3)
                raise OrlogError("SEAL-PLACE", ln, "a program has one seal line (red team E13)")
            prog.seal = (m.group(1), ln)
            content_seen = True                # the Sealed line is content: no Title may follow it (§13)
            continue
        content_seen = True
        m = LABEL_RE.match(line)
        cm = CHECK_RE.match(line) if m else None
        lm = LABEL_RE.match(cm.group(1)) if cm else m
        if lm is None or not lm.group(3).endswith("."):     # a clause's statement ends with a period (§1)
            raise OrlogError("LINE-FORM", ln,
                             "a line is a clause (§1 ... ending with a period), a Note:, a Title: or a Sealed: line")
        if prog.seal is not None:              # within a line LINE-FORM, then SEAL-PLACE (G3, the twin's n04)
            raise OrlogError("SEAL-PLACE", ln, "nothing but a Note may follow the seal line")
        label = m.group(1) or m.group(2)
        body = m.group(3)
        check = None
        if cm:
            expect = line_check(cm.group(1))
            if expect != cm.group(2):
                raise OrlogError("LINE-CHECK", ln,
                                 "the check syllable is [%s] but the line reads as [%s]: the line changed after "
                                 "it was stamped" % (cm.group(2), expect))
            check = cm.group(2)
            body = LABEL_RE.match(cm.group(1)).group(3)
            prog.line_checks += 1
        c = Clause(len(prog.clauses) + 1, label, ln, body)
        c.check = check
        if len(c.parts) > NESTING_MAX:
            raise OrlogError("NESTING-DEPTH", ln, "clauses nest at most %d deep: every stage recurses by depth and the "
                             "Python backend's host allows 100 indentation levels (red team E10)" % NESTING_MAX)
        if not _numbering_next(prev, c.parts):
            raise OrlogError("NUMBERING", ln, "§%s cannot follow §%s: the outline numbering must run without a gap "
                             "or a repeat" % (label, ".".join(map(str, prev)) if prev else "the start"))
        prev = c.parts
        while stack and len(stack[-1].parts) >= len(c.parts):
            stack.pop()
        if stack:
            c.parent = stack[-1]
            stack[-1].children.append(c)
        else:
            prog.top.append(c)
        stack.append(c)
        prog.clauses.append(c)
        prog.by_label[".".join(str(p) for p in c.parts)] = c     # keyed by integer parts: §02 is §2 (red team E20)
    procs = set()
    for c in prog.top:
        # top level only, and read by the lexer, as the statement parser reads it (red team E16: a regex had missed
        # ",  do", ",do" and "do  the", which the tokens accept)
        if not c.text.endswith("."):
            continue
        try:
            toks = lex(c.text[:-1], c.line)
        except OrlogError:
            continue
        tail = [t.text if t.kind == "op" else t.low for t in toks[-4:]]
        if len(toks) > 5 and toks[0].kind == "word" and toks[0].low == "to" and tail == [",", "do", "the", "following"]:
            words = toks[1:-4]
            if all(t.kind == "word" for t in words):
                procs.add(" ".join(t.low for t in words))
    prog.proc_names = procs
    for c in prog.clauses:
        c.stmt = StmtParser(c, prog, procs).statement()
    _attach_otherwise(prog, prog.top)
    return prog


def _attach_otherwise(prog, siblings):
    last_if = None
    for c in siblings:
        st = c.stmt
        if isinstance(st, RawIf) and st.kind in ("otherwise", "otherwise-if"):
            if last_if is None or last_if.stmt.els is not None:
                raise OrlogError("ORPHAN-OTHERWISE", c.line,
                                 "an Otherwise clause must follow an If or Unless that has no otherwise yet")
            arm_body = _body(c, st.then)
            if st.kind == "otherwise-if":
                last_if.stmt.arms.append((st.cond, arm_body, c))
            else:
                last_if.stmt.els = (arm_body, c)
                last_if = None
            c.absorbed = True
        elif isinstance(st, RawIf):
            if st.kind == "unless":
                cond = Un("not", st.cond)
                cond.line = c.line
            else:
                cond = st.cond
            c.stmt = IfS([(cond, _body(c, st.then), c)], None)
            c.stmt.line = c.line
            if st.els is not None:
                c.stmt.els = (st.els, c)
                last_if = None
            else:
                last_if = c
        else:
            last_if = None
        _check_children(c)
        _attach_otherwise(prog, c.children)


def _body(c, then):
    if then == BLOCK:
        return (BLOCK, c)
    return then


def _check_children(c):
    st = c.stmt
    wants = isinstance(st, (While, For, ProcDef)) or (
        isinstance(st, IfS) and any(isinstance(b, tuple) and b[1] is c for _, b, _ in st.arms)) or (
        isinstance(st, IfS) and st.els is not None and isinstance(st.els[0], tuple) and st.els[0][1] is c) or (
        isinstance(st, RawIf) and st.then == BLOCK)
    if wants and not c.children:
        raise OrlogError("EMPTY-BLOCK", c.line, "§%s says 'do the following' but has no sub-clauses" % c.label)
    if not wants and c.children:
        # absorbed Otherwise clauses obey this too: their children were neither checked nor run (red team E3, E3b)
        raise OrlogError("UNEXPECTED-CHILDREN", c.line,
                         "§%s has sub-clauses but does not say 'do the following'" % c.label)


# ------------------------------------------------------------------ statements and expressions
PHRASE_HEADS = {"sum", "product", "quotient", "remainder", "larger", "smaller", "absolute", "square",
                "integer", "negation", "length", "list"}


class StmtParser:
    def __init__(self, clause, prog, procs):
        self.c, self.prog, self.procs = clause, prog, procs
        self.line = clause.line
        text = clause.text
        if not text.endswith("."):             # unreachable from parse_program, whose line pass refuses it first
            raise OrlogError("LINE-FORM", self.line, "a clause's statement ends with a period")
        self.t = lex(text[:-1], self.line)
        self.i = 0
        self.depth = 0
        self.bad_name = None                   # PROCEDURE-NAME and UNKNOWN-PROCEDURE wait for the clause to parse:
        self.unknown = []                      # within a clause, SYNTAX comes first (G3, §13)

    def nest(self):
        self.depth += 1
        if self.depth > EXPR_NEST_MAX:
            raise OrlogError("EXPRESSION-DEPTH", self.line, "expressions nest at most %d deep (parentheses, minus, not, "
                             "phrases): red team E24, E25" % EXPR_NEST_MAX)

    def unnest(self):
        self.depth -= 1

    # -- token helpers
    def peek(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else None

    def at(self, *words):
        for k, w in enumerate(words):
            tok = self.peek(k)
            if tok is None:
                return False
            if w.startswith("@"):
                if tok.kind != "op" or tok.text != w[1:]:
                    return False
            elif tok.kind != "word" or tok.low != w:
                return False
        return True

    def eat(self, *words):
        if not self.at(*words):
            got = " ".join(t.text for t in self.t[self.i:self.i + len(words) + 1]) or "the end"
            raise OrlogError("SYNTAX", self.line, "expected '%s' but read '%s'"
                             % (" ".join(w.lstrip("@") for w in words), got))
        self.i += len(words)

    def op(self, o):
        return self.at("@" + o)

    def done(self):
        return self.i >= len(self.t)

    def mk(self, n):
        n.line = self.line
        return n

    def ident(self):
        tok = self.peek()
        if tok is not None and tok.kind == "word" and tok.low == "the" and self._the_is_filler():
            self.i += 1
            tok = self.peek()
        if tok is None or tok.kind != "word" or tok.low in RESERVED:
            raise OrlogError("SYNTAX", self.line, "expected a name, read '%s'" % (tok.text if tok else "the end"))
        self.i += 1
        return tok.text

    def _the_is_filler(self):
        nxt = self.peek(1)
        return nxt is not None and nxt.kind == "word" and nxt.low not in RESERVED

    def ref(self):
        tok = self.peek()
        if tok is None or tok.kind != "ref":
            raise OrlogError("SYNTAX", self.line, "expected a clause reference like §3")
        self.i += 1
        return ".".join(str(int(p)) for p in tok.text[1:].split("."))

    def expect_end(self):
        if not self.done():
            raise OrlogError("SYNTAX", self.line, "unexpected '%s'"
                             % " ".join(t.text for t in self.t[self.i:self.i + 4]))

    # -- statements
    def statement(self):
        st = self.stmt_head(top=True)
        self.expect_end()
        if ast_depth(st) > AST_DEPTH_MAX:
            raise OrlogError("EXPRESSION-DEPTH", self.line, "a statement's expression tree is at most %d deep" %
                             AST_DEPTH_MAX)
        if self.bad_name is not None:
            raise OrlogError("PROCEDURE-NAME", self.line, "a procedure's name may not begin with a reserved word "
                             "('%s'; so 'do the following' can never be a name: the twin's notes, 21)" % self.bad_name)
        if self.unknown:
            raise OrlogError("UNKNOWN-PROCEDURE", self.line, "no procedure is defined as 'To %s'" % self.unknown[0])
        return st

    def stmt_head(self, top=False):
        tok = self.peek()
        if tok is None:
            raise OrlogError("SYNTAX", self.line, "an empty statement")
        w = tok.low
        if w == "let":
            self.i += 1
            name = self.ident()
            self.eat("be")
            return self.mk(Let(name, self.expr()))
        if w == "set":
            self.i += 1
            name, index = self.target()
            self.eat("to")
            return self.mk(SetS(name, index, self.expr()))
        if w in ("increase", "decrease"):
            self.i += 1
            name, index = self.target()
            self.eat("by")
            return self.mk(Change("+" if w == "increase" else "-", name, index, self.expr()))
        if w == "say":
            self.i += 1
            return self.mk(Say(self.expr()))
        if w == "append":
            self.i += 1
            e = self.expr()
            self.eat("to")
            return self.mk(Append(e, self.ident()))
        if w == "remove":
            self.eat("remove", "the", "last", "item", "of")
            return self.mk(RemoveLast(self.ident()))
        if w == "perform":
            self.i += 1
            name = self.phrase_rest()
            return self.mk(Perform(name))
        if w == "it":
            self.eat("it", "must", "hold", "that")
            return self.mk(Must(self.expr()))
        if w == "we":
            return self.claim()
        if w == "decimals" and top:
            self.eat("decimals", "are")
            if self.at("fixed"):
                self.i += 1
                return self.mk(Decimals("fixed"))
            self.eat("floats")
            return self.mk(Decimals("floats"))
        if w in ("define", "notwithstanding") and top:
            return self.define()
        if not top:
            if tok.kind == "word" and w not in RESERVED:      # the name alone calls the procedure (§3, §13)
                return self.mk(Perform(self.phrase_rest()))
            raise OrlogError("SYNTAX", self.line, "'%s' cannot begin an inline statement" % tok.text)
        if w == "if":
            self.i += 1
            cond = self.expr()
            self.eat("@,")
            if self.at("then"):
                self.i += 1
            if self.at("do", "the", "following"):
                self.i += 3
                return self.mk(RawIf("if", cond, BLOCK, None))
            then = self.stmt_head()
            els = None
            if self.op(";"):
                self.i += 1
                self.eat("otherwise")
                if self.op(","):
                    self.i += 1
                els = self.stmt_head()
            return self.mk(RawIf("if", cond, then, els))
        if w == "unless":
            self.i += 1
            cond = self.expr()
            self.eat("@,")
            if self.at("do", "the", "following"):
                self.i += 3
                return self.mk(RawIf("unless", cond, BLOCK, None))
            return self.mk(RawIf("unless", cond, self.stmt_head(), None))
        if w == "otherwise":
            self.i += 1
            self.eat("@,")
            if self.at("if"):
                self.i += 1
                cond = self.expr()
                self.eat("@,")
                if self.at("then"):
                    self.i += 1
                if self.at("do", "the", "following"):
                    self.i += 3
                    return self.mk(RawIf("otherwise-if", cond, BLOCK, None))
                return self.mk(RawIf("otherwise-if", cond, self.stmt_head(), None))
            if self.at("do", "the", "following"):
                self.i += 3
                return self.mk(RawIf("otherwise", None, BLOCK, None))
            return self.mk(RawIf("otherwise", None, self.stmt_head(), None))
        if w == "while":
            self.i += 1
            cond = self.expr()
            self.eat("@,")
            self.eat("at", "most")
            fuel = self.peek()
            if fuel is None or fuel.kind != "num" or "." in fuel.text:
                raise OrlogError("SYNTAX", self.line, "a While states its bound: 'at most N times'")
            self.i += 1
            self.eat("times")
            self.eat("@,")
            self.eat("do", "the", "following")
            return self.mk(While(cond, int(fuel.text)))
        if w == "for":
            self.eat("for", "each")
            name = self.ident()
            self.eat("from")
            lo = self.sum_expr()
            self.eat("to")
            hi = self.sum_expr()
            self.eat("@,")
            self.eat("do", "the", "following")
            return self.mk(For(name, lo, hi))
        if w == "to":          # at any depth: sema refuses a nested one PROCEDURE-PLACE (red team E16)
            self.i += 1
            words = []
            while not self.op(","):
                tok = self.peek()
                if tok is None or tok.kind != "word":
                    raise OrlogError("SYNTAX", self.line, "a procedure's name is words, then ', do the following'")
                words.append(tok.low)
                self.i += 1
            if not words:
                raise OrlogError("SYNTAX", self.line, "a procedure's name is words, then ', do the following'")
            if words[0] in RESERVED:
                self.bad_name = " ".join(words)
            self.eat("@,")
            self.eat("do", "the", "following")
            return self.mk(ProcDef(" ".join(words)))
        if tok.kind == "word" and w not in RESERVED:          # the name alone calls the procedure (§3, §13)
            return self.mk(Perform(self.phrase_rest()))
        raise OrlogError("SYNTAX", self.line, "no statement begins with '%s'" % tok.text)

    def phrase_rest(self):
        """A call's name: its words, to the end of the statement or a ';'. A name that begins with a reserved word
        names no procedure and is SYNTAX; a name no To clause defines is recorded and refused UNKNOWN-PROCEDURE once
        the whole clause has parsed (§13)."""
        first = self.peek()
        if first is None or first.kind != "word" or first.low in RESERVED:
            raise OrlogError("SYNTAX", self.line, "a call names a procedure: words that do not begin with a reserved "
                             "word")
        words = []
        while self.peek() is not None and self.peek().kind == "word":
            words.append(self.peek().low)
            self.i += 1
            if " ".join(words) in self.procs and (self.peek() is None or self.op(";")):
                break
        name = " ".join(words)
        if name not in self.procs:
            self.unknown.append(name)
        return name

    def target(self):
        if self.at("item"):
            self.i += 1
            index = self.unary()
            self.eat("of")
            return self.ident(), index
        return self.ident(), None

    def claim(self):
        self.eat("we", "claim", "that")
        cond = self.expr()
        oracle = ("computation",)
        named = False
        premises = []
        while self.op(","):
            self.i += 1
            if self.at("by"):
                if named:
                    raise OrlogError("SYNTAX", self.line, "a claim names one oracle (red team E15)")
                self.i += 1
                oracle = self.oracle()
                named = True
            elif self.at("given"):
                self.i += 1
                premises.append(self.ref())
                while self.op(",") and self.peek(1) is not None and self.peek(1).kind == "ref":
                    self.i += 1
                    premises.append(self.ref())
                if self.at("and"):
                    self.i += 1
                    premises.append(self.ref())
            else:
                raise OrlogError("SYNTAX", self.line, "a claim continues with ', by ...' or ', given §...'")
        return self.mk(Claim(cond, oracle, premises))

    def oracle(self):
        if self.at("computation"):
            self.i += 1
            return ("computation",)
        if self.at("the", "theorem"):
            self.i += 2
            tok = self.peek()
            if tok is None or tok.kind != "str":
                raise OrlogError("SYNTAX", self.line, "the theorem is named in quotes")
            self.i += 1
            return ("theorem", tok.text[1:-1].replace('""', '"'))
        if self.at("the", "owner"):
            self.i += 2
            return ("owner",)
        if self.at("the", "certificate", "of"):
            self.i += 3
            r = self.ref()
            if self.at("under", "the", "theorem"):
                self.i += 3
                tok = self.peek()
                if tok is None or tok.kind != "str":
                    raise OrlogError("SYNTAX", self.line, "the determinacy theorem is named in quotes")
                self.i += 1
                return ("certificate", r, tok.text[1:-1].replace('""', '"'))
            return ("certificate", r)
        if self.at("agreement", "of"):
            self.i += 2
            a = self.ref()
            self.eat("and")
            return ("agreement", a, self.ref())
        raise OrlogError("SYNTAX", self.line, "an oracle is: computation, the theorem \"...\", the owner, "
                         "the certificate of §k, or agreement of §a and §b")

    def define(self):
        overrides = []
        if self.at("notwithstanding"):
            self.i += 1
            overrides.append(self.ref())
            while self.op(",") and self.peek(1) is not None and self.peek(1).kind == "ref":
                self.i += 1
                overrides.append(self.ref())
            if self.at("and"):
                self.i += 1
                overrides.append(self.ref())
            self.eat("@,")
        self.eat("define")
        name = self.ident()
        self.eat("as")
        e = self.expr()
        proviso = None
        if self.op(","):
            self.i += 1
            if self.at("provided", "that"):
                self.i += 2
                proviso = self.expr()
            elif self.at("unless"):
                self.i += 1
                proviso = self.mk(Un("not", self.expr()))
            else:
                raise OrlogError("SYNTAX", self.line, "a definition continues with ', provided that' or ', unless'")
        return self.mk(Define(name, e, proviso, overrides))

    # -- expressions, lowest precedence first
    def expr(self):
        return self.or_expr()

    def or_expr(self):
        a = self.and_expr()
        while self.at("or"):
            self.i += 1
            a = self.mk(Bin("or", a, self.and_expr()))
        return a

    def and_expr(self):
        a = self.not_expr()
        while self.at("and"):
            self.i += 1
            a = self.mk(Bin("and", a, self.not_expr()))
        return a

    def not_expr(self):
        if self.at("not") or self.at("it", "is", "not", "the", "case", "that"):
            self.i += 1 if self.at("not") else 6
            self.nest()
            try:
                return self.mk(Un("not", self.not_expr()))
            finally:
                self.unnest()
        return self.cmp_expr()

    PREDS = ("even", "odd", "zero", "positive", "negative")

    def cmp_expr(self):
        a = self.cat_expr()
        for sym, opn in (("<=", "<="), (">=", ">="), ("!=", "!="), ("<", "<"), (">", ">"), ("=", "==")):
            if self.op(sym):
                self.i += 1
                return self.mk(Bin(opn, a, self.cat_expr()))
        if self.at("equals"):
            self.i += 1
            return self.mk(Bin("==", a, self.cat_expr()))
        if self.at("is"):
            self.i += 1
            neg = False
            if self.at("not"):
                self.i += 1
                neg = True
            tok = self.peek()
            if tok is not None and tok.kind == "word" and tok.low in self.PREDS:
                self.i += 1
                e = self.mk(Un(tok.low, a))
                return self.mk(Un("not", e)) if neg else e
            if self.at("less", "than"):
                self.i += 2
                opn = ">=" if neg else "<"
            elif self.at("greater", "than"):
                self.i += 2
                opn = "<=" if neg else ">"
            elif self.at("at", "least"):
                self.i += 2
                opn = "<" if neg else ">="
            elif self.at("at", "most"):
                self.i += 2
                opn = ">" if neg else "<="
            else:
                if self.at("equal", "to"):
                    self.i += 2
                opn = "!=" if neg else "=="
            b = self.cat_expr()
            if neg and opn in ("<", ">", "<=", ">="):
                # 'is not less than' keeps IEEE meaning: not (a < b), which differs from a >= b for NaN
                inner = {"<": ">=", ">": "<=", "<=": ">", ">=": "<"}[opn]
                return self.mk(Un("not", self.mk(Bin(inner, a, b))))
            return self.mk(Bin(opn, a, b))
        return a

    def cat_expr(self):
        a = self.sum_expr()
        parts = [a]
        while self.at("followed", "by"):
            self.i += 2
            parts.append(self.sum_expr())
        return a if len(parts) == 1 else self.mk(Cat(parts))

    def sum_expr(self):
        a = self.term()
        while True:
            if self.at("plus") or self.op("+"):
                self.i += 1
                a = self.mk(Bin("+", a, self.term()))
            elif self.at("minus") or self.op("-"):
                self.i += 1
                a = self.mk(Bin("-", a, self.term()))
            else:
                return a

    def term(self):
        a = self.unary()
        while True:
            if self.at("times") or self.op("*"):
                self.i += 1
                a = self.mk(Bin("*", a, self.unary()))
            elif self.at("divided", "by"):
                self.i += 2
                a = self.mk(Bin("/", a, self.unary()))
            elif self.op("/"):
                self.i += 1
                a = self.mk(Bin("/", a, self.unary()))
            elif self.at("modulo"):
                self.i += 1
                a = self.mk(Bin("rem", a, self.unary()))
            else:
                return a

    def unary(self):
        if self.op("-"):
            self.i += 1
            self.nest()
            try:
                return self.mk(Un("neg", self.unary()))
            finally:
                self.unnest()
        return self.postfix()

    def postfix(self):
        a = self.atom()
        while True:
            if self.at("as", "an", "integer"):
                self.i += 3
                a = self.mk(Conv("as", "int", a))
            elif self.at("as", "a", "fixed"):
                self.i += 3
                a = self.mk(Conv("as", "fix", a))
            elif self.at("as", "a", "float"):
                self.i += 3
                a = self.mk(Conv("as", "float", a))
            elif self.at("rounded", "to", "an", "integer"):
                self.i += 4
                a = self.mk(Conv("rounded", "int", a))
            elif self.at("rounded", "to", "a", "fixed"):
                self.i += 4
                a = self.mk(Conv("rounded", "fix", a))
            elif self.at("rounded", "to", "a", "float"):
                self.i += 4
                a = self.mk(Conv("rounded", "float", a))
            else:
                return a

    def atom(self):
        self.nest()
        try:
            return self._atom()
        finally:
            self.unnest()

    def _atom(self):
        tok = self.peek()
        if tok is None:
            raise OrlogError("SYNTAX", self.line, "an expression is missing")
        if tok.kind == "num":
            self.i += 1
            return self.mk(Num(tok.text))
        if tok.kind == "str":
            self.i += 1
            return self.mk(Str(tok.text[1:-1].replace('""', '"')))
        if self.op("("):
            self.i += 1
            e = self.expr()
            self.eat("@)")
            return e
        if tok.kind != "word":
            raise OrlogError("SYNTAX", self.line, "cannot begin an expression with '%s'" % tok.text)
        w = tok.low
        if w in ("true", "false"):
            self.i += 1
            return self.mk(BoolLit(w == "true"))
        if self.at("this", "law", "@'", "s", "seal"):
            self.i += 5
            return self.mk(Seal())
        if w == "item":
            self.i += 1
            index = self.unary()
            self.eat("of")
            return self.mk(Item(self.ident(), index))
        if self.at("a", "list", "of"):
            self.i += 3
            n = self.sum_expr()
            self.eat("copies", "of")
            return self.mk(ListOf(n, self.unary()))
        if w == "the":
            two = self.peek(1)
            two = two.low if two is not None and two.kind == "word" else None
            if two in PHRASE_HEADS:
                return self.phrase()
            if self._the_is_filler():
                self.i += 1
                return self.mk(Var(self.ident()))
            raise OrlogError("SYNTAX", self.line, "cannot read 'the %s'" % (two or ""))
        if w in RESERVED:
            raise OrlogError("SYNTAX", self.line, "'%s' cannot begin an expression" % tok.text)
        self.i += 1
        return self.mk(Var(tok.text))

    def phrase(self):
        self.eat("the")
        if self.at("sum", "of"):
            self.i += 2
            return self.two("+", "and")
        if self.at("product", "of"):
            self.i += 2
            return self.two("*", "and")
        if self.at("quotient", "of"):
            self.i += 2
            return self.two("quot", "by")
        if self.at("remainder", "of"):
            self.i += 2
            return self.two("rem", "by")
        if self.at("larger", "of"):
            self.i += 2
            return self.two("max", "and")
        if self.at("smaller", "of"):
            self.i += 2
            return self.two("min", "and")
        if self.at("absolute", "value", "of"):
            self.i += 3
            return self.mk(Un("abs", self.unary()))
        if self.at("square", "root", "of"):
            self.i += 3
            return self.mk(Un("sqrt", self.unary()))
        if self.at("integer", "part", "of"):
            self.i += 3
            return self.mk(Un("trunc", self.unary()))
        if self.at("negation", "of"):
            self.i += 2
            return self.mk(Un("neg", self.unary()))
        if self.at("length", "of"):
            self.i += 2
            return self.mk(Length(self.ident()))
        if self.at("list"):
            self.i += 1
            items = [self.sum_expr()]
            while True:
                if self.op(",") and self._starts_expr(1):
                    self.i += 1
                    items.append(self.sum_expr())
                elif self.at("and") and self._starts_expr(1):
                    self.i += 1
                    items.append(self.sum_expr())
                    break
                else:
                    break
            return self.mk(ListLit(items))
        raise OrlogError("SYNTAX", self.line, "cannot read this phrase after 'the'")

    def _starts_expr(self, k):
        tok = self.peek(k)
        if tok is None:
            return False
        if tok.kind in ("num", "str"):
            return True
        if tok.kind == "op":
            return tok.text in ("(", "-")
        return tok.low not in RESERVED or tok.low in ("the", "item", "true", "false", "this")

    def two(self, opn, sep):
        a = self.sum_expr()
        self.eat(sep)
        return self.mk(Bin(opn, a, self.sum_expr()))

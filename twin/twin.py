#!/usr/bin/env python3
"""twin.py -- a clean-room reference interpreter for ORLOG OL-0.

Written from SPEC.md (v0.1, with its §11 amendments) and RUNTIME-SPEC.md alone. The numeric
functions are those of src/orlog/numeric_ref.py and the seal words / check syllable those of
src/orlog/seal.py; both are loaded by file path, so that no other module of the package runs.
"§11 item n" marks a place settled by SPEC §11 (the number is the twin's NOTES number);
"twin reading" marks a place §11 leaves open, listed in twin/probes/EXPECTED.md.

usage:
    python twin.py [--alt N,N...] PROGRAM.orl LAW_SEAL TEXT_SEAL OUTPUT_PATH RECEIPT_PATH [TRACE_PATH]

TRACE_PATH, when given, receives the RUNTIME-SPEC §5 trace lines. --alt switches the listed
items to a reading §11 rejected (ALT_READINGS below); without it the twin follows §11.

Exit status: 0 for a completed or a refused run (output and receipt written);
1 for a compile refusal (nothing written; "twin: compile refused CODE ..." on stderr, §11 G2);
2 for a usage error or a file that cannot be opened or read.
"""
import hashlib
import importlib.util
import os
import re
import struct
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, os.pardir, "src", "orlog"))


def _load(name):
    """Load src/orlog/NAME.py by path, writing no bytecode into that folder."""
    path = os.path.join(SRC, name + ".py")
    spec = importlib.util.spec_from_file_location("orlog_twin_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    saved = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = saved
    return mod


NR = _load("numeric_ref")      # the numeric definition (SPEC §8, RUNTIME-SPEC §2-§3)
SL = _load("seal")             # seal words and check syllable (SPEC §9)
Refusal = NR.Refusal

I64_MAX = NR.I64_MAX
ONE = NR.ONE
LIST_MAX = NR.LIST_MAX         # 2^24
TEXT_MAX = NR.TEXT_MAX         # 2^24
OUTPUT_MAX = 1 << 30
FUEL_MAX = 1 << 62

# ---------------------------------------------------------------- words (SPEC §2, §3)
RESERVED = frozenset("""
let be set to say if then otherwise unless while at most least times do the following for each from perform it must
hold that we claim by given define as provided notwithstanding append remove last item of length list copies is not
and or plus minus divided quotient remainder modulo equals equal less greater than even odd zero positive negative
true false sum product larger smaller absolute value square root integer part float fixed rounded followed this law
seal computation theorem owner certificate agreement decimals are floats negation increase decrease
""".split())

# The words that decide a statement (SPEC §3 "the first word decides").
STATEMENT_WORDS = frozenset("""let set increase decrease say if unless otherwise while for to perform it we
notwithstanding define append remove decimals""".split())

# Reserved words before which ',' and 'and' continue a list literal (§11 item 34).
LIST_GO_ON_WORDS = frozenset(["the", "item", "true", "false", "this"])

NUMERIC = ("I", "X", "F")
ELEM_TYPES = ("I", "X", "F", "B")

# Readings §11 rejected, off by default. "--alt 18,53" (or ALT.update) switches those items
# to the rejected reading, to test whether a disagreement is explained by that item.
ALT_READINGS = {
    15: "Unless C does not count the not",
    18: "an absorbed Otherwise arm names the chain's If/Unless clause",
    24: "a Define's 'unless C' does not count a not",
    35: "and/or evaluate the right operand always (no short-circuit)",
    36: "a unary minus applied directly to a numeric literal is a negative literal (0 ops)",
    37: "'is not <expr>' (equality) is not (=): two operations (the twin's v0 reading)",
    52: "each RULE-CONFLICT comparison counts one operation",
    53: "event E carries the 0-based index k-1",
    54: "event E carries the raw slot (8 bytes, or 1 for Bool) without the value encoding's tag byte",
    57: "the receipt ends without an LF after 'end'",
}
ALT = set()


class CompileRefusal(Exception):
    def __init__(self, code, line=None, clause=None, detail=""):
        Exception.__init__(self, code)
        self.code = code
        self.line = line
        self.clause = clause
        self.detail = detail


class SyntaxFail(Exception):
    """A statement that does not parse; at_err when the parser stopped at an unreadable token."""

    def __init__(self, what, at_err=False):
        Exception.__init__(self, what)
        self.at_err = at_err


class Stop(Exception):
    """A run-time refusal that already names its clause."""

    def __init__(self, code, clause):
        Exception.__init__(self, code)
        self.code = code
        self.clause = clause


# ---------------------------------------------------------------- tokens (SPEC §2)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
NUM_RE = re.compile(r"[0-9]+(?:\.[0-9]+)?")
REF_RE = re.compile("§([0-9]+(?:\\.[0-9]+)*)")
OPS2 = ("<=", ">=", "!=")
OPS1 = "-+*/(),;:<>='"


class Tok(object):
    __slots__ = ("kind", "text", "val", "low")

    def __init__(self, kind, text, val=None):
        self.kind = kind
        self.text = text
        self.val = val
        self.low = text.lower() if kind == "word" else None

    def __repr__(self):
        return "%s %r" % (self.kind, self.text)


def tokenize(s):
    """Longest match at each position; tokens need no separating space (§11 item 10).

    An unreadable token (a character that begins no token, an unterminated text, a section
    sign without digits) ends the list as one 'err' token. The parser stops there only if it
    gets that far, so the first offending position in the statement decides between LEX and
    SYNTAX (§11 item 8; the order within a clause is a twin reading, see EXPECTED.md)."""
    toks = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == " ":
            i += 1
            continue
        if ch == "§":
            m = REF_RE.match(s, i)
            if not m:
                toks.append(Tok("err", s[i:]))
                return toks
            toks.append(Tok("ref", m.group(0), tuple(int(p) for p in m.group(1).split("."))))
            i = m.end()
            continue
        if "0" <= ch <= "9":
            m = NUM_RE.match(s, i)
            toks.append(Tok("num", m.group(0)))
            i = m.end()
            continue
        if ch == '"':
            j = i + 1
            buf = []
            ok = False
            while j < n:
                c = s[j]
                if c == '"':
                    if j + 1 < n and s[j + 1] == '"':
                        buf.append('"')
                        j += 2
                        continue
                    j += 1
                    ok = True
                    break
                if c in "\r\n":
                    break
                buf.append(c)
                j += 1
            if not ok:
                toks.append(Tok("err", s[i:]))
                return toks
            toks.append(Tok("str", s[i:j], "".join(buf).encode("utf-8")))
            i = j
            continue
        if ("A" <= ch <= "Z") or ("a" <= ch <= "z"):
            m = WORD_RE.match(s, i)
            toks.append(Tok("word", m.group(0)))
            i = m.end()
            continue
        if s[i:i + 2] in OPS2:
            toks.append(Tok("op", s[i:i + 2]))
            i += 2
            continue
        if ch in OPS1:
            toks.append(Tok("op", ch))
            i += 1
            continue
        toks.append(Tok("err", s[i:]))
        return toks
    return toks


def list_goes_on(tok):
    """§11 item 34: inside a list literal, ',' and 'and' continue the list only before a number,
    a text, '(', '-', a word that is not reserved, or the, item, true, false, this."""
    if tok is None:
        return False
    if tok.kind in ("num", "str"):
        return True
    if tok.kind == "op":
        return tok.text in ("(", "-")
    if tok.kind == "word":
        return tok.low not in RESERVED or tok.low in LIST_GO_ON_WORDS
    return False


BLOCK = ("block",)


# ---------------------------------------------------------------- parser (SPEC §3, §4)
class Parser(object):
    def __init__(self, toks):
        self.t = toks
        self.i = 0

    # -- helpers
    def peek(self, k=0):
        """The token k ahead. Looking at an unreadable token is LEX at once, as with a lazy lexer:
        the parser reads no further than it needs, so the first offending position decides."""
        j = self.i + k
        if j >= len(self.t):
            return None
        tok = self.t[j]
        if tok.kind == "err":
            raise SyntaxFail("an unreadable token at %r" % tok.text, at_err=True)
        return tok

    def at_end(self):
        return self.i >= len(self.t)

    def kw(self, w, k=0):
        tok = self.peek(k)
        return tok is not None and tok.kind == "word" and tok.low == w

    def op(self, o, k=0):
        tok = self.peek(k)
        return tok is not None and tok.kind == "op" and tok.text == o

    def seq(self, *items):
        for k, it in enumerate(items):
            if it[0].isalpha():
                if not self.kw(it, k):
                    return False
            elif not self.op(it, k):
                return False
        return True

    def take(self, *items):
        if self.seq(*items):
            self.i += len(items)
            return True
        return False

    def need(self, *items):
        if not self.take(*items):
            self.fail("expected '%s'" % " ".join(items))

    def need_end(self):
        if not self.at_end():
            self.fail("unexpected text")

    def fail(self, what):
        tok = self.peek()           # raises LEX itself when the current token is unreadable
        raise SyntaxFail("%s at %s" % (what, repr(tok) if tok is not None else "the end of the statement"))

    def ident(self):
        """An identifier, with the optional filler 'the' (SPEC §4 'the'; §11 item 26)."""
        tok = self.peek()
        if tok is not None and tok.kind == "word" and tok.low == "the":
            nxt = self.peek(1)
            if nxt is not None and nxt.kind == "word" and nxt.low not in RESERVED:
                self.i += 1
                tok = nxt
        if tok is None or tok.kind != "word" or tok.low in RESERVED:
            self.fail("an identifier expected")
        self.i += 1
        return tok.text

    def ref(self):
        tok = self.peek()
        if tok is None or tok.kind != "ref":
            self.fail("a clause reference expected")
        self.i += 1
        return tok.val

    def string(self):
        tok = self.peek()
        if tok is None or tok.kind != "str":
            self.fail("a text literal expected")
        self.i += 1
        return tok.val

    def block_rest(self):
        """True (and consumed) when the rest of the statement is exactly 'do the following'."""
        if self.seq("do", "the", "following") and self.peek(3) is None:
            self.i += 3
            return True
        return False

    def name_words(self):
        """A procedure name in a call. A name cannot begin with a reserved word (§11 item 20),
        so a call whose first word is reserved is SYNTAX (twin reading, see EXPECTED.md)."""
        first = self.peek()
        if first is not None and first.kind == "word" and first.low in RESERVED:
            self.fail("a procedure name cannot begin with a reserved word")
        words = []
        while not self.at_end() and not self.op(";"):
            tok = self.peek()
            if tok.kind != "word":
                self.fail("a procedure name is words only")
            words.append(tok.low)
            self.i += 1
        if not words:
            self.fail("a procedure name expected")
        return " ".join(words)

    # -- expressions (SPEC §4, lowest precedence first)
    def expr(self):
        return self.p_or()

    def p_or(self):
        a = self.p_and()
        while self.kw("or"):
            self.i += 1
            a = ("or", a, self.p_and())
        return a

    def p_and(self):
        a = self.p_not()
        while self.kw("and"):
            self.i += 1
            a = ("and", a, self.p_not())
        return a

    def p_not(self):
        if self.take("not"):
            return ("not", self.p_not())
        if self.take("it", "is", "not", "the", "case", "that"):
            return ("not", self.p_not())
        return self.p_cmp()

    def p_cmp(self):
        a = self.p_cat()
        tok = self.peek()
        if tok is not None and tok.kind == "op" and tok.text in ("<=", ">=", "!=", "<", ">", "="):
            self.i += 1
            return ("cmp", tok.text, a, self.p_cat())
        if self.take("equals"):
            return ("cmp", "=", a, self.p_cat())
        if self.take("is"):
            neg = self.take("not")
            node = None
            for pred in ("even", "odd", "zero", "positive", "negative"):
                if self.take(pred):
                    node = ("pred", pred, a)
                    break
            if node is None:
                if self.take("less", "than"):
                    node = ("cmp", "<", a, self.p_cat())
                elif self.take("greater", "than"):
                    node = ("cmp", ">", a, self.p_cat())
                elif self.take("at", "least"):
                    node = ("cmp", ">=", a, self.p_cat())
                elif self.take("at", "most"):
                    node = ("cmp", "<=", a, self.p_cat())
                else:
                    self.take("equal", "to")
                    node = ("cmp", "=", a, self.p_cat())
                    if neg and 37 not in ALT:
                        return ("cmp", "!=", a, node[3])     # §11 item 37: one operation
            # 'is not <predicate>' and 'is not less than' and kin: a not around the test (§11 item 37)
            return ("not", node) if neg else node
        return a

    def p_cat(self):
        parts = [self.p_sum()]
        while self.take("followed", "by"):
            parts.append(self.p_sum())
        return parts[0] if len(parts) == 1 else ("cat", parts)

    def p_sum(self):
        a = self.p_term()
        while True:
            if self.take("plus") or self.take("+"):
                a = ("bin", "+", a, self.p_term())
            elif self.take("minus") or self.take("-"):
                a = ("bin", "-", a, self.p_term())
            else:
                return a

    def p_term(self):
        a = self.p_unary()
        while True:
            if self.take("times") or self.take("*"):
                a = ("bin", "*", a, self.p_unary())
            elif self.take("divided", "by") or self.take("/"):
                a = ("bin", "/", a, self.p_unary())
            elif self.take("modulo"):
                a = ("bin", "mod", a, self.p_unary())
            else:
                return a

    def p_unary(self):
        if self.take("-"):
            return ("neg", self.p_unary())      # a counted negation, never a negative literal (§11 item 36)
        return self.p_postfix()

    POSTFIX = (
        (("as", "an", "integer"), "I", False),
        (("as", "a", "fixed"), "X", False),
        (("as", "a", "float"), "F", False),
        (("rounded", "to", "an", "integer"), "I", True),
        (("rounded", "to", "a", "fixed"), "X", True),
        (("rounded", "to", "a", "float"), "F", True),
    )

    def p_postfix(self):
        a = self.p_atom()
        while True:
            for words, target, rounded in self.POSTFIX:
                if self.take(*words):
                    a = ("conv", target, rounded, a)
                    break
            else:
                return a

    def p_atom(self):
        tok = self.peek()
        if tok is None:
            self.fail("an expression expected")
        if tok.kind == "num":
            self.i += 1
            return ("num", tok.text)
        if tok.kind == "str":
            self.i += 1
            return ("str", tok.val)
        if tok.kind == "op":
            if tok.text == "(":
                self.i += 1
                e = self.expr()
                self.need(")")
                return e
            self.fail("an expression expected")
        if tok.kind != "word":
            self.fail("an expression expected")
        w = tok.low
        if w == "true":
            self.i += 1
            return ("bool", True)
        if w == "false":
            self.i += 1
            return ("bool", False)
        if self.take("this", "law", "'", "s", "seal"):
            return ("seal",)
        if w == "item":
            self.i += 1
            idx = self.p_unary()
            self.need("of")
            return ("item", idx, self.ident())
        if self.take("a", "list", "of"):
            n = self.p_sum()
            self.need("copies", "of")
            return ("copies", n, self.p_unary())
        if w == "the":
            nxt = self.peek(1)
            if nxt is not None and nxt.kind == "word" and nxt.low in RESERVED:
                self.i += 1
                return self.p_phrase()
            return ("var", self.ident())
        if w in RESERVED:
            self.fail("a reserved word where an expression was expected")
        self.i += 1
        return ("var", tok.text)

    def p_phrase(self):
        if self.take("sum", "of"):
            a = self.p_sum()
            self.need("and")
            return ("bin", "+", a, self.p_sum())
        if self.take("product", "of"):
            a = self.p_sum()
            self.need("and")
            return ("bin", "*", a, self.p_sum())
        if self.take("quotient", "of"):
            a = self.p_sum()
            self.need("by")
            return ("quot", a, self.p_sum())
        if self.take("remainder", "of"):
            a = self.p_sum()
            self.need("by")
            return ("bin", "mod", a, self.p_sum())
        if self.take("larger", "of"):
            a = self.p_sum()
            self.need("and")
            return ("max", a, self.p_sum())
        if self.take("smaller", "of"):
            a = self.p_sum()
            self.need("and")
            return ("min", a, self.p_sum())
        if self.take("absolute", "value", "of"):
            return ("abs", self.p_unary())
        if self.take("square", "root", "of"):
            return ("sqrt", self.p_unary())
        if self.take("integer", "part", "of"):
            return ("intpart", self.p_unary())
        if self.take("negation", "of"):
            return ("neg", self.p_unary())
        if self.take("length", "of"):
            return ("len", self.ident())
        if self.take("list"):
            items = [self.p_sum()]
            while self.op(",") and list_goes_on(self.peek(1)):
                self.i += 1
                items.append(self.p_sum())
            if self.kw("and") and list_goes_on(self.peek(1)):
                self.i += 1
                items.append(self.p_sum())
            return ("list", items)
        self.fail("a phrase expected after 'the'")

    # -- statements (SPEC §3)
    def statement(self):
        tok = self.peek()
        if tok is None or tok.kind != "word":
            self.fail("a statement must begin with a word")
        w = tok.low
        if w == "if":
            self.i += 1
            return self.st_if()
        if w == "unless":
            self.i += 1
            return self.st_unless()
        if w == "otherwise":
            self.i += 1
            return self.st_otherwise()
        if w == "while":
            self.i += 1
            return self.st_while()
        if w == "for":
            self.i += 1
            return self.st_for()
        if w == "to":
            self.i += 1
            return self.st_to()
        if w in ("notwithstanding", "define"):
            return self.st_define()
        if w == "decimals":
            self.i += 1
            self.need("are")
            if self.take("fixed"):
                mode = "fixed"
            elif self.take("floats"):
                mode = "floats"
            else:
                self.fail("'fixed' or 'floats' expected")
            self.need_end()
            return ("decimals", mode)
        s = self.inline()
        self.need_end()
        return s

    def inline(self):
        """An inline statement (SPEC §3): Let, Set, Increase, Decrease, Say, Append, Remove,
        Perform or a bare procedure name, the must form and the claim form."""
        tok = self.peek()
        if tok is None or tok.kind != "word":
            self.fail("a statement expected")
        w = tok.low
        if w == "let":
            self.i += 1
            name = self.ident()
            self.need("be")
            return ("let", name, self.expr())
        if w == "set":
            self.i += 1
            if self.take("item"):
                idx = self.p_unary()        # §11 item 27: a unary, as in the atom
                self.need("of")
                name = self.ident()
                self.need("to")
                return ("setitem", idx, name, self.expr())
            name = self.ident()
            self.need("to")
            return ("set", name, self.expr())
        if w in ("increase", "decrease"):
            self.i += 1
            sign = 1 if w == "increase" else -1
            if self.take("item"):
                idx = self.p_unary()        # §11 item 27
                self.need("of")
                name = self.ident()
                self.need("by")
                return ("incitem", sign, idx, name, self.expr())
            name = self.ident()
            self.need("by")
            return ("inc", sign, name, self.expr())
        if w == "say":
            self.i += 1
            return ("say", self.expr())
        if w == "append":
            self.i += 1
            e = self.expr()
            self.need("to")
            return ("append", e, self.ident())
        if w == "remove":
            self.i += 1
            self.need("the", "last", "item", "of")
            return ("remove", self.ident())
        if w == "perform":
            self.i += 1
            return ("perform", self.name_words())
        if w == "it":
            self.i += 1
            self.need("must", "hold", "that")
            return ("must", self.expr())
        if w == "we":
            self.i += 1
            self.need("claim", "that")
            cond = self.expr()
            oracle = ("computation",)
            premises = []
            if self.op(",") and self.kw("by", 1):
                self.i += 2
                oracle = self.oracle()
            if self.op(",") and self.kw("given", 1):
                self.i += 2
                premises.append(self.ref())
                while self.op(",") and self.peek(1) is not None and self.peek(1).kind == "ref":
                    self.i += 1
                    premises.append(self.ref())
                if self.take("and"):
                    premises.append(self.ref())
            return ("claim", cond, oracle, premises)
        if w in STATEMENT_WORDS:
            self.fail("not an inline statement")
        return ("perform", self.name_words())

    def oracle(self):
        if self.take("computation"):
            return ("computation",)
        if self.take("the", "theorem"):
            return ("theorem", self.string())
        if self.take("the", "owner"):
            return ("owner",)
        if self.take("the", "certificate", "of"):
            r = self.ref()
            if self.take("under", "the", "theorem"):
                return ("certificate", r, self.string())
            return ("certificate", r, None)
        if self.take("agreement", "of"):
            a = self.ref()
            self.need("and")
            return ("agreement", a, self.ref())
        self.fail("an oracle expected")

    def arm(self):
        """After 'If C,' or 'Otherwise, if C,' or 'Unless C,': a block or an inline statement."""
        if self.block_rest():
            return BLOCK
        return self.inline()

    def st_if(self):
        cond = self.expr()
        self.need(",")
        self.take("then")
        if self.block_rest():
            return ("if", cond, BLOCK, None)
        s1 = self.inline()
        if self.take(";"):
            self.need("otherwise")
            self.take(",")
            s2 = self.inline()
            self.need_end()
            return ("if", cond, s1, s2)
        self.need_end()
        return ("if", cond, s1, None)

    def st_unless(self):
        # §11 item 16: no 'then' and no inline '; otherwise' for Unless.
        cond = self.expr()
        self.need(",")
        s = self.arm()
        self.need_end()
        return ("unless", cond, s)

    def st_otherwise(self):
        self.need(",")
        if self.take("if"):
            cond = self.expr()
            self.need(",")
            self.take("then")
            s = self.arm()
            self.need_end()            # §11 item 17: no inline '; otherwise' in an else-if arm
            return ("otherwise_if", cond, s)
        s = self.arm()
        self.need_end()
        return ("otherwise", s)

    def st_while(self):
        cond = self.expr()
        self.need(",")
        self.need("at", "most")
        tok = self.peek()
        if tok is None or tok.kind != "num" or "." in tok.text:
            self.fail("an integer literal expected for the bound")
        self.i += 1
        self.need("times")
        self.need(",")
        self.need("do", "the", "following")
        self.need_end()
        return ("while", cond, int(tok.text))

    def st_for(self):
        self.need("each")
        name = self.ident()
        self.need("from")
        lo = self.p_sum()
        self.need("to")
        hi = self.p_sum()
        self.need(",")
        self.need("do", "the", "following")
        self.need_end()
        return ("for", name, lo, hi)

    def st_to(self):
        words = []
        while self.peek() is not None and self.peek().kind == "word":
            words.append(self.peek().low)
            self.i += 1
        if not words:
            self.fail("a procedure name expected")
        self.need(",")
        self.need("do", "the", "following")
        self.need_end()
        return ("to", " ".join(words))      # a reserved first word is PROCEDURE-NAME, phase 3

    def st_define(self):
        refs = []
        if self.take("notwithstanding"):
            # §11 item 23: one or more references, '§a(, §b)*( and §c)?'
            refs.append(self.ref())
            while self.op(",") and self.peek(1) is not None and self.peek(1).kind == "ref":
                self.i += 1
                refs.append(self.ref())
            if self.take("and"):
                refs.append(self.ref())
            self.need(",")
        self.need("define")
        name = self.ident()
        self.need("as")
        value = self.expr()
        provided = None
        unless = None
        # §11 item 25: at most one proviso; a second one is SYNTAX (need_end below)
        if self.op(",") and self.kw("provided", 1) and self.kw("that", 2):
            self.i += 3
            provided = self.expr()
        elif self.op(",") and self.kw("unless", 1):
            self.i += 2
            unless = self.expr()
        self.need_end()
        return ("define", refs, name, value, provided, unless)


def inline_parts(stmt):
    """The inline statements written inside a clause's statement."""
    k = stmt[0]
    out = []
    if k == "if":
        out = [stmt[2], stmt[3]]
    elif k in ("unless", "otherwise_if"):
        out = [stmt[2]]
    elif k == "otherwise":
        out = [stmt[1]]
    return [s for s in out if s is not None and s is not BLOCK]


def is_block_form(stmt):
    k = stmt[0]
    if k in ("while", "for", "to"):
        return True
    if k in ("if", "unless", "otherwise_if"):
        return stmt[2] is BLOCK
    if k == "otherwise":
        return stmt[1] is BLOCK
    return False


# ---------------------------------------------------------------- lines (SPEC §1)
PQ = "[%s][%s][%s][%s][%s]" % (SL.CONS, SL.VOWS, SL.CONS, SL.VOWS, SL.CONS)
SEALED_RE = re.compile(r"^Sealed: (%s(?:-%s){3})\.$" % (PQ, PQ))
SUFFIX_RE = re.compile(r"^(.*\.) \[([a-z]{3})\]$")
LABEL_RE = re.compile("^(?:§([0-9]+(?:\\.[0-9]+)*)|([0-9]+(?:\\.[0-9]+)*)\\.) (.*)$")


class Clause(object):
    __slots__ = ("id", "label", "line", "text", "stmt", "children", "parent")

    def __init__(self, cid, label, line, text, stmt):
        self.id = cid
        self.label = label
        self.line = line
        self.text = text
        self.stmt = stmt
        self.children = []
        self.parent = None


def numbering_ok(prev, cur):
    if prev is None:
        return cur == (1,)
    if cur == prev[:-1] + (prev[-1] + 1,):
        return True
    if cur == prev + (1,):
        return True
    for i in range(1, len(prev)):
        anc = prev[:i]
        if cur == anc[:-1] + (anc[-1] + 1,):
            return True
    return False


def phase_lines(text):
    """§11 G3 phase 2: every line, in line order; within a line, LINE-FORM, TITLE-PLACE,
    SEAL-FORM, SEAL-PLACE, LINE-CHECK, NUMBERING. The first line with a fault decides
    (twin reading: the code list orders the checks of one line, not passes over all lines).
    Statements are not parsed here. Returns the clause lines and the Sealed line, if any."""
    raws = []
    title_seen = False
    content_seen = False        # a clause line or the Sealed line (twin reading of "content", item 3)
    sealed = None
    prev = None
    for ln, line in enumerate(text.split("\n"), 1):
        if line.strip(" ") == "":                      # §11 item 1
            continue
        if line.startswith("Note:"):                   # §11 items 2, 4: anywhere, after Sealed too
            continue
        if line.startswith("Title:"):                  # §11 items 2, 3
            if title_seen or content_seen:
                raise CompileRefusal("TITLE-PLACE", line=ln, detail="a second Title, or a Title after content")
            title_seen = True
            continue
        if line.startswith("Sealed: "):                # §11 items 2, 4, 5
            m = SEALED_RE.match(line)
            if not m:
                raise CompileRefusal("SEAL-FORM", line=ln, detail="not four '-'-joined proquints and a period")
            if sealed is not None:
                raise CompileRefusal("SEAL-PLACE", line=ln, detail="a line after the Sealed line")
            sealed = (ln, m.group(1))
            content_seen = True
            continue
        m = SUFFIX_RE.match(line)
        if m:
            body, suffix = m.group(1), m.group(2)
        else:
            body, suffix = line, None
        m2 = LABEL_RE.match(body)
        stmt_text = m2.group(3) if m2 else ""
        if not m2 or not stmt_text.endswith(".") or stmt_text.startswith(" "):     # §11 items 6, 7
            raise CompileRefusal("LINE-FORM", line=ln, detail="not a clause line")
        if sealed is not None:
            raise CompileRefusal("SEAL-PLACE", line=ln, detail="a line after the Sealed line")
        if suffix is not None and suffix != SL.line_check(body):
            raise CompileRefusal("LINE-CHECK", line=ln, detail="check suffix [%s], computed [%s]"
                                 % (suffix, SL.line_check(body)))
        label_text = m2.group(1) if m2.group(1) is not None else m2.group(2)
        label = tuple(int(p) for p in label_text.split("."))   # §11 item 6: parts compared as integers
        if not numbering_ok(prev, label):
            raise CompileRefusal("NUMBERING", line=ln, detail="label %s after %s" % (
                ".".join(map(str, label)), ".".join(map(str, prev)) if prev else "nothing"))
        prev = label
        raws.append((ln, line, label, stmt_text[:-1]))
        content_seen = True
    return raws, sealed


def phase_syntax(raws):
    """§11 G3 phase 3: statement syntax, in clause order; within a clause SYNTAX or LEX (the first
    offending position), then PROCEDURE-NAME, then UNKNOWN-PROCEDURE. Returns the clauses."""
    parsed = []
    for (ln, line, label, text) in raws:
        try:
            toks = tokenize(text)
            if not toks:
                raise SyntaxFail("an empty statement")
            parsed.append((Parser(toks).statement(), None, None))
        except SyntaxFail as e:                                    # §11 item 8
            parsed.append((None, "LEX" if e.at_err else "SYNTAX", str(e)))
    names = set(p[0][1] for p in parsed if p[0] is not None and p[0][0] == "to")
    clauses = []
    for i, ((ln, line, label, text), (stmt, code, detail)) in enumerate(zip(raws, parsed)):
        cid = i + 1
        if code is not None:
            raise CompileRefusal(code, line=ln, clause=cid, detail=detail)
        if stmt[0] == "to" and stmt[1].split(" ")[0] in RESERVED:  # §11 items 20, 21
            raise CompileRefusal("PROCEDURE-NAME", line=ln, clause=cid,
                                 detail="'%s' begins with a reserved word" % stmt[1])
        for s in [stmt] + inline_parts(stmt):
            if s[0] == "perform" and s[1] not in names:
                raise CompileRefusal("UNKNOWN-PROCEDURE", line=ln, clause=cid, detail=s[1])
        clauses.append(Clause(cid, label, ln, line, stmt))
    return clauses


# ---------------------------------------------------------------- values
def enc(t, v):
    """RUNTIME-SPEC §5 value encodings."""
    if t == "I" or t == "X":
        return t.encode() + struct.pack(">q", v)
    if t == "F":
        return b"F" + struct.pack(">Q", NR.f_bits(NR.f_canon(v)))
    if t == "B":
        return b"B\x01" if v else b"B\x00"
    if t == "T":
        return b"T" + struct.pack(">I", len(v)) + v
    et = t[1]
    return b"L" + et.encode() + struct.pack(">I", len(v)) + b"".join(slot(et, x) for x in v)


def slot(et, x):
    if et == "I" or et == "X":
        return struct.pack(">q", x)
    if et == "F":
        return struct.pack(">Q", NR.f_bits(NR.f_canon(x)))
    return b"\x01" if x else b"\x00"


def to_text(t, v):
    """RUNTIME-SPEC §3 printing; Text as is."""
    if t == "T":
        return v
    if t == "I":
        return NR.fmt_i(v).encode("ascii")
    if t == "X":
        return NR.fmt_x(v).encode("ascii")
    if t == "F":
        return NR.fmt_f(v).encode("ascii")
    if t == "B":
        return b"true" if v else b"false"
    et = t[1]
    return b"[" + b", ".join(to_text(et, x) for x in v) + b"]"


def u32(n):
    return struct.pack(">I", n)


def u64(n):
    return struct.pack(">Q", n)


def is_list(t):
    return len(t) == 2


# arithmetic by type (SPEC §8 / numeric_ref)
ARITH = {
    "I": {"+": NR.i_add, "-": NR.i_sub, "*": NR.i_mul, "/": NR.i_div, "mod": NR.i_rem, "quot": NR.i_quot,
          "max": NR.i_max, "min": NR.i_min, "neg": NR.i_neg, "abs": NR.i_abs, "sqrt": NR.i_isqrt},
    "X": {"+": NR.x_add, "-": NR.x_sub, "*": NR.x_mul, "/": NR.x_div,
          "max": NR.x_max, "min": NR.x_min, "neg": NR.x_neg, "abs": NR.x_abs, "sqrt": NR.x_sqrt},
    "F": {"+": NR.f_add, "-": NR.f_sub, "*": NR.f_mul, "/": NR.f_div,
          "max": NR.f_max, "min": NR.f_min, "neg": NR.f_neg, "abs": NR.f_abs, "sqrt": NR.f_sqrt},
}


CONVERT = {
    # (from, to, rounded) -> function   (SPEC §5 conversion table; identity refused, §11 item 43)
    ("X", "I", False): NR.x_as_i,       # §11 item 59
    ("X", "I", True): NR.x_round,
    ("F", "I", False): NR.f_as_i,       # §11 item 59
    ("F", "I", True): NR.f_round,
    ("I", "X", False): NR.x_from_i,
    ("I", "X", True): NR.x_from_i,
    ("F", "X", False): lambda x: NR.f_to_x(x, False),
    ("F", "X", True): lambda x: NR.f_to_x(x, True),
    ("I", "F", False): lambda n: NR.f_from_i(n, False),
    ("I", "F", True): lambda n: NR.f_from_i(n, True),
    ("X", "F", False): lambda a: NR.x_to_f(a, False),
    ("X", "F", True): lambda a: NR.x_to_f(a, True),
}

# The implicit promotion of an Int (SPEC §5): to Fix by x_from_i, to Float exactly (§11 item 40).
PROMOTE = {"X": NR.x_from_i, "F": lambda n: NR.f_from_i(n, False)}


def values_equal(t, a, b):
    if t == "F":
        return a == b              # IEEE: NaN != NaN
    return a == b


# ---------------------------------------------------------------- the compiler (SPEC §5)
class Var(object):
    __slots__ = ("name", "vid", "type", "counter")

    def __init__(self, name, vid, t, counter):
        self.name = name
        self.vid = vid
        self.type = t
        self.counter = counter


class RuleDef(object):
    __slots__ = ("cid", "targets", "value", "proviso")

    def __init__(self, cid, targets, value, proviso):
        self.cid = cid
        self.targets = targets
        self.value = value
        self.proviso = proviso


class Proc(object):
    __slots__ = ("name", "clause", "body")

    def __init__(self, name, clause):
        self.name = name
        self.clause = clause
        self.body = []


class Chain(object):
    """An If/Unless chain with its absorbed Otherwise arms (SPEC §3, §7 'If chain')."""

    def __init__(self, head):
        self.head = head        # the If/Unless clause
        self.arms = []          # (condition, the arm's clause id, body)
        self.else_body = None
        self.has_else = False

    def run(self, rt):
        for cond, cc, body in self.arms:
            rt.ops += 1
            try:
                v = cond(rt)
            except Refusal as e:
                raise Stop(e.code, cc)          # §11 item 18: the arm's own clause
            if v:
                body(rt)
                return
        if self.else_body is not None:
            self.else_body(rt)


def run_block(execs):
    def run(rt):
        for s in execs:
            s(rt)
    return run


def wrap_cost(ex, cid):
    """SPEC §7 cost counters: start before the statement's own +1, grow by ops - start after it."""
    def run(rt):
        start = rt.ops
        ex(rt)
        rt.cost[cid] += rt.ops - start
    return run


def const(v):
    return lambda rt: v


class Program(object):
    def __init__(self, body, n_vars, claim_clauses, cert_ids, seal_words):
        self.body = body
        self.n_vars = n_vars
        self.claim_clauses = claim_clauses
        self.cert_ids = cert_ids
        self.seal_words = seal_words


class Compiler(object):
    def __init__(self, clauses, seal_words):
        self.clauses = clauses
        self.seal_bytes = seal_words.encode("ascii")
        self.label_map = {}
        for cl in clauses:
            self.label_map[cl.label] = cl
        self.scopes = []
        self.n_vars = 0
        self.claim_clauses = []
        self.n_musts = 0
        self.decimals = "fixed"
        self.decimals_set = False
        self.decimal_seen = False
        self.cur = None
        self.in_proc = None
        self.proc_defined = {}
        self.rule_compiled = {}
        self.rule_type = {}
        # pre-collection: rule names, procedure names, certificate targets (§11 item 47)
        self.rule_defs = {}
        self.proc_names = set()
        self.cert_ids = set()
        for cl in clauses:
            s = cl.stmt
            if s[0] == "define":
                self.rule_defs.setdefault(s[2], []).append(cl)
            elif s[0] == "to":
                self.proc_names.add(s[1])
            for c in [s] + inline_parts(s):
                if c[0] == "claim" and c[2][0] == "certificate":
                    tgt = self.label_map.get(c[2][1])
                    if tgt is not None:
                        self.cert_ids.add(tgt.id)

    def refuse(self, code, detail="", clause=None):
        cl = clause if clause is not None else self.cur
        raise CompileRefusal(code, line=cl.line if cl else None, clause=cl.id if cl else None, detail=detail)

    # -- the tree
    def build_tree(self):
        top = []
        for cl in self.clauses:
            if len(cl.label) == 1:
                top.append(cl)
            else:
                parent = self.label_map[cl.label[:-1]]
                cl.parent = parent
                parent.children.append(cl)
        return top

    def compile(self):
        """§11 G3 phases 4 to 7 (phases 2 and 3 have run; phase 8 is compile_text's)."""
        top = self.build_tree()
        self.phase_shape(top)                   # 4
        self.phase_define_place()               # 5
        body = self.compile_block(top)          # 6: static semantics, in document walk order
        self.phase_cycles()                     # 7
        return Program(body, self.n_vars, self.claim_clauses, sorted(self.cert_ids), None)

    def phase_shape(self, top):
        """Phase 4: block shape and Otherwise attachment, in tree order; within a clause
        ORPHAN-OTHERWISE, EMPTY-BLOCK, UNEXPECTED-CHILDREN."""
        def walk(siblings):
            open_chain = False
            for cl in siblings:
                s = cl.stmt
                k = s[0]
                if k in ("otherwise", "otherwise_if"):
                    if not open_chain:
                        self.refuse("ORPHAN-OTHERWISE", clause=cl)
                    if k == "otherwise":
                        open_chain = False
                elif k == "if":
                    open_chain = s[3] is None       # an inline otherwise closes the chain
                elif k == "unless":
                    open_chain = True               # §11 item 16: an Otherwise after it attaches
                else:
                    open_chain = False
                needs = is_block_form(s)
                if needs and not cl.children:
                    self.refuse("EMPTY-BLOCK", clause=cl)
                if not needs and cl.children:
                    self.refuse("UNEXPECTED-CHILDREN", clause=cl)
                walk(cl.children)
        walk(top)

    def phase_define_place(self):
        """Phase 5: DEFINE-PLACE, over all clauses (in document order)."""
        for cl in self.clauses:
            if cl.stmt[0] == "define" and len(cl.label) != 1:
                self.refuse("DEFINE-PLACE", clause=cl)

    def phase_cycles(self):
        """Phase 7: PRIORITY-CYCLE, rule names in the order of their first Define."""
        for name in self.rule_compiled:
            defs = self.rule_compiled[name]
            over = override_closure(defs)
            for d in defs:
                if d.cid in over[d.cid]:
                    self.refuse("PRIORITY-CYCLE", "rule %s" % name, clause=self.clauses[d.cid - 1])

    # -- scopes (SPEC §5 Scopes)
    def find_var(self, name):
        for sc in reversed(self.scopes):
            v = sc.get(name)
            if v is not None:
                return v
        return None

    def declare(self, name, t, counter=False):
        for sc in self.scopes:
            if name in sc:
                self.refuse("REDECLARED", "%s is visible in an enclosing scope" % name)
        if name in self.rule_defs:                          # §11 item 47: any rule, wherever defined
            self.refuse("REDECLARED", "%s names a rule" % name)
        if name.lower() in self.proc_defined:               # §11 item 47: a procedure already defined
            self.refuse("REDECLARED", "%s names a procedure" % name)
        v = Var(name, self.n_vars, t, counter)
        self.n_vars += 1
        self.scopes[-1][name] = v
        return v

    def lookup(self, name):
        """A name in a position that needs a variable. A rule name is not a variable: UNDECLARED
        (§11 item 48 for writes; for list reads, item and length of, a twin reading)."""
        v = self.find_var(name)
        if v is None:
            self.refuse("UNDECLARED", name)
        return v

    def lookup_list(self, name):
        v = self.lookup(name)
        if not is_list(v.type):
            self.refuse("TYPE", "%s is not a list" % name)
        return v

    # -- blocks
    def compile_block(self, clauses):
        self.scopes.append({})
        execs = []
        chain = None
        for cl in clauses:
            self.cur = cl
            s = cl.stmt
            k = s[0]
            if k in ("otherwise", "otherwise_if"):
                if chain is None or chain.has_else:
                    raise AssertionError("phase 4 lets no orphan through")
                ncl = chain.head if 18 in ALT else cl       # §11 item 18: the arm names its own clause
                if k == "otherwise":
                    chain.else_body = self.compile_arm(cl, s[1], ncl)
                    chain.has_else = True
                else:
                    cond = self.cbool(s[1])
                    chain.arms.append((cond, ncl.id, self.compile_arm(cl, s[2], ncl)))
                continue
            chain = None
            ex = self.compile_stmt(cl)
            if isinstance(ex, Chain):
                if not ex.has_else:
                    chain = ex
                ex = ex.run
            if ex is not None:
                if cl.id in self.cert_ids:
                    ex = wrap_cost(ex, cl.id)
                execs.append(ex)
        self.scopes.pop()
        return execs

    def compile_arm(self, cl, part, ncl=None):
        """cl owns the arm's children; ncl (default cl) is the clause an inline arm names."""
        if part is BLOCK:
            body = self.compile_block(cl.children)
            return run_block(body)
        self.scopes.append({})                  # each inline arm opens a scope
        ex = self.compile_inline(ncl if ncl is not None else cl, part)
        self.scopes.pop()
        return ex

    # -- statements
    def compile_stmt(self, cl):
        s = cl.stmt
        k = s[0]
        c = cl.id
        if k == "if":
            ch = Chain(cl)
            cond = self.cbool(s[1])
            ch.arms.append((cond, c, self.compile_arm(cl, s[2])))
            if s[3] is not None:
                ch.else_body = self.compile_arm(cl, s[3])
                ch.has_else = True
            return ch
        if k == "unless":
            ch = Chain(cl)
            inner = self.cbool(s[1])
            if 15 in ALT:
                def cond(rt, inner=inner):
                    return not inner(rt)
            else:
                def cond(rt, inner=inner):      # 'as If with not C': the not is counted (§11 item 15)
                    v = inner(rt)
                    rt.ops += 1
                    return not v
            ch.arms.append((cond, c, self.compile_arm(cl, s[2])))
            return ch
        if k == "while":
            n_max = s[2]
            if n_max < 1 or n_max > FUEL_MAX:           # §11 item 19
                self.refuse("FUEL", "bound %d" % n_max)
            cond = self.cbool(s[1])
            body = self.compile_block(cl.children)
            return self.x_while(c, cond, n_max, body)
        if k == "for":
            tlo, flo = self.cexpr(s[2])
            thi, fhi = self.cexpr(s[3])
            if tlo != "I" or thi != "I":
                self.refuse("TYPE", "For bounds must be Int")
            self.scopes.append({})
            var = self.declare(s[1], "I", counter=True)
            body = self.compile_block(cl.children)
            self.scopes.pop()
            return self.x_for(c, flo, fhi, var.vid, body)
        if k == "to":
            if len(cl.label) != 1:
                self.refuse("PROCEDURE-PLACE")
            name = s[1]
            if name in self.proc_defined:
                self.refuse("REDECLARED", "procedure '%s' defined twice" % name)
            if any(r.lower() == name for r in self.rule_defs):
                self.refuse("REDECLARED", "procedure '%s' names a rule" % name)
            # §5's rule ("a name that is visible") applied to the converse of §11 item 47: a
            # procedure may not take the lowercased name of a visible variable (twin reading)
            for sc in self.scopes:
                for vname in sc:
                    if vname.lower() == name:
                        self.refuse("REDECLARED", "procedure '%s' names a visible variable" % name)
            proc = Proc(name, cl)
            saved = self.scopes
            # a procedure body sees the top-level variables declared textually before it
            self.scopes = [dict(saved[0])]
            self.in_proc = cl
            proc.body = self.compile_block(cl.children)
            self.scopes = saved
            self.in_proc = None
            self.proc_defined[name] = proc
            return None
        if k == "define":
            self.compile_define(cl)
            return None
        if k == "decimals":
            if len(cl.label) != 1 or self.decimals_set or self.decimal_seen:      # §11 item 49
                self.refuse("DECIMALS-PLACE")
            self.decimals = s[1]
            self.decimals_set = True
            return None
        return self.compile_inline(cl, s)

    def compile_inline(self, cl, s):
        k = s[0]
        c = cl.id
        if k == "let":
            t, f = self.cexpr(s[2])
            var = self.declare(s[1], t)
            return self.x_assign(c, var.vid, t, f)
        if k == "set":
            var = self.lookup(s[1])
            if var.counter:
                self.refuse("LOOP-VARIABLE", s[1])
            t, f = self.cexpr(s[2])
            f = self.coerce(t, f, var.type)
            return self.x_assign(c, var.vid, var.type, f)
        if k == "setitem":
            ti, fi = self.cexpr(s[1])
            var = self.lookup(s[2])
            if var.counter:                             # §11 item 29: before the list type
                self.refuse("LOOP-VARIABLE", s[2])
            if not is_list(var.type):
                self.refuse("TYPE", "%s is not a list" % s[2])
            if ti != "I":
                self.refuse("TYPE", "an index must be Int")
            et = var.type[1]
            tv, fv = self.cexpr(s[3])
            fv = self.coerce(tv, fv, et)
            return self.x_setitem(c, var.vid, et, fi, fv)
        if k == "inc":
            var = self.lookup(s[2])
            if var.counter:
                self.refuse("LOOP-VARIABLE", s[2])
            if var.type not in NUMERIC:
                self.refuse("TYPE", "Increase/Decrease needs a number")
            t, f = self.cexpr(s[3])
            f = self.coerce(t, f, var.type)            # §11 item 55: the promotion counts inside 'evaluate E'
            fn = ARITH[var.type]["+" if s[1] > 0 else "-"]
            return self.x_inc(c, var.vid, var.type, f, fn)
        if k == "incitem":
            ti, fi = self.cexpr(s[2])
            var = self.lookup(s[3])
            if var.counter:                             # §11 item 29: before the list type
                self.refuse("LOOP-VARIABLE", s[3])
            if not is_list(var.type):
                self.refuse("TYPE", "%s is not a list" % s[3])
            if ti != "I":
                self.refuse("TYPE", "an index must be Int")
            et = var.type[1]
            if et not in NUMERIC:
                self.refuse("TYPE", "Increase/Decrease needs numbers")
            tv, fv = self.cexpr(s[4])
            fv = self.coerce(tv, fv, et)
            fn = ARITH[et]["+" if s[1] > 0 else "-"]
            return self.x_incitem(c, var.vid, et, fi, fv, fn)
        if k == "say":
            t, f = self.cexpr(s[1])
            return self.x_say(c, t, f)
        if k == "append":
            t, f = self.cexpr(s[1])
            var = self.lookup_list(s[2])
            et = var.type[1]
            f = self.coerce(t, f, et)
            return self.x_append(c, var.vid, et, f)
        if k == "remove":
            var = self.lookup_list(s[1])
            return self.x_remove(c, var.vid)
        if k == "perform":
            name = s[1]
            if name not in self.proc_names:
                self.refuse("UNKNOWN-PROCEDURE", name)
            proc = self.proc_defined.get(name)
            if proc is None:                            # §11 item 22 (also at top level)
                self.refuse("PERFORM-BEFORE-DEFINITION", name)
            return self.x_perform(proc)
        if k == "must":
            f = self.cbool(s[1])
            mid = self.n_musts
            self.n_musts += 1
            return self.x_must(c, mid, f)
        if k == "claim":
            f = self.cbool(s[1])
            cid = len(self.claim_clauses)
            self.claim_clauses.append(c)
            ref_clause = self.check_oracle(cl, s[2])
            for r in s[3]:
                tgt = self.label_map.get(r)
                if tgt is None:
                    self.refuse("UNKNOWN-CLAUSE", "given " + fmt_ref(r))
                if tgt.stmt[0] != "claim":                  # §11 item 32
                    self.refuse("PREMISE-TARGET", fmt_ref(r))
            return self.x_claim(c, cid, f, ref_clause)
        raise AssertionError(k)

    def target_ok(self, tgt, cl):
        """CERTIFICATE-TARGET (§11 item 30): an earlier clause, not a To, Define, Decimals or
        claim clause, and not absorbed; clauses inside procedure bodies are allowed."""
        if tgt.id >= cl.id:
            return False
        if tgt.stmt[0] in ("to", "define", "decimals", "claim", "otherwise", "otherwise_if"):
            return False
        return True

    def check_oracle(self, cl, oracle):
        k = oracle[0]
        if k == "certificate":
            tgt = self.label_map.get(oracle[1])
            if tgt is None:
                self.refuse("UNKNOWN-CLAUSE", "certificate of " + fmt_ref(oracle[1]))
            if not self.target_ok(tgt, cl):
                self.refuse("CERTIFICATE-TARGET", fmt_ref(oracle[1]))
            return tgt.id
        if k == "agreement":
            for r in oracle[1:3]:                   # §11 item 31: earlier clauses; ref 0 0
                tgt = self.label_map.get(r)
                if tgt is None:
                    self.refuse("UNKNOWN-CLAUSE", "agreement of " + fmt_ref(r))
                if tgt.id >= cl.id:
                    self.refuse("AGREEMENT-TARGET", fmt_ref(r))
            return 0
        return 0

    def compile_define(self, cl):
        s = cl.stmt
        name = s[2]                             # DEFINE-PLACE was phase 5
        if name.lower() in self.proc_names:
            self.refuse("REDECLARED", "rule %s names a procedure" % name)
        targets = set()
        for r in s[1]:
            tgt = self.label_map.get(r)
            if tgt is None:
                self.refuse("UNKNOWN-CLAUSE", "notwithstanding " + fmt_ref(r))       # §11 item 33
            if tgt.stmt[0] != "define" or tgt.stmt[2] != name:
                self.refuse("NOTWITHSTANDING-TARGET", fmt_ref(r))
            targets.add(tgt.id)
        tv, fv = self.cexpr(s[3])
        if is_list(tv):
            self.refuse("TYPE", "a rule is not a list")
        if name in self.rule_type and self.rule_type[name] != tv:      # §11 item 45
            self.refuse("TYPE", "the Define clauses of %s have different types" % name)
        self.rule_type[name] = tv
        provided = self.cbool(s[4]) if s[4] is not None else None
        unless = self.cbool(s[5]) if s[5] is not None else None
        proviso = make_proviso(provided, unless)          # §11 items 24, 25
        self.rule_compiled.setdefault(name, []).append(RuleDef(cl.id, targets, fv, proviso))
        # PRIORITY-CYCLE is phase 7 (phase_cycles), after the whole static walk

    # -- typing helpers
    def coerce(self, t, f, target):
        """A value stored into a variable, a list item or an append (SPEC §5 promotion)."""
        if t == target:
            return f
        if t == "I" and target in ("X", "F"):
            return promote(f, target)
        self.refuse("TYPE", "%s where %s is needed" % (tname(t), tname(target)))

    def cbool(self, e):
        t, f = self.cexpr(e)
        if t != "B":
            self.refuse("TYPE", "a condition must be Bool")
        return f

    def unify(self, ta, tb, fa, fb):
        if ta not in NUMERIC or tb not in NUMERIC:
            self.refuse("TYPE", "%s with %s" % (tname(ta), tname(tb)))
        if ta == tb:
            return ta, fa, fb
        if "X" in (ta, tb) and "F" in (ta, tb):
            self.refuse("TYPE", "Fix with Float")
        t = "X" if "X" in (ta, tb) else "F"
        if ta == "I":
            fa = promote(fa, t)
        if tb == "I":
            fb = promote(fb, t)
        return t, fa, fb

    # -- expressions
    def cexpr(self, e):
        k = e[0]
        if k == "num":
            return self.c_num(e[1])
        if k == "str":
            return "T", const(e[1])
        if k == "bool":
            return "B", const(e[1])
        if k == "seal":
            return "T", const(self.seal_bytes)
        if k == "var":
            name = e[1]
            v = self.find_var(name)
            if v is not None:
                vid = v.vid
                return v.type, (lambda rt: rt.vars[vid])
            if name in self.rule_defs:
                return self.c_rule(name)
            self.refuse("UNDECLARED", name)
        if k == "item":
            ti, fi = self.cexpr(e[1])
            var = self.lookup_list(e[2])
            if ti != "I":
                self.refuse("TYPE", "an index must be Int")
            vid = var.vid

            def item(rt):
                idx = fi(rt)
                rt.ops += 1
                lst = rt.vars[vid]
                if idx < 1 or idx > len(lst):
                    raise Refusal("INDEX-OUT-OF-RANGE")
                return lst[idx - 1]
            return var.type[1], item
        if k == "len":
            var = self.lookup_list(e[1])     # §11 item 44: lists only
            vid = var.vid

            def length(rt):
                rt.ops += 1
                return len(rt.vars[vid])
            return "I", length
        if k == "copies":
            tn, fn = self.cexpr(e[1])
            tv, fv = self.cexpr(e[2])
            if tn != "I":
                self.refuse("TYPE", "a count must be Int")
            if tv not in ELEM_TYPES:
                self.refuse("TYPE", "a list holds Int, Fix, Float or Bool")

            def copies(rt):
                n = fn(rt)
                v = fv(rt)
                rt.ops += 1
                if n < 0:
                    raise Refusal("NEGATIVE-LENGTH")
                if n > LIST_MAX:
                    raise Refusal("LIST-TOO-LONG")
                return [v] * n
            return "L" + tv, copies
        if k == "list":
            items = [self.cexpr(x) for x in e[1]]
            ts = set(t for t, _ in items)
            if not ts <= set(ELEM_TYPES):
                self.refuse("TYPE", "a list holds Int, Fix, Float or Bool")
            if "B" in ts:
                if ts != {"B"}:
                    self.refuse("TYPE", "a list mixes Bool with numbers")
                et = "B"
            elif "X" in ts and "F" in ts:
                self.refuse("TYPE", "Fix with Float")
            elif "X" in ts:
                et = "X"
            elif "F" in ts:
                et = "F"
            else:
                et = "I"
            fs = [promote(f, et) if (t == "I" and et != "I") else f for t, f in items]   # §11 item 42

            def lit(rt):
                vals = [f(rt) for f in fs]
                rt.ops += 1
                if len(vals) > LIST_MAX:
                    raise Refusal("LIST-TOO-LONG")
                return vals
            return "L" + et, lit
        if k in ("neg", "abs", "sqrt"):
            t, f = self.cexpr(e[1])
            if t not in NUMERIC:
                self.refuse("TYPE", "%s needs a number" % k)
            fn = ARITH[t][k]
            if k == "neg" and 36 in ALT and e[1][0] == "num":     # a negative literal, 0 ops
                return t, const(fn(f(None)))

            def un(rt):
                v = f(rt)
                rt.ops += 1
                return fn(v)
            return t, un
        if k == "intpart":
            t, f = self.cexpr(e[1])
            if t not in ("X", "F"):                       # §11 item 43
                self.refuse("TYPE", "integer part of takes Fix or Float")
            fn = NR.x_trunc if t == "X" else NR.f_trunc

            def ip(rt):
                v = f(rt)
                rt.ops += 1
                return fn(v)
            return "I", ip
        if k == "bin":
            op = e[1]
            ta, fa = self.cexpr(e[2])
            tb, fb = self.cexpr(e[3])
            if op == "mod":
                if ta != "I" or tb != "I":
                    self.refuse("TYPE", "remainder/modulo take Int only")
                t = "I"
            else:
                t, fa, fb = self.unify(ta, tb, fa, fb)
            fn = ARITH[t][op]
            return t, binop(fa, fb, fn)
        if k == "quot":
            ta, fa = self.cexpr(e[1])
            tb, fb = self.cexpr(e[2])
            if ta != "I" or tb != "I":
                self.refuse("TYPE", "quotient takes Int only")
            return "I", binop(fa, fb, NR.i_quot)
        if k in ("max", "min"):
            ta, fa = self.cexpr(e[1])
            tb, fb = self.cexpr(e[2])
            t, fa, fb = self.unify(ta, tb, fa, fb)
            return t, binop(fa, fb, ARITH[t][k])
        if k == "cmp":
            op = e[1]
            ta, fa = self.cexpr(e[2])
            tb, fb = self.cexpr(e[3])
            if op in ("=", "!=") and ta == tb and ta in ("B", "T"):
                pass
            else:
                _, fa, fb = self.unify(ta, tb, fa, fb)
            fn = CMP[op]
            return "B", binop(fa, fb, fn)
        if k == "pred":
            p = e[1]
            t, f = self.cexpr(e[2])
            if p in ("even", "odd"):
                if t != "I":
                    self.refuse("TYPE", "%s takes Int only" % p)
            elif t not in NUMERIC:
                self.refuse("TYPE", "%s takes a number" % p)
            fn = PRED[p]

            def pr(rt):
                v = f(rt)
                rt.ops += 1
                return fn(v)
            return "B", pr
        if k == "not":
            f = self.cbool(e[1])

            def neg(rt):
                v = f(rt)
                rt.ops += 1
                return not v
            return "B", neg
        if k in ("and", "or"):
            fa = self.cbool(e[1])
            fb = self.cbool(e[2])
            if 35 in ALT:                       # no short-circuit (§11 item 35, the other reading)
                is_and = k == "and"

                def both(rt):
                    a = fa(rt)
                    rt.ops += 1
                    b = fb(rt)
                    return (a and b) if is_and else (a or b)
                return "B", both
            if k == "and":
                def conj(rt):
                    a = fa(rt)
                    rt.ops += 1                 # counted after the left operand (§11 item 35)
                    if not a:
                        return False
                    return fb(rt)
                return "B", conj

            def disj(rt):
                a = fa(rt)
                rt.ops += 1
                if a:
                    return True
                return fb(rt)
            return "B", disj
        if k == "cat":
            parts = [self.cexpr(x) for x in e[1]]
            extra = len(parts) - 1

            def cat(rt):
                vals = [(t, f(rt)) for t, f in parts]
                rt.ops += extra
                out = bytearray()
                for t, v in vals:
                    piece = to_text(t, v)
                    if len(out) + len(piece) > TEXT_MAX:
                        raise Refusal("TEXT-TOO-LONG")
                    out += piece
                return bytes(out)
            return "T", cat
        if k == "conv":
            target, rounded = e[1], e[2]
            t, f = self.cexpr(e[3])
            fn = CONVERT.get((t, target, rounded))
            if fn is None:
                self.refuse("TYPE", "no conversion from %s to %s" % (tname(t), tname(target)))

            def cv(rt):
                v = f(rt)
                rt.ops += 1
                return fn(v)
            return target, cv
        raise AssertionError(k)

    def c_num(self, text):
        if "." in text:
            self.decimal_seen = True
            exact = Fraction(text)
            if self.decimals == "fixed":
                raw = NR.round_half_even(exact * ONE)
                if raw > I64_MAX:                               # §11 item 38
                    self.refuse("LITERAL-RANGE", text)
                return "X", const(raw)
            f = float(text)
            if f == float("inf"):                               # §11 item 38
                self.refuse("LITERAL-RANGE", text)
            return "F", const(f)
        v = int(text)
        if v > I64_MAX:
            self.refuse("LITERAL-RANGE", text)
        return "I", const(v)

    def c_rule(self, name):
        """A use of a rule (SPEC §5 Rules, §6)."""
        pos = self.in_proc.id if self.in_proc is not None else self.cur.id
        if any(d.id >= pos for d in self.rule_defs[name]):
            self.refuse("RULE-BEFORE-DEFINITION", name)
        t = self.rule_type[name]
        defs = list(self.rule_compiled[name])
        over = override_closure(defs)
        count_cmp = 1 if 52 in ALT else 0

        def use(rt):
            rt.ops += 1
            app = []
            for d in defs:
                if d.proviso is None or d.proviso(rt):       # every proviso, in clause order
                    app.append(d)
            rem = [d for d in app if not any((o is not d) and (d.cid in over[o.cid]) for o in app)]
            if not rem:
                raise Refusal("RULE-UNDEFINED")
            vals = [d.value(rt) for d in rem]               # all values before any comparison
            first = vals[0]
            for v in vals[1:]:
                rt.ops += count_cmp                         # 0: not counted (§11 item 52)
                if not values_equal(t, first, v):
                    raise Refusal("RULE-CONFLICT")
            return first
        return t, use

    # -- statement executors (SPEC §7 'Statements')
    def x_assign(self, c, vid, t, f):
        listy = is_list(t)

        def run(rt):
            rt.ops += 1
            try:
                v = f(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            if listy:
                v = list(v)
            rt.vars[vid] = v
            rt.event(b"A", c, u32(vid) + enc(t, v))
        return run

    def x_setitem(self, c, vid, et, fi, fv):
        base = 1 if 53 in ALT else 0           # §11 item 53: the event's index is k (or k-1)
        venc = (lambda t, v: slot(t, v)) if 54 in ALT else enc     # §11 item 54

        def run(rt):
            rt.ops += 1
            try:
                k = fi(rt)
                v = fv(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            lst = rt.vars[vid]
            if k < 1 or k > len(lst):
                raise Stop("INDEX-OUT-OF-RANGE", c)
            lst[k - 1] = v
            rt.event(b"E", c, u32(vid) + u64(k - base) + venc(et, v))      # §11 item 53: k as written, 1-based
        return run

    def x_inc(self, c, vid, t, f, fn):
        def run(rt):
            rt.ops += 1
            try:
                d = f(rt)
                rt.ops += 1
                nv = fn(rt.vars[vid], d)
            except Refusal as e:
                raise Stop(e.code, c)
            rt.vars[vid] = nv
            rt.event(b"A", c, u32(vid) + enc(t, nv))
        return run

    def x_incitem(self, c, vid, et, fi, fv, fn):
        base = 1 if 53 in ALT else 0
        venc = (lambda t, v: slot(t, v)) if 54 in ALT else enc

        def run(rt):
            rt.ops += 1
            try:
                k = fi(rt)
                rt.ops += 1
                lst = rt.vars[vid]
                if k < 1 or k > len(lst):
                    raise Refusal("INDEX-OUT-OF-RANGE")
                cur = lst[k - 1]
                d = fv(rt)
                rt.ops += 1
                nv = fn(cur, d)
            except Refusal as e:
                raise Stop(e.code, c)
            lst[k - 1] = nv
            rt.event(b"E", c, u32(vid) + u64(k - base) + venc(et, nv))
        return run

    def x_say(self, c, t, f):
        def run(rt):
            rt.ops += 1
            try:
                v = f(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            line = to_text(t, v)
            if len(line) > TEXT_MAX:
                raise Stop("TEXT-TOO-LONG", c)
            if len(rt.out) + len(line) + 1 > OUTPUT_MAX:
                raise Stop("OUTPUT-TOO-LONG", c)
            data = line + b"\n"
            rt.out += data
            rt.event(b"S", c, data)
        return run

    def x_while(self, c, cond, n_max, body):
        def run(rt):
            n = 0
            while True:
                rt.ops += 1
                try:
                    v = cond(rt)
                except Refusal as e:
                    raise Stop(e.code, c)
                if not v:
                    return
                if n == n_max:
                    raise Stop("FUEL-EXHAUSTED", c)
                n += 1
                for st in body:
                    st(rt)
        return run

    def x_for(self, c, flo, fhi, vid, body):
        def run(rt):
            rt.ops += 1
            try:
                lo = flo(rt)
                hi = fhi(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            k = lo
            while k <= hi:
                rt.ops += 1
                rt.vars[vid] = k
                rt.event(b"A", c, u32(vid) + enc("I", k))
                for st in body:
                    st(rt)
                if k == hi:
                    break
                k += 1
        return run

    def x_perform(self, proc):
        def run(rt):
            rt.ops += 1
            for st in proc.body:
                st(rt)
        return run

    def x_must(self, c, mid, f):
        def run(rt):
            rt.ops += 1
            try:
                v = f(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            rt.event(b"M", c, u32(mid) + (b"\x01" if v else b"\x00"))
            if not v:
                raise Stop("MUST-FAILED", c)
        return run

    def x_claim(self, c, cid, f, ref_clause):
        def run(rt):
            rt.ops += 1
            s0 = rt.ops
            try:
                v = f(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            cost = rt.ops - s0
            rt.event(b"C", c, u32(cid) + (b"\x01" if v else b"\x00"))
            acc = rt.claims[cid]
            acc[0] += 1
            acc[1] += 1 if v else 0
            acc[2] += cost
            if ref_clause:
                acc[3] = ref_clause
                acc[4] = rt.cost[ref_clause]
            else:
                acc[3] = 0
                acc[4] = 0
            if not v:
                raise Stop("CLAIM-REFUTED", c)
        return run

    def x_append(self, c, vid, et, f):
        def run(rt):
            rt.ops += 1
            try:
                v = f(rt)
            except Refusal as e:
                raise Stop(e.code, c)
            lst = rt.vars[vid]
            if len(lst) + 1 > LIST_MAX:
                raise Stop("LIST-TOO-LONG", c)
            lst.append(v)
            rt.event(b"P", c, u32(vid) + enc(et, v))
        return run

    def x_remove(self, c, vid):
        def run(rt):
            rt.ops += 1
            lst = rt.vars[vid]
            if not lst:
                raise Stop("EMPTY-LIST", c)
            lst.pop()
            rt.event(b"Q", c, u32(vid) + u64(len(lst)))
        return run


def promote(f, target):
    """An implicit promotion of an Int, counted right after its operand (§11 item 41, 42)."""
    fn = PROMOTE[target]

    def pr(rt):
        v = f(rt)
        rt.ops += 1
        return fn(v)
    return pr


def binop(fa, fb, fn):
    def b(rt):
        x = fa(rt)
        y = fb(rt)
        rt.ops += 1
        return fn(x, y)
    return b


CMP = {
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "=": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}

PRED = {
    "even": lambda v: v % 2 == 0,
    "odd": lambda v: v % 2 == 1,
    "zero": lambda v: v == 0,
    "positive": lambda v: v > 0,
    "negative": lambda v: v < 0,          # §11 item 50: by comparison, so -0.0 is not negative
}


def make_proviso(provided, unless):
    if provided is None and unless is None:
        return None
    if unless is None:
        return provided
    counted = 24 not in ALT
    if provided is None:
        def p_unless(rt):
            v = unless(rt)
            if counted:
                rt.ops += 1
            return not v
        return p_unless

    def p_both(rt):                       # 'provided that C1, unless C2' = C1 and not C2
        a = provided(rt)
        rt.ops += 1
        if not a:
            return False
        v = unless(rt)
        if counted:
            rt.ops += 1
        return not v
    return p_both


def override_closure(defs):
    direct = dict((d.cid, set(d.targets)) for d in defs)
    over = {}
    for d in defs:
        seen = set()
        stack = list(direct[d.cid])
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(direct.get(x, ()))
        over[d.cid] = seen
    return over


def fmt_ref(r):
    return "§" + ".".join(str(p) for p in r)


def tname(t):
    names = {"I": "Int", "X": "Fix", "F": "Float", "B": "Bool", "T": "Text"}
    if len(t) == 2:
        return "List of " + names[t[1]]
    return names[t]


# ---------------------------------------------------------------- the run (SPEC §7, RUNTIME-SPEC §5-§7)
class RT(object):
    def __init__(self, law_bytes, n_vars, n_claims, cert_ids, tracing):
        self.ops = 0
        self.vars = [None] * n_vars
        self.head = hashlib.sha256(b"orlog-trace-0" + law_bytes).digest()
        self.events = 0
        self.out = bytearray()
        self.claims = [[0, 0, 0, 0, 0] for _ in range(n_claims)]
        self.cost = dict((c, 0) for c in cert_ids)
        self.trace = [] if tracing else None

    def event(self, kind, clause, payload):
        h = hashlib.sha256()
        h.update(self.head)
        h.update(kind)
        h.update(struct.pack(">II", clause, len(payload)))
        h.update(payload)
        self.head = h.digest()
        self.events += 1
        if self.trace is not None:
            self.trace.append("%d %s %d %s %s\n" % (self.events, kind.decode("ascii"), clause,
                                                    payload.hex() if payload else "-", self.head.hex()))


def compile_text(text, law_hex):
    """Compile in §11 G3's phases: 1 the door (not done: the input is taken to be canonical),
    2 lines, 3 statement syntax, 4 shape, 5 DEFINE-PLACE, 6 static semantics, 7 PRIORITY-CYCLE,
    8 SEAL-MISMATCH. The first refusal in the first phase that has one is raised."""
    raws, sealed = phase_lines(text)                    # 2
    clauses = phase_syntax(raws)                        # 3
    words = SL.seal_words(law_hex)
    comp = Compiler(clauses, words)
    prog = comp.compile()                               # 4, 5, 6, 7
    if sealed is not None and sealed[1] != words:       # 8
        raise CompileRefusal("SEAL-MISMATCH", line=sealed[0], detail="Sealed %s, law seal words %s" % (sealed[1], words))
    prog.seal_words = words
    return prog


def execute(prog, law_hex, tracing=False):
    rt = RT(bytes.fromhex(law_hex), prog.n_vars, len(prog.claim_clauses), prog.cert_ids, tracing)
    try:
        for st in prog.body:
            st(rt)
        status = "COMPLETED"
    except Stop as s:
        rt.event(b"R", s.clause, s.code.encode("ascii"))
        status = "REFUSED %s %d" % (s.code, s.clause)
    return rt, status


def receipt_text(rt, status, prog, law_hex, text_hex):
    lines = [
        "orlog-receipt 0",
        "backend twin",
        "law-seal " + law_hex,
        "text-seal " + text_hex,
        "status " + status,
        "output-bytes %d" % len(rt.out),
        "output-sha256 " + hashlib.sha256(bytes(rt.out)).hexdigest(),
        "events %d" % rt.events,
        "trace-head " + rt.head.hex(),
        "ops %d" % rt.ops,
        "claims %d" % len(prog.claim_clauses),
    ]
    for i, c in enumerate(prog.claim_clauses):
        a = rt.claims[i]
        lines.append("claim %d %d %d %d %d %d %d" % (i, c, a[0], a[1], a[2], a[3], a[4]))
    lines.append("end")
    if 57 in ALT:
        return "\n".join(lines)
    return "\n".join(lines) + "\n"                    # §11 item 57: every line ends with LF


HEX64 = re.compile(r"^[0-9a-f]{64}$")


def main(argv):
    argv = list(argv)
    if len(argv) >= 3 and argv[1] == "--alt":
        try:
            alts = set(int(x) for x in argv[2].split(",") if x)
        except ValueError:
            alts = None
        if not alts or not alts <= set(ALT_READINGS):
            sys.stderr.write("twin: --alt takes item numbers among %s\n" % sorted(ALT_READINGS))
            return 2
        ALT.update(alts)
        del argv[1:3]
        for n in sorted(alts):
            sys.stderr.write("twin: alternative reading %d: %s\n" % (n, ALT_READINGS[n]))
    if len(argv) not in (6, 7):
        sys.stderr.write("usage: python twin.py [--alt N,N...] PROGRAM.orl LAW_SEAL TEXT_SEAL OUTPUT_PATH "
                         "RECEIPT_PATH [TRACE_PATH]\n")
        return 2
    prog_path, law_hex, text_hex, out_path, rec_path = argv[1:6]
    trace_path = argv[6] if len(argv) == 7 else None
    for name, h in (("LAW_SEAL", law_hex), ("TEXT_SEAL", text_hex)):
        if not HEX64.match(h):
            sys.stderr.write("twin: %s must be 64 lowercase hex digits\n" % name)
            return 2
    try:
        with open(prog_path, "rb") as fh:
            raw = fh.read()
    except OSError as e:
        sys.stderr.write("twin: cannot open %s: %s\n" % (prog_path, e))
        return 2
    if hashlib.sha256(raw).hexdigest() != text_hex:
        sys.stderr.write("twin: note: the given text seal is not the sha256 of %s (the given one is used)\n" % prog_path)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        sys.stderr.write("twin: compile refused: the program is not UTF-8\n")
        return 1
    try:
        prog = compile_text(text, law_hex)
    except CompileRefusal as e:
        where = []
        if e.clause is not None:
            where.append("clause %d" % e.clause)
        if e.line is not None:
            where.append("line %d" % e.line)
        sys.stderr.write("twin: compile refused %s %s%s\n" % (
            e.code, " ".join(where), (": " + e.detail) if e.detail else ""))
        return 1
    rt, status = execute(prog, law_hex, tracing=trace_path is not None)
    receipt = receipt_text(rt, status, prog, law_hex, text_hex)
    try:
        with open(out_path, "wb") as fh:
            fh.write(bytes(rt.out))
        with open(rec_path, "wb") as fh:
            fh.write(receipt.encode("ascii"))
        if trace_path is not None:
            with open(trace_path, "wb") as fh:
                fh.write("".join(rt.trace).encode("ascii"))
    except OSError as e:
        sys.stderr.write("twin: cannot write: %s\n" % e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

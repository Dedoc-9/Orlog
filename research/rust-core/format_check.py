"""RUST-CORE-0, phase 0: LAW-FORMAT-0's checker, amended to draft 9 (LAW-FORMAT-0-DRAFT-9.md section 11).

Draft 2's amendments (REREAD-1):
- W1 checked line by line, each line completely, the clause prefix byte by byte (G6, G7);
- W14(c) a lexical count of parentheses in phase 2 (G9);
- `\\u{0}` accepted (G3);
- a promote only with target fix or float (G4);
- no check needing a missing clause (G5);
- the line of relational failures, and no walk into a chain failing W5 or an inline statement failing W7 (G8).
Draft 3's (REREAD-2, the owner's rulings C1(a), C2(a) and his three qualifications):
- W14(a) and (b) computed from the parent links in one pass (H2);
- the W8 check on remove-last (H6); a clause named by two blocks fails on the later If's line (H7); no check of a
  promote's place when the other operand's type, or the slot's, is underived (H8).
Draft 4's (REREAD-3, the owner's rulings E1(b), E2 and E3(a)):
- W14(a) and (b) a gate: a law that fails them is refused before any walk, and the walk's cap is gone (E1, J1);
- a chain failing W4 refused before any walk, after the depth gate (E1, J7);
- Python's int-string limit lifted while a law is read, and put back after (J9);
- the overrides' closure by a search from each define, and sibling positions computed once (J10).
Draft 5's (REREAD-4, the owner's rulings F1(b) and F2(a)):
- W5 and W7 a third gate, the three gates one phase before the walk, their failures ranked by line, then W (F1; F8's
  rule); the walk then enters every clause, which a coverage check asserts, so G8's skips are gone (K1, K4, K5);
- W11 against procedure clauses by their statement, not by what the walk has met (K1).
Draft 6's (REREAD-5, the owner's rulings N1(a), N2(a) and N3):
- the depth gate first, then the chain and structure gates together (N1; E1(b)'s adopted text, which F1 did not
  supersede); the plants of the gates' precedence, two same-line ties, three structure failures behind an earlier walk
  failure, and W5's narrow reading of a block (N3) (L6, L7, L8).
Draft 7's (REREAD-6, the owner's rulings U1(a) and U2):
- W5's naming read as its row is written: a first arm that names an absorbed clause names it, in a sound chain as in a
  W4 chain (M3); N3's narrow reading planted for an inline if's else as for its blocks (M4);
- the write-back compared byte for byte on every law, and counted as it is printed (M10).
Draft 8's (REREAD-7, the owner's rulings A to F):
- the i-th declaration the walk meets has id i, for variables, claims and musts alike, a repeated one counted (E1, V2);
- a rule's type is its first define's value's wherever its use stands (derivation 17): the walk is made again with
  the types the last walk gave the first defines until they hold still (E2, V3);
- each part of W9 checked once its own inputs are derived (E2, V3);
- the plants of E1, E2 and V4's two readings.
Draft 9's (REREAD-8, the owner's rulings G, H and L3):
- a rule typed by its first define in clause order alone, and a first define that uses its own rule, directly or
  through other rules' first defines, typing none (G; ZA1, ZA2); a promote's own two parts made wherever it stands
  (G; ZA3); their six plants;
- W14(c) at 91, the candidate limit, with a text the front end writes at 91 among the fixture laws (H; ZA8).
It sets no limit on how deeply perform and rule uses chain (the owner's ruling B1).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/format_check.py

It is written from draft 9's sections 2-4 and 8, not from sema.py's writer or the decoders. It reads law bytes in
section 8's four phases:
1. W1, line by line;
2. W14(c)'s count, then W2, then W3, line by line;
3. the three gates, with no walk: depth (W14(a), (b)) first, its least line reported if it fails; then chains (W4 on
   every arm's, else's and block's clause) and structure (W5, W7) together, the least (line, W) reported; nothing
   walked if any gate fails;
4. the walk of the whole tree: W4's other references, W6 and W8-W13, every failure collected, the least (line, W).
It writes the bytes back and computes section 6's derivations.

On LAW-SUFFICIENCY's 298 laws and on the fixture laws of section 11:
- every law must pass and come back exactly;
- its derivations must equal the analysis's own (the analysis is read only to compare).
Each planted malformation must be refused on the line and by the W that section 8 chooses.

It is evidence for the format, not its authority (the owner, 2026-10-30), and it is outside the core author's reading
set (D1). Its parser recurses at most 91 deep (W14(c), checked first), and its walk at most 24 clauses deep (the
depth gate, in phase 3, comes before it). It runs at Python's default recursion limit."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
# no raised recursion limit (draft 3, H4). Python's default holds its parser (W14(c), 91) and its walk (24, after the
# depth gate), so it changes no other module's limit in its process.

NAT = re.compile(r"(?:0|[1-9][0-9]*)\Z")
HEX16 = re.compile(r"[0-9a-f]{16}\Z")
LABEL = re.compile(r"[1-9][0-9]*(?:\.[1-9][0-9]*)*\Z")
PREFIX = re.compile(r"\(clause (0|[1-9][0-9]*) (0|[1-9][0-9]*) ")    # draft 2, section 2: the prefix, byte by byte
TYPES = {"int", "fix", "float", "bool", "text", "list-int", "list-fix", "list-float", "list-bool"}
LIST_TYPES = {"list-int", "list-fix", "list-float", "list-bool"}
ELEMS = {"int", "fix", "float", "bool"}
NUMERIC = {"int", "fix", "float"}
ARITH = {"+", "-", "*", "/", "max", "min"}
ORDER = {"<", ">", "<=", ">="}
EQUAL = {"==", "!="}
BOOL, INT = {"bool"}, {"int"}
UN_RULES = {   # W9's rule for each unary form: (its operand's types, its result's), each part made on its own (E2)
    "not": (BOOL, BOOL), "even": (INT, BOOL), "odd": (INT, BOOL), "zero": (NUMERIC, BOOL),
    "positive": (NUMERIC, BOOL), "negative": (NUMERIC, BOOL), "neg": (NUMERIC, NUMERIC), "abs": (NUMERIC, NUMERIC),
    "sqrt": (NUMERIC, NUMERIC), "trunc": ({"fix", "float"}, INT)}
BINARY = ARITH | ORDER | EQUAL | {"quot", "rem", "and", "or"}
UNARY = {"neg", "abs", "sqrt", "not", "trunc", "even", "odd", "zero", "positive", "negative"}
CONV = {"as", "rounded", "promote"}
INLINE = {"let", "set", "change", "say", "perform", "must", "claim", "append", "remove-last"}
CONV_OK = {("as", "int"): {"fix", "float"}, ("as", "fix"): {"int", "float"}, ("as", "float"): {"int", "fix"},
           ("rounded", "int"): {"fix", "float"}, ("rounded", "fix"): {"int", "float"},
           ("rounded", "float"): {"int", "fix"}}
I64_MAX = (1 << 63) - 1
DEPTH_CLAUSE, DEPTH_LOOP, DEPTH_PARENS = 24, 16, 91      # W14 (a), (b), (c): (c) lexical, in phase 2 (draft 2); 91 by
# draft 9, his H: the candidate limit, the deepest line the front end is known to write


def paren_depth(line):
    """The deepest nesting of parentheses outside strings in a line (W14(c), counted before the line is parsed)."""
    depth = deepest = 0
    in_str = False
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "(":
            depth += 1
            deepest = max(deepest, depth)
        elif ch == ")":
            depth -= 1
        i += 1
    return deepest


UNDERIVED = object()    # a promote's place that needs a type an earlier failure left underived (draft 3, H8)


def place(t, derived):
    """The target a promote may have at a place beside or into type t (W9's three places): t when it is fix or float,
    None where no promote may stand, UNDERIVED when the type the place needs is underived (the check is not made)."""
    if not derived:
        return UNDERIVED
    return t if t in ("fix", "float") else None


def rules_in(e):
    """The rule names an expression mentions, found by an explicit stack and no types (draft 9, G)."""
    out, stack = set(), [e]
    while stack:
        x = stack.pop()
        if x["k"] == "rule":
            out.add(x["name"])
        for v in x.values():
            if isinstance(v, dict) and "k" in v:
                stack.append(v)
            elif isinstance(v, list):
                stack.extend(y for y in v if isinstance(y, dict) and "k" in y)
    return out


class Refused(Exception):
    def __init__(self, w, why, line=0):
        Exception.__init__(self, "W%d line %d: %s" % (w, line, why))
        self.w, self.why, self.line = w, why, line


def need(ok, w, why, line=0):
    if not ok:
        raise Refused(w, why, line)


class Str:
    __slots__ = ("value", "raw")

    def __init__(self, value, raw):
        self.value, self.raw = value, raw


# ------------------------------------------------------------------ section 3: atoms
ESC = re.compile(r"u\{([0-9a-f]{1,6})\}")


def lex(line):
    out, i, n = [], 0, len(line)
    while i < n:
        ch = line[i]
        if ch == " ":
            i += 1
        elif ch in "()":
            out.append(ch)
            i += 1
        elif ch == '"':
            start = i
            i += 1
            buf = []
            while True:
                need(i < n, 2, "a string with no end")
                ch = line[i]
                if ch == '"':
                    i += 1
                    break
                if ch == "\\":
                    nxt = line[i + 1:i + 2]
                    if nxt in ('"', "\\"):
                        buf.append(nxt)
                        i += 2
                        continue
                    m = ESC.match(line, i + 1)
                    need(m is not None, 2, "an escape that is not \\\", \\\\ or \\u{h} with 1 to 6 lowercase hex digits")
                    need(not (len(m.group(1)) > 1 and m.group(1).startswith("0")), 2, "a \\u{h} with a leading zero")
                    cp = int(m.group(1), 16)
                    need(cp <= 0x10FFFF and not (0xD800 <= cp <= 0xDFFF), 2, "a \\u{h} that is not a scalar value")
                    buf.append(chr(cp))
                    i = m.end()
                else:
                    buf.append(ch)
                    i += 1
            out.append(Str("".join(buf), line[start:i]))
        else:
            j = i
            while j < n and line[j] not in ' ()"':
                j += 1
            out.append(line[i:j])
            i = j
    return out


def forms(toks):
    stack = [[]]
    for t in toks:
        if t == "(":
            stack.append([])
        elif t == ")":
            need(len(stack) > 1, 2, "a ')' with no '('")
            x = stack.pop()
            stack[-1].append(x)
        else:
            stack[-1].append(t)
    need(len(stack) == 1 and len(stack[0]) == 1 and isinstance(stack[0][0], list), 2, "not one form")
    return stack[0][0]


def nat(x):
    need(isinstance(x, str) and NAT.match(x) is not None, 2, "not a canonical natural number: %r" % (x,))
    return int(x)


def word(x, allowed=None):
    need(isinstance(x, str), 2, "a word expected")
    if allowed is not None:
        need(x in allowed, 2, "the word %r is not one of the form's" % x)
    return x


def text(x):
    need(isinstance(x, Str), 2, "a string expected")
    need(q(x.value) == x.raw, 2, "a string not written in its canonical escapes")
    return x.value


def label(x):
    need(isinstance(x, str) and LABEL.match(x) is not None, 2, "not a canonical label: %r" % (x,))
    return x


def q(s):
    out = []
    for ch in s:
        if ch in '"\\':
            out.append("\\" + ch)
        elif 0x20 <= ord(ch) <= 0x7E:
            out.append(ch)
        else:
            out.append("\\u{%x}" % ord(ch))
    return '"' + "".join(out) + '"'


# ------------------------------------------------------------------ section 4: forms (parse to a tree, and write it)
def expr(f):
    need(isinstance(f, list) and f and isinstance(f[0], str), 2, "an expression form expected")
    h = f[0]
    if h == "lit":
        need(len(f) == 3, 2, "lit takes a type and a value")
        t = word(f[1], {"int", "fix", "float", "bool"})
        if t == "float":
            need(isinstance(f[2], str) and HEX16.match(f[2]) is not None, 2, "a float literal is 16 lowercase hex")
            return {"k": "lit", "t": t, "v": int(f[2], 16)}
        if t == "bool":
            return {"k": "lit", "t": t, "v": int(word(f[2], {"0", "1"}))}
        return {"k": "lit", "t": t, "v": nat(f[2])}
    if h == "str":
        need(len(f) == 2, 2, "str takes a string")
        return {"k": "str", "v": text(f[1])}
    if h == "seal":
        need(len(f) == 1, 2, "seal takes nothing")
        return {"k": "seal"}
    if h == "var":
        need(len(f) == 2, 2, "var takes an id")
        return {"k": "var", "V": nat(f[1])}
    if h == "rule":
        need(len(f) == 2, 2, "rule takes a name")
        return {"k": "rule", "name": text(f[1])}
    if h in CONV:
        need(len(f) == 3, 2, "a conversion takes a target and an operand")
        return {"k": "conv", "mode": h, "target": word(f[1], {"int", "fix", "float"}), "a": expr(f[2])}
    if h in BINARY and len(f) == 4:
        return {"k": "bin", "op": h, "t": word(f[1], TYPES), "a": expr(f[2]), "b": expr(f[3])}
    if h in UNARY and len(f) == 3:
        return {"k": "un", "op": h, "t": word(f[1], TYPES), "a": expr(f[2])}
    if h == "cat":
        need(len(f) >= 3, 2, "cat takes two parts or more")
        return {"k": "cat", "parts": [expr(p) for p in f[1:]]}
    if h == "item":
        need(len(f) == 3, 2, "item takes a variable and an index")
        return {"k": "item", "V": nat(f[1]), "i": expr(f[2])}
    if h == "length":
        need(len(f) == 2, 2, "length takes a variable")
        return {"k": "length", "V": nat(f[1])}
    if h == "list-of":
        need(len(f) == 3, 2, "list-of takes a count and a value")
        return {"k": "list-of", "n": expr(f[1]), "v": expr(f[2])}
    if h == "list":
        need(len(f) >= 3, 2, "list takes a list type and one item or more")
        return {"k": "list", "t": word(f[1], LIST_TYPES), "items": [expr(x) for x in f[2:]]}
    raise Refused(2, "an expression headed %r" % h)


def opt(f):
    return None if f == "-" else expr(f)


def stmt(f):
    need(isinstance(f, list) and f and isinstance(f[0], str), 2, "a statement form expected")
    h, n = f[0], len(f)
    if h == "let":
        need(n == 4, 2, "let")
        return {"k": "let", "V": nat(f[1]), "name": text(f[2]), "e": expr(f[3])}
    if h == "set":
        need(n == 4, 2, "set")
        return {"k": "set", "V": nat(f[1]), "i": opt(f[2]), "e": expr(f[3])}
    if h == "change":
        need(n == 5, 2, "change")
        return {"k": "change", "sign": word(f[1], {"+", "-"}), "V": nat(f[2]), "i": opt(f[3]), "e": expr(f[4])}
    if h == "say":
        need(n == 2, 2, "say")
        return {"k": "say", "e": expr(f[1])}
    if h == "if":
        need(n >= 3, 2, "if takes one arm or more and an else")
        arms = []
        for a in f[1:-1]:
            need(isinstance(a, list) and len(a) == 4 and a[0] == "arm", 2, "an if's part that is not an arm")
            arms.append({"C": nat(a[1]), "cond": expr(a[2]), "body": body(a[3])})
        last = f[-1]
        if last == "-":
            els = None
        else:
            need(isinstance(last, list) and len(last) == 3 and last[0] == "else", 2, "an if's last part")
            els = {"C": nat(last[1]), "body": body(last[2])}
        return {"k": "if", "arms": arms, "els": els}
    if h == "while":
        need(n == 3, 2, "while")
        return {"k": "while", "fuel": nat(f[1]), "cond": expr(f[2])}
    if h == "for":
        need(n == 4, 2, "for")
        return {"k": "for", "V": nat(f[1]), "lo": expr(f[2]), "hi": expr(f[3])}
    if h == "procedure":
        need(n == 2, 2, "procedure")
        return {"k": "procedure", "name": text(f[1])}
    if h == "perform":
        need(n == 2, 2, "perform")
        return {"k": "perform", "C": nat(f[1])}
    if h == "must":
        need(n == 3, 2, "must")
        return {"k": "must", "M": nat(f[1]), "cond": expr(f[2])}
    if h == "claim":
        need(n == 5, 2, "claim")
        o = f[3]
        need(isinstance(o, list) and o and isinstance(o[0], str), 2, "an oracle form expected")
        if o[0] == "certificate":
            need(len(o) in (2, 3), 2, "certificate")
            oracle = {"k": "certificate", "C": nat(o[1]), "theorem": text(o[2]) if len(o) == 3 else None}
        elif o[0] == "theorem":
            need(len(o) == 2, 2, "theorem")
            oracle = {"k": "theorem", "name": text(o[1])}
        elif o[0] == "agreement":
            need(len(o) == 3, 2, "agreement takes two labels")
            oracle = {"k": "agreement", "labels": [label(o[1]), label(o[2])]}
        else:
            need(len(o) == 1 and o[0] in ("computation", "owner"), 2, "an oracle headed %r" % o[0])
            oracle = {"k": o[0]}
        g = f[4]
        need(isinstance(g, list) and g and g[0] == "given", 2, "a claim's given part")
        return {"k": "claim", "K": nat(f[1]), "cond": expr(f[2]), "oracle": oracle, "given": [label(x) for x in g[1:]]}
    if h == "define":
        need(n == 5, 2, "define")
        o = f[4]
        need(isinstance(o, list) and o and o[0] == "over", 2, "a define's over part")
        return {"k": "define", "name": text(f[1]), "e": expr(f[2]), "proviso": opt(f[3]), "over": [nat(x) for x in o[1:]]}
    if h == "append":
        need(n == 3, 2, "append")
        return {"k": "append", "V": nat(f[1]), "e": expr(f[2])}
    if h == "remove-last":
        need(n == 2, 2, "remove-last")
        return {"k": "remove-last", "V": nat(f[1])}
    if h == "decimals":
        need(n == 2, 2, "decimals")
        return {"k": "decimals", "mode": word(f[1], {"fixed", "floats"})}
    raise Refused(2, "a statement headed %r" % h)


def body(f):
    if isinstance(f, list) and f and f[0] == "block":
        need(len(f) == 2, 2, "block takes a clause")
        return {"k": "block", "C": nat(f[1])}
    return stmt(f)


def w_expr(e):
    k = e["k"]
    if k == "lit":
        v = "%016x" % e["v"] if e["t"] == "float" else str(e["v"])
        return "(lit %s %s)" % (e["t"], v)
    if k == "str":
        return "(str %s)" % q(e["v"])
    if k == "seal":
        return "(seal)"
    if k == "var":
        return "(var %d)" % e["V"]
    if k == "rule":
        return "(rule %s)" % q(e["name"])
    if k == "conv":
        return "(%s %s %s)" % (e["mode"], e["target"], w_expr(e["a"]))
    if k == "bin":
        return "(%s %s %s %s)" % (e["op"], e["t"], w_expr(e["a"]), w_expr(e["b"]))
    if k == "un":
        return "(%s %s %s)" % (e["op"], e["t"], w_expr(e["a"]))
    if k == "cat":
        return "(cat %s)" % " ".join(w_expr(p) for p in e["parts"])
    if k == "item":
        return "(item %d %s)" % (e["V"], w_expr(e["i"]))
    if k == "length":
        return "(length %d)" % e["V"]
    if k == "list-of":
        return "(list-of %s %s)" % (w_expr(e["n"]), w_expr(e["v"]))
    return "(list %s %s)" % (e["t"], " ".join(w_expr(x) for x in e["items"]))


def w_opt(e):
    return "-" if e is None else w_expr(e)


def w_body(b):
    return "(block %d)" % b["C"] if b["k"] == "block" else w_stmt(b)


def w_stmt(s):
    k = s["k"]
    if k == "let":
        return "(let %d %s %s)" % (s["V"], q(s["name"]), w_expr(s["e"]))
    if k == "set":
        return "(set %d %s %s)" % (s["V"], w_opt(s["i"]), w_expr(s["e"]))
    if k == "change":
        return "(change %s %d %s %s)" % (s["sign"], s["V"], w_opt(s["i"]), w_expr(s["e"]))
    if k == "say":
        return "(say %s)" % w_expr(s["e"])
    if k == "if":
        arms = " ".join("(arm %d %s %s)" % (a["C"], w_expr(a["cond"]), w_body(a["body"])) for a in s["arms"])
        els = "-" if s["els"] is None else "(else %d %s)" % (s["els"]["C"], w_body(s["els"]["body"]))
        return "(if %s %s)" % (arms, els)
    if k == "while":
        return "(while %d %s)" % (s["fuel"], w_expr(s["cond"]))
    if k == "for":
        return "(for %d %s %s)" % (s["V"], w_expr(s["lo"]), w_expr(s["hi"]))
    if k == "procedure":
        return "(procedure %s)" % q(s["name"])
    if k == "perform":
        return "(perform %d)" % s["C"]
    if k == "must":
        return "(must %d %s)" % (s["M"], w_expr(s["cond"]))
    if k == "claim":
        o = s["oracle"]
        if o["k"] == "certificate":
            orc = "(certificate %d%s)" % (o["C"], "" if o["theorem"] is None else " " + q(o["theorem"]))
        elif o["k"] == "theorem":
            orc = "(theorem %s)" % q(o["name"])
        elif o["k"] == "agreement":
            orc = "(agreement %s)" % " ".join(o["labels"])
        else:
            orc = "(%s)" % o["k"]
        return "(claim %d %s %s (given %s))" % (s["K"], w_expr(s["cond"]), orc, " ".join(s["given"]))
    if k == "define":
        return "(define %s %s %s (over %s))" % (q(s["name"]), w_expr(s["e"]), w_opt(s["proviso"]),
                                                " ".join(str(c) for c in s["over"]))
    if k == "append":
        return "(append %d %s)" % (s["V"], w_expr(s["e"]))
    if k == "remove-last":
        return "(remove-last %d)" % s["V"]
    return "(decimals %s)" % s["mode"]


# ------------------------------------------------------------------ section 8: the three phases
class Law:
    pass


def read(law):
    """The law bytes -> a Law with its derivations, or Refused carrying section 8's (line, W).

    An <n> may have any length (section 3), so Python's limit on the digits int() converts is lifted while the law is
    read, and put back after, so that nothing else in this process runs without it (draft 4, J9)."""
    old = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    try:
        return _read(law)
    finally:
        sys.set_int_max_str_digits(old)


def _read(law):
    need(isinstance(law, bytes), 1, "not bytes", 1)
    chunks = law.split(b"\n")
    if chunks[-1] == b"":
        chunks, unterminated = chunks[:-1], False
    else:
        unterminated = True                     # the last line has no LF
    # phase 1: W1, line by line from the start, each line checked completely before the next (draft 2, G6)
    L = Law()
    L.clauses = {}
    L.mode = None
    for i, ch in enumerate(chunks, 1):
        need(all(0x20 <= b <= 0x7E for b in ch), 1, "a byte outside 0x20-0x7E and LF", i)
        ln = ch.decode("ascii")
        if i == 1:
            need(ln == "orlog-law 0", 1, "line 1 is not orlog-law 0", 1)
        elif i == 2:
            need(ln in ("(decimals fixed)", "(decimals floats)"), 1, "line 2 is not the decimals line", 2)
            L.mode = ln[len("(decimals "):-1]
        else:
            k = i - 2
            m = PREFIX.match(ln)                # the prefix, byte by byte (draft 2, G7)
            need(m is not None, 1, "the clause line's prefix is not (clause n n ", i)
            need(ln.endswith(")") and len(ln) > m.end(), 1, "the clause line does not end with its )", i)
            need(int(m.group(1)) == k, 1, "clause line %d is numbered %s" % (k, m.group(1)), i)
            p = int(m.group(2))
            allowed = p == 0 or p == k - 1
            a = L.clauses[k - 1]["parent"] if k > 1 else 0
            while not allowed and a:
                allowed = a == p
                a = L.clauses[a]["parent"]
            need(allowed, 1, "clause %d's parent %d is not 0, %d or an ancestor of %d" % (k, p, k - 1, k - 1), i)
            L.clauses[k] = {"id": k, "parent": p, "rest": ln[m.end():-1], "children": [], "line": ln}
        need(not (unterminated and i == len(chunks)), 1, "no final LF", i)
    need(len(chunks) >= 1, 1, "line 1 is not orlog-law 0", 1)
    need(len(chunks) >= 2, 1, "line 2 is not the decimals line", 2)
    L.n = len(L.clauses)
    # phase 2: line by line, W14(c)'s lexical count, then W2, then W3 (draft 2, G9)
    for k in range(1, L.n + 1):
        c = L.clauses[k]
        need(paren_depth(c["line"]) <= DEPTH_PARENS, 14, "parentheses nested deeper than %d" % DEPTH_PARENS, k + 2)
        rest = c["rest"]
        c["absorbed"] = rest.strip(" ") == "absorbed"
        try:
            c["stmt"] = None if c["absorbed"] else stmt(forms(lex(rest)))
        except Refused as r:
            raise Refused(r.w, r.why, k + 2)
        written = "absorbed" if c["absorbed"] else w_stmt(c["stmt"])
        need(written == rest, 3, "the spacing is not section 1's", k + 2)
    # phases 3 and 4: the three gates, then the walk of the whole tree, every failure of each collected
    derive(L)
    if L.failures:
        line, w, why = min(L.failures)
        raise Refused(w, why, line)
    labels(L)
    return L


def labels(L):
    """Derivation "Labels" for a law that passed: each clause's outline number, and the clause of each. Made only here,
    where W14(a) holds, so a label has at most 24 parts (draft 3, H2)."""
    C = L.clauses
    L.label = {}
    for i, k in enumerate(L.top, 1):
        L.label[k] = str(i)
    for k in range(1, L.n + 1):
        for i, ch in enumerate(C[k]["children"], 1):
            L.label[ch] = L.label[k] + "." + str(i)
    L.by_label = {v: k for k, v in L.label.items()}


def write(L):
    out = ["orlog-law 0", "(decimals %s)" % L.mode]
    for k in range(1, L.n + 1):
        c = L.clauses[k]
        out.append("(clause %d %d %s)" % (k, c["parent"], "absorbed" if c["absorbed"] else w_stmt(c["stmt"])))
    return ("\n".join(out) + "\n").encode("ascii")


def derive(L):
    C = L.clauses
    fails = L.failures = []

    def fail(line, w, why):
        fails.append((line, w, why))

    L.top = [k for k in range(1, L.n + 1) if C[k]["parent"] == 0]
    for k in range(1, L.n + 1):
        if C[k]["parent"]:
            C[C[k]["parent"]]["children"].append(k)
    # phase 3, the three gates (draft 5, F1; their precedence draft 6, N1): depth, chains, structure. Each is computed
    # from the parsed lines and the parent links, with no walk and no recursion over the tree. The depth gate comes
    # first: if it fails, the least such line is reported as W14 and no W4-W13 check is made (E1(b), confirmed in N1).
    # Then the chain and structure gates' failures are collected together, and the least (line, W) is reported. A law
    # that fails any gate is refused, and no part of its tree is walked.
    # gate 1, depth: W14 (a) and (b), in one pass. A parent always comes before its child, so each clause's values are
    # known when its children are reached.
    depth, loops_to = {0: 0}, {0: 0}    # loops_to[a]: while and for clauses among a and its ancestors below the
    for k in range(1, L.n + 1):         # nearest procedure (0 for a procedure itself)
        p, s = C[k]["parent"], C[k]["stmt"]
        depth[k] = depth[p] + 1
        if depth[k] > DEPTH_CLAUSE:
            fail(k + 2, 14, "a clause %d deep" % depth[k])
        is_loop = s is not None and s["k"] in ("while", "for")
        is_proc = s is not None and s["k"] == "procedure"
        loops_to[k] = 0 if is_proc else loops_to[p] + (1 if is_loop else 0)
        if is_loop and loops_to[k] > DEPTH_LOOP:
            fail(k + 2, 14, "loops nested %d deep" % loops_to[k])
    if fails:                       # the depth gate first (E1(b), confirmed in N1): no W4-W13 check is made
        return
    pos = {}                            # each clause's place among its siblings, computed once (draft 4, J10)
    for sibs in [L.top] + [C[k]["children"] for k in range(1, L.n + 1)]:
        for i, j in enumerate(sibs):
            pos[j] = i

    def labelled(x):
        """The clause whose outline number is x, or None. Found by walking from the top, so that no table of every
        label is built here: a table's labels grow with the tree's depth, and its size with depth squared (draft 3,
        H2). The table itself is made only for a law that passes (labels(L))."""
        ks, k = L.top, None
        for part in x.split("."):
            i = int(part)
            if i > len(ks):
                return None
            k = ks[i - 1]
            ks = C[k]["children"]
        return k

    def ancestor(a, k):
        while k:
            if k == a:
                return True
            k = C[k]["parent"]
        return a == 0

    def sibling_or_below(d, u):      # u is a later sibling of d, or a descendant of one
        p = C[d]["parent"]
        while u and C[u]["parent"] != p:
            u = C[u]["parent"]
        return bool(u) and u > d

    def proc_of(k):
        a = C[k]["parent"]
        while a:
            if C[a]["stmt"] is not None and C[a]["stmt"]["k"] == "procedure":
                return a
            a = C[a]["parent"]
        return 0

    # W4: references
    def statements_of(k):
        out = []

        def go(s, ctx, inline):
            out.append((s, ctx, inline))
            if s["k"] == "if":
                for a in s["arms"]:
                    if a["body"]["k"] != "block":
                        go(a["body"], a["C"], True)
                if s["els"] is not None and s["els"]["body"]["k"] != "block":
                    go(s["els"]["body"], s["els"]["C"], True)
        if C[k]["stmt"] is not None:
            go(C[k]["stmt"], k, False)
        return out
    # gate 2, chains (draft 4, E1, J7): the clause of every arm, every else and every block, in every If form, inline
    # ones included, exists (W4)
    bad_ref = set()                 # clauses whose own If statement names a missing clause: its shape is not checked
    for k in range(1, L.n + 1):
        for s, ctx, inline in statements_of(k):
            if s["k"] == "if":
                refs = [a["C"] for a in s["arms"]] + [a["body"]["C"] for a in s["arms"] if a["body"]["k"] == "block"]
                if s["els"] is not None:
                    refs.append(s["els"]["C"])
                    if s["els"]["body"]["k"] == "block":
                        refs.append(s["els"]["body"]["C"])
                for r in refs:
                    if r not in C:
                        fail(k + 2, 4, "an If chain names clause %d, which does not exist" % r)
                        if not inline:
                            bad_ref.add(k)
    # gate 3, structure (draft 5, F1): W7, an inline body is a form section 4 marks inline, in every If form
    for k in range(1, L.n + 1):
        for s, ctx, inline in statements_of(k):
            if inline and s["k"] not in INLINE:
                fail(k + 2, 7, "%s inline" % s["k"])
    # gate 3, structure: W5, bodies and If chains, over the Ifs that are clause statements. A chain that names a missing
    # clause has its shape checks not made (each needs that clause); the clauses it does name are still recorded, so
    # that none of them reads as in no chain, and none as having children and no body.
    blocks, chain_of = [], {}
    for k in range(1, L.n + 1):
        s = C[k]["stmt"]
        if s is None or s["k"] != "if":
            continue
        line = k + 2
        parts = s["arms"] + ([s["els"]] if s["els"] is not None else [])
        if k in bad_ref:
            for part in parts:
                if part["body"]["k"] == "block" and part["body"]["C"] in C:
                    blocks.append((part["body"]["C"], k))
                if part["C"] != k and part["C"] in C and C[part["C"]]["absorbed"]:
                    chain_of.setdefault(part["C"], k)
            continue
        ok = True
        first = s["arms"][0]["C"]
        if first != k:
            fail(line, 5, "an If's first arm is not its own clause")
            ok = False
            # draft 7, M3: W5's row as written, "named by exactly one arm or else": a first arm that names an absorbed
            # clause names it, here as in a chain that names a missing clause, so that clause is not also in no chain
            if C[first]["absorbed"]:
                if first in chain_of:
                    fail(line, 5, "absorbed clause %d is named twice" % first)
                else:
                    chain_of[first] = k
        later = [a["C"] for a in s["arms"][1:]]
        if s["els"] is not None and s["els"]["C"] == k:
            if not (len(s["arms"]) == 1 and s["arms"][0]["body"]["k"] != "block" and s["els"]["body"]["k"] != "block"):
                fail(line, 5, "an otherwise in the If's own line needs one inline arm and an inline body")
                ok = False
        elif s["els"] is not None:
            later.append(s["els"]["C"])
        for a in later:
            if not C[a]["absorbed"]:
                fail(line, 5, "clause %d in the chain is not an absorbed clause" % a)
                ok = False
            elif a in chain_of:
                fail(line, 5, "absorbed clause %d is named twice" % a)
                ok = False
            else:
                chain_of[a] = k
        sibs = L.top if C[k]["parent"] == 0 else C[C[k]["parent"]]["children"]
        at = pos[k]
        if ok and sibs[at:at + 1 + len(later)] != [k] + later:
            fail(line, 5, "the chain's absorbed clauses are not the siblings right after it, in order")
        for part in parts:
            if part["body"]["k"] == "block":
                if part["body"]["C"] != part["C"]:
                    fail(line, 5, "a block names another clause than its arm's or else's own")
                blocks.append((part["body"]["C"], k))
    counted = {}                    # each clause a block names: the Ifs naming it, in clause order
    for b, by in blocks:
        counted.setdefault(b, []).append(by)
    for k in range(1, L.n + 1):
        line = k + 2
        if len(counted.get(k, ())) > 1:
            # draft 3, H7: one named by two Ifs fails on the later If's line (the second to name it)
            fail(counted[k][1] + 2, 5, "clause %d is named by two blocks" % k)
        if C[k]["absorbed"] and k not in chain_of:
            fail(line, 5, "absorbed clause %d is in no If chain" % k)
        s = C[k]["stmt"]
        owner = (s is not None and s["k"] in ("while", "for", "procedure")) or k in counted
        if bool(C[k]["children"]) != owner:
            fail(line, 5, "clause %d %s" % (k, "has children and no body" if C[k]["children"] else "has a body and no children"))
    if fails:
        return
    # phase 4: every gate has passed. W4's other references, in a clause's statement and in inline statements alike
    for k in range(1, L.n + 1):
        line = k + 2
        for s, ctx, inline in statements_of(k):
            refs = []
            if s["k"] == "perform":
                refs.append(s["C"])
            elif s["k"] == "define":
                refs += s["over"]
            elif s["k"] == "claim":
                if s["oracle"]["k"] == "certificate":
                    refs.append(s["oracle"]["C"])
                for x in s["given"] + (s["oracle"]["labels"] if s["oracle"]["k"] == "agreement" else []):
                    if labelled(x) is None:
                        fail(line, 4, "the label %s names no clause" % x)
            for r in refs:
                if r not in C:
                    fail(line, 4, "clause %d does not exist" % r)
    # the walk (section 7), with W6, W8-W13 on every statement. The gates have passed, so it is at most 24 clauses deep,
    # every clause an If chain or a block names exists, and it enters every clause: none is skipped (draft 5, F1)
    L.vars, L.var, L.rules, L.rule_types, L.claims, L.musts, L.cost, L.procs = [], {}, {}, {}, {}, {}, set(), {}
    walked = {}                     # each clause: how many times the walk reached it (the coverage check, below)
    for k in range(1, L.n + 1):
        s = C[k]["stmt"]
        if s is not None and s["k"] == "define":
            L.rules.setdefault(s["name"], []).append(k)
    last_define = {name: max(cls) for name, cls in L.rules.items()}    # computed once (draft 4, J10)
    # draft 9, G (ZA2): a rule whose first define's value uses that same rule, directly or through other rules' first
    # defines, has no type (derivation 17), whatever the value's form gives it. Found from the mentions alone, by a
    # search from each rule
    first_define = {name: cls[0] for name, cls in L.rules.items()}
    mentions = {name: rules_in(C[c]["stmt"]["e"]) for name, c in first_define.items()}
    self_using = set()
    for name, direct in mentions.items():
        seen, stack = set(), list(direct)
        while stack:
            x = stack.pop()
            if x == name:
                self_using.add(name)
                break
            if x not in seen and x in mentions:
                seen.add(x)
                stack.extend(mentions[x])
    decimals_at = [k for k in range(1, L.n + 1) if C[k]["stmt"] is not None and C[k]["stmt"]["k"] == "decimals"]
    if L.mode != (C[decimals_at[0]]["stmt"]["mode"] if decimals_at else "fixed"):
        # draft 2, G8: against a decimals clause, the later line (that clause's); with none, line 2
        fail(decimals_at[0] + 2 if decimals_at else 2, 6, "line 2's mode is not the law's")
    for k in decimals_at[1:]:
        fail(k + 2, 6, "a second decimals clause")
    dec_type = "fix" if L.mode == "fixed" else "float"
    state = {"decimals_seen": False}

    def etype(e, cx, promote_to=None):
        """The type of e (derivations 10-15), checking W6, W8-W10, W13 inside it. promote_to: the target a promote at
        e's root may have here (W9's three places), or None where none may stand. Returns None when underivable."""
        line, U, proc = cx
        k = e["k"]
        if k == "conv" and e["mode"] == "promote":
            ta = etype(e["a"], cx)
            # draft 9, G (ZA3): the promote's own two parts, its operand and its target, are made wherever it stands;
            # only its place's part waits for the type the place needs (draft 3, H8)
            if ta is not None and ta != "int":
                fail(line, 9, "a promote of %s" % ta)
            if e["target"] not in ("fix", "float"):
                fail(line, 9, "a promote to %s" % e["target"])
            if promote_to is not UNDERIVED and (promote_to is None or e["target"] != promote_to):
                fail(line, 9, "a promote where SPEC §5 puts none")
            e["type"] = e["target"]
            return e["target"]
        t = None
        if k == "lit":
            t = e["t"]
            if t in ("fix", "float"):
                if t != dec_type:
                    fail(line, 6, "a %s literal in a law whose decimals are %s" % (t, L.mode))
                if decimals_at and not state["decimals_seen"]:
                    fail(decimals_at[0] + 2, 6, "a decimal literal before the decimals clause")   # the later line (G8)
            if t in ("int", "fix") and e["v"] > I64_MAX:
                fail(line, 13, "a literal above 2^63-1")
            if t == "float" and (e["v"] >> 63 or (e["v"] >> 52) & 0x7FF == 0x7FF):
                fail(line, 13, "a float literal not finite, or negative")
        elif k == "str":
            if len(e["v"].encode("utf-8")) > 1 << 24:
                fail(line, 13, "a text literal above 2^24 bytes")
            t = "text"
        elif k == "seal":
            t = "text"
        elif k == "var":
            t = use(e["V"], cx)
        elif k == "rule":
            name = e["name"]
            if name not in L.rules:
                fail(line, 10, "no define of rule %r" % name)
            else:
                at = proc if proc else U
                if last_define[name] >= at:
                    fail(line, 10, "rule %r used before its last define" % name)
                t = static.get(name)        # draft 8, E2: its first define's type, wherever the use stands
        elif k == "conv":
            ta = etype(e["a"], cx)
            if ta is not None and ta not in CONV_OK[(e["mode"], e["target"])]:
                fail(line, 9, "%s to %s from %s" % (e["mode"], e["target"], ta))
            t = e["target"]
        elif k == "bin":
            op, t = e["op"], e["t"]
            pa, pb = e["a"].get("mode") == "promote", e["b"].get("mode") == "promote"
            if op in ARITH | ORDER | EQUAL:
                if pa and pb:
                    fail(line, 9, "both operands of %s are promotes" % op)
                tb0 = etype(e["b"], cx) if not pb else None
                ta0 = etype(e["a"], cx) if not pa else None
                # draft 2, G4: a promote's target is fix or float, never int; draft 3, H8: no check of its place
                # against an other operand whose type is underived (when only one operand is a promote)
                ta = etype(e["a"], cx, promote_to=place(tb0, tb0 is not None or pb)) if pa else ta0
                tb = etype(e["b"], cx, promote_to=place(ta0, ta0 is not None or pa)) if pb else tb0
            else:
                ta, tb = etype(e["a"], cx), etype(e["b"], cx)
            # draft 8, E2: each part of W9 is checked once its own inputs are derived. Both derived, the parts together
            # are the conjunction drafts 3-7 checked; one underived, the parts that need only the other are still made
            da, db = ta is not None, tb is not None
            if op in ARITH:
                parts = [(True, t in NUMERIC), (da, ta == t), (db, tb == t)]
            elif op in ("quot", "rem"):
                parts = [(True, t == "int"), (da, ta == "int"), (db, tb == "int")]
            elif op in ORDER:
                # his ruling B (the ruling sheet, 2026-10-31): "one numeric type" is a part of the pair, its kind
                # checked with the equality once both operands are derived
                parts = [(True, t == "bool"), (da and db, ta == tb and ta in NUMERIC)]
            elif op in EQUAL:
                kinds = NUMERIC | {"bool", "text"}
                parts = [(True, t == "bool"), (da and db, ta == tb and ta in kinds)]
            else:
                parts = [(True, t == "bool"), (da, ta == "bool"), (db, tb == "bool")]
            if not all(ok for made, ok in parts if made):
                fail(line, 9, "%s on %s and %s as %s" % (op, ta, tb, t))
        elif k == "un":
            ta, op, t = etype(e["a"], cx), e["op"], e["t"]
            # draft 8, E2: the result's part is made even when the operand is underived. His ruling A (the ruling
            # sheet, 2026-10-31): for neg, abs and sqrt the words state two parts, both on the operand, and no part on
            # <type> alone is made
            opnd, res = UN_RULES[op]
            parts = [(op not in ("neg", "abs", "sqrt"), t in res), (ta is not None, ta in opnd)]
            if op in ("neg", "abs", "sqrt"):
                parts.append((ta is not None, ta == t))
            if not all(ok for made, ok in parts if made):
                fail(line, 9, "%s on %s as %s" % (op, ta, t))
        elif k == "cat":
            for p in e["parts"]:
                etype(p, cx)
            t = "text"
        elif k == "item":
            ti, tv = etype(e["i"], cx), use(e["V"], cx)
            # draft 8, E2: the index's part and the variable's, each once its own input is derived
            if ti is not None and ti != "int":
                fail(line, 9, "item %s of %s" % (ti, tv))
            if tv is not None:
                if tv not in LIST_TYPES:
                    fail(line, 9, "item %s of %s" % (ti, tv))
                else:
                    t = tv[len("list-"):]
        elif k == "length":
            tv = use(e["V"], cx)
            if tv is not None and tv not in LIST_TYPES:
                fail(line, 9, "length of %s" % tv)
            t = "int"
        elif k == "list-of":
            tn, tv = etype(e["n"], cx), etype(e["v"], cx)
            # draft 8, E2: the count's part and the value's, each once its own input is derived
            if (tn is not None and tn != "int") or (tv is not None and tv not in ELEMS):
                fail(line, 9, "list-of %s %s" % (tn, tv))
            t = "list-" + tv if tv in ELEMS else None
        else:
            el = e["t"][len("list-"):]
            promotes = [x.get("mode") == "promote" for x in e["items"]]
            if all(promotes):
                fail(line, 9, "every item of a list literal is a promote")
            for x in e["items"]:
                tx = etype(x, cx, promote_to=el if el in ("fix", "float") else None)
                if tx is not None and tx != el:
                    fail(line, 9, "a list item of %s in a %s" % (tx, e["t"]))
            t = e["t"]
        e["type"] = t
        return t

    def visible(v, U):
        d = L.var[v]
        if d["kind"] == "inline":
            return False
        if d["kind"] == "for":
            return U != d["clause"] and ancestor(d["clause"], U)
        return sibling_or_below(d["clause"], U)

    def use(v, cx):
        # his ruling C (the ruling sheet, 2026-10-31): a variable's type is read as the prescribed walk meets its
        # declaration and scope; a variable the walk has not met is undeclared, its type underived. Rule typing stays
        # E2's (derivation 17); this sets up no order-free or least-fixed-point typing of variables
        line, U, proc = cx
        if v not in L.var:
            fail(line, 8, "variable %d used before it is declared" % v)
            return None
        if not visible(v, U):
            fail(line, 8, "variable %d used outside its scope" % v)
        return L.var[v]["type"]

    def declare(v, t, clause, kind, line):
        n = L.n_declared            # draft 8, E1: the i-th declaration the walk meets has id i, a repeated one counted
        L.n_declared += 1
        if v != n:
            fail(line, 8, "variable %d declared where %d is next in the walk" % (v, n))
        if v in L.var:
            fail(line, 8, "variable %d declared twice" % v)
            return                  # his ruling D: the first declaration the walk meets keeps the id's type
        L.var[v] = {"type": t, "clause": clause, "kind": kind}
        L.vars.append((v, t, kind == "let" and C[clause]["parent"] == 0))

    def stored(e, cx, slot, known=True):
        """A stored value (set, change, append): a promote may stand at its root when the slot is fix or float. known:
        whether the variable's type is derived (draft 3, H8: if not, the place is not checked)."""
        return etype(e, cx, promote_to=place(slot, known))

    def visit(s, U, inline, k):
        line = k + 2
        proc = proc_of(k)
        cx = (line, U, proc)
        sk = s["k"]
        if inline and sk not in INLINE:         # the structure gate (W7) has refused every such law
            raise AssertionError("the walk met an inline %s, which gate 3 refuses" % sk)
        if sk in ("define", "procedure", "decimals") and (inline or C[k]["parent"] != 0):
            fail(line, 6, "%s not a top-level clause statement" % sk)
        if sk == "let":
            t = etype(s["e"], cx)
            declare(s["V"], t, U, "inline" if inline else "let", line)
        elif sk in ("set", "change"):
            ti = etype(s["i"], cx) if s["i"] is not None else None
            tv = use(s["V"], cx)
            if s["V"] in L.var and L.var[s["V"]]["kind"] == "for":
                fail(line, 8, "a for counter is set or changed")
            slot = None
            # draft 8, E2: with an index, the index's part and the variable's, each once its own input is derived
            if s["i"] is not None and ti is not None and ti != "int":
                fail(line, 9, "an indexed %s with a %s index" % (sk, ti))
            if tv is not None:
                if s["i"] is None:
                    slot = tv
                elif tv not in LIST_TYPES:
                    fail(line, 9, "an indexed %s on %s" % (sk, tv))
                else:
                    slot = tv[len("list-"):]
            te = stored(s["e"], cx, slot, tv is not None)
            if slot is not None and te is not None and te != slot:
                fail(line, 9, "%s stores %s where %s is held" % (sk, te, slot))
            if sk == "change" and slot is not None and slot not in NUMERIC:
                fail(line, 9, "change on %s" % slot)
        elif sk == "say":
            etype(s["e"], cx)
        elif sk == "if":
            # every clause the chain names exists (gate 2), and the chain has section 4's shape (gate 3): its blocks
            # are all walked, and its absorbed clauses are reached here, through it (draft 5, F1)
            for arm in s["arms"]:
                acx = (line, arm["C"], proc)
                if arm["C"] != k:
                    walked[arm["C"]] = walked.get(arm["C"], 0) + 1
                if etype(arm["cond"], acx) not in ("bool", None):
                    fail(line, 9, "an arm's condition is not bool")
                b = arm["body"]
                if b["k"] == "block":
                    walk_seq(C[b["C"]]["children"])
                else:
                    visit(b, arm["C"], True, k)
            if s["els"] is not None:
                if s["els"]["C"] != k:
                    walked[s["els"]["C"]] = walked.get(s["els"]["C"], 0) + 1
                b = s["els"]["body"]
                if b["k"] == "block":
                    walk_seq(C[b["C"]]["children"])
                else:
                    visit(b, s["els"]["C"], True, k)
        elif sk == "while":
            if not 1 <= s["fuel"] <= 1 << 62:
                fail(line, 13, "a while bound outside 1..2^62")
            if etype(s["cond"], cx) not in ("bool", None):
                fail(line, 9, "a while condition is not bool")
        elif sk == "for":
            tl, th = etype(s["lo"], cx), etype(s["hi"], cx)
            if tl not in ("int", None) or th not in ("int", None):
                fail(line, 9, "a for's bounds are not int")
            declare(s["V"], "int", k, "for", line)
        elif sk == "procedure":
            L.procs[k] = s["name"]
        elif sk == "perform":
            # draft 5, K1: a procedure clause by its statement, as W11 says, not by whether the walk has met it
            P = s["C"]
            is_proc = P in C and C[P]["stmt"] is not None and C[P]["stmt"]["k"] == "procedure"
            if P in C and not (is_proc and P < U and not ancestor(P, U)):
                fail(line, 11, "perform of clause %d, not a procedure defined before" % P)
        elif sk == "must":
            if s["M"] != L.n_musts:      # draft 8, E1: counted as met, as variables are
                fail(line, 8, "must %d where %d is next in the walk" % (s["M"], L.n_musts))
            L.n_musts += 1
            L.musts[s["M"]] = U
            if etype(s["cond"], cx) not in ("bool", None):
                fail(line, 9, "a must's condition is not bool")
        elif sk == "claim":
            if s["K"] != L.n_claims:     # draft 8, E1: counted as met, as variables are
                fail(line, 8, "claim %d where %d is next in the walk" % (s["K"], L.n_claims))
            L.n_claims += 1
            L.claims[s["K"]] = U
            if etype(s["cond"], cx) not in ("bool", None):
                fail(line, 9, "a claim's condition is not bool")
            o = s["oracle"]
            if o["k"] == "certificate" and o["C"] in C:
                T = C[o["C"]]
                if not (o["C"] < U and not T["absorbed"] and T["stmt"]["k"] not in ("procedure", "define", "decimals", "claim")):
                    fail(line, 12, "a certificate's clause %d" % o["C"])
                L.cost.add(o["C"])
            if o["k"] == "agreement" and all(labelled(x) is not None for x in o["labels"]):
                if not all(labelled(x) < U for x in o["labels"]):
                    fail(line, 12, "an agreement's clauses do not come before")
            for x in s["given"]:
                if labelled(x) is not None:
                    T = C[labelled(x)]
                    if T["stmt"] is None or T["stmt"]["k"] != "claim":
                        fail(line, 12, "the premise %s is not a claim's clause" % x)
        elif sk == "define":
            name = s["name"]
            for o in s["over"]:
                if o in C and not (C[o]["stmt"] is not None and C[o]["stmt"]["k"] == "define" and C[o]["stmt"]["name"] == name):
                    fail(line, 10, "over names clause %d, not a define of %r" % (o, name))
            te = etype(s["e"], cx)
            if k == first_define.get(name) and name in self_using:
                te = None                       # draft 9, G: its value's type is underived, whatever its form
            if te in LIST_TYPES:
                fail(line, 10, "a rule's value is a list")
            if te is not None:
                if L.typed.setdefault(name, te) != te:
                    fail(line, 10, "two types for rule %r" % name)
                if k == first_define.get(name):
                    L.rule_types[name] = te     # draft 9, G (ZA1): derivation 17, the first define's, never a later one's
            if s["proviso"] is not None and etype(s["proviso"], cx) not in ("bool", None):
                fail(line, 10, "a proviso is not bool")
        elif sk == "append":
            te0 = None
            tv = use(s["V"], cx)
            if s["V"] in L.var and L.var[s["V"]]["kind"] == "for":
                fail(line, 8, "a for counter is appended to")
            slot = tv[len("list-"):] if tv in LIST_TYPES else None
            if tv is not None and slot is None:
                fail(line, 9, "append to %s" % tv)
            te0 = stored(s["e"], cx, slot, tv is not None)
            if slot is not None and te0 is not None and te0 != slot:
                fail(line, 9, "append %s to %s" % (te0, tv))
        elif sk == "remove-last":
            tv = use(s["V"], cx)
            if s["V"] in L.var and L.var[s["V"]]["kind"] == "for":
                fail(line, 8, "a for counter is removed from")      # draft 3, H6: W8, as for append
            if tv is not None and tv not in LIST_TYPES:
                fail(line, 9, "remove-last on %s" % tv)
        elif sk == "decimals":
            state["decimals_seen"] = True
        if sk in ("while", "for", "procedure"):
            walk_seq(C[k]["children"])

    def walk_seq(ks):
        # the whole tree is walked: the gates have refused every tree deeper than 24 (E1) and every malformed body or
        # chain (F1); an absorbed clause is reached through its chain, never as a member of a sequence
        for j in ks:
            if not C[j]["absorbed"] and C[j]["stmt"] is not None:
                walked[j] = walked.get(j, 0) + 1
                visit(C[j]["stmt"], j, False, j)

    # draft 8, E2: a rule's type is its first define's value's (derivation 17), wherever its use stands. The walk is
    # made again, its failures dropped, with the types the last walk gave the first defines, until they hold still.
    # Draft 9, G: only the first define in clause order types a rule (ZA1), and a self-using one types none (ZA2). A
    # type then flows into a first define from at most one other rule, and none flows round a cycle, so the types hold
    # still within one walk more than there are rules. L.typed holds each name's first derived type, for W10 alone
    static = {}
    mark = len(fails)
    for _ in range(len(L.rules) + 2):
        del fails[mark:]
        L.vars, L.var, L.rule_types, L.claims, L.musts, L.cost, L.procs = [], {}, {}, {}, {}, set(), {}
        L.typed = {}
        L.n_declared = L.n_musts = L.n_claims = 0
        walked.clear()
        state["decimals_seen"] = False
        walk_seq(L.top)
        if L.rule_types == static:
            break
        static = dict(L.rule_types)
    else:
        raise AssertionError("the rules' types did not hold still")
    # the coverage check (draft 5, F1): the walk reached every clause exactly once. A miss or a repeat is a defect of
    # this checker or of section 7's argument, never a verdict on the law, so it is raised, not reported as a refusal
    missed = [k for k in range(1, L.n + 1) if walked.get(k, 0) != 1]
    if missed:
        raise AssertionError("the walk reached clauses %s other than once" % missed[:10])
    # W10: the overrides' closure, derivation 5, by a search from each define (draft 4, J10); a cycle is a define that
    # reaches itself. The closure is a stored set of pairs, so its size, and the time to make it, can be quadratic
    L.overrides = {}
    for name, cls in L.rules.items():
        direct = {c: [o for o in C[c]["stmt"]["over"] if o in C] for c in cls}
        beats = {}
        for a in cls:
            seen, stack = set(), list(direct[a])
            while stack:
                b = stack.pop()
                if b not in seen:
                    seen.add(b)
                    stack.extend(direct.get(b, ()))
            beats[a] = seen
        for a in cls:
            if a in beats[a]:
                fail(a + 2, 10, "the overrides of %r have a cycle" % name)
        L.overrides[name] = beats


def exprs_of(s):
    k = s["k"]
    if k == "let":
        return [s["e"]]
    if k in ("set", "change"):
        return ([s["i"]] if s["i"] is not None else []) + [s["e"]]
    if k == "say":
        return [s["e"]]
    if k == "if":
        return [a["cond"] for a in s["arms"]]
    if k in ("while", "must", "claim"):
        return [s["cond"]]
    if k == "for":
        return [s["lo"], s["hi"]]
    if k == "define":
        return [s["e"]] + ([s["proviso"]] if s["proviso"] is not None else [])
    if k == "append":
        return [s["e"]]
    return []


# ------------------------------------------------------------------ the analysis's view, for comparison only
def tname(t):
    return "list-" + t[1] if isinstance(t, tuple) else t


def analysis_view(comp):
    prog, an = comp.prog, comp.an
    return {
        "top": [c.id for c in prog.top],
        "children": {c.id: [x.id for x in c.children] for c in prog.clauses},
        "labels": {k: c.id for k, c in prog.by_label.items()},
        "vars": [(v.id, tname(v.type), v.top) for v in an.vars],
        "rule_types": {k: tname(v) for k, v in an.rule_types.items()},
        "rules": {k: [c.id for c in v] for k, v in an.rules.items()},
        "overrides": {k: {a: set(b) for a, b in v.items()} for k, v in an.overrides.items()},
        "claims": [c.id for c in an.claims],
        "cost": {c.id for c in prog.clauses if c.cost_tracked},
    }


def law_view(L):
    return {
        "top": L.top,
        "children": {k: L.clauses[k]["children"] for k in L.clauses},
        "labels": L.by_label,
        "vars": L.vars,
        "rule_types": L.rule_types,
        "rules": L.rules,
        "overrides": L.overrides,
        "claims": [L.claims[k] for k in range(len(L.claims))],
        "cost": L.cost,
    }


# ------------------------------------------------------------------ fixtures and plants
FIXTURES = [   # REREAD-0's valid laws (F2, F12), as texts the front end accepts
    ("forward declaration (F2)", "§1 If true, do the following.\n§1.1 Let a be 1.\n§2 Otherwise, let b be 2.\n"),
    ("forward claims (F2)", "§1 If true, do the following.\n§1.1 We claim that true.\n§2 Otherwise, we claim that true.\n"),
    ("certificate from an inline otherwise (F2)",
     "§1 If true, do the following.\n§1.1 Let a be 1.\n§2 Otherwise, we claim that true, by the certificate of §1.1.\n"),
    ("the empty law (F12)", ""),
    # B1: no nesting limit; the front end accepts both chains, and so must the checker
    ("a perform chain of 3,000 (B1)",
     "§1 To p1, do the following.\n§1.1 Say 1.\n"
     + "".join("§%d To p%d, do the following.\n§%d.1 Perform p%d.\n" % (i, i, i, i - 1) for i in range(2, 3001))
     + "§3001 Perform p3000.\n"),
    ("a rule chain of 3,000 (B1)",
     "§1 Define r1 as 1.\n" + "".join("§%d Define r%d as r%d.\n" % (i, i, i - 1) for i in range(2, 3001))
     + "§3001 Say r3000.\n"),
]


def witness_91():
    """REREAD-8's ZA8: a text whose law has a line 91 deep, the deepest found (draft 9, his H). Under an Unless (its
    clause, its arm, its not), an Int comparison over 22 levels of a Fix sum, each over an Int conversion of the next;
    the innermost a sum over a chain of 15 conversions, with no parentheses of its own."""
    e = "w plus w" + " as an integer as a fixed" * 7 + " as an integer"
    for _ in range(22):
        e = "w plus (%s) as an integer" % e
    return ("Title: Depth.\n§1 Let w be 1.5.\n§2 Let k be 2.\n§3 Let b be true.\n"
            "§4 Unless w is less than (%s) as an integer, do the following.\n§4.1 Say 1.\n" % e)


FIXTURES.append(("a law line 91 deep, the deepest the front end is known to write (H)", witness_91()))


def nots(n, inner="(lit bool 1)"):
    e = inner
    for _ in range(n):
        e = "(not bool %s)" % e
    return e


H = "orlog-law 0\n(decimals fixed)\n"
BS = chr(92)
BYTE_FIXTURES = [   # draft 2's byte-level fixtures, which no text writes but the format accepts
    ("U+0000 in a string (G3)", (H + '(clause 1 0 (say (str "%su{0}")))\n' % BS).encode()),
    ("a clause line nested exactly 91 deep (G11; draft 9, H)",
     (H + '(clause 1 0 (if (arm 1 (lit bool 1) (let 0 "x" %s)) -))\n' % nots(86)).encode()),
    # draft 4, J11: an escaped quote, then 131 '(' inside the string; the count skips the byte after a backslash, so
    # the string goes on and the count is 3. A count that does not skip it would close the string early: W14
    ("an escaped quote, then 131 '(' inside the string (J11)",
     (H + '(clause 1 0 (say (str "a%s"%s")))\n' % (BS, "(" * 131)).encode()),
]


def deep_else(deep_stmt, else_stmt):
    """REREAD-3's J1 laws: clause 1 an If whose block is a chain of If blocks 25 deep, the deepest holding a statement,
    and an absorbed top-level clause holding the If's else, whose inline statement is written on line 3. Draft 3's
    capped walk numbered the else's declaration as if the skipped one did not exist."""
    lines = ["(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 27 %s)))" % else_stmt]
    for k in range(2, 26):
        lines.append("(clause %d %d (if (arm %d (lit bool 1) (block %d)) -))" % (k, k - 1, k, k))
    lines.append("(clause 26 25 %s)" % deep_stmt)
    lines.append("(clause 27 0 absorbed)")
    return (H + "\n".join(lines) + "\n").encode()


def statements(L):
    out = []
    for k in range(1, L.n + 1):
        c = L.clauses[k]
        if c["stmt"] is None:
            continue

        def go(s, k=k):
            out.append((k, s))
            if s["k"] == "if":
                for a in s["arms"]:
                    if a["body"]["k"] != "block":
                        go(a["body"])
                if s["els"] is not None and s["els"]["body"]["k"] != "block":
                    go(s["els"]["body"])
        go(c["stmt"])
    return out


def binaries(e, out):
    if isinstance(e, dict):
        if e.get("k") == "bin":
            out.append(e)
        for v in e.values():
            binaries(v, out)
    elif isinstance(e, list):
        for v in e:
            binaries(v, out)
    return out


# each structural plant changes a read Law in one place and returns the line section 8 must report, or None
def p_perform_missing(L):
    for k, s in statements(L):
        if s["k"] == "perform":
            s["C"] = L.n + 50
            return k + 2


def p_child_of_say(L):
    if any(s["k"] == "claim" and (s["given"] or s["oracle"]["k"] == "agreement") for _, s in statements(L)):
        return None
    for a, b in zip(L.top, L.top[1:]):
        sa, sb = L.clauses[a]["stmt"], L.clauses[b]["stmt"]
        if sa is not None and sa["k"] == "say" and sb is not None and sb["k"] in ("say", "let", "set") \
                and not L.clauses[b]["children"] and b == L.n and b == a + 1:
            L.clauses[b]["parent"] = a
            return a + 2


def p_mode_flipped(L):
    if any(L.clauses[k]["stmt"] is not None and L.clauses[k]["stmt"]["k"] == "decimals" for k in L.clauses):
        return None
    if any("lit fix" in w_stmt(L.clauses[k]["stmt"]) for k in L.clauses if L.clauses[k]["stmt"] is not None):
        return None
    L.mode = "floats"
    return 2


def p_inline_while(L):
    for k, s in statements(L):
        if s["k"] == "if":
            for a in s["arms"]:
                if a["body"]["k"] != "block":
                    a["body"] = {"k": "while", "fuel": 1, "cond": {"k": "lit", "t": "bool", "v": 0}}
                    return k + 2


def p_var_before_declared(L):
    for k, s in statements(L):
        if s["k"] == "let" and s["V"] == 0:
            s["e"] = {"k": "var", "V": 0}
            return k + 2


def p_int_sum_as_fix(L):
    for k, s in statements(L):
        for b in binaries(s, []):
            if b["op"] == "+" and b["t"] == "int":
                b["t"] = "fix"
                return k + 2


def p_override_cycle(L):
    for k, s in statements(L):
        if s["k"] == "define" and s["over"]:
            other = s["over"][0]
            L.clauses[other]["stmt"]["over"] = L.clauses[other]["stmt"]["over"] + [k]
            return min(k, other) + 2


def p_perform_not_a_procedure(L):
    procs = [k for k in L.clauses if L.clauses[k]["stmt"] is not None and L.clauses[k]["stmt"]["k"] == "procedure"]
    for k, s in statements(L):
        if s["k"] == "perform":
            earlier = [j for j in range(1, k) if j not in procs and not L.clauses[j]["absorbed"]]
            if earlier:
                s["C"] = earlier[0]
                return k + 2


def p_certificate_later(L):
    for k, s in statements(L):
        if s["k"] == "claim" and s["oracle"]["k"] == "certificate":
            s["oracle"]["C"] = L.n
            return k + 2


def p_while_zero(L):
    for k, s in statements(L):
        if s["k"] == "while":
            s["fuel"] = 0
            return k + 2


def lit(t, v):
    return {"k": "lit", "t": t, "v": v}


DEEP_NOT = "(lit bool 1)"
for _ in range(300):
    DEEP_NOT = "(not bool %s)" % DEEP_NOT

PLANTS = [   # (W, line, what, the plant)
    (1, 2, "a CR at the end of line 2 (draft 0)", ("bytes", b"\n(clause 1 ", b"\r\n(clause 1 ")),
    (2, 3, "a natural number with a leading zero (draft 0)", ("replace-line", 3, lambda ln: ln.replace("(lit int ", "(lit int 0", 1) if "(lit int " in ln else None)),
    (3, 3, "two spaces between two items (draft 0)", ("replace-line", 3, lambda ln: ln.replace(" (", "  (", 1) if " (" in ln[10:] else None)),
    (4, None, "a perform of a clause that does not exist (draft 0)", ("law", p_perform_missing)),
    (5, None, "a clause made a child of a say clause (draft 0)", ("law", p_child_of_say)),
    (6, None, "line 2's mode not the law's (draft 0)", ("law", p_mode_flipped)),
    (7, None, "a while inline in an arm (draft 0)", ("law", p_inline_while)),
    (8, None, "a variable used before it is declared (draft 0)", ("law", p_var_before_declared)),
    (9, None, "an Int sum written as a Fix sum (draft 0)", ("law", p_int_sum_as_fix)),
    (10, None, "a notwithstanding cycle (draft 0)", ("law", p_override_cycle)),
    (11, None, "a perform of an earlier clause that is no procedure (draft 0)", ("law", p_perform_not_a_procedure)),
    (12, None, "a certificate naming the last clause (draft 0)", ("law", p_certificate_later)),
    (13, None, "a while bound of 0 (draft 0)", ("law", p_while_zero)),
    (1, 5, "F1: clause 3 a child of clause 1, after clause 2", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (while 1 (lit bool 1)))\n(clause 2 0 (let 0 "x" (lit int 1)))\n(clause 3 1 (say (var 0)))\n')),
    (14, 3, "F3: a 300-deep chain of not", ("raw", ("orlog-law 0\n(decimals fixed)\n(clause 1 0 (say %s))\n" % DEEP_NOT).encode())),
    (9, 3, "F4: a let whose value is a promote", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (let 0 "x" (promote fix (lit int 1))))\n')),
    (9, 3, "F4: both operands of + promotes", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (say (+ fix (promote fix (lit int 1)) (promote fix (lit int 2)))))\n')),
    (9, 3, "F4: a list whose every item is a promote", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (say (list list-fix (promote fix (lit int 1)))))\n')),
    (5, 3, "F6: a block arm with an otherwise in its own line", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 1 (say (lit int 2)))))\n(clause 2 1 (say (lit int 1)))\n')),
    (5, 3, "F6: two arms and an otherwise in the If's own line", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (if (arm 1 (lit bool 1) (say (lit int 1))) (arm 2 (lit bool 1) (say (lit int 2))) (else 1 (say (lit int 3)))))\n(clause 2 0 absorbed)\n')),
    (2, 3, "F5: a surrogate in a string", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (say (str "\\u{d800}")))\n')),
    (2, 3, "F8: an A written as \\u{41}", ("raw", b'orlog-law 0\n(decimals fixed)\n(clause 1 0 (say (str "\\u{41}")))\n')),
    # draft 2's plants (REREAD-1's G18 and the G-findings' own cases)
    (14, 27, "G18: W14(a), a clause 25 deep (a chain of If blocks)",
     ("raw", (H + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, k - 1, k, k) for k in range(1, 25))
              + "(clause 25 24 (say (lit int 1)))\n").encode())),
    (14, 19, "G18: W14(b), 17 nested loops",
     ("raw", (H + "".join("(clause %d %d (while 1 (lit bool 0)))\n" % (k, k - 1) for k in range(1, 18))
              + "(clause 18 17 (say (lit int 1)))\n").encode())),
    (8, 3, "G18: ids numbered in line order, not walk order",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 3 (let 0 "b" (lit int 2)))))\n'
                  '(clause 2 1 (let 1 "a" (lit int 1)))\n(clause 3 0 absorbed)\n').encode())),
    (6, 3, "G18: a float literal under fixed",
     ("raw", (H + "(clause 1 0 (say (lit float 3ff0000000000000)))\n").encode())),
    (10, 3, "G1, T3: a rule cycle through define values",
     ("raw", (H + '(clause 1 0 (define "b" (rule "c") - (over )))\n(clause 2 0 (define "c" (rule "b") - (over )))\n'
                  '(clause 3 0 (say (rule "b")))\n').encode())),
    (8, 3, "G1, T4: a define's value using a later let",
     ("raw", (H + '(clause 1 0 (define "r" (var 0) - (over )))\n(clause 2 0 (let 0 "x" (lit int 1)))\n'
                  '(clause 3 0 (say (rule "r")))\n').encode())),
    (2, 3, "G18: \\u{110000} in a string", ("raw", (H + '(clause 1 0 (say (str "%su{110000}")))\n' % BS).encode())),
    (9, 3, "G4: promote int in +", ("raw", (H + "(clause 1 0 (say (+ int (promote int (lit int 1)) (lit int 2))))\n").encode())),
    (9, 3, "G4: promote int in ==", ("raw", (H + "(clause 1 0 (say (== bool (lit int 2) (promote int (lit int 2)))))\n").encode())),
    (9, 3, "G4: promote int in <", ("raw", (H + "(clause 1 0 (say (< bool (promote int (lit int 1)) (lit int 2))))\n").encode())),
    (4, 4, "G5: an else naming clause 99",
     ("raw", (H + '(clause 1 0 (let 0 "x" (lit int 1)))\n(clause 2 0 (if (arm 2 (lit bool 1) (say (var 0))) (else 99 (say (var 0)))))\n').encode())),
    (4, 4, "G5: an arm naming clause 99",
     ("raw", (H + '(clause 1 0 (let 0 "x" (lit int 1)))\n(clause 2 0 (if (arm 99 (lit bool 1) (say (var 0))) -))\n').encode())),
    (14, 3, "G9: a clause line nested 92 deep (draft 9, H)",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (let 0 "x" %s)) -))\n' % nots(87)).encode())),
    (14, 3, "G9: nested 25,000 deep, then a W2 line",
     ("raw", (H + "(clause 1 0 (say %s))\n(clause 2 0 (say (lit int 01)))\n" % nots(25000)).encode())),
    (1, 3, "G6: T1, line 3 not a clause line, line 4 a bad byte",
     ("raw", (H + 'XYZ\n(clause 2 0 (say (str "a\x01")))\n').encode())),
    (1, 3, "G6: T2, line 3 not a clause line, line 4 with no LF",
     ("raw", (H + "XYZ\n(clause 2 0 (say (lit int 1)))").encode())),
    (1, 1, "G6: T2b, line 1 wrong, line 4 a bad byte",
     ("raw", b"orlog-law 1\n(decimals fixed)\n(clause 1 0 (say (lit int 1)))\n\x01\n")),
    (7, 5, "G8: an inline if with a block (W7, not walked)",
     ("raw", (H + '(clause 1 0 (while 1 (lit bool 0)))\n(clause 2 1 (let 0 "a" (lit int 1)))\n'
                  "(clause 3 0 (if (arm 3 (lit bool 1) (if (arm 3 (lit bool 1) (block 1)) -)) -))\n").encode())),
    (6, 4, "G8: a decimal literal before decimals (the decimals line)",
     ("raw", (H + "(clause 1 0 (say (lit fix 5)))\n(clause 2 0 (decimals fixed))\n").encode())),
    (5, 5, "G8: an absorbed clause named by two Ifs (the later If)",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (say (lit int 1))) (else 2 (say (lit int 2)))))\n(clause 2 0 absorbed)\n"
                  "(clause 3 0 (if (arm 3 (lit bool 1) (say (lit int 3))) (else 2 (say (lit int 4)))))\n").encode())),
    (3, 4, "G7: two spaces before absorbed",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (say (lit int 1))) (else 2 (say (lit int 2)))))\n(clause 2 0  absorbed)\n").encode())),
    (1, 3, "G7: two spaces in the prefix", ("raw", (H + "(clause 1  0 (say (lit int 1)))\n").encode())),
    # draft 3's plants (REREAD-2's H2, H5-H8, H13)
    (14, 19, "H2: 30,000 nested whiles, refused without a crash",
     ("raw", (H + "".join("(clause %d %d (while 1 (lit bool 0)))\n" % (k, k - 1) for k in range(1, 30001))
              + "(clause 30001 30000 (say (lit int 1)))\n").encode())),
    (14, 27, "H2: 30,000 nested If blocks, refused without a crash",
     ("raw", (H + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, k - 1, k, k)
                          for k in range(1, 30001))
              + "(clause 30001 30000 (say (lit int 1)))\n").encode())),
    (2, 3, "H5: an unbalanced line whose count never exceeds 91",
     ("raw", (H + "(clause 1 0 ))" + "(" * 92 + ")" * 90 + ")\n").encode())),
    (14, 3, "H5: an unbalanced line whose count exceeds 91",
     ("raw", (H + "(clause 1 0 )" + "(" * 92 + ")" * 91 + ")\n").encode())),
    (8, 4, "H6: remove-last on a for counter",
     ("raw", (H + "(clause 1 0 (for 0 (lit int 0) (lit int 1)))\n(clause 2 1 (remove-last 0))\n").encode())),
    (5, 6, "H7: an absorbed clause named by two Ifs through blocks",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (say (lit int 1))) (else 2 (block 2))))\n(clause 2 0 absorbed)\n"
                  "(clause 3 2 (say (lit int 2)))\n"
                  "(clause 4 0 (if (arm 4 (lit bool 1) (say (lit int 3))) (else 2 (block 2))))\n").encode())),
    (10, 3, "H8: a promote beside a rule with no define",
     ("raw", (H + '(clause 1 0 (say (+ fix (promote fix (lit int 1)) (rule "r"))))\n').encode())),
    (4, 5, "H13: G5's third, an else naming clause 99 after a procedure",
     ("raw", (H + '(clause 1 0 (procedure "p"))\n(clause 2 1 (say (lit int 1)))\n'
                  "(clause 3 0 (if (arm 3 (lit bool 1) (perform 1)) (else 99 (perform 1))))\n").encode())),
    # draft 4's plants (REREAD-3's J1, J7-J9, J11, and E1's two gates in their order)
    (14, 27, "J1: deep let 0, inline else let 1 (the depth gate)",
     ("raw", deep_else('(let 0 "a" (lit int 1))', '(let 1 "b" (lit int 2))'))),
    (14, 27, "J1: deep let 1, inline else let 0 (the depth gate)",
     ("raw", deep_else('(let 1 "a" (lit int 1))', '(let 0 "b" (lit int 2))'))),
    (14, 27, "J1: deep must 0, inline else must 1 (the depth gate)",
     ("raw", deep_else("(must 0 (lit bool 1))", "(must 1 (lit bool 1))"))),
    (14, 27, "J1: deep claim 0, inline else claim 1 (the depth gate)",
     ("raw", deep_else("(claim 0 (lit bool 1) (computation) (given ))", "(claim 1 (lit bool 1) (computation) (given ))"))),
    (4, 4, "J7: an inner chain naming clause 99, under an else's let (the chain gate)",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (let 1 "b" (lit int 2)))))\n'
                  "(clause 2 1 (if (arm 2 (lit bool 1) (block 2)) (else 99 (say (lit int 0)))))\n"
                  '(clause 3 2 (let 0 "a" (lit int 1)))\n(clause 4 0 absorbed)\n').encode())),
    # draft 6, N1: the gates' precedence, the depth gate first, then the least (line, W) among the chain and structure
    # gates' failures. Draft 5 expected W4 at line 3 here, and W7 at line 3 in the fourth, from a rule E1(b)'s adopted
    # text did not allow (REREAD-5's L1)
    (14, 28, "N1 gates: a chain on line 3, a clause 25 deep on line 28",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (say (lit int 1))) (else 99 (say (lit int 2)))))\n"
              + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, 0 if k == 2 else k - 1, k, k)
                        for k in range(2, 26))
              + "(clause 26 25 (say (lit int 1)))\n").encode())),
    (14, 27, "N1 gates: a clause 25 deep on line 27, a chain on line 28",
     ("raw", (H + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, k - 1, k, k)
                          for k in range(1, 25))
              + "(clause 25 24 (say (lit int 1)))\n"
              + "(clause 26 0 (if (arm 26 (lit bool 1) (say (lit int 1))) (else 99 (say (lit int 2)))))\n").encode())),
    (5, 3, "N1 gates: a W5 body on line 3 before a chain on line 5",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 1 (say (lit int 2)))\n"
                  "(clause 3 0 (if (arm 3 (lit bool 1) (say (lit int 3))) (else 99 (say (lit int 4)))))\n").encode())),
    (14, 28, "N1 gates: a W7 inline on line 3, a clause 25 deep on line 28",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (while 1 (lit bool 0))) -))\n"
              + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, 0 if k == 2 else k - 1, k, k)
                        for k in range(2, 26))
              + "(clause 26 25 (say (lit int 1)))\n").encode())),
    (4, 3, "N1 gates: W4 and W7 on one line, an inline if naming 99",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (if (arm 99 (lit bool 1) (say (lit int 1))) -)) -))\n").encode())),
    # draft 6, L6: same-line ties between the depth gate and the others: the depth gate wins
    (14, 27, "N1 gates: a clause 25 deep whose own If names 99",
     ("raw", (H + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, k - 1, k, k)
                          for k in range(1, 25))
              + "(clause 25 24 (if (arm 25 (lit bool 1) (say (lit int 1))) (else 99 (say (lit int 2)))))\n").encode())),
    (14, 27, "N1 gates: a clause 25 deep whose own If has an inline while",
     ("raw", (H + "".join("(clause %d %d (if (arm %d (lit bool 0) (block %d)) -))\n" % (k, k - 1, k, k)
                          for k in range(1, 25))
              + "(clause 25 24 (if (arm 25 (lit bool 1) (while 1 (lit bool 0))) -))\n").encode())),
    # draft 6, L7: three structure failures, each on line 4, behind a W8 on line 3: the structure gate reports them
    (5, 4, "L7: a chain whose absorbed clause is not right after it",
     ("raw", (H + "(clause 1 0 (say (var 0)))\n"
                  "(clause 2 0 (if (arm 2 (lit bool 1) (say (lit int 1))) (else 4 (say (lit int 2)))))\n"
                  "(clause 3 0 (say (lit int 3)))\n(clause 4 0 absorbed)\n").encode())),
    (5, 4, "L7: an absorbed clause in no chain",
     ("raw", (H + "(clause 1 0 (say (var 0)))\n(clause 2 0 absorbed)\n").encode())),
    (5, 4, "L7: a block naming a clause with no children",
     ("raw", (H + "(clause 1 0 (say (var 0)))\n(clause 2 0 (if (arm 2 (lit bool 1) (block 2)) -))\n").encode())),
    # draft 6, N3: W5's narrow reading. Only the block of an If that is a clause's statement names a clause; an inline
    # if's block names nothing, so the say keeps a child and no body (W5 at line 3, before the inline if's W7 at line 5)
    (5, 3, "N3: W5, an inline if's block names no clause",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 1 (say (lit int 2)))\n"
                  "(clause 3 0 (if (arm 3 (lit bool 1) (if (arm 3 (lit bool 1) (block 1)) -)) -))\n").encode())),
    # draft 7, M3: W5's naming, read as its row is written, in a sound chain and in a chain naming a missing clause
    (5, 5, "M3: a sound chain's first arm names absorbed clause 2",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 0 absorbed)\n"
                  "(clause 3 0 (if (arm 2 (lit bool 1) (say (lit int 1))) -))\n").encode())),
    (4, 5, "M3: the same first arm, in a chain whose else names 99",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 0 absorbed)\n"
                  "(clause 3 0 (if (arm 2 (lit bool 1) (say (lit int 1))) (else 99 (say (lit int 2)))))\n").encode())),
    (4, 5, "M3: a later arm of a chain naming 99 names an earlier absorbed clause",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 0 absorbed)\n"
                  "(clause 3 0 (if (arm 3 (lit bool 1) (say (lit int 1))) (arm 2 (lit bool 1) (say (lit int 2))) "
                  "(else 99 (say (lit int 3)))))\n").encode())),
    # draft 7, M4: N3's narrow reading for an inline if's else: it names nothing, so clause 2 is in no chain
    (5, 4, "M4: an inline if's else names no absorbed clause",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 0 absorbed)\n"
                  "(clause 3 0 (if (arm 3 (lit bool 1) (if (arm 3 (lit bool 1) (say (lit int 1))) (else 2 (say (lit int 2)))))"
                  " -))\n").encode())),
    # draft 8, E1: the i-th declaration met has id i. The block's two lets (lines 4, 5) are met before the inline else
    # (line 3), so the else's is the third declaration and should be id 2; counting distinct ids gave W8 at line 5
    (8, 3, "E1: ids numbered as met, a repeated declaration counted",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (let 1 "c" (lit int 3)))))\n'
                  '(clause 2 1 (let 0 "a" (lit int 1)))\n(clause 3 1 (let 0 "b" (lit int 2)))\n(clause 4 0 absorbed)\n'
              ).encode())),
    # draft 8, E2: a rule's type is its first define's wherever its use stands: r is bool, so the int sum's W9 is made
    # on line 3, beside the use's W10 there, and the least W is reported. Typed as met, the use had no type, the sum's
    # other parts held, and W10 alone stood
    (9, 3, "E2: a rule used before its define is typed by its first define",
     ("raw", (H + '(clause 1 0 (say (+ int (rule "r") (lit int 1))))\n'
                  '(clause 2 0 (define "r" (lit bool 1) - (over )))\n').encode())),
    # draft 8, E2: each part of W9 once its own inputs are derived: x is no list, which needs no index type
    (9, 4, "E2: an indexed set on a variable that is no list, its index underived",
     ("raw", (H + '(clause 1 0 (let 0 "x" (lit int 1)))\n(clause 2 0 (set 0 (rule "r") (lit int 2)))\n').encode())),
    (9, 4, "E2: an indexed change on a bool, its index underived",
     ("raw", (H + '(clause 1 0 (let 0 "x" (lit bool 1)))\n(clause 2 0 (change + 0 (rule "r") (lit int 1)))\n'
              ).encode())),
    # draft 9, G (ZA2): a first define whose value uses its own rule leaves its type underived, whatever the form gives:
    # the use is W10 alone. Typed by the form, r was int, and `as int` from int stood beside it as W9
    (10, 3, "G: a first define that uses its own rule has no type",
     ("raw", (H + '(clause 1 0 (define "r" (as int (rule "r")) - (over )))\n').encode())),
    # the same through another rule's first define: r's uses s, s's uses r; neither has a type
    (10, 3, "G: two first defines that use each other have no type",
     ("raw", (H + '(clause 1 0 (define "r" (as int (rule "s")) - (over )))\n'
                  '(clause 2 0 (define "s" (as int (rule "r")) - (over )))\n').encode())),
    # draft 9, G (ZA1): the first define in clause order types the rule, never a later one. s's first define names a
    # rule with no define, so s has no type and the use is W10 alone; typed by its second define, s was int (W9)
    (10, 3, "G: a rule typed by its first define, not a later derived one",
     ("raw", (H + '(clause 1 0 (say (as int (rule "s"))))\n(clause 2 0 (define "s" (rule "u") - (over )))\n'
                  '(clause 3 0 (define "s" (lit int 1) - (over )))\n').encode())),
    # the same fallback made the types cycle and the checker crash: r through list-of and s each typed by a later define
    (10, 3, "G: two rules each with a later typed define, no crash",
     ("raw", (H + '(clause 1 0 (define "r" (list-of (lit int 1) (rule "s")) - (over )))\n'
                  '(clause 2 0 (define "s" (rule "r") - (over )))\n(clause 3 0 (define "r" (lit int 1) - (over )))\n'
                  '(clause 4 0 (define "s" (lit bool 0) - (over )))\n').encode())),
    # draft 9, G (ZA3): a promote's own parts are made where its place's type is underived: a bool operand, a target
    # of int. Gated by the place, each gave W10 alone
    (9, 3, "G: a promote of a bool, its place underived",
     ("raw", (H + '(clause 1 0 (say (+ float (promote float (lit bool 1)) (rule "r"))))\n').encode())),
    (9, 3, "G: a promote to int, its place underived",
     ("raw", (H + '(clause 1 0 (say (+ int (promote int (lit int 1)) (rule "r"))))\n').encode())),
    # his ruling A (the ruling sheet, 2026-10-31): neg's two parts both need the operand, so with it underived neither
    # is made and W10 stands alone. With a part on <type> alone, bool not numeric gave W9
    (10, 3, "RS-A: neg bool over an underived rule",
     ("raw", (H + '(clause 1 0 (say (neg bool (rule "r"))))\n').encode())),
    # his ruling B: a comparison's kind is a part of the pair, made once both operands are derived. Per operand, the
    # bool operand alone gave W9
    (10, 3, "RS-B: < over a bool and an underived rule",
     ("raw", (H + '(clause 1 0 (say (< bool (lit bool 1) (rule "r"))))\n').encode())),
    (10, 4, "RS-B: == over a list and an underived rule",
     ("raw", (H + '(clause 1 0 (let 0 "x" (list-of (lit int 1) (lit int 2))))\n'
                  '(clause 2 0 (say (== bool (var 0) (rule "r"))))\n').encode())),
    # his ruling C: a variable's type is read as the walk meets its declaration. q's first define reads id 0, which the
    # walk meets only after it (V1): underived, W10. Met before it, out of scope (V2): typed int, and neg fix of int W9
    (10, 3, "RS-C: a first define reads a variable the walk meets later",
     ("raw", (H + '(clause 1 0 (say (neg fix (rule "q"))))\n(clause 2 0 (define "q" (var 0) - (over )))\n'
                  '(clause 3 0 (let 0 "y" (lit int 1)))\n').encode())),
    (9, 3, "RS-C: a first define reads a variable met earlier, out of scope",
     ("raw", (H + '(clause 1 0 (say (neg fix (rule "q"))))\n'
                  '(clause 2 0 (if (arm 2 (lit bool 1) (let 0 "y" (lit int 1))) -))\n'
                  '(clause 3 0 (define "q" (var 0) - (over )))\n').encode())),
    # his ruling D: an id declared twice is typed by the first declaration the walk meets (int, then fix: q is int)
    (9, 3, "RS-D: id 0 declared int, then fix",
     ("raw", (H + '(clause 1 0 (say (neg fix (rule "q"))))\n(clause 2 0 (let 0 "a" (lit int 1)))\n'
                  '(clause 3 0 (let 0 "b" (lit fix 1)))\n(clause 4 0 (define "q" (var 0) - (over )))\n').encode())),
    (10, 3, "RS-D: id 0 declared fix, then int",
     ("raw", (H + '(clause 1 0 (say (neg fix (rule "q"))))\n(clause 2 0 (let 0 "a" (lit fix 1)))\n'
                  '(clause 3 0 (let 0 "b" (lit int 1)))\n(clause 4 0 (define "q" (var 0) - (over )))\n').encode())),
    # REREAD-8's ZA5 (adopted as test corrections under E1 and E2): E1 for musts and claims, the block's two of id 0
    # met before the inline else's id 1, the third met; and W9's parts outside set and change, each made alone
    (8, 3, "ZA5: E1 musts, counted as met",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (must 1 (lit bool 1)))))\n'
                  '(clause 2 1 (must 0 (lit bool 1)))\n(clause 3 1 (must 0 (lit bool 1)))\n(clause 4 0 absorbed)\n'
              ).encode())),
    (8, 3, "ZA5: E1 claims, counted as met",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (claim 1 (lit bool 1) (computation) '
                  '(given )))))\n(clause 2 1 (claim 0 (lit bool 1) (computation) (given )))\n'
                  '(clause 3 1 (claim 0 (lit bool 1) (computation) (given )))\n(clause 4 0 absorbed)\n').encode())),
    (9, 3, "ZA5: + int over an underived rule and a bool",
     ("raw", (H + '(clause 1 0 (say (+ int (rule "r") (lit bool 1))))\n').encode())),
    (9, 3, "ZA5: not int over an underived rule",
     ("raw", (H + '(clause 1 0 (say (not int (rule "r"))))\n').encode())),
    (9, 4, "ZA5: item of an int variable, its index underived",
     ("raw", (H + '(clause 1 0 (let 0 "x" (lit int 1)))\n(clause 2 0 (say (item 0 (rule "r"))))\n').encode())),
    (9, 3, "ZA5: list-of with a text value, its count underived",
     ("raw", (H + '(clause 1 0 (say (list-of (rule "r") (str "a"))))\n').encode())),
    # draft 8, V4: two readings that agree with the text, pinned. W14(b) counts loops only below the nearest procedure:
    # ten loops, a procedure (not top-level: W6), ten more; with no reset, the depth gate would refuse at the 17th loop
    (6, 13, "V4: W14(b) counts loops again below a procedure",
     ("raw", (H + "".join("(clause %d %d (while 1 (lit bool 0)))\n" % (k, k - 1) for k in range(1, 11))
              + '(clause 11 10 (procedure "p"))\n'
              + "".join("(clause %d %d (while 1 (lit bool 0)))\n" % (k, k - 1) for k in range(12, 22))
              + "(clause 22 21 (say (lit int 1)))\n").encode())),
    # a block that names another clause than its arm's still names it (W5's row): clause 1 may have its child, and only
    # the If's own line fails; counting only a block naming its own clause would also refuse clause 1 at line 3
    (5, 5, "V4: a block naming another clause still names it",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 1 (say (lit int 2)))\n"
                  "(clause 3 0 (if (arm 3 (lit bool 1) (block 1)) -))\n").encode())),
    # draft 5, K1: the children of a clause with children and no body. Draft 4's walk skipped them, and the report
    # moved across lines; the structure gate refuses each at the clause's own line
    (5, 4, "K1: A1, a say with a let 0 child; inline else let 1",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (let 1 "b" (lit int 2)))))\n'
                  '(clause 2 1 (say (lit int 1)))\n(clause 3 2 (let 0 "a" (lit int 1)))\n(clause 4 0 absorbed)\n').encode())),
    (5, 4, "K1: A2, the same numbered the other way",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (let 0 "b" (lit int 2)))))\n'
                  '(clause 2 1 (say (lit int 1)))\n(clause 3 2 (let 1 "a" (lit int 1)))\n(clause 4 0 absorbed)\n').encode())),
    (5, 4, "K1: A4, the same with claims",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 4 (claim 1 (lit bool 1) (computation) (given )))))\n"
                  "(clause 2 1 (say (lit int 1)))\n(clause 3 2 (claim 0 (lit bool 1) (computation) (given )))\n"
                  "(clause 4 0 absorbed)\n").encode())),
    (5, 4, "K1: B1, an absorbed arm clause with a let child",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (say (lit int 1))) (arm 2 (lit bool 1) (say (lit int 2))) "
                  '(else 4 (let 1 "b" (lit int 2)))))\n'
                  '(clause 2 0 absorbed)\n(clause 3 2 (let 0 "a" (lit int 1)))\n(clause 4 0 absorbed)\n').encode())),
    (5, 4, "K1: C1, an inline-else perform of a procedure under a say",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 5 (perform 3))))\n"
                  '(clause 2 1 (say (lit int 1)))\n(clause 3 2 (procedure "p"))\n(clause 4 3 (say (lit int 2)))\n'
                  "(clause 5 0 absorbed)\n").encode())),
    # draft 5, K4: W6 and W7 on one line; the structure gate reports W7 before any walk
    (7, 3, "K4: an inline define",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (define "r" (lit int 1) - (over ))) -))\n').encode())),
    (7, 3, "K4: an inline procedure",
     ("raw", (H + '(clause 1 0 (if (arm 1 (lit bool 1) (procedure "p")) -))\n').encode())),
    (7, 3, "K4: an inline decimals",
     ("raw", (H + "(clause 1 0 (if (arm 1 (lit bool 1) (decimals fixed)) -))\n").encode())),
    # draft 5, K6: the chain gate's own property, a later gate failure reported over an earlier walk failure
    (4, 4, "K6: perform 99 on line 3, a chain naming 99 on line 4",
     ("raw", (H + "(clause 1 0 (perform 99))\n"
                  "(clause 2 0 (if (arm 2 (lit bool 1) (say (lit int 1))) (else 99 (say (lit int 2)))))\n").encode())),
    (4, 4, "K6: an undeclared variable on line 3, (block 99) on line 4",
     ("raw", (H + "(clause 1 0 (say (var 0)))\n(clause 2 0 (if (arm 2 (lit bool 1) (block 99)) -))\n").encode())),
    (6, 3, "J8: a float literal under line 2's fixed, decimals floats later",
     ("raw", (H + "(clause 1 0 (say (lit float 3ff0000000000000)))\n(clause 2 0 (decimals floats))\n").encode())),
    (13, 3, "J9: a 5,000-digit Int literal",
     ("raw", (H + "(clause 1 0 (say (lit int %s)))\n" % ("9" * 5000)).encode())),
    (1, 3, "J9: a 5,000-digit clause number",
     ("raw", (H + "(clause %s 0 (say (lit int 1)))\n" % ("9" * 5000)).encode())),
    (4, 3, "J9: a 5,000-digit perform target",
     ("raw", (H + "(clause 1 0 (perform %s))\n" % ("9" * 5000)).encode())),
    (4, 4, "J9: a 5,000-digit label part",
     ("raw", (H + "(clause 1 0 (say (lit int 1)))\n(clause 2 0 (claim 0 (lit bool 1) (computation) (given %s)))\n"
              % ("9" * 5000)).encode())),
    (14, 3, "J11: an escaped quote, then 131 '(' outside the string",
     ("raw", (H + '(clause 1 0 (say (str "a%s"")%s))\n' % (BS, "(" * 131)).encode())),
]


def plant_bytes(laws, kind):
    """The first law the plant applies to: (its id, the planted bytes, the line section 8 must report)."""
    if kind[0] == "raw":
        return "(the plant's own bytes)", kind[1], None
    for ident, law in laws:
        if kind[0] == "bytes":
            if kind[1] in law:
                return ident, law.replace(kind[1], kind[2], 1), None
            continue
        if kind[0] == "replace-line":
            ls = law.decode("ascii").split("\n")
            if len(ls) > kind[1] - 1:
                new = kind[2](ls[kind[1] - 1])
                if new is not None and new != ls[kind[1] - 1]:
                    ls[kind[1] - 1] = new
                    return ident, "\n".join(ls).encode("ascii"), None
            continue
        try:
            L = read(law)
        except Refused:
            continue
        line = kind[1](L)
        if line is not None:
            return ident, write(L), line
    return None, None, None


def main():
    import common
    from closure_tests import fixtures
    from orlog.front import compile_bytes
    lines = []

    def say(s=""):
        lines.append(s)
        print(s, flush=True)

    texts = common.accepted() + fixtures()
    say("LAW-FORMAT-0'S CHECKER, DRAFT 9 (research/rust-core/format_check.py)")
    with open(os.path.join(HERE, "LAW-FORMAT-0-DRAFT-9.md"), "rb") as f:
        say("LAW-FORMAT-0-DRAFT-9.md sha256 %s" % common.sha(f.read()))
    say("Python's recursion limit in this process: %d (the default; draft 9 raises none); its int-string limit: %d, lifted only inside read()" % (sys.getrecursionlimit(), sys.get_int_max_str_digits()))
    with open(os.path.abspath(__file__), "rb") as f:
        say("format_check.py sha256 %s" % common.sha(f.read()))
    say()
    say("== LAW-SUFFICIENCY's %d laws, and %d fixture laws (REREAD-0's four, and B1's two chains)" % (len(texts), len(FIXTURES)))
    passed = same = exact = 0
    fails = []
    laws = []
    deepest = 0
    for ident, raw in [(t[0], t[2]) for t in texts] + [("fixture: " + n, t.encode("utf-8")) for n, t in FIXTURES]:
        comp = compile_bytes(raw)
        if not comp.ok:
            fails.append("%s: the front end refuses it (%s)" % (ident, comp.error.code))
            continue
        laws.append((ident, comp.law))
        try:
            L = read(comp.law)
        except Refused as r:
            fails.append("%s refused, %s" % (ident, r))
            continue
        passed += 1
        if write(L) == comp.law:                # draft 7, M10: the write-back compared, byte for byte, on every law
            exact += 1
        else:
            fails.append("%s: written back otherwise than read" % ident)
        for k in range(1, L.n + 1):
            deepest = max(deepest, paren_depth(L.clauses[k]["line"]))
        a, b = analysis_view(comp), law_view(L)
        diff = [k for k in a if a[k] != b[k]]
        if diff:
            fails.append("%s: derivations differ from the analysis's: %s" % (ident, diff))
        else:
            same += 1
    total = len(texts) + len(FIXTURES)
    say("read, W1-W14 passed: %d of %d; written back exactly (write() compared byte for byte with the bytes read): %d "
        "of %d" % (passed, total, exact, total))
    say("derivations equal to the analysis's (top, children, labels, vars with type and top, rule types, rules, "
        "overrides, claim sites, cost-tracked clauses): %d of %d" % (same, total))
    say("the deepest nesting of parentheses on any clause line in them: %d (W14(c)'s bound: %d)" % (deepest, DEPTH_PARENS))
    for f in fails:
        say("   FAIL %s" % f)
    say()
    say("== the byte fixtures (draft 2's and 4's), which the format accepts and no text writes")
    for name, raw in BYTE_FIXTURES:
        try:
            Lb = read(raw)
            ok = write(Lb) == raw
            say("   %-48s accepted, written back %s" % (name, "exactly" if ok else "DIFFERENTLY"))
            if not ok:
                fails.append("%s: not written back exactly" % name)
        except Refused as r:
            say("   %-48s REFUSED %s" % (name, r))
            fails.append("%s refused, %s" % (name, r))
    say()
    say("== plants: each refused on the line and by the W section 8 chooses")
    caught = run = 0
    for w, line, what, kind in PLANTS:
        ident, bad, want_line = plant_bytes(laws, kind)
        want_line = want_line if want_line is not None else line
        if bad is None:
            say("   W%-2d %-58s NOT RUN: no law holds its site" % (w, what))
            continue
        run += 1
        try:
            read(bad)
            got, gline = "accepted", None
        except Refused as r:
            got, gline = "W%d" % r.w, r.line
        except RecursionError:                  # draft 3, H2: a crash is recorded as such, never as a refusal
            got, gline = "CRASHED (RecursionError)", None
        ok = got == "W%d" % w and gline == want_line
        caught += ok
        say("   W%-2d line %-3s %-58s on %-34s refused %s line %s: %s" % (
            w, want_line, what[:58], ident[:34], got, gline, "CAUGHT" if ok else "NOT AS STATED"))
    say()
    held = not fails and caught == run == len(PLANTS) and exact == passed == total
    say("FORMAT CHECK (DRAFT 9) %s: %d of %d laws pass, %d written back exactly, derivations equal on %d; plants %d of "
        "%d caught, %d not run" % ("HELD" if held else "FAILED", passed, total, exact, same, caught, run,
                                   len(PLANTS) - run))
    sys.exit(0 if held else 1)


if __name__ == "__main__":
    main()

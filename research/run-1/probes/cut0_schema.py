"""EXPERIMENTAL RESEARCH PROBE. It is not the contract or the trace format, and nothing in the program reads it; the
proposal it supports is research/run-1/CUT-SCHEMA.md, and its output is evidence/run1-cut0-schema.txt.

Draft 2 of the refusal cut's bytes, derived from CUT-0's rule as written (research/run-1/CUT-0.md section 2), held to
the shapes the interpreter can produce, and tested against the cases, the frozen texts and the manifold debate's two
families of laws. Draft 1, the first form, is kept below for the comparison only.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/cut0_schema.py

  payload := u8 len(code) || code || u16 nframes || frame*                                       (big-endian)
  frame   := u32 clause || u16 sel || [u8 more: a For that is not the last frame] || [u16 arm: an If that is the last]
     sel  = 0xFFFF: the clause's own statement; otherwise k: arm k's inline statement of the If chain the clause heads or
            belongs to (k = the number of conditions for the Otherwise arm)

What a frame carries beyond its statement is fixed by the statement's kind and the frame's place. The rule reads a For's
bit only below the top: refused at its own clause, the body follows whatever the bit (CUT-0.md, the For row). It reads an
If's refused arm only on top: an If below the top is running one arm's body, and the chain completes after it. Draft 1
put a flag byte on every frame and a bit on a top For. The rule reads neither.

The decoder holds the form to the shapes the interpreter's calls can produce (src/orlog/interp.py), and refuses each
rule's violation with its reason:
  S1 root      the first frame is a top-level clause's own statement (Interp.run calls seq on the top level);
  S2 nesting   each later frame is a statement the frame before it runs: a loop's child, the performed procedure's
               child, a block arm's child;
  S3 inline    an arm's inline statement follows its own If, and nothing else follows it there;
  S4 top kind  the last frame's statement can refuse at its own clause (version 0: never a Perform, interp.py 242-244);
  S5 ranges    a bit is 0 or 1; an arm names one of the If's conditions;
  S6 event     the 'R' event's clause is the last frame's clause, or, for an If, the refused condition's clause;
  S7 code      a code that one statement kind alone raises names a last frame of that kind;
then the code registry (computed from the source), the count, no trailing bytes, and encode(decode(b)) == b.

The shapes are also generated the other way, from the top down, the way Interp.seq, body and stmt call (a Perform through
its s.proc, as Interp does). The decoder checks parents from the bottom up. The two are written apart, by one author.

Checks:
- every refused run: its cut decodes to the live cut on every field the bytes hold, K-hat is equal, and the cut is a
  generated shape;
- the shapes of each case's program: encode and decode are inverse on every one of them;
- byte mutations (every value at every offset, every deletion, duplication, insertion and truncation) and frame
  forgeries (every frame deleted, substituted or inserted): none accepted outside the generated shapes. Each accepted
  one is classed: a position this run passed through, or a shape the form admits that this run never reached;
- the event clause and the code: every other clause and every registered code tried on every frozen run's cut;
- each field has a role: dropping it changes a named claim's standing, printed as a witness;
- each shape rule is needed: dropping it lets a forgery outside the shapes through, or is an equivalent mutant, said;
- draft 1 on the same forgeries, and its 15 accepted single-byte mutations, classed.
"""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "manifold"))
import cut0_claims as C                                          # noqa: E402
from orlog.front import compile_bytes                            # noqa: E402
from orlog.interp import HostStop                                 # noqa: E402
from orlog.syntax import (BLOCK, Claim, Decimals, Define, For, IfS, Must, Perform, ProcDef, RemoveLast, Say,  # noqa
                          While)

VERSION = 0
OWN = 0xFFFF
PLANT = None
FIELD_PLANTS = ("top-only", "no-for-bit", "first-arm", "no-refused-arm")     # a field dropped from the bytes
SHAPE_PLANTS = ("no-root", "no-nest", "no-inline", "no-top-kind", "no-range", "no-event", "no-code-kind",
                "no-roundtrip")                                                 # a decoder rule dropped
NEUTRAL = "DIVISION-BY-ZERO"     # a code any statement kind may raise: forgeries carry it, so S7 never decides them
PORTS = set()                    # version-1 stand-ins only: the clause ids that stand for port declarations
V1_CODES = {"TICK-BUDGET"}       # version 1's one new run code (the budget, R9 as ruled B1-B4)

with open(os.path.join(ROOT, "src", "orlog", "interp.py"), "rb") as _fh:
    INTERP = _fh.read().decode("utf-8")
with open(os.path.join(ROOT, "src", "orlog", "numeric_ref.py"), "rb") as _fh:
    NUMERIC = _fh.read().decode("utf-8")
LITERAL = re.findall(r'refuse\("([A-Z-]+)"', INTERP)
NUMERIC_CODES = re.findall(r'Refusal\("([A-Z-]+)"', NUMERIC)
CODES = set(LITERAL) | set(NUMERIC_CODES)
DRAFT1_CODES = {"CLAIM-REFUTED", "EMPTY-LIST", "FUEL-EXHAUSTED", "INDEX-OUT-OF-RANGE", "INEXACT-CONVERSION",
                "LIST-TOO-LONG", "MUST-FAILED", "NEGATIVE-LENGTH", "NOT-FINITE", "OUTPUT-TOO-LONG", "RULE-CONFLICT",
                "RULE-UNDEFINED", "TEXT-TOO-LONG", "DIVISION-BY-ZERO", "INEXACT-DIVISION", "NEGATIVE-SQRT",
                "OVERFLOW"}
ONE_KIND = {"CLAIM-REFUTED": Claim, "MUST-FAILED": Must, "FUEL-EXHAUSTED": While, "OUTPUT-TOO-LONG": Say,
            "EMPTY-LIST": RemoveLast}


class Malformed(Exception):
    pass


def raised_in(code):
    """(the statement kind whose branch raises code, its line) when interp.py raises it once and numeric_ref never."""
    lines = INTERP.split("\n")
    at = [i for i, l in enumerate(lines) if 'refuse("%s"' % code in l]
    if len(at) != 1 or code in NUMERIC_CODES:
        return None
    for j in range(at[0], -1, -1):
        m = re.search(r"isinstance\(s, (\w+)\)", lines[j])
        if m:
            return m.group(1), at[0] + 1
    return None


def executable(st):
    return not isinstance(st, (ProcDef, Define, Decimals))


def head_if(prog, c):
    """The clause of the If chain an absorbed Otherwise clause belongs to; c itself otherwise."""
    if not c.absorbed:
        return c
    sib = c.parent.children if c.parent is not None else prog.top
    i = sib.index(c)
    while sib[i].absorbed:
        i -= 1
    return sib[i]


def arms(st):
    """The If chain's arms as (body, clause), the Otherwise arm last. This numbering is the selector's definition."""
    out = [(b, k) for _, b, k in st.arms]
    if st.els is not None:
        out.append(st.els)
    return out


def is_block(b):
    return isinstance(b, tuple) and b[0] == BLOCK


def sel_of(prog, c, s):
    if s is c.stmt and not c.absorbed:
        return OWN
    for k, (b, ac) in enumerate(arms(head_if(prog, c).stmt)):
        if b is s and ac is c:
            return k
    raise AssertionError("a frame's statement is neither its clause's nor an inline arm's")


def key_of(prog, frames):
    """The cut as draft 2's bytes hold it: per frame (clause id, sel, bit, arm); the bit only for a For below the top,
    the arm only for an If on top."""
    out, n = [], len(frames)
    for i, f in enumerate(frames):
        c, s, last = f["clause"], f["stmt"], i == n - 1
        bit = int(bool(f["more"])) if isinstance(s, For) and not last else None
        arm = f["arm"] if isinstance(s, IfS) and last else None
        out.append((c.id, sel_of(prog, c, s), bit, arm))
    return tuple(out)


# ------------------------------------------------------------------------------------------------ draft 2: the bytes
def encode(prog, cut, code):
    frames = cut[-1:] if PLANT == "top-only" else cut
    out = [bytes([len(code)]), code.encode("ascii"), struct.pack(">H", len(frames))]
    for i, f in enumerate(frames):
        c, s, last = f["clause"], f["stmt"], i == len(frames) - 1
        sel = sel_of(prog, c, s)
        if PLANT == "first-arm" and sel != OWN:      # the selector's information dropped: only "an inline statement"
            sel = next(j for j, (bb, ac) in enumerate(arms(head_if(prog, c).stmt)) if ac is c and not is_block(bb))
        out.append(struct.pack(">IH", c.id, sel))
        if isinstance(s, For) and not last and PLANT != "no-for-bit":
            out.append(bytes([int(bool(f["more"]))]))
        if isinstance(s, IfS) and last and PLANT != "no-refused-arm":
            out.append(struct.pack(">H", f["arm"]))
    return b"".join(out)


def encode_key(code, key):
    """Bytes from a key, with no check at all: the forger's encoder."""
    out = [bytes([len(code)]), code.encode("ascii"), struct.pack(">H", len(key))]
    for cid, sel, bit, arm in key:
        out.append(struct.pack(">IH", cid, sel))
        if bit is not None:
            out.append(bytes([bit]))
        if arm is not None:
            out.append(struct.pack(">H", arm))
    return b"".join(out)


def statement(prog, c, sel):
    if sel == OWN:
        if c.absorbed or not executable(c.stmt):
            raise Malformed("selector")
        return c.stmt
    head = head_if(prog, c)
    if not isinstance(head.stmt, IfS):
        raise Malformed("selector")
    ar = arms(head.stmt)
    if sel >= len(ar) or ar[sel][1] is not c or is_block(ar[sel][0]):
        raise Malformed("selector")
    return ar[sel][0]


def follows(prog, outer, inner):
    """S2 and S3, by the clauses' parents: whether inner (clause, statement, sel) may directly follow outer."""
    oc, os_ = outer[0], outer[1]
    ic, isel = inner[0], inner[2]
    if isel != OWN and PLANT != "no-inline":
        return isinstance(os_, IfS) and head_if(prog, ic) is oc
    if PLANT == "no-nest":
        return True
    if isinstance(os_, (For, While)):
        return ic.parent is oc
    if isinstance(os_, Perform):
        procs = {x.stmt.name: x for x in prog.top if isinstance(x.stmt, ProcDef)}
        return ic.parent is procs[os_.name]
    if isinstance(os_, IfS):
        return ic.parent is not None and any(is_block(b) and b[1] is ic.parent for b, _ in arms(os_))
    return False


def decode(prog, b, event_clause=None):
    """The cut a payload names, as frames {clause, stmt, more, arm}, or Malformed with its reason."""
    by_id = {c.id: c for c in prog.clauses}
    field_plant = PLANT in FIELD_PLANTS
    try:
        n = b[0]
        code = b[1:1 + n].decode("ascii")
        if len(code) != n or code not in (CODES | V1_CODES if VERSION == 1 else CODES):
            raise Malformed("code")
        pos = 1 + n
        (count,) = struct.unpack_from(">H", b, pos)
        pos += 2
        if count == 0:
            raise Malformed("no frame")
        frames, prev = [], None
        for i in range(count):
            last = i == count - 1
            cid, sel = struct.unpack_from(">IH", b, pos)
            pos += 6
            c = by_id.get(cid)
            if c is None:
                raise Malformed("clause")
            s = statement(prog, c, sel)
            if PLANT == "top-only":
                pass
            elif i == 0:
                if PLANT != "no-root" and (sel != OWN or c.parent is not None):
                    raise Malformed("not rooted")                                   # S1
            elif not follows(prog, prev, (c, s, sel)):
                raise Malformed("not nested")                                       # S2, S3
            more = arm = None
            if isinstance(s, For) and not last:
                if PLANT == "no-for-bit":
                    more = True
                else:
                    bit = b[pos]
                    pos += 1
                    if bit > 1 and PLANT != "no-range":
                        raise Malformed("bit")                                      # S5
                    more = bool(bit)
            elif isinstance(s, While):
                more = True
            if isinstance(s, IfS) and last and PLANT != "no-refused-arm":
                (arm,) = struct.unpack_from(">H", b, pos)
                pos += 2
                if arm >= len(s.arms) and PLANT != "no-range":
                    raise Malformed("arm")                                          # S5
            frames.append({"clause": c, "stmt": s, "more": more, "arm": arm})
            prev = (c, s, sel)
        if pos != len(b):
            raise Malformed("trailing bytes")
    except (IndexError, struct.error, UnicodeDecodeError):
        raise Malformed("truncated")
    top = frames[-1]
    ts = top["stmt"]
    if VERSION == 0 and isinstance(ts, Perform) and PLANT != "no-top-kind":
        raise Malformed("top kind")                                                 # S4
    if VERSION == 1 and top["clause"].id in PORTS and PLANT != "no-top-kind":
        raise Malformed("top kind")                     # S4, version 1: a port declaration cannot refuse (F20.3)
    if event_clause is not None and PLANT != "no-event":
        if isinstance(ts, IfS) and top["arm"] is not None and top["arm"] < len(ts.arms):
            want = ts.arms[top["arm"]][2].id
        else:
            want = top["clause"].id
        if event_clause != want:
            raise Malformed("event clause")                                         # S6
    if code in ONE_KIND and not isinstance(ts, ONE_KIND[code]) and PLANT != "no-code-kind":
        raise Malformed("code kind")                                                # S7
    if not field_plant and PLANT != "no-roundtrip" and encode(prog, frames, code) != b:
        raise Malformed("not canonical")
    return code, frames


# ------------------------------------------------------------------------- the shapes, generated from the top down
def seq_positions(clauses):
    return [(c, c.stmt, OWN) for c in clauses if not c.absorbed and executable(c.stmt)]


def inner(pos):
    """What a frame's statement runs next, as Interp.stmt and body call it."""
    c, s, _ = pos
    if isinstance(s, (For, While)):
        return seq_positions(c.children)
    if isinstance(s, Perform):
        return seq_positions(s.proc.children)
    if isinstance(s, IfS):
        out = []
        for j, (b, ac) in enumerate(arms(s)):
            out += seq_positions(b[1].children) if is_block(b) else [(ac, b, j)]
        return out
    return []


def can_top(s, c=None):
    if VERSION == 1 and c is not None and c.id in PORTS:
        return False
    return not (VERSION == 0 and isinstance(s, Perform))


def shapes(prog):
    """Every cut shape, as keys: finite, because version 0 refuses recursion."""
    out = []

    def walk(prefix, pos):
        c, s, sel = pos
        if can_top(s, c):
            if isinstance(s, IfS):
                out.extend(prefix + ((c.id, sel, None, a),) for a in range(len(s.arms)))
            else:
                out.append(prefix + ((c.id, sel, None, None),))
        for nxt in inner(pos):
            for bit in ((0, 1) if isinstance(s, For) else (None,)):
                walk(prefix + ((c.id, sel, bit, None),), nxt)
    for p in seq_positions(prog.top):
        walk((), p)
    return out


def in_shapes(prog, key):
    """Membership in shapes(prog), walked along the key without enumerating them."""
    cands = seq_positions(prog.top)
    for i, (cid, sel, bit, arm) in enumerate(key):
        last = i == len(key) - 1
        hit = [p for p in cands if p[0].id == cid and p[2] == sel]
        if len(hit) != 1:
            return False
        s = hit[0][1]
        if isinstance(s, For) and not last:
            if bit not in (0, 1):
                return False
        elif bit is not None:
            return False
        if isinstance(s, IfS) and last:
            if arm is None or not 0 <= arm < len(s.arms):
                return False
        elif arm is not None:
            return False
        if last:
            return can_top(s, hit[0][0])
        cands = inner(hit[0])
    return False


def alphabet(prog):
    """Every statement position of a program: each clause's own statement and each inline arm statement."""
    out = []
    for c in prog.clauses:
        if not c.absorbed and executable(c.stmt):
            out.append((c, c.stmt, OWN))
            if isinstance(c.stmt, IfS):
                out += [(ac, b, j) for j, (b, ac) in enumerate(arms(c.stmt)) if not is_block(b)]
    return out


def keys_for(positions):
    """Every key over a list of positions, the bit and the arm placed as draft 2 places them, with every value."""
    out = [()]
    for i, (c, s, sel) in enumerate(positions):
        last = i == len(positions) - 1
        opts = [(None, None)]
        if isinstance(s, For) and not last:
            opts = [(0, None), (1, None)]
        elif isinstance(s, IfS) and last:
            opts = [(None, a) for a in range(len(s.arms))]
        out = [k + ((c.id, sel, bt, am),) for k in out for bt, am in opts]
    return out


def forgeries(prog, positions):
    """Every position list one frame edit away: a frame deleted, substituted or inserted."""
    alpha = alphabet(prog)
    n = len(positions)
    out = [positions[:i] + positions[i + 1:] for i in range(n) if n > 1]
    out += [positions[:i] + [a] + positions[i + 1:] for i in range(n) for a in alpha
            if (a[0], a[2]) != (positions[i][0], positions[i][2])]
    out += [positions[:i] + [a] + positions[i:] for i in range(n + 1) for a in alpha]
    return out


# --------------------------------------------------------------------------------------------------- the runs
class Witness(C.CutInterp):
    """The reference instrumented once more: every position at which this run could have refused (each expression it
    evaluates; each statement it starts that can refuse at its own clause), as keys."""

    def __init__(self, *a, **k):
        C.CutInterp.__init__(self, *a, **k)
        self.seen = set()

    def eval(self, cid, e):
        self.seen.add(key_of(self.prog, self.frames))
        return C.CutInterp.eval(self, cid, e)

    def stmt(self, c, s):
        if executable(s) and not isinstance(s, (IfS, Perform)):
            self.seen.add(key_of(self.prog, self.frames + [{"clause": c, "stmt": s, "more": None, "arm": None}]))
        return C.CutInterp.stmt(self, c, s)


def run_cut(raw, budget=10 ** 8, cls=None):
    """(compiled law, the live cut, the code, the 'R' event's clause, the interpreter) of a refused run, or None."""
    comp = compile_bytes(raw)
    if not comp.ok:
        return None
    it = (cls or C.CutInterp)(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget)
    try:
        it.run()
    except HostStop:
        return None
    if it.cut is None:
        return None
    p = it.status.split(" ")
    return comp, it.cut, p[1], int(p[2]), it


def new_stats():
    return {"refused": 0, "refused_own": 0, "key_differs": 0, "k_differs": 0, "not_a_shape": 0, "open": 0,
            "top_for": 0, "top_if": 0, "bytes": 0, "frames": 0}


def check(raw, stats, budget=10 ** 8, keep=None):
    r = run_cut(raw, budget)
    if r is None:
        return
    comp, cut, code, ec, _ = r
    stats["refused"] += 1
    b = encode(comp.prog, cut, code)
    stats["bytes"] = max(stats["bytes"], len(b))
    stats["frames"] = max(stats["frames"], len(cut))
    live = key_of(comp.prog, cut)
    assert encode_key(code, live) == b
    stats["not_a_shape"] += not in_shapes(comp.prog, live)
    top = cut[-1]["stmt"]
    stats["open"] += isinstance(top, Claim)
    stats["top_for"] += isinstance(top, For)
    stats["top_if"] += isinstance(top, IfS)
    try:
        dcode, frames = decode(comp.prog, b, ec)
    except Malformed as e:
        stats["refused_own"] += 1
        stats.setdefault("first_refused_own", str(e))
        return
    if key_of(comp.prog, frames) != live or dcode != code:
        stats["key_differs"] += 1
    if C.continuation(comp.prog, frames) != C.continuation(comp.prog, cut):
        stats["k_differs"] += 1
    if keep is not None:
        keep.append((comp, cut, code, ec))


def standing(done, k):
    return {i: done[i] and i not in k for i in done}


def done_of(raw):
    _, out, _ = C.judge(raw)
    return {i: v[5] for i, v in out.items()}


# --------------------------------------------------------------------------------------------- the corpora
def mutate_bytes(b, full):
    """Every replacement (by every other value when full, else by 0, 1, 2, 3, 0x7F, 0xFF and b ^ 1), deletion,
    duplication, insertion (by every value when full) and proper prefix."""
    out = []
    for i in range(len(b)):
        vals = range(256) if full else sorted({0, 1, 2, 3, 0x7F, 0xFF, b[i] ^ 1})
        out += [b[:i] + bytes([v]) + b[i + 1:] for v in vals if v != b[i]]
        out += [b[:i] + b[i + 1:], b[:i] + b[i:i + 1] + b[i:]]
    for i in range(len(b) + 1):
        out += [b[:i] + bytes([v]) + b[i:] for v in (range(256) if full else (0, 1, 0xFF))]
    out += [b[:i] for i in range(len(b))]
    return out


def accepted_outside(prog, payloads, ec=None):
    """(tried, accepted, accepted outside the shapes, accepted not canonical, the accepted keys)."""
    tried = acc = outside = bad = 0
    keys = []
    for v in payloads:
        tried += 1
        try:
            dcode, frames = decode(prog, v, ec)
        except Malformed:
            continue
        acc += 1
        k = key_of(prog, frames)
        if encode_key(dcode, k) != v:
            bad += 1
        if not in_shapes(prog, k):
            outside += 1
        keys.append((v, k))
    return tried, acc, outside, bad, keys


def case_programs():
    out = []
    for name, raw, want, _ in C.CASES:
        comp, cut, code, ec, it = run_cut(raw, cls=Witness)
        out.append((name.split(" ")[0], raw, want, comp, cut, code, ec, it.seen))
    return out


def forgery_corpus(progs):
    """Frame forgeries one edit from every case's live cut and from every shape of its program, under NEUTRAL, with
    every value of the bit and the arm: (tried, accepted, accepted outside the shapes)."""
    tried = acc = outside = 0
    for _, _, _, comp, cut, _, _, _ in progs:
        prog = comp.prog
        by_id = {c.id: c for c in prog.clauses}
        bases = [[(f["clause"], f["stmt"], sel_of(prog, f["clause"], f["stmt"])) for f in cut]]
        for sh in shapes(prog):
            bases.append([(by_id[cid], statement(prog, by_id[cid], sel), sel) for cid, sel, _, _ in sh])
        seen = set()
        for base in bases:
            for pl in forgeries(prog, base):
                for k in keys_for(pl):
                    if k in seen:
                        continue
                    seen.add(k)
                    t, a, o, _, _ = accepted_outside(prog, [encode_key(NEUTRAL, k)])
                    tried, acc, outside = tried + t, acc + a, outside + o
    return tried, acc, outside


def shape_mutation_corpus(progs):
    """Byte mutations of every shape of every case's program, under NEUTRAL."""
    tried = acc = outside = bad = 0
    for _, _, _, comp, _, _, _, _ in progs:
        for sh in shapes(comp.prog):
            t, a, o, x, _ = accepted_outside(comp.prog, mutate_bytes(encode_key(NEUTRAL, sh), False))
            tried, acc, outside, bad = tried + t, acc + a, outside + o, bad + x
    return tried, acc, outside, bad


def live_mutation_corpus(progs):
    """Byte mutations of every case's own payload, with its own code and event clause: each accepted one classed."""
    tried = acc = outside = bad = passed = differs = 0
    for _, raw, _, comp, cut, code, ec, seen in progs:
        b = encode(comp.prog, cut, code)
        done = done_of(raw)
        live_k = standing(done, C.continuation(comp.prog, cut))
        t, a, o, x, keys = accepted_outside(comp.prog, mutate_bytes(b, True), ec)
        tried, acc, outside, bad = tried + t, acc + a, outside + o, bad + x
        for v, k in keys:
            passed += k in seen
            frames = decode(comp.prog, v, ec)[1]
            differs += standing(done, C.continuation(comp.prog, frames)) != live_k
    return tried, acc, outside, bad, passed, differs


def event_corpus(kept):
    """Every clause of the program, and one that does not exist, as the 'R' event's clause of every kept cut."""
    tried = wrong_acc = right_ref = 0
    for comp, cut, code, ec in kept:
        b = encode(comp.prog, cut, code)
        for cid in [c.id for c in comp.prog.clauses] + [max(c.id for c in comp.prog.clauses) + 1]:
            tried += 1
            try:
                decode(comp.prog, b, cid)
                wrong_acc += cid != ec
            except Malformed:
                right_ref += cid == ec
    return tried, wrong_acc, right_ref


def code_corpus(kept):
    """Every registered code on every kept cut: accepted exactly when S7 allows it."""
    tried = incoherent_acc = coherent_ref = 0
    for comp, cut, code, ec in kept:
        top = cut[-1]["stmt"]
        for cd in sorted(CODES):
            tried += 1
            coherent = cd not in ONE_KIND or isinstance(top, ONE_KIND[cd])
            try:
                decode(comp.prog, encode(comp.prog, cut, cd), ec)
                incoherent_acc += not coherent
            except Malformed:
                coherent_ref += coherent
    return tried, incoherent_acc, coherent_ref


# --------------------------------------------------------------------- draft 1, kept for the comparison only
def encode_d1(frames_flags, code):
    out = [bytes([len(code)]), code.encode("ascii"), struct.pack(">H", len(frames_flags))]
    for (c, s, sel), flag, arm in frames_flags:
        out.append(struct.pack(">IHB", c.id, sel, flag))
        if flag == 3:
            out.append(struct.pack(">H", arm))
    return b"".join(out)


def encode_d1_live(prog, cut, code):
    ff = []
    for f in cut:
        c, s = f["clause"], f["stmt"]
        if isinstance(s, For):
            flag = 4 if f["more"] is None else (1 if f["more"] else 2)
        elif isinstance(s, IfS) and f["arm"] is not None:
            flag = 3
        else:
            flag = 0
        ff.append(((c, s, sel_of(prog, c, s)), flag, f["arm"]))
    return encode_d1(ff, code)


def nested_d1(prog, outer, inner_):
    oc, os_ = outer
    ic, is_ = inner_
    if ic is oc or (ic.absorbed and head_if(prog, ic) is oc):
        return isinstance(os_, IfS) and not isinstance(is_, IfS) and is_ is not ic.stmt
    if isinstance(os_, (For, While)):
        return ic.parent is oc
    if isinstance(os_, IfS):
        return ic.parent is not None and any(k is ic.parent for _, k in arms(os_)) and ic.parent in (
            [k for b, k in arms(os_) if isinstance(b, tuple) and b[0] == BLOCK])
    if isinstance(os_, Perform):
        procs = {x.stmt.name: x for x in prog.top if isinstance(x.stmt, ProcDef)}
        return ic.parent is procs[os_.name]
    return False


def decode_d1(prog, b):
    """Draft 1's decoder as it stood: (code, [(clause, stmt, sel, flag, arm)]) or Malformed."""
    by_id = {c.id: c for c in prog.clauses}
    try:
        n = b[0]
        code = b[1:1 + n].decode("ascii")
        if len(code) != n or code not in DRAFT1_CODES:
            raise Malformed("code")
        pos = 1 + n
        (count,) = struct.unpack_from(">H", b, pos)
        pos += 2
        if count == 0:
            raise Malformed("no frame")
        frames = []
        for i in range(count):
            cid, sel, flag = struct.unpack_from(">IHB", b, pos)
            pos += 7
            c = by_id.get(cid)
            if c is None:
                raise Malformed("clause")
            if sel == OWN:
                if c.absorbed or isinstance(c.stmt, (ProcDef, Define, Decimals)):
                    raise Malformed("selector")
                s = c.stmt
            else:
                head = head_if(prog, c)
                if not isinstance(head.stmt, IfS):
                    raise Malformed("selector")
                ar = arms(head.stmt)
                if sel >= len(ar) or ar[sel][1] is not c or isinstance(ar[sel][0], tuple):
                    raise Malformed("selector")
                s = ar[sel][0]
            arm = None
            if isinstance(s, For):
                if flag not in (1, 2, 4):
                    raise Malformed("flag")
            elif flag == 3:
                if not isinstance(s, IfS) or i != count - 1:
                    raise Malformed("flag")
                (arm,) = struct.unpack_from(">H", b, pos)
                pos += 2
                if arm >= len(s.arms):
                    raise Malformed("arm")
            elif flag != 0:
                raise Malformed("flag")
            frames.append((c, s, sel, flag, arm))
        if pos != len(b):
            raise Malformed("trailing bytes")
    except (IndexError, struct.error, UnicodeDecodeError):
        raise Malformed("truncated")
    if frames[0][0].parent is not None:
        raise Malformed("not rooted")
    for o, i in zip(frames, frames[1:]):
        if not nested_d1(prog, (o[0], o[1]), (i[0], i[1])):
            raise Malformed("not nested")
    if encode_d1([((c, s, sel), flag, arm) for c, s, sel, flag, arm in frames], code) != b:
        raise Malformed("not canonical")
    return code, frames


def key_d1(frames):
    """A draft-1 cut as a draft-2 key, or None for a state the rule cannot be in: a bit on a top For, flag 4 below the
    top, a top If without its arm."""
    out, n = [], len(frames)
    for i, (c, s, sel, flag, arm) in enumerate(frames):
        last = i == n - 1
        bit = None
        if isinstance(s, For):
            if (last and flag != 4) or (not last and flag == 4):
                return None
            bit = None if last else int(flag == 1)
        if isinstance(s, IfS) and last and flag != 3:
            return None
        out.append((c.id, sel, bit, arm if isinstance(s, IfS) and last else None))
    return tuple(out)


def d1_flag_variants(positions):
    out = [()]
    for i, (c, s, sel) in enumerate(positions):
        last = i == len(positions) - 1
        if isinstance(s, For):
            opts = [(1, None), (2, None), (4, None)]
        elif isinstance(s, IfS) and last:
            opts = [(0, None)] + [(3, a) for a in range(len(s.arms))]
        else:
            opts = [(0, None)]
        out = [k + (((c, s, sel), fl, am),) for k in out for fl, am in opts]
    return out


def draft1_comparison(progs):
    """Draft 1 on its own single-byte mutations of the cases (its 3,812) and on the frame forgeries."""
    print("== draft 1, for the comparison: its own single-byte mutations of the cases, each accepted one classed")
    tried = refused = 0
    classes = {"outside the shapes": 0, "a shape this run passed through": 0, "a shape this run never reached": 0}
    for name, raw, _, comp, cut, code, ec, seen in progs:
        b = encode_d1_live(comp.prog, cut, code)
        for i in range(len(b)):
            variants = [("%02x" % v, b[:i] + bytes([v]) + b[i + 1:]) for v in (0, 1, 3, 255) if v != b[i]]
            variants += [("deleted", b[:i] + b[i + 1:]), ("duplicated", b[:i] + b[i:i + 1] + b[i:])]
            for what, v in variants:
                tried += 1
                try:
                    _, frames = decode_d1(comp.prog, v)
                except Malformed:
                    refused += 1
                    continue
                k = key_d1(frames)
                if k is None or not in_shapes(comp.prog, k):
                    cls = "outside the shapes"
                elif k in seen:
                    cls = "a shape this run passed through"
                else:
                    cls = "a shape this run never reached"
                classes[cls] += 1
                print("   %-4s offset %2d: %02x -> %-10s %s" % (name, i, b[i], what, cls))
    print("   tried %d: refused %d, accepted %d: %s" % (tried, refused, tried - refused,
                                                        "; ".join("%s %d" % kv for kv in classes.items())))
    ftried = facc = fout = 0
    why = {"a flag state no run reaches": 0}
    for _, _, _, comp, cut, _, _, _ in progs:
        prog = comp.prog
        base = [(f["clause"], f["stmt"], sel_of(prog, f["clause"], f["stmt"])) for f in cut]
        seen_k = set()
        for pl in forgeries(prog, base) + [base]:
            for ff in d1_flag_variants(pl):
                sig = tuple((p[0].id, p[2], fl, am) for p, fl, am in ff)
                if sig in seen_k:
                    continue
                seen_k.add(sig)
                ftried += 1
                try:
                    _, frames = decode_d1(prog, encode_d1(ff, NEUTRAL))
                except Malformed:
                    continue
                facc += 1
                k = key_d1(frames)
                if k is None:
                    why["a flag state no run reaches"] += 1
                elif not in_shapes(prog, k):
                    try:
                        decode(prog, encode_key(NEUTRAL, k))
                        reason = "accepted by draft 2 too"
                    except Malformed as e:
                        reason = "draft 2: %s" % e
                    why[reason] = why.get(reason, 0) + 1
                else:
                    continue
                fout += 1
    print("   frame forgeries one edit from each case's live cut, every flag value: tried %d, accepted %d, outside the "
          "shapes %d (%s)" % (ftried, facc, fout, "; ".join("%s %d" % kv for kv in sorted(why.items()))))
    return classes["outside the shapes"], fout


# ---------------------------------------------------------------------------------------------------- the run
def reading(raw):
    """(each claim's standing from the decoded cut, the payload, K-hat)."""
    comp, cut, code, ec, _ = run_cut(raw)
    b = encode(comp.prog, cut, code)
    frames = decode(comp.prog, b, None if PLANT in FIELD_PLANTS else ec)[1]
    k = C.continuation(comp.prog, frames)
    return standing(done_of(raw), k), b, k


def main():
    global PLANT
    import resume_oracle as O
    ok = True
    print("== the code registry, computed from the source")
    print("   interp.py raises %d codes, numeric_ref.py %d; %d in all; draft 1's hand list %s" % (
        len(set(LITERAL)), len(set(NUMERIC_CODES)), len(CODES), "equal" if CODES == DRAFT1_CODES else "DIFFERS"))
    for code, kind in sorted(ONE_KIND.items()):
        r = raised_in(code)
        good = r is not None and r[0] == kind.__name__
        ok &= good
        print("   S7 %-16s raised once, in %s's branch (interp.py:%s)%s" % (
            code, r[0] if r else "?", r[1] if r else "?", "" if good else "  NOT AS STATED"))
    ok &= CODES == DRAFT1_CODES

    print("== the probe's cases: the decoded cut is the live cut, and every claim reads as the live frames read it")
    progs = case_programs()
    bad = 0
    for name, raw, want, comp, cut, code, ec, seen in progs:
        got = reading(raw)[0]
        wants = want if isinstance(want, dict) else {k: want for k in got}
        b = encode(comp.prog, cut, code)
        same = got == wants and key_of(comp.prog, decode(comp.prog, b, ec)[1]) == key_of(comp.prog, cut)
        bad += not same
        print("   %-5s %s  %2d bytes  %s" % (name, "as live" if same else "DIFFERS", len(b), b.hex()))
    ok &= bad == 0

    print("== every refused run: the cases, COMPAT-0's frozen texts, the fixtures and the examples")
    st, kept = new_stats(), []
    for ident, raw, budget in C.corpus():
        check(raw, st, budget, kept)
    print("   %s" % st)
    print("== the manifold debate's families (research/run-1/manifold/resume_oracle.py's generators)")
    fam = {}
    for which, templates in (("E", O.family_e()), ("G", O.family_g(10000, 26102026))):
        s = new_stats()
        for nodes in templates:
            for c in O.CS:
                check(O.render(nodes, c), s, O.BUDGET)
        fam[which] = s
        print("   family %s: %s" % (which, {k: v for k, v in s.items() if not k.startswith("first")}))
    totals = {k: st[k] + fam["E"][k] + fam["G"][k] for k in new_stats()}
    ok &= all(totals[k] == 0 for k in ("refused_own", "key_differs", "k_differs", "not_a_shape"))

    print("== the shapes of each case's program: encode and decode inverse on every one")
    nshapes = inv_bad = 0
    for _, _, _, comp, _, _, _, _ in progs:
        for sh in shapes(comp.prog):
            nshapes += 1
            try:
                inv_bad += key_of(comp.prog, decode(comp.prog, encode_key(NEUTRAL, sh))[1]) != sh
            except Malformed:
                inv_bad += 1
    print("   %d shapes over %d programs; %d not inverse" % (nshapes, len(progs), inv_bad))
    ok &= inv_bad == 0

    print("== byte mutations of each case's own payload (every value, every offset), its code and event clause")
    lt, la, lo, lb, lp, ld = live_mutation_corpus(progs)
    print("   tried %d: accepted %d, outside the shapes %d, not canonical %d; of the accepted, positions this run "
          "passed through %d, shapes it never reached %d; deciding otherwise than the live cut %d" % (
              lt, la, lo, lb, lp, la - lp, ld))
    print("== byte mutations of every shape of every case's program")
    mt, ma, mo, mb = shape_mutation_corpus(progs)
    print("   tried %d: accepted %d, outside the shapes %d, not canonical %d" % (mt, ma, mo, mb))
    print("== frame forgeries: every frame deleted, substituted or inserted, from every live cut and every shape")
    ft, fa, fo = forgery_corpus(progs)
    print("   tried %d: accepted %d, outside the shapes %d" % (ft, fa, fo))
    print("== the event clause and the code, tried on every frozen run's cut")
    et, ewa, err = event_corpus(kept)
    print("   clauses tried %d: a wrong clause accepted %d, the right one refused %d" % (et, ewa, err))
    ct, cia, ccr = code_corpus(kept)
    print("   codes tried %d: an incoherent code accepted %d, a coherent one refused %d" % (ct, cia, ccr))
    ok &= lo == 0 and lb == 0 and mo == 0 and mb == 0 and fo == 0 and ewa == 0 and err == 0 and cia == 0 and ccr == 0

    print("== each field's role: dropped, it changes a named claim's standing (the witness)")
    roles = [("top-only", "C1'", "the frames below the top (the actual callers)"),
             ("no-for-bit", "C2'", "a For's passes-remain bit, below the top"),
             ("first-arm", "A23", "the selector of an inline statement"),
             ("no-refused-arm", "A09", "the top If's refused arm")]
    caught = 0
    for plant, case, field in roles:
        raw = [r for n, r, _, _ in C.CASES if n.split(" ")[0] == case][0]
        full, bfull, kfull = reading(raw)
        PLANT = plant
        try:
            got, bplant, kplant = reading(raw)
        except Malformed as e:
            got, bplant, kplant = "refused %s" % e, b"", set()
        PLANT = None
        hit = got != full and bfull != bplant     # a witness only when the bytes lack the field and a standing flips
        caught += hit
        print("   %-14s on %-4s (%s): %s" % (plant, case, field, "caught" if hit else "NOT CAUGHT"))
        if isinstance(got, dict):
            for i in sorted(full):
                if full[i] != got[i]:
                    print("      claim %d: %s with the field, %s without it" % (
                        i, "held" if full[i] else "withheld", "held" if got[i] else "withheld"))
            print("      K-hat %s with it, %s without; payload %s with it, %s without%s" % (
                sorted(kfull), sorted(kplant), bfull.hex(), bplant.hex(),
                "  THE SAME BYTES: the field was not dropped" if bfull == bplant else ""))
    ok &= caught == len(roles)

    print("== each shape rule is needed: dropped, a forgery outside the shapes or an incoherent record is accepted")
    rules = [("no-root", "S1"), ("no-nest", "S2"), ("no-inline", "S3"), ("no-top-kind", "S4"), ("no-range", "S5"),
             ("no-event", "S6"), ("no-code-kind", "S7"), ("no-roundtrip", "the round trip")]
    shape_caught = equivalent = 0
    for plant, rule in rules:
        PLANT = plant
        _, _, f_out = forgery_corpus(progs)
        _, _, l_out, l_bad, _, _ = live_mutation_corpus(progs)
        _, _, m_out, m_bad = shape_mutation_corpus(progs)
        _, e_wrong, _ = event_corpus(kept)
        _, c_incoh, _ = code_corpus(kept)
        PLANT = None
        by = ["%s (%d)" % (n, v) for n, v in (("forgeries", f_out), ("case mutations", l_out + l_bad),
                                              ("shape mutations", m_out + m_bad), ("event clauses", e_wrong),
                                              ("codes", c_incoh)) if v]
        if by:
            shape_caught += 1
            print("   %-13s %-16s caught by %s" % (plant, "(%s)" % rule, ", ".join(by)))
        else:
            equivalent += 1
            print("   %-13s %-16s EQUIVALENT in these corpora" % (plant, "(%s)" % rule))
    ok &= shape_caught + equivalent == len(rules) and shape_caught >= len(rules) - 1

    d1_outside_mut, d1_outside_forged = draft1_comparison(progs)

    print("CUT SCHEMA DRAFT 2 %s: %d refused runs, each decoding to its live cut (%d differ), a generated shape in every "
          "one; %d shapes, encode and decode inverse; %d byte mutations and %d frame forgeries, none accepted outside "
          "the shapes; %d of %d fields with a witness; %d of %d shape rules caught, %d equivalent; draft 1 accepted %d "
          "mutations and %d forgeries outside them" % (
              "HELD" if ok else "FAILED", totals["refused"], totals["key_differs"] + totals["k_differs"], nshapes,
              lt + mt, ft, caught, len(roles), shape_caught, len(rules), equivalent, d1_outside_mut,
              d1_outside_forged))
    return 0 if ok else 1


# ------------------------------------------------- version 1's frames, on version-0 stand-ins (added 2026-10-29)
# His rulings of 2026-10-29: F20.3 (the tick block a plain frame, no frame for a port declaration, a Perform able to be
# the last frame), F20.4 (an If-condition refusal names the arm), and B1-B4 (TICK-BUDGET at the operation that makes a
# tick's count N + 1, counted, then refused before it executes). No version-1 interpreter exists, so this runs on
# version-0 laws that stand in for version-1 ones:
#   - the tick block: a top-level While, last in the law; the stand-in runs its body once per tick with no operation of
#     its own (C1), ignoring the While's condition and bound; its frame is the While's, which carries no extra field;
#   - a port declaration: a top-level `Let x be <literal>.` named in PORTS; version 0 counts its +1, version 1 would not
#     (C1), but it stands in the prefix, which no tick budget charges (B3);
#   - the budget: a counting layer over the instrumented reference (cut0_claims.CutInterp), refusing TICK-BUDGET when an
#     increment of ops makes the current tick's count N + 1, at the clause whose statement is executing, an If
#     condition's arm included.
# Its results are MEASURED on these stand-ins only: they show that draft 2's layout holds version 1's frame kinds as the
# rulings read them, not that a version-1 interpreter produces them, and they authorize no format freeze.
V1_LAWS = (
    ("A", "a tick that performs a procedure holding a claim",
     "Title: Stand-in A.\n"
     "§1 Let g be 5.\n"
     "§2 To check, do the following.\n"
     "§2.1 We claim that g is positive, by computation.\n"
     "§3 Let n be 0.\n"
     "§4 While n is less than 1000, at most 1000 times, do the following.\n"
     "§4.1 Say n.\n"
     "§4.2 Perform check.\n"
     "§4.3 Increase n by 1.\n", ("1",), "4"),
    ("B", "a tick whose If chain has conditions that cost operations",
     "Title: Stand-in B.\n"
     "§1 Let g be 3.\n"
     "§2 Let n be 0.\n"
     "§3 While n is less than 1000, at most 1000 times, do the following.\n"
     "§3.1 If n plus g is greater than 50, say 1.\n"
     "§3.2 Otherwise, if n plus g times 2 is even, say 2.\n"
     "§3.3 Otherwise, say 3.\n"
     "§3.4 Increase n by 1.\n", ("1",), "3"),
    ("C", "a tick with a For whose passes remain, and a procedure whose first statement is a Perform",
     "Title: Stand-in C.\n"
     "§1 Let g be 2.\n"
     "§2 Let s be 0.\n"
     "§3 To add, do the following.\n"
     "§3.1 Increase s by g.\n"
     "§4 To outer, do the following.\n"
     "§4.1 Perform add.\n"
     "§4.2 Say s.\n"
     "§5 While s is less than 1000000, at most 1000 times, do the following.\n"
     "§5.1 For each k from 1 to 3, do the following.\n"
     "§5.1.1 Perform outer.\n", ("1",), "5"),
)


class TickStandin(C.CutInterp):
    """The instrumented reference with a stand-in tick block and the budget's counting layer."""

    def __init__(self, *a, **k):
        self.tick_clause, self.ticks, self.n_budget = k.pop("tick"), k.pop("ticks"), k.pop("n")
        self.tick_start, self._evals = None, []
        C.CutInterp.__init__(self, *a, **k)

    @property
    def ops(self):
        return self._ops

    @ops.setter
    def ops(self, v):
        self._ops = v
        if self.tick_start is not None and v - self.tick_start == self.n_budget + 1:
            self.refuse("TICK-BUDGET", self.clause_now())

    def clause_now(self):
        """The clause whose statement is executing: an expression's clause; else an If condition's arm; else the top
        frame's clause (SPEC section 7 and section 11 item 18, as F20.4 keeps them)."""
        if self._evals:
            return self._evals[-1]
        top = self.frames[-1]
        if isinstance(top["stmt"], IfS) and top["arm"] is not None:
            return top["stmt"].arms[top["arm"]][2].id
        return top["clause"].id

    def eval(self, cid, e):
        self._evals.append(cid)
        try:
            return C.CutInterp.eval(self, cid, e)
        finally:
            self._evals.pop()

    def stmt(self, c, s):
        if c.id != self.tick_clause:
            return C.CutInterp.stmt(self, c, s)
        self.frames.append({"clause": c, "stmt": s, "more": True, "arm": None})
        try:
            for _ in range(self.ticks):
                self.tick_start = self.ops
                self.seq(c.children)
            self.tick_start = None
        finally:
            self.frames.pop()


def run_v1(raw, tick_label, ticks, n):
    comp = compile_bytes(raw.encode("utf-8"))
    if not comp.ok:
        raise SystemExit("stand-in law refused at compile: %s" % (comp.status if hasattr(comp, "status") else comp))
    by_label = {c.label: c for c in comp.prog.clauses}
    it = TickStandin(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=10 ** 8,
                     tick=by_label[tick_label].id, ticks=ticks, n=n)
    it.run()
    if it.cut is None:
        return comp, None, None, None, it
    p = it.status.split(" ")
    return comp, it.cut, p[1], int(p[2]), it


def main_v1():
    global VERSION, PORTS, PLANT
    VERSION = 1
    ok = True
    print("# version 1's frames on version-0 stand-ins: MEASURED on these stand-ins only, never on a version-1 "
          "interpreter; no format freeze follows from it")
    reasons, kinds, refused_runs, completed = {}, {}, 0, 0
    live_bad = 0
    forged = forged_outside = forged_inside = 0
    kept = []
    for name, what, raw, ports, tick in V1_LAWS:
        comp = compile_bytes(raw.encode("utf-8"))
        PORTS = {c.id for c in comp.prog.clauses if c.label in ports}
        print("== stand-in %s: %s (ports %s; the tick block %s)" % (name, what, ", ".join(ports), tick))
        for n in range(1, 13):
            comp, cut, code, ec, it = run_v1(raw, tick, 3, n)
            if cut is None:
                completed += 1
                print("   N=%-2d COMPLETED  ops %d" % (n, it.ops))
                continue
            refused_runs += 1
            b = encode(comp.prog, cut, code)
            live = key_of(comp.prog, cut)
            top = cut[-1]["stmt"]
            kinds[type(top).__name__] = kinds.get(type(top).__name__, 0) + 1
            try:
                dcode, frames = decode(comp.prog, b, ec)
                good = (key_of(comp.prog, frames) == live and dcode == code and in_shapes(comp.prog, live)
                        and C.continuation(comp.prog, frames) == C.continuation(comp.prog, cut))
            except Malformed as e:
                good, frames = False, None
                print("      its own payload refused: %s" % e)
            live_bad += not good
            print("   N=%-2d %s %s at %s, last frame %s, %d frames, %s  %s" % (
                n, it.status.split(" ")[0], code, comp.prog.clauses[ec - 1].label, type(top).__name__, len(cut),
                "as live" if good else "DIFFERS", b.hex()))
            kept.append((comp, cut, code, ec))
            positions = [(f["clause"], f["stmt"], sel_of(comp.prog, f["clause"], f["stmt"])) for f in cut]
            for fp in forgeries(comp.prog, positions):
                for key in keys_for(fp):
                    forged += 1
                    try:
                        decode(comp.prog, encode_key(code, key), None)
                        inside = in_shapes(comp.prog, key)
                        forged_outside += not inside
                        forged_inside += inside
                    except Malformed as e:
                        reasons[str(e)] = reasons.get(str(e), 0) + 1
    refused_forged = sum(reasons.values())
    ok &= live_bad == 0 and forged_outside == 0 and refused_forged + forged_inside + forged_outside == forged
    print("== every refused stand-in run: %d refused (%d completed), last-frame kinds %s; decoded as live: %s" % (
        refused_runs, completed, dict(sorted(kinds.items())), "all" if live_bad == 0 else "%d DIFFER" % live_bad))
    print("== frame forgeries on those cuts: %d = %d refused + %d accepted inside the shapes (another position a run "
          "could reach) + %d accepted outside them; refusals by reason %s" % (
              forged, refused_forged, forged_inside, forged_outside, dict(sorted(reasons.items()))))

    print("== the named plants, one per rule, each refused with its own reason (and the cases that must load)")
    named = v1_cases()
    plant_bad = 0
    for label, comp, b, ec, want, key in named:
        PORTS = comp.ports
        try:
            decode(comp.prog, b, ec)
            got = None
        except Malformed as e:
            got = str(e)
        good = got == want
        plant_bad += not good
        print("   %-58s %-14s %s" % (label, got or "loads", "as required" if good else "WANTED %s" % (want or "loads")))
    ok &= plant_bad == 0

    print("== version 0's rule on the same Perform-last payload, for the contrast")
    VERSION = 0
    PORTS = set()
    v0_refused = 0
    for label, comp, b, ec, want, key in named:
        if label.startswith("S4 version 1 loads"):
            try:
                decode(comp.prog, encode_key(NEUTRAL, key), ec)     # a version-0 code: TICK-BUDGET is version 1's
                print("   the same frames with %s: loads under version 0" % NEUTRAL)
            except Malformed as e:
                v0_refused += 1
                print("   the same frames with %s: refused under version 0, %s" % (NEUTRAL, e))
    ok &= v0_refused == 1
    VERSION = 1

    print("== each shape rule is needed on version 1's frames: dropping it lets its named plant load")
    caught = 0
    rules = (("no-root", "S1 "), ("no-nest", "S2 "), ("no-inline", "S3 "), ("no-top-kind", "S4 port"),
             ("no-range", "S5 "), ("no-event", "S6 "), ("no-code-kind", "S7 "))
    for plant, prefix in rules:
        PLANT = plant
        let_through = []
        for label, comp, b, ec, want, key in named:
            if want is None or not label.startswith(prefix):
                continue
            PORTS = comp.ports
            try:
                decode(comp.prog, b, ec)
                let_through.append(label)
            except Malformed:
                pass
        PLANT = None
        caught += bool(let_through)
        print("   %-12s %s" % (plant, ("lets through: " + "; ".join(let_through)) if let_through else "EQUIVALENT here"))
    ok &= caught == len(rules)
    print("CUT SCHEMA DRAFT 2, VERSION 1 ON STAND-INS %s: %d refused runs decoded as live (%d differ); %d frame "
          "forgeries, %d refused, %d accepted inside the shapes, %d accepted outside them; %d named plants as required "
          "(%d not); %d of %d shape rules needed. MEASURED on version-0 stand-ins only" % (
              "HELD" if ok else "FAILED", refused_runs, live_bad, forged, refused_forged, forged_inside,
              forged_outside, len(named) - plant_bad, plant_bad, caught, len(rules)))
    return 0 if ok else 1


def v1_cases():
    """The named plants, built on the stand-ins' compiled laws: (label, compiled law, payload, event clause, the reason
    it must be refused or None when it must load, the key)."""
    laws = {}
    for name, what, raw, ports, tick in V1_LAWS:
        comp = compile_bytes(raw.encode("utf-8"))
        comp.ports = {c.id for c in comp.prog.clauses if c.label in ports}
        laws[name] = comp
    out = []

    def add(label, name, code, key, ec, want):
        comp = laws[name]
        out.append((label, comp, encode_key(code, key), ec, want, key))

    def cid(name, label):
        return next(c.id for c in laws[name].prog.clauses if c.label == label)
    a = lambda l: cid("A", l)
    bb = lambda l: cid("B", l)
    cc = lambda l: cid("C", l)
    TB = "TICK-BUDGET"
    # loads
    add("tick frame, then a Say in its body", "A", TB, ((a("4"), OWN, None, None), (a("4.1"), OWN, None, None)),
        a("4.1"), None)
    add("S4 version 1 loads a Perform as the last frame", "A", TB, ((a("4"), OWN, None, None),
                                                                   (a("4.2"), OWN, None, None)), a("4.2"), None)
    add("S6 an If-condition refusal naming the arm loads", "B", TB, ((bb("3"), OWN, None, None),
                                                                    (bb("3.1"), OWN, None, 1)), bb("3.2"), None)
    add("S7 TICK-BUDGET on a Perform last frame loads", "C", TB, ((cc("5"), OWN, None, None), (cc("5.1"), OWN, 1, None),
                                                                 (cc("5.1.1"), OWN, None, None)), cc("5.1.1"), None)
    # each rule's plant
    add("S1 first frame inside the tick body", "A", TB, ((a("4.1"), OWN, None, None),), a("4.1"), "not rooted")
    add("S2 tick frame then a statement not in its body", "A", TB, ((a("4"), OWN, None, None),
                                                                   (a("3"), OWN, None, None)), a("3"), "not nested")
    add("S2 a port declaration below the tick frame", "A", TB, ((a("4"), OWN, None, None), (a("1"), OWN, None, None)),
        a("1"), "not nested")
    add("S3 an inline arm statement not after its If", "B", TB, ((bb("3"), OWN, None, None), (bb("3.2"), 1, None, None)),
        bb("3.2"), "not nested")
    add("S4 port: a port declaration as the only, last frame", "A", TB, ((a("1"), OWN, None, None),), a("1"),
        "top kind")
    add("S5 a For bit of 2", "C", TB, ((cc("5"), OWN, None, None), (cc("5.1"), OWN, 2, None),
                                       (cc("5.1.1"), OWN, None, None)), cc("5.1.1"), "bit")
    add("S5 an If arm out of range", "B", TB, ((bb("3"), OWN, None, None), (bb("3.1"), OWN, None, 7)), bb("3.1"), "arm")
    add("S6 an If-condition refusal naming the head's clause", "B", TB, ((bb("3"), OWN, None, None),
                                                                        (bb("3.1"), OWN, None, 1)), bb("3.1"),
        "event clause")
    add("S7 CLAIM-REFUTED on a Say last frame", "A", "CLAIM-REFUTED", ((a("4"), OWN, None, None),
                                                                     (a("4.1"), OWN, None, None)), a("4.1"),
        "code kind")
    return out


if __name__ == "__main__":
    if "--v1-standins" in sys.argv:
        sys.exit(main_v1())
    sys.exit(main())

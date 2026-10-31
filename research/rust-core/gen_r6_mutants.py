"""RUST-CORE-0: R6's 10,000 mutants, fixed before any experiment (SHEET.md Amendment 3; the owner's ruling E2).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_r6_mutants.py --out PATH

The sources are the law bytes of LAW-SUFFICIENCY's 298 texts (`common.accepted()`, 290, and LAW-SUFFICIENCY-1's
fixtures, 8), written by the front end at the starting commit and sorted by id. One generator, random.Random(SEED), is
drawn through four operators in this order, 2,500 mutants each:
- flip: one bit of one byte. A source drawn; a byte position drawn; a bit 0-7 drawn; that bit inverted.
- truncate: one line cut short. A source drawn; a line drawn (any line, the first two included); a length c drawn
  from 0 to the line's length less one; the line keeps its first c bytes and its LF.
- swap: the rests of two clause lines exchanged. A source drawn, again until it has two clause lines whose rests differ;
  two such lines drawn, again until their rests differ; each keeps its prefix `(clause k p ` and its final `)`.
- id: one id changed by one. A source drawn, again until it has an id. An id is a token of a clause line, outside its
  strings, that is a natural number or a dotted label, and is neither the value of a `lit` form nor a `while` bound:
  the clause number and parent, and every variable, clause, must, claim and label reference. One drawn, then a step
  of -1 or +1 drawn and added to it (to its last part, for a label); -1 from 0 is +1 instead.
A mutant equal to a source or to an earlier mutant is drawn again, its draws spent, so the 10,000 are distinct byte
strings, none of them one of the 298 (on small laws the operators often repeat, and a swap can turn one source into
another: LAW-SUFFICIENCY-1's E2 fixtures come in pairs whose two defines are swapped). Each mutant is written whole, as
hex, with its sha256: the file is the mutants. The experiment never draws them again, so they depend on no later
Python's `random`.

R6's reference for a mutant is decoder1's decoding run by the interpreter, under the mutant budget. This tool imports
neither; it names decoder1 by path and sha256 in the file's header. It never imports format_check. With
`--checker MUTANTS OUT` it is a second tool: it reads the mutants file and records format_check's verdict on each, as
evidence only (the checker is evidence, not authority). It refuses to write if HEAD is not the starting commit, or if
src/, tests/ or vectors/ differ from it. It is outside the core author's reading set (D1)."""
import hashlib
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
SEED = 20261031
PER_OPERATOR = 2500
OPERATORS = ("flip", "truncate", "swap", "id")
BUDGET = 1000000                                   # COMPAT-0's mutant budget
DECODER1 = os.path.join("research", "law-sufficiency", "decoder1.py")
PREFIX = re.compile(r"\(clause (0|[1-9][0-9]*) (0|[1-9][0-9]*) ")
IDISH = re.compile(r"[0-9]+(?:\.[0-9]+)*\Z")


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return sha(f.read())


def refuse_if_moved(tool):
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("%s: HEAD is not the starting commit %s" % (tool, BASE[:7]))
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("%s: src/, tests/ or vectors/ differ from the starting commit" % tool)


def sources():
    """The 298 texts' law bytes, as (id, law), sorted by id, written by the front end."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
    import common
    from orlog.front import compile_bytes
    texts = [(t[0], t[2]) for t in common.accepted()]
    fx = os.path.join(ROOT, "research", "law-sufficiency", "fixtures")
    for n in sorted(os.listdir(fx)):
        if n.endswith(".orl"):
            with open(os.path.join(fx, n), "rb") as f:
                texts.append(("fixtures/" + n, f.read()))
    out = []
    for ident, raw in sorted(texts):
        c = compile_bytes(raw)
        if not c.ok:
            sys.exit("GEN-R6: the front end refuses %s" % ident)
        out.append((ident, c.law))
    if len(out) != 298 or len(set(i for i, _ in out)) != 298:
        sys.exit("GEN-R6: %d sources, not 298 distinct ids" % len(out))
    return out


def id_tokens(line):
    """The ids of one clause line, as (start, end, text), by the rule in the docstring."""
    out, words, i, n = [], [], 0, len(line)
    while i < n:
        ch = line[i]
        if ch in "() ":
            i += 1
            continue
        if ch == '"':
            i += 1
            while i < n and line[i] != '"':
                i += 2 if line[i] == "\\" else 1
            i += 1
            words.append('"')
            continue
        j = i
        while j < n and line[j] not in ' ()"':
            j += 1
        tok = line[i:j]
        if IDISH.match(tok) and not (len(words) >= 2 and words[-2] == "lit") and not (words and words[-1] == "while"):
            out.append((i, j, tok))
        words.append(tok)
        i = j
    return out


def mutate(op, srcs, rng):
    """One mutant: (the source's index, its parameters, its bytes)."""
    if op == "flip":
        s = rng.randrange(len(srcs))
        law = srcs[s][1]
        p, b = rng.randrange(len(law)), rng.randrange(8)
        return s, "byte %d bit %d" % (p, b), law[:p] + bytes([law[p] ^ (1 << b)]) + law[p + 1:]
    if op == "truncate":
        s = rng.randrange(len(srcs))
        lines = srcs[s][1].split(b"\n")[:-1]
        li = rng.randrange(len(lines))
        c = rng.randrange(len(lines[li]))
        lines[li] = lines[li][:c]
        return s, "line %d to %d" % (li + 1, c), b"\n".join(lines) + b"\n"
    if op == "swap":
        while True:
            s = rng.randrange(len(srcs))
            lines = srcs[s][1].decode("ascii").split("\n")[:-1]
            clause = lines[2:]
            heads = [PREFIX.match(ln).end() for ln in clause]
            rests = [ln[h:-1] for ln, h in zip(clause, heads)]
            if len(set(rests)) >= 2:
                break
        n = len(clause)
        while True:
            i = rng.randrange(n)
            j = rng.randrange(n - 1)
            j += j >= i
            if rests[i] != rests[j]:
                break
        clause[i], clause[j] = clause[i][:heads[i]] + rests[j] + ")", clause[j][:heads[j]] + rests[i] + ")"
        return s, "lines %d and %d" % (i + 3, j + 3), ("\n".join(lines[:2] + clause) + "\n").encode("ascii")
    while True:
        s = rng.randrange(len(srcs))
        lines = srcs[s][1].decode("ascii").split("\n")[:-1]
        toks = [(li, a, b, t) for li in range(2, len(lines)) for a, b, t in id_tokens(lines[li])]
        if toks:
            break
    li, a, b, t = toks[rng.randrange(len(toks))]
    step = 1 if rng.randrange(2) else -1
    parts = t.split(".")
    v = int(parts[-1])
    parts[-1] = str(v + step if v + step >= 0 else v + 1)
    new = ".".join(parts)
    lines[li] = lines[li][:a] + new + lines[li][b:]
    return s, "line %d id %s to %s" % (li + 1, t, new), ("\n".join(lines) + "\n").encode("ascii")


def make(path):
    refuse_if_moved("GEN-R6")
    if "format_check" in sys.modules:
        sys.exit("GEN-R6: format_check is imported")
    srcs = sources()
    rng = random.Random(SEED)
    rows, n = [], 0
    seen = set(sha(law) for _, law in srcs)
    redrawn = {op: 0 for op in OPERATORS}
    for op in OPERATORS:
        for _ in range(PER_OPERATOR):
            n += 1
            while True:
                s, params, m = mutate(op, srcs, rng)
                if sha(m) not in seen:
                    break
                redrawn[op] += 1
            seen.add(sha(m))
            rows.append("%05d %s source %d %s sha256 %s bytes %d hex %s" % (n, op, s, params, sha(m), len(m), m.hex()))
    head = [
        "# R6's mutants: SHEET.md Amendment 3, fixed before any experiment (the owner's ruling E2, 2026-10-30)",
        "# generator research/rust-core/gen_r6_mutants.py sha256 %s" % sha(open(os.path.abspath(__file__), "rb").read()),
        "# decoder1 %s sha256 %s; the reference for a mutant is decoder1's decoding, run by src/orlog/interp.py "
        "sha256 %s, under the mutant budget %d (COMPAT-0's)" % (DECODER1.replace(os.sep, "/"), sha_file(DECODER1),
                                                               sha_file(os.path.join("src", "orlog", "interp.py")),
                                                               BUDGET),
        "# sources: the law bytes of the 298 texts, written by the front end at %s (src/orlog/sema.py sha256 %s), "
        "sorted by id; listed below by index" % (BASE[:7], sha_file(os.path.join("src", "orlog", "sema.py"))),
        "# seed %d: one random.Random(seed), drawn through the operators in this order, %d mutants each: %s; each "
        "operator as gen_r6_mutants.py's docstring states; a mutant equal to a source or an earlier mutant drawn again "
        "(%s)" % (SEED, PER_OPERATOR, ", ".join(OPERATORS),
                  ", ".join("%s %d times" % (op, redrawn[op]) for op in OPERATORS)),
        "# a row: the mutant's number, its operator, its source's index, the operator's draws, its sha256, its length, "
        "and its bytes in lowercase hex",
    ]
    head += ["# source %d %s sha256 %s bytes %d" % (i, ident, sha(law), len(law)) for i, (ident, law) in enumerate(srcs)]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(path, "wb") as f:
        f.write(data)
    distinct = len(set(r.split(" ")[r.split(" ").index("sha256") + 1] for r in rows))
    print("GEN-R6: %d mutants, %d distinct, none a source; drawn again: %s; %d bytes in all; sha256 %s" % (
        len(rows), distinct, ", ".join("%s %d" % (op, redrawn[op]) for op in OPERATORS), len(data), sha(data)))
    if distinct != len(rows):
        sys.exit("GEN-R6: the mutants are not distinct")


def mutants(path):
    """The mutants file -> [(number, operator, bytes)], each held to its own sha256 and length."""
    out = []
    with open(path, "rb") as f:
        for line in f.read().decode("ascii").split("\n"):
            if not line or line.startswith("#"):
                continue
            w = line.split(" ")
            m = bytes.fromhex(w[w.index("hex") + 1])
            if sha(m) != w[w.index("sha256") + 1] or len(m) != int(w[w.index("bytes") + 1]):
                sys.exit("GEN-R6: mutant %s does not match its own sha256 or length" % w[0])
            out.append((w[0], w[1], m))
    return out


def checker(path, out):
    """format_check's verdict on each mutant, as evidence only."""
    refuse_if_moved("GEN-R6 --checker")
    sys.path.insert(0, HERE)
    sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
    import format_check as fc
    with open(path, "rb") as f:
        msha = sha(f.read())
    rows, counts = [], {}
    for num, op, m in mutants(path):
        try:
            fc.read(m)
            v = "accepted"
        except fc.Refused as r:
            v = "W%d line %d" % (r.w, r.line)
        except Exception as e:                       # a crash is recorded as such, never as a refusal
            v = "CRASHED %s" % type(e).__name__
        key = (op, v.split(" line ")[0])
        counts[key] = counts.get(key, 0) + 1
        rows.append("%s %s %s" % (num, op, v))
    head = [
        "# format_check's verdict on R6's mutants, as evidence only (the checker is evidence, not authority)",
        "# mutants file sha256 %s; research/rust-core/format_check.py sha256 %s" % (
            msha, sha(open(os.path.join(HERE, "format_check.py"), "rb").read())),
        "# counts by operator and verdict: %s" % "; ".join("%s %s %d" % (o, v, c) for (o, v), c in sorted(counts.items())),
        "# a row: the mutant's number, its operator, and the checker's verdict (accepted, W<k> line <n>, or CRASHED)",
    ]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(out, "wb") as f:
        f.write(data)
    crashed = sum(c for (o, v), c in counts.items() if v.startswith("CRASHED"))
    accepted = sum(c for (o, v), c in counts.items() if v == "accepted")
    print("GEN-R6 --checker: %d mutants; accepted %d; crashed %d; sha256 %s" % (len(rows), accepted, crashed, sha(data)))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--out":
        make(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "--checker":
        checker(sys.argv[2], sys.argv[3])
    else:
        sys.exit("usage: gen_r6_mutants.py --out PATH | --checker MUTANTS OUT")

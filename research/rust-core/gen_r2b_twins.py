"""RUST-CORE-0: R2b's canonicity twins and their expected refusals, fixed before any experiment (SHEET.md Amendment 4;
the owner's ruling R2b).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_r2b_twins.py --out PATH

Each twin is one of the experiment's canonical laws with exactly one non-canonical change. The laws are the law bytes
of LAW-SUFFICIENCY's 298 texts, written by the front end at the starting commit, sorted by id, each distinct byte
string once (the first id that has it names it). For each law, each kind below that applies makes one twin, at the
first place it applies, scanning the clause lines in order and each line from its start. Nothing is drawn.

The expected outcome of every twin is a load refusal, `LAW-REFUSED W<k> line <L>`, and it is fixed by construction from
section 8 of LAW-FORMAT-0, not by any checker. The law passes every check; the twin changes one line, L, and nothing
else. So every line before L passes phases 1 and 2, as it did. Line L keeps its character set, its prefix and its final
`)`, unless the kind changes them, and its parentheses, so W14(c)'s count is unchanged. The first failure is therefore
on line L, and its W is the kind's:
- W1, the prefix or line 2: `prefix-zero` (`(clause 01 ...`), `mode-upper` (`(decimals Fixed)`);
- W2, an atom or a word not canonical: `literal-zero` (an Int or Fix literal with a leading zero), `id-zero` (an id
  with a leading zero: a variable, a clause, a must, a claim or a label reference), `fuel-zero` (a while bound with a
  leading zero), `hex-upper` (an uppercase hex digit in a Float literal), `escape-printable` (a character from U+0020
  to U+007E written as `\\u{h}`), `escape-zero` (a `\\u{h}` with a leading zero), `escape-upper` (a `\\u{h}` with an
  uppercase digit), `word-upper` (the statement's first word in capitals);
- W3, the spacing, every atom canonical: `space-double` (two spaces between two items), `space-after-open` (a space
  after the statement's `(`), `space-before-close` (a space before the statement's last `)`), `empty-form` (`(given)`
  or `(over)` without its one space), `absorbed-space` (two spaces before `absorbed`).

The twins are the file it writes: research/rust-core/r2b-twins.txt, named in the sheet by its sha256. With
`--checker TWINS OUT` it is a second tool: it records format_check's verdict on each twin beside the expected one, as
evidence only (the checker is evidence, not authority). It refuses to write if HEAD is not the starting commit, or if
src/, tests/ or vectors/ differ from it. It is outside the core author's reading set (D1)."""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
PREFIX = re.compile(r"\(clause (0|[1-9][0-9]*) (0|[1-9][0-9]*) ")
KINDS = [("prefix-zero", 1), ("mode-upper", 1), ("literal-zero", 2), ("id-zero", 2), ("fuel-zero", 2), ("hex-upper", 2),
         ("escape-printable", 2), ("escape-zero", 2), ("escape-upper", 2), ("word-upper", 2), ("space-double", 3),
         ("space-after-open", 3), ("space-before-close", 3), ("empty-form", 3), ("absorbed-space", 3)]
sys.path.insert(0, HERE)
import gen_r6_mutants           # noqa: E402  (its sources() and id_tokens(); it imports nothing but the stdlib here)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def tokens(rest):
    """The rest's tokens outside strings, as (start, end, text), and its strings, as (start, end), in order."""
    toks, strs, i, n = [], [], 0, len(rest)
    while i < n:
        ch = rest[i]
        if ch in "() ":
            i += 1
        elif ch == '"':
            j = i + 1
            while rest[j] != '"':
                j += 2 if rest[j] == "\\" else 1
            strs.append((i, j + 1))
            i = j + 1
        else:
            j = i
            while j < n and rest[j] not in ' ()"':
                j += 1
            toks.append((i, j, rest[i:j]))
            i = j
    return toks, strs


def outside(rest, strs, i):
    return not any(a <= i < b for a, b in strs)


def change(kind, rest):
    """The rest with the kind's one change at its first place, or None where the kind does not apply."""
    if rest == "absorbed":
        return " absorbed" if kind == "absorbed-space" else None
    toks, strs = tokens(rest)
    words = [t[2] for t in toks]
    if kind == "literal-zero":
        for k, (a, b, t) in enumerate(toks):
            if k >= 2 and words[k - 2] == "lit" and words[k - 1] in ("int", "fix"):
                return rest[:a] + "0" + rest[a:]
    if kind == "fuel-zero":
        for k, (a, b, t) in enumerate(toks):
            if k >= 1 and words[k - 1] == "while":
                return rest[:a] + "0" + rest[a:]
    if kind == "id-zero":
        ids = gen_r6_mutants.id_tokens(rest)
        if ids:
            a = ids[0][0]
            return rest[:a] + "0" + rest[a:]
    if kind == "hex-upper":
        for k, (a, b, t) in enumerate(toks):
            if k >= 2 and words[k - 2] == "lit" and words[k - 1] == "float":
                m = re.search(r"[a-f]", t)
                if m:
                    return rest[:a + m.start()] + t[m.start()].upper() + rest[a + m.start() + 1:]
    if kind in ("escape-printable", "escape-zero", "escape-upper"):
        for a, b in strs:
            j = a + 1
            while j < b - 1:
                if rest[j] == "\\":
                    if rest[j + 1] == "u":
                        e = rest.index("}", j)
                        h = rest[j + 3:e]
                        if kind == "escape-zero":
                            return rest[:j + 3] + "0" + rest[j + 3:]
                        if kind == "escape-upper" and re.search(r"[a-f]", h):
                            m = re.search(r"[a-f]", h)
                            return rest[:j + 3 + m.start()] + h[m.start()].upper() + rest[j + 3 + m.start() + 1:]
                        j = e + 1
                    else:
                        j += 2
                    continue
                if kind == "escape-printable":
                    return rest[:j] + "\\u{%x}" % ord(rest[j]) + rest[j + 1:]
                j += 1
    if kind == "word-upper" and toks:
        a, b, t = toks[0]
        return rest[:a] + t.upper() + rest[b:]
    if kind == "space-double":
        for i, ch in enumerate(rest):
            if ch == " " and outside(rest, strs, i):
                return rest[:i] + " " + rest[i:]
    if kind == "space-after-open":
        return "( " + rest[1:]
    if kind == "space-before-close":
        return rest[:-1] + " )"
    if kind == "empty-form":
        for form in ("(given )", "(over )"):
            i = rest.find(form)
            while i >= 0 and not outside(rest, strs, i):
                i = rest.find(form, i + 1)
            if i >= 0:
                return rest[:i] + form.replace(" ", "") + rest[i + len(form):]
    return None


def twin(kind, law):
    """(the twin's bytes, its changed line) or None: the kind's one change, at its first place in the law."""
    lines = law.decode("ascii").split("\n")[:-1]
    if kind == "mode-upper":
        lines[1] = lines[1].replace("(decimals f", "(decimals F", 1)
        return ("\n".join(lines) + "\n").encode("ascii"), 2
    for i in range(2, len(lines)):
        m = PREFIX.match(lines[i])
        if kind == "prefix-zero":
            lines[i] = "(clause 0" + lines[i][len("(clause "):]
            return ("\n".join(lines) + "\n").encode("ascii"), i + 1
        rest = lines[i][m.end():-1]
        new = change(kind, rest)
        if new is not None:
            lines[i] = lines[i][:m.end()] + new + ")"
            return ("\n".join(lines) + "\n").encode("ascii"), i + 1
    return None


def make(path):
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("GEN-R2B: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("GEN-R2B: src/, tests/ or vectors/ differ from the starting commit")
    seen, laws = set(), []
    for ident, law in gen_r6_mutants.sources():
        if sha(law) not in seen:
            seen.add(sha(law))
            laws.append((ident, law))
    rows, counts, made = [], {k: 0 for k, _ in KINDS}, set()
    for ident, law in laws:
        for kind, w in KINDS:
            t = twin(kind, law)
            if t is None:
                continue
            data, line = t
            if data == law or sha(data) in made:
                sys.exit("GEN-R2B: %s of %s is not a new byte string" % (kind, ident))
            made.add(sha(data))
            counts[kind] += 1
            rows.append("%05d %s source %s expect W%d line %d sha256 %s bytes %d hex %s" % (
                len(rows) + 1, kind, ident, w, line, sha(data), len(data), data.hex()))
    head = [
        "# R2b's canonicity twins: SHEET.md Amendment 4, fixed before any experiment (the owner's ruling R2b, "
        "2026-10-30)",
        "# generator research/rust-core/gen_r2b_twins.py sha256 %s; each twin and its expected refusal as its "
        "docstring states, by construction from LAW-FORMAT-0 section 8, never by a checker" % (
            sha(open(os.path.abspath(__file__), "rb").read())),
        "# laws: the law bytes of the 298 texts, written by the front end at %s (src/orlog/sema.py sha256 %s), sorted "
        "by id, each distinct byte string once: %d laws" % (
            BASE[:7], sha(open(os.path.join(ROOT, "src", "orlog", "sema.py"), "rb").read()), len(laws)),
        "# twins by kind (expected W): %s; %d in all" % (
            ", ".join("%s (W%d) %d" % (k, w, counts[k]) for k, w in KINDS), len(rows)),
        "# a row: the twin's number, its kind, its law's id, the expected refusal (LAW-REFUSED W<k> line <L>), its "
        "sha256, its length, and its bytes in lowercase hex",
    ]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(path, "wb") as f:
        f.write(data)
    print("GEN-R2B: %d laws, %d twins; %s; sha256 %s" % (
        len(laws), len(rows), ", ".join("%s %d" % (k, counts[k]) for k, _ in KINDS), sha(data)))


def checker(path, out):
    """format_check's verdict on each twin, beside the expected one, as evidence only."""
    sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
    import format_check as fc
    with open(path, "rb") as f:
        tsha = sha(f.read())
    rows, agree, differ = [], 0, []
    for line in open(path, encoding="ascii"):
        if line.startswith("#"):
            continue
        w = line.split(" ")
        data = bytes.fromhex(w[w.index("hex") + 1].strip())
        if sha(data) != w[w.index("sha256") + 1]:
            sys.exit("GEN-R2B: twin %s does not match its own sha256" % w[0])
        want = "W%s line %s" % (w[w.index("expect") + 1][1:], w[w.index("expect") + 3])
        try:
            fc.read(data)
            got = "accepted"
        except fc.Refused as r:
            got = "W%d line %d" % (r.w, r.line)
        except Exception as e:
            got = "CRASHED %s" % type(e).__name__
        same = got == want
        agree += same
        if not same:
            differ.append(w[0])
        rows.append("%s %s expect %s checker %s %s" % (w[0], w[1], want, got, "agrees" if same else "DIFFERS"))
    head = ["# format_check's verdict on R2b's twins, beside the expected refusal, as evidence only (the checker is "
            "evidence, not authority)",
            "# twins file sha256 %s; research/rust-core/format_check.py sha256 %s" % (
                tsha, sha(open(os.path.join(HERE, "format_check.py"), "rb").read())),
            "# the checker agrees on %d of %d; differs on %s" % (agree, len(rows), " ".join(differ) or "none")]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(out, "wb") as f:
        f.write(data)
    print("GEN-R2B --checker: agrees on %d of %d; differs on %s; sha256 %s" % (
        agree, len(rows), " ".join(differ[:20]) or "none", sha(data)))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--out":
        make(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "--checker":
        checker(sys.argv[2], sys.argv[3])
    else:
        sys.exit("usage: gen_r2b_twins.py --out PATH | --checker TWINS OUT")

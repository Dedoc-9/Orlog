"""RUST-CORE-0: R2's write-back fixtures, frozen before any core exists (SHEET.md Amendment 7; the owner's ruling A,
point 6; REREAD-7's X9).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_r2_fixtures.py OUT

None of the 298 laws holds an `(over …)` list out of ascending order or with a repeated entry, and only two hold a
`(given …)` list out of order, so a writer that sorts a list, or writes it as a set, would pass R2 on every one of them
(REREAD-7's X9). These fixtures are laws whose lists are out of order or repeat an entry. Each is made from a law that
holds a list of two entries or more (three hold an `over` list, three a `given` list), by one change to one list:
- reversed;
- its first entry moved to its end;
- its first entry written twice.
A variant equal to a law already among the 298, or to an earlier variant, is dropped. Every fixture kept must be one
LAW-FORMAT-0's checker accepts and writes back exactly; one it does not is a defect of this generator, and it refuses
to write. The checker is evidence, not authority: it chooses no fixture. R2 expects each fixture written back byte for
byte. It refuses to write if HEAD is not the starting commit, or if src/, tests/ or vectors/ differ from it. Outside
the core author's reading set (D1)."""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_r6_mutants           # noqa: E402

LISTS = (("over", re.compile(rb"\(over((?: [0-9]+){2,})\)")), ("given", re.compile(rb"\(given((?: [0-9.]+){2,})\)")))
CHANGES = (("reversed", lambda xs: xs[::-1]), ("first moved last", lambda xs: xs[1:] + xs[:1]),
           ("first written twice", lambda xs: xs[:1] + xs))


def main(out):
    gen_r6_mutants.refuse_if_moved("GEN-R2-FIXTURES")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "research", "law-sufficiency"))
    import format_check
    sources = gen_r6_mutants.sources()
    seen = {law for _, law in sources}
    rows, refused = [], []
    for ident, law in sources:
        for kind, rx in LISTS:
            for m in rx.finditer(law):
                xs = m.group(1).split()
                for name, change in CHANGES:
                    ys = change(xs)
                    if ys == xs:
                        continue
                    new = law[:m.start(1)] + b"".join(b" " + y for y in ys) + law[m.end(1):]
                    if new in seen:
                        continue
                    seen.add(new)
                    try:
                        L = format_check.read(new)
                        back = format_check.write(L) == new
                    except format_check.Refused as r:
                        refused.append("%s %s %s: W%d line %d" % (ident, kind, name, r.w, r.line))
                        continue
                    if not back:
                        refused.append("%s %s %s: not written back exactly" % (ident, kind, name))
                        continue
                    rows.append("%s | %s %s: (%s %s) -> (%s %s) | sha256 %s | hex %s" % (
                        ident, kind, name, kind, b" ".join(xs).decode(), kind, b" ".join(ys).decode(),
                        hashlib.sha256(new).hexdigest(), new.hex()))
    if refused:
        sys.exit("GEN-R2-FIXTURES: the checker refuses %d variants, a defect of this generator: %s" % (
            len(refused), "; ".join(refused[:5])))
    head = ["# R2's write-back fixtures: SHEET.md Amendment 7 (the owner's ruling A, point 6; REREAD-7's X9). R2 expects "
            "each written back byte for byte",
            "# generator research/rust-core/gen_r2_fixtures.py sha256 %s" % hashlib.sha256(
                open(os.path.abspath(__file__), "rb").read()).hexdigest(),
            "# %d fixtures, from the laws holding an over or given list of two entries or more, one change to one list "
            "each: reversed, first moved last, first written twice" % len(rows),
            "# a row: the law it comes from | the list, before and after | its sha256 | its bytes in hex"]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(out, "wb") as f:
        f.write(data)
    print("GEN-R2-FIXTURES: %d fixtures, each accepted and written back exactly by the checker; sha256 %s" % (
        len(rows), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: gen_r2_fixtures.py OUT")
    main(sys.argv[1])

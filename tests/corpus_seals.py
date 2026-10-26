"""The law seal of every corpus program under this tree's front end, and under the front end of each git revision
named, side by side (a law seal is the sha256 of the law's bytes, SPEC section 9). A change that leaves every law
unchanged leaves this table unchanged; a Note is not law, so editing one changes the text seal and not the law seal.

With revisions named it also says, for each file on the path from raw bytes to the law seal, whether its code changed
from one revision to the next: its syntax tree is compared with every docstring removed, so a changed comment or
docstring reads as unchanged and any changed statement reads as changed. Law seals are not the whole of a law's
meaning: what a law does is in its run, which tests/compat.py holds.

  PYTHONHASHSEED=0 python -B tests/corpus_seals.py [REV ...]
"""
import ast
import io
import json
import os
import subprocess
import sys
import tarfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

PROBE = r'''
import json, os, sys
sys.path.insert(0, os.path.join(sys.argv[1], "src"))
from orlog.front import compile_bytes
out = {}
for p in sys.argv[2:]:
    with open(p, "rb") as fh:
        c = compile_bytes(fh.read())
    out[p] = c.law_seal if c.ok else "REFUSED " + c.error.code
print(json.dumps(out))
'''


def corpus():
    out = []
    for d in ("examples", os.path.join("examples", "spellings")):
        for fn in sorted(os.listdir(os.path.join(ROOT, d))):
            if fn.endswith(".orl"):
                out.append(os.path.join(d, fn).replace(os.sep, "/"))
    return out


def seals(front_root, paths):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-B", "-c", PROBE, front_root] + [os.path.join(ROOT, p) for p in paths],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode:
        raise SystemExit(r.stderr[-800:])
    got = json.loads(r.stdout)
    return [got[os.path.join(ROOT, p)] for p in paths]


def export(rev):
    """The revision's src/ only, from git, into build/ (the working tree is not touched)."""
    sha = subprocess.run(["git", "-C", ROOT, "rev-parse", "--verify", rev + "^{commit}"], capture_output=True,
                         text=True, check=True).stdout.strip()
    dst = os.path.join(ROOT, "build", "seals-" + sha[:12])
    if not os.path.isdir(os.path.join(dst, "src")):
        data = subprocess.run(["git", "-C", ROOT, "archive", sha, "src"], capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(dst, filter="data")
    return sha, dst


SEAL_PATH = ("src/orlog/canon.py", "src/orlog/syntax.py", "src/orlog/sema.py", "src/orlog/seal.py",
             "src/orlog/front.py")


def code_of(source):
    """The module's syntax tree with every docstring removed, as text."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and \
                isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
    return ast.dump(tree)


def code_at(rev, path):
    if rev is None:
        with open(os.path.join(ROOT, path), "rb") as fh:
            return code_of(fh.read().decode("utf-8"))
    src = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (rev, path)], capture_output=True, check=True).stdout
    return code_of(src.decode("utf-8"))


def main(revs):
    paths = corpus()
    here = seals(ROOT, paths)
    cols = [("this tree", here)]
    for rev in revs:
        sha, dst = export(rev)
        cols.append((rev + " (" + sha[:7] + ")", seals(dst, paths)))
    print("law seals of the %d corpus programs (first 16 hex digits)" % len(paths))
    for k, p in enumerate(paths):
        print("  %-36s %s" % (p, "  ".join(s[:16] for _, s in [(n, c[k]) for n, c in cols])))
    for name, col in cols[1:]:
        same = sum(1 for a, b in zip(here, col) if a == b)
        print("front end of %s: %d of %d law seals equal to this tree's" % (name, same, len(paths)))
    if revs:
        steps = list(zip(revs, revs[1:] + [None]))
        print("the code on the path from bytes to law seal (syntax trees, docstrings removed), revision to revision:")
        for path in SEAL_PATH:
            cells = ["%s->%s %s" % (a, b or "this tree", "same" if code_at(a, path) == code_at(b, path) else "CHANGED")
                     for a, b in steps]
            print("  %-22s %s" % (path, "; ".join(cells)))
    return 0 if all(c == here for _, c in cols[1:]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

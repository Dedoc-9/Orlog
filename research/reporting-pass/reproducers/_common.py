"""Shared by the reporting pass's reproducers: the repository's src on the path, planted copies of a module made in
memory (the tracked file is never written), arbitrations in a scratch work folder under work/reporting-pass/."""
import contextlib
import os
import sys
import types

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, "work", "reporting-pass")
FIXTURES = os.path.join(HERE, "fixtures")
sys.path.insert(0, os.path.join(ROOT, "src"))
FIXTURE_NOTE = "FIXTURE written by a research/reporting-pass reproducer, in memory; not a person's act"


def require_env():
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("set PYTHONHASHSEED=0 (and PYTHONUTF8=1 when redirecting)")


def read(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return fh.read()


def fixture(name):
    with open(os.path.join(FIXTURES, name), "rb") as fh:
        return fh.read()


def planted(modname, replacements):
    """A copy of src/orlog/<modname>.py with each (old, new) applied once (each old must occur exactly once), loaded
    as a fresh module in the orlog package. Nothing on disk changes."""
    path = os.path.join(ROOT, "src", "orlog", modname + ".py")
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")
    for old, new in replacements:
        n = text.count(old)
        if n != 1:
            raise SystemExit("plant on %s: %r occurs %d times" % (modname, old[:60], n))
        text = text.replace(old, new)
    import orlog  # noqa: F401  (the package, so that relative imports resolve)
    mod = types.ModuleType("orlog._planted_" + modname)
    mod.__package__ = "orlog"
    mod.__file__ = path
    exec(compile(text, path + " (planted)", "exec"), mod.__dict__)
    return mod


def workdir(name):
    d = os.path.join(WORK, "arb", name)
    os.makedirs(d, exist_ok=True)
    return d


def ledger_all(comp):
    """Every claim's own seal ratified, as the self-test's and court_monotone's fixtures do (in memory)."""
    from orlog.court import claim_seals
    return [{"kind": "claim", "claim_seal": s, "note": FIXTURE_NOTE, "_line": i + 1}
            for i, s in enumerate(claim_seals(comp).values())]


@contextlib.contextmanager
def reference_truncates_quotient():
    """The self-test's own reference plant (tests/selftest.py): the reference truncates a quotient, so the three
    backends dissent from it together (REFERENCE-DISSENT)."""
    from orlog import numeric_ref as N
    saved = N.i_quot

    def trunc(a, b):
        if b == 0:
            raise N.Refusal("DIVISION-BY-ZERO")
        q = abs(a) // abs(b)
        return N.chk(q if (a < 0) == (b < 0) else -q)
    N.i_quot = trunc
    try:
        yield
    finally:
        N.i_quot = saved


def show_rows(p, keys=("integrity", "evaluation", "support", "grounding")):
    out = []
    for r in p["rows"]:
        out.append("%s: %s" % (r["clause"], "; ".join("%s=%s" % (k, r[k]) for k in keys if k in r)))
    return out

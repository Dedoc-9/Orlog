"""LAW-SUFFICIENCY-0: what the three tests share (the sheet: research/law-sufficiency/SHEET.md).

The texts and their budgets, one reference run, and the projection P. P is fixed here, before any comparison, exactly
as the sheet's section 2 states it: the reference's receipt without its `backend` and `text-seal` lines. A change to P
is a new version of the sheet, made before its run, never a fix after a mismatch."""
import base64
import gzip
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)

from orlog import interp                    # noqa: E402
from orlog.front import compile_bytes      # noqa: E402

BASELINE = os.path.join(ROOT, "tests", "compat", "baseline-v0.jsonl")
TEXTS = os.path.join(ROOT, "tests", "compat", "texts-v0.json.gz")
DROPPED = (b"backend ", b"text-seal ")      # the two lines P removes, and nothing else


def sha(b):
    return hashlib.sha256(b).hexdigest()


def budgets():
    """COMPAT-0's budgets of counted operations, by kind (the baseline's header)."""
    with open(BASELINE, encoding="utf-8") as f:
        return json.loads(f.readline())["budgets"]


def frozen_texts():
    """Every frozen text of COMPAT-0, as (id, kind, raw bytes), in the file's order."""
    with gzip.open(TEXTS) as f:
        d = json.load(f)
    return [(t["id"], t["kind"], base64.b64decode(t["b64"])) for t in d["texts"]]


def example_texts():
    """examples/*.orl and examples/spellings/*.orl as they stand at the starting commit, kind 'example'."""
    out = []
    for folder in ("examples", "examples/spellings"):
        for name in sorted(os.listdir(os.path.join(ROOT, folder))):
            if name.endswith(".orl"):
                with open(os.path.join(ROOT, folder, name), "rb") as f:
                    out.append((folder + "/" + name, "example", f.read()))
    return out


def budget_of(kind, table):
    return table["corpus"] if kind in ("corpus", "example") else table[kind]


def accepted():
    """The texts the compiler accepts, from the frozen set and the examples, each once by its bytes (the first id
    kept): a list of (id, kind, raw, budget). A text the compiler refuses has no law, so no test reads it."""
    table = budgets()
    seen, out = set(), []
    for ident, kind, raw in frozen_texts() + example_texts():
        if raw in seen:
            continue
        seen.add(raw)
        if compile_bytes(raw).ok:
            out.append((ident, kind, raw, budget_of(kind, table)))
    return out


def projection(receipt):
    """P: the receipt without its backend and text-seal lines (SHEET.md section 2)."""
    lines = receipt.split(b"\n")
    kept = [ln for ln in lines if not ln.startswith(DROPPED)]
    if len(kept) != len(lines) - 2:
        raise AssertionError("a receipt without exactly one backend line and one text-seal line")
    return b"\n".join(kept).decode("ascii")


def run(prog, an, law_hex, text_hex, budget, proj=projection):
    """One reference run: P of its receipt, or 'STOPPED <ops>' (the host's budget, no receipt), or 'CRASH <type>'."""
    try:
        it = interp.Interp(prog, an, law_hex, text_hex, budget=budget).run()
    except interp.HostStop as e:
        return "STOPPED %d" % e.ops
    except Exception as e:      # a crash is a result, compared like any other
        return "CRASH %s" % type(e).__name__
    return proj(it.receipt("reference"))


def first_difference(a, b):
    la, lb = a.split("\n"), b.split("\n")
    k = next((i for i in range(min(len(la), len(lb))) if la[i] != lb[i]), min(len(la), len(lb)))
    return "line %d: %r against %r" % (k + 1, la[k] if k < len(la) else "<end>", lb[k] if k < len(lb) else "<end>")

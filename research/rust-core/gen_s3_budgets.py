"""RUST-CORE-0: S3's budget values, fixed before any experiment (SHEET.md Amendment 2; the owner's ruling C2(a)).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_s3_budgets.py --out PATH

For each of S3's 298 texts, in the order of their ids, it does three things:
1. It runs the reference twice, as shipped: each run in a fresh `python -B` process, with `PYTHONHASHSEED=0`, Python's
   default recursion limit, never importing format_check, under the text's own budget and a 60-second limit.
2. It classes the text RESULT, NO-REFERENCE-RESULT or UNSTABLE, by Amendment 1's table.
3. For a RESULT text it draws the budgets B that S3 runs.

The values are the file it writes: research/rust-core/s3-budgets.txt, named in the sheet by its sha256. They are data,
fixed now, so the core's experiment never draws them again. The texts are LAW-SUFFICIENCY's (`common.accepted()`, 290)
and LAW-SUFFICIENCY-1's fixtures (8), read from research/law-sufficiency/. This tool is outside the core author's
reading set (D1). It refuses to write if HEAD is not the starting commit, or if src/, tests/ or vectors/ differ from it.

With `--one BUDGET` it is the child: one reference run of the law text on stdin, its outcome printed."""
import concurrent.futures
import hashlib
import os
import platform
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
SEED = 20261030
PER_TEXT = 20
LIMIT_S = 60


def child(budget):
    """One reference run: the ENV line, then the outcome line. Nothing here imports format_check."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from orlog import interp
    from orlog.front import compile_bytes
    raw = sys.stdin.buffer.read()
    print("ENV python %s %s recursion-limit %d format_check %s" % (
        platform.python_implementation(), platform.python_version(), sys.getrecursionlimit(),
        "imported" if "format_check" in sys.modules else "not-imported"))
    c = compile_bytes(raw)
    if not c.ok:
        print("NOT-ACCEPTED")
        return
    it = interp.Interp(c.prog, c.an, c.law_seal, c.text_seal, trace=True, budget=budget)
    try:
        it.run()
    except interp.HostStop as e:
        trace = hashlib.sha256("\n".join(it.trace).encode("ascii")).hexdigest()
        print("STOPPED ops %d trace %s" % (e.ops, trace))
        return
    lines = it.receipt("reference").decode("ascii").split("\n")
    p = "\n".join(ln for ln in lines if not ln.startswith(("backend ", "text-seal ")))
    status = [ln for ln in lines if ln.startswith("status ")][0][len("status "):]
    ops = int([ln for ln in lines if ln.startswith("ops ")][0][len("ops "):])
    trace = hashlib.sha256("\n".join(it.trace).encode("ascii")).hexdigest()
    print("%s ops %d p %s trace %s" % (status.split(" ")[0], ops, hashlib.sha256(p.encode("ascii")).hexdigest(), trace))


def one_run(raw, budget):
    """(the ENV line, the outcome) of one fresh reference process: the child's line, CRASH <exit>, or TIMEOUT."""
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    try:
        p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--one", str(budget)], input=raw,
                           capture_output=True, cwd=ROOT, env=env, timeout=LIMIT_S)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    out = p.stdout.decode("ascii", "replace").replace("\r\n", "\n").rstrip("\n").split("\n")
    envline = out[0] if out and out[0].startswith("ENV ") else None
    if p.returncode != 0:
        return envline, "CRASH exit %d" % p.returncode
    return envline, out[-1]


def classify(r1, r2):
    """Amendment 1's reference classes: RESULT, NO-REFERENCE-RESULT (both crash or both time out), UNSTABLE."""
    ok = [not (r.startswith("CRASH") or r == "TIMEOUT") for r in (r1, r2)]
    if all(ok) and r1 == r2:
        return "RESULT"
    if (r1.startswith("CRASH") and r2.startswith("CRASH")) or (r1 == "TIMEOUT" and r2 == "TIMEOUT"):
        return "NO-REFERENCE-RESULT"
    return "UNSTABLE"


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def texts():
    """S3's 298 texts as (id, kind, raw, budget), sorted by id."""
    sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
    import common
    table = common.budgets()
    out = list(common.accepted())
    fx = os.path.join(ROOT, "research", "law-sufficiency", "fixtures")
    for n in sorted(os.listdir(fx)):
        if n.endswith(".orl"):
            with open(os.path.join(fx, n), "rb") as f:
                out.append(("fixtures/" + n, "fixture", f.read(), table["fixture"]))
    return sorted(out, key=lambda t: t[0])


def main(path):
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("GEN-S3: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("GEN-S3: src/, tests/ or vectors/ differ from the starting commit")
    ts = texts()
    if len(ts) != 298 or len(set(t[0] for t in ts)) != 298:
        sys.exit("GEN-S3: %d texts, not 298 distinct ids" % len(ts))

    def both(t):
        return [one_run(t[2], t[3]) for _ in (1, 2)]

    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        runs = list(pool.map(both, ts))
    envs = set(e for pair in runs for e, _ in pair if e is not None)
    rng = random.Random(SEED)
    rows, counts, nvalues = [], {}, 0
    for (ident, kind, raw, budget), ((_, r1), (_, r2)) in zip(ts, runs):
        if "NOT-ACCEPTED" in (r1, r2):
            sys.exit("GEN-S3: the front end refuses %s, which S3 lists as accepted" % ident)
        cls = classify(r1, r2)
        counts[cls] = counts.get(cls, 0) + 1
        if cls != "RESULT":
            rows.append("%s %s budget %d class %s run1 %s run2 %s" % (ident, kind, budget, cls, r1.replace(" ", "_"),
                                                                      r2.replace(" ", "_")))
            continue
        words = r1.split(" ")
        n = int(words[words.index("ops") + 1])
        m = min(n, budget)
        values = list(range(m + 1)) if m + 1 <= PER_TEXT else sorted(rng.sample(range(m + 1), PER_TEXT))
        nvalues += len(values)
        rows.append("%s %s budget %d class RESULT %s ops %d max %d B %s" % (
            ident, kind, budget, words[0], n, m, " ".join(str(v) for v in values)))
    head = [
        "# S3's budget values: SHEET.md Amendment 2, fixed before any experiment (the owner's ruling C2(a), 2026-10-30)",
        "# generator research/rust-core/gen_s3_budgets.py sha256 %s" % sha(os.path.abspath(__file__)),
        "# reference at %s: src/orlog/interp.py sha256 %s, src/orlog/numeric_ref.py sha256 %s" % (
            BASE[:7], sha(os.path.join(ROOT, "src", "orlog", "interp.py")),
            sha(os.path.join(ROOT, "src", "orlog", "numeric_ref.py"))),
        "# each reference run: one fresh `python -B` process, PYTHONHASHSEED=0, the default recursion limit, never "
        "importing format_check, the text's own budget, a %d s limit; two runs per text" % LIMIT_S,
        "# environment, as each run reported it: %s; %s %s" % (" | ".join(sorted(envs)), platform.system(),
                                                              platform.release()),
        "# texts %d, sorted by id; classes %s; seed %d through the RESULT texts in this order; per text every B from 0 "
        "to max = min(ops, budget) when there are at most %d, else %d drawn by random.Random(seed).sample, sorted; "
        "%d values in all" % (len(ts), ", ".join("%s %d" % kv for kv in sorted(counts.items())), SEED, PER_TEXT,
                              PER_TEXT, nvalues),
        "# a row: id kind budget <b> class <class> then, for RESULT, the run's status word, ops, max and the values B; "
        "otherwise both runs' outcomes",
    ]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(path, "wb") as f:
        f.write(data)
    print("GEN-S3: %d texts; %s; %d values; envs %d; sha256 %s" % (
        len(ts), ", ".join("%s %d" % kv for kv in sorted(counts.items())), nvalues, len(envs),
        hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--one":
        child(int(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "--out":
        main(sys.argv[2])
    else:
        sys.exit("usage: gen_s3_budgets.py --out PATH")

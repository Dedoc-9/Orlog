"""COMPAT-0, the conservative-extension gate: every text version 0 accepted keeps its law and its run.

  PYTHONHASHSEED=0 python -B tests/compat.py check [--jobs N]
  PYTHONHASHSEED=0 python -B tests/compat.py history REV [REV ...]
  PYTHONHASHSEED=0 python -B tests/compat.py selftest
  PYTHONHASHSEED=0 python -B tests/compat.py freeze --version v0 --note TEXT      (once per version; a person's act)

A frozen set of texts (tests/compat/texts-v0.json.gz) was compiled and run on the reference at one commit, and each
text's result was recorded (tests/compat/baseline-v0.jsonl): its refusal code and line, or its law seal, its text seal
and the sha256 of the core of its reference receipt, under a budget of counted operations (a run past it is recorded as
stopped, at its operation). The set holds every version of every corpus program in the history, the twin's 291
hand-worked probes, the red team's and E21's fixtures, the twin's inputs, and 3,000 mutants.

`check` computes every result again with this tree and compares. A text version 0 refused may now be accepted: that is
an extension, counted and listed. Every other change fails the gate, unless it is declared, with its reason and the
amendment that made it, in tests/compat/settled.json. A changed frozen text fails as INPUT CHANGED, never as a change of
the compiler. `history` computes the results under each named revision's src (taken from git, the working tree
untouched), so the gate's record runs back through the history. `selftest` plants defects and requires each caught.

Law seals alone are not enough: a change in what a law does can leave every law seal where it was. The receipt core
covers the run (status, output, events, trace head, operations, claims), and the plant say-counts-twice shows a change
that only the receipts see.

What this gate does not protect is in tests/compat/README.md. In brief: timings, memory over long runs, the arbiter,
the backends, texts outside the frozen set, the door's events, the court's readings, other hosts, and the baseline's
own correctness (it freezes what one commit did, defects included).
"""
import argparse
import base64
import gzip
import hashlib
import io
import json
import os
import random
import subprocess
import sys
import tarfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HERE = os.path.join(ROOT, "tests", "compat")
KINDS = ("corpus", "probe", "fixture", "mutant")
BUDGETS = {"corpus": 10 ** 7, "probe": 10 ** 6, "fixture": 10 ** 6, "mutant": 10 ** 6}
N_MUTANTS, MUTANT_SEED = 3000, 1


def sha(b):
    return hashlib.sha256(b).hexdigest()


def paths(version):
    return (os.path.join(HERE, "texts-%s.json.gz" % version), os.path.join(HERE, "baseline-%s.jsonl" % version),
            os.path.join(HERE, "settled.json"))


# ------------------------------------------------------------------------------------------------ one text's result
def receipt_core(b):
    """The receipt with its second line ('backend <name>') removed, written here so that the gate runs on any
    revision's src. It is laxer than the arbiter's (no check of the head, the final LF or a CR), and that laxity
    reaches no verdict: every framing change still reads as another core (measured by the reporting pass)."""
    first, _, rest = b.partition(b"\n")
    second, _, rest = rest.partition(b"\n")
    if not second.startswith(b"backend "):
        return None
    return first + b"\n" + rest


def result_of(raw, budget):
    """The text's result under the src on sys.path: refused (code, line), or the seals and the receipt core's sha256,
    or stopped (the host's budget ran out at that operation), or a crash (a defect, frozen as found)."""
    import inspect
    from orlog.front import compile_bytes
    from orlog import interp
    try:
        comp = compile_bytes(raw)
    except Exception as e:      # a crash of the compiler is a result too: it is frozen, and flagged
        return {"crash": "compile " + type(e).__name__}
    if not comp.ok:
        return {"refused": comp.error.code, "line": comp.error.line}
    out = {"law": comp.law_seal, "text": comp.text_seal}
    has_budget = "budget" in inspect.signature(interp.Interp.__init__).parameters
    try:
        if has_budget:
            it = interp.Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget=budget).run()
        elif budget is None:
            it = interp.Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
        else:
            out["skipped"] = "no host budget at this revision"
            return out
    except Exception as e:
        if type(e).__name__ == "HostStop":
            out["stopped"] = e.ops
            return out
        out["crash"] = "run " + type(e).__name__
        return out
    core = receipt_core(it.receipt("reference"))
    out["status"] = it.status
    out["receipt_core"] = sha(core) if core is not None else "MALFORMED"
    return out


def _work(item):
    ident, raw_b64, budget = item
    return ident, result_of(base64.b64decode(raw_b64), budget)


def _init(src):
    sys.path.insert(0, src)


def compute(texts, budgets, jobs=1, src=None, only_budget_known=None):
    """{id: result} for every text. With jobs > 1 the texts are spread over processes; the results do not depend on
    how (each text is computed alone). only_budget_known, for revisions without a host budget: the ids whose baseline
    finished within its budget, which are run unbounded; the others are skipped."""
    items = []
    for t in texts:
        budget = budgets[t["kind"]]
        if only_budget_known is not None:
            budget = None if t["id"] in only_budget_known else budget
        items.append((t["id"], t["b64"], budget))
    if jobs <= 1:
        return dict(_work(i) for i in items)
    import multiprocessing
    with multiprocessing.get_context("spawn").Pool(jobs, initializer=_init, initargs=(src or os.path.join(ROOT, "src"),)) as pool:
        return dict(pool.map(_work, items, chunksize=16))


# ------------------------------------------------------------------------------------------------ the frozen files
def write_gz(path, data):
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0) as gz:
        gz.write(data)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def load_texts(version):
    path = paths(version)[0]
    with open(path, "rb") as fh:
        blob = fh.read()
    doc = json.loads(gzip.decompress(blob).decode("utf-8"))
    for t in doc["texts"]:
        t["raw"] = base64.b64decode(t["b64"])
    return doc, sha(blob)


def load_baseline(version):
    with open(paths(version)[1], "rb") as fh:
        lines = fh.read().decode("utf-8").split("\n")
    head = json.loads(lines[0])
    rows = {}
    for line in lines[1:]:
        if line:
            r = json.loads(line)
            rows[r["id"]] = r
    return head, rows


def load_settled():
    path = paths("v0")[2]
    if not os.path.exists(path):
        return {}
    with open(path, "rb") as fh:
        doc = json.loads(fh.read().decode("utf-8"))
    return {s["id"]: s for s in doc.get("settled", [])}


def baseline_gaps(base, texts, count):
    """What the baseline does not cover: a frozen text without a row was never compared, and HELD was printed over the
    rest (the reporting pass's finding 11). Empty when the rows are exactly the texts, as many as the header counts."""
    ids_b, ids_t = set(base), {t["id"] for t in texts}
    gaps = []
    if len(base) != count:
        gaps.append("the baseline has %d rows and its header counts %d" % (len(base), count))
    if ids_t - ids_b:
        gaps.append("%d frozen text(s) have no baseline row (first: %s)" % (len(ids_t - ids_b), min(ids_t - ids_b)))
    if ids_b - ids_t:
        gaps.append("%d baseline row(s) have no frozen text (first: %s)" % (len(ids_b - ids_t), min(ids_b - ids_t)))
    return gaps


def settled_gaps(settled):
    """A settled entry settles a change only with its reason and its amendment (README: {"id", "now", "reason",
    "amendment"}); one with either empty settles nothing (finding 11)."""
    def said(v):
        return isinstance(v, str) and v.strip() != ""
    return ["%s: a settled entry needs its reason and its amendment" % i for i, s in sorted(settled.items())
            if not (said(s.get("reason")) and said(s.get("amendment")))]


# ------------------------------------------------------------------------------------------------ comparing
def compare(base, results, texts, settled):
    """Each text's verdict: same, accepted (refused at the baseline, accepted now: an extension), settled (a declared
    change), skipped (this revision cannot run it), input-changed, or differs."""
    by_id = {t["id"]: t for t in texts}
    verdicts = {}
    for ident, row in sorted(base.items()):
        t = by_id.get(ident)
        if t is None or sha(t["raw"]) != row["sha256"]:
            verdicts[ident] = ("input-changed", row["result"], None)
            continue
        got = results[ident]
        want = row["result"]
        if got == want:
            verdicts[ident] = ("same", want, got)
        elif "skipped" in got and {k: v for k, v in got.items() if k != "skipped"} == \
                {k: want[k] for k in ("law", "text") if k in want}:
            verdicts[ident] = ("skipped", want, got)
        elif "refused" in want and "refused" not in got and "crash" not in got:
            verdicts[ident] = ("accepted", want, got)
        elif ident in settled and not settled_gaps({ident: settled[ident]}) and settled[ident].get("now") == got:
            verdicts[ident] = ("settled", want, got)
        else:
            verdicts[ident] = ("differs", want, got)
    return verdicts


def show(r):
    if r is None:
        return "-"
    if "refused" in r:
        return "refused %s at line %s" % (r["refused"], r["line"])
    if "crash" in r:
        return "CRASH (%s)" % r["crash"]
    s = "law %s text %s" % (r["law"][:12], r["text"][:12])
    if "stopped" in r:
        return s + " stopped by the host at operation %d" % r["stopped"]
    if "skipped" in r:
        return s + " run skipped (%s)" % r["skipped"]
    return s + " %s receipt %s" % (r["status"], r["receipt_core"][:12])


def summary(verdicts, texts):
    kinds = {t["id"]: t["kind"] for t in texts}
    counts, by_kind = {}, {}
    for ident, (v, _, _) in verdicts.items():
        counts[v] = counts.get(v, 0) + 1
        k = kinds.get(ident, "?")
        tot = by_kind.setdefault(k, [0, 0])
        tot[1] += 1
        tot[0] += v in ("same", "accepted", "settled")
    return counts, by_kind


def report(verdicts, texts, limit=12, settled=None):
    counts, by_kind = summary(verdicts, texts)
    print("  same %d, newly accepted %d, settled %d, skipped %d, differ %d, input changed %d" % tuple(
        counts.get(k, 0) for k in ("same", "accepted", "settled", "skipped", "differs", "input-changed")))
    print("  by kind: " + ", ".join("%s %d of %d held" % (k, by_kind[k][0], by_kind[k][1]) for k in KINDS
                                    if k in by_kind))
    for ident, (v, want, got) in sorted(verdicts.items()):     # every settled text named, never only counted
        if v == "settled":
            s = (settled or {}).get(ident, {})
            print("    SETTLED %s: was %s; now %s (%s; %s)" % (ident, show(want), show(got), s.get("reason"),
                                                              s.get("amendment")))
    shown = 0
    for ident, (v, want, got) in sorted(verdicts.items()):
        if v in ("differs", "input-changed", "accepted") and shown < limit:
            print("    %s %s: was %s; now %s" % (v.upper(), ident, show(want), show(got)))
            shown += 1
    return counts


# ------------------------------------------------------------------------------------------------ commands
def cmd_check(a):
    sys.path.insert(0, os.path.join(ROOT, "src"))
    doc, texts_sha = load_texts(a.version)
    head, base = load_baseline(a.version)
    if texts_sha != head["texts_sha256"]:
        print("COMPAT-0 BROKEN: tests/compat/texts-%s.json.gz is not the file the baseline was made from (sha256 %s, "
              "the baseline names %s)" % (a.version, texts_sha[:16], head["texts_sha256"][:16]))
        return 1
    settled = load_settled()
    gaps = baseline_gaps(base, doc["texts"], head["count"]) + settled_gaps(settled)
    if gaps:
        print("COMPAT-0 BROKEN: %s" % "; ".join(gaps))
        return 1
    results = compute(doc["texts"], head["budgets"], jobs=a.jobs)
    verdicts = compare(base, results, doc["texts"], settled)
    print("COMPAT-0 baseline %s (made at commit %s; %d texts; texts sha256 %s)" % (
        a.version, head["commit"][:7], len(base), texts_sha[:16]))
    counts = report(verdicts, doc["texts"], settled=settled)
    bad = counts.get("differs", 0) + counts.get("input-changed", 0)
    crashes = sorted(i for i, r in base.items() if "crash" in r["result"])
    if crashes:
        print("  the baseline froze %d crash(es), defects to repair and settle: %s" % (len(crashes), crashes[:5]))
    print("COMPAT-0 HELD" if bad == 0 else "COMPAT-0 BROKEN: %d text(s) changed" % bad)
    return 0 if bad == 0 else 1


def export_src(rev):
    shaid = subprocess.run(["git", "-C", ROOT, "rev-parse", "--verify", rev + "^{commit}"], capture_output=True,
                           text=True, check=True).stdout.strip()
    dst = os.path.join(ROOT, "build", "compat-src-" + shaid[:12])
    if not os.path.isdir(os.path.join(dst, "src")):
        data = subprocess.run(["git", "-C", ROOT, "archive", shaid, "src"], capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(dst, filter="data")
    return shaid, os.path.join(dst, "src")


def cmd_results(a):
    """Internal: the results under another src, written as JSON (history runs this in a fresh process)."""
    sys.path.insert(0, a.src)
    doc, _ = load_texts(a.version)
    head, base = load_baseline(a.version)
    known = set(i for i, r in base.items() if "stopped" not in r["result"])
    import inspect
    from orlog import interp
    has_budget = "budget" in inspect.signature(interp.Interp.__init__).parameters
    results = compute(doc["texts"], head["budgets"], jobs=a.jobs, src=a.src,
                      only_budget_known=None if has_budget else known)
    with open(a.out, "wb") as fh:
        fh.write(json.dumps(results, sort_keys=True).encode("ascii"))
    return 0


def cmd_history(a):
    doc, texts_sha = load_texts(a.version)
    head, base = load_baseline(a.version)
    settled = load_settled()
    gaps = baseline_gaps(base, doc["texts"], head["count"]) + settled_gaps(settled)
    if gaps:
        print("COMPAT-0 HISTORY INCOMPLETE: %s" % "; ".join(gaps))
        return 1
    print("COMPAT-0 history: the %d frozen texts under each revision's src (from git), against baseline %s "
          "(commit %s)" % (len(base), a.version, head["commit"][:7]))
    corpus = sorted(i for i in base if i.startswith("corpus/"))
    table, worst, tally = {}, 0, []
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    for rev in a.revs:
        shaid, src = export_src(rev)
        out = os.path.join(ROOT, "build", "compat-results-%s.json" % shaid[:12])
        r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "results", "--src", src, "--out", out,
                            "--version", a.version, "--jobs", str(a.jobs)], env=env, capture_output=True, text=True,
                           encoding="utf-8")
        if r.returncode:
            print("== %s (%s): could not compute: %s" % (rev, shaid[:7], (r.stderr or r.stdout)[-400:]))
            worst = 1
            continue
        with open(out, "rb") as fh:
            results = json.loads(fh.read().decode("ascii"))
        verdicts = compare(base, results, doc["texts"], settled)
        print("== %s (%s)" % (rev, shaid[:7]))
        counts = report(verdicts, doc["texts"], settled=settled)
        tally.append("%s %d differ" % (rev, counts.get("differs", 0) + counts.get("input-changed", 0)))
        table[rev] = results
    print("the corpus, every version in the history (law seal / text seal / receipt core, first 12 hex digits):")
    for ident in corpus:
        cells = []
        for rev in a.revs:
            r = table.get(rev, {}).get(ident)
            cells.append("%s/%s/%s" % (r["law"][:12], r["text"][:12], r.get("receipt_core", "skipped")[:12])
                         if r and "law" in r else show(r))
        same = len(set(cells)) == 1
        print("  %-48s %s  %s" % (ident, "same under all" if same else "DIFFERS", cells[0] if same else
                                  " | ".join(cells)))
    # history is an audit, not the gate: a difference here is a fact about the past, to be explained in writing
    print("COMPAT-0 HISTORY %s: %s" % ("COMPUTED" if not worst else "INCOMPLETE", "; ".join(tally)))
    return 0 if not worst else 1


def selftest_texts(doc):
    return [t for t in doc["texts"] if t["kind"] != "mutant"]


def cmd_selftest(a):
    """Plants: each is a defect the gate exists to catch, and each must be caught by its own witness."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import orlog.front as front
    import orlog.syntax as syntax
    import orlog.interp as interp
    doc, _ = load_texts(a.version)
    head, base = load_baseline(a.version)
    texts = selftest_texts(doc)
    sub = {t["id"]: base[t["id"]] for t in texts}
    rows = []

    def run():
        return compare(sub, compute(texts, head["budgets"]), texts, {})

    def moved(verdicts, key):
        return [i for i, (v, want, got) in verdicts.items() if v == "differs" and want and got and key in want
                and key in got and want[key] != got[key]]

    v = run()
    control = [i for i, (k, _, _) in v.items() if k != "same"]
    rows.append(("control: no plant, every non-mutant text the same", not control, "%d differ" % len(control)))
    # 1. a new reserved word that an existing program uses as a name
    syntax.RESERVED.add("tick")
    try:
        v = run()
    finally:
        syntax.RESERVED.discard("tick")
    fall = [(i, show(got)) for i, (k, _, got) in v.items() if k == "differs" and "fall.orl" in i]
    rows.append(("plant reserve-tick (fall.orl names its loop variable tick)", bool(fall),
                 "%s now %s" % fall[0] if fall else "no fall.orl text differs"))
    # the exceptions file: a change declared with its exact new result reads settled; one declared otherwise does not
    if fall:
        ident = fall[0][0]
        got = v[ident][2]
        syntax.RESERVED.add("tick")
        try:
            results = compute(texts, head["budgets"])
        finally:
            syntax.RESERVED.discard("tick")
        why = {"reason": "the self-test's plant reserve-tick", "amendment": "none: a self-test fixture"}
        right = compare(sub, results, texts, {ident: dict(why, id=ident, now=got)})[ident][0]
        wrong = compare(sub, results, texts, {ident: dict(why, id=ident, now=dict(got, line=got.get("line", 0) + 1))})[
            ident][0]
        rows.append(("settled: a declared change passes only with its exact new result", right == "settled" and
                     wrong == "differs", "declared exactly: %s; declared one line off: %s" % (right, wrong)))
        # 5. a declared change with no reason and no amendment settles nothing (the reporting pass's finding 11)
        bare = {ident: {"id": ident, "now": got}}
        verdict = compare(sub, results, texts, bare)[ident][0]
        rows.append(("plant settled-without-reason (declared exactly, with no reason and no amendment)",
                     verdict == "differs" and bool(settled_gaps(bare)),
                     "it reads %s, and the check names it: %s" % (verdict, "; ".join(settled_gaps(bare)))))
    # 2. one law line spelled differently: every law seal moves
    saved_law = front.law_bytes

    def law_bytes(prog, an):
        return saved_law(prog, an).replace(b"(decimals ", b"(decimal ")
    front.law_bytes = law_bytes
    try:
        v = run()
    finally:
        front.law_bytes = saved_law
    accepted = [i for i, r in sub.items() if "law" in r["result"]]
    laws = moved(v, "law")
    # a text that carries its own seal line is refused SEAL-MISMATCH instead: its seal words no longer match
    sealed = [i for i in accepted if v[i][0] == "differs" and (v[i][2] or {}).get("refused") == "SEAL-MISMATCH"]
    rows.append(("plant law-line-format ('(decimals' spelled '(decimal')",
                 bool(accepted) and len(laws) + len(sealed) == len(accepted),
                 "of %d accepted texts, %d law seals moved and %d sealed text(s) now refused SEAL-MISMATCH (%s)"
                 % (len(accepted), len(laws), len(sealed), ", ".join(i.split("/")[-1] for i in sealed))))
    # 3. the reference counts one operation more per Say: no law seal moves, and only the receipts see it
    saved_stmt = interp.Interp.stmt

    def stmt(self, c, s):
        saved_stmt(self, c, s)
        if type(s).__name__ == "Say":
            self.ops += 1
    interp.Interp.stmt = stmt
    try:
        v = run()
    finally:
        interp.Interp.stmt = saved_stmt
    laws, cores = moved(v, "law"), moved(v, "receipt_core")
    rows.append(("plant say-counts-twice (a change only the receipts see)", not laws and bool(cores),
                 "%d law seals moved, %d receipt cores moved" % (len(laws), len(cores))))
    # 4. a frozen text altered: the gate reports the input, not the compiler
    victim = texts[0]
    altered = [dict(t, raw=t["raw"] + b"\n") if t is victim else t for t in texts]
    v = compare(sub, compute(altered, head["budgets"]), altered, {})
    changed = [i for i, (k, _, _) in v.items() if k == "input-changed"]
    rows.append(("plant frozen-text-altered", changed == [victim["id"]], "input changed: %s" % changed))
    # 6. a baseline row removed: its text would never be compared, so the gate refuses before comparing anything (the
    # reporting pass's finding 11, where one row removed read HELD over the other 3,360)
    short = dict(sub)
    short.pop(sorted(short)[0])
    gaps = baseline_gaps(short, texts, len(texts))
    rows.append(("plant baseline-row-removed", not baseline_gaps(sub, texts, len(texts)) and bool(gaps),
                 "; ".join(gaps) or "no gap found"))
    ok = 0
    for name, caught, witness in rows:
        print("[%s] %s: %s -- %s" % ("PASS" if caught else "FAIL", name, "CAUGHT" if caught and name.startswith(
            "plant") else ("HELD" if caught else "NOT CAUGHT" if name.startswith("plant") else "BROKEN"), witness))
        ok += bool(caught)
    print("COMPAT SELFTEST %d/%d" % (ok, len(rows)))
    return 0 if ok == len(rows) else 1


# ------------------------------------------------------------------------------------------------ freezing
def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, check=True).stdout


def corpus_versions():
    """Every version of every corpus program in the history reachable from HEAD, by its bytes."""
    seen, out = set(), []
    for rev in git("rev-list", "--reverse", "HEAD").decode("ascii").split():
        for p in sorted(git("ls-tree", "-r", "--name-only", rev, "--", "examples").decode("utf-8").split("\n")):
            if p.endswith(".orl"):
                raw = git("show", "%s:%s" % (rev, p))
                h = sha(raw)
                if h not in seen:
                    seen.add(h)
                    out.append({"id": "corpus/%s@%s" % (p, h[:12]), "kind": "corpus", "raw": raw})
    return out


def files(kind, *patterns):
    import glob
    out = []
    for pat in patterns:
        for p in sorted(glob.glob(os.path.join(ROOT, pat))):
            with open(p, "rb") as fh:
                rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
                out.append({"id": "%s/%s" % (kind, rel), "kind": kind, "raw": fh.read()})
    return out


def mutants(n=N_MUTANTS, seed=MUTANT_SEED):
    """diff_twin's mutants, made exactly as its own run makes them (the same pool, generator and random sequence)."""
    sys.path.insert(0, os.path.join(ROOT, "tests"))
    import diff_twin as D
    from orlog.canon import canonicalize
    pool = D.seeds()
    rng = random.Random(seed)
    mut = D.Mutator(rng, pool)
    seen = set(sha(t.encode("utf-8")) for t in pool)
    out, attempts = [], 0
    while len(out) < n and attempts < 20 * n:
        attempts += 1
        m = mut.mutate(rng.choice(pool))
        c = canonicalize(m.encode("utf-8"))
        if c.text is None:
            continue
        b = c.text.encode("utf-8")
        if sha(b) in seen:
            continue
        seen.add(sha(b))
        out.append({"id": "mutant/s%d/%04d" % (seed, len(out)), "kind": "mutant", "raw": b})
    return out


def cmd_freeze(a):
    texts_path, base_path, settled_path = paths(a.version)
    if os.path.exists(texts_path) or os.path.exists(base_path):
        print("refused: version %s is frozen already; a new baseline is a new version, never a rewrite" % a.version)
        return 1
    if git("status", "--porcelain", "--", "src").strip():
        print("refused: src/ has uncommitted changes; a baseline is of a committed compiler")
        return 1
    if not a.note:
        print("refused: a freeze needs --note: say why, and at whose word")
        return 1
    sys.path.insert(0, os.path.join(ROOT, "src"))
    commit = git("rev-parse", "HEAD").decode("ascii").strip()
    texts = corpus_versions() + files("probe", "twin/probes/*.orl", "twin/probes3/*.orl") + files(
        "fixture", "tests/fixtures/redteam/*.orl", "tests/fixtures/redteam/*.raw", "tests/fixtures/e21/*.orl",
        "twin/inputs/*.orl") + mutants()
    for t in texts:
        t["b64"] = base64.b64encode(t["raw"]).decode("ascii")
    os.makedirs(HERE, exist_ok=True)
    doc = {"version": "compat-texts 0", "commit": commit, "note": a.note,
           "texts": [{"id": t["id"], "kind": t["kind"], "b64": t["b64"]} for t in texts]}
    write_gz(texts_path, json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("ascii"))
    with open(texts_path, "rb") as fh:
        texts_sha = sha(fh.read())
    results = compute(texts, BUDGETS, jobs=a.jobs)
    lines = [json.dumps({"version": "compat-baseline 0", "commit": commit, "texts_sha256": texts_sha,
                         "budgets": BUDGETS, "count": len(texts), "note": a.note}, sort_keys=True)]
    for t in sorted(texts, key=lambda t: t["id"]):
        lines.append(json.dumps({"id": t["id"], "sha256": sha(t["raw"]), "result": results[t["id"]]},
                                sort_keys=True))
    with open(base_path, "wb") as fh:
        fh.write(("\n".join(lines) + "\n").encode("ascii"))
    if not os.path.exists(settled_path):
        with open(settled_path, "wb") as fh:
            fh.write(json.dumps({"version": "compat-settled 0", "settled": []}, indent=1).encode("ascii") + b"\n")
    counts = {}
    for r in results.values():
        k = next(k for k in ("refused", "crash", "stopped", "status") if k in r)
        counts[k] = counts.get(k, 0) + 1
    print("froze %s: %d texts (%s) at commit %s; texts sha256 %s; results %s" % (
        a.version, len(texts), ", ".join("%s %d" % (k, sum(1 for t in texts if t["kind"] == k)) for k in KINDS),
        commit[:7], texts_sha[:16], counts))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="compat")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "selftest", "history", "freeze", "results"):
        p = sub.add_parser(name)
        p.add_argument("--version", default="v0")
        p.add_argument("--jobs", type=int, default=1)
        if name == "history":
            p.add_argument("revs", nargs="+")
        if name == "freeze":
            p.add_argument("--note")
        if name == "results":
            p.add_argument("--src", required=True)
            p.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    return {"check": cmd_check, "selftest": cmd_selftest, "history": cmd_history, "freeze": cmd_freeze,
            "results": cmd_results}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

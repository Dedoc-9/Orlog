"""Differential run of the reference against the clean-room twin, on mutants of every program the project has.

  python -B tests/diff_twin.py [--n 3000] [--seed 1] [--jobs 8] [--minimize]

The theorem under discussion (T-TWIN): two implementations written apart from one specification that disagree on a
text locate a place where at least one of them departs from the specification, or where it does not decide. The
converse is not claimed: agreement on every text tried shows neither is right. Both were written by one model family,
so they share priors (the verification paradox this language exists for): the run finds slips and undecided
readings, never a misreading both make.

Seeds: examples/, examples/spellings/, twin/probes/, twin/inputs/, tests/fixtures/redteam/. Each mutant is one to
three mutations of a seed (lines deleted, doubled, swapped, moved or relabelled; tokens deleted, doubled, replaced,
inserted, swapped or recased; numbers replaced by edge values; lines spliced from another seed; Title, Note and
Sealed lines inserted, a Sealed line sometimes with the true seal words; periods and check suffixes changed). A
mutant is kept only if the reference's door accepts it (the twin takes canonical text and has no door), and only
once (by its sha256). Results are memoized in work/difftwin/cache.json, keyed by the sha256 of both implementations'
sources, so a rerun after a change starts again and a rerun without one costs nothing.

Every disagreement is classed by a signature (the two codes, a crash, or the receipt lines that differ) and, with
--minimize, its shortest example is reduced line by line and token by token while the signature holds. The report is
work/difftwin/report.md and report.json.
"""
import argparse
import concurrent.futures
import glob
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.canon import canonicalize  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.seal import line_check  # noqa: E402

OUT = os.path.join(ROOT, "work", "difftwin")
WORKER = os.path.join(ROOT, "tests", "diff_worker.py")
TOKEN = re.compile(r'§[0-9]+(?:\.[0-9]+)*|[0-9]+(?:\.[0-9]+)?|"(?:[^"]|"")*"|[A-Za-z][A-Za-z0-9_]*|<=|>=|!=|\S')
LABEL = re.compile(r"^(§[0-9]+(?:\.[0-9]+)*|[0-9]+(?:\.[0-9]+)*\.) (.*)$")
EDGE_NUMBERS = ["0", "1", "2", "3", "7", "10", "64", "1000", "4611686018427387904", "4611686018427387905",
                "9223372036854775807", "9223372036854775808", "18446744073709551616", "0.5", "0.1", "1.0", "2.5",
                "3.14159", "0.0000000001", "2147483648.0000000001", "9223372036854775807.5",
                "1" + "0" * 308 + ".0", "1" + "0" * 309 + ".0", "0." + "0" * 330 + "1"]
OPS = ["(", ")", ",", ";", ":", "-", "+", "*", "/", "<", ">", "=", "<=", ">=", "!=", "'"]
STRINGS = ['"a"', '""', '"x y"', '"a""b"', '"' + "z" * 40 + '"']
PROQUINT_C, PROQUINT_V = "bdfghjklmnprstvz", "aiou"
SOURCES = ["src/orlog/canon.py", "src/orlog/syntax.py", "src/orlog/sema.py", "src/orlog/front.py",
           "src/orlog/interp.py", "src/orlog/numeric_ref.py", "src/orlog/seal.py", "src/orlog/arbiter.py",
           "twin/twin.py", "tests/diff_worker.py"]


def sources_key():
    h = hashlib.sha256()
    for p in SOURCES:
        with open(os.path.join(ROOT, p), "rb") as fh:
            h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def seeds():
    paths = []
    for pat in ("examples/*.orl", "examples/spellings/*.orl", "twin/probes/*.orl", "twin/inputs/*.orl",
                "tests/fixtures/redteam/*.orl"):
        paths += sorted(glob.glob(os.path.join(ROOT, pat)))
    out = []
    for p in paths:
        with open(p, "rb") as fh:
            c = canonicalize(fh.read())
        if c.text:
            out.append(c.text)
    return out


class Mutator:
    def __init__(self, rng, pool):
        self.rng, self.pool = rng, pool
        words = set()
        for t in pool:
            words.update(w for w in re.findall(r"[A-Za-z][A-Za-z0-9_]*", t))
        self.words = sorted(words)

    def vocab(self):
        r = self.rng.random()
        if r < 0.45:
            return self.rng.choice(self.words)
        if r < 0.65:
            return self.rng.choice(EDGE_NUMBERS)
        if r < 0.85:
            return self.rng.choice(OPS)
        if r < 0.93:
            return self.rng.choice(STRINGS)
        return "§%d" % self.rng.randint(1, 6) + (".%d" % self.rng.randint(1, 3) if self.rng.random() < 0.4 else "")

    def proquints(self):
        r = self.rng
        return "-".join("".join(r.choice(PROQUINT_C if k % 2 == 0 else PROQUINT_V) for k in range(5))
                        for _ in range(4))

    def clause_lines(self, lines):
        return [i for i, l in enumerate(lines) if LABEL.match(l)]

    def mutate(self, text):
        lines = text.rstrip("\n").split("\n")
        for _ in range(self.rng.choice((1, 1, 2, 3))):
            lines = getattr(self, "m_" + self.rng.choice(MUTATIONS))(lines) or lines
            if not lines:
                lines = ["§1 Say 1."]
        return "\n".join(lines) + "\n"

    # -- line mutations
    def m_del_line(self, lines):
        if len(lines) > 1:
            del lines[self.rng.randrange(len(lines))]
        return lines

    def m_dup_line(self, lines):
        i = self.rng.randrange(len(lines))
        lines.insert(i, lines[i])
        return lines

    def m_swap_lines(self, lines):
        if len(lines) > 1:
            i = self.rng.randrange(len(lines) - 1)
            lines[i], lines[i + 1] = lines[i + 1], lines[i]
        return lines

    def m_move_line(self, lines):
        if len(lines) > 1:
            l = lines.pop(self.rng.randrange(len(lines)))
            lines.insert(self.rng.randrange(len(lines) + 1), l)
        return lines

    def m_relabel(self, lines):
        idx = self.clause_lines(lines)
        if not idx:
            return lines
        i = self.rng.choice(idx)
        m = LABEL.match(lines[i])
        lab, rest = m.group(1), m.group(2)
        sec = lab.startswith("§")
        parts = [int(p) for p in (lab[1:] if sec else lab[:-1]).split(".")]
        k = self.rng.randrange(4)
        if k == 0:
            parts[-1] = max(0, parts[-1] + self.rng.choice((-1, 1)))
        elif k == 1:
            parts.append(1)
        elif k == 2 and len(parts) > 1:
            parts.pop()
        else:
            sec = not sec
        body = ".".join(str(p) for p in parts)
        lines[i] = ("§" + body if sec else body + ".") + " " + rest
        return lines

    def m_splice(self, lines):
        other = self.rng.choice(self.pool).rstrip("\n").split("\n")
        cand = [l for l in other if LABEL.match(l)]
        if not cand:
            return lines
        l = self.rng.choice(cand)
        if self.rng.random() < 0.6 and self.clause_lines(lines):
            j = self.rng.choice(self.clause_lines(lines))
            lab = LABEL.match(lines[j]).group(1)
            l = lab + " " + LABEL.match(l).group(2)
            lines.insert(j + 1, l)
        else:
            lines.insert(self.rng.randrange(len(lines) + 1), l)
        return lines

    def m_structural(self, lines):
        k = self.rng.randrange(5)
        if k == 0:
            l = "Title: " + self.rng.choice(("a", "the law", "x."))
        elif k == 1:
            l = "Note: " + self.rng.choice(("n", "a note", ""))
        elif k == 2:
            l = "Sealed: " + self.proquints() + "."
        elif k == 3:
            c = compile_bytes(("\n".join(lines) + "\n").encode("utf-8"))
            l = "Sealed: " + (c.seal_words if c.ok else self.proquints()) + "."
            lines = [x for x in lines if not x.startswith("Sealed:")]
            lines.append(l)
            return lines
        else:
            l = self.rng.choice(("Sealed:" + self.proquints() + ".", "sealed: " + self.proquints() + ".",
                                 "Title:", "Note:x", "title: a", "Hello", "§", "§1", "1."))
        lines.insert(self.rng.randrange(len(lines) + 1), l)
        return lines

    def m_period(self, lines):
        idx = self.clause_lines(lines)
        if not idx:
            return lines
        i = self.rng.choice(idx)
        l = lines[i]
        k = self.rng.randrange(4)
        if k == 0 and l.endswith("."):
            lines[i] = l[:-1]
        elif k == 1:
            lines[i] = l + "."
        elif k == 2 and l.endswith("."):
            lines[i] = l + " [" + line_check(l) + "]"
        else:
            lines[i] = l + " [" + "".join(self.rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(3)) + "]"
        return lines

    # -- token mutations, inside one clause's statement
    def tokens_of(self, lines):
        idx = self.clause_lines(lines)
        if not idx:
            return None, None, None
        i = self.rng.choice(idx)
        m = LABEL.match(lines[i])
        body = m.group(2)
        end = "." if body.endswith(".") else ""
        toks = TOKEN.findall(body[:-1] if end else body)
        return i, m.group(1), (toks, end)

    def put(self, lines, i, lab, toks, end):
        lines[i] = lab + " " + " ".join(toks) + end
        return lines

    def m_tok_delete(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None or not te[0]:
            return lines
        toks, end = te
        del toks[self.rng.randrange(len(toks))]
        return self.put(lines, i, lab, toks, end) if toks else lines

    def m_tok_dup(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None or not te[0]:
            return lines
        toks, end = te
        j = self.rng.randrange(len(toks))
        toks.insert(j, toks[j])
        return self.put(lines, i, lab, toks, end)

    def m_tok_replace(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None or not te[0]:
            return lines
        toks, end = te
        toks[self.rng.randrange(len(toks))] = self.vocab()
        return self.put(lines, i, lab, toks, end)

    def m_tok_insert(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None:
            return lines
        toks, end = te
        toks.insert(self.rng.randrange(len(toks) + 1), self.vocab())
        return self.put(lines, i, lab, toks, end)

    def m_tok_swap(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None or len(te[0]) < 2:
            return lines
        toks, end = te
        j = self.rng.randrange(len(toks) - 1)
        toks[j], toks[j + 1] = toks[j + 1], toks[j]
        return self.put(lines, i, lab, toks, end)

    def m_tok_case(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None:
            return lines
        toks, end = te
        ws = [k for k, t in enumerate(toks) if t[:1].isalpha()]
        if not ws:
            return lines
        k = self.rng.choice(ws)
        t = toks[k]
        toks[k] = self.rng.choice((t.upper(), t.lower(), t.capitalize(), t.swapcase()))
        return self.put(lines, i, lab, toks, end)

    def m_tok_number(self, lines):
        i, lab, te = self.tokens_of(lines)
        if i is None:
            return lines
        toks, end = te
        ns = [k for k, t in enumerate(toks) if t[:1].isdigit()]
        if not ns:
            return lines
        toks[self.rng.choice(ns)] = self.rng.choice(EDGE_NUMBERS)
        return self.put(lines, i, lab, toks, end)


MUTATIONS = ["del_line", "dup_line", "swap_lines", "move_line", "relabel", "splice", "structural", "period",
             "tok_delete", "tok_dup", "tok_replace", "tok_replace", "tok_insert", "tok_insert", "tok_swap", "tok_case",
             "tok_number"]


def run_batch(texts, timeout):
    """Run the worker on a list of texts; None for a batch that timed out."""
    fd_in, p_in = tempfile.mkstemp(suffix=".json", prefix="difftwin-in-")
    fd_out, p_out = tempfile.mkstemp(suffix=".json", prefix="difftwin-out-")
    os.close(fd_out)
    try:
        with os.fdopen(fd_in, "wb") as fh:
            fh.write(json.dumps(texts).encode("utf-8"))
        env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
        try:
            r = subprocess.run([sys.executable, "-B", WORKER, p_in, p_out], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=env, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None
        if r.returncode != 0:
            return [{"ref": {"crash": "worker exit %d: %s" % (r.returncode, r.stderr.decode("utf-8", "replace")[-300:])},
                     "twin": {"crash": "worker"}} for _ in texts]
        with open(p_out, "rb") as fh:
            return json.loads(fh.read().decode("utf-8"))
    finally:
        for p in (p_in, p_out):
            try:
                os.remove(p)
            except OSError:
                pass


def evaluate(texts, jobs, batch=40, timeout=60, single_timeout=15):
    """Results for every text, in order; a text that times out alone reads {"timeout": True}."""
    chunks = [texts[i:i + batch] for i in range(0, len(texts), batch)]
    results = [None] * len(chunks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(run_batch, ch, timeout): k for k, ch in enumerate(chunks)}
        for f in concurrent.futures.as_completed(futs):
            results[futs[f]] = f.result()
        redo = [k for k, r in enumerate(results) if r is None]
        for k in redo:
            singles = list(ex.map(lambda t: run_batch([t], single_timeout), chunks[k]))
            results[k] = [s[0] if s is not None else {"timeout": True} for s in singles]
    return [r for ch in results for r in ch]


def signature(res):
    if res.get("timeout"):
        return "TIMEOUT"
    ref, twin = res["ref"], res["twin"]
    if "crash" in ref or "crash" in twin:
        return "CRASH ref=%s twin=%s" % (ref.get("crash", "-").split(":")[0], twin.get("crash", "-").split(":")[0])
    rc = ref.get("code") if "code" in ref else "RUN"
    tc = twin.get("code") if "code" in twin else "RUN"
    if rc == "RUN" and tc is None:
        tc = "RUN"
    if rc != tc:
        return "COMPILE ref=%s twin=%s" % (rc, tc or "accepted")
    if rc != "RUN":
        return None
    if ref == twin:
        return None
    rl = (ref.get("core") or "").split("\n")
    tl = (twin.get("core") or "").split("\n")
    diff = sorted(set(a.split(" ")[0] for a, b in zip(rl, tl) if a != b) | ({"lines"} if len(rl) != len(tl) else set()))
    if ref["out_sha256"] != twin["out_sha256"]:
        diff.append("output")
    return "RUN " + ",".join(diff)


def minimize(text, sig, jobs, rounds=60):
    """Shorten a text while its signature holds: delete lines, then tokens (one batch per round)."""
    cur = text
    for _ in range(rounds):
        lines = cur.rstrip("\n").split("\n")
        cands = []
        for i in range(len(lines)):
            if len(lines) > 1:
                cands.append("\n".join(lines[:i] + lines[i + 1:]) + "\n")
        for i, l in enumerate(lines):
            m = LABEL.match(l)
            if not m:
                continue
            body = m.group(2)
            end = "." if body.endswith(".") else ""
            toks = TOKEN.findall(body[:-1] if end else body)
            for j in range(len(toks)):
                if len(toks) > 1:
                    nl = m.group(1) + " " + " ".join(toks[:j] + toks[j + 1:]) + end
                    cands.append("\n".join(lines[:i] + [nl] + lines[i + 1:]) + "\n")
        keep = []
        for c in cands:
            cc = canonicalize(c.encode("utf-8"))
            if cc.text and cc.text != cur:
                keep.append(cc.text)
        if not keep:
            break
        res = evaluate(keep, jobs, batch=20, timeout=60, single_timeout=10)
        better = [c for c, r in zip(keep, res) if signature(r) == sig]
        if not better:
            break
        cur = min(better, key=lambda t: (len(t), t))
    return cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--minimize", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    key = sources_key()
    cache_path = os.path.join(OUT, "cache.json")
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as fh:
            stored = json.loads(fh.read().decode("utf-8"))
        if stored.get("key") == key:
            cache = stored["results"]
    pool = seeds()
    rng = random.Random(a.seed)
    mut = Mutator(rng, pool)
    texts, seen, door_refused, attempts = [], set(), 0, 0
    for t in pool:                   # the seeds themselves first
        h = hashlib.sha256(t.encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            texts.append(t)
    while len(texts) < a.n + len(pool) and attempts < 20 * a.n:
        attempts += 1
        m = mut.mutate(rng.choice(pool))
        c = canonicalize(m.encode("utf-8"))
        if c.text is None:
            door_refused += 1
            continue
        h = hashlib.sha256(c.text.encode("utf-8")).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        texts.append(c.text)
    todo = [t for t in texts if hashlib.sha256(t.encode("utf-8")).hexdigest() not in cache]
    print("difftwin: %d texts (%d seeds, %d mutants; %d mutants refused by the door and not compared); %d to run, "
          "%d memoized" % (len(texts), len(pool), len(texts) - len(pool), door_refused, len(todo),
                           len(texts) - len(todo)), flush=True)
    for t, r in zip(todo, evaluate(todo, a.jobs)):
        cache[hashlib.sha256(t.encode("utf-8")).hexdigest()] = r
    with open(cache_path, "wb") as fh:
        fh.write(json.dumps({"key": key, "results": cache}, sort_keys=True).encode("utf-8"))
    groups, agree_refused, agree_run = {}, 0, 0
    for t in texts:
        r = cache[hashlib.sha256(t.encode("utf-8")).hexdigest()]
        s = signature(r)
        if s is None:
            if "code" in r["ref"]:
                agree_refused += 1
            else:
                agree_run += 1
            continue
        groups.setdefault(s, []).append(t)
    report = {"key": key, "seed": a.seed, "texts": len(texts), "seeds": len(pool), "door_refused": door_refused,
              "agree_refused_same_code": agree_refused, "agree_run_identical": agree_run,
              "disagree": sum(len(v) for v in groups.values()), "signatures": {}}
    for s in sorted(groups, key=lambda k: (-len(groups[k]), k)):
        ex = min(groups[s], key=lambda t: (len(t), t))
        if a.minimize and not s.startswith("TIMEOUT"):
            ex = minimize(ex, s, a.jobs)
        report["signatures"][s] = {"count": len(groups[s]), "example": ex}
    with open(os.path.join(OUT, "report.json"), "wb") as fh:
        fh.write(json.dumps(report, indent=1, sort_keys=True).encode("utf-8"))
    md = ["# Reference against twin: differential run", "",
          "Seed %d; %d texts (%d seeds and their mutants); sources key %s." % (a.seed, len(texts), len(pool), key[:16]),
          "", "- both refused, with the same code: %d" % agree_refused,
          "- both ran, receipts and output byte-identical: %d" % agree_run,
          "- disagree: %d, in %d signatures" % (report["disagree"], len(groups)),
          "- mutants the door refused (not compared; the twin has no door): %d" % door_refused, ""]
    for s, v in report["signatures"].items():
        md += ["## %s (%d)" % (s, v["count"]), "", "```", v["example"].rstrip("\n"), "```", ""]
    with open(os.path.join(OUT, "report.md"), "wb") as fh:
        fh.write(("\n".join(md) + "\n").encode("utf-8"))
    print("difftwin: both refused alike %d; both ran alike %d; disagree %d in %d signatures" %
          (agree_refused, agree_run, report["disagree"], len(groups)))
    for s, v in report["signatures"].items():
        print("  %5d  %s" % (v["count"], s))
    return 0


if __name__ == "__main__":
    sys.exit(main())

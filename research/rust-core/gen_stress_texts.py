"""RUST-CORE-0: S1's and S2's texts and the do-nothing fixtures, fixed before any experiment (SHEET.md Amendment 3;
the owner's ruling E2, and REREAD-3's J15).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_stress_texts.py --out PATH
With `--write DIR` it writes each text and its law bytes into DIR (empty, or made), each held to the manifest's sha256
given as `--manifest PATH`: that is how an experiment gets the texts.

The texts, each made by a function below from its size alone:
- S1, perform chains of n = 300, 600, 3,000, 30,000: procedure p1 says 1; each p_i performs p_(i-1); the last clause
  performs p_n. By construction it completes, says `1`, and counts n + 1 operations.
- S1, rule chains of the same n: rule r1 is 1; each r_i is r_(i-1); the last clause says r_n. By construction it
  completes, says `1`, and counts n + 1 operations.
- S2, doubling rule chains of n = 18, 24, 64 (REREAD-1's texts): r1 is 1; each r_k is the larger of r_(k-1) and
  r_(k-1); then `Say r_n.` and `Say 2.`. The `Say 2.` after it is what lets a budget of 10 stop the run (REREAD-2's C3):
  the stop comes at the check before it.
- The do-nothing fixtures (J15): `Say 1.`, then a last clause that does nothing at run time: a procedure (with its
  body), a define, or a decimals clause. Under a budget of 0 the reference stops at the check before that last clause,
  after 1 operation; under 1 it completes. A core with no check before a do-nothing clause completes under 0.

For each text the manifest records its sha256 and length, and the sha256 and length of the law bytes the front end
writes for it, each read in a fresh `python -B` process at Python's default recursion limit, never importing
format_check. Before it writes, it holds the constructions to the reference, each in a fresh process: S1's chains of
300 must complete, saying `1`, with 301 operations; each do-nothing fixture must stop after 1 operation under a budget
of 0 and complete with 1 under a budget of 1. Every other run belongs to the experiment, which runs its own reference.
It refuses to write if HEAD is not the starting commit, or if src/, tests/ or vectors/ differ from it. It is outside
the core author's reading set (D1)."""
import hashlib
import os
import platform
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
LIMIT_S = 60
S = "§"
ONE = hashlib.sha256(b"1\n").hexdigest()


def perform_chain(n):
    return ("%s1 To p1, do the following.\n%s1.1 Say 1.\n" % (S, S)
            + "".join("%s%d To p%d, do the following.\n%s%d.1 Perform p%d.\n" % (S, i, i, S, i, i - 1)
                      for i in range(2, n + 1))
            + "%s%d Perform p%d.\n" % (S, n + 1, n))


def rule_chain(n):
    return ("%s1 Define r1 as 1.\n" % S + "".join("%s%d Define r%d as r%d.\n" % (S, i, i, i - 1) for i in range(2, n + 1))
            + "%s%d Say r%d.\n" % (S, n + 1, n))


def doubling(n):
    return ("%s1 Define r1 as 1.\n" % S
            + "".join("%s%d Define r%d as the larger of r%d and r%d.\n" % (S, k, k, k - 1, k - 1) for k in range(2, n + 1))
            + "%s%d Say r%d.\n%s%d Say 2.\n" % (S, n + 1, n, S, n + 2))


def texts():
    """(name, prediction, text, what is expected of it)."""
    out = []
    for n in (300, 600, 3000, 30000):
        out.append(("s1-perform-%d" % n, "S1", perform_chain(n), "COMPLETED ops %d output-sha256 %s" % (n + 1, ONE)))
    for n in (300, 600, 3000, 30000):
        out.append(("s1-rule-%d" % n, "S1", rule_chain(n), "COMPLETED ops %d output-sha256 %s" % (n + 1, ONE)))
    for n, expect in ((18, "runs under budgets 10 and none; compared with the reference"),
                      (24, "runs under budgets 10 and none; compared with the reference"),
                      (64, "runs under no budget; recorded as stress evidence only")):   # draft 5, K16
        out.append(("s2-doubling-%d" % n, "S2", doubling(n), expect))
    for name, last in (("procedure", "%s2 To p, do the following.\n%s2.1 Say 2.\n" % (S, S)),
                       ("define", "%s2 Define r as 1.\n" % S), ("decimals", "%s2 Decimals are fixed.\n" % S)):
        out.append(("nothing-%s" % name, "do-nothing", "%s1 Say 1.\n" % S + last,
                    "budget 0 STOPPED ops 1; budget 1 COMPLETED ops 1"))
    return out


def child(mode, budget):
    """In a fresh process: `compile` prints the law bytes' sha256 and length; `run` runs the reference."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from orlog import interp
    from orlog.front import compile_bytes
    raw = sys.stdin.buffer.read()
    print("ENV python %s %s recursion-limit %d format_check %s; %s" % (
        platform.python_implementation(), platform.python_version(), sys.getrecursionlimit(),
        "imported" if "format_check" in sys.modules else "not-imported", platform.platform()))
    c = compile_bytes(raw)
    if not c.ok:
        print("NOT-ACCEPTED %s" % c.error.code)
        return
    if mode == "compile":
        print("ACCEPTED law-sha256 %s law-bytes %d" % (hashlib.sha256(c.law).hexdigest(), len(c.law)))
        return
    it = interp.Interp(c.prog, c.an, c.law_seal, c.text_seal, trace=True, budget=None if budget < 0 else budget)
    try:
        it.run()
    except interp.HostStop as e:
        print("STOPPED ops %d" % e.ops)
        return
    lines = it.receipt("reference").decode("ascii").split("\n")
    status = [ln for ln in lines if ln.startswith("status ")][0][len("status "):].split(" ")[0]
    ops = int([ln for ln in lines if ln.startswith("ops ")][0][len("ops "):])
    print("%s ops %d output-sha256 %s" % (status, ops, hashlib.sha256(bytes(it.out)).hexdigest()))


def fresh(raw, mode, budget=-1):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    try:
        p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--one", mode, str(budget)], input=raw,
                           capture_output=True, cwd=ROOT, env=env, timeout=LIMIT_S)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    out = p.stdout.decode("ascii", "replace").replace("\r\n", "\n").rstrip("\n").split("\n")
    env_line = out[0] if out and out[0].startswith("ENV ") else None
    if p.returncode != 0:
        err = p.stderr.decode("ascii", "replace").replace("\r\n", "\n").rstrip("\n").split("\n")
        return env_line, "CRASH exit %d %s" % (p.returncode, err[-1].split(":")[0] if err and err[-1] else "none")
    return env_line, out[-1]


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def make(path):
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("GEN-STRESS: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("GEN-STRESS: src/, tests/ or vectors/ differ from the starting commit")
    rows, envs = [], set()
    for name, pred, text, expect in texts():
        raw = text.encode("utf-8")
        env_line, got = fresh(raw, "compile")
        envs.add(env_line)
        if not got.startswith("ACCEPTED "):
            sys.exit("GEN-STRESS: the front end does not accept %s: %s" % (name, got))
        checks = []
        if name in ("s1-perform-300", "s1-rule-300"):
            checks = [(-1, expect)]
        elif pred == "do-nothing":
            checks = [(0, "STOPPED ops 1"), (1, "COMPLETED ops 1 output-sha256 %s" % ONE)]
        for budget, want in checks:
            env_line, ran = fresh(raw, "run", budget)
            envs.add(env_line)
            if ran != want:
                sys.exit("GEN-STRESS: %s under budget %s gives %s, not %s" % (name, budget, ran, want))
        rows.append("%s %s text-sha256 %s text-bytes %d %s expect %s%s" % (
            name, pred, sha(raw), len(raw), got[len("ACCEPTED "):], expect,
            "; held to the reference here" if checks else ""))
    head = [
        "# S1's and S2's texts and the do-nothing fixtures: SHEET.md Amendment 3, fixed before any experiment (the "
        "owner's ruling E2, and J15, 2026-10-30)",
        "# generator research/rust-core/gen_stress_texts.py sha256 %s; each text is made by it from its name alone" % (
            sha(open(os.path.abspath(__file__), "rb").read())),
        "# front end and reference at %s: src/orlog/sema.py sha256 %s, src/orlog/interp.py sha256 %s; each in a fresh "
        "`python -B` process, PYTHONHASHSEED=0, the default recursion limit, never importing format_check, a %d s "
        "limit" % (BASE[:7], sha(open(os.path.join(ROOT, "src", "orlog", "sema.py"), "rb").read()),
                   sha(open(os.path.join(ROOT, "src", "orlog", "interp.py"), "rb").read()), LIMIT_S),
        "# environment, as each process reported it: %s" % " | ".join(sorted(e for e in envs if e)),
        "# a row: name, prediction, the text's sha256 and length, the law bytes' sha256 and length (the front end's), "
        "and what is expected: S1's by construction, S2's from the reference at experiment time, the fixtures' as the "
        "reference gave here",
    ]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(path, "wb") as f:
        f.write(data)
    print("GEN-STRESS: %d texts; environments %d; sha256 %s" % (len(rows), len([e for e in envs if e]), sha(data)))


def write(manifest, folder):
    want = {}
    with open(manifest, "rb") as f:
        for line in f.read().decode("ascii").split("\n"):
            if line and not line.startswith("#"):
                w = line.split(" ")
                want[w[0]] = (w[w.index("text-sha256") + 1], w[w.index("law-sha256") + 1])
    os.makedirs(folder, exist_ok=True)
    if os.listdir(folder):
        sys.exit("GEN-STRESS: %s is not empty" % folder)
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from orlog.front import compile_bytes
    for name, pred, text, expect in texts():
        raw = text.encode("utf-8")
        law = compile_bytes(raw).law
        if (sha(raw), sha(law)) != want.get(name):
            sys.exit("GEN-STRESS: %s does not match the manifest" % name)
        for ext, data in ((".orl", raw), (".law", law)):
            with open(os.path.join(folder, name + ext), "wb") as f:
                f.write(data)
    print("GEN-STRESS: %d texts and their law bytes written, each equal to the manifest" % len(want))


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "--one":
        child(a[1], int(a[2]))
    elif len(a) == 2 and a[0] == "--out":
        make(a[1])
    elif len(a) == 4 and a[0] == "--write" and a[2] == "--manifest":
        write(a[3], a[1])
    else:
        sys.exit("usage: gen_stress_texts.py --out PATH | --write DIR --manifest PATH")

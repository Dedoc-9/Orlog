"""RUST-CORE-0: every way the reference runner ends, through classify (SHEET.md Amendments 5 to 7, 12 and 13; REREAD-5's
L3 and L5, REREAD-6's M7, REREAD-7's X3, X4, X13 and Y14, REREAD-8's ZB3, REREAD-9's NB5 to NB7, and the owner's D5 and
his rulings on ASK 9-4 and 9-6).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/ref_run_paths.py

Each case runs research/rust-core/ref_run.py twice, each a fresh `python -B` process whose working directory is a fresh
empty folder, its input in another. The two raw runs go to `ref_run.classify`, and the class it gives, or what it
raises instead (a runner fault, an anomaly, an interruption), must be the one stated here; so must each run's exit
status, stderr's last line, and, where this check computes it itself, stdout's last line.

- **The outcome lines** of a completed text, a completed law, a law stopped by its budget and a law decoder1 refuses
  are computed here, in this process, by the interpreter and decoder1 themselves, and the runner's must equal them
  (REREAD-7's X3: a runner that ignored the budget in law mode, took the law seal from other bytes, dropped decoder1's
  message or miscounted a stop passed the earlier check).
- **The paths the real modules never take** (an exit, an interrupt or a plant inside decode; a failing platform query;
  an `orlog` or decoder1 import that raises something other than `ImportError`) are reached through a stand-in put in
  place before the runner starts, so the real modules are not changed. A wrong pin and a `__pycache__` folder are
  reached through copies of the runner made here; so is a `__pycache__` in each of the three folders the runner's
  docstring names, `src/orlog`, `research/rust-core` and `research/law-sufficiency`, one copy for each, whose root is
  a folder made here holding the three with the cache in that one, and whose fault must name it (REREAD-8's ZB3).
- **The run conditions** (REREAD-6's M7, REREAD-7's X3 and X13, REREAD-8's ZB3): every run that reaches the reference
  prints the ENV line first, and it must equal the line this check makes itself: the implementation, version and
  platform a fresh interpreter reports in the runner's conditions, that interpreter's default recursion limit,
  `format_check not-imported`, and exactly the `orlog` modules a fresh import of the runner's setup loads (the text
  mode's, the law mode's, or, under a stand-in decoder1, those `orlog`'s own import loads), each by the sha256 of its
  file as it stands, none missing and none more. Before its outcome, the after-run line must equal its own, with the
  same modules.
- **Exactly those lines** (REREAD-9's NB5, his ruling on ASK 9-4): a run's stdout is the ENV line and, for a result,
  the after-run line and the outcome, and nothing else; a run that ends before the ENV line prints nothing.
- **The recorded baseline** (his ruling on ASK 9-6, question 4): every law run's ENV line equals the line
  `r6-reference-5.txt` records for every run, and a text run's agrees with it before the module list and on each
  module it names. So the check holds only in the environment that record was made in.
- **The conditions observed inside the run** (NB5, NB7): a stand-in records, as the reference begins, the recursion
  limit, the `orlog` modules loaded, whether any module from a file `format_check.py` is loaded, `sys.pycache_prefix`
  and `sys.flags`; loads `orlog.lower` during the run, as a reference that loads a module late would; and records the
  modules again after it. The ENV line must report what it saw as the reference began, and the after-run line what it
  saw after; no `format_check`; no pycache prefix; and the flags of a fresh `python -B` whose environment holds no
  PYTHON variable but PYTHONHASHSEED=0 and PYTHONUTF8=1.
- **Paths no earlier case reached** (NB6): law mode with `--files` and a TEXTSEAL other than zeros, the files and the
  receipt held to the interpreter's own; a text stopped by its budget, its outcome computed; a crash beside a timeout;
  a BUDGET with a trailing LF.
- **Some cases of classify** are checked on runs made up here: timeouts, crash types, two different results and two
  different refusals (REREAD-7's X3), an exit 3 without its line (an anomaly), an exit status the runner never gives
  with and without `KeyboardInterrupt` (his D5).
- **The runner's source** is read by its syntax tree (REREAD-7's X3): no name or attribute `environ`, `getenv`,
  `putenv` or `setrecursionlimit`, imported or not; no `getattr` on `os` or `sys`; no import of `format_check`. Since
  REREAD-9 (NB5): no constant string, docstrings aside, holding `environ`, `getenv`, `putenv` or `setrecursion`; every
  `getattr` names its attribute by a constant string, none of those; no import of `importlib`, `runpy`, `time`,
  `datetime` or `timeit`, no name `__import__`, `exec`, `eval` or `compile`, and no attribute that imports a module or
  reads a clock.

It writes nothing in the repository, and prints nothing that varies from run to run. It is evidence that the runner
ends as its docstring says, not that the reference is right, and it is outside the core author's reading set (D1). What
it holds is measured on these cases in this environment; it is no certificate of behaviour outside them."""
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RUNNER = os.path.join(HERE, "ref_run.py")
sys.path.insert(0, HERE)
import ref_run                  # noqa: E402

S = "§"
H = b"orlog-law 0\n(decimals fixed)\n"
STAND_IN = '''import importlib.abc, platform, runpy, sys, types
mode = sys.argv[1]
if mode == "envinterrupt":
    def boom(*a, **k):
        raise KeyboardInterrupt
    platform.platform = boom
elif mode == "envoserror":
    def boom(*a, **k):
        raise OSError("a platform query that fails")
    platform.platform = boom
elif mode == "orlogvalue":
    class Broken(types.ModuleType):
        def __getattr__(self, name):
            raise ValueError("an orlog that fails as it is read")
    sys.modules["orlog"] = Broken("orlog")
elif mode == "decoderraise":
    class Finder(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path=None, target=None):
            if name == "decoder1":
                raise ValueError("a decoder1 that fails as it is found")
            return None
    sys.meta_path.insert(0, Finder())
elif mode.startswith("observe|"):          # REREAD-9's NB5 and NB7: the conditions, seen from inside the run
    import json, os
    _, out, src = mode.split("|")
    sys.path.insert(0, src)
    from orlog import interp
    def orlog_now():
        return sorted(n for n, v in list(sys.modules.items())
                      if (n == "orlog" or n.startswith("orlog.")) and getattr(v, "__file__", None))
    def fc_now():
        return any(os.path.basename(str(getattr(v, "__file__", "") or "")) == "format_check.py"
                   for v in list(sys.modules.values()))
    seen = {}
    def dump():
        with open(out, "w", encoding="utf-8") as f:
            json.dump(seen, f, sort_keys=True)
    real_run = interp.Interp.run
    def observed_run(self, *a, **k):
        seen["begin"] = {"recursion_limit": sys.getrecursionlimit(), "orlog": orlog_now(), "format_check": fc_now(),
                         "pycache_prefix": sys.pycache_prefix, "flags": list(sys.flags)}
        dump()
        try:
            return real_run(self, *a, **k)
        finally:
            import orlog.lower             # a module the reference loads late, which the after-run line must list
            seen["after"] = {"recursion_limit": sys.getrecursionlimit(), "orlog": orlog_now(), "format_check": fc_now()}
            dump()
    interp.Interp.run = observed_run
else:
    m = types.ModuleType("decoder1")
    class DecodeError(Exception):
        pass
    m.DecodeError = DecodeError
    m.PLANT = "a plant" if mode == "plant" else None
    def decode(raw):
        if mode == "exit":
            raise SystemExit(0)
        if mode == "interrupt":
            raise KeyboardInterrupt
        if mode == "refuse":
            raise DecodeError("a refusal")
        if mode == "keyerror":
            raise KeyError("a crash that is not a refusal")
        raise ValueError("a stand-in that decodes nothing")
    m.decode = decode
    sys.modules["decoder1"] = None if mode == "noimport" else m
sys.argv = [sys.argv[2]] + sys.argv[3:]
runpy.run_path(sys.argv[0], run_name="__main__")
'''
# REREAD-8's ZB3: the three folders the runner's docstring names for its bytecode check, as this check states them
BYTECODE_NAMES = ("src/orlog", "research/rust-core", "research/law-sufficiency")
# the stand-in modes that put a decoder1 of their own in place of the real one
DECODER_STAND_INS = ("exit", "keyerror", "interrupt", "plant", "refuse", "noimport")
LISTED = 'import sys; print(" ".join(sorted(n for n in sys.modules if n == "orlog" or n.startswith("orlog."))))'
# his ruling on ASK 9-6, question 4: the ENV line every run of r6-reference-5 reported, its record's fifth line
RECORDED_AT = "# environment, as every run reported it: "
# REREAD-9's NB5: what the runner's source may not hold
FORBIDDEN_TEXT = ("environ", "getenv", "putenv", "setrecursion")
FORBIDDEN_MODULES = {"importlib", "runpy", "time", "datetime", "timeit"}
DYNAMIC_NAMES = {"__import__", "exec", "eval", "compile"}
DYNAMIC_OR_CLOCK_ATTRS = {"import_module", "spec_from_file_location", "exec_module", "run_path", "run_module",
                          "perf_counter", "perf_counter_ns", "monotonic", "monotonic_ns", "process_time",
                          "process_time_ns", "thread_time", "thread_time_ns", "time_ns", "times", "clock_gettime"}


def run(args, work, stand_in=None, files=False, runner=RUNNER, contents=None):
    """One fresh run: (exit status, stdout bytes, stderr bytes), and the names it left in its folder; given a dict
    CONTENTS, each file it left, by name, its bytes."""
    folder = tempfile.mkdtemp(dir=work)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    head = [sys.executable, "-B"] + ([stand_in[0], stand_in[1], runner] if stand_in else [runner])
    p = subprocess.run(head + args + (["--files"] if files else []), capture_output=True, cwd=folder, env=env)
    left = sorted(os.listdir(folder))
    if contents is not None:
        for name in left:
            with open(os.path.join(folder, name), "rb") as f:
                contents[name] = f.read()
    shutil.rmtree(folder)
    return (p.returncode, p.stdout, p.stderr), left


def verdict(r1, r2):
    try:
        return ref_run.classify(r1, r2)
    except ref_run.RunnerFault:
        return "RUNNER-FAULT"
    except ref_run.Anomaly:
        return "ANOMALY"
    except ref_run.Interrupted:
        return "INTERRUPTED"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def outcome(interp, prog, an, law_seal, text_seal, budget):
    """The outcome line, computed here by the interpreter itself, as the runner's docstring states it."""
    it = interp.Interp(prog, an, law_seal, text_seal, trace=True, budget=budget)
    try:
        it.run()
    except interp.HostStop as e:
        return "RUN STOPPED ops %d trace %s" % (e.ops, sha("\n".join(it.trace).encode("ascii")))
    rl = it.receipt("reference").decode("ascii").split("\n")
    pr = "\n".join(ln for ln in rl if not ln.startswith(("backend ", "text-seal ")))
    st = [ln for ln in rl if ln.startswith("status ")][0][len("status "):].split(" ")[0]
    ops = int([ln for ln in rl if ln.startswith("ops ")][0][len("ops "):])
    return "RUN %s ops %d p %s trace %s" % (st, ops, sha(pr.encode("ascii")), sha("\n".join(it.trace).encode("ascii")))


def lines_of(data):
    return [ln for ln in data.decode("ascii", "replace").replace("\r\n", "\n").split("\n") if ln]


def fresh(code, work):
    """What a fresh interpreter prints for CODE, in the runner's conditions: `python -B`, the same environment, a fresh
    empty folder (REREAD-8's ZB3)."""
    folder = tempfile.mkdtemp(dir=work)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    p = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, cwd=folder, env=env)
    shutil.rmtree(folder)
    return p.stdout.decode("utf-8").replace("\r\n", "\n").rstrip("\n").split("\n")


def orlog_part(names):
    """The modules by name, each with the sha256 of its file as it stands, found from its name here."""
    out = []
    for name in names:
        parts = name.split(".")
        path = os.path.join(ROOT, "src", *parts) + ".py"
        if not os.path.isfile(path):
            path = os.path.join(ROOT, "src", *parts, "__init__.py")
        with open(path, "rb") as f:
            out.append("%s=%s" % (name, sha(f.read())))
    return " ".join(out)


def conditions_lines(default, work):
    """REREAD-8's ZB3: the ENV and after-run lines each kind of run must print, made here, whole: {kind: (ENV line,
    after-run line)}. The kinds: a text, a law, and a law under a stand-in decoder1."""
    impl, version, plat = fresh("import platform; print(platform.python_implementation()); "
                                "print(platform.python_version()); print(platform.platform())", work)
    src, ls = os.path.join(ROOT, "src"), os.path.join(ROOT, "research", "law-sufficiency")
    base = "import sys; sys.path.insert(0, %r); from orlog import interp; " % src
    mods = {"text": fresh(base + "from orlog.front import compile_bytes; " + LISTED, work)[0].split(" "),
            "law": fresh(base + "sys.path.insert(0, %r); import decoder1; " % ls + LISTED, work)[0].split(" "),
            "stand-in": fresh(base + LISTED, work)[0].split(" ")}
    lines = {}
    for kind, names in mods.items():
        part = orlog_part(names)
        lines[kind] = ("ENV python %s %s recursion-limit %d format_check not-imported; %s; orlog %s" % (
            impl, version, default, plat, part),
            "CONDITIONS after-run recursion-limit %d format_check not-imported; orlog %s" % (default, part))
    return lines, mods


def source_rows(src):
    """REREAD-7's X3: the runner's source by its syntax tree, not by substrings."""
    tree = ast.parse(src)
    banned = {"environ", "getenv", "putenv", "setrecursionlimit"}
    names, getattrs, fc = set(), False, False
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.ImportFrom):
            names.update(a.name for a in node.names)
            fc = fc or (node.module or "").split(".")[0] == "format_check"
        elif isinstance(node, ast.Import):
            fc = fc or any(a.name.split(".")[0] == "format_check" for a in node.names)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr" and node.args
                and isinstance(node.args[0], ast.Name) and node.args[0].id in ("os", "sys")):
            getattrs = True
    # REREAD-9's NB5: forbidden text in constants (docstrings aside), getattr by a computed name, dynamic imports, clocks
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docs.add(id(first.value))
    texts = getattr_named = dynamic = clock = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
            texts = texts or any(t in node.value for t in FORBIDDEN_TEXT)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr":
            attr = node.args[1] if len(node.args) > 1 else None
            if not (isinstance(attr, ast.Constant) and isinstance(attr.value, str)) or any(
                    t in attr.value for t in FORBIDDEN_TEXT):
                getattr_named = True
        elif isinstance(node, ast.Import):
            dynamic = dynamic or any(a.name.split(".")[0] in FORBIDDEN_MODULES for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            dynamic = dynamic or (node.module or "").split(".")[0] in FORBIDDEN_MODULES
        elif isinstance(node, ast.Name) and node.id in DYNAMIC_NAMES:
            dynamic = True
        elif isinstance(node, ast.Attribute) and node.attr in DYNAMIC_OR_CLOCK_ATTRS:
            clock = True
    return [("no name environ, getenv, putenv or setrecursionlimit", not names & banned),
            ("no getattr on os or sys", not getattrs),
            ("no import of format_check", not fc),
            ("no constant holding a forbidden name (NB5)", not texts),
            ("every getattr names its attribute by a constant (NB5)", not getattr_named),
            ("no dynamic import, exec or eval, no clock module (NB5)", not dynamic),
            ("no attribute that imports or reads a clock (NB5)", not clock)]


def recorded_env():
    """The ENV line r6-reference-5.txt records for every run (his ruling on ASK 9-6, question 4)."""
    with open(os.path.join(ROOT, "research", "rust-core", "r6-reference-5.txt"), encoding="utf-8") as f:
        for ln in f:
            if ln.startswith(RECORDED_AT):
                return ln[len(RECORDED_AT):].rstrip("\n")
    return None


def baseline_ok(line, kind, recorded):
    """A law run's ENV line equals the recorded one; a text run's agrees with it before the module list, and on each
    module the recorded line names."""
    if recorded is None:
        return False
    if kind != "text":
        return line == recorded
    head, _, mods = line.partition("; orlog ")
    rhead, _, rmods = recorded.partition("; orlog ")
    return head == rhead and set(rmods.split(" ")) <= set(mods.split(" "))


def clean_flags(work):
    """sys.flags of a fresh `python -B` whose environment holds no PYTHON variable but PYTHONHASHSEED and PYTHONUTF8."""
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON")}
    env.update(PYTHONHASHSEED="0", PYTHONUTF8="1")
    folder = tempfile.mkdtemp(dir=work)
    p = subprocess.run([sys.executable, "-B", "-c", "import json, sys; print(json.dumps(list(sys.flags)))"],
                       capture_output=True, cwd=folder, env=env)
    shutil.rmtree(folder)
    return p.stdout.decode("ascii").strip()


def mods_of(line):
    """The module names a conditions line lists, in its order."""
    return [x.split("=", 1)[0] for x in line.partition("; orlog ")[2].split(" ") if x]


def recursion_of(line):
    m = re.search(r"recursion-limit (\d+) ", line)
    return int(m.group(1)) if m else None


def main():
    work = tempfile.mkdtemp(prefix="refrunpaths-")
    try:
        inputs = os.path.join(work, "inputs")
        os.mkdir(inputs)

        def put(name, data):
            path = os.path.join(inputs, name)
            with open(path, "wb") as f:
                f.write(data)
            return path

        sys.path.insert(0, os.path.join(ROOT, "src"))
        from orlog import interp
        from orlog.front import compile_bytes
        sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
        import decoder1
        say_text = ("%s1 Say 1.\n%s2 Say 2.\n" % (S, S)).encode("utf-8")
        c = compile_bytes(say_text)
        say = put("say.orl", say_text)
        say_law = put("say.law", c.law)
        bad = put("bad.orl", ("%s1 Say.\n" % S).encode("utf-8"))
        empty = put("empty.law", H)
        v1_bytes = b"orlog-law 1\n(decimals fixed)\n"
        v1 = put("v1.law", v1_bytes)
        high = put("high.law", b"orlog-law 0\n(decimals fixed)\n\xff\n")
        stand = put("stand_in.py", STAND_IN.encode("ascii"))
        missing = os.path.join(inputs, "missing.law")
        z = "0" * 64
        # the outcome lines, computed here (REREAD-7's X3)
        want_text = outcome(interp, c.prog, c.an, c.law_seal, c.text_seal, None)
        want_text_stop = outcome(interp, c.prog, c.an, c.law_seal, c.text_seal, 0)     # REREAD-9's NB6 (K9)
        lp, la = decoder1.decode(c.law)
        want_law = outcome(interp, lp, la, sha(c.law), z, None)
        lp, la = decoder1.decode(c.law)
        want_stop = outcome(interp, lp, la, sha(c.law), z, 0)
        ep, ea = decoder1.decode(H)
        want_empty = outcome(interp, ep, ea, sha(H), z, None)
        try:
            decoder1.decode(v1_bytes)
            want_refused = "decoder1 accepted version 1"
        except decoder1.DecodeError as e:
            want_refused = "DECODER-REFUSED %s" % ascii(str(e))
        U = "REFERENCE-EXCEPTION builtins.UnicodeDecodeError"
        X = "REFERENCE-EXCEPTION builtins.SystemExit"
        F = "RUNNER-FAULT "
        cases = [   # (what, args, stand-in or copy, the class stated, exit status, stderr's last line, stdout's last)
            ("text: a text the front end accepts", ["text", "none", say], None, "RESULT", 0, "", want_text),
            ("text: the same under budget 0", ["text", "0", say], None, "RESULT", 0, "", want_text_stop),
            ("text: a text the front end refuses", ["text", "none", bad], None, "RUNNER-FAULT", 3, F, None),
            ("law: the empty law", ["law", "none", z, empty], None, "RESULT", 0, "", want_empty),
            ("law: a law that completes", ["law", "none", z, say_law], None, "RESULT", 0, "", want_law),
            ("law: the same law stopped by budget 0", ["law", "0", z, say_law], None, "RESULT", 0, "", want_stop),
            ("law: decoder1 refuses (version 1)", ["law", "none", z, v1], None, "REFERENCE-REFUSED", 0, "",
             want_refused),
            ("law: decoder1 crashes (a byte above 0x7E)", ["law", "none", z, high], None, "NO-REFERENCE-RESULT", 1, U,
             None),
            ("usage: no arguments", [], None, "RUNNER-FAULT", 3, F, None),
            ("usage: budget 1e6", ["law", "1e6", z, empty], None, "RUNNER-FAULT", 3, F, None),
            ("usage: budget -1", ["law", "-1", z, empty], None, "RUNNER-FAULT", 3, F, None),
            ("usage: budget 05", ["law", "05", z, empty], None, "RUNNER-FAULT", 3, F, None),
            ("usage: budget +5", ["law", "+5", z, empty], None, "RUNNER-FAULT", 3, F, None),
            ("usage: budget 5 and a line feed (NB6)", ["law", "5\n", z, empty], None, "RUNNER-FAULT", 3, F, None),
            ("usage: a text seal in capitals", ["law", "none", "A" * 64, empty], None, "RUNNER-FAULT", 3, F, None),
            ("usage: an input that does not exist", ["law", "none", z, missing], None, "RUNNER-FAULT", 3, F, None),
            ("stand-in: decode calls sys.exit(0)", ["law", "none", z, empty], "exit", "NO-REFERENCE-RESULT", 1, X, None),
            ("stand-in: decode raises KeyError", ["law", "none", z, empty], "keyerror", "NO-REFERENCE-RESULT", 1,
             "REFERENCE-EXCEPTION builtins.KeyError", None),
            ("stand-in: decode is interrupted", ["law", "none", z, empty], "interrupt", "RUNNER-FAULT", 3, F, None),
            ("stand-in: decoder1 holds a plant", ["law", "none", z, empty], "plant", "RUNNER-FAULT", 3, F, None),
            ("stand-in: decode refuses", ["law", "none", z, empty], "refuse", "REFERENCE-REFUSED", 0, "",
             "DECODER-REFUSED 'a refusal'"),
            ("stand-in: decoder1 cannot be imported", ["law", "none", z, empty], "noimport", "RUNNER-FAULT", 3,
             F + "decoder1 cannot be imported", None),
            ("stand-in: decoder1's import raises ValueError", ["law", "none", z, empty], "decoderraise",
             "RUNNER-FAULT", 3, F + "decoder1 cannot be imported: ValueError", None),
            ("stand-in: orlog's import raises ValueError", ["law", "none", z, empty], "orlogvalue", "RUNNER-FAULT", 3,
             F + "the reference's modules cannot be imported: ValueError", None),
            ("stand-in: the ENV line's platform query fails", ["law", "none", z, empty], "envoserror", "RUNNER-FAULT",
             3, F + "before the reference began: OSError", None),
            ("stand-in: the ENV line is interrupted", ["law", "none", z, empty], "envinterrupt", "RUNNER-FAULT", 3,
             F + "interrupted", None),
            ("a runner whose decoder1 pin is wrong", ["law", "none", z, empty], "wrongpin", "RUNNER-FAULT", 3,
             F + "decoder1.py is not the file", None),
            ("a runner beside a __pycache__ folder", ["law", "none", z, empty], "pycache", "RUNNER-FAULT", 3,
             F + "a __pycache__ folder stands in", None),
        ] + [   # REREAD-8's ZB3: a __pycache__ in each folder the runner checks, by name
            ("a __pycache__ in %s" % rel, ["law", "none", z, empty], "pycache:" + rel, "RUNNER-FAULT", 3,
             F + "a __pycache__ folder stands in %s" % rel, None) for rel in BYTECODE_NAMES]
        print("THE REFERENCE RUNNER'S WAYS OF ENDING, THROUGH classify (research/rust-core/ref_run_paths.py)")
        rows = []
        default = int(subprocess.run([sys.executable, "-B", "-c", "import sys; print(sys.getrecursionlimit())"],
                                     capture_output=True).stdout.decode().strip())
        want_lines, mods = conditions_lines(default, work)
        print("   the orlog modules a fresh import loads: a text %d, a law %d, under a stand-in decoder1 %d (ZB3)" % (
            len(mods["text"]), len(mods["law"]), len(mods["stand-in"])))
        recorded = recorded_env()
        print("   the recorded baseline, r6-reference-5.txt's ENV line: %s" % ("found" if recorded else "NOT FOUND"))
        flags_want = clean_flags(work)
        print("   a fresh interpreter's sys.flags, no PYTHON variable but PYTHONHASHSEED and PYTHONUTF8: %s" % flags_want)
        with open(RUNNER, encoding="utf-8") as f:
            runner_src = f.read()
        fixed_root = "ROOT = %r" % ROOT
        copies = {}
        wrong = os.path.join(work, "wrongpin_ref_run.py")
        with open(wrong, "w", encoding="utf-8", newline="\n") as f:
            f.write(runner_src.replace('DECODER1_SHA256 = "', 'DECODER1_SHA256 = "0' + "0" * 63 + '"  # was "', 1)
                    .replace("ROOT = os.path.dirname(os.path.dirname(HERE))", fixed_root))
        copies["wrongpin"] = wrong
        cache_home = os.path.join(work, "cache_home")
        os.makedirs(os.path.join(cache_home, "__pycache__"))
        cached = os.path.join(work, "pycache_ref_run.py")
        with open(cached, "w", encoding="utf-8", newline="\n") as f:
            f.write(runner_src.replace("ROOT = os.path.dirname(os.path.dirname(HERE))", fixed_root)
                    .replace("BYTECODE = [", "BYTECODE = [%r] + [" % cache_home, 1))
        copies["pycache"] = cached
        for rel in BYTECODE_NAMES:      # REREAD-8's ZB3: a root made here, the three folders in it, the cache in one
            fake = os.path.join(work, "root_" + rel.replace("/", "_"))
            for r in BYTECODE_NAMES:
                os.makedirs(os.path.join(fake, *r.split("/")))
            os.mkdir(os.path.join(fake, *rel.split("/"), "__pycache__"))
            path = os.path.join(work, "pycache_%s_ref_run.py" % rel.replace("/", "_"))
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(re.sub(r"(?m)^ROOT = .*$", lambda m: "ROOT = %r" % fake, runner_src, count=1))
            copies["pycache:" + rel] = path
        for what, args, mode, want, want_exit, want_err, want_out in cases:
            if mode in copies:
                (r1, l1), (r2, l2) = run(args, work, runner=copies[mode]), run(args, work, runner=copies[mode])
            else:
                si = (stand, mode) if mode else None
                (r1, l1), (r2, l2) = run(args, work, si), run(args, work, si)
            got = verdict(r1, r2)
            ends = all(r[0] == want_exit and (ref_run.last_line(r[2]).startswith(want_err) if want_err else
                                              ref_run.last_line(r[2]) == "") for r in (r1, r2))
            out_ok = want_out is None or all(ref_run.last_line(r[1]) == want_out for r in (r1, r2))
            kind = "text" if args[:1] == ["text"] else "stand-in" if mode in DECODER_STAND_INS else "law"
            env_line, after_line = want_lines[kind]
            cond_ok = base_ok = True
            for r in (r1, r2):
                ls = lines_of(r[1])
                if ls[:1] and ls[0].startswith("ENV "):     # ZB3: the whole lines, made here; NB5: those lines alone
                    exact = [env_line] + ([after_line] if r[0] == 0 else [])
                    cond_ok = cond_ok and ls[:len(exact)] == exact and len(ls) == len(exact) + (r[0] == 0)
                    base_ok = base_ok and baseline_ok(ls[0], kind, recorded)
                else:                                       # NB5: a run that ends before the ENV line prints nothing
                    cond_ok = cond_ok and not ls and r[0] == 3
            ok = got == want and ends and out_ok and cond_ok and base_ok and not l1 and not l2
            rows.append(ok)
            print("   %-48s exit %d | out %-26s | err %-44s | %-19s %s" % (
                what, r1[0], ref_run.last_line(r1[1])[:26], ref_run.last_line(r2[2])[:44], got,
                "as stated" if ok else "NOT AS STATED (stated %s; out %s, conditions %s, baseline %s; left %s %s)"
                % (want, out_ok, cond_ok, base_ok, l1, l2)))
        # REREAD-9's NB5 and NB7: the conditions seen from inside the run, by the observing stand-in, twice each
        for what, args, kind, want_out in [
                ("observed: a law that completes", ["law", "none", z, say_law], "law", want_law),
                ("observed: the same law stopped by budget 0", ["law", "0", z, say_law], "law", want_stop),
                ("observed: a text the front end accepts", ["text", "none", say], "text", want_text)]:
            oks = []
            for k in (1, 2):
                obs = os.path.join(work, "observed-%d.json" % k)
                r, left = run(args, work, (stand, "observe|%s|%s" % (obs, os.path.join(ROOT, "src"))))
                try:
                    with open(obs, encoding="utf-8") as f:
                        seen = json.load(f)
                except (OSError, ValueError):
                    seen = {}
                ls, b, a = lines_of(r[1]), seen.get("begin", {}), seen.get("after", {})
                oks.append(r[0] == 0 and len(ls) == 3 and ls[0] == want_lines[kind][0] and ls[2] == want_out
                           and baseline_ok(ls[0], kind, recorded) and not left
                           and b.get("recursion_limit") == recursion_of(ls[0]) and b.get("orlog") == mods_of(ls[0])
                           and b.get("format_check") is False and b.get("pycache_prefix") is None
                           and json.dumps(b.get("flags")) == flags_want and a.get("format_check") is False
                           and "orlog.lower" in a.get("orlog", [])
                           and ls[1] == "CONDITIONS after-run recursion-limit %d format_check not-imported; orlog %s" % (
                               a.get("recursion_limit", -1), orlog_part(a.get("orlog", []))))
            ok = all(oks)
            rows.append(ok)
            print("   %-48s %s" % (what, "as stated" if ok else "NOT AS STATED"))
        # --files: what a completed and a stopped run leave in their folders; NB6: a law with a TEXTSEAL not zeros, its
        # files and its receipt held to the interpreter's own
        seal = "ab" * 32
        lp, la = decoder1.decode(c.law)
        it = interp.Interp(lp, la, sha(c.law), seal, trace=True, budget=None)
        it.run()
        law_files = {"reference.out": bytes(it.out), "reference.receipt": it.receipt("reference"),
                     "reference.trace": "\n".join(it.trace).encode("ascii")}
        for what, args, want, kind, want_bytes in [
                ("--files: a completed run", ["text", "none", say],
                 ["reference.out", "reference.receipt", "reference.trace"], "text", None),
                ("--files: a stopped run", ["text", "0", say], ["reference.out", "reference.trace"], "text", None),
                ("--files: a completed law, TEXTSEAL not zeros (NB6)", ["law", "none", seal, say_law],
                 sorted(law_files), "law", law_files)]:
            contents = {}
            r, left = run(args, work, files=True, contents=contents)
            ls = lines_of(r[1])
            ok = (left == want and r[0] == 0 and len(ls) == 3 and ls[:2] == list(want_lines[kind])
                  and baseline_ok(ls[0], kind, recorded) and (want_bytes is None or contents == want_bytes))
            rows.append(ok)
            print("   %-48s leaves %-52s %s" % (what, " ".join(left), "as stated" if ok else "NOT AS STATED"))
        # classify on runs made up here
        res = (0, b"ENV x\r\nRUN COMPLETED ops 1 p a trace b\r\n", b"")
        res2 = (0, b"ENV x\nRUN COMPLETED ops 2 p c trace d\n", b"")
        ref1 = (0, b"ENV x\nDECODER-REFUSED 'one'\n", b"")
        ref2 = (0, b"ENV x\nDECODER-REFUSED 'two'\n", b"")
        ki = (3221225786, b"ENV x\n", b"Traceback (most recent call last):\nKeyboardInterrupt\n")
        made = [("two timeouts", "TIMEOUT", "TIMEOUT", "NO-REFERENCE-RESULT"),
                ("a timeout and a result", "TIMEOUT", res, "UNSTABLE"),
                ("a crash and a timeout (NB6)", (1, b"", b"REFERENCE-EXCEPTION builtins.KeyError\n"), "TIMEOUT",
                 "UNSTABLE"),
                ("a result, CR LF and LF", res, (0, b"ENV x\nRUN COMPLETED ops 1 p a trace b\n", b""), "RESULT"),
                ("two different results", res, res2, "UNSTABLE"),
                ("two different refusals", ref1, ref2, "UNSTABLE"),
                ("two crashes of different types", (1, b"", b"REFERENCE-EXCEPTION builtins.KeyError\n"),
                 (1, b"", b"REFERENCE-EXCEPTION builtins.ValueError\n"), "UNSTABLE"),
                ("two crashes, one exit status each", (1, b"", b"REFERENCE-EXCEPTION builtins.KeyError\n"),
                 (2, b"", b"REFERENCE-EXCEPTION builtins.KeyError\n"), "UNSTABLE"),
                ("a runner fault's line", (3, b"", b"RUNNER-FAULT a reason\n"), res, "RUNNER-FAULT"),
                ("an exit 3 without its line", (3, b"", b""), res, "ANOMALY"),
                ("an unknown status with KeyboardInterrupt", ki, res, "INTERRUPTED"),
                ("an unknown status without it, twice", (3221226505, b"", b""), (3221226505, b"", b""),
                 "NO-REFERENCE-RESULT")]
        for what, a, b, want in made:
            got = verdict(a, b)
            rows.append(got == want)
            print("   %-48s %-19s %s" % ("made up: " + what, got, "as stated" if got == want else "NOT AS STATED"))
        for what, ok in source_rows(runner_src):
            rows.append(ok)
            print("   %-48s %s" % ("source: " + what, "as stated" if ok else "NOT AS STATED"))
        bad_count = rows.count(False)
        print("REF-RUN PATHS %s: %d of %d as stated" % ("HELD" if bad_count == 0 else "FAILED", len(rows) - bad_count,
                                                        len(rows)))
        sys.exit(0 if bad_count == 0 else 1)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()

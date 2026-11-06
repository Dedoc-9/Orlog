"""RUST-CORE-0: does ref_run_paths.py catch the runner changes the re-reads showed passing it? (REREAD-6's M7,
REREAD-7's X3, REREAD-8's ZB3 and ZB5, REREAD-9's NB5 to NB7; SHEET.md Amendments 7, 12 and 13.)

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/ref_run_variants.py

Each variant is a copy of research/rust-core/ref_run.py with one change, made in a temporary folder, never in the
repository. A copy of ref_run_paths.py is pointed at it and run; the variant is caught when that check fails (exit 1,
"FAILED"). The control, the runner unchanged, must pass. The variants are REREAD-6's five and REREAD-7 reader 2's eleven
(V1-V11), as they read against the runner's code now; REREAD-6's fifth, P keeping the text-seal line in both modes,
was added by REREAD-8's ZB5 (before it, four of the five were made). A variant the check does not catch is said, with
what does catch it, if anything. Apart from them, and counted on their own, are REREAD-8 reader 2's four changes
(X1-X4) that the check before ZB3 let pass or caught only by chance: ZB3's plants, each of which the check must catch.
Since REREAD-9 (his ruling on ASK 9-4), also apart and counted on their own: REREAD-9 reader 2's eleven changes
(K1-K11), which the check before it passed 46 of 46, made as that reader made them; and two environment plants (NB7),
the runner unchanged and the environment changed, a sitecustomize raising the recursion limit and a bytecode prefix.
Evidence about the check, not about the reference; outside the core author's reading set (D1)."""
import concurrent.futures
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ROOTLINE = "ROOT = os.path.dirname(os.path.dirname(HERE))"
RUN_OLD = "    try:\n        it.run()\n    except interp.HostStop as e:\n"
VARIANTS = [   # (name, [(text, replacement)], what catches it if this check does not)
    ("control: the runner unchanged", [], None),
    ("REREAD-6: the ENV line removed", [('print("ENV python', '(lambda *a, **k: None)("ENV python')], None),
    ("REREAD-6: the recursion limit raised", [("        from orlog import interp\n",
                                               "        from orlog import interp\n        sys.setrecursionlimit(100000)\n")],
     None),
    ("REREAD-6: format_check imported", [("        from orlog import interp\n",
                                          "        from orlog import interp\n        sys.path.insert(0, HERE)\n"
                                          "        import format_check\n")], None),
    ("REREAD-6: BUDGET read from os.environ", [
        ('    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files',
         '    budget_s = os.environ.get("REF_BUDGET", budget_s)\n'
         '    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files')], None),
    ("REREAD-6: P keeps the text-seal line (ZB5)", [   # in both modes; V10 is the law mode's alone
        ('p = "\\n".join(ln for ln in lines if not ln.startswith(("backend ", "text-seal ")))',
         'p = "\\n".join(ln for ln in lines if not ln.startswith(("backend ",)))')], None),
    ("V1: law mode ignores BUDGET", [("it = interp.Interp(prog, an, law_seal, text_seal, trace=True, budget=budget)",
                                      "it = interp.Interp(prog, an, law_seal, text_seal, trace=True, "
                                      "budget=None if mode == \"law\" else budget)")], None),
    ("V2: the law seal from the bytes less their last LF", [("law_seal, text_seal = sha(raw), textseal",
                                                            "law_seal, text_seal = sha(raw[:-1]), textseal")], None),
    ("V3: decoder1's message dropped", [('return "DECODER-REFUSED %s" % ascii(str(e))',
                                         'return "DECODER-REFUSED \'x\'"')], None),
    ("V4: a KeyError from decode taken as a refusal", [("except decoder1.DecodeError as e:",
                                                       "except (decoder1.DecodeError, KeyError) as e:")], None),
    ("V5: a stop reports one operation more", [('return "RUN STOPPED ops %d trace %s" % (e.ops, ',
                                                'return "RUN STOPPED ops %d trace %s" % (e.ops + 1, ')], None),
    ("V6: classify, two different results RESULT", [('if a[0] == "result" and a == b:',
                                                      'if a[0] == "result" and b[0] == "result":')], None),
    ("V7: classify, two different refusals REFERENCE-REFUSED", [('if a[0] == "refused" and a == b:',
                                                                 'if a[0] == "refused" and b[0] == "refused":')], None),
    ("V8: the recursion limit raised by getattr", [("        from orlog import interp\n",
                                                    "        from orlog import interp\n"
                                                    "        getattr(sys, 'setrecursion' + 'limit')(100000)\n")], None),
    ("V9: BUDGET read through `from os import environ`", [
        (ROOTLINE, "from os import environ as _e\n" + ROOTLINE),
        ('    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files',
         "    budget_s = _e.get('REF_BUDGET', budget_s)\n"
         '    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files')], None),
    ("V10: P keeps the text-seal line in law mode only", [
        ('p = "\\n".join(ln for ln in lines if not ln.startswith(("backend ", "text-seal ")))',
         'p = "\\n".join(ln for ln in lines if not ln.startswith(("backend ",) if mode == "law" else '
         '("backend ", "text-seal ")))')], None),
    ("V11: an IndexError in law mode's run taken as a refusal", [
        (RUN_OLD, "    try:\n        it.run()\n"
                  "    except (interp.HostStop if mode == 'text' else (interp.HostStop, IndexError)) as e:\n"
                  "        if not isinstance(e, interp.HostStop):\n"
                  "            return \"DECODER-REFUSED %s\" % ascii(str(e))\n")],
     "no case of this check: no input of it makes the interpreter raise IndexError. The record's rows would change "
     "(REREAD-7's reader 2), so the hash closure of a record made by such a runner fails"),
]
ZB3_PLANTS = [   # REREAD-8 reader 2's X1-X4, made against the runner's code now; the check must catch each
    ("ZB3, X1: the conditions lines list orlog.interp alone", [
        ('for name in sorted(n for n in sys.modules if n == "orlog" or n.startswith("orlog.")):',
         'for name in sorted(n for n in sys.modules if n == "orlog.interp"):')], None),
    ("ZB3, X2: the bytecode check covers research/rust-core alone", [
        ('for p in (("src", "orlog"), ("research", "rust-core"), ("research", "law-sufficiency"))]',
         'for p in (("research", "rust-core"),)]')], None),
    ("ZB3, X3: the ENV line leaves out the platform", [
        ('conditions().replace("; orlog", "; %s; orlog" % platform.platform(), 1)),', 'conditions()),')], None),
    ("ZB3, X4: the ENV line leaves out the implementation and version", [
        ('print("ENV python %s %s %s" % (platform.python_implementation(), platform.python_version(),',
         'print("ENV python %s" % (')], None),
]


MAIN = "\n\ndef main(argv):\n"
K_PLANTS = [   # REREAD-9 reader 2's K1-K11 (its NB5 and NB6), its edits as it made them; his ruling on ASK 9-4
    ("K1: a clock read, and a line between ENV and CONDITIONS", [
        ('    try:\n        print("CONDITIONS after-run %s" % conditions())',
         '    try:\n        import time as _t\n        print("WALL %r" % _t.perf_counter())\n'
         '        print("CONDITIONS after-run %s" % conditions())')], None),
    ("K2: BUDGET from the environment, by getattr on an alias", [
        ('    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files',
         '    _o = os\n    budget_s = getattr(_o, "environ").get("REF_BUDGET", budget_s)\n'
         '    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files')], None),
    ("K3: the recursion limit raised for the run, put back after", [
        ("def reference(mods, mode, budget, textseal, raw, files):",
         "def _reference(mods, mode, budget, textseal, raw, files):"),
        (MAIN, "\n\ndef reference(*a):\n    _s = sys\n    _set = getattr(_s, 'setrecursion' + 'limit')\n"
               "    _old = _s.getrecursionlimit()\n    _set(100000)\n    try:\n        return _reference(*a)\n"
               "    finally:\n        _set(_old)\n" + MAIN)], None),
    ("K4: format_check loaded under another name", [
        ("        mods[\"decoder1\"] = decoder1\n    return mods",
         "        mods[\"decoder1\"] = decoder1\n    import importlib.util as _iu\n"
         "    _sp = _iu.spec_from_file_location('fc_alias', os.path.join(ROOT, 'research', 'rust-core', "
         "'format_' + 'check.py'))\n"
         "    _m = _iu.module_from_spec(_sp)\n    sys.modules['fc_alias'] = _m\n    _sp.loader.exec_module(_m)\n"
         "    return mods")], None),
    ("K5: a module loaded in law mode and left out of the lines", [
        ("HEX64 = re.compile", "_HIDDEN = set()\nHEX64 = re.compile"),
        ('        mods = {"interp": interp}\n',
         '        mods = {"interp": interp}\n        if mode == "law":\n            _before = set(sys.modules)\n'
         '            import orlog.canon\n            _HIDDEN.update(n for n in sys.modules if n not in _before)\n'),
        ('    for name in sorted(n for n in sys.modules if n == "orlog" or n.startswith("orlog.")):',
         '    for name in sorted(n for n in sys.modules if (n == "orlog" or n.startswith("orlog.")) and n not in '
         '_HIDDEN):')], None),
    ("K6: the after-run line made before the run", [
        ("        line = reference(mods, *args)\n", "        _after = conditions()\n        line = reference(mods, *args)\n"),
        ('        print("CONDITIONS after-run %s" % conditions())', '        print("CONDITIONS after-run %s" % _after)')],
     None),
    ("K7: TEXTSEAL ignored in law mode", [
        ("law_seal, text_seal = sha(raw), textseal", 'law_seal, text_seal = sha(raw), "0" * 64')], None),
    ("K8: --files ignored in law mode", [
        ("    it = interp.Interp(prog, an, law_seal, text_seal, trace=True, budget=budget)",
         '    files = files and mode == "text"\n    it = interp.Interp(prog, an, law_seal, text_seal, trace=True, '
         'budget=budget)')], None),
    ("K9: a text-mode stop reports one operation more", [
        ('return "RUN STOPPED ops %d trace %s" % (e.ops, ',
         'return "RUN STOPPED ops %d trace %s" % (e.ops + (mode == "text"), ')], None),
    ("K10: classify, a crash and a timeout NO-REFERENCE-RESULT", [
        ('    if a[0] in ("crash", "timeout") and a == b:',
         '    if a[0] in ("crash", "timeout") and (a == b or {a[0], b[0]} == {"crash", "timeout"}):')], None),
    ("K11: BUDGET's pattern ends with $, a trailing LF taken", [
        ('NAT = re.compile(r"(?:0|[1-9][0-9]*)\\Z")', 'NAT = re.compile(r"(?:0|[1-9][0-9]*)$")')], None),
]
ENV_PLANTS = [   # REREAD-9's NB7: the runner unchanged, the environment changed
    ("E1: a sitecustomize raises the default recursion limit", "site"),
    ("E2: PYTHONPYCACHEPREFIX set", "pycache"),
]


def environment(kind, d):
    """The environment variables an environment plant adds, its files made under D."""
    if kind == "site":
        site = os.path.join(d, "site")
        os.makedirs(site)
        with open(os.path.join(site, "sitecustomize.py"), "w", encoding="utf-8", newline="\n") as f:
            f.write("import sys\nsys.setrecursionlimit(5000)\n")
        return {"PYTHONPATH": site}
    prefix = os.path.join(d, "pycache-prefix")
    os.makedirs(prefix)
    return {"PYTHONPYCACHEPREFIX": prefix}


def one(k, name, edits, runner_src, paths_src, work, env_kind=None):
    d = os.path.join(work, "v%02d" % k)
    os.makedirs(d)
    r = runner_src.replace(ROOTLINE, "ROOT = %r" % ROOT)
    for old, new in edits:
        if r.count(old) != 1 and old != ROOTLINE:
            return name, "NOT MADE (its text is not found once)", None
        r = r.replace(old, new) if old != ROOTLINE else r.replace("ROOT = %r" % ROOT, new.replace(
            ROOTLINE, "ROOT = %r" % ROOT), 1)
    with open(os.path.join(d, "ref_run.py"), "w", encoding="utf-8", newline="\n") as f:
        f.write(r)
    p = (paths_src.replace('RUNNER = os.path.join(HERE, "ref_run.py")', "RUNNER = %r" % os.path.join(d, "ref_run.py"))
         .replace("sys.path.insert(0, HERE)\nimport ref_run", "sys.path.insert(0, %r)\nimport ref_run" % d)
         .replace("ROOT = os.path.dirname(os.path.dirname(HERE))", "ROOT = %r" % ROOT))
    with open(os.path.join(d, "paths.py"), "w", encoding="utf-8", newline="\n") as f:
        f.write(p)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    if env_kind:
        env.update(environment(env_kind, d))
    q = subprocess.run([sys.executable, "-B", os.path.join(d, "paths.py")], capture_output=True, env=env)
    last = [ln for ln in q.stdout.decode("utf-8", "replace").replace("\r\n", "\n").split("\n") if ln]
    return name, q.returncode, last[-1] if last else ""


def main():
    with open(os.path.join(HERE, "ref_run.py"), encoding="utf-8") as f:
        runner_src = f.read()
    with open(os.path.join(HERE, "ref_run_paths.py"), encoding="utf-8") as f:
        paths_src = f.read()
    work = tempfile.mkdtemp(prefix="refrunvariants-")
    try:
        jobs = ([(name, edits, None) for name, edits, _ in VARIANTS + ZB3_PLANTS + K_PLANTS]
                + [(name, [], kind) for name, kind in ENV_PLANTS])
        with concurrent.futures.ThreadPoolExecutor(3) as pool:
            results = list(pool.map(lambda kv: one(kv[0], kv[1][0], kv[1][1], runner_src, paths_src, work, kv[1][2]),
                                    enumerate(jobs)))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("THE RUNNER CHANGES THE RE-READS SHOWED, AGAINST ref_run_paths.py (research/rust-core/ref_run_variants.py)")
    bad = caught = 0
    start = len(VARIANTS)
    for title, summary, group in (("REREAD-8's ZB3: its plants, counted on their own", "ZB3'S PLANTS", ZB3_PLANTS),
                                  ("REREAD-9's K1-K11 (his ruling on ASK 9-4): plants, counted on their own",
                                   "K PLANTS", K_PLANTS),
                                  ("REREAD-9's NB7: the environment changed, the runner not; counted on their own",
                                   "ENVIRONMENT PLANTS", ENV_PLANTS)):
        print(title)
        got = 0
        for plant, (_, status, last) in zip(group, results[start:start + len(group)]):
            if status == 1 and "FAILED" in last:
                got += 1
                print("   %-58s caught: %s" % (plant[0], last))
            else:
                bad += 1
                print("   %-58s NOT CAUGHT (%s)" % (plant[0], last or status))
        print("%s %s: %d of %d caught" % (summary, "HELD" if got == len(group) else "FAILED", got, len(group)))
        start += len(group)
    print("REREAD-6's five and REREAD-7's eleven")
    for (name, edits, other), (_, status, last) in zip(VARIANTS, results):
        if not edits:
            ok = status == 0 and "HELD" in last
            print("   %-58s %s  [%s]" % (name, last, "as it must" if ok else "NOT AS IT MUST"))
        elif status == 1 and "FAILED" in last:
            ok, caught = True, caught + 1
            print("   %-58s caught: %s" % (name, last))
        else:
            ok = other is not None
            print("   %-58s NOT CAUGHT (%s): %s" % (name, last or status, other or "and nothing else names it"))
        bad += not ok
    n = len(VARIANTS) - 1
    print("REF-RUN VARIANTS %s: %d of %d changes caught by the check; the control passes; %d not caught, each said" % (
        "HELD" if bad == 0 else "FAILED", caught, n, n - caught))
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()

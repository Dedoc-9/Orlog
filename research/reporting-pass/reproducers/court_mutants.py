"""Mutation test of the reporting layer against the self-test: which planted defects does no row catch?

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/court_mutants.py [--only NAME,...]
      [--backends python,c99,rust]

The working tree (tracked files and the uncommitted, unignored ones, as they stand) is copied whole into
work/reporting-pass/mut/tree, with the self-test's compile cache copied beside it so that a run takes about a minute.
For each plant one source line of the copy is replaced (the old text must occur exactly once), the copy's own
`tests/selftest.py` is run there, every FAIL row is collected, and the line is put back. Nothing outside work/ is
written: the copy's subprocesses (compat.py, court_monotone.py, orl.py) import the copy's src, so a plant reaches them
too.

A plant SURVIVES when the self-test still reads n/n. A surviving plant is a guard with no row only if the plant is not
an equivalent mutant: each one here is paired, in the reproducer named in its `witness` field, with a run that shows the
planted code reading something the real code does not.

Controls: `none` (no plant: the copy must read n/n) and `held-ignores-unreached` (a plant the self-test's inline row
catches), so that a survivor cannot be blamed on a harness that never fails.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
MUT = os.path.join(ROOT, "work", "reporting-pass", "mut")
TREE = os.path.join(MUT, "tree")
COURT = "src/orlog/court.py"
ARB = "src/orlog/arbiter.py"
# always run: no plant (the copy must read n/n), and a plant the self-test is known to catch (its inline row), so that
# a survivor cannot be blamed on a harness that never fails. (The first draft used R8's switch as the caught control;
# it survived, and is now a finding: r8-default-off.)
CONTROLS = ("none", "held-ignores-unreached")

HELD = 'held = hit is None and r["evals"] > 0 and r["trues"] == r["evals"] and row["integrity"] == "AGREED"'
PLANTS = [
    # (name, file, old, new, what the plant breaks, the reproducer that shows it is not equivalent)
    ("none", None, None, None, "control: no plant", None),
    ("r8-default-off", COURT, "REFUSED_EVALUATION_CHECK = True", "REFUSED_EVALUATION_CHECK = False",
     "R8's shipped default switched off, as orl.py court reads it (the self-test's R8 rows and court_monotone set "
     "the switch themselves before every reading)", "r8_default.py"),
    ("held-ignores-integrity", COURT, HELD,
     'held = hit is None and r["evals"] > 0 and r["trues"] == r["evals"]',
     "R1: a claim is held although the backends did not all agree with the reference", "unguarded_held.py"),
    ("held-ignores-refutation", COURT, HELD,
     'held = hit is None and r["evals"] > 0 and row["integrity"] == "AGREED"',
     "a claim false at an evaluation is held", "unguarded_held.py"),
    ("held-ignores-unreached", COURT, HELD,
     'held = hit is None and r["trues"] == r["evals"] and row["integrity"] == "AGREED"',
     "R7: a claim never evaluated is held", "unguarded_held.py"),
    ("agreed-always", COURT,
     'agreed = witness.get("dissent_kind") == "NONE" and bool(witness.get("backends"))',
     'agreed = True', "R1: every witness read as agreed", "unguarded_held.py"),
    ("sandwich-ignores-dissent", COURT,
     '    elif not agreed:\n        sandwich = "VACUOUS (the backends did not all agree)"\n', '',
     "L10: the sandwich's own reason for a contested run is gone (it falls through to 'no claim is well-founded')",
     "unguarded_held.py"),
    ("grounding-skips-premises", COURT,
     'gr_lo, _ = support_sets(ids, {k: rows[k][1] for k in ids}, prem)',
     'gr_lo = {k for k in ids if rows[k][1]}',
     "GROUNDED without the claim's premises grounded", "the self-test's transitive R8 row"),
    ("summary-grounded-counts-all", COURT,
     '"grounded": sum(1 for r in out if r["grounding"] == "GROUNDED"),',
     '"grounded": len(out),', "the printed summary counts every claim GROUNDED", "unguarded_held.py"),
    ("summary-well-founded-counts-unsupported", COURT,
     '"well_founded": sum(1 for r in out if r["support"] == "WELL-FOUNDED"),',
     '"well_founded": sum(1 for r in out if r["support"] in ("WELL-FOUNDED", "UNSUPPORTED")),',
     "the printed summary counts UNSUPPORTED claims as WELL-FOUNDED", "unguarded_held.py"),
    ("agreement-ignores-exit", ARB,
     'and r.get("out") == bytes(ref.out) and r.get("exit") == 0)',
     'and r.get("out") == bytes(ref.out))',
     "a backend that exits with an error status after writing its files is counted agreeing",
     "agreement_conditions.py"),
    ("agreement-ignores-output", ARB,
     'and r.get("out") == bytes(ref.out) and r.get("exit") == 0)',
     'and r.get("exit") == 0)',
     "a backend whose output file differs from the reference's is counted agreeing when its receipt matches",
     "agreement_conditions.py"),
    # a plant given as a list of (old, new) pairs replaces each, once
    ("agreement-lenient-receipts", ARB,
     [('ok = (r.get("receipt") is not None and receipt_core(r["receipt"]) == ref_core and ref_core is not None',
       'ok = (r.get("receipt") is not None and parse_receipt(r["receipt"]) == parse_receipt(ref.receipt())')], None,
     "E7 put back in the verdict: receipts compared through splitlines with every 'backend ' line dropped "
     "(the E7 row tests receipt_core as a function, not the arbiter's use of it)", "agreement_conditions.py"),
    ("run-folder-made-but-shared", ARB,
     [('        rundir = tempfile.mkdtemp(prefix="arb-", dir=self.workdir)\n',
       '        rundir = tempfile.mkdtemp(prefix="arb-", dir=self.workdir)\n'
       '        shared = os.path.join(self.workdir, "shared-runs")\n        os.makedirs(shared, exist_ok=True)\n'),
      ('r = self.run(cmd, "%s-%s" % (name, b), cwd=rundir)', 'r = self.run(cmd, "%s-%s" % (name, b), cwd=shared)'),
      ('trace=True, cwd=rundir)', 'trace=True, cwd=shared)')], None,
     "the shared work folder defect behind a fresh, unused run folder: every arbitration makes and removes its own "
     "folder, and runs in one shared folder", "the self-test's race row, if it fails"),
    ("chain-600-refused-by-compilers", ARB,
     [('                src = self.mutate(b, generate(b, low))\n',
       '                src = self.mutate(b, generate(b, low))\n'
       '                if len(comp.prog.clauses) >= 600 and b == "c99":\n'
       '                    src += "\\n#error the E10 class: a compiler refusing the 600-arm chain\\n"\n'
       '                if len(comp.prog.clauses) >= 600 and b == "rust":\n'
       '                    src += "\\ncompile_error!(\\"the E10 class: a compiler refusing the 600-arm chain\\");\\n"\n')],
     None, "E10's class on the compiled backends: both compilers refuse the 600-arm If chain, which only the "
     "self-test's chain row runs", "the chain row's own detail line"),
]


def tracked_and_unignored():
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    return sorted(p for p in out.split("\0") if p and not p.startswith(("work/", "build/", "research/reporting-pass/")))


def make_tree():
    if os.path.isdir(TREE):
        shutil.rmtree(TREE)
    for rel in tracked_and_unignored():
        src = os.path.join(ROOT, rel)
        if not os.path.isfile(src):         # deleted in the working tree
            continue
        dst = os.path.join(TREE, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)           # bytes as they are: LF stays LF
    cache = os.path.join(ROOT, "build", "selftest", "cache")
    if os.path.isdir(cache):                # content-addressed by the generated source and flags: safe to reuse
        shutil.copytree(cache, os.path.join(TREE, "build", "selftest", "cache"),
                        ignore=shutil.ignore_patterns("*.tmp-*"))


def run_selftest(backends):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-B", "tests/selftest.py", "--backends", backends], cwd=TREE, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--backends", default="python,c99,rust")
    ap.add_argument("--keep-tree", action="store_true")
    a = ap.parse_args(argv)
    if os.environ.get("PYTHONHASHSEED") != "0":
        print("set PYTHONHASHSEED=0")
        return 2
    only = set(a.only.split(",")) if a.only else None
    os.makedirs(MUT, exist_ok=True)
    make_tree()
    results = []
    for name, rel, old, new, what, witness in PLANTS:
        if only and name not in only and name not in CONTROLS:
            continue
        path = os.path.join(TREE, rel) if rel else None
        saved = None
        if path:
            with open(path, "rb") as fh:
                saved = fh.read()
            text = saved.decode("utf-8")
            reps = old if isinstance(old, list) else [(old, new)]
            counts = [text.count(o) for o, _ in reps]
            if counts != [1] * len(reps):
                print("plant %s: its old texts occur %s times in %s; not applied" % (name, counts, rel))
                results.append((name, "NOT APPLIED", []))
                continue
            for o, n_ in reps:
                text = text.replace(o, n_)
            with open(path, "wb") as fh:
                fh.write(text.encode("utf-8"))
        try:
            code, out, err = run_selftest(a.backends)
        finally:
            if path:
                with open(path, "wb") as fh:
                    fh.write(saved)
        with open(os.path.join(MUT, "selftest-%s.txt" % name), "wb") as fh:
            fh.write((out + ("\n--- stderr ---\n" + err if err.strip() else "")).encode("utf-8"))
        fails = [l for l in out.splitlines() if l.startswith("[FAIL]")]
        m = re.search(r"^ORLOG SELFTEST (\d+)/(\d+)", out, re.M)
        summary = m.group(0) if m else "NO SUMMARY (exit %d): %s" % (code, err.strip()[-300:])
        if name == "none":
            verdict = "CONTROL HELD" if m and m.group(1) == m.group(2) else "CONTROL BROKEN"
        else:
            verdict = "CAUGHT" if fails or not m or m.group(1) != m.group(2) else "SURVIVED"
        results.append((name, verdict, fails))
        print("%-42s %-14s %s" % (name, verdict, summary))
        for l in fails[:4]:
            print("      " + l[:160])
        print("      breaks: %s; non-equivalence shown by: %s" % (what, witness or "-"))
        sys.stdout.flush()
    survived = [n for n, v, _ in results if v == "SURVIVED"]
    print("SURVIVED %d of %d plants: %s" % (len(survived), sum(1 for n, _, _ in results if n != "none"),
                                            ", ".join(survived) or "none"))
    ok = any(n == "none" and v == "CONTROL HELD" for n, v, _ in results) and \
        any(n == CONTROLS[1] and v == "CAUGHT" for n, v, _ in results)
    print("HARNESS %s" % ("HELD (no plant reads n/n, and the plant %s is caught)" % CONTROLS[1] if ok else "BROKEN"))
    if not a.keep_tree:
        shutil.rmtree(TREE, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

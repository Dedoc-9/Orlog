"""Plant defects in copies of orlog_rt.rs and require the harness to fail on each (the deliverable
is never edited). usage: python -B mutants.py   (from rt_rs)"""
import os
import shutil
import subprocess
import sys

RT = "orlog_rt.rs"
MUTANTS = [
    ("x_mul tie goes odd", "let q = if r > half || (r == half && (q & 1) == 1) { q + 1 } else { q };\n    orl_chk(q)\n}\n\n/// DIVISION",
     "let q = if r > half || (r == half && (q & 1) == 0) { q + 1 } else { q };\n    orl_chk(q)\n}\n\n/// DIVISION"),
    ("no NaN canonicalization", "    if orl_f_isnan(b) {\n        ORL_CANON_NAN_BITS\n    } else {\n        b\n    }",
     "    if orl_f_isnan(b) && false {\n        ORL_CANON_NAN_BITS\n    } else {\n        b\n    }"),
    ("fmt_f 5^13 off by one", "orl_big_mul_small(&mut big, 1_220_703_125);", "orl_big_mul_small(&mut big, 1_220_703_124);"),
    ("x_sub method calls x_add", "self.or_refuse(orl_x_sub(a, b), c)", "self.or_refuse(orl_x_add(a, b), c)"),
    ("SHA-256 last K constant", "0xbef9a3f7, 0xc67178f2,", "0xbef9a3f7, 0xc67178f3,"),
    # (i_div checking OVERFLOW before INEXACT-DIVISION would be an equivalent mutant: the only
    # Int quotient that overflows, MIN / -1, is exact.)
    ("i_quot truncates instead of Euclid", "orl_chk((a as i128).div_euclid(b as i128))", "orl_chk((a as i128) / (b as i128))"),
]

src = open(RT, encoding="utf-8").read()
os.makedirs("build/mut", exist_ok=True)
caught = 0
for name, old, new in MUTANTS:
    if src.count(old) != 1:
        sys.exit("mutant %r: the text to replace occurs %d times" % (name, src.count(old)))
    with open("build/mut/orlog_rt.rs", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src.replace(old, new))
    shutil.copy("test_rt.rs", "build/mut/test_rt.rs")
    b = subprocess.run(["rustc", "--edition", "2021", "-O", "build/mut/test_rt.rs", "-o", "build/mut/test_rt.exe"],
                       capture_output=True, text=True)
    if b.returncode != 0:
        sys.exit("mutant %r does not compile:\n%s" % (name, b.stderr))
    r = subprocess.run([os.path.abspath(os.path.join("build", "mut", "test_rt.exe")),
                        os.path.join("..", "vectors", "runtime-vectors.txt")], capture_output=True, text=True)
    summary = [l for l in r.stdout.splitlines() if l.startswith("RUNTIME")]
    fails = sum(1 for l in r.stdout.splitlines() if l.startswith("FAIL"))
    ok = r.returncode != 0 and fails > 0
    caught += ok
    print("%-42s %s  (%d FAIL lines; %s)" % (name, "CAUGHT" if ok else "NOT CAUGHT", fails, "; ".join(summary)))
print("MUTANTS CAUGHT %d / %d" % (caught, len(MUTANTS)))
sys.exit(0 if caught == len(MUTANTS) else 1)

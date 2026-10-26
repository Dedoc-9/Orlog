"""Planted defects: does the apparatus (test_rt.c, check_chain.py, check_smoke.py) catch them?

Each plant is one textual change to a copy of orlog_rt.h, made in its own folder
under plants_build/ beside copies of test_rt.c and smoke.c (so that their
#include "orlog_rt.h" takes the planted copy). The folder is built with the
required flags and run: the harness on the vectors (with its chain check and
extra checks) and both smoke variants through check_smoke.py. A plant is
CAUGHT when any witness fails. The control (no change) must pass everything.

  python -B plants.py            (from anywhere; uses clang on PATH)
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VECTORS = os.path.join(ROOT, "vectors", "runtime-vectors.txt")
BUILD = os.path.join(HERE, "plants_build")
FLAGS = ["-std=c99", "-pedantic", "-Wall", "-Wextra", "-O2", "-ffp-contract=off", "-fno-fast-math"]

PLANTS = [
    ("control", None, None, 0),
    ("x_mul ties round up",
     "if (f > ORL__HALF32 || (f == ORL__HALF32 && (ql & 1u) != 0)) {", "if (f >= ORL__HALF32) {", 1),
    ("x_div ties round up",
     "if (r > ub - r || (r == ub - r && (ql & 1u) != 0)) {", "if (r >= ub - r) {", 1),
    ("x_round ties round up",
     "if (f > ORL__HALF32 || (f == ORL__HALF32 && (q & 1u) != 0)) q += 1;", "if (f >= ORL__HALF32) q += 1;", 1),
    ("i_quot truncates", "if (r < 0) q = b > 0 ? q - 1 : q + 1;", "(void)r;", 1),
    ("i_rem truncates", "if (r < 0) r = b > 0 ? r + b : r - b;", "(void)b;", 1),
    ("i_div checks overflow first",
     "    if (a % b != 0) { *e = ORL_INEXACT_DIVISION; return 0; }\n    return a / b;",
     "    if (a % b != 0) { *e = ORL_OVERFLOW; return 0; }\n    return a / b;", 1),
    ("isqrt off by one", "    return (int64_t)orl__isqrt128(0, (uint64_t)a);",
     "    return (int64_t)orl__isqrt128(0, (uint64_t)a + 1u);", 1),
    ("f_from_i ties away", "if (rem > half || (rem == half && (m & 1u) != 0)) {", "if (rem >= half) {", 1),
    ("int-to-double exactness ignored",
     "            if (!rounded) { *e = ORL_INEXACT_CONVERSION; return 0.0; }\n", "", 1),
    ("f_round ties away", "if (r > half || (r == half && (q & 1u) != 0)) q += 1;", "if (r >= half) q += 1;", 1),
    ("f_to_x scales by 2^31", "return orl__f_to_i(x, 32, rounded", "return orl__f_to_i(x, 31, rounded", 1),
    ("f_max as fmax", "static inline double orl_f_max(double a, double b) { return a > b ? a : b; }",
     "static inline double orl_f_max(double a, double b) { return fmax(a, b); }", 1),
    ("f_div by zero not canonical", "if (orl__isnan_bits(orl__fb(a)) || a == 0.0) return orl__bf(ORL__CANON_NAN);",
     "if (orl__isnan_bits(orl__fb(a)) || a == 0.0) return orl__bf(UINT64_C(0xFFF8000000000000));", 1),
    ("fmt_x integral prints .1", "if (frac == 0) buf[n++] = '0';", "if (frac == 0) buf[n++] = '1';", 1),
    ("fmt_f wrong 5^13", "1220703125u", "1220703124u", 1),
    ("fmt_f drops the sign of -0.0", "    if (u >> 63) buf[n++] = '-';\n", "", 1),
    ("SHA-256 K[0] wrong", "0x428a2f98u", "0x428a2f99u", 1),
    ("wrapper passes clause + 1", "orl__i_add(a, b, &e); if (e) orl_refuse(e, c);",
     "orl__i_add(a, b, &e); if (e) orl_refuse(e, c + 1);", 2),
    ("chain clause little-endian", "    orl__be32(hd + 1, c);\n",
     "    hd[1] = (uint8_t)c; hd[2] = (uint8_t)(c >> 8); hd[3] = (uint8_t)(c >> 16); hd[4] = (uint8_t)(c >> 24);\n", 1),
    ("say hashes no LF", "    orl__sha_update(&orl__out_hash, \"\\n\", 1);\n", "", 1),
    ("F events not canonical", "orl__be64(p, orl__isnan_bits(u) ? ORL__CANON_NAN : u);", "orl__be64(p, u);", 1),
    ("B events not 0/1", "p[0] = (uint8_t)(slot != 0);", "p[0] = (uint8_t)slot;", 1),
    ("claim cost not summed", "rec->cost += cost;", "rec->cost = cost;", 1),
    ("builder limit off by one", "if (n > (size_t)(ORL_TEXT_MAX - orl__sb_len)) {",
     "if (n >= (size_t)(ORL_TEXT_MAX - orl__sb_len)) {", 1),
    ("output limit off by one", "if (line > ORL_OUTPUT_MAX - orl__out_bytes) {",
     "if (line >= ORL_OUTPUT_MAX - orl__out_bytes) {", 1),
    ("l_get accepts index 0", "if (k < 1 || (uint64_t)k > l->len) { orl_refuse(ORL_INDEX_OUT_OF_RANGE, c); return 0; }",
     "if (k < 0 || (uint64_t)k > l->len) { orl_refuse(ORL_INDEX_OUT_OF_RANGE, c); return 0; }", 1),
]


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def main():
    rc, ref = run([sys.executable, "-B", os.path.join(ROOT, "src", "check_chain.py")], ROOT)
    ref_heads = [line.strip() for line in ref.splitlines() if line.startswith("head")]
    src = open(os.path.join(HERE, "orlog_rt.h"), "rb").read().decode("utf-8")
    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)
    caught_all = True
    print("%-34s %-30s %-6s %-6s %-6s %-6s  %s" % ("plant", "vectors", "heads", "files", "extra", "smoke", "verdict"))
    for k, (name, old, new, count) in enumerate(PLANTS):
        d = os.path.join(BUILD, "p%02d" % k)
        os.makedirs(d)
        text = src
        if old is not None:
            if text.count(old) != count:
                print("%-34s PLANT DID NOT APPLY (%d occurrences, %d expected)" % (name, text.count(old), count))
                caught_all = False
                continue
            text = text.replace(old, new)
        with open(os.path.join(d, "orlog_rt.h"), "wb") as fh:
            fh.write(text.encode("utf-8"))
        for f in ("test_rt.c", "smoke.c"):
            shutil.copy(os.path.join(HERE, f), d)
        rc1, log1 = run(["clang"] + FLAGS + ["test_rt.c", "-o", "test_rt.exe"], d)
        rc2, log2 = run(["clang"] + FLAGS + ["smoke.c", "-o", "smoke.exe"], d)
        rc3, log3 = run(["clang"] + FLAGS + ["-DSMOKE_REFUSE", "smoke.c", "-o", "smoke_refuse.exe"], d)
        if rc1 or rc2 or rc3:
            print("%-34s BUILD FAILED" % name)
            print(log1 + log2 + log3)
            caught_all = False
            continue
        _, out = run([os.path.join(d, "test_rt.exe"), VECTORS, d], d)
        vec = next((l for l in out.splitlines() if l.startswith("RUNTIME VECTORS")), "RUNTIME VECTORS (none)")
        heads = [l.strip() for l in out.splitlines() if l.startswith("head")]
        heads_ok = heads == ref_heads and len(heads) == 4
        files_ok = "CHAIN FILES CONSISTENT WITH THE HEADS" in out
        extra = next((l for l in out.splitlines() if l.startswith("EXTRA CHECKS")), "EXTRA CHECKS (none)")
        xp = extra.split()
        extra_ok = len(xp) == 5 and xp[2] == xp[4]
        vec_ok = vec.split()[2:] == ["20015", "/", "20015"]
        smoke_ok = True
        for exe, mode in (("smoke.exe", "complete"), ("smoke_refuse.exe", "refuse")):
            run([os.path.join(d, exe), "o.txt", "r.txt", "t.txt"], d)
            rc4, log4 = run([sys.executable, "-B", os.path.join(HERE, "check_smoke.py"),
                             os.path.join(d, "o.txt"), os.path.join(d, "r.txt"), os.path.join(d, "t.txt"), mode], d)
            smoke_ok = smoke_ok and rc4 == 0
        caught = not (vec_ok and heads_ok and files_ok and extra_ok and smoke_ok)
        if name == "control":
            verdict = "PASSES (as it must)" if not caught else "CONTROL FAILED"
            caught_all = caught_all and not caught
        else:
            verdict = "CAUGHT" if caught else "MISSED"
            caught_all = caught_all and caught
        print("%-34s %-30s %-6s %-6s %-6s %-6s  %s" % (
            name, vec, "ok" if heads_ok else "DIFF", "ok" if files_ok else "BAD",
            " ".join(xp[2:]) if len(xp) == 5 else "?", "ok" if smoke_ok else "FAIL", verdict))
    shutil.rmtree(BUILD)
    print("PLANTS: %s" % ("every plant caught, control clean" if caught_all else "NOT ALL CAUGHT"))
    return 0 if caught_all else 1


if __name__ == "__main__":
    sys.exit(main())

"""AddressSanitizer over the C backend (red team E21's repair).

Every corpus program, every red-team fixture that compiles, and the E21 fixtures are compiled from their generated C
with -fsanitize=address and run. Each must exit 0 with no sanitizer report, and its output and receipt (without the
backend line) must equal the reference interpreter's byte for byte. Off the self-test: the sanitizer's runtime is
the host's (on Windows, clang's DLL is put on PATH for the run).

  python -B tests/asan_c.py              every program
  python -B tests/asan_c.py --plant      the E21 fixtures under a planted store that frees before it copies
                                         (the order of a proposed fix that was not adopted): self_store must fail
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.arbiter import generate, receipt_core  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402
from orlog.lower import Lowered  # noqa: E402

FLAGS = ["-std=c99", "-O1", "-g", "-fsanitize=address", "-fno-omit-frame-pointer", "-ffp-contract=off",
         "-fno-fast-math"]
PATTERNS = ["examples/*.orl", "examples/spellings/*.orl", "tests/fixtures/redteam/*.orl", "tests/fixtures/e21/*.orl"]
PLANT_STORE = """static inline void orl_t_store(orl_text *var, orl_tslot *slot, orl_text v) {
    uint8_t *p;
    free(slot->p);
    p = (uint8_t *)orl__alloc(v.n);
    memcpy(p, v.p, v.n);
    slot->p = p;
    slot->cap = v.n;
    var->p = v.n != 0 ? slot->p : orl__empty;
    var->n = v.n;
}
"""


def plant_free_before_copy(src):
    head = "static inline void orl_t_store("
    a = src.index(head)
    b = src.index("\n}\n", a) + 3
    return src[:a] + PLANT_STORE + src[b:]


def run_env():
    env = dict(os.environ)
    if os.name == "nt":
        res = subprocess.run(["clang", "-print-resource-dir"], capture_output=True, text=True).stdout.strip()
        env["PATH"] = os.path.join(res, "lib", "windows") + os.pathsep + env.get("PATH", "")
    return env


def check(path, env, plant=False):
    with open(path, "rb") as fh:
        comp = compile_bytes(fh.read())
    if not comp.ok:
        return None
    ref = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
    src = generate("c99", Lowered(comp))
    if plant:
        src = plant_free_before_copy(src)
    tmp = tempfile.mkdtemp(prefix="orlog-asan-")
    try:
        with open(os.path.join(tmp, "p.c"), "wb") as fh:
            fh.write(src.encode("utf-8"))
        b = subprocess.run(["clang"] + FLAGS + ["p.c", "-o", "p.exe"], capture_output=True, text=True, cwd=tmp)
        if b.returncode != 0:
            return "BUILD FAILED: " + (b.stdout + b.stderr)[-300:]
        r = subprocess.run([os.path.join(tmp, "p.exe"), "out.bin", "receipt.txt"], capture_output=True, cwd=tmp,
                           env=env, timeout=600)
        err = r.stderr.decode("utf-8", "replace")
        if r.returncode != 0 or "AddressSanitizer" in err:
            kind = [l.strip() for l in err.splitlines() if "ERROR: AddressSanitizer" in l]
            return "exit %d: %s" % (r.returncode, kind[0] if kind else err[-600:])
        with open(os.path.join(tmp, "out.bin"), "rb") as fh:
            out = fh.read()
        with open(os.path.join(tmp, "receipt.txt"), "rb") as fh:
            rec = fh.read()
        if out != bytes(ref.out) or receipt_core(rec) != receipt_core(ref.receipt()):
            return "differs from the reference"
        return ""
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    env = run_env()
    if "--plant" in sys.argv:
        verdict = check(os.path.join(ROOT, "tests", "fixtures", "e21", "self_store.orl"), env, plant=True)
        caught = bool(verdict) and "heap-use-after-free" in verdict
        print("plant free-before-copy: %s -- %s" % ("CAUGHT" if caught else "SURVIVED", " ".join(
            l.strip() for l in (verdict or "no report").splitlines() if "ERROR: AddressSanitizer" in l)[:200]
            or (verdict or "no report")[:200]))
        return 0 if caught else 1
    paths = [p for pat in PATTERNS for p in sorted(glob.glob(os.path.join(ROOT, pat)))]
    clean = ran = 0
    for p in paths:
        verdict = check(p, env)
        if verdict is None:
            continue
        ran += 1
        name = os.path.relpath(p, ROOT).replace(os.sep, "/")
        if verdict == "":
            clean += 1
            print("[CLEAN] %s" % name)
        else:
            print("[FAIL]  %s -- %s" % (name, verdict))
    print("ASAN C %d/%d clean under -fsanitize=address and byte-identical to the reference" % (clean, ran))
    return 0 if clean == ran else 1


if __name__ == "__main__":
    sys.exit(main())

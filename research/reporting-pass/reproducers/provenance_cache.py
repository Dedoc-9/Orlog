"""The arbiter keys a compiled build by its generated source and flags, never by the compiler that made it, and runs
a cached build without asking the compiler. The witness's provenance names the compiler on PATH now.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/provenance_cache.py

A stand-in `clang` is compiled (by the real clang) into work/reporting-pass/fakecc/, and removed at the end: asked
--version it answers "clang version 0.0.0 (...)", asked to build anything it fails. Then, for examples/collatz.orl and
the c99 backend only:
  1. work folder A, the real clang: built, AGREED (this fills A's cache);
  2. work folder A, the stand-in first on PATH: the cached build is used; the verdict and the witness's toolchains;
  3. work folder A, the stand-in: a law A's cache does not hold (examples/fall.orl);
  4. work folder B, empty, the stand-in: collatz again.
(c) The Python backend's cached source is run as found, and the witness reports the sha256 of the source generated in
    memory: the cached file for collatz is overwritten with the generated source of another law (fall.orl) and
    collatz is arbitrated again. This one needs a hand on the cache; it shows what source_sha256 attests, nothing more.
"""
import os
import shutil
import subprocess
import sys

import _common as C

C.require_env()
from orlog import arbiter as A  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.lower import Lowered  # noqa: E402

FAKE_C = rb"""#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++)
        if (strcmp(argv[i], "--version") == 0) {
            printf("clang version 0.0.0 (a stand-in written by the reporting pass; it builds nothing)\n");
            return 0;
        }
    fprintf(stderr, "this stand-in builds nothing\n");
    return 1;
}
"""


def verdict(w):
    b = w["backends"].get("c99") or w["backends"].get("python") or {}
    return "%s, build %s, agreeing [%s], did not build [%s]" % (
        w["dissent_kind"], b.get("build"), ",".join(w["agreeing"]), ",".join(w.get("build_failed", [])))


def main():
    fake = os.path.join(C.WORK, "fakecc")
    os.makedirs(fake, exist_ok=True)
    with open(os.path.join(fake, "fakeclang.c"), "wb") as fh:
        fh.write(FAKE_C)
    exe = os.path.join(fake, "clang.exe" if os.name == "nt" else "clang")
    r = subprocess.run(["clang", "-std=c99", os.path.join(fake, "fakeclang.c"), "-o", exe], capture_output=True,
                       text=True)
    if r.returncode != 0:
        print("could not build the stand-in: %s" % r.stderr[-300:])
        return 1
    real_path = os.environ["PATH"]
    wa, wb = C.workdir("cache-A"), C.workdir("cache-B")
    for d in (wa, wb):
        shutil.rmtree(os.path.join(d, "cache"), ignore_errors=True)
    collatz, fall = C.read("examples/collatz.orl"), C.read("examples/fall.orl")

    def arb(wd):
        return A.Arbiter(wd, backends=("c99",))
    _, w1, _ = arb(wa).arbitrate(collatz, "pc-collatz")
    print("1. folder A, real clang (%s): %s" % (A.toolchains()["clang"], verdict(w1)))
    os.environ["PATH"] = fake + os.pathsep + real_path
    try:
        named = A.toolchains()["clang"]
        _, w2, _ = arb(wa).arbitrate(collatz, "pc-collatz")
        art = A.witness_artifact(w2)
        print("2. folder A, the stand-in on PATH: %s; the witness's provenance names clang as %r" % (
            verdict(w2), art["provenance"]["toolchains"]["clang"]))
        _, w3, _ = arb(wa).arbitrate(fall, "pc-fall")
        print("3. folder A, the stand-in, fall.orl (not in A's cache): %s" % verdict(w3))
        _, w4, _ = arb(wb).arbitrate(collatz, "pc-collatz")
        print("4. folder B (empty), the stand-in, collatz again: %s" % verdict(w4))
    finally:
        os.environ["PATH"] = real_path
    shown = (named.startswith("clang version 0.0.0") and w2["dissent_kind"] == "NONE" and
             w4["dissent_kind"] == "BUILD-FAILED")
    print("   the same law and the same named toolchain read %s in folder A and %s in folder B" % (
        w2["dissent_kind"], w4["dissent_kind"]))
    # (c) the Python backend's cached source
    wc = C.workdir("cache-C")
    shutil.rmtree(os.path.join(wc, "cache"), ignore_errors=True)
    pa = A.Arbiter(wc, backends=("python",))
    _, w5, _ = pa.arbitrate(collatz, "pc-py")
    src = A.generate("python", Lowered(compile_bytes(collatz)))
    key = A.sha((src + "\0").encode("utf-8"))[:24]
    cached = os.path.join(wc, "cache", "python-%s.py" % key)
    other = A.generate("python", Lowered(compile_bytes(fall)))
    with open(cached, "wb") as fh:
        fh.write(other.encode("utf-8"))
    _, w6, _ = pa.arbitrate(collatz, "pc-py")
    reported = w6["backends"]["python"]["source_sha256"]
    print("(c) python, collatz's cached source replaced by fall.orl's: %s; source_sha256 reported %s, which is %s" % (
        verdict(w6), reported[:16], "collatz's generated source (not what ran)" if reported == A.sha(
            src.encode("utf-8")) else "what ran"))
    print("CACHE: a warm cache answers for a compiler that cannot build: %s" % shown)
    shutil.rmtree(fake, ignore_errors=True)       # never leave a stand-in compiler where a PATH could find it
    return 0


if __name__ == "__main__":
    sys.exit(main())

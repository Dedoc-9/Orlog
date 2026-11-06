"""RUST-CORE-0 phase 0: do kept_evidence.py's checks bite, and report a damaged kept file rather than raise? (REREAD-9's
NB12, his ruling on ASK 9-5: "Both checks verify the kept file's SHA-256 before decompression and report damage rather
than raising an uncontrolled exception. Include a damaged-file plant.")

  python -B research/rust-core/kept_evidence_plants.py SCRATCH

Each plant is made in a copy of the kept folder under SCRATCH; the repository's kept folder is never touched. The
control must hold. Each plant must make `check` report the damage and fail: a plant whose check raises is MISSED, not
caught (the earlier plants, `work/rust-core/provenance/kept_plants.py`, counted a raise as caught). Two of the plants
are damage of the kind that made gzip raise before the check read the kept file's sha256 first: one that makes
`gzip.decompress` raise `zlib.error`, and one that makes it raise `BadGzipFile`; each is found by trying positions in
order, and the plant says which position. Off the gate."""
import gzip
import importlib.util
import io
import os
import shutil
import sys
import zlib
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ke", os.path.join(HERE, "kept_evidence.py"))
ke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ke)
REAL = ke.KEPT
results = []


def run(kept):
    """kept_evidence's check on a kept folder: (held, its last line, or 'raised …')."""
    ke.KEPT, ke.MANIFEST = kept, os.path.join(kept, "MANIFEST.txt")
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            ok = ke.check()
    except Exception as e:                      # a raise is never a catch
        return None, "raised %s" % type(e).__name__
    return ok, buf.getvalue().strip().split("\n")[-1]


def first_raising(packed, kind):
    """The first position whose one flipped bit makes gzip.decompress raise KIND, or None."""
    for i in range(10, len(packed) - 8):
        b = bytearray(packed)
        b[i] ^= 1
        try:
            gzip.decompress(bytes(b))
        except kind:
            return i
        except Exception:
            continue
    return None


def main(scr):
    ok, last = run(REAL)
    results.append(ok is True)
    print("%-6s control, the kept folder as it is: %s" % ("PASS" if ok is True else "FAIL", last[:110]))
    rows = [ln.split(" | ") for ln in open(os.path.join(REAL, "MANIFEST.txt"), encoding="utf-8")
            if ln.strip() and not ln.startswith("#")]
    first = rows[0]
    rel_kept = first[3][len("kept/"):]
    packed = open(os.path.join(REAL, rel_kept), "rb").read()
    at = {"zlib.error": first_raising(packed, zlib.error), "BadGzipFile": first_raising(packed, gzip.BadGzipFile)}

    def flip(i):
        def fn(d):
            p = os.path.join(d, rel_kept)
            b = bytearray(open(p, "rb").read())
            b[i] ^= 1
            open(p, "wb").write(bytes(b))
        return fn

    def recompress(d):          # the kept file replaced by other bytes that decompress to something else
        open(os.path.join(d, rel_kept), "wb").write(gzip.compress(b"not the evidence", 9, mtime=0))

    def truncate(d):            # the kept file cut short
        p = os.path.join(d, rel_kept)
        open(p, "wb").write(open(p, "rb").read()[: len(packed) // 2])

    def manifest_field(index, new):
        def fn(d):
            p = os.path.join(d, "MANIFEST.txt")
            t = open(p, encoding="utf-8").read()
            old = " | ".join(first)
            fields = list(first)
            fields[index] = new
            open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, " | ".join(fields), 1))
        return fn

    def gone(d):                # a kept file removed
        os.remove(os.path.join(d, rel_kept))

    plants = [("a byte in the middle of a kept file flipped", flip(len(packed) // 2)),
              ("a kept file replaced", recompress), ("a kept file cut short", truncate),
              ("the manifest's sha256 of the source changed",
               manifest_field(2, first[2][:-1] + ("0" if first[2][-1] != "0" else "1"))),
              ("the manifest's length changed", manifest_field(1, str(int(first[1]) + 1))),
              ("a kept file removed", gone)]
    for kind, i in sorted(at.items()):
        if i is None:
            results.append(False)
            print("FAIL   no position of the first kept file makes gzip raise %s; the plant cannot be made" % kind)
        else:
            plants.append(("damage that makes gzip raise %s (bit 0 of byte %d)" % (kind, i), flip(i)))
    for name, fn in plants:
        d = os.path.join(scr, "kept-evidence-plants", "p%02d" % len(results))
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(REAL, d)
        fn(d)
        ok, last = run(d)
        caught = ok is False
        results.append(caught)
        print("%-6s %s: %s" % ("CAUGHT" if caught else "MISSED", name, last[:110]))
    print("KEPT-EVIDENCE PLANTS: %d of %d as stated" % (sum(results), len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

"""RUST-CORE-0 phase 0: the evidence kept itself, beside its sha256 (SHEET.md Amendment 8; the owner's ruling I on
REREAD-8). In his words: "Hashes establish identity; they do not substitute for retaining the evidence."

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/kept_evidence.py check
  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/kept_evidence.py make SOURCE... (once, by the writer)

`make` copies each SOURCE (a path under the repository's root) into `research/rust-core/kept/`, at its own relative
path with `.gz` added, compressed by Python's own gzip at level 9 with no timestamp, so that the same bytes always give
the same file. It refuses a file already kept: nothing kept is ever written over. It appends one line to
`research/rust-core/kept/MANIFEST.txt` for each: the source's path, its length, its sha256, and the kept file's sha256.

`check` reads the manifest and, for every line, checks the kept file's own sha256 first, before anything decompresses
it, then decompresses it and checks its length and sha256 against the line; where the source still stands, it checks
the source is the same bytes. A damaged kept file is reported, never a crash (REREAD-9's NB12, his ruling on ASK 9-5;
the plants are in `kept_evidence_plants.py`). It needs nothing but Python's standard library. It changes nothing.

What it does not show: that a kept file is right, only that it is the bytes the manifest names. Off the gate."""
import gzip
import hashlib
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KEPT = os.path.join(HERE, "kept")
MANIFEST = os.path.join(KEPT, "MANIFEST.txt")
HEAD = ("# the evidence kept itself (SHEET.md Amendment 8): source path | length | sha256 | kept file | its sha256; "
        "each kept file is the source compressed by Python's gzip, level 9, no timestamp\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rows():
    if not os.path.exists(MANIFEST):
        return []
    with open(MANIFEST, encoding="utf-8") as f:
        return [ln.rstrip("\n").split(" | ") for ln in f if ln.strip() and not ln.startswith("#")]


def make(sources):
    have = {r[0] for r in rows()}
    os.makedirs(KEPT, exist_ok=True)
    if not os.path.exists(MANIFEST):
        with open(MANIFEST, "x", encoding="utf-8", newline="\n") as f:
            f.write(HEAD)
    for s in sources:
        rel = os.path.relpath(os.path.abspath(s), ROOT).replace(os.sep, "/")
        if rel.startswith("..") or rel in have:
            sys.exit("KEPT-EVIDENCE: %s is outside the repository or already kept; nothing is written over" % rel)
        with open(os.path.join(ROOT, rel), "rb") as f:
            data = f.read()
        packed = gzip.compress(data, 9, mtime=0)
        assert gzip.decompress(packed) == data
        out = os.path.join(KEPT, rel + ".gz")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "xb") as f:
            f.write(packed)
        line = " | ".join([rel, str(len(data)), sha(data), "kept/" + rel + ".gz", sha(packed)])
        with open(MANIFEST, "a", encoding="utf-8", newline="\n") as f:
            f.write(line + "\n")
        have.add(rel)
        print("kept %s: %d bytes, %d compressed" % (rel, len(data), len(packed)))


def check():
    held = n = 0
    total = packed_total = 0
    for rel, length, digest, kept, kept_digest in rows():
        n += 1
        assert kept.startswith("kept/"), kept
        path = os.path.join(KEPT, kept[len("kept/"):])     # the folder being checked, not this script's own
        if not os.path.exists(path):
            print("BAD  %s: its kept file %s is missing" % (rel, kept))
            continue
        with open(path, "rb") as f:
            packed = f.read()
        if sha(packed) != kept_digest:                  # NB12: the kept file's own sha256 before anything decompresses it
            print("BAD  %s: its kept file is not the bytes the manifest names" % rel)
            continue
        try:
            data = gzip.decompress(packed)
        except (OSError, EOFError, ValueError, zlib.error) as e:     # a damaged kept file is reported, never a crash
            print("BAD  %s: its kept file does not decompress (%s)" % (rel, type(e).__name__))
            continue
        ok = len(data) == int(length) and sha(data) == digest
        src = os.path.join(ROOT, rel)
        where = "the source is gone"
        if os.path.exists(src):
            with open(src, "rb") as f:
                same = f.read() == data
            ok = ok and same
            where = "the source stands, the same bytes" if same else "THE SOURCE DIFFERS"
        held += ok
        total += len(data)
        packed_total += len(packed)
        print("%-4s %s (%s bytes, sha256 %s…): %s" % ("ok" if ok else "BAD", rel, length, digest[:16], where))
    print("KEPT EVIDENCE %s: %d of %d files recovered exactly; %d bytes kept in %d" % (
        "HELD" if held == n and n else "FAILED", held, n, total, packed_total))
    return held == n and n > 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "make":
        make(sys.argv[2:])
    elif len(sys.argv) == 2 and sys.argv[1] == "check":
        sys.exit(0 if check() else 1)
    else:
        sys.exit("usage: kept_evidence.py check | make SOURCE...")

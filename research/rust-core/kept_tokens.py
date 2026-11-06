"""RUST-CORE-0 phase 0: evidence that holds a home path, kept in the tracked tree with each spelling of the path's prefix
replaced by a token, and restored byte for byte only with the exact prefixes given back (the owner's ruling on the
ruling sheet of 2026-10-31, section II, option (c)).

  python -B research/rust-core/kept_tokens.py make SOURCE... --prefix NAME=VALUE... --forbid TEXT...
  python -B research/rust-core/kept_tokens.py restore KEPT OUT --prefix NAME=VALUE...
  python -B research/rust-core/kept_tokens.py check [--prefix NAME=VALUE...]

His conditions, each kept here:
1. Every spelling of the prefix has a token of its own, the short 8.3 form included: a token is `⟦NAME⟧`, one NAME for
   each spelling given to `make` (for instance HOME_ESC for the JSON-escaped long form, HOME83 for the short form).
2. Restoration takes each spelling's exact prefix as an explicit input, `--prefix NAME=VALUE`. Nothing is derived from
   another input: the short form is never made from the long one, nor an escaped form from a plain one.
3. Replacement changes only the bytes of each matched prefix. `make` refuses a source that already holds a token's
   bytes, so a token can only ever stand for its prefix.
4. The restored file must have the original's length and sha256, which the manifest keeps; else nothing is written.
5. A missing input (a token with no prefix given), an ambiguous one (a NAME given twice) and an incorrect one (a wrong
   prefix, or a NAME the file does not hold) each refuse. `make` refuses a source in which two tokens would stand side
   by side, since two wrong prefixes could then trade bytes across the boundary and restore the same bytes; and
   `check` refuses a NAME that no kept file holds (REREAD-9's NB11, his ruling on ASK 9-5).
6. The plants are in `kept_tokens_plants.py`. Both `restore` and `check` read the kept file's sha256 before anything
   decompresses it, and report a damaged kept file rather than raise (REREAD-9's NB12).

`make` also refuses a source in which any `--forbid` text remains after every prefix is replaced, compared without
case: what is kept holds none of it. The prefixes and the forbidden texts are given on the command line and written
nowhere. The manifest, `kept/TOKENED.txt`, holds for each file its source path, the original's length and sha256, the
kept file's path and sha256, and how many times each token stands in it. The kept file is the tokened bytes compressed by
Python's gzip at level 9 with no timestamp. Nothing kept is ever written over. Off the gate."""
import gzip
import hashlib
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KEPT = os.path.join(HERE, "kept")
MANIFEST = os.path.join(KEPT, "TOKENED.txt")
HEAD = ("# evidence kept with its home-path prefixes tokened (SHEET.md Amendment 9): source path | length | sha256 | "
        "kept file | its sha256 | token counts\n")


class Refused(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def token(name):
    return ("⟦%s⟧" % name).encode("utf-8")


def parse_prefixes(pairs):
    """NAME=VALUE pairs to {NAME: bytes}. A NAME given twice is ambiguous and refused, whatever its values."""
    out = {}
    for p in pairs:
        if "=" not in p:
            raise Refused("a prefix is not NAME=VALUE: %r" % p.split("=")[0])
        name, value = p.split("=", 1)
        if not name or not name.replace("_", "").isalnum() or not value:
            raise Refused("a prefix's NAME or VALUE is empty or not plain: %r" % name)
        if name in out:
            raise Refused("the prefix %s is given twice" % name)
        out[name] = value.encode("utf-8")
    return out


def tokenize(data, prefixes, forbid):
    """The tokened bytes and each token's count. Longer prefixes are replaced first, so that no prefix is replaced inside
    another's match."""
    for name in prefixes:
        if token(name) in data:
            raise Refused("the source already holds the token of %s" % name)
    counts = {}
    for name, value in sorted(prefixes.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        counts[name] = data.count(value)
        data = data.replace(value, token(name))
    for a in counts:                            # NB11: no two tokens side by side
        for b in counts:
            if counts[a] and counts[b] and token(a) + token(b) in data:
                raise Refused("two tokens would stand side by side (%s, then %s)" % (a, b))
    low = data.lower()
    for f in forbid:
        if f.lower().encode("utf-8") in low:
            raise Refused("a forbidden text remains after every prefix is replaced")
    return data, counts


def restore_bytes(tokened, counts, prefixes):
    """The original bytes, from the tokened bytes and the prefixes given. Refuses a missing, extra or wrong input."""
    held = {n for n, c in counts.items() if c}
    if set(prefixes) - held:                    # a prefix for a token the file never holds is an incorrect input
        raise Refused("a prefix is given for a token the file does not hold: %s" % sorted(set(prefixes) - held))
    if held - set(prefixes):
        raise Refused("a token has no prefix given: %s" % sorted(held - set(prefixes)))
    for name, c in counts.items():
        if tokened.count(token(name)) != c:
            raise Refused("the kept file holds the token of %s other than %d times" % (name, c))
    for name in counts:
        if name in prefixes:
            tokened = tokened.replace(token(name), prefixes[name])
    return tokened


def rows(manifest=None):
    manifest = manifest or MANIFEST
    if not os.path.exists(manifest):
        return []
    out = []
    with open(manifest, encoding="utf-8") as f:
        for ln in f:
            if ln.strip() and not ln.startswith("#"):
                rel, length, digest, kept, kept_digest, cs = ln.rstrip("\n").split(" | ")
                counts = {k: int(v) for k, v in (x.split("=") for x in cs.split(","))} if cs != "-" else {}
                out.append((rel, int(length), digest, kept, kept_digest, counts))
    return out


def make(sources, prefixes, forbid, kept_dir=None):
    kept_dir = kept_dir or KEPT
    manifest = os.path.join(kept_dir, "TOKENED.txt")
    have = {r[0] for r in rows(manifest)}
    os.makedirs(kept_dir, exist_ok=True)
    if not os.path.exists(manifest):
        with open(manifest, "x", encoding="utf-8", newline="\n") as f:
            f.write(HEAD)
    for s in sources:
        rel = os.path.relpath(os.path.abspath(s), ROOT).replace(os.sep, "/")
        if rel.startswith(".."):            # outside the repository: named by its file name alone, never its path
            rel = os.path.basename(s)
        if rel in have:
            raise Refused("already kept; nothing is written over: %s" % rel)
        with open(s, "rb") as f:
            data = f.read()
        tokened, counts = tokenize(data, prefixes, forbid)
        if restore_bytes(tokened, counts, {n: v for n, v in prefixes.items() if counts[n]}) != data:
            raise Refused("the tokened bytes do not restore to the source")
        packed = gzip.compress(tokened, 9, mtime=0)
        name = rel + ".tok.gz"
        out = os.path.join(kept_dir, name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "xb") as f:
            f.write(packed)
        cs = ",".join("%s=%d" % (n, c) for n, c in sorted(counts.items())) or "-"
        with open(manifest, "a", encoding="utf-8", newline="\n") as f:
            f.write(" | ".join([rel, str(len(data)), sha(data), "kept/" + name, sha(packed), cs]) + "\n")
        have.add(rel)
        print("kept %s tokened: %d bytes, %d compressed; %s" % (rel, len(data), len(packed), cs))


def restore(kept_rel, out, prefixes, kept_dir=None):
    kept_dir = kept_dir or KEPT
    for rel, length, digest, kept, kept_digest, counts in rows(os.path.join(kept_dir, "TOKENED.txt")):
        if kept == kept_rel or rel == kept_rel:
            with open(os.path.join(kept_dir, kept[len("kept/"):]), "rb") as f:
                packed = f.read()
            if sha(packed) != kept_digest:
                raise Refused("the kept file is not the one the manifest names")
            try:
                tokened = gzip.decompress(packed)
            except (OSError, EOFError, ValueError, zlib.error) as e:
                raise Refused("the kept file does not decompress (%s)" % type(e).__name__)
            data = restore_bytes(tokened, counts, prefixes)
            if len(data) != length or sha(data) != digest:
                raise Refused("the restored bytes are not the original's (a wrong prefix?)")
            if out is not None:
                with open(out, "xb") as f:
                    f.write(data)
            return data
    raise Refused("no such kept file: %s" % kept_rel)


def check(prefixes, kept_dir=None):
    kept_dir = kept_dir or KEPT
    n = held = 0
    all_rows = rows(os.path.join(kept_dir, "TOKENED.txt"))
    unheld = sorted(set(prefixes) - {k for r in all_rows for k, c in r[5].items() if c})
    if unheld:                                  # NB11: a NAME no kept file holds is an incorrect input
        print("BAD  a prefix is given for a NAME no kept file holds: %s" % ", ".join(unheld))
    for rel, length, digest, kept, kept_digest, counts in all_rows:
        n += 1
        try:
            if prefixes:
                given = {k: v for k, v in prefixes.items() if counts.get(k)}
                restore(kept, None, given, kept_dir)
                what = "restored exactly (length and sha256 the original's)"
            else:
                with open(os.path.join(kept_dir, kept[len("kept/"):]), "rb") as f:
                    packed = f.read()
                if sha(packed) != kept_digest:  # NB12: the kept file's sha256 before anything decompresses it
                    raise Refused("the kept file is not the one the manifest names")
                try:
                    tokened = gzip.decompress(packed)
                except (OSError, EOFError, ValueError, zlib.error) as e:
                    raise Refused("the kept file does not decompress (%s)" % type(e).__name__)
                if any(tokened.count(token(k)) != c for k, c in counts.items()):
                    raise Refused("the kept file is not the one the manifest names")
                what = "intact; the original is checked only with its prefixes given"
            held += 1
            print("ok   %s: %s" % (rel, what))
        except Refused as e:
            print("BAD  %s: %s" % (rel, e))
    good = held == n and n > 0 and not unheld
    print("TOKENED EVIDENCE %s: %d of %d %s" % ("HELD" if good else "FAILED", held, n,
                                                "restored exactly" if prefixes else "intact (originals not checked)"))
    return good


def main(argv):
    def opts(flag):
        return [argv[i + 1] for i in range(len(argv) - 1) if argv[i] == flag]

    plain = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or not argv[i - 1].startswith("--"))]
    try:
        prefixes = parse_prefixes(opts("--prefix"))
        if plain and plain[0] == "make":
            if not prefixes:
                raise Refused("make needs at least one prefix")
            make(plain[1:], prefixes, opts("--forbid"))
        elif plain and plain[0] == "restore" and len(plain) == 3:
            restore(plain[1], plain[2], prefixes)
            print("restored %s exactly" % plain[1])
        elif plain and plain[0] == "check":
            return 0 if check(prefixes) else 1
        else:
            print("usage: kept_tokens.py make SOURCE... --prefix NAME=VALUE... --forbid TEXT... | restore KEPT OUT "
                  "--prefix NAME=VALUE... | check [--prefix NAME=VALUE...]")
            return 2
    except Refused as e:
        print("KEPT-TOKENS REFUSED: %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

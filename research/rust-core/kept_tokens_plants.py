"""RUST-CORE-0 phase 0: do kept_tokens.py's guarantees hold? His ruling (the ruling sheet, 2026-10-31, section II):
"Plants must cover every spelling, partial matches, multiple occurrences, and incorrect restoration inputs." And: "No
use of option (c) until those tests pass."

  python -B research/rust-core/kept_tokens_plants.py SCRATCH [REAL SOURCES... --prefix NAME=VALUE... --forbid TEXT...]

It works in SCRATCH only, never in the repository's kept folder. On made-up files (an account called `someone`, its
short form `SOMEON~1`, in seven spellings, the real files' REL83 and SLUG shapes among them) it plants every case below
and requires the stated outcome. Given real sources and their prefixes, it also keeps each in SCRATCH, restores it, and
requires the original's sha256, and plants a missing, a shorter and a same-length wrong prefix for every token each
holds. The account and its prefixes are given on the command line and written nowhere.

Since REREAD-9 (his ruling on ASK 9-5): each spelling has a wrong prefix of the same length, which only the sha256
comparison can refuse; REL83 and SLUG have near misses and repeats; two tokens side by side are refused by `make`; a
NAME no kept file holds is refused by `check`; and a damaged kept file, of the kinds that make gzip raise `zlib.error`
or `BadGzipFile`, is reported by `check` and `restore`, never raised."""
import contextlib
import gzip
import io
import os
import shutil
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kept_tokens as kt  # noqa: E402

BS = chr(92)
ESC = BS + BS
SPELLINGS = {                                   # the made-up account's seven spellings, as bytes
    "HOME_ESC": ("C:" + ESC + "Users" + ESC + "someone").encode(),
    "HOME": ("C:" + BS + "Users" + BS + "someone").encode(),
    "HOME_FWD": b"C:/Users/someone",
    "HOME83_ESC": ("C:" + ESC + "Users" + ESC + "SOMEON~1").encode(),
    "HOME83": ("C:" + BS + "Users" + BS + "SOMEON~1").encode(),
    "REL83": b"../../../SOMEON~1",              # the real files' REL83 shape
    "SLUG": b"C--Users-someone",                # the real files' SLUG shape
}
FORBID = ["someone", "SOMEON~1"]
results = []


def row(name, ok, detail=""):
    results.append(ok)
    print("%-6s %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))


def refused(fn):
    try:
        fn()
        return False, "not refused"
    except kt.Refused as e:
        return True, str(e)[:90]


NEAR = [b"C:" + BS.encode() + b"Users" + BS.encode() + b"someon", b"C:Users/someon", b"Users" + ESC.encode() + b"x",
        b"../../../SOMEON", b"../../SOMEON", b"C--Users-someon", b"C--User-someon"]


def fixture():
    """Every spelling, three times each, each repeat one byte from the last (two tokens side by side are refused), at
    the start and at the end, inside longer paths, and beside near misses that are not the prefix (a shorter name, a
    missing separator, one level fewer), REL83's and SLUG's among them."""
    parts = [SPELLINGS["HOME_ESC"]]             # at the start
    for name, v in SPELLINGS.items():
        parts += [b" ", v, b" ", v, b"|", v + ESC.encode() + b"Desktop" + ESC.encode() + b"Orlog", b" "]
    parts += [b" ".join(NEAR), b"\n{\"path\": \"" + SPELLINGS["HOME_ESC"] + ESC.encode() + b"AppData\"}\n",
              SPELLINGS["HOME83"]]
    return b"".join(parts)


def same_length_wrong(value):
    """The prefix with its last character changed and its length kept, so that only the sha256 can refuse it."""
    return value[:-1] + bytes([value[-1] ^ 1])


def damaged_at(packed, kind):
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


def quiet(fn):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn()


def main(argv):
    scr = argv[0]
    real = [a for i, a in enumerate(argv[1:], 1) if not a.startswith("--") and not argv[i - 1].startswith("--")]
    flags = argv[1:]
    real_prefixes = kt.parse_prefixes([flags[i + 1] for i in range(len(flags) - 1) if flags[i] == "--prefix"])
    real_forbid = [flags[i + 1] for i in range(len(flags) - 1) if flags[i] == "--forbid"]
    base = os.path.join(scr, "kept-tokens-plants")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    src = os.path.join(base, "fixture.txt")
    data = fixture()
    open(src, "wb").write(data)
    kd = os.path.join(base, "kept")
    prefixes = {n: v for n, v in SPELLINGS.items()}

    # 1. every spelling, multiple occurrences, partial matches: kept, and restored byte for byte
    kt.make([src], prefixes, FORBID, kd)
    (rel, length, digest, kept, kept_digest, counts), = kt.rows(os.path.join(kd, "TOKENED.txt"))
    row("every spelling tokened, each several times", all(counts[n] >= 3 for n in SPELLINGS),
        ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
    packed = open(os.path.join(kd, kept[len("kept/"):]), "rb").read()
    tokened = gzip.decompress(packed)
    row("no forbidden text left in what is kept", not any(f.lower().encode() in tokened.lower() for f in FORBID))
    row("the near misses kept as they were, REL83's and SLUG's among them", all(m in tokened for m in NEAR))
    back = kt.restore(kept, None, prefixes, kd)
    row("restored byte for byte, the original's sha256", back == data and kt.sha(back) == digest)

    # 2-6. incorrect restoration inputs, each refused
    for name in SPELLINGS:
        ok, why = refused(lambda: kt.restore(kept, None, {k: v for k, v in prefixes.items() if k != name}, kd))
        row("missing prefix %s refused" % name, ok, why)
        ok, why = refused(lambda: kt.restore(kept, None, dict(prefixes, **{name: prefixes[name] + b"x"}), kd))
        row("wrong prefix %s refused" % name, ok, why)
        # NB10: a wrong prefix of the same length passes every count and length test; only the sha256 refuses it
        wrong = same_length_wrong(prefixes[name])
        ok, why = refused(lambda: kt.restore(kept, None, dict(prefixes, **{name: wrong}), kd))
        row("same-length wrong prefix %s refused by the sha256 alone" % name, ok and "not the original's" in why, why)
    ok, why = refused(lambda: kt.parse_prefixes(["HOME=a", "HOME=b"]))
    row("a prefix given twice (ambiguous) refused", ok, why)
    ok, why = refused(lambda: kt.parse_prefixes(["HOME=a", "HOME=a"]))
    row("a prefix given twice with one value refused too", ok, why)
    ok, why = refused(lambda: kt.restore(kept, None, dict(prefixes, OTHER=b"C:/x"), kd))
    row("a prefix the file does not hold refused", ok, why)
    ok, why = refused(lambda: kt.restore(kept, None, dict(prefixes, HOME83=prefixes["HOME"]), kd))
    row("the short form made from the long one refused", ok, why)
    ok, why = refused(lambda: kt.restore(kept, None, dict(prefixes, HOME_ESC=prefixes["HOME"]), kd))
    row("the escaped form made from the plain one refused", ok, why)

    # 7. a source that already holds a token's bytes
    s2 = os.path.join(base, "holds-a-token.txt")
    open(s2, "wb").write(data + kt.token("HOME"))
    ok, why = refused(lambda: kt.make([s2], prefixes, FORBID, os.path.join(base, "k7")))
    row("a source holding a token refused", ok, why)

    # 8. a spelling not given (another case) leaves the account's name: refused
    s3 = os.path.join(base, "other-case.txt")
    open(s3, "wb").write(data + b" c:/users/SomeOne/x")
    ok, why = refused(lambda: kt.make([s3], prefixes, FORBID, os.path.join(base, "k8")))
    row("a spelling not given (other case) refused", ok, why)

    # 9. the kept file damaged, or not the one the manifest names
    k9 = os.path.join(base, "k9")
    shutil.copytree(kd, k9)
    p9 = os.path.join(k9, kept[len("kept/"):])
    b9 = bytearray(open(p9, "rb").read())
    b9[len(b9) // 2] ^= 1
    open(p9, "wb").write(bytes(b9))
    ok, why = refused(lambda: kt.restore(kept, None, prefixes, k9))
    row("a damaged kept file refused", ok, why)

    # 9b. NB12: damage of the kinds that made gzip raise, reported by check and restore, never raised
    for kind_name, kind in (("zlib.error", zlib.error), ("BadGzipFile", gzip.BadGzipFile)):
        i = damaged_at(packed, kind)
        if i is None:
            row("damage that makes gzip raise %s: no position found" % kind_name, False)
            continue
        kd2 = os.path.join(base, "k9-%s" % kind_name.replace(".", "-"))
        shutil.copytree(kd, kd2)
        p2 = os.path.join(kd2, kept[len("kept/"):])
        b2 = bytearray(open(p2, "rb").read())
        b2[i] ^= 1
        open(p2, "wb").write(bytes(b2))
        try:
            held = quiet(lambda: kt.check({}, kd2))
            row("damage that makes gzip raise %s (byte %d): check reports it" % (kind_name, i), held is False)
        except Exception as e:
            row("damage that makes gzip raise %s (byte %d): check reports it" % (kind_name, i), False,
                "raised %s" % type(e).__name__)
        ok, why = refused(lambda: kt.restore(kept, None, prefixes, kd2))
        row("damage that makes gzip raise %s: restore refuses it" % kind_name, ok, why)

    # 10. nothing kept is written over
    ok, why = refused(lambda: kt.make([src], prefixes, FORBID, kd))
    row("keeping the same source again refused", ok, why)

    # 10b. NB11: two tokens side by side are refused by make, whether two spellings or one spelling twice
    s4 = os.path.join(base, "side-by-side.txt")
    open(s4, "wb").write(b"before " + SPELLINGS["HOME_FWD"] + SPELLINGS["HOME"] + b" after")
    ok, why = refused(lambda: kt.make([s4], prefixes, FORBID, os.path.join(base, "k10b")))
    row("two spellings side by side refused", ok and "side by side" in why, why)
    s5 = os.path.join(base, "twice-side-by-side.txt")
    open(s5, "wb").write(b"before " + SPELLINGS["REL83"] + SPELLINGS["REL83"] + b" after")
    ok, why = refused(lambda: kt.make([s5], prefixes, FORBID, os.path.join(base, "k10c")))
    row("one spelling twice side by side refused", ok and "side by side" in why, why)

    # 10c. NB11: check refuses a NAME no kept file holds
    held = quiet(lambda: kt.check(dict(prefixes, BOGUS=b"C:/bogus"), kd))
    row("check given a NAME no kept file holds fails", held is False)
    held = quiet(lambda: kt.check(prefixes, kd))
    row("check given exactly the held NAMEs holds", held is True)

    # 11. the real sources, if given
    if real:
        kr = os.path.join(base, "real")
        kt.make(real, real_prefixes, real_forbid, kr)
        for rel, length, digest, kept, kept_digest, counts in kt.rows(os.path.join(kr, "TOKENED.txt")):
            held = {k: v for k, v in real_prefixes.items() if counts.get(k)}
            back = kt.restore(kept, None, held, kr)
            with open(os.path.join(kt.ROOT, rel), "rb") as f:
                orig = f.read()
            row("real %s restored byte for byte" % rel, back == orig and kt.sha(back) == digest,
                ", ".join("%s=%d" % kv for kv in sorted(counts.items()) if kv[1]))
            for name in held:
                ok1, _ = refused(lambda: kt.restore(kept, None, {k: v for k, v in held.items() if k != name}, kr))
                ok2, _ = refused(lambda: kt.restore(kept, None, dict(held, **{name: held[name][:-1]}), kr))
                ok3, why3 = refused(lambda: kt.restore(kept, None, dict(held, **{name: same_length_wrong(held[name])}),
                                                       kr))
                row("real %s: missing, shorter and same-length wrong %s refused" % (os.path.basename(rel), name),
                    ok1 and ok2 and ok3 and "not the original's" in why3)
    print("KEPT-TOKENS PLANTS: %d of %d as stated" % (sum(results), len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

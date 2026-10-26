"""ORLOG SELFTEST: every self-claim gets a row; every guard gets a plant that must bite.

A row prints [PASS] or [FAIL]. A plant row names the planted defect and the witness that caught
it: the exact refusal, clause or divergent event the defect caused, not merely "something failed"
(the owner's kill-witness ruling: a catch needs a defect-specific causal witness). A plant that
changes nothing is reported EQUIVALENT and asserted to stay so (an honest miss, never counted caught).

  python tests/selftest.py [--backends python,c99,rust]
"""
import argparse
import contextlib
import json
import os
import random
import re
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from orlog import canon as CANON  # noqa: E402
from orlog import court as COURT  # noqa: E402
from orlog import numeric_ref as N  # noqa: E402
from orlog import seal as SEAL  # noqa: E402
from orlog import sema as SEMA  # noqa: E402
from orlog import arbiter as ARB  # noqa: E402
from orlog.arbiter import Arbiter, C_FLAGS, witness_artifact, parse_receipt, receipt_core  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402
from plants import planted  # noqa: E402  (tests/plants.py: a module copied with exact edits, in memory)

ROWS = []


def row(ok, name, detail=""):
    ROWS.append((bool(ok), name))
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" -- " + detail) if detail else ""))


def plant(name, caught, witness, equivalent=False):
    if equivalent:
        ROWS.append((not caught, "plant %s (declared equivalent)" % name))
        print("[%s] plant %s: EQUIVALENT, as declared%s" % ("PASS" if not caught else "FAIL", name,
                                                         (" -- " + witness) if witness else ""))
        return
    ROWS.append((caught, "plant %s" % name))
    print("[%s] plant %s: %s -- %s" % ("PASS" if caught else "FAIL", name, "CAUGHT" if caught else "SURVIVED",
                                      witness))


def read(p):
    with open(os.path.join(ROOT, p), "rb") as fh:
        return fh.read()


def prog(*lines):
    return ("\n".join(lines) + "\n").encode("utf-8")


# ------------------------------------------------------------------ the door
def door_rows():
    cases = [
        ("clean", b"\xc2\xa71 Let n be 27.\n", [], None),
        ("CRLF + BOM + curly delimiters repaired, inner apostrophe kept",
         b"\xef\xbb\xbf\xc2\xa71 Say \xe2\x80\x9cit\xe2\x80\x99s\xe2\x80\x9d.\r\n",
         ["R-BOM", "R-CRLF", "R-QUOTE-DELIM", "R-QUOTE-DELIM"], "§1 Say \"it’s\".\n"),
        ("NBSP in code repaired", b"\xc2\xa71 Let\xc2\xa0n be 27.\n", ["R-SPACE"], None),
        ("bidi override refused", b"\xc2\xa71 Say 1. \xe2\x80\xae\n", ["BIDI-CONTROL"], None),
        ("Cyrillic letter in code refused", b"\xc2\xa71 Let \xd0\xb0 be 1.\n", ["NON-ASCII-CODE"], None),
        ("joiner inside a literal noted, kept", b"\xc2\xa71 Say \"a\xe2\x80\x8db\".\n", ["JOINER-IN-LITERAL"], None),
        ("non-NFC literal noted, kept byte for byte", b"\xc2\xa71 Say \"e\xcc\x81\".\n", ["LITERAL-NOT-NFC"], None),
        ("non-NFC free text repaired to NFC", b"Note: cafe\xcc\x81\n\xc2\xa71 Say 1.\n", ["R-NFC"], None),
        ("times and minus signs repaired", b"\xc2\xa71 Let n be 3 \xc3\x97 \xe2\x88\x921.\n", ["R-TIMES", "R-MINUS"],
         None),
        ("em dash refused as ambiguous", b"\xc2\xa71 Let n be 3 \xe2\x80\x94 1.\n", ["DASH-AMBIGUOUS"], None),
        ("cp1252 bytes refused, never guessed", b"\xc2\xa71 Say \x93hi\x94.\n", ["BYTES-NOT-UTF8"], None),
        ("unterminated literal refused", b"\xc2\xa71 Say \"abc.\n", ["UNTERMINATED-TEXT"], None),
    ]
    for name, raw, rules, want_text in cases:
        c = CANON.canonicalize(raw)
        got = [e["rule"] for e in c.events if e["rule"] != "R-TRAILING-SPACE"]
        ok = got == rules and (want_text is None or c.text == want_text)
        row(ok, "door: " + name, "" if ok else "got %s" % got)
    # idempotence where it can fail: on texts the door had to repair (court finding L13: the corpus needed none)
    repaired_inputs = [raw for _, raw, rules, _ in cases if any(r.startswith("R-") for r in rules)]
    words = read("examples/spellings/words.orl")
    repaired_inputs.append(b"\xef\xbb\xbf" + words.replace(b"\n", b"\r\n").replace(b"times", b"\xc3\x97"))
    bad, n_rep = [], 0
    for raw in repaired_inputs:
        c = CANON.canonicalize(raw)
        if c.text is None:
            continue
        n_rep += len(c.repairs)
        c2 = CANON.canonicalize(c.text.encode("utf-8"))
        if c2.text != c.text or c2.repairs:
            bad.append(raw[:30])
    row(not bad and n_rep > 0, "door: on %d texts that needed %d repairs, a second pass changes nothing (idempotent "
        "where it could fail; retraction in general is DECLARED)" % (len(repaired_inputs), n_rep), str(bad))
    # court finding L12: a repair may never move a literal's boundary. Since E9 the literal must open with a curly
    # quote: inside a straight-opened literal a curly quote is text, and the case cannot arise (SPEC §12, §13).
    boundary = "§1 Say “a”\"b\".\n".encode("utf-8")
    c = CANON.canonicalize(boundary)
    c2 = CANON.canonicalize("§1 Say “a”“b”.\n".encode("utf-8"))
    row(all(x.text is None and any(e["rule"] == "QUOTE-BOUNDARY" for e in x.events) for x in (c, c2)),
        "door: a curly-opened literal whose closer, repaired, would join the next quote into one literal is refused "
        "QUOTE-BOUNDARY, for a straight and a curly next quote (court L12)")
    CANON.QUOTE_BOUNDARY_CHECK = False
    try:
        c = CANON.canonicalize(boundary)
        caught = c.text is not None
    finally:
        CANON.QUOTE_BOUNDARY_CHECK = True
    plant("door-moves-literal-boundary", caught, "under the plant the door accepts it and the program prints a\"b, "
          "so the QUOTE-BOUNDARY row fails")
    # the plant: a door that forgets bidi controls
    saved = CANON.BIDI
    CANON.BIDI = set()
    try:
        c = CANON.canonicalize(b"\xc2\xa71 Say 1. \xe2\x80\xae\n")
        caught_by_row = not any(e["rule"] == "BIDI-CONTROL" for e in c.events)
    finally:
        CANON.BIDI = saved
    plant("door-forgets-bidi", caught_by_row,
          "the bidi row's expected BIDI-CONTROL refusal is absent under the plant")


def corpus():
    out = []
    for d in ("examples", os.path.join("examples", "spellings")):
        for fn in sorted(os.listdir(os.path.join(ROOT, d))):
            if fn.endswith(".orl"):
                out.append(os.path.join(d, fn))
    return out


# ------------------------------------------------------------------ seals and line checks
def seal_rows():
    row(SEAL.damm_property_exhaustive(), "line check: x o y = 2x + y over GF(2^8) is totally anti-symmetric "
        "(65,536 pairs at 4 values of c)")
    line = "§4.1 If n is even, set n to n divided by 2; otherwise set n to 3 times n plus 1."
    base = line.encode("utf-8")
    ref = SEAL.fold(base)
    subs = trans = missed = 0
    for i in range(len(base)):
        for v in range(0x20, 0x7F):
            if v != base[i]:
                b = bytearray(base)
                b[i] = v
                subs += 1
                missed += SEAL.fold(bytes(b)) == ref
        if i + 1 < len(base) and base[i] != base[i + 1]:
            b = bytearray(base)
            b[i], b[i + 1] = b[i + 1], b[i]
            trans += 1
            missed += SEAL.fold(bytes(b)) == ref
    row(missed == 0, "line check: every single-byte substitution (%d) and adjacent transposition (%d) of a clause "
        "line changes its syllable" % (subs, trans), "missed %d" % missed)
    stamped = SEAL.stamp(read("examples/collatz.orl").decode("utf-8"))
    c = compile_bytes(stamped.encode("utf-8"))
    n_clauses = len(compile_bytes(read("examples/collatz.orl")).prog.clauses)   # derived, never typed (Urdr L16)
    row(c.ok and c.prog.line_checks == n_clauses,
        "line check: a stamped program compiles and verifies every clause stamp (%d of %d)"
        % (c.prog.line_checks if c.ok else -1, n_clauses))
    tampered = stamped.replace("set n to n divided by 2", "set n to n divided by 3", 1)
    c = compile_bytes(tampered.encode("utf-8"))
    row(not c.ok and c.error.code == "LINE-CHECK", "line check: one changed digit is refused LINE-CHECK")
    saved = SEAL.line_check
    SEAL.line_check = lambda s: "bal"
    import orlog.syntax as SYN
    saved_syn = SYN.line_check
    SYN.line_check = SEAL.line_check
    try:
        restamped = "\n".join(l if not l.endswith("]") else l[:-5] + "[bal]" for l in tampered.split("\n"))
        c = compile_bytes(restamped.encode("utf-8"))
        caught = c.ok
    finally:
        SEAL.line_check = saved
        SYN.line_check = saved_syn
    plant("line-check-constant", caught, "under the plant the tampered line compiles; the LINE-CHECK row would fail")
    words = read("examples/spellings/words.orl")
    cw = compile_bytes(words)
    sealed = words + ("Sealed: %s.\n" % cw.seal_words).encode("ascii")
    row(compile_bytes(sealed).ok, "seal: a program sealed with its own law-seal compiles")
    edited = sealed.replace(b"3 times n plus 1", b"3 times n plus 3")
    c = compile_bytes(edited)
    row(not c.ok and c.error.code == "SEAL-MISMATCH", "seal: changing the law after sealing is refused SEAL-MISMATCH")
    noted = sealed.replace(b"Title: One Law", b"Note: a note changes the text, not the law.\nTitle: One Law")
    noted = sealed.replace(b"\xc2\xa71 Let", b"Note: a note changes the text, not the law.\n\xc2\xa71 Let", 1)
    c = compile_bytes(noted)
    row(c.ok and c.text_seal != compile_bytes(sealed).text_seal,
        "seal: adding a note changes the text-seal and keeps the law-seal (the seal still verifies)")


# ------------------------------------------------------------------ spellings
def spelling_rows():
    seals = {p: compile_bytes(read(p)).law_seal for p in ("examples/spellings/words.orl",
                                                          "examples/spellings/symbols.orl",
                                                          "examples/spellings/phrases.orl")}
    texts = {p: compile_bytes(read(p)).text_seal for p in seals}
    row(len(set(seals.values())) == 1 and len(set(texts.values())) == 3,
        "spellings: three spellings (words, symbols, phrases), three text-seals, one law-seal")
    noisy = read("examples/spellings/words.orl").replace(b"\n", b"\r\n").replace(b"times", b"\xc3\x97")
    noisy = b"\xef\xbb\xbf" + noisy.replace(b"\"even: \"", b"\xe2\x80\x9ceven: \xe2\x80\x9d")
    noisy = noisy.replace(b"Let m be", b"Let\xc2\xa0m be")
    c = compile_bytes(noisy)
    rules = sorted(set(e["rule"] for e in c.canon.events))
    row(c.ok and c.law_seal == seals["examples/spellings/words.orl"] and c.raw_seal != compile_bytes(
        read("examples/spellings/words.orl")).raw_seal,
        "spellings: a byte-mangled copy (BOM, CRLF, curly quotes, NBSP, U+00D7) is repaired to the same law-seal, "
        "each repair noted", ",".join(rules))


# ------------------------------------------------------------------ compile-time refusals
COMPILE_REFUSALS = [
    ("UNDECLARED", prog("§1 Say x.")),
    ("TYPE", prog("§1 Let a be 1.", "§2 Let b be a plus \"x\".")),
    ("NUMBERING", prog("§1 Let a be 1.", "§3 Say a.")),
    ("REDECLARED", prog("§1 Let a be 1.", "§2 Let a be 2.")),
    ("PRIORITY-CYCLE", prog("§1 Notwithstanding §2, define r as 1.",
                            "§2 Notwithstanding §1, define r as 2.", "§3 Say r.")),
    ("PERFORM-BEFORE-DEFINITION", prog("§1 To loop forever, do the following.", "§1.1 Loop forever.")),
    ("DECIMALS-PLACE", prog("§1 Let a be 1.5.", "§2 Decimals are floats.")),
    ("RULE-BEFORE-DEFINITION", prog("§1 Say r.", "§2 Define r as 1.")),
    ("EMPTY-BLOCK", prog("§1 While true, at most 3 times, do the following.")),
    ("LOOP-VARIABLE", prog("§1 For each i from 1 to 3, do the following.", "§1.1 Set i to 5.")),
    ("ORPHAN-OTHERWISE", prog("§1 Let a be 1.", "§2 Otherwise, say a.")),
    ("CERTIFICATE-TARGET", prog("§1 Let a be 1.", "§2 We claim that a equals 1, by the certificate of §3.",
                                "§3 Say a.")),
    # found through the clean-room twin's notes (38, 7, 21): each crashed or was accepted before
    ("LITERAL-RANGE", prog("§1 Decimals are floats.", "§2 Let x be 1" + "0" * 400 + ".0.")),
    ("LINE-FORM", prog("§1  Let x be 1.")),
    ("PROCEDURE-NAME", prog("§1 To do the following, do the following.", "§1.1 Say 1.")),
]


def compile_refusal_rows():
    for code, raw in COMPILE_REFUSALS:
        c = compile_bytes(raw)
        row(not c.ok and c.error.code == code, "compile refusal %s" % code,
            "" if (not c.ok and c.error.code == code) else str(c.error))
    # recursion through a second procedure is also refused: a procedure may perform only earlier ones
    c = compile_bytes(prog("§1 To ping, do the following.", "§1.1 Pong.",
                           "§2 To pong, do the following.", "§2.1 Ping."))
    row(not c.ok, "compile refusal: mutual recursion between procedures (UNKNOWN-PROCEDURE or PERFORM-BEFORE-DEFINITION)",
        "" if not c.ok else "compiled")


# ------------------------------------------------------------------ runtime refusals, identical across backends
RUNTIME_REFUSALS = [
    ("OVERFLOW", prog("§1 Let a be 9223372036854775807.", "§2 Set a to a plus 1.")),
    ("DIVISION-BY-ZERO", prog("§1 Let a be 0.", "§2 Say 7 divided by a.")),
    ("INEXACT-DIVISION", prog("§1 Say 7 divided by 2.")),
    ("FUEL-EXHAUSTED", prog("§1 Let a be 0.", "§2 While true, at most 5 times, do the following.",
                            "§2.1 Increase a by 1.")),
    ("RULE-CONFLICT", prog("§1 Let a be true.", "§2 Define r as 1, provided that a.",
                           "§3 Define r as 2, provided that a.", "§4 Say r.")),
    ("RULE-UNDEFINED", prog("§1 Let a be false.", "§2 Define r as 1, provided that a.", "§3 Say r.")),
    ("INDEX-OUT-OF-RANGE", prog("§1 Let xs be the list 1, 2 and 3.", "§2 Say item 4 of xs.")),
    ("EMPTY-LIST", prog("§1 Let xs be a list of 0 copies of 1.", "§2 Remove the last item of xs.")),
    ("CLAIM-REFUTED", prog("§1 Let a be 2.", "§2 We claim that a equals 3.")),
    ("MUST-FAILED", prog("§1 Let a be 2.", "§2 It must hold that a is odd.")),
    ("INEXACT-CONVERSION", prog("§1 Let x be 2.5.", "§2 Say x as an integer.")),
    ("NOT-FINITE", prog("§1 Decimals are floats.", "§2 Let z be 0.0.", "§3 Say (1.0 / z) as an integer.")),
    ("NEGATIVE-SQRT", prog("§1 Let a be -4.", "§2 Say the square root of a.")),
]


def runtime_refusal_rows(arb):
    for code, raw in RUNTIME_REFUSALS:
        comp, w, ref = arb.arbitrate(raw, "refuse-" + code.lower())
        st = w.get("reference", {}).get("status", "")
        # every backend that ran agreeing, not merely none dissenting: a backend that did not build is neither (the
        # reporting pass's finding 8)
        ok = comp.ok and st.startswith("REFUSED %s " % code) and len(w["agreeing"]) == len(arb.backends)
        row(ok, "runtime refusal %s: the reference and [%s] stop at the same event with the same code"
            % (code, ",".join(w.get("agreeing", []))), "" if ok else json.dumps(w.get("mismatch_notes"))[:400])


# ------------------------------------------------------------------ the corpus across backends
def corpus_rows(arb):
    for p in corpus():
        name = os.path.splitext(os.path.basename(p))[0]
        comp, w, ref = arb.arbitrate(read(p), name)
        ok = comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(arb.backends)
        row(ok, "corpus %s: reference and [%s] byte-identical (outputs and receipts)" % (name, ",".join(w["agreeing"])),
            "" if ok else json.dumps(w.get("mismatch_notes"))[:600])
    return True


# ------------------------------------------------------------------ backend plants (each with its causal witness)
def mutate_with(backend_name, fn):
    def m(b, src):
        return fn(src) if b == backend_name else src
    return m


C_PLANT_REM = ("static int64_t orlp_rem(int64_t a, int64_t b, uint32_t c) {"
               " if (b == 0) orl_refuse(\"DIVISION-BY-ZERO\", c); if (b == -1) return 0; return a % b; }\n")


def backend_plants(workdir, backends):
    fixture = prog("§1 Let a be -7.", "§2 Let b be 3.", "§3 Say the remainder of a by b.",
                   "§4 Say the quotient of a by -2.")
    if "c99" in backends:
        def c_rem(src):
            # call sites only ("= orl_i_rem("): renaming the runtime's own definition broke the build in the first
            # draft of this plant, and a build failure is not the defect's witness
            src = src.replace("= orl_i_rem(", "= orlp_rem(")
            return src.replace("static double orl_cf(", C_PLANT_REM + "static double orl_cf(", 1)
        arb = Arbiter(workdir, backends=("c99",), mutate=mutate_with("c99", c_rem))
        comp, w, ref = arb.arbitrate(fixture, "plant-c-rem")
        n = (w["mismatch_notes"] or [{}])[0]
        caught = w["dissenting"] == ["c99"] and n.get("clause") == "§3" and n.get("event_kind") == "S"
        plant("c99-remainder-truncates", caught, "first divergent event %s, a Say at %s: reference %s, backend %s" % (
            n.get("first_divergent_event"), n.get("clause"), n.get("reference_payload"), n.get("backend_payload")))

        eq = Arbiter(workdir, backends=("c99",), mutate=mutate_with(
            "c99", lambda s: s.replace("= orl_i_max(", "= ORLP_MAX(").replace(
                "static double orl_cf(", "#define ORLP_MAX(a, b) ((a) > (b) ? (a) : (b))\nstatic double orl_cf(", 1)))
        comp, w, ref = eq.arbitrate(read("examples/collatz.orl"), "plant-c-max-equivalent")
        plant("c99-max-rewritten-as-macro", bool(w["dissenting"]), "same rule (a > b ? a : b), so no witness exists",
              equivalent=True)

        fma_rows(workdir)

        def explicit_fma(src):
            # fuse every "tA = orl_f_mul(P, Q); ... tB = orl_f_sub(tA, R);" into one fma(P, Q, -R)
            import re
            muls = dict((m.group(1), (m.group(2), m.group(3)))
                        for m in re.finditer(r"(t\d+) = orl_f_mul\((t\d+), (t\d+)\);", src))

            def sub(m):
                if m.group(2) in muls:
                    p, q = muls[m.group(2)]
                    return "%s = orl_f_canon(fma(%s, %s, -%s));" % (m.group(1), p, q, m.group(3))
                return m.group(0)
            return re.sub(r"(t\d+) = orl_f_sub\((t\d+), (t\d+)\);", sub, src)
        arb = Arbiter(workdir, backends=("c99",), mutate=mutate_with("c99", explicit_fma))
        comp, w, ref = arb.arbitrate(read("examples/chaos.orl"), "plant-c-explicit-fma")
        n = (w["mismatch_notes"] or [{}])[0]
        caught = w["dissenting"] == ["c99"] and n.get("event_kind") == "A" and n.get("clause") == "§3.1"
        plant("c99-explicit-fma (x*x-2 fused by fma())", caught,
              "first divergent event %s, an assignment at %s: the fused and the twice-rounded x part there" % (
                  n.get("first_divergent_event"), n.get("clause")))

    if "python" in backends:
        def py_quot(src):
            src = src.replace("rt.i_quot(", "_plant_floor_quot(rt, ")
            return src.replace("LAW_SEAL = ", "def _plant_floor_quot(rt, a, b, c):\n    return a // b\n\nLAW_SEAL = ",
                               1)
        arb = Arbiter(workdir, backends=("python",), mutate=mutate_with("python", py_quot))
        comp, w, ref = arb.arbitrate(fixture, "plant-py-quot")
        n = (w["mismatch_notes"] or [{}])[0]
        caught = w["dissenting"] == ["python"] and n.get("clause") == "§4"
        plant("python-quotient-floors", caught, "first divergent event %s, a Say at %s: reference %s, backend %s" % (
            n.get("first_divergent_event"), n.get("clause"), n.get("reference_payload"), n.get("backend_payload")))

    if "rust" in backends:
        def rs_xmul(src):
            src = src.replace("rt.x_mul(", "plant_xmul_trunc(rt, ")
            return src.replace("struct St {", "fn plant_xmul_trunc(rt: &mut Rt, a: i64, b: i64, c: u32) -> i64 {"
                               " ((a as i128 * b as i128) >> 32) as i64 }\nstruct St {", 1)
        arb = Arbiter(workdir, backends=("rust",), mutate=mutate_with("rust", rs_xmul))
        comp, w, ref = arb.arbitrate(read("examples/leapfrog.orl"), "plant-rs-xmul")
        n = (w["mismatch_notes"] or [{}])[0]
        caught = w["dissenting"] == ["rust"] and n.get("first_divergent_event") is not None
        plant("rust-fixed-multiply-floors", caught, "first divergent event %s (%s at %s)" % (
            n.get("first_divergent_event"), n.get("event_kind"), n.get("clause")))


def fma_rows(workdir):
    """Two measurements on this host: contraction is real for naive C, and absent from Orlog's generated C."""
    import subprocess
    probe = os.path.join(workdir, "fma_probe.c")
    with open(probe, "wb") as fh:
        fh.write(b"#include <stdio.h>\nint main(void){ volatile double x = 0.1234567; double y;"
                 b" for (int i = 0; i < 3000; i++) { double t = x * x; y = t - 2.0; x = y; }"
                 b" printf(\"%.17g\\n\", x); return 0; }\n")
    outs = {}
    for mode, flags in (("fast", ["-ffp-contract=fast", "-march=native"]), ("off", ["-ffp-contract=off"])):
        exe = os.path.join(workdir, "fma_probe_%s.exe" % mode)
        subprocess.run(["clang", "-O2"] + flags + [probe, "-o", exe], capture_output=True)
        r = subprocess.run([exe], capture_output=True, text=True)
        outs[mode] = r.stdout.strip()
    row(outs["fast"] != outs["off"], "fma measured: a naive C loop x*x-2 under -ffp-contract=fast -march=native "
        "ends at %s after 3000 steps, against %s unfused (a fused rounding repeated at every step, which chaos "
        "magnifies)"
        % (outs["fast"], outs["off"]))
    # The source is generated here, not looked up in the build cache: the cache also holds the c99-explicit-fma
    # plant's copy of chaos (same law, an fma() call added), and a reused cache once listed it first, so the row
    # counted the plant's FMA instead of Orlog's (found moving the project into its repository).
    from orlog.arbiter import generate
    from orlog.lower import Lowered
    chaos = os.path.join(workdir, "chaos_generated.c")
    with open(chaos, "wb") as fh:
        fh.write(generate("c99", Lowered(compile_bytes(read("examples/chaos.orl")))).encode("utf-8"))
    asm = os.path.join(workdir, "chaos_fast.s")
    subprocess.run(["clang", "-std=c99", "-O2", "-ffp-contract=fast", "-march=native", "-S", chaos, "-o", asm],
                   capture_output=True)
    with open(asm, "rb") as fh:
        text = fh.read().decode("ascii", "replace").lower()
    n_fma = sum(text.count(k) for k in ("vfmadd", "vfmsub", "vfnmadd", "vfnmsub"))
    row(n_fma == 0, "fma measured: Orlog's generated C for chaos.orl has %d FMA instructions under the same flags "
        "(each rounded intermediate is observed by the NaN canonicalization, so it cannot be fused)" % n_fma)


@contextlib.contextmanager
def reference_truncates_quotient():
    saved = N.i_quot

    def trunc(a, b):
        if b == 0:
            raise N.Refusal("DIVISION-BY-ZERO")
        q = abs(a) // abs(b)
        return N.chk(q if (a < 0) == (b < 0) else -q)
    N.i_quot = trunc
    try:
        yield
    finally:
        N.i_quot = saved


def reference_dissent_plant(workdir, backends):
    fixture = prog("§1 Say the quotient of -7 by 2.")
    arb = Arbiter(workdir, backends=backends, reference_patch=reference_truncates_quotient)
    comp, w, ref = arb.arbitrate(fixture, "plant-ref-quot")
    ok = w["dissent_kind"] == "REFERENCE-DISSENT" if len(backends) >= 2 else bool(w["dissenting"])
    if len(backends) >= 2:
        witness = "dissent kind %s: [%s] agree with each other against the reference" % (
            w["dissent_kind"], ",".join(w["dissenting"]))
    else:       # one backend cannot agree with another: REFERENCE-DISSENT needs two (prosecutor F56)
        witness = "dissent kind %s: [%s] dissents from the reference; with one backend the kind cannot be " \
                  "REFERENCE-DISSENT, which needs two backends agreeing against it" % (
                      w["dissent_kind"], ",".join(w["dissenting"]))
    plant("reference-quotient-truncates", ok, witness + "; the reference is still kept, by declaration")


# ------------------------------------------------------------------ the court
FIXTURE = "FIXTURE written by the self-test; not a person's act"


def ledger_for(comp, *claim_ids, theorems=()):
    seals = COURT.claim_seals(comp)
    lines = [{"kind": "claim", "claim_seal": seals[k], "note": FIXTURE, "_line": i + 1} for i, k in enumerate(claim_ids)]
    lines += [{"kind": "theorem", "name": t, "note": FIXTURE, "_line": len(lines) + j + 1} for j, t in enumerate(theorems)]
    return lines


def court_rows(arb, workdir):
    raw = read("examples/plankton.orl")
    comp, w, ref = arb.arbitrate(raw, "court-plankton")
    rec = parse_receipt(ref.receipt())
    p = COURT.panel(comp, w, rec, [])
    sup = {r["clause"]: r["support"] for r in p["rows"]}
    gr = {r["clause"]: r["grounding"] for r in p["rows"]}
    want = {"§3": "CIRCULAR", "§4": "CIRCULAR", "§5": "CIRCULAR", "§6": "WELL-FOUNDED"}
    ok = all(sup[k].startswith(v) for k, v in want.items()) and p["summary"]["sandwich"] == "OPEN"
    row(ok, "court: Plankton's three mutually supporting claims are CIRCULAR (gfp, not lfp); the fourth is "
        "WELL-FOUNDED; the sandwich is OPEN", json.dumps(sup))
    cyc = {r["clause"]: r.get("cycle") for r in p["rows"]}
    row(cyc["§3"] == "§3 -> §4 -> §5 -> §3", "court: a CIRCULAR claim names its cycle (%s)"
        % cyc["§3"])
    row(gr["§6"] == "UNGROUNDED", "court: a cited, unratified theorem leaves its claim UNGROUNDED")
    thm6 = comp.an.claims[3].stmt.oracle[1]
    p_name = COURT.panel(comp, w, rec, ledger_for(comp, theorems=[thm6]))
    row({r["clause"]: r["grounding"] for r in p_name["rows"]}["§6"] == "UNGROUNDED",
        "court: a theorem ratified by name alone grounds nothing (court L4: a name is not bound to the claim)")
    p2 = COURT.panel(comp, w, rec, ledger_for(comp, 3, 0, 1, 2))
    gr2 = {r["clause"]: r["grounding"] for r in p2["rows"]}
    row(gr2["§6"] == "GROUNDED" and all(gr2[k] == "UNGROUNDED" for k in ("§3", "§4", "§5")),
        "court: with this claim's own seal ratified (fixture), §6 is GROUNDED; ratifying the circle's computation "
        "claims grounds none of them (R2)")
    saved = COURT.support_sets
    COURT.support_sets = lambda claims, base, prem: (saved(claims, base, prem)[1],) * 2
    try:
        pp = COURT.panel(comp, w, rec, [])
        caught = any(r["support"] == "WELL-FOUNDED" for r in pp["rows"] if r["clause"] in ("§3", "§4", "§5"))
    finally:
        COURT.support_sets = saved
    plant("court-accepts-gfp", caught, "under the plant §3-§5 read WELL-FOUNDED, so the CIRCULAR row fails")
    # court finding L5: a well-founded computation claim must never ground, even with its own seal in the ledger
    plain = prog("§1 Let a be 2.", "§2 We claim that a equals 2.", "§3 We claim that a is even, "
                 "by agreement of §1 and §2.")
    comp, w, ref = arb.arbitrate(plain, "court-computation")
    rec = parse_receipt(ref.receipt())
    led = ledger_for(comp, 0, 1)
    p = COURT.panel(comp, w, rec, led)
    honest = [(r["support"], r["grounding"]) for r in p["rows"]]
    row(honest == [("WELL-FOUNDED", "UNGROUNDED")] * 2,
        "court: computation and agreement claims are WELL-FOUNDED and stay UNGROUNDED with their seals ratified (R2, R3)",
        str(honest))
    saved_adm = COURT.grounding_admissible
    COURT.grounding_admissible = lambda channel: True
    try:
        pp = COURT.panel(comp, w, rec, led)
        caught = any(r["grounding"] == "GROUNDED" for r in pp["rows"])
    finally:
        COURT.grounding_admissible = saved_adm
    plant("court-grounds-computation", caught, "under the plant a computation claim reads GROUNDED, so the R2 row fails")
    # certificates: CHEAPER is a counted reading, and grounding needs this claim's seal, not a theorem's name (L8)
    comp, w, ref = arb.arbitrate(read("examples/gcd_certificate.orl"), "court-gcd")
    rec = parse_receipt(ref.receipt())
    p = COURT.panel(comp, w, rec, [])
    r = p["rows"][0]
    row(r["cost_reading"].startswith("CHEAPER") and r["grounding"] == "UNGROUNDED",
        "court: the Bezout certificate reads CHEAPER (%s) and is UNGROUNDED unratified" % r["cost"])
    thm = comp.an.claims[0].stmt.oracle[2]
    p = COURT.panel(comp, w, rec, ledger_for(comp, theorems=[thm]))
    row(p["rows"][0]["grounding"] == "UNGROUNDED", "court: its theorem ratified by name alone does not ground it (L8)")
    p = COURT.panel(comp, w, rec, ledger_for(comp, 0))
    row(p["rows"][0]["grounding"] == "GROUNDED", "court: with this claim's own seal ratified (fixture), GROUNDED")
    weak = read("examples/gcd_certificate.orl").split("§12 ".encode("utf-8"))[0] + (
        "§12 We claim that g is positive, by the certificate of §9 under the theorem \"%s\".\n" % thm).encode("utf-8")
    comp2, w2, ref2 = arb.arbitrate(weak, "court-gcd-weak")
    p = COURT.panel(comp2, w2, parse_receipt(ref2.receipt()), ledger_for(comp2, theorems=[thm]))
    row(p["rows"][0]["grounding"] == "UNGROUNDED",
        "court: the prosecution's D2 (a one-op check under Bezout's name, theorem ratified) stays UNGROUNDED")
    row(ledger_for(comp2, 0)[0]["claim_seal"] != ledger_for(comp, 0)[0]["claim_seal"],
        "court: the weak claim's seal differs from the full certificate's, so the full one's ratification cannot "
        "be lifted onto it")
    costly = prog("§1 Let a be 5.", "§2 We claim that a times a times a plus a equals 130 and a is odd, "
                  "by the certificate of §1.")
    comp, w, ref = arb.arbitrate(costly, "court-costly")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    row(p["rows"][0]["cost_reading"].startswith("NOT CHEAPER"),
        "court: a check costing more than half its clause reads NOT CHEAPER, never 'recomputation' (L7)",
        p["rows"][0]["cost"])
    notrun = prog("§1 Let a be 1.", "§2 If a equals 2, do the following.", "§2.1 Let b be a times 1000.",
                  "§3 We claim that a equals 1, by the certificate of §2.1.")
    comp, w, ref = arb.arbitrate(notrun, "court-notrun")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    row(p["rows"][0]["cost_reading"] == "CLAUSE NOT RUN", "court: a certificate of a clause that never ran reads "
        "CLAUSE NOT RUN (L7)")
    # court finding L17: inline claims, and UNREACHED as its own standing
    inline = prog("§1 Let a be 1.", "§2 If a equals 1, we claim that a is positive; otherwise we claim that "
                  "a is negative.", "§3 If a equals 2, do the following.", "§3.1 We claim that a is odd.",
                  "§4 We claim that a equals 1, given §3.1.")
    comp, w, ref = arb.arbitrate(inline, "court-inline")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    sup = [(r["clause"], r["support"]) for r in p["rows"]]
    row(sup == [("§2#0", "WELL-FOUNDED"), ("§2#1", "UNREACHED"), ("§3.1", "UNREACHED"),
                ("§4", "UNSUPPORTED")] and p["summary"]["unreached"] == 2,
        "court: two inline claims in one clause each get a row; an unreached claim reads UNREACHED, and a claim "
        "resting on it is UNSUPPORTED (L17, R7)", str(sup))
    # court finding L10: a closure over nothing, or over a contested run, is VACUOUS
    empty = prog("§1 Say 1.")
    comp, w, ref = arb.arbitrate(empty, "court-empty")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    row(p["summary"]["sandwich"].startswith("VACUOUS"), "court: with no claim at all the sandwich reads VACUOUS, "
        "never CLOSED (L10)")
    contested = Arbiter(workdir, backends=arb.backends, reference_patch=reference_truncates_quotient)
    comp, w, ref = contested.arbitrate(prog("§1 Let q be the quotient of -7 by 2.",
                                            "§2 We claim that q equals -4."), "court-contested")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    row(w["dissent_kind"] != "NONE" and p["summary"]["sandwich"].startswith("VACUOUS"),
        "court: when the backends disagree the sandwich reads VACUOUS, never CLOSED (L10)", w["dissent_kind"])
    # chaotic iteration and Dung's grounded semantics on fixtures
    rng = random.Random(11)
    ids = set(range(40))
    base = {i: rng.random() < 0.8 for i in ids}
    prem = {i: set(rng.sample(sorted(ids), rng.randint(0, 3))) for i in ids}
    row(COURT.chaotic_agrees(ids, base, prem), "court: 200 random fair single-element schedules reach Kleene's "
        "least fixed point on a 40-claim instance (Cousot 1977, one instance)")
    args = {"a", "b", "c", "d", "e"}
    attacks = {("a", "b"), ("b", "c"), ("d", "e"), ("e", "d")}
    inn, out, und = COURT.grounded_extension(args, attacks)
    row(inn == {"a", "c"} and out == {"b"} and und == {"d", "e"},
        "court: Dung grounded extension: a defends c; a mutual attack between d and e is UNDECIDED")


REDTEAM_RUNS = ["E1_eq_promotion_crash", "E2a_rule_in_procedure", "E2b_rule_uses_rule",
                "E10_python_depth_if_chain_110", "E16a_upper_to", "E13b_note_after_seal",
                "E16b_to_two_spaces", "E16e_to_no_space", "E16f_to_inner_spaces"]
REDTEAM_REFUSALS = [("E3_hidden_children", "UNEXPECTED-CHILDREN"), ("E3b_hidden_children_crash", "UNEXPECTED-CHILDREN"),
                    ("E17a_kelvin_identifier", "NON-ASCII-CODE"), ("E17b_greek_question_mark", "NON-ASCII-CODE"),
                    ("E13_two_seals", "SEAL-PLACE"), ("E15_two_oracles", "SYNTAX"),
                    ("E16c_nested_to", "PROCEDURE-PLACE"), ("E16d_to_named_to", "PROCEDURE-NAME"),
                    ("E14_define_both_provisos", "SYNTAX"),
                    ("E24_python_depth_and_inside_loops", "EXPRESSION-DEPTH"),
                    ("E24b_and_inside_loops_ok", "EXPRESSION-DEPTH"),
                    ("E25_parser_recursion_parens", "EXPRESSION-DEPTH"),
                    ("E25b_parser_recursion_and", "EXPRESSION-DEPTH")]


def redteam_rows(arb):
    """The engineering red team's reproducers (tests/fixtures/redteam/, copied from court/redteam-eng/)."""
    for name in REDTEAM_RUNS:
        comp, w, ref = arb.arbitrate(read("tests/fixtures/redteam/%s.orl" % name), "rt-" + name)
        ok = comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(arb.backends)
        row(ok, "red team %s: compiles and runs byte-identically on the reference and [%s]" % (
            name, ",".join(w.get("agreeing", []))), "" if ok else str(w.get("refusal") or w.get("mismatch_notes"))[:300])
    for name, code in REDTEAM_REFUSALS:
        c = compile_bytes(read("tests/fixtures/redteam/%s.orl" % name))
        row(not c.ok and c.error.code == code, "red team %s: refused %s" % (name, code),
            "" if (not c.ok and c.error.code == code) else str(c.error))
    deep = ["§" + ".".join(["1"] * k) + " For each i%d from 1 to 1, do the following." % k for k in range(1, 17)]
    deep.append("§" + ".".join(["1"] * 17) + " Say i1 plus i16.")
    comp, w, ref = arb.arbitrate(prog(*deep), "rt-limit-16-loops")
    row(comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(arb.backends),
        "bounds: 16 nested loops (the LOOP-NESTING limit) run byte-identically on the reference and [%s]"
        % ",".join(w.get("agreeing", [])), "" if comp.ok else str(comp.error))
    over = ["§" + ".".join(["1"] * k) + " For each i%d from 1 to 1, do the following." % k for k in range(1, 18)]
    over.append("§" + ".".join(["1"] * 18) + " Say 1.")
    c = compile_bytes(prog(*over))
    row(not c.ok and c.error.code == "LOOP-NESTING", "bounds: 17 nested loops are refused LOOP-NESTING",
        "" if not c.ok else "compiled")
    at_limit = ["§" + ".".join(["1"] * k) + " If true, do the following." for k in range(1, 24)]
    at_limit.append("§" + ".".join(["1"] * 24) + " Say 1.")
    comp, w, ref = arb.arbitrate(prog(*at_limit), "rt-limit-24-deep")
    ok = comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(arb.backends) and bytes(ref.out) == b"1\n"
    row(ok, "bounds: clauses 24 deep (the NESTING-DEPTH limit) run byte-identically on the reference and [%s]"
        % ",".join(w.get("agreeing", [])), "" if comp.ok else str(comp.error))
    tall = ["§" + ".".join(["1"] * k) + " If true, do the following." for k in range(1, 25)]
    tall.append("§" + ".".join(["1"] * 25) + " Say 1.")
    c = compile_bytes(prog(*tall))
    row(not c.ok and c.error.code == "NESTING-DEPTH", "bounds: clauses 25 deep are refused NESTING-DEPTH",
        "" if not c.ok else "compiled")
    ok, agreeing = chain_runs(arb)
    row(ok, "bounds: a 600-arm If chain runs byte-identically on the reference and [%s] (constant-depth lowering)"
        % ",".join(agreeing))


CHAIN_600 = ["§1 Let x be 599.", "§2 If x equals 0, say 0."] + [
    "§%d Otherwise, if x equals %d, say %d." % (k + 2, k, k) for k in range(1, 600)]


def chain_runs(a):
    """The chain row's reading: every backend that ran agreeing (E10's class shows as a compiler refusing the chain,
    which 'none dissenting' had read as a pass: the reporting pass's finding 8)."""
    comp, w, ref = a.arbitrate(prog(*CHAIN_600), "rt-chain-600")
    return (comp.ok and len(w["agreeing"]) == len(a.backends) and ref is not None and bytes(ref.out) == b"599\n",
            w.get("agreeing", []))


def redteam_v2_rows(arb, workdir, backends):
    """The red team's findings that held at its report (E7 to E26), each repair held by a row, with a plant where the
    row could pass by accident."""
    # E7: agreement is byte equality of the receipts with their second line, 'backend <name>', removed
    comp, w, ref = arb.arbitrate(read("examples/collatz.orl"), "rt2-e7")
    good = ref.receipt()
    core = receipt_core(good)
    renamed = good.replace(b"\nbackend reference\n", b"\nbackend python\n", 1)
    crlf, nolf = good.replace(b"\n", b"\r\n"), good[:-1]
    extra = good.replace(b"\nend\n", b"\nbackend ops 0 trust me\nend\n")
    checks = [core is not None, receipt_core(renamed) == core, receipt_core(crlf) is None,
              receipt_core(nolf) is None, receipt_core(extra) != core]
    row(all(checks), "arbiter: receipts agree byte for byte without their second line, and only that line: a renamed "
        "backend agrees; a CR LF receipt, one without its final LF and one with an extra line do not (red team E7)",
        str(checks))
    # The plant that stood here ran a stand-in comparison and never reached the verdict (the reporting pass's finding
    # 4); E7's plant is now the pre-E7 comparison put back into the arbiter's verdict, in reporting_rows.
    # E8: a failed build is reported, never counted as a dissent
    if {"python", "c99", "rust"} <= set(backends):
        masking = Arbiter(workdir, backends=("python", "c99", "rust"), reference_patch=reference_truncates_quotient,
                          mutate=mutate_with("rust", lambda src: src + "\nthis is not rust\n"))
        comp, w, ref = masking.arbitrate(prog("§1 Say the quotient of -7 by 2."), "rt2-e8")
        ok = w["dissent_kind"] == "REFERENCE-DISSENT" and w["build_failed"] == ["rust"]
        row(ok, "arbiter: with the reference planted wrong and the Rust source planted not to compile, the kind stays "
            "REFERENCE-DISSENT and build_failed names rust (red team E8)", "%s %s" % (w["dissent_kind"],
                                                                                   w["build_failed"]))
    # E9: curly quotes inside a straight-quoted literal are its text
    comp, w, ref = arb.arbitrate(read("tests/fixtures/redteam/E9_door_curly_in_literal.orl"), "rt2-e9")
    want = "Use “followed by” to join\n".encode("utf-8")
    ok = comp.ok and not comp.canon.events and bytes(ref.out) == want and len(w["agreeing"]) == len(arb.backends)
    row(ok, "door: curly quotes inside a straight-quoted literal are its text: no event, and the reference and [%s] "
        "print them byte for byte (red team E9)" % ",".join(w.get("agreeing", [])),
        "" if ok else repr(bytes(ref.out) if ref is not None else comp.error))
    # E11: a work folder with non-ASCII letters in its name
    odd = os.path.join(ROOT, "build", "selftest-ØRLǪG")
    os.makedirs(odd, exist_ok=True)
    comp, w, ref = Arbiter(odd, backends=backends).arbitrate(read("examples/collatz.orl"), "rt2-e11")
    ok = comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(backends)
    row(ok, "arbiter: a work folder named %s changes nothing: the reference and [%s] agree (red team E11)" % (
        os.path.basename(odd), ",".join(w.get("agreeing", []))), "" if ok else str(w.get("mismatch_notes"))[:300])
    # E19: invisible characters inside a literal, and no false event on the refused line
    c = compile_bytes(read("tests/fixtures/redteam/E19_invisible_in_literal.orl"))
    rules = [e["rule"] for e in c.canon.events]
    ok = not c.ok and c.error.code == "INVISIBLE-CHAR" and "QUOTE-BOUNDARY" not in rules
    row(ok, "door: a Hangul filler, a tag character and a line separator inside a literal are refused, and the refused "
        "line logs no QUOTE-BOUNDARY it did not meet (red team E19; SPEC §13)", str(rules))
    # E20: label spelling never reaches the law
    three = [compile_bytes(read("tests/fixtures/redteam/%s.orl" % n)) for n in
             ("E20a_labels_plain", "E20b_labels_leading_zero", "E20c_label_ref_as_integer")]
    ok = all(x.ok for x in three) and len({x.law_seal for x in three}) == 1
    row(ok, "law: §2, §02, and §02 named by a reference §2 give one law-seal (red team E20; amendment 6)",
        "" if ok else str([x.law_seal[:12] if x.ok else x.error.code for x in three]))
    # E26: no false note on a line with no literal
    c = compile_bytes(read("tests/fixtures/redteam/E26_false_door_note.orl"))
    ev = [(e["cls"], e["rule"]) for e in c.canon.events]
    row(c.ok and ev == [("REPAIR", "R-SPACE")], "door: a typographic space in code is repaired once, with no "
        "LITERAL-NOT-NFC note on a line that has no literal (red team E26)", str(ev))
    # E24: the bounds compose under the Python host's 100 indentation levels, and are exact (SPEC §13)
    e = "true"
    for _ in range(23):
        e = "true and (" + e + ")"
    loops = ["§" + ".".join(["1"] * k) + " For each i%d from 1 to 1, do the following." % k for k in range(1, 17)]
    at = "§" + ".".join(["1"] * 17) + " Say %s."
    comp, w, ref = arb.arbitrate(prog(*(loops + [at % e])), "rt2-bounds-compose")
    ok = comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(arb.backends) and bytes(ref.out) == b"true\n"
    row(ok, "bounds: 16 nested loops around 23 nested parenthesized 'and's, both bounds at their limits, run "
        "byte-identically on the reference and [%s] (red team E24)" % ",".join(w.get("agreeing", [])),
        "" if ok else str(comp.error if not comp.ok else w.get("mismatch_notes"))[:300])
    c = compile_bytes(prog(*(loops + [at % ("true and (%s)" % e)])))
    row(not c.ok and c.error.code == "EXPRESSION-DEPTH", "bounds: one more parenthesis is refused EXPRESSION-DEPTH, "
        "as SPEC §13 counts it (atoms, minuses and nots on the path, the atom included; over 24 refused)",
        "" if not c.ok else "compiled")
    # the court's CONSTANT reading (red team E5, Semiotic core TRIAGE's tautology airlock)
    comp, w, ref = arb.arbitrate(prog("§1 Let x be 1.", "§2 We claim that 1 equals 1.", "§3 We claim that x equals 1."),
                                 "rt2-constant")
    p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
    cond = [r.get("condition", "") for r in p["rows"]]
    row(len(cond) == 2 and cond[0].startswith("CONSTANT") and not cond[1], "court: a claim that reads no variable "
        "is marked CONSTANT and one that reads the run is not (red team E5)", str(cond))


# ------------------------------------------------------------------ what agreement measures (tests of a claim)
def load_twin():
    import importlib.util
    spec = importlib.util.spec_from_file_location("orlog_twin", os.path.join(ROOT, "twin", "twin.py"))
    twin = importlib.util.module_from_spec(spec)
    saved, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(twin)
    finally:
        sys.dont_write_bytecode = saved
    return twin


def flip_plus(node, seen):
    """The front-end plant: every 'plus' the parser built becomes a minus."""
    from orlog.syntax import Node, Bin
    if isinstance(node, Node):
        if id(node) in seen:
            return
        seen.add(id(node))
        if isinstance(node, Bin) and node.op == "+":
            node.op = "-"
        for k in node.fields:
            flip_plus(getattr(node, k, None), seen)
    elif isinstance(node, (list, tuple)):
        for x in node:
            flip_plus(x, seen)


def run_python(*args):
    import subprocess
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    return subprocess.run([sys.executable, "-B"] + list(args), capture_output=True, text=True, encoding="utf-8",
                          env=env)


def independence_rows(workdir, backends):
    """Tests of a claim, not of the code (README, 'What agreement measures'). Each plant is a defect in a layer that
    some of the executions share, and each row records which executions can see it. A row that expects a defect to
    slip past them guards against anyone later reading four-way agreement as more than it is."""
    from orlog import front, lower
    # the lowering: the three backends share it; the reference does not lower
    saved_emit = lower.Lowered.emit

    def emit(self, *ins):
        saved_emit(self, *ins)
        if ins and ins[0] == "call" and isinstance(ins[2], str) and ins[2].endswith("_mul"):
            saved_emit(self, "tick")                  # one operation too many at every multiplication
    lower.Lowered.emit = emit
    try:
        comp, w, ref = Arbiter(workdir, backends=backends).arbitrate(read("examples/collatz.orl"), "ind-lowering")
    finally:
        lower.Lowered.emit = saved_emit
    m = re.search(rb"\nops (\d+)\n", ref.receipt()) if ref is not None else None
    ref_ops = int(m.group(1)) if m else -1
    ops = sorted({int(w["backends"][b]["ops"]) for b in w["dissenting"]})
    # the witness: traces and outputs equal, and every backend counts exactly one operation more per multiplication
    # executed: collatz's orbit of 27 has 111 steps, 41 of them 3n+1
    witness = ops == [ref_ops + 41] and all(x.get("first_divergent_event") is None for x in w["mismatch_notes"])
    if len(backends) >= 2:
        ok = witness and w["dissent_kind"] == "REFERENCE-DISSENT" and sorted(w["dissenting"]) == sorted(backends)
        moved = "moves [%s] together, %s: they agree with each other against the reference" % (
            ",".join(w["dissenting"]), w["dissent_kind"])
    else:
        ok = witness and w["dissenting"] == list(backends)
        moved = "makes [%s] dissent from the reference, %s (one backend has no other to agree with)" % (
            ",".join(w["dissenting"]), w["dissent_kind"])
    row(ok, "independence: a defect planted in the shared lowering (one operation counted too many at every "
        "multiplication) %s, the one execution that does not lower" % moved,
        "traces and outputs equal; the receipt's ops reads %d in the reference and %s in the backends: 41 more, one "
        "per 3n+1 step of the orbit of 27" % (ref_ops, ",".join(map(str, ops))))
    # the front end: all four executions share it; the clean-room twin has its own
    saved_parse = front.parse_program

    def parse(text):
        p = saved_parse(text)
        seen = set()
        for c in p.clauses:
            flip_plus(c.stmt, seen)
        return p
    front.parse_program = parse
    try:
        comp, w, ref = Arbiter(workdir, backends=backends).arbitrate(read("examples/fall.orl"), "ind-frontend")
    finally:
        front.parse_program = saved_parse
    planted_out = bytes(ref.out) if ref is not None else None
    good = compile_bytes(read("examples/fall.orl"))
    twin = load_twin()
    rt, status = twin.execute(twin.compile_text(read("examples/fall.orl").decode("utf-8"), good.law_seal),
                              good.law_seal)
    clean = Interp(good.prog, good.an, good.law_seal, good.text_seal).run()
    four_agree = comp.ok and w["dissent_kind"] == "NONE" and len(w["agreeing"]) == len(backends)
    twin_sees = bytes(rt.out) != planted_out and bytes(rt.out) == bytes(clean.out)
    row(four_agree and twin_sees, "independence (MONITORED NEGATIVE: it passes when the defect slips past): a defect "
        "planted in the shared front end (every 'plus' read as 'minus') passes all %d executions, which agree "
        "[reference,%s]; only the clean-room twin, whose front end is its own, differs from them, and it equals the "
        "unplanted reference. Their agreement does not test the front end. The day the front end gains real "
        "diversity this row must flip to expect detection; it is not a failure to delete"
        % (len(backends) + 1, ",".join(w["agreeing"])),
        "" if four_agree else "the four executions no longer agree under a front-end defect: if the front end has "
        "gained diversity, flip this row to expect detection (README, 'What agreement measures')")
    # the arithmetic: numeric_ref generated every vector; a derivation that never imports it holds them
    r = run_python(os.path.join(ROOT, "tests", "vectors_independent.py"))
    lines = r.stdout.splitlines()
    planted = [l for l in lines if l.startswith("plant ")]
    caught = [l for l in planted if ": CAUGHT;" in l]
    m1 = re.search(r"^1\. derivation vs the vectors: (\d+) of (\d+) lines derived, (\d+) differ", r.stdout, re.M)
    m2 = re.search(r"^2\. hand table: (\d+) cases", r.stdout, re.M)
    ok = (r.returncode == 0 and bool(lines) and lines[-1].startswith("VECTORS AGREE") and m1 and m2
          and m1.group(3) == "0" and len(planted) == len(caught) == 5)
    row(ok, "independence: the runtime vectors, every one generated by numeric_ref, agree with a second derivation "
        "that never imports it (%s of %s lines derived, 0 differ), with %s hand-worked cases and with two published "
        "SHA-256 digests; its %d plants caught, three of them mistakes that numeric_ref and its vectors would share "
        "(tests/vectors_independent.py)" % (m1.group(1) if m1 else "?", m1.group(2) if m1 else "?",
                                            m2.group(1) if m2 else "?", len(caught)),
        "" if ok else (r.stdout[-600:] + r.stderr[-600:]))


def isolation_rows(backends):
    """The arbiter's purity: arbitrations sharing a work folder cannot see each other's files."""
    import concurrent.futures
    import shutil
    import tempfile
    wd = os.path.join(ROOT, "build", "selftest-isolation")
    shutil.rmtree(wd, ignore_errors=True)
    os.makedirs(wd)
    a_src, b_src = prog("§1 Let x be 6.", "§2 Say x times 7."), prog("§1 Let y be 5.", "§2 Say y plus 1.")
    real = tempfile.mkdtemp

    def run_two(fake, arbiter_cls=Arbiter):
        """The folders each arbitration made, and the folder every one of its runs ran in."""
        used, cwds = [], []

        class Recording(arbiter_cls):
            def run(self, cmd, tag, trace=False, cwd=None):
                cwds.append(cwd)
                return arbiter_cls.run(self, cmd, tag, trace=trace, cwd=cwd)

        def mk(*args, **kw):
            d = fake(*args, **kw) if kw.get("prefix") == "arb-" else real(*args, **kw)
            if kw.get("prefix") == "arb-":
                used.append(d)
            return d
        tempfile.mkdtemp = mk
        try:
            for src in (a_src, b_src):
                Recording(wd, backends=backends).arbitrate(src, "iso")
        finally:
            tempfile.mkdtemp = real
        return used, cwds

    def isolated(used, cwds):
        """Two folders, distinct, none left, and every run in one of them: a folder made and removed while the runs
        happened in the shared one had passed (the reporting pass's finding 18)."""
        return (len(used) == 2 and used[0] != used[1] and not any(os.path.exists(d) for d in used) and bool(cwds)
                and all(c in used for c in cwds) and set(cwds) == set(used))
    used, cwds = run_two(real)
    ok = isolated(used, cwds)
    # the folders' names are random, so the detail gives counts: a row's text must be the same on every run
    row(ok, "arbiter: each arbitration runs in a folder of its own inside the work folder, every one of its runs "
        "there, and the folder is removed afterwards (two arbitrations, two folders, none left)",
        "" if ok else "%d folder(s) for %d arbitrations, %d distinct, %d left, %d run(s) outside them" % (
            len(used), 2, len(set(used)), sum(1 for d in used if os.path.exists(d)),
            sum(1 for c in cwds if c not in used)))
    shared_runs = planted("src/orlog/arbiter.py", [('r = self.run(cmd, "%s-%s" % (name, b), cwd=rundir)',
                                                    'r = self.run(cmd, "%s-%s" % (name, b), cwd=self.workdir)')])
    used, cwds = run_two(real, shared_runs.Arbiter)
    plant("run-folder-made-but-shared", not isolated(used, cwds),
          "under the plant each arbitration made and removed its own folder while its runs ran in the shared work "
          "folder, so the row's runs are outside the arbitrations' folders")

    def one(k):
        try:
            comp, w, ref = Arbiter(wd, backends=backends).arbitrate(a_src if k % 2 else b_src, "race")
            return "BUILD-FAILED" if w["build_failed"] else w["dissent_kind"]
        except Exception as e:
            return "TRACEBACK " + type(e).__name__
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        outs = list(ex.map(one, range(16)))
    counts = {}
    for o in outs:
        counts[o] = counts.get(o, 0) + 1
    left = [x for x in os.listdir(wd) if x.startswith("arb-")]
    row(counts == {"NONE": 16} and not left, "arbiter: 16 arbitrations of two different programs at once in one work "
        "folder all agree, and no run folder is left (the use-case review's race, which once gave false dissents)",
        "%s; %d left" % (counts, len(left)))
    shared = os.path.join(wd, "arb-shared")

    def constant(*args, **kw):
        os.makedirs(shared, exist_ok=True)
        return shared
    used, _ = run_two(constant)
    plant("arbiter-shares-a-run-folder", len(used) == 2 and used[0] == used[1],
          "under the plant both arbitrations ran in %s, so the row's two folders are one" % os.path.basename(shared))


def honesty_rows(workdir, backends):
    """What a run that did not finish may say: a backend that did not build, a run the host stopped, a torn ledger."""
    if "c99" in backends:
        arb = Arbiter(workdir, backends=backends, mutate=mutate_with("c99", lambda s: s + "\nthis is not C\n"))
        comp, w, ref = arb.arbitrate(read("examples/collatz.orl"), "hon-build-failed")
        p = COURT.panel(comp, w, parse_receipt(ref.receipt()), [])
        integ = sorted({r["integrity"] for r in p["rows"]})
        others = sorted(b for b in backends if b != "c99")
        ok = (w["build_failed"] == ["c99"] and "c99" not in w["agreeing"] + w["dissenting"]
              and sorted(w["agreeing"]) == others and w["dissent_kind"] == "BUILD-FAILED"
              and integ == ["INCOMPLETE (did not build: c99)"] and p["summary"]["sandwich"].startswith("VACUOUS"))
        row(ok, "arbiter: a backend that did not build is counted neither agreeing nor dissenting: BUILD-FAILED, every "
            "claim's integrity INCOMPLETE (did not build: c99), the sandwich VACUOUS",
            "%s %s %s %s" % (w["dissent_kind"], w["build_failed"], integ, p["summary"]["sandwich"][:40]))
    runaway = prog("§1 Let n be 0.", "§2 For each i from 1 to 1000000000, do the following.",
                   "§2.1 Increase n by 1.", "§3 Say n.")
    stops = []
    for _ in range(2):
        comp, w, ref = Arbiter(workdir, backends=backends, ops_budget=10 ** 5).arbitrate(runaway, "hon-runaway")
        stops.append((ref is None, w["dissent_kind"], w.get("stopped"), (w["mismatch_notes"] or [{}])[0].get("detail")))
    comp, w, ref = Arbiter(workdir, backends=backends, ops_budget=10 ** 5).arbitrate(read("examples/collatz.orl"),
                                                                                   "hon-within")
    within = ref is not None and w["dissent_kind"] == "NONE"
    ok = (stops[0] == stops[1] and stops[0][0] and stops[0][1] == "STOPPED-BY-HOST" and stops[0][2] == ["reference"]
          and within)
    row(ok, "host budget: a loop of 10^9 iterations under a budget of 10^5 counted operations is stopped by the host "
        "at the same operation twice (%s): STOPPED-BY-HOST, no receipt, not a refusal; a program within the budget "
        "runs and agrees" % stops[0][3], "" if ok else str(stops))
    torn = os.path.join(workdir, "torn.jsonl")
    with open(torn, "wb") as fh:
        fh.write(b'{"by": "x", "kind": "theorem", "name": "t", "note": "n"}\n{"kind": "claim", "claim_se')
    try:
        COURT.read_ledger(torn)
        refused = None
    except COURT.LedgerBroken as e:
        refused = str(e)
    r = run_python(os.path.join(ROOT, "orl.py"), "court", os.path.join(ROOT, "examples", "collatz.orl"), "--ledger",
                   torn, "--backends", backends[0], "--workdir", workdir)
    ok = (refused is not None and refused.startswith("LEDGER-BROKEN at line 2") and r.returncode == 1
          and r.stdout.startswith("LEDGER-BROKEN at line 2") and not r.stderr.strip())
    row(ok, "ledger: a ledger torn in mid-line is refused whole, LEDGER-BROKEN at line 2, by the reader and by "
        "'orl.py court' (exit 1, no traceback); none of it is read", "" if ok else "%s | exit %s | %s" % (
            refused, r.returncode, (r.stdout + r.stderr)[-300:]))

    def skip_torn(path):            # the other wrong reading: keep what parses, drop the rest without a word
        kept = []
        for line in open(path, "rb").read().split(b"\n"):
            try:
                kept.append(json.loads(line))
            except ValueError:
                pass
        return kept
    kept = skip_torn(torn)
    plant("ledger-skips-torn-lines", len(kept) == 1, "a reader that skips what does not parse returns %d entry and "
          "drops line 2 without a word, so the row's refusal is absent" % len(kept))


def e18_e22_rows(workdir):
    """Two repairs from the red team's report that had no row (prosecutor F6)."""
    raw = read("tests/fixtures/redteam/E18_door_not_idempotent.raw")
    c = CANON.canonicalize(raw)
    ok = c.text is None and any(e["rule"] == "QUOTE-BOUNDARY" for e in c.events)
    row(ok, "door: the red team's E18 bytes (an NBSP, 'Note:', a quote, an NBSP, a quote) are refused QUOTE-BOUNDARY; "
        "the door once repaired them into a text that a second pass repaired again (red team E18)",
        "" if ok else str([e["rule"] for e in c.events]))
    CANON.QUOTE_BOUNDARY_CHECK = False
    try:
        p1 = CANON.canonicalize(raw)
        p2 = CANON.canonicalize(p1.text.encode("utf-8")) if p1.text is not None else None
    finally:
        CANON.QUOTE_BOUNDARY_CHECK = True
    caught = p2 is not None and (p2.text != p1.text or bool(p2.repairs))
    plant("door-not-idempotent-on-E18", caught, "without the QUOTE-BOUNDARY check the door accepts E18 as %r, and a "
          "second pass makes it %r with %s" % (p1.text, p2.text if p2 else None,
                                               [e["rule"] for e in p2.events] if p2 else None))
    led = os.path.join(workdir, "e22.jsonl")
    if os.path.exists(led):
        os.remove(led)
    orl = os.path.join(ROOT, "orl.py")
    r1 = run_python(orl, "ratify", os.path.join(ROOT, "tests", "fixtures", "redteam", "E22_ratify_non_claim.orl"),
                    "--claim", "§1", "--note", "self-test", "--ledger", led)
    refused = r1.returncode == 1 and "no claim there" in r1.stdout and not os.path.exists(led)
    control = os.path.join(workdir, "e22_control.orl")
    with open(control, "wb") as fh:
        fh.write(prog("§1 Let x be 1.", "§2 We claim that x equals 1."))
    r2 = run_python(orl, "ratify", control, "--claim", "§2", "--note", "self-test control", "--ledger", led)
    entries = COURT.read_ledger(led) if os.path.exists(led) else []
    wrote = r2.returncode == 0 and len(entries) == 1 and entries[0].get("kind") == "claim"
    row(refused and wrote, "ratify: --claim §1 on the red team's E22 file (a Say whose text holds '(claim y') is "
        "refused and writes nothing, while --claim §2 on a real claim writes one entry (red team E22)",
        "" if refused and wrote else "%s | %s | %d entries" % (r1.stdout.strip(), r2.stdout.strip(), len(entries)))


def compat_rows():
    """COMPAT-0 (tests/compat.py): every text version 0 accepted keeps its law and its run; a refused one may later be
    accepted, and any other change is declared in tests/compat/settled.json or fails."""
    gate = os.path.join(ROOT, "tests", "compat.py")
    r = run_python(gate, "check", "--jobs", "8")
    m = re.search(r"^  same (\d+), newly accepted (\d+), settled (\d+), skipped (\d+), differ (\d+), input changed (\d+)",
                  r.stdout, re.M)
    n = re.search(r"; (\d+) texts;", r.stdout)
    ok = r.returncode == 0 and "COMPAT-0 HELD" in r.stdout and m is not None and n is not None
    row(ok, "compat: each of the %s texts frozen at version 0 gives the result it gave then (law seal, text seal and "
        "reference receipt, or refusal code and line): %s same, %s newly accepted, %s settled (COMPAT-0)" % (
            n.group(1) if n else "?", m.group(1) if m else "?", m.group(2) if m else "?", m.group(3) if m else "?"),
        "" if ok else (r.stdout[-600:] + r.stderr[-400:]))
    s = run_python(gate, "selftest")
    k = re.search(r"^COMPAT SELFTEST (\d+)/(\d+)", s.stdout, re.M)
    ok = s.returncode == 0 and k is not None and k.group(1) == k.group(2)
    row(ok, "compat: the gate's plants are caught (a word newly reserved, a law line respelled, a change only the "
        "receipts see, a frozen text altered, a declared change without its reason, a baseline row removed) and a "
        "declared change passes only with its exact new result (COMPAT SELFTEST %s/%s)" % (
            k.group(1) if k else "?", k.group(2) if k else "?"),
        "" if ok else (s.stdout[-600:] + s.stderr[-400:]))


R8_EXPECTED = {         # the court's R8 (the doppler debate's DP-5): fixture -> {clause label: (evaluation starts, grounding)}
    "omit.orl": {"§2.1": ("REFUSED at evaluation 17 (INDEX-OUT-OF-RANGE), after 16 true: not held", "UNGROUNDED")},
    "transitive.orl": {"§2": ("true in 1 of 1 evaluations", "UNGROUNDED"),
                       "§3.1": ("REFUSED at evaluation 2 (INDEX-OUT-OF-RANGE), after 1 true: not held", "UNGROUNDED")},
    "inline_claim.orl": {"§2.1": ("REFUSED at its clause (INDEX-OUT-OF-RANGE) after 16 of 16", "UNGROUNDED")},
    "inline_condition.orl": {"§2.1": ("REFUSED at its clause (INDEX-OUT-OF-RANGE) after 16 of 16", "UNGROUNDED")},
    # a plain Otherwise clause evaluates nothing but its arm: read exactly (the reporting pass's finding 15)
    "otherwise_claim.orl": {"§2.2": ("REFUSED at evaluation 17 (INDEX-OUT-OF-RANGE), after 16 true: not held",
                                     "UNGROUNDED")},
    # two claims that support each other, the second refusing at its second evaluation (finding 12)
    "cycle_refusal.orl": {"§2": ("true in 1 of 1 evaluations", "UNGROUNDED"),
                          "§3.1": ("REFUSED at evaluation 2 (INDEX-OUT-OF-RANGE), after 1 true: not held",
                                   "UNGROUNDED")},
}
OTHERWISE_EXACT = ('    if st is site.stmt or (isinstance(st, RawIf) and st.kind == "otherwise" and st.then is site.stmt'
                   '):\n', "    if st is site.stmt:\n")


def r8_rows(arb):
    """The court's R8: an evaluation that refused is not held, and the rule only ever withholds. Every row reads R8 at
    panel's shipped default, the value orl.py reads; only the plant passes r8=False (the reporting pass's finding 1)."""
    def readings(name, off=False, court=COURT):
        comp, w, ref = arb.arbitrate(read("tests/fixtures/r8/" + name), "r8-" + name[:-4])
        seals = court.claim_seals(comp)
        ledger = [{"kind": "claim", "claim_seal": s, "note": FIXTURE, "_line": i + 1}
                  for i, s in enumerate(seals.values())]
        rec = parse_receipt(ref.receipt())
        p = court.panel(comp, w, rec, ledger, r8=False) if off else court.panel(comp, w, rec, ledger)
        return w, {r["clause"]: r for r in p["rows"]}
    for name, want in R8_EXPECTED.items():
        w, rows = readings(name)
        got = {k: (rows[k]["evaluation"], rows[k]["grounding"]) for k in want if k in rows}
        ok = (len(w["agreeing"]) == len(arb.backends) and all(
            k in got and got[k][0].startswith(v[0]) and got[k][1] == v[1] for k, v in want.items()))
        row(ok, "court R8: %s, every claim's seal ratified, agreed on [%s]: %s" % (
            name, ",".join(w["agreeing"]), "; ".join("%s %s, %s" % (k, got[k][0], got[k][1]) for k in sorted(got))),
            "" if ok else str(got))
    w, rows = readings("omit.orl", off=True)
    plant("court-counts-only-finished-evaluations (R8 off)", rows["§2.1"]["grounding"] == "GROUNDED",
          "with R8 off, omit.orl's claim reads %s, %s over a run REFUSED at that claim" % (
              rows["§2.1"]["evaluation"], rows["§2.1"]["grounding"]))
    w, rows = readings("otherwise_claim.orl", court=planted("src/orlog/court.py", [OTHERWISE_EXACT]))
    plant("r8-otherwise-read-as-possible", rows["§2.2"]["evaluation"].startswith("REFUSED at its clause"),
          "under the predicate before finding 15, the Otherwise clause's claim reads 'REFUSED at its clause ... the "
          "refusal may come from the condition or the other arm', which that clause does not have")
    r = run_python(os.path.join(ROOT, "tests", "court_monotone.py"), "--jobs", "8")
    m = re.search(r"^COURT R8 ONE-SIDED: (\d+) gained, (\d+) lost \(frozen texts (\d+), fixtures (\d+); "
                  r"cycle_refusal.orl (\d+)\)", r.stdout, re.M)
    plants_caught = [re.search(r"^plant %s .*: CAUGHT," % n, r.stdout, re.M) is not None
                     for n in ("standing-without-circular", "court-grants-a-refuted-claim")]
    ok = r.returncode == 0 and m is not None and m.group(1) == "0" and all(plants_caught)
    row(ok, "court R8 is one-sided: over COMPAT-0's frozen texts and the court's fixtures, %s standings gained, %s lost "
        "(frozen texts %s, a coverage gap: none refuses inside a claim; fixtures %s, cycle_refusal.orl's two moves out "
        "of CIRCULAR among them), every changed reading counted, and both plants caught: a comparator blind to "
        "CIRCULAR, and a court that grants (tests/court_monotone.py)" % (
            m.group(1) if m else "?", m.group(2) if m else "?", m.group(3) if m else "?", m.group(4) if m else "?"),
        "" if ok else (r.stdout[-600:] + r.stderr[-300:]))


ORDER_CASES = [         # SPEC §13, within a statement: each text holds two faults, the first written is reported
    ("Let: its expression before its name", ["§1 Let x be 1.", "§2 Let x be y."], "UNDECLARED"),
    ("item I of X: I before X", ["§1 Define r as 1.", "§2 Say item \"a\" of r."], "TYPE"),
    ("Set item I of X: I before X", ["§1 Set item \"a\" of nothere to 2."], "TYPE"),
    ("Set item I of X: X before the value", ["§1 For each i from 1 to 2, do the following.",
                                             "§1.1 Set item 1 of i to nothere."], "LOOP-VARIABLE"),
    ("Append E to X: E before X", ["§1 For each i from 1 to 2, do the following.", "§1.1 Append nothere to i."],
     "UNDECLARED"),
    ("While: the condition before the bound", ["§1 While nothere, at most 0 times, do the following.", "§1.1 Say 1."],
     "UNDECLARED"),
    ("For: from before to", ["§1 For each i from nothere to 2.5, do the following.", "§1.1 Say i."], "UNDECLARED"),
    ("For: the bounds before the counter", ["§1 Let i be 1.", "§2 For each i from 1 to nothere, do the following.",
                                            "§2.1 Say 1."], "UNDECLARED"),
    ("Define: the references before the value", ["§1 Notwithstanding §9, define r as nothere."], "UNKNOWN-CLAUSE"),
    ("Define: the name before the value", ["§1 Define go as nothere.", "§2 To go, do the following.", "§2.1 Say 1."],
     "REDECLARED"),
    ("Define: the value before the proviso", ["§1 Define r as nothere, provided that alsonot."], "UNDECLARED"),
    ("and: both operands before its check", ["§1 Say \"a\" and nothere."], "UNDECLARED"),
    ("quotient: both operands before its check", ["§1 Say the quotient of \"a\" by nothere."], "UNDECLARED"),
    ("a claim: the condition before the target", ["§1 We claim that nothere, by the certificate of §9."],
     "UNDECLARED"),
    ("To: the place before the name", ["§1 Let go be 1.", "§2 If true, do the following.",
                                       "§2.1 To go, do the following.", "§2.1.1 Say 1."], "PROCEDURE-PLACE"),
]


def order_misses():
    bad = []
    for what, lines, want in ORDER_CASES:
        c = compile_bytes(prog(*lines))
        got = "accepted" if c.ok else c.error.code
        if got != want:
            bad.append("%s: %s, not %s" % (what, got, want))
    return bad


def order_rows():
    bad = order_misses()
    row(not bad, "spec: within a statement, written order, post-order (SPEC §13): %d texts of two faults each report "
        "the one written first" % len(ORDER_CASES), "; ".join(bad))
    # the plant: the order before §13, which looked up X before typing I in 'item I of X'
    saved = SEMA.Analysis._expr

    def old_item_order(self, c, e):
        if isinstance(e, SEMA.Item):
            vi = self.lookup_var(c, e.list)
            if not SEMA.is_list(vi.type):
                self.err("TYPE", c, "'%s' is not a list" % e.list)
            e.var = vi
            self.want(c, e.index, "int")
            return vi.type[1]
        return saved(self, c, e)
    SEMA.Analysis._expr = old_item_order
    try:
        planted = order_misses()
    finally:
        SEMA.Analysis._expr = saved
    plant("item-target-before-index", bool(planted), "under the pre-§13 order: %s" % "; ".join(planted))


E21_GROW = ["§1 Let t be \"x\".", "§2 For each i from 1 to 22, do the following.", "§2.1 Set t to t followed by t.",
            "§3 For each k from 1 to %d, do the following.", "§3.1 Set t to t followed by \"\".", "§4 Say \"done\"."]
E21_LISTS = ["§1 Let xs be a list of 1000000 copies of 1.", "§2 Let ys be a list of 1 copies of 0.",
             "§3 For each k from 1 to %d, do the following.", "§3.1 Set ys to xs.", "§4 Say the length of ys."]
E21_UNRELEASED = "while (orl__tmp_n > mark) free(orl__tmp[--orl__tmp_n]);"


def child_peak(cmd, cwd):
    """(exit status, peak memory in bytes) of one child process: peak commit on Windows; elsewhere the children's
    peak resident size, which is a maximum over every child so far (so the larger run is measured last)."""
    import subprocess
    if os.name == "nt":
        import ctypes
        import ctypes.wintypes as wt

        class PMC(ctypes.Structure):
            _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t), ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()
        pmc = PMC()
        pmc.cb = ctypes.sizeof(PMC)
        ok = ctypes.windll.psapi.GetProcessMemoryInfo(wt.HANDLE(int(p._handle)), ctypes.byref(pmc), pmc.cb)
        return p.returncode, (pmc.PeakPagefileUsage if ok else -1)
    import resource
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    return r.returncode, kb if sys.platform == "darwin" else kb * 1024


def e21_peaks(plant, template):
    """Peak memory of the C backend on a program run with 4, then 32 rebuilds (red team E21, rt_c finding 8)."""
    import shutil
    import subprocess
    from orlog.arbiter import generate
    from orlog.lower import Lowered
    peaks = []
    for n in (4, 32):
        lines = [l % n if "%d" in l else l for l in template]
        src = generate("c99", Lowered(compile_bytes(prog(*lines))))
        if plant:
            assert E21_UNRELEASED in src
            src = src.replace(E21_UNRELEASED, "(void)mark;")
        tmp = tempfile.mkdtemp(prefix="orlog-e21-")
        try:
            with open(os.path.join(tmp, "p.c"), "wb") as fh:
                fh.write(src.encode("utf-8"))
            subprocess.run(["clang"] + C_FLAGS + ["p.c", "-o", "p.exe"], cwd=tmp, capture_output=True)
            rc, pk = child_peak([os.path.join(tmp, "p.exe"), "out.bin", "receipt.txt"], tmp)
            peaks.append((rc, pk))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return peaks


def e21_rows(arb, backends):
    """The C runtime's text ownership (red team E21): the fixtures agree four ways, and memory stays flat."""
    for p in sorted(os.listdir(os.path.join(ROOT, "tests", "fixtures", "e21"))):
        comp, w, ref = arb.arbitrate(read("tests/fixtures/e21/" + p), "e21-" + p)
        ok = comp.ok and not w["dissenting"] and len(w["agreeing"]) == len(arb.backends)
        row(ok, "E21 %s: runs byte-identically on the reference and [%s]" % (p, ",".join(w.get("agreeing", []))),
            "" if ok else str(w.get("refusal") or w.get("mismatch_notes"))[:300])
    if "c99" not in backends:
        return
    MB = 1 << 20
    (r1, a), (r2, b) = e21_peaks(False, E21_GROW)
    (r3, c), (r4, e) = e21_peaks(False, E21_LISTS)
    ok = r1 == r2 == r3 == r4 == 0 and 0 < a and 0 < c and b - a < 16 * MB and e - c < 16 * MB
    row(ok, "memory: the C backend's peak is flat as a run rebuilds a 4 MiB text 4 and then 32 times (%d and %d MiB) "
        "and stores a 1,000,000-item list 4 and then 32 times (%d and %d MiB); red team E21 and rt_c finding 8: it "
        "grew by every text and list a run made" % (a // MB, b // MB, c // MB, e // MB),
        "exit %d, %d, %d, %d" % (r1, r2, r3, r4))
    (r1, a), (r2, b) = e21_peaks(True, E21_GROW)
    (r3, c), (r4, e) = e21_peaks(True, E21_LISTS)
    caught = r1 == r2 == r3 == r4 == 0 and b - a >= 16 * MB and e - c >= 16 * MB
    plant("c99-temporaries-never-released", caught, "with the temporaries never released, as before the repair, "
          "the text run's peak grows from %d to %d MiB and the list run's from %d to %d MiB"
          % (a // MB, b // MB, c // MB, e // MB))


SPEC_CODE_RE = re.compile(r"`([A-Z][A-Z0-9-]+)`")


def spec_phase_codes():
    """The codes in SPEC.md §13's phase table (its third column)."""
    with open(os.path.join(ROOT, "SPEC.md"), "rb") as fh:
        text = fh.read().decode("utf-8")
    sec = text[text.index("\n## 13."):]
    sec = sec[:sec.index("\n## ", 1)]
    codes = set()
    for line in sec.split("\n"):
        cells = line.split("|")
        if line.startswith("| ") and len(cells) == 5 and not line.startswith("| phase "):
            codes.update(SPEC_CODE_RE.findall(cells[3]))
    return codes


def source_codes(extra=""):
    """The compile refusal codes the front end can raise, read from its source: the door's REFUSE events, and every
    OrlogError and err call with a literal code. sema's err(code) passes its code through (callers are scanned)."""
    codes = set()
    with open(os.path.join(ROOT, "src", "orlog", "canon.py"), "rb") as fh:
        codes.update(re.findall(r'ev\("REFUSE", "([A-Z0-9-]+)"', fh.read().decode("utf-8")))
    texts = [extra]
    for name in ("syntax.py", "sema.py", "front.py"):
        with open(os.path.join(ROOT, "src", "orlog", name), "rb") as fh:
            texts.append(fh.read().decode("utf-8"))
    for t in texts:
        codes.update(re.findall(r'(?:OrlogError|err)\("([A-Z][A-Z0-9-]+)"', t))
    return codes


def spec_rows():
    """The specification held to the code: the twin's hand-worked probes, and SPEC §13's phase table."""
    sys.path.insert(0, os.path.join(ROOT, "tests"))
    import compare_probes
    same, kept, diffs, total, error = compare_probes.compare()
    row(error is None and not diffs and same + len(kept) == total, "spec: the twin's %d hand-worked probes: %d met "
        "as the twin worked them, %d as SPEC §13 settled them against the twin's reading (twin/probes/settled.json), "
        "%d different" % (total, same, len(kept), len(diffs)), error or "; ".join(d[0] for d in diffs))
    same, kept, diffs, total, error = compare_probes.compare(folder="probes3")
    row(error is None and not diffs and same + len(kept) == total, "spec: the twin's %d round-3 probes (SPEC §12, §13): "
        "%d met as the twin worked them, %d as SPEC §14 settled them against the twin's reading "
        "(twin/probes3/settled.json), %d different" % (total, same, len(kept), len(diffs)),
        error or "; ".join(d[0] for d in diffs))
    table, raised = spec_phase_codes(), source_codes()
    row(table == raised and len(raised) > 40, "spec: SPEC §13's phase table lists exactly the %d compile refusal codes "
        "the front end can raise" % len(raised), "only in the table: %s; only in the code: %s" % (
            sorted(table - raised), sorted(raised - table)))
    planted = source_codes(extra='raise OrlogError("STATEMENT-PERIOD", self.line, "")')
    plant("front-end-raises-an-unlisted-code", planted != table, "a front end raising STATEMENT-PERIOD (as the line "
          "pass did before §13) differs from the table by %s" % sorted(planted - table))


def law_plants(arb):
    """Plants in the law itself: the claims must discriminate, not merely run."""
    src = read("examples/gcd_certificate.orl")
    planted = src.replace("§10 Let g be old_r.".encode("utf-8"), "§10 Let g be old_r times 2.".encode("utf-8"))
    comp, w, ref = arb.arbitrate(planted, "plant-law-gcd")
    st = w.get("reference", {}).get("status", "")
    cid = comp.prog.by_label["12"].id if comp.ok else -1
    plant("law-gcd-wrong-answer (g doubled)", comp.ok and st == "REFUSED CLAIM-REFUTED %d" % cid and
          len(w["agreeing"]) == len(arb.backends),
          "the Bezout certificate refuses at §12 in the reference and [%s]: %s" % (",".join(w.get("agreeing", [])), st))
    src = read("examples/leapfrog.orl")
    old = "§9.1.1 Set item i of x to item i of x plus item i of v times h.".encode("utf-8")
    new = "§9.1.1 Set item i of x to item i of x plus (item i of v plus 0.0000000003) times h.".encode("utf-8")
    planted = src.replace(old, new)
    comp, w, ref = arb.arbitrate(planted, "plant-law-leapfrog")
    st = w.get("reference", {}).get("status", "")
    cid = comp.prog.by_label["17"].id if comp.ok else -1
    plant("law-leapfrog-asymmetric-drift (a bias not symmetric under negation)",
          planted != src and comp.ok and st == "REFUSED CLAIM-REFUTED %d" % cid and
          len(w["agreeing"]) == len(arb.backends),
          "exact return fails and the reversibility claim refuses at §17 in the reference and [%s]: %s"
          % (",".join(w.get("agreeing", [])), st))


CODEGEN_PROBE = r'''
import hashlib, os, sys
sys.path.insert(0, os.path.join(sys.argv[1], "src"))
from orlog.front import compile_bytes
from orlog.lower import Lowered
from orlog.arbiter import generate
h = hashlib.sha256()
for p in sys.argv[2:]:
    comp = compile_bytes(open(p, "rb").read())
    low = Lowered(comp)
    for b in ("python", "c99", "rust"):
        h.update(generate(b, low).encode("utf-8"))
    h.update(comp.law)
print(h.hexdigest())
'''


def codegen_rows():
    import subprocess
    paths = [os.path.join(ROOT, p) for p in corpus()]
    digests = []
    for seed in ("0", "424242"):
        env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONUTF8="1")
        r = subprocess.run([sys.executable, "-B", "-c", CODEGEN_PROBE, ROOT] + paths, capture_output=True, text=True,
                           env=env)
        digests.append(r.stdout.strip() or r.stderr.strip()[-200:])
    row(digests[0] == digests[1] and len(digests[0]) == 64,
        "codegen: the law bytes and all three generated sources for the corpus are identical under PYTHONHASHSEED "
        "0 and 424242 (sha256 %s)" % digests[0][:16])


def firewall_rows():
    try:
        witness_artifact({"valid": True})
        row(False, "firewall: a verdict-shaped key in a witness is refused")
    except ValueError:
        row(True, "firewall: a verdict-shaped key in a witness is refused (executable-epistemics)")


# ------------------------------------------------------------------ the reporting layer (the reporting pass, 2026-10-26)
ORL = planted("orl.py", [])                    # orl.py as a module, so its printed reading can be read in process
COURT_PY, ARBITER_PY = "src/orlog/court.py", "src/orlog/arbiter.py"
HELD = '        held = hit is None and r["evals"] > 0 and r["trues"] == r["evals"] and agreed\n'
AGREE_CORE = 'ok = (r.get("receipt") is not None and receipt_core(r["receipt"]) == ref_core and ref_core is not None'
AGREE_COND = 'and r.get("out") == bytes(ref.out) and r.get("exit") == 0)'
PY_RECEIPT = r'fh.write(("\n".join(lines) + "\n").encode("ascii"))'
PY_FINISH = '        self._receipt("COMPLETED")\n        _sys.exit(0)'
PY_CLOSE = '        self.out.close()\n        if self.trace is not None:\n            self.trace.close()'
PY_MUTANTS = {          # a Python backend that breaks one agreement condition, made through the arbiter's mutate hook
    "a CR LF receipt": (PY_RECEIPT, r'fh.write(("\r\n".join(lines) + "\r\n").encode("ascii"))'),
    "a receipt without its final LF": (PY_RECEIPT, r'fh.write(("\n".join(lines)).encode("ascii"))'),
    "a receipt with a second backend line": (
        PY_RECEIPT, r'fh.write(("\n".join(lines[:2] + ["backend extra"] + lines[2:]) + "\n").encode("ascii"))'),
    "an exit status of 5 after a whole run": (PY_FINISH, '        self._receipt("COMPLETED")\n        _sys.exit(5)'),
    "bytes added to its output after the receipt": (PY_CLOSE, '        self.out.write(b"planted extra bytes\\n")\n' +
                                                    PY_CLOSE),
}
STAND_IN_C = (b'#include <stdio.h>\n#include <string.h>\nint main(int argc, char **argv) {\n'
              b'    for (int i = 1; i < argc; i++) if (strcmp(argv[i], "--version") == 0) {\n'
              b'        puts("clang version 0.0.0 (a self-test stand-in that builds nothing)"); return 0; }\n'
              b'    return 1;\n}\n')


def py_mutant(old, new):
    def m(b, src):
        if b != "python":
            return src
        if src.count(old) != 1:
            raise AssertionError("a mutant's anchor occurs %d times in the generated source" % src.count(old))
        return src.replace(old, new)
    return m


def orl_cli(*args, orl=None, court=None):
    """orl.py's main in this process: (its exit status, or 'TRACEBACK <type>', and what it printed). orl: a planted
    copy of orl.py; court: a planted court module whose panel and ledger reader the command uses."""
    import io
    m = orl or ORL
    saved = (m.panel, m.read_ledger, m.LedgerBroken)
    if court is not None:
        m.panel, m.read_ledger, m.LedgerBroken = court.panel, court.read_ledger, court.LedgerBroken
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = m.main([str(x) for x in args])
    except SystemExit as e:                 # argparse's own exit
        code = e.code
    except Exception as e:
        code = "TRACEBACK " + type(e).__name__
    finally:
        m.panel, m.read_ledger, m.LedgerBroken = saved
    return code, buf.getvalue()


def all_ratified(comp):
    return [{"kind": "claim", "claim_seal": s, "note": FIXTURE, "_line": i + 1}
            for i, s in enumerate(COURT.claim_seals(comp).values())]


def reporting_rows(arb, workdir, backends):
    """The reporting pass's findings (research/reporting-pass/FINDINGS.md): each reporter that said more than its run
    is held by a row, and each row by the plant that is the regression the pass planted (2026-10-26)."""
    fixture = lambda name: os.path.join(ROOT, "tests", "fixtures", "court", name)
    collatz = os.path.join(ROOT, "examples", "collatz.orl")
    every, first = ",".join(backends), backends[0]
    wd = ["--workdir", workdir]

    # 1. R8 at panel's shipped default, as orl.py reads it
    def r8_cli(court=None):
        code, out = orl_cli("court", os.path.join(ROOT, "tests", "fixtures", "r8", "omit.orl"), "--backends", every,
                            *wd, court=court)
        return code == 0 and "REFUSED at evaluation 17 (INDEX-OUT-OF-RANGE), after 16 true: not held (R8)" in out
    row(r8_cli(), "court R8 as orl.py reads it: omit.orl's claim reads REFUSED at evaluation 17 at panel's shipped "
        "default, which no row sets (the reporting pass's finding 1)")
    plant("r8-default-off", not r8_cli(planted(COURT_PY, [("ledger=(), r8=True):", "ledger=(), r8=False):")])),
          "with panel's default flipped, orl.py court reads omit.orl's claim true in 16 of 16 evaluations, so the "
          "row's REFUSED at evaluation 17 is absent")

    # 2. R1: no claim held unless every backend agreed, and the sandwich says why
    contested = Arbiter(workdir, backends=backends, reference_patch=reference_truncates_quotient)
    comp_c, w_c, ref_c = contested.arbitrate(read(fixture("contested_true.orl")), "rep-contested")
    rec_c, led_c = parse_receipt(ref_c.receipt()), all_ratified(comp_c)

    def contested_ok(court):
        p = court.panel(comp_c, w_c, rec_c, led_c)
        return (w_c["dissent_kind"] != "NONE" and p["summary"]["sandwich"] == "VACUOUS (the backends did not all "
                "agree)" and all(r["support"] == "UNSUPPORTED" and r["grounding"] == "UNGROUNDED" for r in p["rows"]))
    row(contested_ok(COURT), "court R1: a claim true in every execution, its seal ratified, reads UNSUPPORTED and "
        "UNGROUNDED when the backends dissent (%s), and the sandwich says the backends did not all agree (finding 2)"
        % w_c["dissent_kind"])
    incomplete_ok = None
    if "c99" in backends:
        unbuilt = Arbiter(workdir, backends=backends, mutate=mutate_with("c99", lambda s: s + "\nthis is not C\n"))
        comp_i, w_i, ref_i = unbuilt.arbitrate(read(fixture("contested_true.orl")), "rep-incomplete")
        rec_i, led_i = parse_receipt(ref_i.receipt()), all_ratified(comp_i)

        def incomplete_ok(court):
            p = court.panel(comp_i, w_i, rec_i, led_i)
            return (w_i["build_failed"] == ["c99"] and p["summary"]["sandwich"].startswith("VACUOUS (not every")
                    and all(r["support"] == "UNSUPPORTED" and r["grounding"] == "UNGROUNDED" for r in p["rows"]))
        row(incomplete_ok(COURT), "court R1: the same claim reads UNSUPPORTED and UNGROUNDED when a backend did not "
            "build (integrity INCOMPLETE) (finding 2)")
    unguarded = planted(COURT_PY, [(HELD, HELD.replace(" and agreed\n", "\n"))])
    plant("held-ignores-integrity", not contested_ok(unguarded) and (incomplete_ok is None or
                                                                      not incomplete_ok(unguarded)),
          "with integrity dropped from 'held', the claim reads WELL-FOUNDED and GROUNDED over a run whose backends "
          "did not all agree, so the R1 row%s fail%s" % (("s", "") if incomplete_ok else ("", "s")))
    blind = planted(COURT_PY, [('    elif not agreed:\n        sandwich = "VACUOUS (the backends did not all agree)"\n',
                                "")])
    plant("sandwich-ignores-dissent", not contested_ok(blind), "without its dissent branch the sandwich reads 'VACUOUS "
          "(no claim is well-founded)', a reason that is not the run's, so the R1 row fails")

    # 3. a refuted claim is not held
    comp_r, w_r, ref_r = arb.arbitrate(read(fixture("refuted_claim.orl")), "rep-refuted")
    rec_r, led_r = parse_receipt(ref_r.receipt()), all_ratified(comp_r)

    def refuted_ok(court):
        p = court.panel(comp_r, w_r, rec_r, led_r)
        r = p["rows"][0]
        return (len(w_r["agreeing"]) == len(backends) and r["evaluation"].startswith("REFUTED at evaluation 1 ")
                and r["support"] == "UNSUPPORTED" and r["grounding"] == "UNGROUNDED"
                and p["summary"]["sandwich"].startswith("VACUOUS") and p["summary"]["refuted"] == 1)
    row(refuted_ok(COURT), "court: a refuted claim, its seal ratified, reads UNSUPPORTED and UNGROUNDED and the sandwich "
        "VACUOUS, the reference and [%s] agreeing (finding 3)" % ",".join(w_r["agreeing"]))
    plant("held-ignores-refutation", not refuted_ok(planted(COURT_PY, [(HELD, HELD.replace(
        ' and r["trues"] == r["evals"]', ""))])), "with refutation dropped from 'held', the refuted claim reads "
          "WELL-FOUNDED and GROUNDED beside its REFUTED evaluation, so the row fails")

    # 4, 5 and 16. the arbiter's four agreement conditions, each through a backend that breaks only it, and the witness
    if "python" in backends:
        def arbitrate_mutant(arbiter_cls, mutant):
            a = arbiter_cls(workdir, backends=("python",), mutate=py_mutant(*PY_MUTANTS[mutant]))
            return a.arbitrate(read("examples/collatz.orl"), "rep-agree")[1]
        mutants = {m: arbitrate_mutant(Arbiter, m) for m in PY_MUTANTS}
        for m, w in mutants.items():
            row(w["dissent_kind"] == "BACKEND-DISSENT" and w["dissenting"] == ["python"],
                "arbiter: a Python backend with %s reads BACKEND-DISSENT, in the verdict itself (findings 4, 5)" % m,
                w["dissent_kind"])
        lenient = planted(ARBITER_PY, [(AGREE_CORE, 'ok = (r.get("receipt") is not None and parse_receipt(r["receipt"]'
                                                    ') == parse_receipt(ref.receipt())')]).Arbiter
        framing = ("a CR LF receipt", "a receipt without its final LF", "a receipt with a second backend line")
        passed = [m for m in framing if arbitrate_mutant(lenient, m)["dissent_kind"] == "NONE"]
        plant("arbiter-lenient-receipts (in the verdict)", len(passed) == 3, "with the pre-E7 comparison (lines split "
              "on any line end, every backend line dropped) put back in the verdict, %d of the 3 framing mutants read "
              "NONE, so their rows fail" % len(passed))
        no_exit = planted(ARBITER_PY, [(AGREE_COND, 'and r.get("out") == bytes(ref.out))')]).Arbiter
        plant("agreement-ignores-exit", arbitrate_mutant(no_exit, "an exit status of 5 after a whole run")[
            "dissent_kind"] == "NONE", "without the exit condition the backend that exits 5 reads NONE, so its row "
              "fails")
        no_out = planted(ARBITER_PY, [(AGREE_COND, 'and r.get("exit") == 0)')]).Arbiter
        plant("agreement-ignores-output", arbitrate_mutant(no_out, "bytes added to its output after the receipt")[
            "dissent_kind"] == "NONE", "without the output condition the backend whose output grew after its receipt "
              "reads NONE, so its row fails")

        def hashes_ok(w):
            h = w["reference"].get("receipt_core_sha256")
            return h is not None and bool(w["agreeing"]) and all(
                w["backends"][b].get("receipt_core_sha256") == h for b in w["agreeing"])
        comp_h, w_h, ref_h = arb.arbitrate(read("examples/collatz.orl"), "rep-hashes")
        crlf = mutants["a CR LF receipt"]
        note = (crlf["mismatch_notes"] or [{}])[0].get("detail", "")
        ok = hashes_ok(w_h) and crlf["backends"]["python"].get("receipt_core_sha256") is None and "frame" in note
        row(ok, "arbiter: the witness's receipt hashes are of the receipt's core, the reference's equal to [%s]'s, a "
            "CR LF dissent's none, and its note names the receipt's frame (finding 16)" % ",".join(w_h["agreeing"]),
            "" if ok else note)
        parsed = planted(ARBITER_PY, [('"receipt_core_sha256": sha(core) if core is not None else None}',
                                       '"receipt_core_sha256": sha("\\n".join(rec).encode()) if rec else None}')])
        w_old = parsed.Arbiter(workdir, backends=backends).arbitrate(read("examples/collatz.orl"), "rep-hashes")[1]
        plant("witness-hashes-parsed-lines", not hashes_ok(w_old), "with a backend's hash taken over its parsed lines, "
              "an agreeing run's hashes differ from the reference's, so the row fails")

    # 6. the run's own status in the printed reading, and the exit status over a failed build
    def status_ok(orl=None):
        code1, out1 = orl_cli("court", fixture("must_after_claim.orl"), "--backends", every, *wd, orl=orl)
        code2, out2 = orl_cli("court", fixture("hoisted_omit.orl"), "--backends", every, *wd, orl=orl)
        return (code1 == 0 and out1.startswith("run REFUSED MUST-FAILED at §3\n") and code2 == 0
                and out2.startswith("run REFUSED INDEX-OUT-OF-RANGE at §2.1\n"))
    row(status_ok(), "orl.py court prints the run's status first: REFUSED MUST-FAILED at §3 after a claim held, and "
        "REFUSED INDEX-OUT-OF-RANGE at §2.1, one clause before a claim that held 16 times (finding 6; whether such a "
        "claim stays held, and what a law's own refusal exits with, are the owner's to rule)")
    plant("court-prints-no-run-status", not status_ok(planted("orl.py", [('    print("run %s" % p["summary"]["run"])\n',
                                                                          "")])),
          "without its first line the reading of a refused run names no refusal, so the row fails")
    if "c99" in backends:
        def unbuilt_court(orl=None):
            saved = ARB.C_FLAGS
            ARB.C_FLAGS = saved + ["--orlog-no-such-flag"]
            try:
                return orl_cli("court", collatz, "--backends", "c99", *wd, orl=orl)
            finally:
                ARB.C_FLAGS = saved
        code, out = unbuilt_court()
        row(code == 2 and "integrity INCOMPLETE (did not build: c99)" in out, "orl.py court exits 2, as 'run' does, "
            "when a backend did not build, and prints integrity INCOMPLETE (did not build: c99) (finding 6)", str(code))
        exit_line = '    return 2 if (w["dissenting"] or w.get("build_failed") or w.get("stopped")) else 0\n'
        code, _ = unbuilt_court(planted("orl.py", [(exit_line, "    return 0\n")]))
        plant("court-exits-0-over-a-failed-build", code == 0, "with the exit before the repair, orl.py court exits 0 "
              "over an INCOMPLETE reading, so the row fails")

    # 7. a warm build cache never answers for a compiler that cannot build
    if "c99" in backends:
        standin = os.path.join(workdir, "stand-in")
        exe = os.path.join(standin, "clang.exe" if os.name == "nt" else "clang")
        if not os.path.exists(exe):
            os.makedirs(standin, exist_ok=True)
            with open(os.path.join(standin, "stand_in.c"), "wb") as fh:
                fh.write(STAND_IN_C)
            import subprocess
            subprocess.run(["clang", "-O0", "stand_in.c", "-o", os.path.basename(exe)], cwd=standin,
                           capture_output=True)

        def under_stand_in(arbiter_cls):
            arbiter_cls(workdir, backends=("c99",)).arbitrate(read("examples/collatz.orl"), "rep-cache")  # warm
            saved = os.environ.get("PATH", "")
            os.environ["PATH"] = standin + os.pathsep + saved
            try:
                return arbiter_cls(workdir, backends=("c99",)).arbitrate(read("examples/collatz.orl"), "rep-cache")[1]
            finally:
                os.environ["PATH"] = saved
        w = under_stand_in(Arbiter)
        row(os.path.exists(exe) and w["build_failed"] == ["c99"] and not w["agreeing"], "arbiter: with a stand-in "
            "compiler first on PATH that builds nothing, a warm cache does not answer for it: BUILD-FAILED, as from an "
            "empty folder (finding 7)", w["dissent_kind"])
        keyless = planted(ARBITER_PY, [
            ('key = sha((src + "\\0" + " ".join(flags) + ("\\0" + tool if tool else "")).encode("utf-8"))[:24]',
             'key = sha((src + "\\0" + " ".join(flags)).encode("utf-8"))[:24]'),
            ('if rec.get("toolchain") == tool and rec.get("exe_sha256") == file_sha(exe_abs):',
             'if rec.get("exe_sha256") == file_sha(exe_abs):')]).Arbiter
        w = under_stand_in(keyless)
        plant("cache-ignores-toolchain", w["agreeing"] == ["c99"], "with the toolchain out of the key and the record, "
              "the binary another compiler built answers for the stand-in, and the run reads %s, so the row fails"
              % w["dissent_kind"])
    if "python" in backends:
        from orlog.lower import Lowered
        src = ARB.generate("python", Lowered(compile_bytes(read("examples/collatz.orl"))))
        cached = os.path.join(workdir, "cache", "python-%s.py" % ARB.sha((src + "\0").encode("utf-8"))[:24])
        other = ARB.generate("python", Lowered(compile_bytes(read("examples/fall.orl")))).encode("utf-8")

        def tampered(arbiter_cls):
            with open(cached, "wb") as fh:
                fh.write(other)
            return arbiter_cls(workdir, backends=("python",)).arbitrate(read("examples/collatz.orl"), "rep-pycache")[1]
        w = tampered(Arbiter)
        row(w["agreeing"] == ["python"] and w["backends"]["python"]["build"].startswith("rewritten"), "arbiter: a "
            "cached Python source that is not this law's source is written again before it runs (finding 7)",
            w["backends"]["python"]["build"])
        trusting = planted(ARBITER_PY, [('        elif backend == "python":\n            with open(srcpath, "rb") as fh:',
                                         '        elif False:\n            with open(srcpath, "rb") as fh:')]).Arbiter
        w = tampered(trusting)
        plant("python-cache-runs-as-found", w["dissent_kind"] != "NONE", "without the check, the cached file runs "
              "another law's program and the run reads %s, so the row fails" % w["dissent_kind"])
        Arbiter(workdir, backends=("python",)).arbitrate(read("examples/collatz.orl"), "rep-pycache")  # left whole

    # 8. E10's class: both compilers refusing the 600-arm chain must fail the chain row
    if {"c99", "rust"} & set(backends):
        refusing = Arbiter(workdir, backends=backends, mutate=lambda b, s: s + "\n#error the E10 class\n" if b == "c99"
                           else (s + '\ncompile_error!("the E10 class");\n' if b == "rust" else s))
        ok, agreeing = chain_runs(refusing)
        plant("chain-600-refused-by-compilers", not ok, "with the compilers refusing the chain, it agrees on [%s] of "
              "[%s], so the chain row fails (finding 8)" % (",".join(agreeing), every))

    # 9. the summary counts each reason a claim is not held apart, and every count is its rows'
    texts = [("examples/plankton.orl", False), ("tests/fixtures/court/refuted_claim.orl", True),
             ("tests/fixtures/r8/omit.orl", True), ("tests/fixtures/r8/transitive.orl", True),
             ("tests/fixtures/r8/cycle_refusal.orl", True), ("tests/fixtures/court/unreached.orl", True)]
    runs = []
    for path, ratify in texts:
        comp, w, ref = arb.arbitrate(read(path), "rep-sum")
        runs.append((comp, w, parse_receipt(ref.receipt()), all_ratified(comp) if ratify else []))

    def summary_ok(court):
        sums = []
        for comp, w, rec, led in runs:
            p = court.panel(comp, w, rec, led)
            rows, s = p["rows"], p["summary"]
            want = {"claims": len(rows), "well_founded": sum(r["support"] == "WELL-FOUNDED" for r in rows),
                    "circular": sum(r["support"].startswith("CIRCULAR") for r in rows),
                    "unreached": sum(r["support"] == "UNREACHED" for r in rows),
                    "unsupported": sum(r["support"] == "UNSUPPORTED" for r in rows),
                    "refuted": sum(r["evaluation"].startswith("REFUTED") for r in rows),
                    "refused_evaluation": sum(r["evaluation"].endswith("(R8)") for r in rows),
                    "grounded": sum(r["grounding"] == "GROUNDED" for r in rows)}
            if any(s.get(k) != v for k, v in want.items()):
                return False
            sums.append(s)
        return sums[1]["refuted"] == 1 and sums[2]["refused_evaluation"] == 1 and sums[1] != sums[2]
    row(summary_ok(COURT), "court: the summary counts a refuted claim and an R8-withheld one apart (refuted, "
        "refused_evaluation), and every count equals its rows' on six texts (finding 9)")
    plant("summary-grounded-counts-all", not summary_ok(planted(COURT_PY, [
        ('"grounded": sum(1 for r in out if r["grounding"] == "GROUNDED"),', '"grounded": len(out),')])),
        "a summary counting every claim grounded differs from its rows, so the row fails")
    plant("summary-well-founded-counts-unsupported", not summary_ok(planted(COURT_PY, [
        ('"well_founded": sum(1 for r in out if r["support"] == "WELL-FOUNDED"),',
         '"well_founded": sum(1 for r in out if r["support"] in ("WELL-FOUNDED", "UNSUPPORTED")),')])),
        "a summary counting unsupported claims well-founded differs from its rows, so the row fails")

    # 10. a certificate's cost is not read over an evaluation R8 names
    comp_k, w_k, ref_k = arb.arbitrate(read(fixture("certificate_refused.orl")), "rep-cost")

    def cost_reading(court):
        return court.panel(comp_k, w_k, parse_receipt(ref_k.receipt()), [])["rows"][0]
    r = cost_reading(COURT)
    row(r["cost_reading"].startswith("NOT READ: evaluation 17 refused (R8)"), "court R4 over R8: a certificate whose "
        "17th evaluation refused reads NOT READ, not CHEAPER, since its line (%s) counts only the 16 finished "
        "evaluations (finding 10)" % r["cost"], r["cost_reading"])
    r = cost_reading(planted(COURT_PY, [("            if hit is not None:             # the receipt counts finished "
                                         "evaluations only (finding 10)\n", "            if False:\n")]))
    plant("cost-read-over-a-refused-evaluation", r["cost_reading"].startswith("CHEAPER"), "without the guard the "
          "withheld certificate reads %s from its finished evaluations, so the row fails" % r["cost_reading"][:7])

    # 13, 14. what orl.py court prints: the CONSTANT note, and the backends that agreed
    def constant_ok(orl=None):
        code, out = orl_cli("court", fixture("constant_claim.orl"), "--backends", first, *wd, orl=orl)
        blocks = re.split(r"\n(?=§)", out)
        b2 = [b for b in blocks if b.startswith("§2 ")]
        b3 = [b for b in blocks if b.startswith("§3 ")]
        return code == 0 and len(b2) == 1 and len(b3) == 1 and "CONSTANT" in b2[0] and "CONSTANT" not in b3[0]
    row(constant_ok(), "orl.py court prints the CONSTANT note for a claim that reads no variable, and not for one that "
        "reads the run (finding 13)")
    plant("court-prints-no-condition", not constant_ok(planted("orl.py", [('"evaluation", "condition", "theorem"',
                                                                            '"evaluation", "theorem"')])),
          "with the printed keys before the repair, the CONSTANT note is in the row and not on the screen")

    def names_ok(court=None):
        code, out = orl_cli("court", collatz, "--backends", first, *wd, court=court)
        line = next((l for l in out.splitlines() if l.startswith("integrity ")), "")
        others = [b for b in ("python", "c99", "rust") if b != first]
        return code == 0 and line == "integrity AGREED (the reference and %s)" % first and not any(
            b in line for b in others)
    row(names_ok(), "orl.py court names the backends that agreed: --backends %s reads AGREED (the reference and %s) and "
        "names no other (finding 14)" % (first, first))
    plant("integrity-names-no-backend", not names_ok(planted(COURT_PY, [
        ('        integrity = "AGREED (the reference and %s)" % ", ".join(names) if names else "AGREED"\n',
         '        integrity = "AGREED"\n')])), "an integrity of AGREED alone reads the same over one backend and "
          "three, so the row fails")

    # 17. a ledger line of the wrong shape fails closed, by the reader and by orl.py court
    shapes = [b'{"kind": "claim"}\n', b'{"kind": "theorem"}\n', b'{"kind": "claim", "claim_seal": ["x"]}\n']

    def ledger_ok(court):
        for i, body in enumerate(shapes):
            path = os.path.join(workdir, "rep-ledger-%d.jsonl" % i)
            with open(path, "wb") as fh:
                fh.write(body)
            try:
                court.read_ledger(path)
                return False
            except court.LedgerBroken as e:
                if not str(e).startswith("LEDGER-BROKEN at line 1"):
                    return False
            except Exception:
                return False
            code, out = orl_cli("court", collatz, "--ledger", path, "--backends", first, *wd, court=court)
            if code != 1 or not out.startswith("LEDGER-BROKEN at line 1"):
                return False
        return True
    row(ledger_ok(COURT), "ledger: a line that is a JSON object of the wrong shape (a claim without its seal, a "
        "theorem without its name, a seal that is a list) is refused LEDGER-BROKEN at line 1 by the reader and by "
        "'orl.py court' (exit 1, no traceback) (finding 17)")
    plant("ledger-reads-any-object", not ledger_ok(planted(COURT_PY, [(
        "        # its shape too, so that", '        e["_line"] = i\n        entries.append(e)\n        continue\n'
        "        # its shape too, so that")])), "a reader that keeps any object hands the panel a claim without its "
          "seal, so the row fails")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backends", default="python,c99,rust")
    a = ap.parse_args()
    backends = tuple(a.backends.split(","))
    workdir = os.path.join(ROOT, "build", "selftest")
    os.makedirs(workdir, exist_ok=True)
    arb = Arbiter(workdir, backends=backends)
    door_rows()
    seal_rows()
    spelling_rows()
    compile_refusal_rows()
    spec_rows()
    order_rows()
    firewall_rows()
    codegen_rows()
    corpus_rows(arb)
    runtime_refusal_rows(arb)
    court_rows(arb, workdir)
    redteam_rows(arb)
    redteam_v2_rows(arb, workdir, backends)
    e18_e22_rows(workdir)
    honesty_rows(workdir, backends)
    isolation_rows(backends)
    independence_rows(workdir, backends)
    compat_rows()
    r8_rows(arb)
    reporting_rows(arb, workdir, backends)
    e21_rows(arb, backends)
    law_plants(arb)
    backend_plants(workdir, backends)
    reference_dissent_plant(workdir, backends)
    passed = sum(1 for ok, _ in ROWS if ok)
    print("ORLOG SELFTEST %d/%d  (backends: %s)" % (passed, len(ROWS), ",".join(backends)))
    return 0 if passed == len(ROWS) else 1


if __name__ == "__main__":
    sys.exit(main())

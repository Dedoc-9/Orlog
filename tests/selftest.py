"""ORLOG SELFTEST: every self-claim gets a row; every guard gets a plant that must bite.

A row prints [PASS] or [FAIL]. A plant row names the planted defect and the witness that caught
it: the exact refusal, clause or divergent event the defect caused, not merely "something failed"
(the owner's kill-witness ruling: a catch needs a defect-specific causal witness). A plant that
changes nothing is reported EQUIVALENT and asserted to stay so (an honest miss, never counted caught).

  python tests/selftest.py [--backends python,c99,rust] [--quick]
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
from orlog.arbiter import Arbiter, C_FLAGS, witness_artifact, parse_receipt, receipt_core  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402

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
        ok = comp.ok and st.startswith("REFUSED %s " % code) and not w["dissenting"]
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
        "ends at %s after 3000 steps, against %s unfused (chaos magnifies one fused rounding)"
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
    plant("reference-quotient-truncates", ok, "dissent kind %s: [%s] agree with each other against the reference; "
          "the reference is still kept, by declaration" % (w["dissent_kind"], ",".join(w["dissenting"])))


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
    tall = ["§" + ".".join(["1"] * k) + " If true, do the following." for k in range(1, 25)]
    tall.append("§" + ".".join(["1"] * 25) + " Say 1.")
    c = compile_bytes(prog(*tall))
    row(not c.ok and c.error.code == "NESTING-DEPTH", "bounds: clauses 25 deep are refused NESTING-DEPTH",
        "" if not c.ok else "compiled")
    chain = ["§1 Let x be 599.", "§2 If x equals 0, say 0."]
    chain += ["§%d Otherwise, if x equals %d, say %d." % (k + 2, k, k) for k in range(1, 600)]
    comp, w, ref = arb.arbitrate(prog(*chain), "rt-chain-600")
    row(comp.ok and not w["dissenting"] and bytes(ref.out) == b"599\n",
        "bounds: a 600-arm If chain runs byte-identically on the reference and [%s] (constant-depth lowering)"
        % ",".join(w.get("agreeing", [])))


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

    def lenient(b):         # the comparison before E7: splitlines, every 'backend ' line dropped
        return "\n".join(l for l in b.decode("ascii", "replace").splitlines() if not l.startswith("backend "))
    survived = [lenient(x) == lenient(good) for x in (crlf, nolf, extra)]
    plant("arbiter-lenient-receipts", any(survived), "the pre-E7 comparison calls %d of the 3 malformed receipts "
          "agreeing, so the row fails under it" % sum(survived))
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
    ok = comp.ok and not comp.canon.events and bytes(ref.out) == want and not w["dissenting"]
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
    plant("law-gcd-wrong-answer (g doubled)", comp.ok and st == "REFUSED CLAIM-REFUTED %d" % cid and not w["dissenting"],
          "the Bezout certificate refuses at §12 in the reference and [%s]: %s" % (",".join(w.get("agreeing", [])), st))
    src = read("examples/leapfrog.orl")
    old = "§9.1.1 Set item i of x to item i of x plus item i of v times h.".encode("utf-8")
    new = "§9.1.1 Set item i of x to item i of x plus (item i of v plus 0.0000000003) times h.".encode("utf-8")
    planted = src.replace(old, new)
    comp, w, ref = arb.arbitrate(planted, "plant-law-leapfrog")
    st = w.get("reference", {}).get("status", "")
    cid = comp.prog.by_label["17"].id if comp.ok else -1
    plant("law-leapfrog-asymmetric-drift (a bias not symmetric under negation)",
          planted != src and comp.ok and st == "REFUSED CLAIM-REFUTED %d" % cid and not w["dissenting"],
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
    law_plants(arb)
    backend_plants(workdir, backends)
    reference_dissent_plant(workdir, backends)
    passed = sum(1 for ok, _ in ROWS if ok)
    print("ORLOG SELFTEST %d/%d  (backends: %s)" % (passed, len(ROWS), ",".join(backends)))
    return 0 if passed == len(ROWS) else 1


if __name__ == "__main__":
    sys.exit(main())

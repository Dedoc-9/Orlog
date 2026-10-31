"""LAW-SUFFICIENCY-0, test 3: an independent decoder (SHEET.md, test 3).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/test3_decoder.py

For every accepted text:
- the decoder D (decoder.py) reads the law bytes alone and builds what the interpreter runs;
- the decoded run's P must equal the parsed run's;
- sema.law_bytes of D's result must equal the bytes D read. The writer is used here only to check.
D's independence is checked from its source: what it imports, and that it is given nothing but bytes.

The plants run after the real pass:
- each parsed-path plant changes one structure the law bytes do not write, on every text that has it, and records:
  - that the law bytes are unchanged;
  - whether the parsed P changed;
  - whether the decoded P stayed as it was.
  A plant whose parsed P changes on no text is reported as equivalent on this set, measured, never assumed.
- two plants are in D itself."""
import ast
import os
import sys
from collections import Counter

import common
import decoder
from orlog.front import compile_bytes
from orlog.sema import law_bytes

ALLOWED_IMPORTS = {"struct"}
NODE_NAMES = {"Num", "Str", "BoolLit", "Var", "Bin", "Un", "Conv", "Item", "Length", "ListOf", "ListLit", "Seal", "Cat",
              "Let", "SetS", "Change", "Say", "IfS", "While", "For", "ProcDef", "Perform", "Must", "Claim", "Define",
              "Append", "RemoveLast", "Decimals"}
FORBIDDEN_NAMES = {"__import__", "importlib", "eval", "exec", "compile", "globals", "gc", "inspect", "sys", "open"}


def independence(source):
    """D's source against its rule: it imports struct and syntax.py's node classes, nothing else, and reaches for no
    module or object by name. Returns the breaches."""
    bad = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Import):
            bad += ["import %s" % a.name for a in n.names if a.name not in ALLOWED_IMPORTS]
        elif isinstance(n, ast.ImportFrom):
            if n.module != "orlog.syntax":
                bad.append("from %s import ..." % n.module)
            else:
                bad += ["from orlog.syntax import %s" % a.name for a in n.names if a.name not in NODE_NAMES]
        elif isinstance(n, ast.Name) and n.id in FORBIDDEN_NAMES:
            bad.append("the name %s" % n.id)
    return bad


def decoded(law, text_seal, budget):
    try:
        prog, an = decoder.decode(law)
    except Exception as e:
        return None, "DECODE-FAILED %s: %s" % (type(e).__name__, e)
    return (prog, an), common.run(prog, an, common.sha(law), text_seal, budget)


# ------------------------------------------------------------------ the parsed-path plants: (name, applies, change)
def drop_override_edge(comp):
    for name in sorted(comp.an.overrides):
        beats = comp.an.overrides[name]
        for a in sorted(beats):
            if beats[a]:
                b = min(beats[a])
                beats[a].discard(b)
                return "clause %d no longer beats clause %d (rule %r)" % (a, b, name)
    return None


def drop_claim_site(comp):
    if not comp.an.claims:
        return None
    site = comp.an.claims.pop()
    return "the last claim site (clause %d) dropped from an.claims" % site.id


def flip_cost_tracked(comp):
    for c in comp.prog.clauses:
        if c.cost_tracked:
            c.cost_tracked = False
            return "clause %d's cost_tracked set false" % c.id
    return None


def change_elem(comp):
    for c in comp.prog.clauses:
        for s in statements(c.stmt):
            if type(s).__name__ == "Change" and s.elem == "int":
                s.elem = "fix"
                return "clause %d's Change elem int made fix" % c.id
    return None


def reverse_rules(comp):
    hit = [n for n in sorted(comp.an.rules) if len(comp.an.rules[n]) > 1]
    for n in hit:
        comp.an.rules[n].reverse()
    return "an.rules reversed for %s" % hit if hit else None


def statements(s):
    """A statement and the inline statements of its arms and else."""
    if s is None:
        return []
    out = [s]
    if type(s).__name__ == "IfS":
        for _, b, _ in s.arms:
            if not (isinstance(b, tuple) and b[0] == "block"):
                out += statements(b)
        if s.els is not None and not (isinstance(s.els[0], tuple) and s.els[0][0] == "block"):
            out += statements(s.els[0])
    return out


PARSED_PLANTS = [
    ("an override edge removed from an.overrides", drop_override_edge, "changes"),
    ("a claim site dropped from an.claims", drop_claim_site, "changes"),
    ("cost_tracked flipped on a certificate's clause", flip_cost_tracked, "changes"),
    ("a Change's elem changed from int to fix", change_elem, "changes"),
    ("an.rules reversed", reverse_rules, "measured"),
]


def main():
    lines = []

    def say(s=""):
        lines.append(s)
        print(s, flush=True)

    texts = common.accepted()
    say("LAW-SUFFICIENCY-0, TEST 3: AN INDEPENDENT DECODER (research/law-sufficiency/test3_decoder.py)")
    src = open(os.path.join(common.HERE, "decoder.py"), encoding="utf-8").read()
    say("decoder.py sha256 %s" % common.sha(src.encode("utf-8")))
    breaches = independence(src)
    say("D's independence, from its source: %s" % ("held: it imports struct and syntax.py's node classes only, and "
                                                  "names no module or object to reach the parsed path" if not breaches
                                                  else "BREACHED %s" % breaches))
    say("the shared dependency this test does not attack: syntax.py's node classes, which D builds and the interpreter "
        "dispatches on by isinstance")
    say()
    decoder.SEEN.clear()
    rows, base = Counter(), {}
    fails = []
    for ident, kind, raw, budget in texts:
        comp = compile_bytes(raw)
        p_parsed = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget)
        got, p_dec = decoded(comp.law, comp.text_seal, budget)
        base[ident] = (p_parsed, p_dec)
        if got is None:
            rows["decode failed"] += 1
            fails.append("%s: %s" % (ident, p_dec))
            continue
        rows["decoded"] += 1
        rt = law_bytes(*got) == comp.law
        rows["round trip exact" if rt else "round trip differs"] += 1
        if not rt:
            fails.append("%s: the round trip differs" % ident)
        if p_dec == p_parsed:
            rows["P equal"] += 1
        else:
            rows["P differs"] += 1
            fails.append("%s: P differs, %s" % (ident, common.first_difference(p_parsed, p_dec)))
    say("== the decoded run against the parsed run, on %d texts" % len(texts))
    say("   %s" % ", ".join("%s %d" % kv for kv in sorted(rows.items())))
    for f in fails:
        say("   FAIL %s" % f)
    say("   what D was exercised on (forms decoded, over every text):")
    seen = sorted(decoder.SEEN.items())
    for k in range(0, len(seen), 6):
        say("     " + ", ".join("%s %d" % kv for kv in seen[k:k + 6]))
    never = sorted(set(["expr rounded", "expr as", "expr promote"]) - set(decoder.SEEN))
    say("   conversion forms the grammar has and no text exercised: %s" % (never or "none"))

    say()
    say("== plants in the parsed path: the law bytes fixed, one unsealed structure changed, on every text that has it")
    plant_ok = []
    for what, fn, expect in PARSED_PLANTS:
        applied = changed = dec_moved = law_moved = 0
        example = None
        for ident, kind, raw, budget in texts:
            comp = compile_bytes(raw)
            note = fn(comp)
            if note is None:
                continue
            applied += 1
            if law_bytes(comp.prog, comp.an) != comp.law:
                law_moved += 1
            p = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget)
            if p != base[ident][0]:
                changed += 1
                if example is None:
                    example = "%s: %s; %s" % (ident, note, common.first_difference(base[ident][0], p))
            _, p_dec = decoded(comp.law, comp.text_seal, budget)
            if p_dec != base[ident][1]:
                dec_moved += 1
        if expect == "changes":
            ok = applied > 0 and changed > 0 and dec_moved == 0 and law_moved == 0
            verdict = "CAUGHT" if ok else ("EQUIVALENT ON THIS SET" if applied and not changed else "NOT AS STATED")
        else:
            ok = applied > 0 and dec_moved == 0 and law_moved == 0
            verdict = "MEASURED: %s" % ("changes the parsed run on %d texts" % changed if changed
                                       else "equivalent on every text it applies to")
        plant_ok.append(ok)
        say("   %-48s applied to %3d texts; law bytes moved on %d; parsed P changed on %3d; decoded P moved on %d: %s"
            % (what, applied, law_moved, changed, dec_moved, verdict))
        if example:
            say("      e.g. %s" % example[:240])

    say()
    say("== plants in D")
    decoder.PLANT = "elem-ignores-index"
    try:
        n = moved = 0
        for ident, kind, raw, budget in texts:
            comp = compile_bytes(raw)
            _, p_dec = decoded(comp.law, comp.text_seal, budget)
            n += 1
            if p_dec != base[ident][0]:
                moved += 1
    finally:
        decoder.PLANT = None
    ok = moved > 0
    plant_ok.append(ok)
    say("   D derives a Change's elem without its index (the list's type): the decoded P differs from the parsed on %d "
        "texts: %s" % (moved, "CAUGHT" if ok else "EQUIVALENT ON THIS SET"))
    planted = src.replace("import struct\n", "import struct\nfrom orlog import sema\n", 1)
    b2 = independence(planted)
    ok = bool(b2)
    plant_ok.append(ok)
    say("   D's source given an import of sema (a reach into the parsed path): the independence check reports %s: %s"
        % (b2, "CAUGHT" if ok else "MISSED"))

    say()
    held = not breaches and not fails and all(plant_ok)
    say("TEST 3 %s: %d texts, decoded P equal on %d, round trip exact on %d, independence %s; plants %d of %d as stated"
        % ("HELD" if held else "FAILED", len(texts), rows["P equal"], rows["round trip exact"],
           "held" if not breaches else "breached", sum(plant_ok), len(plant_ok)))
    sys.exit(0 if held else 1)


if __name__ == "__main__":
    main()

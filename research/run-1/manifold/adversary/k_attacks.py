"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

Hand-made version-0 laws against CUT-0's continuation K, read through the probe's own `judge()`
(research/run-1/probes/cut0_claims.py), each also run through the dynamic continuation oracle (cont_oracle.py), which
is written apart from K and can only refute it.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/k_attacks.py

For each claim: the probe's reading (cut rule held or withheld), and whether some continuation evaluated it again
after the cut under S1 (one return) or S2 (every refusal returns). A claim the cut rule HOLDS and a continuation
evaluates again is a counterexample under that semantics; a claim it withholds that no tried continuation reaches is
only a candidate imprecision (the oracle under-approximates).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
sys.path.insert(0, HERE)
import cut0_claims as P                                                   # noqa: E402
from cont_oracle import witnesses                                         # noqa: E402
from orlog.front import compile_bytes                                     # noqa: E402

law = P.law

# (name, lines, the reading this adversary argues for, as {claim label: "held"|"withheld"} or None for no argument)
CASES = [
    # ---- rule uses (Define): a rule refused at its use names the using clause
    ("A01 rule undefined at a Say, pass 2 of 3, claim before", [
        "S1 Let x be 0.", "S2 Define r as 5, provided that x is less than 2.",
        "S3 For each i from 1 to 3, do the following.", "S3.1 We claim that i is positive.",
        "S3.2 Increase x by 1.", "S3.3 Say r."]),
    ("A02 rule undefined inside the claim's own condition, last pass", [
        "S1 Let x be 0.", "S2 Define r as 5, provided that x is less than 2.",
        "S3 For each i from 1 to 2, do the following.", "S3.1 Increase x by 1.", "S3.2 We claim that r is positive."]),
    ("A03 rule undefined in a For's upper bound; the body holds the claim, run once before", [
        "S1 Let x be 0.", "S2 Define r as 1, provided that x is zero.",
        "S3 To body, do the following.", "S3.1 We claim that x is at least 0.",
        "S4 For each i from 1 to r, do the following.", "S4.1 Perform body.",
        "S5 Increase x by 1.", "S6 For each j from 1 to r, do the following.", "S6.1 Perform body."]),
    ("A04 rule undefined in a While's condition after the last allowed pass", [
        "S1 Let x be 0.", "S2 Define r as x, provided that x is less than 2.",
        "S3 While r is less than 5, at most 2 times, do the following.", "S3.1 Increase x by 1.",
        "S3.2 We claim that x is positive."]),
    # ---- Musts
    ("A05 a Must fails on pass 2 of 3, claim before it", [
        "S1 For each i from 1 to 3, do the following.", "S1.1 We claim that i is positive.",
        "S1.2 It must hold that i is less than 2."]),
    ("A06 a Must fails on the last pass, claim before it", [
        "S1 For each i from 1 to 3, do the following.", "S1.1 We claim that i is positive.",
        "S1.2 It must hold that i is less than 3."]),
    ("A07 a Must in a procedure performed twice fails in the second call; claim between the calls", [
        "S1 Let x be 0.", "S2 To guard, do the following.", "S2.1 It must hold that x is zero.",
        "S3 Perform guard.", "S4 We claim that x is zero.", "S5 Increase x by 1.", "S6 Perform guard."]),
    # ---- otherwise-if chains
    ("A08 refusal in an Otherwise-if condition, last pass; claim in a later arm, run earlier", [
        "S1 Let xs be a list of 2 copies of 0.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 If i equals 2, say i.", "S2.2 Otherwise, if item i of xs equals 1, say 0.",
        "S2.3 Otherwise, we claim that i is positive."]),
    ("A09 refusal in an Otherwise-if condition, last pass; claim in the first arm, run earlier", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 If i equals 2, we claim that i is positive.", "S2.2 Otherwise, if item i of xs equals 1, say 0.",
        "S2.3 Otherwise, say 1."]),
    ("A10 a three-arm chain whose third arm's block refuses on the last pass; claim in arm two", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 If i equals 1, say 1.", "S2.2 Otherwise, if i equals 2, we claim that i is positive.",
        "S2.3 Otherwise, do the following.", "S2.3.1 Say item i of xs."]),
    # ---- inline Perform in an If arm
    ("A11 inline Perform in the If arm of a loop, refusal inside it on the last pass", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 Let k be 0.", "S3 To look, do the following.",
        "S3.1 Increase k by 1.", "S3.2 We claim that k is positive.", "S3.3 Say item k of xs.",
        "S4 For each i from 1 to 3, do the following.", "S4.1 If i is positive, perform look."]),
    ("A12 inline Perform in an inline otherwise arm; the other arm's procedure holds the claim", [
        "S1 Let x be 0.", "S2 To good, do the following.", "S2.1 We claim that x is at least 0.",
        "S3 To bad, do the following.", "S3.1 Say 1 divided by x.",
        "S4 For each i from 1 to 2, do the following.", "S4.1 If i equals 1, perform good; otherwise, perform bad."]),
    ("A13 inline Perform in an Otherwise-if arm, refusal inside, pass 2 of 3", [
        "S1 Let x be 0.", "S2 To good, do the following.", "S2.1 We claim that x is at least 0.",
        "S3 To bad, do the following.", "S3.1 Say 1 divided by x.",
        "S4 For each i from 1 to 3, do the following.", "S4.1 If i equals 1, perform good.",
        "S4.2 Otherwise, if i equals 2, perform bad.", "S4.3 Otherwise, perform good."]),
    # ---- procedures from loops; nested procedures
    ("A14 a procedure performed from a loop and after it; refusal in the loop's last pass", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 Let k be 0.", "S3 To step, do the following.",
        "S3.1 Increase k by 1.", "S3.2 We claim that k is positive.", "S3.3 Say item k of xs.",
        "S4 For each i from 1 to 3, do the following.", "S4.1 Perform step.", "S5 Perform step."]),
    ("A15 nested procedures, the inner performed by two outers, the second outer refuses", [
        "S1 Let x be 1.", "S2 To inner, do the following.", "S2.1 We claim that x is positive.",
        "S3 To first, do the following.", "S3.1 Perform inner.", "S4 To second, do the following.",
        "S4.1 Set x to x minus 1.", "S4.2 Say 1 divided by x.", "S4.3 Perform inner.",
        "S5 Perform first.", "S6 Perform second."]),
    ("A16 a procedure performed in a While of fuel 2, refusing on the 2nd pass after the claim", [
        "S1 Let x be 0.", "S2 To step, do the following.", "S2.1 Increase x by 1.", "S2.2 We claim that x is positive.",
        "S2.3 Say 1 divided by (2 minus x).", "S3 While x is less than 9, at most 2 times, do the following.",
        "S3.1 Perform step."]),
    # ---- For bounds
    ("A17 a For whose upper bound refuses, the body run by an earlier For", [
        "S1 Let x be 0.", "S2 For each i from 1 to 2, do the following.", "S2.1 We claim that i is positive.",
        "S3 For each j from 1 to 1 divided by x, do the following.", "S3.1 We claim that j is positive."]),
    ("A18 a nested For whose bound refuses on the outer's last pass; the claim in the inner body", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 For each j from 1 to item i of xs, do the following.", "S2.1.1 We claim that j is positive."]),
    ("A19 a For with expression bounds lo > hi on the last pass of the outer", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 For each j from i to 2, do the following.", "S2.1.1 We claim that j is positive.",
        "S2.2 Say item i of xs."]),
    # ---- a refusal in an If condition on a loop's last pass
    ("A20 If condition refuses on the last pass; claim before the If", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 We claim that i is positive.", "S2.2 If item i of xs equals 1, say i."]),
    ("A21 If condition refuses on the last pass; claim in its arm, run earlier", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 For each i from 1 to 3, do the following.",
        "S2.1 If item i of xs equals 1, we claim that i is positive."]),
    # ---- a refusal in a procedure performed from an Otherwise arm
    ("A22 a refusal in a procedure performed from a block Otherwise arm, called twice", [
        "S1 Let x be 2.", "S2 To probe, do the following.", "S2.1 Say 1 divided by (x minus 1).",
        "S3 To look, do the following.", "S3.1 If x equals 5, say 0.", "S3.2 Otherwise, do the following.",
        "S3.2.1 We claim that x is positive.", "S3.2.2 Perform probe.", "S4 Perform look.", "S5 Set x to 1.",
        "S6 Perform look."]),
    # ---- claims sharing a clause
    ("A23 two claims on one clause (cond literal true): the second claim, the otherwise arm's, open on the last pass", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 Let c be true.", "S3 For each i from 1 to 3, do the following.",
        "S3.1 If (i equals 1) equals c, we claim that item i of xs equals 1; otherwise, we claim that item i of xs "
        "equals 1."]),
    ("A23' the same law, one literal apart (cond literal false): the first claim, the If arm's, open", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 Let c be false.", "S3 For each i from 1 to 3, do the following.",
        "S3.1 If (i equals 1) equals c, we claim that item i of xs equals 1; otherwise, we claim that item i of xs "
        "equals 1."]),
    # ---- a While whose condition refuses
    ("A24 While condition refuses with fuel left; claim in body", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 Let k be 0.",
        "S3 While item (k plus 1) of xs equals 1, at most 5 times, do the following.", "S3.1 Increase k by 1.",
        "S3.2 We claim that k is positive."]),
    ("A25 While condition refuses with the fuel spent (2 of 2 passes made)", [
        "S1 Let xs be a list of 2 copies of 1.", "S2 Let k be 0.",
        "S3 While item (k plus 1) of xs equals 1, at most 2 times, do the following.", "S3.1 Increase k by 1.",
        "S3.2 We claim that k is positive."]),
    # ---- the fuel bit against C6 (the probe's own case, as its benign twin)
    ("C6 the probe's case: FUEL-EXHAUSTED at the 4th check", P.FUEL if False else [
        "S1 Let i be 0.", "S2 While i is less than 10, at most 3 times, do the following.", "S2.1 Increase i by 1.",
        "S2.2 We claim that i is positive, by the owner."]),
    ("A26 C6 with a refusal on the 3rd (last fuelled) pass, after the claim: d = 0", [
        "S1 Let i be 0.", "S2 Let d be 0.", "S3 While i is less than 10, at most 3 times, do the following.",
        "S3.1 Increase i by 1.", "S3.2 We claim that i is positive, by the owner.",
        "S3.3 If i equals 3, say 1 divided by d."]),
    ("A26' the same law, one literal apart: d = 1 (no refusal on pass 3; FUEL-EXHAUSTED at the 4th check)", [
        "S1 Let i be 0.", "S2 Let d be 1.", "S3 While i is less than 10, at most 3 times, do the following.",
        "S3.1 Increase i by 1.", "S3.2 We claim that i is positive, by the owner.",
        "S3.3 If i equals 3, say 1 divided by d."]),
    ("A27 a refusal on the 3rd pass whose next check would refute the claim (claim i is at most 3)", [
        "S1 Let i be 0.", "S2 Let d be 0.", "S3 While i is less than 10, at most 3 times, do the following.",
        "S3.1 Increase i by 1.", "S3.2 We claim that i is at most 3, by the owner.",
        "S3.3 If i equals 3, say 1 divided by d."]),
    ("A27' one literal apart: d = 1, the 4th check refuses FUEL-EXHAUSTED", [
        "S1 Let i be 0.", "S2 Let d be 1.", "S3 While i is less than 10, at most 3 times, do the following.",
        "S3.1 Increase i by 1.", "S3.2 We claim that i is at most 3, by the owner.",
        "S3.3 If i equals 3, say 1 divided by d."]),
]


def main():
    bad_s1 = bad_s2 = cand = 0
    descs = {}
    for name, lines in CASES:
        raw = law(*lines)
        comp = compile_bytes(raw)
        if not comp.ok:
            print("%s\n   DOES NOT COMPILE: %s" % (name, comp.error))
            continue
        status, out, desc = P.judge(raw)
        wit = witnesses(comp, refuted=True)
        descs[name.split(" ")[0]] = (desc, out)
        print("%s\n   run %s; cut [%s]" % (name, status, desc))
        for k, (lab, ev, built, site, cut, done) in sorted(out.items()):
            s1, s2 = k in wit["S1"], k in wit["S2"]
            r1, r2 = k in wit["S1-refuted"], k in wit["S2-refuted"]
            flag = ""
            if cut and s1:
                flag, bad_s1 = "   <- UNSOUND under S1 (held, yet a one-return continuation evaluates it)", bad_s1 + 1
            elif cut and s2:
                flag, bad_s2 = "   <- UNSOUND under S2 (held, yet an every-return continuation evaluates it)", bad_s2 + 1
            elif done and not cut and not s1 and not s2:
                flag, cand = "   <- withheld; no tried continuation reaches it (candidate imprecision)", cand + 1
            elif done and not cut and not s1:
                flag = "   <- withheld; under S1 no tried continuation reaches it (imprecise under S1 only)"
            print("   claim %d %s %s: as built %s; site %s; cut %s; evaluated after the cut: S1 %s, S2 %s%s" % (
                k, lab, ev, *("held" if v else "withheld" for v in (built, site, cut)),
                ("yes, refuted" if r1 else "yes") if s1 else "no", ("yes, refuted" if r2 else "yes") if s2 else "no",
                flag))
    print("== descriptor pairs: equal cut descriptors, different readings")
    for a, b in (("A23", "A23'"), ("A26", "A26'"), ("A27", "A27'")):
        (da, oa), (db, ob) = descs[a], descs[b]
        ra = tuple(v[4] for _, v in sorted(oa.items()))
        rb = tuple(v[4] for _, v in sorted(ob.items()))
        print("   %s [%s] %s / %s [%s] %s: descriptors %s, readings %s" % (
            a, da, ra, b, db, rb, "EQUAL" if da == db else "differ", "differ" if ra != rb else "equal"))
    print("K-ATTACKS: %d unsound under S1, %d unsound under S2 (and not S1), %d candidate imprecisions" % (
        bad_s1, bad_s2, cand))


if __name__ == "__main__":
    main()

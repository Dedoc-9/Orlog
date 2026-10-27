"""RESEARCH SCRIPT (the manifold debate's proponent, 2026-10-26). Writes the regression laws under laws/, in binary,
LF line ends, UTF-8. Each is a version-0 law; resume_oracle.py's REGRESSION table holds what each must read, worked
by hand (PROPONENT.md, section 4).

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/make_laws.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LAWS = os.path.join(HERE, "laws")
NOTE = "Note: FIXTURE written by research/run-1/manifold/make_laws.py; not a person's act. "

LAWS_TEXT = {
    # precision: a later refusal that is certain stops every R1 resumption before the claim; K ignores it
    "later-refusal.orl": ["the claim is withheld by CUT-0 although no R1 resumption evaluates it again.",
                          "S1 Let x be 0.", "S2 For each i from 1 to 2, do the following.",
                          "S2.1 We claim that x is at least 0.", "S2.2 Say 1 divided by x.", "S2.3 Say 1 divided by x."],
    # precision: a guard no remaining pass satisfies (the adversary's D08, smaller)
    "guard.orl": ["the claim is withheld by CUT-0 although no remaining pass satisfies its guard.",
                  "S1 Let x be 0.", "S2 For each i from 1 to 3, do the following.",
                  "S2.1 If i equals 1, we claim that x is at least 0.", "S2.2 Say 2 divided by (2 minus i)."],
    # beyond CUT-0's definition: K's While bit relies on the next fuel check refusing
    "fuel-bit.orl": ["CUT-0 holds the claim; only a resumption that also returns from FUEL-EXHAUSTED evaluates it again.",
                     "S1 Let x be 0.", "S2 While x is less than 9, at most 2 times, do the following.",
                     "S2.1 Increase x by 1.", "S2.2 We claim that x is positive.", "S2.3 Say 6 divided by (x minus 2)."],
    # fuel-bit one literal apart (9 -> 2): the first form holds both, reading S2 withholds both; only fuel-bit's claim
    # is ever evaluated again, so here S2's withholding is its price, the While's condition unread
    "s2-price.orl": ["fuel-bit one literal apart: reading S2 withholds the claim, and no resumption evaluates it again.",
                     "S1 Let x be 0.", "S2 While x is less than 2, at most 2 times, do the following.",
                     "S2.1 Increase x by 1.", "S2.2 We claim that x is positive.", "S2.3 Say 6 divided by (x minus 2)."],
    # K reads a refuted claim as open; harmless, since a refuted claim is never held
    "refuted-open.orl": ["the refuted claim is in K as an open evaluation, though its evaluation completed.",
                         "S1 Let x be 0.", "S2 We claim that x is positive."],
    # the adversary's F2 in this script's vocabulary: one descriptor, two cuts; x = 0 and x = 2, one literal apart
    "desc-alias-0.orl": ["with alias-2, one cut descriptor for two cuts whose open claims differ.", "S1 Let x be 0.",
                         "S2 For each i from 1 to 3, do the following.",
                         "S2.1 If i equals 1 plus x, we claim that 6 divided by (3 minus i) is positive; otherwise, we "
                         "claim that 6 divided by (3 minus i) is positive."],
    "desc-alias-2.orl": ["with alias-0, one cut descriptor for two cuts whose open claims differ.", "S1 Let x be 2.",
                         "S2 For each i from 1 to 3, do the following.",
                         "S2.1 If i equals 1 plus x, we claim that 6 divided by (3 minus i) is positive; otherwise, we "
                         "claim that 6 divided by (3 minus i) is positive."],
    # one law per unsound plant of K, each its minimised witness
    "plant-no-open.orl": ["the claim's own evaluation is open at the cut; it completes in every resumption.",
                          "S1 Let x be 0.", "S2 We claim that (x minus 0) divided by (x minus 0) equals 1."],
    "plant-header-bit.orl": ["FUEL-EXHAUSTED at the While's own check, its bit says no passes remain; the check "
                             "guarded a third pass.", "S1 Let x be 0.",
                             "S2 While x is less than 3, at most 2 times, do the following.",
                             "S2.1 We claim that x is at least 0."],
    "plant-top-after-missing.orl": ["the rest of the refusing clause's block follows it.", "S1 Let x be 0.",
                                    "S2 Let y be 1.", "S3 Set y to (x minus 0) divided by (x minus 0).",
                                    "S4 We claim that x is at least 0."],
    "plant-outer-loop-never.orl": ["a For with a pass left runs its body again.", "S1 Let x be 0.", "S2 Let y be 1.",
                                   "S3 Increase x by 1.", "S4 For each i from 1 to 2, do the following.",
                                   "S4.1 We claim that x is at least 0.",
                                   "S4.2 Set y to (x minus 1) divided by (x minus 1)."],
    "plant-if-first-arm.orl": ["an If whose condition refused may run its Otherwise arm.", "S1 Let x be 0.",
                               "S2 If (x minus 0) divided by (x minus 0) equals 1, do the following.",
                               "S2.1 Increase x by 1.", "S3 Otherwise, do the following.",
                               "S3.1 We claim that x is less than 0."],
    "plant-proc-empty.orl": ["a Perform in the continuation runs the procedure's body.", "S1 Let x be 0.",
                             "S2 Let y be 1.", "S3 To p, do the following.", "S3.1 We claim that x is at least 0.",
                             "S4 Set y to (x minus 0) divided by (x minus 0).", "S5 Perform p."],
    "plant-else-missing.orl": ["an If chain after the cut may take its Otherwise arm.", "S1 Let x be 0.",
                               "S2 While x is less than 3, at most 2 times, do the following.",
                               "S2.1 Increase x by 1.", "S3 If x is even, do the following.", "S3.1 Increase x by 1.",
                               "S4 Otherwise, do the following.", "S4.1 We claim that x is at least 0."],
    "plant-no-return.orl": ["a procedure refused inside returns to its caller, and the caller goes on.",
                            "S1 Let x be 0.", "S2 Let y be 1.", "S3 To p, do the following.",
                            "S3.1 Set y to (x minus 0) divided by (x minus 0).", "S4 Perform p.",
                            "S5 We claim that x is at least 0."],
}


def main():
    os.makedirs(LAWS, exist_ok=True)
    for name, lines in sorted(LAWS_TEXT.items()):
        text = NOTE + lines[0] + "\n" + "".join(("§" + l[1:]) + "\n" for l in lines[1:])
        with open(os.path.join(LAWS, name), "wb") as fh:
            fh.write(text.encode("utf-8"))
        print("wrote laws/%s (%d clauses)" % (name, len(lines) - 1))


if __name__ == "__main__":
    main()

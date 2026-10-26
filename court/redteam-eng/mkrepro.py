"""Writes every reproducer .orl as exact bytes (UTF-8, LF only) into court/redteam-eng/.

  python -B mkrepro.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mkdeep  # noqa: E402

S = "§"


def lines(*ls):
    return "\n".join(ls) + "\n"


R = {
    "E1_eq_promotion_crash.orl": lines(S + "1 Let x be 0.5.", S + "2 Say x + 1 = 1.5."),
    "E1b_eq_note_twice.orl": lines(S + "1 Let x be 0.5.", S + "2 Say x = 0.1."),
    "E2a_rule_in_procedure.orl": lines(S + "1 Define r as 5.", S + "2 To show, do the following.",
                                       S + "2.1 Say r.", S + "3 Perform show."),
    "E2b_rule_uses_rule.orl": lines(S + "1 Define r as 5.", S + "2 Define s as r plus 1.", S + "3 Say s."),
    "E3_hidden_children.orl": lines(S + "1 Let x be 1.", S + "2 If x = 2, say \"two\".",
                                    S + "3 Otherwise, say \"not two\".", S + "3.1 Say \"hidden child\"."),
    "E3b_hidden_children_crash.orl": lines(S + "1 Let x be 1.", S + "2 If x = 2, say \"two\".",
                                           S + "3 Otherwise, say \"not two\".", S + "3.1 Let y be 5."),
    "E4_court_inline_claim.orl": lines(S + "1 Let x be 1.", S + "2 If x = 1, we claim that x = 1."),
    "E5_court_tautology_certificate.orl": lines(S + "1 Let x be 3.", S + "2 Let y be x times x.",
                                                S + "3 We claim that true, by the certificate of " + S +
                                                "2 under the theorem \"T\"."),
    "E6_court_recompute_certified.orl": lines(S + "1 Let x be 3.", S + "2 Let y be 0.",
                                              S + "3 For each k from 1 to 2, do the following.",
                                              S + "3.1 Set y to x times x times x times x.",
                                              S + "4 We claim that y = x times x times x times x, by the certificate of "
                                              + S + "3.1 under the theorem \"T\"."),
    "E9_door_curly_in_literal.orl": lines(S + "1 Say \"Use “followed by” to join\"."),
    "E10_python_depth_if_chain_110.orl": mkdeep.chain(110),
    "E10b_python_depth_nested_for_40.orl": mkdeep.nested_for(40),
    "E10c_lowering_recursion_if_chain_3000.orl": mkdeep.chain(3000),
    "E10d_sema_recursion_nested_for_400.orl": mkdeep.nested_for(400),
    "E12_huge_float_literal.orl": lines(S + "1 Decimals are floats.", S + "2 Let x be 1" + "0" * 400 + ".0.",
                                        S + "3 Say x."),
    "E13_two_seals.orl": lines(S + "1 Say 1.", "Sealed: babab-babab-babab-babab.", "Sealed: sutiv-kapol-rigog-pamit."),
    "E13b_note_after_seal.orl": lines(S + "1 Say 1.", "Sealed: sutiv-kapol-rigog-pamit.", "Note: written after the seal."),
    "E14_define_both_provisos.orl": lines(S + "1 Let x be 1.",
                                          S + "2 Define r as 1, provided that x = 1, unless x = 2.", S + "3 Say r."),
    "E15_two_oracles.orl": lines(S + "1 Let x be 2.", S + "2 We claim that x = 2, by the owner, by computation."),
    "E16a_upper_to.orl": lines(S + "1 TO greet, DO THE FOLLOWING.", S + "1.1 Say \"hi\".", S + "2 Perform greet."),
    "E16b_to_two_spaces.orl": lines(S + "1 To greet,  do the following.", S + "1.1 Say \"hi\".", S + "2 Perform greet."),
    "E16c_nested_to.orl": lines(S + "1 Let x be 1.", S + "2 If x = 1, do the following.",
                                S + "2.1 To greet, do the following.", S + "2.1.1 Say \"hi\"."),
    "E16d_to_named_to.orl": lines(S + "1 To to greet, do the following.", S + "1.1 Say \"hi\".",
                                  S + "2 Perform to greet."),
    "E17a_kelvin_identifier.orl": lines(S + "1 Let Key be 1.", S + "2 Say Key."),
    "E17b_greek_question_mark.orl": lines(S + "1 Let x be 1.", S + "2 If x = 1, say \"a\"; otherwise, say \"b\"."),
    "E19_invisible_in_literal.orl": lines(S + "1 Say \"payㅤ\U000E0041 to\"."),
    "E20a_labels_plain.orl": lines(S + "1 Let x be 1.", S + "2 We claim that x = 1.",
                                   S + "3 We claim that x is positive, given " + S + "2."),
    "E20b_labels_leading_zero.orl": lines(S + "1 Let x be 1.", S + "02 We claim that x = 1.",
                                          S + "3 We claim that x is positive, given " + S + "02."),
}

if __name__ == "__main__":
    for name, text in R.items():
        with open(os.path.join(HERE, name), "wb") as fh:
            fh.write(text.encode("utf-8"))
    # E18: a line the door maps to a text that is not its own fixed point (raw bytes, no final newline)
    with open(os.path.join(HERE, "E18_door_not_idempotent.raw"), "wb") as fh:
        fh.write(" Note:\" \"".encode("utf-8"))
    with open(os.path.join(HERE, "E5-fixture-ledger.jsonl"), "wb") as fh:
        fh.write(b'{"by": "red-team fixture", "kind": "theorem", "name": "T", "note": "FIXTURE written by the '
                 b'red-team for an unrelated program; not a person\'s act"}\n')
    print("wrote %d reproducers" % (len(R) + 2))

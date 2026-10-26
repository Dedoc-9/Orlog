"""Runs every reproducer's exact command from R (the orlog folder) and saves what it printed to observed/.

  python -B court/redteam-eng/run_all.py            (from R; PYTHONHASHSEED=0 and PYTHONUTF8=1 are set here)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(HERE, "..", ".."))
OBS = os.path.join(HERE, "observed")
RT = "court/redteam-eng"
WD = RT + "/work"
PY = [sys.executable, "-B"]
REF = ("import sys; sys.path.insert(0, 'src'); from orlog.front import compile_bytes; from orlog.interp import Interp; "
       "c = compile_bytes(open(sys.argv[1], 'rb').read()); i = Interp(c.prog, c.an, c.law_seal, c.text_seal).run(); "
       "sys.stdout.write('reference status %s, output %r' % (i.status, bytes(i.out).decode()) + chr(10))")
LAW = ("import sys; sys.path.insert(0, 'src'); from orlog.front import compile_bytes; "
       "c = compile_bytes(open(sys.argv[1], 'rb').read()); sys.stdout.write(c.law.decode())")

CMDS = [
    ("E1", PY + ["orl.py", "run", RT + "/E1_eq_promotion_crash.orl", "--backends", "python,c99", "--workdir", WD]),
    ("E1b", PY + ["orl.py", "check", RT + "/E1b_eq_note_twice.orl"]),
    ("E2a", PY + ["orl.py", "run", RT + "/E2a_rule_in_procedure.orl", "--backends", "python,c99", "--workdir", WD]),
    ("E2a-ref", PY + ["-c", REF, RT + "/E2a_rule_in_procedure.orl"]),
    ("E2b-ref", PY + ["-c", REF, RT + "/E2b_rule_uses_rule.orl"]),
    ("E2b", PY + ["orl.py", "run", RT + "/E2b_rule_uses_rule.orl", "--backends", "python,c99", "--workdir", WD]),
    ("E3", PY + ["orl.py", "run", RT + "/E3_hidden_children.orl", "--backends", "python,c99,rust", "--workdir", WD,
                 "--show"]),
    ("E3-law", PY + ["-c", LAW, RT + "/E3_hidden_children.orl"]),
    ("E3b", PY + ["orl.py", "check", RT + "/E3b_hidden_children_crash.orl"]),
    ("E4", PY + ["orl.py", "court", RT + "/E4_court_inline_claim.orl", "--workdir", WD, "--ledger",
                 RT + "/E5-fixture-ledger.jsonl"]),
    ("E5", PY + ["orl.py", "court", RT + "/E5_court_tautology_certificate.orl", "--workdir", WD, "--ledger",
                 RT + "/E5-fixture-ledger.jsonl"]),
    ("E6", PY + ["orl.py", "court", RT + "/E6_court_recompute_certified.orl", "--workdir", WD, "--ledger",
                 RT + "/E5-fixture-ledger.jsonl"]),
    ("E7", PY + [RT + "/arbiter_plants.py"]),
    ("E8", PY + [RT + "/arbiter_masking.py"]),
    ("E9", PY + ["orl.py", "run", RT + "/E9_door_curly_in_literal.orl", "--backends", "python,c99", "--workdir", WD,
                 "--show"]),
    ("E9-check", PY + ["orl.py", "check", RT + "/E9_door_curly_in_literal.orl"]),
    ("E10", PY + ["orl.py", "run", RT + "/E10_python_depth_if_chain_110.orl", RT + "/E10b_python_depth_nested_for_40.orl",
                  "--backends", "python,c99,rust", "--workdir", WD]),
    ("E10-stderr", PY + [RT + "/show_stderr.py", RT + "/E10_python_depth_if_chain_110.orl"]),
    ("E10c", PY + ["orl.py", "run", RT + "/E10c_lowering_recursion_if_chain_3000.orl", "--backends", "c99",
                   "--workdir", WD]),
    ("E10d", PY + ["orl.py", "check", RT + "/E10d_sema_recursion_nested_for_400.orl"]),
    ("E11", PY + ["orl.py", "run", "examples/collatz.orl", "--backends", "python,c99,rust", "--workdir",
                  WD + "/ØRLǪG"]),
    ("E11-c99", PY + [RT + "/e11_c_stderr.py"]),
    ("E12", PY + ["orl.py", "check", RT + "/E12_huge_float_literal.orl"]),
    ("E13", PY + ["orl.py", "check", RT + "/E13_two_seals.orl"]),
    ("E13b", PY + ["orl.py", "check", RT + "/E13b_note_after_seal.orl"]),
    ("E14", PY + ["orl.py", "check", RT + "/E14_define_both_provisos.orl"]),
    ("E15", PY + ["orl.py", "check", RT + "/E15_two_oracles.orl"]),
    ("E15-law", PY + ["-c", LAW, RT + "/E15_two_oracles.orl"]),
    ("E16a", PY + ["orl.py", "check", RT + "/E16a_upper_to.orl"]),
    ("E16b", PY + ["orl.py", "check", RT + "/E16b_to_two_spaces.orl"]),
    ("E16c", PY + ["orl.py", "check", RT + "/E16c_nested_to.orl"]),
    ("E16d", PY + ["orl.py", "check", RT + "/E16d_to_named_to.orl"]),
    ("E17a", PY + ["orl.py", "run", RT + "/E17a_kelvin_identifier.orl", "--backends", "python,c99", "--workdir", WD,
                   "--show"]),
    ("E17a-check", PY + ["orl.py", "check", RT + "/E17a_kelvin_identifier.orl"]),
    ("E17b-check", PY + ["orl.py", "check", RT + "/E17b_greek_question_mark.orl"]),
    ("E18", PY + [RT + "/door_retraction.py"]),
    ("E19", PY + ["orl.py", "check", RT + "/E19_invisible_in_literal.orl"]),
    ("E20a", PY + ["orl.py", "check", RT + "/E20a_labels_plain.orl"]),
    ("E20b", PY + ["orl.py", "check", RT + "/E20b_labels_leading_zero.orl"]),
    ("E21", PY + [RT + "/memleak.py"]),
    ("E22", PY + ["orl.py", "ratify", RT + "/E22_ratify_non_claim.orl", "--claim", "§1", "--note",
                  "red-team probe: is this a claim?", "--ledger", WD + "/E22-ledger.jsonl"]),
    ("E16e", PY + ["orl.py", "check", RT + "/E16e_to_no_space.orl"]),
    ("E16f", PY + ["orl.py", "check", RT + "/E16f_to_inner_spaces.orl"]),
    ("E20c", PY + ["orl.py", "check", RT + "/E20c_label_ref_as_integer.orl"]),
    ("E24", PY + ["orl.py", "run", RT + "/E24_python_depth_and_inside_loops.orl", RT + "/E24b_and_inside_loops_ok.orl",
                  "--backends", "python,c99,rust", "--workdir", WD]),
    ("E24-stderr", PY + [RT + "/show_stderr.py", RT + "/E24_python_depth_and_inside_loops.orl"]),
    ("E25", PY + ["orl.py", "check", RT + "/E25_parser_recursion_parens.orl"]),
    ("E25b", PY + ["orl.py", "check", RT + "/E25b_parser_recursion_and.orl"]),
    ("E18-fuzz", PY + [RT + "/doorfuzz.py", "30000", "5"]),
    ("E26", PY + ["orl.py", "check", RT + "/E26_false_door_note.orl"]),
    ("E23-spec", PY + ["-c", "import re; t = open('SPEC.md', encoding='utf-8').read(); "
                       "print({k: k in t for k in ('NESTING-DEPTH', 'LOOP-NESTING', 'QUOTE-BOUNDARY')})"]),
]


def main():
    os.makedirs(OBS, exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    only = set(sys.argv[1:])
    for name, cmd in CMDS:
        if only and name not in only:
            continue
        p = subprocess.run(cmd, cwd=R, env=env, capture_output=True)
        text = "$ " + " ".join(c if " " not in c else repr(c) for c in cmd[1:]) + "\n"
        text += p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
        text += "[exit %d]\n" % p.returncode
        with open(os.path.join(OBS, name + ".txt"), "wb") as fh:
            fh.write(text.encode("utf-8"))
        print("%-10s exit %d" % (name, p.returncode))
    return 0


if __name__ == "__main__":
    sys.exit(main())

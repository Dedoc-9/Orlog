"""Writes the door candidates as exact bytes (binary mode, LF only)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cand")

CASES = {
    # a curly pair inside an ASCII-delimited literal: the author's output text
    "c12_curly_inside_literal.orl": "§1 Say \"Use “followed by” to join\".\n",
    # U+212A KELVIN SIGN in an identifier; NFC maps it to ASCII K
    "c13_kelvin_identifier.orl": "§1 Let Key be 1.\n§2 Say Key.\n",
    # U+037E GREEK QUESTION MARK where the grammar wants ';'
    "c14_greek_question_mark.orl": "§1 Let x be 1.\n§2 If x = 1, say \"a\"; otherwise, say \"b\".\n",
    # invisible characters the literal check does not list: U+3164 HANGUL FILLER, U+E0041 TAG A, U+2028
    "c15_invisible_in_literal.orl": "§1 Say \"payㅤ\U000E0041 to\".\n",
    # U+2028 LINE SEPARATOR inside a Note (free text)
    "c16_linesep_in_note.orl": "Note: a §1 Say 2.\n§1 Say 1.\n",
}

os.makedirs(OUT, exist_ok=True)
for name, text in CASES.items():
    with open(os.path.join(OUT, name), "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("wrote", name)

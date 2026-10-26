#!/usr/bin/env python3
"""Write the §11 probes: twin/probes/NAME.orl, manifest.json, expected.json and EXPECTED.md.

Every expectation below was worked by hand from SPEC.md v0.1 (§11), not taken from the twin:
the twin is checked against these (python probe_run.py --check), never the other way round.
"reading": "11" means the expectation rests on §11 alone; "twin" means it also rests on a twin
reading of a point §11 leaves open, and "alt" gives the outcome under the other reading.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes")

DBL_MAX = (2 ** 53 - 1) * 2 ** 971
MID = 2 ** 1024 - 2 ** 970                     # halfway between DBL_MAX and 2^1024: ties to even = inf
assert float(str(MID) + ".0") == float("inf")
assert float(str(MID - 1) + ".0") == float(DBL_MAX)
TEN309 = "1" + "0" * 309 + ".0"
FIX_MAX = "2147483647.99999999976716935634613037109375"     # (2^63 - 1) / 2^32
SEAL = "lusab-lusab-lusab-lusab"                           # well formed; not the zero seal's words


def R(code):
    return {"refused": code}


def RUN(status="COMPLETED", out="", ops=0, events=0, claims=(), trace=None):
    d = {"status": status, "output": out, "ops": ops, "events": events, "claims": list(claims)}
    if trace is not None:
        d["trace"] = trace
    return d


P = []


def probe(name, items, what, text, expect, reading="11", alt=None):
    P.append(dict(name=name, items=items, what=what, text=text, expect=expect, reading=reading, alt=alt))


# ------------------------------------------------------------------ G3: the phase order
probe("g3-lines-before-syntax", ["G3"], "phase 2 (NUMBERING, line 2) before phase 3 (SYNTAX, clause 1)",
      "§1 Say 1 +.\n§3 Say 2.\n", R("NUMBERING"))
probe("g3-line-order-check", ["G3"], "phase 2 goes line by line: LINE-CHECK on line 1 before LINE-FORM on line 2",
      "§1 Say 1. [zzz]\nHello\n", R("LINE-CHECK"), "twin",
      "LINE-FORM, if phase 2's code list were passes over all lines")
probe("g3-line-order-numbering", ["G3"], "the same with NUMBERING on line 2 and LINE-FORM on line 3",
      "§1 Say 1.\n§3 Say 2.\nHello\n", R("NUMBERING"), "twin",
      "LINE-FORM, if phase 2's code list were passes over all lines")
probe("g3-syntax-before-shape", ["G3"], "phase 3 (SYNTAX, clause 2) before phase 4 (EMPTY-BLOCK, clause 1)",
      "§1 If true, do the following.\n§2 Say 1 +.\n", R("SYNTAX"))
probe("g3-unknown-procedure-before-shape", ["G3"], "UNKNOWN-PROCEDURE is phase 3, before phase 4's ORPHAN-OTHERWISE",
      "§1 Otherwise, say 1.\n§2 Fly away.\n", R("UNKNOWN-PROCEDURE"))
probe("g3-unknown-procedure-clause-order", ["G3"], "phase 3 goes clause by clause: UNKNOWN-PROCEDURE (clause 1) before SYNTAX (clause 2)",
      "§1 Fly away.\n§2 Say 1 +.\n", R("UNKNOWN-PROCEDURE"), "twin",
      "SYNTAX, if phase 3's code list were passes over all clauses")
probe("g3-procedure-name-clause-order", ["G3", "20"], "PROCEDURE-NAME (clause 1) before SYNTAX (clause 3), clause order",
      "§1 To the go, do the following.\n§1.1 Say 1.\n§2 Say 1 +.\n", R("PROCEDURE-NAME"), "twin",
      "SYNTAX, if phase 3's code list were passes over all clauses")
probe("g3-orphan-before-empty", ["G3"], "one clause both orphaned and empty: ORPHAN-OTHERWISE is listed first",
      "§1 Say 1.\n§2 Otherwise, do the following.\n", R("ORPHAN-OTHERWISE"))
probe("g3-shape-tree-order", ["G3"], "phase 4 in tree order: UNEXPECTED-CHILDREN (clause 1) before ORPHAN-OTHERWISE (clause 4)",
      "§1 Say 1.\n§1.1 Say 2.\n§2 Say 3.\n§3 Otherwise, say 4.\n", R("UNEXPECTED-CHILDREN"), "twin",
      "ORPHAN-OTHERWISE, if phase 4's code list were passes over the tree")
probe("g3-shape-preorder", ["G3"], "'tree order' as depth-first pre-order: the orphan at §1.1 comes before §2's children",
      "§1 If true, do the following.\n§1.1 Otherwise, say 1.\n§2 Say 2.\n§2.1 Say 3.\n", R("ORPHAN-OTHERWISE"), "twin",
      "UNEXPECTED-CHILDREN, if 'tree order' were breadth-first")
probe("g3-define-place-before-static", ["G3"], "phase 5 (DEFINE-PLACE, clause 3) before phase 6 (TYPE, clause 1)",
      "§1 Say 1 plus true.\n§2 If true, do the following.\n§2.1 Define r as 1.\n", R("DEFINE-PLACE"))
probe("g3-perform-order-is-static", ["G3", "22"], "PERFORM-BEFORE-DEFINITION is static (phase 6): phase 4's ORPHAN-OTHERWISE wins",
      "§1 Greet.\n§2 To greet, do the following.\n§2.1 Say 1.\n§3 Otherwise, say 2.\n", R("ORPHAN-OTHERWISE"))
probe("g3-static-before-cycle", ["G3"], "phase 6 (TYPE, clause 3) before phase 7 (PRIORITY-CYCLE)",
      "§1 Notwithstanding §2, define r as 1.\n§2 Notwithstanding §1, define r as 1.\n§3 Say 1 plus true.\n",
      R("TYPE"))
probe("g3-cycle-before-seal", ["G3"], "phase 7 (PRIORITY-CYCLE) before phase 8 (SEAL-MISMATCH)",
      "§1 Notwithstanding §1, define r as 1.\nSealed: %s.\n" % SEAL, R("PRIORITY-CYCLE"))
probe("g3-literal-range-is-static", ["G3", "38"], "LITERAL-RANGE (clause 1) is static semantics, so SYNTAX (clause 2) wins",
      "§1 Say 99999999999999999999.\n§2 Say 1 +.\n", R("SYNTAX"), "twin",
      "LITERAL-RANGE, if literals were range-checked while reading tokens (phase 3)")
probe("g3-let-expression-first", ["G3"], "Let x (REDECLARED) be y (UNDECLARED): the expression is checked first",
      "§1 Let x be 1.\n§2 Let x be y.\n", R("UNDECLARED"), "twin",
      "REDECLARED, if the declared name were checked before its expression")
probe("g3-syntax-then-lex", ["G3", "8"], "a misplaced token before an unreadable one: the first offending position decides",
      "§1 Say ) #.\n", R("SYNTAX"), "twin", "LEX, if a statement were read into tokens whole before parsing")
probe("g3-lex-then-syntax", ["G3", "8"], "an unreadable token before a misplaced one",
      "§1 Say 1 # 2.\n", R("LEX"), "twin", "SYNTAX, if unreadable characters were set aside until a parse succeeded")

# ------------------------------------------------------------------ G4: counting after operands
probe("g4-count-after-operands", ["G4"], "plus is counted after its operands, so the refusal inside them comes at ops 2",
      "§1 Say (7 divided by 0) plus 1.\n", RUN("REFUSED DIVISION-BY-ZERO 1", "", 2, 1))
probe("g4-rule-counts-first", ["G4", "6"], "a rule use counts before its provisos; the refusal names the using clause",
      "§1 Let z be 0.\n§2 Define r as 1, provided that 1 divided by z = 1.\n§3 Say r.\n",
      RUN("REFUSED DIVISION-BY-ZERO 3", "", 4, 2))

# ------------------------------------------------------------------ §1 lines
probe("n02-title-no-space", ["2"], "Title: takes any text, no space needed",
      "Title:Compact\n§1 Say 1.\n", RUN(out="1\n", ops=1, events=1))
probe("n02-title-empty", ["2"], "Title: with no text", "Title:\n§1 Say 1.\n", RUN(out="1\n", ops=1, events=1))
probe("n02-note-no-space", ["2"], "Note: takes any text", "Note:x\n§1 Say 1.\n", RUN(out="1\n", ops=1, events=1))
probe("n02-title-lowercase", ["2"], "prefixes are case-sensitive: 'title:' is no Title line",
      "title: x\n§1 Say 1.\n", R("LINE-FORM"))
probe("n02-sealed-no-space", ["2", "5"], "'Sealed:' without its space is not the exact 'Sealed: '",
      "§1 Say 1.\nSealed:%s.\n" % SEAL, R("LINE-FORM"), "twin",
      "SEAL-FORM, if any line starting 'Sealed:' were a Sealed line")
probe("n02-sealed-lowercase", ["2"], "'sealed: ' is not the exact prefix", "§1 Say 1.\nsealed: %s.\n" % SEAL, R("LINE-FORM"))
probe("n03-two-titles", ["3"], "a second Title", "Title: a\nTitle: b\n§1 Say 1.\n", R("TITLE-PLACE"))
probe("n03-title-after-clause", ["3"], "a Title after a clause", "§1 Say 1.\nTitle: a\n", R("TITLE-PLACE"))
probe("n03-title-after-note", ["3"], "a Title after a Note: is a Note 'content'?",
      "Note: first\nTitle: a\n§1 Say 1.\n", RUN(out="1\n", ops=1, events=1), "twin",
      "TITLE-PLACE, if a Note counts as content")
probe("n04-note-after-sealed", ["4", "5"], "a Note may follow the Sealed line; the words then mismatch the law (phase 8)",
      "§1 Say 1.\nSealed: %s.\nNote: after the seal\n" % SEAL, R("SEAL-MISMATCH"))
probe("n04-clause-after-sealed", ["4"], "a clause after the Sealed line", "§1 Say 1.\nSealed: %s.\n§2 Say 2.\n" % SEAL,
      R("SEAL-PLACE"))
probe("n04-second-sealed", ["4"], "a second Sealed line", "§1 Say 1.\nSealed: %s.\nSealed: %s.\n" % (SEAL, SEAL),
      R("SEAL-PLACE"))
probe("n04-title-after-sealed", ["3", "4", "G3"], "a Title after the Sealed line: TITLE-PLACE is checked before SEAL-PLACE",
      "§1 Say 1.\nSealed: %s.\nTitle: late\n" % SEAL, R("TITLE-PLACE"))
probe("n04-junk-after-sealed", ["4", "G3"], "a malformed line after the Sealed line: LINE-FORM is checked first",
      "§1 Say 1.\nSealed: %s.\nHello\n" % SEAL, R("LINE-FORM"))
probe("n05-sealed-space-joined", ["5"], "proquints joined by spaces", "§1 Say 1.\nSealed: lusab lusab lusab lusab.\n",
      R("SEAL-FORM"))
probe("n05-sealed-three", ["5"], "three proquints", "§1 Say 1.\nSealed: lusab-lusab-lusab.\n", R("SEAL-FORM"))
probe("n05-sealed-bad-letter", ["5"], "'c' is not a proquint consonant", "§1 Say 1.\nSealed: lusac-lusab-lusab-lusab.\n",
      R("SEAL-FORM"))
probe("n05-sealed-no-period", ["5"], "no final period", "§1 Say 1.\nSealed: %s\n" % SEAL, R("SEAL-FORM"))
probe("n05-sealed-mismatch", ["5"], "well formed, but not the law's words", "§1 Say 1.\nSealed: %s.\n" % SEAL,
      R("SEAL-MISMATCH"))
probe("n06-leading-zeros", ["6"], "label parts compared as integers: §01, §1.01, §002 are 1, 1.1, 2",
      "§01 If true, do the following.\n§1.01 Say 1.\n§002 Say 2.\n", RUN(out="1\n2\n", ops=3, events=2))
probe("n06-section-and-period", ["6"], "'§1.' is neither label form", "§1. Say 1.\n", R("LINE-FORM"))
probe("n07-two-spaces", ["7"], "exactly one space after the label", "§1  Say 1.\n", R("LINE-FORM"))
probe("n08-syntax", ["8"], "a malformed statement", "§1 Say 1 +.\n", R("SYNTAX"))
probe("n08-lex-character", ["8"], "a character that begins no token", "§1 Say #.\n", R("LEX"))
probe("n08-lex-unterminated", ["8"], "an unterminated text literal", "§1 Say \"abc.\n", R("LEX"))
probe("n08-lex-dot", ["8"], "a second decimal point: '.' begins no token", "§1 Say 1.5.5.\n", R("LEX"))
probe("n09-mixed-labels", ["9"], "the two label forms mixed", "1. Say 1.\n§2 Say 2.\n3. Say 3.\n",
      RUN(out="1\n2\n3\n", ops=3, events=3))

# ------------------------------------------------------------------ §2 tokens
probe("n10-no-separators", ["10"], "no separator between tokens", "§1 Say 3*4+1.\n", RUN(out="13\n", ops=3, events=1))
probe("n10-longest-word", ["10"], "longest match: 'times3' is one word, so the statement does not parse",
      "§1 Say 2times3.\n", R("SYNTAX"))
probe("n11-colon", ["11"], "':' begins nothing", "§1 Say 1 : 2.\n", R("SYNTAX"))
probe("n12-reserved-any-case", ["12"], "'Sum' is reserved", "§1 Let Sum be 2.\n", R("SYNTAX"))
probe("n12-keywords-any-case", ["12"], "keywords in any case", "§1 LET n BE 2.\n§2 SAY n TIMES n.\n",
      RUN(out="4\n", ops=3, events=2))
probe("n13-seal-phrase-and-s", ["13"], "'s' is an identifier; this law's seal is a phrase (compared, not printed)",
      "§1 Let s be 5.\n§2 Say s.\n§3 Say this law's seal = this law's seal.\n", RUN(out="5\ntrue\n", ops=4, events=3))

# ------------------------------------------------------------------ §3 statements
probe("n15-unless-counts-not", ["15"], "Unless counts its not: arm, not, Say", "§1 Unless false, say 1.\n",
      RUN(out="1\n", ops=3, events=1))
probe("n16-unless-then", ["16"], "Unless takes no then", "§1 Unless false, then say 1.\n", R("SYNTAX"))
probe("n16-unless-inline-otherwise", ["16"], "Unless takes no inline otherwise",
      "§1 Unless true, say 1; otherwise say 2.\n", R("SYNTAX"))
probe("n16-unless-otherwise-attaches", ["16", "15"], "an Otherwise clause attaches to an Unless",
      "§1 Unless true, say 1.\n§2 Otherwise, say 2.\n", RUN(out="2\n", ops=3, events=1))
probe("n17-elseif-inline-otherwise", ["17"], "an else-if arm takes no inline otherwise",
      "§1 If false, say 1.\n§2 Otherwise, if true, say 2; otherwise say 3.\n", R("SYNTAX"))
probe("n18-arm-condition-clause", ["18"], "an absorbed arm's condition names its own clause (3, not 2)",
      "§1 Let z be 0.\n§2 If false, say 1.\n§3 Otherwise, if 1 divided by z = 1, say 2.\n",
      RUN("REFUSED DIVISION-BY-ZERO 3", "", 4, 2))
probe("n18-arm-statement-clause", ["18"], "an absorbed arm's inline statement names its own clause",
      "§1 Let z be 0.\n§2 If false, say 1.\n§3 Otherwise, say 1 divided by z.\n",
      RUN("REFUSED DIVISION-BY-ZERO 3", "", 4, 2))
probe("n18-arm-claim-clause", ["18"], "an inline claim in an absorbed arm is declared at its own clause",
      "§1 If false, say 1.\n§2 Otherwise, we claim that 1 = 1.\n",
      RUN(out="", ops=3, events=1, claims=["claim 0 2 1 1 1 0 0"]))
probe("n19-decimal-bound", ["19"], "a decimal While bound", "§1 While false, at most 5.0 times, do the following.\n§1.1 Say 1.\n",
      R("SYNTAX"))
probe("n19-zero-bound", ["19"], "a bound of 0", "§1 While false, at most 0 times, do the following.\n§1.1 Say 1.\n", R("FUEL"))
probe("n19-bound-over", ["19"], "2^62 + 1",
      "§1 While false, at most 4611686018427387905 times, do the following.\n§1.1 Say 1.\n", R("FUEL"))
probe("n19-bound-max", ["19"], "2^62 is allowed",
      "§1 While false, at most 4611686018427387904 times, do the following.\n§1.1 Say 1.\n", RUN(ops=1, events=0))
probe("n19-bound-beyond-i64", ["19"], "a bound beyond i64 is FUEL, not LITERAL-RANGE",
      "§1 While false, at most 99999999999999999999 times, do the following.\n§1.1 Say 1.\n", R("FUEL"))
probe("n20-name-reserved-the", ["20"], "a name beginning with 'the'", "§1 To the go, do the following.\n§1.1 Say 1.\n",
      R("PROCEDURE-NAME"))
probe("n20-name-statement-word", ["20"], "a name beginning with 'say'", "§1 To say hi, do the following.\n§1.1 Say 1.\n",
      R("PROCEDURE-NAME"))
probe("n21-name-do-the-following", ["21"], "the name 'do the following'",
      "§1 To do the following, do the following.\n§1.1 Say 1.\n", R("PROCEDURE-NAME"))
probe("n20-reserved-word-inside-name", ["20"], "reserved words after the first are allowed",
      "§1 To step the masses, do the following.\n§1.1 Say 1.\n§2 Step the masses.\n§3 Perform step the masses.\n",
      RUN(out="1\n1\n", ops=4, events=2))
probe("n21-call-reserved-first-word", ["21", "20"], "a call whose first word is reserved ('do the following' as an arm)",
      "§1 If true, do the following; otherwise say 2.\n", R("SYNTAX"), "twin",
      "UNKNOWN-PROCEDURE (or PROCEDURE-NAME), if such a call were parsed as a name")
probe("n22-perform-before-definition", ["22"], "a top-level call before the definition",
      "§1 Greet.\n§2 To greet, do the following.\n§2.1 Say 1.\n", R("PERFORM-BEFORE-DEFINITION"))
probe("n22-recursion", ["22"], "a procedure performing itself", "§1 To greet, do the following.\n§1.1 Greet.\n",
      R("PERFORM-BEFORE-DEFINITION"))
probe("n22-mutual", ["22"], "mutual recursion",
      "§1 To ping, do the following.\n§1.1 Pong.\n§2 To pong, do the following.\n§2.1 Ping.\n",
      R("PERFORM-BEFORE-DEFINITION"))
probe("n23-notwithstanding-four", ["23"], "notwithstanding with four references",
      "§1 Define r as 1.\n§2 Define r as 2.\n§3 Define r as 3.\n§4 Define r as 4.\n"
      "§5 Notwithstanding §1, §2, §3 and §4, define r as 5.\n§6 Say r.\n", RUN(out="5\n", ops=2, events=1))
probe("n23-given-three", ["23", "32"], "given with three references, one of them the claim itself",
      "§1 We claim that true.\n§2 We claim that true.\n§3 We claim that true, given §1, §2 and §3.\n",
      RUN(ops=3, events=3, claims=["claim 0 1 1 1 0 0 0", "claim 1 2 1 1 0 0 0", "claim 2 3 1 1 0 0 0"]))
probe("n24-define-unless-counts", ["24"], "a Define's unless counts its not",
      "§1 Let a be false.\n§2 Define r as 1, unless a.\n§3 Say r.\n", RUN(out="1\n", ops=4, events=2))
probe("n25-two-provisos", ["25"], "provided that and unless together",
      "§1 Let a be true.\n§2 Define r as 1, provided that a, unless a.\n§3 Say r.\n", R("SYNTAX"))
probe("n26-the-everywhere", ["26"], "the filler in every identifier position",
      "§1 Let the xs be the list 1, 2 and 3.\n§2 Set item 1 of the xs to 7.\n§3 Increase item 2 of the xs by 1.\n"
      "§4 Append 9 to the xs.\n§5 Remove the last item of the xs.\n§6 Let the n be the length of the xs.\n"
      "§7 For each the i from 1 to the n, do the following.\n§7.1 Say item the i of the xs.\n"
      "§8 Define the r as 5.\n§9 Say the r.\n", RUN(out="7\n3\n3\n5\n", ops=22, events=13))
probe("n27-set-item-unary", ["27"], "the index of Set item is a unary",
      "§1 Let xs be the list 1 and 2.\n§2 Let i be 1.\n§3 Set item i plus 1 of xs to 5.\n", R("SYNTAX"))
probe("n27-increase-item-parenthesized", ["27"], "a parenthesized index",
      "§1 Let xs be the list 1 and 2.\n§2 Let i be 1.\n§3 Increase item (i plus 1) of xs by 5.\n§4 Say xs.\n",
      RUN(out="[1, 7]\n", ops=8, events=4))
probe("n28-define-in-arm", ["28"], "a Define inside an inline arm", "§1 If true, define r as 1.\n", R("SYNTAX"))
probe("n28-while-in-arm", ["28"], "a While inside an inline arm",
      "§1 If true, while false, at most 1 times, do the following.\n§1.1 Say 1.\n", R("SYNTAX"))
probe("n29-set-item-counter", ["29"], "Set item of a For counter: LOOP-VARIABLE before the list type",
      "§1 For each i from 1 to 2, do the following.\n§1.1 Set item 1 of i to 2.\n", R("LOOP-VARIABLE"))
probe("n29-increase-item-counter", ["29"], "Increase item of a For counter",
      "§1 For each i from 1 to 2, do the following.\n§1.1 Increase item 1 of i by 2.\n", R("LOOP-VARIABLE"))
probe("n29-decrease-counter", ["29"], "Decrease a For counter",
      "§1 For each i from 1 to 2, do the following.\n§1.1 Decrease i by 1.\n", R("LOOP-VARIABLE"))
probe("n29-append-to-counter", ["29"], "Append to a For counter (not a set, increase or decrease)",
      "§1 For each i from 1 to 2, do the following.\n§1.1 Append 1 to i.\n", R("TYPE"), "twin",
      "LOOP-VARIABLE, if item 29 covered every write")

# ------------------------------------------------------------------ oracles and targets
probe("n30-certificate-later", ["30"], "a later target", "§1 We claim that true, by the certificate of §2.\n§2 Say 1.\n",
      R("CERTIFICATE-TARGET"))
probe("n30-certificate-to", ["30"], "a To clause", "§1 To go, do the following.\n§1.1 Say 1.\n"
      "§2 We claim that true, by the certificate of §1.\n", R("CERTIFICATE-TARGET"))
probe("n30-certificate-define", ["30"], "a Define clause", "§1 Define r as 1.\n§2 We claim that true, by the certificate of §1.\n",
      R("CERTIFICATE-TARGET"))
probe("n30-certificate-decimals", ["30"], "a Decimals clause",
      "§1 Decimals are floats.\n§2 We claim that true, by the certificate of §1.\n", R("CERTIFICATE-TARGET"))
probe("n30-certificate-claim", ["30"], "a claim clause", "§1 We claim that true.\n§2 We claim that true, by the certificate of §1.\n",
      R("CERTIFICATE-TARGET"))
probe("n30-certificate-absorbed", ["30"], "an absorbed Otherwise clause",
      "§1 If false, say 1.\n§2 Otherwise, say 2.\n§3 We claim that true, by the certificate of §2.\n",
      R("CERTIFICATE-TARGET"))
probe("n30-certificate-in-procedure", ["30"], "a clause inside a procedure body: its counter grows each run (2 + 2)",
      "§1 Let s be 0.\n§2 To bump, do the following.\n§2.1 Increase s by 1.\n§3 Bump.\n§4 Bump.\n"
      "§5 We claim that s = 2, by the certificate of §2.1.\n",
      RUN(ops=9, events=4, claims=["claim 0 6 1 1 1 3 4"]))
probe("n30-certificate-chain", ["30"], "an If chain's counter covers its absorbed arms",
      "§1 Let x be 0.\n§2 If x = 1, say 1.\n§3 Otherwise, say 2.\n§4 We claim that true, by the certificate of §2.\n",
      RUN(out="2\n", ops=5, events=3, claims=["claim 0 4 1 1 0 2 3"]))
probe("n31-agreement-earlier-any", ["31"], "agreement of an earlier To and an earlier Define",
      "§1 To go, do the following.\n§1.1 Say 1.\n§2 Define r as 1.\n§3 We claim that true, by agreement of §1 and §2.\n",
      RUN(ops=1, events=1, claims=["claim 0 4 1 1 0 0 0"]))
probe("n31-agreement-same-clause", ["31"], "agreement of one clause with itself",
      "§1 Let a be 1.\n§2 We claim that a = 1, by agreement of §1 and §1.\n",
      RUN(ops=3, events=2, claims=["claim 0 2 1 1 1 0 0"]))
probe("n31-agreement-later", ["31"], "a target that is not earlier",
      "§1 We claim that true, by agreement of §1 and §2.\n§2 Say 1.\n", R("AGREEMENT-TARGET"))
probe("n32-premise-later-and-self", ["32"], "premises later than the claim, and the claim itself",
      "§1 We claim that true, given §2 and §1.\n§2 We claim that true.\n",
      RUN(ops=2, events=2, claims=["claim 0 1 1 1 0 0 0", "claim 1 2 1 1 0 0 0"]))
probe("n32-premise-inline-claim", ["32"], "an If clause whose arm is a claim is not a claim clause",
      "§1 If true, we claim that true.\n§2 We claim that true, given §1.\n", R("PREMISE-TARGET"))
probe("n33-unknown-notwithstanding", ["33"], "notwithstanding a missing clause", "§1 Notwithstanding §9, define r as 1.\n",
      R("UNKNOWN-CLAUSE"))
probe("n33-unknown-given", ["33"], "given a missing clause", "§1 We claim that true, given §9.\n", R("UNKNOWN-CLAUSE"))
probe("n33-unknown-certificate", ["33"], "a certificate of a missing clause",
      "§1 We claim that true, by the certificate of §9.\n", R("UNKNOWN-CLAUSE"))
probe("n33-unknown-agreement", ["33"], "agreement with a missing clause",
      "§1 Say 1.\n§2 We claim that true, by agreement of §1 and §9.\n", R("UNKNOWN-CLAUSE"))

# ------------------------------------------------------------------ §4 expressions
probe("n34-list-stops-before-not", ["34"], "'and not' ends the list, so 'and' joins a list and a Bool",
      "§1 Let b be true.\n§2 Say the list 1 and not b.\n", R("TYPE"))
probe("n34-list-goes-on-before-name", ["34"], "'and' before a name continues the list",
      "§1 Let a be 2.\n§2 Say the list 1 and a.\n", RUN(out="[1, 2]\n", ops=3, events=2))
probe("n34-list-goes-on-before-minus-and-the", ["34"], "',' before '-' and 'and' before 'the' continue the list",
      "§1 Let n be 3.\n§2 Say the list 1, -2 and the n.\n", RUN(out="[1, -2, 3]\n", ops=4, events=2))
probe("n34-list-goes-on-before-item", ["34"], "'and' before 'item' continues the list",
      "§1 Let xs be the list 5 and 6.\n§2 Say the list 1 and item 2 of xs.\n", RUN(out="[1, 6]\n", ops=5, events=2))
probe("n35-short-circuit", ["35"], "the right operand is not evaluated (it would be out of range)",
      "§1 Let xs be the list 1.\n§2 Say false and item 9 of xs = 1.\n§3 Say true or item 9 of xs = 1.\n",
      RUN(out="false\ntrue\n", ops=6, events=3))
probe("n36-minus-on-literal-counted", ["36"], "-4 is a counted negation", "§1 Let a be -4.\n§2 Say a.\n",
      RUN(out="-4\n", ops=3, events=2))
probe("n37-is-not-forms", ["37"], "is not E and is not equal to E: one op; is not less than, is not even: two",
      "§1 Say 1 is not 2.\n§2 Say 1 is not equal to 2.\n§3 Say 1 is not less than 2.\n§4 Say 2 is not even.\n"
      "§5 Say 1 != 2.\n", RUN(out="true\ntrue\nfalse\nfalse\ntrue\n", ops=12, events=5))
probe("n37-is-not-nan", ["37", "50"], "NaN: is not n is true; is not less than 1.0 is true; >= 1.0 is false",
      "§1 Decimals are floats.\n§2 Let z be 0.0.\n§3 Let n be z / z.\n§4 Say n is not n.\n"
      "§5 Say n is not less than 1.0.\n§6 Say n >= 1.0.\n", RUN(out="true\ntrue\nfalse\n", ops=10, events=5))

# ------------------------------------------------------------------ §5 types
probe("n38-fix-literal-over", ["38"], "a Fix literal of 2^31", "§1 Say 2147483648.0.\n", R("LITERAL-RANGE"))
probe("n38-fix-literal-rounds-over", ["38"], "a Fix literal that rounds to raw 2^63", "§1 Say 2147483647.9999999999.\n",
      R("LITERAL-RANGE"))
probe("n38-fix-literal-max", ["38"], "the largest Fix, exactly", "§1 Say %s.\n" % FIX_MAX,
      RUN(out=FIX_MAX + "\n", ops=1, events=1))
probe("n38-float-literal-huge", ["38"], "10^309 as a Float literal", "§1 Decimals are floats.\n§2 Say %s.\n" % TEN309,
      R("LITERAL-RANGE"))
probe("n38-float-literal-midpoint", ["38"], "halfway between DBL_MAX and 2^1024 rounds (to even) to infinity",
      "§1 Decimals are floats.\n§2 Say %d.0.\n" % MID, R("LITERAL-RANGE"))
probe("n38-float-literal-below-midpoint", ["38"], "one below the midpoint rounds to DBL_MAX",
      "§1 Decimals are floats.\n§2 Say %d.0.\n" % (MID - 1), RUN(out="%d.0\n" % DBL_MAX, ops=1, events=1))
probe("n39-int-with-fix", ["39", "42"], "Int with Fix makes a Fix list; the Int item's promotion counts",
      "§1 Say the list 1 and 2.5.\n", RUN(out="[1.0, 2.5]\n", ops=3, events=1))
probe("n39-int-with-float", ["39"], "Int with Float makes a Float list",
      "§1 Decimals are floats.\n§2 Say the list 1 and 0.5.\n", RUN(out="[1.0, 0.5]\n", ops=3, events=1))
probe("n39-bool-with-int", ["39"], "Bool goes only with Bool", "§1 Say the list true and 1.\n", R("TYPE"))
probe("n39-fix-with-float", ["39"], "Fix with Float", "§1 Say the list 1.5 and (2 as a float).\n", R("TYPE"))
probe("n39-text-item", ["39"], "a Text item", "§1 Say the list \"a\" and \"b\".\n", R("TYPE"))
probe("n40-promotion-inexact", ["40"], "2^53 + 1 promoted to Float", "§1 Decimals are floats.\n§2 Say 0.5 plus 9007199254740993.\n",
      RUN("REFUSED INEXACT-CONVERSION 2", "", 2, 1))
probe("n40-promotion-exact", ["40"], "2^53 is exact; the sum rounds", "§1 Decimals are floats.\n§2 Say 0.5 plus 9007199254740992.\n",
      RUN(out="9007199254740992.0\n", ops=3, events=1))
probe("n41-promotion-before-right-operand", ["41"], "the left promotion overflows before the right operand divides by zero",
      "§1 Say 3000000000 plus (1.5 plus 7 divided by 0).\n", RUN("REFUSED OVERFLOW 1", "", 2, 1))
probe("n42-promotion-before-next-item", ["42"], "a list item's promotion comes before the next item",
      "§1 Let xs be the list 3000000000, 1.5 and 7 divided by 0.\n", RUN("REFUSED OVERFLOW 1", "", 2, 1))
probe("n41-promotion-counts", ["41"], "promotions in an operator and a comparison are counted",
      "§1 Say 1 plus 1.5.\n§2 Say 1.5 is less than 2.\n", RUN(out="2.5\ntrue\n", ops=6, events=2))
probe("n43-int-as-integer", ["43"], "Int as an integer", "§1 Say 3 as an integer.\n", R("TYPE"))
probe("n43-integer-part-of-int", ["43"], "integer part of an Int", "§1 Say the integer part of 3.\n", R("TYPE"))
probe("n43-fix-as-fixed", ["43"], "Fix as a fixed", "§1 Say 1.5 as a fixed.\n", R("TYPE"))
probe("n44-length-of-text", ["44"], "length of a Text", "§1 Let t be \"abc\".\n§2 Say the length of t.\n", R("TYPE"))
probe("n45-int-and-fix-defines", ["45"], "Define clauses of Int and Fix", "§1 Define r as 1.\n§2 Define r as 1.5.\n", R("TYPE"))
probe("n46-define-sees-earlier-variables", ["46"], "a Define cannot see a later variable",
      "§1 Define r as x.\n§2 Let x be 1.\n", R("UNDECLARED"))
probe("n46-define-uses-complete-rule", ["46"], "a Define may use a rule completely defined before it",
      "§1 Define q as 2.\n§2 Define r as q plus 1.\n§3 Say r.\n", RUN(out="3\n", ops=4, events=1))
probe("n46-define-uses-incomplete-rule", ["46"], "a rule not completely defined before",
      "§1 Define q as 2.\n§2 Define r as q plus 1.\n§3 Define q as 2.\n", R("RULE-BEFORE-DEFINITION"))
probe("n47-variable-before-procedure", ["47"], "a local named as a procedure defined later is allowed",
      "§1 To a1, do the following.\n§1.1 Let b2 be 1.\n§2 To b2, do the following.\n§2.1 Say 2.\n§3 A1.\n§4 B2.\n",
      RUN(out="2\n", ops=4, events=2))
probe("n47-variable-after-procedure", ["47"], "a variable named (lowercased) as a procedure already defined",
      "§1 To go, do the following.\n§1.1 Say 1.\n§2 Let Go be 1.\n", R("REDECLARED"))
probe("n47-procedure-after-variable", ["47"], "a procedure named as a visible variable (the converse)",
      "§1 Let go be 1.\n§2 To go, do the following.\n§2.1 Say 1.\n", R("REDECLARED"), "twin",
      "COMPLETED (ops 1, events 1), if item 47 restricted variables only")
probe("n47-variable-named-rule", ["47"], "a variable named as a rule defined later", "§1 Let r be 1.\n§2 Define r as 2.\n",
      R("REDECLARED"))
probe("n48-set-rule", ["48"], "Set a rule name", "§1 Define r as 1.\n§2 Set r to 2.\n", R("UNDECLARED"))
probe("n48-append-to-rule", ["48"], "Append to a rule name", "§1 Define r as 1.\n§2 Append 1 to r.\n", R("UNDECLARED"))
probe("n48-increase-rule", ["48"], "Increase a rule name", "§1 Define r as 1.\n§2 Increase r by 1.\n", R("UNDECLARED"))
probe("n48-item-of-rule", ["48"], "item of a rule name (a read, not a write)", "§1 Define r as 1.\n§2 Say item 1 of r.\n",
      R("UNDECLARED"), "twin", "TYPE, if only writes to a rule name were UNDECLARED")
probe("n49-decimals-nested", ["49"], "Decimals not at top level",
      "§1 If true, do the following.\n§1.1 Decimals are floats.\n", R("DECIMALS-PLACE"))
probe("n49-decimals-twice", ["49"], "Decimals twice", "§1 Decimals are floats.\n§2 Decimals are fixed.\n", R("DECIMALS-PLACE"))
probe("n49-decimals-after-literal", ["49"], "Decimals after a decimal literal", "§1 Say 1.5.\n§2 Decimals are floats.\n",
      R("DECIMALS-PLACE"))
probe("n49-decimals-after-literal-in-procedure", ["49"], "after a decimal literal inside an earlier procedure",
      "§1 To go, do the following.\n§1.1 Say 1.5.\n§2 Decimals are floats.\n", R("DECIMALS-PLACE"))
probe("n50-signed-zero-and-nan", ["50"], "-0.0 is zero, not negative; NaN is none of the three",
      "§1 Decimals are floats.\n§2 Let z be 0.0.\n§3 Let n be z / z.\n§4 Say -0.0 is zero.\n§5 Say -0.0 is negative.\n"
      "§6 Say n is zero.\n§7 Say n is positive.\n§8 Say n is negative.\n",
      RUN(out="true\nfalse\nfalse\nfalse\nfalse\n", ops=15, events=7))

# ------------------------------------------------------------------ §6 rules
probe("n51-static-closure", ["51"], "§4 overrides §2 through the inapplicable §3",
      "§1 Let b be false.\n§2 Define r as 3.\n§3 Notwithstanding §2, define r as 2, provided that b.\n"
      "§4 Notwithstanding §3, define r as 1.\n§5 Say r.\n", RUN(out="1\n", ops=3, events=2))
probe("n52-conflict-not-counted", ["52"], "the comparison behind RULE-CONFLICT is not counted",
      "§1 Define r as 1.\n§2 Define r as 2.\n§3 Say r.\n", RUN("REFUSED RULE-CONFLICT 3", "", 2, 1))
probe("n52-agreeing-values-not-counted", ["52"], "three equal values: two comparisons, uncounted",
      "§1 Define r as 1.\n§2 Define r as 1.\n§3 Define r as 1.\n§4 Say r.\n", RUN(out="1\n", ops=2, events=1))

# ------------------------------------------------------------------ §7 dynamic semantics
probe("n53-event-e-index-and-tag", ["53", "54"], "event E carries the 1-based index and a tagged value (visible in the trace)",
      "§1 Let xs be the list true and false.\n§2 Set item 2 of xs to true.\n§3 Let ys be the list 5 and 6.\n"
      "§4 Increase item 2 of ys by 1.\n",
      RUN(ops=8, events=4, trace=[
          ["A", 1, "00000000" + "4c" + "42" + "00000002" + "01" + "00"],
          ["E", 2, "00000000" + "0000000000000002" + "42" + "01"],
          ["A", 3, "00000001" + "4c" + "49" + "00000002" + "0000000000000005" + "0000000000000006"],
          ["E", 4, "00000001" + "0000000000000002" + "49" + "0000000000000007"]]))
probe("n55-increase-promotion-counts", ["55"], "Increase of a Fix by an Int: +1, promotion +1, add +1",
      "§1 Let x be 1.5.\n§2 Increase x by 1.\n§3 Say x.\n", RUN(out="2.5\n", ops=5, events=3))
probe("n55-increase-promotion-refusal", ["55"], "the promotion refuses before the add is counted",
      "§1 Let x be 1.5.\n§2 Increase x by 3000000000.\n", RUN("REFUSED OVERFLOW 2", "", 3, 2))
probe("n56-unevaluated-claim", ["56"], "a claim never evaluated has ref clause and ref cost 0 0",
      "§1 Let a be 1.\n§2 If false, we claim that true, by the certificate of §1.\n",
      RUN(ops=2, events=1, claims=["claim 0 2 0 0 0 0 0"]))

# ------------------------------------------------------------------ RUNTIME-SPEC and numeric_ref
probe("n59-fix-as-integer", ["59"], "-3.0 as an integer is -3; 2.5 refuses",
      "§1 Say -3.0 as an integer.\n§2 Say 2.5 as an integer.\n", RUN("REFUSED INEXACT-CONVERSION 2", "-3\n", 5, 2))
probe("n59-float-as-integer-overflow", ["59"], "2^63 is integral and finite, then OVERFLOW",
      "§1 Decimals are floats.\n§2 Say 4.0 as an integer.\n§3 Say 9223372036854775808.0 as an integer.\n",
      RUN("REFUSED OVERFLOW 3", "4\n", 4, 2))
probe("n59-float-as-integer-inexact", ["59"], "2.5 as an integer", "§1 Decimals are floats.\n§2 Say 2.5 as an integer.\n",
      RUN("REFUSED INEXACT-CONVERSION 2", "", 2, 1))
probe("n59-float-as-integer-nan", ["59"], "NaN as an integer",
      "§1 Decimals are floats.\n§2 Let z be 0.0.\n§3 Say (z / z) as an integer.\n", RUN("REFUSED NOT-FINITE 3", "", 4, 2))
probe("n60-negative-sqrt-int", ["60"], "the square root of -4", "§1 Say the square root of -4.\n",
      RUN("REFUSED NEGATIVE-SQRT 1", "", 3, 1))
probe("n60-negative-sqrt-fix", ["60"], "the square root of -0.25 (Fix)", "§1 Say the square root of -0.25.\n",
      RUN("REFUSED NEGATIVE-SQRT 1", "", 3, 1))
probe("n60-float-sqrt-negative", ["60"], "Float: NaN for a negative, -0.0 for -0.0",
      "§1 Decimals are floats.\n§2 Say the square root of -0.25.\n§3 Say the square root of -0.0.\n",
      RUN(out="NaN\n-0.0\n", ops=6, events=2))


AMBIGUOUS = [
    ("§11 against the body (a contradiction)", "§11 does not say that it overrides the text above it, and the body "
     "still states the replaced rules: §1 \"Any other line is refused with LINE-FORM\" and Sealed as \"the last "
     "non-blank line\" (items 3, 4, 5, 8: TITLE-PLACE, SEAL-PLACE, SEAL-FORM, SYNTAX, LEX); §3 \"a name may not "
     "begin with a statement word\" (item 20: any reserved word), `Notwithstanding §a[, §b][ and §c]` (item 23), "
     "`[, provided that C][, unless C]` (item 25) and `Set item E of X` (item 27); §4 \"can begin an expression\" "
     "(item 34); §5 \"names a rule or a procedure\" (item 47: a procedure already defined) and its code list "
     "(item 8 says SYNTAX and LEX are added to it; they are not). The twin follows §11 wherever they differ."),
    ("G3 phases 2, 3 and 4", "Each phase lists several codes after its order (\"lines, in order: LINE-FORM, TITLE-PLACE, ...\"). "
     "Read (a): one pass in that order, the listed codes ordering the checks of one line or clause, so the first faulty "
     "line or clause decides; or (b): one pass per code, so a LINE-FORM on line 9 beats a LINE-CHECK on line 1. The twin "
     "takes (a). Probes g3-line-order-check, g3-line-order-numbering, g3-unknown-procedure-clause-order, "
     "g3-procedure-name-clause-order and g3-shape-tree-order separate them. Phase 4's \"tree order\" is taken as "
     "depth-first pre-order (document order), not breadth-first: probe g3-shape-preorder."),
    ("G3 phase 3, SYNTAX and LEX in one clause", "Listed SYNTAX before LEX, but a statement holding both an unreadable "
     "token and a misplaced one can be read three ways: lexed whole first (LEX always), parsed with a lazy lexer (the "
     "first offending position decides), or parsed without the unreadable characters (SYNTAX whenever the parse fails). "
     "The twin takes the first offending position. Probes g3-syntax-then-lex and g3-lex-then-syntax separate all three."),
    ("G3 phase 6, order within one clause", "\"Document walk order\" does not order two faults of one statement: "
     "`Let x be y` with x already declared and y undeclared. The twin checks the expression first (UNDECLARED). "
     "Probe g3-let-expression-first."),
    ("G3, which phase LITERAL-RANGE is in", "Not listed. The twin types literals in phase 6. Probe g3-literal-range-is-static."),
    ("G3 phase 1 and items 1, 14", "The door's refusals have no codes in SPEC, and a canonical text cannot carry a "
     "spaces-only line or a CR, so items 1 and 14 have no probe; the twin assumes canonical input."),
    ("Item 3, \"content\"", "§1 says a Title comes \"before any clause\"; §11 says \"after content\". Is a Note content? "
     "Is the Sealed line? The twin counts clause lines and the Sealed line. Probe n03-title-after-note."),
    ("Items 2 and 5, a line starting \"Sealed:\" without the space", "\"`Sealed: ` is exact\" can mean that only "
     "\"Sealed: \" opens a Sealed line (so `Sealed:x` is LINE-FORM, the twin's reading) or that such a line is a "
     "malformed Sealed line (SEAL-FORM). Probe n02-sealed-no-space."),
    ("Items 20 and 21, calls", "PROCEDURE-NAME is given for a definition. A call whose first word is reserved "
     "(`If C, do the following; otherwise S`; `Perform the go`) can never name a procedure: SYNTAX (twin), "
     "UNKNOWN-PROCEDURE, or PROCEDURE-NAME? Probe n21-call-reserved-first-word."),
    ("Item 29, Append and Remove", "\"Setting, increasing or decreasing ... item forms included\" leaves Append and "
     "Remove on a counter: TYPE (twin, the counter is not a list) or LOOP-VARIABLE. Probe n29-append-to-counter."),
    ("Item 47, the converse", "A variable may not take a procedure's name; may a procedure take a visible variable's "
     "name? §5's general rule says REDECLARED (twin); item 47 alone says nothing. Probe n47-procedure-after-variable. "
     "Also: inside a procedure's own body, is that procedure \"already defined\"? The twin says no (it is defined when "
     "its body ends, as for PERFORM-BEFORE-DEFINITION)."),
    ("Item 48, reads", "\"Writing to a rule name is UNDECLARED\". Reading a rule name where a list variable is needed "
     "(`item 1 of r`, `length of r`) is not a write: UNDECLARED (twin) or TYPE? Probe n48-item-of-rule."),
]

NOTES = [
    ("Item 31 (clear, perhaps unintended)", "Agreement targets are \"earlier clauses\" of any kind (a To, a Define, a "
     "claim, an absorbed Otherwise, the same clause twice), while certificate targets exclude those. The twin follows "
     "the text. Probes n31-*."),
    ("Items 53 and 54 (only in the trace)", "The trace head depends on the law seal, which the probes leave UNKNOWN. "
     "`probe_run.py --seals FILE` reruns with the reference's seals to compare trace heads; the event payloads given "
     "for n53-event-e-index-and-tag do not depend on the seal."),
    ("Items 1, 14, 58, 61, 62, G1, G2", "No probe: a canonical text carries no spaces-only line and no CR (1, 14); 58, "
     "61 and 62 are unobservable; G1 and G2 are about comparing and reporting (every refused probe shows G2: no "
     "receipt)."),
]


def main():
    os.makedirs(PROBES, exist_ok=True)
    manifest = {}
    expected = {}
    names = set()
    for p in P:
        assert p["name"] not in names, p["name"]
        names.add(p["name"])
        data = p["text"].encode("utf-8")
        assert data.endswith(b"\n") and b"\r" not in data and b"\t" not in data
        assert not any(line.endswith(b" ") for line in data.split(b"\n")), p["name"]
        with open(os.path.join(PROBES, p["name"] + ".orl"), "wb") as fh:
            fh.write(data)
        manifest[p["name"]] = {"law_seal": "UNKNOWN", "seal_words": "UNKNOWN",
                               "text_seal": hashlib.sha256(data).hexdigest(), "items": p["items"]}
        e = dict(p["expect"])
        if "output" in e:
            out = e["output"].encode("utf-8")
            e["output_bytes"] = len(out)
            e["output_sha256"] = hashlib.sha256(out).hexdigest()
        e["items"] = p["items"]
        e["what"] = p["what"]
        e["reading"] = p["reading"]
        if p["alt"]:
            e["alt"] = p["alt"]
        expected[p["name"]] = e
    with open(os.path.join(PROBES, "manifest.json"), "wb") as fh:
        fh.write((json.dumps(manifest, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    with open(os.path.join(PROBES, "expected.json"), "wb") as fh:
        fh.write((json.dumps(expected, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    write_md(expected)
    covered = sorted(set(i for p in P for i in p["items"]), key=lambda s: (s[0] != "G", int(s.lstrip("G"))))
    print("%d probes; items covered: %s" % (len(P), " ".join(covered)))


def write_md(expected):
    L = []
    L.append("# §11 probes: expected outcomes")
    L.append("")
    L.append("Written by the clean-room twin's author from SPEC.md v0.1 (§11) alone, 2026-10-25. Each probe is a "
             "canonical `.orl` text in this folder; `manifest.json` gives its text seal and its law seal as UNKNOWN. "
             "Every expectation was worked by hand from §11 and then checked against the twin "
             "(`python twin/probe_run.py --check`); the twin did not write them. `expected.json` holds the same "
             "expectations for a machine.")
    L.append("")
    L.append("How to read an entry:")
    L.append("- **refused CODE**: a compile refusal, so no receipt (§11 G2).")
    L.append("- otherwise the receipt lines that do not depend on the law seal: `status`, `output-bytes`, "
             "`output-sha256`, `events`, `ops`, `claims` and each `claim` line; and the output. `law-seal`, "
             "`text-seal` and `trace-head` are left out (the trace head starts from the law seal). The output never "
             "contains the seal words.")
    L.append("- **§11**: the expectation rests on §11 alone. **twin**: it also rests on a twin reading of a point §11 "
             "leaves open (listed at the end), and *other reading* gives the outcome under the alternative.")
    L.append("- A Sealed line in a probe uses the words `%s`, well formed and (barring a 2^-64 chance) not the law's, "
             "so a run that reaches phase 8 is SEAL-MISMATCH under any law seal." % SEAL)
    L.append("")
    L.append("| probe | items | tests | expected | basis |")
    L.append("|---|---|---|---|---|")
    for name in [p["name"] for p in P]:
        e = expected[name]
        if "refused" in e:
            exp = "refused **%s**" % e["refused"]
        else:
            parts = ["`status %s`" % e["status"]]
            if e["output"]:
                shown = e["output"].replace("\n", "\\n")
                if len(shown) > 60:
                    shown = shown[:28] + "…" + shown[-24:]
                parts.append("output `%s`" % shown)
            else:
                parts.append("no output")
            parts.append("`output-bytes %d`" % e["output_bytes"])
            parts.append("`events %d`" % e["events"])
            parts.append("`ops %d`" % e["ops"])
            parts.append("`claims %d`" % len(e["claims"]))
            for c in e["claims"]:
                parts.append("`%s`" % c)
            exp = ", ".join(parts)
        basis = "§11" if e["reading"] == "11" else "twin; *other reading:* " + e["alt"]
        L.append("| `%s` | %s | %s | %s | %s |" % (name, ", ".join(e["items"]), e["what"], exp, basis))
    L.append("")
    L.append("Output digests (`output-sha256`) of the probes that run, for byte comparison:")
    L.append("")
    for name in [p["name"] for p in P]:
        e = expected[name]
        if "refused" not in e:
            L.append("- `%s`: `%s`" % (name, e["output_sha256"]))
    L.append("")
    L.append("The events of `n53-event-e-index-and-tag` (kind, clause, payload; independent of the law seal):")
    L.append("")
    for kind, clause, payload in expected["n53-event-e-index-and-tag"]["trace"]:
        L.append("- `%s %d %s`" % (kind, clause, payload))
    L.append("")
    L.append("## Points of §11 still open")
    L.append("")
    L.append("The probes marked *twin* rest on these. Each names the probe that separates the readings.")
    L.append("")
    for title, text in AMBIGUOUS:
        L.append("- **%s.** %s" % (title, text))
    L.append("")
    L.append("## Notes")
    L.append("")
    for title, text in NOTES:
        L.append("- **%s.** %s" % (title, text))
    L.append("")
    with open(os.path.join(PROBES, "EXPECTED.md"), "wb") as fh:
        fh.write("\n".join(L).encode("utf-8"))


if __name__ == "__main__":
    main()

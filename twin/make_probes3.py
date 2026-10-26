#!/usr/bin/env python3
"""Write the round-3 probes for SPEC §12 and §13: twin/probes3/NAME.orl, manifest.json,
expected.json and EXPECTED.md.

Every expectation below was worked by hand from SPEC.md (§11, §12, §13 and the body), before the
twin was run on any of these texts; the twin is checked against them (python probe_run.py --check
--dir probes3), never the other way round. "basis" is "§12" or "§13" when that text decides the
outcome, "twin reading" when the twin's author had to choose; then "alt" says the other reading,
"alt_key" is the twin's --alt switch for it and "alt_expect" the outcome under it (worked by hand
too; python probe_run.py --dir probes3 --alts checks the switches).
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes3")
SEAL = "lusab-lusab-lusab-lusab"          # well formed; not the law's words (barring 2^-64)


def R(code):
    return {"refused": code}


def RUN(status="COMPLETED", out="", ops=0, events=0, claims=()):
    return {"status": status, "output": out, "ops": ops, "events": events, "claims": list(claims)}


P = []


def probe(name, items, what, text, expect, basis="§13", alt=None, alt_key=None, alt_expect=None, note=None):
    P.append(dict(name=name, items=items, what=what, text=text, expect=expect, basis=basis,
                  alt=alt, alt_key=alt_key, alt_expect=alt_expect, note=note))


def lab(k):
    """The label of depth k on the first-child chain: §1, §1.1, §1.1.1, ..."""
    return "§" + ".".join(["1"] * k)


def par(n, inner):
    return "(" * n + inner + ")" * n


def plus(n):
    return " plus ".join(["1"] * n)


def L(*lines):
    return "".join(l + "\n" for l in lines)


def ifs(n):
    return ["%s If true, do the following." % lab(k) for k in range(1, n + 1)]


def fors(n):
    return ["%s For each i%d from 1 to 1, do the following." % (lab(k), k) for k in range(1, n + 1)]


# ------------------------------------------------------------------ phase 2: lines (§12 NESTING-DEPTH, §13)
probe("p2-depth-24-passes", ["§12 NESTING-DEPTH"], "a label of 24 parts is allowed",
      L(*(ifs(23) + ["%s Say 1." % lab(24)])),
      # 23 Ifs: +1 each (the condition 'true' costs 0); Say: +1 and event S.
      RUN(out="1\n", ops=24, events=1), "§12")
probe("p2-depth-25-refused", ["§12 NESTING-DEPTH"], "a label of 25 parts",
      L(*(ifs(24) + ["%s Say 1." % lab(25)])), R("NESTING-DEPTH"), "§12")
probe("p2-line-check-before-depth", ["§13 phase 2"], "one line: LINE-CHECK is listed before NESTING-DEPTH",
      L(*(ifs(24) + ["%s Say 1. [zzz]" % lab(25)])), R("LINE-CHECK"))
probe("p2-depth-before-numbering", ["§13 phase 2"], "one line both 25 parts deep and misnumbered: NESTING-DEPTH first",
      L("§1 If true, do the following.", "%s Say 1." % lab(25)), R("NESTING-DEPTH"))
probe("p2-numbering-line-before-depth-line", ["§13 phase 2"],
      "one pass, line by line: NUMBERING on line 2 before NESTING-DEPTH on line 3",
      L("§1 Say 1.", "§3 Say 2.", "%s Say 3." % lab(25)), R("NUMBERING"))
probe("p2-seal-place-before-depth", ["§13 phase 2"], "after the Sealed line, SEAL-PLACE is listed before NESTING-DEPTH",
      L("§1 Say 1.", "Sealed: %s." % SEAL, "%s Say 2." % lab(25)), R("SEAL-PLACE"))
probe("p2-reference-of-25-parts", ["§12 NESTING-DEPTH"], "a reference (not a label) of 25 parts names no clause",
      L("§1 We claim that true, given %s." % lab(25)), R("UNKNOWN-CLAUSE"), "twin reading",
      "NESTING-DEPTH, if the bound on a label's parts also bounded references", "ref-parts", R("NESTING-DEPTH"))
probe("p2-period-inside-literal", ["§13 phase 2"], "the line ends with a quote, its period inside the literal",
      L('§1 Say "a."'), R("LINE-FORM"))
probe("p2-sealed-prefix-opens", ["§13 phase 2"], "'Sealed: ' opens a Sealed line; what follows is malformed",
      L("§1 Say 1.", "Sealed:  %s." % SEAL), R("SEAL-FORM"))
probe("p2-second-sealed-malformed", ["§13 phase 2"], "a second Sealed line that is malformed: SEAL-FORM before SEAL-PLACE",
      L("§1 Say 1.", "Sealed: %s." % SEAL, "Sealed: lusab."), R("SEAL-FORM"))
probe("p2-no-period-after-sealed", ["§13 phase 2"], "a clause line without its period after the Sealed line: LINE-FORM first",
      L("§1 Say 1.", "Sealed: %s." % SEAL, "§2 Say 2"), R("LINE-FORM"))
probe("p2-bad-check-after-sealed", ["§13 phase 2"], "after the Sealed line: SEAL-PLACE before LINE-CHECK",
      L("§1 Say 1.", "Sealed: %s." % SEAL, "§2 Say 2. [zzz]"), R("SEAL-PLACE"))
probe("p2-title-after-note-after-sealed", ["§13 phase 2"], "the Sealed line is content, a Note is not",
      L("§1 Say 1.", "Sealed: %s." % SEAL, "Note: x", "Title: late"), R("TITLE-PLACE"))
probe("p2-line-check-line-1-before-line-form-line-9", ["§13 phase 2"], "§13's own example",
      L("§1 Say 1. [zzz]", "§2 Say 2.", "§3 Say 3.", "§4 Say 4.", "§5 Say 5.", "§6 Say 6.", "§7 Say 7.", "§8 Say 8.",
        "Hello"), R("LINE-CHECK"))

# ------------------------------------------------------------------ phase 3: statements
probe("p3-lex-before-syntax", ["§13 phase 3"], "the statement is read into tokens whole: '@' is LEX though '=' fails first",
      L("§1 Let = 1 @."), R("LEX"), alt="SYNTAX under the round-2 reading (first offending position)",
      alt_key="lex-lazy", alt_expect=R("SYNTAX"))
probe("p3-lex-at-the-end", ["§13 phase 3"], "a SYNTAX fault early, an unreadable '?' last",
      L("§1 Say 1 plus plus 2 ?."), R("LEX"), alt="SYNTAX under the round-2 reading",
      alt_key="lex-lazy", alt_expect=R("SYNTAX"))
probe("p3-syntax-clause-1-before-lex-clause-2", ["§13 phase 3"], "across clauses, clause order decides",
      L("§1 Say 1 +.", "§2 Say #."), R("SYNTAX"))
probe("p3-syntax-before-procedure-name", ["§13 phase 3"], "a To with a reserved first word that does not parse",
      L("§1 To the go 1, do the following.", "§1.1 Say 1."), R("SYNTAX"))
probe("p3-perform-fly-away-1", ["§13 phase 3"], "§13's own example", L("§1 Perform fly away 1."), R("SYNTAX"))
probe("p3-syntax-before-unknown-procedure", ["§13 phase 3"], "an unknown call and a syntax fault in one clause",
      L("§1 If true, fly; otherwise say 1 +."), R("SYNTAX"))
probe("p3-name-alone-unknown", ["§13 phase 3"], "§13's own example: the name alone, defined nowhere",
      L("§1 Fly away."), R("UNKNOWN-PROCEDURE"))
probe("p3-call-holds-a-number", ["§13 phase 3"], "§13's own example", L("§1 Fly 1."), R("SYNTAX"))
probe("p3-perform-the-name", ["§13 phase 3"], "the filler 'the' is not part of a call",
      L("§1 To go, do the following.", "§1.1 Say 1.", "§2 Perform the go."), R("SYNTAX"))
probe("p3-call-reserved-first-word", ["§13 phase 3"], "a call in an Unless arm beginning with a reserved word",
      L("§1 Unless false, sum things."), R("SYNTAX"))
probe("p3-to-without-name", ["§13 phase 3"], "a To with no name", L("§1 To, do the following.", "§1.1 Say 1."), R("SYNTAX"))
probe("p3-perform-nothing", ["§13 phase 3"], "a Perform with nothing after it", L("§1 Perform."), R("SYNTAX"))
probe("p3-call-in-arm-to-semicolon", ["§13 phase 3"], "an inline arm's call ends at ';'",
      L("§1 To fly away, do the following.", "§1.1 Say 1.", "§2 If false, fly away; otherwise say 2."),
      # §2: the arm +1 (false), then the otherwise arm: Say +1, event S.
      RUN(out="2\n", ops=2, events=1))
probe("p3-unknown-call-in-arm-never-run", ["§13 phase 3"], "UNKNOWN-PROCEDURE is static, run or not",
      L("§1 If true, say 1; otherwise fly."), R("UNKNOWN-PROCEDURE"))
probe("p3-call-to-nested-to", ["§12 procedures", "§13 phase 3"],
      "procedures are collected from top-level clauses, so a nested To's name is no procedure",
      L("§1 If true, do the following.", "§1.1 To go, do the following.", "§1.1.1 Say 1.", "§2 Go."),
      R("UNKNOWN-PROCEDURE"), "twin reading",
      "PROCEDURE-PLACE, if every To clause's name were collected (§13: 'a name no To clause defines')",
      "procs-all", R("PROCEDURE-PLACE"))
probe("p3-malformed-to-defines-nothing", ["§12 procedures", "§13 phase 3"],
      "a call (clause 1) of a name whose top-level To (clause 2) does not parse",
      L("§1 Go.", "§2 To go 1, do the following.", "§2.1 Say 1."), R("UNKNOWN-PROCEDURE"), "twin reading",
      "SYNTAX, if the lexer collected the words after 'To' whether or not the clause parses",
      "procs-lexer", R("SYNTAX"))
probe("p3-to-spacing", ["§12 procedures"], "spacing inside ', do the following' and the name does not matter",
      L("§1 To fly  away ,do the following.", "§1.1 Say 1.", "§2 Fly away."),
      # §2: Perform +1; Say 1: +1, event S.
      RUN(out="1\n", ops=2, events=1), "§12")
probe("p3-procedure-name-of-nested-to", ["§12 procedures", "§13 phase 3"],
      "a nested To is parsed: PROCEDURE-NAME (phase 3) before PROCEDURE-PLACE (phase 6)",
      L("§1 If true, do the following.", "§1.1 To the go, do the following.", "§1.1.1 Say 1."), R("PROCEDURE-NAME"))

# ------------------------------------------------------------------ EXPRESSION-DEPTH (§12, as §13 states it)
probe("ed-23-parens-pass", ["§13 EXPRESSION-DEPTH"], "23 nested parentheses around a name: 24 on the path",
      L("§1 Let a be 5.", "§2 Say %s." % par(23, "a")), RUN(out="5\n", ops=2, events=2))
probe("ed-24-parens", ["§13 EXPRESSION-DEPTH"], "24 nested parentheses around a name: 25",
      L("§1 Let a be 5.", "§2 Say %s." % par(24, "a")), R("EXPRESSION-DEPTH"))
probe("ed-63-terms-pass", ["§13 EXPRESSION-DEPTH"], "Say with 63 terms joined by plus: the tree is 64 deep",
      L("§1 Say %s." % plus(63)), RUN(out="63\n", ops=63, events=1))
probe("ed-64-terms", ["§13 EXPRESSION-DEPTH"], "with 64 terms: 65 deep", L("§1 Say %s." % plus(64)), R("EXPRESSION-DEPTH"))
probe("ed-23-minuses-pass", ["§13 EXPRESSION-DEPTH"], "23 unary minuses and a number: 24",
      L("§1 Say %s1." % ("- " * 23)), RUN(out="-1\n", ops=24, events=1))
probe("ed-24-minuses", ["§13 EXPRESSION-DEPTH"], "24 unary minuses and a number: 25",
      L("§1 Say %s1." % ("- " * 24)), R("EXPRESSION-DEPTH"))
probe("ed-23-nots-pass", ["§13 EXPRESSION-DEPTH"], "23 nots over 1 = 1: 24 on the path to each 1",
      # comparison +1, 23 nots +23, Say +1; true negated 23 times is false.
      L("§1 Say %s1 = 1." % ("not " * 23)), RUN(out="false\n", ops=25, events=1))
probe("ed-24-nots", ["§13 EXPRESSION-DEPTH"], "24 nots: 25", L("§1 Say %s1 = 1." % ("not " * 24)), R("EXPRESSION-DEPTH"))
probe("ed-23-phrases-pass", ["§13 EXPRESSION-DEPTH"], "23 nested phrases and a number: 24",
      L("§1 Say %s1." % ("the absolute value of " * 23)), RUN(out="1\n", ops=24, events=1))
probe("ed-24-phrases", ["§13 EXPRESSION-DEPTH"], "24 nested phrases: 25",
      L("§1 Say %s1." % ("the absolute value of " * 24)), R("EXPRESSION-DEPTH"))
probe("ed-mixed-24-pass", ["§13 EXPRESSION-DEPTH"], "6 nots, 6 parentheses, 6 minuses, 5 phrases and a number: 24",
      # abs x5, negation x6, comparison 1, not x6, Say 1 = 19 operations; the value is true.
      L("§1 Say %s%s%s%s1%s = 1." % ("not " * 6, "(" * 6, "- " * 6, "the absolute value of " * 5, ")" * 6)),
      RUN(out="true\n", ops=19, events=1))
probe("ed-mixed-25", ["§13 EXPRESSION-DEPTH"], "the same with a seventh minus: 25",
      L("§1 Say %s%s%s%s1%s = 1." % ("not " * 6, "(" * 6, "- " * 7, "the absolute value of " * 5, ")" * 6)),
      R("EXPRESSION-DEPTH"))
probe("ed-item-counts", ["§13 EXPRESSION-DEPTH"], "24 nested 'item ... of' around a number: is 'item' an atom?",
      L("§1 Let xs be the list 1.", "§2 Say %s1%s." % ("item " * 24, " of xs" * 24)),
      R("EXPRESSION-DEPTH"), "twin reading",
      "COMPLETED, if only §13's five kinds (number, text, name, parenthesized expression, phrase) were counted",
      # Let: +1, list +1, event A; Say +1, 24 items +24, event S.
      "depth-atoms5", RUN(out="1\n", ops=27, events=2))
probe("ed-true-counts", ["§13 EXPRESSION-DEPTH"], "24 parentheses around true: is 'true' an atom?",
      L("§1 Say %s." % par(24, "true")), R("EXPRESSION-DEPTH"), "twin reading",
      "COMPLETED, if true were not counted (it is none of §13's five kinds)",
      "depth-atoms5", RUN(out="true\n", ops=1, events=1))
probe("ed-is-not-not-counted", ["§13 EXPRESSION-DEPTH"], "the not of 'is not less than' on the right operand's path",
      # 1 < 2 +1, its not +1, Say +1.
      L("§1 Say 1 is not less than %s." % par(23, "2")), RUN(out="false\n", ops=3, events=1), "twin reading",
      "EXPRESSION-DEPTH, if the not that item 37 puts around the test were one of 'the nots'",
      "depth-isnot", R("EXPRESSION-DEPTH"))
probe("ed-is-not-left-operand", ["§13 EXPRESSION-DEPTH"], "23 parentheses around the left operand of 'is not even'",
      # 1 is even: +1, its not +1, Say +1; 'not false' is true.
      L("§1 Say %s is not even." % par(23, "1")), RUN(out="true\n", ops=3, events=1), "twin reading",
      "EXPRESSION-DEPTH, if the not of item 37 were on the tree path to every atom below it (a path a left-to-right "
      "reading has passed before the not is written)", "depth-isnot-tree", R("EXPRESSION-DEPTH"))
probe("ed-unless-not-not-counted", ["§13 EXPRESSION-DEPTH"], "the implicit not of Unless on its condition's path",
      # arm +1, 1 = 2 +1, the Unless's not +1, Say +1.
      L("§1 Unless %s, say 1." % par(23, "1 = 2")), RUN(out="1\n", ops=4, events=1), "twin reading",
      "EXPRESSION-DEPTH, if Unless's not (counted at run time, item 15) were on the path",
      "depth-implicit-not", R("EXPRESSION-DEPTH"))
probe("ed-missing-atom", ["§13 EXPRESSION-DEPTH"], "24 '(' then ')': a 25th atom is expected but absent",
      L("§1 Say %s%s." % ("(" * 24, ")" * 24)), R("SYNTAX"), "twin reading",
      "EXPRESSION-DEPTH, if the count were taken on entering an atom position", "depth-entry", R("EXPRESSION-DEPTH"))
probe("ed-met-before-later-syntax", ["§13 phase 3"], "the nesting part is met left to right, before a later SYNTAX",
      L("§1 Say %s +." % par(24, "1")), R("EXPRESSION-DEPTH"))
probe("ed-after-earlier-syntax", ["§13 phase 3"], "a SYNTAX fault before the deep part",
      L("§1 Say 1 1 %s." % par(25, "1")), R("SYNTAX"))
probe("ed-tree-checked-after-parse", ["§13 phase 3"], "a 64-term tree whose parse fails at its end: SYNTAX",
      L("§1 Say %s plus." % plus(64)), R("SYNTAX"))
probe("ed-before-unknown-procedure", ["§13 phase 3"], "EXPRESSION-DEPTH before UNKNOWN-PROCEDURE in one clause",
      L("§1 If %s, fly." % par(24, "1 = 1")), R("EXPRESSION-DEPTH"))
probe("ed-tree-before-unknown-procedure", ["§13 phase 3"], "the tree's depth before UNKNOWN-PROCEDURE",
      L("§1 If %s = 1, fly." % plus(63)), R("EXPRESSION-DEPTH"))
probe("ed-clause-1-before-syntax-clause-2", ["§13 phase 3"], "clause order across clauses",
      L("§1 Say %s." % par(24, "1"), "§2 Say 1 +."), R("EXPRESSION-DEPTH"))
probe("ed-tree-paren-node", ["§13 EXPRESSION-DEPTH"], "63 terms, the first parenthesized: is '( )' a node of the tree?",
      L("§1 Say (1) plus %s." % plus(62)), R("EXPRESSION-DEPTH"), "twin reading",
      "COMPLETED, if parentheses were not nodes of the tree", "tree-no-paren", RUN(out="63\n", ops=63, events=1))
probe("ed-tree-cat-one-node", ["§13 EXPRESSION-DEPTH"], "64 parts joined by 'followed by'",
      # 63 for the concatenation, 1 for Say; 64 ones and LF.
      L("§1 Say %s." % " followed by ".join(["1"] * 64)), RUN(out="1" * 64 + "\n", ops=64, events=1), "twin reading",
      "EXPRESSION-DEPTH, if 'followed by' were a left-associative binary node", "tree-cat-binary", R("EXPRESSION-DEPTH"))
probe("ed-tree-inline-below-clause", ["§13 EXPRESSION-DEPTH"], "an inline Say of 63 terms in an If arm",
      L("§1 If true, say %s." % plus(63)), R("EXPRESSION-DEPTH"), "twin reading",
      "COMPLETED, if an inline statement rooted its own tree", "tree-inline-root",
      # arm +1, Say +1, 62 additions.
      RUN(out="63\n", ops=64, events=1))
probe("ed-tree-is-not-two-nodes", ["§13 EXPRESSION-DEPTH"], "'is not less than' with a right operand of 62 terms",
      L("§1 Say 2 is not less than %s." % plus(62)), R("EXPRESSION-DEPTH"), "twin reading",
      "COMPLETED, if 'is not less than' were one node", "tree-isnot-one",
      # 61 additions, 2 < 62 +1, not +1, Say +1.
      RUN(out="false\n", ops=64, events=1))
probe("ed-tree-length-name", ["§13 EXPRESSION-DEPTH"], "63 terms, the first 'the length of xs': is xs a node?",
      L("§1 Let xs be the list 1.", "§2 Say the length of xs plus %s." % plus(62)),
      # Let: +1, list +1, event A; Say +1, length +1, 62 additions, event S.
      RUN(out="63\n", ops=66, events=2), "twin reading",
      "EXPRESSION-DEPTH, if the name in 'length of X' were a node below the phrase", "tree-name-node",
      R("EXPRESSION-DEPTH"))
probe("ed-tree-conversions", ["§13 EXPRESSION-DEPTH"], "63 conversions in a row",
      L("§1 Say 1%s as a float." % (" as a float as a fixed" * 31)), R("EXPRESSION-DEPTH"), "twin reading",
      "COMPLETED, if conversions were not nodes of the tree", "tree-no-conv",
      # 63 conversions, Say +1; the last is to Float, 1.0.
      RUN(out="1.0\n", ops=64, events=1))

# ------------------------------------------------------------------ LOOP-NESTING (§12)
probe("ln-16-pass", ["§12 LOOP-NESTING"], "16 nested For loops",
      # each For from 1 to 1: +1, then +1 and event A for k = 1; Say +1, event S.
      L(*(fors(16) + ["%s Say 1." % lab(17)])), RUN(out="1\n", ops=33, events=17), "§12")
probe("ln-17-mixed", ["§12 LOOP-NESTING"], "17 nested loops, While and For alternating",
      L(*(["%s While false, at most 1 times, do the following." % lab(k) if k % 2 else
           "%s For each i%d from 1 to 1, do the following." % (lab(k), k) for k in range(1, 18)] +
          ["%s Say 1." % lab(18)])), R("LOOP-NESTING"), "§12")
_seq = ["F", "I"] * 7 + ["F"] * 9
probe("ln-ifs-do-not-count", ["§12 LOOP-NESTING"], "16 loops with 7 If blocks between them",
      L(*(["%s For each i%d from 1 to 1, do the following." % (lab(k), k) if s == "F" else
           "%s If true, do the following." % lab(k) for k, s in enumerate(_seq, 1)] + ["%s Say 1." % lab(24)])),
      # 16 Fors 2 ops and 1 event each, 7 Ifs 1 op each, Say 1 op 1 event.
      RUN(out="1\n", ops=40, events=17), "§12")
probe("ln-siblings-do-not-nest", ["§12 LOOP-NESTING"], "17 loops in sequence",
      L(*[l for k in range(1, 18) for l in ("§%d While false, at most 1 times, do the following." % k, "§%d.1 Say 1." % k)]),
      RUN(out="", ops=17, events=0), "§12")
probe("ln-place-before-condition", ["§12 LOOP-NESTING", "§13 phase 6"], "the 17th loop's condition is undeclared",
      L(*(fors(16) + ["%s While y, at most 1 times, do the following." % lab(17), "%s Say 1." % lab(18)])),
      R("LOOP-NESTING"), "twin reading",
      "UNDECLARED, if a loop's own parts were checked before its nesting", "loop-parts-first", R("UNDECLARED"))
probe("ln-procedure-body", ["§12 LOOP-NESTING"], "a procedure of 16 nested loops performed inside a loop",
      L(*(["§1 To p, do the following."] +
          ["§1%s For each i%d from 1 to 1, do the following." % (".1" * k, k) for k in range(1, 17)] +
          ["§1%s Say 1." % (".1" * 17), "§2 For each j from 1 to 1, do the following.", "§2.1 P."])),
      # §2: 2 ops 1 event; Perform +1; 16 Fors 32 ops 16 events; Say 1 op 1 event.
      RUN(out="1\n", ops=36, events=18), "§12")

# ------------------------------------------------------------------ phase 6: within a statement
probe("w-let-expression-before-name", ["§13 phase 6"], "Let x (REDECLARED) be a TYPE fault",
      L("§1 Let x be 1.", "§2 Let x be 1 plus true."), R("TYPE"))
probe("w-for-bound-before-counter", ["§13 phase 6"], "For i (REDECLARED) from y (UNDECLARED)",
      L("§1 Let i be 1.", "§2 For each i from y to 2, do the following.", "§2.1 Say 1."), R("UNDECLARED"))
probe("w-for-upper-bound-before-counter", ["§13 phase 6"], "For i (REDECLARED) from 1 to 2.5 (TYPE)",
      L("§1 Let i be 1.", "§2 For each i from 1 to 2.5, do the following.", "§2.1 Say 1."), R("TYPE"))
probe("w-for-lower-bound-type-at-once", ["§13 phase 6"], "For from 1.5 (TYPE) to y (UNDECLARED)",
      L("§1 For each i from 1.5 to y, do the following.", "§1.1 Say 1."), R("TYPE"), "twin reading",
      "UNDECLARED, if the bounds' Int requirement were checked after both bounds", "for-bounds-post", R("UNDECLARED"))
probe("w-item-index-before-list", ["§13 phase 6"], "item 1.5 (TYPE) of y (UNDECLARED)",
      L("§1 Say item 1.5 of y."), R("TYPE"))
probe("w-set-item-list-before-value", ["§13 phase 6"], "Set item of an Int (TYPE) to y (UNDECLARED)",
      L("§1 Let n be 1.", "§2 Set item 1 of n to y."), R("TYPE"))
probe("w-set-item-index-before-counter", ["§13 phase 6"], "Set item 1.5 (TYPE) of a counter (LOOP-VARIABLE)",
      L("§1 For each i from 1 to 1, do the following.", "§1.1 Set item 1.5 of i to 2."), R("TYPE"))
probe("w-increase-item-numbers-before-value", ["§13 phase 6"], "Increase item of a Bool list (TYPE) by y",
      L("§1 Let bs be the list true.", "§2 Increase item 1 of bs by y."), R("TYPE"))
probe("w-append-value-before-list", ["§13 phase 6"], "Append y (UNDECLARED) to an Int (TYPE)",
      L("§1 Let n be 1.", "§2 Append y to n."), R("UNDECLARED"))
probe("w-while-condition-before-fuel", ["§13 phase 6"], "While 1 (TYPE), at most 0 times (FUEL)",
      L("§1 While 1, at most 0 times, do the following.", "§1.1 Say 1."), R("TYPE"))
probe("w-while-undeclared-before-fuel", ["§13 phase 6"], "While y, at most 5*10^18 times (FUEL)",
      L("§1 While y, at most 5000000000000000000 times, do the following.", "§1.1 Say 1."), R("UNDECLARED"))
probe("w-define-references-before-name", ["§13 phase 6"], "a Define naming a later procedure, notwithstanding §9",
      L("§1 Notwithstanding §9, define go as 1.", "§2 To go, do the following.", "§2.1 Say 1."), R("UNKNOWN-CLAUSE"),
      note="Text changed after the first run: see the correction of w-to-walked-before-define.")
probe("w-define-name-before-value", ["§13 phase 6"], "Define go (a later procedure's name) as y",
      L("§1 Define go as y.", "§2 To go, do the following.", "§2.1 Say 1."), R("REDECLARED"),
      note="Text changed after the first run: its first text passed for the reason of w-to-walked-before-define.")
probe("w-to-walked-before-define", ["§13 phase 6", "§13 item 47"],
      "To go (clause 1) walked before Define go notwithstanding §9 (clause 2): the To meets the rule's name first",
      L("§1 To go, do the following.", "§1.1 Say 1.", "§2 Notwithstanding §9, define go as 1."), R("REDECLARED"),
      note="Corrected: first worked as UNKNOWN-CLAUSE (the Define's references before its name), which overlooked "
           "that the walk reaches the To at clause 1 first, and that 'a procedure may not take the lowercased name "
           "of any rule. Rules are collected first' (§13). The twin's REDECLARED was right; this was the first text "
           "of w-define-references-before-name.")
probe("w-define-value-before-proviso", ["§13 phase 6"], "a TYPE value, an undeclared proviso",
      L("§1 Define r as true plus 1, provided that y."), R("TYPE"))
probe("w-define-target-before-value", ["§13 phase 6"], "notwithstanding a Define of another name; value undeclared",
      L("§1 Define r as 1.", "§2 Notwithstanding §1, define q as y."), R("NOTWITHSTANDING-TARGET"))
probe("w-define-one-type-at-value", ["§13 phase 6"], "the one-type relation is checked at the value, before the proviso",
      L("§1 Define r as 1.", "§2 Define r as 1.5, provided that y."), R("TYPE"))
probe("w-to-place-before-name", ["§13 phase 6"], "a nested To named as a visible variable",
      L("§1 Let go be 1.", "§2 If true, do the following.", "§2.1 To go, do the following.", "§2.1.1 Say 1."),
      R("PROCEDURE-PLACE"))
probe("w-to-name-before-body", ["§13 phase 6"], "a To named as a visible variable, its body undeclared",
      L("§1 Let go be 1.", "§2 To go, do the following.", "§2.1 Say y."), R("REDECLARED"))
probe("w-claim-condition-before-oracle", ["§13 phase 6"], "an undeclared condition, a certificate of §9",
      L("§1 We claim that y, by the certificate of §9."), R("UNDECLARED"))
probe("w-claim-oracle-before-premises", ["§13 phase 6"], "a later certificate target, an unknown premise",
      L("§1 We claim that true, by the certificate of §2, given §9.", "§2 Say 1."), R("CERTIFICATE-TARGET"))
probe("w-and-types-both-operands", ["§13 phase 6"], "1 and y: both operands typed before and's own check",
      L("§1 Say 1 and y."), R("UNDECLARED"))
probe("w-and-check-before-later-operand", ["§13 phase 6"], "(true and 1) or y: the and's check completes first",
      L("§1 Say true and 1 or y."), R("TYPE"))
probe("w-quotient-types-both-operands", ["§13 phase 6"], "the quotient of 1.5 by y",
      L("§1 Say the quotient of 1.5 by y."), R("UNDECLARED"))
probe("w-operator-check-before-next-operand", ["§13 phase 6"], "(1 plus true) plus z: post-order",
      L("§1 Say (1 plus true) plus z."), R("TYPE"))
probe("w-copies-count-post-order", ["§13 phase 6"], "a list of 1.5 copies of y",
      L("§1 Say a list of 1.5 copies of y."), R("UNDECLARED"), "twin reading",
      "TYPE, if the count's Int requirement were checked when the count is reached, as an index's is",
      "copies-count-first", R("TYPE"))
probe("w-for-counter-last", ["§13 phase 6"], "For i (a rule's name) from 1 to y",
      L("§1 Define i as 1.", "§2 For each i from 1 to y, do the following.", "§2.1 Say 1."), R("UNDECLARED"))
probe("w-agreement-written-order", ["§13 phase 6"], "agreement of a later clause and a missing one",
      L("§1 We claim that true, by agreement of §2 and §9.", "§2 Say 1."), R("AGREEMENT-TARGET"))
probe("w-literal-range-in-written-order", ["§13 phase 6"], "LITERAL-RANGE (left operand) before UNDECLARED",
      L("§1 Say 99999999999999999999 plus y."), R("LITERAL-RANGE"))
probe("w-increase-number-before-value", ["§13 phase 6"], "Increase a Text (TYPE) by y (UNDECLARED)",
      L('§1 Let t be "a".', "§2 Increase t by y."), R("TYPE"))

# ------------------------------------------------------------------ item 47, extended by §13
probe("i47-variable-after-procedure-upper", ["§13 item 47"], "Let GO after To go",
      L("§1 To go, do the following.", "§1.1 Say 1.", "§2 Let GO be 1."), R("REDECLARED"))
probe("i47-procedure-after-visible-variable", ["§13 item 47"], "To go after Let Go",
      L("§1 Let Go be 1.", "§2 To go, do the following.", "§2.1 Say 1."), R("REDECLARED"))
probe("i47-procedure-after-invisible-variable", ["§13 item 47"], "To go after a go whose block has ended",
      L("§1 If true, do the following.", "§1.1 Let go be 1.", "§2 To go, do the following.", "§2.1 Say 2.", "§3 Go."),
      # If +1; Let +1, event A; Perform +1; Say +1, event S.
      RUN(out="2\n", ops=4, events=2), "twin reading",
      "REDECLARED, if 'one name may not stand for a variable and a procedure' covered variables no longer visible",
      "visible-global", R("REDECLARED"))
probe("i47-define-then-procedure", ["§13 item 47"], "Define go, then To go",
      L("§1 Define go as 1.", "§2 To go, do the following.", "§2.1 Say 1."), R("REDECLARED"))
probe("i47-procedure-then-define-case", ["§13 item 47"], "To go, then Define Go (compared lowercased)",
      L("§1 To go, do the following.", "§1.1 Say 1.", "§2 Define Go as 1."), R("REDECLARED"))
probe("i47-local-in-own-body", ["§13 item 47"], "a local of the procedure's own name inside its body",
      L("§1 To go, do the following.", "§1.1 Let go be 1.", "§1.2 Say go.", "§2 Go."),
      # Perform +1; Let +1, event A; Say +1, event S.
      RUN(out="1\n", ops=3, events=2))
probe("i47-variable-in-later-procedure", ["§13 item 47"], "a later procedure's local named as an earlier procedure",
      L("§1 To go, do the following.", "§1.1 Say 1.", "§2 To other, do the following.", "§2.1 Let go be 1."),
      R("REDECLARED"))
probe("i47-define-named-as-nested-to", ["§12 procedures", "§13 item 47"], "a Define named as a nested To",
      L("§1 Define go as 1.", "§2 If true, do the following.", "§2.1 To go, do the following.", "§2.1.1 Say 1."),
      R("PROCEDURE-PLACE"), "twin reading",
      "REDECLARED, if every To clause's name were collected", "procs-all", R("REDECLARED"))
probe("i47-rule-and-variable-case-sensitive", ["§13 item 47"], "Let R beside Define r",
      L("§1 Define r as 1.", "§2 Let R be 2.", "§3 Say R plus r."),
      # Let +1, event A; Say +1, the rule use +1, plus +1, event S.
      RUN(out="3\n", ops=4, events=2), "twin reading",
      "REDECLARED, if a variable were compared with rule names lowercased", "rule-var-lower", R("REDECLARED"))
probe("i47-counter-named-procedure", ["§13 item 47"], "a For counter Go after To go",
      L("§1 To go, do the following.", "§1.1 Say 1.", "§2 For each Go from 1 to 1, do the following.", "§2.1 Say 2."),
      R("REDECLARED"))
probe("i47-multiword-name-and-variable", ["§13 item 47"], "To go home beside a variable go",
      L("§1 Let go be 1.", "§2 To go home, do the following.", "§2.1 Say go.", "§3 Go home."),
      # Let +1, event A; Perform +1; Say +1, event S.
      RUN(out="1\n", ops=3, events=2))
probe("i47-own-call-in-block", ["§13 item 47"], "a procedure calling itself from an inline arm",
      L("§1 To go, do the following.", "§1.1 If true, go.", "§2 Go."), R("PERFORM-BEFORE-DEFINITION"))

# ------------------------------------------------------------------ items 29 and 48
probe("i29-append-to-counter", ["§13 item 29"], "Append to a For counter",
      L("§1 For each i from 1 to 1, do the following.", "§1.1 Append 1 to i."), R("TYPE"))
probe("i29-remove-from-counter", ["§13 item 29"], "Remove from a For counter",
      L("§1 For each i from 1 to 1, do the following.", "§1.1 Remove the last item of i."), R("TYPE"))
probe("i29-decrease-item-of-counter", ["§13 item 29"], "Decrease item of a For counter",
      L("§1 For each i from 1 to 1, do the following.", "§1.1 Decrease item 1 of i by 1."), R("LOOP-VARIABLE"))
probe("i48-length-of-rule", ["§13 item 48"], "length of a rule name", L("§1 Define r as 1.", "§2 Say the length of r."),
      R("UNDECLARED"))
probe("i48-remove-from-rule", ["§13 item 48"], "Remove from a rule name",
      L("§1 Define r as 1.", "§2 Remove the last item of r."), R("UNDECLARED"))
probe("i48-set-item-of-rule", ["§13 item 48"], "Set item of a rule name",
      L("§1 Define r as 1.", "§2 Set item 1 of r to 2."), R("UNDECLARED"))
probe("i48-item-of-rule", ["§13 item 48"], "item of a rule name", L("§1 Define r as 1.", "§2 Say item 1 of r."),
      R("UNDECLARED"))

# ------------------------------------------------------------------ §12 references and nested To
probe("ref-leading-zero-certificate", ["§12 references"], "a certificate of §01 names §1",
      L("§1 Let a be 1.", "§2 We claim that a = 1, by the certificate of §01."),
      # Let +1 (its counter 1), event A; claim +1, a = 1 +1 (cost 1), event C; ref clause 1, ref cost 1.
      RUN(ops=3, events=2, claims=["claim 0 2 1 1 1 1 1"]), "§12")
probe("ref-leading-zero-notwithstanding", ["§12 references"], "notwithstanding §001 names §1",
      L("§1 Define r as 1, provided that false.", "§2 Notwithstanding §001, define r as 2.", "§3 Say r."),
      # Say +1, the rule use +1 (the proviso 'false' costs 0); only §2 applies.
      RUN(out="2\n", ops=2, events=1), "§12")
probe("ref-leading-zero-given", ["§12 references"], "given §01 names §1",
      L("§1 We claim that true.", "§2 We claim that true, given §01."),
      RUN(ops=2, events=2, claims=["claim 0 1 1 1 0 0 0", "claim 1 2 1 1 0 0 0"]), "§12")
probe("nested-to-empty-block", ["§12 procedures", "§13 phase 4"], "a nested To without children: EMPTY-BLOCK (phase 4)",
      L("§1 If true, do the following.", "§1.1 To go, do the following."), R("EMPTY-BLOCK"))
probe("nested-to-place", ["§12 procedures"], "a nested To is parsed and refused",
      L("§1 If true, do the following.", "§1.1 To go, do the following.", "§1.1.1 Say 1."), R("PROCEDURE-PLACE"), "§12")

# ------------------------------------------------------------------ the phases, across the new codes
probe("x-nesting-depth-before-lex", ["§13 phase table"], "NESTING-DEPTH (phase 2, line 2) before LEX (phase 3, clause 1)",
      L("§1 Say #.", "%s Say 1." % lab(25)), R("NESTING-DEPTH"))
probe("x-expression-depth-before-orphan", ["§13 phase table"], "EXPRESSION-DEPTH (phase 3) before ORPHAN-OTHERWISE",
      L("§1 Otherwise, say 1.", "§2 Say %s." % par(24, "1")), R("EXPRESSION-DEPTH"))
probe("x-define-place-before-loop-nesting", ["§13 phase table"], "DEFINE-PLACE (phase 5) before LOOP-NESTING (phase 6)",
      L(*(fors(17) + ["%s Say 1." % lab(18), "§2 If true, do the following.", "§2.1 Define r as 1."])),
      R("DEFINE-PLACE"))
probe("x-loop-nesting-before-later-type", ["§13 phase table"], "LOOP-NESTING in walk order, before a later TYPE",
      L(*(fors(17) + ["%s Say 1." % lab(18), "§2 Say 1 plus true."])), R("LOOP-NESTING"))
probe("x-expression-depth-before-literal-range", ["§13 phase table"], "EXPRESSION-DEPTH (phase 3) before LITERAL-RANGE (6)",
      L("§1 Say 99999999999999999999.", "§2 Say %s." % par(24, "1")), R("EXPRESSION-DEPTH"))
probe("x-empty-block-before-loop-nesting", ["§13 phase table"], "the 17th loop has no children: EMPTY-BLOCK (phase 4)",
      L(*fors(17)), R("EMPTY-BLOCK"))


AMBIGUOUS = [
    ("§12 against §13: which To clauses define a procedure (phase 3)",
     "§12 says procedures are collected from top-level clauses; §13 says a call names a procedure unless 'no To "
     "clause defines' it. A nested To clause has a name but is refused PROCEDURE-PLACE in phase 6. The twin takes "
     "§12's mechanism: a nested To defines nothing (p3-call-to-nested-to, i47-define-named-as-nested-to). A To clause "
     "that does not parse defines nothing either (p3-malformed-to-defines-nothing); 'collected by the lexer' could "
     "mean the words after 'To' are collected before any parse."),
    ("EXPRESSION-DEPTH: which atoms count",
     "§13 lists 'a number, a text, a name, a parenthesized expression, a phrase'. §4's atom has five more forms: "
     "true, false, this law's seal, 'item U of X' and 'a list of N copies of V'. The twin counts every atom of §4 "
     "(ed-item-counts, ed-true-counts)."),
    ("EXPRESSION-DEPTH: which nots count",
     "§13 counts 'the nots'. Item 37 makes 'is not less than' a not around the test, item 15 gives Unless a not, item "
     "24 gives a Define's 'unless' a not. The twin counts only written not and 'it is not the case that' "
     "(ed-is-not-not-counted, ed-unless-not-not-counted). §13 defines the count on 'the path from a statement to "
     "each atom' (a tree) but says it is met reading left to right: the two disagree for the left operand of 'is "
     "not even' or 'is not less than', which a left-to-right reading has passed before the not is written "
     "(ed-is-not-left-operand). The twin's reading is the one under which they agree."),
    ("EXPRESSION-DEPTH: where the count is exceeded",
     "'Met in the order of a left-to-right predictive reading' does not say whether an atom position that holds no "
     "atom counts. The twin counts atoms that are there (ed-missing-atom)."),
    ("EXPRESSION-DEPTH: what the statement's tree is",
     "Only the plus chain is given. Not said: whether parentheses are nodes (ed-tree-paren-node), whether 'followed "
     "by' is one node of k parts as §7 evaluates it or a binary chain (ed-tree-cat-one-node), whether an inline "
     "statement is a node below its clause's statement (ed-tree-inline-below-clause), whether 'is not less than' is "
     "two nodes (ed-tree-is-not-two-nodes), whether conversions are nodes (ed-tree-conversions), whether the name "
     "in 'length of X' is a node (ed-tree-length-name). The twin: parentheses, conversions and the inline statement "
     "are nodes, a concatenation is one node, 'is not less than' is a not over a comparison, X is part of its "
     "phrase."),
    ("LOOP-NESTING: where in the loop's statement",
     "§13 orders a While's parts (C, then N) and a For's (A, B, the counter) but not LOOP-NESTING among them; a To's "
     "place is checked first. The twin checks a loop's place first (ln-place-before-condition)."),
    ("Phase 6: a requirement on an operand",
     "Refinement 2 checks 'a requirement on one part' when that part is reached, while an expression's operands are "
     "checked before 'the operator's own check'. For a For's bound (a statement part) the twin checks Int at the "
     "bound (w-for-lower-bound-type-at-once); for 'a list of N copies of V' (an expression) after both operands "
     "(w-copies-count-post-order). §13 settles 'item I of X' (the index at I) and quotient (after both) only."),
    ("Item 47: 'one name may not stand for a variable and a procedure'",
     "The lead sentence reads over the whole program; its bullets restrict it to a procedure already defined and a "
     "visible variable. The twin follows the bullets (i47-procedure-after-invisible-variable)."),
    ("Rules and variables: case",
     "Only procedure names are said to be compared lowercased. The twin compares a variable with a rule name "
     "exactly, as identifiers (i47-rule-and-variable-case-sensitive)."),
    ("NESTING-DEPTH and references",
     "Labels are bounded at 24 parts; a reference of 25 parts names no clause, UNKNOWN-CLAUSE in the twin "
     "(p2-reference-of-25-parts)."),
]

DEAD = [
    ("PROCEDURE-NAME against UNKNOWN-PROCEDURE, and EXPRESSION-DEPTH against PROCEDURE-NAME, within a clause",
     "Only a To clause can be PROCEDURE-NAME, and a To clause holds no call and no expression, so the order within "
     "a clause between these codes never decides anything."),
    ("'A procedure body starts again at 0' (LOOP-NESTING)",
     "A To stands only at top level (a nested To is PROCEDURE-PLACE, and §13 checks the place before the body), so "
     "its body is at loop depth 0 however the rule reads; only a dynamic reading (calls adding their callee's "
     "loops) would differ (ln-procedure-body)."),
    ("Phase 1 and QUOTE-BOUNDARY",
     "The door's codes and its literal rules cannot be reached by a canonical text: the twin takes canonical text."),
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
        e = finish(dict(p["expect"]))
        e["items"] = p["items"]
        e["what"] = p["what"]
        e["basis"] = p["basis"]
        if p["alt"]:
            e["alt"] = p["alt"]
        if p["note"]:
            e["note"] = p["note"]
        if p["alt_key"]:
            e["alt_key"] = p["alt_key"]
            e["alt_expect"] = finish(dict(p["alt_expect"]))
        expected[p["name"]] = e
    with open(os.path.join(PROBES, "manifest.json"), "wb") as fh:
        fh.write((json.dumps(manifest, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    with open(os.path.join(PROBES, "expected.json"), "wb") as fh:
        fh.write((json.dumps(expected, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    write_md(expected)
    n_twin = sum(1 for p in P if p["basis"] == "twin reading")
    print("%d probes (%d on a twin reading)" % (len(P), n_twin))


def finish(e):
    if "output" in e:
        out = e["output"].encode("utf-8")
        e["output_bytes"] = len(out)
        e["output_sha256"] = hashlib.sha256(out).hexdigest()
    return e


def show(e):
    if "refused" in e:
        return "refused **%s**" % e["refused"]
    parts = ["`status %s`" % e["status"]]
    if e["output"]:
        shown = e["output"].replace("\n", "\\n")
        if len(shown) > 40:
            shown = shown[:16] + "…" + shown[-12:]
        parts.append("output `%s`" % shown)
    else:
        parts.append("no output")
    parts.append("`output-bytes %d`" % e["output_bytes"])
    parts.append("`events %d`" % e["events"])
    parts.append("`ops %d`" % e["ops"])
    parts.append("`claims %d`" % len(e["claims"]))
    for c in e["claims"]:
        parts.append("`%s`" % c)
    return ", ".join(parts)


def write_md(expected):
    M = ["# §12 and §13 probes: expected outcomes", "",
         "Written by the clean-room twin's author from SPEC.md (body, §11, §12, §13) alone, 2026-10-25. Each "
         "probe is a canonical `.orl` text in this folder; `manifest.json` gives its text seal and its law seal as "
         "UNKNOWN. Every expectation was worked by hand before the twin ran on the probe; the twin is checked "
         "against them with `python twin/probe_run.py --check --dir probes3`, and its alternative readings with "
         "`python twin/probe_run.py --dir probes3 --alts`. `expected.json` holds the same expectations for a machine.",
         "", "How to read an entry:",
         "- **refused CODE**: a compile refusal, so no receipt (§11 G2).",
         "- otherwise the receipt lines that do not depend on the law seal (`status`, `output-bytes`, `events`, "
         "`ops`, `claims` and each `claim` line) and the output.",
         "- **basis**: `§12` or `§13` when that text decides the outcome; `twin reading` when it does not, with the "
         "other reading, the twin's `--alt` switch for it, and the outcome under it.",
         "- A Sealed line uses `%s`, well formed and (barring 2^-64) not the law's words." % SEAL,
         "", "| probe | rule | tests | expected | basis |", "|---|---|---|---|---|"]
    for p in P:
        e = expected[p["name"]]
        basis = e["basis"]
        if basis == "twin reading":
            basis = "twin reading; *other reading* (`--alt %s`): %s → %s" % (e["alt_key"], e["alt"], show(e["alt_expect"]))
        M.append("| `%s` | %s | %s | %s | %s |" % (p["name"], ", ".join(p["items"]), p["what"], show(e), basis))
    M += ["", "## Corrections after the first run", "",
          "The twin was run on these probes once their expectations were written. It disagreed with one hand-worked "
          "value, and the working was wrong; the probes involved are listed with what changed and why.", ""]
    M += ["- `%s`: %s" % (p["name"], p["note"]) for p in P if p["note"]]
    M += ["", "## Points of §12 and §13 still open", "",
          "Each names the probes that separate the readings; the twin's reading is its default, the other its `--alt`."]
    M += [""] + ["- **%s.** %s" % t for t in AMBIGUOUS]
    M += ["", "## Rules no canonical text can reach", ""] + ["- **%s.** %s" % t for t in DEAD] + [""]
    with open(os.path.join(PROBES, "EXPECTED.md"), "wb") as fh:
        fh.write("\n".join(M).encode("utf-8"))


if __name__ == "__main__":
    main()

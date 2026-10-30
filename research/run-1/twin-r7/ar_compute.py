"""Compute A_r = T_r ∪ L_r ∪ D_r (R7, point 4) over SPEC-15-DRAFT-1.md for the rulings of 2026-10-26 on finding 24
and the PREFIX licence. A clause is clause_diff.py's unit: a top-level item of a section, its continuation lines
included. T_r: clauses whose tag names the ruling. L_r: clauses containing a term the ruling defines or newly defines,
closed over §15.0's formal definitions. D_r: clauses the review, or a later record, names as dependent on the ruling,
given by draft 1's line numbers and mapped to every clause whose lines meet them. Prints Markdown; writes nothing.

With the argument 2 it computes the second set the same way: the rulings of 2026-10-27 (the labels' definitions, the
closure's rule table, R6's control), over SPEC-15-DRAFT-2.md, with D_r given by clause name."""
import hashlib
import re
import sys

D1 = "research/run-1/SPEC-15-DRAFT-1.md"
D0 = "research/run-1/twin-r7/SPEC-15-DRAFT-0-AS-REVIEWED.md"
D1_SHA = "367b1b4866e795d44141a87ef23579237fe414cf1fe61817fd47df135bd99d47"

RULINGS = {
    "F24": {
        "title": "finding 24: D10's court clause scoped (D)",
        "tag": r"\bD10\b",
        "terms": {   # what the ruling defines or newly defines
            "REFERENCE-ONLY": r"REFERENCE-ONLY",
            "configured": r"\bconfigured\b",
            "witness": r"\bwitness\b",
            "agreement": r"\bagree(?:d|s|ment)?\b",
            "HELD / held": r"\b(?:HELD|held)\b",
            "control": r"\bcontrols?\b",
        },
        "deps": [   # (source, first line, last line) in draft 1
            ("review finding 24 and A20: 15.13.11", 368, 373),
            ("review finding 24 and B14 items 5-6: 15.12.5", 311, 312),
            ("review finding 24 and B14 item 6: 15.12.6", 313, 316),
            ("packet A §6: the tag legend", 10, 18),
            ("packet A §6: §15.8's core", 232, 233),
            ("packet A §6: §15.9", 245, 253),
            ("packet A §6: §15.11", 276, 282),
            ("packet A §6: §15.12.2", 289, 290),
            ("packet A §6: §15.12.3", 291, 292),
            ("packet A §6: §15.12.5", 311, 312),
            ("packet A §6: §15.12.6", 313, 316),
            ("packet A §6: §15.13.1-4", 320, 327),
            ("packet A §6: §15.13.11", 368, 373),
            ("packet A §6: §15.14", 377, 381),
            ("packet A §6: the §15.15 row", 402, 402),
            ("packet E: 15.12.5 and 15.12.6, tagged R6 only", 311, 316),
        ],
    },
    "PREFIX": {
        "title": "the PREFIX licence (B1 + 4a + 5c + K1)",
        "tag": r"\bPREFIX\b",
        "terms": {
            "PREFIX / prefix": r"(?i)\bprefix\b",
            "licence": r"\blicen[cs](?:e|ed|es|ing)\b",
            "exempt": r"\bexempt(?:s|ed|ion)?\b",
            "boundary": r"\bboundary\b",
            "first input": r"\bfirst input\b",
            "first port declaration": r"\bfirst port declaration\b",
            "closure": r"\bclosure\b",
            "Reach": r"\bReach\b",
            "may execute": r"\bmay(?: |-)execute\b",
            "statement kind": r"\bstatement kinds?\b",
            "oracle": r"\boracle\b",
        },
        "deps": [
            ("review finding 3, A19, B14 item 4: 15.12.4 and its open note", 297, 310),
            ("review A19's missing dependency: 15.1.3", 52, 57),
            ("review audit A1: 15.0 Port", 32, 34),
            ("review audit: 15.1.3", 52, 57),
            ("review audit: 15.1.6", 63, 66),
            ("review finding 4: the trigger and the licence in a tick-only law, 15.12.1", 287, 288),
            ("packet B §5: §15.0", 28, 41),
            ("packet B §5: §15.1.3", 52, 57),
            ("packet B §5: §15.1.6", 63, 66),
            ("packet B §5: §15.3's read-once bullet", 122, 124),
            ("packet B §5: §15.5", 147, 167),
            ("packet B §5: §15.7.1", 178, 181),
            ("packet B §5: §15.7.5", 197, 201),
            ("packet B §5: §15.12.1-6", 287, 316),
            ("packet B §5: §15.13.7-8", 333, 357),
            ("packet B §5: §15.13.11", 368, 373),
            ("packet B §5: §15.15 row", 388, 388),
            ("packet B §5: §15.15 rows", 392, 393),
            ("packet B §5: §15.15 row", 400, 400),
            ("packet B §5: §15.15 row", 402, 402),
            ("packet E: L_r candidates", 63, 66),
            ("packet E: L_r candidates", 294, 299),
            ("packet E: L_r candidates", 311, 311),
            ("packet E: L_r candidates", 315, 315),
            ("packet E: L_r candidates", 370, 370),
            ("integration I-3: the binding place, 15.7.1", 178, 181),
            ("integration I-9: Reach shared with K-hat, 15.13.8", 351, 357),
        ],
    },
}

D2 = "research/run-1/SPEC-15-DRAFT-2.md"
D2_SHA = "43f6a725831308b9dc5b671d67b807e9366615310761fac6cf33710704ba66d5"

RULINGS2 = {   # D_r by clause name: a clause whose name starts with the given text
    "LABELS": {
        "title": "the labels' definitions (D, B1, 4a, 5c, K1), adopted without their conclusions",
        "tag": r"\b(?:PREFIX|F24)\b",   # the rulings whose labels it defines
        "terms": {
            "boundary": r"\bboundary\b",
            "exempt": r"\bexempt(?:s|ed|ion)?\b",
            "licence": r"\blicen[cs](?:e|ed|es|ing)\b",
            "closure": r"\bclosure\b",
            "Reach": r"\bReach\b",
            "may execute": r"\bmay(?: |-)execute\b",
            "fail closed": r"\bfails? closed\b",
            "REFERENCE-ONLY": r"REFERENCE-ONLY",
            "configured": r"\bconfigured\b",
        },
        "deps": [
            ("re-read 1, PREFIX-1 and PREFIX-4: the licence as ruled", "15.12 ¶ The licence as ruled"),
            ("re-read 1, PREFIX-1 and PREFIX-2: 15.13.8's closing line", '15.13 ¶ What "may execute"'),
            ("re-read 1, PREFIX-1: K-hat's tick-block rows, 15.13.8", "15.13.8"),
            ("re-read 1: 15.0 Boundary, B1's wording", "15.0 Boundary"),
            ("D's definition: 15.13.11", "15.13.11"),
        ],
    },
    "TABLE": {
        "title": "the closure's rule table",
        "tag": r"\bPREFIX\b",
        "terms": {
            "closure": r"\bclosure\b",
            "statement kind": r"\bstatement kinds?\b",
            "Reach": r"\bReach\b",
            "may execute": r"\bmay(?: |-)execute\b",
            "fail closed": r"\bfails? closed\b",
            "port declaration": r"\bport declarations?\b",
            "To": r"\bTo\b",
        },
        "deps": [
            ("re-read 1, PREFIX-3: the licence as ruled", "15.12 ¶ The licence as ruled"),
            ("re-read 1, PREFIX-13: 15.1.1, the forms", "15.1.1"),
            ("re-read 1, PREFIX-13: 15.13.6", "15.13.6"),
            ("re-read 1, PREFIX-12: 15.1.3", "15.1.3"),
            ("re-read 1, PREFIX-12: 15.1.6", "15.1.6"),
            ("re-read 1, PREFIX-12: 15.3's read-once bullet", "15.3 Read-once"),
            ("the shared reachability: 15.13.8 and its closing line", "15.13.8"),
            ("the shared reachability: 15.13.8 and its closing line", '15.13 ¶ What "may execute"'),
        ],
    },
    "V0CTL": {
        "title": "R6's row and control on the configured witness, a measured version-0 control apart",
        "tag": r"\bF24\b",
        "terms": {
            "control": r"\bcontrols?\b",
            "configured": r"\bconfigured\b",
            "measured": r"\bmeasured\b",
            "witness": r"\bwitness\b",
        },
        "deps": [
            ("re-read 1, F24-6: 15.12.6", "15.12.6"),
            ("re-read 1, F24-6: condition 1 in 15.13.11", "15.13.11"),
        ],
    },
}

D3 = "research/run-1/SPEC-15-DRAFT-3.md"
D3_SHA = "59ec11c1b7f710f5e613b9865ac447257748f8aa1c5d5f9f1919443a29575f7c"

RULINGS3 = {
    "PERFORM": {
        "title": "the table's Perform row: SPEC §3's row, the bare name included",
        "tag": r"\bPREFIX\b",
        "terms": {
            "Perform": r"\bPerform\b",
            "the name alone": r"\bname alone\b",
        },
        "deps": [
            ("re-read 2, TABLE-1: the table's Perform row", "15.12 row: Perform"),
            ("re-read 2, TABLE-1: the licence as ruled", "15.12 ¶ The licence as ruled"),
            ("re-read 2, TABLE-1: the table's last row", "15.12 row: any other kind"),
        ],
    },
}

D4 = "research/run-1/SPEC-15-DRAFT-4.md"
D4_SHA = "f4225545ffe8766580194fdf2fbfcc2c96e3a6b9808b079788eecce48864a411"

RULINGS4 = {
    "F6": {
        "title": "finding 6: read-once ports, A′ as RO′-1 to RO′-6",
        "tag": r"finding 6",
        "terms": {
            "read-once": r"\bread-once\b",
            "binds": r"\bbind(?:s|ing)?\b",
            "NOT-RUN": r"NOT-RUN|\bnot-run\b",
            "LOG-OPEN": r"LOG-OPEN",
            "malformed": r"\bmalformed\b",
            "the cut": r"\bcut\b",
            "K̂": r"K̂",
        },
        "deps": [
            ("packet C §5, packet F §5: 15.0 Port", "15.0 Port"),
            ("packet C §5, packet F §5: 15.0 Arrival", "15.0 Arrival"),
            ("packet C §5, packet F §5: 15.0 Input log", "15.0 Input log"),
            ("packet C §5, packet F §5: 15.0 Execution", "15.0 Execution"),
            ("packet C §5: 15.1.3", "15.1.3"),
            ("packet C §5: 15.1.6", "15.1.6"),
            ("packet C §5: 15.3", "§", "15.3"),
            ("packet C §5: 15.4", "§", "15.4"),
            ("packet C §5, packet F §5: 15.5", "§", "15.5"),
            ("packet C §5: 15.6", "§", "15.6"),
            ("packet C §5, packet F §5: 15.7", "§", "15.7"),
            ("packet C §5, packet F §5: 15.8", "§", "15.8"),
            ("packet C §5: 15.9", "§", "15.9"),
            ("packet C §5: 15.10", "§", "15.10"),
            ("packet C §5: 15.11", "§", "15.11"),
            ("packet F §5: the provenance line, 15.12.3", "15.12.3"),
            ("re-read 1, PREFIX-6: the licence's presupposition", "15.12 ¶ The licence as ruled"),
            ("packet F §4: 15.13.7", "15.13.7"),
            ("packet F §4: 15.13.8", "15.13.8"),
            ("packet F §4: 15.13.8's closing line", '15.13 ¶ What "may execute"'),
            ("packet F §4: 15.13.9, the row named", "15.13.9"),
            ("packet C §5: 15.13.12", "15.13.12"),
            ("packet C §5: 15.15", "§", "15.15"),
        ],
    },
}

D5 = "research/run-1/SPEC-15-DRAFT-5.md"
D5_SHA = "3322571640426cafc10f445a9d606a6df4829c4151ac30fd3ba63d5ed3f53400"

RULINGS5 = {
    "STOPROW": {
        "title": "the read-once stop's own row (his answer on F6-1)",
        "tag": r"\bF6\b",
        "terms": {
            "the read-once stop": r"read-once stop",
            "the rest of a block": r"rest of (?:a|the) block",
            "withholding": r"\bwithh(?:old|olds|olding|oldings|eld)\b",
        },
        "deps": [
            ("re-read 3, F6-1: 15.13.8's rows", "15.13.8"),
            ("re-read 3, F6-1: 15.13.9's list of rows", "15.13.9"),
        ],
    },
    "V1CHECK": {
        "title": "the read-once stop's version-1 check, owed before the pin (his answer on F6-14)",
        "tag": r"\bF6\b",
        "terms": {
            "stand-ins": r"\bstand-ins?\b",
            "the pin": r"\bpin(?:ned|s)?\b",
        },
        "deps": [
            ("re-read 3, F6-14: 15.13.8's rows", "15.13.8"),
            ("re-read 3, F6-14: what 15.15 lists open", "§", "15.15"),
        ],
    },
}

D6 = "research/run-1/SPEC-15-DRAFT-6.md"
D6_SHA = "e9e3f442bbd51ec2e5ca7a9b45027ad3a5bb82d61581b95fde36e2cb26aa76cf"

RULINGS6 = {
    "CARRIER": {
        "title": "the read-once stop's own receipt status (his answer on STOPROW-1)",
        "tag": r"\bF6\b",
        "terms": {
            "receipt": r"\breceipts?\b",
            "status": r"\bstatus(?:es)?\b",
            "LOG-OPEN": r"LOG-OPEN",
            "the read-once stop": r"read-once stop",
        },
        "deps": [
            ("re-read 4, STOPROW-1: the statuses, 15.7.5", "15.7.5"),
            ("re-read 4, STOPROW-1: the receipt's status line", "15.8 ¶ - status"),
            ("re-read 4, STOPROW-1: the stop's row, 15.13.8", "15.13.8"),
            ("re-read 4, STOPROW-1: what 15.15 lists open", "§", "15.15"),
        ],
    },
    "CONTAIN": {
        "title": "the owed version-1 check is containment (his answer on V1CHECK-2)",
        "tag": r"\bF6\b",
        "terms": {
            "version-1 check": r"version-1 check",
            "stand-ins": r"\bstand-ins?\b",
        },
        "deps": [
            ("re-read 4, V1CHECK-2: the stop's row, 15.13.8", "15.13.8"),
            ("re-read 4, V1CHECK-2: 15.15's row on the check", "15.15 row: 15.13.8"),
        ],
    },
    "ORDER": {
        "title": "check, then pin, then 1a (his answer on V1CHECK-3)",
        "tag": r"\bF6\b",
        "terms": {
            "the pin": r"\bpin(?:ned|s)?\b",
            "digest": r"\bdigest\b",
            "1a": r"\b1a\b",
        },
        "deps": [
            ("re-read 4, V1CHECK-3: the meet's digest, 15.13.4", "15.13.4"),
            ("re-read 4, V1CHECK-3: 1a's rows, 15.12.5", "15.12.5"),
            ("re-read 4, V1CHECK-3: 1a's rows, 15.12.6", "15.12.6"),
            ("re-read 4, V1CHECK-3: 1a's rows, 15.13.11", "15.13.11"),
            ("re-read 4, V1CHECK-3: the stop's row, 15.13.8", "15.13.8"),
        ],
    },
}

D7 = "research/run-1/SPEC-15-DRAFT-7.md"
D7_SHA = "130480cafc0002377088da4de99c6cb11e5ded253efa20f900eaecf54a190a60"

RULINGS7 = {
    "TEST": {
        "title": "the containment check is a fixture test on the version-1 reference (his answer on Q1)",
        "tag": r"\bF6\b",
        "terms": {
            "fixture": r"\bfixtures?\b",
            "MEASURED": r"\bMEASURED\b",
            "the version-1 reference": r"\breference\b",
            "containment": r"\bcontainment\b",
            "falsifies": r"\bfalsif\w*",
            "T10.8": r"T10\.8",
        },
        "deps": [
            ("re-read 5, CONTAIN-2: the stop's row and its check, 15.13.8", "15.13.8"),
            ("re-read 5, CONTAIN-2: T10 stays open, 15.13.10", "15.13.10"),
            ("re-read 5, CONTAIN-2: 15.15's row on the check", "15.15 row: 15.13.8"),
            ("re-read 5, ORDER-2: the order of work, 15.13.4", "15.13.4"),
            ("re-read 5, ORDER-2: 1a's rows, 15.12.5", "15.12.5"),
            ("re-read 5, ORDER-2: 1a's rows, 15.12.6", "15.12.6"),
            ("re-read 5, ORDER-2: 1a and its rows, 15.13.11", "15.13.11"),
            ("re-read 5, ORDER-2: 15.15's row on the two-commit split", "15.15 row: 15.13.11"),
        ],
    },
    "PIN": {
        "title": "findings 8 and 20 resolved before the pin (his answer on Q2)",
        "tag": r"\bF6\b|\bclaims\b|\bfindings? 8\b|\bfindings? 20\b",
        "terms": {
            "the pin": r"\bpin(?:ned|s)?\b",
            "digest": r"\bdigest\b",
            "candidate": r"\bcandidate\b",
            "finding 8": r"\bfindings? 8\b",
            "finding 20": r"\bfindings? 20\b",
            "'R'": r"'R'",
            "1a": r"\b1a\b",
        },
        "deps": [
            ("re-read 5, ORDER-1: the order of work, 15.13.4", "15.13.4"),
            ("re-read 5, ORDER-1: the stop's row, chosen from the status, 15.13.8", "15.13.8"),
            ("re-read 5, ORDER-1: the pin's reach, 15.13", "15.13 ¶ What \"may execute\""),
            ("re-read 5, ORDER-1: the statuses, 15.7.5", "15.7.5"),
            ("re-read 5, ORDER-1: the status line, 15.8", "15.8 ¶ - status"),
            ("re-read 5, ORDER-1: 'R' and the cut, 15.9", "15.9 The `'R'` event"),
            ("re-read 5, ORDER-1: 15.15's row on 'R'", "15.15 row: 15.9"),
            ("re-read 5, ORDER-1: 15.15's row on the four statuses", "15.15 row: 15.7.5 and 15.8"),
            ("re-read 5, ORDER-1: 15.15's row on the stop's form", "15.15 row: 15.5 and 15.7.5"),
        ],
    },
    "RO5": {
        "title": "RO′-5 confirmed: no fifth status word (his confirmation)",
        "tag": r"\bF6\b",
        "terms": {
            "status": r"\bstatus(?:es)?\b",
            "NOT-RUN": r"NOT-RUN",
            "LOG-OPEN": r"LOG-OPEN",
            "the read-once stop": r"read-once stop",
            "fifth status": r"fifth status",
        },
        "deps": [
            ("re-read 5, CARRIER-1: the stop, 15.7.1", "15.7.1"),
            ("re-read 5, CARRIER-1 and CARRIER-3: the statuses, 15.7.5", "15.7.5"),
            ("re-read 5, CARRIER-1: the status line, 15.8", "15.8 ¶ - status"),
            ("re-read 5, CARRIER-2: the stop's row and the NOT-RUN/LOG-OPEN row, 15.13.8", "15.13.8"),
            ("re-read 5, CARRIER-1: 15.15's row on the four statuses", "15.15 row: 15.7.5 and 15.8"),
            ("re-read 5, CARRIER-3: 15.15's row on the stop's form", "15.15 row: 15.5 and 15.7.5"),
        ],
    },
}

D8 = "research/run-1/SPEC-15-DRAFT-8.md"
D8_SHA = "53d468213392da911d3b1fc5a50597b61b5c12bbb495c1368c0032f1f0e491c0"

RULINGS8 = {
    "INPUTS": {
        "title": "every input the pinned rule reads, fixed before the pin (his answer on PIN-1 and PIN-3)",
        "tag": r"\bclaims\b|\bF6\b|\bfindings? 8\b|\bfindings? 20\b|port place|\bcounting\b",
        "terms": {
            "the pin": r"\bpin(?:ned|s)?\b",
            "digest": r"\bdigest\b",
            "candidate": r"\bcandidate\b",
            "port place": r"port place",
            "top-level": r"\btop-level\b",
            "counting": r"\bcounting\b",
            "finding 8": r"\bfindings? 8\b",
            "finding 20": r"\bfindings? 20\b",
            "'R'": r"'R'",
            "decoding": r"\bdecod\w*",
            "the format freeze": r"\bP6\b|format[- ]freeze",
        },
        "deps": [
            ("re-read 6, PIN-3: the stop row's premises, 15.13.8", "15.13.8"),
            ("re-read 6, PIN-3: the place of ports, 15.1.3", "15.1.3"),
            ("re-read 6, PIN-3: counting, 15.7.1", "15.7.1"),
            ("re-read 6, PIN-3: 15.15's row on the place", "15.15 row: 15.1.3"),
            ("re-read 6, PIN-3: 15.15's row on counting", "15.15 row: 15.7.1"),
            ("re-read 6, PIN-3: 15.15's row on the stop's premises", "15.15 row: 15.13.8"),
            ("re-read 6, PIN-1: 'R' and the cut, 15.9", "15.9 The `'R'` event"),
            ("re-read 6, PIN-1: 15.15's row on 'R'", "15.15 row: 15.9"),
            ("re-read 6, PIN-2: 15.15's row on 15.5 and 15.6", "15.15 row: 15.5 and 15.6"),
            ("re-read 6, PIN-4 and TEST-3: the order of work, 15.13.4", "15.13.4"),
            ("re-read 6, the legend's [pinned]", "preamble [pinned]"),
        ],
    },
}

D9 = "research/run-1/SPEC-15-DRAFT-9.md"
D9_SHA = "8a1ccf5ce22895d0106884b1208603315c80704f781adb87c3b2e520289d0e8e"

RULINGS9 = {
    "ROWS": {
        "title": "the principle reaches every row of CUT-0 (his clarification on INPUTS-2)",
        "tag": r"\bclaims\b|\bF6\b|\bR2\b|identity and bytes|four statuses",
        "terms": {
            "the pin": r"\bpin(?:ned|s)?\b",
            "status": r"\bstatus(?:es)?\b",
            "NOT-RUN": r"NOT-RUN",
            "LOG-OPEN": r"LOG-OPEN",
            "R2": r"\bR2\b",
            "spelling": r"\bspellings?\b",
            "statement kind": r"statement kinds?",
            "inputs": r"\binputs?\b",
        },
        "deps": [
            ("re-read 7, INPUTS-2: the order and the inputs, 15.13.4", "15.13.4"),
            ("re-read 7, INPUTS-2: the NOT-RUN/LOG-OPEN row and the test's record, 15.13.8", "15.13.8"),
            ("re-read 7, INPUTS-2: CUT-0's reach on the version-1 kinds", "15.13 ¶ What \"may execute\""),
            ("re-read 7, INPUTS-2: the statuses, 15.7.5", "15.7.5"),
            ("re-read 7, INPUTS-2: the status line, 15.8", "15.8 ¶ - status"),
            ("re-read 7, INPUTS-2: the spellings, 15.1.1", "15.1.1"),
            ("re-read 7, INPUTS-2: the closure's table, 15.12.4", "15.12.4"),
            ("re-read 7, INPUTS-2: 15.15's row on spellings", "15.15 row: 15.0 and 15.1"),
            ("re-read 7, INPUTS-2: 15.15's row on the four statuses", "15.15 row: 15.7.5 and 15.8"),
            ("re-read 7, INPUTS-1: 'R' and its frames, 15.9", "15.9 The `'R'` event"),
            ("re-read 7, INPUTS-1: 15.15's row on 'R'", "15.15 row: 15.9"),
        ],
    },
}

D10 = "research/run-1/SPEC-15-DRAFT-10.md"
D10_SHA = "c69e7e3b02542a5cb6b320de1c5994786f2425d04bbfdb1c7e45ce1741098eb7"

RULINGS10 = {
    "F8": {
        "title": "finding 8: packet G, the read-once record's line, packet D and typed values (2026-10-28, 2026-10-29)",
        "tag": r"\bfinding 8\b|identity and bytes|\bF6\b",
        "terms": {
            "status": r"\bstatus(?:es)?\b",
            "NOT-RUN": r"NOT-RUN",
            "LOG-OPEN": r"LOG-OPEN",
            "end record": r"end record",
            "the read-once record": r"read-once record",
            "load refusal": r"\bLOG-[A-Z-]+|load refusal|PORT-SIGNATURE",
            "value encoding": r"value(?:'s)? encoding|lowercase hex",
        },
        "deps": [
            ("re-read 8 and finding 8: the input log, 15.5", "§", "15.5"),
            ("finding 8: the statuses, 15.7.5", "15.7.5"),
            ("finding 8: the status line, 15.8", "15.8 ¶ - status"),
            ("finding 8: the rows chosen by the status, 15.13.8", "15.13.8"),
            ("finding 8: 15.15's rows on 15.5", "15.15 row: 15.5"),
            ("finding 8: 15.15's row on the statuses", "15.15 row: 15.7.5"),
            ("typed values: 'N''s payload, 15.9", "15.9 `'N'`"),
        ],
    },
    "F20": {
        "title": "finding 20: the cut in version 1's 'R' (F20.1 to F20.4)",
        "tag": r"\bfinding 20\b|\bP6\b",
        "terms": {
            "'R'": r"'R'",
            "the cut": r"\bcut\b",
            "frame": r"\bframes?\b",
            "decoding": r"\bdecod\w*",
        },
        "deps": [
            ("finding 20: the trace, 15.9", "§", "15.9"),
            ("finding 20: the cut and K-hat, 15.13.8", "15.13.8"),
            ("finding 20: CUT-0's reach", "15.13 ¶ What \"may execute\""),
            ("finding 20: 15.15's row on 15.9", "15.15 row: 15.9"),
        ],
    },
    "R2": {
        "title": "R2: statement kinds, spellings and reach rules, with R2.3's clarification",
        "tag": r"\bR2\b",
        "terms": {
            "spelling": r"\bspellings?\b",
            "statement kind": r"statement kinds?",
            "tick block": r"tick block",
            "port declaration": r"port declarations?",
            "reach": r"\breach\w*",
        },
        "deps": [
            ("R2: the terms, 15.0", "§", "15.0"),
            ("R2: the forms, 15.1", "§", "15.1"),
            ("R2.3: the closure's table, 15.12.4", "15.12.4"),
            ("R2.3: the licence as ruled", "15.12 ¶ The licence as ruled"),
            ("R2.3 and re-read 8's ROWS-1: CUT-0's reach", "15.13 ¶ What \"may execute\""),
            ("R2: 15.15's row on 15.0 and 15.1", "15.15 row: 15.0 and 15.1"),
        ],
    },
    "PP": {
        "title": "the port place, PP1 to PP6",
        "tag": r"port place",
        "terms": {
            "place": r"\bplaces?\b",
            "top-level": r"\btop-level\b",
            "compile code": r"PORT-PLACE|TICK-PLACE|PORT-VARIABLE|PORT-READ|REDECLARED",
        },
        "deps": [
            ("PP: the places, 15.1.3", "15.1.3"),
            ("PP: the licence's boundary", "15.12 ¶ The licence as ruled"),
            ("PP: 15.15's row on 15.1.3", "15.15 row: 15.1.3"),
        ],
    },
    "R9": {
        "title": "counting (C1 to C3) and the budget (R9, B1 to B4)",
        "tag": r"\bcounting\b|\bbudget\b|\bR9\b",
        "terms": {
            "ops": r"\bops\b",
            "count": r"\bcount(?:s|ed|ing)?\b",
            "budget": r"\bbudget\b|TICK-BUDGET",
            "tick-ops": r"tick-ops",
        },
        "deps": [
            ("counting and R9: execution, 15.7", "§", "15.7"),
            ("B3: tick-ops, 15.8", "15.8 ¶ - tick-ops"),
            ("C2: the tick line's identities, 15.10", "15.10 ¶ These must hold"),
            ("counting: 15.15's row on 15.7.1 to 15.7.3", "15.15 row: 15.7.1"),
        ],
    },
    "SESSION": {
        "title": "N2, N3 and finding 10: the session's ends",
        "tag": r"\bA2\b|session record|\bN2\b|\bN3\b",
        "terms": {
            "end()": r"end\(\)",
            "session": r"\bsessions?\b",
            "history": r"\bhistor(?:y|ies)\b",
            "verifier": r"\bverifier\b",
        },
        "deps": [
            ("N2, N3 and finding 10: the session's events, 15.3", "§", "15.3"),
            ("finding 10: the verifier, 15.4", "§", "15.4"),
            ("N2 and N3: 15.15's rows on 15.3", "15.15 row: 15.3"),
        ],
    },
    "ROWS": {
        "title": "re-read 8's three fixes (ROWS-1, ROWS-2, CHANGED-1)",
        "tag": r"@@none@@",
        "terms": {},
        "deps": [
            ("ROWS-1: CUT-0's reach on the version-1 kinds", "15.13 ¶ What \"may execute\""),
            ("ROWS-1: 15.15's row on 15.13.8", "15.15 row: 15.13.8"),
            ("ROWS-2: the inputs record, 15.13.4", "15.13.4"),
            ("CHANGED-1: the stop's NOT-RUN t, 15.7.5", "15.7.5"),
        ],
    },
}

D11 = "research/run-1/SPEC-15-DRAFT-11.md"
D11_SHA = "937499a6daa87ebeb483cb535d1dba2f20eecb4d3518b83d2598991db96524f5"

RULINGS11 = {
    "RR9": {
        "title": "his answers to re-read 9's five questions, with its drafting fixes and open items",
        "tag": r"\bF8\b|\bF20\b|\bN3\b|\bR9\b|\bR5\b|\bPP\b|\bF6\b",
        "terms": {
            "the fixed example": r"580000000000000003",
            "'N'": r"'N'",
            "budget": r"\bbudget\b",
            "tick record": r"tick records?",
            "byte grammar": r"byte grammar|draft 2",
            "exit": r"\bexit\b",
        },
        "deps": [
            ("S15.0-1: the legend", "preamble [open: X]"),
            ("S15.0-1: Prefix", "15.0 Prefix"),
            ("S15.1-1: the law's lines, 15.1.4", "15.1.4"),
            ("S15.3-1, S15.3-2: the session's events, 15.3", "§", "15.3"),
            ("S15.5-1 to S15.5-5: the input log, 15.5", "§", "15.5"),
            ("S15.3-1: the order, 15.7.1", "15.7.1"),
            ("S15.1-1: the budget, 15.7.3", "15.7.3"),
            ("S15.9-1, S15.9-2: the trace, 15.9", "§", "15.9"),
            ("S15.13-1: the pin's inputs, 15.13.4", "15.13.4"),
            ("S15.9-1: the stop's row and the cut, 15.13.8", "15.13.8"),
            ("S15.15-1: what is open, 15.15", "§", "15.15"),
        ],
    },
}

D12 = "research/run-1/SPEC-15-DRAFT-12.md"
D12_SHA = "772fda5264fd0c10c86aba95cd85e44669e4611761914700969b70fc4e86e750"

RULINGS12 = {
    "CLOSE": {
        "title": "close() refused in a law with no tick block, with re-read 10's fixes",
        "tag": r"\bA2\b|\bPP\b|\bF8\b",
        "terms": {
            "close()": r"close\(\)",
            "no tick block": r"no tick block",
            "tick record": r"tick records?|`t` line",
            "the one-shot law": r"one-shot",
        },
        "deps": [
            ("S15.3-1: the session's events, 15.3", "§", "15.3"),
            ("S15.5-1: the input log and its order, 15.5", "§", "15.5"),
            ("S15.13-1: the NOT-RUN/LOG-OPEN row, 15.13.8", "15.13.8"),
            ("S15.15-1: what is open, 15.15", "§", "15.15"),
        ],
    },
}

SETS = {
    "12": {"draft": D12, "sha": D12_SHA, "prev": D11, "rulings": RULINGS12,
           "head": "Draft 12: %d clauses; %d changed or added since draft 11 (DRAFT-12-CHANGES.md).",
           "among": "changed since draft 11", "col": "changed since draft 11",
           "union": "%d clauses are in A_CLOSE; %d in more than one set; %d of them changed since draft 11; %d of the "
                    "clauses changed since draft 11 are not in it."},
    "11": {"draft": D11, "sha": D11_SHA, "prev": D10, "rulings": RULINGS11,
           "head": "Draft 11: %d clauses; %d changed or added since draft 10 (DRAFT-11-CHANGES.md).",
           "among": "changed since draft 10", "col": "changed since draft 10",
           "union": "%d clauses are in A_RR9; %d in more than one set; %d of them changed since draft 10; %d of the "
                    "clauses changed since draft 10 are not in it."},
    "10": {"draft": D10, "sha": D10_SHA, "prev": D9, "rulings": RULINGS10,
           "head": "Draft 10: %d clauses; %d changed or added since draft 9 (DRAFT-10-CHANGES.md).",
           "among": "changed since draft 9", "col": "changed since draft 9",
           "union": "%d clauses are in A_F8, A_F20, A_R2, A_PP, A_R9, A_SESSION or A_ROWS; %d in more than one; %d of "
                    "them changed since draft 9; %d of the clauses changed since draft 9 are in none."},
    "9": {"draft": D9, "sha": D9_SHA, "prev": D8, "rulings": RULINGS9,
          "head": "Draft 9: %d clauses; %d changed or added since draft 8 (DRAFT-9-CHANGES.md).",
          "among": "changed since draft 8", "col": "changed since draft 8",
          "union": "%d clauses are in A_ROWS; %d in more than one set; %d of them changed since draft 8; %d of the "
                   "clauses changed since draft 8 are not in it."},
    "8": {"draft": D8, "sha": D8_SHA, "prev": D7, "rulings": RULINGS8,
          "head": "Draft 8: %d clauses; %d changed or added since draft 7 (DRAFT-8-CHANGES.md).",
          "among": "changed since draft 7", "col": "changed since draft 7",
          "union": "%d clauses are in A_INPUTS; %d in more than one set; %d of them changed since draft 7; %d of the "
                   "clauses changed since draft 7 are not in it."},
    "7": {"draft": D7, "sha": D7_SHA, "prev": D6, "rulings": RULINGS7,
          "head": "Draft 7: %d clauses; %d changed or added since draft 6 (DRAFT-7-CHANGES.md).",
          "among": "changed since draft 6", "col": "changed since draft 6",
          "union": "%d clauses are in A_TEST, A_PIN or A_RO5; %d in more than one; %d of them changed since draft 6; "
                   "%d of the clauses changed since draft 6 are in none."},
    "6": {"draft": D6, "sha": D6_SHA, "prev": D5, "rulings": RULINGS6,
          "head": "Draft 6: %d clauses; %d changed or added since draft 5 (DRAFT-6-CHANGES.md).",
          "among": "changed since draft 5", "col": "changed since draft 5",
          "union": "%d clauses are in A_CARRIER, A_CONTAIN or A_ORDER; %d in more than one; %d of them changed since "
                   "draft 5; %d of the clauses changed since draft 5 are in none."},
    "5": {"draft": D5, "sha": D5_SHA, "prev": D4, "rulings": RULINGS5,
          "head": "Draft 5: %d clauses; %d changed or added since draft 4 (DRAFT-5-CHANGES.md).",
          "among": "changed since draft 4", "col": "changed since draft 4",
          "union": "%d clauses are in A_STOPROW or A_V1CHECK; %d in both; %d of them changed since draft 4; %d of the "
                   "clauses changed since draft 4 are in neither."},
    "4": {"draft": D4, "sha": D4_SHA, "prev": D3, "rulings": RULINGS4,
          "head": "Draft 4: %d clauses; %d changed or added since draft 3 (DRAFT-4-CHANGES.md).",
          "among": "changed since draft 3", "col": "changed since draft 3",
          "union": "%d clauses are in A_F6; %d in more than one set; %d of them changed since draft 3; %d of the "
                   "clauses changed since draft 3 are not in it."},
    "3": {"draft": D3, "sha": D3_SHA, "prev": D2, "rulings": RULINGS3,
          "head": "Draft 3: %d clauses; %d changed or added since draft 2 (DRAFT-3-CHANGES.md).",
          "among": "changed since draft 2", "col": "changed since draft 2",
          "union": "%d clauses are in A_PERFORM; %d in more than one set; %d of them changed since draft 2; %d of the "
                   "clauses changed since draft 2 are not in it."},
    "1": {"draft": D1, "sha": D1_SHA, "prev": D0, "rulings": RULINGS,
          "head": "Draft 1: %d clauses; %d changed or added since draft 0, so owed a re-read before any ruling "
                  "(DRAFT-1-CHANGES.md gives 61 + 13 = 74).",
          "among": "among the 74", "col": "in the 74",
          "union": "%d clauses are in A_F24 or A_PREFIX; %d in both; %d of the union are among the 74; %d of the 74 "
                   "are in neither."},
    "2": {"draft": D2, "sha": D2_SHA, "prev": D1, "rulings": RULINGS2,
          "head": "Draft 2: %d clauses; %d changed or added since draft 1 (DRAFT-2-CHANGES.md).",
          "among": "changed since draft 1", "col": "changed since draft 1",
          "union": "%d clauses are in A_LABELS, A_TABLE or A_V0CTL; %d in more than one; %d of the union changed since "
                   "draft 1; %d of the clauses changed since draft 1 are in none."},
}


def units(path):
    """clause_diff.py's units, with each unit's first and last line kept."""
    lines = open(path, encoding="utf-8").read().split("\n")
    out, cur, prev_blank = [], "preamble", True
    for n, line in enumerate(lines, 1):
        m = re.match(r"## (15\.\d+) ", line)
        if m:
            cur, prev_blank = m.group(1), True
            continue
        if not line.strip():
            prev_blank = True
            continue
        starts = re.match(r"(\d+\. |- |\| |\*\*)", line)
        if starts or prev_blank or not out or out[-1]["sec"] != cur:
            out.append({"sec": cur, "text": line.strip(), "first": n, "last": n})
        else:
            out[-1]["text"] += " " + line.strip()
            out[-1]["last"] = n
        prev_blank = False
    return [u for u in out if not re.match(r"\|[-| ]+\|$", u["text"])]


def name(u):
    t = u["text"]
    m = re.match(r"(\d+)\. ", t)
    if m:
        return "%s.%s" % (u["sec"], m.group(1))
    m = re.match(r"- \*\*([^*]+?):?\*\*", t)
    if m:
        return "%s %s" % (u["sec"], m.group(1).rstrip(":"))
    m = re.match(r"\| ([^|]+?) \|", t)
    if m:
        return "%s row: %s" % (u["sec"], m.group(1)[:48])
    return "%s ¶ %s" % (u["sec"], re.sub(r"[*`]", "", t)[:48])


def tags(t):
    return re.findall(r"\[(?:ruled|open|pinned|v0|fixed)[^\]]*\]", t)


def meets(dep, u):
    """A D_r entry is (source, first line, last line), (source, the start of a clause's name), or (source, "§", a
    section's number) for every clause of that section."""
    if dep[1] == "§":
        return u["sec"] == dep[2]
    if isinstance(dep[1], str):
        return name(u).startswith(dep[1])
    return not (u["last"] < dep[1] or u["first"] > dep[2])


def main(which):
    cfg = SETS[which]
    raw = open(cfg["draft"], "rb").read()
    if hashlib.sha256(raw).hexdigest() != cfg["sha"]:
        sys.exit("REFUSED: %s is not the text ruled against, %s" % (cfg["draft"], cfg["sha"][:16]))
    u1, u0 = units(cfg["draft"]), units(cfg["prev"])
    old = {(u["sec"], re.sub(r"\s+", " ", u["text"])) for u in u0}
    for u in u1:
        u["owed"] = (u["sec"], re.sub(r"\s+", " ", u["text"])) not in old
    print(cfg["head"] % (len(u1), sum(u["owed"] for u in u1)))
    for r in cfg["rulings"].values():   # a D_r entry that names no clause is a defect of this table
        for dep in r["deps"]:
            if not any(meets(dep, u) for u in u1):
                sys.exit("REFUSED: D_r entry %r meets no clause" % (dep,))

    defs = [u for u in u1 if u["sec"] == "15.0" and u["text"].startswith("- **")]
    union = {}
    for key, r in cfg["rulings"].items():
        terms = dict(r["terms"])
        grown = True
        while grown:   # the term closure over 15.0's formal definitions
            grown = False
            for d in defs:
                for m in re.finditer(r"\*\*([^*]+?):\*\*\s*([^*]*)", d["text"]):
                    term, body = m.group(1), m.group(2)
                    if term not in terms and any(re.search(p, body) for p in terms.values()):
                        terms[term] = r"\b%s\b" % re.escape(term)
                        grown = True
        added = sorted(set(terms) - set(r["terms"]))
        rows = []
        for i, u in enumerate(u1):
            why = []
            decider = u["text"].rstrip(" |").rsplit("|", 1)[-1] if u["sec"] == "15.15" else ""
            if any(re.search(r["tag"], t) for t in tags(u["text"])) or re.search(r["tag"], decider):
                why.append("T")   # a bracket tag, or the 15.15 row's "decided by" cell
            hit = [t for t, p in terms.items() if re.search(p, u["text"])]
            if hit:
                why.append("L(" + ", ".join(hit) + ")")
            src = sorted({dep[0] for dep in r["deps"] if meets(dep, u)})
            if src:
                why.append("D(" + "; ".join(src) + ")")
            if why:
                rows.append((i, u, why))
                union.setdefault(i, set()).add(key)
        print("\n## A_r for %s\n" % r["title"])
        print("Terms the ruling defines or newly defines: %s. The closure over 15.0's definitions adds: %s.\n"
              % (", ".join(r["terms"]), ", ".join(added) if added else "none"))
        nT = sum("T" in w for _, _, w in rows)
        nL = sum(any(x.startswith("L(") for x in w) for _, _, w in rows)
        nD = sum(any(x.startswith("D(") for x in w) for _, _, w in rows)
        print("|A_r| = %d clauses (T_r %d, L_r %d, D_r %d; a clause may be in several); %d of them %s.\n"
              % (len(rows), nT, nL, nD, sum(u["owed"] for _, u, _ in rows), cfg["among"]))
        print("| # | clause | lines | %s | why |\n|---|---|---|---|---|" % cfg["col"])
        for i, u, why in rows:
            print("| %d | %s | %d-%d | %s | %s |" % (i + 1, name(u).replace("|", "/"), u["first"], u["last"],
                                                   "yes" if u["owed"] else "", " ".join(why).replace("|", "/")))
    both = [i for i, k in union.items() if len(k) >= 2]
    owed_in = sum(u1[i]["owed"] for i in union)
    print("\n## The union\n")
    print(cfg["union"] % (len(union), len(both), owed_in, sum(u["owed"] for u in u1) - owed_in))


main(sys.argv[1] if len(sys.argv) > 1 else "1")

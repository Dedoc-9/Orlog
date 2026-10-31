"""RUST-CORE-0 phase 0: do the plants of drafts 4 to 9 bite? (LAW-FORMAT-0-DRAFT-9.md section 11)

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/plant_reverts.py

Each fix is undone in a copy of format_check.py held in memory, and each plant of the fix, and each byte fixture, must
then come out other than stated. A fix may replace several things, so it is undone once for each: the depth gate
replaces draft 3's capped walk and a walk of the whole tree with no gate; the structure gate replaces draft 4's checker
(W5 and W7 found in the walk, with G8's skips), draft 4's text (W6 read on a W7 statement), and a walk of the whole tree
with W5 not a gate; the gates' precedence (the depth gate first, then the least line and W among the chain and
structure gates' failures: N1) replaces draft 5's rule (the least line and W among all three) and each of the six
orders in which the three gates could run one after another; each structure check (the chain's shape, an orphan, an
empty block) replaces that check made in the walk; W5's narrow reading of a block (N3) replaces the reading in which an
inline if's block names a clause; W5's naming as its row reads (M3) replaces each of three narrower namings; N3's
reading of an inline if's else (M4) replaces the reading in which it names. Every plant must change under at least one
undoing. And the checker is run whole once with its writer broken: the count of laws written back exactly must fall,
and the run must fail (M10). Since REREAD-9 (its NA2, his ruling on ASK 9-5), the count falls when it is below the
number of laws read, both taken from the checker's own line, never from a constant; and the same test, applied to the
unbroken checker's line, must not call it fallen.

An undoing that crashes the checker is counted apart from one that changes its report (REREAD-4's K6): a crash shows a
fix is needed, a changed report shows what the fix decides. It reads the checker's source and writes nothing. It is
evidence that the plants test what their findings say, not that the checker is right, and it is outside the core
author's reading set (D1)."""
import itertools
import os
import re
import subprocess
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(HERE, "format_check.py")
sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))

GATES_RETURN = "    if fails:\n        return\n    # phase 4"
DEPTH_RETURN = ("    if fails:                       # the depth gate first (E1(b), confirmed in N1): no W4-W13 check is "
                "made\n        return\n")
COVERAGE_OFF = [("    if missed:\n", "    if False:\n", 1)]
BLOCK_WALK = '                if b["k"] == "block":\n                    walk_seq(C[b["C"]]["children"])'


def guarded(cond):
    return [(BLOCK_WALK, '                if b["k"] == "block":\n                    if %s:\n'
                         '                        walk_seq(C[b["C"]]["children"])' % cond, 2)]


# the depth gate (E1): its failures found as the walk's, and the walk capped (draft 3) or whole
NO_DEPTH_GATE = [
    ("    depth, loops_to = {0: 0}, {0: 0}", "    deferred14 = []\n    depth, loops_to = {0: 0}, {0: 0}", 1),
    ('            fail(k + 2, 14, "a clause %d deep" % depth[k])',
     '            deferred14.append((k + 2, 14, "a clause %d deep" % depth[k]))', 1),
    ('            fail(k + 2, 14, "loops nested %d deep" % loops_to[k])',
     '            deferred14.append((k + 2, 14, "loops nested %d deep" % loops_to[k]))', 1),
    (GATES_RETURN, "    if fails:\n        return\n    fails.extend(deferred14)\n    # phase 4", 1)]
CAP = [('        for j in ks:\n            if not C[j]["absorbed"]',
        '        for j in ks:\n            if depth[j] > DEPTH_CLAUSE + 1:\n                continue\n'
        '            if not C[j]["absorbed"]', 1)]
# the chain gate (E1): its failures found as the walk's, with draft 3's skip of the chain's blocks or with none
NO_CHAIN_GATE = [
    ("    bad_ref = set() ", "    deferred = []\n    bad_ref = set() ", 1),
    ('                        fail(k + 2, 4, "an If chain names clause %d, which does not exist" % r)',
     '                        deferred.append((k + 2, 4, "an If chain names clause %d, which does not exist" % r))', 1),
    (GATES_RETURN, "    if fails:\n        return\n    fails.extend(deferred)\n    # phase 4", 1)]
# the structure gate (F1): W5 and W7 found as the walk's
STRUCTURE_IN_WALK = [
    ('                fail(k + 2, 7, "%s inline" % s["k"])', "                pass", 1),
    (GATES_RETURN, "    if any(f[1] in (4, 14) for f in fails):\n        return\n    # phase 4", 1)]
W7_RETURNS = [('            raise AssertionError("the walk met an inline %s, which gate 3 refuses" % sk)',
               '            fail(line, 7, "%s inline" % sk)\n            return', 1)]
W7_GOES_ON = [('            raise AssertionError("the walk met an inline %s, which gate 3 refuses" % sk)',
               '            fail(line, 7, "%s inline" % sk)', 1)]
G8_SKIPS = [
    ("    blocks, chain_of = [], {}", "    blocks, chain_of = [], {}\n    w5_bad = set()", 1),
    ("        ok = True\n", "        ok = True\n        n_fails = len(fails)\n", 1),
    ("                blocks.append((part[\"body\"][\"C\"], k))\n    counted = {}",
     "                blocks.append((part[\"body\"][\"C\"], k))\n        if len(fails) > n_fails:\n"
     "            w5_bad.add(k)\n    counted = {}", 1)] + guarded('k not in w5_bad and b["C"] in C')
BODYLESS_WALKED = [('                visit(C[j]["stmt"], j, False, j)\n',
                    '                visit(C[j]["stmt"], j, False, j)\n            s_ = C[j]["stmt"]\n'
                    '            if C[j]["children"] and j not in counted and not (s_ is not None and s_["k"] in '
                    '("while", "for", "procedure")):\n                walk_seq(C[j]["children"])\n', 1)]


# draft 5's W11 (K1): a procedure clause by its statement; draft 4 judged it by what the walk had met
W11_BY_WALK = [('    is_proc = P in C and C[P]["stmt"] is not None and C[P]["stmt"]["k"] == "procedure"',
                "    is_proc = P in L.procs", 1)]


def order(ranks):
    """The gates run one after another in this order: the first gate with a failure reports its least (line, W)."""
    rank = {14: ranks.index("depth"), 4: ranks.index("chain"), 5: ranks.index("structure"),
            7: ranks.index("structure")}
    return [(DEPTH_RETURN, "", 1),
            (GATES_RETURN, "    if fails:\n        fails.sort(key=lambda f: (%r[f[1]], f[0], f[1]))\n"
                           "        del fails[1:]\n        return\n    # phase 4" % rank, 1)]


# draft 5's rule (REREAD-5's L1): the least (line, W) among all three gates, the depth gate's failures among them
DRAFT5_RULE = [(DEPTH_RETURN, "", 1)]
# a structure check made in the walk, not the gate (REREAD-5's L7): its failures join the walk's
DEFER5 = [("    blocks, chain_of = [], {}", "    deferred5 = []\n    blocks, chain_of = [], {}", 1),
          (GATES_RETURN, "    if fails:\n        return\n    fails.extend(deferred5)\n    # phase 4", 1)]


def deferred(*calls):
    return DEFER5 + [(c, "deferred5.append((" + c[len("fail("):] + ")", 1) for c in calls]


SHAPE_IN_WALK = deferred(
    'fail(line, 5, "an If\'s first arm is not its own clause")',
    'fail(line, 5, "an otherwise in the If\'s own line needs one inline arm and an inline body")',
    'fail(line, 5, "clause %d in the chain is not an absorbed clause" % a)',
    'fail(line, 5, "absorbed clause %d is named twice" % a)',
    'fail(line, 5, "the chain\'s absorbed clauses are not the siblings right after it, in order")',
    'fail(line, 5, "a block names another clause than its arm\'s or else\'s own")')
ORPHAN_IN_WALK = deferred('fail(line, 5, "absorbed clause %d is in no If chain" % k)')
EMPTY_IN_WALK = DEFER5 + [
    ('fail(line, 5, "clause %d %s" % (k, "has children and no body" if C[k]["children"] else "has a body and no children"))',
     '(fails if C[k]["children"] else deferred5).append((line, 5, "clause %d %s" % (k, "has children and no body" if '
     'C[k]["children"] else "has a body and no children")))', 1)]
# W5's general reading (REREAD-5's L8, which the owner did not take): an inline if's block names a clause too
INLINE_BLOCKS_NAME = [("    blocks, chain_of = [], {}\n",
                       "    blocks, chain_of = [], {}\n"
                       "    for k_ in range(1, L.n + 1):\n"
                       "        for s_, ctx_, inline_ in statements_of(k_):\n"
                       "            if inline_ and s_[\"k\"] == \"if\":\n"
                       "                for part_ in s_[\"arms\"] + ([s_[\"els\"]] if s_[\"els\"] is not None else []):\n"
                       "                    if part_[\"body\"][\"k\"] == \"block\" and part_[\"body\"][\"C\"] in C:\n"
                       "                        blocks.append((part_[\"body\"][\"C\"], k_))\n", 1)]

# draft 7, M3: the three narrower namings W5's row, read as written, replaces
FIRST_ARM_SOUND = [('            if C[first]["absorbed"]:\n                if first in chain_of:\n'
                    '                    fail(line, 5, "absorbed clause %d is named twice" % first)\n'
                    '                else:\n                    chain_of[first] = k\n', "", 1)]
BAD_NAMING = '                if part["C"] != k and part["C"] in C and C[part["C"]]["absorbed"]:\n'
FIRST_ARM_BAD = [(BAD_NAMING, BAD_NAMING.replace(" and C[part", ' and part is not s["arms"][0] and C[part'), 1)]
BAD_NAMES_NONE = [(BAD_NAMING + '                    chain_of.setdefault(part["C"], k)\n',
                   '                pass\n', 1)]
# draft 7, M4: N3's other reading for an inline if's arms and else: they name absorbed clauses too
INLINE_ARMS_NAME = [("    blocks, chain_of = [], {}\n",
                     "    blocks, chain_of = [], {}\n"
                     "    for k_ in range(1, L.n + 1):\n"
                     "        for s_, ctx_, inline_ in statements_of(k_):\n"
                     "            if inline_ and s_[\"k\"] == \"if\":\n"
                     "                for part_ in s_[\"arms\"] + ([s_[\"els\"]] if s_[\"els\"] is not None else []):\n"
                     "                    if part_[\"C\"] != k_ and part_[\"C\"] in C and C[part_[\"C\"]][\"absorbed\"]:\n"
                     "                        chain_of.setdefault(part_[\"C\"], k_)\n", 1)]
# draft 8, E1 and E2: draft 7's readings, put back
DISTINCT_IDS = [("        n = L.n_declared            # draft 8, E1: the i-th declaration the walk meets has id i, "
                 "a repeated one counted\n        L.n_declared += 1\n", "        n = len(L.vars)\n", 1)]
TYPED_AS_MET = [("                t = static.get(name)        # draft 8, E2: its first define's type, wherever the use "
                 "stands\n", "                t = L.rule_types.get(name)\n", 1)]
WHOLE_SET_CHECK = [('            if s["i"] is not None and ti is not None and ti != "int":\n'
                    '                fail(line, 9, "an indexed %s with a %s index" % (sk, ti))\n'
                    '            if tv is not None:\n                if s["i"] is None:\n                    slot = tv\n'
                    '                elif tv not in LIST_TYPES:\n'
                    '                    fail(line, 9, "an indexed %s on %s" % (sk, tv))\n'
                    '                else:\n                    slot = tv[len("list-"):]\n',
                    '            if tv is not None:\n                if s["i"] is None:\n                    slot = tv\n'
                    '                elif ti is not None and (ti != "int" or tv not in LIST_TYPES):\n'
                    '                    fail(line, 9, "an indexed %s on %s" % (sk, tv))\n'
                    '                else:\n'
                    '                    slot = tv[len("list-"):] if tv in LIST_TYPES else None\n', 1)]
# draft 9, G: draft 8's typing put back, each part alone and both together: a self-using first define typed by its
# form (ZA2); a rule typed by its first derived define, a later one where the first is underived (ZA1)
SELF_USE_TYPED = [("            if k == first_define.get(name) and name in self_using:\n"
                   "                te = None                       # draft 9, G: its value's type is underived, "
                   "whatever its form\n", "", 1)]
FIRST_DERIVED = [("                if k == first_define.get(name):\n"
                  "                    L.rule_types[name] = te     # draft 9, G (ZA1): derivation 17, the first define's, "
                  "never a later one's\n", "                L.rule_types.setdefault(name, te)\n", 1)]
# draft 9, G (ZA3): draft 8's promote, its own parts made only where its place's type is derived
PROMOTE_GATED = [("            if ta is not None and ta != \"int\":\n"
                  "                fail(line, 9, \"a promote of %s\" % ta)\n"
                  "            if e[\"target\"] not in (\"fix\", \"float\"):\n"
                  "                fail(line, 9, \"a promote to %s\" % e[\"target\"])\n"
                  "            if promote_to is not UNDERIVED and (promote_to is None or e[\"target\"] != promote_to):\n"
                  "                fail(line, 9, \"a promote where SPEC §5 puts none\")\n",
                  "            if promote_to is UNDERIVED:\n                pass\n"
                  "            elif promote_to is None or e[\"target\"] != promote_to:\n"
                  "                fail(line, 9, \"a promote where SPEC §5 puts none\")\n"
                  "            elif ta is not None and ta != \"int\":\n"
                  "                fail(line, 9, \"a promote of %s\" % ta)\n", 1)]
# his rulings on the ruling sheet (2026-10-31): the reading he did not choose for each of A to D put back
RS_A_TYPE_PART = [('            parts = [(op not in ("neg", "abs", "sqrt"), t in res), (ta is not None, ta in opnd)]\n',
                   '            parts = [(True, t in res), (ta is not None, ta in opnd)]\n', 1)]
RS_B_PER_OPERAND = [('                parts = [(True, t == "bool"), (da and db, ta == tb and ta in NUMERIC)]\n',
                     '                parts = [(True, t == "bool"), (da, ta in NUMERIC), (db, tb in NUMERIC), '
                     '(da and db, ta == tb)]\n', 1),
                    ('                parts = [(True, t == "bool"), (da and db, ta == tb and ta in kinds)]\n',
                     '                parts = [(True, t == "bool"), (da, ta in kinds), (db, tb in kinds), '
                     '(da and db, ta == tb)]\n', 1)]
# C's reading (i): a variable the walk has not met takes the type its declaration had in the last walk (the naive
# form, which never settles on some of R6's mutants; it is run here on its plant alone)
RS_C_ANY_CLAUSE = [('            fail(line, 8, "variable %d used before it is declared" % v)\n            return None\n',
                    '            fail(line, 8, "variable %d used before it is declared" % v)\n'
                    '            return static_vars.get(v)\n', 1),
                   ("        if L.rule_types == static:\n            break\n        static = dict(L.rule_types)\n",
                    "        new_vars = {k: d[\"type\"] for k, d in L.var.items()}\n"
                    "        if L.rule_types == static and new_vars == static_vars:\n            break\n"
                    "        static = dict(L.rule_types)\n        static_vars.clear()\n        static_vars.update(new_vars)\n",
                    1),
                   ("    static = {}\n    mark = len(fails)\n", "    static = {}\n    static_vars = {}\n    mark = len(fails)\n", 1)]
# C's reading (ii): a variable not in scope at the use has no type
RS_C_SCOPE = [('            fail(line, 8, "variable %d used outside its scope" % v)\n        return L.var[v]["type"]\n',
               '            fail(line, 8, "variable %d used outside its scope" % v)\n            return None\n'
               '        return L.var[v]["type"]\n', 1)]
RS_D_LAST = [("            return                  # his ruling D: the first declaration the walk meets keeps the id's "
              "type\n", '            L.var[v]["type"] = t\n            return\n', 1)]
# REREAD-8's ZA5: draft 7's readings of E1 for musts and claims, and W9's parts whole or nothing, each put back
ZA5_MUSTS = [('            if s["M"] != L.n_musts:      # draft 8, E1: counted as met, as variables are\n'
              '                fail(line, 8, "must %d where %d is next in the walk" % (s["M"], L.n_musts))\n'
              '            L.n_musts += 1\n',
              '            if s["M"] != len(L.musts):\n'
              '                fail(line, 8, "must %d where %d is next in the walk" % (s["M"], len(L.musts)))\n', 1)]
ZA5_CLAIMS = [('            if s["K"] != L.n_claims:     # draft 8, E1: counted as met, as variables are\n'
               '                fail(line, 8, "claim %d where %d is next in the walk" % (s["K"], L.n_claims))\n'
               '            L.n_claims += 1\n',
               '            if s["K"] != len(L.claims):\n'
               '                fail(line, 8, "claim %d where %d is next in the walk" % (s["K"], len(L.claims)))\n', 1)]
ZA5_BINARY = [('            if not all(ok for made, ok in parts if made):\n'
               '                fail(line, 9, "%s on %s and %s as %s" % (op, ta, tb, t))\n',
               '            if da and db and not all(ok for made, ok in parts):\n'
               '                fail(line, 9, "%s on %s and %s as %s" % (op, ta, tb, t))\n', 1)]
ZA5_UNARY = [('            if not all(ok for made, ok in parts if made):\n'
              '                fail(line, 9, "%s on %s as %s" % (op, ta, t))\n',
              '            if ta is not None and not all(ok for made, ok in parts):\n'
              '                fail(line, 9, "%s on %s as %s" % (op, ta, t))\n', 1)]
ZA5_ITEM = [('            if ti is not None and ti != "int":\n                fail(line, 9, "item %s of %s" % (ti, tv))\n'
             '            if tv is not None:\n                if tv not in LIST_TYPES:\n'
             '                    fail(line, 9, "item %s of %s" % (ti, tv))\n',
             '            if tv is not None:\n                if ti is not None and (ti != "int" or tv not in LIST_TYPES):\n'
             '                    fail(line, 9, "item %s of %s" % (ti, tv))\n                if tv not in LIST_TYPES:\n'
             '                    pass\n', 1)]
ZA5_LIST_OF = [('            if (tn is not None and tn != "int") or (tv is not None and tv not in ELEMS):\n',
                '            if tn is not None and tv is not None and (tn != "int" or tv not in ELEMS):\n', 1)]
# draft 8, V4: the other reading of each, which agrees with the text as well
NO_PROC_RESET = [("        loops_to[k] = 0 if is_proc else loops_to[p] + (1 if is_loop else 0)\n",
                  "        loops_to[k] = loops_to[p] + (1 if is_loop else 0)\n", 1)]
OWN_BLOCKS_ONLY = [('                    fail(line, 5, "a block names another clause than its arm\'s or else\'s own")\n'
                    '                blocks.append((part["body"]["C"], k))\n',
                    '                    fail(line, 5, "a block names another clause than its arm\'s or else\'s own")\n'
                    '                if part["body"]["C"] == part["C"]:\n'
                    '                    blocks.append((part["body"]["C"], k))\n', 1)]
# draft 8, V5: a reader of fixed-width numbers, which refuses rather than crashes: an n wider than 64 bits is W2, a
# clause number wider than 20 digits W1, a label part wider than 64 bits W2, and Python's int-string limit is kept
LABEL_NEED = "    need(isinstance(x, str) and LABEL.match(x) is not None, 2, \"not a canonical label: %r\" % (x,))\n"
FIXED_WIDTH = [("    sys.set_int_max_str_digits(0)\n", "", 1),
               ("    return int(x)\n", "    need(len(x) <= 20 and int(x) < 1 << 64, 2, \"a number wider than 64 bits\")\n"
                                     "    return int(x)\n", 1),
               ("            need(int(m.group(1)) == k, 1,", "            need(len(m.group(1)) <= 20 and int(m.group(1)) == k, 1,",
                1),
               (LABEL_NEED, LABEL_NEED + "    need(all(len(p) <= 20 and int(p) < 1 << 64 for p in x.split(\".\")), 2, "
                                         "\"a label part wider than 64 bits\")\n", 1)]
WRITE_BROKEN = ('    return ("\\n".join(out) + "\\n").encode("ascii")\n',
                '    return ("\\n".join(out) + "\\nX").encode("ascii")\n')

PRECEDENCE = ["N1 gates: "]
REVERTS = [   # (the fix undone, [(its text, what replaces it, how many times)], the plants' prefixes, the fixtures')
    ("E1 undone: draft 3's capped walk, no depth gate", NO_DEPTH_GATE + CAP + COVERAGE_OFF,
     ["J1:", "H2: 30,000 nested", "N1 gates: a chain on line 3", "N1 gates: a W7 inline on line 3"], []),
    ("E1 undone: the whole tree walked, no depth gate", NO_DEPTH_GATE,
     ["J1:", "H2: 30,000 nested", "N1 gates: a chain on line 3", "N1 gates: a W7 inline on line 3"], []),
    ("E1 undone: draft 3's skip of a W4 chain", NO_CHAIN_GATE + guarded('k not in bad_ref and b["C"] in C') + COVERAGE_OFF,
     ["J7:", "K6:"], []),
    ("E1 undone: no chain gate, nothing skipped", NO_CHAIN_GATE + guarded('b["C"] in C') + COVERAGE_OFF,
     ["J7:", "K6:"], []),
    ("F1 undone: draft 4's checker", STRUCTURE_IN_WALK + W7_RETURNS + G8_SKIPS + W11_BY_WALK + COVERAGE_OFF,
     ["K1:", "K4:"], []),
    ("K1 undone alone: W11 by what the walk has met", W11_BY_WALK, ["K1:"], []),
    ("F1 undone: draft 4's text, W6 read on a W7 one", STRUCTURE_IN_WALK + W7_GOES_ON + G8_SKIPS + COVERAGE_OFF,
     ["K1:", "K4:"], []),
    ("F1 undone: W5 in a whole walk, bodiless ones too", STRUCTURE_IN_WALK + W7_RETURNS + BODYLESS_WALKED + COVERAGE_OFF,
     ["K1:", "K4:"], []),
] + [("N1 undone: draft 5's rule, the least (line, W) among all three", DRAFT5_RULE, PRECEDENCE, [])] + [
    ("N1 undone: the gates in order %s" % ", ".join(p), order(list(p)), PRECEDENCE, [])
    for p in itertools.permutations(("depth", "chain", "structure"))] + [
    ("L7 undone: the chain's shape checked in the walk", SHAPE_IN_WALK + COVERAGE_OFF, ["L7: a chain whose"], []),
    ("L7 undone: an orphan checked in the walk", ORPHAN_IN_WALK + COVERAGE_OFF, ["L7: an absorbed clause"], []),
    ("L7 undone: an empty block checked in the walk", EMPTY_IN_WALK + COVERAGE_OFF, ["L7: a block naming"], []),
    ("N3 undone: an inline if's block names its clause", INLINE_BLOCKS_NAME, ["N3:"], []),
    ("M3 undone: a sound chain's first arm names nothing", FIRST_ARM_SOUND, ["M3:"], []),
    ("M3 undone: a W4 chain's first arm names nothing", FIRST_ARM_BAD, ["M3:"], []),
    ("M3 undone: a W4 chain names nothing", BAD_NAMES_NONE, ["M3:"], []),
    ("M4 undone: an inline if's arms and else name", INLINE_ARMS_NAME, ["M4:"], []),
    ("E1 undone: ids counted by distinct id", DISTINCT_IDS, ["E1:"], []),
    ("E2 undone: a rule typed as the walk meets it", TYPED_AS_MET, ["E2: a rule used"], []),
    ("E2 undone: an indexed set's W9 whole or not at all", WHOLE_SET_CHECK, ["E2: an indexed"], []),
    ("V4 undone: W14(b) not reset at a procedure", NO_PROC_RESET, ["V4: W14(b)"], []),
    ("V4 undone: only a block naming its own clause", OWN_BLOCKS_ONLY, ["V4: a block"], []),
    ("V5: J9 under a fixed-width reader, no crash", FIXED_WIDTH, ["J9:"], []),
    ("G undone: a self-using first define typed by its form", SELF_USE_TYPED,
     ["G: a first define that uses", "G: two first defines that use", "G: two rules each with"], []),
    ("G undone: a rule typed by its first derived define", FIRST_DERIVED,
     ["G: a rule typed by its first define", "G: two rules each with"], []),
    ("G undone: draft 8's typing, both parts", SELF_USE_TYPED + FIRST_DERIVED,
     ["G: a first define that uses", "G: two first defines that use", "G: a rule typed by its first define",
      "G: two rules each with"], []),
    ("G undone: a promote's parts gated by its place", PROMOTE_GATED, ["G: a promote"], []),
    # draft 9, H: W14(c) at 91, moved back to draft 8's 130 and down to 90 (which refuses a line the front end writes)
    ("H undone: W14(c) at draft 8's 130", [("DEPTH_PARENS = 24, 16, 91 ", "DEPTH_PARENS = 24, 16, 130 ", 1)],
     ["G9: a clause line nested 92", "H5: an unbalanced line whose count exceeds"], []),
    ("H undone: W14(c) at 90", [("DEPTH_PARENS = 24, 16, 91 ", "DEPTH_PARENS = 24, 16, 90 ", 1)],
     ["H5: an unbalanced line whose count never"], ["a clause line nested exactly 91"]),
    ("RS-A undone: a part on <type> alone for neg", RS_A_TYPE_PART, ["RS-A"], []),
    ("RS-B undone: a comparison's kind per operand", RS_B_PER_OPERAND, ["RS-B"], []),
    ("RS-C undone: reading (i), any clause declares", RS_C_ANY_CLAUSE,
     ["RS-C: a first define reads a variable the walk meets later"], []),
    ("RS-C undone: reading (ii), in scope at the use", RS_C_SCOPE,
     ["RS-C: a first define reads a variable met earlier"], []),
    ("RS-D undone: the last declaration types the id", RS_D_LAST, ["RS-D"], []),
    ("ZA5 undone: musts counted by distinct id", ZA5_MUSTS, ["ZA5: E1 musts"], []),
    ("ZA5 undone: claims counted by distinct id", ZA5_CLAIMS, ["ZA5: E1 claims"], []),
    ("ZA5 undone: a binary's W9 whole or nothing", ZA5_BINARY, ["ZA5: + int"], []),
    ("ZA5 undone: a unary's W9 whole or nothing", ZA5_UNARY, ["ZA5: not int"], []),
    ("ZA5 undone: item's W9 whole or nothing", ZA5_ITEM, ["ZA5: item"], []),
    ("ZA5 undone: list-of's W9 whole or nothing", ZA5_LIST_OF, ["ZA5: list-of"], []),
] + [
    ("J8 undone: under the decimals clause's mode",
     [('    dec_type = "fix" if L.mode == "fixed" else "float"',
       '    dec_type = "fix" if (C[decimals_at[0]]["stmt"]["mode"] if decimals_at else "fixed") == "fixed" else "float"',
       1)], ["J8:"], []),
    ("J9 undone: Python's int-string limit kept", [("    sys.set_int_max_str_digits(0)\n", "", 1)], ["J9:"], []),
    ("J11 undone: no skip after a backslash",
     [('            if ch == "\\\\":\n                i += 2\n                continue\n', "", 1)], ["J11:"],
     ["an escaped quote"]),
]


def load(src, name):
    m = types.ModuleType(name)
    m.__file__ = SRC
    exec(compile(src, SRC, "exec"), m.__dict__)
    return m


def outcome(m, raw):
    try:
        m.read(raw)
        return "accepted"
    except m.Refused as r:
        return "W%d line %d" % (r.w, r.line)
    except Exception as e:                   # a crash is recorded as such, never as a refusal
        return "CRASHED (%s)" % type(e).__name__


def main():
    with open(SRC, encoding="utf-8") as f:
        text = f.read()
    base = load(text, "fc_base")
    print("THE PLANTS OF DRAFTS 4 TO 9, EACH FIX UNDONE IN MEMORY (research/rust-core/plant_reverts.py)")
    print("Python's recursion limit: %d; int-string limit: %d" % (sys.getrecursionlimit(),
                                                                 sys.get_int_max_str_digits()))
    bad, bitten = 0, {}
    for name, pairs, prefixes, fixtures in REVERTS:
        src, ok = text, True
        for old, new, count in pairs:
            if src.count(old) != count:
                ok = False
                break
            src = src.replace(old, new)
        if not ok:
            print("%-50s a fix's text is not found as often as stated: NOT RUN" % name)
            bad += 1
            continue
        m = load(src, "fc_undone")
        rows = [(w, line, what, kind[1]) for w, line, what, kind in base.PLANTS
                if any(what.startswith(p) for p in prefixes)]
        rows += [(None, None, "fixture: " + n, raw) for n, raw in base.BYTE_FIXTURES
                 if any(n.startswith(p) for p in fixtures)]
        if not rows:
            print("%-50s names no plant: NOT RUN" % name)
            bad += 1
        for w, line, what, raw in rows:
            want = "accepted" if w is None else "W%d line %d" % (w, line)
            fixed, undone = outcome(base, raw), outcome(m, raw)
            bad += fixed != want
            bitten.setdefault(what, [])
            how = "same"
            if fixed == want and undone != want:
                how = "BITES BY A CRASH" if undone.startswith("CRASHED") else "BITES"
                bitten[what].append(how)
            print("%-50s %-56s as stated %-12s undone %-26s %s" % (name, what[:56], fixed, undone, how))
    for what, hows in sorted(bitten.items()):
        if not hows:
            bad += 1
            print("   NO UNDOING CHANGES IT: %s" % what)
    # draft 7, M10: the checker run whole with its writer broken; the write-back count must fall and the run fail
    old, new = WRITE_BROKEN
    if text.count(old) != 1:
        print("M10 undone: the writer's text is not found once: NOT RUN")
        bad += 1
    else:
        def checker_run(replace):
            code = ("import sys, types; src = open(%r, encoding='utf-8').read().replace(%r, %r); "
                    "m = types.ModuleType('__main__'); m.__file__ = %r; sys.argv = [%r]; "
                    "exec(compile(src, %r, 'exec'), m.__dict__)" % (SRC, old, replace, SRC, SRC, SRC))
            env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
            p = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, env=env, cwd=ROOT)
            lines = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
            count = [ln for ln in lines if ln.startswith("read, W1-W14 passed:")]
            final = [ln for ln in lines if ln.startswith("FORMAT CHECK")]
            return p.returncode, (count[0] if count else ""), (final[0] if final else "")

        def fell(count_line):
            """REREAD-9's NA2 (his ruling on ASK 9-5): the count written back exactly is below the number of laws
            read, both read from the line itself, never against a constant."""
            m = re.search(r"passed: \d+ of (\d+); written back exactly \(.*\): (\d+) of (\d+)$", count_line)
            return bool(m) and m.group(1) == m.group(3) and int(m.group(2)) < int(m.group(1))

        rc_b, count_b, final_b = checker_run(new)
        rc_u, count_u, final_u = checker_run(old)     # the unbroken checker: the test must not call its count fallen
        failed = " FAILED:" in final_b and rc_b != 0
        meaningful = bool(count_u) and not fell(count_u) and rc_u == 0
        what = "the write-back count of the laws read"
        bitten.setdefault(what, [])
        if fell(count_b) and failed and meaningful:
            bitten[what].append("BITES")
        else:
            bad += not meaningful
        print("%-50s %-56s %s" % ("M10 undone: the writer appends a byte", what,
                                  ("BITES: %s, where the unbroken checker's is %s" % (
                                      count_b.split(": ")[-1].strip(), count_u.split(": ")[-1].strip()))
                                  if fell(count_b) and failed and meaningful else
                                  "same" if meaningful else "NOT MEANINGFUL: the test calls the unbroken count fallen"))
    by_crash_only = sorted(w for w, h in bitten.items() if h and all(x == "BITES BY A CRASH" for x in h))
    print("int-string limit after every read: %d" % sys.get_int_max_str_digits())
    print("changed only by a crash of an undone checker: %s" % ("; ".join(by_crash_only) if by_crash_only else "none"))
    print("PLANT REVERTS %s: %d plants and fixtures, %d changed by at least one undoing, %d of them only by a crash" % (
        "HELD" if bad == 0 else "FAILED", len(bitten), sum(1 for v in bitten.values() if v), len(by_crash_only)))
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()

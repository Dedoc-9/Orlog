"""Write court/record.json: the first court's arguments and attacks, as the judge reads them.

Edition-1 claims are attacked by the findings that defeat or narrow them. Edition-2 claims are new arguments,
narrowed to what survived; a finding attacks an edition-2 claim only if it still applies to the narrowed text.
No finding was rebutted: each was conceded or repaired (court/RECORD.md says which).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "claims.json"), "rb") as fh:
    ed1 = json.loads(fh.read().decode("utf-8"))

args = {}
for k, text in ed1.items():
    args["ed1-" + k] = {"by": "doctrine", "text": "edition 1: " + text}
args["ed1-S0"] = {"by": "doctrine", "text": "edition 1 section 0: the horns cite Loeb, Montague, Aumann as theorems at work"}
args["ed1-S2"] = {"by": "doctrine", "text": "edition 1 section 2: what Orlog does that the lineage did not (unqualified)"}
args["ed1-S5"] = {"by": "doctrine", "text": "edition 1 section 5: 78/78 and 9 plants (typed counts)"}
args["ed1-S7"] = {"by": "doctrine", "text": "edition 1 section 7: Kleene and Damm wording"}
args["ed1-S8"] = {"by": "doctrine", "text": "edition 1 section 8: the non-claims in one place"}
args["ed1-IMPL"] = {"by": "doctrine", "text": "edition 1 implementation: every program the spec admits compiles, and runs "
                                              "identically on four executions; every invalid one is refused"}

logic = {
    "L1": ("IMPRECISION", ["ed1-S0"]), "L2": ("OVERREACH", ["ed1-T0"]), "L3": ("FATAL", ["ed1-T1", "ed1-P2"]),
    "L4": ("OVERREACH", ["ed1-T2", "ed1-P3"]), "L5": ("OVERREACH", ["ed1-T2"]),
    "L6": ("FATAL", ["ed1-T3", "ed1-P4"]), "L7": ("OVERREACH", ["ed1-T3"]), "L8": ("OVERREACH", ["ed1-T3", "ed1-P4"]),
    "L9": ("IMPRECISION", ["ed1-T4"]), "L10": ("OVERREACH", ["ed1-T4", "ed1-P1"]), "L11": ("IMPRECISION", ["ed1-T4"]),
    "L12": ("FATAL", ["ed1-T6", "ed1-IMPL"]), "L13": ("OVERREACH", ["ed1-T6"]), "L14": ("IMPRECISION", ["ed1-T7"]),
    "L15": ("IMPRECISION", ["ed1-T8", "ed1-P5"]), "L16": ("FATAL", ["ed1-T9"]),
    "L17": ("OVERREACH", ["ed1-T2", "ed1-IMPL"]), "L18": ("OVERREACH", ["ed1-S8"]), "L19": ("IMPRECISION", ["ed1-S5"]),
    "L20": ("IMPRECISION", ["ed1-S7"]),
}
for k, (sev, targets) in logic.items():
    args[k] = {"by": "prosecution-logic", "text": "%s %s (court/prosecution-logic.md)" % (k, sev), "targets": targets}

novelty = {
    "N1": ["ed1-P1"], "N2": ["ed1-P1"], "N3": ["ed1-P1"], "N4": ["ed1-P1"], "N5": ["ed1-P1"], "N6": ["ed1-P1"],
    "N7": ["ed1-P2"], "N8": ["ed1-P2"], "N9": ["ed1-P2"], "N10": ["ed1-P3"], "N11": ["ed1-P3"], "N12": ["ed1-P3"],
    "N13": ["ed1-P1", "ed1-P3", "ed1-P5", "ed1-NF"], "N14": ["ed1-P4"], "N15": ["ed1-P4"], "N16": ["ed1-P4"],
    "N17": ["ed1-NF", "ed1-P5"], "N18": ["ed1-NF", "ed1-P5"], "N19": ["ed1-P5", "ed1-T8"], "N20": ["ed1-P5", "ed1-T8"],
    "N21": [], "N22": [], "N23": [], "N24": [], "N25": ["ed1-S2"],
}
for k, targets in novelty.items():
    sev = "NO-PRIOR-ART-FOUND" if not targets and k != "N21" else ("DEFEATS" if k in ("N1", "N2", "N3", "N4") else
                                                                    "NARROWS")
    args[k] = {"by": "prosecution-novelty", "text": "%s %s (court/prosecution-novelty.md)" % (k, sev),
               "targets": targets}

redteam = ["E1 equality with promotion crashed the compiler", "E2 rules in procedures or rules crashed the lowering",
           "E3 children of an inline Otherwise were never checked or run",
           "E10 deep If chains broke the Python backend and the lowering's recursion",
           "E13 a second seal line silently overrode the first", "E15 a second oracle silently overrode the first",
           "E16 procedure names were collected case-sensitively and from nested clauses",
           "E17 NFC in code turned a Kelvin sign into K and a Greek question mark into ;"]
for item in redteam:
    k = item.split(" ")[0]
    args[k] = {"by": "redteam", "text": item + " (court/redteam-eng/)", "targets": ["ed1-IMPL"]}
args["TW37"] = {"by": "twin", "text": "twin note 37: 'is not E' op count underdetermined by SPEC v0", "targets": ["ed1-IMPL"]}
args["TW38"] = {"by": "twin", "text": "twin note 38: a float literal beyond binary64 crashed the compiler",
                "targets": ["ed1-IMPL"]}

ed2 = {
    "T0": "what is computed (integrity, formal truth per run) and what is not (intent); no theorem instantiated",
    "T1": "certificates checked at run time (certifying algorithms; LCF discipline); no construct refers to the checker",
    "T2": "standing never exceeds channel; grounding binds to the claim's own seal; computation never grounds",
    "T3": "a counted reading (CHEAPER / NOT CHEAPER / CLAUSE NOT RUN) at this input; not little-oh",
    "T4": "circular support as Fitting's Kripke-Kleene undefined set (prior art), VACUOUS rule, declared premises only",
    "T5": "determinism by construction; four-way identity here; 0 FMA in generated C; floats in identity a fork",
    "T6": "the door never moves a literal boundary, refuses non-ASCII in code before normalizing; retraction DECLARED",
    "T7": "reversibility and momentum are properties of the update (Newton III, not Noether)",
    "T8": "three spellings, one law-seal (one program); names are in the law; prior art ALGOL 60, Dhall, Unison",
    "T9": "chaos magnifies a recurring difference; a single one-ulp difference is erased about a quarter of the time",
    "P": "applications and the combination may be new; mechanisms are prior art; nearest neighbour Lara (2026)",
    "IMPL": "edition 2 implementation: each repaired finding is held by a self-test row (and a plant where a defect "
            "could return silently); four-way identity on the corpus, refusals and red-team fixtures",
}
for k, text in ed2.items():
    args["ed2-" + k] = {"by": "doctrine", "text": "edition 2: " + text}

# --- Round 2 (2026-11-09): the ten re-verified October-25 HOLDS findings, as a documentation of
# repairs (owner ruled S1-S4 as amended). Each finding attacked edition-2's implementation claim; the
# repair that resolved it, cited by its commit, defeats it, so ed2-IMPL survives IN and the verdict
# delta on it is empty. Evidence: court/redteam-eng/FINDINGS.md (HOLDS 2026-10-25) and the archived
# re-verification (COURT-ROUND-2-REVERIFICATION-RESULTS-2026-11-09.md): all ten RESOLVED at e2b40ee,
# self-test 211/211, re-measured in a clean clone before this patch. A finding left unresolved would
# stand, move ed2-IMPL OUT, and halt the closeout; none does.
round2 = {
    "E7":  ("E7 the arbiter read non-byte-identical receipts (CR LF, no final LF, an injected 'backend' line) as agreeing",
            "fc19339 (receipt_core: byte-exact core comparison)"),
    "E8":  ("E8 a backend that failed to build flipped REFERENCE-DISSENT into BACKEND-DISSENT, masking a reference dissent",
            "b4eaf11 (a failed build counted neither agreeing nor dissenting: INCOMPLETE)"),
    "E9":  ("E9 a curly quote inside a straight-quoted literal closed it, so the literal's contents changed (DOCTRINE T6)",
            "b4eaf11 (the door's literal segmentation, canon.py)"),
    "E11": ("E11 C99 and Rust failed on a non-ASCII work-folder path: host-dependent (RUNTIME-SPEC 1)",
            "b4eaf11 (arbiter run folders) with fc19339 (the C runtime)"),
    "E19": ("E19 invisible characters inside a literal passed through unseen: the door's INVISIBLE set was too small",
            "b4eaf11 (the door, canon.py)"),
    "E20": ("E20 labels '(given 2)' and '(given 02)' gave different law-seals, and a reference refused UNKNOWN-CLAUSE",
            "fc19339 (label parts compare as integers, sema.py; amendment 6)"),
    "E21": ("E21 the C runtime leaked: orl_s_take copies were never freed (already rt_c/NOTES.md finding 8)",
            "fc19339 (every heap text and list has one owner)"),
    "E23": ("E23 three refusals (NESTING-DEPTH, LOOP-NESTING, QUOTE-BOUNDARY) were not listed in the specification",
            "fc19339 (SPEC 14 lists and places them)"),
    "E24": ("E24 a Python-only IndentationError diverged from the other backends on deep nested 'and' inside loops",
            "fc19339 (EXPRESSION-DEPTH raised at the shared front end, SPEC 14)"),
    "E25": ("E25 a deep nesting of parentheses raised RecursionError with no refusal",
            "fc19339 (EXPRESSION-DEPTH, EXPR_NEST_MAX)"),
    "E26": ("E26 a false LITERAL-NOT-NFC note was logged on a line with no literal (a regression of the E17 fix)",
            "b4eaf11 (the door, canon.py)"),
}
for k, (text, repair) in round2.items():
    args["R2-" + k] = {"by": "redteam-round2",
                       "text": "%s (court/redteam-eng/FINDINGS.md; HOLDS at 2026-10-25)" % text,
                       "targets": ["ed2-IMPL"]}
    args["R2-" + k + "-fixed"] = {"by": "repair",
                                  "text": "resolved at %s; re-verified RESOLVED at e2b40ee on 2026-11-09, held by a self-test row (SELFTEST 211/211)" % repair,
                                  "targets": ["R2-" + k]}

# E18/E22 (prosecutor F6): both repaired, but at fc19339 they had no self-test row, so by the record's
# own rule they transiently defeated ed2-IMPL; the rows added in b4eaf11 (E18's with a plant) defeat them.
for k, text in (("E18", "E18 the door was not idempotent: a second pass added a repair the first missed"),
                ("E22", "E22 'orl.py ratify' wrote a claim ratification for a non-claim")):
    args["R2-" + k] = {"by": "redteam-round2",
                       "text": "%s; repaired before entry, but with no self-test row at fc19339 (prosecutor F6) it transiently defeated ed2-IMPL" % text,
                       "targets": ["ed2-IMPL"]}
    args["R2-" + k + "-fixed"] = {"by": "repair",
                                  "text": "the self-test row added in b4eaf11 holds the repair (E18's with a plant); re-verified RESOLVED on 2026-11-09",
                                  "targets": ["R2-" + k]}

# Twin round 3 (S4): documented deviations, merged alongside SPEC 14 at fc19339. The three Part-1
# deviations remain live on the corpus (not compliant with 14); the twin author's SPEC 14 adoption is
# EXPLICITLY UNRESOLVED -- a merged implementation is not author adoption. Documented; attacks nothing.
args["R2-TW3"] = {"by": "twin",
                  "text": "twin round 3: 128 hand-worked probes, 3 settled against the twin in SPEC 14 at fc19339; the three Part-1 deviations remain live on the corpus (twin/probes3/settled.json); the twin author's SPEC 14 adoption stays EXPLICITLY UNRESOLVED -- a merged implementation is not author adoption"}

attacks = []
for k, a in args.items():
    for t in a.pop("targets", []):
        attacks.append([k, t])
with open(os.path.join(HERE, "record.json"), "wb") as fh:
    fh.write(json.dumps({"arguments": args, "attacks": sorted(attacks)}, indent=1, sort_keys=True).encode("utf-8"))
print("record:", len(args), "arguments,", len(attacks), "attacks")

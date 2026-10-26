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

attacks = []
for k, a in args.items():
    for t in a.pop("targets", []):
        attacks.append([k, t])
with open(os.path.join(HERE, "record.json"), "wb") as fh:
    fh.write(json.dumps({"arguments": args, "attacks": sorted(attacks)}, indent=1, sort_keys=True).encode("utf-8"))
print("record:", len(args), "arguments,", len(attacks), "attacks")

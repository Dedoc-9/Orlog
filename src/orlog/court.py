"""The court: standing for claims, by least and greatest fixed points. Never truth.

Two engines, both monotone operators on finite lattices:

  support   G(X) = {c : held(c) and premises(c) <= X}, where held(c) means the claim was evaluated, was true at
            every evaluation, and every backend agreed with the reference byte for byte. lfp(G) is WELL-FOUNDED.
            gfp(G) \\ lfp(G) is CIRCULAR: held claims, all of whose declared support is held, with some support
            chain reaching a cycle (on one, or resting on one). Premises are what the author declared: undeclared
            dependence is invisible to this operator (court finding L10).
            When lfp = gfp, G has exactly one fixed point, and iteration from any assignment reaches it
            (monotonicity and finite height: G^n(empty) <= G^n(X) <= G^n(all)). A closure over an empty lfp, or over
            a run whose backends disagreed, is VACUOUS and is never reported as closed (L10).
  argument  Dung's characteristic function F(S) = {a : every attacker of a is attacked by S}; lfp(F) is the grounded
            extension (IN); OUT is what IN attacks; the rest is UNDECIDED. Used for the court's own record.

Verdicts are computed by one deterministic Kleene schedule. chaotic_lfp exists to test, on fixtures, Cousot's
result (IMAG R.R. 88, 1977: any fair chaotic iteration from below the least fixed point of a monotone system
reaches it); no verdict uses it (L11).

Grounding is bound to the claim: GROUNDED requires a ledger line that ratifies this claim's own seal (its law
statement, claim id and law-seal). A ratified theorem *name* is recorded but grounds nothing by itself, because a
name says nothing about whether this check is the one the theorem characterizes (L4, L8; Urdr L28).
"""
import hashlib
import json
import random

from .sema import law_stmt

COURT_RULES = [
    "R1 integrity: a claim is held only if every backend agreed with the reference byte for byte (otherwise the "
    "integrity column reads CONTESTED and no claim is held).",
    "R2 computation: a claim checked by the program's own computation carries no bits about the author's intent "
    "beyond the text; it can be WELL-FOUNDED, never GROUNDED.",
    "R3 agreement: 'by agreement of' is a label the author writes; the court treats it as computation.",
    "R4 certificate: the reading compares the check's counted operations (summed over its evaluations) with the "
    "certified clause's (summed over every execution of the clause before the claim's latest evaluation), at this "
    "input (CHEAPER at most 1/2, NOT CHEAPER above, CLAUSE NOT RUN at 0). Counted operations are a unit-cost model, not "
    "time; the reading is not Blum's little-oh (Blum 1988; Wasserman & Blum 1997), which compares with the fastest "
    "program for the task. Difference from the computation must be argued from the check's characterization.",
    "R5 grounding: GROUNDED only if a ledger line ratifies this claim's own seal; nothing in the program can write the "
    "ledger, and nothing authenticates who did.",
    "R6 premises: a claim is WELL-FOUNDED only if it is held and its declared premises are (least fixed point); held "
    "claims whose declared support reaches a cycle are CIRCULAR (gfp minus lfp).",
    "R7 absence: a claim never evaluated is UNREACHED: neither supported nor refuted; a claim citing it is not "
    "supported through it.",
]
CHEAP_RATIO = (1, 2)


def reads_state(expr):
    """Whether an expression reads a variable, a list or a rule (iteratively; the tree is bounded anyway)."""
    from .syntax import Node, Var, Item, Length
    stack = [expr]
    while stack:
        n = stack.pop()
        if isinstance(n, (Var, Item, Length)):
            return True
        if isinstance(n, Node):
            stack.extend(getattr(n, k, None) for k in n.fields)
        elif isinstance(n, (list, tuple)):
            stack.extend(n)
    return False


def grounding_admissible(channel):
    """R2 and R3: the program's own computation, and the author's agreement label, can never be grounded."""
    return channel not in ("computation", "agreement")


def lfp(universe, step):
    x = set()
    while True:
        y = step(x)
        if y == x:
            return x
        x = y


def gfp(universe, step):
    x = set(universe)
    while True:
        y = step(x)
        if y == x:
            return x
        x = y


def chaotic_lfp(universe, member, rng):
    """Single-element updates in a random fair order: add c when member(c, X) holds, until none can be added."""
    x = set()
    pending = list(universe)
    while True:
        rng.shuffle(pending)
        changed = False
        for c in pending:
            if c not in x and member(c, x):
                x.add(c)
                changed = True
        if not changed:
            return x


def support_sets(claims, base, premises):
    """claims: ids; base: id -> bool; premises: id -> set of ids."""
    def step(x):
        return {c for c in claims if base[c] and premises[c] <= x}
    lo = lfp(claims, step)
    hi = gfp(claims, step)
    return lo, hi


def find_cycle(start, premises, within):
    """A premise path from start back to start inside `within`, or [] if start only rests on a cycle.
    Deterministic: premises are explored in sorted order."""
    stack = [(start, [start])]
    seen = set()
    while stack:
        node, path = stack.pop()
        for p in sorted(premises[node], reverse=True):
            if p == start:
                return path + [start]
            if p in within and p not in seen:
                seen.add(p)
                stack.append((p, path + [p]))
    return []


def grounded_extension(args, attacks):
    """Dung 1995. attacks: set of (attacker, target). Returns (IN, OUT, UNDECIDED)."""
    attackers = {a: {x for (x, y) in attacks if y == a} for a in args}

    def step(s):
        return {a for a in args if all(any((d, b) in attacks for d in s) for b in attackers[a])}
    inn = lfp(args, step)
    out = {a for a in args if any((x, a) in attacks for x in inn)}
    return inn, out, set(args) - inn - out


# ------------------------------------------------------------------ the ratification ledger
def claim_seal(law_seal, claim_id, claim_law):
    """A claim's own seal: the law it stands in, its claim id, and its own law statement (L17)."""
    return hashlib.sha256(b"orlog-claim-1" + bytes.fromhex(law_seal) + claim_id.to_bytes(4, "big") +
                          claim_law.encode("ascii")).hexdigest()


def read_ledger(path):
    entries = []
    try:
        with open(path, "rb") as fh:
            for i, line in enumerate(fh.read().decode("utf-8").splitlines(), 1):
                if line.strip():
                    e = json.loads(line)
                    e["_line"] = i
                    entries.append(e)
    except FileNotFoundError:
        pass
    return entries


def claim_seals(comp):
    """claim id -> its seal."""
    return {site.stmt.id: claim_seal(comp.law_seal, site.stmt.id, law_stmt(site.stmt)) for site in comp.an.claims}


# ------------------------------------------------------------------ the panel
def panel(comp, witness, ref_receipt_lines, ledger=()):
    """One row per claim (by claim id), side by side; no scalar."""
    an = comp.an
    agreed = witness.get("dissent_kind") == "NONE" and bool(witness.get("backends"))
    recs = {}
    for line in ref_receipt_lines:
        if line.startswith("claim "):
            p = line.split(" ")
            recs[int(p[1])] = {"clause": int(p[2]), "evals": int(p[3]), "trues": int(p[4]), "cost": int(p[5]),
                               "ref": int(p[6]), "ref_cost": int(p[7])}
    status = next((l[7:] for l in ref_receipt_lines if l.startswith("status ")), "")
    seals = claim_seals(comp)
    ratified = {e["claim_seal"]: e for e in ledger if e.get("kind") == "claim"}
    theorems = {e["name"]: e for e in ledger if e.get("kind") == "theorem"}

    rows, base, prem, label = {}, {}, {}, {}
    for site in an.claims:
        s = site.stmt
        k = s.id
        label[k] = "§" + site.label + ("" if sum(1 for x in an.claims if x.id == site.id) == 1 else "#%d" % k)
        r = recs.get(k, {"evals": 0, "trues": 0, "cost": 0, "ref": 0, "ref_cost": 0})
        o = s.oracle
        row = {"claim": k, "clause": label[k], "text": site.text}
        if o[0] == "computation":
            row["channel"] = "computation"
        elif o[0] == "agreement":
            row["channel"] = "agreement of §%s and §%s (a label; read as computation)" % (o[1], o[2])
        elif o[0] == "certificate":
            row["channel"] = "certificate of §%s" % o[1] + (" under the theorem \"%s\"" % o[2] if len(o) > 2 else "")
        elif o[0] == "theorem":
            row["channel"] = "theorem \"%s\"" % o[1]
        else:
            row["channel"] = "the owner"
        row["integrity"] = "AGREED" if agreed else ("CONTESTED" if witness.get("backends") else "REFERENCE-ONLY")
        if r["evals"] == 0:
            row["evaluation"] = "UNREACHED"
        elif r["trues"] < r["evals"]:
            row["evaluation"] = "REFUTED at evaluation %d (%s)" % (r["evals"], status)
        else:
            row["evaluation"] = "true in %d of %d evaluations" % (r["trues"], r["evals"])
        held = r["evals"] > 0 and r["trues"] == r["evals"] and row["integrity"] == "AGREED"
        if not reads_state(s.cond):
            row["condition"] = ("CONSTANT: it reads no variable, so it cannot depend on the run (if it always holds it "
                                "is a tautology airlock: Semiotic core TRIAGE, red team E5)")
        row["claim_seal"] = seals[k]
        if o[0] == "certificate":
            row["cost"] = "check %d ops / certified clause %d ops (counted, unit cost)" % (r["cost"], r["ref_cost"])
            if r["ref_cost"] == 0:
                row["cost_reading"] = "CLAUSE NOT RUN"
            elif r["cost"] * CHEAP_RATIO[1] <= r["ref_cost"] * CHEAP_RATIO[0]:
                row["cost_reading"] = "CHEAPER (at most 1/2 of the clause's counted ops, this input)"
            else:
                row["cost_reading"] = "NOT CHEAPER (above 1/2 of the clause's counted ops, this input)"
        cited = o[1] if o[0] == "theorem" else (o[2] if o[0] == "certificate" and len(o) > 2 else None)
        if cited is not None:
            row["theorem"] = ("ratified by name, ledger line %d (grounds nothing alone)" % theorems[cited]["_line"]
                              if cited in theorems else "cited, not ratified")
        e = ratified.get(seals[k])
        if not grounding_admissible(o[0]):
            row["ratification"] = "not admissible for this channel (R2, R3)"
            ext = False
        else:
            row["ratification"] = ("this claim ratified, ledger line %d" % e["_line"]) if e else "this claim not ratified"
            ext = e is not None
        row["external_bits"] = ("none beyond the text" if o[0] in ("computation", "agreement") else
                                "only through a ledger line ratifying this claim")
        base[k] = held
        prem[k] = {comp.prog.by_label[p].stmt.id for p in s.premises}
        rows[k] = (row, held and ext)
    ids = set(rows)
    sup_lo, sup_hi = support_sets(ids, base, prem)
    gr_lo, _ = support_sets(ids, {k: rows[k][1] for k in ids}, prem)
    circular = sup_hi - sup_lo
    out = []
    for k in sorted(rows):
        row = rows[k][0]
        if k in sup_lo:
            row["support"] = "WELL-FOUNDED"
        elif row["evaluation"] == "UNREACHED":
            row["support"] = "UNREACHED"
        elif k in sup_hi:
            cyc = find_cycle(k, prem, circular)
            row["support"] = "CIRCULAR (in gfp, not in lfp)"
            row["cycle"] = " -> ".join(label[x] for x in cyc) if cyc else "rests on a cycle, not on one"
        else:
            row["support"] = "UNSUPPORTED"
        row["grounding"] = "GROUNDED" if k in gr_lo else "UNGROUNDED"
        out.append(row)
    if not agreed:
        sandwich = "VACUOUS (the backends did not all agree)"
    elif not sup_lo:
        sandwich = "VACUOUS (no claim is well-founded)"
    else:
        sandwich = "CLOSED" if sup_lo == sup_hi else "OPEN"
    summary = {
        "claims": len(out),
        "well_founded": sum(1 for r in out if r["support"] == "WELL-FOUNDED"),
        "circular": sum(1 for r in out if r["support"].startswith("CIRCULAR")),
        "unreached": sum(1 for r in out if r["support"] == "UNREACHED"),
        "unsupported": sum(1 for r in out if r["support"] == "UNSUPPORTED"),
        "grounded": sum(1 for r in out if r["grounding"] == "GROUNDED"),
        "sandwich": sandwich,
        "ledger_entries": len(list(ledger)),
    }
    return {"rules": COURT_RULES, "rows": out, "summary": summary}


def court_artifact(comp, p):
    body = {"data": p, "provenance": {"law_seal": comp.law_seal, "text_seal": comp.text_seal},
            "claim_class": "orlog_court_standing_under_declared_rules_only",
            "validity_scope": {"certifies": ["standing computed by the declared rules from this run's receipts and "
                                             "the ledger as read"],
                               "does_not_certify": ["that any claim is true",
                                                    "that the ledger's ratifications were made by a person (nothing "
                                                    "authenticates a person)",
                                                    "that a cited theorem says what the claim uses it for",
                                                    "dependence the author did not declare as a premise"],
                               "unmeasured": ["time or work: operations are counted at unit cost",
                                              "any input but this one"]},
            "forbidden_interpretations": ["GROUNDED means true", "WELL-FOUNDED means correct",
                                          "CHEAPER means the check is independent of the computation",
                                          "a closed sandwich means the author's premises are complete"]}
    body["chain_hash"] = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=True).encode()).hexdigest()
    return body


def chaotic_agrees(universe, base, premises, trials=200, seed=7):
    """Cousot's chaotic iteration on one instance: every random fair order reaches Kleene's lfp (a test of
    chaotic_lfp on a fixture, not of any verdict)."""
    lo, _ = support_sets(universe, base, premises)
    rng = random.Random(seed)
    for _ in range(trials):
        if chaotic_lfp(universe, lambda c, x: base[c] and premises[c] <= x, rng) != lo:
            return False
    return True

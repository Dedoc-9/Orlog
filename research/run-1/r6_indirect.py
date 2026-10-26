"""R6's correction, measured with version 0 (research for RULINGS.md; a measurement, not a test).

RUN-1 is not built, so no program can declare a port yet. The stand-in for a port is a variable set once from a literal,
`thrust`. The claim reads only `x`, which every tick updates from `thrust`, and it rests on the owner, a channel that
can be grounded. Four things are measured:
1. the claim's condition reads x alone, so a rule that withholds grounding only from a claim whose condition reads a
   port would not touch it;
2. its truth depends on thrust all the same, through state: it holds for every tick at thrust 1 and 2, and is refuted
   at thrust 6;
3. in version 0 the value is in the law, so a ratification binds to it: thrust 1's claim seal is not thrust 2's, and
   thrust 1's ratification grounds nothing in thrust 2's law;
4. with its own seal ratified, the claim reads GROUNDED. That is legitimate in version 0, where the person ratified a
   law that holds the value.

What follows for RUN-1 is argued, not measured. With thrust a port (R1 b), the law and the claim's seal stay the same
whatever the log says, so one ratification would carry from one log to every other. The narrow rule would then let this
claim read GROUNDED over a log nobody vouched for. The coarse rule withholds grounding from every claim of a law that
declares a port: sound, since it never reads a false GROUNDED, and not complete, since it also withholds grounding from
a claim that depends on no port.

  PYTHONHASHSEED=0 python -B research/run-1/r6_indirect.py
"""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import Arbiter, parse_receipt  # noqa: E402
from orlog.syntax import Node, Var  # noqa: E402

PORT = "thrust"          # the stand-in: in RUN-1 this would be `Let thrust be given as an integer.`
FIXTURE = "FIXTURE written by research/run-1/r6_indirect.py; not a person's act"


def law(thrust, claim="x is at most 100"):
    lines = ["§1 Let thrust be %d." % thrust,
             "§2 Let x be 0.",
             "§3 For each tick from 1 to 20, do the following.",
             "§3.1 Increase x by thrust.",
             "§3.2 We claim that %s, by the owner." % claim]
    return ("\n".join(lines) + "\n").encode("utf-8")


def reads(node, out):
    """The variable names an expression reads directly."""
    if isinstance(node, Var):
        out.add(node.name)
    elif isinstance(node, Node):
        for k in node.fields:
            reads(getattr(node, k, None), out)
    elif isinstance(node, (list, tuple)):
        for x in node:
            reads(x, out)
    return out


def run(arb, thrust, ledger_seal=None, claim="x is at most 100"):
    comp, w, ref = arb.arbitrate(law(thrust, claim), "r6-thrust-%d" % thrust)
    site = comp.an.claims[0]
    seal = COURT.claim_seals(comp)[site.stmt.id]
    ledger = [] if ledger_seal is None else [{"kind": "claim", "claim_seal": ledger_seal, "note": FIXTURE, "_line": 1}]
    row = COURT.panel(comp, w, parse_receipt(ref.receipt()), ledger)["rows"][0]
    return {"thrust": thrust, "law": comp.law_seal, "seal": seal, "status": w["reference"]["status"],
            "agreed": w["dissent_kind"], "evaluation": row["evaluation"], "grounding": row["grounding"],
            "reads": sorted(reads(site.stmt.cond, set()))}


def main():
    wd = os.path.join(ROOT, "build", "r6-indirect")
    os.makedirs(wd, exist_ok=True)
    arb = Arbiter(wd, backends=("python",))
    print("== R6, measured with version 0: `%s`, set once from a literal, stands in for a port" % PORT)
    plain = {t: run(arb, t) for t in (1, 2, 6)}
    for t, r in plain.items():
        print("  thrust %d: law %s, claim seal %s, run %s (%s), evaluation %s" % (
            t, r["law"][:12], r["seal"][:12], r["status"], r["agreed"], r["evaluation"]))
    r2 = plain[2]
    print("1. the claim's condition reads: %s; it does not read `%s`" % (", ".join(r2["reads"]), PORT))
    print("2. its truth depends on `%s` through state: thrust 1 %s; thrust 2 %s; thrust 6 %s" % (
        PORT, plain[1]["evaluation"], plain[2]["evaluation"], plain[6]["evaluation"]))
    carried = run(arb, 2, ledger_seal=plain[1]["seal"])
    print("3. version 0 binds a ratification to the value: thrust 1's and thrust 2's claim seals differ: %s; thrust 1's "
          "ratification applied to thrust 2's law: grounding %s" % (plain[1]["seal"] != plain[2]["seal"],
                                                                    carried["grounding"]))
    own = run(arb, 2, ledger_seal=plain[2]["seal"])
    print("4. with its own seal ratified, thrust 2's claim reads %s (version 0: the value is in the law the person "
          "ratified)" % own["grounding"])
    narrow = PORT in own["reads"]
    coarse = True        # the law declares the port
    print("the two wordings of R6, with `%s` as the port:" % PORT)
    print("  narrow, 'a claim whose condition reads a port': withholds grounding: %s (the claim would read %s over "
          "any log)" % (narrow, own["grounding"]))
    print("  coarse, 'a law that declares any port': withholds grounding: %s" % coarse)
    # the control: the narrow check itself works, so its miss above is the indirect path and nothing else
    direct = run(arb, 2, claim="x plus thrust is at most 102")
    direct_withheld = PORT in direct["reads"]
    print("control: a claim that reads `%s` directly (x plus thrust is at most 102) reads %s; the narrow rule "
          "withholds grounding: %s" % (PORT, ", ".join(direct["reads"]), direct_withheld))
    ok = (r2["reads"] == ["x"] and plain[1]["status"] == "COMPLETED" and plain[2]["status"] == "COMPLETED"
          and plain[6]["status"].startswith("REFUSED CLAIM-REFUTED") and plain[1]["seal"] != plain[2]["seal"]
          and carried["grounding"] == "UNGROUNDED" and own["grounding"] == "GROUNDED" and not narrow and coarse
          and direct_withheld)
    print("R6 INDIRECT DEPENDENCE %s: the narrow rule misses dependence through state; the coarse rule does not "
          "(sound, not complete)" % ("SHOWN" if ok else "NOT SHOWN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

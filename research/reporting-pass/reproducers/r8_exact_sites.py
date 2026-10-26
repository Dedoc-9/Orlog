"""R8's exact branch, measured where a claim can stand: does a refusal inside a claim's own condition always name the
claim's clause, and does the court then read 'exact' with the right evaluation number?

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/reporting-pass/reproducers/r8_exact_sites.py

Each text evaluates its claim 16 times true, then refuses inside the claim's condition at the 17th evaluation, with
the claim standing: as its clause's statement at the top of a loop body; in a procedure performed in a loop; in a block
If's sub-clause; in an Otherwise block's sub-clause; in a While body; through a rule whose proviso refuses; through a
rule whose value refuses. Expected for each: the reference's status names the claim's clause, refusal_in_claim reads
'exact', and the row reads "REFUSED at evaluation 17". A text where any of these fails is printed as a MISS.
"""
import sys

import _common as C

C.require_env()
from orlog import court as COURT  # noqa: E402
from orlog.arbiter import parse_receipt  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402

HEAD = "§1 Let xs be a list of 16 copies of 1.\n"
CASES = {
    "the clause's statement, in a For body":
        HEAD + "§2 For each i from 1 to 17, do the following.\n§2.1 We claim that item i of xs equals 1, by the owner.\n",
    "in a procedure performed in a loop":
        HEAD + "§2 Let k be 0.\n§3 To probe, do the following.\n§3.1 We claim that item k of xs equals 1, by the owner.\n"
        "§4 For each i from 1 to 17, do the following.\n§4.1 Set k to i.\n§4.2 Probe.\n",
    "in a block If's sub-clause":
        HEAD + "§2 For each i from 1 to 17, do the following.\n§2.1 If true, do the following.\n"
        "§2.1.1 We claim that item i of xs equals 1, by the owner.\n",
    "in an Otherwise block's sub-clause":
        HEAD + "§2 For each i from 1 to 17, do the following.\n§2.1 If false, say 0.\n"
        "§2.2 Otherwise, do the following.\n§2.2.1 We claim that item i of xs equals 1, by the owner.\n",
    "in a While body":
        HEAD + "§2 Let i be 0.\n§3 While i is less than 17, at most 20 times, do the following.\n§3.1 Increase i by 1.\n"
        "§3.2 We claim that item i of xs equals 1, by the owner.\n",
    "through a rule whose proviso refuses":
        HEAD + "§2 Let k be 0.\n§3 Define one as 1, provided that item k of xs equals 1.\n"
        "§4 For each i from 1 to 17, do the following.\n§4.1 Set k to i.\n§4.2 We claim that one equals 1, by the owner.\n",
    "through a rule whose value refuses":
        HEAD + "§2 Let k be 0.\n§3 Define v as item k of xs.\n"
        "§4 For each i from 1 to 17, do the following.\n§4.1 Set k to i.\n§4.2 We claim that v equals 1, by the owner.\n",
}


def main():
    misses = 0
    for name, text in CASES.items():
        comp = compile_bytes(text.encode("utf-8"))
        if not comp.ok:
            print("== %s: REFUSED %s at line %s (%s) -- the text, not R8" % (name, comp.error.code, comp.error.line,
                                                                          comp.error.msg))
            misses += 1
            continue
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
        site = comp.an.claims[0]
        parts = it.status.split(" ")
        hit = COURT.refusal_in_claim(site, (parts[1], int(parts[2]))) if parts[0] == "REFUSED" else None
        p = COURT.panel(comp, {"dissent_kind": "NONE", "backends": {"reference": {}}}, parse_receipt(it.receipt()), [])
        ev = p["rows"][0]["evaluation"]
        ok = parts[0] == "REFUSED" and int(parts[2]) == site.id and hit == "exact" and \
            ev.startswith("REFUSED at evaluation 17 ")
        misses += not ok
        print("== %s: status %s; claim clause %d; R8 reads %r; %s" % (name, it.status, site.id, hit,
                                                                     "held as expected" if ok else "MISS"))
        print("   " + ev)
    print("R8 EXACT SITES: %d of %d as expected" % (len(CASES) - misses, len(CASES)))
    return 0 if not misses else 1


if __name__ == "__main__":
    sys.exit(main())

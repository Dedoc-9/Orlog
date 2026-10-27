"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

G7: the host's drop and the cause INPUT-MISSING. A player who sent nothing, and a player whose valid input the host
dropped, end with one input log and one receipt core, both naming the player's input as missing.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/s_drop.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
import cut0_session as S                                                  # noqa: E402

AB = ["a", "b"]
silent = [("arrive", "b", S.B("1")), ("assign", 0, 1), ("close",)]
dropped = [("arrive", "a", S.B("1")), ("arrive", "b", S.B("1")), ("drop", 0), ("assign", 1, 1), ("close",)]
for name, h in (("a sent nothing", silent), ("a's valid 1 dropped by the host", dropped)):
    s = S.settle(h, AB)
    log = S.input_log(s)
    r = S.execute(log, AB)
    print("%-34s legal; dispositions %s; status %s; rows failed %s" % (
        name, s.dispositions(), r["status"], S.check_run(h, AB) or "none"))
ls, ld = (S.input_log(S.settle(h, AB)) for h in (silent, dropped))
cs, cd = (S.execute(l, AB)["core"] for l in (ls, ld))
rs, rd = (S.session_record(h, AB) for h in (silent, dropped))
print("input logs %s; receipt cores %s; session records %s" % (
    "EQUAL" if ls == ld else "differ", "EQUAL" if cs == cd else "differ", "EQUAL" if rs == rd else "differ"))

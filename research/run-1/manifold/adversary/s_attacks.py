"""ADVERSARY'S RESEARCH CODE (research/run-1/manifold/ADVERSARY.md). Nothing in the program reads it.

Attacks on research/run-1/probes/cut0_session.py, read through its own functions (Session, check_run, parse_log,
serialize, door, history_bytes, session_record), never a copy of them.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/adversary/s_attacks.py

1. Wider domains: every legal history of two ports, and of one port deeper than 6, through check_run's rows.
2. No each-tick port: a legal history whose own projection the strict parser refuses.
3. The door's grammar and Python's `$`.
4. Multi-byte edits of every distinct log: line swaps, deletions, duplications, field substitutions (the other
   cause, the i64 bounds): each accepted edit is checked canonical, and checked against the image of A2's projection.
5. Which of check_run's rows any of the probe's nine plants can turn red on the exhaustive domain.
6. The session record against pairs of histories: injectivity measured; what the history does not hold.
7. A tick closed after the run has refused.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
import cut0_session as S                                                  # noqa: E402

B = S.B


def exhaustive(ports, depth, values):
    n, failed, logs, hb = 0, {}, set(), {}
    stack = [[]]
    while stack:
        h = stack.pop()
        n += 1
        for f in S.check_run(h, ports):
            failed[f] = failed.get(f, 0) + 1
        s = S.settle(h, ports)
        logs.add(S.input_log(s))
        hb.setdefault(S.history_bytes(h), set()).add(tuple(h))
        if len(h) < depth:
            for m in s.legal_moves(values):
                stack.append(h + [m])
    collisions = sum(1 for v in hb.values() if len(v) > 1)
    return n, failed, logs, collisions


def in_a2_image(parsed):
    """A log is the projection of some legal A2 history iff it parses and its end is open, closed, or not-run with
    INPUT-MISSING: every int64 is some door output (raw / 2^32 has a finite decimal), any record sequence is reached by
    assigning and closing, and A2 never puts a refused arrival in a slot (DECLARED from Session.step, lines 101-103 and
    116-131)."""
    records, end = parsed
    return end is None or end == ("closed",) or end[2] == "INPUT-MISSING"


def edits(log):
    lines = log.decode("ascii").split("\n")[:-1]
    out = []
    for i in range(3, len(lines)):
        out.append(lines[:i] + lines[i + 1:])                            # delete a line
        out.append(lines[:i + 1] + [lines[i]] + lines[i + 1:])          # duplicate a line
        for j in range(i + 1, len(lines)):
            sw = list(lines)
            sw[i], sw[j] = sw[j], sw[i]
            out.append(sw)                                               # swap two lines
        f = lines[i].split(" ")
        if f[0] == "t":
            for v in ("8000000000000000", "7fffffffffffffff", "ffffffffffffffff", "0000000000000000"):
                out.append(lines[:i] + [" ".join(f[:2] + [v] * (len(f) - 2))] + lines[i + 1:])
        if f[0] == "end" and len(f) == 6:
            for c in ("INPUT-REFUSED", "INPUT-MISSING"):
                out.append(lines[:i] + [" ".join(f[:4] + [c] + f[5:])] + lines[i + 1:])
        if f[0] == "end" and f[2:] == ["closed"]:
            n = int(f[1])
            out.append(lines[:i] + ["end %d not-run %d INPUT-REFUSED a" % (n, n + 1)] + lines[i + 1:])
            out.append(lines[:i] + ["end %d not-run %d INPUT-MISSING a" % (n, n + 1)] + lines[i + 1:])
    if lines[3:] and not lines[-1].startswith("end"):
        n = sum(1 for l in lines if l.startswith("t "))
        out.append(lines + ["end %d not-run %d INPUT-REFUSED a" % (n, n + 1)])
    return [("\n".join(e) + "\n").encode("ascii") for e in out]


def no_value_invented(history, ports):
    """A row this adversary proposes for CONTRACT-DRAFT 1.5 ("no value is ever invented, held over or defaulted"):
    every value of tick record t is the door's value of the accepted arrival the history assigned to (t, port)."""
    s = S.settle(history, ports)
    arrivals = []
    slot = {}
    for e in history:
        if e[0] == "arrive":
            arrivals.append(e)
        elif e[0] == "assign":
            slot[(e[2], arrivals[e[1]][1])] = arrivals[e[1]][2]
    for t, vals in enumerate(s.records, 1):
        for p, v in zip(ports, vals):
            raw = slot.get((t, p))
            if raw is None or S.door(raw)[0] != "ok" or S.door(raw)[1] != v:
                return False
    return True


def exhaustive_row(ports, depth, values, row):
    n = bad = 0
    stack = [[]]
    while stack:
        h = stack.pop()
        n += 1
        bad += not row(h, ports)
        if len(h) < depth:
            for m in S.settle(h, ports).legal_moves(values):
                stack.append(h + [m])
    return n, bad


def main():
    print("== 1. wider domains (policy A2)")
    for ports, depth, vals in ((["a", "b"], 5, ["1", "1.1", "13"]), (["a", "b"], 6, ["1", "13"]),
                               (["a"], 8, ["1", "13"]), (["a", "b", "c"], 5, ["1", "13"])):
        n, failed, logs, coll = exhaustive(ports, depth, [B(v) for v in vals])
        print("   ports %s, depth %d, arrivals among %s: histories %d, distinct logs %d, rows failed: %s; "
              "history_bytes collisions %d" % (",".join(ports), depth, ", ".join(vals), n, len(logs),
                                               ", ".join("%s %d" % kv for kv in sorted(failed.items())) or "none",
                                               coll))
    print("== 2. a law with no each-tick port")
    h = [("close",)]
    s = S.settle(h, [])
    log = S.input_log(s)
    print("   history [close]: legal; its projection %r" % log.split(b"\n")[3])
    print("   check_run fails: %s" % S.check_run(h, []))
    try:
        S.execute(S.serialize([], [[]], ("closed",)), [])
    except S.Malformed as e:
        print("   execute on the projection: Malformed %s" % e)
    except Exception as e:
        print("   execute on the projection: %r" % e)
    print("== 3. the door: FIXED is matched with `$`, which also matches before a final LF")
    for raw in (b"1", b"1\n", b"-0", b"007", b"1.50", b"1\n\n", b" 1"):
        print("   door(%r) = %s" % (raw, S.door(raw)))
    print("== 4. multi-byte edits of every distinct log of one port, depth 6 (the probe's domain)")
    n, failed, logs, _ = exhaustive(["a"], 6, [B(v) for v in ("1", "1.1", "4", "13")])
    tried = accepted = noncanon = outside = 0
    example = None
    for log in sorted(logs):
        for v in edits(log):
            if v == log:
                continue
            tried += 1
            try:
                parsed = S.parse_log(v, ["a"])
            except S.Malformed:
                continue
            accepted += 1
            if S.serialize(["a"], *parsed) != v:
                noncanon += 1
            if not in_a2_image(parsed):
                outside += 1
                if example is None or len(v) < len(example):
                    example = v
    print("   %d logs, %d edits tried: accepted %d (non-canonical %d); accepted outside A2's image %d" % (
        len(logs), tried, accepted, noncanon, outside))
    if example:
        print("   the shortest outside A2's image:\n      " + "\n      ".join(example.decode().split("\n")[:-1]))
        print("   execute reads it: %s" % S.execute(example, ["a"])["status"])
    print("== 5. which rows any of the probe's nine plants turns red on the probe's own domain (one port, depth 6)")
    vals = [B(v) for v in ("1", "1.1", "4", "13")]
    rows = ["projection-is-a-function", "log-round-trips", "projection-parses", "door-replays",
            "no-assignment-disappears", "one-disposition-each", "execution-is-a-function", "statuses-partition",
            "T1-is-the-prefix", "T-differences-are-the-lines", "ops-minus-last-T-is-tick-ops",
            "no-T-ops-is-the-prefix", "budget-tick-counts-N+1", "executed-is-counted-less-the-refused",
            "session-binds"]
    red = {r: [] for r in rows}
    for plant in ("assign-refused", "hold-previous", "no-cause", "overwrite", "budget-uncounted", "end-anytime",
                  "lenient-hex", "after-end", "record-without-history"):
        S.PLANT = plant
        try:
            _, failed, _, _ = exhaustive(["a"], 6, vals)
        except S.Malformed:
            failed = {"(the plant's projection refused: Malformed)": 1}
        finally:
            S.PLANT = None
        for r in failed:
            red.setdefault(r, []).append(plant)
    for r in rows:
        print("   %-38s %s" % (r, ", ".join(red[r]) if red[r] else "NEVER RED"))
    for r in red:
        if r not in rows:
            print("   %-38s %s" % (r, ", ".join(red[r])))
    print("== 5b. the proposed row no-value-invented on the same domain, as it stands and under the plant hold-previous")
    for plant in (None, "hold-previous"):
        S.PLANT = plant
        try:
            n, bad = exhaustive_row(["a"], 6, vals, no_value_invented)
        finally:
            S.PLANT = None
        print("   plant %-14s histories %d, failing the row %d" % (plant or "none", n, bad))
    print("== 6. the session record and what the history holds")
    h1 = [("arrive", "a", B("1")), ("assign", 0, 1), ("close",), ("end",)]
    print("   CONTRACT-DRAFT 1.1: an arrival carries its sequence number, the port's name, the source's label and the "
          "bytes.\n   The model's arrive event is %r: no source. Two sessions, alice's `1` and mallory's `1`, have "
          "the one history\n   and the one record: %s" % (
              h1[0], hashlib.sha256(S.session_record(h1, ["a"])).hexdigest()[:16]))
    print("== 7. a tick closed after the run refused")
    h = [("arrive", "a", B("13")), ("assign", 0, 1), ("close",), ("arrive", "a", B("1")), ("assign", 1, 2),
         ("close",), ("end",)]
    try:
        s = S.settle(h, ["a"])
    except S.Illegal as e:
        # Added 2026-10-26, the script's one change since the adversary's run: the probe's G6 repair refuses this
        # history at the first event after tick 1's refusal (only the end is legal then), so the attack is reported
        # as refused instead of raising.
        print("   history: tick 1 carries 13 (refuses), then tick 2 is assigned and closed, then end")
        print("   refused by the session model: %s (the G6 repair: after the run refused, only the end is legal)" % e)
        return
    r = S.execute(S.input_log(s), ["a"])
    print("   history: tick 1 carries 13 (refuses), then tick 2 is assigned and closed, then end")
    print("   legal; records (\"the ticks that will run\") %d; status %s; ticks run %d; rows failed %s" % (
        len(s.records), r["status"], r["ticks"], S.check_run(h, ["a"]) or "none"))


if __name__ == "__main__":
    main()

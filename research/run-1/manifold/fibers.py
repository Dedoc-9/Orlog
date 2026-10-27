"""RESEARCH SCRIPT (the manifold debate's proponent, 2026-10-26). Nothing in the program reads it; it edits nothing.

The session side of CUT-0 (research/run-1/probes/cut0_session.py), read as a configuration complex: its vertices the
session states, its edges the events, its squares the pairs of events that commute.

  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/manifold/fibers.py 2> research/run-1/manifold/fibers-timing.txt

Every transition, projection, receipt core and session record is cut0_session's own function, imported. Measured:
1. the fibers of history -> input log, -> receipt core, -> session record, and what differs inside each;
2. three quotients of the histories: by end state (the complex's vertices), by Mazurkiewicz trace (paths modulo the
   squares), and by what the contract can observe (arrivals, door results, dispositions, input log);
3. the strict parser's language against the projection's image: which logs are no history's projection;
4. the state graph as a smaller complete representation: every row of cut0_session's check_run except the session
   binding is a function of the end state (checked under every plant), so it is checked once per state, deeper.
Timings go to stderr, never into the record (a timing is not a byte-identical output).
"""
import hashlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "research", "run-1", "probes"))
import cut0_session as S                                          # noqa: E402

B = lambda s: s.encode()                                          # noqa: E731
D1 = (["a"], [B("1"), B("1.1"), B("4"), B("13")], 6)              # the probe's own domain
D2 = (["a", "b"], [B("1"), B("1.1")], 6)                          # two ports, an accepted and a refused value


def tlog(*a):
    sys.stderr.write(" ".join(str(x) for x in a) + "\n")


# ------------------------------------------------------------------ states, histories, labels
def key(s):
    return (tuple(s.arrivals), tuple(sorted(s.disposed.items())), tuple(sorted(s.slots.items())), s.tick,
            tuple(tuple(r) for r in s.records), s.outcome, tuple(s.sources), s.refused)


def from_key(k, ports):
    s = S.Session(ports)
    s.arrivals, s.disposed, s.slots = list(k[0]), dict(k[1]), dict(k[2])
    s.tick, s.records, s.outcome = k[3], [list(r) for r in k[4]], k[5]
    s.sources, s.refused = list(k[6]), k[7]
    return s


def histories(ports, values, depth):
    """Every legal history up to depth events, in cut0_session.exhaustive's order, with its end state."""
    stack = [([], S.Session(ports))]
    while stack:
        h, s = stack.pop()
        yield h, s
        if len(h) < depth:
            for m in s.legal_moves(values):
                s2 = from_key(key(s), ports)
                try:
                    s2.step(m)
                except S.Illegal:
                    continue
                stack.append((h + [m], s2))


def labels(h, ports):
    """Each event's letter: arrivals carry their number, port and bytes; an assignment its port; a close whether it
    ran its tick, ran one whose run refused (after which only the end may follow), or ended the session."""
    s = S.Session(ports)
    out = []
    for e in h:
        if e[0] == "arrive":
            out.append(("arrive", len(s.arrivals), e[1], e[-1]))
        elif e[0] == "assign":
            out.append(("assign", e[1], s.arrivals[e[1]][0]))
        elif e[0] == "drop":
            out.append(("drop", e[1]))
        elif e[0] == "close":
            ticks = len(s.records)
            s.step(e)
            out.append(("close-notrun",) if len(s.records) == ticks else
                       ("close-refused",) if s.refused is not None else ("close-run",))
            continue
        else:
            out.append(("end",))
        s.step(e)
    return out


def independent(a, b):
    """The squares of the complex: a static, symmetric, irreflexive relation on letters (checked as a diamond)."""
    ka, kb = a[0], b[0]
    if ka > kb:
        a, b, ka, kb = b, a, kb, ka
    if ka == kb == "assign":
        return a[1] != b[1] and a[2] != b[2]
    if ka == kb == "drop":
        return a[1] != b[1]
    if (ka, kb) == ("assign", "drop"):
        return a[1] != b[1]
    if (ka, kb) in (("arrive", "assign"), ("arrive", "drop")):
        return a[1] != b[1]
    if (ka, kb) in (("arrive", "close-run"), ("close-run", "drop")):
        return True
    return False


def foata(lab):
    """The Foata normal form of the trace of a word: its levels, each a sorted tuple of letters."""
    level = []
    for j, x in enumerate(lab):
        lv = 0
        for i in range(j):
            if not independent(lab[i], x):
                lv = max(lv, level[i] + 1)
        level.append(lv)
    out = [[] for _ in range(max(level) + 1)] if lab else []
    for x, lv in zip(lab, level):
        out[lv].append(x)
    return tuple(tuple(sorted(l, key=repr)) for l in out)


def situation(h, s):
    """Why a NOT-RUN tick's port had no value: an accepted arrival the host withheld, one it dropped, only refused
    arrivals since the last tick ran, or none. None if the session did not end NOT-RUN."""
    if not (s.outcome and s.outcome[0] == "not-run"):
        return None
    port = s.outcome[3]
    arrivals_at_last_run, n_arr, ticks = 0, 0, 0
    t = S.Session(s.ports)
    for e in h:
        t.step(e)
        if e[0] == "close" and len(t.records) > ticks:
            ticks = len(t.records)
            arrivals_at_last_run = len(t.arrivals)
    mine = [(i, r) for i, (p, _, r) in enumerate(s.arrivals) if p == port]
    if any(r[0] == "ok" and i not in s.disposed for i, r in mine):
        return "withheld"
    if any(s.disposed.get(i) == ("dropped",) for i, r in mine):
        return "dropped"
    if any(r[0] != "ok" and i >= arrivals_at_last_run for i, r in mine):
        return "refused"
    return "none"


def outcome_facts(log, ports):
    r = S.execute(log, ports)
    return (r["status"], r["ticks"], r["ops"], r["executed"], r["tick_ops"], tuple(r["T"]), tuple(r["lines"]))


# ------------------------------------------------------------------ 1-2: fibers and quotients
def fibers(name, dom):
    ports, values, depth = dom
    t0 = time.perf_counter()
    n = 0
    by_log, by_core, by_rec, by_state, by_trace, by_obs = {}, {}, {}, {}, {}, {}
    swaps, sit_count = {}, {}
    diamond_checked = diamond_bad = 0
    for h, s in histories(ports, values, depth):
        n += 1
        log = S.input_log(s)
        core = S.execute(log, ports)["core"]
        rec = S.session_record(h, ports)
        disp = tuple(s.dispositions())
        sit = situation(h, s)
        facts = outcome_facts(log, ports)
        lab = labels(h, ports)
        tr = foata(lab)
        obs = (tuple((p, raw, r[0]) for p, raw, r in s.arrivals), disp, log)
        k = key(s)
        f = by_log.setdefault(log, {"n": 0, "disp": set(), "sit": set(), "rec": set(), "core": set(), "facts": set(),
                                    "refusals": set()})
        f["n"] += 1
        f["disp"].add(disp)
        f["sit"].add(sit)
        if sit is not None:
            sit_count[sit] = sit_count.get(sit, 0) + 1
        f["rec"].add(rec)
        f["core"].add(core)
        f["facts"].add(facts)
        f["refusals"].add(sum(1 for _, _, r in s.arrivals if r[0] != "ok"))
        g = by_core.setdefault(core, {"n": 0, "facts": set(), "log": set()})
        g["n"] += 1
        g["facts"].add(facts)
        g["log"].add(log)
        by_rec.setdefault(rec, set()).add(S.history_bytes(h))
        by_state.setdefault(k, {"n": 0, "trace": set(), "obs": set(), "log": set()})
        by_state[k]["n"] += 1
        by_state[k]["trace"].add(tr)
        by_state[k]["obs"].add(obs)
        by_state[k]["log"].add(log)
        tcl = by_trace.setdefault(tr, {"n": 0, "log": set(), "obs": set(), "state": set(), "rec": set(), "h": []})
        tcl["n"] += 1
        tcl["log"].add(log)
        tcl["obs"].add(obs)
        tcl["state"].add(k)
        tcl["rec"].add(rec)
        if len(tcl["h"]) < 2:
            tcl["h"].append(h)
        by_obs.setdefault(obs, set()).add(tr)
        for j in range(len(h) - 1):                     # every square: the swapped word is legal, same end state
            if independent(lab[j], lab[j + 1]):
                diamond_checked += 1
                h2 = h[:j] + [h[j + 1], h[j]] + h[j + 2:]
                try:
                    s2 = S.settle(h2, ports)
                    ok = key(s2) == k and labels(h2, ports) == lab[:j] + [lab[j + 1], lab[j]] + lab[j + 2:]
                except S.Illegal:
                    ok = False
                diamond_bad += not ok
                kind = tuple(sorted((lab[j][0], lab[j + 1][0])))
                swaps[kind] = swaps.get(kind, 0) + 1
    tlog("fibers", name, "histories", n, "seconds %.1f" % (time.perf_counter() - t0))
    print("== %s: every legal history of %d port(s) %s up to %d events, arrivals among %s" % (
        name, len(ports), ",".join(ports), depth, ", ".join(v.decode() for v in values)))
    print("  histories %d; distinct input logs %d, receipt cores %d, session records %d" % (
        n, len(by_log), len(by_core), len(by_rec)))
    sizes = sorted((f["n"] for f in by_log.values()), reverse=True)
    print("  log fibers: largest %s; singletons %d" % (", ".join(map(str, sizes[:6])), sizes.count(1)))
    print("  RECORDS THAT MUST TELL THINGS APART:")
    print("    core fibers holding two execution outcomes (status, ticks, ops, executed, tick-ops, T, tick lines): %d"
          % sum(len(g["facts"]) > 1 for g in by_core.values()))
    print("    core fibers holding two input logs (the core binds the log's sha256): %d" % sum(
        len(g["log"]) > 1 for g in by_core.values()))
    print("    session-record fibers holding two histories: %d" % sum(len(v) > 1 for v in by_rec.values()))
    print("  WHAT THE INPUT LOG FORGETS (inside a log fiber, by design: CUT-0 section 3 reads these from the history):")
    print("    log fibers with two disposition vectors %d; with two refusal counts %d" % (
        sum(len(f["disp"]) > 1 for f in by_log.values()), sum(len(f["refusals"]) > 1 for f in by_log.values())))
    nr = {lg: f for lg, f in by_log.items() if None not in f["sit"]}
    print("    NOT-RUN logs %d, their histories %d by why the port had no value: %s" % (
        len(nr), sum(f["n"] for f in nr.values()), ", ".join("%s %d" % kv for kv in sorted(sit_count.items()))))
    print("    NOT-RUN logs whose fiber mixes two of those reasons: %d of %d (each told apart by the session record:"
          " %s)" % (sum(len(f["sit"]) > 1 for f in nr.values()), len(nr),
                    "yes" if all(len(f["rec"]) == f["n"] for f in nr.values()) else "NO"))
    causes = sorted({lg.split(b"\n")[-2].split(b" ")[4].decode() for lg in nr})
    print("    distinct causes written in those logs' end records: %s" % ", ".join(causes))
    print("  QUOTIENTS (vertices, paths modulo squares, what the contract observes):")
    print("    end states %d; Mazurkiewicz traces %d; contract observations %d; input logs %d; histories %d" % (
        len(by_state), len(by_trace), len(by_obs), len(by_log), n))
    print("    squares checked as diamonds (both orders legal, one end state, the letters kept) %d, failed %d" % (
        diamond_checked, diamond_bad))
    print("    squares by the kinds of their two events: %s" % ", ".join(
        "%s/%s %d" % (k[0], k[1], v) for k, v in sorted(swaps.items())))
    print("    traces whose histories reach two end states %d, two input logs %d, two observations %d" % (
        sum(len(t["state"]) > 1 for t in by_trace.values()), sum(len(t["log"]) > 1 for t in by_trace.values()),
        sum(len(t["obs"]) > 1 for t in by_trace.values())))
    print("    end states reached by two traces %d; observations made by two traces %d" % (
        sum(len(v["trace"]) > 1 for v in by_state.values()), sum(len(v) > 1 for v in by_obs.values())))
    multi = [t for t in by_trace.values() if t["n"] > 1]
    print("    traces of two or more histories %d (largest %d), each history with a session record of its own: %s" % (
        len(multi), max([t["n"] for t in multi] or [0]),
        "yes" if all(len(t["rec"]) == t["n"] for t in by_trace.values()) else "NO"))
    ex = min((t for t in multi), key=lambda t: (len(t["h"][0]), repr(t["h"])), default=None)
    if ex is not None:
        print("    the smallest such pair, one trace and two session records:")
        for h in ex["h"]:
            print("      %s" % " ".join("%s(%s)" % (e[0], ",".join(x.decode() if isinstance(x, bytes) else str(x)
                                                                     for x in e[1:])) for e in h))
    return {"n": n, "states": by_state, "logs": set(by_log)}


# ------------------------------------------------------------------ 3: the parser's language and the image
def parser_language(ports, accepted_raw, max_ticks):
    """Every log the strict parser (under the policy in force) accepts with at most max_ticks records over the given
    raw values: each end variant (open, closed, not-run of the next tick for each cause and port), kept only if
    parse_log accepts it, and then checked canonical."""
    import itertools
    out = []
    for n in range(max_ticks + 1):
        for recs in itertools.product(itertools.product(accepted_raw, repeat=len(ports)), repeat=n):
            recs = [list(r) for r in recs]
            ends = [None, ("closed",)] + [("not-run", n + 1, c, p) for c in S.CAUSES for p in ports]
            for e in ends:
                b = S.serialize(ports, recs, e)
                try:
                    parsed = S.parse_log(b, ports)
                except S.Malformed:
                    continue
                assert S.serialize(ports, *parsed) == b
                out.append(b)
    return out


def why_unreachable(b, ports):
    """A parser-accepted log that no history projects: past a refusing tick, an A1-only cause, or other."""
    records, end = S.parse_log(b, ports)
    r = S.execute(b, ports)
    if r["status"].startswith("REFUSED") and (r["ticks"] < len(records) or (end and end[0] == "not-run")):
        return "a record or a not-run end past a refusing tick"
    if end and end[0] == "not-run" and end[2] == "INPUT-REFUSED":
        return "INPUT-REFUSED"
    return "other"


# ------------------------------------------------------------------ 4: the log-relevant abstraction
LOG_ROWS = frozenset(["projection-is-a-function", "projection-parses", "log-round-trips", "execution-is-a-function",
                      "statuses-partition", "T1-is-the-prefix", "T-differences-are-the-lines",
                      "ops-minus-last-T-is-tick-ops", "no-T-ops-is-the-prefix", "budget-tick-counts-N+1",
                      "executed-is-counted-less-the-refused"])


def moves(s, values):
    """cut0_session's legal moves; under policy A1 also the assignment of a refused arrival (A1 assigns before the
    door judges; legal_moves, written for A2, does not list it)."""
    ms = s.legal_moves(values)
    if S.POLICY == "A1" and s.outcome is None and s.refused is None:
        ms += [("assign", i, s.tick) for i, (p, _, r) in enumerate(s.arrivals)
               if r[0] != "ok" and i not in s.disposed and p not in s.slots]
    return ms


def akey(s):
    """What the input log's future depends on: the open tick, the records, the outcome, each filled slot's port and
    door result, and the multiset of assignable arrivals' (port, door result). Arrival numbers, refused arrivals
    (under A2), disposed arrivals and the order of every event are forgotten."""
    assignable = sorted((p, r) for i, (p, _, r) in enumerate(s.arrivals)
                        if i not in s.disposed and (r[0] == "ok" or S.POLICY == "A1"))
    slots = tuple(sorted((p, s.arrivals[i][2]) for p, i in s.slots.items()))
    return (s.tick, tuple(tuple(r) for r in s.records), s.outcome, slots, tuple(assignable), s.refused)


def aevent(s, m):
    if m[0] == "arrive":
        return ("arrive", m[1], S.door(m[-1]))
    if m[0] in ("assign", "drop"):
        p, _, r = s.arrivals[m[1]]
        return (m[0], p, r)
    return (m[0],)


def successors(k, ports, values):
    s = from_key(k, ports)
    for m in moves(s, values):
        s2 = from_key(k, ports)
        try:
            s2.step(m)
        except S.Illegal:
            continue
        yield m, aevent(s, m), s2


def concrete_graph(ports, values, depth):
    """Breadth first over concrete states: each state's number of histories (paths from the start) and one
    representative history. A state fixes its own number of events, so the levels are exact."""
    k0 = key(S.Session(ports))
    paths, rep, frontier = {k0: 1}, {k0: []}, [k0]
    for _ in range(depth):
        nxt = {}
        for k in frontier:
            for m, ae, s2 in successors(k, ports, values):
                k2 = key(s2)
                if k2 not in nxt:
                    nxt[k2] = 0
                    rep[k2] = rep[k] + [m]
                nxt[k2] += paths[k]
        paths.update(nxt)
        frontier = list(nxt)
    return paths, rep


def congruence(ports, values, depth):
    """Every concrete state with fewer than depth events: the states of one abstract class have one input log and one
    multiset of (abstract event, abstract successor). EXHAUSTIVE over those states. (states, classes, failures)."""
    k0 = key(S.Session(ports))
    seen, frontier, cls = {k0}, [k0], {}
    n = bad = 0
    for _ in range(depth):
        nxt = []
        for k in frontier:
            n += 1
            out = {}
            for m, ae, s2 in successors(k, ports, values):
                kk = (ae, akey(s2))
                out[kk] = out.get(kk, 0) + 1
                k2 = key(s2)
                if k2 not in seen:
                    seen.add(k2)
                    nxt.append(k2)
            s = from_key(k, ports)
            sig = (S.input_log(s), frozenset(out.items()))
            a = akey(s)
            bad += a in cls and cls[a] != sig
            cls.setdefault(a, sig)
        frontier = nxt
    return n, len(cls), bad


def abstract_graph(ports, values, depth):
    """Level by level over abstract classes, expanded from one representative each (exact under the congruence):
    the number of histories of at most depth events, counted with each abstract edge's multiplicity."""
    s0 = S.Session(ports)
    a0 = akey(s0)
    rep, level, total = {a0: (key(s0), [])}, {a0: 1}, 1
    for _ in range(depth):
        nxt = {}
        for a, w in level.items():
            k, h = rep[a]
            for m, ae, s2 in successors(k, ports, values):
                a2 = akey(s2)
                if a2 not in rep:
                    rep[a2] = (key(s2), h + [m])
                nxt[a2] = nxt.get(a2, 0) + w
        level = nxt
        total += sum(level.values())
    return rep, total


def quotient_rows_check(ports, values, depth):
    """Under no plant and under each of cut0_session's plants, EXHAUSTIVE over the domain: (a) each history's rows,
    the session binding aside, equal its end state's representative's; (b) its log rows equal its abstract class's
    representative's; (c) the abstraction is a congruence, and its weighted count is the number of histories."""
    print("== the rows as functions of the end state and of the abstract class (%s, every history to %d events)" % (
        ",".join(ports), depth))
    for plant in (None, "assign-refused", "hold-previous", "overwrite", "budget-uncounted", "end-anytime",
                  "no-cause", "lenient-hex", "after-end", "record-without-history", "no-source",
                  "close-after-refusal", "door-dollar", "a1-cause-under-a2"):
        S.PLANT = plant
        paths, crep = concrete_graph(ports, values, depth)
        per_state = {k: frozenset(S.check_run(h, ports)) - {"session-binds"} for k, h in crep.items()}
        n_states, n_cls, bad = congruence(ports, values, depth)
        arep, total = abstract_graph(ports, values, depth)
        per_cls = {a: frozenset(S.check_run(h, ports)) & LOG_ROWS for a, (k, h) in arep.items()}
        n = d_state = d_cls = fail_h = fail_log_h = binds = 0
        for h, s in histories(ports, values, depth):
            n += 1
            f = frozenset(S.check_run(h, ports))
            binds += "session-binds" in f
            f = f - {"session-binds"}
            fail_h += bool(f)
            fail_log_h += bool(f & LOG_ROWS)
            d_state += f != per_state[key(s)]
            d_cls += (f & LOG_ROWS) != per_cls[akey(s)]
        S.PLANT = None
        print("  plant %-23s histories %6d (counted on the states %6d, on the classes %6d); states %5d, classes %4d,"
              " congruence failures %d" % (plant or "none", n, sum(paths.values()), total, len(crep), len(arep), bad))
        print("    histories failing a row %5d (a log row %5d; the binding %d); rows differing from the state's %d, "
              "log rows differing from the class's %d" % (fail_h, fail_log_h, binds, d_state, d_cls))


def deeper(ports, values, cdepths, adepths):
    print("== deeper: each concrete state, or each abstract class, checked once; its histories counted, not listed")
    for d in cdepths:
        t0 = time.perf_counter()
        paths, rep = concrete_graph(ports, values, d)
        failed = {}
        for k, h in rep.items():
            for f in frozenset(S.check_run(h, ports)) - {"session-binds"}:
                failed[f] = failed.get(f, 0) + 1
        tlog("deeper concrete", ",".join(ports), d, "%.2fs" % (time.perf_counter() - t0), "states", len(rep))
        print("  %s, %2d events, concrete states %7d, histories %13d: rows (binding aside) failed on a state: %s" % (
            ",".join(ports), d, len(rep), sum(paths.values()),
            ", ".join("%s %d" % kv for kv in sorted(failed.items())) or "none"))
    n_states, n_cls, bad = congruence(ports, values, cdepths[-1])
    print("  %s: the congruence checked on every concrete state to %d events: %d states, %d classes, %d failures" % (
        ",".join(ports), cdepths[-1], n_states, n_cls, bad))
    for d in adepths:
        t0 = time.perf_counter()
        rep, total = abstract_graph(ports, values, d)
        failed = {}
        logs = set()
        for a, (k, h) in rep.items():
            logs.add(S.input_log(from_key(k, ports)))
            for f in frozenset(S.check_run(h, ports)) & LOG_ROWS:
                failed[f] = failed.get(f, 0) + 1
        tlog("deeper abstract", ",".join(ports), d, "%.2fs" % (time.perf_counter() - t0), "classes", len(rep))
        print("  %s, %2d events, abstract classes %6d, histories %22d, input logs %6d: log rows failed on a class: %s"
              % (",".join(ports), d, len(rep), total, len(logs),
                 ", ".join("%s %d" % kv for kv in sorted(failed.items())) or "none"))


def language_vs_image():
    print("== the strict parser's language against the projection's image (logs of at most 2 ticks)")
    for ports, values, depth in ((["a"], [B("1"), B("4"), B("1.1")], 9), (["a", "b"], [B("1"), B("4"), B("1.1")], 13)):
        acc = sorted({S.door(v)[1] for v in values if S.door(v)[0] == "ok"})
        for policy in ("A2", "A1"):
            S.POLICY = policy
            lang = parser_language(ports, acc, 2)
            n_states, n_cls, bad = congruence(ports, values, 5)
            if policy == "A1" and len(ports) == 2:
                depth = 15                  # a refused b on tick 3, after two ticks of two ports, takes 15 events
            rep, total = abstract_graph(ports, values, depth)
            img = {S.input_log(from_key(k, ports)) for k, h in rep.values()}
            missing = [b for b in lang if b not in img]
            kinds = {}
            for b in missing:
                kd = why_unreachable(b, ports)
                kinds[kd] = kinds.get(kd, 0) + 1
            S.POLICY = "A2"
            print("  ports %s, policy %s (its abstraction a congruence to 5 events: %d failures): the parser accepts %d "
                  "logs; %d are no legal history's projection (every history to %d events): %s" % (
                      ",".join(ports), policy, bad, len(lang), len(missing), depth,
                      ", ".join("%s %d" % kv for kv in sorted(kinds.items())) or "none"))
            if policy == "A2" and missing:
                smallest = min(missing, key=lambda b: (len(b), b))
                print("    the smallest, accepted by the parser yet the projection of no A2 history:")
                for line in smallest.decode().split("\n")[:-1]:
                    print("      " + (line if not line.startswith("ports") else "ports <the signature of %s>" %
                                      ",".join(ports)))
                r = S.execute(smallest, ports)
                print("    executed, it reads: status %s (a receipt core is written for it)" % r["status"])


def timing():
    """The cost of the rows per history, per concrete state and per abstract class, on D1 (stderr only)."""
    ports, values, depth = D1
    t0 = time.perf_counter()
    for h, s in histories(ports, values, depth):
        S.check_run(h, ports)
    t1 = time.perf_counter()
    paths, rep = concrete_graph(ports, values, depth)
    for k, h in rep.items():
        S.check_run(h, ports)
    t2 = time.perf_counter()
    arep, total = abstract_graph(ports, values, depth)
    for a, (k, h) in arep.items():
        S.check_run(h, ports)
    t3 = time.perf_counter()
    tlog("timing D1 to %d events, check_run: per history %.2fs (%d), per state %.2fs (%d), per class %.3fs (%d)" % (
        depth, t1 - t0, total, t2 - t1, len(rep), t3 - t2, len(arep)))


def main():
    with open(S.__file__, "rb") as fh:
        print("== the probe read: research/run-1/probes/cut0_session.py sha256 %s" % hashlib.sha256(fh.read()).hexdigest())
    fibers("D0", ([], [B("1")], 5))
    fibers("D1", D1)
    fibers("D2", D2)
    quotient_rows_check(*D1)
    quotient_rows_check(["a", "b"], [B("1"), B("1.1")], 5)
    language_vs_image()
    deeper(D1[0], D1[1], (6, 7), (6, 8, 10, 12, 14))
    deeper(D2[0], D2[1], (6, 7), (6, 8, 10, 12))
    timing()
    print("FIBERS DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())

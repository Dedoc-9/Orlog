"""LAW-SUFFICIENCY-0, test 2: equal seal, equal behaviour (SHEET.md, test 2).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/test2_equal_seal.py

Every accepted text and every generated variant that keeps its source's law seal is run, and grouped by law seal.
Within a group, every member's P must equal every other's. A variant whose seal moves is counted and reported, never
compared. A variant the compiler refuses is counted. The two plants run after the real pass."""
import re
import sys
from collections import Counter, defaultdict

import common
from orlog import interp
from orlog.front import compile_bytes

CLAUSE = re.compile(r"^(§[0-9]+(?:\.[0-9]+)*|[0-9]+(?:\.[0-9]+)*\.) ")
DECIMAL = re.compile(r"(?<![\w.])([0-9]+\.[0-9]+)(?![\w.])")


def clause_lines(lines):
    return [i for i, ln in enumerate(lines) if CLAUSE.match(ln)]


def outside_strings(line, fn):
    """Apply fn to the parts of a clause line outside double-quoted strings; None if fn changed nothing."""
    parts = line.split('"')
    new = [fn(p) if k % 2 == 0 else p for k, p in enumerate(parts)]
    out = '"'.join(new)
    return out if out != line else None


def first_in_code(lines, old, new):
    for i in clause_lines(lines):
        m = CLAUSE.match(lines[i])
        head, rest = lines[i][:m.end()], lines[i][m.end():]
        done = [False]

        def once(p):
            if not done[0] and old in p:
                done[0] = True
                return p.replace(old, new, 1)
            return p
        changed = outside_strings(rest, once)
        if changed is not None:
            return lines[:i] + [head + changed] + lines[i + 1:]
    return None


def with_title_note(lines, note):
    k = 1 if lines and lines[0].startswith("Title:") else 0
    return lines[:k] + [note] + lines[k:]


def transforms():
    """(name, function on the text's lines or its whole text): each returns the variant's text, or None."""
    def lines_of(f):
        def g(t):
            ls = t.split("\n")
            out = f(ls)
            return None if out is None else "\n".join(out)
        return g

    def decimal_zero(ls):
        out, hit = list(ls), False
        for i in clause_lines(ls):
            m = CLAUSE.match(ls[i])
            changed = outside_strings(ls[i][m.end():], lambda p: DECIMAL.sub(r"\g<1>0", p))
            if changed is not None:
                out[i] = ls[i][:m.end()] + changed
                hit = True
        return out if hit else None

    def keyword_upper(ls):
        for i in clause_lines(ls):
            m = CLAUSE.match(ls[i])
            rest = ls[i][m.end():]
            w = re.match(r"[A-Za-z]+", rest)
            if w and w.group(0).upper() != w.group(0):
                return ls[:i] + [ls[i][:m.end()] + w.group(0).upper() + rest[w.end():]] + ls[i + 1:]
        return None

    def double_space(ls):
        for i in clause_lines(ls):
            m = CLAUSE.match(ls[i])
            changed = outside_strings(ls[i][m.end():], lambda p: p.replace(" ", "  ", 1))
            if changed is not None:
                return ls[:i] + [ls[i][:m.end()] + changed] + ls[i + 1:]
        return None

    def title_changed(ls):
        if ls and ls[0].startswith("Title:"):
            return ["Title: A Variant."] + ls[1:]
        return ["Title: A Variant."] + ls

    return [
        ("crlf", lambda t: t.replace("\n", "\r\n")),
        ("bom", lambda t: "﻿" + t),
        ("trailing-spaces", lambda t: "\n".join(ln + "  " if ln else ln for ln in t.split("\n"))),
        ("blank-lines", lambda t: "\n\n" + t + "\n\n"),
        ("nbsp-in-code", lines_of(lambda ls: first_in_code(ls, " ", " "))),
        ("minus-sign", lines_of(lambda ls: first_in_code(ls, "-", "−"))),
        ("times-sign", lines_of(lambda ls: first_in_code(ls, "*", "×"))),
        ("note-added", lines_of(lambda ls: with_title_note(ls, "Note: a line added by the variant generator."))),
        ("note-nfc", lines_of(lambda ls: with_title_note(ls, "Note: café."))),
        ("title-changed", lines_of(title_changed)),
        ("decimal-zero", lines_of(decimal_zero)),
        ("double-space", lines_of(double_space)),
        ("keyword-upper", lines_of(keyword_upper)),
    ]


def members(texts):
    """The accepted texts and their kept variants: (id, budget, raw, law seal, text seal), and the variants' counts."""
    out, counts = [], defaultdict(Counter)
    for ident, kind, raw, budget in texts:
        src = compile_bytes(raw)
        out.append((ident, budget, raw, src.law_seal, src.text_seal))
        t = raw.decode("utf-8")
        for name, fn in transforms():
            v = fn(t)
            if v is None:
                counts[name]["no site"] += 1
                continue
            vraw = v.encode("utf-8")
            comp = compile_bytes(vraw)
            if not comp.ok:
                counts[name]["refused"] += 1
                continue
            if comp.law_seal != src.law_seal:
                counts[name]["law seal moved"] += 1
                continue
            counts[name]["kept, text seal %s" % ("same" if comp.text_seal == src.text_seal else "differs")] += 1
            out.append((ident + " [" + name + "]", budget, vraw, comp.law_seal, comp.text_seal))
    return out, counts


def results(mem, proj=common.projection):
    res = {}
    for ident, budget, raw, law, text in mem:
        comp = compile_bytes(raw)
        res[ident] = common.run(comp.prog, comp.an, comp.law_seal, comp.text_seal, budget, proj)
    return res


def failing(mem, res):
    groups = defaultdict(list)
    for m in mem:
        groups[m[3]].append(m)
    bad = {}
    for law, ms in groups.items():
        ps = set(res[m[0]] for m in ms)
        if len(ps) > 1:
            bad[law] = ms
    return groups, bad


def main():
    lines = []

    def say(s=""):
        lines.append(s)
        print(s, flush=True)

    texts = common.accepted()
    say("LAW-SUFFICIENCY-0, TEST 2: EQUAL SEAL, EQUAL BEHAVIOUR (research/law-sufficiency/test2_equal_seal.py)")
    say("P: the reference receipt without its backend and text-seal lines (common.projection, fixed before the run)")
    frozen = defaultdict(set)
    for ident, kind, raw, budget in texts:
        c = compile_bytes(raw)
        frozen[c.law_seal].add(c.text_seal)
    say("the accepted texts: %d, %d distinct laws; laws with two or more distinct text seals among them: %d (%d texts)"
        % (len(texts), len(frozen), sum(1 for v in frozen.values() if len(v) > 1),
           sum(len(v) for v in frozen.values() if len(v) > 1)))
    mem, counts = members(texts)
    say()
    say("== the variants, by transform (each applied once to each accepted text)")
    for name, _ in transforms():
        say("   %-16s %s" % (name, ", ".join("%s %d" % kv for kv in sorted(counts[name].items()))))
    res = results(mem)
    groups, bad = failing(mem, res)
    multi = {k: v for k, v in groups.items() if len(v) > 1}
    multi_text = {k: v for k, v in multi.items() if len(set(m[4] for m in v)) > 1}
    say()
    say("== the groups: %d laws; %d with two or more members (%d members); %d with two or more distinct text seals"
        % (len(groups), len(multi), sum(len(v) for v in multi.values()), len(multi_text)))
    outcomes = Counter(res[m[0]].split(" ")[0] if not res[m[0]].startswith("orlog-receipt") else "receipt" for m in mem)
    say("   every member's run: %s" % ", ".join("%s %d" % kv for kv in sorted(outcomes.items())))
    say("   the three spellings (examples/spellings/): %s" % spellings(mem, res))
    say()
    say("== groups whose members' P differ: %d" % len(bad))
    for law, ms in sorted(bad.items()):
        ref = res[ms[0][0]]
        for m in ms[1:]:
            if res[m[0]] != ref:
                say("   law %s: %s against %s, %s" % (law[:12], ms[0][0], m[0], common.first_difference(ref, res[m[0]])))

    say()
    say("== plants: each run alone, after the real pass; each must fail exactly the groups stated before it ran")
    want = set(multi_text)
    plant_ok = []
    orig = interp.Interp.run

    def run_folding_text_seal(self):
        r = orig(self)
        self.out += self.text_hex.encode("ascii")
        return r
    interp.Interp.run = run_folding_text_seal
    try:
        _, bad1 = failing(mem, results(mem))
    finally:
        interp.Interp.run = orig
    ok = set(bad1) == want
    plant_ok.append(ok)
    say("   plant 1, Interp folds the text seal into its output: expected to fail the %d groups with two or more text "
        "seals and no other: %d fail, %s" % (len(want), len(bad1), "CAUGHT" if ok else "NOT AS STATED"))

    def keep_text_seal(receipt):
        ls = receipt.split(b"\n")
        return b"\n".join(ln for ln in ls if not ln.startswith(b"backend ")).decode("ascii")
    _, bad2 = failing(mem, results(mem, keep_text_seal))
    ok = set(bad2) == want
    plant_ok.append(ok)
    say("   plant 2, P keeps the text-seal line (COMPAT-0's receipt core): expected to fail the same %d groups: %d fail, %s"
        % (len(want), len(bad2), "CAUGHT" if ok else "NOT AS STATED"))
    say()
    held = not bad and all(plant_ok)
    say("TEST 2 %s: %d groups with two or more members compared, %d of them across distinct text seals; %d differ; plants %d of %d"
        % ("HELD" if held else "FAILED", len(multi), len(multi_text), len(bad), sum(plant_ok), len(plant_ok)))
    sys.exit(0 if held else 1)


def spellings(mem, res):
    ids = [m for m in mem if "spellings" in m[0] and "[" not in m[0]]
    if not ids:
        frozen_ids = [m for m in mem if "[" not in m[0]]
        names = ("words", "symbols", "phrases")
        raws = {}
        for n in names:
            with open(common.os.path.join(common.ROOT, "examples", "spellings", n + ".orl"), "rb") as f:
                raws[n] = f.read()
        ids = [m for m in frozen_ids if m[2] in raws.values()]
    seals = set(m[3] for m in ids)
    texts = set(m[4] for m in ids)
    ps = set(res[m[0]] for m in ids)
    return "%d texts (%s), %d law seal, %d text seals, %d P" % (len(ids), ", ".join(m[0] for m in ids), len(seals),
                                                                 len(texts), len(ps))


if __name__ == "__main__":
    main()

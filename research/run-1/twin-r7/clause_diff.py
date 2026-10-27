"""Compare two drafts of SPEC §15 clause by clause. A clause is a top-level item of a section (a numbered item, a
bullet, a table row or a paragraph), its indented continuation lines included. Sections are matched by their number."""
import difflib
import re
import sys

A, B = sys.argv[1], sys.argv[2]


def units(path):
    text = open(path, encoding="utf-8").read()
    secs = {}
    cur = "preamble"
    secs[cur] = []
    for line in text.split("\n"):
        m = re.match(r"## (15\.\d+) ", line)
        if m:
            cur = m.group(1)
            secs[cur] = []
            continue
        if not line.strip():
            if secs[cur] and secs[cur][-1] != "":
                secs[cur].append("")
            continue
        starts = re.match(r"(\d+\. |- |\| |\*\*)", line)
        if starts or not secs[cur] or secs[cur][-1] == "":
            secs[cur].append(line.strip())
        else:
            secs[cur][-1] += " " + line.strip()
    return {k: [u for u in v if u and not re.match(r"\|[-| ]+\|$", u)] for k, v in secs.items()}


def label(u):
    u = re.sub(r"\s+", " ", u)
    return (u[:90] + "…") if len(u) > 90 else u


a, b = units(A), units(B)
total = {"changed": 0, "added": 0, "removed": 0, "unchanged": 0}
for sec in [k for k in b if k in a] + [k for k in b if k not in a]:
    ua, ub = a.get(sec, []), b[sec]
    sm = difflib.SequenceMatcher(a=ua, b=ub, autojunk=False)
    lines = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            total["unchanged"] += i2 - i1
            continue
        if op == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                if k < i2 - i1 and k < j2 - j1:
                    total["changed"] += 1
                    lines.append("CHANGED  %s" % label(ub[j1 + k]))
                elif k < j2 - j1:
                    total["added"] += 1
                    lines.append("ADDED    %s" % label(ub[j1 + k]))
                else:
                    total["removed"] += 1
                    lines.append("REMOVED  %s" % label(ua[i1 + k]))
        elif op == "insert":
            for k in range(j1, j2):
                total["added"] += 1
                lines.append("ADDED    %s" % label(ub[k]))
        elif op == "delete":
            for k in range(i1, i2):
                total["removed"] += 1
                lines.append("REMOVED  %s" % label(ua[k]))
    if lines:
        print("## %s" % sec)
        for l in lines:
            print("   " + l)
print("TOTAL %s" % total)

"""The judge's measurement for research/speed: the nine real spherical-harmonic basis functions (bands 0 to 2) in
Q31.32, at every integer lattice direction with coordinates from -R to R, normalized in Fix. Writes three laws:
  sh_say_r4.orl  every direction's nine values said (for the error against binary64), R = 4
  sh_sum_r4.orl  only the nine sums said, R = 4
  sh_sum_r8.orl  only the nine sums said, R = 8 (with R = 4, the cost of one evaluation by difference)
  PYTHONHASHSEED=0 python -B research/speed/judge/make_sh.py
"""
import os

# the judge's scripts live in research/speed/judge/; what they make and read lives in work/speed-judge/, which
# git ignores
HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "work",
                                     "speed-judge"))

# 1/(2 sqrt pi), sqrt(3/(4 pi)), (1/2) sqrt(15/pi), (1/4) sqrt(5/pi), (1/4) sqrt(15/pi), to 17 significant digits
CONSTS = [("c0", "0.28209479177387814"), ("c1", "0.4886025119029199"), ("c2", "1.0925484305920792"),
          ("c3", "0.31539156525252005"), ("c4", "0.5462742152960396")]
BASIS = [
    "c0",
    "c1 times y",
    "c1 times z",
    "c1 times x",
    "c2 times x times y",
    "c2 times y times z",
    "c3 times (3.0 times z times z minus 1.0)",
    "c2 times x times z",
    "c4 times (x times x minus y times y)",
]


def law(r, say_each):
    out = ["Title: Spherical Harmonics to Band 2 in Q31.32, R %d." % r,
           "Note: The judge's measurement for research/speed, 2026-10-26: the nine real basis functions at every "
           "integer lattice direction with coordinates from -%d to %d, normalized in Fix." % (r, r)]
    n = 0

    def top(stmt):
        nonlocal n
        n += 1
        out.append("§%d %s" % (n, stmt))
        return n

    for name, lit in CONSTS:
        top("Let %s be %s." % (name, lit))
    for k in range(9):
        top("Let s%d be 0.0." % k)
    top("Let count be 0.")
    loop = top("For each i from -%d to %d, do the following." % (r, r))
    p = "%d.1" % loop
    out.append("§%s For each j from -%d to %d, do the following." % (p, r, r))
    p += ".1"
    out.append("§%s For each k from -%d to %d, do the following." % (p, r, r))
    p += ".1"
    out.append("§%s Let n2 be i times i plus j times j plus k times k." % p)
    q = p[:-1] + "2"
    out.append("§%s If n2 is greater than 0, do the following." % q)
    body = [
        "Let len be the square root of (n2 as a fixed).",
        "Let x be (i as a fixed) divided by len.",
        "Let y be (j as a fixed) divided by len.",
        "Let z be (k as a fixed) divided by len.",
    ]
    body += ["Let y%d be %s." % (m, e) for m, e in enumerate(BASIS)]
    if say_each:
        parts = ["i", '" "', "j", '" "', "k"]
        for m in range(9):
            parts += ['" "', "y%d" % m]
        body.append("Say " + " followed by ".join(parts) + ".")
    body += ["Increase s%d by y%d." % (m, m) for m in range(9)]
    body.append("Increase count by 1.")
    for m, stmt in enumerate(body, 1):
        out.append("§%s.%d %s" % (q, m, stmt))
    parts = ['"directions "', "count", '" sums"']
    for m in range(9):
        parts += ['" "', "s%d" % m]
    top("Say " + " followed by ".join(parts) + ".")
    return "\n".join(out) + "\n"


os.makedirs(HERE, exist_ok=True)
for name, r, say_each in (("sh_say_r4", 4, True), ("sh_sum_r4", 4, False), ("sh_sum_r8", 8, False),
                           ("sh_sum_r16", 16, False)):
    with open(os.path.join(HERE, name + ".orl"), "wb") as fh:
        fh.write(law(r, say_each).encode("utf-8"))
    print("wrote", name + ".orl")

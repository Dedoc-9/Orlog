"""A deterministic battery of edge-value programs (generate(seed) for seed in range(len(BATTERY))).

Each program builds edge values of one type into variables, then applies one operation and prints or stores the
result (so refusals, printing and event encodings are all compared).
"""
S = "§"

INT_VALS = {
    "min": "(0 - 9223372036854775807) - 1", "max": "9223372036854775807", "m1": "0 - 1", "zero": "0",
    "one": "1", "two53p1": "9007199254740993", "big": "4611686018427387904", "nbig": "0 - 4611686018427387905",
    "i31": "2147483648", "ni31": "0 - 2147483648", "seven": "7", "nseven": "0 - 7",
}
FIX_VALS = {   # in fixed mode
    "fmin": "(0.0 - 2147483647.0) - 1.0", "fmax": "2147483647.99999999976716935634613037109375",
    "ulp": "0.00000000023283064365386962890625", "nulp": "0.0 - 0.00000000023283064365386962890625",
    "half": "0.5", "nhalf": "0.0 - 0.5", "onehalf": "1.5", "ntwohalf": "0.0 - 2.5", "zero": "0.0",
    "tenth": "0.1", "big": "2147483647.5", "third": "0.333",
}
FLT_VALS = {   # in floats mode
    "inf": "1.0 / 0.0", "ninf": "(0.0 - 1.0) / 0.0", "nan": "0.0 / 0.0", "nzero": "0.0 * (0.0 - 1.0)",
    "zero": "0.0", "max": str(int(1.7976931348623157e308)) + ".0", "sub": "0." + "0" * 323 + "5",
    "half": "0.5", "nhalf": "0.0 - 0.5", "twohalf": "2.5", "two63": "9223372036854775808.0",
    "ntwo63": "0.0 - 9223372036854775808.0", "big": "9007199254740993.0", "tenth": "0.1", "n3half": "0.0 - 3.5",
}

INT_UN = ["(-A)", "the absolute value of A", "the square root of A", "(A as a float)", "(A rounded to a float)",
          "(A as a fixed)", "(A rounded to a fixed)", "(A is even)", "(A is odd)", "(A is zero)", "(A is negative)",
          "(A is positive)", "(the list A, A and 1)", "(a list of 2 copies of A)"]
INT_BIN = ["(A plus B)", "(A minus B)", "(A times B)", "(A divided by B)", "the quotient of A by B",
           "the remainder of A by B", "(A modulo B)", "the larger of A and B", "the smaller of A and B", "(A < B)",
           "(A = B)", "(A is not less than B)", "(A followed by B)"]
NUM_UN = ["(-A)", "the absolute value of A", "the square root of A", "(A as an integer)", "(A rounded to an integer)",
          "the integer part of A", "(A is zero)", "(A is negative)", "(A is positive)", "(the list A, A and 1)",
          "(A as OTHER)", "(A rounded to OTHER)"]
NUM_BIN = ["(A plus B)", "(A minus B)", "(A times B)", "(A divided by B)", "the larger of A and B",
           "the smaller of A and B", "(A < B)", "(A > B)", "(A = B)", "(A != B)", "(A is not less than B)",
           "(A is not greater than B)", "(A followed by B)", "(A + 1)", "(1 < A)"]


def _battery():
    out = []
    for vals, un, bins, mode, other in ((INT_VALS, INT_UN, INT_BIN, None, None),
                                        (FIX_VALS, NUM_UN, NUM_BIN, "fixed", "a float"),
                                        (FLT_VALS, NUM_UN, NUM_BIN, "floats", "a fixed")):
        names = sorted(vals)
        for a in names:
            for op in un:
                out.append((mode, vals, (a,), op.replace("OTHER", other or "")))
        for a in names:
            for b in names:
                for op in bins:
                    out.append((mode, vals, (a, b), op))
    return out


BATTERY = _battery()


def generate(seed):
    mode, vals, args, op = BATTERY[seed % len(BATTERY)]
    lines = []
    k = 1
    if mode == "floats":
        lines.append(S + "1 Decimals are floats.")
        k = 2
    names = {}
    for i, a in enumerate(args):
        if a in names:
            continue
        v = "v%d" % (i + 1)
        names[a] = v
        lines.append("%s%d Let %s be %s." % (S, k, v, vals[a]))
        k += 1
    expr = op.replace("A", names[args[0]])
    if len(args) > 1:
        expr = expr.replace("B", names[args[1]])
    lines.append("%s%d Let r be %s." % (S, k, expr))
    lines.append("%s%d Say r." % (S, k + 1))
    lines.append("%s%d Say \"done\"." % (S, k + 2))
    return ("\n".join(lines) + "\n").encode("utf-8")


if __name__ == "__main__":
    import sys
    print(len(BATTERY))
    if len(sys.argv) > 1:
        sys.stdout.buffer.write(generate(int(sys.argv[1])))

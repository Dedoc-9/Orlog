"""RUST-CORE-0: R5's budgets, fixed before any experiment (SHEET.md Amendment 3; the owner's ruling E2).

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_r5_budgets.py --out PATH

R5 runs each text of 2 operations or more under B = floor(ops / 2), where ops is the count its RESULT run reports under
its own budget. Those counts are already fixed: research/rust-core/s3-budgets.txt records them, from two fresh
reference runs per text (SHEET.md Amendment 2). So this reads that file, holds it to the sha256 Amendment 2 records, and
writes one row per text with its B. It runs nothing and draws nothing, so the values depend on no later Python.

The values are the file it writes: research/rust-core/r5-budgets.txt, named in the sheet by its sha256. This tool is
outside the core author's reading set (D1)."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S3 = os.path.join(HERE, "s3-budgets.txt")
S3_SHA256 = "86f3a7b08f6713b240b3705fdf5fe3abb93b4d75de104fad7c5e194c4bb578bd"     # SHEET.md Amendment 2


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(path):
    with open(S3, "rb") as f:
        s3 = f.read()
    if sha(s3) != S3_SHA256:
        sys.exit("GEN-R5: s3-budgets.txt is not the file Amendment 2 records")
    rows, skipped = [], []
    for line in s3.decode("ascii").split("\n"):
        if not line or line.startswith("#"):
            continue
        w = line.split(" ")
        ident, kind, budget, cls = w[0], w[1], int(w[3]), w[5]
        if cls != "RESULT":
            sys.exit("GEN-R5: %s is %s in s3-budgets.txt; R5's values need every text's count" % (ident, cls))
        status, ops = w[6], int(w[w.index("ops") + 1])
        if ops < 2:
            skipped.append(ident)
            continue
        b = ops // 2
        if b > budget:
            sys.exit("GEN-R5: %s's B %d exceeds its own budget %d" % (ident, b, budget))
        rows.append("%s %s budget %d class RESULT %s ops %d B %d" % (ident, kind, budget, status, ops, b))
    head = [
        "# R5's budgets: SHEET.md Amendment 3, fixed before any experiment (the owner's ruling E2, 2026-10-30)",
        "# generator research/rust-core/gen_r5_budgets.py sha256 %s" % sha(open(os.path.abspath(__file__), "rb").read()),
        "# read from research/rust-core/s3-budgets.txt sha256 %s (SHEET.md Amendment 2): each text's ops, the count of "
        "its RESULT run under its own budget, from two fresh reference runs" % S3_SHA256,
        "# B = floor(ops / 2) for each text of 2 operations or more; %d texts, in s3-budgets.txt's order; %d texts of "
        "fewer than 2 operations draw none: %s" % (len(rows), len(skipped), " ".join(skipped) if skipped else "none"),
        "# a row: id kind budget <b> class RESULT, the run's status word, ops, and B",
    ]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    with open(path, "wb") as f:
        f.write(data)
    print("GEN-R5: %d texts with a B, %d with none; sha256 %s" % (len(rows), len(skipped), sha(data)))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--out":
        main(sys.argv[2])
    else:
        sys.exit("usage: gen_r5_budgets.py --out PATH")

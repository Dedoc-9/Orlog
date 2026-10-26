#!/usr/bin/env python3
"""Run every program of twin/inputs/ (by manifest.json) through twin.py into twin/out/.

Writes NAME.out and NAME.receipt for each program, and NAME.trace (the RUNTIME-SPEC §5
trace lines) as an aid to whoever compares. A compile refusal writes NAME.compile with
the refusal printed by twin.py and no .out or .receipt. Prints one line per program.
Exit status 0 when every program produced a receipt, 1 otherwise.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "inputs")
OUT = os.path.join(HERE, "out")
TWIN = os.path.join(HERE, "twin.py")


def main():
    with open(os.path.join(INPUTS, "manifest.json"), "rb") as fh:
        manifest = json.loads(fh.read().decode("utf-8"))
    os.makedirs(OUT, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONUTF8"] = "1"
    failures = 0
    for name in sorted(manifest):
        entry = manifest[name]
        prog = os.path.join(INPUTS, name + ".orl")
        paths = dict((ext, os.path.join(OUT, name + "." + ext)) for ext in ("out", "receipt", "trace", "compile"))
        for p in paths.values():
            if os.path.exists(p):
                os.remove(p)
        cmd = [sys.executable, "-B", TWIN, prog, entry["law_seal"], entry["text_seal"],
               paths["out"], paths["receipt"], paths["trace"]]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        err = res.stderr.decode("utf-8", "replace").strip()
        if res.returncode == 0:
            status = ops = events = "?"
            with open(paths["receipt"], "rb") as fh:
                for line in fh.read().decode("ascii").split("\n"):
                    if line.startswith("status "):
                        status = line[7:]
                    elif line.startswith("ops "):
                        ops = line[4:]
                    elif line.startswith("events "):
                        events = line[7:]
            print("%-28s %-40s ops %-9s events %s%s" % (name, status, ops, events, ("   [" + err + "]") if err else ""))
        else:
            failures += 1
            with open(paths["compile"], "wb") as fh:
                fh.write((err + "\n").encode("utf-8"))
            print("%-28s exit %d: %s" % (name, res.returncode, err))
    print("%d programs, %d without a receipt" % (len(manifest), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run the twin on every probe of twin/probes/ (by its manifest.json).

usage: python probe_run.py [--check] [--seals FILE.json] [--alt N,N...]

The law seal is 64 zeros (the probes' law seals are UNKNOWN to the twin), or the probe's entry
in --seals FILE.json ({"NAME": "<64 hex>"}), for instance the reference's seals, to compare
trace heads too. The text seal is the sha256 of the file. For each probe it writes
twin/probes/out/NAME.out, NAME.receipt and NAME.trace, or NAME.refused holding the compile
refusal's code. --check compares every result with twin/probes/expected.json (worked by hand,
see EXPECTED.md) and prints each difference; --alt passes the twin's --alt through.
Exit status 0, or 1 when --check found a difference.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes")
OUT = os.path.join(PROBES, "out")
TWIN = os.path.join(HERE, "twin.py")
ZERO_SEAL = "0" * 64
REFUSED_RE = re.compile(r"twin: compile refused (\S+)")


def run_probe(name, law, alt):
    path = os.path.join(PROBES, name + ".orl")
    with open(path, "rb") as fh:
        text_seal = hashlib.sha256(fh.read()).hexdigest()
    paths = dict((ext, os.path.join(OUT, name + "." + ext)) for ext in ("out", "receipt", "trace", "refused"))
    for p in paths.values():
        if os.path.exists(p):
            os.remove(p)
    cmd = [sys.executable, "-B", TWIN] + (["--alt", alt] if alt else []) + [
        path, law, text_seal, paths["out"], paths["receipt"], paths["trace"]]
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONUTF8"] = "1"
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    err = res.stderr.decode("utf-8", "replace")
    if res.returncode == 0:
        return {"receipt": read_text(paths["receipt"]), "output": read_bytes(paths["out"]),
                "trace": read_text(paths["trace"])}
    m = REFUSED_RE.search(err)
    if res.returncode == 1 and m:
        with open(paths["refused"], "wb") as fh:
            fh.write((m.group(1) + "\n").encode("ascii"))
        return {"refused": m.group(1)}
    return {"error": "exit %d: %s" % (res.returncode, err.strip())}


def read_text(p):
    with open(p, "rb") as fh:
        return fh.read().decode("utf-8")


def read_bytes(p):
    with open(p, "rb") as fh:
        return fh.read()


def receipt_fields(text):
    fields = {}
    claims = []
    for line in text.split("\n"):
        if line.startswith("claim "):
            claims.append(line)
        elif " " in line:
            k, v = line.split(" ", 1)
            fields[k] = v
    return fields, claims


def compare(name, got, exp):
    diffs = []
    if "error" in got:
        return ["twin failed: " + got["error"]]
    if "refused" in exp:
        if got.get("refused") != exp["refused"]:
            diffs.append("expected refused %s, got %s" % (exp["refused"], describe(got)))
        return diffs
    if "refused" in got:
        return ["expected a run (%s), got refused %s" % (exp["status"], got["refused"])]
    if not got["receipt"].endswith("\nend\n"):
        diffs.append("the receipt does not end with 'end' and LF (§11 item 57)")
    fields, claims = receipt_fields(got["receipt"])
    want = {"status": exp["status"], "output-bytes": str(exp["output_bytes"]), "output-sha256": exp["output_sha256"],
            "events": str(exp["events"]), "ops": str(exp["ops"]), "claims": str(len(exp["claims"]))}
    for k, v in sorted(want.items()):
        if fields.get(k) != v:
            diffs.append("%s: expected %s, got %s" % (k, v, fields.get(k)))
    if claims != exp["claims"]:
        diffs.append("claim lines: expected %s, got %s" % (exp["claims"], claims))
    if got["output"] != exp["output"].encode("utf-8"):
        diffs.append("output: expected %r, got %r" % (exp["output"], got["output"].decode("utf-8", "replace")))
    if "trace" in exp:
        lines = [l.split(" ") for l in got["trace"].split("\n") if l]
        events = [[l[1], int(l[2]), "" if l[3] == "-" else l[3]] for l in lines]
        if events != exp["trace"]:
            diffs.append("events: expected %s, got %s" % (exp["trace"], events))
    return diffs


def describe(got):
    if "refused" in got:
        return "refused " + got["refused"]
    if "receipt" in got:
        return "a run: " + receipt_fields(got["receipt"])[0].get("status", "?")
    return got.get("error", "?")


def main(argv):
    check = "--check" in argv
    seals = {}
    alt = None
    if "--seals" in argv:
        with open(argv[argv.index("--seals") + 1], "rb") as fh:
            seals = json.loads(fh.read().decode("utf-8"))
    if "--alt" in argv:
        alt = argv[argv.index("--alt") + 1]
    with open(os.path.join(PROBES, "manifest.json"), "rb") as fh:
        manifest = json.loads(fh.read().decode("utf-8"))
    expected = {}
    if check:
        with open(os.path.join(PROBES, "expected.json"), "rb") as fh:
            expected = json.loads(fh.read().decode("utf-8"))
    os.makedirs(OUT, exist_ok=True)
    n_diff = 0
    n_ref = 0
    for name in sorted(manifest):
        law = seals.get(name, ZERO_SEAL)
        got = run_probe(name, law, alt)
        if "refused" in got:
            n_ref += 1
        line = "%-48s %s" % (name, describe(got))
        if check:
            diffs = compare(name, got, expected[name])
            if diffs:
                n_diff += 1
                line += "   DIFFERS: " + "; ".join(diffs)
        print(line)
    print("%d probes: %d refused at compile time, %d ran%s" % (
        len(manifest), n_ref, len(manifest) - n_ref,
        ("; %d differ from expected.json" % n_diff) if check else ""))
    return 1 if (check and n_diff) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

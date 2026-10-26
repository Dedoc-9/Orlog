#!/usr/bin/env python3
"""Run the twin on every probe of a probe folder (by its manifest.json).

usage: python probe_run.py [--dir probes|probes3] [--check] [--settled] [--alts] [--seals FILE.json] [--alt N,...]

--dir picks the folder under twin/ (default probes, the round-2 probes; probes3 holds the round-3
probes for SPEC §12 and §13). The law seal is 64 zeros (the probes' law seals are UNKNOWN to the
twin), or the probe's entry in --seals FILE.json ({"NAME": "<64 hex>"}), for instance the
reference's seals, to compare trace heads too. The text seal is the sha256 of the file. For each
probe it writes DIR/out/NAME.out, NAME.receipt and NAME.trace, or NAME.refused holding the compile
refusal's code. --check compares every result with DIR/expected.json (worked by hand, see
EXPECTED.md) and prints each difference; --alt passes the twin's --alt through.
--settled (with --check) replaces an expectation by the code DIR/settled.json records for it (the
readings SPEC §13 settled against the twin), and marks a settled code of the door, which the twin
does not implement, as such. --alts runs each probe whose expectation names an "alt_key" with
--alt alt_key and compares the result with its hand-worked "alt_expect".
Exit status 0, or 1 when a comparison found a difference (door codes under --settled excepted).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TWIN = os.path.join(HERE, "twin.py")
ZERO_SEAL = "0" * 64
REFUSED_RE = re.compile(r"twin: compile refused (\S+)")
DOOR_CODES = set("BYTES-NOT-UTF8 BIDI-CONTROL CONTROL-CHAR INVISIBLE-CHAR DASH-AMBIGUOUS NON-ASCII-CODE "
                 "UNTERMINATED-TEXT QUOTE-BOUNDARY".split())          # SPEC §13, phase 1


def run_probe(probes, name, law, alt):
    out_dir = os.path.join(probes, "out")
    path = os.path.join(probes, name + ".orl")
    with open(path, "rb") as fh:
        text_seal = hashlib.sha256(fh.read()).hexdigest()
    paths = dict((ext, os.path.join(out_dir, name + "." + ext)) for ext in ("out", "receipt", "trace", "refused"))
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
    return {"error": "exit %d: %s" % (res.returncode, err.strip().splitlines()[-1] if err.strip() else "")}


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


def arg(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def load(path):
    with open(path, "rb") as fh:
        return json.loads(fh.read().decode("utf-8"))


def main(argv):
    check = "--check" in argv
    probes = os.path.join(HERE, arg(argv, "--dir", "probes"))
    seals = load(arg(argv, "--seals")) if "--seals" in argv else {}
    alt = arg(argv, "--alt")
    manifest = load(os.path.join(probes, "manifest.json"))
    expected = load(os.path.join(probes, "expected.json")) if (check or "--alts" in argv) else {}
    settled = {}
    if "--settled" in argv and os.path.exists(os.path.join(probes, "settled.json")):
        settled = load(os.path.join(probes, "settled.json"))
    os.makedirs(os.path.join(probes, "out"), exist_ok=True)
    n_diff = n_ref = n_door = 0
    for name in sorted(manifest):
        got = run_probe(probes, name, seals.get(name, ZERO_SEAL), alt)
        if "refused" in got:
            n_ref += 1
        line = "%-48s %s" % (name, describe(got))
        if check:
            exp = expected[name]
            if name in settled:
                exp = {"refused": settled[name]["settled"]}
                line += "   [settled: %s]" % settled[name]["settled"]
            diffs = compare(name, got, exp)
            if diffs and name in settled and settled[name]["settled"] in DOOR_CODES:
                n_door += 1
                line += "   DIFFERS (a door code; the twin takes canonical text): " + "; ".join(diffs)
            elif diffs:
                n_diff += 1
                line += "   DIFFERS: " + "; ".join(diffs)
        print(line)
    print("%d probes: %d refused at compile time, %d ran%s" % (
        len(manifest), n_ref, len(manifest) - n_ref,
        ("; %d differ from expected.json%s" % (n_diff, (", %d more on a door code" % n_door) if n_door else ""))
        if check else ""))
    n_alt_diff = 0
    if "--alts" in argv:
        alts = [n for n in sorted(manifest) if "alt_key" in expected[n]]
        for name in alts:
            exp = expected[name]
            got = run_probe(probes, name, seals.get(name, ZERO_SEAL), exp["alt_key"])
            diffs = compare(name, got, exp["alt_expect"])
            n_alt_diff += 1 if diffs else 0
            print("%-48s --alt %-18s %s%s" % (name, exp["alt_key"], describe(got),
                                               ("   DIFFERS: " + "; ".join(diffs)) if diffs else ""))
        print("%d probes run under their other reading; %d differ from alt_expect" % (len(alts), n_alt_diff))
    return 1 if (n_diff or n_alt_diff) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

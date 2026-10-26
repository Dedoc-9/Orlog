"""Prepare the clean-room twin's inputs: canonical texts and seals (twin/inputs/), and the reference's
expected outputs and receipts kept apart (build/twin-expected/), where the twin is told not to look."""
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402
import selftest as T  # noqa: E402

inp = os.path.join(ROOT, "twin", "inputs")
exp = os.path.join(ROOT, "build", "twin-expected")
os.makedirs(inp, exist_ok=True)
os.makedirs(exp, exist_ok=True)
programs = {}
for p in T.corpus():
    programs[os.path.splitext(os.path.basename(p))[0]] = T.read(p)
for code, raw in T.RUNTIME_REFUSALS:
    programs["refuse-" + code.lower()] = raw
manifest = {}
for name, raw in sorted(programs.items()):
    comp = compile_bytes(raw)
    assert comp.ok, name
    with open(os.path.join(inp, name + ".orl"), "wb") as fh:
        fh.write(comp.text.encode("utf-8"))
    manifest[name] = {"law_seal": comp.law_seal, "text_seal": comp.text_seal, "seal_words": comp.seal_words}
    it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
    with open(os.path.join(exp, name + ".out"), "wb") as fh:
        fh.write(bytes(it.out))
    with open(os.path.join(exp, name + ".receipt"), "wb") as fh:
        fh.write(it.receipt("twin"))
with open(os.path.join(inp, "manifest.json"), "wb") as fh:
    fh.write(json.dumps(manifest, indent=1, sort_keys=True).encode("ascii"))
print("twin inputs:", len(manifest))

"""One batch of the reference-against-twin differential run (tests/diff_twin.py starts this in a subprocess, so that a
text that loops for a long time can be stopped by a timeout).

  python -B tests/diff_worker.py IN.json OUT.json

IN.json is a list of canonical texts. OUT.json is a list of results, one per text, each {"ref": R, "twin": R}, where
R is {"code": CODE} for a compile refusal, {"crash": TEXT} for an exception that is not a refusal, or
{"core": RECEIPT-WITHOUT-ITS-BACKEND-LINE, "out_sha256": HEX, "out_len": N} for a run. The twin is given the
reference's law seal and text seal (it cannot compute a law seal: SPEC §11 items 61 and 62).
"""
import hashlib
import importlib.util
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog.arbiter import receipt_core  # noqa: E402
from orlog.front import compile_bytes  # noqa: E402
from orlog.interp import Interp  # noqa: E402

ZERO = "0" * 64


def load_twin():
    spec = importlib.util.spec_from_file_location("orlog_twin_main", os.path.join(ROOT, "twin", "twin.py"))
    mod = importlib.util.module_from_spec(spec)
    saved = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = saved
    return mod


def crash(e):
    return {"crash": "%s: %s" % (type(e).__name__, str(e)[:300])}


def run_reference(text):
    try:
        comp = compile_bytes(text.encode("utf-8"))
    except Exception as e:      # a crash is a finding: every text is refused or run
        return crash(e), None, None
    if not comp.ok:
        # a law seal exists only when the refusal is SEAL-MISMATCH; the twin gets it, never a made-up one (a zero
        # seal's words are babab-babab-babab-babab, so a text sealed with them read as accepted: the first run)
        return {"code": comp.error.code}, getattr(comp, "law_seal", None), getattr(comp, "text_seal", None)
    try:
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal).run()
        rec = it.receipt()
        out = bytes(it.out)
    except Exception as e:
        return crash(e), comp.law_seal, comp.text_seal
    core = receipt_core(rec)
    return ({"core": core.decode("ascii") if core is not None else None,
             "out_sha256": hashlib.sha256(out).hexdigest(), "out_len": len(out)}, comp.law_seal, comp.text_seal)


def run_twin(twin, text, law, text_seal):
    try:
        prog = twin.compile_text(text, law or ZERO)
    except twin.CompileRefusal as e:
        return {"code": e.code}
    except Exception as e:
        return crash(e)
    if law is None:             # the reference refused it: only the code is compared
        return {"code": None}
    try:
        rt, status = twin.execute(prog, law)
        rec = twin.receipt_text(rt, status, prog, law, text_seal).encode("ascii")
        out = bytes(rt.out)
    except Exception as e:
        return crash(e)
    core = receipt_core(rec)
    return {"core": core.decode("ascii") if core is not None else None,
            "out_sha256": hashlib.sha256(out).hexdigest(), "out_len": len(out)}


def main():
    with open(sys.argv[1], "rb") as fh:
        texts = json.loads(fh.read().decode("utf-8"))
    twin = load_twin()
    results = []
    for text in texts:
        ref, law, text_seal = run_reference(text)
        results.append({"ref": ref, "twin": run_twin(twin, text, law, text_seal)})
    with open(sys.argv[2], "wb") as fh:
        fh.write(json.dumps(results, sort_keys=True).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

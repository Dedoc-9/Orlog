"""The arbiter: one law, the reference and three compiled backends, compared byte for byte.

What it decides, and on what authority:
  - Agreement is integrity: every receipt (minus its backend line) and every output byte equal.
    It shows that four executions did the same thing; it does not show the law is right.
  - On disagreement the reference's output is kept, because the reference is the DECLARED
    authority (a small definition, the de Bruijn criterion), never because of a vote. Each
    dissent is localized to its first divergent event and written down. When the compiled
    backends agree with each other against the reference, that is REFERENCE-DISSENT: the
    reference is still kept, and the witness says loudly that its authority is a declaration.
Compilation is memoized by the sha256 of the generated source and the flags; runs never are,
because a run is the observation.
"""
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

from .front import compile_bytes
from .interp import Interp
from .lower import Lowered
from . import gen_py, gen_c, gen_rs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
C_RT = os.path.join(ROOT, "rt_c", "orlog_rt.h")
RS_RT = os.path.join(ROOT, "rt_rs", "orlog_rt.rs")
BACKENDS = ("python", "c99", "rust")
C_FLAGS = ["-std=c99", "-O2", "-ffp-contract=off", "-fno-fast-math", "-Wall", "-Wno-unused-variable",
           "-Wno-unused-but-set-variable", "-Wno-unused-function"]
RS_FLAGS = ["--edition", "2021", "-O"]
VERDICT_KEYS = {"verdict", "valid", "passed", "healthy", "anomaly", "correct", "legal", "safe", "approved",
                "score_is_good"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def file_sha(path):
    with open(path, "rb") as fh:
        return sha(fh.read())


def toolchains():
    def first(cmd):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True)
            return (r.stdout or r.stderr).splitlines()[0].strip()
        except (OSError, IndexError):
            return "unavailable"
    return {"python": platform.python_version(), "clang": first(["clang", "--version"]),
            "rustc": first(["rustc", "--version"])}


def parse_receipt(b):
    """For display and for the court's reading only. Agreement is decided by receipt_core, never by this."""
    lines = b.decode("ascii", "replace").splitlines()
    return [l for l in lines if not l.startswith("backend ")]


BACKEND_LINE = re.compile(rb"^backend [a-z0-9]+\n")


def receipt_core(b):
    """The receipt's exact bytes with its second line, and only that line, removed; None if the frame is wrong.
    Agreement is byte equality of cores (red team E7: a CRLF receipt, a missing final LF, or an injected 'backend'
    line had all counted as agreeing, because the comparison went through splitlines and dropped every such line)."""
    head = b"orlog-receipt 0\n"
    if b is None or not b.startswith(head):
        return None
    rest = b[len(head):]
    m = BACKEND_LINE.match(rest)
    if m is None:
        return None
    core = head + rest[m.end():]
    if not core.endswith(b"\nend\n") or b"\r" in core:
        return None
    return core


def generate(backend, low):
    if backend == "python":
        return gen_py.generate(low)
    if backend == "c99":
        return gen_c.generate(low, C_RT)
    if backend == "rust":
        return gen_rs.generate(low, RS_RT)
    raise ValueError(backend)


class Arbiter:
    def __init__(self, workdir, backends=BACKENDS, mutate=None, c_flags=None, reference_patch=None):
        self.workdir = workdir
        self.backends = backends
        self.mutate = mutate or (lambda backend, src: src)
        self.c_flags = c_flags or C_FLAGS
        self.reference_patch = reference_patch
        os.makedirs(os.path.join(workdir, "cache"), exist_ok=True)

    # ------------------------------------------------ building and running
    # Every path a compiler or a compiled program sees is relative and ASCII, with the working directory set: with a
    # work folder named ØRLǪG, the C runtime's fopen on the narrow argv and the GNU linker both failed (red team E11).
    def build(self, backend, src):
        ext = {"python": ".py", "c99": ".c", "rust": ".rs"}[backend]
        flags = {"python": [], "c99": self.c_flags, "rust": RS_FLAGS}[backend]
        key = sha((src + "\0" + " ".join(flags)).encode("utf-8"))[:24]
        cache = os.path.join(self.workdir, "cache")
        name = "%s-%s" % (backend, key)
        srcpath = os.path.join(cache, name + ext)
        if not os.path.exists(srcpath):
            with open(srcpath, "wb") as fh:
                fh.write(src.encode("utf-8"))
        if backend == "python":
            return [sys.executable, "-I", "-B", os.path.join("cache", name + ext)], "interpreted", key
        exe_rel = os.path.join("cache", name + ".exe")
        if os.path.exists(os.path.join(self.workdir, exe_rel)):
            return [exe_rel], "cached", key
        if backend == "c99":
            cmd = ["clang"] + flags + [name + ext, "-o", name + ".exe"]
        else:
            cmd = ["rustc"] + flags + [name + ext, "-o", name + ".exe"]
        # Build in a fresh directory under the system temp folder and copy the program back: rustc writes linker
        # temporaries beside its output, and the GNU linker cannot open a non-ASCII path (red team E11). This assumes
        # the system temp path is ASCII (true on this host; NOT_MEASURED elsewhere).
        tmp = tempfile.mkdtemp(prefix="orlog-build-")
        try:
            shutil.copyfile(srcpath, os.path.join(tmp, name + ext))
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp)
            built = os.path.join(tmp, name + ".exe")
            if r.returncode != 0 or not os.path.exists(built):
                raise RuntimeError("%s build failed:\n%s" % (backend, (r.stdout + r.stderr)[-4000:]))
            shutil.copyfile(built, os.path.join(cache, name + ".exe"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return [exe_rel], "built", key

    def run(self, cmd, tag, trace=False):
        names = (tag + ".out", tag + ".receipt", tag + ".trace")
        out, rec, trc = (os.path.join(self.workdir, n) for n in names)
        for p in (out, rec, trc):
            if os.path.exists(p):
                os.remove(p)
        env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
        exe = cmd[0] if cmd[0] == sys.executable else os.path.join(self.workdir, cmd[0])
        args = [exe] + cmd[1:] + list(names[:2]) + ([names[2]] if trace else [])
        r = subprocess.run(args, capture_output=True, env=env, cwd=self.workdir)
        res = {"exit": r.returncode, "stderr": r.stderr.decode("utf-8", "replace")[-2000:]}
        res["out"] = open(out, "rb").read() if os.path.exists(out) else None
        res["receipt"] = open(rec, "rb").read() if os.path.exists(rec) else None
        res["trace"] = open(trc, "rb").read().decode().splitlines() if trace and os.path.exists(trc) else None
        return res

    # ------------------------------------------------ the arbitration
    def arbitrate(self, raw, name="program"):
        comp = compile_bytes(raw)
        w = {"name": name, "compiled": comp.ok}
        if not comp.ok:
            w["refusal"] = {"code": comp.error.code, "line": comp.error.line, "message": comp.error.msg}
            w["door"] = comp.canon.events
            return comp, w, None
        ref = self.reference(comp, trace=False)
        low = Lowered(comp)
        results = {}
        for b in self.backends:
            src = self.mutate(b, generate(b, low))
            try:
                cmd, how, key = self.build(b, src)
            except RuntimeError as e:
                results[b] = {"build": "FAILED", "error": str(e)}
                continue
            r = self.run(cmd, "%s-%s" % (name, b))
            r.update({"build": how, "source_sha256": sha(src.encode("utf-8")), "cmd": cmd})
            results[b] = r
        ref_core = receipt_core(ref.receipt())
        agree, dissent = [], []
        for b, r in results.items():
            ok = (r.get("receipt") is not None and receipt_core(r["receipt"]) == ref_core and ref_core is not None
                  and r.get("out") == bytes(ref.out) and r.get("exit") == 0)
            (agree if ok else dissent).append(b)
        notes = []
        if dissent:
            ref_t = self.reference(comp, trace=True)
            for b in dissent:
                r = results[b]
                if r.get("build") == "FAILED":
                    notes.append({"backend": b, "kind": "BUILD-FAILED", "detail": r["error"][-600:]})
                    continue
                again = self.run(r["cmd"], "%s-%s-trace" % (name, b), trace=True)
                notes.append(self.localize(comp, b, ref_t, again))
        # the kind is read over the backends that built; a failed build is reported, never a vote (red team E8)
        built = [b for b in self.backends if results.get(b, {}).get("build") != "FAILED"]
        failed = [b for b in self.backends if results.get(b, {}).get("build") == "FAILED"]
        built_dissent = [b for b in dissent if b in built]
        if not dissent:
            kind = "NONE"
        elif not built_dissent:
            kind = "BUILD-FAILED"
        elif len(built_dissent) == len(built) and len(built) >= 2 and self._agree_among(
                [results[b] for b in built_dissent]):
            kind = "REFERENCE-DISSENT"
        else:
            kind = "BACKEND-DISSENT"
        w["build_failed"] = failed
        w.update({
            "seals": {"raw": comp.raw_seal, "text": comp.text_seal, "law": comp.law_seal, "law_words": comp.seal_words},
            "door": [e for e in comp.canon.events],
            "literal_notes": comp.an.notes,
            "reference": {"status": ref.status, "output_sha256": sha(bytes(ref.out)), "events": ref.events,
                          "trace_head": ref.head.hex(), "ops": ref.ops,
                          "receipt_sha256": sha(ref.receipt())},
            "backends": {b: self._summary(r) for b, r in results.items()},
            "agreeing": sorted(agree), "dissenting": sorted(dissent), "dissent_kind": kind,
            "mismatch_notes": notes,
            "authority": "the reference interpreter, by declaration (not proven; not a vote)",
            "final_output_sha256": sha(bytes(ref.out)),
        })
        return comp, w, ref

    def reference(self, comp, trace):
        it = Interp(comp.prog, comp.an, comp.law_seal, comp.text_seal, trace=trace)
        if self.reference_patch:
            with self.reference_patch():
                return it.run()
        return it.run()

    def _agree_among(self, rs):
        cores = [receipt_core(r.get("receipt")) for r in rs]
        outs = [r.get("out") for r in rs]
        return cores[0] is not None and all(x == cores[0] for x in cores) and all(o == outs[0] for o in outs)

    def _summary(self, r):
        if r.get("build") == "FAILED":
            return {"build": "FAILED"}
        rec = parse_receipt(r["receipt"]) if r.get("receipt") else []
        get = lambda k: next((l.split(" ", 1)[1] for l in rec if l.startswith(k + " ")), None)
        return {"build": r["build"], "source_sha256": r["source_sha256"], "exit": r["exit"],
                "status": get("status"), "output_sha256": sha(r["out"]) if r.get("out") is not None else None,
                "events": get("events"), "trace_head": get("trace-head"), "ops": get("ops"),
                "receipt_sha256": sha("\n".join(rec).encode()) if rec else None}

    def localize(self, comp, backend, ref, run):
        """The first event where the backend and the reference part, decoded, plus the first output byte."""
        labels = {c.id: c.label for c in comp.prog.clauses}
        note = {"backend": backend, "kind": "DIVERGENCE"}
        rt, bt = ref.trace or [], run.get("trace") or []
        idx = None
        for i in range(max(len(rt), len(bt))):
            a = rt[i] if i < len(rt) else None
            b = bt[i] if i < len(bt) else None
            if a != b:
                idx = i
                break
        if idx is None:
            note["first_divergent_event"] = None
            note["detail"] = "traces equal; the difference is outside the event chain (exit %s)" % run.get("exit")
        else:
            a = rt[idx].split(" ") if idx < len(rt) else None
            b = bt[idx].split(" ") if idx < len(bt) else None
            note["first_divergent_event"] = idx + 1
            src = a or b
            note["clause"] = "§" + labels.get(int(src[2]), "?")
            note["event_kind"] = src[1]
            note["reference_payload"] = a[3] if a else "(no event: the reference stopped)"
            note["backend_payload"] = b[3] if b else "(no event: the backend stopped)"
        ro, bo = bytes(ref.out), run.get("out") or b""
        off = next((i for i in range(min(len(ro), len(bo))) if ro[i] != bo[i]), None)
        if off is None and len(ro) != len(bo):
            off = min(len(ro), len(bo))
        note["first_output_byte_differing"] = off
        note["replacement"] = "the reference's bytes are kept (declared authority); this backend's run is quarantined"
        return note


def scope_for(w):
    return {
        "certifies": ["each listed backend's receipt and output were compared byte for byte with the reference's, "
                      "on this host, in this run"],
        "does_not_certify": ["that the law means what its author intended", "that any claim is true",
                             "that the reference interpreter is correct (its authority is declared)",
                             "agreement on any other host, compiler, or version",
                             "anything about programs or inputs not run"],
        "unmeasured": ["cross-host identity", "cross-compiler identity beyond the named toolchains"],
    }


FORBIDDEN = ["the program is correct", "the claims are true", "the backends are bug-free",
             "agreement implies correctness", "this result holds on another machine"]


def witness_artifact(w, extra_provenance=None):
    """Executable epistemics' five fields; a verdict-shaped key anywhere in data is refused."""
    def scan(node, path="data"):
        if isinstance(node, dict):
            for k, v in node.items():
                if str(k).lower() in VERDICT_KEYS:
                    raise ValueError("verdict-shaped field %s.%s refused" % (path, k))
                scan(v, "%s.%s" % (path, k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                scan(v, "%s[%d]" % (path, i))
    scan(w)
    src = {}
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith(".py"):
            src[fn] = file_sha(os.path.join(HERE, fn))
    for p in (C_RT, RS_RT):
        if os.path.exists(p):
            src[os.path.relpath(p, ROOT).replace("\\", "/")] = file_sha(p)
    prov = {"orlog_sources_sha256": src, "toolchains": toolchains(), "host": platform.platform(),
            "pythonhashseed": os.environ.get("PYTHONHASHSEED")}
    if extra_provenance:
        prov.update(extra_provenance)
    art = {"data": w, "provenance": prov, "claim_class": "orlog_cross_backend_agreement_only",
           "validity_scope": scope_for(w), "forbidden_interpretations": FORBIDDEN}
    art["chain_hash"] = sha(json.dumps(art, sort_keys=True, ensure_ascii=True).encode())
    return art

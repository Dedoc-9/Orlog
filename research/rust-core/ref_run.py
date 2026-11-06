"""RUST-CORE-0: the reference runner, one program for every reference run of the experiment but R8's (SHEET.md
Amendments 4 to 7; the owner's rulings F2, N3, U2 and D5, and REREAD-4's K3 and K15, REREAD-5's L3 and L5, REREAD-6's
M7, REREAD-7's X3, X4, X13 and Y14).

One run, in a fresh process, from the run's own folder (its working directory):

    python -B research/rust-core/ref_run.py text BUDGET PATH             a text, through the front end
    python -B research/rust-core/ref_run.py law BUDGET TEXTSEAL PATH     law bytes, through decoder1 (R6)

BUDGET is `none`, or a canonical decimal: digits only, no sign, no leading zero. TEXTSEAL is 64 lowercase hex digits.
PATH is the input, outside the run's folder. Add `--files` to have it write the run's output, receipt (when there is
one) and trace into its folder, as `reference.out`, `reference.receipt` and `reference.trace`. The trace's digest, and
its file, are its lines joined by LF, with no LF after the last (SHEET.md Amendment 7, X11).

Every way it ends, and nothing else:
- **A result**, exit 0: stdout's last line is `RUN COMPLETED ops <n> p <sha256 of P> trace <sha256 of the trace>`,
  `RUN REFUSED ...` alike, or `RUN STOPPED ops <n> trace <sha256 of the trace>`. P is the receipt without its `backend`
  and `text-seal` lines.
- **decoder1's refusal**, exit 0: stdout's last line is `DECODER-REFUSED <message>`. decoder1's `DecodeError` is caught
  where `decode` is called, and nowhere else; the message is `ascii(str(e))`, one line.
- **A crash of the reference**, exit 1: any other exception raised once the reference has begun (the front end,
  decoder1's `decode`, the interpreter), `SystemExit` included. Its traceback is printed, then, as the last line on
  stderr, `REFERENCE-EXCEPTION <module>.<qualname>` of the exception's type, written by this program's own handler.
- **A fault of the runner**, exit 3: stderr's last line is `RUNNER-FAULT <reason>`. Every failure before the reference
  begins is one (his D5): the runner's own imports; arguments not as above (the usage); an input it cannot read; the
  ENV line not made; a `__pycache__` folder in `src/orlog`, `research/rust-core` or `research/law-sufficiency`; the
  reference's modules (`orlog`, and decoder1 in law mode) not importable, whatever the exception; decoder1.py not the
  file the sheet pins by sha256, or holding a plant. And after it has begun: an interrupt (`KeyboardInterrupt`); a text
  the front end refuses, since every text of the experiment is one it accepts; the outcome not written. A runner fault
  is never a class of a case: `classify` raises `RunnerFault`, and the experiment stops there. It is an interruption of
  the experiment (SHEET.md Amendments 6 and 7: the attempt is kept and repeated whole; a second interruption of the same
  experiment, of any cause, stops it, and it goes to the owner).

Before the outcome, stdout holds two lines of conditions:
- first, once the arguments are checked and the reference's modules imported, `ENV python <implementation> <version>
  recursion-limit <n> format_check <not-imported|imported>; <platform>; orlog <module>=<sha256> ...`, every `orlog`
  module loaded then, by name, each with its file's sha256;
- then, after the reference has run, `CONDITIONS after-run recursion-limit <n> format_check <...>; orlog ...` alike.

`classify(run1, run2)` decides a case's reference class from its two runs. Each run is given raw, as (exit status,
stdout bytes, stderr bytes), or the word TIMEOUT. It reads their lines itself: ASCII with any other byte replaced, CR LF
made LF, the last line that is not empty. A harness passes what the process gave and decides nothing itself. Besides
the four classes it raises, deciding no class (his D5):
- `RunnerFault`, for a run whose stderr ends with the runner's `RUNNER-FAULT` line;
- `Anomaly`, for an exit 3 without that line: the experiment stops, and it is reported, never classed or guessed;
- `Interrupted`, for an exit status the runner never gives (not 0, 1 or 3) with `KeyboardInterrupt` last on stderr.

It sets no recursion limit, never imports format_check, reads no clock and no environment variable. It is outside the
core author's reading set (D1)."""
import os
import sys


def fault(reason):
    """End as a fault of the runner: its line last on stderr, exit 3."""
    sys.stdout.flush()
    sys.stderr.write("RUNNER-FAULT %s\n" % reason)
    sys.stderr.flush()
    os._exit(3)


try:
    import hashlib
    import platform
    import re
    import traceback
except BaseException as e:             # his D5: a failure before the reference begins is the runner's
    fault("the runner's own imports failed: %s" % type(e).__name__)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
USAGE = "usage: ref_run.py text BUDGET PATH [--files] | ref_run.py law BUDGET TEXTSEAL PATH [--files]"
NAT = re.compile(r"(?:0|[1-9][0-9]*)\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
DECODER1 = os.path.join(ROOT, "research", "law-sufficiency", "decoder1.py")
DECODER1_SHA256 = "3584f565f6929879c3d942a45b3fa8d5c09cc2382b67772559109e38930ab877"     # SHEET.md Amendment 3
BYTECODE = [os.path.join(ROOT, *p) for p in (("src", "orlog"), ("research", "rust-core"), ("research", "law-sufficiency"))]


class RunnerFault(Exception):
    """A run the runner itself could not make. Never a class of a case: the experiment stops."""


class Anomaly(Exception):
    """An exit 3 without the runner's line (his D5): no class, no runner fault; the experiment stops, and it is
    reported."""


class Interrupted(Exception):
    """An exit status the runner never gives, with KeyboardInterrupt last on stderr (his D5): an interruption."""


def last_line(data):
    """The last line that is not empty, of a process's output as bytes: ASCII, any other byte replaced, CR LF as LF."""
    lines = [ln for ln in data.decode("ascii", "replace").replace("\r\n", "\n").split("\n") if ln]
    return lines[-1] if lines else ""


def classify(run1, run2):
    """A case's reference class from its two raw runs: RESULT, REFERENCE-REFUSED, NO-REFERENCE-RESULT or UNSTABLE.
    Raises RunnerFault, Anomaly or Interrupted for a run that is none of the reference's (his D5)."""
    def kind(r):
        if r == "TIMEOUT":
            return ("timeout",)
        status, out, err = r[0], last_line(r[1]), last_line(r[2])
        if err.startswith("RUNNER-FAULT "):
            raise RunnerFault(err)
        if status == 3:
            raise Anomaly("exit 3 without its line")
        if status not in (0, 1) and err.startswith("KeyboardInterrupt"):
            raise Interrupted("exit %d with KeyboardInterrupt" % status)
        if status == 0 and out.startswith("RUN "):
            return ("result", out)
        if status == 0 and out.startswith("DECODER-REFUSED "):
            return ("refused", out)
        typ = err[len("REFERENCE-EXCEPTION "):] if err.startswith("REFERENCE-EXCEPTION ") else "none"
        return ("crash", status, typ)
    a, b = kind(run1), kind(run2)
    if a[0] == "result" and a == b:
        return "RESULT"
    if a[0] == "refused" and a == b:
        return "REFERENCE-REFUSED"
    if a[0] in ("crash", "timeout") and a == b:
        return "NO-REFERENCE-RESULT"
    return "UNSTABLE"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, data):
    with open(name, "wb") as f:
        f.write(data)


def arguments(argv):
    """The arguments checked before anything runs: (mode, budget, textseal, raw input, files), or a runner fault."""
    files = argv[-1:] == ["--files"]
    if files:
        argv = argv[:-1]
    if len(argv) == 3 and argv[0] == "text":
        mode, budget_s, textseal, path = "text", argv[1], None, argv[2]
    elif len(argv) == 4 and argv[0] == "law":
        mode, budget_s, textseal, path = "law", argv[1], argv[2], argv[3]
        if not HEX64.match(textseal):
            fault("TEXTSEAL is not 64 lowercase hex digits; " + USAGE)
    else:
        fault(USAGE)
    if budget_s != "none" and not NAT.match(budget_s):
        fault("BUDGET is not none or a canonical decimal; " + USAGE)
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as e:
        fault("the input cannot be read: %s" % type(e).__name__)
    return mode, None if budget_s == "none" else int(budget_s), textseal, raw, files


def setup(mode):
    """Everything before the reference begins: the bytecode check, the reference's modules, decoder1's pin and plant.
    Every failure here is the runner's (his D5)."""
    for d in BYTECODE:
        if os.path.isdir(os.path.join(d, "__pycache__")):
            fault("a __pycache__ folder stands in %s" % os.path.relpath(d, ROOT).replace(os.sep, "/"))
    sys.path.insert(0, os.path.join(ROOT, "src"))
    try:
        from orlog import interp
        mods = {"interp": interp}
        if mode == "text":
            from orlog.front import compile_bytes
            mods["compile_bytes"] = compile_bytes
    except Exception as e:
        fault("the reference's modules cannot be imported: %s" % type(e).__name__)
    if mode == "law":
        try:
            with open(DECODER1, "rb") as f:
                pinned = sha(f.read()) == DECODER1_SHA256
        except OSError as e:
            fault("decoder1.py cannot be read: %s" % type(e).__name__)
        if not pinned:
            fault("decoder1.py is not the file the sheet pins by sha256")
        sys.path.insert(0, os.path.join(ROOT, "research", "law-sufficiency"))
        try:
            import decoder1
        except Exception as e:
            fault("decoder1 cannot be imported: %s" % type(e).__name__)
        if decoder1.PLANT is not None:
            fault("decoder1 holds a plant")
        mods["decoder1"] = decoder1
    return mods


def conditions():
    """The run's conditions: the recursion limit, whether format_check is loaded, and every orlog module loaded, each
    by its file's sha256 (his D5, REREAD-7's X3 and X13)."""
    orlog = []
    for name in sorted(n for n in sys.modules if n == "orlog" or n.startswith("orlog.")):
        path = getattr(sys.modules[name], "__file__", None)
        if path:
            with open(path, "rb") as f:
                orlog.append("%s=%s" % (name, sha(f.read())))
    return "recursion-limit %d format_check %s; orlog %s" % (
        sys.getrecursionlimit(), "imported" if "format_check" in sys.modules else "not-imported", " ".join(orlog))


def reference(mods, mode, budget, textseal, raw, files):
    """One reference run, begun: its outcome line, or an exception for the handler in main."""
    interp = mods["interp"]
    if mode == "text":
        c = mods["compile_bytes"](raw)
        if not c.ok:
            fault("the front end refuses the text (%s), which the experiment holds as one it accepts" % c.error.code)
        prog, an, law_seal, text_seal = c.prog, c.an, c.law_seal, c.text_seal
    else:
        decoder1 = mods["decoder1"]
        try:
            prog, an = decoder1.decode(raw)
        except decoder1.DecodeError as e:
            return "DECODER-REFUSED %s" % ascii(str(e))
        law_seal, text_seal = sha(raw), textseal
    it = interp.Interp(prog, an, law_seal, text_seal, trace=True, budget=budget)
    try:
        it.run()
    except interp.HostStop as e:
        trace_text = "\n".join(it.trace)
        if files:
            write("reference.out", bytes(it.out))
            write("reference.trace", trace_text.encode("ascii"))
        return "RUN STOPPED ops %d trace %s" % (e.ops, sha(trace_text.encode("ascii")))
    trace_text = "\n".join(it.trace)
    receipt = it.receipt("reference")
    lines = receipt.decode("ascii").split("\n")
    p = "\n".join(ln for ln in lines if not ln.startswith(("backend ", "text-seal ")))
    status = [ln for ln in lines if ln.startswith("status ")][0][len("status "):].split(" ")[0]
    ops = int([ln for ln in lines if ln.startswith("ops ")][0][len("ops "):])
    if files:
        write("reference.out", bytes(it.out))
        write("reference.receipt", receipt)
        write("reference.trace", trace_text.encode("ascii"))
    return "RUN %s ops %d p %s trace %s" % (status, ops, sha(p.encode("ascii")), sha(trace_text.encode("ascii")))


def main(argv):
    try:                                # before the reference begins: every failure is the runner's (his D5)
        args = arguments(argv)
        mods = setup(args[0])
        print("ENV python %s %s %s" % (platform.python_implementation(), platform.python_version(),
                                           conditions().replace("; orlog", "; %s; orlog" % platform.platform(), 1)),
              flush=True)
    except KeyboardInterrupt:
        fault("interrupted")
    except Exception as e:
        fault("before the reference began: %s" % type(e).__name__)
    try:
        line = reference(mods, *args)
    except KeyboardInterrupt:
        fault("interrupted")
    except BaseException as e:          # SystemExit included: a reference that exits is a crash, not a result
        try:
            traceback.print_exc()
            sys.stderr.write("REFERENCE-EXCEPTION %s.%s\n" % (type(e).__module__, type(e).__qualname__))
            sys.stderr.flush()
            sys.stdout.flush()
        finally:
            os._exit(1)
    try:
        print("CONDITIONS after-run %s" % conditions())
        print(line)
        sys.stdout.flush()
    except KeyboardInterrupt:
        fault("interrupted")
    except Exception as e:
        fault("the outcome could not be written: %s" % type(e).__name__)


if __name__ == "__main__":
    main(sys.argv[1:])

"""RUST-CORE-0: the reference's class on each of R6's 10,000 mutants, recorded before any experiment (SHEET.md
Amendments 4 to 7; the owner's rulings F2, N3, U2, B, F and the R6 remake, and REREAD-4's K3, REREAD-5's L3, REREAD-7's
X5, X8, X10).

Run from the repository's root:

    PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_r6_reference.py --out GEN1 GEN2 --record RECORD
                                                                                   [--only 1|2]

It makes the record twice, as two generations, one after the other (his R6 remake ruling, which supersedes F1's
concurrent generations for this attempt only): generation 1 to completion into GEN1, then generation 2 into GEN2, each
its own experiment (his B2), sharing no mutable state, no cache and no output: each has its own copy of the mutants'
files, its own run folders, its own attempt record and its own file. Generation 2 starts only once generation 1 has
completed. `--only N` makes generation N alone (the repeat of one interrupted generation; `--only 2` only after
generation 1 completed). Once both generations have completed, it compares their files byte for byte, and writes
RECORD, the same bytes, only when they are equal; when they differ, the attempt fails verification and no record is
written (his R6 remake ruling, 1, 4 and 5: no generation is selected, no type normalized, no row discarded).

For each mutant of research/rust-core/r6-mutants.txt (held to the sha256 Amendment 3 records), a generation runs the
reference runner twice: `ref_run.py law 1000000 <64 zeros> <the mutant's file>`, each run a fresh `python -B` process
with PYTHONHASHSEED=0, in a process group of its own (his B3), under a 60-second limit, its working directory a fresh
empty folder of its own, the mutant's file outside it. A generation has 4 workers (his F1). Each case is classed by
`ref_run.classify` as soon as its two runs end (REREAD-7's X10), from the runs raw.

**The attempt record** (his B2 and B4, REREAD-7's X10; the proposal of an attempt record put to him beside his A-F
ruling). Every attempt of a generation has a folder of its own under `work/rust-core/attempts/` (outside the
repository's tracked files), named `r6-reference-5-gen<N>-a<n>`:
- `attempt.json`, written before any child process starts: the experiment and attempt, `retry_of`, the command, the
  inputs and sources by sha256, the environment, the worker count, the limit and the budget, the clock its times are
  read by, and the host's commit before the generation (his R6 remake ruling, 3);
- `runs.jsonl`, one line appended as each run ends: the case, the run, its start and end (seconds since the epoch, by
  that clock), its exit status or timeout, its wall time and CPU time (software timings), its raw stdout and stderr,
  what it left in its folder. A mutant's start is its first run's and its end its second's (his 3);
- `host.jsonl`, the host's commit and physical memory in use, read twice a second while the generation runs (his 3);
- `end.json`, its one terminal disposition: COMPLETED; INTERRUPTED, with its cause (RUNNER-FAULT, HARNESS-FAULT, a run
  INTERRUPTED, OPERATOR-INTERRUPT, ENV-MISMATCH, RUN-LEFT-FILES) and reason; or STOPPED-ANOMALY (an exit 3 without the
  runner's line, his D5: stopped and reported, never classed). Beside it, his F1's figures: wall time, CPU time, peak
  host commit and physical memory in use, workers, process-start failures, and the runs past 30 s (half the limit, X5);
  the host's commit after the generation (his 3); and a COMPLETED attempt's file's sha256.
Nothing is ever deleted: a `finally` closes the record, never removes it. Only a COMPLETED attempt writes its file.

**The protocol** (his B1-B4). A generation's first attempt that ends INTERRUPTED is repeated whole, as its next
attempt, `retry_of` the first; the repeat is asked for by running this again. If the repeat is interrupted too, by any
cause, the generation stops: it refuses a third attempt, which goes to the owner. It refuses any attempt after a
COMPLETED one (a completed attempt stands) and after a STOPPED-ANOMALY. An attempt folder with no `end.json` (the
harness itself ended) counts as interrupted. A run that cannot be started is a harness fault: the attempt stops there;
workers are never reduced to go on (his F1).

**The record** is RECORD, written only from two COMPLETED generations' files that are byte for byte equal, each held
to the sha256 its attempt record states, and named in the sheet by its sha256. It records what the reference did when
the mutants were fixed, so that R6's power is known before the experiment. Its rows depend on host load where a run
comes near the limit (REREAD-7's X5): such runs are listed in the attempt record. A crash's type can depend on the
host's free memory (mutant 09729, SHEET.md Amendment 7). It refuses to run if HEAD is not the starting commit, if src/,
tests/ or vectors/ differ from it, or if an output exists. It never imports format_check, and it is outside the core
author's reading set (D1)."""
import concurrent.futures
import ctypes
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "2e9805aaa1ceeae0beb443d527680796b66f39c7"
MUTANTS_SHA256 = "a8f704fbba7ec3bcebc662de076c0ff0b52e101479dff98618ee84880bd8e155"     # SHEET.md Amendment 3
BUDGET = 1000000
TEXTSEAL = "0" * 64
LIMIT_S = 60
WORKERS = 4             # his F1(a): four per generation; for this attempt one generation after the other (R6 remake)
FLAG_S = 30             # REREAD-7's X5: a run past half the limit is listed
RAISE_S = 45            # his F1: workers may be raised only while no run passes 45 s and no process fails to start
RECORDS = os.path.join(ROOT, "work", "rust-core", "attempts")
EXPERIMENT = "r6-reference-5"     # his R6 remake ruling's attempt; each generation an experiment of its own
CLOCK = time.get_clock_info("time")     # the clock each run's start and end are read by, recorded with its resolution
WINDOWS = os.name == "nt"
sys.path.insert(0, HERE)
import ref_run                  # noqa: E402  (its classify; ref_run imports nothing at import time but the stdlib)


class Stop(Exception):
    """An attempt ends here, without a record: its cause and reason go to its end record."""

    def __init__(self, cause, reason, case=None):
        super().__init__(reason)
        self.cause, self.reason, self.case = cause, reason, case


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(*rel):
    with open(os.path.join(ROOT, *rel), "rb") as f:
        return sha(f.read())


# -- the host's figures (his F1): software readings, labelled so, never a claim about speed
class FILETIME(ctypes.Structure):
    _fields_ = [("lo", ctypes.c_uint32), ("hi", ctypes.c_uint32)]


class PERFINFO(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_uint32), ("CommitTotal", ctypes.c_size_t), ("CommitLimit", ctypes.c_size_t),
                ("CommitPeak", ctypes.c_size_t), ("PhysicalTotal", ctypes.c_size_t),
                ("PhysicalAvailable", ctypes.c_size_t), ("SystemCache", ctypes.c_size_t),
                ("KernelTotal", ctypes.c_size_t), ("KernelPaged", ctypes.c_size_t),
                ("KernelNonpaged", ctypes.c_size_t), ("PageSize", ctypes.c_size_t), ("HandleCount", ctypes.c_uint32),
                ("ProcessCount", ctypes.c_uint32), ("ThreadCount", ctypes.c_uint32)]


def cpu_seconds(p):
    """A finished child's CPU time, user and kernel, from the system (Windows); None elsewhere."""
    if not WINDOWS:
        return None
    c, e, k, u = FILETIME(), FILETIME(), FILETIME(), FILETIME()
    if not ctypes.windll.kernel32.GetProcessTimes(ctypes.c_void_p(int(p._handle)), ctypes.byref(c), ctypes.byref(e),
                                                  ctypes.byref(k), ctypes.byref(u)):
        return None
    return round((((k.hi << 32) | k.lo) + ((u.hi << 32) | u.lo)) / 1e7, 3)


def host_figures():
    """The host's commit in use, its commit limit and its physical memory in use, in bytes, now, with the time read;
    the figures None where they cannot be read."""
    t = round(time.time(), 3)
    if not WINDOWS:
        return {"t": t, "commit": None, "commit_limit": None, "physical_in_use": None}
    pi = PERFINFO()
    pi.cb = ctypes.sizeof(pi)
    if not ctypes.windll.kernel32.K32GetPerformanceInfo(ctypes.byref(pi), pi.cb):
        return {"t": t, "commit": None, "commit_limit": None, "physical_in_use": None}
    return {"t": t, "commit": pi.CommitTotal * pi.PageSize, "commit_limit": pi.CommitLimit * pi.PageSize,
            "physical_in_use": (pi.PhysicalTotal - pi.PhysicalAvailable) * pi.PageSize}


class Monitor(threading.Thread):
    """Reads the host's memory twice a second; each generation keeps every reading over its own span, in its attempt
    record's host.jsonl (his R6 remake ruling, 3), and reads the peaks."""

    def __init__(self):
        super().__init__(daemon=True)
        self.lock, self.spans, self.done = threading.Lock(), {}, threading.Event()

    def open(self, name, path):
        with self.lock:
            self.spans[name] = [None, None, open(path, "a", encoding="utf-8", newline="\n")]

    def close(self, name):
        with self.lock:
            s = self.spans.pop(name)
            s[2].flush()
            os.fsync(s[2].fileno())
            s[2].close()
            return s[0], s[1]

    def run(self):
        while not self.done.wait(0.5):
            h = host_figures()
            c, m = h["commit"], h["physical_in_use"]
            with self.lock:
                for s in self.spans.values():
                    s[2].write(json.dumps(h, sort_keys=True) + "\n")
                    if c is not None:
                        s[0] = c if s[0] is None else max(s[0], c)
                        s[1] = m if s[1] is None else max(s[1], m)


# -- the attempt record (his B2, B4; X10)
def history(experiment):
    """The earlier attempts of an experiment: [(attempt id, disposition)], the disposition None for a folder whose
    attempt never ended."""
    out = []
    n = 1
    while os.path.isdir(os.path.join(RECORDS, "%s-a%d" % (experiment, n))):
        end = os.path.join(RECORDS, "%s-a%d" % (experiment, n), "end.json")
        disp = None
        if os.path.isfile(end):
            with open(end, encoding="utf-8") as f:
                disp = json.load(f)["disposition"]
        out.append(("%s-a%d" % (experiment, n), disp))
        n += 1
    return out


def next_attempt(experiment):
    """The next attempt's id and retry_of, or a refusal under his B1-B3."""
    past = history(experiment)
    if any(d == "COMPLETED" for _, d in past):
        return None, None, "a completed attempt of %s stands; it is not made again" % experiment
    if any(d == "STOPPED-ANOMALY" for _, d in past):
        return None, None, "an attempt of %s stopped on an anomaly; it goes to the owner" % experiment
    if len(past) >= 2:
        return None, None, ("%s was interrupted on its repeat; it stops, and goes to the owner (his B1, B3)"
                            % experiment)
    return "%s-a%d" % (experiment, len(past) + 1), (past[-1][0] if past else None), None


class Attempt:
    """One attempt's durable record: written before execution, appended as runs end, closed, never erased."""

    def __init__(self, ident, meta):
        self.folder = os.path.join(RECORDS, ident)
        os.makedirs(self.folder)                        # never an existing folder
        self.lock, self.n = threading.Lock(), 0
        self._write("attempt.json", meta)
        self.runs = open(os.path.join(self.folder, "runs.jsonl"), "a", encoding="utf-8", newline="\n")

    def _write(self, name, obj):
        with open(os.path.join(self.folder, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, indent=1, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())

    def run(self, rec):
        with self.lock:
            self.runs.write(json.dumps(rec, sort_keys=True) + "\n")
            self.runs.flush()
            self.n += 1
            if self.n % 500 == 0:
                os.fsync(self.runs.fileno())

    def end(self, rec):
        with self.lock:
            self.runs.flush()
            os.fsync(self.runs.fileno())
            self.runs.close()
            self._write("end.json", rec)


# -- one generation
def one_run(num, k, law_path, work, attempt, check):
    """One fresh reference run, recorded as it ends: raw (exit status, stdout, stderr) or TIMEOUT, and its wall time."""
    folder = tempfile.mkdtemp(dir=work)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1")
    extra = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if WINDOWS else {"start_new_session": True}
    start = round(time.time(), 3)
    t0 = time.perf_counter()
    try:
        p = subprocess.Popen([sys.executable, "-B", os.path.join(HERE, "ref_run.py"), "law", str(BUDGET), TEXTSEAL,
                              law_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=folder, env=env, **extra)
    except OSError as e:
        shutil.rmtree(folder, ignore_errors=True)
        attempt.run({"case": num, "run": k, "start": start, "end": round(time.time(), 3),
                     "start_failure": "%s: %s" % (type(e).__name__, e)})
        raise Stop("HARNESS-FAULT", "run %d of mutant %s could not be started: %s" % (k, num, type(e).__name__), num)
    try:
        out, err = p.communicate(timeout=LIMIT_S)
        raw = (p.returncode, out, err)
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        raw = "TIMEOUT"
    wall = time.perf_counter() - t0
    end = round(time.time(), 3)
    cpu = cpu_seconds(p)
    left = sorted(os.listdir(folder))
    shutil.rmtree(folder, ignore_errors=True)
    attempt.run({"case": num, "run": k, "start": start, "end": end, "status": None if raw == "TIMEOUT" else p.returncode,
                 "timeout": raw == "TIMEOUT", "wall_s": round(wall, 3), "cpu_s": cpu,
                 "stdout": out.decode("latin-1"), "stderr": err.decode("latin-1"), "left": left})
    if left:
        raise Stop("RUN-LEFT-FILES", "run %d of mutant %s left %s in its folder" % (k, num, left), num)
    if raw != "TIMEOUT" and raw[0] in (0, 1):
        check(num, k, out)
    return raw, wall


def show(r):
    if r == "TIMEOUT":
        return "timeout"
    status, out, err = r[0], ref_run.last_line(r[1]), ref_run.last_line(r[2])
    if status == 0:
        return out
    typ = err[len("REFERENCE-EXCEPTION "):] if err.startswith("REFERENCE-EXCEPTION ") else "none"
    return "crash exit %d type %s" % (status, typ)


def generation(gen, out_path, mutants, laws, experiment, monitor, operator_stop, header_sources):
    """One generation, one attempt: its summary. The record file is written only when the attempt completes."""
    ident, retry_of, refusal = next_attempt(experiment)
    if refusal:
        return {"gen": gen, "disposition": "REFUSED", "reason": refusal}
    default = int(subprocess.run([sys.executable, "-B", "-c", "import sys; print(sys.getrecursionlimit())"],
                                 capture_output=True).stdout.decode().strip())
    orlog_sha = {}
    for name in os.listdir(os.path.join(ROOT, "src", "orlog")):
        if name.endswith(".py"):
            mod = "orlog" if name == "__init__.py" else "orlog." + name[:-3]
            orlog_sha[mod] = sha_file("src", "orlog", name)
    meta = {"experiment": experiment, "attempt": ident, "retry_of": retry_of, "generation": gen,
            "command": "python -B research/rust-core/ref_run.py law %d %s <the mutant's file>, twice per mutant"
                       % (BUDGET, TEXTSEAL),
            "inputs": header_sources, "environment": {"python": platform.python_implementation() + " " +
                                                      platform.python_version(), "platform": platform.platform(),
                                                      "PYTHONHASHSEED": "0", "default recursion limit": default},
            "workers": WORKERS, "limit_s": LIMIT_S, "budget": BUDGET, "mutants": len(mutants),
            "clock": {"read_by": "time.time", "implementation": CLOCK.implementation,
                      "resolution_s": CLOCK.resolution},
            "host_before": host_figures(),              # his R6 remake ruling, 3
            "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    attempt = Attempt(ident, meta)                      # written before any child process starts (his B4)
    expected = {"env": None}
    tail = "recursion-limit %d format_check not-imported; " % default

    def fields_ok(line):
        if tail not in line or "; orlog " not in line:
            return False
        mods = dict(x.split("=", 1) for x in line.split("; orlog ", 1)[1].split(" ") if "=" in x)
        return bool(mods) and all(orlog_sha.get(m) == d for m, d in mods.items())

    def check(num, k, out):
        """REREAD-7's X10: every run's conditions, against a fresh interpreter's and the files'."""
        ls = [ln for ln in out.decode("ascii", "replace").replace("\r\n", "\n").split("\n") if ln]
        env = ls[0] if ls and ls[0].startswith("ENV ") else None
        with attempt.lock:
            if expected["env"] is None and env is not None and fields_ok(env):
                expected["env"] = env
        if env is None or env != expected["env"]:
            raise Stop("ENV-MISMATCH", "run %d of mutant %s: its ENV line is not the attempt's" % (k, num), num)
        if len(ls) >= 3 and ls[-1].startswith(("RUN ", "DECODER-REFUSED ")) and not (
                ls[-2].startswith("CONDITIONS after-run ") and fields_ok(ls[-2])):
            raise Stop("ENV-MISMATCH", "run %d of mutant %s: its after-run conditions are not the default" % (k, num),
                       num)

    work = tempfile.mkdtemp(prefix="r6ref-g%d-" % gen)
    stop, first = threading.Event(), []
    results, walls = {}, []
    t0, cpu0 = time.perf_counter(), 0.0
    monitor.open(gen, os.path.join(attempt.folder, "host.jsonl"))

    def case(i):
        if stop.is_set() or operator_stop.is_set():
            return
        num, op, m = mutants[i]
        try:
            r1, w1 = one_run(num, 1, laws[i], work, attempt, check)
            r2, w2 = one_run(num, 2, laws[i], work, attempt, check)
            walls.extend([(w1, num, 1), (w2, num, 2)])
            cls = ref_run.classify(r1, r2)
            results[i] = (cls, r1, r2)
        except Stop as e:
            halt(e)
        except ref_run.RunnerFault as e:
            halt(Stop("RUNNER-FAULT", "mutant %s: %s" % (num, e), num))
        except ref_run.Anomaly as e:
            halt(Stop("STOPPED-ANOMALY", "mutant %s: %s" % (num, e), num))
        except ref_run.Interrupted as e:
            halt(Stop("INTERRUPTED", "mutant %s: a run was interrupted (%s)" % (num, e), num))
        except BaseException as e:
            halt(Stop("HARNESS-FAULT", "mutant %s: the harness raised %s" % (num, type(e).__name__), num))

    def halt(e):
        with attempt.lock:
            if not first:
                first.append(e)
        stop.set()

    try:
        with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
            list(pool.map(case, range(len(mutants))))
    finally:
        shutil.rmtree(work, ignore_errors=True)
        peak_commit, peak_phys = monitor.close(gen)
    wall = time.perf_counter() - t0
    if operator_stop.is_set() and not first:
        first.append(Stop("OPERATOR-INTERRUPT", "the operator interrupted the harness"))
    complete = not first and len(results) == len(mutants)
    cpu = None
    runs_cpu = []
    with open(os.path.join(attempt.folder, "runs.jsonl"), encoding="utf-8") as f:
        for ln in f:
            r = json.loads(ln)
            if r.get("cpu_s") is not None:
                runs_cpu.append(r["cpu_s"])
    if runs_cpu:
        cpu = round(sum(runs_cpu), 3)
    over = sorted((round(w, 3), num, k) for w, num, k in walls if w > FLAG_S)
    max_wall = round(max((w for w, _, _ in walls), default=0.0), 3)
    disposition = "COMPLETED" if complete else ("STOPPED-ANOMALY" if first[0].cause == "STOPPED-ANOMALY"
                                                else "INTERRUPTED")
    end = {"disposition": disposition, "cause": None if complete else first[0].cause,
           "reason": None if complete else first[0].reason, "case": None if complete else first[0].case,
           "cases_classed": len(results), "cases": len(mutants), "wall_s": round(wall, 3), "cpu_s": cpu,
           "cpu_note": "the runs' own CPU time, user and kernel, summed (software readings)" if cpu is not None else
           "not read on this platform", "peak_commit_bytes": peak_commit, "peak_physical_in_use_bytes": peak_phys,
           "workers": WORKERS, "process_start_failures": sum(1 for e in first if e.cause == "HARNESS-FAULT"
                                                             and "could not be started" in e.reason),
           "runs_over_%d_s" % FLAG_S: over, "max_run_wall_s": max_wall,
           "workers_may_rise": max_wall <= RAISE_S and not any("could not be started" in e.reason for e in first),
           "host_before": meta["host_before"], "host_after": host_figures(),     # his R6 remake ruling, 3
           "ended": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if not complete:
        attempt.end(end)
        return dict(end, gen=gen, attempt=ident)
    counts, rows, envs = {}, [], set()
    for i, (num, op, m) in enumerate(mutants):
        cls, r1, r2 = results[i]
        counts[cls] = counts.get(cls, 0) + 1
        rows.append("%s %s %s run1 %s | run2 %s" % (num, op, cls, show(r1), show(r2)) if cls == "UNSTABLE"
                    else "%s %s %s %s" % (num, op, cls, show(r1)))
    head = [
        "# The reference on R6's mutants: SHEET.md Amendments 4 to 7, recorded before any experiment (the owner's "
        "rulings F2, N3, U2, B, F and the R6 remake, 2026-10-30)",
        "# generator research/rust-core/gen_r6_reference.py sha256 %s" % header_sources["generator"],
        "# runner research/rust-core/ref_run.py sha256 %s; decoder1 research/law-sufficiency/decoder1.py sha256 %s; "
        "src/orlog/interp.py sha256 %s; mutants research/rust-core/r6-mutants.txt sha256 %s" % (
            header_sources["runner"], header_sources["decoder1"], header_sources["interp"], MUTANTS_SHA256),
        "# each mutant: ref_run.py law %d %s <its file>, twice, each a fresh `python -B` process in a process group "
        "of its own, PYTHONHASHSEED=0, the default recursion limit, a %d s limit, its working directory a fresh empty "
        "folder left empty; classed by ref_run.classify as its runs end; %d workers in each of two generations made one "
        "after the other" % (BUDGET, TEXTSEAL, LIMIT_S, WORKERS),
        "# environment, as every run reported it: %s" % expected["env"],
        "# classes: %s" % ", ".join("%s %d" % kv for kv in sorted(counts.items())),
        "# a row: the mutant's number, its operator, its class, and the outcome: the runner's RUN or DECODER-REFUSED "
        "line, or a crash's exit and type, or timeout; both runs for UNSTABLE",
    ]
    data = ("\n".join(head + rows) + "\n").encode("ascii")
    end["output_sha256"] = sha(data)
    attempt.end(end)
    with open(out_path, "wb") as f:
        f.write(data)
    return dict(end, gen=gen, attempt=ident, sha256=sha(data), classes=counts, rows=len(rows))


def completed(experiment):
    """An experiment's COMPLETED attempt and its end record, or None."""
    for ident, disp in history(experiment):
        if disp == "COMPLETED":
            with open(os.path.join(RECORDS, ident, "end.json"), encoding="utf-8") as f:
                return ident, json.load(f)
    return None


def main(argv):
    if len(argv) not in (5, 7) or argv[0] != "--out" or argv[3] != "--record" or (
            len(argv) == 7 and (argv[5] != "--only" or argv[6] not in ("1", "2"))):
        sys.exit("usage: gen_r6_reference.py --out GEN1 GEN2 --record RECORD [--only 1|2]")
    outs = {1: os.path.abspath(argv[1]), 2: os.path.abspath(argv[2])}
    record = os.path.abspath(argv[4])
    gens = [int(argv[6])] if len(argv) == 7 else [1, 2]
    if git("rev-parse", "HEAD") != BASE:
        sys.exit("GEN-R6-REF: HEAD is not the starting commit %s" % BASE[:7])
    if git("status", "--porcelain", "--untracked-files=all", "--", "src", "tests", "vectors"):
        sys.exit("GEN-R6-REF: src/, tests/ or vectors/ differ from the starting commit")
    if os.path.exists(record):
        sys.exit("GEN-R6-REF: %s exists; a record is never written over" % record)
    for g in gens:
        if os.path.exists(outs[g]):
            sys.exit("GEN-R6-REF: %s exists; a generation's file is never written over" % outs[g])
    if gens == [2] and completed("%s-gen1" % EXPERIMENT) is None:
        sys.exit("GEN-R6-REF: generation 2 starts only once generation 1 has completed (his R6 remake ruling, 2)")
    mpath = os.path.join(HERE, "r6-mutants.txt")
    with open(mpath, "rb") as f:
        if sha(f.read()) != MUTANTS_SHA256:
            sys.exit("GEN-R6-REF: r6-mutants.txt is not the file Amendment 3 records")
    import gen_r6_mutants
    mutants = gen_r6_mutants.mutants(mpath)
    sources = {"generator": sha_file("research", "rust-core", "gen_r6_reference.py"),
               "runner": sha_file("research", "rust-core", "ref_run.py"),
               "decoder1": sha_file("research", "law-sufficiency", "decoder1.py"),
               "interp": sha_file("src", "orlog", "interp.py"), "mutants": MUTANTS_SHA256}
    inputs = tempfile.mkdtemp(prefix="r6ref-inputs-")
    monitor, operator_stop = Monitor(), threading.Event()
    monitor.start()
    summaries = {}
    try:
        laws = {}
        for g in gens:                  # each generation its own copy of the inputs: no shared state (his F1)
            d = os.path.join(inputs, "gen%d" % g)
            os.mkdir(d)
            laws[g] = []
            for num, op, m in mutants:
                p = os.path.join(d, num + ".law")
                with open(p, "wb") as f:
                    f.write(m)
                laws[g].append(p)
        for g in gens:                  # one after the other (his R6 remake ruling, 2)
            if g == 2 and completed("%s-gen1" % EXPERIMENT) is None:
                summaries[2] = {"disposition": "NOT STARTED",
                                "reason": "generation 1 has not completed (his R6 remake ruling, 2)"}
                break

            def go(g=g):
                summaries[g] = generation(g, outs[g], mutants, laws[g], "%s-gen%d" % (EXPERIMENT, g), monitor,
                                          operator_stop, sources)
            t = threading.Thread(target=go)
            t.start()
            while t.is_alive():
                try:
                    t.join(0.5)
                except KeyboardInterrupt:
                    operator_stop.set()
            if operator_stop.is_set():
                break
    finally:
        monitor.done.set()
        shutil.rmtree(inputs, ignore_errors=True)
    for g in gens:
        s = summaries.get(g, {"disposition": "NOT ENDED"})
        if s["disposition"] == "COMPLETED":
            print("GEN-R6-REF generation %d (%s): COMPLETED; %d mutants; %s; sha256 %s" % (
                g, s["attempt"], s["rows"], ", ".join("%s %d" % kv for kv in sorted(s["classes"].items())),
                s["sha256"]))
        elif s["disposition"] in ("REFUSED", "NOT STARTED", "NOT ENDED"):
            print("GEN-R6-REF generation %d: %s: %s" % (g, s["disposition"], s.get("reason")))
            continue
        else:
            print("GEN-R6-REF generation %d (%s): %s, %s: %s" % (g, s.get("attempt"), s["disposition"], s.get("cause"),
                                                                 s.get("reason")))
        if "wall_s" in s:
            print("   wall %.1f s; CPU %s s (%s); peak commit %s; peak physical in use %s; commit before %s, after %s; "
                  "workers %d; process-start failures %d; runs past %d s: %d (longest %.1f s); workers may rise: %s  "
                  "[software readings]" % (
                      s["wall_s"], s["cpu_s"], s["cpu_note"], s["peak_commit_bytes"], s["peak_physical_in_use_bytes"],
                      s.get("host_before", {}).get("commit"), s["host_after"]["commit"], s["workers"],
                      s["process_start_failures"], FLAG_S, len(s["runs_over_%d_s" % FLAG_S]), s["max_run_wall_s"],
                      s["workers_may_rise"]))
    done = {g: completed("%s-gen%d" % (EXPERIMENT, g)) for g in (1, 2)}
    if not (done[1] and done[2]):
        left = [str(g) for g in (1, 2) if not done[g]]
        print("GEN-R6-REF: %s not completed; nothing is compared and no record is written"
              % ("generation " + left[0] + " has" if len(left) == 1 else "generations 1 and 2 have"))
        sys.exit(1)
    datas = {}
    for g in (1, 2):
        ident, end = done[g]
        if not os.path.isfile(outs[g]):
            print("GEN-R6-REF: generation %d's file %s is missing; no record is written" % (g, outs[g]))
            sys.exit(1)
        with open(outs[g], "rb") as f:
            datas[g] = f.read()
        if sha(datas[g]) != end.get("output_sha256"):
            print("GEN-R6-REF: generation %d's file is not the one %s completed with; no record is written" % (g, ident))
            sys.exit(1)
    if datas[1] != datas[2]:
        a, b = datas[1].decode("ascii").split("\n"), datas[2].decode("ascii").split("\n")
        diff = [x.split(" ", 1)[0] for x, y in zip(a, b) if x != y]
        print("GEN-R6-REF: the two generations are NOT EQUAL (%d lines differ: %s): the attempt fails verification, "
              "and no record is written (his R6 remake ruling, 4)" % (len(diff) + abs(len(a) - len(b)),
                                                                        " ".join(diff[:10])))
        sys.exit(1)
    with open(record, "xb") as f:
        f.write(datas[1])
    print("GEN-R6-REF: the two generations are BYTE FOR BYTE EQUAL; the record %s is written, sha256 %s"
          % (os.path.relpath(record, ROOT).replace(os.sep, "/"), sha(datas[1])))
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

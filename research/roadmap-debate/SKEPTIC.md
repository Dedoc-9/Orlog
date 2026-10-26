# Debate record: the use-case skeptic's report (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the foundations architect's report. Its
scripts and results are in `work/arch-redteam/` (ignored by git). Its figures are MEASURED once on this host, a
desktop with other sessions running, not a quiet benchmark machine; ranges marked DERIVED are extrapolated.

---

# Ørlǫg checked against four scenarios: measurements, the minimum foundations, and a ranking

**Where this ran:** this Windows 11 host with 16 logical CPUs. CPython 3.14.5 (python.exe, not the WindowsApps alias); clang 22.1.8 (x86_64-pc-windows-msvc); rustc 1.96.1 (x86_64-pc-windows-gnu). Clock: `time.perf_counter` (QueryPerformanceCounter, 0.1 µs resolution). Figures are medians unless stated. Grade: MEASURED here, one session per script. PYTHONHASHSEED=0, PYTHONUTF8=1, `python -B`. No tracked file was changed. TMP and TEMP pointed into `work/arch-redteam/`, so the arbiter's build folders stayed under work/.

## The finding

The work per tick or per edit is small; the way runs are made is what costs. Ticks are cheap: one fall.orl tick costs 28 µs in the reference and 1.3 µs in C. Every run is a new process: starting one costs 12.5 ms for a native program and 107 ms for Python, and `orl.py` costs about 300 ms before it does any work. Every text change is a rebuild: c99 takes 0.33–0.53 s and Rust 0.83–1.3 s per corpus program, and the C build grows faster than linearly with the size of the law. There is no input, so every variation of a run has to be a new law.

The scenarios therefore need a foundation with two speeds: one resident execution, for exploration and live play; the four executions plus the court, for admission. Read literally, that is the owner's anchor ("Exploration should be cheap. Recovery should be reliable. Generation should be explainable. Admission should be earned."). It puts inputs before servers. ADMISSION.md:19 says the relation to the App Studio goal is "NOT claimed" and is the owner's to rule.

## 1. Measurements

**Cost of starting a process** (bench_spawn.py)

| what | median | p10–p90 | n |
|---|---|---|---|
| trivial C exe | 12.5 ms | 11.6–19.0 | 300 |
| trivial Rust exe | 14.4 ms | 13.0–21.2 | 300 |
| `python.exe -I -B -c pass` | 107 ms | 103–213 | 40 |
| `python` through the WindowsApps alias | 328 ms | 268–430 | 15 |
| Python importing orlog.arbiter and orlog.court | 315 ms | 255–361 | 15 |
| `orl.py check` on collatz | 298 ms | 287–795 | 15 |
| first run of a freshly built C exe (later runs: 12.4 ms) | 84 ms | — | 6 |
| pipe round trip to a resident Python | 0.053 ms | 0.047–0.099 | 3000 |
| localhost TCP round trip | 0.214 ms | 0.193–0.338 | 3000 |

**`python -B orl.py run` wall time, in seconds** (bench_cli.py; cold = empty build cache, median of 2; warm = cache filled, median of 5, or 3 for all three backends; the Python backend has no build step)

| program | python warm | c99 cold/warm | rust cold/warm | all three cold/warm |
|---|---|---|---|---|
| aztec | 1.01 | 1.93/0.78 | 2.15/0.81 | 3.00/1.11 |
| chaos | 0.44 | 0.81/0.37 | 1.63/0.40 | 2.77/0.53 |
| collatz | 0.45 | 0.75/0.32 | 2.15/0.32 | 2.44/0.45 |
| fall | 0.43 | 0.76/0.33 | 2.01/0.31 | 2.16/0.48 |
| gcd_certificate | 0.42 | 0.87/0.33 | 1.36/0.30 | 1.96/0.48 |
| leapfrog | 0.64 | 1.25/0.55 | 1.83/0.55 | 2.49/0.84 |
| legal | 0.40 | 0.73/0.32 | 1.44/0.33 | 2.01/0.45 |
| plankton | 0.41 | 0.77/0.38 | 1.27/0.32 | 1.89/0.51 |

**Build against run, cached against not** (bench_phases.py, the library in one process)

| phase | time |
|---|---|
| front end | 0.6–3.7 ms |
| lowering and code generation | under 0.5 ms each |
| c99 build, empty cache (median of 3) | 325–531 ms |
| Rust build, empty cache (median of 3) | 832–1,315 ms |
| build served from the cache | 0.07–0.15 ms |
| first run after a build | c99 53–88 ms, Rust 119–365 ms |
| later runs | Python 124–281 ms, c99 13.5–38 ms, Rust 15–48 ms |
| `arbitrate` with all four executions | 1.6–4.0 s cold, 154–819 ms warm |
| court panel | 0.03–0.07 ms |
| witness artifact | 102–153 ms (`toolchains()` alone takes 130 ms: it starts clang and rustc every time) |

A cold build costs 14–33 times a warm run for c99, and 27–69 times for Rust. The arbiter builds the backends one after another (arbiter.py:170–179), so a cold verdict pays the sum of the builds. The cache never evicts anything (a Rust build is 4.9 MB, a C build 139 KB).

**The reference interpreter's operations per second** (the receipt's `ops` over `Interp.run`'s wall time, in process): 0.73–1.81 M ops/s over the corpus; aztec (mostly Int and Bool list work) 0.55 µs per op; fall (every fixed-point multiply through `Fraction`) 1.36 µs per op. `ops` is a unit-cost count, not work (DOCTRINE §8). Per op in the 1,000-body tick below, each including its SHA-256 per event: C 66 ns, Rust 74 ns, Python backend 333 ns, reference 956 ns.

**The 60 Hz budget, 16.7 ms** (bench_tick.py)

fall.orl with T ticks (22 ops and 8 events per tick, fitted over T from 1 to 40,000):

| execution | per tick | fixed cost per run |
|---|---|---|
| reference (in process) | 28 µs | 0.12 ms |
| Python backend | 9.3 µs | 127 ms |
| c99 | 1.34 µs | 14.9 ms |
| Rust | 1.57 µs | 16.0 ms |

K bodies, per tick:

| K | ops per tick | reference | Python | c99 | Rust |
|---|---|---|---|---|---|
| 100 | 1,502 | 1.51 ms | 0.60 ms | 0.15 ms | 0.17 ms |
| 1,000 | 13,002 | 12.4 ms | 4.3 ms | 0.86 ms | 0.96 ms |
| 10,000 | 130,002 | 124.6 ms | 43.6 ms | 8.7 ms | 8.8 ms |

An input written into the text (the only way to feed one today; each tick a one-tick program with the input as a literal): reference in process 0.93 ms per tick; Python backend 157 ms; c99 with a cold build every tick 430 ms; Rust 983 ms.

**Is 60 Hz reachable today?** One `orl.py` process per run, as shipped: no (its floor of about 0.30 s is 18 times the budget; all four executions take 27–66 times the budget warm, 108–193 times cold). A cached compiled program re-run every tick: 15–16 ms of fixed cost, which fits at the median with 1–2 ms to spare and misses at p90 (starting the process alone takes 19–21 ms), and it cannot take an input without a rebuild (26–59 times the budget). The reference on a one-tick text in one resident process: 0.93 ms, reachable, but every tick is a new law (the seal would identify a tick, not the game). Inside a single run, the compute fits: the reference keeps up to about 1,300 bodies (7.5 times over at 10,000); C and Rust up to about 19,000 bodies (DERIVED).

**Size of the law** (scale.py and scale2.py: a world written as N property clauses)

| N | front end | reference | c99 -O2 build | Rust build |
|---|---|---|---|---|
| 100 | 3.8 ms | 0.14 ms | 0.44 s | 1.05 s |
| 1,000 | 37 ms | 1.1 ms | 4.9–5.4 s | 2.2 s |
| 2,000 | — | — | 27.7 s | — |
| 3,000 | 114 ms | 3.4 ms | 72.4 s (6.6 s at -O1, 0.58 s at -O0) | 9.9 s |
| 10,000 | 407 ms | 11.8 ms | 336 s (1.65 s at -O0) | not run |

The front end grows linearly (about 40 µs per clause). At -O2 the C build grows faster than linearly, because everything lands in one huge `orl_main`: a client has a lever (a 317 KB text cost 336 s of clang time). At -O0 and -O1 the receipts and outputs still equalled the reference's for these worlds.

**Defects that the measurements exposed**
- **Runs that share a work folder report false disagreements** (race.py). Two different `case.orl` programs run 48 times at once in one `--workdir`: 16 agreed, 18 false BACKEND-DISSENT, 3 false REFERENCE-DISSENT, 11 tracebacks. With a folder of their own, all 48 agreed. The cause is in the code: a run's files are named after the program and the backend, and are deleted and read back inside the shared folder (arbiter.py:144–156); `orl.py`'s default folder, build/runs, is shared by every caller (orl.py:51). A false REFERENCE-DISSENT is a false statement about the authority itself. The counts are one session's; the mechanism is in the code.
- **Nothing bounds a whole run** (runaway.py). A legal four-clause program (`For each i from 1 to 1000000000`) was still running after 20 s, when the watchdog killed it; one iteration costs 2.80 µs (measured over 10^5), so the reference alone would take about 47 minutes (DERIVED). There is no timeout on a backend's subprocess (arbiter.py:152) and no budget for a run in the reference (interp.py:106–113); fuel is per While loop only (interp.py:205–214). It has happened before: one case in the differential run counted 270,000,669 ops (evidence/difftwin-seed2-timeout.txt).
- **Editing a note rebuilds both compiled backends** (undo.py). The law seal stayed the same, but c99 and Rust both rebuilt (1.71 s), because the text seal is compiled into every generated program (gen_c.py:309–310, gen_rs.py:313, gen_py.py:220). Undo is a cache hit: returning to the earlier text took 85 ms for the reference plus c99 plus Rust, against 1.90 s for the edit itself.
- **There is no reference-only run mode.** `--backends reference` raises ValueError (arbiter.py:94), and an empty value falls back to all three backends (orl.py:50).

## 2. The four scenarios

**S1: an artist makes 200 property changes an hour, each previewed in under a second, each undoable.**
- Today: a version is a text with three seals (front.py, `Compiled`); `stamp` and a `Sealed:` line mark a version, and SEAL-MISMATCH refuses a sealed text whose law has changed. The build cache is addressed by content (arbiter.py:112, 122), so undo is a cache hit (85 ms). The trace records every assignment as a typed event (interp.py:39–45, 88–93): with the symbol table, already a stream of state changes a view could read. Missing: a reference-only mode, a history, and build identity by the law rather than by the text.
- Smallest missing piece: a reference-only preview, and an append-only list of text seals with the texts they name. The CLI's floor of about 0.3 s already meets the one-second target (3.4 ms in process), so S1 needs no server.
- Kill assumption: that a world property belongs in the sealed law. If it does, every change mints a new law; compiled previews always rebuild (1.6–4.0 s for all four executions on a corpus program, 4.9–5.4 s for c99 alone at 1,000 clauses); a preview could only mean "the reference ran", not "verified". It also assumes worlds stay small: a reference-only preview stays under a second up to about 25,000 clauses (DERIVED).
- Cheap experiment: script 200 edits of one property, with an undo every fifth edit, at the world's real size; it passes if every preview takes under a second and every undo reproduces its earlier receipt byte for byte.

**S2: a game simulation at 60 ticks a second with player inputs, replayed byte-identically.**
- Today: determinism by construction (Q31.32 fixed point and canonical floats, held by 20,015 vectors per runtime and by four-way receipts on chaos, fall and leapfrog); an event hash chain (interp.py:88–93), with any disagreement localized to its first divergent event (arbiter.py:247–277); procedures that could serve as the tick body (leapfrog.orl §9). No input at all: the runtimes read no clock, environment or randomness (RUNTIME-SPEC.md:25); a program's argv is `OUTPUT RECEIPT [TRACE]` (rt_py.py:74–76); a run goes from main to finish (gen_c.py:308–313); "capability inputs" is a declared next rung (DOCTRINE.md:427).
- Smallest missing piece: an input stream all four executions read identically, each read a chain event, the stream's sha256 in the receipt. Reading the whole log at the start would already give byte-identical replay of a recorded match, checked four ways. Live play would add a resident tick loop in one compiled backend, with the reference replaying offline.
- Kill assumption: that the reference can stand behind a live game (about 1,300 simple bodies per tick; beyond that it can only audit replays slower than real time). A process per tick (15–16 ms fixed) and inputs written into the text (430–983 ms per tick) are both dead. Identity across hosts is NOT_MEASURED.
- Cheap experiment: the tick probe, run here. Next: compare the corpus receipts on a second host or toolchain.

**S3: an external client or AI agent submits an edit over a socket and gets a verdict with evidence.**
- Today: every part of the verdict is already a library call (`compile_bytes`: refusal code and line; `Arbiter.arbitrate`: agreement, dissent kind, first divergent event, arbiter.py:160–223; `court.panel`: each claim's standing, court.py:167; `witness_artifact` and `court_artifact`), exposed by the command line as `run --witness` and `court --json` (orl.py:49–98). The front end has been hardened against hostile text (60,000 door fuzz cases, 20,221 mutants, red-team findings E1–E26). Missing: everything listed under the race and runaway defects.
- Smallest missing piece: a resident worker reading JSON lines on stdin (the prototype `worker_proto.py` uses library calls only), with a work folder per request, a bound on each run, and the base text seal in every request, refused when the base has moved. The reply can be today's witness and court artifacts.
- Kill assumption: that a verdict with evidence is worth its latency to the client. A four-way verdict on an edited law takes a median of 2.7 s through the worker. A claim checked by the program's own computation can never be GROUNDED (R2). If clients act only on the refusal code, the product is the 3.4 ms reference verdict, and the four-way verdict belongs to admission.
- Cheap experiment: the server-shell probe (race and runaway), run here: killed. Next: an agent makes 50 edits through the worker; read its transcript to see whether any field beyond the refusal code changed its next edit.

**S4: a test harness drives thousands of cases over a socket.**
- Today: the repository already runs thousands of cases without a socket: tests/diff_twin.py uses 8 threads and batches of 40 texts per worker subprocess, with timeouts of 60 s per batch and 15 s per text (diff_twin.py:301–339), and it ran 20,221 texts. Every case is a program, so a compiled backend builds once per case.
- Smallest missing piece: nothing in the transport. Cases should be inputs to one law, so one build serves all; a deterministic budget would turn a runaway case into a refusal with a code (today it is a timeout whose firing depends on the machine).
- Kill assumption: that cases are programs. Per case through the worker: c99 581 ms for a new program, 38 ms for the same program cached; all four executions 2.69 s new, 278 ms cached. At 2.69 s each, 1,000 four-way cases take about 45 minutes on one thread.
- Cheap experiment: cases.py, run here: reference only in a resident worker, 3.41 ms per case; one `orl.py` process per case, 531 ms (156 times slower).

## 3. Next steps, ranked by foundational value

| # | step | serves | cost |
|---|---|---|---|
| 1 | A ruling by the owner, no code: is Ørlǫg this foundation at all (ADMISSION.md disclaims it)? Is a world property part of the law, or of its inputs, or a data section sealed apart from it? | all | none |
| 2 | Inputs as data: read identically by all four executions, each read a chain event, sealed apart from the law; the input's sha256 and a deterministic ops budget in one new receipt version (deterministic for free, because `ops` is already in the receipt core the arbiter compares). Hold the twin's paper round first. | S2 (blocks it), S1, S3, S4 | M–L |
| 3 | Isolate runs: run files named per arbitration, not per program; publish into the cache atomically; a wall-clock backstop reported as its own outcome, never as a dissent. | S3, S4 | S |
| 4 | Two speeds: a reference-only mode for previews; all four executions and the court only at admission. | S1, S3 | S |
| 5 | A resident worker speaking JSON lines on stdin and stdout over the library (3.4 ms per case against 531 ms). | S3, S4, S1 | S |
| 6 | Build identity by the law: pass the text seal in at run time instead of compiling it in. | S1, S3 | S |
| 7 | Whole-text history keyed by text seal, plus base binding on submitted edits: undo exact by construction and a cache hit. | S1, S3 | S |
| 8 | The verdict reply: today's artifacts plus a clause-level diff of the law, the toolchain probe run once per worker. | S3 | S |
| 9 | A tick loop in the generated programs: a declared procedure run once per input record, resident, a chain head per tick. Only after step 2. | S2 | M |
| 10 | A build policy: c99 and Rust built in parallel; an optimization level decided for large laws. | admission, S3 | S |
| 11 | Measure identity across hosts and toolchains. | S2 | S per host |
| 12 | A socket adapter over the worker, only once a remote client exists. | S3, S4 | S |

**Wasted if built early.** Step 12 before steps 3 and 5 (a socket in front of today's arbiter delivers false dissents and unbounded runs). Step 9 before step 2 (a tick loop with no input is only a benchmark). Parallel builds before steps 2 and 4 (they would speed up a rebuild that inputs and reference-only previews take off the hot path). Left off deliberately: an ECS or transaction engine, an incremental compiler or build daemon, an edit language with exact inverses, a UX editor before steps 4 and 5, an MCP or plugin layer, networked play before step 11.

**Where the "architecture first" ranking goes wrong.** Server and API first: the transport costs 0.05–0.21 ms, while a request costs 300 ms of Python start and imports and 0.3–1.3 s per rebuild; the win comes from being resident, not from having a socket. Verifying every edit fully: 1.6–4.0 s per edit, and the C build grows faster than linearly with the law (336 s at 10,000 clauses); verification belongs to admission. An ECS or transaction model first: whole texts plus the content-addressed cache already make undo exact (85 ms); an edit language would bring back the exact-inverse problem Verðandi's 0254 had to solve. Treating inputs as a later rung: their absence is why a tweak becomes a new law, why a note edit rebuilds, why each test case is a build, and why S2 cannot start. Sockets for testing: diff_twin.py already ran 20,221 cases with no socket.

## 4. The three cheapest kill-experiments (all run here)

1. **Server-shell probe** (race.py and runaway.py, about 3 minutes). Kills: putting a socket in front of today's arbiter. Fails if any false dissent, traceback or unbounded run appears. Result: **killed.**
2. **Tick probe** (bench_tick.py, about 5 minutes). Kills: a process per tick; inputs written into the text; the reference as live authority above about 1,300 bodies. Fails if a tick takes more than 16.7 ms of wall time. Result: the way runs are made is killed for 60 Hz; the compute survives (C takes 0.86 ms per 1,000-body tick).
3. **Law-size build probe** (scale.py; about 1 minute up to 1,000 clauses, about 8 minutes up to 3,000). Kills: recompiling the whole world in C on every edit. Fails if a cold build takes more than 1 s at the world's target size. Result: **killed at -O2** beyond a few hundred clauses; -O0 survives (1.65 s at 10,000 clauses).

The cheapest one not yet run needs a second machine: compare the corpus receipts on another host or toolchain. A single differing byte kills networked replay as specified.

## 5. Limits of these results

Not shown: other hosts; a quiet machine; why a fresh executable's first run is slow (84 ms against 12.4 ms; NOT_MEASURED); race counts beyond this one session; other workloads (the unit cost of an op differs by type). DERIVED, not measured: the 47-minute runaway, the 1,300- and 19,000-body ceilings, the 25,000-clause preview ceiling. Built is not adopted: `worker_proto.py` is a measuring instrument kept in work/, not a proposed implementation. What would weaken a claim: rerunning on a quiet host; a native process start under 2 ms would reopen a process per tick for small worlds, though the argument about inputs would still stand. Disk: `work/arch-redteam/runs/` holds about 0.55 GB of builds and can be deleted.

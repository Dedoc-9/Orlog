# Debate record: the proponent's design for the speed debate, round 1 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the adversary's prosecution and the
prior-art survey. Its probes ran against a checked snapshot of f16dc26 and are in `work/speed-probe/` (ignored by
git); its MEASURED lines are this host's.

---

# The speed reconciler and the view tier: the proponent, round 1 (2026-10-26)

A subagent's report for the judge of the debate set out in `research/speed/PROPOSAL.md`. It is model output, not the
owner's words, and it decides nothing. Nothing here is built into the language or admitted: every probe is scratch
apparatus under `work/speed-probe/` (ignored by git), and no tracked file was changed.

**Where it ran.** Every probe ran on this host against a snapshot of the last commit, `f16dc26` (tree `8be71851`),
extracted with `git archive HEAD` into `work/speed-probe/tree` and checked file by file: all 719 files hash to the
commit's blobs (`work/speed-probe/SNAPSHOT.txt`). Nothing ran against the working copy, which another session was
editing. A first attempt at this task had run its probes against that working copy; its outputs are kept as history in
`work/speed-probe/attempt1-outputs/`, and none of its numbers is used here. Python 3.14.5, clang 22.1.8 and rustc
1.96.1 (the toolchains the skeptic's record names), `PYTHONHASHSEED=0`, `PYTHONUTF8=1`, `python -B`. The clock is
`time.perf_counter_ns` (QueryPerformanceCounter): declared resolution 0.1 µs, smallest positive step observed 100 ns,
in every probe that reads it.

**Grades.** MEASURED: a run here shows it. ESTABLISHED: read from the code or settled. DECLARED: designed, not built.
DERIVED: arithmetic on measured inputs. OBSERVED, SPECULATIVE, NOT_MEASURED as the lineage uses them. Every timing is a
software timing of this host, one corpus, one sitting, with the host's memory load at 95–98% throughout
(`work/speed-probe/run_all.log`, recorded beside each probe and read by nothing). No latency, frame rate,
input-to-photon figure or feel is claimed or implied anywhere. Figures from other apparatus (Verðandi's records, the
skeptic's) are compared in orders of magnitude only (Verðandi G4).

---

## 0. The four answers, short

1. **Two speeds, joined by a tick receipt.** Play is the law's own compiled C program, resident, reading the input log
   as a stream. The reference replays the same log behind it. Every execution writes one line per tick boundary, and
   that line is the receipt's every field at that boundary plus a digest of the state: events, ops, output bytes,
   trace head, output chain, claims, state. A reconciler compares lines; the first line that differs names the tick and
   the field, and a windowed re-run from the nearest snapshot names the event. MEASURED (P4): the trace head alone
   names one of five planted defect classes at its tick; R5's head and output chain name two; the full line names all
   five. So the sheet is missing the counters, the claims and the state from its per-tick commitment, plus three
   smaller edges (§1.6). The reference's record stands on a dissent, as the arbiter's does today. Admission lags play by
   the log's durability group while the reference is faster than real time (fall: about 450 times), and, when it is
   not, segments replayed in parallel from play's snapshots, each snapshot checked against the reference's own state
   before it is trusted, multiplied the reference's rate by 5.9 at 16 lanes (MEASURED, P11).
2. **No language swap.** On this host the compiled tick is 93–95% commitment (SHA-256 per event) and 5–7% arithmetic
   (MEASURED, P1 and P7, three laws). A faster language could only touch the arithmetic. The lever is the
   commitment's form: one SHA-256 per tick over the tick's event encodings cut the commitment to 0.29–0.30 of the
   per-event chain's cost on ticks of 301 and 3,001 events, and still named every planted defect at its tick
   (MEASURED, P7). It must be chosen
   before RUN-1 freezes `orlog-trace-1`, or never. A GPU or SIMD backend has a place only for many independent worlds
   (previews, sweeps), never for one world faster, and only as a fifth execution held to the reference, never the
   authority: integer-only, 64-bit values carried as two 32-bit words (in a guarded model, exact on all 5,620 vectors of
   the eight operations tried, about 108 32-bit steps per Fix multiply: MEASURED, P6), SHA-256 already 32-bit, no
   floats.
3. **The view reads; it never writes.** It reads each tick's output and, after SNAP-1, the snapshot, through a one-way
   pipe from play, and it can reach the law only as a typed input record of a later tick, through the door and the log.
   The fence has a witness that already exists in this design: any write that bypasses the log is a state change
   without an event, and the state field names its tick (P4's "silent" plant is exactly that). Whatever a player is
   allowed to see, if it decides play, is computed in the law in Fix and drawn by the view, never recomputed in floats:
   an order-2 spherical-harmonic evaluation costs 35 counted operations, about 1.2 µs in C and 51 µs in the reference,
   and stays within 1.5 units of 2^-32 of binary64 on the same inputs (MEASURED, P5).
4. **HEADROOM-0, written Verðandi's way.** The first attempt's draft (`work/speed-probe/headroom0-draft.json`, sha256
   `5e01f69d…`, written before any pilot number and unchanged since) is kept, with five amendments proposed before any
   reading exists (§4). One observable per tick, through the resident pipe; a transport-only cell in the same run as the
   comparator and the VOID gate; 1,000 samples per cell after 10 warm-up ticks, so p99 is the 11th largest, with the 12
   largest recorded; PASS iff p99 ≤ 950‰ of the declared budget; a confirmation run; the clock's step and the host's
   state recorded; never a frame rate. A pilot here tested the instrument only: every line equal to the reference's for
   1,010 ticks, p99 of 41, 39 and 47 µs for the transport alone and the two commitments (P9), not a reading.

---

## 1. Two speeds

### 1.1 Three tiers over one log

The skeptic's "two speeds" (`research/roadmap-debate/SKEPTIC.md`): one resident execution for play, the four
executions and the court for admission. This design keeps both and adds a middle one, so that admission does not wait
for a session to end.

| tier | what runs | reads | writes per tick | its standing |
|---|---|---|---|---|
| play | the law's C program (the arbiter's c99 build), resident in one process, its tick block reading the log as a stream | the door's records, after they are in the log | the tick line (to a pipe); the tick's output lines (to the view) | testimony: never admitted on its own |
| watch | the reference interpreter replaying the log behind play (one process, or segments: §1.5) | the durable log; play's snapshots, each checked before use | the tick line | the session's record, by declaration (the de Bruijn criterion, `src/orlog/arbiter.py`) |
| admission | all four executions over the closed log, the arbiter, the court | the closed log | receipt 1 and the tick lines, four ways | admitted, or a dissent with its tick |

Why C for play: on fall.orl the C tick cost 1.30 µs and the Rust tick 1.63 µs (MEASURED, P1), and c99 builds in about
half Rust's time (the skeptic's record). Either would do; the choice is a measurement on this host, not a principle.
The input path is write-ahead: the door appends a record to the log and only then hands the same bytes to play, so play
never plays an input the log lacks (DECLARED). Play never waits on the device: durability is a group commit beside it,
and admission reads only what is durable (§1.5).

### 1.2 What every execution commits per tick: the tick receipt

**Definition (DECLARED; prototyped in the probes).** `orlog-ticks 0`: a header naming the law seal and R10's port
signature, then one line per tick boundary t = 0 (after the prefix), 1, 2, …:

```
<t> <events> <ops> <output-bytes> <trace-head> <output-chain> <claims> <state>
```

- `events`, `ops`, `output-bytes`: the receipt's counters at the boundary, cumulative.
- `trace-head`: the chain's head at the boundary (R5's head at the next `'T'` is a function of it and t).
- `output-chain`: R5's out_t.
- `claims`: `-` when the law declares no claim; otherwise the SHA-256 of the claim lines the receipt would write at
  that boundary (`claim <id> <clause> <evaluations> <trues> <cost> <ref-clause> <ref-cost>`).
- `state`: the SHA-256 of every persistent variable (D6: the top-level variables before the tick block) in id order,
  each as u32 id and its value encoding (RUNTIME-SPEC §5), and of every clause-cost accumulator: the variable section
  of a future SNAP-1 snapshot. Where the state is too large to digest every tick, the host may compute it every k
  ticks and write `-` between (§7, weakness 1).

ASCII, LF, lowercase hex, decimal counters: the trace's conventions. Each line is what the receipt would say if the run
ended at that boundary, plus the state; the final receipt can be checked against the last line.

**Why every field: the plants (MEASURED, P4).** The claim-bearing fall (`examples/fall.orl` with one claim in the
tick, a probe law; T = 400). The fast execution is its C program writing the full line; the reference writes the same
line. Five defects are planted at the start of tick 237, each a textual change to the generated C only. A reading
"catches" a defect when the first line whose chosen fields differ is tick 237's.

| defect planted at tick 237 | head alone | R5 (head, output chain) | + counters | + claims | full line | final receipt differs |
|---|---|---|---|---|---|---|
| none (control) | — | — | — | — | — | no |
| `vx` one raw unit more, no event | 237 | 237 | 237 | 237 | 237 | yes |
| one counted operation more | — | — | 237 | 237 | 237 | yes |
| one output byte, hashed, no `'S'` event | — | 237 | 237 | 237 | 237 | yes |
| the claim reports one unit of cost more | — | — | — | 237 | 237 | yes |
| `landed_at` one more, no event (silent) | — | — | — | — | 237 | yes |

Each field catches exactly the class the others miss. The trace head commits to events, and four of these defects
change none: an operation counted, an output byte written past its event, a cost added (a `'C'` event carries the
claim id and the result, not the cost: RUNTIME-SPEC §5), a state change nothing re-assigns. R5's output chain catches
the second; nothing on the sheet catches the other three. The silent one stands for memory written where it should
not be, the class a C program's memory errors fall into: `landed_at` is read every tick after the landing at tick 91,
always nonzero, so no event differs until the final Say, after the last tick. Without the state field the reconciler
could not name any tick for it. Localization agreed: a window kept for tick 237 alone found the first divergent event
for the value defect (event 1,871, §12.4's `'A'` on `vx`) and, for the other four, "every event of the tick agrees",
which is exactly when the line's other fields must say what parted.

OBSERVED, not re-run by me: the adversary's preliminary scratch output (`work/speed-adv/chain_blind.txt`) describes
the same hole from the other side. With R9's per-tick budget, counters that part at tick 1 show in the heads only at
the budget's refusal, many ticks later. The counters field closes it, since a budget is read from ops.

**What it costs (MEASURED, P1, P3, P7).** fall.orl, per tick, the slope of the medians between loop bounds of 4,000 and
40,000 (process runs, n = 30 and 20 per cell, cells in a seeded shuffled order per round):

| execution | per tick | bytes a tick |
|---|---|---|
| C, as the arbiter builds it (the chain, no line) | 1.30 µs | — |
| C with the full tick line and the `'T'` event | 2.67 µs | 218 |
| C with the whole trace written (argv[3]) | 4.42 µs | 815 |
| C with SHA-256's compression a no-op (timing only) | 0.075 µs | — |
| Rust, as built / with the whole trace | 1.63 / 3.51 µs | — / 815 |
| reference in process, plain / with the full line and `'T'` | 27.8 / 36.8 µs | — / 218 |

The full line adds 1.4 µs a tick in C and 9 µs in the reference on fall; at 1,000 bodies it added 64 µs to an
830 µs C tick (P7, 7.7%), most of it the state digest over 16 KB (about 250 compressions at about 0.16 µs each on this
host; DERIVED from P7's 1,000-body chain, 784 µs for about 5,000 compressions a tick). A whole trace in play would
cost more than the line (4.4 against 2.7 µs on fall) and grows with the events: 815 bytes a tick on fall, and the
trace of a 40,000-tick fall run is 32.6 MB against 8.7 MB of lines. The line is constant in the events and linear in
the state. (The slope between 400 and 4,000 ticks is not read: its 6.5 ms of difference is the size of the process
start's own p10–p90 spread.)

### 1.3 The reconciler

1. Compare the two executions' lines in order. The first line that differs names tick t* and the fields that differ;
   one side with no line names the tick where it stopped (a refusal, or a host's stop).
2. Localize inside t*: run both again from the nearest snapshot at or before t* − 1, keeping the trace for t* only,
   and compare event lines (the arbiter's `localize`, unchanged in kind). If every event agrees, the line's fields
   say what parted: counters, claims, output or state "outside the event chain".
3. Write the dissent: kind, t*, fields, event (if any), and which record stands (§1.4).

MEASURED (P4, fall at T = 40,000 with `x` one raw unit more at tick 39,999; one run of each step, software timings):
comparing 40,000 lines took 1.6 ms and named tick 39,999 (fields head and state); the reference resumed from its own
snapshot at tick 39,000 with a one-tick window took 30 ms, against 1,219 ms replaying from tick 1, and found event
319,732 (§12.5, `x`); the C program again from tick 1 with its window took 120 ms (it has no restore). Today's way, both
whole traces: 196 ms for C, 1,357 ms for the reference, 41 ms to compare 319,742 lines.

### 1.4 When play and the reference part

The owner's request already says what a mismatch is owed: *"can handle and replace safely byte mismatches(noting
so)"* (`ADMISSION.md`). A session applies it per tick (DECLARED):

- **Whose record stands:** the reference's replay of the logged inputs, by declaration, never by a vote; as the
  arbiter does now (`src/orlog/arbiter.py`: "the reference's output is kept, because the reference is the DECLARED
  authority"). The log stands as data (R6 a). Play's lines from t* on are kept as evidence and never admitted.
- **The dissent's kind:** BACKEND-DISSENT when play alone parts; REFERENCE-DISSENT when every compiled execution agrees
  against the reference (the reference still stands, and the record says loudly that its authority is declared);
  STOPPED-BY-HOST when a host's bound fired. The kinds and their meanings are the arbiter's, carried to a tick.
- **What happens to play:** a policy, the owner's to rule. (a) Stop. (b) Resynchronise: restore play from the
  reference's snapshot at t* − 1, replay the logged inputs to the present through the fast path, go on; the player
  sees a correction. (c) Go on, unadmitted past t* − 1. My recommendation: (b) for exploration and previews; for any
  competitive use, nothing after t* − 1 counts as a result unless the owner rules otherwise, because every input after
  t* answered a picture the law did not produce.
- **The court** reads the reference's run, as it would read a batch run; R6 a already keeps every claim of a run with
  an input log from GROUNDED, outside its licence.

### 1.5 How far admission lags behind play

Definitions (DECLARED): the *watermark* is the last tick whose line the reference has written and play's equals; the
*lag* is play's tick minus the watermark. With tick period P, the reference's cost per tick c_ref on this host, a
durability group of g records, and W lanes of segments of L ticks:

- **c_ref < P (the reference faster than real time):** the lag is about one durability group, g ticks, plus the
  g·c_ref of software time its replay takes: a constant. fall.orl: c_ref = 36.8 µs with the full line (MEASURED, P3),
  27,170 ticks a second of software time, about 450 times 60 ticks a second (DERIVED). The durability group
  (MEASURED, P10, a 64-byte record, 1,000 per cell): an append without fsync took 4.7 µs at p50 and 45 µs at p99;
  with an fsync every record, 317 µs at p50, 1.0 ms at p99 and 3.0 ms at most;
  with one fsync per 16 records, 5.2 µs at p50, 502 µs at p99 and 34 µs on average. So play never waits on the device:
  the door group-commits beside it, and the watermark trails by about one group (16 ticks: 0.27 s at 60 ticks a
  second, DERIVED). A software timing of this host's file system; it shows an order of magnitude, never a guarantee of
  durability (Verðandi G16).
- **c_ref ≥ P:** a single reference falls behind by (c_ref/P − 1) ticks per tick played. The 1,000-body law: c_ref =
  12.5 ms (MEASURED, P3b: 10,002 counted operations a tick at 1.25 µs each; 100 bodies, 1.23 ms), so c_ref/P is 0.75
  at 1/60 s and 1.50 at 1/120 s: at the faster period one reference loses half a tick per tick played (DERIVED).
- **Segments (needs SNAP-1):** play writes a snapshot every L ticks; lane j replays segment j from play's snapshot;
  before a segment's start is trusted, the previous segment's own end state (the reference's) must equal it, field by
  field, so every state the reference starts from is one it computed, by induction from tick 0. The lag is then about
  L·c_ref/P ticks and the rate scales with the lanes. MEASURED (P11, fall at T = 200,000, 16 segments, the reference
  with the full line, medians of 3 rounds in a seeded shuffled order):

| admission | wall time | ticks a second of software time | against sequential |
|---|---|---|---|
| sequential reference | 7,251 ms | 27,582 | 1.00 |
| 16 segments in 1 lane | 7,300 ms | 27,396 | 0.99 |
| 2 lanes | 3,740 ms | 53,473 | 1.94 |
| 4 lanes | 2,250 ms | 88,899 | 3.22 |
| 8 lanes | 1,516 ms | 131,968 | 4.78 |
| 16 lanes | 1,236 ms | 161,795 | 5.87 |

Every segment's lines equalled play's, play's equalled the sequential reference's, every boundary reproduced, and the
final state was the sequential reference's. Planted: a value defect at tick 62,623 was named at 62,623 (and the next
boundary, 75,000, broke); a snapshot forged at 100,000 (`landed_at` one more in the snapshot only, play's own run
correct) broke boundary 100,000, before any line it fed was trusted. The rate stops scaling past eight lanes (4.8 at 8,
5.9 at 16), as Verðandi's threaded pass did (G2); the cause here is NOT_MEASURED. For the 1,000-body law at 1/120 s,
two lanes would keep pace, and 16 lanes at fall's 5.9 would bring the reference to about 2.1 ms a tick, a quarter of
the period (DERIVED; the speedup on that law is NOT_MEASURED).

### 1.6 What the RUN-1 sheet needs before it is built

| | change | why | grade | falsifier |
|---|---|---|---|---|
| **must** | add the tick receipt (§1.2), written by every execution given a path: one more argument in R11's revision of `orl_init` | R5's head and output chain name 2 of 5 planted classes at their tick; the line names 5 | MEASURED (P4) | a defect that changes the receipt, or a later tick's state, and no field of the line names its tick |
| **must** | define the output chain's start and edges: link 0 is the output before the first `'T'`; out before it fixed (the probes used 32 zero bytes, a convention); a refused tick's partial output is the last link | R5 leaves out_0 and the prefix's output undefined | ESTABLISHED (read from R5) | two executions equal in every output byte and different in output chain |
| **must** | the log readable as a stream, with an explicit end record; D3's "a run completes when its log ends" to mean that record, never the end of a file | in live play the log is still being written: a replay that reads to the end of the file would complete early with a receipt that looks final | ESTABLISHED (read from D3, R5) | a truncated log that yields COMPLETED (a plant) |
| **must** | say what `ticks <n>` counts at a refusal (proposed: ticks begun; a refused tick writes no tick line, the receipt is its record) | the reconciler compares line counts | ESTABLISHED | two executions that refuse at one operation and disagree on `ticks` |
| should | a port may declare a range the door enforces | if R4 a is ruled, anyone whose input value overflows the law's checked arithmetic ends the session for every player; a range moves that refusal from the law to the door, which refuses the record and lets the session go on | ESTABLISHED (RUNTIME-SPEC §2's checked arithmetic, R4 a as recommended); remedy DECLARED | an out-of-range value that reaches the law |
| should | SNAP-1 next after RUN-1 | cheap localization (30 ms against 1,219 ms) and segment admission both need restore | MEASURED (P4, P11) | a restored run whose later lines differ from the sequential run's (P0 checks this for the probe's snapshot) |
| **option, now or never** | the stream head in `orlog-trace-1` (§2.2) | the commitment is 93–95% of the compiled tick; the stream cuts it to 0.29 on list-heavy ticks | MEASURED (P7) | a defect class the per-event chain names at its tick and the stream head does not |

R8 b (floats deferred) is untouched by speed and agrees with §2.4. D4 (OUTPUT-TOO-LONG per tick at 2^30 bytes) is a
refusal bound, not a view budget: a view needs its own bound on what it reads per tick (§3.1).

---

## 2. A language swap

### 2.1 The law does not need a faster language

What a compiled tick is made of, measured by making SHA-256's compression a no-op (outputs unchanged, heads
meaningless; timing only) (MEASURED, P1 and P7):

| law | events a tick | C as built | C, compression a no-op | the commitment's share |
|---|---|---|---|---|
| fall.orl | 8 | 1.30–1.34 µs | 0.08–0.10 µs | 93–94% |
| 100 bodies | 301 | 83.5 µs | 4.2 µs | 95% |
| 1,000 bodies | 3,001 | 830 µs | 46 µs | 94% |

A faster language for the law's arithmetic could remove at most the last column's complement, 5–7% of the tick. Rust
is no faster than C here (1.63 against 1.30 µs on fall). The Python backend (the skeptic's record: 9.3 µs a fall tick)
and the reference (27.8 µs, P3) are slower by about an order of magnitude, and neither is on play's path. The
reference is the bottleneck of admission, not of play; three ways to speed it, measured or not:

- **Its carrier.** x_mul through an integer form of the same rule (floor division and a half-even test; all 992 x_mul
  vectors agree) and its operator table built once: 18.9 µs a fall tick against 27.8 (MEASURED, P3), 1.47 times,
  without changing what it computes, but changing the code whose smallness is its authority.
- **A rewrite in another language:** NOT_MEASURED, and the wrong trade: it gives up the de Bruijn criterion for a
  constant factor.
- **Segments:** 5.9 times at 16 lanes with no change to the definition (P11). This is the one I propose.

### 2.2 The commitment is the cost, and its form is the lever

The per-event chain hashes each event with the previous head, so every event costs at least one compression, and an
`'E'` item event two (21 bytes of payload, 62 with the head and header, 71 with padding). The stream head commits the
same bytes once per tick: P_t = SHA-256(P_{t−1} ‖ every event's kind, clause, length and payload in tick t), P_0 = R5's
head0. MEASURED (P7, the full tick line written in both cells, n = 25/15 and 21/15 process runs):

| law | chain + line | stream + line | commitment beyond the no-op, stream ÷ chain |
|---|---|---|---|
| fall.orl (8 events a tick) | 2.48 µs | 1.85 µs | 0.73 |
| 100 bodies (301) | 88.2 µs | 29.3 µs | 0.30 |
| 1,000 bodies (3,001) | 894 µs | 289 µs | 0.29 |

With the stream head every plant of P4 (value, ops, out, claim cost, silent) was still named at tick 237, and the
control at none (MEASURED, P7). What it costs: v0 laws keep the per-event chain (COMPAT-0), so each runtime carries
both; a v1 trace line loses its per-event head, and the `'T'` line carries P_{t−1} instead; a trace is
self-authenticating per tick, not per event. What it buys, in orders of magnitude against Verðandi's records: a
1,000-body tick moves from about 10^-3 s to a few 10^-4 s, against a software frame of about 1.5·10^-2 s (G8) and a
refresh of about 1.3·10^-2 s (G10) on another apparatus. Under HEADROOM-0's budget at the second period that
amendment 3 proposes (1/120 s, bound 792 µs, §4.2) that is the difference between failing and passing at the median,
by this host's process slopes (DERIVED; HEADROOM-0 would read it at p99, resident). My recommendation: adopt it in
`orlog-trace-1`, since after receipt 1 is frozen it would cost a trace-2.

Hardware SHA-256 would be cheaper still, but RUNTIME-SPEC §1 forbids every compiler extension and intrinsic in C, and
Rust's standard library has none; it would be a change to the runtime contract (NOT_MEASURED).

### 2.3 GPU and SIMD: many worlds, never one world faster

One world's tick is a sequence: events are ordered and the chain (or stream) is sequential. A reduction reordered moves
a refusal and a Fix product: order is semantics (T5, T10). So a GPU or SIMD backend has a place only across worlds: a
preview of one law over many candidate logs, a sweep over a read-once port (R1 b), a test harness's thousands of cases
as inputs to one law (the skeptic's S4). RUN-1 makes this possible, since a sweep then shares one law and one build.
On a CPU the same idea is SIMD across worlds: each lane one world, its operations in its own order, its chain one lane
of a multi-buffer SHA-256 (DECLARED; nothing of it is built or measured here).

The baseline it must beat (MEASURED, P8): 64 worlds of fall.orl at 40,000 ticks each, as processes of the plain C
program, every receipt the reference's. One at a time, 4.66 s (5.5·10^5 world-ticks a second); 16 at once, 0.68 s
(3.8·10^6 world-ticks a second, 6.8 times); medians of 3 batches, minimum to maximum within 12% of the median at
every level. Every world-tick there includes its full per-event chain. A GPU backend earns a place only if a court
shows it beating that by a declared margin, on the same host, with its receipts equal to the reference's (DECLARED).

### 2.4 What an exact GPU backend would need

- **Integer only.** Int, Fix and Bool. No Float: flush-to-zero is unchecked even on CPUs (DOCTRINE T5), R8 b already
  defers float ports, and, recalled from outside sources and not checked here, WGSL has no 64-bit float type and many
  devices run binary64 at a fraction of their 32-bit rate.
- **64 bits as two 32-bit words, products from 16-bit halves**, since a shader language may have no 64-bit integer and
  its 32-bit multiply may keep only the low word (recalled, not checked here). MEASURED (P6, a Python model with every
  primitive guarded to [0, 2^32) and counted; no device ran): all 5,620 vectors of i_add, i_sub, i_mul, x_add, x_sub,
  x_neg, x_abs and x_mul agree. A Fix multiply took 108 primitives
  on average (16 of them 16-bit multiplies), an Int multiply 98, an add or a subtraction 7: two orders of magnitude
  more steps than one native 64-bit multiply. Three mistakes planted in the multiply (a dropped carry, ties rounded
  away from zero, 2^63 admitted) were caught by 28, 18 and 21 vectors. Division, square root and printing were not
  tried.
- **SHA-256 is already 32-bit**: the commitment maps to a GPU with no emulation, one chain per world (DECLARED).
- **A refusal per lane**, masked, at the same operation as the reference; lists bounded far below 2^24 items, texts
  excluded (DECLARED).
- **Its standing:** a fifth execution under the arbiter, held byte for byte to the reference's receipt 1, never the
  authority. The arbiter's word stands: integrity is not truth, and a fifth agreeing execution measures what it does
  not share with the others (T11).

---

## 3. The view tier's contract

### 3.1 What it reads

- Each tick's output lines (the `'S'` payloads of tick t), from play's output pipe, tagged with t.
- The tick line, so that it can show whether a tick is admitted yet (the watermark).
- After SNAP-1, snapshot bytes at the ticks it asks for: typed state, no decimal text to parse. Printing every Fix value
  exactly is not cheap (RUNTIME-SPEC §3: up to 32 fraction digits), so a view that draws many bodies should read
  snapshots, not Say lines.
- It may interpolate between two ticks' states for display, predict for display, and use floats, shaders, spherical
  harmonics, anything; its picture is judged by a person and hashed by nothing (Verðandi's `art/README.md`).
- It needs its own per-tick budget for what it reads; D4's 2^30 bytes a tick is a refusal bound of the law, not one.

### 3.2 How it is fenced, and how the fence is witnessed

- **One way.** Play is its own process; the view gets read-only pipes. A click or a key reaches the law only as a typed
  input record of a later tick, written by the door into the log, as Verðandi's interface rule has it ("Anything that
  would change the game … goes back as an input record of the next tick", `docs/BOUNDARIES.md`) (DECLARED).
- **Witnessed by the reconciler.** The reference replays the log and nothing else. A view (or a debug tool, or a memory
  error) that writes into play's state by any other path makes play part from the reference, and the write is a state
  change without an event: the class P4's "silent" plant is, and only the state field named its tick (MEASURED, P4).
  So the fence is not a promise about the view's code; it is a check on play's state against the reference's, every
  tick, paid for by the tick receipt's state field (§1.2).
- **Plant to require** (DECLARED): a view that pokes one value into play at tick k must be named at tick k.

### 3.3 What graphical must be in the law, and what it costs in Fix

The lineage's rule: the render world decorates and must not decide where anything that blocks is; *"If visual
decoration is intended to affect gameplay, that change must be represented in the authoritative world and checked."*
(the owner's rule, quoted in Verðandi's `docs/BOUNDARIES.md`). For a game, the visual result most likely to affect
play is what a player can see: line of sight, darkness and light, fog. Those go into the law, computed in Fix, and the
law emits its decision (a flag, a visible set); the view draws that decision and never recomputes the predicate in
floats, because a float recomputation near a threshold can disagree with the law's Fix value.

Spherical harmonics of bands 0 to 2 are polynomials of degree at most two in a unit direction's components, so they
need only multiplication and addition, plus a square root and a division to normalize, all exactly rounded in Fix (T5);
no transcendental is needed. A rotation by an angle would need sine and cosine, which Ørlǫg does not have, so a law
takes directions as vectors (or writes its own polynomial approximation, with its error stated).

MEASURED (P5): an order-2 probe (nine coefficients folded with the usual real-SH constants, each literal rounded once
and noted), evaluated at 64 directions per tick and thresholded; the arbiter found the reference, Python, C and Rust in
agreement (dissent NONE) at T = 10. Per evaluation: 34.9 counted operations and 4.5 events; 51 µs in the reference,
1.22 µs in C, 1.33 µs in Rust; C with the compression a no-op 0.47 µs, a soft number (its p10–p90 at T = 500 spans 14
to 34 ms). Against binary64 on the same rounded inputs: at most 1.5 units of 2^-32 (3.6·10^-10) apart, no threshold
decision flipped among the 64, the nearest direction 3.5·10^-3 from the threshold.

What it costs, in admission rather than play: 512 such evaluations a tick (8 players by 64 directions, an
illustration) is about 0.6 ms of C but about 26 ms of reference, so at 60 ticks a second the reference falls behind
and admission needs segments (§1.5) (DERIVED). The cost in Fix is paid by the reference, not by play.

### 3.4 Fairness of view

How much a screen shows depends on its aspect and field of view, which are view parameters. Where seeing confers an
advantage, the law should decide what each player may see, with its field of view fixed in the law, and the view should
draw only that: a renderer cannot reveal what it was never sent. That needs a per-player output (an output port per
player, the door delivering each player only theirs): a later rung, not RUN-1 (DECLARED).

---

## 4. HEADROOM-0: a preregistered headroom measurement

### 4.1 The draft, kept

`work/speed-probe/headroom0-draft.json` (sha256 `5e01f69d6e0376ab2c4beb287639fe1400f1053f6ebf1ced04810cb96150b61d`,
written by the first attempt before any pilot number; its hash was checked again before this round's pilot). It
registers nothing; the owner registers a method or does not. In short:

- **Observable:** S_t per tick, outside the execution (the runtimes read no clock, RUNTIME-SPEC §1): from just before
  tick t's input record is written to the resident play process's pipe to just after tick t's line is read whole.
- **Cells**, all alive at once, one sample each per round in a seeded shuffled order: FLOOR (an echo of the same
  record and line lengths: the transport alone), PLAY, CHAIN.
- **Witness first:** every PLAY and CHAIN line equals the reference's line for its tick; a mismatch, a dead process or
  a short line yields no number.
- **Samples:** 1,000 per cell after 10 warm-up ticks; nearest rank, so p99 is the 11th largest; the 12 largest kept.
- **Rule:** PASS iff p99(S_PLAY) ≤ 950‰ × B × P, in the same run; P = 16,667 µs, B = 100‰ (bound 1,583 µs); the
  50‰ is an adoption margin, not a confidence interval (ALLOC-REUSE-1); VOID if p99(S_FLOOR) alone exceeds the bound.
- **Comparator:** FLOOR, in the same run and interleaved with PLAY, never a number from another run (G10, G13); CHAIN
  beside it, its ratio to PLAY reported and never ruled.
- **Confirmation:** HELD iff PASS in the run and in a confirmation at least 30 minutes later on the same host and
  corpus (G13: twice in Verðandi a preregistered second run was 40–60% slower than its first).
- **Corpus, after RUN-1:** fall.orl as a tick block over a recorded log of at least 1,010 ticks, and 100, 1,000 and
  10,000 bodies over recorded logs.
- **Clock and host:** the declared resolution and the smallest observed step are recorded, and a percentile under 10
  steps is reported as at the clock's resolution; the host is named by the record's own host-state snapshot.

### 4.2 Amendments proposed before any reading

No HEADROOM-0 reading exists; the pilot below is of the instrument, on a stand-in for RUN-1.

1. **PLAY's commitment follows the ruling on the stream head.** The draft calls PLAY the stream; if R5's chain is kept,
   PLAY is the chain, and the other is reported beside, never ruled.
2. **The line is the tick receipt of §1.2,** every field, so the witness is the reconciler itself.
3. **A second period, P = 8,333 µs (1/120 s),** the fixed tick of Verðandi's graybox simulation (`docs/BOUNDARIES.md`),
   read as a label of its own (bound 792 µs). A period is a design parameter, never a claim that anyone's game runs at
   it.
4. **Beside the rule, never read by it:** the reference's cost per tick on the same law and log (the input of §1.5's
   lag), the line's bytes a tick, and Verðandi's HOST-STATE-0 fields attached after the label is fixed.
5. **G12's warning stated in the entry:** until a play shell exists, the measured loop is the instrument's own loop
   (the probe's gate byte stands in for an input record); a shipped play loop gets its own court.

### 4.3 The pilot (MEASURED, P9; the instrument, not the rule)

RUN-1 is not built, so one byte on the pipe gates each tick of fall.orl (loop bound 2,000; 1,010 ticks played), a
stand-in for an input record. Three processes alive at once, one sample each per round in a seeded shuffled order, 10
warm-up ticks, then 1,000 samples per cell; the draft's hash checked first; every PLAY and CHAIN line equal to the
reference's for all 1,010 ticks.

| cell | p50 | p90 | p99 (11th largest) | max | the 12 largest |
|---|---|---|---|---|---|
| FLOOR: an echo answering 214 bytes, the transport alone | 10.2 µs | 12.9 | 41.2 | 144.7 | 39.0 … 144.7 |
| PLAY: the stream head and the full line | 11.9 µs | 16.2 | 39.1 | 112.2 | 39.0 … 112.2 |
| CHAIN: R5's chain and the full line | 12.6 µs | 16.4 | 46.7 | 84.6 | 46.6 … 84.6 |

What it shows about the instrument: the witness holds through the pipe; the tails are the transport's (FLOOR's p99 is
above PLAY's), so on a law this small the reading would be a reading of the pipe, which is why the draft makes FLOOR
the VOID gate; the clock's 100 ns step is far below every percentile. It makes no headroom reading: the corpus does
not exist yet, and a gate byte is not an input.

### 4.4 What it may never be read as

A frame rate; a latency of play, of input or of display; input-to-photon; feel; "competitive"; anything about another
host, another corpus, a network or the view; the admission's speed (recorded beside, never ruled); a correctness result
(correctness is the witness's); a statement that 1/60 s or 1/120 s is anyone's target.

---

## 5. The probes, as run

Every script is in `work/speed-probe/`, run from that folder as `python -B <script>` with `PYTHONHASHSEED=0` and
`PYTHONUTF8=1`, through `run_all.py` one at a time in fresh processes with nothing else of this round running, host
state before and after each in `run_all.log`. Shared apparatus: `common.py` (it refuses to run if `orlog` is not
imported from the snapshot). Witnesses before numbers in every probe.

| probe | what | samples | result file |
|---|---|---|---|
| P0 `p0_apparatus.py` | every variant the probes time or read, against the reference: plain receipts, tick lines (with `'T'`, with state, stream), nohash output; a reference resumed from every C snapshot reproduces every later line and the final head | four laws | APPARATUS HELD |
| P1 `p1_trace_cost.py` | fall.orl: plain, trace, lines, nohash, Rust | n = 40/30/20 per cell at T = 400/4,000/40,000 | `p1.txt` |
| P3 `p3_reference_rate.py` | the reference in process: plain, trace, lines, an integer x_mul | n = 30/12/5 | `p3.txt` |
| P3b `p3b_reference_bodies.py` | the reference on 100 and 1,000 bodies | n = 5 per bound | `p3b.txt` |
| P4 `p4_reconcile.py` | five plants × five field sets; localization; costs at 40,000 ticks | one run each | `p4.txt` |
| P5 `p5_sh_fix.py` | order-2 SH in Fix: four-way agreement, cost, error | n = 15/7 | `p5.txt` |
| P6 `p6_u32_fix.py` | Int and Fix on 32-bit primitives against the vectors; three plants | every vector of 8 ops | `p6.txt` |
| P7 `p7_stream_commit.py` | stream head against chain: plants; fall, 100 and 1,000 bodies | n = 25/15, 21/15 | `p7.txt` |
| P8 `p8_many_worlds.py` | 64 worlds as processes, 1–16 at once | 3 batches per level | `p8.txt` |
| P9 `p9_resident_pilot.py` | HEADROOM-0's instrument | 1,000 per cell | `p9.txt` |
| P10 `p10_log_append.py` | a 64-byte record appended, with and without fsync | 1,000 per cell | `p10.txt` |
| P11 `p11_segment_admission.py` | admission in segments from play's snapshots; two plants | 3 rounds per cell | `p11.txt` |

Per-tick figures are slopes of medians between two loop bounds (the process start cancels); P4's step timings are
single runs. The spread of every cell is in its file (p10–p90, minimum, maximum). Disk: `work/speed-probe/runs2/`
(this round's builds and run folders, about 330 MB) and `runs/` (the first attempt's, about 110 MB) can be deleted.

**Commands.** From `work/speed-probe/`, with `PYTHONHASHSEED=0 PYTHONUTF8=1`: `python -B p0_apparatus.py` (P0),
`python -B p4_reconcile.py` (P4, run alone before the chain), `python -B run_all.py` (P1, P3, P7, P11, P5, P8, P9, P10
and P6, in that order, 2026-10-26 09:00–09:07 local time), `python -B run_all.py p3b_reference_bodies` (P3b, alone,
09:09). Clock: QueryPerformanceCounter through `time.perf_counter_ns`, declared resolution 0.1 µs, smallest positive
step 100 ns; every median below is at least 10^4 steps.

**The measured lines behind the per-tick figures** (milliseconds per run; spread p10–p90 for process runs, minimum to
maximum where n ≤ 5 and for P11's rounds):

| probe | cell | bound | n | median | spread | per tick (slope) |
|---|---|---|---|---|---|---|
| P1 | C plain | 4,000 / 40,000 | 30 / 20 | 19.36 / 66.06 | 17.45–23.22 / 64.28–70.46 | 1.297 µs |
| P1 | C full line and `'T'` | 4,000 / 40,000 | 30 / 20 | 24.98 / 121.19 | 22.68–34.48 / 116.91–147.37 | 2.672 µs |
| P1 | C whole trace | 4,000 / 40,000 | 30 / 20 | 28.63 / 187.56 | 25.66–36.32 / 144.83–243.40 | 4.415 µs |
| P1 | C compression a no-op | 4,000 / 40,000 | 30 / 20 | 13.34 / 16.06 | 12.09–20.59 / 15.30–26.60 | 0.075 µs |
| P1 | Rust plain | 4,000 / 40,000 | 30 / 20 | 20.85 / 79.34 | 19.30–25.27 / 76.21–84.17 | 1.625 µs |
| P3 | reference plain | 4,000 / 40,000 | 12 / 5 | 109.5 / 1,108.5 | 108.1–125.3 / 1,087.5–1,134.5 | 27.75 µs |
| P3 | reference, full line and `'T'` | 4,000 / 40,000 | 12 / 5 | 144.6 / 1,469.6 | 141.0–146.2 / 1,452.3–1,485.5 | 36.81 µs |
| P3 | reference, integer x_mul, table once | 4,000 / 40,000 | 12 / 5 | 76.1 / 754.7 | 75.0–77.4 / 750.4–808.6 | 18.85 µs |
| P3b | reference, 1,000 bodies, full line | 10 / 30 | 5 / 5 | 122.0 / 371.7 | 120.8–124.2 / 368.9–385.6 | 12.5 ms |
| P7 | 1,000 bodies, chain and line | 20 / 200 | 21 / 15 | 29.97 / 190.96 | 28.50–32.89 / 187.01–199.38 | 894 µs |
| P7 | 1,000 bodies, stream and line | 20 / 200 | 21 / 15 | 17.81 / 69.85 | 16.90–18.71 / 68.16–83.70 | 289 µs |
| P7 | 1,000 bodies, plain | 20 / 200 | 21 / 15 | 28.23 / 177.65 | 27.35–30.23 / 174.69–191.22 | 830 µs |
| P7 | 1,000 bodies, compression a no-op | 20 / 200 | 21 / 15 | 12.29 / 20.64 | 11.38–13.05 / 19.06–32.80 | 46 µs |
| P7 | fall, chain and line / stream and line | 40,000 | 15 | 112.16 / 86.41 | 109.74–124.71 / 83.90–98.63 | 2.48 / 1.85 µs |
| P11 | sequential reference | 200,000 | 3 | 7,251 | 7,151–7,448 | — |
| P11 | 16 lanes | 200,000 | 3 | 1,236 | 1,228–1,318 | — |

---

## 6. The claims, graded

| # | claim | grade | does not show | falsifier |
|---|---|---|---|---|
| 1 | Of five planted defect classes, the trace head names one at its tick, R5's per-tick pair two, the full tick line five | MEASURED (P4, one law, one tick) | that five classes are all; any law but the probe's | a class that changes the receipt or a later state and that no field names at its tick |
| 2 | The full line costs 1.4 µs a tick in C and 9 µs in the reference on fall; 64 µs on a 1,000-body C tick | MEASURED (P1, P3, P7) | any other host or law; a resident loop's tail | a confirmation run on this host outside the reported spreads |
| 3 | On fall, a whole trace in play costs more than the full line (4.4 against 2.7 µs a tick; 815 against 218 bytes) | MEASURED (P1) | a law with fewer events a tick; another disk | a rerun on fall in which the trace costs less than the line |
| 4 | Localization from a snapshot costs one window, not a replay (30 ms against 1,219 ms at 40,000 ticks) | MEASURED once (P4) | the cost of SNAP-1's real restore | a restore whose window differs from the full replay's (P4 asserts equality) |
| 5 | Segment admission from checked snapshots equals sequential admission and ran 5.9 times faster at 16 lanes | MEASURED (P11) | scaling on another host; the plateau's cause | a segment's lines, a boundary or the final state differing from the sequential run's on a law that resumes |
| 6 | The compiled tick is 93–95% commitment | MEASURED (P1, P7, three laws) | laws with heavier arithmetic per event (texts, divisions) | a law whose no-op-compression tick is over half its tick |
| 7 | The stream head cuts the commitment to 0.29–0.73 of the chain's and names every planted class | MEASURED (P7) | other defect classes; hash strength beyond SHA-256's | a planted class named by the chain and not by the stream |
| 8 | Int and Fix add, sub, mul, neg and abs are exact on 32-bit primitives | MEASURED (P6, a guarded model, every vector of the eight operations) | division, square root, printing; any device or shader compiler | a vector that differs |
| 9 | Order-2 SH in Fix: 35 operations, 1.2 µs in C, 51 µs in the reference, within 1.5 units of 2^-32 of binary64 | MEASURED (P5) | other directions, bands, thresholds | a direction that flips the predicate with the inputs equal |
| 10 | The two-speed architecture, the dissent rule, the view contract, the sheet's changes, HEADROOM-0 | DECLARED | that any of it works as built | each row of §1.6; HEADROOM-0's own apparatus falsifiers |

---

## 7. Where this proposal is weakest

1. **The state field is linear in the state.** A world of megabytes cannot be digested every tick (about 21 ms a tick
   for 8 MB at this host's per-compression cost, DERIVED). The fallback, a digest every k ticks and a window re-run to
   find the tick, weakens "names the tick" to "names the window" for silent defects. An incremental digest updated
   by events would not see a silent write at all; only one computed from memory does.
2. **Segments need SNAP-1 in all four executions,** none built. The probe resumes the reference by re-entering a For
   loop from a snapshot (`ResumeInterp`), which is the shape a tick block's restore would have, not the thing itself.
3. **Play's snapshots come from the execution under suspicion.** The chained check is what makes them safe; a check
   that compared the wrong boundary, or fewer fields than the snapshot holds, would admit a forged state. The plant
   catches one forged variable; the check must be exact over the whole snapshot.
4. **The timings are process slopes and single shots.** Tails per tick, in a resident loop, were only piloted (P9).
   The memory load sat at 95–98% (recorded, not controlled); Verðandi's record has a second run 40–60% slower than
   its first, once beside a memory load like this one, an association and not a cause (G13). Within-run comparisons
   carry every rule above, and no absolute here should be carried to another sitting.
5. **The stream head changes the trace's form** and keeps the per-event chain alive for v0 in every runtime.
6. **Everything rests on SHA-256's collision resistance,** as the chain already does.
7. **The competitive consequence of a dissent** (is a result after t* − 1 void?) is a policy left to the owner.

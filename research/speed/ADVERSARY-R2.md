# Debate record: the adversary's report on the proponent's design, round 2 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. It was written after the adversary read PROPONENT.md, RESEARCH.md and the judge's measurements and
reran the proponent's probes; its experiments are in `work/speed-adv/` (ignored by git); its MEASURED lines are
this host's.

---

# The speed debate, round 2: the adversary's report (2026-10-26)

A subagent's report for the debate `research/speed/PROPOSAL.md` opens. It is model output, not the owner's words, and
carries no authority. Round 2 prosecutes the proponent's design (`work/speed/PROPONENT.md`) after reading it, the
prior-art survey (`work/speed/RESEARCH.md`), the judge's measurements (`work/speed/JUDGE-MEASUREMENTS.md`) and my own
round 1 (`work/speed/ADVERSARY.md`). Nothing here is built into the language or admitted.

**Where this ran.** On this host, with other sessions running.
- **Ørlǫg** ran only from my round-1 snapshot of `f16dc26` (`work/speed-adv/tree`). `work/speed-adv/r2/verify_tree.py`
  checked it against the commit's blobs: 719 files, 0 differ, 0 missing, 0 extra, tree `8be71851`, the tree the
  proponent checked (`work/speed-adv/r2/SNAPSHOT.txt`). The working copy, which another session has changed, was
  never imported.
- **The proponent's probes** were copied into `work/speed-adv/r2/`, with their hashes at copy time in
  `COPIED-FROM-SPEED-PROBE.sha256`. Two one-line changes are marked in the files: `common.py`'s `TREE` and
  `p6_u32_fix.py`'s `ROOT` point at my snapshot. As copied, P6 looked for `r2/tree` and stopped with
  FileNotFoundError; rerun after the change. Nothing was written into `work/speed-probe/`.
- **My own fixtures** use the proponent's apparatus (its tick line, its reference lines, its `patch_c`). Every plant is
  a textual change to the generated C, asserted to apply once. Each is applied before `patch_c`, except S3's, which
  edits the hashing line `patch_c` leaves and so comes after it.
- **Toolchains** as in round 1. **Clock:** QueryPerformanceCounter through `time.perf_counter_ns`, declared resolution
  1e-7 s, smallest observed step 100 ns, recorded in each run's JSON. **Host state:** recorded beside each run by the
  proponent's `host_state()` (`work/speed-adv/r2/run_all.log`), read by no rule.
- **Environment:** PYTHONHASHSEED=0, PYTHONUTF8=1, `python -B`, scripts run from `work/speed-adv/r2/`. No tracked file
  was changed.

**Grades.** MEASURED (a run here; the command is the script named), ESTABLISHED (read from code or a cited record),
DECLARED (an argument, or a statement that nothing checks something), OBSERVED, SPECULATIVE, NOT_MEASURED. DERIVED marks
arithmetic on measured numbers. **Severity**, worst first: *breaks a guarantee*, *overclaims*, *costs more than
stated*, *only words*. Every timing is a software timing of one component on this host. None is a latency, a frame
rate, an input-to-photon figure or a feel, and no number carries to another host, law or sitting.

---

## The findings at a glance

Witnesses side by side, not a score. The rows are in the brief's order of severity; their names are only labels.

| # | finding | grade | severity | § |
|---|---|---|---|---|
| B1 | **Segmented admission accepts a wrong receipt.** The proponent's snapshot and state field omit a certificate clause's cost accumulator, which its own design text puts in the state. On a law whose certificate clause runs in the tick and whose claim follows the last tick, every check P11 makes passes, and so does P11's own final comparison. Yet the segmented reference's receipt reads ref-cost 2,000 where the sequential reference's reads 32,000. In RUN-1's shape, with the claim inside the tick, the same omission gives a false dissent against a correct play (14 boundaries broken), and under §1.4 the wrong receipt is the record that stands | MEASURED | **breaks a guarantee**: "a run is a function of the law and its log alone" | 4.2 |
| B2 | **The stream head, as prototyped, commits nothing of a refused tick**, nor, in version 0's shape, of statements after the last tick. Two executions whose `'A'` events differ there write byte-identical receipts in both of P7's stream modes. Under the chain the receipts differ in `trace-head`. The design text does not say where a refused tick's events go | MEASURED | **breaks a guarantee** (as prototyped); a hole in the design | 5.2 |
| O1 | A bit flipped in a truth value's storage (1 to 3) at tick 237 is named at tick 300, 63 ticks late. The value encoding writes any nonzero truth value as the byte 1, and the C comparison is `== 1`. The localization at tick 300 shows the comparison, never the corrupted variable. The plant the proponent asks for ("a view that pokes one value into play at tick k must be named at tick k") fails for this value | MEASURED | overclaims ("memory written where it should not be" is named at its tick) | 2.2 |
| O2 | The bytes a view is shown are not the bytes committed. A one-bit difference between the bytes written and the bytes hashed at tick 237 leaves every field of every line, and the receipt core, equal to the reference's. Only the arbiter's byte comparison of output files sees it, after the run. In the design the view reads play's pipe, which no admission run compares | MEASURED (the plant); DECLARED (the consequence) | overclaims (the fence and the view contract) | 2.2, 6.2 |
| O3 | The restore joins the authority. Three planted restore defects each make segmented admission dissent against a play that the sequential reference agrees with: first divergence at tick 2,001, 14 boundaries broken. In one, the reference raises a Python exception in 15 segments. Under §1.4's rule ("the reference's record stands") play would be quarantined. "With no change to the definition" overclaims | MEASURED | overclaims | 4.3 |
| O4 | A transient fault (one that does not recur) is named at its tick by the live line. The design's localization re-runs play, and that re-run reproduces nothing: receipt and window equal the reference's. Localizing it needs play's own live window, which the design does not keep | MEASURED | overclaims ("a windowed re-run names the event") | 2.2 |
| O5 | A defect in the commitment's own code is located to its event by the chain (event 1,631: payload equal, head different). The stream locates it to its tick only | MEASURED | overclaims ("a trace is self-authenticating per tick" understates what is lost) | 5.1 |
| O6 | HEADROOM-0 reads PASS, at both periods, for a law whose every 100th tick takes 19.0–21.2 ms of play: 10 ticks of 1,000, each over the whole 1/60 s period. It reads PASS on ticks 11–1,010 of a law that FAILs on ticks 4,011–5,010 of the same run (p99 575 µs, then 2,802 µs, against a bound of 1,583 µs) | MEASURED | overclaims (if PASS or HELD is read as headroom) | 7 |
| O7 | The proponent's view reads snapshots, that is all state, which is exactly what my round-1 floor-mirror leak needs. Per-player output, the remedy the proponent names, is deferred to "a later rung, not RUN-1" | ESTABLISHED; MEASURED in round 1 | overclaims ("the view reads; it never writes" offered as the view's safety) | 6.2 |
| O8 | P11's 5.9 times is batch admission of a completed run, on a law whose reference is already about 450 times faster than real time. The probe's snapshot refuses the laws that need segments (lists). Live, the lag is a segment's length in reference time | MEASURED (the refusal); DERIVED | overclaims | 4.4 |
| O9 | P5's spherical-harmonic law evaluates pre-normalized literal directions, so no square root or division ran. Its 1.5 units and 35 operations do not cover a law that normalizes: round 1's A12 stands. P6's 32-bit model covers neither division nor square root | ESTABLISHED (read from P5's generated law) | overclaims, if generalized | 6.1 |
| C1 | The state field on a large state costs about 20 ns an element in C and about 134 ns in the reference, the watch tier's cost. At 2^16 Fix values the reference's digest alone takes 8.8 ms a tick, over 1/120 s. At the language's list maximum (2^24) that is about 0.33 s a tick in C and 2.2 s in the reference, per list | MEASURED to 2^20 (C) and 2^16 (reference); DERIVED beyond | costs more than stated (the reference's side was not stated) | 3.2 |
| C2 | HEADROOM-0's adoption margin is 50‰. Between the proponent's sitting and mine, the same day, its own instrument's p99 moved by 29–60% (P9 rerun). Between two of my runs minutes apart, the same window of the same law moved by 33% | MEASURED | costs more than stated | 7 |
| W1 | Write-ahead to a log whose durability trails by a group means that after a crash the durable log is shorter than what was played and shown, by up to a group. Those ticks can never be admitted | DECLARED | only words, until a document says what a session's last group is | 4.4 |

---

## 1. The proponent's probes and claims, rerun

### 1.1 The probes

Each probe as the proponent wrote it, from `work/speed-adv/r2/`, run one at a time by its own `run_all.py` (P1, P3,
P7, P11, P5, P8, P9, P10, P6), plus P0, P4 and P3b alone. Deterministic results are compared byte for byte; timings in
orders of magnitude (Verðandi G4).

| probe | the proponent's result | here | reproduces |
|---|---|---|---|
| P0 apparatus | APPARATUS HELD | APPARATUS HELD | yes |
| P4 five plants × five readings | the table of §1.2 | the first 11 lines of `p4.txt` byte-identical to the proponent's | yes, exactly |
| P4 at 40,000 ticks | compare lines 1.6 ms; resume from the reference's snapshot 30 ms against 1,219 ms from tick 1 | 1.5 ms; 33.9 against 1,311.5 ms | yes |
| P1 fall, C per tick | plain 1.297, full line + `'T'` 2.672, nohash 0.075, Rust 1.625 µs | 1.307, 2.708, 0.109, 1.586 µs | yes. The nohash slope between T = 400 and 4,000 read −0.210 µs here: process-start noise at small T, as the proponent warned |
| P3 the reference, fall | plain 27.75, full line 36.81, integer x_mul 18.85 µs | 28.96, 38.20, 20.25 µs | yes |
| P3b the reference, 1,000 bodies | 12.5 ms a tick | 12.4 ms | yes |
| P7 the stream's plants | all five named at 237, the control at none | identical | yes, exactly |
| P7 stream ÷ chain beyond nohash | 0.734, 0.299, 0.286 | 0.742, 0.306, 0.290 | yes |
| P11 segments | 16 lanes 1,236 ms against 7,251 (5.87 times); both plants caught | 1,225 against 7,330 ms (5.98 times); plants identical | yes. One W = 8 round read 2,459 ms against a median of 1,600 |
| P5 SH in Fix | four-way NONE; 1.5 units; 1,220 ns C; 51 µs reference; nohash 468 ns | NONE; 1.5 units; 820 ns; 49 µs; nohash 108 ns | accuracy exactly; times within an order; the nohash figure moved 4.3 times, confirming the proponent's "a soft number" |
| P6 32-bit model | 5,620 of 5,620 agree; plants caught by 28, 18 and 21 vectors | `p6.txt` identical | yes, exactly |
| P8 64 worlds | 16 at once 0.681 s, 3.76e6 world-ticks a second | 0.655 s, 3.91e6 | yes |
| P9 HEADROOM-0's instrument | witness held; p99 FLOOR 41.2, PLAY 39.1, CHAIN 46.7 µs | witness held; p99 56.3, 50.5, 74.5 µs | the witness, yes; the p99s moved +37%, +29% and +60% (C2) |
| P10 log append | p50 4.7 µs; fsync 317 µs; one fsync per 16, p99 502 µs | 5.0; 318.6; 530.4 µs | yes |

So every deterministic claim reproduces exactly, and every timing within its order of magnitude.

### 1.2 The ten claims of the proponent's §6

| # | claim | reproduces here | where it overclaims | what it does not show |
|---|---|---|---|---|
| 1 | the trace head names 1 of 5 planted classes at its tick, R5's pair 2, the full line 5 | exactly | read as covering "memory written where it should not be": a truth value is named 63 ticks late (O1); bytes shown are named never (O2); a transient is named but not localized (O4); the probe's line omits the accumulators the design lists (§2.2, A5) | representations; the output a view is shown; faults that do not recur; texts |
| 2 | the full line costs 1.4 µs a tick in C and 9 µs in the reference on fall; 64 µs on a 1,000-body C tick | yes: 1.40 µs, 9.24 µs, 68 µs | — | a large state: about 20 ns an element in C and 134 ns in the reference (C1) |
| 3 | on fall a whole trace costs more than the line | yes: 3.65 against 2.71 µs | — | — |
| 4 | localization from a snapshot is one window: 30 against 1,219 ms | yes: 33.9 against 1,311.5 ms | "names the event" assumes play's defect recurs when play is re-run (O4); play has no restore and re-runs from tick 1 | play's re-run on a heavy law |
| 5 | segment admission equals sequential admission, 5.9 times at 16 lanes | yes on fall: 5.98 times; plants identical | "equals" fails where the snapshot omits state (B1); "no change to the definition" (O3); the laws and the mode that need it (O8) | lists; live play; after a broken boundary; the plateau's cause |
| 6 | the compiled tick is 93–95% commitment | yes: 94.8% on 1,000 bodies | — | laws with heavier arithmetic per event |
| 7 | the stream cuts the commitment to 0.29–0.73 of the chain's and names every planted class | yes: 0.290–0.742; plants identical | a refused tick and the statements after the last tick are committed nowhere (B2: its own falsifier met); commitment-code defects located to the tick only (O5) | refusals; the end of a run |
| 8 | Int and Fix add, sub, mul, neg and abs exact on 32-bit primitives | exactly | — (it names its eight operations) | division, square root, printing (O9) |
| 9 | order-2 SH in Fix: 35 operations, 1.2 µs C, 51 µs reference, 1.5 units | accuracy exactly; 0.82 µs; 49 µs | if read as covering a law that normalizes (O9; round 1's A12) | normalization; short vectors |
| 10 | the architecture, the dissent rule, the view contract, the sheet's changes, HEADROOM-0 (DECLARED) | — | the view contract (O2, O7); the dissent rule under segments (O3); HEADROOM-0 (O6, C2); durability (W1) | — |

What follows is about what the claims do not cover.

---

## 2. Q1: does the per-tick line name every defect at its tick?

### 2.1 What holds

The proponent's line (events, ops, output bytes, head, output chain, claims, state) names each of its five planted
classes at tick 237, and R5's pair names two (MEASURED, reproduced exactly). This answers my round-1 A1: committing
`ops` per tick names the tick where the counts part. I concede A1's remedy (§9).

The proponent's falsifier for its claim 1 is "a class that changes the receipt or a later state and that no field
names at its tick".
- A2, and A5 in version 0's shape, meet it.
- A3 changes the run's output and not its receipt, and no field names it.
- A4 is named at its tick and fails later, at localization.
- A1 is the control.

### 2.2 Kinds neither side planted (`q1_new_plants.py`, `q1_new_plants.txt`)

Same apparatus, same reference lines, same reading (the first line whose fields differ).

| plant | law | planted | the line names | fields there | receipt core | output |
|---|---|---|---|---|---|---|
| A1 bit 1 of an integer flipped (`shots ^= 2`) | latch | end of tick 237 | **237** | state | differs | `shots 103` against `shots 101` |
| A2 bit 1 of a truth value flipped (`armed ^= 2`: 1 to 3) | latch | end of tick 237 | **300** | events, ops, head, state | differs | `shots 0` against `shots 101` |
| A3 one bit of the bytes written, not of the bytes hashed | fall with a Say in its tick | tick 237 | **none** | — | **equal** | differs at byte 6,499, line 237: `y = 5.5282958…` against `x = 5.5282958…` |
| A4 transient: `landed_at` one more, live run only | P4's claim-bearing fall | tick 237 | live: **237**; re-run: **none** | live: state | live: differs; re-run: equal | — |
| A5 a certificate's cost accumulator one more (`g_cost4 += 1`) | CERT-AFTER (`q3b_certificate.py`) | tick 237 | **none** | — | differs (`… 4 32001` against `… 4 32000`) | — |
| A5 in RUN-1's shape | CERT-IN | tick 237 | 237 | claims | differs | — |

The latch law is `Let armed be true. Let shots be 0.` and a tick of `If tick is at least 300 and armed equals true,
set shots to shots plus 1.` (in the script).

- **A2: a representation the encoding normalizes.**
  - `orl__enc_elem` writes "Any nonzero v is true: … the byte 1 (its one normalisation point)" (`rt_c/orlog_rt.h`).
    The state field hashes that encoding, so the corrupted slot reads as `true` in both executions, and every line
    through 299 is equal.
  - The C comparison `armed equals true` is generated as `t = (a == b)` (`src/orlog/gen_c.py`, op `cmp`), and `3 == 1`
    is false. The divergence appears only when that comparison first runs, at tick 300, as a missing `'A'` event on
    `shots`.
  - A localization there shows a comparison that "should" have been true, while `armed` reads `true` in both traces.
    The corrupted variable is invisible to every observation the design makes. Only a raw memory read shows the 3.
  - RUNTIME-SPEC §8 states the representation ("bools as 0/1"). Nothing checks it at a tick boundary.
  - A1 is the control: the same flip on an integer is named at 237.
  - The proponent's §1.2 offers the silent plant as standing for "memory written where it should not be, the class a
    C program's memory errors fall into". A2 is a member of that class that the state field names late.
- **A3: shown is not committed.**
  - The tick line, R5's output chain and the receipt's output hash are all computed from the buffer the runtime
    hashes. A defect between that buffer and the bytes actually written (a second write path, a buffer reused, a
    serializer for the view) leaves every commitment equal.
  - The arbiter does compare output files (`r.get("out") == bytes(ref.out)`, `src/orlog/arbiter.py`), so a batch run
    would dissent at the end, naming no tick.
  - In the proponent's design the view reads play's pipe, and admission re-runs C fresh. Nothing ever compares the
    bytes a player was shown with anything.
- **A4: a fault that does not recur.**
  - The live line names 237 (state), which is right.
  - The proponent's step 2, "run both again from the nearest snapshot … compare event lines", re-runs play. Here
    the re-run's receipt equals the reference's, its every line equals the reference's, and the window trace equals
    the reference's.
  - Memory errors that depend on allocation, stack contents, a race or hardware (the survey: Haque and Pande, soft
    errors on consumer GPUs in the field) are of this kind. Localizing them needs what play recorded live.
- **A5: state the probe's line does not hold.** The proponent's design text puts "every clause-cost accumulator" into
  the state field (§1.2). The probe's state field (`common.state_digest`, `statedigest_code`) does not: it hashes
  top-level variables only. So the MEASURED claim covers a narrower line than the DECLARED one.
  - In version 0's shape, a claim after the last tick, no line names the change.
  - In RUN-1's shape, a claim in the tick (R2 makes the tick block the last top-level clause; D8), the claims field
    names it at the claim's next evaluation, here in the same tick.

**Grade:** MEASURED, one run each, deterministic. **Severity:** overclaims (A2, A3, A4); only words, for the gap
between the probe and the design (A5's line). **Does not show:** that these defects exist in any runtime today, or
how often memory errors take these forms. **Falsifier:** a state field that names A2 at tick 237, for instance one
that checks each truth-value slot is 0 or 1 at the boundary; a view that recomputes R5's out_t over the bytes it
received and names A3 at 237.

### 2.3 What the sheet would still need, beyond the proponent's §1.6

1. **The representation checked, not only the value.** At each boundary, play refuses a truth-value slot that holds
   anything but 0 or 1, as a host fault rather than a law refusal. Alternatively, the generated code canonicalizes
   at every write. Either names A2 at its tick. A plant: A2.
2. **The view verifies what it reads.**
   - For Say output, the view hashes each tick's bytes as received and checks them against the line's out_t (R5's
     own definition).
   - For snapshots, it checks against the state field.
   - That moves the fence's witness to the point where the player is shown something. A plant: A3.
3. **Play keeps its own last window**, the events of the last few ticks in a ring buffer, written out when its line
   is first contradicted. Re-running cannot localize what does not recur. A plant: A4.
4. **The state field and SNAP-1 hold every clause-cost accumulator**, as the design text says and the probe does not.
   A plant: A5, and B1 below.

---

## 3. Q2: is a state digest per tick sound, and what does it cost?

### 3.1 Sound for values, not for representations; and only over what it lists

- **Values.** SHA-256 over an injective encoding of the listed variables in id order. Equal digests imply equal
  values, barring a collision. The silent plant on an integer is named at its tick (P4; A1). ESTABLISHED, MEASURED.
- **Representations.** The encoding is not injective on the machine's state: truth values are normalized (A2), and so
  are NaN payloads (`ORL__CANON_NAN`). Equal digests do not imply equal machine states, and C's `==` reads the
  machine state. MEASURED (A2).
- **What it leaves out.**
  - Clause-cost accumulators: in the design text, absent from the probe (A5, B1). MEASURED.
  - Texts: the probe refuses them ("the probe's state field does not encode texts"). ESTABLISHED.
  - The bytes shown (A3). They are not state, but they are what the view contract is about.
  - Variables declared after the tick: D6 excludes them. The probe is inconsistent here: the reference's state field
    raised KeyError on one (MEASURED, S2's law in `q1_new_plants.py`), while the C one hashes them as zero
    (ESTABLISHED, `statedigest_code`). This is harmless under R2, where nothing follows the tick block.
- **Its author is the suspect.** The digest is computed by the execution under suspicion from the memory it computes
  with. It is testimony checked against the reference's, which is right. But a defect in the digest's own code is
  a false dissent, never a miss. DECLARED.
- **Not chained.** Each line's state field stands alone, so a divergence that heals (written, then overwritten
  unread) shows in one line and not in the next. The reconciler must scan lines in order, as the proponent's does, and
  never bisect them. The survey makes the same point about unchained per-tick hashes (`work/speed/RESEARCH.md` §12,
  Q1.2). DECLARED.

### 3.2 What it costs on the worst law one can write (`q2_state_cost.py`, `q2_state_cost.txt`)

The worst law for this field is a large state that a tick barely touches: `Let big be a list of N copies of 0.5.`,
and a tick of one integer assignment. The cost is the proponent's own field (`patch_c(state=True)`,
`CkptInterp(state=True)`); witnesses first (receipt core and lines equal the reference's, N ≤ 2^16). Per tick =
slope of medians between two loop bounds; C cells interleaved in a seeded shuffled order.

| N (Fix values) | state | C: the state field a tick | the reference: the state field a tick |
|---|---|---|---|
| 2^12 | 32 KB | — | 0.46 ms |
| 2^14 | 128 KB | 0.33 ms | 2.02 ms |
| 2^16 | 512 KB | 1.36 ms | **8.78 ms** (over 1/120 s) |
| 2^18 | 2 MB | 5.25 ms | — |
| 2^20 | 8 MB | **20.7 ms** (over 1/60 s) | — |

- C costs about 20 ns an element. That confirms the proponent's DERIVED "about 21 ms a tick for 8 MB".
- The reference costs about 134 ns an element, 6.8 times C. The proponent did not state that side, and it is the
  binding one, because the watch tier must compute the same digest every tick to compare it.
- The tick's own work is below this method's noise: the plain cell's slope read between −7.9 and +96 µs. P1 measured
  1.3 µs for a fall tick of 8 events.
- DERIVED: at 2^24, the language's list maximum (`ORL_LIST_MAX`), the field costs about 0.33 s a tick in C and
  2.2 s in the reference, per list. The ratio of field to tick is unbounded, since a law may hold as many such
  lists as memory allows.
- The proponent's fallback, a digest every k ticks, weakens "names the tick" to "names the window" (its §7, weakness
  1). An incremental digest would not see a silent write at all (its own note).

**Grade:** MEASURED (this host, one sitting); DERIVED beyond 2^20 and 2^16. **Severity:** costs more than stated.
**Does not show:** texts; any law with less state; another host. **Falsifier:** a state field that names P4's
silent plant at its tick on W(2^20) in the reference within 1/120 s.

---

## 4. Q3: does segmented replay keep "a function of the law and its log alone"?

### 4.1 What holds

The boundary check is an induction. Segment 0 runs from the law, and segment j's start is admitted only if segment
j−1's own end equals it. That is sound over whatever the snapshot holds. The forged-snapshot plant is caught at its
boundary, and the value plant at its tick (P11, reproduced exactly). The proponent saw the condition itself (§7,
weakness 3): "the check must be exact over the whole snapshot". §4.2 is where "the whole snapshot" and "the whole
state" part. §4.3 is about the code that reads the snapshot back.

### 4.2 The snapshot omits state the receipt depends on (B1; `q3b_certificate.py`, `q3b_certificate.txt`)

`Let s be 0. Let total be 0.`, and a tick in which `§3.1 For each i from 1 to 3` adds i to s and `§3.2` adds 6 to
total, for 3,200 ticks. The claim is `We claim that s equals total, by the certificate of §3.1 under the theorem "one
plus two plus three is six".`
- **CERT-AFTER**: the claim after the last tick (version 0's shape, the shape of fall.orl's own closing must).
- **CERT-IN**: the claim inside the tick (RUN-1's shape).
- Segmented admission as P11 runs it: 16 segments of 200 ticks, segment j > 0 resumed by `common.ResumeInterp` from
  play's snapshot.

| | P11's line check | P11's boundary check | P11's final comparison | play's receipt = the sequential reference's | the segmented reference's receipt |
|---|---|---|---|---|---|
| CERT-AFTER | passes | passes | passes | yes | `claim 0 7 1 1 1 4 2000` against `… 4 32000`: **wrong** |
| CERT-IN | fails from tick 201 | 14 broken | fails | yes | `… 3200 3200 3200 4 2000` against `… 4 32000` |

- **The mechanism.**
  - The reference keeps a certificate clause's accumulated cost in `Interp.clause_cost` (`src/orlog/interp.py`), the
    C program in `g_cost<clause>`, and the receipt's claim line records it (RUNTIME-SPEC §7).
  - The probe's snapshot (`snap_line`, `orl__pk_snap`) holds the top-level variables and the claim records, not the
    accumulators. `ResumeInterp` therefore restarts them at zero, and neither check compares them.
  - The proponent's design text names them as state; its probe omits them; SNAP-1 does not exist.
- **What it breaks.**
  - In CERT-AFTER the segmented reference's receipt depends on where the segments were cut, while every check that
    would admit it passes. That breaks "a run is a function of the law and its log alone", as segmented admission
    is built.
  - The proponent's falsifier for its claim 5 is "a segment's lines, a boundary or the final state differing from
    the sequential run's on a law that resumes", and it is met: the final receipt differs, and the lines and
    boundaries do not.
  - In CERT-IN, RUN-1's shape, the same omission is caught, but as a dissent against a correct play. Under §1.4 the
    record that stands is the segmented reference's, and its receipt (ref-cost 2,000) is the wrong one.
  - CERT-AFTER's silent admission needs a statement after the tick. That cannot happen in a v1 law (R2), only in a
    version-0 law admitted in segments, which is what P11 itself does with fall.orl. CERT-IN's false dissent is the
    RUN-1 case.

**Grade:** MEASURED, deterministic. **Severity:** breaks a guarantee. **Does not show:** that SNAP-1, once written,
would omit the accumulators. It shows that nothing in segmented admission's checks can notice an omission that the
snapshot and the line share. **Falsifier:** a SNAP-1 snapshot and boundary check under which CERT-AFTER's segmented
receipt equals the sequential one, held by this law as a plant.

### 4.3 The restore joins the authority (O3; `q3_segments.py`, `q3_segments.txt`)

Play is fall.orl's C program at T = 32,000, correct, and the sequential reference agrees with it. Admission is 16
segments of 2,000 ticks, with four restores:

| restore | the first tick whose line differs | boundaries broken | the segmented verdict on a correct play |
|---|---|---|---|
| as built (`common.ResumeInterp`) | none | none | agrees |
| ops+1 (the counter restored one high) | 2,001 | 14 (4,000 to 30,000) | **dissents** |
| fencepost (the loop re-entered at k, not k+1) | 2,001 | 14 | **dissents** |
| unsigned (a negative value decoded as unsigned) | 2,001 | 14 | **dissents**; the reference raised `struct.error` in all 15 resumed segments |

- The proponent rejected an integer x_mul in the reference for "changing the code whose smallness is its authority"
  (§2.1), and proposed segments "with no change to the definition". A segmented reference is the reference plus a
  restore. A restore defect turns a correct play into a dissenter.
- Under §1.4 ("Whose record stands: the reference's replay of the logged inputs, by declaration"), play would be
  quarantined.
- The pattern is diagnostic: every segment but segment 0, the one without a restore, dissents at its first tick. But
  no rule reads patterns.
- The unsigned case adds that the interpreter is not a hardened consumer of restored state. An out-of-range value
  makes it raise, an outcome the arbiter's kinds do not name.

**Grade:** MEASURED, with planted defects in code that does not exist yet. **Severity:** overclaims ("with no change to
the definition"). **Remedy (DECLARED):** hold the restore with its own court, before it is trusted.
- The survey's GGPO sync test, rolling back and resimulating every frame (`work/speed/RESEARCH.md` §2), is the
  pattern.
- Re-admit a sample of segments sequentially, and plant restore defects like these three.
- Say in §1.4 that a dissent which every resumed segment shares, and the unresumed one does not, is charged to the
  restore.

### 4.4 What P11 does not show (O8)

- **The laws that need it.** On fall the reference is already about 450 times faster than real time. The probe's
  snapshot refuses lists: `top_scalars(bodies_text(100, 10))` stops with "the probe's snapshot holds scalar top-level
  variables only" (MEASURED, `q3_segments.txt`). On the 1,000-body law, where c_ref is 12.4 ms against 8.33 ms, the
  speed-up is NOT_MEASURED, as the proponent says.
- **Live.** P11 admits a completed 200,000-tick run in parallel.
  - Live, a segment can start only when play has written its snapshot, and it can run no further than play's log.
    So it needs about c_ref/P lanes, and the watermark trails by about one segment's length in reference time.
  - DERIVED for the 1,000-body law at 1/120 s, with segments of 1,000 ticks: 2 lanes, a lag of about 12 s; with
    12,500 ticks, about 155 s.
  - A short segment means a snapshot and a restore every L ticks: NOT_MEASURED.
- **After a break.** Once a boundary breaks, every later snapshot of play is suspect. Admission from there runs
  sequentially from the reference's own state, at c_ref a tick. DECLARED; the design does not say it.
- **The plateau** past 8 lanes reproduces (W = 8, 1,600 ms; W = 16, 1,225 ms). Its cause is NOT_MEASURED here too.
- **W1, durability.** The door writes ahead to the log and commits to the device by groups (§1.1, §1.5). After a
  crash, up to a group of ticks were played and shown that the durable log lacks, and they can never be admitted.
  DECLARED.

**Severity:** overclaims, where 5.9 times is read as the reference keeping pace on a heavy law in live play.

---

## 5. Q4: what does one hash per tick let a divergence report locate?

### 5.1 Events: the same; the commitment's own code: the tick, not the event (O5)

- **A divergence in an event.** The stream names its tick (P7, reproduced). Comparing the window's records (number,
  kind, clause, payload) names the event, exactly as the chain's trace lines do. The record carries everything the
  chain's line carries except the head. DECLARED from the formats.
- **A divergence in the commitment's computation** (S3, printed as B3 in `q1_new_plants.txt`): the header's clause
  byte of one event of tick 237 is hashed flipped, while the trace writes the event as it is.

| | the line names | the window names |
|---|---|---|
| chain | tick 237 (head) | event 1,631, §12.2, `'A'`: **payloads equal, heads differ**: "this event's commitment differs" |
| stream | tick 237 (head) | nothing: every record of the tick agrees |

A new implementation of the commitment can introduce this kind of defect: a GPU lane, a v1 runtime, a port. How often
it would is SPECULATIVE. With the chain, the arbiter's existing `localize` names it to the event. With the stream, it
names the tick and the field `head`, and stops. **Grade:** MEASURED. **Severity:** overclaims. **Remedy (DECLARED):** a
debug mode in which each execution writes, per event, the exact bytes it fed to the stream, compared as the chain's
heads are.

### 5.2 A refused tick, and what follows the last tick: nothing, as prototyped (B2)

Two fixtures, printed as B1 and B2 in `q1_new_plants.txt`:
- **S1**: GAUGE is fall's motion plus `If tick is 300, set gauge to x times 1000000000.0 times 1000000000.0`, which
  refuses OVERFLOW in tick 300. The plant: x one raw unit more at the start of tick 300, so tick 300's `'A'` on x
  differs and the refusal comes at the same operation.
- **S2**: the same motion with no overflow, and `Let z be x times 2.0.` after the last Say. The plant: x one raw unit
  more after that Say, so z's `'A'` differs and no output does.

| | chain (as built) | chain + line | stream + line (P7's PLAY) | stream only |
|---|---|---|---|---|
| S1 receipts, clean against planted | differ in `trace-head` | differ in `trace-head` | **byte-identical** | **byte-identical** |
| S2 receipts, clean against planted | differ in `trace-head` | differ in `trace-head` | **byte-identical** | **byte-identical** |

- Tick lines 1–299 (S1) and 1–400 (S2) are equal in every mode: the refused tick writes no line (the proponent's
  §1.6), and nothing after the last tick does.
- In P7's stream + line mode the receipt's head stays head0. In stream-only mode it is the last tick's P_t. Neither
  folds in the partial tick (its `'R'` event included) or the post-loop events.
- The design says only that "the `'T'` line carries P_{t−1}". So two executions that part inside a refusing tick, or
  after the last one, agree on every committed byte, and the arbiter's comparison (receipt core and output) reads
  agreement.
- **S1 is the case that matters for RUN-1.** Under R4 a a refusal ends a session inside a tick, or inside the prefix
  before the first `'T'`, which is the same hole. **S2 cannot arise** in a v1 law, because R2 makes the tick block
  the last top-level clause and the proponent keeps the chain for v0 laws (COMPAT-0). It shows the same omission at
  the run's other end, should anything ever follow the last tick.
- The proponent's falsifier for its claim 7, "a planted class named by the chain and not by the stream", is met.

**Grade:** MEASURED. **Severity:** breaks a guarantee (the replay theorem's "the trace head commits"), as prototyped.
The fix is cheap: finalize the stream into the receipt's head at a refusal and at the end, with these two laws as
plants. P7's per-tick costs are unaffected.

### 5.3 What a dissent can carry

With the chain, an event can be checked against the next committed `'T'` head by hashing the events from it to the end
of its tick. With the stream, by hashing the whole tick. That is a factor of at most about two in a dissent's evidence:
a cost, not a loss. DERIVED.

---

## 6. Q5: the GPU carve-out, and the view that only reads

### 6.1 The GPU carve-out holds, because it claims little

"A GPU only for many independent worlds, integer-only, never the authority" agrees with my round-1 A15. P8's CPU
baseline reproduces (3.91e6 world-ticks a second at 16 processes), and it is the right falsifier for any GPU claim.
P6 reproduces exactly. What its evidence does not cover (O9):
- division, square root and printing (a Fix prints up to 32 fraction digits; RUNTIME-SPEC §3), all of which a law
  that normalizes a direction needs;
- refusals masked per lane under divergence between worlds;
- any device or shader compiler.

P5's law does not normalize: its directions are 6-decimal literals (`p5-program-T20.orl`), and its basis uses
`3.0 times z times z minus 1.0`, equal to 3z² − r² only on the unit sphere. The survey measured that the two spellings
differ in raw value on 49,951 of 100,000 directions (`work/speed/RESEARCH.md` §11). So P5's 1.5 units and 35
operations are for pre-normalized inputs, and round 1's A12 (short vectors lose precision, then refuse below 2^-16 m)
stands untouched. Each world a GPU previews is still admitted only by the reference's full replay, so the GPU speeds
exploration, never admission. **Grade:** ESTABLISHED; MEASURED (reruns). **Severity:** overclaims, only if
generalized.

### 6.2 "The view reads; it never writes" does not survive the floor mirror

1. **What the view reads.** §3.1: each tick's output lines and, "after SNAP-1, snapshot bytes at the ticks it asks
   for: typed state … a view that draws many bodies should read snapshots".
   - A snapshot is the whole state, every hidden entity included.
   - My round-1 A10 measured Verðandi's own renderer putting a target wholly behind a 4 m wall on the screen: 76–457
     pixels changed, by up to 30 of 255, at every distance from 6 to 40 m, through the floor mirror's pass. That was
     one browser engine on one GPU (`work/speed-adv/webleak/results/`, MEASURED in round 1).
   - A renderer can leak only what it was given. The proposal gives it everything.
2. **What the fence witnesses.** §3.2's witness is play's state against the reference's.
   - It does not see a value the encoding normalizes (O1).
   - It does not see the bytes the view was shown (O2).
   - It does not see the channel round 1 called A11, the player: an input shaped by a leaked picture enters the log
     and replays identically by construction.
3. **The remedy is in the proposal, deferred.** §3.4 says the law should decide what each player may see and the view
   draw only that, which "needs a per-player output … a later rung, not RUN-1". Until then a view that "only reads"
   reads too much. A view tier, if it ships with RUN-1, needs per-player output in the same rung, or a written
   statement that it is unfit for any use where hidden state matters.

**Grade:** ESTABLISHED (the text); MEASURED in round 1 (the leak) and here (O1, O2). **Severity:** overclaims, where
"never writes back" is offered as the view's safety. **Falsifier:** `work/speed-adv/webleak/index.html` reading 0
differing pixels on the shipped renderer, or a view tier whose input is only what its player may see.

---

## 7. Q6: is HEADROOM-0 falsifiable, or a scalar scorecard?

The proponent's draft is preregistered, hashed and unchanged (sha256 `5e01f69d…`, checked again here). It has a
same-run comparator, a VOID gate, a witness before numbers, and apparatus falsifiers. That is more than my round 1
expected, and as a rule it is falsifiable: a run can read FAIL. `q6_headroom.py` applies it with the proponent's own
instrument (P9's three resident cells), unchanged, to two laws written to test the rule rather than the host.
- **SPIKE**: every 100th tick runs an inner loop of 100,000 steps; **SPIKE150** runs 150,000.
- **GROWTH**: tick t runs an inner loop of t steps (a world that accumulates).

| law | ticks | period | bound | p99 PLAY (11th largest) | label | beside, never read: over the bound / over the period / max |
|---|---|---|---|---|---|---|
| SPIKE | 11–1,010 | 1/60 s | 1,583 µs | 166.8 µs | PASS | 10 / 0 / 13,956 µs |
| SPIKE | 11–1,010 | 1/120 s | 792 µs | 166.8 µs | PASS | 10 / **10** / 13,956 µs |
| SPIKE150 | 11–1,010 | 1/60 s | 1,583 µs | 132.7 µs | PASS | 10 / **10** / 21,158 µs |
| SPIKE150 | 11–1,010 | 1/120 s | 792 µs | 132.7 µs | PASS | 10 / **10** / 21,158 µs |
| GROWTH | 11–1,010 | 1/60 s | 1,583 µs | 575.3 µs | PASS | 0 / 0 / 1,450 µs |
| GROWTH | 11–1,010 | 1/120 s | 792 µs | 575.3 µs | PASS | 2 / 0 / 1,450 µs |
| GROWTH | 4,011–5,010 | 1/60 s | 1,583 µs | 2,802.0 µs | **FAIL** | 409 / 0 / 3,835 µs |
| GROWTH | 4,011–5,010 | 1/120 s | 792 µs | 2,802.0 µs | **FAIL** | 1,000 / 0 / 3,835 µs |

- **Sources.** The SPIKE and GROWTH rows are run 1 (`q6_headroom-run1.txt`). SPIKE150 is in
  `q6_headroom-SPIKE-SPIKE150.txt`, beside a second SPIKE run. Run 2 of the full script (`q6_headroom.txt`, minutes
  after run 1) gave every label again:
  - SPIKE: PASS, p99 248.9 µs, max 15,532 µs;
  - GROWTH early: PASS, p99 542.8 µs;
  - GROWTH late: FAIL, p99 1,889.2 µs.
- **The witness held:** every PLAY and CHAIN line equals the reference's for every tick played. No reading was VOID:
  FLOOR's p99 was 67–108 µs.
- **The 1/120 s bound** is 950‰ × 100‰ × 8,333 µs = 791.6 µs, the proponent's 792.
- **Under amendment 1** (if R5's chain is kept, PLAY is the chain), the same rule on CHAIN reads PASS at both
  periods: SPIKE with ten ticks up to 35,078 µs, SPIKE150 with ten up to 58,781 µs, each over the 1/60 s period.

- **The label reads one order statistic of one window.**
  - p99 of 1,000 is the 11th largest, so up to ten ticks of any size never move the label. In SPIKE150, ten ticks of
    19.0–21.2 ms, each longer than the whole 1/60 s period and 12 to 13 times the bound, read PASS at both periods.
  - The window is ticks 11–1,010 of the recorded log. GROWTH reads PASS there, and FAIL on ticks 4,011–5,010 of the
    same run, on the same host, minutes apart. The draft samples the first 1,010 ticks of a log "of at least 1,010
    ticks" and says nothing about the rest of a session.
  - So HELD is a property of a law, a log, a window, a host and a sitting, and the draft's `does_not_show` omits the
    two things a player would ask: "that no tick overruns" and "any tick past the window".
- **The margin is smaller than the instrument's own drift.** The draft's margin is 50‰, "an engineering decision
  threshold". Two measurements of the drift:
  - Between the proponent's P9 sitting and mine, the same day, the same instrument's p99 moved by +37% (FLOOR), +29%
    (PLAY) and +60% (CHAIN).
  - Between my runs 1 and 2, minutes apart, GROWTH's late window read p99 2,802 then 1,889 µs (−33%), and p50 1,417
    then 938 µs. That is 409 then 61 samples over the 1/60 s bound, from the same law and the same ticks.

  The confirmation run 30 minutes later is the draft's guard. Two sittings that agree do not bound a third (Verðandi
  G13). MEASURED.
- **Scorecard or test?** It is a test, narrow and falsifiable, whose label behaves like a score. The label is driven
  by one number against one bound ("a p50 never moves the label", and neither does anything above p99). P9's fall,
  whose largest tick took 0.13 ms, and SPIKE150, whose ten largest took 19–21 ms, both read PASS. The label is what
  will travel.

**What would make it a standard of the lineage's kind**, as round 1's §6.4 had it (DECLARED):
1. **Counts, not only quantiles.** "Ticks over the period: 0 of every tick played", falsifiable by one tick, beside
   the p99.
2. **Every tick of the recorded session**, not a window, so that no regime is chosen.
3. **The margin wider than the drift measured on that host.**
4. **`does_not_show` adds** "that no tick overruns the period" and "any tick past the samples".

**Grade:** MEASURED (the two laws; the P9 rerun). **Severity:** overclaims, if PASS or HELD is read as headroom; costs
more than stated (C2).

---

## 8. Evidence

Run from `work/speed-adv/r2/` as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B <script>`; each writes the `.txt` (and most a
`.json`) of the same name there.

| file | what it holds | grade |
|---|---|---|
| `verify_tree.py`, `SNAPSHOT.txt` | my snapshot of f16dc26 against the commit's blobs: 719 files, 0 differ | MEASURED |
| `COPIED-FROM-SPEED-PROBE.sha256` | the proponent's scripts as copied, before the two marked changes | — |
| `p0.txt`, `p4.txt`, `p1.txt`, `p3.txt`, `p3b.txt`, `p5.txt`, `p6.txt`, `p7.txt`, `p8.txt`, `p9.txt`, `p10.txt`, `p11.txt`, `run_all.log` | the proponent's probes rerun (§1); `run_all.py`, then `run_all.py p6_u32_fix` and `run_all.py p3b_reference_bodies`; P0 and P4 alone | MEASURED |
| `q1_new_plants.py`, `.txt`, `.json` | A1–A4 against the full line; S1, S2 (printed B1, B2) receipts in four commitment modes; S3 (printed B3) localization under chain and stream (§2, §5) | MEASURED |
| `q2_state_cost.py`, `.txt`, `.json` | the state field on W(N), C and the reference (§3.2) | MEASURED |
| `q3_segments.py`, `.txt`, `.json` | segmented admission with four restores; the list law refused (§4.3, §4.4) | MEASURED |
| `q3b_certificate.py`, `.txt`, `.json` | the certificate accumulator against the line and segmented admission (§2.2 A5, §4.2) | MEASURED |
| `q6_headroom.py`; `q6_headroom-run1.txt`, `.json`; `q6_headroom-SPIKE-SPIKE150.txt`, `.json`; `q6_headroom.txt`, `.json` | HEADROOM-0's rule with P9's instrument, in order: run 1 on SPIKE and GROWTH (the script before the CHAIN reading was added, its output kept as `-run1`); `q6_headroom.py SPIKE SPIKE150`; run 2 of the full script, with the rule also applied to CHAIN (§7) | MEASURED |
| `../webleak/results/` | round 1's renderer leak, cited in §6.2 | MEASURED in round 1 |
| `scan_paths.py` | checks this report and every file of `r2/` for home-folder strings: 0 hits | — |

Disk: `work/speed-adv/r2/runs2/` and `work/speed-adv/r2/tmp/` hold the builds and run folders, about 350 MB in all,
ignored by git. Nothing in this report reads them after the runs, and they can be deleted.

---

## 9. What I concede from round 1, after reading the proponent and the survey

1. **A1 (per-tick heads are blind to `ops`) is answered.** The proponent's counters field names the tick where the
   counts part (P4, reproduced exactly). My severity ("breaks a guarantee") stands against R5 as written, not against
   the proposal. A3, the same counting defect shared by every compiled execution, is then named at its tick by the
   watch tier. It is named only as fast as the reference replays, which is A8's question.
2. **A2 (a reconciler of compiled backends shares their lowering) is answered for the watch tier,** which is the
   reference. It stands for any design that reconciles with compiled executions only (the survey's Knight and
   Leveson).
3. **A4 (a live outcome is one execution's) is stated honestly** in §1.4: the reference's record stands, and the
   competitive policy is the owner's, with "nothing after t* − 1 counts" recommended. The dilemma remains; it is now
   written down.
4. **A6 (localizing by whole traces does not scale) is answered.**
   - Lines compared in 1.5 ms over 40,000 ticks, and a window localized in 34 ms from the reference's own snapshot
     (reproduced).
   - The survey shows every shipped lockstep system splits detection from localization, so my round-1 framing, that
     per-tick commitments must be chain heads, was narrower than needed.
   - I also concede that a late detection is still a detection: Factorio and 0 A.D. ship deliberately incomplete
     digests. O1 is an overclaim, not a broken guarantee.
5. **A7 (the chain is 95–98% of a compiled tick):** both sides agree. But my round-1 dilemma was a false one: keep
   the chain and be slow, or drop it and commit nothing per tick. A per-tick stream is a third path. It cuts the
   commitment to 0.29–0.31 of the chain's on list-heavy ticks (reproduced) and still names every event-level
   divergence at its tick, provided B2 is fixed and O5 is accepted or remedied. The survey's finding that no shipped
   system keeps a per-assignment cryptographic chain in play points the same way.
6. **A8 (the reference cannot keep pace):** segments are a credible direction. The boundary induction is sound where
   the snapshot is complete, and the forged snapshot is caught (reproduced). B1, O3 and O8 are what remain.
7. **A9 (a refusal reachable from a port ends the match):** conceded on both sides. The proponent's "should", a port
   range the door enforces, is the remedy round 1 asked for.
8. **A19 (a headroom standard as a number):** HEADROOM-0 is a preregistered method, not a number. §7 is what remains.
9. **Agreements that need no concession:** A14 and A15 (no language swap; a GPU never the authority), A16 (operations
   are not time), A20 (no competitive claim), A13 (per-pixel work in the law is out by orders of magnitude; P5's costs
   agree), A22 (per-player output is needed; the proponent defers it).
10. **Maintained:**
    - A5: write-ahead does not touch who assigns inputs to ticks.
    - A10 and A11: §6.2.
    - A12: §6.1.
    - A17: P3b's bodies law has no floor, so its regime never changes.
    - A18's lesson: GROWTH is its descendant.
